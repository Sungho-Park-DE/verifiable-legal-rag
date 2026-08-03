"""Verification for project 01.

Run:  .venv/bin/python 01_pdf_parsing/verify.py

Checks that the two extraction scripts actually produced what the
comments claim: plain text has the CONTENT but no STRUCTURE; markdown
has both. Exits non-zero on the first failed check.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PLAIN = ROOT / "01_pdf_parsing" / "out_plain.txt"
MD = ROOT / "data" / "sample_agreement.md"

failures = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global failures
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail and not ok else ""))
    if not ok:
        failures += 1


def main() -> None:
    check("plain text output exists", PLAIN.exists())
    check("markdown output exists", MD.exists())
    if not (PLAIN.exists() and MD.exists()):
        sys.exit(1)

    plain = PLAIN.read_text(encoding="utf-8")
    md = MD.read_text(encoding="utf-8")

    # 1. Content survived in both: key facts from the source contract.
    for needle in ("thirty (30) days", "EUR 100,000", "Art. 28 GDPR", "Munich"):
        check(f"plain text contains {needle!r}", needle in plain)
        check(f"markdown contains {needle!r}", needle in md)

    # 2. Structure exists ONLY in the markdown: heading markers and a
    #    pipe table. This is the whole point of the project.
    md_headings = [l for l in md.splitlines() if l.lstrip().startswith("#")]
    check("markdown has >= 10 headings (one per clause)", len(md_headings) >= 10)
    check("plain text has no markdown headings",
          not any(l.lstrip().startswith("#") for l in plain.splitlines()))
    check("markdown contains a pipe table (fee schedule)",
          any(l.lstrip().startswith("|") for l in md.splitlines()))

    # 3. The termination clause is findable as a section in markdown.
    check("a heading mentions termination",
          any("termination" in h.lower() for h in md_headings))

    print()
    if failures:
        print(f"{failures} check(s) failed")
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
