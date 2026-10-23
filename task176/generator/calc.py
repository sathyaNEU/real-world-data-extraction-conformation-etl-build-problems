"""task176 calculations from the shipped files: the conformed home record (licences, the 2019 crosswalk and the
capacity worksheets), the person-month frame over 2016 to 2026, the golden forecast of 2027 closures and the
routes the checks measure it against. deliver.py and checks.py read this module; verify.py has its own code."""
from __future__ import annotations

import datetime as dt
import os
import warnings

import numpy as np

import common as C

warnings.filterwarnings("ignore")

REL = {"OWN CHILD": "OWN", "C": "OWN", "GRANDCHILD": "GRANDCHILD", "GC": "GRANDCHILD", "FOSTER": "FOSTER",
       "FC": "FOSTER", "OTHER REL": "RELATIVE", "R": "RELATIVE"}
FRAME_FROM = (2016, 1)
FRAME_TO = (2026, 12)


def pdate(s):
    s = s.strip()
    if not s:
        return None
    if "/" in s:
        m, d, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s)


def mon(d):
    return (d.year - 2004) * 12 + d.month - 1


def load(target):
    lic = C.read_csv(os.path.join(target, C.F_LIC))
    xw = {r["legacy_licence_no"]: r["licence_no"] for r in C.read_csv(os.path.join(target, C.F_XW))}
    homes = {}
    for r in lic:
        homes[r["licence_no"]] = dict(
            no=r["licence_no"], first=pdate(r["first_licensed_date"]), close=pdate(r["closure_effective_date"]),
            by=int(r["provider_birth_year"]) if r["provider_birth_year"] else None, county=r["county"],
            ltype=r["licence_type"], kids={})
    for r in C.read_csv(os.path.join(target, C.F_WS)):
        no = xw.get(r["licence_ref"], r["licence_ref"])
        if no not in homes:
            continue
        b = pdate(r["child_birth_date"])
        key = (r["child_initials"].upper(), b)
        homes[no]["kids"][key] = (REL[r["relationship"].strip().upper()], r["lives_in_home"].strip().upper())
    return homes


def own_births(h, rel=("OWN",), in_home=True):
    return sorted(b for (ini, b), (rr, lv) in h["kids"].items() if rr in rel and (lv == "Y" or not in_home))


def frame(homes, start=FRAME_FROM, stop=FRAME_TO, kspec=None):
    """person-months: home index, month, tenure in months, age, event, and the kindergarten flag per kspec"""
    m0, m1 = (start[0] - 2004) * 12 + start[1] - 1, (stop[0] - 2004) * 12 + stop[1] - 1
    cols = {k: [] for k in ("i", "m", "t", "age", "ev", "k", "kany", "has_young", "yc_age", "grandk")}
    keys = sorted(homes)
    for i, no in enumerate(keys):
        h = homes[no]
        lm = mon(h["first"])
        cm = mon(h["close"]) if h["close"] else None
        a = max(lm + 1, m0)
        b = min(cm if cm is not None else m1, m1)
        if b < a:
            continue
        ms = np.arange(a, b + 1)
        cols["i"].append(np.full(len(ms), i))
        cols["m"].append(ms)
        cols["t"].append(ms - lm)
        yr = 2004 + ms // 12
        cols["age"].append(yr - h["by"] if h["by"] else np.full(len(ms), -1))
        cols["ev"].append((ms == cm).astype(float) if cm is not None else np.zeros(len(ms)))
        k, ka, hy, ya, gk = kflags(h, ms, kspec)
        cols["k"].append(k), cols["kany"].append(ka), cols["has_young"].append(hy), cols["yc_age"].append(ya)
        cols["grandk"].append(gk)
    return {k: np.concatenate(v) for k, v in cols.items()}, keys


