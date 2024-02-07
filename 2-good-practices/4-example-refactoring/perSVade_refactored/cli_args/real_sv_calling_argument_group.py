import argparse


def define_real_sv_calling_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    real_sv_args = parser.add_argument_group("SV CALLING. FINDING REAL SVs")
    real_sv_args.add_argument(
        "--close_shortReads_table",
        dest="close_shortReads_table",
        type=str,
        default=None,
        help=(
            "This is the path to a table that has 4 fields:"
            " sampleID,runID,short_reads1,short_reads2. These should be WGS"
            " runs of samples that are close to the reference genome and some"
            " expected SV. Whenever this argument is provided, the pipeline"
            " will find SVs in these samples and generate a folder"
            " <outdir>/findingRealSVs<>/SVs_compatible_to_insert that will"
            " contain one file for each SV, so that they are compatible and"
            " ready to insert in a simulated genome. This table will be used"
            " if --testAccuracy is specified, which will require at least 3"
            " runs for each sample. It can be 'auto', in which case it will be"
            " inferred from the taxID provided by --target_taxID."
        ),
    )

    real_sv_args.add_argument(
        "--real_bedpe_breakpoints",
        dest="real_bedpe_breakpoints",
        type=str,
        default=None,
        help=(
            "A file with the list of 'real' breakpoints around which to insert"
            " the SVs in simulations. It may be created with"
            " --close_shortReads_table. If both --real_bedpe_breakpoints and"
            " --close_shortReads_table are provided, --real_bedpe_breakpoints"
            " will be used, and --close_shortReads_table will have no effect."
            " If none of them are provided, this pipeline will base the"
            " parameter optimization on randomly inserted SVs (the default"
            " behavior). The coordinates have to be 1-based, as they are ready"
            " to insert into RSVsim."
        ),
    )

    real_sv_args.add_argument(
        "--job_array_mode",
        dest="job_array_mode",
        type=str,
        default="local",
        help=(
            "It specifies in how to run the job arrays for,  --testAccuracy,"
            " the downloading of reads if  --close_shortReads_table is auto,"
            " and the SV calling for the table in --close_shortReads_table. It"
            " can be 'local' (runs one job after the other or 'job_array'. If"
            " 'job_array' is specified, this pipeline will generate a file"
            " with all the jobs to run, and stop. You will have to run these"
            " jobs before stepping into downstream analyses."
        ),
    )
    return real_sv_args
