from closira_agent.agent import ClosiraAgent
from closira_agent.sop import load_sop


def make_agent() -> ClosiraAgent:
    return ClosiraAgent(load_sop(), TestWorkflowClient())


class TestWorkflowClient:
    def evaluate_turn(self, sop: dict, session_payload: dict) -> dict:
        message = session_payload["latest_customer_message"].lower()
        qualification_answers = session_payload.get("qualification_answers", {})

        if "botox" in message and ("price" in message or "cost" in message):
            return turn("faq", "Botox starts from £200 at Bloom Aesthetics Clinic.", 0.96, ["services.Botox"])
        if "laser" in message or "hair removal" in message:
            return turn(
                "faq",
                "That service is not covered in the Bloom Aesthetics SOP, so I cannot confirm it.",
                0.35,
                [],
                escalate=True,
                escalation_reason="The customer asked about a service not listed in the SOP.",
                sop_gap="Laser hair removal availability is not in the SOP.",
            )
        if "filler" in message and "treatment" not in qualification_answers:
            return turn(
                "qualification",
                "Thanks. When would you ideally like to book?",
                0.86,
                ["lead_qualification_questions"],
                lead_question="Thanks. When would you ideally like to book?",
                collected_detail={"treatment": "fillers"},
            )
        if ("next week" in message or "saturday" in message) and "timeline" not in qualification_answers:
            return turn(
                "qualification",
                "Great. Would you prefer to continue via WhatsApp or the website?",
                0.86,
                ["lead_qualification_questions"],
                lead_question="Great. Would you prefer to continue via WhatsApp or the website?",
                collected_detail={"timeline": message},
            )
        if "whatsapp" in message and "preferred_channel" not in qualification_answers:
            return turn(
                "qualification",
                "Perfect, I have noted WhatsApp as your preferred booking channel.",
                0.86,
                ["lead_qualification_questions"],
                collected_detail={"preferred_channel": "WhatsApp"},
            )
        return turn(
            "qualification",
            "I can help with that. Which treatment are you interested in: Botox, fillers, or a consultation?",
            0.8,
            ["lead_qualification_questions"],
            lead_question="Which treatment are you interested in: Botox, fillers, or a consultation?",
        )

    def summarize(self, sop: dict, session_payload: dict) -> dict:
        reasons = session_payload.get("escalation_reasons", [])
        return {
            "customer_intent": "Customer is exploring Bloom Aesthetics services and potential booking.",
            "key_details_collected": session_payload.get("qualification_answers", {}),
            "sop_gaps_identified": session_payload.get("sop_gaps", []),
            "escalation_status": "escalated" if reasons else "not_escalated",
            "escalation_reasons": reasons,
            "recommended_next_action": (
                "Human agent should follow up with safety guidance and booking support."
                if reasons
                else "Continue qualification and offer booking via WhatsApp or website."
            ),
        }


def turn(
    stage: str,
    answer: str,
    confidence: float,
    sources: list[str],
    *,
    escalate: bool = False,
    escalation_reason: str | None = None,
    lead_question: str | None = None,
    collected_detail: dict | None = None,
    sop_gap: str | None = None,
) -> dict:
    return {
        "stage": stage,
        "answer": answer,
        "confidence": confidence,
        "sop_sources": sources,
        "escalate": escalate,
        "escalation_reason": escalation_reason,
        "lead_question": lead_question,
        "collected_detail": collected_detail or {},
        "sop_gap": sop_gap,
    }


def test_in_sop_botox_price_answer_uses_sop_source() -> None:
    result = make_agent().handle_customer_message("What are your Botox prices?")

    assert result.escalate is False
    assert "£200" in result.answer
    assert result.sop_sources == ["services.Botox"]


def test_out_of_scope_question_escalates_instead_of_guessing() -> None:
    result = make_agent().handle_customer_message("Do you offer laser hair removal packages?")

    assert result.escalate is True
    assert result.escalation_reason is not None
    assert "not listed" in result.escalation_reason or "not covered" in result.answer
    assert result.sop_gap


def test_frustrated_complaint_escalates_deterministically() -> None:
    result = make_agent().handle_customer_message("I am angry and this service was unacceptable.")

    assert result.escalate is True
    assert result.escalation_reason is not None
    assert "frustration" in result.escalation_reason or "complaint" in result.escalation_reason


def test_lead_qualification_collects_structured_answers() -> None:
    agent = make_agent()

    agent.handle_customer_message("I want to book something for my face.")
    agent.handle_customer_message("I am interested in fillers.")
    agent.handle_customer_message("Next week works.")
    agent.handle_customer_message("WhatsApp is best.")

    assert agent.state.qualification_answers["treatment"] == "fillers"
    assert "next week" in agent.state.qualification_answers["timeline"]
    assert agent.state.qualification_answers["preferred_channel"] == "WhatsApp"


def test_summary_contains_intent_details_gaps_and_next_action() -> None:
    agent = make_agent()
    agent.handle_customer_message("How much are fillers?")
    agent.handle_customer_message("Do you treat allergic reactions after fillers?")

    summary = agent.summarize()

    assert summary.customer_intent
    assert summary.escalation_status == "escalated"
    assert summary.escalation_reasons
    assert summary.recommended_next_action
