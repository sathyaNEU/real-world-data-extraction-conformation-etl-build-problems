"""Assemble the clean truth: the network, the fleet to 30 September 2026, three simulated summers, the boundary
fix-ups that keep every event clear of each transformer's 2026 peak, the forward fleet to the record date placed clear
of the line, and the steered district counts.

    python3 truth.py            builds and caches the truth (generator/.truth.pkl, never shipped or committed)"""
from __future__ import annotations

import datetime as dt
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402
import forward as FW    # noqa: E402
import world as W       # noqa: E402

CACHE = os.path.join(HERE, ".truth.pkl")
REC = pd.Timestamp(K.RECORD_DATE)
END26 = pd.Timestamp("2026-09-30")


class Truth:
    pass


def post_peak_changes(tx, veh, sw, pr_base):
    """State at the record date from the history alone (no forward events yet)."""
    return FW.states_at(tx, veh, sw, pr_base, REC)


def boundary_and_holes(tx, veh, sw, pr_base, log):
    """One pass: events on a transformer's 2026 peak date are moved off it; late-summer events that leave the
    transformer inside the hole are moved. Returns the districts to re-simulate."""
    redo = set()
    pkd = dict(zip(tx["ti"], W.peak_date(tx, 2026)))
    # registrations and departures on the peak date itself
    for i, v in veh.iterrows():
        p = pkd[v.ti]
        if v.reg == p:
            veh.at[i, "reg"] = v.reg - pd.Timedelta(days=1); redo.add(v.di); log["reg_on_peak"] += 1
        if not pd.isna(v.dep) and v.dep == p:
            veh.at[i, "dep"] = v.dep + pd.Timedelta(days=1); redo.add(v.di); log["dep_on_peak"] += 1
    for pi, s in list(sw.items()):
        ti = int(PI2TI[pi])
        if s == pkd[ti]:
            sw[pi] = s - pd.Timedelta(days=1); redo.add(int(TI2DI[ti])); log["sw_on_peak"] += 1
    if redo:
        return redo
    fam, _ = FW.family(tx)
    k1, e1 = post_peak_changes(tx, veh, sw, pr_base)
    chg = np.where((k1 != tx["k2026"].values) | (e1 != tx["e2026"].values))[0]
    rows = tx.set_index("ti")
    for j in chg:
        ti = int(tx["ti"].iloc[j])
        row = rows.loc[ti]
        if FW.clear(FW.margins(fam, row, k1[j], e1[j])):
            continue
        di = int(row["di"])
        p = pkd[ti]
        # the offending events: late registrants, post-peak departures, post-peak switches
        late = veh[(veh.ti == ti) & (veh.reg > p) & (veh.dep.isna() | (veh.dep > REC))]
        gone = veh[(veh.ti == ti) & (veh.reg <= p) & veh.dep.notna() & (veh.dep > p)]
        sws = [pi for pi in PREMS_OF[ti] if pi in sw and sw[pi] > p and
               ((veh.pi == pi) & (veh.reg <= p) & (veh.dep.isna() | (veh.dep > p))).any()]
        if len(late):
            i = late.index[0]
            oldpi0 = int(veh.at[i, "pi"])
            alone = int((veh.pi == oldpi0).sum()) == 1
            own_switch = sw.get(oldpi0) if alone else None
            cand = veh_candidates(tx, di, veh.at[i, "reg"], pkd)
            r = K.rng("move", ti, log["moved"])
            for _ in range(300):
                t2 = int(cand[r.integers(len(cand))])
                # a premise on t2 with no vehicle and no rate history of its own takes the vehicle, with the
                # vehicle's own enrollment (if any) moving with it
                free = [p for p in PREMS_OF[t2] if p not in sw and p not in VEH_PREM]
                if not free:
                    continue
                newpi = int(free[0])
                rate = K.RATE_EV if (own_switch is not None and own_switch <= REC) else pr_base[newpi]
                if pr_base[newpi] == K.RATE_FLAT:
                    rate = K.RATE_FLAT
                a, b = k1[TI_POS[t2]], e1[TI_POS[t2]]
                a2, b2 = (a + 1, b) if rate != K.RATE_EV else (a, b + 1)
                if FW.clear(FW.margins(fam, rows.loc[t2], a2, b2)):
                    veh.at[i, "ti"], veh.at[i, "pi"] = t2, newpi
                    VEH_PREM.add(newpi)
                    if alone:
                        VEH_PREM.discard(oldpi0)
                    if own_switch is not None:
                        sw[newpi] = sw.pop(oldpi0)
                    log["moved"] += 1
                    break
            redo.add(di)
        elif len(gone):
            veh.at[gone.index[0], "dep"] = pd.NaT
            log["dep_cancelled"] += 1
            redo.add(di)
        elif sws:
            sw[sws[0]] = p - pd.Timedelta(days=2)
            log["sw_moved"] += 1
            redo.add(di)
    return redo


