import os

from pydantic import BaseModel, ConfigDict

from adapters.ftp_submission_service import FTPSubmissionService
from core.loguru import logger
from domain.services.abstract_ftp_submission_service import AbstractFTPSubmissionService
from exceptions import ReadsExportMissingFileError
from schemas.read_file import ReadFile


class FTPReadFilesUpload(BaseModel):
    reads: list[ReadFile]
    ena_username: str
    ena_password: str
    ena_ftp_upload_dir: str
    test: bool
    ftp_submission_service: AbstractFTPSubmissionService

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def upload_read_files(self) -> None:
        for read_file in self.reads:
            if not os.path.exists(read_file.absolute_filepath):
                raise ReadsExportMissingFileError(full_path=read_file.absolute_filepath)

            logger.info(
                f'Running {'Testing' if self.test else 'Production'} uploading of the Read file '
                f'{read_file.absolute_filepath=} to ENA FTP server...')

            self.ftp_submission_service.upload_file(file=read_file, ena_user=self.ena_username,
                                                    ena_pass=self.ena_password, test=self.test,
                                                    ena_ftp_upload_dir=self.ena_ftp_upload_dir)

        logger.info('All read files have been uploaded to the ENA FTP server')
