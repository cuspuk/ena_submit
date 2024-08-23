import os

from core.config import settings
from domain.entities.raw_reads_submission import RawReadsSubmission
from use_cases.submit_raw_reads_to_ena import submit_raw_reads_to_ena


def test_submit_raw_reads_to_ena(mock_api_raw_reads_submission_service):
    experiment_set_xml_path = os.path.join(settings.ROOT_DIR_PATH, 'tests/data/experiment.xml')
    run_set_xml_path = os.path.join(settings.ROOT_DIR_PATH, 'tests/data/run.xml')
    submission_xml_path = os.path.join(settings.ROOT_DIR_PATH, 'tests/data/submission.xml')
    results_dir = os.path.join(settings.ROOT_DIR_PATH, 'tests/results')

    raw_reads_submission = RawReadsSubmission(
        experiment_set_xml_path=experiment_set_xml_path,
        run_set_xml_path=run_set_xml_path,
        submission_xml_path=submission_xml_path,
        ena_username='test_user',
        ena_password='test_pass',
        results_dir=results_dir,
        test=True,
        api_submission_service=mock_api_raw_reads_submission_service
    )

    raw_reads_accession = submit_raw_reads_to_ena(
        raw_reads_submission=raw_reads_submission,
        submission_accession='ERS30843922'
    )

    assert raw_reads_accession.experiment_accession == 'ERX2151578'
