#!/usr/bin/env python
"""
This is the perSVade pipeline main script, which should be run on the perSVade conda environment
"""
import argparse
import os
import sys
import time
from argparse import RawTextHelpFormatter
from typing import Any, Iterable

import pandas as pd
import sv_functions
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from cli_args.parser import collect_arguments_from_cli

CWD: str = os.path.dirname(__file__)
ENVIRONMENT_DIRECTORY: str = "/".join(sys.executable.split("/")[0:-2])

# packages installed into the conda environment
SAMTOOLS: str = os.path.join(ENVIRONMENT_DIRECTORY, "bin", "samtools")
JAVA: str = os.path.join(ENVIRONMENT_DIRECTORY, "binjava")

# scripts that are installed under this software
VARCALL_CNV_PIPELINE: str = os.path.join(CWD, "varcall_cnv_pipeline.py")
PERSVADE_GENOME_BROWSER: str = os.path.join(CWD, "perSVade_genome_browser.py")

opt: argparse.Namespace = collect_arguments_from_cli()

########################################
##### GENERAL PROCESSING OF INPUTS #####
########################################


def check_modules_input(modules: Iterable[str]) -> None:
    strange_modules: set[str] = modules_set.difference(
        {"SV", "coverageCNV", "small_vars"}
    )
    if len(strange_modules) > 0:
        raise ValueError(
            "There are some strange modules: %s. Provide a valid"
            " --type_variant_calling." % strange_modules
        )

def check_fastq_inputs(fastq1: str, fastq2: str) -> None:
    # check that there is some sequence input
    if any([x == "skip" for x in {fastq1, fastq2}]):
        raise ValueError(
            "If you want to execute some modules with --type_variant_calling"
            " you have to provide reads (-f1 and -f2) or a bam file (-sbam)."
            " If you specified '-f1 skip' and/or '-f2 skip' you are telling"
            " perSVade to not use any sequence input, which is incomaptible"
            " with --type_variant_calling. "
        )

def adjust_argument_values(args: argparse.Namespace) -> None:
    # override arguments depending on the combinations
    opt.skip_SVcalling = True
    if "SV" in modules_set:
        opt.skip_SVcalling = False

    opt.skip_CNV_calling = True
    if "coverageCNV" in modules_set:
        opt.skip_CNV_calling = False

    opt.run_smallVarsCNV = False
    if "small_vars" in modules_set:
        opt.run_smallVarsCNV = True

    if opt.run_smallVarsCNV:
        opt.remove_smallVarsCNV_nonEssentialFiles = True

def write_reference_genome_file(new_reference_genome_file: str) -> None:
    """
    Rewrite the reference genome so that all the chars ar upper.
    """
    all_chroms_seq_records: list[SeqRecord] = [
        SeqRecord(Seq(str(seq.seq).upper()), id=seq.id, description="", name="")
        for seq in SeqIO.parse(opt.ref, "fasta")
    ]
    SeqIO.write(all_chroms_seq_records, new_reference_genome_file, "fasta")

def manage_output_paths_by_arguments(opt: argparse.Namespace, final_file: str, reference_genome_dir: str) -> None:
    if opt.replace:
        sv_functions.delete_folder(opt.outdir)
    sv_functions.make_folder(opt.outdir)

    if (
        opt.replace
        or opt.replace_SV_CNVcalling
        or opt.replace_FromGridssRun_final_perSVade_run
        or opt.replace_var_integration
    ):
        sv_functions.remove_file(final_file)

    if not sv_functions.file_is_empty(final_file):
        print(
            "WARNING: %s exists, suggesting that perSVade was already  run in this"
            " folder. Remove this file if you want this command to work."
            " Exiting..." % final_file
        )
        sys.exit(1)

    sv_functions.make_folder(reference_genome_dir)

def check_mito_chromosomes(opt: argparse.Namespace) -> None:
    """
    Check that the mitoChromosomes are in the ref
    """

    all_chroms: set[Any] = {s.id for s in SeqIO.parse(opt.ref, "fasta")}
    if (
        any([x not in all_chroms for x in opt.mitochondrial_chromosome.split(",")])
        and opt.mitochondrial_chromosome != "no_mitochondria"
    ):
        raise ValueError(
            "The provided mitochondrial_chromosomes are not in the reference"
            " genome."
        )

    # check that the simulation_chromosomes are in all_chroms
    if opt.simulation_chromosomes:
        strange_chroms = set(opt.simulation_chromosomes.split(",")).difference(
            all_chroms
        )
        if len(strange_chroms) > 0:
            raise ValueError(
                "The --simulation_chromosomes argument was not properly set. There"
                " are some chromosome IDs (%s) not found in the provided reference"
                " genome" % strange_chroms
            )

def manage_gff_files_by_arguments(opt: argparse.Namespace, target_gff: str) -> None:
    # If you want to repeat the annotation,
    # remove all the files in the reference genome dir that are related
    # to the annotation.
    if opt.replace_var_annotation:
        for file in os.listdir(reference_genome_dir):
            file_path = os.path.join(reference_genome_dir, file)
            if file_path.startswith(target_gff):
                sv_functions.remove_file(file_path)

    if not opt.gff:
        print(
            "WARNING: gff was not provided. This will be a problem if you want to"
            " annotate small variant calls"
        )
        return

    if sv_functions.file_is_empty(target_gff):
        sv_functions.soft_link_files(opt.gff, target_gff)

    opt.gff = target_gff

def swap_previous_repeats_table_soft_link(previous_repeats_table: str, current_repeats_table_file: str ) -> None:
    if sv_functions.file_is_empty(previous_repeats_table):
        raise ValueError("The provided repeats table does not exist")

    sv_functions.remove_file(current_repeats_table_file)
    sv_functions.soft_link_files(
        previous_repeats_table, current_repeats_table_file
    )

