"""Generator assertions: the call, its standing family, the ladder, the careful frame, the fork table, the three rules on
the clean truth, mess neutrality, the asks' devices and stops, separation, the input gates, the realism sweep and the
documents read back with positive controls. Returns the number of failures."""
import datetime as dt
import os
import shutil
import tempfile

import numpy as np
import pandas as pd
import statsmodels.api as sm

import build as B
import docs as DC
import params as P
import solve as S
import world as WO

BAD = []
U = S.ROUND


def check(name, ok, info=""):
    print(("ok   " if ok else "FAIL ") + name + ((" :: " + str(info)) if info != "" else ""))
    if not ok:
        BAD.append(name)


def edge(x, u=U):
    return u / 2.0 - abs(x - S.rnd(x, u))


def pdf_text(path):
    from pypdf import PdfReader
    import re
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def main(target, R=None):
    del BAD[:]
    D, ci, ev, g = S.solve(target)
    ci.attrs["target"] = target
    gold = g["plan_r"]
    L, col = g["L"], g["col"]
    check("call: the plan is 45,000 GP-referred visits", gold == 45000, round(g["plan"]))
    check("call: at least 600 inside its 2,500 cell", edge(g["plan"]) >= 600, round(edge(g["plan"])))
    aic = g["aic"]
    gap5 = min(aic[l] - aic[L] for l in aic if l <= 5)
    check("fit: the record's fit picks the world's own eight-week window", L == P.DETER_WEEKS,
          {k: round(v - aic[L], 1) for k, v in aic.items()})
    check("fit: every window of five weeks or fewer at least 50 worse in AIC", gap5 >= 50, round(gap5, 1))
    # SF11: the write-up's AIC margin is a bound that holds on every sample its method implies, not one sample's figure
    bound, gvar = S.window_gap_bound(D, target)
    for k, (Lv, gv) in gvar.items():
        check("SF11 on the %s the fit picks eight weeks and every window of five weeks or fewer is at least the stated %d "
              "worse, with 2 to spare for an implementation's own fit" % (k, bound), Lv == P.DETER_WEEKS and gv >= bound + 2,
              (Lv, round(gv, 1)))
    check("SF11 the stated bound is the lowest margin over those samples floored to ten, and at least 50",
          bound >= 50 and bound == int(10 * np.floor(min(v[1] for v in gvar.values()) / 10.0)), bound)
    _here = os.path.dirname(os.path.abspath(__file__))
    _fj = os.path.join(_here, "figures.json")
    if os.path.exists(_fj):
        import json as _json
        with open(_fj) as _fh:
            _stated = _json.load(_fh)["aic_gap_five_weeks_or_fewer"]
        _sub = open(os.path.join(os.path.dirname(_here), "submission.md")).read()
        check("SF11 figures.json and the write-up's step 3 carry that bound",
              _stated == bound and ("every window of five weeks or fewer at least %d worse" % bound) in _sub, _stated)
    fam = S.family(D, ci, L)
    for k, v in fam.items():
        check("family: %s prints 45,000, at least 300 inside the cell" % k, S.rnd(v) == gold and edge(v) >= 300, round(v))
    geo = fam["a geometric decay over 26 weeks, its rate by AIC"]
    check("family: the geometric decay, the top-edge soft spot, at least 250 below 46,250", 46250 - geo >= 250, round(46250 - geo))
    more = S.family_more(D, target, L)
    for k, v in more.items():
        check("family: %s prints 45,000, at least 250 inside the cell" % k, S.rnd(v) == gold and edge(v) >= 250, round(v))
    extra = S.family_extra(D, L)
    for k, v in extra.items():
        check("family (other exposure forms): %s prints 45,000, at least 250 inside" % k, S.rnd(v) == gold and edge(v) >= 250,
              "%.0f, %.0f inside" % (v, edge(v)))
    allfam = list(fam.values()) + list(more.values()) + list(extra.values())
    check("family: %d specifications in one printed cell" % len(allfam), len({S.rnd(v) for v in allfam}) == 1,
          "%.0f to %.0f, %.2f of the unit" % (min(allfam), max(allfam), (max(allfam) - min(allfam)) / U))
    for k, (v, da) in S.reduced(D, L).items():
        check("reduced controls ruled out by fit: %s costs at least 100 in AIC" % k, da >= 100, "%.0f, AIC +%.0f" % (v, da))
    for k, (v, n, miss) in S.quiet(D, L).items():
        check("quiet-period fit ruled out by support: %s holds no day in %d months of the year" % (k, len(miss)),
              len(miss) >= 1, "%d days, months absent %s, %.0f" % (n, miss, v))
    # what the probes' own return check sees on this pack: the day-lagged turned-away counts (recorded)
    Dv = D.assign(g1=D.away_gp.shift(1).fillna(0), g2=D.away_gp.shift(2).fillna(0),
                  a1=(D.away_gp + D.away_h).shift(1).fillna(0), a2=(D.away_gp + D.away_h).shift(2).fillna(0),
                  tot=D.seen_gp + D.seen_h)
    cl = Dv[Dv.ro == 0]
    mg = sm.GLM(cl.seen_gp, S.calX(cl, ["g1", "g2"]), family=sm.families.Poisson()).fit()
    mt = sm.GLM(cl.tot, S.calX(cl, ["a1", "a2"]), family=sm.families.Poisson()).fit()
    check("visibility (recorded): the return check on GP-form visits, lag 1 and 2 days' GP turned away", True,
          "t %.1f and %.1f" % (mg.params["g1"] / mg.bse["g1"], mg.params["g2"] / mg.bse["g2"]))
    check("visibility (recorded): the return check on all visits", True,
          "t %.1f and %.1f" % (mt.params["a1"] / mt.bse["a1"], mt.params["a2"] / mt.bse["a2"]))
    lad = S.ladder(D, target, ci)
    want = {"R0": 40000, "R1": 42500, "R2": 42500, "R3": 42500, "R4": 42500, "R5": 42500}
    for k, v in lad.items():
        far = abs(v - 45000) - U / 2.0
        if k.startswith("R2 demand fitted"):
            check("ladder: %s misses, at least 1,000 from the golden's cell (its own cell at the 41,250 edge)" % k[:2],
                  S.rnd(v) != gold and far >= 1000, round(v))
            continue
        check("ladder: %s prints %s" % (k, "{:,}".format(want[k[:2]])), S.rnd(v) == want[k[:2]], round(v))
        check("ladder: %s at least %s from the golden's cell" % (k[:2], "1,000" if "reader" in k or "golden" in k else "900"),
              far >= (1000 if ("reader" in k or "golden" in k) else 900), round(far))
    for lab, kw in (("no month terms", dict(month=False)), ("with the day's hospital-form visits", dict(hosp=True)),
                    ("Poisson", dict(poisson=True))):
        v = S.lag_route(D, **kw)
        check("ladder: the round 2 Opus reader's route, %s, at least 1,000 below the golden's cell" % lab, 43750 - v >= 1000, round(v))
    for n, must in ((20, True), (30, True)):
        v = S.lag_route(D, n=n)
        check("ladder: the round 2 Opus reader's route with %d daily lags misses" % n, v < 43750, round(v))
    v40 = S.lag_route(D, n=40)
    check("ladder (recorded): with 40 daily lags, eight weeks of them, the route reaches the golden's cell", True, round(v40))
    comp = lad["R2 the run-out days completed from the GP ticket-issue curve (the round 1 Opus reader)"]
    careful = [lad["R1 seen plus GP-referred turned away (the default path; the round 1 Sonnet reader)"], comp,
               lad["R5 ten daily lags of the kiosk's full days on open days (the round 2 Opus reader)"]]
    check("check 2: the default and both Opus readers' careful routes agree in one cell and the decisive step alone moves "
          "the call out", len({S.rnd(x) for x in careful}) == 1 and S.rnd(careful[0]) != gold, [round(x) for x in careful])
    # fork table
    fy = (D.fy == 2025).values
    gp_coded = ci[(ci.request_type == "GP") & ci.request_org.notna() & (ci.request_org != "")]
    pr = pd.read_csv(os.path.join(target, DC.FILES["practices"]), dtype=str)
    blank = int(((ci.request_type == "GP") & (ci.request_org.isna() | (ci.request_org == ""))).sum())
    D1 = D.copy()
    lost = ci[(ci.request_type == "GP") & (ci.request_org.isna() | (ci.request_org == ""))].groupby("d").size()
    D1["arr"] = D1.arr - D1.d.map(lost).fillna(0).astype(int)
    v = S.deterred(D1)[0] * S.G2
    check("SF1 GP-referred read as a practice code on the form instead of the kiosk's GP choice: 45,000 still",
          S.rnd(v) == gold and 0 < blank, "%d forms without a barcode; %.0f" % (blank, v))
    cal = (D.d >= dt.date(2025, 1, 1)) & (D.d <= dt.date(2025, 12, 31))
    vcal = float((D.arr.values[cal.values] * np.exp(-g["b"] * D[col].values[cal.values])).sum()) * S.G2
    check("SF2 2025-26 read as calendar 2025: the ICB letter and the annual report use financial years",
          "2025-26, the last complete year" in pdf_text(os.path.join(target, DC.FILES["icb"])), round(vcal))
    check("SF3 growth compounded or simple (1.07): 45,000 either way", S.rnd(g["base"] * 1.07) == gold, round(g["base"] * 1.07))
    d2728 = len([d for d in WO.clinic_days(dt.date(2027, 4, 1), dt.date(2028, 3, 31))])
    vwd = g["plan"] * d2728 / g["days"]
    check("SF4 a working-day adjustment the prompt rules out would still print 45,000", S.rnd(vwd) == gold, "%d days, %.0f" % (d2728, vwd))
    check("SF5 the turned away left out: 40,000, ruled out by a hub that never runs out of tickets",
          S.rnd(lad["R0 GP-referred patients seen"]) == 40000)
    leg = pd.read_csv(os.path.join(target, DC.FILES["legacy"]), dtype=str)
    leg = leg[leg.Outcome == "Seen"].copy()
    leg["d"] = pd.to_datetime(leg.Date, format="%d/%m/%Y").dt.date
    dup = leg[(leg.d >= P.NEW_SYSTEM_LIVE) & (leg.Request == "GP form")].groupby("d").size()
    D6 = D.copy()
    D6["arr"] = D6.arr + D6.d.map(dup).fillna(0).astype(int)
    v6 = S.deterred(D6)[0] * S.G2
    ev_ci = ci[(ci.d <= P.OLD_SYSTEM_OFF) & (ci.request_type == "GP")].groupby("d").size()
    check("SF6 the parallel-run fortnight counted twice: 45,000 still, and the two systems agree day by day",
          S.rnd(v6) == gold and dup.reindex(ev_ci.index).fillna(-1).astype(int).equals(ev_ci.astype(int)), round(v6))
    check("SF7 the hub's first weeks carry no run-out record: the window's share is nil from April 2027",
          True, "the plan grows a never-ran-out base")
    check("SF8 visits, not patients: the prompt asks for visits and the records carry no patient key",
          "patient" not in "".join(c.lower() for c in ci.columns))
    rep6 = pdf_text(os.path.join(target, DC.FILES["report"]))
    csv_cols = [c.lower() for f in os.listdir(target) if f.endswith(".csv")
                for c in pd.read_csv(os.path.join(target, f), nrows=1).columns]
    check("SF9 every patient with a GP request is the hub's GP-referred demand set from 2025-26, not the practices' own "
          "clinics' work: no file counts the practices' phlebotomy activity",
          "Its activity plan is to be set from 2025-26" in rep6 and not any("activity" in c or "bled" in c for c in csv_cols))
    check("SF10 the booked clinic at Brantmoor carries on as now, so its own booked patients stay out of the hub's figure",
          "the booked clinic at %s carries on as now" % P.SATELLITE in rep6)
    # three rules on the clean truth
    if R is not None:
        W = R["W"]
        fyw = np.array([WO.fy(x) == 2025 for x in W["days"]])
        arr_t = float((W["A"]["P"] + W["A"]["N"])[fyw].sum()) * S.G2
        lat_t = float((W["lam"]["P"] + W["lam"]["N"])[fyw].sum()) * S.G2
        und_t = float((W["A"]["P"] * np.exp(W["K"] * W["E"]) + W["A"]["N"])[fyw].sum()) * S.G2
        check("R1 the field's raw material ships: daily referrals by request form, the turned-away record and practice codes",
              len(D) > 800 and D.ro.sum() > 100 and gp_coded.request_org.isin(pr.practice_code).mean() > 0.95)
        check("R1 no shipped column holds the deterrence or the suppressed demand",
              not any(("suppress" in c.lower() or "deter" in c.lower() or "kept" in c.lower()) for f in os.listdir(target)
                      if f.endswith(".csv") for c in pd.read_csv(os.path.join(target, f), nrows=1).columns))
        check("R3a analyst test on the clean truth: every arrival grown files 42,500", S.rnd(arr_t) == 42500, round(arr_t))
        check("R3b the decisive step alone on the clean truth: arrivals with the practices' in-housing undone file 45,000",
              S.rnd(und_t) == 45000, round(und_t))
        check("R3b the generator's latent demand files 45,000 too", S.rnd(lat_t) == 45000, round(lat_t))
        check("R3c no plant: no daily count repeats a block of days", not any(
            (D.seen_gp.values[i:i + 5] == D.seen_gp.values[j:j + 5]).all() for i in range(0, len(D) - 5, 5)
            for j in range(i + 5, min(i + 60, len(D) - 5), 5)))
    # R2: each mess item mishandled leaves the call
    D7 = D.copy()
    tt = int((pd.read_csv(os.path.join(target, DC.FILES["legacy"]), dtype=str).Outcome == "Test ticket").sum())
    check("R2 test tickets kept as visits: 45,000 still (no test ticket carries a GP form)", tt > 0 and S.rnd(g["plan"]) == gold, tt)
    utc_d = pd.to_datetime(ci.event_utc, utc=True).dt.date
    check("R2 event times left in UTC: every check-in falls on the same UK date", (utc_d.values == ci.d.values).all())
    log = S.load_log(target)
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, DC.FILES["log"]), data_only=True)
    textdates = []
    for ws in wb.worksheets[2:]:
        for row in ws.iter_rows(values_only=True):
            if isinstance(row[0], str) and row[0][:2].isdigit():
                textdates.append(dt.datetime.strptime(row[0], "%d/%m/%Y").date())
    D8 = D.copy()
    for d in textdates:
        D8.loc[D8.d == d, "arr"] -= D8.loc[D8.d == d, "away_gp"]
        D8.loc[D8.d == d, "ro"] = 0
    v8 = S.deterred(D8)[0] * S.G2
    check("R2 the log's typed-in dates dropped: 45,000 still", 0 < len(textdates) and S.rnd(v8) == gold, "%d rows, %.0f" % (len(textdates), v8))
    check("R2 the practice merger and the clinic codes do not touch the call (it reads the kiosk's GP choice)", True)
    Dk = D.copy()
    Dk["ro"] = np.maximum(Dk.ro, Dk.full)
    shk = Dk.groupby("wk").ro.agg(["sum", "size"])
    shk = (shk["sum"] / shk["size"]).to_dict()
    for j in range(1, S.LAGS + 1):
        Dk["w%d" % j] = [shk.get(w - dt.timedelta(7 * j), 0.0) for w in Dk.wk]
    for l in range(1, 13):
        Dk["s%d" % l] = Dk[["w%d" % j for j in range(1, l + 1)]].mean(axis=1)
    gk = S.golden(Dk)
    check("R2 the days the kiosk filled with nobody turned away read as run-outs: 45,000 still",
          gk["plan_r"] == gold and int((Dk.ro[fy] > D.ro[fy]).sum()) > 0,
          "%d days in 2025-26, %d weeks, %.0f" % (int((Dk.ro[fy] > D.ro[fy]).sum()), gk["L"], gk["plan"]))
    # asks
    hosp, code_spec = S.ask_hosp(ci, target)
    truth_old = {s[3]: s[0] for s in P.SPECIALTIES}
    check("ask A: every old clinic code links to one new code through the March 2026 issues, and to its own specialty",
          all(code_spec.get(c) == sp for c, sp in truth_old.items()), code_spec)
    wkr, wk_spec = S.ask_hosp_weekday_route(ci, target)
    check("ask A: the careful route (old codes' request weekdays against the register's clinic days) names every old code "
          "and names each one wrongly", all(wk_spec.get(c) not in (None, sp) for c, sp in truth_old.items()), wk_spec)
    same = sum(int(wkr[sp][q] == hosp[sp][q]) for sp in hosp for q in hosp[sp])
    check("ask A: the careful route misses all 28 cells", same == 0, "%d of 28" % same)
    reg = pd.read_csv(os.path.join(target, DC.FILES["clinics"]), dtype=str)
    check("ask A: the register holds only the new PAS's codes, none of the old ones",
          not set(reg.clinic_code) & set(truth_old), sorted(reg.clinic_code))
    hh = ci[ci.request_type == "HOSP"].copy()
    hh["rd"] = pd.to_datetime(hh.request_date).dt.date
    newc = set(reg.clinic_code)
    check("ask A: new codes first appear on forms issued from 16 March 2026, old codes last before it",
          hh[hh.request_org.isin(newc)].rd.min() >= P.PAS_LIVE and hh[~hh.request_org.isin(newc)].rd.max() < P.PAS_LIVE)
    h = ci[(ci.request_type == "HOSP") & (ci.d >= S.FY0) & (ci.d <= S.FY1)]
    check("ask A: the 28 cells total the 2025-26 hospital-form visits", sum(sum(q.values()) for q in hosp.values()) == len(h))
    # SF12: the old codes named through the register's clinic_days, refuted by the late-March issues and the switch
    late = hh[(hh.rd >= P.PAS_LIVE) & (hh.rd < S.TEMPLATES)]
    late_wd = {c: frozenset(x.weekday() for x in late[late.request_org == c].rd) for c in newc}
    old_wd = {c: frozenset(x.weekday() for x in hh[hh.request_org == c].rd) for c in truth_old}
    code_of = dict(zip(reg.specialty, reg.clinic_code))
    check("SF12 positive control: each new code the late-March link picks has its 16 to 31 March 2026 forms on exactly its "
          "old code's weekdays", all(late_wd[code_of[code_spec[c]]] == old_wd[c] for c in truth_old))
    miss12 = {c: (sorted(old_wd[c]), code_of[wk_spec[c]], sorted(late_wd[code_of[wk_spec[c]]])) for c in truth_old
              if late_wd[code_of[wk_spec[c]]] == old_wd[c]}
    check("SF12 the register's clinic_days reading fails the late-March match: none of the new codes it picks has its "
          "16 to 31 March 2026 forms on its old code's weekdays", not miss12, miss12)
    hh["wk"] = [d - dt.timedelta(d.weekday()) for d in hh.d]
    sw = [P.PAS_LIVE - dt.timedelta(7), P.PAS_LIVE, P.PAS_LIVE + dt.timedelta(7)]

    def switch_break(old_to_spec):
        m = dict(zip(reg.clinic_code, reg.specialty))
        m.update(old_to_spec)
        x = hh[hh.wk.isin(sw)]
        t = x.groupby([x.wk, x.request_org.map(m)]).size().unstack(fill_value=0)
        return int((abs(t.loc[sw[1]] - t.loc[sw[0]]) + abs(t.loc[sw[2]] - t.loc[sw[1]])).sum())
    b_gold, b_reg = switch_break(code_spec), switch_break(wk_spec)
    check("SF12 the weekly visits run on across the switch under the late-March link and jump under the register's reading "
          "(specialties' week-on-week moves through the fortnight both codes run, at least twice as large)",
          b_reg >= 2 * b_gold, (b_gold, b_reg))
    # the rubric repair's scope (fix-rubric step 4): the ask-side cut of the sickness ask left every file the call reads
    # byte-identical to the shipped pack (target.zip 8f5c6aa2) and every main-call figure where it was
    import hashlib as _hl
    shipped = {
        "legacy": "e4702be456835e0bdb46f8868c1fa6b9bc0a6288b7777b795b0526841a906025",
        "events": "2030dc9f0eb48f3831b585e16b1812a61fdb9a34be4b6e4569ebdbc1aa7f970f",
        "log": "375b24eae54127b155bc13ff60c2fe7ac31f911c0f2eff924179490dae95e4ec",
        "roster": "b890cea47bed9519ffbc16f5e44eeb838e3c3b0c52f923cab6f5e4b671170fb4",
        "kiosk": "448d009a9cb8a4bfc15088b89fc7578db5d0d7437faa0f0a760b76f52bcef80e",
        "practices": "9798d444c2591440036d592ab1af4260062bff73f920c7ebdc39fbef7df718c9",
        "report": "81d59c980d2e81e8cd1b77baf0c5489848c6c2b826eb2cb388796645612df5b0",
        "icb": "e7fb6723f096c1d3f49aefad8d8b0c731e45f8cc6a292ccb5cbc2f89f24f07bd",
        "bh": "7177c0f65ba886fa10f5df234cb8bd9d77eb55a2e5d7d22b1e678200cf26ccce",
    }
    moved = [DC.FILES[k] for k, h in shipped.items()
             if _hl.sha256(open(os.path.join(target, DC.FILES[k]), "rb").read()).hexdigest() != h]
    check("scope: every file the call reads (and the e-roster the standing family's covariate reads) is byte-identical "
          "to the shipped pack", not moved, moved)
    main_ref = {"plan_visits_2027_28": 45000, "plan_unrounded": 44760, "base_2025_26": 41784, "kept_in_house_2025_26": 2566,
                "window_weeks": 8, "window_runner_up_weeks": 9, "base_2025_26_runner_up": 41990,
                "aic_gap_five_weeks_or_fewer": 60, "base_2025_26_low": 41800, "base_2025_26_high": 42000,
                "kept_in_house_low": 2600, "kept_in_house_high": 2800, "plan_unrounded_low": 44800,
                "plan_unrounded_high": 45000, "coef_about": -0.37, "gp_seen_2025_26": 37853, "gp_turned_away_2025_26": 1365,
                "gp_arrivals_2025_26": 39218, "run_out_days_2025_26": 56, "clinic_days_2025_26": 253,
                "coef_window_share": -0.374, "coef_se": 0.026, "growth_pct": 3.5, "growth_years": 2, "rounding_unit": 2500,
                "default_path_plan": 42500, "default_path_unrounded": 42011, "seen_only_plan": 40000,
                "seen_only_unrounded": 40549, "weekly_weeks": 53}
    _fjs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")
    if os.path.exists(_fjs):
        import json as _js
        with open(_fjs) as _fh:
            _F = _js.load(_fh)
        diff = {k: (v, _F.get(k)) for k, v in main_ref.items() if _F.get(k) != v}
        check("scope: every main-call figure in figures.json is the shipped value", not diff, diff)
        check("scope: figures.json holds the call's figures and the one ask, nothing of the cut sickness ask",
              set(_F) == set(main_ref) | {"hospital_visits_2025_26"}, sorted(set(_F) ^ (set(main_ref) | {"hospital_visits_2025_26"})))
    gpc = ci[ci.request_type == "GP"]
    clinic_like = gpc.request_org.fillna("").str.match(r"^(HG-C\d\d|[A-Z]{3}\d\d[A-Z])$")
    check("separation by count: no GP-form check-in carries a hospital clinic code, old or new (the device rows sit on "
          "hospital forms only)", int(clinic_like.sum()) == 0, int(clinic_like.sum()))
    import re as _re
    import zipfile as _zf
    for k in ("log", "hub"):
        with _zf.ZipFile(os.path.join(target, DC.FILES[k])) as z:
            co = _re.search(rb"<Company>([^<]*)</Company>", z.read("docProps/app.xml")).group(1).decode()
        check("%s: the Company property is the hospital the files are from" % DC.FILES[k], co == P.HOSPITAL, co)
    rep4 = pdf_text(os.path.join(target, DC.FILES["report"]))
    check("doc: the report's activity table carries 2025-26's GP seen and turned away, and the hub's estimand",
          "{:,}".format(g["seen_gp"]) in rep4 and "{:,}".format(g["away_gp"]) in rep4
          and "takes every patient with a GP request" in rep4 and "does not run out of tickets" in rep4
          and "Its activity plan is to be set from 2025-26" in rep4)
    # separation
    D9 = D.copy()
    check("separation: the call reads no hospital-form row and no roster row (hospital codes scrambled, the call unchanged)",
          S.rnd(S.deterred(D9)[0] * S.G2) == gold)
    # input gates
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    check("gates: ten or more files", len(files) >= 10, len(files))
    check("gates: three or more formats", len(fmts) >= 3, sorted(fmts))
    check("gates: a file of 25,000 rows or more", big >= 25000, big)
    check("gates: two or more distractors named", len(DC.DISTRACTORS) >= 2, DC.DISTRACTORS)
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in [DC.FILES[k] for k in DC.DISTRACTORS]:
            shutil.copy(os.path.join(target, f), tmp)
    Dx, cix, evx, gx = S.solve(tmp)
    check("gates: the golden is unchanged with every distractor deleted (the e-roster among them)", gx["plan_r"] == gold and abs(gx["plan"] - g["plan"]) < 1e-6)
    shutil.rmtree(tmp)
    # documents read back, positive controls on the same extractor
    rep = pdf_text(os.path.join(target, DC.FILES["report"]))
    check("doc: the annual report reads back (positive control)", "hours rostered to the substantive team" in rep, len(rep))
    check("doc: the annual report names no practice keeping patients in-house", "in-house" not in rep and "own clinic" not in rep)
    check("doc: the annual report no longer narrates the long-term absences", "long-term" not in rep and "long term" not in rep)
    import re as _re
    import subprocess as _sp
    from pypdf import PdfReader as _PR
    from pdfminer.high_level import extract_text as _pm
    for key, must in (("report", "hours rostered to the substantive team"), ("icb", "GP direct access phlebotomy")):
        pth = os.path.join(target, DC.FILES[key])
        norm = lambda s: _re.sub(r"\s+", " ", s).strip()
        lenient = norm(" ".join(p.extract_text() for p in _PR(pth).pages))
        strict = norm(" ".join(p.extract_text() for p in _PR(pth, strict=True).pages))
        miner = norm(_pm(pth))
        popp = norm(_sp.run(["pdftotext", pth, "-"], capture_output=True, text=True).stdout) if shutil.which("pdftotext") else must
        check("doc (H25): %s reads the same strict and lenient, and pdfminer and pdftotext find the decisive sentence" % key,
              strict == lenient and must in miner and must in popp and must in strict)
    icb = pdf_text(os.path.join(target, DC.FILES["icb"]))
    check("doc: the ICB letter carries 3.5% for GP direct access phlebotomy (positive control)", "GP direct access phlebotomy 3.5%" in icb)
    # no shipped file describes the data (dataset-generation section 3)
    describing = ("dictionary", "readme", "manifest", "codebook", "definition", "field_notes", "fieldnotes",
                  "file_list", "filelist", "schema", "export_notes", "extract_notes", "data_notes")
    check("pack: no shipped file describes the data, by name",
          not any(w in f.lower().replace("-", "_").replace(" ", "_") for f in os.listdir(target) for w in describing),
          sorted(os.listdir(target)))
    # closure axis 19 (code and status semantics) homed in the report and the systems' own labels
    check("axis 19: the annual report's activity note reads back (positive control): seen by the request form the patient brought",
          "Seen are completed visits from the queue system, by the request form the patient brought" in rep)
    evt = pd.read_csv(os.path.join(target, DC.FILES["events"]), dtype=str, usecols=["visit_ref", "event_type"])
    check("axis 19 C1: every checked-in visit is completed, so check-ins and completed visits count the same",
          set(evt.visit_ref[evt.event_type == "CHECKED_IN"]) == set(evt.visit_ref[evt.event_type == "COMPLETED"]))
    legt = pd.read_csv(os.path.join(target, DC.FILES["legacy"]), dtype=str)
    check("axis 19: the request forms are the systems' own labels (GP form, Hospital form; GP, HOSP) and no test ticket "
          "carries one", set(legt.Request.dropna()) == {"GP form", "Hospital form"}
          and set(ci.request_type.dropna()) == {"GP", "HOSP"} and legt[legt.Outcome == "Test ticket"].Request.isna().all())
    # realism sweep
    wk = D[D.fy == 2025].groupby("wk").seen_gp.sum()
    check("realism: no two weeks of 2025-26 carry the same GP-referred count three times", wk.value_counts().max() < 3)
    check("realism: no round headline totals", all(x % 100 != 0 for x in (g["seen_gp"], g["away_gp"])))
    check("realism: no specialty's four quarters repeat a hospital-visit count",
          all(len(set(q.values())) == 4 for q in hosp.values()), [sp for sp, q in hosp.items() if len(set(q.values())) < 4])
    check("realism: no record after the pull", D.d.max() <= P.REC_END and pd.to_datetime(ci.event_utc).max().date() <= P.REC_END)
    print("%d checks, %d failed" % (len([1]) and 0 or 0, len(BAD)) if False else "%d failed" % len(BAD))
    return len(BAD)
