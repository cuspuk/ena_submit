import argparse
import json

from adapters.api_submission_service import APISubmissionService
from adapters.ftp_submission_service import FTPSubmissionService
from adapters.webin_cli_submission_service import WebinCLISubmissionService
from core.loguru import logger
from domain.entities.assembly_submission import AssemblySubmission
from domain.entities.ftp_read_files_upload import FTPReadFilesUpload
from domain.entities.raw_reads_submission import RawReadsSubmission
from domain.entities.sample_registration import SampleRegistration
from schemas.submit_config import SubmitConfig
from use_cases.register_sample_to_ena import register_sample_to_ena
from use_cases.submit_assembly_to_ena import submit_assembly_to_ena
from use_cases.submit_raw_reads_to_ena import submit_raw_reads_to_ena
from use_cases.upload_read_files_to_ena import upload_read_files_to_ena


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='This script processes input files and information for ENA submission using a configuration file.'
    )

    parser.add_argument('--config', type=str, required=True, help='Path to the configuration JSON file.')

    args = parser.parse_args()

    return args


def load_submit_config(config_path: str) -> SubmitConfig:
    with open(config_path, 'r') as f:
        config_data = json.load(f)
        try:
            config = SubmitConfig(**config_data)
        except Exception as e:
            raise ValueError(
                f'Invalid configuration file. Please check the configuration file and try again. Error: {e}')
    return config


def main():
    args = parse_arguments()
    try:
        submit_config = load_submit_config(args.config)
    except Exception as e:
        logger.info(e)
        return

    upload_read_files_to_ena(
        ftp_read_files_upload=FTPReadFilesUpload(
            **submit_config.dict(),
            ena_ftp_upload_dir='/',
            ftp_submission_service=FTPSubmissionService()
        )
    )

    sample_accessions = register_sample_to_ena(
        sample_registration=SampleRegistration(
            **submit_config.dict(),
            api_submission_service=APISubmissionService()
        )
    )

    submit_raw_reads_to_ena(
        raw_reads_submission=RawReadsSubmission(
            **submit_config.dict(),
            api_submission_service=APISubmissionService()
        ),
        submission_accession=sample_accessions.submission_accession
    )

    submit_assembly_to_ena(
        assembly_submission=AssemblySubmission(
            **submit_config.dict(),
            webin_cli_submission_service=WebinCLISubmissionService()
        ),
        submission_accession=sample_accessions.submission_accession
    )


if __name__ == "__main__":
    main()
