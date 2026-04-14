import os
import sys
from functools import wraps

from flask import Flask, jsonify, request, send_from_directory, session

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.config import Config
from backend.db import init_db, insert_history, query_history, query_logs, query_user
from backend.services.algorithm_service import ALGORITHM_META, RUNNERS
from backend.services.file_service import extension_allowed, save_upload_file
from backend.utils.logger import app_log

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config["SECRET_KEY"]


def init_environment() -> None:
    os.makedirs(app.config["UPLOAD_IMAGE_DIR"], exist_ok=True)
    os.makedirs(app.config["UPLOAD_VIDEO_DIR"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_DIR"], exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT, "data"), exist_ok=True)
    init_db(app.config["DATABASE_PATH"])


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return jsonify({"success": False, "message": "请先登录"}), 401
        return func(*args, **kwargs)

    return wrapper


def _run_algorithm(algorithm_key: str, file_path: str):
    if algorithm_key not in RUNNERS:
        return {"success": False, "message": "不支持的算法"}, 400
    if not file_path or not os.path.exists(file_path):
        return {"success": False, "message": "输入文件不存在，请先上传文件"}, 400

    username = session.get("username", "anonymous")
    try:
        result = RUNNERS[algorithm_key](file_path, app.config["OUTPUT_DIR"])
        insert_history(
            app.config["DATABASE_PATH"],
            username,
            algorithm_key,
            file_path,
            result["output_path"],
            result.get("result_text", ""),
        )
        app_log(
            app.config["DATABASE_PATH"],
            app.config["LOG_FILE_PATH"],
            "INFO",
            f"{username} 运行算法 {algorithm_key} 成功",
        )
        payload = {
            "success": True,
            "algorithm": algorithm_key,
            "output_url": f"/outputs/{os.path.basename(result['output_path'])}",
            "result_text": result.get("result_text", ""),
        }
        if "extra_output_path" in result:
            payload["extra_output_url"] = f"/outputs/{os.path.basename(result['extra_output_path'])}"
        return payload, 200
    except Exception as error:
        app_log(
            app.config["DATABASE_PATH"],
            app.config["LOG_FILE_PATH"],
            "ERROR",
            f"运行算法 {algorithm_key} 失败: {error}",
        )
        return {"success": False, "message": f"算法运行失败: {error}"}, 500


@app.route("/")
def root():
    return send_from_directory(os.path.join(PROJECT_ROOT, "frontend"), "login.html")


@app.route("/<path:filename>")
def static_frontend(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, "frontend"), filename)


@app.route("/uploads/<path:filename>")
def uploaded_files(filename):
    for folder in [app.config["UPLOAD_IMAGE_DIR"], app.config["UPLOAD_VIDEO_DIR"]]:
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            return send_from_directory(folder, filename)
    return jsonify({"success": False, "message": "文件不存在"}), 404


@app.route("/outputs/<path:filename>")
def output_files(filename):
    return send_from_directory(app.config["OUTPUT_DIR"], filename)


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()
    user = query_user(app.config["DATABASE_PATH"], username, password)
    if not user:
        app_log(app.config["DATABASE_PATH"], app.config["LOG_FILE_PATH"], "WARN", f"登录失败: {username}")
        return jsonify({"success": False, "message": "用户名或密码错误"}), 401

    session["username"] = user["username"]
    session["role"] = user["role"]
    app_log(app.config["DATABASE_PATH"], app.config["LOG_FILE_PATH"], "INFO", f"用户登录: {username}")
    return jsonify({"success": True, "message": "登录成功", "username": username, "role": user["role"]})


@app.route("/api/logout", methods=["POST"])
def logout():
    username = session.get("username", "unknown")
    session.clear()
    app_log(app.config["DATABASE_PATH"], app.config["LOG_FILE_PATH"], "INFO", f"用户退出: {username}")
    return jsonify({"success": True, "message": "已退出登录"})


@app.route("/api/algorithms", methods=["GET"])
@login_required
def list_algorithms():
    return jsonify({"success": True, "algorithms": ALGORITHM_META})


@app.route("/api/upload/image", methods=["POST"])
@login_required
def upload_image():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "未检测到文件"}), 400
    file = request.files["file"]
    if not file.filename:
        return jsonify({"success": False, "message": "文件名为空"}), 400
    if not extension_allowed(file.filename, app.config["ALLOWED_IMAGE_EXTENSIONS"]):
        return jsonify({"success": False, "message": "图片格式不支持"}), 400
    file_path = save_upload_file(file, app.config["UPLOAD_IMAGE_DIR"])
    return jsonify(
        {
            "success": True,
            "message": "图片上传成功",
            "file_path": file_path,
            "file_url": f"/uploads/{os.path.basename(file_path)}",
        }
    )


@app.route("/api/upload/video", methods=["POST"])
@login_required
def upload_video():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "未检测到文件"}), 400
    file = request.files["file"]
    if not file.filename:
        return jsonify({"success": False, "message": "文件名为空"}), 400
    if not extension_allowed(file.filename, app.config["ALLOWED_VIDEO_EXTENSIONS"]):
        return jsonify({"success": False, "message": "视频格式不支持"}), 400
    file_path = save_upload_file(file, app.config["UPLOAD_VIDEO_DIR"])
    return jsonify(
        {
            "success": True,
            "message": "视频上传成功",
            "file_path": file_path,
            "file_url": f"/uploads/{os.path.basename(file_path)}",
        }
    )


@app.route("/api/run/yolo", methods=["POST"])
@login_required
def run_yolo():
    data = request.get_json(silent=True) or {}
    return _run_algorithm("yolo", data.get("file_path", ""))


@app.route("/api/run/segmentation", methods=["POST"])
@login_required
def run_segmentation():
    data = request.get_json(silent=True) or {}
    return _run_algorithm("segmentation", data.get("file_path", ""))


@app.route("/api/run/mnist", methods=["POST"])
@login_required
def run_mnist():
    data = request.get_json(silent=True) or {}
    return _run_algorithm("mnist", data.get("file_path", ""))


@app.route("/api/run/super_resolution", methods=["POST"])
@login_required
def run_super_resolution():
    data = request.get_json(silent=True) or {}
    return _run_algorithm("super_resolution", data.get("file_path", ""))


@app.route("/api/run/action_recognition", methods=["POST"])
@login_required
def run_action_recognition():
    data = request.get_json(silent=True) or {}
    return _run_algorithm("action_recognition", data.get("file_path", ""))


@app.route("/api/run/texture_style", methods=["POST"])
@login_required
def run_texture_style():
    data = request.get_json(silent=True) or {}
    return _run_algorithm("texture_style", data.get("file_path", ""))


@app.route("/api/history", methods=["GET"])
@login_required
def history():
    username = request.args.get("username")
    data = query_history(app.config["DATABASE_PATH"], username=username)
    for item in data:
        item["output_url"] = f"/outputs/{os.path.basename(item['output_path'])}"
    return jsonify({"success": True, "history": data})


@app.route("/api/logs", methods=["GET"])
@login_required
def logs():
    data = query_logs(app.config["DATABASE_PATH"])
    return jsonify({"success": True, "logs": data})


@app.route("/api/algorithm_docs", methods=["GET"])
@login_required
def algorithm_docs():
    return jsonify({"success": True, "algorithms": ALGORITHM_META})


if __name__ == "__main__":
    init_environment()
    app.run(host="0.0.0.0", port=5000, debug=True)
