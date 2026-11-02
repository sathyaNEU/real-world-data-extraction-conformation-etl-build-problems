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
    # the DER Register extract and the re-allocation log are distractors: read when they ship, empty when deleted
    der = (pd.read_csv(p(K.DER), dtype=str, keep_default_na=False) if os.path.exists(p(K.DER)) else
           pd.DataFrame(columns=["ac_connection_id", "nmi", "registered_date", "status_date", "ac_connection_status"]))
    realloc = (pd.read_csv(p(K.REALLOC), dtype=str, keep_default_na=False) if os.path.exists(p(K.REALLOC)) else
               pd.DataFrame(columns=["old_nmi", "new_nmi", "effective_date", "reason"]))
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
    out = dict(reg=reg, leg=leg, net=net, xref=xref, rates=rates, der=der, realloc=realloc, feeder=feeder, log=log,
               hca=hca, letter=letter_counts(target))
    if os.path.exists(p(K.SCADA)) and os.path.exists(p(K.CHECK_METERS)):
        out.update(winter_frames(target))
    return out


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
# the asks: the winter at Yarrabin zone substation (the feeder-head SCADA historian and the 22 kV check meters)

MONTHS = (6, 7, 8)


def winter_frames(target):
    """The historian's feeder heads (MW, one column per feeder in K.FEEDERS order, one row per half hour by its start in
    Queensland time), the bus section each feeder hangs on (from its tag) and each bus section's flow through its
    transformer's check meter (MW: the half hour's import into the bus less its export back, the meter's interval end
    moved to the half hour's start)."""
    h = pd.read_csv(os.path.join(target, K.SCADA), dtype=str, keep_default_na=False)
    h = h.assign(feeder="YRB" + h.tag.str.extract(r"FDR(\d\d)", expand=False),
                 section="T" + h.tag.str.extract(r"\.B(\d)\.", expand=False))
    hw = h.pivot(index="interval_start_aest", columns="feeder", values="value").astype(float)[K.FEEDERS]
    hw.index = pd.to_datetime(hw.index, format="%Y-%m-%d %H:%M")
    hw = hw.sort_index()
    section = h.drop_duplicates("feeder").set_index("feeder").section.to_dict()
    m = pd.read_csv(os.path.join(target, K.CHECK_METERS), dtype=str, keep_default_na=False)
    m = m.assign(start=pd.to_datetime(m.interval_end_aest, format="%Y-%m-%d %H:%M") - pd.Timedelta(minutes=30),
                 mw=(m.import_kwh.astype(float) - m.export_kwh.astype(float)) / 500.0,
                 back=m.export_kwh.astype(float) / 500.0,
                 section=m.meter_id.str.extract(r"-(T\d)-", expand=False))
    mw = m.pivot(index="start", columns="section", values="mw").sort_index()
    back = m.pivot(index="start", columns="section", values="back").sort_index()
    return dict(scada=hw, section=section, meters=mw, meter_export=back)


def bay_factors(L, pooled=False, intercept=True, shift=0):
    """Each feeder head's factor on the historian: least squares of each bus section's check-meter flow on its own
    feeder heads (with an intercept), or of both meters' total on all eight (pooled). shift moves the meter by whole
    half hours against the historian (0: the meter's interval end read as the half hour it closes). Returns the
    factors and the rms residual of each fit."""
    hw, mw = L["scada"], L["meters"]
    meters = mw.shift(shift) if shift else mw
    j = hw.join(meters, how="inner").dropna()
    groups = {"all": list(K.FEEDERS)} if pooled else {t: [f for f in K.FEEDERS if L["section"][f] == t]
                                                      for t in sorted(set(L["section"].values()))}
    k, rms = {}, {}
    for t, fs in groups.items():
        y = j[list(mw.columns)].sum(axis=1).values if pooled else j[t].values
        A = j[fs].values
        if intercept:
            A = np.column_stack([A, np.ones(len(A))])
        sol = np.linalg.lstsq(A, y, rcond=None)[0]
        res = y - A @ sol
        rms[t] = float(np.sqrt(np.mean((res - res.mean()) ** 2)))
        for i, f in enumerate(fs):
            k[f] = float(sol[i])
    return k, rms


