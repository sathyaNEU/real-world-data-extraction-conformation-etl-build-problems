"""The golden and every rung, read from the cut pack alone (target/): the paid-stays route the default path takes, the
plants' loads per resident the golden takes, the family of licensed constructions around it, and the two reports."""
import csv
import datetime as dt
import os
import re

import numpy as np
import openpyxl

TOWNS = ["Birchwick", "Teskadel", "Ruddmere", "Sorrelton", "Pinehold", "Tamsen Point", "Esker Narrows", "Hollin Bay"]
PLANT_OF = {"Birchwick": "MN0099127", "Teskadel": "MN0099146", "Ruddmere": "Ruddmere", "Sorrelton": "MN0099158",
            "Pinehold": "Pinehold", "Tamsen Point": "MN0099173", "Esker Narrows": "MN0099181", "Hollin Bay": "MN0099181"}
JOINT = ("Esker Narrows", "Hollin Bay")
MY = [(2025, 10), (2025, 11), (2025, 12)] + [(2026, m) for m in range(1, 10)]
WINTER = [(2026, m) for m in (1, 2, 3, 4)]
APPROPRIATION = 2_400_000
THRESHOLD = 3.0
QUARTERS = {1: ((2025, 7), (2025, 8), (2025, 9)), 2: ((2025, 10), (2025, 11), (2025, 12)),
            3: ((2026, 1), (2026, 2), (2026, 3)), 4: ((2026, 4), (2026, 5), (2026, 6))}
RATE_CHANGE = dt.date(2026, 1, 1)


def days_in(y, m):
    import calendar
    return calendar.monthrange(y, m)[1]


def rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def find(T, prefix):
    for n in sorted(os.listdir(T)):
        if n.startswith(prefix):
            return os.path.join(T, n)
    raise FileNotFoundError(prefix)


def mdy(s):
    return dt.datetime.strptime(s.split(" ")[0], "%m/%d/%Y").date()


# ------------------------------------------------------------------------------------------------ loading

def load(T):
    p = dict(T=T)
    p["residents"] = {r["GEOGRAPHY"].replace(" city", ""): int(r["POPEST_2026_07_01"])
                      for r in rows(find(T, "quillmere_county_population")) if r["GEOGRAPHY"].endswith(" city")}
    # e-reporting: the latest accepted submission for each permit, period, location and parameter
    best = {}
    for r in rows(find(T, "edmr_dmr_export")):
        if r["SUBMISSION_STATUS"] != "Accepted":
            continue
        d = mdy(r["MONITORING_PERIOD_END_DATE"])
        k = (r["PERMIT_ID"], d.year, d.month, r["MONITORING_LOCATION_CODE"], r["PARAMETER_CODE"])
        rec = mdy(r["RECEIVED_DATE"])
        if k not in best or rec > best[k][0]:
            best[k] = (rec, float(r["DMR_VALUE"]))
    plant = {}
    for (pid, y, m, loc, pc), (_, v) in best.items():
        plant.setdefault(pid, {}).setdefault((y, m), {})[(loc, pc)] = v
    p["edmr"] = plant
    p["edmr_raw"] = rows(find(T, "edmr_dmr_export"))
    # the pond systems' workbook
    wb = openpyxl.load_workbook(find(T, "ruddmere_pinehold_ponds"), data_only=True)
    ponds = {}
    mon = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
                                       "Dec"], 1)}
    for ws in wb.worksheets:
        town = ws.title.rsplit(" ", 1)[0]
        for r in ws.iter_rows(min_row=5, values_only=True):
            if not r[0]:
                continue
            mo, yr = r[0].split(" ")
            ponds.setdefault(town, {})[(int(yr), mon[mo])] = dict(inf_flow=r[1], inf_bod=r[2], inf_tss=r[3],
                                                                   discharge=r[4], days=r[5] or 0, eff_flow=r[6],
                                                                   eff_tp=r[9])
    p["ponds"] = ponds
    met = {}
    for r in rows(find(T, "narrows_joint_member_meters")):
        d = mdy(r["READ_AT"]) - dt.timedelta(days=1) if r["READ_AT"].endswith("00:00") else mdy(r["READ_AT"])
        met[(r["MEMBER"], d.year, d.month)] = met.get((r["MEMBER"], d.year, d.month), 0) + int(r["VOLUME_SINCE_LAST_READ_GAL"])
    p["meters"] = met
    p["returns"] = rows(find(T, "lake_protection_fee_returns_2"))
    p["lakeward"] = rows(find(T, "lakeward_stays_remittance"))
    p["kettlepine"] = rows(find(T, "kettle_and_pine_remittance"))
    return p


