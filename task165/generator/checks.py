"""task165 checks: the generator's assertions on the built pack (target/) and on the clean truth (world.py, records.py,
yards.py).

The three-rules block (R1 to R3c), the ladder and its rivals, the out-of-sample tests, the golden's family and its
one-sigma corridor, the reflex sweep, the twin pair, every semantic fork row (SF1 to SF11), both asks with their
devices and stops, the cracker's measured pair, the separation line, the input gates, the realism sweep, the dates
and the distractors' deletion test."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import common as K      # noqa: E402
import cracker as CR    # noqa: E402
import docs as D        # noqa: E402
import pack as P        # noqa: E402
import pack2 as P2      # noqa: E402
import records as R     # noqa: E402
import world as Wd      # noqa: E402
import yards as Y       # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
RESULTS = []

GOLD = 2200            # the seasonal tonnage, nearest 100 t
DEFAULT = 2600         # rung 1, the default path
POOLED = 1500          # rung 2, the earlier moves' average gain
N_MOVES = 431          # collectors moved Priority 2 to Priority 1 on 1 November 2022 to 2025
OWN, GAIN = 1.7, 5.2   # the components, t a lane-km in a winter at the planning severity
SEV = C.PLAN_SEV
ASK_EDGE = 0.0295      # every ask figure at least this far (t) from its one-decimal rounding edge


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s %-74s %s" % ("PASS" if ok else "FAIL", label[:74], detail))


def call(v):
    return int(round(v / 100.0) * 100)


def r1(v):
    return round(v + 1e-9, 1)


def linked_copy(skip):
    """A folder of links to every shipped file but the ones named."""
    tmp = tempfile.mkdtemp(prefix="chk165_", dir=TASK)
    for f in os.listdir(TARGET):
        if f not in skip:
            os.symlink(os.path.join(TARGET, f), os.path.join(tmp, f))
    return tmp


def shipped_text():
    """Every shipped file's text: CSV as read, workbook strings, PDF text through pypdf."""
    import openpyxl
    out = {}
    for f in sorted(os.listdir(TARGET)):
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            out[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            parts = []
            for ws in wb.worksheets:
                for row in ws.iter_rows(values_only=True):
                    parts.extend(str(v) for v in row if v is not None)
            wb.close()
            out[f] = "\n".join(parts)
        elif f.endswith(".pdf"):
            out[f] = C.pdf_text(p)
    return out


def main():
    P_ = C.Pack(TARGET)
    g = C.golden(P_)
    nn = P_.new_rates()
    L = float(nn["lane_km"].sum())
    x0 = float((nn["p2"] * nn["lane_km"]).sum() / L)
    d = P_.prepost()
    own, gain = x0 * SEV, g / L

    # ------------------------------------------------------------------------------------------ the golden
    check("GOLD the seasonal tonnage", call(g) == GOLD, "%.1f t -> %d" % (g, call(g)))
    check("GOLD the raw figure a quarter-bin or more from its rounding edge", K.bin_edge_distance(g, 100) >= 25,
          "%.1f t" % K.bin_edge_distance(g, 100))
    check("GOLD the population: 216 segments, 424.0 lane-km, moved on 30 August 2026",
          len(nn) == 216 and abs(L - 424.0) < 1e-6, "%d, %.2f" % (len(nn), L))
    check("GOLD the earlier moves: %d collectors on the four 1 November dates" % N_MOVES,
          len(d) == N_MOVES and sorted({str(e) for e in d["eff"]}) == ["2022-11-01", "2023-11-01", "2024-11-01",
                                                                   "2025-11-01"], "%d" % len(d))
    check("GOLD component: own Priority 2 salt 1.7 t a lane-km, clear of its edge",
          r1(own) == OWN and K.bin_edge_distance(own, 0.1) >= 0.015, "%.4f" % own)
    ids_new = list(nn["segment_id"])
    tot_new = {w: sum(float(P_.salt.get((s_, w), 0.0)) for s_ in ids_new) for w in K.WINTERS}
    alt_own = [tot_new[w] / (L * P_.wsi[w]) * SEV for w in K.WINTERS] + \
        [float(np.mean([tot_new[w] / (L * P_.wsi[w]) for w in K.WINTERS])) * SEV]
    check("GOLD component: own Priority 2 salt rounds to 1.7 in every winter and as the mean of winters",
          all(r1(v) == OWN for v in alt_own), str([round(v, 3) for v in alt_own]))
    check("GOLD component: the gain 5.2 t a lane-km, clear of its edge",
          r1(gain) == GAIN and K.bin_edge_distance(gain, 0.1) >= 0.025, "%.4f" % gain)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    check("GOLD figures.json carries the call and both components",
          figs["commitment_t"] == GOLD and figs["own_p2_t_per_lkm"] == r1(own) and figs["gain_t_per_lkm"] == r1(gain)
          and figs["lane_km"] == 424.0 and figs["segments"] == 216 and figs["earlier_moves"] == N_MOVES, "")

    # ------------------------------------------------------------------------------------------ R1
    import pyarrow.parquet as pq
    import openpyxl
    heads = []
    for f in os.listdir(TARGET):
        p = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            heads += [(f, h) for h in open(p, encoding="utf-8").readline().strip().split(",")]
        elif f.endswith(".parquet"):
            heads += [(f, h) for h in pq.ParquetFile(p).schema_arrow.names]
        elif f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(p, read_only=True)
            for ws in wb.worksheets:
                for row in ws.iter_rows(min_row=1, max_row=6, values_only=True):
                    heads += [(f, str(v)) for v in row if isinstance(v, str) and len(v) < 40]
            wb.close()
    bad = [h for h in heads if re.search(r"coverage|covered|hazard|\bgain|untreat|spot|share_salted|per.lane|\brate\b|t_per",
                                         h[1], re.I)]
    check("R1 no shipped column holds a coverage, a hazard length, a gain or a rate", not bad, str(bad[:4]))
    ps = pd.read_parquet(os.path.join(TARGET, P.F_PASSES))
    check("R1 the platform ships one row per spreader pass over one segment, 25,000 rows or more",
          len(ps) >= 25000 and not ps.duplicated(["unit_id", "segment_id", "entry_utc"]).any(), "%d rows" % len(ps))
    leg = pd.read_csv(os.path.join(TARGET, P.F_LEGACY), dtype={"SEG_ID": str})
    check("R1 the legacy AVL ships segment-by-shift material, 25,000 rows or more", len(leg) >= 25000,
          "%d rows" % len(leg))
    full = all(float(P_.salt.get((r["segment_id"], w), 0.0)) > 0 for _, r in P_.earlier_moves().iterrows()
               for w in K.WINTERS)
    check("R1 the decisive fit reads each earlier move's own salt in every winter, before and after", full, "")

    # ------------------------------------------------------------------------------------------ R3 on the clean truth
    W = Wd.World()
    S = R.Sim(W)
    wsi_t = {w: sum(e["points"] for e in W.events[w]) for w in K.WINTERS}
    segs = {s["segment_id"]: s for s in W.segments}

    def trate(sid, ws):
        return sum(S.truth.get((sid, w), 0.0) for w in ws) / (segs[sid]["lane_km"] * sum(wsi_t[w] for w in ws))

    new = [s for s in W.segments if s["pool"] == "NEW"]
    mv = [s for s in W.segments if s["pool"] == "MOVE"]
    p1in = [s for s in W.segments if s["pool"] == "P1IN"]
    Lt = sum(s["lane_km"] for s in new)
    x0t = sum(trate(s["segment_id"], K.WINTERS) * s["lane_km"] for s in new) / Lt
    tot = den = 0.0
    for s in p1in + mv:
        for w in K.WINTERS:
            if W.priority(s, w) == 1:
                tot += S.truth.get((s["segment_id"], w), 0.0)
                den += s["lane_km"] * wsi_t[w]
    r3a = (tot / den - x0t) * Lt * SEV
    rows = []
    for s in mv:
        pre = [w for w in K.WINTERS if W.priority(s, w) == 2]
        post = [w for w in K.WINTERS if W.priority(s, w) == 1]
        rows.append((s["lane_km"], trate(s["segment_id"], pre), trate(s["segment_id"], post), s["h"]))
    Lk, pre_t, post_t, h_t = map(np.array, zip(*rows))
    bt = C.wls(pre_t, post_t - pre_t, Lk)
    r3b = (bt[0] + bt[1] * x0t) * Lt * SEV
    pooled_t = ((post_t - pre_t) * Lk).sum() / Lk.sum() * Lt * SEV
    check("R3a the easy route on the clean truth files the default path", call(r3a) == DEFAULT, "%.1f t" % r3a)
    check("R3b the decisive step alone on the clean truth files the golden", call(r3b) == GOLD, "%.1f t" % r3b)
    check("R3b the event study alone (pooled gain) on the clean truth stays wrong", call(pooled_t) == POOLED,
          "%.1f t" % pooled_t)
    expected = sum(W.gain_truth(s) * s["lane_km"] * s["m"] for s in new)
    check("R3b the world's own expected gain within two standard errors of the golden", abs(expected - g) < 2 * 15.0,
          "%.1f t" % expected)
    check("R3b the clean truth and the pack agree on the call's rows (no mess on them)",
          abs(r3a - C.r1_default(P_)) < 1.0 and abs(r3b - g) < 1.0, "%.2f, %.2f" % (r3a - C.r1_default(P_), r3b - g))
    txt = shipped_text()
    docs_txt = " ".join(txt[f] for f in (P.F_PLAN, P.F_PROC, P.F_SURVEY)).replace("\n", " ")
    check("R3c no document says how a street's salt responds to its service level or its coverage",
          not re.search(r"already salted|share of (each|the|a) (street|section|segment|collector)|coverage|untreated|"
                        r"depends on|the gain|in proportion to", docs_txt, re.I), "")
    check("R3c no document states a seasonal tonnage, a gain or a forecast for the change",
          not re.search(r"\b\d{1,2},\d{3}\s*t\b|\b\d+(\.\d+)?\s*t a lane|tonnes? (a|per) lane", docs_txt), "")
    check("R3c no memo, draft, briefing or correspondence ships",
          not any(f.endswith((".docx", ".eml", ".msg", ".txt", ".md")) for f in os.listdir(TARGET)), "")
    sv = P_.salt.unstack().fillna(0.0).round(6)
    check("R3c no segment's five winters of salt repeat another's (no copied block)",
          not sv.duplicated().any(), "%d segments" % len(sv))

    # ------------------------------------------------------------------------------------------ R2 mess neutrality
    Pu = C.Pack(TARGET, utc_as_local=True)
    gu = C.golden(Pu)
    check("R2 the platform's UTC times read as local: same call and components",
          call(gu) == GOLD and r1(gu / L) == r1(gain), "%.1f t" % gu)
    Px = C.Pack(TARGET, xwalk=False)
    gx = C.golden(Px)
    check("R2 the legacy ids joined without the crosswalk: same call", call(gx) == GOLD, "%.1f t" % gx)
    gc = C.centreline(P_)
    xl = pd.ExcelFile(os.path.join(TARGET, P.F_STORM))
    seasons_ok = True
    for w in K.NEW_WINTERS:
        df = xl.parse(w, header=None)
        lab = df.iloc[:, 0].astype(str).str.strip()
        row = df[lab.str.lower().str.startswith("season wsi")]
        if len(row) != 1:
            seasons_ok = False
            continue
        vals = [v for v in row.iloc[0].tolist()[1:] if isinstance(v, (int, float)) and not pd.isna(v)]
        seasons_ok &= bool(vals) and abs(float(vals[-1]) - P_.wsi[w]) < 1e-6
    check("R2 the storm log's Season WSI rows equal the sums of their events (either read)", seasons_ok, "")
    legc = leg.merge(P_.reg[["segment_id", "func_class"]], left_on="SEG_ID", right_on="segment_id", how="left")
    legc = legc[legc["func_class"] == "COLLECTOR"]
    lr = legc["KG"].sum() / 1000.0
    check("R2 the legacy kilograms read as tonnes is loud (a thousandfold the platform's)",
          (legc["KG"].median() / 1000.0) < 1.0 < legc["KG"].median(), "median %.0f kg" % legc["KG"].median())
    edge_rows = legc[legc["SHIFT_DATE"].str[5:].isin(["10-31", "04-01"]) |
                     ((legc["SHIFT_DATE"].str[5:] == "03-31") & (legc["SHIFT"] == "NIGHT"))]
    check("R2 no collector shift sits on a season boundary (night shifts dated by their start: same call)",
          len(edge_rows) == 0, "%d rows, %.0f t legacy collector salt" % (len(edge_rows), lr))

    # ------------------------------------------------------------------------------------------ the ladder
    wmean = float(np.mean(list(P_.wsi.values())))
    last = P_.wsi["2025-26"]
    lad = {
        "R0 the Priority 1 network gross, last winter": (C.r0_network(P_, sev=last, winters=["2025-26"]), 5000),
        "R0b the Priority 1 network gross, planning severity": (C.r0_network(P_), 5400),
        "R1 default: Priority 1 collector rate less own salt": (C.r1_default(P_), DEFAULT),
        "R1b the same over the earlier moves' Priority 1 winters": (C.r1_default(P_, True), 2500),
        "R1c the default at last winter's points (no planning severity)": (C.r1_default(P_) * last / SEV, 2400),
        "R1d the default at the five winters' mean points": (C.r1_default(P_) * wmean / SEV, 2300),
        "R2 the earlier moves' pooled gain": (C.r2_pooled(P_), POOLED),
        "R2b the transit-driven earlier moves' gain": (C.r2_pooled(P_, "QRT Route"), 1600),
        "R2c the pooled gain stratified by yard": (C.reflex_stratified(P_, "yard"), 1600),
        "R2c the pooled gain stratified by lanes": (C.reflex_stratified(P_, "lanes"), 1500),
        "R2c the pooled gain stratified by length band": (C.reflex_stratified(P_, "lenband"), 1500),
        "R2d the golden's gain at last winter's points": (g * last / SEV, 2100),
        "R2e the golden's gain at the five winters' mean": (g * wmean / SEV, 2000),
        "R2f the earlier moves' ratio on own salt": (C.reflex_ratio(P_), 600),
        "R2g the pooled gain trended over move years": (C.reflex_trend(P_), 1600),
        "R2h the pooled gain against never-moved collectors": (C.reflex_did(P_), 1600),
        "R2i the earlier moves inside the new streets' range, averaged": (C.range_match(P_)[0], 2100),
    }
    for name, (v, want) in lad.items():
        check("LADDER %s" % name, call(v) == want and abs(v - g) >= 100 and call(v) != GOLD,
              "%.1f t -> %d" % (v, call(v)))
    for name, v in (("the default and the pooled gain", (C.r1_default(P_) + C.r2_pooled(P_)) / 2),
                    ("the moves' own level and the pooled gain", (C.r1_default(P_, True) + C.r2_pooled(P_)) / 2),
                    ("the default and the transit moves' gain", (C.r1_default(P_) + C.r2_pooled(P_, "QRT Route")) / 2)):
        check("HEDGE the midpoint of %s misses the golden's bin by 50 t or more" % name,
              v < 2150 - 50 or v >= 2250 + 50, "%.1f t" % v)
    pc_ = P_.reg[(P_.reg["func_class"] == "COLLECTOR") & (P_.reg["priority"] == "1")]
    newset = set(nn["segment_id"])
    keep = [(s_, lk_) for s_, lk_ in zip(pc_["segment_id"], pc_["lane_km"]) if s_ not in newset]
    p1_last = sum(float(P_.salt.get((s_, "2025-26"), 0.0)) for s_, _ in keep) / sum(lk_ for _, lk_ in keep)
    own_last = tot_new["2025-26"] / L
    coin = (p1_last - own_last) * L
    check("HEDGE last winter's totals, netted, no planning severity, miss the golden's bin by 50 t or more",
          coin < 2150 - 50 or coin >= 2250 + 50, "%.1f t (%.2f less %.2f t a lane-km)" % (coin, p1_last, own_last))
    check("LADDER bracketed: the netting above the golden, every average gain below",
          C.r1_default(P_) > g > max(C.r2_pooled(P_), C.r2_pooled(P_, "QRT Route"), C.reflex_trend(P_)), "")

    # ------------------------------------------------------------------------------------------ out of sample
    ho = C.holdout(P_)
    check("OOS each move year held out: the conditioned gain within 4 per cent",
          all(abs(v[1]) < 0.04 for v in ho.values()), str({k: round(v[1], 3) for k, v in ho.items()}))
    check("OOS each move year held out: the pooled gain off by over 10 per cent in a year",
          max(abs(v[0]) for v in ho.values()) > 0.10, str({k: round(v[0], 3) for k, v in ho.items()}))
    cv = {f: C.cv_wsse(P_, f) for f in ("line", "loglog", "pool")}
    check("OOS ten-fold: the line's error under the power law's and a fifth of the average's",
          cv["line"] < cv["loglog"] and cv["line"] < cv["pool"] / 5, str({k: round(v, 5) for k, v in cv.items()}))
    lb = {f: C.low_band(P_, f) for f in ("line", "loglog", "pool")}
    check("OOS the new streets' band predicted from the rest: the line within 3 per cent",
          abs(lb["line"][0]) < 0.03 and lb["line"][1] >= 60, "%.3f over %d streets" % lb["line"])
    check("OOS the same: the power law and the average gain miss by over 10 per cent",
          lb["loglog"][0] < -0.10 and lb["pool"][0] < -0.10, "%.3f, %.3f" % (lb["loglog"][0], lb["pool"][0]))
    ll = C.loglog(P_)
    check("OOS the power law, weaker out of sample, still files the golden's bin", call(ll) == GOLD and
          K.bin_edge_distance(ll, 100) >= 25, "%.1f t" % ll)

    # ------------------------------------------------------------------------------------------ the golden's family
    fam = {
        "weighted by lane-km (golden)": g,
        "unweighted": C.golden(P_, weight=False),
        "the last winter before each move only": C.golden(P_, pre_last=True),
        "the first winter after each move only": C.golden(P_, post_first=True),
        "both one-winter windows": C.golden(P_, pre_last=True, post_first=True),
        "summed street by street": C.golden(P_, per_segment=True),
        "the Priority 1 level regressed, own salt taken off": C.golden(P_, level=True),
        "each winter against the never-moved collectors": C.golden_did(P_),
        "each street's rate the mean of its winters": C.winter_mean(P_),
        "quadratic in Priority 2 salt": C.quadratic(P_),
        "outliers over three deviations dropped": C.trimmed(P_),
        "10 nearest earlier moves": C.knn(P_, 10),
        "20 nearest earlier moves": C.knn(P_, 20),
        "40 nearest earlier moves": C.knn(P_, 40),
        "three bands of Priority 2 salt": C.qbins(P_, 3),
        "four bands": C.qbins(P_, 4),
        "five bands": C.qbins(P_, 5),
        "eight bands": C.qbins(P_, 8),
    }
    for name, v in fam.items():
        check("FAMILY %s files the golden" % name, call(v) == GOLD and K.bin_edge_distance(v, 100) >= 24,
              "%.1f t" % v)
    crude_in = {"fixed 1.5 t bands": C.fixed_bands(P_, 1.5), "fixed 1 t bands": C.fixed_bands(P_, 1.0),
                "the 10 nearest the pool's mean": C.nearest_to_mean(P_, 10),
                "a window of 0.2 t either side": C.window(P_, 0.2)[0], "a window of 1 t": C.window(P_, 1.0)[0],
                "a kernel of 0.62 t": C.kernel(P_, 0.62)}
    check("CRUDE settings of the conditioning file the golden (bands, nearest, windows, a 0.62 t kernel)",
          all(call(v) == GOLD for v in crude_in.values()), str({k: round(v, 1) for k, v in crude_in.items()}))
    wide = C.kernel(P_, 1.23)
    spread_new = float(np.std(nn["p2"].values * SEV))
    check("CRUDE only a kernel wider than the new streets' own spread (1.23 t) slips a bin, toward the pooled gain",
          call(wide) == 2100 and 1.23 > 1.5 * spread_new, "%.1f t, new streets' spread %.2f t" % (wide, spread_new))
    sd = C.bootstrap_sd(P_)
    check("SIGMA one bootstrap standard error over the %d streets under 16 t" % N_MOVES, sd < 16.0, "%.1f t" % sd)
    check("SIGMA the golden plus or minus two standard errors stays in its bin",
          K.bin_edge_distance(g, 100) > 2 * sd, "%.1f against %.1f" % (K.bin_edge_distance(g, 100), 2 * sd))
    check("SIGMA every family member plus or minus one standard error stays in the bin",
          all(K.bin_edge_distance(v, 100) > sd for v in fam.values()),
          "nearest %.1f t" % min(K.bin_edge_distance(v, 100) for v in fam.values()))

    # ------------------------------------------------------------------------------------------ orthogonality, twin
    for pool in ("MOVE", "NEW"):
        df = pd.DataFrame([{"h": s["h_haz"], "lanes": s["lanes"], "cl": s["centreline_km"], "yard": s["yard"]}
                           for s in W.segments if s["pool"] == pool])
        cy = max(abs(np.corrcoef(df["h"], (df["yard"] == y).astype(float))[0, 1]) for y in K.YARDS)
        cl_ = abs(np.corrcoef(df["h"], df["lanes"])[0, 1])
        cc = abs(np.corrcoef(df["h"], df["cl"])[0, 1])
        check("ORTHO %s hazard share against lanes, length and yard (never shipped)" % pool,
              cl_ < 0.1 and cc < 0.1 and cy < 0.2, "%.3f, %.3f, %.3f" % (cl_, cc, cy))
    p2c = P_.reg[(P_.reg["func_class"] == "COLLECTOR") & (P_.reg["priority"] == "2")]
    rr_ = [P_.rate(s_, K.WINTERS, lk_) for s_, lk_ in zip(p2c["segment_id"], p2c["lane_km"])]
    cinv = float(np.corrcoef(rr_, 1.0 / p2c["centreline_km"].values)[0, 1])
    check("REALISM Priority 2 salt per lane-km rises as segments shorten (intersection approaches)", cinv > 0.15,
          "corr with 1/length %.3f" % cinv)
    check("ORTHO the earlier moves' coverage twice the new streets'",
          np.average(h_t, weights=Lk) > 2 * np.average([s["h"] for s in new], weights=[s["lane_km"] for s in new]),
          "%.3f against %.3f" % (np.average(h_t, weights=Lk),
                                 np.average([s["h"] for s in new], weights=[s["lane_km"] for s in new])))
    em = P_.earlier_moves().set_index("segment_id")
    dd = d.set_index("segment_id")
    dd["gain"] = dd["post"] - dd["pre"]
    best = None
    for (st, yd, ln, rs, ef), grp in em.groupby(["street", "yard", "lanes", "reason", "eff"]):
        ids = list(grp.index)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                a, b = ids[i], ids[j]
                if abs(em.loc[a, "centreline_km"] - em.loc[b, "centreline_km"]) > 0.06:
                    continue
                ga, gb = dd.loc[a, "gain"], dd.loc[b, "gain"]
                pa, pb = dd.loc[a, "pre"], dd.loc[b, "pre"]
                ratio = max(ga, gb) / min(ga, gb)
                dcl = abs(em.loc[a, "centreline_km"] - em.loc[b, "centreline_km"])
                if 2.0 <= ratio <= 4.0 and max(pa, pb) / min(pa, pb) >= 3.0 and \
                        (best is None or (dcl, abs(ratio - 2.5)) < best[8:]):
                    best = (ratio, a, b, st, ga * SEV, gb * SEV, pa * SEV, pb * SEV, dcl, abs(ratio - 2.5))
    check("TWIN two earlier moves alike on every visible field, gains two to one or more apart", best is not None,
          "%s/%s %s: gain %.2f vs %.2f, own %.2f vs %.2f t a lane-km" % best[1:8] if best else "")
    check("TWIN the pair's gains run against their Priority 2 salt",
          best is not None and (best[4] - best[5]) * (best[6] - best[7]) < 0, "")

    # ------------------------------------------------------------------------------------------ semantic forks
    proc = txt[P.F_PROC].replace("\n", " ")
    plan = txt[P.F_PLAN].replace("\n", " ")
    rev = P_.rev
    late = rev[(rev["field"] == "PRIORITY") & (rev["effective_date"] > "2026-03-31")]
    check("SF1 the change since the last winter closed is the redesign alone, only its salt above the rollover",
          "approved since the last winter closed" in proc and len(late) == 216 and
          set(late["effective_date"]) == {"2026-08-30"}, "%d entries" % len(late))
    gross = g + x0 * L * SEV
    check("SF2 over what they needed before: their whole Priority 1 salt files another figure",
          "over what they needed before it" in proc and call(gross) != GOLD and call(gross + 0) >= 2800,
          "%.1f t" % gross)
    check("SF3 the 424 lane-km are the register's lane_km; centreline rates are off the plan's per lane-km basis",
          abs(L - 424.0) < 1e-6 and call(gc) != GOLD and
          "application rates, which are set in kilograms per lane-km" in plan, "centreline throughout %.1f t" % gc)
    col_ids = set(P_.reg.loc[P_.reg["func_class"] == "COLLECTOR", "segment_id"])
    pc = ps[ps["segment_id"].isin(col_ids)].copy()
    loc = pc["entry_utc"].dt.tz_convert("America/Toronto").dt.tz_localize(None)
    near = 0
    for yr in range(2023, 2027):
        for b in (dt.datetime(yr, 11, 1), dt.datetime(yr, 4, 1), dt.datetime(yr, 10, 1)):
            near += int(((loc - b).abs() < pd.Timedelta(hours=6)).sum())
            near += int(((pc["entry_utc"].dt.tz_convert(None) - b).abs() < pd.Timedelta(hours=6)).sum())
    octo = int(((loc.dt.month == 10) | (loc.dt.month == 4)).sum())
    check("SF4 the winter by local date, by UTC or from the supply season's 1 October: same call",
          near == 0 and octo == 0 and call(gu) == GOLD, "%d near, %d in October or April" % (near, octo))
    check("SF5 the planning severity is filed: 61.7 WSI points",
          "Material planning uses the planning severity of 61.7 WSI points" in plan and
          call(g * last / SEV) != GOLD and call(g * wmean / SEV) != GOLD, "")
    ctrl = P_.reg[(P_.reg["func_class"] == "COLLECTOR") & (P_.reg["priority"] == "2")]
    ws_ = np.array([P_.wsi[w] for w in K.WINTERS])
    st_ = np.array([sum(float(P_.salt.get((s, w), 0.0)) for s in ctrl["segment_id"]) for w in K.WINTERS])
    bi = np.polyfit(ws_, st_, 1)
    check("SF6 salt against severity: in proportion (the never-moved collectors' intercept near nil)",
          abs(bi[1]) / st_.mean() < 0.03, "intercept %.1f t of %.1f" % (bi[1], st_.mean()))
    check("SF7 the collectors carry rock salt only (RS), no sand and salt mix",
          set(pc["material_code"]) == {"RS"} and set(legc["MATL"]) == {"SALT"}, "")
    qrt = pd.read_excel(os.path.join(TARGET, P.F_QRT), header=3)
    reg_new = P_.reg[P_.reg["segment_id"].isin(set(nn["segment_id"]))]
    by_street = set(qrt["Street"])
    check("SF8 the transit agency's street list covers exactly the revision log's 30 August segments",
          by_street == set(reg_new["street"]) and
          set(P_.reg[P_.reg["street"].isin(by_street) & (P_.reg["func_class"] == "COLLECTOR") &
                     (P_.reg["frequent_transit"].fillna("").str.match(r"^(41|43|46|48|52|55|57|61|64)"))]["segment_id"])
          == set(nn["segment_id"]), "%d streets" % len(by_street))
    dic = pd.read_excel(os.path.join(TARGET, P.F_DICT), sheet_name="Fields")
    kg = dic[(dic["File"] == P.F_LEGACY) & (dic["Field"] == "KG")]["Description"].iloc[0]
    check("SF9 the legacy export's KG field is filed in kilograms", "kilograms" in kg, kg)
    check("SF10 the total rounded once, or the gain per lane-km rounded first: same call",
          call(r1(gain) * L) == GOLD and "rounded to the nearest 100 t" in proc, "%.1f t" % (r1(gain) * L))
    moves_all = rev[(rev["field"] == "PRIORITY") & (rev["old_value"] == "2") & (rev["new_value"] == "1")]
    check("SF11 the earlier moves are every collector moved 2 to 1 before the redesign (transit only is a rung)",
          len(moves_all) == N_MOVES + 216 and call(C.r2_pooled(P_, "QRT Route")) != GOLD, "%d entries" % len(moves_all))

    # ------------------------------------------------------------------------------------------ Ask A
    Yd = Y.Yards(W, S)
    pr = P.pass_rows(W, S)
    P2.settle_arterial_edges(W, S, pr)
    P2.settle_dome_edges(Yd)
    gs, gr = C.ask_a(TARGET)
    check("ASK A the golden equals the clean truth (stock on 1 November, every dome)",
          all(abs(gs[y] - Yd.stock[y]) < 1e-6 for y in K.YARDS), str({y: r1(gs[y]) for y in K.YARDS}))
    cap = pd.read_csv(os.path.join(TARGET, P.F_DOMES)).set_index("yard")["rated_capacity_t"]
    check("ASK A room is capacity less stock, every dome has room", all(abs(gr[y] - (cap[y] - gs[y])) < 1e-9 and
                                                                     gr[y] > 0 for y in K.YARDS), "")
    ea = min(min(K.bin_edge_distance(gs[y], 0.1), K.bin_edge_distance(gr[y], 0.1)) for y in K.YARDS)
    check("ASK A every figure clear of its rounding edge", ea >= ASK_EDGE, "%.4f t" % ea)
    stopsA = {"day_after": K.YARDS, "day_after_dome": K.YARDS, "day_whole": K.YARDS, "utc_local": K.YARDS,
              "sheets": K.YARDS, "supplier_only": ["MPF", "RDG", "LKS"], "first_issue": ["KLV", "MPF", "RDG"]}
    for m, want in stopsA.items():
        s_, r_ = C.ask_a(TARGET, m)
        moved = [y for y in K.YARDS if r1(s_[y]) != r1(gs[y])]
        gap = min(abs(s_[y] - gs[y]) for y in want)
        check("ASK A the %s route moves %s" % (m, ",".join(want)), moved == want and gap >= 0.15,
              "smallest %.1f t" % gap)
    hit = 0
    for f in np.arange(0.50, 0.95, 0.001):
        hit = max(hit, sum(1 for y in K.YARDS if r1(cap[y] * f) == r1(gs[y])))
    check("ASK A no single fill share of capacity recovers more than one dome", hit <= 1, "%d" % hit)

    # ------------------------------------------------------------------------------------------ Ask B
    ga = C.arterial_salt(TARGET)
    cells = P2.arterial_cells(W, S, pr)
    check("ASK B the golden equals the records' own arterial salt (runs once, brine off, contractor in)",
          all(abs(ga[k] - cells[k]) < 1e-6 for k in ga), "")
    truthB = {}
    for p in list(S.passes) + list(S.patrols):
        if p["kind"] != "ART":
            continue
        for rr in p["rows"]:
            w = K.winter_of(rr["entry"].date())
            if w in K.NEW_WINTERS:
                key = (p["route_code"][:3], w)
                truthB[key] = truthB.get(key, 0.0) + rr["t"]
    dB = max(abs(ga[k] - truthB.get(k, 0.0)) for k in ga)
    check("ASK B the golden within a tonne of the simulated truth in every cell", dB < 1.0, "%.3f t" % dB)
    eb = min(K.bin_edge_distance(v, 1.0) for v in ga.values())
    check("ASK B every figure 0.3 t or more from its whole-tonne rounding edge", eb >= 0.3, "%.3f t" % eb)
    gp = C.arterial_salt(TARGET, "prewet_rate")
    check("ASK B the salt read back from the brine at 40 litres a tonne files the same whole tonnes (C1)",
          all(round(gp[k]) == round(ga[k]) for k in ga), "largest gap %.3f t" % max(abs(gp[k] - ga[k]) for k in ga))
    art = ps[ps["route_code"].str.contains("-A") & (ps["material_code"] == "RS")].copy()
    art["day"] = art["entry_utc"].dt.tz_convert("America/Toronto").dt.date
    m410 = [W.controller_on(u, d) == "M410" for u, d in zip(art["unit_id"], art["day"])]
    art["m410"] = m410
    r720 = art[~art["m410"]]
    r410 = art[art["m410"]]
    check("ASK B newer controllers' rows carry 40 litres a tonne exactly, older ones about 38.2 (salt and brine)",
          (abs(r720["prewet_l"] - 40.0 * r720["applied_t"]) <= 0.051).all() and
          abs(float((r410["prewet_l"] / r410["applied_t"]).median()) - 40.0 / (1 + 40.0 * 1.18 / 1000)) < 0.05,
          "%.2f" % float((r410["prewet_l"] / r410["applied_t"]).median()))
    runs = r410.groupby("run_ref")["applied_t"].nunique()
    check("ASK B every older-controller run repeats one total on each of its rows", (runs == 1).all(),
          "%d runs" % len(runs))
    two = [(y, w) for y in ("KLV", "MPF") for w in K.NEW_WINTERS]
    stopsB = {"rows": list(ga), "runs_once": list(ga), "net_brine": list(ga), "no_contract": two,
              "register_yard": two, "utc_season": [("LKS", "2024-25"), ("RDG", "2025-26")]}
    for m, want in stopsB.items():
        a_ = C.arterial_salt(TARGET, m)
        moved = sorted(k for k in ga if round(a_[k]) != round(ga[k]))
        gap = min(abs(a_[k] - ga[k]) for k in want)
        check("ASK B the %s route moves %d figures" % (m, len(want)), moved == sorted(want) and gap >= 1.5,
              "smallest %.1f t" % gap)
    lk = P_.reg[P_.reg["func_class"] == "ARTERIAL"].copy()
    lk["y"] = lk["route_code"].str[:3]
    tot_l = lk["lane_km"].sum()
    blind = 0
    for w in K.NEW_WINTERS:
        rate_ = sum(ga[(y, w)] for y in K.YARDS) / tot_l
        for y in K.YARDS:
            blind += int(round(rate_ * lk.loc[lk["y"] == y, "lane_km"].sum()) == round(ga[(y, w)]))
    check("ASK B one network rate times each yard's arterial lane-km recovers no cell", blind == 0, "%d" % blind)

    # ------------------------------------------------------------------------------------------ the cracker
    cr = CR.main(TARGET, quiet=True)
    check("CRACKER pair ceiling 40 or under", cr["pair"] <= 40.0, "%.1f" % cr["pair"])
    check("CRACKER mirror leakage under 35 per cent of ask weight", cr["leak"] < 35.0, "%.1f" % cr["leak"])
    check("CRACKER the most obvious single device cracked keeps the pair at 40 or under", cr["worst"] <= 40.0,
          "%.1f" % cr["worst"])

    # ------------------------------------------------------------------------------------------ separation
    fl = pd.read_csv(os.path.join(TARGET, P.F_FLEET), dtype=str)
    old = fl[(fl["spreader_controller"] == "M410") | fl["controller_retrofit"].notna()]
    check("SEPARATION every older-controller unit runs an arterial circuit", old["home_circuit"].str.contains("-A").all()
          and ps[ps["unit_id"].isin(set(old["unit_id"]))]["route_code"].str.contains("-A").all(), "%d units" % len(old))
    check("SEPARATION the collectors spread dry salt (no brine on any collector row)",
          int(pc["prewet_l"].sum()) == 0, "")
    xw = pd.read_csv(os.path.join(TARGET, P.F_XWALK), dtype=str)
    split = set(xw.loc[xw["change"] == "SPLIT", "segment_id"])
    check("SEPARATION no collector segment the call reads is split by the crosswalk",
          not (split & (set(d["segment_id"]) | set(nn["segment_id"]))), "%d split" % len(split))
    con = P_.reg[P_.reg["operator"] == "CONTRACT"]
    yardch = rev[rev["field"].isin(["YARD", "OPERATOR"])].merge(P_.reg[["segment_id", "func_class"]], on="segment_id")
    check("SEPARATION the contractor and the realignment touch arterials only",
          set(con["func_class"]) == {"ARTERIAL"} and set(yardch["func_class"]) == {"ARTERIAL"}, "")
    asks_files = [P.F_SCALE, P.F_DISPATCH1, P.F_DISPATCH2, P.F_SURVEY, P.F_DOMES, P.F_LOADING, P.F_PELLARD, P.F_FLEET]
    tmp = linked_copy(asks_files)
    try:
        g_del = C.golden(C.Pack(tmp))
    finally:
        shutil.rmtree(tmp)
    check("SEPARATION the golden reads none of the asks' files (deleted: unchanged)", abs(g_del - g) < 1e-9, "")
    check("SEPARATION Ask B reads arterial route codes only, Ask A no AVL row", True,
          "by construction in calc.arterial_salt and calc.ask_a")

    # ------------------------------------------------------------------------------------------ input gates
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(TARGET))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    check("GATES ten or more files", len(files) >= 10, "%d" % len(files))
    check("GATES three or more formats", len(fmts) >= 3, str(sorted(fmts)))
    check("GATES a file of 25,000 rows or more", meta["input_gates"]["largest_file_rows"] >= 25000,
          "%s %d" % (meta["input_gates"]["largest_file"], meta["input_gates"]["largest_file_rows"]))
    dis = meta["distractor_files"]
    check("GATES two distractors, shipped, none named as such", len(dis) >= 2 and all(x in files for x in dis) and
          not any("distract" in x.lower() for x in files), str(dis))
    tmp = linked_copy(dis)
    try:
        Pd = C.Pack(tmp)
        same = abs(C.golden(Pd) - g) < 1e-9 and C.ask_a(tmp) == (gs, gr) and C.arterial_salt(tmp) == ga
    finally:
        shutil.rmtree(tmp)
    check("DISTRACTORS deleted: the golden and both asks unchanged", same, "")
    man = pd.read_csv(os.path.join(TARGET, P.F_MANIFEST), dtype=str)
    check("REGISTERS the manifest lists every shipped file but itself (set equality)",
          set(man["file"]) == set(files) - {P.F_MANIFEST}, str(sorted(set(files) - set(man["file"]))))
    dic_files = set(dic["File"])
    data_files = {f for f in files if f.endswith((".csv", ".parquet", ".xlsx"))} - {P.F_DICT}
    check("REGISTERS the dictionary covers every shipped data file (set equality)", dic_files == data_files,
          str(sorted(data_files ^ dic_files)))
    check("GATES every shipped file has a source, a date and a licence in metadata.json",
          sorted(x["path"] for x in meta["files"]) == files and all(x["source"] and x["date"] and x["license"]
                                                                   for x in meta["files"]), "")

    # ------------------------------------------------------------------------------------------ realism
    dash = [f for f, t in txt.items() if "—" in t or "–" in t]
    check("REALISM no shipped file carries an em or en dash", not dash, str(dash))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    pt = os.path.join(TASK, "prompt.txt")
    prompt = open(pt, encoding="utf-8").read() if os.path.exists(pt) else ""
    check("REALISM the submission and prompt carry no em or en dash",
          not any(c in sub + prompt for c in ("—", "–")), "")
    alltxt = " ".join(txt.values())
    check("REALISM every persona from guard.py names appears, and no placeholder identity",
          all(n in alltxt for n in K.PEOPLE.values()) and
          not re.search(r"John Doe|Jane Doe|Acme|Company [AB]\b|Lorem|Example Corp", alltxt), "")
    tot_rs = float(ps.loc[ps["material_code"] == "RS", "applied_t"].sum())
    check("REALISM no round headline totals (platform rock salt, WSI, ask figures)",
          abs(tot_rs - round(tot_rs, -1)) > 0.5 and all(abs(v - round(v)) > 0.01 for v in list(ga.values()) +
                                                         list(gs.values())), "%.1f t" % tot_rs)
    tk = []
    for y in K.YARDS:
        df = pd.read_excel(os.path.join(TARGET, P.F_SCALE), sheet_name=y, dtype=str)
        tk += list(df["Ticket"])
    check("REALISM scale tickets unique across the four scale houses", len(tk) == len(set(tk)), "%d" % len(tk))
    units = set(fl["unit_id"])
    check("REALISM every unit in the passes is in the fleet list", set(ps["unit_id"]) <= units, "")
    tr = pd.read_excel(os.path.join(TARGET, P.F_SCALE), sheet_name="RDG", dtype=str)
    unit_tr = set(tr.loc[tr["Carrier"] == "CITY OF QUELLBROOK", "Vehicle"].str.replace("Unit ", ""))
    check("REALISM the transfer truck is a Ridge unit in the fleet list",
          unit_tr <= set(fl.loc[fl["yard"] == "RDG", "unit_id"]), str(unit_tr))
    rcount = rev[rev["field"] == "PRIORITY"]["reason"].value_counts()
    check("REALISM revision reasons are the audit's own batches (no reason on more than one move date)",
          all(rev[rev["reason"] == r_]["effective_date"].nunique() <= 30 for r_ in rcount.index), "")
    lagd = (pd.to_datetime(rev["effective_date"]) - pd.to_datetime(rev["entered_on"])).dt.days
    check("REALISM route audit entries lag their effective dates unevenly, some entered after",
          lagd.min() < 0 and lagd.max() - lagd.min() >= 40, "%d to %d days" % (lagd.min(), lagd.max()))
    upc = ps.groupby(["route_code"])["unit_id"].nunique()
    check("REALISM trucks rotate: most circuits run by more than one unit over the three winters",
          (upc > 1).mean() > 0.5, "%.0f per cent of circuits" % (100 * (upc > 1).mean()))

    # ------------------------------------------------------------------------------------------ dates
    end_local = ps["exit_utc"].dt.tz_convert("America/Toronto").max()
    check("DATES the platform export ends before the 24 September pull window",
          end_local.tz_localize(None) < pd.Timestamp("2026-09-24"), str(end_local))
    sc_max = max(pd.read_excel(os.path.join(TARGET, P.F_SCALE), sheet_name=y)["Date"].max() for y in K.YARDS)
    check("DATES the scale houses' last weighing on 24 September", str(sc_max)[:10] == "2026-09-24", str(sc_max))
    check("DATES the revision log entered no later than the register date",
          rev["entered_on"].max() <= "2026-09-14" and rev["effective_date"].max() <= "2026-09-14", "")
    d1 = pd.read_csv(os.path.join(TARGET, P.F_DISPATCH2))
    check("DATES only the supplier's dispatch schedules carry dates after the pull (forward bookings)",
          d1["delivery_date"].min() >= "2026-10-01", "")
    check("DATES every document issued before the pull",
          max(D.PLAN_DATE, D.PROC_DATE, D.SURVEY_DATE) <= K.AS_OF and "Issued 18 September 2026" in plan and
          "issued 16 September 2026" in txt[P.F_SURVEY].replace("\n", " ") and "Approved 12 May 2025" in proc, "")
    sv_ = C.survey(TARGET)
    ok_cap = all(7 <= (sv_[y]["capture_end_utc"] - dt.timedelta(hours=4)).hour <= 9 and
                 sv_[y]["capture_end_utc"].date() == Y.SURVEY_DAY[y] for y in K.YARDS)
    check("DATES each survey capture ends in the morning of its survey day, local", ok_cap, "")

    # ------------------------------------------------------------------------------------------ documents read back
    check("DOCS the procedure files the estimand (4.2), positive control on the same extractor",
          "the additional rock salt the roads the change moves will need from 1 November to 31 March" in proc and
          "Road salt procurement" in proc, "")
    check("DOCS the plan files the Priority 2 service level and the dome stock rule",
          "Salted at intersections, hills and curves during and after each event" in plan and
          "brought forward by the loads weighed in to it and out of it at the scale houses" in plan, "")
    check("DOCS the plan files the pre-wet brine and its weight", "1.18 kg a litre" in plan, "")
    check("DOCS the survey report's stock table reads back", all(abs(sv_[y]["stock"] - Y.SURVEY_STOCK[y]) < 1e-9
                                                                 for y in K.YARDS), "")

    n_fail = sum(1 for _l, ok, _d in RESULTS if not ok)
    print("\n%d checks, %d failed" % (len(RESULTS), n_fail))
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
