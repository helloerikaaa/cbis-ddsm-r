from dataset.processor import CBISDDSMProcessor
from consts.paths import RawDataPaths, DownloadArtifacts


def main():
    csv_files = [
        DownloadArtifacts.CALC_TRAIN_FILE_PATH,
        DownloadArtifacts.CALC_TEST_FILE_PATH,
        DownloadArtifacts.MASS_TRAIN_FILE_PATH,
        DownloadArtifacts.MASS_TEST_FILE_PATH
    ]
    processor = CBISDDSMProcessor(RawDataPaths.RAW_CSV_PATH, csv_files, RawDataPaths.RAW_DATASET_CSV_PATH)
    processor.process()

if __name__ == "__main__":
    main()
