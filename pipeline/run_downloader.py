from dataset.downloader import CBISDDSMDownloader
from consts.paths import DownloadArtifacts, CBISDDSMPaths

def main():
    downloader = CBISDDSMDownloader(
        DownloadArtifacts.MANIFEST_FILE_PATH,
        CBISDDSMPaths.CBIS_DDSM_IMG_PATH
    )
    downloader.run()

if __name__ == "__main__":
    main()
