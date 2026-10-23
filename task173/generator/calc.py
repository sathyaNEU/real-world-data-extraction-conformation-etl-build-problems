"""Every graded figure, computed from the shipped pack alone (the golden), and every rival route the design note
names, so checks.py can assert the ladder on the files a solver holds.

The golden for the call:
  bench (junior) services: each service's 2022 April to September energy, the season the district delivered
    nothing, at a normal season's reference ET (2022 energy x normal ET / 2022 ET);
  bottomland (senior) plants: each plant's normal-season energy (its 2015 to 2026 seasons each at normal ET, averaged),
    less its river lift's energy on the diversion the order removes, plus its well's energy on that water pumped from
    the well instead; the river lift and the well share one meter, so each plant's energy per acre-foot at the river
    and at the well comes from fitting its water-year energy to its own diversions and its own metered extraction.
    A plant with no well cannot make the water up and leaves it unirrigated.
"""
from __future__ import annotations

import datetime as dt
import os
import re

import numpy as np
import pandas as pd

import common as C


class Pack:
    def __init__(self, folder):
        p = lambda f: os.path.join(folder, f)
        self.folder = folder
        self.bill = pd.read_csv(p(C.F_BILL), dtype={"acct_no": str, "svc_no": str})
        self.xw = pd.read_csv(p(C.F_XW), dtype=str)
        self.reg = pd.read_excel(p(C.F_REG), sheet_name="IP services", dtype={"svc_no": str, "acct_no": str})
        self.spt = pd.read_csv(p(C.F_SPT), dtype=str)
        self.fdr = pd.read_csv(p(C.F_FDR), dtype=str)
        self.div = pd.read_csv(p(C.F_DIV), dtype={"right_no": str, "pod": str})
        self.alt = pd.read_excel(p(C.F_ALT), sheet_name="Schedule of allotments", dtype={"right_no": str})
        self.lbid_con = pd.read_excel(p(C.F_LBID), sheet_name="Contracts")
        self.lbid_alc = pd.read_excel(p(C.F_LBID), sheet_name="Allocations")
        self.eto = pd.read_csv(p(C.F_ETO), dtype={"qc": str})
        self.dpi = pd.read_csv(p(C.F_DPI), dtype={"meter_no": str})
        self.peaks = pd.read_csv(p(C.F_PEAK), dtype=str)
        gsa = pd.read_excel(p(C.F_GSA), sheet_name=None)
        frames = []
        for name, df in gsa.items():
            m = re.fullmatch(r"WY(\d{4})", name)
            if not m:
                continue
            wy = int(m.group(1))
            if "Volume (ac-ft)" in df.columns:
                df = df.rename(columns={"State Well No.": "well", "Power Account": "power", "Volume (ac-ft)": "af",
                                        "APN": "apn", "Owner of Record": "owner"})
            else:
                df = df.rename(columns={"state_well_no": "well", "power_source": "power", "extraction_af": "af"})
            df = df.assign(wy=wy)
            frames.append(df[["wy", "well", "power", "af"]])
        self.gsa = pd.concat(frames, ignore_index=True)
        self.gsa["svc_no"] = self.gsa["power"].str.extract(r"(\d{6})")[0]


# ---------------------------------------------------------------- shared building blocks
def eto_seasons(P, drop_flagged=False):
    e = P.eto.copy()
    if drop_flagged:
        e = e[e["qc"].fillna("") != "M"]
    e["d"] = pd.to_datetime(e["date"])
    e = e[e["d"].dt.month.isin(C.SEASON)]
    tot = e.groupby(e["d"].dt.year)["eto_in"].sum()
    normal = float(tot.loc[C.ET_YEARS[0]:C.ET_YEARS[-1]].mean())
    return {int(k): float(v) for k, v in tot.items()}, normal


