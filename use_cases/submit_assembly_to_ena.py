import json

from domain.entities.assembly_submission import AssemblySubmission


def update_sample_descriptor_accession(manifest_json_path: str, submission_accession: str):
    with open(manifest_json_path, 'r') as file:
        data = json.load(file)

    data['sample'] = submission_accession

    with open(manifest_json_path, 'w') as file:
        json.dump(data, file, indent=4)


def submit_assembly_to_ena(assembly_submission: AssemblySubmission, submission_accession: str):
    update_sample_descriptor_accession(
        manifest_json_path=assembly_submission.manifest_json_path,
        submission_accession=submission_accession
    )
    assembly_submission.submit_assembly()

