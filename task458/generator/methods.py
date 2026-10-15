"""Every route to each county's members with each condition, on the shipped files: the golden (each identified member
weighted by the months it was observed), its valid variants, the default path's completion, the reflexes and the Layer 1
slips; each route's three standards and designated set."""
import datetime as dt

import numpy as np
import pandas as pd

import conform as CF

GOLD = ("Adams", "Douglas", "Franklin", "Grant", "Okanogan")


def _cells(mem, key):
    return mem.groupby(["county", "group"])[key].sum().unstack(fill_value=0).reindex(index=CF.COUNTIES, columns=CF.GROUPS,
                                                                                    fill_value=0)


def needs(a):
    """route -> (members with a serious mental illness by county, with an opioid use disorder, reach numerator)."""
    return needs_from(a["members"], a.get("final"), a.get("spans_days"))


def _shares(fy, cond, k_max=12):
    return np.array([float((fy["first_" + cond] <= k).mean()) if len(fy) else np.nan for k in range(1, k_max + 1)])


def ipw(mem, cond, by=None):
    """Each identified member counted as 1 over F(m): the share of the members enrolled all year with the condition,
    in the member's stratum (by=None the plan, 'group', or 'cell' county and group), identified within their first m
    contract-year months, m the member's months enrolled."""
    rec = mem[mem["rec_" + cond]]
    fy_all = mem[mem["full_year"] & mem["rec_" + cond]]
    if by is None:
        cap = _shares(fy_all, cond)
        w = 1.0 / cap[rec["months"].values - 1]
        return pd.Series(w, index=rec.index).groupby(rec["county"]).sum().reindex(CF.COUNTIES, fill_value=0.0)
    keys = ["group"] if by == "group" else ["county", "group"]
    out = pd.Series(0.0, index=CF.COUNTIES)
    for key, part in rec.groupby(keys):
        key = key if isinstance(key, tuple) else (key,)
        sel = fy_all
        for col, v in zip(keys, key):
            sel = sel[sel[col] == v]
        cap = _shares(sel, cond)
        w = 1.0 / cap[part["months"].values - 1]
        out = out.add(pd.Series(w, index=part.index).groupby(part["county"]).sum(), fill_value=0.0)
    return out.reindex(CF.COUNTIES, fill_value=0.0)


def needs_from(members, final=None, days=None):
    mem = members.copy()
    mem["one"] = 1
    mem["fy"] = mem["full_year"].astype(int)
    mem["m11"] = (mem["months"] >= 11).astype(int)
    for c in ("rec_smi", "rec_oud"):
        mem[c + "_fy"] = (mem[c] & mem["full_year"]).astype(int)
        mem[c + "_11"] = (mem[c] & (mem["months"] >= 11)).astype(int)
    mem["seen_smi"] = (mem["rec_smi"] & mem["seen"]).astype(int)
    N, NF, N11 = _cells(mem, "one"), _cells(mem, "fy"), _cells(mem, "m11")
    MM = _cells(mem, "months")
    seen = _cells(mem, "seen_smi").sum(axis=1)
    out = {}
    per = {}
    for cond in ("smi", "oud"):
        rec = _cells(mem, "rec_" + cond)
        rfy = _cells(mem, "rec_%s_fy" % cond)
        r11 = _cells(mem, "rec_%s_11" % cond)
        d = {}
        if "first_" + cond in mem:
            d["golden"] = ipw(mem, cond)
            d["ipw_group"] = ipw(mem, cond, "group")
            d["ipw_cell"] = ipw(mem, cond, "cell")
            d["fitted_capture"] = _fitted(mem, cond)
        d["full_year_group"] = (N * rfy / NF).sum(axis=1)
        d["full_year_group_11"] = (N * r11 / N11).sum(axis=1)
        d["plan_group"] = (N * (rfy.sum() / NF.sum())).sum(axis=1)
        d["recorded"] = rec.sum(axis=1)
        d["full_year_only"] = rfy.sum(axis=1)
        d["county_full_year"] = rfy.sum(axis=1) / NF.sum(axis=1) * N.sum(axis=1)
        d["county_full_year_11"] = r11.sum(axis=1) / N11.sum(axis=1) * N.sum(axis=1)
        d["plan_full_year"] = rfy.values.sum() / NF.values.sum() * N.sum(axis=1)
        d["pooled_factor"] = rec.sum(axis=1) * (rfy.values.sum() / NF.values.sum() * N.values.sum() / rec.values.sum())
        d["plan_recorded_group"] = (N * (rec.sum() / N.sum())).sum(axis=1)
        d["exposure"] = (rec / MM * 12 * N).sum(axis=1)
        if "first_day_" + cond in mem and "days" in mem:
            d["ipw_days"] = _ipw_days(mem, cond)
        per[cond] = d
    for k in per["smi"]:
        sn = mem[mem["full_year"]].groupby("county")["seen_smi"].sum().reindex(CF.COUNTIES) if k == "full_year_only" else seen
        out[k] = (per["smi"][k], per["oud"][k], sn)
    return out


