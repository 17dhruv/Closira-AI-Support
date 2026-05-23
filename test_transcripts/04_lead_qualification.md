# Lead qualification

Customer: I want to book something for my face but I am not sure where to start.
Assistant: I can help with that. Which treatment are you interested in: Botox, fillers, or a consultation?
Stage: qualification
Confidence: 0.80
Escalate: False
SOP sources: lead_qualification_questions
Lead question: Which treatment are you interested in: Botox, fillers, or a consultation?

Customer: I am interested in fillers.
Assistant: Thanks. When would you ideally like to book?
Stage: qualification
Confidence: 0.86
Escalate: False
SOP sources: lead_qualification_questions
Lead question: Thanks. When would you ideally like to book?
Collected detail: treatment=fillers

Customer: Ideally next week.
Assistant: Great. Would you prefer to continue via WhatsApp or the website?
Stage: qualification
Confidence: 0.86
Escalate: False
SOP sources: lead_qualification_questions
Lead question: Great. Would you prefer to continue via WhatsApp or the website?
Collected detail: timeline=ideally next week.

Customer: WhatsApp is best.
Assistant: Perfect, I have noted WhatsApp as your preferred booking channel.
Stage: qualification
Confidence: 0.86
Escalate: False
SOP sources: lead_qualification_questions
Collected detail: preferred_channel=WhatsApp

Conversation Summary
Customer intent: Customer is exploring Bloom Aesthetics services and potential booking.
Key details collected:
- treatment: fillers
- timeline: ideally next week.
- preferred_channel: WhatsApp
SOP gaps identified:
- None
Escalation status: not_escalated
Escalation reasons:
- None
Recommended next action: Continue qualification and offer booking via WhatsApp or website.
