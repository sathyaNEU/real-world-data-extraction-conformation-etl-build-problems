#!/usr/bin/env python3
"""task122 independent verifier.

Reads only the shipped bytes under target/ and recomputes, on its own code path (no import from the
generator), every rung of the ladder, the rival-killers (the archive back-test and the twin tests),
the guardrail, floor and bar conditions, the decomposition by both routes, and every graded figure:
the call, the runner-up and the gap, the 48 fee cells of ask 1 and the 12 slot totals of ask 2.
The constants it needs (thresholds, tariff, slot dates, gating) are read from the shipped documents.

    python3 task122/generator/verify_pack.py <task folder or target folder> [--record build_record.json] [--out v.json]

Exit status 0 only if every check passes and, with --record, every figure agrees with the build record.
"""
import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

RANKERS_ORDER = None   # filled from the register
CELL_LABELS = ["app 0-29", "app 30-179", "app 180-729", "app 730+", "web 0-29", "web 30-179", "web 180-729",
               "web 730+"]


class V:
    def __init__(self):
        self.rows = []

    def check(self, cond, name, detail=""):
        self.rows.append((name, bool(cond), str(detail)[:240]))
        return bool(cond)


def find(tgt, prefix, ext):
    hits = [f for f in os.listdir(tgt) if f.startswith(prefix) and f.endswith(ext)]
    if len(hits) != 1:
        raise SystemExit(f"expected one {prefix}*{ext} in {tgt}, found {hits}")
    return os.path.join(tgt, hits[0])


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def docx_text(path):
    from docx import Document
    return re.sub(r"\s+", " ", " ".join(p.text for p in Document(path).paragraphs))


# ---------------------------------------------------------------------------------------------- rules

def read_rules(tgt):
    ch = pdf_text(find(tgt, "experimentation_charter", ".pdf"))
    r = {}
    r["bar"] = float(re.search(r"its lift is at least (\d+(?:\.\d+)?)", ch).group(1))
    r["guard_pct"] = float(re.search(r"more than (\d+(?:\.\d+)?) per cent below the incumbent", ch).group(1))
    r["reproduce"] = float(re.search(r"within (\d+(?:\.\d+)?) extra orders", ch).group(1))
    r["slot_share"] = float(re.search(r"takes (\d+) per cent of logged-in carousel sessions", ch).group(1)) / 100
    r["slot_weeks"] = {"twelve": 12}[re.search(r"on each platform for (\w+) weeks", ch).group(1)]
    edges = re.search(r"Tenure 0 to (\d+) days (\d+) to (\d+) days (\d+) to (\d+) days (\d+) days and over", ch)
    r["band_lo"] = [0, int(edges.group(2)), int(edges.group(4)), int(edges.group(6))]
    cm = docx_text(find(tgt, "fresh_listing_commitment", ".docx"))
    m = re.search(r"at least (\d+) of every 100 tiles it serves go to listings under (\d+) hours old", cm)
    r["floor"], r["fresh_h"] = float(m.group(1)), float(m.group(2))
    r["floor_unit"] = "per served ranking" if "count per served ranking" in cm else "rendered"
    cap = re.sub(r"\s+", " ", open(find(tgt, "test_capacity_and_release_gating", ".md"), encoding="utf-8").read())
    m = re.search(r"slot runs from (\d+) (\w+) to (\d+) (\w+) (\d{4})", cap)
    r["slot_start"] = datetime.strptime(f"{m.group(1)} {m.group(2)} {m.group(5)}", "%d %B %Y").date()
    r["cell_by_cell"] = "cell by cell" in cap
    r["one_year_before"] = "same ISO weeks one year before the slot" in cap
    ics = open(find(tgt, "app_release_calendar", ".ics"), encoding="utf-8").read()
    rel = []
    for ev in ics.split("BEGIN:VEVENT")[1:]:
        d = re.search(r"DTSTART;VALUE=DATE:(\d{8})", ev).group(1)
        if re.search(r"SUMMARY:App release", ev):
            rel.append(datetime.strptime(d, "%Y%m%d").date())
    r["app_start"] = min(d for d in rel if d >= r["slot_start"])
    # the tariff in force for the slot: the newest register row the pricing committee approved
    tar = pd.read_csv(find(tgt, "kopersbescherming", ".csv"))
    minutes = docx_text(find(tgt, "pricing_committee_minutes", ".docx"))
    deferred = {m.group(1) for m in re.finditer(r"(KB-\d{4}-\d{2})", minutes)
                if "deferred" in minutes[m.end():m.end() + 600]}
    tar["start"] = pd.to_datetime(tar.ingangsdatum).dt.date
    live = tar[(tar.start <= r["slot_start"]) & ~tar.tarief_id.isin(deferred)].sort_values("start")
    row = live.iloc[-1]
    r["tariff_fixed"], r["tariff_pct"] = float(row.vast_bedrag_eur), float(row.percentage_van_artikelprijs) / 100
    r["tariff_id"] = row.tarief_id
    jan = tar[tar.start <= r["slot_start"]].sort_values("start").iloc[-1]
    r["tariff_jan_fixed"] = float(jan.vast_bedrag_eur)
    terms = pdf_text(find(tgt, "buyer_protection_terms", ".pdf"))
    r["fee_on_price_paid"] = "percentage of the price you pay for the item, after any accepted offer" in terms
    r["in_person_no_fee"] = "pay the seller directly, the purchase is not covered and no Buyer Protection fee" in terms
    rl = open(find(tgt, "analytics_release_log", ".md"), encoding="utf-8").read()
    r["r2_replaces"] = "R2 replaces the first release" in rl
    reg = json.load(open(find(tgt, "ranking_policy_register", ".json"), encoding="utf-8"))
    r["incumbent"] = [p["policy_id"] for p in reg["policies"] if p["status"] == "production"][0]
    r["policies"] = [p["policy_id"] for p in reg["policies"] if p["status"] == "registered"]
    r["names"] = {p["policy_id"]: p["name"] for p in reg["policies"]}
    return r


