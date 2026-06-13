"""Render entrypoint for the backend service.

Render's current service runs `uvicorn main:app` from the repository root.
The actual FastAPI app lives in `backend/main.py`, so this shim exposes it.
"""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

from main import app  # noqa: E402
