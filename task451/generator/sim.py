"""Simulate task451's world as IATI activities and transactions, in each publisher's own currency, before any file is
written. Every amount is built forward from the design's per-country channel sizes (world.TARGET); the figures the
task grades are computed afterwards from the records, never fixed first."""
import calendar
import datetime as dt
import math

import numpy as np

import world as W

D = dt.date


def month_end(y, m):
    return D(y, m, calendar.monthrange(y, m)[1])


def add_months(y, m, k):
    t = (y * 12 + (m - 1)) + k
    return t // 12, t % 12 + 1


# ---------------------------------------------------------------------------------------------- exchange table
def fx_table(rng):
    """Units of each currency per US dollar for every calendar day from 1 January 2023 to 30 September 2026: a
    smooth path from the first level to the last with small daily moves; the birr floats on 29 July 2024."""
    days = (W.FX_TO - W.EXTRACT_FROM).days + 1
    dates = [W.EXTRACT_FROM + dt.timedelta(d) for d in range(days)]
    out = {"USD": {d: 1.0 for d in dates}}
    for ccy in sorted(W.FX0):
        a, b = W.FX0[ccy]
        t = np.linspace(0, 1, days)
        noise = np.cumsum(rng.normal(0, 0.0021, days))
        noise -= np.linspace(noise[0], noise[-1], days)                     # pin both ends
        wiggle = 0.012 * np.sin(2 * math.pi * (t * 3.1 + rng.uniform()))
        if ccy == "ETB":
            k = (D(2024, 7, 29) - W.EXTRACT_FROM).days
            path = np.empty(days)
            path[:k] = np.log(a) + (np.log(57.3) - np.log(a)) * t[:k] / t[k]
            path[k:] = np.log(74.6) + (np.log(b) - np.log(74.6)) * ((t[k:] - t[k]) / (1 - t[k])) ** 0.55
            lvl = np.exp(path + noise * 0.6)
        else:
            if ccy == "XAF":                                            # pegged to the euro like the franc CFA of the west
                lvl = None
            else:
                lvl = np.exp(np.log(a) + (np.log(b) - np.log(a)) * t + noise + wiggle * (0.3 if ccy in ("XOF",) else 1.0))
        if lvl is not None:
            dec = 4 if lvl.max() < 20 else (3 if lvl.max() < 1000 else 2)
            out[ccy] = {d: round(float(v), dec) for d, v in zip(dates, lvl)}
    # the two francs CFA hold the euro peg: 655.957 per euro
    out["XOF"] = {d: round(655.957 * out["EUR"][d], 3) for d in dates}
    out["XAF"] = dict(out["XOF"])
    return out


def to_ccy(usd, ccy, fx, d):
    v = usd * fx[ccy][d]
    return round(v, 0) if ccy in ("UGX", "TZS", "RWF", "XOF", "XAF", "ETB", "KES", "NPR", "BDT", "PKR") and v > 1e5 else round(v, 2)


# ---------------------------------------------------------------------------------------------- organisations
def organisations():
    """Every organisation in the pack: ref -> dict(name, type, country, key)."""
    orgs = {}
    for k in W.MEMBER_KEYS:
        m = W.M[k]
        orgs[m["ref"]] = dict(name=m["name"], type="60", key=k, role="member")
    orgs["XI-IATI-FJR"] = dict(name="Fjellrev Foundation", type="60", key="FJE_OLD", role="member_old")
    for f in W.FUNDS.values():
        orgs[f["ref"]] = dict(name=f["name"], type="60", key=f["key"], role="fund")
    for k, p in W.PARTNERS.items():
        orgs[p["ref"]] = dict(name=p["name"], type="60", key=k, role="partner")
    orgs[W.REGIONAL["ref"]] = dict(name=W.REGIONAL["name"], type="40", key="TAM", role="regional")
    for key, country, name_new, ref_new, name_old, ref_old, rereg, ccy in W.DEVICE_ORGS:
        orgs[ref_new] = dict(name=name_new, type="24", key=key, role="impl", country=country, ccy=ccy, rereg=rereg)
        orgs[ref_old] = dict(name=name_old, type="24", key=key, role="impl_old", country=country, ccy=ccy, rereg=rereg)
    for key, countries, name, ref, typ, ccy in W.NET_ORGS:
        orgs[ref] = dict(name=name, type=typ, key=key, role="impl", countries=countries, ccy=ccy)
    return orgs


DEV = {d[0]: dict(key=d[0], country=d[1], name_new=d[2], ref_new=d[3], name_old=d[4], ref_old=d[5], rereg=d[6], ccy=d[7])
       for d in W.DEVICE_ORGS}
NET = {n[0]: dict(key=n[0], countries=n[1], name=n[2], ref=n[3], type=n[4], ccy=n[5]) for n in W.NET_ORGS}


def org_identity(key, identity):
    """(ref, name, currency) an organisation publishes and is paid under."""
    if key in DEV:
        d = DEV[key]
        return (d["ref_old"], d["name_old"], d["ccy"]) if identity == "old" else (d["ref_new"], d["name_new"], d["ccy"])
    n = NET[key]
    return n["ref"], n["name"], n["ccy"]


