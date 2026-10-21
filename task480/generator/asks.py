"""The two supplementary asks, golden and the paths that miss them, from the shipped files (the 2024 station list
read from the generator's register, which the annual report prints; verify.py reads it off the PDF instead).

Ask A, the 2025 pilot by county: the vehicles it retired (a voucher whose vehicle is registered again at 1 July 2026
was not retired), the dismantler charges the Department paid for them (the rate card's charge for each line's tow
zone, not the amount a billing export writes) and the NOx they would have emitted in 2027 (the call's construction).
Ask B, every county: the completed initial inspections of the vehicles registered there at 1 July 2026 that were
done at a station in that county (a station number read with the licence that held it on the test date)."""
import datetime as dt
import os
from functools import lru_cache

import numpy as np
import pandas as pd

import methods as M
import pilot as P
import stations as S
import world as W


@lru_cache(maxsize=None)
def _vouchers(target):
    v = pd.read_excel(os.path.join(target, W.FILES["vouchers"]), dtype=str)
    v["county"] = v["applicant_county_no"].astype(int).map(W.NAME_OF)
    v["my"] = v["model_year"].astype(int)
    return v


@lru_cache(maxsize=None)
def _invoices(target):
    return pd.read_csv(os.path.join(target, W.FILES["invoices"]), dtype=str)


def pilot_figures(target, drop_reinstated=True, rate_card=True, construction="golden"):
    reg = M.load(target)[0]
    v = _vouchers(target)
    active = set(reg.loc[reg["record_status"] == "ACTIVE", "vin"])
    keep = ~v["vin"].isin(active) if drop_reinstated else pd.Series(True, index=v.index)
    r = v[keep].reset_index(drop=True)
    inv = _invoices(target).drop_duplicates()
    if rate_card:
        line = inv.set_index("voucher_no")["tow_zone"].astype(int).map(lambda z: P.PROCESS + P.TOW[z])
    else:
        line = inv.groupby("voucher_no")["amount"].apply(lambda s: s.astype(float).sum())
    r["charge"] = r["voucher_no"].map(line)
    body = M.load(target)[2]
    rates = M.load(target)[3]
    r["cls"] = r["body_code"].map(body)
    r["rate"] = [rates.at[m, "passenger_car_g_per_mi" if c == "PC" else "light_truck_g_per_mi"] for m, c in zip(r["my"], r["cls"])]
    m = M.match(target, r[["vin", "plate", "my"]].reset_index(drop=True))
    a0, a1 = (2027 - r["my"]).to_numpy(), (2028 - r["my"]).to_numpy()
    if construction == "golden":
        Mq = M.quad(target)
        miles = np.asarray(m["miles"] / Mq(m["age"].to_numpy()) * (Mq(a1) - Mq(a0)))
    else:
        miles = np.asarray(m["miles"] / m["age"])
    r["tons"] = miles * r["rate"].to_numpy() / W.GRAMS_PER_TON
    out = {}
    for c in W.PILOT_COUNTIES:
        s = r[r["county"] == c]
        out[c] = dict(n=int(len(s)), charges=float(s["charge"].sum()), tons=float(s["tons"].sum()),
                      unread=int(s["tons"].isna().sum()))
    return out


def station_county_on(no, d, reg=None):
    """The county of the station that held licence number no on date d."""
    reg = reg or S.register()
    for x in reg.s:
        if x["no"] == no and x["start"] <= d and (x["end"] is None or d <= x["end"]):
            return x["county"]
    return None


def station_figures(target, by_date=True):
    reg_file = M.load(target)[0]
    t = M.load(target)[1].drop_duplicates()
    t = t[(t["test_type"] == "INITIAL") & t["result"].isin(["PASS", "FAIL"])].copy()
    t = t.sort_values(["test_start", "test_id"], kind="mergesort").drop_duplicates("vin")
    act = reg_file[reg_file["record_status"] == "ACTIVE"].copy()
    act["my"] = act["model_year"].astype(int)
    act["county"] = act["county_no"].astype(int).map(W.NAME_OF)
    first = t.set_index("vin")
    vins = set(reg_file["vin"])
    orphan = t[~t["vin"].isin(vins)].copy()
    orphan["my"] = orphan["model_year"].astype(int)
    orphan = orphan.drop_duplicates(["plate", "my"]).set_index(["plate", "my"])
    sta, day = [], []
    for vin, pl, my in zip(act["vin"], act["plate"], act["my"]):
        if vin in first.index:
            row = first.loc[vin]
        elif (pl, my) in orphan.index:
            row = orphan.loc[(pl, my)]
        else:
            sta.append(None)
            day.append(None)
            continue
        sta.append(int(row["station_no"]))
        day.append(dt.date.fromisoformat(row["test_start"][:10]))
    act["station"] = sta
    act["day"] = day
    reg = S.register()
    current = {x["no"]: x["county"] for x in reg.s if x["end"] is None}
    if by_date:
        act["st_county"] = [station_county_on(s, d, reg) if s is not None else None for s, d in zip(act["station"], act["day"])]
    else:
        act["st_county"] = [current.get(s) if s is not None else None for s in act["station"]]
    out = {}
    for c in W.NAMES:
        s = act[act["county"] == c]
        out[c] = int((s["st_county"] == c).sum())
    return out
