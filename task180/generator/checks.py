"""Assertion regime for task180. Run after build.py:  python3 checks.py   (exit 1 on any failure).

Rungs, the twin pair, the grid, the attribution signatures, decoupling, every ask stop, rounding
edges, separation of the devices from the main call, mess neutrality and the input gates.
"""
import datetime as dt
import inspect
import itertools
import json
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W        # noqa: E402
import standard as S     # noqa: E402
import golden as G       # noqa: E402

FAILS, PASSES = [], []
OUT = {}


def check(name, cond, detail=""):
    (PASSES if cond else FAILS).append((name, detail))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


R = W.ROLE_UNIT
L1, L2, V, A3, T1, T2, T3 = (R[k] for k in ("L1", "L2", "V", "A3", "T1", "T2", "T3"))
ANSWER = [V, A3, T1]


def edge_distance(v, places):
    q = 10 ** places
    return 0.5 / q - abs(v - round(v, places))


def main():
    g = G.solve()
    coded, naive, sig = g["coded"], g["naive"], g["signatures"]
    OUT["slate"] = g["slate"]

    # -- the answer ---------------------------------------------------------------------------
    check("answer slate is V, A3, T1 in order", g["slate"] == ANSWER, str(g["slate"]))
    check("attribution drops exactly L1 and L2", g["attributed"] == sorted([L1, L2]), str(g["attributed"]))
    c3 = sorted([t for t in coded if coded[t][0] == 3], key=lambda t: -coded[t][1])
    check("code 3 after attribution is V, A3, T1, T2, T3", c3 == [V, A3, T1, T2, T3], str(c3))
    sv = {t: coded[t][1] for t in W.IDS}
    check("V over A3 by 5 per cent or more", sv[V] / sv[A3] >= 1.05, f"{sv[V]:.4f}/{sv[A3]:.4f}")
    check("A3 over T1 by 5 per cent or more", sv[A3] / sv[T1] >= 1.05, f"{sv[A3]:.4f}/{sv[T1]:.4f}")
    check("slate cut: T1 over T2 by 5 per cent or more", sv[T1] / sv[T2] >= 1.05, f"{sv[T1]:.4f}/{sv[T2]:.4f}")
    check("V and A3 driven by acetylene, T1 by ethylene",
          (coded[V][2], coded[A3][2], coded[T1][2]) == ("C2H2", "C2H2", "C2H4"))
    check("T2 and T3 driven by ethylene", (coded[T2][2], coded[T3][2]) == ("C2H4", "C2H4"))
    check("L1 and L2 attributed: remaining gases code 2", coded[L1][0] == 2 and coded[L2][0] == 2,
          f"{coded[L1][:3]} {coded[L2][:3]}")
    check("L1 and L2 attributed severity below 1 and from paper gases",
          coded[L1][1] < 1 and coded[L2][1] < 1 and coded[L1][2] in ("CO", "CO2") and coded[L2][2] in ("CO", "CO2"),
          f"{coded[L1][1]:.4f} {coded[L1][2]} {coded[L2][1]:.4f} {coded[L2][2]}")
    OUT["severity"] = {t: round(sv[t], 4) for t in W.IDS}

    # -- the rungs ----------------------------------------------------------------------------
    lc = g["latest_c2h2"]
    r0 = sorted(W.IDS, key=lambda t: -lc[t])[:3]
    check("rung 0 (latest acetylene) names L2, L1, V", set(r0) == {L2, L1, V} and r0[0] == L2,
          str([(t, lc[t]) for t in r0]))
    check("rung 0: L1 and V tied on latest acetylene", lc[L1] == lc[V], f"{lc[L1]} {lc[V]}")
    r1 = g["naive_slate"]
    nsv = {t: naive[t][1] for t in W.IDS}
    check("rung 1 (code 3 ranked by severity) is L2 then L1 and V", r1[0] == L2 and set(r1) == {L2, L1, V},
          str([(t, round(nsv[t], 4)) for t in r1]))
    check("rung 1: L2 about 9.6", 9.5 < nsv[L2] < 9.7, f"{nsv[L2]:.4f}")
    check("rung 1: L1 and V tied about 8.1", nsv[L1] == nsv[V] and 8.0 < nsv[V] < 8.15, f"{nsv[L1]:.4f}")
    check("rung 1: A3 4.9-5.0, T1 4.7-4.8, T2 4.4-4.5, T3 3.x",
          4.9 < nsv[A3] < 5.0 and 4.7 < nsv[T1] < 4.8 and 4.4 < nsv[T2] < 4.5 and 3.0 < nsv[T3] < 4.0,
          f"{nsv[A3]:.4f} {nsv[T1]:.4f} {nsv[T2]:.4f} {nsv[T3]:.4f}")
    check("rung 1: the naive fourth (A3) is outside the naive slate by 5 per cent",
          nsv[V] / nsv[A3] >= 1.05)
    r2a, _ = G.solve_main([L2])
    r2b, _ = G.solve_main([L1])
    check("rung 2a (drop L2's acetylene only) names L1, V, A3", set(r2a) == {L1, V, A3}, str(r2a))
    check("rung 2b (drop L1's acetylene only) names L2, V, A3", set(r2b) == {L2, V, A3}, str(r2b))
    r3, _ = G.solve_main([t for t in W.IN_OIL])
    check("rung 3 (drop acetylene at every in-oil unit) names V, T1, T2", r3 == [V, T1, T2], str(r3))
    for nm, sl in (("rung 0", r0), ("rung 1", r1), ("rung 2a", r2a), ("rung 2b", r2b), ("rung 3", r3)):
        check(f"{nm} differs from the answer by at least one unit", set(sl) != set(ANSWER))
    OUT["rungs"] = {"r0": r0, "r1": r1, "r2a": r2a, "r2b": r2b, "r3": r3}

    # -- the twin pair -------------------------------------------------------------------------
    units = S.by_unit(S.record_of_issue(list(G.main_rows())))
    sl1, sv_ = units[L1], units[V]
    b1, bv = S.base_sample(sl1), S.base_sample(sv_)
    check("twin: same latest acetylene", sl1[-1]["C2H2"] == sv_[-1]["C2H2"], f"{sl1[-1]['C2H2']}")
    check("twin: same base-sample acetylene", b1["C2H2"] == bv["C2H2"], f"{b1['C2H2']}")
    check("twin: same sampling dates (latest and base)",
          sl1[-1]["sampled"].date() == sv_[-1]["sampled"].date() and b1["sampled"].date() == bv["sampled"].date())
    check("twin: same preservation class (latest and median) and age band",
          S.preservation(sl1) == S.preservation(sv_) and S.preservation(sl1, "median") == S.preservation(sv_, "median")
          and W.age_band(W.UNIT[L1]) == W.age_band(W.UNIT[V]))
    check("twin: identical naive code and severity", naive[L1][:3] == naive[V][:3], f"{naive[L1][:3]}")
    reg = G.register()
    check("twin: L1 in-oil arcing, V vacuum", reg[L1]["oltc_type"] == "In-oil arcing" and reg[V]["oltc_type"] == "Vacuum")

    # -- signatures ------------------------------------------------------------------------------
    for win in ("first_detectable", "last_bdl"):
        s2 = G.signatures(window=win)
        for t in (L1, L2):
            lim = 0.97 if win == "first_detectable" else 0.95
            check(f"{t} tracks its tap operations ({win}, raw r >= {lim})", s2[t]["r"] >= lim, f"{s2[t]['r']:.3f}")
            check(f"{t} tracks its tap operations ({win}, per-day r >= 0.95)", s2[t]["r_day"] >= 0.95,
                  f"{s2[t]['r_day']:.3f}")
        for t in (V, A3):
            check(f"{t} does not track ({win}, |r| raw and per day <= 0.3)",
                  abs(s2[t]["r"]) <= 0.3 and abs(s2[t]["r_day"]) <= 0.3,
                  f"{s2[t]['r']:.3f} {s2[t]['r_day']:.3f}")
        OUT[f"sig_{win}"] = {t: {k: (round(v, 3) if isinstance(v, float) else v) for k, v in s2[t].items()}
                             for t in s2}
    for t in (L1, L2):
        check(f"{t} C2H2/H2 twelve-month ratio at least 5", sig[t]["ratio"] >= 5, f"{sig[t]['ratio']:.2f}")
        check(f"{t} cumulative growth follows operations better than time", sig[t]["cum_ops_better"])
    check("V C2H2/H2 about 0.5", 0.4 <= sig[V]["ratio"] <= 0.6, f"{sig[V]['ratio']:.3f}")
    check("A3 C2H2/H2 about 0.6", 0.5 <= sig[A3]["ratio"] <= 0.7, f"{sig[A3]['ratio']:.3f}")
    for t in (V, A3):
        check(f"{t} cumulative growth does not follow operations better than time", not sig[t]["cum_ops_better"])
    # monthly sampling only (2026), the twelve-month window
    rest = sorted(set(sig) - {L1, L2, V, A3})
    cnt2 = {t: sum([sig[t]["type"] == "In-oil arcing", sig[t]["r"] >= 0.8, sig[t]["ratio"] >= 2]) for t in rest}
    check("no other unit with detectable acetylene meets two signatures", all(v < 2 for v in cnt2.values()),
          str({t: (round(sig[t]["r"], 2), round(min(sig[t]["ratio"], 99), 2)) for t in rest}))
    # tap operations do not follow load or season at the leaking units
    t0, arr = G.top_oil()
    lp = pd.read_parquet(G.tp("scada_top_oil"), columns=["transformer_id", "timestamp", "load_mva"])
    for t in (L1, L2):
        days, c = G.counters()[t]
        d_ops = pd.Series(np.diff(c), index=pd.to_datetime(days[:-1]))
        m_ops = d_ops.resample("MS").sum()
        ld = lp[lp.transformer_id == t].set_index("timestamp")["load_mva"].resample("MS").mean()
        both = pd.concat([m_ops, ld], axis=1, sort=True).dropna()
        rr = float(np.corrcoef(both.iloc[:, 0], both.iloc[:, 1])[0, 1])
        check(f"{t} monthly tap operations do not follow monthly load (|r| < 0.4)", abs(rr) < 0.4, f"{rr:.3f}")
        mon = m_ops.groupby(m_ops.index.month).mean()
        cv = float(mon.std() / mon.mean())
        check(f"{t} tap operations carry no strong season (monthly-mean CV < 0.25)", cv < 0.25, f"{cv:.3f}")

    # -- the grid -------------------------------------------------------------------------------
    cols = list(itertools.product(("zero", "half", "limit"), (330, 365, 400), ("latest", "median")))
    attribution_rules = {
        "type+tracking+ratio": dict(rule=("type", "tracking", "ratio")),
        "type+tracking": dict(rule=("type", "tracking")),
        "type+ratio": dict(rule=("type", "ratio")),
        "tracking+ratio": dict(rule=("tracking", "ratio")),
        "two of three": dict(rule=("type", "tracking", "ratio"), need=2),
        "ratio>2": dict(rule=("ratio",), ratio_min=2), "ratio>3": dict(rule=("ratio",), ratio_min=3),
        "ratio>5": dict(rule=("ratio",), ratio_min=5),
        "r>=0.8": dict(rule=("tracking",), r_min=0.8), "r>=0.9": dict(rule=("tracking",), r_min=0.9),
        "r>=0.95": dict(rule=("tracking",), r_min=0.95),
        "r/day>=0.9": dict(rule=("tracking",), r_min=0.9, tracking="day"),
        "cumulative growth": dict(rule=("tracking",), tracking="cum"),
        "type+cumulative": dict(rule=("type", "tracking"), tracking="cum"),
    }
    grid = {}
    nbad = 0
    for bdl, gap, cls in cols:
        kw = dict(bdl=bdl, gap=gap, cls_mode=cls)
        for win in ("first_detectable", "last_bdl"):
            sg = G.signatures(bdl=bdl, window=win, gap=gap)
            for name, rk in attribution_rules.items():
                att = G.attribute(sg, **rk)
                top, _ = G.solve_main(att, **kw)
                key = f"{name}|{win}|{bdl}|{gap}|{cls}"
                grid[key] = top
                if top != ANSWER:
                    nbad += 1
                    print("   grid miss", key, top, att)
        for name, excl in (("main-tank only", []),):
            top, cd = G.solve_main(excl, **kw)
            grid[f"{name}|{bdl}|{gap}|{cls}"] = top
            check(f"grid main-tank-only rule keeps L1 or L2 ({bdl},{gap},{cls})", bool({L1, L2} & set(top)), str(top))
        top_lc = sorted(W.IDS, key=lambda t: -S.value(units[t][-1]["C2H2"], bdl))[:3]
        check(f"grid latest-acetylene rule keeps L1 or L2 ({bdl})", bool({L1, L2} & set(top_lc)))
    check(f"grid: every attribution rule returns V, A3, T1 in every column ({len(cols)} columns x 2 windows x "
          f"{len(attribution_rules)} rules)", nbad == 0, f"{nbad} misses")
    OUT["grid_cells"] = len(grid)

    # analysis date in place of sampling date, record of issue ignored: the main call does not move
    top, _ = G.solve_main(g["attributed"], when="date")
    check("mess neutral: analysis date as the sample date leaves the slate", top == ANSWER, str(top))
    first_rows = {}
    for r in G.main_rows():
        if r["sample_id"] not in first_rows or int(r["issue"]) < int(first_rows[r["sample_id"]]["issue"]):
            first_rows[r["sample_id"]] = r
    co_first = S.fleet(list(first_rows.values()), excl={t: ("C2H2",) for t in g["attributed"]})
    check("mess neutral: first issue in place of the latest leaves every code and severity",
          all(co_first[t][:3] == coded[t][:3] for t in W.IDS))

    # -- separation: no device row inside the main call's population ----------------------------
    pop = [L1, L2, V, A3, T1, T2, T3]
    drops = {t: int((np.diff(G.counters()[t][1]) < 0).sum()) for t in pop}
    check("separation: no counter drop (rollover or replacement) at a code-3 unit", sum(drops.values()) == 0,
          str(drops))
    last, repl = G.services("log")
    regd = {t: (reg[t]["oltc_last_service"].date() if isinstance(reg[t]["oltc_last_service"], dt.datetime)
                else reg[t]["oltc_last_service"]) for t in reg}
    stale = sorted(t for t in reg if t in last and last[t] != regd[t])
    check("separation: no stale register date at a code-3 unit", not (set(stale) & set(pop)), str(stale))
    check("separation: no counter replacement at a code-3 unit", not (set(repl) & set(pop)))
    reiss = sorted({r["transformer_id"] for r in G.main_rows() if r["issue"] != "1"})
    check("separation: no laboratory re-issue at a code-3 unit", not (set(reiss) & set(pop)), str(reiss))
    OUT["devices"] = {"stale_register": stale, "replacements": {t: sorted(map(str, v)) for t, v in repl.items()},
                      "reissues": reiss}

    # -- ask A ---------------------------------------------------------------------------------
    a = g["ask_a"]
    check("ask A covers every in-oil tap changer", sorted(a) == sorted(W.IN_OIL), f"{len(a)}")
    check("ask A: ops never within 1,000 of 60,000", all(abs(v["ops"] - 60_000) >= 1000 for v in a.values()),
          str(sorted((abs(v['ops'] - 60000), t) for t, v in a.items())[:2]))
    latest_day = G.counters()[L1][0][-1]
    near7 = [(t, (latest_day - dt.date(v["last_service"].year + 7, v["last_service"].month,
                                        v["last_service"].day)).days) for t, v in a.items()]
    check("ask A: no service within 45 days of the seven-year line", all(abs(x) >= 45 for _, x in near7),
          str(sorted(near7, key=lambda x: abs(x[1]))[:2]))
    stops_a = {"register last-service date": G.ask_a(source="register"),
               "every drop a rollover": G.ask_a(drops="all_rollover"),
               "every drop a reset": G.ask_a(drops="all_reset"),
               "register date and every drop a rollover": G.ask_a(source="register", drops="all_rollover")}
    for nm, st in stops_a.items():
        moved = [t for t in a if st[t]["ops"] != a[t]["ops"]]
        flips = [t for t in a if st[t]["past"] != a[t]["past"]]
        check(f"ask A stop '{nm}' moves its figures", len(moved) >= 3, f"{len(moved)} ops moved, {len(flips)} flags")
        OUT[f"stopA {nm}"] = {"moved": moved, "flips": flips,
                              "values": {t: st[t]["ops"] for t in moved}}
    check("ask A stop 'register date' flips past-interval flags", len(OUT["stopA register last-service date"]["flips"]) >= 2)
    conv = G.ask_a(start="next_day")
    check("ask A converges: counting from the morning after the service gives the same figures",
          all(conv[t]["ops"] == a[t]["ops"] for t in a))
    for t in a:
        lr = G.log_counter_reading(t, a[t]["last_service"])
        days, c = G.counters()[t]
        if lr is not None and a[t]["last_service"] >= days[0]:
            if lr != int(c[days.index(a[t]["last_service"])]):
                check(f"log counter reading agrees with SCADA at {t}", False)

    # -- ask B ---------------------------------------------------------------------------------
    b = g["ask_b"]
    wet = sorted(t for t in b if b[t]["rs"] > 30)
    check("ask B: six wet transformers", len(wet) == 6, str(wet))
    check("ask B: every RS at least 0.02 from a one-decimal edge",
          all(edge_distance(v["rs"], 1) >= 0.02 for v in b.values()),
          str(min((edge_distance(v['rs'], 1), t) for t, v in b.items())))
    check("ask B: every RS at least 0.5 from 30 per cent", all(abs(v["rs"] - 30) >= 0.5 for v in b.values()),
          str(min((abs(v['rs'] - 30), t) for t, v in b.items())))
    stops_b = {"SCADA read on the local clock (no UTC conversion)": G.ask_b(tz="none"),
               "fixed UTC+12 all year": G.ask_b(tz="fixed12"), "fixed UTC+13 all year": G.ask_b(tz="fixed13"),
               "analysis date as the sampling date": G.ask_b(when="analysis"),
               "laboratory re-issue ignored": G.ask_b(reissue="first")}
    for nm, st in stops_b.items():
        moved = [t for t in b if round(st[t]["rs"], 1) != round(b[t]["rs"], 1)]
        lst = sorted(t for t in st if st[t]["rs"] > 30)
        check(f"ask B stop '{nm}' moves its figures", len(moved) >= 2,
              f"{len(moved)} moved, list {'changes' if lst != wet else 'same'}")
        OUT[f"stopB {nm}"] = {"moved": moved, "list": lst,
                              "values": {t: round(st[t]["rs"], 1) for t in moved}}
    check("ask B: the UTC stop changes the wet list", OUT["stopB SCADA read on the local clock (no UTC conversion)"]["list"] != wet)
    check("ask B: the re-issue stop changes the wet list", OUT["stopB laboratory re-issue ignored"]["list"] != wet)

    # -- decoupling: clearing the attribution moves no ask figure ---------------------------------
    keep = G.attribute
    G.attribute = lambda *aa, **kk: []
    g2 = {"a": G.ask_a(), "b": G.ask_b(), "slate": G.answer()[0]}
    G.attribute = keep
    check("decoupling: with the attribution cleared the slate moves", g2["slate"] != ANSWER, str(g2["slate"]))
    check("decoupling: ...and no ask A figure moves", all(g2["a"][t] == a[t] for t in a))
    check("decoupling: ...and no ask B figure moves", all(g2["b"][t]["rs"] == b[t]["rs"] for t in b))
    src = inspect.getsource(G.ask_a) + inspect.getsource(G.ask_b) + inspect.getsource(G.ops_since)
    check("decoupling: the ask code never reads a code or the slate",
          not re.search(r"solve_main|code_unit|fleet\(|attribute\(", src))

    # -- rounding edges and thresholds ------------------------------------------------------------
    worst = min((edge_distance(sv[t], 2), t) for t in W.IDS)
    check("every severity at least 0.002 from a two-decimal edge", worst[0] >= 0.002, f"{worst[0]:.4f} {worst[1]}")
    worst_r = min((abs(sv[t] - round(sv[t], 2)), t) for t in W.IDS)
    check("no severity within 0.0003 of its two-decimal value", worst_r[0] >= 0.0003, f"{worst_r[0]:.5f} {worst_r[1]}")
    for t in (L1, L2):
        check(f"naive severity of {t} at least 0.002 from an edge", edge_distance(nsv[t], 2) >= 0.002, f"{nsv[t]:.4f}")
    near = []
    for t in W.IDS:
        det = coded[t][3]
        for gg, rt in det["ratios"].items():
            if abs(rt - 1) < 0.03:
                near.append((t, gg, rt))
    check("no coded rate within 3 per cent of its limit", not near, str(near[:3]))

    o2n2 = []
    for t in W.IDS:
        ss = units[t]
        lat = float(ss[-1]["O2"]) / float(ss[-1]["N2"])
        med = float(np.median([float(r["O2"]) / float(r["N2"]) for r in ss]))
        o2n2.append(min(abs(lat - 0.2), abs(med - 0.2)))
    check("every unit's O2/N2 (latest and median) at least 0.07 from 0.2", min(o2n2) >= 0.07, f"{min(o2n2):.3f}")
    ages = [abs((2026 - max(W.UNIT[t]["year"], W.UNIT[t]["rewind"] or 0)) - b_) for t in W.IDS for b_ in (10, 30)]
    check("no transformer's age within one year of an age-band boundary", min(ages) >= 2, str(min(ages)))

    # -- input gates -------------------------------------------------------------------------------
    files = sorted(os.listdir(G.TARGET))
    exts = sorted({os.path.splitext(f)[1] for f in files})
    check("12 to 14 files", 12 <= len(files) <= 14, str(len(files)))
    check("at least 5 formats", len(exts) >= 5, str(exts))
    import pyarrow.parquet as pq
    nrow = pq.ParquetFile(G.tp("scada_top_oil")).metadata.num_rows
    check("hourly top-oil parquet above 1,500,000 rows", nrow > 1_500_000, f"{nrow:,}")
    check("no file name says distractor", not any("distractor" in f.lower() for f in files))
    meta = json.load(open(os.path.join(HERE, "..", "metadata.json"))) if os.path.exists(
        os.path.join(HERE, "..", "metadata.json")) else {}
    dist = meta.get("distractor_files", [])
    check("metadata names two distractors that ship", len(dist) == 2 and all(d in files for d in dist), str(dist))
    gsrc = open(os.path.join(HERE, "golden.py")).read()
    check("the golden never reads a distractor", "protection_relay" not in gsrc and "thermal_imaging" not in gsrc)
    # the daily cycle makes the export's clock discoverable
    lt = lp[lp.transformer_id == "LIN-T1"].copy()
    lt["h"] = lt["timestamp"].dt.hour
    jul = lt[(lt.timestamp.dt.month == 7)].groupby("h")["load_mva"].mean().idxmax()
    jan = lt[(lt.timestamp.dt.month == 1)].groupby("h")["load_mva"].mean().idxmax()
    check("evening peak sits at 05:00 to 07:00 by the export clock in July (NZST)", 5 <= jul <= 7, str(jul))
    check("and an hour earlier in January (NZDT)", jan == jul - 1 or 4 <= jan <= 6, f"{jan} vs {jul}")
    # text sweeps: em dashes, the standard's silence on leakage, no clock zone named anywhere
    texts = {}
    for f in files:
        p = os.path.join(G.TARGET, f)
        if f.endswith((".md", ".txt", ".csv")):
            texts[f] = open(p, encoding="utf8").read()
        elif f.endswith(".pdf"):
            from pypdf import PdfReader
            texts[f] = "\n".join(pg.extract_text() for pg in PdfReader(p).pages)
        elif f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                texts[f] = " ".join(z.read(n).decode("utf8", "ignore") for n in z.namelist() if n.endswith(".xml"))
    check("no em dash in any shipped file", not any("\u2014" in t for t in texts.values()))
    std = texts["ES-DGA-02_fleet_dga_condition_standard.pdf"].lower()
    check("the standard never mentions leakage, contamination, weeping or barriers",
          not re.search(r"leak|contaminat|weep|barrier|seep", std))
    check("no shipped file names UTC or GMT", not any(re.search(r"\bUTC\b|\bGMT\b|Zulu", t) for t in texts.values()))
    logtxt = texts["maintenance_log_2019-2026.xlsx"].lower()
    check("the maintenance log never mentions leaks, barriers or gas results",
          not re.search(r"leak|weep|barrier|seep|acetylene|dga|dissolved gas", logtxt))
    notes = texts["oil_results_notes.md"].lower()
    check("the notes narrate no device", not re.search(r"utc|rollover|roll over|re-issue|stale|replaced|leak", notes))
    # no golden figure (two decimals, one decimal or four or more digits) stated in a shipped document
    figs = {f"{sv[t]:.2f}" for t in W.IDS} | {f"{b[t]['rs']:.1f}" for t in b} | \
        {f"{a[t]['ops']:,}" for t in a} | {str(a[t]["ops"]) for t in a}
    figs = {x for x in figs if len(re.sub(r"\D", "", x)) >= 3}
    hits = []
    for f_, t_ in texts.items():
        if f_.endswith((".md", ".txt", ".pdf")):
            for x in figs:
                if re.search(r"(?<![\d.,])" + re.escape(x) + r"(?![\d])", t_):
                    hits.append((f_, x))
    check("no golden figure appears in a shipped document", not hits, str(hits[:4]))
    # container metadata
    scrub = os.path.join(HERE, "..", "..", ".claude", "skills", "reduce-house-fixes", "scripts",
                         "scrub_producer_metadata.py")
    rr = subprocess.run([sys.executable, scrub, G.TARGET, "--floor", "2025-01-01", "--ceiling", "2026-10-16"],
                        capture_output=True, text=True)
    check("container metadata: no writer signature, dates in band (target)", "clean" in rr.stdout, rr.stdout.strip()[:200])
    rr = subprocess.run([sys.executable, scrub, G.GOLDEN, "--floor", "2026-10-01", "--ceiling", "2026-10-28"],
                        capture_output=True, text=True)
    check("container metadata: golden clean and dated with the paper", "clean" in rr.stdout, rr.stdout.strip()[:200])
    # the golden files agree with the solve
    gcsv = pd.read_csv(os.path.join(G.GOLDEN, "dga_fleet_review.csv"), dtype=str, keep_default_na=False)
    ok = True
    for _, row in gcsv.iterrows():
        t = row["transformer_id"]
        ok &= row["severity_score"] == f"{sv[t]:.2f}" and row["condition_code"] == str(coded[t][0])
        ok &= row["relative_saturation_pct"] == f"{b[t]['rs']:.1f}"
        ok &= row["oltc_operations_since_service"] == (str(a[t]["ops"]) if t in a else "")
        ok &= row["on_slate"] == ("yes" if t in ANSWER else "no")
    check("golden CSV carries every solved figure", ok and len(gcsv) == 44)

    print(f"\n{len(PASSES)} passed, {len(FAILS)} failed")
    with open(os.environ.get("T180_RESULTS", "/tmp/task180_checks.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
