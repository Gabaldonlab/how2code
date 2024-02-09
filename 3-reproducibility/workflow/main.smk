#Basic rules

rule download_data:
    output:
        a = "data/input.1.fastq.gz",
        b = "data/input.2.fastq.gz",
        ref = "data/ref.fa"
    shell:
        "wget -O {output.a} https://raw.githubusercontent.com/Gabaldonlab/redundans/master/test/5000_1.fq.gz;"
        "wget -O {output.b} https://raw.githubusercontent.com/Gabaldonlab/redundans/master/test/5000_1.fq.gz;"
        "wget -O {output.ref} https://raw.githubusercontent.com/Gabaldonlab/redundans/master/test/ref.fa;"

rule align_sequences:
    input:
        a =  rules.download_data.output.a,
        b = rules.download_data.output.b,
        ref = rules.download_data.output.ref
    output:
        "aligned.bam"
    threads: 4
    shell:
        "bwa index {input.ref};"
        "bwa mem -t {threads} {input.ref} {input.a} {input.b} > {output}"

#Main rule to be called to infer the dependency of rules
rule all:
    input:
        "aligned.bam"
