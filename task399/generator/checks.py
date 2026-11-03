"""The generator's assertions for task399: every semantic fork (SF1 to SF10), the ladder on the clean truth, the
three-rules block (the analyst test executed), every graded figure's bin edge, the separation of the ask devices
from the main population, the device masses, the input gates and the realism screens. Exit 1 on any failure.

    python3 task399/generator/checks.py
"""
import csv
import json
import math
import os
import sys

import datetime as dt

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import figs as F    # noqa: E402
import world as W   # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def gap(df):
    return F.gap(df)


def main():
    w = W.build_world()
    fa = w["first"].copy()
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    f = F.main_figures(fa)

    # ---------------------------------------------------------------- structure and the ladder on the clean truth
    st = F.structure_ok(f)
    for k, v in st.items():
        check("structure: " + k, v)
    # R0: EM bail is never decided at a first appearance (every EM order sits on a later appearance)
    later = w["later"]
    em_first = later[(later.outcome.str.contains("EM bail"))]
    check("R0 dies: no first appearance carries an EM order", (em_first.appearance_type != "First appearance (custody)").all()
          and len(em_first) > 0, "%d EM orders, all on later appearances" % len(em_first))
    # R1: the field's method, within court and officer with the legally relevant controls, names the magistrate
    d = fa.copy()
    d["none"] = 1 - d["own"]
    d["p2"] = (d.period == "P2").astype(int)
    d["lpri"] = np.log1p(d["pri"])
    d["oc"] = d["court"] + "|" + d["officer"]
    kb2 = d[(d.court == "KB") & (d.period == "P2")].copy()
    kb2["mag"] = (kb2.officer == W.MAGISTRATE).astype(int)
    m1 = smf.ols("ric ~ none*mag + C(ser) + lpri + fta + onb + fv + nfa", data=kb2).fit()
    eff, se = 100 * m1.params["none:mag"], 100 * m1.bse["none:mag"]
    check("R1 lands on the magistrate (within-officer, controls)", eff > 4 * se and eff > 8,
          "none x magistrate %.1f points (SE %.1f)" % (eff, se))
    # R2 (decisive): with the AVL-time calls in the same model the magistrate carries nothing of his own
    kb2["avl"] = kb2["during_avl"]
    m2 = smf.ols("ric ~ none*mag + none*avl + C(ser) + lpri + fta + onb + fv + nfa", data=kb2).fit()
    check("R2 the magistrate's own term vanishes beside the AVL-time term",
          abs(100 * m2.params["none:mag"]) < 2.5 * 100 * m2.bse["none:mag"] and 100 * m2.params["none:avl"] > 25,
          "none x magistrate %.1f (SE %.1f), none x AVL time %.1f" % (100 * m2.params["none:mag"],
                                                                      100 * m2.bse["none:mag"],
                                                                      100 * m2.params["none:avl"]))
    check("R2 the AVL split carries the widening", f["region_widening_rest"] <= 0.25 * f["region_widening"],
          "%.2f of %.2f left once the AVL-time calls are set apart" % (f["region_widening_rest"],
                                                                         f["region_widening"]))
    # analyst test (dataset-generation 7.1): the easy route on the clean truth files the wrong initiative
    easy = "a judge on the Kestrel Bay custody list" if eff > 8 else "other"
    check("three rules: the analyst test's easy route files a judge on the custody list", easy.startswith("a judge"))
    check("three rules: the decisive route files the duty lawyer roster",
          f["kb_avl_gap"] - f["kb_other_gap"] > 25 and abs(f["kb_other_mag_gap"] - f["kb_other_judges_gap"]) <= 3)

    # ---------------------------------------------------------------- semantic forks
    app = pd.read_csv(os.path.join(TARGET, "cms_appearances_oct2024_sep2026.csv"), dtype=str, keep_default_na=False)
    fa_p = app[app.AppearanceType == "First appearance (custody)"]
    # SF1: every custody-list appearance (later in-person remand appearances included) keeps the call
    alt = app[(app.List == "Custody")].copy()
    alt["own"] = (alt.CounselOfRecord != "").astype(int)
    alt["ric"] = (alt.Outcome.str.startswith("Remanded in custody")).astype(int)
    alt["date"] = pd.to_datetime(alt.AppearanceDate).dt.date
    alt["period"] = ["P1" if x < W.P2_START else "P2" for x in alt["date"]]
    key = fa[["crn", "during_avl"]].rename(columns={"crn": "CRN"})
    alt = alt.merge(key, on="CRN", how="left")
    alt["during_avl"] = np.where(alt.AppearanceType == "First appearance (custody)", alt["during_avl"].fillna(0), 0)
    wide = gap(alt[alt.period == "P2"]) - gap(alt[alt.period == "P1"])
    rest = alt[alt.during_avl == 0]
    wide_rest = gap(rest[rest.period == "P2"]) - gap(rest[rest.period == "P1"])
    check("SF1 every custody-list appearance: same call", wide_rest <= 0.4 * wide and wide > 3,
          "widening %.2f, %.2f left once the AVL-time calls are set apart" % (wide, wide_rest))
    # SF2: the custody outcome at a first appearance has one code
    outs = set(fa_p.Outcome)
    check("SF2 one custody outcome code at first appearance",
          outs == {"Remanded in custody", "Remanded on bail", "Remanded at large", "Convicted and sentenced"},
          ", ".join(sorted(outs)))
    # SF3: counsel per appearance equals the truth at that appearance
    own_p = (fa_p.CounselOfRecord != "").astype(int).values
    tr = fa.set_index("crn").loc[fa_p.CRN.values, "own"].values
    check("SF3 counsel of record is the appearance's own", (own_p == tr).all())
    # SF4: the local appearance date is the call's New Zealand date
    ok4 = all(c[:10] == d for c, d in zip(fa_p.CalledAt, fa_p.AppearanceDate))
    check("SF4 the appearance date is the New Zealand date of the call", ok4)
    # SF5: a ratio of shares names the same leaf
    def ratio(df):
        r = df.groupby("own")["ric"].mean()
        return float(r.get(0) / r.get(1))
    kbp2 = fa[(fa.court == "KB") & (fa.period == "P2")]
    r_av, r_ot = ratio(kbp2[kbp2.during_avl == 1]), ratio(kbp2[kbp2.during_avl == 0])
    check("SF5 a ratio of the shares: same call", r_av > 1.4 and abs(r_ot - 1) < 0.15,
          "AVL-time ratio %.2f, other calls %.2f" % (r_av, r_ot))
    # SF6: the change net of the legally relevant factors: same call
    m3 = smf.ols("ric ~ none*p2 + C(ser) + lpri + fta + onb + fv + nfa + C(oc)", data=d).fit()
    d["avl"] = d["during_avl"]
    m4 = smf.ols("ric ~ none*p2 + none*avl + C(ser) + lpri + fta + onb + fv + nfa + C(oc)", data=d).fit()
    check("SF6 adjusted widening: same call", 100 * m3.params["none:p2"] > 3 and
          abs(100 * m4.params["none:p2"]) <= 0.35 * 100 * m3.params["none:p2"],
          "adjusted widening %.2f, %.2f beside the AVL-time term" % (100 * m3.params["none:p2"],
                                                                      100 * m4.params["none:p2"]))
    # SF7: the extract carries the hearing court only
    check("SF7 one court field, the hearing court", "Court" in app.columns and "PoliceDistrict" not in app.columns)
    # SF8: no custody call on an AVL window's start minute or between its last call and its rising
    bad8 = 0
    for a in w["avl"].itertuples(index=False):
        calls = fa[(fa.court == "KB") & (fa.date == a.date)].call_min
        m1, m2 = W.avl_margins(a.date)
        bad8 += int((((calls >= a.start) & (calls < a.start + m1)) | ((calls > a.end - m2) & (calls < a.end))).sum())
    check("SF8 the calendar window and the AVL list's own calls classify alike", bad8 == 0, "%d edge calls" % bad8)
    # SF9: removes it, under the remands-avoided reading too
    no = kbp2[kbp2.own == 0]
    avoided_dl = (no[no.during_avl == 1].ric.mean() - no[no.during_avl == 0].ric.mean()) * (no.during_avl == 1).sum()
    oth = no[no.during_avl == 0]
    mag = oth.officer == W.MAGISTRATE
    avoided_judge = max(0.0, (oth[mag].ric.mean() - oth[~mag].ric.mean()) * mag.sum())
    check("SF9 the remands-avoided reading: same call", avoided_dl > 3 * max(avoided_judge, 1.0),
          "duty lawyer roster %.0f remands, a judge on the list %.0f" % (avoided_dl, avoided_judge))
    # SF10: one row per case at first appearance
    check("SF10 one first appearance per case", fa_p.CRN.is_unique, "%d first appearances" % len(fa_p))

    # ---------------------------------------------------------------- bins (edge distance, every graded figure)
    units = figs["_units"]
    tight = None
    for k, u in units.items():
        v = float(figs[k])
        if u >= 1 and float(v).is_integer():
            continue
        e = F.edge(v, u)
        if tight is None or e < tight[1]:
            tight = (k, e)
        check("bin %s" % k, e >= 0.07, "%.4f of a bin from its edge" % e)
    check("tightest graded figure", tight[1] >= 0.07, "%s at %.3f of a bin" % tight)

    # ---------------------------------------------------------------- separation and device mass
    check("separation: no ask device row in the main population",
          not fa_p.Outcome.str.contains("EM bail").any())
    sys.path.insert(0, HERE)
    import ceiling as C
    cr = {}
    cr.update(C.em_cracker(TARGET))
    cr.update(C.bh_cracker(TARGET))
    for k in [k for k in units if k.startswith(("em_", "bh_"))]:
        dist = abs(cr[k] - float(figs[k])) / units[k]
        check("device mass %s" % k, dist >= 3, "the careful route %.1f bins off" % dist)

    # ---------------------------------------------------------------- input gates and realism
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(x)[1] for x in files}
    check("input gate: ten or more files", len(files) >= 10, "%d files" % len(files))
    check("input gate: three or more formats", len(exts) >= 3, ", ".join(sorted(exts)))
    check("input gate: a file of 25,000 rows or more", len(app) >= 25000, "%d appearance rows" % len(app))
    meta = os.path.join(TASK, "metadata.json")
    if os.path.exists(meta):
        md = json.load(open(meta))
        check("input gate: two or more distractors named", len(md.get("distractor_files", [])) >= 2)
        for dfile in md.get("distractor_files", []):
            check("distractor %s unread by the golden" % dfile,
                  os.path.basename(dfile) not in open(os.path.join(HERE, "verify.py")).read())
        named = {x["file"] for x in md.get("files", [])}
        check("metadata: every file has provenance", set(files) <= named, ", ".join(sorted(set(files) - named)))
    inc = list(csv.DictReader(open(os.path.join(TARGET, "bail_house_incidents.csv"), encoding="utf-8")))
    check("realism: no em dash in any text file", all(chr(0x2014) not in open(os.path.join(TARGET, x), encoding="utf-8",
                                                                                errors="ignore").read()
                                                      for x in files if x.endswith(".csv")))
    check("realism: incidents carry UTC stamps", all(e["ReportedAt"].endswith("Z") for e in inc))

    # realism sweep: no identifier column steps by one constant amount; no attribute dealt round-robin
    def const_step(vals):
        nums = sorted({int("".join(ch for ch in v if ch.isdigit())[-6:] or 0) for v in vals if v})
        steps = {b - a for a, b in zip(nums, nums[1:])}
        return len(nums) > 20 and len(steps) == 1
    em_case = list(csv.DictReader(open(os.path.join(TARGET, "em_case_system_assessments.csv"), encoding="utf-8")))
    for name, vals in (("PersonId", list(app.PersonId)), ("OrderRef", [r["OrderRef"] for r in em_case]),
                       ("IncidentId", [e["IncidentId"] for e in inc]), ("Placement", [e["Placement"] for e in inc])):
        check("realism: %s does not step by one constant amount" % name, not const_step(vals))
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(TARGET, "duty_lawyer_returns_2025-26.xlsx"), read_only=True)["Returns"]
    kb = [r[2] for r in ws.iter_rows(min_row=2, values_only=True) if r[0] == "Kestrel Bay"]
    periodic = any(all(kb[i] == kb[i + p] for i in range(len(kb) - p)) for p in range(1, 9))
    check("realism: the Kestrel Bay duty lawyer is not dealt round-robin", not periodic and len(set(kb)) >= 3)
    # R2: each mess item on the main path is neutral; dropping the offset leaves every call time where it was
    loc = [c[11:16] for c in fa_p.CalledAt]
    tru = ["%02d:%02d" % divmod(int(m), 60) for m in fa.set_index("crn").loc[fa_p.CRN.values, "call_min"]]
    check("R2 the offset on CalledAt is the local clock: dropping it moves no call", loc == tru)
    cal = load_workbook(os.path.join(TARGET, "court_sitting_calendar_2024-2026.xlsx"), read_only=True)["Sittings"]
    avl_days = {r[1].date() for r in cal.iter_rows(min_row=2, values_only=True) if r[3] == "AVL remand list"}
    kb2_days = set(pd.to_datetime(app[(app.Courtroom == "KBY-2")].AppearanceDate).dt.date)
    check("R2 the calendar's Courtroom 2 is the extract's KBY-2 on every AVL sitting", avl_days == kb2_days,
          "%d sittings" % len(avl_days))
    # the coordinator's cheap routes to the roster, each measured: none names it without the call-time overlap
    first_avl = min(w["avl"].date)
    first_mag = min(fa[fa.officer == W.MAGISTRATE].date)
    check("cheap route (a): the AVL list's first sitting is the magistrate's, so its date names both",
          abs((first_avl - first_mag).days) <= 3, "%s against %s" % (first_avl, first_mag))
    hrs = {}
    for fy in ("2024-25", "2025-26", "2026-27"):
        wsr = load_workbook(os.path.join(TARGET, "duty_lawyer_returns_%s.xlsx" % fy), read_only=True)["Returns"]
        it = wsr.iter_rows(values_only=True)
        hdr = list(next(it))
        for row in it:
            r = dict(zip(hdr, row))
            court = r.get("Court")
            day = (r.get("Date") or r.get("Sitting date")).date()
            if str(court).startswith("Kestrel Bay"):
                hrs[day] = float(r.get("Hours") or r.get("Hours claimed"))
        check("cheap route (c): the %s returns carry no defendant count or name" % fy,
              not any("efendant" in str(h) or "assisted" in str(h).lower() for h in hdr), ", ".join(map(str, hdr)))
    kbu = app[(app.Court == "KBY") & (app.CounselOfRecord == "") & (app.List.isin(["Custody", "AVL remand"]))].copy()
    kbu["d"] = pd.to_datetime(kbu.AppearanceDate).dt.date
    per = kbu.groupby("d").size()
    def mph(lo, hi):
        days = [d for d in per.index if lo <= d <= hi and d in hrs]
        return sum(per[d] for d in days) / sum(hrs[d] for d in days)
    a, b = mph(W.START, W.P2_START - dt.timedelta(days=1)), mph(W.REORG, W.END)
    check("cheap route (b): unrepresented matters per duty lawyer hour at Kestrel Bay hold level",
          abs(b / a - 1) <= 0.10, "%.2f a claimed hour before, %.2f from December 2025" % (a, b))
    check("R3c no copied block: no two Kestrel Bay sitting days share a call sequence",
          fa[fa.court == "KB"].groupby("date").call_min.apply(tuple).duplicated().sum() == 0)

    # H1 and H13: each workbook and PDF carries its own saved stamp, created no later than modified
    import re as _re
    import zipfile as _zf
    stamps = []
    for x in files + ["../golden/" + g for g in sorted(os.listdir(os.path.join(TASK, "golden")))]:
        pth = os.path.normpath(os.path.join(TARGET, x))
        if x.endswith(".xlsx"):
            core = _zf.ZipFile(pth).read("docProps/core.xml").decode()
            app_xml = _zf.ZipFile(pth).read("docProps/app.xml").decode()
            cr = _re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1)
            mo = _re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
            check("H1 %s names its owner, not the writing library" % os.path.basename(x),
                  "openpyxl" not in core + app_xml and "<Application>Microsoft Excel</Application>" in app_xml)
            nsheets = len(_zf.ZipFile(pth).read("xl/workbook.xml").decode().split("<sheet ")) - 1
            check("H1 %s app.xml lists its %d sheets" % (os.path.basename(x), nsheets),
                  app_xml.count("<vt:lpstr>") >= nsheets)
            stamps.append((os.path.basename(x), cr, mo))
        elif x.endswith(".pdf"):
            from pypdf import PdfReader
            r = PdfReader(pth)
            cr, mo = str(r.metadata.get("/CreationDate")), str(r.metadata.get("/ModDate"))
            lenient = " ".join((p.extract_text() or "") for p in r.pages)
            strict = " ".join((p.extract_text() or "") for p in PdfReader(pth, strict=True).pages)
            check("H25 %s reads the same strictly and leniently" % os.path.basename(x), lenient == strict and lenient)
            check("H1 %s carries no library banner" % os.path.basename(x),
                  b"ReportLab" not in open(pth, "rb").read() and b"matplotlib" not in open(pth, "rb").read())
            stamps.append((os.path.basename(x), cr, mo))
    check("H13 every document's created stamp is its own", len({s[1] for s in stamps}) == len(stamps),
          ", ".join("%s %s" % (s[0], s[1]) for s in stamps if [t[1] for t in stamps].count(s[1]) > 1))
    check("H13 no document modified before it was created",
          all(s[1].replace("D:", "")[:14] <= s[2].replace("D:", "")[:14] for s in stamps if s[1] and s[2]))
    check("H9 no file under target/ describes the pack",
          not any(_re.search(r"readme|dictionar|manifest|field.?notes|codebook|schema", x, _re.I) for x in files))

    bad = [r for r in RESULTS if not r[1]]
    for name, ok, detail in RESULTS:
        if not ok or os.environ.get("VERBOSE"):
            print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, detail))
    print("checks: %d of %d pass" % (len(RESULTS) - len(bad), len(RESULTS)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