# the members' direct grants: country (or {country: percentage}), member, organisation, identity, start, months,
# payment pattern, relative size within the country
MEMBER_GRANTS = [
    ("Kenya", "FJE", "KE1", "old", (2023, 3), 42, "semi", 1.0), ("Kenya", "ASH", "KE1", "new", (2024, 7), 36, "semi", 1.1),
    ("Kenya", "TRE", "KE2", None, (2024, 7), 36, "semi", 0.9), ("Kenya", "SEE", "IN1", None, (2025, 1), 24, "semi", 0.6),
    ("Uganda", "FJE", "UG1", "old", (2023, 4), 36, "semi", 1.0), ("Uganda", "MER", "UG1", "new", (2025, 2), 24, "semi", 0.8),
    ("Tanzania", "FJE", "TZ1", "old", (2023, 2), 42, "semi", 1.0), ("Tanzania", "ASH", "TZ1", "new", (2024, 4), 36, "semi", 0.9),
    ("Tanzania", "TRE", "TZ2", None, (2023, 9), 36, "semi", 0.8), ("Tanzania", "MER", "IN2", None, (2025, 1), 24, "semi", 0.6),
    ("Ethiopia", "FJE", "ET1", "old", (2023, 5), 36, "semi", 1.0), ("Ethiopia", "TRE", "ET1", "new", (2024, 9), 24, "semi", 0.7),
    ("Ethiopia", "MER", "ET2", None, (2024, 1), 36, "semi", 0.8), ("Ethiopia", "TRE", "IN1", None, (2024, 3), 30, "semi", 0.6),
    ("Rwanda", "FJE", "RW1", "old", (2023, 1), 48, "semi", 1.0), ("Rwanda", "ZIL", "RW1", "new", (2024, 6), 36, "semi", 1.2),
    ("Rwanda", "MER", "RW2", None, (2023, 7), 48, "semi", 1.8), ("Rwanda", "ASH", "IN2", None, (2024, 4), 36, "semi", 1.5),
    ("Niger", "FJE", "NE1", "old", (2023, 3), 36, "semi", 1.0), ("Niger", "ZIL", "NE1", "new", (2024, 8), 24, "semi", 0.8),
    ("Niger", "SEE", "NE2", None, (2025, 1), 24, "semi", 0.6),
    ({"Burkina Faso": 60, "Niger": 40}, "ZIL", "IN3", None, (2024, 1), 36, "semi", 0.9),
    ("Mali", "FJE", "ML1", "old", (2023, 4), 42, "semi", 1.0), ("Mali", "SEE", "ML1", "new", (2024, 3), 36, "semi", 0.8),
    ("Mali", "ZIL", "ML2", None, (2024, 10), 24, "semi", 0.5),
    ("Burkina Faso", "FJE", "BF1", "old", (2023, 6), 36, "semi", 1.0), ("Burkina Faso", "ZIL", "BF1", "new", (2024, 9), 30, "semi", 0.8),
    ("Chad", "FJE", "TD1", "old", (2023, 2), 42, "semi", 1.0), ("Chad", "SEE", "TD1", "new", (2024, 5), 30, "semi", 0.9),
    ("Chad", "SEE", "TD2", None, (2025, 3), 24, "semi", 0.6),
    ("Senegal", "FJE", "SN1", "old", (2023, 7), 36, "semi", 1.0), ("Senegal", "SEE", "SN1", "new", (2024, 10), 36, "semi", 0.9),
    ("Senegal", "ZIL", "SN2", None, (2024, 9), 24, "semi", 0.6),
    ("Nepal", "FJE", "NP1", "old", (2023, 1), 42, "semi", 1.0), ("Nepal", "TRE", "NP1", "new", (2024, 4), 36, "semi", 0.8),
    ("Nepal", "MER", "NP2", None, (2025, 3), 36, "upfront", 1.3), ("Nepal", "TRE", "IN1", None, (2023, 10), 36, "semi", 0.7),
    ("Bangladesh", "FJE", "BD1", "old", (2023, 8), 36, "semi", 1.0), ("Bangladesh", "MER", "BD1", "new", (2024, 7), 36, "semi", 0.9),
    ("Bangladesh", "TRE", "BD2", None, (2024, 11), 24, "semi", 0.7), ("Bangladesh", "MER", "IN4", None, (2025, 2), 24, "semi", 0.5),
    ("Pakistan", "FJE", "PK1", "old", (2023, 3), 36, "semi", 1.0), ("Pakistan", "MER", "PK1", "new", (2024, 7), 30, "semi", 0.8),
    ("Pakistan", "MER", "PK2", None, (2025, 1), 24, "semi", 0.6), ("Pakistan", "TRE", "IN4", None, (2024, 2), 30, "semi", 0.6),
]
# INGO activities that leave the currency on each transaction to the activity's default (Layer 1)
DEFAULT_CCY_ONLY = {("IN1", "Ethiopia"), ("IN4", "Pakistan"), ("IN4", "Bangladesh")}

