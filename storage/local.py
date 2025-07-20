import os
import pydicom
import numpy as np
import pandas as pd
from PIL import Image
from loguru import logger
from preprocessing.image_utils import array_to_png, array_to_dicom, png_to_array


class LocalHandler:

    def read_csv(self, org_path: str, file_name: str) -> pd.DataFrame:
        """
        Read a CSV file from local drive

        Args:
            org_path (str): Path to the folder of the CSV file
            file_name (str): Name of the CSV file to open

        Returns:
            pd.DataFrame: The pandas DataFrame containing the CSV data
        """
        try:
            file_path = os.path.join(org_path, file_name)
            csv_df = pd.read_csv(file_path)
            logger.info(f"File {file_name} has been retrieved from {org_path} of the local drive")
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
            csv_file (pd.DataFrame): CSV object to save
            dst_path (str): Path to the destination folder
            file_name (str): Name of the CSV file to save
        """
        try:
            file_path = os.path.join(dst_path, file_name)
            csv_file.to_csv(file_path)
            logger.info(f"File {file_name} has been saved")
        except Exception as err:
            logger.error(f"Error ocurred: {err}")
            raise err

    def read_dicom(self, org_path: str, file_name:str) -> pydicom.Dataset:
        """
        Read a DICOM dataset from a local drive

        Args:
            org_path (str): Path to the folder of the DICOM file
            file_name (str): Name of the DICOM file to open

        Returns:
            np.ndarray: The DICOM dataset converted to array
        """
        try:
            file_path = os.path.join(org_path, file_name)
            dcm_img = pydicom.dcmread(file_path)
            logger.info(f"File {file_name} has been retrieved from {org_path} of the local drive")
        except FileNotFoundError as fne_err:
            logger.error("File does not exist")
            raise fne_err
        except Exception as err:
            logger.error(f"Error ocurred: {err}")
            raise err
        return dcm_img

    def save_dicom(self, dcm_img: pydicom.Dataset, img: np.ndarray, dst_path:str, file_name:str) -> None:
        """
        Save a DICOM dataset to local drive

        Args:
            dcm_img (np.ndarray): Array of the DICOM dataset to save
            dst_path (str): Path to the destination folder
            file_name (str): Name of the DICOM file to save
        """
        try:
            file_path = os.path.join(dst_path, file_name)
            dcm_img: pydicom.Dataset = array_to_dicom(dcm_img, img)
            dcm_img.save_as(file_path)
            logger.info(f"File {file_name} has been saved to {dst_path}")
        except Exception as err:
            logger.error(f"Error ocurred: {err}")
            raise err


    def read_image(self, org_path: str, file_name:str) -> np.ndarray:
        """
        Read a PNG image from a local drive

        Args:
            org_path (str): Path to the folder of the PNG file
            file_name (str): Name of the PNG file to open

        Returns:
            np.ndarray: The PNG image converted to array
        """
        try:
            file_path = os.path.join(org_path, file_name)
            img = Image.open(file_path)
            img = png_to_array(img)
            logger.info(f"File {file_name} has been retrieved from {org_path} of the local drive")
        except FileNotFoundError as fne_err:
            logger.error("File does not exist")
            raise fne_err
        except Exception as err:
            logger.error(f"Error ocurred: {err}")
            raise err
        return img

    def save_image(self, dst_path: str, file_path: str, img: np.ndarray, format: str) -> None:
        """
        Save a PNG file to local drive

        Args:
            dst_path (str): Path to the destination folder
            file_path (str): Name of the image file to save
            img (np.ndarray): Array of the image to save
            format (str): Image format
        """
        file_path = file_path.replace(".dcm", format)
        try:
            path = os.path.join(dst_path, file_path)
            dir_path = os.path.dirname(path)
            os.makedirs(dir_path, exist_ok=True)
            image: Image.Image = array_to_png(img)
            image.save(path)
            logger.info(f"File {file_path} has been saved to {dst_path}")
        except Exception as err:
            logger.error(f"Error occurred: {err}")
            raise err
