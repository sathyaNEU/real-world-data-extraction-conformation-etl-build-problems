"""Weather, Business Saver calls, interval reads, settled zone loads and programme credits, ten summers."""
from __future__ import annotations

import math
from datetime import date, timedelta

import numpy as np
import pandas as pd

from common import (BOOKS, EXTRACT, FULL_LIFT, HEAT_LO, HEAT_SAT, HEDGES, NC, ORDINARY_DROP, PEAKS, READ_HOURS,
                    SUMMERS, TARGET_EXPOSURE, TEMP_BASE, TEMP_NOISE, TEMP_SCALE, WINDOW_HOURS, billing_holidays, daterange, p90,
                    summer_weekdays)
from world import CENTRE_TOTAL_KW, MEMBERS, TWIN_COLD

HOUR_MOD = dict(zip(READ_HOURS, [-0.006, -0.004, -0.002, 0.0, 0.001, 0.001, 0.0, 0.0, -0.002, -0.004]))
SHAPE = {  # IDR general premise shapes, hour ending 1..24, share of the premise's level
    "office": [.42, .41, .40, .40, .41, .45, .55, .68, .80, .88, .93, .96, .98, .99, 1.0, 1.0, .99, .95, .86, .74, .62, .53, .47, .44],
    "flat": [.93, .92, .92, .92, .92, .93, .94, .95, .96, .97, .98, .99, 1.0, 1.0, 1.0, 1.0, 1.0, .99, .98, .97, .96, .95, .94, .93],
    "hospital": [.70, .68, .67, .67, .68, .72, .78, .84, .89, .93, .96, .98, .99, 1.0, 1.0, .99, .98, .96, .92, .87, .82, .78, .74, .72],
    "plant": [.78, .77, .77, .77, .78, .82, .88, .93, .96, .98, .99, 1.0, 1.0, .99, .99, .98, .97, .95, .92, .88, .85, .82, .80, .79],
    "warehouse": [.45, .44, .44, .44, .46, .55, .70, .84, .92, .96, .98, .99, 1.0, 1.0, .99, .98, .95, .88, .76, .63, .54, .49, .47, .46],
    "retail": [.40, .39, .38, .38, .39, .42, .50, .62, .74, .84, .91, .95, .97, .99, 1.0, 1.0, 1.0, .99, .96, .90, .80, .66, .52, .44],
}
BETA = {"office": 0.34, "flat": 0.04, "hospital": 0.18, "plant": 0.07, "warehouse": 0.14, "retail": 0.29}
BOOK_SHAPE = [.52, .50, .49, .49, .50, .54, .62, .72, .80, .86, .90, .93, .95, .97, .985, .995, 1.0, .99, .96, .91, .84, .75, .66, .58]
BOOK_GAMMA = {"Coast": 0.36, "East": 0.33, "Far West": 0.30, "North": 0.34, "North Central": 0.37,
              "South Central": 0.35, "Southern": 0.31, "West": 0.30}
# summer-to-summer swing of the general coincidence factor (2023 and 2026 the two hottest)
W = {2017: 0.30, 2018: -0.55, 2019: 0.12, 2020: 0.62, 2021: 0.05, 2022: 0.78, 2023: 1.00, 2024: 0.66,
     2025: -0.08, 2026: 0.996}
SWING = {"Coast": 0.040, "East": 0.044, "Far West": 0.033, "North": 0.048, "North Central": 0.051,
         "South Central": 0.045, "Southern": 0.037, "West": 0.035}


def summer_days(y):
    return list(daterange(date(y, 6, 1), date(y, 9, 30)))


def build_heat(rng):
    """Daily heat index per summer: system and per book."""
    heat = {}
    for y in SUMMERS:
        days = summer_days(y)
        n = len(days)
        t = np.arange(n)
        seas = 0.36 + 0.42 * np.sin(np.pi * np.clip((t - 5) / 100.0, 0, 1))
        e = np.zeros(n)
        for i in range(1, n):
            e[i] = 0.72 * e[i - 1] + rng.normal(0, 0.075)
        hs = seas + e
        pk = days.index(PEAKS[y][0])
        hs[pk] = hs.max() + 0.045
        zb = {}
        for b in BOOKS:
            z = hs + rng.normal(0, 0.035, n)
            z[pk] = hs[pk] + rng.normal(0, 0.005)
            zb[b] = z
        heat[y] = {"days": days, "sys": hs, "book": zb}
    return heat