def veh_candidates(tx, di, reg, pkd):
    sub = tx[(tx.di == di)]
    ok = [t for t in sub["ti"].values if pkd[t] < reg]
    return np.array(ok)


def place_forward(T, fam, log):
    """Forward registrations, departures and drive switches, each clear of the line under every estimator."""
    tx, veh, sw, pr_base = T.tx, T.veh, T.sw, T.pr_base
    rows = tx.set_index("ti")
    k1, e1 = post_peak_changes(tx, veh, sw, pr_base)
    k1 = dict(zip(tx["ti"], k1)); e1 = dict(zip(tx["ti"], e1))
    global AT_REC
    pres = veh[(veh.reg <= REC) & (veh.dep.isna() | (veh.dep > REC))]
    AT_REC = pres.groupby("pi").size().to_dict()
    new = []
    span = (REC - pd.Timestamp("2026-10-01")).days + 1
    for di, d in enumerate(K.DISTRICTS):
        r = K.rng("forward", di)
        sub = T.pr[T.pr.di == di]
        pis, tis = sub["pi"].values, sub["ti"].values
        cnt = np.array([k1[t] + e1[t] for t in tis], dtype=float)
        n = int(d[9] * len(sub))
        days = np.sort(r.integers(0, span, n))
        for dd in days:
            reg = pd.Timestamp("2026-10-01") + pd.Timedelta(days=int(dd))
            for attempt in range(120):
                w = 1.0 + d[10] * cnt
                j = r.choice(len(sub), p=w / w.sum())
                pi, ti = int(pis[j]), int(tis[j])
                cur = W.rate_on(pr_base, sw, pi, REC)
                will_switch = (cur != K.RATE_EV and pr_base[pi] != K.RATE_FLAT and pi not in sw and r.random() < d[8])
                rate = K.RATE_EV if (cur == K.RATE_EV or will_switch) else cur
                # a premise that moves to the EV rate moves its other vehicles with it
                others = AT_REC.get(pi, 0)
                if rate == K.RATE_EV:
                    a, b = k1[ti] - (others if will_switch else 0), e1[ti] + 1 + (others if will_switch else 0)
                else:
                    a, b = k1[ti] + 1, e1[ti]
                if a >= 0 and FW.clear(FW.margins(fam, rows.loc[ti], a, b)):
                    break
                log["fwd_reg_redrawn"] += 1
            k1[ti], e1[ti] = a, b
            cnt[j] += 1
            AT_REC[pi] = AT_REC.get(pi, 0) + 1
            swd = None
            if will_switch:
                # enrolled up to three weeks before delivery, never before the summer's close
                swd = min(max(reg + pd.Timedelta(days=int(r.integers(-20, 11))), pd.Timestamp("2026-10-01")),
                          REC - pd.Timedelta(days=2))
                sw[pi] = swd
            new.append((pi, ti, di, reg, swd))
    fv = pd.DataFrame([(a, b, c, d_) for a, b, c, d_, _ in new], columns=["pi", "ti", "di", "reg"])
    fv["dep"] = pd.NaT
    fv["phase"] = "fwd"
    fv = W.attributes(fv, "fwd")
    veh = pd.concat([veh, fv], ignore_index=True)
    # departures between 1 October and the record date
    for di, d in enumerate(K.DISTRICTS):
        r = K.rng("forward-dep", di)
        pv = veh[(veh.di == di) & (veh.reg <= pd.Timestamp("2026-10-01")) & veh.dep.isna()]
        target = int(d[13] * 0.5 * len(pv))
        done = 0
        for i in r.permutation(pv.index.values):
            if done >= target:
                break
            v = veh.loc[i]
            ti = int(v.ti)
            rate = W.rate_on(pr_base, sw, int(v.pi), REC)
            a, b = (k1[ti] - 1, e1[ti]) if rate != K.RATE_EV else (k1[ti], e1[ti] - 1)
            if min(a, b) < 0 or not FW.clear(FW.margins(fam, rows.loc[ti], a, b)):
                log["fwd_dep_skipped"] += 1
                continue
            k1[ti], e1[ti] = a, b
            veh.at[i, "dep"] = pd.Timestamp("2026-10-01") + pd.Timedelta(days=int(r.integers(1, span - 1)))
            done += 1
    # the winter enrollment drive: default-rate premises with vehicles move to the EV rate
    drive = 0
    T.drive_pi = {}
    for di, d in enumerate(K.DISTRICTS):
        if d[12] <= 0:
            continue
        r = K.rng("drive", di)
        pv = veh[(veh.di == di) & (veh.reg <= pd.Timestamp("2026-11-01")) & (veh.dep.isna() | (veh.dep > REC))]
        at_rec = veh[(veh.di == di) & (veh.reg <= REC) & (veh.dep.isna() | (veh.dep > REC))].groupby("pi").size()
        prem = [p for p in pv["pi"].unique() if W.rate_on(pr_base, sw, int(p), REC) in (K.RATE_TOU, K.RATE_CARE)]
        target = int(d[12] * len(prem))
        done = 0
        for p in r.permutation(np.array(prem)):
            if done >= target:
                break
            ti = int(PI2TI[p])
            nv = int(at_rec.get(p, 0))
            a, b = k1[ti] - nv, e1[ti] + nv
            if a < 0 or not FW.clear(FW.margins(fam, rows.loc[ti], a, b)):
                log["drive_skipped"] += 1
                continue
            k1[ti], e1[ti] = a, b
            sw[int(p)] = pd.Timestamp(K.DRIVE_START) + pd.Timedelta(days=int(r.integers(0, (K.DRIVE_END - K.DRIVE_START).days + 1)))
            T.drive_pi[int(p)] = True
            drive += 1
    log["drive_switches"] = drive
    T.veh = veh
    return T


