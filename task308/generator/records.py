"""Ardenmoor Mutual's records: every home claim with a date of loss from 2010 to 2025 as the claims platform held it on
31 October 2026, the policies in force by postcode district and year, the rebuild cost index, the Major Loss Unit's
monthly reports, the Lowther and Pike scheme's risk bordereaux and the direct book on 31 December 2025.

Each catastrophe, each region-year of everyday claims, the Major Loss Unit and the scheme draw from their own random
streams, so the records of one never move another's."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import params as P
import world as W

ASAT = P.AS_AT
REDATE = 45
NOTICE = 23         # the stream for notice given ahead of the day cover ends
W0 = dt.date(2025, 10, 1)   # the first bordereau month
ADVANCE = 0.075     # the share of scheme terms with a further advance for home improvements
# an everyday claim: (peril, claims a year per policy, mean cost at 2015 prices, spread)
PERIL_ATTR = [("escape of water", 0.0118, 3900.0, 1.08), ("accidental damage", 0.0062, 1150.0, 0.8),
              ("theft", 0.0029, 2300.0, 0.9), ("fire", 0.0011, 14500.0, 1.4), ("subsidence", 0.0007, 9200.0, 1.05),
              ("windstorm", 0.0021, 1300.0, 0.7), ("flood", 0.0003, 9000.0, 1.0), ("freeze", 0.0006, 4100.0, 0.8)]
# everyday claims run at different rates by region (housing stock, ground, town and country) and move from year to
# year: escape of water rising, theft falling and down in the 2020 and 2021 lockdowns, subsidence up in dry summers
REGION_RATE = {"escape of water": {"Fenland": 0.90, "Pennine": 1.14, "Severn Vale": 0.97, "Coastal North": 1.06},
               "accidental damage": {"Fenland": 0.94, "Pennine": 0.97, "Severn Vale": 1.08, "Coastal North": 1.01},
               "theft": {"Fenland": 0.78, "Pennine": 1.09, "Severn Vale": 1.04, "Coastal North": 1.21},
               "fire": {"Fenland": 1.06, "Pennine": 1.03, "Severn Vale": 0.93, "Coastal North": 0.99},
               "subsidence": {"Fenland": 1.55, "Pennine": 0.62, "Severn Vale": 1.24, "Coastal North": 0.71}}


def year_rate(peril, y):
    if peril == "escape of water":
        return 1.0 + 0.018 * (y - 2017)
    if peril == "accidental damage":
        return 1.0 + 0.008 * (y - 2017) + (0.09 if y in (2020, 2021) else 0.0)
    if peril == "theft":
        return math.exp(-0.045 * (y - 2017)) * {2020: 0.72, 2021: 0.86}.get(y, 1.0)
    if peril == "subsidence":
        return {2018: 1.9, 2022: 2.1, 2025: 1.35}.get(y, 1.0)
    return 1.0


# catastrophes the claims team declared only after the first claims were in, with the code it then gave them
LATE_DECLARED = {2: "FLD1204", 10: "WND1501", 17: "FLD1906", 18: "FLD1911"}
# what rebuilding a home costs differs by region (house types, local wages), so sums insured do
SI_REGION = {"Fenland": 0.87, "Pennine": 0.92, "Severn Vale": 1.11, "Coastal North": 0.95}
# how many days a catastrophe's claims are dated over, and how likely each length is
SPAN = {"windstorm": ([1, 2, 3], [0.2, 0.55, 0.25]), "flood": ([3, 4, 5, 6], [0.25, 0.35, 0.25, 0.15]),
        "freeze": ([4, 5, 6], [0.3, 0.45, 0.25])}


def _day_shares(seed, i, peril):
    """share of a catastrophe's claims by day from its start: storms and floods front-loaded, freezes on the thaw;
    each catastrophe's length and fall-off from its own stream, inside the hours clause's period"""
    r = np.random.default_rng([seed, 10, i])
    days, p = SPAN[peril]
    n = int(r.choice(days, p=p))
    k = np.arange(n)
    if peril == "freeze":
        w = np.exp(-0.5 * ((k - 0.45 * (n - 1)) / (0.33 * n)) ** 2)
    else:
        w = r.uniform(*((0.2, 0.45) if peril == "windstorm" else (0.3, 0.55))) ** k
    return w / w.sum()


# days to a signed-off repair by the work a peril brings (drying out, strip-out, monitoring), before the load and the draws
REPAIR_DAYS = {"windstorm": 38, "flood": 64, "freeze": 61, "theft": 24, "accidental damage": 31,
               "escape of water": 57, "fire": 79, "subsidence": 101}


def _claims(seed):
    rows = []
    rota = {}
    lj = np.random.default_rng([seed, 51])     # how soon a firm can start, apart from the claim's own draws

    def add(region, d, peril, loss_date, amount, code, u, cash, r):
        if cash:
            con, sign = "", None
        else:
            ids = W.panel_in(region, loss_date.year)
            k = int(r.integers(0, len(ids)))
            if peril in P.CAT_PERILS:
                # weather work goes round the whole panel before any firm takes a second weather job in the year
                q = rota.setdefault((region, loss_date.year), list(np.random.default_rng(
                    [seed, 49, loss_date.year, W.REGIONS.index(region)]).permutation(len(ids))))
                if q:
                    k = int(q.pop())
            con = ids[k]
            base = REPAIR_DAYS[peril]
            extra = 0.0 if u is None else 2.6 * max(0.0, u - 20.0)
            sign = loss_date + dt.timedelta(days=int(base + extra + r.gamma(2.0, 12.0)) - int(lj.integers(0, 16)))
        rows.append((region, d, peril, loss_date, amount, code, u, cash, con, sign))

    truth = []
    for i, (d0, peril, code, rates) in enumerate(W.EVENTS):
        rng = np.random.default_rng([seed, 7, i])
        prof = np.random.default_rng([seed, 9, i]).dirichlet(40.0 * _day_shares(seed, i, peril))
        start = dt.date.fromisoformat(d0)
        y, m = start.year, start.month
        for rg, rate in rates.items():
            ds = W.DISTRICTS[rg]
            w = W.weights(rg, "flood" if peril == "flood" else ("freeze" if peril == "freeze" else "wind"))
            pol = np.array([W.policies(rg, d, y) for d in ds])
            lam = pol * rate / 1000.0 * w * pol.sum() / (pol * w).sum()
            n_d = rng.poisson(lam)
            n = int(n_d.sum())
            u = n / W.panel_path(rg, y)
            mu = W.BASE_SEV[peril] * W.cost_index(y, m) / 100.0 * W.surge(u)
            sig = {"windstorm": 0.75, "flood": 0.55, "freeze": 0.6}[peril]
            first_row = len(rows)
            for d, k in zip(ds, n_d):
                for _ in range(int(k)):
                    amt = mu * math.exp(rng.normal(0, sig) - sig * sig / 2)
                    ld = start + dt.timedelta(days=int(rng.choice(len(prof), p=prof)))
                    # storm claims are coded at first notice; frozen pipes surface over the following weeks, so
                    # a freeze's claims more often come in late and without the code
                    c = code if (code and rng.random() > (0.16 if peril == "freeze" else 0.03)) else None
                    add(rg, d, peril, ld, amt, c, u, rng.random() < 0.12, rng)
            if i in LATE_DECLARED:
                # the code reaches the claims notified once the event is declared, on its own stream
                rc = np.random.default_rng([seed, 8, i, list(W.REGIONS).index(rg)])
                for j in range(first_row, len(rows)):
                    if rc.random() > 0.03:
                        rows[j] = rows[j][:5] + (LATE_DECLARED[i],) + rows[j][6:]
            truth.append(dict(event=i, start=d0, peril=peril, code=code or LATE_DECLARED.get(i), region=rg, n=n, u=u,
                              mu=mu))
    for y in W.YEARS:
        days = (dt.date(y, 12, 31) - dt.date(y, 1, 1)).days + 1
        for ri, rg in enumerate(W.REGIONS):
            rng = np.random.default_rng([seed, 11, y, ri])
            rt = np.random.default_rng([seed, 12, y, ri])      # the region and year rates, apart from the base draws
            ds = W.DISTRICTS[rg]
            pol = np.array([W.policies(rg, d, y) for d in ds])
            for peril, freq, sev, sig in PERIL_ATTR:
                f = REGION_RATE[peril][rg] * year_rate(peril, y) if peril in P.NONCAT else 1.0
                n = rng.poisson(pol.sum() * freq)
                dd = rng.choice(len(ds), size=n, p=pol / pol.sum())
                doy = rng.integers(0, days, size=n)
                amt = sev * np.array([W.cost_index(y, (int(x) * 12) // days + 1) / 100.0 for x in doy]) * \
                    np.exp(rng.normal(0, sig, n) - sig * sig / 2)
                for k in range(n):
                    add(rg, ds[dd[k]], peril, dt.date(y, 1, 1) + dt.timedelta(days=int(doy[k])), float(amt[k]), None,
                        None, rng.random() < 0.3, rng)
                    if f < 1.0 and rt.random() >= f:
                        rows.pop()
                if f > 1.0:
                    m = int(rt.poisson(pol.sum() * freq * (f - 1.0)))
                    dd2 = rt.choice(len(ds), size=m, p=pol / pol.sum())
                    doy2 = rt.integers(0, days, size=m)
                    amt2 = sev * np.array([W.cost_index(y, (int(x) * 12) // days + 1) / 100.0 for x in doy2]) * \
                        np.exp(rt.normal(0, sig, m) - sig * sig / 2)
                    for k in range(m):
                        add(rg, ds[dd2[k]], peril, dt.date(y, 1, 1) + dt.timedelta(days=int(doy2[k])), float(amt2[k]),
                            None, None, rt.random() < 0.3, rt)
    df = pd.DataFrame(rows, columns=["region", "postcode_district", "peril", "date_of_loss", "incurred", "event_code",
                                     "u", "cash", "repair_contractor", "repair_signed_off"])
    df = df.sort_values(["date_of_loss", "region", "postcode_district"], kind="stable").reset_index(drop=True)
    return df, truth


def _reserve(df, seed):
    """paid and outstanding on 31 October 2026: a claim settles in its own time, longer for a larger claim and not
    before its repair is signed off, so recent claims are still part-reserved"""
    rng = np.random.default_rng([seed, 19])
    age = np.array([(ASAT - d).days for d in df["date_of_loss"]])
    amt = np.maximum(df["incurred"].values, 100.0)
    settle = 50.0 * (amt / 3000.0) ** 0.35 * np.exp(rng.normal(0.0, 0.8, len(df)))
    lag = np.array([(s - d).days if s is not None else 0 for s, d in zip(df["repair_signed_off"], df["date_of_loss"])])
    settle = np.minimum(np.maximum(settle, lag + rng.integers(6, 40, len(df))), 700.0)
    frac_os = np.clip(1.0 - age / settle, 0.0, 1.0) * 0.85
    osr = np.round(df["incurred"].values * frac_os, 2)
    df["paid"] = np.round(df["incurred"].values - osr, 2)
    df["outstanding"] = osr
    late = [s is not None and s > ASAT for s in df["repair_signed_off"]]
    df.loc[late, "repair_signed_off"] = None
    return df


def _refs(df, seed):
    """claim numbers in order of loss; policy numbers drawn from each district's own run of numbers, so a policy
    can claim more than once; notification dates, late notifications usually entered without the event code"""
    rng = np.random.default_rng([seed, 13])
    n = len(df)
    base = {d: 100000000 + 1100000 * k for k, d in enumerate(sorted({d for ds in W.DISTRICTS.values() for d in ds}))}
    span = {d: int(W.policies(rg, d, 2025) * 1.6) for rg, ds in W.DISTRICTS.items() for d in ds}
    df["policy_no"] = ["%09d" % (base[d] + int(rng.integers(0, span[d]))) for d in df["postcode_district"]]
    # one claim a policy for a peril on a day: a second draw for the same day goes to another of the district's policies
    rd = np.random.default_rng([seed, 53])
    col = df.columns.get_loc("policy_no")
    seen = set()
    for i, (pn, per, dol, d) in enumerate(zip(df["policy_no"], df["peril"], df["date_of_loss"], df["postcode_district"])):
        while (pn, per, dol) in seen:
            pn = "%09d" % (base[d] + int(rd.integers(0, span[d])))
            df.iat[i, col] = pn
        seen.add((pn, per, dol))
    df["policy_ref"] = "P" + df["policy_no"]
    r2 = np.random.default_rng([seed, 17])
    lag = np.empty(n, dtype=int)
    is_cat = df["u"].notna().values
    coded_event = df["event_code"].notna().values
    late_cat = is_cat & ~coded_event & (r2.random(n) < 0.85)
    lag[:] = np.round(r2.gamma(1.3, 3.2, n)).astype(int)
    lag[is_cat & coded_event] = np.round(r2.gamma(1.1, 1.4, int((is_cat & coded_event).sum()))).astype(int)
    lag[late_cat] = 15 + np.round(r2.gamma(2.0, 11.0, int(late_cat.sum()))).astype(int)
    df["date_notified"] = [min(d + dt.timedelta(days=int(x)), ASAT) for d, x in zip(df["date_of_loss"], lag)]
    order = np.lexsort((np.arange(n), np.array([d.toordinal() for d in df["date_notified"]])))
    ref = np.empty(n, dtype=int)
    ref[order] = np.arange(n)
    df["claim_ref"] = ["HC%07d" % (1000000 + i) for i in ref]
    return df


def _numbering():
    """each district's own run of nine-digit policy numbers"""
    base = {d: 100000000 + 1100000 * k for k, d in enumerate(sorted({d for ds in W.DISTRICTS.values() for d in ds}))}
    span = {d: int(W.policies(rg, d, 2025) * 1.6) for rg, ds in W.DISTRICTS.items() for d in ds}
    return base, span


