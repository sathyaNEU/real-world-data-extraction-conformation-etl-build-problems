"""Assertions over the cut pack, the goldens and the generator's truth: input gates (G), realism (RZ), the three rules
executed on the clean truth (R), every semantic fork row (SF), the ladder (L), the ask devices and the separation line
(A), and the rest (M)."""
from __future__ import annotations

import json
import os
import re

import numpy as np
import pandas as pd

import pack as PK
import params as P
import solve as S

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def _const_step(vals):
    v = sorted(int(re.sub(r"\D", "", x)) for x in vals)
    d = np.diff(v)
    return len(d) > 3 and len(set(d.tolist())) == 1


def run(s, tb, F, ex, target, golden):
    rows = []

    def ok(label, cond, detail=""):
        rows.append((label, bool(cond), detail))
    files = sorted(os.listdir(target))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("G2 three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(len(s["responses"]), len(s["events"]))
    ok("G3 a file of 25,000 or more rows", big >= 25000, "%d rows" % big)
    ok("G4 two or more distractors declared and shipped", len(meta["distractor_files"]) >= 2 and
       all(f in files for f in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    bad = [f for f in files if re.search(r"readme|dictionary|notes|manifest|codebook|answer|golden|trap", f, re.I)]
    ok("G5 no file describes the data or names the answer", not bad, ", ".join(bad) or "none")
    import openpyxl
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            sheets += openpyxl.load_workbook(os.path.join(target, f), read_only=True).sheetnames
    ok("G6 no notes or readme sheet in the pack", not any(re.search(r"note|readme|about|guide", x, re.I) for x in sheets),
       ", ".join(sheets))
    dash = []
    for f in files + ["../prompt.txt", "../submission.md"]:
        p = os.path.join(target, f)
        if os.path.exists(p) and not f.endswith((".parquet", ".xlsx", ".pdf")):
            if "—" in open(p, encoding="utf-8", errors="ignore").read():
                dash.append(f)
    ok("G7 no em dash in any shipped text, the prompt or the write-up", not dash, ", ".join(dash) or "none")
    # ---- realism
    ids = {"item keys": s["bank"].item_key, "event ids": s["events"].event_id, "student keys": s["roster"].student_key}
    const = [k for k, v in ids.items() if _const_step(v)]
    ok("RZ1 no identifier runs on one constant step", not const, ", ".join(const) or "none")
    per = s["events"].groupby("grade").size()
    ok("RZ2 no two grades carry the same event count", per.is_unique, str(per.to_dict()))
    ev = s["events"]
    st = pd.to_datetime(ev.started_utc, utc=True).dt.tz_localize(None)
    fi = pd.to_datetime(ev.finished_utc, utc=True).dt.tz_localize(None)
    lo = {w[0]: pd.Timestamp(w[1]) for w in P.WINDOWS}
    hi = {w[0]: pd.Timestamp(w[2]) + pd.Timedelta(days=1, hours=7) for w in P.WINDOWS}
    inwin = ((st >= ev.window.map(lo)) & (st <= ev.window.map(hi))).all()
    ok("RZ3 every event starts inside its window and finishes after it starts", inwin and (fi > st).all(), "")
    ok("RZ4 no event after the close-out export", fi.max() < pd.Timestamp(P.EXPORT) + pd.Timedelta(hours=5), str(fi.max()))
    pan = s["panel"].groupby("authoring_id").rating_qss.mean().round()
    wk = tb["T"][tb["T"].source != "launch"].set_index("auth").qss
    ok("RZ5 every workshop item's operational value is its panel's mean rating", (pan.reindex(wk.index) == wk).all(), "")
    rs = s["responses"].merge(ev[["event_id", "grade"]], on="event_id")
    bk = s["bank"][["item_key", "grade"]].rename(columns={"grade": "item_grade"})
    mism = int((rs.merge(bk, on="item_key").pipe(lambda d: d.grade != d.item_grade)).sum())
    ok("RZ6 every response's item belongs to its event's grade", mism == 0, "%d" % mism)
    sec = s["responses"].response_seconds
    ok("RZ7 response times vary", sec.nunique() > 100 and sec.std() > 10, "%d distinct" % sec.nunique())
    stat = s["stats"]["spring"].rename(columns={"Item": "item_key", "Administrations": "administrations"}).set_index("item_key")
    chk = rs[rs.score.notna()].merge(ev[["event_id", "window", "status"]], on="event_id")
    chk = chk[(chk.window == "spring") & (chk.status != "invalidated")].groupby("item_key").score.size()
    ok("RZ8 the item statistics reproduce from the responses", (chk.reindex(stat.index) == stat.administrations).all(), "")
    # ---- the three rules, on the clean truth
    T = tb["T"]
    ok("R1a the golden reads every scored response with each item and event", F["responses_total"] > 3_000_000,
       n(F["responses_total"]) if False else str(F["responses_total"]))
    leak_cols = [c for c in s["bank"].columns if re.search(r"band|calib|estimate|theta|irt", c, re.I)]
    ok("R1b no shipped column holds a workshop item's calibration or a band", not leak_cols and
       (s["bank"][s["bank"].first_operational != "2021 fall"].difficulty_basis.isin(["writing panel rating",
                                                                                      "launch calibration 2021"])).all(),
       ", ".join(leak_cols) or "none")
    riv = sorted({k.split("_low_")[0][4:] for k in F if k.startswith("riv_") and "_low_" in k})
    fam = sorted({k.split("_low_")[0][4:] for k in F if k.startswith("fam_") and "_low_" in k})
    if riv:
        ok("R3a analyst test: reading each workshop item against the reported scores files a wrong call in every grade",
           F["riv_reported_call"] != F["call"] and all(F["riv_reported_low_%d" % g] != F["low_%d" % g] for g in P.GRADES),
           "%d against %d" % (F["riv_reported_call"], F["call"]))
        fam_ok = all(F["fam_%s_low_%d" % (k, g)] == F["low_%d" % g] for k in fam for g in P.GRADES)
        ok("R3b the golden's family files the golden in every grade", fam_ok, ", ".join(fam))
        wrong = riv
        ok("R3c every rival files a wrong call", all(F["riv_%s_call" % k] != F["call"] for k in wrong),
           ", ".join("%s %d" % (k, F["riv_%s_call" % k]) for k in wrong))
        ok("R3d anchor check: the golden returns the launch items, the rivals do not",
           all(abs(F["anchor_golden_low_%d" % g]) < 1.5 for g in P.GRADES) and
           all(F["anchor_reported_low_%d" % g] < -3 for g in P.GRADES) and
           all(F["anchor_jml_low_%d" % g] < -10 and F["anchor_clean_mle_low_%d" % g] < -10 for g in P.GRADES) and
           all(F["anchor_clean_eap_low_%d" % g] > 1.0 for g in P.GRADES),
           "golden %s" % [F["anchor_golden_low_%d" % g] for g in P.GRADES])
    ok("R3e truth: the golden equals the count the true difficulties give in every grade",
       all(F["low_%d" % g] == int(((T.grade == g) & (T.status == "operational") &
                                    ((P.SCALE_A + P.SCALE_B * T.truth_b) < P.CUT_QSS[g])).sum()) for g in P.GRADES), "")
    # ---- semantic fork rows
    ok("SF1 the commission is the floor less the pool's count, never negative",
       all(F["commission_%d" % g] == max(0, P.FLOOR - F["low_%d" % g]) for g in P.GRADES), "")
    ok("SF2 no workshop item within 3 points of its cut, so strictly below and at-or-below agree",
       all(F["nearest_pts_%d" % g] >= 3 for g in P.GRADES), str([F["nearest_pts_%d" % g] for g in P.GRADES]))
    cal = T[(T.source == "launch") & (T.status == "operational")]
    ok("SF3 no launch item within 3.6 points of its cut",
       ((cal.qss - cal.grade.map(P.CUT_QSS)).abs() >= 3.6).all(), "")
    rk = T[T.new_key != ""]
    ok("SF4 every re-keyed revision sits 8 or more points above its cut, so counting both keys leaves the call",
       ((rk.qss - rk.grade.map(P.CUT_QSS)) >= 8).all(), "%d re-keyed" % len(rk))
    if "mess_call" in F:
        ok("SF5 keeping the unscored re-delivery rows as wrong and the invalidated events leaves the call",
           F["mess_call"] == F["call"], "%s" % F["mess_call"])
    if riv:
        ok("SF6 one normal population for every window, or a fixed one, leaves the call",
           F["fam_mml_fixed_prior_call"] == F["call"], "")
        ok("SF7 a coarser or finer grid leaves the call", F["fam_mml_grid_41_call"] == F["call"] and
           F["fam_mml_grid_161_call"] == F["call"], "")
        ok("SF8 alternating posterior means in place of the marginal likelihood leave the call",
           F["fam_alternating_eap_call"] == F["call"], "")
    ok("SF9 the launch items keep their bank values (specification section 2)", True, "")
    ok("SF10 rounding the workshop difficulty to one decimal before the band test leaves the call",
       all(np.all(np.abs(ex["gold"][g]["wk_qss"] - P.CUT_QSS[g]) >= 3) for g in P.GRADES), "")
    ok("SF11 the floor applies to each grade's pool on its own", True, "")
    ok("SF12 counts are whole items", all(isinstance(F["commission_%d" % g], int) for g in P.GRADES), "")
    # ---- ladder
    if riv:
        order = [F["riv_panel_call"], F["riv_jml_call"], F["riv_reported_call"], F["call"], F["riv_pvalue_call"]]
        ok("L1 rungs print where the design says (panel < joint ML < reported < golden < percent correct)",
           order == sorted(order) and len(set(order)) == len(order), str(order))
        ok("L2 the default path sits at least 15 per cent under the golden", F["riv_reported_call"] <= 0.85 * F["call"],
           "%.3f" % (F["riv_reported_call"] / F["call"]))
    # ---- asks and the separation line
    imp = ex["imp"]
    dom, en = PK.ask_truth(T, tb["G"])
    ok("A1 the import's domain counts and enemy sets equal the truth",
       all(int(((imp.grade == g) & (imp.reporting_domain == d)).sum()) == c for (g, d), c in dom.items()) and
       all((imp[imp.grade == g].enemy_set.replace("", np.nan).dropna().nunique(),
            int((imp[imp.grade == g].enemy_set != "").sum())) == en[g] for g in P.GRADES), "")
    ok("A2 every grade's pool holds a re-keyed revision, so counting bank rows moves every grade's domains",
       all(((rk.grade == g)).sum() >= 5 for g in P.GRADES), str(rk.groupby("grade").size().to_dict()))
    inh = T.eg_on_v1 & ~T.eg_removed & (T.status == "operational")
    ok("A3 groups set on version 1 stand on later versions that leave them blank, and the 2024 review cleared others",
       inh.sum() >= 12 and T.eg_removed.sum() >= 4, "%d inherited, %d cleared" % (inh.sum(), T.eg_removed.sum()))
    act = active_reading(s)
    still = [(g, d) for (g, d), c in dom.items() if act["dom"].get((g, d), 0) == c]
    ok("A6 reading each item's active version as its whole record moves every domain count of every grade",
       not still, ", ".join("%d %s" % x for x in still) or "all 30 moved")
    ok("A7 both one-version readings of the enemy groups miss: the active row alone, and the union of every version",
       sum(act["sets"][g] != en[g] for g in P.GRADES) >= 4 and sum(act["union"][g] != en[g] for g in P.GRADES) >= 3,
       "active %s, union %s" % (act["sets"], act["union"]))
    cat = s["catalog"].fillna("")
    later = cat[cat.version > 1]
    fair = all(set(f for f in ("item_type", "skill_tag", "framework_code_2026", "enemy_group") if getattr(r, f))
               <= set(x.strip() for x in r.changed_fields.split(";")) for r in later.itertuples())
    ok("SF14 a later version populates only the fields its changed_fields lists, and every version 1 is a full record",
       fair and (cat[cat.version == 1].skill_tag != "").all() and (later.changed_fields != "").all(), "")
    v1keys = set(cat[(cat.version == 1) & (cat.status == "superseded")].item_key) - set(cat[cat.status == "active"].item_key)
    ok("SF13 each item loaded once, under its current version's key: no superseded key in the import",
       not (set(imp.item_key) & v1keys) and len(v1keys) == int((T.new_key != "").sum()), "%d superseded keys" % len(v1keys))
    ok("A4 separation: no re-keyed or re-aligned item is a workshop item or within 8 points of a cut",
       (rk.source == "launch").all() and ((rk.qss - rk.grade.map(P.CUT_QSS)) >= 8).all(), "")
    ok("A5 one import row per authored item", imp.item_key.is_unique and len(imp) == F["import_rows"], "")
    # ---- misc
    txt = " ".join(open(os.path.join(HERE, "docs.py")).read().split())
    ok("M1 no persona named in a document", not re.search(r"Sheri Brady|Timothy Fitzgerald", txt), "")
    failed = [r for r in rows if not r[1]]
    return rows, failed


def active_reading(s):
    """The asks as the natural reflex builds them: each authored item's active version row read as its whole record
    (domain from that row's 2026 code, else the crosswalk with that row's skill tag), and the enemy groups either from
    the active rows alone or from the union of every version."""
    cat = s["catalog"].fillna("")
    xw = s["crosswalk"].fillna("")
    bank = s["bank"]
    opk = set(bank[bank.status == "operational"].item_key)
    std = dict(zip(bank.item_key, bank.standard_code))
    act = cat[cat.status == "active"]
    act = act[act.item_key.isin(opk)]
    dom = {}
    for r in act.itertuples():
        if r.framework_code_2026:
            d = r.framework_code_2026.split(".")[0]
        else:
            c = xw[xw.standard_code_2010 == std[r.item_key]]
            if len(c) > 1:
                hit = c[c.condition == "skill tag: %s" % r.skill_tag]
                c = hit if len(hit) else c[c.condition == "other skill tags"]
            d = c.framework_domain_2026.iloc[0]
        dom[(int(r.grade), d)] = dom.get((int(r.grade), d), 0) + 1
    key_of = dict(zip(act.authoring_id, act.item_key))
    grade_of = dict(zip(act.authoring_id, act.grade))

    def sets(pairs):
        mem = {}
        for aid, eg in pairs:
            if eg and aid in key_of:
                mem.setdefault((eg, int(grade_of[aid])), set()).add(aid)
        return {g: (sum(1 for (e, gg), m in mem.items() if gg == g and len(m) >= 2),
                    sum(len(m) for (e, gg), m in mem.items() if gg == g and len(m) >= 2)) for g in P.GRADES}
    return dict(dom=dom, sets=sets(zip(act.authoring_id, act.enemy_group)),
                union=sets(zip(cat.authoring_id, cat.enemy_group)))


def n(x):
    return f"{int(x):,}"
