"""The ask layer's ceiling, measured on the cut pack: each response's ask figures recomputed from target/ with the
handling that response applies, scored cell by cell against the golden on the same files (the ortho-phosphate figures
are whole counts, so a cell is kept only when it is exact), and the pair priced on the planning weights (38 for the
call and its components, 7 for instruction-following, 55 for the asks).

    python3 task189/generator/ceiling.py [target]

The ask is the return's ortho-phosphate figures: for each water body, the compliance samples the year holds an
approved ortho-phosphate result for, and how many of those results were below the reporting limit (26 cells; the
chart's bars are the same cells).

Rows. The cracker lands the call and runs the whole hygiene battery on the ask: it keeps FIELD rows, takes each
result's latest version and drops withdrawn and provisional ones (regulation 7.5), joins every client code through
monitoring_point_crosswalk.csv, keeps the programme's points inside their dates (4.1, 4.2) and the reporting year
(1.4), and removes exact duplicates and natural-key duplicates (one result per point, determinand, collection date and
time). The mirror files rung 0 on the call (half the reporting limit) and handles the ask the same way, since the ask
reads nothing the call's construction produces: the separation assertions in checks.py prove the two share no row.
Stress rows: the plan reader counts the programme's required nutrient rounds less the rounds the programme sheet
records as not sampled; the one-a-month reader caps every point at one bottle a month; three partial includers each
handle one of the three reconstructions (the bottle booked twice at one point, the bottle re-booked to its own point,
the Tirneevin code the laboratory's numbering gives two points) and two handle two of them; the full includer handles
all three. The visit reader takes, at each compliance point, the nutrient booking filled on the visit that took the
point's pesticide sample (the same collection date and time): it is the golden's own handling, and the full includer
reaches the same figures from the bottles alone, which is the device side's convergence.
"""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
sys.path.insert(0, HERE)
import golden as G   # noqa: E402
import world as W    # noqa: E402


def score(resp, gold):
    cells = [(k, j) for k in sorted(gold) for j in (0, 1)]
    return sum(1 for (k, j) in cells if resp.get(k, (None, None))[j] == gold[k][j]), len(cells)


def tally(bt, pr, rg):
    pts = G.programme_points(pr)
    dates = G.programme_dates(pr)
    names = {r.water_body_code: r.water_body_name for r in rg.itertuples()}
    out = {}
    for b in bt:
        if b["point"] not in pts or not (W.YEAR_FROM <= b["date"] <= W.YEAR_TO):
            continue
        frm, to = dates[b["point"]]
        if not (frm <= b["date"] <= to) or b["opo4"][0] != "A":
            continue
        n, nd = out.get(names[b["wb"]], (0, 0))
        out[names[b["wb"]]] = (n + 1, nd + (1 if b["opo4"][1] == "<" else 0))
    return out


def handled(target, copies, rebook, shared):
    """the bookings after the chosen reconstructions; with none chosen it is the cracker's battery, since the
    natural-key and exact duplicate sweeps find nothing to remove in these bookings"""
    bk, xw, rg, pr = G.bookings(target)
    drop = set()
    if copies:
        by_pt = {}
        for i, b in enumerate(bk):
            by_pt.setdefault((b["lab"], b["point"], b["received"], b["sig"]), []).append(i)
        for idx in by_pt.values():
            idx = sorted(idx, key=lambda i: bk[i]["date"])
            for a, b in zip(idx, idx[1:]):
                if 1 <= (bk[b]["date"] - bk[a]["date"]).days <= 3:
                    drop.add(a)
    if rebook:
        by_bottle = {}
        for i, b in enumerate(bk):
            by_bottle.setdefault((b["lab"], b["date"], b["time"], b["received"], b["sig"]), []).append(i)
        for idx in by_bottle.values():
            if len({bk[i]["point"] for i in idx}) > 1:
                keep = max(idx, key=lambda i: bk[i]["newest"])
                drop.update(i for i in idx if i != keep)
    if shared:
        nut_lab = {}
        for b in bk:
            nut_lab.setdefault(b["point"], set()).add(b["lab"])
        for key, (comp, oppt) in G.shared_codes(target, xw, rg).items():
            mine = [i for i, b in enumerate(bk) if (b["lab"], b["code"]) == key and i not in drop]
            if nut_lab[comp] - {key[0]}:
                drop.update(mine)
            else:
                months = {}
                for i in mine:
                    months.setdefault((bk[i]["date"].year, bk[i]["date"].month), []).append(i)
                for idx in months.values():
                    drop.update(sorted(idx)[1:])
    # the battery's own sweeps: exact duplicates and one result per point, collection date and time
    seen, keep = set(), []
    for i, b in enumerate(bk):
        if i in drop:
            continue
        k = (b["point"], b["date"], b["time"])
        if k in seen:
            continue
        seen.add(k)
        keep.append(b)
    return tally(keep, pr, rg)


