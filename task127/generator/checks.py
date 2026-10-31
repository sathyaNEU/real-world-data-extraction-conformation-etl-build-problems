"""Assertions on the built pack: the golden split and its rungs with their margins, every semantic fork row (SF1 to
SF14), the clearance, the data facts the counterfactual rests on, the separation of the ask devices from the main
call's rows, every ask stop and the cracker's and the mirror's sheets, the deliverables, the realism sweep, the
distractors' deletion test and the input gates."""
import collections
import csv
import datetime as dt
import os
import re
import shutil
import tempfile
from fractions import Fraction

import analysis as AN
import core
import golden as GD
import pack as P
import records as RC
import world as W

N = [0]
HALF = Fraction(1, 2)


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def whole(x):
    return int(x + HALF)


GOLD = {"RMC01": 508, "RMC02": 350, "RSM03": 120, "RSM02": 222, "RSM01": 0}


def main_call(F):
    M = F["M"]
    ok(M["packages"] == GOLD, "golden split %s" % M["packages"])
    ok(M["order"] == ["RMC01", "RMC02", "RSM03", "RSM02", "RSM01"], "golden order %s" % M["order"])
    ok(M["none"] == ["RSM01"], "Ashby Vale gets none")
    ok(sum(M["packages"].values()) == AN.FUND, "all 1,200 placed")
    ok(sum(M["caps"].values()) > AN.FUND, "the covered patients outnumber the packages")
    v = M["val"]
    ok(v["RSM03"] / v["RSM02"] >= Fraction(6, 5), "Holmford over Cleeve Park by 1.2x (%.3f)" % float(v["RSM03"] / v["RSM02"]))
    ok(v["RSM02"] / v["RSM01"] >= Fraction(6, 5), "Cleeve Park over Ashby Vale by 1.2x (%.3f)" % float(v["RSM02"] / v["RSM01"]))
    ok(v["RMC02"] / v["RSM02"] >= Fraction(6, 5), "Wendlebury over Cleeve Park by 1.2x")
    for s in core.SITES:
        if 0 < M["packages"][s] < M["caps"][s]:
            x = M["bed"][s]
            ok(Fraction(1, 5) <= x - int(x) <= Fraction(4, 5), "part-filled hospital mid-bin (%s)" % float(x))
            for nd in (2, 3):
                ok(whole(Fraction(round(float(v[s]), nd)).limit_denominator(10 ** nd) * M["packages"][s]) == whole(x),
                   "rounding the value to %d places first gives the same bed-days" % nd)
        else:
            ok(M["bed"][s].denominator == 1, "a full or empty hospital's bed-days are whole")
    ok(whole(M["total"]) == sum(whole(M["bed"][s]) for s in core.SITES), "total from unrounded equals sum of rounded")


def ladder(F):
    M = F["M"]
    a, r = M["alloc"], M["rungs"]
    top = lambda k: max(core.SITES, key=lambda s: r[k][s])
    ok(top("R0") == "RSM01" and a["R0"]["RSM01"] == M["caps"]["RSM01"], "R0 fills Ashby Vale first and full")
    ok(top("R1") == "RSM01" and a["R1"]["RSM01"] == M["caps"]["RSM01"], "R1 (default) fills Ashby Vale first and full")
    ok(r["R1"]["RSM01"] / r["R1"]["RSM02"] >= Fraction(21, 20), "R1: Ashby Vale over Cleeve Park")
    ok(a["R1"]["RSM02"] == M["caps"]["RSM02"] and a["R1"]["RSM03"] == 0, "R1 fills Cleeve Park and leaves Holmford out")
    ok(a["R0"] != a["R1"] != M["packages"], "R0, R1 and the golden are three allocations")
    ok(a["NE"]["RSM01"] == M["caps"]["RSM01"], "the no-equipment average fills Ashby Vale")
    # the over-correction (equipment patients at nought) fills Cleeve Park and leaves Wendlebury short
    ok(a["OC"]["RSM02"] == M["caps"]["RSM02"] and 0 < a["OC"]["RMC02"] < M["caps"]["RMC02"],
       "the over-correction fills Cleeve Park and part-fills Wendlebury (%s)" % a["OC"])
    oc = M["rungs"]["OC"]
    ok(oc["RSM02"] / oc["RMC02"] >= Fraction(6, 5) and oc["RMC02"] / oc["RSM01"] >= Fraction(6, 5),
       "the over-correction's deciding boundaries are 1.2x apart")
    ok(all(whole(M["rung_bed"]["OC"][s]) != whole(M["bed"][s]) for s in core.SITES if M["packages"][s]),
       "the over-correction misses every hospital's bed-days")
    # every rung's bed-days total misses the golden's
    for k in ("R0", "R1", "OC", "NE"):
        ok(whole(sum(M["rung_bed"][k].values())) != whole(M["total"]), "rung %s total differs" % k)
    # shared figures with the default path: only Wendlebury's 350 packages
    shared = [s for s in core.SITES if a["R1"][s] == M["packages"][s]]
    ok(shared == ["RMC02"], "the default path shares only Wendlebury's packages (%s)" % shared)


def control_reflex(target, F):
    """Restart patients (care already in place) as a control: subtract their average nights. Lands on Ashby Vale."""
    mp = AN.marchshire_practices(target)
    st, sr = collections.Counter(), collections.Counter()
    nt, nr = collections.Counter(), collections.Counter()
    for r in AN.spells(target):
        if (r["discharge_pathway"] == "1" and AN.W0 <= AN.d(r["discharge_ready_date"]) <= AN.W1
                and r["gp_practice_code"] in mp and r["site_code"] in core.SITES):
            dl = (AN.d(r["discharge_datetime"]) - AN.d(r["discharge_ready_date"])).days
            if r["p1_care_package"] == "New package":
                nt[r["site_code"]] += 1
                st[r["site_code"]] += dl
            else:
                nr[r["site_code"]] += 1
                sr[r["site_code"]] += dl
    v = {s: Fraction(st[s], nt[s]) - Fraction(sr[s], nr[s]) for s in core.SITES}
    o, a = AN.allocate(v, F["M"]["caps"])
    ok(o[0] == "RSM01" and a["RSM01"] == F["M"]["caps"]["RSM01"], "the restart-control reflex fills Ashby Vale")
    return a


