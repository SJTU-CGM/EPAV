#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    @Author: Shiyu FAN
    @Usage: python3 plot.py [options]
"""
import argparse
import os


def plot_heatmap(pav_file, phenotype_file, selected_phenotype, output, plot_height, plot_width):
    cmd = "Rscript lib/plot_heatmap.R %s %s %s %s %s %s" % \
          (pav_file, phenotype_file, selected_phenotype, output, plot_height, plot_width)
    os.system(cmd)


def plot_hist(pav_file, threshold_core, threshold_softcore, output, plot_height, plot_width):
    cmd = "Rscript lib/plot_hist.R %s %s %s %s %s %s" % \
          (pav_file, threshold_core, threshold_softcore, output, plot_height, plot_width)
    os.system(cmd)


def plot_pca(pav_file, phenotype_file, selected_phenotype, center, scale, output, plot_height, plot_width):
    cmd = "Rscript lib/plot_pca.R %s %s %s %s %s %s %s %s" % \
          (pav_file, phenotype_file, selected_phenotype, center, scale, output, plot_height, plot_width)
    os.system(cmd)


def plot_manhattan(gwas_file, suggestive_line, annotate_pval, output, plot_height, plot_width):
    cmd = "Rscript lib/plot_manhattan.R %s %s %s %s %s %s" % \
          (gwas_file, suggestive_line, annotate_pval, output, plot_height, plot_width)
    os.system(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pav', type=str,
                        help="Input pav file")
    parser.add_argument('-q', '--phenotype', type=str,
                        help="Input phenotype file")
    parser.add_argument('-s', '--select', type=str,
                        help="Selected phenotypes, seperated by '/'")
    parser.add_argument('-g', '--gwas', type=str,
                        help="GWAS result file")
    parser.add_argument('-o', '--output', type=str,
                        help="Output directory")
    parser.add_argument('--height', type=float,
                        help="Plot height", default=10)
    parser.add_argument('--width', type=float,
                        help="Plot width", default=8)
    parser.add_argument('--cthreshold', type=float,
                        help="Core element threshold", default=1)
    parser.add_argument('--sthreshold', type=float,
                        help="Softcore element threshold", default=0.9)
    parser.add_argument('--suggestive', type=float,
                        help="Suggestive line p value", default=0.00001)
    parser.add_argument('--annotation', type=float,
                        help="Annotation p value", default=0.00001)
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    if args.pav and args.phenotype and args.select:
        plot_heatmap(args.pav,
                     args.phenotype,
                     args.select,
                     args.output + "/heatmap.pdf",
                     args.height,
                     args.width)
        plot_pca(args.pav,
                 args.phenotype,
                 args.select,
                 "TRUE",
                 "FALSE",
                 args.output + "/pcv.pdf",
                 args.height,
                 args.width)
        plot_hist(args.pav,
                  args.cthreshold,
                  args.sthreshold,
                  args.output + "/hist.pdf",
                  args.height,
                  args.width)

    if args.gwas:
        plot_manhattan(args.gwas,
                       args.suggestive,
                       args.annotation,
                       args.output + "/manhattan.pdf",
                       args.height,
                       args.width)
