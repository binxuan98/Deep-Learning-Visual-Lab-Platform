# 深度学习算法可视化实验平台  
Deep Learning Visual Lab Platform

## 1. 项目总体说明

本项目面向高职院校《人工智能应用开发》《深度学习技术应用》课程，提供一个本地部署、教学友好、可二次开发的深度学习算法实验平台。  
平台支持在浏览器中上传图片或视频，调用不同算法模块进行推理，并显示可视化输出、结果说明、历史记录和系统日志。

项目设计目标：

- 教学友好：结构清晰，便于学生阅读代码
- 可运行：开箱即用，默认本地部署
- 可协作：适配 GitHub 小组开发
- 可扩展：每个算法独立封装，便于二次开发

---

## 2. 适用课程与教学目标

适用课程：

- 《人工智能应用开发》
- 《深度学习技术应用》

教学目标：

1. 理解深度学习任务类型（检测、分割、分类、增强、视频分析、风格化）
2. 掌握 Web + Flask + PyTorch 的完整项目流程
3. 形成团队协作开发能力（分工、分支、PR、测试）
4. 能基于已有平台进行功能扩展与优化

---

## 3. 项目目录结构

```text
deep-learning-visual-lab/
├── backend/                  # Flask 后端
│   ├── app.py
│   ├── config.py
│   ├── db.py
│   ├── services/
│   └── utils/
├── frontend/                 # 前端页面与静态资源
│   ├── login.html
│   ├── pages/
│   └── assets/
├── models/                   # 算法推理模块
├── uploads/                  # 上传文件
│   ├── images/
│   └── videos/
├── outputs/                  # 算法输出结果
├── data/                     # SQLite 数据库与日志
├── docs/                     # 项目文档
├── tests/                    # 自动化测试
├── scripts/                  # 启动与初始化脚本
├── requirements.txt
└── README.md
```

---

## 4. 已实现功能模块

1. 用户登录与退出模块
2. 算法首页展示模块
3. 图像上传与预览模块
4. 视频上传与预览模块
5. 算法选择模块
6. 算法运行结果展示模块
7. 历史测试记录模块
8. 系统日志模块
9. 部署与测试文档模块
10. 算法说明页面模块

---

## 5. 算法模块说明

| 算法 | 路由 | 输入 | 输出 | 教学意义 |
|---|---|---|---|---|
| YOLO 目标检测（演示版） | `/api/run/yolo` | 图片 | 检测框图片 | 目标检测流程与边界框理解 |
| U-Net 分割（演示版） | `/api/run/segmentation` | 图片 | 分割叠加图 + 掩码 | 像素级预测理解 |
| MNIST CNN（演示版） | `/api/run/mnist` | 图片 | 分类标签与置信度 | 分类任务与 softmax 输出 |
| SRCNN 超分辨率（演示版） | `/api/run/super_resolution` | 图片 | 增强图像 | 图像重建与增强 |
| 动作识别（演示版） | `/api/run/action_recognition` | 视频 | 标签 + 输出视频 | 视频时序分析 |
| 纹理风格化（演示版） | `/api/run/texture_style` | 图片 | 风格化图片 | 风格迁移思想入门 |

---

## 6. 快速启动

### 6.1 安装依赖

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### 6.2 初始化数据库

```bash
python scripts/init_db.py
```

### 6.3 启动后端服务

```bash
python scripts/run_backend.py
```

访问地址：

- http://127.0.0.1:5000/

默认账号：

- admin / admin123

---

## 7. 接口清单

- `/api/login`
- `/api/logout`
- `/api/algorithms`
- `/api/upload/image`
- `/api/upload/video`
- `/api/run/yolo`
- `/api/run/segmentation`
- `/api/run/mnist`
- `/api/run/super_resolution`
- `/api/run/action_recognition`
- `/api/run/texture_style`
- `/api/history`
- `/api/logs`
- `/api/algorithm_docs`

详细接口见 [docs/api.md](docs/api.md)

---

## 8. 前端页面清单

1. 登录页：`/login.html`
2. 平台首页：`/pages/home.html`
3. 算法导航页：`/pages/algorithms.html`
4. 图片测试页：`/pages/image_test.html`
5. 视频测试页：`/pages/video_test.html`
6. 历史记录页：`/pages/history.html`
7. 算法说明页：`/pages/docs.html`

---

## 9. 测试

```bash
pytest tests -q
```

---

## 10. 教学协作与分工

完整教学内容见 [docs/teaching_guide.md](docs/teaching_guide.md)，包含：

- 项目简介
- 模块教学意义
- 六岗位任务分工
- GitHub 协作规范
- 提交规范与 PR 要求
- 二次开发清单
- 实施顺序与课堂建议
- 常见问题排查

---

## 11. 说明

- 本项目为教学示例，默认算法采用轻量演示实现，确保在普通教学电脑可运行
- 教师可逐步替换为真实预训练模型，以提升实验深度
