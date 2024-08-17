import re
import xml.etree.ElementTree as ET

from schemas.accessions import RawReadsAccession


def parse_raw_reads_accession(log_str: str) -> RawReadsAccession:
    """
    Response is in XML format looking sth like this:

    1. metadata has not been yet uploaded:
    <?xml version="1.0" encoding="UTF-8"?>
    <RECEIPT receiptDate="2017-08-11T15:07:36.746+01:00" submissionFile="sub.xml" success="true">
       <EXPERIMENT accession="ERX2151578" alias="exp_mantis_religiosa" status="PRIVATE"/>
       <RUN accession="ERR2094164" alias="run_mantis_religiosa" status="PRIVATE"/>
       <SUBMISSION accession="ERA986371" alias="mantis_religiosa_submission"/>
       <MESSAGES>
           <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
       </MESSAGES>
       <ACTIONS>ADD</ACTIONS>
       <ACTIONS>ADD</ACTIONS>
    </RECEIPT>

    2. metadata has been already uploaded:
    <?xml version="1.0" encoding="UTF-8"?>
    <?xml-stylesheet type="text/xsl" href="receipt.xsl"?>
    <RECEIPT receiptDate="2024-08-17T17:35:50.808+01:00" submissionFile="submission.xml" success="false">
         <EXPERIMENT alias="ENA Experiment - uvzsr-PT_24_00014-A12-AR_24_00000940" status="PUBLIC"/>
         <SUBMISSION alias="SUBMISSION-17-08-2024-17:35:49:521"/>
         <MESSAGES>
              <ERROR>In experiment, alias: "ENA Experiment - uvzsr-PT_24_00014-A12-AR_24_00000940". The object being added already exists in the submission account with accession: "ERX12811976".</ERROR>
              <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
         </MESSAGES>
         <ACTIONS>ADD</ACTIONS>
    </RECEIPT>
    """
    root = ET.fromstring(log_str)

    try:
        if root.attrib.get('success') == 'true':
            experiment_accession = root.find('EXPERIMENT').attrib['accession']
            return RawReadsAccession(experiment_accession=experiment_accession)
        else:
            experiment_accession = None
            for message in root.find('MESSAGES'):
                if "accession:" in message.text:
                    pattern = r'accession: "([A-Z0-9]+)"'
                    match = re.search(pattern, message.text)
                    if match:
                        experiment_accession = match.group(1)
                        break
            return RawReadsAccession(experiment_accession=experiment_accession)
    except Exception:
        raise Exception(f'Could not parse Experiment / Run accessions from Raw Reads receipt XML: {log_str}')


if __name__ == "__main__":
    xml_data = """<?xml version="1.0" encoding="UTF-8"?>
        <RECEIPT receiptDate="2017-08-11T15:07:36.746+01:00" submissionFile="sub.xml" success="true">
           <EXPERIMENT accession="ERX2151578" alias="exp_mantis_religiosa" status="PRIVATE"/>
           <RUN accession="ERR2094164" alias="run_mantis_religiosa" status="PRIVATE"/>
           <SUBMISSION accession="ERA986371" alias="mantis_religiosa_submission"/>
           <MESSAGES>
               <INFO>This submission is a TEST submission and will be discarded within 24 hours</INFO>
           </MESSAGES>
           <ACTIONS>ADD</ACTIONS>
           <ACTIONS>ADD</ACTIONS>
        </RECEIPT>"""

    parse_raw_reads_accession(log_str=xml_data)