def facts(target, F):
    """What the counterfactual rests on, from the shipped files."""
    eq = AN.discharge_orders(target)
    mp = AN.marchshire_practices(target)
    sp = AN.spells(target)
    n_rs = n_rs_eq = n_new_eq = 0
    for r in sp:
        if r["discharge_pathway"] != "1" or r["gp_practice_code"] not in mp:
            continue
        R, D = AN.d(r["discharge_ready_date"]), AN.d(r["discharge_datetime"])
        E = eq.get((r["nhs_number"], R))
        E = min(E) if E else None
        if E:
            ok(E <= D, "no discharge before the equipment arrives (%s)" % r["spell_number"])
        if r["p1_care_package"] != "New package":
            n_rs += 1
            n_rs_eq += E is not None
            ok(D == max(R, E or R), "a restart patient leaves on the later of ready and delivery (%s)" % r["spell_number"])
        else:
            n_new_eq += E is not None
    ok(n_rs_eq >= 200, "restart patients waiting for equipment on file (%d)" % n_rs_eq)
    ok(n_new_eq >= 2000, "new-package patients with discharge equipment (%d)" % n_new_eq)
    cov = AN.covered(target)
    ok(len({r["nhs_number"] for r in cov}) == len(cov), "one covered spell per patient")
    ok(all(r["site_code"] in core.SITES for r in cov), "covered spells end at the five hospitals")
    # the brokerage holds one hospital referral for every Marchshire new-package discharge, none for a restart
    refs = collections.Counter()
    for r in AN._rows(target, P.FILES["brokerage"]):
        if r["source"] == "Hospital discharge":
            refs[r["nhs_number"].replace(" ", "")] += 1
    new = collections.Counter(r["nhs_number"] for r in sp if r["discharge_pathway"] == "1"
                              and r["p1_care_package"] == "New package" and r["gp_practice_code"] in mp)
    ok(refs == new, "hospital referrals match new-package discharges person for person")
    # every equipment join a reader might write gives the same nights: any delivery to the person on or before the
    # discharge date, or between admission and discharge
    lines = collections.defaultdict(list)
    for r in AN._rows(target, P.FILES["ices"]):
        if r["delivered_date"]:
            lines[r["nhs_number"].replace(" ", "")].append((AN.d(r["delivered_date"]), r["route"]))
    for r in cov:
        R, D, A = AN.d(r["discharge_ready_date"]), AN.d(r["discharge_datetime"]), AN.t(r["admission_datetime"])
        E = eq.get((r["nhs_number"], R))
        g = max(0, (D - max(R, min(E) if E else R)).days)
        before = [x for x, _ in lines[r["nhs_number"]] if x <= D]
        g1 = max(0, (D - max([R] + ([max(before)] if before else []))).days)
        inside = [x for x, _ in lines[r["nhs_number"]] if A.date() <= x <= D]
        g2 = max(0, (D - max([R] + inside)).days)
        ok(g == g1 == g2, "equipment joins converge (%s)" % r["spell_number"])
    return n_rs, n_rs_eq


def edges(target, F):
    """The judge's residual forks closed by construction: no discharge order placed before admission (so every
    join on the stay's dates agrees), and no midnight falls between two ward stays."""
    eq_rows = [r for r in AN._rows(target, P.FILES["ices"]) if r["route"] == "Hospital discharge"]
    adm = {}
    for r in AN.spells(target):
        adm.setdefault(r["nhs_number"], []).append((AN.t(r["admission_datetime"]).date(), AN.d(r["discharge_datetime"]),
                                                    AN.d(r["discharge_ready_date"])))
    for r in eq_rows:
        stays = [s for s in adm[r["nhs_number"].replace(" ", "")] if s[2] == AN.d(r["required_by"])]
        ok(len(stays) == 1 and AN.d(r["ordered_date"]) >= stays[0][0], "discharge order placed during the stay (%s)"
           % r["order_no"])
    ws = AN.ward_stays(target)
    gaps = 0
    for k, v in ws.items():
        for (a1, b1, w1), (a2, b2, w2) in zip(v, v[1:]):
            m = dt.datetime(b1.year, b1.month, b1.day)
            if b1 > m:
                m += dt.timedelta(1)
            gaps += a2 > b1 and a2 > m
    ok(gaps == 0, "no midnight, a stay's end on one included, falls between two ward stays (%d)" % gaps)
    # so a strict point-in-time join (the ward whose stay holds the midnight) gives every Ask A cell
    strict = {(s, mo): 0 for s in core.SITES for mo in core.ASK_MONTHS}
    so = AN.ward_sites(target)
    for r in AN.spells(target):
        R, D = AN.d(r["discharge_ready_date"]), AN.d(r["discharge_datetime"])
        stays = ws.get((r["provider_code"], r["spell_number"]), [])
        n = R
        while n < D:
            mid = dt.datetime(n.year, n.month, n.day) + dt.timedelta(1)
            hold = [w for a, b, w in stays if a <= mid < b]
            if hold and (so[hold[0]], (n.year, n.month)) in strict:
                strict[(so[hold[0]], (n.year, n.month))] += 1
            n += dt.timedelta(1)
    ok(strict == F["A"], "a strict point-in-time join of nights to wards gives every Ask A bed-day cell")
    # the strict join (orders placed on or after admission, delivered by discharge) gives the golden
    eq = {}
    for r in eq_rows:
        if r["delivered_date"]:
            eq.setdefault(r["nhs_number"].replace(" ", ""), []).append((AN.d(r["ordered_date"]), AN.d(r["delivered_date"])))
    tot = {s: 0 for s in core.SITES}
    for r in AN.covered(target):
        A, R, D = AN.t(r["admission_datetime"]).date(), AN.d(r["discharge_ready_date"]), AN.d(r["discharge_datetime"])
        E = [dl for o, dl in eq.get(r["nhs_number"], []) if o >= A and dl <= D]
        tot[r["site_code"]] += max(0, (D - max([R] + E)).days)
    ok(tot == F["M"]["save"], "the strict equipment join gives the golden nights")


