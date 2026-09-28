# The Jev Launch Week Dossier
## A Memorial Record of the "10 Wild Builds" and the Design Patterns They Reveal

**Compiled:** September 28, 2026
**Source presentation:** Cloud Codes — *10 Wild Things You Can Build With Jev* (14:15, published Sep 21, 2026)
**Source URL:** https://youtu.be/X4Lqj54sw4I
**Subject:** TypeSafe's Jev — a "System One" decision model
**Launch window documented:** September 15 – 21, 2026 (six days)

**Companion volumes:** [The Jev Design Pattern Handbook](jev-design-patterns-handbook.md) — the vendor's official pattern set: 3 primitives, 10 decision shapes, 4 design patterns. · [The Jev Benchmark Report](jev-benchmark-report.md) — independent measurement of Jev against 12 local decision models.

---

## Preface

On September 15, 2026, a company called TypeSafe emerged from two years of stealth with $40 million in funding and one strange idea: a model that cannot write a sentence — **by design**. Within six days, developers had bolted it onto everything from a flight search engine to Super Mario to an air traffic control tower.

This document memorializes that week: the ten builds the presentation selected as the wildest, the sixteen architectural and agent patterns extractable from them, the five measurement patterns the audit exposed, and a full accounting of what held up under scrutiny and what did not.

It is written to stand alone. No prior viewing required.

---

## Part I — The Model: What Jev Actually Is

### The premise

A conventional language model writes one word at a time, left to right. Ask it a yes/no question and it still spins up the entire sentence machine just to say "yes."

Jev does not do this. TypeSafe calls it a **System One model**. The contract is:

> Give it the current state of your program plus a set of questions. Every question arrives with a fixed menu of allowed answers. Jev reads all of it in **one pass** and returns each answer with a **probability attached**.

**Example of the contract in operation:**

| Input | Output |
|---|---|
| Program state: *agent has landed on a page* | — |
| Question 1: *Which button do I click?* + menu of N buttons | **Button 4 — 91%** |
| Question 2: *Is the form finished?* + menu {yes, no} | **Not finished** |

No paragraph. Just the picks. Returned in well under a second.

### The person behind it

**Diogo Almeida**, who was on the original team that built ChatGPT. His stated argument is almost a confession: *superhuman chat didn't deliver what it promised, so he went the other way* — toward a model that **decides instead of talks**.

### The framing

Almeida borrows a split from psychology:

| System | Character | Who chases it |
|---|---|---|
| **System Two** | Slow, deliberate, verbal reasoning | Chat models |
| **System One** | Fast, automatic, non-verbal judgment | Jev |

Chat models chase the slow, talkative kind. Jev is built for the fast, automatic kind — **the thousands of tiny calls software makes that never needed a paragraph in the first place.**

### The training claim

TypeSafe calls it **reinforcement learning for calibrated decisions**. The analogy offered is a weather forecast: if it says 90% chance of rain, it should rain about nine times in ten. *Calibrated* means Jev's confidence is honest in exactly that sense.

> **Hold that word.** It returns at the end of the document as the load-bearing unverified assumption.

### The economics

| Metric | Value |
|---|---|
| Input pricing | **$0.04 per million words** |
| Output pricing | **Free** — a typed choice is too small to bill |
| Latency per call | **70–500 ms** |
| Cost for 1M small decisions | **$0.04** |
| Equivalent chat-model workload | **Dollars, plus long minutes of waiting** |

The pricing is the flex. A normal model charges for every word it writes; Jev barely writes anything, so there is almost nothing to charge for.

---

## Part II — The Ten Wild Builds

The presentation ordered these intentionally: useful first, working up to ridiculous.

---

### Build 1 — The 7-Second Flight Search
**Author:** Browser Use (team) · **Repo:** `github.com/browser-use/jev-ultrafast` · **License:** permissive
**Category:** Serious / Ship-It

#### What it does
Opens Google Flights, types Zurich → London, sets a date, and pulls the results — in about 7 seconds, at real speed, unedited.

#### The architectural insight — State Menu Instead of Screenshot

**How most web agents work:**
1. Take a screenshot
2. Send the picture to a big model
3. Wait while it says what to click
4. Click it, repeat

