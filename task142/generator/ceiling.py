"""Pair ceiling on the cut pack: the cracker (lands the call, runs the hygiene battery, reads every document) and the
mirror (stops at the pre-1985 rung) each answer every ask the careful way they would, and each figure is scored
against the golden at the prompt's rounding (a hit is the same rounded figure).

    python3 task142/generator/ceiling.py            # prints the sheet; exit 1 if the pair ceiling exceeds 60
"""
import datetime as dt
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402

TARGET = os.path.join(TASK, "target")
CALL_POINTS = 45.0     # a response on the main call before any ask (supplemental-stumping Part 0)
OFF_POINTS = 12.0      # a response off it
ASK_WEIGHT = 55.0


def cracker_gas(T, L):
    """Joins the schedule's EAN to the telemetry, drops the resent duplicate, differences each serial's first and last
    read inside the gas year."""
    reads = defaultdict(list)
    seen = set()
    for r in T["gasreads"]:
        k = tuple(r.values())
        if k in seen:
            continue
        seen.add(k)
        reads[r["ean"]].append(r)
    out = defaultdict(int)
    for b in L:
        rs = sorted(reads[b["ean"]], key=lambda r: r["tijdstip"])
        by_ser = defaultdict(list)
        for r in rs:
            if "2025-10-01T06:00" <= r["tijdstip"][:16] <= "2026-10-01T06:00":
                by_ser[r["meternummer"]].append(int(r["meterstand_m3"]))
        out[b["phase"]] += sum(v[-1] - v[0] for v in by_ser.values())
    return dict(out)


def cracker_heat(T):
    """Converts the drive-by units and differences each meter from its annual (or connection) read to its last drive-by
    read for 2024-25; takes 2025-26 from the AMR registers per serial (right)."""
    cat = {c["aansluitnummer"]: c["categorie"] for c in T["conns"]}
    owner = {}
    for m in T["meters"]:
        owner[str(m["meternummer"])] = m["aansluitnummer"]
    leg = defaultdict(list)
    for r in T["legacy"]:
        f = 277.7778 if r["eenheid"] == "GJ" else 1000.0
        leg[r["meternummer"]].append((dt.datetime.strptime(r["opnamedatum"], "%d-%m-%Y").date(),
                                      A.fnum(r["stand"]) * f))
    y1 = defaultdict(float)
    for ser, rs in leg.items():
        rs.sort()
        y1[cat[owner[ser]]] += rs[-1][1] - rs[0][1]
    _, y2 = A.heat_by_category(T)
    return {k: v / 1000.0 for k, v in y1.items()}, y2


def score(F, gas, h1, h2):
    figs = []
    for ph in range(1, 7):
        figs.append(("gas phase %d" % ph, A.rnd(gas.get(ph, 0), 1000) == F["gas_m3"][str(ph)]))
    figs.append(("heat 2024-25 Woningen", A.rnd(h1["Woningen"], 1000) == F["heat_2425_MWh"]["Woningen"]))
    figs.append(("heat 2024-25 Utiliteit", A.rnd(h1["Utiliteit"], 100) == F["heat_2425_MWh"]["Utiliteit"]))
    figs.append(("change Woningen", A.rnd(h2["Woningen"] - h1["Woningen"], 1000) == F["heat_change_MWh"]["Woningen"]))
    figs.append(("change Utiliteit", A.rnd(h2["Utiliteit"] - h1["Utiliteit"], 100) == F["heat_change_MWh"]["Utiliteit"]))
    return figs


def main(target=TARGET):
    F, M, _ = A.figures(target)
    T = M["T"]
    gas = cracker_gas(T, M["loads"])
    h1, h2 = cracker_heat(T)
    figs = score(F, gas, h1, h2)
    kept = sum(1 for _, hit in figs if hit) / len(figs)
    cracker = CALL_POINTS + ASK_WEIGHT * kept
    mirror = OFF_POINTS + ASK_WEIGHT * kept          # the asks are decoupled: the mirror handles them the same way
    pair = (cracker + mirror) / 2
    leak = 100.0 * kept
    print("ask figures kept by the cracker: %d of %d" % (sum(1 for _, h in figs if h), len(figs)))
    for name, hit in figs:
        print("  %-26s %s" % (name, "hit" if hit else "miss"))
    print("cracker %.1f  mirror %.1f  pair ceiling %.1f  mirror leakage %.1f per cent" % (cracker, mirror, pair, leak))
    # the full includer keeps every figure
    gas_full, _ = A.gas_by_phase(T, M["loads"])
    f1, f2 = A.heat_by_category(T)
    full = score(F, gas_full, f1, f2)
    print("full includer keeps %d of %d" % (sum(1 for _, h in full if h), len(full)))
    return pair, leak, figs


if __name__ == "__main__":
    p, l, _ = main(sys.argv[1] if len(sys.argv) > 1 else TARGET)
    sys.exit(0 if p <= 60 and l < 50 else 1)
