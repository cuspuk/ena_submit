import os
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Submission credentials
    ROOT_DIR_PATH: pathlib.Path = pathlib.Path().resolve()
    XSD_SCHEMAS_PATH: pathlib.Path = os.path.join(ROOT_DIR_PATH, 'schemas', 'xsd_schemas')
    # if you downloaded it locally -> 'java -jar /webin-cli.jar'
    ENA_WEBIN_CLI: str = (
        f'docker run --rm -u 1000:1000 -e PV_DATA_DIR=/pv_data '
        f'-v {os.path.join(ROOT_DIR_PATH, "testing", "pv_data")}:{os.path.join(ROOT_DIR_PATH, "testing", "pv_data")} '
        f'ena_webin_cli')

    LOGGING_FILE: str = os.path.join('logs', 'logs.txt')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
