"""Independent verifier: every graded figure recomputed from target/ by code that shares nothing with solve.py, then
compared with figures.json.

    python3 task308/generator/verify.py <target dir>
"""
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REG = ["Fenland", "Pennine", "Severn Vale", "Coastal North"]
PREM = {"Fenland": 2.155, "Pennine": 2.93, "Severn Vale": 4.34, "Coastal North": 4.17}
HOURS_DAYS = {"windstorm": 3, "flood": 7, "freeze": 7}


def files(t):
    out = {}
    for f in os.listdir(t):
        out[f.split("_")[0]] = os.path.join(t, f)
    return out


def main(t):
    fx = sorted(os.listdir(t))
    get = lambda stem: os.path.join(t, [f for f in fx if f.startswith(stem)][0])
    claims = pd.read_parquet(get("home_claims"))
    claims["inc"] = claims.paid.values + claims.outstanding.values
    expo = pd.read_csv(get("exposure_by_district"))
    idx = pd.read_excel(get("rebuild_cost_index"), sheet_name=0)
    idx.columns = ["y", "m", "v"]
    ix = {(a, b): v for a, b, v in idx.itertuples(index=False)}
    plan_p = pd.read_excel(get("business_plan"), sheet_name="Policies")
    plan_a = pd.read_excel(get("business_plan"), sheet_name="Assumptions")
    i27 = float(plan_a[plan_a.iloc[:, 0].str.startswith("Rebuild cost index")].iloc[0, 1])
    p27 = dict(zip(plan_p.iloc[:, 0], plan_p.iloc[:, 2]))

    # 2027 policies per district, and each claim's book factor and cost factor
    e = expo.set_index(["year", "postcode_district"])
    last = expo[expo.year == expo.year.max()]
    mix = last.policies_in_force_mid_year / last.groupby("region").policies_in_force_mid_year.transform("sum")
    d27 = dict(zip(last.postcode_district, mix.values * last.region.map(p27).values))
    cat = claims[claims.peril.isin(list(HOURS_DAYS))].copy()
    yrs = cat.date_of_loss.dt.year.values
    cat["book"] = [d27[d] / e.loc[(y, d), "policies_in_force_mid_year"] for y, d in zip(yrs, cat.postcode_district)]
    cat["cost"] = [i27 / ix[(a.year, a.month)] for a in cat.date_of_loss]
    firms = claims[claims.repair_contractor.str.len() > 0].groupby([claims.date_of_loss.dt.year, "region"]).repair_contractor.nunique()

    # catastrophes: a run of days whose count stands far above the region's usual day for the peril; one period
    # from the run's first day
    occ = []
    for (rg, pr), g in cat.groupby(["region", "peril"]):
        days = g.date_of_loss.dt.normalize()
        cnt = days.value_counts().sort_index()
        base = float(np.median(cnt.values))
        spikes = cnt[cnt > max(15, 5 * base)].index
        taken = pd.DatetimeIndex([])
        for s0 in spikes:
            if s0 in taken:
                continue
            first = s0
            for back in (1, 2):
                if cnt.get(s0 - pd.Timedelta(days=back), 0) > max(4, 2 * base):
                    first = s0 - pd.Timedelta(days=back)
            span = pd.date_range(first, periods=HOURS_DAYS[pr])
            taken = taken.union(span)
            w = g[days.isin(span).values]
            n = len(w)
            yr = first.year
            occ.append((rg, pr, yr, n, n / firms[(yr, rg)], w.book.sum() / firms[(2025, rg)],
                        float((w.inc * w.cost).sum()) / n, float((w.inc * w.book * w.cost).sum()) / 1e6))
    O = pd.DataFrame(occ, columns=["rg", "pr", "yr", "n", "u", "u27", "sev", "L"])

    # cost per claim on claims per firm: a level per peril and one slope past a threshold, log scale, claim-weighted
    E = O[O.n >= 150]
    best = None
    for th in np.arange(6.0, 34.5, 0.5):
        X = np.column_stack([pd.get_dummies(E.pr).values.astype(float), np.clip(E.u.values - th, 0, None)])
        wsq = np.sqrt(E.n.values)
        beta = np.linalg.lstsq(X * wsq[:, None], np.log(E.sev.values) * wsq, rcond=None)[0]
        err = float((((X @ beta) - np.log(E.sev.values)) ** 2 * E.n.values).sum())
        if best is None or err < best[0]:
            best = (err, th, beta[-1])
    _, th, k = best
    O["G"] = O.L * np.exp(k * (np.clip(O.u27 - th, 0, None) - np.clip(O.u - th, 0, None)))

    val = {}
    for rg in REG:
        a = np.zeros(16)
        for yr, L in zip(O[O.rg == rg].yr, O[O.rg == rg].G):
            a[yr - 2010] += min(max(L - 10.0, 0.0), 15.0)
        a = np.minimum(a, 30.0)
        val[rg] = a.mean() - PREM[rg] - (PREM[rg] * np.minimum(a, 15.0) / 15.0).mean()

    # ask A: every report row of every unit case, in report order
    pol = expo.groupby(["year", "region"]).policies_in_force_mid_year.sum()
    sheets = pd.read_excel(get("major_loss_unit"), sheet_name=None, header=2)
    names = list(sheets)
    hist = {}
    for i, nm in enumerate(names):
        sh = sheets[nm]
        sh = sh[sh.iloc[:, 0].astype(str).str.startswith("MLU-")]
        for r in sh.itertuples(index=False):
            hist.setdefault(r[0], []).append((i, str(int(r[1])), r[2], str(r[3]).lower(), pd.Timestamp(r[4]).normalize(),
                                              float(r[9]), r[10]))
    # a case's last word: listed in the last report or closed; otherwise it left the report open
    cases = {}
    for ref, h in hist.items():
        i, pno, dist, per, dol, inc, st = h[-1]
        cases[ref] = dict(pno=pno, dist=dist, per=per, now=dol, dates={x[4] for x in h},
                          fin=inc if (i == len(names) - 1 or st == "Closed") else None)
    # cases of one claim share a policy, a peril and a date
    parent = {r: r for r in cases}

    def root(r):
        while parent[r] != r:
            parent[r] = parent[parent[r]]
            r = parent[r]
        return r
    seen_k = {}
    for r, cs in cases.items():
        for d in cs["dates"]:
            k = (cs["pno"], cs["per"], d)
            if k in seen_k:
                parent[root(r)] = root(seen_k[k])
            else:
                seen_k[k] = r
    groups = {}
    for r in cases:
        groups.setdefault(root(r), []).append(r)
    nc = claims[claims.peril.isin(["escape of water", "accidental damage", "theft", "fire", "subsidence"])].copy()
    nc["year"] = nc.date_of_loss.dt.year
    nc["inc2"] = nc.inc.values
    look = {}
    for i, k in zip(nc.index, zip(nc.policy_ref.str[1:], nc.peril, nc.date_of_loss.dt.normalize())):
        look.setdefault(k, i)
    dreg = dict(zip(last.postcode_district, last.region))
    add = {}
    for g in groups.values():
        cs = [cases[r] for r in g]
        now = max(c["now"] for c in cs)
        ks = [(c["pno"], c["per"], d) for c in cs for d in c["dates"]]
        hit = [look[k] for k in ks if k in look]
        if any(c["fin"] is None for c in cs):
            continue                      # back on the platform: its own figure stands
        tot = sum(c["fin"] for c in cs)
        if hit:
            nc.loc[hit[0], "inc2"] = tot
            nc.loc[hit[0], "year"] = now.year
        else:
            k = (dreg[cs[0]["dist"]], now.year)
            add[k] = add.get(k, 0.0) + tot
    tot = nc.groupby(["region", "year"]).inc2.sum()
    askA = {rg: {str(y): round((tot.get((rg, y), 0.0) + add.get((rg, y), 0.0)) / pol[(y, rg)] + 1e-9, 2)
                 for y in (2023, 2024, 2025)} for rg in REG}

    # ask B: a term is in force on 31 December when its dates cover the day and no cancellation of it took effect by
    # then, unless it is listed for a later month that began after the cancellation took effect (a reinstatement); its
    # sum insured is the first listing's, moved by endorsements effective by then
    bd = pd.read_csv(get("lowther_pike"), dtype=str)
    pdt = lambda s: pd.to_datetime(s, format="%d/%m/%Y", errors="coerce")
    for col in ("term_start", "term_end", "cancellation_effective", "endorsement_effective"):
        bd[col] = pdt(bd[col])
    day = pd.Timestamp(2025, 12, 31)
    terms = {}
    for r in bd.itertuples(index=False):
        tm = terms.setdefault((r.scheme_policy_no, r.term_start), dict(rows=[], mtas=[], district=r.postcode_district))
        if r.transaction == "Mid-term adjustment":
            tm["mtas"].append((r.endorsement_effective, float(r.buildings_sum_insured)))
        else:
            tm["rows"].append(r)
    dmap = dict(zip(last.postcode_district, last.region))
    scheme = {rg: 0.0 for rg in REG}
    for tm in terms.values():
        covers = [r for r in tm["rows"] if r.transaction != "Cancelled" and r.term_start <= day <= r.term_end]
        if not covers:
            continue
        # out when a cancellation effective by the day was never followed by a month the term was in force after it
        months = [pd.Timestamp(r.bordereau_month + "-01") for r in tm["rows"] if r.transaction != "Cancelled"]
        cuts = [r.cancellation_effective for r in tm["rows"] if r.transaction == "Cancelled"
                and r.cancellation_effective <= day]
        if any(not any(m > ce for m in months) for ce in cuts):
            continue
        si = float(covers[0].buildings_sum_insured)
        for eff, s in sorted(tm["mtas"], key=lambda q: q[0]):
            if eff <= day:
                si = s
        scheme[dmap[tm["district"]]] += si
    dr = pd.read_csv(get("direct_policies"))
    askB = {rg: round((dr[dr.region == rg].buildings_sums_insured_gbp.sum() + scheme[rg]) / 1e6 + 1e-9, 1) for rg in REG}

    figs = json.load(open(os.path.join(HERE, "figures.json")))
    bad = []
    for rg in REG:
        if round(val[rg] + 1e-9, 1) != figs["values"][rg]:
            bad.append(("value", rg, round(val[rg], 3), figs["values"][rg]))
        for y in ("2023", "2024", "2025"):
            if abs(askA[rg][y] - figs["askA"][rg][y]) > 0.001:
                bad.append(("askA", rg, y, askA[rg][y], figs["askA"][rg][y]))
        if askB[rg] != figs["askB"][rg]:
            bad.append(("askB", rg, askB[rg], figs["askB"][rg]))
    pick = max(val, key=val.get)
    if pick != figs["call"]["region"]:
        bad.append(("call", pick, figs["call"]["region"]))
    print("verify: %s; call %s %.3f; %d figures compared" % ("OK" if not bad else "MISMATCH", pick, val[pick], 1 + 4 + 12 + 4))
    for b in bad:
        print("   ", b)
    return 1 if bad else 0


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(main(tgt))
