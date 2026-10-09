"""task122 generator: every assertion the build makes, on the files as written (read back from disk),
plus the few facts only the generator can see (the archive's hidden layers, the come-back counts it
planted). Fails loudly at the first assertion that does not hold, and returns the build record (every
figure the design note quotes).
"""
import itertools
import json
import os
import re

import numpy as np
import pandas as pd

import analysis as A
import archive as Ar
import asks as K
import docs as D
import params as P
import writers as Wr

L = {r: P.LETTER[r] for r in P.RANKERS}
E_, B_, A_, C_, D_, F_ = "HC-37", "HC-33", "HC-31", "HC-34", "HC-36", "HC-39"


class Checks:
    def __init__(self):
        self.items = []

    def __call__(self, cond, name, detail=""):
        ok = bool(cond)
        self.items.append((name, ok, str(detail)[:300]))
        if not ok:
            if os.environ.get("CHECKS_SOFT") == "1":       # survey mode: report every failure, then stop
                print(f"FAIL [{name}] {str(detail)[:300]}", flush=True)
                return ok
            raise AssertionError(f"[{name}] {detail}")
        return ok


def bin_dist(x, unit=0.1):
    """Distance from x to the nearest rounding boundary of its bin (bins of width unit)."""
    k = np.floor(x / unit + 0.5)
    return min(abs(x - (k - 0.5) * unit), abs((k + 0.5) * unit - x))


def same_bin(a, b, unit=0.1):
    return np.floor(a / unit + 0.5) == np.floor(b / unit + 0.5)


def outside(x, ref, unit=0.1):
    """How far x sits outside ref's bin (negative when inside it, by its distance to the nearer edge)."""
    k = np.floor(ref / unit + 0.5)
    return max((k - 0.5) * unit - x, x - (k + 0.5) * unit)


def reading(M, y_basis, y_guard, est_kind, guard, floor_grain):
    S = M.S
    vals = A.est(S, y_basis, est_kind)
    ok, g, f, b = A.conditions(S, y_guard, vals, est_kind, guard, floor_grain)
    first, second, margin = A.leader(vals, ok)
    return vals, ok, first, second, margin


