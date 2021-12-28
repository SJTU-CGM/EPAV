#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author: Shiyu FAN
    @Usage: python3 getdepth.py [options]
"""
import os
import argparse


def samtools_depth(bed_file, bam_file, thread, depth_file):
    cmd = "samtools depth -@ %s -a -b %s %s | gzip > %s" % \
          (str(thread), bed_file, bam_file, depth_file)
    os.system(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bed', type=str, help="Input bed file name", required=True)
    parser.add_argument('-B', '--bam', type=str, help="Input bam file name", required=True)
    parser.add_argument('-t', '--thread', type=int, help="Thread number", default=1)
    parser.add_argument('-o', '--output', type=str, help="Output depth file name")
    args = parser.parse_args()

    if args.output:
        output = args.output
    else:
        output = args.bed.replace(".bam", ".depth.gz") \
            if ".bam" in args.bam else args.bam + ".depth.gz"
    samtools_depth(args.bed, args.bam, args.thread, output)