# ---------------------------------------------------------------------------- each town's plant series

def series(p, town):
    """Monthly average daily influent flow (gallons), BOD load and TSS load (pounds) carried for the town."""
    out = {}
    pid = PLANT_OF[town]
    if town in JOINT:
        for (y, m), v in p["edmr"][pid].items():
            g = p["meters"][(town, y, m)] / days_in(y, m)
            out[(y, m)] = dict(flow=g, bod=g / 1e6 * v[("G", "00310")] * 8.34, tss=g / 1e6 * v[("G", "00530")] * 8.34)
    elif pid in p["ponds"]:
        for ym, r in p["ponds"][pid].items():
            out[ym] = dict(flow=r["inf_flow"] * 1e6, bod=r["inf_flow"] * r["inf_bod"] * 8.34,
                           tss=r["inf_flow"] * r["inf_tss"] * 8.34)
    else:
        for ym, v in p["edmr"][pid].items():
            f = v[("G", "50050")]
            out[ym] = dict(flow=f * 1e6, bod=f * v[("G", "00310")] * 8.34, tss=f * v[("G", "00530")] * 8.34)
    return out


def ck_arrival(r, ck="checkout"):
    """A Kettle & Pine stay's first night: its reference carries the departure date (ck='checkout'); ck='arrival' reads
    that date as the arrival."""
    d = dt.datetime.strptime(r["Reservation"][1:7], "%y%m%d").date()
    return d - dt.timedelta(days=int(r["Nights"])) if ck == "checkout" else d


def paid(p, split="days", ck="checkout"):
    """Paid guests on an average day by town and month: the returns (a quarterly return spread over its months as
    the split says), Lakeward's stays by night, Kettle & Pine's stays by night from the departure its reference carries
    (ck='arrival' reads that date as the arrival; ck='period' puts the stay in its reporting period)."""
    gn = {}

    def add(town, y, m, v):
        gn[(town, y, m)] = gn.get((town, y, m), 0) + v

    for town, y, m, g in returns_by_month(p, split):
        add(town, y, m, g)
    for r in p["lakeward"]:
        town = r["listing_city"].title()
        d = dt.date.fromisoformat(r["check_in"])
        for i in range(int(r["nights"])):
            x = d + dt.timedelta(days=i)
            add(town, x.year, x.month, int(r["guests"]))
    for r in p["kettlepine"]:
        n, g = int(r["Nights"]), int(r["Party size"])
        if ck in ("checkout", "arrival"):
            d = ck_arrival(r, ck)
            for i in range(n):
                x = d + dt.timedelta(days=i)
                add(r["Municipality"], x.year, x.month, g)
        else:
            y, m = int(r["Reporting period"][:4]), int(r["Reporting period"][5:])
            add(r["Municipality"], y, m, g * n)
    return {k: v / days_in(k[1], k[2]) for k, v in gn.items()}


def current_returns(p):
    """Each account's returns for a period: the latest original or amended return, plus any supplemental."""
    by = {}
    for r in p["returns"]:
        k = (r["ACCOUNT_NO"], r["PERIOD_START"])
        by.setdefault(k, []).append(r)
    out = []
    for k, rs in by.items():
        rs = sorted(rs, key=lambda r: mdy(r["DATE_FILED"]))
        base = [r for r in rs if r["RETURN_TYPE"] in ("Original", "Amended")][-1]
        out.append(base)
        out += [r for r in rs if r["RETURN_TYPE"] == "Supplemental"]
    return out