def choose_calls(rng, heat):
    calls = {}
    for y in SUMMERS:
        days, hs = heat[y]["days"], heat[y]["sys"]
        hol = billing_holidays(y)
        bdays = [d for d in days if d.weekday() < 5 and d not in hol]
        cand = bdays[10:]
        idx = {d: i for i, d in enumerate(days)}
        score = {d: hs[idx[d]] + rng.normal(0, 0.07) for d in cand}
        k = 15 + int(rng.integers(0, 7))
        chosen = set(sorted(cand, key=lambda d: -score[d])[:k])
        pk = PEAKS[y][0]
        chosen.add(pk)
        wk = [d for d in days if d.weekday() < 5]
        n10 = math.ceil(0.1 * len(wk))
        top = sorted(wk, key=lambda d: -hs[idx[d]])[:n10]
        unc = [d for d in top if d not in chosen]
        # at least five of the hottest decile left uncalled (forecast misses), the peak always called
        for d in sorted([d for d in top if d in chosen and d != pk], key=lambda d: score.get(d, 0)):
            if len(unc) >= 5:
                break
            chosen.discard(d)
            unc.append(d)
            alt = [c for c in sorted(cand, key=lambda c: -score[c]) if c not in chosen and c not in top]
            chosen.add(alt[0])
        calls[y] = sorted(chosen)
    return calls


def member_share(u: float, h: float) -> float:
    """Share of maximum demand a member draws in an uncalled afternoon hour at zone heat h: its base level on ordinary
    afternoons, its full-load level once the zone reaches design-day heat, linear between."""
    full = u + FULL_LIFT
    t = min(1.0, max(0.0, (h - HEAT_LO) / (HEAT_SAT - HEAT_LO)))
    return full - ORDINARY_DROP * (1.0 - t)


def member_reads(rng, prem, calls, heat):
    """Hourly reads, hours ending 11 to 20, every weekday each member is in the book."""
    mem = prem[(prem["comp"] == "ref") & (prem["record_type"] == "NEW")]
    rows = []
    for _, m in mem.iterrows():
        md, phi, u = m["md_kw"], m["phi"], m["u"]
        for y in SUMMERS:
            cs = set(calls[y])
            di = {d: i for i, d in enumerate(heat[y]["days"])}
            hb = heat[y]["book"][m["book"]]
            for d in summer_weekdays(y):
                if d < m["start"]:
                    continue
                s = member_share(u, hb[di[d]])
                called = d in cs
                for h in READ_HOURS:
                    if called and h in WINDOW_HOURS:
                        v = md * phi * (1 + rng.normal(0, 0.0018))
                    elif called and h in (13, 14):
                        v = md * min(0.985, s + 0.03) * (1 + rng.normal(0, 0.003))
                    elif called and h == 19:
                        v = md * min(0.985, s + 0.035) * (1 + rng.normal(0, 0.003))
                    elif called and h == 20:
                        v = md * min(0.985, s + 0.015) * (1 + rng.normal(0, 0.003))
                    else:
                        v = md * s * (1 + HOUR_MOD[h]) * (1 + rng.normal(0, 0.0022))
                    rows.append((m["esi_id"], d, h, round(v, 1)))
    return pd.DataFrame(rows, columns=["esi_id", "date", "he", "kwh"])


def build_temps(rng, heat):
    """The weather vendor's daily maximum and minimum by zone, whole degrees F."""
    rows = []
    for y in SUMMERS:
        for b in BOOKS:
            for d, h in zip(heat[y]["days"], heat[y]["book"][b]):
                tmax = TEMP_BASE[b] + TEMP_SCALE * (h - 0.62) + rng.normal(0, TEMP_NOISE)
                tmin = tmax - 21 - rng.normal(0, 2.0)
                rows.append((d, b, int(round(tmax)), int(round(tmin))))
    return pd.DataFrame(rows, columns=["date", "book", "tmax", "tmin"])


