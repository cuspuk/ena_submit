import requests

from domain.services.abstract_api_submission_service import AbstractAPISubmissionService


class APISubmissionService(AbstractAPISubmissionService):
    def submit_files(self, files: dict[str, str], ena_user: str, ena_pass: str, test: bool) -> requests.Response:
        if test:
            url = 'https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/'
        else:
            url = 'https://www.ebi.ac.uk/ena/submit/drop-box/submit/'

        return requests.post(
            url,
            auth=(ena_user, ena_pass),
            files={key: open(path) for key, path in files.items()}
        )
