import os
import json
import requests
import zipfile
from io import BytesIO
from tqdm import tqdm
from loguru import logger
from consts.consts import DatasetMetadata, DownloadUrls, ImageFormats, SuccessLogMessages, ErrorLogMessages


class CBISDDSMDownloader:
    def __init__(self, manifest_path: str, output_dir: str, skip_existing: bool = True):
        self.manifest_path = manifest_path
        self.output_dir = output_dir
        self.skip_existing = skip_existing
        os.makedirs(self.output_dir, exist_ok=True)
        self.series_uids = self._parse_manifest()

    def _parse_manifest(self):
        series_uids = []
        with open(self.manifest_path, "r") as f:
            lines = f.readlines()
        start = False
        for line in lines:
            if not start:
                if line.startswith(DatasetMetadata.LIST_SERIES):
                    start = True
            else:
                uid = line.strip()
                if uid:
                    series_uids.append(uid)
        if not series_uids:
            raise ValueError(ErrorLogMessages.NO_SERIES_UID_MSG)
        return series_uids

    def _get_metadata(self, uid: str):
        response = requests.get(DownloadUrls.BASE_METADATA_URL.format(uid))
        response.raise_for_status()
        return json.loads(response.content.decode("utf-8"))[0]

    def _already_downloaded(self, path: str, expected_num: int) -> bool:
        if not os.path.exists(path):
            return False
        files = os.listdir(path)
        dcm_count = len([f for f in files if f.endswith(ImageFormats.DICOM)])
        return dcm_count >= expected_num

    def _download_series(self, uid: str):
        try:
            metadata = self._get_metadata(uid)
            subject = metadata[DatasetMetadata.SUBJECT_ID]
            study_uid = metadata[DatasetMetadata.STUDY_UID]
            series_uid = metadata[DatasetMetadata.SERIES_UID]
            num_images = int(metadata[DatasetMetadata.NUM_IMGS])

            save_path = os.path.join(self.output_dir, subject, study_uid, series_uid)
            if self.skip_existing and self._already_downloaded(save_path, num_images):
                logger.info(SuccessLogMessages.ALREADY_DOWNLOADED_MSG)
                return  # already downloaded

            os.makedirs(save_path, exist_ok=True)
            response = requests.get(DownloadUrls.BASE_IMAGE_URL.format(uid))
            response.raise_for_status()

            with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(save_path)

        except Exception as e:
            logger.error(f"{ErrorLogMessages.ERROR_DOWNLOADING_MSG} {uid}: {e}")

    def run(self):
        logger.info(f"{SuccessLogMessages.DOWNLOAD_START_MSG} : {len(self.series_uids)}")
        for uid in tqdm(self.series_uids, desc=SuccessLogMessages.DOWNLOAD_SERIES_MSG, unit=SuccessLogMessages.DOWNLOAD_UNIT_MSG):
            self._download_series(uid)
        logger.info(SuccessLogMessages.COMPLETE_DOWNLOAD_MSG)
