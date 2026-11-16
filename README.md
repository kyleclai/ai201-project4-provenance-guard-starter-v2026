# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

A submission takes seven steps (the full trace is in [DESIGN.md](DESIGN.md)):

1. `POST /submit` (`app.py::submit`) validates `text` and `creator_id`. Bad input gets a 4xx JSON error and a `rejected` log entry.
2. A `content_id` (uuid) is minted. The appeal endpoint needs it.
3. Signal one (`detector.py::model_signal`) runs GPT-2 locally and returns `model_score`.
4. Signal two (`stylometry.py::style_signal`) measures the shape of the text and returns `style_score`.
5. `scoring.py::combine_signals` merges them into `combined_score`.
6. `scoring.py::score_to_label` maps the score to `ai` / `human` / `unsure` plus a plain-English label. `confidence` = `|combined - 0.5| * 2`.
7. `audit.py::log_decision` writes all three scores, guess, label and status to `logs/audit.jsonl`, and the JSON goes back to the caller.

`POST /appeal` checks the `content_id` exists (404 if not), appends an `appeal` entry with the writer's reasoning (status `under_review`) next to the original decision, and confirms.

---

## Signals and Scoring

### Signal one: the model signal

**What it measures:** perplexity under GPT-2 (run locally), i.e. how predictable the text is, mapped to 0-1 (higher = more AI-like).

**Why that might differ between human and AI writing:** generated text is the likely continuation, so a language model finds it easy to predict. People are less predictable.

**What it can't see:** meaning, facts, or who wrote it. Plain, conventional human writing is also predictable and reads as AI (see the false positive in my calibration run below). Light editing of AI text can push it toward "human". GPT-2 is small and old, and short texts give noisy readings.

### Signal two: the style signal

**What it measures:** three things, each turned into 0-1 "AI-likeness": sentence-length spread (stdev / mean, weight 0.5), vocabulary variety (50-word moving-window type-token ratio, weight 0.25) and punctuation (rate of commas, semicolons, dashes, quotes, ! and ?, plus variety of marks, weight 0.25).

**Why that might differ between human and AI writing:** generated prose tends toward even, mid-length sentences and a narrower vocabulary. Human writing is lumpier.

**What it can't see:** meaning, entirely. Anything that changes the shape but not the substance moves it: typos, chopped sentences, pasted quotes. A human who writes in short even sentences looks AI-like. One-sentence or very short texts return a neutral 0.5 for the parts it can't measure.

### The combining rule

**The rule:** weighted average of the two signals, with one safeguard: an AI verdict needs both signals to lean AI. If either signal is below 0.5, the combined score is capped just under the AI threshold (0.69), so a disagreement can land in "unsure" but never "ai".

**The numbers:** model weight 0.6, style weight 0.4, human threshold 0.35, AI threshold 0.70 (all in `config.py`). I weight the model signal higher because it was the more discriminating one in calibration. I put the AI threshold above the 0.65 starter value and added the cap because a wrong accusation costs a writer more than a missed detection costs the site.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:** a lightly edited AI text ("Remote work has changed how teams collab, no doubt... honestly. Its not perfect...") scored model 0.247 / style 0.500. The average (0.348) lands in "human" and the cap doesn't matter, so the AI text got through. The cap protects against the opposite split. This is the missed-detection side of the trade I chose.

**Calibration run (both signals, one table):**

| Input | model | style | combined | guess |
|---|---|---|---|---|
| clearly AI | 0.854 | 0.744 | 0.810 | ai |
| clearly human (chatty, varied) | 0.469 | 0.106 | 0.324 | human |
| plain conventional human | 0.818 | 0.726 | 0.781 | **ai (false positive)** |
| lightly edited AI | 0.247 | 0.500 | 0.348 | human (missed) |
| borderline committee minutes | 0.475 | 0.589 | 0.520 | unsure |

