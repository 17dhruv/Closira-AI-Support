from __future__ import annotations

from typing import Any


class DeterministicWorkflowClient:
    """Rule-based client used for tests and transcript generation without API spend."""

    def evaluate_turn(self, sop: dict[str, Any], session_payload: dict[str, Any]) -> dict[str, Any]:
        message = session_payload["latest_customer_message"].lower()
        qualification_answers = session_payload.get("qualification_answers", {})

        if "botox" in message and ("price" in message or "cost" in message):
            return {
                "stage": "faq",
                "answer": "Botox starts from £200 at Bloom Aesthetics Clinic.",
                "confidence": 0.96,
                "sop_sources": ["services.Botox"],
                "escalate": False,
                "escalation_reason": None,
                "lead_question": None,
                "collected_detail": {},
                "sop_gap": None,
            }
        if "filler" in message and ("price" in message or "cost" in message or "how much" in message):
            return {
                "stage": "faq",
                "answer": "Fillers start from £250 at Bloom Aesthetics Clinic.",
                "confidence": 0.95,
                "sop_sources": ["services.Fillers"],
                "escalate": False,
                "escalation_reason": None,
                "lead_question": None,
                "collected_detail": {},
                "sop_gap": None,
            }
        if "consultation" in message:
            return {
                "stage": "faq",
                "answer": "Consultations are free at Bloom Aesthetics Clinic.",
                "confidence": 0.95,
                "sop_sources": ["services.Consultations"],
                "escalate": False,
                "escalation_reason": None,
                "lead_question": None,
                "collected_detail": {},
                "sop_gap": None,
            }
        if "laser" in message or "hair removal" in message:
            return {
                "stage": "faq",
                "answer": "That service is not covered in the Bloom Aesthetics SOP, so I cannot confirm it.",
                "confidence": 0.35,
                "sop_sources": [],
                "escalate": True,
                "escalation_reason": "The customer asked about a service not listed in the SOP.",
                "lead_question": None,
                "collected_detail": {},
                "sop_gap": "Laser hair removal availability is not in the SOP.",
            }

        if "filler" in message and "treatment" not in qualification_answers:
            return self._qualification_response(
                "Thanks. When would you ideally like to book?",
                {"treatment": "fillers"},
            )
        if ("next week" in message or "saturday" in message) and "timeline" not in qualification_answers:
            return self._qualification_response(
                "Great. Would you prefer to continue via WhatsApp or the website?",
                {"timeline": message},
            )
        if "whatsapp" in message and "preferred_channel" not in qualification_answers:
            return self._qualification_response(
                "Perfect, I have noted WhatsApp as your preferred booking channel.",
                {"preferred_channel": "WhatsApp"},
            )

        return {
            "stage": "qualification",
            "answer": "I can help with that. Which treatment are you interested in: Botox, fillers, or a consultation?",
            "confidence": 0.8,
            "sop_sources": ["lead_qualification_questions"],
            "escalate": False,
            "escalation_reason": None,
            "lead_question": "Which treatment are you interested in: Botox, fillers, or a consultation?",
            "collected_detail": {},
            "sop_gap": None,
        }

    def summarize(self, sop: dict[str, Any], session_payload: dict[str, Any]) -> dict[str, Any]:
        reasons = session_payload.get("escalation_reasons", [])
        gaps = session_payload.get("sop_gaps", [])
        details = session_payload.get("qualification_answers", {})
        return {
            "customer_intent": "Customer is exploring Bloom Aesthetics services and potential booking.",
            "key_details_collected": details,
            "sop_gaps_identified": gaps,
            "escalation_status": "escalated" if reasons else "not_escalated",
            "escalation_reasons": reasons,
            "recommended_next_action": (
                "Human agent should follow up with safety guidance and booking support."
                if reasons
                else "Continue qualification and offer booking via WhatsApp or website."
            ),
        }

    @staticmethod
    def _qualification_response(answer: str, detail: dict[str, str]) -> dict[str, Any]:
        return {
            "stage": "qualification",
            "answer": answer,
            "confidence": 0.86,
            "sop_sources": ["lead_qualification_questions"],
            "escalate": False,
            "escalation_reason": None,
            "lead_question": answer if answer.endswith("?") else None,
            "collected_detail": detail,
            "sop_gap": None,
        }
