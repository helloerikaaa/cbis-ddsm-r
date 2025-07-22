from consts.consts import RadiomicsConfig
from consts.paths import CBISDDSMRPaths, CBISDDSMPaths
from features.radiomics_features import RadiomicsFeatures

def main():
    settings = {
        "label": int(RadiomicsConfig.LABEL),
        "force2D": bool(RadiomicsConfig.FORCE2D),
    }

    rf = RadiomicsFeatures(settings)

    rf.process_dataset(
        CBISDDSMPaths.CBIS_DDSM_RADIOMICS_CSV_PATH,
        CBISDDSMRPaths.CBIS_DDSM_R_RADIOMICS_FEATS_PATH
    )


if __name__ == '__main__':
    main()