# ---------------------------------------------------------------------------------------------- data

def band_of(days, lo):
    return np.searchsorted(np.array(lo[1:]), np.asarray(days), side="right")


def load(tgt, rules):
    R = pd.read_csv(find(tgt, "home_carousel_render_log", ".csv"), dtype={"ordered_tiles": str},
                    keep_default_na=False)
    R["k"] = R.ordered_tiles.str.split().str.len().fillna(0).astype(int)
    R.loc[R.ordered_tiles == "", "k"] = 0
    g = R.groupby("session_id", sort=True)
    S = pd.DataFrame({"platform": g.platform.first(), "tenure": g.buyer_tenure_days.first(),
                      "ranker": g.ranker.first(), "p": g.propensity.first(), "n": g.size(),
                      "y": g.k.first(), "ynuniq": g.k.nunique(), "pnuniq": g.propensity.nunique(),
                      "rnuniq": g.ranker.nunique()}).reset_index()
    S["cell"] = np.where(S.platform == "app", 0, 4) + band_of(S.tenure, rules["band_lo"])
    SR = pd.read_parquet(find(tgt, "home_carousel_served_rankings", ".parquet"))
    S = S.merge(SR, on="session_id", how="left", validate="one_to_one")
    O = pd.read_parquet(find(tgt, "orders_enrolled_buyers", ".parquet"))
    PM = pd.read_parquet(find(tgt, "payments_buyer_protection", ".parquet"))
    OF = pd.read_csv(find(tgt, "offers_accepted", ".csv"), parse_dates=["offered_at", "accepted_at", "expires_at"])
    return R, S, O, PM, OF


def window_orders(S, O, days=21, cal=False):
    m = O.merge(S[["buyer_id", "session_id", "started_at"]].rename(columns={"session_id": "sid"}),
                on="buyer_id", how="inner")
    dt = (m.ordered_at - m.started_at).dt.total_seconds()
    if cal:
        dd = (m.ordered_at.dt.normalize() - m.started_at.dt.normalize()).dt.days
        return m[(dt >= 0) & (dd <= days)]
    return m[(dt >= 0) & (dt <= days * 86400)]


def per_session(S, m, values=None):
    v = pd.Series(1.0 if values is None else values, index=m.index)
    s = v.groupby(m.sid).sum()
    return S.session_id.map(s).fillna(0.0).to_numpy()


