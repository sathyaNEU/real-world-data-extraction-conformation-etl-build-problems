"""task127 generator: the assertion regime, run on the files as written.

Every assertion goes through ok(); the count is recorded and printed. A failure stops the build.
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

import askcalc as K
import ladder as L
import params as P

F = P.F
N = {"n": 0}
REC = {}


def ok(cond, msg):
    N["n"] += 1
    if not cond:
        raise AssertionError(f"[{N['n']}] {msg}")


def near(a, b, tol=1e-6):
    return abs(a - b) <= tol


def dist_edge(x, step=10.0):
    r = (x - step / 2) % step
    return min(r, step - r)


# ------------------------------------------------------------------ input gates and hygiene

def gates(tgt, root):
    files = sorted(os.listdir(tgt))
    ok(len(files) >= 10, f"file count {len(files)}")
    fm = sorted({Path(f).suffix for f in files})
    ok(len(fm) >= 3, f"formats {fm}")
    rows = sum(1 for _ in open(tgt / F["orders"], encoding="utf-8")) - 1
    ok(rows >= 25000, f"largest file rows {rows}")
    ok(set(files) == set(F.values()), "shipped set equals the declared asset list")
    ok(len(P.DISTRACTORS) >= 2 and all(d in files for d in P.DISTRACTORS), "two distractors shipped")
    for f in files:
        ok("distractor" not in f.lower(), f"file name {f}")
        blob = (tgt / f).read_bytes()
        if f.endswith((".docx", ".xlsx")):
            with zipfile.ZipFile(tgt / f) as z:
                blob = b"".join(z.read(n) for n in z.namelist())
        ok(b"distractor" not in blob.lower(), f"word distractor in {f}")
    ok(1 <= len(P.DELIVERABLES) <= 3, "one to three deliverables")
    REC.update(files=len(files), formats=fm, spine_rows=rows)


def registers(tgt):
    about = (tgt / F["about"]).read_text()
    listed = {ln.split(" | ")[0] for ln in about.splitlines() if " | " in ln and not ln.startswith("file |")}
    ok(listed == set(F.values()) - {F["about"]}, "provenance lists every other file (H9)")
    fields = (tgt / F["fields"]).read_text()
    data = [v for k, v in F.items() if v.endswith((".csv", ".xlsx", ".json")) or k == "tables"]
    ok(all(v in fields for v in data), "field definitions cover every data file by name")


def vocabulary(tgt):
    banned = ["capacity of the crew", "crew capacity", "backlog", "queue", "spare", "keep up", "catch up",
              "bottleneck", "overtime", "workload", "behind on"]
    texts = doc_texts(tgt)
    for f, t in texts.items():
        low = t.lower()
        for w in banned:
            ok(w not in low, f"banned word '{w}' in {f}")
    single = {"5 kW": F["terms"], "invoice of record": F["finance"], "Central time": F["finance"],
              "to the nearest ten": F["rules"], "is one install": F["prices"], "in two legs": F["terms"],
              "Table H1": F["rules"], "lapse": F["rules"]}
    for phrase, home in single.items():
        hits = [f for f, t in texts.items() if phrase.lower() in t.lower()]
        ok(hits == [home], f"'{phrase}' stated once, in {home}: {hits}")
    paper = texts[F["paper"]]
    quotes = re.findall(r'"([^"]+)"', paper)
    ok(len(quotes) >= 4 and all(not re.search(r"\d", re.sub(r"\b20\d\d\b", "", q).replace("30 November", "")) for q in quotes),
       "voices quote no figure")
    REC["texts"] = len(texts)


def doc_texts(tgt):
    from pypdf import PdfReader
    from docx import Document
    out = {}
    for f in sorted(os.listdir(tgt)):
        p = tgt / f
        if f.endswith(".pdf"):
            out[f] = "\n".join(pg.extract_text() for pg in PdfReader(str(p)).pages).replace("\n", " ")
        elif f.endswith(".docx"):
            out[f] = "\n".join(x.text for x in Document(str(p)).paragraphs)
        elif f.endswith(".txt"):
            out[f] = p.read_text()
    return out


def hygiene(tgt, sc):
    ok(sc[0] == 0 and sc[1] == 0, f"scrub repair and audit exit codes {sc[:2]}")
    for f in os.listdir(tgt):
        if f.endswith((".docx", ".xlsx")):
            with zipfile.ZipFile(tgt / f) as z:
                meta = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/")).decode("utf-8", "ignore")
            ok(not any(s in meta for s in ("python-docx", "openpyxl", "xlsxwriter", "XlsxWriter")), f"writer name in {f}")
            yrs = set(re.findall(r"(\d{4})-\d\d-\d\dT", meta))
            ok(yrs <= {"2025", "2026"}, f"container dates in {f}: {yrs}")
        if f.endswith(".pdf"):
            b = (tgt / f).read_bytes()
            ok(b"ReportLab" not in b and b"reportlab" not in b, f"writer name in {f}")
    for f in (F["orders"], F["invoices"], F["ledger"], F["wx"]):
        txt = (tgt / f).read_text()
        ds = re.findall(r"20\d\d-\d\d-\d\d", txt)
        ok(max(ds) <= "2026-12-11", f"dates after the pull in {f}: {max(ds)}")


# ------------------------------------------------------------------ calibration and certification

def calibration(D):
    sys_bt = L.backtest(D, ("sys",))
    pool_bt = L.backtest(D, ())
    inc_bt = L.backtest(D, ("income_band",))
    ok(all(abs(v[2]) <= 0.04 for v in sys_bt.values()) and len(sys_bt) == 6, "system rates reproduce 6 of 6")
    ok(all(abs(v[2]) >= 0.15 for v in pool_bt.values()), "pooled rate misses every pilot neighbourhood by 15%+")
    ok(sum(abs(v[2]) >= 0.12 for v in inc_bt.values()) >= 2, "income-band rates miss two or more by 12%+")
    r_sys = L.rates(D, ("sys",))
    r_fine = L.rates(D, ("sys", "income_band"))
    ok(all(near(v, r_sys[(k[0],)]) for k, v in r_fine.items()), "system x income rates equal system rates (C1)")
    r_coop = L.rates(D, ("coop", "sys"))
    ok(all(near(v, r_sys[(k[1],)]) for k, v in r_coop.items()), "each pilot neighbourhood's own system rates equal "
       "the pooled system rates (C1)")
    REC["rates"] = {k[0]: round(v * 100, 4) for k, v in r_sys.items()}
    REC["pooled_rate"] = round(L.rates(D, ())[()] * 100, 4)
    REC["backtest_pooled_min_miss"] = round(min(abs(v[2]) for v in pool_bt.values()) * 100, 1)
    REC["backtest_income_min_miss"] = round(min(abs(v[2]) for v in inc_bt.values()) * 100, 1)
    REC["swept_rules"] = 4


def certification(D):
    sv, t = D["sv"], D["tabs"]
    name = P.COOP_NAME
    fuel = sv.heating_system.map(lambda x: P.FUEL_SURVEY[x][1])
    h1 = t["H1"].set_index(t["H1"].columns[0])
    for c in P.COOPS:
        for col in h1.columns:
            ok(int(h1.loc[name[c], col]) == int(sv[(sv.coop == c) & (fuel == col)].weight.sum()),
               f"H1 {c} {col} reproduces") if col in ("electricity", "bottled, tank or LP gas") else None
    h3 = t["H3"]
    per = {}
    unweighted = []
    for c in P.COOPS:
        g = sv[sv.coop == c]
        hh = g.weight.sum()
        ms = []
        for ten in P.TENURE:
            row = h3[(h3.iloc[:, 0] == name[c]) & (h3.iloc[:, 1] == ten)]
            for st in P.STRUCT:
                act = int(row[st].iloc[0])
                ok(act == int(g[(g.tenure == ten) & (g.structure == st)].weight.sum()), f"H3 {c} {ten} {st}")
                prod = hh * (g[g.tenure == ten].weight.sum() / hh) * (g[g.structure == st].weight.sum() / hh)
                if act:
                    ms.append(abs(prod / act - 1))
        per[c] = max(ms)
        unweighted.append(abs((g.structure == P.STRUCT[0]).mean() / (g[g.structure == P.STRUCT[0]].weight.sum() / hh) - 1))
    ok(min(per.values()) >= 0.10, f"one-way product misses a tenure x structure cell by 10%+ in every co-op {per}")
    ratio = L.product_counts(D) / L.joint_counts(D)
    ok((abs(ratio - 1) >= 0.10).all(), f"product of one-way shares misses every co-op's joint count by 10%+ {dict(ratio)}")
    REC["product_cell_miss_max"] = {c: round(v * 100, 1) for c, v in per.items()}
    REC["product_over_joint"] = {c: round(float(v), 3) for c, v in ratio.items()}
    REC["unweighted_share_miss_max"] = round(max(unweighted) * 100, 1)
    ok(max(unweighted) >= 0.05, "unweighted shares miss the weighted tables")
    ok(sv.weight.sum() % 100 != 0, "survey household total is not a round figure")


# ------------------------------------------------------------------ the ladder

def ranking(vals):
    o = sorted(vals, key=lambda k: -vals[k])
    return o, vals[o[0]] / vals[o[1]]


def ladder(D):
    pooled = L.rates(D, ())[()]
    r0 = dict(L.product_counts(D) * pooled)
    r1 = dict(L.joint_counts(D) * pooled)
    r2 = dict(L.nbhd_buyers(D).groupby(level=0).sum())
    r3 = L.placeable(D)
    G = L.golden(D)
    r4 = G["sets"]
    want = {0: "VA", 1: "UP", 2: "NS", 3: "LA", 4: "RB"}
    rungs = {0: r0, 1: r1, 2: r2, 3: r3, 4: r4}
    pos = {}
    for k, v in rungs.items():
        o, m = ranking(v if k < 4 else G["slots"])
        ok(o[0] == want[k], f"rung {k} leader {o[0]} (want {want[k]})")
        ok(m >= 1.15, f"rung {k} leader margin {m:.3f}")
        pos[k] = (o.index("RB") + 1, round(m, 3))
    ok(pos[0][0] in (4, 5), f"answer ranks {pos[0][0]} on the natural pipeline")
    ok(all(pos[k][0] != 1 for k in (0, 1, 2, 3)), "answer leads no intermediate rung")
    ok(sum(pos[k][0] == 2 for k in (0, 1, 2, 3)) <= 1, "answer second on at most one rung")
    ok(r3["LA"] / r3["RB"] >= 1.20, f"rung 3 margin over the answer {r3['LA'] / r3['RB']:.3f}")
    ok(sum(r0.values()) > P.SLOTS_TOTAL and sum(r1.values()) > P.SLOTS_TOTAL and sum(r2.values()) > P.SLOTS_TOTAL,
       "rungs 0 to 2 fire the sharing branch")
    for k in (0, 1, 2):
        s = sum(rungs[k].values())
        rem = sorted(((v / s * 180) % 1) for v in rungs[k].values())
        ok(min(b - a for a, b in zip(rem, rem[1:])) > 1e-6, f"no largest-remainder tie at rung {k}")
    r3s = L.allocate(r3)
    ok(sum(r3s.values()) == 1480 and r3s["LA"] == 420, f"rung 3 split {r3s}")
    ok(G["slots"] == {"NS": 160, "VA": 180, "LA": 240, "UP": 170, "RB": 340, "PW": 80}, f"golden split {G['slots']}")
    ok(G["placed"] == 1170 and G["unallocated"] == 630 and G["leader"] == "RB" and G["lead_by"] == 100,
       "placed 1,170, unallocated 630, Riverbend ahead by 100")
    ok(sum(G["sets"].values()) < P.SLOTS_TOTAL, "sharing branch does not fire at rung 4")
    for c, v in G["sets"].items():
        ok(dist_edge(v) >= 1.5, f"{c} sets {v:.2f} at least 1.5 from a bin edge")
        ok(abs(v - round(v / 10) * 10) >= 0.3, f"{c} sets {v:.2f} not on the round value")
    carried = r3["LA"] / r3["RB"]
    edge = (r3["RB"] / G["sets"]["RB"]) ** -1 / (G["sets"]["LA"] / r3["LA"])
    ok(edge >= 1.2 * carried, f"discriminator dominance {edge:.3f} against {1.2 * carried:.3f}")
    REC["rungs"] = {k: {c: round(float(v[c]), 2) for c in P.COOPS} for k, v in rungs.items()}
    REC["rung_splits"] = {k: L.allocate(rungs[k]) for k in (0, 1, 2, 3)}
    REC["position"] = pos
    REC["golden"] = {k: G[k] for k in ("slots", "placed", "unallocated", "leader", "lead_by")}
    REC["spare"] = {c: round(v, 4) for c, v in G["spare"].items()}
    REC["dominance"] = [round(edge, 3), round(carried, 3)]
    return G, rungs


def crews(D, G):
    out = {}
    for c in P.FOUR_DAY:
        R = L.crew_record(D, c)
        s26, _ = L.standing_level(R, "2026-01-01", "2026-12-10")
        bdays = set(R["plateau"])
        s25, _ = L.standing_level(R, "2025-01-01", "2025-12-31", exclude=lambda x: x in bdays)
        s52, _ = L.standing_level(R, (P.AS_OF - timedelta(days=364)).isoformat(), "2026-12-10")
        sp, ceil, _ = L.spare_of(D, c)
        ok(max(s26, s25, s52) - min(s26, s25, s52) <= 0.05, f"{c} standing level stationary {s26:.3f} {s25:.3f} {s52:.3f}")
        ok(len(R["plateau"]) >= 40, f"{c} ceiling held {len(R['plateau'])} working days")
        tot = R["total"]
        ok(max(abs(tot.get(x, 0) - ceil) for x in R["plateau"]) <= 1.0, f"{c} completions flat at the ceiling")
        fo = D["fo"]
        d = fo[(fo.coop == c) & (fo.completed_date != "")]
        wd = pd.to_datetime(d.completed_date).dt.weekday
        ok((wd >= 4).sum() == 0, f"{c} crew completes nothing on a Friday or weekend")
        ok((d.completed_date == "2026-07-02").sum() > 0, f"{c} crew worked Thursday 2 July 2026")
        batch = (d.order_type == "MXCH") & (d.requested_date == L.BATCH_DAY)
        std = d[(d.order_type != "HPRM") & ~batch]
        lag = (pd.to_datetime(std.completed_date) - pd.to_datetime(std.requested_date)).dt.days
        inp = std.completed_date.isin(bdays)
        ok(abs(lag[inp].mean() - lag[~inp].mean()) <= 0.4, f"{c} standing lag unchanged through the ceiling weeks")
        hp = d[d.order_type == "HPRM"]
        wk = hp.groupby(pd.to_datetime(hp.requested_date).dt.to_period("W-SUN")).size()
        ok(wk.max() <= 0.6 * 4 * sp, f"{c} pilot never loaded the crew: {wk.max()} a week against {4 * sp:.2f}")
        wd27 = L.crew_days_2027()
        ok(sp * len(wd27) >= G["placeable"][c] * 1.1, f"{c} annual check passes ({sp * len(wd27):.0f})")
        arr = L.forward_arrivals(D)
        ok(G["sets"][c] < G["placeable"][c] - 100, f"{c} meters left unset on 31 December 2027")
        closed = G["placeable"][c] * P.SPRING_SHARE + sp * len([x for x in wd27 if x >= date(2027, 9, 27)])
        ok(near(closed, G["sets"][c], 1e-6), f"{c} queue never empties after 27 September ({closed:.3f})")
        out[c] = dict(standing=[round(s26, 3), round(s25, 3), round(s52, 3)], ceiling=round(ceil, 3),
                      spare=round(sp, 4), plateau_days=len(R["plateau"]), pilot_peak_week=int(wk.max()))
    # spring orders are all set by the end of August at both binding crews
    for c in P.FOUR_DAY:
        arr = {k: v for k, v in L.forward_arrivals(D).items() if k < date(2027, 9, 1)}
        done, left = L.fluid_sets(G["placeable"][c], G["spare"][c], arr, L.crew_days_2027())
        ok(left < 1e-9, f"{c} spring orders cleared by 31 August")
    # the four five-day crews: demonstrated weeks against standing plus the programme's peak week
    arr = pd.Series(L.forward_arrivals(D))
    arr.index = pd.to_datetime(arr.index)
    peak_share = arr.groupby(arr.index.to_period("W-SUN")).sum().max()
    for c in P.COOPS:
        if c in P.FOUR_DAY:
            continue
        R = L.crew_record(D, c)
        wk = pd.Series(R["total"])
        wk.index = pd.to_datetime(wk.index)
        wk = wk.groupby(wk.index.to_period("W-SUN")).sum()
        top3 = wk.rolling(3).mean().max()
        std = np.median(wk.values)
        need = std + peak_share * G["placeable"][c]
        ok(top3 >= 1.15 * need, f"{c} crew's demonstrated weeks {top3:.1f} against {need:.1f}")
        out[c] = dict(median_week=float(std), top_three_week_mean=round(float(top3), 1), need=round(float(need), 1))
    hp = D["fo"][D["fo"].order_type == "HPRM"]
    lag = [np.busday_count(a, b) for a, b in zip(hp.requested_date, hp.completed_date)]
    ok(len(hp) == 412 and max(lag) <= 15, f"every pilot meter set inside 15 working days ({max(lag)})")
    ok(hp.completed_date.max() < P.AS_OF.isoformat(), "last pilot meter set before the as-of date")
    REC["crews"] = out


# ------------------------------------------------------------------ partial readings, variants and the grid

def partials(D, G):
    plc = G["placeable"]
    sp = G["spare"]
    gold = G["slots"]

    def summary(sets):
        sl = L.slots(sets) if sum(sets.values()) <= P.SLOTS_TOTAL else L.largest_remainder(sets)
        return sl, max(sl, key=sl.get), sum(sl.values())
    rows = {}
    # (a) the year-end lapse on the pilot's lag: every placeable meter set
    rows["a"] = summary(dict(plc))
    # (b) annual spare against placeable meters: passes everywhere, so the same split
    wd27 = L.crew_days_2027()
    rows["b"] = summary({c: min(plc[c], sp[c] * len(wd27)) if c in sp else plc[c] for c in P.COOPS})
    # (c) the queue on rung 2's buyers, no feeder cap
    r2 = dict(L.nbhd_buyers(D).groupby(level=0).sum())
    rows["c"] = summary(L.queue_sets(D, r2, sp))
    # (d) the queue on an even year-round arrival
    even = {date(2027, 1, 1) + timedelta(days=i): 1 / 365 for i in range(365)}
    dsets = {c: (L.fluid_sets(plc[c], sp[c], even, wd27)[0] if c in sp else plc[c]) for c in P.COOPS}
    rows["d"] = summary(dsets)
    # (e) the queue against the full ceiling, standing work ignored
    ceil = {c: L.spare_of(D, c)[1] for c in sp}
    rows["e"] = summary(L.queue_sets(D, plc, ceil))
    # (f) one queue across standing and programme orders, in request order
    fsets = dict(plc)
    for c in sp:
        _, cl, st = L.spare_of(D, c)
        fsets[c] = L.fcfs_sets(D, plc, c, cl, st)
    rows["f"] = summary(fsets)
    # (g) standing work forecast from averages that carry the July 2025 batch as run-rate
    gsp = {}
    for c in sp:
        R = L.crew_record(D, c)
        days = [x for x in R["days"]]
        nonhp = R["standing"].reindex(days, fill_value=0).sum() + R["batch_n"]
        gsp[c] = R["ceiling"] - nonhp / len(days)
    rows["g"] = summary(L.queue_sets(D, plc, gsp))
    # (h) convention variants: inside every bin
    for name, kw in {"h_thanksgiving_ignored": dict(thanksgiving=False), "h_weekday_mapping": dict(mapping="weekday"),
                     "h_weekly_capacity": dict(weekly=True), "h_per_coop_calendar": dict(per_coop=True)}.items():
        v = L.queue_sets(D, plc, sp, **kw)
        ok(L.slots(v) == gold, f"variant {name} gives the golden split ({ {c: round(v[c], 2) for c in sp} })")
        rows[name] = ({c: round(v[c], 2) for c in sp},)
    want = {"a": ("LA", 1480), "b": ("LA", 1480), "c": ("NS", 1800), "d": ("LA", 1480), "e": ("LA", 1480),
            "f": ("LA", None), "g": ("RB", None)}
    for k, (lead, placed) in want.items():
        sl, ld, pl = rows[k]
        ok(ld == lead, f"partial ({k}) leader {ld}")
        ok(placed is None or pl == placed, f"partial ({k}) placed {pl}")
        ok(sl != gold, f"partial ({k}) misses the golden split")
    ok(rows["f"][2] >= 1350, f"partial (f) placed {rows['f'][2]}")
    ok(rows["g"][2] < G["placed"] and rows["g"][0]["LA"] < gold["LA"] and rows["g"][0]["UP"] < gold["UP"],
       f"partial (g) lands below the answer on both binding co-ops ({rows['g'][2]})")
    REC["partials"] = {k: (v[0], v[1], v[2]) if len(v) == 3 else v[0] for k, v in rows.items()}


def grid(D, G):
    """shares (product, joint) x rate (pooled, system) x feeder cap (none, co-op total, feeder) x queue."""
    pooled = L.rates(D, ())[()]
    nb_sys = L.nbhd_buyers(D, "system")
    nb_pool = L.nbhd_buyers(D, "pooled")
    prod_ratio = (L.product_counts(D) / L.joint_counts(D))
    cells = {}
    for shares in ("product", "joint"):
        for rate in ("pooled", "system"):
            b = nb_sys if rate == "system" else nb_pool
            if shares == "product":
                b = b * b.index.get_level_values(0).map(prod_ratio).to_numpy()
            for cap in ("none", "coop", "feeder"):
                plc = L.placeable(D, b, cap)
                for q in (False, True):
                    sets = L.queue_sets(D, plc, G["spare"]) if q else dict(plc)
                    sl = L.allocate(sets)
                    cells[(shares, rate, cap, q)] = (sl, max(sl, key=sl.get), sum(sl.values()))
    gold_cell = ("joint", "system", "feeder", True)
    for k, (sl, lead, placed) in cells.items():
        if k == gold_cell:
            ok(sl == G["slots"], "the golden cell reproduces the answer")
        else:
            ok(sl != G["slots"], f"grid cell {k} misses the answer")
    ok(len(cells) == 24, "24 grid cells")
    REC["grid"] = {"|".join(map(str, k)): [v[1], v[2]] for k, v in cells.items()}


# ------------------------------------------------------------------ determinism closures

def closures(D, G, tgt):
    sv, pl, fo = D["sv"], D["pl"], D["fo"]
    # keys and identities
    ok(fo.order_id.is_unique and sv.case_id.is_unique and pl.rebate_id.is_unique and pl.premises_id.is_unique,
       "no duplicate keys on the main path")
    ok(not fo.duplicated().any(), "no duplicate field-order rows")
    nb_sv = set(sv.neighbourhood)
    ok(nb_sv == set(D["fmap"].neighbourhood) and set(pl.neighbourhood) <= nb_sv, "neighbourhood keys agree")
    ok(set(D["fmap"].feeder) == set(D["host"].feeder) and D["host"].feeder.is_unique, "feeder keys agree")
    ok((D["host"].hosting_capacity_remaining_kw % P.KW_PER_HP == 0).all(), "every filed headroom a multiple of 5 kW")
    ok(D["fmap"].groupby("neighbourhood").feeder.nunique().max() == 1, "each neighbourhood on exactly one feeder")
    # pilot calendar
    d = pd.to_datetime(pl.install_date)
    ok(pd.to_datetime(pl.purchase_date).dt.year.eq(2026).all() and d.dt.year.eq(2026).all()
       and pd.to_datetime(pl.meter_set_date).dt.year.eq(2026).all(), "every pilot date inside 2026")
    for nb, g in pl.groupby("neighbourhood"):
        dd = pd.to_datetime(g.install_date)
        spring = (dd < "2026-07-01").sum()
        ok(spring * 4 == len(g), f"{nb} spring share exactly a quarter")
        ok(dd[dd >= "2026-07-01"].min() == pd.Timestamp("2026-09-25"), f"{nb} first autumn install 25 September")
    ok(set(zip(fo[fo.order_type == "HPRM"].premises_id, fo[fo.order_type == "HPRM"].requested_date))
       == set(zip(pl.premises_id, pd.to_datetime(pl.install_date).dt.strftime("%Y-%m-%d"))),
       "each heat-pump rate meter order raised on its install date")
    hp = fo[fo.order_type == "HPRM"].set_index("premises_id").completed_date
    ok((pd.to_datetime(pl.meter_set_date).dt.strftime("%Y-%m-%d").to_numpy() == hp.reindex(pl.premises_id).to_numpy()).all(),
       "pilot meter-set dates match the field orders")
    # row order (axis 14)
    for s in range(6):
        D2 = dict(D, fo=fo.sample(frac=1, random_state=s).reset_index(drop=True))
        ok(L.golden(D2)["slots"] == G["slots"], f"row-order shuffle {s}")
    # clean-data tests: census survey, one year of field orders at a time, distractors deleted
    cells = sv.groupby(["coop", "neighbourhood", "heating_system", "tenure", "structure", "income_band"],
                       as_index=False).weight.sum()
    cells["case_id"] = [f"C{i}" for i in range(len(cells))]
    ok(L.golden(dict(D, sv=cells))["slots"] == G["slots"], "census of the weighted cells gives the same split")
    for yr in ("2025", "2026"):
        fo1 = fo[fo.completed_date.str.startswith(yr)]
        sp = {}
        for c in P.FOUR_DAY:
            R = L.crew_record(dict(D, fo=fo1), c)
            R0 = L.crew_record(D, c)
            plateau = set(R0["plateau"])
            st = L.standing_level(R, f"{yr}-01-01", f"{yr}-12-31", exclude=lambda x: x in plateau)[0]
            sp[c] = R0["ceiling"] - st
        ok(L.slots(L.queue_sets(D, G["placeable"], sp)) == G["slots"], f"{yr} standing level alone gives the same split")
    tmp = Path(tempfile.mkdtemp())
    try:
        t2 = tmp / "target"
        shutil.copytree(tgt, t2)
        for f in P.DISTRACTORS:
            (t2 / f).unlink()
        D3 = L.load(t2)
        ok(L.golden(D3)["slots"] == G["slots"], "golden unchanged with both distractors deleted")
        ok(K.golden(K.load(t2)) == K.golden(K.load(tgt)), "asks unchanged with both distractors deleted")
    finally:
        shutil.rmtree(tmp)
    wx = pd.read_csv(tgt / F["wx"])
    ok(set(wx.neighbourhood) <= nb_sv and wx.coop.nunique() == 6, "weatherization register sits in the same world")
    up = doc_texts(tgt)[F["upgrades"]]
    feeders_named = set(re.findall(r"[A-Z]{2}-\d{3}", up))
    ok(feeders_named and feeders_named <= set(D["host"].feeder), "reinforcement schedule names filed feeders")
    ok(re.findall(r"Q\d 20(\d\d)", up) and set(re.findall(r"Q\d 20(\d\d)", up)) == {"28"}, "every upgrade energised in 2028")
    # lens swap: the naive read and the answer are different forward quantities
    r3 = L.allocate(G["placeable"])
    ok(r3 != G["slots"] and sum(r3.values()) != G["placed"], "naive and answer are different constructions")


def twins(D, G):
    sv = D["sv"]
    cols = ["heating_system", "tenure", "structure", "income_band", "year_built", "bedrooms", "weight"]
    for a, b in ((("NS", "Elm Park"), ("VA", "Birch Hollow")), (("LA", "Loon Point"), ("RB", "Sauk Flats"))):
        ra = sv[sv.neighbourhood == a[1]][cols].sort_values(cols).reset_index(drop=True)
        rb = sv[sv.neighbourhood == b[1]][cols].sort_values(cols).reset_index(drop=True)
        ok(ra.equals(rb), f"twins {a[1]} and {b[1]} identical on every survey column")
    fm = D["fmap"].set_index("neighbourhood").feeder
    nb = L.nbhd_buyers(D)
    host = D["host"].set_index("feeder").hosting_capacity_remaining_kw // 5
    fb = nb.groupby(nb.index.get_level_values(1).map(fm)).sum()
    ok(fb[fm["Elm Park"]] > host[fm["Elm Park"]] and fb[fm["Birch Hollow"]] < host[fm["Birch Hollow"]],
       "Elm Park sits behind a full feeder, Birch Hollow does not")
    share_la = G["sets"]["LA"] / G["placeable"]["LA"]
    ok(fb[fm["Loon Point"]] < host[fm["Loon Point"]] and fb[fm["Sauk Flats"]] < host[fm["Sauk Flats"]]
       and 1 / share_la >= 1.5, f"Loon Point and Sauk Flats separated only by the crew ({1 / share_la:.2f}x)")
    REC["twin_sets"] = {"Loon Point": round(float(nb[("LA", "Loon Point")]) * share_la, 1),
                        "Sauk Flats": round(float(nb[("RB", "Sauk Flats")]), 1)}


# ------------------------------------------------------------------ the asks

def asks(tgt, D):
    KD = K.load(tgt)
    gold = K.golden(KD)
    for c in P.COOPS:
        g = gold[c]
        r = (g["cost_raw"] - 0.5) % 1
        ok(min(r, 1 - r) >= 0.2, f"{c} average cost {g['cost_raw']:.2f} clear of a whole-dollar edge")
        r = (g["share_raw"] - 0.05) % 0.1
        ok(min(r, 0.1 - r) >= 0.02, f"{c} rebate share {g['share_raw']:.3f} clear of a one-decimal edge")
    a_stops = {n: K.ask_a(KD, **kw) for n, kw in K.A_STOPS.items()}
    b_stops = {n: K.ask_b(KD, **kw) for n, kw in K.B_STOPS.items()}
    for n, v in a_stops.items():
        moved = [c for c in P.COOPS if round(v[c][0]) != gold[c]["cost"] or round(v[c][1], 1) != gold[c]["share"]]
        need = P.COOPS if n in ("every version summed", "first version", "latest delivered version",
                                "natural read (latest, head lines summed)") else (
            ["NS", "LA", "RB", "PW"] if n == "head lines summed as delivered" else P.COOPS[:0])
        ok(set(need) <= set(moved), f"ask A stop '{n}' misses the golden in {sorted(set(need) - set(moved))}")
    for n, v in b_stops.items():
        moved = [c for c in P.COOPS if round(v[c][0]) != gold[c]["paid"]]
        ok(len(moved) == 6, f"ask B stop '{n}' misses the golden dollars in every co-op ({moved})")
    lazy = b_stops["ledger as it stands, UTC dates"]
    ok(sum(lazy[c][1] != gold[c]["covered"] for c in P.COOPS) >= 4, "lazy B count off in four or more co-ops")
    # devices: fairness and separation
    inv = KD["inv"]
    rec = inv[inv.accepted_at != ""].groupby("invoice_no").version.max()
    ok(len(rec) == inv.invoice_no.nunique() == 412, "every job has exactly one invoice of record")
    heads = inv[inv.description.str.startswith(K.HEAD_LINE)]
    ok(heads.installer_id.nunique() == 1 and heads.groupby(["invoice_no", "version"]).amt.nunique().max() == 1,
       "head lines come from one firm and repeat one system price")
    pl = KD["pl"].set_index("premises_id")
    hj = heads.groupby("invoice_no").agg(n=("line_no", "size"), p=("premises_id", "first"),
                                         v=("version", "nunique"))
    ok(((hj.n / hj.v).astype(int) == pl.loc[hj.p, "indoor_heads"].to_numpy()).all(),
       "the referee: one head line per indoor head, one install per premises")
    ret = K.returned_ids(KD)
    led = KD["led"]
    ok(ret <= set(led.payment_id) and set(led.rebate_id) <= set(KD["pl"].rebate_id), "ledger and notices join")
    ok(led[led.payment_id.isin(ret)].method.eq("ACH").all(), "only bank transfers are returned")
    legs = led.groupby("rebate_id").payee_type.nunique()
    ok((legs == 2).sum() >= 100, "assigned rebates paid in two legs")
    two = led[led.rebate_id.isin(legs[legs == 2].index)]
    ok(not two.rebate_id.isin(led[led.payment_id.isin(ret)].rebate_id).any(), "no returned leg on an assigned rebate")
    eq = two.groupby("rebate_id").amt.nunique().eq(1).sum()
    ok(eq >= 20, f"{eq} assigned rebates with two equal legs (over-cleaning half)")
    t = pd.to_datetime(led[led.cleared_at != ""].cleared_at, utc=True)
    boundary = ((t.dt.tz_convert(K.CT).dt.strftime("%Y-%m-%d") == "2026-11-30") &
                (t.dt.strftime("%Y-%m-%d") == "2026-12-01")).sum()
    ok(boundary >= 15, f"{boundary} payments clear on 30 November Central, 1 December UTC")
    # separation: no device or hazard rows on the main call's path
    main_cols = ["rebate_id", "premises_id", "coop", "neighbourhood", "heating_system_replaced", "purchase_date",
                 "install_date", "meter_set_date"]
    ok(not KD["pl"][main_cols].isna().any().any(), "main path pilot columns complete")
    ok(set(inv.premises_id) == set(KD["pl"].premises_id) and len(set(inv.premises_id) & set(D["fo"].premises_id)
       - set(KD["pl"].premises_id)) == 0, "device rows sit only in the invoices, ledger and notices (0 on the main path)")
    REC["asks"] = {c: {k: gold[c][k] for k in ("cost", "share", "paid", "covered")} for c in P.COOPS}
    REC["ask_stops_a"] = {n: {c: [round(v[c][0]), round(v[c][1], 1)] for c in P.COOPS} for n, v in a_stops.items()}
    REC["ask_stops_b"] = {n: {c: [round(v[c][0]), v[c][1]] for c in P.COOPS} for n, v in b_stops.items()}
    REC["returns"] = len(ret)
    REC["boundary_payments"] = int(boundary)


def check_metadata(root, tgt, record):
    m = json.loads((root / "metadata.json").read_text())
    ok(m["distractor_files"] == P.DISTRACTORS and all((tgt / f).exists() for f in m["distractor_files"]),
       "metadata names the distractors")
    ok({f["path"] for f in m["files"]} == set(os.listdir(tgt)), "metadata lists every shipped file")
    ok(m["input_gates"]["files"] >= 10 and len(m["input_gates"]["formats"]) >= 3
       and m["input_gates"]["largest_file_rows"] >= 25000, "metadata input gates")
    ok(all(f["source"] and f["date"] and f["license"] for f in m["files"]), "source, date and licence per file")
    record["assertions"] = N["n"]


def run_all(W, tgt, root, sc):
    N["n"] = 0
    REC.clear()
    gates(tgt, root)
    registers(tgt)
    vocabulary(tgt)
    hygiene(tgt, sc)
    D = L.load(tgt)
    calibration(D)
    certification(D)
    G, rungs = ladder(D)
    crews(D, G)
    partials(D, G)
    grid(D, G)
    closures(D, G, tgt)
    twins(D, G)
    asks(tgt, D)
    REC["assertions"] = N["n"]
    return dict(REC)
