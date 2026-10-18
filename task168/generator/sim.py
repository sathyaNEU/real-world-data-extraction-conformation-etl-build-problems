"""Departure-level simulation: demand, the booking build by day, sell-out, sold seats, flown passengers,
lap infants and the booking engines' turned-away request log.

One RNG stream per (season, route, direction, purpose) keyed by a stable string, so a record never depends on
the order other records were drawn in, and two builds give byte-identical output.
"""
import datetime as dt
import hashlib
import math
from zoneinfo import ZoneInfo

import numpy as np

import world as W

ROME = ZoneInfo("Europe/Rome")
UTC = ZoneInfo("UTC")
DAYS = np.arange(W.HORIZON, -1, -1)            # days before departure, 330 .. 0


def stream(*key):
    h = hashlib.sha256(("|".join(str(k) for k in (W.SEED,) + key)).encode()).digest()
    return np.random.default_rng(int.from_bytes(h[:8], "little"))


def season_dates(season):
    a, b = W.SEASONS[season]
    return [a + dt.timedelta(days=i) for i in range((b - a).days + 1)]


def season_factor(d, amp):
    return 1.0 + amp * (W.base_of(d) - 1.0)


def holiday_factor(d, outbound):
    """Demand lift around Easter, the spring bridges and Ferragosto: outbound (from the northern base) before
    the holiday, the return after it."""
    f = 1.0
    e = W.EASTER[d.year]
    delta = (d - e).days
    if outbound and -4 <= delta <= -1:
        f *= 1.16
    if (not outbound) and 1 <= delta <= 2:
        f *= 1.16
    for (m, day) in W.FIXED_HOLIDAYS:
        h = dt.date(d.year, m, day)
        k = (d - h).days
        if (m, day) == (8, 15):
            if outbound and -7 <= k <= -1:
                f *= 1.10
            if (not outbound) and 1 <= k <= 9:
                f *= 1.09
        else:
            if outbound and k == -1:
                f *= 1.08
            if (not outbound) and (k == 0 or (h.weekday() == 4 and k == 2)):
                f *= 1.07
    return f


def direction_factor(d, outbound):
    return W.direction_of[bool(outbound)](d)


def shape_mean(dates, freq, amp, outbound):
    """Unnormalised mean demand per departure for every departure of one leg in a season, in departure order
    (date, then rotation)."""
    out = []
    for d in dates:
        base = season_factor(d, amp) * W.DOW[d.weekday()] * holiday_factor(d, outbound) * direction_factor(d, outbound)
        for k in range(freq):
            out.append(base * W.TOD[freq][k])
    return np.array(out)


def curve(t, tau):
    return np.exp(-(np.maximum(t, 0.0) / tau) ** W.BETA)


def local_to_utc(d, hh, mm, ss=0):
    loc = dt.datetime(d.year, d.month, d.day, hh, mm, ss, tzinfo=ROME)
    return loc.astimezone(UTC)


# Hour-of-day weights (local time) for bookings and for requests by channel. Website and app traffic runs round
# the clock with an evening peak; the contact centre is open 08:00-22:00 and agencies work office hours.
BOOK_HOURS = np.array([0.6, 0.35, 0.2, 0.15, 0.2, 0.5, 1.2, 2.6, 4.1, 5.3, 6.0, 6.2, 5.8, 5.4, 5.6, 5.9, 5.8, 5.6,
                       5.7, 6.1, 6.6, 6.2, 4.2, 2.1])
REQ_HOURS = {
    "WEB": BOOK_HOURS,
    "APP": np.array([0.9, 0.5, 0.3, 0.2, 0.25, 0.5, 1.3, 2.9, 3.8, 4.3, 4.6, 4.9, 5.2, 4.9, 4.6, 4.7, 4.9, 5.1,
                     5.6, 6.4, 7.3, 7.6, 6.0, 3.4]),
    "CC": np.array([0, 0, 0, 0, 0, 0, 0, 0, 5.2, 7.4, 7.9, 7.6, 6.4, 5.9, 6.6, 6.9, 6.5, 6.0, 5.4, 4.6, 3.6,
                    2.4, 0, 0], float),
    "GDS": np.array([0.1, 0.05, 0.03, 0.03, 0.05, 0.1, 0.4, 2.2, 6.1, 8.3, 8.8, 8.4, 6.0, 5.4, 7.6, 8.1, 7.7, 6.3,
                     3.8, 1.6, 0.8, 0.5, 0.3, 0.2]),
}
SALES_CLOSE_MIN = 45     # sales close this many minutes before the scheduled departure


