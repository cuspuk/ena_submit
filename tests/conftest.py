import pytest
from requests import Response

from domain.services.abstract_api_submission_service import AbstractAPISubmissionService


class MockAPISubmissionService(AbstractAPISubmissionService):
    def submit_files(self, files: dict[str, str], ena_user: str, ena_pass: str, test: bool) -> Response:
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = b"""<?xml version="1.0" encoding="UTF-8"?>
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
                """
        return mock_response


@pytest.fixture(scope='function')
def mock_api_submission_service():
    return MockAPISubmissionService()
