"""The ask layer's cracker and mirror, run on the contractors' exports as the pack cuts them: each stop is a route a
careful reader takes, scored figure by figure against the golden at the ask's rounding (a site's tonnes to the
nearest 10, its recovery share to one decimal). Prints the pair ceiling and the mirror's leakage.

    python3 task485/generator/ceiling.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import ash as A    # noqa: E402

REC = {"Yarrdale Blocks", "Velthwaite Cement Works"}


def load():
    """the cut pack's three exports, read back from target/ when present, else from the generator"""
    import pack_read
    return pack_read.ash_exports()


def route(E, keep_moorside_sub=True, keep_local_sub=True, drop_same_day=False, by_invoice=True, kg_as_t=False,
          other=False, y2027=False):
    """each site's ash taken off site in 2026 and its recovery share under one handling of the three exports"""
    sub_refs = set()
    for r in E["moorside"]:
        if r["ref"] and not r["ref"].startswith("WM-"):
            sub_refs.add(r["ref"])
    rows = []
    for r in E["moorside"]:
        if r["kind"] == "other" and not other:
            continue
        if (not r["ref"].startswith("WM-")) and not keep_moorside_sub:
            continue
        rows.append(dict(src="M", site=r["site"], day=r["day"], t=r["qty"], rec=r["dest"] in ("cement", "blocks"),
                         ref=r["ref"]))
    for key, unit in (("tolland", "kg"), ("greave", "t")):
        for r in E[key]:
            if r["kind"] == "other" and not other:
                continue
            if r["job"] in sub_refs and not keep_local_sub:
                continue
            t = r["net_kg"] / (1.0 if kg_as_t else 1000.0) if unit == "kg" else r["net_t"]
            rows.append(dict(src="L", site=r["site"], day=r["day"], t=t, rec=r["dest"] in REC, ref=r["job"]))
    if drop_same_day:
        local_days = set((r["site"], r["day"]) for r in rows if r["src"] == "L")
        rows = [r for r in rows if not (r["src"] == "M" and (r["site"], r["day"]) in local_days)]
    out = {}
    for r in rows:
        if r["day"] > 364 and not y2027:
            continue
        o = out.setdefault(r["site"], [0.0, 0.0])
        o[0] += r["t"]
        o[1] += r["t"] if r["rec"] else 0.0
    return {s: (v[0], 100 * v[1] / v[0] if v[0] else 0.0) for s, v in out.items()}


def score(gold, got):
    hits = 0
    for s, (t, p) in gold.items():
        g = got.get(s, (0, 0))
        hits += int(round(g[0], -1) == round(t, -1))
        hits += int(round(g[1], 1) == round(p, 1))
    return hits


def main():
    E = load()
    gold = route(E, keep_moorside_sub=False)
    n = 2 * len(gold)
    stops = [
        ("every ash line once as exported", route(E)),
        ("a Whinmoss line beside a same-day local job dropped", route(E, drop_same_day=True)),
        ("Whinmoss's lines kept and the local jobs they bill dropped", route(E, keep_local_sub=False)),
        ("the reference read, Carnhope's kilograms read as tonnes", route(E, keep_moorside_sub=False, kg_as_t=True)),
        ("the reference read, other waste and January 2027 kept", route(E, keep_moorside_sub=False, other=True, y2027=True)),
        ("golden", gold),
    ]
    print("ask A: %d graded figures (16 sites' tonnes to the nearest 10 and recovery share to one decimal)" % n)
    res = {}
    for name, got in stops:
        h = score(gold, got)
        res[name] = h
        print("  %-62s %2d of %d" % (name, h, n))
    cracker = res["every ash line once as exported"]
    mirror = res["every ash line once as exported"]
    lc, ls = cracker / n, mirror / n
    C = 38 + 7 + 55 * lc
    S = 5 + 7 + 55 * ls
    print("cracker keeps %.1f per cent of ask weight (scores %.1f with the call); mirror %.1f per cent (%.1f)" % (
        100 * lc, C, 100 * ls, S))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return res


if __name__ == "__main__":
    main()