def day_window(dep_time, days_before):
    """Seconds after local midnight between which a booking or request for this departure can be made on the
    day that is days_before days before the departure date."""
    if days_before > 0:
        return 0, 24 * 3600 - 1
    hh, mm = (int(x) for x in dep_time.split(":"))
    return 0, hh * 3600 + mm * 60 - SALES_CLOSE_MIN * 60


def window_weight(weights, lo, hi):
    edges = np.arange(25) * 3600
    ov = np.clip(np.minimum(edges[1:], hi) - np.maximum(edges[:-1], lo), 0, None)
    return float((weights * ov).sum())


def draw_secs(rng, weights, lo, hi):
    """A time of day in [lo, hi) seconds, drawn from hourly weights (uniform within the hour)."""
    if hi - lo < 2:
        return lo
    edges = np.arange(25) * 3600
    ov = np.clip(np.minimum(edges[1:], hi) - np.maximum(edges[:-1], lo), 0, None)
    w = weights * ov
    if w.sum() <= 0:
        w = ov.astype(float)
    h = int(rng.choice(24, p=w / w.sum()))
    a, b = max(edges[h], lo), min(edges[h + 1], hi)
    return int(a + rng.random() * (b - a))


def secs_at_share(weights, lo, hi, f):
    """The time of day in [lo, hi) by which a share f of the day's bookings (hourly weights) has arrived."""
    edges = np.arange(25) * 3600
    ov = np.clip(np.minimum(edges[1:], hi) - np.maximum(edges[:-1], lo), 0, None)
    w = weights * ov / 3600.0
    c = np.concatenate([[0.0], np.cumsum(w)])
    if c[-1] <= 0:
        return int(lo + f * (hi - lo))
    target = f * c[-1]
    h = int(np.searchsorted(c, target, side="right") - 1)
    h = min(max(h, 0), 23)
    a, b = max(edges[h], lo), min(edges[h + 1], hi)
    part = (target - c[h]) / (c[h + 1] - c[h]) if c[h + 1] > c[h] else 0.0
    return int(a + part * (b - a))


class Leg:
    """All departures of one route direction in one season."""

    def __init__(self, season, orig, dest, freq, seats_by_date, df, amp, ns_route, kind, outbound, growth=1.0,
                 mu_seats=None, purpose="pack"):
        self.season, self.orig, self.dest, self.freq, self.kind = season, orig, dest, freq, kind
        self.outbound = outbound
        dates = season_dates(season)
        self.dates = dates
        rng = stream(season, orig, dest, purpose, "demand")
        rng_t = stream(season, orig, dest, purpose, "build")
        rng_f = stream(season, orig, dest, purpose, "flown")
        shape = shape_mean(dates, freq, amp, outbound)
        # mean demand normalised so the season mean equals df x the reference seats
        ref_seats = mu_seats if mu_seats is not None else seats_by_date(dates[0])
        mu = df * ref_seats * shape / shape.mean() * growth
        n = len(mu)
        self.n = n
        self.dep_date = [d for d in dates for _ in range(freq)]
        self.rot = [k for _ in dates for k in range(freq)]
        self.seats = np.array([seats_by_date(d) for d in self.dep_date])
        lam = mu * np.exp(rng.normal(0.0, W.SIG_D, n) - W.SIG_D ** 2 / 2)
        self.D = rng.poisson(lam)
        self.mean = mu
        tau_d = {d: W.tau_of(d) for d in dates}
        dows = np.array([d.weekday() for d in self.dep_date])
        self.tau = (np.array([tau_d[d] for d in self.dep_date]) * np.array([W.DOW_TAU[w] for w in dows])
                    * np.exp(rng_t.normal(0.0, W.SIG_TAU, n)))
        self.cum = np.zeros((n, len(DAYS)), dtype=np.int32)
        self.so_day = np.full(n, -1)            # days before departure of the sell-out day, -1 never
        self.so_frac = np.full(n, np.nan)       # share of the sell-out day's arrivals the last seat took
        self.arr = []                           # daily arrivals (kept for the turnaway log)
        for i in range(n):
            F = curve(DAYS.astype(float), self.tau[i])
            p = np.diff(np.concatenate([[0.0], F]))
            p = np.clip(p, 0, None)
            p /= p.sum()
            a = rng_t.multinomial(int(self.D[i]), p)
            c = np.cumsum(a)
            self.arr.append(a)
            self.cum[i] = c
            if c[-1] >= self.seats[i]:
                j = int(np.argmax(c >= self.seats[i]))
                before = c[j - 1] if j > 0 else 0
                self.so_day[i] = DAYS[j]
                self.so_frac[i] = (self.seats[i] - before) / a[j] if a[j] > 0 else 1.0
        booked = np.minimum(self.cum, self.seats[:, None])
        self.booked = booked                    # bookings on hand by day (capped)
        self.sold = booked[:, -1].copy()
        ns = np.clip(ns_route * np.exp(rng_f.normal(0.0, 0.15, n)), 0.0, 0.12)
        self.noshow = rng_f.binomial(self.sold, ns)
        self.flown = self.sold - self.noshow
        inf_rate = np.array([0.021 if d.month in (7, 8) else 0.015 for d in self.dep_date])
        self.inf = rng_f.binomial(self.flown, inf_rate)
        self.spill = np.maximum(self.D - self.seats, 0)

    # -------------------------------------------------------- derived fields
    def dep_time(self, i):
        times = W.OUT_TIMES[self.freq] if self.outbound else W.RET_TIMES[self.freq]
        return times[self.rot[i]]

    def sellout_local(self, i):
        """Local timestamp of the last seat sold: the point of the sell-out day's booking profile by which the
        share of that day's bookings the last seat took had arrived."""
        if self.so_day[i] < 0:
            return None
        day = self.dep_date[i] - dt.timedelta(days=int(self.so_day[i]))
        lo, hi = day_window(self.dep_time(i), int(self.so_day[i]))
        secs = secs_at_share(BOOK_HOURS, lo, hi, float(self.so_frac[i]))
        secs = min(max(secs, lo + 1), hi - 1)
        return dt.datetime(day.year, day.month, day.day, tzinfo=ROME) + dt.timedelta(seconds=secs)

    def equip_code(self, i):
        return {144: "319", 180: "320", 186: "32N", 220: "321", 232: "32Q"}[int(self.seats[i])]

    def snapshot(self, dcps):
        idx = [int(np.nonzero(DAYS == t)[0][0]) for t in dcps]
        return self.booked[:, idx]


