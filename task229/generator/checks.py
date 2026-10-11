"""Assertions over the built pack: the ladder, the grid, the asks' stops, separation, gates, bins.

Run after build.py. Everything is computed from target/ through golden.py, plus the simulated world
where an assertion is about the world itself (separation, chronology, the network's events)."""
import collections
import datetime as dt
import itertools
import json
import math
import os
import shutil
import sys
import tempfile

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G
import world as W

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


GOLD_FIRE = ("EM3.10.9", "EM3.12.1", "PX5.2.7")


def random_intercept(y, groups):
    """One-way random-intercept model by the moment (ANOVA) estimator: the variance of the simple mean
    under the model, and the full fit's GLS mean and its standard error."""
    df = pd.DataFrame({"y": y, "g": groups})
    grp = df.groupby("g")["y"]
    m, mu = grp.size().to_numpy().astype(float), grp.mean().to_numpy()
    n, k, yb = len(df), len(m), float(df["y"].mean())
    msb = float((m * (mu - yb) ** 2).sum()) / (k - 1)
    msw = float(((df["y"] - grp.transform("mean")) ** 2).sum()) / (n - k)
    su2, se2 = max(0.0, (msb - msw) / ((n - float((m ** 2).sum()) / n) / (k - 1))), msw
    w = 1.0 / (su2 + se2 / m)
    return dict(rh=yb, se_simple=math.sqrt(su2 * float((m ** 2).sum()) + se2 * n) / n,
                gls=float((w * mu).sum() / w.sum()), se_gls=1.0 / math.sqrt(float(w.sum())))


def edge(x):
    """Distance from x to the nearest two-decimal rounding edge (the x.xx5 points)."""
    return abs((x * 100) % 1 - 0.5) / 100


def margin(v):
    return v["rh"] - v["lcl"]