def monthly_kwh(P, v=None):
    """kWh by service and bill month, every read line counted once (a cancel and its reversal net to nothing).

    v carries the Layer 1 mishandlings checks.py runs (R2): drop_legacy, drop_cancel_rows, dedupe_meter, drop_est."""
    v = v or {}
    b = P.bill.copy()
    if v.get("drop_cancel_rows"):
        b = b[b["bill_status"] != "CANCEL"]
    if v.get("drop_est"):
        b = b[b["read_type"] != "E"]
    if v.get("dedupe_meter"):
        b = b.drop_duplicates(["acct_no", "bill_month"], keep="first")
    leg = dict(zip(P.xw["legacy_acct_no"], P.xw["svc_no"]))
    if v.get("drop_legacy"):
        leg = {}
    b["svc"] = b["svc_no"].where(b["svc_no"].notna() & (b["svc_no"] != ""), b["acct_no"].map(leg))
    b = b[b["svc"].notna()]
    b["y"] = b["bill_month"].str[:4].astype(int)
    b["m"] = b["bill_month"].str[5:7].astype(int)
    return b.groupby(["svc", "y", "m"])["kwh"].sum()


def population(P):
    reg = P.reg
    act = reg[(reg["status"] == "ACTIVE")]
    return set(act["svc_no"])


def classes(P):
    """Bottomland plants are the services that pump a decree point of diversion; bench services are the rest."""
    d = P.div[P.div["measure"].str.startswith("VVPUD")]
    pod_svc = d.groupby("right_no")["measure"].first().str.replace("VVPUD ", "", regex=False)
    seniors = dict(zip(pod_svc.values, pod_svc.index))          # svc -> right
    return seniors


def season_kwh(mk, svc, y):
    try:
        s = mk.loc[svc]
    except KeyError:
        return 0.0
    return float(sum(s.get((y, m), 0.0) for m in C.SEASON))


def wy_kwh(mk, svc, wy):
    try:
        s = mk.loc[svc]
    except KeyError:
        return 0.0
    months = [(wy - 1, 10), (wy - 1, 11), (wy - 1, 12)] + [(wy, m) for m in range(1, 10)]
    return float(sum(s.get(k, 0.0) for k in months))


