# Design Patterns in "10 Wild Things You Can Build With Jev"
**Source:** [Cloud Codes — 10 Wild Things You Can Build With Jev](https://youtu.be/X4Lqj54sw4I) (14:15, Sep 21 2026)
**Subject:** TypeSafe's Jev — a "System One" decision model (instructGPT co-founder Diogo Almeida), launched Sep 15 2026
**Summary:** A model that *cannot* write sentences — it reads program state + a menu of allowed answers in one pass, returns each with a probability, in 70–500ms. 10 community builds shipped in 6 days.

---

## Part 1 — Architectural Patterns (the model itself)

### 1. The Typed Choice / Closed Menu Pattern
Give the model a **fixed enumeration of allowed answers** with each question. It returns one of N, never free text.
- **Why it matters:** Output is constrained *by the decode*, not by prompting. No parsing a paragraph and praying it's valid.
- **Trade-off:** Validity ≠ correctness. Schema-guaranteed ≠ judgment-guaranteed.
- **Source:** TypeSafe's core thesis; echoed in the audit section ("guaranteed by construction" covers format only).

### 2. System One vs. System Two
Borrowed from psychology's dual-process split.
- **System Two** (chat models): slow, deliberate, talkative — paragraphs of reasoning.
- **System One** (Jev): fast, automatic, non-verbal — the thousands of tiny calls software makes that never needed a paragraph.
- **Pattern:** Match the *inference mode* to the *task's latency budget*. Don't spin up the sentence machine to say "yes."

### 3. Batch Multi-Question Single-Pass
One request carries **many independent questions**, each with its own menu.
- **Failure mode it removes:** the sequential per-question round trip.
- **Failure mode it enables:** cross-question coupling — one latent state can flip several answers at once (called out explicitly in the Mario build).
- **Example:** "Which button do I click?" + "Is the form finished?" resolved *in one shot*.

### 4. Calibrated Decisions (RL for honest confidence)
Trained so a stated 90% means it's right ~9 times in 10 — a weather-forecast contract.
- **Forward reference:** the entire third act of the video hangs on this. Compaction trusts the confidence score; the score is the unverified part; OpenJev's probabilities are explicitly *uncalibrated* raw logits.

### 5. Menu-as-Safety-Boundary
Because the vocabulary is closed, the model **cannot emit anything outside the permitted set** — including injected instructions. Structural containment rather than behavioral guardrails.
- **Contrast:** token-level jailbreaks don't apply when there are only 7 legal moves.

### 6. Prose Reconstructed From Typed Choices (the inversion hack)
Enumerate a fixed word list, then ask "which word comes next?" repeatedly.
- **Result:** functional text generation that immediately degrades to word salad on anything real.
- **Insight:** it's a *negative* demonstration — the model's worst capability is exactly what it was built to avoid.

---

## Part 2 — Agent / Integration Patterns

### 7. State Menu Instead of Screenshot (Vision Bypass)
Hand the model a **structured description** — numbered list of clickables, or telemetry — instead of pixels.
- **Cost win:** strips the expensive vision round trip from the loop.
- **Latency win:** no image encode, no vision-token prefill.
- **Caveat:** only viable when the environment can self-describe. Emulators and DOMs can; the open world can't.

### 8. Two-Tier / Router Model Split
A small decision model chooses the *action*; a second tiny model generates the *payload*.
- **Example:** Jev picks "type into element #4"; a separate model produces the keystrokes.
- **Pattern:** separate *policy* from *content synthesis*. Cheapest tier handles the high-frequency call.

### 9. Polling Loop at Fixed Cadence
Mario decided every **8 frames** from live emulator telemetry; "danger level" answered alongside each action as a side question.
- **Pattern:** decision frequency is a tunable — decouple it from the render/telemetry rate.
- **Pattern:** the auxiliary scalar ("how dangerous is this moment?") shaped behavior without being an action.

### 10. Streaming Evaluation Per Unit of Content
Sponsor skipper evaluates **second by second** rather than consulting a crowd-sourced timestamp list. The feed cleaner collapses matching posts as it scrolls.
- **Pattern:** continuous local classification replaces a precomputed global index.
- **Why it's enabled:** cost per decision is low enough to run unbatched forever.

### 11. Daemon-Scale Repetition (Always-On Classification)
Downloads organizer runs **with no other model in the loop** — one small decision repeated per file event.
- **Pattern:** cheap-per-decision + event-driven trigger = a resident process you can leave running all day. The economics, not the algorithm, is what makes it a daemon.

### 12. Compose From Trusted Components (No-Generation UI)
Instead of generating an interface, expose a **box of pre-built pieces** and let the model select order and placement.
- **Two passes:** one to choose the set, one to lay it out.
- **Wins:** fast, no drift across turns, and **cannot invent a component that doesn't exist**.
- **Pattern name:** *safety by construction*, applied to design rather than decoding.

### 13. Structural Compaction (Prune, Don't Summarize)
Walk back through tool-call history and ask per-call: **keep at all?** and **keep verbatim or trim?** Survivors are preserved exactly — never rewritten, never summarized.
- **Pattern:** deletion and elision preserve fidelity that paraphrase destroys.
- **Open question this creates:** you're trusting a confidence score to decide what's safe to lose — which is exactly the unverified number.

### 14. Parallel Fan-Out, Single Verdict
"Kill My Idea" fires ~10 evaluations at once (demand, competition, execution risk...), then reduces to one of three outcomes: **kill / fix / ship**.
- **Pattern:** independent scorers in parallel, then a categorical collapse. Latency stays flat as criteria multiply.

### 15. Simulation as Stress Bench for Policy
Full simulated JFK tower (GPT-6 Astra generated the world), Jev makes every clearance — land, hold, go-around — voice model on the radio.
- **Pattern:** use a generative world as the load generator for decision policy; the builder labels it simulation, not live data.
- **Value:** forces decisions under climbing traffic without real-world stakes.

### 16. Open-Source Local Reimplementation (Mechanism Proof)
OpenJev/SemIf: runs **entirely in-browser on local open models**, leans on the user's own GPU, no server, no account.
- **Pattern:** reproduce the *mechanism* with visible internals to separate the idea from the vendor's numbers.
- **Finding:** best open model matched reference answers ~85% vs Jev's reported 88%; browser-scale models much worse; probabilities raw, not calibrated.
- **Author's own framing:** "evidence the mechanism can be reproduced, not a reproduction of Jev's reported performance."

---

## Part 3 — The Audit: Claims vs. Evidence (patterns of *mis*-measurement)

| Claim | Reality per the video |
|---|---|
| "Zero hallucinations" | Their own page says the number **isn't measured**. "Guaranteed by construction" covers format, not judgment. |
| "200× faster" | One page says 40–200×, another says 20×. Independent test clocked **~25×** (0.33s vs ~9s Claude Fable 5 on a writing review). |
| Accuracy | ~**68% agreement** with a panel of frontier models — agreement, not correctness, and *the company grading its own homework*. |
| Compaction demo | GIF was a **dramatized mock-up** that never calls the real model. Run for real across 5 sessions at safe confidence: **0% dropped** — the calls Jev wanted to discard were the ones it was least sure about. |
| Flight demo | Genuine — **real speed, no editing**. 1,092 → 101 browser calls; 9.5s → 7s; ~$0.0039/run; 9,000 users in 3 days; permissive license. |

**Meta-pattern — the two-blender problem:** format validity and judgment accuracy get blended in marketing. Pulling them apart *is* the answer. Judge the decisions, not the sentences.

---

## Part 4 — Cost / Pricing Model

- **$0.04 per million input words; output free** — because a typed choice is too small to bill.
- 70–500ms per call.
- Equivalent chat-model workload: dollars and long minutes (one wordy answer at a time).
- **Strategic read:** pricing inverts when output collapses to an enum. Metered-per-token models are structurally disadvantaged on high-frequency, low-content decisions.

---

## Part 5 — When to Reach For This Constellation

**Use it when** a fast, cheap typed decision replaces a giant model **and a wrong call is easy to catch**: routing requests, retries, feed filtering, ad/sponsor skipping, file classification, UI assembly.

**Don't lean on it when** accuracy numbers from the landing page are load-bearing, or when the decision is unverifiable in the moment (the compaction case).

**The real headline:** the moment a model stopped trying to talk and started making decisions, developers found a hundred uses in six days.

---

## Quick Reference — 21 patterns named

**Model:** 1 Typed Choice/Closed Menu · 2 System One vs Two · 3 Batch Multi-Question Single-Pass · 4 Calibrated Decisions · 5 Menu-as-Safety-Boundary · 6 Prose-From-Choices inversion

**Agent:** 7 State Menu Instead of Screenshot · 8 Two-Tier Policy/Payload Split · 9 Fixed-Cadence Polling + Auxiliary Scalar · 10 Streaming Per-Unit Evaluation · 11 Daemon-Scale Repetition · 12 Compose From Trusted Components · 13 Structural Compaction · 14 Parallel Fan-Out Single Verdict · 15 Simulation as Stress Bench · 16 Open-Source Local Reimplementation

**Audit:** 17 Format≠Judgment valid-vs-right split · 18 Unmeasured Guarantee by Construction · 19 Agreement-With-Panel as proxy accuracy · 20 Company-Grades-Own-Homework · 21 Dramatized Mock-Up vs Real Run

---

## Appendix — Projects & Links

| # | Build | Author | Repo / Link | License |
|---|---|---|---|---|
| 1 | 7-Second Flight Search | Browser Use | github.com/browser-use/jev-ultrafast | permissive |
| 2 | Real-Time Super Mario | Faadil Shaik | github.com/fhshaik/typesafe-mario | — |
| 3 | YouTube Sponsor Skipper | Tony Dinh | github.com/trungdq88/youtube-sponsor-detection | **none yet — don't ship on it** |
| 4 | Downloads Organizer | Marcel Pociot | — | — |
| 5 | Feed Cleaner (NL rules) | Marcel Pociot | — | — |
| 6 | 1-Second UI Assembly | json-render / credited to Michael Tetteh Akula | — | — |
| 7 | Claude Code Context Compactor | Tamara Tran | github.com/tamaratran/fast-jev-compaction | — |
| 8 | JFK ATC Simulator | Reddit builder | — | — |
| 9 | Kill My Idea | stemonte | killmyidea.stemonte.io | — |
| 10 | World's Worst Chatbot | mkotlikov / finetuningsingh | — | — |
| — | OpenJev / SemIf | Theo Lee | github.com/TheoLeeCJ/SemIf | open source |
| — | Jev (the model) | TypeSafe / Diogo Almeida | typesafe.ai/blog/introducing-system-one-models-and-jev | commercial |
