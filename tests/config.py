from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    ENA_USER: str = ''
    ENA_PASS: str = ''
    WEBIN_CLI_PATH: str = ''

    model_config = SettingsConfigDict(env_file='.testing_env', env_file_encoding='utf-8')


test_settings = TestSettings()
