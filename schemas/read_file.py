import os

from pydantic import BaseModel, field_validator


class ReadFile(BaseModel):
    absolute_filepath: str
    target_filename: str

    @field_validator('absolute_filepath', mode='after')
    def check_file_exists(cls, v):
        if not os.path.isfile(v):
            raise ValueError(f"The file '{v}' does not exist.")
        return v
