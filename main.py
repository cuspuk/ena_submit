import argparse
import json
from pydantic import BaseModel
from typing import List

from schemas.read_file import File


class Config(BaseModel):
    ena_username: str
    ena_password: str
    results_dir: str
    test: str
    sample_set_xml_path: str
    submission_xml_path: str
    experiment_set_xml_path: str
    run_set_xml_path: str
    manifest_json_path: str
    read_files: List[File]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='This script processes input files and information for ENA submission using a configuration file.'
    )

    parser.add_argument('--config', type=str, required=True, help='Path to the configuration JSON file.')

    args = parser.parse_args()

    return args


def load_config(config_path: str) -> Config:
    with open(config_path, 'r') as f:
        config_data = json.load(f)
        config = Config(**config_data)
    return config


def main():
    args = parse_arguments()
    config = load_config(args.config)

    print("ENA Username:", config.ena_username)
    print("Results Directory:", config.results_dir)
    print("Read Files:")
    for file in config.read_files:
        print(f" - Filepath: {file.absolute_filepath}, Filename: {file.target_filename}, Type: {file.filetype}")


if __name__ == "__main__":
    main()
