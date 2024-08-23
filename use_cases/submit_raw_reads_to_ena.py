import xml.etree.ElementTree as ET

from domain.entities.raw_reads_submission import RawReadsSubmission
from schemas.accessions import RawReadsAccession


def update_sample_descriptor_accession(xml_file_path: str, submission_accession: str):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Find the SAMPLE_DESCRIPTOR element and update its accession attribute
    sample_descriptor = root.find('.//SAMPLE_DESCRIPTOR')
    if sample_descriptor is not None:
        sample_descriptor.set('accession', submission_accession)

    # Write the updated XML back to the file
    tree.write(xml_file_path, encoding='UTF-8', xml_declaration=True)


def submit_raw_reads_to_ena(raw_reads_submission: RawReadsSubmission, submission_accession: str) -> RawReadsAccession:
    update_sample_descriptor_accession(raw_reads_submission.experiment_set_xml_path,
                                       submission_accession=submission_accession)

    return raw_reads_submission.register_raw_reads()
