import os
from loguru import logger
from storage.local import LocalHandler
from consts.paths import CBISDDSMPaths, CBISDDSMRPaths
from preprocessing.image_processing import ImageProcessor
from consts.consts import FeatureNames, SuccessLogMessages, ImgProcessingConfig, WarningLogMessages


def main() -> None:
    handler = LocalHandler()
    not_found_paths = []

    logger.info(SuccessLogMessages.MSG_FULL_MMG_DCM)
    logger.info(SuccessLogMessages.MSG_DICOM_INFO)

    full_data = handler.read_csv(CBISDDSMPaths.CBIS_DDSM_DATASET_CSV_PATH)

    for _, row in full_data.iterrows():
        dicom_file = str(row[FeatureNames.IMG_FILE_PATH])
        laterality = str(row[FeatureNames.BREAST_LATERALITY])
        view = str(row[FeatureNames.IMAGE_VIEW])

        original_file = os.path.join(CBISDDSMPaths.CBIS_DDSM_IMG_PATH, dicom_file)
        processed_file = os.path.join(CBISDDSMRPaths.CBIS_DDSM_R_IMG_PATH, dicom_file)

        try:
            dicom_img = handler.read_dicom(original_file)

            ImageProcessor().process(
                handler=handler,
                processed_img_path=processed_file,
                laterality=laterality,
                view=view,
                dcm_img=dicom_img,
                blur_kernel=int(ImgProcessingConfig.BLUR_KERNEL),
                thresh=int(ImgProcessingConfig.THRESHOLD),
                thresh_max_value=int(ImgProcessingConfig.THRESH_BINARY_MAXVAL),
                obj_kernel=int(ImgProcessingConfig.OBJECT_KERNEL),
                obj_lab_value=int(ImgProcessingConfig.LABEL_VALUE),
            )

        except Exception as e:
            logger.warning(f"{WarningLogMessages.SKIPPING_IMG_MSG} {original_file}: {e}")
            not_found_paths.append(original_file)

    if not_found_paths:
        logger.info(f"{len(not_found_paths)} {WarningLogMessages.NOT_PROCESSED_IMG_MSG}")
        for path in not_found_paths:
            logger.info(f" - {path}")
    else:
        logger.success(SuccessLogMessages.PREPROCESS_IMG_MSG)


if __name__ == "__main__":
    main()
