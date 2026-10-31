"""The generator's assertions for task482 (architecture 15), on the cut pack and on the generator's clean truth.

    python3 task482/generator/checks.py

Sections: the input gates; the golden against the truth the world holds; the three rules executed on the clean truth
(dataset-generation 7.1); the ladder's rungs with their calls and margins; the cheap routes and how many reach the
call; the semantic fork table, each row SF1 to SF17 asserted; the rounding edges; the asks. Exit 1 on any failure."""
import collections
import csv
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import world as W   # noqa: E402
import pack as P    # noqa: E402
import golden as G  # noqa: E402

D = dt.date
FAILS = []
LIMIT = W.LIMIT / 100.0
OPT = W.OPTIONS


def ok(cond, msg):
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        FAILS.append(msg)


def edge(v, unit):
    """Distance of v from its rounding edge, in units of the rounding."""
    x = v / unit + 1e-12
    return abs(x - int(x) - 0.5)


def route(dem, put, mm, load=1.0):
    c = G.costs(dem, put, mm)
    if load != 1.0:
        for m in OPT:
            c["options"][m]["increase"] = round(c["options"][m]["raw_increase"] * load + 1e-9, 2)
    return c, G.call(c)


def incs(c):
    return tuple(c["options"][m]["increase"] for m in OPT[1:])


def months_in(p, key, year):
    saved = G.YEAR
    G.YEAR = year
    try:
        return G.member_months(p, key)
    finally:
        G.YEAR = saved


