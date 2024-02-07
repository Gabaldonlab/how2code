import argparse


def define_resources_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    resources_args = parser.add_argument_group("RESOURCES")

    resources_args.add_argument(
        "-thr",
        "--threads",
        dest="threads",
        default=16,
        type=int,
        help="Number of threads, Default: 16",
    )

    resources_args.add_argument(
        "--fraction_available_mem",
        dest="fraction_available_mem",
        default=None,
        type=float,
        help=(
            "The fraction of RAM that is being allocated to this perSVade run."
            " In several steps, this pipeline needs to calculate the available"
            " memory (using psutil.virtual_memory()). This returns all the"
            " available memory in the computer. If you are running on a"
            " fraction of the computers' resources, this calculation is"
            " overestimating the available RAM. In such case you can provide"
            " the fraction available through this argument. By default, it"
            " will calculate the available ram by filling the memory, which"
            " may give errors. It is highly reccommended that you provide this"
            " option. If you want to use all the allocated memory you should"
            " specify --fraction_available_mem 1.0"
        ),
    )

    resources_args.add_argument(
        "--fractionRAM_to_dedicate",
        dest="fractionRAM_to_dedicate",
        type=float,
        default=0.5,
        help=(
            "This is the fraction of the available memory that will be used by"
            " several java programs that require a heap size. By default we"
            " set this to 0.5 to not overload the system"
        ),
    )

    resources_args.add_argument(
        "--tmpdir",
        dest="tmpdir",
        default=None,
        help=(
            "A full path to a directory where to write intermediate files."
            " This is useful if you are running on a cluster that has some"
            " directories that have higher writing speed than others."
        ),
    )

    resources_args.add_argument(
        "--min_gb_RAM_required",
        dest="min_gb_RAM_required",
        default=2,
        type=int,
        help=(
            "The minimum number of RAM required to run perSVade. This can be"
            " related to --fraction_available_mem"
        ),
    )
    return resources_args
