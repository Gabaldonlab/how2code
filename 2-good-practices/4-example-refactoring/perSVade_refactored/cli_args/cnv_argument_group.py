import argparse


def define_cnv_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    cnv_args = parser.add_argument_group("READ DEPTH-BASED CNV CALLING")

    cnv_args.add_argument(
        "--min_CNVsize_coverageBased",
        dest="min_CNVsize_coverageBased",
        default=300,
        type=int,
        help="The minimum size of a CNV inferred from coverage.",
    )

    cnv_args.add_argument(
        "--window_size_CNVcalling",
        dest="window_size_CNVcalling",
        default=100,
        type=int,
        help=(
            "The window size in which the genome will be fragmented for CNV"
            " calling."
        ),
    )

    cnv_args.add_argument(
        "--cnv_calling_algs",
        dest="cnv_calling_algs",
        default="HMMcopy,AneuFinder",
        type=str,
        help=(
            "A comma-sepparated string thatindicates which programs should be"
            " used for the CNV calling. It can be any of"
            " HMMcopy,CONY,AneuFinder. We note that CONY does not work well"
            " for small chromosomes or large binned windows."
        ),
    )

    cnv_args.add_argument(
        "--bg_sorted_bam_CNV",
        dest="bg_sorted_bam_CNV",
        default=None,
        help=(
            "This is a sorted bam (with duplicated marked) that is taken as a"
            " 'reference' background in the CNV calling. By default, perSVade"
            " corrects the coverage by GC content, mappability and the"
            " distance to the telomere. If --bg_sorted_bam_CNV, the coverage"
            " will be normalised by the coverage of this sorted bam."
        ),
    )
    return cnv_args
