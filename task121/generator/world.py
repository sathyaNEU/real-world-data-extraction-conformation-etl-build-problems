"""The world for task121 (architecture 6): the centre's call-takers and the shifts they worked, the medical calls
they triaged and the patients the crews found, the ambulances assigned, the 911 calls the phone system answered and the
cardiac arrest calls the quality team reviewed.

Every event is placed on one clock in UTC; the centre's systems record local wall-clock time (US Central) and the
phone system records UTC. A call is sent cold when the call-taker's triage falls short; the chance rises on a shift the
call-taker began less than eleven hours after the previous one ended, for a graduate in the first months, and between
midnight and six. Release 13.3 changes how long a call takes to process, not how it is triaged."""
import bisect
import collections
import datetime as dt

import numpy as np

import common as K

H = dt.timedelta(hours=1)


def to_utc(local):
    """local wall-clock time to UTC; a time in the spring-forward gap is read an hour later, the repeated hour of
    2 November 2025 as standard time"""
    if dt.datetime(2026, 3, 8, 2) <= local < dt.datetime(2026, 3, 8, 3):
        local = local + H
    return local + (5 * H if K.is_cdt(local) else 6 * H)


def to_local(utc):
    """UTC to local wall-clock time (central daylight time from the second Sunday of March to the first Sunday of
    November)"""
    cdt = (dt.datetime(2025, 3, 9, 8) <= utc < dt.datetime(2025, 11, 2, 7)) or \
        (dt.datetime(2026, 3, 8, 8) <= utc < dt.datetime(2026, 11, 1, 7))
    return utc - (5 * H if cdt else 6 * H)


def _load(t):
    """the centre's busy hours and the winter months lengthen the wait for a position"""
    loc = to_local(t)
    busy = 1.0 + 0.45 * np.sin(np.pi * max(0, loc.hour - 7) / 15.0) if 7 <= loc.hour <= 22 else 0.85
    winter = 1.10 if loc.month in (12, 1, 2) else 1.0
    return busy * winter


