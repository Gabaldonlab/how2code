#Basic rules

rule download_data:
    output:
        a = "data/input.1.fastq",
        b = "data/input.2.fastq",
        ref = "data/ref.fa"
    shell:
        "mkdir data"
        "wget -O {output.a} https://github.com/Gabaldonlab/redundans/blob/master/test/5000_1.fq.gz;"
        "wget -O {output.b} https://github.com/Gabaldonlab/redundans/blob/master/test/5000_1.fq.gz;"
        "wget -O {output.ref} https://github.com/Gabaldonlab/redundans/blob/master/test/ref.fa;"

rule align_sequences:
    input:
        a =  rules.download_data.output.a,
        b = rules.download_data.output.b,
        ref = rules.download_data.output.ref
    output:
        "results/aligned.bam"

    threads: 4
    shell:
        "mkdir results"
        "bwa index {input.ref}"
        "bwa mem -t {threads} {input.ref} {input.a} {input.b} | samtools view -b - > {output}"

#Main rule to be called to infer the dependency of rules
rule all:
    input:
        "results/aligned.bam"