# ---------------------------------------------------------------- the call
def golden(P, variant=None):
    """variant selects one construction of the golden family (asserted to agree) or a rival route by name."""
    v = variant or {}
    et, etn = eto_seasons(P, drop_flagged=v.get("drop_flagged", False))
    if v.get("normal_years") == "2015-2026":
        etn = float(np.mean([et[y] for y in C.YEARS]))
    mk = monthly_kwh(P, v)
    pop = population(P)
    sen = classes(P)
    juniors = sorted(s for s in pop if s not in sen)
    seniors = sorted(s for s in pop if s in sen)

    # bench services
    jroute = v.get("junior", "2022")
    if jroute == "2022":
        J = sum(season_kwh(mk, s, 2022) for s in juniors) * etn / et[2022]
    elif jroute == "regression":
        # per service: season kWh = k (need x ET/ETn - alloc x contract); fitted across the 12 seasons
        con = P.lbid_con
        apn_con = {}
        for _, r in con.iterrows():
            for a in str(r["apn"]).split("; "):
                apn_con[a] = float(r["contract_af"])
        reg = P.reg.set_index("svc_no")
        alloc = dict(zip(P.lbid_alc["season"].astype(int), P.lbid_alc["allocation_pct"].astype(float) / 100))
        J = 0.0
        for s in juniors:
            a0 = str(reg.loc[s, "apn"]).split("; ")[0]
            cont = apn_con.get(a0, 0.0)
            ys = np.array(C.YEARS)
            y_ = np.array([season_kwh(mk, s, y) for y in ys])
            X = np.c_[np.array([et[y] / etn for y in ys]), -np.array([alloc[y] * cont for y in ys])]
            co, *_ = np.linalg.lstsq(X, y_, rcond=None)
            # co = [k*need, k]; the 2027 season delivers nothing
            J += co[0]
    elif jroute == "2026":
        con = P.lbid_con
        apn_con = {}
        for _, r in con.iterrows():
            for a in str(r["apn"]).split("; "):
                apn_con[a] = float(r["contract_af"])
        reg = P.reg.set_index("svc_no")
        J = 0.0
        for s in juniors:
            a0 = str(reg.loc[s, "apn"]).split("; ")[0]
            cont = apn_con.get(a0, 0.0)
            k22 = season_kwh(mk, s, 2022) / et[2022]
            # 2026 delivered 5 per cent of contract: add that water back at the service's own energy per acre-foot,
            # read from its 2022 and 2026 seasons (same need per unit ET, different delivery)
            e26 = season_kwh(mk, s, 2026)
            kaf = (k22 * et[2026] - e26) / (0.05 * cont) if cont > 0 else 0.0
            J += (e26 + 0.05 * cont * kaf) * etn / et[2026]
    else:
        raise ValueError(jroute)

    # bottomland plants
    alt = P.alt.set_index("right_no")
    div = P.div[P.div["right_no"].isin(set(sen.values()))]
    dseas = div.groupby(["right_no", "year"])["af_diverted"].sum()
    gsa = P.gsa.groupby(["svc_no", "wy"])["af"].sum()
    wells = set(P.gsa["svc_no"].dropna())
    Sn = 0.0
    add_w = 0.0
    save_r = 0.0
    detail = []
    kj_mean = None
    for s in seniors:
        right = sen[s]
        Fa = float(alt.loc[right, "season_allotment_af"])
        ys = [y for y in C.YEARS if season_kwh(mk, s, y) > 0] if v.get("drop_legacy") else C.YEARS
        if v.get("raw_mean"):
            en = np.mean([season_kwh(mk, s, y) for y in ys]) * etn / np.mean([et[y] for y in ys])
            dn = float(np.mean([dseas.loc[(right, y)] for y in C.YEARS])) * etn / np.mean([et[y] for y in C.YEARS])
        else:
            en = np.mean([season_kwh(mk, s, y) * etn / et[y] for y in ys])
            dn = float(np.mean([dseas.loc[(right, y)] * etn / et[y] for y in C.YEARS]))
        lim = C.SENIOR_LIMIT_2027 * Fa
        if v.get("cut") == "face":
            cut = (1 - C.SENIOR_LIMIT_2027) * Fa
        elif v.get("cut") == "share_of_use":
            cut = (1 - C.SENIOR_LIMIT_2027) * dn
        else:
            cut = max(dn - lim, 0.0)
        has_well = s in wells
        wys = [wy for wy in C.WY_GSA if (s, wy) in gsa.index] if has_well else []
        if v.get("gsa_missing_zero") and has_well:
            wys = list(C.WY_GSA)
        if v.get("drop_legacy"):
            wys = [wy for wy in wys if wy >= 2021]
        if has_well:
            Y = np.array([wy_kwh(mk, s, wy) for wy in wys])
            X = np.c_[np.array([dseas.loc[(right, wy)] for wy in wys]), np.array([gsa.get((s, wy), 0.0) for wy in wys])]
            if v.get("fit") == "intercept":
                X = np.c_[X, np.ones(len(wys))]
            co, *_ = np.linalg.lstsq(X, Y, rcond=None)
            kr, kw = float(co[0]), float(co[1])
        else:
            D = np.array([dseas.loc[(right, y)] for y in C.YEARS])
            Y = np.array([season_kwh(mk, s, y) for y in C.YEARS])
            kr, kw = float(Y.sum() / D.sum()), 0.0
        Sn += en
        detail.append((s, right, Fa, dn, cut, has_well, kr, kw, en))
    det = pd.DataFrame(detail, columns=["svc", "right", "allot", "dn", "cut", "well", "kr", "kw", "en"])
    if v.get("kappa") == "pooled":
        sub = [s for s in seniors if s in wells]
        rows = []
        for s in sub:
            right = sen[s]
            for wy in C.WY_GSA:
                if (s, wy) in gsa.index:
                    rows.append((wy_kwh(mk, s, wy), dseas.loc[(right, wy)], gsa.loc[(s, wy)]))
        A = np.array(rows)
        co, *_ = np.linalg.lstsq(A[:, 1:], A[:, 0], rcond=None)
        det.loc[det["well"], "kr"] = co[0]
        det.loc[det["well"], "kw"] = co[1]
    rule = v.get("seniors", "golden")
    if rule == "golden":
        add = float((det["cut"] * det["kw"] * det["well"]).sum() - (det["cut"] * det["kr"]).sum())
    elif rule == "no_river":
        add = float((det["cut"] * det["kw"] * det["well"]).sum())
    elif rule == "own_history":
        add = 0.0
    elif rule == "blended":
        bl = []
        for _, r in det.iterrows():
            s, right = r["svc"], r["right"]
            ys = [wy for wy in C.WY_GSA]
            kw_tot = sum(wy_kwh(mk, s, wy) for wy in ys)
            af = sum(dseas.loc[(right, wy)] for wy in ys) + sum(gsa.get((s, wy), 0.0) for wy in ys)
            bl.append(kw_tot / af)
        add = float((det["cut"] * np.array(bl)).sum())
    elif rule == "analog":
        add = analog_beta(P, mk, et) * float(det["cut"].sum())
    elif rule == "junior_kappa":
        add = float((det["cut"] * det["well"]).sum() * junior_kappa(P, mk, juniors) - (det["cut"] * det["kr"]).sum())
    elif rule == "well_ratio":
        # each plant's water-year energy over its metered well extraction, read as the well's energy per acre-foot
        kws = []
        for _, r in det.iterrows():
            s = r["svc"]
            wys = [wy for wy in C.WY_GSA if (s, wy) in gsa.index]
            kws.append(sum(wy_kwh(mk, s, wy) for wy in wys) / sum(gsa.loc[(s, wy)] for wy in wys) if wys else 0.0)
        add = float((det["cut"] * np.array(kws) * det["well"]).sum())
    elif rule == "two_step":
        # river energy per acre-foot from the plants with no well, then each well's from what is left of its meter
        ro = det[~det["well"]]
        kr0 = float(ro["kr"].mean())
        kws = []
        for _, r in det.iterrows():
            s, right = r["svc"], r["right"]
            wys = [wy for wy in C.WY_GSA if (s, wy) in gsa.index]
            if not wys:
                kws.append(0.0)
                continue
            e = sum(wy_kwh(mk, s, wy) for wy in wys)
            dd = sum(dseas.loc[(right, wy)] for wy in wys)
            ww = sum(gsa.loc[(s, wy)] for wy in wys)
            kws.append((e - kr0 * dd) / ww)
        add = float((det["cut"] * np.array(kws) * det["well"]).sum() - det["cut"].sum() * kr0)
    elif rule == "all_seniors_pump":
        kw_mean = float(det.loc[det["well"], "kw"].mean())
        add = float((det["cut"] * np.where(det["well"], det["kw"], kw_mean)).sum() - (det["cut"] * det["kr"]).sum())
    else:
        raise ValueError(rule)
    total = J + Sn + add
    return {"total_kwh": total, "juniors_kwh": J, "seniors_normal_kwh": Sn, "seniors_add_kwh": add,
            "seniors_kwh": Sn + add, "detail": det, "etn": etn, "et": et, "n_juniors": len(juniors),
            "n_seniors": len(seniors), "n_wells": int(det["well"].sum())}