def semantic_forks(target, F):
    M = F["M"]
    eq = AN.discharge_orders(target)
    sp = AN.spells(target)
    mp = AN.marchshire_practices(target)
    base = lambda r: r["discharge_pathway"] == "1" and r["site_code"] in core.SITES

    def G(r):
        R, D = AN.d(r["discharge_ready_date"]), AN.d(r["discharge_datetime"])
        E = eq.get((r["nhs_number"], R))
        return max(0, (D - max(R, min(E) if E else R)).days)

    def split(rows, f=G, caps=None):
        c, s = collections.Counter(), collections.Counter()
        for r in rows:
            c[r["site_code"]] += 1
            s[r["site_code"]] += f(r)
        v = {x: Fraction(s[x], c[x]) for x in core.SITES}
        return AN.allocate(v, caps or dict(c))[1]

    inwin = lambda r: AN.W0 <= AN.d(r["discharge_ready_date"]) <= AN.W1
    # SF1 the packages each hospital should get: the bed-day-maximising split; a split in proportion to need is not
    prop = {s: AN.FUND * M["save"][s] / sum(M["save"].values()) for s in core.SITES}
    ok(any(abs(prop[s] - M["packages"][s]) >= 20 for s in core.SITES), "SF1 the proportional split is another call")
    ok(sum(M["packages"][s] * M["val"][s] for s in core.SITES) > sum(Fraction(round(prop[s])) * M["val"][s]
                                                                      for s in core.SITES),
       "SF1 the greedy split frees more than the proportional one")
    # SF2 bed-days freed are packages times value; the best patients' nights at the part-filled hospital differ
    cov = AN.covered(target)
    gs = sorted((G(r) for r in cov if r["site_code"] == "RSM02"), reverse=True)
    ok(sum(gs[:M["packages"]["RSM02"]]) != whole(M["bed"]["RSM02"]), "SF2 top-k nights differ from packages x value")
    # SF3 covered: registration in Marchshire, a new package, the ready date in the window
    rs = [r for r in sp if base(r) and r["gp_practice_code"] in mp and inwin(r)]
    ok(split(rs) != M["packages"], "SF3 counting restarts gives another call")
    act = {r["practice_code"] for r in AN._rows(target, P.FILES["practices"]) if "Marchshire" in r["icb"]
           and r["status"] == "Active"}
    ac = [r for r in cov if r["gp_practice_code"] in act]
    ok(len(ac) == len(cov) and split(ac) == M["packages"],
       "SF3 dropping the merged practices' codes gives the same call (no covered spell carries a retired code)")
    outs = {r["postcode"].split()[0] for r in AN._rows(target, P.FILES["postcodes"])}
    res = [r for r in sp if base(r) and r["p1_care_package"] == "New package" and r["postcode_district"] in outs
           and inwin(r)]
    ok(len(res) > len(cov) and split(res) != M["packages"], "SF3 residence by outward code gives another call")
    # SF4 the window is by the ready date
    dd = [r for r in sp if base(r) and r["p1_care_package"] == "New package" and r["gp_practice_code"] in mp
          and AN.W0 <= AN.d(r["discharge_datetime"]) <= AN.W1]
    ok(split(dd) != M["packages"], "SF4 the window by discharge date gives another call")
    # SF5 nights are whole nights; fractional days keep the packages and move the bed-days
    def Gh(r):
        R, Dt = AN.d(r["discharge_ready_date"]), AN.t(r["discharge_datetime"])
        E = eq.get((r["nhs_number"], R))
        st = max(R, min(E) if E else R)
        return max(0.0, (Dt - dt.datetime(st.year, st.month, st.day)).total_seconds() / 86400)
    c, s = collections.Counter(), collections.Counter()
    for r in cov:
        c[r["site_code"]] += 1
        s[r["site_code"]] += Gh(r)
    vh = {x: s[x] / c[x] for x in core.SITES}
    ok(AN.allocate(vh, M["caps"])[1] == M["packages"], "SF5 fractional days keep the packages")
    ok(all(round(vh[x] * M["packages"][x]) != whole(M["bed"][x]) for x in core.SITES if M["packages"][x]),
       "SF5 fractional days move every bed-day figure")
    # SF6 the average is over every covered patient, helped or not
    c2, s2 = collections.Counter(), collections.Counter()
    for r in cov:
        g = G(r)
        if g:
            c2[r["site_code"]] += 1
            s2[r["site_code"]] += g
    ok(AN.allocate({x: Fraction(s2[x], c2[x]) for x in core.SITES}, M["caps"])[1] != M["packages"],
       "SF6 averaging over helped patients only gives another call")
    # SF7 the cap: covered patients equal covered spells (one spell per patient)
    ok(len({r["nhs_number"] for r in cov}) == len(cov), "SF7 patients and spells agree")
    # SF8 the equipment date is the delivery, not the required-by date (required-by is the ready date)
    ok(split(cov, lambda r: (AN.d(r["discharge_datetime"]) - AN.d(r["discharge_ready_date"])).days) == M["alloc"]["R1"],
       "SF8 the required-by date (the ready date) returns the default path")
    # SF9 duplicate submissions: covered spells carry one submission each
    allrows = AN.spells(target, dedup=False)
    sub = collections.Counter((r["provider_code"], r["spell_number"]) for r in allrows)
    ok(all(sub[(r["provider_code"], r["spell_number"])] == 1 for r in cov), "SF9 no covered spell was resubmitted")
    # SF10 the five hospitals: no covered spell moved site
    ws = AN.ward_stays(target)
    so = AN.ward_sites(target)
    ok(all({so[w] for _, _, w in ws[(r["provider_code"], r["spell_number"])]} == {r["site_code"]} for r in cov),
       "SF10 every covered patient stayed at one hospital")
    # SF11 rounding path: asserted in main_call; SF12 the order has no ties
    # SF12 tie-break: only an order that decides packages matters; the two filled leaders may swap freely
    o = M["order"]
    ok(M["val"][o[2]] / M["val"][o[3]] >= Fraction(6, 5) and M["val"][o[3]] / M["val"][o[4]] >= Fraction(6, 5),
       "SF12 the boundaries that decide packages are 1.2x apart")
    for i in range(len(o) - 1):
        sw = o[:i] + [o[i + 1], o[i]] + o[i + 2:]
        left, alt = AN.FUND, {}
        for s in sw:
            alt[s] = min(left, M["caps"][s])
            left -= alt[s]
        if M["val"][o[i]] / M["val"][o[i + 1]] < Fraction(6, 5):
            ok(alt == M["packages"], "SF12 swapping %s and %s moves nothing" % (o[i], o[i + 1]))
    # SF13 "last winter" for the basis is 1 December 2025 to 28 February 2026 inclusive: nothing on either edge moves
    edge = [r for r in sp if base(r) and r["p1_care_package"] == "New package" and r["gp_practice_code"] in mp
            and AN.d(r["discharge_ready_date"]) in (AN.W0, AN.W1)]
    ok(len(edge) > 0, "SF13 patients sit on the window's edges (the window is inclusive by its wording)")
    # SF14 medically optimised = the discharge ready date column (one date per spell, never blank)
    ok(all(r["discharge_ready_date"] for r in sp), "SF14 every spell carries a discharge ready date")
    # SF15 a package is "up to four weeks of home care ... available from the day a patient is medically optimised":
    # every covered patient's equipment arrived within four weeks of the ready date, so a package running from the
    # ready date is still running when the patient can leave, on any reading of the four weeks
    lags = [(min(eq[(r["nhs_number"], AN.d(r["discharge_ready_date"]))]) - AN.d(r["discharge_ready_date"])).days
            for r in cov if (r["nhs_number"], AN.d(r["discharge_ready_date"])) in eq]
    ok(max(lags) < 28, "SF15 no covered patient's equipment came four weeks or more after the ready date (%d)" % max(lags))
    return True


