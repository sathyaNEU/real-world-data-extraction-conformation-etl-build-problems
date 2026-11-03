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
VARIANTS = {}


def ok(name, cond, detail=""):
    print("%s  %s  %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAIL.append(name)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def docx_text(path):
    z = zipfile.ZipFile(path)
    return re.sub(r"<[^>]+>", " ", z.read("word/document.xml").decode("utf8"))


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join(p.extract_text() or "" for p in PdfReader(path).pages)


def steps_text():
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    st = sub.split("## 3. Step-by-Step Solution")[1].split("## 4.")[0]
    steps = {int(n): t for n, t in re.findall(r"(?m)^(\d)\. (.+)$", st)}
    ans = sub.split("## 4. Deliverable Answers")[1]
    return steps, ans


def num(s):
    return float(s.replace(",", ""))


def literal_steps():
    """SOLUTION_STEPS executed as written, on the shipped files, with nothing from the generator: each step's own words
    read at face value, and the figure it states asserted."""
    steps, ans = steps_text()
    D = pd.Timestamp("2020-10-01")
    # step 1: unplanned records, major event days by 2.5 beta on fiscal 2021 to 2025 daily SAIDI (legacy sheet in hours)
    dr = pd.read_excel(os.path.join(T, "daily_reliability_fy2021-fy2026.xlsx"), sheet_name=None)
    leg, oms = dr["Legacy OMS to Feb 2023"], dr["OMS daily"]
    sa = pd.concat([pd.Series(leg["SAIDI Hrs"].values * 60, index=pd.to_datetime(leg.Date, format="%m/%d/%Y")),
                    pd.Series(oms.saidi_min.values, index=pd.to_datetime(oms.date))])
    h = sa[(sa.index < "2025-10-01") & (sa > 0)]
    thr = float(np.exp(np.log(h).mean() + 2.5 * np.log(h).std(ddof=1)))
    meds = set(sa.index[sa > thr].normalize())
    said = num(re.search(r"threshold ([\d.]+) minutes", steps[1]).group(1))
    ok("literal step 1: the threshold it states", round(thr, 1) == said, "%.2f against %s" % (thr, said))
    ev = pd.read_csv(os.path.join(T, "outage_events_fy2022-fy2026.csv"), dtype=str, keep_default_na=False)
    cw = pd.read_excel(os.path.join(T, "system_register_2026-09-30.xlsx"), sheet_name="gis_crosswalk")
    ev["sec"] = ev.section_id.map(dict(zip(cw.old_section_id, cw.section_id))).fillna(ev.section_id)
    ev["s"], ev["e"] = pd.to_datetime(ev.start_local), pd.to_datetime(ev.end_local)
    ev["ci"] = ev.customers_interrupted.astype(int)
    kept = ev[(ev.planned == "N") & ~ev.s.dt.normalize().isin(meds)]
    # step 2: records of section devices by section and start, each against the end of the section's previous record
    sx = kept[kept.device_type != "XFMR"].sort_values(["sec", "s"]).copy()
    sx["pe"], sx["ps"] = sx.groupby("sec").e.shift(1), sx.groupby("sec").s.shift(1)
    gap = (sx.s - sx.pe).dt.total_seconds() / 60; dur = (sx.pe - sx.ps).dt.total_seconds() / 60
    hit = (sx.cause_code == "OVLD") & (gap >= 0) & (gap <= 10) & (dur >= 60)
    g2 = sx.ci[hit & (sx.s >= "2025-12-01") & (sx.s < "2026-10-01")].sum()
    staged = int((hit & (sx.s >= "2024-10-01") & (sx.s < "2025-12-01")).sum())
    ok("literal step 2: the total it states", round(g2, -2) == num(re.search(r"total ([\d,]+)", steps[2]).group(1)), "%d" % g2)
    ok("literal step 2: no pair from October 2024 to November 2025, as it states", staged == 0 and "no such pair" in steps[2], "%d" % staged)
    fy = kept[(kept.s >= "2025-10-01") & (kept.s < "2026-10-01")]
    # step 3: overload records on the waived transformers, from each transformer's first waiver connection
    rb = pd.read_excel(os.path.join(T, "heat_pump_rebates_fy2024-fy2026.xlsx"))
    rb = rb[rb.load_study == "waived"]
    first = pd.to_datetime(rb.connected).groupby(rb.service_transformer.str.replace("T-", "T", regex=False)).min()
    x3 = fy[(fy.cause_code == "OVLD") & fy.transformer_id.isin(first.index)]
    g3 = x3.ci[x3.s >= x3.transformer_id.map(first)].sum()
    ok("literal step 3: the figure it states", round(g3, -2) == num(re.search(r": ([\d,]+)\.$", steps[3]).group(1)), "%d" % g3)
    # step 4: the list structures, the 2025 risers, the Brekke units
    al = pd.read_excel(os.path.join(T, "asset_programme_lists_2022-2026.xlsx"), sheet_name=None)
    s26 = set(al["animal_guards"].structure_id[al["animal_guards"].list_year == 2026])
    r25 = set(al["riser_replacements"].riser_structure_id[al["riser_replacements"].list_year == 2025])
    g4a = fy.ci[(fy.cause_code == "ANML") & fy.structure_id.isin(s26) & (fy.s >= "2026-01-01")].sum()
    g4b = fy.ci[(fy.cause_code == "UGTERM") & fy.structure_id.isin(r25) & (fy.s >= "2025-10-01")].sum()
    un = pd.read_parquet(os.path.join(T, "transformer_units.parquet"))
    bk = un[(un.supplier == "Brekke Power Products") & (pd.to_datetime(un.fitted) >= "2026-02-01")]
    fit = pd.to_datetime(bk.fitted).groupby(bk.transformer_id).min()
    x4 = fy[(fy.cause_code == "XFMR") & (fy.device_type == "XFMR") & fy.transformer_id.isin(fit.index)]
    g4c = x4.ci[x4.s > x4.transformer_id.map(fit)].sum()
    st4 = [num(x) for x in re.findall(r": ([\d,]+)", steps[4])]
    ok("literal step 4: the three figures it states", [round(g4a, -2), round(g4b, -2), round(g4c, -2)] == st4, "%d %d %d" % (g4a, g4b, g4c))
    # step 7: the ranking it states
    a7, b7 = [num(x) for x in re.search(r"at ([\d,]+) against ([\d,]+)", steps[7]).groups()]
    costs = sorted([g2, g3, g4a, g4b, g4c], reverse=True)
    ok("literal step 7: the ranking and the two costs it states", costs[0] == g2 and (round(costs[0], -2), round(costs[1], -2)) == (a7, b7))
    # step 5: Ask A as written
    reg = pd.read_excel(os.path.join(T, "system_register_2026-09-30.xlsx"), sheet_name=None)
    sec, rcd = reg["sections"], reg["reclosing_devices"]
    op = pd.read_csv(os.path.join(T, "scada_reclosing_operations_fy2026.csv"))
    op["t"] = pd.to_datetime(op.time_utc.str.replace("Z", ""), utc=True).dt.tz_convert("America/Chicago").dt.tz_localize(None)
    op = op.sort_values(["device_id", "t"]).reset_index(drop=True)
    seqs, cur = [], None
    for d_, t_, o_ in zip(op.device_id, op.t, op.operation):
        if cur is None or d_ != cur[0] or (t_ - cur[1]).total_seconds() > 300:
            cur = [d_, t_, []]; seqs.append(cur)
        cur[2].append(o_)
    sus = ev[(ev.planned == "N") & (ev.device_type != "XFMR")]
    by_dev = sus.groupby("device_id").s.apply(list).to_dict()
    xfer = {r.sec: (r.feeder, r.e) for r in ev[ev.cause_code == "XFER"].itertuples()}
    now = dict(zip(sec.section_id, sec.feeder)); mem = dict(zip(sec.section_id, sec.members)); dist = dict(zip(sec.section_id, sec.district))
    rsec = dict(zip(rcd.device_id, rcd.section_id))
    hits, locked = {}, 0
    for d_, t0, ops in seqs:
        if "TRIP" not in ops:
            continue
        if ops[-1] == "TRIP":
            continue                                   # ended in lockout
        locked += any(abs((s_ - t0).total_seconds()) < 60 for s_ in by_dev.get(d_, []))
        if d_.startswith("CB-"):
            ss = [s_ for s_ in now if (xfer[s_][0] if (s_ in xfer and t0 < xfer[s_][1]) else now[s_]) == d_[3:]]
        else:
            ss = [rsec[d_]]
        for s_ in ss:
            hits.setdefault(s_, []).append(t0)
    tot = {}
    for s_, ts in hits.items():
        last = None
        for t_ in sorted(ts):
            if last is None or (t_ - last).total_seconds() > 300:
                last = t_
                q_ = {10: 1, 11: 1, 12: 1, 1: 2, 2: 2, 3: 2, 4: 3, 5: 3, 6: 3}.get(t_.month, 4)
                tot[(dist[s_], q_)] = tot.get((dist[s_], q_), 0) + mem[s_]
    dm_ = sec.groupby("district").members.sum()
    stated = {}
    for m_ in re.finditer(r"(?m)^\s+- (\w+): Q1 ([\d.]+), Q2 ([\d.]+), Q3 ([\d.]+), Q4 ([\d.]+)", ans):
        for qq in (1, 2, 3, 4):
            stated[(m_.group(1), qq)] = float(m_.group(qq + 1))
    ok("literal step 5: no momentary sequence kept sits at a sustained record's start on the same device", locked == 0, "%d" % locked)
    mine = {k: round(v / dm_[k[0]], 2) for k, v in tot.items()}
    ok("literal step 5: Ask A as written gives every figure in block 4", len(stated) == 16 and all(abs(mine.get(k, 0) - v) < 1e-9 for k, v in stated.items()),
       "%d of 16" % sum(abs(mine.get(k, 0) - v) < 1e-9 for k, v in stated.items()))
    # step 6: Ask B as written
    ct = pd.read_csv(os.path.join(T, "crew_time_overtime_fy2026.csv"), dtype=str)
    ap = ct[(ct.status == "APPROVED") & (ct.pay_code == "CALLOUT")].sort_values("entered_at")
    ap = ap.groupby(["employee_id", "work_order", "start_time"], as_index=False).last()
    ap = ap[ap.order_type == "OUTAGE"]
    os_ = dict(zip(ev.work_order, ev.s))
    rate = {"Line Foreman": 61.42, "Journeyman Lineworker": 55.87, "Apprentice Lineworker (6th step)": 50.28,
            "Apprentice Lineworker (4th step)": 44.69, "Equipment Operator": 46.15}
    hol = set(pd.to_datetime(asks.HOLIDAYS).date)
    jobs = []
    for r in ap.itertuples():
        o = os_[r.work_order]
        s_ = o.normalize() + pd.Timedelta(hours=int(r.start_time[:2]), minutes=int(r.start_time[3:]))
        if s_ < o:
            s_ += pd.Timedelta(days=1)
        dur_ = (int(r.end_time[:2]) * 60 + int(r.end_time[3:]) - int(r.start_time[:2]) * 60 - int(r.start_time[3:])) % 1440
        jobs.append((r.employee_id, s_, s_ + pd.Timedelta(minutes=dur_), rate[r.job_class]))
    H, Pp = {}, {}
    for emp, g_ in pd.DataFrame(jobs, columns=["emp", "s", "e", "rate"]).sort_values(["emp", "s"]).groupby("emp"):
        cs_, ce_ = None, None
        spans = []
        for r in g_.itertuples():
            if cs_ is not None and (r.s - ce_).total_seconds() / 60 < 15:
                ce_ = max(ce_, r.e)
            else:
                if cs_ is not None:
                    spans.append((cs_, ce_, rt_))
                cs_, ce_, rt_ = r.s, r.e, r.rate
        spans.append((cs_, ce_, rt_))
        for cs_, ce_, rt_ in spans:
            k_ = cs_.strftime("%b %Y"); hrs = (ce_ - cs_).total_seconds() / 3600
            H[k_] = H.get(k_, 0) + hrs
            if hrs < 2:
                Pp[k_] = Pp.get(k_, 0) + 2 * rt_ * 1.5
            else:
                t_ = cs_
                while t_ < ce_:
                    nx = min(ce_, t_.normalize() + pd.Timedelta(days=1))
                    Pp[k_] = Pp.get(k_, 0) + (nx - t_).total_seconds() / 3600 * rt_ * (2.0 if t_.date() in hol else 1.5)
                    t_ = nx
    sb = {m_.group(1): (num(m_.group(2)), num(m_.group(3))) for m_ in re.finditer(r"(?m)^\s+- (\w{3} \d{4}): ([\d,]+) hours, USD ([\d,]+)", ans)}
    good = sum(1 for k_, (hh, pp) in sb.items() if round(H.get(k_, 0)) == hh and round(Pp.get(k_, 0)) == pp)
    ok("literal step 6: Ask B as written gives every figure in block 4", len(sb) == 12 and good == 12, "%d of 12 months" % good)
    return g2


def main(fast=False):
    P = golden.load(T)
    F, med = P["F"], P["med"]
    m = golden.main_figures(P)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    order = sorted(m, key=lambda k: -m[k])
    # ---------------------------------------------------------------- the call and its figures
    ok("call: the switching revision costs the most", order[0] == "G", str({k: round(v) for k, v in m.items()}))
    ok("call: at least 1.5 times the runner-up", m["G"] >= 1.5 * m[order[1]], "%.2f" % (m["G"] / m[order[1]]))
    # ---- lesson (ii): every operationalisation a solver who pairs might add prints the graded cost and gap
    v = golden.variants(P)
    vals = np.array(list(v.values()))
    ok("SF14 lesson (ii) every pairing operationalisation prints the cost's bin (window 5 to 30 min, qualifying outage 30 to 120 "
       "min, eleven frost filters on the trip's or the outage's day, overload or every trip, three pairings, three nettings)",
       {round(x / 100) for x in vals} == {round(m["G"] / 100)}, "%d variants, %.0f to %.0f" % (len(vals), vals.min(), vals.max()))
    ok("SF14 lesson (ii) the gap holds its bin under every one of them", {round((x - m["R"]) / 100) for x in vals} == {round((m["G"] - m["R"]) / 100)},
       "%.0f to %.0f" % (vals.min() - m["R"], vals.max() - m["R"]))
    ok("lesson (ii) every variant and its gap at least 7 per cent of a bin from an edge",
       all(edge(x, 100) >= 7 and edge(x - m["R"], 100) >= 7 for x in vals))
    ok("SF5 the staged era carries no pair under any variant, so netting is nil",
       all(abs(v[k] - v[k[:5] + ("not netted",)]) < 1e-6 for k in v))
    VARIANTS.update(v)
    # ---------------------------------------------------------------- forks
    pol = docx_text(os.path.join(T, "board_policy_407_reliability_work_plan.docx"))
    ok("SF1 one record one interruption is filed", "as the outage management system records them" in pol)
    pr = L.pair(F[~F.planned], 10, 60, None, cause="OVLD").reindex(F.index, fill_value=False)
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
    sc_all = L.scope_did(Fa, med, hpi); sc_band = L.scope_did(Fa, med, hpi, bands=[0.18, 0.3, 0.45, 0.6], eheat=ehv)
    ok("SF13 the policy's sections against the rest on every overload trip, flat or in electric-heat bands, keeps the call",
       m["G"] > 1.5 * max(sc_all, sc_band), "%.0f and %.0f against %.0f" % (sc_all, sc_band, m["G"]))
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
    # ---------------------------------------------------------------- SOLUTION_STEPS executed as written
    g_lit = literal_steps()
    ok("literal step 2 equals the golden's switching cost to the interruption", abs(g_lit - m["G"]) < 1e-6, "%.0f against %.0f" % (g_lit, m["G"]))
    # ---- the world's re-trips are the golden's pairs, each clear of every variant's threshold
    sx = F[~F.planned & (F.level == "section")].sort_values(["sec", "start"])
    pe, ps = sx.groupby("sec").end.shift(1), sx.groupby("sec").start.shift(1)
    pp = pr.reindex(sx.index).fillna(False).astype(bool) & (sx.start >= L.G_DAY * 1440) & (sx.start < L.YE * 1440)
    rt = Fw[(Fw.kind == "retrip") & (Fw.start >= L.G_DAY * 1440) & (Fw.start < L.YE * 1440)]
    ok("the golden's pairs are exactly the world's re-trips", int(pp.sum()) == len(rt) and abs(rt.ci.sum() - m["G"]) < 1e-6,
       "%d pairs, %d re-trips, %d interruptions" % (pp.sum(), len(rt), rt.ci.sum()))
    durs = (pe - ps)[pp]
    td = P["daymean"].reindex((sx.start[pp] // 1440).astype(int)).values
    od = P["daymean"].reindex((ps[pp] // 1440).astype(int)).values
    ok("margins: every paired re-trip follows an outage of two and a quarter hours or more (the longest variant asks two)",
       durs.min() >= 135, "shortest %.0f min" % durs.min())
    ok("margins: every paired re-trip's own day and its outage's start day average -6 C or colder on local dates (the "
       "coldest variant asks -5)", max(td.max(), od.max()) <= -6.0, "warmest %.2f C" % max(td.max(), od.max()))
    ok("margins: no paired re-trip within a day of 1 December 2025", (np.abs(sx.start[pp] - L.G_DAY * 1440) >= 1440).all())
    # ---- ask B dated two ways: by the clock rolling past midnight (the golden) and by the outage's own date
    ap = allc[(allc.status == "APPROVED") & (allc.pay_code == "CALLOUT")].sort_values("entered_at")
    ap = ap.groupby(["employee_id", "work_order", "start_time"], as_index=False).last()
    ap = ap[ap.order_type == "OUTAGE"]
    o0 = ap.work_order.map(dict(zip(F.wo, F.start)))
    clk = ap.start_time.str[:2].astype(int) * 60 + ap.start_time.str[3:5].astype(int)
    base = (o0 // 1440) * 1440 + clk
    mon = lambda d_: pd.DatetimeIndex(golden.D0 + pd.to_timedelta(np.asarray(d_, float), "D")).month
    rolled = (base < o0).sum()
    ok("ask B: a job past midnight is dated to the same month under either reading", (mon(np.where(base < o0, base + 1440, base) // 1440)
       .values == mon(base // 1440).values).all() and rolled > 0, "%d jobs past midnight, none across a month" % rolled)
    ok("ask B: no work order carries two order types", (allc.groupby("work_order").order_type.nunique() == 1).all())
    agr = pdf_text(os.path.join(T, "labor_agreement_2024-2027_extract.pdf"))
    ok("ask B: the agreement reads back (positive control) and files that a correction replaces the entry and a rejected "
       "entry is not paid", "time and one-half" in agr and "replaces the earlier entry" in agr and "rejects is not paid" in agr)
    gw = pd.read_excel(os.path.join(TASK, "golden", "interruption_costing_fy2026.xlsx"), sheet_name=None)
    ok("ask A: the golden's quarters are labelled fiscal", any(str(c).startswith("Fiscal Q1") for sh in gw.values() for c in sh.columns))
    # ---- realism fixes
    mem_v = reg["sections"].members
    ok("realism: no section on a bound (the largest and smallest sections are single natural counts)",
       (mem_v == mem_v.max()).sum() == 1 and (mem_v == mem_v.min()).sum() == 1 and mem_v.max() % 50 and not mem_v.isin([35, 1000]).any(),
       "largest %d, smallest %d" % (mem_v.max(), mem_v.min()))
    xs = reg["transformers"].groupby("section_id").members_served.sum()
    ok("realism: each section's transformers serve exactly its members", (xs.reindex(reg["sections"].section_id).values == mem_v.values).all()
       and xs.sum() == mem_v.sum(), "%d against %d" % (xs.sum(), mem_v.sum()))
    dsh = pd.read_excel(os.path.join(T, "daily_reliability_fy2021-fy2026.xlsx"), sheet_name=None)
    cs_ = dsh["OMS daily"].customers_served; lg_ = dsh["Legacy OMS to Feb 2023"]["Cust Served"]
    yrs = (len(lg_) + len(cs_)) / 365.25
    grow = (cs_.iloc[-1] / lg_.iloc[0]) ** (1 / yrs) - 1
    ok("realism: members served follow a path that ends at the register's count (daily in the OMS, monthly in the legacy sheet)",
       cs_.iloc[-1] == mem_v.sum() and cs_.nunique() > 200 and 12 <= lg_.nunique() <= 30 and 0.005 <= grow <= 0.015,
       "%d to %d, %.2f per cent a year" % (lg_.iloc[0], cs_.iloc[-1], 100 * grow))
    stp = pd.read_csv(os.path.join(T, "restoration_steps_fy2025-fy2026.csv"))
    last = stp.sort_values("step").groupby("switching_order").last()
    evk = pd.read_csv(os.path.join(T, "outage_events_fy2022-fy2026.csv"), dtype=str)
    keys = evk.groupby(["device_id", "end_local"]).size()
    j = keys.reindex(list(zip(last.device_id, last.restored_local)))
    ok("realism: the switching log keys its own orders and joins the outage extract by device and restoration time, one record each",
       "event_id" not in stp.columns and len(last) > 1000 and j.notna().all() and (j == 1).all(), "%d orders" % len(last))
    sq = np.sort(last.index.str[-5:].astype(int).values[last.index.str[2:4] == "26"])
    ok("realism: switching order numbers are not a constant-step sequence", len(set(np.diff(sq))) > 3)
    seen_cols, steady = 0, []
    for f in sorted(os.listdir(T)):
        q = os.path.join(T, f)
        frames = ([pd.read_csv(q, dtype=str)] if f.endswith(".csv") else list(pd.read_excel(q, sheet_name=None, dtype=str).values())
                  if f.endswith(".xlsx") else [pd.read_parquet(q).astype(str)] if f.endswith(".parquet") else [])
        for df in frames:
            for c in df.columns:
                if re.search(r"(_id|serial|meter|account|work_order|switching_order|protective_device|service_transformer)$", str(c)):
                    nums = pd.to_numeric(df[c].dropna().astype(str).str.extract(r"(\d+)$")[0], errors="coerce").dropna().unique()
                    if len(nums) > 20:
                        seen_cols += 1
                        if len(set(np.diff(np.sort(nums)))) <= 2:
                            steady.append("%s %s" % (f, c))
    ok("realism: no id column advances in a constant step (every id-like column differenced)", seen_cols >= 12 and not steady,
       "%d columns read; %s" % (seen_cols, ", ".join(steady) or "none steady"))
    meds = sorted(str((golden.D0 + pd.Timedelta(days=int(d_))).date()) for d_ in med)
    ok("major event days unchanged from the round-1 cut (fiscal 2026: 10 April 2026 only)",
       meds == ["2021-06-19", "2021-06-30", "2023-04-14", "2023-05-19", "2024-06-17", "2026-04-10"], ", ".join(meds))
    # ---------------------------------------------------------------- the joint re-trip closure over redraws
    if not fast:
        rates, wins, leads, rungs = [], 0, [], {"category": 0, "scope": 0, "banded": 0}
        for k in range(20):
            Pk = dict(world.P, seed=1000 + k, rt_seed=5000 + k)
            Wk = world.run(Pk); Fk = normalise(Wk, 1007 + k); Fk = Fk[~Fk.planned]
            Sk = Wk["S"]
            dd = (Fk.start // 1440).astype(int)
            daily = (Fk.cmi.groupby(dd).sum() / Sk.members.sum()).reindex(range(world.NDAY), fill_value=0.0)
            _, mk = L.med_days(daily)
            fr = L.frost_days(Wk["dm"], -7.0)
            pk = L.pair(Fk, 10, 60, None, cause="OVLD")
            prk = pk & ~(Fk.start // 1440).isin(mk) & (Fk.start >= L.G_DAY * 1440) & (Fk.start < L.YE * 1440)
            q = L.qualifying(Fk, 135, fr) & ~pk & (Fk.end >= L.G_DAY * 1440) & (Fk.start < L.YE * 1440)
            cs = set(Sk.sec[Sk.conn]); us = set(Sk.sec[(Sk.eheat > 0.18) & ~Sk.conn])
            rc = prk[Fk.sec.isin(cs)].sum() / max(q[Fk.sec.isin(cs)].sum(), 1); ru = prk[Fk.sec.isin(us)].sum() / max(q[Fk.sec.isin(us)].sum(), 1)
            rates.append(rc - ru)
            Gk = L.golden_switching(Fk, mk)
            X = Wk["X"]; Rk = L.replay_heat_pumps(Fk, mk, dict(zip(X.xf[X.rebate], X.conn_day[X.rebate])))
            Ek = L.replay_guards(Fk, mk, set(Wk["G"].site[Wk["G"].list_year == 2026]))
            Dk = L.replay_risers(Fk, mk, set(Wk["Rr"].riser[Wk["Rr"].list_year == 2025]))
            Fu = L.replay_supplier(Fk, mk, {int(a): int(b) for a, b in zip(Wk["NU"].xf, Wk["NU"].fit_day) if b >= L.F_DAY})
            leads.append(Gk / max(Rk, Ek, Dk, Fu))
            ovk = L.category_rise(Fk, mk, "OVLD")
            sck = L.scope_did(Fk, mk, cs)
            bdk = L.scope_did(Fk, mk, cs, bands=[0.18, 0.3, 0.45, 0.6], eheat=(Sk.eheat_members / Sk.members).values)
            for nm, val in (("category", ovk), ("scope", sck), ("banded", bdk)):
                rungs[nm] += max({"R": val, "E": Ek, "D": Dk, "F": Fu}.items(), key=lambda kv: kv[1])[0] == "R"
            jb = Fk.ci[prk & Fk.sec.isin(cs)].sum()
            wins += (Gk - jb) > (Rk + jb)
        rates = np.array(rates); leads = np.array(leads)
        ok("SF10 over 20 redraws: re-trip rate per qualifying restoration equal with and without a connection",
           abs(rates.mean()) < 2 * rates.std(ddof=1) / np.sqrt(len(rates)) + 0.02, "mean difference %.1f points, sd %.1f" % (100 * rates.mean(), 100 * rates.std(ddof=1)))
        # re-measured on the long-outage, hard-frost mechanism (round-2 fix pass): 17 of these 20 and 53 of 60 on a wider run;
        # the shipped draw holds it two to one and the fork is closed by the rebate terms' eligibility sentence (SF10)
        ok("SF10 over 20 redraws: booked to the policy, the revision still first in at least four worlds of five", wins >= 16,
           "%d of 20" % wins)
        ok("screen 1 over 20 redraws: the switching revision at least 1.5 times every rival's replay", (leads >= 1.5).sum() >= 19,
           "%d of 20, worst %.2f" % ((leads >= 1.5).sum(), leads.min()))
        ok("screen 3 over 20 redraws: the overload category's rise files the heat pump policy", rungs["category"] >= 19,
           "category %d, scope %d, banded %d of 20 name the policy (the switching revision costs nil on each)" % (rungs["category"], rungs["scope"], rungs["banded"]))
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
