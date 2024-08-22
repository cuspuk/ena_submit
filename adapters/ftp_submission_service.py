import ftplib

from core.config import settings
from core.loguru import logger
from domain.services.abstract_ftp_submission_service import AbstractFTPSubmissionService
from schemas.read_file import File


def ftps_upload(file_source_path: str, ftp: ftplib.FTP_TLS, target_filename: str, test: bool):
    tmp_filename = f'{target_filename}.tmp'

    existing_files = ftp.nlst()

    if tmp_filename in existing_files:
        raise FileExistsError(f'{tmp_filename=} already exists in ENA FTP server')

    if target_filename in existing_files:
        raise FileExistsError(f'{target_filename=} already exists in ENA FTP server')

    with open(file_source_path, 'rb') as source_file:
        response = ftp.storbinary(f'STOR {tmp_filename}', source_file)

        logger.info(f'Received {response=} when exporting {file_source_path=}')

        # Try to delete the target file first
        if target_filename in ftp.nlst():
            ftp.delete(target_filename)

        # Throws permission error if target file exists
        if not test:
            ftp.rename(tmp_filename, target_filename)
            logger.info(f'Renaming temp uploaded file to {target_filename} in ENA FTP server')
        else:
            ftp.delete(tmp_filename)
            logger.info(f'Deleting uploaded file {tmp_filename} from ENA FTP server')


class FTPSubmissionService(AbstractFTPSubmissionService):
    def upload_file(self, file: File, ena_user: str, ena_pass: str, ena_ftp_upload_dir: str,
                    test: bool) -> None:
        with ftplib.FTP_TLS() as ftp:
            hostname = settings.ENA_HOST
            port = 21

            ftp.connect(host=hostname, port=port)
            ftp.login(user=ena_user, passwd=ena_pass)
            ftp.cwd(ena_ftp_upload_dir)

            ftps_upload(file_source_path=file.absolute_filepath, ftp=ftp, target_filename=file.target_filename,
                        test=test)

        logger.info(f'{file.absolute_filepath=} uploaded to ENA FTP server')
