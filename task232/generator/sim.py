"""task232 simulation: the unit's childcare enteric investigations, July 2021 to September 2026.

Each investigation opens on a laboratory's notification of a child or educator who attended a long day care room while
infectious. The room's roster books every child for set weekdays and hours and every educator for set shifts; daily
attendance follows the bookings with absences. The index attends from onset (on that day only until the centre sends
them home, or the whole day when the illness starts in the evening) and again when back in care after the centre's
48-hour rule, until the unit's call excludes them. Each room contact present on an infectious day is infected with
probability 1 - exp(-lambda x overlap hours); infected contacts fall ill one incubation later (lognormal, inside the
condition's range) when symptomatic. Secondary cases attend briefly while shedding and infect others (tertiary cases);
some rooms had cases before the index (the index's own source and co-primary cases); community and other-route cases of
the condition arrive at a background rate over the whole follow-up. The truth is kept beside every record."""
import math
import random
from datetime import date, datetime, timedelta

import params as P
import world as W

WEEKDAYS = [0, 1, 2, 3, 4]


def _q(x, step=0.25):
    return round(round(x / step) * step, 2)


class Room:
    """A room's roster at the time of an investigation."""

    def __init__(self, r, centre, room, layout_ids):
        self.centre, self.room = centre, room
        lo, hi = centre["opens"], centre["closes"]
        n_child = int(round(room["places"] * r.uniform(1.25, 1.6)))
        self.people = []
        for _ in range(n_child):
            k = r.choices([2, 3, 4, 5], weights=[0.24, 0.36, 0.2, 0.2])[0]
            days = sorted(r.sample(WEEKDAYS, k))
            start = _q(r.uniform(lo, 9.25))
            if start == P.CALL_FROM:
                start += 0.25   # no booking starts at the unit's first call of the day (C1)
            end = _q(r.uniform(14.75, hi))
            self.people.append(dict(pid=layout_ids(), role="child", days=set(days), start=start, end=end))
        n_ed = int(math.ceil(room["places"] / float(room["ratio"])))
        shifts = [(lo, lo + 8.5), (lo + 1.5, lo + 10.0), (hi - 8.5, hi)]
        for j in range(n_ed):
            s, e = shifts[j % len(shifts)]
            days = WEEKDAYS if r.random() < 0.7 else sorted(r.sample(WEEKDAYS, 4))
            s = s + 0.25 if _q(s) == P.CALL_FROM else s
            self.people.append(dict(pid=layout_ids(), role="educator", days=set(days), start=_q(s), end=_q(e)))
        self.casual = layout_ids  # casual educators cover absences under fresh ids

    def children(self):
        return [p for p in self.people if p["role"] == "child"]


class IdMaker:
    """Each layout's management software numbers people its own way; numbers are unique within a centre."""

    def __init__(self, r, layout):
        self.r, self.layout, self.used = r, layout, set()

    def __call__(self):
        while True:
            if self.layout == "A":
                x = "%06d" % self.r.randint(100000, 389999)
            elif self.layout == "B":
                x = "CH%05d" % self.r.randint(10000, 99999)
            else:
                x = "%08x" % self.r.getrandbits(32)
            if x not in self.used:
                self.used.add(x)
                return x


def season(c, d):
    m = P.SUMMER[c] if d.month in (12, 1, 2, 3) else 0.8
    norm = (4 * P.SUMMER[c] + 8 * 0.8) / 12.0
    return m / norm


def incubation(r, c):
    name, lo, hi, med, sd = P.COND[c][:5]
    while True:
        x = math.exp(math.log(med) + sd * r.gauss(0, 1))
        if lo + 0.05 <= x <= hi - 0.05:
            return x


