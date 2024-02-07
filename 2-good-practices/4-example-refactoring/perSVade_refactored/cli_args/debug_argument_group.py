import argparse


def define_debug_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    debug_args = parser.add_argument_group(
        "ONLY TO BE USED FOR DEVELOPMENT. USE AT YOUR OWN RISK!"
    )

    debug_args.add_argument(
        "--target_taxID",
        dest="target_taxID",
        type=int,
        default=None,
        help=(
            "This is the taxID (according to NCBI taxonomy) to which your"
            " reference genome belongs. If provided it is used to download"
            " genomes and reads."
        ),
    )

    debug_args.add_argument(
        "--goldenSet_max_n_samples",
        dest="goldenSet_max_n_samples",
        default=6,
        type=int,
        help="Number of runs to run golden set analysis on.",
    )

    debug_args.add_argument(
        "--goldenSet_table",
        dest="goldenSet_table",
        type=str,
        default=None,
        help=(
            "This is the path to a table that has ONT reads for several"
            " samples, each line one sample. It can be 'auto', which will"
            " download as many datasets as possible not exceeding"
            " goldenSet_max_n_samples"
        ),
    )

    debug_args.add_argument(
        "--n_close_samples",
        dest="n_close_samples",
        default=5,
        type=int,
        help=(
            "Number of close samples to search in case --target_taxID is"
            " provided"
        ),
    )

    debug_args.add_argument(
        "--nruns_per_sample",
        dest="nruns_per_sample",
        default=3,
        type=int,
        help=(
            "Number of runs to download for each sample in the case that"
            " --target_taxID is specified. "
        ),
    )

    debug_args.add_argument(
        "--StopAfter_readObtentionFromSRA",
        dest="StopAfter_readObtentionFromSRA",
        action="store_true",
        default=False,
        help="Stop after obtaining reads from SRA.",
    )

    debug_args.add_argument(
        "--StopAfter_sampleIndexingFromSRA",
        dest="StopAfter_sampleIndexingFromSRA",
        action="store_true",
        default=False,
        help=(
            "It will stop after indexing the samples of SRA. You can use this"
            " if, for example, your local machine has internet connection and"
            " your slurm cluster does not. You can first obtain the SRA"
            " indexes in the local machine. And then run again this pipeline"
            " without this option in the slurm cluster."
        ),
    )

    debug_args.add_argument(
        "--StopAfterPrefecth_of_reads",
        dest="StopAfterPrefecth_of_reads",
        action="store_true",
        default=False,
        help=(
            "Stop after obtaining the prefetched .srr file in case"
            " close_shortReads_table is 'auto'"
        ),
    )

    debug_args.add_argument(
        "--StopAfterPrefecth_of_reads_goldenSet",
        dest="StopAfterPrefecth_of_reads_goldenSet",
        action="store_true",
        default=False,
        help=(
            "Stop after obtaining the prefetched .srr file in case"
            " --goldenSet_table is specified."
        ),
    )

    debug_args.add_argument(
        "--StopAfter_testAccuracy_perSVadeRunning",
        dest="StopAfter_testAccuracy_perSVadeRunning",
        action="store_true",
        default=False,
        help=(
            "When --testAccuracy is specified, the pipeline will stop after"
            " the running of perSVade on all the inputs of"
            " --close_shortReads_table with the different configurations."
        ),
    )

    debug_args.add_argument(
        "--StopAfter_testAccuracy",
        dest="StopAfter_testAccuracy",
        action="store_true",
        default=False,
        help=(
            "When --testAccuracy is specified, the pipeline will stop after"
            " testing the accuracy."
        ),
    )

    debug_args.add_argument(
        "--StopAfter_goldenSetAnalysis",
        dest="StopAfter_goldenSetAnalysis",
        action="store_true",
        default=False,
        help=(
            "When --goldenSet_table is specified, the pipeline will stop after"
            " running the golden set analysis."
        ),
    )

    debug_args.add_argument(
        "--StopAfter_replace_SV_CNVcalling",
        dest="StopAfter_replace_SV_CNVcalling",
        action="store_true",
        help="Stop after the removal of files for repeating the CNV calling.",
    )

    debug_args.add_argument(
        "--testAccuracy",
        dest="testAccuracy",
        action="store_true",
        default=False,
        help=(
            "Reports the accuracy  of your calling on the real data,"
            " simulations and fastSVcalling for all the WGS runs specified in"
            " --close_shortReads_table. "
        ),
    )

    debug_args.add_argument(
        "--testAccuracy_skipHomRegionsSimulation",
        dest="testAccuracy_skipHomRegionsSimulation",
        action="store_true",
        default=False,
        help=(
            "If --testAccuracy is provided, skip the simulation of SVs around"
            " hom regions "
        ),
    )

    debug_args.add_argument(
        "--correct_close_shortReads_table_by_nRunsAndSamples",
        dest="correct_close_shortReads_table_by_nRunsAndSamples",
        action="store_true",
        default=False,
        help=(
            "Corrects --close_shortReads_table keeping only nruns and"
            " nsamples. "
        ),
    )

    debug_args.add_argument(
        "--skip_cleaning_outdir",
        dest="skip_cleaning_outdir",
        action="store_true",
        default=False,
        help=(
            "Will NOT remove all the unnecessary files of the perSVade outdir"
        ),
    )

    debug_args.add_argument(
        "--max_coverage_sra_reads",
        dest="max_coverage_sra_reads",
        default=10000000000000000,
        type=int,
        help=(
            "This is the maximum coverage allowed in the reads downloaded by"
            " SRA. If the datasets have a coverage above this perSVade will"
            " randmomly subset reads to match this."
        ),
    )

    debug_args.add_argument(
        "--replace_addingCNstate_to_smallVars",
        dest="replace_addingCNstate_to_smallVars",
        action="store_true",
        default=False,
        help="Replace the step of adding the Copy Number of each variant.",
    )

    debug_args.add_argument(
        "--generate_alternative_genome",
        dest="generate_alternative_genome",
        default=False,
        action="store_true",
        help="Generate an alternative genome in smallVariantCalling.",
    )

    debug_args.add_argument(
        "--visualization_results",
        dest="visualization_results",
        default=False,
        action="store_true",
        help="Visualize the results",
    )

    debug_args.add_argument(
        "--keep_simulation_files",
        dest="keep_simulation_files",
        action="store_true",
        default=False,
        help="Keeps the simulation files from perSVade.",
    )
    return debug_args
