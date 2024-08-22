import re

import requests

from core.loguru import logger
from domain.services.abstract_api_submission_service import AbstractAPISubmissionService
from schemas.accessions import SampleAccessions
from use_cases.receipt_utils.parse_receipt import parse_receipt


def get_accession_inside_double_quotes_from_log(log_str: str, pattern: str) -> str:
    # ([^"]+) captures one or more characters that are not double quotes into a group
    try:
        return re.search(f'{pattern.strip()} "([^"]+)"', log_str).group(1)
    except AttributeError:
        raise Exception(f'Failed to parse accession from log string {log_str}. Provided {pattern=}')


def parse_sample_accessions_from_response(response: requests.Response, ena_user: str, ena_pass: str, test: bool,
                                          api_submission_service: AbstractAPISubmissionService) -> SampleAccessions:
    """
    Response is in XML format looking sth like this:

    1. metadata has not been yet uploaded:
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-02-23T07:08:53.866Z" submissionFile="submission.xml" success="true">
         <SAMPLE accession="ERS28175515" alias="ENA sample - s_1-e_1" status="PRIVATE">
              <EXT_ID accession="SAMEA130841939" type="biosample"/>
         </SAMPLE>
         <SUBMISSION accession="ERA29152472" alias="SUBMISSION-23-02-2024-07:08:53:080"/>
         <MESSAGES>
              <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
         </MESSAGES>
         <ACTIONS>ADD</ACTIONS>
    </RECEIPT>

    2. Metadata has already been uploaded and sample accession exists:
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-02-23T07:11:17.148Z" submissionFile="submission.xml" success="false">
         <SAMPLE alias="ENA sample - s_1-e_1" status="PRIVATE"/>
         <SUBMISSION alias="SUBMISSION-23-02-2024-07:11:17:115"/>
         <MESSAGES>
              <ERROR>In sample, alias: "ENA sample - s_1-e_1". The object being added already exists in the submission account with accession: "ERS28175515".</ERROR>
              <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
         </MESSAGES>
         <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    """
    # Read XML
    receipt = parse_receipt(response)

    if receipt.success:
        for child in receipt.xml:
            if child.tag == 'SAMPLE':
                submission_accession = child.get('accession')
                ext_id = child.find('EXT_ID')
                biosample_accession = ext_id.get('accession')
                return SampleAccessions(
                    submission_accession=submission_accession,
                    biosample_accession=biosample_accession
                )
    else:
        for child in receipt.xml:
            if child.tag == 'MESSAGES':
                for msg in child:
                    pattern = 'The object being added already exists in the submission account with accession:'
                    if pattern in msg.text:
                        submission_accession = get_accession_inside_double_quotes_from_log(pattern=pattern,
                                                                                           log_str=msg.text)
                        logger.warning(f'Duplicate submission detected: Sample is already submitted. Accession: '
                                       f'{submission_accession}')
                        biosample_accession = api_submission_service.fetch_biosample_accession(
                            sample_accession=submission_accession,
                            ena_user=ena_user,
                            ena_pass=ena_pass,
                            test=test
                        )
                        return SampleAccessions(
                            submission_accession=submission_accession,
                            biosample_accession=biosample_accession
                        )

    raise Exception(f'Could not parse accession from xml: {response.text}')
