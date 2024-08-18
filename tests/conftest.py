import os
from typing import Literal

import pytest
from requests import Response

from adapters.webin_cli_submission_service import WebinCLISubmissionService
from core.config import settings
from core.loguru import logger
from domain.services.abstract_api_submission_service import AbstractAPISubmissionService
from exceptions import WebinCLIFileValidationError


class MockAPISampleSubmissionService(AbstractAPISubmissionService):
    def submit_files(self, files: dict[str, str], ena_user: str, ena_pass: str, test: bool) -> Response:
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b"""<?xml version="1.0" encoding="UTF-8"?>
                <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
                <RECEIPT receiptDate="2024-02-23T07:08:53.866Z" submissionFile="submission.xml" success="true">
                     <SAMPLE accession="ERS28175515" alias="ENA sample - s_1-e_1" status="PRIVATE">
                          <EXT_ID accession="SAMEA130841939" type="biosample"/>
                     </SAMPLE>
                     <SUBMISSION accession="ERA29152472" alias="SUBMISSION-23-02-2024-07:08:53:080"/>
                     <MESSAGES>
                          <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
                     </MESSAGES>
                     <ACTIONS>ADD</ACTIONS>
                </RECEIPT>
            """
        return mock_response


class MockAPIRawReadsSubmissionService(AbstractAPISubmissionService):
    def submit_files(self, files: dict[str, str], ena_user: str, ena_pass: str, test: bool) -> Response:
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b"""<?xml version="1.0" encoding="UTF-8"?>
            <RECEIPT receiptDate="2017-08-11T15:07:36.746+01:00" submissionFile="sub.xml" success="true">
               <EXPERIMENT accession="ERX2151578" alias="exp_mantis_religiosa" status="PRIVATE"/>
               <RUN accession="ERR2094164" alias="run_mantis_religiosa" status="PRIVATE"/>
               <SUBMISSION accession="ERA986371" alias="mantis_religiosa_submission"/>
               <MESSAGES>
                   <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
               </MESSAGES>
               <ACTIONS>ADD</ACTIONS>
               <ACTIONS>ADD</ACTIONS>
            </RECEIPT>
            """
        return mock_response


class MockWebinCLISubmissionService(WebinCLISubmissionService):
    def validate_assembly_manifest(self, manifest_json_path: str, log_dir_path: str, test: bool, ena_user: str,
                                   ena_pass: str,
                                   context: Literal['genome', 'transcriptome', 'sequence', 'reads'] = 'genome') -> None:
        validation_log_path = os.path.join(log_dir_path, 'ena_webin_cli_validation.log')
        run_type = '-test' if test else ''
        exit_code = os.system(
            f'{settings.ENA_WEBIN_CLI} \
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
                                 ena_pass: str,
                                 context: Literal['genome', 'transcriptome', 'sequence', 'reads'] = 'genome') -> None:
        pass


@pytest.fixture(scope='function')
def mock_api_sample_submission_service():
    return MockAPISampleSubmissionService()


@pytest.fixture(scope='function')
def mock_api_raw_reads_submission_service():
    return MockAPIRawReadsSubmissionService()


@pytest.fixture(scope='function')
def mock_webin_cli_submission_service():
    return MockWebinCLISubmissionService()
