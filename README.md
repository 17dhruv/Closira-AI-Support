# Closira AI Support Workflow

Python CLI prototype for the Closira AI Engineering Intern assignment. It handles a simulated customer support conversation for Bloom Aesthetics Clinic across FAQ answering, lead qualification, escalation detection, and final conversation summary.

## What This Demonstrates

- FAQ answers are grounded only in `data/sop.json`.
- Lead qualification asks structured follow-up questions and stores answers.
- Escalation is triggered for low confidence, out-of-scope questions, complaints, medical questions, price negotiation, explicit human requests, or more than two unanswered questions.
- End-of-session summaries include intent, details collected, SOP gaps, escalation reasons, and recommended next action.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
export OPENAI_MODEL="gpt-5-mini"
```

You can also copy `.env.example` to `.env` and fill in your key. `.env` is ignored by git and must never be committed. Do not paste your API key into `.venv/bin/activate`, source files, docs, transcripts, or terminal commands that will be saved in shell history.

The default model is `gpt-5-mini` for cost control. Current OpenAI model docs list `gpt-5-mini` as the faster, cost-efficient GPT-5 model with Responses API and structured output support. To use a stronger frontier model, set another available model explicitly:

```bash
export OPENAI_MODEL="gpt-5.2"
```

## Run

Interactive API-backed chat:

```bash
python -m closira_agent.cli chat
```

Run a scripted assignment scenario with the real API:

```bash
python -m closira_agent.cli run-scenario in_sop
```

Or use the smoke-test helper:

```bash
./scripts/smoke_real_api.sh
```

Available scenarios:

```text
in_sop, out_of_scope, escalation_trigger, lead_qualification, conversation_summary
```

Generate deterministic local transcripts without spending API credit:

```bash
python -m closira_agent.cli generate-transcripts
```

Local mock mode for demos/tests:

```bash
python -m closira_agent.cli run-scenario lead_qualification --mock
python -m closira_agent.cli chat --mock
```

## Tests

```bash
pytest
```

The tests use a deterministic mock client, so they do not require `OPENAI_API_KEY` and do not spend API credits.

## Assignment Checklist

- GitHub repo with code: this project is structured as a clean Python package.
- `prompt_design.md`: included with the full prompt and design rationale.
- `test_transcripts/`: included with one transcript per required behaviour.
- `README.md`: this setup and usage guide.
- 2-5 minute video walkthrough: use `docs/video_walkthrough_script.md` as a recording script.

## SOP Source

The assistant operates on `data/sop.json`, based on the provided assignment SOP:

- Business: Bloom Aesthetics Clinic
- Hours: Mon-Sat, 9 am-7 pm
- Services: Botox from £200, fillers from £250, consultations free
- Booking: WhatsApp or website
- Cancellation: 24hr cancellation required
- Escalate if: complaint, medical question, pricing negotiation, or more than two unanswered questions

## Trade-Offs and Limitations

- This is a CLI prototype, not a production WhatsApp/email/phone integration.
- The SOP is intentionally small to prove safe grounding behaviour.
- Medical and complaint handling is escalated instead of answered.
- Transcript generation uses deterministic mock responses to keep the submitted examples stable and avoid API spend.
