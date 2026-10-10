"""Assemble the whole world once, deterministically, and tune the graded figures to sit mid-bin.

build_world() returns a dict with the colocated hosts, the cloud hosts and spine, the CVE pool, the
request corpus, the close-out, and the fully computed ladder (R0 to R4) with the answer split and
every graded figure. Tuning nudges a few safely selected cloud tickets by one finding each so every
graded figure (the six estate figures and the total) lands at least 3 from a multiple of ten.
"""
import random

from params import SEED, ESTATES, COLO, CLOUD
from cves import Registry
import colo as COLOM
import cloud as CLOUDM
import windows as WIN
import ladder as G


def _rungs(hosts, spine, pool, flagv, scorev):
    colo_pkg = G.colo_pkg_values(hosts, "score")
    wh, day = WIN.nov_drains()
    r2c = {e: G.colo_drains_per_package(hosts, day[e])[e] for e in COLO}
    r3c = {e: G.colo_drains_per_package(hosts, wh[e])[e] for e in COLO}
    r4raw = {e: G.colo_whole_host(hosts, wh[e])[e] for e in COLO}
    r4c = {e: (r4raw[e][0], r4raw[e][1]) for e in COLO}
    r5raw = G.colo_per_window(hosts, WIN.nov_windows())
    r5c = {e: (r5raw[e][0], r5raw[e][1]) for e in COLO}
    R0 = G.assemble_unbounded(colo_pkg, flagv)
    R1 = G.assemble_unbounded(colo_pkg, scorev)
    R2 = G.assemble_bounded(r2c, scorev)
    R3 = G.assemble_bounded(r3c, scorev)
    R4 = G.assemble_bounded(r4c, scorev)
    R5 = G.assemble_bounded(r5c, scorev)
    return {"R0": R0, "R1": R1, "R2": R2, "R3": R3, "R4": R4, "R5": R5,
            "colo_pkg": colo_pkg, "r2c": r2c, "r3c": r3c, "r4c": r4c, "r4raw": r4raw,
            "r5c": r5c, "r5raw": r5raw,
            "drains": {"wh": wh, "day": day}}


def _estate_figs(hosts, spine, pool, scorev, r4c):
    """The six graded November figures under the answer (R5, passed as r4c): colocated whole-host
    exposure plus the
    selected cloud ticket exposure per estate. Returns {estate: figure} and the per-estate ticket
    lists needed to tune."""
    split, total, boundary = G.assemble_bounded(r4c, scorev)
    # recompute per-estate cloud exposure for the chosen cloud tickets
    n_cloud = 300 - sum(r4c[e][0] for e in COLO)
    cs = G._cloud_sorted(scorev)[:n_cloud]
    cloud_exp = {e: 0 for e in ESTATES}
    for v, _, e, p in cs:
        cloud_exp[e] += v
    figs = {}
    for e in COLO:
        figs[e] = r4c[e][1]
    for e in CLOUD:
        figs[e] = cloud_exp[e]
    figs["_total"] = total
    return figs, cs, split


def _mid_bin(x):
    """Integer distance of x from the nearest-ten rounding edge (the x5 value); mid-bin means >= 3
    and not on the round value itself, so residues 1, 2, 8 and 9 qualify."""
    r = x % 10
    return abs(r - 5) if r else 0


def _residue_delta(fig, aim=2):
    """Smallest non-negative delta that lands fig at residue `aim` mod 10 (1, 2, 8, 9 are mid-bin)."""
    return (aim - fig % 10) % 10


def _safe_cloud_ticket(scorev, est, n_cloud):
    """The highest-value selected cloud ticket on estate `est`, far above the cutline."""
    cs = G._cloud_sorted(scorev)[:n_cloud]
    for v, _, e, p in cs:
        if e == est:
            return p
    return None


def _tune_cutline(pool, scorev, n_cloud):
    """Shift pool targets so that exactly n_cloud - 1 cloud tickets take out at least a + 1, one
    takes out a (the last ticket in), one takes out a - 1 (the first below the line) and every other
    takes out at most a - 2, where a is the value at the line before tuning."""
    cs = G._cloud_sorted(scorev)
    a = cs[n_cloud - 1][0]
    above = [x for x in cs if x[0] > a]
    at = [x for x in cs if x[0] == a]
    below = [x for x in cs if x[0] < a]
    need = (n_cloud - 1) - len(above)          # tickets lifted from a and a - 1 to a + 1
    lift_a = at[:-1][:need] if need > 0 else []
    rest_a = [x for x in at if x not in lift_a]
    last_in = rest_a[0]
    others = rest_a[1:]
    lifts = [(x, a + 1 - x[0]) for x in lift_a]
    short = need - len(lift_a)
    nxt = [x for x in below if x[0] == a - 1]
    if short > 0:
        lifts += [(x, 2) for x in nxt[:short]]
        nxt = nxt[short:]
    # the first below: one ticket at a - 1; everything else at a, or at a - 1, drops to a - 2
    first_below = (others + nxt)[0]
    drops = [(x, (a - 1) - x[0]) for x in [first_below] if x[0] != a - 1]
    drops += [(x, (a - 2) - x[0]) for x in (others + nxt)[1:]]
    for (v, _, e, p), d in lifts + drops:
        pool[(e, p)]["target"] += d
    return last_in


