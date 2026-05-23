# Closira AI Support Workflow

Python CLI prototype for the Closira AI Engineering Intern assignment. The workflow handles customer support for a fictional SMB, Bloom Aesthetics Clinic, across SOP-grounded FAQ answering, lead qualification, escalation detection, and structured conversation summaries.

## Highlights

- Uses the OpenAI Responses API with structured JSON outputs.
- Answers only from `data/sop.json` and cites SOP source keys.
- Escalates out-of-scope questions, low confidence, complaints, medical questions, pricing negotiation, explicit human requests, and repeated unanswered questions.
- Collects lead qualification details such as treatment interest, timeline, and preferred booking channel.
- Includes required test transcripts plus real-world demo scenarios with expected-vs-actual evaluation criteria.

## Project Structure

```text
closira_agent/
  agent.py              Core workflow, state handling, escalation checks
  cli.py                Real API-backed CLI
  config.py             Environment/model configuration
  formatting.py         Human-readable CLI output
  models.py             Conversation result and summary models
  openai_client.py      OpenAI Responses API structured-output adapter
  prompts.py            System, turn, and summary prompts
  scenarios.py          Required and real-world scripted scenarios
  sop.py                SOP loading helpers
data/
  sop.json              Bloom Aesthetics Clinic SOP source of truth
docs/
  real_world_case_scenarios.md
  video_walkthrough_script.md
test_transcripts/       Required assignment sample conversations
tests/                  Automated behaviour tests
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a private `.env` file:

```bash
cp .env.example .env
```

Fill it with:

```bash
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-5-mini
```

`.env` is ignored by git. Do not commit API keys, virtual environments, caches, or local repo metadata.

## Run The Workflow

Interactive chat:

```bash
.venv/bin/python -m closira_agent.cli chat
```

Run a required assignment scenario:

```bash
.venv/bin/python -m closira_agent.cli run-scenario in_sop
```

Run the real API smoke test:

```bash
./scripts/smoke_real_api.sh
```

Available scenarios:

```text
in_sop
out_of_scope
escalation_trigger
lead_qualification
conversation_summary
real_booking_policy
real_service_comparison
real_price_negotiation
real_medical_safety
real_human_handoff
```

## Real-World Demo Scenarios

The assignment checklist is covered by the five required transcripts. I also added real-world scenarios for a stronger walkthrough:

- Booking and cancellation policy
- Service comparison
- Price negotiation handoff
- Medical safety handoff
- Explicit human handoff

See [docs/real_world_case_scenarios.md](docs/real_world_case_scenarios.md) for the expected-vs-actual evaluation table and scorecard.

## Tests

```bash
.venv/bin/python -m pytest -v
```

The automated tests use a local test adapter so they do not spend OpenAI credits. The public CLI itself is real API-backed and requires `OPENAI_API_KEY`.

## Assignment Coverage

| Requirement | Status | Evidence |
| --- | --- | --- |
| FAQ answering from SOP only | Complete | `data/sop.json`, `closira_agent/agent.py`, `test_transcripts/01_in_sop.md` |
| Lead qualification | Complete | `ConversationState`, `lead_qualification` scenario, `test_transcripts/04_lead_qualification.md` |
| Escalation detection | Complete | deterministic checks in `closira_agent/agent.py` |
| Conversation summary | Complete | `ClosiraAgent.summarize`, `test_transcripts/05_conversation_summary.md` |
| Prompt design document | Complete | `prompt_design.md` |
| Test transcripts | Complete | `test_transcripts/` |
| Setup and trade-offs | Complete | this README |
| Video walkthrough support | Complete | `docs/video_walkthrough_script.md` |

## SOP Source

The assistant operates on `data/sop.json`:

- Business: Bloom Aesthetics Clinic
- Hours: Mon-Sat, 9 am-7 pm
- Services: Botox from £200, fillers from £250, consultations free
- Booking: WhatsApp or website
- Cancellation: 24hr cancellation required
- Escalate if: complaint, medical question, pricing negotiation, or more than two unanswered questions

## Safety Design

- The model must return structured JSON.
- Factual answers must include SOP source keys.
- Missing SOP evidence forces escalation.
- Medical questions are escalated instead of answered.
- Pricing negotiation is escalated instead of inventing discounts.
- Angry sentiment and explicit human handoff requests are caught before model response.

## Trade-Offs And Limitations

- This is a CLI prototype, not a production WhatsApp/email/phone integration.
- The SOP is intentionally compact to demonstrate safe grounding.
- The workflow is optimized for reliability and explainability over broad conversational freedom.
- Checked-in transcripts are sample conversations for the assignment behaviours.
