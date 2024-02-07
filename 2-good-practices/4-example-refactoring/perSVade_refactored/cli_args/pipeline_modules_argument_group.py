import argparse


def define_pipeline_modules_argument_group(
    parser: argparse.ArgumentParser,
) -> argparse._ArgumentGroup:
    module_inputs = parser.add_argument_group("PIPELINE MODULES")
    module_inputs.add_argument(
        "--type_variant_calling",
        dest="type_variant_calling",
        default=None,
        help=(
            "Specify which modules to execute. By default, perSVade runs only"
            " coverage-based CNV and SV calling (with random-based parameter"
            " optimisation). This command can be any combination of 'SV',"
            " 'coverageCNV' and 'small_vars' in a comma comma-sepparated"
            " manner. For example, if you want to execute SV and small variant"
            " calling you can specify --type_variant_calling SV,small_vars."
            " Note that this command overrides the effect of"
            " --run_smallVarsCNV, --remove_smallVarsCNV_nonEssentialFiles,"
            " --skip_SVcalling, --skip_CNV_calling. If you want to execute"
            " this argument you need to specify some sequence input (either"
            " reads or bam file)."
        ),
    )
    return module_inputs
