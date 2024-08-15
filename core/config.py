import os
import pathlib

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Submission credentials
    ROOT_DIR_PATH: pathlib.Path = pathlib.Path().resolve()
    XSD_SCHEMAS_PATH: pathlib.Path = os.path.join(ROOT_DIR_PATH, 'schemas', 'xsd_schemas')
    # if you downloaded it locally -> 'java -jar /webin-cli.jar'
    ENA_WEBIN_CLI: str = (
        f'docker run --rm -u 1000:1000 -e PV_DATA_DIR=/pv_data '
        f'-v {os.path.join(ROOT_DIR_PATH, "testing", "pv_data")}:{os.path.join(ROOT_DIR_PATH, "testing", "pv_data")} '
        f'ena_webin_cli')  # run "sh get_webin_cli.sh" (or just the content of the script in cmd line)

    LOGGING_FILE: str = os.path.join('logs', 'logs.txt')

    # SMTP_HOST: str
    # SMTP_PORT: int = 25
    # SMTP_TLS: bool = True


settings = Settings()