def _claims_2026(seed):
    """everyday claims with a date of loss from 1 January to 31 August 2026: outside the extract, but the Major Loss
    Unit's reports carry the large ones"""
    rng = np.random.default_rng([seed, 27])
    base, span = _numbering()
    out = []
    for rg in W.REGIONS:
        ds = W.DISTRICTS[rg]
        pol = np.array([W.policies(rg, d, 2025) for d in ds])
        for peril, freq, sev, sig in PERIL_ATTR:
            if peril not in P.NONCAT:
                continue
            n = int(rng.poisson(pol.sum() * freq * 243 / 365.0))
            dd = rng.choice(len(ds), size=n, p=pol / pol.sum())
            doy = rng.integers(0, 243, size=n)
            z = rng.normal(0, sig, n)
            lag = np.round(rng.gamma(1.3, 3.2, n)).astype(int)
            pn = rng.integers(0, 10 ** 9, n)
            for k in range(n):
                d0 = dt.date(2026, 1, 1) + dt.timedelta(days=int(doy[k]))
                amt = sev * W.cost_index(2026, d0.month) / 100.0 * math.exp(z[k] - sig * sig / 2)
                d = ds[dd[k]]
                out.append(dict(region=rg, postcode_district=d, peril=peril, date_of_loss=d0, incurred=float(amt),
                                date_notified=d0 + dt.timedelta(days=int(lag[k])),
                                policy_no="%09d" % (base[d] + int(pn[k]) % span[d])))
    return out