def get_simulation_ploidies(opt: argparse.Namespace) -> list[str]:
    if opt.simulation_ploidies != "auto":
        return opt.simulation_ploidies.split(",")

    # for pooled seq it takes simulated on 1 in 10
    if opt.pooled_sequencing:
        return ["diploid_homo", "ref:9_var:1"]
    elif opt.ploidy == 1:
        return ["haploid"]

    return ["ref:%i_var:1" % (opt.ploidy - 1)]


def get_cnv_calling_alignments(opt: argparse.Namespace) -> set[str]:
    cnv_calling_algs = set(opt.cnv_calling_algs.split(","))
    all_expected_cnv_calling_algs = {"HMMcopy", "AneuFinder", "CONY"}

    if len(cnv_calling_algs.difference(all_expected_cnv_calling_algs)) > 0:
        raise ValueError(
            "the cnv calling algs should be in %s" % all_expected_cnv_calling_algs
        )

    if opt.pooled_sequencing is True:
        print(
            "WARNING: Running on pooled sequencing.  These are the simulated"
            " ploidies for the SV calling parameter optimisation:",
            simulation_ploidies,
        )
    return cnv_calling_algs


def generate_and_write_real_bedpe_breakpoints_around_repeats(opt: argparse.Namespace, repeats_table_file: str) -> None:
    # debug
    if opt.real_bedpe_breakpoints:
        raise ValueError(
            "You can not specify --simulate_SVs_around_repeats and"
            " --real_bedpe_breakpoints. You may definir either of both."
        )
    if opt.skip_repeat_analysis:
        raise ValueError(
            "You should not skip the repeats analysis (with"
            " --skip_repeat_analysis) if you want to simulate SVs around"
            " repeats."
        )
    if opt.simulate_SVs_around_HomologousRegions:
        raise ValueError(
            "You can not specify --simulate_SVs_around_repeats and"
            " --simulate_SVs_around_HomologousRegions."
        )

    # override the real_bedpe_breakpoints with the bedpe comming from repeats
    opt.real_bedpe_breakpoints = (
        sv_functions.get_bedpe_breakpoints_around_repeats(
            repeats_table_file,
            replace=opt.replace,
            max_breakpoints=(opt.nvars * 5 * 10000),
            max_breakpoints_per_repeat=1,
            threads=opt.threads,
            max_repeats=(opt.nvars * 5 * 2500),
        )
    )

def generate_real_bedpe_breakpoints_around_homologous_regions(opt: argparse.Namespace) -> None:
    # debug
    if opt.real_bedpe_breakpoints:
        raise ValueError(
            "You can not specify --simulate_SVs_around_repeats and"
            " --real_bedpe_breakpoints. You may definie either of both."
        )
    if opt.simulate_SVs_around_repeats:
        raise ValueError(
            "You can not specify --simulate_SVs_around_repeats and"
            " --simulate_SVs_around_HomologousRegions."
        )

    # get a file that contains the blastn of some regions of the genome
    if not opt.simulate_SVs_around_HomologousRegions_previousBlastnFile:
        blastn_file = sv_functions.get_blastn_regions_genome_against_itself(
            opt.ref,
            opt.simulate_SVs_around_HomologousRegions_maxEvalue,
            opt.simulate_SVs_around_HomologousRegions_queryWindowSize,
            opt.replace,
            opt.threads,
        )
    else:
        blastn_file = (
            opt.simulate_SVs_around_HomologousRegions_previousBlastnFile
        )

    # define the bedpe breakpoints around the homologous regions
    bedpe_breakpoints = (
        "%s/breakpoints_aroundHomRegions_wsize=%ibp_maxEval=%s_minQcovS=%i.bedpe"
        % (
            opt.outdir,
            opt.simulate_SVs_around_HomologousRegions_queryWindowSize,
            opt.simulate_SVs_around_HomologousRegions_maxEvalue,
            opt.simulate_SVs_around_HomologousRegions_minPctOverlap,
        )
    )

    opt.real_bedpe_breakpoints = sv_functions.get_bedpe_breakpoints_around_homologousRegions(
        blastn_file,
        bedpe_breakpoints,
        replace=opt.replace,
        threads=opt.threads,
        max_eval=opt.simulate_SVs_around_HomologousRegions_maxEvalue,
        query_window_size=opt.simulate_SVs_around_HomologousRegions_queryWindowSize,
        min_qcovs=opt.simulate_SVs_around_HomologousRegions_minPctOverlap,
        max_n_hits=(opt.nvars * 5 * 2500),
    )


if opt.type_variant_calling:
    modules_set: set[str] = set(opt.type_variant_calling.split(","))
    check_modules_input(modules_set)
    check_fastq_inputs(opt.fastq1, opt.fastq2)
    adjust_argument_values(opt)

# start time of processing
start_time_general_processing: float = time.time()
start_time_all: float = time.time()

final_file: str = os.path.join(opt.outdir, "perSVade_finished_file.txt")
reference_genome_dir: str = os.path.join(opt.outdir, "reference_genome_dir")
target_gff: str = os.path.join(reference_genome_dir, "reference_genome_features.gff")
opt.ref = os.path.join(reference_genome_dir, "reference_genome.fasta")

manage_output_paths_by_arguments(opt, final_file, reference_genome_dir)
write_reference_genome_file(opt.ref)
check_mito_chromosomes(opt)
sv_functions.index_genome(opt.ref, replace=opt.replace)
manage_gff_files_by_arguments(opt, target_gff)

