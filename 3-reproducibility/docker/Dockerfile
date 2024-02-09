FROM python:3.9.1
#Image in buster flavor
# metadata
LABEL base.image="python:3.9.1"
LABEL version="1.0.0"
LABEL software="testing_docker"
LABEL software.version="Latest:1.0.0"
LABEL description="Test a dockerfile generation "
LABEL website="https://github.com/Gabaldonlab/how2code"
LABEL license="GNU General Public License 3.0"
LABEL maintainer="Diego Fuentes (BSC)"
##Set up bash and install basic dependencies
SHELL ["/bin/bash", "-c"]
#RUN apt update && apt install -y software-properties-common
RUN apt-get update && apt-get install -y openjdk-11-jre-headless && apt-get clean
RUN apt-get update -qq && apt-get install -y perl default-jre python3-pip make nano automake wget git g++ zlib1g-dev libbz2-dev libncurses5-dev libncursesw5-dev liblzma-dev
##Install from source htslib, samtools, trimmomatic, hisat2, Kraken2, KrakenTools, Bracken, Krona
RUN cd /bin && wget https://github.com/samtools/htslib/releases/download/1.16/htslib-1.16.tar.bz2 && tar -vxjf htslib-1.16.tar.bz2 && rm htslib-1.16.tar.bz2 && cd htslib-1.16 && make install
RUN cd /bin && wget https://github.com/samtools/samtools/releases/download/1.13/samtools-1.13.tar.bz2 && tar -vxjf samtools-1.13.tar.bz2  && rm samtools-1.13.tar.bz2 && cd samtools-1.13 && make install
RUN cd /bin && wget http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.12.1.zip && unzip fastqc_v0.12.1.zip  && rm fastqc_v0.12.1.zip  
RUN cd /bin && wget https://github.com/usadellab/Trimmomatic/files/5854859/Trimmomatic-0.39.zip && \
        unzip Trimmomatic-0.39.zip && rm Trimmomatic-0.39.zip && \
        #Added the following alias for nomenclature sake in the snakemake rules
        echo "alias trimmomatic='java -jar /bin/Trimmomatic-0.39/trimmomatic-0.39.jar'" >> ~/.bash_aliases && \
        echo "source ~/.bash_aliases" >> ~/.bashrc
RUN cd /bin && wget https://github.com/DaehwanKimLab/hisat2/archive/refs/tags/v2.2.1.tar.gz && tar -zxvf v2.2.1.tar.gz && rm v2.2.1.tar.gz && cd hisat2-2.2.1/ && make
#Copy the hisat dependencies to /bin path
RUN cd /bin/hisat2-2.2.1/ && cp ./hisat2-build* ./hisat2-inspect* ./hisat2-repeat* ./hisat2-align* ./hisat2 /bin/
#Install python packages
RUN python3 -m pip install --upgrade pip && pip3 install --upgrade numpy pysam biopython pandas pandarallel pybedtools
#Test that every dependency is working as intended 
RUN export PATH="/bin/"
RUN hisat2-build -h
RUN samtools --version
RUN java -jar /bin/Trimmomatic-0.39/trimmomatic-0.39.jar PE -version
RUN /bin/FastQC/fastqc --help

