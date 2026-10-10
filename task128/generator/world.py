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
    R0 = G.assemble_unbounded(colo_pkg, flagv)
    R1 = G.assemble_unbounded(colo_pkg, scorev)
    R2 = G.assemble_bounded(r2c, scorev)
    R3 = G.assemble_bounded(r3c, scorev)
    R4 = G.assemble_bounded(r4c, scorev)
    return {"R0": R0, "R1": R1, "R2": R2, "R3": R3, "R4": R4,
            "colo_pkg": colo_pkg, "r2c": r2c, "r3c": r3c, "r4c": r4c, "r4raw": r4raw,
            "drains": {"wh": wh, "day": day}}


def _estate_figs(hosts, spine, pool, scorev, r4c):
    """The six graded November figures under the answer (R4): colocated whole-host exposure plus the
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


def build_world(seed=SEED):
    rng = random.Random(seed)
    reg = Registry(rng)
    base_adv, role_adv = COLOM.build_advisories(rng, reg)
    hosts = COLOM.build_colo(rng, reg, base_adv, role_adv)
    chosts = CLOUDM.build_cloud_hosts(rng)
    pool = CLOUDM.build_cve_pool(rng, reg)
    spine = CLOUDM.build_spine(rng, chosts, pool)
    requests, req_rivals = WIN.build_requests(random.Random(seed + 20), hosts)
    COLOM.bind_acceptances(requests, hosts, base_adv, role_adv)
    fixed, co_truth, co_rivals, co_meta = CLOUDM.build_closeout(rng, reg)

    scorev = G.cloud_values(spine, pool, "score")
    flagv = G.cloud_values(spine, pool, "flag")
    rungs = _rungs(hosts, spine, pool, flagv, scorev)
    figs, chosen_cloud, split = _estate_figs(hosts, spine, pool, scorev, rungs["r4c"])

    # ---- tune the seven graded figures to sit mid-bin, by nudging safe tickets/hosts ----
    n_cloud = 300 - sum(rungs["r4c"][e][0] for e in COLO)
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
    figs, chosen_cloud, split = _estate_figs(hosts, spine, pool, scorev, rungs["r4c"])
    n_cloud = 300 - sum(rungs["r4c"][e][0] for e in COLO)
    cs = G._cloud_sorted(scorev)
    fb = cs[n_cloud] if len(cs) > n_cloud else cs[-1]
    first_below = {"estate": fb[2], "package": fb[3], "exposures": fb[0]}
    import asks as ASKM
    deployments, coverage, assets, ans_A, ans_B = ASKM.build_asks(seed, chosts)
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
