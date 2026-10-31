"""Every assertion the build stands on, run on the clean truth and the cut pack. run() returns the count."""
import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import statistics
import tempfile
import zipfile
from collections import Counter, defaultdict

import openpyxl
import pypdf

import analysis as AN
import docs
import pack as P
import world as W

N = [0]
UNIT = 100
DESCRIBING = ("readme", "dictionary", "field_notes", "fieldnotes", "manifest", "notes", "codebook", "schema",
              "data_guide", "how_to")


def ok(cond, label, detail=""):
    if not cond:
        raise AssertionError("%s %s" % (label, detail))
    N[0] += 1


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def pdf_text(path):
    return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(path).pages)


def truth_asks(R):
    """The asks from the simulation itself, for comparison with the files."""
    V = R["visits"]
    prem = {p["pid"]: p for p in R["premises"]}
    perm = R["permits"]
    ta, tc = defaultdict(list), defaultdict(int)
    by_routine = defaultdict(list)
    for v in V:
        if v["kind"] == "return" and v["seq"]:
            by_routine[v["seq"]["routine"]].append(v)
    for ri, rets in by_routine.items():
        rv = V[ri]
        if rv["day"].year != 2026:
            continue
        dist = prem[perm[rv["permit"]]["prem"]]["d26"]
        done = sorted([x for x in rets if x["result"] != "No access"], key=lambda x: x["day"])
        if done and done[0]["day"].year == 2026:
            ta[dist].append(W.working_between(rv["day"], done[0]["day"]))
        for x in sorted(rets, key=lambda x: x["day"])[1:]:
            if x["day"].year == 2026:
                tc[dist] += W.FEE_OLD if x["day"] < W.FEE_CHANGE else W.FEE_NEW
    tb = defaultdict(list)
    for v in V:
        if v["kind"] == "complaint" and v["day"].year == 2026:
            inc = R["incidents"][v["incident"]]
            start = dt.datetime.combine(v["day"], v["time"])
            shown = [t for t in inc["times"] if t <= start - dt.timedelta(minutes=20)]
            if shown:
                tb[prem[perm[v["permit"]]["prem"]]["d26"]].append((start - shown[0]).total_seconds() / 3600)
    return ({d: statistics.median(v) for d, v in ta.items()}, {d: statistics.median(v) for d, v in tb.items()},
            dict(tc))