# the global fund's annual grants: year -> [(country, organisation, share of the year's grants)]
G_GRANTS = {
    2024: [("Uganda", "UG2", 6.1), ("Uganda", "IN1", 2.2), ("Tanzania", "TZ2", 1.5), ("Ethiopia", "ET2", 2.6),
           ("Rwanda", "RW2", 3.1), ("Niger", "NE2", 1.6), ("Mali", "ML2", 0.9), ("Burkina Faso", "BF2", 1.8),
           ("Chad", "TD2", 2.0), ("Senegal", "SN2", 2.4), ("Nepal", "NP2", 1.3), ("Bangladesh", "BD2", 1.6),
           ("Pakistan", "PK2", 1.5), ("Pakistan", "IN4", 1.2)],
    2025: None,                                                   # sized from the targets below
}
G_2025_SPLIT = {"Uganda": [("UG2", 0.62), ("IN1", 0.38)], "Pakistan": [("PK2", 0.55), ("IN4", 0.45)],
                "Rwanda": [("RW2", 1.0)], "Tanzania": [("TZ2", 1.0)], "Ethiopia": [("ET2", 1.0)],
                "Niger": [("NE2", 1.0)], "Mali": [("ML2", 1.0)], "Burkina Faso": [("BF2", 1.0)], "Chad": [("TD2", 1.0)],
                "Senegal": [("SN2", 1.0)], "Nepal": [("NP2", 1.0)], "Bangladesh": [("BD2", 1.0)]}
S_GRANTS = {2024: [("Niger", "NE2", 9.4), ("Mali", "ML2", 13.9), ("Mali", "IN3", 3.1), ("Burkina Faso", "BF2", 2.6),
                   ("Chad", "TD2", 2.9), ("Senegal", "SN2", 2.1)],
            2025: None}
S_2025_SPLIT = {"Niger": [("NE2", 0.7), ("NE1", 0.3)], "Mali": [("ML2", 0.66), ("IN3", 0.34)],
                "Burkina Faso": [("BF2", 1.0)], "Chad": [("TD2", 1.0)], "Senegal": [("SN2", 1.0)]}


def _jit(rng, d, lo, hi):
    return d + dt.timedelta(int(rng.integers(lo, hi + 1)))


def _workday(d):
    while d.weekday() >= 5:
        d += dt.timedelta(1)
    return d


def tx(kind, date, value, ccy, value_date=None, provider=None, receiver=None, country=None, desc="", ref=""):
    return dict(type=kind, date=date, value=value, ccy=ccy, value_date=value_date, provider=provider, receiver=receiver,
                country=country, desc=desc, ref=ref)


def activity(aid, reporting, title, countries, start, end, status, funding, implementing, ccy, sector, hierarchy=None,
             parent=None, other_ids=None, updated=None, description=""):
    return dict(id=aid, reporting=reporting, title=title, countries=countries, start=start, end=end, status=status,
                funding=funding, implementing=implementing, ccy=ccy, sector=sector, hierarchy=hierarchy, parent=parent,
                other_ids=other_ids or [], updated=updated, description=description, tx=[])


def status_for(end):
    return "2" if end > D(2026, 9, 30) else ("3" if end > D(2026, 3, 31) else "4")


