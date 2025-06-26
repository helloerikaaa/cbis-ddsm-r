from dataset.downloader import CBISDDSMDownloader
from consts.paths import DATA_PATH, DownloadArtifacts

def main():

    print("🚀 Starting CBIS-DDSM download...")
    downloader = CBISDDSMDownloader(
        DownloadArtifacts.MANIFEST_FILE_PATH,
        DATA_PATH)
    downloader.run()

if __name__ == "__main__":
    main()