name_sample: str = sv_functions.get_sampleName_from_perSVade_outdir(opt.outdir)
print(
    f"Running perSVade into {opt.outdir}. The name_sample is {name_sample}"
)
# get the genome len
genome_length = sum(sv_functions.get_chr_to_len(opt.ref).values())
print("The genome has %.2f Mb" % (genome_length / 1000000))


# Define the repeats table.
# This will work for any downstream analysis of this.
repeats_table_file: str = f"{opt.ref}.repeats.tab"

if opt.previous_repeats_table:
    print(f"Using privided repeats {opt.previous_repeats_table}")
    swap_previous_repeats_table_soft_link(opt.previous_repeats_table, repeats_table_file)

if opt.other_perSVade_outdirs_sameReadsANDalignment:
    sv_functions.link_files_from_other_perSVade_outdirs_reads_and_alignment(
        opt.outdir, opt.other_perSVade_outdirs_sameReadsANDalignment
    )

# define a log file for perSVade
sv_functions.log_file_all_cmds = "%s/all_cmds_ran.txt" % opt.outdir
if sv_functions.file_is_empty(sv_functions.log_file_all_cmds):
    open(sv_functions.log_file_all_cmds, "w").write(
        "# These are all the cmds:\n"
    )

simulation_ploidies: list[str] = get_simulation_ploidies(opt)
cnv_calling_algs: set[str] = get_cnv_calling_alignments(opt)

# the window length for all operations
sv_functions.window_l = sv_functions.get_perSVade_window_l(
    opt.ref, opt.mitochondrial_chromosome, opt.min_chromosome_len
)

# TBC: HERE!

# Define the verbosity.
# If opt.verbose is False, none of the 'print' statements of sv_functions
# will have an effect.
sv_functions.printing_verbose_mode = opt.verbose

# defin the fraction of available mem
sv_functions.fraction_available_mem = opt.fraction_available_mem
if opt.fraction_available_mem is None:
    print(
        "WARNING: You did not specify how much RAM should be used through"
        " --fraction_available_mem. perSVade will calculate this by filling"
        " the memory, which may be dangerous. If you want to use all the"
        " allocated memory you should specify --fraction_available_mem 1.0"
    )

# define the fraction of RAM to dedicate
if opt.fractionRAM_to_dedicate > 0.95:
    raise ValueError(
        "You are using >95 pct of the systems RAM, which is dangerous"
    )
sv_functions.fractionRAM_to_dedicate = opt.fractionRAM_to_dedicate

# define the min_CNVsize_coverageBased
sv_functions.min_CNVsize_coverageBased = opt.min_CNVsize_coverageBased

# redefine the real threads
real_available_threads = sv_functions.get_available_threads(opt.outdir)
if opt.threads > real_available_threads:
    print(
        "WARNING: There are %i available threads, and you required %i."
        % (real_available_threads, opt.threads)
    )

available_Gb_RAM = sv_functions.get_availableGbRAM(opt.outdir)
if available_Gb_RAM < opt.min_gb_RAM_required:
    raise ValueError(
        "You should be running with at least %i Gb of RAM. There are just %.3f"
        " in this system" % (opt.min_gb_RAM_required, available_Gb_RAM)
    )
print(
    "Running with %.3f Gb of RAM and %i cores"
    % (available_Gb_RAM, opt.threads)
)

# change the default parameters if specified
if opt.parameters_json_file:
    (
        gridss_blacklisted_regions,
        gridss_maxcoverage,
        gridss_filters_dict,
        max_rel_coverage_to_consider_del,
        min_rel_coverage_to_consider_dup,
    ) = sv_functions.get_parameters_from_json(opt.parameters_json_file)

    sv_functions.default_filtersDict_gridss = gridss_filters_dict
    sv_functions.default_gridss_blacklisted_regions = (
        gridss_blacklisted_regions
    )
    sv_functions.default_gridss_maxcoverage = gridss_maxcoverage
    sv_functions.default_max_rel_coverage_to_consider_del = (
        max_rel_coverage_to_consider_del
    )
    sv_functions.default_min_rel_coverage_to_consider_dup = (
        min_rel_coverage_to_consider_dup
    )

# test whether the gff is correct
if opt.gff:
    (
        correct_gff,
        gff_with_biotype,
    ) = sv_functions.get_correct_gff_and_gff_with_biotype(
        opt.gff, replace=opt.replace
    )
    sv_functions.check_that_gff_is_correct(
        opt.gff,
        opt.ref,
        opt.mitochondrial_chromosome,
        opt.mitochondrial_code,
        opt.gDNA_code,
        opt.threads,
        opt.replace,
    )

# check that the tmpdir exists
if opt.tmpdir:
    if not os.path.isdir(opt.tmpdir):
        raise ValueError(
            "The folder that you specified with --tmpdir does not exist"
        )

# get the repeats table
if not opt.skip_repeat_analysis:
    print("getting repeats")
    repeats_df, repeats_table_file = sv_functions.get_repeat_maskerDF(
        opt.ref, threads=opt.threads, replace=opt.replace
    )
else:
    print("skipping the repeats analysis")
    sv_functions.write_repeats_table_file(repeats_table_file)


if opt.StopAfter_repeatsObtention is True:
    print(
        "Stopping after the obtention of repeats. They can be found in %s"
        % repeats_table_file
    )
    sys.exit(0)


if opt.simulate_SVs_around_repeats:
    print("simulating around repeats")
    generate_and_write_real_bedpe_breakpoints_around_repeats(opt, repeats_table_file)

if opt.simulate_SVs_around_HomologousRegions:
    print("simulating around Homologous regions")
    generate_real_bedpe_breakpoints_around_homologous_regions(opt)

