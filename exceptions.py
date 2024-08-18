import requests


class ResponseError(Exception):
    def __init__(self, response: requests.Response):
        super().__init__(f'Failed to submit sample. Response status code: {response.status_code}. '
                         f'Response text: {response.text}')


class WebinCLIFileUploadError(Exception):
    def __init__(self, log_path: str):
        super().__init__(f'Failed to upload file via webin-cli. Please check log at: {log_path}')


class WebinCLIFileValidationError(Exception):
    def __init__(self, log_path: str):
        super().__init__(f'Failed to validate file via webin-cli. Please check log at: {log_path}')
