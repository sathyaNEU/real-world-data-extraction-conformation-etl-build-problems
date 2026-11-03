"""The generator's assertions: the three rules on the clean truth, every rung, every fork row, every ask against
the truth, the mess one item at a time, the realism sweep and the input gates. LOG carries each check's line."""
import datetime as dt
import os
import re
import shutil
import tempfile
import zipfile

import numpy as np
import pandas as pd

import pack as PK
import params as P
import solve as SV

LOG = []
TEAMS = SV.TEAMS


def ok(label, cond, detail=""):
    assert cond, "%s FAILED %s" % (label, detail)
    LOG.append("%s  %s" % (label, detail))


def edge(v, unit):
    """distance from v to the nearest rounding edge at the printed unit"""
    c = round(v / unit) * unit
    return unit / 2 - abs(v - c)


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", x))


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(pg.extract_text() or "" for pg in PdfReader(path).pages)


def run(target, golden, W, S, A):
    del LOG[:]
    pp, tp = W["people"], W["tip"]
    ros = S["roster"]
    M = S["main"]
    cur = pp[pp.left.isna()]
    team_of = dict(zip(cur.index, cur.team_end))

    # ----------------------------------------------------------------- input gates and the no-helper rule
    files = PK.walk(target) if hasattr(PK, "walk") else None
    files = []
    for root, _, fs in os.walk(target):
        for f in fs:
            files.append(os.path.relpath(os.path.join(root, f), target))
    ok("gate.files", len(files) >= 10, "%d files" % len(files))
    fm = sorted({f.rsplit(".", 1)[1] for f in files})
    ok("gate.formats", len(fm) >= 3, ",".join(fm))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
    ok("gate.volume", big >= 25000, "largest csv %d rows" % big)
    ok("gate.distractors", len(PK.DISTRACTORS) >= 2 and all(os.path.exists(os.path.join(target, PK.F[k]))
                                                             for k in PK.DISTRACTORS), str(PK.DISTRACTORS))
    bad = [f for f in files if re.search(r"(?i)readme|dictionary|codebook|manifest|notes|field_guide|schema", f)]
    ok("gate.no_helper_file", not bad, str(bad))
    for f in files:
        if f.endswith((".csv", ".eml")):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            assert chr(0x2014) not in txt and chr(0x2013) not in txt, f
    ok("gate.no_em_dash_in_text_files", True, "%d text files" % sum(f.endswith((".csv", ".eml")) for f in files))

    # ----------------------------------------------------------------- the clean truth's own order
    t26 = tp[(tp.ts.dt.tz_convert("Europe/London").dt.year == 2026) & ~tp.cancelled & tp.pid.isin(cur.index)].copy()
    t26["team"] = t26.pid.map(team_of)
    true_novel = t26[t26.k == 0].groupby("team").p_hit.mean()
    true_order = list(true_novel.sort_values().index)
    ok("truth.order", true_order == A["order"], "true first-meeting chance %s" % true_novel.round(3).to_dict())
    # the true chance of a member on a brand-new image, averaged over the members (independent of what they met)
    skill = cur.groupby("team_end").skill.mean().sort_values()
    ok("truth.skill_order", list(skill.index) == A["order"], "mean member skill order %s" % list(skill.index))

    # ----------------------------------------------------------------- R1: the field's raw material ships
    ct26 = pd.read_csv(os.path.join(target, PK.F["ct26"]), nrows=5)
    pbh = pd.read_csv(os.path.join(target, PK.F["pb"]), skiprows=3, nrows=5)
    cols = [c.lower() for c in list(ct26.columns) + list(pbh.columns)]
    ok("R1.projection_rows", {"tip_image", "operator_login", "result"} <= set(ct26.columns)
       and {"Image", "Operator", "Result"} <= set(pbh.columns), "image, operator and result on every projection row")
    ok("R1.no_deciding_column", not any(re.search(r"first|prior|repeat|seen|met|familiar|exposure", c) for c in cols),
       "no shipped column marks an earlier meeting")
    ok("R1.history_ships", all(os.path.exists(os.path.join(target, PK.F[k])) for k in ("ct24", "ct25")),
       "the 2024 and 2025 exports ship beside 2026")

    # ----------------------------------------------------------------- R3a / R3b on the clean truth
    raw_truth = t26.groupby("team").hit.mean()
    ok("R3a.easy_route_wrong", raw_truth.idxmin() == "Brook" and A["order"][0] == "Fell",
       "clean truth, every projection: %s first; golden %s" % (raw_truth.idxmin(), A["order"][0]))
    one_step = t26[t26.k == 0].groupby("team").hit.mean()
    ok("R3b.decisive_step_alone", list(one_step.sort_values().index) == A["order"],
       "clean truth, the easy route with first meetings only: %s" % list(one_step.sort_values().index))
    ok("R3c.no_plant", True, "no copied block, no decoy document, no stakeholder figure; asserted below by the sweep")

    # ----------------------------------------------------------------- the ladder on the pack
    R = S["rungs"]
    first = lambda s: list(s.sort_values(kind="mergesort").index)[0]
    ok("rung0.raw", first(R["R0 raw"]) == "Brook", "every 2026 projection: %s" % R["R0 raw"].round(3).to_dict())
    ok("rung1.dprime", first(R["R1 dprime"]) == "Esk", "d-prime: %s" % R["R1 dprime"].round(3).to_dict())
    for tph in (80.0, 120.0, 200.0, 300.0):
        d = SV.rung_dprime(M["t"], S["B"]["golden"], S["A"]["golden"], tph)
        assert first(d) == "Esk", (tph, d.to_dict())
    ok("rung1.dprime_any_tray_rate", True, "Esk first at 80, 120, 150, 200 and 300 trays a screen-hour")
    ok("rung2.logit_area_class", first(R["R2 logit area class"]) == "Brook", R["R2 logit area class"].round(3).to_dict())
    ok("rung3.logit_practice", first(R["R3 logit practice"]) == "Brook", R["R3 logit practice"].round(3).to_dict())
    ok("rung4.central_only", first(R["R4 central only"]) == "Brook" and "Fell" not in R["R4 central only"].index,
       "Fell has no Central projection")
    for k in ("G first meetings", "G member mean", "G logit met"):
        assert list(R[k].sort_values(kind="mergesort").index) == A["order"], (k, R[k].to_dict())
    ok("golden.family_unanimous", True, "pooled first meetings, the member mean and the logit with earlier meetings "
       "all give %s" % A["order"])
    g = R["G first meetings"].sort_values()
    gaps = np.diff(g.values)
    ok("golden.margins", gaps.min() >= 0.03, "adjacent gaps %s" % np.round(gaps, 4).tolist())
    fam = pd.DataFrame({k: R[k] for k in ("G first meetings", "G member mean", "G logit met")})
    spread = (fam.max(axis=1) - fam.min(axis=1)).max()
    ok("golden.family_spread_under_gap", spread < gaps.min(), "largest family spread %.4f against the smallest gap %.4f"
       % (spread, gaps.min()))
    ok("golden.fell_far_below", g.iloc[1] - g.iloc[0] >= 0.045, "Fell %.4f, %s %.4f" % (g.iloc[0], g.index[1], g.iloc[1]))
    raw = R["R0 raw"].sort_values()
    ok("shock.fell_mid_raw", list(raw.index).index("Fell") in (2, 3), "Fell's place on every projection: %d of 6"
       % (list(raw.index).index("Fell") + 1))

    # ----------------------------------------------------------------- the fork table
    allp = S["tip"]
    base = M["golden_order"]

    def order_from(t):
        return list(t[t.k == 0].groupby("team").hit.mean().sort_values().index)
    # SF1 duplicates kept
    ros_ = S["roster"]
    dup = SV.tip_with_duplicates(target, ros_)
    ok("SF1", order_from(SV.year26(dup)) == base, "the repeated first-of-month rows kept: same order")
    # SF2 cancelled read as misses (and as meetings)
    tt = allp.copy()
    tt["res2"] = tt.res.replace({"cancelled": "miss"})
    tt["k2"] = tt.groupby(["person", "image"]).cumcount()
    t2 = tt[(tt.year == 2026) & tt.team.notna()].copy()
    t2["hit"] = (t2.res2 == "hit").astype(int)
    o2 = list(t2[t2.k2 == 0].groupby("team").hit.mean().sort_values().index)
    ok("SF2", o2 == base, "cancelled projections read as shown misses: same order")
    # SF3 team at the time of the projection
    mv = pd.read_excel(os.path.join(target, PK.F["roster"]), sheet_name="Moves 2026")
    t3 = SV.year26(allp)
    tat = t3.team.copy()
    for r in mv.itertuples():
        sel = (t3.staff == r[1]) & (t3.ts.dt.tz_convert("Europe/London").dt.tz_localize(None) < pd.Timestamp(r[4]))
        tat[sel] = r[2]
    t3 = t3.assign(team=tat)
    ok("SF3", order_from(t3) == base, "each projection read to the team its screener was in that day: same order")
    # SF4 the window read in UTC
    t4 = allp[(allp.ts.dt.year == 2026) & (allp.res != "cancelled") & allp.team.notna()].copy()
    t4["hit"] = (t4.res == "hit").astype(int)
    ok("SF4", order_from(t4) == base, "2026 read in UTC rather than UK time: same order")
    # the half-handled step: earlier meetings counted from 1 January 2026 only, the history files left unread
    t5 = SV.year26(allp).copy()
    t5["k"] = t5.groupby(["person", "image"]).cumcount()
    o5 = order_from(t5)
    ok("rung5.first_within_2026", o5[0] == "Brook", "earlier meetings counted inside 2026 only: %s" % o5)
    # SF5 the history read from each library's load (the exports begin there): an image a screener met in 2024 or
    # 2025 is not a first meeting in 2026; asserted as the golden's own construction
    ok("SF5", (SV.year26(allp).k == 0).sum() == int(sum(A["first"][k]["n"] for k in TEAMS)),
       "first meetings counted against the whole history since each library's load")
    # SF6 operators who left during 2026 (not on the roster) left out; with their last team kept in, same order
    ok("SF6", "Fell" == base[0] and allp.team.isna().sum() > 0, "leavers' rows carry no 31 December team")
    # SF7 Pier B log read as UTC
    pbu = allp.copy()
    shift = (pbu.area == "Pier B")
    loc = pbu.ts.dt.tz_convert("Europe/London")
    pbu.loc[shift, "ts"] = loc[shift].dt.tz_localize(None).dt.tz_localize("UTC")
    pbu["year"] = pbu.ts.dt.tz_convert("Europe/London").dt.year
    ok("SF7", order_from(SV.year26(pbu)) == base, "the Pier B clock read as UTC: same order")
    # SF8 member mean against pooled
    ok("SF8", list(R["G member mean"].sort_values().index) == base, "each member's own rate averaged: same order")
    # SF9 rounding of the order's figures: every first-meeting rate clear of a whole-per-cent edge
    e9 = min(edge(100 * v, 1.0) for v in R["G first meetings"].values)
    ok("SF9", e9 >= 0.05, "nearest first-meeting rate to a whole-per-cent edge: %.3f points" % e9)
    # SF10 supervisors included as X-ray operators: with them left out, same order
    sup = set(ros[ros.Role.str.contains("Supervisor")]["Staff no"])
    t10 = SV.year26(allp)
    t10 = t10[~t10.staff.isin(sup)]
    ok("SF10", order_from(t10) == base, "screening supervisors left out: same order")
    # SF11 starters in 2026 left out
    st = set(ros[pd.to_datetime(ros["Start date"]) >= pd.Timestamp("2026-01-01")]["Staff no"])
    t11 = SV.year26(allp)
    t11 = t11[~t11.staff.isin(st)]
    ok("SF11", order_from(t11) == base, "2026 starters left out: same order")
    # SF12 the images loaded in April 2026 left out
    t12 = SV.year26(allp)
    added = set(W["library"][W["library"].loaded == P.PB_ADD].image)
    t12 = t12[~t12.image.isin(added)]
    ok("SF12", order_from(t12) == base, "the April 2026 Pier B images left out: same order")

    # ----------------------------------------------------------------- the asks against the truth
    pbl = W["pb_logged"].copy()
    pbl = pbl[pbl.on.dt.tz_convert("Europe/London").dt.year == 2026]
    ss = W["sessions"]
    c26 = ss[(pd.to_datetime(ss.day).dt.year == 2026) & (ss.area == "C")]
    hrs = pd.Series(0.0, index=TEAMS)
    for pid, sec in ((c26.end - c26.start).dt.total_seconds()).groupby(c26.pid).sum().items():
        if pid in team_of:
            hrs[team_of[pid]] += sec
    for pid, sec in ((pbl.off - pbl.on).dt.total_seconds()).groupby(pbl.pid).sum().items():
        if pid in team_of:
            hrs[team_of[pid]] += sec
    hrs = hrs / 3600.0
    ok("askA.truth", (hrs - S["A"]["golden"]).abs().max() < 1e-6, "screen time equals the sessions as worked and "
       "logged on, to the second")
    HV = SV.hours_variants(target, S["roster"])
    worst = min(((edge(v, 0.1), k, t) for k, X in HV.items() for t, v in X.items()))
    ok("askA.edge", worst[0] >= 0.02, "nearest screen-time figure to a tenth-of-an-hour edge under every merge and "
       "clipping variant (%s): %.4f h (%s, %s)" % (", ".join(HV), worst[0], worst[2], worst[1]))
    ok("askA.variants_converge", all((X - S["A"]["golden"]).abs().max() < 1e-9 for X in HV.values()),
       "every merge and clipping variant files the golden screen time to the second")
    span_pb = (pbl.off - pbl.on).dt.total_seconds().max()
    span_ct = (c26.end - c26.start).dt.total_seconds().max()
    ok("SF13.cap20_inert", span_pb <= 20 * 60 and span_ct <= 20 * 60 and
       (HV["cap20"] - S["A"]["golden"]).abs().max() < 1e-9,
       "SPS-04 5.1 read as a 20-minute cap on a logged-on span moves no team's screen time: longest Pier B log-on %.0f s, "
       "longest Central session %.0f s" % (span_pb, span_ct))
    tot = float(S["A"]["golden"].sum())
    ok("askA.total_edge", edge(tot, 0.1) >= 0.02, "the airport total %.4f h, %.4f h from its edge" % (tot, edge(tot, 0.1)))
    moved = W.get("hours_moved", {})
    ok("askA.moves_small", all(len(v) <= 3 and sum(s for _i, s in v) <= 360 for v in moved.values()) and
       all(20 * 60 >= (W["sessions"].loc[W["sessions"].sid == i].pipe(lambda d: (d.end - d.start).dt.total_seconds()
                                                                             .iloc[0])) for v in moved.values()
           for i, _s in v), "screen-time moves: %s" % moved)
    rj = W["rejects"]
    clear = rj[(rj.outcome == "CLEAR") & rj.pid.isin(cur.index)]
    tb = clear.pid.map(team_of).value_counts().reindex(TEAMS, fill_value=0)
    ok("askB.truth", (tb == S["B"]["golden"]).all(), "clear searches equal the truth's clear searches by rejecting "
       "screener: %s" % tb.to_dict())
    a, e = W["assess"], W["external"]
    certday = {}
    for r in a[(a.result == "PASS") & a.code.isin(["IIC", "EXT-IIC"])].itertuples():
        d = r.date
        if r.code == "EXT-IIC":
            d = e[e.cert_no == r.cert_no].assessed.iloc[0]
        certday[r.pid] = max(certday.get(r.pid, d), d)
    tc = pd.Series(0, index=TEAMS)
    for pid, d in certday.items():
        if pid in team_of and pd.Timestamp(d.replace(year=d.year + 3)) < pd.Timestamp(P.CERT_CUTOFF):
            tc[team_of[pid]] += 1
    ok("askC.truth", (tc == S["C"]["golden"]).all(), "certificates equal the truth: %s" % tc.to_dict())
    near = [d for d in certday.values() if abs((pd.Timestamp(d) - pd.Timestamp("2024-07-01")).days) <= 3]
    ok("askC.no_boundary_day", not near, "no certifying assessment within three days of 1 July 2024")
    lmsx = pd.read_excel(os.path.join(target, PK.F["lms"]), sheet_name="Assessments")
    cenx = pd.read_csv(os.path.join(target, PK.F["certs"]), dtype=str, keep_default_na=False)
    unheld = cenx[~cenx.certificate_no.isin(set(lmsx["Certificate ref"].dropna()))]
    late = e[e.cert_no.isin(unheld.certificate_no)]
    late_teams = sorted(team_of[pid] for pid in late.pid)
    missed = sorted(t for t in TEAMS if S["C"]["joined"][t] != S["C"]["golden"][t])
    ok("askC.late_renewals", len(unheld) == P.EARLY_RENEWALS and (pd.to_datetime(late.keyed) > pd.Timestamp(P.LMS_EXPORT)).all()
       and len(set(late_teams)) == P.EARLY_RENEWALS and missed == late_teams and
       (S["C"]["golden"] <= S["C"]["joined"]).all(),
       "%d centre certificates awarded in December 2026 and keyed after the LMS export (%s); dated through the LMS "
       "references alone the count misses exactly those teams" % (len(unheld), ", ".join(late_teams)))
    ok("askC.lms_export_dates", lmsx["Completed"].max() <= pd.Timestamp(P.LMS_EXPORT),
       "no LMS entry after the export of %s" % P.LMS_EXPORT)
    for k in ("cracker", "mirror"):
        for name, X in (("A", S["A"]), ("B", S["B"])):
            diff = (X[k] - X["golden"]).abs()
            tol = 0.05 if name == "A" else 0.5
            assert (diff > tol).all(), (name, k, diff.to_dict())
    assert (S["C"]["lms"] != S["C"]["golden"]).all()
    ok("asks.cracker_and_mirror_miss_every_figure", True, "A, B and C: every team's figure off the golden on both routes")

    # ----------------------------------------------------------------- the main population carries no ask device
    ok("separation.tip_rows", True, "the call reads only the TIP exports and the roster; the ask devices sit in the "
       "session, event, search, reject, badge and training files")

    # ----------------------------------------------------------------- documents: what they file, and what they never say
    sps = docx_text(os.path.join(target, PK.F["sps"]))
    ok("doc.sps_control", "least likely to find a prohibited article" in sps and "rostered to on 31 December" in sps,
       "SPS-04 files the order's WHAT and the team definition")
    banned = re.compile(r"(?i)repeat|familiar|first time|memor|librar|recogn|seen before|met before")
    ok("doc.sps_silent", not banned.search(sps), "SPS-04 names no earlier meeting with an image")
    import docx as _docx
    for path, must in ((os.path.join(target, PK.F["sps"]), "least likely to find a prohibited article"),
                       (os.path.join(golden, "remedial_course_2027_note.docx"), "met for the first time in 2026")):
        d = _docx.Document(path)
        txt = " ".join(p.text for p in d.paragraphs) + " " + " ".join(
            c.text for tb in d.tables for row in tb.rows for c in row.cells)
        assert must in txt and "**" not in txt, path
    sd = _docx.Document(os.path.join(target, PK.F["sps"]))
    revrows = [[c.text for c in row.cells] for row in sd.tables[-1].rows][1:]
    pdate = lambda x: pd.Timestamp(dt.datetime.strptime(x, "%d %B %Y"))
    cp = sd.core_properties
    ok("doc.sps_issue_dates", len(revrows) == 3 and all(pdate(r[1]) < pdate(r[2]) for r in revrows)
       and revrows[-1][2] in sps.split("Owner")[0] and "Issue %s, effective %s" % (revrows[-1][0], revrows[-1][2]) in sps
       and "%s." % revrows[-1][1] in sps.split("Owner")[1][:200]
       and pdate(revrows[-1][1]).date() == cp.modified.date() and pdate(revrows[0][1]).date() == cp.created.date(),
       "SPS-04 revision history: each issue issued before it took effect, Issue 3 issued on its approval day and the "
       "file's last save, Issue 1 on the file's creation: %s" % revrows)
    ok("doc.docx_two_readers", True, "python-docx reads SPS-04 and the golden note with their key sentences, no "
       "stray markup")
    eml = open(os.path.join(target, PK.F["eml"]), encoding="utf-8").read()
    ok("doc.eml_control", "six blocks and one team in each" in eml and not banned.search(eml), "the planning email")
    rev = pdf_text(os.path.join(target, PK.F["review"]))
    import pdfplumber
    with pdfplumber.open(os.path.join(target, PK.F["review"])) as pdf:
        rev2 = " ".join((pg.extract_text() or "") for pg in pdf.pages)
    norm = lambda x: re.sub(r"\s+", " ", x).strip()
    from collections import Counter as _C
    ok("doc.review_two_readers", "Fourteen test articles detected" in norm(rev2) and
       _C(rev.split()) == _C(rev2.split()), "pypdf and pdfplumber read the same words")
    ok("doc.review_control", "Fourteen test articles detected" in rev and not banned.search(rev),
       "the compliance review read back from its streams")
    from pypdf import PdfReader as _PR
    rp = os.path.join(target, PK.F["review"])
    rr = _PR(rp, strict=True)
    md = rr.metadata
    faces = {str(v.get_object()["/BaseFont"]) for pg in rr.pages for _k, v in pg["/Resources"]["/Font"].items()}
    ok("doc.review_word_export", rr.pdf_header == "%PDF-1.7" and os.path.getsize(rp) > 20000
       and md["/Producer"] == md["/Creator"] == "Microsoft\u00ae Word for Microsoft 365"
       and md["/CreationDate"][2:16] < md["/ModDate"][2:16] < "20261214000000"
       and all("+" in f for f in faces) and "/Metadata" in rr.trailer["/Root"],
       "the compliance review reads as a Word export: PDF 1.7, %d bytes, created %s, saved %s before the 14 December "
       "meeting, fonts %s" % (os.path.getsize(rp), md["/CreationDate"], md["/ModDate"], sorted(faces)))

    # ----------------------------------------------------------------- the write-up's own figures and prose claims
    import writeup as WU
    f, al, a0 = A["first"], A["all"], A["order"][0]
    stated = ([100 * f[k]["rate"] for k in TEAMS] + [100 * al[A["order"][0]]["rate"], 100 * al[A["order"][1]]["rate"],
                                                    100 * A["met_rate"][a0]])
    ep = min(edge(v, 1.0) for v in stated)
    ok("figures.pct_edges", ep >= 0.05, "nearest stated percentage to a whole-per-cent edge: %.3f points" % ep)
    # every graded figure against its printed unit, in one place: the hours to a tenth of an hour (0.02 h floor, the
    # figure the write-up prints is the rounding of the exact value), the percentages to a whole per cent, and the
    # counts exact integers that no rounding touches
    he = {k: edge(A["hours_exact"][k], 0.1) for k in TEAMS}
    graded_ok = (all(v >= 0.02 for v in he.values())
                 and all(abs(A["hours"][k] - round(A["hours_exact"][k] + 1e-9, 1)) < 1e-9 for k in TEAMS)
                 and ep >= 0.05
                 and all(float(S[x]["golden"][k]).is_integer() for x in ("B", "C") for k in TEAMS))
    ok("figures.graded_edges", graded_ok, "every graded figure off its edge: hours %s; percentages >= %.3f points; "
       "clear searches and certificates whole counts" % ({k: round(v, 4) for k, v in he.items()}, ep))
    lift = {k: al[k]["rate"] - f[k]["rate"] for k in TEAMS}
    ok("prose.flatters", all(v > 0 for v in lift.values()) and
       lift[a0] > 3 * max(v for k, v in lift.items() if k != a0),
       "the overall score lifts %s by %.1f points, no other team by more than %.1f" % (
           a0, 100 * lift[a0], 100 * max(v for k, v in lift.items() if k != a0)))
    ok("prose.met_higher", all(A["met_rate"][k] > f[k]["rate"] for k in TEAMS), "every team finds more on images "
       "already met")
    per = {k: 1.0 / A["repeat_share"][k] for k in TEAMS if k != a0}
    ok("prose.one_in", WU.one_in(A) == "eight" and all(7.0 <= v <= 10.0 for v in per.values()) and
       A["repeat_share"][a0] > 0.5, "one in %s for the Central teams pooled, one in %s by team; %s %.0f per cent" % (
           WU.one_in(A), ", ".join("%.1f" % per[k] for k in sorted(per)), a0, 100 * A["repeat_share"][a0]))
    ok("prose.dprime_most_clear", S["B"]["golden"].idxmax() == A["dprime_first"], "%s sends the most trays that come "
       "back clear and is first on d-prime" % A["dprime_first"])

    # ----------------------------------------------------------------- realism sweep
    for key, col in (("ct26", "event_id"), ("ctpos", "session_ref")):
        d = pd.read_csv(os.path.join(target, PK.F[key]), usecols=[col], dtype=str)
        n = d[col].str[-7:].astype(int).drop_duplicates().sort_values().diff().dropna()
        assert n.nunique() > 3, key
    ok("realism.ids_not_arithmetic", True, "event ids and session refs step unevenly")
    sizes = ros.groupby("Team").size()
    ok("realism.team_sizes_vary", sizes.nunique() >= 4, sizes.to_dict())
    ok("realism.no_round_hours", all(abs(v - round(v, -1)) > 0.5 for v in S["A"]["golden"].values), "hours")
    srch = pd.read_csv(os.path.join(target, PK.F["search"]), dtype=str, usecols=["search_id"])
    ok("realism.search_ids_unique", srch.search_id.is_unique, "%d records" % len(srch))
    limits = {2 ** k + d for k in range(10, 21) for d in (-1, 0)}
    counts = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) for f in files if f.endswith(".csv")}
    bad = [f for f, n in counts.items() if (n - 1) in limits or n in limits or (n - 1) % 1000 == 0]
    ok("realism.no_limit_row_counts", not bad, "no CSV holds a row count at a 16-bit or 20-bit limit or a round "
       "thousand: %s" % sorted(counts.values()))
    ok("realism.personas", True, "the pack names only Marian Taylor and Bernard Vincent (drawn with guard.py names)")

    # ----------------------------------------------------------------- distractors deleted
    tmp = tempfile.mkdtemp()
    t2 = os.path.join(tmp, "t")
    shutil.copytree(target, t2)
    for k in PK.DISTRACTORS:
        os.remove(os.path.join(t2, PK.F[k]))
    S2 = SV.solve(t2)
    shutil.rmtree(tmp)
    ok("distractors.deleted", S2["main"]["golden_order"] == A["order"] and
       (S2["A"]["golden"] - S["A"]["golden"]).abs().max() < 1e-9 and (S2["B"]["golden"] == S["B"]["golden"]).all()
       and (S2["C"]["golden"] == S["C"]["golden"]).all(), "throughput, queue samples and the compliance review deleted")
    return len(LOG)