def plan_reader(target):
    """the programme's required nutrient rounds less the rounds its sheet records as not sampled"""
    import pandas as pd
    pr = pd.read_excel(os.path.join(target, "monitoring_programme_2025_26.xlsx"), sheet_name="Programme 2025-26",
                       header=None, dtype=object)
    ns = pd.read_excel(os.path.join(target, "monitoring_programme_2025_26.xlsx"), sheet_name="Rounds not sampled",
                       header=None, dtype=object)
    missed = {}
    for i in range(len(ns)):
        v = ns.iloc[i, 0]
        if isinstance(v, str) and v.startswith("ARW-"):
            missed[v] = missed.get(v, 0) + 1
    bk, xw, rg, _pr = G.bookings(target)
    lab_of = {}
    for b in bk:
        lab_of.setdefault(b["point"], set()).add(b["lab"])
    name_wb = {r.water_body_name: r.water_body_code for r in rg.itertuples()}
    out = {}
    for i in range(len(pr)):
        v = pr.iloc[i, 0]
        if not (isinstance(v, str) and v.startswith("ARW-")):
            continue
        rounds = int(pr.iloc[i, 5]) - missed.get(v, 0)
        wbname = str(pr.iloc[i, 2])
        n, nd = out.get(wbname, (0, 0))
        tas = lab_of.get(v, set()) == {"TAS"}
        out[wbname] = (n + rounds, nd + (rounds if tas else 0))
    return out


def one_a_month(target, rebook=False):
    """every point capped at one bottle a month, the battery otherwise as the cracker's; with rebook the
    re-booked bottles are first moved to their own points"""
    bk, xw, rg, pr = G.bookings(target)
    if rebook:
        by_bottle = {}
        for i, b in enumerate(bk):
            by_bottle.setdefault((b["lab"], b["date"], b["time"], b["received"], b["sig"]), []).append(i)
        gone = set()
        for idx in by_bottle.values():
            if len({bk[i]["point"] for i in idx}) > 1:
                keep_i = max(idx, key=lambda i: bk[i]["newest"])
                gone.update(i for i in idx if i != keep_i)
        bk = [b for i, b in enumerate(bk) if i not in gone]
    seen, keep = set(), []
    for b in sorted(bk, key=lambda z: (z["point"], z["date"], z["time"])):
        k = (b["point"], b["date"].year, b["date"].month)
        if k in seen:
            continue
        seen.add(k)
        keep.append(b)
    return tally(keep, pr, rg)


def main(target=TARGET):
    gold = G.ask_orthophosphate(target)
    rows = {
        "cracker": handled(target, False, False, False),
        "plan reader": plan_reader(target),
        "one bottle a month": one_a_month(target),
        "re-booking then one bottle a month": one_a_month(target, rebook=True),
        "double booking only": handled(target, True, False, False),
        "re-booking only": handled(target, False, True, False),
        "shared code only": handled(target, False, False, True),
        "double booking and re-booking": handled(target, True, True, False),
        "re-booking and shared code": handled(target, False, True, True),
        "full includer": handled(target, True, True, True),
        "visit reader": G.ask_orthophosphate(target),
    }
    k = {name: score(r, gold)[0] for name, r in rows.items()}
    n = score(gold, gold)[1]
    lc = k["cracker"] / n
    ls = k["cracker"] / n          # the mirror handles the ask exactly as the cracker does
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    print("cracker (lands the call, runs the battery, executes regulations 1.4, 4.1, 4.2 and 7.5): keeps %d of %d ask "
          "cells, response %.1f" % (k["cracker"], n, c))
    print("mirror (rung 0 on the call, the same ask handling; no row is shared, checks.py separation): keeps %d of %d, "
          "response %.1f" % (k["cracker"], n, s))
    for name in rows:
        if name == "cracker":
            continue
        print("%s: keeps %d of %d (stress row; on the call it scores %.1f)" % (name, k[name], n, 45 + 55 * k[name] / n))
    print("pair ceiling %.1f; mirror leakage %.1f per cent of the ask weight" % ((c + s) / 2, 100 * ls))
    print("golden  %s" % {w: gold[w] for w in sorted(gold)})
    print("cracker %s" % {w: rows["cracker"][w] for w in sorted(gold)})
    return dict(kept=k, n=n, pair=(c + s) / 2, leakage=100 * ls, rows=rows, gold=gold)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else TARGET)
