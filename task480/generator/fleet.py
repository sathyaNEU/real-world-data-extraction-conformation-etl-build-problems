"""The area's vehicles from 1 January 2024 to 1 July 2026 as the registration and inspection systems would hold
them: who is on file, who left (scrapped, moved out, retired under the 2025 pilot), who moved between member
counties or arrived from out of state, and each first-cycle inspection with its odometer reading. One table of
truth per vehicle; the files are cut from it in pack.py and books.py."""
import datetime as dt
from functools import lru_cache

import numpy as np
import pandas as pd

import vin as V
import world as W

ORD0 = dt.date(2024, 1, 1).toordinal()


def dec(d):
    """A date as a decimal year (the generator's clock)."""
    y0 = dt.date(d.year, 1, 1)
    return d.year + (d - y0).days / ((dt.date(d.year + 1, 1, 1) - y0).days)


def from_dec(x):
    y = int(np.floor(x))
    y0 = dt.date(y, 1, 1)
    n = (dt.date(y + 1, 1, 1) - y0).days
    return y0 + dt.timedelta(days=int(min(n - 1, max(0, np.floor((x - y) * n)))))


def dec_days(t):
    """Decimal years to dates (a Sunday moves to the Saturday before; nothing after the cycle's last day)."""
    t = np.asarray(t, float)
    y = np.floor(t).astype(int)
    n = np.where((y % 4 == 0), 366, 365)
    off = np.minimum(n - 1, np.maximum(0, np.floor((t - y) * n))).astype(int)
    out = []
    for yy, oo in zip(y, off):
        d = dt.date(int(yy), 1, 1) + dt.timedelta(days=int(oo))
        if d.weekday() == 6:
            d -= dt.timedelta(days=1)
        d = max(d, W.EIP_START)
        out.append(min(d, W.CYCLE_END))
    return np.array(out, dtype=object)


def cum(a):
    """Cumulative miles since first sale at age a (years) for a vehicle of intensity 1."""
    a = np.asarray(a, float)
    ab = (W.ACC_NEW - W.ACC_FLOOR) / (-W.ACC_SLOPE)
    x = np.clip(a, 0, ab)
    return W.ACC_NEW * x + W.ACC_SLOPE / 2 * x ** 2 + W.ACC_FLOOR * np.maximum(a - ab, 0)


def _vins(rng, wmi, my, serial):
    n = len(my)
    al = np.array(list(V.ALLOWED))
    vds = al[rng.integers(0, 23, (n, 4))]
    d5 = rng.integers(0, 10, n)
    plant = al[rng.integers(0, len(al), n)]
    out = []
    for i in range(n):
        body = "%s%s%d0%s%s%06d" % (wmi[i], "".join(vds[i]), d5[i], V.YEAR_CODE[int(my[i])], plant[i], serial[i])
        out.append(body[:8] + V.check_digit(body) + body[9:])
    return out


def _plates(rng, n):
    letters = np.array(list("ABCDEFGHJKLMNPRSTUVWXYZ"))
    a = letters[rng.integers(0, len(letters), (n, 3))]
    num = rng.integers(0, 10000, n)
    return ["%s%04d" % ("".join(a[i]), num[i]) for i in range(n)]


@lru_cache(maxsize=None)
def build():
    frames = [county(name, W.FLEET[name], W.DRAW.get(name, 0)) for name in W.NAMES]
    T = pd.concat(frames, ignore_index=True)
    _inspections(T)
    _pilot(T)
    return T


@lru_cache(maxsize=None)
def _models():
    models, mw = V.model_table()
    span = {m: [i for i, x in enumerate(models) if x[5][0] <= m <= x[5][1]] for m in range(1990, 2028)}
    return models, mw, span


