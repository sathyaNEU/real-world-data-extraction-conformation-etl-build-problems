"""Every owed figure from the pack alone (target/): the layer's 2027 value on each region by the golden route, the
default path, the standing family, the cheap routes, and the two submission asks with their ladders."""
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P

F = P.FILES
LW = {"windstorm": 3, "flood": 7, "freeze": 7}       # the hours clause in days: 72 hours, 168 hours
RET, LIM = P.RETENTION / 1e6, P.LIMIT / 1e6


def load(target):
    c = pd.read_parquet(os.path.join(target, F["claims"]))
    c["inc"] = c["paid"] + c["outstanding"]
    ex = pd.read_csv(os.path.join(target, F["exposure"]))
    ci = pd.read_excel(os.path.join(target, F["index"]), sheet_name="Index")
    I = {(int(r[0]), int(r[1])): float(r[2]) for r in ci.itertuples(index=False)}
    asm = pd.read_excel(os.path.join(target, F["plan"]), sheet_name="Assumptions")
    I27 = float(asm.loc[asm.Item == "Rebuild cost index, 2027 average", "Value"].iloc[0])
    pl = pd.read_excel(os.path.join(target, F["plan"]), sheet_name="Policies")
    PLAN = dict(zip(pl.iloc[:, 0], pl.iloc[:, 2]))
    return c, ex, I, I27, PLAN


def occurrences(target, mix_years=(2025,)):
    """each region's windstorm, flood and freeze catastrophes, one period from each catastrophe's first loss, with
    the claims per panel firm then and at the 2027 scale (the plan's 2027 policies spread by the district mix of
    mix_years, mid-2025 by default)"""
    c, ex, I, I27, PLAN = load(target)
    e25 = ex[ex.year.isin(mix_years)].groupby(["region", "postcode_district"], as_index=False).policies_in_force_mid_year.sum()
    e25["sh"] = e25.policies_in_force_mid_year / e25.groupby("region").policies_in_force_mid_year.transform("sum")
    p27 = {(r.region, r.postcode_district): r.sh * PLAN[r.region] for r in e25.itertuples()}
    pe = ex.set_index(["year", "region", "postcode_district"]).policies_in_force_mid_year
    d = c[c.peril.isin(P.CAT_PERILS)].copy()
    d["yr"] = d.date_of_loss.dt.year
    d["date"] = d.date_of_loss.dt.normalize()
    d["scale"] = [p27[(r, pc)] / pe[(y, r, pc)] for r, pc, y in zip(d.region, d.postcode_district, d.yr)]
    d["i_loss"] = [I27 / I[(t.year, t.month)] for t in d.date_of_loss]
    so = d["repair_signed_off"]
    d["i_sign"] = [I27 / I.get((s.year, s.month), I[max(I)]) if not pd.isna(s) else il for s, il in zip(so, d["i_loss"])]
    d["panel_job"] = d["repair_contractor"] != ""
    panel = c[c.repair_contractor != ""].groupby([c.date_of_loss.dt.year, "region"])["repair_contractor"].nunique()
    occ = []
    for (rg, peril), g in d.groupby(["region", "peril"]):
        daily = g.groupby("date").size()
        med = daily.median()
        thr = max(15, 5 * med)
        used = set()
        for d0 in sorted(daily[daily > thr].index):
            if d0 in used:
                continue
            start = d0
            for k in (1, 2):
                dd = d0 - pd.Timedelta(days=k)
                if daily.get(dd, 0) > max(4, 2 * med):
                    start = dd
            end = start + pd.Timedelta(days=LW[peril] - 1)
            x = g[(g["date"] >= start) & (g["date"] <= end)]
            for k in range(LW[peril]):
                used.add(start + pd.Timedelta(days=k))
            y = start.year
            n = len(x)
            npj = int(x.panel_job.sum())
            occ.append(dict(region=rg, peril=peril, start=start.date(), year=y, n=n, n27=float(x.scale.sum()),
                            panel=int(panel[(y, rg)]), panel25=int(panel[(2025, rg)]),
                            u_all=n / panel[(y, rg)], u27_all=float(x.scale.sum()) / panel[(2025, rg)],
                            u_pan=npj / panel[(y, rg)], u27_pan=float((x.scale * x.panel_job).sum()) / panel[(2025, rg)],
                            sev_loss=float((x.inc * x.i_loss).sum()) / n, sev_sign=float((x.inc * x.i_sign).sum()) / n,
                            L_loss=float((x.inc * x.scale * x.i_loss).sum()) / 1e6,
                            L_sign=float((x.inc * x.scale * x.i_sign).sum()) / 1e6))
    return pd.DataFrame(occ)


