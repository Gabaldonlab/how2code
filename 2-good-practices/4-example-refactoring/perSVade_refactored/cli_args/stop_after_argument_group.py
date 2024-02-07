import argparse


def define_stop_after_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    stopping_args = parser.add_argument_group("STOP AFTER SOME OPERATIONS")

    stopping_args.add_argument(
        "--StopAfter_bamFileObtention",
        dest="StopAfter_bamFileObtention",
        action="store_true",
        default=False,
        help="Stop after obtaining the BAM file of aligned reads.",
    )

    stopping_args.add_argument(
        "--StopAfter_obtentionOFcloseSVs",
        dest="StopAfter_obtentionOFcloseSVs",
        action="store_true",
        default=False,
        help="Stop after obtaining the real_bedpe_breakpoints ",
    )

    stopping_args.add_argument(
        "--StopAfter_repeatsObtention",
        dest="StopAfter_repeatsObtention",
        action="store_true",
        default=False,
        help="Stop after obtaining  the repeats table",
    )

    stopping_args.add_argument(
        "--StopAfter_smallVarCallSimpleRunning",
        dest="StopAfter_smallVarCallSimpleRunning",
        action="store_true",
        default=False,
        help="Stop after obtaining the filtered vcf outputs of each program.",
    )

    stopping_args.add_argument(
        "--StopAfter_smallVarCall",
        dest="StopAfter_smallVarCall",
        action="store_true",
        default=False,
        help=(
            "Stop after running for small variant calls and calculation of per"
            " gene coverage."
        ),
    )
    return stopping_args
