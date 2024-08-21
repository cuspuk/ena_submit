from pydantic import BaseModel, ConfigDict

from adapters.webin_cli_submission_service import WebinCLISubmissionService
from core.loguru import logger
from domain.services.abstract_webin_cli_submission_service import AbstractWebinCLISubmissionService


class AssemblySubmission(BaseModel):
    manifest_json_path: str
    ena_username: str
    ena_password: str
    results_dir: str
    test: bool
    webin_cli_submission_service: AbstractWebinCLISubmissionService

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def submit_assembly(self) -> None:
        logger.info(f'Assembly validation / submission logs will be saved to: {self.results_dir}')

        logger.info('Validating assembly manifest...')
        self.webin_cli_submission_service.validate_assembly_manifest(manifest_json_path=self.manifest_json_path,
                                                                     log_dir_path=self.results_dir,
                                                                     test=self.test,
                                                                     ena_pass=self.ena_password,
                                                                     ena_user=self.ena_username)

        logger.info('Uploading assembly manifest to ENA...')
        self.webin_cli_submission_service.submit_assembly_manifest(
            manifest_json_path=self.manifest_json_path,
            log_dir_path=self.results_dir,
            test=self.test,
            ena_user=self.ena_username,
            ena_pass=self.ena_password
        )
