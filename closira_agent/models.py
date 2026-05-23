from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


Stage = Literal["faq", "qualification", "escalation", "summary"]


@dataclass
class TurnResult:
    stage: Stage
    answer: str
    confidence: float
    sop_sources: list[str] = field(default_factory=list)
    escalate: bool = False
    escalation_reason: str | None = None
    lead_question: str | None = None
    collected_detail: dict[str, str] = field(default_factory=dict)
    sop_gap: str | None = None

    @classmethod
    def from_model_json(cls, payload: dict[str, Any]) -> "TurnResult":
        collected_detail = _details_to_dict(payload.get("collected_detail", {}))
        return cls(
            stage=payload.get("stage", "faq"),
            answer=payload.get("answer", ""),
            confidence=float(payload.get("confidence", 0.0)),
            sop_sources=list(payload.get("sop_sources", [])),
            escalate=bool(payload.get("escalate", False)),
            escalation_reason=payload.get("escalation_reason"),
            lead_question=payload.get("lead_question"),
            collected_detail=collected_detail,
            sop_gap=payload.get("sop_gap"),
        )


@dataclass
class ConversationState:
    customer_messages: list[str] = field(default_factory=list)
    assistant_messages: list[str] = field(default_factory=list)
    qualification_answers: dict[str, str] = field(default_factory=dict)
    sop_gaps: list[str] = field(default_factory=list)
    escalation_reasons: list[str] = field(default_factory=list)
    unanswered_count: int = 0

    def history(self) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        max_len = max(len(self.customer_messages), len(self.assistant_messages))
        for index in range(max_len):
            if index < len(self.customer_messages):
                rows.append({"role": "customer", "content": self.customer_messages[index]})
            if index < len(self.assistant_messages):
                rows.append({"role": "assistant", "content": self.assistant_messages[index]})
        return rows


@dataclass(frozen=True)
class Summary:
    customer_intent: str
    key_details_collected: dict[str, str]
    sop_gaps_identified: list[str]
    escalation_status: str
    escalation_reasons: list[str]
    recommended_next_action: str

    @classmethod
    def from_model_json(cls, payload: dict[str, Any]) -> "Summary":
        key_details = _details_to_dict(payload.get("key_details_collected", {}))
        return cls(
            customer_intent=payload.get("customer_intent", "Unknown"),
            key_details_collected=key_details,
            sop_gaps_identified=list(payload.get("sop_gaps_identified", [])),
            escalation_status=payload.get("escalation_status", "not_escalated"),
            escalation_reasons=list(payload.get("escalation_reasons", [])),
            recommended_next_action=payload.get("recommended_next_action", "Review session"),
        )


def _details_to_dict(raw_details: Any) -> dict[str, str]:
    if isinstance(raw_details, dict):
        return {str(key): str(value) for key, value in raw_details.items()}
    if isinstance(raw_details, list):
        details: dict[str, str] = {}
        for item in raw_details:
            if isinstance(item, dict) and "key" in item and "value" in item:
                details[str(item["key"])] = str(item["value"])
        return details
    return {}
