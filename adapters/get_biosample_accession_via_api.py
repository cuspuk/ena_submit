import requests
from requests.auth import HTTPBasicAuth


def fetch_biosample_accession(sample_accession: str, ena_user: str, ena_pass: str) -> str:
    response = requests.get(
        f'https://www.ebi.ac.uk/ena/submit/drop-box/cli/reference/sample/{sample_accession}',
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
