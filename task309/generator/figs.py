"""Every owed figure from the cut pack, as the write-up and the goldens state them, written to figures.json."""
import json
import os

import params as P
import solve as S

HERE = os.path.dirname(os.path.abspath(__file__))


def m1(x):
    return round(x / 1e6, 1)


def m2(x):
    return round(x / 1e6, 2)


def k0(x):
    return int(round(x / 1e3))


def compute(target):
    r = S.main_call(target)
    names = [P.COUNTY_NAME[c] for c in P.CANDIDATES]
    g = r["removed"][S.GOLDEN]
    d = r["removed"][S.DEFAULT]
    tab = S.class_table(r["cells"])
    bt = r["bt"][S.GOLDEN]
    btd = r["bt"][S.DEFAULT]
    f = {
        "call": r["call"],
        "call_removed_musd": m1(g[r["call"]]),
        "runner_up": r["runner"],
        "aal_musd": {n: m2(r["aal"][n]) for n in names},
        "removed_musd_2dp": {n: m2(g[n]) for n in names},
        "default_removed_musd": {n: m2(d[n]) for n in names},
        "default_call": d.idxmax(),
        "one_ratio_pooled": round(float(S.adjustments(r["cells"])[S.DEFAULT](100.0)), 3),
        "class_cut": {str(k): round(float(v), 3) for k, v in sorted(tab.items()) if k >= 40},
        "cut_under_130": round(float(S._ratio(r["cells"][r["cells"].gust_mph < 130])), 3),
        "cut_130_up": round(float(S._ratio(r["cells"][r["cells"].gust_mph >= 130])), 3),
        "mg04_storms": [sid for sid, *_ in bt],
        "mg04_golden_pct": {sid: round(100 * e, 1) for sid, a, p, e in bt},
        "mg04_default_pct": {sid: round(100 * e, 1) for sid, a, p, e in btd},
        "mg04_paid_musd": {sid: m1(a) for sid, a, p, e in bt},
        "share_130_up": {},
        "constants": {"gust_split_mph": 130, "class_width_mph": 10, "mg04_tol_pct": round(100 * P.MG04_TOL),
                      "mg04_min_musd": P.MG04_MIN_PAID // 1_000_000, "kt_to_mph": S.KT, "round_homes": P.ROUND_HOMES,
                      "round_cost_musd": 18.0, "roof_age_years": 15, "storms_tested": len(bt),
                      "legacy_last_year": 2011},
    }
    m = S.vendor(target)
    for n in names:
        mm = m[m.county == n]
        f["share_130_up"][n] = round(100 * float(mm[mm.cls_lo >= 130].aal.sum() / mm.aal.sum()))
    a = S.ask_a(target)
    f["ask_a"] = {n: [int(a.loc[n, "homes"]), k0(a.loc[n, "cov"])] for n in names}
    b = S.ask_b(target)
    reg = S.storm_table(target).set_index("storm_id")
    f["ask_b"] = {reg.loc[sid, "storm_name"]: [k0(t), k0(af)] for sid, (t, af) in b.items()}
    c = S.ask_c(target)
    f["ask_c"] = {n: [int(c.loc[n, "homes"]), k0(c.loc[n, "cov"])] for n in names}
    return f, r


def write(target, path=os.path.join(HERE, "figures.json")):
    f, r = compute(target)
    with open(path, "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
    return f, r


if __name__ == "__main__":
    import sys
    print(json.dumps(write(sys.argv[1])[0], indent=1))