class World:
    def __init__(self, seed=K.SEED):
        self.seed = seed
        self._staff()
        self._roster()
        self._calls()
        self._units()
        self._splits()
        self._che()
        self._tcpr()
        self._distractors()

    # ------------------------------------------------------------------ call-takers
    def _staff(self):
        rng = np.random.default_rng([121, self.seed, 1])
        self.staff = []
        logins = sorted(rng.choice(np.arange(104, 399), size=60, replace=False))
        emps = sorted(rng.choice(np.arange(10230, 18990), size=54, replace=False))
        for i in range(54):
            cert = dt.date(2008, 3, 1) + dt.timedelta(days=int(rng.integers(0, 5900)))
            self.staff.append(dict(emp="QC%05d" % emps[i], login="CT%03d" % logins[i], certified=cert,
                                   cls="", start=K.ROSTER_FROM, leave=None, new=False))
        for j in range(6):
            self.staff.append(dict(emp="QC%05d" % (19104 + 3 * j + int(rng.integers(0, 3))),
                                   login="CT%03d" % logins[54 + j], certified=dt.date(2026, 2, 6), cls="2026-1",
                                   start=K.ACADEMY, leave=None, new=True))
        # one call-taker retired at the end of June 2026, one came across from a neighbouring centre in October 2025
        self.staff[11]["leave"] = dt.date(2026, 6, 26)
        self.staff[37]["start"] = dt.date(2025, 10, 6)
        self.staff[37]["certified"] = dt.date(2016, 5, 20)
        self.by_login = {s["login"]: s for s in self.staff}

    # ------------------------------------------------------------------ the shifts worked
    def _roster(self):
        """an eight-day cycle, four on and four off; before the 2026 rotation a block is four shifts of one type, the
        type moving forward between blocks; from each call-taker's first block on or after 2 March 2026 a block holds
        two shift types, stepping back from evening to day and from night to evening"""
        rng = np.random.default_rng([121, self.seed, 2])
        fwd = ["D", "E", "N"]
        pat = [("E", "E", "D", "D"), ("N", "N", "E", "E"), ("D", "D", "N", "N")]
        days = [K.ROSTER_FROM + dt.timedelta(d) for d in range((K.END - K.ROSTER_FROM).days + 2)]
        shifts = []
        for i, s in enumerate(self.staff):
            off = (i * 3 + int(rng.integers(0, 2))) % 8
            base = int(rng.integers(0, 3))
            # leave: two or three whole blocks a year
            leave_blocks = set(int(x) for x in rng.choice(np.arange(0, 48), size=int(rng.integers(2, 4)), replace=False))
            for d in days:
                if d < s["start"] or (s["leave"] and d > s["leave"]):
                    continue
                t = (d - K.ROSTER_FROM).days + off
                p, b = t % 8, t // 8
                if b in leave_blocks:
                    continue
                if p < 4:
                    bs = d - dt.timedelta(days=p)
                    typ = pat[(base + b) % 3][p] if bs >= K.ROTATION else fwd[(base + b) % 3]
                    kind = "REGULAR"
                    if rng.random() < 0.025:
                        typ = fwd[(fwd.index(typ) + 1 + int(rng.integers(0, 2))) % 3]
                        kind = "SWAP"
                    if rng.random() < 0.03:        # sick: not worked
                        continue
                    shifts.append((s["login"], d, typ, kind))
                elif rng.random() < 0.012:
                    shifts.append((s["login"], d, fwd[int(rng.integers(0, 3))], "OVERTIME"))
        rows = []
        # the extract runs to 31 August 2026
        shifts = [x for x in shifts if x[1] <= K.END]
        for login, d, typ, kind in shifts:
            h0, n = K.SHIFT[typ]
            st = dt.datetime.combine(d, dt.time(h0))
            en = st + dt.timedelta(hours=n)
            rows.append(dict(login=login, date=d, type=typ, kind=kind, start=st, end=en,
                             ustart=to_utc(st), uend=to_utc(en)))
        rows.sort(key=lambda r: (r["login"], r["ustart"]))
        # a swap or an overtime shift that would run straight on from, or into, another shift was not taken
        keep = []
        for k, r in enumerate(rows):
            if r["kind"] != "REGULAR":
                before = rows[k - 1] if k and rows[k - 1]["login"] == r["login"] else None
                after = rows[k + 1] if k + 1 < len(rows) and rows[k + 1]["login"] == r["login"] else None
                if (before and (r["ustart"] - before["uend"]) < 4 * H) or (after and (after["ustart"] - r["uend"]) < 4 * H):
                    continue
            keep.append(r)
        rows = keep
        prev = {}
        for r in rows:
            pe = prev.get(r["login"])
            r["rest"] = None if pe is None else (r["ustart"] - pe).total_seconds() / 3600.0
            r["qr"] = r["rest"] is not None and r["rest"] < K.QUICK_RETURN_HOURS
            prev[r["login"]] = r["uend"]
        self.shifts = rows
        # who is on duty, by UTC hour
        self.on_duty = collections.defaultdict(list)
        for k, r in enumerate(rows):
            t = r["ustart"]
            while t < r["uend"]:
                self.on_duty[t.replace(minute=0, second=0)].append(k)
                t += H

    # ------------------------------------------------------------------ medical calls and the crews' findings
    def _calls(self):
        rng = np.random.default_rng([121, self.seed, 3])
        hour_w = np.array([2.1, 1.7, 1.5, 1.3, 1.2, 1.4, 2.1, 3.1, 4.1, 4.7, 4.9, 5.0, 5.1, 5.0, 4.9, 4.9, 4.9, 4.8,
                           4.7, 4.4, 4.1, 3.7, 3.2, 2.6])
        hour_w = hour_w / hour_w.sum()
        codes = [p[0] for p in K.PROTOCOLS]
        mix = np.array([p[2] for p in K.PROTOCOLS])
        self.calls = []
        seq = {2025: 41260, 2026: 2130}
        for d in K.DAYS:
            doy = d.timetuple().tm_yday
            lam = 182 * (1 + 0.10 * np.cos(2 * np.pi * (doy - 15) / 365.0)) * (1.05 if d.weekday() >= 5 else 1.0)
            w = mix.copy()
            if d.month in (12, 1, 2):
                w[codes.index("06")] *= 1.25
                w[codes.index("26")] *= 1.10
            if d.month in (6, 7, 8):
                w[codes.index("29")] *= 1.15
            w = w / w.sum()
            day_calls = []
            for _ in range(int(rng.poisson(lam))):
                hr = int(rng.choice(24, p=hour_w))
                sec = int(rng.integers(0, 3600))
                local = dt.datetime.combine(d, dt.time(hr)) + dt.timedelta(seconds=sec)
                day_calls.append(local)
            for local in sorted(day_calls):
                utc = to_utc(local)
                duty = self.on_duty.get(utc.replace(minute=0, second=0))
                duty = [k for k in (duty or []) if self.shifts[k]["ustart"] <= utc < self.shifts[k]["uend"]]
                if not duty:
                    continue
                k = duty[int(rng.integers(0, len(duty)))]
                sh = self.shifts[k]
                pc = codes[int(rng.choice(len(codes), p=w))]
                p = K.PROTOCOL[pc]
                hi = rng.random() < p[3]
                contact = rng.random() < (0.94 if hi else 0.74)
                staff = self.by_login[sh["login"]]
                mult = 1.0
                if sh["qr"]:
                    mult *= K.QR_FACTOR
                if staff["new"] and (d - K.ACADEMY).days < K.NEW_DAYS:
                    mult *= K.NEW_FACTOR
                if local.hour < 6:
                    mult *= K.NIGHT_FACTOR
                if hi:
                    cold = rng.random() < min(0.9, p[4] * mult)
                else:
                    cold = rng.random() >= 0.24
                if cold:
                    level = str(rng.choice(list(K.LEVELS_COLD), p=[0.45, 0.25, 0.25, 0.05]))
                else:
                    level = "E" if pc == "09" or (pc == "31" and rng.random() < 0.15) else "D"
                if contact:
                    acuity = (1 if rng.random() < 0.3 else 2) if hi else (3 if rng.random() < 0.55 else 4)
                else:
                    acuity = None
                yr = local.year
                seq[yr] += int(rng.integers(1, 4))
                self.calls.append(dict(
                    incident="%02d-%07d" % (yr % 100, seq[yr]), local=local, utc=utc, login=sh["login"], shift=k,
                    protocol=pc, level=level, cold=cold, hi=hi, contact=contact, acuity=acuity,
                    version="13.3" if utc >= to_utc(K.RELEASE) else "13.1",
                    suffix=int(rng.integers(1, 6)),
                    second_patient=contact and rng.random() < 0.012))

    # ------------------------------------------------------------------ ambulances assigned (Ask A)
    def _units(self):
        """the first ambulance is assigned a minute or two after answer (a few seconds longer on release 13.3, its
        new breathing prompt); about one call in eighteen loses its first ambulance to a higher-priority call or to a
        closer unit and is given a second"""
        rng = np.random.default_rng([121, self.seed, 4])
        rel = to_utc(K.RELEASE)
        for c in self.calls:
            med = 58.0 if c["level"] in K.LEVELS_HOT else 84.0
            delay = max(15.0, med * float(np.exp(rng.normal(0, 0.38)))) + (7.0 if c["utc"] >= rel else 0.0)
            c["answered_utc"] = c["utc"]
            a1 = c["utc"] + dt.timedelta(seconds=int(round(delay)))
            u1 = K.UNITS[int(rng.integers(0, len(K.UNITS)))]
            units = [dict(unit=u1, assigned=a1, outcome="Arrived")]
            if rng.random() < 0.055:
                lost = a1 + dt.timedelta(seconds=int(rng.integers(60, 600)))
                units[0]["outcome"] = "Diverted" if rng.random() < 0.6 else "Cancelled"
                units[0]["cleared"] = lost
                u2 = K.UNITS[int(rng.integers(0, len(K.UNITS)))]
                if u2 == u1:
                    u2 = K.UNITS[(K.UNITS.index(u1) + 3) % len(K.UNITS)]
                units.append(dict(unit=u2, assigned=lost + dt.timedelta(seconds=int(rng.integers(5, 90))),
                                  outcome="Arrived"))
            last = units[-1]
            last["enroute"] = last["assigned"] + dt.timedelta(seconds=int(rng.integers(20, 120)))
            last["at_scene"] = last["enroute"] + dt.timedelta(seconds=int(rng.integers(240, 1200)))
            last["cleared"] = last["at_scene"] + dt.timedelta(seconds=int(rng.integers(1500, 4800)))
            if units[0] is not last:
                units[0]["enroute"] = units[0]["assigned"] + dt.timedelta(seconds=int(rng.integers(20, 90)))
            c["units"] = units
            c["first_assigned"] = units[0]["assigned"]
            c["dispatched"] = units[-1]["assigned"]

    # ------------------------------------------------------------------ split incidents (Ask A)
    def _splits(self):
        """a traffic incident with a patient in a second vehicle, or a second patient found at another call, goes to
        a second ambulance on its own CAD incident: the split copies the call's answer time, call-taker, phone call
        and triage, and carries its own ambulance and patient record. Never on an arrest. The CAD numbers incidents
        as they are created, so the split takes the next number at the time it was made"""
        rng = np.random.default_rng([121, self.seed, 11])
        self.splits = []
        for c in self.calls:
            c["split"] = None
            if not c["contact"] or c["protocol"] == "09":
                continue
            p = 0.34 if c["protocol"] == "29" else (0.45 if c["second_patient"] else 0.0)
            if p == 0.0 or rng.random() >= p:
                continue
            made = c["utc"] + dt.timedelta(seconds=int(rng.integers(150, 1500)))
            made = max(made, c["units"][0]["assigned"] + dt.timedelta(seconds=int(rng.integers(30, 120))))
            used = {u["unit"] for u in c["units"]}
            unit = K.UNITS[int(rng.integers(0, len(K.UNITS)))]
            while unit in used:
                unit = K.UNITS[(K.UNITS.index(unit) + 5) % len(K.UNITS)]
            u = dict(unit=unit, assigned=made + dt.timedelta(seconds=int(rng.integers(10, 90))), outcome="Arrived")
            u["enroute"] = u["assigned"] + dt.timedelta(seconds=int(rng.integers(20, 120)))
            u["at_scene"] = u["enroute"] + dt.timedelta(seconds=int(rng.integers(240, 1200)))
            u["cleared"] = u["at_scene"] + dt.timedelta(seconds=int(rng.integers(1500, 4800)))
            sp = dict(parent=c, made=made, units=[u],
                      acuity=None if c["second_patient"] else (3 if rng.random() < 0.6 else 4))
            c["split"] = sp
            self.splits.append(sp)
        # incident numbers in the order the incidents were created, each year's series on its own
        rng = np.random.default_rng([121, self.seed, 12])
        made = [(c["utc"], 0, c) for c in self.calls] + [(s["made"], 1, s) for s in self.splits]
        made.sort(key=lambda x: (x[0], x[1]))
        seq = {2025: 41260, 2026: 2130}
        for t, _, x in made:
            yr = to_local(t).year
            seq[yr] += int(rng.integers(1, 4))
            x["incident"] = "%02d-%07d" % (yr % 100, seq[yr])

    # ------------------------------------------------------------------ the phone system's call detail (Asks B and C)
    def _che(self):
        """every call on the centre's 911 trunks and its 10-digit emergency lines; a medical call's record is the one
        the CAD incident was opened from. Calls on the 10-digit lines wait behind 911 calls"""
        rng = np.random.default_rng([121, self.seed, 5])
        n = 880000
        trunks_911 = ["TG01", "TG02", "TG03"]
        cls = {"TG01": ["RESD", "BUSN", "PBXB", "COIN"], "TG02": ["WPH2", "WPH1"], "TG03": ["VOIP"],
               "TG05": ["WPH2", "WPH1", "RESD"], "TG07": ["RESD", "BUSN", "PBXB"]}

        def ring(t, ten):
            base = float(rng.gamma(2.2, 2.4)) * _load(t)
            if rng.random() < 0.05 * _load(t):
                base += float(rng.exponential(14.0))
            if ten:
                base = base * 1.8 + float(rng.exponential(9.0))
            return max(1, int(round(base)))

        events = []
        for c in self.calls:
            tg = "TG05" if rng.random() < 0.03 else trunks_911[int(rng.choice(3, p=[0.18, 0.72, 0.10]))]
            r = ring(c["utc"], False)
            arrived = c["utc"] - dt.timedelta(seconds=r)
            events.append(("911", tg, arrived, r, c))
        # the other 911 calls (fire, police, misdials, hang-ups) and the 10-digit lines
        for d in K.DAYS + [K.END + dt.timedelta(1)]:
            for kind, lam in (("911", 148.0), ("ten", 26.0)):
                for _ in range(int(rng.poisson(lam))):
                    local = dt.datetime.combine(d, dt.time(0)) + dt.timedelta(seconds=int(rng.integers(0, 86400)))
                    utc = to_utc(local)
                    if kind == "911":
                        tg = "TG05" if rng.random() < 0.03 else trunks_911[int(rng.choice(3, p=[0.18, 0.72, 0.10]))]
                    else:
                        tg = "TG07"
                    events.append((kind, tg, utc, None, None))
        events.sort(key=lambda e: (e[2], e[1]))
        rows = []
        for kind, tg, arrived, r, c in events:
            n += int(rng.integers(1, 3))
            ten = tg == "TG07"
            if r is None:
                r = ring(arrived, ten)
            abandoned = c is None and rng.random() < (0.035 if not ten else 0.05)
            answered = None if abandoned else arrived + dt.timedelta(seconds=r)
            gone = arrived + dt.timedelta(seconds=int(rng.integers(2, 40))) if abandoned else \
                answered + dt.timedelta(seconds=int(rng.integers(40, 900)))
            pos = "P%02d" % int(rng.integers(1, 15))
            rec = dict(trunk=tg, cos=cls[tg][int(rng.integers(0, len(cls[tg])))], arrived=arrived,
                       answered=answered, released=gone, position=pos, abandoned=abandoned, medical=c is not None,
                       leg=False)
            rows.append(rec)
            if c is not None:
                c["che_rec"] = rec
                c["ring"] = r
                c["arrived_utc"] = arrived
        self.che = self._che_follow_on(rows)
        for c in self.calls:
            c["che"] = c["che_rec"]["call_id"]

    def _che_follow_on(self, rows):
        """the phone system logs every call a position is offered: the caller's number (masked to its last four
        digits), a caller who rings again after hanging up or after the call ended, a medical caller whose first
        attempt dropped before it was answered, a call the call floor passes to a dispatch position (the passed call
        offered to that position the second the call-taker let it go) and a call answered at a dispatch position when
        the call floor is full. Medical calls stay with the call-taker who answered them. Every record then takes its
        call identifier in the order the calls arrived"""
        rng = np.random.default_rng([121, self.seed, 13])

        def ring(t, ten):
            base = float(rng.gamma(2.2, 2.4)) * _load(t)
            if rng.random() < 0.05 * _load(t):
                base += float(rng.exponential(14.0))
            if ten:
                base = base * 1.8 + float(rng.exponential(9.0))
            return max(1, int(round(base)))

        def caller():
            return "XXX-XXX-%04d" % int(rng.integers(0, 10000))

        def again(rec, t0, busy=False):
            """the number rings again; a caller who hung up unanswered rings back into the same busy spell"""
            ten = rec["trunk"] == "TG07"
            ab = rng.random() < 0.06
            r = ring(t0, ten) + (int(rng.integers(4, 25)) if busy else 0)
            ans = None if ab else t0 + dt.timedelta(seconds=r)
            gone = t0 + dt.timedelta(seconds=int(rng.integers(2, 40))) if ab else \
                ans + dt.timedelta(seconds=int(rng.integers(40, 900)))
            return dict(trunk=rec["trunk"], cos=rec["cos"], ani=rec["ani"], arrived=t0, answered=ans, released=gone,
                        position="P%02d" % int(rng.integers(1, 15)), abandoned=ab, medical=False, leg=False)

        for rec in rows:
            rec["ani"] = caller()
        extra = []
        for rec in rows:
            last = rec
            if rec["medical"]:
                if rng.random() < 0.02:
                    t0 = rec["arrived"] - dt.timedelta(seconds=int(rng.integers(25, 150)))
                    gone = t0 + dt.timedelta(seconds=int(rng.integers(2, 15)))
                    extra.append(dict(trunk=rec["trunk"], cos=rec["cos"], ani=rec["ani"], arrived=t0, answered=None,
                                      released=gone, position="P%02d" % int(rng.integers(1, 15)), abandoned=True,
                                      medical=False, leg=False))
            elif rec["abandoned"]:
                if rng.random() < 0.45:
                    last = again(rec, rec["released"] + dt.timedelta(seconds=int(rng.integers(6, 76))), busy=True)
                    extra.append(last)
            else:
                if rng.random() < 0.06:
                    rec["position"] = "P%02d" % int(rng.integers(15, 21))
                if rng.random() < 0.20:
                    rec["released"] = rec["answered"] + dt.timedelta(seconds=int(rng.integers(15, 151)))
                    t0 = rec["released"]
                    ab = rng.random() < 0.02
                    r2 = max(1, int(round(float(rng.gamma(1.6, 1.9)))))
                    if rng.random() < 0.05:
                        r2 += int(round(float(rng.exponential(12.0))))
                    ans = None if ab else t0 + dt.timedelta(seconds=r2)
                    gone = t0 + dt.timedelta(seconds=int(rng.integers(2, 20))) if ab else \
                        ans + dt.timedelta(seconds=int(rng.integers(30, 600)))
                    pos = "P%02d" % (int(rng.integers(15, 21)) if rng.random() < 0.65 else int(rng.integers(1, 15)))
                    last = dict(trunk=rec["trunk"], cos=rec["cos"], ani=rec["ani"], arrived=t0, answered=ans,
                                released=gone, position=pos, abandoned=ab, medical=False, leg=True)
                    extra.append(last)
            if not last["abandoned"] and rng.random() < 0.02:
                extra.append(again(last, last["released"] + dt.timedelta(seconds=int(rng.integers(120, 2400)))))
        allrows = rows + extra
        # a stranger's call on the same trunk group with the same last four digits never arrives the second another
        # call ends (a passed call is the only record that does)
        ends = collections.Counter((x["trunk"], x["ani"], x["released"]) for x in allrows)
        clash = [x for x in allrows if not x["leg"] and ends[(x["trunk"], x["ani"], x["arrived"])]]
        assert not clash, "%d calls arrive the second a same-number call ends" % len(clash)
        allrows.sort(key=lambda x: (x["arrived"], x["trunk"], x["ani"], x["leg"]))
        rng2 = np.random.default_rng([121, self.seed, 14])
        n = 880000
        for x in allrows:
            n += int(rng2.integers(1, 3))
            x["call_id"] = "%07d" % n
        return allrows

    # ------------------------------------------------------------------ cardiac arrest reviews (Ask B)
    def _tcpr(self):
        """every protocol 09 call with a patient is reviewed from its recording; the recorder starts when the call
        arrives on the trunk, so the reviewer's seconds run from arrival. About one arrest in eight is reviewed a
        second time by another reviewer for calibration"""
        rng = np.random.default_rng([121, self.seed, 6])
        self.tcpr = []
        reviewers = ["QA2", "QA3", "QA5", "QA7"]
        reasons = ["Bystander CPR under way", "Caller unable", "Obvious death", "Caller disconnected"]
        n = 3100
        for c in self.calls:
            if c["protocol"] != "09" or not c["contact"]:
                continue
            recog = max(8, int(round(42.0 * float(np.exp(rng.normal(0, 0.45))))))
            coached = rng.random() >= 0.22
            first = recog + max(12, int(round(66.0 * float(np.exp(rng.normal(0, 0.40)))))) if coached else None
            reason = None if coached else reasons[int(rng.choice(4, p=[0.45, 0.25, 0.2, 0.1]))]
            c["arrest"] = dict(recognised=recog, first=first, reason=reason)
            local_day = to_local(c["utc"]).date()
            n += int(rng.integers(1, 4))
            rv = dict(review_id="TR%05d" % n, incident=c["incident"], reviewer=reviewers[int(rng.integers(0, 4))],
                      reviewed=local_day + dt.timedelta(days=int(rng.integers(3, 25))),
                      start=c["arrived_utc"], recognised=recog + c["ring"],
                      first=None if first is None else first + c["ring"], reason=reason, kind="Primary")
            self.tcpr.append(rv)
            if rng.random() < 0.13:
                n += int(rng.integers(1, 4))
                jit = int(rng.integers(-4, 5))
                cal = dict(rv, review_id="TR%05d" % n, reviewer=[x for x in reviewers if x != rv["reviewer"]][
                    int(rng.integers(0, 3))], reviewed=rv["reviewed"] + dt.timedelta(days=int(rng.integers(5, 40))),
                    recognised=rv["recognised"] + int(rng.integers(-3, 4)),
                    first=None if rv["first"] is None else rv["first"] + jit, kind="Calibration")
                self.tcpr.append(cal)
        # a month whose arrests number evenly can put its median on a half second; the arrest at the upper middle
        # took a second longer to reach its first compression, so every month's median is a whole second
        while True:
            per = collections.defaultdict(list)
            for c in self.calls:
                a_ = c.get("arrest")
                if a_ and a_["first"] is not None:
                    loc = to_local(c["utc"])
                    per[(loc.year, loc.month)].append(c)
            moved = False
            for ym, cs in per.items():
                cs.sort(key=lambda c: (c["arrest"]["first"], c["incident"]))
                n = len(cs)
                if n % 2 == 0 and (cs[n // 2 - 1]["arrest"]["first"] + cs[n // 2]["arrest"]["first"]) % 2 == 1:
                    up = cs[n // 2]
                    up["arrest"]["first"] += 1
                    for rv in self.tcpr:
                        if rv["incident"] == up["incident"] and rv["first"] is not None:
                            rv["first"] += 1
                    moved = True
            if not moved:
                break
        self.tcpr.sort(key=lambda r: r["review_id"])

    # ------------------------------------------------------------------ distractors
    def _distractors(self):
        rng = np.random.default_rng([121, self.seed, 7])
        # protocol case reviews: three in a hundred medical calls drawn at random each month, scored by the QA team
        self.cases = []
        n = 52000
        for c in self.calls:
            if rng.random() < 0.03:
                n += int(rng.integers(1, 5))
                parts = [min(100, int(round(float(rng.normal(m, s))))) for m, s in ((97, 4), (95, 5), (91, 7), (93, 6))]
                self.cases.append(dict(case_id="CR%06d" % n, incident=c["incident"], login=c["login"],
                                       reviewed=to_local(c["utc"]).date() + dt.timedelta(days=int(rng.integers(2, 30))),
                                       parts=parts))
        # the ambulance service's unit hours on duty each day
        self.unit_hours = []
        for d in K.DAYS:
            for u in K.UNITS:
                staffed = 24.0 if u in K.UNITS[:14] else (12.0 if rng.random() < 0.85 else 0.0)
                if staffed and rng.random() < 0.03:
                    staffed -= float(rng.choice([2.0, 4.0, 6.0]))
                self.unit_hours.append((d, u, staffed))
