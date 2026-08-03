"""Generate the sample contract PDF used by all three projects.

Run:      .venv/bin/python data/make_sample_pdf.py
Creates:  data/sample_agreement.pdf

Why generate instead of download: the repo stays self-contained and
reproducible. To practice on a real contract later, drop any PDF into
data/ (e.g. one of the 510 real contracts in the CUAD dataset,
https://arxiv.org/pdf/2103.06268) and point the scripts at it.

The clause set below is deliberately chosen so the RAG project (02) has
distinct, findable retrieval targets: a termination notice period, a
liability cap with a number, a governing-law clause, etc.
"""

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).parent / "sample_agreement.pdf"

# (heading, body) pairs. Plain ASCII only: fpdf2's built-in core fonts
# are latin-1, so we write "EUR" instead of the euro sign.
CLAUSES = [
    (
        "1. Parties and purpose",
        "This Service Agreement (the 'Agreement') is entered into between "
        "Aquila Analytics GmbH, Arcisstrasse 21, 80333 Munich, Germany (the "
        "'Provider') and Borealis Logistik AG, Speicherstadt 4, 20457 Hamburg, "
        "Germany (the 'Customer'). The Provider agrees to develop and operate "
        "a document-analysis platform for the Customer's freight contracts.",
    ),
    (
        "2. Definitions",
        "'Confidential Information' means any non-public business, technical "
        "or legal information disclosed by either party, whether in writing, "
        "orally or by inspection. 'Deliverables' means the software, models "
        "and documentation listed in Annex A. 'Effective Date' means 1 "
        "September 2026.",
    ),
    (
        "3. Fees and payment",
        "The Customer shall pay the Provider a monthly service fee of EUR "
        "12,500, invoiced at the beginning of each calendar month and payable "
        "within 14 days of receipt of a proper invoice. Late payments accrue "
        "interest at 9 percentage points above the base rate pursuant to "
        "Section 288 BGB.",
    ),
    (
        "4. Confidentiality",
        "Each party shall use the other party's Confidential Information "
        "solely for the performance of this Agreement and shall protect it "
        "with at least the same degree of care it applies to its own "
        "confidential information, but no less than reasonable care. This "
        "obligation survives termination of the Agreement for a period of "
        "five (5) years.",
    ),
    (
        "5. Data protection",
        "The parties shall comply with the EU General Data Protection "
        "Regulation (GDPR). Where the Provider processes personal data on "
        "behalf of the Customer, the parties shall conclude a data processing "
        "agreement pursuant to Art. 28 GDPR before any such processing "
        "begins. Personal data shall be processed exclusively within the "
        "European Economic Area.",
    ),
    (
        "6. Term and termination",
        "This Agreement commences on the Effective Date and runs for an "
        "initial term of twenty-four (24) months. It renews automatically for "
        "successive twelve (12) month periods unless either party gives "
        "written notice of termination at least thirty (30) days before the "
        "end of the then-current term. The right to terminate for good cause "
        "(Section 314 BGB) remains unaffected.",
    ),
    (
        "7. Limitation of liability",
        "The Provider's aggregate liability under this Agreement is capped at "
        "EUR 100,000 per contract year. The cap does not apply to damages "
        "caused by intent or gross negligence, to injury of life, body or "
        "health, or to claims under the German Product Liability Act. "
        "Liability for loss of profit is excluded.",
    ),
    (
        "8. Non-solicitation",
        "During the term of this Agreement and for twelve (12) months "
        "thereafter, neither party shall actively solicit for employment any "
        "employee of the other party who was directly involved in the "
        "performance of this Agreement. Job advertisements addressed to the "
        "general public are not considered active solicitation.",
    ),
    (
        "9. Assignment",
        "Neither party may assign this Agreement or any rights hereunder "
        "without the prior written consent of the other party, except that "
        "either party may assign to an affiliate or in connection with a "
        "merger or sale of substantially all of its assets.",
    ),
    (
        "10. Governing law and jurisdiction",
        "This Agreement is governed by the laws of the Federal Republic of "
        "Germany, excluding its conflict-of-law rules and the UN Convention "
        "on Contracts for the International Sale of Goods (CISG). Exclusive "
        "place of jurisdiction is Munich.",
    ),
]

# A small fee table so project 01 can show how table content comes
# through in plain text extraction vs. markdown extraction.
FEE_TABLE = [
    ("Item", "Fee (EUR)", "Billing"),
    ("Platform operation", "12,500 / month", "monthly"),
    ("Onboarding (one-off)", "20,000", "on signature"),
    ("Additional model training", "1,800 / day", "per use"),
]


def block(pdf: FPDF, height: float, text: str) -> None:
    """Full-width paragraph. fpdf2's multi_cell defaults to new_x='RIGHT',
    so after a w=0 (full-width) cell the cursor would sit on the right
    margin and the NEXT w=0 cell would have zero width and crash. Always
    return the cursor to the left margin instead."""
    pdf.multi_cell(0, height, text, new_x="LMARGIN", new_y="NEXT")


def main() -> None:
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    pdf.set_font("Helvetica", style="B", size=16)
    block(pdf, 9, "Service Agreement")
    pdf.set_font("Helvetica", size=10)
    block(pdf, 6, "between Aquila Analytics GmbH and Borealis Logistik AG")
    pdf.ln(4)

    for heading, body in CLAUSES:
        pdf.set_font("Helvetica", style="B", size=12)
        block(pdf, 7, heading)
        pdf.set_font("Helvetica", size=11)
        block(pdf, 6, body)
        pdf.ln(3)

    pdf.set_font("Helvetica", style="B", size=12)
    block(pdf, 7, "Annex A: Fee schedule")
    pdf.set_font("Helvetica", size=10)
    col_widths = (80, 50, 40)
    for row in FEE_TABLE:
        for value, width in zip(row, col_widths):
            pdf.cell(width, 7, value, border=1)
        pdf.ln()

    pdf.output(str(OUT))
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