def returns_by_month(p, split="days"):
    for r in current_returns(p):
        a, b = mdy(r["PERIOD_START"]), mdy(r["PERIOD_END"])
        g = int(r["GUEST_NIGHTS_TOTAL"])
        months = [(a.year, a.month)]
        while months[-1] != (b.year, b.month):
            y, m = months[-1]
            months.append((y + 1, 1) if m == 12 else (y, m + 1))
        w = [days_in(*ym) for ym in months] if split == "days" else [1] * len(months)
        for ym, wi in zip(months, w):
            yield r["PROPERTY_CITY"], ym[0], ym[1], g * wi / sum(w)


# ------------------------------------------------------------------------------------------------ the rungs

def records_route(p, split="days", ck="checkout"):
    """The default path: residents plus the paid guests the returns and the platforms record."""
    pd_ = paid(p, split, ck)
    out = {}
    for n in TOWNS:
        R = p["residents"][n]
        pres = {ym: R + pd_.get((n,) + ym, 0) for ym in MY}
        b = max(pres, key=pres.get)
        out[n] = dict(busiest=b, peak=pres[b], ratio=pres[b] / R, qualifies=pres[b] >= THRESHOLD * R)
    return out


def load_route(p, measure="bod", cal=WINTER, winter_paid=True, pooled=False, pd_=None):
    """The golden family: each month's load divided by the load per person in the winter months, when the people in
    town are the residents and the few paid guests the records hold."""
    pd_ = paid(p) if pd_ is None else pd_
    S = {n: series(p, n) for n in TOWNS}
    out = {}
    if pooled:
        per_all = np.mean([sum(S[n][ym][measure] for n in TOWNS) /
                           sum(p["residents"][n] + (pd_.get((n,) + ym, 0) if winter_paid else 0) for n in TOWNS)
                           for ym in cal])
    for n in TOWNS:
        R = p["residents"][n]
        per = per_all if pooled else np.mean([S[n][ym][measure] / (R + (pd_.get((n,) + ym, 0) if winter_paid else 0))
                                              for ym in cal])
        pres = {ym: S[n][ym][measure] / per for ym in MY}
        b = max(pres, key=pres.get)
        out[n] = dict(busiest=b, peak=pres[b], ratio=pres[b] / R, qualifies=pres[b] >= THRESHOLD * R, per=per,
                      present=pres)
    return out


def load_route_paid(p, pd_):
    """The golden with the paid winter guests from another reading of the records."""
    return load_route(p, pd_=pd_)


FAMILY_CALS = ([(2026, m) for m in c] for c in ((1, 2, 3, 4), (1,), (2,), (3,), (4,), (1, 2, 3), (2, 3, 4), (2, 3),
                                                 (1, 2), (3, 4)))


def family(p):
    out = {}
    cals = list(FAMILY_CALS)
    for measure in ("bod", "flow", "tss"):
        for cal in cals:
            for wp in (True, False):
                out[(measure, tuple(cal), wp, False)] = load_route(p, measure, cal, wp, False)
            out[(measure, tuple(cal), True, True)] = load_route(p, measure, cal, True, True)
    return out


def golden(p):
    return load_route(p)


def aid(route):
    q = [n for n in TOWNS if route[n]["qualifies"]]
    share = APPROPRIATION / len(q) if q else 0
    return q, {n: (share if n in q else 0) for n in TOWNS}


def thousand(x):
    return int(np.floor(x / 1000.0 + 0.5)) * 1000


# --------------------------------------------------------------------------------------------- the reports

def quarter_of(d):
    for q, months in QUARTERS.items():
        if (d.year, d.month) in months:
            return q
    return None


def rate_on(d):
    return 1.50 if d >= RATE_CHANGE else 1.25


