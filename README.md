EPAV : Element Presence-Absence Variation analysis
============
EPAV is a pan-genome analysis pipeline using presence-absence 
variations(PAVs) of small genomic elements inside or in 
flanking regions of genes instead of the whole genes. It is 
capable to capture more genotype-phenotype associations in the 
map-to-pan alignments than traditional gene PAV analysis pipeline.
Altering PAV unit from gene to more detailed functional segments 
or elements might lead to more biological insights.

EPAV takes map-to-pan alignments and BED format element 
coordinates as standard input. It computes coverage of each element
and reports element PAVs in PAV table and VCF format. Then it 
serves as a toolbox for further element PAVs analysis including
PCA and element PAV-GWAS.

<img src="https://github.com/SJTU-CGM/EPAV/blob/master/main.png"
width=800/>

Installation
------------

Usage
------------

