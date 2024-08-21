from abc import ABC, abstractmethod

from schemas.read_file import File


class AbstractFTPSubmissionService(ABC):
    @abstractmethod
    def upload_file(self, file: File, ena_user: str, ena_pass: str, ena_ftp_upload_dir: str, test: bool):
        pass
