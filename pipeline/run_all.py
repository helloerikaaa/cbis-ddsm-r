from pipeline import run_dataset_construction, run_downloader, run_image_processing, run_metadata_processor, run_radiomics


def main():
    run_downloader.main()
    run_metadata_processor.main()
    run_image_processing.main()
    run_radiomics.main()
    run_dataset_construction.main()