Every step is a slow, expensive round trip.

**How jev-ultrafast works:**
- **Throws out the screenshot entirely.**
- Hands Jev a **numbered list of everything clickable on the page**
- Asks exactly one thing: *which action, and which element number?*
- When the action is "type some text," **a tiny separate model** fills in the actual keystrokes.

#### Measured results

| Metric | Before | After |
|---|---|---|
| Browser talks to the page | ~1,092 calls | **101** |
| Wall time | 9.5 seconds | **7 seconds** |
| Cost per run | — | **under $0.004** (~$0.0039) |
| Jev calls | 22 | **17** |
| Adoption | — | **9,000 users in 3 days** |

#### Two notes from the team
1. The whole project is **open source under a permissive license**.
2. The founder pointed out that **the demo runs at real speed — no editing tricks.**

---

### Build 2 — Playing Super Mario in Real Time
**Author:** Faadil Shaik · **Repo:** `github.com/fhshaik/typesafe-mario`
**Category:** Gloriously silly, technically instructive

#### What it does
Jev plays Super Mario Brothers from live emulator telemetry.

#### The architectural insight — Telemetry Instead of Pixels

**Jev does not see the screen.** The emulator hands it a *description* instead:

- Mario's position
- How fast he's going
- Whether he is mid-jump
- The nearest enemy, and when it will reach him
- The gap coming up

Every **8 frames**, Jev picks from **seven moves**: stand still, go right, jump, run, run and jump (and the balance of the set).

It **also answers a side question each time**: *roughly, how dangerous is this exact moment?* That scalar nudges whether it should leave the ground.

#### Honest limitations stated in the presentation
- There is **no clean run posted start to finish** — the presentation explicitly will not claim it beat the game.
- What you can watch is a model that **thinks in fast reactions**, keeping Mario alive in real time.
- The presenter's own words: *"which shouldn't really work as well as it does."*

#### The pattern named here
**Hand Jev a state in a menu, get a quick decision back.** This is the repeatable shape the rest of the builds share.

---

### Build 3 — The Instant YouTube Sponsor Skipper
**Author:** Tony Dinh (indie developer) · **Repo:** `github.com/trungdq88/youtube-sponsor-detection`
**License:** ⚠️ **None yet** — do not ship on top of it without checking
**Category:** Installable dev tool

#### What it does
A Chrome extension that skips the sponsor read for you.

#### The architectural insight — Streaming Per-Unit Evaluation

**Not from a crowd-sourced list of timestamps.** It *listens and decides*, second by second: *is this the sponsor, or the actual video?*

The distinction matters. A crowd list is a precomputed global index that goes stale and requires human labor. This is **continuous local classification** with no prior index at all.

#### Cost
Approximately **half a cent per video**, by the author's own estimate.

---

### Build 4 — The Auto-Sorting Downloads Folder
**Author:** Marcel Pociot (runs a developer tools company)
**Category:** Installable dev tool · the quiet workhorse

#### What it does
A desktop app that watches your downloads folder. The second a file lands, it decides what the file is and where it belongs. Something that reads like an invoice gets filed with your invoices.

#### The architectural insight — Daemon-Scale Repetition

The detail the presenter singled out, from the author's own post:

> **No other model in the loop. Just Jev.**

There is no big language model reading your files and summarizing them. It is **one small decision repeated** — which is precisely why it is cheap enough to leave running all day.

This is the pattern in its purest form: the *economics* of a 4-cent-per-million decision is what makes a resident daemon viable, not any algorithmic cleverness.

---

### Build 5 — The Natural Language Feed Cleaner
**Author:** Marcel Pociot (same developer, one day earlier)
**Category:** Demo, not benchmark

#### What it does
A browser extension where you type a plain rule — *"hide engagement bait"* — and Jev walks down your timeline collapsing the posts that match.

#### The architectural insight — Rules in Natural Language, Executed Locally

The author says it is quick enough that you don't notice it working. **There is no measurement on that, so the presentation files it as a demo, not a benchmark.**

#### Why it still matters
A content filter you describe in **one sentence** instead of hunting through settings is a real shift in how you would use a site.

