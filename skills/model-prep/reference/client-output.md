# Client-facing output — format

Optional, produced only when the advisor asks. Always a **draft the advisor reviews, personalizes, and owns** before it reaches a client.

Three variants: an email, talking points, or a one-page takeaway. Ask which; don't produce all three.

## Before anything in this file

**Two things must already have happened, in this order:** the compliance disclosure printed verbatim in chat, and the advisor's confirmation returned through the question tool. Both are specified in step 5 of SKILL.md.

**If either is missing, stop and go do it.** Reaching this file is not itself authorization — it's common to arrive here because the advisor asked for the artifact directly ("draft the client email", "client version please"), and that request is not a substitute for the gate. Print the notice, call the confirmation question, and only then work through what follows.

**Nothing below may be asked ahead of that disclosure**, including the variant question and any question about the PDF itself. A question that secures agreement before the compliance notice has appeared defeats the notice, however procedural the question seems.

**Delivery, by variant** — text in chat first in every case, because the advisor will want to reword before this reaches a client:

| Variant | Delivery |
|---|---|
| Email | Text in chat only. **No PDF** — it goes into a mail client as text |
| Talking points | Text in chat, then offer the PDF — some advisors want a page in hand |
| One-page takeaway | Text in chat, then generate the PDF |

See "Generating the PDF" at the bottom of this file.

## Rules that apply to all three

**Nothing from "Why this fits your practice" appears here.** Practice economics — time saved, onboarding smaller accounts, book valuation and transfer — is advisor-only. A client reading that the model saves their advisor nine hours a week is a different conversation than the one intended.

**No internal labels.** No "Matched to," no "advisor-only," no field names as headings, no "Client-Ready" badge. No model-series tag vocabulary either — a client has no idea what "Active-Passive" or "Dynamic" means, and a series name like "Dynamic Active-Passive Series" is usually better described than named ("a portfolio that blends actively managed and index funds"). The client sees the deliverable, not the machinery.

**Don't attribute anything to the client that they didn't say.** No "you asked about…", no invented goals, no assumed concerns. If the advisor supplied context about the client, you may use it; otherwise write to a general reader and let the advisor personalize.

**The recommendation boundary is unchanged.** Plain language, warm tone, no action directed. "Here's how this approach works and why it may matter" — never "here's what you should do."

**Same field boundary as everywhere else.** No performance, yield, or asset-class breakdown, in any form, however casually phrased — including one derived from the fund weights.

**Cost: the figure or nothing.** The weighted average expense ratio is a real field now, per sleeve, so quoting it plainly is fine — *"the expense ratio on this portfolio is 0.13% a year"* — if the advisor wants it in the piece. What stays out is the **unquantified comparative**: "keeps costs low", "costs that add up in your favor over the years", "low-cost approach". Those read as supported claims, have no benchmark behind them, and are promotional in exactly the way the client voice forbids. A number the advisor can stand behind is defensible; an adjective is a pitch.

**Note on the samples below.** The skill brief's illustrative email and talking points both say costs are kept low. That phrasing contradicts the brief's own guardrail — "nothing promotional, alarming, persuasive, or overly certain" — so the samples here don't reproduce it. If a reviewer wants the cost point in client material, make it the figure.

**Default to no cost figure at all.** This variant is meant to be essentially figure-free, and a client reading an expense ratio in isolation has nothing to compare it against. Include it when the advisor asks; don't volunteer it.

**Voice:** see "Tone and Voice for Client-Ready Output" in SKILL.md — that section is the specification, and it's the plugin's shared client-ready voice. In short: plain and approachable but credible; an intelligent client who isn't a market professional; one main idea per sentence; active voice; calm, never promotional or urgent.

**Short.** The client tier is the shortest thing this skill writes, not the longest. An email is a handful of short paragraphs. Talking points are five or six single speakable lines. A one-page takeaway is one page. If a client piece is running longer than the advisor analysis it came from, cut it — and cut the figures first, since this variant is meant to be essentially figure-free anyway.

**Placeholders stay placeholders.** `[Client Name]`, `[Advisor Name]` — never invent names.

**No links to the advisor site.** `advisors.vanguard.com` is behind an advisor login, so a client following that link hits a wall. The model portfolios page belongs in the advisor one-pager, never here. If a client-facing piece needs a source, the advisor supplies one they can stand behind.

Carry the provider disclaimer verbatim if one accompanied the data.

## Email