def ask_a(target, F):
    A, AP = F["A"], F["AP"]
    stops = {}
    for k, kw in (("A1 spell site", dict(site_from="spell")), ("month of discharge", dict(month_by="discharge")),
                  ("month of ready date", dict(month_by="ready")), ("window by ready date", dict(window="ready")),
                  ("no dedup", dict(dedup=False)), ("first submission", dict(keep="first")),
                  ("month-first ward times", dict(parse=AN.monthfirst))):
        stops[k] = (AN.ask_a(target, **kw), AN.ask_a(target, patients=True, **kw))
    for k in ("A1 spell site", "month of discharge", "no dedup", "first submission"):
        ok(all(stops[k][0][c] != A[c] for c in A), "Ask A bed-days: %s moves every cell" % k)
    for k in ("A1 spell site", "month of discharge"):
        ok(all(stops[k][1][c] != AP[c] for c in AP), "Ask A patients: %s moves every cell" % k)
    ok(all(stops["month-first ward times"][0][c] != A[c] for c in A if c[0].startswith("RSM")),
       "month-first ward times move every South Marches cell")
    ok(sum(stops["A1 spell site"][0].values()) == sum(A.values()), "A1 leaves the five-hospital total unchanged")
    ok(all(stops["window by ready date"][0][(s, (2025, 12))] < A[(s, (2025, 12))] for s in core.SITES),
       "the ready-date window loses every December cell")
    ok(len(set(A.values())) == len(A), "no two Ask A bed-day figures equal")
    ok(len(AP) - len(set(AP.values())) <= 1, "Ask A patient counts repeat at most once")
    # one spell per patient with delayed nights in any month at any hospital, so patients and spells agree
    ws = AN.ward_stays(target)
    so = AN.ward_sites(target)
    seen = collections.Counter()
    for r in AN.spells(target):
        R, D = AN.d(r["discharge_ready_date"]), AN.d(r["discharge_datetime"])
        cells = set()
        n = R
        while n < D:
            mid = dt.datetime(n.year, n.month, n.day) + dt.timedelta(1)
            st = [w for a, b, w in ws[(r["provider_code"], r["spell_number"])] if a < mid]
            if (n.year, n.month) in core.MONTH_LABEL:
                cells.add((so[st[-1]], (n.year, n.month)))
            n += dt.timedelta(1)
        for cl in cells:
            seen[(r["nhs_number"],) + cl] += 1
    ok(max(seen.values()) == 1, "no patient has two spells in one hospital-month")
    return stops