AUTH = {
    # laboratory: (days it authorises, profile) in the laboratory's own clock; hours past 24 run into the next morning
    "CRBH": (set(range(7)), [(0.795, 7.5, 21.5), (0.205, 0.0, 24.0)]),
    "LPG": ({0, 1, 2, 3, 4, 5}, [(0.52, 8.0, 12.5), (0.48, 14.0, 21.5)]),
    "HDN": ({0, 1, 2, 3, 4, 5}, [(0.75, 7.0, 18.5), (0.25, 16.0, 20.0)]),
    "KES": ({0, 1, 2, 3, 4, 5}, [(0.89, 3.5, 8.5), (0.11, 10.0, 16.0)]),
    "HPS": (set(range(7)), [(1.0, 17.0, 25.5)]),
    "SERL": ({0, 1, 2, 3, 4}, [(1.0, 9.0, 17.0)]),
}
TURNAROUND = {"SHIG": [(1, 0.15), (2, 0.5), (3, 0.35)], "STEC": [(1, 0.2), (2, 0.5), (3, 0.3)],
              "CRYP": [(1, 0.45), (2, 0.4), (3, 0.15)]}


def auth_time(r, feed, d, knobs=None):
    days, prof = AUTH[feed]
    if knobs and ("auth_" + feed) in knobs:
        prof = knobs["auth_" + feed]
    tz = W.QLD if feed == "KES" else W.NSW
    while True:
        if d.weekday() in days and not (feed == "HDN" and d.weekday() == 5 and r.random() < 0.5):
            break
        d += timedelta(days=1)
    u = r.random()
    acc = 0.0
    for w, a, b in prof:
        acc += w
        if u <= acc:
            break
    h = r.uniform(a, b)
    if h >= 24.0:
        d, h = d + timedelta(days=1), h - 24.0
    hh = int(h)
    mm = int((h - hh) * 60)
    r.randint(0, 59)
    return datetime(d.year, d.month, d.day, hh, mm, 0, tzinfo=tz).astimezone(W.NSW)


DELIVERY = {
    # laboratory: (P(stream), stream minutes median, batch interval hours)
    "CRBH": (0.97, 3.0, None),
    "LPG": (0.0, None, 0.5),
    "HDN": (0.0, None, 1.0),
    "KES": (0.9, 6.0, None),
    "HPS": (0.0, None, 2.0),
    "SERL": (0.0, None, 4.0),
}


def deliver(r, feed, auth):
    """Hours from authorisation to receipt on an ordinary day (outages and replays are added by the records layer)."""
    p, med, every = DELIVERY[feed]
    if feed == "HPS" and auth.date() >= P.ACQUISITION:
        every = 0.5
    if every is None or r.random() < p:
        return max(0.01, med / 60.0 * math.exp(0.5 * r.gauss(0, 1)))
    t = auth.astimezone(W.UTC)
    k = (t.hour + t.minute / 60.0 + t.second / 3600.0) / every
    nxt = (math.floor(k) + 1) * every
    return nxt - (t.hour + t.minute / 60.0 + t.second / 3600.0) + r.uniform(0.02, 0.12)


class Investigation:
    pass


