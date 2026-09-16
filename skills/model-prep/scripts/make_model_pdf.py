#!/usr/bin/env python3
"""Render a Vanguard model portfolio page as a styled PDF.

Two modes, one script:

    mode: "advisor"   the advisor one-pager (reference/one-pager.md)
    mode: "client"    the client one-page takeaway (reference/client-output.md)

Nothing internal ("Model Prep", "Advisor Draft", "Client-Ready", tag vocabulary,
field names) appears in the output. Which format it is goes in the chat message,
not in the file.

Usage:
    python3 make_model_pdf.py content.json out.pdf

The JSON shape mirrors the two reference formats:

{
  "mode": "advisor",                       # "advisor" (default) or "client"
  "title": "Core Series - Client Review",
  "subtitle": "Prepared September 2026",   # optional, neutral
  "matched_to": "Long-term growth - 60/40 - ETFs - index funds only",
                                           # advisor mode only; the compliance
                                           # breadcrumb recording that the
                                           # advisor set the criteria
  "intro": "One or two plain sentences.",  # client mode: what a model is
  "models_table": {                        # optional: the matched shortlist
    "headers": ["Model", "Equity / FI split", "Vehicle", "How it's managed"],
    "rows": [["Core Series", "60 / 40", "ETF build", "Index funds; reviewed annually"]]
  },
  "scope_note": "Performance, yield, and asset-class breakdowns are not part of
                 the model data reported here.",
  "sections": [                            # the body: narrative, table, or both
    {"heading": "What's inside (Core Series)",
     "body": "4-6 sentences, every clause traceable to the name, the split, or
              the holdings.",
     "table": {"caption": "60% Equity - 40% Fixed Income",
               "headers": ["Ticker", "Fund", "%"],
               "rows": [["BND", "Vanguard Total Bond Market ETF", "27.4%"]],
               "note": "Weights are percentages of the portfolio and sum to 100."}}
  ],
  "practice_value": ["2-4 advisor-only bullets"],   # advisor mode ONLY;
                                                    # an error in client mode
  "open_items": ["2-4 bullets: what to confirm before implementing"],
  "link": "https://advisors.vanguard.com/portfolio-construction-tools/model-portfolios/#multi-asset",
                                           # advisor mode only - login-walled
  "next_step": "A neutral, non-directive invitation to discuss.",
  "disclosures": ["Provider disclaimer, verbatim.", "As-of date."]
}

Only "title" is required; everything else degrades gracefully.

Two boundaries are enforced here rather than left to judgment, because both are
compliance controls rather than styling:

  * practice_value is refused in client mode. Practice economics - time saved,
    onboarding smaller accounts, book valuation - is advisor-only.
  * link is dropped in client mode. advisors.vanguard.com is behind an advisor
    login, so a client following it hits a wall.
"""

import json
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# Palette, type scale and table-cell handling are the plugin's shared PDF
# styling, not this script's own choices. If another skill in the plugin ships
# a PDF renderer, keep these values identical across them so the pages look
# like they came from the same place — a fix here usually belongs there too.
ACCENT = colors.HexColor("#d97757")   # burnt orange: rules, accents
BRAND = colors.HexColor("#96151d")    # Vanguard red: logo only
INK = colors.HexColor("#1a1a1a")
BODY = colors.HexColor("#53493a")
MUTED = colors.HexColor("#666666")
FAINT = colors.HexColor("#999999")
HAIRLINE = colors.HexColor("#eeeeee")
TINT = colors.HexColor("#f5efec")

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"
FONT_I = "Helvetica-Oblique"

styles = {
    "title": ParagraphStyle("title", fontName=FONT_B, fontSize=19, leading=24,
                            textColor=INK, spaceAfter=14),
    "subtitle": ParagraphStyle("subtitle", fontName=FONT, fontSize=9.5, leading=13,
                               textColor=FAINT, spaceAfter=2),
    "matched": ParagraphStyle("matched", fontName=FONT, fontSize=9, leading=13,
                              textColor=MUTED),
    "intro": ParagraphStyle("intro", fontName=FONT, fontSize=10.5, leading=16,
                            textColor=BODY, spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName=FONT_B, fontSize=11.5, leading=15,
                         textColor=INK, spaceAfter=5),
    "body": ParagraphStyle("body", fontName=FONT, fontSize=10, leading=15,
                           textColor=BODY, alignment=TA_LEFT),
    "bullet": ParagraphStyle("bullet", fontName=FONT, fontSize=10, leading=15,
                             textColor=BODY, leftIndent=12, bulletIndent=2,
                             spaceAfter=3),
    "caption": ParagraphStyle("caption", fontName=FONT_I, fontSize=9, leading=12,
                              textColor=MUTED, spaceAfter=3),
    "note": ParagraphStyle("note", fontName=FONT_I, fontSize=8, leading=11,
                           textColor=FAINT, spaceBefore=3),
    "scope": ParagraphStyle("scope", fontName=FONT, fontSize=9, leading=13,
                            textColor=MUTED),
    "advisoronly": ParagraphStyle("advisoronly", fontName=FONT_B, fontSize=8,
                                  leading=11, textColor=ACCENT, spaceAfter=6),
    "next": ParagraphStyle("next", fontName=FONT, fontSize=10, leading=15,
                           textColor=BODY, spaceBefore=14),
    "disc": ParagraphStyle("disc", fontName=FONT, fontSize=7.5, leading=10.5,
                           textColor=FAINT, spaceAfter=4),
    # Table cells. These exist so cell text is a Paragraph rather than a bare
    # string: reportlab does not wrap a string cell, it draws it as one line
    # that runs straight over the next column. See _data_table.
    "th": ParagraphStyle("th", fontName=FONT_B, fontSize=9, leading=12,
                         textColor=INK),
    "td": ParagraphStyle("td", fontName=FONT, fontSize=9, leading=12,
                         textColor=BODY),
}

