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
**Requirements**

 - Python 3.6 or later (https://www.python.org/)
    
 - Python package
   
    Python package *pandas* is needed. Follow the Installation step, 
    or you can install the package by yourself.
   
 - R 3.6 or later (https://www.r-project.org/)
    
    R is utilized for visualization and statistical tests in EPAV
    toolbox. Please install R first and make sure R and Rscript are
    under your PATH.

 - R packages 

    Several R packages are needed including *ggplot2*, *ggrepel*
    and *ComplexHeatmap* packages. Follow the Installation step, 
    or you can install the packages by yourself.

**Installation procedures** 
```
## install EPAV
git clone --recursive https://github.com/SJTU-CGM/EPAV

## install supporting tools
cd ${EPAV_PATH}/tools && bash install_tools.sh
pip3 install pandas
Rscript ${EPAV_PATH}/tools/install_r_packages.R

## get help
python3 ${EPAV_PATH}/epav.py --help
python3 ${EPAV_PATH}/epav.py [command] --help
```

Workflow
------------
<img src="https://github.com/SJTU-CGM/EPAV/blob/master/workflow.png"
width=800/>