def _fitted(mem, cond):
    """The cross-sectional reflex: within each group, the share identified among members enrolled m months fitted to
    r(1 - exp(-lambda m)), each identified member then counted as 1 over 1 - exp(-lambda m)."""
    from scipy.optimize import curve_fit
    out = pd.Series(0.0, index=CF.COUNTIES)
    for g, part in mem.groupby("group"):
        ms = np.arange(1, 13)
        sh = np.array([part.loc[part["months"] == m, "rec_" + cond].mean() if (part["months"] == m).sum() else np.nan for m in ms])
        n = np.array([(part["months"] == m).sum() for m in ms])
        ok = n >= 20
        (r_, l_), _ = curve_fit(lambda x, r, l: r * (1 - np.exp(-l * x)), ms[ok], sh[ok], p0=(sh[ok][-1], 0.3),
                                sigma=1 / np.sqrt(n[ok]), maxfev=20000)
        rec = part[part["rec_" + cond]]
        w = 1.0 / (1 - np.exp(-l_ * rec["months"].values))
        out = out.add(pd.Series(w, index=rec.index).groupby(rec["county"]).sum(), fill_value=0.0)
    return out.reindex(CF.COUNTIES, fill_value=0.0)


def _ipw_days(mem, cond):
    """Days in place of months: F(d) the share of the full-year members with the condition first identified within the
    year's first d days, each identified member counted as 1 over F(their days enrolled)."""
    fy = mem[mem["full_year"] & mem["rec_" + cond]]["first_day_" + cond].values
    fy = np.sort(fy)
    rec = mem[mem["rec_" + cond]]
    cap = np.searchsorted(fy, rec["days"].values, side="right") / len(fy)
    return pd.Series(1.0 / cap, index=rec.index).groupby(rec["county"]).sum().reindex(CF.COUNTIES, fill_value=0.0)


def standards(prescribers, smi, oud, seen):
    p = pd.Series(prescribers).reindex(CF.COUNTIES)
    s1 = p / smi * 1000
    s2 = p / oud * 1000
    s3 = seen / smi
    fails = (s1 < CF.THRESH["smi"]).astype(int) + (s2 < CF.THRESH["oud"]).astype(int) + (s3 < CF.THRESH["reach"]).astype(int)
    return pd.DataFrame({"s_smi": s1, "s_oud": s2, "s_reach": s3, "fails": fails})


def designated(df):
    return tuple(sorted(df.index[df["fails"] >= 2]))


def routes(a):
    return routes_from(a["members"], {c: len(v) for c, v in a["practising"].items()}, a)


def routes_from(members, pres, a=None):
    out = {}
    for k, (smi, oud, seen) in needs_from(members, (a or {}).get("final"), (a or {}).get("spans_days")).items():
        df = standards(pres, smi, oud, seen)
        out[k] = (df, designated(df))
    return out


def margins(df):
    """Relative distance of each value from its threshold."""
    return pd.DataFrame({"m_smi": df["s_smi"] / CF.THRESH["smi"] - 1, "m_oud": df["s_oud"] / CF.THRESH["oud"] - 1,
                         "m_reach": df["s_reach"] / CF.THRESH["reach"] - 1})
