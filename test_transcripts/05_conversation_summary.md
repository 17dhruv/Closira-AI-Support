# Conversation summary

Customer: How much are fillers?
Assistant: Fillers start from £250 at Bloom Aesthetics Clinic.
Stage: faq
Confidence: 0.95
Escalate: False
SOP sources: services.Fillers

Customer: I would like a consultation too.
Assistant: Consultations are free at Bloom Aesthetics Clinic.
Stage: faq
Confidence: 0.95
Escalate: False
SOP sources: services.Consultations

Customer: Next Saturday if possible.
Assistant: Great. Would you prefer to continue via WhatsApp or the website?
Stage: qualification
Confidence: 0.86
Escalate: False
SOP sources: lead_qualification_questions
Lead question: Great. Would you prefer to continue via WhatsApp or the website?
Collected detail: timeline=next saturday if possible.

Customer: Please use WhatsApp.
Assistant: Perfect, I have noted WhatsApp as your preferred booking channel.
Stage: qualification
Confidence: 0.86
Escalate: False
SOP sources: lead_qualification_questions
Collected detail: preferred_channel=WhatsApp

Customer: Do you treat allergic reactions after fillers?
Assistant: I do not want to guess here. I will hand this to a Bloom Aesthetics team member so they can help safely. Reason: Customer asked a medical question that must be handled by a human.
Stage: escalation
Confidence: 1.00
Escalate: True
Escalation reason: Customer asked a medical question that must be handled by a human.

Conversation Summary
Customer intent: Customer is exploring Bloom Aesthetics services and potential booking.
Key details collected:
- timeline: next saturday if possible.
- preferred_channel: WhatsApp
SOP gaps identified:
- None
Escalation status: escalated
Escalation reasons:
- Customer asked a medical question that must be handled by a human.
Recommended next action: Human agent should follow up with safety guidance and booking support.
