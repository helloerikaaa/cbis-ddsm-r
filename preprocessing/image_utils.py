import pydicom
import pydicom.uid
import numpy as np
from PIL import Image


def dicom_to_array(dicom_dataset: pydicom.Dataset) -> np.ndarray:
    dicom_dataset.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    img = dicom_dataset.pixel_array
    if len(img.shape) > 2:
        img = img[:, :, 0]
    img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
    img = img.astype(np.uint8)
    return img


def array_to_dicom(dcm_img: pydicom.Dataset, img_array:np.ndarray) -> pydicom.Dataset:
    dcm_img.is_little_endian = True
    dcm_img.is_implicit_VR = False
    dcm_img.PixelData = img_array.tobytes()
    dcm_img.Rows, dcm_img.Columns = img_array.shape
    return dcm_img


def png_to_array(img: Image.Image) -> np.ndarray:
    img_array = np.array(img)
    if len(img_array.shape) > 2:
        img_array = img_array[:, :, 0]
    return img_array


def array_to_png(img_array: np.ndarray) -> Image.Image:
    img_array = (
        (img_array - np.min(img_array)) / (np.max(img_array) - np.min(img_array)) * 255
    )
    img_array = img_array.astype(np.uint8)
    img = Image.fromarray(img_array)
    return img
