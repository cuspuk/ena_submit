import os
import pathlib

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Submission credentials
    ROOT_DIR_PATH: pathlib.Path = pathlib.Path().resolve()
    XSD_SCHEMAS_PATH: pathlib.Path = os.path.join(ROOT_DIR_PATH, 'schemas', 'xsd_schemas')

    ENA_HOST: str = 'webin2.ebi.ac.uk'

    LOGGING_FILE: str = os.path.join('logs', 'logs.txt')


settings = Settings()
