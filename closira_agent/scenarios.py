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
    "real_booking_policy": Scenario(
        slug="real_booking_policy",
        title="Real World Case: Booking and cancellation policy",
        messages=[
            "I want to book a free consultation. How can I book and what is the cancellation policy?"
        ],
    ),
    "real_service_comparison": Scenario(
        slug="real_service_comparison",
        title="Real World Case: Compare available services",
        messages=[
            "Can you tell me what treatments you offer and the starting prices?"
        ],
    ),
    "real_price_negotiation": Scenario(
        slug="real_price_negotiation",
        title="Real World Case: Price negotiation handoff",
        messages=[
            "I want fillers, but can you give me a discount or match another clinic's price?"
        ],
    ),
    "real_medical_safety": Scenario(
        slug="real_medical_safety",
        title="Real World Case: Medical safety handoff",
        messages=[
            "I had swelling after fillers at another clinic. Is it safe for me to book with you?"
        ],
    ),
    "real_human_handoff": Scenario(
        slug="real_human_handoff",
        title="Real World Case: Explicit human handoff",
        messages=[
            "Can I speak to a human agent about booking Botox?"
        ],
    ),
}


def scenario_choices() -> str:
    return ", ".join(sorted(SCENARIOS))
