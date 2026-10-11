"""The golden solve: reads only ../target/ and computes every graded figure.

Run: python3 golden.py           prints the figures
     python3 golden.py --write   also writes ../golden/field_team_q1_2027.pptx and patch_screen_q1_2027.csv
The loaders and the screen are parameterised so checks.py can run every rung and grid cell on the
same shipped bytes.
"""
import datetime as dt
import json
import math
import os
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "..", "target")
GOLDEN = os.path.join(HERE, "..", "golden")

RUN_DATE = dt.date(2026, 12, 7)
ASSESS_START = RUN_DATE - dt.timedelta(weeks=8)
HIST_START = ASSESS_START - dt.timedelta(weeks=104)
WINDOW = (HIST_START, RUN_DATE - dt.timedelta(1))
HEATING_CHANGES = {"Air source heat pump", "High heat retention storage heaters"}
PATCH_ORDER = ["INV", "NRN", "FRS", "ELG", "SPY", "LOC", "CAI", "SKY"]


def tp(name):
    return os.path.join(TARGET, name)


def find(prefix):
    return next(f for f in sorted(os.listdir(TARGET)) if f.startswith(prefix))


# ---------------------------------------------------------------------------------------------
# loaders
def load_register():
    p = tp(find("supply_point_register"))
    sup = pd.read_excel(p, sheet_name="Supplies", header=4, dtype={"mpan_core": str})
    rel = pd.read_excel(p, sheet_name="Related metering points", header=3,
                        dtype={"related_mpan_core": str, "primary_mpan_core": str})
    exch = pd.read_excel(p, sheet_name="Meter exchanges", header=3, dtype={"mpan_core": str})
    acct = pd.read_excel(p, sheet_name="Account history", header=3)
    return sup, exch, acct, rel


def all_supplies():
    """Every supply number in the register: primaries, and related metering points carrying their
    primary's premises, patch and payment method."""
    sup, _, _, rel = load_register()
    base = sup[["mpan_core", "uprn", "rp_patch", "payment_method"]].copy()
    r = rel.merge(base.rename(columns={"mpan_core": "primary_mpan_core"}), on="primary_mpan_core", how="left")
    r = r.rename(columns={"related_mpan_core": "mpan_core"})[["mpan_core", "uprn", "rp_patch", "payment_method"]]
    return pd.concat([base, r], ignore_index=True)


def load_stations():
    with open(tp("patch_weather_stations.json")) as fh:
        return {d["rp_patch"]: d["station"] for d in json.load(fh)["patches"]}


def load_hdd(base=15.5):
    df = pd.read_csv(tp(find("station_degree_days")), parse_dates=["date"])
    if base == 15.5:
        df["hdd"] = df["hdd_15_5c"]
    else:
        df["hdd"] = (base - df["mean_air_temperature_c"]).clip(lower=0)
    return df


def week_starts():
    return [HIST_START + dt.timedelta(weeks=k) for k in range(112)]


def weekly_hdd(base=15.5):
    df = load_hdd(base)
    out = {}
    for st, g in df.groupby("station"):
        s = g.set_index(g["date"].dt.date)["hdd"]
        out[st] = np.array([s.loc[w:w + dt.timedelta(6)].sum() for w in week_starts()])
    return out


def supply_weekly_from_reads(alloc="linear"):
    """Weekly kWh per supply number, weeks Monday 00:00 to Monday 00:00, from cumulative reads.

    Meter exchanges are bridged with the exchange reads. A missing Monday read is filled by linear
    interpolation in days between the neighbouring reads ("linear"), or the consumption across the gap
    is booked to the week holding the later read ("later").
    """
    reads = pd.read_parquet(tp(find("smart_daily_reads")))
    _, exch, _, _ = load_register()
    ex = {r.mpan_core: r for r in exch.itertuples()}
    mondays = [HIST_START + dt.timedelta(weeks=k) for k in range(113)]
    m_ord = np.array([d.toordinal() for d in mondays])
    out = {}
    reads = reads.sort_values(["mpan_core", "read_date"])
    for mp, g in reads.groupby("mpan_core", sort=False):
        dates = np.array([d.toordinal() for d in g["read_date"]])
        vals = g["cumulative_kwh"].to_numpy(float).copy()
        if mp in ex:
            e = ex[mp]
            new = (g["meter_serial"] == e.fitted_serial).to_numpy()
            vals[new] = vals[new] - e.initial_read_kwh + e.final_read_kwh
        if alloc == "linear":
            cm = np.interp(m_ord, dates, vals)
        else:
            idx = np.searchsorted(dates, m_ord, side="left")
            idx = np.clip(idx, 0, len(dates) - 1)
            cm = vals[idx]
        out[mp] = np.diff(cm)
    return out


