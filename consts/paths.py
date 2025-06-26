import os
from consts.consts import DirNames, DownloadFiles


PROJECT_PATH = os.path.abspath(os.path.join(__file__, *(os.path.pardir,)*2))
MANIFEST_PATH = os.path.join(PROJECT_PATH, DirNames.MANIFEST)
METADATA_PATH = os.path.join(PROJECT_PATH, DirNames.METADATA)
DATA_PATH = os.path.join(PROJECT_PATH, DirNames.DATA)


class DownloadArtifacts:
    MANIFEST_FILE_PATH = os.path.join(MANIFEST_PATH, DownloadFiles.MANIFEST_FILE)
