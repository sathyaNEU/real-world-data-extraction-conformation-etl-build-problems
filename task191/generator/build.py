"""Build target/ from the world, read it the golden way into figures.json, and write metadata.json.

    python3 task191/generator/build.py
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A    # noqa: E402
import common as C      # noqa: E402
import pack as Pk       # noqa: E402
import world as Wd      # noqa: E402

LADDER = [
    ("R0 productivity over the decided alerts (the conversion an MI pack shows)", "decided_only", {}),
    ("R1 SARs so far over every alert, the undecided read as not ending in a SAR", "open_as_no", {}),
    ("R2 the undecided projected at the scenario's decided share", "project_decided_share", {}),
    ("R3 undecided investigations at the scenario's investigation SAR share", "status", {}),
    ("R4 each undecided alert read by how the scenario's alerts undecided at that age ended (golden)", "golden", {}),
]
FAMILY = [
    ("history from 300 days old", "golden", {"min_age": 300}),
    ("history from 365 days old", "golden", {"min_age": 365}),
    ("business date read from the Eastern clock", "golden", {"by": "eastern"}),
    ("the re-run duplicates kept", "golden", {"dups": True}),
    ("mature cohorts, 6 months", "mature", {"months": 6}),
    ("mature cohorts, 7 months", "mature", {"months": 7}),
    ("mature cohorts, 8 months", "mature", {"months": 8}),
    ("mature cohorts, 9 months", "mature", {"months": 9}),
]


def figures(P, W):
    call, prod = P.call("golden")
    tr, n, s = Wd.truth(W)
    fig = {"call": {"tuning": call, "stay": sorted(c for c in C.CODES if c not in call)},
           "productivity": {c: round(prod[c], 3) for c in C.CODES},
           "truth": {c: round(tr[c], 3) for c in C.CODES},
           "counts": {c: P.counts(c) for c in C.CODES},
           "names": {c: C.NAME[c] for c in C.CODES},
           "constants": {"floor_per_cent": C.FLOOR, "history_days": 330}}
    fig["ladder"] = {}
    for label, m, kw in LADDER:
        st, pr = P.call(m, **kw)
        fig["ladder"][label] = {"tuning": st, "productivity": {c: round(pr[c], 3) for c in C.CODES}}
    fig["family"] = {}
    for label, m, kw in FAMILY:
        st, pr = P.call(m, **kw)
        fig["family"][label] = {"tuning": st, "productivity": {c: round(pr[c], 3) for c in C.CODES}}
    aa = P.ask_investigations()
    quarters = ["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]
    fig["ask_investigations"] = {c: {q: aa.get((c, q), 0) for q in quarters} for c in C.CODES}
    sb = P.ask_sars()
    months = ["2026-%02d" % m for m in range(1, 11)]
    fig["ask_sars"] = {m: {"initial": sb.get((m, "initial"), 0), "continuing": sb.get((m, "continuing"), 0)}
                       for m in months}
    traps = [c for c in C.CODES if c not in call and c in fig["ladder"][LADDER[0][0]]["tuning"]]
    fig["traps"] = traps
    return fig


def metadata(n):
    src = {"alerts": "transaction monitoring alerts, July 2025 to October 2026",
           "cases": "AML case records from a case management system",
           "sars": "suspicious activity report filing log",
           "catalogue": "transaction monitoring scenario catalogue",
           "runs": "nightly monitoring run log",
           "procedure": "AML alert handling procedure",
           "thread": "compliance email on the 2027 tuning set",
           "risk": "customer risk tier extract",
           "capacity": "case team staffing plan for 2027",
           "qa": "quality assurance sampling of closed cases, 2026"}
    meta = {"task": "task191",
            "files": [{"name": Pk.FILES[k], "description": src[k], "source": "synthetic, built for this task",
                       "format": Pk.FILES[k].rsplit(".", 1)[1], "license": "CC0-1.0", "created": "2026-10-31"}
                      for k in Pk.FILES],
            "distractors": [Pk.FILES[k] for k in Pk.DISTRACTORS],
            "deliverables": ["tuning_scenarios_2027.docx", "tm_alert_figures_2026.xlsx"],
            "rows": n}
    with open(os.path.join(C.TASK, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1, ensure_ascii=False)
        f.write("\n")


def build():
    W = Wd.build()
    if os.path.isdir(C.TARGET):
        shutil.rmtree(C.TARGET)
    os.makedirs(C.TARGET)
    n = Pk.build(W, C.TARGET)
    P = A.Pack(C.TARGET)
    fig = figures(P, W)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
    metadata(n)
    return W, P, fig, n


if __name__ == "__main__":
    W, P, fig, n = build()
    print("tuning", fig["call"]["tuning"], "traps", fig["traps"])
    print("rows", n)