def peak_heat_draw(prem, mreads, calls, temps):
    """The golden's estimator of what a cold store draws in the system peak hour when it is not called: the members'
    MD-weighted share of maximum demand at each summer's peak hour on weekdays with no called window on which the
    site's weather zone reached at least the lowest maximum temperature that zone recorded on any closed system-peak
    day. Returns the share and the number of site-days behind it."""
    md = prem[prem["comp"] == "ref"].drop_duplicates("esi_id").set_index("esi_id")
    t = temps.set_index(["date", "book"])["tmax"]
    cut = {b: min(t[(PEAKS[y][0], b)] for y in SUMMERS) for b in BOOKS}
    r = mreads.copy()
    r["y"] = [d.year for d in r["date"]]
    r = r[r["he"] == r["y"].map(lambda y: PEAKS[y][1])]
    called = {d for y in SUMMERS for d in calls[y]}
    r = r[[d not in called for d in r["date"]]]
    bk = r["esi_id"].map(md["book"])
    r = r[[t[(d, b)] >= cut[b] for d, b in zip(r["date"], bk)]]
    return float(r["kwh"].sum() / r["esi_id"].map(md["md_kw"]).sum()), len(r), cut


def daily_md(prem):
    """Daily dedup MD (kW) per book over the summers and members' MD per book."""
    d0, d1 = date(2017, 6, 1), date(2026, 9, 30)
    nd = (d1 - d0).days + 1
    out, mem = {}, {}
    p = prem[prem["record_type"] == "NEW"]
    for b in BOOKS:
        for key, sub in (("all", p[p["book"] == b]), ("ref", p[(p["book"] == b) & (p["comp"] == "ref")])):
            arr = np.zeros(nd + 1)
            for s, e, md in zip(sub["start"], sub["end"], sub["md_kw"]):
                i0 = max(0, (s - d0).days)
                if i0 > nd - 1:
                    continue
                i1 = nd if e is None else (e - d0).days + 1
                if i1 <= 0:
                    continue
                arr[i0] += md
                arr[min(i1, nd)] -= md
            (out if key == "all" else mem)[b] = np.cumsum(arr)[:nd]
    return d0, out, mem


def solve_factors(rng, prem, mreads, calls, u_star):
    """General coincidence factor per book and summer: a book-level scale on the swing pattern, solved so the answer's
    exposures land on the design's targets. Returns f[b][y] and the peak-hour pieces."""
    d0, mdall, mdref = daily_md(prem)
    ref_at = {}
    md = prem[prem["comp"] == "ref"].drop_duplicates("esi_id").set_index("esi_id")
    for y in SUMMERS:
        pd_, he, _ = PEAKS[y]
        r = mreads[(mreads["date"] == pd_) & (mreads["he"] == he)]
        r = r.assign(book=r["esi_id"].map(md["book"]))
        ref_at[y] = r.groupby("book")["kwh"].sum().reindex(BOOKS).fillna(0.0)
    act = prem[(prem["record_type"] == "NEW") & (prem["start"] <= EXTRACT) & prem["end"].isna()]
    m27 = act[act["comp"] != "centre"].groupby("book")["md_kw"].sum().reindex(BOOKS)
    pieces = {}
    noise = {b: {y: (0.0 if y in (2023, 2026) else rng.normal(0, 0.006)) for y in SUMMERS} for b in BOOKS}
    f = {}
    for b in BOOKS:
        rows = []
        for y in SUMMERS:
            i = (PEAKS[y][0] - d0).days
            rows.append((y, mdall[b][i], mdref[b][i], ref_at[y][b]))
        pieces[b] = rows
        a26 = rows[-1][1]
        extra = u_star * CENTRE_TOTAL_KW if b == NC else 0.0
        tgt = TARGET_EXPOSURE[b]
        for _ in range(60):
            w = {y: 1 + SWING[b] * W[y] + noise[b][y] for y in SUMMERS}

            def expo(k):
                x = [(k * w[y] * (a - r) + rf) / a * m27[b] for (y, a, r, rf) in rows]
                return (p90(x) + extra) / 1000.0 - HEDGES[b]
            lo, hi = 0.2, 0.9
            for _ in range(200):
                mid = (lo + hi) / 2
                lo, hi = (mid, hi) if expo(mid) < tgt else (lo, mid)
            k = (lo + hi) / 2
            # every cell of the close-out replay table clear of a half-MW edge: the two summers that set the 1-in-10
            # are pinned by the target, so those move with a small shift of the target, the rest with their swing
            cells = {y: (k * w[y] * (a - r) + rf) / a * a26 / 1000.0 for (y, a, r, rf) in rows}
            top2 = sorted(cells, key=lambda y: -cells[y])[:2]
            moved = False
            for y, cell in cells.items():
                frac = cell % 1.0
                if y in top2 and abs(frac - 0.5) < 0.08:
                    # cell-space moves that clear the edge, smallest first; the target keeps its own MW bin clear and
                    # never moves a book toward the lot it is closest to losing or gaining
                    opts = []
                    for d in (0.1, 0.14, 0.18, 0.22, 0.26, 0.3, 0.34, 0.38):
                        for sgn in (-1, 1):
                            if (b == "South Central" and sgn < 0) or (b == "Southern" and sgn > 0):
                                continue
                            if any(abs(((cells[t] + sgn * d) % 1.0) - 0.5) < 0.1 for t in top2):
                                continue
                            t2 = tgt + sgn * d * m27[b] / a26
                            if abs((t2 % 1.0) - 0.5) >= 0.27 and abs(t2 - TARGET_EXPOSURE[b]) <= 0.45:
                                opts.append(t2)
                    if not opts:
                        raise AssertionError(f"no clear target for {b}")
                    tgt = opts[0]
                    moved = True
                    break
                if y not in top2 and abs(frac - 0.5) < 0.1:
                    step = 0.3 if frac < 0.5 else -0.3
                    noise[b][y] -= step / cell * w[y]
                    moved = True
            if not moved:
                break
        else:
            raise AssertionError(f"replay cells not cleared for {b}")
        f[b] = {y: k * w[y] for y in SUMMERS}
    return f, pieces, m27


