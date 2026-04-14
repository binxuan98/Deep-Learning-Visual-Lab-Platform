import os
from datetime import datetime

import cv2
import numpy as np


def _motion_to_label(motion_score: float) -> str:
    if motion_score < 2.0:
        return "静止/低动作"
    if motion_score < 6.0:
        return "轻度动作"
    return "高动作强度"


def run_action_recognition(input_path: str, output_dir: str) -> dict:
    # 教学简化版：计算连续帧差分强度，映射动作类别
    capture = cv2.VideoCapture(input_path)
    if not capture.isOpened():
        raise ValueError("无法读取输入视频")

    fps = capture.get(cv2.CAP_PROP_FPS) or 25
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    os.makedirs(output_dir, exist_ok=True)
    output_filename = f"action_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    output_path = os.path.join(output_dir, output_filename)
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    previous_gray = None
    motion_values = []
    while True:
        success, frame = capture.read()
        if not success:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if previous_gray is not None:
            diff = cv2.absdiff(gray, previous_gray)
            motion = float(np.mean(diff))
            motion_values.append(motion)
        previous_gray = gray
        writer.write(frame)

    capture.release()
    writer.release()

    avg_motion = float(np.mean(motion_values)) if motion_values else 0.0
    label = _motion_to_label(avg_motion)
    return {
        "output_path": output_path,
        "result_text": f"动作识别结果：{label}（平均运动分数 {avg_motion:.2f}）",
    }
