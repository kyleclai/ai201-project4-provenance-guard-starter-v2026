# Criteria check: after

Scenario run: `run_2026-11-16_2111_after.json`  
Produced by `check_criteria.py` (criteria 1-3 from the run_eval JSON; 4 and 5 live).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | 0 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. Clearly-AI vs clearly-human mean gap | >= 0.30 | 0.483 | 0.483 | 0.483 | MET |
| 3. All 3 labels reachable; borderline -> unsure | 3/3 labels, >= 3/5 unsure | 3/3, 4/5 | 3/3, 4/5 | 3/3, 4/5 | MET |
| 4. Valid appeals set under_review + logged; unknown id 404 | 10 of 10 | 10/10, 404 ok | 10/10, 404 ok | 10/10, 404 ok | MET |
| 5. Bad input: 4xx not 500, logged, /ping up | 7 of 7, 0 x 500 | 7/7 4xx, 7 logged, ping ok | 7/7 4xx, 7 logged, ping ok | 7/7 4xx, 7 logged, ping ok | MET |

## Raw

```json
[
 {
  "c1": 0,
  "c2": 0.4827199999999999,
  "c3_labels": 3,
  "c3_unsure": 4,
  "c4": 10,
  "c4_unknown_404": true,
  "c5_statuses": [
   400,
   400,
   400,
   400,
   429,
   413,
   429
  ],
  "c5_4xx": 7,
  "c5_logged": 7,
  "ping": true
 },
 {
  "c1": 0,
  "c2": 0.4827199999999999,
  "c3_labels": 3,
  "c3_unsure": 4,
  "c4": 10,
  "c4_unknown_404": true,
  "c5_statuses": [
   400,
   400,
   400,
   400,
   400,
   413,
   400
  ],
  "c5_4xx": 7,
  "c5_logged": 7,
  "ping": true
 },
 {
  "c1": 0,
  "c2": 0.4827199999999999,
  "c3_labels": 3,
  "c3_unsure": 4,
  "c4": 10,
  "c4_unknown_404": true,
  "c5_statuses": [
   400,
   400,
   400,
   400,
   400,
   413,
   400
  ],
  "c5_4xx": 7,
  "c5_logged": 7,
  "ping": true
 }
]
```
