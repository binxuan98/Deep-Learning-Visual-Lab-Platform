# 部署说明（Windows / macOS / Linux）

## 1. 环境准备

- Python 3.10 或 3.11
- pip
- 推荐虚拟环境工具：venv

## 2. 获取项目

```bash
git clone <你的仓库地址>
cd deep-learning-visual-lab
```

## 3. 安装依赖

```bash
python -m venv .venv
# Windows:
# .venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
```

## 4. 初始化数据库

```bash
python scripts/init_db.py
```

## 5. 启动项目

```bash
python scripts/run_backend.py
```

启动后访问：

- http://127.0.0.1:5000/

默认账号：

- 用户名：admin
- 密码：admin123

## 6. 目录挂载说明

- 上传图片：uploads/images/
- 上传视频：uploads/videos/
- 推理结果：outputs/
- 数据库文件：data/platform.db
- 系统日志：data/system.log

## 7. 常见启动问题

- `ModuleNotFoundError`：确认当前目录为项目根目录并已激活虚拟环境
- `cv2` 安装失败：升级 pip 后重试 `pip install opencv-python`
- 端口占用：修改 `scripts/run_backend.py` 中端口
