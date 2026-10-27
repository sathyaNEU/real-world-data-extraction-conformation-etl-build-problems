"""Central Payroll's overtime lines for the checks of 3 July 2025 to 31 July 2026, and the units' overtime offer log for
FY2026. Every line-shift the rosters show off post or vacant is covered on overtime, or left short, by an officer of
the same title: a full shift, or a four-hour holdover and a four-hour call-in; from the unit's own staff or, offered
across the agency, from another unit's. Overtime is keyed by the officer's home timekeeper and paid at time and a half
or taken as compensatory time; the night shift carries a differential; the garages call crews in for winter storms;
the 2026 settlement's 3 per cent increase reached back to 29 June 2025 and was paid as retroactive lines on the check
of 24 April 2026, on every overtime line of the earlier periods it had paid; some timesheets were approved after their
period closed and paid on a later check, and some approved timesheets were sent again and paid twice."""
import datetime as dt

import numpy as np

import common as K
import records as R

PAY_SEED = 133
P_COVER = {"CO": 0.93, "PCO": 0.96, "FSA": 0.91, "HMW": 0.74}
P_SPLIT = 0.18                       # covered by a four-hour holdover and a four-hour call-in instead of one shift
P_BORROW = {"CO": 0.12, "PCO": 0.08, "FSA": 0.0, "HMW": 0.10}
P_LATE = 0.03                        # share of the year's overtime pieces approved after their period closed
P_REPLAY = 0.03                      # share of the year's full-shift overtime whose timesheet was paid again
BASE = {"CO": (25.14, 0.61), "PCO": (22.37, 0.55), "FSA": (19.62, 0.47), "HMW": (21.08, 0.50)}
NIGHT_DIFF = 1.25
RAISE = 0.03
PP0 = dt.date(2025, 6, 15)           # first day of the earliest pay period in the extract
RETRO_FROM = dt.date(2025, 6, 29)    # the settlement's increase took effect with the period beginning 29 June 2025
NEW_RATES_FROM = dt.date(2026, 4, 5)
RETRO_CHECK = dt.date(2026, 4, 24)
RETRO_PERIOD_END = dt.date(2026, 4, 18)
CHECK_FROM, CHECK_TO = dt.date(2025, 7, 1), dt.date(2026, 7, 31)
FY_END = dt.date(2026, 6, 30)
HOLIDAY_CHECKS = {dt.date(2025, 7, 4): dt.date(2025, 7, 3), dt.date(2026, 7, 3): dt.date(2026, 7, 2)}
CHAIN_Q = {"CO": 0.95, "PCO": 1.15, "FSA": 1.75}   # the rehired officers' overtime propensity, a quantile of their title's
MOVER_Q = (0.80, 0.60, 0.60, 0.60)                 # the movers' propensity, in the order of K.MOVERS
COMP_CREDIT = {"CO": 1.5, "PCO": 1.5, "FSA": 1.0, "HMW": 1.5}   # compensatory hours credited for an hour worked; the
                                     # aides' unit (not the Protective Services MOU) credits hour for hour
TWC_SITE = "SL-0410"                 # ShiftLink's site number for Thornmere
OFF = ("VAC", "SICK", "IOD", "TRN", "FMLA", "MIL", "V")
START_H = {"D": 7, "E": 15, "N": 23}


def period_of(d):
    """(start, end, check) of the biweekly pay period holding date d"""
    k = (d - PP0).days // 14
    start = PP0 + dt.timedelta(days=14 * k)
    end = start + dt.timedelta(days=13)
    check = end + dt.timedelta(days=6)
    return start, end, HOLIDAY_CHECKS.get(check, check)


