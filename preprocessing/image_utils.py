import pydicom
import pydicom.uid
import numpy as np
from loguru import logger
from PIL import Image
from pydicom.dataset import FileDataset
from pydicom.uid import ExplicitVRLittleEndian


def dicom_to_array(dicom_dataset: pydicom.Dataset) -> np.ndarray:
    dicom_dataset.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    img = dicom_dataset.pixel_array
    if len(img.shape) > 2:
        img = img[:, :, 0]
    img = (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
    img = img.astype(np.uint8)
    return img


def array_to_dicom(original_dcm: pydicom.Dataset, img: np.ndarray) -> pydicom.Dataset:
    # Convertir a uint16 si no lo es
    if img.dtype != np.uint16:
        img = img.astype(np.uint16)

    # Crear nuevo dataset
    file_meta = original_dcm.file_meta
    new_dcm = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Copiar elementos excepto PixelData
    for elem in original_dcm:
        if elem.tag == (0x7FE0, 0x0010):  # PixelData
            continue
        try:
            new_dcm.add(elem)
        except:
            pass

    # Ajustar los parámetros de la imagen
    new_dcm.Rows, new_dcm.Columns = img.shape
    new_dcm.SamplesPerPixel = 1
    new_dcm.PhotometricInterpretation = "MONOCHROME2"
    new_dcm.BitsAllocated = 16
    new_dcm.BitsStored = 16
    new_dcm.HighBit = 15
    new_dcm.PixelRepresentation = 0
    if 'NumberOfFrames' in new_dcm:
        del new_dcm.NumberOfFrames
    if 'PlanarConfiguration' in new_dcm:
        del new_dcm.PlanarConfiguration

    # Insertar pixel data
    new_dcm.PixelData = img.tobytes()

    # Establecer sintaxis
    new_dcm.is_little_endian = True
    new_dcm.is_implicit_VR = False
    new_dcm.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    return new_dcm


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