def run_all(W, meta, A_hidden, tgt, root, distractors, scrub_rc):
    K_ = Checks()
    rec = {}
    tgt = str(tgt)
    M = A.load_main(tgt)
    S, O = M.S, M.O
    y_in = S.y.to_numpy().astype(float)
    y_kept = A.followup(M, hours=21 * 24).astype(float)
    y_r1 = y_in                                              # the render log's ordered_tiles
    y_r2 = A.tile_orders(M).astype(float)                    # every order placed from the session's tiles
    y_w7 = A.carousel_window(M, 7).astype(float)             # every carousel order by the buyer, 7 days

    # ---------------------------------------------------------------- ties and identities
    K_(len(S) == 150_400 and len(M.R) >= 25_000, "spine.size", (len(S), len(M.R)))
    K_((A.session_orders(M) == S.y.to_numpy()).all(), "tie.ordered_tiles_to_orders_credited_to_the_session")
    K_((A.tile_orders(M, timed=True) == S.y.to_numpy()).all(), "tie.tile_orders_before_the_end_to_ordered_tiles")
    fam = {k: A.est(S, y_in, k) for k in A.SESSION_GRAIN}
    K_(all(abs(fam[k][r] - fam["session_ipw"][r]) < 1e-9 for k in A.SESSION_GRAIN for r in P.POLICIES),
       "estimators.session_grain_identical")
    cnt = S.groupby(["cell", "ranker"]).size()
    K_(all(cnt[(c, r)] == round(P.N_CELL[c] * P.PI[c, P.RANKERS.index(r)]) for c in range(8) for r in P.RANKERS),
       "logger.quota_exact")
    rec["sessions"], rec["renders"] = int(len(S)), int(len(M.R))

    # ---------------------------------------------------------------- come-back tile orders
    tiles = S.melt(id_vars=["session_id", "buyer_id", "ranker", "cell", "ended_at", "watchlist_at_start"],
                   value_vars=[f"tile_{i}" for i in range(1, 7)], value_name="listing_id")
    x = O.merge(tiles, on=["buyer_id", "listing_id"], how="inner")
    after = x[x.ordered_at > x.ended_at]
    cb = after[after.channel == "carousel"]
    secs = (cb.ordered_at - cb.ended_at).dt.total_seconds()
    K_(len(cb) == int((y_r2 - y_r1).sum()) and len(cb) > 0, "comeback.count_is_the_tile_order_gap", len(cb))
    K_(secs.min() >= 120 and secs.max() <= P.COMEBACK_MAX_S, "comeback.2_minutes_to_4_hours_after_the_end",
       (secs.min(), secs.max()))
    K_(not cb.home_session_id.isin(S.session_id).any() and cb.home_session_id.notna().all(),
       "comeback.credited_to_an_unlogged_home_session")
    K_(cnt.loc[[(0, C_)]].sum() > 0 and int((cb[cb.cell == 0].ranker == C_).sum()) == 0 and
       1000 * int((cb.ranker == C_).sum()) / int(cnt.xs(C_, level=1).sum()) < 0.3,
       "comeback.session_sequence_model_rarely_none_in_app_0_29", int((cb.ranker == C_).sum()))
    wl_hit = [str(l) in (w or "").split() for l, w in zip(cb.listing_id, cb.watchlist_at_start)]
    K_(not any(wl_hit), "comeback.never_a_watched_listing")
    per = cb.groupby(["cell", "ranker"]).size()
    want = {(c, k): W.comeback_counts[(c, k)] for c in range(8) for k in range(7)}
    K_(all(int(per.get((c, P.RANKERS[k]), 0)) == n for (c, k), n in want.items()), "comeback.counts_as_planted")
    # the seven-day rule: no listing a session showed comes back to its buyer through a carousel tile later,
    # other than the come-backs from the tile still on screen
    K_(not ((after.channel == "carousel") & ((after.ordered_at - after.ended_at).dt.total_seconds()
                                            > P.COMEBACK_MAX_S)).any(), "comeback.seven_day_rule_holds")
    rate = {f"{P.CELL_NAMES[c]}|{L[r]}": round(1000 * int(per.get((c, r), 0)) / int(cnt[(c, r)]), 3)
            for c in range(8) for r in P.RANKERS}
    rec["comebacks"] = dict(orders=int(len(cb)), sessions=int((y_r2 != y_r1).sum()), per_1000=rate,
                            later_orders_of_shown_listings_by_channel=after.channel.value_counts().to_dict())

    # ---------------------------------------------------------------- the five rungs
    rungs = [("replay_rows", "platform", y_in, y_r1, "rendered", D_, 1.20),
             ("render_weights", "platform", y_in, y_r1, "rendered", A_, 1.20),
             ("session_ipw", "eight", y_in, y_r1, "ranking", C_, 1.20),
             ("session_ipw", "eight", y_in, y_r2, "ranking", B_, 1.20),
             ("session_ipw", "eight", y_kept, y_r2, "ranking", E_, 1.50)]
    rec["rungs"] = []
    raw = []
    for i, (ek, gr, yb, yg, fg, want_, mmin) in enumerate(rungs):
        vals, ok, first, second, margin = reading(M, yb, yg, ek, gr, fg)
        raw.append({L[r]: float(v) for r, v in vals.items()})
        K_(first == want_ and margin >= mmin, f"rung{i}.leader",
           (i, L[first], L[second], round(margin, 3), {L[r]: round(v, 3) for r, v in vals.items()}))
        rank_all = sorted(P.POLICIES, key=lambda r: -vals[r])
        rec["rungs"].append(dict(rung=i, estimator=ek, guardrail=gr,
                                 guardrail_count="ordered_tiles" if yg is y_r1 else "orders from the tiles",
                                 basis="kept" if yb is y_kept else "in-session",
                                 values={L[r]: round(v, 3) for r, v in vals.items()}, leader=L[first],
                                 runner_up=L[second] if second else None, margin=round(margin, 3),
                                 E_rank_all=rank_all.index(E_) + 1,
                                 qualifiers=[L[r] for r in P.POLICIES if ok[r]]))
    pos = [r["E_rank_all"] for r in rec["rungs"]]
    K_(pos[0] == 5 and pos[1] == 4 and pos[2] == 4 and pos[3] == 4, "position.E_5th_4th_4th_4th", pos)
    K_(all(r["leader"] != "E" for r in rec["rungs"][:4]), "position.E_leads_no_intermediate_rung")
    second_at = [i for i, r in enumerate(rec["rungs"][:4]) if r["runner_up"] == "E"]
    K_(second_at == [3], "position.E_second_only_at_rung3", second_at)
    v3, v4 = raw[3], raw[4]
    K_(v3["B"] / v3["E"] >= 1.20, "position.rung3_gap", v3["B"] / v3["E"])
    carried = v3["B"] / v3["E"]
    edge = (v4["E"] / v3["E"]) / (v4["B"] / v3["B"])
    K_(edge >= 1.2 * carried, "dominance", (round(edge, 3), round(carried, 3)))
    rec["dominance"] = dict(carried=round(carried, 3), edge=round(edge, 3), product=round(edge / carried, 3))
    e_k, b_k = v4["E"], v4["B"]
    rec["call"] = dict(answer="HC-37", lift=round(e_k, 3), runner_up="HC-33", runner_up_lift=round(b_k, 3),
                       gap=round(e_k - b_k, 3))
    for nm, x_ in (("E_kept", e_k), ("B_kept", b_k), ("gap", e_k - b_k)):
        K_(bin_dist(x_) >= 0.03, f"bins.{nm}", (x_, bin_dist(x_)))

    # ---------------------------------------------------------------- the stump: kept lift, guardrail on the logger
    vals, ok, first, second, margin = reading(M, y_kept, y_r1, "session_ipw", "eight", "ranking")
    K_(first == C_ and second == E_ and margin >= 1.5, "stump.kept_with_the_logger_guardrail_names_C",
       (L[first], L[second], round(margin, 3)))
    rec["stump"] = dict(call=L[first], lift=round(vals[first], 3), runner_up=L[second],
                        runner_up_lift=round(vals[second], 3), gap=round(vals[first] - vals[second], 3))
    K_(not same_bin(vals[first], e_k) and not same_bin(vals[second], b_k) and
       not same_bin(vals[first] - vals[second], e_k - b_k), "stump.every_call_figure_apart", rec["stump"])

    # ---------------------------------------------------------------- the guardrail by count
    counts = {"ordered_tiles": y_r1, "orders_from_the_tiles": y_r2}
    for h in (0.5, 1, 1.5, 2, 3, 4, 6, 24):
        counts[f"tiles_within_{h}h"] = A.tile_orders(M, hours=h).astype(float)
    for d in (1, 7, 21):
        counts[f"buyer_carousel_orders_{d}d"] = A.carousel_window(M, d).astype(float)
    counts["orders_credited_to_the_session"] = A.session_orders(M).astype(float)
    gtab = {}
    for nm, yc in counts.items():
        g = A.guardrail(S, yc)
        gtab[nm] = dict(breaches=sorted(f"{L[r]}|{P.CELL_NAMES[c]}" for (r, c), v in g.items() if v < -1.5),
                        C_app_0_29=round(g[(C_, 0)], 3), A_web_730=round(g[(A_, 7)], 3))
    rec["guardrail_by_count"] = gtab
    K_(gtab["ordered_tiles"]["breaches"] == ["A|web 730+"], "guardrail.logger_breaches_A_only",
       gtab["ordered_tiles"])
    K_(gtab["orders_credited_to_the_session"] == gtab["ordered_tiles"], "guardrail.credited_equals_logger")
    K_(gtab["orders_from_the_tiles"]["breaches"] == ["A|web 730+", "C|app <30"], "guardrail.tiles_breach_A_and_C",
       gtab["orders_from_the_tiles"])
    K_(gtab["ordered_tiles"]["C_app_0_29"] >= -1.5 + 0.4 and gtab["orders_from_the_tiles"]["C_app_0_29"] <= -1.5 - 1.5,
       "guardrail.C_margins", (gtab["ordered_tiles"]["C_app_0_29"], gtab["orders_from_the_tiles"]["C_app_0_29"]))
    for h in (4, 6, 24):
        K_(np.array_equal(counts[f"tiles_within_{h}h"], y_r2), f"guardrail.C1_any_limit_from_4h.{h}")
    for d in (1, 7, 21):
        K_("C|app <30" not in gtab[f"buyer_carousel_orders_{d}d"]["breaches"], f"guardrail.buyer_window_passes_C.{d}",
           gtab[f"buyer_carousel_orders_{d}d"])
    for nm, yc in (("logger", y_r1), ("tiles", y_r2)):
        g = A.guardrail(S, yc)
        others = [v for (r, c), v in g.items() if (r, c) not in ((A_, 7), (C_, 0))]
        K_(min(others) >= -0.9, f"guardrail.others_clear.{nm}", min(others))
        for coarse in ("platform", "tenure", "pooled"):
            gc = A.guardrail(S, yc, coarse=coarse)
            K_(min(gc.values()) >= -0.8, f"guardrail.coarse.{coarse}.{nm}", min(gc.values()))
    g0 = A.guardrail(S, y_r2)
    rec["guardrail_pct"] = {f"{L[r]}|{P.CELL_NAMES[c]}": round(v, 3) for (r, c), v in g0.items()}

    # ---------------------------------------------------------------- correction grid (24 cells)
    guards = {"platform": ("platform", y_r1), "eight_logger": ("eight", y_r1), "eight_tiles": ("eight", y_r2),
              "eight_buyer_7d": ("eight", y_w7)}
    want = {}
    for gk in guards:
        want[("replay_rows", gk, "in")] = D_
        want[("replay_rows", gk, "kept")] = D_
    want.update({("render_weights", "platform", "in"): A_, ("render_weights", "platform", "kept"): A_,
                 ("render_weights", "eight_logger", "in"): B_, ("render_weights", "eight_logger", "kept"): B_,
                 ("render_weights", "eight_tiles", "in"): B_, ("render_weights", "eight_tiles", "kept"): B_,
                 ("render_weights", "eight_buyer_7d", "in"): A_, ("render_weights", "eight_buyer_7d", "kept"): A_,
                 ("session_ipw", "platform", "in"): C_, ("session_ipw", "platform", "kept"): C_,
                 ("session_ipw", "eight_logger", "in"): C_, ("session_ipw", "eight_logger", "kept"): C_,
                 ("session_ipw", "eight_tiles", "in"): B_, ("session_ipw", "eight_tiles", "kept"): E_,
                 ("session_ipw", "eight_buyer_7d", "in"): C_, ("session_ipw", "eight_buyer_7d", "kept"): C_})
    grid = {}
    for (ek, gk, bas), w in want.items():
        fg = "ranking" if ek == "session_ipw" else "rendered"
        gr, yg = guards[gk]
        vals, ok, first, second, margin = reading(M, y_kept if bas == "kept" else y_in, yg, ek, gr, fg)
        grid[f"{ek}|{gk}|{bas}"] = dict(leader=L[first], value=round(vals[first], 3),
                                        next=L[second] if second else None,
                                        margin=round(margin, 3) if np.isfinite(margin) else "only qualifier")
        K_(first == w and margin >= 1.15, f"grid.{ek}.{gk}.{bas}", grid[f"{ek}|{gk}|{bas}"])
    K_(len(grid) == 24 and sum(v["leader"] == "E" for v in grid.values()) == 1, "grid.E_in_one_cell_only")
    rec["correction_grid"] = grid

    # ---------------------------------------------------------------- partial readings
    share_B = (v3["B"] - v4["B"]) / v3["B"]
    flat = {r: v * (1 - share_B) for r, v in v3.items()}
    elig = rec["rungs"][3]["qualifiers"]
    lead_flat = max([r for r in elig if flat[r] >= 2.0], key=lambda r: flat[r])
    K_(lead_flat == "B", "partial.flat_haircut_at_B_share", (round(share_B, 3), {r: round(v, 2) for r, v in flat.items()}))
    q, Sw, m = A.route2(M)
    pooled_share = float((Sw * q).sum() / max(1, y_in.sum()))
    flat2 = {r: v * (1 - pooled_share) for r, v in v3.items()}
    K_(max([r for r in elig if flat2[r] >= 2.0], key=lambda r: flat2[r]) == "B", "partial.flat_haircut_pooled",
       round(pooled_share, 4))
    rec["partial"] = dict(B_borrowed_share=round(share_B, 4), pooled_share=round(pooled_share, 4),
                          flat_B=round(flat["B"], 3), flat_E=round(flat["E"], 3))
    win = {}
    for d in range(1, 22):
        yw = A.followup(M, hours=d * 24).astype(float)
        vals, ok, first, second, margin = reading(M, yw, y_r2, "session_ipw", "eight", "ranking")
        win[d] = dict(leader=L[first], E=round(vals[E_], 3), B=round(vals[B_], 3))
    full = min(d for d in range(1, 22) if all(win[x_]["E"] == win[21]["E"] and win[x_]["B"] == win[21]["B"]
                                              for x_ in range(d, 22)))
    rec["window_complete_from_days"] = full
    K_(full <= 7, "window.complete_by_7_days", full)
    K_(all(win[d]["leader"] == "B" for d in (1, 2, 3)), "partial.windows_1_to_3_name_B", {d: win[d] for d in (1, 2, 3)})
    K_(all(win[d]["leader"] == "E" and not same_bin(win[d]["B"], b_k) for d in range(4, full)),
       "partial.windows_4_up_E_wrong_runner_up", {d: win[d] for d in range(4, full)})
    K_(all(win[d]["E"] == win[21]["E"] and win[d]["B"] == win[21]["B"] for d in range(7, 22)),
       "window.7_to_21_days_identical")
    for d in (7, 10, 14, 21):
        yc = A.followup(M, calendar_days=d).astype(float)
        vc = A.est(S, yc, "session_ipw")
        K_(all(abs(vc[r] - A.est(S, y_kept, "session_ipw")[r]) < 1e-9 for r in P.POLICIES), f"window.calendar_{d}")
    rec["windows"] = win

    # ---------------------------------------------------------------- route 2 and the anyway rate
    K_(abs(q - 0.625) < 1e-12, "route2.anyway_rate", q)
    k2 = y_in - q * Sw
    r1v, r2v = A.est(S, y_kept, "session_ipw"), A.est(S, k2, "session_ipw")
    K_(all(abs(r1v[r] - r2v[r]) < 0.005 for r in P.POLICIES), "route1_equals_route2.pooled",
       {L[r]: (round(r1v[r], 4), round(r2v[r], 4)) for r in P.POLICIES})
    c1, c2 = A.per_cell(S, y_kept), A.per_cell(S, k2)
    dif = [abs((c1[(r, c)] - c1[("HC-24", c)]) - (c2[(r, c)] - c2[("HC-24", c)])) for r in P.POLICIES for c in range(8)]
    K_(max(dif) < 1e-6, "route1_equals_route2.per_cell", max(dif))
    si = S.set_index("session_id")
    seg_of = {
        "cell": si.cell,
        "ranker": si.ranker,
        "cell_ranker": si.cell.astype(str) + "|" + si.ranker,
        "platform": si.platform,
        "tenure_band": si.band,
        "renders": si.n.clip(upper=5),
        "watch_size": si.watchlist_at_start.map(lambda s: len(s.split()) if s else 0).clip(upper=3),
        "weekday": si.started_at.dt.dayofweek,
        "iso_week": si.started_at.dt.isocalendar().week.astype(int),
        "half": (si.started_at < pd.Timestamp(P.HALF_SPLIT)).map({True: "first", False: "second"}),
    }
    un = m[~m.shown].copy()
    rates = {}
    strat = {}
    for col, ser in seg_of.items():
        un[col] = un.session_id.map(ser)
        g = un.groupby(col, observed=True).bought_later.agg(["mean", "size"])
        rates[col] = {str(k): (round(float(v["mean"]), 4), int(v["size"])) for k, v in g.iterrows()}
        qs = S.session_id.map(ser).map(g["mean"]).to_numpy(float)
        qs = np.where(Sw > 0, qs, 0.0)
        K_(not np.isnan(qs).any(), f"anyway.every_netted_session_has_a_rate.{col}")
        vs = A.est(S, y_in - qs * Sw, "session_ipw")
        strat[col] = (round(vs[E_], 4), round(vs[B_], 4))
        K_(same_bin(vs[E_], e_k) and same_bin(vs[B_], b_k), f"anyway.stratified_netting.{col}",
           (col, vs[E_], vs[B_]))
    rec["anyway_rates"] = rates
    rec["anyway_stratified"] = strat
    exact = [v[0] for col in ("cell", "ranker", "cell_ranker", "platform", "tenure_band") for v in rates[col].values()]
    K_(all(abs(x_ - 0.625) < 1e-9 for x_ in exact), "anyway.exact_in_every_charter_cut_and_arm")
    seg = [v[0] for col in ("renders", "watch_size", "weekday", "iso_week", "half") for v in rates[col].values()
           if v[1] >= 2000]
    K_(all(abs(x_ - 0.625) <= 0.01 for x_ in seg), "anyway.segments_close", (min(seg), max(seg)))
    rec["anyway_segment_range"] = (min(seg), max(seg))
    subs = {"incumbent_arm": un.ranker == "HC-24", "velocity_arm": un.ranker == B_, "app": un.platform == "app",
            "web": un.platform == "web", "first_half": un.half == "first", "second_half": un.half == "second",
            "one_render": un.renders == 1, "up_to_two_renders": un.renders <= 2}
    sub_fig = {}
    for nm, mk in subs.items():
        qq = float(un[mk].bought_later.mean())
        vx = A.est(S, y_in - qq * Sw, "session_ipw")
        sub_fig[nm] = (round(qq, 4), round(vx[E_], 4), round(vx[B_], 4))
        K_(same_bin(vx[E_], e_k) and same_bin(vx[B_], b_k), f"anyway.subpopulation.{nm}", sub_fig[nm])
    rec["anyway_subpopulations"] = sub_fig
    ext = {}
    for x_ in (min(seg), max(seg)):
        vx = A.est(S, y_in - x_ * Sw, "session_ipw")
        ext[str(x_)] = (round(vx[E_], 4), round(vx[B_], 4))
    rec["anyway_extreme_segment_applied_globally"] = ext
    K_(all(same_bin(v[0], e_k) for v in ext.values()), "anyway.E_independent_of_rate", ext)
    rec["route2_q"] = q

    # ---------------------------------------------------------------- floor, bar, halves
    fl = A.floors(S)
    rec["floors"] = {f"{L[r]}|{k}": round(fl[(r, k)], 3) for (r, k) in fl}
    K_(fl[(D_, "per_ranking")] < 12 and fl[(D_, "per_ranking_ipw")] < 12, "floor.D_fails_per_ranking",
       (fl[(D_, "per_ranking")], fl[(D_, "per_ranking_ipw")]))
    K_(fl[(D_, "rendered_tiles")] >= 12 and fl[(D_, "rendered_tiles_ipw")] >= 12, "floor.D_passes_over_rendered_tiles")
    K_(all(fl[(r, k)] >= 13.0 for r in P.POLICIES if r != D_ for k in
           ("per_ranking", "per_ranking_ipw", "rendered_tiles", "rendered_tiles_ipw")), "floor.others_clear")
    K_(all(abs(fl[(r, "per_ranking")] - fl[(r, "rendered_tiles")]) < 0.4 for r in P.POLICIES if r != D_),
       "floor.only_D_moves_with_counting_unit")
    for k in A.SESSION_GRAIN:
        vv = A.est(S, y_in, k)
        K_(vv[F_] <= 2.0 - 0.6, f"bar.F_under.{k}", vv[F_])
    K_(b_k >= 2.0 + 1.3, "bar.B_kept_clears", b_k)
    half = (S.started_at < pd.Timestamp(P.HALF_SPLIT)).to_numpy()
    for nm, yb in (("in", y_in), ("kept", y_kept)):
        h1 = A.est(S[half].reset_index(drop=True), yb[half], "session_snipw")
        h2 = A.est(S[~half].reset_index(drop=True), yb[~half], "session_snipw")
        dmax = max(abs(h1[r] - h2[r]) for r in P.POLICIES)
        K_(dmax <= 0.10, f"halves.{nm}", round(dmax, 3))
        rec[f"halves_{nm}_max_diff"] = round(dmax, 3)

    # ---------------------------------------------------------------- the archive
    xa = pd.read_excel(os.path.join(tgt, D.F_ARCHIVE), sheet_name=None)
    T, AS = xa["tests"], xa["logged_sessions"]
    arch = {}
    for _, t in T.iterrows():
        df = AS[AS.test_id == t.test_id].rename(columns={"propensity": "p", "renders": "n", "in_session_orders": "y"})
        s, rw, rp, rs = Ar.arch_estimates(df)
        N = len(df)
        Tt, Cc = df[df.arm == "test"], df[df.arm == "control"]
        snip = ((Tt.y / Tt.p).sum() / (1 / Tt.p).sum() - (Cc.y / Cc.p).sum() / (1 / Cc.p).sum()) * 1000
        clip = ((Tt.y / np.maximum(Tt.p, 0.05)).sum() - (Cc.y / np.maximum(Cc.p, 0.05)).sum()) / N * 1000
        strat_ = 0.0
        for c, gc in df.groupby(["platform", "tenure_band"]):
            strat_ += len(gc) / N * (gc[gc.arm == "test"].y.mean() - gc[gc.arm == "control"].y.mean()) * 1000
        arch[t.test_id] = dict(R=float(t.realised_lift), sess=s, snip=snip, clip=clip, strat=strat_, render=rw,
                               replay=rp, replay_sessions=rs, published=float(t.offline_estimate_published))
    rec["archive"] = {k: {kk: round(vv, 3) for kk, vv in v.items()} for k, v in arch.items()}
    hits = lambda key: [k for k, v in arch.items() if abs(v[key] - v["R"]) <= 0.25]
    K_(len(hits("sess")) == 9 and max(abs(v["sess"] - v["R"]) for v in arch.values()) <= 0.21,
       "archive.session_weights_9_of_9", max(abs(v["sess"] - v["R"]) for v in arch.values()))
    K_(all(abs(v[k] - v["sess"]) < 1e-9 for v in arch.values() for k in ("snip", "clip", "strat")),
       "archive.session_grain_readings_agree")
    K_(sorted(set(arch) - set(hits("render"))) == ["T2", "T7", "T9"], "archive.render_weights_6_of_9",
       sorted(set(arch) - set(hits("render"))))
    K_(len(hits("replay")) == 3 and sorted(set(hits("replay"))) == ["T1", "T5", "T6"], "archive.replay_3_of_9")
    K_(len(hits("replay_sessions")) < 9, "archive.replay_over_sessions_refuted")
    misses = [v[k] - v["R"] for v in arch.values() for k in ("render", "replay") if abs(v[k] - v["R"]) > 0.25]
    K_(all(x_ > 0 for x_ in misses), "archive.every_miss_overstates", min(misses))
    rec["archive_totals"] = {k: round(100 * (sum(v[k] for v in arch.values()) / sum(v["R"] for v in arch.values()) - 1), 1)
                             for k in ("render", "replay")}
    K_(all(round(v["replay"] + 1e-9, 1) == v["published"] for v in arch.values()), "archive.published_is_replay")
    cols = ["policy_family", "inputs", "logger_version", "traffic_share_pct", "duration_days", "cells_in_scope",
            "offline_estimate_published"]
    t3, t7 = T[T.test_id == "T3"].iloc[0], T[T.test_id == "T7"].iloc[0]
    K_(all(t3[c] == t7[c] for c in cols), "archive.twins_identical", [(c, t3[c], t7[c]) for c in cols])
    K_(t3.realised_lift / t7.realised_lift >= 2.0, "archive.twins_apart", (t3.realised_lift, t7.realised_lift))
    K_(abs(arch["T3"]["sess"] - 5.6) <= 0.25 and abs(arch["T7"]["sess"] - 2.5) <= 0.25 and
       abs(arch["T7"]["render"] - 2.5) > 0.25 and abs(arch["T7"]["replay"] - 2.5) > 0.25, "archive.twins_only_sessions")
    K_(not T.inputs.str.contains("save|watch", case=False).any(), "archive.no_archived_ranker_read_saves")
    for tid, g in A_hidden.groupby("test_id"):
        Tt, Cc = g[g.arm == "test"], g[g.arm == "control"]
        wl = ((Tt.watched_orders / Tt.p).sum() - (Cc.watched_orders / Cc.p).sum()) / len(g) * 1000
        K_(abs(wl) <= 0.1, f"archive.blind.{tid}", wl)
        kept = ((Tt.y + Tt.followup_orders) / Tt.p).sum() / len(g) * 1000 - ((Cc.y + Cc.followup_orders) / Cc.p).sum() / len(g) * 1000
        K_(abs(kept - arch[tid]["R"]) <= 0.25, f"archive.clean_data_kept_reproduces.{tid}", (kept, arch[tid]["R"]))
    fam_of = {A_: "Two-tower personaliser", B_: "Trending boost", C_: "Sequence model", D_: "Local pickup radius",
              E_: "Sequence model", F_: "Seller-diversity cap"}
    transfer = {r: T[T.policy_family == f].realised_lift.mean() for r, f in fam_of.items()}
    K_(max(transfer, key=transfer.get) == A_, "archive.lookup_transfer_names_decoy",
       {L[r]: round(v, 2) for r, v in transfer.items()})
    rec["lookup_transfer"] = {L[r]: round(v, 2) for r, v in transfer.items()}
    K_(rec["rungs"][4]["leader"] == "E" and rec["rungs"][3]["leader"] == "B", "clean_data.answer_E_naive_B")

    # ---------------------------------------------------------------- per-cell rounding before pooling
    cells_k = A.per_cell(S, y_kept)
    Nc = np.array([(S.cell == c).sum() for c in range(8)], float)
    for r in (E_, B_):
        pooled_rounded = sum(Nc[c] / Nc.sum() * round(cells_k[(r, c)] - cells_k[("HC-24", c)], 1) for c in range(8))
        K_(same_bin(pooled_rounded, A.est(S, y_kept, "session_ipw")[r]), f"rounding.per_cell_first.{L[r]}",
           pooled_rounded)

    # ---------------------------------------------------------------- asks
    res = K.compute(tgt, M)
    # the headline on the slot's own planned cell mix converges with the logged window's
    hl, hs = res["headline_logged_mix"], res["headline_slot_mix"]
    K_(abs(hl[E_] - e_k) < 1e-9 and abs(hl[B_] - b_k) < 1e-9, "headline.logged_mix_is_the_estimator")
    K_(same_bin(hs[E_], e_k) and same_bin(hs[B_], b_k) and same_bin(hs[E_] - hs[B_], e_k - b_k) and
       min(bin_dist(hs[E_]), bin_dist(hs[B_]), bin_dist(hs[E_] - hs[B_])) >= 0.02, "headline.C1_slot_mix",
       (hs[E_], hs[B_]))
    other_mix = {}
    for nm, a in (("first_release", res["arm_sessions_r1"]), ("twelve_weeks_app", res["arm_sessions_12wk"]),
                  ("both", res["arm_sessions_r1_12wk"])):
        sm = a / a.sum()
        other_mix[nm] = {L[r]: round(float(sum(sm[c] * res["orders_kept"][(r, c)] for c in range(8))), 4)
                         for r in (E_, B_)}
    rec["headline"] = dict(logged_mix={L[r]: round(hl[r], 4) for r in P.POLICIES},
                           slot_mix={L[r]: round(hs[r], 4) for r in P.POLICIES}, slot_mix_wrong_traffic=other_mix)
    K_(res["price_routes_agree"], "ask1.price_paid_routes_agree")
    gold = res["fee"]
    dists = {k: bin_dist(v) for k, v in gold.items()}
    K_(min(dists.values()) >= 0.035, "ask1.cells_mid_bin", min(dists.values()))
    off_round = min(abs(v - round(v, 1)) for v in gold.values())
    K_(off_round >= 0.0049, "ask1.cells_off_the_round_value", round(off_round, 4))
    small = [k for k, v in gold.items() if abs(v) < 1.0]
    K_(len(small) <= 4, "ask1.small_cells", [(L[r], c, round(gold[(r, c)], 2)) for r, c in small])
    # FX's three states by every reading of the four hazards (47 wrong readings), and the natural read, carry
    # every cell out of its bin
    gen_gold, gen_combos = W.fee_grid_gen
    K_(max(abs(gen_gold[k] / 100 - gold[(P.RANKERS[k[0]], k[1])]) for k in gen_gold) < 1e-6,
       "ask1.generator_and_files_agree.golden")
    clear = []
    for key, g in res["fee_combos"].items():
        stay = [k for k in gold if same_bin(g[k], gold[k])]
        K_(not stay, f"ask1.subset.{'-'.join(key)}", stay)
        clear += [outside(g[k], gold[k]) for k in gold]
        gg = gen_combos[key]
        K_(max(abs(gg[k] / 100 - g[(P.RANKERS[k[0]], k[1])]) for k in gg) < 1e-6,
           f"ask1.generator_and_files_agree.{'-'.join(key)}")
    nat_stay = [k for k in gold if same_bin(res["fee_natural"][k], gold[k])]
    K_(not nat_stay, "ask1.natural_read_moves_every_cell", nat_stay)
    clear += [outside(res["fee_natural"][k], gold[k]) for k in gold]
    K_(len(res["fee_combos"]) == 47, "ask1.readings_47", len(res["fee_combos"]))
    K_(min(clear) >= 0.02, "ask1.devices_clear_by_0.02", round(min(clear), 4))
    rec["ask1_device_min_clearance"] = round(float(min(clear)), 4)
    nearest = min((outside(g[k], gold[k]), "-".join(key), L[k[0]], P.CELL_NAMES[k[1]])
                  for key, g in res["fee_combos"].items() for k in gold)
    rec["ask1_nearest_reading"] = [round(float(nearest[0]), 4)] + list(nearest[1:])
    # FX: the slot runs on the logged window's cover before 1 March and on full cover from it; each cell's share
    # of the arm's planned sessions before the change is its share of the slot's weeks (and days), so the blends
    # by planned sessions, by weeks and by days file one grid
    shares = res["pre_change_share"]
    K_(max(abs(shares[c] - (0.6 if c < 4 else 2 / 3)) for c in range(8)) < 5e-4, "FX.pre_change_shares",
       [round(float(x_), 6) for x_ in shares])
    wb = res["fee_week_blend"]
    K_(all(same_bin(wb[k], gold[k]) for k in gold) and max(abs(wb[k] - gold[k]) for k in gold) < 0.002,
       "FX.C1_blend_by_weeks_days_sessions", max(abs(wb[k] - gold[k]) for k in gold))
    for nm, key in (("logged_cover_throughout", ("right", "right", "old", "right", "right")),
                    ("full_cover_throughout", ("right", "right", "new", "right", "right"))):
        g = res["fee_combos"][key]
        K_(all(not same_bin(g[k], gold[k]) for k in gold), f"FX.{nm}_moves_every_cell")
        rec[f"FX_{nm}_min_clear"] = round(float(min(outside(g[k], gold[k]) for k in gold)), 4)
    jan = res["fee_app_from_january"]
    rec["FX_app_blend_from_january_cells_moved"] = int(sum(not same_bin(jan[k], gold[k]) for k in gold))
    K_(all(same_bin(jan[k], gold[k]) for k in gold if k[1] >= 4), "FX.app_weeks_touch_app_cells_only")
    rec["FX_pre_change_share"] = [round(float(x_), 6) for x_ in shares]
    rec["fee_old_cover"] = {f"{L[r]}|{P.CELL_NAMES[c]}": round(v, 3) for (r, c), v in res["fee_old_cover"].items()}
    rec["fee_full_cover"] = {f"{L[r]}|{P.CELL_NAMES[c]}": round(v, 3) for (r, c), v in res["fee_full_cover"].items()}
    # VAT taken off order by order to the cent files the same grid
    vp = res["fee_vat_per_order"]
    inside = [-outside(vp[k], gold[k]) for k in gold]
    K_(min(inside) >= 0.01, "ask1.C1_vat_per_order", round(min(inside), 4))
    rec["ask1_vat_per_order_min_inside"] = round(float(min(inside)), 4)
    for nm, floor_ in (("fee_charged", 40), ("fee_drop_pickups", 36), ("fee_every_offer", 36), ("fee_old_tariff", 40),
                       ("fee_vat_off_gross", 36)):
        moved = sum(not same_bin(res[nm][k], gold[k]) for k in gold)
        K_(moved >= floor_, f"ask1.over_cleaner.{nm}", moved)
        rec[f"ask1_{nm}_cells_moved"] = int(moved)
    b_cells = [(B_, c) for c in range(8) if abs(res["orders_insession"][(B_, c)] - res["orders_kept"][(B_, c)]) > 1e-9]
    moved_b = [k for k in b_cells if not same_bin(res["fee_insession_right"][k], gold[k])]
    K_(len(b_cells) >= 4 and len(moved_b) >= 4 and
       all(same_bin(res["fee_insession_right"][k], gold[k]) for k in gold if k[0] != B_),
       "ask1.in_session_basis_moves_B_cells_only", (len(b_cells), len(moved_b)))
    rec["ask1_in_session_B_cells_moved"] = [P.CELL_NAMES[c] for _, c in moved_b]
    rec["ask1"] = {f"{L[r]}|{P.CELL_NAMES[c]}": round(v, 3) for (r, c), v in gold.items()}
    rec["ask1_small_cells"] = [f"{L[r]}|{P.CELL_NAMES[c]}" for r, c in small]
    split = res["no_payment_split"]
    rec["no_payment_split"] = split
    # ask 2
    inside_readings = []
    for r in P.POLICIES:
        for nm in ("tot_orders", "tot_fee"):
            x_ = res[nm][r]
            K_(20 <= bin_dist(x_, 100) <= 45, f"ask2.mid_bin.{nm}.{L[r]}", x_)
        readings = [(nm, res[nm][r], res["tot_orders"][r]) for nm in
                    ("tot_orders_r1", "tot_orders_12wk", "tot_orders_r1_12wk", "tot_orders_natural", "tot_orders_pooled")]
        readings += [("tot_fee_pooled", res["tot_fee_pooled"][r], res["tot_fee"][r]),
                     ("tot_fee_natural", res["tot_fee_natural"][r], res["tot_fee"][r])]
        readings += [("fee|" + "|".join(str(z) for z in key), v[r], res["tot_fee"][r])
                     for key, v in res["tot_fee_subsets"].items()]
        clr = []
        for nm, x_, g_ in readings:
            o_ = outside(x_, g_, 100)
            clr.append((abs(o_), nm, round(x_, 1), round(g_, 1)))
            if o_ < 0:
                inside_readings.append(f"{L[r]}|{nm}")
        K_(min(clr)[0] >= 5 and len(clr) == 5 + 2 + 191, f"ask2.every_reading_clear_of_the_edges.{L[r]}", min(clr))
        K_(abs(res["tot_orders_r1"][r] - res["tot_orders"][r]) >= 100, f"ask2.P2_moves_100.{L[r]}",
           res["tot_orders_r1"][r] - res["tot_orders"][r])
    pooled_inside = [z for z in inside_readings if "pooled" in z]
    device_inside = [z for z in inside_readings if "pooled" not in z]
    K_(len(device_inside) <= 6 and not any("tot_orders" in z for z in device_inside),
       "ask2.device_readings_out_of_the_hundred", device_inside)
    fx_alone = [z for z in device_inside if z.split("|", 1)[1] in ("fee|False|False|right|right|old|right|right",
                                                                  "fee|False|False|right|right|new|right|right")]
    K_(len(fx_alone) <= 1, "ask2.FX_alone_moves_five_fee_totals_of_six", fx_alone)
    rec["ask2_FX_alone_inside"] = fx_alone
    rec["ask2_readings_inside_the_hundred"] = dict(pooled=pooled_inside, devices=device_inside)
    tot_in = K.totals(res["orders_insession"], res["arm_sessions"])
    K_(not same_bin(tot_in[B_], res["tot_orders"][B_], 100) and
       all(abs(tot_in[r] - res["tot_orders"][r]) < 1e-6 for r in P.POLICIES if r != B_),
       "ask2.in_session_basis_moves_B_only", {L[r]: round(tot_in[r], 1) for r in P.POLICIES})
    rec["ask2_orders_in_session_basis"] = {L[r]: round(tot_in[r], 1) for r in P.POLICIES}
    K_(len(res["tot_fee_subsets"]) == 191, "ask2.fee_readings_191", len(res["tot_fee_subsets"]))
    rec["ask2"] = {"orders": {L[r]: round(v, 1) for r, v in res["tot_orders"].items()},
                   "fee": {L[r]: round(v, 1) for r, v in res["tot_fee"].items()},
                   "arm_sessions": [int(round(x_)) for x_ in res["arm_sessions"]],
                   "orders_first_release": {L[r]: round(v, 1) for r, v in res["tot_orders_r1"].items()},
                   "orders_12_weeks_app": {L[r]: round(v, 1) for r, v in res["tot_orders_12wk"].items()},
                   "orders_pooled": {L[r]: round(v, 1) for r, v in res["tot_orders_pooled"].items()},
                   "orders_natural": {L[r]: round(v, 1) for r, v in res["tot_orders_natural"].items()},
                   "fee_pooled": {L[r]: round(v, 1) for r, v in res["tot_fee_pooled"].items()},
                   "fee_natural": {L[r]: round(v, 1) for r, v in res["tot_fee_natural"].items()}}
    r1n, r2n, cur = K.load_traffic(tgt)
    j = r1n.merge(r2n, on=["year", "week", "platform", "band"], suffixes=("_r1", "_r2"))
    pw1 = j.groupby(["year", "week", "platform"]).sessions_r1.sum()
    pw2 = j.groupby(["year", "week", "platform"]).sessions_r2.sum()
    K_((pw1 == pw2).all(), "P2.platform_week_totals_unchanged")
    moved = (j[j.band >= 2].sessions_r2.sum() - j[j.band >= 2].sessions_r1.sum()) / j.sessions_r2.sum()
    K_(abs(moved - P.R2_MOVED_SHARE) < 0.004, "P2.share_moved", round(moved, 4))
    rec["R2_moved_share"] = round(float(moved), 4)

    # ---------------------------------------------------------------- referee and hygiene battery
    pay = pd.read_parquet(os.path.join(tgt, Wr.F_PAYMENTS))
    o, w = K.load_fee_path(tgt, M)
    fin = pd.read_excel(os.path.join(tgt, D.F_FINANCE), header=None)
    hdr = int(np.flatnonzero(fin[0].astype(str).str.strip() == "Month")[0])
    body = fin.iloc[hdr + 1:hdr + 7]
    names = {"July 2026": "2026-07", "August 2026": "2026-08", "September 2026": "2026-09"}
    tariffs = pd.read_csv(os.path.join(tgt, D.F_TARIFF))
    starts = pd.to_datetime(tariffs.ingangsdatum).to_numpy()
    fixed_c = np.round(tariffs.vast_bedrag_eur.to_numpy() * 100).astype(int)
    prot = o[~o.inperson].copy()
    prot["booked"] = np.where(prot.paid_through, prot.captured_at, prot.ordered_at)
    idx_t = np.searchsorted(starts, prot.booked.to_numpy(), side="right") - 1
    prot["fee_c"] = fixed_c[idx_t] + 5 * np.round(prot.price_paid.to_numpy()).astype(int)
    prot["m"] = pd.to_datetime(prot.booked).dt.strftime("%Y-%m")
    q3 = prot[prot.m.isin(names.values())]
    gq = q3.groupby(["m", "platform"]).agg(n=("order_id", "size"), fee=("fee_c", "sum"), item=("price_paid", "sum"))
    tie = all(abs(round(gq.loc[(names[r[0]], r[1]), "fee"] / 100 / (1 + P.VAT_RATE), 2) - float(r[4])) < 0.005 and
              int(gq.loc[(names[r[0]], r[1]), "n"]) == int(r[2]) and
              abs(gq.loc[(names[r[0]], r[1]), "item"] - float(r[3])) < 0.005 for r in body.itertuples(index=False))
    K_(tie, "referee.ties_to_every_protected_purchase_excl_VAT")
    # the provider's charged fees alone, with or without the VAT, do not tie
    pq3 = pay.assign(m=pay.captured_at.dt.strftime("%Y-%m"))
    pq3 = pq3[pq3.m.isin(names.values())]
    gross_pay = float(pq3.buyer_protection_fee_eur.sum())
    stated = float(body[4].astype(float).sum())
    K_(abs(gross_pay / stated - 1) > 0.10 and abs(gross_pay / 1.21 / stated - 1) > 0.05,
       "referee.payments_alone_do_not_tie", (round(gross_pay, 2), round(stated, 2)))
    # the statement certifies the logged window's cover: charging every pickup, as the slot does from 1 March,
    # overstates it
    allp = o.copy()
    allp["booked"] = np.where(allp.paid_through, allp.captured_at, allp.ordered_at)
    idx_a = np.searchsorted(starts, allp.booked.to_numpy(), side="right") - 1
    allp["fee_c"] = fixed_c[idx_a] + 5 * np.round(allp.price_paid.to_numpy()).astype(int)
    allp["m"] = pd.to_datetime(allp.booked).dt.strftime("%Y-%m")
    full_q3 = float(allp[allp.m.isin(names.values())].fee_c.sum()) / 100 / (1 + P.VAT_RATE)
    K_(full_q3 / stated - 1 > 0.01, "referee.full_cover_does_not_tie", round(full_q3 / stated - 1, 4))
    rec["referee_full_cover_over"] = round(100 * (full_q3 / stated - 1), 2)
    rec["referee"] = dict(stated=round(stated, 2), payments_gross=round(gross_pay, 2),
                          payments_net=round(gross_pay / 1.21, 2),
                          balance_share_of_protected=round(float((~q3.paid_through).mean()), 4))
    offf = pd.read_csv(os.path.join(tgt, K.offers_file(tgt)))
    K_(O.order_id.is_unique and pay.payment_id.is_unique and pay.order_id.is_unique and offf.offer_id.is_unique,
       "hygiene.keys_unique")
    K_(pay.order_id.isin(O.order_id).all(), "hygiene.every_payment_has_an_order")
    ob = offf.merge(O[["buyer_id", "listing_id"]], on=["buyer_id", "listing_id"], how="left", indicator=True)
    K_((ob["_merge"] == "both").all(), "hygiene.every_offer_has_an_order")
    K_(not O.duplicated(["buyer_id", "listing_id"]).any(), "hygiene.no_duplicate_purchases")
    ship = o[o.delivery == "shipped"]
    bal = ship.groupby(ship.ordered_at.dt.strftime("%Y-%m")).balance.mean()
    K_(bal.between(0.06, 0.08).all(), "hygiene.balance_share_steady_by_month", bal.round(4).to_dict())
    K_(not o[o.inperson].paid_through.any() and (o[o.balance].delivery == "shipped").all(),
       "hygiene.no_payment_is_pickup_in_person_or_shipped_on_balance")
    # a watched listing is never paid at the handover, so no brought-forward order changes cover on 1 March
    wl = S[["buyer_id", "watchlist_at_start"]].copy()
    wl["listing_id"] = wl.watchlist_at_start.str.split()
    wl = wl.explode("listing_id").dropna(subset=["listing_id"])
    wl["listing_id"] = wl.listing_id.astype("int64")
    ow = o.merge(wl[["buyer_id", "listing_id"]], on=["buyer_id", "listing_id"], how="inner")
    K_(len(ow) > 0 and not ow.inperson.any(), "world.watched_listings_never_paid_at_the_handover", len(ow))

    # ---------------------------------------------------------------- separation and necessity
    declared_main = {Wr.F_RENDER, Wr.F_RANKINGS, Wr.F_ORDERS, D.F_ARCHIVE, D.F_CHARTER, D.F_COMMIT, D.F_REGISTER,
                     D.F_FIELDS}
    device_files = {Wr.F_PAYMENTS, K.offers_file(tgt), D.F_TARIFF, D.F_TERMS, D.F_MINUTES, K.F_WEEKLY, K.F_R2,
                    D.F_RELEASES, D.F_CAPACITY, D.F_ICS, D.F_FINANCE}
    K_(not (declared_main & device_files), "separation.files")
    main_cols = {"order_id", "buyer_id", "listing_id", "ordered_at", "channel", "home_session_id"}
    K_(not ({"asking_price_eur", "delivery", "platform", "category"} & main_cols), "separation.columns")
    M2 = A.load_main(tgt)
    M2.O["asking_price_eur"] = M2.O.asking_price_eur.sample(frac=1.0, random_state=1).to_numpy()
    M2.O["delivery"] = "shipped"
    yk2 = A.followup(M2, hours=21 * 24).astype(float)
    v2 = A.est(M2.S, yk2, "session_ipw")
    g2 = A.guardrail(M2.S, A.tile_orders(M2).astype(float))
    K_(abs(v2[E_] - e_k) < 1e-12 and abs(v2[B_] - b_k) < 1e-12 and
       sorted((L[r], c) for (r, c), v in g2.items() if v < -1.5) == [("A", 7), ("C", 0)],
       "necessity.devices_do_not_move_the_call")
    rec["device_rows_in_main_population"] = 0

    # ---------------------------------------------------------------- pair simulation
    rec["pair"] = pair_simulation(res, gold)
    K_(rec["pair"]["pair"] <= 40.0, "pair.at_or_under_40", rec["pair"])

    # ---------------------------------------------------------------- pack
    files = sorted(os.listdir(tgt))
    exts = {os.path.splitext(f)[1] for f in files}
    K_(len(files) >= 10 and len(exts) >= 3, "gates.files_formats", (len(files), sorted(exts)))
    K_(len(M.R) >= 25_000, "gates.volume")
    K_(len(distractors) >= 2 and all(d in files for d in distractors), "gates.distractors_shipped")
    blob = {}
    for f in files:
        p = os.path.join(tgt, f)
        if f.endswith((".md", ".txt", ".csv", ".json", ".ics")) and os.path.getsize(p) < 2_000_000:
            blob[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".pdf"):
            from pypdf import PdfReader
            blob[f] = "\n".join(pg.extract_text() for pg in PdfReader(p).pages)
        elif f.endswith(".docx"):
            from docx import Document
            blob[f] = "\n".join(x_.text for x_ in Document(p).paragraphs)
        elif f.endswith(".xlsx") and f != D.F_ARCHIVE:
            blob[f] = "\n".join(pd.read_excel(p, sheet_name=None, header=None)[s].astype(str).to_csv() for s in
                                pd.ExcelFile(p).sheet_names)
    blob[D.F_ARCHIVE + ":tests+notes"] = T.to_csv() + pd.read_excel(os.path.join(tgt, D.F_ARCHIVE), sheet_name="notes",
                                                                       header=None).to_csv()
    alltext = "\n".join(blob.values())
    K_("distractor" not in alltext.lower() and not any("distractor" in f.lower() for f in files),
       "gates.distractors_unnamed_in_pack")
    bad = re.compile(r"\b(trap|decoy|golden|stump|rung|ladder|answer key|synthetic|generated by|placeholder|lorem|"
                     r"python-docx|openpyxl|reportlab|matplotlib|xlsxwriter|pyarrow|seed|come-back|comeback)\b", re.I)
    hits_ = {f: bad.findall(t) for f, t in blob.items() if bad.search(t)}
    K_(not hits_, "leak.author_vocabulary", hits_)
    K_("\u2014" not in alltext, "leak.no_em_dash")
    for f, t in blob.items():
        ids = [r for r in P.POLICIES if r in t]
        if len(ids) >= 3:
            K_(f == D.F_REGISTER, f"no_ranking_artifact.{f}", ids)
    reg = json.load(open(os.path.join(tgt, D.F_REGISTER), encoding="utf-8"))
    K_(not re.search(r"\d+\.\d+ (extra )?orders|lift", json.dumps(reg).lower().replace("lift", "LIFTX"))
       or "liftx" not in json.dumps(reg).lower(), "register.no_lift")
    facts = {
        "lift_definition": r"change in orders placed by the arm's buyers during the test",
        "rate_definition": r"orders placed from the carousel tiles it served",
        "seven_day_rule": r"kept off it in their later sessions for seven days",
        "reproduction_clause": r"within 0\.25 extra orders",
        "cell_table": r"730 days and over",
        "floor": r"at least 12 of every 100 tiles",
        "slot_share": r"10 per cent of logged-in carousel sessions",
        "tariff_deferral": r"deferred to the Q2 2027 review",
        "app_gating": r"first app release on or after",
        "r2_replaces": r"R2 replaces the first release",
        "cell_by_cell_planning": r"cell by cell, in the cells of the experimentation charter",
        "fee_basis": r"percentage of the\s+price you pay",
        "change_clause": r"approved by the Vouwlijn pricing committee",
        "vat_in_the_fee": r"includes 21 per cent VAT",
        "balance_payment": r"your Vouwlijn balance",
        "provider_captures_only": r"card and iDEAL payment the payment provider captured",
        "checkout_change": r"checkout change of 1 March 2027",
        "in_person_cover": r"pay the seller directly, the purchase is not covered",
    }
    single = {}
    for k, pat in facts.items():
        where = [f for f, t in blob.items() if re.search(pat, re.sub(r"\s+", " ", t))]
        single[k] = where
        K_(len(where) == 1, f"single_statement.{k}", where)
    rec["single_statement"] = single
    idx = blob[D.F_INDEX]
    listed = set(re.findall(r"^\| ([^|]+?) \|", idx, re.M)) - {"file", "---"}
    K_(listed == set(files) - {D.F_INDEX}, "H9.index_covers_every_file", sorted(set(files) ^ (listed | {D.F_INDEX})))
    allow = {D.F_TARIFF, D.F_ICS, D.F_CAPACITY, D.F_MINUTES}
    late = sorted(f for f, t in blob.items() if any(d > P.PACK_DATE.isoformat() for d in
                                                     re.findall(r"\b20\d\d-\d\d-\d\d\b", t)))
    K_(set(late) <= allow, "H16.forward_dates_allow_list", late)
    K_(scrub_rc[1] == 0 and "clean" in scrub_rc[2], "H1.containers_clean", scrub_rc[2][-200:])
    rows = [len(M.R), len(S), len(O), len(pay), len(offf)]
    K_(len(set(rows)) == len(rows) and all(x_ % 1000 for x_ in rows[2:]), "tells.row_counts", rows)
    drawn = ["Saar Dries", "Tygo Knoers", "Livia Verhaar", "Fabian Stoffel", "Kayleigh Zeemans", "Amélie Middelkoop",
             "Esila Stichter", "Lindsey Mudden", "Rik Breugelensis", "Britt Tins", "Zoey Joosten", "Jasmijn Zijlemans",
             "Tycho Feenstra", "Yasmine Billung", "Ali Maas", "Stef Steenbakkers", "Evy Mathieu"]
    rec["personas"] = drawn
    K_(all(n in alltext for n in drawn[:6]), "personas.core_present")
    failed = [n for n, ok, _ in K_.items if not ok]
    if failed:
        raise AssertionError(f"{len(failed)} assertions failed: {failed}")
    rec["assertions"] = len(K_.items)
    rec["assertion_names"] = [n for n, _, _ in K_.items]
    return rec