def idr_reads(rng, prem, heat, f, twin_2026_kw=910.0):
    """Hourly reads for the general IDR premises; each premise's summer scaled so the premises in the book at the
    system peak sum to the book's general factor times their MD in that hour."""
    gen = prem[(prem["comp"] == "idr") & (prem["record_type"] == "NEW")].copy()
    gen["a"] = rng.uniform(0.86, 1.0, len(gen))
    gen["e"] = np.exp(rng.normal(0, 0.10, len(gen)))
    hidx = np.array(READ_HOURS) - 1
    frames = []
    for y in SUMMERS:
        pkd, he, _ = PEAKS[y]
        days = summer_days(y)
        di = {d: i for i, d in enumerate(days)}
        wk = summer_weekdays(y)
        at_peak = gen[(gen["start"] <= pkd) & gen["end"].map(lambda e: e is None or e >= pkd)]
        target = {}
        for b in BOOKS:
            sub = at_peak[at_peak["book"] == b]
            e = sub["e"].to_numpy() * np.exp(rng.normal(0, 0.035, len(sub)))
            P = sub["md_kw"].to_numpy() * f[b][y] * e
            tw = sub["twin"].to_numpy()
            if y == 2026 and tw.any():
                fixed = twin_2026_kw
                rest = f[b][y] * sub["md_kw"].sum() - fixed
                P[~tw] = P[~tw] / P[~tw].sum() * rest
                P[tw] = fixed
            else:
                P = P / P.sum() * f[b][y] * sub["md_kw"].sum()
            P = np.minimum(P, 0.95 * sub["md_kw"].to_numpy())
            for esi, pv in zip(sub["esi_id"], P):
                target[esi] = pv
        for _, p in gen.iterrows():
            if not (p["start"] <= date(y, 9, 30) and (p["end"] is None or p["end"] >= date(y, 6, 1))):
                continue
            act = [d for d in wk if d >= p["start"] and (p["end"] is None or d <= p["end"])]
            if not act:
                continue
            shp = np.array(SHAPE[p["family"]])
            hb = heat[y]["book"][p["book"]]
            hpk = hb[di[pkd]]
            H = np.array([hb[di[d]] for d in act])
            raw = p["md_kw"] * p["a"] * shp[hidx][None, :] * (1 + BETA[p["family"]] * (H - hpk))[:, None]
            raw = raw * (1 + rng.normal(0, 0.022, raw.shape))
            raw_pk = p["md_kw"] * p["a"] * shp[he - 1]
            tgt = target.get(p["esi_id"], p["md_kw"] * f[p["book"]][y] * p["e"])
            c = tgt / raw_pk
            v = np.minimum(raw * c, 0.96 * p["md_kw"])
            if pkd in act:
                v[act.index(pkd), READ_HOURS.index(he)] = tgt
            v = np.round(v, 1)
            n = len(act)
            frames.append(pd.DataFrame({"esi_id": p["esi_id"], "date": np.repeat(act, 10),
                                        "he": np.tile(READ_HOURS, n), "kwh": v.ravel()}))
    return pd.concat(frames, ignore_index=True)


