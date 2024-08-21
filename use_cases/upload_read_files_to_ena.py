from domain.entities.ftp_read_files_upload import FTPReadFilesUpload


def upload_read_files_to_ena(ftp_read_files_upload: FTPReadFilesUpload):
    ftp_read_files_upload.upload_read_files()