def ask_b(target, F):
    B = F["B"]
    stops = {}
    for k, kw in (("B1 no spot", dict(spot=False)), ("month-first", dict(parse="monthfirst")),
                  ("prefix map", dict(prefix_map=True)), ("raw postcodes", dict(normalise=False)),
                  ("latest service start", dict(first=False))):
        stops[k] = AN.ask_b(target, **kw)[0]
    ok(all(stops["B1 no spot"][c] < B[c] for c in B), "B1 moves every Ask B cell")
    ok(min(B[c] - stops["B1 no spot"][c] for c in B) >= 2, "B1 moves every cell by at least two")
    every = AN.ask_b(target, spot=False, prefix_map=True, normalise=False)[0]
    ok(all(every[c] < B[c] for c in B), "the natural read with every hazard leaves every cell")
    for kw in (dict(parse="monthfirst"), dict(first=False), dict(normalise=False), dict(prefix_map=True)):
        for kw2 in (dict(parse="monthfirst"), dict(first=False), dict(normalise=False), dict(prefix_map=True)):
            if kw == kw2:
                continue
            both = AN.ask_b(target, **dict(kw, **kw2))[0]
            single = AN.ask_b(target, **kw)[0]
            ok(all(both[c] != B[c] for c in B if single[c] != B[c]), "no pair of hazards composes back (%s, %s)" % (kw, kw2))
    ok(sum(stops["month-first"][c] != B[c] for c in B) >= 5, "the month-first parse moves most cells")
    ok(all(stops["prefix map"][("Teme Valley", m)] < B[("Teme Valley", m)] for m in core.ASK_MONTHS),
       "the prefix map loses Teme Valley's SV7 addresses every month")
    ok(sum(stops["raw postcodes"][c] != B[c] for c in B) >= 5, "unnormalised postcodes move most cells")
    ok(sum(stops["latest service start"][c] != B[c] for c in B) >= 3, "the latest service start moves some cells")
    vals = list(B.values())
    ok(len(set(vals)) >= 8, "Ask B cells are not uniform")
    # "the referrals the brokerage took": only a started referral carries a start date, and every spot purchase is a
    # closed referral, so no reading of which statuses count moves a cell
    br = AN._rows(target, P.FILES["brokerage"])
    spot_refs = {"BR%06d" % int(r["brokerage_ref"][3:]) for r in AN._rows(target, P.FILES["spot"])}
    ok(all((r["status"] == "Started") == bool(r["start_date"]) for r in br), "only started referrals carry a start")
    ok({r["status"] for r in br if r["referral_no"] in spot_refs} == {"Closed"}, "every spot purchase is closed")
    F2 = AN.files()
    starts = {}
    for r in AN._rows(target, F2["spot"]):
        dd, mm, yy = (int(x) for x in r["service_start"].split("/"))
        k = "BR%06d" % int(r["brokerage_ref"][3:])
        starts[k] = min(starts.get(k, dt.date(yy, mm, dd)), dt.date(yy, mm, dd))
    agree = True
    for r in AN._rows(target, F2["brokerage"]):
        sd = AN.d(r["start_date"]) if r["start_date"] else starts.get(r["referral_no"])
        if sd is None:
            continue
        rt = AN.t(r["received_at"])
        a = (sd - rt.date()).days <= 7
        b = (dt.datetime(sd.year, sd.month, sd.day) - rt) <= dt.timedelta(days=7)
        agree &= a == b
    ok(agree, "the seven days agree on dates and on timestamps")
    closed = {r["referral_no"]: r for r in AN._rows(target, F2["brokerage"])}
    ok(all(k in closed and closed[k]["status"] == "Closed" and not closed[k]["start_date"] for k in starts),
       "every spot purchase traces to a closed brokerage referral with no start")
    return stops


def separation(target, R, info, F):
    """No device or hazard row sits in the main call's population (covered pathway-1 spells, their equipment
    orders, their practices), and the brokerage, the invoices, the postcode lookup and the ward stays are off the
    main call's path."""
    cov_keys = {sp["spell"] for sp in R["spells"] if sp["pathway"] == 1}
    ok(all(sp["pathway"] in (2, 3) for sp in R["spells"] if sp.get("transfer_from")), "transfers are pathway 2 or 3")
    ok(sum(1 for sp in R["spells"] if sp.get("transfer_from")) >= 300, "transfers on file")
    multi = collections.Counter(s["spell"] for s in info["subs"])
    ok(all(k not in cov_keys for k, v in multi.items() if v > 1), "resubmissions are pathway 2 or 3")
    ok(all(x["source"] != "Hospital discharge" for x in info["refs"] if x["pc_style"]),
       "postcode variants are community referrals")
    tmp = tempfile.mkdtemp()
    t2 = os.path.join(tmp, "t")
    shutil.copytree(target, t2)
    for k in ("brokerage", "spot", "postcodes", "wards"):
        os.remove(os.path.join(t2, P.FILES[k]))
    M2 = AN.main_call(t2)
    ok(M2["packages"] == F["M"]["packages"] and M2["total"] == F["M"]["total"], "the main call reads no ask file")
    shutil.rmtree(tmp)


def deliverables(golden_dir, F):
    from openpyxl import load_workbook
    M = F["M"]
    wb = load_workbook(os.path.join(golden_dir, GD.XLSX))
    ws = wb["Split"]
    got = {}
    for row in ws.iter_rows(min_row=5, max_row=9, values_only=True):
        got[row[0]] = (row[4], row[5])
    for s in core.SITES:
        ok(got[core.HOSPITALS[s]["name"]] == (M["packages"][s], whole(M["bed"][s])), "xlsx row %s" % s)
    tot = [r for r in ws.iter_rows(min_row=10, max_row=10, values_only=True)][0]
    ok(tot[4] == AN.FUND and tot[5] == whole(M["total"]), "xlsx total row")
    wb2 = wb["Brokerage starts"]
    for i, dist in enumerate(core.DISTRICTS):
        row = [r for r in wb2.iter_rows(min_row=5 + i, max_row=5 + i, values_only=True)][0]
        ok(row[0] == dist and list(row[1:4]) == [F["B"][(dist, m)] for m in core.ASK_MONTHS], "xlsx Ask B %s" % dist)
    svg = open(os.path.join(golden_dir, GD.SVG), encoding="utf-8").read()
    for c, v in F["A"].items():
        ok("{:,} ({:,})".format(v, F["AP"][c]) in svg, "svg labels %s" % (c,))
    ok("Date" not in svg[:600] or "<dc:date>" not in svg, "svg carries no build date")


