import argparse


def define_sv_calling_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    sv_calling_args = parser.add_argument_group("SV CALLING")

    sv_calling_args.add_argument(
        "--parameters_json_file",
        dest="parameters_json_file",
        type=str,
        default=None,
        help=(
            "A file with the json parameters to use. This only has effect if"
            " --fast_SVcalling is specified"
        ),
    )

    sv_calling_args.add_argument(
        "--fast_SVcalling",
        dest="fast_SVcalling",
        action="store_true",
        default=False,
        help=(
            "Run SV calling with a default set of parameters. There will not"
            " be any optimisation nor reporting of accuracy. This is expected"
            " to work almost as fast as gridss and clove together. If"
            " --parameters_json_file, the parameters are substituted by the"
            " json parameters."
        ),
    )

    sv_calling_args.add_argument(
        "--simulation_chromosomes",
        dest="simulation_chromosomes",
        type=str,
        default=None,
        help=(
            "A comma-sepparated set of chromosomes (i.e.: chr1,chr2,chr3) in"
            " which to perform simulations. By default it takes all the"
            " chromosomes."
        ),
    )

    sv_calling_args.add_argument(
        "--nvars",
        dest="nvars",
        default=50,
        type=int,
        help="Number of variants to simulate for each SVtype.",
    )

    sv_calling_args.add_argument(
        "--nsimulations",
        dest="nsimulations",
        default=2,
        type=int,
        help="The number of 'replicate' simulations that will be produced.",
    )

    sv_calling_args.add_argument(
        "--simulation_ploidies",
        dest="simulation_ploidies",
        type=str,
        default="auto",
        help=(
            "A comma-sepparated string of the ploidies to simulate for"
            ' parameter optimisation. It can have any of "haploid",'
            ' "diploid_homo", "diploid_hetero", "ref:2_var:1", "ref:3_var:1",'
            ' "ref:4_var:1", "ref:5_var:1", "ref:9_var:1", "ref:19_var:1",'
            ' "ref:99_var:1" . By default it will be inferred from the ploidy.'
            " For example, if you are running on ploidy=2, it will optimise"
            " for diploid_hetero."
        ),
    )

    sv_calling_args.add_argument(
        "--range_filtering_benchmark",
        dest="range_filtering_benchmark",
        type=str,
        default="theoretically_meaningful",
        help=(
            "The range of parameters that should be tested in the SV"
            " optimisation pipeline. It can be any of large, medium, small,"
            " theoretically_meaningful,"
            " theoretically_meaningful_NoFilterRepeats or single. "
        ),
    )

    sv_calling_args.add_argument(
        "--simulate_SVs_around_repeats",
        dest="simulate_SVs_around_repeats",
        action="store_true",
        default=False,
        help=(
            "Simulate SVs around repeats. This requires that there are some"
            " repeats inferred. This option will generate a simulated set of"
            " breakpoints around repeats, if possible of the same family, and"
            " with random orientations."
        ),
    )

    sv_calling_args.add_argument(
        "--simulate_SVs_around_HomologousRegions",
        dest="simulate_SVs_around_HomologousRegions",
        action="store_true",
        default=False,
        help="Simulate SVs around regions that have high similarity.",
    )

    sv_calling_args.add_argument(
        "--simulate_SVs_around_HomologousRegions_queryWindowSize",
        dest="simulate_SVs_around_HomologousRegions_queryWindowSize",
        default=500,
        type=int,
        help=(
            "The window size used for finding regions with high similarity."
            " This only works if --simulate_SVs_around_HomologousRegions is"
            " specified."
        ),
    )

    sv_calling_args.add_argument(
        "--simulate_SVs_around_HomologousRegions_maxEvalue",
        dest="simulate_SVs_around_HomologousRegions_maxEvalue",
        default=1e-5,
        type=float,
        help=(
            "The maximum evalue by which two regions will be said to have high"
            " similarity. This only works if"
            " --simulate_SVs_around_HomologousRegions is specified."
        ),
    )

    sv_calling_args.add_argument(
        "--simulate_SVs_around_HomologousRegions_minPctOverlap",
        dest="simulate_SVs_around_HomologousRegions_minPctOverlap",
        default=50,
        type=int,
        help=(
            "The minimum percentage of overlap between two homologous"
            " regionsso that there can be a brèkpoint drawn in between. This"
            " only works if--simulate_SVs_around_HomologousRegions is"
            " specified."
        ),
    )

    sv_calling_args.add_argument(
        "--simulate_SVs_around_HomologousRegions_previousBlastnFile",
        dest="simulate_SVs_around_HomologousRegions_previousBlastnFile",
        default=None,
        help=(
            "A file that contains the output of blastn of regions of the"
            " genomeagainst itself. It will be put under refetence genome dir"
        ),
    )
    return sv_calling_args
