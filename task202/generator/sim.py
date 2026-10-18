"""The clean truth behind the task202 pack: every award the Household Relief Grant resolved between
July 2024 and March 2027, the partners that resolved them, and which of them the partner claim portal
holds award by award.

Nothing here is shipped. The pack ships the monthly claim returns (a total and an award count per
partner, band and month) for every partner, and the portal's award-level rows for the two pilot
provinces only; the within-partner award shape exists at award level in one of those two places and
in aggregate in the other, which is the whole point of the build.
"""
import datetime as dt

import numpy as np

import params as P

MONTHS = []
_y, _m = P.RETURNS_FROM
while (_y, _m) <= (2027, 3):
    MONTHS.append((_y, _m))
    _m += 1
    if _m == 13:
        _y, _m = _y + 1, 1
WINDOW = [t for t in MONTHS if P.WINDOW_FROM <= t <= P.WINDOW_TO]
PORTAL_MONTHS = [t for t in MONTHS if P.PORTAL_FROM <= t <= P.PORTAL_TO]

UPPER_NORM = P.P_UPPER * P.UPPER_MULT + (1.0 - P.P_UPPER)   # so the shape averages one


def stream(*key):
    """One reproducible RNG per entity, so a partner's draws never depend on another's."""
    return np.random.default_rng([P.SEED] + [int(k) for k in key])


def month_days(y, m):
    return (dt.date(y + (m == 12), m % 12 + 1, 1) - dt.date(y, m, 1)).days


def partner_table():
    """The 88 accredited partners: province, award level, volume, band mix and lifecycle."""
    rng = stream(1)
    prov_eff = rng.normal(0.0, P.PROV_SD, len(P.PROVINCES))
    order = np.argsort(prov_eff)
    pilot = {P.PROVINCES[i][0] for i in order[list(P.PILOT_RANKS)]}
    rows = []
    for pi, (pcode, pname, psgc, region) in enumerate(P.PROVINCES):
        towns = P.TOWNS[pcode]
        for slot in range(P.PARTNERS_PER_PROVINCE):
            r = stream(2, pi, slot)
            town = towns[slot]
            form = P.FORMS[(slot + P.PARTNER_NAME_ROTATE * pi) % len(P.FORMS)]
            level = float(np.exp(prov_eff[pi] + r.normal(0.0, P.WITHIN_PROV_SD)))
            vol = float(max(90.0, round(P.MED_AWARDS_YR * np.exp(r.normal(0.0, P.VOL_SD)))))
            start, end = P.RETURNS_FROM, (2027, 3)
            if pcode == P.NEW_PARTNER["province"] and slot == P.NEW_PARTNER["slot"]:
                d = P.NEW_PARTNER["accredited"]
                start = (d.year, d.month)
            if pcode == P.EXIT_PARTNER["province"] and slot == P.EXIT_PARTNER["slot"]:
                d = P.EXIT_PARTNER["withdrawn"]
                end = (d.year, d.month)
            rows.append(dict(
                idx=len(rows), province=pcode, province_name=pname, psgc=psgc, region=region,
                slot=slot, town=town, name=form.format(t=town), level=level, volume=vol,
                portal=pcode in pilot, first_month=start, last_month=end))
    return rows, sorted(pilot)


def _components(r, upper, n):
    tab = P.COMPONENTS_UPPER if upper else P.COMPONENTS_STD
    codes = [c for c, _, _ in tab]
    w = np.array([x for _, _, x in tab], float)
    return [codes[i] for i in r.choice(len(codes), n, p=w / w.sum())]


def awards():
    """Every award, as the foundation's own systems would hold it."""
    parts, pilot = partner_table()
    mix_rest = np.array([0.16, 0.17, 0.18, 0.19, 0.16, 0.14])
    mix_pilot = np.array([0.27, 0.24, 0.19, 0.14, 0.09, 0.07])
    out = []
    for pt in parts:
        mix = mix_pilot if pt["portal"] else mix_rest
        for (y, m) in MONTHS:
            if not (pt["first_month"] <= (y, m) <= pt["last_month"]):
                continue
            r = stream(3, pt["idx"], y, m)
            lam = pt["volume"] / 12.0 * P.SEASON[m]
            n = int(r.poisson(lam))
            if n == 0:
                continue
            cw = r.multinomial(n, mix)
            nd = month_days(y, m)
            for bi, b in enumerate(P.BANDS):
                k = int(cw[bi])
                if not k:
                    continue
                lvl = P.BASE * pt["level"] * (P.SCALE3[b] / 1000.0) * P.BAND_LEVEL_TILT[b]
                up = r.random(k) < (P.P_UPPER if (y, m) >= P.CAPITAL_FROM else 0.0)
                sh = np.where(up,
                              P.UPPER_MULT * np.exp(r.normal(-0.5 * P.LOG_SD_UPPER ** 2, P.LOG_SD_UPPER, k)),
                              np.exp(r.normal(-0.5 * P.LOG_SD_STD ** 2, P.LOG_SD_STD, k))) / UPPER_NORM
                amt = np.round(lvl * sh, 2)
                comp_u = _components(r, True, int(up.sum()))
                comp_s = _components(r, False, int((~up).sum()))
                iu = is_ = 0
                sizes = b + (r.random(k) < 0.42) * (1 + (r.random(k) < 0.45) + (r.random(k) < 0.18)) if b == 6 else np.full(k, b)
                days = 1 + r.integers(0, nd, k)
                lag = 6 + r.integers(0, 15, k)
                for j in range(k):
                    if up[j]:
                        comp = comp_u[iu]; iu += 1
                    else:
                        comp = comp_s[is_]; is_ += 1
                    dec = dt.date(y, m, int(days[j]))
                    out.append(dict(partner=pt["idx"], band=b, size=int(sizes[j]), month=(y, m),
                                    decided=dec - dt.timedelta(days=int(lag[j])), paid=dec,
                                    amount=float(amt[j]), component=comp, upper=bool(up[j])))
    out.sort(key=lambda a: (a["partner"], a["month"], a["band"], a["paid"], a["amount"]))
    return parts, pilot, out


def make():
    parts, pilot, aw = awards()
    cells = {}
    for a in aw:
        k = (a["partner"], a["month"], a["band"])
        c = cells.setdefault(k, [0, 0.0])
        c[0] += 1
        c[1] = round(c[1] + a["amount"], 2)
    # the window's partner-band cells, which is what the claim returns state about the window
    wcell = {}
    for (pi, mo, b), (n, tot) in cells.items():
        if P.WINDOW_FROM <= mo <= P.WINDOW_TO:
            c = wcell.setdefault((pi, b), [0, 0.0])
            c[0] += n
            c[1] = round(c[1] + tot, 2)
    mean = {k: v[1] / v[0] for k, v in wcell.items()}
    cnt = {k: v[0] for k, v in wcell.items()}
    win = [a for a in aw if P.WINDOW_FROM <= a["month"] <= P.WINDOW_TO]
    por = [a for a in aw if parts[a["partner"]]["portal"] and P.PORTAL_FROM <= a["month"] <= P.PORTAL_TO]
    porwin = [a for a in por if P.WINDOW_FROM <= a["month"] <= P.WINDOW_TO]
    shape = np.array([a["amount"] / mean[(a["partner"], a["band"])] for a in porwin], float)
    return dict(parts=parts, pilot=pilot, awards=aw, cells=cells, mean=mean, cnt=cnt,
                win=win, por=por, porwin=porwin, shape=shape, months=MONTHS, window=WINDOW)
