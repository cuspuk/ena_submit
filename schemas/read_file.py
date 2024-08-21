import os

from pydantic import BaseModel, field_validator


class File(BaseModel):
    absolute_filepath: str
    target_filename: str

    @field_validator('absolute_filepath', mode='before')
    def check_file_exists(cls, v):
        if not os.path.isfile(v):
            raise ValueError(f"The file '{v}' does not exist.")
        return v
