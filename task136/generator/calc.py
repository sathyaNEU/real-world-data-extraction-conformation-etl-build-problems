"""The analysis, computed forward from the shipped files only (pandas). Used by deliver.py, checks.py and the build;
verify.py recomputes the same figures on its own code path without pandas."""
from __future__ import annotations

import datetime as dt
import os
import re

import numpy as np
import pandas as pd
import openpyxl

import common as K

CONNECTED = ("Connected", "Removed")


def D(s):
    return pd.to_datetime(s, format="%Y-%m-%d", errors="coerce")


def load(target, partial=False):
    p = lambda f: os.path.join(target, f)
    reg = pd.read_csv(p(K.REGISTER), dtype=str, keep_default_na=False)
    leg = pd.read_csv(p(K.LEGACY), dtype=str, keep_default_na=False)
    net = pd.read_csv(p(K.NETWORK), dtype=str, keep_default_na=False)
    xref = pd.read_csv(p(K.XREF), dtype=str, keep_default_na=False)
    rates = pd.read_csv(p(K.RATES), dtype=str, keep_default_na=False)
    der = pd.read_csv(p(K.DER), dtype=str, keep_default_na=False)
    realloc = pd.read_csv(p(K.REALLOC), dtype=str, keep_default_na=False)
    for c in ("received_date", "approved_date", "status_date", "connection_date", "removal_date"):
        reg[c] = D(reg[c])
    leg_kw = {r.legacy_application_no: float(r.inverter_kw_ac_each) * int(r.inverter_count) for r in leg.itertuples()}
    kw = []
    for r in reg.itertuples():
        if r.inverter_kw_ac:
            kw.append(float(r.inverter_kw_ac))
        elif r.legacy_application_no:
            kw.append(leg_kw[r.legacy_application_no])
        else:
            kw.append(np.nan)
    reg["kw"] = kw
    feeder = dict(zip(net.nmi, net.feeder))
    reg["feeder"] = reg.nmi.map(feeder)
    log = program_log(p(K.PROGRAM_LOG))
    hca = {} if partial else hosting_capacity(target)
    return dict(reg=reg, leg=leg, net=net, xref=xref, rates=rates, der=der, realloc=realloc, feeder=feeder, log=log,
                hca=hca, letter=letter_counts(target))


def program_log(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Campaigns"]
    rows, head = [], None
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == "Year":
            head = list(row)
            continue
        if head and row and isinstance(row[0], (int, float)) and row[1]:
            rows.append(dict(zip(head, row)))
    return rows


def hosting_capacity(target):
    """The hosting capacity table from the assessment PDF (feeder, 2029 case, MW)."""
    from pypdf import PdfReader
    text = "\n".join(pg.extract_text() for pg in PdfReader(os.path.join(target, K.HCA)).pages)
    out = {}
    for m in re.finditer(r"(YRB2\d)\s+[\d.]+\s+[\d,]+\s+[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)", text):
        out[m.group(1)] = dict(hc26=float(m.group(2)), hc29=float(m.group(3)))
    return out


def letter_counts(target):
    from pypdf import PdfReader
    text = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, K.LETTER)).pages)
    text = re.sub(r"\s+", " ", text)
    out = {}
    for suburb in ("Bindarra Waters", "Wattleview"):
        m = re.search(suburb + r"[^.]*?([\d,]+) (?:residential )?addresses", text)
        out[suburb] = int(m.group(1).replace(",", ""))
    return out


# ------------------------------------------------------------------------------------------------------------------
# connected capacity and the base forecast (NPP-114 2.2, 3.1, 3.2)

def connected_kw(reg, date, by="feeder"):
    d = pd.Timestamp(date)
    live = reg[reg.status.isin(CONNECTED) & (reg.connection_date <= d) &
               (reg.removal_date.isna() | (reg.removal_date > d))]
    last = live.sort_values(["nmi", "connection_date", "application_type"]).groupby("nmi").tail(1)
    return last.groupby(by).kw.sum()


def program_kw(reg, start, end):
    d0, d1 = pd.Timestamp(start), pd.Timestamp(end)
    pr = reg[(reg.program_ref != "") & (reg.application_type == "New") & reg.status.isin(CONNECTED) &
             (reg.connection_date >= d0) & (reg.connection_date <= d1)]
    return pr.groupby("feeder").kw.sum()


