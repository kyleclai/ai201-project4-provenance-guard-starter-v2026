# Acceptance criteria — Provenance Guard

Written in unit 7 before any results existed. Each names a target; each has a reason.

---
## 1. No human writing is called high-confidence AI

Of 10 pieces I wrote myself (plain, everyday prose, 80+ words each), **0 of 10** get the high-confidence AI label (guess `ai`), and this holds in each of 3 repeated trials.

**Why this target:** On a writing site, accusing a real writer costs that person far more than missing an AI text costs the site. I'd rather the system say "unsure" about a human than say "AI". Zero is strict and I may miss it, but a target that tolerates accusing 1 in 10 real writers is one I wouldn't want applied to my own work.

---
## 2. Clearly-AI and clearly-human text score apart

The mean `combined_score` of 5 clearly-AI texts is **at least 0.30 higher** than the mean `combined_score` of 5 clearly-human texts.

**Why this target:** A confidence score that doesn't move between obvious cases isn't confidence. 0.30 is a modest bar I think two imperfect signals can clear, but it is large enough to span at least one threshold boundary.

---
## 3. All three labels are reachable

I can submit real text that produces each of the 3 labels (high-confidence human, unsure, high-confidence AI) through `POST /submit`, and of 5 pieces I judge borderline, **at least 3 land in "unsure"**.

**Why this target:** A label that can't be reached is a gap in the threshold ranges. "Unsure" is the label that protects writers, so it has to happen on genuinely ambiguous text, not just exist in the code.

---
## 4. Every valid appeal changes status and is recorded

For 10 of 10 appeals sent with a valid `content_id`, the response returns status `under_review` and `GET /log` shows an `appeal` entry with the reasoning next to the original decision. An unknown `content_id` returns 404 and writes nothing as an appeal.

**Why this target:** The appeal is the only recourse a wrongly-labeled writer has, so it has no acceptable failure rate. It must be 10 of 10.

---
## 5. Bad input never crashes the service

For each of these inputs — missing `text`, empty `text`, whitespace-only `text`, non-string `text`, missing `creator_id`, a non-JSON body, and `text` over 50,000 characters — `POST /submit` returns a 4xx JSON error (**0 responses with status 500**), and each rejection leaves a `rejected` entry in `logs/audit.jsonl`. `/ping` still answers afterwards.

**Why this target:** A crash on malformed input is one of the most common real failures, and a rejection that leaves no log trace is an attack I could never see later.
