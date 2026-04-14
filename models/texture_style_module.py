import os
from datetime import datetime

import cv2


def run_texture_style(input_path: str, output_dir: str) -> dict:
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError("无法读取输入图片")

    # 教学简化版：使用 OpenCV 风格化滤镜生成纹理化效果
    try:
        stylized = cv2.stylization(image, sigma_s=80, sigma_r=0.35)
    except Exception:
        stylized = cv2.applyColorMap(image, cv2.COLORMAP_OCEAN)

    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"texture_style_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    output_path = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_path, stylized)

    return {"output_path": output_path, "result_text": "已完成纹理风格化处理。"}