def load_exclusions():
    cot = pd.read_csv(tp(find("change_of_occupier")), dtype={"uprn": int})
    cot["d"] = pd.to_datetime(cot["event_date"], format="%d/%m/%Y").dt.date
    cot_u = set(cot.loc[(cot["d"] >= WINDOW[0]) & (cot["d"] <= WINDOW[1]), "uprn"])
    meas = pd.read_csv(tp(find("heating_measures")), dtype={"uprn": int})
    meas["d"] = pd.to_datetime(meas["commissioned_on"], format="%d %b %Y").dt.date
    heat_u = set(meas.loc[(meas["d"] >= WINDOW[0]) & (meas["d"] <= WINDOW[1]) &
                          meas["measure"].isin(HEATING_CHANGES), "uprn"])
    return cot_u, heat_u


def screen(series, hdd_w, threshold=0.30, every_week=True):
    """series: weekly kWh over the 112 weeks; hdd_w: matching weekly degree days. Returns (shortfall, referred)."""
    yb, xb = series[:104], hdd_w[:104]
    ya, xa = series[104:112], hdd_w[104:112]
    A = np.vstack([np.ones(104), xb]).T
    coef, *_ = np.linalg.lstsq(A, yb, rcond=None)
    exp = coef[0] + coef[1] * xa
    sf = 1 - ya.sum() / exp.sum()
    ok = sf >= threshold and (not every_week or bool((ya < exp).all()))
    return float(sf), ok


# ---------------------------------------------------------------------------------------------
def referrals(grain="supply", base=15.5, alloc="linear", use_cot=True, use_heat=True, credit_only=True,
              threshold=0.30, every_week=True, count="supply", related=True):
    sup, _, _, _ = load_register()
    allsup = all_supplies() if related else sup[["mpan_core", "uprn", "rp_patch", "payment_method"]]
    st = load_stations()
    hw = weekly_hdd(base)
    cot_u, heat_u = load_exclusions()
    excl = set()
    if use_cot:
        excl |= cot_u
    if use_heat:
        excl |= heat_u
    credit = set(sup.loc[sup["payment_method"] == "Credit", "uprn"])
    patch_of = dict(zip(sup["uprn"], sup["rp_patch"]))
    hits = {}
    if grain == "supply":
        wk = supply_weekly_from_reads(alloc)
        for r in allsup.itertuples():
            if credit_only and r.uprn not in credit:
                continue
            if r.uprn in excl:
                continue
            sf, ok = screen(wk[r.mpan_core], hw[st[r.rp_patch]], threshold, every_week)
            if ok:
                hits.setdefault(r.rp_patch, set()).add(r.mpan_core if count == "supply" else r.uprn)
    elif grain == "system":
        mart = pd.read_csv(tp(find("rp_mart_weekly_import")), parse_dates=["week_commencing"],
                           dtype={"mpan_core": str})
        mart = mart[mart["week_commencing"].dt.date >= HIST_START]
        u_of = dict(zip(sup["mpan_core"], sup["uprn"]))
        wk_idx = {w: i for i, w in enumerate(week_starts())}
        for m, g in mart.groupby("mpan_core"):
            u = u_of[m]
            if credit_only and u not in credit:
                continue
            if u in excl:
                continue
            s = np.zeros(112)
            for d, v in zip(g["week_commencing"].dt.date, g["kwh_import"]):
                s[wk_idx[d]] += v
            sf, ok = screen(s, hw[st[patch_of[u]]], threshold, every_week)
            if ok:
                hits.setdefault(patch_of[u], set()).add(m)
    elif grain == "premises":
        wk = supply_weekly_from_reads(alloc)
        tot = {}
        for r in allsup.itertuples():
            tot.setdefault(r.uprn, np.zeros(112))
            tot[r.uprn] = tot[r.uprn] + wk[r.mpan_core]
        for u, s in tot.items():
            if (credit_only and u not in credit) or u in excl:
                continue
            sf, ok = screen(s, hw[st[patch_of[u]]], threshold, every_week)
            if ok:
                hits.setdefault(patch_of[u], set()).add(u)
    return {p: len(hits.get(p, ())) for p in PATCH_ORDER}