def kflags(h, ms, kspec=None):
    """per month: the youngest own in-home child's kindergarten summer (or the variant kspec names), any own child's
    kindergarten summer, an own child under six, the youngest's age, a grandchild's kindergarten summer"""
    spec = dict(months=(6, 7, 8), rule="cutoff", rel=("OWN",), in_home=True, whole=False)
    spec.update(kspec or {})
    births = own_births(h, spec["rel"], spec["in_home"])
    allown = own_births(h, ("OWN",), True)
    grands = own_births(h, ("GRANDCHILD",), False)
    yr = 2004 + ms // 12
    mo = ms % 12 + 1
    end = np.array([C.month_start(int(m)).toordinal() for m in ms])  # month start
    mend_true = np.array([C.month_end(int(m)).toordinal() for m in ms])
    k = np.zeros(len(ms))
    ka = np.zeros(len(ms))
    hy = np.zeros(len(ms))
    ya = np.full(len(ms), -1.0)
    gk = np.zeros(len(ms))
    if births:
        bo = np.array([b.toordinal() for b in births])
        ky = np.array([_ky(b, spec["rule"]) for b in births])
        # youngest born by the end of the month: births sorted, so the last one with birth <= month end
        mend = mend_true
        idx = np.searchsorted(bo, mend, side="right") - 1
        ok = idx >= 0
        yk = np.where(ok, ky[np.clip(idx, 0, None)], -1)
        if spec["whole"]:
            k = (ok & (yk == yr)).astype(float)
        else:
            k = (ok & (yk == yr) & np.isin(mo, spec["months"])).astype(float)
    if allown:
        bo = np.array([b.toordinal() for b in allown])
        ky = np.array([C.kyear(b) for b in allown])
        mend = mend_true
        for j in range(len(allown)):
            ka = np.maximum(ka, ((bo[j] <= mend) & (ky[j] == yr) & np.isin(mo, (6, 7, 8))).astype(float))
        idx = np.searchsorted(bo, mend, side="right") - 1
        ok = idx >= 0
        yb = np.where(ok, bo[np.clip(idx, 0, None)], 0)
        ya = np.where(ok, (end - yb) / 365.25, -1.0)
        hy = (ok & (ya < 6)).astype(float)
    if grands:
        bo = np.array([b.toordinal() for b in grands])
        ky = np.array([C.kyear(b) for b in grands])
        mend = mend_true
        idx = np.searchsorted(bo, mend, side="right") - 1
        ok = idx >= 0
        yk = np.where(ok, ky[np.clip(idx, 0, None)], -1)
        gk = (ok & (yk == yr) & np.isin(mo, (6, 7, 8))).astype(float)
    return k, ka, hy, ya, gk


def _ky(b, rule):
    if rule == "cutoff":
        return C.kyear(b)
    if rule == "calyear":
        return b.year + 5
    raise ValueError(rule)