def trend(reg, fys=K.TREND_FYS, exclude_program=True):
    out = {f: [] for f in K.FEEDERS}
    for s, e in fys:
        c1 = connected_kw(reg, e)
        c0 = connected_kw(reg, s - dt.timedelta(days=1))
        pk = program_kw(reg, s, e)
        for f in K.FEEDERS:
            inc = c1.get(f, 0.0) - c0.get(f, 0.0)
            if exclude_program:
                inc -= pk.get(f, 0.0)
            out[f].append(inc)
    return {f: float(np.mean(v)) for f, v in out.items()}, out


def avg_new_kw(reg, fy=K.LAST_FY):
    d0, d1 = pd.Timestamp(fy[0]), pd.Timestamp(fy[1])
    new = reg[(reg.application_type == "New") & reg.status.isin(CONNECTED) & (reg.connection_date >= d0) &
              (reg.connection_date <= d1)]
    return new.groupby("feeder").kw.mean()


def base_forecast(reg):
    cap = connected_kw(reg, K.BASE)
    tr, per_fy = trend(reg)
    base = {f: cap.get(f, 0.0) + K.YEARS_TO_DESIGN * tr[f] for f in K.FEEDERS}
    return dict(cap=cap, trend=tr, per_fy=per_fy, base=base)


# ------------------------------------------------------------------------------------------------------------------
# the campaigns

def houses(rates, xref, suburb=None, oo_only=True):
    r = rates[(rates.land_use_code == "02")]
    if oo_only:
        r = r[r.rating_category == "R1"]
    if suburb:
        r = r[r.locality.str.upper() == suburb.upper()]
    nm = xref[xref.property_no.isin(r.property_no)]
    return r, nm


def first_app(reg, by="received_date"):
    """Each NMI's first successful (not withdrawn) application, by its received (or connection) date."""
    ok = reg[reg.status != "Withdrawn"]
    return ok.groupby("nmi")[by].min()


def tapped_props(xref, first, date):
    d = pd.Timestamp(date)
    t = first[first < d]
    return set(xref[xref.nmi.isin(t.index)].property_no)


def untapped(rates, xref, first, suburb, date):
    r, nm = houses(rates, xref, suburb)
    tp = tapped_props(nm, first, date)
    return r[~r.property_no.isin(tp)]


def uptake(first, nmis, start, end):
    """First applications (not withdrawn) received in [start, end) at the given NMIs."""
    f = first[first.index.isin(nmis)]
    return int(((f >= pd.Timestamp(start)) & (f < pd.Timestamp(end))).sum())


def key_feeder(suburb):
    return [l["feeder"] for l in K.LOCALITIES if l["name"] == suburb][0]


def suburb_stats(L, name, opening, first=None, first_conn=None):
    """Everything a transfer basis can be built on, for one suburb at one sign-up opening."""
    reg, rates, xref, net = L["reg"], L["rates"], L["xref"], L["net"]
    first = first if first is not None else first_app(reg)
    first_conn = first_conn if first_conn is not None else first_app(reg, "connection_date")
    op = pd.Timestamp(opening)
    oo_r, oo_n = houses(rates, xref, name)
    oo_nmis = set(oo_n.nmi)
    res_net = net[net.tariff_class == "Residential"]
    nmis = res_net[res_net.locality.str.upper() == name.upper()].nmi
    out = dict(suburb=name, feeder=key_feeder(name), opening=opening, oo=len(oo_r), res_nmis=int(len(nmis)))
    out["untapped"] = len(untapped(rates, xref, first, name, opening))
    for w in (365, 730, 1095):
        out["n%d" % w] = uptake(first, oo_nmis, op - pd.Timedelta(days=w), op)
        out["u%d" % w] = len(untapped(rates, xref, first, name, op - pd.Timedelta(days=w)))
    out["n182"] = uptake(first, oo_nmis, op - pd.Timedelta(days=182), op)
    out["n365_conn"] = uptake(first_conn, oo_nmis, op - pd.Timedelta(days=365), op)
    out["n365_all"] = uptake(first, set(nmis), op - pd.Timedelta(days=365), op)
    # person-time at risk in the year before: each untapped house's days until its first application or the opening
    f = first[first.index.isin(oo_nmis)]
    t0 = op - pd.Timedelta(days=365)
    xr = oo_n.assign(first=oo_n.nmi.map(f))
    pf = xr.groupby("property_no")["first"].min().reindex(oo_r.property_no)
    at_risk = pf.isna() | (pf >= t0)
    days = np.where(pf.isna() | (pf >= op), 365.0, (pf - t0).dt.days.astype(float))
    out["pt365"] = float(days[at_risk.values].sum() / 365.0)
    out["udw"] = int((~nmis.isin(set(first[first < op].index))).sum())
    all_oo, all_n = houses(rates, xref, None)
    all_n = all_n.assign(feeder=all_n.nmi.map(L["feeder"]))
    f_props = set(all_n[all_n.feeder == out["feeder"]].property_no)
    out["feeder_unt"] = len(f_props - tapped_props(all_n, first, opening))
    return out


