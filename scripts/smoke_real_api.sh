#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -x ".venv/bin/python" ]]; then
  echo "Missing .venv. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt" >&2
  exit 1
fi

if [[ ! -f ".env" && -z "${OPENAI_API_KEY:-}" ]]; then
  echo "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key, or export it in this shell." >&2
  exit 1
fi

".venv/bin/python" -m closira_agent.cli run-scenario in_sop
