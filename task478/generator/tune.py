"""Pick each section's pothole stream so the cut pack sits where the design needs it: every section's completed
estimate inside one whole-number bin, with room to spare, under each member of the completion's family (one find rate
for every unit, by maximum likelihood or by pairs; a rate per kind of section; a rate per fleet), the default path's
sections clear of the line and the generator's true count on the golden's side of it. The search reads only the
generator's own draws."""
import json
import os

import numpy as np

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))


def lane_miles(segs):
    out = {}
    for s in segs:
        if not s["turnback"]:
            out[s["sec"]] = out.get(s["sec"], 0.0) + s["length"] * s["lanes"]
    return out


def k_of(d):
    return sum(1 for u in d["seen"] if d["seen"][u])


def q_pairs(pots):
    a = b = 0
    for d in pots:
        C, k = len(d["seen"]), k_of(d)
        if C >= 2 and k >= 1:
            a += k * (k - 1)
            b += k * (C - 1)
    return a / b


def q_fleet(pots, unit_group):
    out = {}
    for g in ("PATROL", "FSP", "SWEEPER", "CREW"):
        a = b = 0
        for d in pots:
            for u in d["seen"]:
                if unit_group[u] != g:
                    continue
                if any(d["seen"][x] for x in d["seen"] if x != u):
                    b += 1
                    a += 1 if d["seen"][u] else 0
        out[g] = a / b
    return out


def family(no, pots, rates, lm, unit_group):
    """The section's estimate under each member of the family."""
    found = [d for d in pots if not d["turnback"] and k_of(d)]
    L = lm[no] / 10.0
    kind = W.SEC[no]["kind"]
    out = {}
    for name in ("pairs", "type", "fleet"):
        tot = 0.0
        for d in found:
            if name == "pairs":
                miss = (1.0 - rates["pairs"]) ** len(d["seen"])
            elif name == "type":
                miss = (1.0 - rates["type"][kind]) ** len(d["seen"])
            else:
                miss = float(np.prod([1.0 - rates["fleet"][unit_group[u]] for u in d["seen"]]))
            tot += 1.0 / (1.0 - miss)
        out[name] = tot / L
    out["raw"] = len(found) / L
    out["true"] = sum(1 for d in pots if not d["turnback"]) / L
    return out


def ok(no, f):
    whole = W.SEC[no]["whole"]
    if any(abs(f[m] - whole) > 0.4 for m in ("pairs", "type", "fleet")) or abs(f["pairs"] - whole) > 0.3:
        return False
    if whole >= 7 and no in (403, 407):
        return f["raw"] >= 6.9 and f["true"] >= 6.6
    if whole >= 7:
        return f["raw"] <= 5.15 and f["true"] >= 6.6
    return f["true"] <= 5.3 and f["raw"] <= 5.0


def rates_of(pots, unit_group):
    by = {"U": [], "S": [], "R": []}
    for d in pots:
        by[W.SEC[d["sec"]]["kind"]].append(d)
    return {"pairs": q_pairs(pots), "type": {k: q_pairs(v) for k, v in by.items()}, "fleet": q_fleet(pots, unit_group)}


def search(segs, looks, vehicles, rounds=12, span=900):
    tb = {s["seg"]: s["turnback"] for s in segs}
    lm = lane_miles(segs)
    unit_group = {v["unit"]: v["group"] for v in vehicles}
    pick = {no: 0 for no in W.ORDER}
    cache = {}

    def pots(no, off):
        if (no, off) not in cache:
            ps = W.section_potholes(no, segs, looks, off)
            for d in ps:
                d["turnback"] = tb[d["seg"]]
            cache[(no, off)] = ps
        return cache[(no, off)]
    for _ in range(rounds):
        allp = [d for no in W.ORDER for d in pots(no, pick[no]) if not d["turnback"]]
        rates = rates_of(allp, unit_group)
        changed = False
        for no in W.ORDER:
            if ok(no, family(no, pots(no, pick[no]), rates, lm, unit_group)):
                continue
            best = None
            for off in range(span):
                if ok(no, family(no, pots(no, off), rates, lm, unit_group)):
                    best = off
                    break
            assert best is not None, (no, "no stream in range")
            pick[no] = best
            changed = True
        if not changed:
            return pick
    raise AssertionError("tuning did not settle")


def main():
    segs, seg25, _ = W.network()
    veh = W.fleet(segs)
    trav, ign = W.driving(segs, veh)
    looks = W.looks_of(veh, trav)
    pick = search(segs, looks, veh)
    json.dump({str(k): v for k, v in pick.items()}, open(os.path.join(HERE, "tune.json"), "w"), indent=1, sort_keys=True)
    print(pick)


if __name__ == "__main__":
    main()
