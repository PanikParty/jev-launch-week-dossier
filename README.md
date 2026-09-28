# The Jev Launch Week Dossier

**A memorial record of the ten wildest community builds shipped during TypeSafe Jev's launch week, and the 21 design patterns they reveal.**

[![Patterns](https://img.shields.io/badge/patterns-21-blueviolet)](#the-pattern-catalogue)
[![Builds](https://img.shields.io/badge/builds-10-orange)](#the-ten-wild-builds)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## What is this?

On **September 15, 2026**, a company called TypeSafe emerged from two years of stealth with $40M in funding and one strange idea: **a model that cannot write a sentence — by design.**

Jev reads your program's state plus a menu of allowed answers, and returns typed decisions with probabilities attached. No paragraphs. No prose. Just the picks.

Within **six days**, developers had bolted it onto everything from flight search to Super Mario to an air traffic control tower.

This repository is a systematic teardown of that week: the ten builds, the architectural patterns underneath them, and an honest audit of which vendor claims survived contact with anyone outside the company.

**Source presentation:** [Cloud Codes — *10 Wild Things You Can Build With Jev*](https://youtu.be/X4Lqj54sw4I) (14:15, Sep 21 2026)

---

## Read the dossier

- **[📄 The full dossier (Markdown)](docs/jev-launch-week-dossier.md)** — 4,300 words, 7 parts, 13 tables
- **[🌐 The full dossier (HTML)](docs/jev-launch-week-dossier.html)** — self-contained, dark-themed, print-ready
- **[⚡ Quick-reference pattern sheet](patterns/design-patterns-quick-reference.md)** — all 21 patterns, one screen

> The HTML file is fully self-contained — no CDN, no external assets. Open it directly in any browser, or `Ctrl+P` → *Save as PDF* for an archival copy.

---

## Contents

| Part | Subject |
|---|---|
| **I** | [The Model](#part-i--the-model) — what Jev actually is |
| **II** | [The Ten Wild Builds](#the-ten-wild-builds) — each with its architectural insight |
| **III** | OpenJev — the weekend open-source clone |
| **IV** | The Audit — five vendor claims vs. the evidence |
| **V** | The Complete Pattern Catalogue — 21 patterns in 3 families |
| **VI** | Reference tables — build index, cross-reference, claims register |
| **VII** | Closing assessment |

---

## Part I — The Model

A conventional language model writes one word at a time, left to right. Ask it a yes/no question and it still spins up the entire sentence machine just to say "yes."

Jev doesn't do that. TypeSafe calls it a **System One model**:

> Give it the current state of your program plus a set of questions. Every question arrives with a fixed menu of allowed answers. Jev reads all of it in **one pass** and returns each answer with a **probability attached**.

| Input | Output |
|---|---|
| Program state: *agent has landed on a page* | — |
| Q1: *Which button do I click?* + menu of N buttons | **Button 4 — 91%** |
| Q2: *Is the form finished?* + menu {yes, no} | **Not finished** |

**The person:** Diogo Almeida, on the original team that built ChatGPT. His argument is almost a confession — *superhuman chat didn't deliver what it promised, so he went the other way*, toward a model that **decides instead of talks.**

**The framing:** Chat models chase the slow, talkative, deliberate kind of cognition. Jev is built for the fast, automatic kind — **the thousands of tiny calls software makes that never needed a paragraph in the first place.**

**The economics:**

| Metric | Value |
|---|---|
| Input pricing | **$0.04 per million words** |
| Output pricing | **Free** — a typed choice is too small to bill |
| Latency per call | **70–500 ms** |
| Equivalent chat-model workload | **Dollars, plus long minutes of waiting** |

---

## The Ten Wild Builds

| # | Build | Author | Key pattern | Repo |
|---|---|---|---|---|
| 1 | **7-Second Flight Search** | Browser Use | State Menu ≠ Screenshot | [jev-ultrafast](https://github.com/browser-use/jev-ultrafast) |
| 2 | **Real-Time Super Mario** | Faadil Shaik | Telemetry ≠ Pixels | [typesafe-mario](https://github.com/fhshaik/typesafe-mario) |
| 3 | **YouTube Sponsor Skipper** | Tony Dinh | Streaming Per-Unit Eval | [youtube-sponsor-detection](https://github.com/trungdq88/youtube-sponsor-detection) ⚠️ |
| 4 | **Downloads Organizer** | Marcel Pociot | Daemon-Scale Repetition | — |
| 5 | **Feed Cleaner (NL rules)** | Marcel Pociot | Streaming Per-Unit Eval | — |
| 6 | **1-Second UI Assembly** | json-render | Compose From Trusted Components | — |
| 7 | **Claude Code Compactor** | Tamara Tran | Structural Compaction | [fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) |
| 8 | **JFK ATC Simulator** | Reddit builder | Simulation as Stress Bench | — |
| 9 | **Kill My Idea** | stemonte | Parallel Fan-Out, Single Verdict | [killmyidea.stemonte.io](https://killmyidea.stemonte.io/) |
| 10 | **World's Worst Chatbot** | mkotlikov / finetuningsingh | Prose-From-Choices (inversion) | — |
| — | **OpenJev / SemIf** | Theo Lee | Open-Source Local Reimpl. | [SemIf](https://github.com/TheoLeeCJ/SemIf) |

⚠️ *Tony Dinh's sponsor skipper has **no license yet** — do not ship on top of it without checking first.*

### The repeatable shape

Every successful build reduces to one motion:

> **Hand the model a state and a menu. Get back a typed decision.**

Everything else — the DOM list, the emulator telemetry, the file event, the second of audio, the component palette — is just a way of producing the state.

### Highlighted build: the flight search that started it

The `jev-ultrafast` approach throws out the screenshot entirely. Instead of *screenshot → big model → wait → click → repeat*, it hands Jev a **numbered list of everything clickable** and asks exactly one thing: *which action, and which element number?*

| Metric | Before | After |
|---|---|---|
| Browser calls to the page | ~1,092 | **101** |
| Wall time | 9.5s | **7s** |
| Cost per run | — | **~$0.0039** |
| Adoption | — | **9,000 users in 3 days** |

---

## The Pattern Catalogue

Twenty-one patterns across three families. Full definitions with evidence in [the dossier](docs/jev-launch-week-dossier.md#part-v--the-complete-pattern-catalogue).

### Family A — Model Architecture (1–6)

| # | Pattern | Core mechanic |
|---|---|---|
| 1 | **Typed Choice / Closed Menu** | Fixed enumeration per question. Constraint enforced **by the decode**, not by prompting. |
| 2 | **System One vs. System Two** | Match inference mode to latency budget. |
| 3 | **Batch Multi-Question Single-Pass** | Many questions in one request. Removes round trips; enables cross-question coupling. |
| 4 | **Calibrated Decisions** | Train so a stated 90% means right ~9/10 times. |
| 5 | **Menu-as-Safety-Boundary** | Closed vocabulary = structural containment, including against injection. |
| 6 | **Prose-From-Choices (Inversion)** | Enumerate words, ask "which next?" repeatedly — a *negative* demonstration of the thesis. |

### Family B — Agent & Integration (7–16)

| # | Pattern | Core mechanic |
|---|---|---|
| 7 | **State Menu Instead of Screenshot** | Structured description replaces pixels. Strips the vision round trip. |
| 8 | **Two-Tier Policy / Payload Split** | Small model chooses the action; a second tiny model generates the payload. |
| 9 | **Fixed-Cadence Polling + Auxiliary Scalar** | Decision frequency is a tunable; a side-question scalar shapes behavior without being an action. |
| 10 | **Streaming Per-Unit Evaluation** | Continuous local classification replaces a precomputed global index. |
| 11 | **Daemon-Scale Repetition** | Cheap-per-decision + event trigger = a resident process. *The economics enables the daemon.* |
| 12 | **Compose From Trusted Components** | Select from pre-built pieces. Cannot invent a component that doesn't exist. |
| 13 | **Structural Compaction** | Prune and elide history; survivors preserved exactly. Never summarize. |
| 14 | **Parallel Fan-Out, Single Verdict** | N independent scorers concurrently → one categorical verdict. Latency stays flat. |
| 15 | **Simulation as Stress Bench** | Generative world as load generator for decision policy. |
| 16 | **Open-Source Local Reimplementation** | Reproduce the *mechanism* with visible internals to separate idea from numbers. |

### Family C — Measurement & Claims (17–21)

*These are patterns of mis-measurement — a reusable diagnostic toolkit for evaluating the next vendor launch.*

| # | Pattern | Core mechanic |
|---|---|---|
| 17 | **Format ≠ Judgment** | Schema-validity and correctness are different properties. Blending them *is* the marketing. |
| 18 | **Unmeasured Guarantee by Construction** | A headline metric the company's own page concedes isn't measured. |
| 19 | **Agreement-With-Panel as Proxy Accuracy** | Measuring agreement with peer models and presenting it as accuracy. |
| 20 | **Company Grades Own Homework** | Self-reported benchmarks, no replication. Tell: the number changes by the page. |
| 21 | **Dramatized Mock-Up as Evidence** | Demo assets that never call the real system, placed next to the claim they support. |

---

## The Audit (summary)

> **Being valid is not the same as being right.**

| TypeSafe claim | What the evidence shows |
|---|---|
| **"Zero hallucinations"** | Their **own page admits it isn't measured**. *"Guaranteed by construction"* covers the **format**, not the judgment. |
| **"200× faster"** | Company pages say 40–200× **and** 20×. The one independent test found **~25×** (0.33s vs ~9s). |
| **Accuracy** | ~**68% agreement** with a frontier-model panel. Agreement, not correctness — and **the company grading its own homework.** |
| **Compaction demo** | The GIF was a **dramatized mock-up** that never calls the model. Run for real over 5 sessions: **0% dropped.** |

**The pattern:** the mechanism is genuinely new and useful. The benchmark claims are not proven by anyone outside the company.

**The verdict:** try it where a fast, cheap typed decision replaces a giant model **and a wrong call is easy to catch**. Wait for outside testing if the landing-page accuracy numbers are load-bearing.

> **Judge Jev on the decisions it makes, not the sentences it won't write.**

---

## Repository layout

```
.
├── README.md                                   ← you are here
├── docs/
│   ├── jev-launch-week-dossier.md              ← full dossier (source of truth)
│   └── jev-launch-week-dossier.html            ← rendered, self-contained
├── patterns/
│   └── design-patterns-quick-reference.md      ← all 21 patterns, one screen
└── scripts/
    └── render.py                               ← markdown → styled HTML
```

### Regenerating the HTML

The HTML is generated from the Markdown by a dependency-free Python script:

```bash
python3 scripts/render.py
```

Edit `docs/jev-launch-week-dossier.md`, run the script, and the HTML updates in place.

---

## Methodology & provenance

- **All quotes, figures, and caveats** are as reported in the source presentation and are attributed to it.
- **Company-stated figures are labelled separately from independently-measured ones** throughout the dossier. This distinction is the document's central discipline.
- **The pattern names are authored, not quoted.** The presentation describes how each build works but never names patterns. The labels — *Two-Tier Policy/Payload Split*, *Structural Compaction*, etc. — were formalized from the described mechanics.
- **Family C is an abstraction.** The audit findings were refactored into reusable diagnostic patterns rather than left as a list of grievances.

## Contributing

Corrections welcome — especially where a figure is now stale, a repo has changed license, or a claim has since been independently tested. Open an issue.

## License

[MIT](LICENSE) — for the document and scripts. The third-party projects linked above retain their own licenses (note build #3 has **none**).
