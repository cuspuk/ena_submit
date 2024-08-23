from typing import Optional

from pydantic import BaseModel, Field


class SubmitFiles(BaseModel):
    SUBMISSION: str = Field(description='Path to the submission XML file')
    EXPERIMENT: Optional[str] = Field(None, description='Path to the experiment set XML file')
    RUN: Optional[str] = Field(None, description='Path to the run set XML file')
    SAMPLE: Optional[str] = Field(None, description='Path to the sample set XML file')
