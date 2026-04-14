import os
from datetime import datetime

import cv2


def run_yolo_detection(input_path: str, output_dir: str) -> dict:
    # 教学简化版：通过边缘和轮廓提取模拟目标框输出，便于学生理解检测流程
    image = cv2.imread(input_path)
    if image is None:
        raise ValueError("无法读取输入图片")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 60, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 1200:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        boxes.append((x, y, w, h))
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 220, 0), 2)
        cv2.putText(
            image,
            "object",
            (x, max(0, y - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 220, 0),
            2,
        )

    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"yolo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    output_path = os.path.join(output_dir, output_filename)
    cv2.imwrite(output_path, image)

    if not boxes:
        result_text = "未检测到明显目标，可尝试更清晰或主体更突出的图片。"
    else:
        result_text = f"检测到 {len(boxes)} 个目标区域。"

    return {"output_path": output_path, "result_text": result_text}
