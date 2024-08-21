from pydantic import BaseModel


class File(BaseModel):
    absolute_filepath: str
    target_filename: str
    filetype: str

    # TODO: Check if the file (absolute_filepath) exists