def fit(O, form, pool, ub, ib):
    """cost per claim on claims per panel firm across the catastrophes, with a level per peril"""
    E = O[O.n >= 150]
    if pool == "pennine":
        E = E[E.region == "Pennine"]
    u = E["u_" + ub].values
    yv = np.log(E["sev_" + ib].values)
    wt = E["n"].values
    perils = sorted(E.peril.unique())
    D = np.column_stack([(E["peril"] == p).astype(float) for p in perils])
    best = None
    if form == "hinge_lin":
        for u0 in np.arange(6, 34.5, 0.5):
            h = np.maximum(0, u - u0)
            for sl in np.arange(0.0, 0.1, 0.001):
                z = yv - np.log(1 + sl * h)
                b = np.array([np.average(z[D[:, j] == 1], weights=wt[D[:, j] == 1]) for j in range(len(perils))])
                sse = float((((D @ b) + np.log(1 + sl * h) - yv) ** 2 * wt).sum())
                if best is None or sse < best[0]:
                    best = (sse, u0, sl)
        sse, u0, sl = best
        return (lambda v: 1 + sl * np.maximum(0, v - u0)), dict(u0=u0, slope=sl)
    grid = np.arange(6, 34.5, 0.5) if form == "hinge_log" else [0.0]
    for u0 in grid:
        X = {"hinge_log": lambda: np.maximum(0, u - u0)[:, None], "linear_log": lambda: u[:, None],
             "quad_log": lambda: np.column_stack([u, u * u])}[form]()
        A = np.column_stack([D, X])
        W = np.sqrt(wt)[:, None]
        coef, *_ = np.linalg.lstsq(A * W, yv * W[:, 0], rcond=None)
        sse = float(((A @ coef - yv) ** 2 * wt).sum())
        if best is None or sse < best[0]:
            best = (sse, u0, coef[len(perils):])
    sse, u0, k = best
    if form == "hinge_log":
        return (lambda v: np.exp(k[0] * np.maximum(0, v - u0))), dict(u0=float(u0), k=float(k[0]))
    if form == "linear_log":
        return (lambda v: np.exp(k[0] * v)), dict(k=float(k[0]))
    return (lambda v: np.exp(k[0] * v + k[1] * v * v)), dict(k1=float(k[0]), k2=float(k[1]))


def annual(O, col, region):
    a = np.zeros(16)
    X = O[O.region == region]
    for y, L in zip(X.year, X[col]):
        a[y - 2010] += min(max(L - RET, 0), LIM)
    return np.minimum(a, 2 * LIM)


def value(O, col, region):
    p = P.PREMIUM[region] / 1e6
    a = annual(O, col, region)
    rec = a.mean()
    rip = (p * np.minimum(a, LIM) / LIM).mean()
    return dict(value=rec - p - rip, recoveries=rec, rip=rip, premium=p, by_year=[round(x, 3) for x in a])


def family(O):
    """the standing family: index from the month of loss or of sign-off, claims per firm on all claims or on the
    panel's jobs, four forms, fitted on every region or on Pennine alone"""
    cols = {}
    for ib in ("loss", "sign"):
        for ub in ("all", "pan"):
            for form in ("hinge_log", "hinge_lin", "linear_log", "quad_log"):
                for pool in ("all", "pennine"):
                    m, _ = fit(O, form, pool, ub, ib)
                    col = "G_%s_%s_%s_%s" % (ib, ub, form, pool)
                    O[col] = O["L_" + ib] * m(O["u27_" + ub].values) / m(O["u_" + ub].values)
                    cols[col] = dict(index=ib, u=ub, form=form, pool=pool)
    return cols


