"""Step 3b — the tool-use loop: what every "agent framework" does under the hood.

Run:  .venv/bin/python 03_llm_structured/tool_use_loop.py "Is there a cap on damages?"
      (needs ANTHROPIC_API_KEY and the project-02 index; verify.py tests the
      loop offline with a scripted fake client)

An "agent" is this loop and nothing more:

    1. send the conversation + tool definitions to the model,
    2. if stop_reason == "tool_use": execute the requested tool(s) locally,
       append the assistant turn AND the tool results, go to 1,
    3. otherwise the text answer is final.

The tool here is the Chroma retriever from project 02 — which makes this
file "agentic RAG": instead of us deciding what to retrieve (project 02),
the MODEL decides what to search for and can search multiple times.

Two rules the API enforces that frameworks usually hide:
  * the assistant turn must be echoed back VERBATIM (including tool_use
    blocks) before the tool results,
  * every tool_use id needs exactly one matching tool_result, and all
    results for a turn go back in ONE user message.
"""

import sys
from pathlib import Path

import anthropic

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "02_rag"))

from query import retrieve  # project 02's Chroma retriever

MODEL = "claude-opus-4-8"

# The description is not documentation — it is the model's ONLY basis for
# deciding when to call the tool. Be prescriptive about the "when".
SEARCH_TOOL = {
    "name": "search_contract",
    "description": (
        "Search the indexed service agreement and return the most relevant "
        "clauses. Call this before answering ANY question about the "
        "contract — never answer from memory. Call it again with a "
        "different query if the first results do not contain the answer."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "what to look for, e.g. 'termination notice period'",
            }
        },
        "required": ["query"],
        "additionalProperties": False,
    },
    # strict: guarantees tool inputs validate against the schema exactly
    "strict": True,
}

SYSTEM = (
    "You are a contract analyst. Answer questions about the service "
    "agreement using ONLY what search_contract returns. Cite the section "
    "title for every claim, like [6. Term and termination]. If the search "
    "results do not contain the answer, say so instead of guessing."
)


def search_contract(query: str) -> str:
    hits = retrieve(query, k=3)
    return "\n\n".join(f"[{h['section']}] {h['text']}" for h in hits)


TOOLS = {"search_contract": search_contract}


def run_agent_loop(client, question: str, max_turns: int = 5):
    """The entire agent. `client` is injected so verify.py can pass a fake.

    Returns (final_response, messages) — messages is everything that was
    SENT to the model (the final reply is returned separately, not
    appended). Read it once to see exactly what the model saw each turn.
    """
    messages = [{"role": "user", "content": question}]

    for _ in range(max_turns):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM,
            tools=[SEARCH_TOOL],
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            return response, messages  # model is done — text answer is final

        # Rule 1: echo the assistant turn back verbatim, tool_use blocks included.
        messages.append({"role": "assistant", "content": response.content})

        # Rule 2: one tool_result per tool_use id, all in ONE user message.
        results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  -> {block.name}({block.input})")
                output = TOOLS[block.name](**block.input)
                results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": output}
                )
        messages.append({"role": "user", "content": results})

    raise RuntimeError(f"agent did not finish within {max_turns} turns")


if __name__ == "__main__":
    question = sys.argv[1] if len(sys.argv) > 1 else "What is the termination notice period?"
    client = anthropic.Anthropic()

    try:
        response, transcript = run_agent_loop(client, question)
    # No credentials at all -> TypeError at request time; invalid key ->
    # AuthenticationError. Catch both, but let an unrelated TypeError
    # (a real bug, e.g. inside a tool) propagate — see structured_extract.py.
    except (anthropic.AuthenticationError, TypeError) as err:
        if isinstance(err, TypeError) and "authentication" not in str(err).lower():
            raise
        raise SystemExit(
            "No usable API credentials. Set ANTHROPIC_API_KEY and re-run. "
            "verify.py tests this loop offline without a key."
        )

    print(f"\nquestion: {question}\n")
    for block in response.content:
        if block.type == "text":
            print(block.text)
    print(f"\n({len(transcript)} messages were sent to the model)")
