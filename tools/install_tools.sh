#!/bin/bash

TOOL_ROOT=$(dirname "$0")

# Install SAMtools
wget -c "https://github.com/samtools/samtools/releases/download/1.14/samtools-1.14.tar.bz2"
tar -jxvf samtools-1.14.tar.bz2
cd samtools-1.14 && ./configue
make
make install
echo "export PATH=$PATH:$PWD" >> ~/.bash_profile
cd "$TOOL_ROOT" || exit

# Install PLINK
wget -c "https://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20210606.zip"
unzip -d plink_linux_x86_64_20210606.zip
cd plink_linux_x86_64_20210606 || exit
echo "export PATH=$PATH:$PWD" >> ~/.bash_profile
cd "$TOOL_ROOT" || exit

# Install EMMAX
wget -c "http://csg.sph.umich.edu/kang/emmax/download/emmax-beta-07Mar2010.tar.gz"
tar -zxvf emmax-beta-07Mar2010.tar.gz
cd emmax-beta-07Mar2010 || exit
echo "export PATH=$PATH:$PWD" >> ~/.bash_profile
cd "$TOOL_ROOT" || exit

source "$HOME"/.bash_profile