---

### Build 6 — 1-Second UI Assembly
**Author:** A UI framework called **json-render** · clip credited to Michael Tetteh Akula
**Category:** The one developers keep arguing about

#### What it does
Instead of asking a model to generate a whole app from scratch, you give it a **box of pre-built pieces** — a button, a chart, a form — and let Jev decide which ones this screen needs and how they are arranged.

#### The architectural insight — Compose From Trusted Components

json-render wired it in directly:
1. Your app **lists the candidate components**
2. Jev **picks which to include, in what order, where they sit**
3. **One pass to choose them, another to lay them out**

#### Why it matters

| Generating a full interface with a big model | Picking from parts you already trust |
|---|---|
| Slow | Fast |
| It **drifts** | Cannot drift |
| — | **Cannot invent a button that doesn't exist** |

**"Safety by construction"** — applied to design rather than to decoding.

#### Evidence caveat
A clip circulating shows an interface assembling itself in about a second. The presenter **could not track down the original post**, so that speed is *what the video shows, not a lab result*. The mechanism underneath, however, is already inside real component libraries.

---

### Build 7 — Fixing Claude Code's Context Window
**Author:** Tamara Tran · **Repo:** `github.com/tamaratran/fast-jev-compaction`
**Category:** Strong idea, unproven — and the pivot of the whole audit

#### The problem it targets
The context window fills up, and the tool makes room by having a language model **summarize the conversation so far**. Those summaries drop details you needed, and you find out which ones too late.

#### The architectural insight — Structural Compaction

Tran's project takes a different route. It **walks back through your old tool calls** and asks Jev **two tiny questions about each one**:

1. **Keep this call at all?**
2. **Keep the result word for word, or trim it?**

Whatever survives is **kept exactly — not rewritten, not summarized.**

#### The evidence, honestly reported

**The eye-catching animation on her post is, by her own README, a dramatized mock-up.** It does not call the real model. It exists to be screen-recorded.

When someone ran the **actual thing** across **five real coding sessions** at a safe confidence setting:

> **It dropped 0% of the context.**

The calls Jev wanted to throw away were **the ones it was least sure about**, so a careful cutoff kept everything.

**Verdict: good idea, not proven yet.**

#### Credit where due — and the flaw identified
To be fair to the idea, **keeping the real text instead of a summary is the right instinct.** The trouble is **trusting a confidence score to decide what is safe to lose** — and that confidence is the exact thing that hasn't been checked yet.

> *Remember this. It is about to become the whole point.*

---

### Build 8 — Running JFK Airport Air Traffic Control
**Author:** A Reddit builder (GPT-6 Astra generated the simulation)
**Category:** Spectacle · the clearest stress test in the batch

#### What it does
An entire simulated JFK airport, with Jev dropped into the control tower.

- **Every clearance is a Jev decision:** cleared to land, hold your position, go around.
- **A separate voice model handles the radio**, so you *hear* the pilot and the controller talk while Jev makes the calls underneath.
- **As traffic climbs, it keeps planes separated without stalling.**

#### The honesty marker
It is a simulation, and **the builder says so up front — not real air traffic data.**

#### Why it earns its place
As a **stress test of decisions under load**, it is the clearest one in the batch.

---

### Build 9 — "Kill My Idea" Instant Startup Scorer
**Author:** Indie hacker posting as **stemonte** · **Site:** `killmyidea.stemonte.io`
**Category:** The model turns on you

#### What it does
Takes your startup pitch and, **instead of writing feedback**, fires about **10 Jev questions at once**:
- Demand
- Competition
- Execution risk
- *(and the rest of the set)*

Each scored **in parallel**. Outcomes a single verdict: **kill it, fix it, or ship it.**

#### Epistemic hygiene
The presentation advises holding the result loosely — and **so does the maker**, who calls it *purely demonstrative*. **A score is not a market.**

#### Why it is bracing anyway
There is something clarifying about a tool that hands you a cold number in a second, instead of a paragraph telling you your idea is amazing.

---

### Build 10 — The World's Worst Chatbot
**Authors:** mkotlikov / finetuningsingh
**Category:** A joke that compresses the entire thesis