def _tune_two_lines(pool, scorev, n_ans, n_r4):
    """Shift pool targets so the answer's line (n_ans cloud tickets) and the stop rung's line (n_r4)
    are both strict: n_ans - 1 tickets at a + 1 or more, the last in at a, the first below at a - 1,
    the next n_r4 - n_ans - 1 at a - 2 (the stop rung takes them), everything else at a - 3 or less.
    The seven tickets the stop rung adds over the answer are drawn round-robin over the four cloud
    estates, so every cloud count differs between the two rungs."""
    cs = G._cloud_sorted(scorev)
    a = cs[n_ans - 1][0]
    above = [x for x in cs if x[0] > a]
    mid = [x for x in cs if a - 2 <= x[0] <= a]
    need = (n_ans - 1) - len(above)
    k_extra = n_r4 - n_ans                      # first below plus the stop rung's other extras
    # pick the extras round-robin over estates from the bottom of the near-line pool
    by_e = {e: [x for x in reversed(mid) if x[2] == e] for e in CLOUD}
    extras, i = [], 0
    while len(extras) < k_extra:
        e = CLOUD[i % len(CLOUD)]
        if by_e[e]:
            extras.append(by_e[e].pop(0))
        i += 1
        if i > 400:
            raise SystemExit("not enough near-line cloud tickets to spread the stop rung's extras")
    rest = [x for x in mid if x not in extras]
    last_in = [x for x in rest if x[0] == a][-1] if any(x[0] == a for x in rest) else rest[-1]
    rest = [x for x in rest if x is not last_in]
    lifts = rest[:need]
    drops = rest[need:]
    plan = [(x, a + 1 - x[0]) for x in lifts] + [(last_in, a - last_in[0])]
    plan += [(extras[0], a - 1 - extras[0][0])] + [(x, a - 2 - x[0]) for x in extras[1:]]
    plan += [(x, a - 3 - x[0]) for x in drops]
    for (v, _, e, p), d in plan:
        pool[(e, p)]["target"] += d
    return last_in


def build_world(seed=SEED):
    rng = random.Random(seed)
    reg = Registry(rng)
    base_adv, role_adv = COLOM.build_advisories(rng, reg)
    hosts = COLOM.build_colo(rng, reg, base_adv, role_adv)
    chosts = CLOUDM.build_cloud_hosts(rng)
    pool = CLOUDM.build_cve_pool(rng, reg)
    spine = CLOUDM.build_spine(rng, chosts, pool)
    requests, req_rivals = WIN.build_requests(random.Random(seed + 20), hosts)
    WIN.mark_office(requests, seed)
    COLOM.bind_acceptances(requests, hosts, base_adv, role_adv)
    fixed, co_truth, co_rivals, co_meta = CLOUDM.build_closeout(rng, reg)

    scorev = G.cloud_values(spine, pool, "score")
    flagv = G.cloud_values(spine, pool, "flag")
    rungs = _rungs(hosts, spine, pool, flagv, scorev)
    figs, chosen_cloud, split = _estate_figs(hosts, spine, pool, scorev, rungs["r5c"])

    # ---- make the answer's cutline strict: one ticket at the last value in, one at the first
    # value out, every other ticket clear of both ----
    n_cloud = 300 - sum(rungs["r5c"][e][0] for e in COLO)
    n_r4 = 300 - sum(rungs["r4c"][e][0] for e in COLO)
    _tune_two_lines(pool, scorev, n_cloud, n_r4)
    W0 = _rebuild(seed, pool, {})
    pool, scorev, figs = W0["_pool_final"], W0["scorev"], W0["figs"]

    # ---- tune the seven graded figures to sit mid-bin, by nudging safe tickets/hosts ----
    # cloud: shrink one safe (high-value, far above the cutline) selected ticket per estate so its
    # estate figure reaches residue 2; shrinking always has headroom on a top ticket
    for e in CLOUD:
        down = (figs[e] % 10 - 2) % 10
        if down:
            pkg = _safe_cloud_ticket(scorev, e, n_cloud)
            ent = pool[(e, pkg)]
            ent["target"] = max(6, ent["target"] - down)
    # colo: add d exploitable findings to the most-exposed drained host of each estate
    colo_tune = {}
    for e in COLO:
        d = _residue_delta(figs[e])
        colo_tune[e] = d
    # total: shift the search estate's safe ticket further so the total also lands mid-bin
    # (recomputed after the per-estate nudges below)
    W = _rebuild(seed, pool, colo_tune)
    # fix the total if needed, keeping search mid-bin
    if _mid_bin(W["figs"]["_total"]) < 3:
        for extra in range(0, 10):
            # shrink search by `extra`, keeping search and the total mid-bin
            if _mid_bin(W["figs"]["search"] - extra) >= 3 and _mid_bin(W["figs"]["_total"] - extra) >= 3:
                pkg = _safe_cloud_ticket(W["scorev"], "search", n_cloud)
                W = _rebuild(seed, W["_pool_final"], W["_colo_tune"], extra_cloud=("search", pkg, -extra))
                break
    return W


