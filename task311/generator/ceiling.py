"""The ask ceiling, measured on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every filed
rule) and the mirror (stops at the Kish rung) each scored on every graded ask figure, with the stress rows printed
beside them. Reads target.zip (or target/) through verify.py's own readers.

    python3 task311/generator/ceiling.py [target.zip]
"""
import datetime as dt
import hashlib
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import verify as V      # noqa: E402

REG = list(V.REG.values())


def ask_under(nm, wts, old2new, newreg, read):
    """The 2024 figures with each case's number read by `read(code, assigned, disposition_date)` -> new code."""
    w24 = {r["area_pre2024"]: r for r in wts if r["wave"] == "2024"}
    new2old = {v: k for k, v in old2new.items()}
    areas = {}
    for r in nm:
        if r["wave"] != "2024" or r["disposition"] not in ("1100", "1120"):
            continue
        new = read(r["area_at_assignment"], dt.date.fromisoformat(r["assigned"]),
                   dt.date.fromisoformat(r["disposition_date"]))
        if new is None:
            continue
        areas.setdefault(new, []).append({"1": 1, "2": 0, "3": 0}.get(r["q_rx_cost"]))
    out = {}
    for a, ys in areas.items():
        wrow = w24[new2old[a]]
        wt = float(wrow["design_weight"]) * int(wrow["occupied_dwellings"]) / len(ys)
        y = np.array([v for v in ys if v is not None], float)
        out.setdefault(newreg[a], []).append(dict(code=a, w=wt, m_all=len(ys), y=y,
                                                  stratum="S" if wrow["stratum"] == "CVS" else "C"))
    res = {}
    for reg, ar in out.items():
        p, v = V.taylor(ar)
        res[reg] = (sum(d["m_all"] for d in ar), round(100 * p, 1), round(100 * math.sqrt(v), 2))
    return res


def kept(res, figs):
    k = 0
    for reg in REG:
        key = reg.lower().replace(" ", "_")
        got = res.get(reg, (None, None, None))
        k += got[0] == figs["ask_completes_" + key]
        k += got[1] is not None and abs(got[1] - figs["ask_est_" + key]) < 0.05
        k += got[2] is not None and abs(got[2] - figs["ask_se_" + key]) < 0.005
    return k


def main(path):
    b = V.Bundle(path)
    nm, os_, wts, old2new, new2old, newreg = V.load(b)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    old = set(old2new)
    new = set(old2new.values())
    eff = dt.date(2024, 4, 1)
    readings = {
        "cracker: a number the pre-2024 series holds read as pre-2024 (battery repair)":
            lambda c, a, d: old2new[c] if c in old else (c if c in new else None),
        "cracker variant: split at the reorganisation date, by assignment":
            lambda c, a, d: (old2new.get(c) if a < eff else (c if c in new else None)),
        "cracker variant: split at the reorganisation date, by disposition date":
            lambda c, a, d: (old2new.get(c) if d < eff else (c if c in new else None)),
        "every 2024 number read as pre-2024":
            lambda c, a, d: old2new.get(c),
        "every 2024 number read as new":
            lambda c, a, d: c if c in new else None,
        "full includer: the switch read from the data (22 April 2024)":
            lambda c, a, d: (old2new.get(c) if a < dt.date(2024, 4, 22) else (c if c in new else None)),
    }
    n_fig = 3 * len(REG)
    rows = {}
    for name, fn in readings.items():
        rows[name] = kept(ask_under(nm, wts, old2new, newreg, fn), figs)
    digest = hashlib.sha256(open(path, "rb").read()).hexdigest()[:8] if os.path.isfile(path) else "folder"
    cr = list(readings)[0]
    cracker = 38 + 7 + 55.0 * rows[cr] / n_fig
    mirror = 5 + 7 + 55.0 * rows[cr] / n_fig
    print("pack %s; %d graded ask figures" % (digest, n_fig))
    for name, k in rows.items():
        print("  %-78s keeps %2d of %d" % (name, k, n_fig))
    print("cracker %.1f (38 + 7 + 55 x %d/%d); mirror %.1f (5 + 7 + 55 x %d/%d)" % (cracker, rows[cr], n_fig, mirror, rows[cr], n_fig))
    print("Pair ceiling: %.1f" % ((cracker + mirror) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * rows[cr] / n_fig))
    inc = rows[list(readings)[-1]]
    print("stress: the full includer keeps %d of %d; with the call landed the pair with a mirror-includer is %.1f"
          % (inc, n_fig, (38 + 7 + 55.0 * inc / n_fig + 5 + 7 + 55.0 * inc / n_fig) / 2))
    return 0 if all(rows[n] == 0 for n in list(readings)[:3]) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target.zip")))
