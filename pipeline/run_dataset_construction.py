import pandas as pd
from consts.consts import FeatureNames
from consts.paths import CBISDDSMPaths, CBISDDSMRPaths

def main():
    metadata = pd.read_csv(CBISDDSMPaths.CBIS_DDSM_DATASET_CSV_PATH)
    metadata = metadata.drop_duplicates(subset=FeatureNames.IMG_FILE_PATH)
    radiomics_data = pd.read_csv(CBISDDSMRPaths.CBIS_DDSM_R_RADIOMICS_FEATS_PATH)
    radiomics_data = radiomics_data.drop_duplicates(subset=FeatureNames.IMG_FILE_PATH)
    full_dataset = pd.merge(metadata, radiomics_data, how='inner')
    full_dataset = full_dataset.loc[:, ~full_dataset.columns.str.contains('^Unnamed')]
    full_dataset.to_csv(CBISDDSMRPaths.CBIS_DDSM_R_DATASET_PATH)

if __name__ == "__main__":
    main()
