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


def first_app(reg):
    """Each NMI's first successful (not withdrawn) application's received date."""
    ok = reg[reg.status != "Withdrawn"]
    return ok.groupby("nmi").received_date.min()


def tapped_props(xref, first, date):
    d = pd.Timestamp(date)
    t = first[first < d]
    return set(xref[xref.nmi.isin(t.index)].property_no)


def untapped(rates, xref, first, suburb, date):
    r, nm = houses(rates, xref, suburb)
    tp = tapped_props(nm, first, date)
    return r[~r.property_no.isin(tp)]


def campaigns(L):
    reg, rates, xref, net = L["reg"], L["rates"], L["xref"], L["net"]
    first = first_app(reg)
    res_net = net[net.tariff_class == "Residential"]
    out = []
    for row in L["log"]:
        name = row["Suburb"]
        key = [c for c in K.CAMPAIGNS if c["suburb"] == name][0]
        opening = row["Sign-ups opened"]
        opening = opening.date() if hasattr(opening, "date") else opening
        oo_r, oo_n = houses(rates, xref, name)
        unt = untapped(rates, xref, first, name, opening)
        ref = "SS-%s-%s" % (key["key"][-2:], key["key"][:3])
        sysn = reg[(reg.program_ref == ref) & (reg.application_type == "New") & reg.status.isin(CONNECTED)]
        # addresses without PV: residential NMIs in the suburb with no successful application before the opening
        nmis = res_net[res_net.locality.str.upper() == name.upper()].nmi
        t_before = set(first[first < pd.Timestamp(opening)].index)
        udw = int((~nmis.isin(t_before)).sum())
        # untapped owner-occupied houses on the whole feeder
        feeder = key_feeder(name)
        all_oo, all_n = houses(rates, xref, None)
        all_n = all_n.assign(feeder=all_n.nmi.map(L["feeder"]))
        f_props = set(all_n[all_n.feeder == feeder].property_no)
        f_tapped = tapped_props(all_n, first, opening)
        feeder_unt = len(f_props - f_tapped)
        # the suburb's owner-occupied first applications in the twelve months before the opening (organic pace)
        oo_nmis = set(oo_n.nmi)
        f_oo = first[first.index.isin(oo_nmis)]
        before12 = int(((f_oo >= pd.Timestamp(opening) - pd.Timedelta(days=365)) & (f_oo < pd.Timestamp(opening))).sum())
        out.append(dict(key=key["key"], suburb=name, feeder=feeder, opening=opening, letterboxed=int(row["Homes letterboxed"]),
                        systems_log=int(row["Systems installed"]), systems=len(sysn), oo=len(oo_r), untapped=len(unt),
                        udw=udw, feeder_unt=feeder_unt, before12=before12,
                        res_nmis=int(len(nmis)), kw_program=float(sysn.kw.sum())))
    return out


def key_feeder(suburb):
    return [l["feeder"] for l in K.LOCALITIES if l["name"] == suburb][0]


def pools_2027(L):
    reg, rates, xref, net = L["reg"], L["rates"], L["xref"], L["net"]
    first = first_app(reg)
    res_net = net[net.tariff_class == "Residential"]
    out = {}
    for c in K.CAMPAIGNS_2027:
        name = c["suburb"]
        oo_r, oo_n = houses(rates, xref, name)
        unt_base = untapped(rates, xref, first, name, K.BASE + dt.timedelta(days=1))
        f_oo = first[first.index.isin(set(oo_n.nmi))]
        fy0, fy1 = pd.Timestamp(K.LAST_FY[0]), pd.Timestamp(K.LAST_FY[1])
        adopt_fy = int(((f_oo >= fy0) & (f_oo <= fy1)).sum())
        nmis = res_net[res_net.locality.str.upper() == name.upper()].nmi
        t_before = set(first[first <= pd.Timestamp(K.BASE)].index)
        udw = int((~nmis.isin(t_before)).sum())
        all_oo, all_n = houses(rates, xref, None)
        all_n = all_n.assign(feeder=all_n.nmi.map(L["feeder"]))
        f_props = set(all_n[all_n.feeder == c["feeder"]].property_no)
        f_tapped = tapped_props(all_n, first, K.BASE + dt.timedelta(days=1))
        before12 = int(((f_oo > pd.Timestamp(K.BASE) - pd.Timedelta(days=365)) & (f_oo <= pd.Timestamp(K.BASE))).sum())
        out[name] = dict(feeder=c["feeder"], letterboxed=L["letter"][name], oo=len(oo_r), untapped_base=len(unt_base),
                         adopt_fy=adopt_fy, untapped_open=len(unt_base) - adopt_fy, udw=udw,
                         feeder_unt=len(f_props - f_tapped), before12=before12, res_nmis=int(len(nmis)))
    return out


BASES = ["count", "letterboxed", "ratio", "oo", "udw", "feeder_unt", "untapped"]
BASIS_NAME = {"count": "an average campaign", "letterboxed": "per home letterboxed",
              "ratio": "as a rate ratio on the suburb's own pace", "oo": "per owner-occupied house",
              "udw": "per address without PV", "feeder_unt": "per untapped owner-occupied house on the feeder",
              "untapped": "per owner-occupied house without PV in the suburb"}


