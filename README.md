# CBIS-DDSM-R: A Reproducible and Radiomics-Ready Mammography Dataset

CBIS-DDSM-R is a curated and reproducible version of the Curated Breast Imaging Subset of DDSM (CBIS-DDSM). This project provides a fully automated pipeline for downloading, processing, and extracting radiomic features from CBIS-DDSM, enabling reproducible experiments in breast cancer imaging research.


# Project Structure
```bash
cbis-ddsm-r/
│
├── consts/                # Project-wide constants and paths
│   ├── const.py
│   └── paths.py
│
├── data/
│   ├── img/               # DICOM images and ROI masks
│   └── csv/               # Final output CSVs with radiomic features
│
├── dataset/               # Dataset construction and metadata processing
│   ├── constructor.py     # Merges radiomic features with CBIS-DDSM metadata
│   ├── downloader.py      # Downloads CBIS-DDSM from TCIA
│   └── processor.py       # Processes and parses CBIS-DDSM metadata
│
├── features/
│   └── radiomics_features.py # Handles radiomic feature extraction using PyRadiomics
│
├── manifest/
│   └── CBIS-DDSM-All.tcia   # Manifest file to download dataset via NBIA Data Retriever
│
├── metadata/             # Original CBIS-DDSM metadata files from TCIA
│   ├── calc_case_description_test_set.csv
│   ├── calc_case_description_train_set.csv
│   ├── mass_case_description_test_set.csv
│   └── mass_case_description_train_set.csv
│
├── pipeline/             # Orchestrates the full processing pipeline
│   ├── run_downloader.py
│   ├── run_metadata_processor.py
│   ├── run_image_processing.py
│   └── run_radiomics.py
│
├── preprocessing/        # Image preprocessing utilities and filters
│   ├── image_processing.py
│   └── image_utils.py
│
├── storage/              # Handles saving of local data
│   └── local.py

```

# What's Included
- Automated download of CBIS-DDSM via manifest
- DICOM image conversion and pectoral muscle removal
- ROI extraction and alignment
- Full PyRadiomics feature extraction pipeline
- Metadata processing and merging with radiomic features

# Requirements
- Python 3.9

# Python Environment
```bash
conda create -n cbis-ddsm-r
conda activate cbis-ddsm-r
conda install -r requirements.txt
```


# Usage
## 1.  Download the dataset
```bash
python pipeline/run_downloader.py
```
## 2. Process the metadata
```bash
python pipeline/run_metadata_processor.py
```
## 3. Preprocess images
```bash
python pipeline/run_image_processing.py
```
## 4. Extract radiomic features using PyRadiomics
```bash
python pipeline/run_radiomics.py
```
