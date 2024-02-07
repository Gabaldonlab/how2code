import argparse


def define_mandatory_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    mandatory_args = parser.add_argument_group("MANDATORY ARGUMENTS")
    mandatory_args.add_argument(
        "-r",
        "--ref",
        dest="ref",
        required=True,
        help="Reference genome. Has to end with .fasta.",
    )
    mandatory_args.add_argument(
        "-o",
        "--outdir",
        dest="outdir",
        action="store",
        required=True,
        help="Directory where the data will be stored",
    )
    mandatory_args.add_argument(
        "-mchr",
        "--mitochondrial_chromosome",
        dest="mitochondrial_chromosome",
        required=True,
        type=str,
        help=(
            "The name of the mitochondrial chromosome. This is important if"
            " you have mitochondrial proteins for which to annotate the impact"
            " of nonsynonymous variants, as the mitochondrial genetic code is"
            " different. This should be the same as in the gff. If there is no"
            " mitochondria just put 'no_mitochondria'. If there is more than"
            " one mitochindrial scaffold, provide them as comma-sepparated"
            " IDs."
        ),
    )
    return mandatory_args
