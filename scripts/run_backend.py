import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import app, init_environment


if __name__ == "__main__":
    init_environment()
    app.run(host="0.0.0.0", port=5000, debug=True)