def pair_simulation(res, gold):
    """Two answer sheets at the planning weights (38 / 7 / 55 over 4 call, 4 file and 64 ask criteria): the
    response that lands the call and the best one that misses it on the guardrail count (it files the
    session-sequence model). Both run the habitual battery, net the velocity boost's brought-forward orders,
    take the restatement and the app release gate, and price the fee the way round 2 did, reconciled to the cent
    with Finance's Q3 statement (slot tariff, price paid, VAT out, balance purchases charged, pickups paid in person
    uncharged) and carried through the slot; a fee cell or total counts only where that path lands in the golden
    bin. Full cover through the whole slot (the 1 March line found, its date not) is priced beside it."""
    w_call, w_if, w_ask = 38 / 4, 7 / 4, 55 / 64
    paths = {"reconciled_basis_carried": ("right", "right", "old", "right", "right"),
             "full_cover_throughout": ("right", "right", "new", "right", "right")}
    kept = {}
    for nm, key in paths.items():
        g = res["fee_combos"][key]
        cells = sum(same_bin(g[k], gold[k]) for k in gold)
        tf = res["tot_fee_subsets"][(False, False) + key]
        tots = sum(same_bin(tf[r], res["tot_fee"][r], 100) for r in P.POLICIES)
        kept[nm] = (int(cells), int(tots))
    cells, tots = kept["reconciled_basis_carried"]
    # cracker: the call block, the files, the heatmap's four parts, the six order totals
    cracker = 4 * w_call + 4 * w_if + (4 + 6 + cells + tots) * w_ask
    # mirror: three call criteria survive (the exclusions it names), the files, the euro scale, the six order
    # totals; its hatching misses the session-sequence model's cell and its outline and title name C
    mirror = 3 + 4 * w_if + (1 + 6 + cells + tots) * w_ask
    exposure = 4 * w_call + 4 * w_if + (4 + 6 + 48 + 6) * w_ask
    return dict(cracker=round(cracker, 1), mirror=round(mirror, 1), pair=round((cracker + mirror) / 2, 1),
                fee_kept_by_path=kept,
                exposure_if_one_top_response_blends=round((exposure + mirror) / 2, 1))
