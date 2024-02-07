import argparse


def define_optional_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    general_optional_args = parser.add_argument_group(
        "GENERAL OPTIONAL ARGUMENTS"
    )

    general_optional_args.add_argument(
        "-p",
        "--ploidy",
        dest="ploidy",
        default=1,
        type=int,
        help="Ploidy, can be 1 or 2",
    )

    general_optional_args.add_argument(
        "-gff",
        "--gff-file",
        dest="gff",
        default=None,
        help=(
            "path to the GFF3 annotation of the reference genome. Make sure"
            " that the IDs are completely unique for each 'gene' tag. This is"
            " necessary for both the CNV analysis (it will look at genes"
            " there) and the annotation of the variants."
        ),
    )

    general_optional_args.add_argument(
        "-mcode",
        "--mitochondrial_code",
        dest="mitochondrial_code",
        default=3,
        type=int,
        help=(
            "The code of the NCBI mitochondrial genetic code. For yeasts it is"
            " 3. You can find the numbers for your species here"
            " https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi. The"
            " information of this website may be wrong, so you may want to"
            " double check with the literature."
        ),
    )

    general_optional_args.add_argument(
        "-gcode",
        "--gDNA_code",
        dest="gDNA_code",
        default=1,
        type=int,
        help=(
            "The code of the NCBI gDNA genetic code. You can find the numbers"
            " for your species here"
            " https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi . For"
            " C. albicans it is 12. The information of this website may be"
            " wrong, so you may want to double check with the literature."
        ),
    )

    general_optional_args.add_argument(
        "--QC_and_trimming_reads",
        dest="QC_and_trimming_reads",
        action="store_true",
        default=False,
        help=(
            "Will run fastq and trimmomatic of reads, and use the trimmed"
            " reads for downstream analysis. This option will generate files"
            " under the same dir as f1 and f2, so be aware of it. This is a"
            " rather dangerous option, sinc you may want to do the quality"
            " control of the reads before running perSVade."
        ),
    )

    general_optional_args.add_argument(
        "--min_chromosome_len",
        dest="min_chromosome_len",
        default=100000,
        type=int,
        help=(
            "The minimum length to consider chromosomes from the provided"
            " fasta for calculating the window length. Any chromosomes that"
            " shorter than the window length will not be considered in the"
            " random SV simulations."
        ),
    )

    general_optional_args.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help=(
            "Whether to print a verbose output. This is important if there are"
            " any errors in the run."
        ),
    )

    general_optional_args.add_argument(
        "--previous_repeats_table",
        dest="previous_repeats_table",
        default=None,
        help=(
            "This may be the path to a file that contains the processed output"
            " of RepeatMasker (such as the one output by the function"
            " get_repeat_maskerDF). This should be a table with the following"
            " header: 'SW_score, perc_div, perc_del, perc_ins, chromosome,"
            " begin_repeat, end_repeat, left_repeat, strand, repeat, type,"
            " position_inRepeat_begin, position_inRepeat_end,"
            " left_positionINrepeat, IDrepeat'. It is created by parsing the"
            " tabular output of RepeatMasker and putting into a real .tab"
            " format."
        ),
    )
    return general_optional_args
