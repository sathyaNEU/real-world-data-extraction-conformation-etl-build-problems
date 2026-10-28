"""Every owed figure, from the pack alone. The call: each duty's demand from the Statistics Office's quarterly series (a
partial-adjustment model with quarterly seasons), the cut the GBP 3 million envelope buys once consumers respond over
2027, and the excess burden it removes in 2027 on the whole wedge of duty and GST. The asks: the excise accounted for on
releases from bonded warehouses by duty and quarter, from Customs' declarations under CE14. The wrong routes are kept
beside the golden for the checks."""
import csv
import datetime as dt
import os
import zoneinfo

import numpy as np
from openpyxl import load_workbook
from scipy.optimize import brentq

import params as P

LONDON = zoneinfo.ZoneInfo("Europe/London")
NAMES = {c: n for c, n, *_ in P.DUTIES}
CODE = {n: c for c, n, *_ in P.DUTIES}


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def qkey(label):
    label = label.replace(" ", "")
    return int(label[:4]), int(label[-1])


def series(target):
    """per duty: quarters 2008Q1 to the latest, volume (thousand litres) and price (2026 prices), both layouts stacked"""
    out = {c: {} for c in NAMES}
    wb = load_workbook(os.path.join(target, P.FILES["series_old"]), read_only=True)
    for code, name in NAMES.items():
        for r in list(wb[name].iter_rows(values_only=True))[1:]:
            if r and r[0]:
                out[code][qkey(r[0])] = (float(r[1]), float(r[2]))
    for r in read(os.path.join(target, P.FILES["series_new"])):
        out[CODE[r["duty"]]][qkey(r["quarter"])] = (float(r["duty_paid_clearances_thousand_litres"]),
                                                    float(r["average_shelf_price_gbp_per_litre_2026_prices"]))
    res = {}
    for code, d in out.items():
        ks = sorted(d)
        res[code] = dict(quarters=ks, q=np.array([d[k][0] for k in ks]), p=np.array([d[k][1] for k in ks]))
    return res


def rates(target):
    wb = load_workbook(os.path.join(target, P.FILES["rates"]), read_only=True)
    rows = list(wb["Duty rates"].iter_rows(values_only=True))[1:]
    out = {c: [] for c in NAMES}
    for name, frm, rate, _ in rows:
        d = frm.date() if isinstance(frm, dt.datetime) else frm
        out[CODE[name]].append((d, float(rate)))
    for c in out:
        out[c].sort()
    return out


def rate_on(rt, code, day):
    r = None
    for d, v in rt[code]:
        if d <= day:
            r = v
    return r


def fit(s, form="adl10"):
    """OLS of log volume on quarter dummies, log price and last quarter's log volume (the golden); the variants for the
    checks"""
    lnq, lnp = np.log(s["q"]), np.log(s["p"])
    qs = [k[1] for k in s["quarters"]]
    n = len(lnq)
    Dm = np.array([[1.0 if qs[t] == j + 1 else 0.0 for j in range(4)] for t in range(n)])
    if form == "static":
        b, *_ = np.linalg.lstsq(np.column_stack([Dm, lnp]), lnq, rcond=None)
        return dict(form="static", beta=b[4])
    cols = [Dm[1:], lnp[1:], lnq[:-1]]
    if form in ("adl11",):
        cols.append(lnp[:-1])
    if form in ("adl10t",):
        cols.append(np.arange(1, n)[:, None] / 100.0)
    b, *_ = np.linalg.lstsq(np.column_stack(cols), lnq[1:], rcond=None)
    out = dict(form=form, beta=b[4], lam=b[5])
    if form == "adl11":
        out["beta1"] = b[6]
    return out


def path(m, horizon="year"):
    """the cumulative response of log volume in each quarter of 2027 to a permanent log price change from 1 January"""
    if m["form"] == "static":
        return [m["beta"]] * 4
    if horizon == "longrun":
        return [(m["beta"] + m.get("beta1", 0.0)) / (1 - m["lam"])] * 4
    out, prev = [], 0.0
    for k in range(4):
        prev = m["beta"] + (m.get("beta1", 0.0) if k > 0 else 0.0) + m["lam"] * prev
        out.append(prev)
    if horizon == "impact":
        return [out[0]] * 4
    if horizon == "yearend":
        return [out[3]] * 4
    return out


def baseline(s, rt, code):
    """the latest four quarters, each standing for its quarter of 2027; the latest shelf price; the producer price it
    implies at the duty in force then; the 2027 rate already set"""
    last = s["quarters"][-4:]
    q0 = {k[1]: v * 1000.0 for k, v in zip(last, s["q"][-4:])}
    q0 = np.array([q0[1], q0[2], q0[3], q0[4]])
    y, qn = s["quarters"][-1]
    day = dt.date(y, 3 * qn, 1)
    d_now = rate_on(rt, code, day)
    p_last = s["p"][-1]
    c = p_last / (1 + P.GST) - d_now
    d27 = rate_on(rt, code, dt.date(P.BUDGET_YEAR, 1, 1))
    return q0, c, d27


