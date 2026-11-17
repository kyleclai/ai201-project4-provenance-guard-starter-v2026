#!/usr/bin/env python3
"""
Score my five criteria (criteria.md) over three trials.  (Unit 8, M3/M5)

    python app.py                                   # terminal 1
    python run_eval.py --label before               # sends scenarios.py x3
    python check_criteria.py --label before         # scores 1-3, runs 4 and 5

Criteria 1-3 are scored from the run_eval JSON for the label. Criteria 4
(appeals) and 5 (bad input + log) need live requests and the log, so this
script makes them itself, once per trial. It waits 61 s between trials so the
per-address rate limit (6/min) can't turn a 400 into a 429 and blur criterion 5.
This is test harness only; it does not touch the service.
"""
import argparse
import json
import sys
import time
import uuid
from pathlib import Path

import requests

import config
import scenarios

URL = f"http://{config.HOST}:{config.PORT}"
H = {"Content-Type": "application/json"}


def latest_eval(label):
    files = sorted(config.RESULTS_DIR.glob(f"run_*_{label}.json"))
    if not files:
        sys.exit(f"No results/run_*_{label}.json. Run: python run_eval.py --label {label}")
    return json.loads(files[-1].read_text()), files[-1]


def by_name(data, prefix):
    return next(s for s in data if s["name"].startswith(prefix))


def crit_1_2_3(data, t):
    mine = by_name(data, "my own")["trials"][t]
    ai = by_name(data, "clearly AI")["trials"][t]
    hu = by_name(data, "clearly human")["trials"][t]
    bl = by_name(data, "borderline")["trials"][t]
    flagged = sum(r.get("guess") == "ai" for r in mine)
    gap = (sum(r["combined_score"] for r in ai) / len(ai)
           - sum(r["combined_score"] for r in hu) / len(hu))
    seen = {r.get("guess") for s in data if s["criterion"] in (1, 2, 3)
            for r in s["trials"][t]}
    labels = len(seen & {"ai", "human", "unsure"})
    unsure = sum(r.get("guess") == "unsure" for r in bl)
    return flagged, gap, labels, unsure


def crit_4():
    """10 valid appeals; plus an unknown id that must 404 and write nothing."""
    ok = 0
    ids = []
    for i in range(10):
        r = requests.post(f"{URL}/submit", headers=H, json={
            "text": "I went to the market this morning and bought some apples. "
                    "The weather was cold but dry, so I walked home slowly.",
            "creator_id": f"eval_appeal_{uuid.uuid4().hex[:8]}"})
        ids.append(r.json()["content_id"])
    for cid in ids:
        a = requests.post(f"{URL}/appeal", headers=H,
                          json={"content_id": cid, "reasoning": "I wrote this."})
        entries = requests.get(f"{URL}/log").json()["entries"]
        logged = any(e.get("content_id") == cid and e.get("event") == "appeal"
                     and e.get("status") == "under_review"
                     and e.get("reasoning") == "I wrote this." for e in entries)
        if a.status_code == 200 and a.json().get("status") == "under_review" and logged:
            ok += 1
    bad = requests.post(f"{URL}/appeal", headers=H,
                        json={"content_id": "no-such-id", "reasoning": "x"})
    entries = requests.get(f"{URL}/log").json()["entries"]
    unknown_ok = bad.status_code == 404 and not any(
        e.get("content_id") == "no-such-id" for e in entries)
    return ok, unknown_ok


def crit_5():
    """Seven bad inputs: no 500s, and each leaves a rejected entry."""
    bodies = [dict(b) for b in next(s for s in scenarios.SCENARIOS
                                    if s["criterion"] == 5)["bodies"]]
    before = len(requests.get(f"{URL}/log").json()["entries"])
    statuses = []
    for b in bodies:
        statuses.append(requests.post(f"{URL}/submit", headers=H, json=b).status_code)
    statuses.append(requests.post(f"{URL}/submit", headers=H, data="not json").status_code)
    entries = requests.get(f"{URL}/log").json()["entries"][before:]
    rejected = sum(e.get("event") == "rejected" for e in entries)
    pinged = requests.post(f"{URL}/ping", headers=H, json={"message": "x"}).status_code == 200
    no500 = sum(s < 500 and s >= 400 for s in statuses)
    return statuses, no500, rejected, pinged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--wait", type=int, default=61)
    args = ap.parse_args()
    data, src = latest_eval(args.label)

    runs = []
    for t in range(3):
        if t:
            time.sleep(args.wait)
        f, gap, labels, unsure = crit_1_2_3(data, t)
        ok4, unk = crit_4()
        st, n4xx, rej, ping = crit_5()
        runs.append(dict(c1=f, c2=gap, c3_labels=labels, c3_unsure=unsure,
                         c4=ok4, c4_unknown_404=unk, c5_statuses=st,
                         c5_4xx=n4xx, c5_logged=rej, ping=ping))
        print(f"trial {t+1}: {runs[-1]}", flush=True)

    def row(n, name, target, cells, verdict):
        return f"| {n}. {name} | {target} | " + " | ".join(cells) + f" | {verdict} |"

    r = runs
    lines = [f"# Criteria check: {args.label}", "", f"Scenario run: `{src.name}`  ",
             f"Produced by `check_criteria.py` (criteria 1-3 from the run_eval JSON;"
             f" 4 and 5 live).", "",
             "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |", "|---|---|---|---|---|---|",
             row(1, "My own writing flagged as AI", "0 of 10",
                 [f"{x['c1']}/10" for x in r], "MET" if all(x['c1'] == 0 for x in r) else "MISSED"),
             row(2, "Clearly-AI vs clearly-human mean gap", ">= 0.30",
                 [f"{x['c2']:.3f}" for x in r], "MET" if all(x['c2'] >= 0.30 for x in r) else "MISSED"),
             row(3, "All 3 labels reachable; borderline -> unsure", "3/3 labels, >= 3/5 unsure",
                 [f"{x['c3_labels']}/3, {x['c3_unsure']}/5" for x in r],
                 "MET" if all(x['c3_labels'] == 3 and x['c3_unsure'] >= 3 for x in r) else "MISSED"),
             row(4, "Valid appeals set under_review + logged; unknown id 404", "10 of 10",
                 [f"{x['c4']}/10, 404 {'ok' if x['c4_unknown_404'] else 'FAIL'}" for x in r],
                 "MET" if all(x['c4'] == 10 and x['c4_unknown_404'] for x in r) else "MISSED"),
             row(5, "Bad input: 4xx not 500, logged, /ping up", "7 of 7, 0 x 500",
                 [f"{x['c5_4xx']}/7 4xx, {x['c5_logged']} logged, ping {'ok' if x['ping'] else 'FAIL'}" for x in r],
                 "MET" if all(x['c5_4xx'] == 7 and x['c5_logged'] >= 7 and x['ping'] for x in r) else "MISSED"),
             "", "## Raw", "", "```json", json.dumps(runs, indent=1), "```"]
    out = config.RESULTS_DIR / f"criteria_{args.label}.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[5:12]))
    print("wrote", out)


if __name__ == "__main__":
    main()
