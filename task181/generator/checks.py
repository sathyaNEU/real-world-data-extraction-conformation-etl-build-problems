"""task181's assertions, run on the cut pack after build.py: the three rules (R1 to R3c), every semantic
fork row, the routes and their margins, the shock sorts, separation, the asks' stops and bins, the input
gates, the documents read back with positive controls, and the realism sweep.

    python3 task181/generator/checks.py
"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import Counter

import numpy as np
import pdfplumber
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B  # noqa: E402
import ceiling as CE  # noqa: E402
import design as D  # noqa: E402
import reader as RD  # noqa: E402
import routes as R  # noqa: E402
import world as Wd  # noqa: E402
from common import TARGET, TRIGGER, mw_of  # noqa: E402

RESULTS = []
GOLD_NAMES = {"San Roque", "Bagumbayan", "Maligaya"}
BESIDE = ["Tabing-Ilog", "Pulong Bayabas", "Malinta", "Kanluran", "Burol", "Silangan"]
DEFAULT_NAMES = GOLD_NAMES - {"San Roque"} | set(BESIDE)


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def p(k):
    return os.path.join(TARGET, B.FILES[k])


# ------------------------------------------------------------------ variant readings of the line list
def cases_variant(rows, canon, merge=True, other_towns=False, not_a_case=False, week_by="onset", drop_blank=False,
                  split=True, latest=True, drop_travel=False):
    pick = {}
    for r in rows:
        if latest or r["case_no"] not in pick:
            pick[r["case_no"]] = r
    out = []
    for no, r in pick.items():
        if r["case_classification"] in ("Not a case", "X") and not not_a_case:
            continue
        town = r["city_municipality"].strip()
        b = RD.norm(r["barangay"])
        if town != "Dalisay City":
            if not other_towns or b not in canon:
                continue
        if b not in canon:
            raise KeyError(r["barangay"])
        if drop_travel and r["travel_14d"] == "Y":
            continue
        name = canon[b]
        pk = RD.purok_no(r["street_purok"])
        if split and name == "Santo Tomas" and pk is not None and pk >= 5:
            name = "Santo Tomas Norte"
        onset = RD.parse_date(r["date_onset"])
        if onset is None and drop_blank:
            continue
        d = onset or RD.parse_date(r["date_consult"])
        if week_by == "consult":
            d = RD.parse_date(r["date_consult"])
        out.append({"case_no": no, "barangay": name, "age": int(r["age_years"]), "onset": d,
                    "initials": r["patient_initials"], "sex": r["sex"], "reported": RD.parse_date(r["date_reported"]),
                    "onset_key": onset or RD.parse_date(r["date_consult"])})
    if merge:
        seen, kept = set(), []
        for c in sorted(out, key=lambda c: (c["reported"], c["case_no"])):
            k = (c["initials"], c["sex"], c["age"], c["barangay"], c["onset_key"])
            if k in seen:
                continue
            seen.add(k)
            kept.append(c)
        out = kept
    return out


def iso_aggregates(cases, names):
    idx = {n: k for k, n in enumerate(names)}
    res = np.zeros((len(names), 3))
    hist = np.zeros((len(names), 3))
    for c in cases:
        y, w, _ = c["onset"].isocalendar()
        i = idx[c["barangay"]]
        if y == 2027 and 37 <= w <= 40:
            res[i, RD.band(c["age"])] += 1
        if y <= 2026:
            hist[i, RD.band(c["age"])] += 1
    return res, hist


def sets_of(res, hist, L):
    pop, emp, W, names = L["pop"], L["emp"], L["W"], L["names"]
    out = {}
    for k, f in list(R.ROUTES_STEP.items()) + list(R.ROUTES_EASY.items()):
        out[k] = {names[i] for i in R.flagged(f(res, hist, pop, emp, W))}
    return out


def main():
    L = RD.load()
    names, res, hist, pop, emp, W = L["names"], L["res"], L["hist"], L["pop"], L["emp"], L["W"]
    canon = {RD.norm(n): n for n in names}
    rows = L["rows"]
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))

    # ---------------- R1: the field's raw material ships, the deciding quantity does not
    headers = {}
    for k, fn in B.FILES.items():
        if fn.endswith(".csv"):
            with open(p(k), encoding="utf-8") as f:
                headers[k] = next(csv.reader(f))
    banned = re.compile(r"infect|acquir|workplace|place_of|exposure|commut", re.I)
    check("R1 no column of any csv holds a place of infection or a workplace",
          not any(banned.search(h) for hs in headers.values() for h in hs), str(headers.get("line_list")))
    check("R1 the line list carries each case's age and home barangay at case grain",
          {"age_years", "barangay", "date_onset"} <= set(headers["line_list"]))
    wb = load_workbook(p("cbms"), read_only=True)
    check("R1 the CBMS workbook carries the place-of-work table at barangay grain", "Table 4" in wb.sheetnames)
    check("R1 the golden's decisive computation reads the case rows and Table 4",
          res.sum() > 600 and W[:, :len(names)].sum() > 0)

    # ---------------- the routes on the cut pack
    sets = sets_of(res, hist, L)
    for k in R.ROUTES_STEP:
        c = R.ROUTES_STEP[k](res, hist, pop, emp, W)
        mi, mo = R.margins(c, {names.index(n) for n in GOLD_NAMES})
        need = 3.5 if k == "fractional_0.5" else 6.0
        check("route %s files the golden with margins (inside %.1f, outside %.1f)" % (k, mi, mo),
              sets[k] == GOLD_NAMES and mi >= 12 and mo >= need)
    check("R3a the default path (home address) files the eight", sets["residence"] == DEFAULT_NAMES,
          str(sorted(sets["residence"])))
    check("R3a the default path's answer is not the golden", sets["residence"] != GOLD_NAMES)
    check("rung 2 the home-transmission marker files the two outbreaks alone",
          sets["local_marker"] == {"Bagumbayan", "Maligaya"}, str(sorted(sets["local_marker"])))
    # R3b: the default path with only the decisive step changed
    rows_ = cases_variant(rows, canon)
    r0, h0 = RD.aggregates(rows_, names)
    check("R3b the default's cleaning with only the placement changed files the golden",
          {names[i] for i in R.flagged(R.fractional(r0, h0, pop, emp, W, 0.6))} == GOLD_NAMES)
    rt = cases_variant(rows, canon, drop_travel=True)
    r1, h1 = RD.aggregates(rt, names)
    check("R3b rung 1 (travellers out) alone leaves the default's answer",
          {names[i] for i in R.flagged(R.residence(r1, h1, pop, emp, W))} == DEFAULT_NAMES)

    # R3a on the clean truth (the generator's world before any mess)
    cases, tables, rates = Wd.simulate_cases(B.WORLD_SEED)
    people = Wd.assign_attributes(cases, B.WORLD_SEED)
    ev = D.evaluate(people, tables)
    check("R3a on the clean truth: the design holds (every placement golden, easy routes off it, no shock interval)",
          not ev["fails"], str(ev["fails"][:3]))
    tr_res, tr_place = ev["res"], ev["place"]
    check("R3a on the clean truth: the true place-of-infection set is the golden",
          {Wd.NAMES[i] for i in R.flagged(tr_place)} == GOLD_NAMES)
    check("R3a on the clean truth: the home-address count misses San Roque",
          tr_res[Wd.SR].sum() < TRIGGER and tr_place[Wd.SR] > TRIGGER)

    # ---------------- R2: each Layer 1 item mishandled leaves the call
    variants = {
        "re-notified patients counted twice (SF2)": dict(merge=False),
        "other towns' residents kept at same-named barangays (SF3)": dict(other_towns=True),
        "classification by the first row, not the latest (axis 5)": dict(latest=False),
        "blank onsets dropped (SF5)": dict(drop_blank=True),
        "Santo Tomas Puroks 5 to 8 left under Santo Tomas (SF10)": dict(split=False),
        "travellers set aside (SF9)": dict(drop_travel=True),
        "cases dated by consultation week (SF4)": dict(week_by="consult"),
    }
    for label, kw in variants.items():
        cs = cases_variant(rows, canon, **kw)
        rr, hh = RD.aggregates(cs, names)
        st = sets_of(rr, hh, L)
        # the golden method and every member from a 0.6 share up; the half share is the family's weakest
        # member and is asserted on the plan's own readings above
        members = [k for k in R.ROUTES_STEP if k != "fractional_0.5"]
        ok = all(st[k] == GOLD_NAMES for k in members) and st["residence"] != GOLD_NAMES
        check("R2 %s: the inversion, the excess spread and every share from 0.6 still file the golden" % label, ok,
              str({k: sorted(v) for k, v in st.items() if v != GOLD_NAMES and k in members}))
    cs = cases_variant(rows, canon, not_a_case=True)
    rr, hh = RD.aggregates(cs, names)
    st = sets_of(rr, hh, L)
    check("SF1 Not a case counted as cases: the placements still file the golden (the plan rules it out anyway)",
          all(st[k] == GOLD_NAMES for k in R.ROUTES_STEP))
    ri, hi_ = iso_aggregates(rows_, names)
    st = sets_of(ri, hi_, L)
    check("SF7 ISO weeks instead of the plan's calendar: same call", all(st[k] == GOLD_NAMES for k in R.ROUTES_STEP))

    # ---------------- the fork rows that close by convergence
    for k in R.ROUTES_STEP:
        c = R.ROUTES_STEP[k](res, hist, pop, emp, W)
        if np.any(np.abs(c - TRIGGER) < 1.0):
            break
    else:
        k = None
    check("SF8 no barangay sits within one case of 40 under any placement (at least 40 and over 40 agree)", k is None)
    plan_txt = _pdf_text(p("plan"))
    check("SF11 the plan counts where cases were infected (4.3) and calls the line list's cases the city's residents (4.1)",
          "were infected in that barangay" in plan_txt and "dengue cases among the city's residents" in plan_txt)
    check("SF12 the outside-city column kept or dropped: same call",
          sets["fractional_0.6_outside_dropped"] == GOLD_NAMES and sets["fractional_1.0_outside_dropped"] == GOLD_NAMES)
    check("SF13 a working resident's share at work from a half to all of it: same call",
          all(sets["fractional_%s" % s] == GOLD_NAMES for s in ("0.5", "0.6", "0.7", "0.8", "1.0")))
    # SF14: working age 20 to 64 rather than 15 to 64
    res2 = np.zeros_like(res)
    hist2 = np.zeros_like(hist)
    idx = {n: k for k, n in enumerate(names)}
    for c in rows_:
        y, w = mw_of(c["onset"])
        b2 = 0 if c["age"] < 20 else (1 if c["age"] < 65 else 2)
        if y == 2027 and 37 <= w <= 40:
            res2[idx[c["barangay"]], b2] += 1
        if y <= 2026:
            hist2[idx[c["barangay"]], b2] += 1
    wbk = load_workbook(p("cbms"), data_only=True)["Table 1"]
    pop2 = []
    for row in wbk.iter_rows(min_row=6, values_only=True):
        if row[0] == "Dalisay City":
            break
        if row[0] and row[1] is not None:
            a = [0 if v in (None, "-") else int(v) for v in row[2:16]]
            pop2.append([sum(a[0:4]), sum(a[4:13]), a[13]])
    pop2 = np.array(pop2, dtype=float)
    st = {k: {names[i] for i in R.flagged(f(res2, hist2, pop2, emp, W))} for k, f in R.ROUTES_STEP.items()}
    check("SF14 working age from 20 rather than 15: same call", all(v == GOLD_NAMES for v in st.values()),
          str({k: sorted(v) for k, v in st.items() if v != GOLD_NAMES}))
    # SF15: the history behind the usual age mix taken from the same weeks only
    hist3 = np.zeros_like(hist)
    for c in rows_:
        y, w = mw_of(c["onset"])
        if y <= 2026 and 37 <= w <= 40:
            hist3[idx[c["barangay"]], RD.band(c["age"])] += 1
    check("SF15 the usual age mix from weeks 37 to 40 of 2022 to 2026 only: same call",
          {names[i] for i in R.flagged(R.excess_spread(res, hist3, pop, emp, W))} == GOLD_NAMES and
          {names[i] for i in R.flagged(R.inversion(res, hist3, pop, emp, W))} == GOLD_NAMES)
    latest = {}
    for r in rows:
        latest[r["case_no"]] = r
    sus = [c for c in rows_ if latest[c["case_no"]]["case_classification"] in ("Suspect", "S")
           and mw_of(c["onset"])[0] == 2027 and 37 <= mw_of(c["onset"])[1] <= 40]
    check("SF16 the window's unclassified suspects are counted, as plan 4.1 counts every notification not classified "
          "Not a case (%d of them)" % len(sus), len(sus) > 0 and sum(res.sum(1)) == len([c for c in rows_ if mw_of(c["onset"])[0] == 2027 and 37 <= mw_of(c["onset"])[1] <= 40]))
    check("SF6 the export holds no report after 10 October 2027",
          max(RD.parse_date(r["date_reported"]) for r in rows) <= dt.date(2027, 10, 10))

    # ---------------- shock: the golden set is not an interval of any sort
    tot = res.sum(1)
    gidx = {names.index(n) for n in GOLD_NAMES}
    prev, _ = RD.aggregates(rows_, names, weeks=(33, 36))
    sorts = {"home-address count": tot, "rate per resident": tot / pop.sum(1),
             "working-age share": res[:, 1] / np.maximum(tot, 1), "growth on weeks 33 to 36": (tot + 1) / (prev.sum(1) + 1),
             "children's cases": res[:, 0]}
    for nm, v in sorts.items():
        check("shock: the golden set is not an interval of the %s" % nm,
              not D.is_interval(v, gidx) and not D.is_interval(-np.asarray(v, dtype=float), gidx))

    # ---------------- separation: the ask files are not the call's, the call's files cannot rebuild the asks
    check("separation: the line list cannot rebuild ask A (admissions by hospital and week)",
          _linelist_admissions(rows) != (fig["dmc_admissions"], fig["ddh_admissions"]))
    src = open(os.path.join(HERE, "reader.py"), encoding="utf-8").read()
    opened = [fn for fn in B.FILES.values() if fn in src]
    check("separation: the call's reader opens only the line list and the CBMS workbook, never an ask file",
          sorted(opened) == sorted([B.FILES["line_list"], B.FILES["cbms"]]), str(opened))

    # ---------------- the asks: golden equals the generator's truth, every wrong stop misses
    gd, go, gl, gb = CE.gold()
    check("ask A golden equals the figures (DMC)", {str(k): v for k, v in gd.items()} == fig["dmc_admissions"])
    check("ask A golden equals the figures (DDH)", {str(k): v for k, v in go.items()} == fig["ddh_admissions"])
    seg = CE.dmc_by_segment()
    once = CE.dmc_by_patient()
    check("ask A DMC: every segment an admission misses every week", all(seg[w] != gd[w] for w in gd))
    check("ask A DMC: a patient once by hospital number misses most weeks", sum(once[w] != gd[w] for w in gd) >= 5)
    ddh_all = CE.ddh_all_by_date()
    check("ask A DDH: every row by its date misses most weeks", sum(ddh_all[w] != go[w] for w in go) >= 6)
    bh = [b for b in gl if b in __import__("asks").TEAM_B]
    lv = CE.larval(False)
    check("ask B BHW: houses by number across puroks miss every barangay", all(abs(lv[b] - gl[b]) >= 0.05 for b in bh))
    check("ask B golden equals the figures", gl == fig["house_index"])
    lab0 = CE.lab(True, False)
    check("ask C IgM: first positive by laboratory reference misses every week",
          all(lab0[("IgM", w)] != gb[("IgM", w)] for w in CE.LW))
    lab1 = CE.lab(False, True)
    check("ask C NS1: rejected runs left in miss at least four weeks", sum(lab1[("NS1", w)] != gb[("NS1", w)] for w in CE.LW) >= 4)
    # bins: house indices away from their rounding edges
    raw = _larval_raw()
    edge = min(0.05 - abs(v - round(v, 1)) for v in raw.values())
    check("bins: every house index at least 0.005 from a rounding edge (tightest %.4f)" % edge, edge >= 0.005)
    pc, ml, kept, n = _ceiling_quiet()
    check("ask layer: pair ceiling at or under 60 (%.1f) and mirror leakage under 50 per cent (%.1f)" % (pc, ml),
          pc <= 60 and ml < 50)

    # ---------------- input gates
    files = sorted(os.listdir(TARGET))
    check("gate: 10 or more files (%d)" % len(files), len(files) >= 10)
    check("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    check("gate: one file of 25,000 rows or more (line list %d)" % len(rows), len(rows) >= 25000)
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json"), encoding="utf-8"))
    check("gate: two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
    import inspect
    golden_src = src + open(os.path.join(HERE, "ceiling.py"), encoding="utf-8").read() + "".join(
        inspect.getsource(f) for f in (B.golden_dmc, B.golden_ddh, B.golden_larval, B.golden_lab, B.dmc_transfers_out))
    check("gate: no distractor is read by the golden or any ask (and deleting them moves nothing)",
          not any(('"%s"' % k) in golden_src or B.FILES[k] in golden_src for k in B.DISTRACTORS))
    check("gate: no file under target/ describes the data", not any(re.search(r"readme|dictionary|manifest|notes|codebook", f, re.I)
                                                                     for f in files))

    # ---------------- documents read back, with positive controls on the same path
    plan = _pdf_text(p("plan"))
    check("plan: positive control, the trigger sentence is read", "40 or more of those cases were infected in that barangay" in plan)
    check("plan: positive control, the house index definition is read", "larvae or pupae were found in at least one container" in plan)
    check("plan: names no workplace, travel, biting hours or place-of-work table",
          not re.search(r"workplace|place of work|commut|bite|biting|daytime|daylight|estate", plan, re.I))
    bull = _pdf_text(p("bulletin"))
    check("bulletin: positive control read, and it carries no barangay", "Dalisay City" in bull and
          not any(n in bull for n in BESIDE + ["San Roque", "Bagumbayan", "Maligaya"]))

    # ---------------- the goldens read back
    gb_txt = _pdf_text(os.path.join(B.GOLDEN, "dengue_hotspots_mw41_44_2027.pdf"))
    check("golden brief: positive control, the decision sentence is read",
          "Send the hotspot response to San Roque, Bagumbayan and Maligaya" in gb_txt)
    gcsv = list(csv.DictReader(open(os.path.join(B.GOLDEN, "response_figures_2027.csv"), encoding="utf-8")))
    check("golden csv: 40 figures, each equal to figures.json", len(gcsv) == 40 and all(
        (fig["dmc_admissions"] if r["item"] == "Dalisay Medical Center" else fig["ddh_admissions"])[r["morbidity_week"]] == int(r["value"])
        for r in gcsv if r["figure"] == "dengue_admissions"))

    # ---------------- realism sweep
    hn = sorted({int(r["hospital_no"]) for r in csv.DictReader(open(p("dmc"), encoding="utf-8"))})
    check("realism: DMC hospital numbers are not an arithmetic sequence", len(set(np.diff(hn))) > 5)
    sp = sorted(int(r["specimen_id"][2:]) for r in csv.DictReader(open(p("lab"), encoding="utf-8")))
    check("realism: specimen numbers are not an arithmetic sequence", len(set(np.diff(sorted(set(sp))))) > 2)
    weekly = Counter((mw_of(c["onset"])) for c in rows_)
    check("realism: no two morbidity weeks share an identical count across the whole 2027 season run",
          len({weekly[(2027, w)] for w in range(28, 41)}) >= 9)
    check("realism: the CBMS city totals are not round", int(pop.sum()) % 100 != 0)
    order_codes = [r["barangay"] for r in csv.DictReader(open(p("register"), encoding="utf-8"))]
    check("realism: the register's code order is not the alphabet", order_codes != sorted(order_codes))

    bad = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if (detail and not ok) else ""))
    print("%d of %d checks pass" % (len(RESULTS) - len(bad), len(RESULTS)))
    return 1 if bad else 0


def _linelist_admissions(rows):
    c = {"Dalisay Medical Center": Counter(), "Dalisay Doctors' Hospital": Counter()}
    for r in rows:
        if r["admitted"] == "Y" and r["report_status"] == "New" and r["reporting_unit"] in c:
            d = RD.parse_date(r["date_admitted"]) or RD.parse_date(r["date_consult"])
            y, w = mw_of(d)
            if y == 2027 and 33 <= w <= 40:
                c[r["reporting_unit"]][w] += 1
    return ({str(w): c["Dalisay Medical Center"][w] for w in range(33, 41)},
            {str(w): c["Dalisay Doctors' Hospital"][w] for w in range(33, 41)})


def _larval_raw():
    rows = list(csv.DictReader(open(p("larval"), encoding="utf-8")))
    houses = {}
    for r in rows:
        key = (r["barangay"], r["purok"], r["household_code"])
        pos = (r["larvae"] == "Y" or r["pupae"] == "Y") if r["team"] == "VCU" else int(r["containers_positive"] or 0) > 0
        houses[key] = houses.get(key, False) or pos
    out = {}
    for b in sorted(set(k[0] for k in houses)):
        hs = [v for k, v in houses.items() if k[0] == b]
        out[b] = 100.0 * sum(hs) / len(hs)
    return out


def _ceiling_quiet():
    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        return CE.main()


def _pdf_text(path):
    with pdfplumber.open(path) as pdf:
        text = " ".join((pg.extract_text() or "") for pg in pdf.pages)
    return re.sub(r"\s+", " ", text)


def note_figures():
    """The design note's derived figures, printed from the cut pack (no assertion, so the check count is unchanged)."""
    L = RD.load()
    names, res, hist, pop, emp, W = L["names"], L["res"], L["hist"], L["pop"], L["emp"], L["W"]
    six = [names.index(n) for n in ("Tabing-Ilog", "Pulong Bayabas", "Malinta", "Kanluran", "Burol", "Silangan")]
    sr = names.index("San Roque")
    gold = {names.index(n) for n in GOLD_NAMES}
    tot = res.sum(1)
    over = sorted((i for i in range(len(names)) if tot[i] >= TRIGGER), key=lambda i: -tot[i])
    print("note: by home address %d barangays at %d or more (%d to %d): %s; the six beside the estate %d to %d" % (
        len(over), TRIGGER, min(tot[over]), max(tot[over]), ", ".join(names[i] for i in over),
        min(tot[six]), max(tot[six])))
    fam = {k: f(res, hist, pop, emp, W) for k, f in R.ROUTES_STEP.items()}
    for k, c in fam.items():
        lo = min(gold, key=lambda i: c[i])
        hi = max((i for i in range(len(names)) if i not in gold), key=lambda i: c[i])
        print("note: %-31s San Roque %.1f; lowest in %s %.1f; highest out %s %.1f" % (
            k, c[sr], names[lo], c[lo], names[hi], c[hi]))
    print("note: across the step family San Roque %.1f to %.1f, the six %.1f to %.1f" % (
        min(c[sr] for c in fam.values()), max(c[sr] for c in fam.values()),
        min(c[i] for c in fam.values() for i in six), max(c[i] for c in fam.values() for i in six)))
    print("note: the six's window cases aged 0 to 14 run %d to %d, aged 15 to 64 %d to %d" % (
        res[six, 0].min(), res[six, 0].max(), res[six, 1].min(), res[six, 1].max()))
    send = sorted((i for i in range(len(names)) if i != sr), key=lambda i: -emp[i] * W[i, sr])[:7]
    print("note: the barangays sending the most employed residents to San Roque (CBMS Tables 3 and 4): %s" % (
        ", ".join("%s %d (%.0f per cent)" % (names[i], round(emp[i] * W[i, sr]), 100 * W[i, sr]) for i in send)))
    ex = R._excess(res, hist)
    print("note: working-age excess %.0f cases city-wide, %.0f in the six; the six's working-age cases %d, "
          "Poisson spread %.1f a barangay" % (ex.sum(), ex[six].sum(), res[six, 1].sum(), np.sqrt(res[six, 1].mean())))


if __name__ == "__main__":
    rc = main()
    note_figures()
    sys.exit(rc)
