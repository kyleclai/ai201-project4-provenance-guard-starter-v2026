# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-15 23:28
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `2f0fa380-2eb2-4ea1-a52a-9f0e25e8d528` | human | 0.333 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `396049df-24cf-4100-9fcd-0a1416450894` | unsure | 0.121 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `cec841ce-30d0-4ab4-a2a7-8a32c06b2e4a` | unsure | 0.021 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `bf65cb43-0b98-4cfa-9afd-91d3f65a3db0` | unsure | 0.186 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `2fe95dd9-45f8-4431-bc00-0af1987b1ee1` | human | 0.462 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `0d71800c-1503-423b-89e6-51a72c1c0174` | unsure | 0.086 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `232947fc-8e44-4d2b-8916-bedc81a0038d` | unsure | 0.054 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `e2a2dc31-ecb4-461e-89a4-d307477e9dc0` | unsure | 0.267 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `877e47b5-26b5-4b8f-99ba-671437454d3d` | unsure | 0.134 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `899f61b2-655e-4313-989a-195196765b48` | ai | 0.750 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `d8c0f7c2-269d-4715-ba21-1bb3c4f31466` | unsure | 0.142 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `9fd389cf-f9c7-4f0c-8b84-d6b4f8be3d12` | ai | 0.442 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `980331cd-ed02-4ea1-8bda-176209ce9b02` | ai | 0.435 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `9cb2a048-caf2-4c70-8a1b-d7f45775acdc` | ai | 0.457 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `7dd9a5cd-15cd-4f73-b8a3-1782fbe205e8` | ai | 0.576 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `c0de7cc4-9e2b-4124-9f07-47d4a43eb2f8` | unsure | 0.380 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `07fe6c0f-bd0b-4744-9880-b1111e034805` | unsure | 0.380 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `ef8dfec8-e662-4292-afc5-8fcfef4fc035` | unsure | 0.261 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `7a66e01f-eb56-4e2f-a299-4d8e8e239a80` | unsure | 0.224 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `29755cf0-c878-4952-bd83-2214c64bb6f4` | human | 0.562 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `063f4837-dbb1-43ee-9f33-16461b16aa36` | unsure | 0.053 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `4fa3d5cb-0a7b-42b7-8401-6efb965e7970` | unsure | 0.089 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `7b37d462-029d-4666-96a1-f3c99d027993` | unsure | 0.101 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `723799e0-7eeb-40b4-bbe6-1f6389ee4c01` | unsure | 0.074 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `b4f4004c-b592-442f-848f-e4c95a9b86b2` | human | 0.600 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `f938c0fa-41b3-4fff-8052-59b93d356371` | human | 0.587 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `4b27e896-c9da-47d4-87d0-54fd42ed466c` | ai | 0.597 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `aa3514ec-f842-4c7a-b1e5-977b05cfc6ff` | ai | 0.596 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `107d6907-5094-48b1-8dc0-6dba84c4c426` | ai | 0.488 | BROKE |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d673f2b0-f3d3-423d-9ea9-bfa239e2e671` | human | 0.566 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8ef19707-2259-4e37-b974-f429d09f76ba` | human | 0.566 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ecd38dea-a92b-4550-8fd1-380322e2a074` | human | 0.566 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `39e75b37-0166-4b4c-aa96-6da9c849ceeb` | human | 0.566 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cc6d41fc-5fcc-45f2-a2d6-18a844af2b73` | human | 0.566 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `33998de9-da8f-4b83-b2d5-1aad4963a0aa` | human | 0.566 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 1 | 19 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "2f0fa380-2eb2-4ea1-a52a-9f0e25e8d528",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.3326,
  "model_score": 0.1635,
  "style_score": 0.5889,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "396049df-24cf-4100-9fcd-0a1416450894",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.1208,
  "model_score": 0.5943,
  "style_score": 0.2076,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "cec841ce-30d0-4ab4-a2a7-8a32c06b2e4a",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.0206,
  "model_score": 0.6662,
  "style_score": 0.2765,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "bf65cb43-0b98-4cfa-9afd-91d3f65a3db0",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.186,
  "model_score": 0.6114,
  "style_score": 0.5655,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "2fe95dd9-45f8-4431-bc00-0af1987b1ee1",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.4624,
  "model_score": 0.3212,
  "style_score": 0.1901,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "0d71800c-1503-423b-89e6-51a72c1c0174",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.086,
  "model_score": 0.5727,
  "style_score": 0.2834,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "232947fc-8e44-4d2b-8916-bedc81a0038d",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.054,
  "model_score": 0.5862,
  "style_score": 0.3033,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "e2a2dc31-ecb4-461e-89a4-d307477e9dc0",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.2674,
  "model_score": 0.2452,
  "style_score": 0.548,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "877e47b5-26b5-4b8f-99ba-671437454d3d",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.1338,
  "model_score": 0.7042,
  "style_score": 0.361,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "899f61b2-655e-4313-989a-195196765b48",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.75,
  "model_score": 0.9792,
  "style_score": 0.7186,
  "label": "Our checks suggest this may have been written with an AI tool. We can get this wrong. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "d8c0f7c2-269d-4715-ba21-1bb3c4f31466",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.1418,
  "model_score": 0.6175,
  "style_score": 0.501,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "9fd389cf-f9c7-4f0c-8b84-d6b4f8be3d12",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.4424,
  "model_score": 0.7387,
  "style_score": 0.695,
  "label": "Our checks suggest this may have been written with an AI tool. We can get this wrong. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "980331cd-ed02-4ea1-8bda-176209ce9b02",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.4352,
  "model_score": 0.8051,
  "style_score": 0.5864,
  "label": "Our checks suggest this may have been written with an AI tool. We can get this wrong. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "9cb2a048-caf2-4c70-8a1b-d7f45775acdc",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.4566,
  "model_score": 0.8329,
  "style_score": 0.5714,
  "label": "Our checks suggest this may have been written with an AI tool. We can get this wrong. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "7dd9a5cd-15cd-4f73-b8a3-1782fbe205e8",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.5758,
  "model_score": 0.8005,
  "style_score": 0.7689,
  "label": "Our checks suggest this may have been written with an AI tool. We can get this wrong. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c0de7cc4-9e2b-4124-9f07-47d4a43eb2f8",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.8814,
  "style_score": 0.4958,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "07fe6c0f-bd0b-4744-9880-b1111e034805",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.8816,
  "style_score": 0.4951,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "ef8dfec8-e662-4292-afc5-8fcfef4fc035",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.2606,
  "model_score": 0.3223,
  "style_score": 0.4407,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "7a66e01f-eb56-4e2f-a299-4d8e8e239a80",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.2236,
  "model_score": 0.4625,
  "style_score": 0.2767,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "29755cf0-c878-4952-bd83-2214c64bb6f4",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.5616,
  "model_score": 0.2044,
  "style_score": 0.2413,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "063f4837-dbb1-43ee-9f33-16461b16aa36",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.0526,
  "model_score": 0.5943,
  "style_score": 0.4243,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "4fa3d5cb-0a7b-42b7-8401-6efb965e7970",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.0888,
  "model_score": 0.4998,
  "style_score": 0.3894,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "7b37d462-029d-4666-96a1-f3c99d027993",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.1012,
  "model_score": 0.6401,
  "style_score": 0.1633,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "723799e0-7eeb-40b4-bbe6-1f6389ee4c01",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.0744,
  "model_score": 0.5583,
  "style_score": 0.5056,
  "label": "We can't tell how this was written. Our checks didn't point clearly either way, and that happens with plenty of writing by real people. No conclusion has been drawn about this piece.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n<title>500 Internal Server Error</title>\n<h1>Internal Server Error</h1>\n<p>The server encountered an internal error and was unable to complete your request. Either the s",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "b4f4004c-b592-442f-848f-e4c95a9b86b2",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.6,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "f938c0fa-41b3-4fff-8052-59b93d356371",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.5866,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "4b27e896-c9da-47d4-87d0-54fd42ed466c",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.5972,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "Our checks suggest this may have been written with an AI tool. We can get this wrong. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "aa3514ec-f842-4c7a-b1e5-977b05cfc6ff",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.5962,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "Our checks suggest this may have been written with an AI tool. We can get this wrong. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "107d6907-5094-48b1-8dc0-6dba84c4c426",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.4876,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "Our checks suggest this may have been written with an AI tool. We can get this wrong. If you wrote it yourself, you can appeal and a person will take a look.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "d673f2b0-f3d3-423d-9ea9-bfa239e2e671",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5656,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "8ef19707-2259-4e37-b974-f429d09f76ba",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5656,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "ecd38dea-a92b-4550-8fd1-380322e2a074",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5656,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "39e75b37-0166-4b4c-aa96-6da9c849ceeb",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5656,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "cc6d41fc-5fcc-45f2-a2d6-18a844af2b73",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5656,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "33998de9-da8f-4b83-b2d5-1aad4963a0aa",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.5656,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person. Our checks found nothing that suggests otherwise.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