def cheap(O):
    """routes a response could take without the claims-per-firm step"""
    out = {}
    for scope, name in ((["region", "peril"], "T_rp"), (["region"], "T_r"), (["peril"], "T_p")):
        O[name] = O["L_loss"]
        for keys, g in O.groupby(scope):
            g2 = g[g.n >= 150]
            if len(g2) >= 3:
                b = np.polyfit(g2.year, np.log(g2.sev_loss), 1, w=np.sqrt(g2.n))[0]
                O.loc[g.index, name] = g["L_loss"] * np.exp(b * (2027 - g["year"]))
        out[name] = "severity trend by " + "+".join(scope)
    O["A_post"] = O["L_loss"]
    for (rg, per), g in O.groupby(["region", "peril"]):
        post, pre = g[g.year >= 2021], g[g.year < 2021]
        if len(post) and len(pre):
            O.loc[pre.index, "A_post"] = pre["L_loss"] * np.average(post.sev_loss, weights=post.n) / \
                np.average(pre.sev_loss, weights=pre.n)
    out["A_post"] = "each region's post-2021 cost per claim carried to its earlier catastrophes"
    E = O[O.n >= 150]
    perils = sorted(E.peril.unique())
    D = np.column_stack([(E.peril == p).astype(float) for p in perils])
    n27 = O.u27_all / O.u_all * O.n
    for name, x in (("N_count", E.n.values), ("N_scaled", E.n.values / E.groupby("region").n.transform("median").values)):
        A = np.column_stack([D, x])
        W = np.sqrt(E.n.values)[:, None]
        k = np.linalg.lstsq(A * W, np.log(E.sev_loss.values) * W[:, 0], rcond=None)[0][-1]
        if name == "N_count":
            O[name] = O["L_loss"] * np.exp(k * (n27 - O.n))
        else:
            O[name] = O["L_loss"] * np.exp(k * (n27 - O.n) / O.groupby("region").n.transform("median"))
        out[name] = "cost per claim on the catastrophe's claim count" + (" scaled by the region's median" if name == "N_scaled" else "")
    # the catastrophe's extra cost read off its size, its claim count or its loss, in four forms, pooled or by peril
    lown = O.sev_loss * O.n / 1e6
    for size, v_all, v27 in (("claims", O.n.astype(float), O.n27), ("loss", lown, O.L_loss)):
        vE = v_all[O.n >= 150].values
        for form in ("linear", "log", "quad", "hinge"):
            for by in ("pooled", "peril"):
                name = "Z_%s_%s_%s" % (size, form, by)
                O[name] = O["L_loss"] * np.exp(_size_term(E, vE, form, by, v27.values, O.peril.values)
                                               - _size_term(E, vE, form, by, v_all.values, O.peril.values))
                out[name] = "a surge on the catastrophe's %s, %s, %s" % ("claim count" if size == "claims" else "loss",
                                                                           form, by)
    return out


def _size_term(E, vE, form, by, v, peril):
    """the fitted log cost uplift at size v, from cost per claim on catastrophe size with a level per peril"""
    perils = sorted(E.peril.unique())
    D = np.column_stack([(E.peril == p).astype(float) for p in perils])
    yv, wt = np.log(E.sev_loss.values), E.n.values

    def X(a, u0, pr):
        a = np.asarray(a, dtype=float)
        m = {"linear": a[:, None], "log": np.log(a)[:, None], "quad": np.column_stack([a, a * a]),
             "hinge": np.maximum(0, a - (u0 or 0))[:, None]}[form]
        if by == "peril":
            m = np.column_stack([m * (pr == p)[:, None] for p in perils])
        return m
    best = None
    for u0 in (np.quantile(vE, np.linspace(0.05, 0.95, 40)) if form == "hinge" else [None]):
        A = np.column_stack([D, X(vE, u0, E.peril.values)])
        W = np.sqrt(wt)[:, None]
        coef, *_ = np.linalg.lstsq(A * W, yv * W[:, 0], rcond=None)
        sse = float((((A @ coef) - yv) ** 2 * wt).sum())
        if best is None or sse < best[0]:
            best = (sse, u0, coef[len(perils):])
    _, u0, k = best
    return X(v, u0, peril) @ k


