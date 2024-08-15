import requests


class ResponseError(Exception):
    def __init__(self, response: requests.Response):
        super().__init__(f'Failed to submit sample. Response status code: {response.status_code}. '
                         f'Response text: {response.text}')
