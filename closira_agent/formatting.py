from __future__ import annotations

from .models import Summary, TurnResult


def format_turn(result: TurnResult) -> str:
    lines = [f"Assistant: {result.answer}"]
    lines.append(f"Stage: {result.stage}")
    lines.append(f"Confidence: {result.confidence:.2f}")
    lines.append(f"Escalate: {result.escalate}")
    if result.escalation_reason:
        lines.append(f"Escalation reason: {result.escalation_reason}")
    if result.sop_sources:
        lines.append(f"SOP sources: {', '.join(result.sop_sources)}")
    if result.lead_question:
        lines.append(f"Lead question: {result.lead_question}")
    if result.collected_detail:
        details = ", ".join(f"{key}={value}" for key, value in result.collected_detail.items())
        lines.append(f"Collected detail: {details}")
    if result.sop_gap:
        lines.append(f"SOP gap: {result.sop_gap}")
    return "\n".join(lines)


def format_summary(summary: Summary) -> str:
    detail_lines = (
        [f"- {key}: {value}" for key, value in summary.key_details_collected.items()]
        or ["- None collected"]
    )
    gap_lines = [f"- {gap}" for gap in summary.sop_gaps_identified] or ["- None"]
    reason_lines = [f"- {reason}" for reason in summary.escalation_reasons] or ["- None"]
    return "\n".join(
        [
            "Conversation Summary",
            f"Customer intent: {summary.customer_intent}",
            "Key details collected:",
            *detail_lines,
            "SOP gaps identified:",
            *gap_lines,
            f"Escalation status: {summary.escalation_status}",
            "Escalation reasons:",
            *reason_lines,
            f"Recommended next action: {summary.recommended_next_action}",
        ]
    )
