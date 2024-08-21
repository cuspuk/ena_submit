import os
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Submission credentials
    ROOT_DIR_PATH: pathlib.Path = pathlib.Path().resolve()
    XSD_SCHEMAS_PATH: pathlib.Path = os.path.join(ROOT_DIR_PATH, 'schemas', 'xsd_schemas')

    ENA_HOST: str = 'webin2.ebi.ac.uk'
    ENA_WEBIN_CLI: str

    LOGGING_FILE: str = os.path.join('logs', 'logs.txt')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
