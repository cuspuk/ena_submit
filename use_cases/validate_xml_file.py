from lxml import etree

from core.loguru import logger


def validate_xml_file(xml_file_path: str, xsd_schema_path: str) -> None:
    try:
        xsd_schema = etree.XMLSchema(file=xsd_schema_path)
    except (etree.XMLSchemaParseError, OSError) as e:
        raise ValueError(f"Error loading XSD schema from '{xsd_schema_path}': {e}")

    try:
        with open(xml_file_path, 'rb') as xml_file:
            xml_doc = etree.parse(xml_file)
    except OSError as e:
        raise FileNotFoundError(f"XML file '{xml_file_path}' not found: {e}")
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Error parsing XML file '{xml_file_path}': {e}")

    is_valid = xsd_schema.validate(xml_doc)

    if not is_valid:
        errors = '\n'.join([str(error) for error in xsd_schema.error_log])
        raise ValueError(f"XML file '{xml_file_path}' is not valid according to XSD schema '{xsd_schema_path}'."
                     f"\nErrors:\n{errors}")
