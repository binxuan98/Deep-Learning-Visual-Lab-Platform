import os
from datetime import datetime

import cv2


def run_super_resolution(input_path: str, output_dir: str) -> dict:
    # 教学简化版：双三次插值 + 锐化，模拟超分辨率效果
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError("无法读取输入图片")

    height, width = image.shape[:2]
    upscaled = cv2.resize(image, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)
    kernel = cv2.getGaussianKernel(5, 1)
    blur = cv2.filter2D(upscaled, -1, kernel @ kernel.T)
    sharpened = cv2.addWeighted(upscaled, 1.5, blur, -0.5, 0)

    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"super_resolution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    output_path = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_path, sharpened)

    return {"output_path": output_path, "result_text": "已完成超分辨率增强（演示版）。"}
