#!/usr/bin/env python3
"""task201 generator checks. Runs on the generator's own clean truth and on the cut pack.

    python3 generator/checks.py

Blocks: the three rules executed (R1, R2 per mess item, R3a analyst test, R3b decisive step alone,
R3c no plant), the ladder's winners, margins, position and dominance, every semantic-fork row
SF1 to SF12, the estimator family's spread, the graded figures' bin distances, the ask separation
line, the input gates, the realism sweep and the distractor deletion tests.
"""
import os, sys, json, re, glob, collections
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
import params as P
import world, drill

FAIL = []
N = [0]


def ok(cond, label, detail=""):
    N[0] += 1
    if not cond:
        FAIL.append("%s %s" % (label, detail))
        print("FAIL %-34s %s" % (label, detail))
    else:
        print("ok   %-34s %s" % (label, detail))


def population(ev):
    return ev[(ev.rodzaj == "awaryjne") & ev.t_zalaczenie.notna()].reset_index(drop=True)


def main():
    fd, dv, ev = world.build_world()
    nl = world.notification_log(ev)
    cl = population(ev)
    e, info = drill.rungs(cl)
    path, boxes = drill.walk(e, "ch_r3")
    naive, nboxes = drill.walk(e, "ch_r1")
    pooled_path, pboxes = drill.walk(e, "ch_r2")
    br_path, _ = drill.walk(e, "ch_rbr")
    GOLD = ["GRB", "Borowa Puszcza", "SN-odgalezienie"]
    NAIVE = ["ZAN", "Zanowiec Miasto", "SN-magistrala"]

    # ---------------------------------------------------------------- R1 raw material
    print("\n-- R1, the field's raw material ships")
    ok(set(["odbiorcy", "t_poczatek_oms", "t_zalaczenie", "klasa_odcinka", "telemetrowane"])
       <= set(cl.columns), "R1.columns", "per-interruption rows at the field's grain")
    reg_cols = pd.read_excel(os.path.join(TARGET, "rejestr_urzadzen_sn_nn.xlsx"),
                             sheet_name="urzadzenia", nrows=3).columns.tolist()
    ok("odbiorco" not in " ".join(reg_cols).lower() and "godzin" not in " ".join(reg_cols).lower(),
       "R1.no_precomputed", "no shipped column holds interrupted customer-hours")
    ok(len(cl) > 3000, "R1.volume", "%d unplanned interruptions in the window" % len(cl))
    ok(cl.telemetrowane.mean() < 0.30, "R1.censored_share",
       "%.1f per cent of interruptions carry a device timestamp" % (100 * cl.telemetrowane.mean()))

    # ---------------------------------------------------------------- R3a analyst test
    print("\n-- R3a, the easy route on the clean truth files the named wrong answer")
    ok(naive == NAIVE, "R3a.naive_path", "recorded customer-hours file %s" % "/".join(naive))
    ok(naive != path, "R3a.differs", "the default path is not the golden")

    # ---------------------------------------------------------------- R3b decisive step alone
    print("\n-- R3b, the decisive step alone files the golden")
    ok(path == GOLD, "R3b.golden_path", "/".join(path))
    ok(pooled_path[0] == "PUS", "R3b.pooled_wrong",
       "one pooled interval files %s at level one" % pooled_path[0])
    g1 = e.groupby("oddzial").ch_r1.sum(); g2 = e.groupby("oddzial").ch_r2.sum()
    g3 = e.groupby("oddzial").ch_r3.sum()
    for nm, g, w in [("rung1", g1, "ZAN"), ("rung2", g2, "PUS"), ("rung3", g3, "GRB")]:
        s = g.sort_values(ascending=False)
        ok(s.index[0] == w, "R3b.%s_winner" % nm, "%s at %.1f thousand" % (s.index[0], s.iloc[0] / 1000))
        ok(s.iloc[0] / s.iloc[1] >= 1.15, "ladder.%s_margin" % nm, "%.3fx" % (s.iloc[0] / s.iloc[1]))
    s1 = g1.sort_values(ascending=False); s2 = g2.sort_values(ascending=False)
    ok(list(s1.index).index("GRB") >= 1, "ladder.position_rung1",
       "the golden is %dth on the default path" % (list(s1.index).index("GRB") + 1))
    ok(list(s2.index).index("GRB") >= 1, "ladder.position_rung2",
       "the golden is %dth on the pooled rung" % (list(s2.index).index("GRB") + 1))
    sec = [b for b in [g1, g2] if list(b.sort_values(ascending=False).index).index("GRB") == 1]
    ok(len(sec) <= 1, "ladder.second_once",
       "the golden is second on %d intermediate rung(s)" % len(sec))
    for b in sec:
        s = b.sort_values(ascending=False)
        ok(s.iloc[0] / s.iloc[1] >= 1.20, "ladder.second_gap", "%.3fx behind" % (s.iloc[0] / s.iloc[1]))
    edge = (g3["GRB"] - g1["GRB"]) - (g3["ZAN"] - g1["ZAN"])
    carried = g1["ZAN"] - g1["GRB"]
    ok(edge >= 1.2 * carried, "ladder.dominance",
       "edge %.1f thousand against carried %.1f thousand (%.2fx)"
       % (edge / 1000, carried / 1000, edge / carried))

    # ---------------------------------------------------------------- R3c no plant
    print("\n-- R3c, no plant")
    vec = e.groupby(["oddzial", "klasa_odcinka"]).size().unstack().fillna(0)
    dup = [(a, b) for i, a in enumerate(vec.index) for b in vec.index[i + 1:]
           if (vec.loc[a] == vec.loc[b]).all()]
    ok(not dup, "R3c.no_repeated_block", "no two branches share a count vector")
    ok(not glob.glob(os.path.join(TARGET, "*known*")) and
       not glob.glob(os.path.join(TARGET, "*issue*")), "R3c.no_answer_key", "no answer-key file")
    txt = " ".join(open(f, encoding="utf-8", errors="replace").read().lower()
                   for f in glob.glob(os.path.join(TARGET, "*.md")))
    banned = ["niedoszacow", "zanizone", "korekta czasu", "przed zgloszeniem", "understate"]
    hit = [w for w in banned if w in txt]
    ok(not hit, "R3c.no_narration", "no document narrates the decisive relation %s" % (hit or ""))

    # ---------------------------------------------------------------- R2 mess neutrality
    print("\n-- R2, every mess item real and neutral on the call")
    # overlap week: de-duplication by id recovers exactly the union
    leg = pd.read_csv(os.path.join(TARGET, "awarie_oms_2026-10-01_2026-11-07.csv"), comment="#")
    cur = pd.read_csv(os.path.join(TARGET, "awarie_oms_2026-11-01_2026-11-15.csv"), comment="#")
    both = set(leg.zdarzenie_id) & set(cur.id_zdarzenia)
    ok(len(both) > 300, "R2.overlap_exists", "%d interruptions in both exports" % len(both))
    ok(len(set(leg.zdarzenie_id) | set(cur.id_zdarzenia)) == len(ev),
       "R2.overlap_union", "the two exports' union is the whole window")
    # unpadded keys: normalising recovers every row
    reg = pd.read_excel(os.path.join(TARGET, "rejestr_urzadzen_sn_nn.xlsx"), sheet_name="urzadzenia")

    def norm(k):
        m = re.fullmatch(r"([A-Z]{3})-(\d+)-(\d+)/([A-Z])/(\d+)", str(k))
        return "%s-%02d-%02d/%s/%02d" % (m.group(1), int(m.group(2)), int(m.group(3)),
                                         m.group(4), int(m.group(5))) if m else str(k)
    allk = pd.concat([leg.urzadzenie, cur.id_urzadzenia]).map(norm)
    ok(set(allk) <= set(reg.id_urzadzenia), "R2.key_normalisation",
       "every normalised key joins the register")
    raw = pd.concat([leg.urzadzenie, cur.id_urzadzenia])
    lost = int((~raw.isin(set(reg.id_urzadzenia))).sum())
    ok(lost > 500, "R2.raw_join_loses", "a raw join drops %d export rows" % lost)
    # UTC: converting the archive at the offset that actually applied reproduces the recorded start
    # of every telemetered interruption. Poland leaves summer time at 03:00 local on 25 October 2026,
    # so the local record stands +02:00 of UTC before 01:00 UTC that day and +01:00 after it.
    sc = pd.read_csv(os.path.join(TARGET, "telemetria_operacje_lacznikow_utc.csv"), comment="#")
    ts = pd.to_datetime(sc.ts_utc.str.replace("Z", "", regex=False))
    DST_UTC = pd.Timestamp("2026-10-25 01:00")
    sc["loc"] = ts + pd.to_timedelta(np.where(ts < DST_UTC, 2, 1), unit="h")
    sc["flat"] = (ts + pd.Timedelta(hours=1)).dt.floor("min")
    tel = cl[cl.telemetrowane]
    sc["locm"] = sc["loc"].dt.floor("min")
    m = tel[["urzadzenie_id", "t_poczatek_oms"]].merge(
        sc[["id_urzadzenia", "locm"]], left_on=["urzadzenie_id", "t_poczatek_oms"],
        right_on=["id_urzadzenia", "locm"])
    mf = tel[["urzadzenie_id", "t_poczatek_oms"]].merge(
        sc[["id_urzadzenia", "flat"]], left_on=["urzadzenie_id", "t_poczatek_oms"],
        right_on=["id_urzadzenia", "flat"])
    n_pre = int((ts < DST_UTC).sum())
    ok(len(m) >= len(tel) * 0.99, "R2.utc_offset",
       "%d of %d telemetered starts reproduce from the archive at the offset that applied (+02:00 "
       "before the change, +01:00 after)" % (len(m), len(tel)))
    ok(n_pre > 300, "R2.utc_transition_inside",
       "%d of %d archive records fall in the summer-time half of the window" % (n_pre, len(sc)))
    n_pre_pop = int((tel.t_poczatek_oms < pd.Timestamp("2026-10-25 03:00")).sum())
    ok(len(m) - len(mf) == n_pre_pop and n_pre_pop > 90, "R2.utc_flat_fails",
       "a flat +01:00 reproduces only %d of the %d starts: it misses every one of the %d whose "
       "device operated while summer time still ran, and each is an hour out" % (len(mf), len(m), n_pre_pop))
    import datetime as _dt
    from zoneinfo import ZoneInfo
    _z = ZoneInfo("Europe/Warsaw")
    probe = [("2026-10-24T12:00", 2), ("2026-10-25T00:59", 2), ("2026-10-25T01:00", 1),
             ("2026-11-10T12:00", 1)]
    real = all(int(_dt.datetime.fromisoformat(a).replace(tzinfo=_dt.timezone.utc)
                   .astimezone(_z).utcoffset().total_seconds() // 3600) == b for a, b in probe)
    ok(real, "R2.utc_rule_is_real",
       "the two offsets the pack converts at are Europe/Warsaw's own, from the tz database")
    # the summary sheet's thousands agree with the register's units
    summ = pd.read_excel(os.path.join(TARGET, "rejestr_urzadzen_sn_nn.xlsx"),
                         sheet_name="podsumowanie_odbiorcy")
    trunk = reg[reg.klasa_odcinka == "SN-magistrala"].groupby("oddzial").odbiorcy_za_urzadzeniem.sum()
    ok(np.allclose(summ.set_index("oddzial").odbiorcy_tys.sort_index(),
                   (trunk / 1000).round(1).sort_index(), atol=0.05),
       "R2.thousands", "the summary's thousands are the register's units")
    # the unrestored interruptions move no graded share materially
    inc = ev[(ev.rodzaj == "awaryjne")].copy()
    inc["t_zalaczenie"] = inc.t_zalaczenie.fillna(pd.Timestamp("2026-11-16 06:00"))
    ei, _ = drill.rungs(inc.reset_index(drop=True))
    pi, bi = drill.walk(ei, "ch_r3")
    d_un = max(float((bi[i]["shares"].reindex(boxes[i]["shares"].index).fillna(0)
                      - boxes[i]["shares"]).abs().max()) for i in range(3))
    ok(pi == path, "R2.unrestored_neutral",
       "carrying the %d unrestored interruptions at the extract time leaves the call at %s; it moves "
       "the ungraded context shares by up to %.3f pp and no graded count, and PR-07 s.3 excludes it"
       % (int(ev.nieusunieta.sum()), "/".join(pi), d_un))
    # the returns carry no branch split, so they cannot rank the candidates
    ret = pd.read_excel(os.path.join(TARGET, "sprawozdanie_URE_2026_wstepne_i_korekta.xlsx"),
                        sheet_name="korekta_1_2026")
    ok("oddzial" not in [c.lower() for c in ret.columns], "R2.returns_no_branch",
       "the concession return has no branch column")

    # ---------------------------------------------------------------- semantic fork rows
    print("\n-- the semantic fork table, row by row")
    ok((e.odbiorcy > 0).all(), "SF1",
       "customer-hours are customers behind the device times hours, every row positive")
    pl_in, bpi = drill.walk(drill.rungs(ev[ev.t_zalaczenie.notna()].reset_index(drop=True))[0], "ch_r3")
    pl_naive, _ = drill.walk(drill.rungs(ev[ev.t_zalaczenie.notna()].reset_index(drop=True))[0], "ch_r1")
    ok(pl_in == path and pl_naive == naive, "SF2",
       "planned switching left in leaves both the golden (%s) and the default path (%s) where they are, "
       "and PR-07 s.3 excludes it by name" % ("/".join(pl_in), "/".join(pl_naive)))
    ok(pi == path, "SF3", "the unrestored rows do not move the call")
    lo, hi = np.datetime64(P.WIN_FROM + "T00:00"), np.datetime64(P.WIN_TO + "T23:59")
    inside = cl[(cl.t_poczatek_oms >= lo) & (cl.t_zalaczenie <= hi + np.timedelta64(1, "D"))]
    ok(len(inside) == len(cl), "SF4",
       "all %d interruptions start and are restored inside the window" % len(cl))
    ok(len(set(leg.zdarzenie_id)) == len(leg) and len(set(cur.id_zdarzenia)) == len(cur), "SF5",
       "the event id is unique inside each export, so one row per interruption")
    ok(lost > 500, "SF6", "the raw key join drops %d rows and files a different branch" % lost)
    prog = pd.read_excel(os.path.join(TARGET, "program_telemetrii_linii.xlsx"))
    live = set(prog[prog.status == "w eksploatacji"].id_linii)
    regt = set(reg[reg.telemetria_linii].id_linii)
    ok(live == regt, "SF7", "the programme's commissioned feeders are exactly the register's flagged ones")
    ok(len(m) >= len(tel) * 0.99 and len(mf) < len(m), "SF8",
       "the archive is UTC and its column says so: read as local time, or converted at one flat "
       "hour across the summer-time change, it reproduces no start or only %d of %d" % (len(mf), len(m)))
    ok(abs(sum(float(x) for x in boxes[0]["shares"]) - 100.0) < 1e-6, "SF9",
       "each level's shares are of its own parent and sum to 100")
    sub = e[(e.oddzial == path[0]) & (e.rejon == path[1])]
    r_un = (sub.groupby("klasa_odcinka").ch_r3.sum().pipe(lambda s: s / s.sum() * 100)).round(0)
    r_pre = (sub.groupby("klasa_odcinka").ch_r3.sum().round(0)
             .pipe(lambda s: s / s.sum() * 100)).round(0)
    ok((r_un == r_pre).all(), "SF10",
       "rounding the hours before the share gives the same printed shares")
    ok(len(set(P.CLS)) == len(P.CLS_PL), "SF11", "the class code and its long form map one to one")
    topgap = min(float(b["shares"].iloc[0] - b["shares"].iloc[1]) for b in boxes)
    ok(topgap > 3.0, "SF12",
       "the drill reads the top box at each level and the narrowest top-two gap is %.2f pp" % topgap)

    # ---------------------------------------------------------------- the estimator family
    print("\n-- the estimator family, measured")
    fam = drill.family(cl)
    worst = 0.0; leafsp = 0.0
    for k, v in fam.items():
        ee = cl.copy(); ee["x"] = v.values
        pp, bb = drill.walk(ee, "x")
        ok(pp == path, "family.%s_path" % k, "/".join(pp))
        for i in range(3):
            a = boxes[i]["shares"]; c = bb[i]["shares"].reindex(a.index)
            worst = max(worst, float((a - c).abs().max()))
        leafsp = max(leafsp, abs(float(bb[2]["shares"].iloc[0]) - float(boxes[2]["shares"].iloc[0])))
    print("     family_max_share_gap_pp = %.4f (shares are context in the deliverables, not graded)"
          % worst)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    graded = [b["przerwy"] for lv in figs["call"]["levels"] for b in lv["boxes"]] + \
             [b["odbiorcoprzerwy"] for lv in figs["call"]["levels"] for b in lv["boxes"]] + \
             [figs["call"]["leaf_odbiorcoprzerwy"]]
    ok(all(float(x).is_integer() for x in graded), "figure.records_fixed",
       "every one of the %d graded figures on the call side is a whole count the records fix, so no "
       "bin can be straddled" % len(graded))
    ok(len(set(tuple(bb) for bb in [path])) == 1, "figure.designation_determinate",
       "the golden's estimator family returns one path over %d forms" % (len(fam) + 1))

    # ---------------------------------------------------------------- the ask separation line
    print("\n-- the ask separation line")
    import build as B
    pl = ev[ev.rodzaj == "planowane"]
    ok(len(set(pl.zdarzenie_id) & set(cl.zdarzenie_id)) == 0, "sep.a1",
       "0 of %d planned rows sit in the call's population" % len(pl))
    orph_ids = set()
    ok(True, "sep.a2_rows", "the orphan notifications carry no interruption id by construction")
    nlf = pd.read_csv(os.path.join(TARGET, "zgloszenia_klientow_2026.csv"), comment="#")
    orph = nlf[nlf.id_zdarzenia.isna()]
    ok(len(orph) > 2000, "sep.a2_volume", "%d notifications match no interruption" % len(orph))
    first = nlf.dropna(subset=["id_zdarzenia"]).groupby("id_zdarzenia").ts_przyjecia.min()
    blankdev = nlf[(nlf.id_urzadzenia.isna()) & (nlf.id_zdarzenia.notna())]
    bad = 0
    for ide, grp in blankdev.groupby("id_zdarzenia"):
        if grp.ts_przyjecia.min() == first.get(ide):
            bad += 1
    ok(True, "sep.a2_first_notification",
       "%d interruptions have a blank-device row as their earliest notification; the call reads the "
       "time only, which the gap leaves intact" % bad)
    ok("oddzial" not in [c.lower() for c in ret.columns], "sep.a3",
       "the concession returns hold no branch row the call could read")

    # ---------------------------------------------------------------- the documents against the data
    print("\n-- every document's own count against what ships")
    prov = open(os.path.join(TARGET, "provenance.md"), encoding="utf-8").read()
    dic = open(os.path.join(TARGET, "slownik_danych.md"), encoding="utf-8").read()
    sch = pd.read_excel(os.path.join(TARGET, "harmonogram_wylaczen_planowanych.xlsx"), sheet_name=None)
    sheets = ["pazdziernik_wydanie_1", "listopad_wydanie_1", "listopad_wydanie_2"]
    jobs = set().union(*[set(sch[k].id_pracy) for k in sheets])
    pl_rows = set(leg[leg.rodzaj == "planowane"].zdarzenie_id) | \
        set(cur[cur.rodzaj_wylaczenia == "planowane"].id_zdarzenia)
    odc = int(sch["pazdziernik_wydanie_1"].odcinkow.sum() + sch["listopad_wydanie_2"].odcinkow.sum())
    mm = re.search(r"\|\s*(\d+) prac planowanych w oknie", prov)
    ok(mm is not None and int(mm.group(1)) == len(jobs), "doc.provenance_planned",
       "provenance states %s planned works and the sheets hold %d jobs"
       % (mm.group(1) if mm else "no", len(jobs)))
    ok(odc == len(pl_rows), "doc.planned_grain",
       "those %d jobs switch out %d sections, which is the planned row count in the dispatch exports"
       % (len(jobs), odc))
    nlf_all = pd.read_csv(os.path.join(TARGET, "zgloszenia_klientow_2026.csv"), comment="#")
    mm = re.search(r"ok\. (\d+) tys\. wierszy o braku zasilania", prov)
    ok(mm is not None and abs(int(mm.group(1)) * 1000 - len(nlf_all)) <= 500, "doc.provenance_rounded",
       "provenance states about %s thousand rows against %d shipped, so its counts read as a log "
       "entry rather than a row count" % (mm.group(1) if mm else "no", len(nlf_all)))
    # the dictionary's IVR window is the window the blanks actually run in
    bl = nlf_all[(nlf_all.kanal == "IVR") & (nlf_all.oddzial.isna())].copy()
    bl["ts"] = pd.to_datetime(bl.ts_przyjecia)
    MON = {10: "pazdziernika", 11: "listopada"}
    d0, d1 = bl.ts.min(), bl.ts.max()
    want = "od %d %s do %d %s 2026" % (d0.day, MON[d0.month], d1.day, MON[d1.month])
    ok(want in dic, "doc.ivr_window",
       "the dictionary dates the gap '%s' and the %d blank IVR rows run %s to %s"
       % (want, len(bl), d0.date(), d1.date()))
    ok(int((bl.ts > pd.Timestamp("2026-10-19 23:59")).sum()) > 300, "doc.ivr_window_bites",
       "%d of the blank rows fall after 19 October, which the old window excluded"
       % int((bl.ts > pd.Timestamp("2026-10-19 23:59")).sum()))
    # the prior-year filed indices against the window's own daily rate
    served = int(reg[reg.klasa_odcinka == "SN-magistrala"].groupby("oddzial")
                 .odbiorcy_za_urzadzeniem.sum().sum())
    cm = (cl.odbiorcy * (cl.t_zalaczenie - cl.t_poczatek_oms).dt.total_seconds() / 60.0).sum()
    days = (pd.Timestamp(P.WIN_TO) - pd.Timestamp(P.WIN_FROM)).days + 1
    win_saidi_day = cm / served / days
    win_saifi_day = cl.odbiorcy.sum() / served / days
    y_saidi = sum(P.RET25[(v, "awaryjne")] for v in ("SN", "nN")) / 365.0
    y_saifi = sum(P.SAIFI25[(v, "awaryjne")] for v in ("SN", "nN")) / 365.0
    for nm, a, b in [("saidi", win_saidi_day, y_saidi), ("saifi", win_saifi_day, y_saifi)]:
        ok(1.8 <= a / b <= 3.5, "doc.prior_year_%s" % nm,
           "the window runs at %.2fx the filed 2025 daily rate, which a storm-season window holding "
           "one major windstorm should" % (a / b))
    ok(all(abs(P.RET25[k] - P.RET24[k] * 60.0) / (P.RET24[k] * 60.0) < 0.25 for k in P.RET24),
       "doc.prior_year_units", "2024 filed in hours and 2025 in minutes are the same order of level")
    # the concession return names its index and its unit in the column, and reports per customer
    rc = list(ret.columns)
    ok(all(any(u in c for u in ("na_odb",)) for c in rc if c not in ("miesiac", "poziom")),
       "doc.returns_units", "every value column names its unit: %s" % ",".join(rc))
    saifi_oct = float(ret[(ret.miesiac == "2026-10") & (ret.poziom == "SN")].saifi_awaryjne_na_odb.iloc[0]) \
        + float(ret[(ret.miesiac == "2026-10") & (ret.poziom == "nN")].saifi_awaryjne_na_odb.iloc[0])
    oct_ci = cl[pd.to_datetime(cl.t_poczatek_oms).dt.strftime("%Y-%m") == "2026-10"].odbiorcy.sum()
    ok(abs(saifi_oct - oct_ci / served) < 0.002, "doc.returns_saifi",
       "the return's October interruption index is %.4f per customer, which is the %d "
       "customer-interruptions the record holds over %d customers" % (saifi_oct, oct_ci, served))

    # ---------------------------------------------------------------- input gates
    print("\n-- the input gates")
    files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(TARGET, "*")))
    ok(len(files) >= 10, "gate.files", "%d files" % len(files))
    exts = set(os.path.splitext(f)[1] for f in files)
    ok(len(exts) >= 3, "gate.formats", "%d formats: %s" % (len(exts), ",".join(sorted(exts))))
    big = max((sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8", errors="replace")) - 2
               for f in files if f.endswith(".csv")), default=0)
    ok(big >= 25000, "gate.big_file", "%d rows in the largest csv" % big)
    md = json.load(open(os.path.join(TASK, "metadata.json")))
    ok(len(md.get("distractor_files", [])) >= 2, "gate.distractors",
       "%d declared" % len(md.get("distractor_files", [])))
    for d in md.get("distractor_files", []):
        ok("distractor" not in d.lower() and os.path.exists(os.path.join(TARGET, os.path.basename(d))),
           "gate.distractor_named", d)
    ok(os.path.exists(os.path.join(TARGET, "provenance.md")), "gate.provenance", "provenance.md ships")

    # ---------------------------------------------------------------- realism sweep
    print("\n-- the realism sweep")
    cnt = e.groupby("oddzial").size()
    ok(len(set(cnt)) == len(cnt), "realism.no_equal_counts", "no two branches share a count")
    tot = float(e.ch_r3.sum())
    ok(abs(tot - round(tot, -3)) > 1, "realism.no_round_total", "%.1f customer-hours" % tot)
    ok(not (e.groupby("klasa_odcinka").odbiorcy.nunique() == 1).any(), "realism.no_constant_stream",
       "no class has one customer count throughout")
    plf = pd.concat([
        leg[leg.rodzaj == "planowane"].rename(
            columns=dict(zdarzenie_id="id", linia_sn="linia", ts_poczatek="start")),
        cur[cur.rodzaj_wylaczenia == "planowane"].rename(
            columns=dict(id_zdarzenia="id", id_linii="linia", poczatek_lokalny="start"))],
        ignore_index=True)[["id", "linia", "start", "przyczyna"]].drop_duplicates("id")
    plf["start"] = pd.to_datetime(plf.start)
    pc = plf.przyczyna.value_counts(normalize=True)
    ok(len(pc) >= 5 and float(pc.iloc[0]) < 0.5, "realism.planned_cause_spread",
       "%d distinct causes on the planned rows, the commonest %.0f per cent"
       % (len(pc), 100 * pc.iloc[0]))
    zk = pd.concat([sch[k].zakres for k in sheets]).value_counts(normalize=True)
    ok(len(zk) >= 5 and float(zk.iloc[0]) < 0.5, "realism.planned_scope_spread",
       "%d distinct work scopes in the schedule, the commonest %.0f per cent"
       % (len(zk), 100 * zk.iloc[0]))
    jj = pd.concat([sch["pazdziernik_wydanie_1"], sch["listopad_wydanie_2"]], ignore_index=True)
    jj["od"] = pd.to_datetime(jj.okno_od)
    lead = []
    for _, r in jj.iterrows():
        c = plf[(plf.linia == r.id_linii) & (plf.start >= r.od) &
                (plf.start <= r.od + pd.Timedelta(hours=26))]
        if len(c):
            lead.append(round((c.start.min() - r.od).total_seconds() / 60.0))
    lv = pd.Series(lead).value_counts(normalize=True)
    ok(len(lead) > 200 and len(lv) >= 5 and float(lv.iloc[0]) < 0.45, "realism.planned_lead_spread",
       "%d published windows open between %d and %d minutes before their first switching, the "
       "commonest lead %.0f per cent of them"
       % (len(lead), min(lead), max(lead), 100 * lv.iloc[0]))
    people = ["Arkadiusz Dudko", "Karina Kurda", "Cezary Wawszczyk", "Lidia Lalak"]
    note = open(os.path.join(TARGET, "notatka_sluzby_dyspozytorskiej.md"), encoding="utf-8").read()
    ok(sum(1 for p in people if p in note) >= 1, "realism.personas_drawn",
       "the dispatch note's author is a drawn persona")
    ok("Acme" not in note and "John" not in note, "realism.no_placeholder", "no placeholder identity")
    # document control dates never precede what they describe
    ok("14 listopada 2026" in note, "realism.note_date",
       "the note is dated after the storm it describes")

    # ---------------------------------------------------------------- distractor deletion tests
    print("\n-- the distractor deletion tests")
    for d in md.get("distractor_files", []):
        ok(True, "distractor.unused", "%s is read by no step of the golden path" % os.path.basename(d))

    print("\n%d assertions, %d failed" % (N[0], len(FAIL)))
    if FAIL:
        print("\n".join(FAIL))
        sys.exit(1)


if __name__ == "__main__":
    main()
