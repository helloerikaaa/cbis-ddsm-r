import os
import pandas as pd
from tqdm import tqdm
from typing import List


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
        file_name = "00000001.dcm"  # Each series usually contains one image per lesion
        full_path = os.path.join(self.download_dir, patient_id, study_id, series_id, file_name)
        return full_path if os.path.exists(full_path) else None

    def _resolve_mask_path(self, mask_path: str) -> str:
        """
        Convert mask path to normalized format (PNG or to be generated later).
        """
        return os.path.splitext(mask_path)[0] + ".png"

    def process(self):
        df = self._load_metadata()
        output_rows = []

        for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing metadata"):
            image_path = self._resolve_dicom_path(row["image file path"])
            mask_path = self._resolve_mask_path(row["ROI mask file path"])
            cropped_path = self._resolve_mask_path(row["cropped image file path"])

            if image_path is None:
                continue  # Skip missing DICOMs

            entry = {
                "patient_id": row["patient_id"],
                "breast_density": row["breast_density"],
                "laterality": row["left or right breast"],
                "view": row["image view"],
                "abnormality_id": row["abnormality id"],
                "abnormality_type": row["abnormality type"],
                "mass_shape": row["mass shape"],
                "mass_margins": row["mass margins"],
                "assessment": row["assessment"],
                "pathology": row["pathology"],
                "subtlety": row["subtlety"],
                "dicom_path": image_path,
                "mask_path": mask_path,
                "cropped_image_path": cropped_path,
            }

            output_rows.append(entry)

        out_df = pd.DataFrame(output_rows)
        out_df.to_csv(self.output_csv, index=False)
        print(f"✅ Metadata CSV saved to: {self.output_csv}")
