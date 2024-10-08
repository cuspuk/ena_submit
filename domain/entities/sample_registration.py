import os

from pydantic import BaseModel, ConfigDict

from core.config import settings
from core.loguru import logger
from domain.services.abstract_api_submission_service import AbstractAPISubmissionService
from exceptions import ResponseError
from schemas.accessions import SampleAccessions
from schemas.submit_files import SubmitFiles
from use_cases.receipt_utils.parse_sample_accessions import parse_sample_accessions_from_response
from use_cases.receipt_utils.save_receipt import save_receipt
from use_cases.validate_xml_file import validate_xml_file


class SampleRegistration(BaseModel):
    sample_set_xml_path: str
    submission_xml_path: str
    ena_username: str
    ena_password: str
    results_dir: str
    test: bool
    api_submission_service: AbstractAPISubmissionService

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def register_sample(self) -> SampleAccessions:
        logger.info('Validating SampleSet XML file...')
        validate_xml_file(xml_file_path=self.sample_set_xml_path,
                          xsd_schema_path=os.path.join(settings.XSD_SCHEMAS_PATH, 'SRA.sample.xsd'))

        logger.info('Validating Submission XML file...')
        validate_xml_file(xml_file_path=self.submission_xml_path,
                          xsd_schema_path=os.path.join(settings.XSD_SCHEMAS_PATH, 'SRA.submission.xsd'))

        logger.info('Registering Sample to ENA...')
        r = self.api_submission_service.submit_files(
            files=SubmitFiles(SUBMISSION=self.submission_xml_path, SAMPLE=self.sample_set_xml_path),
            ena_user=self.ena_username, ena_pass=self.ena_password, test=self.test)
        if r.status_code != 200:
            raise ResponseError(response=r)

        receipt_path = os.path.join(self.results_dir, 'sample_receipt.xml')
        save_receipt(text=r.text, receipt_path=receipt_path)
        logger.info(f'Sample receipt has been saved to: {receipt_path}')

        sample_accessions = parse_sample_accessions_from_response(
            response=r,
            ena_user=self.ena_username,
            ena_pass=self.ena_password,
            api_submission_service=self.api_submission_service,
            test=self.test
        )

        logger.info(
            f'Sample has been registered into ENA. Sample accession: {sample_accessions.submission_accession} '
            f'Biosample accession: {sample_accessions.biosample_accession}')

        return sample_accessions