def main_call(target):
    O = occurrences(target)
    m, par = fit(O, "hinge_log", "all", "all", "loss")
    O["G"] = O["L_loss"] * m(O["u27_all"].values) / m(O["u_all"].values)
    O["f"] = m(O["u27_all"].values) / m(O["u_all"].values)
    gold = {r: value(O, "G", r) for r in P.REGIONS}
    dflt = {r: value(O, "L_loss", r) for r in P.REGIONS}
    fam = family(O)
    famv = {col: {r: value(O, col, r)["value"] for r in P.REGIONS} for col in fam}
    famd = {ib: {r: value(O, "L_" + ib, r)["value"] for r in P.REGIONS} for ib in ("loss", "sign")}
    ch = cheap(O)
    chv = {col: {r: value(O, col, r)["value"] for r in P.REGIONS} for col in ch}
    return dict(O=O, fit=par, gold=gold, default=dflt, family=fam, family_values=famv, family_default=famd,
                cheap=ch, cheap_values=chv)


# ------------------------------------------------------------------ ask A: everyday claims per policy
def _mlu_sheets(target):
    wb = pd.read_excel(os.path.join(target, F["mlu"]), sheet_name=None, header=2)
    out = []
    for i, (name, df) in enumerate(wb.items()):
        df = df[df["MLU reference"].astype(str).str.startswith("MLU-")].copy()
        df["sheet"] = i
        out.append(df)
    return pd.concat(out, ignore_index=True), len(wb)


A_ROUTES = [("platform",)] + [(ret, date, reo) for ret in ("keep", "unit") for date in ("unit", "platform", "exact")
                                for reo in ("sum", "latest", "first")]
A_GOLDEN = ("keep", "unit", "sum")


