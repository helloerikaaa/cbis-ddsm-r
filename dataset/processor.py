import pandas as pd
from loguru import logger
from consts.paths import CBISDDSMPaths
from consts.consts import FeatureNames, FileNames, DatasetMetadata, SuccessLogMessages, RadiomicsFeatureNames


class CBISDDSMMetadataProcessor:
    def __init__(self, csv_files):
        self.dataframe = None
        self.radiomics_dataframe = None
        self.csv_files = csv_files

    def _update_path(self, path, roi=False):
        if pd.isna(path):
            return path
        parts = path.strip().split('/')
        parts[-1] = FileNames.MASK_IMG_FILE if roi else FileNames.DICOM_IMG_FILE
        return '/'.join(parts)

    def _rename_columns(self, dataframe):
        dataframe = dataframe.rename(columns={
            DatasetMetadata.PATIENT_ID: FeatureNames.PATIENT_ID,
            DatasetMetadata.BREAST_DENSITY: FeatureNames.BREAST_DENSITY,
            DatasetMetadata.BREAST_LATERALITY: FeatureNames.BREAST_LATERALITY,
            DatasetMetadata.IMAGE_VIEW: FeatureNames.IMAGE_VIEW,
            DatasetMetadata.ABNORMALITY_ID: FeatureNames.ABNORMALITY_ID,
            DatasetMetadata.ABNORMALITY_TYPE: FeatureNames.ABNORMALITY_TYPE,
            DatasetMetadata.CALC_TYPE: FeatureNames.CALC_TYPE,
            DatasetMetadata.CALC_DIST: FeatureNames.CALC_DIST,
            DatasetMetadata.MASS_SHAPE: FeatureNames.MASS_SHAPE,
            DatasetMetadata.MASS_MARGINS: FeatureNames.MASS_MARGINS,
            DatasetMetadata.ASSESSMENT: FeatureNames.ASSESSMENT,
            DatasetMetadata.PATHOLOGY: FeatureNames.PATHOLOGY,
            DatasetMetadata.SUBTLETY: FeatureNames.SUBTLETY,
            DatasetMetadata.IMG_FILE_PATH: FeatureNames.IMG_FILE_PATH,
            DatasetMetadata.ROI_FILE_PATH: FeatureNames.ROI_FILE_PATH,
            DatasetMetadata.CROPPED_FILE_PATH: FeatureNames.CROPPED_FILE_PATH,
        })
        return dataframe

    def _create_radiomics_dataset(self, orginial_dataframe):
        radiomics_dataframe = orginial_dataframe[[FeatureNames.IMG_FILE_PATH, FeatureNames.ROI_FILE_PATH]]
        radiomics_dataframe = radiomics_dataframe.rename(columns={
            FeatureNames.IMG_FILE_PATH: RadiomicsFeatureNames.IMAGE,
            FeatureNames.ROI_FILE_PATH: RadiomicsFeatureNames.MASK
        })
        return radiomics_dataframe

    def merge_and_process(self):
        dataframes = []
        for file in self.csv_files:
            dataframe = pd.read_csv(file)
            dataframe = self._rename_columns(dataframe)
            dataframe[FeatureNames.IMG_FILE_PATH] = dataframe[FeatureNames.IMG_FILE_PATH].apply(lambda x: self._update_path(x, roi=False))
            dataframe[FeatureNames.ROI_FILE_PATH] = dataframe[FeatureNames.ROI_FILE_PATH].apply(lambda x: self._update_path(x, roi=True))
            dataframes.append(dataframe)

        features = [
            FeatureNames.PATIENT_ID,
            FeatureNames.BREAST_DENSITY,
            FeatureNames.BREAST_LATERALITY,
            FeatureNames.IMAGE_VIEW,
            FeatureNames.ABNORMALITY_ID,
            FeatureNames.ABNORMALITY_TYPE,
            FeatureNames.CALC_TYPE,
            FeatureNames.CALC_DIST,
            FeatureNames.MASS_SHAPE,
            FeatureNames.MASS_MARGINS,
            FeatureNames.ASSESSMENT,
            FeatureNames.PATHOLOGY,
            FeatureNames.SUBTLETY,
            FeatureNames.IMG_FILE_PATH,
            FeatureNames.ROI_FILE_PATH,
            FeatureNames.CROPPED_FILE_PATH,
        ]

        self.dataframe = pd.concat(dataframes, ignore_index=True)
        self.dataframe = self.dataframe[features]
        self.dataframe.to_csv(CBISDDSMPaths.CBIS_DDSM_DATASET_CSV_PATH, index=False)
        logger.info(f"{SuccessLogMessages.METADATA_SAVED_MSG}: {CBISDDSMPaths.CBIS_DDSM_DATASET_CSV_PATH}")
        self.radiomics_dataframe = self._create_radiomics_dataset(self.dataframe)
        self.radiomics_dataframe.to_csv(CBISDDSMPaths.CBIS_DDSM_RADIOMICS_CSV_PATH, index=False)
        logger.info(f"{SuccessLogMessages.METADATA_SAVED_MSG}: {CBISDDSMPaths.CBIS_DDSM_RADIOMICS_CSV_PATH}")