# ------------------------------------------------------------------ the booking engines' turned-away requests
CHANNELS = ["WEB", "APP", "CC", "GDS"]
CHANNEL_MIX = {"S24": [0.50, 0.24, 0.07, 0.19], "S25": [0.44, 0.32, 0.06, 0.18]}
# share of refused parties that leave a record, by channel (a sold-out date is shown as such on the website and
# in the app, so most of those visitors never send a request; an agent or a contact-centre agent usually tries)
CAPTURE = {"WEB": 0.22, "APP": 0.10, "CC": 0.55, "GDS": 0.65}
PARTY = ([1, 2, 3, 4, 5, 6], [0.55, 0.27, 0.09, 0.06, 0.02, 0.01])
LIGHT_CLOSE = 0.70        # load at which the lowest fare family closes
LIGHT_ASK = 0.12          # share of parties arriving after that which ask for it first
RETRY = {"WEB": 0.30, "APP": 0.15, "CC": 0.0, "GDS": 0.0}
# Agency bookings that are one leg of a longer journey (an interline connection at the base) carry the journey's
# origin and destination in the feed's airport fields.
CONNECT_SHARE = 0.15
CONNECT = {"LIN": ["LHR", "LCY", "AMS", "CDG", "ORY", "FRA", "BRU", "DUS", "MAD"],
           "TRN": ["FRA", "MUC", "CDG", "AMS"], "VRN": ["FRA", "MUC", "AMS"],
           "VCE": ["FRA", "MUC", "CDG", "AMS", "LHR"], "BLQ": ["FRA", "MUC", "CDG", "AMS"]}


def _parties(rng, pax):
    out = []
    while pax > 0:
        k = int(rng.choice(PARTY[0], p=PARTY[1]))
        k = min(k, pax)
        out.append(k)
        pax -= k
    return out


