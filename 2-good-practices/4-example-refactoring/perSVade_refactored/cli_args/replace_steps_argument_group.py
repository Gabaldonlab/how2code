import argparse


def define_replace_steps_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    replacing_args = parser.add_argument_group("REPLACE SOME STEPS")

    replacing_args.add_argument(
        "--replace",
        dest="replace",
        action="store_true",
        help="Replace existing files",
    )

    replacing_args.add_argument(
        "--replace_SV_CNVcalling",
        dest="replace_SV_CNVcalling",
        action="store_true",
        help="Replace everything related to the SV and CNV calling.",
    )

    replacing_args.add_argument(
        "--replace_FromGridssRun_final_perSVade_run",
        dest="replace_FromGridssRun_final_perSVade_run",
        action="store_true",
        help=(
            "Replace from the clove running in the final gridss+clove running"
        ),
    )

    replacing_args.add_argument(
        "--replace_var_integration",
        dest="replace_var_integration",
        action="store_true",
        help=(
            "Replace all the variant integration steps for"
            " smallVariantCalling."
        ),
    )

    replacing_args.add_argument(
        "--replace_var_annotation",
        dest="replace_var_annotation",
        action="store_true",
        help=(
            "Replace all the variant annotation steps for smallVariantCalling,"
            " SV and CNV calling."
        ),
    )
    return replacing_args
