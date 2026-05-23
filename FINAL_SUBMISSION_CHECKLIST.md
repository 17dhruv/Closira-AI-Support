# Final Submission Checklist

Project status: complete and tested.

## Assignment Requirements

| Assignment requirement | Status | Evidence |
| --- | --- | --- |
| Python-based AI workflow using OpenAI or Claude API | Complete | `closira_agent/openai_client.py`, `closira_agent/cli.py` |
| Simulated conversation end-to-end | Complete | `python -m closira_agent.cli chat` and `run-scenario` commands |
| Stage 1: FAQ answering from SOP only | Complete | `data/sop.json`, `ClosiraAgent.handle_customer_message`, `test_transcripts/01_in_sop.md` |
| Stage 2: lead qualification with 2-3 structured questions | Complete | `lead_qualification_questions` in SOP, `ConversationState.qualification_answers`, `test_transcripts/04_lead_qualification.md` |
| Stage 3: escalation detection | Complete | deterministic checks in `closira_agent/agent.py`, `test_transcripts/02_out_of_scope.md`, `03_escalation_trigger.md` |
| Stage 4: conversation summary | Complete | `ClosiraAgent.summarize`, `format_summary`, `test_transcripts/05_conversation_summary.md` |
| SOP data documented | Complete | `data/sop.json`, README SOP section |
| `prompt_design.md` | Complete | system prompt, hallucination prevention, confidence escalation, tone/persona |
| Test transcripts folder | Complete | `test_transcripts/` has five required scenario transcripts |
| README setup and run instructions | Complete | `README.md` |
| Dependencies documented | Complete | `requirements.txt` |
| Trade-offs / known limitations | Complete | README trade-offs section |
| 2-5 minute video walkthrough support | Complete | `docs/video_walkthrough_script.md` |

## Expected Behaviour Coverage

| Expected behaviour | Covered by |
| --- | --- |
| In-SOP question: "What are your Botox prices?" | `test_transcripts/01_in_sop.md`, pytest |
| Out-of-scope question escalates instead of guessing | `test_transcripts/02_out_of_scope.md`, pytest |
| Complaint/frustration escalates with reason | `test_transcripts/03_escalation_trigger.md`, pytest |
| Lead qualification asks structured questions and stores responses | `test_transcripts/04_lead_qualification.md`, pytest |
| Final summary contains intent, details, SOP gaps, and next action | `test_transcripts/05_conversation_summary.md`, pytest |

## Final Verification Commands

```bash
.venv/bin/python -m pytest -v
.venv/bin/python -m compileall closira_agent tests
.venv/bin/python -m closira_agent.cli run-scenario in_sop --mock
.venv/bin/python -m closira_agent.cli run-scenario out_of_scope --mock
.venv/bin/python -m closira_agent.cli run-scenario escalation_trigger --mock
.venv/bin/python -m closira_agent.cli run-scenario lead_qualification --mock
.venv/bin/python -m closira_agent.cli run-scenario conversation_summary --mock
./scripts/smoke_real_api.sh
```

Latest local verification:

- Pytest: 5 passed
- Mock scenarios: all required behaviours passed
- Real API smoke test: passed with `gpt-5-mini`
- Secret scan: no API key found in tracked files
- `.env`, `.venv`, and `.repo` are ignored

## Submission Notes

- Do not submit `.env`, `.venv`, `.repo`, `__pycache__`, or `.pytest_cache`.
- Rotate the OpenAI API key after final testing because it was visible during local setup.
- Use the isolated Git commands from the README/final assistant instructions if the parent `/home/drizzy` Git repo interferes.