def _mlu(df, seed):
    """Claims other than windstorm, flood and freeze whose platform reserve passes GBP 75,000 move to the Major Loss
    Unit, which runs them in its own system. The platform keeps the date of loss, paid and reserve it held at handover;
    when the unit closes a claim the platform's reserve is set to nil. A claim whose reserve the unit cuts below
    GBP 70,000 goes back to the home claims team, which carries it on the platform from then on, and leaves the unit's
    report. The unit's adjusters date a leak or a subsidence claim from when the damage began, and the unit's report
    carries that date once the adjuster has fixed it. A closed claim that needs more work is reopened in the unit as a
    new case under a new reference, carrying only the further costs."""
    rng = np.random.default_rng([seed, 21])
    cand = df[df.peril.isin(P.NONCAT) & (df.date_of_loss >= dt.date(2021, 7, 1)) &
              (df.date_of_loss <= dt.date(2025, 12, 31))].index
    est = df.loc[cand, "incurred"].values * rng.uniform(0.5, 1.6, len(cand))
    sel, est = cand[est > 75000.0], est[est > 75000.0]
    adjusters = ["Quenby Adjusting", "Carrow Loss Adjusters", "in-house"]

    def case(rng, true, e0, notified):
        ho = notified + dt.timedelta(days=int(rng.integers(6, 62)))
        cl = ho + dt.timedelta(days=int(rng.gamma(3.0, 150.0)) + 30)
        ret = None
        if true < 72000.0:
            ret = ho + dt.timedelta(days=int(rng.integers(60, 300)))
            cl = ret
        ppaid = round(min(true, e0) * rng.uniform(0.08, 0.22), 2)
        pres = round(max(e0 - ppaid, 1000.0), -2)
        return dict(handover=ho, close=cl, ret=ret, true=true,
                    target=(max(true * rng.uniform(1.08, 1.35), 70500.0) if ret else true),
                    est=ppaid + pres, ppaid=ppaid, pres=pres, noise=rng.normal(0, 0.06, 64),
                    adjuster=adjusters[int(rng.integers(0, 3))], dol2=None, redate=None, parent=None, kind="claim")

    recs = []
    for i, e0 in zip(sel, est):
        r = df.loc[i]
        rc = case(rng, float(r.incurred), e0, r.date_notified)
        rc.update(idx=i, pno=r.policy_no, dist=r.postcode_district, peril=r.peril, dol=r.date_of_loss, region=r.region)
        recs.append(rc)
    r26 = np.random.default_rng([seed, 29])
    for x in _claims_2026(seed):
        e0 = x["incurred"] * r26.uniform(0.5, 1.6)
        if e0 <= 75000.0:
            continue
        rc = case(r26, x["incurred"], e0, x["date_notified"])
        if rc["handover"] > ASAT:
            continue
        rc.update(idx=None, pno=x["policy_no"], dist=x["postcode_district"], peril=x["peril"], dol=x["date_of_loss"],
                  region=x["region"])
        recs.append(rc)
    # the adjuster's date for a leak or a subsidence claim
    r3 = np.random.default_rng([seed, 23, REDATE])
    for rc in recs:
        if rc["peril"] in ("escape of water", "subsidence") and rc["ret"] is None and r3.random() < 0.65:
            back = int(r3.integers(14, 200)) if rc["peril"] == "escape of water" else int(r3.integers(30, 300))
            when = rc["handover"] + dt.timedelta(days=int(r3.integers(25, 170)))
            if when < rc["close"] and dt.date(2023, 3, 1) <= when <= ASAT:
                rc["dol2"], rc["redate"] = rc["dol"] - dt.timedelta(days=back), when

    def dol_at(rc, day):
        return rc["dol2"] if (rc["dol2"] is not None and day >= rc["redate"]) else rc["dol"]

    # reopened cases: at least one in each region and loss year 2023 to 2025, and a few more
    r4 = np.random.default_rng([seed, 25])
    closed = [rc for rc in recs if rc["ret"] is None and rc["close"] <= ASAT - dt.timedelta(days=90)]
    pick = set()
    for rg in W.REGIONS:
        for y in (2023, 2024, 2025):
            pool = [k for k, rc in enumerate(closed) if rc["region"] == rg and dol_at(rc, ASAT).year == y]
            if pool:
                pick.add(pool[int(r4.integers(0, len(pool)))])
    for k in range(len(closed)):
        if r4.random() < 0.03:
            pick.add(k)
    reopen = []
    for k in sorted(pick):
        rc = closed[k]
        lo = 45
        hi = (ASAT - rc["close"]).days - 20
        if hi <= lo:
            continue
        ro = rc["close"] + dt.timedelta(days=int(r4.integers(lo, min(hi, 420))))
        extra = float(r4.uniform(22000.0, 65000.0))
        e0 = extra * float(r4.uniform(0.8, 1.25))
        cl = ro + dt.timedelta(days=int(r4.gamma(2.0, 90.0)) + 20)
        ppaid = round(e0 * float(r4.uniform(0.0, 0.1)), 2)
        nc = dict(handover=ro, close=cl, ret=None, true=extra, target=extra, est=e0, ppaid=ppaid,
                  pres=round(max(e0 - ppaid, 500.0), -2), noise=r4.normal(0, 0.05, 64), adjuster=rc["adjuster"],
                  dol2=None, redate=None, parent=rc, kind="reopened", idx=None, pno=rc["pno"], dist=rc["dist"],
                  peril=rc["peril"], dol=dol_at(rc, ro), region=rc["region"])
        reopen.append(nc)
    recs += reopen
    # references in the order cases reach the unit
    seq = {}
    for rc in sorted(recs, key=lambda q: (q["handover"], q["pno"], q["kind"])):
        yy = rc["handover"].year % 100
        seq[yy] = seq.get(yy, 0) + 1
        rc["ref"] = "MLU-%02d-%04d" % (yy, seq[yy])

    def incurred_at(rc, day):
        if rc["ret"] is None and day >= rc["close"]:
            return rc["true"]
        f = (day - rc["handover"]).days / max(1, (rc["close"] - rc["handover"]).days)
        q = min(int(f * 8), 7)
        base = rc["est"] + (rc["target"] - rc["est"]) * min(1.0, (q + 1) / 8.0)
        return max(round(base * (1 + rc["noise"][q] * (1 - q / 8.0)), -2), rc["ppaid"] + 500.0)

    def paid_at(rc, day, inc):
        if rc["ret"] is None and day >= rc["close"]:
            return rc["true"]
        f = (day - rc["handover"]).days / max(1, (rc["close"] - rc["handover"]).days)
        return round(min(0.92, 0.15 + 0.8 * f) * inc, 2)

    sheets = []
    y, m = 2023, 1
    while (y, m) <= (2026, 10):
        ms = dt.date(y, m, 1)
        me = dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
        rows = []
        for rc in recs:
            if rc["handover"] > me:
                continue
            if rc["ret"] is not None:
                if rc["ret"] <= me:
                    continue
                closed_, day = False, me
            else:
                if rc["close"] < ms:
                    continue
                closed_ = rc["close"] <= me
                day = rc["close"] if closed_ else me
            inc = incurred_at(rc, day)
            pd_ = paid_at(rc, day, inc)
            rows.append((rc["ref"], rc["pno"], rc["dist"], rc["peril"].capitalize(), dol_at(rc, day),
                         rc["handover"], rc["adjuster"], round(pd_, 2), round(inc - pd_, 2), round(inc, 2),
                         "Closed" if closed_ else "Open"))
        rows.sort(key=lambda t: t[0])
        sheets.append((ms, me, pd.DataFrame(rows, columns=[
            "MLU reference", "Policy number", "Postcode district", "Peril", "Date of loss", "Transferred to MLU",
            "Loss adjuster", "Paid to date", "Outstanding", "Incurred", "Status"])))
        y, m = (y + (m == 12), m % 12 + 1)
    # the truth: each claim's incurred on 31 October 2026 and the date its damage began
    truth = {}
    extra_claims = []
    df["mlu"] = False
    df["mlu_returned"] = False
    df["dol_true"] = df["date_of_loss"]
    further = {}
    for rc in reopen:
        further[id(rc["parent"])] = further.get(id(rc["parent"]), 0.0) + (incurred_at(rc, ASAT) if rc["close"] > ASAT
                                                                         else rc["true"])
    for rc in recs:
        if rc["kind"] != "claim":
            continue
        if rc["ret"] is not None and rc["ret"] <= ASAT:
            inc = None
        else:
            inc = (incurred_at(rc, ASAT) if rc["close"] > ASAT else rc["true"]) + further.get(id(rc), 0.0)
        dol = dol_at(rc, ASAT)
        i = rc["idx"]
        if i is None:
            if inc is not None:
                extra_claims.append(dict(region=rc["region"], peril=rc["peril"], date_of_loss=dol, incurred=inc,
                                         ref=rc["ref"]))
            continue
        df.loc[i, "mlu"] = True
        df.loc[i, "dol_true"] = dol
        if inc is None:
            df.loc[i, "mlu_returned"] = True
            truth[i] = float(df.loc[i, "paid"] + df.loc[i, "outstanding"])
            continue
        truth[i] = inc
        df.loc[i, "paid"] = rc["ppaid"]
        df.loc[i, "outstanding"] = 0.0 if rc["close"] <= ASAT else rc["pres"]
    return df, sheets, truth, recs, extra_claims