# end time of processing
end_time_GeneralProcessing = time.time()


#####################################
############# BAM FILE ##############
#####################################

start_time_alignment = time.time()

if not any([x == "skip" for x in {opt.fastq1, opt.fastq2}]):
    ##### DEFINE THE SORTED BAM #####

    # define the dest bam files
    bamfile = "%s/aligned_reads.bam" % opt.outdir
    sorted_bam = "%s.sorted" % bamfile
    index_bam = "%s.bai" % sorted_bam

    # if you provided a sorted bam it should be placed into sorted_bam
    if opt.sortedbam is not None:
        # debug the fact that you prvided reads and bam. You should just provide one
        if any([not x is None for x in {opt.fastq1, opt.fastq2}]):
            raise ValueError(
                "You have provided reads and a bam, you should only"
                " provide one"
            )

        # downsample the bam for testing if speciefied
        if opt.downsampled_coverage is not None:
            print(
                "WARNING: You are running perSVade on a downsampled bam (to"
                " %.3fx)."
                % opt.downsampled_coverage
            )
            opt.sortedbam = (
                sv_functions.get_downsampled_bam_to_specified_coverage(
                    opt.outdir,
                    opt.sortedbam,
                    opt.downsampled_coverage,
                    opt.ref,
                    replace=opt.replace,
                    threads=opt.threads,
                )
            )

        # get the linked bam files
        sv_functions.soft_link_files(
            sv_functions.get_fullpath(opt.sortedbam), sorted_bam
        )
        sv_functions.soft_link_files(
            sv_functions.get_fullpath(opt.sortedbam) + ".bai",
            sorted_bam + ".bai",
        )

    ###################################

    # normal alignment of provided reads
    if (
        all([not x is None for x in {opt.fastq1, opt.fastq2}])
        or opt.input_SRRfile is not None
    ):
        # if you have reads, you may want to downsample them
        if (
            all([not x is None for x in {opt.fastq1, opt.fastq2}])
            and opt.downsampled_coverage is not None
        ):
            # downsample the reads
            print(
                "WARNING: You are running perSVade on downsampled reads (to"
                " %.3fx)."
                % opt.downsampled_coverage
            )
            opt.fastq1, opt.fastq2 = sv_functions.get_paired_downsampled_reads(
                opt.fastq1,
                opt.fastq2,
                "%s/downsampled_reads" % opt.outdir,
                opt.downsampled_coverage,
                opt.ref,
                replace=opt.replace,
                threads=opt.threads,
            )

        # if the reads have to be QC and trimmed:
        if opt.QC_and_trimming_reads is True or opt.input_SRRfile is not None:
            # define the reads dir
            reads_dir = "%s/reads" % opt.outdir
            sv_functions.make_folder(reads_dir)

            # define the raw reads under reads dir
            dest_fastq1 = "%s/raw_reads1.fastq.gz" % reads_dir
            dest_fastq2 = "%s/raw_reads2.fastq.gz" % reads_dir

            # define the trimmed reads
            trimmed_reads1 = "%s.trimmed.fastq.gz" % dest_fastq1
            trimmed_reads2 = "%s.trimmed.fastq.gz" % dest_fastq2

            if (
                sv_functions.file_is_empty(trimmed_reads1)
                or sv_functions.file_is_empty(trimmed_reads2)
                or opt.replace is True
            ):
                print("running trimming and QC of the reads")

                # get reads from prefetch
                if (
                    opt.input_SRRfile is not None
                    and opt.fastq1 is None
                    and opt.fastq2 is None
                ):
                    print("Getting raw reads from SRR file")

                    dest_input_SRRfile = "%s/input_SRRfile.srr" % reads_dir
                    sv_functions.soft_link_files(
                        opt.input_SRRfile, dest_input_SRRfile
                    )
                    (
                        opt.fastq1,
                        opt.fastq2,
                    ) = sv_functions.run_parallelFastqDump_on_prefetched_SRRfile(
                        dest_input_SRRfile,
                        replace=opt.replace,
                        threads=opt.threads,
                    )

                # get the reads under outdir
                sv_functions.soft_link_files(opt.fastq1, dest_fastq1)
                sv_functions.soft_link_files(opt.fastq2, dest_fastq2)

            # trim reads
            opt.fastq1, opt.fastq2 = sv_functions.run_trimmomatic(
                dest_fastq1,
                dest_fastq2,
                replace=opt.replace,
                threads=opt.threads,
            )

            # clean
            for f in os.listdir(reads_dir):
                if f not in {
                    sv_functions.get_file(opt.fastq1),
                    sv_functions.get_file(opt.fastq2),
                }:
                    sv_functions.delete_file_or_folder(
                        "%s/%s" % (reads_dir, f)
                    )

        # deifine if marking duplicates (default yes)
        if opt.skip_marking_duplicates is True:
            bwa_mem_MarkDuplicates = False
        else:
            bwa_mem_MarkDuplicates = True

        print("WORKING ON ALIGNMENT")
        sv_functions.run_bwa_mem(
            opt.fastq1,
            opt.fastq2,
            opt.ref,
            opt.outdir,
            bamfile,
            sorted_bam,
            index_bam,
            name_sample,
            threads=opt.threads,
            replace=opt.replace,
            tmpdir_writingFiles=opt.tmpdir,
            MarkDuplicates=bwa_mem_MarkDuplicates,
        )
        sv_functions.clean_sorted_bam_coverage_per_window_files(sorted_bam)

    else:
        print(
            "Warning: No fastq file given, assuming that you provided a bam"
            " file"
        )

    # check that all the important files exist
    if any([sv_functions.file_is_empty(x) for x in {sorted_bam, index_bam}]):
        raise ValueError("You need the sorted and indexed bam files in ")