# ---------------------------------------------------------------------------------------------- estimators

def levels(S, y, how, rankers):
    out = {}
    N = len(S)
    for r in rankers:
        g = (S.ranker == r).to_numpy()
        yy, p, n = y[g], S.p.to_numpy()[g], S.n.to_numpy()[g]
        if how == "replay_rows":
            out[r] = (yy * n).sum() / n.sum()
        elif how == "render_weights":
            out[r] = (yy * n / p).sum() / (n / p).sum()
        elif how == "session_weights":
            out[r] = (yy / p).sum() / N
        elif how == "session_weights_selfnorm":
            out[r] = (yy / p).sum() / (1 / p).sum()
        elif how == "session_weights_clipped":
            out[r] = (yy / np.maximum(p, 0.05)).sum() / N
        elif how == "within_cell":
            out[r] = sum((S.cell == c).sum() / N * yy[(S.cell.to_numpy()[g] == c)].mean() for c in range(8))
        elif how == "replay_sessions":
            out[r] = yy.mean()
    return out


def lifts(S, y, how, inc, pol):
    lv = levels(S, y, how, [inc] + pol)
    return {r: (lv[r] - lv[inc]) * 1000 for r in pol}


def cell_rates(S, y, rankers, render_weighted=False):
    out = {}
    for c in range(8):
        cm = (S.cell == c).to_numpy()
        for r in rankers:
            g = cm & (S.ranker == r).to_numpy()
            n = S.n.to_numpy()[g]
            out[(r, c)] = ((y[g] * n).sum() / n.sum() if render_weighted else y[g].mean()) * 1000
    return out


def guard(S, y_basis, y_in, inc, pol, grain, render_weighted):
    base = cell_rates(S, y_in, [inc], render_weighted)
    val = cell_rates(S, y_basis, [inc] + pol, render_weighted)
    Nc = np.array([(S.cell == c).sum() for c in range(8)], float)
    groups = {"eight": {c: [c] for c in range(8)}, "platform": {"app": [0, 1, 2, 3], "web": [4, 5, 6, 7]},
              "tenure": {b: [b, b + 4] for b in range(4)}, "pooled": {"all": list(range(8))}}[grain]
    out = {}
    for r in pol:
        for key, cs in groups.items():
            w = Nc[cs] / Nc[cs].sum()
            d = sum(wi * (val[(r, c)] - val[(inc, c)]) for wi, c in zip(w, cs))
            b = sum(wi * base[(inc, c)] for wi, c in zip(w, cs))
            out[(r, key)] = 100 * d / b
    return out


def floors(S, rankers, fresh_h):
    ages = S[[f"tile_{i}_age_h" for i in range(1, 7)]].to_numpy()
    f = (ages < fresh_h).sum(axis=1)
    n, p = S.n.to_numpy(), S.p.to_numpy()
    out = {}
    for r in rankers:
        g = (S.ranker == r).to_numpy()
        out[(r, "per_ranking")] = 100 * f[g].sum() / (6 * g.sum())
        out[(r, "rendered")] = 100 * (f[g] * n[g]).sum() / (6 * n[g].sum())
        out[(r, "rendered_w")] = 100 * (f[g] * n[g] / p[g]).sum() / (6 * (n[g] / p[g]).sum())
    return out


def screen(S, y_basis, y_in, how, grain, floor_key, rules, inc, pol):
    val = lifts(S, y_basis, how, inc, pol)
    rw = how in ("replay_rows", "render_weights")
    g = guard(S, y_basis, y_in, inc, pol, grain, rw)
    keys = range(8) if grain == "eight" else ("app", "web")
    fl = floors(S, pol, rules["fresh_h"])
    ok = {r: all(g[(r, k)] >= -rules["guard_pct"] for k in keys) and fl[(r, floor_key)] >= rules["floor"]
          and val[r] >= rules["bar"] for r in pol}
    elig = sorted([r for r in pol if ok[r]], key=lambda r: -val[r])
    first = elig[0] if elig else None
    second = elig[1] if len(elig) > 1 else None
    margin = val[first] / val[second] if second else float("inf")
    return val, ok, first, second, margin


def nbin(x, unit):
    return np.floor(x / unit + 0.5)


