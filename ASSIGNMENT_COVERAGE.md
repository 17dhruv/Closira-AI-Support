# Assignment Coverage

This file maps the Closira assignment checklist to the implementation.

## Workflow Stages

| Stage | Covered By | Notes |
| --- | --- | --- |
| FAQ answering | `closira_agent/agent.py`, `closira_agent/openai_client.py`, `data/sop.json` | Answers must cite SOP source keys. Missing SOP evidence forces escalation. |
| Lead qualification | `closira_agent/scenarios.py`, `closira_agent/fake_client.py`, `ConversationState` | Collects treatment, timeline, and preferred booking channel. |
| Escalation detection | `closira_agent/agent.py` | Handles explicit handoff, angry sentiment, medical questions, pricing negotiation, low confidence, missing SOP sources, and repeated unanswered questions. |
| Conversation summary | `ClosiraAgent.summarize`, `format_summary` | Produces intent, collected details, SOP gaps, escalation status/reasons, and next action. |

## Required Deliverables

| Deliverable | Status | Location |
| --- | --- | --- |
| Python code | Complete | `closira_agent/` |
| SOP data | Complete | `data/sop.json` |
| Prompt design document | Complete | `prompt_design.md` |
| Test transcripts | Complete | `test_transcripts/` |
| README/setup instructions | Complete | `README.md` |
| Tests | Complete | `tests/test_agent.py` |
| Video walkthrough support | Complete | `docs/video_walkthrough_script.md` |

## Required Behaviour Scenarios

| Scenario | Status | Transcript |
| --- | --- | --- |
| In-SOP question: Botox price | Complete | `test_transcripts/01_in_sop.md` |
| Out-of-scope question | Complete | `test_transcripts/02_out_of_scope.md` |
| Escalation trigger: complaint/frustration | Complete | `test_transcripts/03_escalation_trigger.md` |
| Lead qualification | Complete | `test_transcripts/04_lead_qualification.md` |
| Conversation summary | Complete | `test_transcripts/05_conversation_summary.md` |

## Current Verification

```bash
.venv/bin/python -m pytest
.venv/bin/python -m closira_agent.cli run-scenario in_sop --mock
.venv/bin/python -m closira_agent.cli run-scenario escalation_trigger --mock
```

All automated tests pass locally. Mock scenarios do not spend OpenAI API credit.
