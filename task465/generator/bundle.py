"""Read the shipped pack the way an analyst would, for the goldens and the checks: nothing here touches the generator's
internal state. Every handling a route can take is a keyword, the golden's the default."""
import csv
import datetime as dt
import os
import re

import world as W

NI_ITEMS = {
    "SORGHUM, GRAIN, NON-IRRIGATED - ACRES HARVESTED": "harvested",
    "SORGHUM, GRAIN, NON-IRRIGATED - PRODUCTION, MEASURED IN BU": "production",
    "SORGHUM, GRAIN, NON-IRRIGATED - YIELD, MEASURED IN BU / ACRE": "yield",
}
ALL_ITEMS = {
    "SORGHUM, GRAIN - ACRES HARVESTED": "harvested",
    "SORGHUM, GRAIN - PRODUCTION, MEASURED IN BU": "production",
    "SORGHUM, GRAIN - YIELD, MEASURED IN BU / ACRE": "yield",
}


def path(target, key):
    return os.path.join(target, W.FILES[key])


def num(v):
    v = v.strip()
    if v.startswith("("):
        return None
    return float(v.replace(",", ""))


def district_code(code, year):
    c = int(code)
    return c * 10 if c < 10 else c


def read_export(target, key):
    with open(path(target, key), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def estimates(target, vintage="latest", items=None):
    """{(level, district, county, year, field): value or None} for the sorghum items asked, with the later download
    taking the years it holds ('latest'), or the March 2024 download wherever it has the year ('early')."""
    items = items or NI_ITEMS
    out = {}
    order = ("pull24", "pull26") if vintage == "latest" else ("pull26", "pull24")
    for key in order:
        for r in read_export(target, key):
            if r["Data Item"] not in items or r["Geo Level"] == "STATE":
                continue
            y = int(r["Year"])
            d = district_code(r["Ag District Code"], y)
            c = r["County"].title() if r["Geo Level"] == "COUNTY" else ""
            out[(r["Geo Level"], d, c, y, items[r["Data Item"]])] = num(r["Value"])
    return out


def county_district(target):
    """Each county's district, from the export (unchanged over the years)."""
    out = {}
    for r in read_export(target, "pull26"):
        if r["Geo Level"] == "COUNTY":
            out[r["County"].title()] = district_code(r["Ag District Code"], int(r["Year"]))
    return out


def sorghum(target, vintage="latest", practice="NI"):
    """county -> year -> dict(harvested, production, yield) (None where withheld); district -> year -> dict."""
    e = estimates(target, vintage, NI_ITEMS if practice == "NI" else ALL_ITEMS)
    cty, dist = {}, {}
    for (lvl, d, c, y, f), v in e.items():
        if lvl == "COUNTY":
            cty.setdefault(c, {}).setdefault(y, {})[f] = v
        else:
            dist.setdefault(d, {}).setdefault(y, {})[f] = v
    return cty, dist


def terms(target):
    """The term sheet's expected 2027 yield and trend per county, read from its table."""
    import pypdf
    txt = "\n".join(p.extract_text() for p in pypdf.PdfReader(path(target, "terms")).pages)
    out = {}
    for c in W.MEMBERS:
        m = re.search(r"\b%s\s+(\d+\.\d)\s+(\d+\.\d\d)\b" % c, txt)
        out[c] = dict(expected=float(m.group(1)), trend=float(m.group(2)))
    return out


def quotes(target):
    import openpyxl
    wb = openpyxl.load_workbook(path(target, "quotes"), data_only=True)
    ws = wb["Dryland grain sorghum"]
    out = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        if row[0] in W.MEMBERS:
            out[row[0]] = 100.0 * float(row[3])
    return out


def enrolment(target):
    with open(path(target, "enrol"), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def tickets(target):
    with open(path(target, "tickets"), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def transfers(target):
    with open(path(target, "transfers"), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- the main call
def yields(target, mode="golden", vintage="latest", practice="NI"):
    """county -> year -> the yield a route uses (absent where it drops the year)."""
    cty, dist = sorghum(target, vintage, practice)
    cd = county_district(target)
    out = {}
    for c in W.MEMBERS:
        d = cd[c]
        peers = [k for k, v in cd.items() if v == d and k != c]
        ser = {}
        pub = {y: v["yield"] for y, v in cty[c].items() if v["yield"] is not None}
        dy = {y: v["production"] / v["harvested"] for y, v in dist[d].items()}
        pubyears = sorted(pub)
        ratio = sum(pub[y] / dy[y] for y in pubyears) / len(pubyears)
        import numpy as np
        bb, aa = np.polyfit([dy[y] for y in pubyears], [pub[y] for y in pubyears], 1)
        worst = min(pub.values())
        for y in range(1991, 2026):
            if y in pub:
                ser[y] = pub[y]
                continue
            if mode == "drop":
                continue
            if mode == "golden":
                h = dist[d][y]["harvested"] - sum(cty[k][y]["harvested"] for k in peers)
                p = dist[d][y]["production"] - sum(cty[k][y]["production"] for k in peers)
                ser[y] = round(p / h, 1)
            elif mode == "golden_unrounded":
                h = dist[d][y]["harvested"] - sum(cty[k][y]["harvested"] for k in peers)
                p = dist[d][y]["production"] - sum(cty[k][y]["production"] for k in peers)
                ser[y] = p / h
            elif mode == "district":
                ser[y] = round(dy[y], 1)
            elif mode == "ratio":
                ser[y] = ratio * dy[y]
            elif mode == "regress":
                ser[y] = float(aa + bb * dy[y])
            elif mode == "worst":
                ser[y] = worst
            elif mode == "zero":
                ser[y] = 0.0
        out[c] = ser
    return out


def recovered(target, vintage="latest"):
    cty, dist = sorghum(target, vintage)
    cd = county_district(target)
    out = {}
    for c in W.MEMBERS:
        d = cd[c]
        peers = [k for k, v in cd.items() if v == d and k != c]
        for y, v in cty[c].items():
            if v["yield"] is None:
                h = dist[d][y]["harvested"] - sum(cty[k][y]["harvested"] for k in peers)
                p = dist[d][y]["production"] - sum(cty[k][y]["production"] for k in peers)
                out[(c, y)] = dict(harvested=h, production=p, yld=round(p / h, 1))
    return out


def share(c, y, v, ts, ratio_trend=False):
    e, b = ts[c]["expected"], ts[c]["trend"]
    trig = W.COVERAGE * e
    if ratio_trend:
        adj = v * e / (e - b * (2027 - y))
    else:
        adj = v + b * (2027 - y)
    return min(1.0, max(0.0, (trig - adj) / trig))


def expected_loss(series, ts, ratio_trend=False):
    return {c: 100.0 * sum(share(c, y, v, ts, ratio_trend) for y, v in s.items()) / len(s) for c, s in series.items()}


# ---------------------------------------------------------------- Ask A
def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def enrolled(target, local_close=True, keep_irrigated=False, latest=True):
    close = dt.datetime(2026, 10, 30, 17, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5)))
    rows = enrolment(target)
    if local_close:
        ok = [r for r in rows if utc(r["submitted_at"]) < close]
    else:
        ok = [r for r in rows if r["submitted_at"][:10] <= "2026-10-30"]
    by = {}
    for r in sorted(ok, key=lambda r: r["submitted_at"]):
        if not latest and r["field_id"] in by:
            continue
        by[r["field_id"]] = r
    out = {c: 0.0 for c in W.MEMBERS}
    for r in by.values():
        if r["practice"] != "Non-irrigated" and not keep_irrigated:
            continue
        out[r["field_county"]] += float(r["acres"])
    return out


def liability(target, price_per_bu=None, **kw):
    ts = terms(target)
    q = quotes(target)
    acres = enrolled(target, **kw)
    p = W.PRICE_CWT * W.BUSHEL_LB / 100.0 if price_per_bu is None else price_per_bu
    lia = {c: acres[c] * ts[c]["expected"] * W.COVERAGE * p for c in W.MEMBERS}
    prem = {c: lia[c] * q[c] / 100.0 for c in W.MEMBERS}
    return acres, lia, prem


# ---------------------------------------------------------------- Ask B
def receipts_share(target, drop_transfers=True, shrink=True, sorghum_only=True, vintage="latest"):
    tr = {t["transfer_no"] for t in transfers(target)}
    bu = {c: 0.0 for c in W.MEMBERS}
    for t in tickets(target):
        if sorghum_only and t["commodity"] != "Sorghum":
            continue
        if drop_transfers and t["site"] == "MAIN" and t["reference"] in tr:
            continue
        net = float(t["net_lb"])
        m = float(t["moisture_pct"])
        b = net * (100 - m) / (100 - W.STANDARD_MOISTURE) / W.BUSHEL_LB if shrink else net / W.BUSHEL_LB
        bu[t["origin_county"]] += b
    cty, _ = sorghum(target, vintage, practice="ALL")
    out = {}
    for c in W.MEMBERS:
        prod = sum(cty[c][y]["production"] for y in range(2016, 2021))
        out[c] = 100.0 * bu[c] / prod
    return out
