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


**Unit 8: using AI to run and diagnose the tests**

**Moment 3: the attack run and the diagnosis**

- *What I asked for:* Claude Code to run the staff attack set against my service before changing anything, mark each attack held or broke, and diagnose every failure.
- *What came back:* 22 broken of 56, with a held/broke table I could read. The useful part came when it did not take the evasion attacks at face value: it scored the **unedited** AI paragraph behind them with my own functions and found it already scored 0.552, "unsure", before any edit. That turned several "evasions" into pre-existing misses of signal two and my combining rule, instead of attacks that had worked.
- *What I changed:* the diagnosis. I stopped blaming the edits for six of the nine evasions and put the cause on signal two, which I had weighted 0.4 and given veto power in `combine_signals`. Claude Code wrote the held/broke rules and I should say plainly that they are its judgment calls (for example, "unsure" counts as BROKE for AI text but HELD for human text). They are written at the top of the Attack Run section so they can be argued with.

**Moment 4: choosing the ten pieces of my own writing**

I like notetaking the machinations of my mind: thoughts, things I'm learning, mental models, questions about what I'm doing, and a lot of philosophical developer golden tidbits I hear from the people in my life. I think there might be something in there I haven't figured out yet, and so I wanted to pick the ten pieces from my notes purposefully to see if I could uncover/flip over a hidden/undiscovered seashell with a pearl.

I chose a series of candidate notes and then also used Claude Code to help search my notes for other candidates I didn't consider, with my rules: my own writing, nothing sensitive, natural prose over bullets. It was most useful for what it ruled out. Some of my notes were AI-written or AI-summarized, one was copied from the web, and it said plainly it couldn't verify who wrote what. So the final calls were mine. I added two pieces I'd written (my bio and a question about staying aligned with the business), and swapped out the piece that sounded the most AI for another question of mine. Names and personal details came out before anything went into `scenarios.py`.

It also showed me how little of my writing is plain, assignment-style prose. Mine is mostly fragments and half-formed questions, which is probably why criterion 1 passed so easily. I'd like to retest it on plainer writing.

**Moment 5: choosing the one improvement**

- *What I asked for:* the single change that best followed from the diagnoses.
- *What came back:* two candidates with numbers. Moving the AI threshold from 0.70 to 0.80 clears the four false positives, but my five AI texts score 0.69 to 0.79, so all would become "unsure". Validating input in the route fixes the only crash and five junk-input verdicts with no new misses. It recommended the second.
- *What I changed:* I went with input validation. It does not touch the false accusations I care most about, and thus added that as a note into What's Still Broken. Additionally, I noted that the all-MET result on my own criteria are too narrow and can't be considered a success.

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

## Attack Run: Before

Run with nothing changed since the end of unit 7 except the rate limiter and the log: `python run_attacks.py --set attack_set --label before`. Full output: `results/attack_run_2026-11-15_2328_before.md`. **56 attacks: 22 BROKE, 34 HELD.**

**How I marked held and broke.** The set says what each attack was going for, so I judged each against that goal, and I applied the same asymmetry as my criteria:
- *Evasion and injection* (AI text, with or without an instruction attached): HELD only if the system said **ai**. Anything else (`human` or `unsure`) means AI text got past the check, so BROKE.
- *False positives* (human writing): HELD if the system did **not** say `ai`. `unsure` is a safe landing. A confident `ai` label on a person's work is BROKE.
- *Injection that targets the output* (hostile label, log injection): HELD if the output stayed clean.
- *Malformed*: HELD if a 4xx JSON came back or the service gave a sensible answer. BROKE on a crash, or on a confident `ai`/`human` verdict on something that isn't prose.
- *Flood*: HELD if the limiter returned 429 partway through.

The score columns are the audit log's, joined to the run by `content_id`. The run report's own "Score" column is my `confidence` (distance from 0.5), not the combined score, so I did not use it.

