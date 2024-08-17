import os

from pydantic import BaseModel, ConfigDict

from adapters.api_submission_service import APISubmissionService
from core.config import settings
from core.loguru import logger
from domain.services.abstract_api_submission_service import AbstractAPISubmissionService
from exceptions import ResponseError
from schemas.accessions import RawReadsAccession
from use_cases.receipt_utils.parse_raw_reads_accessions import parse_raw_reads_accession
from use_cases.receipt_utils.save_receipt import save_receipt
from use_cases.validate_xml_file import validate_xml_file


class RawReadsSubmission(BaseModel):
    experiment_set_xml_path: str
    run_set_xml_path: str
    submission_xml_path: str
    ena_username: str
    ena_password: str
    results_dir: str
    test: bool
    api_submission_service: AbstractAPISubmissionService = APISubmissionService()

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def register_raw_reads(self) -> RawReadsAccession:
        logger.info('Validating Experiment Set XML file...')
        validate_xml_file(xml_file_path=self.experiment_set_xml_path,
                          xsd_schema_path=os.path.join(settings.XSD_SCHEMAS_PATH, 'SRA.experiment.xsd'))

        logger.info('Validating Run Set XML file...')
        validate_xml_file(xml_file_path=self.run_set_xml_path,
                          xsd_schema_path=os.path.join(settings.XSD_SCHEMAS_PATH, 'SRA.run.xsd'))

        logger.info('Validating Submission XML file...')
        validate_xml_file(xml_file_path=self.submission_xml_path,
                          xsd_schema_path=os.path.join(settings.XSD_SCHEMAS_PATH, 'SRA.submission.xsd'))

        logger.info('Registering Raw Reads (Experiment / Run) to ENA...')
        r = self.api_submission_service.submit_files(
            files={
                'SUBMISSION': self.submission_xml_path,
                'EXPERIMENT': self.experiment_set_xml_path,
                'RUN': self.run_set_xml_path
            },
            ena_user=self.ena_username, ena_pass=self.ena_password, test=self.test)
        if r.status_code != 200:
            raise ResponseError(response=r)

        receipt_path = os.path.join(self.results_dir, 'raw_reads_receipt.xml')
        save_receipt(text=r.text, receipt_path=receipt_path)
        logger.info(f'Raw reads receipt has been saved to: {receipt_path}')

        raw_reads_accession = parse_raw_reads_accession(log_str=r.text)

        logger.info(
            f'The raw reads (Experiment / Run) have been successfully registered in ENA. Experiment accession: '
            f'{raw_reads_accession.experiment_accession}')

        return raw_reads_accession