#### What it does — the inversion hack
Jev cannot write a sentence, so a developer made it write one anyway.

**The hack, in three steps:**
1. Give Jev a **fixed list of words**
2. Ask it, **over and over**, *which word comes next*
3. A reply slowly assembles, one choice at a time

#### Results
- Ask it something **short and factual** — it manages.
- Ask it **anything real** — it drifts into **word salad**.

It is a joke, and the builders label it one.

#### Why it is the best entry
It is the whole presentation compressed into a bit: **you took a model designed to decide, forced it to talk, and got a properly terrible chatbot.** The thing it is worst at is exactly what it was built to avoid.

---

### Beyond the ten
Inside one week there were:
- Curated lists of Jev projects
- An official showcase with **hundreds of entries**
- So many clones that **the same app name showed up five times over**

The presentation was clear that ten was not close to all of them.

---

## Part III — OpenJev: The Weekend Open-Source Clone

**Author:** Theo Lee (solo developer) · **Shipped six days after Jev launched**
**Repo:** `github.com/TheoLeeCJ/SemIf` · Originally released as OpenJev, since renamed

### What it is
An open-source version that **runs entirely in your browser on open models you can download yourself.**

### What it proves — the core trick is real
> You can read the probabilities for a set of options **straight out of an ordinary model in one pass**, instead of making it type them out word by word.

### The comparison it draws, stated exactly
**One decision, two roads:**
- Road A — read the answer from the model's **internal scores, in one pass**
- Road B — make the model **type that same answer out as text**

**Road A is the whole idea of Jev.**

### Deployment characteristics
- Leans on **your own graphics card** through the browser — the kind a single gaming machine has
- **No server**
- **No account**

### The half that matters most — the audit-bearing caveat
OpenJev's probabilities are **raw** — just the model's gut feeling over the allowed words. **They are NOT calibrated the way TypeSafe says Jev's are.**

| Model | Agreement with reference answers |
|---|---|
| Best open model (OpenJev) | **~85%** |
| Jev (as reported by TypeSafe) | **88%** |
| Browser-size models | **Much worse** |

### Reception and the author's own framing
It hit the front page of Hacker News within a couple of days — *which usually means a thing struck a nerve.* People wanted to try the trick with their own eyes, on their own hardware.

The author's own line is the fairest summary anyone wrote all week:

> **"This is evidence that the mechanism can be reproduced, not a reproduction of Jev's reported performance. It proves the idea. It doesn't prove the numbers."**

---

## Part IV — The Audit: Claims vs. Evidence

Two things keep getting blended together. **Pulling them apart is the whole answer.**

### What is actually solid

Jev **cannot hand you an answer outside the menu.** Ask for one of five choices, you get one of five — **guaranteed by the way the model is decoded.**

For software, that is real value. No parsing a paragraph and praying it is valid.

### What is slippery

> **Being valid is not the same as being right.**

| TypeSafe claim | What the evidence shows |
|---|---|
| **"Zero hallucinations"** | Their **own page admits the number isn't measured**. They call it *"guaranteed by construction"* — **which only covers the format, not the judgment.** |
| **"200× faster"** | One TypeSafe page says **40–200×**. Another says **20×**. The one independent test found ~**25×** (0.33s vs ~9s against Claude Fable 5 on a writing review). |
| **Accuracy** | TypeSafe's own check measures how often Jev **agrees with a panel of frontier models** (GPT-6 Astra, Claude Fable) — it lands around **68%**. That is **agreement with other models, not proof of being right** — and it is **the company grading its own homework**. |

### On the speed test specifically
On the one writing-review task measured independently:
- Jev came in at about **a third of a second** vs nearly **nine seconds** for Claude Fable 5
- That is roughly **25× faster, not 200×**
- And on that task, **Jev missed a flaw the slower model caught**

### The pattern, lined up
- The compaction tool that **dropped nothing** at a safe setting
- OpenJev's **accuracy gap**
- A **zero that isn't measured**
- A **speed number that changes by the page**

> **The pattern is clear. The mechanism is genuinely new and useful. The benchmark claims are not proven by anyone outside the company.**

### The verdict

