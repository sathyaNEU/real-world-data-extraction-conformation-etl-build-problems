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
# the campaigns: each suburb's owner-occupied houses and the day each first applied

NEVER = [l["name"] for l in K.LOCALITIES if l["kind"] in ("rest", "transfer")]


def house_first(L, by="received_date"):
    """Every owner-occupied house on the rates roll (land use 02, rating R1) with its locality and the date of its
    first application other than a withdrawn one (NaT if it has none), matched through the GIS cross-reference; a
    house with two NMIs takes the earlier. Also the program reference of that first application."""
    key = "_houses_" + by
    if key in L:
        return L[key]
    rates, xref, reg = L["rates"], L["xref"], L["reg"]
    r = rates[(rates.land_use_code == "02") & (rates.rating_category == "R1")][["property_no", "locality"]]
    ok = reg[reg.status != "Withdrawn"].sort_values([by, "application_id"])
    g = ok.groupby("nmi")
    f, prog = g[by].first(), g.program_ref.first()
    xr = xref[xref.property_no.isin(r.property_no)][["nmi", "property_no"]]
    xr = xr.assign(first=xr.nmi.map(f), prog=xr.nmi.map(prog).fillna(""))
    per = xr.sort_values(["first", "nmi"]).groupby("property_no").agg(first=("first", "first"), prog=("prog", "first"))
    out = r.set_index("property_no").join(per, how="left")
    out["prog"] = out["prog"].fillna("")
    L[key] = out
    return out


def suburb_first(L, name, by="received_date"):
    H = house_first(L, by)
    return H[H.locality == name.upper()]["first"]


def n_between(first, a, b):
    return int(((first >= a) & (first < b)).sum())


def without_pv(first, t):
    return int((first.isna() | (first >= t)).sum())


def openings(L):
    """Each campaign suburb's sign-up opening: the council's summary for 2018 to 2024, its letter for 2026."""
    out = {}
    for row in L["log"]:
        d = row["Sign-ups opened"]
        out[row["Suburb"]] = pd.Timestamp(d.date() if hasattr(d, "date") else d)
    for c in K.CAMPAIGNS_2026:
        out[c["suburb"]] = pd.Timestamp(c["open"])
    return out


def window_end(op, months=36):
    """The end of a campaign's window: months after its opening, or the day after the base date if sooner."""
    return min(pd.Timestamp(op) + pd.DateOffset(months=months), pd.Timestamp(K.BASE) + pd.Timedelta(days=1))


def comparison(L, op, end, mode="nyt", own=None):
    """The suburbs a campaign is read against. nyt: suburbs whose own campaign opens after the window closes (not yet
    treated through it); never: suburbs with no campaign; both: the two; all: every other suburb, campaigns already
    run included."""
    ops = openings(L)
    nyt = [s for s, o in ops.items() if o >= end and s != own]
    if mode == "nyt":
        return nyt
    if mode == "never":
        return list(NEVER)
    if mode == "both":
        return nyt + list(NEVER)
    if mode == "all":
        return [s for s in ops if s != own] + list(NEVER)
    raise KeyError(mode)


def _sorted_days(first):
    return np.sort(first.dropna().values.astype("datetime64[ns]"))


def _monthly(first, edges):
    """First applications in each month between consecutive edges, and houses without PV at each month's start."""
    d = _sorted_days(first)
    pos = np.searchsorted(d, np.array(edges, dtype="datetime64[ns]"), side="left")
    return np.diff(pos), len(first) - pos[:-1]


def campaign_effect(L, suburb, op, months=36, pre=12, mode="nyt", form="ratio", by="received_date"):
    """What a campaign added to its suburb's owner-occupied houses with PV by the end of its window. post: the
    suburb's first applications (program and otherwise) from the opening to the window's end; cf: what the suburb would
    have lodged without the campaign. ratio: its own first applications in the pre months before the opening, scaled
    by the comparison suburbs' change over the same calendar months; hazard: its pre-months rate per house without
    PV, scaled month by month by the comparison's, run forward on its houses without PV at the opening; cs: the ratio
    month by month against the suburbs not yet treated in that month; prepost: its own pre months carried at their
    rate over the window."""
    op = pd.Timestamp(op)
    first = suburb_first(L, suburb, by)
    end = window_end(op, months)
    p0 = op - pd.DateOffset(months=pre)
    post = n_between(first, op, end)
    pre_n = n_between(first, p0, op)
    span = (end - op).days / 365.25
    if form == "prepost":
        cf = pre_n * span / (pre / 12.0)
    elif form == "ratio":
        comp = comparison(L, op, end, mode, suburb)
        cp = sum(n_between(suburb_first(L, s, by), op, end) for s in comp)
        cq = sum(n_between(suburb_first(L, s, by), p0, op) for s in comp)
        cf = pre_n * cp / cq
    elif form in ("hazard", "cs"):
        nm = int(round((end - op).days / 30.4375))
        post_edges = [op + pd.DateOffset(months=k) for k in range(nm)] + [end]
        pre_edges = [p0 + pd.DateOffset(months=k) for k in range(pre)] + [op]
        ops = openings(L)
        if form == "hazard":
            comp = comparison(L, op, end, mode, suburb)
            ca = np.zeros(len(post_edges) - 1)
            cr = np.zeros(len(post_edges) - 1)
            qa = qr = 0.0
            for s in comp:
                a, rk = _monthly(suburb_first(L, s, by), post_edges)
                ca, cr = ca + a, cr + rk
                a0, r0 = _monthly(suburb_first(L, s, by), pre_edges)
                qa, qr = qa + a0.sum(), qr + r0.sum()
            a_s, r_s = _monthly(first, pre_edges)
            h_pre = a_s.sum() / r_s.sum()
            n = float(without_pv(first, op))
            cf = 0.0
            for k in range(len(ca)):
                h = h_pre * (ca[k] / cr[k]) / (qa / qr)
                cf += h * n
                n -= h * n
        else:
            pool = [s for s, o in ops.items() if s != suburb] + list(NEVER)
            series = {s: (_monthly(suburb_first(L, s, by), post_edges)[0], n_between(suburb_first(L, s, by), p0, op))
                      for s in pool}
            cf = 0.0
            for k in range(len(post_edges) - 1):
                m1 = post_edges[k + 1]
                live = [s for s in pool if s in NEVER or ops[s] >= m1] if mode == "both" else \
                       [s for s in pool if s not in NEVER and ops[s] >= m1]
                num = sum(series[s][0][k] for s in live)
                den = sum(series[s][1] for s in live) / float(pre)
                cf += (pre_n / float(pre)) * num / den
    else:
        raise KeyError(form)
    return dict(post=post, pre=pre_n, cf=cf, net=post - cf, pool=without_pv(first, op), span=span)


