# The Jev Production Playbook
## Deployment Economics — Jev + Treg in Real Automation Workflows

**Compiled:** September 29, 2026
**Source presentation:** AI Jason — *Jev + Treg is a crazy combo for automation...* (14:29, published Sep 21, 2026)
**Source URL:** https://youtu.be/o4Vi5uBZYH0
**Primary sources:** [treg](https://github.com/superdesigndev/treg) (Apache 2.0, 3.8k ★) · [treg.to/jev](https://treg.to/jev) · workshop at [treg.to/jev](https://treg.to/jev)

**Companion volumes:** [Launch Week Dossier](jev-launch-week-dossier.md) · [Pattern Handbook](jev-design-patterns-handbook.md) · [Benchmark Report](jev-benchmark-report.md)

---

## Preface — The Fourth Layer

The first three volumes established what the model is, how to build with it, and how it performs. **This volume answers the question that decides whether any of it ships: does the economics close?**

| | I — Dossier | II — Handbook | III — Benchmark | **IV — Playbook** |
|---|---|---|---|---|
| **Question** | What did they build? | How should you build? | What performs best? | **Does it pay for itself?** |
| **Authority** | Third-party observation | Vendor docs | Independent measurement | **Practitioner deployment** |
| **Unit** | Applications | Decisions | Model profiles | **Workflows and dollars** |

### What makes this volume different — and why it's the most useful one

Volumes I–III all analyze **the model**. This volume analyzes **the economics of a workflow** — and its central insight is that the second half of the equation is not the model at all.

The presenter runs two live products (Superdesign, a vibe-design platform; Treg, an "OpenRouter for agent tools"). His team's production pipelines pair a cheap decision model with a cheap data layer. **Neither half was affordable before; together they made a category of automation newly viable.**

> *"The workflow like this before Jev and Treg emerge is very difficult to do because the unique economy just didn't make sense."*

### The correction this volume carries

Volume I flagged TypeSafe's "200× faster / 444× cheaper" claims as unsupported. **This volume's primary source independently measured them — and asked for the same discipline.**

From `treg.to/jev`:

> *"TypeSafe's own workflow demo claims far more (193.6× faster, 444.6× cheaper); these are our numbers."*

Their measured figures: **5–6× cheaper and 5–7× faster** than GPT-5.6 Luna, the cheapest chat model they could find.

**Volume I's audit pattern 20 — *Company Grades Own Homework* — is confirmed for the fourth time, now with a competing practitioner publishing the counter-measurement.**

---

## Part I — The Problem Jev Actually Solves

The presentation opens with a question worth preserving, because it names the gap precisely.

> **Frontier models handle Olympic-math-level problems brilliantly — and still can't be trusted with a basic business workflow.**

Ask a model to handle a customer enquiry involving billing, and most companies will not let it decide autonomously. Two reasons.

### Reason 1 — Overconfidence

> *"You definitely experience agents just saying 'you're absolutely right.' And in fact, it is absolutely wrong. The model today will make a judgment call like this without calibrating the actual confidence. While most business workflows require almost 100% accuracy. That's why humans are good."*

### Reason 2 — Cost and speed at scale

> *"Many business workflows have huge scale volume."*

You cannot spend frontier-model money on every signup, every document, every tweet.

**And the presenter identifies the root cause of both:**

> *"The reason large models have those factors is baked into the results from the training process. The large language models today all go through this reinforcement learning from human feedback process, where the model will be fine-tuned based on feedback that humans give in chat assistant."*

RLHF optimizes for being **helpful in conversation** — which trains fluency and confidence, not calibration. Jev's alternative is **reinforcement learning for calibrated decisions**, which optimizes for being *right and knowing how right*.

### What that buys you

> *"This is a game-changer, because for business automation you can finally trust a model to operate fully autonomously — because every answer it gives comes with this confidence score that you can build business logic around."*

**The confidence score is the product.** Volume II documented it as a primitive property; this volume shows what it's *for*.

---

## Part II — The Model's Shape, From a Practitioner

### What it is

> *"A model that is designed for reliable, high-quality decision making rather than being creative or assisting humans. Basically it is a model designed to make a decision given a set of options — but it cannot make up options itself, and it cannot output text, it cannot write code, it cannot reason step by step."*

> *"Unlike a normal language model, where they output results token by token, Jev does not predict text but outputs probability of a list of given answers in an extremely fast and efficient approach."*

**The honest framing:** *"At a high level it might feel a bit limited, but it is just so much faster and cheaper than even the cheapest large model out there."*

### The measured comparison — and the discipline behind it

The presentation says **5–7× faster and 5× cheaper** against GPT-5.6 Luna. The primary source breaks it down properly, with input padded by real support tickets from 2k to 200k tokens:

| Input | Jev cost | Jev time | Luna cost | Luna time | Jev advantage |
|---|---:|---:|---:|---:|---|
| 2k | $0.0000755 | 0.39 s | $0.0001299 | 2.74 s | 1.7× cheaper / 7.0× faster |
| 8k | $0.0002248 | 0.40 s | $0.0013071 | 2.35 s | **5.8× / 5.9×** |
| 16k | $0.0004122 | 0.40 s | $0.0023791 | 2.46 s | **5.8× / 6.1×** |
| 32k | $0.0008031 | 0.51 s | $0.0045953 | 2.29 s | **5.7× / 4.5×** |
| 34k | **over limit** | — | $0.0080371 | 3.59 s | — |
| 100k | **over limit** | — | $0.0233656 | 3.03 s | — |
| 200k | **over limit** | — | $0.0467147 | 3.89 s | — |

**Two structural observations the table makes unavoidable:**

1. **Jev's time barely moves with input** (0.39 s → 0.51 s across a 16× input increase) because **it never writes**. Luna's time is dominated by producing ~80 output tokens, so it sits at 2–4 s regardless.
2. **Jev stops at ~30k tokens.** Above that you chunk the state yourself.

> **The measured conclusion:** *"Where both run, Jev is 5 to 6× cheaper and 5 to 7× faster, and its time barely moves with input because it never writes."*

At ~$0.0008 per 32k-token decision, the primary source estimates **≈ $20 per million decisions.**

### The capability boundary — stated cleanly

The `treg.to/jev` page draws the line better than anything in the first three volumes:

| **CAN** | **CAN'T** |
|---|---|
| Pick an action from your options, with a probability on each | **Write a sentence** — an LLM writes; Jev verifies each field |
| Classify (`billing 0.99 · technical 0.01 · account 0.00`) | **Explain itself** — *"the distribution is the explanation: log it"* |
| Score / rank — 368 people in 42.8 s, $0.013 | **Write code** — it can *judge* code: risky change, needs review |
| Say yes/no — jailbreak 0.99, four hazards in one call | **Reason step by step** — you write the steps as questions |
| Route on confidence — two thresholds in your code, nothing re-run | **Read past ~30k tokens** — chunk, or summarise then judge the summary |
| Read your JSON as-is — rows, tables, element lists, ticket histories | **Fetch anything** — that's the data layer's job |
| At 5–7× a chat model's speed and 5–6× cheaper | **Remember the last call** — every request is stateless; put history in the state |

**"It is a judge, not a writer."** That single line is the clearest statement of the paradigm in any of the four volumes.

### The three question types, from the practitioner

Not a re-derivation — an operational framing.

| Type | Shape | The presentation's example |
|---|---|---|
| **Choice** | Pick one of your options | *"Which department should handle this request?"* |
| **Noul** | Yes/no as a probability | *"Is this prompt a jailbreak? true or false"* — for an AI chat platform's injection guard |
| **Score** | Position on your ordered rubric | *"Is this Twitter post organic or paid advertisement, based on engagement stats?"* |

**On Score specifically:** *"You can give different criteria ranging from 'clearly manipulated' to 'suspicious' to 'probably organic' to 'clearly organic.' Each new option you add will plus one on the index and Jev will output probability for each option and give you a final score."*

### The context-window workaround

> *"One thing to be aware of is that Jev has this context window of 32K. If your response is bigger, currently it can't handle it — or you will have to do things like map-reduce to work around it."*

**Volume III measured this empirically:** the ABCD full-handbook condition ran at ~19.5–21K tokens, comfortably inside, and Jev's latency went from 245 ms (short) to 358 ms (full handbook). The practical ceiling is real but generous for most support workflows.

---

## Part III — The Confidence Decision Tree

The presentation's most directly reusable artifact: a three-band routing policy built entirely on the confidence score.

### Worked example: prompt-injection guard

Send **every** user request to Jev with the question *"is this a jailbreak?"* and detailed instructions. Jev returns a probability. Then:

```python
if hazard_score > 0.70:
    block()                    # automatically block the message
elif 0.35 < jailbreak_score <= 0.70:
    ask_human_for_review()     # flag for review
else:
    send_as_normal()           # pass through
```

> *"This is one example of how you can build really sophisticated business logic based on the confidence score from Jev."*

### The richer version from the primary source

The `treg.to/jev` page publishes TypeSafe's guardrail cookbook pattern in full — **one call per message, four hazard Nouls plus a severity score, about $0.00002:**

```python
review_threshold = 0.35
action_threshold = 0.70
severity_block   = 2.0

action = {
    "jailbreak": "block",
    "harmful":   "block",
    "medical":   "review",
    "self_harm": "support",
}
```

> *"Edit the two numbers and the same assessments route differently, nothing is re-run."*

**This is Volume II's *Confidence-Gated Routing* pattern, deployed.** The key property: **the model's assessment is cached and reusable.** Change your policy, re-route the same answers, pay nothing.

### Why this works and chat models don't

Volume I's audit found TypeSafe's calibration claims unverified. Volume III measured the aggregate accuracy. **This volume supplies the operational argument:**

> Most business workflows require *almost 100% accuracy*. A confidence score lets you achieve that **not by making every decision correct, but by routing the uncertain ones to a human** — which is exactly what a well-run human process already does.

The three-band structure is not a compromise. It is how the work was always done; Jev just makes the first and third bands cheap enough to automate.

---

## Part IV — Steering: There Is No System Prompt

A genuinely important operational fact, and the primary source states it plainly:

> **There is no system prompt. Everything you would say in one goes into the question itself.**

And every text field also accepts structure: `instructions`, each option under `criteria`, each level of a score. **Jev reads the keys as well as the values.**

### The three shapes of the same question

**1 — A string.** The minimum. One sentence per field.

```json
{
  "department": {
    "type": "choice",
    "instructions": "Which team should handle this?",
    "criteria": {
      "billing": "Charges, invoices, credits",
      "technical": "Bugs, errors, integrations"
    }
  }
}
```

**2 — Instructions as an object.** Keys are yours to name; none is reserved.

```json
{
  "type": "choice",
  "instructions": {
    "question": "Which team should handle this?",
    "focus": "Route to whoever must fix the root cause."
  },
  "criteria": { "...": "same as 1" }
}
```

**3 — Options as rubrics.** Each option says what it covers, what it does **not**, and what it looks like.

```json
{
  "criteria": {
    "billing": {
      "what": "charges, invoices, credits, refunds",
      "not_for": "a bug that caused a wrong charge",
      "examples": ["I was charged twice", "Where is my refund?"]
    },
    "technical": {
      "what": "bugs, errors, integrations",
      "not_for": "a correct charge the customer disputes",
      "examples": ["The export is empty", "API returns 500"]
    }
  }
}
```

> Score levels take the same shape with `summary` and `signals`.

### The measured effect of steering

The presentation demonstrates this with a real ticket:

> *"The export button double-charged my credits, so my invoice is wrong this month."*

| Instructions | Result |
|---|---|
| **Simple:** *"Which team should handle this?"* | Routes to **billing** (confidence 0.99) — it's a double-charge |
| **Steered:** `"focus": "route to whoever must fix the root cause"` | **Flips to technical** |

The primary source quantifies a related effect:

> *"Strip the options back to one-line labels and a tenth of the mass moves to `technical`, because a bug caused it; add `"focus": "route to whoever must fix the root cause"` and the same message flips."*

> **The rubric is where your routing policy lives.**

### This is Volume II's advice, now measured

Volume II documented *structured criteria for confusable options* and *the level-examples trap* (a relevant example took confidence 0.35 → 0.96; an unrelated one changed nothing). **This volume confirms the same mechanism from a production deployment** — and adds the finding that a single `focus` key can flip an answer outright.

**The practical rule:** when a model keeps misclassifying something, you have three escalating levers — a better `what`, a `not_for` that names the confusion, and a `focus` that redirects the policy.

---

## Part V — The Two-Tool Thesis

This is the volume's core argument, and it is not about Jev at all.

### What Treg is

> **OpenRouter, but for agent tools instead of models.** One base URL, one token, a curated catalog of thousands of endpoints across many providers — SEO and backlinks, social and trends, people and company enrichment, ads, scraping, image and video generation — **priced per call, from a cent, with no provider signup.**

The problem it solves:

> *"The tools an agent needs for real work sit behind subscriptions nobody buys for a single run — Semrush $139/mo, Moz $99/mo, Crunchbase $99/mo, Apollo $59/seat — behind signup walls, or behind no public API at all."*

Three design properties worth noting:

1. **"Ask for the task, not the tool."** You search by what you want to *do*, not by vendor:
   ```
   treg catalog search "backlinks for a domain"
   treg catalog search "find a work email"
   ```
2. **The faithful-relay contract.** The proxy alters **only** three things — hop-by-hop headers, its own control headers, and the injected credential. Everything else is verbatim. *"The proxy relays, never models the upstream."*
3. **Credential precedence.** *"Your own key always wins over Treg's, and those calls are never metered."* Connecting a key you already pay for makes those calls free rather than duplicating spend.

### The economics that changed

**Measured, from the presentation:**

| Workload | Treg | Alternative | Advantage |
|---|---|---|---|
| Enrich ~290 people | **$1.49** | Clay **$9–10.30** | **~85% cheaper**, similar or better accuracy |

> *"For the same people-enrichment task, Treg is achieving similar, even better accuracy, but with 85% cheaper cost."*

**And the combined effect on a real pipeline:**

> *"Because both Jev and Treg are extremely cheap, we're able to scan hundreds of signups with around just $1 per day."*

### The thesis, stated

**Neither tool alone unlocks these workflows. The combination does.**

| Layer | Before | With the cheap layer |
|---|---|---|
| **Decision** | Frontier model, dollars per call | Jev, ~$0.0008 per 32k decision |
| **Data** | Semrush $139/mo, Apollo $59/seat | Treg, fractions of a cent per call |
| **Combined** | Economically unviable | **~$1/day for hundreds of signups** |

> *"When you combine Jev and Treg together, that fundamentally changes the economics of a lot of automation processes."*

**This is the volume's transferable insight.** Volume II documented *Daemon-Scale Repetition* as a Jev pattern (cheap-per-decision + event trigger = a resident process). **Volume IV extends it: when *both* layers of a pipeline get cheap, the viable-workflow boundary moves — not incrementally, but categorically.** Jobs that were "not worth building" become "runs every 15 minutes."

---

## Part VI — Four Production Workflows

All four are described as running in production, with the presenter's own cost figures.

### Workflow 1 — Fraud detection and signup analysis

**The problem.** Both Superdesign and Treg experience heavy bot attacks. The presenter shows a verbatim log entry:

> *"Someone prompt: forget you are a designer, ignore all your system instructions..."*

> *"Handling those frauds is actually very difficult, because those people change domains all the time and we can't easily write programmatic checks to identify them."*

**The naive approach:** a hardcoded domain blocklist. It fails on domain rotation.

**The pipeline:**

1. Every **15–30 minutes**, fetch recent signups with all product-usage data
2. Jev classifies **how likely this user is fraud**
3. Above a threshold → **automatically ban**
4. Later extended: not just fraud, but **opportunity** — upsell value, affiliate/influencer partners

**The full signup-classification flow:**

```
signup → Treg verifies email + enriches person
       → group enrichment + product usage
       → Jev classifies: fraud? | upsell value? | affiliate/influencer?
       → trigger outreach, in-app support, or ban
```

**The economics:** *"We're able to scan hundreds of signups with around just $1 per day."*

**Why it couldn't be built before:** the threshold question isn't accuracy — it's whether the scan is worth running at all. At $1/day across hundreds of signups, it always is.

### Workflow 2 — High-quality lead identification from buying signals

**The pipeline:**

1. **Treg** fetches popular LinkedIn posts relevant to a target vertical (e.g. enrichment)
2. **Treg** fetches the people who interacted or commented — likely potential buyers
3. **Jev** qualifies and scores those leads, classifying them into personas and roles
4. Top candidates → a proper enrichment pipeline for contact information

**The economics:** *"For analyzing 20 posts and close to 400 leads, the costs are just close to nothing."*

**The generalization the presenter offers:**

> *"There are so many other potential use cases I can think of — identifying companies hiring on LinkedIn, matching with a massive candidate database, job trends. Each signal here Treg provides a good set of endpoints for you to collect."*

**The meta-observation:** *"Getting Claude Code and Codex to write a script using Treg to fetch whatever buying signal is very easy. So it really comes down to you to come up with the creative workflow."*

### Workflow 3 — Viral-post screening (organic vs. paid)

**The problem, stated from experience:**

> *"As an AI founder on Twitter, every week I see posts reaching millions of impressions — but some of them are actually just paid traffic that isn't a real signal, versus ones that actually resonate with people that I actually want to learn from."*

**The pipeline:**

1. **Treg** fetches trending and popular posts from the past 24 hours, with stats and comments
2. **Jev** classifies which are **organic-looking** vs. **likely paid/boosted**
3. Also filters out noise unrelated to product launches
4. Result: a daily feed of genuinely resonant trends

**The insight:** this is a *classification* task where the labels are subjective and no ground truth exists — the ideal shape for a calibrated judgment rather than a rule.

### Workflow 4 — Internal link mapping at SEO scale

**The problem:** internal linking requires a model to race through hundreds of pages and accurately locate which pages should link to which.

> *"With a normal model like Claude Opus 5, it can take hours."*

**The result, from an independent practitioner published on `treg.to/jev`:**

| Metric | Value |
|---|---:|
| Pages scanned | **586** |
| Time | **45.1 s** |
| Total cost | **$0.21** |
| Links placed | 584 |
| Pages refused (no real reason to link) | 139 |
| **Comparison — Claude Opus 5** | 21 pages, **$1.43** |
| **Advantage** | **≈ 190× cheaper per page** |

The framing is what makes it click:

> *"Internal linking is not writing — it is **8,790 yes/no calls.** Does this page have a real reason to link to that one, and is the anchor text already in the copy?"*

**Decompose a creative-sounding task into atomic judgments, and it becomes cheap.** This is Volume II's decomposition principle with a price tag attached.

### Bonus — three more measured deployments

From `treg.to/jev`, all independently reported by named practitioners:

| Use case | Result | Source |
|---|---|---|
| **Game loop** | Seven ticks of a side-scroller, judged live from game state — **~0.35 s, $0.00002 per decision**. A chat model writing *"I would press jump"* took 2.7 s | @bryantchou |
| **Page that picks itself** | **25 ms** per page load, **no real impact on LCP** — Jev selects copy *and* design per section per visitor segment at load time | @bryantchou |
| **Search without an index** | Thousands of listings scanned in **< 20 s for $0.18** — filtering on architecture, renovation status, freeway proximity. *"No index, no embeddings, no vector column"* | @venturetwins |

**The search case deserves attention:** filtering on attributes **no column holds** — judged from the listing text directly. *"The query is a sentence and every record is judged against it."*

---

## Part VII — The Independence Ledger

Across four volumes, a pattern has emerged: **every independent measurement lands below the vendor's own claim.** This is worth tabulating explicitly, because it is the most reliable finding in the entire series.

| Claim | Vendor's number | Independent measurement | Source |
|---|---|---|---|
| **Speed vs. a frontier model** | **193.6× faster** | **5–7× faster** | treg.to/jev |
| **Cost vs. a frontier model** | **444.6× cheaper** | **5–6× cheaper** | treg.to/jev |
| **Speed (Volume I)** | **200×** (elsewhere 40×, 20×) | **~25×** | Volume I audit |
| **Accuracy** | **"Zero hallucinations"** (unmeasured) | **95.23%** label agreement | Volume III |
| **Compaction** | Demo implied lossless | **0% dropped** at safe threshold | Volume I audit |
| **Signup scanning** | — | **~$1/day** for hundreds | This volume |

**Four independent sources. Four consistent downward revisions.**

> **The transferable discipline:** when a vendor publishes a multiplier with no methodology, expect the independent number to be **one to two orders of magnitude smaller** — and still good enough to matter.

**And note the honest framing from the primary source:** *"these are our numbers."* A competitor publishing its own measured figures alongside the vendor's inflated ones, explicitly labelling which is which, is the behavior Volume I's pattern 23 — *Published Caveats Beat Published Wins* — was written to reward.

### The precision that must be preserved

With such large revisions, the temptation is to dismiss the claims entirely. **Don't.** The corrected numbers still describe a genuinely different cost structure:

- **5–6× cheaper and 5–7× faster** than the cheapest available chat model
- **~$0.0008 per 32k-token decision**, ≈ $20 per million decisions
- **190× cheaper per page** than Opus 5 on internal-link auditing
- **586 pages in 45 seconds for $0.21**

**A 5× improvement that actually holds is a bigger deal than a 200× claim that doesn't.** The workflows in Part VI exist because the real numbers close.

---

## Part VIII — What This Volume Adds to the Pattern Set

Volume I's Family B catalogued agent and integration patterns. **This volume supplies three more, all from production deployment rather than observation.**

### 24 — Cheap-Layer Pairing (the Economics Threshold)

> **A workflow becomes viable when *every* layer of its pipeline gets cheap — not when one does.**

The fraud pipeline needs a cheap decision model *and* a cheap data layer. Either alone leaves the workflow unaffordable. The economic threshold is a property of the **pipeline**, not the model.

**Diagnostic:** when evaluating a new cheap component, ask what the *rest* of the pipeline costs. The bottleneck is usually not where you're looking.

### 25 — Confidence-Banded Autonomy

> **Build three bands — act / review / pass — and tune the two thresholds, not the model.**

The prompt-injection guard, the fraud classifier, and TypeSafe's own guardrail cookbook all use the same shape: a high band that acts automatically, a middle band routed to a human, and a low band that passes through.

**Why it matters:** most business workflows require near-100% accuracy. The band structure achieves that **not by making every decision correct, but by making the uncertain ones cheap to escalate.** Because the assessment is cached, re-tuning thresholds costs nothing — you re-route the same answers.

### 26 — Decompose the Creative-Sounding Task

> **A task that sounds like judgment is often hundreds of atomic judgments wearing a costume.**

**Internal linking is not writing — it is 8,790 yes/no calls.** Once decomposed, a task that took hours on a frontier model takes 45 seconds for $0.21.

**Diagnostic:** when a task "needs a smart model," ask what the smallest question is and how many times you'd ask it. Volume II's *decompose the questions* step said this; this volume prices it.

---

## Part IX — Reference Tables

### A. The measured cost table (32k input, single runs)

| | Jev | GPT-5.6 Luna | Advantage |
|---|---:|---:|---|
| Cost | $0.0008031 | $0.0045953 | **5.7× cheaper** |
| Time | 0.51 s | 2.29 s | **4.5× faster** |
| Output tokens | **0** | ~80 | — |
| Works at 100k tokens? | **No** | Yes ($0.0233656) | — |
| Works at 200k tokens? | **No** | Yes ($0.0467147) | — |

### B. Production workflow economics

| Workflow | Volume | Cost | Per-unit |
|---|---|---|---|
| Signup fraud scan | Hundreds/day | **~$1/day** | ~$0.005–0.01 each |
| Lead qualification | 20 posts, ~400 leads | *"Close to nothing"* | — |
| People enrichment | 290 people | **$1.49** | ~$0.005 each |
| Internal link audit | 586 pages | **$0.21** | **$0.00036/page** |
| Jailbreak guard | Per message | **~$0.00002** | — |
| Game tick | Per decision | **$0.00002** | — |
| Page-variant selection | Per page load | 25 ms | — |

### C. Tool-layer comparison

| | Treg | Alternatives |
|---|---|---|
| Enrichment, 290 people | **$1.49** | Clay **$9–10.30** |
| Access model | Per call, from a cent | Semrush $139/mo · Moz $99/mo · Crunchbase $99/mo · Apollo $59/seat |
| Own keys | **Free, never metered** | — |
| New verified team | **$1.00 free** once | — |

### D. Model capability boundary

| Can | Can't |
|---|---|
| Choose from your options, with probabilities | Write a sentence |
| Classify, score, rank | Explain itself |
| Yes/no with calibrated confidence | Write code (but can *judge* code) |
| Route on confidence | Reason step by step |
| Read structured JSON as state | Read past ~30k tokens |
| Operate at 5–7× chat speed | Fetch anything, or remember the last call |

### E. Resource index

| Resource | URL |
|---|---|
| Presentation | https://youtu.be/o4Vi5uBZYH0 |
| Treg repo (Apache 2.0) | https://github.com/superdesigndev/treg |
| Jev + Treg recipes | https://treg.to/jev |
| TypeSafe console | https://console.typesafe.ai |
| AI Builder Club workshop | https://www.aibuilderclub.com |

---

## Closing Assessment

### The four-volume picture

| Volume | Answers | Read it for |
|---|---|---|
| **I — Launch Week Dossier** | What was built, and did the claims hold? | Knowing what to be skeptical of |
| **II — Pattern Handbook** | How does TypeSafe say you should build? | Knowing how to build |
| **III — Benchmark Report** | What actually performs best, measured? | Knowing what to choose |
| **IV — Production Playbook** | Does the economics close in production? | **Knowing whether to build it at all** |

### What this volume settles

**The economics close — and the second layer is the interesting part.**

Volume III answered "which decision model?" Volume IV answers the question that comes *after*: what does the whole pipeline cost? The answer is that a cheap decision model paired with a cheap data layer moves a category of automation from "not worth building" to "runs every 15 minutes for $1 a day."

**The confidence score is the operative feature.** Not accuracy — *banded autonomy*. A model that knows when it doesn't know can be trusted with the band it's good at, and the rest goes to a human. That's how the work was always done; Jev makes two of the three bands nearly free.

**"It is a judge, not a writer."** The cleanest formulation of the paradigm across all four volumes, and the one that most quickly tells you whether a task fits.

### And the discipline this volume reinforces

**Every independent measurement lands below the vendor's claim** — and this volume supplies the widest gap yet: **193.6× claimed, 5–7× measured.**

The correct response is neither cynicism nor acceptance. It is to notice that **a 5× cost advantage that survives independent testing is a more valuable fact than a 200× one that doesn't** — and to build the fraud pipeline, the lead-screening workflow, and the $0.21 link audit on the measured numbers.

> **Read the Playbook to know whether to build it. Then check your own pipeline's other layers — that's where the real cost lives.**

---

*Compiled from AI Jason's presentation "Jev + Treg is a crazy combo for automation..." (https://youtu.be/o4Vi5uBZYH0) and the primary sources at [treg.to/jev](https://treg.to/jev) and [github.com/superdesigndev/treg](https://github.com/superdesigndev/treg). Cost and latency figures are the primary source's own measurements ("single runs," cost as billed by OpenRouter), explicitly distinguished there from TypeSafe's vendor claims, which are quoted for comparison. Third-party practitioner figures (internal-link audit, game loop, page-variant selection, search) are attributed to their named sources.*
