#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author: Shiyu FAN
    @Usage: python3 covtopav.py [options]
"""
import os
import pandas as pd
import argparse
from dptocov import read_bed


def merge_coverage(cov_dir, samples):
    res = pd.DataFrame()
    for sample in samples:
        res[sample] = pd.read_table("%s/%s.cov" % (cov_dir, sample))[sample]
    res.index = pd.read_table("%s/%s.cov" % (cov_dir, samples[0]))["ID"]
    return res


def pav_to_vcf(pav_table: pd.DataFrame, bed_file: str):
    bed = read_bed(bed_file)
    bed.index = bed.ID
    bed.START = bed.START + 1
    res = "##fileformat=VCFv4.2\n"
    res += "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT"
    for sample in pav_table.columns:
        res += "\t" + sample
    res += "\n"
    for index, row in pav_table.iterrows():
        bed_row = bed.loc[index]
        res += "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (bed_row["CHR"], bed_row["START"],
                                                       bed_row["ID"], "<PRE>", "<ABS>",
                                                       99, ".", bed_row["CLASS"], "GT")
        for i in row:
            res += "\t0|0" if i == 1 else "\t1|1"
        res += "\n"
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', "--cov", type=str, help="Input coverage directory", required=True)
    parser.add_argument('-b', "--bed", type=str, help="Input bed file", required=True)
    parser.add_argument('-s', "--samples", type=str, help="Input sample names")
    parser.add_argument('-t', "--threshold", type=float, help="Coverage threshold for presence/absence",
                        default=0.95)
    parser.add_argument('-o', "--output", type=str, help="Output directory")
    args = parser.parse_args()

    output = args.output if args.output else args.cov
    if not os.path.exists(output):
        os.mkdir(output)

    # Merge coverage to a coverage table
    list_sample = []
    if args.samples:
        for line in open(args.samples, 'rt').readlines():
            list_sample.append(line.strip())
    else:
        list_sample = ' '.join(filter(lambda val: '.cov' in val, os.listdir(args.cov))).replace(".cov", "").split()
    cov = merge_coverage(args.cov, list_sample)
    cov.to_csv("%s/gene_elements.cov" % output, sep="\t")
    # Determine presence or absence variation based on coverage threshold
    pav = cov.applymap(lambda x: 1 if x > args.threshold else 0)
    pav.to_csv("%s/%s.pav" % (output, str(args.threshold)), sep="\t")
    # Output core gene elements and distributed gene elements
    pav[pav.apply(lambda x: x.sum() == len(pav.columns), axis=1)].\
        to_csv("%s/%s_core.pav" % (output, str(args.threshold)), sep="\t")
    pav[pav.apply(lambda x: x.sum() < len(pav.columns), axis=1)].\
        to_csv("%s/%s_distributed.pav" % (output, str(args.threshold)), sep="\t")
    pav[pav.apply(lambda x: 0.9 * len(pav.columns) <= x.sum() < len(pav.columns), axis=1)].\
        to_csv("%s/%s_softcore.pav" % (output, str(args.threshold)), sep="\t")
    pav[pav.apply(lambda x: 1 < x.sum() <= 0.9 * len(pav.columns), axis=1)].\
        to_csv("%s/%s_cloud.pav" % (output, str(args.threshold)), sep="\t")
    pav[pav.apply(lambda x: x.sum() == 1, axis=1)].\
        to_csv("%s/%s_unique.pav" % (output, str(args.threshold)), sep="\t")
    # Transfer PAV table to vcf format
    vcf = pav_to_vcf(pav, args.bed)
    open("%s/%s.vcf" % (output, str(args.threshold)), 'wt').write(vcf)
