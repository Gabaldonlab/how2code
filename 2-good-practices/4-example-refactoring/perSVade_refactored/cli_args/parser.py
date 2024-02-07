#!/usr/bin/env python
"""
This is the perSVade pipeline CLI argument parser module.
"""
import argparse
from argparse import RawTextHelpFormatter

from cli_args.cnv_argument_group import define_cnv_argument_group
from cli_args.debug_argument_group import define_debug_argument_group
from cli_args.mandatory_argument_group import define_mandatory_argument_group
from cli_args.optional_argument_group import define_optional_argument_group
from cli_args.real_sv_calling_argument_group import (
    define_real_sv_calling_argument_group,
)
from cli_args.replace_steps_argument_group import (
    define_replace_steps_argument_group,
)
from cli_args.resources_argument_group import define_resources_argument_group
from cli_args.sequence_input_argument_group import (
    define_sequence_input_argument_group,
)
from cli_args.skip_step_args import define_skip_step_args
from cli_args.small_variant_calling_argument_group import (
    define_small_variant_calling_argument_group,
)
from cli_args.stop_after_argument_group import define_stop_after_argument_group
from cli_args.sv_calling_argument_group import define_sv_calling_argument_group


def collect_arguments_from_cli() -> argparse.Namespace:
    description: str = (
        "Runs perSVade pipeline on an input set of paired end short ends. "
        "See https://github.com/Gabaldonlab/perSVade for more information."
    )
    parser = argparse.ArgumentParser(
        description=description, formatter_class=RawTextHelpFormatter
    )
    _ = define_mandatory_argument_group(parser)
    _ = define_sequence_input_argument_group(parser)
    _ = define_resources_argument_group(parser)
    _ = define_optional_argument_group(parser)
    _ = define_sv_calling_argument_group(parser)
    _ = define_real_sv_calling_argument_group(parser)
    _ = define_cnv_argument_group(parser)
    _ = define_small_variant_calling_argument_group(parser)
    _ = define_skip_step_args(parser)
    _ = define_stop_after_argument_group(parser)
    _ = define_replace_steps_argument_group(parser)
    _ = define_debug_argument_group(parser)
    return parser.parse_args()