def analog_beta(P, mk, et):
    """The bench services' energy per acre-foot the district did not deliver, fitted on the 12 seasons with ET."""
    alloc = dict(zip(P.lbid_alc["season"].astype(int), P.lbid_alc["allocation_pct"].astype(float) / 100))
    contract = float(P.lbid_con["contract_af"].sum())
    pop = population(P)
    sen = classes(P)
    juniors = [s for s in pop if s not in sen]
    Y = np.array([sum(season_kwh(mk, s, y) for s in juniors) for y in C.YEARS])
    X = np.c_[np.ones(len(C.YEARS)), np.array([(1 - alloc[y]) * contract for y in C.YEARS]),
              np.array([et[y] for y in C.YEARS])]
    co, *_ = np.linalg.lstsq(X, Y, rcond=None)
    return float(co[1])


def junior_kappa(P, mk, juniors):
    gsa = P.gsa.groupby(["svc_no", "wy"])["af"].sum()
    ks = []
    for s in juniors:
        wys = [wy for wy in C.WY_GSA if (s, wy) in gsa.index]
        if not wys:
            continue
        ks.append(sum(wy_kwh(mk, s, wy) for wy in wys) / sum(gsa.loc[(s, wy)] for wy in wys))
    return float(np.mean(ks))


# ---------------------------------------------------------------- the asks
def dp_meter_local(P, meters=None, shift_hours=1):
    d = P.dpi.copy()
    if meters is not None:
        d = d[d["meter_no"].isin(meters)]
    t = pd.to_datetime(d["interval_end"])
    # meter clock is Pacific standard time; billing months and hours are prevailing time
    if shift_hours:
        dst = (t >= pd.Timestamp("2026-03-08 02:00")) & (t < pd.Timestamp("2026-11-01 01:00"))
        t = t + pd.to_timedelta(np.where(dst, shift_hours, 0), unit="h")
    d = d.assign(t=t)
    return d


