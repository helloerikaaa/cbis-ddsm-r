import enum


class EnumConstant(str, enum.Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    def __str__(self):
        return self.value


class DirNames(EnumConstant):
    CBIS_DDMS = ".CBIS-DDSM"
    CBIS_DDMS_R = "CBIS-DDSM-R"
    MANIFEST = enum.auto()
    METADATA = enum.auto()
    DATA = enum.auto()
    IMG = enum.auto()
    CSV = enum.auto()


class FileNames(EnumConstant):
    CBIS_DDSM_METADATA_FILE = "cbis_ddsm_metadata.csv"
    RADIOMICS_DATASET_FILE = "radiomics_dataset.csv"
    RADIOMICS_FEATS_FILE = "radiomics_features.csv"
    DICOM_IMG_FILE = "00000001.dcm"
    MASK_IMG_FILE = "00000002.dcm"


class DatasetMetadata(EnumConstant):
    SUBJECT_ID = "Subject ID"
    STUDY_UID = "Study UID"
    SERIES_UID = "Series UID"
    NUM_IMGS = "Number of Images"
    PATIENT_ID = enum.auto()
    BREAST_DENSITY = "breast density"
    BREAST_LATERALITY = "left or right breast"
    IMAGE_VIEW = "image view"
    ABNORMALITY_ID = "abnormality id"
    ABNORMALITY_TYPE = "abnormality type"
    CALC_TYPE = "calc type"
    CALC_DIST = "calc distribution"
    MASS_SHAPE = "mass shape"
    MASS_MARGINS = "mass margins"
    ASSESSMENT = enum.auto()
    PATHOLOGY = enum.auto()
    SUBTLETY = enum.auto()
    IMG_FILE_PATH = "image file path"
    ROI_FILE_PATH = "ROI mask file path"
    CROPPED_FILE_PATH = "cropped image file path"
    LIST_SERIES = "ListOfSeriesToDownload="


class FeatureNames(EnumConstant):
    PATIENT_ID = enum.auto()
    BREAST_DENSITY = enum.auto()
    BREAST_LATERALITY = enum.auto()
    IMAGE_VIEW = enum.auto()
    ABNORMALITY_ID = enum.auto()
    ABNORMALITY_TYPE = enum.auto()
    CALC_TYPE = enum.auto()
    CALC_DIST = enum.auto()
    MASS_SHAPE = enum.auto()
    MASS_MARGINS = enum.auto()
    ASSESSMENT = enum.auto()
    PATHOLOGY = enum.auto()
    SUBTLETY = enum.auto()
    IMG_FILE_PATH = "image_file_path"
    ROI_FILE_PATH = "ROI_mask_file_path"
    CROPPED_FILE_PATH = "cropped_image_file_path"


class RadiomicsFeatureNames(EnumConstant):
    IMAGE = enum.auto()
    MASK = enum.auto()


class DownloadUrls(EnumConstant):
    BASE_IMAGE_URL = "https://services.cancerimagingarchive.net/nbia-api/services/v1/getImage?SeriesInstanceUID={}"
    BASE_METADATA_URL = "https://services.cancerimagingarchive.net/nbia-api/services/v1/getSeriesMetaData?SeriesInstanceUID={}"


class ImageFormats(EnumConstant):
    DICOM = ".dcm"
    PNG = ".png"


class DownloadFiles(EnumConstant):
    MANIFEST_FILE = "CBIS-DDSM-All.tcia"
    CALC_TRAIN_FILE = "calc_case_description_train_set.csv"
    CALC_TEST_FILE = "calc_case_description_test_set.csv"
    MASS_TRAIN_FILE = "mass_case_description_train_set.csv"
    MASS_TEST_FILE = "mass_case_description_test_set.csv"


class ProcessingLogMessages(EnumConstant):
    PROCESSING_METADATA = "Processing CBIS-DDSM metadata..."

class SuccessLogMessages(EnumConstant):
    DOWNLOAD_DATASET_MSG = "Downloading CBIS-DDSM dataset..."
    DOWNLOAD_START_MSG = "Starting to download"
    DOWNLOAD_SERIES_MSG = "Downloading series"
    COMPLETE_DOWNLOAD_MSG = "Download complete"
    DOWNLOAD_UNIT_MSG = "series"
    ALREADY_DOWNLOADED_MSG = "Already downloading. Skipping..."
    PROCESSING_DATASET_MSG = "Processing metadata"
    METADATA_SAVED_MSG = "Metadata saved to"
    MSG_FULL_MMG_DCM = "Processing full mammograph DICOM images"
    MSG_DICOM_INFO = "Reading DICOM information..."
    PREPROCESS_IMG_MSG = "All images processed successfully."


class ErrorLogMessages(EnumConstant):
    ERROR_DOWNLOADING_MSG = "Error downloading"
    NO_SERIES_UID_MSG = "No SeriesInstanceUIDs found in manifest file"


class WarningLogMessages(EnumConstant):
    SKIPPING_IMG_MSG = "Skipping file"
    NOT_PROCESSED_IMG_MSG = "images not found or failed to process"


class RadiomicsConfig(EnumConstant):
    LABEL = 255
    FORCE2D = True


class ImgProcessingConfig(EnumConstant):
    BLUR_KERNEL = 3
    THRESHOLD = 18
    OBJECT_KERNEL = 15
    LABEL_VALUE = 255
    HALF_HEIGHT_RATIO = 0.5
    HALF_WIDTH_RATIO = 0.5
    CORNER_PERCENTILE = 63
    EROSION_ITERATIONS = 3
    SMOOTH_KERNEL_SIZE = 75
    THRESH_BINARY_MAXVAL = 255
    MORPH_KERNEL_VALUE = 1
