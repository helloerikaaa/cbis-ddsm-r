import numpy as np
import pandas as pd
from tqdm import tqdm
import SimpleITK as sitk
from loguru import logger
from radiomics import featureextractor
from consts.paths import CBISDDMSPaths
from storage.local import LocalHandler
from consts.consts import RadiomicsFeatureNames
from preprocessing.image_utils import dicom_to_array


class RadiomicsFeatures:
    def __init__(self, settings: dict):
        self.handler = LocalHandler()
        self.settings = settings
        self.feature_extractor = featureextractor.RadiomicsFeatureExtractor(**settings)

    def extract_features(self, image_array: np.ndarray, label_array: np.ndarray) -> dict:
        image = sitk.GetImageFromArray(image_array)
        label = sitk.GetImageFromArray(label_array)
        label.CopyInformation(image)
        result = self.feature_extractor.execute(image, label)

        clean_result = {
            k: v for k, v in result.items()
            if not (k.startswith("diagnostics") or k.startswith("general"))
        }

        return clean_result

    def process_dataset(self, dataset_path: str, output_file: str) -> None:
        dataset = pd.read_csv(dataset_path)
        all_results = []

        for index, row in tqdm(dataset.iterrows(), total=dataset.shape[0]):
            image_id = str(row[RadiomicsFeatureNames.IMAGE])
            mask_id = str(row[RadiomicsFeatureNames.MASK])

            try:
                image_dcm = self.handler.read_dicom(CBISDDMSPaths.CBIS_DDMS_IMG_PATH, image_id)
                label_dcm = self.handler.read_dicom(CBISDDMSPaths.CBIS_DDMS_IMG_PATH, mask_id)

                image_array = dicom_to_array(image_dcm)
                label_array = dicom_to_array(label_dcm)

                result = self.extract_features(image_array, label_array)
                result["image_id"] = image_id

                all_results.append(result)

            except Exception as e:
                logger.error(f"Error processing image {image_id}: {str(e)}")

        results_df = pd.DataFrame(all_results)
        self.handler.save_csv(dataset_path, output_file, results_df)