def settled(rng, prem, heat, f, mreads):
    """Hourly settled load per book (MWh), every day June to September, ten summers."""
    d0, mdall, mdref = daily_md(prem)
    md = prem[prem["comp"] == "ref"].drop_duplicates("esi_id").set_index("esi_id")
    mr = mreads.assign(book=mreads["esi_id"].map(md["book"]))
    refh = mr.groupby(["book", "date", "he"])["kwh"].sum()
    mem = md.reset_index()
    rows = []
    shp = np.array(BOOK_SHAPE)
    for y in SUMMERS:
        pkd, he, _ = PEAKS[y]
        days = summer_days(y)
        for b in BOOKS:
            hb = heat[y]["book"][b]
            hpk = hb[days.index(pkd)]
            dpk = shp[he - 1]
            for i, d in enumerate(days):
                k = (d - d0).days
                mdg = mdall[b][k] - mdref[b][k]
                wkend = d.weekday() >= 5
                base = shp * (0.78 if wkend else 1.0) * (1 + BOOK_GAMMA[b] * (hb[i] - hpk))
                g = f[b][y] * base / dpk
                if not (d == pkd):
                    g = g * (1 + rng.normal(0, 0.004, 24))
                act = mem[(mem["book"] == b) & (mem["start"] <= d)]
                rf0 = float(sum(k * member_share(uu, hb[i]) for k, uu in zip(act["md_kw"], act["u"])))
                for h in range(1, 25):
                    if not wkend and h in READ_HOURS:
                        rf = refh.get((b, d, h), 0.0)
                    else:
                        rf = rf0 * (1 + rng.normal(0, 0.002))
                    rows.append((b, d, h, round((mdg * g[h - 1] + rf) / 1000.0, 3)))
    return pd.DataFrame(rows, columns=["book", "date", "he", "mwh"])


def credits(prem, mreads, calls, rate):
    """Business Saver credits: per account per called window, kWh below baseline over hours ending 15 to 18, where the
    baseline for an hour is the site's average in that hour on its ten most recent business days without a call."""
    md = prem[prem["comp"] == "ref"].drop_duplicates("esi_id").set_index("esi_id")
    r = mreads.set_index(["esi_id", "date", "he"])["kwh"].copy()
    out, base_at_peak = [], {}
    for y in SUMMERS:
        hol = billing_holidays(y)
        cs = set(calls[y])
        bdays = [d for d in summer_weekdays(y) if d not in hol]
        for d in calls[y]:
            prior = [x for x in bdays if x < d and x not in cs]
            per_acct, sites = {}, {}
            for esi, m in md.iterrows():
                if m["start"] > d:
                    continue
                pr = [x for x in prior if x >= m["start"]][-10:]
                kwh = 0.0
                for h in WINDOW_HOURS:
                    base = np.mean([r[(esi, x, h)] for x in pr])
                    kwh += max(0.0, base - r[(esi, d, h)])
                    if d == PEAKS[y][0] and h == PEAKS[y][1]:
                        base_at_peak[(y, esi)] = base
                per_acct[m["account"]] = per_acct.get(m["account"], 0.0) + kwh
                sites.setdefault(m["account"], esi)
            for a, k in per_acct.items():
                if abs((k % 1.0) - 0.5) < 0.06:
                    # a whole-kWh credit with no half to round: the site's first window hour read 0.1 kWh higher
                    r[(sites[a], d, WINDOW_HOURS[0])] = round(r[(sites[a], d, WINDOW_HOURS[0])] + 0.1, 1)
                    k -= 0.1
                kw = int(round(k))
                out.append((a, d, kw, round(kw * rate[y], 2)))
    mreads = r.reset_index()
    return pd.DataFrame(out, columns=["account", "date", "kwh", "usd"]), base_at_peak, mreads
