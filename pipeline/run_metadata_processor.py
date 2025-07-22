from consts.paths import DownloadArtifacts
from dataset.processor import CBISDDSMMetadataProcessor


def main():
    csv_files = [
        DownloadArtifacts.CALC_TRAIN_FILE_PATH,
        DownloadArtifacts.CALC_TEST_FILE_PATH,
        DownloadArtifacts.MASS_TRAIN_FILE_PATH,
        DownloadArtifacts.MASS_TEST_FILE_PATH
    ]
    merger = CBISDDSMMetadataProcessor(csv_files)
    merger.merge_and_process()

if __name__ == "__main__":
    main()
