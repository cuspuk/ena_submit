import os

from core.config import settings
from domain.entities.assembly_submission import AssemblySubmission
from exceptions import WebinCLIFileValidationError
from tests.config import test_settings
from use_cases.submit_assembly_to_ena import submit_assembly_to_ena


def test_submit_assembly_to_ena(mock_webin_cli_submission_service):
    manifest_json_path = os.path.join(settings.ROOT_DIR_PATH, 'tests/data/manifest.json')
    results_dir = os.path.join(settings.ROOT_DIR_PATH, 'tests/results/')

    assembly_submission = AssemblySubmission(
        manifest_json_path=manifest_json_path,
        ena_username=test_settings.ENA_USER,
        ena_password=test_settings.ENA_PASS,
        webin_cli_path=test_settings.WEBIN_CLI_PATH,
        results_dir=results_dir,
        test=True,
        webin_cli_submission_service=mock_webin_cli_submission_service
    )

    try:
        submit_assembly_to_ena(assembly_submission=assembly_submission, submission_accession='ERS30843922')
    except WebinCLIFileValidationError:
        assert False, 'WebinCLIFileValidationError was raised!'
