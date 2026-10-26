"""The golden analysis for task270, read from the shipped pack only: the HFC packs in service throughout 2026, each
pack's 2026 refrigerant charged less recovered from Kelbray's job sheets, each pack's own receiver response (the rise
in receiver level per kilogram charged, from the arrival and departure readings of its 2024 to 2026 charges) and full
level, the charge each pack was short on 31 December 2025 and on 31 December 2026 from Tarnley's daily mean
receiver level, and each region's 2026 loss as a share of its packs' full charge. The ladder's other routes run on
the same reads through switches."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import common as K

HFC = {"R404A", "R448A", "R449A", "R407F"}
NAMES = {"SOLSTICE N40": "R448A", "OPTEON XP40": "R449A"}


def read(target, key, **kw):
    path = os.path.join(target, K.FILES[key])
    if path.endswith(".xlsx"):
        return pd.read_excel(path, sheet_name=kw.get("sheet"), dtype=str).fillna("")
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def gas(name):
    n = name.strip().upper().replace("-", "")
    return NAMES.get(name.strip().upper(), n)


def packs(target):
    """the register's HFC packs in service on 1 January 2026 and still in service on 31 December 2026"""
    P = read(target, "register", sheet="Packs")
    S = read(target, "stores")
    P["gas"] = P["Refrigerant"].map(gas)
    P["charge"] = P["Full charge (kg)"].astype(float)
    P["since"] = pd.to_datetime(P["In service from"], format="%d/%m/%Y")
    P["until"] = pd.to_datetime(P["Decommissioned"].replace("", None), format="%d/%m/%Y")
    P["store"] = P["Pack"].str[:3].astype(int)
    keep = P["gas"].isin(HFC) & (P["since"] <= pd.Timestamp(K.YEAR, 1, 1)) & (P["until"].isna())
    P = P[keep].copy()
    code = {v: k for k, v in K.REGION_NAME.items()}
    reg = dict(zip(S["store_no"].astype(int), S["region"].map(code)))
    P["region"] = P["store"].map(reg)
    return P.set_index("Pack")[["store", "region", "gas", "charge"]]


def jobs(target):
    J = read(target, "jobs")
    J["date"] = pd.to_datetime(J["job_date"], format="%d/%m/%Y")
    J["code"] = J["store"].astype(int).map("{:03d}".format) + "/" + J["asset"]
    for c in ("charged_kg", "recovered_kg"):
        J[c] = pd.to_numeric(J[c], errors="coerce").fillna(0.0)
    for c in ("receiver_arrival_pct", "receiver_departure_pct"):
        J[c] = pd.to_numeric(J[c], errors="coerce")
    return J


def pack_jobs(target, P):
    J = jobs(target)
    J = J[J["code"].isin(P.index) & J["job_type"].isin(["ROUTINE", "BREAKDOWN"])].copy()
    J["net"] = J["charged_kg"] - J["recovered_kg"]
    return J


def calibration(J, kmode="median", fmode="median"):
    """each pack's rise in receiver level per kilogram charged and its full level, from its own job sheets"""
    c = J[(J["net"] > 0.5) & (J["receiver_arrival_pct"] > 1) & (J["receiver_departure_pct"] < 99)]
    ratio = (c["receiver_departure_pct"] - c["receiver_arrival_pct"]) / c["net"]
    if kmode == "median":
        k = ratio.groupby(c["code"]).median()
    elif kmode == "mean":
        k = ratio.groupby(c["code"]).mean()
    else:   # least squares through the origin
        num = ((c["receiver_departure_pct"] - c["receiver_arrival_pct"]) * c["net"]).groupby(c["code"]).sum()
        k = num / (c["net"] ** 2).groupby(c["code"]).sum()
    d = J[J["charged_kg"] > 0]
    full = d["receiver_departure_pct"].groupby(d["code"]).median() if fmode == "median" else \
        d["receiver_departure_pct"].groupby(d["code"]).mean()
    return k, full


