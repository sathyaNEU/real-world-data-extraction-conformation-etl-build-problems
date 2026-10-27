"""task270 world, the mood app: the patients each community team assessed in 2026, their care episodes, their app
codes and assessment fortnights, and every prompt the trust's app sent them with the ratings they gave.

Negative affect wanders and returns: each patient's level follows an Ornstein-Uhlenbeck process (a standard deviation
sigma about the patient's own mean, returning with a time constant tau hours of waking life; a night's sleep counts as
the patient's own half hour to an hour and a half, so the first rating of a day carries much of the evening's), seen
through four items each with its own error and the app's own resolution (sliders to 0 to 100 before 15 June 2026,
buttons 0 to 10 after). The trust's app prompted once at a random minute in each of eight 90-minute blocks from 9:00,
so adjacent ratings sat about 90 minutes apart; the collaborative's app prompts every three hours. Each patient is
drawn so that the change in negative affect their own process gives over three hours sits in a band: low (1.0 to 1.6),
mid (2.35 to 2.6) or high (3.05 to 3.8), and the bands' mix differs by team."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

# current team, patients with a completed 2026 fortnight, share high, share mid, mean answering rate
SPEC = {"BW-CM02": (59, .48, .07, .70), "BW-CM05": (55, .46, .07, .74), "BW-CM11": (53, .10, .46, .88),
        "BW-CM31": (56, .11, .45, .86), "BW-CM17": (49, .08, .47, .90), "BW-CM03": (51, .05, .07, .68),
        "BW-CM08": (55, .04, .07, .62), "BW-CM20": (48, .04, .06, .77), "BW-CM09": (52, .04, .08, .66),
        "BW-CM22": (47, .04, .06, .73), "BW-CM12": (53, .04, .07, .65)}
BANDS = {"low": (1.0, 1.6), "mid": (2.35, 2.6), "high": (3.05, 3.8)}
ITEM_OFFSET = np.array([0.35, 0.5, -0.4, -0.45])       # down, anxious, irritable, ashamed
CODE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def diurnal(hours):
    """The mean shift in negative affect by local clock hour: a morning lift that fades by early afternoon and a
    smaller evening rise."""
    h = np.asarray(hours, float)
    return 0.32 * np.exp(-(h - 9.0) / 2.2) + 0.12 * np.clip(h - 18.0, 0, None) / 3.0


def three_hour_change(sig, tau, noise_var):
    """The expected squared change in negative affect between two ratings three hours apart, before the app's
    rounding and its floor and ceiling, averaged over the collaborative's four same-day pairs."""
    d = diurnal(np.array(K.COLLAB_TIMES, float))
    return 2 * sig ** 2 * (1 - math.exp(-3 / tau)) + 2 * noise_var + float(np.mean(np.diff(d) ** 2))


class Patient:
    pass


def draw_patient(r, team, cls, comp):
    p = Patient()
    p.team, p.cls = team, cls
    p.tau = float(r.uniform(4.0, 8.0))
    p.item_sd = float(r.uniform(0.55, 0.85))
    noise_var = p.item_sd ** 2 / 4 + 1 / 48
    p.target = float(r.uniform(*BANDS[cls]))
    d = diurnal(np.array(K.COLLAB_TIMES, float))
    rest = p.target ** 2 - 2 * noise_var - float(np.mean(np.diff(d) ** 2))
    p.sig = math.sqrt(max(rest, 0.05) / (2 * (1 - math.exp(-3 / p.tau))))
    lo, hi = {"low": (2.0, 5.0), "mid": (3.5, 5.4), "high": (4.0, 5.8)}[cls]
    p.mu = float(r.uniform(lo, hi))
    p.night = float(r.uniform(0.4, 1.4))
    p.comp = float(np.clip(r.normal(comp, 0.09), 0.52, 0.96))
    return p


def code(r, used, prefix="BWM-"):
    while True:
        c = prefix + "".join(CODE_CHARS[i] for i in r.integers(0, len(CODE_CHARS), 5))
        if c not in used:
            used.add(c)
            return c


def schedule_day(r, day):
    """The trust app's eight prompts on a day: a random second in each 90-minute block from 9:00, at least 30 minutes
    after the one before (local wall times)."""
    out, prev = [], None
    base = dt.datetime(day.year, day.month, day.day, 9, 0)
    for b in range(K.BLOCKS):
        for _ in range(40):
            t = base + dt.timedelta(seconds=int(r.integers(0, K.BLOCK_MIN * 60)) + b * K.BLOCK_MIN * 60)
            if prev is None or (t - prev).total_seconds() >= 1800:
                break
        out.append(t)
        prev = t
    return out


