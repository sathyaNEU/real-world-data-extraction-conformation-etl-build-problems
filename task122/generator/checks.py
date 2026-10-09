"""task122 generator: every assertion the build makes, on the files as written (read back from disk),
plus the few facts only the generator can see (the archive's hidden layers). Fails loudly at the
first assertion that does not hold, and returns the build record (every figure the design note
quotes).
"""
import itertools
import json
import os
import re
import subprocess
import sys

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
            raise AssertionError(f"[{name}] {detail}")
        return ok


def bin_dist(x, unit=0.1):
    """Distance from x to the nearest rounding boundary of its bin (bins of width unit)."""
    k = np.floor(x / unit + 0.5)
    return min(abs(x - (k - 0.5) * unit), abs((k + 0.5) * unit - x))


def same_bin(a, b, unit=0.1):
    return np.floor(a / unit + 0.5) == np.floor(b / unit + 0.5)


def reading(M, y_basis, y_in, est_kind, guard, floor_grain):
    S = M.S
    vals = A.est(S, y_basis, est_kind)
    ok, g, f, b = A.conditions(S, y_basis, y_in, vals, est_kind, guard, floor_grain)
    first, second, margin = A.leader(vals, ok)
    return vals, ok, first, second, margin


def run_all(W, meta, A_hidden, tgt, root, distractors, scrub_rc):
    K_ = Checks()
    rec = {}
    tgt = str(tgt)
    M = A.load_main(tgt)
    S = M.S
    y_in = S.y.to_numpy().astype(float)
    y_kept = A.followup(M, hours=21 * 24).astype(float)

    # ---------------------------------------------------------------- ties and identities
    K_(len(S) == 150_400 and len(M.R) >= 25_000, "spine.size", (len(S), len(M.R)))
    K_((A.in_session_from_orders(M) == S.y.to_numpy()).all(), "tie.render_log_to_orders_by_session")
    fam = {k: A.est(S, y_in, k) for k in A.SESSION_GRAIN}
    K_(all(abs(fam[k][r] - fam["session_ipw"][r]) < 1e-9 for k in A.SESSION_GRAIN for r in P.POLICIES),
       "estimators.session_grain_identical")
    cnt = S.groupby(["cell", "ranker"]).size()
    K_(all(cnt[(c, r)] == round(P.N_CELL[c] * P.PI[c, P.RANKERS.index(r)]) for c in range(8) for r in P.RANKERS),
       "logger.quota_exact")
    rec["sessions"], rec["renders"] = int(len(S)), int(len(M.R))

    # ---------------------------------------------------------------- the five rungs
    rungs = [("replay_rows", "platform", y_in, "rendered", D_, 1.20),
             ("render_weights", "platform", y_in, "rendered", A_, 1.20),
             ("session_ipw", "platform", y_in, "ranking", C_, 1.15),
             ("session_ipw", "eight", y_in, "ranking", B_, 1.20),
             ("session_ipw", "eight", y_kept, "ranking", E_, 1.50)]
    rec["rungs"] = []
    for i, (ek, gr, yb, fg, want, mmin) in enumerate(rungs):
        vals, ok, first, second, margin = reading(M, yb, y_in, ek, gr, fg)
        K_(first == want and margin >= mmin, f"rung{i}.leader",
           (i, L[first], L[second], round(margin, 3), {L[r]: round(v, 3) for r, v in vals.items()}))
        rank_all = sorted(P.POLICIES, key=lambda r: -vals[r])
        rec["rungs"].append(dict(rung=i, estimator=ek, guardrail=gr, basis="kept" if yb is y_kept else "in-session",
                                 values={L[r]: round(v, 3) for r, v in vals.items()}, leader=L[first],
                                 runner_up=L[second] if second else None, margin=round(margin, 3),
                                 E_rank_all=rank_all.index(E_) + 1,
                                 qualifiers=[L[r] for r in P.POLICIES if ok[r]]))
    pos = [r["E_rank_all"] for r in rec["rungs"]]
    K_(pos[0] == 5 and pos[1] == 4 and pos[2] == 4, "position.E_5th_4th_4th", pos)
    K_(all(r["leader"] != "E" for r in rec["rungs"][:4]), "position.E_leads_no_intermediate_rung")
    second_at = [i for i, r in enumerate(rec["rungs"][:4]) if r["runner_up"] == "E"]
    K_(second_at == [3], "position.E_second_only_at_rung3", second_at)
    v3 = rec["rungs"][3]["values"]
    v4 = rec["rungs"][4]["values"]
    K_(v3["B"] / v3["E"] >= 1.20, "position.rung3_gap", v3["B"] / v3["E"])
    # discriminator dominance
    carried = v3["B"] / v3["E"]
    edge = (v4["E"] / v3["E"]) / (v4["B"] / v3["B"])
    K_(edge >= 1.2 * carried, "dominance", (round(edge, 3), round(carried, 3)))
    rec["dominance"] = dict(carried=round(carried, 3), edge=round(edge, 3), product=round(edge / carried, 3))
    # the call
    e_k, b_k = v4["E"], v4["B"]
    rec["call"] = dict(answer="HC-37", lift=round(e_k, 3), runner_up="HC-33", runner_up_lift=round(b_k, 3),
                       gap=round(e_k - b_k, 3))
    for nm, x in (("E_kept", e_k), ("B_kept", b_k), ("gap", e_k - b_k)):
        K_(bin_dist(x) >= 0.03, f"bins.{nm}", (x, bin_dist(x)))

    # ---------------------------------------------------------------- correction grid (12 cells)
    grid = {}
    want = {("replay_rows", "platform", "in"): D_, ("replay_rows", "platform", "kept"): D_,
            ("replay_rows", "eight", "in"): D_, ("replay_rows", "eight", "kept"): D_,
            ("render_weights", "platform", "in"): A_, ("render_weights", "platform", "kept"): A_,
            ("render_weights", "eight", "in"): B_, ("render_weights", "eight", "kept"): B_,
            ("session_ipw", "platform", "in"): C_, ("session_ipw", "platform", "kept"): C_,
            ("session_ipw", "eight", "in"): B_, ("session_ipw", "eight", "kept"): E_}
    for (ek, gr, bas), w in want.items():
        fg = "ranking" if ek == "session_ipw" else "rendered"
        vals, ok, first, second, margin = reading(M, y_kept if bas == "kept" else y_in, y_in, ek, gr, fg)
        grid[f"{ek}|{gr}|{bas}"] = dict(leader=L[first], value=round(vals[first], 3),
                                        next=L[second] if second else None,
                                        margin=round(margin, 3) if np.isfinite(margin) else "only qualifier")
        K_(first == w and margin >= 1.15, f"grid.{ek}.{gr}.{bas}", grid[f"{ek}|{gr}|{bas}"])
    rec["correction_grid"] = grid

    # ---------------------------------------------------------------- partial readings
    share_B = (v3["B"] - v4["B"]) / v3["B"]
    flat = {r: v * (1 - share_B) for r, v in v3.items()}
    elig = rec["rungs"][3]["qualifiers"]
    elig_flat = [r for r in elig if flat[r] >= 2.0]
    lead_flat = max(elig_flat, key=lambda r: flat[r])
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
        vals, ok, first, second, margin = reading(M, yw, y_in, "session_ipw", "eight", "ranking")
        win[d] = dict(leader=L[first], E=round(vals[E_], 3), B=round(vals[B_], 3))
    full = min(d for d in range(1, 22) if all(win[x]["E"] == win[21]["E"] and win[x]["B"] == win[21]["B"]
                                                for x in range(d, 22)))
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
    # comparison sets for the anyway rate: every segment a reader can form from the logged sessions
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
        # stratified netting: each session's watched in-session orders netted at its own segment's rate
        qs = S.session_id.map(ser).map(g["mean"]).to_numpy(float)
        qs = np.where(Sw > 0, qs, 0.0)          # a segment with no unshown watched listing has nothing to net
        K_(not np.isnan(qs).any(), f"anyway.every_netted_session_has_a_rate.{col}")
        vs = A.est(S, y_in - qs * Sw, "session_ipw")
        strat[col] = (round(vs[E_], 4), round(vs[B_], 4))
        K_(same_bin(vs[E_], e_k) and same_bin(vs[B_], b_k), f"anyway.stratified_netting.{col}",
           (col, vs[E_], vs[B_]))
    rec["anyway_rates"] = rates
    rec["anyway_stratified"] = strat
    exact = [v[0] for col in ("cell", "ranker", "cell_ranker", "platform", "tenure_band") for v in rates[col].values()]
    K_(all(abs(x - 0.625) < 1e-9 for x in exact), "anyway.exact_in_every_charter_cut_and_arm")
    seg = [v[0] for col in ("renders", "watch_size", "weekday", "iso_week", "half") for v in rates[col].values()
           if v[1] >= 2000]
    K_(all(abs(x - 0.625) <= 0.01 for x in seg), "anyway.segments_close", (min(seg), max(seg)))
    rec["anyway_segment_range"] = (min(seg), max(seg))
    # a rate measured on one natural sub-population and applied to every session
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
    # the thinnest boundary, recorded rather than asserted: the most extreme single segment's rate
    # applied to every session (no reading does this; it bounds what any segment can do)
    ext = {}
    for x in (min(seg), max(seg)):
        vx = A.est(S, y_in - x * Sw, "session_ipw")
        ext[str(x)] = (round(vx[E_], 4), round(vx[B_], 4))
    rec["anyway_extreme_segment_applied_globally"] = ext
    K_(all(same_bin(v[0], e_k) for v in ext.values()), "anyway.E_independent_of_rate", ext)
    rec["route2_q"] = q

    # ---------------------------------------------------------------- guardrail, floor, bar
    breaches = {}
    for basis_nm, yb in (("in", y_in), ("kept", y_kept)):
        for rw in (False, True):
            g = A.guardrail(S, yb, y_in, weighted_by_renders=rw)
            br = sorted((L[r], c) for (r, c) in g if g[(r, c)] < -1.5)
            breaches[f"{basis_nm}|{'render' if rw else 'session'}"] = br
            K_(br == [("A", 7), ("C", 0)], f"guardrail.breaches.{basis_nm}.{rw}", br)
            others = [g[k] for k in g if (L[k[0]], k[1]) not in (("A", 7), ("C", 0))]
            K_(min(others) >= -0.9, f"guardrail.others_clear.{basis_nm}.{rw}", min(others))
            for coarse in ("platform", "tenure", "pooled"):
                gc = A.guardrail(S, yb, y_in, weighted_by_renders=rw, coarse=coarse)
                K_(min(gc.values()) >= -0.8, f"guardrail.coarse.{coarse}.{basis_nm}.{rw}", min(gc.values()))
    g0 = A.guardrail(S, y_in, y_in)
    rec["guardrail_pct"] = {f"{L[r]}|{P.CELL_NAMES[c]}": round(v, 3) for (r, c), v in g0.items()}
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
    # halves
    half = (S.started_at < pd.Timestamp(P.HALF_SPLIT)).to_numpy()
    for nm, yb in (("in", y_in), ("kept", y_kept)):
        h1 = A.est(S[half].reset_index(drop=True), yb[half], "session_snipw")
        h2 = A.est(S[~half].reset_index(drop=True), yb[~half], "session_snipw")
        dmax = max(abs(h1[r] - h2[r]) for r in P.POLICIES)
        K_(dmax <= 0.25, f"halves.{nm}", round(dmax, 3))
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
        strat = 0.0
        for c, gc in df.groupby(["platform", "tenure_band"]):
            strat += len(gc) / N * (gc[gc.arm == "test"].y.mean() - gc[gc.arm == "control"].y.mean()) * 1000
        arch[t.test_id] = dict(R=float(t.realised_lift), sess=s, snip=snip, clip=clip, strat=strat, render=rw,
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
    K_(all(x > 0 for x in misses), "archive.every_miss_overstates", min(misses))
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
    # lookup transfer by resemblance names the two-tower personaliser, a decoy
    fam_of = {A_: "Two-tower personaliser", B_: "Trending boost", C_: "Sequence model", D_: "Local pickup radius",
              E_: "Sequence model", F_: "Seller-diversity cap"}
    transfer = {r: T[T.policy_family == f].realised_lift.mean() for r, f in fam_of.items()}
    K_(max(transfer, key=transfer.get) == A_, "archive.lookup_transfer_names_decoy",
       {L[r]: round(v, 2) for r, v in transfer.items()})
    rec["lookup_transfer"] = {L[r]: round(v, 2) for r, v in transfer.items()}
    # the clean-data repair moves neither answer: the main pack is untouched by it
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
    K_(res["price_routes_agree"], "ask1.price_paid_routes_agree")
    gold = res["fee"]
    dists = {k: bin_dist(v) for k, v in gold.items()}
    K_(min(dists.values()) >= 0.03, "ask1.cells_mid_bin", min(dists.values()))
    small = [k for k, v in gold.items() if abs(v) < 1.0]
    K_(len(small) <= 4, "ask1.small_cells", [(L[r], c, round(gold[(r, c)], 2)) for r, c in small])
    for key, g in res["fee_combos"].items():
        stay = [k for k in gold if same_bin(g[k], gold[k]) and k not in small]
        K_(not stay, f"ask1.subset.{'-'.join(key)}", stay)
    nat_stay = [k for k in gold if same_bin(res["fee_natural"][k], gold[k])]
    K_(not nat_stay, "ask1.natural_read_moves_every_cell", nat_stay)
    for nm in ("fee_charged", "fee_drop_pickups", "fee_every_offer", "fee_old_tariff"):
        moved = sum(not same_bin(res[nm][k], gold[k]) for k in gold)
        K_(moved >= 36, f"ask1.over_cleaner.{nm}", moved)
        rec[f"ask1_{nm}_cells_moved"] = int(moved)
    b_cells = [(B_, c) for c in range(8) if abs(res["orders_insession"][(B_, c)] - res["orders_kept"][(B_, c)]) > 1e-9]
    K_(all(not same_bin(res["fee_insession_right"][k], gold[k]) for k in b_cells) and len(b_cells) >= 4,
       "ask1.in_session_basis_moves_B_cells", len(b_cells))
    # route 2 at the fee level files the same grid (the asks pin the fee, whichever route reaches it)
    rec["ask1"] = {f"{L[r]}|{P.CELL_NAMES[c]}": round(v, 3) for (r, c), v in gold.items()}
    rec["ask1_small_cells"] = [f"{L[r]}|{P.CELL_NAMES[c]}" for r, c in small]
    # ask 2
    for r in P.POLICIES:
        for nm in ("tot_orders", "tot_fee"):
            x = res[nm][r]
            K_(bin_dist(x, 100) >= 20, f"ask2.mid_bin.{nm}.{L[r]}", x)
        for nm in ("tot_orders_r1", "tot_orders_12wk", "tot_orders_r1_12wk", "tot_orders_pooled", "tot_orders_natural"):
            K_(not same_bin(res[nm][r], res["tot_orders"][r], 100), f"ask2.stop.{nm}.{L[r]}",
               (res[nm][r], res["tot_orders"][r]))
        K_(abs(res["tot_orders_r1"][r] - res["tot_orders"][r]) >= 100, f"ask2.P2_moves_100.{L[r]}",
           res["tot_orders_r1"][r] - res["tot_orders"][r])
    stay = [(k, L[r]) for k, v in res["tot_fee_subsets"].items() for r in P.POLICIES
            if same_bin(v[r], res["tot_fee"][r], 100)]
    K_(not stay and len(res["tot_fee_subsets"]) == 31, "ask2.fee_31_subsets", stay[:5])
    rec["ask2"] = {"orders": {L[r]: round(v, 1) for r, v in res["tot_orders"].items()},
                   "fee": {L[r]: round(v, 1) for r, v in res["tot_fee"].items()},
                   "arm_sessions": [int(round(x)) for x in res["arm_sessions"]],
                   "orders_first_release": {L[r]: round(v, 1) for r, v in res["tot_orders_r1"].items()},
                   "orders_12_weeks_app": {L[r]: round(v, 1) for r, v in res["tot_orders_12wk"].items()},
                   "orders_pooled": {L[r]: round(v, 1) for r, v in res["tot_orders_pooled"].items()},
                   "orders_natural": {L[r]: round(v, 1) for r, v in res["tot_orders_natural"].items()}}
    # R2 against the first release
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
    o = M.O.merge(pay, on="order_id", how="left")
    fin = pd.read_excel(os.path.join(tgt, D.F_FINANCE), header=None).iloc[5:11]
    o["m"] = o.captured_at.dt.strftime("%Y-%m")
    q3 = o[o.m.isin(["2026-07", "2026-08", "2026-09"])]
    booked = q3.groupby(["m", "platform"]).buyer_protection_fee_eur.sum().round(2)
    names = {"July 2026": "2026-07", "August 2026": "2026-08", "September 2026": "2026-09"}
    tie = all(abs(booked[(names[r[0]], r[1])] - float(r[4])) < 0.005 for r in fin.itertuples(index=False))
    K_(tie, "referee.ties_to_payments")
    # formula pricing of every order in Q3 overstates it
    allq3 = M.O[M.O.ordered_at.dt.strftime("%Y-%m").isin(["2026-07", "2026-08", "2026-09"])]
    formula = (0.80 + 0.05 * allq3.asking_price_eur).sum()
    over = formula / float(fin[4].sum()) - 1
    K_(over > 0.10, "referee.formula_overstates", round(over, 3))
    rec["referee_overstatement"] = round(float(over), 4)
    offf = pd.read_csv(os.path.join(tgt, K.offers_file(tgt)))
    K_(M.O.order_id.is_unique and pay.payment_id.is_unique and pay.order_id.is_unique and offf.offer_id.is_unique,
       "hygiene.keys_unique")
    K_(pay.order_id.isin(M.O.order_id).all(), "hygiene.every_payment_has_an_order")
    ob = offf.merge(M.O[["buyer_id", "listing_id"]], on=["buyer_id", "listing_id"], how="left", indicator=True)
    K_((ob["_merge"] == "both").all(), "hygiene.every_offer_has_an_order")
    K_(not M.O.duplicated(["buyer_id", "listing_id"]).any(), "hygiene.no_duplicate_purchases")

    # ---------------------------------------------------------------- separation and necessity
    declared_main = {Wr.F_RENDER, Wr.F_RANKINGS, Wr.F_ORDERS, D.F_ARCHIVE, D.F_CHARTER, D.F_COMMIT, D.F_REGISTER,
                     D.F_FIELDS}
    device_files = {Wr.F_PAYMENTS, K.offers_file(tgt), D.F_TARIFF, D.F_TERMS, D.F_MINUTES, K.F_WEEKLY, K.F_R2,
                    D.F_RELEASES, D.F_CAPACITY, D.F_ICS, D.F_FINANCE}
    K_(not (declared_main & device_files), "separation.files")
    main_cols = {"order_id", "buyer_id", "listing_id", "ordered_at", "channel", "home_session_id"}
    K_(not ({"asking_price_eur", "delivery"} & main_cols), "separation.columns")
    # scramble every device column the orders file carries: the call does not move
    M2 = A.load_main(tgt)
    M2.O["asking_price_eur"] = M2.O.asking_price_eur.sample(frac=1.0, random_state=1).to_numpy()
    M2.O["delivery"] = "shipped"
    yk2 = A.followup(M2, hours=21 * 24).astype(float)
    v2 = A.est(M2.S, yk2, "session_ipw")
    K_(abs(v2[E_] - e_k) < 1e-12 and abs(v2[B_] - b_k) < 1e-12, "necessity.devices_do_not_move_the_call")
    rec["device_rows_in_main_population"] = 0

    # ---------------------------------------------------------------- pair simulation
    rec["pair"] = pair_simulation(res, gold, small)
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
            blob[f] = "\n".join(x.text for x in Document(p).paragraphs)
        elif f.endswith(".xlsx") and f != D.F_ARCHIVE:
            blob[f] = "\n".join(pd.read_excel(p, sheet_name=None, header=None)[s].astype(str).to_csv() for s in
                                pd.ExcelFile(p).sheet_names)
    blob[D.F_ARCHIVE + ":tests+notes"] = T.to_csv() + pd.read_excel(os.path.join(tgt, D.F_ARCHIVE), sheet_name="notes",
                                                                       header=None).to_csv()
    alltext = "\n".join(blob.values())
    K_("distractor" not in alltext.lower() and not any("distractor" in f.lower() for f in files),
       "gates.distractors_unnamed_in_pack")
    bad = re.compile(r"\b(trap|decoy|golden|stump|rung|ladder|answer key|synthetic|generated by|placeholder|lorem|"
                     r"python-docx|openpyxl|reportlab|matplotlib|xlsxwriter|pyarrow|seed)\b", re.I)
    hits_ = {f: bad.findall(t) for f, t in blob.items() if bad.search(t)}
    K_(not hits_, "leak.author_vocabulary", hits_)
    K_("—" not in alltext, "leak.no_em_dash")
    # no shipped table carries a per-policy lift, guardrail or ranking
    for f, t in blob.items():
        ids = [r for r in P.POLICIES if r in t]
        if len(ids) >= 3:
            K_(f == D.F_REGISTER, f"no_ranking_artifact.{f}", ids)
    reg = json.load(open(os.path.join(tgt, D.F_REGISTER), encoding="utf-8"))
    K_(not re.search(r"\d+\.\d+ (extra )?orders|lift", json.dumps(reg).lower().replace("lift", "LIFTX"))
       or "liftx" not in json.dumps(reg).lower(), "register.no_lift")
    # single-statement invariant
    facts = {
        "lift_definition": r"change in orders placed by the arm's buyers during the test",
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
    }
    single = {}
    for k, pat in facts.items():
        where = [f for f, t in blob.items() if re.search(pat, re.sub(r"\s+", " ", t))]
        single[k] = where
        K_(len(where) == 1, f"single_statement.{k}", where)
    rec["single_statement"] = single
    # folder index lists every file but itself
    idx = blob[D.F_INDEX]
    listed = set(re.findall(r"^\| ([^|]+?) \|", idx, re.M)) - {"file", "---"}
    K_(listed == set(files) - {D.F_INDEX}, "H9.index_covers_every_file", sorted(set(files) ^ (listed | {D.F_INDEX})))
    # dates after the pack date only where the record is forward-looking by design
    allow = {D.F_TARIFF, D.F_ICS, D.F_CAPACITY, D.F_MINUTES}
    late = sorted(f for f, t in blob.items() if any(d > P.PACK_DATE.isoformat() for d in
                                                     re.findall(r"\b20\d\d-\d\d-\d\d\b", t)))
    K_(set(late) <= allow, "H16.forward_dates_allow_list", late)
    # container metadata
    K_(scrub_rc[1] == 0 and "clean" in scrub_rc[2], "H1.containers_clean", scrub_rc[2][-200:])
    # generation tells: no uniform row counts; headline totals off round boundaries
    rows = [len(M.R), len(S), len(M.O), len(pay), len(offf)]
    K_(len(set(rows)) == len(rows) and all(x % 1000 for x in rows[2:]), "tells.row_counts", rows)
    # personas: every named person in the pack is from the guard draw
    drawn = ["Saar Dries", "Tygo Knoers", "Livia Verhaar", "Fabian Stoffel", "Kayleigh Zeemans", "Amélie Middelkoop",
             "Esila Stichter", "Lindsey Mudden", "Rik Breugelensis", "Britt Tins", "Zoey Joosten", "Jasmijn Zijlemans",
             "Tycho Feenstra", "Yasmine Billung", "Ali Maas", "Stef Steenbakkers", "Evy Mathieu"]
    rec["personas"] = drawn
    named = set(re.findall(r"\b([A-Z][a-zé]+ (?:[A-Z][a-z]+))\b", alltext))
    K_(all(n in alltext for n in drawn[:6]), "personas.core_present")
    rec["assertions"] = len(K_.items)
    rec["assertion_names"] = [n for n, _, _ in K_.items]
    return rec


def pair_simulation(res, gold, small):
    """Two answer sheets with the habitual hygiene battery applied and no device handled beyond it:
    the response that lands the call, and the best one that stops at the velocity boost. Weights at
    the planning split (38 / 7 / 55 over 4 call, 4 file and 64 ask criteria)."""
    w_call, w_if, w_ask = 38 / 4, 7 / 4, 55 / 64
    # cracker: the call, the files, the heatmap's four parts; a grid cell only where the natural fee path
    # (formula on the asking price at the newest register row, every order priced) leaves it in its bin
    nat = res["fee_natural"]
    keep_c = sum(same_bin(res["fee_combos"][("wrong", "asking", "jan")][k], gold[k]) for k in gold)
    cracker = 4 * w_call + 4 * w_if + (4 + keep_c) * w_ask
    # mirror: stops at B on in-session orders; three points of the call block survive (the exclusions it
    # names), the files, two heatmap parts (scale and hatching); its natural fee path keeps no cell
    keep_m = sum(same_bin(nat[k], gold[k]) for k in gold)
    mirror = 3 + 4 * w_if + (2 + keep_m) * w_ask
    exposure = 4 * w_call + 4 * w_if + (4 + 48) * w_ask
    return dict(cracker=round(cracker, 1), mirror=round(mirror, 1), pair=round((cracker + mirror) / 2, 1),
                cracker_cells=int(keep_c), mirror_cells=int(keep_m),
                exposure_if_cracker_handles_every_fee_device=round((exposure + mirror) / 2, 1))
