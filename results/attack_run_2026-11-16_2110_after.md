# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 21:10
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `241fe1cd-7edc-46b6-8849-42333bbf869f` | human | 0.333 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `4ae38a0d-6dff-46d0-84e9-ddb06f970c8a` | unsure | 0.121 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `67c3e075-f3c1-4546-b329-a0adb3eec16b` | unsure | 0.021 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `95e98d9c-ce61-44e4-84d8-2ad92c887077` | unsure | 0.186 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `da09b718-8b24-4f43-a95b-defc19ca6fe7` | human | 0.462 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c4bc4095-6921-4a59-b69a-c468d45af358` | unsure | 0.086 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `ddd4af5e-2501-4565-9a34-e87407ec02d7` | unsure | 0.054 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `cf14d31d-7b22-41ba-9c64-5b15983808fa` | unsure | 0.267 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `da65e957-ab37-4931-b514-f02842637ae9` | unsure | 0.134 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `25b34bad-74a1-4207-87d2-c50c22641d77` | ai | 0.750 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `3c43604c-dfa0-4ab9-9350-0cd7468d7765` | unsure | 0.142 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `68d28007-110b-4ed1-a0ea-383f41088ae2` | ai | 0.442 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `116719eb-1336-45c1-a811-90b41daf19d3` | ai | 0.435 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d7c39ac5-a713-40c1-9dca-f99f66aaede0` | ai | 0.457 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `a60c1694-d0fb-4d86-9176-536c770ac1df` | ai | 0.576 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `46ac11a2-0795-4d86-9a4e-b1f3c99ade3d` | unsure | 0.380 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `ca5ad2a0-de50-4e30-9650-c70026f2864e` | unsure | 0.380 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `1db43c28-7dc1-44c7-97b5-afca52349570` | unsure | 0.261 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `80a9eec9-21cf-4985-b15b-a5e957ede994` | unsure | 0.224 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `cd6f7f7b-7b0f-40ec-ba79-0d0ea694818b` | human | 0.562 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `eed09a6b-eb51-4437-8ac3-8cf7085fd096` | unsure | 0.053 | BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `16ffd635-d587-4a6b-b3f8-f69468f6e464` | unsure | 0.089 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `10418ae7-fe8c-4596-b512-c02c45fe17af` | unsure | 0.101 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `aa1f7011-4e4b-45dd-a1c6-1414deb61518` | unsure | 0.074 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — | HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9709c18c-c7e1-46b7-979f-99ed0e99bf14` | human | 0.566 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f973df32-7fe6-4cb7-b52c-faa3f0efd570` | human | 0.566 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `843e4989-f041-4cd3-a2ed-1e201a0a17ea` | human | 0.566 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bb1fa67d-2a48-4fc8-9467-1a14c4e421da` | human | 0.566 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f54fbd8f-0989-4c42-aacf-c2a747275e2e` | human | 0.566 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a9cc25ae-629d-422f-8bb8-571de290f661` | human | 0.566 | HELD |
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
| `malformed` | 20 | 0 | 20 |
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
  "content_id": "241fe1cd-7edc-46b6-8849-42333bbf869f",
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
  "content_id": "4ae38a0d-6dff-46d0-84e9-ddb06f970c8a",
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
  "content_id": "67c3e075-f3c1-4546-b329-a0adb3eec16b",
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
  "content_id": "95e98d9c-ce61-44e4-84d8-2ad92c887077",
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
  "content_id": "da09b718-8b24-4f43-a95b-defc19ca6fe7",
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
  "content_id": "c4bc4095-6921-4a59-b69a-c468d45af358",
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
  "content_id": "ddd4af5e-2501-4565-9a34-e87407ec02d7",
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
  "content_id": "cf14d31d-7b22-41ba-9c64-5b15983808fa",
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
  "content_id": "da65e957-ab37-4931-b514-f02842637ae9",
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
  "content_id": "25b34bad-74a1-4207-87d2-c50c22641d77",
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
  "content_id": "3c43604c-dfa0-4ab9-9350-0cd7468d7765",
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
  "content_id": "68d28007-110b-4ed1-a0ea-383f41088ae2",
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
  "content_id": "116719eb-1336-45c1-a811-90b41daf19d3",
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
  "content_id": "d7c39ac5-a713-40c1-9dca-f99f66aaede0",
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
  "content_id": "a60c1694-d0fb-4d86-9176-536c770ac1df",
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
  "content_id": "46ac11a2-0795-4d86-9a4e-b1f3c99ade3d",
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
  "content_id": "ca5ad2a0-de50-4e30-9650-c70026f2864e",
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
  "content_id": "1db43c28-7dc1-44c7-97b5-afca52349570",
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
  "content_id": "80a9eec9-21cf-4985-b15b-a5e957ede994",
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
  "content_id": "cd6f7f7b-7b0f-40ec-ba79-0d0ea694818b",
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
  "content_id": "eed09a6b-eb51-4437-8ac3-8cf7085fd096",
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
  "content_id": "16ffd635-d587-4a6b-b3f8-f69468f6e464",
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
  "content_id": "10418ae7-fe8c-4596-b512-c02c45fe17af",
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
  "content_id": "aa1f7011-4e4b-45dd-a1c6-1414deb61518",
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
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
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
  "content_id": "9709c18c-c7e1-46b7-979f-99ed0e99bf14",
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
  "content_id": "f973df32-7fe6-4cb7-b52c-faa3f0efd570",
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
  "content_id": "843e4989-f041-4cd3-a2ed-1e201a0a17ea",
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
  "content_id": "bb1fa67d-2a48-4fc8-9467-1a14c4e421da",
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
  "content_id": "f54fbd8f-0989-4c42-aacf-c2a747275e2e",
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
  "content_id": "a9cc25ae-629d-422f-8bb8-571de290f661",
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
