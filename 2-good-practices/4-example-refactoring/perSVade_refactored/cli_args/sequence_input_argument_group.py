import argparse


def define_sequence_input_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    seq_inputs = parser.add_argument_group("SEQUENCE INPUTS")
    seq_inputs.add_argument(
        "-f1",
        "--fastq1",
        dest="fastq1",
        default=None,
        help=(
            "fastq_1 file. Option required to obtain bam files. It can be"
            " 'skip', which will tell the pipeline to not use any fastq or bam"
            " input."
        ),
    )
    seq_inputs.add_argument(
        "-f2",
        "--fastq2",
        dest="fastq2",
        default=None,
        help=(
            "fastq_2 file. Option required to obtain bam files. It can be"
            " 'skip', which will tell the pipeline to not use any fastq or bam"
            " input."
        ),
    )

    seq_inputs.add_argument(
        "--input_SRRfile",
        dest="input_SRRfile",
        default=None,
        help=(
            "An input srr file that can be provided instead of the fastq"
            " files. If this is provided the pipeline will run fastqdump on"
            " the reads, and also run fastqc and trimmomatic on them. This may"
            " be dangerous, since you may supervise the downloading and"
            " quality control of the reads."
        ),
    )

    seq_inputs.add_argument(
        "-sbam",
        "--sortedbam",
        dest="sortedbam",
        default=None,
        help=(
            "The path to the sorted bam file, which should have a bam.bai file"
            " in the same dir. For example, if your bam file is called"
            " 'aligned_reads.bam', there should be an 'aligned_reads.bam.bai'"
            " as well. This is mutually exclusive with providing reads. By"
            " default, it is assumed that this bam has marked duplicates."
        ),
    )

    seq_inputs.add_argument(
        "--downsampled_coverage",
        dest="downsampled_coverage",
        default=None,
        type=float,
        help=(
            "A float indicating whether to downsample to a specific coverage"
            " for faster running. This can be useful for testing some"
            " argument. For example, '--downsampled_coverage 5.0' would"
            " downsample randomly your input reads or bam to an average"
            " coverage of 5x."
        ),
    )

    seq_inputs.add_argument(
        "--other_perSVade_outdirs_sameReadsANDalignment",
        dest="other_perSVade_outdirs_sameReadsANDalignment",
        default=None,
        help=(
            "A comma-sepparated set of full paths to perSVade outdirs that can"
            " be used to replace the sorted bam and reads dir."
        ),
    )
    return seq_inputs