def golden_counts(T, fam, tab_name=FW.GOLD):
    tx = T.tx
    k1, e1 = FW.states_at(tx, T.veh, T.sw, T.pr_base, REC)
    tab = fam[tab_name]
    f = np.array([FW.forecast(tab, s, a, b, c, d, p) for s, a, b, c, d, p in
                  zip(tx["sg"], tx["k2026"], tx["e2026"], k1, e1, tx["pk2026"])])
    at = f > K.THRESH * tx["kva"].values
    return pd.Series(at).groupby(tx["district"].values).sum().reindex(K.NAMES).astype(int), f, k1, e1


def cut_gap(counts):
    """The gap around the largest-remainder cut, and the worst quota's distance from a half (plain rounding)."""
    alloc, q = FW.allocate(counts)
    rem = q - np.floor(q)
    seat = (alloc - np.floor(q)).astype(int) == 1
    lo = rem[seat].min() if seat.any() else 1.0
    hi = rem[~seat].max() if (~seat).any() else 0.0
    half = float((rem - 0.5).abs().min())
    return min(lo - hi, 2 * half), alloc, q


def move_one(T, fam, rows, kk, ee, di, sign, r, log):
    """Move one forward default-rate registration in district di so the district's count rises (sign +1) or falls
    (sign -1) by one, every transformer touched staying clear of the line."""
    tx = T.tx
    fv = T.veh[(T.veh.phase == "fwd") & (T.veh.di == di)]
    for i in r.permutation(fv.index.values):
        v = T.veh.loc[i]
        if W.rate_on(T.pr_base, T.sw, int(v.pi), REC) == K.RATE_EV:
            continue
        if int((T.veh.pi == v.pi).sum()) > 1:
            continue
        ti = int(v.ti)
        m_now = FW.margins(fam, rows.loc[ti], kk[ti], ee[ti])
        crossing = bool(np.all(m_now > 0))
        m_wo = FW.margins(fam, rows.loc[ti], kk[ti] - 1, ee[ti])
        if not FW.clear(m_wo):
            continue
        if sign > 0 and crossing:
            continue
        if sign < 0 and not (crossing and np.all(m_wo < -FW.DELTA)):
            continue
        sub = tx[(tx.di == di) & (tx.ti != ti)]
        for t2 in r.permutation(sub["ti"].values)[:3000]:
            prem = [p for p in PREMS_OF[t2] if p not in VEH_PREM and p not in T.sw and T.pr_base[p] != K.RATE_FLAT]
            if not prem:
                continue
            m2 = FW.margins(fam, rows.loc[t2], kk[t2] + 1, ee[t2])
            if not FW.clear(m2):
                continue
            m2b = FW.margins(fam, rows.loc[t2], kk[t2], ee[t2])
            if sign > 0 and not (np.all(m2 > 0) and np.all(m2b < 0)):
                continue
            if sign < 0 and not np.all(m2 < 0):
                continue
            VEH_PREM.discard(int(v.pi))
            T.veh.at[i, "ti"], T.veh.at[i, "pi"] = int(t2), int(prem[0])
            VEH_PREM.add(int(prem[0]))
            log["steer_moves"] += 1
            return True
    return False


