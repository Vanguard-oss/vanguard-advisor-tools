# Advisor one-pager — format

The default Model Prep deliverable. Advisor-facing. Contains a section that must never appear in client material.

**Delivered as text in chat first, then as a PDF** — see "Delivery" in step 5 of SKILL.md and "Generating the PDF" at the bottom of this file. The advisor almost always wants to reword something, and editing wants text.

## Before anything in this file

**Two things must already have happened, in this order:** the compliance disclosure printed verbatim in chat, and the advisor's confirmation returned through the question tool. Both are specified in step 5 of SKILL.md.

**The gate is not client-material-only.** This page is a generated document that goes into client files and gets handed to colleagues, and it carries an advisor-only section that must never reach a client — so it sits behind the same notice as anything else this skill produces.

**If either part is missing, stop and go do it.** Reaching this file is not itself authorization — it's common to arrive here because the advisor asked for the artifact directly ("just build the one-pager", "make it a PDF"), and that request is not a substitute for the gate. Print the notice, call the confirmation question, and only then work through what follows. Nothing on this page — including the output and format questions — may be asked ahead of that disclosure.

**It is one page.** That's not a name, it's a constraint: if the text version is running past a page, the narrative is too long or too many sleeves are being shown. Cut before you render — a three-page "one-pager" is the same failure as a sprawling chat reply, and the length tiers in SKILL.md's Default Response Structure apply here too.

## Structure

```
<series name> — Client Review
<The title names the series, never this skill. "Core Series — Client Review",
 not "Model Prep — Client Review": step 5 of SKILL.md forbids internal labels
 in both modes, and the title is the most visible place to leak one. Say which
 format it is in your chat message instead.>

Matched to: <the criteria the advisor stated, in the advisor's own terms>
            e.g. Long-term growth · 60/40 · ETFs and mutual funds · blend of
                 active and index · allocation reviewed a few times a year

## Matched models
<table: Model | Equity/FI split | Wtd. expense ratio | Characteristics>
<"Wtd. expense ratio" is the expense ratio of the sleeve named in the split
 column — never a series-level figure and never an average across sleeves.
 See "Cost" in SKILL.md.

 "Characteristics" carries the tags as published, `·`-separated, per the skill
 brief's sample. It is a compact record of what the series is; the plain-language
 explanation of what those tags mean belongs in "What's inside", not here.

 Add a "Vehicle" or "How it's managed" column instead of, or alongside,
 Characteristics when the advisor's criteria make one of them the salient
 difference — but keep the table to four or five columns. A one-pager column
 that wraps to three lines has stopped being a table.>

<one line noting performance, yield and asset-class breakdowns are not part of
 the model data reported here>

## What's inside (<model name>)
<narrative paragraph: what the model is built from, the equity/FI split and what
 that means, how it's managed, and what it costs to implement. Prose, not
 bullets — this is the interpretation the table can't carry. Keep it to 4-6
 sentences: this is a one-pager, and a 250-word block stops being scannable.
 Push the rest into Open items.

 This is also where the characteristics tags get *explained* rather than listed —
 "blends actively managed and index funds, with the allocation revisited a few
 times a year" instead of "Active/Passive · Dynamic". The column above carries
 the tags; this paragraph carries the meaning.

 There is no portfolio description in the data. Build this from the series name,
 the split, the holdings beneath it, and the expense ratio — every clause should
 be traceable to one of those. Do not describe Vanguard's investment process,
 mandate, or how allocation decisions get made; none of that is available here.>

<per-sleeve holdings table: Ticker | Fund | % — one table per sleeve, bond funds
 before stock funds, 0% weights included, with that sleeve's weighted average
 expense ratio stated in the caption or a note beneath. Markdown tables, same as
 everywhere else — the MCP directive asks for box-drawing characters and that
 part is ignored in every surface, because the chat clients render markdown and
 turn box-drawing into reflowed raw text. See the standing rules in SKILL.md.>

## Why this fits your practice
Advisor-only — not for client distribution.
<2–4 bullets from the advisor-value layer>

## Open items for the advisor
<2–4 bullets: what to confirm or review before implementing>
```