# Matches a real XML/HTML entity, so bare ampersands can be escaped without
# mangling an intentional &mdash; or &amp;.
_ENTITY = re.compile(r"&(?:#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);")


def _markup_safe(text):
    """Escape bare ampersands, leaving real entities intact.

    Needed because cell text goes through the Paragraph parser now, and the
    characteristics column routinely carries a literal ampersand ("ETF & MF")
    which is not valid markup. Inline tags the callers are told they can use —
    <b>, <i>, <br/> — are deliberately left alone.
    """
    out, pos = [], 0
    for m in _ENTITY.finditer(text):
        out.append(text[pos:m.start()].replace("&", "&amp;"))
        out.append(m.group(0))
        pos = m.end()
    out.append(text[pos:].replace("&", "&amp;"))
    return "".join(out)

# Vanguard's internal taxonomy — field and parameter names. These are how the
# work gets done, not content, and they never belong on a rendered page in
# either mode. See "Say what it means, not how it's tagged" in SKILL.md.
BANNED_ALWAYS = (
    "isdynamic", "isfixedincome", "subassettype", "sleevecount",
    "characteristics[]", "series_type", "cardname",
)

# Labels that belong to the advisor's side of the conversation. Checked in
# client mode only, so a copy-paste from chat can't carry one into the file the
# client receives — the advisor's own page may name itself.
BANNED_IN_CLIENT = (
    "model prep", "advisor draft", "advisor-only", "client-ready",
    "one-pager", "matched to", "not for client distribution",
    "active-passive", "active/passive", "dynamic series",
)


class Rule(Flowable):
    """A hairline separator."""

    def __init__(self, width, color=HAIRLINE, thickness=0.6, space=10):
        Flowable.__init__(self)
        self.width, self.color, self.thickness, self.space = width, color, thickness, space
        self.height = space

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space / 2, self.width, self.space / 2)


def _boxed(inner, avail, bg=colors.white, left_accent=True, pad=11):
    """A bordered card with an optional accent rule down the left edge."""
    t = Table([[inner]], colWidths=[avail])
    cmds = [
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), pad + (3 if left_accent else 0)),
        ("RIGHTPADDING", (0, 0), (-1, -1), pad),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
    ]
    if left_accent:
        cmds += [("BOX", (0, 0), (-1, -1), 0.6, HAIRLINE),
                 ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT)]
    t.setStyle(TableStyle(cmds))
    return t


def _data_table(spec, avail):
    """A comparison or holdings table. No row highlighting — highlighting one
    row would imply a ranking, and this skill matches rather than ranks."""
    headers = spec.get("headers", [])
    rows = spec.get("rows", [])
    if not headers and not rows:
        return []

    widths = spec.get("widths")
    if widths:
        total = float(sum(widths))
        col_widths = [avail * (w / total) for w in widths]
    else:
        col_widths = [avail / len(headers)] * len(headers)

    # Every cell is a Paragraph, never a bare string. A string cell does not
    # wrap — reportlab lays it out as a single line and lets it overflow into
    # the neighbouring column, which reads as overlapping text rather than as a
    # too-narrow column. Wrapping also means a bad `widths` ratio degrades into
    # a taller row instead of a corrupted one.
    head = [Paragraph(_markup_safe(str(h)), styles["th"]) for h in headers]
    body = [[Paragraph(_markup_safe(str(c)), styles["td"]) for c in row]
            for row in rows]

    t = Table([head] + body, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TINT),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, TINT]),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, HAIRLINE),
    ]))

    out = []
    if spec.get("caption"):
        out.append(Paragraph(spec["caption"], styles["caption"]))
    out.append(t)
    if spec.get("note"):
        out.append(Paragraph(spec["note"], styles["note"]))
    return out


def _bullets(items):
    return [Paragraph(i, styles["bullet"], bulletText="•") for i in items]