def appraise(s, rt, code, m, horizon="year", welfare="full", revenue="behav", wedge="all"):
    q0, c, d27 = baseline(s, rt, code)
    p0 = (c + d27) * (1 + P.GST)
    eps = path(m, horizon)

    def outcome(cut):
        p1 = (c + d27 - cut) * (1 + P.GST)
        mult = np.array([(p1 / p0) ** e for e in eps])
        w0, w1 = (p0 - c, p1 - c) if wedge == "all" else (d27, d27 - cut)
        q1 = q0 * mult
        rev = float(np.sum(w0 * q0 - w1 * q1)) if revenue == "behav" else float(np.sum((w0 - w1) * q0))
        gain = 0.0
        for a, b, e in zip(q0, q1, eps):
            if welfare == "full" and wedge != "all":       # the area above the producer price under the pre-GST price
                k = 1.0 + 1.0 / e
                gain += p0 / (1 + P.GST) * a / k * ((b / a) ** k - 1.0) - c * (b - a)
            elif welfare == "full":
                k = 1.0 + 1.0 / e
                gain += p0 * a / k * ((b / a) ** k - 1.0) - c * (b - a)
            elif welfare == "linear":
                gain += (w0 - (w0 - w1) / 2.0) * (b - a)
            else:
                gain += 0.5 * (w0 - w1) * (b - a)
        return rev, gain, q1
    cut = brentq(lambda x: outcome(x)[0] - P.ENVELOPE, 1e-9, d27 * 0.999)
    rev, gain, q1 = outcome(cut)
    return dict(gain=gain, cut=cut, d27=d27, c=c, p0=p0, p1=(c + d27 - cut) * (1 + P.GST), q0=q0, q1=q1,
                wedge_share=(p0 - c) / p0, eps=eps)


ROUTES = {
    "golden": dict(form="adl10"),
    "family_trend": dict(form="adl10t"),
    "family_adl11": dict(form="adl11"),
    "family_linear": dict(form="adl10", welfare="linear"),
    "static_triangle": dict(form="static", welfare="triangle"),
    "triangle_year": dict(form="adl10", welfare="triangle"),
    "longrun_full": dict(form="adl10", horizon="longrun"),
    "static_full": dict(form="static"),
    "static_triangle_static_revenue": dict(form="static", welfare="triangle", revenue="static"),
    "golden_static_revenue": dict(form="adl10", revenue="static"),
    "longrun_triangle": dict(form="adl10", horizon="longrun", welfare="triangle"),
    "duty_only": dict(form="adl10", wedge="duty"),
    "impact_full": dict(form="adl10", horizon="impact"),
    "yearend_full": dict(form="adl10", horizon="yearend"),
}


def call(target):
    S = series(target)
    rt = rates(target)
    fits = {(c, f): fit(S[c], f) for c in NAMES for f in ("adl10", "adl10t", "adl11", "static")}
    routes = {}
    for name, kw in ROUTES.items():
        kw = dict(kw)
        form = kw.pop("form")
        routes[name] = {c: appraise(S[c], rt, c, fits[(c, form)], **kw) for c in NAMES}
    g = routes["golden"]
    order = sorted(g, key=lambda c: -g[c]["gain"])
    return dict(S=S, rt=rt, fits=fits, routes=routes, order=order, winner=order[0], runner=order[1])


# ---------------------------------------------------------------------------------------------------- the asks

def warehouses(target):
    wb = load_workbook(os.path.join(target, P.FILES["warehouses"]), read_only=True)
    rows = list(wb["Approved warehouses"].iter_rows(values_only=True))[1:]
    out = {}
    for wid, name, prem, goods, frm, end in rows:
        d0 = frm.date() if isinstance(frm, dt.datetime) else frm
        d1 = end.date() if isinstance(end, dt.datetime) else (end or None)
        out[wid] = dict(premises=prem, start=d0, end=d1)
    return out


def local_day(ts):
    t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
    return t.astimezone(LONDON).date()


