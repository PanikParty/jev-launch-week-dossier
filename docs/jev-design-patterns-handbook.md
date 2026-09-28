# The Jev Design Pattern Handbook
## The Official TypeSafe Pattern Set — Three Primitives, Ten Decision Shapes, Four Design Patterns

**Compiled:** September 28, 2026
**Source presentation:** The AI Automators — *Master ALL Jev Design Patterns (With Practical Examples)* (14:20, published Sep 25, 2026)
**Source URL:** https://youtu.be/LzweTaOzvVo
**Primary documentation:** docs.typesafe.ai — [Introduction](https://docs.typesafe.ai/introduction) · [Primitives](https://docs.typesafe.ai/primitives) · [Patterns](https://docs.typesafe.ai/patterns) · [Confidence](https://docs.typesafe.ai/confidence)

**Companion volumes:** [The Jev Launch Week Dossier](jev-launch-week-dossier.md) — the ten community builds and the 21 patterns they reveal. · [The Jev Benchmark Report](jev-benchmark-report.md) — independent measurement: which decision models actually perform best.

---

## Preface — What This Volume Is, and How It Differs

The Launch Week Dossier documents what developers **built** in six days. This volume documents what TypeSafe **designed** — the vendor's own canonical, documented pattern vocabulary, taught with practical worked examples.

The two are not the same layer, and neither supersedes the other.

| | Launch Week Dossier | This Handbook |
|---|---|---|
| **Subject** | Community builds | Vendor's official pattern set |
| **Authority** | Third-party observation | Primary documentation |
| **Unit of analysis** | Whole applications | Atomic decisions and their composition |
| **Answer to "what is a pattern?"** | Reverse-engineered from mechanics | Stated by the vendor, with names |
| **Tone** | Auditing claims | Teaching usage |

**The critical distinction:** the Launch Week Dossier's Family B patterns (State Menu ≠ Screenshot, Daemon-Scale Repetition, Structural Compaction) were *authored* — reverse-engineered from how builds worked. **Every pattern in this volume is named and defined by TypeSafe itself.** Where the two vocabularies overlap, this volume's terms are the canonical ones.

**The most important thing in this document:** the parallel-questions benchmark. Batching 13 questions into one call is **12.2× cheaper and 10.0× faster** than 13 separate calls — with *identical answers*. That single result explains why almost every pattern here takes the shape it does.

---

## Part I — Where Jev Fits

### The category

> **Jev isn't a chat model. It's a decision model.**

You give it context and a question; it returns an answer your software can act on. The judgments are the fuzzy micro-decisions that were previously too expensive or too slow to hand to an LLM:

- Which team should handle an inbound message?
- Is a customer review reporting a defect?
- What product should be recommended for this situation?

### The five opportunity categories

TypeSafe groups the opportunities into five broad areas.

| # | Category | What it looks like |
|---|---|---|
| 1 | **Automation** | An inbound support message becomes a prioritized task in the right queue; a supplier email is identified as an invoice query and sent to accounts payable. |
| 2 | **Real-time applications** | Frontier intelligence at ~150ms — faster than humans can perceive. Games (Doom, Mario), but also a drawing app where "make something bigger" triggers the action near-instantly. |
| 3 | **Data processing at scale** | Analyze time-series en masse; check product reviews for recurring complaints; scan support transcripts for known problems. Classify once, then total with ordinary code across months, versions, products. |
| 4 | **Verification** | Does a citation actually support the claim beside it? Does a drafted support reply promise a refund the policy doesn't permit? Every one of these used to require another LLM call. |
| 5 | **Harness engineering** | The software around an AI agent (Claude Code, Codex) or a custom piece of software you create. |

### The token economics that make it work

| Metric | Value |
|---|---|
| Jev list price | **4.2 US cents per million input tokens** |
| Output tokens | **$0.00** — not charged |
| A 1,000-token request | ~$0.000042 |
| **1 million such requests** | **~$42** |

That arithmetic is what makes *repeated* fuzzy decisions interesting. Once a decision costs effectively nothing, you can consider checks across entire collections of records, or several checks inside a single workflow, at scale.

### Why this is bigger than one vendor

The presentation makes a point worth preserving:

> This isn't specific to Jev. With the success of this model in the space of a week, we are guaranteed to see a wave of new decision models — both proprietary and open source — that we can deploy locally.

**The patterns in this volume are model-agnostic.** They describe how to organize typed decisions into a working system, not how to call one company's API.

---

## Part II — The Three Primitives (Decision Types)

### The paradigm shift

> LLMs are designed to produce text for humans to read. When you need a model to make a judgment that your **code** will consume, that creates a mismatch: you are coercing a text-generation system into outputting structured decisions, then **parsing the results back** into something your code can depend on.

Jev eliminates the parsing step. It evaluates typed *questions* against a *state* and returns typed values and probability distributions directly.

| Primitive | Goal | Returns |
|---|---|---|
| **Choice** | Choose an option from a list | `choice`, `probabilities`, `confidence` |
| **Score** | Score the state on a rubric | `score`, `legend`, `probabilities`, `confidence` |
| **Noul** | Is this statement true? | `noul` (0 to 1) |

All three can be mixed in a single API call. Every question is evaluated **in parallel and in isolation** against the same state in one go.

### Type 1 — Choice: pick one option

**Use when** the answer is one of a fixed set of options with no order between them.

```json
{
  "department": {
    "type": "choice",
    "instructions": "Which team should handle this?",
    "criteria": {
      "returns": "Exchanges, wrong or damaged items",
      "shipping": "Delivery status, delays, lost packages",
      "billing": "Charges, invoices, payment problems"
    }
  }
}
```

**Response:**

```json
{
  "department": {
    "type": "choice",
    "choice": "returns",
    "confidence": 1.0,
    "probabilities": { "shipping": 0.0, "returns": 1.0, "billing": 0.0 }
  }
}
```

| Field | Meaning |
|---|---|
| `choice` | The option with the highest probability |
| `probabilities` | Full distribution across every option; **sums to 1** |
| `confidence` | 0–1, computed from how peaked the distribution is |

**Design notes from the docs:**
- A Choice accepts **up to 255 options**. Adding options costs a few tokens each, so give the full list rather than a shortlist.
- Add an `other` or `none of the above` option when the list might not cover every input.
- Option names *and* descriptions are both sent to the model — write descriptions that separate the options from each other.

### Type 2 — Score: rate along ordered levels

**Use when** the answer is a position on a spectrum you can describe in steps.

```json
{
  "bug_severity": {
    "type": "score",
    "instructions": "How severe is the reported issue?",
    "criteria": [
      "Cosmetic; no impact to functionality",
      "Broken or degraded feature, but workaround exists",
      "Blocking issue; no workaround exists"
    ]
  }
}
```

**Response:**

```json
{
  "bug_severity": {
    "type": "score",
    "score": 1.43,
    "confidence": 0.35,
    "legend": {
      "0": "Cosmetic; no impact to functionality",
      "1": "Broken or degraded feature, but workaround exists",
      "2": "Blocking issue; no workaround exists"
    },
    "probabilities": { "0": 0.0, "1": 0.57, "2": 0.43 }
  }
}
```

**How the score is computed:** each level number × its probability, summed.
`0 × 0.0 + 1 × 0.57 + 2 × 0.43 = 1.43`

**The score can land *between* levels.** 1.43 means the model is split between levels 1 and 2, leaning to 1.

**Writing good levels — the two hard rules:**

1. **Describe situations, not degrees.** "Broken or degraded feature, but workaround exists" gives the model something to match against. "Moderately severe" does not.
2. **Every level is evaluated separately.** The model does not see a level's number or its neighbors. "Worse than the previous level" means nothing to it, and **numbers in the descriptions do not help**.

The docs demonstrate the failure mode directly. Given a misaligned-button report:

| Levels | Result |
|---|---|
| `["0", "1", "2"]` with "Rate severity 0 to 2" | score **0.55**, confidence **0.33** — split between 0 and 1 |
| The three descriptive levels above | score **0.0**, confidence **1.0** — correct |

**Additional guidance:**
- Use as many levels as you can describe distinctly, **up to 10**. Three is fine. Don't add levels you can't describe distinctly.
- **Keep each Score to one dimension.** If a description says "punctual and smart and experienced," the question measures three things and can't be placed. Split it and combine in code.
- Give a rare extreme case its own level. A sentiment scale ending at "very angry" should add "abusive or threatening" — otherwise both score near the top and the score alone can't distinguish them.
- If there's no in-between at all, use Choice instead.

### Type 3 — Noul: is this true?

**Use when** the answer is yes or no, and the probability itself is the useful signal.

```json
{
  "is_human_escalation": {
    "type": "noul",
    "instructions": "Is the customer asking for a human agent?"
  },
  "is_repeat_contact": {
    "type": "noul",
    "instructions": "Has the customer contacted support about this before?",
    "criteria": {
      "true": "Mentions a prior attempt, ticket, or that they have asked before",
      "false": "No sign of any previous contact"
    }
  }
}
```

**A Noul answer is a single number: the probability that the answer is yes.** Near 1 is a strong yes, near 0 a strong no, near 0.5 genuinely uncertain.

**There is no separate `confidence` for a Noul.** Its distribution has only two outcomes, so the single value describes it completely.

**Recorded `jev-1.13.0` answers** to *"Is the customer asking for a human agent?"*:

| State | `noul` |
|---|---|
| Thanks, that fixed it! | 0.02 |
| How do I reset my password? | 0.07 |
| I need this sorted today, whatever it takes. | 0.26 |
| Are you a bot? | 0.40 |
| Is there any way to speak to someone about my invoice? | 0.84 |
| I have asked three times now. Can I please just talk to a real person? | 0.99 |

Note the middle two. "I need this sorted today" is *urgent* but never asks for a person — 0.26. "Are you a bot?" *hints* at wanting a human without asking — 0.40, nearly even. **Both are exactly the cases where code needs a threshold.**

### The critical Noul gotcha: it is not a scale

> A Noul value runs from 0 to 1, but **it's not a scale of the thing you asked about.** It is the probability that the answer is yes. If the question is really about degree, the value does not measure the degree.

The docs contrast the same four candidates under a Noul and a Score:

| Candidate | Noul: *"Is the candidate strong in Python?"* | Score: *"How much Python experience?"* |
|---|---|---|
| Java and Go, never used Python | 0.03 | 0.0 (No experience) |
| Occasional small scripts | 0.14 | 1.0 (Some familiarity) |
| Daily for two years, data pipelines | 0.81 | 2.05 (Regular use in a job) |
| Daily for eight years, large Django codebase | 0.92 | 2.89 (Deep expertise) |

The Noul judges one proposition — "strong" — and the values are how likely it is. You *could* invent levels in the 0–1 range in your code, **but the model never saw them, so nothing was judged against them.** A middle value might mean medium experience or an unclear case; the spacing between candidates is not something you chose.

The Score judges each level description on its own, so every candidate landed on or near a level you wrote.

**Rule: use Noul for a yes/no judgment and Score to measure a position on a spectrum.**

**Other Noul rules:**
- **One yes/no question per Noul.** "Is the customer angry *and* asking for a refund?" makes the model judge both at once and the value means less. Ask two Nouls and combine in code.
- **Phrase so a high value means yes.** "Does the message contain personal data?" is clear. "Is the message *free of* personal data?" inverts the meaning and downstream code will get it backwards.
- **Make the yes/no boundary unambiguous.** "Does this candidate have *any* Python experience?" works because "any" leaves no middle ground. When the boundary is subtle, add `criteria` with `true`/`false` descriptions.

---

## Part III — The Ten Decision Shapes

The **type** tells you what comes back. The **shape** describes the job you're trying to do with it.

| # | Shape | Definition | Preferred type |
|---|---|---|---|
| 1 | **Classification** | Give something a category | Choice |
| 2 | **Detection** | Ask whether a property is present | Noul |
| 3 | **Scoring** | Measure along defined levels | Score |
| 4 | **Routing** | Select what happens next | Choice (+ confidence) |
| 5 | **Search** | Find matches by meaning | Choice (+ Noul guard) |
| 6 | **Retrieval** | Get the right evidence into the next step | Choice / Noul |
| 7 | **Ranking** | Put candidates in order | Choice / Noul |
| 8 | **Verification** | Check a specific claim or failure mode | Noul |
| 9 | **Feature extraction** | Turn language into inputs for another model | Any |
| 10 | **Structured data extraction** | Identify the correct values in raw data | Noul / Choice |

### 1. Classification
Gives something a category. An upload failure message gets labeled a bug; a shared company inbox gets messages labeled invoices, sales pitches, or delivery updates. **Choice works well because the categories are known and one can be selected.**

### 2. Detection
Asks whether a particular property is present. A sales reply might ask you to stop contacting the sender. **Noul fits** because it gives the yes/no probability, and your application decides what to do with it.

### 3. Scoring
Both a shape and a type. How destructive is this bug? How clear is this help article? **Define the levels so the number has useful meaning**, then use it to prioritize work — engineering or editorial.

### 4. Routing
Uses a decision to select what actually happens next. An order status question goes to a database lookup; a product question goes to an assistant with the relevant documentation. Confidence is what makes routing safe (see Pattern 2).

### 5. Search
Find matches **by meaning**. The docs' worked recipe scores every line of a document against a query with a Choice question, and uses a Noul to check whether the document contains an answer at all.

> That's not to say you can use a decision model *as* a search engine — but you can build it *into* a search engine using the design patterns.

### 6. Retrieval
Getting the right evidence into the next step in a process. A support assistant selects the returns-policy passages that apply to a particular customer's region and purchase. **This is a filtering process that improves downstream accuracy.**

### 7. Ranking
Putting candidates in a particular order. Ten backpacks, and the request is "I want a backpack for my laptop on a rainy bike commute." Jev evaluates the descriptions against those requirements and sorts the candidates.

**The relationship between 5, 6, and 7:** search finds the candidates, **ranking orders them**, and **retrieval uses the results to supply what the next step needs.**

### 8. Verification
Checking a specific claim or specific failure mode.

> **A quote can exist and still be used to make the wrong claim.**

Does a cited passage support the sentence that refers to it? Does a drafted reply promise a refund the policy and the case details don't support? **You're giving the model something concrete to check against.**

### 9. Feature extraction
Turning language into inputs for another model. Extract buyer intent or product interest, then test whether those signals improve a demand forecast. **This is the bridge to classical ML** — see the composite-scoring docs, which recommend using probabilities as features in a downstream model.

### 10. Structured data extraction
LLMs are great at data extraction but slow and expensive. With a decision model you have two options:
- **Code finds candidates, Jev identifies which are correct** — cheaper and more controlled.
- **Load the raw data and let Jev work through it**, identifying the specific data you're looking for.

---

## Part IV — The Four Design Patterns

These describe how to organize decisions into a working system. **All four are named and defined by TypeSafe in its public documentation.**

| Pattern | What it does | Benefits |
|---|---|---|
| **Speculative Fan-Out** | Send many questions in a single call, including speculative ones, and let your code decide what's relevant | Cost, Speed |
| **Confidence-Gated Routing** | Use confidence as a second decision axis to build safer systems | Reliability, Safety |
| **Composite Scoring** | Combine several dimensions of analysis into a single score | Cost, Reliability, Speed |
| **Intent Routing** | Classify a user's intent and route to the appropriate handler | Cost, Speed |

---

### Pattern 1 — Speculative Fan-Out

**The core claim:** because questions are evaluated in parallel, **the time it takes to ask one question versus ten in a single request is virtually the same.** So you should ask the questions you *might* need, to avoid a series of round trips.

**Worked example: support ticket triage**

You need the category. *If* it's a bug report, you also need severity. Instead of asking for category first and severity in a follow-up call — ask for both at once. If the ticket turns out not to be a bug, **your code simply ignores the severity answer.**

**One request, five questions, five answers:**

| Question ID | Type | Purpose |
|---|---|---|
| `category` | Choice | bug_report / billing / feature_request / account |
| `bug_severity` | Score | **Speculative** — only matters if bug |
| `has_reproducible_steps` | Noul | **Speculative** — only matters if bug |
| `refund_requested` | Noul | **Speculative** — only matters if billing |
| `frustration` | Score | **Useful regardless of category** |

**The routing code, verbatim from the docs:**

```python
category = response.answers["category"]
bug_severity = response.answers["bug_severity"]
bug_repro = response.answers["has_reproducible_steps"]
refund = response.answers["refund_requested"]
frustration = response.answers["frustration"]

if category.choice == "bug_report":
    if bug_severity.score > 1.5 and bug_repro.noul > 0.6:
        escalate_to_engineering(ticket_id, severity="high")
    else:
        add_to_bug_backlog(ticket_id)

elif category.choice == "billing":
    if refund.noul > 0.7:
        route_to_billing_with_flag(ticket_id, refund_likely=True)
    else:
        route_to_billing(ticket_id)

elif category.choice == "feature_request":
    log_feature_request(ticket_id)

# Frustration is useful regardless of category
if frustration.score > 1.5:
    flag_for_priority_response(ticket_id)
```

**Why this works — the measured proof.** The `parallel_questions` cookbook asked 13 questions (8 Noul, 2 Choice, 3 Score) against a ~54,000-character document, both as one batched call and as 13 separate calls, 5 repetitions each:

```
batching                 calls        cost  total time
one call, all 13             1   $0.000497       0.27s
13 calls, one each          13   $0.006090       2.71s

batching: 12.2x cheaper, 10.0x faster
```

**And the answers did not change.** Per-question means agreed to within noise, and the run-to-run standard deviation was *the same size under both strategies* — choices and scores and six of the eight Nouls returned **std dev exactly 0.0** either way. Whatever noise a question has, it has under both. **Batching neither shifts the answer nor adds variance.**

The mechanism: **the document dominates every request.** N single-question calls pay for it N times, in N round trips; the batched call pays once. **The bigger the document, the nearer that saving comes to a full Nx.**

> **Important caveat on the speed figure:** the 10.0× sums the 13 single-call latencies, assuming they run one after another. Fire them concurrently and the gap shrinks — **but the 13× token cost stays.**

**When you genuinely need two requests instead of one.** Questions in the same request are independent — one answer is *not* hidden context for another. A second request is warranted only when *code cannot build the second request until it has the first answer*: it needs the answer to fetch more data for the state, to decide what the state is made of, or to pick the next question's options. The docs' three legitimate cases:

- **Skill suggestion** — rank 182 skills in one request, then fetch the full text of the top three and judge them again against that better evidence.
- **Structure recovery** — ask whether each line break split a sentence, merge lines into blocks from those answers, *then* classify blocks that did not exist until the first request answered.
- **Hierarchical classification** — use each Choice answer to decide which options the next request offers.

---

### Pattern 2 — Confidence-Gated Routing

**The idea:** sometimes the best available answer is still too uncertain to act upon. Confidence becomes a **second decision axis**.

**Worked example: voice banking commands**

If someone says *"Cancel it"* — are they talking about their subscription or an appointment? A clear interpretation goes to the appropriate handler; an ambiguous one triggers clarification.

**The two-tier gating logic:**

```python
action = response.answers["intent"]

# Below 0.6 confidence on any action, route to a human
if action.confidence < 0.6:
    route_to_support_agent(account_id)

elif action.choice == "check_balance":
    # Low stakes. 0.6 confidence is sufficient.
    show_balance(account_id)

elif action.choice == "approve_transfer":
    if action.confidence > 0.85:
        # High stakes, but high confidence. Safe to act automatically.
        approve_transfer(account_id)
    else:
        # High stakes, moderate confidence. Verify intent first.
        ask_user_to_confirm(
            "Just to confirm: you would like to approve this transfer, is that correct?"
        )

else:
    route_to_support_agent(account_id)
```

**Read the structure carefully — it is two thresholds, not one.**

| Gate | Threshold | Rationale |
|---|---|---|
| **Floor** (any action) | **0.6** | Catches anything the model is genuinely uncertain about |
| `check_balance` | **0.6** is enough | Worst case: user hears the wrong balance read-out. Recoverable. |
| `approve_transfer` | **>0.85** | Otherwise **ask the user to confirm** |

> Above that floor, **each action type has its own threshold based on the consequences of acting on a wrong classification.**

**The three-range pattern, from the Confidence docs:**

| Range | Behavior |
|---|---|
| **High confidence** | Act automatically. The model has a clear read. |
| **Medium confidence** | Proceed with caution. Whatever fits the context — ask the user to confirm, flag for review, or gather more information. |
| **Low confidence** | **Do not act.** Route to a human, request clarification, or fall back to a different system. |

**Two absolute rules stated plainly in the docs:**

1. **A confidence threshold is not one number.** Different actions within the same system should be gated at different levels depending on the consequences of getting it wrong.
2. **You still need permission checks and confirmation rules in your software.**

> **Don't just trust what the decision model tells you. You still need to properly secure and gauge everything on your own side using your own business logic.**

**Calibration is measured across groups of predictions — it does not guarantee that an individual answer is correct.** That's why thresholds are yours to test: *start conservative, test with your own data, and adjust as you observe results.*

---

### Pattern 3 — Composite Scoring

**The idea:** break the judgment into **independent dimensions**, score each separately, and combine them with **weights you control in code**.

**Worked example: resume screening**

Score each candidate on four dimensions, then rank for two different roles with different weights.

**The four Score questions (one request):**

| Dimension | Levels (0 → 4) |
|---|---|
| `python_depth` | No mention → Mentioned, no detail → Used in projects → Primary language → Deep expertise |
| `team_leadership` | None → Informal mentorship → Led small team → Direct reports → Multiple teams/org |
| `system_design` | No architecture work → Design discussions → Components → Owned significant system → Systems at scale |
| `generalist` | One domain → Narrow variety → A few areas → Regularly moved → Ramped in unfamiliar areas |

**The combination — the whole point of the pattern:**

```python
py      = response.answers["python_depth"].score / 4
lead    = response.answers["team_leadership"].score / 4
arch    = response.answers["system_design"].score / 4
general = response.answers["generalist"].score / 4

# Senior IC
ic_score = (0.40 * py) + (0.10 * lead) + (0.40 * arch) + (0.10 * general)

# Engineering Manager
em_score = (0.15 * py) + (0.40 * lead) + (0.20 * arch) + (0.25 * general)
```

**Same four answers. Two completely different rankings.** Engineering Manager flips Python from 40% to 15% and leadership from 10% to 40%.

**Why this is the highest-leverage pattern:**

> This gives you the ability to rank candidates. But more importantly, it gives you **visibility into how exactly the final score is being calculated.** If the highest ranking candidates are not matching your expectations, you can adjust the weights to find the right balance.

**The normalization rule.** Scales of different lengths return different maxima — a four-level scale returns 0–3, a three-level scale returns 0–2. **Divide each score by its top level number, `len(criteria) - 1`, to put every score on 0–1.** Only then do the weights mean what they say: 0.6 on severity counts twice as much as 0.3 on frustration.

The docs' ticket-priority worked example:

```python
def normalized(answers, question_id: str) -> float:
    """Put a score on 0 to 1 by dividing by its top level number."""
    top_level = len(TRIAGE_QUESTIONS[question_id].criteria) - 1
    return answers[question_id].score / top_level

# ...
return 0.6 * severity + 0.3 * frustration + 0.1 * report_quality
```

> 0.62 severity, 0.64 frustration, 1.0 report quality →
> `0.6 × 0.62 + 0.3 × 0.64 + 0.1 × 1.0 = 0.664`

**Why weights belong in code, not in a prompt:** *When priorities shift, change a coefficient in your code rather than rewriting a prompt.*

**Extension — dynamic weights:** the presentation notes you could send the situation into the model and have it determine the weights. This is not in the core docs and should be treated as an advanced variant.

**Extension — composite scoring over Nouls.** The same combination works on Noul probabilities:

```python
quality = (
    0.4 * answers["answers_request"].noul
    + 0.4 * answers["citations_are_supported"].noul
    + 0.2 * (1 - answers["contradicts_context"].noul)
)
```

**And the bridge to classical ML:** *For learned composition, use the probabilities as features in a downstream machine-learning model.* If you lack labels, the docs suggest using an ensemble of expensive reasoning models to generate them.

---

### Pattern 4 — Intent Routing

**The idea:** not every request needs the same kind of handler. Some can be answered with a database lookup. Some need an LLM with domain context. Some need a human. **A decision model sits in front of all of them as a fast, cheap classifier.**

**Worked example: customer service routing**

**Two questions in one request:**

- `intent` (Choice): `order_status`, `product_question`, `return_exchange`, `complaint`
- `complexity` (Score): Simple lookup → Requires judgment/multi-step → Unusual edge case/escalation

**The routing logic:**

```python
def route_ticket(ticket_id, response):
    intent = response.answers["intent"]
    complexity = response.answers["complexity"]

    if intent.confidence < 0.5:
        # If we don't have enough confidence to classify, route to a human agent
        return route_to_human_agent(ticket_id)

    if intent.choice == "order_status":
        handle_order_status(ticket_id)          # deterministic code, no LLM

    elif intent.choice == "product_question":
        handle_with_llm(ticket_id, PRODUCT_SPECIALIST)

    elif intent.choice == "return_exchange":
        handle_with_llm(ticket_id, RETURNS_SPECIALIST)

    elif intent.choice == "complaint":
        low_confidence = complexity.confidence < 0.5
        # A higher complexity.score leans toward the "escalation needed" end of the scale.
        if complexity.score > 1 or low_confidence:
            # Too complex for safe automation, or we're not sure about the complexity;
            # route to a human.
            route_to_human_agent(ticket_id)
        else:
            handle_with_llm(ticket_id, COMPLAINT_RESOLUTION)
```

**Four intents, four different handler types:**

| Intent | Handler | Cost |
|---|---|---|
| `order_status` | **Deterministic code** | Zero model cost |
| `product_question` | LLM + product docs | Expensive |
| `return_exchange` | LLM + returns docs | Expensive |
| `complaint` | LLM, **or human if complex/uncertain** | Expensive, gated |

**Two things to notice:**

1. **Faithful to the presentation:** *one intent routes to deterministic code with no LLM involved. Two route to different specialist LLMs, each loaded with different context. One uses the complexity score to decide between an LLM and a human.*
2. **The union of Patterns 1 and 2.** Intent routing is speculative fan-out (both questions in one call) *plus* confidence-gated routing (both axes gated). The docs make the second explicit: *Note the additional confidence check on the complexity score.*

> TypeSafe handles the classification all in a single quick call; **the expensive resources only get invoked for the requests that actually need them.**

---

## Part V — Putting It All Together

The presentation closes with a full customer-support application.

### The flow

1. **A ticket arrives** — an upload failure.
2. **Send it to the decision model** with **several questions together**: the category, a disruption/priority score, and a deadline signal.
3. **Check whether the answers are clear enough to use** — confidence gates.
4. **Code selects the appropriate handler and sets the priority.**
5. **Only then is an LLM bundled in** — if the customer needs a written response, it goes to a generative model, *which handles that step using the relevant evidence provided.*

### The design principle stated

> **Each decision has a defined job and the application controls how the pieces fit together.**

The decision model is not the application. It is a service the application calls for common-sense judgments, and the application retains control flow, deterministic rules, and side effects.

### The three-question starting framework

When you're thinking about using a decision model:

1. **Pick a workflow you already understand.**
2. **Find a point where the software needs to interpret fuzzy natural language.**
3. **Figure out the smallest useful question.** Does the answer need to be a probability, a choice, or a score? What should happen when the answer is uncertain?

### The seven-step workflow from the docs

The official guide is more prescriptive, and worth having in full:

| Step | Instruction |
|---|---|
| **1** | **Use code when you can.** Deterministic work is reliable and cheap. Avoid agent `while` loops when a software workflow expresses the same behavior. |
| **2** | **Decompose the input state.** Include *only* the context relevant to the current questions. This helps the model avoid distractions and context rot. Don't rely on model weights when current information can come from your own knowledge base. |
| **3** | **Use structure in the input state.** Point questions at specific values with backticked dot-and-index paths — `` `support.tickets[0].message` `` — when that removes ambiguity. |
| **4** | **Decompose the questions.** Ask the most explicit, narrow, specific, atomic questions you can. *"This is probably the most important concept in this guide."* |
| **5** | **Use structure in the questions** when the question needs context/examples, part of it comes from your code, or several questions share similar wording. |
| **6** | **Ask a lot of questions.** Many narrow, independent questions in one request. |
| **7** | **Combine outputs in code** — or feed the probabilities into a classical ML model. |

### Step 4, illustrated: the spam-detection decomposition

The docs make the argument by contrasting one bad question with six good ones.

**Bad — one broad question hides several judgments:**

```json
{ "is_spam": { "type": "noul", "instructions": "Is `message` spam?" } }
```

**Good — six atomic judgments, combined in code:**

```json
{
  "requests_credentials":   { "type": "noul", "instructions": "Does `message.body` ask the recipient to provide a password or other login credential?" },
  "offers_unexpected_reward": { "type": "noul", "instructions": "Does `message.body` claim the recipient received an unexpected prize, payment, or reward?" },
  "creates_time_pressure":  { "type": "noul", "instructions": "Does `message.subject` or `message.body` pressure the recipient to act quickly?" },
  "sender_identity_mismatch": { "type": "noul", "instructions": "Does the organization named in `message.sender.display_name` conflict with the domain in `message.sender.email`?" },
  "link_domain_mismatch":   { "type": "noul", "instructions": "Does the domain in `message.links[0].url` conflict with the organization named in `message.sender.display_name`?" },
  "disguises_link_destination": { "type": "noul", "instructions": "Does `message.links[0].text` conceal or misrepresent the destination in `message.links[0].url`?" }
}
```

> **Why this is better:** broad questions hide several judgments behind one answer. **Atomic questions expose those judgments** so you can inspect, tune, and combine them in code.

The same decomposition is shown for verifying a tool-call trace — one broad *"Is `trace.tool_calls` correct?"* versus nine atomic checks on tool relevance, argument schema conformance, ID matching, and coordinate propagation.

### What makes System One composable

| Property | Meaning |
|---|---|
| **Structured** | Type-safe by construction. Decisions conform to the JSON schema your code expects, so it never has to recover a value from generated prose. |
| **Parallel** | Questions are evaluated independently and in parallel. One primitive's result is not hidden context that changes another's. |
| **Comparable** | Outputs are sortable and can drive smart `if` statements, thresholds, comparisons. |
| **Fast** | Most queries complete in about 100 ms — fast enough for real-time request paths and UIs. |
| **Calibrated confidence** | Communicates uncertainty through calibrated probabilities instead of tending toward overconfidence. |
| **Self-consistent** | Designed to return stable answers across repeated evaluations. |

---

## Part VI — Three Worked Micro-Patterns from the Docs

### A. Structured criteria for confusable options

When two options are similar and the model keeps confusing them, give each option an **object** instead of a string — with fields for what it covers, what belongs to a neighbor, and examples. The field names are **yours**; none are reserved.

```json
{
  "return_policy": {
    "what": "Whether and how an item can be returned",
    "not_for": "Progress of a return already sent",
    "examples": ["Can I return shoes I've worn once?", "How long do I have to return an order?"]
  },
  "return_status": {
    "what": "Progress of a return already sent",
    "not_for": "Whether and how an item can be returned",
    "examples": ["Has my return arrived yet?", "When will my refund be paid?"]
  }
}
```

### B. Examples on Score levels — and the trap

Adding an `examples` array to a level can concentrate probability dramatically:

| Level description | `score` | `confidence` |
|---|---|---|
| Plain strings | 1.43 | **0.35** |
| + relevant example ("export fails in one browser but works in another") | 1.03 | **0.96** |
| + **unrelated** example ("search fails, but browsing categories still works") | 1.43 | **0.35** |

> **Examples steer the model, and they only help when they look like your real inputs.** The unrelated example returned *exactly the same result* as plain strings.

**And the warning that follows: higher confidence does not establish which answer is correct.** Choose examples with known expected levels, then test on separate inputs before keeping them.

### C. Two questions in one request — the line-by-line search

A genuinely elegant recipe, worth preserving in full because it demonstrates **code compensating for a structural property of the primitives.**

**The problem:** you want the lines of a document that answer a query, *and* a way to detect when the document has no answer.

**The trick:** `Choice` probabilities always sum to 1, so **some line ranks first even when the document doesn't answer the question.** The ranking alone cannot distinguish a real answer from the closest irrelevant line.

**The fix:** tag every line with an ID (`L000`, `L001`, …), ask a `Choice` to rank the line IDs, **and in the same request** ask a `Noul` whether the document contains an answer at all.

```python
def where_question(query: str) -> Choice:
    return Choice(
        instructions=f'Which line of the document contains the answer to: "{query}"?',
        criteria={line_id(i): None for i in range(len(LINES))},
    )

def exists_question(query: str) -> Noul:
    return Noul(
        instructions=f'Does any line of the document address or answer: "{query}"?',
        criteria=NoulCriteria(
            true="At least one line of the document states or directly implies the answer",
            false="No line of the document addresses this",
        ),
    )
```

**Actual measured results** against GitHub's Terms of Service (218 clauses, 43,980 characters):

**"who owns the code I upload?"**
```
exists 0.98 -> answered in this document
L052  0.95  ###########   You own Your Content. If you post Content you did not crea
L046  0.02  #             Short version: You own content you create, but you allow u
```

**"do I have to take disputes to arbitration?"**
```
exists 0.14 -> not in this document
L205  0.86  ##########    Except to the extent applicable law provides otherwise, th
```

**"can minors use GitHub with parental permission?"**
```
exists 0.46 -> partially addressed
L029  0.90  ###########   You must be age 13 or older. While we are thrilled to see
```

> **The ranking tells you where to look; the `exists` score tells you whether the result answers the question.**

Note the arbitration case: the ranking gives the closest line **0.86** — a high number that looks like a hit — while `exists` is only **0.14**. **Without the Noul guard, you would confidently return an irrelevant line.**

**Structural limits to know:**
- A Choice accepts **up to 255 options** → this recipe searches documents of up to 255 lines in one request.
- Past that, **search in two passes**: one Choice picks a window of lines, a second ranks inside it.

---

## Part VII — Cross-Reference: The Two Volumes

### Vocabulary mapping

| Launch Week Dossier term | This Handbook's canonical term | Relationship |
|---|---|---|
| Batch Multi-Question Single-Pass | **Speculative Fan-Out** | Same pattern; the vendor name is canonical |
| Parallel Fan-Out, Single Verdict | **Composite Scoring** | Related but distinct — fan-out gathers, composite *weights and combines* |
| State Menu ≠ Screenshot | *(no vendor equivalent)* | Authored from agent-build mechanics |
| Two-Tier Policy / Payload Split | *(no vendor equivalent)* | Authored |
| Streaming Per-Unit Evaluation | *(no vendor equivalent)* | Authored |
| Daemon-Scale Repetition | *(no vendor equivalent)* | Authored |
| Compose From Trusted Components | *(no vendor equivalent)* | Authored |
| Structural Compaction | *(no vendor equivalent)* | Authored |
| Simulation as Stress Bench | *(no vendor equivalent)* | Authored |
| Open-Source Local Reimplementation | *(no vendor equivalent)* | Authored |
| Calibrated Decisions | **Calibrated confidence** | Same concept; vendor frames it as a composability property |
| Menu-as-Safety-Boundary | **"type-safe by construction"** | Same concept, vendor phrasing |
| Fixed-Cadence Polling + Scalar | **Intent Routing + Confidence Gating** | Related; the vendor pattern is the general form |
| *(not in dossier)* | **Confidence-Gated Routing** | **New here** |
| *(not in dossier)* | **Intent Routing** | **New here** |

### What each volume contributes

**The Launch Week Dossier answers:** *what did people actually build, and did the vendor's claims hold up?*

**This Handbook answers:** *how does the vendor say you should build, and what vocabulary do the docs use?*

The dossier's Family C — the five measurement patterns (*Format ≠ Judgment*, *Company Grades Own Homework*, *Dramatized Mock-Up as Evidence*) — remains the necessary counterweight. This volume is a fair and complete account of **the documented design vocabulary**. It is not evidence that the benchmarks are what the marketing says. Those are separate questions, and the dossier addresses them.

### The unified picture

**30 distinct patterns across two volumes:**

| Source | Count | Nature |
|---|---|---|
| Vendor-documented design patterns | **4** | Speculative Fan-Out, Confidence-Gated Routing, Composite Scoring, Intent Routing |
| Vendor-documented primitives & shapes | **13** | 3 types + 10 shapes |
| Authored, reverse-engineered from builds | **16** | Dossier Family A (6) + Family B (10) |
| Authored, diagnostic | **5** | Dossier Family C |
| **Distinct patterns (deduplicated)** | **30** | Overlaps mapped above |

---

## Part VIII — Reference Tables

### A. Decision type selection

| If the answer is... | Use | Returns |
|---|---|---|
| One of a fixed set, unordered | **Choice** | `choice`, `probabilities`, `confidence` |
| A position on a describable spectrum | **Score** | `score`, `legend`, `probabilities`, `confidence` |
| Yes or no, and the probability is the signal | **Noul** | `noul` (no separate confidence) |

**Tiebreaker from the docs:** *If two types both seem to fit, prefer the one whose answer your code can act on directly.* A Choice between `refund`/`rebook`/`information` maps to three code paths. A Score maps to a threshold. A Noul maps to an `if`.

### B. Threshold placement

| Situation | Threshold guidance |
|---|---|
| Yes and no equally easy to act on | 0.5 |
| Acting on a false yes is **expensive** (paging, refunds) | **Raise it** |
| Missing a true yes is **expensive** (safety failures) | **Lower it** |
| Genuinely ambiguous cases | **Route to a person** — neither code path |

### C. Quantitative claims register

| Claim | Value | Source |
|---|---|---|
| List price | $0.042 / 1M input tokens | TypeSafe docs |
| Output tokens | **$0.00** | TypeSafe docs |
| 1M × 1,000-token requests | **~$42** | Presentation arithmetic |
| Typical latency | **~100 ms** | "Most queries" — docs |
| Real-time latency cited | **~150 ms** | Presentation |
| Choice options max | **255** | Docs |
| Score levels max | **10** | Docs |
| Batching saving | **12.2× cheaper, 10.0× faster** | Cookbook, measured |
| Batching answer change | **None** (std dev 0.0 on 11 of 13) | Cookbook, measured |
| Target intelligence-to-speed-and-cost ratio | **>100×** | Docs |

### D. Resource index

| Resource | URL |
|---|---|
| Introduction | https://docs.typesafe.ai/introduction |
| Patterns | https://docs.typesafe.ai/patterns |
| Primitives (Questions) | https://docs.typesafe.ai/primitives |
| Confidence | https://docs.typesafe.ai/confidence |
| System One concept | https://docs.typesafe.ai/concepts/system-one |
| How to build with TypeSafe | https://docs.typesafe.ai/concepts/how-to-build-with-system-one |
| Line-by-line search cookbook | https://docs.typesafe.ai/cookbooks/semantic_find |
| Parallel questions cookbook | https://docs.typesafe.ai/cookbooks/parallel_questions |
| Speculative fan-out | https://docs.typesafe.ai/patterns/fan-out |
| Confidence-gated routing | https://docs.typesafe.ai/patterns/confidence-routing |
| Composite scoring | https://docs.typesafe.ai/patterns/composite-scoring |
| Intent routing | https://docs.typesafe.ai/patterns/intent-routing |

---

## Closing Assessment

### The shape of the whole thing

Every pattern in this volume is a way of answering one question:

> **Where does the decision model sit in my software, and what does my code do with what it returns?**

The answers form a consistent philosophy. **Code owns the workflow.** The model supplies narrow, typed, calibrated judgments. Confidence is a first-class value that determines which code path runs. Weights live in code so they can be tuned without rewriting prompts. And because questions run in parallel within one request, asking more of them is close to free.

### The two guiding disciplines

**Decompose.** One broad question hides several judgments. Ask atomically, combine explicitly. You gain visibility into how a result was produced — which is the real payoff of composite scoring, not the ranking itself.

**Gate on uncertainty.** A model that cannot express honest uncertainty cannot be trusted. Thresholds are yours, they scale with the stakes of each action, and the middle range — where the model is genuinely unsure — belongs to a human.

### The one number to carry forward

Batching 13 questions into one request is **12.2× cheaper and 10.0× faster** than 13 separate calls, **with no change to the answers.** Every pattern that says "ask many questions together" rests on that measurement. It is the single most actionable finding in either volume.

### And the discipline that must not be dropped

This volume documents **the design vocabulary**. It is a fair account of what TypeSafe says, and its pattern set is genuinely well-constructed.

It is not, and cannot be, independent evidence that the vendor's *performance* claims hold. The Launch Week Dossier addresses that separately, and its Family C patterns still apply: **format-validity is not judgment-correctness, and a designed pattern is not the same as a validated benchmark.**

> **Read this volume to learn how to build. Read the dossier to know what to believe.**

---

## See also

**[The Jev Launch Week Dossier](jev-launch-week-dossier.md)** — Volume I. What developers actually built in the six days after launch, and an honest audit of which vendor claims held up.

**[The Jev Benchmark Report](jev-benchmark-report.md)** — Volume III. Independent measurement of Jev against 12 local decision models. It tests this volume's patterns in production conditions and reports where they hold:

- **Speculative Fan-Out** is confirmed — batching 13 questions is 12.2× cheaper and 10.0× faster with identical answers
- **Confidence-Gated Routing** is validated by the *option-order fragility* finding: one model swung from 21% to 72% on reversed options, so thresholds must be validated per model, not adopted across models
- **Composite Scoring's** decomposition principle is what makes the benchmark interpretable at all — the aggregate rank hides per-task inversions
- **Intent Routing's** "act vs. speak" distinction is exactly what separates Jev from Winnow in the support-workflow test

> **Read this volume to learn how to build. Read Volume III to choose.**

---

*Compiled from The AI Automators' presentation "Master ALL Jev Design Patterns (With Practical Examples)" (https://youtu.be/LzweTaOzvvo) and the primary TypeSafe documentation at docs.typesafe.ai. All pattern names, definitions, code examples, and measured figures are as published by TypeSafe; presentation-sourced figures (the ~150ms latency, the $42 arithmetic) are noted as such. Quote, figure, and caveat provenance is marked throughout.*
