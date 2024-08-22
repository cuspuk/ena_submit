from abc import ABC, abstractmethod
from requests import Response


class AbstractAPISubmissionService(ABC):
    @abstractmethod
    def submit_files(self, files: dict[str, str], ena_user: str, ena_pass: str, test: bool) -> Response:
        pass

    @abstractmethod
    def fetch_biosample_accession(self, sample_accession: str, ena_user: str, ena_pass: str) -> str:
        pass
