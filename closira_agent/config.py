from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_MODEL = "gpt-5-mini"


@dataclass(frozen=True)
class Settings:
    model: str = DEFAULT_MODEL
    api_key_present: bool = False


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        model=os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
        api_key_present=bool(os.getenv("OPENAI_API_KEY")),
    )
