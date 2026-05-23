# 2-5 Minute Video Walkthrough Script

1. Introduce the project: "This is a Python CLI prototype for Closira's AI support workflow assignment."
2. Show `data/sop.json`: explain that Bloom Aesthetics Clinic is the only source of truth.
3. Show `prompt_design.md`: highlight SOP grounding, structured JSON, confidence, and escalation rules.
4. Run tests:

   ```bash
   pytest
   ```

5. Run a safe in-SOP example:

   ```bash
   python -m closira_agent.cli run-scenario in_sop
   ```

6. Run an escalation example:

   ```bash
   python -m closira_agent.cli run-scenario escalation_trigger
   ```

7. Show real-world case scenarios:

   ```bash
   python -m closira_agent.cli run-scenario real_booking_policy
   python -m closira_agent.cli run-scenario real_price_negotiation
   python -m closira_agent.cli run-scenario real_medical_safety
   ```

   Open `docs/real_world_case_scenarios.md` and point to the expected-vs-actual evaluation table.

8. Show real API setup briefly:

   ```bash
   export OPENAI_API_KEY="..."
   export OPENAI_MODEL="gpt-5-mini"
   python -m closira_agent.cli chat
   ```

9. Close by showing `test_transcripts/` and explaining that each required assignment behaviour has a sample transcript.