The plain-human row is the failure my criterion 1 (0 of 10) is aimed at. Both signals read plain writing as AI, so the cap doesn't help. I have not changed the thresholds or the criterion to hide it; this is a finding to diagnose in unit 8.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 - 0.35 | We think this was probably written by a person. Our checks found nothing that suggests otherwise. |
| unsure | 0.35 - 0.70 | We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece. |
| high-confidence AI | 0.70 - 1.00 | Our checks suggest this may have been written with an AI tool. We can get this wrong. If you wrote it yourself, you can appeal and a person will take a look. |

**Why I worded the "unsure" one this way:** it says plainly that nothing was concluded and that real people land here often, so it doesn't read as an accusation. The AI label says "suggest" and "may", admits the system can be wrong, and tells the writer what to do next.

All three are reachable: the Sample Run submissions below produced all three.

---

## Sample Run

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I missed the bus again. Third time this week! My sister laughed at me over the phone, then told me about her dog eating a whole birthday cake (candles and all, apparently). Honestly? I walked the two miles in the drizzle and didnt mind. There is something about wet pavement and a bad mood that clears the head.", "creator_id": "writer-001"}'
```

```json
{"combined_score":0.2765,"confidence":0.447,"content_id":"3b2ec0a4-0956-4704-b17e-4f740eecb63b","guess":"human","label":"We think this was probably written by a person. Our checks found nothing that suggests otherwise.","model_score":0.3998,"status":"decided","style_score":0.0915}
```

The other two labels, from the same run:

```json
{"combined_score":0.8097,"confidence":0.6194,"guess":"ai","model_score":0.8537,"style_score":0.7438,"status":"decided"}
{"combined_score":0.5205,"confidence":0.041,"guess":"unsure","model_score":0.4751,"style_score":0.5886,"status":"decided"}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "3b2ec0a4-0956-4704-b17e-4f740eecb63b", "reasoning": "I wrote this myself on the walk home."}'
```

```json
{"content_id":"3b2ec0a4-0956-4704-b17e-4f740eecb63b","message":"Thank you. Your appeal has been recorded and this piece is now under review.","status":"under_review"}
```

An unknown id returns `{"error":"unknown_content_id","message":"No submission with that content_id."}` with status 404.

**What the log shows afterwards** (entries for that content_id from `GET /log`):

```json
[
  {"combined_score": 0.2765, "content_id": "3b2ec0a4-0956-4704-b17e-4f740eecb63b", "creator_id": "writer-001", "guess": "human", "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.", "model_score": 0.3998, "status": "decided", "style_score": 0.0915, "timestamp": "2026-11-16T06:56:10+00:00"},
  {"content_id": "3b2ec0a4-0956-4704-b17e-4f740eecb63b", "creator_id": "writer-001", "event": "appeal", "reasoning": "I wrote this myself on the walk home.", "status": "under_review", "timestamp": "2026-11-16T06:56:10+00:00"}
]
```

Bad input (missing text, empty, whitespace, non-string, missing creator_id, non-JSON) returned 400 each, text over 50,000 characters returned 413, and `/ping` still answered afterwards. Each rejection is a `rejected` entry in the log.

---

## How I Used AI

**Moment 1**

- *What I asked for:* Claude Code to build the whole unit and keep a progress file. Before it wrote `criteria.md` it stopped and asked me to choose the targets (false positives, spread, appeals, bad input), because the assignment says the criteria must be mine.
- *What came back:* a draft of `criteria.md` built from my four answers, written and committed before any results existed.
- *What I changed:* <!-- EDIT THIS: say what you actually changed in the wording or reasons -->

**Moment 2**

- *What I asked for:* the style signal and combining rule.
- *What came back:* a three-measure style signal and a weighted average with an "AI needs both signals" cap. The first calibration run flagged a plain human paragraph as AI (0.78).
- *What I changed:* nothing in the thresholds or criteria; I recorded the false positive as a finding instead of tuning to two samples.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