def margin_score(counts):
    """The smaller of the half-gap around the largest-remainder cut and the worst share's distance from a half."""
    gap, alloc, q = cut_gap(pd.Series(counts))
    return gap / 2.0


def plan_counts(counts, banned=(), need=0.26, span=9, nspan=45):
    """The smallest change to the district counts (in transformers moved) that puts every district's quota at least
    a quarter clear of a half, so the largest-remainder cut has a clear gap and plain rounding agrees with it: for each
    candidate total, every district's admissible counts near its own, then the cheapest combination summing to the
    total (a knapsack over the districts), never in a direction found infeasible for a district."""
    c0 = counts.astype(int).copy()
    if margin_score(c0) >= need and len(set(int(x) for x in c0.values)) == len(c0):
        return c0
    names = list(c0.index)
    N0 = int(c0.sum())
    sols = []
    for N1 in range(N0 - nspan, N0 + nspan + 1):
        opts = []
        for d in names:
            o = []
            for s in range(-span, span + 1):
                if s != 0 and (d, int(np.sign(s))) in banned:
                    continue
                c = int(c0[d]) + s
                if c < 0:
                    continue
                q = K.TOTAL * c / N1
                if abs(q - np.floor(q) - 0.5) >= need:
                    o.append((s, abs(s)))
            opts.append(o)
        if any(not o for o in opts):
            continue
        # knapsack on the running change in the total, keeping the eight cheapest paths to each running total
        target = N1 - N0
        dp = {0: [(0, [])]}
        for o in opts:
            nd = {}
            for acc, lst in dp.items():
                for cost, path in lst:
                    for s, cs in o:
                        nd.setdefault(acc + s, []).append((cost + cs, path + [s]))
            dp = {a: sorted(l, key=lambda x: (x[0], x[1]))[:8] for a, l in nd.items()}
        for cost, path in dp.get(target, []):
            c = c0.copy()
            for d, s in zip(names, path):
                c[d] += s
            # no two districts on the same count
            if len(set(int(x) for x in c.values)) == len(c):
                sols.append((cost, abs(target), N1, c))
    sols.sort(key=lambda x: (x[0], x[1]))
    for cost, _, N1, c in sols:
        if margin_score(c) >= need:
            return c
    return c0


def steer(T, fam, log):
    """Plan the district counts, then move forward default-rate registrations between crossing and non-crossing
    transformers, one at a time, until the counts are the plan; a district that cannot move one way is re-planned
    around."""
    tx = T.tx
    rows = tx.set_index("ti")
    banned = set()
    for replan in range(12):
        counts, f, k1, e1 = golden_counts(T, fam)
        plan = plan_counts(counts, banned=banned)
        log["steer_plan"] = {d: int(plan[d] - counts[d]) for d in plan.index if plan[d] != counts[d]}
        failed = None
        for it in range(80):
            counts, f, k1, e1 = golden_counts(T, fam)
            diff = plan - counts
            if (diff == 0).all():
                log["steer_iterations"] = it
                log["steer_margin"] = round(margin_score(counts), 3)
                return T
            kk = dict(zip(tx["ti"], k1)); ee = dict(zip(tx["ti"], e1))
            r = K.rng("steer", replan, it)
            moved = False
            for d in diff.index[diff != 0]:
                s = int(np.sign(diff[d]))
                if move_one(T, fam, rows, kk, ee, K.NAMES.index(d), s, r, log):
                    moved = True
                    break
                failed = (d, s)
            if not moved:
                banned.add(failed)
                break
    log["steer_failed"] = sorted(banned)
    return T