# ---------------------------------------------------------------------------------------------- the members' grants
def member_grants(rng, fx, orgs):
    """The members' direct grants: the member's activity (commitment and payments) and the organisation's activity
    (receipts and monthly spending). Sizes put each country's 2025 spending of members' money near its target."""
    acts, grants = [], []
    by_country = {}
    for g in MEMBER_GRANTS:
        key = g[0] if isinstance(g[0], str) else max(g[0], key=g[0].get)
        by_country.setdefault(key, []).append(g)
    seq = {}
    for g in MEMBER_GRANTS:
        where, mk, okey, ident, (y0, m0), n, pay, wt = g
        countries = {where: 100} if isinstance(where, str) else dict(where)
        main = max(countries, key=countries.get)
        member = W.M[mk]
        ref_i, name_i, ccy_i = org_identity(okey, ident)
        if okey in NET and NET[okey]["ccy"] != "USD":
            ccy_i = NET[okey]["ccy"]
        # the 2025 spending this grant should carry: the country's target spread by weight over its grants
        tgt = W.TARGET[main][0]
        peers = by_country[main]
        months25 = [k for k in range(n) if add_months(y0, m0, k)[0] == 2025]
        frac25 = len(months25) / n
        share = wt / sum(p[7] for p in peers)
        usd_total = tgt * share / max(frac25, 1e-9) if frac25 > 0 else tgt * share * 2
        usd_total *= float(rng.uniform(0.97, 1.03))
        usd_total = round(usd_total * 1e6, 2)
        end = month_end(*add_months(y0, m0, n - 1))
        start = D(y0, m0, 1)
        seq[mk] = seq.get(mk, 0) + 1
        sector = W.SECTORS[int(rng.integers(0, len(W.SECTORS)))][0]
        iso_list = [(W.ISO[c], p) for c, p in countries.items()]
        # the member's activity, under its identifier at the time it was published
        if mk == "FJE":
            mid = "%s-MNH-%02d-%03d" % (member["ref"], y0 % 100, seq[mk])
            oldid = "XI-IATI-FJR-%d-%03d" % (y0, seq[mk]) if start < W.NEW_ID_FROM else None
        else:
            mid = "%s-%s-%d-%03d" % (member["ref"], {"ASH": "GR", "MER": "MF", "TRE": "TT", "ZIL": "SZ", "SEE": "SST"}[mk], y0, seq[mk])
            oldid = None
        oact_id = "%s-%s%02d%s" % (ref_i, member["key"], y0 % 100, "%02d" % seq[mk])
        place = " and ".join(countries) if len(countries) > 1 else main
        mtitle = {"FJE": "Mødre- og nyfødthelse, %s %d-%02d" % (place, y0, end.year % 100),
                  "ASH": "Safe delivery and newborn care in %s" % place, "MER": "Maternal and newborn health, %s" % place,
                  "TRE": "%s: skilled birth attendance programme" % place,
                  "ZIL": "Moeder- en kindzorg %s" % place, "SEE": "Santé maternelle et néonatale, %s" % place}[mk]
        mact = activity(mid, member["ref"], mtitle, iso_list, start, end, status_for(end), [member["ref"]], [ref_i],
                        member["ccy"], sector, other_ids=[(oldid, "A3")] if oldid else [])
        mact["grant"] = dict(member=mk, org=okey, ident=ident, usd=usd_total, months=n, pay=pay, start=start)
        rate0 = fx[member["ccy"]][start]
        commit = round(usd_total * rate0, -3 if member["ccy"] in ("NOK",) else 0)
        mact["tx"].append(tx("2", start, commit, member["ccy"], start, provider=(member["ref"], member["name"], None),
                             receiver=(ref_i, name_i, None), desc="Grant agreement signed"))
        # payments: every six months in advance, or the whole grant at once
        tranches = [0] if pay == "upfront" else list(range(0, n, 6))
        amounts = []
        for i, k in enumerate(tranches):
            if pay == "upfront":
                amounts.append(commit)
            elif i < len(tranches) - 1:
                amounts.append(round(commit * 6 / n, 2))
            else:
                amounts.append(round(commit - sum(amounts), 2))
        # FJE's own payments cite the organisation as its grants system recorded it in 2023 (the old identity);
        # every other member cites the identity the organisation was paid under
        recv_activity = oact_id if mk == "FJE" else None
        stop = W.CANCELLED.get((mk, okey))
        for k, amt in zip(tranches, amounts):
            yy, mm = add_months(y0, m0, k)
            d = _workday(_jit(rng, D(yy, mm, 1), 2, 12))
            if d > W.EXTRACT_TO or (stop and d > stop):
                continue
            if mk == "FJE" and d >= W.NEW_ID_FROM:
                prov = (member["ref"], member["name"], mid)
            elif mk == "FJE":
                prov = ("XI-IATI-FJR", "Fjellrev Foundation", oldid)
            else:
                prov = (member["ref"], member["name"], mid)
            mact["tx"].append(tx("3", d, amt, member["ccy"], d, provider=prov, receiver=(ref_i, name_i, recv_activity),
                                 desc="Grant payment %d of %d" % (tranches.index(k) + 1, len(tranches))))
        if stop:
            paid = sum(t["value"] for t in mact["tx"] if t["type"] == "3")
            mact["tx"].append(tx("2", stop, round(-(commit - paid), 2), member["ccy"], stop,
                                 provider=(member["ref"], member["name"], None), receiver=(ref_i, name_i, None),
                                 desc="Unpaid balance cancelled: grant ended early"))
            mact["status"] = "5"
            mact["end"] = stop
        acts.append(mact)
        # the organisation's activity: receipts and monthly spending
        oact = activity(oact_id, ref_i, "%s: %s" % (name_i, mtitle if mk not in ("FJE", "ZIL", "SEE") else
                                                     "maternal and newborn health, %s" % place),
                        iso_list, start, end, status_for(end), [member["ref"]], [ref_i], ccy_i, sector)
        oact["grant"] = mact["grant"]
        oact["member_activity"] = mid
        for p in mact["tx"]:
            if p["type"] != "3":
                continue
            rd = _workday(p["date"] + dt.timedelta(int(rng.integers(3, 10))))
            if rd > W.EXTRACT_TO:
                continue
            usd = p["value"] / fx[member["ccy"]][p["date"]]
            v = to_ccy(usd * float(rng.uniform(0.994, 1.003)), ccy_i, fx, rd)
            src = p["provider"]
            if mk == "FJE":
                src = ("XI-IATI-FJR", "Fjellrev Foundation", None) if rd < W.NEW_ID_FROM else (member["ref"], member["name"], None)
            oact["tx"].append(tx("1", rd, v, ccy_i, rd, provider=(src[0], src[1], mid if src[0] == member["ref"] else oldid),
                                 receiver=(ref_i, name_i, None), desc="Funds received"))
        # monthly spending in US dollar terms, reported in the organisation's currency at month end
        w = rng.gamma(9.0, 1.0, n)
        w /= w.sum()
        for k in range(n):
            yy, mm = add_months(y0, m0, k)
            d = month_end(yy, mm)
            if d > W.EXTRACT_TO or (stop and d > month_end(stop.year, stop.month)):
                break
            usd = usd_total * w[k]
            v = to_ccy(usd, ccy_i, fx, d)
            oact["tx"].append(tx("4", d, v, ccy_i, d, desc="Programme expenditure, %s %d" % (calendar.month_abbr[mm], yy)))
        if (okey, main) in DEFAULT_CCY_ONLY:
            oact["omit_ccy"] = True
        if stop:
            oact["status"] = "5"
            oact["end"] = stop
        acts.append(oact)
        grants.append(mact["grant"])
    return acts