def _rebuild(seed, pool_targets, colo_tune, extra_cloud=None):
    """Second pass: rebuild spine from the tuned pool targets and apply the colocated host nudges."""
    rng = random.Random(seed)
    reg = Registry(rng)
    base_adv, role_adv = COLOM.build_advisories(rng, reg)
    hosts = COLOM.build_colo(rng, reg, base_adv, role_adv)
    chosts = CLOUDM.build_cloud_hosts(rng)
    pool = CLOUDM.build_cve_pool(rng, reg)
    # carry the tuned targets across (same keys, deterministic)
    for k, ent in pool.items():
        if k in pool_targets and isinstance(pool_targets[k], dict):
            ent["target"] = pool_targets[k]["target"]
    if extra_cloud:
        e, p, extra = extra_cloud
        pool[(e, p)]["target"] += extra
    spine = CLOUDM.build_spine(rng, chosts, pool)
    requests, req_rivals = WIN.build_requests(random.Random(seed + 20), hosts)
    WIN.mark_office(requests, seed)
    COLOM.bind_acceptances(requests, hosts, base_adv, role_adv)
    fixed, co_truth, co_rivals, co_meta = CLOUDM.build_closeout(rng, reg)
    # colocated host nudges: add `d` exploitable findings to the most-exposed drained host
    wh, _ = WIN.nov_drains()
    for e in COLO:
        d = colo_tune.get(e, 0)
        if not d:
            continue
        ranked = sorted(hosts[e], key=lambda h: (-h.whole(), h.hid))
        for h0 in ranked[:5]:
            if COLOM.tune_host(h0, d, base_adv, role_adv):
                break
        else:
            raise SystemExit(f"colocated tuning found no package set for {e} delta {d}")
    scorev = G.cloud_values(spine, pool, "score")
    flagv = G.cloud_values(spine, pool, "flag")
    rungs = _rungs(hosts, spine, pool, flagv, scorev)
    figs, chosen_cloud, split = _estate_figs(hosts, spine, pool, scorev, rungs["r5c"])
    n_cloud = 300 - sum(rungs["r5c"][e][0] for e in COLO)
    cs = G._cloud_sorted(scorev)
    fb = cs[n_cloud] if len(cs) > n_cloud else cs[-1]
    first_below = {"estate": fb[2], "package": fb[3], "exposures": fb[0]}
    import asks as ASKM
    deployments, coverage, assets, ans_A, ans_B = ASKM.build_asks(seed, chosts, requests)
    out = {"rng": rng, "reg": reg, "base_adv": base_adv, "role_adv": role_adv,
           "deployments": deployments, "coverage": coverage, "assets": assets,
           "ans_A": ans_A, "ans_B": ans_B, "first_below": first_below,
           "hosts": hosts, "chosts": chosts, "pool": pool, "spine": spine,
           "requests": requests, "req_rivals": req_rivals,
           "fixed": fixed, "co_truth": co_truth, "co_rivals": co_rivals, "co_meta": co_meta,
           "scorev": scorev, "flagv": flagv, "rungs": rungs, "figs": figs,
           "chosen_cloud": chosen_cloud, "answer_split": split,
           "_pool_final": pool, "_colo_tune": colo_tune}
    return out


if __name__ == "__main__":
    W = build_world()
    f = W["figs"]
    for e in ESTATES:
        print(e, "fig", f[e], "mid-bin dist", _mid_bin(f[e]))
    print("total", f["_total"], "mid-bin", _mid_bin(f["_total"]))
    print("split", "/".join(str(W["answer_split"][e]) for e in ESTATES))
