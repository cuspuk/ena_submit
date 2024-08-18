import os
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    ROOT_DIR_PATH: pathlib.Path = pathlib.Path().resolve()
    ENA_WEBIN_CLI: str = (
        f'docker run --rm -u 1000:1000 -e PV_DATA_DIR=/pv_data '
        f'-v {os.path.join(ROOT_DIR_PATH, "testing", "pv_data")}:{os.path.join(ROOT_DIR_PATH, "testing", "pv_data")} '
        f'ena_webin_cli')
    ENA_USER: str = ''
    ENA_PASS: str = ''

    model_config = SettingsConfigDict(env_file='.testing_env', env_file_encoding='utf-8')


test_settings = TestSettings()