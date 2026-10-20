"""The generator's checks on the cut pack and the generator's clean truth: the gates, the call under every route, the
analyst test executed, the semantic fork table (SF1 to SF10), the bins, the asks' devices."""
import calendar
import datetime as dt
import json
import os

import bundle as B
import methods as M
import pack as P
import world as W

GOLD = ["Brennan Hill", "Elmwood", "Fenwick", "Harlow", "Ivers"]
MID = ["Ashby", "Elmwood", "Ivers"]


def main(target, gdir, x):
    fails = []
    n = [0]

    def check(label, cond, detail=None):
        n[0] += 1
        print("%s  %s%s" % ("ok  " if cond else "FAIL", label, "" if cond or detail is None else "  [%s]" % (detail,)))
        if not cond:
            fails.append(label)

    files = sorted(os.listdir(target))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gates: %d files, formats %s, the largest %d rows" % (len(files), fmts, big),
          len(files) >= 10 and len(fmts) >= 3 and big >= 25000)
    check("gates: the pack is exactly world.FILES", set(files) == set(W.FILES.values()))
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json")))
    check("gates: two distractors in metadata.json, no file named for it", len(meta["distractors"]) >= 2)

    sets = {r: B.designated(B.inventory(target, route=r)) for r in ("record", "mid", "full", "golden")}
    check("call: the golden designates %s" % ", ".join(sets["golden"]), sets["golden"] == GOLD)
    check("analyst test (the midpoint start, the default path) designates %s" % ", ".join(sets["mid"]),
          sets["mid"] == MID)
    check("ladder R0 (from the find) designates none", sets["record"] == [])
    check("ladder R1 (from the previous survey) designates all 12", len(sets["full"]) == 12)
    # the analyst test on the clean truth: true starts against the midpoint of the true survey interval
    rows = P.inventory_rows(x)
    mi = P.miles(x)
    tr, md = {}, {}
    for r in rows:
        stop = min(r["repaired"] or dt.datetime(2027, 1, 1), dt.datetime(2027, 1, 1))
        rate = W.RATE[r["grade"]]
        tr[r["district"]] = tr.get(r["district"], 0) + rate * (stop - r["true"]).total_seconds() / 3.6e6
        st = r["found"] if r["how"] == "ODOR" else (dt.datetime.combine(r["prev"], dt.time(0)) + dt.timedelta(days=1)
                                                   + (r["found"] - dt.datetime.combine(r["prev"], dt.time(0))
                                                      - dt.timedelta(days=1)) / 2)
        md[r["district"]] = md.get(r["district"], 0) + rate * (stop - st).total_seconds() / 3.6e6
    tset = sorted(d for d in mi if tr[d] / mi[d] >= W.LINE)
    mset = sorted(d for d in mi if md[d] / mi[d] >= W.LINE)
    check("three rules, analyst test on the clean truth: the midpoint designates %s, the true starts %s" % (
        ", ".join(mset), ", ".join(tset)), mset == MID and tset == GOLD)
    gi = B.inventory(target)
    # forks
    v = B.designated(B.inventory(target, local=False))
    check("SF2 the odor calls read in UTC: the same call (%s)" % ", ".join(v), v == GOLD)
    for yrs, lab in ((range(2026, 2027), "2026 only"), (range(2016, 2026), "2016 to 2025")):
        inv = B.inventory(target, prof_years=set(yrs))
        check("SF5 the start profile from %s: the same call" % lab, B.designated(inv) == GOLD)
    # month-resolution expected start
    saved = M.expected_start

    def monthly(prev, found, prof):
        d0, d1 = prev, found.date()
        num = den = 0.0
        t = dt.date(d0.year, d0.month, 1)
        while t <= d1:
            last = dt.date(t.year, t.month, calendar.monthrange(t.year, t.month)[1])
            a, b = max(d0 + dt.timedelta(days=1), t), min(d1, last)
            if a <= b:
                days = (b - a).days + 1
                w = prof[t.month - 1] * days / calendar.monthrange(t.year, t.month)[1]
                mid = (a - d0).days + days / 2.0
                num += w * mid
                den += w
            t = last + dt.timedelta(days=1)
        return dt.datetime.combine(d0, dt.time(0)) + dt.timedelta(days=num / den)
    M.expected_start = monthly
    inv_m = B.inventory(target)
    M.expected_start = saved
    # SF3, SF4, SF6, SF7: the grade's latest value, the call less two days, the last visit, the district's first day
    seg, sched, lk, odor = B.load(target)
    prof = M.profile(odor)
    rep_rows = B.rows(target, "leak_repair_orders")
    last_grade, last_visit = {}, {}
    for r in rep_rows:
        t = dt.datetime.strptime(r["visit_local"], "%Y-%m-%d %H:%M")
        if r["leak_no"] not in last_visit or t >= last_visit[r["leak_no"]]:
            last_visit[r["leak_no"]] = t
            last_grade[r["leak_no"]] = B.grade(r["grade"])
    first_day = {}
    for (sid, y), d in sched.items():
        if y == 2025:
            k = seg[sid]["district"]
            first_day[k] = min(first_day.get(k, d), d)

    def alt(kind):
        rs = []
        for L in lk.values():
            if L["found"].year != 2026 or L["material"] not in ("CAST IRON", "BARE STEEL"):
                continue
            found, grade, rep = L["found"], L["grade"], L["repaired"]
            prev = sched.get((L["seg"], 2025)) if L["how"] == "SURVEY" else None
            if kind == "SF3":
                grade = last_grade.get(L["lid"], grade)
            if kind == "SF4" and L["how"] == "ODOR":
                found = found - dt.timedelta(days=2)
            if kind == "SF6":
                rep = last_visit.get(L["lid"]) if L["lid"] in last_visit and last_visit[L["lid"]] > L["found"] else rep
            if kind == "SF7" and prev:
                prev = first_day[L["district"]]
            rs.append(dict(district=L["district"], how=L["how"], found=found, prev=prev, grade=grade, repaired=rep))
        t = M.methane(rs, "golden", prof, B.RATE, B.YEAR_END)
        return sorted(d for d in gi if t.get(d, 0) / gi[d][2] >= B.LINE)
    for k, lab in (("SF3", "a regrade's grade"), ("SF4", "a called leak started two days before the call"),
                   ("SF6", "the last visit as the repair"), ("SF7", "the district's first survey day as the previous "
                                                                 "survey")):
        check("%s %s: the same call" % (k, lab), alt(k) == GOLD, alt(k))
    allmiles = {}
    for s_ in seg.values():
        allmiles[s_["district"]] = allmiles.get(s_["district"], 0) + int(s_["length_ft"]) / 5280.0
    check("SF8 every main's miles as the denominator: a different quantity, ruled out by guidelines 2.3 (%s)" %
          ", ".join(sorted(d for d in gi if gi[d][1] / allmiles[d] >= W.LINE)) or "none", True)
    near = min(abs(v[3] - W.LINE) for v in gi.values())
    check("SF9 the start weighted month by month rather than day by day: the same call", B.designated(inv_m) == GOLD)
    check("SF1 no district within 0.10 of the line (nearest %.3f)" % near, near > 0.10)
    import methods as M2
    spread = {}
    for lab, inv in (("2026 only", B.inventory(target, prof_years={2026})), ("by month", inv_m),
                     ("UTC", B.inventory(target, local=False))):
        spread[lab] = max(abs(inv[d][3] - gi[d][3]) for d in gi)
    check("SF5/SF9/SF2 the family's largest move in any district's per mile (%s) stays under its nearest district's "
          "distance to the line (%.3f): the call holds and no per-mile figure is graded" % (
              ", ".join("%s %.3f" % kv for kv in spread.items()), near), max(spread.values()) < near)
    g = x["fig"]
    check("figures: the bundle's inventory equals the generator's",
          all(abs(gi[r["district"]][3] - r["per_mile"]) < 1e-6 and gi[r["district"]][0] == r["leaks"] for r in g["rows"]))
    # asks
    a_g, a_c, a_cc = B.ask_a(target), B.ask_a(target, cumulative=False), B.ask_a(target, by_leak=False)
    check("ask A golden equals the generator's", all(abs(a_g[d] - g["ask_a"][d]) < 0.005 for d in W.DISTRICTS))
    miss = [d for d in W.DISTRICTS if round(a_c[d]) == round(a_g[d])]
    check("ask A device: the 2026 lines summed as they stand miss every district", not miss, miss)
    miss = [d for d in W.DISTRICTS if round(a_cc.get(d, 0)) == round(a_g[d])]
    check("ask A hazard: the cost center instead of the leak's district misses every district", not miss, miss)
    b_g, b_t, b_d = B.ask_b(target), B.ask_b(target, meters=False), B.ask_b(target, dedupe=False)
    check("ask B golden equals the generator's", b_g == g["ask_b"])
    miss = [d for d in W.DISTRICTS if b_t.get(d) == b_g.get(d)]
    check("ask B device: tickets counted as customers miss every district", not miss, miss)
    check("asks free of the call: the call reads no cost line, closeout, ticket or premise", True)
    print("checks: %d of %d pass" % (n[0] - len(fails), n[0]))
    return not fails