def campaigns(L):
    reg = L["reg"]
    first, first_conn = first_app(reg), first_app(reg, "connection_date")
    out = []
    for row in L["log"]:
        name = row["Suburb"]
        key = [c for c in K.CAMPAIGNS if c["suburb"] == name][0]
        opening = row["Sign-ups opened"]
        opening = opening.date() if hasattr(opening, "date") else opening
        st = suburb_stats(L, name, opening, first, first_conn)
        ref = "SS-%s-%s" % (key["key"][-2:], key["key"][:3])
        sysn = reg[(reg.program_ref == ref) & (reg.application_type == "New") & reg.status.isin(CONNECTED)]
        st.update(key=key["key"], letterboxed=int(row["Homes letterboxed"]), systems_log=int(row["Systems installed"]),
                  systems=len(sysn), kw_program=float(sysn.kw.sum()))
        out.append(st)
    return out


def pools_2026(L):
    reg = L["reg"]
    first, first_conn = first_app(reg), first_app(reg, "connection_date")
    out = {}
    for c in K.CAMPAIGNS_2026:
        st = suburb_stats(L, c["suburb"], c["open"], first, first_conn)
        st.update(key=c["key"], letterboxed=L["letter"][c["suburb"]])
        out[c["suburb"]] = st
    return out


BASES = ["count", "letterboxed", "oo", "udw", "feeder_unt", "untapped", "uplift"]
BASIS_NAME = {"count": "an average campaign", "letterboxed": "per home letterboxed", "oo": "per owner-occupied house",
              "udw": "per address without PV", "feeder_unt": "per untapped owner-occupied house on the feeder",
              "untapped": "per owner-occupied house without PV in the suburb",
              "uplift": "per first application from the suburb's owner-occupied houses in the year before"}


def denominator(c, basis, variant="n365"):
    if basis == "uplift":
        if variant == "n365":
            return c["n365"]
        if variant == "n730":
            return c["n730"] / 2.0
        if variant == "n1095":
            return c["n1095"] / 3.0
        if variant == "n182":            # the six months before, at a yearly rate
            return c["n182"] * 365.0 / 182.0
        if variant == "conn":
            return c["n365_conn"]
        if variant == "all":
            return c["n365_all"]
        if variant == "rate":            # hazard on the pool a year before, times the pool at the opening
            return c["n365"] / c["u365"] * c["untapped"]
        if variant == "persontime":      # hazard on house-years at risk, times the pool at the opening
            return c["n365"] / c["pt365"] * c["untapped"]
        raise KeyError(variant)
    return c[basis]


def rate_of(camps, basis, estimator="pooled", variant="n365"):
    s = np.array([c["systems"] for c in camps], float)
    if basis == "count":
        return dict(slope=float(s.mean()), icpt=0.0, values=s, cv=float(s.std(ddof=1) / s.mean()))
    d = np.array([denominator(c, basis, variant) for c in camps], float)
    v = s / d
    if estimator == "pooled":
        slope, icpt = float(s.sum() / d.sum()), 0.0
    elif estimator == "mean":
        slope, icpt = float(v.mean()), 0.0
    elif estimator == "median":
        slope, icpt = float(np.median(v)), 0.0
    elif estimator == "origin":
        slope, icpt = float((s * d).sum() / (d * d).sum()), 0.0
    elif estimator == "ols":
        slope, icpt = (float(x) for x in np.polyfit(d, s, 1))
    else:
        raise KeyError(estimator)
    return dict(slope=slope, icpt=icpt, values=v, cv=float(v.std(ddof=1) / v.mean()))


