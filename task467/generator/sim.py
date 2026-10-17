"""The clean truth and the records it leaves: every taxi trip that began or ended at Velmont International Airport from
2023 to August 2026, the licences that drove them and the brokerages they belonged to on each day, then the records
the Vehicle-for-Hire Office received (voided trips with their reversals, store-and-forward trips sent late and, from
the January 2026 meter firmware, the Corvane units' re-sent copies)."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import world as W

DAYS = [W.FIRST_DAY + dt.timedelta(days=i) for i in range((W.LAST_DAY - W.FIRST_DAY).days + 1)]
NDAY = len(DAYS)
DAY_INDEX = {d: i for i, d in enumerate(DAYS)}
ZONES = W.CITY_ZONES
NZ = len(ZONES)
ZI = {z: i for i, z in enumerate(ZONES)}
DAY64 = np.array(DAYS, dtype="datetime64[D]")

# arrivals leave the rank on the airport's arrival banks; departures reach the forecourt on its departure banks
HOUR_P = [0.62, 0.16, 0.03, 0.01, 0.01, 0.04, 0.78, 2.35, 3.55, 3.20, 2.45, 2.20, 2.60, 3.05, 3.40, 3.55, 3.85,
          4.40, 4.55, 4.25, 3.80, 4.05, 3.90, 2.55]
HOUR_D = [0.06, 0.02, 0.01, 0.03, 0.92, 3.70, 4.55, 3.45, 2.60, 2.40, 2.60, 2.90, 3.00, 3.10, 3.20, 3.40, 3.45,
          3.20, 2.80, 2.40, 1.90, 1.30, 0.62, 0.22]


def rngs():
    return {k: np.random.default_rng([W.SEED, i]) for i, k in enumerate(
        ("shares", "months", "days", "times", "attrs", "fleet", "assign", "voids", "late", "resend", "ids", "pax"))}


# ---------------------------------------------------------------- where the trips go
def zone_shares(r):
    """The share of the airport's pickups bound for each city zone and of its drop-offs coming from each, before the
    line: the station zones per W.STATION_SPLIT_*, the rest falling off with distance and differing a little by
    direction (residents ride home from the airport more than to it)."""
    others = W.OTHER_ZONES
    km = np.array([W.ZONE[z][2] for z in others])
    base = np.exp(-km / 17.0) * np.exp(r.normal(0, 0.35, len(others)))
    base[others.index(38)] *= 0.55
    tilt = np.exp(r.normal(0, 0.18, len(others)))
    wp = base * tilt
    wd = base / tilt
    sp = {z: W.STATION_SHARE_P * W.STATION_SPLIT_P[z] for z in W.STATION_ZONES}
    sd = {z: W.STATION_SHARE_D * W.STATION_SPLIT_D[z] for z in W.STATION_ZONES}
    sp.update({z: (1 - W.STATION_SHARE_P) * w / wp.sum() for z, w in zip(others, wp)})
    sd.update({z: (1 - W.STATION_SHARE_D) * w / wd.sum() for z, w in zip(others, wd)})
    return np.array([sp[z] for z in ZONES]), np.array([sd[z] for z in ZONES])


def expected(sp, sd):
    """Expected trips a day by zone, pickups and drop-offs: traffic growth, the month, the weekday, the line on the
    station zones from 4 November 2024 and the temporary rank on pickups until 2027."""
    ep = np.zeros((NDAY, NZ))
    ed = np.zeros((NDAY, NZ))
    station = np.array([z in W.STATION_ZONES for z in ZONES])
    for i, d in enumerate(DAYS):
        g = (1 + W.GROWTH) ** ((d - dt.date(2024, 7, 1)).days / 365.25)
        s = W.SEAS[d.month - 1] / (sum(W.SEAS) / 12)
        line = np.where(station & (d >= W.CHANGE), W.LINE, 1.0)
        rank = W.RANK if W.CHANGE <= d < W.RETURN else 1.0
        lean = W.TILT[d.month - 1]
        ep[i] = W.P_DAY * g * s * (1 + lean) * W.DOW_P[d.weekday()] * sp * line * rank
        ed[i] = W.D_DAY * g * s * (1 - lean) * W.DOW_D[d.weekday()] * sd * line
    return ep, ed


def stoch_round(x, r):
    f = np.floor(x)
    return (f + (r.random(np.shape(x)) < (x - f))).astype(int)


def daily_counts(ep, ed, r_m, r_d):
    """Each zone-month's count drawn once for both directions (a month's shock and a zone's month shock shared by
    pickups and drop-offs, a small one each), then spread over the month's days by expected value and a day's
    shock shared across the airport."""
    cp = np.zeros((NDAY, NZ), dtype=int)
    cd = np.zeros((NDAY, NZ), dtype=int)
    dayshock = np.exp(r_d.normal(0, 0.05, NDAY))
    for (y, m) in W.months():
        idx = [i for i, d in enumerate(DAYS) if (d.year, d.month) == (y, m)]
        sm = math.exp(r_m.normal(0, 0.02))
        u = np.exp(r_m.normal(0, 0.03, NZ))
        eP = ep[idx].sum(0) * sm * u * np.exp(r_m.normal(0, 0.006, NZ))
        eD = ed[idx].sum(0) * sm * u * np.exp(r_m.normal(0, 0.006, NZ))
        nP, nD = stoch_round(eP, r_m), stoch_round(eD, r_m)
        for j in range(NZ):
            for arr, n, e in ((cp, nP[j], ep), (cd, nD[j], ed)):
                if n:
                    w = e[idx, j] * dayshock[idx]
                    arr[idx, j] = r_d.multinomial(n, w / w.sum())
    return cp, cd


# ---------------------------------------------------------------- the licences and their brokerages
def fleet(r):
    """Taxi licences that serve the airport, each with a meter vendor, an activity weight and its affiliation spells.
    Licences change brokerage at the 1 January renewal (about one in nine) and now and then during a year; a few are
    surrendered and new ones issued."""
    bro = list(W.BROKERAGES)
    bw = np.array([0.22, 0.20, 0.16, 0.18, 0.14, 0.10])
    lic = []
    nxt = 1001

    def new(start, b=None):
        nonlocal nxt
        v = dict(vid="VT%04d" % nxt, vendor=1 + int(r.random() < 0.45), w=float(np.exp(r.normal(0, 0.45))),
                 start=start, end=None, spells=[[int(b or r.choice(bro, p=bw)), start, None]])
        nxt += 1
        lic.append(v)
        return v

    for _ in range(214):
        new(dt.date(2015, 1, 1) + dt.timedelta(days=int(r.integers(0, 2900))))

    def switch(v, day):
        cur = v["spells"][-1][0]
        others = [b for b in bro if b != cur]
        p = np.array([bw[bro.index(b)] for b in others])
        v["spells"][-1][2] = day - dt.timedelta(days=1)
        v["spells"].append([int(r.choice(others, p=p / p.sum())), day, None])

    for year in (2023, 2024, 2025, 2026):
        jan1 = dt.date(year, 1, 1)
        active = [v for v in lic if v["end"] is None and v["start"] < jan1]
        if year > 2023:
            for v in active:
                if r.random() < 0.11:
                    switch(v, jan1)
        last = W.LAST_DAY if year == 2026 else dt.date(year, 12, 31)
        span = (last - jan1).days
        for v in list(active):
            if r.random() < 0.03 * span / 365:
                switch(v, jan1 + dt.timedelta(days=int(r.integers(20, span))))
            if r.random() < 0.035 * span / 365:
                day = jan1 + dt.timedelta(days=int(r.integers(10, span)))
                if day > v["spells"][-1][1]:
                    v["end"] = day
                    v["spells"][-1][2] = day
                    new(day + dt.timedelta(days=int(r.integers(1, 30))), v["spells"][-1][0])
    return lic


def force_renewal_moves(lic, r):
    """At the 2026 renewal every brokerage both lost and gained at least two licences that drove all of 2025."""
    jan = dt.date(2026, 1, 1)
    full = [v for v in lic if v["start"] <= dt.date(2025, 1, 1) and (v["end"] is None or v["end"] > dt.date(2026, 2, 10))]

    def moved(v):
        return any(s[1] == jan for s in v["spells"])

    def held(v, day):
        return next(s[0] for s in v["spells"] if s[1] <= day and (s[2] is None or day <= s[2]))

    for b in W.BROKERAGES:
        out = [v for v in full if moved(v) and held(v, dt.date(2025, 12, 31)) == b]
        inn = [v for v in full if moved(v) and held(v, jan) == b]
        while len(out) < 2 or len(inn) < 2:
            cands = [v for v in full if not moved(v) and len(v["spells"]) == 1 and v["spells"][0][2] is None]
            v = cands[int(r.integers(0, len(cands)))]
            src = v["spells"][0][0]
            if len(out) < 2 and src == b:
                tgt = [c for c in W.BROKERAGES if c != b][int(r.integers(0, 5))]
            elif len(inn) < 2 and src != b:
                tgt = b
            else:
                continue
            v["spells"][0][2] = jan - dt.timedelta(days=1)
            v["spells"].append([tgt, jan, None])
            out = [v for v in full if moved(v) and held(v, dt.date(2025, 12, 31)) == b]
            inn = [v for v in full if moved(v) and held(v, jan) == b]


def brokerage_on(v, day):
    for b, a, z in v["spells"]:
        if a <= day and (z is None or day <= z):
            return b
    return v["spells"][-1][0]


def latest_brokerage(v, built):
    """The brokerage an annual file built on `built` stamps on a licence's trips: the licence's spell that day, or its
    last spell if it was surrendered before then."""
    for b, a, z in v["spells"]:
        if a <= built and (z is None or built <= z):
            return b
    return v["spells"][-1][0]


# ---------------------------------------------------------------- the trips
def hour_draw(n, prof, r):
    p = np.array(prof) / sum(prof)
    h = r.choice(24, size=n, p=p)
    return h * 3600 + r.integers(0, 3600, n)


def speed(h):
    return np.where((h >= 7) & (h < 9) | (h >= 16) & (h < 18), 29.0, np.where((h >= 22) | (h < 6), 56.0, 43.0))


def make_trips(cp, cd, lic, R):
    """One row per trip, pickups and drop-offs, before any record is written."""
    rows = []
    for direction, counts in (("P", cp), ("D", cd)):
        di, zj = np.nonzero(counts)
        n = counts[di, zj]
        day = np.repeat(di, n)
        zone = np.array(ZONES)[np.repeat(zj, n)]
        rows.append(pd.DataFrame({"dir": direction, "day": day, "zone": zone}))
    t = pd.concat(rows, ignore_index=True)
    return finish(t, lic, R, "trip")


def finish(t, lic, R, kind):
    r = R["times"]
    n = len(t)
    pick = (t["dir"] == "P").to_numpy()
    sec = np.where(pick, hour_draw(n, HOUR_P, r), hour_draw(n, HOUR_D, r))
    km_zone = np.array([W.ZONE[z][2] for z in t["zone"]])
    km = np.round(km_zone * R["attrs"].uniform(0.92, 1.13, n) + R["attrs"].uniform(0.3, 1.4, n), 2)
    hr = (sec // 3600).astype(int)
    mins = km / speed(hr) * 60 + R["attrs"].uniform(1.5, 6.5, n)
    dur = np.round(mins * 60).astype(int)
    base = DAY64[t["day"].to_numpy()].astype("datetime64[s]")
    anchor = base + sec.astype("timedelta64[s]")
    # a pickup's meter starts at the rank; a drop-off's anchor is its arrival at the forecourt
    on = np.where(pick, anchor, anchor - dur.astype("timedelta64[s]"))
    off = on + dur.astype("timedelta64[s]")
    t = t.assign(meter_on=on, meter_off=off, km=km, wait=np.round(R["attrs"].uniform(0, 1, n) ** 2 * 7, 1))
    t["kind"] = kind
    assign_vehicles(t, lic, R)
    price(t, R, lic)
    return t


TURN = 25 * 60     # seconds: no taxi starts a trip within 25 minutes of ending its last
BUSY = {}          # licence index -> (sorted starts, ends) of the trips already given to it


def assign_vehicles(t, lic, R):
    """Each trip to a licence active that day, drawn by the licences' activity, and free: no taxi starts a trip within
    25 minutes of ending another (the holding lot's queue after a drop-off, the run back after a pickup)."""
    import bisect
    r = R["assign"]
    on = t["meter_on"].to_numpy().astype("datetime64[s]").astype(np.int64)
    off = t["meter_off"].to_numpy().astype("datetime64[s]").astype(np.int64)
    days = t["day"].to_numpy()
    pick = np.empty(len(t), dtype=np.int64)
    active = {}
    for i in np.argsort(on, kind="stable"):
        d = int(days[i])
        if d not in active:
            day = DAYS[d]
            act = [k for k, v in enumerate(lic) if v["start"] <= day and (v["end"] is None or day < v["end"])]
            active[d] = (act, np.cumsum([lic[k]["w"] for k in act]))
        act, cw = active[d]
        for _ in range(2000):
            k = act[int(np.searchsorted(cw, r.random() * cw[-1], side="right"))]
            st, en = BUSY.setdefault(k, ([], []))
            j = bisect.bisect_left(st, off[i] + TURN)
            if j == 0 or en[j - 1] + TURN <= on[i]:
                st.insert(j, int(on[i]))
                en.insert(j, int(off[i]))
                pick[i] = k
                break
        else:
            raise RuntimeError("no free licence on day %d" % d)
    t["vehicle"] = [lic[k]["vid"] for k in pick]
    on_day = pd.to_datetime(t["meter_on"]).dt.date.to_numpy()
    t["vendor"] = [lic[k]["vendor"] for k in pick]
    t["brokerage"] = [brokerage_on(lic[k], dd) for k, dd in zip(pick, on_day)]


REPROGRAM = {}


def reprogram_day(vid, year, r):
    key = (vid, year)
    if key not in REPROGRAM:
        REPROGRAM[key] = dt.date(year, 1, 1) + dt.timedelta(days=int(r.integers(1, 23)))
    return REPROGRAM[key]


def price(t, R, lic):
    """The Office's rate order (2025 raised the flag and the distance rate), the fee the meter charges on an airport
    pickup (last year's until the meter is reprogrammed in January), tips on cards."""
    r = R["attrs"]
    n = len(t)
    on = pd.to_datetime(t["meter_on"])
    year = on.dt.year.to_numpy()
    flag = np.where(year >= 2025, 4.25, 4.10)
    rate = np.where(year >= 2025, 2.02, 1.95)
    waitr = np.where(year >= 2025, 0.64, 0.62)
    fare = np.round((flag + rate * t["km"].to_numpy() + waitr * t["wait"].to_numpy()) * 20) / 20
    pick = (t["dir"] == "P").to_numpy()
    fee = np.zeros(n)
    dates = on.dt.date.to_numpy()
    for i in np.nonzero(pick)[0]:
        d = dates[i]
        fee[i] = W.FEES[d.year] if d >= reprogram_day(t["vehicle"].iat[i], d.year, R["fleet"]) else W.FEES[d.year - 1]
    pay = r.choice([1, 2, 3], size=n, p=[0.72, 0.23, 0.05])
    tip = np.where(pay == 1, np.round(fare * r.uniform(0.08, 0.21, n), 2) * (r.random(n) > 0.06), 0.0)
    pax = R["pax"].choice([1, 2, 3, 4], size=n, p=[0.62, 0.24, 0.09, 0.05])
    t["fare"] = fare
    t["fee"] = fee
    t["tip"] = tip
    t["total"] = np.round(fare + fee + tip, 2)
    t["pay"] = pay
    t["pax"] = pax


def voids(cp, cd, lic, R):
    """Voided trips: a meter started and the trip voided (the passenger gone, a dispute settled at the rank); the meter
    sends the trip and then its reversal. None is a trip."""
    r = R["voids"]
    vp = r.poisson(cp * W.VOID_RATE)
    vd = r.poisson(cd * W.VOID_RATE)
    t = make_trips(vp, vd, lic, R)
    t["kind"] = "void"
    t["km"] = np.round(t["km"] * r.uniform(0.02, 0.15, len(t)), 2)
    flag = np.where(pd.to_datetime(t["meter_on"]).dt.year >= 2025, 4.25, 4.10)
    t["fare"] = np.round((flag + 2.0 * t["km"]) * 20) / 20
    t["tip"] = 0.0
    t["total"] = np.round(t["fare"] + t["fee"], 2)
    t["meter_off"] = t["meter_on"] + (r.integers(40, 400, len(t))).astype("timedelta64[s]")
    rev = t.copy()
    rev["kind"] = "reversal"
    for c in ("fare", "fee", "tip", "total"):
        rev[c] = -rev[c]
    return t, rev


def receive(t, R):
    """When each record reached the Office: minutes after the meter stopped, days for a store-and-forward record."""
    r = R["late"]
    n = len(t)
    late = r.random(n) < W.LATE_RATE
    delay = np.where(late, r.integers(86400, 9 * 86400, n), r.integers(8, 1200, n))
    t["received"] = t["meter_off"] + delay.astype("timedelta64[s]")
    t["sf"] = np.where(late | (r.random(n) < 0.021), "Y", "N")
    return t


def resends(t, R):
    """From the January 2026 firmware, a Corvane unit that loses its connection re-sends its unacknowledged trips once
    it reconnects; the Office's intake gives each copy a new record number, and the unit writes the copy's meter times
    to the minute."""
    r = R["resend"]
    base = t[(t["kind"] == "trip") & (t["vendor"] == 2) &
             (pd.to_datetime(t["meter_on"]) >= pd.Timestamp(W.UTC_FROM))]
    take = base[r.random(len(base)) < W.RESEND_RATE].copy()
    take["kind"] = "resend"
    take["meter_on"] = take["meter_on"].dt.floor("min")
    take["meter_off"] = take["meter_off"].dt.floor("min")
    take["received"] = take["received"] + (r.integers(86400, 12 * 86400, len(take))).astype("timedelta64[s]")
    take["sf"] = "Y"
    return take


def everything():
    """The world: the truth, the records and everything the documents quote."""
    REPROGRAM.clear()
    BUSY.clear()
    R = rngs()
    sp, sd = zone_shares(R["shares"])
    ep, ed = expected(sp, sd)
    cp, cd = daily_counts(ep, ed, R["months"], R["days"])
    lic = fleet(R["fleet"])
    force_renewal_moves(lic, R["fleet"])
    trips = make_trips(cp, cd, lic, R)
    v, rev = voids(cp, cd, lic, R)
    trips = receive(trips, R)
    v = receive(v, R)
    rev["received"] = v["received"].to_numpy() + R["late"].integers(1800, 3 * 86400, len(rev)).astype("timedelta64[s]")
    rev["sf"] = "N"
    # a void whose reversal would reach the Office after the last monthly file closes is left out with it (in that
    # file it would be indistinguishable from a trip)
    cut = np.datetime64(W.LAST_DAY + dt.timedelta(days=1))
    edge = (v["received"].to_numpy() < cut) & (rev["received"].to_numpy() >= cut)
    v, rev = v[~edge], rev[~edge]
    rs = resends(trips, R)
    recs = pd.concat([trips, v, rev, rs], ignore_index=True)
    recs = recs.sort_values(["received", "meter_on", "vehicle"], kind="stable").reset_index(drop=True)
    recs["rid"] = 41_870_000 + np.arange(len(recs)) * 1 + R["ids"].integers(0, 3, len(recs)).cumsum()
    return dict(sp=sp, sd=sd, ep=ep, ed=ed, cp=cp, cd=cd, lic=lic, recs=recs)


def truth(x):
    """The trips themselves, one row each, voided trips and copies out."""
    r = x["recs"]
    return r[r["kind"] == "trip"]
