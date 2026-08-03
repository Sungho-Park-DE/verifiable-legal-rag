"""Verification for project 03.

Run:  .venv/bin/python 03_llm_structured/verify.py

Two layers:
  1. OFFLINE (always runs, no API key): the Pydantic schema accepts valid
     data and rejects invalid data; the agent loop mechanics are exercised
     with a scripted fake client — the LLM is mocked, but the tool call
     into project 02's real Chroma index is executed for real.
  2. LIVE (only if credentials are available): one real structured-output
     call and one real agent run against the sample contract.
"""

import os
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parent))

import pydantic

from structured_extract import MD, ContractAnalysis, analyze
from tool_use_loop import run_agent_loop

failures = 0


def check(name: str, ok: bool) -> None:
    global failures
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        failures += 1


# --- offline 1: schema validation -----------------------------------------

GOOD = {
    "parties": ["Aquila Analytics GmbH", "Borealis Logistik AG"],
    "termination_notice_days": 30,
    "liability_cap_eur": 100_000,
    "clauses": [
        {
            "number": "6",
            "title": "Term and termination",
            "category": "term_termination",
            "risk_note": "Auto-renews unless notice is given 30 days before term end.",
        }
    ],
}


def offline_schema_checks() -> None:
    parsed = ContractAnalysis.model_validate(GOOD)
    check("schema accepts a valid analysis", parsed.termination_notice_days == 30)

    bad_category = {**GOOD, "clauses": [{**GOOD["clauses"][0], "category": "misc"}]}
    try:
        ContractAnalysis.model_validate(bad_category)
        check("schema rejects an out-of-enum category", False)
    except pydantic.ValidationError:
        check("schema rejects an out-of-enum category", True)

    missing_field = {k: v for k, v in GOOD.items() if k != "liability_cap_eur"}
    try:
        ContractAnalysis.model_validate(missing_field)
        check("schema rejects a missing required field", False)
    except pydantic.ValidationError:
        check("schema rejects a missing required field", True)


# --- offline 2: agent loop with a scripted fake client ---------------------


def text_block(text):
    return SimpleNamespace(type="text", text=text)


def tool_use_block(id, name, input):
    return SimpleNamespace(type="tool_use", id=id, name=name, input=input)


class FakeClient:
    """Stands in for anthropic.Anthropic(): pops one scripted response per
    call and records the request kwargs. `self.messages = self` makes
    `client.messages.create(...)` resolve to this create()."""

    def __init__(self, scripted):
        self._scripted = list(scripted)
        self.calls = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._scripted.pop(0)


def offline_loop_checks() -> None:
    # the loop's tool queries project 02's real index — require it first
    import build_index  # importable because tool_use_loop put 02_rag on sys.path

    if build_index.get_collection().count() == 0:
        print("project-02 index is empty — run 02_rag/build_index.py first")
        check("project-02 index exists (the loop's tool needs it)", False)
        return

    fake = FakeClient(
        [
            SimpleNamespace(  # turn 1: model asks for a search
                stop_reason="tool_use",
                content=[
                    text_block("Let me look that up."),
                    tool_use_block(
                        "toolu_01", "search_contract", {"query": "termination notice period"}
                    ),
                ],
            ),
            SimpleNamespace(  # turn 2: model answers
                stop_reason="end_turn",
                content=[
                    text_block(
                        "Notice must be given thirty (30) days before the end "
                        "of the term [6. Term and termination]."
                    )
                ],
            ),
        ]
    )

    response, messages = run_agent_loop(fake, "What is the termination notice period?")

    check("loop returns the final text answer",
          "thirty" in response.content[0].text)
    check("loop made exactly 2 model calls", len(fake.calls) == 2)
    check("request includes the tool definition",
          fake.calls[0]["tools"][0]["name"] == "search_contract")
    check("assistant turn echoed back verbatim",
          messages[1]["role"] == "assistant"
          and messages[1]["content"][1].type == "tool_use")
    tool_result = messages[2]["content"][0]
    check("tool_result id matches the tool_use id",
          tool_result["tool_use_id"] == "toolu_01")
    # the fake mocks the LLM only — the tool hit the REAL project-02 index:
    check("real retrieval ran inside the loop (found the 30-day clause)",
          "thirty (30) days" in tool_result["content"])


# --- live (needs credentials) ----------------------------------------------


def live_checks() -> None:
    import anthropic

    client = anthropic.Anthropic()

    result = analyze(client, MD.read_text(encoding="utf-8"))
    check("LIVE: extracted termination notice == 30 days",
          result.termination_notice_days == 30)
    check("LIVE: extracted liability cap == EUR 100,000",
          result.liability_cap_eur == 100_000)
    check("LIVE: >= 8 clauses extracted", len(result.clauses) >= 8)

    response, _ = run_agent_loop(client, "What is the termination notice period?")
    answer = " ".join(b.text for b in response.content if b.type == "text")
    check("LIVE: agent answer mentions 30 days",
          "30" in answer or "thirty" in answer.lower())


def main() -> None:
    print("--- offline: schema ---")
    offline_schema_checks()
    print("\n--- offline: agent loop (scripted LLM, real retrieval) ---")
    offline_loop_checks()

    if os.environ.get("ANTHROPIC_API_KEY"):
        print("\n--- live: real API calls ---")
        live_checks()
    else:
        print("\n(no ANTHROPIC_API_KEY — live checks skipped; offline checks "
              "fully cover the loop mechanics and schema. Other auth methods "
              "also skip: export ANTHROPIC_API_KEY to opt in to live checks.)")

    print()
    if failures:
        print(f"{failures} check(s) failed")
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
