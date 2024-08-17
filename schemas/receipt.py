from lxml import etree

from pydantic import BaseModel, ConfigDict


class Receipt(BaseModel):
    xml: etree._Element
    success: bool

    model_config = ConfigDict(arbitrary_types_allowed=True)