def quarter(d):
    return "%dQ%d" % (d.year, (d.month - 1) // 3 + 1)


# Each route is a set of readings. chain: which declaration's acceptance dates a correction (the first release in
# the chain of related declarations, the declaration it names, or its own). keep: which declarations count (those no
# later declaration corrects, the latest correction of each named declaration, all of them, or those no declaration of
# any procedure names). price: each item's litres at the rates on the first release's day, on the dating day, or on
# its own day; or the declaration's duty kept once on its first item, shared by litres, or summed on every row.
GOLDEN = dict(chain="first", keep="uncorrected", price="first", utc=False, dedup=True, repay=True, lapsed=True,
              imports=False)
MODES = {
    "golden": {},
    "one_hop": dict(chain="named", price="dating"),
    "one_hop_duty": dict(chain="named"),
    "one_hop_header_once": dict(chain="named", price="header_once"),
    "own_quarter": dict(chain="own", price="own"),
    "latest_per_named": dict(chain="named", keep="latest_per_named", price="dating"),
    "every_declaration": dict(chain="own", keep="all", price="own"),
    "named_by_any": dict(keep="named_by_any"),
    "first_own_rate": dict(price="own"),
    "header_once": dict(price="header_once"),
    "header_litres": dict(price="header_litres"),
    "header_every_item": dict(price="header_every_item"),
    "utc_day": dict(utc=True),
    "no_repayments": dict(repay=False),
    "no_lapsed": dict(lapsed=False),
    "no_dedup": dict(dedup=False),
    "with_imports": dict(imports=True),
}


def asks(target, mode="golden"):
    """excise accounted for on releases from bonded warehouses, by duty and quarter (CE14). The golden counts each
    release once, as its last correction, in the quarter the release was first accepted, each item at the rates of
    that day; repayments in their own quarter; removals to premises not approved that day at that day's rates."""
    o = dict(GOLDEN, **MODES[mode])
    rows = read(os.path.join(target, P.FILES["declarations"]))
    rt = rates(target)
    wh = warehouses(target)
    if o["dedup"]:
        seen, uniq = set(), []
        for r in rows:
            key = tuple(r.values())
            if key not in seen:
                seen.add(key)
                uniq.append(r)
        rows = uniq
    out = {c: {q: 0.0 for q in P.ASK_QUARTERS} for c in NAMES}

    def day_of(r):
        if o["utc"]:
            return dt.datetime.strptime(r["accepted_at_utc"], "%Y-%m-%dT%H:%M:%SZ").date()
        return local_day(r["accepted_at_utc"])

    def put(code, d, v):
        q = quarter(d)
        if code in out and q in out[code]:
            out[code][q] += v

    cpcs = ("4071", "4000") if o["imports"] else ("4071",)
    decl = {}
    for r in rows:
        if r["cpc"] in cpcs and r["status"] != "CANCELLED":
            decl.setdefault(r["declaration_no"], []).append(r)
    named = {k: v[0]["related_declaration"] for k, v in decl.items() if v[0]["related_declaration"]}

    def first(k):
        while named.get(k) in decl:
            k = named[k]
        return k
    if o["keep"] == "uncorrected":
        keep = [k for k in decl if k not in set(named.values())]
    elif o["keep"] == "named_by_any":
        refs = {r["related_declaration"] for r in rows if r["related_declaration"]}
        keep = [k for k in decl if k not in refs]
    elif o["keep"] == "latest_per_named":
        latest = {}
        for k, n in named.items():
            if n not in latest or day_of(decl[k][0]) > day_of(decl[latest[n]][0]):
                latest[n] = k
        keep = [k for k in decl if k not in named and k not in named.values()] + list(latest.values())
    else:
        keep = list(decl)
    for k in keep:
        items = decl[k]
        own = day_of(items[0])
        start = day_of(decl[first(k)][0])
        d = {"first": start, "named": day_of(decl[named[k]][0]) if named.get(k) in decl else own, "own": own}[o["chain"]]
        header = float(items[0]["duty_gbp"])
        if o["price"] == "header_once":
            put(min(items, key=lambda r: int(r["item_no"]))["duty_code"], d, header)
        elif o["price"] == "header_litres":
            tot = sum(float(r["quantity_litres"]) for r in items)
            for r in items:
                put(r["duty_code"], d, header * float(r["quantity_litres"]) / tot)
        elif o["price"] == "header_every_item":
            for r in items:
                put(r["duty_code"], d, header)
        else:
            rate_day = {"first": start, "dating": d, "own": own}[o["price"]]
            for r in items:
                if r["duty_code"] in NAMES:
                    put(r["duty_code"], d, round(float(r["quantity_litres"]) * rate_on(rt, r["duty_code"], rate_day), 2))
    if o["repay"]:
        for r in rows:
            if r["cpc"] == "6171" and r["status"] != "CANCELLED":
                put(r["duty_code"], day_of(r), -float(r["duty_gbp"]))
    if o["lapsed"]:
        for r in rows:
            if r["cpc"] != "7171" or r["status"] == "CANCELLED":
                continue
            d = day_of(r)
            prem = wh[r["warehouse_to"]]["premises"]
            ok = any(w["premises"] == prem and w["start"] <= d and (w["end"] is None or d < w["end"])
                     for w in wh.values())
            if not ok:
                put(r["duty_code"], d, round(float(r["quantity_litres"]) * rate_on(rt, r["duty_code"], d), 2))
    return {c: {q: round(v, 2) for q, v in d.items()} for c, d in out.items()}


def thousand(v):
    """GBP thousands to one decimal place"""
    return float(np.floor(v / 100.0 + 0.5) / 10.0)