# ---------------------------------------------------------------------------------------------
def history(dedupe=True, appeals=True, local_time=True, access_only=True):
    sup, _, _, _ = load_register()
    patch_of = dict(zip(sup["uprn"], sup["rp_patch"]))
    fl = pd.read_csv(tp(find("fieldlink_visits")), dtype={"JobNo": str})
    fo = pd.read_csv(tp(find("fieldops_visits")), dtype={"legacy_job_no": str})
    v1 = pd.DataFrame({"job": fl["JobNo"], "alt": None,
                       "date": pd.to_datetime(fl["VisitDate"], format="%d/%m/%Y").dt.date,
                       "uprn": fl["UPRN"], "out": fl["Outcome"].map({"CONF": "C", "NFF": "N", "NOACC": "X"})})
    ts = pd.to_datetime(fo["visit_start_utc"], utc=True)
    if local_time:
        d2 = ts.dt.tz_convert(ZoneInfo("Europe/London")).dt.date
    else:
        d2 = ts.dt.date
    v2 = pd.DataFrame({"job": fo["job_id"], "alt": fo["legacy_job_no"], "date": d2, "uprn": fo["uprn"],
                       "out": fo["outcome"].map({"DIV-CONFIRMED": "C", "NO-FAULT": "N", "NO-ACCESS": "X"})})
    if dedupe:
        rekeyed = set(v2["alt"].dropna())
        v1 = v1[~v1["job"].isin(rekeyed)]
    v = pd.concat([v1, v2], ignore_index=True)
    if appeals:
        ap = pd.read_excel(tp(find("tamper_appeals")), header=3)
        over = set(ap.loc[ap["decision"] == "Overturned", "job_reference"])
        hit = v["job"].isin(over) | v["alt"].isin(over)
        v.loc[hit & (v["out"] == "C"), "out"] = "N"
    winters = [(dt.date(2023, 10, 1), dt.date(2024, 3, 31)), (dt.date(2024, 10, 1), dt.date(2025, 3, 31)),
               (dt.date(2025, 10, 1), dt.date(2026, 3, 31))]
    inw = v["date"].apply(lambda d: any(a <= d <= b for a, b in winters))
    v = v[inw].copy()
    v["patch"] = v["uprn"].map(patch_of)
    res = {}
    for p in PATCH_ORDER:
        g = v[v["patch"] == p]
        acc = int((g["out"] != "X").sum()) if access_only else len(g)
        conf = int((g["out"] == "C").sum())
        res[p] = (acc, conf, round(100 * conf / acc, 1) if acc else None)
    return res


def capacity(scotland=True, honour_start=True, standby_is_field=True):
    p = tp(find("rp_field_rota"))
    team = pd.read_excel(p, sheet_name="Team", header=3)
    leave = pd.read_excel(p, sheet_name="Leave and training", header=2)
    hol = pd.read_excel(p, sheet_name="Bank holidays", header=2)
    region = "Scotland" if scotland else "England and Wales"
    hols = set(pd.to_datetime(hol.loc[hol["calendar"] == region, "date"]).dt.date)
    off_codes = {"AL", "TRN", "IND"} | (set() if standby_is_field else {"STBY"})
    lv = {(r.officer, pd.Timestamp(r.date).date()) for r in leave.itertuples() if r.code in off_codes}
    days = 0
    d = dt.date(2027, 1, 1)
    while d <= dt.date(2027, 3, 31):
        if d.weekday() < 5 and d not in hols:
            for r in team.itertuples():
                start = pd.Timestamp(r.field_start).date()
                if honour_start and d < start:
                    continue
                if (r.officer, d) not in lv:
                    days += 1
        d += dt.timedelta(1)
    from docx import Document
    doc = Document(tp(find("FW-3")))
    t = doc.tables[0]
    travel = {row.cells[1].text: int(row.cells[2].text) for row in t.rows[1:]}
    vpd = {k: math.floor(450 / (70 + m)) for k, m in travel.items()}
    return days, {k: days * vpd[k] for k in PATCH_ORDER}, vpd


def solve():
    ref = referrals()
    ranked = sorted(PATCH_ORDER, key=lambda p: -ref[p])
    hist_ = history()
    days, cap, vpd = capacity()
    return {"referrals": ref, "pick": ranked[0], "runner_up": ranked[1],
            "margin": ref[ranked[0]] - ref[ranked[1]], "history": hist_, "officer_days": days,
            "capacity": cap, "visits_per_day": vpd}


PATCH_NAMES = {"INV": "Inverness City", "NRN": "Nairn and Ardersier", "FRS": "Forres",
               "ELG": "Elgin and Lossiemouth", "SPY": "Strathspey", "LOC": "Lochaber",
               "CAI": "Caithness", "SKY": "Skye and Lochalsh"}


if __name__ == "__main__":
    s = solve()
    print(json.dumps(s, indent=1, default=str))
    if "--write" in sys.argv:
        import deliver
        deliver.write(s, GOLDEN)
