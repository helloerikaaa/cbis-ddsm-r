import os
import pandas as pd
from tqdm import tqdm
from typing import List
from loguru import logger
from consts.consts import FileNames, ImageFormats, FeatureNames, DatasetMetadata, SuccessLogMessages


class CBISDDSMProcessor:
    def __init__(self, download_dir: str, metadata_csvs: List[str], output_csv: str):
        """
        Args:
            download_dir (str): Path to the CBIS_DDSM_RAW directory.
            metadata_csvs (List[str]): List of CBIS-DDSM metadata CSVs to merge.
            output_csv (str): Output path to the metadata CSV.
        """
        self.download_dir = download_dir
        self.metadata_csvs = metadata_csvs
        self.output_csv = output_csv

    def _load_metadata(self) -> pd.DataFrame:
        dataframes = []
        for csv_file in self.metadata_csvs:
            df = pd.read_csv(csv_file)
            dataframes.append(df)
        return pd.concat(dataframes, ignore_index=True)

    def _resolve_dicom_path(self, image_path: str) -> str:
        """
        Reconstruct the path to the raw DICOM file from the image path column in the CSVs.
        """
        parts = os.path.normpath(image_path).split(os.sep)
        patient_id = parts[0]
        study_id = parts[1]
        series_id = parts[2]
        file_name = FileNames.DICOM_IMG_FILE  # Each series usually contains one image per lesion
        full_path = os.path.join(self.download_dir, patient_id, study_id, series_id, file_name)
        return full_path if os.path.exists(full_path) else None

    def _resolve_mask_path(self, mask_path: str) -> str:
        """
        Convert mask path to normalized format (PNG or to be generated later).
        """
        return os.path.splitext(mask_path)[0] + ImageFormats.PNG

    def process(self):
        df = self._load_metadata()
        output_rows = []

        for _, row in tqdm(df.iterrows(), total=len(df), desc=SuccessLogMessages.PROCESSING_DATASET_MSG):
            image_path = self._resolve_dicom_path(row[DatasetMetadata.IMG_FILE_PATH])
            mask_path = self._resolve_mask_path(row[DatasetMetadata.ROI_FILE_PATH])
            cropped_path = self._resolve_mask_path(row[DatasetMetadata.CROPPED_FILE_PATH])

            if image_path is None:
                continue  # Skip missing DICOMs

            entry = {
                FeatureNames.PATIENT_ID: row[FeatureNames.PATIENT_ID],
                FeatureNames.BREAST_DENSITY: row[FeatureNames.BREAST_DENSITY],
                FeatureNames.LATERALITY: row[DatasetMetadata.BREAST_LATERALITY],
                FeatureNames.VIEW: row[DatasetMetadata.IMAGE_VIEW],
                FeatureNames.ABNORMALITY: row[DatasetMetadata.ABNORMALITY_ID],
                FeatureNames.ABNORMALITY_TYPE: row[DatasetMetadata.ABNORMALITY_TYPE],
                FeatureNames.MASS_SHAPE: row[DatasetMetadata.MASS_SHAPE],
                FeatureNames.MASS_MARGINS: row[DatasetMetadata.MASS_MARGINS],
                FeatureNames.ASSESSMENT: row[FeatureNames.ASSESSMENT],
                FeatureNames.PATHOLOGY: row[FeatureNames.PATHOLOGY],
                FeatureNames.SUBTLETY: row[FeatureNames.SUBTLETY],
                FeatureNames.DICOM_PATH: image_path,
                FeatureNames.MASK_PATH: mask_path,
                FeatureNames.CROPPED_IMAGE_PATH: cropped_path,
            }

            output_rows.append(entry)

        out_df = pd.DataFrame(output_rows)
        out_df.to_csv(self.output_csv, index=False)
        logger.info(f"{SuccessLogMessages.METADATA_SAVED_MSG}: {self.output_csv}")
