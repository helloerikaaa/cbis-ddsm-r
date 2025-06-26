from dataset.processor import CBISDDSMProcessor

def main():
    download_dir = "CBIS_DDSM_RAW"
    csv_files = [
        "metadata/mass_case_description_train_set.csv",
        "metadata/calc_case_description_train_set.csv",
    ]
    output_csv = "data/cbis_train_metadata.csv"

    print("🛠️  Processing CBIS-DDSM metadata...")
    processor = CBISDDSMProcessor(download_dir, csv_files, output_csv)
    processor.process()

if __name__ == "__main__":
    main()