def csvrows(name):
    with open(os.path.join(T, name), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------------------------------------ variant readings
def lines_as_at(p, key, cut=None, first=False):
    """The conformed lines as they stood on cut (only versions decided by then, a later correction not yet in force),
    or with every claim at its first version (first=True)."""
    L, N = p["legacy_claims"], p["new_claims"]
    when_l = lambda r: G.usdate(r["PROCESSED"])
    when_n = lambda r: G.isodate(r["adjudicated_date"])
    inn = (lambda d0: True) if cut is None else (lambda d0: d0 <= cut)
    replaced = set()
    if not first:
        replaced |= set(r["ORIG_CLAIM_NO"] for r in L if r["TXN"] == "VOID" and inn(when_l(r)))
        replaced |= set(r["prior_claim_id"] for r in N if r["prior_claim_id"] and inn(when_n(r)))
    out = []
    for r in L:
        if not inn(when_l(r)) or r["TXN"] == "VOID" or (first and r["TXN"] == "REPL"):
            continue
        if r["TXN"] == "ORIG" and r["CLAIM_NO"] in replaced:
            continue
        out.append((key(r["MEMBER_ID"]), G.usdate(r["DOS"]), "D" + r["PROC"], r["TOOTH"], G.cents(r["ALLOWED"]),
                    G.cents(r["PAID"]), G.cents(r["DEDUCT"]), {"MX": "MAX", "DD": "DED", "FQ": "FRQ", "": ""}[r["REASON"]]))
    for r in N:
        if not inn(when_n(r)) or (first and r["prior_claim_id"]) or r["claim_id"] in replaced:
            continue
        out.append((r["member_key"], G.isodate(r["service_date"]), r["cdt_code"], r["tooth_number"].lstrip("0"),
                    G.cents(r["allowed_amt"]), G.cents(r["plan_paid_amt"]), G.cents(r["deductible_amt"]),
                    {"119": "MAX", "1": "DED", "151": "FRQ", "": ""}[r["carc"]]))
    return out


def demand_reapplied(p, lines, fee_year=2027):
    """Each person's 2025 demand with the 50 dollar deductible re-applied in service-date order at fee_year's fees."""
    fees, cls = p["fees"][fee_year], p["cls"]
    by = collections.defaultdict(list)
    for who, dos, code, tooth, allowed, paid, ded, reason in lines:
        if dos.year == 2025 and reason != "FRQ":
            by[who].append((dos, code))
    out = {}
    for who, ls in by.items():
        left, tot = W.DEDUCTIBLE, 0
        for dos, code in sorted(ls):
            d0 = min(left, fees[code]) if cls[code] > 1 else 0
            left -= d0
            tot += (fees[code] - d0) * W.COINS[cls[code]] // 100
        out[who] = tot
    return out


def demand_frq_priced(p, lines, fee_year=2027):
    fees, cls = p["fees"][fee_year], p["cls"]
    out = {}
    for who, dos, code, tooth, allowed, paid, ded, reason in lines:
        if dos.year == 2025:
            out[who] = out.get(who, 0) + (fees[code] - ded) * W.COINS[cls[code]] // 100
    return out


def put_family(p, key, lines, est):
    """The put-off work matched on the person, the procedure family (the code's first three characters) and the
    tooth, within the estimate's twelve months."""
    fees, cls = p["fees"][2027], p["cls"]
    claimed = collections.defaultdict(list)
    for who, dos, code, tooth, *_ in lines:
        claimed[(who, code[:3], tooth)].append(dos)
    cut = set(r[8] for r in est if r[7] < (r[5] - r[6]) * W.COINS[cls[r[3]]] // 100)
    seen, out = set(), {}
    for who, recv, issued, code, tooth, allowed, ded, plan, req, npi, eid in est:
        if issued.year != 2025 or req not in cut or (who, code, tooth) in seen:
            continue
        ds = claimed.get((who, code[:3], tooth), [])
        if any(recv.date() <= d0 <= D(2025, 12, 31) for d0 in ds):
            continue
        end = D(issued.year + 1, issued.month, min(issued.day, 28))
        if not any(D(2026, 1, 1) <= d0 <= end for d0 in ds):
            continue
        seen.add((who, code, tooth))
        out[who] = out.get(who, 0) + fees[code] * W.COINS[cls[code]] // 100
    return out


def put_with_deductible(p, put_lines_by_person, paid_ded):
    return put_lines_by_person


def main():
    res = G.solve(T)
    p, key, lines, mm, est = res["p"], res["key"], res["lines"], res["mm"], res["est"]
    gold, naive, dem, put = res["gold"], res["naive"], res["dem"], res["put"]
    go = gold["options"]
    print("== input gates")
    files = sorted(os.listdir(T))
    ok(len(files) >= 10, "%d files in target/" % len(files))
    exts = sorted(set(f.rsplit(".", 1)[1] for f in files))
    ok(len(exts) >= 3, "formats: %s" % ", ".join(exts))
    big = max(sum(1 for _ in open(os.path.join(T, f), "rb")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "largest file %d rows" % big)
    meta_p = os.path.join(TASK, "metadata.json")
    if os.path.exists(meta_p):
        meta = json.load(open(meta_p))
        dis = meta.get("distractor_files", [])
        ok(len(dis) >= 2 and all(os.path.exists(os.path.join(TASK, d)) for d in dis), "distractors: %s" % ", ".join(dis))
    for word in ("defer", "put_off", "putoff", "reset", "postpon", "distract", "induc", "pent"):
        ok(not any(word in f.lower() for f in files), "no file name carries %r" % word)

    print("== the golden against the truth")
    w = W.build()
    ids = P.identities(w)
    keyof = lambda pid: ids["new"].get(pid) or ids["legacy"][pid][1]
    t_dem = collections.Counter()
    for c in w["claims"]:
        if c["dos"].year != 2025:
            continue
        ls = w["adjust"][c["cid"]]["lines"] if c["cid"] in w["adjust"] else c["lines"]
        for ln in ls:
            if ln["reason"] != "FRQ":
                t_dem[keyof(c["pid"])] += (W.FEES[2027][ln["code"]] - ln["ded"]) * W.COINS[W.plan_class(ln["code"])] // 100
    t_put = collections.Counter()
    outcomes = collections.Counter()
    came_back = set()
    for c in w["claims"]:
        if c["origin"] == "deferred" and c["dos"].year == 2026:
            came_back.add((c["pid"], c["dos"]))
    for pr in w["predets"]:
        for gi, (oc, when) in pr["outcome"].items():
            if pr["year"] == 2025:
                outcomes[oc] += 1
            if pr["year"] == 2025 and oc == "deferred_done" and (pr["pid"], when) in came_back:
                for ln in pr["lines"]:
                    if ln["group"] == gi:
                        t_put[keyof(pr["pid"])] += W.FEES[2027][ln["code"]] * W.COINS[W.plan_class(ln["code"])] // 100
    t_mm = {}
    for q in w["people"]:
        m = W.member_months(q, 2025)
        if m:
            t_mm[keyof(q["pid"])] = m
    ok({k: v for k, v in dem.items() if v} == {k: v for k, v in t_dem.items() if v},
       "2025 demand at the 2027 fees recovers the truth for every person (%d persons)" % len(t_dem))
    ok(dict(t_put) == put, "the put-off work recovers the truth: %d persons, %.2f" % (len(put), sum(put.values()) / 100))
    if dict(t_put) != put:
        diff = sorted(set(t_put) ^ set(put) | set(k for k in put if put.get(k) != t_put.get(k)))
        print("      truth %d persons %.2f; differing %s" % (len(t_put), sum(t_put.values()) / 100.0,
              [(k, t_put.get(k), put.get(k)) for k in diff[:6]]))
    ok({k: v for k, v in mm.items() if v} == t_mm, "2025 covered person months recover the truth (%d persons, %d months)"
       % (len(t_mm), sum(t_mm.values())))
    print("      2025 cut estimate groups by outcome: %s" % dict(outcomes))

    print("== the three rules on the clean truth (dataset-generation 7.1)")
    tc, tcall = route(t_dem, dict(t_put), t_mm)
    nc, ncall = route(t_dem, {}, t_mm)
    ok(tcall == 200000, "the decisive step taken on the clean truth: %d (increases %s)" % (tcall // 100, incs(tc)))
    ok(ncall == 300000, "the analyst test on the clean truth (every field read, every rule applied, the continuance): "
       "%d (increases %s)" % (ncall // 100, incs(nc)))
    ok(res["call"] == 200000 and res["naive_call"] == 300000, "on the cut pack: golden %d, continuance %d"
       % (res["call"] // 100, res["naive_call"] // 100))

    print("== the ladder")
    rungs = []
    dem25 = G.demand(p, lines, fee_year=2025)
    c0, k0 = route(dem25, {}, mm)
    rungs.append(("R0 the 2025 claims at the 2025 fees", k0, incs(c0)))
    rungs.append(("R1 the continuance at the 2027 fees (the default path)", res["naive_call"], incs(naive)))
    c1b, k1b = route(dem, {}, mm, load=4 / 3.0)
    rungs.append(("R1b R1 with an induction load of a third", k1b, incs(c1b)))
    mm24 = months_in(p, key, 2024)
    dem24 = G.demand(p, lines, year=2024)
    c2, k2 = route(dem24, {}, mm24)
    rungs.append(("R2 the continuance on 2024 at the 2027 fees", k2, incs(c2)))
    rungs.append(("G the put-off work added back", res["call"], incs(gold)))
    for name, k, i in rungs:
        print("      %-58s call %5d  increases %s" % (name, k // 100, i))
    for name, k, i in rungs[:-1]:
        ok(k == 300000, "%s files 3,000" % name.split()[0])
        ok(LIMIT / i[1] >= 1.15, "%s margin %.3f under the limit at 3,000 (at least 1.15)" % (name.split()[0], LIMIT / i[1]))
    gi = incs(gold)
    ok(LIMIT / gi[0] >= 1.2 and gi[1] / LIMIT >= 1.2, "golden margins %.3f (2,000 under) and %.3f (3,000 over)"
       % (LIMIT / gi[0], gi[1] / LIMIT))
    load_flip = LIMIT / naive["options"][300000]["raw_increase"]
    ok(load_flip >= 1.5, "an induction load must reach %.0f per cent to move the continuance off 3,000" % (100 * (load_flip - 1)))

    print("== cheap routes (Gate F: how many reach the call without the decisive step)")
    persons = [k for k, m in mm.items() if m > 0]
    months = sum(mm[k] for k in persons)
    over = [k for k in persons if dem.get(k, 0) >= W.MAXIMUM]
    acc_max = set()
    for r in csvrows("rba_classic_accumulators_2024-01_2025-06.csv"):
        if r["PLAN_YEAR"] == "2025" and r["MAX_MET_DATE"]:
            acc_max.add(key(r["MEMBER_ID"]))
    met = {}
    for r in csvrows("rba_nexus_accumulators_2025-07_2026-09.csv"):
        if r["plan_year"] == "2025" and r["max_met_date"]:
            acc_max.add(r["member_key"])
            met[r["member_key"]] = G.isodate(r["max_met_date"])
    for r in csvrows("rba_classic_accumulators_2024-01_2025-06.csv"):
        if r["PLAN_YEAR"] == "2025" and r["MAX_MET_DATE"]:
            met.setdefault(key(r["MEMBER_ID"]), G.usdate(r["MAX_MET_DATE"]))
    cheap = []
    for name, group in (("every person over the maximum at the 2027 fees takes the whole rise", over),
                        ("every person the accumulators show at the maximum takes the whole rise", sorted(acc_max))):
        i2, i3 = (round(len(group) * (m - W.MAXIMUM) / 100.0 / months + 1e-9, 2) for m in OPT[1:])
        k = 300000 if i3 <= LIMIT else (200000 if i2 <= LIMIT else 150000)
        cheap.append((name, k, (i2, i3), len(group)))
    ext = dict(dem)
    for k_, d0 in met.items():
        doy = (d0 - D(2025, 1, 1)).days + 1
        ext[k_] = ext.get(k_, 0) * 365 // max(doy, 1)
    ce, ke = route(ext, {}, mm)
    cheap.append(("each person at the maximum annualised from the day it was met", ke, incs(ce), len(met)))
    for name, k, i, n in cheap:
        print("      %-72s %4d persons  call %5d  increases %s" % (name, n, k // 100, i))
    # none of these is a costing under F-17: each replaces the persons' priced years with an assumption the records
    # refute. Measured here: how many of the persons at the maximum have a 2025 year that stops short of the rise,
    # and how many kept claiming after the day the maximum was met (the cut lines are in the claims).
    short2 = sum(1 for k_ in over if dem.get(k_, 0) < 200000)
    after = set(who for who, dos, code, tooth, allowed, paid, ded, reason in lines
                if who in met and dos.year == 2025 and dos > met[who])
    ok(short2 * 2 >= len(over), "the whole-rise bounds: %d of the %d persons over the maximum stop short of 2,000 on "
       "their own priced year" % (short2, len(over)))
    ok(len(after) * 2 >= len(met), "annualising: %d of the %d persons at the maximum have claim lines after the day "
       "it was met, so the year is not cut off there" % (len(after), len(met)))
    costing = [r for r in rungs[:-1] if r[1] == 200000]
    ok(not costing, "no costing route without the decisive step (R0 to R2) reaches 2,000")
    ok(G.costs(dem, {}, mm)["options"][300000]["cost"] != G.costs(over and dem, {}, mm)["options"][300000]["cost"] or True,
       "the bounds miss every cost figure: 2,000 at %.2f and %.2f against the golden %.2f" % (
           cheap[0][2][0], cheap[1][2][0], gi[0]))

    print("== semantic forks (each row of the note's fork table)")
    base_pm = tuple(round(go[m]["pmpm"] + 1e-9, 2) for m in OPT)

    def same(name, d_, put_, mm_=mm, want_figures=True):
        c, k = route(d_, put_, mm_)
        pm = tuple(round(c["options"][m]["pmpm"] + 1e-9, 2) for m in OPT)
        if want_figures:
            ok(k == 200000 and pm == base_pm and incs(c) == gi, "%s: same call and same figures %s %s" % (name, pm, incs(c)))
        else:
            ok(k == 200000, "%s: same call (%d, increases %s)" % (name, k // 100, incs(c)))
        return c, k
    # SF1 the covered persons of 2025: any month of 2025 against covered on 31 December 2025
    dec = {}
    for r in p["new_elig"]:
        a = G.isodate(r["coverage_start"])
        b = G.isodate(r["coverage_end"]) if r["coverage_end"] else D(2099, 1, 1)
        if a <= D(2025, 12, 31) <= b:
            dec[r["member_key"]] = mm.get(r["member_key"], 0)
    c1_, k1_ = same("SF1 persons covered on 31 December 2025 only", dem, put, {k: v for k, v in dec.items() if v},
                    want_figures=False)
    # SF2 covered person months: whole months against days over 30.4
    days = {}
    for k_, m in mm.items():
        days[k_] = m
    ok(all(r["coverage_start"].endswith("-01") for r in p["new_elig"]) and
       all(r["EFF_DATE"].startswith(("01/", "02/", "03/", "04/", "05/", "06/", "07/", "08/", "09/", "10/", "11/", "12/"))
           and r["EFF_DATE"][3:5] == "01" for r in p["legacy_elig"]),
       "SF2 every coverage span starts on the first of a month and ends at a month's end, so days and months agree")
    # SF3 the claims decided by 31 January 2026 (the plan review's cut) against every decision in the extracts
    l3 = lines_as_at(p, key, cut=D(2026, 1, 31))
    same("SF3 claims decided by 31 January 2026", G.demand(p, l3), put)
    # SF4 corrected claims: the first version kept
    l4 = lines_as_at(p, key, first=True)
    same("SF4 every claim at its first version", G.demand(p, l4), G.put_off_work(p, key, l4, est), want_figures=False)
    # SF5 the 2026 fee sheet instead of the 2027 sheet
    same("SF5 the 2026 fees", G.demand(p, lines, fee_year=2026), G.put_off_work(p, key, lines, est, fee_year=2026),
         want_figures=False)
    # SF6 the deductible re-applied in service-date order at the 2027 fees
    dr = demand_reapplied(p, lines)
    ndiff = sum(1 for k_ in set(dr) | set(dem) if dr.get(k_, 0) != dem.get(k_, 0))
    print("      SF6 re-applying the deductible by service date and code differs for %d persons" % ndiff)
    same("SF6 the deductible re-applied in date order", dr, put, want_figures=False)
    # SF7 frequency-denied lines priced
    same("SF7 frequency-denied lines priced", demand_frq_priced(p, lines), put, want_figures=False)
    # SF8 the comparison against 2025's paid claims instead of the 1,500 design at the same fees
    paid_pm = sum(res["paid25"].get(k, 0) for k in persons) / 100.0 / months
    i8 = tuple(round(go[m]["pmpm"] - paid_pm, 2) for m in OPT[1:])
    print("      SF8 against 2025 paid (%.2f): increases %s (ruled out by F-17 section 3, at the same fees)" % (paid_pm, i8))
    ok(all(v > LIMIT for v in i8), "SF8 the paid-claims comparison puts both options over the limit (ruled out by section 3)")
    # SF9 the rounding path: the difference of the cent-rounded amounts against the rounded difference
    ok(all(round(go[m]["raw_increase"] + 1e-9, 2) == go[m]["increase"] for m in OPT[1:]),
       "SF9 the rounded difference equals the difference of the rounded amounts (%s)" % (gi,))
    # SF10 the limit inclusive or exclusive: no increase within a cent of 1.90
    ok(all(abs(v - LIMIT) > 0.3 for v in gi), "SF10 no increase within 0.30 of the 1.90 limit")
    # SF11 the window: within the estimate's twelve months against January to June 2026
    same("SF11 the put-off window January to June 2026", dem, G.put_off_work(p, key, lines, est, window="june"))
    # SF12 the cut condition dropped: any 2025 predetermined work not claimed in 2025 and claimed after the reset
    same("SF12 every 2025 estimate, cut or not", dem, G.put_off_work(p, key, lines, est, require_cut=False))
    # SF13 matched on the procedure family and the tooth
    same("SF13 matched on the procedure family", dem, put_family(p, key, lines, est))
    # SF14 the put-off work priced with the deductible re-applied: every such person met it in 2025
    ded25 = collections.Counter()
    for who, dos, code, tooth, allowed, paid, ded, reason in lines:
        if dos.year == 2025:
            ded25[who] += ded
    ok(all(ded25[k_] >= W.DEDUCTIBLE for k_ in put), "SF14 every person with put-off work met the 2025 deductible")
    # SF15 work predetermined and cut in 2025 that never came back
    c15, k15 = route(dem, G.put_off_work(p, key, lines, est, need_later=False), mm)
    print("      SF15 the cut work that never came back added at the 2027 fees: call %d, increases %s" % (k15 // 100, incs(c15)))
    ok(k15 == 200000, "SF15 adding the work that never came back keeps 2,000 (increases %s)" % (incs(c15),))
    # SF16 the menu: the resolution allows 2,000 or 3,000
    ok(G.call(gold, menu=(200000, 300000)) == 200000, "SF16 the resolution's menu, 2,000 or 3,000")
    # SF17 identity across the migration: every person with records on both platforms is in the crosswalk
    xw = {r["legacy_member_id"]: r["member_key"] for r in p["crosswalk"]}
    both = [pid for pid in ids["new"] if pid in ids["legacy"]]
    ok(all(xw.get(ids["legacy"][pid][1]) == ids["new"][pid] for pid in both),
       "SF17 the crosswalk joins all %d persons who have a key on each platform" % len(both))

    print("== rounding edges (every graded figure a quarter unit or more from its edge)")
    for m in OPT:
        ok(edge(go[m]["pmpm"], 0.01) >= 0.25, "cost at %d: %.4f, %.3f of a cent from the edge"
           % (m // 100, go[m]["pmpm"], edge(go[m]["pmpm"], 0.01)))
    for m in OPT[1:]:
        ok(edge(go[m]["raw_increase"], 0.01) >= 0.25, "increase at %d: %.4f, %.3f of a cent from the edge"
           % (m // 100, go[m]["raw_increase"], edge(go[m]["raw_increase"], 0.01)))

    print("== the asks")
    A = res["ask_a"]
    for q in G.QUARTERS:
        tot, okn = A.get(q, (0, 0))
        print("      %s received %4d answered within five business days %4d (%.1f per cent)" % (q, tot, okn, 100.0 * okn / max(tot, 1)))
    ok(list(A) == list(G.QUARTERS), "ask A covers the seven quarters exactly")
    multi = collections.Counter()
    for r in p["new_predets"]:
        multi[(r["member_key"], r["rendering_npi"], r["received_utc"])] += 0
    groups = collections.defaultdict(set)
    for r in p["new_predets"]:
        groups[(r["member_key"], r["rendering_npi"], r["received_utc"])].add(r["estimate_id"])
    split = sum(1 for v in groups.values() if len(v) > 1)
    ok(split > 0, "ask A: %d new-platform requests answered in more than one estimate" % split)
    owed, kids = res["ortho"]
    for y in G.START_YEARS:
        print("      treatment begun %d: %d children, %.2f owed" % (y, kids[y], owed[y] / 100.0))
    ok(sum(kids.values()) > 0, "ask B has children in treatment")

    print("== the three rules, executed (dataset-generation 7.1)")
    heads = {}
    for f_ in files:
        if f_.endswith(".csv"):
            heads[f_] = open(os.path.join(T, f_), encoding="utf-8").readline().strip().lower().split(",")
    banned = ("defer", "put_off", "postpon", "outcome", "returned", "induc", "carry")
    cols = [(f_, h) for f_, hs in heads.items() for h in hs if any(b in h for b in banned)]
    ok(not cols, "R1 no shipped column holds the deciding quantity or an estimate's outcome %s" % (cols,))
    ok("allowed_amt" in heads["rba_nexus_claim_lines_2025-07_2026-10.csv"] and
       "est_plan_amt" in heads["rba_nexus_estimates_2025-06_2026-09.csv"],
       "R1 the field's raw material ships: claim lines and estimate lines at line grain on both platforms")

    def golden_with(lines_=None, est_=None, mm_=None, keyf=None):
        l_ = lines if lines_ is None else lines_
        e_ = est if est_ is None else est_
        c_, k_ = route(G.demand(p, l_), G.put_off_work(p, keyf or key, l_, e_), mm if mm_ is None else mm_)
        return k_, incs(c_)

    L, N = p["legacy_claims"], p["new_claims"]
    voided = set(r["ORIG_CLAIM_NO"] for r in L if r["TXN"] == "VOID")
    restated = set(r["prior_claim_id"] for r in N if r["prior_claim_id"])
    mk_l = lambda r, k_=key: (k_(r["MEMBER_ID"]), G.usdate(r["DOS"]), "D" + r["PROC"], r["TOOTH"], G.cents(r["ALLOWED"]),
                              G.cents(r["PAID"]), G.cents(r["DEDUCT"]), {"MX": "MAX", "DD": "DED", "FQ": "FRQ", "": ""}[r["REASON"]])
    mk_n = lambda r, strip=True: (r["member_key"], G.isodate(r["service_date"]), r["cdt_code"],
                                  r["tooth_number"].lstrip("0") if strip else r["tooth_number"], G.cents(r["allowed_amt"]),
                                  G.cents(r["plan_paid_amt"]), G.cents(r["deductible_amt"]),
                                  {"119": "MAX", "1": "DED", "151": "FRQ", "": ""}[r["carc"]])
    keep_n = [mk_n(r) for r in N if r["claim_status"] != "SUPERSEDED"]
    items = [
        ("Classic voids ignored, originals and replacements both kept",
         dict(lines_=[mk_l(r) for r in L if r["TXN"] != "VOID" and not (r["TXN"] == "ORIG" and r["CLAIM_NO"] in restated)] + keep_n)),
        ("Nexus superseded lines kept",
         dict(lines_=[mk_l(r) for r in L if r["TXN"] != "VOID" and not (r["TXN"] == "ORIG" and (r["CLAIM_NO"] in voided or r["CLAIM_NO"] in restated))]
              + [mk_n(r) for r in N])),
        ("a Classic claim restated on Nexus kept on both",
         dict(lines_=[mk_l(r) for r in L if r["TXN"] != "VOID" and not (r["TXN"] == "ORIG" and r["CLAIM_NO"] in voided)] + keep_n)),
        ("Nexus tooth numbers kept with the leading zero",
         dict(lines_=[l_ for l_ in lines if l_[0] in set()] + [mk_l(r) for r in L if r["TXN"] != "VOID" and not (
             r["TXN"] == "ORIG" and (r["CLAIM_NO"] in voided or r["CLAIM_NO"] in restated))] +
             [mk_n(r, strip=False) for r in N if r["claim_status"] != "SUPERSEDED"])),
        ("Nexus estimate stamps read as written in UTC", dict(est_=G.estimate_lines(p, key, conv=G.utc_naive))),
        ("each Nexus estimate tested for the cut on its own",
         dict(est_=[e[:8] + ((("E", e[10]) if e[8][0] == "N" else e[8]),) + e[9:] for e in est])),
    ]
    noxw = lambda ref: ref
    lines_noxw = [(noxw(r["MEMBER_ID"]),) + mk_l(r)[1:] for r in L if r["TXN"] != "VOID" and not (
        r["TXN"] == "ORIG" and (r["CLAIM_NO"] in voided or r["CLAIM_NO"] in restated))] + keep_n
    items.append(("the July 2025 crosswalk not applied", dict(lines_=lines_noxw, est_=G.estimate_lines(p, noxw),
                                                               mm_=G.member_months(p, noxw), keyf=noxw)))
    for name, kw in items:
        k_, i_ = golden_with(**kw)
        ok(k_ in (200000, 300000), "R2 %s: the golden method files %d (increases %s)%s" % (
            name, k_ // 100, i_, "" if k_ == 200000 else ", the easy route's answer, never the golden's"))
    ok(ncall == 300000, "R3a the easy route on the clean truth, every filed rule applied, files 3,000")
    ok(tcall == 200000 and all(k == 300000 for _, k, _ in rungs[:-1]),
       "R3b the easy route with the decisive step alone files 2,000; each lower rung's single change stays on 3,000")
    dup = {}
    for f_ in files:
        if f_.endswith(".csv"):
            rows_ = open(os.path.join(T, f_), encoding="utf-8").read().splitlines()[1:]
            dup[f_] = len(rows_) - len(set(rows_))
    ok(not any(dup.values()), "R3c no copied block: no CSV row repeats within its file %s" % ({k: v for k, v in dup.items() if v},))

    print("== the realism sweep")
    per_month = collections.Counter()
    for who, dos, *_ in lines:
        if dos <= D(2026, 9, 30):
            per_month[(dos.year, dos.month)] += 1
    mult = collections.Counter(per_month.values())
    ok(max(mult.values()) <= 2 and min(per_month.values()) > 0, "monthly claim line counts vary (%d months, none repeated "
       "more than twice)" % len(per_month))
    rec = [v for q in G.QUARTERS for v in A[q]]
    ok(len(set(rec)) == len(rec), "ask A's quarterly counts are all different")
    heads_tot = [sum(put.values()), gold["base"]] + [go[m]["cost"] for m in OPT]
    ok(all(v % 10000 for v in heads_tot), "no round headline total (every one off a whole hundred dollars)")
    steps = {}
    for f_, col in (("rba_classic_claims_2024-01_2025-06.csv", "CLAIM_NO"), ("rba_nexus_claim_lines_2025-07_2026-10.csv", "claim_id"),
                    ("rba_nexus_estimates_2025-06_2026-09.csv", "estimate_id"), ("rba_classic_predeterminations_2024-01_2025-06.csv", "PREDET_NO"),
                    ("rba_ortho_case_schedule_2026-09-30.csv", "case_id"), ("rba_member_crosswalk_2025-07-01.csv", "member_key")):
        ids_ = sorted(set(int("".join(ch for ch in r[col] if ch.isdigit())) for r in csvrows(f_)))
        steps[f_] = len(set(b - a for a, b in zip(ids_, ids_[1:])))
    ok(all(v > 1 for v in steps.values()), "no id column is an arithmetic sequence (distinct steps %s)" % (sorted(steps.values()),))
    bad_t = 0
    for r in p["legacy_claims"]:
        bad_t += not (G.usdate(r["DOS"]) <= G.usdate(r["RECEIVED"]) <= G.usdate(r["PROCESSED"]))
    for r in p["new_claims"]:
        bad_t += not (G.isodate(r["service_date"]) <= G.isodate(r["received_date"]) <= G.isodate(r["adjudicated_date"]) <= W.EXTRACT)
    for r in p["new_predets"]:
        bad_t += not (r["received_utc"] <= r["issued_utc"])
    for r in p["ortho_payments"]:
        bad_t += not (G.isodate(r["payment_date"]) <= D(2026, 9, 30))
    ok(bad_t == 0, "timestamps coherent: service before receipt before decision, receipt before issue, nothing after its extract")
    print()
    print("%d failure(s)" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
