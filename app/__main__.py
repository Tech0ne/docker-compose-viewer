import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app


HOST = os.getenv("FLASK_RUN_HOST") or "0.0.0.0"

PORT = int(os.getenv("FLASK_RUN_PORT") or 80)

app = create_app()

app.run(host=HOST, port=PORT, debug=False)