# ---------------------------------------------------------------------------------------------- the pooled funds
def fund_cycles(rng, fx):
    """The global fund (collects in October to December, pays the collection out as annual grants the next year, its
    first payment of each year the Sahel fund's share in January) and the Sahel fund (its funders pay in January; it
    pays the round out as one-year grants in February and July)."""
    G, S = W.FUNDS["G"], W.FUNDS["S"]
    gfund = activity("%s-POOL" % G["ref"], G["ref"], "%s: pooled fund" % G["name"], [], D(2023, 10, 1), D(2028, 12, 31),
                     "2", [G["ref"]], [G["ref"]], "USD", "13020", hierarchy="1",
                     description=("The Pelorus Maternal Health Fund pools contributions from foundations and other donors "
                                  "and makes annual grants to organisations working on maternal and newborn health in "
                                  "Africa and South Asia. Contributions are pooled: grants are paid from the Fund's pooled "
                                  "resources, and no contribution is earmarked to a grant, a grantee or a country."))
    sfund = activity("%s-POOL" % S["ref"], S["ref"], "%s: pooled fund" % S["name"], [], D(2024, 1, 1), D(2027, 12, 31),
                     "2", [S["ref"]], [S["ref"]], "USD", "13020", hierarchy="1",
                     description=("The Sahel Maternal Survival Fund pools contributions from its funders and makes one-year "
                                  "grants to organisations in the Sahel. Contributions are pooled: grants are paid from the "
                                  "Fund's pooled resources, and no contribution is earmarked to a grant, a grantee or a country."))
    donors = {k: (W.M[k]["ref"], W.M[k]["name"]) for k in W.MEMBER_KEYS}
    donors.update({k: (p["ref"], p["name"]) for k, p in W.PARTNERS.items()})
    donors["TAM"] = (W.REGIONAL["ref"], W.REGIONAL["name"])
    # the collections: in 2023 and 2024 the partners matched each member's contribution on the day it arrived; in
    # 2025 the match lapsed and each donor paid on its own day
    for y, d in W.G_COLLECTION.items():
        members = [k for k in d if k in W.MEMBER_KEYS]
        partners = [k for k in d if k not in W.MEMBER_KEYS]
        mtot = sum(d[k] for k in members)
        days = sorted({_workday(_jit(rng, D(y, 10, 6), 0, 60)) for _ in range(len(members))})
        while len(days) < len(members):
            days.append(_workday(days[-1] + dt.timedelta(9)))
        days = sorted(days)[:len(members)]
        if y in (2023, 2024):
            pc = {k: int(round(d[k] * 1e8)) for k in partners}
            left = dict(pc)
            for i, (k, day) in enumerate(zip(members, days)):
                ref, name = donors[k]
                gfund["tx"].append(tx("1", day, round(d[k] * 1e6, 2), "USD", day, provider=(ref, name, None),
                                      receiver=(G["ref"], G["name"], gfund["id"]), desc="Contribution %d" % y))
                for p in partners:
                    c = left[p] if i == len(members) - 1 else int(round(pc[p] * d[k] / mtot))
                    left[p] -= c
                    pref, pname = donors[p]
                    gfund["tx"].append(tx("1", day, c / 100.0, "USD", day, provider=(pref, pname, None),
                                          receiver=(G["ref"], G["name"], gfund["id"]), desc="Matching contribution %d" % y))
        else:
            for k in members + partners:
                amt = d[k]
                parts = [amt] if amt < 8 else [round(amt * 0.5, 3), round(amt - round(amt * 0.5, 3), 3)]
                for i, a in enumerate(parts):
                    day = _workday(_jit(rng, D(y, 10, 1) + dt.timedelta(34 * i), 0, 40))
                    if day > D(y, 12, 18):
                        day = _workday(D(y, 12, 14))
                    ref, name = donors[k]
                    gfund["tx"].append(tx("1", day, round(a * 1e6, 2), "USD", day, provider=(ref, name, None),
                                          receiver=(G["ref"], G["name"], gfund["id"]), desc="Contribution %d" % y))
    # the Sahel fund's rounds settle on one day each January, the global fund's share with the others
    for y, d in W.S_ROUND.items():
        gday = _workday(D(y, 1, 23))
        rday = _workday(gday + dt.timedelta(2))
        for k, amt in d.items():
            if k == "G":
                gfund["tx"].append(tx("2", _workday(D(y, 1, 9)), round(amt * 1e6, 2), "USD", _workday(D(y, 1, 9)),
                                      provider=(G["ref"], G["name"], gfund["id"]), receiver=(S["ref"], S["name"], sfund["id"]),
                                      desc="Allocation to the Sahel Maternal Survival Fund, %d round" % y))
                gfund["tx"].append(tx("3", gday, round(amt * 1e6, 2), "USD", gday, provider=(G["ref"], G["name"], gfund["id"]),
                                      receiver=(S["ref"], S["name"], sfund["id"]), desc="Transfer to the Sahel Maternal Survival Fund, %d round" % y))
                sfund["tx"].append(tx("1", rday, round(amt * 1e6, 2), "USD", rday, provider=(G["ref"], G["name"], gfund["id"]),
                                      receiver=(S["ref"], S["name"], sfund["id"]), desc="Contribution, %d round" % y))
            else:
                ref, name = donors[k]
                sfund["tx"].append(tx("1", rday, round(amt * 1e6, 2), "USD", rday, provider=(ref, name, None),
                                      receiver=(S["ref"], S["name"], sfund["id"]), desc="Contribution, %d round" % y))
    return gfund, sfund


