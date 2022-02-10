#!/bin/bash

# 1.gfftobed module
python3 ../epav.py gfftobed \
  --gff pan.gff \
  --length pan.chrl \
  --region "CDS/5UTR/3UTR/UP2000/DOWN2000" \
  --bin 1000 \
  --output pan.bed

# 2.getdepth module
python3 ../epav.py getdepth \
  --bed pan.bed \
  --bam B001_mkdup.bam \
  --thread 1 \
  --output B001_mkdup.depth.gz

# 3.dptocov module
python3 ../epav.py dptocov \
  --depth B001_mkdup.depth.gz \
  --sample B001 \
  --bed pan.bed \
  --threshold 1 \
  --output B001.cov

# 4.covtopav module
python3 ../epav.py covtopav \
  --cov cov_demo \
  --bed pan.bed \
  --samples samples.txt \
  --threshold 0.95 \
  --output demo_pav_output

# 5.pavgwas module
python3 ../epav.py pavgwas \
  --vcf demo_pav_output/0.95.vcf \
  --phenotype rice_phe.txt \
  --output demo_gwas_output \
  --select "grain_weight/grain_width/height"

# 6.plot module
python3 ../epav.py plot \
  --pav demo_pav_output/0.95.pav \
  --phenotype rice_phe.txt \
  --select "grain_weight/grain_width/height" \
  --output demo_plot_output

python3 ../epav.py plot \
  --gwas demo_gwas_output/height_emmax.ps \
  --output demo_plot_output