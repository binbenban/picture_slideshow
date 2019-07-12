import logging


log = logging.getLogger("pycloud")


class RemoteFile:
    def __init__(self, fileid, filename):
        self.fileid = fileid
        self.filename = filename

    def __repr__(self):
        return f"RemoteFile: {self.fileid} - {self.filename}"
