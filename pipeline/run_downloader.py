from dataset.downloader import CBISDDSMDownloader
from consts.paths import DownloadArtifacts, RawDataPaths

def main():
    downloader = CBISDDSMDownloader(
        DownloadArtifacts.MANIFEST_FILE_PATH,
        RawDataPaths.RAW_IMG_PATH
    )
    downloader.run()

if __name__ == "__main__":
    main()
