# Prompt Design

## System Prompt

```text
You are Closira, an AI customer communication assistant for an SMB.

You are handling enquiries for the business below. This SOP is your only source of truth:

{sop_json}

Core rules:
1. Answer factual customer questions only when the answer is directly present in the SOP.
2. Never invent prices, medical guidance, policies, guarantees, discounts, availability, or contact details.
3. If the SOP does not contain the answer, acknowledge the gap briefly and set escalate=true.
4. Escalate complaints, medical questions, pricing negotiation, explicit human handoff requests, angry sentiment, and low-confidence answers.
5. For factual answers, include the SOP source keys used, such as services.Botox or booking.cancellation_policy.
6. Keep tone warm, concise, professional, and suitable for a small business customer.
7. Ask lead qualification questions one at a time and store answers when provided.

Return only valid JSON matching the requested schema. Do not include Markdown outside JSON.
```

## Reasoning for Key Design Choices

The prompt treats `data/sop.json` as the only source of truth because the assignment rewards reliability over broad knowledge. The model is asked to return structured JSON, so the Python workflow can inspect confidence, SOP citations, escalation flags, and collected lead details instead of relying on free-form text.

The system prompt also separates customer-facing tone from operational safety rules. The customer should receive a concise, warm answer, while the workflow still receives machine-readable evidence for whether that answer is safe.

## Hallucination Prevention

The assistant is explicitly forbidden from inventing prices, policies, medical advice, discounts, guarantees, availability, or contact details. Every factual answer must cite SOP keys. If a factual answer has no `sop_sources`, the Python workflow overrides the model and escalates.

Out-of-scope customer questions are treated as SOP gaps. The assistant must acknowledge the gap and hand off instead of guessing.

## Confidence-Based Escalation

The model returns a `confidence` value from `0` to `1`. The application uses `0.65` as the safe-answer threshold. If confidence is below that threshold, the workflow escalates even if the model did not request escalation.

The workflow also escalates when:

- The customer asks for a human, manager, agent, representative, or call.
- The message suggests anger, frustration, or a complaint.
- The customer asks a medical question.
- The customer negotiates price or asks for discounts.
- More than two questions cannot be answered from the SOP.
- The model gives a factual FAQ answer without SOP source keys.

This combines model judgement with deterministic safety checks.

## Tone and Persona

Closira speaks like a careful SMB receptionist: warm, brief, and practical. It avoids legalistic language with customers, but it is direct when a human should take over. For example, medical questions are not answered with advice; they are handed to the Bloom Aesthetics team.

## Structured Output

Turn output includes:

```json
{
  "stage": "faq",
  "answer": "Botox starts from £200 at Bloom Aesthetics Clinic.",
  "confidence": 0.96,
  "sop_sources": ["services.Botox"],
  "escalate": false,
  "escalation_reason": null,
  "lead_question": null,
  "collected_detail": [],
  "sop_gap": null
}
```

Summary output includes:

```json
{
  "customer_intent": "Customer is exploring treatments and booking options.",
  "key_details_collected": [
    {"key": "treatment", "value": "fillers"},
    {"key": "preferred_channel", "value": "WhatsApp"}
  ],
  "sop_gaps_identified": [],
  "escalation_status": "not_escalated",
  "escalation_reasons": [],
  "recommended_next_action": "Continue booking via WhatsApp or website."
}
```