def fund_grants(rng, fx, gfund, sfund):
    """The funds' grant activities (hierarchy 2) and the grantees' activities. A grant is spent in the year paid."""
    G, S = W.FUNDS["G"], W.FUNDS["S"]
    acts = []
    g_total = {y: round(sum(W.G_COLLECTION[y - 1].values()) - W.S_ROUND[y]["G"], 3) for y in (2024, 2025, 2026)}
    s_total = {y: round(sum(W.S_ROUND[y].values()), 3) for y in W.S_ROUND}
    tg = sum(W.TARGET[c][2] for c in W.NAMES)
    ts = sum(W.TARGET[c][3] for c in W.NAMES)
    plan = {}
    plan[("G", 2024)] = [(c, o, w) for c, o, w in G_GRANTS[2024]]
    plan[("G", 2025)] = [(c, o, W.TARGET[c][2] * f) for c, lst in G_2025_SPLIT.items() for o, f in lst]
    plan[("S", 2024)] = [(c, o, w) for c, o, w in S_GRANTS[2024]]
    plan[("S", 2025)] = [(c, o, W.TARGET[c][3] * f) for c, lst in S_2025_SPLIT.items() for o, f in lst]
    plan[("G", 2026)] = [(c, o, w * (1.0 + 0.04 * ((i * 7) % 5 - 2))) for i, (c, o, w) in enumerate(plan[("G", 2025)])]
    plan[("S", 2026)] = [(c, o, w * (1.0 + 0.05 * ((i * 3) % 5 - 2))) for i, (c, o, w) in enumerate(plan[("S", 2025)])]
    for (fk, y), items in sorted(plan.items()):
        fund, pool = (G, gfund) if fk == "G" else (S, sfund)
        total = g_total[y] if fk == "G" else s_total[y]
        wsum = sum(w for _, _, w in items)
        cents = [int(round(total * 1e8 * w / wsum)) for _, _, w in items]
        cents[-1] += int(round(total * 1e8)) - sum(cents)
        for i, ((c, okey, _), cv) in enumerate(zip(items, cents)):
            amt = cv / 100.0
            ident = "new" if okey in DEV else None
            ref_i, name_i, _ = org_identity(okey, ident)
            gid = "%s-%s%d-%s-%02d" % (fund["ref"], "G" if fk == "G" else "S", y % 100, W.ISO[c], i + 1)
            oid = "%s-%s%d%s" % (ref_i, "PEL" if fk == "G" else "SMSF", y % 100, W.ISO[c])
            end = D(y, 12, 31)
            ga = activity(gid, fund["ref"], "%s grant %d: %s, %s" % (fund["short"], y, name_i, c), [(W.ISO[c], 100)],
                          D(y, 1, 1) if fk == "G" else D(y, 2, 1), end, status_for(end), [fund["ref"]], [ref_i], "USD", "13020",
                          hierarchy="2", parent=pool["id"])
            commit_day = D(y, 1, 20) if fk == "G" else D(y, 2, 3)
            ga["tx"].append(tx("2", commit_day, round(amt, 2), "USD", commit_day, provider=(fund["ref"], fund["name"], ga["id"]),
                               receiver=(ref_i, name_i, oid), desc="Grant awarded"))
            sched = [(D(y, 2, 10), 0.40), (D(y, 6, 10), 0.35), (D(y, 9, 10), 0.25)] if fk == "G" else \
                    [(D(y, 2, 12), 0.60), (D(y, 7, 10), 0.40)]
            paid = 0.0
            pays = []
            for j, (pd, f) in enumerate(sched):
                pd = _workday(pd)
                if pd > W.EXTRACT_TO:
                    continue
                v = round(amt * f, 2) if j < len(sched) - 1 else round(amt - paid, 2)
                paid = round(paid + v, 2)
                pays.append((pd, v))
                ga["tx"].append(tx("3", pd, v, "USD", pd, provider=(fund["ref"], fund["name"], ga["id"]),
                                   receiver=(ref_i, name_i, oid), desc="Grant tranche %d" % (j + 1)))
            ga["grant"] = dict(fund=fk, year=y, org=okey, country=c, usd=amt)
            acts.append(ga)
            oa = activity(oid, ref_i, "%s: maternal and newborn health, %s (%s %d)" % (name_i, c, fund["short"], y),
                          [(W.ISO[c], 100)], D(y, 1, 1) if fk == "G" else D(y, 2, 1), end, status_for(end),
                          [fund["ref"]], [ref_i], "USD", "13020")
            oa["grant"] = ga["grant"]
            for pd, v in pays:
                rd = _workday(pd + dt.timedelta(int(rng.integers(2, 7))))
                oa["tx"].append(tx("1", rd, v, "USD", rd, provider=(fund["ref"], fund["name"], ga["id"]),
                                   receiver=(ref_i, name_i, oid), desc="Funds received"))
            first = sched[0][0].month
            months = list(range(first, 13))
            wv = rng.gamma(10.0, 1.0, len(months))
            wv /= wv.sum()
            cents_m = [int(round(amt * 100 * x)) for x in wv]
            cents_m[-1] += int(round(amt * 100)) - sum(cents_m)
            for mm, cm in zip(months, cents_m):
                d = month_end(y, mm)
                if d > W.EXTRACT_TO:
                    break
                oa["tx"].append(tx("4", d, cm / 100.0, "USD", d, desc="Programme expenditure, %s %d" % (calendar.month_abbr[mm], y)))
            acts.append(oa)
    return acts


