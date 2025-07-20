import os
from consts.consts import DirNames, DownloadFiles, FileNames


PROJECT_PATH = os.path.abspath(os.path.join(__file__, *(os.path.pardir,)*2))
MANIFEST_PATH = os.path.join(PROJECT_PATH, DirNames.MANIFEST)
METADATA_PATH = os.path.join(PROJECT_PATH, DirNames.METADATA)
DATA_PATH = os.path.join(PROJECT_PATH, DirNames.DATA)


class DownloadArtifacts:
    MANIFEST_FILE_PATH = os.path.join(MANIFEST_PATH, DownloadFiles.MANIFEST_FILE)
    CALC_TRAIN_FILE_PATH = os.path.join(METADATA_PATH, DownloadFiles.CALC_TRAIN_FILE)
    CALC_TEST_FILE_PATH = os.path.join(METADATA_PATH, DownloadFiles.CALC_TEST_FILE)
    MASS_TRAIN_FILE_PATH = os.path.join(METADATA_PATH, DownloadFiles.MASS_TRAIN_FILE)
    MASS_TEST_FILE_PATH = os.path.join(METADATA_PATH, DownloadFiles.MASS_TEST_FILE)


class RawDataPaths:
    RAW_PATH = os.path.join(DATA_PATH, DirNames.RAW)
    RAW_IMG_PATH = os.path.join(RAW_PATH, DirNames.DICOM)
    RAW_CSV_PATH = os.path.join(RAW_PATH, DirNames.CSV)
    RAW_DATASET_CSV_PATH = os.path.join(RAW_CSV_PATH, FileNames.RAW_DATASET_FILE)
    RAW_RADIOMICS_CSV_PATH = os.path.join(RAW_CSV_PATH, FileNames.RADIOMICS_RAW_DATASET_FILE)


class ProcessedDataPaths:
    PROCESSED_PATH = os.path.join(DATA_PATH, DirNames.PROCESSED)
    PROCESSED_IMG_PATH = os.path.join(PROCESSED_PATH, DirNames.DICOM)
    PROCESSED_CSV_PATH = os.path.join(PROCESSED_PATH, DirNames.CSV)
    PROCESSED_RADIOMICS_FEATS_PATH = os.path.join(PROCESSED_CSV_PATH, FileNames.PROCESSED_RADIOMICS_FEATS_FILE)
