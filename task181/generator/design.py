"""Design constraints measured on the clean truth, and the deterministic search for a world meeting them."""
import numpy as np

import routes as R
import datetime as dt
from world import (simulate_cases, assign_attributes, N, NAMES, GROUPS, BARANGAYS, SR, POB, LOC1, LOC2, DORMS)
EXTRACT_DAY = dt.date(2027, 10, 10)   # notified on or before the Sunday the extract follows

GOLD = {SR, LOC1, LOC2}
MARGIN_IN, MARGIN_OUT = 8.0, 5.0


def band(age):
    return 0 if age < 15 else (1 if age < 65 else 2)


def window(people, weeks=(37, 40), year=2027):
    """The cases the line list holds at the extract with onset in the window, by home, age band and place."""
    res = np.zeros((N, 3))
    place = np.zeros(N)
    for p in people:
        if p["year"] == year and weeks[0] <= p["week"] <= weeks[1] and p["reported"] <= EXTRACT_DAY:
            res[p["home"], band(p["age"])] += 1
            if p["place"] >= 0:
                place[p["place"]] += 1
    return res, place


def history(people):
    hist = np.zeros((N, 3))
    for p in people:
        if p["year"] <= 2026:
            hist[p["home"], band(p["age"])] += 1
    return hist


def cbms_bands(grp):
    """CBMS residents by band (0-14, 15-64, 65+) and employed residents, from the group table."""
    pop = np.stack([grp[:, 0], grp[:, 1] + grp[:, 2], grp[:, 3]], axis=1)
    return pop, grp[:, 1]


def is_interval(vals, gold):
    order = list(np.argsort(-np.asarray(vals, dtype=float), kind="stable"))
    pos = sorted(order.index(i) for i in gold)
    return pos[-1] - pos[0] == len(gold) - 1


def evaluate(cases, tables):
    popn, grp, W, workers = tables
    res, place = window(cases)
    prev, _ = window(cases, (33, 36))
    hist = history(cases)
    pop, emp = cbms_bands(grp)
    tot = res.sum(1)
    out = {"res": res, "place": place, "tot": tot, "prev": prev.sum(1)}
    fails = []
    if R.flagged(place) != GOLD:
        fails.append("truth set %s" % sorted(R.flagged(place)))
    over = [d for d in DORMS if tot[d] >= R.TRIGGER + MARGIN_OUT]
    for d in DORMS:
        if R.TRIGGER - MARGIN_OUT < tot[d] < R.TRIGGER + MARGIN_OUT:
            fails.append("dorm %s residence %d" % (NAMES[d], tot[d]))
    if len(over) < 4:
        fails.append("only %d dormitories over the trigger by residence" % len(over))
    for i in range(N):
        if i not in GOLD and i not in DORMS and tot[i] > R.TRIGGER - MARGIN_OUT:
            fails.append("ordinary %s residence %d" % (NAMES[i], tot[i]))
    if tot[SR] > R.TRIGGER - 10:
        fails.append("San Roque residence %d" % tot[SR])
    out["hist"], out["pop"], out["emp"] = hist, pop, emp
    for k, f in R.ROUTES_STEP.items():
        c = f(res, hist, pop, emp, W)
        if R.flagged(c) != GOLD:
            fails.append("%s set" % k)
            continue
        mi, mo = R.margins(c, GOLD)
        need_out = 1.5 if k == "fractional_0.5" else MARGIN_OUT
        if mi < MARGIN_IN or mo < need_out:
            fails.append("%s margins %.1f %.1f" % (k, mi, mo))
    for k, f in R.ROUTES_EASY.items():
        if R.flagged(f(res, hist, pop, emp, W)) == GOLD:
            fails.append("easy route %s lands" % k)
    rate = tot / popn
    emp_sh = res[:, 1] / np.maximum(tot, 1)
    growth = (tot + 1) / (out["prev"] + 1)
    for nm, v in (("count", tot), ("rate", rate), ("employed share", emp_sh), ("growth", growth),
                  ("children", res[:, 0]), ("children and elderly", res[:, [0, 2]].sum(1))):
        if is_interval(v, GOLD) or is_interval(-np.asarray(v, dtype=float), GOLD):
            fails.append("interval under %s" % nm)
    out["fails"] = fails
    return out


def search(limit=400):
    for k in range(limit):
        cases, tables, rates = simulate_cases(k)
        cases = assign_attributes(cases, k)
        ev = evaluate(cases, tables)
        if not ev["fails"]:
            return k, cases, tables, rates, ev
    raise RuntimeError("no world met the design in %d seeds" % limit)


if __name__ == "__main__":
    import sys, time
    t = time.time()
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    for k in range(lim):
        cases, tables, rates = simulate_cases(k)
        cases = assign_attributes(cases, k)
        ev = evaluate(cases, tables)
        print(k, len(cases), "OK" if not ev["fails"] else ev["fails"][:4])
    print("%.1fs" % (time.time() - t))