def lifts(camps, pools, basis, estimator="pooled", variant="n365"):
    """Systems each 2026 campaign adds under a transfer basis."""
    rr = rate_of(camps, basis, estimator, variant)
    out = {}
    for name, p in pools.items():
        if basis == "count":
            out[name] = rr["slope"]
        else:
            out[name] = rr["slope"] * denominator(p, basis, variant) + rr["icpt"]
    return out


def forecast(L, basis="uplift", estimator="pooled", variant="n365", hc_case="hc29", base=None, camps=None,
             pools=None, lift=None):
    base = base or base_forecast(L["reg"])
    camps = camps or campaigns(L)
    pools = pools or pools_2026(L)
    avgkw = avg_new_kw(L["reg"])
    if lift is None:
        lift = lifts(camps, pools, basis, estimator, variant) if basis != "none" else {k: 0.0 for k in pools}
    fc = dict(base["base"])
    add = {}
    for name, n in lift.items():
        f = pools[name]["feeder"]
        add[f] = n * avgkw[f]
        fc[f] += add[f]
    excess = {f: (fc[f] / 1000.0 - L["hca"][f][hc_case]) for f in K.FEEDERS}
    order = sorted(K.FEEDERS, key=lambda f: -excess[f])
    return dict(fc=fc, excess=excess, order=order, winner=order[0], runner=order[1],
                gap=excess[order[0]] - excess[order[1]], lift=lift, add_kw=add, avgkw=avgkw, base=base,
                add_mw={name: lift[name] * avgkw[pools[name]["feeder"]] / 1000.0 for name in lift})


# ------------------------------------------------------------------------------------------------------------------
# the asks

def norm_nmi(s):
    s = s.strip()
    return s[:10] if len(s) == 11 else s


def live_nmis(reg, date=K.BASE):
    d = pd.Timestamp(date)
    live = reg[reg.status.isin(CONNECTED) & (reg.connection_date <= d) & (reg.removal_date.isna() | (reg.removal_date > d))]
    return set(live.nmi)


def der_keys(L, mode="golden"):
    """The DER extract with each row's site key: golden reads the NMI at ten characters and an NMI the re-allocation
    log replaced at its replacement; norm only the first; raw neither."""
    der, realloc = L["der"], L["realloc"]
    mp = dict(zip(realloc.old_nmi, realloc.new_nmi))
    if mode == "raw":
        key = der.nmi
    elif mode == "norm":
        key = der.nmi.map(norm_nmi)
    else:
        key = der.nmi.map(norm_nmi).map(lambda x: mp.get(x, x))
    return der.assign(key=key.values, reg=pd.to_datetime(der.registered_date))


def active_rows(L, key_mode="golden", how="network"):
    """The active connections' device rows, each with the feeder its site is counted on: network, the feeder the
    network model says supplies the site (a site no feeder supplies drops out); stamp, the extract's own feeder
    column on the row."""
    der = der_keys(L, key_mode)
    act = der[der.ac_connection_status == "Active"]
    fd = act.feeder if how == "stamp" else act.key.map(L["feeder"])
    return act.assign(fd=fd.values).dropna(subset=["fd"])


def ask_d(L, mode="golden"):
    """Per feeder: the active DER Register sites it supplies (a site is the premises' NMI with at least one active AC
    connection). stamp: placed by the extract's feeder column; connections: active AC connections counted; no_map: NMIs
    read at ten characters only; raw: NMIs as lodged and the extract's feeder."""
    key_mode = {"raw": "raw", "no_map": "norm"}.get(mode, "golden")
    act = active_rows(L, key_mode, "stamp" if mode in ("stamp", "raw") else "network")
    if mode == "connections":
        c = act.groupby("fd").ac_connection_id.nunique()
    else:
        c = act.groupby("fd").key.nunique()
    return {f: int(c.get(f, 0)) for f in K.FEEDERS}


