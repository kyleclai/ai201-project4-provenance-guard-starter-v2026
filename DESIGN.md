# Design notes (Milestone 1)

## 1. The path a submission takes

1. **Route (`app.py::submit`)** receives JSON, validates `text` (present, a string, non-empty, within a length cap) and `creator_id`. Bad input is rejected with a 4xx JSON error and logged as a rejection. Adds: a clean `text` and `creator_id`.
2. **ID assignment** — a `content_id` (uuid) is minted. Adds: the handle the appeal endpoint needs.
3. **Signal one (`detector.py::model_signal`)** — local GPT-2 scores how predictable the text is. Adds `model_score` (0–1, higher = more AI-like).
4. **Signal two (`stylometry.py::style_signal`)** — sentence-length spread, type-token ratio, punctuation density. Adds `style_score` (0–1, higher = more AI-like).
5. **Combining rule (`scoring.py::combine_signals`)** — merges both into `combined_score`.
6. **Label mapping (`scoring.py::score_to_label`)** — thresholds in `config.py` turn the score into a `guess` (`ai`/`human`/`unsure`) and a plain-English label.
7. **Audit log (`audit.py::log_decision`)** — writes the entry (all three scores, guess, label, status `decided`) to `logs/audit.jsonl`, then the route returns the JSON to the caller.

## 2. The two signals

**Signal one — model signal (`detector.py`).** Measures perplexity: how predictable the text is to GPT-2. Language-model output tends to be high-probability text, so it is more predictable than a person's. *Cannot see:* anything about meaning, facts or authorship. Plain, conventional or formulaic human writing is also predictable, so it reads as AI; AI text with odd word choices or edits reads as human. GPT-2 is old and small, and short texts give noisy readings.

**Signal two — style signal (`stylometry.py`).** Measures shape: how much sentence length varies, how much vocabulary repeats, how varied the punctuation is. Generated prose tends to have even, mid-length sentences and a narrower vocabulary; people write lumpier. *Cannot see:* meaning at all. Anything that changes the shape without changing the substance moves it: typos, chopped-up sentences, pasted quotations, or a human who simply writes in even sentences. Short texts have almost no spread to measure.

## 3. Tracing the false positive

A real writer submits a plain, conventional essay they wrote themselves. GPT-2 finds it predictable (`model_score` ≈ 0.8) and their sentences are even (`style_score` ≈ 0.7). Combined ≈ 0.75, above the AI threshold, so they'd see the "high-confidence AI" label. What they can do: `POST /appeal` with their reasoning. The item goes to `under_review` and the appeal is logged beside the original decision. That is why the AI threshold must be high, why the unsure band must be wide, and why the AI label wording must stay measured rather than accusatory: the label must never state certainty the system doesn't have.

## 4. Endpoint contracts

### `POST /submit`
In: `{"text": string (non-empty, ≤ 50,000 chars), "creator_id": string (non-empty)}`

Out (200): `{"content_id": string, "guess": "ai"|"human"|"unsure", "confidence": float 0–1, "label": string, "model_score": float, "style_score": float, "combined_score": float, "status": "decided"}`

Errors: 400 `{"error": "<code>", "message": "..."}` for missing/non-string/empty fields or non-JSON body; 413 for text over the cap.

`confidence` = how sure the system is of its `guess` (distance from the middle: 0 when the combined score is 0.5, rising to 1 at either end). `combined_score` is the raw AI-likelihood.

### `POST /appeal`
In: `{"content_id": string, "reasoning": string (non-empty)}`

Out (200): `{"content_id": string, "status": "under_review", "message": "..."}`

Errors: 400 for missing fields, 404 `{"error": "unknown_content_id"}` if the id was never logged.
