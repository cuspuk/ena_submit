from domain.entities.raw_reads_submission import RawReadsSubmission
from schemas.accessions import RawReadsAccession


def upload_read_files_to_ena(raw_reads_submission: RawReadsSubmission):
    raw_reads_submission.register_raw_reads()
