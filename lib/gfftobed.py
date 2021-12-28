#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author: Shiyu FAN
    @Usage: python3 gfftobed.py [options]
"""
import argparse
import pandas as pd


class RegionList(object):
    def __init__(self, regions, region_bin):
        self.upflag, self.downflag = False, False
        self.upinterval, self.downinterval = [], []
        self.up_bound, self.down_bound = 0, 0
        self.in_gene_regions = []

        for i in regions:
            if "UP" in i:
                self.upflag = True
                width = int(i.strip("UP"))
                self.up_bound = -width
                if width <= region_bin:
                    self.upinterval.append([-width, -1])
                else:
                    if width % region_bin != 0:
                        self.upinterval.append([-width, -int(width/region_bin)*region_bin-1])
                    for j in reversed(range(int(width/region_bin))):
                        self.upinterval.append([-region_bin*(j+1), -region_bin*j-1])
            elif "DOWN" in i:
                self.downflag = True
                width = int(i.strip("DOWN"))
                self.down_bound = width
                if width <= region_bin:
                    self.downinterval.append([1, width])
                else:
                    for j in range(int(width/region_bin)):
                        self.downinterval.append([region_bin*j+1, region_bin*(j+1)])
                    if width % region_bin != 0:
                        self.downinterval.append([int(width/region_bin)*region_bin-1, width])
            else:
                self.in_gene_regions.append(i)

    def get_in_gene_regions(self):
        return self.in_gene_regions

    def is_extend(self):
        return self.upflag or self.downflag

    def is_up_extend(self):
        return self.upflag

    def get_up_interval(self):
        return self.upinterval

    def is_down_extend(self):
        return self.downflag

    def get_down_interval(self):
        return self.downinterval

    def get_up_bound(self):
        return self.up_bound

    def get_down_bound(self):
        return self.down_bound


def struct(element_id, element_chr, start, end, element_class):
    return {"ID": element_id,
            "CHR": element_chr,
            "START": start,
            "END": end,
            "CLASS": element_class}


def transfer_gff_to_bed(gff_file: str, chrl_file: str, regions: str, region_bin: int, bed_output: str):
    gff_structure = pd.read_table(gff_file, header=None).loc[:, [0, 3, 4, 8, 2]]
    gff_structure.columns = ["CHR", "START", "END", "ID", "CLASS"]

    chrl = pd.read_table(chrl_file, header=None)

    # Parse selected regions
    region_list = RegionList(regions.split("/"), region_bin)
    # Initialization
    cur_gene_id, cur_gene_chr = "", ""
    cur_index, cur_gene_start, cur_gene_end = 0, 0, 0
    tmp_list = []
    # Traverse the gff file to generate bed file
    for index, row in gff_structure.iterrows():
        if row["END"] - row["START"] < 2:
            continue
        if row["CLASS"] == "gene":
            # Add downstream regions of the previous gene
            if cur_gene_id != "" and region_list.is_down_extend():
                cur_chrl = chrl[chrl[0] == cur_gene_chr].iloc[0, 1]
                if cur_gene_end + region_list.get_down_bound() > cur_chrl:
                    tmp_list.append(struct(cur_gene_id + "_" + str(cur_index),
                                           cur_gene_chr,
                                           cur_gene_end + 1,
                                           cur_chrl,
                                           "downstream"))
                else:
                    for i in region_list.get_down_interval():
                        tmp_list.append(struct(cur_gene_id + "_" + str(cur_index),
                                               cur_gene_chr,
                                               cur_gene_end + i[0],
                                               cur_gene_end + i[1],
                                               "downstream"))
                        cur_index += 1
            # Record current gene information
            cur_gene_id = row["ID"].replace("ID=", "")
            cur_gene_chr, cur_gene_start, cur_gene_end = row["CHR"], row["START"], row["END"]
            cur_index = 0
            # Add upstream regions of the current gene
            if region_list.is_up_extend():
                if cur_gene_start + region_list.get_up_bound() > 0:
                    for i in region_list.get_up_interval():
                        tmp_list.append(struct(cur_gene_id + "_" + str(cur_index),
                                               cur_gene_chr,
                                               cur_gene_start + i[0],
                                               cur_gene_end + i[1],
                                               "upstream"))
                        cur_index += 1
                else:
                    tmp_list.append(struct(cur_gene_id + "_" + str(cur_index),
                                           cur_gene_chr,
                                           0,
                                           cur_gene_start - 1,
                                           "upstream"))
        # Add gene element
        if row["CLASS"] in region_list.get_in_gene_regions():
            tmp_list.append(struct(cur_gene_id + "_" + str(cur_index),
                                   cur_gene_chr,
                                   row["START"],
                                   row["END"],
                                   row["CLASS"]))
            cur_index += 1
    # Add downstream regions of the last gene
    if region_list.is_down_extend():
        cur_chrl = chrl[chrl[0] == cur_gene_chr].iloc[0, 1]
        if cur_gene_end + region_list.get_down_bound() > cur_chrl:
            tmp_list.append(struct(cur_gene_id + "_" + str(cur_index),
                                   cur_gene_chr,
                                   cur_gene_end + 1,
                                   cur_chrl,
                                   "downstream"))
        else:
            for i in region_list.get_down_interval():
                tmp_list.append(struct(cur_gene_id + "_" + str(cur_index),
                                       cur_gene_chr,
                                       cur_gene_end + i[0],
                                       cur_gene_end + i[1],
                                       "downstream"))
                cur_index += 1

    # Output bed file
    bed = pd.DataFrame(columns=["CHR", "START", "END", "ID", "CLASS"])
    bed = bed.append(tmp_list)
    bed["START"] = bed["START"] - 1
    bed.to_csv(bed_output, index=False, sep="\t", header=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gff', type=str, help="Input gff file name", required=True)
    parser.add_argument('-l', '--length', type=str, help="Chromosome length table", required=True)
    parser.add_argument('-r', '--region', type=str, help="Selected gene elements", required=True)
    parser.add_argument('-b', '--bin', type=int, help="Bin width", default=1000)
    parser.add_argument('-o', '--output', type=str, help="Output bed file name")
    args = parser.parse_args()

    if args.output:
        output = args.output
    else:
        output = args.gff.replace(".gff", ".bed") if ".gff" in args.gff else args.gff + ".bed"

    transfer_gff_to_bed(args.gff, args.length, args.region, args.bin, output)

