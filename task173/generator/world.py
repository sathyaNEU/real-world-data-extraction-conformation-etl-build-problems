"""The world behind task173: Ashdale's seasonal experts from 2021 to 2027 and every expert contact of the 2021 to 2026
seasons, simulated at contact level. Nothing here is shipped as it stands; records.py writes the files.

How a contact comes about. A customer preparing a return opens a case with their first expert contact on that return.
The queue offers each contact to an expert who is free, so over a day each expert takes contacts in proportion to the
hours they are on the queue over the time each contact takes them. Whether the customer has to come back depends on
the expert who took the case's first contact: an experienced expert usually settles the question at the first
contact, an expert in their first season settles fewer, and settles more each week they have been taking contacts.
A customer who does come back is equally likely to need yet another contact whoever takes the follow-up. Handle time
falls the same way over a first season. Agents from the outsourcer settle fewer first contacts than the company's
own experienced experts and take longer over each."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

# ------------------------------------------------------------------------------------------------- behaviour
PAR = dict(
    skill_mu=0.140, skill_sd=0.018,       # an experienced expert's chance that a first contact needs a follow-up
    p0_mu=0.470, p0_sd=0.022,             # the same at go-live for a first-season expert
    tau=5.5,                              # weeks for a first-season expert's excess to fall by 1/e
    q=0.180,                              # a follow-up contact's chance of needing another, whoever takes it
    aht_base=31.0,                        # minutes of talk and after-contact work, an experienced expert
    aht_sd=0.035,                         # lognormal sd of an expert's own pace
    ramp=0.455, tau_aht=5.0,              # first-season handle-time excess at go-live and its decay in weeks
    v_p_mu=0.335, v_p_sd=0.010,           # outsourcer agents' first-contact follow-up chance
    v_aht=35.5, v_aht_sd=0.020,            # outsourcer agents' handle time
    contact_sd=0.42,                      # lognormal sd of one contact's handle time around its expected value
)
TOPICS = [
    # name, share early (Jan-Feb), share late (Mar-May), follow-up multiplier, handle-time multiplier
    ("Employment income and slips", 0.20, 0.18, 0.92, 0.92),
    ("Deductions and credits", 0.17, 0.17, 0.97, 0.98),
    ("Self-employment and business income", 0.08, 0.10, 1.18, 1.22),
    ("Rental income", 0.05, 0.06, 1.15, 1.15),
    ("Investments and capital gains", 0.08, 0.08, 1.10, 1.08),
    ("RRSP, FHSA and pension income", 0.13, 0.07, 0.95, 0.95),
    ("Medical, disability and caregiver", 0.06, 0.07, 1.04, 1.02),
    ("Tuition, moving and childcare", 0.07, 0.07, 0.96, 0.94),
    ("Filing, NETFILE and corrections", 0.08, 0.13, 0.94, 0.90),
    ("Account, billing and upgrades", 0.08, 0.07, 0.86, 0.80),
]
CHANNELS = [("Video", 0.50, 1.08), ("Chat", 0.38, 0.90), ("Phone", 0.12, 1.00)]
LAGS = [(0, 0.55), (1, 0.30), (2, 0.06), (3, 0.04), (4, 0.025), (5, 0.015), (6, 0.01)]

# ------------------------------------------------------------------------------------------------- the benches
# returning experts per season and the classes that went live (date, seats filled); FR is the Montreal queue.
BENCH = {
    2021: dict(ret=170, classes=[(dt.date(2021, 2, 1), 60), (dt.date(2021, 2, 22), 60), (dt.date(2021, 3, 22), 60)],
               fr_ret=30, fr_classes=[(dt.date(2021, 2, 8), 8)], vendor=None),
    2022: dict(ret=240, classes=[(dt.date(2022, 2, 7), 70), (dt.date(2022, 3, 7), 60)],
               fr_ret=32, fr_classes=[(dt.date(2022, 2, 14), 6)], vendor=None),
    2023: dict(ret=300, classes=[(dt.date(2023, 1, 30), 60), (dt.date(2023, 2, 27), 30)],
               fr_ret=34, fr_classes=[(dt.date(2023, 2, 13), 4)], vendor=None),
    2024: dict(ret=260, classes=[(dt.date(2024, 2, 5), 60), (dt.date(2024, 2, 26), 50), (dt.date(2024, 3, 25), 30)],
               fr_ret=33, fr_classes=[(dt.date(2024, 2, 12), 6)], vendor=(26, "fortnight", 80.0)),
    2025: dict(ret=310, classes=[(dt.date(2025, 1, 27), 60), (dt.date(2025, 2, 24), 40)],
               fr_ret=35, fr_classes=[(dt.date(2025, 2, 10), 5)], vendor=None),
    2026: dict(ret=300, classes=[(dt.date(2026, 1, 12), 60), (dt.date(2026, 1, 26), 60), (dt.date(2026, 3, 23), 40)],
               fr_ret=34, fr_classes=[(dt.date(2026, 2, 9), 6)], vendor=(45, "three weeks", 114.0)),
}
CLASSES_2027 = [(dt.date(2027, 2, 15), 60), (dt.date(2027, 3, 1), 60), (dt.date(2027, 3, 29), 60),
                (dt.date(2027, 4, 12), 60)]
TRAINING_WEEKS = 4
RETURN_2027 = dict(veterans=138, second=12)


class Expert:
    __slots__ = ("emp", "queue", "first", "cls", "golive", "skill", "p0", "tau", "pace", "seasons", "old_code",
                 "team", "rehire_of", "kind")

    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))


def build_people():
    """Every in-house expert from the 2021 bench to the 2027 recall, with their own behaviour."""
    R = K.rng("people")
    people = []
    next_emp = [104210]

    def emp():
        next_emp[0] += int(R.integers(1, 9))
        return "E%06d" % next_emp[0]

    def new_expert(queue, first, cls, golive):
        return Expert(emp=emp(), queue=queue, first=first, cls=cls, golive=golive,
                      skill=float(np.clip(R.normal(PAR["skill_mu"], PAR["skill_sd"]), 0.08, 0.21)),
                      p0=float(np.clip(R.normal(PAR["p0_mu"], PAR["p0_sd"]), 0.30, 0.58)),
                      tau=float(np.clip(R.normal(PAR["tau"], 0.3), 4.5, 6.5)),
                      pace=float(np.exp(R.normal(0, PAR["aht_sd"]))), seasons=[], old_code=None, team=None,
                      rehire_of=None, kind="expert")

    # the 2021 returning bench: first seasons 2009 to 2020
    for queue, n in (("EN", BENCH[2021]["ret"]), ("FR", BENCH[2021]["fr_ret"])):
        for _ in range(n):
            first = int(R.choice(np.arange(2009, 2021), p=np.linspace(0.4, 1.6, 12) / np.linspace(0.4, 1.6, 12).sum()))
            e = new_expert(queue, first, None, None)
            people.append(e)
            e.seasons.append(2021)
    for y in K.SEASONS_OLD + [K.SEASON_CRM]:
        b = BENCH[y]
        if y > 2021:
            prev = [e for e in people if (y - 1) in e.seasons]
            for queue, n in (("EN", b["ret"]), ("FR", b["fr_ret"])):
                pool = [e for e in prev if e.queue == queue]
                idx = R.choice(len(pool), size=n, replace=False)
                for i in sorted(idx):
                    pool[i].seasons.append(y)
        for queue, classes in (("EN", b["classes"]), ("FR", b["fr_classes"])):
            for ci, (gl, n) in enumerate(classes):
                code = "%s-%02d-%d" % (queue, y % 100, ci + 1)
                for _ in range(n):
                    e = new_expert(queue, y, code, gl)
                    e.seasons.append(y)
                    people.append(e)
    # 2027 recall: 138 experts with two seasons or more and 12 from last season's classes, English queue
    en26 = [e for e in people if 2026 in e.seasons and e.queue == "EN"]
    vets = [e for e in en26 if e.first < 2026]
    sec = [e for e in en26 if e.first == 2026]
    for pool, n in ((vets, RETURN_2027["veterans"]), (sec, RETURN_2027["second"])):
        idx = R.choice(len(pool), size=n, replace=False)
        for i in sorted(idx):
            pool[i].seasons.append(2027)
    fr26 = [e for e in people if 2026 in e.seasons and e.queue == "FR"]
    idx = R.choice(len(fr26), size=29, replace=False)
    for i in sorted(idx):
        fr26[i].seasons.append(2027)
    # old-system agent codes for everyone who worked before 2026, teams per season are assigned in simulate()
    codes = R.permutation(np.arange(1100, 1100 + 3 * len(people)))
    for k, e in enumerate(people):
        if e.seasons[0] < 2026:
            e.old_code = ("TX%04d" if e.queue == "EN" else "TF%04d") % codes[k]
    return people


def vendor_agents(y, n):
    R = K.rng("vendor", y)
    out = []
    for i in range(n):
        out.append(Expert(emp="HCS-%d%03d" % (y % 10, 101 + i), queue="EN", first=y, cls="vendor", golive=None,
                          skill=float(np.clip(R.normal(PAR["v_p_mu"], PAR["v_p_sd"]), 0.22, 0.40)), p0=None,
                          tau=None, pace=float(np.exp(R.normal(0, PAR["v_aht_sd"]))), seasons=[y], old_code=None,
                          team="HCS", rehire_of=None, kind="vendor"))
    return out


# ------------------------------------------------------------------------------------------------- behaviour at a date
def weeks_on_queue(e, d):
    return (d - e.golive).days / 7.0


def follow_chance(e, d, y):
    """The chance that a case whose first contact e takes on day d needs a follow-up (before the topic)."""
    if e.kind == "vendor":
        return e.skill
    if e.first == y:
        return e.skill + (e.p0 - e.skill) * math.exp(-weeks_on_queue(e, d) / e.tau)
    return e.skill


def handle_minutes(e, d, y):
    if e.kind == "vendor":
        return PAR["v_aht"] * e.pace
    base = PAR["aht_base"] * e.pace
    if e.first == y:
        return base * (1 + PAR["ramp"] * math.exp(-weeks_on_queue(e, d) / PAR["tau_aht"]))
    return base


def weekly_hours(d, y):
    f0, f1 = K.fortnight(y)
    if f0 <= d <= f1:
        return K.SCHEDULE_HOURS / 2
    if d > f1:
        return 16.0
    m = d.month
    return {1: 16.0, 2: 26.0, 3: 35.0, 4: 40.0}[m]


def on_queue(e, d, y):
    if y not in e.seasons:
        return False
    if e.kind == "vendor":
        return True
    if e.first == y and d < e.golive:
        return False
    return K.season_open(y) <= d <= K.season_close(y)


# ------------------------------------------------------------------------------------------------- demand
def demand_curve(d, y, scale=1.0, queue="EN"):
    """Expected new expert cases on day d (the English queue; the French queue is a fixed share)."""
    f0, f1 = K.fortnight(y)
    dl = K.deadline(y)
    s0 = K.season_open(y)
    ramp = K.netfile_ramp(y)
    if d < ramp:
        base = 150 + 5.0 * (d - s0).days
    elif d < f0:
        base = 1380 + 13.0 * (d - ramp).days
        rrsp = dt.date(y, 3, 1)
        if abs((d - rrsp).days) <= 3:
            base *= 1.06
    elif d <= f1:
        k = (dl - d).days
        if k >= 0:
            base = {0: 5900, 1: 5400, 2: 4850, 3: 4300}.get(k, 3250 - 30 * (k - 4))
            if d.weekday() >= 5 and k > 3:
                base *= 0.84
        else:
            base = 1750 if k == -1 else (1050 if k == -2 else (860 if k == -3 else 760))
    else:
        base = max(220, 640 - 15 * (d - f1).days)
    if d.weekday() >= 5 and not (f0 <= d <= f1):
        base *= 0.66
    if d in K.ON_HOLIDAYS:
        base *= 0.55
    base *= scale
    return base * (0.085 if queue == "FR" else 1.0)


SCALE = {2021: 0.80, 2022: 0.88, 2023: 0.92, 2024: 0.96, 2025: 0.99, 2026: 1.00}


# ------------------------------------------------------------------------------------------------- simulation
CONTACT = np.dtype([("day", "i4"), ("t_start", "f8"), ("hsec", "f4"), ("talk", "f4"), ("wrap", "f4"),
                    ("expert", "i4"), ("case", "i4"), ("pos", "i2"), ("topic", "i1"), ("channel", "i1"),
                    ("followed", "b1"), ("queue", "i1"), ("disp", "i1"), ("p_first", "f4")])


def _intraday(R, n, fortnight_day):
    """Seconds after local midnight a contact is taken: 08:00 to 22:00, to midnight in the deadline fortnight."""
    close = 24.0 if fortnight_day else 22.0
    hrs = np.arange(8, int(close))
    w = np.array([0.6, 0.9, 1.1, 1.15, 1.0, 0.95, 1.0, 1.05, 1.0, 0.95, 1.05, 1.15, 1.1, 0.9, 0.7, 0.5][:len(hrs)])
    w = w / w.sum()
    h = R.choice(hrs, size=n, p=w)
    return h * 3600.0 + R.random(n) * 3600.0


def simulate(y, people, vendors, start=None, end=None):
    """Every expert contact of season y on both queues. Returns the contact array and the expert list it indexes."""
    R = K.rng("season", y)
    f0, f1 = K.fortnight(y)
    D0 = start or K.season_open(y)
    D1 = end or K.season_close(y)
    staff = [e for e in people if y in e.seasons] + list(vendors)
    idx_of = {id(e): i for i, e in enumerate(staff)}
    # each in-house expert's own hours: a weekly level around the phase's, a day off pattern
    level = {id(e): float(np.clip(R.normal(1.0, 0.12), 0.7, 1.3)) for e in staff}
    vend = BENCH[y]["vendor"]
    if vend:
        nv, span, hv = vend
        v0 = f0 - dt.timedelta(7) if span == "three weeks" else f0
        vdays = (f1 - v0).days + 1
    topic_w_early = np.array([t[1] for t in TOPICS]); topic_w_late = np.array([t[2] for t in TOPICS])
    t_mult = np.array([t[3] for t in TOPICS]); a_mult = np.array([t[4] for t in TOPICS])
    ch_w = np.array([c[1] for c in CHANNELS]); ch_mult = np.array([c[2] for c in CHANNELS])
    lag_days = np.array([l for l, _ in LAGS]); lag_p = np.array([p for _, p in LAGS])
    rows = []
    pending = {}
    case_meta = []          # per case: topic, channel, queue
    d = D0
    while d <= D1:
        fdays = f0 <= d <= f1
        mix = topic_w_early if d.month <= 2 else topic_w_late
        mix = mix / mix.sum()
        for qi, queue in enumerate(("EN", "FR")):
            scale = SCALE.get(y, 1.0)
            n_new = int(R.poisson(demand_curve(d, y, scale, queue) * float(np.exp(R.normal(0, 0.05)))))
            on = [e for e in staff if e.queue == queue and on_queue(e, d, y)]
            if vend and queue == "EN":
                on = [e for e in on if e.kind != "vendor" or v0 <= d <= f1]
            if not on:
                continue
            hrs = []
            for e in on:
                if e.kind == "vendor":
                    hrs.append(hv / vdays)
                else:
                    base = weekly_hours(d, y) * level[id(e)] if not fdays else weekly_hours(d, y)
                    hrs.append(base / 7.0)
            mins = np.array([handle_minutes(e, d, y) for e in on])
            cap = np.array(hrs) / mins
            prob = cap / cap.sum()
            pfirst = np.array([follow_chance(e, d, y) for e in on])
            queue_items = [(-1, 1, 0.0)] * n_new + pending.pop((d, queue), [])
            k = 0
            while k < len(queue_items):
                batch = queue_items[k:]
                k = len(queue_items)
                who = R.choice(len(on), size=len(batch), p=prob)
                times = _intraday(R, len(batch), fdays)
                for (case, pos, not_before), j, tt in zip(batch, who, times):
                    e = on[j]
                    if case < 0:
                        case = len(case_meta)
                        topic = int(R.choice(len(TOPICS), p=mix))
                        channel = int(R.choice(3, p=ch_w))
                        case_meta.append((topic, channel, qi))
                        pf = pfirst[j]
                    else:
                        topic, channel, _ = case_meta[case]
                        if R.random() < 0.2:
                            channel = int(R.choice(3, p=ch_w))
                        pf = -1.0
                    t0 = max(tt, not_before)
                    exp_min = mins[j] * a_mult[topic] * ch_mult[channel]
                    hmin = exp_min * float(np.exp(R.normal(-PAR["contact_sd"] ** 2 / 2, PAR["contact_sd"])))
                    hsec = max(90.0, hmin * 60.0)
                    wrap = hsec * float(np.clip(R.normal(0.17, 0.05), 0.04, 0.35))
                    chance = (pfirst[j] if pos == 1 else PAR["q"]) * t_mult[topic]
                    fol = bool(R.random() < chance)
                    if fol:
                        lag = int(R.choice(lag_days, p=lag_p))
                        nd = d + dt.timedelta(lag)
                        if lag == 0:
                            nb = t0 + hsec + float(R.uniform(900, 7200))
                            if nb < (24.0 if fdays else 22.0) * 3600 - 600:
                                queue_items.append((case, pos + 1, nb))
                            else:
                                nd = d + dt.timedelta(1)
                                pending.setdefault((nd, queue), []).append((case, pos + 1, 0.0))
                        elif nd <= D1:
                            pending.setdefault((nd, queue), []).append((case, pos + 1, 0.0))
                        else:
                            fol = False
                    # the expert's own wrap-up code: resolved, or one of three open dispositions
                    rd = R.random()
                    new_hand = e.kind == "vendor" or e.first == y
                    if not fol:
                        disp = 0 if rd < 0.91 else (1 if rd < 0.96 else (2 if rd < 0.985 else 3))
                    else:
                        cut = 0.70 if new_hand else 0.56
                        disp = 0 if rd < cut else (1 if rd < cut + 0.24 else (2 if rd < cut + 0.33 else 3))
                    rows.append((d.toordinal(), t0, hsec, hsec - wrap, wrap, idx_of[id(e)], case, pos, topic, channel,
                                 fol, qi, disp, pf))
        d += dt.timedelta(1)
    arr = np.array(rows, dtype=CONTACT)
    return arr, staff, case_meta


def bench_2027(people):
    """The 2027 English bench: 150 returning, four classes of 60 (seats planned, not yet hired)."""
    ret = [e for e in people if 2027 in e.seasons and e.queue == "EN"]
    return ret, CLASSES_2027
