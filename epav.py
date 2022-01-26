#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author: Shiyu FAN
    @Usage: python3 epav.py [command] [options]
"""
import argparse
import os
import sys

DESCRIPTION = """
Element Presence-Absence Variation analysis toolkit (EPAV)
"""
VERSION = "Version 1.0"

if __name__ == "__main__":
    dir_name, file_name = os.path.split(os.path.abspath(sys.argv[0]))
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-v', '--version', action='version', version=VERSION)

    sub_parser = parser.add_subparsers(dest='subcmd', title='sub commands')

    # GffToBed
    parser_gtb = sub_parser.add_parser("gfftobed", help='Convert gff to bed format based on chosen '
                                                        'gene element, e.g. gene/transcript/mRNA/EXON/CDS/'
                                                        '5UTR/3UTR/upstream or downstream n kb region.')
    parser_gtb.add_argument('-g', '--gff', metavar='<annotation.gff>',
                            help='Input gff file', type=str, required=True)
    parser_gtb.add_argument('-l', '--chrl', metavar='<chr_length>',
                            help='Chromosome length table', type=str, required=True)
    parser_gtb.add_argument('-r', '--region', metavar='<region>',
                            help='List of gene element in gff file seperated by "/". e.g., CDS/EXON/UP2000/DOWN1000',
                            type=str, required=True)
    parser_gtb.add_argument('-b', '--bin', metavar='<bin>',
                            help='The interval width of bin for gene upstream and downstream regions',
                            type=int)
    parser_gtb.add_argument('-o', '--output', metavar='<annotation.bed>',
                            help='Output bed file', type=str)

    # GetDepth
    parser_dp = sub_parser.add_parser("getdp", help='Use samtools depth to get mapping depth of each base '
                                                    'in each chosen gene element.')
    parser_dp.add_argument('-b', '--bed', metavar='<bed>',
                           help='Input bed file', type=str, required=True)
    parser_dp.add_argument('-B', '--bam', metavar='<sample.bam>',
                           help='Input bam file', type=str, required=True)
    parser_dp.add_argument('-t', '--thread', metavar='<thread>',
                           help='Thread number', type=int)
    parser_dp.add_argument('-o', '--output', metavar='<output>',
                           help='Output depth file', type=str)

    # DepthToCoverage
    parser_dtp = sub_parser.add_parser("dptocov", help='Compute coverage of each gene element. Base position '
                                                       'with depth under threshold is considered as uncovered')
    parser_dtp.add_argument('-b', '--bed', metavar='<bed>',
                            help='Input bed file', type=str, required=True)
    parser_dtp.add_argument('-d', '--depth', metavar='<depth>',
                            help='Input depth file', type=str, required=True)
    parser_dtp.add_argument('-s', '--sample', metavar='<sample>',
                            help='Single sample name', type=str)
    parser_dtp.add_argument('-t', '--threshold', metavar='<threshold>',
                            help='Depth threshold', type=int)
    parser_dtp.add_argument('-o', '--output', metavar='<output>',
                            help='Output coverage file directory', type=str)

    # CoverageToPAV
    parser_ctp = sub_parser.add_parser("covtopav", help='Determine presence or absence of each gene element. Element '
                                                        'with coverage under threshold is considered as absence')
    parser_ctp.add_argument('-c', '--cov', metavar='<cov>',
                            help='Input coverage file directory', type=str, required=True)
    parser_ctp.add_argument('-b', '--bed', metavar='<bed>',
                            help='Input bed file', type=str, required=True)
    parser_ctp.add_argument('-s', '--samples', metavar='<samples>',
                            help='Input sample names in a text file, each sample name in a single line', type=str)
    parser_ctp.add_argument('-t', '--threshold', metavar='<threshold>',
                            help='Coverage threshold', type=float)
    parser_ctp.add_argument('-o', '--output', metavar='<output>',
                            help='Output PAV file directory', type=str)

    # PAV-GWAS
    parser_pg = sub_parser.add_parser("pavgwas", help='Use EMMAX to apply PAV-GWAS')
    parser_pg.add_argument('-v', '--vcf', metavar='<pav.vcf>',
                           help='Input PAV vcf file', type=str, required=True)
    parser_pg.add_argument('-p', '--phenotype', metavar='<phe.txt>',
                           help='Input phenotype file', type=str, required=True)
    parser_pg.add_argument('-o', '--output', metavar='<output>',
                           help='Output directory', type=str, required=True)
    parser_pg.add_argument('-t', '--select', type=str,
                           help="Selected phenotype, seperated by /, e.g. height/width/weight")
    parser_pg.add_argument('-s', '--seperate', type=str,
                           help="Seperating symbol in phenotype file")
    parser_pg.add_argument('-m', '--miss', type=str,
                           help="Missing value in phenotype file")
    parser_pg.add_argument('-f', '--maf', type=float,
                           help="MAF threshold")

    # Plot
    parser_pt = sub_parser.add_parser("plot", help='Visualize EPAV result')
    parser_pt.add_argument('-p', '--pav',
                           help="Input pav file", type=str)
    parser_pt.add_argument('-q', '--phenotype',
                           help="Input phenotype file", type=str)
    parser_pt.add_argument('-s', '--select',
                           help="Selected phenotypes, seperated by '/'", type=str)
    parser_pt.add_argument('-g', '--gwas',
                           help="GWAS result file", type=str)
    parser_pt.add_argument('-o', '--output',
                           help="Output directory", required=True, type=str)
    parser_pt.add_argument('--height',
                           help="Plot height", type=float)
    parser_pt.add_argument('--width',
                           help="Plot width", type=float)
    parser_pt.add_argument('--cthreshold',
                           help="Core element threshold", type=float)
    parser_pt.add_argument('--sthreshold',
                           help="Softcore element threshold", type=float)
    parser_pt.add_argument('--suggestive',
                           help="Suggestive line p value", type=float)
    parser_pt.add_argument('--annotation',
                           help="Annotation p value", type=float)

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        exit()

    args = vars(parser.parse_args())
    command = "%s %s/lib/%s.py " % (sys.executable, dir_name, args["subcmd"])
    command += ' '.join(sys.argv[2:])
    os.system(command)
    exit()
