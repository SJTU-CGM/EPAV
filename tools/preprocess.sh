#!/bin/bash

THREADS=24
MEM=2G
ref=$1
sample=$2
fastq1=$3
fastq2=$4

bwa mem -M -t $THREADS "$ref" "$fastq1" "$fastq2" \
  | samtools view -@ $THREADS -bS \
  | samtools sort -@ $THREADS -m $MEM -o "$sample".bam -O bam -T sorted

samtools view -H "$sample".bam  | grep @SQ \
  | awk '{print $2"\t"$3}' | sed 's/SN://g' | sed 's/LN://g' > "$sample".chrl
