#!/usr/bin/env python3
"""task122 independent verifier.

Reads only the shipped bytes under target/ and recomputes, on its own code path (no import from the
generator), every rung of the ladder, the rival-killers (the archive back-test and the twin tests), the
guardrail on every count a reader can take (the render log's ordered tiles, the orders credited to the
session, every order placed from the session's tiles, the buyer's carousel orders over a window), the
floor and bar conditions, the decomposition by both routes, and every graded figure: the call, the
runner-up and the gap, the 48 fee cells of ask 1 and the 12 slot totals of ask 2, with the referee tie.
The constants it needs (thresholds, tariff, VAT, slot dates, gating) are read from the shipped documents, and the
checkout the slot runs on from the records: the date from which every pickup order carries a provider capture.

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
    cap = re.sub(r"\s+", " ", open(find(tgt, "slot_capacity_and_release_gating", ".md"), encoding="utf-8").read())
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
    # the tariff in force on the slot's dates: the register row whose effective date is the latest on or before the
    # slot's start, provided no row takes effect inside the slot; the register's newest row is a later proposal
    tar = pd.read_csv(find(tgt, "kopersbescherming", ".csv"))
    tar["start"] = pd.to_datetime(tar.ingangsdatum).dt.date
    m3 = re.search(r"to (\d+) (\w+) (\d{4}), twelve weeks", cap)
    r["slot_end"] = datetime.strptime(" ".join(m3.groups()), "%d %B %Y").date()
    row = tar[tar.start <= r["slot_start"]].sort_values("start").iloc[-1]
    r["tariff_fixed"], r["tariff_pct"] = float(row.vast_bedrag_eur), float(row.percentage_van_artikelprijs) / 100
    r["tariff_id"] = row.tarief_id
    r["tariff_changes_inside_slot"] = int(((tar.start > r["slot_start"]) & (tar.start <= r["slot_end"])).sum())
    newest = tar.sort_values("start").iloc[-1]
    r["tariff_latest_fixed"], r["tariff_latest_start"] = float(newest.vast_bedrag_eur), newest.start
    terms = pdf_text(find(tgt, "buyer_protection_terms", ".pdf"))
    r["fee_on_price_paid"] = "percentage of the price you pay for the item, after any accepted offer" in terms
    r["in_person_no_fee"] = "pay the seller directly, the purchase is not covered and no Buyer Protection fee" in terms
    r["balance_is_a_method"] = "your Vouwlijn balance" in terms
    r["rate_from_tiles"] = "orders placed from the carousel tiles it served" in ch
    fields = re.sub(r"\s+", " ", open(find(tgt, "carousel_logger_field_reference", ".md"), encoding="utf-8").read())
    r["seven_day_rule"] = "kept off it in their later sessions for seven days" in fields
    r["provider_captures_only"] = "card and iDEAL payment the payment provider captured" in fields
    fin = pd.read_excel(find(tgt, "finance_buyer_protection_fee_income", ".xlsx"), header=None)
    head = " ".join(str(x) for x in fin[0].iloc[:5])
    r["vat"] = float(re.search(r"includes (\d+) per cent VAT", head).group(1)) / 100
    r["income_excl_vat"] = "Fee income excl. VAT" in head
    rl = open(find(tgt, "analytics_release_log", ".md"), encoding="utf-8").read()
    r["r2_replaces"] = "R2 replaces the first release" in rl
    thread = open(find(tgt, "planning_thread_carousel_slot", ".txt"), encoding="utf-8").read()
    r["checkout3_named"] = "Checkout 3" in thread
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


def guard(S, y_count, inc, pol, grain, render_weighted):
    """Per cent change in each cell's carousel order rate against the incumbent's, both on y_count."""
    val = cell_rates(S, y_count, [inc] + pol, render_weighted)
    Nc = np.array([(S.cell == c).sum() for c in range(8)], float)
    groups = {"eight": {c: [c] for c in range(8)}, "platform": {"app": [0, 1, 2, 3], "web": [4, 5, 6, 7]},
              "tenure": {b: [b, b + 4] for b in range(4)}, "pooled": {"all": list(range(8))}}[grain]
    out = {}
    for r in pol:
        for key, cs in groups.items():
            w = Nc[cs] / Nc[cs].sum()
            d = sum(wi * (val[(r, c)] - val[(inc, c)]) for wi, c in zip(w, cs))
            b = sum(wi * val[(inc, c)] for wi, c in zip(w, cs))
            out[(r, key)] = 100 * d / b
    return out


def tile_orders(S, O, hours=None, before_end=False):
    """Orders placed from each session's tiles: the buyer's carousel orders of a listing the session showed."""
    t = S.melt(id_vars=["session_id", "buyer_id", "started_at", "ended_at"],
               value_vars=[f"tile_{i}" for i in range(1, 7)], value_name="listing_id")
    c = O[O.channel == "carousel"].merge(t, on=["buyer_id", "listing_id"], how="inner")
    c = c[c.ordered_at >= c.started_at]
    if before_end:
        c = c[c.ordered_at <= c.ended_at]
    if hours is not None:
        c = c[(c.ordered_at - c.ended_at).dt.total_seconds() <= hours * 3600]
    return S.session_id.map(c.groupby("session_id").size()).fillna(0).astype(int).to_numpy()


def buyer_carousel(S, O, days):
    m = O[O.channel == "carousel"].merge(S[["buyer_id", "session_id", "started_at"]].rename(
        columns={"session_id": "sid"}), on="buyer_id")
    dt = (m.ordered_at - m.started_at).dt.total_seconds()
    return S.session_id.map(m[(dt >= 0) & (dt <= days * 86400)].groupby("sid").size()).fillna(0).to_numpy()


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


def screen(S, y_basis, y_count, how, grain, floor_key, rules, inc, pol):
    val = lifts(S, y_basis, how, inc, pol)
    rw = how in ("replay_rows", "render_weights")
    g = guard(S, y_count, inc, pol, grain, rw)
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
                                   "r2_replaces", "balance_is_a_method", "rate_from_tiles", "seven_day_rule",
                                   "provider_captures_only", "income_excl_vat", "checkout3_named"))
            and rules["tariff_id"] == "KB-2026-02" and rules["tariff_changes_inside_slot"] == 0
            and rules["tariff_latest_start"] > rules["slot_end"] and len(pol) == 6 and abs(rules["vat"] - 0.21) < 1e-12,
            "rules.read_from_documents", {k: rules[k] for k in ("tariff_id", "app_start", "slot_start", "vat")})
    R, S, O, PM, OF = load(tgt, rules)
    v.check(len(R) >= 25_000 and len(S) == R.session_id.nunique(), "data.render_rows", len(R))
    v.check((S.ynuniq == 1).all() and (S.pnuniq == 1).all() and (S.rnuniq == 1).all(), "data.one_draw_per_session")
    v.check(S.buyer_id.is_unique, "data.one_session_per_buyer")
    # the render log's ordered tiles tie to the carousel orders the orders extract credits to the session
    ins = O[O.channel == "carousel"].groupby("home_session_id").size()
    v.check((S.session_id.map(ins).fillna(0).astype(int) == S.y).all(), "tie.render_log_orders")
    y_in = S.y.to_numpy().astype(float)
    y_tiles = tile_orders(S, O).astype(float)
    v.check((tile_orders(S, O, before_end=True) == S.y.to_numpy()).all(), "tie.tile_orders_before_the_end")
    W21 = window_orders(S, O, 21)
    y_k = per_session(S, W21)
    # orders placed from a session's tiles after it closed: carousel orders in an unlogged home session,
    # within 4 hours of the end, never in the session-sequence model's arm; no shown listing reaches its
    # buyer through a carousel tile later than that (the seven-day rule)
    t_all = S.melt(id_vars=["session_id", "buyer_id", "ranker", "ended_at"],
                   value_vars=[f"tile_{i}" for i in range(1, 7)], value_name="listing_id")
    aft = O.merge(t_all, on=["buyer_id", "listing_id"])
    aft = aft[(aft.ordered_at > aft.ended_at) & (aft.channel == "carousel")]
    hrs = (aft.ordered_at - aft.ended_at).dt.total_seconds() / 3600
    v.check(len(aft) == int((y_tiles - y_in).sum()) > 0 and hrs.max() <= 4.0 and
            not aft.home_session_id.isin(S.session_id).any() and (aft.ranker == "HC-34").sum() <= 5,
            "tiles.orders_after_the_end", (len(aft), round(float(hrs.max()), 2)))
    out["tile_orders_after_the_end"] = {"orders": int(len(aft)), "by_ranker": aft.ranker.value_counts().to_dict()}
    # ------------------------------------------------------------------ rungs
    L = rules["names"]
    rung_def = [("replay_rows", "platform", "rendered", y_in, y_in),
                ("render_weights", "platform", "rendered_w", y_in, y_in),
                ("session_weights", "eight", "per_ranking", y_in, y_in),
                ("session_weights", "eight", "per_ranking", y_in, y_tiles),
                ("session_weights", "eight", "per_ranking", y_k, y_tiles)]
    rungs = []
    for how, grain, fk, yb, yc in rung_def:
        val, ok, first, second, margin = screen(S, yb, yc, how, grain, fk, rules, inc, pol)
        rungs.append(dict(estimator=how, guardrail=grain, count="tiles" if yc is y_tiles else "ordered_tiles",
                          basis="kept" if yb is y_k else "in-session",
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
    for how in ("session_weights_selfnorm", "session_weights_clipped", "within_cell"):
        lv = lifts(S, y_k, how, inc, pol)
        v.check(all(abs(lv[r] - E_[r]) < 1e-9 for r in pol), f"session_grain.{how}")
    # the stump: the lift over the test with the guardrail read on the render log's ordered tiles
    val, ok, first, second, margin = screen(S, y_k, y_in, "session_weights", "eight", "per_ranking", rules, inc, pol)
    out["stump"] = {"call": first, "lift": val[first], "runner_up": second, "runner_up_lift": val[second]}
    v.check(first == "HC-34" and second == "HC-37" and margin >= 1.5, "stump.logger_guardrail_files_C",
            (first, second, round(margin, 3)))
    # ------------------------------------------------------------------ conditions in detail
    counts = {"ordered_tiles": y_in, "tiles": y_tiles,
              "credited": S.session_id.map(ins).fillna(0).to_numpy().astype(float),
              "tiles_within_4h": tile_orders(S, O, hours=4).astype(float),
              "tiles_within_1h": tile_orders(S, O, hours=1).astype(float),
              "buyer_7d": buyer_carousel(S, O, 7), "buyer_21d": buyer_carousel(S, O, 21)}
    br = {}
    for nm, yc in counts.items():
        g = guard(S, yc, inc, pol, "eight", False)
        br[nm] = sorted((r, c) for (r, c), x in g.items() if x < -rules["guard_pct"])
        out[f"guardrail_{nm}"] = {f"{r}|{CELL_LABELS[c]}": round(x, 3) for (r, c), x in g.items()
                                  if r in ("HC-31", "HC-34") and c in (0, 7)}
    out["guardrail_breaches"] = {k: [f"{r}|{CELL_LABELS[c]}" for r, c in x] for k, x in br.items()}
    v.check(br["tiles"] == [("HC-31", 7), ("HC-34", 0)], "guardrail.breaches_on_the_tiles", br["tiles"])
    v.check(br["ordered_tiles"] == [("HC-31", 7)] and br["credited"] == br["ordered_tiles"],
            "guardrail.logger_count_passes_C", br["ordered_tiles"])
    v.check(br["tiles_within_4h"] == br["tiles"] and ("HC-34", 0) not in br["tiles_within_1h"],
            "guardrail.time_limits", (br["tiles_within_4h"], br["tiles_within_1h"]))
    v.check(("HC-34", 0) not in br["buyer_7d"] and ("HC-34", 0) not in br["buyer_21d"], "guardrail.buyer_windows_pass_C")
    gt = guard(S, y_tiles, inc, pol, "eight", False)
    out["guardrail_pct"] = {f"{r}|{CELL_LABELS[c]}": round(x, 3) for (r, c), x in gt.items()}
    for coarse in ("platform", "tenure", "pooled"):
        gc = guard(S, y_tiles, inc, pol, coarse, False)
        v.check(min(gc.values()) > -rules["guard_pct"], f"guardrail.coarse_{coarse}_passes_everyone")
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
    xa = pd.read_excel(find(tgt, "carousel_experiment_archive", ".xlsx"), sheet_name=None)
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
    # ------------------------------------------------------------------ the slot's planned traffic by cell
    wk1 = pd.read_csv(find(tgt, "home_carousel_sessions_weekly_2025", ".csv"))
    wk2 = pd.read_csv(find(tgt, "home_carousel_sessions_weekly_R2", ".csv"))
    key = ["iso_week", "platform", "tenure_band"]
    cur = pd.concat([wk1[~wk1.set_index(key).index.isin(wk2.set_index(key).index)], wk2])
    week_starts = [rules["slot_start"] + timedelta(weeks=i) for i in range(rules["slot_weeks"])]
    slot_wk = [d.isocalendar()[1] for d in week_starts]
    app_wk = [d.isocalendar()[1] for d in week_starts if d + timedelta(days=6) >= rules["app_start"]]
    prev = rules["slot_start"].year - 1
    band_lab = ["0-29", "30-179", "180-729", "730+"]

    def arm_of(table, app_weeks):
        a_ = np.zeros(8)
        for c in range(8):
            plat = "app" if c < 4 else "web"
            for w_ in (app_weeks if plat == "app" else slot_wk):
                m = (table.iso_week == f"{prev}-W{w_:02d}") & (table.platform == plat) & \
                    (table.tenure_band == band_lab[c % 4])
                a_[c] += rules["slot_share"] * table.loc[m, "logged_in_sessions"].sum()
        return a_
    arm = arm_of(cur, app_wk)
    # ------------------------------------------------------------------ ask 1: fee income per 1,000 sessions
    o = W21.merge(PM, on="order_id", how="left")
    captured = o.payment_id.notna().to_numpy()
    pickup = (o.delivery == "pickup").to_numpy()
    in_person = ~captured & pickup                     # collected and paid to the seller at the handover
    on_balance = ~captured & ~pickup                   # shipped, paid from a Vouwlijn balance: fee charged
    # the checkout the slot runs on, from the records: the last pickup paid at the handover, and every pickup after it
    # (to the extract's end) paid at checkout
    pk = O[O.delivery == "pickup"].merge(PM[["order_id", "payment_id"]], on="order_id", how="left")
    hand = pk[pk.payment_id.isna()]
    switch = hand.ordered_at.max().normalize() + pd.Timedelta(days=1)
    after = pk[pk.ordered_at >= switch]
    before = pk[pk.ordered_at < switch]
    out["checkout3"] = dict(switch=str(switch.date()), after_pickups=len(after),
                            after_handover=int(after.payment_id.isna().sum()), before_pickups=len(before),
                            before_handover=int(before.payment_id.isna().sum()),
                            days_to_extract=int((O.ordered_at.max().normalize() - switch).days))
    v.check(len(after) >= 5000 and after.payment_id.notna().all() and out["checkout3"]["days_to_extract"] >= 14 and
            before.payment_id.isna().mean() >= 0.4 and switch.date() < rules["slot_start"] and rules["checkout3_named"],
            "checkout.every_pickup_paid_at_checkout_before_the_slot", out["checkout3"])
    v.check(not ((o.channel == "carousel") & (o.home_session_id == o.sid) & (o.ordered_at >= switch)).any(),
            "checkout.in_session_orders_predate_the_switch")
    x = o.merge(OF, on=["buyer_id", "listing_id"], how="left")
    live = ((x.accepted_at <= x.ordered_at) & (x.expires_at >= x.ordered_at)).to_numpy()
    off_price = np.where(live, x.offer_eur, x.asking_price_eur)
    any_offer = np.where(x.offer_eur.notna(), x.offer_eur, x.asking_price_eur)
    pay_price = (o.amount_eur - o.shipping_eur - o.buyer_protection_fee_eur).round(2).to_numpy()
    v.check(np.allclose(off_price[captured], pay_price[captured], atol=0.004), "ask1.price_paid_two_routes")
    price_paid = np.where(captured, pay_price, off_price)
    asking = o.asking_price_eur.to_numpy()
    vat = 1 + rules["vat"]
    insess = ((o.channel == "carousel") & (o.home_session_id == o.sid)).to_numpy()

    def fee_vec(vat_out=True, charge_balance=True, cover="new", price=None, fixed=None):
        p_ = price_paid if price is None else price
        f = (rules["tariff_fixed"] if fixed is None else fixed) + rules["tariff_pct"] * np.round(p_)
        if cover == "old":
            f = np.where(in_person, 0.0, f)
        if not charge_balance:
            f = np.where(on_balance, 0.0, f)
        return f / vat if vat_out else f

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
    covers = {}
    for f1, f2, hz2, hz1 in np.ndindex(2, 2, 2, 2):
        for cv in ("new", "old"):
            covers[(f1, f2, hz2, hz1, cv)] = grid_for(fee_vec(vat_out=not f1, charge_balance=not f2, cover=cv,
                                                              price=asking if hz2 else None,
                                                              fixed=rules["tariff_latest_fixed"] if hz1 else None))
    cells_fee = covers[(0, 0, 0, 0, "new")]           # every order charged: the slot runs on the new checkout
    cells_ord = {}
    for c in range(8):
        cm = (S.cell == c).to_numpy()
        b0o = y_k[cm & (S.ranker == inc).to_numpy()].mean()
        for r in pol:
            cells_ord[(r, c)] = (y_k[cm & (S.ranker == r).to_numpy()].mean() - b0o) * 1000
    out["ask1"] = {f"{r}|{CELL_LABELS[c]}": round(x_, 4) for (r, c), x_ in cells_fee.items()}
    out["ask1_filed"] = {f"{r}|{CELL_LABELS[c]}": round(x_, 1) for (r, c), x_ in cells_fee.items()}
    v.check(min(bin_clear(x_, 0.1) for x_ in cells_fee.values()) >= 0.03, "ask1.mid_bin",
            min(bin_clear(x_, 0.1) for x_ in cells_fee.values()))
    # every way of mishandling the checkout (the logged window's, where a pickup with no capture carries no fee) and
    # the four hazards (VAT kept in, balance purchases uncharged, the asking price, the register's newest row) moves
    # every cell out of its bin; so does the natural read (every order priced on the formula, VAT in, asking price,
    # the newest row, in-session)
    fee_sets = {}
    for f1, f2, hz2, hz1 in np.ndindex(2, 2, 2, 2):
        for cv in ("new", "old"):
            if cv == "new" and not any((f1, f2, hz2, hz1)):
                continue
            g_ = covers[(f1, f2, hz2, hz1, cv)]
            fee_sets[(f1, f2, cv, hz2, hz1)] = g_
            stay = [k for k in cells_fee if nbin(g_[k], 0.1) == nbin(cells_fee[k], 0.1)]
            v.check(not stay, f"ask1.devices_{f1}{f2}{cv}{hz2}{hz1}_move_every_cell", stay)
    v.check(len(fee_sets) == 31, "ask1.readings_31", len(fee_sets))
    gn = grid_for(fee_vec(vat_out=False, cover="new", price=asking, fixed=rules["tariff_latest_fixed"]), insess)
    v.check(not [k for k in cells_fee if nbin(gn[k], 0.1) == nbin(cells_fee[k], 0.1)], "ask1.natural_read_moves_every_cell")
    gv = grid_for(np.round(fee_vec(vat_out=False, cover="new") * 100 / vat) / 100)
    v.check(all(nbin(gv[k], 0.1) == nbin(cells_fee[k], 0.1) for k in cells_fee), "ask1.vat_per_order_same_grid")
    for nm, g_ in (("every_offer", grid_for(fee_vec(price=any_offer))),
                   ("drop_pickups", grid_for(np.where(pickup, 0.0, fee_vec()))),
                   ("payments_as_charged", grid_for(np.where(captured, o.buyer_protection_fee_eur.fillna(0).to_numpy(),
                                                             0.0)))):
        moved = sum(nbin(g_[k], 0.1) != nbin(cells_fee[k], 0.1) for k in cells_fee)
        out[f"ask1_{nm}_cells_moved"] = int(moved)
        v.check(moved >= 36, f"ask1.over_cleaner_{nm}", moved)
    out["ask1_cells_under_one_euro"] = [f"{r}|{CELL_LABELS[c]}" for (r, c), x_ in cells_fee.items() if abs(x_) < 1.0]
    # ------------------------------------------------------------------ the referee: Finance's fee income, Q3
    allo = O.merge(PM, on="order_id", how="left")
    cap_all = allo.payment_id.notna().to_numpy()
    allx = allo.merge(OF, on=["buyer_id", "listing_id"], how="left")
    live_all = ((allx.accepted_at <= allx.ordered_at) & (allx.expires_at >= allx.ordered_at)).to_numpy()
    pp_all = np.where(cap_all, (allo.amount_eur - allo.shipping_eur - allo.buyer_protection_fee_eur).round(2),
                      np.where(live_all, allx.offer_eur, allx.asking_price_eur))
    covered = cap_all | (allo.delivery != "pickup").to_numpy()
    booked = np.where(cap_all, allo.captured_at, allo.ordered_at)
    tar = pd.read_csv(find(tgt, "kopersbescherming", ".csv"))
    starts = pd.to_datetime(tar.ingangsdatum).to_numpy()
    k_ = np.searchsorted(starts, booked.astype("datetime64[ns]"), side="right") - 1
    fee_all = np.round(tar.vast_bedrag_eur.to_numpy()[k_] * 100) + tar.percentage_van_artikelprijs.to_numpy()[k_] * np.round(pp_all)
    ref = pd.DataFrame({"m": pd.to_datetime(booked).strftime("%Y-%m"), "platform": allo.platform, "fee": fee_all,
                        "item": pp_all, "covered": covered})
    ref = ref[ref.covered & ref.m.isin(["2026-07", "2026-08", "2026-09"])]
    gq = ref.groupby(["m", "platform"]).agg(n=("fee", "size"), fee=("fee", "sum"), item=("item", "sum"))
    fin = pd.read_excel(find(tgt, "finance_buyer_protection_fee_income", ".xlsx"), header=None)
    h = int(np.flatnonzero(fin[0].astype(str).str.strip() == "Month")[0])
    months = {"July 2026": "2026-07", "August 2026": "2026-08", "September 2026": "2026-09"}
    ok_ = True
    for row in fin.iloc[h + 1:h + 7].itertuples(index=False):
        g = gq.loc[(months[row[0]], row[1])]
        ok_ &= int(g.n) == int(row[2]) and abs(g["item"] - float(row[3])) < 0.005 and \
            abs(round(g.fee / 100 / vat, 2) - float(row[4])) < 0.005
    v.check(ok_, "referee.ties_excl_vat_with_balance_purchases")
    full = pd.DataFrame({"m": pd.to_datetime(booked).strftime("%Y-%m"), "fee": fee_all})
    full_q3 = float(full[full.m.isin(["2026-07", "2026-08", "2026-09"])].fee.sum()) / 100 / vat
    stated_q3 = float(fin.iloc[h + 1:h + 7][4].astype(float).sum())
    out["referee_full_cover_over_pct"] = round(100 * (full_q3 / stated_q3 - 1), 2)
    v.check(full_q3 / stated_q3 - 1 > 0.01, "referee.full_cover_does_not_tie", out["referee_full_cover_over_pct"])
    # ------------------------------------------------------------------ ask 2: slot totals
    out["arm_sessions"] = arm.tolist()
    out["app_weeks"], out["web_weeks"] = app_wk, slot_wk
    tot = lambda g_, a_: {r: sum(g_[(r, c)] * a_[c] / 1000 for c in range(8)) for r in pol}
    tot_o, tot_f = tot(cells_ord, arm), tot(cells_fee, arm)
    out["ask2"] = {"orders": tot_o, "fee": tot_f,
                   "orders_filed": {r: int(nbin(x_, 100) * 100) for r, x_ in tot_o.items()},
                   "fee_filed": {r: int(nbin(x_, 100) * 100) for r, x_ in tot_f.items()}}
    v.check(min(bin_clear(x_, 100) for x_ in list(tot_o.values()) + list(tot_f.values())) >= 20, "ask2.mid_bin")
    arms_all = {"planned": arm, "first_release": arm_of(wk1, app_wk), "all_weeks_app": arm_of(cur, slot_wk),
                "both": arm_of(wk1, slot_wk)}
    arms = {k: a_ for k, a_ in arms_all.items() if k != "planned"}
    pooled_in = lifts(S, y_in, "session_weights", inc, pol)
    inside = []
    for r in pol:
        reads = [(nm, tot(cells_ord, a_)[r], tot_o[r], True) for nm, a_ in arms.items()]
        reads.append(("natural", pooled_in[r] * arms["both"].sum() / 1000, tot_o[r], True))
        reads.append(("orders_pooled", E_[r] * arm.sum() / 1000, tot_o[r], False))
        nc = np.array([(S.cell == c).sum() for c in range(8)], float)
        reads.append(("fee_pooled", sum(nc[c] / nc.sum() * cells_fee[(r, c)] for c in range(8)) * arm.sum() / 1000,
                      tot_f[r], False))
        for (f1, f2, hz2, hz1) in np.ndindex(2, 2, 2, 2):
            for cv in ("new", "old"):
                for an, a_ in arms_all.items():
                    if an == "planned" and cv == "new" and not any((f1, f2, hz2, hz1)):
                        continue
                    reads.append((f"fee_{f1}{f2}{cv}{hz2}{hz1}_{an}", tot(covers[(f1, f2, hz2, hz1, cv)], a_)[r],
                                  tot_f[r], False))
        worst = None
        for nm, x_, g0, stop in reads:
            k0 = nbin(g0, 100)
            o_ = max((k0 - 0.5) * 100 - x_, x_ - (k0 + 0.5) * 100)
            score = abs(o_) if (o_ > 0 or not stop) else -abs(o_)
            if worst is None or score < worst[0]:
                worst = (score, nm, round(x_, 1), round(g0, 1))
            if o_ < 0:
                inside.append(f"{r}|{nm}")
        v.check(worst[0] >= 5 and len(reads) == 3 + 1 + 1 + 1 + 127, f"ask2.every_reading_clear.{r}", worst)
    out["ask2_readings_inside_the_hundred"] = inside
    v.check(len([z for z in inside if "pooled" not in z]) <= 6, "ask2.device_readings_out", inside)
    v.check(not [z for z in inside if z.split("|", 1)[1].startswith("fee_00old00_planned")],
            "ask2.logged_checkout_alone_moves_every_fee_total")
    # ------------------------------------------------------------------ device separation from the call
    O2 = O.copy()
    O2["asking_price_eur"] = O2.asking_price_eur.sample(frac=1.0, random_state=7).to_numpy()
    O2["delivery"] = "shipped"
    y2 = per_session(S, window_orders(S, O2, 21))
    l2 = lifts(S, y2, "session_weights", inc, pol)
    g2 = guard(S, tile_orders(S, O2).astype(float), inc, pol, "eight", False)
    v.check(all(abs(l2[r] - E_[r]) < 1e-12 for r in pol) and
            sorted((r, c) for (r, c), x_ in g2.items() if x_ < -rules["guard_pct"]) == [("HC-31", 7), ("HC-34", 0)],
            "separation.prices_and_delivery_do_not_move_the_call")
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