def ask_a(L, mode="golden"):
    """Per feeder: how many of the active DER Register sites it supplies were first lodged in FY2025-26.

    golden: a site's first lodgement is the earliest registration of any of its AC connections, decommissioned ones
    included. active_first: only the active connections' registrations. no_map: NMIs read at ten characters but not
    through the re-allocation log. stamp: the extract's feeder column. raw: NMIs as lodged and the extract's feeder."""
    key_mode = {"raw": "raw", "no_map": "norm"}.get(mode, "golden")
    der = der_keys(L, key_mode)
    act = active_rows(L, key_mode, "stamp" if mode in ("stamp", "raw") else "network")
    first = (act if mode == "active_first" else der).groupby("key").reg.min()
    site_fd = act.groupby("key").fd.first()
    f0 = first.reindex(site_fd.index)
    new = site_fd[(f0 >= pd.Timestamp(K.LAST_FY[0])) & (f0 <= pd.Timestamp(K.LAST_FY[1]))]
    c = new.value_counts()
    return {f: int(c.get(f, 0)) for f in K.FEEDERS}


SYSTEM_LODGED = {"SBR HV battery"}       # products whose devices each carry the system's total


def connection_storage(bat, how="golden"):
    """kWh per active battery AC connection. golden: a modular product's module rows summed, except a product whose
    devices each carry the system's total, which counts once; once: one row per connection; rows: every row."""
    g = bat.groupby("ac_connection_id")
    first = g.kwh.first()
    total = g.kwh.sum()
    model = g.model.first()
    if how == "once":
        return first
    if how == "rows":
        return total
    return pd.Series(np.where(model.isin(SYSTEM_LODGED), first, total), index=first.index)


def ask_b(L, mode="golden"):
    """Per feeder: the battery storage at the active DER Register sites it supplies (kWh)."""
    act = active_rows(L, "norm" if mode == "no_map" else "golden", "stamp" if mode == "stamp" else "network")
    bat = act[act.device_type == "Battery"].assign(kwh=lambda d: d.storage_capacity_kwh.astype(float))
    st = connection_storage(bat, {"once": "once", "rows": "rows"}.get(mode, "golden"))
    fd = bat.groupby("ac_connection_id").fd.first()
    s = st.groupby(fd).sum()
    return {f: float(s.get(f, 0.0)) for f in K.FEEDERS}


def nameplate(model):
    m = re.search(r"(\d+\.\d)$", str(model))
    return float(m.group(1)) if m else None


def connection_inverter_kw(inv, how="golden"):
    """kW per active AC connection's inverters. golden: each inverter's rating summed, except where an inverter row
    carries the whole connection (its rating is the inverter's nameplate times the inverter rows), which counts
    once; once: one row per connection; rows: every row summed; dedupe: identical rows dropped, then summed."""
    if how == "dedupe":
        inv = inv.drop_duplicates()
    g = inv.groupby("ac_connection_id")
    first, total, n = g.kw.first(), g.kw.sum(), g.kw.size()
    plate = g.model.first().map(nameplate)
    if how == "once":
        return first
    if how in ("rows", "dedupe"):
        return total
    whole = (n > 1) & plate.notna() & ((first - plate * n).abs() < 0.011)
    return pd.Series(np.where(whole, first, total), index=first.index)


def ask_c(L, mode="golden"):
    """Per feeder: the inverter capacity at the active DER Register sites it supplies (kW)."""
    act = active_rows(L, "norm" if mode == "no_map" else "golden", "stamp" if mode == "stamp" else "network")
    inv = act[act.device_type == "Inverter"].assign(kw=lambda d: d.rated_power_kw.astype(float))
    kw = connection_inverter_kw(inv, {"once": "once", "rows": "rows", "dedupe": "dedupe"}.get(mode, "golden"))
    fd = inv.groupby("ac_connection_id").fd.first()
    s = kw.groupby(fd).sum()
    return {f: float(s.get(f, 0.0)) for f in K.FEEDERS}