def run(target, world=None, quiet=False):
    D, g = G.solve(target)
    sc = g["scorecard"]
    log = []

    # ---------------------------------------------------------------- the call
    ok(g["fire"] == GOLD_FIRE, "golden fire set moved: %s" % (g["fire"],))
    for r in G.RELEASES:
        v = sc[r]
        ok(abs(margin(v)) >= 0.05, "%s sits %.4f from its limit" % (r, margin(v)))
        ok(min(edge(v["rh"]), edge(v["se"]), edge(v["lcl"]), edge(margin(v))) >= 0.0015, "%s two-decimal edge" % r)
        ok(round(round(v["rh"], 2) - round(v["lcl"], 2), 2) == round(margin(v), 2), "%s distance reads the same from rounded figures" % r)
    margins = sorted(margin(sc[r]) for r in G.RELEASES)
    ok(min(b - a for a, b in zip(margins, margins[1:])) >= 0.04, "order by distance to the limit is not a near tie")

    # ---------------------------------------------------------------- the ladder
    vers = {w: G.versions(D["mdm"], w) for w in ("cutoff", "latest", "first")}
    pops = {m: G.assessed(D, m) for m in ("fullweek", "start", "end")}
    rung = collections.OrderedDict([
        ("R0 latest deliveries, every installation on its end-of-week build, pooled reads, read-count error",
         ("latest", "end", "pooled", "binomial_reads", "register")),
        ("R1 + reads held at the cut-off against every expected interval (a register-day held nowhere counts zero)",
         ("cutoff", "end", "pooled", "binomial_reads", "register")),
        ("R2 + installations that ran the build all week", ("cutoff", "fullweek", "pooled", "binomial_reads", "register")),
        ("R3 + the mean of installation read health", ("cutoff", "fullweek", "installation", "binomial_reads", "register")),
        ("R4 + a standard error with each installation its own unit (sample SD over root n)",
         ("cutoff", "fullweek", "installation", "installation", "register")),
        ("R5 + a standard error built over the comms parents the installations share (the answer)",
         ("cutoff", "fullweek", "installation", "collector", "register")),
    ])
    expect = [("EM3.10.9", "EM3.12.0", "EM3.12.2", "PX5.3.0", "PX5.3.1"),
              ("EM3.10.9", "EM3.12.0", "EM3.12.1", "EM3.12.2", "PX5.2.7", "PX5.3.0", "PX5.3.1"),
              ("EM3.10.9", "EM3.12.0", "EM3.12.1", "EM3.12.2", "PX5.2.7", "PX5.3.0"),
              ("EM3.10.9", "EM3.12.0", "EM3.12.1", "EM3.12.2", "PX5.2.7", "PX5.3.1"),
              ("EM3.10.9", "EM3.12.0", "EM3.12.1", "EM3.12.2", "PX5.2.7"),
              GOLD_FIRE]
    sets = []
    for (name, cell), want in zip(rung.items(), expect):
        fs = G.fire_set(G.score(vers[cell[0]], pops[cell[1]], cell[2], cell[3], cell[4], D=D))
        ok(fs == tuple(sorted(want)), "%s fires %s" % (name, fs))
        sets.append(fs)
        log.append("%s -> fires %s" % (name, ", ".join(fs)))
    ok(len(set(sets)) == len(sets), "every rung names a different set")
    right = [sum(1 for r in G.RELEASES if (r in fs) == (r in GOLD_FIRE)) for fs in sets]
    ok(max(right[:-1]) <= 6 and right[-1] == 8, "no rung below the answer lands the call: %s" % right)
    log.append("calls right per rung: %s" % right)

    # ---------------------------------------------------------------- the grid, cell by cell
    units = ("installation", "pooled", "row", "stream")
    errs = ("collector", "collector_cr0", "installation", "binomial_reads", "binomial_installations", "none")
    golden_cells = []
    cells = 0
    for v, p, u, e, dn in itertools.product(vers, pops, units, errs, ("register", "rows")):
        fs = G.fire_set(G.score(vers[v], pops[p], u, e, dn, D=D))
        cells += 1
        if fs == GOLD_FIRE:
            golden_cells.append((v, p, u, e, dn))
    ok(cells == 432, "grid size")
    want_cells = [("cutoff", "fullweek", "installation", "collector", "register"),
                  ("cutoff", "fullweek", "installation", "collector_cr0", "register")]
    extra = [c for c in golden_cells if c not in want_cells]
    ok(all(c in golden_cells for c in want_cells), "the standard's reading lands the call under either small-sample convention")
    ok(all(c[3] in ("collector", "collector_cr0") for c in golden_cells),
       "every cell that lands the call builds its error over the comms parents: %s" % golden_cells)
    for c in extra:
        sc_x = G.score(vers[c[0]], pops[c[1]], c[2], c[3], c[4], D=D)
        moved = [r for r in G.RELEASES if round(sc_x[r]["rh"], 2) != round(sc[r]["rh"], 2)
                 or round(sc_x[r]["lcl"], 2) != round(sc[r]["lcl"], 2)]
        ok(len(moved) >= 4, "a cell %s that lands the call moves at least four builds' graded figures (%d)" % (c, len(moved)))
    log.append("grid: %d cells; %d land the call, every one on the comms-parent error: %s" % (cells, len(golden_cells), golden_cells))

    # convergence: the call does not depend on the small-sample convention or the estimator family
    fw = (vers["cutoff"], pops["fullweek"], "installation")
    for e in ("collector_cr0", "collector_jack"):
        ok(G.fire_set(G.score(*fw, e, "register", D=D)) == GOLD_FIRE, "%s: same call" % e)
    jack = G.score(*fw, "collector_jack", "register", D=D)
    log.append("jackknife over comms parents: same call; standard errors %s" % {r: round(jack[r]["se"], 3) for r in G.RELEASES})
    # the judge's residual (pass 1): the simple mean with a random-intercept variance holds EM3.10.9, whose
    # node spread is one failed collector the model charges to every node by size squared; the full
    # random-intercept fit, which applies the same model to the mean, fires it with the golden call
    U = G._units(D, vers["cutoff"], pops["fullweek"], "register", "installation")
    ri = {r: random_intercept(U.loc[U["release"] == r, "y"].to_numpy(), U.loc[U["release"] == r, "parent"].to_numpy())
          for r in G.RELEASES}
    gls_fire = tuple(sorted(r for r in G.RELEASES if ri[r]["gls"] < G.REFERENCE - G.K * ri[r]["se_gls"]))
    hyb_fire = tuple(sorted(r for r in G.RELEASES if ri[r]["rh"] < G.REFERENCE - G.K * ri[r]["se_simple"]))
    ok(gls_fire == GOLD_FIRE, "the full random-intercept fit lands the call: %s" % (gls_fire,))
    ok(hyb_fire == ("EM3.12.1", "PX5.2.7"), "the simple mean with a random-intercept variance holds EM3.10.9 only: %s" % (hyb_fire,))
    big = U[U["release"] == "EM3.10.9"].groupby("parent")["y"].agg(["size", "mean"]).sort_values("size").tail(10)
    log.append("random intercept (moment estimator): full fit fires %s (EM3.10.9 %.2f, SE %.2f); simple mean with the model's "
               "variance fires %s (EM3.10.9 SE %.2f, needs %.2f to hold); EM3.10.9's ten largest nodes (%d to %d "
               "installations) average %.2f to %.2f"
               % (gls_fire, ri["EM3.10.9"]["gls"], ri["EM3.10.9"]["se_gls"], hyb_fire, ri["EM3.10.9"]["se_simple"],
                  (G.REFERENCE - ri["EM3.10.9"]["rh"]) / G.K, big["size"].min(), big["size"].max(), big["mean"].min(),
                  big["mean"].max()))
    # the error built over installations (either divisor) fires EM3.12.0 and EM3.12.2 with margin
    inst = G.score(*fw, "installation", "register", D=D)
    inst0 = G.score(*fw, "installation_ddof0", "register", D=D)
    for r, lim in (("EM3.12.2", -0.2), ("EM3.12.0", -0.5)):
        ok(margin(inst[r]) <= lim and margin(inst0[r]) <= lim, "%s fires on an installation-level error (%.3f)" % (r, margin(inst[r])))
    ok(margin(sc["EM3.12.2"]) >= 2.0 and margin(sc["EM3.12.0"]) >= 0.3, "EM3.12.2 and EM3.12.0 hold on the comms-parent error")
    for r in GOLD_FIRE:
        ok(margin(inst[r]) <= -0.15, "%s fires on either error" % r)
    log.append("deciding contrasts: EM3.12.2 %.2f against %.2f (installations as units) or %.2f (comms parents, k=%d); "
               "EM3.12.0 %.2f against %.2f or %.2f (k=%d)"
               % (sc["EM3.12.2"]["rh"], inst["EM3.12.2"]["lcl"], sc["EM3.12.2"]["lcl"], sc["EM3.12.2"]["k"],
                  sc["EM3.12.0"]["rh"], inst["EM3.12.0"]["lcl"], sc["EM3.12.0"]["lcl"], sc["EM3.12.0"]["k"]))

    # the data's own structure: a node-night either loses the day for most of the installations behind
    # it or for very few of them, nothing between (the hole that makes the node the unit)
    x = G.panel(D, vers["cutoff"], pops["end"])
    x["parent"] = x["NMI"].map(D["nmi_parent"])
    day = x.groupby(["NMI", "READ_DATE"]).agg(A=("QTY_A", "sum"), parent=("parent", "first"))
    day["lost"] = day["A"] == 0
    frac = day.groupby(["parent", "READ_DATE"])["lost"].mean()
    lo, hi = frac[frac < 0.5], frac[frac >= 0.5]
    ok(float(lo.max()) <= 0.12, "outside a node failure, a node-night loses the day for at most 12 per cent of its installations (%.3f)" % lo.max())
    ok(float(hi.min()) >= 0.6 and len(hi) == 4, "four node-nights lose the day for 60 per cent or more of their installations: %s" % hi.round(3).to_dict())
    log.append("node-nights losing the day for most installations: %s; every other node-night at most %.1f per cent"
               % ({k: round(v_, 3) for k, v_ in hi.items()}, 100 * lo.max()))
    ok(set(pops["fullweek"]) <= set(D["nmi_parent"]), "every assessed installation has a comms parent")

    # independence of installations, which the installation-level error assumes, is refuted by the files:
    # at the rate installations lose a whole day on every other node-night, each failed node-night
    # has a binomial tail below 1e-10
    import math as _m
    from scipy import stats as _st
    cnt = day.groupby(["parent", "READ_DATE"])["lost"].agg(["sum", "size"])
    base = cnt[frac < 0.5]
    p0 = float(base["sum"].sum() / base["size"].sum())
    tails = {k: _st.binom.logsf(int(r_["sum"]) - 1, int(r_["size"]), p0) / _m.log(10) for k, r_ in cnt[frac >= 0.5].iterrows()}
    ok(all(t <= -10 for t in tails.values()), "every failed node-night is impossible under independent installations: %s" % tails)
    log.append("independence test: whole-day loss rate %.4f outside node failures; log10 tail per failed node-night %s"
               % (p0, {k: round(t, 1) for k, t in tails.items()}))

    # every grouping that respects the shared failures lands the call: nodes, node-days, days, and the
    # two-way node and day error, on the installation-day panel (each installation-day an equal share)
    xf = G.panel(D, vers["cutoff"], pops["fullweek"])
    xf["parent"] = xf["NMI"].map(D["nmi_parent"])
    idy = xf.groupby(["NMI", "READ_DATE"]).agg(A=("QTY_A", "sum"), E=("expected", "sum"), parent=("parent", "first"),
                                              release=("release", "first")).reset_index()
    idy["s"] = 100.0 * idy["A"] / idy["E"]

    def se_by(y, g_):
        d_ = pd.Series(y - y.mean()).groupby(pd.Series(g_).values).sum().to_numpy()
        k_ = len(d_)
        return _m.sqrt(k_ / (k_ - 1) * float((d_ ** 2).sum())) / len(y)
    alt = {}
    for rel, g_ in idy.groupby("release"):
        y = g_["s"].to_numpy()
        se_n, se_nd, se_d = se_by(y, g_["parent"]), se_by(y, g_["parent"] + "|" + g_["READ_DATE"]), se_by(y, g_["READ_DATE"])
        two = _m.sqrt(max(se_n ** 2 + se_d ** 2 - se_nd ** 2, se_n ** 2))
        alt[rel] = {k_: bool(y.mean() < 99.5 - 3 * v_) for k_, v_ in (("node", se_n), ("node-day", se_nd), ("day", se_d), ("two-way", two))}
    for k_ in ("node", "node-day", "day", "two-way"):
        fs_ = tuple(sorted(r for r in G.RELEASES if alt[r][k_]))
        ok(fs_ == GOLD_FIRE, "the %s grouping lands the call: %s" % (k_, fs_))
    log.append("node, node-day, day and two-way groupings of the installation-day panel all fire %s" % ", ".join(GOLD_FIRE))

    # the outage carve-out a solver might improvise (no clause allows it: 3.3 counts every interval)
    # files a wrong set on every variant, with EM3.12.0 firing clearly, so it reaches no knife edge
    failed = set(frac[frac >= 0.5].index)
    nodes_f = {p_ for p_, _ in failed}
    xl = G.panel(D, vers["latest"], pops["fullweek"])
    dl = xl.groupby(["NMI", "READ_DATE"])["QTY_A"].sum()
    idy["AL"] = [dl.get((n_, d_), 0) for n_, d_ in zip(idy["NMI"], idy["READ_DATE"])]
    idy["nf"] = [(p_, d_) in failed for p_, d_ in zip(idy["parent"], idy["READ_DATE"])]
    variants = {"failed node-days dropped": idy[~idy["nf"]],
                "node backlog counted as held": idy.assign(A=idy["A"].where(~idy["nf"], idy["AL"])),
                "installations behind failed nodes dropped": idy[~idy["parent"].isin(nodes_f)]}
    for nm, dv in variants.items():
        iv = dv.groupby("NMI").agg(A=("A", "sum"), E=("E", "sum"), release=("release", "first"))
        iv["s"] = 100.0 * iv["A"] / iv["E"]
        mm = {rel: g_["s"].mean() - (99.5 - 3 * g_["s"].std(ddof=1) / _m.sqrt(len(g_))) for rel, g_ in iv.groupby("release")}
        fs_ = tuple(sorted(r for r, v_ in mm.items() if v_ < 0))
        ok(fs_ != GOLD_FIRE and mm["EM3.12.0"] <= -0.1, "carve-out (%s) files %s, EM3.12.0 at %.3f" % (nm, fs_, mm["EM3.12.0"]))
        log.append("carve-out, %s, installation-level error: fires %s (EM3.12.0 %.3f)" % (nm, ", ".join(fs_), mm["EM3.12.0"]))
    if world is not None:
        moved_parent = [i for i in world["insts"] if i.group == "full" and i.since.date() >= dt.date(2026, 10, 5)]
        ok(not moved_parent, "no assessed installation changed comms parent during the week")

    # the cut-off rung: register-days held nowhere at the cut-off, and the partial application
    naive_rows = G.score(vers["cutoff"], pops["fullweek"], "installation", "collector", "rows", D=D)
    ok(not naive_rows["PX5.2.7"]["fire"], "dividing by the register-days held at the cut-off holds PX5.2.7")
    part = G.fire_set(G.score(vers["cutoff"], pops["end"], "pooled", "binomial_reads", "rows", D=D))
    ok(part != GOLD_FIRE and "PX5.2.7" not in part, "the cut-off filter applied to rows alone holds PX5.2.7: %s" % (part,))
    ok(naive_rows["EM3.12.2"]["rh"] >= 99.5 and G.fire_set(naive_rows) != GOLD_FIRE,
       "dividing by held rows drops the node failures' days altogether (EM3.12.2 %.2f)" % naive_rows["EM3.12.2"]["rh"])
    log.append("cut-off on rows alone fires %s; on held rows the node failures vanish (EM3.12.2 %.2f, EM3.12.0 %.2f)"
               % (", ".join(part), naive_rows["EM3.12.2"]["rh"], naive_rows["EM3.12.0"]["rh"]))
    held_days = set(map(tuple, vers["cutoff"][["NMI", "NMI_SUFFIX", "READ_DATE"]].values.tolist()))
    pxn = [n for n, b in pops["fullweek"].items() if b == "PX5.2.7"]
    st = D["streams"][D["streams"]["NMI"].isin(pxn)]
    absent = sum(1 for _, r_ in st.iterrows() for d_ in G.DATES if (r_["NMI"], r_["NMI_SUFFIX"], d_) not in held_days)
    ok(absent >= 60, "PX5.2.7 has register-days the MDM held nothing for at the cut-off (%d)" % absent)
    log.append("PX5.2.7: %d register-days held nowhere at the cut-off; dividing by held rows gives %.2f against %.2f, the register gives %.2f"
               % (absent, naive_rows["PX5.2.7"]["rh"], naive_rows["PX5.2.7"]["lcl"], sc["PX5.2.7"]["rh"]))
    late = G.score(vers["latest"], pops["fullweek"], D=D)
    ok(not late["PX5.2.7"]["fire"], "PX5.2.7 holds on the latest deliveries")
    first = G.score(vers["first"], pops["fullweek"], D=D)
    moved = [r for r in G.RELEASES if round(first[r]["rh"], 2) != round(sc[r]["rh"], 2)]
    ok(len(moved) >= 4, "the first-delivery reading moves at least four graded read-health figures: %s" % moved)
    pooled = G.score(vers["cutoff"], pops["fullweek"], "pooled", "collector", D=D)
    ok(pooled["PX5.3.0"]["fire"] and not pooled["EM3.12.1"]["fire"], "pooled reads fire PX5.3.0 and hold EM3.12.1")
    log.append("pooled reads: PX5.3.0 %.2f, EM3.12.1 %.2f against the mean's %.2f and %.2f"
               % (pooled["PX5.3.0"]["rh"], pooled["EM3.12.1"]["rh"], sc["PX5.3.0"]["rh"], sc["EM3.12.1"]["rh"]))

    # convergent readings (C1): same population and same figures
    sp_fail = G.running_builds(D["hes"], D["img2rel"], failed_moves=True)
    sp_raw = G.running_builds(D["hes"], D["img2rel"], dedupe=False)
    ok(G.assessed(D, "fullweek", sp_fail) == pops["fullweek"], "a failed activation read as a move changes no assessed installation")
    ok(G.assessed(D, "fullweek", sp_raw) == pops["fullweek"], "replayed events change no assessed installation")
    xx = G.panel(D, vers["cutoff"], pops["fullweek"])
    dd = xx.groupby(["NMI", "READ_DATE"])[["QTY_A", "expected"]].sum()
    day_mean = (100 * dd["QTY_A"] / dd["expected"]).groupby(level=0).mean()
    wk = xx.groupby("NMI")[["QTY_A", "expected"]].sum()
    wk_share = 100 * wk["QTY_A"] / wk["expected"]
    ok(float((day_mean - wk_share).abs().max()) < 1e-9, "installation-day mean equals the installation's week share")
    gap = (D["mdm"]["cutoff"] - D["mdm"]["received"]).dt.total_seconds().abs() / 60
    ok(float(gap.min()) >= 8.0, "no delivery lands within 8 minutes of its cut-off")
    ok(bool(((D["mdm"]["expected"] * D["mdm"]["INTERVAL_LENGTH"]) == 1440).all()), "every delivered register-day carries a full day of intervals")

    # clean-data and lens-swap tests: repair the Layer 1 mess on the main path; the answer and the
    # installation-level answer do not move, and they differ
    ok(G.fire_set(G.score(vers["cutoff"], G.assessed(D, "fullweek", sp_raw), "installation", "collector", D=D)) == GOLD_FIRE,
       "clean data: replays removed, same call")
    ok(G.fire_set(G.score(vers["cutoff"], pops["fullweek"], "installation", "installation", "rows", D=D)) != GOLD_FIRE,
       "clean data: the installation-level error is still wrong on held rows")
    ok(len(pops["end"]) - len(pops["fullweek"]) >= 1100, "the naive population is not the assessed population")

    # ---------------------------------------------------------------- ask A: Wave 8 moves under the call
    a = g["wave8"]
    ok(a == {"EM3.12.2": 1274, "PX5.3.1": 109}, "wave 8 moves %s" % a)
    ok(G.wave8_moves(D, sets[4]) == {"EM3.12.2": 0, "PX5.3.1": 109}, "the installation-level call stops Wave 8 onto EM3.12.2")
    wb = __import__("openpyxl").load_workbook(os.path.join(target, "wave8_schedule.xlsx"), read_only=True)
    raw = []
    for name in ("Batch A 13-10", "Batch B 14-10"):
        for r_ in list(wb[name].iter_rows(values_only=True))[2:]:
            raw.append(dict(serial=str(r_[1]), nmi=r_[2], target=r_[5]))
    raw = pd.DataFrame(raw)
    rows_ct = raw.groupby("target").size().to_dict()
    ok(rows_ct != a, "schedule row count is not the answer")
    pad = raw.assign(serial=raw["serial"].str.zfill(8)).drop_duplicates()
    ok(pad.groupby("target").size().to_dict() != a, "distinct scheduled meters is not the answer")
    by_nmi = raw.fillna("").drop_duplicates(["nmi", "target"]).groupby("target").size().to_dict()
    ok(by_nmi != a, "collapsing on the NMI column (blanks included) is not the answer")
    log.append("wave 8: rows %s, distinct meters %s, one-per-NMI-cell %s, answer %s" % (rows_ct, pad.groupby("target").size().to_dict(), by_nmi, a))

    # ---------------------------------------------------------------- ask B: the substitution load
    load = g["load"]
    run_now = G.running_now(D)
    ok(load == sum(run_now[r] for r in GOLD_FIRE), "the load is every installation running a build that fires")
    week_end = G.running_now(D, dt.datetime(2026, 10, 11, 14, 0, tzinfo=dt.timezone.utc))
    ok(week_end == run_now, "the build each installation runs is the same at the week's end and at the extract")
    load_r4 = G.substitution_load(D, sets[4])
    ok(load_r4 != load and load_r4 - load >= 3000, "the installation-level call loads %d installations, not %d" % (load_r4, load))
    log.append("substitution load: %d installations on the builds that fire; the installation-level call would load %d" % (load, load_r4))

    # ---------------------------------------------------------------- chronology (H16)
    if world is not None:
        import records as R
        inv = {v: k for k, v in R.ALL_IMAGES.items()}
        early = sum(1 for es in world["ev"].values() for e in es
                    if e["image"] and e["type"] in ("COMMISSIONED", "FW_ACTIVATED")
                    and e["at"].date() < dt.date.fromisoformat(R.RELEASED[inv[e["image"]]]))
        ok(early == 0, "no meter runs an image before its release date (%d)" % early)
        late_ev = sum(1 for es in world["ev"].values() for e in es if e["at"] > W.EXTRACT_AT)
        ok(late_ev == 0, "no event after the extract")
        ok(all(i.since >= i.meters[0][3] for i in world["insts"]), "no meter joins a node before it was installed")

    # ---------------------------------------------------------------- separation
    if world is not None:
        dev = {i.nmi for i in world["insts"] if i.group in ("w7", "exch")}
        ok(not (dev & set(pops["fullweek"].keys())), "no mover or exchanged installation sits in the main population")
        sched_full = {row["inst"].nmi for row in world["sched"] if row["inst"].group == "full"}
        ok(len(sched_full) > 1000, "schedule rows for full-week installations are separate records, not main-path rows")

    # ---------------------------------------------------------------- gates
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten files")
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "three formats: %s" % fmts)
    ok(len(D["mdm"]) >= 25000, "a file of 25,000 rows")
    meta_p = os.path.join(os.path.dirname(target), "metadata.json")
    meta = json.load(open(meta_p)) if os.path.exists(meta_p) else None
    if meta:
        ok(len(meta["distractor_files"]) >= 2, "two distractors")
        tmp = tempfile.mkdtemp()
        for f in files:
            if f not in meta["distractor_files"]:
                shutil.copy(os.path.join(target, f), tmp)
        _, g2 = G.solve(tmp)
        shutil.rmtree(tmp)
        ok(g2["fire"] == g["fire"] and g2["wave8"] == g["wave8"] and g2["load"] == g["load"], "the golden ignores the distractors")
    # single statement: the reference and the cut-off hour are stated only in the standard
    txt = {f: open(os.path.join(target, f), errors="ignore").read() for f in files if f.endswith((".md", ".csv")) and "mdm_" not in f}
    for needle in ("99.50", "06:00"):
        hits = [f for f, t in txt.items() if needle in t]
        ok(not hits, "%s stated outside the standard: %s" % (needle, hits))
    for f in files:
        ok("distract" not in f.lower(), "no file named for its role")
    # the write-up carries the golden's figures, to the golden's rounding (H2, H3)
    sub = os.path.join(os.path.dirname(target), "submission.md")
    gj = os.path.join(os.path.dirname(target), "golden", "wave8_read_health_alerts.json")
    if os.path.exists(sub) and os.path.exists(gj):
        s_ = open(sub).read()
        pj = json.load(open(gj))
        for b_ in pj["builds"]:
            line = "%s: %.2f%%, standard error %.2f, lower limit %.2f%%, %.2f %s the limit, %s" % (
                b_["release"], b_["read_health_pct"], b_["standard_error_pct"], b_["lower_limit_pct"], abs(b_["vs_limit_pct"]),
                "below" if b_["vs_limit_pct"] < 0 else "above", b_["alert"].lower())
            ok(line in s_, "submission carries %s" % line)
        for v_ in list(pj["wave8_moves_under_this_call"].values()) + [pj["settlement_substitution_load_installations"]]:
            ok(format(v_, ",") in s_, "submission carries %s" % v_)
        ok("\u2014" not in s_, "no em dash in the write-up")
    if not quiet:
        print("checks: %d assertions passed" % N[0])
        for line in log:
            print("  " + line)
    return N[0], log


if __name__ == "__main__":
    run(os.path.join(os.path.dirname(HERE), "target"))