@lru_cache(maxsize=None)
def county(name, fleet, draw):
    """One county's vehicles from its own random stream (the county's draw number picks the stream)."""
    models, mw, span = _models()
    cno = W.CNO[name]
    serial0 = 100000 + cno * 9871
    rng = np.random.default_rng(W.SEED * 1000 + cno + 7919 * draw)
    n, shift, kc = fleet
    age26 = np.clip(rng.gamma(3.4, 3.4, n) + shift - 0.6, 0.05, 32.9)
    mys = [np.floor(2026.5 - age26).astype(int) + 1]
    kinds = [np.array(["active"] * n)]
    nd = int(round(0.075 * n))
    ageD = np.clip(rng.gamma(4.6, 3.5, nd) + shift, 3.0, 32.9)
    mys.append(np.floor(2025.2 - ageD).astype(int) + 1)
    kinds.append(np.array(["departed"] * nd))
    if name in W.PILOT_COUNTIES:
        npil = {"Elkhollow": 238, "Dunmarsh": 214, "Larkhaven": 171, "Kinnard": 118}[name]
        mys.append(rng.integers(W.PILOT_MY[0], W.PILOT_MY[1] + 1, npil))
        kinds.append(np.array(["pilot"] * npil))
    my = np.clip(np.concatenate(mys), 1990, 2027)
    kind = np.concatenate(kinds)
    N = len(my)
    mi = np.empty(N, int)
    for m in np.unique(my):
        idx = np.where(my == m)[0]
        cand = np.array(span[int(m)])
        p = mw[cand] / mw[cand].sum()
        mi[idx] = cand[rng.choice(len(cand), len(idx), p=p)]
    mk = np.array([models[i][0] for i in mi])
    cls = np.array([models[i][3] for i in mi])
    body = np.array([models[i][2] for i in mi])
    wmi = np.array([models[i][4][j] for i, j in zip(mi, rng.integers(0, 2, N))])
    fuel = np.full(N, "G", dtype="<U1")
    u = rng.random(N)
    for i in range(N):
        fs = models[mi[i]][7]
        if fs in ("E", "H"):
            fuel[i] = fs
            continue
        m = my[i]
        p = [("G", 1.0)]
        if "F" in fs and 2002 <= m <= 2016:
            p.append(("F", 0.28))
        if "H" in fs and m >= 2005:
            p.append(("H", 0.10))
        if "D" in fs and m >= 2007:
            p.append(("D", 0.07))
        tot = sum(w for _, w in p)
        acc = 0.0
        for f, w in p:
            acc += w / tot
            if u[i] <= acc:
                fuel[i] = f
                break
    g = rng.random(N)
    gvwr = np.where(cls == "PC", "1", np.where((body == "PK") & (g < 0.08), "2b",
                                               np.where((body == "PK") | (body == "MV") | (g > 0.7), "2a", "1")))
    o = rng.random(N)
    owner = np.where((my >= 2023) & (o < 0.10), "LSR", np.where(o < 0.15, "BUS", np.where(o < 0.165, "GOV", "IND")))
    serial = serial0 + np.cumsum(rng.integers(1, 40, N))
    vins = _vins(rng, wmi, my, serial % 1000000)
    k = kc * np.exp(rng.normal(-W.SIGMA_K ** 2 / 2, W.SIGMA_K, N))
    first = my + (rng.beta(5, 3, N) - 0.625) * 1.2
    df = pd.DataFrame(dict(county=name, kind=kind, my=my, make=mk, model=[models[i][1] for i in mi], body=body,
                           cls=cls, fuel=fuel, gvwr=gvwr, owner=owner, vin=vins, k=k, first=first))
    df["plate"] = _plates(rng, N)
    chg = rng.random(N) < 0.015
    df["plate_test"] = np.where(chg, _plates(rng, N), df["plate"])
    arr = (kind == "active") & (rng.random(N) < 0.026) & (my <= 2024)
    df["arrived"] = np.where(arr, 2024.0 + rng.random(N) * 2.45, np.nan)
    mv = ((kind == "active") & (rng.random(N) < 0.013)) | ((kind == "pilot") & (rng.random(N) < 0.06))
    others = [c for c in W.NAMES if c != name]
    df["moved_from"] = np.where(mv, np.array(others)[rng.integers(0, len(others), N)], None)
    df["moved_on"] = np.where(mv, np.where(kind == "pilot", 2024.0 + rng.random(N) * 1.2, 2024.0 + rng.random(N) * 2.45), np.nan)
    dep = kind == "departed"
    df["left"] = np.where(dep, 2024.0 + rng.random(N) * 2.45, np.nan)
    df["left_how"] = np.where(dep, np.where(rng.random(N) < 0.72, "CANCELLED", "EXPIRED"), None)
    df["renewed"] = 2025.5 + rng.random(N) * 0.99
    df["u_cycle"] = rng.random(N)
    df["u_comp"] = rng.random(N)
    df["u_station"] = rng.random(N)
    df["u_odo"] = rng.normal(0, 1, N)
    df["u_pilot"] = rng.random(N)
    df["u_reinst"] = rng.random(N)
    return df


