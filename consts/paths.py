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


class CBISDDSMPaths:
    CBIS_DDSM_PATH = os.path.join(DATA_PATH, DirNames.CBIS_DDMS)
    CBIS_DDSM_IMG_PATH = os.path.join(CBIS_DDSM_PATH, DirNames.IMG)
    CBIS_DDSM_CSV_PATH = os.path.join(CBIS_DDSM_PATH, DirNames.CSV)
    CBIS_DDSM_DATASET_CSV_PATH = os.path.join(CBIS_DDSM_CSV_PATH, FileNames.CBIS_DDSM_METADATA_FILE)
    CBIS_DDSM_RADIOMICS_CSV_PATH = os.path.join(CBIS_DDSM_CSV_PATH, FileNames.RADIOMICS_DATASET_FILE)


class CBISDDSMRPaths:
    CBIS_DDSM_R_PATH = os.path.join(DATA_PATH, DirNames.CBIS_DDMS_R)
    CBIS_DDSM_R_IMG_PATH = os.path.join(CBIS_DDSM_R_PATH, DirNames.IMG)
    CBIS_DDSM_R_CSV_PATH = os.path.join(CBIS_DDSM_R_PATH, DirNames.CSV)
    CBIS_DDSM_R_RADIOMICS_FEATS_PATH = os.path.join(CBIS_DDSM_R_CSV_PATH, FileNames.RADIOMICS_FEATS_FILE)
