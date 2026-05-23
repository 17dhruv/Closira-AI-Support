from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_SOP_PATH = Path(__file__).resolve().parents[1] / "data" / "sop.json"


def load_sop(path: Path | str = DEFAULT_SOP_PATH) -> dict[str, Any]:
    sop_path = Path(path)
    with sop_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def sop_as_prompt_context(sop: dict[str, Any]) -> str:
    return json.dumps(sop, indent=2, ensure_ascii=False)