def key_feeder(suburb):
    return [l["feeder"] for l in K.LOCALITIES if l["name"] == suburb][0]


def residential_nmis(L, name):
    net = L["net"]
    return int(((net.tariff_class == "Residential") & (net.locality.str.upper() == name.upper())).sum())


def campaigns(L, months=36, pre=12, mode="nyt", form="ratio", by="received_date"):
    """The seven past campaigns: the council's figures, the program-referenced systems, the suburb's owner-occupied
    houses and those without PV at the opening, and what each campaign added by the end of its window."""
    reg = L["reg"]
    ops = openings(L)
    out = []
    for row in L["log"]:
        name = row["Suburb"]
        key = [c for c in K.CAMPAIGNS if c["suburb"] == name][0]["key"]
        op = ops[name]
        e = campaign_effect(L, name, op, months, pre, mode, form, by)
        ref = "SS-%s-%s" % (key[-2:], key[:3])
        sysn = reg[(reg.program_ref == ref) & (reg.application_type == "New") & reg.status.isin(CONNECTED)]
        first = suburb_first(L, name)
        e.update(key=key, suburb=name, feeder=key_feeder(name), opening=op.date(), letterboxed=int(row["Homes letterboxed"]),
                 systems_log=int(row["Systems installed"]), systems=len(sysn), kw_program=float(sysn.kw.sum()),
                 oo=len(first), n365=n_between(first, op - pd.DateOffset(months=12), op), res_nmis=residential_nmis(L, name))
        out.append(e)
    return out


def pools_2026(L):
    out = {}
    for c in K.CAMPAIGNS_2026:
        name = c["suburb"]
        first = suburb_first(L, name)
        op = pd.Timestamp(c["open"])
        out[name] = dict(suburb=name, key=c["key"], feeder=key_feeder(name), opening=c["open"], oo=len(first),
                         pool=without_pv(first, op), n365=n_between(first, op - pd.DateOffset(months=12), op),
                         letterboxed=L["letter"][name], res_nmis=residential_nmis(L, name))
    return out


BASES = ["count", "letterboxed", "oo", "n365", "pool"]
BASIS_NAME = {"count": "an average campaign", "letterboxed": "per home letterboxed", "oo": "per owner-occupied house",
              "n365": "per first application in the year before sign-ups",
              "pool": "per owner-occupied house without PV at the opening"}


def rate_of(camps, measure="net", basis="pool", estimator="pooled"):
    """A rate per unit of basis across the past campaigns, for what they added (net) or what they installed
    (systems)."""
    y = np.array([c[measure] for c in camps], float)
    if basis == "count":
        return dict(slope=float(y.mean()), icpt=0.0, values=y, cv=float(y.std(ddof=1) / y.mean()))
    d = np.array([c[basis] for c in camps], float)
    v = y / d
    if estimator == "pooled":
        slope, icpt = float(y.sum() / d.sum()), 0.0
    elif estimator == "mean":
        slope, icpt = float(v.mean()), 0.0
    elif estimator == "median":
        slope, icpt = float(np.median(v)), 0.0
    elif estimator == "origin":
        slope, icpt = float((y * d).sum() / (d * d).sum()), 0.0
    elif estimator == "ols":
        slope, icpt = (float(x) for x in np.polyfit(d, y, 1))
    else:
        raise KeyError(estimator)
    return dict(slope=slope, icpt=icpt, values=v, cv=float(v.std(ddof=1) / v.mean()))


def ratio_se(camps, measure="net", basis="pool"):
    """The standard error of the pooled ratio across the campaigns (the ratio estimator's linearised variance)."""
    y = np.array([c[measure] for c in camps], float)
    d = np.array([c[basis] for c in camps], float)
    rr = y.sum() / d.sum()
    n = len(y)
    return float(np.sqrt(((y - rr * d) ** 2).sum() / (n * (n - 1))) / d.mean())


def lifts(camps, pools, measure="net", basis="pool", estimator="pooled"):
    """What each 2026 campaign adds by its suburb's three-year horizon (systems), on a transfer basis."""
    rr = rate_of(camps, measure, basis, estimator)
    if basis == "count":
        return {name: rr["slope"] for name in pools}
    return {name: rr["slope"] * p[basis] + rr["icpt"] for name, p in pools.items()}


def forecast(L, measure="net", basis="pool", estimator="pooled", hc_case="hc29", base=None, camps=None, pools=None,
             lift=None):
    base = base or base_forecast(L["reg"])
    camps = camps or campaigns(L)
    pools = pools or pools_2026(L)
    avgkw = avg_new_kw(L["reg"])
    if lift is None:
        lift = lifts(camps, pools, measure, basis, estimator) if measure != "none" else {k: 0.0 for k in pools}
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
