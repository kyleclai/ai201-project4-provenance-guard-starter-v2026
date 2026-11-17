# Progress — Provenance Guard (Unit 7)

Running log of the build. Updated as each step completes.

## Checklist

- [x] Setup: venv, dependencies, `python test.py`, model download
- [x] M1: Trace the path, signals + blind spots, false-positive trace, endpoint contracts (`DESIGN.md`)
- [x] M2: `criteria.md` — five criteria (targets chosen by the student, before results)
- [x] M3: `POST /submit` + signal one + audit log
- [x] M4: stylometry signal, `combine_signals`, both scores logged
- [x] M5: three labels, `POST /appeal`
- [x] M6: README (five sections), `logs/audit.jsonl` committed, 4+ commits

## Updates

- 2026-11-15 — Read starter repo. `submit` and `appeal` return 501; `stylometry.py`, `scoring.py` are stubs. Created this file.
- 2026-11-15 — Setup done: venv, deps, `test.py` passes, GPT-2 downloaded. Sanity check of signal one: plain human sentence -> 0.15, generic AI-sounding text -> 0.82.
- 2026-11-15 — M1 written to `DESIGN.md` (path, signals + blind spots, false-positive trace, endpoint contracts).
- 2026-11-15 — M2 written to `criteria.md`. Targets chosen by you (0/10 false positives, spread >= 0.30, 10/10 appeals, no-500 bad input + logged). Please review the wording and the reasons — they must be ones you can defend.
- 2026-11-15 — M3–M5 code written: `/submit` (validation, both signals, combine, label, audit log), `/appeal` (404 on unknown id), `stylometry.py` (3 measures -> `style_signal`), `scoring.py` (rule: weighted 0.6/0.4 avg, AI verdict needs both signals >= 0.5; three labels), `config.py` (AI threshold 0.70, 50k char cap). Next: test with real inputs.
- 2026-11-15 — Tested live: /submit gives all 3 labels, /appeal sets `under_review` and logs (404 on unknown id), 6 bad inputs -> 400, oversize -> 413, /ping still up.
- 2026-11-15 — Calibration finding: a plain human paragraph scored 0.78 (labeled AI) and a lightly edited AI text scored 0.35 (labeled human). Criteria/thresholds NOT changed to hide this; it's material for unit 8.
- 2026-11-15 — README filled in (five sections). `logs/audit.jsonl` (11 entries) committed.

## Still needs you

- (done) Reviewed criteria; README Moment 1 and group-discussion note filled in.
- Push to your fork and submit the fork URL.
- 2026-11-15 — Added local-only `REFLECTION_NOTES.md` (my criteria options and picks), gitignored.
- 2026-11-15 — You reviewed the criteria (kept as written) and added notes from a group discussion on requirements and AI-engineering roles; both are in the README's How I Used AI. Pushing to fork.

---

# Unit 8 — Testing

## Checklist

- [x] M1: rate limit on (6/min, 100/day), flood test, audit log has 9 fields + rejections
- [x] M2: run the attack set (before), mark held/broke, 10 log entries, worst outcome
- [x] M3: scenarios.py + `run_eval.py --label before` (5 criteria x 3 trials)
- [x] M4: verdicts + stage/mechanism diagnoses
- [ ] M5: ONE improvement, re-run attacks + eval (`--label after`)
- [ ] M6: README sections (Rate Limiting, Attack Before, Run Log, Improvement, Still Broken), How I Used AI, push

## Updates

- 2026-11-15 — Attack set is not in the repo yet; deliberately not looking for it until M2.
- 2026-11-15 — M1: enabled limiting in `config.py` (default on), 6/min + 100/day, uncommented `@limiter.limit` on `/submit`.
- 2026-11-15 — M1 verified: `--flood 15` gave `200 x6, 429 x9`; `/health` shows `rate_limiting: true`; rejections logged with reason + limit. README Rate Limiting section written. Decision entries already carry all nine fields; own-route 400s were already logged via `audit.log_rejection` in unit 7.
- 2026-11-15 — M2: attack set unpacked at `attack_set/`; ran it BEFORE any fix (`--label before`). 56 attacks: 22 BROKE / 34 HELD. Biggest clusters: evasion 9/10 not flagged, 4/8 false positives called AI (FP02-05), MF02 single char = 500 crash with no log entry, junk text (MF03-07) given confident verdicts. Worst outcome: FP03 (non-native speaker, 0.718 'ai'). Verdicts written into the results file; 10 log entries + definitions of held/broke in README. Diagnosis deferred to M4.
- 2026-11-16 — M3: wrote `scenarios.py` (your 10 pieces, names/city redacted for the public repo; 5 AI + 5 borderline written by Claude; bad-input bodies), `check_criteria.py` (criteria 4+5 live), small harness tweak in `run_eval.py` (records combined_score, JSON copy). `run_eval --label before` + `check_criteria --label before`: all 5 criteria MET, 3 identical trials.
- 2026-11-16 — M4: verdicts all MET, but criteria were too narrow (my pieces are casual; criterion 5 omitted a 1-char input). Diagnosed all 22 broken attacks into 4 patterns: signal one over-reads predictability; signal two weak + used as a veto; no input validation; threshold 0.70 crossed by plain human text. Key finding: the unedited AI paragraph already scores 0.552 (unsure), so most 'evasions' were pre-existing misses. criteria.md NOT edited.
