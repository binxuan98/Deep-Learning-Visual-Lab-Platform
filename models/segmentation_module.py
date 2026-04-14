import os
from datetime import datetime

import cv2
import numpy as np


def run_segmentation(input_path: str, output_dir: str) -> dict:
    # 教学简化版：基于阈值 + 形态学操作生成分割掩码
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError("无法读取输入图片")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    overlay = image.copy()
    overlay[mask > 0] = (0, 0, 255)
    blended = cv2.addWeighted(image, 0.7, overlay, 0.3, 0)

    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"segmentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    output_path = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_path, blended)

    mask_filename = f"segmentation_mask_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    mask_path = os.path.join(output_dir, mask_filename)
    cv2.imwrite(mask_path, mask)

    return {
        "output_path": output_path,
        "result_text": "已完成图像分割并生成掩码。",
        "extra_output_path": mask_path,
    }
