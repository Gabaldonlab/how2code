import argparse


def define_small_variant_calling_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    small_variant_call_args = parser.add_argument_group(
        "SMALL VARIANT CALLING AND COVERAGE PER GENE CALCULATION"
    )

    small_variant_call_args.add_argument(
        "--run_smallVarsCNV",
        dest="run_smallVarsCNV",
        action="store_true",
        default=False,
        help="Will call small variants and CNV.",
    )

    small_variant_call_args.add_argument(
        "-caller",
        "--caller",
        dest="caller",
        required=False,
        default="all",
        help=(
            "SNP caller option to obtain vcf file. options:"
            " no/all/HaplotypeCaller/bcftools/freebayes. It can be a"
            " comma-sepparated string, like 'HaplotypeCaller,freebayes'"
        ),
    )

    small_variant_call_args.add_argument(
        "-c",
        "--coverage",
        dest="coverage",
        default=20,
        type=int,
        help=(
            "minimum Coverage (int) of a position to be considered for small"
            " variant calling. This parameter should be related to the"
            " coverage of your library. You may be careful with setting it too"
            " low (i.e. <15) as it will yield many false positive calls. It is"
            " reasonable to check how other similar studies set this"
            " parameter."
        ),
    )

    small_variant_call_args.add_argument(
        "--minAF_smallVars",
        dest="minAF_smallVars",
        default="infer",
        help=(
            "The minimum fraction of reads covering a variant to be called."
            " The default is 'infer', which will set a threshold based on the"
            " ploidy. This is only relevant for the final vcfs, where only"
            " PASS vars are considered. It can be a number between 0 and 1."
        ),
    )

    small_variant_call_args.add_argument(
        "--window_freebayes_bp",
        dest="window_freebayes_bp",
        default=10000,
        type=int,
        help=(
            "freebayes is run in parallel by chunks of the genome. This cmd"
            " specifies the window (in bp) in which freebayes regions are"
            " split to. If you increase this number the splitting will be in"
            " larger chunks of the genome."
        ),
    )

    small_variant_call_args.add_argument(
        "--pooled_sequencing",
        dest="pooled_sequencing",
        action="store_true",
        default=False,
        help=(
            "It is a pooled sequencing run, which means that the small variant"
            " calling is not done based on ploidy. If you are also running SV"
            " calling, you will run parameters optimisation on a sample that"
            " has 1-10 pooling."
        ),
    )

    small_variant_call_args.add_argument(
        "--run_ploidy2_ifHaploid",
        dest="run_ploidy2_ifHaploid",
        action="store_true",
        default=False,
        help=(
            "If ploidy==1, run also in diploid configuration. This is useful"
            " because there may be diploid mutations in duplicated regions."
        ),
    )

    small_variant_call_args.add_argument(
        "--consider_repeats_smallVarCall",
        dest="consider_repeats_smallVarCall",
        action="store_true",
        default=False,
        help=(
            "If --run_smallVarsCNV, this option will imply that each small "
            " variant will have an annotation of whether it overlaps a repeat"
            " region."
        ),
    )

    small_variant_call_args.add_argument(
        "--remove_smallVarsCNV_nonEssentialFiles",
        dest="remove_smallVarsCNV_nonEssentialFiles",
        action="store_true",
        default=False,
        help=(
            "Will remove all the varCall files except the integrated final"
            " file and the bam file."
        ),
    )
    return small_variant_call_args
