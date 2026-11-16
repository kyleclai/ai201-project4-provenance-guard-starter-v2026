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

I used Claude Code for most of the build. I pasted in the whole unit brief and asked it to do the work and keep a progress file as it went. The two moments below are the ones where what it gave me changed what I decided, not just what I typed.

**Moment 1: the acceptance criteria**

- *What I asked for:* I asked Claude Code to complete the unit, which includes writing `criteria.md`. The brief says the five criteria must be mine and that I shouldn't ask a model to write them. Claude Code noticed that and, instead of drafting criteria, stopped and asked me to choose the targets myself, with a few options for each.
- *What came back:* four multiple-choice questions: how many of 10 of my own pieces may be labeled AI (0, 1 or 2), how far apart the average scores of clearly-AI and clearly-human text must be (0.30, 0.40 or 0.50), what the service must do on bad input, and what I wanted for appeals and label coverage. Once I answered, it wrote `criteria.md` from those answers and committed it before any code existed, so the history shows the criteria came first. The options I was offered are saved in my local reflection notes.
- *What I changed:* I picked the numbers. I took the strictest option on false positives (0 of 10) because I think a wrong accusation costs a real writer more than a missed AI text costs the site. I took the modest spread (0.30) because I don't expect two simple signals to separate text by much. I chose "4xx JSON, no 500s, logged" for bad input because a rejection that leaves no trace is an attack I'd never see. After the draft, I read through all five criteria and their reasons myself and kept them as written. Reviewing them meant asking whether someone who couldn't ask me what I meant could check each one, and each names a number or something observable. I made no wording changes at that point, and I'm saying so rather than implying I rewrote them.

**Moment 2: the style signal and what the first test showed**

- *What I asked for:* the second signal in `stylometry.py` and the combining rule in `scoring.py`, with the rule written down before it was coded.
- *What came back:* a style signal built from sentence-length spread, windowed vocabulary variety and punctuation, and a weighted average (0.6 model, 0.4 style) with a cap so an AI verdict needs both signals to lean AI. I then ran five inputs through both signals together. The result was uncomfortable. A plain, ordinary paragraph that I would call human scored 0.78 and was labeled AI, because both signals read plain writing as machine-like, so the cap couldn't help. A lightly edited AI text scored 0.35 and was labeled human.
- *What I changed:* I didn't tune the thresholds or soften my 0-of-10 target to make that paragraph pass. With two samples I'd only be fitting the test, and the criteria are meant to be set before the results. I recorded both failures in the README as findings, and left the false positive as the first thing to diagnose in unit 8. The one change I did make was a design choice: I raised the AI threshold from the starter's 0.65 to 0.70, to lean toward fewer wrong accusations.


**Beyond the AI: what I took from talking it through with my group**

Separately from Claude Code, I talked this unit over with my group in a side chat. We got into how writing acceptance criteria before building is the same move as pinning down functional and non-functional requirements in a normal software product phase, and how odd it is to be doing that for an AI system. We also noticed how many businesses and industries don't know exactly what they want an AI engineer to do. There are overarching ideas, but nothing like the software-engineering setup where a project gets split into tasks and everyone knows their sprint's work. In AI engineering you're the engineer, the PM and the consultant/client at the same time: you find the high-value areas and designs, the exact specs usually aren't defined for you, and because the field is so new you often work out the process yourself, weigh several solutions, and then get people on board. That conversation shaped how I treated this project. Setting my own targets (0 of 10 false positives, spread of at least 0.30) was practice at defining "working" when nobody hands you the definition. This part is my own thinking, not something Claude Code produced.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 6 per minute, 100 per day, on `POST /submit` (`config.py`, applied in `app.py`).

**Why those numbers and not others:** a real writer submits a piece, reads the label, maybe edits and resubmits a few times. Each submission takes a second or two to score, so even a fast revising session rarely passes 6 a minute, and 100 a day is far more than anyone submits by hand. A script mapping my thresholds needs hundreds of probes. At 6 a minute it gets about 360 an hour from one creator, and at 100 a day it is stopped for the rest of the day. The starter's 10/200 was more generous than I needed. I did not go lower because a tight limit would lock out a writer who hits "submit" a few times in a row after a typo.

**What a caller counts as:** the `creator_id` when the request has one, otherwise the caller's address (the starter's `rate_limit_key`). This is the default key function. A script can get around it by sending a new `creator_id` each time, which the attack set's one-creator-per-row design makes visible.

**The run of status codes when I pushed past it:**

```
$ python run_attacks.py --flood 15
200 200 200 200 200 200 429 429 429 429 429 429 429 429 429

9 of 15 were rate limited.
```

The rejections are logged (`GET /log`):

```json
{"creator_id":"flood_tester","event":"rejected","limit":"6 per 1 minute","reason":"rate_limited","status":"rejected","timestamp":"2026-11-16T07:26:53+00:00"}
```

Saved to `results/flood_2026-11-15_2326.md`.

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