# ---------------------------------------------------------------------------------------------- the old dataset
def old_copies(acts):
    """The member that moved identifier republished its 2023 activities under new identifiers; its old dataset was
    never withdrawn, so the Datastore still holds the old copies as they stood when last updated."""
    out = []
    for a in acts:
        g = a.get("grant")
        if not g or a["reporting"] != W.M["FJE"]["ref"] or g["start"] >= W.NEW_ID_FROM:
            continue
        oldid = [r for r, t in a["other_ids"] if t == "A3"][0]
        c = dict(a)
        c["id"] = oldid
        c["reporting"] = "XI-IATI-FJR"
        place = " and ".join(W.NAME_OF[i] for i, _ in a["countries"])
        c["title"] = "Safe childbirth programme, %s" % place
        c["other_ids"] = []
        c["status"] = "2"
        c["updated"] = W.OLD_DATASET_UPDATED
        c["old_copy"] = True
        c["tx"] = []
        for t in a["tx"]:
            if t["date"] > W.OLD_DATASET_UPDATED.date():
                continue
            t2 = dict(t)
            if t2["provider"] and t2["provider"][0] == W.M["FJE"]["ref"]:
                t2["provider"] = ("XI-IATI-FJR", "Fjellrev Foundation", oldid)
            if t2["provider"] and t2["provider"][0] == "XI-IATI-FJR":
                t2["provider"] = ("XI-IATI-FJR", "Fjellrev Foundation", oldid)
            c["tx"].append(t2)
        out.append(c)
    return out


# ---------------------------------------------------------------------------------------------- other publishers
DONOR_WORDS = ["Halden", "Okonjo", "Varenne", "Brightmoor", "Kestwick", "Alder", "Sorrel", "Umberly", "Castellane",
               "Rimbaud", "Tesoro", "Ashgrove", "Wyndholm", "Ilford", "Morrow", "Pennick", "Larsson", "Fairhaven"]
DONOR_KIND = ["Foundation", "Health Trust", "Fund", "Philanthropies", "Charitable Trust", "Global Health Fund"]
IMPL_WORDS_EN = ["Community", "Village", "Lakeside", "Highland", "Riverside", "Valley", "Hilltop", "Coastal", "Plains",
                 "Savannah", "Delta", "Frontier"]
IMPL_KIND_EN = ["Health Alliance", "Care Network", "Development Trust", "Health Initiative", "Women's Health Group",
                "Midwives Association"]
IMPL_FR = ["Association", "Réseau", "ONG", "Groupement", "Collectif"]
IMPL_FR_KIND = ["Santé Communautaire", "Femmes et Santé", "Solidarité Santé", "Appui Sanitaire", "Mères et Enfants"]