**Try Jev this week if** you are building something where a fast, cheap typed decision replaces a giant model **and a wrong call is easy to catch** — routing a request, retrying, filtering a feed, skipping an ad.

**Wait for outside testing if** you are leaning on the accuracy numbers from the landing page.

> **The real headline of the week isn't the flight demo, fun as it was. It's that the moment a model stopped trying to talk and started making decisions, developers found a hundred uses for it in six days.**
>
> **Judge Jev on the decisions it makes, not the sentences it won't write.**

---

## Part V — The Complete Pattern Catalogue

Twenty-one patterns across three families.

### Family A — Model Architecture Patterns (1–6)

| # | Pattern | Definition | Origin in the material |
|---|---|---|---|
| **1** | **Typed Choice / Closed Menu** | Present a fixed enumeration of allowed answers with each question. The model returns one of N, never free text. Constraint is enforced **by the decode**, not by prompting. | TypeSafe's core thesis |
| **2** | **System One vs. System Two** | Match inference mode to the task's latency budget. Slow deliberate talk vs. fast automatic judgment. Don't spin up the sentence machine to say "yes." | Almeida's psychological framing |
| **3** | **Batch Multi-Question Single-Pass** | One request carries many independent questions, each with its own menu. Removes sequentially-ordered round trips. **Cost:** enables cross-question coupling — one latent state can flip several answers at once. | "Which button" + "is the form finished" in one shot |
| **4** | **Calibrated Decisions** | Train so a stated confidence is honest — 90% means right ~9/10, a weather-forecast contract. | TypeSafe's RL claim |
| **5** | **Menu-as-Safety-Boundary** | A closed vocabulary is structural containment. The model cannot emit outside the permitted set — including injected instructions. Guardrails become unnecessary. | Implied throughout; explicit in json-render |
| **6** | **Prose-From-Choices (Inversion)** | Enumerate a fixed word list; ask "which word comes next?" repeatedly. Produces text generation that immediately degrades to word salad. A *negative* demonstration: the model's worst capability is what it was designed to avoid. | Build 10 |

### Family B — Agent & Integration Patterns (7–16)

| # | Pattern | Definition | Origin in the material |
|---|---|---|---|
| **7** | **State Menu Instead of Screenshot** | Hand the model a structured description — numbered clickables, or telemetry — instead of pixels. Strips the vision round trip from the loop. **Caveat:** only viable when the environment can self-describe. | Build 1 (DOM list), Build 2 (emulator telemetry) |
| **8** | **Two-Tier Policy / Payload Split** | A small decision model chooses the *action*; a second tiny model generates the *payload*. Separate policy from content synthesis; the cheapest tier handles the high-frequency call. | "Type into element #4" → separate model produces keystrokes |
| **9** | **Fixed-Cadence Polling + Auxiliary Scalar** | Decision frequency is a tunable — decouple it from the render/telemetry rate. An auxiliary scalar answered alongside each action can shape behavior without being an action itself. | Build 2 — every 8 frames, plus "how dangerous is this moment?" |
| **10** | **Streaming Per-Unit Evaluation** | Continuous local classification replaces a precomputed global index. Enabled because cost-per-decision is low enough to run unbatched forever. | Build 3 (second-by-second sponsor detection), Build 5 |
| **11** | **Daemon-Scale Repetition** | Cheap-per-decision + event-driven trigger = a resident process you can leave running all day. **The economics enables the daemon, not the algorithm.** | Build 4 — "no other model in the loop, just Jev" |
| **12** | **Compose From Trusted Components** | Expose a box of pre-built pieces; let the model select the set, the order, and the placement. Two passes: one to choose, one to lay out. Fast, cannot drift, **cannot invent a component that does not exist**. Safety by construction, applied to design. | Build 6 (json-render) |
| **13** | **Structural Compaction** | Walk back through history; ask per-call *keep at all?* and *keep verbatim or trim?* Survivors preserved exactly — never rewritten, never summarized. **Open question it creates:** you are trusting a confidence score to decide what is safe to lose — the exact unverified number. | Build 7 |
| **14** | **Parallel Fan-Out, Single Verdict** | Fire N independent scorers concurrently, then collapse to a categorical verdict. Latency stays flat as criteria multiply. | Build 9 — ~10 scores → kill / fix / ship |
| **15** | **Simulation as Stress Bench** | Use a generative world as the load generator for decision policy. Forces decisions under climbing pressure without real-world stakes. Honesty marker: label it simulation, not live data. | Build 8 — JFK tower |
| **16** | **Open-Source Local Reimplementation** | Reproduce the *mechanism* with visible internals to separate the idea from the vendor's numbers. Runs on commodity hardware, no server, no account. | OpenJev / SemIf |