REVENUE = ["81-2207", "81-3318", "81-1940", "81-1977", "81-4062"]
CHECKS = ["81-2251", "81-3362", "81-1988", "81-4107"]


def ask_a(P, meters=REVENUE, shift_hours=1):
    """Energy Halvern metered at each delivery point in each billing month April to September 2026, MWh."""
    d = dp_meter_local(P, meters, shift_hours)
    # an interval belongs to the month its end falls in, the interval ending at 00:00 on the 1st to the month before
    tm = d["t"] - pd.Timedelta(minutes=1)
    d = d.assign(month=tm.dt.month, year=tm.dt.year)
    d = d[(d["year"] == 2026) & d["month"].isin(C.SEASON)]
    g = d.groupby(["dp_code", "month"])["kwh"].sum() / 1000.0
    return {(dp, m): float(g.loc[(C.DP_CODES[dp], m)]) for dp in C.DPS for m in C.SEASON}


def ask_c(P, meters=REVENUE, shift_hours=1):
    """Each delivery point's demand in Halvern's monthly system peak hour, April to September 2026, kW."""
    d = dp_meter_local(P, meters, shift_hours)
    out = {}
    pk = P.peaks
    for _, r in pk.iterrows():
        m = int(r["month"][5:7])
        if m not in C.SEASON:
            continue
        he = int(r["hour_ending"][:2])
        end = pd.Timestamp(r["peak_date"]) + pd.Timedelta(hours=he)
        start = end - pd.Timedelta(hours=1)
        sel = d[(d["t"] > start) & (d["t"] <= end)]
        g = sel.groupby("dp_code")["kwh"].sum()
        for dp in C.DPS:
            out[(dp, m)] = float(g.get(C.DP_CODES[dp], 0.0))
    return out


def ask_b(P, use_gis_label=False):
    """For each delivery point, the IP services it supplied through the 2026 season and their April to September
    2026 billed energy (MWh)."""
    mk = monthly_kwh(P)
    pop = population(P)
    spt = P.spt.set_index("svc_no")
    f = P.fdr.copy()
    code_dp = {v: k for k, v in C.DP_CODES.items()}
    out_n = {dp: 0 for dp in C.DPS}
    out_e = {dp: 0.0 for dp in C.DPS}
    for s in pop:
        feeder = spt.loc[s, "feeder"]
        if use_gis_label:
            dp = spt.loc[s, "substation"]
        else:
            rows = f[f["feeder"] == feeder]
            cur = rows[(rows["effective_from"] <= "2026-04-01") &
                       ((rows["effective_to"].isna()) | (rows["effective_to"] >= "2026-09-30"))]
            dp = code_dp[cur["source_dp"].iloc[0]]
        out_n[dp] += 1
        out_e[dp] += season_kwh(mk, s, 2026) / 1000.0
    return out_n, out_e
