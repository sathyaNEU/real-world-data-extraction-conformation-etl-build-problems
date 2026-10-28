"""task179 day-level truth: identities, supervision episodes with their county segments, bookings with their
clocks, jails, agencies, charges and releases, the Halverton police's violent incidents with every victim, the risk
assessments, the programme referrals and Belvantis's devices. Built from world.World; nothing here is a layout."""
from __future__ import annotations

import datetime as dt
from collections import defaultdict

import numpy as np

import codes as K
import common as C
import names as NM

D = dt.date
TD = dt.timedelta


def _day_in(r, lo, hi):
    n = (hi - lo).days
    return lo + TD(days=int(r.integers(0, n + 1))) if n > 0 else lo


_HOURS = {"arrest": np.array([5, 4, 3, 2, 2, 1, 1, 2, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6], float),
          "incident": np.array([7, 6, 5, 4, 3, 2, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 5, 5, 6, 6, 7, 7, 7, 7], float),
          "office": np.array([1, 1, 1, 1, 1, 1, 2, 3, 6, 9, 10, 10, 9, 8, 8, 8, 7, 5, 3, 2, 1, 1, 1, 1], float)}
for _k in _HOURS:
    _HOURS[_k] = _HOURS[_k] / _HOURS[_k].sum()


_CDF = {k: np.cumsum(v) for k, v in _HOURS.items()}


def _hour(r, kind):
    u = r.random(3)
    h = int(np.searchsorted(_CDF.get(kind, _CDF["office"]), u[0] * 0.999999))
    return h, int(u[1] * 60), int(u[2] * 60)


def _pick(r, items, cdf):
    return items[int(np.searchsorted(cdf, r.random() * cdf[-1]))]


_WEAPONS = {"13A": (["KNIFE/CUTTING", "BLUNT OBJECT", "HANDS/FEET", "OTHER"], np.cumsum([0.35, 0.25, 0.3, 0.1])),
            "13A-F": (["FIREARM"], np.array([1.0])), "13B": (["HANDS/FEET", "NONE"], np.cumsum([0.85, 0.15])),
            "120": (["FIREARM", "KNIFE/CUTTING", "HANDS/FEET", "NONE"], np.cumsum([0.45, 0.15, 0.3, 0.1])),
            "09A": (["FIREARM", "KNIFE/CUTTING", "OTHER"], np.cumsum([0.75, 0.15, 0.1])),
            "11A": (["HANDS/FEET", "NONE"], np.cumsum([0.7, 0.3])), "100": (["FIREARM", "NONE", "OTHER"], np.cumsum([1, 1, 1.0])),
            "13C": (["NONE"], np.array([1.0])), "520": (["FIREARM"], np.array([1.0]))}


def norm_key(last, first, dob):
    """the cleaned surname, given name and birth date a person is matched on"""
    import re
    ln = re.sub(r"\b(JR|SR|II|III|IV)\b\.?", " ", last.upper())
    ln = re.sub(r"[^A-Z]", "", ln)
    fn = re.sub(r"[^A-Z]", "", first.upper())
    return ln, fn, dob


