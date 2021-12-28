#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author: Shiyu FAN
    @Usage: python3 dptocov.py [options]
"""
import pandas as pd
import argparse


def read_bed(bed_file: str):
    # Read bed file and constrct element structure dataframe
    element = pd.read_table(bed_file, header=None)
    element.columns = ["CHR", "START", "END", "ID", "CLASS"]
    element["START"] = element["START"] + 1
    return element


def compute_coverage(depth: list, min_reads: int):
    uncovered = 0
    if depth:
        for i in depth:
            if i < min_reads:
                uncovered += 1
    return float("%.4f" % (1 - uncovered/len(depth)))


def coverage(depth_file: str, element: pd.DataFrame, min_reads: int):
    list_cov = []
    dict_depth = {}
    depth = pd.read_table(depth_file, compression="gzip", header=None)
    depth.columns = ["CHR", "POS", "COUNT"]
    for i in element.CHR.unique():
        dict_depth[i] = depth[depth.CHR == i]
        dict_depth[i].index = dict_depth[i].POS
    for index, row in element.iterrows():
        list_depth = dict_depth[row.CHR].loc[row.START:row.END, "COUNT"].tolist()
        list_cov.append(compute_coverage(list_depth, min_reads))
    return list_cov


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--depth", type=str, help="Input depth file", required=True)
    parser.add_argument('-s', "--sample", type=str, help="Input single sample name", required=True)
    parser.add_argument('-b', "--bed", type=str, help="Input bed file", required=True)
    parser.add_argument('-t', "--threshold", type=float, help="Depth threshold", default=1)
    parser.add_argument('-o', "--output", type=str, help="Output file name")
    args = parser.parse_args()

    bed = read_bed(args.bed)
    cov = pd.DataFrame()
    cov[args.sample] = coverage(args.depth, bed, 1)
    cov.index = bed["ID"]
    if args.output:
        output = args.output
    else:
        output = args.sample + ".cov"
    cov.to_csv(output, sep="\t")