def validate(data):
    """Raise on anything that is a boundary violation rather than a style slip."""
    mode = data.get("mode", "advisor")
    if mode not in ("advisor", "client"):
        raise ValueError(f'mode must be "advisor" or "client", got {mode!r}')
    client = mode == "client"

    if client:
        if data.get("practice_value"):
            raise ValueError(
                'practice_value is advisor-only and cannot appear in a client '
                'page. Practice economics — time saved, onboarding smaller '
                'accounts, book valuation — is not a client conversation. '
                'Drop the field; do not rewrite it into the narrative.')
        if data.get("matched_to"):
            raise ValueError(
                'matched_to is the advisor-facing criteria breadcrumb and does '
                'not belong on a client page. Drop the field.')

    visible = json.dumps({k: v for k, v in data.items()
                          if k not in ("mode",)}).lower()
    for term in BANNED_ALWAYS:
        if term in visible:
            raise ValueError(
                f'{term!r} is an internal field name and must not appear on a '
                'rendered page. Translate it to what it means for the advisor.')
    if client:
        for term in BANNED_IN_CLIENT:
            if term in visible:
                raise ValueError(
                    f'{term!r} is an advisor-side label or series tag and must '
                    'not appear on a client page. Say which format it is in the '
                    'chat message, and describe a series rather than naming it.')
    return mode


def build(data, out_path):
    mode = validate(data)
    client = mode == "client"

    doc = BaseDocTemplate(
        out_path, pagesize=LETTER,
        leftMargin=0.85 * inch, rightMargin=0.85 * inch,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch,
        title=data.get("title", "Model Portfolio Summary"),
        author="Vanguard",
    )
    avail = doc.width
    doc.addPageTemplates([
        PageTemplate(id="main", frames=[
            Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
        ])
    ])

    story = [Paragraph(data.get("title", "Model Portfolio Summary"), styles["title"])]

    if data.get("subtitle"):
        story.append(Paragraph(data["subtitle"], styles["subtitle"]))
        story.append(Spacer(1, 6))

    # The "Matched to" breadcrumb is doing compliance work: it records that the
    # advisor set the criteria and the skill applied them. Advisor pages only.
    if data.get("matched_to") and not client:
        story.append(_boxed(
            [Paragraph("<b>Matched to:</b> " + data["matched_to"], styles["matched"])],
            avail, bg=TINT, left_accent=False, pad=9))
        story.append(Spacer(1, 10))

    if data.get("intro"):
        story.append(Paragraph(data["intro"], styles["intro"]))
        story.append(Rule(avail))

    if data.get("models_table"):
        story.extend(_data_table(data["models_table"], avail))
        story.append(Spacer(1, 6))

    # Scope note sits directly under the table so the absence of performance,
    # yield and asset-class figures reads as scope rather than omission.
    if data.get("scope_note"):
        story.append(Paragraph(data["scope_note"], styles["scope"]))
        story.append(Spacer(1, 10))

    for sec in data.get("sections", []):
        inner = []
        if sec.get("heading"):
            inner.append(Paragraph(sec["heading"], styles["h2"]))
        if sec.get("body"):
            inner.append(Paragraph(sec["body"], styles["body"]))
        if sec.get("bullets"):
            inner.append(Spacer(1, 4))
            inner.extend(_bullets(sec["bullets"]))
        if sec.get("table"):
            inner.append(Spacer(1, 8))
            inner.extend(_data_table(sec["table"], avail - 28))
        story.append(KeepTogether(_boxed(inner, avail)))
        story.append(Spacer(1, 9))

    if data.get("practice_value"):
        inner = [Paragraph("Why this fits your practice", styles["h2"]),
                 Paragraph("ADVISOR-ONLY — NOT FOR CLIENT DISTRIBUTION",
                           styles["advisoronly"])]
        inner.extend(_bullets(data["practice_value"]))
        story.append(Spacer(1, 3))
        story.append(KeepTogether(_boxed(inner, avail, bg=TINT)))
        story.append(Spacer(1, 9))

    if data.get("open_items"):
        heading = "Where we go from here" if client else "Open items"
        inner = [Paragraph(heading, styles["h2"])]
        inner.extend(_bullets(data["open_items"]))
        story.append(KeepTogether(_boxed(inner, avail, left_accent=False)))
        story.append(Spacer(1, 9))

    # advisors.vanguard.com is login-walled, so it never reaches a client page.
    if data.get("link") and not client:
        story.append(Paragraph(
            "Yield, performance, risk statistics and the allocation breakdown "
            f'are on Vanguard\'s model portfolios page: <font color="#d97757">'
            f'{data["link"]}</font>', styles["scope"]))
        story.append(Spacer(1, 6))

    if data.get("next_step"):
        story.append(Paragraph(data["next_step"], styles["next"]))

    if data.get("disclosures"):
        story.append(Spacer(1, 24))
        story.append(Rule(avail))
        for d in data["disclosures"]:
            story.append(Paragraph(d, styles["disc"]))

    doc.build(story)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1]) as fh:
        data = json.load(fh)
    try:
        build(data, sys.argv[2])
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)
    print(f"wrote {sys.argv[2]}")


if __name__ == "__main__":
    main()
