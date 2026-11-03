"""task402 generator checks: every fork in the design note's table, the analyst test on the clean truth, mid-bin on
every graded figure, the ask devices' mass, the joint re-trip closure over redraws, realism and the metadata scrub.

    python3 checks.py [--fast]        exit 1 on any failure (--fast skips the 20 redraws)"""
import json, os, re, sys, zipfile
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world, asks, golden, ladder as L
from normal import normalise

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FAIL = []


def ok(name, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAIL.append(name)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def docx_text(path):
    z = zipfile.ZipFile(path)
    return re.sub(r"<[^>]+>", " ", z.read("word/document.xml").decode("utf8"))


def main(fast=False):
    P = golden.load(T)
    F, med, frost = P["F"], P["med"], P["frost"]
    m = golden.main_figures(P)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    order = sorted(m, key=lambda k: -m[k])
    # ---------------------------------------------------------------- the call and its figures
    ok("call: the switching revision costs the most", order[0] == "G", str({k: round(v) for k, v in m.items()}))
    ok("call: at least 1.5 times the runner-up", m["G"] >= 1.5 * m[order[1]], "%.2f" % (m["G"] / m[order[1]]))
    v = golden.variants(P)
    r100 = {k: round(x / 100) * 100 for k, x in v.items()}
    ok("SF5 netting and every licensed pairing variant give one figure", len(set(r100.values())) == 1,
       "%d variants, %s" % (len(v), sorted(set(round(x) for x in v.values()))))
    ok("SF5 the staged era carries no re-trip, so netting is nil", abs(v["not_netted"] - m["G"]) < 1e-6)
    # ---------------------------------------------------------------- forks
    pol = docx_text(os.path.join(T, "board_policy_407_reliability_work_plan.docx"))
    ok("SF1 one record one interruption is filed", "as the outage management system records them" in pol)
    merged = F.copy()
    pr = L.pair(F[~F.planned], 10, 60, frost).reindex(F.index, fill_value=False)
    ok("SF1 merging a re-trip into the interruption before it would move the figure (the filed reading decides)", pr.sum() > 0, "%d paired records" % pr.sum())
    dsaidi = (F[~F.planned].groupby((F.start // 1440).astype(int)).ci.size())
    near = set()
    dr = pd.read_excel(os.path.join(T, "daily_reliability_fy2021-fy2026.xlsx"), sheet_name="OMS daily")
    ds = pd.Series(dr.saidi_min.values, index=(pd.to_datetime(dr.date) - golden.D0).dt.days.values)
    near = set(ds.index[(ds.values > 0.75 * P["tmed"]) & (ds.values < 1.25 * P["tmed"])])
    graded_days = set((F.start[pr & (F.start >= L.G_DAY * 1440)] // 1440).astype(int))
    ok("SF2 no paired re-trip on a day within 25 per cent of the major event threshold", not (graded_days & near))
    nomed = golden.main_figures(dict(P, med=set()))
    ok("SF2 the costs without any major event exclusion keep the call", max(nomed, key=nomed.get) == "G",
       str({k: round(x) for k, x in nomed.items()}))
    withpl = dict(P, F=F.assign(planned=False))
    mp = golden.main_figures(withpl)
    ok("SF3 planned work included changes no cost's bin", all(round(mp[k] / 100) == round(m[k] / 100) for k in m), str({k: round(x) for k, x in mp.items()}))
    b = [L.Y2 * 1440, L.YE * 1440]
    ok("SF4 no paired re-trip within a day of either end of the year",
       not any(abs(F.start[pr] - x).min() < 1440 for x in b))
    rev = docx_text(os.path.join(T, "reliability_review_fy2026.docx"))
    ok("SF6 the review files each change's in-place date", all(s in rev for s in ("1 Nov 2025", "1 Dec 2025", "1 Oct 2025", "1 Jan 2026", "1 Feb 2026")))
    e2 = L.replay_guards(F, med, P["sites_2026"], start=L.day("2026-02-01"))
    d2 = L.replay_risers(F, med, P["risers_2025"], start=L.day("2025-11-01"))
    ok("SF6 counting from the month after the date keeps the call", m["G"] > max(e2, d2, m["R"]), "E %.0f D %.0f" % (e2, d2))
    rb = pd.read_excel(os.path.join(T, "heat_pump_rebates_fy2024-fy2026.xlsx"))
    rb["xf"] = rb.service_transformer.str.replace("T-", "T", regex=False)
    allx = ((pd.to_datetime(rb.connected) - golden.D0).dt.days).groupby(rb.xf).min().to_dict()
    r_all = L.replay_heat_pumps(F, med, allx)
    ok("SF7 every rebate connection in place of the waiver's: the same bin", round(r_all / 100) == round(m["R"] / 100), "%.0f against %.0f" % (r_all, m["R"]))
    sec = P["sec"]; mem = dict(zip(sec.section_id, sec.members))
    xm = pd.read_excel(os.path.join(T, "system_register_2026-09-30.xlsx"), sheet_name="transformers")
    xmem = dict(zip(xm.transformer_id, xm.members_served))
    fy = F[(F.start >= L.Y2 * 1440) & ~F.planned]
    agree = np.mean([(r.ci == (xmem[r.xf] if r.level == "transformer" else mem[r.sec])) for r in fy.itertuples()])
    ok("SF8 customers interrupted agree with the register's members on every record", agree == 1.0, "%.4f" % agree)
    ok("SF9 every cost rounded once", all(figs["costs"][golden.CHANGES[k]] == round(m[k] / 100) * 100 for k in m))
    S = sec.set_index("section_id")
    conn = set(rb.section_id[rb.load_study == "waived"])
    prY = pr & (F.start >= L.G_DAY * 1440) & (F.start < L.YE * 1440) & ~F.start.floordiv(1440).isin(med)
    share = F.ci[prY & F.sec.isin(conn)].sum() / F.ci[prY].sum()
    booked_G = m["G"] - F.ci[prY & F.sec.isin(conn)].sum(); booked_R = m["R"] + F.ci[prY & F.sec.isin(conn)].sum()
    ok("SF10 re-trips on sections with a waiver connection are a minority", share < 0.4, "%.0f per cent" % (100 * share))
    ok("SF10 booked to the heat pump policy, the switching revision still costs the most", booked_G > max(booked_R, m["E"], m["D"]),
       "%.0f against %.0f" % (booked_G, booked_R))
    terms = docx_text(os.path.join(T, "heat_pump_rebate_terms_2025-26.docx"))
    ok("SF10 the rebate goes only to homes heated by electric resistance", "heated mainly by electric resistance heat" in terms)
    ok("SF11 the load study checks the service transformer and secondary", "service transformer and the secondary conductor" in terms)
    # ---------------------------------------------------------------- the analyst test on the clean truth
    ovl = L.category_rise(F, med, "OVLD")
    ok("analyst test: the overload category's rise booked to the heat pumps files them", ovl > m["G"], "%.0f against %.0f" % (ovl, m["G"]))
    hp = set(rb.section_id[rb.load_study == "waived"])
    eh = dict(zip(sec.section_id, sec.electric_heat_members / sec.members))
    secs = list(sec.section_id)
    scope = L.scope_did(F.assign(sec=F.sec.map({s: i for i, s in enumerate(secs)})), med, {secs.index(s) for s in hp})
    strat = L.scope_did(F.assign(sec=F.sec.map({s: i for i, s in enumerate(secs)})), med, {secs.index(s) for s in hp},
                        bands=[0.18, 0.3, 0.45, 0.6], eheat=np.array([eh[s] for s in secs]))
    rungs = {"scope": dict(m, R=scope, G=0.0), "banded": dict(m, R=strat, G=0.0), "category": dict(m, R=ovl, G=0.0)}
    for k, rr in rungs.items():
        w = max(rr, key=rr.get)
        ok("ladder rung %s names %s, not the switching revision" % (k, w), w != "G", "%.0f" % rr[w])
    tot = F.ci[(F.start >= L.Y2 * 1440) & ~F.planned & ~F.start.floordiv(1440).isin(med)].sum() - \
        F.ci[(F.start >= L.Y1 * 1440) & (F.start < L.Y2 * 1440) & ~F.planned & ~F.start.floordiv(1440).isin(med)].sum()
    resid = tot - ovl - (L.category_rise(F, med, "ANML") + L.category_rise(F, med, "UGTERM") + L.category_rise(F, med, "XFMR"))
    ok("SF12 ladder: the system residual after the category rises does not reach the switching revision's cost", resid < m["G"] * 0.5, "%.0f" % resid)
    # ---------------------------------------------------------------- mid-bin on every graded figure
    graded = [("cost " + k, m[k], 100) for k in m] + [("gap", m["G"] - m[order[1]], 100)]
    A = golden.maifi_files(P, "golden"); h, p = golden.callouts_files(P, "golden")
    graded += [("MAIFIe %s Q%d" % k, A[k], 0.01) for k in A] + [("hours %d" % i, h[i], 1) for i in range(12)] + [("pay %d" % i, p[i], 1) for i in range(12)]
    worst = min(graded, key=lambda g: edge(g[1], g[2]) / g[2])
    ok("mid-bin: every graded figure at least 7 per cent of its unit from a rounding edge", all(edge(x, u) >= 0.07 * u for _, x, u in graded),
       "tightest %s %.4f (edge %.1f per cent)" % (worst[0], worst[1], 100 * edge(worst[1], worst[2]) / worst[2]))
    # ---------------------------------------------------------------- the asks: files against the world, and the devices
    import build
    W, Fw, O, R, EMP = build.truth()
    Aw = asks.maifi(O, W["S"], "golden")
    dn = ["North", "Lakes", "Prairie", "River"]
    ok("ask A: the files reproduce the world's MAIFIe", max(abs(Aw[i, q - 1] - A[(dn[i], q)]) for i in range(4) for q in (1, 2, 3, 4)) < 1e-9)
    hw, pw = asks.callout_figures(R, "golden")
    ok("ask B: the files reproduce the world's hours and pay", np.allclose(hw, h) and np.allclose(pw, p, atol=1e-6))
    full = golden.maifi_files(P, "full"); cr = golden.maifi_files(P, "cracker")
    p1 = [k for k in A if k[0] in ("North", "Lakes")]
    p2 = [k for k in A if k[0] in ("Prairie", "River") and k[1] < 4]
    ok("ask A P1: counting each device's sequences moves every North and Lakes figure", all(abs(round(cr[k], 2) - round(full[k], 2)) >= 0.0099 for k in p1))
    ok("ask A P2: the feeders as they stand at year end move every Prairie and River figure before July", all(abs(round(full[k], 2) - round(A[k], 2)) >= 0.0099 for k in p2))
    hf, pf = golden.callouts_files(P, "full"); hc, pc = golden.callouts_files(P, "cracker")
    ok("ask B P1: each row its own callout moves every month's pay", all(abs(round(pc[i]) - round(pf[i])) >= 1 for i in range(12)))
    moved_b = sum(1 for i in range(12) if abs(round(hf[i]) - round(h[i])) >= 1) + sum(1 for i in range(12) if abs(round(pf[i]) - round(p[i])) >= 1)
    ok("ask B P2: dating each row by its Monday entry instead of its order's outage moves at least three fifths of the figures", moved_b >= 15, "%d of 24" % moved_b)
    c = golden.crew_frame(P, "golden").sort_values(["emp", "s"])
    ok("ask B literal: every restoration row is an OUTAGE order at face value; no capital or service row sits in a restoration chain",
       set(golden.crew_frame(P, "golden").wo_type) == {"OUTAGE"})
    hol = set(pd.to_datetime(asks.HOLIDAYS))
    ch = c.assign(gap=c.s - c.groupby("emp").e.shift(1))
    ch["cid"] = (ch.gap.isna() | (ch.gap >= 15)).cumsum()
    spans = ch.groupby("cid").agg(s=("s", "min"), e=("e", "max"))
    sd = golden.D0 + pd.to_timedelta(spans.s * 60, "s"); ed = golden.D0 + pd.to_timedelta((spans.e - 1) * 60, "s")
    ok("ask B: no restoration callout crosses a month boundary", (sd.dt.month == ed.dt.month).all())
    short = spans.e - spans.s < 120
    ok("ask B: no callout under two hours touches a holiday", not (short & (sd.dt.normalize().isin(hol) | ed.dt.normalize().isin(hol))).any())
    # ---- Ask A: the feeder record, and one event per member is one event per fault
    reg = pd.read_excel(os.path.join(T, "system_register_2026-09-30.xlsx"), sheet_name=None)
    ok("ask A literal: the register states its as-at date inside the workbook", (reg["sections"].as_at.astype(str) == "2026-09-30").all()
       and (reg["reclosing_devices"].as_at.astype(str) == "2026-09-30").all())
    Sw = W["S"]
    nmoved = int((Sw.feeder_new != Sw.feeder).sum())
    ok("ask A literal: every section moved on 1 June 2026 has its transfer recorded in the outage extract", (F.cause == "XFER").sum() == nmoved, "%d transfers" % nmoved)
    Sq, _ = golden.scada_events(P, "oms")
    Sq = Sq[~Sq.lockout]
    cur, hist = golden.feeder_history(P)
    secs_on = {}
    for s_, f_ in cur.items():
        secs_on.setdefault(f_, []).append(s_)
    reach = {}
    for k_, i_, t_ in zip(Sq.kind.values, Sq.id.values, Sq.t.values):
        ss = [s_ for s_ in cur if (hist[s_][0] if (s_ in hist and t_ < hist[s_][1]) else cur[s_]) == i_] if k_ == "B" else [i_]
        for s_ in ss:
            reach.setdefault(s_, []).append(t_)
    mid = 0
    for s_, ts in reach.items():
        ts = np.sort(np.array(ts))
        d_ = np.diff(ts)
        mid += int(((d_ > 1.0 / 60) & (d_ <= 5.0)).sum())
    ok("ask A P1: no member sees two operations between one second and five minutes apart (every merge is one fault's same-second pair)", mid == 0, "%d" % mid)
    # ---- main side, lesson (ii): every graded cost and the gap at every estimator the filed text allows
    rb2 = pd.read_excel(os.path.join(T, "heat_pump_rebates_fy2024-fy2026.xlsx"))
    ix = {s_: i_ for i_, s_ in enumerate(secs)}
    hpi = {ix[s_] for s_ in rb2.section_id[rb2.load_study == "waived"]}
    ehv = np.array([eh[s_] for s_ in secs])
    Fx = F[F.level == "transformer"].assign(sec=lambda d_: d_.sec.map(ix))
    r_ests = {"replay": m["R"], "every rebate connection": r_all, "scope, transformer trips": L.scope_did(Fx, med, hpi),
              "scope in electric-heat bands, transformer trips": L.scope_did(Fx, med, hpi, bands=[0.18, 0.3, 0.45, 0.6], eheat=ehv)}
    ok("SF13 the heat pump policy's cost holds its bin under every estimator of the trips a load study checks",
       len({round(x / 100) for x in r_ests.values()}) == 1 and all(edge(x, 100) >= 7 for x in r_ests.values()),
       ", ".join("%s %.0f" % kv for kv in r_ests.items()))
    ok("SF13 the gap holds its bin under each of them", len({round((m["G"] - x) / 100) for x in r_ests.values()}) == 1,
       ", ".join("%.0f" % (m["G"] - x) for x in r_ests.values()))
    Fa = F.assign(sec=F.sec.map(ix))
    sec_share = 1 - L.scope_did(Fx, med, hpi) / max(L.scope_did(Fa, med, hpi), 1)
    ok("SF13 the unrestricted scope comparison counts section-device trips a load study never checks", sec_share > 0, "%.0f per cent of it" % (100 * sec_share))
    al = pd.read_excel(os.path.join(T, "asset_programme_lists_2022-2026.xlsx"), sheet_name=None)
    gfit = al["animal_guards"].dropna(subset=["fitted"])
    fitted = dict(zip(gfit.structure_id, (pd.to_datetime(gfit.fitted) - golden.D0).dt.days))
    an = F[(F.cause == "ANML") & ~F.planned]
    after = sum(1 for r in an.itertuples() if r.site in fitted and r.start >= fitted[r.site] * 1440)
    expo = sum(max(0, L.YE - d_) for d_ in fitted.values()) + 0.0
    before = sum(1 for r in an.itertuples() if r.site in P["sites_2026"] and r.start < L.E_DAY * 1440 and r.start >= L.day("2021-10-01") * 1440)
    resid = (after / max(expo, 1)) / max(before / (len(P["sites_2026"]) * (L.E_DAY - L.day("2021-10-01"))), 1e-9)
    ok("lesson (ii) animal guards: netted by the contact rate at sites already guarded, the same bin", round(m["E"] * (1 - resid) / 100) == round(m["E"] / 100), "residual %.1f per cent, %.0f" % (100 * resid, m["E"] * (1 - resid)))
    rr = al["riser_replacements"].dropna(subset=["replaced"])
    repd = dict(zip(rr.riser_structure_id, (pd.to_datetime(rr.replaced) - golden.D0).dt.days))
    tf = F[(F.cause == "UGTERM") & ~F.planned]
    ok("lesson (ii) risers: no replaced riser failed after its replacement, so nothing nets", not any(r.riser in repd and r.start >= repd[r.riser] * 1440 for r in tf.itertuples()))
    un = pd.read_parquet(os.path.join(T, "transformer_units.parquet"))
    oldfit = un[(un.supplier != golden.NEW_SUP) & (pd.to_datetime(un.fitted) >= "2021-10-01")]
    of = dict(zip(oldfit.transformer_id, (pd.to_datetime(oldfit.fitted) - golden.D0).dt.days))
    xf_ = F[(F.cause == "XFMR") & ~F.planned & (F.level == "transformer")]
    infant = sum(1 for r in xf_.itertuples() if r.xf in of and of[r.xf] * 1440 <= r.start < (of[r.xf] + 240) * 1440)
    rate_old = infant / max(len(of), 1)
    newfit = un[(un.supplier == golden.NEW_SUP)]
    net_f = m["F"] - rate_old * len(newfit) * float(np.mean(list(xmem.values())))
    ok("lesson (ii) transformer supplier: netted by the old supplier's infant failures, the same bin", round(net_f / 100) == round(m["F"] / 100), "old rate %.4f, %.0f" % (rate_old, net_f))
    S1, _ = golden.scada_events(P, "oms"); S2, _ = golden.scada_events(P, "final")
    ok("ask A: lockouts read from the outage system and from each device's final state agree", (S1.lockout == S2.lockout).all())
    c = golden.crew_frame(P, "golden").sort_values(["emp", "s"])
    gaps = (c.s - c.groupby("emp").e.shift(1)).dropna()
    ok("ask B: an employee's restoration rows are under 15 minutes apart or 4 hours and more", ((gaps < 15) | (gaps >= 240)).all())
    allc = pd.read_csv(os.path.join(T, "crew_time_overtime_fy2026.csv"))
    ok("ask B: a correction and a rejected entry are in the export", (allc.entry_type == "CORRECTION").any() and (allc.status == "REJECTED").any())
    # ---------------------------------------------------------------- the joint re-trip closure over redraws
    if not fast:
        rates, wins = [], 0
        for k in range(20):
            Pk = dict(world.P, seed=1000 + k)
            Wk = world.run(Pk); Fk = normalise(Wk, 1007 + k); Fk = Fk[~Fk.planned]
            Sk = Wk["S"]
            dd = (Fk.start // 1440).astype(int)
            daily = (Fk.cmi.groupby(dd).sum() / Sk.members.sum()).reindex(range(world.NDAY), fill_value=0.0)
            _, mk = L.med_days(daily)
            fr = L.frost_days(Wk["dm"])
            prk = L.pair(Fk, 10, 60, fr) & ~(Fk.start // 1440).isin(mk) & (Fk.start >= L.G_DAY * 1440) & (Fk.start < L.YE * 1440)
            q = L.qualifying(Fk, 60, fr) & ~L.pair(Fk, 10, 60, fr) & (Fk.end >= L.G_DAY * 1440) & (Fk.start < L.YE * 1440)
            cs = set(Sk.sec[Sk.conn]); us = set(Sk.sec[(Sk.eheat > 0.18) & ~Sk.conn])
            rc = prk[Fk.sec.isin(cs)].sum() / max(q[Fk.sec.isin(cs)].sum(), 1); ru = prk[Fk.sec.isin(us)].sum() / max(q[Fk.sec.isin(us)].sum(), 1)
            rates.append(rc - ru)
            Gk = L.golden_switching(Fk, mk, fr)
            X = Wk["X"]; Rk = L.replay_heat_pumps(Fk, mk, dict(zip(X.xf[X.rebate], X.conn_day[X.rebate])))
            jb = Fk.ci[prk & Fk.sec.isin(cs)].sum()
            wins += (Gk - jb) > (Rk + jb)
        rates = np.array(rates)
        ok("SF10 over 20 redraws: re-trip rate per qualifying restoration equal with and without a connection",
           abs(rates.mean()) < 2 * rates.std(ddof=1) / np.sqrt(len(rates)) + 0.02, "mean difference %.1f points, sd %.1f" % (100 * rates.mean(), 100 * rates.std(ddof=1)))
        ok("SF10 over 20 redraws: booked to the policy, the revision still first", wins >= 18, "%d of 20" % wins)
    # ---------------------------------------------------------------- realism, scrub and input gates
    ev = pd.read_csv(os.path.join(T, "outage_events_fy2022-fy2026.csv"), dtype=str)
    u4 = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
    newids = ev.event_id[~ev.event_id.str.startswith("LG")]
    ok("realism: outage event ids are valid UUID4s (legacy ids before the migration)", newids.map(lambda x: bool(u4.match(x))).all())
    ok("realism: timestamps carry seconds", ev.start_local.str.match(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d$").all())
    heads = []
    for f in os.listdir(T):
        q = os.path.join(T, f)
        if f.endswith(".csv"):
            heads += pd.read_csv(q, nrows=1).columns.tolist()
        elif f.endswith(".xlsx"):
            for sh in pd.read_excel(q, sheet_name=None, nrows=1).values():
                heads += sh.columns.tolist()
        elif f.endswith(".parquet"):
            heads += pd.read_parquet(q).columns.tolist()
    ok("actor: no column names a re-trip, a cold load or a preceding interruption",
       not [h for h in heads if re.search(r"re.?trip|cold|parent|previous|prior|pickup", str(h), re.I)])
    ok("no describing file", not [f for f in os.listdir(T) if re.search(r"readme|dictionar|manifest|codebook|notes|schema", f, re.I)])
    fmts = {f.rsplit(".", 1)[1] for f in os.listdir(T)}
    big = max(sum(1 for _ in open(os.path.join(T, f))) for f in os.listdir(T) if f.endswith(".csv"))
    md = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("input gates: 10 files, 3 formats, a 25,000-row file, 2 distractors",
       len(os.listdir(T)) >= 10 and len(fmts) >= 3 and big >= 25000 and len(md["distractors"]) >= 2, "%d files, %s, %d rows" % (len(os.listdir(T)), sorted(fmts), big))
    import pyarrow.parquet as pq
    cb = pq.read_metadata(os.path.join(T, "transformer_units.parquet")).created_by
    meta = pq.read_metadata(os.path.join(T, "transformer_units.parquet")).metadata or {}
    ok("scrub: the parquet footer names a release writer and carries no arrow schema", cb.startswith("parquet-mr version") and b"ARROW:schema" not in meta, cb)
    bad = []
    for root in (T, os.path.join(TASK, "golden")):
        for f in os.listdir(root):
            q = os.path.join(root, f)
            if f.endswith((".docx", ".xlsx")):
                z = zipfile.ZipFile(q)
                for n in ("docProps/core.xml", "docProps/app.xml"):
                    if n in z.namelist() and re.search(rb"python-docx|openpyxl|XlsxWriter", z.read(n), re.I):
                        bad.append(f)
            if f.endswith(".pdf") and re.search(rb"ReportLab|reportlab", open(q, "rb").read()):
                bad.append(f)
            if f.endswith(".png") and b"matplotlib" in open(q, "rb").read():
                bad.append(f)
    ok("scrub: no toolchain signature in any document, workbook, PDF or image", not bad, ", ".join(bad))
    print("%s: %d failures" % ("PASS" if not FAIL else "FAIL", len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main("--fast" in sys.argv))
