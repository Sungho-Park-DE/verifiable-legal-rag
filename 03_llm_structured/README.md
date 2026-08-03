# 03 — LLM structured outputs + tool-use loop

Goal: the two LLM-API skills that carry a legaltech hackathon — getting
validated structured data out of documents, and writing the agent loop
that frameworks hide from you.

## Run order

Prerequisite: the project-02 index must exist (`02_rag/build_index.py`) —
the agent's search tool queries it.

```bash
.venv/bin/python 03_llm_structured/verify.py        # works WITHOUT an API key
# with a key (hackathon sponsor credits):
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/python 03_llm_structured/structured_extract.py
.venv/bin/python 03_llm_structured/tool_use_loop.py "Is there a cap on damages?"
.venv/bin/python 03_llm_structured/verify.py        # now also runs live checks
```

## What to study, in order

1. `structured_extract.py` — schema-first extraction. The Pydantic model
   IS the prompt engineering: field names, types, `Literal` enums, and
   field descriptions all steer the model. `messages.parse()` guarantees
   the return value validates — no JSON parsing code exists in this file.
2. `tool_use_loop.py` — read `run_agent_loop` until you can rewrite it
   from memory (~25 lines). Note the two API rules: echo the assistant
   turn verbatim, and return every `tool_result` (matching `tool_use_id`)
   in one user message.
3. `verify.py` — see `FakeClient`: because the loop takes `client` as a
   parameter, the LLM can be replaced with a script while the tool still
   hits the real project-02 index. Separating "loop mechanics" from
   "model behavior" is also how you test agents in a real project.

## Ideas to retain

* Project 02 was RAG: **we** decided what to retrieve. This is agentic
  RAG: the **model** decides what to search, and can search repeatedly.
  That one difference is most of what "agent" means.
* Tool `description`s are decision criteria, not documentation — say
  WHEN to call the tool ("call this before answering ANY question about
  the contract"), not just what it does.
* `strict: true` on the tool + `additionalProperties: false` guarantees
  the tool input validates — the tool-side analog of structured outputs.

## Experiments worth trying

* Ask something the contract doesn't cover ("What is the SLA uptime?")
  and check the model says so instead of guessing — that behavior comes
  from one sentence in `SYSTEM`; delete it and compare.
* Add a second tool (e.g. `get_statute(paragraph)` returning a canned
  BGB text) and watch the model chain both tools in one run.
* Swap `MODEL` to a cheaper model and compare extraction quality on
  `structured_extract.py`.
