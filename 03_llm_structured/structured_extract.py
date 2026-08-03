"""Step 3a — structured outputs: contract text -> validated Python objects.

Run:  .venv/bin/python 03_llm_structured/structured_extract.py
      (needs ANTHROPIC_API_KEY; without it, verify.py still checks the schema)

"Document -> structured data" is the single most common demo in legaltech
(clause tagging, risk scoring, obligation extraction). The 2026 way to do
it is SCHEMA-FIRST:

  1. define the output shape as a Pydantic model,
  2. call client.messages.parse(..., output_format=Model),
  3. the API constrains generation to the schema and the SDK returns a
     validated instance in response.parsed_output.

No "please answer in JSON" prompting, no regex parsing, no retry-on-bad-
JSON loop — those are the legacy patterns this replaces.
"""

from pathlib import Path
from typing import Literal

import anthropic
from pydantic import BaseModel, Field

MD = Path(__file__).parent.parent / "data" / "sample_agreement.md"

# claude-opus-4-8: current-generation Opus. At a hackathon you would swap
# in whatever model the sponsor credits cover — one string.
MODEL = "claude-opus-4-8"


class Clause(BaseModel):
    """One contract clause. Field descriptions reach the model as part of
    the schema — write them as instructions, they steer extraction."""

    number: str = Field(description="clause number as written, e.g. '6'")
    title: str
    category: Literal[
        "payment", "confidentiality", "data_protection", "term_termination",
        "liability", "non_solicitation", "assignment", "governing_law", "other",
    ]
    risk_note: str = Field(
        description="one sentence: what should the CUSTOMER watch out for here"
    )


class ContractAnalysis(BaseModel):
    parties: list[str]
    termination_notice_days: int
    liability_cap_eur: int
    clauses: list[Clause]


def analyze(client: anthropic.Anthropic, contract_text: str) -> ContractAnalysis:
    # parse() = create() + schema enforcement + Pydantic validation.
    # The model cannot return anything that fails ContractAnalysis.
    response = client.messages.parse(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": (
                    "Analyze this service agreement from the customer's "
                    "perspective.\n\n" + contract_text
                ),
            }
        ],
        output_format=ContractAnalysis,
    )
    return response.parsed_output


if __name__ == "__main__":
    contract = MD.read_text(encoding="utf-8")
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY (or an `ant auth login` profile)

    try:
        result = analyze(client, contract)
    # No credentials at all -> the SDK raises TypeError("Could not resolve
    # authentication method") at request time; AuthenticationError only
    # fires when a key exists but is invalid. Catch both, but let an
    # unrelated TypeError (a real bug) propagate.
    except (anthropic.AuthenticationError, TypeError) as err:
        if isinstance(err, TypeError) and "authentication" not in str(err).lower():
            raise
        raise SystemExit(
            "No usable API credentials. Set ANTHROPIC_API_KEY (hackathon "
            "sponsor key) and re-run. The offline checks in verify.py work "
            "without one."
        )

    print(f"parties:            {result.parties}")
    print(f"termination notice: {result.termination_notice_days} days")
    print(f"liability cap:      EUR {result.liability_cap_eur:,}")
    print("\nclauses:")
    for c in result.clauses:
        print(f"  {c.number:>2}. [{c.category:<16}] {c.title}")
        print(f"      risk: {c.risk_note}")