def realism(target):
    names = {"Lauren Simpson", "Dennis Mahmood", "Hollie Bird"}
    txt = ""
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith((".txt", ".csv")):
            s = open(p, encoding="utf-8").read()
            ok("\u2014" not in s and "\u2013" not in s, "no em or en dash in %s" % f)
            txt += s if f.endswith(".txt") else ""
        b = open(p, "rb").read()
        ok(b"openpyxl" not in b and b"ReportLab" not in b and b"python" not in b.lower()[:4000], "container scrubbed %s" % f)
    import docs as D
    g = D.guidance_text()
    ok("\u2014" not in g and "\u2013" not in g, "no dash in the guidance")
    found = set(re.findall(r"[A-Z][a-z]+ [A-Z][a-z]+(?=, (?:Head|Deputy Director) of)", g))
    ok(found <= names, "personas from the draw (%s)" % found)
    ok("equipment" not in g.lower(), "the guidance never mentions equipment")
    # no identical monthly counts, no round headline totals
    wr = AN._rows(target, P.FILES["weekly"])
    ok(len({r["p1_nights_after_ready"] for r in wr}) > 0.7 * len(wr), "weekly return varies")
    # ward stays: each trust writes its own date style, no ward holds more patients aged 65 and over at midnight than
    # it has beds, and wards fill to different shares of their beds
    ref = {r["ward_code"]: int(r["beds"]) for r in AN._rows(target, P.FILES["wardref"])}
    load = collections.Counter()
    styles = collections.defaultdict(set)
    for r in AN._rows(target, P.FILES["wards"]):
        uk = "/" in r["ward_start"]
        styles[r["provider_code"]].add(uk)
        f = "%d/%m/%Y %H:%M" if uk else "%Y-%m-%d %H:%M"
        a, b = dt.datetime.strptime(r["ward_start"], f), dt.datetime.strptime(r["ward_end"], f)
        d = a.date()
        while True:
            mid = dt.datetime(d.year, d.month, d.day) + dt.timedelta(1)
            if mid > b:
                break
            if mid > a:
                load[(r["ward_code"], d)] += 1
            d += dt.timedelta(1)
    ok(styles == {"RMC": {False}, "RSM": {True}}, "each trust writes one date style")
    ok(all(n <= ref[w] for (w, d), n in load.items()), "no ward over its beds at midnight")
    top = collections.defaultdict(int)
    for (w, d), n in load.items():
        top[w] = max(top[w], n)
    shares = collections.Counter(round(top[w] / ref[w], 2) for w in top)
    ok(len(shares) >= 18 and max(shares.values()) <= len(top) // 10,
       "wards fill to different shares of their beds (%s)" % shares)
    # the postcode lookup's districts differ in size, and escalation differs by site
    outs = collections.Counter(r["postcode"].split()[0] for r in AN._rows(target, P.FILES["postcodes"]))
    ok(len(outs) == 12 and len(set(outs.values())) >= 9, "the lookup's postcode districts differ in size (%s)" % outs)
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, P.FILES["census"]), read_only=True)
    esc = collections.defaultdict(list)
    for row in wb["Midnight census"].iter_rows(min_row=2, values_only=True):
        if row[0].month in (12, 1, 2):
            esc[row[1]].append(row[4])
    m = sorted(sum(v) / len(v) for v in esc.values())
    ok(len(m) == 5 and m[-1] > 2.5 * m[0], "escalation beds differ by site (%s)" % m)
    # container stamps sit off the whole minute
    import zipfile
    for f in (P.FILES["census"], P.FILES["reablement"]):
        xml = zipfile.ZipFile(os.path.join(target, f)).read("docProps/core.xml").decode()
        secs = re.findall(r"T\d\d:\d\d:(\d\d)Z", xml)
        ok(secs and "00" not in secs, "%s stamped off the minute" % f)
    secs = re.findall(rb"D:\d{12}(\d\d)[+Z]", open(os.path.join(target, P.FILES["guidance"]), "rb").read())
    ok(secs and b"00" not in secs, "the guidance stamped off the minute")


def distractors(target, F):
    tmp = tempfile.mkdtemp()
    for k in P.DISTRACTORS:
        t2 = os.path.join(tmp, k)
        shutil.copytree(target, t2)
        os.remove(os.path.join(t2, P.FILES[k]))
        G = AN.main(t2)
        ok(G["M"]["packages"] == F["M"]["packages"] and G["M"]["total"] == F["M"]["total"] and G["A"] == F["A"]
           and G["B"] == F["B"], "deleting %s changes nothing" % P.FILES[k])
    shutil.rmtree(tmp)


def gates(target, meta):
    files = os.listdir(target)
    ok(len(files) >= 10, "10 or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    ok(big >= 25000, "a file of 25,000 rows or more (%d)" % big)
    ok(len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]), "distractors listed")
    ok(not any("distractor" in f for f in files), "no file named for its role")


def _headers(target):
    from openpyxl import load_workbook
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                out[f] = next(csv.reader(fh))
        elif f.endswith(".xlsx"):
            wb = load_workbook(p, read_only=True)
            out[f] = [str(c) for ws in wb.worksheets for c in next(ws.iter_rows(max_row=1, values_only=True)) if c]
    return out


def _repeated_week(series):
    """A run of seven days repeated exactly elsewhere in a daily series (the copied-week plant)."""
    seen = {}
    for i in range(len(series) - 6):
        w = tuple(series[i:i + 7])
        if len(set(w)) > 1 and w in seen and i - seen[w] >= 7:
            return True
        seen.setdefault(w, i)
    return False


