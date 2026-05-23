from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    slug: str
    title: str
    messages: list[str]


SCENARIOS: dict[str, Scenario] = {
    "in_sop": Scenario(
        slug="in_sop",
        title="In-SOP question",
        messages=["What are your Botox prices?"],
    ),
    "out_of_scope": Scenario(
        slug="out_of_scope",
        title="Out-of-scope question",
        messages=["Do you offer laser hair removal packages?"],
    ),
    "escalation_trigger": Scenario(
        slug="escalation_trigger",
        title="Escalation trigger",
        messages=["I am really frustrated. My appointment experience was unacceptable."],
    ),
    "lead_qualification": Scenario(
        slug="lead_qualification",
        title="Lead qualification",
        messages=[
            "I want to book something for my face but I am not sure where to start.",
            "I am interested in fillers.",
            "Ideally next week.",
            "WhatsApp is best.",
        ],
    ),
    "conversation_summary": Scenario(
        slug="conversation_summary",
        title="Conversation summary",
        messages=[
            "How much are fillers?",
            "I would like a consultation too.",
            "Next Saturday if possible.",
            "Please use WhatsApp.",
            "Do you treat allergic reactions after fillers?",
        ],
    ),
}


def scenario_choices() -> str:
    return ", ".join(sorted(SCENARIOS))