class World:
    def __init__(self, seed=P.SEED, knobs=None):
        self.seed = seed
        self.k = dict(knobs or {})
        self.centres = W.build_centres(seed)
        self.invs = []
        self.ids = {}

    def kn(self, name, default):
        return self.k.get(name, default)

    # ------------------------------------------------------------------ index cases
    def stream(self, *key):
        """One random stream per investigation and purpose, keyed by the episode's identity (condition and onset date),
        so a tuned parameter moves only the records it governs."""
        return random.Random("%d|" % self.seed + "|".join(str(k) for k in key))

    def onsets(self):
        out = []
        for c in P.COND_KEYS:
            r = self.stream("onsets", c)
            d = P.EPI_FROM
            while d <= P.EPI_TO:
                per_year = P.COND[c][10] * self.kn("vol_" + c, 1.0)
                u = r.random()
                if u < per_year / 365.0 * season(c, d):
                    out.append((d, c))
                d += timedelta(days=1)
        out.sort()
        return out

    def run(self):
        for n, (d0, c) in enumerate(self.onsets()):
            inv = self.episode(n, d0, c)
            if inv is not None:
                self.invs.append(inv)
        return self

    def pick_feed(self, r, c, border):
        u = r.random()
        if border and u < P.BORDER_KES:
            return "KES"
        sh = P.FEED_SHARE[c]
        keys = sorted(sh)
        w = [sh[k] * self.kn("share_" + k, P.FEED_WEIGHT[k]) for k in keys]
        v = r.random() * sum(w)
        acc = 0.0
        for k, x in zip(keys, w):
            acc += x
            if v <= acc:
                return k
        return keys[-1]

    def busy(self, centre, room, d0):
        """A room already under investigation: a new index whose room export (from 21 days before onset to about 30
        days after) would overlap that investigation's export is a case in that investigation, not a new one, so a
        new investigation goes to a room that is not under one."""
        for i in self.invs:
            if i.centre is centre and i.room is room and i.ex_from - timedelta(days=30) <= d0 <= i.ex_to + timedelta(days=21):
                return True
        return False

    def episode(self, n, d0, c):
        rc = self.stream(c, d0, "case")
        border_w = self.kn("border_weight", P.BORDER_WEIGHT)
        cw = [border_w if ce["border"] else 1.0 for ce in self.centres]
        while True:
            centre = rc.choices(self.centres, weights=cw)[0]
            room = rc.choices(centre["rooms"], weights=[x["places"] for x in centre["rooms"]])[0]
            if not self.busy(centre, room, d0):
                break
        if centre["sid"] not in self.ids:
            self.ids[centre["sid"]] = IdMaker(self.stream("ids", centre["sid"]), centre["layout"])
        roster = Room(rc, centre, room, self.ids[centre["sid"]])
        staff = rc.random() < P.STAFF_SHARE_INDEX
        pool = [p for p in roster.people if p["role"] == ("educator" if staff else "child")]
        index = rc.choice(pool)
        inv = Investigation()
        inv.n, inv.cond, inv.centre, inv.room, inv.roster, inv.index = n, c, centre, room, roster, index
        inv.onset = d0
        # how the illness started on the onset day
        booked_today = W.centre_open(centre, d0) and d0.weekday() in index["days"]
        sw = self.kn("scen", [0.4, 0.35, 0.25])
        if booked_today:
            inv.scenario = rc.choices(["centre", "evening", "morning"], weights=sw)[0]
        else:
            inv.scenario = "home"
        ill = self.kn("ill_" + c, {"SHIG": (1, 3), "STEC": (1, 4), "CRYP": (1, 5)}[c])
        inv.ill_days = rc.randint(*ill)
        inv.back = d0 + timedelta(days=inv.ill_days + 2)      # back in care 48 hours after the last loose stool
        # specimen, laboratory, authorisation, delivery, the unit's call
        rf = self.stream(c, d0, "feed")
        inv.feed = self.pick_feed(rf, c, centre["border"])
        sp = rf.choices([0, 1, 2, 3, 4], weights=self.kn("spec_w", [0.06, 0.3, 0.3, 0.2, 0.14]))[0]
        inv.specimen = d0 + timedelta(days=sp)
        ta = rf.choices([t for t, w in TURNAROUND[c]], weights=[w for t, w in TURNAROUND[c]])[0]
        auth = auth_time(rf, inv.feed, inv.specimen + timedelta(days=ta), self.k)
        lateness = deliver(rf, inv.feed, auth)
        inv.received = W.add_hours(auth, lateness)
        # the minute the laboratory's system stamped the authorisation (its validation queue runs a few minutes ahead
        # of the release to the interface)
        early = self.stream(c, d0, "stamp", self.kn("stamp_salt", P.STAMP_SALT)).randint(0, 12)
        if (auth.minute - early) % 15 == 0:
            early += 1      # a stamp on the quarter hour would tie a call with a booked arrival (C1)
        inv.auth = W.add_hours(auth, -early / 60.0)
        inv.lateness = lateness + early / 60.0
        inv.triage = rf.uniform(0.15, 1.4)
        inv.call = W.call_time(W.add_hours(inv.received, inv.triage))
        inv.excl_date = inv.call.date()
        dates = [d0, inv.specimen, inv.auth.date(), inv.received.date(), inv.call.date(),
                 inv.auth.astimezone(W.UTC).date(), inv.received.astimezone(W.UTC).date()]
        for edge in (P.BASIS_FROM, P.BASIS_TO + timedelta(days=1), P.YEAR_FROM):
            if min(dates) < edge <= max(dates):
                return None     # an index whose dates straddle a basis boundary is left out of the simulation (C1)
        self.attend(self.stream(c, d0, "attend"), inv)
        if not inv.inf_days:
            return None
        self.transmit(self.stream(c, d0, "tx"), inv)
        return inv

    # ------------------------------------------------------------------ attendance
    def attend(self, r, inv):
        """Daily attendance for the room from 21 days before onset to 14 days after the exclusion."""
        c, centre, roster, idx = inv.cond, inv.centre, inv.roster, inv.index
        inv.ex_from = inv.onset - timedelta(days=P.SOURCE_LOOKBACK)
        inv.ex_to = inv.excl_date + timedelta(days=14)
        inv.att = {}           # (pid, date) -> (in, out) wall hours
        inv.away = {}          # pid -> first date of illness absence (cases), set in transmit
        call_h = W.wall(inv.call)
        d = inv.ex_from
        while d <= inv.ex_to:
            if W.centre_open(centre, d):
                for p in roster.people:
                    if d.weekday() not in p["days"]:
                        continue
                    if p is idx:
                        continue
                    if r.random() < (0.08 if p["role"] == "child" else 0.04):
                        if p["role"] == "educator":
                            cas = dict(pid=roster.casual(), role="educator", days=set(), start=p["start"], end=p["end"])
                            roster.people.append(cas)
                            inv.att[(cas["pid"], d)] = (p["start"], p["end"])
                        continue
                    a = _q(p["start"] + r.gauss(0, 0.3), 0.0833)
                    b = _q(p["end"] + r.gauss(0, 0.3), 0.0833)
                    a = max(centre["opens"], a)
                    b = min(centre["closes"], max(a + 2.0, b))
                    inv.att[(p["pid"], d)] = (a, b)
            d += timedelta(days=1)
        # the index
        inv.inf_days = []
        d = inv.ex_from
        while d <= inv.ex_to:
            if W.centre_open(centre, d) and d.weekday() in idx["days"]:
                a = max(centre["opens"], _q(idx["start"] + r.gauss(0, 0.25), 0.0833))
                b = min(centre["closes"], max(a + 2.0, _q(idx["end"] + r.gauss(0, 0.25), 0.0833)))
                go = True
                if d < inv.onset:
                    go = r.random() > 0.06
                elif d == inv.onset:
                    if inv.scenario == "morning":
                        go = False
                    elif inv.scenario == "centre":
                        b = min(b, max(a + 1.0, _q(r.uniform(9.5, 14.0), 0.0833)))
                elif d < inv.back:
                    go = False
                if d > inv.excl_date or (d == inv.excl_date and call_h <= a):
                    go = False
                if go and d == inv.excl_date:
                    b = min(b, _q(call_h + P.LEAVE_AFTER - r.uniform(0.0, 0.3), 0.0833))
                    if b <= a:
                        go = False
                if go:
                    inv.att[(idx["pid"], d)] = (a, b)
                    if d >= inv.onset:
                        inv.inf_days.append(d)
            d += timedelta(days=1)

    def present(self, inv, d):
        return [p for p in inv.roster.people if (p["pid"], d) in inv.att]

    # ------------------------------------------------------------------ transmission and the room's other illness
    def transmit(self, r, inv):
        c = inv.cond
        name, lo, hi, med, sd, lam, psym, shed, bg, pearly, _, plate = P.COND[c]
        lam *= self.kn("lam_" + c, 1.0)
        bg *= self.kn("bg_" + c, 1.0)
        pearly = min(0.95, pearly * self.kn("early_" + c, 1.0))
        plate *= self.kn("late_" + c, 1.0)
        idx = inv.index
        inv.first_inf = inv.inf_days[0]
        inv.last_inf = inv.inf_days[-1]
        inv.fu_from = inv.onset - timedelta(days=P.SOURCE_LOOKBACK)
        inv.fu_to = inv.excl_date + timedelta(days=P.FOLLOWUP_DAYS[c])
        inv.cases = []
        infected = {}
        for d in inv.inf_days:
            ia, ib = inv.att[(idx["pid"], d)]
            for p in self.present(inv, d):
                if p is idx or p["pid"] in infected:
                    continue
                a, b = inv.att[(p["pid"], d)]
                ov = max(0.0, min(ib, b) - max(ia, a))
                if ov > 0 and r.random() < 1 - math.exp(-lam * ov):
                    infected[p["pid"]] = datetime(d.year, d.month, d.day) + timedelta(hours=max(ia, a) + r.uniform(0, ov))
        contacts = {p["pid"]: p for d in inv.inf_days for p in self.present(inv, d) if p is not idx}
        inv.contacts = contacts
        secs = []
        for pid in sorted(infected):
            if r.random() < psym:
                on = infected[pid] + timedelta(days=incubation(r, c))
                secs.append((pid, on))
                inv.cases.append(dict(pid=pid, onset=on.date(), kind="sec"))
        # tertiary: secondary cases attend while shedding before the centre sends them home
        ter_p = 1 - math.exp(-lam * self.kn("ter_" + c, 1.0) * 7.5 * shed)
        others = [pid for pid in sorted(contacts) if pid not in infected]
        for pid, on in secs:
            for q in others:
                if q in infected or r.random() >= ter_p * 0.62:
                    continue
                t = on + timedelta(days=r.uniform(-0.3, shed + 0.4))
                infected[q] = t
                if r.random() < psym:
                    inv.cases.append(dict(pid=q, onset=(t + timedelta(days=incubation(r, c))).date(), kind="ter"))
        # earlier cases in the room: the index's own source and co-primary cases
        if r.random() < pearly:
            pool = [pid for pid in sorted(contacts) if pid not in infected]
            for pid in r.sample(pool, min(len(pool), r.choice([1, 1, 2, 2, 3]))):
                back = r.uniform(1.0, P.SOURCE_LOOKBACK - 1)
                infected[pid] = None
                inv.cases.append(dict(pid=pid, onset=inv.onset - timedelta(days=int(back)), kind="early"))
        # later cases: a household chain or a new introduction into the room after the index's window
        if r.random() < plate:
            (l0, l1), (h0, h1) = self.zones(inv)
            pool = [pid for pid in sorted(contacts) if pid not in infected]
            gap = (inv.fu_to - h1).days
            if gap >= 2:
                for pid in r.sample(pool, min(len(pool), r.choice([1, 1, 1, 2, 2, 3]))):
                    infected[pid] = None
                    inv.cases.append(dict(pid=pid, onset=h1 + timedelta(days=r.randint(1, gap)), kind="late"))
        # community and other-route cases of the condition over the follow-up
        span = (inv.fu_to - inv.fu_from).days + 1
        for pid in sorted(contacts):
            if pid in infected:
                continue
            if r.random() < bg * span * season(c, inv.onset):
                infected[pid] = None
                inv.cases.append(dict(pid=pid, onset=inv.fu_from + timedelta(days=r.randrange(span)), kind="bg"))
        inv.cases = [x for x in inv.cases if inv.fu_from <= x["onset"] <= inv.fu_to]
        for x in inv.cases:
            x["status"] = "confirmed" if r.random() < 0.56 else "probable"
        self.converge(inv)
        self.absences(inv)
        inv.closed_on = inv.fu_to + timedelta(days=r.randint(4, 30))
        inv.closed = inv.closed_on <= P.EXTRACT
        self.sign_times(inv)

    def absences(self, inv):
        """A case who falls ill after the index's infectious attendance is home from the day after onset until 48 hours
        after the diarrhoea stops (the centre's illness policy); earlier days are left as they were."""
        ra = self.stream(inv.cond, inv.onset, "absence")
        lo, hi = {"SHIG": (1, 3), "STEC": (2, 4), "CRYP": (2, 5)}[inv.cond]
        for x in sorted(inv.cases, key=lambda y: (y["onset"], y["pid"])):
            x["ill_days"] = ra.randint(lo, hi)
            d = max(x["onset"] + timedelta(days=1), inv.last_inf + timedelta(days=1))
            end = x["onset"] + timedelta(days=x["ill_days"] + 2)
            while d <= end:
                inv.att.pop((x["pid"], d), None)
                d += timedelta(days=1)

    def sign_times(self, inv):
        """Sign-in and sign-out times as the centre's software records them, to the minute."""
        rf = self.stream(inv.cond, inv.onset, "minutes", self.kn("fine_salt", P.FINE_SALT))
        lo, hi = inv.centre["opens"], inv.centre["closes"]
        for key in sorted(inv.att, key=lambda k: (k[1], k[0])):
            a, b = inv.att[key]
            a2 = round(min(max(lo, a + rf.randint(-2, 2) / 60.0), hi) * 60) / 60.0
            b2 = round(min(max(a2 + 0.5, b + rf.randint(-2, 2) / 60.0), hi) * 60) / 60.0
            inv.att[key] = (a2, b2)

    def zones(self, inv):
        c = inv.cond
        lo, hi = P.COND[c][1], P.COND[c][2]
        low = (inv.onset, inv.first_inf + timedelta(days=math.ceil(lo)))
        high = (inv.last_inf + timedelta(days=math.floor(hi)), inv.excl_date + timedelta(days=math.ceil(hi)))
        return low, high

    def converge(self, inv):
        """No case onset on a date where the window's edge depends on a convention (C1): a case dated in either edge
        zone is moved to the nearest date outside it on the side its truth gives (a secondary case inside the window,
        any other case outside it). A case other than a secondary case that the index's window keeps is also inside
        the window of the days the contact itself shared with the index, or it is moved out of the index's window, so
        the room's window and each contact's own window keep the same cases."""
        c = inv.cond
        lo, hi = P.COND[c][1], P.COND[c][2]
        (l0, l1), (h0, h1) = self.zones(inv)
        for x in inv.cases:
            on = x["onset"]
            if l0 <= on <= l1:
                x["onset"] = l1 + timedelta(days=1) if x["kind"] == "sec" else l0 - timedelta(days=1)
            elif h0 <= on <= h1:
                x["onset"] = h0 - timedelta(days=1) if x["kind"] == "sec" else h1 + timedelta(days=1)
            if x["kind"] != "sec" and l1 < x["onset"] < h0:
                days = [d for d in inv.inf_days if (x["pid"], d) in inv.att]
                own = days and (x["onset"] - days[0]).days >= lo and (x["onset"] - days[-1]).days <= hi
                if not own:
                    mid = l1 + (h0 - l1) / 2
                    x["onset"] = l0 - timedelta(days=1) if x["onset"] < mid else h1 + timedelta(days=1)
            x["onset"] = min(max(x["onset"], inv.fu_from), inv.fu_to)