def simulate_fortnight(r, p, first, stop_day=None):
    """Every prompt of a fortnight beginning on `first`: (day, block, sent local, answered local or None, item values
    or None). stop_day: the patient stops answering from that day (a fortnight that ends early)."""
    rows = []
    x = p.mu + p.sig * r.standard_normal()
    last_t = None
    day_rate = None
    for k in range(14):
        day = first + dt.timedelta(days=k)
        day_rate = float(np.clip(p.comp + r.normal(0, 0.11), 0.05, 0.99))
        for b, sent in enumerate(schedule_day(r, day)):
            answered = None
            if (stop_day is None or k < stop_day) and r.random() < day_rate:
                delay = min(float(r.exponential(330)), 1795.0)
                answered = sent + dt.timedelta(seconds=int(delay))
            vals = None
            if answered is not None:
                if last_t is not None:
                    a = math.exp(-waking_hours(p, last_t, answered) / p.tau)
                    x = p.mu + (x - p.mu) * a + p.sig * math.sqrt(1 - a * a) * r.standard_normal()
                last_t = answered
                hour = answered.hour + answered.minute / 60.0
                vals = x + float(diurnal([hour])[0]) + ITEM_OFFSET + p.item_sd * r.standard_normal(4)
            rows.append((k, b, sent, answered, vals))
    return rows


