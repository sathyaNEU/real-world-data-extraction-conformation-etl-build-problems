"""The golden from the shipped files alone: the 2027 permit forecast for the three areas, the fiscal 2026 new
connections by phase and quarter, the fiscal 2026 capacity fee receipts by quarter, and the routes the ladder and
the checks price. Reads only <target>/."""
from __future__ import annotations

import csv
import datetime as dt
import os
import re
from collections import defaultdict

import numpy as np

import common as C

FORWARD = ["North 6", "North 7", "Northwest 3"]
EXACT = [True]      # the filed estimand: expected distinct lots permitted, 1 - exp(-cumulative rate) per lot
SUFFIX_ABBR = {"STREET": "ST", "TERRACE": "TER", "PLACE": "PL", "LANE": "LN", "COURT": "CT", "WAY": "WAY"}


def _csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _mdy(s):
    if not s:
        return None
    m, d, y = s.split("/")
    return dt.date(int(y), int(m), int(d))


def _iso(s):
    return dt.date.fromisoformat(s) if s else None


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        return "\n".join((p.extract_text() or "") for p in pdf.pages)


def schedule(target):
    txt = pdf_text(os.path.join(target, C.F_SCHED))
    areas = {}
    mon = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
    for line in txt.splitlines():
        m = re.match(r"^((?:Southwest|Central|North|Northwest) \d) (\d) ([\d, ]+?) ([\d,]+) (scheduled |planned )?(\d{1,2} \w{3} \d{4}|\d{4})$", line.strip())
        if not m:
            continue
        name, ph, units, lots, kind, when = m.groups()
        if re.match(r"\d{4}$", when):
            acc = None
        else:
            dd, mm, yy = when.split()
            acc = dt.date(int(yy), mon[mm], int(dd))
        areas[name] = dict(phase=ph, units=[int(x) for x in units.replace(" ", "").split(",")], lots=int(lots.replace(",", "")),
                           accepted=acc, planned=(kind or "").strip())
    m = re.search(r"plat\s+units\s+(\d+)\s+to\s+(\d+)", txt)
    core_units = list(range(int(m.group(1)), int(m.group(2)) + 1))
    return areas, core_units


def norm_addr(a):
    a = re.sub(r"\s+", " ", a.strip().upper())
    parts = a.rsplit(" ", 1)
    if len(parts) == 2 and parts[1] in SUFFIX_ABBR:
        a = parts[0] + " " + SUFFIX_ABBR[parts[1]]
    return a


