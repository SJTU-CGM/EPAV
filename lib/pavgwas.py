#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author: Shiyu FAN
    @Usage: python3 pavgwas.py [options]
"""
import subprocess
import argparse
import os
import pandas as pd


def plink_preprocess(vcf_file, prefix, maf):
    cmd = "plink --vcf %s --out %s_tmp --double-id --allow-extra-chr && " % (vcf_file, prefix)
    cmd += "plink --bfile %s_tmp --out %s --make-bed --allow-extra-chr && " % (prefix, prefix)
    cmd += "plink --bfile %s --maf %s --make-bed --out %s_tmp --allow-extra-chr && " % (prefix, maf, prefix)
    cmd += "plink --bfile %s_tmp --recode vcf-iid --out %s --allow-extra-chr && " % (prefix, prefix)
    cmd += "plink --vcf %s.vcf --recode 12 transpose --output-missing-genotype 0 --out %s " \
           "--autosome-num 90 --allow-extra-chr --double-id" % (prefix, prefix)
    subprocess.call(cmd)


def add_phenotype(fam, select, phe, sep, miss):
    phe_table = pd.read_table(phe)
    fam = pd.read_csv(fam, sep=sep, header=None)

    for index, row in phe_table.iterrows():
        fam.loc[fam[1] == row["sample"], 5] = row[select]

    fam.fillna(miss).to_csv(fam, header=False, index=False, sep=sep)


def emmax_gwas(prefix):
    cmd = "emmax-kin -v -h -d 10 %s && " % prefix
    cmd += "emmax -v -d 10 -t %s -p %s.fam -k %s.hBN.kinf -o %s" % (prefix, prefix, prefix, prefix)
    subprocess.call(cmd)
    # Merge .bim .ps
    ps = pd.read_table("%s.ps" % prefix, header=None)
    ps.columns = ["id", "beta", "pval"]
    bim = pd.read_table("%s.bim" % prefix, header=None)
    bim.columns = ["chr", "id", "val", "pos", "ref", "alt"]
    res = pd.merge(ps, bim, on="id")
    res = res[["id", "chr", "pos", "pval", "beta", "ref", "alt"]]
    # Output p-value file
    res.to_csv("%s_emmax.ps" % prefix, header=True, index=False, sep="\t")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', type=str,
                        help="Input vcf file", required=True)
    parser.add_argument('-p', '--phenotype', type=str,
                        help="Input phenotype file", required=True)
    parser.add_argument('-o', '--output', type=str,
                        help="Output directory", required=True)
    parser.add_argument('-t', '--select', type=str,
                        help="Selected phenotype, seperated by /, e.g. height/width/weight")
    parser.add_argument('-s', '--seperate', type=str,
                        help="Seperating symbol in phenotype file", default="\t")
    parser.add_argument('-m', '--miss', type=str,
                        help="Missing value", default="NA")
    parser.add_argument('-f', '--maf', type=float,
                        help="MAF threshold", default=0.05)
    args = parser.parse_args()

    if args.select:
        phenotype = args.select.split("/")
    else:
        phenotype = open(args.phenotype, 'rt').readline().strip().split(args.seperate)

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    for i in phenotype:
        plink_preprocess(args.vcf, "%s/%s" % (args.output, i), args.maf)
        add_phenotype("%s/%s.tfam" % (args.output, i), i, args.phenotype, args.seperate, args.miss)
        emmax_gwas("%s/%s" % (args.output, i))