end_time_alignment = time.time()

#####################################
#####################################
#####################################

###########################################
############# NECESSARY FILES #############
###########################################

# First create some files that are important for any program

# Create a reference dictionary
sv_functions.create_sequence_dict(opt.ref, replace=opt.replace)

#### calculate coverage per windows of window_l ####

if not any([x == "skip" for x in {opt.fastq1, opt.fastq2}]):
    destination_dir = "%s.calculating_windowcoverage" % sorted_bam
    coverage_file = sv_functions.generate_coverage_per_window_file_parallel(
        opt.ref,
        destination_dir,
        sorted_bam,
        windows_file="none",
        replace=opt.replace,
        run_in_parallel=True,
        delete_bams=True,
    )

####################################################

###########################################
###########################################
###########################################

if opt.StopAfter_bamFileObtention is True:
    print("Stopping pipeline after the bamfile obtention.")
    sys.exit(0)

#####################################
##### STRUCTURAL VARIATION ##########
#####################################

start_time_obtentionCloseSVs = time.time()

##### find a set of 'real_bedpe_breakpoints' that will be used for the simulations #####

if opt.real_bedpe_breakpoints is not None and opt.fast_SVcalling is False:
    print(
        "using the set of real variants from %s" % opt.real_bedpe_breakpoints
    )
    real_bedpe_breakpoints = opt.real_bedpe_breakpoints

elif opt.fast_SVcalling is False and opt.close_shortReads_table is not None:
    # the table was provided
    if opt.close_shortReads_table != "auto":
        print(
            "finding the set of compatible SVs from %s"
            % opt.close_shortReads_table
        )

        # define the outdir for the real vars
        outdir_finding_realVars = (
            "%s/findingRealSVs_providedCloseReads" % opt.outdir
        )

    # a taxID was provided, which overrides the value of opt.genomes_withSV_and_shortReads_table
    else:
        print(
            "finding close genomes or reads for close taxIDs in the SRA"
            " database for taxID %s"
            % opt.target_taxID
        )

        # define the outdir for the real vars
        outdir_finding_realVars = (
            "%s/findingRealSVs_automaticFindingOfCloseReads" % opt.outdir
        )
        sv_functions.make_folder(outdir_finding_realVars)

        # define the outdir where the close genomes whould be downloaded
        outdir_getting_closeReads = (
            "%s/getting_closeReads" % outdir_finding_realVars
        )
        sv_functions.make_folder(outdir_getting_closeReads)

        opt.close_shortReads_table = sv_functions.get_close_shortReads_table_close_to_taxID(
            opt.target_taxID,
            opt.ref,
            outdir_getting_closeReads,
            opt.ploidy,
            n_close_samples=opt.n_close_samples,
            nruns_per_sample=opt.nruns_per_sample,
            replace=opt.replace,
            threads=opt.threads,
            job_array_mode=opt.job_array_mode,
            StopAfter_sampleIndexingFromSRA=opt.StopAfter_sampleIndexingFromSRA,
            StopAfterPrefecth_of_reads=opt.StopAfterPrefecth_of_reads,
            max_coverage_sra_reads=opt.max_coverage_sra_reads,
        )

    # redefine close_shortReads_table to match n_close_samples and nruns_per_sample
    if opt.correct_close_shortReads_table_by_nRunsAndSamples is True:
        opt.close_shortReads_table = sv_functions.get_redefined_close_shortReads_table_with_meaningful_samples(
            opt.close_shortReads_table,
            n_close_samples=opt.n_close_samples,
            nruns_per_sample=opt.nruns_per_sample,
        )

    # skip the running of the pipeline
    if opt.StopAfter_readObtentionFromSRA:
        print("Stopping pipeline after the reads obtention from SRA")
        sys.exit(0)

    # skip pipeline running if you have to stop after prefetch of reads
    if opt.StopAfterPrefecth_of_reads:
        print("Stopping pipeline after the prefetch of reads")
        sys.exit(0)

    # get the real SVs
    real_bedpe_breakpoints = (
        sv_functions.get_compatible_real_bedpe_breakpoints(
            opt.close_shortReads_table,
            opt.ref,
            outdir_finding_realVars,
            replace=opt.replace,
            threads=opt.threads,
            max_nvars=opt.nvars,
            mitochondrial_chromosome=opt.mitochondrial_chromosome,
            job_array_mode=opt.job_array_mode,
            parameters_json_file=opt.parameters_json_file,
            tmpdir=opt.tmpdir,
            skip_marking_duplicates=opt.skip_marking_duplicates,
        )
    )

else:
    print("Avoiding the simulation of real variants. Only inserting randomSV.")

    # define the set of vars as empty. This will trigger the random generation of vars
    real_bedpe_breakpoints = None


if opt.StopAfter_obtentionOFcloseSVs:
    print("stopping pipeline after obtention of close SVs")
    sys.exit(0)

end_time_obtentionCloseSVs = time.time()

# test that the real_bedpe_breakpoints are correct
if real_bedpe_breakpoints is not None and not os.path.isfile(
    real_bedpe_breakpoints
):
    raise ValueError(
        "The provided real bedpe breakpoints %s are incorrect."
        % real_bedpe_breakpoints
    )

###################################################################################################