def turnaway_events(leg, flight_numbers):
    """Rows for every request the engines refused on this leg's departures.

    Each event: (logged_at_utc, channel, session_ref, flight, dep_date, orig, dest, fare_family, pax, after_so,
    party, party_size, leg_orig, leg_dest) where the last five are the generator's own truth (the departure had
    sold out before the request; which refused party wrote the record and how many passengers it was; the leg the
    departure flies) and never ship.
    Requests before the sell-out are refused only for the lowest fare family, which closes at LIGHT_CLOSE of the
    seats; those parties then book a higher family (they are among the day's bookings).
    """
    rng = stream(leg.season, leg.orig, leg.dest, "turnaway")
    rng_j = stream(leg.season, leg.orig, leg.dest, "journey")
    mix = CHANNEL_MIX[leg.season]
    ev = []
    for i in range(leg.n):
        a = leg.arr[i]
        seats = leg.seats[i]
        c = leg.cum[i]
        dep = leg.dep_date[i]
        flt = flight_numbers[i]
        dtime = leg.dep_time(i)
        jl = int(np.argmax(c >= LIGHT_CLOSE * seats)) if c[-1] >= LIGHT_CLOSE * seats else None
        jso = int(np.argmax(c >= seats)) if c[-1] >= seats else None
        so = leg.sellout_local(i)
        so_secs = so.hour * 3600 + so.minute * 60 + so.second if so is not None else None
        for j in range(len(DAYS)):
            if a[j] == 0:
                continue
            day = dep - dt.timedelta(days=int(DAYS[j]))
            lo_d, hi_d = day_window(dtime, int(DAYS[j]))
            before = c[j - 1] if j > 0 else 0
            booked_today = a[j] if jso is None or j < jso else (max(seats - before, 0) if j == jso else 0)
            spilled_today = a[j] - booked_today
            if jl is not None and j >= jl and booked_today > 0:
                for k in _parties(rng, int(booked_today)):
                    if rng.random() < LIGHT_ASK:
                        ch = CHANNELS[int(rng.choice(4, p=mix))]
                        if rng.random() < CAPTURE[ch]:
                            lo, hi = lo_d, hi_d
                            cap = None
                            if jso is not None and j == jso:
                                hi = so_secs - 600
                                cap = so_secs - 30
                            if hi - lo < 120 or window_weight(REQ_HOURS[ch], lo, hi) <= 0:
                                continue
                            secs = draw_secs(rng, REQ_HOURS[ch], lo, hi)
                            ev.extend(_rows(rng, ch, day, secs, flt, dep, leg, "LIGHT", k, False, cap or hi_d,
                                            (leg.orig, leg.dest, i, j, len(ev)), rng_j))
            if spilled_today > 0:
                for k in _parties(rng, int(spilled_today)):
                    ch = CHANNELS[int(rng.choice(4, p=mix))]
                    if rng.random() < CAPTURE[ch]:
                        lo = lo_d
                        if jso is not None and j == jso:
                            lo = so_secs + 30
                        hi = hi_d
                        if hi - lo < 120 or window_weight(REQ_HOURS[ch], lo, hi) <= 0:
                            continue
                        secs = draw_secs(rng, REQ_HOURS[ch], lo, hi)
                        fam = ["LIGHT", "CLASSIC", "FLEX"][int(rng.choice(3, p=[0.55, 0.35, 0.10]))]
                        ev.extend(_rows(rng, ch, day, secs, flt, dep, leg, fam, k, True, hi_d,
                                        (leg.orig, leg.dest, i, j, len(ev)), rng_j))
    return ev


_SESS = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"


def _session(rng, ch):
    if ch == "GDS":
        return "".join(_SESS[int(x)] for x in rng.integers(10, len(_SESS), 6))
    if ch == "CC":
        return "CC%07d" % int(rng.integers(0, 10 ** 7))
    return "".join("0123456789abcdef"[int(x)] for x in rng.integers(0, 16, 16))


def _rows(rng, ch, day, secs, flt, dep, leg, fam, pax, after, last_secs, pid, rng_j):
    """The records one refused party leaves. The agency feed writes one record per passenger name under the
    booking reference, a second apart, each carrying the passengers in the booking, and writes the journey's origin
    and destination when the booking is one leg of a connection; the website and the app write one record per
    request, and a visitor who asks again in the same session writes another; the contact centre writes one record
    per call."""
    base = dt.datetime(day.year, day.month, day.day, tzinfo=ROME)
    t_loc = base + dt.timedelta(seconds=int(secs))
    sess = _session(rng, ch)
    rows = []
    o, d = leg.orig, leg.dest
    if ch == "GDS":
        if rng_j.random() < CONNECT_SHARE:
            hub = leg.orig if leg.outbound else leg.dest
            far = CONNECT[hub][int(rng_j.integers(0, len(CONNECT[hub])))]
            o, d = (far, leg.dest) if leg.outbound else (leg.orig, far)
        for p in range(pax):
            rows.append(((t_loc + dt.timedelta(seconds=p)).astimezone(UTC), ch, sess, flt, dep, o, d,
                         fam, pax, after, pid, pax, leg.orig, leg.dest))
        return rows
    rows.append((t_loc.astimezone(UTC), ch, sess, flt, dep, o, d, fam, pax, after, pid, pax, leg.orig, leg.dest))
    if rng.random() < RETRY[ch]:
        t = secs
        for r in range(int(rng.integers(1, 3))):
            t = t + int(rng.integers(40, 400))
            if t >= last_secs:
                break
            rows.append(((base + dt.timedelta(seconds=t)).astimezone(UTC), ch, sess, flt, dep, o, d,
                         fam, pax, after, pid, pax, leg.orig, leg.dest))
    return rows
