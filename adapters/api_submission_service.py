import requests
from requests.auth import HTTPBasicAuth

from domain.services.abstract_api_submission_service import AbstractAPISubmissionService
from schemas.submit_files import SubmitFiles


class APISubmissionService(AbstractAPISubmissionService):
    def submit_files(self, files: SubmitFiles, ena_user: str, ena_pass: str, test: bool) -> requests.Response:
        if test:
            url = 'https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit/'
        else:
            url = 'https://www.ebi.ac.uk/ena/submit/drop-box/submit/'

        files_dict = files.model_dump(exclude_unset=True)

        return requests.post(
            url=url,
            auth=(ena_user, ena_pass),
            files={key: open(path) for key, path in files_dict.items()}
        )

    def fetch_biosample_accession(self, sample_accession: str, ena_user: str, ena_pass: str, test: bool) -> str:
        if test:
            url = f'https://wwwdev.ebi.ac.uk/ena/submit/drop-box/cli/reference/sample/{sample_accession}'
        else:
            url = f'https://www.ebi.ac.uk/ena/submit/drop-box/cli/reference/sample/{sample_accession}'

        response = requests.get(
            url=url,
            headers={'Accept': 'application/json'},
            auth=HTTPBasicAuth(ena_user, ena_pass)
        )

        if response.status_code != 200:
            raise Exception(f'Failed to fetch biosample ID for {sample_accession}. Response: {response.text}')

        try:
            biosample_accession = response.json()['bioSampleId']
        except KeyError:
            raise Exception(f'Failed to fetch biosample ID for {sample_accession}. Response: {response.text}')

        return biosample_accession
