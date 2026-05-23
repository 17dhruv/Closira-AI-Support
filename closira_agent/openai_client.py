from __future__ import annotations

import json
from typing import Any

from .prompts import build_summary_prompt, build_system_prompt, build_turn_prompt


TURN_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "stage": {"type": "string", "enum": ["faq", "qualification", "escalation", "summary"]},
        "answer": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "sop_sources": {"type": "array", "items": {"type": "string"}},
        "escalate": {"type": "boolean"},
        "escalation_reason": {"type": ["string", "null"]},
        "lead_question": {"type": ["string", "null"]},
        "collected_detail": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["key", "value"],
            },
        },
        "sop_gap": {"type": ["string", "null"]},
    },
    "required": [
        "stage",
        "answer",
        "confidence",
        "sop_sources",
        "escalate",
        "escalation_reason",
        "lead_question",
        "collected_detail",
        "sop_gap",
    ],
}

SUMMARY_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "customer_intent": {"type": "string"},
        "key_details_collected": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "key": {"type": "string"},
                    "value": {"type": "string"},
                },
                "required": ["key", "value"],
            },
        },
        "sop_gaps_identified": {"type": "array", "items": {"type": "string"}},
        "escalation_status": {"type": "string", "enum": ["not_escalated", "escalated"]},
        "escalation_reasons": {"type": "array", "items": {"type": "string"}},
        "recommended_next_action": {"type": "string"},
    },
    "required": [
        "customer_intent",
        "key_details_collected",
        "sop_gaps_identified",
        "escalation_status",
        "escalation_reasons",
        "recommended_next_action",
    ],
}


class OpenAIWorkflowClient:
    def __init__(self, model: str, client: Any | None = None) -> None:
        self.model = model
        if client is not None:
            self.client = client
            return
        try:
            from openai import OpenAI
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "The openai package is not installed. Run: pip install -r requirements.txt"
            ) from exc
        self.client = OpenAI()

    def evaluate_turn(self, sop: dict[str, Any], session_payload: dict[str, Any]) -> dict[str, Any]:
        return self._json_response(
            instructions=build_system_prompt(sop),
            prompt=build_turn_prompt(session_payload),
            schema_name="support_turn",
            schema=TURN_SCHEMA,
            max_output_tokens=1800,
        )

    def summarize(self, sop: dict[str, Any], session_payload: dict[str, Any]) -> dict[str, Any]:
        return self._json_response(
            instructions=build_system_prompt(sop),
            prompt=build_summary_prompt(session_payload),
            schema_name="conversation_summary",
            schema=SUMMARY_SCHEMA,
            max_output_tokens=1800,
        )

    def _json_response(
        self,
        instructions: str,
        prompt: str,
        schema_name: str,
        schema: dict[str, Any],
        max_output_tokens: int,
    ) -> dict[str, Any]:
        response = self.client.responses.create(
            model=self.model,
            instructions=instructions,
            input=[
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": prompt}],
                }
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": schema_name,
                    "schema": schema,
                    "strict": True,
                }
            },
            max_output_tokens=max_output_tokens,
        )
        output_text = response.output_text
        if not output_text:
            status = getattr(response, "status", "unknown")
            incomplete = getattr(response, "incomplete_details", None)
            raise RuntimeError(
                f"OpenAI returned no output text. status={status}, incomplete_details={incomplete}"
            )
        return json.loads(output_text)
