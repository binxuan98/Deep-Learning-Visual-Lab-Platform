from models.action_recognition_module import run_action_recognition
from models.mnist_module import run_mnist_classification
from models.segmentation_module import run_segmentation
from models.super_resolution_module import run_super_resolution
from models.texture_style_module import run_texture_style
from models.yolo_module import run_yolo_detection


ALGORITHM_META = [
    {
        "key": "yolo",
        "name": "YOLO 目标检测",
        "type": "image",
        "description": "识别图像中的目标位置和类别，适合目标检测教学。",
        "input": "图片（jpg/png）",
        "output": "带检测框的图片 + 检测结果文本",
        "scenarios": "智能安防、自动驾驶、工业检测",
    },
    {
        "key": "segmentation",
        "name": "U-Net 图像分割",
        "type": "image",
        "description": "对图像中的目标区域进行像素级分割。",
        "input": "图片（jpg/png）",
        "output": "分割掩码图 + 叠加效果图",
        "scenarios": "医学影像、遥感图像、缺陷识别",
    },
    {
        "key": "mnist",
        "name": "CNN 手写数字识别",
        "type": "image",
        "description": "将输入的数字图片分类到 0-9。",
        "input": "手写数字图片",
        "output": "预测类别与置信度",
        "scenarios": "字符识别、OCR 入门教学",
    },
    {
        "key": "super_resolution",
        "name": "SRCNN 图像超分辨率",
        "type": "image",
        "description": "将低分辨率图像重建为更清晰图像。",
        "input": "低清晰度图片",
        "output": "增强后的图片",
        "scenarios": "图像修复、视频增强",
    },
    {
        "key": "action_recognition",
        "name": "视频动作识别",
        "type": "video",
        "description": "对视频片段进行动作类别预测。",
        "input": "短视频（mp4/avi）",
        "output": "动作标签 + 处理后视频",
        "scenarios": "行为分析、课堂演示",
    },
    {
        "key": "texture_style",
        "name": "纹理风格化",
        "type": "image",
        "description": "将图片转换为材质风格化效果。",
        "input": "图片（jpg/png）",
        "output": "风格化结果图",
        "scenarios": "美术设计、游戏贴图演示",
    },
]


RUNNERS = {
    "yolo": run_yolo_detection,
    "segmentation": run_segmentation,
    "mnist": run_mnist_classification,
    "super_resolution": run_super_resolution,
    "action_recognition": run_action_recognition,
    "texture_style": run_texture_style,
}
