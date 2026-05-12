"""Export OpenAPI JSON schema for frontend type generation.

Run from the backend directory:
    python scripts/export_openapi.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.main import app  # noqa: E402

output = Path(__file__).parents[2] / "frontend" / "src" / "api" / "openapi.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(app.openapi(), indent=2), encoding="utf-8")
print(f"Written: {output}")
