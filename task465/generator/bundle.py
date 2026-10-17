"""Read the shipped pack the way an analyst would, for the goldens and the checks: nothing here touches the generator's
internal state. Every handling a route can take is a keyword, the golden's the default."""
import csv
import datetime as dt
import os

import world as W


def path(target, key):
    return os.path.join(target, W.FILES[key])


def rows(target, key):
    with open(path(target, key), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def register(target):
    """County code (three digits) to service division."""
    return {r["COUNTY_FIPS"]: r["SERVICE_DIVISION"] for r in rows(target, "divisions")}


def county_names(target):
    return {r["COUNTY"]: r["SERVICE_DIVISION"] for r in rows(target, "divisions")}


def band_of_income(v):
    v = float(v)
    return 0 if v < 25000 else 1 if v < 50000 else 2 if v < 75000 else 3


INCCAT_BAND = {k: b for k, _, b in W.INCCAT}


def burden_shares(target, monthly_as_annual=False, weight="WT_FINAL", by="division"):
    """The energy survey's weighted share with annual home energy costs above 6 per cent of income, by division (or
    county) and eligible band."""
    reg = register(target)
    num, den = {}, {}
    for r in rows(target, "heas"):
        d = reg.get(r["COUNTY"])
        if d is not None and by == "county":
            d = r["COUNTY"]
        b = band_of_income(r["HHINC"])
        if d is None or b not in W.ELIGIBLE_BANDS:
            continue
        elec = float(r["ELEC_AMT"]) * (12 if r["ELEC_BASIS"] == "M" and not monthly_as_annual else 1)
        cost = elec + float(r["GAS_AMT"]) + float(r["OTHER_AMT"])
        w = float(r[weight])
        key = (d, b)
        den[key] = den.get(key, 0.0) + w
        num[key] = num.get(key, 0.0) + w * (cost / float(r["HHINC"]) > W.BURDEN)
    return {k: num[k] / den[k] for k in den}


def equipment_shares(target, dk_as_no=False, by="division"):
    """The health survey's household-weighted share with someone using electrically powered medical equipment, by
    division (or county) and eligible band."""
    reg = register(target)
    num, den = {}, {}
    for r in rows(target, "shs"):
        d = reg.get("%03d" % int(r["CNTYFIPS"]))
        if d is not None and by == "county":
            d = "%03d" % int(r["CNTYFIPS"])
        b = INCCAT_BAND[int(r["INCCAT"])]
        a = int(r["MEDEQUIP"])
        if d is None or b not in W.ELIGIBLE_BANDS or (a in (7, 9) and not dk_as_no):
            continue
        w = float(r["HH_WT"])
        key = (d, b)
        den[key] = den.get(key, 0.0) + w
        num[key] = num.get(key, 0.0) + w * (a == 1)
    return {k: num[k] / den[k] for k in den}


def households(target, by="division"):
    """The demographer's July 1, 2025 households of each division (or county) and eligible band (county rows only)."""
    import openpyxl
    reg = register(target)
    ws = openpyxl.load_workbook(path(target, "estimates"), data_only=True)["Households by income"]
    out = {}
    for row in ws.iter_rows(min_row=5, values_only=True):
        fips = row[1]
        if not fips or fips not in reg:
            continue
        for b in W.ELIGIBLE_BANDS:
            key = (reg[fips] if by == "division" else fips, b)
            out[key] = out.get(key, 0) + int(row[3 + b])
    return out


def pilot_tables(target, keep_dups=False, partial_as_no=False, dk_as_no=False):
    """The pilot's 2x2 tables (both, burden only, equipment only, neither) by band and by division and band, from each
    address's latest complete screen."""
    recs = rows(target, "pilot")
    if not keep_dups:
        latest = {}
        for r in recs:
            if r["STATUS"] == "Complete" or (partial_as_no and r["STATUS"] == "Partial"):
                k = r["ADDRESS_KEY"]
                if k not in latest or (r["RECEIVED"], r["SCREEN_ID"]) > (latest[k]["RECEIVED"], latest[k]["SCREEN_ID"]):
                    latest[k] = r
        recs = list(latest.values())
    tabs, tabs_div = {}, {}
    for r in recs:
        st = r["STATUS"]
        if st == "Ended - income" or (st == "Partial" and not partial_as_no):
            continue
        eq = r["MED_EQUIPMENT"] or "No"
        if eq == "Don't know":
            if not dk_as_no:
                continue
            eq = "No"
        inc = float(r["HH_INCOME"])
        x = (float(r["ELEC_12M"]) + float(r["OTHER_FUELS_12M"])) / inc > W.BURDEN
        y = eq == "Yes"
        k = 0 if (x and y) else 1 if x else 2 if y else 3
        b = band_of_income(inc)
        for key, store in ((b, tabs), ((r["DIVISION"], b), tabs_div)):
            store.setdefault(key, [0, 0, 0, 0])[k] += 1
    return tabs, tabs_div


def conformed(target, **kw):
    """Everything the fusion reads: households, the two surveys' shares and the pilot's tables."""
    p = burden_shares(target, monthly_as_annual=kw.get("monthly_as_annual", False), weight=kw.get("weight", "WT_FINAL"))
    q = equipment_shares(target, dk_as_no=kw.get("dk_as_no", False))
    tabs, tabs_div = pilot_tables(target, keep_dups=kw.get("keep_dups", False),
                                  partial_as_no=kw.get("partial_as_no", False), dk_as_no=kw.get("pilot_dk_as_no", False))
    return households(target), p, q, tabs, tabs_div


# ---------------------------------------------------------------- the asks
COUNT_DATE = dt.date(2026, 10, 31)


class Chains:
    """Accounts joined into households through the enrolment extract's prior accounts."""

    def __init__(self, target):
        self.parent = {}
        for r in rows(target, "baseline"):
            self.find(r["ACCOUNT_NO"])
            if r["PRIOR_ACCOUNT_NO"]:
                self.union(r["ACCOUNT_NO"], r["PRIOR_ACCOUNT_NO"])

    def find(self, a):
        self.parent.setdefault(a, a)
        while self.parent[a] != a:
            self.parent[a] = self.parent[self.parent[a]]
            a = self.parent[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[max(ra, rb)] = min(ra, rb)


def baseline_households(target, unit="household", division="register"):
    """Households (or accounts) on the medical baseline rate at the end of October 2026, by division: unit 'household'
    joins accounts through prior accounts, 'account' counts accounts; division 'register' takes the premise county's
    division from the register, 'stored' the extract's own column."""
    names = county_names(target)
    ch = Chains(target) if unit == "household" else None
    seen = {}
    for r in rows(target, "baseline"):
        start = dt.date.fromisoformat(r["START_DATE"])
        end = dt.date.fromisoformat(r["END_DATE"]) if r["END_DATE"] else None
        if not (start <= COUNT_DATE and (end is None or end >= COUNT_DATE)):
            continue
        key = ch.find(r["ACCOUNT_NO"]) if ch else r["ACCOUNT_NO"]
        d = names[r["SERVICE_COUNTY"]] if division == "register" else r["DIVISION"]
        if key not in seen or start > seen[key][0]:
            seen[key] = (start, d)
    out = {d: 0 for d in W.DIV_NAMES}
    for start, d in seen.values():
        out[d] += 1
    return out


def central_date(utc):
    t = dt.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
    off = 5 if dt.datetime(2026, 3, 8, 8) <= t < dt.datetime(2026, 11, 1, 7) else 6
    return (t - dt.timedelta(hours=off)).date()


def battery_households(target, unit="household", clock="central"):
    """Households given a backup battery from January to October 2026, by division: unit 'household' (accounts joined
    through the enrolment extract's prior accounts), 'account', 'serial' or 'order'; clock 'central' or 'utc'."""
    names = county_names(target)
    ch = Chains(target) if unit == "household" else None
    seen = {}
    for r in rows(target, "batteries"):
        if r["STATUS"] != "Completed":
            continue
        day = central_date(r["COMPLETED_UTC"]) if clock == "central" else dt.date.fromisoformat(r["COMPLETED_UTC"][:10])
        if not (dt.date(2026, 1, 1) <= day <= COUNT_DATE):
            continue
        key = {"household": lambda: ch.find(r["ACCOUNT_NO"]), "account": lambda: r["ACCOUNT_NO"],
               "serial": lambda: r["UNIT_SERIAL"], "order": lambda: r["WORK_ORDER"]}[unit]()
        seen[key] = names[r["SERVICE_COUNTY"]]
    out = {d: 0 for d in W.DIV_NAMES}
    for d in seen.values():
        out[d] += 1
    return out