def others(rng, fx, orgs):
    """Donors outside the network and the organisations they fund, in the same countries and sectors."""
    acts = []
    donors = []
    used = set()
    for i in range(18):
        while True:
            nm = "%s %s" % (DONOR_WORDS[int(rng.integers(0, len(DONOR_WORDS)))], DONOR_KIND[int(rng.integers(0, len(DONOR_KIND)))])
            if nm not in used and nm.split()[0] not in {u.split()[0] for u in used}:
                used.add(nm)
                break
        pre = ["US-EIN-%09d" % int(rng.integers(1e8, 9.9e8)), "GB-CHC-%07d" % int(rng.integers(1.0e6, 1.2e6)),
               "NL-KVK-%08d" % int(rng.integers(1e7, 9.9e7)), "XI-IATI-%s" % "".join(w[0] for w in nm.split()).upper() + str(i)]
        ref = pre[i % 4]
        ccy = {0: "USD", 1: "GBP", 2: "EUR", 3: "USD"}[i % 4]
        donors.append(dict(ref=ref, name=nm, ccy=ccy))
        orgs[ref] = dict(name=nm, type="60", key="ND%02d" % i, role="other_donor")
    impls = []
    used_i = set()
    for i in range(40):
        c = W.NAMES[i % 13]
        fr = W.REGION[c] == "Sahel"
        while True:
            if fr:
                nm = "%s %s %s" % (IMPL_FR[int(rng.integers(0, 5))], IMPL_FR_KIND[int(rng.integers(0, 5))], c)
            else:
                nm = "%s %s %s" % (IMPL_WORDS_EN[int(rng.integers(0, 12))], IMPL_KIND_EN[int(rng.integers(0, 6))], c)
            if nm not in used_i:
                used_i.add(nm)
                break
        ref = "XI-IATI-%s%02d" % ("".join(w[0] for w in nm.split() if w[0].isalpha()).upper()[:4], i)
        impls.append(dict(ref=ref, name=nm, country=c, ccy="USD" if i % 3 else W.LOCAL[c]))
        orgs[ref] = dict(name=nm, type="22" if i % 4 else "24", key="NI%02d" % i, role="other_impl", country=c)
    # the network's own organisations also take money from donors outside the network
    net_targets = [("KE2", "Kenya"), ("RW2", "Rwanda"), ("UG2", "Uganda"), ("NP2", "Nepal"), ("SN2", "Senegal"),
                   ("IN2", "Bangladesh"), ("IN3", "Chad")]
    n_act = 0
    for di, dn in enumerate(donors):
        for j in range(30):
            n_act += 1
            imp = impls[int(rng.integers(0, len(impls)))]
            c = imp["country"]
            ref_i, name_i, ccy_i = imp["ref"], imp["name"], imp["ccy"]
            if j == 0 and di < len(net_targets):
                okey, c = net_targets[di]
                ref_i, name_i, ccy_i = org_identity(okey, "new" if okey in DEV else None)
            y0 = int(rng.choice([2022, 2023, 2023, 2024, 2024, 2025]))
            m0 = int(rng.integers(1, 13))
            n = int(rng.choice([24, 30, 36, 48]))
            start = D(y0, m0, 1)
            end = month_end(*add_months(y0, m0, n - 1))
            usd = float(rng.gamma(2.0, 0.9)) * 1e6
            sector = W.SECTORS[int(rng.integers(0, len(W.SECTORS)))][0]
            aid = "%s-%d-%04d" % (dn["ref"], y0, 100 + j)
            da = activity(aid, dn["ref"], "%s: %s, %s" % (dn["name"], ["maternal health", "newborn care", "family planning",
                                                                       "midwifery training"][j % 4], c),
                          [(W.ISO[c], 100)], start, end, status_for(end), [dn["ref"]], [ref_i], dn["ccy"], sector)
            oid = "%s-%s%d%02d" % (ref_i, "D%02d" % di, y0 % 100, j)
            oa = activity(oid, ref_i, "%s: %s programme, %s" % (name_i, ["maternal health", "newborn care", "family planning",
                                                                         "midwifery training"][j % 4], c),
                          [(W.ISO[c], 100)], start, end, status_for(end), [dn["ref"]], [ref_i], ccy_i, sector)
            if start >= W.EXTRACT_FROM:
                da["tx"].append(tx("2", start, round(usd * fx[dn["ccy"]][start], 2), dn["ccy"], start,
                                   provider=(dn["ref"], dn["name"], None), receiver=(ref_i, name_i, None), desc="Commitment"))
            q = list(range(0, n, 3))
            w = rng.gamma(6.0, 1.0, n)
            w /= w.sum()
            for k in q:
                yy, mm = add_months(y0, m0, k)
                d = _workday(_jit(rng, D(yy, mm, 1), 1, 15))
                if d < W.EXTRACT_FROM or d > W.EXTRACT_TO:
                    continue
                amt = usd * w[k:k + 3].sum()
                da["tx"].append(tx("3", d, round(amt * fx[dn["ccy"]][d], 2), dn["ccy"], d, provider=(dn["ref"], dn["name"], aid),
                                   receiver=(ref_i, name_i, oid), desc="Disbursement"))
                rd = _workday(d + dt.timedelta(int(rng.integers(3, 12))))
                if rd <= W.EXTRACT_TO:
                    oa["tx"].append(tx("1", rd, to_ccy(amt, ccy_i, fx, rd), ccy_i, rd, provider=(dn["ref"], dn["name"], aid),
                                       receiver=(ref_i, name_i, oid), desc="Funds received"))
            for k in range(n):
                yy, mm = add_months(y0, m0, k)
                d = month_end(yy, mm)
                if d < W.EXTRACT_FROM or d > W.EXTRACT_TO:
                    continue
                oa["tx"].append(tx("4", d, to_ccy(usd * w[k], ccy_i, fx, d), ccy_i, d,
                                   desc="Programme expenditure, %s %d" % (calendar.month_abbr[mm], yy)))
            acts.extend([da, oa])
    return acts, donors, impls


# ---------------------------------------------------------------------------------------------- the whole world
def simulate(seed=W.SEED):
    rng = np.random.default_rng(seed)
    fx = fx_table(np.random.default_rng(seed + 1))
    orgs = organisations()
    macts = member_grants(np.random.default_rng(seed + 2), fx, orgs)
    gfund, sfund = fund_cycles(np.random.default_rng(seed + 3), fx)
    facts = fund_grants(np.random.default_rng(seed + 4), fx, gfund, sfund)
    olds = old_copies(macts)
    oacts, donors, impls = others(np.random.default_rng(seed + 5), fx, orgs)
    # each publisher's last update: after the 2025 year closed and before the pull
    upd = {}
    urng = np.random.default_rng(seed + 6)
    for a in macts + facts + oacts + [gfund, sfund]:
        if a["reporting"] not in upd:
            base = dt.datetime(2026, 10, 1, 0, 0, 0) + dt.timedelta(minutes=int(urng.integers(0, 60 * 24 * 4 - 1)))
            upd[a["reporting"]] = base
        if a.get("updated") is None:
            a["updated"] = upd[a["reporting"]]
    return dict(fx=fx, orgs=orgs, member_acts=macts, gfund=gfund, sfund=sfund, fund_acts=facts, old=olds,
                other_acts=oacts, donors=donors, impls=impls, rng=rng)


if __name__ == "__main__":
    w = simulate()
    n = sum(len(a["tx"]) for k in ("member_acts", "fund_acts", "old", "other_acts") for a in w[k]) + len(w["gfund"]["tx"]) + len(w["sfund"]["tx"])
    print("activities", sum(len(w[k]) for k in ("member_acts", "fund_acts", "old", "other_acts")), "transactions", n)
