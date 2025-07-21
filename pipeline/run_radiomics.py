from consts.consts import RadiomicsConfig
from consts.paths import CBISDDMSRPaths, CBISDDMSPaths
from features.radiomics_features import RadiomicsFeatures

def main():
    settings = {
        "label": int(RadiomicsConfig.LABEL),
        "force2D": bool(RadiomicsConfig.FORCE2D),
    }

    rf = RadiomicsFeatures(settings)

    rf.process_dataset(
        CBISDDMSPaths.CBIS_DDMS_RADIOMICS_CSV_PATH,
        CBISDDMSRPaths.CBIS_DDSM_R_RADIOMICS_FEATS_PATH
    )


if __name__ == '__main__':
    main()
