from domain.entities.raw_reads_submission import RawReadsSubmission
from schemas.accessions import RawReadsAccession


def submit_raw_reads_to_ena(raw_reads_submission: RawReadsSubmission) -> RawReadsAccession:
    return raw_reads_submission.register_raw_reads()