def rates_by_basis(camps):
    out = {}
    for b in BASES:
        if b == "count":
            v = [c["systems"] for c in camps]
        elif b == "ratio":
            v = [(c["systems"] + c["before12"]) / max(c["before12"], 1) for c in camps]
        else:
            v = [c["systems"] / c[b] for c in camps]
        v = np.array(v, float)
        out[b] = dict(values=v, mean=float(v.mean()), cv=float(v.std() / v.mean()))
    s = np.array([c["systems"] for c in camps], float)
    u = np.array([c["untapped"] for c in camps], float)
    out["untapped"]["pooled"] = float(s.sum() / u.sum())
    out["untapped"]["origin"] = float((s * u).sum() / (u * u).sum())
    slope, icpt = np.polyfit(u, s, 1)
    out["untapped"]["ols"] = (float(slope), float(icpt))
    out["untapped"]["median"] = float(np.median(s / u))
    return out


def lifts(camps, pools, basis, estimator="pooled", pool_date="open"):
    """Systems each 2027 campaign adds under a transfer basis."""
    rb = rates_by_basis(camps)
    out = {}
    for name, p in pools.items():
        if basis == "count":
            n = rb["count"]["mean"]
        elif basis == "letterboxed":
            n = rb["letterboxed"]["mean"] * p["letterboxed"]
        elif basis == "ratio":
            n = (rb["ratio"]["mean"] - 1.0) * p["before12"]
        elif basis in ("oo", "udw", "feeder_unt"):
            n = rb[basis]["mean"] * p[basis]
        else:
            pool = p["untapped_open"] if pool_date == "open" else p["untapped_base"]
            if estimator == "pooled":
                c = rb["untapped"]["pooled"]
                n = c * pool
            elif estimator == "mean":
                n = rb["untapped"]["mean"] * pool
            elif estimator == "origin":
                n = rb["untapped"]["origin"] * pool
            elif estimator == "median":
                n = rb["untapped"]["median"] * pool
            else:
                sl, ic = rb["untapped"]["ols"]
                n = sl * pool + ic
        out[name] = float(n)
    return out


def forecast(L, basis="untapped", estimator="pooled", pool_date="open", hc_case="hc29", base=None, camps=None,
             pools=None):
    base = base or base_forecast(L["reg"])
    camps = camps or campaigns(L)
    pools = pools or pools_2027(L)
    avgkw = avg_new_kw(L["reg"])
    lift = lifts(camps, pools, basis, estimator, pool_date) if basis != "none" else {k: 0.0 for k in pools}
    fc = dict(base["base"])
    add = {}
    for name, n in lift.items():
        f = pools[name]["feeder"]
        add[f] = n * avgkw[f]
        fc[f] += add[f]
    excess = {f: (fc[f] / 1000.0 - L["hca"][f][hc_case]) for f in K.FEEDERS}
    order = sorted(K.FEEDERS, key=lambda f: -excess[f])
    return dict(fc=fc, excess=excess, order=order, winner=order[0], runner=order[1],
                gap=excess[order[0]] - excess[order[1]], lift=lift, add_kw=add, avgkw=avgkw, base=base)


# ------------------------------------------------------------------------------------------------------------------
# the asks

def norm_nmi(s):
    s = s.strip()
    return s[:10] if len(s) == 11 else s


def ask_a(L, mode="golden"):
    """Per feeder: (connected at the base date with no active DER Register record, active DER Register sites with
    no connected system)."""
    reg, der, net, realloc = L["reg"], L["der"], L["net"], L["realloc"]
    live = reg[reg.status.isin(CONNECTED) & (reg.connection_date <= pd.Timestamp(K.BASE)) &
               (reg.removal_date.isna() | (reg.removal_date > pd.Timestamp(K.BASE)))]
    connected = set(live.nmi)
    act = der[der.ac_connection_status == "Active"]
    if mode == "raw":
        nm = act.assign(key=act.nmi)
    else:
        nm = act.assign(key=act.nmi.map(norm_nmi))
        if mode == "golden":
            mp = dict(zip(realloc.old_nmi, realloc.new_nmi))
            nm = nm.assign(key=nm.key.map(lambda x: mp.get(x, x)))
    feeder = L["feeder"]
    der_sites = nm.groupby("key").feeder.first()
    reg_set = set(der_sites.index)
    a, b = {f: 0 for f in K.FEEDERS}, {f: 0 for f in K.FEEDERS}
    for n in connected:
        if n not in reg_set:
            a[feeder[n]] += 1
    for n, f in der_sites.items():
        if n not in connected:
            fd = feeder.get(n, f)
            if mode == "dropunknown" and n not in feeder:
                continue
            b[fd] += 1
    if mode == "rows":
        # device rows counted for the second figure
        b = {f: 0 for f in K.FEEDERS}
        rows = act.assign(key=act.nmi.map(norm_nmi))
        for r in rows.itertuples():
            if r.key not in connected:
                b[feeder.get(r.key, r.feeder)] += 1
    return a, b


def ask_b(L, mode="golden"):
    der, realloc = L["der"], L["realloc"]
    bat = der[(der.device_type == "Battery")]
    if mode != "nodecom":
        bat = bat[bat.ac_connection_status == "Active"]
    if mode in ("golden", "nodecom"):
        one = bat.groupby("ac_connection_id").agg(kwh=("storage_capacity_kwh", "first"), feeder=("feeder", "first"))
    else:
        one = bat.assign(kwh=bat.storage_capacity_kwh)[["kwh", "feeder"]]
    one = one.assign(kwh=one.kwh.astype(float))
    s = one.groupby("feeder").kwh.sum()
    return {f: float(s.get(f, 0.0)) for f in K.FEEDERS}