# test accuracy on real data
if opt.testAccuracy is True:
    print("testing accuracy on simulations and real variants (if provided)")

    # test that you have provided a opt.close_shortReads_table
    if opt.close_shortReads_table is None or opt.fast_SVcalling is True:
        raise ValueError(
            "You have to specify a --close_shortReads_table or"
            " --real_bedpe_breakpoints and not run in --fast_SVcalling to test"
            " the accuracy of the pipeline on several datasets"
            " (--testAccuracy)"
        )

    ### RUN PERSVADE ###
    print("testing perSVade on several samples. --tmpdir is %s" % opt.tmpdir)

    dict_perSVade_outdirs = sv_functions.report_accuracy_realSVs_perSVadeRuns(
        opt.close_shortReads_table,
        opt.ref,
        "%s/testing_Accuracy" % opt.outdir,
        real_bedpe_breakpoints,
        threads=opt.threads,
        replace=opt.replace,
        n_simulated_genomes=opt.nsimulations,
        mitochondrial_chromosome=opt.mitochondrial_chromosome,
        simulation_ploidies=simulation_ploidies,
        range_filtering_benchmark=opt.range_filtering_benchmark,
        nvars=opt.nvars,
        job_array_mode=opt.job_array_mode,
        parameters_json_file=opt.parameters_json_file,
        gff=opt.gff,
        replace_FromGridssRun_final_perSVade_run=opt.replace_FromGridssRun_final_perSVade_run,
        fraction_available_mem=opt.fraction_available_mem,
        replace_SV_CNVcalling=opt.replace_SV_CNVcalling,
        skip_CNV_calling=opt.skip_CNV_calling,
        outdir_finding_realVars=outdir_finding_realVars,
        simulate_SVs_around_HomologousRegions_previousBlastnFile=opt.simulate_SVs_around_HomologousRegions_previousBlastnFile,
        simulate_SVs_around_HomologousRegions_maxEvalue=opt.simulate_SVs_around_HomologousRegions_maxEvalue,
        simulate_SVs_around_HomologousRegions_queryWindowSize=opt.simulate_SVs_around_HomologousRegions_queryWindowSize,
        skip_SV_CNV_calling=opt.skip_SV_CNV_calling,
        tmpdir=opt.tmpdir,
        simulation_chromosomes=opt.simulation_chromosomes,
        testAccuracy_skipHomRegionsSimulation=opt.testAccuracy_skipHomRegionsSimulation,
    )

    if opt.StopAfter_testAccuracy_perSVadeRunning is True:
        print(
            "You already ran all the configurations of perSVade. Stopping"
            " after the running of perSVade on testAccuracy"
        )
        sys.exit(0)

    ####################

    ### REPORT ACCURACY SINGLE SAMPLE ###
    # youhavetoaddcodeof_codeGraveyard_report_accuracy_realSVs

    if opt.StopAfter_testAccuracy is True:
        print(" Stopping after the running of perSVade on testAccuracy")
        sys.exit(0)

    #####################################


# get the golden set
if opt.goldenSet_table is not None:
    # run jobs golden set testing
    outdir_goldenSet = "%s/testing_goldenSetAccuracy" % opt.outdir
    dict_paths_goldenSetAnalysis = sv_functions.report_accuracy_golden_set_runJobs(
        opt.goldenSet_table,
        outdir_goldenSet,
        opt.ref,
        real_bedpe_breakpoints,
        threads=opt.threads,
        replace=opt.replace,
        n_simulated_genomes=opt.nsimulations,
        mitochondrial_chromosome=opt.mitochondrial_chromosome,
        simulation_ploidies=simulation_ploidies,
        range_filtering_benchmark=opt.range_filtering_benchmark,
        nvars=opt.nvars,
        job_array_mode=opt.job_array_mode,
        StopAfterPrefecth_of_reads=opt.StopAfterPrefecth_of_reads_goldenSet,
        target_taxID=opt.target_taxID,
        parameters_json_file=opt.parameters_json_file,
        fraction_available_mem=opt.fraction_available_mem,
        verbose=opt.verbose,
        simulate_SVs_around_HomologousRegions_previousBlastnFile=opt.simulate_SVs_around_HomologousRegions_previousBlastnFile,
        simulate_SVs_around_HomologousRegions_maxEvalue=opt.simulate_SVs_around_HomologousRegions_maxEvalue,
        simulate_SVs_around_HomologousRegions_queryWindowSize=opt.simulate_SVs_around_HomologousRegions_queryWindowSize,
        max_n_samples=opt.goldenSet_max_n_samples,
    )

    # plot the accurac
    sv_functions.report_accuracy_golden_set_reportAccuracy(
        dict_paths_goldenSetAnalysis,
        outdir_goldenSet,
        opt.ref,
        threads=opt.threads,
        replace=opt.replace,
    )

    if opt.StopAfter_goldenSetAnalysis is True:
        print(" Stopping after the running of golden-set analysis")
        sys.exit(0)

start_time_SVcalling = time.time()

# run the actual perSVade function optimising parameters
if opt.skip_SVcalling is False and not any(
    [x == "skip" for x in {opt.fastq1, opt.fastq2}]
):
    SVdetection_outdir = "%s/SVdetection_output" % opt.outdir
    outdir_gridss_final = sv_functions.run_GridssClove_optimising_parameters(
        sorted_bam,
        opt.ref,
        SVdetection_outdir,
        threads=opt.threads,
        replace=opt.replace,
        n_simulated_genomes=opt.nsimulations,
        mitochondrial_chromosome=opt.mitochondrial_chromosome,
        simulation_ploidies=simulation_ploidies,
        range_filtering_benchmark=opt.range_filtering_benchmark,
        nvars=opt.nvars,
        fast_SVcalling=opt.fast_SVcalling,
        real_bedpe_breakpoints=real_bedpe_breakpoints,
        replace_FromGridssRun_final_perSVade_run=opt.replace_FromGridssRun_final_perSVade_run,
        tmpdir=opt.tmpdir,
        simulation_chromosomes=opt.simulation_chromosomes,
    )

