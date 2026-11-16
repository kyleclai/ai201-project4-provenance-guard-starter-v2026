# Progress — Provenance Guard (Unit 7)

Running log of the build. Updated as each step completes.

## Checklist

- [x] Setup: venv, dependencies, `python test.py`, model download
- [x] M1: Trace the path, signals + blind spots, false-positive trace, endpoint contracts (`DESIGN.md`)
- [x] M2: `criteria.md` — five criteria (targets chosen by the student, before results)
- [ ] M3: `POST /submit` + signal one + audit log
- [ ] M4: stylometry signal, `combine_signals`, both scores logged
- [ ] M5: three labels, `POST /appeal`
- [ ] M6: README (five sections), `logs/audit.jsonl` committed, 4+ commits

## Updates

- 2026-11-15 — Read starter repo. `submit` and `appeal` return 501; `stylometry.py`, `scoring.py` are stubs. Created this file.
- 2026-11-15 — Setup done: venv, deps, `test.py` passes, GPT-2 downloaded. Sanity check of signal one: plain human sentence -> 0.15, generic AI-sounding text -> 0.82.
- 2026-11-15 — M1 written to `DESIGN.md` (path, signals + blind spots, false-positive trace, endpoint contracts).
- 2026-11-15 — M2 written to `criteria.md`. Targets chosen by you (0/10 false positives, spread >= 0.30, 10/10 appeals, no-500 bad input + logged). Please review the wording and the reasons — they must be ones you can defend.