Open with a clear purpose, maintain a natural human flow, close with a low-pressure next step.

> Subject: A simple look at a model approach for your portfolio
>
> Hi [Client Name],
>
> Ahead of our next conversation, I wanted to share a simple way we could approach managing your investments — using a professionally built, globally diversified model portfolio.
>
> A model like this spreads your money across a broad mix of investments and keeps that mix on track over time. It's built and maintained by an experienced investment team, following a consistent, disciplined process.
>
> None of this changes the plan we've built together — it's simply a way to keep your investments diversified and disciplined while freeing up more of our time to focus on your bigger financial picture.
>
> If it would help, let's set up a short call to walk through what this could look like for you. Just let me know what works.
>
> Warm regards,
> [Advisor Name]

Note the last paragraph: it reassures without promising an outcome, and the close invites rather than instructs.

## Talking points

Each point is a **single speakable idea** the advisor can say out loud or personalize. Not a data dump with bullets.

> - A model portfolio is a ready-made, professionally managed mix of investments designed to work together toward your goals.
> - It stays diversified and rebalanced over time, so it doesn't drift away from the plan we set.
> - It's built and monitored by an experienced investment team following a consistent process.
> - Using an approach like this frees up more of our time together to focus on your planning, not just the investments.
> - There's no single right answer here — we'd weigh it against your goals, comfort with risk, and what you already own.

The last point is load-bearing: it keeps the set from reading as a pitch. Include something equivalent every time.

## One-page takeaway

Same voice as the email, structured as a short titled page the client can keep. Lead with what a model portfolio is in one or two sentences, then how it works, then what it would mean for them in general terms, then a closing note that the advisor will help weigh it against their situation.

Keep it essentially figure-free. The equity/fixed-income split is fine ("roughly 60% stocks, 40% bonds") because it's how the model is labeled. A fund-by-fund weights table is not — it belongs on the advisor one-pager, and a client seeing percentages will read them as a recommended allocation.

## Generating the PDF

For the one-page takeaway (and talking points, if the advisor wants a page), render the approved text with the bundled script — the same one that produces the advisor page, in client mode:

```bash
python3 scripts/make_model_pdf.py content.json "A simple look at a model portfolio approach.pdf"
```

The interpreter name is OS-specific: `python3` on macOS and Linux, `py -3` or `python` on Windows. Use whichever resolves on this machine.

```json
{
  "mode": "client",
  "title": "A simple look at a model portfolio approach",
  "subtitle": "Prepared for our next conversation",
  "intro": "One or two plain sentences on what a model portfolio is.",
  "sections": [
    {"heading": "How it works", "body": "Plain-language paragraph."},
    {"heading": "What it would mean for you", "bullets": ["One speakable idea per bullet."]}
  ],
  "open_items": ["We'll talk it through together and decide what makes sense for your situation."],
  "next_step": "A low-pressure invitation to talk.",
  "disclosures": ["This is a draft prepared for discussion with your advisor.", "Provider disclaimer, verbatim."]
}
```

**`mode: "client"` is a boundary the script enforces, not a style flag.** Three things it does that you should not try to route around:

- **`practice_value` is refused** — passing it raises an error rather than dropping the field. Practice economics is advisor-only, and rewriting those bullets into the client narrative defeats the control rather than satisfying it.
- **`matched_to` is refused** — the criteria breadcrumb is advisor-facing compliance record-keeping, not client copy.
- **The advisors.vanguard.com link is dropped**, because a client following it hits a login wall.

It also rejects series tag vocabulary in client mode — `Active-Passive`, `Dynamic Series` and similar. That's the "describe it, don't name it" rule from above, enforced: write *"a portfolio that blends actively managed and index funds"* rather than the series name.

**No holdings table on a client page.** `sections[].table` exists in the script, but a fund-by-fund weights table belongs on the advisor one-pager — a client seeing percentages reads them as a recommended allocation. Keep this variant essentially figure-free; the equity/fixed-income split in prose ("roughly 60% stocks, 40% bonds") is the one number that belongs, because it's how the model is labeled.

**Placeholders survive rendering.** `[Client Name]` and `[Advisor Name]` go into the PDF as-is — they're the advisor's cue to personalize, and the script won't fill them in.

**If the script can't run**, deliver the takeaway as formatted text in chat and say so plainly.

## Before delivering

Say plainly that it's a draft for the advisor's review, and that they should personalize it before sending. That framing is not a formality — the advisor owns anything that leaves the system.
