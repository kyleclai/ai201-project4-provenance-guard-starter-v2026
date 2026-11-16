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

- Review `criteria.md` wording and reasons; you must be able to defend each.
- Edit "What I changed" under How I Used AI, Moment 1 (placeholder comment in README).
- Push to your fork and submit the fork URL.
- 2026-11-15 — Added local-only `REFLECTION_NOTES.md` (my criteria options and picks), gitignored.