### Family C — Measurement & Claims Patterns (17–21)

*These are patterns of mis-measurement — the reusable diagnostic shapes the audit exposed.*

| # | Pattern | Definition | Evidence |
|---|---|---|---|
| **17** | **Format ≠ Judgment** | Schema-validity and correctness are different properties. "Guaranteed by construction" typically covers only the first. **The blender of the two is the marketing.** | *Valid is not the same as right* |
| **18** | **Unmeasured Guarantee by Construction** | A headline metric ("zero hallucinations") that the company's own page concedes is not measured. The guarantee is structural, not empirical. | TypeSafe's own disclosure |
| **19** | **Agreement-With-Panel as Proxy Accuracy** | Measuring how often a model agrees with peer models and presenting it as accuracy. Agreement is not correctness — peers can share a blind spot. | ~68% vs GPT-6 Astra / Claude Fable panel |
| **20** | **Company Grades Own Homework** | Self-reported benchmarks with no external replication. **Diagnostic tell:** the number changes depending on which page you read. | 200× vs 40× vs 20× |
| **21** | **Dramatized Mock-Up as Evidence** | A demo asset (GIF/video) that never calls the real system, presented adjacent to the claim it is meant to support. The tell is usually a README's own admission. | Build 7's animation |

---

## Part VI — Reference Tables

### A. Build Index

| # | Build | Author | Category | Repo / Link | License |
|---|---|---|---|---|---|
| 1 | **7-Second Flight Search** | Browser Use | Serious / Ship-It | `github.com/browser-use/jev-ultrafast` | Permissive |
| 2 | **Real-Time Super Mario** | Faadil Shaik | Silly but instructive | `github.com/fhshaik/typesafe-mario` | — |
| 3 | **YouTube Sponsor Skipper** | Tony Dinh | Installable tool | `github.com/trungdq88/youtube-sponsor-detection` | ⚠️ **None yet** |
| 4 | **Downloads Organizer** | Marcel Pociot | Installable tool | — | — |
| 5 | **Feed Cleaner (NL rules)** | Marcel Pociot | Demo | — | — |
| 6 | **1-Second UI Assembly** | json-render / Michael Tetteh Akula | Contested | — | — |
| 7 | **Claude Code Compactor** | Tamara Tran | Unproven | `github.com/tamaratran/fast-jev-compaction` | — |
| 8 | **JFK ATC Simulator** | Reddit builder | Spectacle / stress test | — | — |
| 9 | **Kill My Idea** | stemonte | Demonstrative only | `killmyidea.stemonte.io` | — |
| 10 | **World's Worst Chatbot** | mkotlikov / finetuningsingh | Joke | — | — |
| — | **OpenJev / SemIf** | Theo Lee | Open-source clone | `github.com/TheoLeeCJ/SemIf` | Open source |
| — | **Jev (the model)** | TypeSafe / Diogo Almeida | — | `typesafe.ai/blog/introducing-system-one-models-and-jev` | Commercial |

### B. Pattern-to-Build Cross-Reference