def _scheme(seed):
    """Homes insured through the Lowther and Pike Building Society, bound by Tellwright Underwriting under a delegated
    authority and reported in a monthly risk bordereau. A bordereau lists every term in force at some time in its
    month as the coverholder knew it at the month end, and every cancellation processed in the month with its effective
    date. The society sends its redemptions file on the 10th of each month, so a policy cancelled because the mortgage
    was redeemed is processed in the following month. A policy cancelled for a missed direct debit is reinstated
    without a break when the customer pays within the month; a customer moving to the society's fuller cover is
    rewritten onto a new twelve-month term from the day of the change, under the same policy number."""
    rng = np.random.default_rng([seed, 31])
    rw_rng = np.random.default_rng([seed, 33])
    ri_rng = np.random.default_rng([seed, 35])
    fd_rng = np.random.default_rng([seed, 37, NOTICE])
    fa_rng = np.random.default_rng([seed, 39])
    share = {"Severn Vale": 0.016, "Pennine": 0.031, "Coastal North": 0.012, "Fenland": 0.015}
    BM = [(2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2)]
    DD = dt.date(2025, 12, 31)
    rows, truth = [], {}
    pid = 400000
    ptypes = ["Detached house", "Semi-detached house", "Terraced house", "Bungalow", "Flat"]
    for rg, ds in W.DISTRICTS.items():
        for d in ds:
            n = int(round(W.policies(rg, d, 2025) * share[rg]))
            for _ in range(n):
                pid += int(rng.integers(1, 9))
                first = dt.date(2022, 1, 1) + dt.timedelta(days=int(rng.integers(0, 4 * 365 + 58)))
                if (first.month, first.day) == (1, 1):
                    first += dt.timedelta(days=1)
                si = int(round(rng.lognormal(math.log(268000), 0.30) * SI_REGION[rg], -3))
                prem = round(si * rng.uniform(0.0011, 0.0016), 2)
                ptype = ptypes[int(rng.choice(5, p=[0.22, 0.31, 0.27, 0.08, 0.12]))]
                no = "LP%07d" % pid
                terms, s, alive, rewritten = [], first, True, False
                while s <= dt.date(2026, 2, 28) and alive:
                    e = dt.date(s.year + 1, s.month, min(s.day, 28)) - dt.timedelta(days=1)
                    canc = proc = reason = rein = None
                    if rng.random() < 0.09:
                        c = s + dt.timedelta(days=int(rng.integers(15, 365)))
                        if c <= e and c not in (dt.date(2025, 12, 31), dt.date(2026, 1, 1)):
                            canc = c
                            if rng.random() < 0.62:
                                reason = "Mortgage redeemed"
                                proc = dt.date(c.year + (c.month == 12), c.month % 12 + 1, 10)
                            else:
                                reason = "Customer request" if rng.random() < 0.7 else "Non-payment"
                                proc = canc + dt.timedelta(days=int(rng.integers(0, 4)))
                                # a customer moving to another insurer often gives notice ahead of the day cover ends
                                if reason == "Customer request" and fd_rng.random() < 0.45:
                                    proc = max(s, canc - dt.timedelta(days=int(fd_rng.integers(6, 46))))
                                    # a notice for a day inside the bordereaux is keyed inside them, so no term
                                    # leaves the bordereaux without its cancellation row
                                    if proc < W0 <= canc:
                                        proc = W0 + (canc - W0) // 2
                    mta = None
                    if rng.random() < 0.07:   # an endorsement: an extension or a revaluation the customer asked for
                        eff = s + dt.timedelta(days=int(rng.integers(20, 350)))
                        if eff <= e and (canc is None or eff < canc) and eff not in (dt.date(2025, 12, 31), dt.date(2026, 1, 1)):
                            lead = int(rng.integers(5, 50)) if rng.random() < 0.45 else -int(rng.integers(0, 12))
                            mproc = eff - dt.timedelta(days=lead)
                            mta = dict(eff=eff, proc=max(mproc, s), fac=float(rng.uniform(1.08, 1.32)))
                    stop = canc is not None or rng.random() < 0.10
                    # a missed direct debit paid up within the month: the term carries on as if never cancelled
                    if reason == "Non-payment" and dt.date(2025, 9, 25) <= proc <= dt.date(2025, 12, 22) \
                            and ri_rng.random() < 0.55:
                        rein = proc + dt.timedelta(days=int(ri_rng.integers(2, 9)))
                        stop = ri_rng.random() < 0.10
                    # a rewrite onto the fuller cover: the term ends the day before, a new term starts that day
                    rw = None
                    if canc is None and mta is None and rw_rng.random() < 0.035:
                        x = s + dt.timedelta(days=int(rw_rng.integers(30, 330)))
                        if x <= e and x not in (dt.date(2025, 12, 31), dt.date(2026, 1, 1)):
                            rw = x
                            canc, reason = x, "Customer request"
                            proc = x + dt.timedelta(days=int(rw_rng.integers(0, 5)))
                            stop = False
                    # a further advance from the society for home improvements: the society tells the coverholder when
                    # it lends, and the sum insured rises from the day the works are finished, two to five months on
                    if mta is None and fa_rng.random() < ADVANCE:
                        adv = max(s + dt.timedelta(days=int(fa_rng.integers(10, 300))),
                                  terms[-1]["proc"] if rewritten else s)
                        eff = adv + dt.timedelta(days=int(fa_rng.integers(60, 151)))
                        if eff <= e and (canc is None or eff < canc) and eff not in (dt.date(2025, 12, 31),
                                                                                     dt.date(2026, 1, 1)):
                            if adv < W0 and DD < eff:
                                adv = W0 + (eff - W0) // 4     # keyed inside the bordereaux when it outlasts the year
                            mta = dict(eff=eff, proc=adv, fac=float(fa_rng.uniform(1.10, 1.35)))
                    terms.append(dict(start=s, end=e, canc=canc, proc=proc, reason=reason, rein=rein, rw=rw,
                                      first=(s == first) or rewritten, keyed=(terms[-1]["proc"] if rewritten else s),
                                      mta=mta, up=(float(rw_rng.uniform(1.06, 1.25)) if rw else None)))
                    if stop:
                        alive = False
                    rewritten = rw is not None
                    s = rw if rw is not None else e + dt.timedelta(days=1)
                tsi, tprem = si, prem
                for k, t in enumerate(terms):
                    renewed = k + 1 < len(terms) and terms[k]["rw"] is None
                    if k > 0:
                        if terms[k - 1]["rw"] is not None:
                            tsi = int(round(tsi * terms[k - 1]["up"], -3))
                            tprem = round(tprem * (terms[k - 1]["up"] + 0.05), 2)
                        else:
                            tsi = int(round(tsi * 1.04, -3))      # index-linked at each renewal
                    t["si"] = tsi
                    if t["mta"] is not None:      # an endorsement raises the term's own sum insured
                        t["mta"]["si"] = int(round(tsi * t["mta"]["fac"], -3))
                    for (by, bm) in BM:
                        ms = dt.date(by, bm, 1)
                        me = dt.date(by + (bm == 12), bm % 12 + 1, 1) - dt.timedelta(days=1)
                        mt = t["mta"]
                        # the coverholder's system holds one sum insured a term, overwritten when an endorsement is
                        # processed; the month's own listing is taken before that month's endorsements are keyed
                        cur = mt["si"] if (mt is not None and mt["proc"] < ms) else tsi
                        if t["proc"] is not None and ms <= t["proc"] <= me:
                            rows.append(("%d-%02d" % (by, bm), no, d, ptype, "Cancelled", t["start"], t["end"],
                                         t["canc"], t["reason"], None, cur, tprem))
                        # listed when in force at any time in the month, as the coverholder held it at the month end
                        dead = t["proc"] is not None and t["proc"] <= me and not (t["rein"] is not None and t["rein"] <= me)
                        last = t["canc"] - dt.timedelta(days=1) if dead else t["end"]
                        if t["keyed"] > me or t["start"] > me or last < ms:
                            continue
                        if mt is not None and ms <= mt["proc"] <= me:
                            rows.append(("%d-%02d" % (by, bm), no, d, ptype, "Mid-term adjustment", t["start"], t["end"],
                                         None, None, mt["eff"], mt["si"], tprem))
                        if ms <= t["start"] <= me:
                            tx = "New business" if t["first"] else "Renewal"
                        elif ms <= t["end"] <= me and not dead:
                            tx = "Renewed" if renewed else "Lapsed"
                        else:
                            tx = "In force"
                        rows.append(("%d-%02d" % (by, bm), no, d, ptype, tx, t["start"], t["end"], None, None, None, cur,
                                     tprem))
                for t in terms:
                    eff_end = t["end"] if (t["canc"] is None or t["rein"] is not None) else t["canc"] - dt.timedelta(days=1)
                    if t["start"] <= DD <= eff_end:
                        mt = t["mta"]
                        truth[no] = (rg, d, mt["si"] if (mt is not None and mt["eff"] <= DD) else t["si"],
                                     "reinstated" if t["rein"] else ("rewritten" if (t["first"] and t["start"] != first) else ""))
    B = pd.DataFrame(rows, columns=["bordereau_month", "scheme_policy_no", "postcode_district", "property_type",
                                    "transaction", "term_start", "term_end", "cancellation_effective",
                                    "cancellation_reason", "endorsement_effective", "buildings_sum_insured",
                                    "annual_premium"])
    B = B.sort_values(["bordereau_month", "scheme_policy_no", "term_start"], kind="stable").reset_index(drop=True)
    return B, truth