class Events:
    def __init__(self, w):
        self.w = w
        self.r_id = C.stream("ids")
        self.r_name = C.stream("names")
        self.r_ep = C.stream("episodes")
        self.r_bk = C.stream("bookings")
        self.r_hpd = C.stream("hpd")
        self.r_gps = C.stream("gps")
        self.r_as = C.stream("assess")
        self.r_pg = C.stream("programs")
        self._identities()
        self._episodes()
        self._bookings()
        self._incidents()
        self._assessments()
        self._programs()
        self._gps()

    # ------------------------------------------------------------------ identities
    def _identities(self):
        w, r = self.w, self.r_id
        n = w.N
        ids = r.choice(np.arange(1_200_000, 9_900_000), size=n, replace=False)
        self.pid = ids
        sid_core = r.choice(np.arange(100_000, 999_999), size=n, replace=False)
        chk = [(sum(int(c) * (i + 2) for i, c in enumerate(str(s))) % 10) for s in sid_core]
        self.sid = np.array(["MR%06d%d" % (s, c) for s, c in zip(sid_core, chk)])
        first, middle, last, suffix = NM.draw_people(self.r_name, w.male, w.hispanic)
        self.first, self.middle, self.last, self.suffix = first, middle, last, suffix
        self.dob = [D.fromisoformat(str(x)) for x in w.dob]
        keys = {}
        for i in range(n):
            k = norm_key(last[i], first[i], self.dob[i])
            while k in keys:
                self.dob[i] = self.dob[i] + TD(days=int(r.integers(1, 40)))
                k = norm_key(last[i], first[i], self.dob[i])
            keys[k] = i
        self.sup_keys = keys
        # legacy numbers for everyone supervised before the cutover; a few people held two
        self.oms = {}
        legacy = [i for i in range(n) if C.month_start(int(w.first_start[i])) < C.MIGRATION]
        nums = r.choice(np.arange(210_000, 689_999), size=len(legacy) + 400, replace=False)
        j = 0
        for i in legacy:
            self.oms[i] = ["%06d" % nums[j]]
            j += 1
        dup = r.choice(legacy, size=min(300, len(legacy)), replace=False)
        for i in dup:
            self.oms[int(i)].append("%06d" % nums[j])
            j += 1
        # residence addresses (Halverton residents) and towns
        self.addr = {}
        for i in range(n):
            if w.city[i]:
                num, st, t, unit = NM.street_address(r)
                self.addr[i] = (num, st, t, unit, "Halverton")
            else:
                towns = NM.TOWNS_DARROW[1:] if w.county0[i] == 0 else NM.TOWNS_KESWICK
                num, st, t, unit = NM.street_address(r)
                self.addr[i] = (num, st, t, unit, towns[r.integers(len(towns))])

    # ------------------------------------------------------------------ episodes
    def _episodes(self):
        """records as the case-management system holds them: one row per episode, a county move closing one
        episode and opening the next, a few people carrying a second concurrent case"""
        w, r = self.w, self.r_ep
        moves = w.move_days
        self.episodes = []
        self.person_eps = defaultdict(list)
        case_seq = {}
        for e in w.spells:
            i = e["p"]
            c0 = int(w.county0[i])
            # the county at the episode start: replay earlier moves
            for (d, a, b) in moves.get(i, []):
                if d < e["start"]:
                    c0 = b
            yr = e["start"].year
            cty = "DC" if c0 == 0 else "KC"
            case_seq.setdefault((cty, yr), 0)
            case_seq[(cty, yr)] += int(r.integers(3, 40))
            case = "%s-%04d-CR-%05d" % (cty, yr - (0 if e["parole"] else int(r.integers(0, 2))), case_seq[(cty, yr)])
            segs = []
            cur = e["start"]
            county = c0
            for (d, a, b) in sorted(moves.get(i, [])):
                if e["start"] < d and (e["end"] is None or d < e["end"]):
                    segs.append((cur, d, county, "TRANSFERRED - COUNTY"))
                    cur = d + TD(days=1)
                    county = b
            segs.append((cur, e["end"], county, e["why"]))
            for k, (a, b, cnty, why) in enumerate(segs):
                rec = dict(p=i, start=a, end=b, county=cnty, why=why, parole=e["parole"], expires=e["expires"],
                           case=case, lead=self._lead(i, e), first_seg=(k == 0), received=(k > 0))
                self.episodes.append(rec)
                self.person_eps[i].append(rec)
        # concurrent second cases
        self.concurrent = []
        for e in list(self.episodes):
            if e["first_seg"] and e["end"] is not None and (e["end"] - e["start"]).days > 200 and r.random() < self.w.p["concurrent"]:
                a = e["start"] + TD(days=int(r.integers(0, 90)))
                b = a + TD(days=int(r.integers(120, max(121, (e["end"] - a).days))))
                b = min(b, e["end"])
                fam = K.BY_FAMILY["PROPERTY" if r.random() < 0.5 else "DRUG"]
                rec = dict(p=e["p"], start=a, end=b, county=e["county"], why="EXPIRED", parole=False, expires=b,
                           case=e["case"][:-5] + "%05d" % int(r.integers(10000, 99999)), lead=fam[r.integers(len(fam))],
                           first_seg=True, received=False, concurrent=True)
                self.episodes.append(rec)
                self.person_eps[e["p"]].append(rec)
                self.concurrent.append(rec)
        for i in self.person_eps:
            self.person_eps[i].sort(key=lambda x: x["start"])

    def _lead(self, i, e):
        return self.w.lead0[i]

    def supervised(self, i, d):
        """the Region 4 episode open for person i on day d, if any (concurrent cases ignored)"""
        for e in self.person_eps.get(i, []):
            if e.get("concurrent"):
                continue
            if e["start"] <= d and (e["end"] is None or d <= e["end"]):
                return e
        return None

    def county_on(self, i, d):
        e = self.supervised(i, d)
        if e is not None:
            return e["county"]
        c = int(self.w.county0[i])
        for (dd, a, b) in self.w.move_days.get(i, []):
            if dd < d:
                c = b
        return c

    # ------------------------------------------------------------------ bookings
    def _bookings(self):
        w, r = self.w, self.r_bk
        self.bookings = []
        spells_by_p = defaultdict(list)
        for s in w.spells:
            spells_by_p[s["p"]].append(s)
        for (i, mi, kind) in sorted(w.book, key=lambda t: (t[1], t[0])):
            sp = None
            for s in spells_by_p[i]:
                if s["sm"] <= mi and (s["em"] >= mi):
                    sp = s
                    break
            if sp is None:
                continue
            lo = max(C.month_start(mi), sp["start"])
            hi = C.month_start(mi + 1) - TD(days=1)
            if sp["end"] is not None:
                hi = min(hi, sp["end"])
            if hi < lo:
                continue
            d = _day_in(r, lo, hi)
            self._add_booking(i, d, kind, r)
        # the state list lags a discharge by up to a week, so a few bookings in the days after one still notify
        for s in w.spells:
            if s["end"] is not None and s["why"] in ("EXPIRED", "DISCHARGED EARLY") and r.random() < 0.004:
                d = s["end"] + TD(days=int(r.integers(1, 8)))
                if d <= C.RECORDS_END:
                    self._add_booking(s["p"], d, "VW" if r.random() < 0.2 else "NC", r, late=True)
        # re-bookings on the same incident, and returns from hospital
        extra = []
        for b in self.bookings:
            if b["type"] == "NEW ARREST" and b["agency"] == "HPD" and b["kind"] == "VW" and b["release"] is not None and r.random() < 0.05:
                d2 = b["release"].date() + TD(days=int(r.integers(3, 26)))
                if self.supervised(b["p"], d2) is not None and d2 <= C.RECORDS_END:
                    nb = self._make(b["p"], d2, "VW", r, agency="HPD", case=b["case"], incident=b["incident"],
                                    charges=self._upgrade(b["charges"], r))
                    nb["rebook_src"] = b
                    extra.append(nb)
            if b["release"] is not None and r.random() < (0.07 if b["kind"] == "VW" else 0.02) and b["kind"] in ("VW", "NC", "PV"):
                d2 = b["release"] + TD(days=int(r.integers(1, 4)), hours=int(r.integers(1, 9)))
                nb = dict(b)
                nb["bid"] = None
                nb["type"] = "RETURN FROM HOSPITAL"
                nb["kind"] = "RH"
                nb["booked"] = d2
                nb["release_reason"] = b["release_reason"]
                hold = b.get("hold_days", 3)
                nb["release"] = d2 + TD(days=int(max(1, hold)), hours=int(r.integers(0, 10)))
                b["release_reason"] = "RELEASED TO HOSPITAL"
                nb["hospital_of"] = b
                extra.append(nb)
        self.bookings += extra
        self.bookings.sort(key=lambda b: b["booked"])
        seq = {}
        for b in self.bookings:
            j = b["jail"]
            y = b["booked"].year
            seq.setdefault((j, y), int(r.integers(100, 900)))
            seq[(j, y)] += int(r.integers(4, 17))
            b["bid"] = ("%02d%06d" % (y % 100, seq[(j, y)])) if j == "D" else ("K%d-%05d" % (y, seq[(j, y)]))
        # co-arrestees: a few Halverton police incidents behind two supervisees' Category V arrests
        hpd_vw = [b for b in self.bookings if b["type"] == "NEW ARREST" and b["agency"] == "HPD" and b["kind"] == "VW"
                  and "rebook_src" not in b and isinstance(b.get("incident"), tuple)]
        bym = defaultdict(list)
        for b in hpd_vw:
            bym[(b["booked"].year, b["booked"].month)].append(b)
        for key, lst in bym.items():
            if len(lst) < 2:
                continue
            k = int(len(lst) * 0.05 + r.random())
            pick = r.choice(len(lst), size=min(len(lst) // 2 * 2, 2 * k), replace=False)
            for a, bb in zip(pick[0::2], pick[1::2]):
                A, B = lst[a], lst[bb]
                if A["p"] != B["p"]:
                    B["incident"] = A["incident"]
                    B["case"] = A["case"]
                    B["co_of"] = A

    def _upgrade(self, charges, r):
        out = list(charges)
        add = K.SCHEDULE_B[r.integers(len(K.SCHEDULE_B))]
        if add not in out:
            out.append(add)
        return out

    def _add_booking(self, i, d, kind, r, late=False):
        b = self._make(i, d, kind, r)
        b["late_notice"] = late
        self.bookings.append(b)

    def _make(self, i, d, kind, r, agency=None, case=None, incident=None, charges=None):
        w = self.w
        cty = self.county_on(i, d)
        city = bool(w.city[i]) and cty == 0
        if agency is None:
            u = r.random()
            if city:
                agency = "HPD" if u < 0.86 else ("DCSO" if u < 0.90 else "MSP")
            elif cty == 0:
                agency = "DCSO" if u < 0.80 else "MSP"
            else:
                agency = "KCSO" if u < 0.86 else "MSP"
        jail = "D" if cty == 0 else "K"
        if agency == "HPD":
            jail = "K" if r.random() < (0.13 if d.year >= 2025 else 0.04) else "D"
        h, m, s = _hour(r, "arrest")
        booked = dt.datetime(d.year, d.month, d.day, h, m, s)
        if charges is None:
            charges = self._charges(kind, r)
        if kind in ("VW", "NC"):
            typ = "NEW ARREST"
            u = r.random()
            if u < 0.55:
                hold = r.integers(0, 4)
                why = "BONDED" if r.random() < 0.7 else "OWN RECOGNIZANCE"
            elif u < 0.86:
                hold = r.integers(4, 46)
                why = "BONDED" if (r.random() < 0.6 or kind == "VW") else "CHARGES DISMISSED"
            else:
                hold = r.integers(30, 151)
                why = "TRANSFER TO MDOC"
        elif kind == "WT":
            typ = "WARRANT"
            hold = r.integers(1, 15)
            why = "COURT RELEASE"
        else:
            typ = "PROBATION/PAROLE VIOLATION"
            hold = r.integers(2, 36)
            why = "HOLD LIFTED"
        rel = booked + TD(days=int(hold), hours=int(r.integers(1, 20)), minutes=int(r.integers(0, 60)))
        if rel.date() > C.RECORDS_END:
            rel = None
            why = ""
        if case is None:
            case = self._case(agency, d, r)
        b = dict(p=i, booked=booked, release=rel, release_reason=why, kind=kind, type=typ, agency=agency, jail=jail,
                 case=case, charges=charges, incident=incident, hold_days=int(hold), bid=None)
        if agency == "HPD" and incident is None and kind in ("VW", "NC") and self._violent_incident(charges):
            b["incident"] = ("arrest", len(self.bookings), d)
        return b

    def _violent_incident(self, charges):
        return any(K.FAMILY.get(c) in ("VIOLENT", "WEAPON") or c in ("302.01", "302.02", "302.05", "302.20") for c in charges)

    def _case(self, agency, d, r):
        yy = d.year % 100
        if agency == "HPD":
            return ("HPD", yy, None)
        if agency == "DCSO":
            return "DC%02d-%05d" % (yy, int(r.integers(100, 19999)))
        if agency == "KCSO":
            return "K%02d-%04d" % (yy, int(r.integers(10, 9999)))
        return "MSP-%02d-%05d" % (yy, int(r.integers(100, 49999)))

    def _charges(self, kind, r):
        if kind == "VW":
            pool = [("302.10", 14), ("302.11", 16), ("302.12", 5), ("303.01", 8), ("303.02", 6), ("303.04", 2),
                    ("501.02", 20), ("501.04", 12), ("501.06", 4), ("501.10", 3), ("501.08", 2), ("401.02", 3),
                    ("301.05", 1.5), ("301.02", 0.6), ("304.01", 1), ("305.01", 1.2), ("301.04", 0.4)]
        elif kind == "NC":
            pool = [("402.01", 15), ("401.01", 6), ("402.05", 4), ("403.01", 5), ("601.01", 16), ("601.03", 7),
                    ("601.08", 4), ("701.01", 7), ("701.02", 1.5), ("701.05", 6), ("302.02", 7), ("302.05", 6),
                    ("302.01", 3), ("302.20", 2.5), ("302.40", 2), ("801.03", 3), ("403.05", 2), ("405.02", 1),
                    ("405.10", 1), ("501.12", 1), ("701.09", 1.5), ("802.01", 1.5), ("803.04", 0.7), ("306.02", 0.6)]
        elif kind == "WT":
            return ["804.01"]
        else:
            return []
        names = [a for a, _ in pool]
        p = np.array([b for _, b in pool], float)
        p /= p.sum()
        first = names[r.choice(len(names), p=p)]
        out = [first]
        k = r.choice(3, p=[0.55, 0.32, 0.13])
        sec = [("601.01", 5), ("601.08", 3), ("801.03", 3), ("402.01", 2), ("701.05", 2), ("302.02", 1.5), ("501.12", 0.7)]
        sn = [a for a, _ in sec]
        sp = np.array([b for _, b in sec], float)
        sp /= sp.sum()
        for _ in range(k):
            c = sn[r.choice(len(sn), p=sp)]
            if c not in out:
                out.append(c)
        return out

    # ------------------------------------------------------------------ Halverton police incidents
    def _incidents(self):
        """every violent incident the Halverton police recorded in the city, 2018 to 2026, with each victim"""
        from world import TREND, SEASON
        w, r = self.w, self.r_hpd
        self.incidents = []
        # victimizations of supervisees living in Halverton
        sup_v = []
        for (i, mi) in w.vict:
            if mi < C.month_index(C.RECORDS_START) or mi > C.month_index(C.RECORDS_END):
                continue
            if not w.city[i]:
                continue
            lo = C.month_start(mi)
            hi = C.month_start(mi + 1) - TD(days=1)
            d = _day_in(r, lo, hi)
            if self.county_on(i, d) != 0:
                continue
            sup_v.append((i, d))
        self.sup_victimizations = sup_v
        for (i, d) in sup_v:
            off = r.choice(["13A", "13B", "120", "13A-F"], p=[0.40, 0.33, 0.15, 0.12])
            inc = self._new_incident(d, int(self.w.dist[i]), off, r)
            inc["victims"].append(dict(kind="sup", p=i))
            if r.random() < 0.15:
                inc["victims"].append(self._gen_victim(r, d))
            self.incidents.append(inc)
        # supervisees' Halverton police arrests on crimes against persons or weapons
        self.arrest_incidents = {}
        for b in self.bookings:
            if isinstance(b.get("incident"), tuple) and b["incident"][0] == "arrest" and "co_of" not in b and "rebook_src" not in b:
                if not (C.RECORDS_START <= b["booked"].date() <= C.RECORDS_END):
                    continue
                d = max(C.RECORDS_START, (b["booked"] - TD(hours=int(r.integers(0, 30)))).date())
                off = self._nibrs(b["charges"])
                inc = self._new_incident(d, int(self.w.dist[b["p"]]) or int(r.integers(1, 6)), off, r)
                if off == "520":
                    inc["victims"].append(dict(kind="society"))
                elif off == "120" and r.random() < 0.3:
                    inc["victims"].append(dict(kind="business", name=self._business(r)))
                else:
                    for _ in range(int(r.choice([1, 2, 3], p=[0.72, 0.22, 0.06]))):
                        inc["victims"].append(self._gen_victim(r, d))
                    for k in range(1, len(inc["victims"])):
                        if r.random() < 0.65:
                            inc["victims"][k]["household_of"] = 0
                inc["arrest"] = True
                if r.random() < 0.55:
                    inc["supplement"] = True
                    if inc["victims"] and inc["victims"][0].get("kind") == "gen" and r.random() < 0.55:
                        nv = self._gen_victim(r, d)
                        nv["added"] = True
                        if r.random() < 0.5:
                            nv["household_of"] = 0
                        inc["victims"].append(nv)
                self.incidents.append(inc)
                b["incident"] = inc
        for b in self.bookings:
            if "co_of" in b:
                b["incident"] = b["co_of"]["incident"]
        for b in self.bookings:
            if "rebook_src" in b:
                b["incident"] = b["rebook_src"]["incident"]
        for b in self.bookings:
            if isinstance(b.get("incident"), tuple):
                b["incident"] = None
        # everyone else
        for mi in range(C.month_index(C.RECORDS_START), C.month_index(C.RECORDS_END) + 1):
            y, mo = mi // 12, mi % 12 + 1
            for dist in range(1, 6):
                lam = 1050 * [0.28, 0.24, 0.18, 0.17, 0.13][dist - 1] * TREND[y] * SEASON[mo - 1] * (0.965 if y == 2026 else 1.0)
                for _ in range(int(r.poisson(lam * 0.86))):
                    d = _day_in(r, C.month_start(mi), C.month_start(mi + 1) - TD(days=1))
                    off = r.choice(["13A", "13B", "120", "13A-F", "09A", "11A", "100", "13C", "520"],
                                   p=[0.27, 0.40, 0.11, 0.06, 0.006, 0.035, 0.009, 0.07, 0.04])
                    inc = self._new_incident(d, dist, off, r)
                    if off == "520":
                        inc["victims"].append(dict(kind="society"))
                    elif off == "120" and r.random() < 0.32:
                        inc["victims"].append(dict(kind="business", name=self._business(r)))
                    else:
                        for _ in range(int(r.choice([1, 2, 3], p=[0.85, 0.12, 0.03]))):
                            inc["victims"].append(self._gen_victim(r, d))
                        if len(inc["victims"]) >= 2 and r.random() < 0.35:
                            inc["victims"][1]["household_of"] = 0
                    self.incidents.append(inc)
        self.incidents.sort(key=lambda x: (x["report"], x["occurred"]))
        seq = {}
        for inc in self.incidents:
            y = inc["report"].year
            seq.setdefault(y, int(r.integers(200, 900)))
            seq[y] += int(r.integers(2, 9))
            inc["number"] = (y % 100, seq[y])
        taken = defaultdict(set)
        for inc in self.incidents:
            taken[inc["number"][0]].add(inc["number"][1])
        top = {y: max(v) for y, v in taken.items()}
        for b in self.bookings:
            if isinstance(b.get("incident"), dict):
                b["case"] = ("HPD", b["incident"]["number"][0], b["incident"]["number"][1])
            elif isinstance(b["case"], tuple):
                yy = b["booked"].year % 100
                while True:
                    n = int(r.integers(150, top.get(yy, 90000)))
                    if n not in taken[yy]:
                        break
                taken[yy].add(n)
                b["case"] = ("HPD", yy, n)
                b["case_unlisted"] = True

    def _nibrs(self, charges):
        fams = [c for c in charges if K.FAMILY.get(c) in ("VIOLENT", "WEAPON")]
        c = fams[0] if fams else charges[0]
        if c in ("301.01", "301.02", "301.04"):
            return "09A"
        if c in ("301.05", "302.10", "302.11", "302.12", "501.10"):
            return "13A"
        if c in ("303.01", "303.02", "303.04"):
            return "120"
        if c in ("304.01", "304.02"):
            return "100"
        if c == "305.01":
            return "11A"
        if c in ("501.02", "501.04", "501.06", "501.08"):
            return "520"
        if c == "302.20":
            return "13C"
        return "13B"

    def _new_incident(self, d, dist, off, r):
        h, m, s = _hour(r, "incident")
        occ = dt.datetime(d.year, d.month, d.day, h, m)
        lag = 0 if r.random() < 0.8 else int(r.integers(1, 9))
        rep = occ.date() + TD(days=lag)
        if rep > C.RECORDS_END:
            rep = C.RECORDS_END
        offs = [off]
        if off in ("13A", "13A-F", "120") and r.random() < 0.12:
            offs.append("520" if off != "120" else "13A")
        weapon = _pick(r, *_WEAPONS[off])
        return dict(occurred=occ, report=rep, dist=dist, offenses=offs, weapon=weapon, victims=[],
                    supplement=(r.random() < 0.06), beat=int(r.integers(1, 7)))

    def _business(self, r):
        names = ["QUIK STOP #%d" % int(r.integers(2, 40)), "SUNRISE FUEL", "MERCER LIQUORS", "DOLLAR DEPOT #%d" % int(r.integers(1, 9)),
                 "HOLLIS PHARMACY", "PELL CREDIT UNION", "BIG RIVER CELLULAR", "NORTHFIELD MARKET", "EASTGATE PAWN",
                 "HARMON AVE LAUNDROMAT", "ORCHARD DELI"]
        return names[r.integers(len(names))]

    def _gen_victim(self, r, d):
        if not getattr(self, "_vbuf", None):
            n = 6000
            male = r.random(n) < 0.58
            hisp = r.random(n) < 0.14
            f, m, l, s = NM.draw_people(r, male, hisp)
            age = np.clip(r.gamma(2.6, 11.0, n) + 5, 1, 92).astype(int)
            off = r.integers(0, 365, n)
            race = np.where(hisp, "W", np.where(r.random(n) < 0.5, "W", np.where(r.random(n) < 0.75, "B", "A")))
            cu = r.random(n)
            towns = r.integers(0, len(NM.OTHER_TOWNS), n)
            self._vbuf = [dict(first=f[k], middle=m[k], last=l[k], suffix=s[k], male=bool(male[k]), hisp=bool(hisp[k]),
                               age_=int(age[k]), off=int(off[k]), race=str(race[k]), cu=float(cu[k]), town=int(towns[k]))
                          for k in range(n)]
            self._vbuf.reverse()
        v = self._vbuf.pop()
        dob = d - TD(days=int(v["age_"] * 365.25 + v["off"]))
        key = norm_key(v["last"], v["first"], dob)
        while key in self.sup_keys:
            dob = dob + TD(days=int(r.integers(1, 60)))
            key = norm_key(v["last"], v["first"], dob)
        num, st, t, unit = NM.street_address(r)
        u = v["cu"]
        city = "HALVERTON" if u < 0.78 else (NM.OTHER_TOWNS[v["town"]].upper() if u < 0.96 else "")
        return dict(kind="gen", first=v["first"], middle=v["middle"], last=v["last"], suffix=v["suffix"], dob=dob,
                    age=(d - dob).days // 365, male=v["male"], race=v["race"], hisp=v["hisp"], addr=(num, st, t, unit),
                    city=city)

    # ------------------------------------------------------------------ assessments
    def _assessments(self):
        w, r = self.w, self.r_as
        self.assessments = []
        bk_by_p = defaultdict(list)
        for b in self.bookings:
            if b["kind"] in ("VW", "NC"):
                bk_by_p[b["p"]].append(b["booked"].date())
        for e in self.episodes:
            if not e["first_seg"] or e.get("concurrent"):
                continue
            i = e["p"]
            end = e["end"] or D(2027, 1, 8)
            d = e["start"] + TD(days=int(r.integers(8, 46)))
            dates = []
            while d < end and d <= D(2026, 12, 31):
                dates.append(d)
                d = d + TD(days=int(r.integers(300, 421)))
            for bd in bk_by_p.get(i, []):
                if e["start"] <= bd < end and r.random() < 0.3:
                    dd = bd + TD(days=int(r.integers(15, 61)))
                    if dd < end and dd <= D(2026, 12, 31):
                        dates.append(dd)
            for dd in sorted(set(dates)):
                if dd < D(2017, 1, 1):
                    continue
                self.assessments.append(self._score(i, dd, r))

    def _score(self, i, d, r):
        w = self.w
        mi = C.month_index(d)
        age = w.age0[i] + (mi - w.first_start[i]) / 12.0
        from world import OFF_O
        lat = w.frail[i] + 0.28 * np.log1p(w.priors[i]) + 0.5 * w.male[i] - 0.03 * (age - 30) + OFF_O[w.fam[i]]
        base = 17.0 + 4.2 * lat + r.normal(0, 2.4)
        v2 = d >= C.INSTRUMENT_V2
        if v2:
            tot = int(np.clip(round(base + r.normal(0, 0.8)), 0, 38))
            caps = [10, 5, 3, 2, 6, 6, 6]
        else:
            tot = int(np.clip(round(base), 0, 38))
            caps = [8, 6, 4, 3, 6, 5, 6]
        wts = np.array(caps, float) * (1 + r.normal(0, 0.25, 7)).clip(0.2)
        parts = np.floor(tot * wts / wts.sum()).astype(int)
        parts = np.minimum(parts, caps)
        k = 0
        while parts.sum() < tot and k < 200:
            j = int(r.integers(7))
            if parts[j] < caps[j]:
                parts[j] += 1
            k += 1
        tot = int(parts.sum())
        return dict(p=i, date=d, v2=v2, parts=[int(x) for x in parts], total=tot)

    # ------------------------------------------------------------------ programme referrals (distractor)
    def _programs(self):
        w, r = self.w, self.r_pg
        self.referrals = []
        for e in self.episodes:
            if not e["first_seg"] or e.get("concurrent"):
                continue
            end = e["end"] or D(2026, 12, 31)
            if end < C.RECORDS_START:
                continue
            k = r.poisson(0.55)
            for _ in range(int(k)):
                lo = max(e["start"], C.RECORDS_START)
                if (end - lo).days < 10:
                    continue
                d = _day_in(r, lo, min(end, C.RECORDS_END))
                prog = r.choice(["T4C", "MRT", "SUD-IOP", "SUD-OP", "EMPLOY", "ANGER MGMT"], p=[0.22, 0.14, 0.18, 0.2, 0.16, 0.1])
                started = r.random() < 0.72
                st = d + TD(days=int(r.integers(5, 60))) if started else None
                outcome, dd = "", None
                if started:
                    pc = 1 / (1 + np.exp(-(0.4 - 0.9 * w.frail[e["p"]])))
                    if st > C.RECORDS_END:
                        st, outcome = None, ""
                    else:
                        dd = st + TD(days=int(r.integers(40, 160)))
                        if dd > C.RECORDS_END:
                            dd, outcome = None, "ACTIVE"
                        else:
                            outcome = "COMPLETED" if r.random() < pc else r.choice(["NON-COMPLIANT", "WITHDRAWN", "ABSCONDED", "OTHER"])
                self.referrals.append(dict(p=e["p"], date=d, prog=prog, start=st, end=dd, outcome=outcome))

    # ------------------------------------------------------------------ Belvantis devices
    def _gps(self):
        w, r = self.w, self.r_gps
        self.enrolments = []
        bk_by_p = defaultdict(list)
        for b in self.bookings:
            bk_by_p[b["p"]].append(b)
        cand_w = {}
        for e in self.episodes:
            if not e["first_seg"] or e.get("concurrent"):
                continue
            lead = e["lead"]
            wt = 1.0
            if lead in ("305.01", "305.04", "803.04"):
                wt = 7.0
            elif lead in ("302.05", "302.12", "302.40"):
                wt = 4.0
            if w.frail[e["p"]] > 0.6:
                wt *= 2.0
            cand_w[(e["p"], e["start"])] = (e, wt)
        start_m = C.month_index(D(2024, 3, 1))
        used = set()
        cands = [(e, wt) for (e, wt) in cand_w.values() if e["end"] is None or e["end"] >= D(2024, 3, 1)]
        cs = np.array([e["start"].toordinal() for e, _ in cands])
        ce = np.array([(e["end"] or D(2099, 1, 1)).toordinal() for e, _ in cands])
        cw = np.array([wt for _, wt in cands])
        cp = np.array([e["p"] for e, _ in cands])
        taken = np.zeros(len(cands), bool)
        for mi in range(start_m, C.month_index(C.RECORDS_END) + 1):
            ms = C.month_start(mi)
            me = C.month_start(mi + 1) - TD(days=1)
            ok = np.where((cs <= ms.toordinal()) & (ce > me.toordinal()) & ~taken)[0]
            if len(ok) == 0:
                continue
            pw = cw[ok] / cw[ok].sum()
            k = int(r.poisson(25))
            pick = ok[r.choice(len(ok), size=min(k, len(ok)), replace=False, p=pw)]
            for j in pick:
                e, _ = cands[j]
                taken |= (cp == e["p"])
                i = e["p"]
                used.add(i)
                s = _day_in(r, ms, me)
                plan = s + TD(days=int(r.integers(120, 541)))
                end = plan
                why = "TERM COMPLETE"
                ep_end = self._region4_end(i, s)
                if ep_end is not None and ep_end[0] < end:
                    end, why = ep_end
                self.enrolments.append(dict(p=i, start=s, end=end, why=why, plan=plan))
        # events
        self.gps_events = []
        for en in self.enrolments:
            self._gps_events(en, bk_by_p.get(en["p"], []), r)

    def _region4_end(self, i, d):
        """the day Region 4's supervision of person i ends after day d, with its reason"""
        e = self.supervised(i, d)
        if e is None:
            return None
        cur = e
        while True:
            if cur["end"] is None:
                return None
            if cur["why"] == "TRANSFERRED - COUNTY":
                nxt = [x for x in self.person_eps[i] if x["start"] == cur["end"] + TD(days=1) and not x.get("concurrent")]
                if nxt:
                    cur = nxt[0]
                    continue
            return cur["end"], cur["why"]

    def _gps_events(self, en, books, r):
        ser = lambda: "BV%07d" % int(r.integers(1_000_000, 9_999_999))
        ev = []
        dev = ser()
        ev.append(dict(t="ENROL", d=en["start"], dev=dev))
        d = en["start"]
        end = en["end"]
        while True:
            d = d + TD(days=int(r.exponential(900)) + 1)
            if d >= end or d > C.RECORDS_END:
                break
            new = ser()
            ev.append(dict(t="DEVICE_RETURN", d=d, dev=dev, note=r.choice(["battery fault", "strap damage", "no GPS fix", "tamper alert", "charger fault"])))
            ev.append(dict(t="DEVICE_ISSUE", d=d, dev=new))
            dev = new
        for b in books:
            bd = b["booked"].date()
            if en["start"] <= bd <= end and bd <= C.RECORDS_END:
                if r.random() < 0.55:
                    ev.append(dict(t="SUSPEND", d=bd, dev=None, note="client in custody"))
                    if b["release"] is not None and b["release"].date() < end:
                        ev.append(dict(t="RESUME", d=b["release"].date(), dev=None))
        if en["why"] == "TRANSFER OUT" and end <= C.RECORDS_END:
            lag = int(r.integers(10, 46))
            ev.append(dict(t="ACCOUNT_TRANSFER", d=end + TD(days=lag), dev=None, note="moved to receiving region account"))
        elif end <= C.RECORDS_END:
            ev.append(dict(t="END", d=end, dev=dev))
        en["events"] = sorted(ev, key=lambda x: (x["d"], ["ENROL", "DEVICE_RETURN", "DEVICE_ISSUE", "SUSPEND", "RESUME", "END", "ACCOUNT_TRANSFER"].index(x["t"])))
