"""The trust's grants: the grants system's register and instalment schedule at 30 November 2026, and the finance
system's payment ledger from January 2023.

Core grants run three years with an instalment at the start of each grant year, paid on its due date. Project grants
pay a first instalment on the start date (paid on its due date) and later instalments on progress report dates: the
grants system schedules each later instalment on the date the report is due, and the trust pays it once the grants
committee has accepted the report, 35 to 70 days after the due date. A withdrawal is recorded on the grant; its
instalments keep the status they had. Grants to partners in Ireland are awarded and paid in euro; the schedule carries
the amount in the grant's own currency.
"""
import datetime as dt

import numpy as np

import world as W

PROGRAMMES = ["Communities", "Young people", "Environment", "Arts and heritage"]
TOWNS = ["Wrexford", "Hexley", "Barnsworth", "Coldmere", "Stainby", "Linthorpe", "Ashwell", "Drayford", "Kelsall",
         "Morley Green", "Pennington", "Upper Tadley", "Wolsey Bridge", "Hatherby", "Grisedale", "Norbrook",
         "Elmstead", "Thornaby Vale", "Rushden Cross", "Calder Moor"]
KINDS = {
    "Communities": ["Community Hub", "Food Partnership", "Advice Centre", "Neighbourhood Trust", "Community Association",
                    "Credit Union", "Tenants' Federation", "Community Transport"],
    "Young people": ["Youth Project", "Young Carers", "Youth Theatre", "Boxing Club", "Scout and Guide Hut Trust",
                     "Mentoring Scheme", "Youth Forum", "Detached Youth Work"],
    "Environment": ["Rivers Trust", "Wildlife Group", "Community Orchard", "Repair Cafe", "Allotment Society",
                    "Woodland Trust", "Canal Partnership", "Green Spaces Network"],
    "Arts and heritage": ["Heritage Railway", "Arts Centre", "Local History Society", "Brass Band", "Museum Trust",
                          "Choral Society", "Mill Heritage Trust", "Print Workshop"],
}
IRISH = ["Ballyconnell Community Development CLG", "Shannonside Rivers Network CLG", "Kilmacow Youth Arts CLG",
         "Drumshanbo Heritage Trust CLG", "Inishowen Food Partnership CLG", "Glenbrien Repair Network CLG"]
CORRIDORS = [(dt.date(2026, 10, 23), dt.date(2026, 11, 26)), (dt.date(2027, 10, 23), dt.date(2027, 11, 26))]


def bday_on_or_after(d):
    while not W.is_bday(d, "UK"):
        d += dt.timedelta(days=1)
    return d


def in_corridor(d):
    return any(a <= d <= b for a, b in CORRIDORS)


def make(seed, knobs):
    """knobs: euro grants' scale, withdrawn grants' scale, the year-end tails' scales"""
    rng = np.random.default_rng(seed)
    grants, inst = [], []
    used = set()
    refno = 21000 + int(rng.integers(100, 300))

    def name(prog):
        while True:
            nm = "%s %s" % (rng.choice(TOWNS), rng.choice(KINDS[prog]))
            if nm not in used:
                used.add(nm)
                return nm
    # awards from January 2021 to November 2026
    awards = []
    d = dt.date(2021, 1, 18)
    while d <= dt.date(2026, 11, 20):
        awards.append(d)
        d += dt.timedelta(days=int(rng.integers(9, 21)))
    euro_left = 6
    for ad in awards:
        ad = bday_on_or_after(ad)
        refno += int(rng.integers(1, 9))
        prog = PROGRAMMES[int(rng.integers(0, 4))]
        core = rng.random() < 0.34
        euro = euro_left > 0 and ad >= dt.date(2024, 1, 1) and rng.random() < 0.08 * knobs.get("euro_rate", 1.0)
        if euro:
            grantee = IRISH[6 - euro_left]
            euro_left -= 1
        else:
            grantee = name(prog)
        ref = "WT%d" % refno
        start = bday_on_or_after(ad + dt.timedelta(days=int(rng.integers(14, 35))))
        if core:
            per = int(rng.choice([25, 30, 35, 40, 45, 50, 60, 75]) * 1000 * knobs.get("scale", 1.0) / 500) * 500
            n = 3
            amounts = [per] * n
            dues = [bday_on_or_after(dt.date(start.year + k, start.month, min(start.day, 28))) for k in range(n)]
            kinds = ["core"] * n
        else:
            total = int(rng.choice([20, 24, 30, 36, 40, 45, 48, 60, 75, 90, 120, 150]) * 1000 * knobs.get("scale", 1.0) / 1000) * 1000
            n = int(rng.choice([2, 3, 3, 4]))
            first = round(total * float(rng.choice([0.4, 0.5])) / 250) * 250 if n > 2 else round(total * 0.6 / 250) * 250
            rest = total - first
            later = [round(rest / (n - 1) / 250) * 250] * (n - 1)
            later[-1] = rest - sum(later[:-1])
            amounts = [first] + later
            gap = int(rng.choice([6, 12, 12]))
            dues = [start]
            for k in range(1, n):
                m0 = start.month - 1 + gap * k
                y, m = start.year + m0 // 12, m0 % 12 + 1
                dues.append(bday_on_or_after(dt.date(y, m, min(start.day, 28)) + dt.timedelta(days=int(rng.integers(-3, 4)))))
            kinds = ["first"] + ["later"] * (n - 1)
        if euro:
            amounts = [int(round(a * 1.15 / 500) * 500) for a in amounts]
        grants.append(dict(ref=ref, grantee=grantee, programme=prog, type="Core" if core else "Project", award=ad,
                           currency="EUR" if euro else "GBP", amount=sum(amounts), status="Active", status_date=ad))
        for k, (a, dd, kd) in enumerate(zip(amounts, dues, kinds), 1):
            inst.append(dict(ref=ref, no=k, due=dd, amount=a, kind=kd, type=grants[-1]["type"]))
    return grants, inst