| ID | Family | Status | Guess | model | style | combined | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | 200 | human | 0.164 | 0.589 | 0.334 | **BROKE** |
| EV02 | evasion | 200 | unsure | 0.594 | 0.208 | 0.440 | **BROKE** |
| EV03 | evasion | 200 | unsure | 0.666 | 0.277 | 0.510 | **BROKE** |
| EV04 | evasion | 200 | unsure | 0.611 | 0.566 | 0.593 | **BROKE** |
| EV05 | evasion | 200 | human | 0.321 | 0.190 | 0.269 | **BROKE** |
| EV06 | evasion | 200 | unsure | 0.573 | 0.283 | 0.457 | **BROKE** |
| EV07 | evasion | 200 | unsure | 0.586 | 0.303 | 0.473 | **BROKE** |
| EV08 | evasion | 200 | unsure | 0.245 | 0.548 | 0.366 | **BROKE** |
| EV09 | evasion | 200 | unsure | 0.704 | 0.361 | 0.567 | **BROKE** |
| EV10 | evasion | 200 | ai | 0.979 | 0.719 | 0.875 | **HELD** |
| FP01 | false_positive | 200 | unsure | 0.618 | 0.501 | 0.571 | **HELD** |
| FP02 | false_positive | 200 | ai | 0.739 | 0.695 | 0.721 | **BROKE** |
| FP03 | false_positive | 200 | ai | 0.805 | 0.586 | 0.718 | **BROKE** |
| FP04 | false_positive | 200 | ai | 0.833 | 0.571 | 0.728 | **BROKE** |
| FP05 | false_positive | 200 | ai | 0.800 | 0.769 | 0.788 | **BROKE** |
| FP06 | false_positive | 200 | unsure | 0.881 | 0.496 | 0.690 | **HELD** |
| FP07 | false_positive | 200 | unsure | 0.882 | 0.495 | 0.690 | **HELD** |
| FP08 | false_positive | 200 | unsure | 0.322 | 0.441 | 0.370 | **HELD** |
| PI01 | prompt_injection | 200 | unsure | 0.463 | 0.277 | 0.388 | **BROKE** |
| PI02 | prompt_injection | 200 | human | 0.204 | 0.241 | 0.219 | **BROKE** |
| PI03 | prompt_injection | 200 | unsure | 0.594 | 0.424 | 0.526 | **BROKE** |
| PI04 | prompt_injection | 200 | unsure | 0.500 | 0.389 | 0.456 | **HELD** |
| PI05 | prompt_injection | 200 | unsure | 0.640 | 0.163 | 0.449 | **HELD** |
| PI06 | prompt_injection | 200 | unsure | 0.558 | 0.506 | 0.537 | **HELD** |
| MF01 | malformed | 400 | — | — | — | — | **HELD** |
| MF02 | malformed | 500 | — | — | — | — | **BROKE** |
| MF03 | malformed | 200 | human | 0.000 | 0.500 | 0.200 | **BROKE** |
| MF04 | malformed | 200 | human | 0.011 | 0.500 | 0.207 | **BROKE** |
| MF05 | malformed | 200 | ai | 0.998 | 0.500 | 0.799 | **BROKE** |
| MF06 | malformed | 200 | ai | 0.997 | 0.500 | 0.798 | **BROKE** |
| MF07 | malformed | 200 | ai | 0.906 | 0.500 | 0.744 | **BROKE** |
| MF08 | malformed | 413 | — | — | — | — | **HELD** |
| RQ01 | malformed | 400 | — | — | — | — | **HELD** |
| RQ02 | malformed | 400 | — | — | — | — | **HELD** |
| RQ03 | malformed | 400 | — | — | — | — | **HELD** |
| RQ04 | malformed | 400 | — | — | — | — | **HELD** |
| RQ05 | malformed | 400 | — | — | — | — | **HELD** |
| RQ06 | malformed | 400 | — | — | — | — | **HELD** |
| RQ07 | malformed | 400 | — | — | — | — | **HELD** |
| RQ08 | malformed | 400 | — | — | — | — | **HELD** |
| RQ09 | malformed | 400 | — | — | — | — | **HELD** |
| RQ10 | malformed | 400 | — | — | — | — | **HELD** |
| RQ11 | malformed | 429 | — | — | — | — | **HELD** |
| RQ12 | malformed | 400 | — | — | — | — | **HELD** |
| FL01_01 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_02 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_03 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_04 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_05 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_06 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_07 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_08 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_09 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_10 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_11 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_12 | flood_same_creator | 429 | — | — | — | — | **HELD** |

