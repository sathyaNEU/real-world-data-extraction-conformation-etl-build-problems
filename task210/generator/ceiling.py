"""The cracker and mirror sheets, run on the cut pack. Every graded ask figure of the return lines and the chart is
scored for three responses, each computed here from target/ by its own route:

  cracker  lands the call (each station's wet well cycles), runs the hygiene battery (re-sent telemetry events
           dropped, the platform's UK local time converted, the procedure's 12/24 count, overlapping records
           counted once, the year's 8,760 hours) and joins the discharge log and the daily status on the monitor
           the asset register lists for each overflow;
  mirror   stops at the rated duty of the running pump (the meter at the three metered stations), so every
           overflow met its permit, and takes the asks by the same careful route;
  naive    times the drawdown without the inflow (rung 0b), so Hagworth Wold, Gallowfen and Marram End fall short,
           and takes the asks by the same careful route (printed beside the mirror; the rated route scores higher);
  full     the golden: every serial the platform holds mapped to its overflow and pooled.

A hit is a figure within half a unit of its stated rounding. Scores on 38, 7 and 55 so builds compare; the pack's
digest is printed so a figure is tied to the pack it was measured on. No figure here is typed: each response is
code run on the pack."""
import hashlib
import os
import sys

import golden as G
import routes as RT


def lines_for(g, serial_site):
    st = g["stations"]
    return G.returns(st, g["log"], g["status"], serial_site)


def measure(tgt, g, L=None):
    st = g["stations"]
    L = L or RT.ladder(g, tgt)
    gold = g["lines"]
    current = {s["edm"]: c for c, s in st.items()}
    cur = lines_for(g, current)
    # an unrestricted mapping (alarm coincidence without the install dates) is the half-handled stop
    unres, _ = G.map_monitors(st, g["log"], g["mlist"], g["alarms"], restrict=False)
    half = lines_for(g, unres)
    mf = L["R1_meter_flow"]
    rated = {c: (mf[c] if c in mf else min(st[c]["rated"].values())) for c in st}

    def figures(route):
        out = {}
        for c in st:
            if route == "full":
                dl, met, ln = g["delivered"][c], c not in g["breach"], gold[c]
            elif route == "cracker":
                dl, met, ln = g["delivered"][c], c not in g["breach"], cur[c]
            elif route == "mirror":
                dl, met, ln = rated[c], rated[c] >= g["pff"][c], cur[c]
            elif route == "half":
                dl, met, ln = g["delivered"][c], c not in g["breach"], half[c]
            elif route == "naive":
                dl, met, ln = L["naive"][c], L["naive"][c] >= g["pff"][c], cur[c]
            out[c] = dict(pff=round(g["pff"][c]), delivered=round(dl), met=met, spills=ln["spills"],
                          hours="%.1f" % ln["hours"], operational="%.1f" % ln["operational"],
                          months=tuple("%.1f" % x for x in ln["months"]))
        return out

    ref = figures("full")
    rows = {}
    for route in ("cracker", "mirror", "full", "half", "naive"):
        f = figures(route)
        keep = {k: sum(1 for c in st if f[c][k] == ref[c][k]) for k in ("pff", "delivered", "met", "spills", "hours",
                                                                          "operational", "months")}
        rows[route] = keep
    n = len(st)
    total = 7 * n
    Lc = sum(rows["cracker"].values()) / total
    Lm = sum(rows["mirror"].values()) / total
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Lm
    device_cols = ("spills", "hours", "operational", "months")
    Ln = sum(rows["naive"].values()) / total
    out_naive = round((C + 5 + 7 + 55 * Ln) / 2, 1)
    out = dict(rows=rows, figures=total, naive_mirror_score=round(5 + 7 + 55 * Ln, 1), pair_with_naive_mirror=out_naive,
               cracker_score=round(C, 1), mirror_score=round(S, 1), pair=round((C + S) / 2, 1),
               cracker_keep=round(100 * Lc, 1), mirror_leakage=round(100 * Lm, 1),
               full_keep=round(100 * sum(rows["full"].values()) / total, 1),
               cracker_device_keep="%d of %d" % (sum(rows["cracker"][k] for k in device_cols), len(device_cols) * n),
               half_device_keep="%d of %d" % (sum(rows["half"][k] for k in device_cols), len(device_cols) * n))
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(tgt)):
        for fn in sorted(files):
            h.update(open(os.path.join(root, fn), "rb").read())
    out["pack_digest"] = h.hexdigest()[:16]
    return out


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    tgt = os.path.join(os.path.dirname(here), "target")
    g = G.compute(tgt)
    m = measure(tgt, g)
    for k, v in m.items():
        print(k, v)
