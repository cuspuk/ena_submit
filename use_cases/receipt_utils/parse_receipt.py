import requests
from lxml import etree

from schemas.receipt import Receipt


def parse_receipt(response: requests.Response) -> Receipt:
    root = etree.fromstring(response.text.encode())
    return Receipt(xml=root, success=root.get('success').lower() == 'true')