def run(R, Dd, counts, target, F, golden_dir):
    N[0] = 0
    D = F["D"]
    G = F["G"]
    files = sorted(os.listdir(target))
    # ------------------------------------------------------------ input gates
    ok(len(files) >= 10, "gate: ten or more files", len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "gate: three or more formats")
    ok(max(counts["legacy"], counts["current"]) >= 25000, "gate: a file of 25,000 rows or more", counts["legacy"])
    ok(all(P.FILES[k] in files for k in P.DISTRACTORS) and len(P.DISTRACTORS) >= 2, "gate: two distractors shipped")
    ok(not any(any(w in f.lower() for w in DESCRIBING) for f in files), "gate: no file describing the data by name")
    for f in files:
        if f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(os.path.join(target, f), read_only=True)
            ok(not any(any(w in s.lower() for w in ("readme", "notes", "dictionary", "about")) for s in wb.sheetnames),
               "gate: no describing sheet", f)
    # ------------------------------------------------------------ R1: the field's raw material ships
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().strip().split(",")
             for f in files if f.endswith(".csv")}
    allcols = {c.lower() for h in heads.values() for c in h}
    ok(not any(re.search(r"visit_(count|number)|prior_|previous|earlier|first_visit|tenure|familiar", c)
               for c in allcols), "R1: no column holds an inspector's earlier visits to an establishment")
    ok({"inspector", "permit_no", "insp_date"} <= set(heads[P.FILES["legacy"]]) and
       {"inspector_employee_no", "permit_id", "inspected_at_utc"} <= set(heads[P.FILES["current"]]),
       "R1: visit-level records with inspector and establishment ship in both exports")
    # ------------------------------------------------------------ the call
    tot = G["total"]
    ok(G["add"] and tot > W.THRESHOLD * 1.15, "call: the golden adds the third officer, past the 1.15 floor", tot)
    fam = dict(golden=tot,
               classes_0123=AN.golden_variant(D, classes=(0, 1, 2, 3)),
               window_2021=AN.golden_variant(D, years=(2021, 2026)),
               window_2023=AN.golden_variant(D, years=(2023, 2026)),
               routine_and_complaint_only=AN.golden_variant(D, types=("routine", "complaint")),
               routine_only=AN.golden_variant(D, types=("routine",)),
               window_36_months=AN.golden_variant(D, window=36))
    for k, v in fam.items():
        ok(v > W.THRESHOLD * 1.15, "call: standing member %s clears 540 by 1.15" % k, v)
        ok(round(v / UNIT) * UNIT == round(tot / UNIT) * UNIT and edge(v, UNIT) >= UNIT / 4,
           "call: standing member %s in the golden's bin a quarter-bin from its edge" % k, "%.1f" % v)
    F["family"] = fam
    # the crossed family: every estimation window, class set, visit definition, count window and model form at once
    crossed = {}
    for yl in ((2021, 2026), (2022, 2026), (2023, 2026)):
        for cl in ((0, 1, 2), (0, 1, 2, 3)):
            for ty in (None, ("routine",)):
                for wn in (None, 36):
                    for mo in ("cells", "main"):
                        crossed[(yl, cl, ty, wn, mo)] = AN.golden_variant(D, years=yl, classes=cl, types=ty, window=wn,
                                                                          model=mo)
    for k, v in crossed.items():
        ok(v > W.THRESHOLD * 1.15 and round(v / UNIT) == round(tot / UNIT) and edge(v, UNIT) >= UNIT / 8,
           "call: crossed member %s in the golden's bin, an eighth of a bin from its edge" % (k,), "%.1f" % v)
    rich = dict(inspector=AN.pair_with_terms(D), own=AN.pair_with_terms(D, inspector=False, prior=1.0),
                both=AN.pair_with_terms(D, prior=1.0), both_prior4=AN.pair_with_terms(D, prior=4.0))
    for k, v in rich.items():
        ok(round(v / UNIT) == round(tot / UNIT) and edge(v, UNIT) >= UNIT / 4,
           "call: the visit classes with the %s terms in the golden's bin a quarter-bin from its edge" % k, "%.1f" % v)
    F["crossed"] = (min(crossed.values()), max(crossed.values()), len(crossed))
    F["rich"] = rich
    rungs = dict(category=AN.route_category(D), own_history=AN.route_own_history(D),
                 inspector=AN.route_inspector(D), trend=AN.route_trend(D), tenure=AN.route_tenure(D),
                 category_2025_2026=AN.route_category(D, years=(2025, 2026)))
    for k, v in rungs.items():
        ok(v < W.THRESHOLD / 1.15, "R3a: the easy route %s files no third officer, under the 1.15 floor" % k, v)
    F["rungs"] = rungs
    contam = AN.golden_variant(D, years=(2019, 2026))
    ok(contam < W.THRESHOLD, "ladder: visits counted from the record's start and fitted on every year (left "
                             "truncation unhandled) lands under 540", contam)
    binary = AN.golden_variant(D, classes=(0, 1))
    F["refuted"] = dict(contaminated=contam, binary=binary)
    # the record refutes collapsing second visits into later ones: second visits run above later visits
    rows, seen = AN.visit_counts(D)
    rates, cells = AN.cell_rates(D, rows)
    num = var = 0.0
    for risk in (1, 2, 3):
        a, n1 = cells[(risk, 1)]
        b, n2 = cells[(risk, 2)]
        p1, p2 = a / n1, b / n2
        m, nn = a + b, n1 + n2
        num += a - n1 * m / nn
        var += n1 * n2 * m * (nn - m) / (nn * nn * (nn - 1))
        ok(p1 > p2, "SF7: second visits run above later visits in risk category %d" % risk, "%.3f %.3f" % (p1, p2))
        ok(cells[(risk, 0)][0] / cells[(risk, 0)][1] > 2.0 * p2, "data: first visits run at more than twice later "
                                                                   "visits in risk category %d" % risk)
    zmh = num / var ** 0.5
    ok(zmh > 4.0, "SF7: the record refutes folding second visits into later ones (Mantel-Haenszel z %.1f)" % zmh)
    F["z_second"] = zmh
    # R3b: the easy route with only the decisive step changed lands the golden's call and bin
    ok(abs(AN.golden_variant(D) - tot) < 1e-9, "R3b: the category route with visit classes is the golden")
    ok(round(rungs["category"] / UNIT) != round(tot / UNIT), "R3b: the category route alone is in another bin")
    # back-test in the field's own way: fit on 2022-2024, predict 2025-2026 as recorded, and the 2023 appointee
    rows_all, _ = AN.visit_counts(D)
    rates_fit, _ = AN.cell_rates(D, rows_all, years=(2022, 2024))
    cat = defaultdict(lambda: [0, 0])
    for x in rows_all:
        if 2022 <= x["t"].year <= 2024:
            cc = cat[int(D["permits"][x["permit"]]["risk_category"])]
            cc[0] += x["unsat"]
            cc[1] += 1
    obs = pred_f = pred_c = 0.0
    for x in rows_all:
        if 2025 <= x["t"].year <= 2026:
            risk = int(D["permits"][x["permit"]]["risk_category"])
            obs += x["unsat"]
            pred_f += rates_fit[(risk, min(x["k"], 2))]
            pred_c += cat[risk][0] / cat[risk][1]
    ok(abs(pred_c / obs - 1) < 0.06, "Back-test: the category route validates on 2025-2026 (within 6 per cent)",
       "%.3f" % (pred_c / obs))
    ok(abs(pred_f / obs - 1) < 0.06, "Back-test: the golden's construction validates on 2025-2026", "%.3f" % (pred_f / obs))
    obs5 = predf5 = predc5 = 0.0
    emp_collins = "E46590"
    for x in rows_all:
        if x["who"] == emp_collins and dt.date(2023, 5, 1) <= x["t"].date() <= dt.date(2024, 4, 30):
            risk = int(D["permits"][x["permit"]]["risk_category"])
            obs5 += x["unsat"]
            predf5 += rates_fit[(risk, min(x["k"], 2))]
            predc5 += cat[risk][0] / cat[risk][1]
    ok(abs(predf5 / obs5 - 1) < abs(predc5 / obs5 - 1) / 2,
       "Back-test: on the 2023 appointee's first year the visit classes beat the category rates by half",
       "%.2f %.2f" % (predf5 / obs5, predc5 / obs5))
    ok(abs(tot / R["truth27"] - 1) < 0.12, "oracle: the golden within 12 per cent of the truth's expected count",
       "%.1f %.1f" % (tot, R["truth27"]))
    # the memo's statements about the record and the schedule
    share = defaultdict(lambda: [0, 0])
    for x in rows_all:
        share[x["t"].year][0] += x["k"] == 0
        share[x["t"].year][1] += 1
    ok(all(share[y][0] / share[y][1] < 0.10 for y in range(2022, 2027)),
       "memo: each year 2022-2026 fewer than one routine inspection in ten was a first visit")
    s27 = G["nk"][0] / sum(G["nk"].values())
    ok(0.20 < s27 < 0.25, "memo: nearly one in four of the 2027 schedule is a first visit", "%.3f" % s27)
    fp = sum(F["first_part"].values())
    ok(edge(fp, 10) >= 2.5, "memo: the first visits' part of the forecast a quarter-bin from a nearest-10 edge", fp)
    F["first_share"] = {y: share[y][0] / share[y][1] for y in sorted(share)}
    # ------------------------------------------------------------ the fork table
    ok(all(r["result"] in AN.UNSAT or r["result"] not in ("IHH CLOSURE", "Closed - imminent health hazard")
           for r in D["visits"]), "SF1: closures for an imminent hazard read as unsatisfactory")
    no_ihh = []
    for v in D["visits"]:
        if v["result"] in ("IHH CLOSURE", "Closed - imminent health hazard"):
            no_ihh.append(v)
    saved = AN.UNSAT
    AN.UNSAT = {"UNSAT", "Unsatisfactory"}
    alt = AN.golden_call(D)["total"]
    AN.UNSAT = saved
    ok(alt > W.THRESHOLD * 1.15 and round(alt / UNIT) == round(tot / UNIT), "SF1: same call and bin with closures "
                                                                           "left out", alt)
    ok(sum(s["n"] for s in D["schedule"]) == sum(G["nk"].values()), "SF2: the schedule's inspections are the forecast's")
    ok(set(D["d27"]) == set(s["d27"] for s in D["schedule"]), "SF3: every scheduled district has its named inspector")
    ok(round(fam["routine_only"] / UNIT) == round(tot / UNIT), "SF4: counting only routine visits: same bin")
    na_counted = AN.golden_variant(D, count_noaccess=True)
    ok(round(na_counted / UNIT) == round(tot / UNIT) and edge(na_counted, UNIT) >= UNIT / 4,
       "SF5: closed-premises calls counted as earlier visits: same bin", "%.1f" % na_counted)
    F["sf5"] = na_counted
    ok(round(fam["window_2021"] / UNIT) == round(tot / UNIT) == round(fam["window_2023"] / UNIT),
       "SF6: estimation window 2021 or 2023 onward: same bin")
    ok(round(fam["classes_0123"] / UNIT) == round(tot / UNIT), "SF7: classes 0, 1, 2, 3 and more: same bin")
    ok(round(fam["window_36_months"] / UNIT) == round(tot / UNIT), "SF8: earlier visits within 36 months: same bin")
    ok(all(G["nk"].get(k, 0) > 0 for k in (0, 1, 2)), "SF9: the schedule's own earlier 2027 visits advance the count")
    last, same_year = {}, 0
    for v in D["visits"]:
        key = (v["who"], v["permit"])
        if v["type"] == "routine" and v["result"] not in AN.NOACC and key in last and last[key].year == v["t"].year:
            same_year += 1
        if v["result"] not in AN.NOACC:
            last[key] = v["t"]
    ok(same_year > 1000, "SF9: the record's classes count the same year's earlier visits by the inspector", same_year)
    noadv = AN.golden_variant(D, advance=False)
    ok(noadv > tot * 1.2, "SF9: reading every 2027 inspection at the end-2026 count is another construction",
       "%.1f" % noadv)
    F["sf9"] = noadv
    utc_naive = _utc_as_local(D, target)
    ok(round(utc_naive / UNIT) == round(tot / UNIT), "SF10: new-system times read without converting UTC: same bin",
       utc_naive)
    by_addr = _by_address(D)
    ok(by_addr > W.THRESHOLD * 1.15 and round(by_addr / UNIT) == round(tot / UNIT),
       "SF11: an establishment's visits counted across a change of ownership: same call and bin", by_addr)
    ok(tot > W.THRESHOLD and round(tot) != W.THRESHOLD, "SF12: 'exceed 540' strict or not: same call")
    r2 = dict(utc_as_local=utc_naive, ownership_by_address=by_addr, closures_left_out=alt,
              closed_premises_counted=na_counted)
    for k, v in r2.items():
        ok(v > W.THRESHOLD * 1.15 and round(v / UNIT) == round(tot / UNIT),
           "R2: the Layer 1 mess is neutral on the call: %s keeps the call and the bin" % k, "%.1f" % v)
    inits = Counter(s["initials"] for s in D["staff"].values())
    ok(max(inits.values()) == 1, "R2: no two staff share initials, so the legacy initials resolve one to one")
    F["r2"] = r2
    ok(edge(tot, UNIT) >= UNIT / 4, "SF13: the total sits a quarter-bin from a nearest-100 edge", tot)
    # ------------------------------------------------------------ the asks
    ta, tb, tc = truth_asks(R)
    a0, _ = AN.ask_a(target, D, use_daysheet=False)
    b0, _ = AN.ask_b(target, D, first_notice=False)
    c0 = AN.ask_c(target, D, use_letters=False, use_daysheet=False)
    for d in sorted(W.SEEDS_2026):
        ok(F["A"][d] == ta[d], "SF14: ask A district %d equals the truth" % d, (F["A"][d], ta[d]))
        ok(abs(F["B"][d] - tb[d]) < 1e-6, "SF17: ask B district %d equals the truth" % d)
        ok(F["C"].get(d, 0) == tc.get(d, 0), "SF19: ask C district %d equals the truth" % d)
        ok(F["A"][d] != a0.get(d), "device: the keying stamp moves ask A district %d" % d)
        ok(round(F["B"][d], 1) != round(b0.get(d, -9), 1), "device: the dispatched report moves ask B district %d" % d)
        ok(F["C"].get(d, 0) != c0.get(d, 0), "device: the unkeyed closed-premises calls move ask C district %d" % d)
        ok(edge(F["B"][d], 0.1) >= 0.025, "bins: ask B district %d a quarter-bin from its edge" % d, F["B"][d])
        ok(abs(F["A"][d] * 2 - round(F["A"][d] * 2)) < 1e-9, "bins: ask A district %d is a whole or half day" % d)
    hol = AN.holidays(target)
    ok(all(dt.date.fromisoformat(x) in hol for x in ("2026-11-26", "2026-11-27", "2026-06-19")),
       "SF15: the county holidays file carries Thanksgiving, the day after and Juneteenth")
    ok(all(r["template"].startswith("RV-NA") is False or r["visit_date"] for r in AN.letters(target)),
       "SF16: every closed-premises return letter carries its visit date")
    ok(len(F["B"]) == 11 and all(n >= 8 for n in F["B_n"].values()), "SF18: every district has complaint "
                                                                     "investigations in 2026", F["B_n"])
    ok(all(v > 0 for v in F["C"].values()), "SF20: every district owes return visit fees")
    ok(sum(F["C"].values()) % 8 == 0, "SF21: fees are sums of 152 and 168")
    # the asks never touch the call's rows: no ask device sits on a routine inspection
    ok(all(Dd["entry"][i] and R["visits"][i]["kind"] == "return" for i in Dd["entry"]),
       "separation: every keying stamp sits on a return inspection, none on a routine one")
    ok(all(c["ref"] in (True, False) for c in Dd["complaints"]), "separation: the dispatched report is a complaint record")
    # ------------------------------------------------------------ distractors, realism, leaks
    for k in P.DISTRACTORS:
        src = open(os.path.join(os.path.dirname(__file__), "analysis.py")).read()
        ok(P.FILES[k] not in src, "distractor: %s is never read by the golden" % P.FILES[k])
    leg_ids = [r.split(",")[0] for r in open(os.path.join(target, P.FILES["legacy"]), encoding="utf-8").read().splitlines()[1:200] if r]
    steps = {int(b[-6:]) - int(a[-6:]) for a, b in zip(leg_ids, leg_ids[1:])}
    ok(len(steps) > 1, "realism: legacy inspection numbers do not step evenly")
    names = [r["establishment"] for r in D["permits"].values()]
    shapes = Counter(len(n.split()) for n in names)
    ok(len(shapes) >= 3, "realism: establishment names take several shapes")
    ok(len({F["A_n"][d] for d in F["A_n"]}) > 5, "realism: no identical return counts across districts")
    plan = pdf_text(os.path.join(target, P.FILES["plan"]))
    fees = pdf_text(os.path.join(target, P.FILES["fees"]))
    ok("540" in plan and "Table 1" in plan, "control: the plan's text reads back through the PDF extractor")
    ok("$168" in fees, "control: the fee schedule reads back through the PDF extractor")
    for word in ("first visit", "familiar", "earlier visit", "previous visit", "new to the", "same inspector",
                 "rotation", "tenure", "experience"):
        ok(word not in plan.lower() and word not in fees.lower(), "leak: the governing documents never say %r" % word)
    ok("—" not in plan and "–" not in plan and "—" not in fees, "style: no dash in the documents")
    for f in files:
        if f.endswith((".csv", ".json")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            ok("—" not in txt, "style: no em dash in %s" % f)
    lets = open(os.path.join(target, P.FILES["letters"]), encoding="utf-8").read()
    ok(max(re.findall(r"20\d\d-\d\d-\d\d", lets)) <= "2026-12-31", "dates: the correspondence log ends with 2026")
    cur = open(os.path.join(target, P.FILES["current"]), encoding="utf-8").read()
    ok(max(re.findall(r"20\d\d-\d\d-\d\dT", cur)) < "2027-01-02T", "dates: the new export ends with 2026",
       max(re.findall(r"20\d\d-\d\d-\d\dT", cur)))
    # golden deliverables read back
    gx = openpyxl.load_workbook(os.path.join(golden_dir, "return_inspections_2027.xlsx"), read_only=True)
    ok({"Forecast 2027", "Return timeliness 2026", "Complaint response 2026", "Return visit fees 2026"} <=
       set(gx.sheetnames), "golden: the workbook carries the forecast and the three 2026 tables")
    memo = pdf_text(os.path.join(golden_dir, "return_officer_memo_2027.pdf"))
    ok("Add the third return-inspection officer" in memo and format(int(UNIT * int(tot / UNIT + 0.5)), ",") in memo,
       "golden: the memo states the call and the rounded forecast")
    return N[0]


def _utc_as_local(D, target):
    """The golden with the new export's UTC stamps taken as local time."""
    import copy
    D2 = dict(D)
    vs = []
    for v in D["visits"]:
        if v["src"] == "current":
            v = dict(v)
            v["t"] = dt.datetime.strptime(v["t_utc"], "%Y-%m-%dT%H:%M:%SZ")
        vs.append(v)
    vs.sort(key=lambda v: (v["t"], v["id"]))
    D2["visits"] = vs
    return AN.golden_call(D2)["total"]


def _by_address(D):
    """The golden with an establishment's permits merged by street address (ownership changes ignored)."""
    D2 = dict(D)
    addr = {pid: r["street_address"] + "|" + r["city"] for pid, r in D["permits"].items()}
    canon = {}
    for pid in sorted(D["permits"]):
        canon.setdefault(addr[pid], pid)
    m = {pid: canon[addr[pid]] for pid in D["permits"]}
    D2["visits"] = [dict(v, permit=m[v["permit"]]) for v in D["visits"]]
    rows, seen = AN.visit_counts(D2)
    rates, cells = AN.cell_rates(D2, rows)
    D3 = dict(D2)
    D3["schedule"] = [dict(s, permit=m[s["permit"]]) for s in D["schedule"]]
    return AN.forecast(D3, rates, seen)[0]
