"""task273 architecture 5: the cracker and mirror sheets, run on the cut pack (target/) against generator/figures.json.

The cracker lands the call, runs the hygiene battery and executes every filed rule; the mirror stops at the default
path (every controlled-load heater moved into the soak window). Each is scored on every graded figure, a hit within
half a unit of the stated rounding, and the pair ceiling is computed with the construction figures (forecast minima,
curtailment, further capacity) counted as ask weight, the conservative reading of a generated rubric.

    python3 task273/generator/cracker.py"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import build as B      # noqa: E402
import params as P     # noqa: E402

TASK = os.path.dirname(HERE)
CODE_OF = {n: c for c, n, *_ in P.SUBS}


def ask_routes(pk, der, on=P.REF_DAY):
    """Solar in service and its backstop share under the handlings a careful solver reaches for."""
    loc_cur, loc_any, alive = {}, {}, {}
    for m in pk.meters:
        loc_any[m["nmi"]] = m["zone_substation"]
        if not m["removed"]:
            loc_cur[m["nmi"]] = m["zone_substation"]
        a, b = A.to_date(m["installed"]), A.to_date(m["removed"])
        if a <= on and (b is None or b > on):
            alive[m["nmi"]] = True
    by_id = {r["application_id"]: r for r in der}

    def root(aid):
        while True:
            r = by_id[aid]
            if r["application_type"] == "New connection" or not r["prior_application"]:
                return aid
            aid = r["prior_application"]

    def run(key, where, anchor, exist=False):
        groups = {}
        for r in der:
            if r["status"] != "Commissioned" or r["commissioned"] > on:
                continue
            groups.setdefault(root(r["application_id"]) if key == "chain" else r["nmi"], []).append(r)
        cap = {c: 0.0 for c in A.CODES}
        bs = {c: 0.0 for c in A.CODES}
        for links in groups.values():
            links.sort(key=lambda r: (r["commissioned"], r["application_id"]))
            last = links[-1]
            nmi = last["nmi"]
            if exist and not alive.get(nmi):
                continue
            if where == "register":
                sub = CODE_OF[last["zone_substation_at_approval"]]
            elif where == "current":
                if nmi not in loc_cur:
                    continue
                sub = loc_cur[nmi]
            elif where == "current_or_register":
                sub = loc_cur.get(nmi, CODE_OF[last["zone_substation_at_approval"]])
            else:
                sub = loc_any[nmi]
            kw = float(last["inverter_kw"])
            if anchor == "serial":
                inst = min(r["commissioned"] for r in links if r["inverter_serial"] == last["inverter_serial"])
            else:
                inst = last["commissioned"]
            cap[sub] += kw
            if inst >= P.BACKSTOP_FROM:
                bs[sub] += kw
        return {c: v / 1000 for c, v in cap.items()}, {c: v / 1000 for c, v in bs.items()}
    return run


def hits(v, gold, unit):
    return [c for c in A.CODES if abs(round(v[c] / unit) * unit - gold[c]) < unit / 2]


def main(verbose=True):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    ps = F["per_substation"]
    target = os.path.join(TASK, "target")
    S = B.solve(target, {c: ps[c]["threshold_mw"] for c in ps})
    pk, der = S["pk"], S["der"]
    gold_cap = {c: ps[c]["in_service_mw"] for c in ps}
    gold_bs = {c: ps[c]["backstop_mw"] for c in ps}
    run = ask_routes(pk, der)
    routes = {
        "cracker": dict(key="chain", where="current_or_register", anchor="current"),
        "cracker, unmatched NMIs dropped": dict(key="chain", where="current", anchor="current"),
        "cracker, register's own substation": dict(key="chain", where="register", anchor="current"),
        "cracker, NMI keyed": dict(key="nmi", where="current_or_register", anchor="current"),
        "golden handling of the asks": dict(key="chain", where="any", anchor="serial", exist=True),
    }
    out = {}
    for name, kw in routes.items():
        cap, bs = run(**kw)
        out[name] = (hits(cap, gold_cap, 0.01), hits(bs, gold_bs, 0.01))
    # construction figures: the cracker is on the call (golden construction), the mirror stops at the default path
    g_min = {c: ps[c]["forecast_min_mw"] for c in ps}
    T = {c: ps[c]["threshold_mw"] for c in ps}
    mir_min = {c: S["mins"]["R2"][c] for c in ps}
    mir_des = set(S["sets"]["R2"])
    mir_hits_min = hits(mir_min, g_min, 0.1)
    import numpy as np
    mir_out = {}
    for c in ps:
        if c in mir_des:
            mir_out[c] = T[c] - S["mins"]["R2"][c]
        else:
            mir_out[c] = float(np.min((S["F"]["R2"][c] - T[c]) / S["pv"]))
    gold_out = {c: ps[c].get("curtail_mw", ps[c].get("headroom_mw")) for c in ps}
    same_kind = [c for c in ps if (c in mir_des) == ps[c]["designated"]]
    mir_hits_out = [c for c in hits(mir_out, gold_out, 0.1) if c in same_kind]
    n_cons, n_ask, n_chart = 32, 32, 5
    cr_cap, cr_bs = out["cracker"]
    lc = (n_cons + len(cr_cap) + len(cr_bs) + n_chart) / float(n_cons + n_ask + n_chart)
    ls = (len(mir_hits_min) + len(mir_hits_out) + len(cr_cap) + len(cr_bs) + 2) / float(n_cons + n_ask + n_chart)
    c_score = 38 + 7 + 55 * lc
    s_score = 5 + 7 + 55 * ls
    res = dict(routes={k: {"A_hits": len(v[0]), "B_hits": len(v[1])} for k, v in out.items()},
               mirror={"minima_hits": mir_hits_min, "curtail_or_further_hits": mir_hits_out},
               Lc=round(lc, 3), Ls=round(ls, 3), cracker_score=round(c_score, 1), mirror_score=round(s_score, 1),
               pair=round((c_score + s_score) / 2, 1), mirror_leakage_pct=round(100 * ls, 1),
               pack=B.digest(target)[:12])
    if verbose:
        for k, v in res["routes"].items():
            print("%-38s solar in service %2d/16 hit, backstop share %2d/16 hit" % (k, v["A_hits"], v["B_hits"]))
        print("mirror (default path): minima hit %s, curtailment or further capacity hit %s" %
              (mir_hits_min, mir_hits_out))
        print("Lc %.3f -> cracker %.1f; Ls %.3f -> mirror %.1f; pair %.1f; mirror leakage %.1f per cent of ask "
              "weight; pack %s" % (lc, c_score, ls, s_score, res["pair"], res["mirror_leakage_pct"], res["pack"]))
    return res


if __name__ == "__main__":
    main()
