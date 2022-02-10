#!/bin/bash

wget -c "https://cgm.sjtu.edu.cn/epav/demo/pan.gff"
wget -c "https://cgm.sjtu.edu.cn/epav/demo/pan.chrl"
wget -c "https://cgm.sjtu.edu.cn/epav/demo/rice_phe.txt"
wget -c "https://cgm.sjtu.edu.cn/epav/demo/demo_cov.tar.gz" && tar -zxvf demo_cov.tar.gz
wget -c "https://cgm.sjtu.edu.cn/epav/demo/B001_mkdup.bam"