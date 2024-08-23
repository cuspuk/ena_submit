import os
from typing import Literal

from core.config import settings
from core.loguru import logger
from domain.services.abstract_webin_cli_submission_service import AbstractWebinCLISubmissionService
from exceptions import WebinCLIFileUploadError, WebinCLIFileValidationError
from use_cases.receipt_utils.parse_sample_accessions import get_accession_inside_double_quotes_from_log


def read_log_file(log_path: str) -> list[str]:
    with open(log_path) as f:
        return f.readlines()


class WebinCLISubmissionService(AbstractWebinCLISubmissionService):
    def validate_assembly_manifest(self, manifest_json_path: str, log_dir_path: str, test: bool, ena_user: str,
                                   ena_pass: str, webin_cli_path: str,
                                   context: Literal['genome', 'transcriptome', 'sequence', 'reads'] = 'genome') -> None:
        validation_log_path = os.path.join(log_dir_path, 'ena_webin_cli_validation.log')
        run_type = '-test' if test else ''
        exit_code = os.system(
            f'{webin_cli_path} \
                            -username {ena_user} \
                            -password {ena_pass} \
                            -context {context} \
                            -manifest {manifest_json_path} \
                            -validate \
                            -outputDir {log_dir_path} \
                            {run_type} > {validation_log_path}'
        )
        if exit_code == 0:
            logger.info('Assembly Manifest have been validated successfully')
        else:
            raise WebinCLIFileValidationError(log_path=log_dir_path)

    def submit_assembly_manifest(self, manifest_json_path: str, log_dir_path: str, test: bool, ena_user: str,
                                 ena_pass: str, webin_cli_path: str,
                                 context: Literal['genome', 'transcriptome', 'sequence', 'reads'] = 'genome') -> None:
        submit_log_path = os.path.join(log_dir_path, 'ena_webin_cli_submit.log')
        run_type = '-test' if test else ''
        exit_code = os.system(
            f'{webin_cli_path} \
                    -username {ena_user} \
                    -password {ena_pass} \
                    -context {context} \
                    -manifest {manifest_json_path} \
                    -submit \
                    -outputDir {log_dir_path} \
                    {run_type} > {submit_log_path}'
        )
        if exit_code == 0:
            logger.info('Assembly Manifest have been uploaded successfully')
        else:
            log = read_log_file(submit_log_path)
            pattern = 'The object being added already exists in the submission account with accession:'
            for line in log:
                if pattern in line:
                    accession = get_accession_inside_double_quotes_from_log(pattern=pattern, log_str=line)
                    logger.warning(f'Assembly Manifest already exists in the ENA database under accession: {accession}')
                    return
            else:
                raise WebinCLIFileUploadError(log_path=log_dir_path)
