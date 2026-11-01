"""The generator's assertions on the cut pack: the call and its margins, every semantic fork (SF1 to SF14) closed or
convergent, the ladder's rungs, rounding edges, the separation line, the shock sorts and the ask devices.
Exit 1 on any failure."""
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import askcheck as AC  # noqa: E402
import routes as R     # noqa: E402
import solve as S      # noqa: E402

TARGET = os.path.join(HERE, "..", "target")
GOLD = ["Abbots Hollow", "Calder Bank", "Kestrel Rise"]
FAILS = []


def check(label, ok, detail=""):
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))
    if not ok:
        FAILS.append(label)


def r1(x):
    return round(float(x) + 1e-12, 1)


def same_figures(a, b):
    return all(r1(a[w]) == r1(b[w]) for w in a)


def interval(sorted_wards, chosen):
    pos = sorted(sorted_wards.index(w) for w in chosen)
    return pos == list(range(pos[0], pos[0] + len(pos)))


def main(t=TARGET):
    RT = R.routes(t)
    G = RT["R3 golden"]
    D = RT["R1 every pair (default)"]
    check("C1 the call", S.pressured(G) == GOLD, str(S.pressured(G)))
    check("C1 the default path files four", S.pressured(D) == sorted(GOLD + ["Pellbury"]), str(S.pressured(D)))
    near = min(abs(v - 5.0) for v in G.values())
    check("C2 golden margin to the line", near >= 0.4, "%.2f" % near)
    check("C2 default margin, Pellbury", D["Pellbury"] - 5.0 >= 0.5, "%.2f" % D["Pellbury"])
    check("SF1 constant quality: every pair files the four, pairs spanning work set aside file three",
          S.pressured(D) != S.pressured(G))
    for k, sf in (("R3 size works only", "SF2"), ("R3 received date", "SF3"), ("R3 loose match", "SF4"),
                  ("R3 recode linked", "SF4b")):
        check("%s %s files the golden figures" % (sf, k), same_figures(RT[k], G))
    check("SF5 update not applied: same call on the decisive route", S.pressured(RT["R3 no update"]) == GOLD)
    check("SF5 update not applied: the default still files four", "Pellbury" in S.pressured(RT["R1 every pair, no update"]))
    check("SF6 category B in the index is ruled out by methodology section 2 (moves the call)",
          S.pressured(RT["R3 A and B"]) != GOLD, str(S.pressured(RT["R3 A and B"])))
    check("SF7 new dwellings' first sales left out: same call", S.pressured(RT["R3 no new-build first"]) == GOLD)
    check("SF8 2019 wards: same call", S.pressured(RT["R3 2019 wards"]) == GOLD)
    for k in ("R3 WRS", "R3 six-month hold", "R3 3-sd trim"):
        check("SF9 %s: same call" % k, S.pressured(RT[k]) == GOLD, "%.2f Abbots" % RT[k]["Abbots Hollow"])
    for k in ("R2 every pair, six-month hold", "R2 every pair, WRS", "R2 every pair, 3-sd trim",
              "R2 every pair, no new-build first", "R2 every pair, 2019 wards"):
        check("SF9 rung 2 %s keeps Pellbury" % k, "Pellbury" in S.pressured(RT[k]) and S.pressured(RT[k]) != GOLD)
    check("C3 rung 0 (median) is not the golden", S.pressured(RT["R0 median"]) != GOLD, str(S.pressured(RT["R0 median"])))
    # SF10: same-year pairs drop out; SF11: no ward near the line at the published decimal
    check("SF11 no ward within 0.05 of the line", all(abs(v - 5.0) > 0.05 for v in G.values()))
    edges = {w: abs((v * 10) % 1 - 0.5) / 10 for w, v in G.items()}
    check("C4 rounding edges", min(edges.values()) >= 0.006, "%s %.4f" % min(edges.items(), key=lambda x: x[1]))
    # the shares
    homes = S.pipeline_homes(t)
    sh, exact = S.shares(GOLD, homes)
    check("SF12 shares sum to the pot", sum(sh.values()) == S.POT, str(sh))
    check("SF12 no share on an exact half", all(abs(v - int(v) - 0.5) > 0.01 for v in exact.values()))
    from openpyxl import load_workbook
    wb = load_workbook(S.p(t, "pipe"), read_only=True, data_only=True)
    starts = [r[9].date() for r in list(wb["Pipeline"].iter_rows(values_only=True))[1:]]
    bounds = {dt.date(2027, 3, 31), dt.date(2027, 4, 1), dt.date(2028, 3, 31), dt.date(2028, 4, 1)}
    check("SF13 SF14 no scheme starts on a programme-year boundary", not (set(starts) & bounds))
    # separation: device rows outside the call's population
    recs = S.load_ppd(t)
    st = S.standard(recs)
    check("C5 separation: every entry the money ask groups is outside the standard sales",
          all(x["cat"] == "B" for x in recs if x["ptype"] in "DSTF" and x["date"].year == 2026 and
              sum(1 for y in recs if y["date"] == x["date"] and y["price"] == x["price"]) > 1 and x["price"] > 900000)
          and not any(x["cat"] == "B" for x in st))
    reg = S.load_register(t)
    full = S.works_index(reg)
    works_only = S.works_index(reg, kinds=lambda w: w["created"] == 0 and not w["lost"] and not w["lost_blank"])
    prs = S.pairs_of(st)
    a = len(S.clean(prs, full))
    b = len(S.clean(prs, works_only))
    check("C5 separation: no supply row (new dwellings, conversions, demolitions) sets a sales pair aside", a == b,
          "%d against %d" % (a, b))
    # shock: the golden set is not an interval of any shipped sort
    by_default = sorted(D, key=lambda w: -D[w])
    med = RT["R0 median"]
    by_med = sorted(med, key=lambda w: -med[w])
    cnt = defaultdict(int)
    for x in st:
        if x["date"].year == 2026:
            cnt[S.load_wards(t).get(S.norm_pc(x["postcode"]))] += 1 if False else 0
    ward_of = S.load_wards(t)
    for x in st:
        if x["date"].year == 2026:
            cnt[ward_of.get(S.norm_pc(x["postcode"]))] += 1
    by_cnt = sorted(cnt, key=lambda w: -cnt[w])
    for name, order in (("every-pair change", by_default), ("median change", by_med), ("2026 sales", by_cnt)):
        check("C6 shock: the golden set is not an interval of the %s sort" % name, not interval(order, GOLD),
              ", ".join(w[:6] for w in order[:6]))
    # the flips the decisive step sets aside
    Gs = S.solve(t)
    Ds = S.solve(t, drop_works=False)
    n_all = sum(1 for k, x, y in Ds["pairs"] if y["date"].year == 2026 and ward_of.get(S.norm_pc(y["postcode"])) == "Pellbury")
    n_kept = sum(1 for k, x, y in Gs["pairs"] if y["date"].year == 2026 and ward_of.get(S.norm_pc(y["postcode"])) == "Pellbury")
    check("C7 Pellbury pairs set aside, 2026", n_all - n_kept >= 30, "%d of %d" % (n_all - n_kept, n_all))
    # the asks' devices
    A, B, C = AC.variants(t)
    off = lambda route, gold: sum(1 for w in gold if route.get(w, 0) != gold.get(w, 0))
    check("C8 Ask A blank lost read as none moves every ward", off(A["blank lost as 0"], A["golden"]) >= 11,
          str(off(A["blank lost as 0"], A["golden"])))
    check("C8 Ask A blank lost read as one (the over-cleaner) misses", off(A["blank lost as 1"], A["golden"]) >= 4)
    check("C8 Ask B every title", off(B["every title"], B["golden"]) >= 7)
    check("C8 Ask B every same-day pair grouped (the over-cleaner)", off(B["same-day pairs one"], B["golden"]) >= 6)
    check("C8 Ask C every claim", off(C["every claim"], C["golden"]) >= 7)
    check("C8 Ask C exact repeats only", off(C["exact repeats only"], C["golden"]) >= 5)
    # fairness: the golden handling reproduces the world's truth for the asks
    import pack as K
    import world as Wm
    W = Wm.simulate()
    K.price_paid(W)
    rows = K.register_rows(W)
    truth = defaultdict(int)
    seen = set()
    for x in rows:
        if x["completed"].year == 2026 and (x["created"] or x.get("lost_true") or x["lost"]) and x["ref"] not in seen:
            seen.add(x["ref"])
            lost = x.get("lost_true", x["lost"] or 0) if x["kind"] in ("conversion", "change_of_use") else (x["lost"] or 0)
            truth[x["ward"]] += x["created"] - lost
    check("C9 Ask A golden equals the world's net additions", all(truth[w] == A["golden"].get(w, 0) for w in truth),
          str(dict(truth)))
    print("%d checks failed" % len(FAILS) if FAILS else "all checks pass")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else TARGET))
