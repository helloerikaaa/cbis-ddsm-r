import enum


class EnumConstant(str, enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    def __str__(self):
        return self.value


class DirNames(EnumConstant):
    MANIFEST = enum.auto()
    METADATA = enum.auto()
    DATA = enum.auto()


class DownloadFiles(EnumConstant):
    MANIFEST_FILE = "CBIS-DDSM-All.tcia"
    CALC_TRAIN_FILE = "calc_case_description_train_set.csv"
    CALC_TEST_FILE = "calc_case_description_test_set.csv"
    MASS_TRAIN_FILE = "mass_case_description_train_set.csv"
    MASS_TEST_FILE = "mass_case_description_test_set.csv"


class LogMessages(EnumConstant):
    DOWNLOAD_DATASET = "Downloading CBIS-DDSM dataset..."