def winter_figures(flow):
    """Per feeder: the energy its head sent back to the zone substation in June, July and August 2026 (MWh, the
    reverse flow summed half hour by half hour) and its largest half-hour reverse flow (MW)."""
    rev = (-flow).clip(lower=0.0)
    out = {}
    for f in K.FEEDERS:
        by_month = rev[f].groupby(rev.index.month).sum() * 0.5
        out[f] = tuple(float(by_month.get(m, 0.0)) for m in MONTHS) + (float(rev[f].max()),)
    return out


def reverse_flow(L, how="golden"):
    """The asks' figures under a route. golden: each feeder head at its own factor fitted to its bus section's check
    meter (bay_factors); recorded: the historian as archived; one_factor: one factor fitted to both meters; section:
    one factor per bus section fitted to its meter; totals: one factor per bus section as the ratio of its meter's
    energy to its feeder heads' (the pro-rata repair under which the totals tie exactly); share: each bus section's
    export register shared among its feeders by the historian's reverse energy that month, the largest half hour at
    the section factor; pv_share: the
    same shared by each feeder's connected capacity at the base date; pooled, no_intercept, misaligned (the meter read
    one half hour early) and exact (each bay's factor as the ratio of two CT ratios, rounded from the fit): the
    decomposition's other constructions."""
    hw, mw = L["scada"], L["meters"]
    if how in ("golden", "pooled", "no_intercept", "misaligned", "exact"):
        k, _ = bay_factors(L, pooled=how == "pooled", intercept=how != "no_intercept",
                           shift=-1 if how == "misaligned" else 0)
        if how == "exact":
            k = {f: nearest_ct_quotient(v) for f, v in k.items()}
        return winter_figures(hw * pd.Series(k))
    if how == "recorded":
        return winter_figures(hw)
    if how == "one_factor":
        x, y = hw.sum(axis=1), mw.sum(axis=1).reindex(hw.index)
        return winter_figures(hw * float((x * y).sum() / (x * x).sum()))
    sec_k = {}
    for t in sorted(set(L["section"].values())):
        fs = [f for f in K.FEEDERS if L["section"][f] == t]
        x, y = hw[fs].sum(axis=1), mw[t].reindex(hw.index)
        kk = float(y.sum() / x.sum()) if how == "totals" else float((x * y).sum() / (x * x).sum())
        for f in fs:
            sec_k[f] = kk
    scaled = hw * pd.Series(sec_k)
    if how in ("section", "totals"):
        return winter_figures(scaled)
    if how in ("share", "pv_share"):
        rec = winter_figures(hw)
        cap = connected_kw(L["reg"], K.BASE) if how == "pv_share" else None
        out = {f: list(winter_figures(scaled)[f]) for f in K.FEEDERS}
        for t in sorted(set(L["section"].values())):
            fs = [f for f in K.FEEDERS if L["section"][f] == t]
            rev = L["meter_export"][t]
            for i, m in enumerate(MONTHS):
                tot = float(rev[rev.index.month == m].sum() * 0.5)
                w = np.array([rec[f][i] if cap is None else cap.get(f, 0.0) for f in fs], float)
                for f, wf in zip(fs, w / w.sum()):
                    out[f][i] = tot * wf
        return {f: tuple(v) for f, v in out.items()}
    raise KeyError(how)


def nearest_ct_quotient(v):
    """The quotient of two standard CT primary ratings nearest a fitted factor."""
    ratings = (200, 300, 400, 500, 600, 800, 1000, 1200)
    return min((b / float(a) for a in ratings for b in ratings), key=lambda q: abs(q - v))
