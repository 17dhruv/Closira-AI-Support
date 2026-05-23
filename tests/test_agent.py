from closira_agent.agent import ClosiraAgent
from closira_agent.fake_client import DeterministicWorkflowClient
from closira_agent.sop import load_sop


def make_agent() -> ClosiraAgent:
    return ClosiraAgent(load_sop(), DeterministicWorkflowClient())


def test_in_sop_botox_price_answer_uses_sop_source() -> None:
    result = make_agent().handle_customer_message("What are your Botox prices?")

    assert result.escalate is False
    assert "£200" in result.answer
    assert result.sop_sources == ["services.Botox"]


def test_out_of_scope_question_escalates_instead_of_guessing() -> None:
    result = make_agent().handle_customer_message("Do you offer laser hair removal packages?")

    assert result.escalate is True
    assert "not listed" in result.escalation_reason or "not covered" in result.answer
    assert result.sop_gap


def test_frustrated_complaint_escalates_deterministically() -> None:
    result = make_agent().handle_customer_message("I am angry and this service was unacceptable.")

    assert result.escalate is True
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