def ask_a(p, ck="checkout", split_nights=True, rate_by_night=True, returns="current"):
    """The fee generated by stays in each town and quarter of fiscal 2026: the returns' fee for their periods, and
    each platform stay's fee on the nights in the quarter."""
    fee = {(n, q): 0.0 for n in TOWNS for q in QUARTERS}
    rr = current_returns(p) if returns == "current" else (
        [r for r in p["returns"] if r["RETURN_TYPE"] != "Supplemental"] if returns == "latest" else p["returns"])
    if returns == "latest":
        last = {}
        for r in sorted(p["returns"], key=lambda r: mdy(r["DATE_FILED"])):
            last[(r["ACCOUNT_NO"], r["PERIOD_START"])] = r
        rr = list(last.values())
    for r in rr:
        a = mdy(r["PERIOD_START"])
        q = quarter_of(a)
        if q:
            fee[(r["PROPERTY_CITY"], q)] += float(r["FEE_DUE"])

    def stay(town, d0, nights, guests, total, period=None):
        if nights >= 30:
            return
        if period is not None:
            q = quarter_of(period)
            if q:
                fee[(town, q)] += total
            return
        if not split_nights:
            q = quarter_of(d0)
            if q:
                fee[(town, q)] += total
            return
        for i in range(nights):
            x = d0 + dt.timedelta(days=i)
            q = quarter_of(x)
            if q:
                fee[(town, q)] += (rate_on(x) * guests) if rate_by_night else total / nights

    for r in p["lakeward"]:
        stay(r["listing_city"].title(), dt.date.fromisoformat(r["check_in"]), int(r["nights"]), int(r["guests"]),
             float(r["lake_protection_fee_usd"]))
    for r in p["kettlepine"]:
        n, g, tot = int(r["Nights"]), int(r["Party size"]), float(r["Fee remitted (USD)"])
        if ck in ("checkout", "arrival"):
            stay(r["Municipality"], ck_arrival(r, ck), n, g, tot)
        else:
            per = dt.date(int(r["Reporting period"][:4]), int(r["Reporting period"][5:]), 1)
            stay(r["Municipality"], None, n, g, tot, period=per)
    return {k: int(np.floor(v + 0.5)) for k, v in fee.items()}


PLANTS_B = ["Birchwick", "Teskadel", "Ruddmere", "Sorrelton", "Pinehold", "Tamsen Point", "Narrows"]
PERMIT_B = dict(PLANT_OF, Narrows="MN0099181")


def ask_b(p, pond_days="month", edmr="accepted"):
    """Pounds of total phosphorus each plant discharged in each half of 2025: the month's average daily flow (MGD) x
    concentration (mg/L) x 8.34 x the days of the month (pond_days='discharged' takes the pond systems' flow over the
    days discharged instead)."""
    out = {}
    for name in PLANTS_B:
        for h in (1, 2):
            months = range(1, 7) if h == 1 else range(7, 13)
            lb = 0.0
            for m in months:
                if name in ("Ruddmere", "Pinehold"):
                    r = p["ponds"][name][(2025, m)]
                    if r["days"]:
                        d = r["days"] if pond_days == "discharged" else days_in(2025, m)
                        lb += r["eff_flow"] * r["eff_tp"] * 8.34 * d
                else:
                    pid = PERMIT_B[name]
                    v = p["edmr"][pid][(2025, m)] if edmr == "accepted" else edmr_latest(p, pid, 2025, m)
                    lb += v[("1", "50050")] * v[("1", "00665")] * 8.34 * days_in(2025, m)
            out[(name, h)] = round(lb, 1)
    return out


def edmr_latest(p, pid, y, m):
    """The latest submission received for the period, whatever its status (the reflex dedupe)."""
    best = {}
    for r in p["edmr_raw"]:
        d = mdy(r["MONITORING_PERIOD_END_DATE"])
        if r["PERMIT_ID"] != pid or (d.year, d.month) != (y, m):
            continue
        k = (r["MONITORING_LOCATION_CODE"], r["PARAMETER_CODE"])
        rec = mdy(r["RECEIVED_DATE"])
        if k not in best or rec >= best[k][0]:
            best[k] = (rec, float(r["DMR_VALUE"]))
    return {k: v for k, (_, v) in best.items()}


if __name__ == "__main__":
    import sys
    T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                            "target")
    p = load(T)
    g = golden(p)
    d = records_route(p)
    for n in TOWNS:
        print("%-14s golden %d-%02d %7.0f %4.2f %s | records %d-%02d %7.0f %4.2f %s" % (
            n, g[n]["busiest"][0], g[n]["busiest"][1], g[n]["peak"], g[n]["ratio"], g[n]["qualifies"],
            d[n]["busiest"][0], d[n]["busiest"][1], d[n]["peak"], d[n]["ratio"], d[n]["qualifies"]))
    print("golden", aid(g)[0], "records", aid(d)[0])
