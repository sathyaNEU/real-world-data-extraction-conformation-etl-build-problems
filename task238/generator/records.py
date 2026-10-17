"""task238 records: the households of sim.World turned into what the office's systems hold. The sample management
system's issued-sample extract (one row per address, its final outcome as that system set it), the web platform's
export (one row per web session, stamped in UTC), the CATI system's export (one row per interview, stamped in Halvreth
clock time), the CATI call log, the published series and the region lookup.

Every record carries the system that holds it and the mode the household actually answered in: they differ only for
the interviews keyed through the web platform while the CATI system was down (9 to 12 August 2027)."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import params as P

MT = ZoneInfo(P.TZ)
UTC = dt.timezone.utc
ALPHA = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
ITEMS = ["Q01", "Q02", "Q03", "Q04", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16", "Q17"]
SECTION = {"Q01": 1, "Q02": 1, "Q03": 1, "Q04": 1, "Q10": 2, "Q11": 2, "Q12": 2, "Q13": 3, "Q14": 3, "Q15": 3,
           "Q16": 4, "Q17": 4}
DEMO = ["age", "sex", "qual", "emp", "tenure", "hhsize"]
ITEM_OF = {x[0]: x[2] for x in P.INDEXES}
CODE_OF = {x[2]: x[0] for x in P.INDEXES}
# web: share left unanswered (blank), share answering prefer not to say (-7, offered on Q14, Q15 and Q17)
WEB_MISS = {"Q01": (0.004, 0), "Q02": (0.005, 0), "Q03": (0.004, 0), "Q04": (0.006, 0), "Q10": (0.009, 0),
            "Q11": (0.011, 0), "Q12": (0.008, 0), "Q13": (0.005, 0), "Q14": (0.004, 0.013), "Q15": (0.006, 0.028),
            "Q16": (0.007, 0), "Q17": (0.007, 0.031)}
# telephone: share don't know (-8), share refused (-9)
CATI_MISS = {"Q01": (0.005, 0.002), "Q02": (0.007, 0.002), "Q03": (0.004, 0.002), "Q04": (0.006, 0.003),
             "Q10": (0.004, 0.004), "Q11": (0.021, 0.003), "Q12": (0.006, 0.002), "Q13": (0.003, 0.002),
             "Q14": (0.001, 0.006), "Q15": (0.004, 0.012), "Q16": (0.003, 0.002), "Q17": (0.008, 0.016)}


def close_utc(q):
    d = P.Q_END[P.QUARTERS[q]]
    return dt.datetime(d.year, d.month, d.day, 23, 59, tzinfo=MT).astimezone(UTC)


def mailing(q, b):
    return P.Q_START[P.QUARTERS[q]] + dt.timedelta(days=14 * int(b))


def _local(day, minutes):
    return dt.datetime(day.year, day.month, day.day, tzinfo=MT) + dt.timedelta(minutes=float(minutes))


def _web_time(rng, day):
    """a web submission on a given Halvreth day: evenings busiest"""
    k = rng.choice(3, p=[0.22, 0.30, 0.48])
    lo, hi = [(7 * 60, 12 * 60), (12 * 60, 18 * 60), (18 * 60, 23 * 60 + 58)][k]
    return _local(day, rng.uniform(lo, hi))


def _cati_time(rng, day):
    """the end of a telephone interview: weekdays 09:30 to 20:45, Saturdays 10:30 to 16:30, no Sundays"""
    while day.weekday() == 6:
        day = day + dt.timedelta(days=1)
    lo, hi = (10.5 * 60, 16.5 * 60) if day.weekday() == 5 else (9.5 * 60, 20.75 * 60)
    return _local(day, rng.uniform(lo, hi))


def in_outage(t_local):
    return P.OUTAGE[0] <= t_local.date() <= P.OUTAGE[1]


class Records:
    def __init__(self, W):
        self.W = W
        n = W.n
        self.n = n
        rng = np.random.default_rng(P.SEED + 1)
        serial = rng.permutation(np.arange(110000, 110000 + n * 3))[:n]
        self.address_id = np.array(["MA%06d" % s for s in serial])
        codes, login = set(), []
        while len(login) < n:
            c = "".join(rng.choice(list(ALPHA), 8))
            if c not in codes:
                codes.add(c)
                login.append(c)
        self.login = np.array(login)
        self.batch = np.zeros(n, dtype=int)
        for q in range(len(P.QUARTERS)):
            idx = np.flatnonzero(W.quarter == q)
            self.batch[idx] = rng.permutation(np.arange(len(idx)) % P.BATCHES)
        self.mailed = [mailing(q, b) for q, b in zip(W.quarter, self.batch)]
        self.dwelling = rng.choice(["house", "flat", "rural"], n, p=[0.71, 0.21, 0.08])
        self._events()
        self._answers()

    # ------------------------------------------------------------------ who submitted what, when
    def _ev(self, i, system, mode, t_utc, kind, answers, status="complete", section=6, opened="respondent"):
        self.events.append(dict(i=int(i), system=system, mode=mode, utc=t_utc, kind=kind, answers=answers,
                                status=status, section=section, opened=opened))

    def _events(self):
        W = self.W
        rng = np.random.default_rng(P.SEED + 2)
        self.events = []
        self.counted = {}
        for i in np.flatnonzero(W.complete):
            q = W.quarter[i]
            close = close_utc(q)
            mail = self.mailed[i]
            span = (P.Q_END[P.QUARTERS[q]] - mail).days
            for _ in range(500):
                if W.web[i]:
                    if W.letter_a[i]:
                        k = rng.choice(3, p=[0.52, 0.30, 0.18])
                        d = [rng.integers(2, 8), rng.integers(8, 15), rng.integers(15, 46)][k]
                    else:
                        d = rng.integers(12, 52)
                    t = _web_time(rng, mail + dt.timedelta(days=int(min(d, span))))
                else:
                    d = rng.integers(15, 52) if W.letter_a[i] else rng.integers(3, 46)
                    t = _cati_time(rng, mail + dt.timedelta(days=int(min(d, span))))
                if t.astimezone(UTC) <= close and t.date() >= mail:
                    break
            tu = t.astimezone(UTC)
            if W.web[i]:
                self._ev(i, "web", "web", tu, "complete", "own")
            elif in_outage(t):
                self._ev(i, "web", "cati", tu, "complete", "own", opened="staff")
            else:
                self._ev(i, "cati", "cati", tu, "complete", "own")
            self.counted[int(i)] = len(self.events) - 1
        self._duplicates(np.random.default_rng(P.SEED + 3))
        self._late(np.random.default_rng(P.SEED + 4))
        self._teen(np.random.default_rng(P.SEED + 5))
        self._partials(np.random.default_rng(P.SEED + 6))
        self._helpline(np.random.default_rng(P.SEED + 7))

    def _duplicates(self, rng):
        """the nightly feed from the web platform to the CATI system lets a household be interviewed after it has
        submitted online, and some households submit online after their interview"""
        W = self.W
        base = [e for e in self.events if e["kind"] == "complete" and e["opened"] == "respondent"]
        for e in base:
            i = e["i"]
            t_loc = e["utc"].astimezone(MT)
            close = close_utc(W.quarter[i])
            if e["system"] == "web" and W.letter_a[i] and (t_loc.date() - self.mailed[i]).days >= 15:
                if rng.random() < 0.045:
                    t2 = _cati_time(rng, (t_loc + dt.timedelta(hours=float(rng.uniform(0.5, 20)))).date())
                    if t2 <= t_loc:
                        t2 = t_loc + dt.timedelta(minutes=float(rng.uniform(25, 95)))
                    if t2.astimezone(UTC) <= close and not in_outage(t2) and 9 <= t2.hour < 21:
                        self._ev(i, "cati", "cati", t2.astimezone(UTC), "duplicate", "other")
            elif e["system"] == "cati":
                end_q3 = t_loc.date() >= dt.date(2027, 9, 26)
                p = 0.03 if end_q3 else (0.012 if not W.letter_a[i] else 0.008)
                if rng.random() < p:
                    if end_q3:
                        gap = rng.uniform(0.2, 0.95)
                    else:
                        gap = rng.uniform(0.3, 11.5) if rng.random() < 0.55 else rng.uniform(11.5, 30)
                    t2 = t_loc + dt.timedelta(hours=float(gap))
                    if t2.astimezone(UTC) <= close:
                        self._ev(i, "web", "web", t2.astimezone(UTC), "duplicate", "other")

    def _late(self, rng):
        """web returns submitted after the quarter's close by households with no complete by then"""
        W = self.W
        for q in range(len(P.QUARTERS)):
            close = close_utc(q)
            free = W.eligible & ~W.complete & (W.quarter == q) & (self.batch >= 3)
            pick = list(rng.choice(np.flatnonzero(free & W.letter_a), 172, replace=False)) + \
                list(rng.choice(np.flatnonzero(free & ~W.letter_a), 44, replace=False))
            pick = [pick[k] for k in rng.permutation(len(pick))]
            for k, i in enumerate(pick):
                if k < 52:
                    tu = close + dt.timedelta(minutes=float(min(rng.exponential(55) + 1, 178)))
                else:
                    tu = close + dt.timedelta(hours=float(rng.uniform(3, 24 * 10)))
                self._ev(i, "web", "web", tu, "late", "nonresp")

    def _teen(self, rng):
        """returns completed by a household member under 18 instead of the selected adult"""
        W = self.W
        taken = {e["i"] for e in self.events}
        for q in range(len(P.QUARTERS)):
            close = close_utc(q)
            free = W.eligible & ~W.complete & (W.quarter == q)
            pool_a = [i for i in np.flatnonzero(free & W.letter_a) if i not in taken]
            pool_b = [i for i in np.flatnonzero(free & ~W.letter_a) if i not in taken]
            pick = list(rng.choice(pool_a, 69, replace=False)) + list(rng.choice(pool_b, 13, replace=False))
            for i in pick:
                mail = self.mailed[i]
                span = (P.Q_END[P.QUARTERS[q]] - mail).days
                for _ in range(200):
                    t = _web_time(rng, mail + dt.timedelta(days=int(min(rng.integers(2, 30), span))))
                    if t.astimezone(UTC) <= close and t.date() >= mail:
                        break
                self._ev(i, "web", "web", t.astimezone(UTC), "teen", "teen")

    def _partials(self, rng):
        """web sessions abandoned part way and interviews broken off, from households with no complete"""
        W = self.W
        taken = {e["i"] for e in self.events}
        for q in range(len(P.QUARTERS)):
            close = close_utc(q)
            pool = np.array([i for i in np.flatnonzero(W.eligible & ~W.complete & (W.quarter == q)) if i not in taken])
            web = rng.choice(pool, 548, replace=False)
            cati = rng.choice(np.setdiff1d(pool, web), 66, replace=False)
            for i, system in [(i, "web") for i in web] + [(i, "cati") for i in cati]:
                mail = self.mailed[i]
                span = (P.Q_END[P.QUARTERS[q]] - mail).days
                for _ in range(200):
                    day = mail + dt.timedelta(days=int(min(rng.integers(2, 40), span)))
                    t = _web_time(rng, day) if system == "web" else _cati_time(rng, day)
                    if t.astimezone(UTC) <= close and t.date() >= mail and not (system == "cati" and in_outage(t)):
                        break
                sec = int(rng.choice([1, 2, 3, 4, 5], p=[0.36, 0.24, 0.18, 0.12, 0.10]))
                self._ev(i, system, system, t.astimezone(UTC), "partial", "nonresp", status="partial", section=sec)

    def _helpline(self, rng):
        """the help line reissues a household's link and the household completes online: a session opened by staff"""
        for e in self.events:
            if e["kind"] == "complete" and e["system"] == "web" and e["mode"] == "web":
                if not in_outage(e["utc"].astimezone(MT)) and rng.random() < 0.016:
                    e["opened"] = "staff"

    # ------------------------------------------------------------------ answers on each record
    def _answers(self):
        W = self.W
        rng = np.random.default_rng(P.SEED + 8)
        for e in self.events:
            i = e["i"]
            a = {}
            if e["answers"] == "teen":
                for code, name, item, kind, tol, th in P.INDEXES:
                    a[item] = self._teen_item(rng, code)
                a.update(age=int(rng.integers(15, 18)), sex=int(rng.choice([1, 2, 3], p=[0.48, 0.49, 0.03])), qual=2,
                         emp=4, tenure=int(rng.choice([1, 2, 3], p=[0.25, 0.45, 0.30])),
                         hhsize=int(max(3, W.hh[i])))
            else:
                web = e["mode"] == "web"
                for code, name, item, kind, tol, th in P.INDEXES:
                    v = int(W.ans[code][1 if web else 0][i])
                    if e["answers"] == "other":
                        if kind == "score" and rng.random() < 0.3:
                            v = int(np.clip(v + rng.choice([-1, 1]), 0, 10))
                        elif kind == "pct" and rng.random() < 0.05:
                            v = 1 - v
                    a[item] = v if kind == "score" else self._category(rng, code, v)
                a.update(self._demo(rng, i))
            e["a"] = a
            self._missing(rng, e)

    def _category(self, rng, code, yes):
        pick = lambda vals, p: int(rng.choice(vals, p=p))
        if code == "LN":
            return pick([4, 5], [0.76, 0.24]) if yes else pick([1, 2, 3], [0.36, 0.36, 0.28])
        if code == "TR":
            return 1 if yes else pick([2, 3], [0.8, 0.2])
        if code == "SF":
            return pick([1, 2], [0.44, 0.56]) if yes else pick([3, 4, 5], [0.52, 0.24, 0.24])
        if code == "GH":
            return pick([1, 2], [0.41, 0.59]) if yes else pick([3, 4, 5], [0.70, 0.22, 0.08])
        if code == "SM":
            return pick([1, 2], [0.70, 0.30]) if yes else 3
        if code == "BD":
            return pick([1, 2, 3, 4, 5, 6, 7], [0.55, 0.24, 0.10, 0.05, 0.03, 0.02, 0.01]) if yes else 0
        if code == "VL":
            return 1 if yes else 2
        if code == "FS":
            return pick([4, 5], [0.70, 0.30]) if yes else pick([1, 2, 3], [0.30, 0.40, 0.30])
        raise KeyError(code)

    def _teen_item(self, rng, code):
        score = {"LS": 7.2, "WW": 7.0, "HY": 7.3, "AX": 3.6}
        if code in score:
            return int(np.clip(np.round(rng.normal(score[code], 2.0)), 0, 10))
        p = {"LN": 0.14, "TR": 0.38, "SF": 0.60, "GH": 0.86, "SM": 0.05, "BD": 0.09, "VL": 0.34, "FS": 0.09}[code]
        return self._category(rng, code, int(rng.random() < p))

    def _demo(self, rng, i):
        W = self.W
        sex = 3 if rng.random() < 0.004 else (2 if W.female[i] else 1)
        qual = 4 if W.deg[i] else (3 if W.post[i] else int(rng.choice([1, 2], p=[0.27, 0.73])))
        if W.emp[i]:
            emp = 1
        elif W.age[i] >= 65:
            emp = 3
        else:
            emp = int(rng.choice([2, 4, 5, 6], p=[0.30, 0.20, 0.35, 0.15]))
        if W.rent[i]:
            ten = 3
        else:
            ten = 1 if rng.random() < (0.62 if W.age[i] >= 55 else 0.18) else 2
        return dict(age=int(W.age[i]), sex=sex, qual=qual, emp=emp, tenure=ten, hhsize=int(W.hh[i]))

    def _missing(self, rng, e):
        a = e["a"]
        if e["status"] == "partial":
            for it in ITEMS:
                if SECTION[it] > e["section"]:
                    a[it] = None
            if e["section"] < 5:
                for d in DEMO:
                    a[d] = None
        web_system = e["system"] == "web"
        staff_interview = e["system"] == "web" and e["mode"] == "cati"
        for it in ITEMS:
            if a[it] is None:
                continue
            u = rng.random()
            if web_system and not staff_interview:
                blank, pnts = WEB_MISS[it]
                if u < blank:
                    a[it] = None
                elif u < blank + pnts:
                    a[it] = -7
            else:
                dk, rf = CATI_MISS[it]
                if u < dk:
                    a[it] = None if staff_interview else -8
                elif u < dk + rf:
                    if staff_interview:
                        a[it] = -7 if WEB_MISS[it][1] > 0 else None
                    else:
                        a[it] = -9

    # ------------------------------------------------------------------ the systems' files
    def issued(self, salt=0):
        """the sample management system's extract: one row per issued address, its final outcome as the system
        set it (a web submission sets 1.1 whenever it arrives, unless the field team has already locked the address
        as ineligible)"""
        W = self.W
        rng = np.random.default_rng(P.SEED + 9 + 1000 * salt)
        by = {}
        for e in self.events:
            by.setdefault(e["i"], []).append(e)
        # addresses a telephone contact reported unoccupied or not a home, locked as ineligible by the field team
        # before the household's own web return arrived: the system keeps a field team's ineligibility code
        locked = {}
        for q in range(len(P.QUARTERS)):
            for L in (True, False):
                cand = [e for e in self.events if e["kind"] == "complete" and e["system"] == "web" and e["mode"] == "web"
                        and e["opened"] == "respondent" and W.quarter[e["i"]] == q and W.letter_a[e["i"]] == L
                        and (e["utc"].astimezone(MT).date() - self.mailed[e["i"]]).days >= 9]
                for k in rng.choice(len(cand), 36, replace=False):
                    e = cand[k]
                    locked[e["i"]] = (str(rng.choice(["4.1", "4.2"], p=[0.8, 0.2])),
                                      e["utc"].astimezone(MT).date() - dt.timedelta(days=int(rng.integers(1, 6))))
        rows = []
        for i in range(self.n):
            q = W.quarter[i]
            evs = sorted(by.get(i, []), key=lambda e: e["utc"])
            comp = [e for e in evs if e["status"] == "complete"]
            part = [e for e in evs if e["status"] == "partial"]
            if i in locked:
                out, when = locked[i]
            elif comp:
                out, when = "1.1", comp[0]["utc"].astimezone(MT).date()
            elif part:
                out, when = "1.2", part[0]["utc"].astimezone(MT).date()
            elif not W.eligible[i]:
                if rng.random() < 0.72:
                    out = W.elig[i]
                    when = self.mailed[i] + dt.timedelta(days=int(rng.integers(4, 30)))
                else:
                    out, when = "3.1", P.Q_END[P.QUARTERS[q]]
            else:
                out = str(rng.choice(["2.1", "2.2", "2.3", "3.1"], p=[0.28, 0.42, 0.06, 0.24]))
                when = (self.mailed[i] + dt.timedelta(days=int(rng.integers(5, 50)))) if out == "2.1" else P.Q_END[P.QUARTERS[q]]
                when = min(when, P.Q_END[P.QUARTERS[q]])
            rows.append((self.address_id[i], self.login[i], P.QUARTERS[q], int(self.batch[i]) + 1, int(W.region[i]),
                         self.dwelling[i], "A" if W.letter_a[i] else "B", self.mailed[i].isoformat(), out,
                         when.isoformat()))
        df = pd.DataFrame(rows, columns=["address_id", "login_code", "quarter", "release", "region_code", "dwelling_type",
                                         "letter", "letter_mailed", "final_outcome", "outcome_date"])
        return df.sort_values(["quarter", "release", "address_id"]).reset_index(drop=True)

    def web_export(self):
        rng = np.random.default_rng(P.SEED + 10)
        rows = []
        evs = sorted((e for e in self.events if e["system"] == "web"), key=lambda e: e["utc"])
        ids = rng.permutation(np.arange(3000000, 3000000 + 3 * len(evs)))[:len(evs)]
        ids.sort()
        for rid, e in zip(ids, evs):
            if e["mode"] == "cati":
                dur = rng.uniform(19, 34)
                device = "desktop"
            else:
                dur = float(np.clip(rng.lognormal(np.log(15.5), 0.35), 6, 90))
                device = str(rng.choice(["mobile", "desktop", "tablet"], p=[0.58, 0.33, 0.09]))
            if e["status"] == "partial":
                dur = dur * e["section"] / 7.0
            start = e["utc"] - dt.timedelta(minutes=float(dur))
            fmt = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")
            r = dict(response_id="R%07d" % rid, login_code=self.login[e["i"]], opened_by=e["opened"], device_type=device,
                     started_utc=fmt(start), submitted_utc=fmt(e["utc"]) if e["status"] == "complete" else "",
                     last_saved_utc=fmt(e["utc"]), last_section=6 if e["status"] == "complete" else e["section"])
            for it in ITEMS:
                r[it] = e["a"][it]
            for d in DEMO:
                r[d] = e["a"][d]
            rows.append(r)
        df = pd.DataFrame(rows)
        for c in ITEMS + DEMO:
            df[c] = df[c].astype("Int64")
        return df

    def cati_export(self):
        W = self.W
        rng = np.random.default_rng(P.SEED + 11)
        interviewers = ["INT%03d" % k for k in rng.choice(np.arange(101, 190), 46, replace=False)]
        rows = []
        evs = sorted((e for e in self.events if e["system"] == "cati"), key=lambda e: e["utc"])
        sexmap = {1: "M", 2: "F", 3: "X"}
        for e in evs:
            end = e["utc"].astimezone(MT)
            dur = float(np.clip(rng.normal(24, 5), 13, 48))
            if e["status"] == "partial":
                dur = dur * e["section"] / 7.0
            start = end - dt.timedelta(minutes=dur)
            fmt = lambda t: t.strftime("%Y-%m-%d %H:%M:%S")
            r = dict(CASE_ID="C%s" % self.address_id[e["i"]][2:],
                     ADDRESS_ID=self.address_id[e["i"]], INTERVIEWER=str(rng.choice(interviewers)),
                     START_TIME=fmt(start), END_TIME=fmt(end), RESULT="C" if e["status"] == "complete" else "P")
            for it in ITEMS:
                r[it] = e["a"][it]
            a = e["a"]
            r.update(AGE=a["age"], SEX=sexmap.get(a["sex"]) if a["sex"] is not None else None, QUAL=a["qual"],
                     EMP=a["emp"], TENURE=a["tenure"], HHSIZE=a["hhsize"])
            rows.append(r)
        df = pd.DataFrame(rows)
        for c in ITEMS + ["AGE", "QUAL", "EMP", "TENURE", "HHSIZE"]:
            df[c] = df[c].astype("Int64")
        return df

    def call_log(self):
        """the CATI system's call records: every attempt on an address the system called, in Halvreth clock time; the
        system logged nothing while it was down"""
        W = self.W
        rng = np.random.default_rng(P.SEED + 12)
        by = {}
        for e in self.events:
            by.setdefault(e["i"], []).append(e)
        rows = []
        for i in range(self.n):
            q = W.quarter[i]
            evs = sorted(by.get(i, []), key=lambda e: e["utc"])
            mail = self.mailed[i]
            start = mail + dt.timedelta(days=3 if not W.letter_a[i] else 15)
            first_web = next((e for e in evs if e["system"] == "web"), None)
            if first_web is not None and first_web["utc"].astimezone(MT).date() < start:
                continue
            if not W.eligible[i] and rng.random() < 0.55:
                continue
            end = P.Q_END[P.QUARTERS[q]]
            cati = next((e for e in evs if e["system"] == "cati"), None)
            if cati is not None:
                final_t = cati["utc"].astimezone(MT) - dt.timedelta(minutes=float(rng.uniform(14, 40)))
                k = int(min(8, rng.geometric(0.38)))
                final = "IC" if cati["status"] == "complete" else "IP"
            else:
                final_t, final = None, None
                k = int(min(8, rng.geometric(0.34) + 1))
            if start > end:
                continue
            span = max(1, (end - start).days if final_t is None else (final_t.date() - start).days)
            days = sorted(int(x) for x in rng.integers(0, span + 1, k - (final is not None)))
            for n_, d in enumerate(days):
                t = _cati_time(rng, start + dt.timedelta(days=d))
                if final_t is not None and t >= final_t:
                    continue
                if in_outage(t) or t.date() > end:
                    continue
                res = str(rng.choice(["NA", "BZ", "AM", "AP", "CB"], p=[0.55, 0.06, 0.25, 0.07, 0.07]))
                rows.append((self.address_id[i], t, res))
            if final is not None:
                rows.append((self.address_id[i], final_t, final))
            elif rng.random() < 0.3:
                t = _cati_time(rng, start + dt.timedelta(days=int(rng.integers(0, span + 1))))
                if not in_outage(t) and t.date() <= end:
                    rows.append((self.address_id[i], t, str(rng.choice(["RF", "WN"], p=[0.8, 0.2]))))
        df = pd.DataFrame(rows, columns=["ADDRESS_ID", "t", "RESULT"]).sort_values(["ADDRESS_ID", "t"])
        df["ATTEMPT"] = df.groupby("ADDRESS_ID").cumcount() + 1
        df["CALL_TIME"] = df["t"].map(lambda t: t.strftime("%Y-%m-%d %H:%M:%S"))
        df["CASE_ID"] = "C" + df["ADDRESS_ID"].str[2:]
        return df.sort_values(["t", "CASE_ID"])[["CASE_ID", "ATTEMPT", "CALL_TIME", "RESULT"]].reset_index(drop=True)

    def published(self):
        """the tracker's published quarterly estimates, 2019 to the second quarter of 2027, under the
        telephone-first design (the second quarter of 2027 from the telephone-first half of the test)"""
        rng = np.random.default_rng(P.SEED + 13)
        quarters = ["%dQ%d" % (y, k) for y in range(2019, 2028) for k in range(1, 5)][:34]
        level = {"LS": 7.62, "WW": 7.94, "HY": 7.51, "AX": 3.07, "LN": 6.8, "TR": 54.1, "SF": 69.2, "GH": 73.6,
                 "SM": 12.9, "BD": 17.4, "VL": 39.8, "FS": 15.2}
        trend = {"LS": -0.004, "WW": -0.002, "HY": -0.003, "AX": 0.006, "LN": 0.05, "TR": -0.08, "SF": -0.05,
                 "GH": -0.06, "SM": -0.11, "BD": -0.05, "VL": -0.10, "FS": 0.07}
        covid = {"LS": -0.30, "WW": -0.12, "HY": -0.25, "AX": 0.45, "LN": 2.4, "TR": 1.2, "SF": 1.0, "GH": 0.8,
                 "SM": -0.3, "BD": -1.9, "VL": -6.5, "FS": 1.6}
        # the second quarter of 2027 was released from the letter B half of the test: anchor the series' last quarter on
        # those completes, the release's calibration weights moving each estimate a little
        W = self.W
        b2 = W.complete & ~W.letter_a & (W.quarter == 0)
        last = {}
        for code, name, item, kind, tol, th in P.INDEXES:
            v = np.where(W.web[b2], W.ans[code][1][b2], W.ans[code][0][b2]).astype(float)
            last[code] = v.mean() if kind == "score" else 100 * v.mean()
        for code in level:
            level[code] = last[code] - trend[code] * 33
        rows = []
        for k, qq in enumerate(quarters):
            web = 7.9 + 0.33 * k + rng.normal(0, 0.6)
            comp = int(rng.normal(19300, 420))
            if qq == "2027Q2":
                web, comp = 100 * W.web[b2].mean(), int(b2.sum())
            shock = 1.0 if qq in ("2020Q2", "2020Q3") else (0.5 if qq in ("2020Q4", "2021Q3", "2021Q4") else 0.0)
            pub = (dt.date(int(qq[:4]), 3 * int(qq[-1]), 1) + dt.timedelta(days=75)).isoformat()
            for code, name, item, kind, tol, th in P.INDEXES:
                v = level[code] + trend[code] * k + covid[code] * shock
                if kind == "score":
                    v += rng.normal(0, 0.025)
                    moe = 1.96 * 2.0 / np.sqrt(comp) * 1.25
                    rows.append((qq, code, name, "%.2f" % v, "%.2f" % moe, comp, "%.1f" % web, pub))
                else:
                    v += rng.normal(0, 0.35)
                    moe = 1.96 * np.sqrt(v * (100 - v) / comp) * 1.25
                    rows.append((qq, code, name, "%.1f" % v, "%.1f" % moe, comp, "%.1f" % web, pub))
        return pd.DataFrame(rows, columns=["quarter", "index_code", "index_name", "estimate", "margin_of_error_95",
                                           "completes", "web_share_pct", "released"])

    def regions(self):
        rows = []
        hh = {1: 612400, 2: 371900, 3: 336800, 4: 274100, 5: 236500, 6: 139300}
        for code, name, share in P.REGIONS:
            rows.append((code, name, hh[code], int(round(hh[code] * 1.93, -2))))
        return pd.DataFrame(rows, columns=["region_code", "region_name", "households_2027", "adults_2027"])
