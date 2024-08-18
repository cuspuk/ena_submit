from abc import ABC, abstractmethod
from typing import Literal


class AbstractWebinCLISubmissionService(ABC):
    @abstractmethod
    def validate_assembly_manifest(self, manifest_json_path: str, log_dir_path: str, test: bool, ena_user: str,
                                   ena_pass: str) -> None:
        pass

    @abstractmethod
    def submit_assembly_manifest(self, manifest_json_path: str, log_dir_path: str, test: bool, ena_user: str, ena_pass: str,
                                 context: Literal['genome', 'transcriptome', 'sequence', 'reads'] = 'genome') -> None:
        pass