| Pattern | Builds |
|---|---|
| 1 Typed Choice / Closed Menu | All (foundational) |
| 2 System One vs. Two | All (framing) |
| 3 Batch Multi-Question | 1, 2, 9 |
| 4 Calibrated Decisions | 7, OpenJev (audit) |
| 5 Menu-as-Safety-Boundary | 6, all |
| 6 Prose-From-Choices | 10 |
| 7 State Menu ≠ Screenshot | 1, 2 |
| 8 Two-Tier Policy / Payload | 1 |
| 9 Fixed-Cadence + Scalar | 2 |
| 10 Streaming Per-Unit | 3, 5 |
| 11 Daemon-Scale Repetition | 4 |
| 12 Compose From Trusted Components | 6 |
| 13 Structural Compaction | 7 |
| 14 Parallel Fan-Out | 9 |
| 15 Simulation as Stress Bench | 8 |
| 16 Open-Source Local Reimpl. | OpenJev |
| 17 Format ≠ Judgment | Audit |
| 18 Unmeasured Guarantee | Audit |
| 19 Agreement-as-Accuracy | Audit |
| 20 Company Grades Own Homework | Audit |
| 21 Dramatized Mock-Up | 7 |

### C. Quantitative Claims Register

| Claim | Value | Status |
|---|---|---|
| Input price | $0.04 / million words | Company-stated |
| Output price | Free | Company-stated |
| Latency | 70–500 ms | Company-stated |
| Flight search: browser calls | 1,092 → 101 | Team-reported, demo unedited |
| Flight search: wall time | 9.5s → 7s | Team-reported, demo unedited |
| Flight search: cost | ~$0.0039 / run | Team-reported |
| Flight search: adoption | 9,000 users / 3 days | Team-reported |
| Sponsor skip cost | ~$0.005 / video | Author estimate |
| Mario decision cadence | every 8 frames | Repo |
| Mario move menu | 7 moves | Repo |
| Compaction drop rate | **0%** across 5 sessions | Independent run |
| OpenJev accuracy | **~85%** | Independent |
| Jev accuracy (reported) | **88%** | Company-stated |
| Jev agreement w/ panel | **~68%** | Company self-check |
| Speed (independent) | **~25×** (0.33s vs ~9s) | Independent |
| Speed (marketed) | 40–200× / 20× | **Company-stated, self-contradictory** |
| "Zero hallucinations" | **Not measured** | Company concession |
| Jev calls (flight) | 22 → 17 | Team-reported |

---

## Part VII — Closing Assessment

### The repeatable shape
Every successful build reduces to one motion:

> **Hand the model a state and a menu. Get back a typed decision.**

Everything else — the DOM list, the emulator telemetry, the file event, the second of audio, the component palette — is just a way of producing the state.

### The two questions that decide fitness
1. **Is the decision high-frequency and low-content?** If yes, the pricing model wins outright.
2. **Is a wrong call easy to catch?** If yes, validity-without-correctness is an acceptable bargain. If no — the compaction case — you are trusting an unverified confidence score with something you cannot audit after the fact.

### The honest summary
The mechanism is genuinely new and useful. The benchmark claims are not proven by anyone outside the company. Both statements are true at once, and the discipline is to hold them together rather than letting the marketing blend them.

> **Judge Jev on the decisions it makes, not the sentences it won't write.**

---

*Document compiled from the Cloud Codes presentation "10 Wild Things You Can Build With Jev" (https://youtu.be/X4Lqj54sw4I). All quotes, figures, and caveats are as reported in that presentation. Independent measurements are identified as such; company-stated figures are labelled throughout.*

---

## See also

This dossier is Volume I of three. Each answers a different question.

| | Volume I (this) | [Volume II — Handbook](jev-design-patterns-handbook.md) | [Volume III — Benchmark Report](jev-benchmark-report.md) |
|---|---|---|---|
| **Question** | What did they build? | How should you build? | **What actually performs best?** |
| **Authority** | Third-party observation | Vendor documentation | **Independent measurement** |
| **Tone** | Auditing claims | Teaching usage | **Measuring** |

**Volume II** documents the vendor's own named pattern set: the three primitives (Choice, Score, Noul), the ten decision shapes, and the four official design patterns.

**Volume III is the independent test this dossier said was missing.** It validates the broad verdict — the mechanism is sound, the marketing overreached — but the numbers are now measured rather than asserted. Its most important finding for this volume: Volume I's *Format ≠ Judgment* pattern turned out to be the organizing insight of the whole benchmark, and the measured accuracy (~95% against real answer keys) supersedes the ~68% agreement figure reported here.

> **Read Volume II to learn how to build. Read Volume III to choose. Read this dossier to know what to believe.**