## Rules

**The "Matched to" breadcrumb is doing compliance work.** It records that the advisor set the criteria and the skill applied them. Keep it — it's what makes the shortlist a match rather than a recommendation. Write it in the advisor's own words, not in Vanguard's tag vocabulary; the compliance value is in recording *that* they chose, and plain phrasing records it just as well.

**The title names the series, not the skill.** `Core Series — Client Review`. Not `Model Prep`, not `Advisor Draft`, not `Client-Ready` — step 5 of SKILL.md forbids those in *both* modes, and the title line is where they leak, because it's the one piece of text that feels like a header rather than content. This page is advisor-facing, which makes it easy to assume the internal name is fine here. It isn't: the advisor puts this in a client file.

**No internal vocabulary anywhere on this page — with one exception.** No field names, no parameter names, no explanation of how Vanguard categorizes its models. This is a page an advisor may put in front of a client's file or hand to a colleague, and it should read as investment writing, not a systems export.

**The exception is the `Characteristics` column**, which carries the tags as published, per the skill brief's sample one-pager. That's a factual column on an advisor-facing page. It is not licence to write tag strings into the prose — see "Say what it means, not how it's tagged" in SKILL.md, and note that the "Matched to" breadcrumb still uses the advisor's own words, not the taxonomy.

**Table ordering must not imply ranking.** Don't put a "best fit" first, and don't sort on any dimension that reads as better-to-worse. Use the order the tool returned, or alphabetical. No highlighting, bolding, or callouts on one row.

**Only the permitted fields appear.** No performance column, no yield, and **no asset-class breakdown in any form** — including one summed from the holdings table on this same page. See the Data boundary in SKILL.md. The note about their absence goes directly under the table so it reads as scope, not omission.

**The cost column is a real field — and it is per sleeve.** `sleeves[].expenseRatio` is Vanguard's own weighted average for that sleeve, and the brief lists it as one-pager content. Two things it must not become: an average across a series' sleeves, or a figure presented as "the series' expense ratio." If the page shows the 60/40 version, the ratio in that row is the 60/40 version's. Never compute one from the underlying fund weights. See "Cost" in SKILL.md.

**And a cost column is not a ranking column.** With two models side by side, the cheaper row is visually the answer, which is why the ordering rule above matters more once this column exists. State both figures, note the difference if the advisor is comparing, and leave the trade-off to them — the one-pager records a match, not a verdict.

**"Why this fits your practice" carries its advisor-only label every time.** The label is not decoration; it's the control that keeps practice-economics content out of client hands. Never include this section — or anything derived from it — in client-facing output.

**"Open items" are considerations, not instructions.** "Confirm the split against the client's objectives and existing holdings" is right. "Move the client to the 60/40 series" is not.

**And they are not a place to park a data complaint.** This section attracts them, because a note about the data feels like something to flag and this is the flagging section. It isn't. *"The data returned this fund's name incorrectly"* and *"this build is labeled ETF but holds Admiral Shares"* are both feedback for Vanguard, not actions for the advisor — the second one has reached a real page. Every open item is something **the advisor does about the client**. See "Observations about the data are not advisor content" in SKILL.md.

**Where an open item is a missing figure, give the advisor the link.** Yield, performance (since-inception and 3-year), 3-year standard deviation, the allocation breakdown, and the model's stated objective all live on Vanguard's model portfolios page — include it once here rather than leaving the advisor to search. Cost is not on that list any more; it's on the page above:

```
https://advisors.vanguard.com/portfolio-construction-tools/model-portfolios/#multi-asset
```

Drop the `#multi-asset` anchor for a fixed-income series. **Never build a per-series URL** — the data carries no URL and the internal ids don't map to page slugs, so a constructed link is a confident dead end. Name the series in the sentence instead. See "Linking out" in SKILL.md.

**Include the provider disclaimer verbatim** if one came back with the data.

## Worked example

Illustrative format only; figures are placeholders.