def ask_a(target, route=A_GOLDEN):
    """incurred per policy in force, 2023 to 2025, on the escape of water, accidental damage, theft, fire and
    subsidence claims together. Each claim the Major Loss Unit holds is at the unit's figure: its latest report's where
    it is still listed in October 2026 or was closed, the platform's where it left the report open (sent back). A
    reopened case is a further cost on the same claim. The unit's date of loss is the claim's date, so a claim dated
    by the unit into another year moves year, and a 2026 platform claim the unit dates into 2025 joins 2025.

    route: ("platform",) or (returned: keep|unit, date: unit|platform|exact, reopened: sum|latest|first)"""
    c, ex, _, _, _ = load(target)
    pol = ex.groupby(["year", "region"]).policies_in_force_mid_year.sum()
    dmap = ex[ex.year == ex.year.max()].set_index("postcode_district").region.to_dict()
    x = c[c.peril.isin(P.NONCAT)].copy()
    x["yr"] = x.date_of_loss.dt.year
    x["pno"] = x.policy_ref.str[1:]
    x["dkey"] = x.date_of_loss.dt.normalize()
    extra = []
    if route != ("platform",):
        ret, datemode, reo = route
        M, ns = _mlu_sheets(target)
        M["pno"] = M["Policy number"].astype("int64").astype(str)
        M["dol"] = pd.to_datetime(M["Date of loss"]).dt.normalize()
        M["per"] = M.Peril.str.lower()
        M = M.sort_values("sheet", kind="stable")
        g = M.groupby("MLU reference", sort=False)
        last = g.tail(1).set_index("MLU reference")
        carried = g.dol.apply(lambda s: set(s)).to_dict()
        firstseen = g.sheet.min().to_dict()
        # a case's figure: listed in the last report or closed; otherwise it left the report open
        left = {r: not (last.loc[r, "sheet"] == ns - 1 or last.loc[r, "Status"] == "Closed") for r in last.index}
        # cases of one claim: same policy, peril and the date the claim now carries
        chains = {}
        for r in last.index:
            chains.setdefault((last.loc[r, "pno"], last.loc[r, "per"], last.loc[r, "dol"]), []).append(r)
        idx = {}
        for k, i in zip(zip(x.pno, x.peril, x.dkey), x.index):
            idx.setdefault(k, []).append(i)
        for (pno, per, dol), refs in chains.items():
            refs = sorted(refs, key=lambda r: firstseen[r])
            if reo == "sum":
                use = refs
            elif reo == "latest":
                use = refs[-1:]
            else:
                use = refs[:1]
            dates = set().union(*[carried[r] for r in refs])
            if datemode == "exact":
                dates = {dol}
            hit = [i for d in dates for i in idx.get((pno, per, d), [])]
            back = any(left[r] for r in use)
            if hit:
                i = hit[0]
                if back and ret == "keep":
                    continue
                x.loc[i, "inc"] = float(sum(last.loc[r, "Incurred"] for r in use))
                if datemode == "unit":
                    x.loc[i, "yr"] = dol.year
            elif datemode == "unit" and not (back and ret == "keep"):
                extra.append((dmap.get(last.loc[refs[0], "Postcode district"]), dol.year,
                              float(sum(last.loc[r, "Incurred"] for r in use))))
    s = x[x.yr.between(2023, 2025)].groupby(["region", "yr"]).inc.sum()
    out = {}
    for rg in P.REGIONS:
        for y in (2023, 2024, 2025):
            v = float(s.get((rg, y), 0.0)) + sum(e[2] for e in extra if e[0] == rg and e[1] == y)
            out["%s|%d" % (rg, y)] = v / pol[(y, rg)]
    return out


# ------------------------------------------------------------------ ask B: sums insured on 31 December 2025
def _bdx(target):
    ex = pd.read_csv(os.path.join(target, F["exposure"]))
    dmap = ex[ex.year == 2025].set_index("postcode_district").region
    B = pd.read_csv(os.path.join(target, F["bdx"]), dtype=str)
    for col in ("term_start", "term_end", "cancellation_effective", "endorsement_effective"):
        B[col] = pd.to_datetime(B[col], format="%d/%m/%Y", errors="coerce")
    B["buildings_sum_insured"] = B["buildings_sum_insured"].astype(float)
    B["region"] = B.postcode_district.map(dmap)
    B["ord"] = np.arange(len(B))
    return B


B_ROUTES = ["direct", "december", "union_policy", "union_term", "union_policy_back", "any_cancellation",
            "relisted_processed", "relisted_later", "snapshot", "snapshot_month_end", "golden"]
B_SAME = ["listed_december"]     # readings that must file the golden