def bin_clear(x, unit):
    k = nbin(x, unit)
    return min(x - (k - 0.5) * unit, (k + 0.5) * unit - x)


# ---------------------------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--record")
    ap.add_argument("--out")
    a = ap.parse_args()
    tgt = a.folder if os.path.basename(os.path.normpath(a.folder)) == "target" else os.path.join(a.folder, "target")
    v = V()
    out = {}
    rules = read_rules(tgt)
    out["rules"] = {k: (str(x) if isinstance(x, date) else x) for k, x in rules.items() if k != "names"}
    inc, pol = rules["incumbent"], rules["policies"]
    v.check(all(rules[k] for k in ("cell_by_cell", "one_year_before", "fee_on_price_paid", "in_person_no_fee",
                                   "r2_replaces")) and rules["tariff_id"] == "KB-2026-02" and len(pol) == 6,
            "rules.read_from_documents", {k: rules[k] for k in ("tariff_id", "app_start", "slot_start")})
    R, S, O, PM, OF = load(tgt, rules)
    v.check(len(R) >= 25_000 and len(S) == R.session_id.nunique(), "data.render_rows", len(R))
    v.check((S.ynuniq == 1).all() and (S.pnuniq == 1).all() and (S.rnuniq == 1).all(), "data.one_draw_per_session")
    v.check(S.buyer_id.is_unique, "data.one_session_per_buyer")
    # the render log's ordered tiles tie to the orders extract's carousel orders by session
    ins = O[O.channel == "carousel"].groupby("home_session_id").size()
    v.check((S.session_id.map(ins).fillna(0).astype(int) == S.y).all(), "tie.render_log_orders")
    y_in = S.y.to_numpy().astype(float)
    W21 = window_orders(S, O, 21)
    y_k = per_session(S, W21)
    # ------------------------------------------------------------------ rungs
    L = rules["names"]
    rung_def = [("replay_rows", "platform", "rendered", y_in),
                ("render_weights", "platform", "rendered_w", y_in),
                ("session_weights", "platform", "per_ranking", y_in),
                ("session_weights", "eight", "per_ranking", y_in),
                ("session_weights", "eight", "per_ranking", y_k)]
    rungs = []
    for how, grain, fk, yb in rung_def:
        val, ok, first, second, margin = screen(S, yb, y_in, how, grain, fk, rules, inc, pol)
        rungs.append(dict(estimator=how, guardrail=grain, basis="kept" if yb is y_k else "in-session",
                          values={r: round(x, 4) for r, x in val.items()}, leader=first, runner_up=second,
                          margin=round(margin, 4), qualifiers=[r for r in pol if ok[r]]))
    out["rungs"] = rungs
    want = ["HC-36", "HC-31", "HC-34", "HC-33", "HC-37"]
    for i, (rg, w) in enumerate(zip(rungs, want)):
        v.check(rg["leader"] == w and rg["margin"] >= 1.15, f"rung{i}.{w}", (rg["leader"], rg["margin"]))
    E_ = lifts(S, y_k, "session_weights", inc, pol)
    e, b = E_["HC-37"], E_["HC-33"]
    out["call"] = {"answer": rungs[4]["leader"], "answer_name": L[rungs[4]["leader"]], "lift": e,
                   "runner_up": rungs[4]["runner_up"], "runner_up_lift": b, "gap": e - b,
                   "filed": [round(e, 1), round(b, 1), round(e - b, 1)]}
    for nm, x in (("E", e), ("B", b), ("gap", e - b)):
        v.check(bin_clear(x, 0.1) >= 0.03, f"bin.{nm}", (x, bin_clear(x, 0.1)))
    # the session-grain estimators agree; the call holds under each
    for how in ("session_weights_selfnorm", "session_weights_clipped", "within_cell"):
        lv = lifts(S, y_k, how, inc, pol)
        v.check(all(abs(lv[r] - E_[r]) < 1e-9 for r in pol), f"session_grain.{how}")
    # ------------------------------------------------------------------ conditions in detail
    g8 = guard(S, y_in, y_in, inc, pol, "eight", False)
    out["guardrail_pct"] = {f"{r}|{CELL_LABELS[c]}": round(x, 3) for (r, c), x in g8.items()}
    breaches = sorted((r, c) for (r, c), x in g8.items() if x < -rules["guard_pct"])
    v.check(breaches == [("HC-31", 7), ("HC-34", 0)], "guardrail.breaches", breaches)
    gk = guard(S, y_k, y_in, inc, pol, "eight", False)
    v.check(sorted((r, c) for (r, c), x in gk.items() if x < -rules["guard_pct"]) == breaches,
            "guardrail.same_on_kept")
    fl = floors(S, pol, rules["fresh_h"])
    out["floors"] = {f"{r}|{k}": round(x, 3) for (r, k), x in fl.items()}
    v.check(fl[("HC-36", "per_ranking")] < rules["floor"] <= fl[("HC-36", "rendered")], "floor.D_counting_unit")
    v.check(all(fl[(r, "per_ranking")] >= rules["floor"] for r in pol if r != "HC-36"), "floor.others")
    v.check(E_["HC-39"] < rules["bar"] and all(E_[r] >= rules["bar"] for r in pol if r != "HC-39"), "bar.F_only")
    # ------------------------------------------------------------------ the decomposition, route 1 and route 2
    for d in (7, 10, 14, 21):
        yd = per_session(S, window_orders(S, O, d))
        ld = lifts(S, yd, "session_weights", inc, pol)
        v.check(all(abs(ld[r] - E_[r]) < 1e-9 for r in pol), f"route1.window_{d}d")
        yc = per_session(S, window_orders(S, O, d, cal=True))
        lc = lifts(S, yc, "session_weights", inc, pol)
        v.check(all(abs(lc[r] - E_[r]) < 1e-9 for r in pol), f"route1.calendar_{d}d")
    wl = S[["session_id", "buyer_id", "started_at", "watchlist_at_start"] + [f"tile_{i}" for i in range(1, 7)]]
    rows = []
    for sid, bid, st, wls, *tiles in wl.itertuples(index=False):
        if wls:
            ts = set(tiles)
            for x in wls.split():
                rows.append((sid, bid, st, int(x), int(x) in ts))
    WL = pd.DataFrame(rows, columns=["session_id", "buyer_id", "started_at", "listing_id", "shown"])
    mm = WL.merge(O[["buyer_id", "listing_id", "ordered_at", "channel", "home_session_id"]],
                  on=["buyer_id", "listing_id"], how="left")
    insess = (mm.channel == "carousel") & (mm.home_session_id == mm.session_id)
    later = ~insess & ((mm.ordered_at - mm.started_at).dt.total_seconds().between(1, 21 * 86400))
    q = float(later[~mm.shown].mean())
    wis = mm[insess].groupby("session_id").size()
    Sw = S.session_id.map(wis).fillna(0).to_numpy()
    r2 = lifts(S, y_in - q * Sw, "session_weights", inc, pol)
    out["route2"] = {"anyway_rate": q, "lifts": r2}
    v.check(all(abs(r2[r] - E_[r]) < 0.005 for r in pol), "route2.equals_route1",
            {r: (round(r2[r], 4), round(E_[r], 4)) for r in pol})
    # ------------------------------------------------------------------ the archive
    xa = pd.read_excel(find(tgt, "carousel_test_archive", ".xlsx"), sheet_name=None)
    T, AS = xa["tests"], xa["logged_sessions"]
    arch = {}
    for _, t in T.iterrows():
        d = AS[AS.test_id == t.test_id]
        N = len(d)
        te, co = d[d.arm == "test"], d[d.arm == "control"]
        sw = ((te.in_session_orders / te.propensity).sum() - (co.in_session_orders / co.propensity).sum()) / N * 1000

        def rw(x):
            return (x.in_session_orders * x.renders / x.propensity).sum() / (x.renders / x.propensity).sum()

        def rp(x):
            return (x.in_session_orders * x.renders).sum() / x.renders.sum()
        arch[t.test_id] = dict(realised=float(t.realised_lift), session=sw, render=(rw(te) - rw(co)) * 1000,
                               replay=(rp(te) - rp(co)) * 1000, published=float(t.offline_estimate_published))
    out["archive"] = arch
    tol = rules["reproduce"]
    hit = {k: sorted(t for t, x in arch.items() if abs(x[k] - x["realised"]) <= tol) for k in ("session", "render",
                                                                                              "replay")}
    out["archive_hits"] = {k: len(x) for k, x in hit.items()}
    v.check(len(hit["session"]) == 9, "archive.session_9_of_9")
    v.check(len(hit["render"]) == 6 and len(hit["replay"]) == 3, "archive.render_6_replay_3",
            (hit["render"], hit["replay"]))
    v.check(all(x[k] > x["realised"] for x in arch.values() for k in ("render", "replay")
                if abs(x[k] - x["realised"]) > tol), "archive.misses_overstate")
    v.check(all(round(x["replay"] + 1e-9, 1) == x["published"] for x in arch.values()), "archive.published_is_replay")
    cols = ["policy_family", "inputs", "logger_version", "traffic_share_pct", "duration_days", "cells_in_scope",
            "offline_estimate_published"]
    t3, t7 = T.set_index("test_id").loc["T3"], T.set_index("test_id").loc["T7"]
    v.check(all(t3[c] == t7[c] for c in cols) and t3.realised_lift / t7.realised_lift >= 2.0, "archive.twins")
    v.check(abs(arch["T7"]["session"] - arch["T7"]["realised"]) <= tol and
            abs(arch["T7"]["render"] - arch["T7"]["realised"]) > tol and
            abs(arch["T7"]["replay"] - arch["T7"]["realised"]) > tol, "archive.twin_T7_session_only")
    # ------------------------------------------------------------------ ask 1: fee per 1,000 sessions, per policy and cell
    o = W21.merge(PM, on="order_id", how="left")
    paid_through = o.payment_id.notna().to_numpy()
    price_paid = (o.amount_eur - o.shipping_eur - o.buyer_protection_fee_eur).round(2).to_numpy()
    fee = np.where(paid_through, rules["tariff_fixed"] + rules["tariff_pct"] * np.nan_to_num(price_paid), 0.0)
    o["fee"] = fee
    fee_s = S.session_id.map(o.groupby("sid").fee.sum()).fillna(0.0).to_numpy()
    ord_s = y_k
    cells_fee, cells_ord = {}, {}
    for c in range(8):
        cm = (S.cell == c).to_numpy()
        b0f = fee_s[cm & (S.ranker == inc).to_numpy()].mean()
        b0o = ord_s[cm & (S.ranker == inc).to_numpy()].mean()
        for r in pol:
            gm = cm & (S.ranker == r).to_numpy()
            cells_fee[(r, c)] = (fee_s[gm].mean() - b0f) * 1000
            cells_ord[(r, c)] = (ord_s[gm].mean() - b0o) * 1000
    out["ask1"] = {f"{r}|{CELL_LABELS[c]}": round(x, 4) for (r, c), x in cells_fee.items()}
    out["ask1_filed"] = {f"{r}|{CELL_LABELS[c]}": round(x, 1) for (r, c), x in cells_fee.items()}
    v.check(min(bin_clear(x, 0.1) for x in cells_fee.values()) >= 0.03, "ask1.mid_bin",
            min(bin_clear(x, 0.1) for x in cells_fee.values()))
    # every way of mishandling the three fee devices (pricing in-person pickups, the asking price, the
    # January tariff row) moves every cell out of its bin; so does the natural read (all three, in-session
    # orders only)
    asking = o.asking_price_eur.to_numpy()

    def grid_for(fees, mask=None):
        f = pd.Series(np.where(mask, fees, 0.0) if mask is not None else fees, index=o.index)
        fs = S.session_id.map(f.groupby(o.sid).sum()).fillna(0.0).to_numpy()
        out_ = {}
        for c in range(8):
            cm = (S.cell == c).to_numpy()
            base = fs[cm & (S.ranker == inc).to_numpy()].mean()
            for r in pol:
                out_[(r, c)] = (fs[cm & (S.ranker == r).to_numpy()].mean() - base) * 1000
        return out_
    big = list(cells_fee)          # every cell, the two under EUR 1.00 included
    combos = {}
    for p1 in (False, True):
        for hz2 in (False, True):
            for hz1 in (False, True):
                if not (p1 or hz2 or hz1):
                    continue
                fixed = rules["tariff_jan_fixed"] if hz1 else rules["tariff_fixed"]
                price = asking if hz2 else np.where(paid_through, np.nan_to_num(price_paid), asking)
                f_ = fixed + rules["tariff_pct"] * price
                if not p1:
                    f_ = np.where(paid_through, f_, 0.0)
                g_ = grid_for(f_)
                stay = [k for k in big if nbin(g_[k], 0.1) == nbin(cells_fee[k], 0.1)]
                combos[f"{int(p1)}{int(hz2)}{int(hz1)}"] = len(stay)
                v.check(not stay, f"ask1.devices_{int(p1)}{int(hz2)}{int(hz1)}_move_every_cell", stay)
                if p1 and hz2 and hz1:
                    insess = ((o.channel == "carousel") & (o.home_session_id == o.sid)).to_numpy()
                    gn = grid_for(f_, insess)
                    stay_n = [k for k in cells_fee if nbin(gn[k], 0.1) == nbin(cells_fee[k], 0.1)]
                    v.check(not stay_n, "ask1.natural_read_moves_every_cell", stay_n)
    out["ask1_cells_under_one_euro"] = [f"{r}|{CELL_LABELS[c]}" for (r, c), x in cells_fee.items() if abs(x) < 1.0]
    # the price paid read from the offers export agrees with the payments ledger
    x = o[paid_through].merge(OF, on=["buyer_id", "listing_id"], how="left")
    live = (x.accepted_at <= x.ordered_at) & (x.expires_at >= x.ordered_at)
    pp_off = np.where(live, x.offer_eur, x.asking_price_eur)
    pp_pay = (x.amount_eur - x.shipping_eur - x.buyer_protection_fee_eur).round(2)
    v.check(np.allclose(pp_off, pp_pay, atol=0.004), "ask1.price_paid_two_routes")
    # ------------------------------------------------------------------ ask 2: slot totals
    wk1 = pd.read_csv(find(tgt, "home_carousel_sessions_weekly_2025", ".csv"))
    wk2 = pd.read_csv(find(tgt, "home_carousel_sessions_weekly_R2", ".csv"))
    key = ["iso_week", "platform", "tenure_band"]
    cur = pd.concat([wk1[~wk1.set_index(key).index.isin(wk2.set_index(key).index)], wk2])
    slot_wk = [(rules["slot_start"] + timedelta(weeks=i)).isocalendar()[1] for i in range(rules["slot_weeks"])]
    app_wk = [w for w, i in zip(slot_wk, range(rules["slot_weeks"]))
              if rules["slot_start"] + timedelta(weeks=i) + timedelta(days=6) >= rules["app_start"]]
    prev = rules["slot_start"].year - 1
    band_lab = ["0-29", "30-179", "180-729", "730+"]
    arm = np.zeros(8)
    for c in range(8):
        plat = "app" if c < 4 else "web"
        wks = app_wk if plat == "app" else slot_wk
        labels = [f"{prev}-W{w:02d}" for w in wks]
        m = cur.iso_week.isin(labels) & (cur.platform == plat) & (cur.tenure_band == band_lab[c % 4])
        arm[c] = rules["slot_share"] * cur.loc[m, "logged_in_sessions"].sum()
    out["arm_sessions"] = arm.tolist()
    out["app_weeks"], out["web_weeks"] = app_wk, slot_wk
    tot_o = {r: sum(cells_ord[(r, c)] * arm[c] / 1000 for c in range(8)) for r in pol}
    tot_f = {r: sum(cells_fee[(r, c)] * arm[c] / 1000 for c in range(8)) for r in pol}
    out["ask2"] = {"orders": tot_o, "fee": tot_f,
                   "orders_filed": {r: int(nbin(x, 100) * 100) for r, x in tot_o.items()},
                   "fee_filed": {r: int(nbin(x, 100) * 100) for r, x in tot_f.items()}}
    v.check(min(bin_clear(x, 100) for x in list(tot_o.values()) + list(tot_f.values())) >= 20, "ask2.mid_bin")
    # stops: the first release, all weeks on the app, the pooled lift
    arm_r1 = np.zeros(8)
    for c in range(8):
        plat = "app" if c < 4 else "web"
        wks = app_wk if plat == "app" else slot_wk
        m = wk1.iso_week.isin([f"{prev}-W{w:02d}" for w in wks]) & (wk1.platform == plat) & \
            (wk1.tenure_band == band_lab[c % 4])
        arm_r1[c] = rules["slot_share"] * wk1.loc[m, "logged_in_sessions"].sum()
    for r in pol:
        t_r1 = sum(cells_ord[(r, c)] * arm_r1[c] / 1000 for c in range(8))
        v.check(nbin(t_r1, 100) != nbin(tot_o[r], 100), f"ask2.stop_first_release.{r}", (t_r1, tot_o[r]))
        t_pool = E_[r] * arm.sum() / 1000
        v.check(nbin(t_pool, 100) != nbin(tot_o[r], 100), f"ask2.stop_pooled.{r}", (t_pool, tot_o[r]))
    # ------------------------------------------------------------------ device separation from the call
    O2 = O.copy()
    O2["asking_price_eur"] = O2.asking_price_eur.sample(frac=1.0, random_state=7).to_numpy()
    y2 = per_session(S, window_orders(S, O2, 21))
    l2 = lifts(S, y2, "session_weights", inc, pol)
    v.check(all(abs(l2[r] - E_[r]) < 1e-12 for r in pol), "separation.prices_do_not_move_the_call")
    # ------------------------------------------------------------------ pack gates
    files = sorted(os.listdir(tgt))
    v.check(len(files) >= 10 and len({os.path.splitext(f)[1] for f in files}) >= 3, "gates.files_formats",
            (len(files), sorted({os.path.splitext(f)[1] for f in files})))
    meta_p = os.path.join(os.path.dirname(os.path.normpath(tgt)), "metadata.json")
    if os.path.exists(meta_p):
        meta = json.load(open(meta_p, encoding="utf-8"))
        dis = meta.get("distractor_files", [])
        v.check(len(dis) >= 2 and all(d in files for d in dis), "gates.distractors", dis)
        out["metadata_distractors"] = dis
    out["files"] = files
    # ------------------------------------------------------------------ compare with the build record
    if a.record:
        rec = json.load(open(a.record, encoding="utf-8"))
        v.check(abs(rec["call"]["lift"] - e) < 0.0006 and abs(rec["call"]["runner_up_lift"] - b) < 0.0006,
                "record.call", (rec["call"], e, b))
        lab = {"A": "HC-31", "B": "HC-33", "C": "HC-34", "D": "HC-36", "E": "HC-37", "F": "HC-39"}
        rec_cells = list(dict.fromkeys(k.split("|", 1)[1] for k in rec["ask1"]))      # the record's cell order
        diffs = [abs(rec["ask1"][f"{k}|{cl}"] - cells_fee[(lab[k], c)]) for k in lab for c, cl in enumerate(rec_cells)]
        v.check(max(diffs) < 0.0006, "record.ask1", max(diffs))
        d2 = [abs(rec["ask2"]["orders"][k] - tot_o[lab[k]]) for k in lab] + \
             [abs(rec["ask2"]["fee"][k] - tot_f[lab[k]]) for k in lab]
        v.check(max(d2) < 0.06, "record.ask2", max(d2))
        for i, rg in enumerate(rec["rungs"]):
            v.check(lab[rg["leader"]] == rungs[i]["leader"], f"record.rung{i}", (rg["leader"], rungs[i]["leader"]))
    out["checks"] = [{"name": n, "ok": ok, "detail": d} for n, ok, d in v.rows]
    failed = [n for n, ok, _ in v.rows if not ok]
    out["passed"], out["failed"] = len(v.rows) - len(failed), failed
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=1, default=lambda x: float(x) if isinstance(x, (np.floating, np.integer)) else str(x))
    print(f"verify_pack: {len(v.rows) - len(failed)} of {len(v.rows)} checks passed")
    print(f"call {out['call']['answer']} ({out['call']['answer_name']}) {e:.4f}; runner-up "
          f"{out['call']['runner_up']} {b:.4f}; gap {e - b:.4f}")
    if failed:
        print("FAILED:", failed)
        sys.exit(1)


if __name__ == "__main__":
    main()
