from abc import ABC, abstractmethod
from requests import Response


class AbstractAPISubmissionService(ABC):
    @abstractmethod
    def submit_files(self, files: dict[str, str], ena_user: str, ena_pass: str, test: bool) -> Response:
        pass