(`—` in the score columns = no decision was made: a 4xx/5xx/429, or one of the flood rows, whose scores are in the log under creator `attacker_flood`.)

**Count by family:** evasion 1 held / 9 broke · false_positive 4 / 4 · prompt_injection 3 / 3 · malformed (MF) 2 / 6 · malformed requests (RQ) 12 / 0 · flood 12 / 0.

Two notes on the held count. RQ11 came back 429 because earlier malformed rows with no `creator_id` all count against my own address; that request never reached my route, so "held" there means the limiter held, not my validation. And flood rows FL01_01 to FL01_06 returned 200 and FL01_07 to FL01_12 returned 429, so the limiter cut in at the 7th request as set (6/min).

**Ten audit log entries from the run** (`GET /log`, labels shortened to fit):

```json
{"combined_score": 0.7176, "content_id": "980331cd-ed02-4ea1-8bda-176209ce9b02", "creator_id": "attacker_FP03", "guess": "ai", "label": "Our checks suggest this may have been wr…", "model_score": 0.8051, "status": "decided", "style_score": 0.5864, "timestamp": "2026-11-16T07:28:46+00:00"}
{"combined_score": 0.7879, "content_id": "7dd9a5cd-15cd-4f73-b8a3-1782fbe205e8", "creator_id": "attacker_FP05", "guess": "ai", "label": "Our checks suggest this may have been wr…", "model_score": 0.8005, "status": "decided", "style_score": 0.7689, "timestamp": "2026-11-16T07:28:46+00:00"}
{"combined_score": 0.7438, "content_id": "107d6907-5094-48b1-8dc0-6dba84c4c426", "creator_id": "attacker_MF07", "guess": "ai", "label": "Our checks suggest this may have been wr…", "model_score": 0.9064, "status": "decided", "style_score": 0.5, "timestamp": "2026-11-16T07:28:47+00:00"}
{"combined_score": 0.2192, "content_id": "29755cf0-c878-4952-bd83-2214c64bb6f4", "creator_id": "attacker_PI02", "guess": "human", "label": "We think this was probably written by a …", "model_score": 0.2044, "status": "decided", "style_score": 0.2413, "timestamp": "2026-11-16T07:28:46+00:00"}
{"combined_score": 0.3337, "content_id": "2f0fa380-2eb2-4ea1-a52a-9f0e25e8d528", "creator_id": "attacker_EV01", "guess": "human", "label": "We think this was probably written by a …", "model_score": 0.1635, "status": "decided", "style_score": 0.5889, "timestamp": "2026-11-16T07:28:45+00:00"}
{"combined_score": 0.2688, "content_id": "2fe95dd9-45f8-4431-bc00-0af1987b1ee1", "creator_id": "attacker_EV05", "guess": "human", "label": "We think this was probably written by a …", "model_score": 0.3212, "status": "decided", "style_score": 0.1901, "timestamp": "2026-11-16T07:28:45+00:00"}
{"combined_score": 0.2, "content_id": "b4f4004c-b592-442f-848f-e4c95a9b86b2", "creator_id": "attacker_MF03", "guess": "human", "label": "We think this was probably written by a …", "model_score": 0.0, "status": "decided", "style_score": 0.5, "timestamp": "2026-11-16T07:28:47+00:00"}
{"combined_score": 0.4494, "content_id": "7b37d462-029d-4666-96a1-f3c99d027993", "creator_id": "attacker_PI05", "guess": "unsure", "label": "We can't tell how this was written. Our …", "model_score": 0.6401, "status": "decided", "style_score": 0.1633, "timestamp": "2026-11-16T07:28:46+00:00"}
{"creator_id": "attacker_flood", "event": "rejected", "limit": "6 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-16T07:28:48+00:00"}
{"creator_id": "attacker_RQ05", "event": "rejected", "reason": "missing_text", "status": "rejected", "timestamp": "2026-11-16T07:28:47+00:00"}
```

