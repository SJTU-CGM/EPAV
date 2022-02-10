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
   
    Python package [pandas][1] is needed. Follow the Installation step, 
    or you can install the package by yourself.
   
 - R 3.6 or later (https://www.r-project.org/)
    
    R is utilized for visualization and statistical tests in EPAV
    toolbox. Please install R first and make sure R and Rscript are
    under your PATH.

 - R packages 

    R packages [ggplot2][2], [ggrepel][3] and [ComplexHeatmap][4] are needed. 
    Follow the Installation step, or you can install the packages by yourself.
   
 - Supporting software

    Supporting software [Samtools][5], [PLINK][6] and [EMMAX][7] are needed. 
    Follow the Installation step, or you can install the software by yourself.

**Installation procedures** 
```
## install EPAV
git clone --recursive https://github.com/SJTU-CGM/EPAV

## install supporting tools
cd ${EPAV_PATH}/tools && bash install_tools.sh
pip3 install pandas
Rscript ${EPAV_PATH}/tools/install_r_packages.R
```

Workflow
------------
<img src="https://github.com/SJTU-CGM/EPAV/blob/master/workflow.png"
width=800/>

**Usage**
```
python3 ${EPAV_PATH}/epav.py [command] [options]

    ## Available commands:
            gfftobed        Convert gff to bed format based on chosen element.
            getdp           Get mapping depth of each base in each chosen gene element.
            dptocov         Compute coverage of each gene element.
            covtopav        Determine presence or absence of each gene element.
            pavgwas         Apply PAV-GWAS.
            plot            Visualize EPAV result.

## get help
python3 ${EPAV_PATH}/epav.py --help
python3 ${EPAV_PATH}/epav.py [command] --help
```

**Demo**

Follow the instructions below to run the demo.
```
cd ${EPAV_PATH}/demo

# 1.Download example data
bash download_example_data.sh

# 2.Run demo
bash run_demo.sh
```



[1]: https://pandas.pydata.org/
[2]: https://github.com/tidyverse/ggplot2
[3]: https://github.com/slowkow/ggrepel
[4]: https://github.com/jokergoo/ComplexHeatmap
[5]: https://github.com/samtools/samtools
[6]: https://www.cog-genomics.org/plink2
[7]: https://genome.sph.umich.edu/wiki/EMMAX