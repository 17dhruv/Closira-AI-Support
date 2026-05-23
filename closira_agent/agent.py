from __future__ import annotations

import re
from typing import Any

from .models import ConversationState, Summary, TurnResult


EXPLICIT_HANDOFF_TERMS = (
    "human",
    "manager",
    "agent",
    "representative",
    "real person",
    "call me",
    "phone me",
)
ANGRY_TERMS = (
    "angry",
    "furious",
    "frustrated",
    "unacceptable",
    "terrible",
    "awful",
    "complaint",
    "complain",
    "bad service",
    "not happy",
    "upset",
)
MEDICAL_TERMS = (
    "side effect",
    "side effects",
    "pregnant",
    "allergic",
    "allergy",
    "medical",
    "safe for me",
    "diagnose",
    "infection",
    "swelling",
    "pain",
    "medicine",
)
NEGOTIATION_TERMS = (
    "discount",
    "cheaper",
    "negotiate",
    "lower price",
    "price match",
    "deal",
    "coupon",
)


class ClosiraAgent:
    def __init__(
        self,
        sop: dict[str, Any],
        workflow_client: Any,
        confidence_threshold: float = 0.65,
    ) -> None:
        self.sop = sop
        self.workflow_client = workflow_client
        self.confidence_threshold = confidence_threshold
        self.state = ConversationState()

    def handle_customer_message(self, message: str) -> TurnResult:
        self.state.customer_messages.append(message)

        deterministic_reason = self._deterministic_escalation_reason(message)
        if deterministic_reason:
            result = TurnResult(
                stage="escalation",
                answer=self._handoff_message(deterministic_reason),
                confidence=1.0,
                escalate=True,
                escalation_reason=deterministic_reason,
            )
            self._record_result(result)
            return result

        payload = self._session_payload(message)
        model_payload = self.workflow_client.evaluate_turn(self.sop, payload)
        result = TurnResult.from_model_json(model_payload)

        if self._should_force_escalation(result):
            reason = self._forced_escalation_reason(result)
            result.escalate = True
            result.stage = "escalation"
            result.escalation_reason = reason
            result.answer = self._handoff_message(reason)

        self._record_result(result)
        return result

    def summarize(self) -> Summary:
        payload = {
            "history": self.state.history(),
            "qualification_answers": self.state.qualification_answers,
            "sop_gaps": self.state.sop_gaps,
            "escalation_reasons": self.state.escalation_reasons,
            "unanswered_count": self.state.unanswered_count,
        }
        model_payload = self.workflow_client.summarize(self.sop, payload)
        summary = Summary.from_model_json(model_payload)

        if self.state.escalation_reasons and summary.escalation_status != "escalated":
            return Summary(
                customer_intent=summary.customer_intent,
                key_details_collected=summary.key_details_collected,
                sop_gaps_identified=summary.sop_gaps_identified,
                escalation_status="escalated",
                escalation_reasons=self.state.escalation_reasons,
                recommended_next_action=summary.recommended_next_action,
            )
        return summary

    def _session_payload(self, latest_message: str) -> dict[str, Any]:
        return {
            "latest_customer_message": latest_message,
            "history": self.state.history(),
            "qualification_answers": self.state.qualification_answers,
            "unanswered_count": self.state.unanswered_count,
            "known_sop_gap_count": len(self.state.sop_gaps),
        }

    def _deterministic_escalation_reason(self, message: str) -> str | None:
        normalized = message.lower()
        if _contains_terms(normalized, EXPLICIT_HANDOFF_TERMS):
            return "Customer explicitly requested a human handoff."
        if _contains_terms(normalized, ANGRY_TERMS):
            return "Customer sentiment indicates frustration or a complaint."
        if _contains_terms(normalized, MEDICAL_TERMS):
            return "Customer asked a medical question that must be handled by a human."
        if _contains_terms(normalized, NEGOTIATION_TERMS):
            return "Customer is negotiating price, which the SOP marks for escalation."
        if self.state.unanswered_count > 2:
            return "More than two questions have gone unanswered from the SOP."
        return None

    def _should_force_escalation(self, result: TurnResult) -> bool:
        if result.escalate:
            return True
        if result.confidence < self.confidence_threshold:
            return True
        if result.stage == "faq" and not result.sop_sources:
            return True
        return False

    def _forced_escalation_reason(self, result: TurnResult) -> str:
        if result.escalation_reason:
            return result.escalation_reason
        if result.confidence < self.confidence_threshold:
            return "Model confidence was below the safe-answer threshold."
        if result.stage == "faq" and not result.sop_sources:
            return "Model did not cite any SOP source for a factual answer."
        return "The workflow could not safely answer from the SOP."

    def _record_result(self, result: TurnResult) -> None:
        self.state.assistant_messages.append(result.answer)
        if result.collected_detail:
            self.state.qualification_answers.update(result.collected_detail)
        if result.sop_gap:
            self.state.sop_gaps.append(result.sop_gap)
            self.state.unanswered_count += 1
        if result.escalate and result.escalation_reason:
            self.state.escalation_reasons.append(result.escalation_reason)

    @staticmethod
    def _handoff_message(reason: str) -> str:
        return (
            "I do not want to guess here. I will hand this to a Bloom Aesthetics "
            f"team member so they can help safely. Reason: {reason}"
        )


def _contains_terms(text: str, terms: tuple[str, ...]) -> bool:
    for term in terms:
        if " " in term:
            if term in text:
                return True
        elif re.search(rf"\b{re.escape(term)}\b", text):
            return True
    return False