def three_rules(target, F, R):
    """The client's three rules, executed (dataset-generation 7.1): R1 the field's raw material ships and the decisive
    computation reads it; R2 every Layer 1 item on the main path is neutral, and the ask-side mess sits off it; R3a the
    easy route on the generator's clean truth files the named wrong answer; R3b the decisive step alone files the
    golden and each single lower correction stays wrong; R3c nothing is planted. With the lens-swap test and the
    equipment notes' one sentence."""
    M = F["M"]
    cov = AN.covered(target)
    eq = AN.discharge_orders(target)
    heads = _headers(target)
    sp_cols, eq_cols = set(heads[P.FILES["spells"]]), set(heads[P.FILES["ices"]])
    ok({"nhs_number", "discharge_ready_date", "discharge_datetime", "discharge_pathway", "p1_care_package"} <= sp_cols
       and {"nhs_number", "route", "required_by", "delivered_date"} <= eq_cols,
       "R1 the field's raw material ships: each spell's ready date and discharge time, each equipment line's delivery")
    banned = re.compile(r"sav|free|value|benefit|counterfact|reason|cause|overlap|wait|depend", re.I)
    ok(not any(banned.search(c) for cols in heads.values() for c in cols),
       "R1 no shipped column holds the deciding quantity (no saving, value, cause, wait or dependency column)")
    moved = 0
    for r in cov:
        Rd, D = AN.d(r["discharge_ready_date"]), AN.d(r["discharge_datetime"])
        E = eq.get((r["nhs_number"], Rd))
        E = min(E) if E else None
        if max(0, (D - max(Rd, E or Rd)).days) != (D - Rd).days:
            moved += 1
            ok(E is not None and E > Rd, "R1 a patient the decisive step moves has a delivery after the ready date (%s)"
               % r["spell_number"])
    ok(moved >= 700, "R1 the decisive computation reads the equipment service's rows: %d covered patients' nights come "
                     "from their delivery dates" % moved)
    # the lens-swap test: the default and the golden are not one quantity under two lenses; the golden needs a second
    # system's dates, and without them every construction on the warehouse alone files another split
    tmp = tempfile.mkdtemp()
    t2 = os.path.join(tmp, "t")
    shutil.copytree(target, t2)
    os.remove(os.path.join(t2, P.FILES["ices"]))
    open(os.path.join(t2, P.FILES["ices"]), "w").write(open(os.path.join(target, P.FILES["ices"])).readline())
    M2 = AN.main_call(t2)
    shutil.rmtree(tmp)
    ok(M2["packages"] == M["alloc"]["R1"] and M2["packages"] != M["packages"],
       "lens swap: with the equipment lines removed the same population, window and estimand file the default split")
    ok(moved < len(cov), "lens swap: the golden and the default agree on every covered patient whose equipment did not "
                         "arrive after the ready date (%d of %d moved)" % (moved, len(cov)))
    # R2: the main path's Layer 1 items
    raw = AN.spells(target, dedup=False)
    first = {}
    for r in raw:
        k = (r["provider_code"], r["spell_number"])
        if k not in first or int(r["submission_id"]) < int(first[k]["submission_id"]):
            first[k] = r
    ck = {(r["provider_code"], r["spell_number"]) for r in cov}
    ok({k for k, r in first.items() if r["discharge_pathway"] == "1"} >= ck
       and sum(1 for r in raw if (r["provider_code"], r["spell_number"]) in ck) == len(ck),
       "R2 mess neutral: resubmitted spells (kept beside the rows they correct) are none of the covered spells, so the "
       "first, the latest or every submission gives the same covered patients")
    plain_rows = [r for r in AN._rows(target, P.FILES["ices"]) if r["route"] == "Hospital discharge"]
    exact = {r["nhs_number"] for r in plain_rows}
    ok(not any(r["nhs_number"] in exact for r in cov) and all(" " in x for x in exact),
       "R2 mess neutral: the equipment export writes every NHS number spaced, so an unnormalised join matches nothing "
       "(a loud failure, never a silent partial match)")
    in_stay = collections.defaultdict(list)
    for r in plain_rows:
        if r["delivered_date"]:
            in_stay[r["nhs_number"].replace(" ", "")].append(AN.d(r["delivered_date"]))
    by_stay = {r["spell_number"] for r in cov if any(AN.t(r["admission_datetime"]).date() <= x <= AN.d(
        r["discharge_datetime"]) for x in in_stay[r["nhs_number"]])}
    by_key = {r["spell_number"] for r in cov if (r["nhs_number"], AN.d(r["discharge_ready_date"])) in eq}
    ok(by_stay == by_key and len(by_key) == F["X"]["with_equipment"],
       "R2 mess neutral: once the spaces go, a join on the NHS number and the stay's dates and a join on the number and "
       "the required-by date find the same %d covered patients" % len(by_key))
    merged = {r["practice_code"]: (r["successor_code"], AN.d(r["status_date"])) for r in
              AN._rows(target, P.FILES["practices"]) if r["status"].startswith("Closed")}
    on_spells = [r for r in raw if r["gp_practice_code"] in merged]
    ok(on_spells and all(AN.t(r["admission_datetime"]).date() < merged[r["gp_practice_code"]][1] for r in on_spells)
       and not any(r["gp_practice_code"] in merged for r in cov),
       "R2 mess neutral: practices closed by merger sit only on spells admitted before the merger (%d), none covered, "
       "so dropping or mapping them leaves the call" % len(on_spells))
    tmp = tempfile.mkdtemp()
    t2 = os.path.join(tmp, "t")
    shutil.copytree(target, t2)
    for k in ("wards", "wardref", "brokerage", "spot", "postcodes", "weekly", "census", "reablement"):
        os.remove(os.path.join(t2, P.FILES[k]))
    M3 = AN.main_call(t2)
    shutil.rmtree(tmp)
    ok(M3["packages"] == M["packages"] and M3["total"] == M["total"],
       "R2 mess neutral: the ask-side mess (ward times in two styles, moves within a trust, finance's references and "
       "dates, typed postcodes, SV7 across the county line) sits in files the main call never reads")
    # R3a and R3b on the generator's clean truth (the world before any record is written)
    cl = [sp for sp in R["spells"] if sp["pathway"] == 1 and sp["p1"] == "New" and core.in_winter(sp["ready"])
          and sp["home"] != "Severnside"]
    caps = collections.Counter(sp["site"] for sp in cl)
    ok(dict(caps) == M["caps"], "R3 the clean truth's covered patients are the pack's (%s)" % dict(caps))

    def per_site(f, pop=cl):
        s, n = collections.Counter(), collections.Counter()
        for sp in pop:
            n[sp["site"]] += 1
            s[sp["site"]] += f(sp)
        return {x: Fraction(s[x], n[x]) for x in core.SITES}

    stay = lambda sp: (sp["dis_t"].date() - sp["ready"]).days
    lag = lambda sp: max(0, (sp["equip"] - sp["ready"]).days) if sp["equip"] else 0
    dflt = per_site(stay)
    o, a = AN.allocate(dflt, dict(caps))
    r1bed = whole(sum(M["rung_bed"]["R1"].values()))
    ok(a == {"RSM01": 361, "RSM02": 285, "RMC02": 350, "RMC01": 204, "RSM03": 0} == M["alloc"]["R1"]
       and whole(sum(a[s] * dflt[s] for s in core.SITES)) == r1bed,
       "R3a the analyst test on the clean truth: the nights after the ready date, every filed rule applied, fill Ashby "
       "Vale 361, Cleeve Park 285, Wendlebury 350, Royal Marchford 204, Holmford none, %s bed-days (%s)" % (
           "{:,}".format(r1bed), a))
    gold = per_site(lambda sp: max(0, stay(sp) - lag(sp)))
    o, a = AN.allocate(gold, dict(caps))
    ok(a == GOLD and whole(sum(a[s] * gold[s] for s in core.SITES)) == whole(M["total"]),
       "R3b the decisive step alone on the clean truth (the nights from the later of the ready date and the delivery) "
       "files the golden split and %s bed-days" % "{:,}".format(whole(M["total"])))
    rs = [sp for sp in R["spells"] if sp["pathway"] == 1 and sp["p1"] == "Restart" and core.in_winter(sp["ready"])
          and sp["home"] != "Severnside"]
    rmean = per_site(stay, rs)
    eqp = [sp for sp in cl if lag(sp)]
    emean = per_site(lag, eqp)
    singles = {
        "equipment patients counted at nought": per_site(lambda sp: 0 if sp["equip"] else stay(sp)),
        "the average over patients without equipment": per_site(stay, [sp for sp in cl if not sp["equip"]]),
        "the restart patients' nights subtracted": {s: dflt[s] - rmean[s] for s in core.SITES},
        "the equipment patients' average wait subtracted": {s: dflt[s] - emean[s] for s in core.SITES},
    }
    for lab, v in singles.items():
        o, a = AN.allocate(v, dict(caps))
        bed = whole(sum(a[s] * v[s] for s in core.SITES))
        ok(a != GOLD or bed != whole(M["total"]), "R3b one correction alone stays wrong: %s files %s, %d bed-days"
           % (lab, a, bed))
    ok(all(stay(sp) == lag(sp) for sp in rs if sp["equip"]) and sum(1 for sp in rs if lag(sp)) >= 50,
       "R3b the comparison group: every restart patient (care already in place) waiting for equipment left on its "
       "delivery day (%d)" % sum(1 for sp in rs if lag(sp)))
    # R3c: nothing planted
    days = collections.defaultdict(collections.Counter)
    for r in AN.spells(target):
        days[r["site_code"]][AN.d(r["discharge_datetime"])] += 1
    span = [core.REC0 + dt.timedelta(i) for i in range((core.REC1 - core.REC0).days + 1)]
    ok(not any(_repeated_week([days[s][x] for x in span]) for s in core.SITES),
       "R3c no plant: no site's daily discharges repeat a week of another stretch")
    dl = collections.defaultdict(collections.Counter)
    for r in AN._rows(target, P.FILES["ices"]):
        if r["delivered_date"]:
            dl[r["depot"]][AN.d(r["delivered_date"])] += 1
    ok(not any(_repeated_week([dl[k][x] for x in span]) for k in dl),
       "R3c no plant: neither depot's daily deliveries repeat a week of another stretch")
    ok(not any(re.search(r"memo|draft|brief|minutes|summary|review", f, re.I) for f in os.listdir(target)),
       "R3c no plant: no memo, draft, briefing or earlier review ships")
    import docs as D
    g = D.guidance_text()
    ok(not re.search(r"\d[\d.,]*\s*(nights|bed-days)", g) and not any(re.search(r"%s\D{0,12}\d" % re.escape(
        core.HOSPITALS[s]["short"]), g) for s in core.SITES),
       "R3c no plant: the allocation note carries no hospital figure, value or ranking")
    wk = collections.defaultdict(lambda: [0] * 8)
    for r in AN.spells(target):
        dd = AN.d(r["discharge_datetime"])
        we = dd + dt.timedelta((6 - dd.weekday()) % 7)
        o = wk[(r["provider_code"], we)]
        pw = int(r["discharge_pathway"])
        o[2 * pw] += 1
        o[2 * pw + 1] += (dd - AN.d(r["discharge_ready_date"])).days
    rows = AN._rows(target, P.FILES["weekly"])
    ok(all([int(r[c]) for c in heads[P.FILES["weekly"]][3:]] == wk[(r["provider_code"], AN.d(r["week_ending"]))]
           for r in rows), "R3c no plant: the national weekly return reproduces from the warehouse by trust and week "
                           "(nothing in it is wrong)")
    ok(not any(re.search(r"notes|dictionar|manifest|read_?me|request_log|layout", f, re.I) for f in os.listdir(target)),
       "no shipped file describes the data (no field notes, dictionary, manifest or request log)")
    return moved


def run(F, target, meta, R, info, golden_dir):
    N[0] = 0
    three_rules(target, F, R)
    main_call(F)
    ladder(F)
    control_reflex(target, F)
    facts(target, F)
    edges(target, F)
    semantic_forks(target, F)
    ask_a(target, F)
    ask_b(target, F)
    separation(target, R, info, F)
    deliverables(golden_dir, F)
    realism(target)
    distractors(target, F)
    gates(target, meta)
    return N[0]
