import os
import json
import requests
import zipfile
from io import BytesIO

from tqdm import tqdm

BASE_IMAGE_URL = "https://services.cancerimagingarchive.net/nbia-api/services/v1/getImage?SeriesInstanceUID={}"
BASE_METADATA_URL = "https://services.cancerimagingarchive.net/nbia-api/services/v1/getSeriesMetaData?SeriesInstanceUID={}"


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
                if line.startswith("ListOfSeriesToDownload="):
                    start = True
            else:
                uid = line.strip()
                if uid:
                    series_uids.append(uid)
        if not series_uids:
            raise ValueError("No SeriesInstanceUIDs found in manifest file.")
        return series_uids

    def _get_metadata(self, uid: str):
        response = requests.get(BASE_METADATA_URL.format(uid))
        response.raise_for_status()
        return json.loads(response.content.decode("utf-8"))[0]

    def _already_downloaded(self, path: str, expected_num: int) -> bool:
        if not os.path.exists(path):
            return False
        files = os.listdir(path)
        dcm_count = len([f for f in files if f.endswith(".dcm")])
        return dcm_count >= expected_num

    def _download_series(self, uid: str):
        try:
            metadata = self._get_metadata(uid)
            subject = metadata["Subject ID"]
            study_uid = metadata["Study UID"]
            series_uid = metadata["Series UID"]
            num_images = int(metadata["Number of Images"])

            save_path = os.path.join(self.output_dir, subject, study_uid, series_uid)
            if self.skip_existing and self._already_downloaded(save_path, num_images):
                return  # already downloaded

            os.makedirs(save_path, exist_ok=True)
            response = requests.get(BASE_IMAGE_URL.format(uid))
            response.raise_for_status()

            with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(save_path)

        except Exception as e:
            print(f"❌ Error downloading {uid}: {e}")

    def run(self):
        print(f"📥 Starting download of {len(self.series_uids)} series...")
        for uid in tqdm(self.series_uids, desc="Downloading series", unit="series"):
            self._download_series(uid)
        print("✅ Download completed.")