def ask_b(target, route="golden"):
    """each region's buildings sums insured on 31 December 2025: the direct book that day and every scheme term in
    force that day at its sum insured that day. A term counts when its dates cover the day and no cancellation of it
    took effect by then; a listing names every term in force at some time in its month, so a term listed for a month
    that began after its cancellation took effect was reinstated. Endorsements count from their effective date; a
    rewrite ends one term and starts another under the same policy number."""
    D = pd.read_csv(os.path.join(target, F["direct"]))
    B = _bdx(target)
    dd = pd.Timestamp("2025-12-31")
    key = ["scheme_policy_no", "term_start"]
    lst = B[~B.transaction.isin(["Mid-term adjustment", "Cancelled"])]
    cover = lst[(lst.term_start <= dd) & (lst.term_end >= dd)]
    if route == "listed_december":
        # a reading that also asks for a listing for December or later: the same terms, since none leaves unexplained
        seen = lst.groupby(key).bordereau_month.max()
        seen = set(seen[seen >= "2025-12"].index)
        cover = cover[[k in seen for k in zip(cover.scheme_policy_no, cover.term_start)]]
    canc = B[B.transaction == "Cancelled"]
    if route == "direct":
        sch = pd.DataFrame(columns=["region", "si"])
    elif route == "december":
        x = cover[cover.bordereau_month == "2025-12"].sort_values("ord").drop_duplicates(key)
        sch = x.assign(si=x.buildings_sum_insured)[["region", "si"]]
    else:
        cut = canc if route == "any_cancellation" else canc[canc.cancellation_effective <= dd]
        back_ok = route in ("union_policy_back", "golden", "any_cancellation", "relisted_processed", "relisted_later",
                            "listed_december", "snapshot", "snapshot_month_end")
        relisted = set()
        if back_ok:
            lm = lst.groupby(key).bordereau_month.max()
            ms = pd.to_datetime(lm + "-01")
            for k, m, ce in zip(zip(cut.scheme_policy_no, cut.term_start), cut.bordereau_month, cut.cancellation_effective):
                if k not in lm.index:
                    continue
                if route == "relisted_processed":
                    hit = lm.loc[k] >= m           # any listing from the month the cancellation was processed
                elif route == "relisted_later":
                    hit = lm.loc[k] > m            # any listing after the month the cancellation was processed
                else:
                    hit = ms.loc[k] > ce           # a listing for a month that began after the cancellation took effect
                if hit:
                    relisted.add(k)
        out_keys = [k for k in zip(cut.scheme_policy_no, cut.term_start) if k not in relisted]
        x = cover.sort_values("ord")
        if route in ("union_policy", "union_policy_back"):
            gone = {k[0] for k in out_keys}
            x = x[~x.scheme_policy_no.isin(gone)]
        else:
            gone = set(out_keys)
            x = x[[k not in gone for k in zip(x.scheme_policy_no, x.term_start)]]
        if route.startswith("snapshot"):
            # the December listing read as the term on 31 December, the first later listing for a term keyed late
            x = x.assign(pref=np.where(x.bordereau_month == "2025-12", 0, np.where(x.bordereau_month > "2025-12", 1, 2)))
            x = x.sort_values(["pref", "bordereau_month", "ord"])
        base = x.groupby(key).head(1).set_index(key)
        mta = B[(B.transaction == "Mid-term adjustment") & (B.endorsement_effective <= dd)].sort_values(
            ["endorsement_effective", "ord"])
        if route == "snapshot":
            mta = mta[mta.bordereau_month >= "2025-12"]       # the endorsements keyed from December on
        elif route == "snapshot_month_end":
            mta = mta[mta.bordereau_month >= "2026-01"]       # December's own endorsements taken as in its listing
        mta = mta.groupby(key).tail(1).set_index(key)
        si = base.buildings_sum_insured.copy()
        hit = si.index.intersection(mta.index)
        si.loc[hit] = mta.loc[hit, "buildings_sum_insured"]
        sch = pd.DataFrame({"region": base.region, "si": si}).reset_index(drop=True)
    out = {}
    for rg in P.REGIONS:
        s = sch[sch.region == rg]
        d = D[D.region == rg]
        out[rg] = dict(si_m=(float(d.buildings_sums_insured_gbp.sum()) + float(s.si.sum())) / 1e6)
    return out


def all_figures(target):
    mc = main_call(target)
    A = {"golden": ask_a(target)}
    A.update({"|".join(r): ask_a(target, r) for r in A_ROUTES if r != A_GOLDEN})
    Bq = {r: ask_b(target, r) for r in B_ROUTES}
    return mc, A, Bq


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    mc, A, Bq = all_figures(tgt)
    print("fit", mc["fit"])
    for r in P.REGIONS:
        print("%-14s golden %+.3f  default %+.3f" % (r, mc["gold"][r]["value"], mc["default"][r]["value"]))
    for r, v in A.items():
        print("ask A %-18s" % r, " ".join("%.2f" % v[k] for k in sorted(v)))
    for r, v in Bq.items():
        print("ask B %-18s" % r, " ".join("%s %.1f" % (g[:4], v[g]["si_m"]) for g in P.REGIONS))
