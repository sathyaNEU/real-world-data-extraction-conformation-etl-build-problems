"""task170 calculations from the shipped bundle: the golden and every rung, read from the files in a target folder
only (deliver.py, checks.py and ceiling.py call these; verify.py has its own code path)."""
from __future__ import annotations

import math
import os
import re

import numpy as np
import pandas as pd

import common as C

HALF = np.arange(12) + 0.5           # half hours after 18:00
MONTHS = {"Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}


# ---------------------------------------------------------------------------------------------------- entomology
def hour_bin(label):
    """The bin index (0 = 18:00 to 19:00) from any of the sheets' hour labels."""
    s = label.strip().lower()
    m = re.match(r"^(\d{1,2})(?::?(\d{2}))?\s*(am|pm)?", s)
    if re.match(r"^\d{4}-", s):
        h = int(s[:2])
    elif m and m.group(3):
        h = int(m.group(1)) % 12 + (12 if m.group(3) == "pm" else 0)
    else:
        h = int(m.group(1))
    return (h - 18) % 24


def hlc_table(target, dedupe=True, per_minute=True, species=("an_ruvariensis",)):
    df = pd.read_csv(os.path.join(target, "hlc_sentinel_2024_2026.csv"), dtype=str, keep_default_na=False)
    if dedupe:
        df = df.drop_duplicates()
    df = df[df["an_ruvariensis"] != ""].copy()
    df["bin"] = df["hour"].map(hour_bin)
    df["pos"] = df["position"].str[:2].str.upper().map({"IN": "IN", "OU": "OUT"})
    df["minutes"] = df["minutes_collected"].astype(int)
    df["n"] = sum(df[s].astype(int) for s in species)
    g = df.groupby(["pos", "bin"]).agg(n=("n", "sum"), minutes=("minutes", "sum"), rows=("n", "size"))
    rate = (g["n"] / (g["minutes"] if per_minute else g["rows"])).unstack(0)
    return rate["IN"].values, rate["OUT"].values, df


# ---------------------------------------------------------------------------------------------------- behaviour
def after_six(clock, morning=False):
    if morning:
        return clock + 6
    return clock - 18 if clock >= 12 else clock + 6


def parse_bare(s, morning):
    """Times as the survey sheets hold them: 21:30, 2130, 9:30 PM, or a bare 9:30 meaning the evening."""
    s = str(s).strip()
    m = re.match(r"^(\d{1,2})(:?)(\d{2})\s*([AaPp][Mm])?$", s)
    hs, colon, mi, ap = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    h = int(hs)
    if ap:
        h = h % 12 + (12 if ap.upper() == "PM" else 0)
    elif colon and not hs.startswith("0") and h <= 12 and not morning:
        h = 0 if h == 12 else (h if h <= 3 else h + 12)
    return h + mi / 60


def hbs_table(target, rounds=(1, 2), first_only=False):
    path = os.path.join(target, "human_behaviour_survey_2025.xlsx")
    frames = []
    for k, sheet in ((1, "Round 1 Apr 2025"), (2, "Round 2 Aug 2025")):
        if k not in rounds:
            continue
        d = pd.read_excel(path, sheet_name=sheet, dtype=str)
        d["round"] = k
        frames.append(d)
    df = pd.concat(frames, ignore_index=True)
    if first_only:
        df = df.drop_duplicates(["hh_no", "line_no"], keep="first")
    df["t_in"] = [after_six(parse_bare(x, False)) for x in df["went_inside"]]
    df["t_bed"] = [after_six(parse_bare(x, False)) for x in df["went_to_bed"]]
    df["t_rise"] = [after_six(parse_bare(x, True), True) for x in df["got_up"]]
    return df


def shares(df, points=HALF):
    ind = np.array([((df.t_in <= t) & (df.t_rise > t)).mean() for t in points])
    inb = np.array([((df.t_bed <= t) & (df.t_rise > t)).mean() for t in points])
    return ind, inb


def shares_integral(df):
    """Share of each hour spent indoors and in bed, averaged over people (an alternative to the half-hour read)."""
    ind, inb = np.zeros(12), np.zeros(12)
    for h in range(12):
        a, b = h, h + 1
        def frac(start, stop):
            lo = np.clip(start, a, b)
            hi = np.clip(stop, a, b)
            return np.clip(hi - lo, 0, None).mean()
        ind[h] = frac(df.t_in.values, df.t_rise.values)
        inb[h] = frac(df.t_bed.values, df.t_rise.values)
    return ind, inb


def in_bed_share(b_in, b_out, ind, inb):
    expo = b_in * ind + b_out * (1 - ind)
    return float((b_in * inb).sum() / expo.sum())


def indoor_share(b_in, b_out, ind, inb):
    expo = b_in * ind + b_out * (1 - ind)
    return float((b_in * ind).sum() / expo.sum())


def indoor_only_share(b_in, b_out, ind, inb):
    return float((b_in * inb).sum() / b_in.sum())


# ---------------------------------------------------------------------------------------------------- trial
def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as p:
        return "\n".join(pg.extract_text() or "" for pg in p.pages)


def trial_tables(target):
    txt = pdf_text(os.path.join(target, "kinga5_final_report_2024.pdf"))
    sites = ["Mabwe", "Kisiriri", "Kibondeni", "Chibowa", "Lukonde"]
    t1 = {}
    for s in sites:
        m = re.search(r"^%s ([\d,]+) ([\d,]+\.\d) ([\d,]+) ([\d,]+\.\d) " % s, txt, re.M)
        cc, pc, cn, pn = (float(x.replace(",", "")) for x in m.groups())
        t1[s] = dict(cases_c=cc, py_c=pc, cases_n=cn, py_n=pn)
    m = re.search(r"^All sites [\d,]+ [\d,.]+ [\d,]+ [\d,.]+ (\d+\.\d)", txt, re.M)
    pooled = float(m.group(1)) / 100

    def block(title, pattern_rows, conv):
        start = txt.index(title)
        seg = txt[start:]
        rows = []
        for lab in pattern_rows:
            mm = re.search(r"^%s((?: [\d.]+){5})$" % re.escape(lab), seg, re.M)
            rows.append([conv(x) for x in mm.group(1).split()])
        return np.array(rows).T  # sites x hours

    hrs = ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00", "05:00"]
    halves = ["18:30", "19:30", "20:30", "21:30", "22:30", "23:30", "00:30", "01:30", "02:30", "03:30", "04:30", "05:30"]
    b_in = block("Table 2a", hrs, float)
    b_out = block("Table 2b", hrs, float)
    ind = block("Table 3a", halves, float) / 100
    inb = block("Table 3b", halves, float) / 100
    out = []
    for i, s in enumerate(sites):
        r = dict(site=s, **t1[s], b_in=b_in[i], b_out=b_out[i], ind=ind[i], inb=inb[i])
        r["E"] = 1 - (r["cases_n"] / r["py_n"]) / (r["cases_c"] / r["py_c"])
        r["share"] = in_bed_share(r["b_in"], r["b_out"], r["ind"], r["inb"])
        r["share_I"] = indoor_share(r["b_in"], r["b_out"], r["ind"], r["inb"])
        r["share_in_only"] = indoor_only_share(r["b_in"], r["b_out"], r["ind"], r["inb"])
        out.append(r)
    return out, pooled


def q_estimates(sites, key="share"):
    E = np.array([s["E"] for s in sites])
    f = np.array([s[key] for s in sites])
    cc = np.array([s["cases_c"] for s in sites])
    cn = np.array([s["cases_n"] for s in sites])
    var = (1 - E) ** 2 * (1 / cn + 1 / cc)
    b = np.linalg.lstsq(np.column_stack([np.ones(len(f)), f]), E, rcond=None)[0]
    pooled_E = 1 - cn.sum() / np.array([s["py_n"] for s in sites]).sum() / (cc.sum() / np.array([s["py_c"] for s in sites]).sum())
    pooled_f = (f * cc).sum() / cc.sum()
    return dict(ivw_origin=float((E * f / var).sum() / (f * f / var).sum()),
                ols_origin=float((E * f).sum() / (f * f).sum()),
                mean_ratio=float(np.mean(E / f)),
                ratio_pooled=float(pooled_E / pooled_f),
                ols_intercept=(float(b[0]), float(b[1])))


# ---------------------------------------------------------------------------------------------------- plan
def baseline(target):
    df = pd.read_excel(os.path.join(target, "obf_planning_baseline_2027.xlsx"), header=2)
    df["m"] = df["month"].str[:3].map(MONTHS)
    return {(r.sub_county_code, int(r.m)): int(r.expected_cases) for r in df.itertuples()}


def usage(target):
    from docx import Document
    d = Document(os.path.join(target, "lulanet_r_distribution_plan_2027.docx"))
    out = {}
    import calendar
    names = {calendar.month_name[m]: m for m in range(1, 13)}
    for t in d.tables:
        if t.rows[0].cells[0].text.startswith("Month"):
            for r in t.rows[1:]:
                out[names[r.cells[0].text]] = int(r.cells[1].text) / 100
    return out


# ---------------------------------------------------------------------------------------------------- the call
def golden(target):
    b_in, b_out, _ = hlc_table(target)
    hbs = hbs_table(target)
    ind, inb = shares(hbs)
    phi = in_bed_share(b_in, b_out, ind, inb)
    sites, pooled = trial_tables(target)
    q = q_estimates(sites)["ivw_origin"]
    base = baseline(target)
    use = usage(target)
    by_sc = {sc: sum(base[(sc, m)] * use[m] * q * phi for (_, m) in C.WINDOW) for sc in C.SC_CODES}
    by_month = {m: sum(base[(sc, m)] * use[m] * q * phi for sc in C.SC_CODES) for (_, m) in C.WINDOW}
    total = sum(by_sc.values())
    base_total = sum(base.values())
    return dict(phi=phi, q=q, pooled=pooled, by_sc=by_sc, by_month=by_month, total=total, base_total=base_total,
                share=total / base_total, base=base, use=use, sites=sites, b_in=b_in, b_out=b_out, ind=ind, inb=inb)


def averted_with(G, eff_per_user):
    """Cases averted at a constant per-user effect on the plan's baseline and use."""
    return sum(G["base"][(sc, m)] * G["use"][m] * eff_per_user for sc in C.SC_CODES for (_, m) in C.WINDOW)


# ---------------------------------------------------------------------------------------------------- the asks
def nets_needed(target, mode="golden"):
    """Nets by sub-county under the plan's rule. mode: golden (replays dropped, mop-up re-registrations of a main-round
    household dropped), naive (every row), exact (replays only), dwelling (one household per dwelling mark), idonly
    (replays and same-ID re-registrations dropped)."""
    df = pd.read_parquet(os.path.join(target, "nets_registration_2026.parquet"))
    if mode != "naive":
        df = df.drop_duplicates()
    if mode == "golden":
        key = ["sub_county", "ward", "dwelling_mark", "usual_members", "under_five", "sleeping_spaces"]
        main = df[df["round"] == "MAIN"][key].drop_duplicates()
        mop = df[df["round"] == "MOPUP"].merge(main.assign(_m=1), on=key, how="left")
        keep_mop = mop[mop["_m"].isna()].drop(columns="_m")
        df = pd.concat([df[df["round"] == "MAIN"], keep_mop], ignore_index=True)
    elif mode == "dwelling":
        df = df.sort_values(["round", "reg_date", "reg_no"]).drop_duplicates(["sub_county", "ward", "dwelling_mark"])
    elif mode == "idonly":
        has = df[df["head_id_no"].notna()]
        main_ids = set(has[has["round"] == "MAIN"]["head_id_no"])
        df = df[~((df["round"] == "MOPUP") & df["head_id_no"].isin(main_ids))]
    nets = np.minimum(C.NET_RULE[1], np.ceil(df["usual_members"].astype(int) / C.NET_RULE[0])).astype(int)
    out = nets.groupby(df["sub_county"]).sum().to_dict()
    return {sc: int(out.get(sc, 0)) for sc in C.SC_CODES}


def reported_cases(target, mode="golden"):
    """Confirmed Ombeni fever, January to September 2026, by sub-county under the July 2026 boundaries.
    mode: golden (facility list's sub-county, the June re-entry counted once, the parents' January to March returns
    net of their outreach clinics), naive (the export's sub-county column, every row), mapped (facility list, every
    row), dedup (facility list, the June re-entry once), export_dedup (the export's column, June once)."""
    df = pd.read_csv(os.path.join(target, "khis_moh705_obf_2024_2026.csv"), dtype={"mfl_code": str, "period": str})
    fac = pd.read_csv(os.path.join(target, "facility_list_2026.csv"), dtype={"mfl_code": str, "parent_mfl_code": str})
    name_to_code = {n: c for c, n in C.SUBCOUNTIES}
    df = df[df["period"].between("202601", "202609")].copy()
    if mode in ("golden", "dedup", "export_dedup"):
        df = df.sort_values("last_updated").drop_duplicates(["period", "mfl_code", "age_group"], keep="last")
    if mode in ("naive", "export_dedup"):
        sc = df["sub_county"].map(name_to_code)
    else:
        sc = df["mfl_code"].map(dict(zip(fac["mfl_code"], fac["sub_county"]))).map(name_to_code)
    conf = df["confirmed_obf"].astype(int).copy()
    if mode == "golden":
        par = dict(zip(fac["mfl_code"], fac["parent_mfl_code"].fillna("")))
        sat = df[df["mfl_code"].map(par).fillna("") != ""]
        sat_key = {(par[r.mfl_code], r.period, r.age_group): int(r.confirmed_obf) for r in sat.itertuples()}
        inc = df["comment"].fillna("").str.startswith("incl.")
        sub = [sat_key.get((r.mfl_code, r.period, r.age_group), 0) if i else 0 for r, i in zip(df.itertuples(), inc)]
        conf = conf - np.array(sub)
    out = conf.groupby(sc.values).sum().to_dict()
    return {s: int(out.get(s, 0)) for s in C.SC_CODES}