def build(seed=P.SEED):
    df, ev_truth = _claims(seed)
    df = _reserve(df, seed)
    df = _refs(df, seed)
    df, mlu_sheets, mlu_truth, mlu_recs, mlu_extra = _mlu(df, seed)
    df["inc_true"] = df["incurred"]
    for i, v in mlu_truth.items():
        df.loc[i, "inc_true"] = v
    df["status"] = np.where(df["outstanding"] > 0, "Open", "Closed")
    rng = np.random.default_rng([seed, 41])
    jit = np.random.default_rng([seed, 43, 18])
    ex = []
    for y in W.YEARS:
        for rg in W.REGIONS:
            for d in W.DISTRICTS[rg]:
                p = W.policies(rg, d, y)
                ex.append((y, rg, d, int(round(p * (1.0 + jit.uniform(-0.006, 0.006)))),
                           int(round(p * (238000 + 4200 * (y - 2010)) * SI_REGION[rg]
                                     * rng.uniform(0.97, 1.03) / 1e3)) * 1000))
    EX = pd.DataFrame(ex, columns=["year", "region", "postcode_district", "policies_in_force_mid_year",
                                   "sums_insured_buildings_gbp"])
    BDX, sch_truth = _scheme(seed)
    sch_cnt = {}
    for no, (rg, d, si, _) in sch_truth.items():
        sch_cnt[d] = sch_cnt.get(d, 0) + 1
    dr = []
    for rg in W.REGIONS:
        for d in W.DISTRICTS[rg]:
            tot = 0.5 * (W.policies(rg, d, 2025) + W.policies(rg, d, 2026))
            n_dir = int(round(tot - sch_cnt.get(d, 0)))
            si_d = int(round(n_dir * (238000 + 4200 * 15.5) * SI_REGION[rg] * rng.uniform(0.97, 1.03) / 1e3)) * 1000
            dr.append((rg, d, n_dir, si_d, int(round(n_dir * rng.uniform(0.11, 0.17)))))
    DR = pd.DataFrame(dr, columns=["region", "postcode_district", "policies_in_force", "buildings_sums_insured_gbp",
                                   "policies_over_400k"])
    fr = []
    for rg in W.REGIONS:
        for d in W.DISTRICTS[rg]:
            sv = int(W.policies(rg, d, 2024) * rng.uniform(0.004, 0.012))
            fr.append((rg, d, sv, int(sv * rng.uniform(0.05, 0.22)), int(sv * rng.uniform(0.02, 0.10)),
                       int(sv * rng.uniform(0.10, 0.35))))
    FR = pd.DataFrame(fr, columns=["region", "postcode_district", "homes_surveyed", "flood_doors_or_barriers",
                                   "non_return_valves", "raised_sockets_or_services"])
    # the index as the house publishes it: its monthly movements are uneven about the cost of rebuilding
    wob = np.random.default_rng([seed, 47])
    w, pub = 0.0, []
    for y in range(2010, 2027):
        for m in range(1, 13):
            if y == 2026 and m > 9:
                continue
            w = 0.75 * w + wob.normal(0.0, 0.0025)
            pub.append((y, m, round(W.cost_index(y, m) * math.exp(w), 1)))
    CI = pd.DataFrame(pub, columns=["year", "month", "index"])
    return dict(claims=df, events=ev_truth, exposure=EX, mlu_sheets=mlu_sheets, mlu_truth=mlu_truth,
                mlu_recs=mlu_recs, mlu_extra=mlu_extra, bdx=BDX, scheme_truth=sch_truth, direct=DR, flood=FR, index=CI)