end_time_SVcalling = time.time()

print("structural variation analysis with perSVade finished")

#####################################
#####################################
#####################################

###########################
###### CNV CALLING ########
###########################

# run CNVcalling by getting df_CNV_coverage
minimal_CNV_fields = [
    "chromosome",
    "merged_relative_CN",
    "start",
    "end",
    "CNVid",
    "median_coverage",
    "median_coverage_corrected",
    "SVTYPE",
] + ["median_relative_CN_%s" % x for x in cnv_calling_algs]

run_CNV_calls = opt.skip_CNV_calling is False and not any(
    [x == "skip" for x in {opt.fastq1, opt.fastq2}]
)
if run_CNV_calls is True:
    print("RUNNING COVERAGE-BASED CNV CALLING...")

    # make folder
    cnv_calling_outdir = "%s/CNV_calling" % opt.outdir
    sv_functions.make_folder(cnv_calling_outdir)

    # run CNV calling
    df_CNV_coverage = sv_functions.run_CNV_calling(
        sorted_bam,
        opt.ref,
        cnv_calling_outdir,
        opt.threads,
        opt.replace,
        opt.mitochondrial_chromosome,
        opt.window_size_CNVcalling,
        opt.ploidy,
        bg_sorted_bam_CNV=opt.bg_sorted_bam_CNV,
        cnv_calling_algs=cnv_calling_algs,
    )

else:
    df_CNV_coverage = pd.DataFrame(columns=minimal_CNV_fields)

###########################
###########################
###########################

#####################################
###### SV and CNV ANNOTATION ########
#####################################

start_time_SVandCNVcalling = time.time()

run_SV_CNV_calling = (
    opt.skip_SVcalling is False
    and not any([x == "skip" for x in {opt.fastq1, opt.fastq2}])
    and opt.skip_SV_CNV_calling is False
)
if run_SV_CNV_calling is True:
    print("running CNV calling per window and integrating to SV calling")

    # define outdirs
    outdir_var_calling = "%s/SVcalling_output" % opt.outdir

    # remove folders if there is some replacement to be done. Remove
    if opt.replace_SV_CNVcalling is True:
        sv_functions.delete_folder(outdir_var_calling)

    # stop after the removal
    if opt.StopAfter_replace_SV_CNVcalling is True:
        print("exitting after the --replace_SV_CNVcalling action")
        sys.exit(0)

    # make folder
    sv_functions.make_folder(outdir_var_calling)

    # get the variant calling
    SV_CNV_vcf = sv_functions.get_vcf_all_SVs_and_CNV(
        opt.outdir,
        outdir_var_calling,
        sorted_bam,
        opt.ref,
        opt.ploidy,
        df_CNV_coverage,
        opt.window_size_CNVcalling,
        cnv_calling_algs,
        replace=opt.replace,
        threads=opt.threads,
        mitochondrial_chromosome=opt.mitochondrial_chromosome,
    )

    print("the SV and CNV calling vcf can be found in %s" % SV_CNV_vcf)

    # get variant annotation
    if opt.gff is not None:
        # remove the annotated vcf if needed
        if opt.replace_var_annotation is True:
            sv_functions.remove_file("%s_annotated_VEP.tab" % SV_CNV_vcf)
            sv_functions.remove_file(
                "%s_annotated_VEP.tab.raw.tbl.tmp_summary.html" % SV_CNV_vcf
            )

        print("annotating SV, CNV variants with VEP")
        SV_CNV_vcf_annotated = sv_functions.annotate_SVs_inHouse(
            SV_CNV_vcf,
            gff_with_biotype,
            opt.ref,
            replace=opt.replace,
            threads=opt.threads,
            mitochondrial_chromosome=opt.mitochondrial_chromosome,
            mito_code=opt.mitochondrial_code,
            gDNA_code=opt.gDNA_code,
        )

        print("annotated SV vcf can be found in %s" % SV_CNV_vcf_annotated)

    else:
        print("WARNING: Skipping SV annotation because -gff was not provided.")

end_time_SVandCNVcalling = time.time()

#####################################
#####################################
#####################################

# stop after the generation of SV and CNV calls

#####################################
###### SMALL VARS AND CNV ###########
#####################################

start_time_smallVarsCNV = time.time()