> **Core Series — Client Review**
>
> Matched to: Long-term growth · 60/40 · ETFs · index funds only · allocation held steady rather than shifted
>
> **Matched models**
>
> | Model | Equity / FI split | Wtd. expense ratio | Characteristics |
> |---|---|---|---|
> | Core Series | 60 / 40 | 0.04% | Growth · ETF · Mutual Funds · Strategic · Passive |
> | S&P Series | 60 / 40 | 0.04% | Growth · ETF · Mutual Funds · Strategic · Passive |
>
> Each expense ratio is that version's own weighted average. Performance, yield, and asset-class breakdowns are not part of the model data reported here.
>
> **What's inside (Core Series)**
>
> This version is built from five broad Vanguard funds — total U.S. and international stock, total U.S. and international bond, and a small cash position — at a 60/40 equity/fixed-income split. The holdings are index funds, so the allocation rather than security selection is doing the work. The mix is held steady and revisited about once a year rather than shifted a few times a year, which means less portfolio turnover than a dynamic approach. The weighted average expense ratio for this version is 0.04%, and it happens to be the same across every version in this series — which is not true of every series, so it's stated per version rather than once.
>
> *60% Equity - 40% Fixed Income · weighted average expense ratio 0.04%*
>
> | Ticker | Fund | % |
> |---|---|---|
> | BND | Vanguard Total Bond Market ETF | 27.4% |
> | BNDX | Vanguard Total International Bond ETF | 11.8% |
> | Cash | Money Market Fund | 2.0% |
> | VTI | Vanguard Total Stock Market ETF | 35.3% |
> | VXUS | Vanguard Total International Stock ETF | 23.5% |
>
> *Weights are percentages of the portfolio and sum to 100.*
>
> *(Construction notes for whoever maintains this format, not lines to reproduce on the page: bond funds precede stock funds per the presentation directive on the response; weights are shares of the whole sleeve; use the fund name the data returns, including for `Cash`.)*
>
> **Why this fits your practice**
>
> *Advisor-only — not for client distribution.*
>
> - Outsourcing construction and rebalancing can free meaningful time each week for planning and client relationships.
> - A consistent, repeatable approach makes it easier to onboard smaller or growth-potential accounts and keep similar clients aligned.
> - A uniform investment process supports oversight today and makes a book easier to value and transfer over time.
>
> **Open items for the advisor**
>
> - Confirm the split and vehicle preference against the client's objectives and existing holdings.
> - Review the underlying funds and any tax considerations before implementing.

Note what the example does *not* do: it doesn't say which of the two models to use, doesn't rank them, and doesn't claim anything about Vanguard's investment process or mandate — because the data carries no portfolio description, every clause in that paragraph traces back to the series name, the split, the expense ratio, or the holdings table underneath it. In particular, it lists VTI and VXUS with weights without ever summing them into a "35% U.S. / 23% international equity" statement, and it doesn't restate them as a share of the equity sleeve either. Both are the reconstruction boundary this format exists to hold.

Two more things it doesn't do, both of which have gone wrong in real sessions. It doesn't pick a winner on cost — the two ratios happen to be equal here, but with 0.04% against 0.03% the page still states both and stops. And it puts the tags in the column while the paragraph explains what they *mean*; the paragraph never says "Strategic · Passive."

A reader who knows what VTI and VXUS are can derive the breakdown from this table anyway, and that's acceptable — what's restricted is Morningstar's look-through figure, not the information. Weights belong here. See the Data boundary in SKILL.md.

## Generating the PDF

Once the advisor is happy with the text version, render it with the bundled script. Don't hand-roll a layout — the styling, page breaks and palette are already encoded, and they follow the plugin's shared PDF styling so every skill in it produces pages that look like they came from the same place.

```bash
python3 scripts/make_model_pdf.py content.json "Core Series - Client Review.pdf"
```

The interpreter name is OS-specific: `python3` on macOS and Linux, `py -3` or `python` on Windows. Use whichever resolves on this machine.

`content.json`, for the advisor page:

```json
{
  "mode": "advisor",
  "title": "Core Series — Client Review",
  "subtitle": "Prepared September 2026",
  "matched_to": "Long-term growth · 60/40 · ETFs · index funds only · reviewed about annually",
  "models_table": {
    "headers": ["Model", "Equity / FI split", "Wtd. expense ratio", "Characteristics"],
    "rows": [["Core Series", "60 / 40", "0.04%", "Growth · ETF · Mutual Funds · Strategic · Passive"]],
    "widths": [24, 18, 18, 40]
  },
  "scope_note": "Each expense ratio is that version's own weighted average. Performance, yield, and asset-class breakdowns are not part of the model data reported here.",
  "sections": [
    {
      "heading": "What's inside (Core Series)",
      "body": "4–6 sentences, every clause traceable to the series name, the split, the expense ratio, or the holdings.",
      "table": {
        "caption": "60% Equity - 40% Fixed Income · weighted average expense ratio 0.04%",
        "headers": ["Ticker", "Fund", "%"],
        "rows": [["BND", "Vanguard Total Bond Market ETF", "27.4%"]],
        "widths": [14, 66, 20],
        "note": "Weights are percentages of the portfolio and sum to 100."
      }
    }
  ],
  "practice_value": ["2–4 advisor-only bullets"],
  "open_items": ["2–4 bullets: what to confirm or review before implementing"],
  "link": "https://advisors.vanguard.com/portfolio-construction-tools/model-portfolios/#multi-asset",
  "disclosures": ["Model data as of 08/31/2026.", "Provider disclaimer, verbatim."]
}
```

Only `title` is required; everything else degrades gracefully. Notes:

- **`mode` is the boundary, not a style switch.** `"advisor"` renders `practice_value` under its `ADVISOR-ONLY — NOT FOR CLIENT DISTRIBUTION` label and includes the advisors.vanguard.com link. `"client"` **refuses** `practice_value` and `matched_to` outright — an error, not a silently dropped field — and drops the link, because it's behind an advisor login. Use `reference/client-output.md` for that page.
- **`widths` is a relative ratio**, not points or inches. Omit it for even columns; supply it when one column carries much longer text than the others (the "How it's managed" phrase, or a fund name). **Cell text wraps**, so a column that's too narrow for its content costs row height rather than breaking the table — size the ratio against the longest cell, and don't try to make it exact. A wrapped header is normal and looks deliberate; "Wtd. expense ratio" over two lines is fine.
- **Keep the split cell to the label alone.** `50–70% equity` — not `50–70% equity (Growth version)`. That cell is the narrowest one carrying real text, the version is already named in the section heading below it, and doubling it up is what pushed this table into a visible overlap before the script wrapped cells. Same principle for any column: the table carries short factual values, and anything that needs a parenthetical belongs in the narrative.
- **One `sections` entry per sleeve you're showing**, with the sleeve label as the table `caption`. Bond funds before stock funds, 0% weights included, `null` weights left out entirely. Showing every sleeve in a series buries the one that matters — see the sleeve-scope gate in step 2b of SKILL.md.
- **No row highlighting exists in the script, deliberately.** Emphasising one row would read as a ranking, and this skill matches rather than ranks.
- **Internal field names are rejected in both modes** — `isDynamic`, `subAssetType`, `cardName`, `series_type` and friends. If one trips the check, the fix is to translate it to what it means, not to work around it.
- Basic inline tags work in `body` and other text fields — `<b>`, `<i>`, `<br/>`, `&mdash;`. Use `<br/><br/>` for a paragraph break within a section.
- **No internal labels in the file.** Say which format it is in your chat message instead.

**If the script can't run** (no Python, missing `reportlab`), deliver the page as formatted text in chat and tell the advisor what they lost rather than what broke: *"I can't generate the PDF on this machine — here's the full page as text."* No package names, no interpreter names, no error text; see "Nothing an engineer would care about reaches the advisor" in SKILL.md. Don't silently produce something else, and don't fall back to an HTML artifact with a print button — the embedded viewer blocks `window.print()`.

**When it runs normally, the tooling gets no mention at all** — not the dependency check, not the JSON, not the command. The advisor gets the page and its path.