**What the log does not show.** MF02 (a one-character text) returned a 500 and left **no entry at all**: the route crashed in `detector.py` ("Text is too short to score") before it reached `audit.log_decision`, and nothing catches the error. That is a crash and a gap in my log in one.

**The single worst outcome:** FP03, "a non-native English speaker writing carefully". A person describing their first month in a new country, in simple, careful sentences, was told "Our checks suggest this may have been written with an AI tool" (combined 0.718, model 0.805, style 0.586). It is the false accusation my criterion 1 exists to prevent, and it lands on someone who may already feel scrutinised for how they write. FP05 (technical documentation, 0.788) was scored even higher, but FP03 is the one I would least want to explain to the writer. (Diagnosis is in the next sections.)

---

## Run Log and Verdicts

`python run_eval.py --label before` then `python check_criteria.py --label before` (three trials each, nothing changed in between). Scenarios are in `scenarios.py`: ten pieces I wrote myself, five AI-written texts, five borderline texts (the last two sets written by Claude for this test, and the "clearly human" set for criterion 2 reuses five of my own pieces, so criteria 1 and 2 are not independent), and the bad-input bodies. Raw files: `results/run_2026-11-16_2106_before.md/.json`, `results/criteria_before.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | 0 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. Clearly-AI vs clearly-human mean gap | >= 0.30 | 0.483 | 0.483 | 0.483 | MET |
| 3. All 3 labels reachable; borderline text lands in unsure | 3/3 labels and >= 3 of 5 unsure | 3/3, 4/5 | 3/3, 4/5 | 3/3, 4/5 | MET |
| 4. Every valid appeal sets under_review and is logged | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 5. Bad input never 500s, each rejection logged | 7 of 7 inputs, 0 x 500 | 7/7 | 7/7 | 7/7 | MET |

The three trials were identical to the last digit, which is what a deterministic pipeline should do (GPT-2 and the style measures have no randomness). So the repeats show the result is stable, not that it was a lucky pass.

**Real output from trial 1** (`run_eval.py` / `check_criteria.py`, produced by `app.py::submit` and `app.py::appeal`):

Criterion 1, ten of my pieces (labels omitted for length; `scoring.py::score_to_label` produced the guess):

```json
[{"status":200,"guess":"unsure","confidence":0.0308,"model_score":0.72,"style_score":0.1315,"combined_score":0.4846},
 {"status":200,"guess":"unsure","confidence":0.1018,"model_score":0.6521,"style_score":0.1446,"combined_score":0.4491},
 {"status":200,"guess":"unsure","confidence":0.0086,"model_score":0.6908,"style_score":0.203,"combined_score":0.4957},
 {"status":200,"guess":"human","confidence":0.4958,"model_score":0.3145,"style_score":0.1584,"combined_score":0.2521},
 {"status":200,"guess":"human","confidence":0.5938,"model_score":0.1763,"style_score":0.2432,"combined_score":0.2031},
 {"status":200,"guess":"human","confidence":0.9022,"model_score":0.0815,"style_score":0.0,"combined_score":0.0489},
 {"status":200,"guess":"unsure","confidence":0.2332,"model_score":0.4232,"style_score":0.3236,"combined_score":0.3834},
 {"status":200,"guess":"human","confidence":0.4346,"model_score":0.3567,"style_score":0.1718,"combined_score":0.2827},
 {"status":200,"guess":"human","confidence":0.3438,"model_score":0.2715,"style_score":0.4131,"combined_score":0.3281},
 {"status":200,"guess":"human","confidence":0.3192,"model_score":0.1467,"style_score":0.631,"combined_score":0.3404}]
