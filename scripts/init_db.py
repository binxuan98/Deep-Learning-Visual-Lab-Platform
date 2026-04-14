import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.config import Config
from backend.db import init_db


if __name__ == "__main__":
    init_db(Config.DATABASE_PATH)
    print("数据库初始化完成:", Config.DATABASE_PATH)