def truth_rmssd(p, days=500):
    """The patient's emotional instability as the collaborative's app records it over a long run: prompts at 9:00,
    12:00, 15:00, 18:00 and 21:00 answered on the hour, items on 0 to 10 buttons."""
    r = K.rng("truth", p.number)
    x = p.mu + p.sig * r.standard_normal()
    t_prev = None
    sq = []
    for k in range(days):
        vals = []
        for h in K.COLLAB_TIMES:
            t = k * 24.0 + h
            if t_prev is not None:
                a = math.exp(-((t - t_prev) - (11.0 - p.night) * (int(t // 24) - int(t_prev // 24))) / p.tau)
                x = p.mu + (x - p.mu) * a + p.sig * math.sqrt(1 - a * a) * r.standard_normal()
            t_prev = t
            items = np.clip(np.round(x + float(diurnal([h])[0]) + ITEM_OFFSET + p.item_sd * r.standard_normal(4)), 0, 10)
            vals.append(items.mean())
        sq.extend(np.diff(vals) ** 2)
    return float(math.sqrt(np.mean(sq)))


def classes(r, n, ph, pm):
    """A team's patients by band, in a shuffled order: the high and mid counts are the shares of n rounded."""
    out = ["high"] * int(round(n * ph)) + ["mid"] * int(round(n * pm))
    out += ["low"] * (n - len(out))
    return [out[i] for i in r.permutation(n)]


def waking_hours(p, t0, t1):
    """The hours of waking life between two ratings: a night's sleep counts as the patient's own few hours however
    long it lasts, so mood at the first prompt of a day carries much of the evening's."""
    nights = (t1.date() - t0.date()).days
    return (t1 - t0).total_seconds() / 3600.0 - (11.0 - p.night) * nights


def fortnight_start(r, lo, hi):
    while True:
        d = lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days + 1)))
        if d.weekday() < 5 or r.random() < 0.15:
            return d


def build():
    """Patients, each with: number, team history (episodes), fortnights (each with its prompts), app codes."""
    r = K.rng("world")
    used_codes, used_numbers = set(), set()
    patients = []
    for team, (n, ph, pm, comp) in SPEC.items():
        rt = K.rng("team", team)
        for cls in classes(rt, n, ph, pm):
            p = draw_patient(rt, team, cls, comp)
            while True:
                num = str(int(rt.integers(1000000, 1999999)))
                if num not in used_numbers:
                    used_numbers.add(num)
                    break
            p.number = num
            patients.append(p)
    # each patient's latest completed 2026 fortnight, any earlier 2026 fortnight, and a later one that ended early
    for p in patients:
        rp = K.rng("fortnights", p.number)
        last = fortnight_start(rp, K.FIRST_FORTNIGHT, K.LAST_FORTNIGHT)
        p.fortnights = []
        if last > dt.date(2026, 7, 20) and rp.random() < 0.13:
            p.fortnights.append(("earlier", fortnight_start(rp, K.FIRST_FORTNIGHT, last - dt.timedelta(days=150))))
        p.fortnights.append(("latest", last))
        if last < dt.date(2026, 10, 1) and rp.random() < 0.06:
            p.fortnights.append(("ended_early", fortnight_start(rp, last + dt.timedelta(days=60), K.LAST_FORTNIGHT)))
    # patients assessed in 2026 whose only fortnight did not complete (not in any team's count)
    extra = []
    for team, (n, ph, pm, comp) in SPEC.items():
        rt = K.rng("incomplete", team)
        for i in range(int(round(n * 0.08)) + int(rt.integers(0, 3))):
            u = rt.random()
            cls = "high" if u < ph else ("mid" if u < ph + pm else "low")
            p = draw_patient(rt, team, cls, comp - 0.18)
            while True:
                num = str(int(rt.integers(1000000, 1999999)))
                if num not in used_numbers:
                    used_numbers.add(num)
                    break
            p.number = num
            p.fortnights = [("incomplete", fortnight_start(rt, K.FIRST_FORTNIGHT, K.LAST_FORTNIGHT))]
            extra.append(p)
    allp = patients + extra
    # team history: segments in today's teams, then Haddersley split North and South before 1 October
    others = [c for c, _ in K.TEAMS]
    for p in allp:
        rh = K.rng("episodes", p.number)
        dates = [f for _, f in p.fortnights]
        start = min(dates) - dt.timedelta(days=int(rh.integers(40, 700)))
        if p.team == "BW-CM31" and min(dates) >= K.MERGER and rh.random() < 0.25:
            start = K.MERGER + dt.timedelta(days=int(rh.integers(0, 30)))
            start = min(start, min(dates) - dt.timedelta(days=3))
        segs = [[p.team, start, None, ""]]
        if rh.random() < 0.09:
            other = [c for c in others if c != p.team][int(rh.integers(0, 10))]
            segs.insert(0, [other, start - dt.timedelta(days=int(rh.integers(120, 900))), start - dt.timedelta(days=1),
                            "Transfer"])
        after = max(dates) + dt.timedelta(days=14)
        if rh.random() < 0.05 and after < dt.date(2026, 12, 1):
            other = [c for c in others if c != p.team][int(rh.integers(0, 10))]
            move = after + dt.timedelta(days=int(rh.integers(5, 25)))
            segs[-1][2], segs[-1][3] = move - dt.timedelta(days=1), "Transfer"
            segs.append([other, move, None, ""])
        if rh.random() < 0.18:
            end = max(dates) + dt.timedelta(days=int(rh.integers(30, 260)))
            if end <= K.PULL_EPR - dt.timedelta(days=2) and end > segs[-1][1]:
                segs[-1][2], segs[-1][3] = end, "Discharged"
        half = "BW-CM14" if rh.random() < 0.55 else "BW-CM15"
        p.episodes = []
        for team, s, e, why in segs:
            if team == "BW-CM31" and s < K.MERGER:
                if e is not None and e < K.MERGER:
                    p.episodes.append([half, s, e, why])
                else:
                    p.episodes.append([half, s, K.MERGER - dt.timedelta(days=1), "Team merger"])
                    p.episodes.append(["BW-CM31", K.MERGER, e, why])
            else:
                p.episodes.append([team, s, e, why])
    # app codes and the prompts of every fortnight
    for p in allp:
        rp = K.rng("prompts", p.number)
        p.codes = []
        p.fortnight_rows = []
        enrol = None
        for kind, first in sorted(p.fortnights, key=lambda z: z[1]):
            c = code(rp, used_codes)
            stop = None
            if kind in ("ended_early", "incomplete"):
                stop = int(rp.integers(2, 7))
            rows = simulate_fortnight(rp, p, first, stop)
            while kind == "latest" and sum(1 for z in rows if z[3] is not None) < K.COMPLETE:
                rows = simulate_fortnight(rp, p, first, stop)
            swap = None
            if kind == "latest" and rp.random() < 0.035:
                swap = int(rp.integers(3, 11))
            c2 = code(rp, used_codes) if swap is not None else None
            enrol_on = first - dt.timedelta(days=int(rp.integers(0, 6)))
            p.codes.append((c, enrol_on, first, swap, c2))
            p.fortnight_rows.append((kind, first, c, swap, c2, rows))
    return patients, extra


def truths(patients):
    return {p.number: truth_rmssd(p) for p in patients}
