import os
import pydicom
import numpy as np
import pandas as pd
from PIL import Image
from loguru import logger
from preprocessing.image_utils import array_to_png, array_to_dicom, png_to_array


class LocalHandler:

    def read_csv(self, file_path: str) -> pd.DataFrame:
        """
        Read a CSV file from local drive

        Args:
            file_path (str): Name of the CSV file to open

        Returns:
            pd.DataFrame: The pandas DataFrame containing the CSV data
        """
        try:
            csv_df = pd.read_csv(file_path)
            logger.info(f"File {file_path} has been retrieved from the local drive")
        except FileNotFoundError as fne_err:
            logger.error("File does not exist")
            raise fne_err
        except Exception as err:
            logger.error(f"Error ocurred: {err}")
            raise err

        return csv_df

    def save_csv(self, dst_path: str, file_name: str, csv_file: pd.DataFrame) -> None:
        """
        Save a CSV file to local drive

        Args:
            dst_path (str): Path to the destination folder
            file_name (str): Name of the CSV file to save
            csv_file (pd.DataFrame): CSV object to save
        """
        try:
            file_path = os.path.join(dst_path, file_name)
            csv_file.to_csv(file_path)
            logger.info(f"File {file_name} has been saved")
        except Exception as err:
            logger.error(f"Error ocurred: {err}")
            raise err

    def read_dicom(self, file_path:str) -> pydicom.Dataset:
        """
        Read a DICOM dataset from a local drive

        Args:
            file_path (str): Name of the DICOM file to open

        Returns:
            np.ndarray: The DICOM dataset converted to array
        """
        try:
            dcm_img = pydicom.dcmread(file_path)
            logger.info(f"File {file_path} has been retrieved of the local drive")
        except FileNotFoundError as fne_err:
            logger.error("File does not exist")
            raise fne_err
        except Exception as err:
            logger.error(f"Error ocurred: {err}")
            raise err
        return dcm_img

    def save_dicom(self, dcm_img: pydicom.Dataset, img: np.ndarray, file_path:str) -> None:
        """
        Save a DICOM dataset to local drive

        Args:
            dcm_img (pydicom.Dataset): Array of the DICOM dataset to save
            dst_path (str): Path to the destination folder
            file_name (str): Name of the DICOM file to save
        """
        try:
            dcm_img: pydicom.Dataset = array_to_dicom(dcm_img, img)
            logger.info(f"Original shape: {dcm_img.pixel_array.shape}")
            logger.info(f"Original rows/cols: {dcm_img.Rows, dcm_img.Columns}")
            logger.info(f"SamplesPerPixel: {dcm_img.SamplesPerPixel}")
            logger.info(f"BitsAllocated: {dcm_img.BitsAllocated}")
            dcm_img.save_as(file_path)
            logger.info(f"File {file_path} has been saved")
        except Exception as err:
            logger.error(f"Error ocurred: {err}")
            raise err


    def read_image(self, file_path:str) -> np.ndarray:
        """
        Read a PNG image from a local drive

        Args:
            file_path (str): Name of the PNG file to open

        Returns:
            np.ndarray: The PNG image converted to array
        """
        try:
            img = Image.open(file_path)
            img = png_to_array(img)
            logger.info(f"File {file_path} has been retrieved of the local drive")
        except FileNotFoundError as fne_err:
            logger.error("File does not exist")
            raise fne_err
        except Exception as err:
            logger.error(f"Error ocurred: {err}")
            raise err
        return img

    def save_image(self, file_path: str, img: np.ndarray, format: str) -> None:
        """
        Save a PNG file to local drive

        Args:
            file_path (str): Name of the image file to save
            img (np.ndarray): Array of the image to save
        """
        file_path = file_path.replace(".dcm", format)
        try:
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, exist_ok=True)
            image: Image.Image = array_to_png(img)
            image.save(file_path)
            logger.info(f"File {file_path} has been saved")
        except Exception as err:
            logger.error(f"Error occurred: {err}")
            raise err