```

Criterion 2 (`scoring.py::combine_signals` scores):

```json
{
 "mean_combined_clearly_AI": 0.7283,
 "mean_combined_clearly_human": 0.2456,
 "gap": 0.4827
}
```

Criterion 3 (`scoring.py::score_to_label`):

```json
{"labels_seen_across_run": ["ai", "human", "unsure"], "borderline_guesses": ["unsure", "unsure", "unsure", "unsure", "ai"], "borderline_combined": [0.559, 0.679, 0.5, 0.696, 0.763]}
```

Criterion 4 (`app.py::appeal` plus `GET /log`):

```json
{"valid_appeals_ok": 10, "unknown_id_returns_404_and_no_log_entry": true}
```

Criterion 5 (`app.py::submit` validation; the 7th input is a non-JSON body; 413 is the 50,000-character cap):

```json
{"statuses_for_7_bad_inputs": [400, 400, 400, 400, 400, 413, 400], "rejected_entries_logged": 7, "ping_after": true}
```

**How I decided each verdict.** I applied the targets exactly as written and required them to hold in every trial. Criterion 1 needed 0 flags in all three trials: 0, 0, 0. Criterion 3 needed both conditions: all three labels appeared, and 4 of 5 borderline pieces were "unsure" against a target of 3. Criterion 4 counted an appeal only if the response said `under_review` **and** a matching `appeal` entry with the reasoning appeared in the log, and the unknown id returned 404 and wrote nothing. Criterion 5 needed every input to return 4xx with a `rejected` log entry.

**An honest look at "all MET".** A clean sweep on my own criteria sits next to 22 broken attacks, and I don't think my service is that good. The criteria were too narrow, and the attack set found what they didn't:

- **Criterion 1** passed because my ten pieces are casual: seven are fragments, notes or chat-style messages. The attack set's plain and formal human writing (FP02 to FP05) got labeled AI four times out of eight. My own writing is the wrong place to look for the failure, and I should have included a few plain assignment-style paragraphs. This is the one I would tighten.
- **Criterion 5** passed because the seven inputs I listed don't include a one-character text. MF02 crashed the route with a 500 and left no log entry, and criterion 5 as written could never have caught it. That is a gap in what I chose to list, not an unmeasurable criterion, so I am not revising the wording; I would add short and non-prose inputs to the test.
- **Criterion 2** is inflated by using my casual notes as the "clearly human" side. The 0.483 gap would shrink if the human side included plain, formal prose.
- **Criterion 3**'s "borderline" texts were written by Claude, and one of five (0.763) was labeled AI.

I did not edit `criteria.md`. The targets were not unmeasurable; they were met.

**Diagnoses.** Each of the 22 broken attacks, with stage and mechanism. For the evasion cases I also scored the unedited paragraph the attack set is built on, with my own functions (not through the service): **model 0.754, style 0.250, combined 0.552, which is "unsure" before any edit.**

| Attacks | Stage | Mechanism |
|---|---|---|
| EV01, EV05 | Signal one | Typos and a heavy editing pass add rare, odd tokens, which GPT-2 finds unpredictable, so perplexity rises and `model_score` collapses (0.754 to 0.164 and 0.321). The style signal barely moved on EV01 (0.589). |
| EV02, EV03, EV04, EV06, EV07, EV09 | Signal two and the combining rule | These land at 0.44 to 0.59, within about 0.1 of the **unedited** 0.552, so the edits did little. The paragraph was already not caught: its long, varied sentences give `style_score` 0.25, which reads as human, and my rule treats any style score under 0.5 as a veto on an AI verdict (the cap in `scoring.py::combine_signals`) while weighting style 0.4. The style signal's wrong assumption (varied sentence length means human) is the cause. |
| EV08 | Signal one | A ten-word text is below the signal's useful size; GPT-2's perplexity on so few tokens is noise (0.245). |
| PI01, PI02, PI03 | Signal one and signal two | Nothing in my pipeline reads instructions, so these were not obeyed. The injected lines ("Ignore all previous instructions.", "SYSTEM: ...") are short, abrupt sentences and odd tokens in front of the paragraph. They change its shape (sentence length spread) and raise perplexity, moving combined from 0.552 to 0.39, 0.22 and 0.53. It looks like injection working, but the mechanism is only text statistics. |
| FP02, FP03, FP04, FP05 | Signal one, then the combining rule and the threshold | Plain, formal, careful or technical writing is highly predictable, so `model_score` is 0.74 to 0.83. The style signal agrees (0.57 to 0.77) because those texts have even sentences, so both signals lean AI and my "both must agree" cap, built for disagreement, does nothing. Combined 0.718 to 0.788 clears the 0.70 AI threshold. |
| MF02 | Route | `detector.py` raises `ValueError("Text is too short to score")` and `app.py::submit` has no input check or try/except for it, so it surfaces as a 500, and the crash happens before `audit.log_decision`, so the log has no entry for it. |
| MF03, MF04 | Route (no input validation), signal one | Control characters and punctuation-only text are not prose. Signal one returns about 0.0 on them (junk is unpredictable), signal two returns its neutral 0.5 for "nothing to measure", and combined 0.20 becomes "human". |
| MF05, MF06, MF07 | Route (no input validation), signal one, combining rule | A long single word, emoji and right-to-left text give signal one 0.91 to 0.998 (very repetitive or byte-level tokens), while signal two says a neutral 0.5. The neutral 0.5 still gets 40% weight and is not treated as "I can't tell", so combined is 0.74 to 0.80 and clears the AI threshold. It also labels a real right-to-left writer "AI", which is the worst version of this. |

**Patterns.** Four underlying problems, not 22:
1. **Signal one over-reads predictability.** Plain human text and junk repeats both look machine-written to it (FP02 to FP05, MF05 to MF07), and token-level noise makes AI text look human (EV01, EV05, EV08).
2. **Signal two is weak and I made it a veto.** It scores an ordinary AI paragraph 0.25, and my combining rule lets it block an AI verdict on its own. It also returns 0.5 for "can't measure", which the rule counts as an opinion.
3. **No input validation in the route** (MF02 to MF07: six attacks, including the only crash).
4. **The 0.70 threshold is crossed by plain human writing** (0.72 to 0.79) while real AI text sits only slightly higher (0.69 to 0.79 in my own AI set), so no threshold separates them well.

The safeguard did work once: FP06 and FP07 (model 0.88, style 0.496) would have averaged 0.727, but the "both must agree" cap held them to 0.69, "unsure". The false positive for FP02 to FP05 is the case the cap can't catch.

---

## The Improvement

**What I changed:** one thing, validating input in the route (`app.py::submit`, setting `MIN_WORDS = 5` in `config.py`). Text with fewer than 5 words in the Latin alphabet is refused with `400 text_too_short` and a `rejected` log entry, before either signal sees it. Nothing else changed: no weights, thresholds, labels or signals.

**Which diagnosis pointed at it:** pattern 3, no input validation in the route. MF02 crashed `detector.py` with a `ValueError` and a 500 (with no log entry), and MF03 to MF07 got confident labels on text that isn't prose (control characters, punctuation, one long word, emoji, right-to-left script), because both signals returned something and neither was told to refuse. All six had one cause, in the route, so one fix at the route could be measured cleanly. I picked it over a threshold move because I checked the alternative first and rejected it: moving the AI threshold from 0.70 to 0.80 would clear the four false positives, but my own five "clearly AI" texts score 0.69 to 0.79, so all five would become "unsure" and the service would stop detecting anything.

### Attack Run: After

`python run_attacks.py --set attack_set --label after` (`results/attack_run_2026-11-16_2110_after.md`), marked with the same rules as before. **56 attacks: 16 BROKE, 40 HELD (before: 22 / 34).**

| ID | Family | Status | Guess | model | style | combined | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | 200 | human | 0.164 | 0.589 | 0.334 | **BROKE** |
| EV02 | evasion | 200 | unsure | 0.594 | 0.208 | 0.440 | **BROKE** |
| EV03 | evasion | 200 | unsure | 0.666 | 0.277 | 0.510 | **BROKE** |
| EV04 | evasion | 200 | unsure | 0.611 | 0.566 | 0.593 | **BROKE** |
| EV05 | evasion | 200 | human | 0.321 | 0.190 | 0.269 | **BROKE** |
| EV06 | evasion | 200 | unsure | 0.573 | 0.283 | 0.457 | **BROKE** |
| EV07 | evasion | 200 | unsure | 0.586 | 0.303 | 0.473 | **BROKE** |
| EV08 | evasion | 200 | unsure | 0.245 | 0.548 | 0.366 | **BROKE** |
| EV09 | evasion | 200 | unsure | 0.704 | 0.361 | 0.567 | **BROKE** |
| EV10 | evasion | 200 | ai | 0.979 | 0.719 | 0.875 | **HELD** |
| FP01 | false_positive | 200 | unsure | 0.618 | 0.501 | 0.571 | **HELD** |
| FP02 | false_positive | 200 | ai | 0.739 | 0.695 | 0.721 | **BROKE** |
| FP03 | false_positive | 200 | ai | 0.805 | 0.586 | 0.718 | **BROKE** |
| FP04 | false_positive | 200 | ai | 0.833 | 0.571 | 0.728 | **BROKE** |
| FP05 | false_positive | 200 | ai | 0.800 | 0.769 | 0.788 | **BROKE** |
| FP06 | false_positive | 200 | unsure | 0.881 | 0.496 | 0.690 | **HELD** |
| FP07 | false_positive | 200 | unsure | 0.882 | 0.495 | 0.690 | **HELD** |
| FP08 | false_positive | 200 | unsure | 0.322 | 0.441 | 0.370 | **HELD** |
| PI01 | prompt_injection | 200 | unsure | 0.463 | 0.277 | 0.388 | **BROKE** |
| PI02 | prompt_injection | 200 | human | 0.204 | 0.241 | 0.219 | **BROKE** |
| PI03 | prompt_injection | 200 | unsure | 0.594 | 0.424 | 0.526 | **BROKE** |
| PI04 | prompt_injection | 200 | unsure | 0.500 | 0.389 | 0.456 | **HELD** |
| PI05 | prompt_injection | 200 | unsure | 0.640 | 0.163 | 0.449 | **HELD** |
| PI06 | prompt_injection | 200 | unsure | 0.558 | 0.506 | 0.537 | **HELD** |
| MF01 | malformed | 400 | — | — | — | — | **HELD** |
| MF02 | malformed | 400 | — | — | — | — | **HELD** |
| MF03 | malformed | 400 | — | — | — | — | **HELD** |
| MF04 | malformed | 400 | — | — | — | — | **HELD** |
| MF05 | malformed | 400 | — | — | — | — | **HELD** |
| MF06 | malformed | 400 | — | — | — | — | **HELD** |
| MF07 | malformed | 400 | — | — | — | — | **HELD** |
| MF08 | malformed | 413 | — | — | — | — | **HELD** |
| RQ01 | malformed | 400 | — | — | — | — | **HELD** |
| RQ02 | malformed | 400 | — | — | — | — | **HELD** |
| RQ03 | malformed | 400 | — | — | — | — | **HELD** |
| RQ04 | malformed | 400 | — | — | — | — | **HELD** |
| RQ05 | malformed | 400 | — | — | — | — | **HELD** |
| RQ06 | malformed | 400 | — | — | — | — | **HELD** |
| RQ07 | malformed | 400 | — | — | — | — | **HELD** |
| RQ08 | malformed | 400 | — | — | — | — | **HELD** |
| RQ09 | malformed | 400 | — | — | — | — | **HELD** |
| RQ10 | malformed | 400 | — | — | — | — | **HELD** |
| RQ11 | malformed | 429 | — | — | — | — | **HELD** |
| RQ12 | malformed | 400 | — | — | — | — | **HELD** |
| FL01_01 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_02 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_03 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_04 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_05 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_06 | flood_same_creator | 200 | human | — | — | — | **HELD** |
| FL01_07 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_08 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_09 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_10 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_11 | flood_same_creator | 429 | — | — | — | — | **HELD** |
| FL01_12 | flood_same_creator | 429 | — | — | — | — | **HELD** |

Exactly six rows changed and nothing else moved, which is what makes the comparison clean:

| Attack | Before (status / guess) | After |
|---|---|---|
| MF02 | 500 / — (BROKE) | 400 / text_too_short (HELD) |
| MF03 | 200 / human (BROKE) | 400 / text_too_short (HELD) |
| MF04 | 200 / human (BROKE) | 400 / text_too_short (HELD) |
| MF05 | 200 / ai (BROKE) | 400 / text_too_short (HELD) |
| MF06 | 200 / ai (BROKE) | 400 / text_too_short (HELD) |
| MF07 | 200 / ai (BROKE) | 400 / text_too_short (HELD) |

Side by side: broken attacks **22 to 16**. Evasion 9 broke before and after; false positives 4 before and after; prompt injection 3 before and after; malformed text 6 broke before, 0 after. The five criteria ran again with `--label after` (`results/run_2026-11-16_2111_after.md`, `results/criteria_after.md`) and came out the same as before (all MET, 0/10, gap 0.483, 4/5 borderline unsure, 10/10 appeals, 7/7 bad inputs), because none of them tests what changed.

Three of the new rejection entries from the run:

```json
{"creator_id": "attacker_MF02", "event": "rejected", "reason": "text_too_short", "status": "rejected", "timestamp": "2026-11-17T05:10:41+00:00"}
{"creator_id": "attacker_MF03", "event": "rejected", "reason": "text_too_short", "status": "rejected", "timestamp": "2026-11-17T05:10:41+00:00"}
{"creator_id": "attacker_MF04", "event": "rejected", "reason": "text_too_short", "status": "rejected", "timestamp": "2026-11-17T05:10:41+00:00"}
```

**Did it help, and how do I know:** yes for the thing it targeted. The only crash is gone and five junk inputs no longer get a confident verdict, and the 22-to-16 count is the same set of attacks with the same marking rules. It did not touch the harm I care most about: the four false accusations (FP02 to FP05) and the evasion misses are unchanged.

**What it costs:** an honest trade. Any text that isn't mostly Latin-alphabet words now gets a 400, so a writer using Arabic, Hebrew, Chinese or another script gets "we can only check English text" instead of a verdict. That is better than being labeled "AI" on a language the signals can't read (MF07 was), but it is a real limit on who the service can serve. Real text shorter than 5 words is also refused.

---

## What's Still Broken

| Still broken | What I'd do | Why I stopped |
|---|---|---|
| EV01, EV05 (typos / heavy editing move signal one) | Make signal one less sensitive to token-level noise, e.g. score on a cleaned-up copy of the text or use a bigger model than GPT-2 | Needs a new signal design; one change per unit. |
| EV02, EV03, EV04, EV06, EV07, EV09 and PI01 to PI03 (AI text not flagged, even unedited) | Rework the style signal (it scores an ordinary AI paragraph 0.25) and stop treating it as a veto in `combine_signals` | Out of scope after the validation fix. The edits aren't the root cause here, the base paragraph already scores "unsure". |
| EV08 (ten-word text, noisy perplexity) | Require a larger minimum length for a verdict, say 40 words, and answer "unsure" below it | A bigger version of the same validation idea. Would also reject FP08-style short human posts. |
| FP02, FP03, FP04, FP05 (plain, formal, non-native or technical human writing labeled AI) | Add a signal that doesn't equate predictable with AI, and test more human writing of this kind | The one I care about most, and it has no single-knob fix. Threshold to 0.80 costs all detection on my own AI set. |

**The trade I'd make if this ran for real:** I'd keep leaning toward fewer wrong accusations, because a false "AI" label lands on a person whose work is theirs, and I'd route every high-confidence AI label through a human review rather than showing it as a verdict. The cost is more AI text going through unflagged (nine of ten evasions, and two of my five AI-written texts, are not labeled "ai"), and the people who pay for that are the readers and honest writers who lose the benefit of a working check.

---

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
