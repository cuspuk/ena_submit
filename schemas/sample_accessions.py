from pydantic import BaseModel


class SampleAccessions(BaseModel):
    submission_accession: str
    biosample_accession: str