if opt.run_smallVarsCNV:
    # define an outdir
    outdir_varcall = "%s/smallVars_CNV_output" % opt.outdir

    # define the basic cmd
    varcall_cmd = (
        "%s -r %s --threads %i --outdir %s -sbam %s --caller %s --coverage %i"
        " --mitochondrial_chromosome %s --mitochondrial_code %i --gDNA_code %i"
        " --minAF_smallVars %s --window_freebayes_bp %i --log_file_all_cmds %s"
        % (
            VARCALL_CNV_PIPELINE,
            opt.ref,
            opt.threads,
            outdir_varcall,
            sorted_bam,
            opt.caller,
            opt.coverage,
            opt.mitochondrial_chromosome,
            opt.mitochondrial_code,
            opt.gDNA_code,
            opt.minAF_smallVars,
            opt.window_freebayes_bp,
            sv_functions.log_file_all_cmds,
        )
    )

    # add options
    if opt.replace is True:
        varcall_cmd += " --replace"
    if opt.gff is not None:
        varcall_cmd += " -gff %s" % opt.gff
    if opt.StopAfter_smallVarCallSimpleRunning is True:
        varcall_cmd += " --StopAfter_smallVarCallSimpleRunning"
    if opt.replace_var_integration is True:
        varcall_cmd += " --replace_var_integration"
    if opt.pooled_sequencing is True:
        varcall_cmd += " --pooled_sequencing"
    if opt.consider_repeats_smallVarCall is True:
        varcall_cmd += " --repeats_table %s" % repeats_table_file
    if opt.generate_alternative_genome is True:
        varcall_cmd += " --generate_alternative_genome"
    if opt.skip_cnv_per_gene_analysis is True:
        varcall_cmd += " --skip_cnv_analysis"

    # define which ploidies to run
    if opt.ploidy == 1 and opt.run_ploidy2_ifHaploid is False:
        ploidies_varcall = [1]
    if opt.ploidy == 1 and opt.run_ploidy2_ifHaploid is True:
        ploidies_varcall = [1, 2]
    else:
        ploidies_varcall = [opt.ploidy]

    # run for each ploidy
    for ploidy_varcall in ploidies_varcall:
        # remove the annotation-derived outputs
        if opt.replace_var_annotation is True:
            sv_functions.remove_file(
                "%s/variant_annotation_ploidy%i.tab"
                % (outdir_varcall, ploidy_varcall)
            )
            sv_functions.delete_folder("%s/CNV_results" % outdir_varcall)

        # run the variant calling command
        varcall_cmd += " -p %i" % ploidy_varcall
        if __name__ == "__main__":
            sv_functions.run_cmd(varcall_cmd)

        # regenerate the variant calling file according to run_SV_CNV_calling
        if run_CNV_calls is True:
            sv_functions.get_small_variant_calling_withCNstate(
                "%s/variant_calling_ploidy%i.tab"
                % (outdir_varcall, ploidy_varcall),
                df_CNV_coverage,
                replace=(
                    opt.replace or opt.replace_addingCNstate_to_smallVars
                ),
            )

    # define the small variants vcf
    small_vars_vcf = "%s/variants_atLeast1PASS_ploidy%i.vcf" % (
        outdir_varcall,
        opt.ploidy,
    )

    # define the variant annotation
    small_vars_var_annotation = "%s/variant_annotation_ploidy%i.tab" % (
        outdir_varcall,
        opt.ploidy,
    )

    # clean the varcall dir if specified
    if opt.remove_smallVarsCNV_nonEssentialFiles is True:
        sv_functions.remove_smallVarsCNV_nonEssentialFiles_severalPloidies(
            outdir_varcall, ploidies_varcall
        )

end_time_smallVarsCNV = time.time()

if opt.StopAfter_smallVarCall is True:
    print("WARNING: Ending after the running of small variant calling...")
    sys.exit(0)

#####################################
#####################################
#####################################


#####################################
##### VARIANTS VISUALIZATION ########
#####################################

if (
    (opt.skip_SVcalling is False or opt.run_smallVarsCNV is True)
    and not any([x == "skip" for x in {opt.fastq1, opt.fastq2}])
    and opt.visualization_results is True
    and opt.gff is not None
):
    # visualize the results with the browser

    # create a table with the data to visualize the browser for this sample. This will include many things
    dict_data = {"sorted_bam": sorted_bam, "sampleID": name_sample}
    if opt.skip_SVcalling is False:
        dict_data["SV_CNV_vcf"] = SV_CNV_vcf
        dict_data["SV_CNV_var_annotation"] = SV_CNV_vcf_annotated

    if opt.run_smallVarsCNV is True:
        dict_data["smallVars_vcf"] = small_vars_vcf
        dict_data["smallVars_var_annotation"] = small_vars_var_annotation

    # make df
    df_visualization = pd.DataFrame({0: dict_data}).transpose()

    # save to file
    outdir_visualization = "%s/variant_visualization" % opt.outdir
    sv_functions.make_folder(outdir_visualization)
    visualization_file = "%s/visualization_data.tab" % outdir_visualization
    df_visualization.to_csv(
        visualization_file, sep="\t", index=False, header=True
    )

    # get the visualization cmd
    cmd_visualization = (
        "%s --input_data %s --outdir %s --reference_genome %s --gff %s"
        " --threads %i --only_affected_genes --mitochondrial_chromosome %s"
        % (
            PERSVADE_GENOME_BROWSER,
            visualization_file,
            outdir_visualization,
            opt.ref,
            opt.gff,
            opt.threads,
            opt.mitochondrial_chromosome,
        )
    )
    if opt.replace is True:
        cmd_visualization += " --replace"

    sv_functions.run_cmd(cmd_visualization)

#####################################
#####################################
#####################################

# keep the simulation files
if opt.keep_simulation_files is True:
    sv_functions.keep_simulation_files_for_perSVade_outdir(
        opt.outdir,
        replace=opt.replace,
        n_simulated_genomes=opt.nsimulations,
        simulation_ploidies=simulation_ploidies,
    )

# at the end you want to clean the outdir to keep only the essential files
if opt.skip_cleaning_outdir is False:
    sv_functions.clean_perSVade_outdir(opt.outdir)

# define times
end_time_all = time.time()

# generate a file that indicates whether the gridss run is finished
sv_functions.generate_final_file_report(
    final_file,
    start_time_general_processing,
    end_time_GeneralProcessing,
    start_time_alignment,
    end_time_alignment,
    start_time_all,
    end_time_all,
    start_time_obtentionCloseSVs,
    end_time_obtentionCloseSVs,
    start_time_SVcalling,
    end_time_SVcalling,
    start_time_SVandCNVcalling,
    end_time_SVandCNVcalling,
    start_time_smallVarsCNV,
    end_time_smallVarsCNV,
)

print("perSVade Finished correctly")
