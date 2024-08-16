import os

from core.config import settings
from domain.entities.sample_registration import SampleRegistration
from use_cases.register_sample_to_ena import register_sample_to_ena


def test_register_sample_to_ena(mock_api_submission_service):

    sample_set_xml_path = os.path.join(settings.ROOT_DIR_PATH, 'tests/data/sample.xml')
    submission_xml_path = os.path.join(settings.ROOT_DIR_PATH, 'tests/data/submission.xml')
    results_dir = os.path.join(settings.ROOT_DIR_PATH, 'tests/results')

    sample_registration = SampleRegistration(
        sample_set_xml_path=sample_set_xml_path,
        submission_xml_path=submission_xml_path,
        ena_username='test_user',
        ena_password='test_pass',
        results_dir=results_dir,
        test=True,
        api_submission_service=mock_api_submission_service
    )

    sample_accessions = register_sample_to_ena(sample_registration)

    assert sample_accessions.submission_accession == 'ERS28175515'
    assert sample_accessions.biosample_accession == 'SAMEA130841939'
