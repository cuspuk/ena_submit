import os
import shutil
from typing import List

from pydantic import BaseModel, field_validator

from schemas.read_file import File


class SubmitConfig(BaseModel):
    ena_username: str
    ena_password: str
    webin_cli_path: str
    results_dir: str
    test: bool
    sample_set_xml_path: str
    submission_xml_path: str
    experiment_set_xml_path: str
    run_set_xml_path: str
    manifest_json_path: str
    reads: List[File]
    antibiograms: List[File] | None = None

    @field_validator('webin_cli_path', 'sample_set_xml_path', 'submission_xml_path',
                     'experiment_set_xml_path', 'run_set_xml_path', 'manifest_json_path', mode='before')
    def check_file_exists(cls, v):
        if not os.path.isfile(v):
            raise ValueError(f'The file "{v}" does not exist.')
        return v

    @field_validator('results_dir', mode='before')
    def check_directory_exists(cls, v):
        if not os.path.isdir(v):
            raise ValueError(f'The directory "{v}" does not exist.')
        return v

    def model_post_init(self, __context):
        upload_files_dir = os.path.join(self.results_dir, 'upload_files')
        os.makedirs(upload_files_dir, exist_ok=True)

        shutil.copy(self.sample_set_xml_path, os.path.join(upload_files_dir, 'sample_set.xml'))
        self.sample_set_xml_path = os.path.join(upload_files_dir, 'sample_set.xml')

        shutil.copy(self.experiment_set_xml_path, os.path.join(upload_files_dir, 'experiment_set.xml'))
        self.experiment_set_xml_path = os.path.join(upload_files_dir, 'experiment_set.xml')

        shutil.copy(self.run_set_xml_path, os.path.join(upload_files_dir, 'run_set.xml'))
        self.run_set_xml_path = os.path.join(upload_files_dir, 'run_set.xml')

        shutil.copy(self.submission_xml_path, os.path.join(upload_files_dir, 'submission.xml'))
        self.submission_xml_path = os.path.join(upload_files_dir, 'submission.xml')

        shutil.copy(self.manifest_json_path, os.path.join(upload_files_dir, 'manifest.json'))
        self.manifest_json_path = os.path.join(upload_files_dir, 'manifest.json')
