# The Jev Benchmark Report
## Independent Evaluation: Jev vs 12 Local Decision Models

**Compiled:** September 28, 2026
**Source presentation:** The AI Automators — *I Tested Jev vs 12 Local Decision Models* (12:18, published Sep 28, 2026)
**Source URL:** https://youtu.be/zBw5BMrlZLo
**Harness:** [jev-arena](https://github.com/theaiautomators/jev-arena) (MIT, independent, unaffiliated with TypeSafe)
**Run:** `20260927-205440-6350b9`, 27–28 September 2026 · Windows RTX 5090 (32 GB) · serial calls

**Companion volumes:** [The Jev Launch Week Dossier](jev-launch-week-dossier.md) · [The Jev Design Pattern Handbook](jev-design-patterns-handbook.md)

---

## Preface — The Third Layer

Three volumes now sit on three different axes.

| | Volume I | Volume II | **Volume III** |
|---|---|---|---|
| **Question** | What did they build? | How should you build? | **What actually performs best?** |
| **Authority** | Third-party observation | Vendor documentation | **Independent measurement** |
| **Evidence type** | Demos and claims | Specs and patterns | **Frozen protocols, recorded runs** |
| **Tone** | Auditing | Teaching | **Measuring** |

**This volume is the most evidentially careful of the three, and it changes what we can say confidently.**

Volume I documented TypeSafe's own accuracy numbers and flagged them as unverified: a ~68% agreement-with-a-panel figure, the company grading its own homework, a speed claim that varied by page. **Volume III is the independent test Volume I said was missing.** It reaches the same broad verdict — the mechanism is sound, the marketing overreached on specifics — but the numbers are now measured rather than asserted.

And it delivers a finding neither prior volume anticipated: **several small models you can run on your own hardware are within a fraction of a percent of Jev on the same questions, and are 4–5× faster.**

### What "independent" means here, precisely

The harness publishes its own limitations more aggressively than its results. That is the reason to trust it. Highlights of what it discloses:

- **The suite is a restricted intersection, not the whole workload.** The shared cohort excludes 1,000 cases two models couldn't accept, plus 36 more. 4,635 of 7,671 planned cases.
- **"Not public" is not "not seen."** Held-out items were sent to the services being evaluated to get predictions. *"This is not a contamination proof."*
- **The latency adjustment is an assumption, not a measurement.** Self-hosted runs got a ×2 / +0.15 s penalty to approximate production load.
- **8,192-token limits were often chosen serving configurations, not architectural ceilings.**
- **`publication_ready=false`** — "the unmet human-audit gate; do not claim paper-level acceptance."
- **13 entrants are not 13 architectures.** Three are Laya variants; there are diagnostic controls.
- Every invalid output is preserved, never repaired into a valid distribution. *"An unknown price is `null`, not `0`."*

> **The harness's own framing, worth adopting:** *"Jev led this suite; several local profiles were close on shared label selection and much faster per serial request. There is no universal winner."*

---

## Part I — The Arena

### What was tested

**13 pinned deployment profiles**, each run through **7,671 static records** — 99,723 unique records total. Plus 39 serial timing blocks, 1,040 workflow episodes, 33 local load/cleanup cycles, and 1,600 targeted follow-up predictions.

| Profile | Tested approach | Base / scale |
|---|---|---|
| **Jev 1.13** | Hosted decision service | **Undisclosed** |
| **Winnow** | Decision fine-tune, Q8_0 | Gemma 4 12B |
| **Decider v2** | Decision fine-tune, BF16 | Qwen3.5-4B-Base |
| **Plumb** | Decision fine-tune, BF16 | JevK5 on Qwen3.5-4B |
| **Nimble** | Decision adapter/backbone, BF16 | Qwen3.5-9B |
| **CLM** | Learned contrastive heads | Frozen Qwen3-8B backbone |
| **SemIf** | Direct option scoring, no new fine-tune | Qwen3.5-4B |
| **Laya English** | Decision encoder | ModernBERT-large + head, **421M** |
| **Laya typed** | Related task-specific checkpoint | ModernBERT-large + head, 421M |
| **Laya multilingual** | Related multilingual checkpoint | mmBERT + head, **322M** |
| **Qwen JSON** | Generative classification control | Qwen3.5-4B |
| **ModernBERT NLI** | Entailment classification control | 395M |
| **Uniform baseline** | Deterministic first-option selection | **No model** |

### The three question types

Same structure as Volume II's primitives — the benchmark tests the paradigm, not just one vendor.

- **Noul (yes/no)** — "is this requested action permitted?" returns a probability
- **Choice** — extraction: "extract the final confirmed delivery method," with options and probabilities
- **Score** — "how likely is the customer to stop doing business?" with defined levels up to imminent cancellation

### The data

**7,671 cases per entrant**, drawn from JevBench (public repo), classification, multilingual document relevance, and a chat-conversation set with full agent/customer back-and-forth.

**5,671 primary reference cases + 2,000 teacher-agreement cases** before capability exclusions.

### Two metrics, deliberately kept apart

This is the most important methodological decision in the whole report, and it directly vindicates Volume I's *Format ≠ Judgment* pattern.

| Metric | Definition |
|---|---|
| **Strict correctness** | Correct label **AND** valid output under Arena's frozen contract |
| **Selected-label agreement** | Correct selected label, **ignoring** probability-format failures |

> **Why both matter:** *"Output quality and decision quality therefore need separate explanations."* A model can pick the right answer and still emit a probability vector that software cannot consume.

---

## Part II — Headline Accuracy

### The shared cohort: 4,635 identical references

Every entrant answered the same questions. This is the fairest comparison in the report.

| Profile | Strict correct | Label matches | **Label agreement** |
|---|---:|---:|---:|
| **Jev 1.13** | 4,412 | 4,414 | **95.23%** |
| **Winnow 12B** | 4,385 | 4,385 | **94.61%** |
| **Decider 4B · v2** | 4,373 | 4,378 | **94.46%** |
| **Nimble 9B** | 4,280 | 4,280 | **92.34%** |
| Plumb 4B | 4,150 | 4,150 | 89.54% |
| Qwen 3.5 · JSON | 3,976 | 3,976 | 85.78% |
| SemIf 4B | 3,787 | 3,787 | 81.70% |
| Laya | 3,000 | 3,005 | 64.83% |
| Laya · typed | 2,960 | 2,962 | 63.91% |
| ModernBERT · NLI | 2,722 | 2,722 | 58.73% |
| Laya · multilingual | 2,604 | 2,610 | 56.31% |
| Uniform baseline | 2,075 | 2,075 | 44.77% |
| CLM 8B | 1,673 | 1,673 | 36.09% |

**Jev wins the aggregate.** But look at the margin:

> Jev's selected-label advantage is **29 answers over Winnow** and 36 over Decider — out of 4,635.

### The confidence intervals — read these before quoting anything

The harness publishes descriptive paired cluster-bootstrap intervals for **competitor minus Jev**:

| Comparison | Interval | Reading |
|---|---|---|
| **Winnow − Jev** | **−0.63 pp [−1.25, −0.07]** | Does not cross zero — a real, if small, gap |
| **Decider − Jev** | **−0.78 pp [−2.17, +0.38]** | **Crosses zero** — proves neither equivalence **nor** superiority |
| **Nimble − Jev** | **−2.89 pp [−5.59, −1.03]** | Does not cross zero |

> *"The Decider interval crossing zero proves neither equivalence nor superiority. These are unadjusted exploratory comparisons on a fixed suite, not population guarantees."*

**The honest summary: Jev leads, and the lead over the two strongest local models is small enough that one of the two intervals includes zero.**

### Full coverage — and the denominator trap

The next table uses each profile's *recorded* denominator. The harness explicitly warns it is **inappropriate to rank these rows as equal-coverage accuracy.**

| Profile | Recorded n | Strict | Label | Valid outputs / 7,671 | Unsupported |
|---|---:|---:|---:|---:|---:|
| **Jev 1.13** | 5,671 | 5,217 (91.99%) | 5,263 (92.81%) | **7,587** | 0 |
| Winnow 12B | 5,671 | 4,813 (84.87%) | 4,813 (84.87%) | 7,171 | 0 |
| Decider 4B · v2 | 5,671 | 4,752 (83.79%) | **5,235 (92.31%)** | 7,090 | 0 |
| Nimble 9B | 5,671 | **5,121 (90.30%)** | 5,121 (90.30%) | **7,671** | 0 |
| Plumb 4B | 4,671 | 4,177 (89.42%) | 4,177 (89.42%) | 6,671 | **1,000** |
| Qwen 3.5 · JSON | 5,671 | 4,675 (82.44%) | 4,675 (82.44%) | 7,669 | 0 |
| SemIf 4B | 4,671 | 3,807 (81.50%) | 3,807 (81.50%) | 6,671 | **1,000** |
| Laya | 5,671 | 3,151 (55.56%) | 3,244 (57.20%) | 6,997 | 0 |
| Laya · typed | 5,671 | 3,056 (53.89%) | 3,234 (57.03%) | 7,111 | 0 |
| ModernBERT · NLI | 5,671 | 3,207 (56.55%) | 3,207 (56.55%) | 7,671 | 0 |
| Laya · multilingual | 5,671 | 2,806 (49.48%) | 2,927 (51.61%) | 7,023 | 0 |
| Uniform baseline | 5,671 | 2,096 (36.96%) | 2,096 (36.96%) | 7,671 | 0 |
| CLM 8B | 5,635 | 1,731 (30.72%) | 1,731 (30.72%) | 7,635 | 36 |

**Three things to notice:**

1. **Nimble has the highest local strict result on the full denominator** — 90.30%, with zero unsupported cases and all 7,671 valid.
2. **Decider's 483-answer strict/label gap** is not 483 reasoning errors. It is probability-sum failures under Arena's 1e-4 tolerance — *"Arena's chosen contract, not necessarily a reasoning error."*
3. **Jev has only 84 probability-sum failures across all 7,671.** Decider has 581; Laya 674.

### The post-hoc sensitivity that must be read with the primary result

Excluding the 500 BANKING77 cases (see Part III) leaves 5,171 references:

| | Strict | Labels |
|---|---:|---:|
| **Jev** | 4,818 | 4,852 |
| **Winnow** | **4,813** | **4,813** |

> **Only five strict answers apart.** The harness labels this a *"post-hoc capacity sensitivity"* that *"does not replace the frozen primary result or establish equivalence."*

**But it is the single most decision-relevant number in the report** for anyone considering self-hosting: on a workload both models can actually accept, a 12B model you run yourself lands within five answers of hosted Jev.

---

## Part III — Capacity: The Silent Disqualifier

The presentation's second lesson, and the one most likely to bite a builder who skips it.

> *"The number of choices sounds like a minor detail until it actually stops the whole request."*

| Profile / interface | Choice capacity | What happens on BANKING77 |
|---|---:|---|
| **Plumb 4B** | **16** | 500 unsupported cases |
| **SemIf** (on Qwen3.5-4B) | **16** in this interface | 500 unsupported cases |
| **Winnow 12B** native server | **64** | 500 HTTP 400 failures |
| **Jev** | up to **255** (per Volume II docs) | Handles all 77 options |

**BANKING77 supplies 77 options per question.** Plumb and SemIf have a native limit of 16 — they cannot weigh in at all. Those two 500-case groups, plus 36 further unsupported cases, account for the 1,036 questions outside the shared cohort.

### The Winnow incident — a harness bug, disclosed in full

This is the most instructive episode in the report, because the harness made an error and published the post-mortem.

> **Winnow's 500 BANKING77 HTTP 400s came from a missed native 64-option limit. Arena incorrectly advertised 255. These are failed requests caused by a capability mismatch, not 500 wrong decisions.**

The recorded manifest stays frozen and uncorrected. A corrected registry entry and a 64/65 boundary regression test were added. The shared comparison already excludes BANKING77 and is unaffected.

**Why this matters beyond one bug:** it is the exact failure mode Volume I's audit pattern *Dramatized Mock-Up vs Real Run* warns about, handled correctly. The error was found, the raw evidence preserved, the correction documented, the affected numbers excluded rather than patched, and the conclusion explicitly restricted. **A benchmark that hides a bug like this is worth less than one that documents it.**

### Input length is the other disqualifier

| Model | Input ceiling | Consequence |
|---|---|---|
| **Nimble 9B** (pinned release) | **8,192 tokens** | Could not accept the full ABCD policy handbook |
| **Jev** | 32K state/question; 64K total | — |
| Winnow | 64K | Longest tested input was 29,128 tokens |
| Qwen | configured 32K (incl. output) | Backbone supports more than tested |

> **Nimble's 1,200 full-handbook records and 108 longer synthetic variants were explicitly unavailable. "Unavailable capacity is not a wrong reasoning answer."**

**Bonus correction for Volume I readers:** the docs note many 8K figures were **serving choices, not architectural limits**. Qwen's native configuration is larger than its tested setting. Do not infer a model's ceiling from a benchmark's pinned profile.

---

## Part IV — Speed: The Reversal

### Short inputs — local wins decisively

Three serial timing blocks each, same first 200 frozen inputs, one request in flight, warmup excluded.

| Profile | Block p50 values (ms) | Valid / 600 |
|---|---|---:|
| **Jev 1.13** | 244.70, 243.63, 245.13 | 600 |
| **Winnow 12B** | 55.00, 55.97, 59.14 | 600 |
| **Decider 4B · v2** | **46.95, 47.45, 48.49** | 600 |
| Nimble 9B | 47.90, 49.68, 52.58 | 600 |
| Plumb 4B | 48.07, 49.59, 48.84 | 600 |
| Qwen 3.5 · JSON | 316.90, 318.95, 305.06 | 600 |
| SemIf 4B | 54.29, 50.96, 48.16 | 600 |
| Laya | **17.22, 16.60, 18.01** | 588 |
| Laya · typed | 18.10, 15.86, 17.06 | 597 |
| ModernBERT · NLI | 23.29, 20.45, 18.91 | 600 |
| Laya · multilingual | 15.19, 13.87, 13.45 | 594 |
| Uniform baseline | 0.00 | 600 |
| CLM 8B | 116.58, 117.22, 117.84 | 516 |

**Jev's 245 ms includes the network trip; local profiles do not.** Decider is ~5× faster. Laya is ~14× faster.

### Long inputs — the advantage reverses completely

Same models, a ~20,000-token policy handbook instead of a short state.

| Profile | Short-input median* | **Full handbook** | **Retrieved policy** |
|---|---:|---:|---:|
| **Jev** | 244.70 ms | **358 ms** | 265 ms |
| Winnow | 55.97 ms | **2,847 ms** | 320 ms |
| Decider | 47.45 ms | **1,895 ms** | **144 ms** |
| Nimble | 49.68 ms | Unsupported | 240 ms |
| Qwen JSON | 316.90 ms | 1,570 ms | 468 ms |

> **The reversal is the finding.** Local models are faster only when the input is short. Feed them a full handbook and Jev turns the request around in **0.36 s** while Decider takes **1.9 s** and Winnow **2.8 s**.

**The retrieval mitigation.** Instead of the full handbook, retrieve sections:

- **Decider: 1,895 ms → 144 ms** (13× faster)
- **Winnow: 2,847 ms → 320 ms** (8.9× faster)
- **Jev: 358 ms → 265 ms** (a modest gain)

> *"An alternative approach is to use a RAG style system: not use the full handbook but instead just retrieve sections of the handbook and drop that in for the decision."*

### The caveats the harness insists on

- These are **serial** calls — not maximum-throughput measurements.
- Jev is **hosted, with network included and an undisclosed backend**; local runs are one GPU. *"A hosted endpoint and a local CPU are not the same kind of latency and should not be read as one ranking."*
- Local profiles used the ×2 / +0.15 s adjustment, which is *"an assumption, not a measurement."*
- Jev's parameter count and hardware are **undisclosed**. Slower short requests do not prove it is larger.

---

## Part V — Where Task Fit Beats Aggregate Rank

The harness's repeated warning: *"Start with the actual decision, not the leaderboard."*

### Slices where the aggregate inverts

| Job | Observation | Implication |
|---|---|---|
| **News classification** | **Laya 92.2%**, Decider 90.0%, Jev 88.2% on the same 500 articles | A 421M encoder beats Jev on a narrow job |
| **Sentiment** | Jev 96.4%, Winnow 96.2%, ModernBERT NLI 95.8% on 500 reviews | A compact classifier is competitive |
| **Multilingual entailment** | **Decider 84.0%**; Jev and Nimble 81.4% on 500 translated examples | A model named "multilingual" isn't automatically best |
| **Public decision questions** | **Plumb 92.3%**, Jev 90.3% on the shared 195-question JevBench subset | Aggregate rank hides specialties |
| **Explicit policy rules** | Jev and Winnow **100%** on 1,440 generated rules; 100% on 1,000 changed-input cases | Strong controlled rule-following |
| **Support action selection** | **Jev 78.67%** vs Winnow 66.67% full-handbook | Jev much stronger at choosing *which* action |

### The tiny-model upset

The presentation's most striking finding:

> **Laya — a 421M-parameter encoder — comes out on top for news classification, beating Jev and models 30× its size.**

The task analysis quantifies the divergence:

| News paired outcomes | Count |
|---|---:|
| Both correct | 427 |
| **Laya only** | **34** |
| **Jev only** | **14** |
| Both wrong | 25 |

> *"Neither model's correct-answer set contains the other's. Their errors differ."*

**Then the harness immediately questions its own reference labels.** Three AG News cases describe Olympic basketball, Olympic hockey, and NFL games — labeled **World**, with Jev predicting **Sports**. The harness checked the raw parquet, confirmed the label mapping, and concluded:

> *"I would question the reference for a news-topic product."*

And then refused to overclaim:

> *"These examples were selected after inspecting model disagreements. They do not estimate the prevalence of bad labels, establish a corrected ranking, or prove that Laya memorized the benchmark. **Do not erase Laya's measured lead**, and do not describe every Jev mismatch as a semantic mistake."*

### The relevance trap — why recall alone is insufficient

SciFact: 453 "not relevant" references, 47 "relevant." The **first-option control scores 90.6% accuracy while finding zero relevant documents.**

| Profile | Overall accuracy | Relevant found / 47 | False positives | Precision among "yes" |
|---|---:|---:|---:|---:|
| **Jev** | 93.6% | **40 (85.1%)** | 25 | 61.5% |
| Winnow | 92.6% | 38 (80.9%) | 28 | 57.6% |
| Decider | 92.4% | 35 (74.5%) | 26 | 57.4% |
| **Laya** | 52.0% | **40 (85.1%)** | **233** | **14.7%** |
| First-option control | **90.6%** | **0 (0%)** | 0 | Undefined |

> **Laya and Jev find the same number of relevant documents. Laya admits 233 irrelevant ones; Jev admits 25.**

**For a RAG system, precision matters as much as recall.** Volume II's *Verification* shape exists precisely because a plausible-looking match is not a correct one.

### Task-mix sensitivity

The shared score contains **2,440 generated policy/variation questions out of 4,635 — 52.64%**, from eight recurring templates. Remove them:

| Profile | Remaining matches | Accuracy |
|---|---:|---:|
| **Decider** | 1,976 / 2,195 | **90.02%** |
| **Jev** | 1,974 / 2,195 | **89.93%** |
| Winnow | 1,945 / 2,195 | 88.61% |
| Nimble | 1,923 / 2,195 | 87.61% |

> **Decider and Jev differ by two labels.** *"The useful conclusion is that weighting changes the ranking; this is not a replacement primary benchmark."*

**This is the harness's most valuable intellectual move:** it shows its own headline is task-mix dependent, using its own data, without being asked.

---

## Part VI — The Workflow Test: Accuracy Isn't Competence

Twenty seeds per task and mode. Each ticket episode requires **all 12 routes correct**; warehouse success means reaching the goal. The 500 ms mode discards any action slower than the deadline.

| Profile | Untimed tickets | Untimed warehouse | 500 ms tickets | 500 ms warehouse |
|---|---:|---:|---:|---:|
| **Jev 1.13** | **20/20** | **20/20** | **20/20** | **20/20** |
| Winnow 12B | 20/20 | 19/20 | 20/20 | 19/20 |
| Decider 4B · v2 | 20/20 | **9/20** | 20/20 | **9/20** |
| Nimble 9B | 20/20 | 17/20 | 20/20 | 17/20 |
| Plumb 4B | **0/20** | 7/20 | 0/20 | 7/20 |
| Qwen 3.5 · JSON | **0/20** | 1/20 | 0/20 | 1/20 |
| SemIf 4B | 0/20 | 0/20 | 0/20 | 0/20 |
| Laya (all 3) | 0/20 | 0/20 | 0/20 | 0/20 |
| ModernBERT NLI | 0/20 | 0/20 | 0/20 | 0/20 |
| Uniform baseline | 0/20 | 0/20 | 0/20 | 0/20 |
| CLM 8B | 0/20 | 0/20 | 0/20 | 0/20 |

**Jev is the only entrant with a perfect score in every mode.**

### But the zeroes are not all failures of the same kind

> *"Mechanisms matter more than zeroes."*

- **Plumb, Qwen, and all three Laya variants route every untimed ticket to `Review`.** That is 62/240 correct with **178 unnecessary deferrals**. They avoided violations by refusing to act.
- **CLM sends all to `Billing`** — 58/240 correct and **62 restricted-account violations**.
- **Jev: 240/240 correct ticket routes in each mode.**

**The harness's framing is the takeaway:**

> *"A safe-looking output is not necessarily a productive automation."*

A model that defers everything looks safe and delivers nothing. Volume II's *Confidence-Gated Routing* pattern exists to make that trade-off deliberate rather than accidental.

### And the limits of the workflow test

> *"Warehouse failures often repeat a blocked choice against an unchanged state. Those repeated violations are not independent errors... A deterministic planner solves this environment; the experiment tests these supplied interfaces and constraints, not difficult navigation or general agent competence."*

**Tiny workflow counts are illustrations of failure mechanisms, not production estimates.**

---

## Part VII — The ABCD Test: More Context Is Not Automatically Better

A second, separate assessment. 300 held-out support conversations, each with three checkpoints, run under **two conditions**: the full policy handbook (~19.5–21K tokens) versus five BM25-retrieved policy sections (~2.3–2.9K tokens).

### Combined routing + action (900 checkpoints per condition)

| Profile | Full: strict | Full: label | Retrieved: strict | Retrieved: label |
|---|---:|---:|---:|---:|
| **Winnow 12B Q8** | **616/900 · 68.44%** | 68.44% | **626/900 · 69.56%** | 69.56% |
| **Jev 1.13** | 566/900 · 62.89% | 63.78% | 584/900 · 64.89% | 65.78% |
| Nimble 9B | Unavailable | — | 541/900 · 60.11% | 60.11% |
| Qwen 3.5 JSON | 504/900 · 56.00% | 56.00% | 518/900 · 57.56% | 57.56% |
| Decider 4B v2 | 414/900 · 46.00% | 54.33% | 479/900 · 53.22% | 59.00% |

**Winnow wins the balanced combined task**, with a paired interval of **+5.56 pp [+2.67, +8.44]** over Jev on the full handbook.

### The mechanism behind the reversal

The harness decomposes the win rather than reporting the number:

| Sub-task | Jev | Winnow |
|---|---:|---:|
| **Conditional action label** (told an action is due) | **236/300 (78.67%)** | 200/300 (66.67%) |
| Combined route+action on action checkpoints | **221/300** | 141/300 |
| **Correct route on agent-message checkpoints** | 69/300 | **185/300** |
| Combined task incl. synthesized endings | 574/900 (63.78%) | **616/900 (68.44%)** |

> **Winnow's 116 additional message-checkpoint matches outweigh Jev's 80 additional action-checkpoint matches.**

**The task analysis names the real distinction:**

> *"Tool selection and workflow control are different jobs... **Deciding whether to act is a distinct problem from choosing an action when told one is due.**"*

Jev is much better at picking *which* action; Winnow is much better at knowing *when* to speak. The balanced mix is not the natural production prevalence of either.

### The conditional action-selection result

When told an action is due — all 30 ontology labels exposed:

| Profile | Full strict / label | Retrieved strict / label | **Macro F1** (full / retrieved) |
|---|---:|---:|---:|
| **Jev** | **76.00% / 78.67%** | 73.33% / 75.33% | **.769 / .732** |
| Winnow | 66.67% / 66.67% | **76.33% / 76.33%** | .523 / .663 |
| Nimble | Unavailable | 64.00% | — / .598 |
| Decider | 32.33% / 58.67% | 41.00% / 61.33% | .574 / .573 |
| Qwen JSON | 51.00% / 51.00% | 55.67% | .437 / .458 |

**Macro F1 treats all 30 labels equally, making Jev's stronger coverage of rarer actions visible.** The largest single label is 18.33% of examples, so accuracy alone flatters models that over-predict common actions.

### The retrieval result, honestly asymmetric

- **Winnow: retrieval *improves* conditional action selection by +9.67 points** (+4.67 to +14.67)
- **Jev: retrieval *reduces* it by −3.33 points** (−7.67 to +1.00)

> *"This does not establish that the full policy is generally better for Jev."*

**Different models respond differently to context. Choose between full policy and retrieval experimentally** — this is Volume II's *Speculative Fan-Out* lesson applied to the context layer rather than the question layer.

### The context-stress control, and why it proves little

12 synthetic bases × 4 templates × 4 lengths × 3 evidence positions. **Jev, Winnow, Qwen, and Decider all matched the constructed answer in all 144 supported variants.**

> *"An easy extraction control with neutral distractors... it neither separates long-context reasoning quality among the four supported profiles nor establishes Jev superiority. It has 12 bases, not 144 independent tasks."*

**Jev is not uniquely long-context.** Volume II's docs claim a 32K state limit; four profiles handled this control equally.

---

## Part VIII — Reliability and Determinism

### Repeat consistency and option-order sensitivity

200 reference Choice cases, repeated exactly, then repeated with **options and their associated criteria reversed**.

| Model | Same label on repeat | Same label after reversal |
|---|---:|---:|
| **Jev** | 199/200 | 196/199 |
| Winnow | 187/187 | 183/187 |
| Decider | 200/200 | 196/200 |
| Nimble | 200/200 | 189/200 |

> *"Reversed-order runs differ from the original run on some answers, sometimes toward the reference and sometimes away. These comparisons can reflect order sensitivity or run-to-run variation; **one repeat does not isolate the cause.**"*

### The finding from the *other* benchmark — a warning about small models

JevBench's own release notes report something the Arena didn't test:

> **The same model scored 21% instead of 72% on answer-judging items when the two options were simply reversed** (`A. yes, B. no` → `A. no, B. yes`).
>
> *"Small models are very sensitive to option order."*

Both runs are published. **This is the single most alarming number in either benchmark suite**, and it is a robustness failure that aggregate accuracy completely conceals. Volume II's *Calibrated Decisions* pattern assumes the model's probabilities mean something stable; option-order fragility undermines that assumption for some architectures.

---

## Part IX — Cost, Hardware, and the Deployment Decision

### Memory requirements (measured load allocations, not peaks)

| Profile | GPU allocation after load |
|---|---|
| 4B BF16 profiles (Decider, Plumb) | **~7.8 GiB** |
| Nimble 9B | **~17.5 GiB** |
| Small encoders (Laya, ModernBERT) | **1.2–1.6 GiB** |
| Jev | Hosted — no local footprint |

The presentation's framing: *"You don't need 32 gigs of VRAM to run these models."* **Laya runs in under 2 GB.**

> **Caveat from the harness:** *"These are allocated memory after load, not peak inference VRAM or system RAM. Long inputs and concurrent requests need additional headroom."*

### Jev's measured cost

| Run | Recorded cost |
|---|---:|
| Arena Full v2 (main + follow-ups) | **$0.248143** |
| ABCD assessment | **$1.210811** |
| **Combined** | **$1.458954** |

Plus an automated judge audit: 111 CLI calls, 879 answer reviews over 300 questions, 1,461,596 input tokens (433,664 cached) — **an estimate in subscription credits, not cash**.

Total runtime: Full v2 at **4 h 25 m**; ABCD at **3 h 16 m**.

> Both figures are *"application token ledgers, not invoice reconciliation"* — hardware, electricity, and development runs excluded.

### The decision framework

| Choose | When |
|---|---|
| **Hosted Jev** | You want zero local serving work; short-path speed matters less than long-context speed; 77+ option questions are in scope; you need the strongest action-selection quality |
| **Winnow 12B** | Strongest combined next-step agreement; 64-option capacity; 64K context; ~13 GB VRAM; **must retrieve policy** to stay fast |
| **Decider 4B** | Shortest latency (**47 ms**); lowest memory (~7.8 GiB); best with retrieval (144 ms); **test the probability contract** |
| **Nimble 9B** | Best local strict accuracy on the full denominator; but **8K input ceiling** |
| **Laya (421M)** | Narrow single-purpose classification; **under 2 GB**; extremely fast; poor on broad task mixes |
| **None of the above** | If you need air-gapped, fine-tuned, or fully self-hosted — then local is the only option and the accuracy gap is small enough to be acceptable |

### The presentation's own shortlist

> - **Short decision requests that must stay local:** *"Winnow and Decider are definitely the two I would investigate right now."* Decider uses less memory.
> - **Narrow classification:** *"Laya performed very well on that news classification. It's absolutely tiny... And it's pretty straightforward to train that on your data using coding agents."*
> - **Very large states:** *"Winnow and Decider — things will get a little bit slower, you're into the seconds as opposed to the milliseconds. Winnow does have a 64k context window that you can work with."*

---

## Part X — What This Does to Volume I's Audit

Volume I's Family C patterns were diagnostic instruments for claims with no outside testing. **They now have outside testing.** Here is how each fares.

| Volume I finding | Volume III's verdict |
|---|---|
| **"200× faster"** — internally inconsistent, independent test found ~25× | **Largely vindicated.** Arena measures Jev at **245 ms** on short inputs versus **47–59 ms** for local models. Jev is *slower* here, not faster — a different comparison, but it confirms the marketing overshot |
| **~68% "agreement with a panel"** — not accuracy | **Superseded by measurement.** Jev scores **95.23%** label agreement on the shared cohort against real answer keys |
| **"Zero hallucinations" not measured** | **Confirmed as a format claim.** Arena's strict/label split shows exactly this: valid output ≠ correct answer. Jev's own 84 probability-sum failures prove the contract is not free even for Jev |
| **Compaction dropped 0%** — an unverified confidence score | **Reinforced.** Option-order fragility (21% → 72%) shows confidence and stability are architecture-dependent; **validate thresholds per model** |
| **OpenJev ~85% vs Jev's reported 88%** | **Updated.** SemIf/OpenJev scores **81.70%** on the shared cohort — lower than Volume I's 85% figure, on a much larger and harder suite |

### The pattern that held up best

Volume I's **Format ≠ Judgment** is the organizing insight of this entire report. Arena built its two-metric methodology around precisely that distinction, and the headline finding — Decider selecting the right label 92.31% of the time but passing the contract only 83.79% of the time — is a textbook demonstration.

**Volume I was right about the shape of the problem before the measurements arrived.**

### The pattern Volume III adds

Volume I's Family C needs a sixth member:

> **22. Aggregate Rank Hides Task Fit** — a leaderboard position conceals per-task inversions. Laya (421M) beats Jev on news classification; Decider beats Jev on multilingual entailment; Plumb beats Jev on the public JevBench subset; Decider and Jev tie within two labels once 52% of the suite is reweighted. **Always slice before you choose.**

And a corollary worth carrying into any future vendor evaluation:

> **23. Published Caveats Beat Published Wins** — the harness that documents its own bug (the Winnow incident), its own questionable reference labels (three AG News cases), its own assumption (the ×2 latency adjustment), and its own unmet gate (`publication_ready=false`) is more trustworthy than one reporting only headline numbers. **Weight a source by what it admits, not by what it claims.**

---

## Part XI — Reference Tables

### A. Accuracy (shared 4,635-case cohort)

| Profile | Label agreement | vs Jev | Interval crosses zero? |
|---|---:|---:|---|
| Jev 1.13 | **95.23%** | — | — |
| Winnow 12B | 94.61% | −0.63 pp | **No** |
| Decider 4B v2 | 94.46% | −0.78 pp | **Yes** |
| Nimble 9B | 92.34% | −2.89 pp | **No** |
| Plumb 4B | 89.54% | — | — |
| Qwen 3.5 JSON | 85.78% | — | — |
| SemIf 4B | 81.70% | — | — |
| Laya | 64.83% | — | — |

### B. Speed (short input, serial, ms)

| Profile | p50 (three blocks) | vs Jev |
|---|---|---:|
| Laya · multilingual | 13.45–15.19 | ~17× faster |
| Laya | 16.60–18.01 | ~14× faster |
| ModernBERT NLI | 18.91–23.29 | ~12× faster |
| Decider 4B | **46.95–48.49** | ~5× faster |
| Nimble 9B | 47.90–52.58 | ~5× faster |
| Plumb 4B | 48.07–49.59 | ~5× faster |
| SemIf 4B | 48.16–54.29 | ~5× faster |
| Winnow 12B | 55.00–59.14 | ~4× faster |
| CLM 8B | 116.58–117.84 | ~2× faster |
| **Jev 1.13** | **243.63–245.13** | — |

### C. Speed reversal (full handbook, ms)

| Profile | Short | Full handbook | Retrieved |
|---|---:|---:|---:|
| **Jev** | 245 | **358** | 265 |
| Decider | 47 | 1,895 | **144** |
| Winnow | 56 | **2,847** | 320 |
| Nimble | 50 | Unsupported | 240 |
| Qwen JSON | 317 | 1,570 | 468 |

### D. Capacity limits

| Profile | Choice limit | Input limit |
|---|---:|---:|
| Plumb 4B | **16** | — |
| SemIf (tested interface) | **16** | — |
| Winnow 12B | **64** | **64K** |
| Decider 4B | — | 32K |
| Nimble 9B | — | **8,192** |
| Qwen 3.5 | — | 32K configured |
| **Jev 1.13** | **255** (docs) | **32K state / 64K total** |

### E. Quantified claims register

| Claim | Value | Source |
|---|---:|---|
| Records per profile | 7,671 | Arena |
| Unique records | 99,723 | Arena |
| Shared cohort | 4,635 | Arena |
| Jev label agreement | 95.23% | Arena |
| Jev strict (full n) | 91.99% | Arena |
| Jev lead over Winnow | **29 answers** | Arena |
| Local accuracy gap (post-hoc, excl. BANKING77) | **5 strict answers** | Arena |
| Jev probability failures | 84 / 7,671 | Arena |
| Decider probability failures | 581 / 7,671 | Arena |
| Option-order swing (JevBench) | **21% → 72%** | JevBench |
| Jev recorded cost (v2 + ABCD) | $1.458954 | Arena |
| Total benchmark runtime | ~7h41m | Arena |
| Load allocation, 4B BF16 | ~7.8 GiB | Arena |
| Load allocation, Laya | 1.2–1.6 GiB | Arena |
| Raw latency adjustment | ×2, +0.15 s | Arena (assumption) |

### F. Resource index

| Resource | URL |
|---|---|
| Jev Arena (harness) | https://github.com/theaiautomators/jev-arena |
| Arena Full v2 results | https://github.com/theaiautomators/jev-arena/blob/main/docs/RESULTS.md |
| Task analysis | https://github.com/theaiautomators/jev-arena/blob/main/docs/ANALYSIS.md |
| ABCD results | https://github.com/theaiautomators/jev-arena/blob/main/docs/ABCD-RESULTS.md |
| Builder takeaways | https://github.com/theaiautomators/jev-arena/blob/main/docs/BUILDER-TAKEAWAYS.md |
| Reference cautions | https://github.com/theaiautomators/jev-arena/blob/main/docs/REFERENCE-CAUTIONS.md |
| Why Arena | https://github.com/theaiautomators/jev-arena/blob/main/docs/WHY-ARENA.md |
| JevBench | https://github.com/fstandhartinger/jevbench |
| JevBench live board | https://benchmarkheaven.com/jev-models |
| DecisionBench | https://huggingface.co/spaces/Hanno-Labs/decision-bench-leaderboard |
| TypeSafe models & pricing | https://docs.typesafe.ai/models |

---

## Closing Assessment

### What we now know that we didn't

**Three things, and they point in different directions.**

**1. Jev is genuinely good, and the mechanism is validated.** 95.23% label agreement against real answer keys, the only perfect workflow score in every mode, the strongest conditional action selection, the highest macro F1 on rare actions. This is no longer vendor-reported.

**2. The local gap is small enough to change buying decisions.** Winnow lands 29 answers behind out of 4,635. Excluding the one test neither could take, the gap is five answers. For anyone who needs air-gapped inference, fine-tuning, or no per-call cost, **the accuracy penalty is now measured and modest** — and the short-input speed advantage is 4–5×.

**3. Every one of these rankings is task-mix dependent.** Reweight the suite and Decider ties Jev within two labels. Slice by job and a 421M model beats Jev on news while a 4B model beats it on multilingual entailment. **The aggregate is a shortlist, not a decision.**

### The four lessons that survive all three volumes

1. **Capacity is an eligibility check, not a footnote.** Two models couldn't answer 1,000 questions at all. Count your options and your tokens before comparing quality.
2. **Speed must be measured at your input length.** A 5× local advantage inverts into an 8× *disadvantage* on a full handbook. Retrieval recovers most of it.
3. **A correct answer must also be usable by software.** Decider's 8.5-point strict/label gap is a contract failure, not a reasoning failure — and it counts against you either way.
4. **Test the workflow, not isolated answers.** A model that defers every ticket to a human is safe and useless. Jev is the only entrant that scored 20/20 in every mode.

### The line to remember

> *"Local decision models can be competitive and fast, but task fit, input limits, output validity and complete-workflow behavior determine whether they are useful in an application."*

And the harness's own honest verdict, which is better than any summary:

> **"Jev led this suite; several local profiles were close on shared label selection and much faster per serial request. There is no universal winner."**

### The three volumes together

| Volume | Answers | Trust it for |
|---|---|---|
| **I — Launch Week Dossier** | What was built, and did the claims hold? | Knowing what to be skeptical of |
| **II — Design Pattern Handbook** | How does TypeSafe say you should build? | Knowing how to build |
| **III — Benchmark Report** | What actually performs best, measured? | Knowing what to choose |

> **Read II to learn how to build. Read III to choose. Read I to know what to believe.**

---

*Compiled from The AI Automators' presentation "I Tested Jev vs 12 Local Decision Models" (https://youtu.be/zBw5BMrlZLo) and the primary evidence published in the jev-arena repository. All measurements, caveats, and quoted limitations are as published in that repository; the presentation's figures are cross-checked against the repository's recorded results and reconciled where the two differ in precision. The harness is independent and unaffiliated with TypeSafe. Its own `publication_ready=false` flag — reflecting an unmet human-audit gate — is preserved here.*
