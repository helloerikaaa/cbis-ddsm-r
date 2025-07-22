import os
import cv2
import pydicom
import numpy as np
from preprocessing.image_utils import dicom_to_array


class ImageProcessor:
    def process(
        self,
        handler,
        processed_img_path: str,
        laterality: str,
        view: str,
        dcm_img: pydicom.Dataset,
        blur_kernel: int,
        thresh: int,
        thresh_max_value: int,
        obj_lab_value: int,
        obj_kernel: int,
    ) -> None:
        dir_path = os.path.dirname(processed_img_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        img = dicom_to_array(dcm_img)

        img_blurred = self._median_blur(img, blur_kernel)

        img_bin = self._global_threshold(img_blurred, thresh, thresh_max_value)

        largest_obj = self._select_largest_obj(
            img_bin, img_blurred, obj_lab_value, obj_kernel
        )

        if view.upper() == "MLO":
            final_img = self._remove_pectoral_muscle(largest_obj)
        else:
            final_img = largest_obj

        handler.save_dicom(dcm_img, final_img, processed_img_path)

    def _median_blur(self, img: np.ndarray, kernel: int):
        return cv2.medianBlur(img, kernel)

    def _global_threshold(self, img: np.ndarray, thresh: int, max_val: int):
        _, img_binary = cv2.threshold(img, thresh, maxval=max_val, type=cv2.THRESH_BINARY)
        return img_binary

    def _select_largest_obj(
        self,
        img_bin: np.ndarray,
        img: np.ndarray,
        lab_val: int,
        kernel: int,
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

        return largest_mask

    def _remove_pectoral_muscle(self, img: np.ndarray) -> np.ndarray:
        h, w = img.shape
        half_h = int(h * 0.5)
        half_w = int(w * 0.5)

        def triangle_mask(side):
            mask = np.zeros_like(img, dtype=np.uint8)
            if side == "RIGHT":
                cnt = np.array([[w, 0], [w, half_h], [half_w, 0]])
            else:
                cnt = np.array([[0, 0], [0, half_h], [half_w, 0]])
            cv2.drawContours(mask, [cnt], 0, 255, -1)
            return mask

        # Crear máscaras para ambos lados
        mask_L = triangle_mask("LEFT")
        mask_R = triangle_mask("RIGHT")

        # Calcular intensidad promedio en cada esquina
        val_L = np.sum(cv2.bitwise_and(img, img, mask=mask_L)) / np.count_nonzero(mask_L)
        val_R = np.sum(cv2.bitwise_and(img, img, mask=mask_R)) / np.count_nonzero(mask_R)

        # Escoger lado con mayor contenido (más brillante → más músculo)
        chosen_mask = mask_L if val_L > val_R else mask_R

        # Eliminar músculo aplicando la máscara invertida
        img_result = cv2.bitwise_and(img, img, mask=cv2.bitwise_not(chosen_mask))

        return img_result
