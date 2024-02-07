import argparse


def define_skip_step_args(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    skipping_args = parser.add_argument_group("SKIP SOME STEPS")

    skipping_args.add_argument(
        "--skip_repeat_analysis",
        dest="skip_repeat_analysis",
        default=False,
        action="store_true",
        help=(
            "Skip the inference of repeats. If --previous_repeats_table is"
            " provided, this argument will override it."
        ),
    )

    skipping_args.add_argument(
        "--skip_SVcalling",
        dest="skip_SVcalling",
        action="store_true",
        default=False,
        help="Do not run SV calling.",
    )

    skipping_args.add_argument(
        "--skip_SV_CNV_calling",
        dest="skip_SV_CNV_calling",
        action="store_true",
        default=False,
        help=(
            "Do not run the integration of SV and CNV calling into a final"
            " vcf. Note that this integration will only take place if SV"
            " calling is performed."
        ),
    )

    skipping_args.add_argument(
        "--skip_CNV_calling",
        dest="skip_CNV_calling",
        action="store_true",
        default=False,
        help=(
            "Do not run the calling of CNV based on coverage. This is"
            " reccommended if you have samples with smiley face in coverage in"
            " a fragmented genome, which does not allow for a proper"
            " normalisation of coverage."
        ),
    )

    skipping_args.add_argument(
        "--skip_cnv_per_gene_analysis",
        dest="skip_cnv_per_gene_analysis",
        default=False,
        action="store_true",
        help=(
            "Don't perform the cnv analysis where we calculate coverage per"
            " gene and per equal windows of the genome. This refers to the"
            " per-gene CNV analysis, not the per-window."
        ),
    )

    skipping_args.add_argument(
        "--skip_marking_duplicates",
        dest="skip_marking_duplicates",
        default=False,
        action="store_true",
        help="Don't mark the duplicate reads in the .bam file.",
    )
    return skipping_args
