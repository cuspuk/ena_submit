import requests
from lxml import etree
from pydantic import BaseModel, ConfigDict


class Receipt(BaseModel):
    xml: etree._Element
    success: bool

    model_config = ConfigDict(arbitrary_types_allowed=True)


def parse_receipt(response: requests.Response) -> Receipt:
    root = etree.fromstring(response.text.encode())
    return Receipt(xml=root, success=root.get('success').lower() == 'true')