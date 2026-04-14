import os


def main():
    weights_dir = os.path.join(os.path.dirname(__file__), "..", "models", "weights")
    os.makedirs(weights_dir, exist_ok=True)
    print("已创建模型权重目录:", os.path.abspath(weights_dir))
    print("教学说明：当前项目默认使用轻量演示模型，可自行下载并放入该目录。")


if __name__ == "__main__":
    main()
