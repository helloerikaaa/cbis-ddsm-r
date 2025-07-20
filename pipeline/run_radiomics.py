from consts.consts import RadiomicsConfig
from consts.paths import RawDataPaths, ProcessedDataPaths
from features.radiomics_features import RadiomicsFeatures

def main():
    settings = {
        "label": int(RadiomicsConfig.LABEL),
        "force2D": bool(RadiomicsConfig.FORCE2D),
    }

    rf = RadiomicsFeatures(settings)

    rf.process_dataset(
        RawDataPaths.RAW_RADIOMICS_CSV_PATH,
        ProcessedDataPaths.PROCESSED_RADIOMICS_FEATS_PATH
    )


if __name__ == '__main__':
    main()
