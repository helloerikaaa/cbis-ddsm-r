import os
import cv2
import pydicom
import numpy as np
from loguru import logger
from consts.consts import ImageFormats
from image_utils import dicom_to_array, array_to_png



class ImageProcessor:
    def process(
        self,
        handler,
        data_path: str,
        processed_img_path: str,
        dcm_img: pydicom.Dataset,
        blur_kernel: int,
        thresh: int,
        thresh_max_value: int,
        obj_kernel: int,
        obj_lab_value: int,
        fill_holes: bool,
        remove_pect: bool,
    ) -> None:
        """
        Procesa una imagen DICOM y la prepara para su posterior análisis.

        Parámetros:
        dcm_img (pydicom.dataset.FileDataset): Archivo DICOM que se va a procesar.

        Descripción:
        Esta función lee la imagen DICOM, la recorta para eliminar bordes innecesarios, la normaliza, la binariza,
        edita la máscara para eliminar ruido, encuentra los blobs más grandes y aplica la máscara a la imagen original.

        Devuelve:
        None
        """
        dir_path = os.path.dirname(processed_img_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        img = dicom_to_array(dcm_img)
        img_blurred: np.ndarray = self._median_blur(img, blur_kernel)
        img_bin: np.ndarray = self._global_threshold(
            img_blurred, thresh, thresh_max_value
        )
        largest_obj: np.ndarray = self._select_largest_obj(
            img_bin, img_blurred, obj_lab_value, obj_kernel, fill_holes, remove_pect
        )

        processed_img = array_to_png(largest_obj)
        logger.info(f"Processed Image: {processed_img}")
        handler.save_image(
            data_path, processed_img_path, processed_img, str(ImageFormats.PNG)
        )

    def _median_blur(self, img: np.ndarray, kernel: int):
        return cv2.medianBlur(img, kernel)

    def _global_threshold(self, img: np.ndarray, thresh: int, max_val: int):
        _, img_binary = cv2.threshold(
            img, thresh, maxval=max_val, type=cv2.THRESH_BINARY
        )
        return img_binary

    def _select_largest_obj(
        self,
        img_bin: np.ndarray,
        img: np.ndarray,
        lab_val: int,
        kernel: int,
        fill_holes: bool,
        remove_pect: bool,
    ):
        n_labels, img_labeled, lab_stats, _ = cv2.connectedComponentsWithStats(
            img_bin, connectivity=8, ltype=cv2.CV_32S
        )
        largest_obj_lab = np.argmax(lab_stats[1:, 4]) + 1

        largest_mask = np.zeros(img_bin.shape, dtype=np.uint8)
        largest_mask[img_labeled == largest_obj_lab] = lab_val
        kernel_ = np.ones((kernel, kernel), dtype=np.uint8)
        largest_mask = cv2.morphologyEx(largest_mask, cv2.MORPH_OPEN, kernel_)
        largest_mask = cv2.bitwise_and(img, largest_mask)

        if fill_holes:
            bkg_locs = np.where(img_labeled == 0)
            bkg_seed = (bkg_locs[0][0], bkg_locs[1][0])
            img_floodfill = largest_mask.copy()
            h_, w_ = largest_mask.shape
            mask_ = np.zeros((h_ + 2, w_ + 2), dtype=np.uint8)
            cv2.floodFill(img_floodfill, mask_, seedPoint=bkg_seed, newVal=lab_val)
            holes_mask = cv2.bitwise_not(img_floodfill)
            largest_mask = largest_mask + holes_mask

        return largest_mask