def levels(target, P, days):
    L = read(target, "levels")
    T = read(target, "tags")
    tag = dict(zip(T["bureau_tag"], T["pack_code"]))
    L = L[L["date"].isin(days)].copy()
    L["code"] = L["bureau_tag"].map(tag)
    L["level"] = pd.to_numeric(L["receiver_level_pct"], errors="coerce")
    L = L[L["code"].isin(P.index) & L["level"].between(0, 100)]
    return L.pivot_table(index="code", columns="date", values="level", aggfunc="first")


def losses(target, kmode="median", fmode="median", start_day="2025-12-31", end_day="2026-12-31", ends=(True, True),
           conv="own", P=None, J=None, lev=None):
    """each pack's 2026 loss: refrigerant charged less recovered in 2026, plus the shortfall at the end of 2026 less
    the shortfall at the end of 2025; conv picks how a receiver level becomes kilograms (own: the pack's own response,
    pooled: one response for every pack, charge: the level's span read as the pack's full charge)"""
    P = packs(target) if P is None else P
    J = pack_jobs(target, P) if J is None else J
    yr = J[J["date"].dt.year == K.YEAR]
    net = yr.groupby("code")["net"].sum().reindex(P.index).fillna(0.0)
    k, full = calibration(J, kmode, fmode)
    if conv == "pooled":
        k = pd.Series(k.median(), index=k.index)
    lev = levels(target, P, [start_day, end_day]) if lev is None else lev

    def short(day):
        lv = lev[day].reindex(P.index)
        if conv == "charge":
            return ((full.reindex(P.index) - lv).clip(lower=0) / 100.0 * P["charge"])
        return ((full.reindex(P.index) - lv) / k.reindex(P.index)).clip(lower=0)
    d0, d1 = short(start_day), short(end_day)
    loss = net + (d1 if ends[1] else 0.0) - (d0 if ends[0] else 0.0)
    return pd.DataFrame({"region": P["region"], "charge": P["charge"], "net": net, "short_start": d0,
                         "short_end": d1, "loss": loss})


def regions(L):
    g = L.groupby("region")[["loss", "charge", "net"]].sum().reindex(K.REGIONS)
    return pd.DataFrame({"loss_kg": g["loss"], "charge_kg": g["charge"], "rate": 100 * g["loss"] / g["charge"],
                         "topup_rate": 100 * g["net"] / g["charge"]})


def run(target):
    P = packs(target)
    J = pack_jobs(target, P)
    L = losses(target, P=P, J=J)
    R = regions(L)
    order = R["rate"].sort_values(ascending=False)
    k, full = calibration(J)
    return dict(P=P, J=J, L=L, R=R, call=order.index[0], runner=order.index[1], k=k, full=full)


def ladder(target, P=None, J=None):
    """each route's regional rates and the region it names"""
    P = packs(target) if P is None else P
    J = pack_jobs(target, P) if J is None else J
    lev = levels(target, P, ["2025-12-31", "2026-12-31"])
    routes = {
        "R1 top-ups charged less recovered": dict(ends=(False, False)),
        "R2 shortfall at the year's end only": dict(ends=(False, True)),
        "R3 shortfall at the year's start only": dict(ends=(True, False)),
        "R4 level read as the full charge": dict(conv="charge"),
        "R5 one response for every pack": dict(conv="pooled"),
        "golden": dict(),
    }
    out = {}
    for name, kw in routes.items():
        R = regions(losses(target, P=P, J=J, lev=lev, **kw))
        out[name] = (R["rate"].idxmax(), R["rate"].round(2).to_dict())
    yr = J[J["date"].dt.year == K.YEAR]
    gross = yr.groupby("code")["charged_kg"].sum().reindex(P.index).fillna(0.0)
    g = pd.DataFrame({"region": P["region"], "gross": gross, "charge": P["charge"]}).groupby("region").sum()
    rate = 100 * g["gross"] / g["charge"]
    out["R0 top-ups charged"] = (rate.idxmax(), rate.round(2).to_dict())
    return out