def settle(grants, inst, seed, knobs):
    """payments up to 30 November 2026, withdrawals, statuses; corridors kept clear of later instalments"""
    rng = np.random.default_rng(seed + 1)
    G = {g["ref"]: g for g in grants}
    cut = W.VAL_DATE
    # keep the year-end corridors clear: a later instalment due inside one moves to the corridor's far side
    for i in inst:
        if i["kind"] == "later" and in_corridor(i["due"]):
            a, b = [c for c in CORRIDORS if c[0] <= i["due"] <= c[1]][0]
            i["due"] = bday_on_or_after(b + dt.timedelta(days=1)) if rng.random() < 0.5 else a - dt.timedelta(days=3)
            while not W.is_bday(i["due"], "UK"):
                i["due"] -= dt.timedelta(days=1)
        if i["kind"] in ("core", "first") and dt.date(2027, 10, 23) <= i["due"] <= dt.date(2027, 11, 26):
            i["due"] = bday_on_or_after(dt.date(2027, 10, 18))
    # withdrawals: a handful of grants in 2025 and 2026
    wd = [g for g in grants if dt.date(2023, 6, 1) <= g["award"] <= dt.date(2026, 3, 31)]
    for g in rng.choice(wd, size=5, replace=False):
        g["status"] = "Withdrawn"
        g["status_date"] = bday_on_or_after(max(g["award"] + dt.timedelta(days=int(rng.integers(200, 500))), dt.date(2025, 2, 3)))
        if g["status_date"] > dt.date(2026, 10, 30):
            g["status_date"] = dt.date(2026, 10, 30)
    pays = []
    for i in inst:
        g = G[i["ref"]]
        if i["kind"] == "later":
            hi = 70
            if i["due"] < dt.date(2026, 10, 23):
                hi = min(hi, max(35, (cut - i["due"]).days))
            ok = [i["due"] + dt.timedelta(days=x) for x in range(35, hi + 1)]
            ok = [x for x in ok if W.is_bday(x, "UK")]
            pay = ok[int(rng.integers(0, len(ok)))]
        else:
            pay = i["due"]
        withdrawn = g["status"] == "Withdrawn" and pay >= g["status_date"]
        i["pay_expected"] = pay
        if pay <= cut and not withdrawn:
            i["status"] = "Paid"
            i["paid"] = pay
            pays.append(i)
        else:
            i["status"] = "Scheduled"
            i["paid"] = None
    for g in grants:
        if g["status"] == "Active" and all(i["status"] == "Paid" for i in inst if i["ref"] == g["ref"]):
            g["status"] = "Closed"
            g["status_date"] = max(i["paid"] for i in inst if i["ref"] == g["ref"])
    return pays


def summary(grants, inst, lag=50):
    """the 2027 grant payments and the hazards' deltas, straight from the generated records"""
    G = {g["ref"]: g for g in grants}
    out = dict(G=0.0, due=0.0, eur_as_gbp=0.0, withdrawn=0.0, lag_all=0.0)
    for i in inst:
        if i["status"] != "Scheduled":
            continue
        g = G[i["ref"]]
        kind = "core" if g["type"] == "Core" else ("first" if i["no"] == 1 else "later")
        conv = W.EUR_RATE if g["currency"] == "EUR" else 1.0
        exp = i["due"] + dt.timedelta(days=lag) if kind == "later" else i["due"]
        if g["status"] != "Withdrawn":
            if exp.year == 2027:
                out["G"] += i["amount"] / conv
                out["eur_as_gbp"] += i["amount"] - i["amount"] / conv
            if i["due"].year == 2027:
                out["due"] += i["amount"] / conv
            if (i["due"] + dt.timedelta(days=lag)).year == 2027:
                out["lag_all"] += i["amount"] / conv
        elif exp.year == 2027:
            out["withdrawn"] += i["amount"] / conv
    return dict(G=out["G"], D8=out["due"] - out["G"], H3=out["eur_as_gbp"], H4=out["withdrawn"], o3=out["lag_all"] - out["G"])