def _inspections(T):
    """The first biennial cycle: a vehicle's inspection year is set by the last digit of its VIN (even 2024, odd
    2025); arrivals inspect when they register; the four newest model years, diesels, electrics and trucks over
    8,500 pounds are exempt; the 2025 pilot took only vehicles already inspected."""
    import stations as S
    reg = S.register()
    subject = T["fuel"].isin(["G", "F", "H"]) & T["gvwr"].isin(["1", "2a"]) & (T["my"] >= W.FIRST_OBD_MY)
    yr = np.where(T["vin"].str[-1].astype(int) % 2 == 0, 2024, 2025)
    t = yr + T["u_cycle"].to_numpy()
    arr = T["arrived"].to_numpy()
    late = ~np.isnan(arr) & (arr > t - 0.1)
    t = np.where(late, np.minimum(arr + T["u_cycle"].to_numpy() * 0.08, 2025.995), t)
    out = ~np.isnan(arr) & (arr > 2025.99)
    yr_t = np.floor(t).astype(int)
    pil = (T["kind"] == "pilot").to_numpy() & (t > 2025.42)
    t = np.where(pil, 2024.0 + T["u_cycle"].to_numpy() * 1.40, t)
    yr_t = np.floor(t).astype(int)
    exempt = T["my"].to_numpy() > yr_t - W.EXEMPT_NEWEST
    gone = (T["kind"] == "departed").to_numpy() & (T["left"].to_numpy() <= t)
    noncomp = (T["u_comp"].to_numpy() > W.COMPLIANCE) & (T["kind"] != "pilot").to_numpy()
    tested = subject.to_numpy() & ~out & ~exempt & ~gone & ~noncomp
    T["tested"] = tested
    days = dec_days(t)
    T["test_date"] = np.where(tested, days, None)
    age = np.array([dec(d) for d in days]) - T["first"].to_numpy()
    odo = T["k"].to_numpy() * cum(np.maximum(age, 0.0)) * (1 + W.YEAR_NOISE * T["u_odo"].to_numpy() / np.sqrt(np.maximum(age, 1.0)))
    T["odo_true"] = np.where(tested, odo, np.nan)
    home = T["county"].to_numpy().astype(object)
    mf = T["moved_from"].to_numpy()
    mo = T["moved_on"].to_numpy()
    dd = np.array([dec(d) for d in days])
    before_move = np.array([isinstance(m, str) for m in mf]) & (mo > dd)
    home = np.where(before_move, mf, home)
    away = np.zeros(len(T), bool)
    nbi = np.zeros(len(T), int)
    lane_u = np.zeros(len(T))
    for name in W.NAMES:
        idx = np.where(T["county"].to_numpy() == name)[0]
        r = np.random.default_rng(W.SEED + 77 + W.CNO[name])
        away[idx] = r.random(len(idx)) < 0.16
        nbi[idx] = r.integers(0, 12, len(idx))
        lane_u[idx] = r.random(len(idx))
    where = np.array([S.NEIGHBOURS[h][j % len(S.NEIGHBOURS[h])] if a else h for h, a, j in zip(home, away, nbi)], dtype=object)
    u = T["u_station"].to_numpy()
    st = np.full(len(T), -1)
    ln = np.zeros(len(T), int)
    cuts = sorted({x["start"] for x in reg.s} | {x["end"] + dt.timedelta(days=1) for x in reg.s if x["end"]})
    bounds = [dt.date(2023, 1, 1)] + [c for c in cuts if c > dt.date(2023, 12, 31)] + [dt.date(2027, 1, 1)]
    for lo, hi in zip(bounds[:-1], bounds[1:]):
        inwin = tested & np.array([lo <= d < hi for d in days])
        for c in W.NAMES:
            idx = np.where(inwin & (where == c))[0]
            if not len(idx):
                continue
            cand = reg.open_in(c, max(lo, dt.date(2024, 1, 1)))
            w = np.cumsum([x["size"] for x in cand]); w = w / w[-1]
            pick = np.searchsorted(w, u[idx])
            st[idx] = [cand[j]["no"] for j in pick]
            ln[idx] = [1 + int(lane_u[i] * cand[j]["lanes"]) for i, j in zip(idx, pick)]
    T["station"] = np.where(tested, st, -1)
    T["lane"] = np.where(tested, ln, 0)


def _pilot(T):
    """The 2025 pilot's vehicles: surrendered to a licensed dismantler between June and December 2025; a few were
    taken back by their owners before the dismantler crushed them, and their titles were reinstated."""
    span = (W.PILOT_END - W.PILOT_START).days
    p = (T["kind"] == "pilot").to_numpy()
    T["surrendered"] = [W.PILOT_START + dt.timedelta(days=int(u * (span + 1))) if q else None
                        for u, q in zip(T["u_pilot"], p)]
    T["reinstated"] = p & (T["u_reinst"].to_numpy() < 0.075)