def stock_frame(homes, keys, kspec=None, year=C.FORECAST_YEAR):
    """the 2027 months of every home open at the end of 2026"""
    cols = {k: [] for k in ("i", "m", "t", "age", "ev", "k", "kany", "has_young", "yc_age", "grandk")}
    m0 = (year - 2004) * 12
    ms = np.arange(m0, m0 + 12)
    for i, no in enumerate(keys):
        h = homes[no]
        if h["close"] is not None:
            continue
        lm = mon(h["first"])
        cols["i"].append(np.full(12, i))
        cols["m"].append(ms)
        cols["t"].append(ms - lm)
        cols["age"].append(2004 + ms // 12 - h["by"] if h["by"] else np.full(12, -1))
        cols["ev"].append(np.zeros(12))
        k, ka, hy, ya, gk = kflags(h, ms, kspec)
        cols["k"].append(k), cols["kany"].append(ka), cols["has_young"].append(hy), cols["yc_age"].append(ya)
        cols["grandk"].append(gk)
    return {k: np.concatenate(v) for k, v in cols.items()}


def tband(t, cap=10):
    return np.minimum(t // 12, cap)


def design(F, feats, cap=10):
    tb = tband(F["t"], cap)
    X = [np.ones(len(tb))] + [(tb == b).astype(float) for b in range(1, cap + 1)]
    mo = F["m"] % 12 + 1
    for f in feats:
        if f == "age":
            X.append((F["age"] >= AGE_TERMS[0]).astype(float))
            X.append((F["age"] >= AGE_TERMS[1]).astype(float))
        elif f == "summer":
            X.append(np.isin(mo, (6, 7, 8)).astype(float))
        elif f == "k":
            X.append(F["k"])
        elif f == "kany":
            X.append(F["kany"])
        elif f == "grandk":
            X.append(F["grandk"])
        elif f == "under6":
            X.append(F["has_young"])
        elif f == "ycage":
            ok = F["yc_age"] >= 0
            X.append(ok.astype(float))
            X.append(np.where(ok, np.clip(F["yc_age"], 0, 13), 0))
        elif f == "ycbands":
            a = F["yc_age"]
            for lo, hi in ((0, 2), (2, 4), (4, 5), (5, 6), (6, 13)):
                X.append(((a >= lo) & (a < hi)).astype(float))
        elif f == "y2020":
            yr = 2004 + F["m"] // 12
            X.append(((yr == 2020) & (mo >= 4)).astype(float))
        else:
            raise ValueError(f)
    return np.column_stack(X)


def _agg(X, ev):
    """collapse identical design rows to cells with events and exposure"""
    u, inv = np.unique(X, axis=0, return_inverse=True)
    inv = inv.ravel()
    e = np.bincount(inv, weights=ev, minlength=len(u))
    n = np.bincount(inv, minlength=len(u)).astype(float)
    return u, e, n


def fit_glm(F, feats, link="log", cap=10):
    import statsmodels.api as sm
    X = design(F, feats, cap)
    u, e, n = _agg(X, F["ev"])
    keep = u.std(axis=0) > 0
    keep[0] = True
    if link == "log":
        r = sm.GLM(e, u[:, keep], family=sm.families.Poisson(), exposure=n).fit()
    else:
        r = sm.GLM(np.column_stack([e, n - e]), u[:, keep], family=sm.families.Binomial()).fit()
    return r, keep


def predict_glm(r, keep, S, feats, link="log", cap=10):
    X = design(S, feats, cap)[:, keep]
    if link == "log":
        return np.clip(np.exp(X @ r.params), 0, 0.99)
    return np.clip(1 / (1 + np.exp(-(X @ r.params))), 0, 0.99)


def expected(S, hz):
    order = np.argsort(S["i"], kind="stable")
    ids = S["i"][order]
    lh = np.log1p(-np.clip(hz[order], 0, 0.999))
    _, start = np.unique(ids, return_index=True)
    return float((1 - np.exp(np.add.reduceat(lh, start))).sum())


def glm_route(F, S, feats, link="log", cap=10):
    r, keep = fit_glm(F, feats, link, cap)
    return expected(S, predict_glm(r, keep, S, feats, link, cap)), r


def cell_route(F, S, key):
    ka, ks = key(F), key(S)
    hz = np.zeros(len(ks))
    for v in np.unique(ks):
        sel = ka == v
        hz[ks == v] = F["ev"][sel].sum() / max(sel.sum(), 1)
    return expected(S, hz)


def additive_route(F, S, kcol="k"):
    """non-kindergarten hazard by tenure year, retirement age and summer from the months without the flag, plus the
    flag's mean excess"""
    mo = lambda X: np.isin(X["m"] % 12 + 1, (6, 7, 8)).astype(int)
    key = lambda X: tband(X["t"]) * 12 + (X["age"] >= 63) * 4 + (X["age"] >= 68) * 2 + mo(X)
    ka, ks = key(F), key(S)
    base = {}
    for v in np.unique(ka):
        sel = (ka == v) & (F[kcol] == 0)
        base[v] = F["ev"][sel].sum() / max(sel.sum(), 1)
    bF = np.array([base[v] for v in ka])
    on = F[kcol] == 1
    exc = float((F["ev"][on] - bF[on]).mean())
    hz = np.array([base.get(v, 0.006) for v in ks]) + S[kcol] * exc
    return expected(S, hz), exc


def annual_share_route(homes, keys, F, S):
    """homes open on 1 January of their youngest own child's kindergarten year: the share that closed that year; the
    other homes by tenure year from 1 January"""
    yr = 2004 + F["m"] // 12
    first_jan = (F["m"] % 12 == 0)
    kyr = np.zeros(len(F["i"]), bool)
    # a home-year is a kindergarten year when its January row's youngest own child starts kindergarten that year
    ky_of = {}
    for i, no in enumerate(keys):
        b = own_births(homes[no])
        ky_of[i] = b
    closed_year = {}
    for j in np.where(F["ev"] == 1)[0]:
        closed_year[(int(F["i"][j]), int(yr[j]))] = 1
    kn = kc = 0
    tn, tc = {}, {}
    for j in np.where(first_jan)[0]:
        i, y = int(F["i"][j]), int(yr[j])
        d = dt.date(y, 1, 1)
        bs = [b for b in ky_of[i] if b <= dt.date(y, 8, 31)]
        isk = bool(bs) and C.kyear(max(bs)) == y
        c = closed_year.get((i, y), 0)
        if isk:
            kn += 1
            kc += c
        else:
            band = min(int(F["t"][j]) // 12, 10)
            tn[band] = tn.get(band, 0) + 1
            tc[band] = tc.get(band, 0) + c
    pk = kc / kn
    tot = 0.0
    for i in np.unique(S["i"]):
        sel = S["i"] == i
        if S["k"][sel].max() > 0:
            tot += pk
        else:
            band = min(int(S["t"][sel][0]) // 12, 10)
            tot += tc.get(band, 0) / max(tn.get(band, 1), 1)
    return tot, pk


GOLD_FEATS = ["age", "summer", "k"]
AGE_TERMS = (63, 68)


def golden(target):
    homes = load(target)
    F, keys = frame(homes)
    S = stock_frame(homes, keys)
    g, r = glm_route(F, S, GOLD_FEATS)
    stock = len(np.unique(S["i"]))
    nk = int(len(np.unique(S["i"][S["k"] > 0])))
    on = F["k"] == 1
    # the record's kindergarten-summer homes: those open on 1 June of the summer; the share that closed by 31 August
    starts = set()
    closes = 0
    for j in np.where(on)[0]:
        if F["m"][j] % 12 == 5:
            starts.add((int(F["i"][j]), int(2004 + F["m"][j] // 12)))
    for j in np.where(on & (F["ev"] == 1))[0]:
        if (int(F["i"][j]), int(2004 + F["m"][j] // 12)) in starts:
            closes += 1
    pk = closes / len(starts)
    return dict(golden=g, stock=stock, nk=nk, ksummers=len(starts), kcloses=closes, pk=pk, homes=homes, F=F, S=S,
                keys=keys, fit=r)


def default_route(info):
    F, S = info["F"], info["S"]
    return cell_route(F, S, lambda X: tband(X["t"]))


# ---- the asks, from the shipped files ---------------------------------------------------------------------------

def regions_by_fips(target):
    return {r["county_fips"]: int(r["region_no"]) for r in C.read_csv(os.path.join(target, C.F_CTY))}


def regions_by_name(target):
    out = {}
    for r in C.read_csv(os.path.join(target, C.F_CTY)):
        nm = r["county_name"].replace(" County", "").upper()
        out[nm] = int(r["region_no"])
        out[r["county_name"].upper()] = int(r["region_no"])
    return out


def ask_child_days(target, union=True, drop_void=True, statewide=True):
    """subsidised child-days at family child care homes by half of 2026, statewide (keys 1 and 2) or by region (keys
    (region, half)): each child's weekdays counted once whichever lines and homes cover them (union=False sums every
    line's weekdays)"""
    reg = regions_by_fips(target)
    y0, y1 = dt.date(2026, 1, 1), dt.date(2026, 12, 31)
    sets, sums = {}, {}
    for r in C.read_csv(os.path.join(target, C.F_CCAP)):
        if r["provider_type"] not in ("SFCC", "LFCC"):
            continue
        if drop_void and r["remittance_status"] == "VOID":
            continue
        a, b = dt.date.fromisoformat(r["service_from"]), dt.date.fromisoformat(r["service_to"])
        a, b = max(a, y0), min(b, y1)
        if b < a:
            continue
        g = reg[r["county_fips"]]
        d = a
        while d <= b:
            if d.weekday() < 5:
                k = (1 if d.month <= 6 else 2) if statewide else (g, 1 if d.month <= 6 else 2)
                sets.setdefault(k, set()).add((r["child_no"], d))
                sums[k] = sums.get(k, 0) + 1
            d += dt.timedelta(days=1)
    return {k: len(v) for k, v in sets.items()} if union else sums


MONEY_KEYS = {
    "remittance": lambda r: (r["remittance_no"], r["pay_run_date"], r["county_fips"]),
    "number": lambda r: r["remittance_no"],
    "number_run": lambda r: (r["remittance_no"], r["pay_run_date"]),
    "number_provider": lambda r: (r["remittance_no"], r["provider_no"]),
    "number_amount": lambda r: (r["remittance_no"], r["remittance_amount"]),
    "number_county": lambda r: (r["remittance_no"], r["county_fips"]),
    "provider_amount": lambda r: (r["provider_no"], r["remittance_amount"]),
    "run_provider": lambda r: (r["pay_run_date"], r["provider_no"]),
    "run_provider_amount": lambda r: (r["pay_run_date"], r["provider_no"], r["remittance_amount"]),
    "run_county_amount": lambda r: (r["pay_run_date"], r["county_fips"], r["remittance_amount"]),
    "number_run_amount": lambda r: (r["remittance_no"], r["pay_run_date"], r["remittance_amount"]),
    "number_run_provider": lambda r: (r["remittance_no"], r["pay_run_date"], r["provider_no"]),
}


RATES = {"SFCC": 812.0, "LFCC": 846.0, "CTR": 1138.0, "EXEMPT": 402.0}   # CCAP policy section 5


def month_weekdays(d):
    a = dt.date(d.year, d.month, 1)
    b = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return sum(1 for k in range((b - a).days) if (a + dt.timedelta(days=k)).weekday() < 5)


def line_pay(r):
    """a line's pay at the full-time rate prorated by its days over the month's Monday to Friday days (section 3)"""
    return RATES[r["provider_type"]] * int(r["care_days"]) / month_weekdays(dt.date.fromisoformat(r["service_from"]))


def home_regions(target):
    """licence number -> region of the home, from the licence extract's county"""
    byname = regions_by_name(target)
    return {r["licence_no"]: byname[r["county"].upper()] for r in C.read_csv(os.path.join(target, C.F_LIC))}


def ask_money(target, key="remittance", drop_void=True, region="home", alloc="pay"):
    """money the subsidy paid family child care homes in the 2026 runs by region and quarter of the run date: each
    remittance once (key names what is taken as one remittance; key='lines' sums the amount on every line).
    region='home' credits the region of the home that gave the care: a remittance whose homes lie in one region goes
    there whole, one whose homes lie in several is shared by its lines' pay at the filed rates (alloc='pay'), by their
    care_days (alloc='days') or credited whole to its first line's home (alloc='first'); region='office' credits the
    region of the county office that issued it (county_fips)."""
    reg = regions_by_fips(target)
    home = home_regions(target) if region == "home" else None
    groups = {}
    tot = {}
    for r in C.read_csv(os.path.join(target, C.F_CCAP)):
        if r["provider_type"] not in ("SFCC", "LFCC") or not r["pay_run_date"].startswith("2026"):
            continue
        if drop_void and r["remittance_status"] == "VOID":
            continue
        q = (int(r["pay_run_date"][5:7]) - 1) // 3 + 1
        amt = float(r["remittance_amount"])
        rg = home.get(r["provider_no"], reg[r["county_fips"]]) if home else reg[r["county_fips"]]
        if key == "lines":
            tot[(rg, q)] = tot.get((rg, q), 0.0) + amt
            continue
        k = MONEY_KEYS[key](r)
        g = groups.setdefault(k, {"q": q, "amt": amt, "lines": []})
        g["lines"].append((rg, line_pay(r), int(r["care_days"])))
    for g in groups.values():
        regs = {x[0] for x in g["lines"]}
        if len(regs) == 1 or alloc == "first":
            rg = g["lines"][0][0]
            tot[(rg, g["q"])] = tot.get((rg, g["q"]), 0.0) + g["amt"]
            continue
        w = {}
        for rg, pay, days in g["lines"]:
            w[rg] = w.get(rg, 0.0) + (pay if alloc == "pay" else days)
        sw = sum(w.values())
        for rg, v in w.items():
            tot[(rg, g["q"])] = tot.get((rg, g["q"]), 0.0) + g["amt"] * v / sw
    return {k: round(v, 2) for k, v in tot.items()}


def ask_money_priced(target, drop_void=True):
    """every line priced at the filed full-time rate and summed by the home's region (no remittance amount read)"""
    home = home_regions(target)
    reg = regions_by_fips(target)
    tot = {}
    for r in C.read_csv(os.path.join(target, C.F_CCAP)):
        if r["provider_type"] not in ("SFCC", "LFCC") or not r["pay_run_date"].startswith("2026"):
            continue
        if drop_void and r["remittance_status"] == "VOID":
            continue
        k = (home.get(r["provider_no"], reg[r["county_fips"]]), (int(r["pay_run_date"][5:7]) - 1) // 3 + 1)
        tot[k] = tot.get(k, 0.0) + line_pay(r)
    return {k: round(v, 2) for k, v in tot.items()}


def ask_meals(target, key="sponsor"):
    """meals and snacks claimed for family child care homes by region and half of 2026: each sponsor's latest claim
    for a home and month (key='sponsor'); key='site' keeps one claim per home and month; key='all' sums every claim"""
    reg = regions_by_name(target)
    keep = {}
    rows = [r for r in C.read_csv(os.path.join(target, C.F_CACFP)) if r["site_licence_no"].startswith("FC")]
    out = {}
    if key == "all":
        sel = rows
    else:
        for r in rows:
            k = (r["sponsor_id"], r["site_licence_no"], r["claim_month"]) if key == "sponsor" else (r["site_licence_no"], r["claim_month"])
            if k not in keep or (r["received_date"], r["claim_no"]) > (keep[k]["received_date"], keep[k]["claim_no"]):
                keep[k] = r
        sel = keep.values()
    for r in sel:
        g = reg[r["county_fips"].upper()]
        half = 1 if int(r["claim_month"][5:7]) <= 6 else 2
        out[(g, half)] = out.get((g, half), 0) + sum(int(r[c]) for c in ("breakfasts", "lunches", "suppers", "snacks"))
    return out


def ask_visits(target, key="arrival"):
    """visits inspectors made to family child care homes in 2026 by region, and their hours on site: one visit per
    inspector, home, date and arrival (key='arrival'); key='records' counts every record; key='day' one per home and date"""
    reg = regions_by_name(target)
    seen = {}
    n = 0
    for r in C.read_csv(os.path.join(target, C.F_VIS)):
        if r["facility_type"] not in ("SFCC", "LFCC") or r["status"] != "COMPLETED":
            continue
        a = int(r["arrived"][:2]) * 60 + int(r["arrived"][3:])
        b = int(r["departed"][:2]) * 60 + int(r["departed"][3:])
        n += 1
        k = {"arrival": (r["licence_no"], r["visit_date"], r["inspector_id"], a), "records": n,
             "day": (r["licence_no"], r["visit_date"])}[key]
        seen[k] = (reg[r["county"].upper()], (b - a) / 60.0)
    out = {}
    for g, hrs in seen.values():
        c, t = out.get(g, (0, 0.0))
        out[g] = (c + 1, t + hrs)
    return out


def loglik(F, feats, link="log"):
    """Poisson log-likelihood of a fitted model on the person-month rows themselves (comparable across models)"""
    r, keep = fit_glm(F, feats, link)
    mu = predict_glm(r, keep, F, feats, link)
    y = F["ev"]
    return float((y * np.log(np.clip(mu, 1e-12, None)) - mu).sum()), int(keep.sum())