def build(verbose=True):
    tic = time.time()
    T = Truth()
    T.tx = W.transformers()
    T.pr = W.premises(T.tx)
    T.veh, T.sw = W.fleet(T.tx, T.pr)
    T.pr_base = dict(zip(T.pr["pi"], T.pr["base_rate"]))
    global PI2TI, TI2DI, PREMS_OF, TI_POS, VEH_PREM
    PI2TI = dict(zip(T.pr["pi"], T.pr["ti"]))
    TI2DI = dict(zip(T.tx["ti"], T.tx["di"]))
    TI_POS = {t: i for i, t in enumerate(T.tx["ti"])}
    PREMS_OF = T.pr.groupby("ti")["pi"].apply(list).to_dict()
    VEH_PREM = set(T.veh["pi"])
    for y in K.SUMMERS:
        T.tx["pk%d" % y] = 0.0
        T.tx["pkday%d" % y] = 0
        T.tx["pkq%d" % y] = 0
    W.simulate(T.tx, T.veh, T.sw, T.pr_base)
    # the pilot's upsizings (before summer 2026) and the summer 2026 failure replacements
    T.kva_orig = T.tx["kva"].copy()
    T.pilot, T.wos, T.corr = W.pilot(T.tx)
    T.tx["kva_mid"] = T.tx["kva"]
    T.tx.loc[T.pilot["ti"].values, "kva_mid"] = T.pilot["kva_new"].values
    T.fail = W.failures(T.tx)
    T.tx["kva"] = T.tx["kva_mid"]
    T.tx.loc[T.fail["ti"].values, "kva"] = T.fail["kva_new"].values
    T.other = W.other_changes(T.tx)
    T.other = T.other[~T.other.ti.isin(set(T.pilot.ti) | set(T.fail.ti) | set(T.corr.ti)) | (T.other.kind == "MAINT")]
    up = T.other[T.other.kind == "LOAD"]
    T.tx.loc[up["ti"].values, "kva"] = up["kva_to"].values
    T.tx["sg"] = T.tx["kva"].map(lambda k: K.SIZE_GROUP.get(k, "L"))
    log = {k: 0 for k in ("reg_on_peak", "dep_on_peak", "sw_on_peak", "moved", "dep_cancelled", "sw_moved",
                          "fwd_reg_redrawn", "fwd_dep_skipped", "drive_skipped", "steer_moves")}
    for it in range(8):
        FW.panel_states(T.tx, T.veh, T.sw, T.pr_base)
        redo = boundary_and_holes(T.tx, T.veh, T.sw, T.pr_base, log)
        if verbose:
            print("fix-up pass %d: %d districts to re-simulate (%.0fs) %s" % (it, len(redo), time.time() - tic, log))
        if not redo:
            break
        W.simulate(T.tx, T.veh, T.sw, T.pr_base, years=(2026,), districts=sorted(redo))
    FW.panel_states(T.tx, T.veh, T.sw, T.pr_base)
    T.fam, T.P = FW.family(T.tx)
    place_forward(T, T.fam, log)
    steer(T, T.fam, log)
    T.counts, T.f, T.k1, T.e1 = golden_counts(T, T.fam)
    for name in T.fam:
        c, _, _, _ = golden_counts(T, T.fam, name)
        if not c.equals(T.counts):
            log.setdefault("family_mismatch", []).append(name)
    T.alloc, T.q = FW.allocate(T.counts)
    T.log = log
    T.prems_of = PREMS_OF
    T.pr_district = dict(zip(T.pr["pi"], T.pr["district"]))
    if verbose:
        print("truth built in %.0fs: %s" % (time.time() - tic, log))
    return T


def load(rebuild=False):
    if not rebuild and os.path.exists(CACHE) and os.environ.get("T164_CACHE") == "1":
        return pickle.load(open(CACHE, "rb"))
    T = build()
    if os.environ.get("T164_CACHE") == "1":
        pickle.dump(T, open(CACHE, "wb"))
    return T


if __name__ == "__main__":
    os.environ["T164_CACHE"] = "1"
    import truth as _self
    T = _self.load(rebuild=True)
    print(T.counts.to_dict())
    print(T.alloc.to_dict())
    print("quotas", {k: round(v, 3) for k, v in T.q.items()})