class Pack:
    """the shipped files, parsed"""

    def __init__(self, target):
        self.t = target
        self.areas, self.core_units = schedule(target)
        roll = _csv(os.path.join(target, C.F_ROLL))
        self.strap = np.array([r["STRAP"] for r in roll], dtype=object)
        self.addr = np.array([r["SITE_ADDR"] for r in roll], dtype=object)
        self.unit = np.array([int(re.search(r"UNIT (\d+)", r["LEGAL_DESC"]).group(1)) for r in roll])
        self.block = np.array([int(re.search(r"BLK (\d+)", r["LEGAL_DESC"]).group(1)) for r in roll])
        self.canal = np.array([r["WATERFRONT"] == "Y" for r in roll])
        self.yb = np.array([int(r["YR_BUILT"]) if r["YR_BUILT"] else 0 for r in roll])
        self.N = len(roll)
        self.ix = {s: i for i, s in enumerate(self.strap)}
        self.ix_addr = {a: i for i, a in enumerate(self.addr)}
        unit_area = {}
        for nm, a in self.areas.items():
            for u in a["units"]:
                unit_area[u] = nm
        for u in self.core_units:
            unit_area[u] = "Core"
        self.area = np.array([unit_area[u] for u in self.unit], dtype=object)
        # street segment: street name and hundred-block of the site address (both sides of the street)
        num = np.array([int(a.split(" ", 1)[0]) for a in self.addr])
        street = np.array([a.split(" ", 1)[1] for a in self.addr], dtype=object)
        keys = {}
        self.seg = np.array([keys.setdefault((s, n // 100), len(keys)) for s, n in zip(street, num)])
        self.nseg = len(keys)
        self.seg_n = np.bincount(self.seg, minlength=self.nseg)
        self._permits()

    def _permits(self):
        t = self.t
        leg = _csv(os.path.join(t, C.F_PLEG))
        from openpyxl import load_workbook
        wb = load_workbook(os.path.join(t, C.F_PNEW), read_only=True)
        ws = wb.worksheets[0]
        it = ws.iter_rows(values_only=True)
        head = list(next(it))
        new = [dict(zip(head, r)) for r in it]
        migrated = set(r["Legacy Permit #"] for r in new if r["Legacy Permit #"])
        issue = {}
        co = {}
        nlist = []
        for r in leg:
            if r["PERMIT_TYPE"] != "RES NEW SFR" or r["PERMIT_NBR"] in migrated:
                continue
            i = self.ix_addr[norm_addr(r["SITE_ADDR"])]
            nlist.append((i, _mdy(r["ISSUE_DT"]), _mdy(r["FINAL_DT"]), r["PERMIT_NBR"]))
        for r in new:
            if r["Work Class"] != "Residential New Single Family":
                continue
            i = self.ix[r["Parcel ID"]]
            iss = r["Issued Date"].date() if isinstance(r["Issued Date"], dt.datetime) else r["Issued Date"]
            c = r["CO Issued"]
            c = c.date() if isinstance(c, dt.datetime) else c
            nlist.append((i, iss, c, r["Permit Number"]))
        self.sf_permits = nlist
        for i, iss, c, _ in nlist:
            if i not in issue or iss < issue[i]:
                issue[i] = iss
                co[i] = c
        self.issue = issue
        self.co = co


def season_shares(P):
    """monthly shares of single-family permits in fully served lot-years, from the record"""
    cnt = np.zeros(12)
    for i, iss, c, _ in P.sf_permits:
        a = P.area[i]
        acc = None if a == "Core" else P.areas[a]["accepted"]
        if a == "Core" or (acc is not None and acc.year < iss.year):
            cnt[iss.month - 1] += 1
    return cnt / cnt.sum()


def served_weight(acc, year, season, mdays):
    if acc is None:
        return 0.0
    if acc.year < year:
        return 1.0
    if acc.year > year:
        return 0.0
    m = acc.month - 1
    dim = mdays(year, acc.month)
    return float(season[m + 1:].sum() + season[m] * (dim - acc.day + 1) / dim)


def _mdays(y, m):
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return (nxt - dt.date(y, m, 1)).days


def completed_by(P, day):
    """homes standing (completed) before the given day: the roll's year built, or the certificate of occupancy"""
    done = (P.yb > 0) & (P.yb < day.year)
    for i, c in P.co.items():
        if c is not None and c < day:
            done[i] = True
    return done


def lot_years(P, season, neighbourhood="street", years=range(2008, 2027)):
    """served vacant lot-years: exposure (seasonal weight served and before the permit), event, canal, the
    homes standing on the lot's street at 1 January (or the alternative neighbourhood)"""
    issue_day = np.array([P.issue.get(i, dt.date(2100, 1, 1)) for i in range(P.N)], dtype=object)
    pre = (P.yb > 0) & np.array([i not in P.issue for i in range(P.N)])
    cum = np.concatenate([[0], np.cumsum(season)])
    acc = np.array([None if a == "Core" else P.areas[a]["accepted"] for a in P.area], dtype=object)
    out = defaultdict(list)
    for y in years:
        jan1 = dt.date(y, 1, 1)
        done = completed_by(P, jan1)
        cnt = neighbourhood_count(P, done, neighbourhood)
        vac = ~pre & np.array([d >= jan1 for d in issue_day])
        for i in np.where(vac)[0]:
            a = acc[i]
            core = P.area[i] == "Core"
            if not core and (a is None or a.year > y):
                continue
            # served from the acceptance day
            if core or a.year < y:
                s0 = 0.0
            else:
                dim = _mdays(y, a.month)
                s0 = cum[a.month - 1] + season[a.month - 1] * (a.day - 1) / dim
            d = issue_day[i]
            if d.year == y:
                dim = _mdays(y, d.month)
                e0 = cum[d.month - 1] + season[d.month - 1] * d.day / dim
                ev = (core or a.year < y or d >= a)
            else:
                e0 = 1.0
                ev = False
            exp = max(e0 - s0, 0.0)
            if exp <= 0 and not ev:
                continue
            out["y"].append(y); out["exp"].append(max(exp, 1e-6)); out["ev"].append(1.0 if ev else 0.0)
            out["canal"].append(int(P.canal[i])); out["n"].append(cnt[i]); out["lot"].append(i)
    return {k: np.array(v) for k, v in out.items()}


def neighbourhood_count(P, done, kind):
    if kind == "street":
        return np.bincount(P.seg, weights=done.astype(float), minlength=P.nseg)[P.seg]
    if kind == "block":
        nb = P.block.max() + 1
        return np.bincount(P.block, weights=done.astype(float), minlength=nb)[P.block]
    raise ValueError(kind)


COUNT_BINS = np.array([1, 2, 3, 4, 6, 9, 13, 18])     # homes on the street: 0, 1, 2, 3, 4-5, 6-8, 9-12, 13-17, 18+


def fit_poisson(LY, groups, ng):
    """multiplicative Poisson: year effect x canal effect x group effect, exposure in served seasonal weight"""
    yrs = np.unique(LY["y"]); yi = np.searchsorted(yrs, LY["y"])
    X, E, Cn = LY["exp"], LY["ev"], LY["canal"]
    ye = np.ones(len(yrs)); ce = np.ones(2); ge = np.ones(ng)
    for _ in range(200):
        den = np.bincount(groups, weights=X * ye[yi] * ce[Cn], minlength=ng)
        ge = np.where(den > 0, np.bincount(groups, weights=E, minlength=ng) / np.maximum(den, 1e-300), 0.0)
        den = np.bincount(Cn, weights=X * ye[yi] * ge[groups], minlength=2)
        ce = np.bincount(Cn, weights=E, minlength=2) / den
        ce = ce / ce[0]
        den = np.bincount(yi, weights=X * ce[Cn] * ge[groups], minlength=len(yrs))
        ye = np.bincount(yi, weights=E, minlength=len(yrs)) / den
    mu = X * ye[yi] * ce[Cn] * ge[groups]
    ll = float(np.sum(E * np.log(np.maximum(mu, 1e-300)) - mu))
    return dict(zip(yrs.tolist(), ye)), ce, ge, ll


def forward_lots(P):
    jan27 = dt.date(2027, 1, 1)
    fw = np.isin(P.area, FORWARD) & (P.yb == 0) & np.array([i not in P.issue for i in range(P.N)])
    return np.where(fw)[0]


def unserved_rate(P):
    """permits per vacant lot-year on unserved lots (well and septic), 2023 to 2026"""
    n = d = 0
    issue_y = {i: v.year for i, v in P.issue.items()}
    unserved = np.array([a != "Core" and (P.areas[a]["accepted"] is None or P.areas[a]["accepted"].year > 2026)
                         for a in P.area])
    for y in (2023, 2024, 2025, 2026):
        vac = unserved & (P.yb == 0) & np.array([issue_y.get(i, 9999) >= y for i in range(P.N)])
        d += vac.sum()
        n += sum(1 for i in np.where(unserved)[0] if issue_y.get(i) == y)
    return n / d


def forecast(P, season=None, groups_fn=None, neighbourhood="street", level_years=(2026,), LY=None):
    """the golden family: lot-years binned on the homes standing on the lot's street"""
    season = season_shares(P) if season is None else season
    LY = lot_years(P, season, neighbourhood) if LY is None else LY
    gfn = groups_fn or (lambda n: np.digitize(n, COUNT_BINS))
    groups = gfn(LY["n"])
    ng = int(groups.max()) + 1
    ye, ce, ge, ll = fit_poisson(LY, groups, ng)
    lvl = float(np.mean([ye[y] for y in level_years]))
    fl = forward_lots(P)
    done = completed_by(P, dt.date(2027, 1, 1))
    n27 = neighbourhood_count(P, done, neighbourhood)[fl]
    g27 = np.minimum(gfn(n27), ng - 1)
    u = unserved_rate(P)
    out = {}
    for nm in FORWARD:
        sel = P.area[fl] == nm
        w = served_weight(P.areas[nm]["accepted"], 2027, season, _mdays)
        lam = lvl * ce[P.canal[fl][sel].astype(int)] * ge[g27[sel]]
        out[nm] = float(np.sum(1 - np.exp(-(lam * w + u * (1 - w))))) if EXACT[0] else float(np.sum(lam * w + u * (1 - w)))
    out["total"] = sum(out[n] for n in FORWARD)
    return out, dict(ye=ye, ce=ce, ge=ge, ll=ll, season=season, u=u, n27=n27, fl=fl)


def analog(P, season=None, scaled=False):
    """the default path: each earlier area's permits per vacant lot in its first twelve months of service"""
    season = season_shares(P) if season is None else season
    num = den = 0.0
    LY = None
    rows = []
    for nm, a in P.areas.items():
        acc = a["accepted"]
        if acc is None or acc > dt.date(2025, 12, 31):
            continue
        end = dt.date(acc.year + 1, acc.month, acc.day)
        sel = np.where(P.area == nm)[0]
        vac = [i for i in sel if not (P.yb[i] > 0 and i not in P.issue) and P.issue.get(i, dt.date(2100, 1, 1)) >= acc]
        n = sum(1 for i in vac if acc <= P.issue.get(i, dt.date(2100, 1, 1)) < end)
        built = 1 - len(vac) / len(sel)
        rows.append((nm, n, len(vac), built, acc))
    return rows


def connections_fy26(target, P=None):
    """new single-family connections in fiscal 2026: a lot's first meter install, made in fiscal 2026 at a lot with no
    account opened before it, by the schedule's phase and fiscal quarter. Premises are placed on lots by parcel number or
    service address, and a lot carried under two premises is one connection. Returns the golden grid and the grids of the
    routes the ceiling prices."""
    P = P or Pack(target)
    prem = _csv(os.path.join(target, C.F_PREM))
    acct = _csv(os.path.join(target, C.F_ACCT))
    ami = _csv(os.path.join(target, C.F_AMI))
    plot = {}
    for r in prem:
        plot[r["PREMISE_ID"]] = P.ix[r["PARCEL_ID"]] if r["PARCEL_ID"] else P.ix_addr[norm_addr(r["SVC_ADDR"])]
    stored = {r["PREMISE_ID"]: r["UEP_PHASE"] for r in prem}
    status = {r["PREMISE_ID"]: r["STATUS"] for r in prem}
    akey = {r["PREMISE_ID"]: norm_addr(r["SVC_ADDR"]) for r in prem}
    fa_p, fa_l, fi_p, fi_l, fa_a, fi_a = {}, {}, {}, {}, {}, {}

    def lower(dct, k, v):
        if k not in dct or v < dct[k]:
            dct[k] = v
    for r in acct:
        s_ = _iso(r["SVC_START"])
        lower(fa_p, r["PREMISE_ID"], s_)
        lower(fa_l, plot[r["PREMISE_ID"]], s_)
        lower(fa_a, akey[r["PREMISE_ID"]], s_)
    for r in ami:
        d = _iso(r["INSTALL_DATE"])
        lower(fi_p, r["PREMISE_ID"], d)
        lower(fi_l, plot[r["PREMISE_ID"]], d)
        lower(fi_a, akey[r["PREMISE_ID"]], d)
    routes = {k: defaultdict(int) for k in ("golden", "cracker", "reader_a", "reader_b", "reader_d", "reader_e",
                                            "reader_f", "stored_phase")}
    for r in ami:
        d = _iso(r["INSTALL_DATE"])
        fy, q = C.fq(d)
        if fy != 2026:
            continue
        pid = r["PREMISE_ID"]
        lot = plot[pid]
        a = P.area[lot]
        ph = "Core" if a == "Core" else P.areas[a]["phase"]
        f = fa_p.get(pid)
        routes["cracker"][(ph, q)] += 1
        if f is None or f >= d:
            routes["reader_a"][(ph, q)] += 1
            sph = "Core" if stored[pid] == "00" else str(int(stored[pid]))
            routes["stored_phase"][(sph, q)] += 1
        if f is None or (d - f).days <= 1000:
            routes["reader_b"][(ph, q)] += 1
        if fi_p[pid] == d and (f is None or f >= d):
            routes["reader_d"][(ph, q)] += 1
            if status[pid] == "ACTIVE":
                routes["reader_e"][(ph, q)] += 1
        fa = fa_a.get(akey[pid])
        if fi_a[akey[pid]] == d and (fa is None or fa >= d):
            routes["reader_f"][(ph, q)] += 1
        fl = fa_l.get(lot)
        if fi_l[lot] == d and (fl is None or fl >= d):
            routes["golden"][(ph, q)] += 1
    return routes


def fees_fy26(target):
    """capacity fees received by fiscal quarter: one amount per payment, a payment being a receipt number and its payer
    (receipt numbers run by drawer and day, and a receipt repeats its amount on each permit line). Returns the golden,
    the sum of every line and the sum of one amount per receipt number."""
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, C.F_FEES), read_only=True)
    it = wb.worksheets[0].iter_rows(values_only=True)
    head = list(next(it))
    rows = [dict(zip(head, r)) for r in it]
    pay, by_no = {}, {}
    lines = defaultdict(float)
    for r in rows:
        d = r["Receipt Date"].date() if isinstance(r["Receipt Date"], dt.datetime) else r["Receipt Date"]
        fy, q = C.fq(d)
        pay[(r["Receipt No"], r["Payer"])] = (q, float(r["Amount"]))
        by_no.setdefault(r["Receipt No"], (q, float(r["Amount"])))
        lines[q] += float(r["Amount"])
    golden, number = defaultdict(float), defaultdict(float)
    for q, amt in pay.values():
        golden[q] += amt
    for q, amt in by_no.values():
        number[q] += amt
    return golden, lines, number

def routes(P, season=None):
    """every priced route to the 2027 total, keyed by name: the golden family and the rivals"""
    season = season_shares(P) if season is None else season
    res = {}
    LY = lot_years(P, season, "street")
    g, info = forecast(P, season, LY=LY)
    res["golden (homes on the street, count bins)"] = g
    sh = LY["n"] / P.seg_n[P.seg[LY["lot"].astype(int)]]
    E5 = np.concatenate([[1e-9], np.arange(0.05, 1.0, 0.05)])
    E10 = np.concatenate([[1e-9], np.arange(0.10, 1.0, 0.10)])
    fl = info["fl"]
    sh27 = info["n27"] / P.seg_n[P.seg[fl]]

    def share_route(edges):
        groups = np.digitize(sh, edges)
        ng = len(edges) + 1
        ye, ce, ge, _ = fit_poisson(LY, groups, ng)
        g27 = np.digitize(sh27, edges)
        return _project(P, fl, ye[2026], ce, ge[g27], season, info["u"])
    res["golden family: share of the street built, 5-point bins"] = share_route(E5)
    res["golden family: share of the street built, 10-point bins"] = share_route(E10)
    res["rival: street started or not (two bins)"] = share_route(np.array([1e-9]))
    ye1, ce1, ge1, _ = fit_poisson(dict(LY, canal=np.zeros(len(LY["y"]), dtype=int)), np.digitize(LY["n"], COUNT_BINS), len(COUNT_BINS) + 1)
    res["rival: golden without the canal term"] = _project(P, fl, ye1[2026], np.array([1.0, 1.0]), ge1[np.minimum(np.digitize(info["n27"], COUNT_BINS), len(COUNT_BINS))], season, info["u"])
    res["golden family: level of 2024 to 2026"] = forecast(P, season, LY=LY, level_years=(2024, 2025, 2026))[0]
    # no street term
    ye, ce, ge, _ = fit_poisson(LY, np.zeros(len(LY["y"]), dtype=int), 1)
    res["rival: served lot model without the street"] = _project(P, fl, ye[2026], ce, np.full(len(fl), ge[0]), season, info["u"])
    # plat block
    LB = lot_years(P, season, "block")
    gb, _ = forecast(P, season, neighbourhood="block", LY=LB)
    res["rival: homes on the plat block"] = gb
    # analog: earlier areas' first twelve months
    rows = analog(P, season)
    num = sum(r[1] for r in rows); den = sum(r[2] for r in rows)
    yes = ye  # served-lot year effects (no street) as the market index
    res["default: first-year analog, raw"] = _flat(P, fl, num / den, season, info["u"])
    sc = sum(r[1] / yes[r[4].year] * yes[2026] for r in rows) / den
    res["default: first-year analog, market-scaled"] = _flat(P, fl, sc, season, info["u"])
    x = np.array([r[3] for r in rows]); yv = np.array([r[1] / r[2] / yes[r[4].year] * yes[2026] for r in rows])
    b1, b0 = np.polyfit(x, yv, 1)
    fsh = 1 - len(fl) / np.isin(P.area, FORWARD).sum()
    res["rival: analog regressed on built share at service"] = _flat(P, fl, b0 + b1 * fsh, season, info["u"])
    return res, info


def _project(P, fl, lvl, ce, ge_lots, season, u):
    out = {}
    for nm in FORWARD:
        sel = P.area[fl] == nm
        w = served_weight(P.areas[nm]["accepted"], 2027, season, _mdays)
        lam = lvl * ce[P.canal[fl][sel].astype(int)] * ge_lots[sel]
        out[nm] = float(np.sum(1 - np.exp(-(lam * w + u * (1 - w))))) if EXACT[0] else float(np.sum(lam * w + u * (1 - w)))
    out["total"] = sum(out[n] for n in FORWARD)
    return out


def _flat(P, fl, rate, season, u):
    out = {}
    for nm in FORWARD:
        sel = P.area[fl] == nm
        w = served_weight(P.areas[nm]["accepted"], 2027, season, _mdays)
        out[nm] = float(sel.sum() * ((1 - np.exp(-(rate * w + u * (1 - w)))) if EXACT[0] else (rate * w + u * (1 - w))))
    out["total"] = sum(out[n] for n in FORWARD)
    return out


def _subset(LY, mask):
    return {k: v[mask] for k, v in LY.items()}


def glm_forecast(P, LY, info, season, form, years=None, level_years=(2026,)):
    """parametric street forms by Poisson IRLS on cells (year, canal, homes on the street): 'zero' an indicator for a
    street with no home, 'zero_linear' that indicator plus a linear term in the homes standing"""
    if years is not None:
        LY = _subset(LY, np.isin(LY["y"], years))
    n = np.minimum(LY["n"], 40)
    keys = np.stack([LY["y"], LY["canal"], n], axis=1)
    uk, inv = np.unique(keys, axis=0, return_inverse=True)
    inv = inv.ravel()
    X_ = np.bincount(inv, weights=LY["exp"]); E_ = np.bincount(inv, weights=LY["ev"])
    yrs = np.unique(uk[:, 0])
    cols = [(uk[:, 0] == y).astype(float) for y in yrs] + [uk[:, 1].astype(float), (uk[:, 2] == 0).astype(float)]
    if form == "zero_linear":
        cols.append(uk[:, 2].astype(float))
    D = np.column_stack(cols)
    beta = np.zeros(D.shape[1]); beta[:len(yrs)] = np.log(E_.sum() / X_.sum())
    for _ in range(60):
        mu = X_ * np.exp(D @ beta)
        W = mu
        z = D @ beta + (E_ - mu) / np.maximum(mu, 1e-12)
        beta = np.linalg.solve((D * W[:, None]).T @ D + 1e-9 * np.eye(D.shape[1]), (D * W[:, None]).T @ z)
    yeff = dict(zip(yrs.tolist(), beta[:len(yrs)]))
    lvl = np.mean([yeff[y] for y in level_years])
    fl = info["fl"]; n27 = np.minimum(info["n27"], 40)
    eta = lvl + beta[len(yrs)] * P.canal[fl] + beta[len(yrs) + 1] * (n27 == 0)
    if form == "zero_linear":
        eta = eta + beta[len(yrs) + 2] * n27
    lam = np.exp(eta)
    out = {}
    for nm in FORWARD:
        sel = P.area[fl] == nm
        w = served_weight(P.areas[nm]["accepted"], 2027, season, _mdays)
        r = lam[sel] * w + info["u"] * (1 - w)
        out[nm] = float(np.sum(1 - np.exp(-r))) if EXACT[0] else float(np.sum(r))
    out["total"] = sum(out[k] for k in FORWARD)
    return out


def family(P, season=None):
    """the honest family on the filed estimand (and the rate form beside it), totals and areas"""
    season = season_shares(P) if season is None else season
    LY = lot_years(P, season, "street")
    fam = {}
    g, info = forecast(P, season, LY=LY)
    fam["count bins (golden)"] = g
    sh = LY["n"] / P.seg_n[P.seg[LY["lot"].astype(int)]]
    fl = info["fl"]
    sh27 = info["n27"] / P.seg_n[P.seg[fl]]
    for nm, edges in (("share bins 5 points", np.concatenate([[1e-9], np.arange(0.05, 1.0, 0.05)])),
                      ("share bins 10 points", np.concatenate([[1e-9], np.arange(0.10, 1.0, 0.10)]))):
        ye, ce, ge, _ = fit_poisson(LY, np.digitize(sh, edges), len(edges) + 1)
        fam[nm] = _project(P, fl, ye[2026], ce, ge[np.digitize(sh27, edges)], season, info["u"])
    EXACT[0] = False
    fam["count bins, rate times exposure"] = forecast(P, season, LY=LY)[0]
    EXACT[0] = True
    for nm, yrs in (("fit 2019 to 2026", list(range(2019, 2027))), ("fit 2025 to 2026", [2025, 2026]),
                    ("fit 2013 to 2026", list(range(2013, 2027)))):
        sub = _subset(LY, np.isin(LY["y"], yrs))
        fam[nm] = forecast(P, season, LY=sub)[0]
    fam["level 2023 to 2026 averaged"] = forecast(P, season, LY=LY, level_years=(2023, 2024, 2025, 2026))[0]
    ye1, _, ge1, _ = fit_poisson(dict(LY, canal=np.zeros(len(LY["y"]), dtype=int)), np.digitize(LY["n"], COUNT_BINS),
                                 len(COUNT_BINS) + 1)
    fam["no canal term"] = _project(P, fl, ye1[2026], np.array([1.0, 1.0]),
                                    ge1[np.minimum(np.digitize(info["n27"], COUNT_BINS), len(COUNT_BINS))], season, info["u"])
    fam["zero-homes indicator"] = glm_forecast(P, LY, info, season, "zero")
    fam["zero indicator plus linear count"] = glm_forecast(P, LY, info, season, "zero_linear")
    return fam, info