def money(x):
    from decimal import ROUND_HALF_UP, Decimal
    return float(Decimal(repr(float(x))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def night_hours(start_h, hours):
    n = 0.0
    for q in range(int(round(hours * 4))):
        h = (start_h + q / 4.0) % 24
        if h >= 23 or h < 7:
            n += 0.25
    return n


class Payroll:
    def __init__(self, w, rc, seed=PAY_SEED, chain_q=None, mover_q=None):
        self.w, self.rc = w, rc
        self.seed = seed
        self.chain_q = dict(CHAIN_Q, **(chain_q or {}))
        self.mover_q = tuple(mover_q or MOVER_Q)
        self.rng = np.random.default_rng(seed)
        self.rng_offer = np.random.default_rng(seed + 101)
        self.rng_replay = np.random.default_rng(seed + 206)
        self._people()
        self._events()
        self._reinstate()
        self._lines()

    # ---------------------------------------------------------------------------------------------- people
    def _people(self):
        w, rc, rng = self.w, self.rc, self.rng
        n = len(w.people)
        self.base = np.zeros(n)
        self.prop = np.exp(rng.normal(0.0, 0.85, n))
        self.comp = np.where(rng.uniform(size=n) < 0.22, rng.uniform(0.35, 0.9, n), 0.0)
        for e, p in enumerate(w.people):
            b0, step = BASE[p["title"]]
            svc = p["service"]
            if e in rc.rehire_of:
                svc = w.people[rc.rehire_of[e]]["service"]
            self.base[e] = round(b0 + step * min(svc, 25) + rng.uniform(-0.4, 0.4), 2)
        # the officers who left and came back worked a great deal of overtime on both records
        for new, old in rc.rehire_of.items():
            t = w.people[new]["title"]
            same = [e for e, p in enumerate(w.people) if p["title"] == t]
            q = self.chain_q[t]
            hi = float(np.quantile(self.prop[same], min(q, 1.0))) * max(q, 1.0)
            self.prop[new] = self.prop[old] = hi
            self.comp[new] = self.comp[old] = 0.0
            self.base[new] = self.base[old]
        order = [m[0] for m in K.MOVERS]
        for e in sorted(rc.movers, key=lambda e: order.index(w.people[e]["unit"])):
            k = order.index(w.people[e]["unit"])
            t = w.people[e]["title"]
            same = [x for x, p in enumerate(w.people) if p["title"] == t]
            q = self.mover_q[k]
            self.prop[e] = float(np.quantile(self.prop[same], min(q, 1.0))) * max(q, 1.0)
            self.comp[e] = 0.0
        # each unit's staff on each day: available or off post, and the shift of their own line if they work one
        self.staff = {}
        for j, ln in enumerate(w.lines):
            for i in range(K.FY26_DAYS):
                e = w.holder[j, i]
                if e < 0:
                    continue
                s = self.staff.setdefault((ln["unit"], i), {})
                st = w.status[j, i]
                ok = st not in ("VAC", "SICK", "IOD", "FMLA", "MIL", "TRN")
                own = ln["shift"] if (w.on[j, i] and st == "W") else None
                prev = s.get(e)
                s[e] = (ok, own) if prev is None else (prev[0] and ok, prev[1] or own)
        self.used = {}                    # (person, date) -> [(start hour, hours)]

    def eligible(self, unit, i, date, shift, start_h, hours):
        out = []
        for e, (ok, own) in self.staff.get((unit, i), {}).items():
            if not ok or own == shift:
                continue
            p = self.w.people[e]
            if date < K.FY26_START and (p["start"] > 0 or self.rc.cls[e] == "2025-1"):
                continue
            done = self.used.get((e, date), [])
            if hours > 4 and done:
                continue
            if hours <= 4 and (sum(h for _, h in done) + hours > 8 or any(s == start_h for s, _ in done)):
                continue
            out.append(e)
        return out

    # ---------------------------------------------------------------------------------------------- events
    def _need(self, i):
        """the line-shifts off post or vacant on FY2026 day i: (unit, shift)"""
        w = self.w
        out = []
        for j, ln in enumerate(w.lines):
            if w.on[j, i] and w.status[j, i] in OFF:
                out.append((ln["unit"], ln["shift"]))
        return out

    def _events(self):
        """one event per overtime piece"""
        rng, ro = self.rng, self.rng_offer
        days = [(dt.date(2025, 6, 15) + dt.timedelta(days=k), 349 + k) for k in range(16)] + \
               [(K.fy26_day(i), i) for i in range(K.FY26_DAYS)] + \
               [(dt.date(2026, 7, 1) + dt.timedelta(days=k), k) for k in range(25)]
        self.events = []
        for date, i in days:
            pi_day = 0 if date < K.FY26_START else (K.FY26_DAYS - 1 if date >= dt.date(2026, 7, 1) else i)
            for u, s in self._need(i):
                t = K.UNIT_TITLE[u]
                if rng.uniform() >= P_COVER[t]:
                    continue
                pieces = [(START_H[s], 8.0)] if rng.uniform() >= P_SPLIT else [(START_H[s], 4.0),
                                                                               ((START_H[s] + 4) % 24, 4.0)]
                for k, (h0, h) in enumerate(pieces):
                    src = u
                    if rng.uniform() < P_BORROW[t]:
                        others = [v for v in K.UNIT_CODES if K.UNIT_TITLE[v] == t and v != u]
                        src = others[int(rng.integers(0, len(others)))]
                    pool = self.eligible(src, pi_day, date, s, h0, h)
                    if not pool:
                        continue
                    pr = self.prop[pool] / self.prop[pool].sum()
                    e = int(pool[int(rng.choice(len(pool), p=pr))])
                    self.used.setdefault((e, date), []).append((h0, h))
                    if src != u:
                        vol = True
                    elif h > 4:
                        vol = ro.uniform() < 0.8
                    elif k == 0:
                        vol = ro.uniform() < 0.3
                    else:
                        vol = ro.uniform() < 0.85
                    self.events.append(dict(e=e, date=date, unit=u, shift=s, start=h0, hours=h,
                                            night=night_hours(h0, h), comp=None, vol=vol, pool=pool))
        self._storms()
        self.events.sort(key=lambda x: (x["date"], x["e"], x["unit"], x["start"]))

    def _storms(self):
        """winter storms: the garages call crews in beyond the rota for the length of the event, up to twelve hours"""
        import context as CX
        rng = np.random.default_rng(self.seed + 5)
        for r in CX.winter_rows()[1]:
            u = r[1]
            if u not in K.UNIT_CODES:
                continue
            t0 = dt.datetime.strptime(r[3], "%Y-%m-%d %H:%M").replace(minute=0)
            t1 = dt.datetime.strptime(r[4], "%Y-%m-%d %H:%M")
            dur = (t1 - t0).total_seconds() / 3600.0
            i = (t0.date() - K.FY26_START).days
            pool = [e for e, (ok, own) in self.staff.get((u, i), {}).items()
                    if ok and own is None and not self.used.get((e, t0.date()))]
            n = min(len(pool), 4, max(1, int(r[5]) // 3))
            if not n:
                continue
            pr = self.prop[pool] / self.prop[pool].sum()
            for k in rng.choice(len(pool), size=n, replace=False, p=pr):
                e = int(pool[int(k)])
                h = float(min(12, max(4, int(round(dur)))))
                self.used.setdefault((e, t0.date()), []).append((t0.hour, h))
                comp = bool(self.comp[e] > 0 and rng.uniform() < self.comp[e])
                self.events.append(dict(e=e, date=t0.date(), unit=u, shift="X", start=t0.hour, hours=h,
                                        night=night_hours(t0.hour, h), comp=comp, vol=False, pool=[]))

    def _reinstate(self):
        """the garages' heaviest overtime worker who held one line all year resigned and was reinstated to it after the
        days off between, under a new employee number with the seniority date restored"""
        w, rc = self.w, self.rc
        fy = [ev for ev in self.events if K.FY26_START <= ev["date"] <= FY_END]
        hours = {}
        for ev in fy:
            hours[ev["e"]] = hours.get(ev["e"], 0.0) + ev["hours"]
        skip = set(rc.movers) | set(rc.rehire_of) | set(rc.rehire_of.values())
        cands = sorted((e for e, q in enumerate(w.people) if q["title"] == "HMW" and e not in skip and
                        q["cls"] != "2025-1" and hours.get(e, 0.0) > 620), key=lambda e: (-hours[e], e))
        lo, hi = (dt.date(2025, 9, 1) - K.FY26_START).days, (dt.date(2026, 5, 31) - K.FY26_START).days
        for e in cands:
            js = [j for j in range(len(w.lines)) if (w.holder[j] == e).all()]
            if not js:
                continue
            j = js[0]
            worked = {ev["date"] for ev in self.events if ev["e"] == e}
            best = None
            for i in range(lo, hi):
                if not (w.on[j, i] and not w.on[j, i + 1]):
                    continue
                back = next(x for x in range(i + 1, K.FY26_DAYS) if w.on[j, x])
                if back - i > 4 or {K.fy26_day(x) for x in range(i + 1, back)} & worked:
                    continue
                a = sum(ev["hours"] for ev in fy if ev["e"] == e and ev["date"] <= K.fy26_day(i))
                b = hours[e] - a
                if a < 575 and b < 575 and (best is None or min(a, b) > best[0]):
                    best = (min(a, b), K.fy26_day(i), K.fy26_day(back))
            if best:
                rc.reinstate(e, best[1], best[2])
                return

    def away(self, e, d):
        """between leaving and coming back"""
        r = self.rc.reinstated
        return r is not None and e == r[0] and r[1] < d < r[2]

    # ---------------------------------------------------------------------------------------------- lines
    def rate(self, e, d):
        b = self.base[e]
        if d >= NEW_RATES_FROM:
            b = round(b * (1 + RAISE), 2)
        return money(1.5 * b)

    def location(self, e, d):
        u = self.w.people[e]["unit"]
        return TWC_SITE if (u == "TWC" and d >= K.fy26_day(R.MIGRATION_DAY)) else u

    def _lines(self):
        rc, rng = self.rc, self.rng
        rows = []
        self.ot_by_period = {}
        for ev in self.events:
            e, d, h, night = ev["e"], ev["date"], ev["hours"], ev["night"]
            start, end, check = period_of(d)
            if not (CHECK_FROM <= check <= CHECK_TO):
                continue
            loc = self.location(e, d)
            cc = K.COST_CENTER[self.w.people[e]["unit"]]
            st = "%02d:00" % ev["start"]
            pre = ev["comp"]
            take_comp = pre if pre is not None else (self.comp[e] > 0 and rng.uniform() < self.comp[e])
            rid = rc.id_on(e, d)
            if take_comp:
                cr = COMP_CREDIT[self.w.people[e]["title"]]
                rows.append([check, end, rid, cc, loc, "CTE" if cr == 1.5 else "CTS", d, st, "", "", cr * h, "", 0.0])
            else:
                r = self.rate(e, d)
                rows.append([check, end, rid, cc, loc, "OT", d, st, "", "", h, r, money(h * r)])
                if RETRO_FROM <= d < NEW_RATES_FROM:
                    self.ot_by_period.setdefault((e, rid, start, end), []).append((d, h))
            if night:
                rows.append([check, end, rid, cc, loc, "OTN", d, st, "", "", night, NIGHT_DIFF,
                             money(night * NIGHT_DIFF)])
        idx = {v: k for k, v in enumerate(rc.emp_id)}
        if rc.reinstated is not None:
            idx[rc.reinstated[3]] = rc.reinstated[0]

        def later(end, k):
            end = end + dt.timedelta(days=14 * k)
            c = end + dt.timedelta(days=6)
            return HOLIDAY_CHECKS.get(c, c), end
        # timesheets approved after their period closed: the piece paid in full on a later check
        rng_late = np.random.default_rng(self.seed + 404)
        pieces = {}
        for x in rows:
            pieces.setdefault((x[2], x[6], x[7]), []).append(x)
        self.late = []
        for key, xs in pieces.items():
            d = xs[0][6]
            if not (K.FY26_START <= d <= FY_END) or rng_late.uniform() >= P_LATE:
                continue
            check, end = later(xs[0][1], int(rng_late.integers(1, 3)))
            if check > CHECK_TO or (d < NEW_RATES_FROM and check >= RETRO_CHECK):
                continue
            for x in xs:
                x[0], x[1] = check, end
            self.late.append(key)
        # approved timesheets sent to Central Payroll again when a supervisor reopened them to correct another day:
        # the same overtime paid again on a later check
        self.replays = []
        extra = []
        otn = {(x[2], x[6], x[7]): x for x in rows if x[5] == "OTN"}
        for r in rows:
            if r[5] != "OT" or r[10] != 8.0 or not (K.FY26_START <= r[6] <= FY_END):
                continue
            if self.rng_replay.uniform() >= P_REPLAY:
                continue
            check, end = later(r[1], int(self.rng_replay.integers(1, 4)))
            if check > CHECK_TO or (r[6] < NEW_RATES_FROM and check >= RETRO_CHECK):
                continue
            twin = otn.get((r[2], r[6], r[7]))
            for x in [r] + ([twin] if twin else []):
                extra.append([check, end] + x[2:])
            self.replays.append((r[2], r[6], r[7]))
            if RETRO_FROM <= r[6] < NEW_RATES_FROM:
                s, e_, _ = period_of(r[6])
                self.ot_by_period[(idx[r[2]], r[2], s, e_)].append((r[6], r[10]))
        rows += extra
        # the settlement's retroactive overtime, one line per officer and original pay period
        for (e, rid, start, end), items in sorted(self.ot_by_period.items(), key=lambda kv: (kv[0][2], kv[0][0], kv[0][1])):
            hours = sum(h for _, h in items)
            old = money(1.5 * self.base[e])
            new = money(1.5 * round(self.base[e] * (1 + RAISE), 2))
            diff = round(new - old, 2)
            sp_start = max(start, RETRO_FROM)
            u = self.w.people[e]["unit"]
            rows.append([RETRO_CHECK, RETRO_PERIOD_END, rid, K.COST_CENTER[u], "", "OTR", "", "",
                         sp_start, end, hours, diff, money(hours * diff)])
        rows.sort(key=lambda r: (r[0], r[2], r[6] or r[8], r[7], r[5]))
        self.rows = rows

    def payroll_rows(self):
        out = []
        for r in self.rows:
            check, end, emp, cc, loc, code, d, st, sps, spe, h, rate, amt = r
            out.append([R.iso(check), R.iso(end), emp, cc, loc, code, R.iso(d) if d else "", st,
                        R.iso(sps) if sps else "", R.iso(spe) if spe else "",
                        ("%.2f" % h), ("%.2f" % rate) if rate != "" else "", "%.2f" % amt])
        return (["check_date", "pay_period_end", "employee_id", "home_cost_center", "home_timekeeper", "earn_code",
                 "work_date", "start_time", "service_period_start", "service_period_end", "hours", "rate", "amount"],
                out)

    # ---------------------------------------------------------------------------------------------- offers
    def offer_rows(self):
        """the voluntary pieces of FY2026 as the units' offer lists recorded them: the offers declined or unanswered,
        then the acceptance"""
        rc = self.rc
        rng = np.random.default_rng(self.seed + 303)
        rows = []
        for ev in self.events:
            d = ev["date"]
            if not ev["vol"] or not (K.FY26_START <= d <= dt.date(2026, 6, 30)):
                continue
            at = dt.datetime.combine(d, dt.time(ev["start"]))
            lead = float(rng.uniform(2, 30)) if ev["hours"] > 4 else float(rng.uniform(0.5, 6))
            t = at - dt.timedelta(hours=lead)
            others = [x for x in ev["pool"] if x != ev["e"] and not self.away(x, d)]
            n = min(len(others), int(rng.geometric(0.5)) - 1, 4)
            asked = [others[int(k)] for k in rng.choice(len(others), size=n, replace=False)] if n else []
            for x in asked:
                rows.append([t, ev["unit"], d, ev["shift"], ev["start"], ev["hours"], rc.id_on(x, d),
                             "Declined" if rng.uniform() < 0.7 else "No answer"])
                t += dt.timedelta(minutes=int(rng.integers(4, 40)))
            rows.append([t, ev["unit"], d, ev["shift"], ev["start"], ev["hours"], rc.id_on(ev["e"], d), "Accepted"])
        rows.sort(key=lambda r: (r[0], r[1], r[6]))
        return (["offered_at", "post_unit", "post_date", "shift", "start_time", "hours", "employee_id", "response"],
                [[r[0].strftime("%Y-%m-%d %H:%M"), r[1], r[2].isoformat(), r[3], "%02d:00" % r[4], "%.2f" % r[5],
                  r[6], r[7]] for r in rows])
