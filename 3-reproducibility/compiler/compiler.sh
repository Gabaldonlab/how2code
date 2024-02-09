#!/bin/sh

###Example of a compiler script: how2code tutorial

SELF="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

SPAdes_VERSION=3.9.0
TRIMMOMATIC_VERSION=0.36
PICARD_VERSION=1.78


mkdir dependencies
chmod 777 dependencies
cd dependencies
dep_folder=`pwd`

#Installins SPADes
echo "#################"
echo "Installing SPADes"
echo "#################"
SPAdes_VERSION=3.9.0
wget https://github.com/ablab/spades/releases/download/v$SPAdes_VERSION/SPAdes-$SPAdes_VERSION-Linux.tar.gz
tar -xvf SPAdes-$SPAdes_VERSION-Linux.tar.gz

#Installing SOAPdeNovo
echo "#####################"
echo "Installing SOAPdeNovo"
echo "#####################"
wget https://downloads.sourceforge.net/project/soapdenovo2/SOAPdenovo2/bin/r240/SOAPdenovo2-bin-LINUX-generic-r240.tgz
tar -xvf SOAPdenovo2-bin-LINUX-generic-r240.tgz

echo "####################"
echo "Installing Platanus"
echo "####################"
mkdir platanus-1.2.4
mkdir platanus-1.2.4/bin
cd platanus-1.2.4/bin
wget -O- http://platanus.bio.titech.ac.jp/?ddownload=145 > platanus && chmod +x platanus
cd $SELF/../dependencies

#Installing nQuire
echo "#################"
echo "Installing nQuire"
echo "#################"
git clone --recursive https://github.com/clwgg/nQuire.git
chmod 777 nQuire
cd nQuire
make submodules
make
cd ..

#Installing Trimmomatic
echo "Installing Trimmomatic"
wget http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/Trimmomatic-$TRIMMOMATIC_VERSION.zip
unzip Trimmomatic-$TRIMMOMATIC_VERSION.zip

#####hint https://github.com/usadellab/Trimmomatic/archive/refs/tags/v0.39.tar.gz

#Installing Picard-tools
echo "Installing Picard-Tools"
wget https://downloads.sourceforge.net/project/picard/picard-tools/$PICARD_VERSION/picard-tools-$PICARD_VERSION.zip
unzip picard-tools-$PICARD_VERSION.zip

