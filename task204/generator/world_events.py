"""The clean truth of Carvale's occurrences: the four offender groups behind the 2026 rise, background phone
offences in both windows, every other occurrence the RMS extract carries, the transit officers' log and the
fare-gate counts. Nothing here is written to disk (pack.py does that)."""
import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

import params as P
import world_net as N

TZL = ZoneInfo(P.TZ)
UTC = ZoneInfo("UTC")


def to_utc(t):
    return t.replace(tzinfo=TZL).astimezone(UTC).replace(tzinfo=None)


def dates(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def at(d, sec):
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(seconds=int(sec))


def stop_dep(trip, code):
    for s, arr, dep in trip["stops"]:
        if s == code:
            return dep
    return None


SCHOOL_BREAK_26 = (dt.date(2026, 3, 30), dt.date(2026, 4, 3))


NO_SCHOOL_26 = {dt.date(2026, 2, 26), dt.date(2026, 2, 27)}


def school_day(d):
    return (d.weekday() < 5 and d not in P.HOLIDAYS and d not in NO_SCHOOL_26
            and not (SCHOOL_BREAK_26[0] <= d <= SCHOOL_BREAK_26[1]))


class Events:
    def __init__(self, trips):
        self.rng = np.random.default_rng(P.SEED + 7)
        self.trips = trips
        self.tidx = N.index_trips(trips)
        self.events = []          # every phone offence (groups and background), dicts
        self.g1_runs = []

    # ---- helpers ----------------------------------------------------------------------------------
    def inbound_el(self, d):
        return [t for t in N.trips_on(self.tidx, d) if t["line"] == "EL" and t["direction"] == 1]

    def add(self, **kw):
        kw.setdefault("tpo", None)
        self.events.append(kw)
        return kw

    def report_time(self, ev_time):
        return ev_time + dt.timedelta(seconds=int(self.rng.integers(-40, 41)))

    # ---- group G1: rides the Eastline inbound and snatches as the doors close ---------------------
    def make_g1(self):
        r = self.rng
        cands = [d for d in dates(*P.W26) if d.weekday() in (1, 3, 4) and d not in P.HOLIDAYS]
        while True:
            pick = sorted(r.choice(len(cands), size=P.GROUPS["G1"]["n_runs"], replace=False))
            ds = [cands[i] for i in pick]
            if max((b - a).days for a, b in zip(ds, ds[1:])) <= 10:
                break
        g1_st = P.GROUPS["G1"]["stations"]           # inbound order RV, AR, MB, UY
        patterns = []
        for i in range(len(pick)):
            k = 3 if r.random() < 0.42 else 2
            patterns.append(sorted(r.choice(4, size=k, replace=False)))
        # every station appears in at least six runs
        for s in range(4):
            while sum(s in p for p in patterns) < 6:
                j = int(r.integers(0, len(patterns)))
                if s not in patterns[j] and len(patterns[j]) < 3:
                    patterns[j] = sorted(patterns[j] + [s])
        for d_i, pat in zip(pick, patterns):
            d = cands[d_i]
            trips = [t for t in self.inbound_el(d)
                     if stop_dep(t, "PG") is not None and 16 * 3600 + 35 * 60 <= stop_dep(t, "PG") <= 18 * 3600 + 10 * 60]
            trip = trips[int(r.integers(0, len(trips)))]
            run = {"date": d, "trip_id": trip["trip_id"], "events": []}
            for s_i in pat:
                code = g1_st[s_i]
                dep = at(d, stop_dep(trip, code))
                ev = dep + dt.timedelta(seconds=int(r.integers(0, 46)))
                e = self.add(group="G1", date=d, station=code, t_event=ev, t_occ=self.report_time(ev),
                             x=N.STN[code]["x"] + float(r.normal(0, 18)), y=N.STN[code]["y"] + float(r.normal(0, 18)),
                             mo="SNATCH", suspects=int(r.choice([2, 3], p=[0.55, 0.45])),
                             age_low=int(r.integers(17, 21)), age_high=int(r.integers(22, 27)), sex="M",
                             weapon="NONE", offence="ROB-PERS" if r.random() < 0.3 else "THFT-PERS",
                             loc="LRT PLATFORM", trip_id=trip["trip_id"])
                run["events"].append(e)
            self.g1_runs.append(run)

    def g1_passing(self, d, code):
        """Departure times at a station of the trips G1 rode on date d."""
        out = []
        for run in self.g1_runs:
            if run["date"] == d:
                trip = next(t for t in self.trips if t["trip_id"] == run["trip_id"])
                out.append(at(d, stop_dep(trip, code)))
        return out

    def clear_of_trips(self, d, code, t, margin_min):
        for p in self.g1_passing(d, code):
            if abs((t - p).total_seconds()) < margin_min * 60:
                return False
        return self.clear_of_runs(d, code, t)

    def clear_of_runs(self, d, code, t, tol_min=5.5):
        """No train (either direction) leaving `code` near t also leaves a G1 station near a G1 offence that day."""
        g1 = [e for e in self.events if e["group"] == "G1" and e["date"] == d]
        if not g1:
            return True
        for tr in N.trips_on(self.tidx, d):
            if tr["line"] != "EL":
                continue
            dep = stop_dep(tr, code)
            if dep is None or abs((at(d, dep) - t).total_seconds()) > tol_min * 60:
                continue
            for e in g1:
                if e["station"] == code:
                    continue
                d2 = stop_dep(tr, e["station"])
                if d2 is not None and abs((at(d, d2) - e["t_occ"]).total_seconds()) <= tol_min * 60:
                    return False
        return True

    # ---- group G2: Cobb Street evenings ------------------------------------------------------------
    def make_g2(self):
        r = self.rng
        n = P.GROUPS["G2"]["n"]
        made = 0
        # six evenings where a G1 run struck at Union Yards: G2 strikes at Cobb Street within three minutes of it
        uy_runs = [run for run in self.g1_runs if any(e["station"] == "UY" for e in run["events"])]
        sim = [uy_runs[i] for i in sorted(r.choice(len(uy_runs), size=min(6, len(uy_runs)), replace=False))]
        for run in sim:
            uy = next(e for e in run["events"] if e["station"] == "UY")
            ok = False
            for _ in range(400):
                ev = uy["t_event"] + dt.timedelta(seconds=int(r.integers(-95, 96)))
                if self.clear_of_trips(run["date"], "CB", ev, 6):
                    ok = True
                    break
            if not ok:
                continue
            self._g2(run["date"], ev)
            made += 1
        cands = [d for d in dates(*P.W26) if d.weekday() < 6 and d not in P.HOLIDAYS]
        while made < n:
            d = cands[int(r.integers(0, len(cands)))]
            ev = at(d, int(r.integers(16 * 3600 + 30 * 60, 20 * 3600 + 15 * 60)))
            if not self.clear_of_trips(d, "CB", ev, 9):
                continue
            if any(e["group"] == "G2" and e["date"] == d for e in self.events):
                continue
            self._g2(d, ev)
            made += 1

    def _g2(self, d, ev):
        r = self.rng
        self.add(group="G2", date=d, station="CB", t_event=ev, t_occ=self.report_time(ev),
                 x=N.STN["CB"]["x"] + float(r.normal(0, 18)), y=N.STN["CB"]["y"] + float(r.normal(0, 18)),
                 mo="SNATCH", suspects=int(r.choice([2, 3], p=[0.6, 0.4])), age_low=int(r.integers(16, 20)),
                 age_high=int(r.integers(21, 25)), sex="M", weapon="NONE",
                 offence="ROB-PERS" if r.random() < 0.25 else "THFT-PERS", loc="LRT PLATFORM", trip_id=None)

    # ---- group G3: Hollin after school -------------------------------------------------------------
    def make_g3(self):
        r = self.rng
        cands = [d for d in dates(*P.W26) if school_day(d)]
        while True:
            pick = sorted(r.choice(len(cands), size=P.GROUPS["G3"]["n"], replace=False))
            ds = [cands[i] for i in pick]
            if max((b - a).days for a, b in zip(ds, ds[1:])) <= 12:
                break
        for i in pick:
            d = cands[i]
            ev = at(d, int(r.integers(15 * 3600 + 15 * 60, 17 * 3600 + 45 * 60)))
            self.add(group="G3", date=d, station="HL", t_event=ev, t_occ=self.report_time(ev),
                     x=N.STN["HL"]["x"] + float(r.normal(0, 25)), y=N.STN["HL"]["y"] + float(r.normal(0, 25)),
                     mo="SNATCH", suspects=int(r.choice([2, 3, 4], p=[0.4, 0.4, 0.2])), age_low=int(r.integers(13, 15)),
                     age_high=int(r.integers(15, 17)), sex="M", weapon="NONE",
                     offence="ROB-PERS" if r.random() < 0.35 else "THFT-PERS", loc="LRT PLATFORM", trip_id=None)

    # ---- group G4: university corridor, late night -------------------------------------------------
    def make_g4(self):
        r = self.rng
        cands = [d for d in dates(*P.W26) if d.weekday() in (3, 4, 5)]
        while True:
            pick = sorted(r.choice(len(cands), size=P.GROUPS["G4"]["n"], replace=False))
            ds = [cands[i] for i in pick]
            if max((b - a).days for a, b in zip(ds, ds[1:])) <= 10:
                break
        cx, cy = P.UNIVERSITY
        for i in pick:
            d = cands[i]
            sec = int(r.integers(22 * 3600 + 30 * 60, 25 * 3600 + 45 * 60))
            ev = at(d, sec)
            ang = r.uniform(0, 2 * np.pi)
            rad = 230 * np.sqrt(r.uniform(0, 1))
            self.add(group="G4", date=ev.date(), station=None, t_event=ev, t_occ=self.report_time(ev),
                     x=cx + rad * np.cos(ang), y=cy + rad * np.sin(ang), mo="STREET-WEAPON",
                     suspects=2, age_low=int(r.integers(19, 23)),
                     age_high=int(r.integers(25, 31)), sex="M", weapon="KNIFE", offence="ROB-PERS",
                     loc="STREET", trip_id=None)

    # ---- background phone robberies and snatches (lone offenders mostly) -----------------------------
    def make_background(self):
        r = self.rng
        stations_by_d = {}
        for code, st in N.STN.items():
            d26 = N.district_of(st["x"], st["y"], P.D26)
            stations_by_d.setdefault(d26, []).append(code)
        hours = np.array([0.9, 0.6, 0.4, 0.25, 0.2, 0.3, 0.6, 1.0, 1.2, 1.1, 1.1, 1.3, 1.5, 1.5, 1.6, 1.8, 2.0,
                          2.1, 2.0, 1.8, 1.6, 1.5, 1.3, 1.1])
        hours = hours / hours.sum()
        group_spots = [(N.STN[c]["x"], N.STN[c]["y"]) for c in ("RV", "AR", "MB", "UY", "CB", "HL")] + [P.UNIVERSITY]
        for (a, b), year in ((P.X25, 2025), (P.X26, 2026)):
            for d in dates(a, b):
                for dist, rate in sorted(P.BG_RATE.items()):
                    k = int(r.poisson(rate))
                    for _ in range(k):
                        at_station = (r.random() < 0.27) and dist in stations_by_d
                        h = int(r.choice(24, p=hours))
                        t = dt.datetime(d.year, d.month, d.day, h, int(r.integers(0, 60)), int(r.integers(0, 60)))
                        if at_station:
                            code = stations_by_d[dist][int(r.integers(0, len(stations_by_d[dist])))]
                            if code == "FG" and d < P.SPRING_CHANGE:
                                code = "MB"          # Fairgrounds opened on 29 March 2026
                            x, y = N.STN[code]["x"] + float(r.normal(0, 22)), N.STN[code]["y"] + float(r.normal(0, 22))
                            if year == 2026 and code in ("RV", "AR", "MB", "UY") and not self.clear_of_trips(d, code, t, 12):
                                continue
                            mo = "SNATCH" if r.random() < 0.72 else "STREET"
                            loc = "LRT PLATFORM"
                        else:
                            code = None
                            rects = P.D26[dist]
                            areas = np.array([(x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in rects], dtype=float)
                            x0, y0, x1, y1 = rects[int(r.choice(len(rects), p=areas / areas.sum()))]
                            x, y = float(r.uniform(x0, x1)), float(r.uniform(y0, y1))
                            u = r.random()
                            mo = "STREET" if u < 0.55 else ("SNATCH" if u < 0.86 else "STREET-WEAPON")
                            loc = "STREET" if r.random() < 0.8 else "COMMERCIAL"
                        sus = 2 if r.random() < 0.13 else 1
                        if sus == 2 and (code is not None or min(N.dist((x, y), g) for g in group_spots) < 1700):
                            sus = 1
                        lo = int(r.integers(14, 36))
                        offence = "THFT-PERS" if (mo == "SNATCH" and r.random() < 0.75) else "ROB-PERS"
                        self.add(group=None, date=t.date(), station=code, t_event=t, t_occ=t, x=x, y=y, mo=mo,
                                 suspects=sus, age_low=lo, age_high=lo + int(r.integers(2, 11)),
                                 sex="M" if r.random() < 0.84 else "F",
                                 weapon="KNIFE" if mo == "STREET-WEAPON" else "NONE", offence=offence, loc=loc,
                                 trip_id=None)

    def make_ontrain(self):
        """Phone thefts on trains, recorded by transit officers at the station where the victim reported."""
        r = self.rng
        codes = sorted(N.STN)
        for (a, b) in (P.X25, P.X26):
            for d in dates(a, b):
                for _ in range(int(r.poisson(P.ONTRAIN_RATE))):
                    code = codes[int(r.integers(0, len(codes)))]
                    if code == "FG" and d < P.SPRING_CHANGE:
                        continue
                    t = dt.datetime(d.year, d.month, d.day, int(r.integers(6, 24)), int(r.integers(0, 60)))
                    if d.year == 2026 and code in ("RV", "AR", "MB", "UY", "CB") and not self.clear_of_trips(d, code, t, 12):
                        continue
                    lo = int(r.integers(15, 40))
                    self.add(group=None, date=d, station=code, t_event=t, t_occ=t,
                             x=N.STN[code]["x"] + float(r.normal(0, 15)), y=N.STN[code]["y"] + float(r.normal(0, 15)),
                             mo="PICKPOCKET", suspects=1, age_low=lo, age_high=lo + int(r.integers(3, 12)),
                             sex="M" if r.random() < 0.7 else "F", weapon="NONE", offence="THFT-PERS",
                             loc="LRT TRAIN", trip_id=None)

    # ---- who recorded each phone offence -------------------------------------------------------------
    def assign_recording(self):
        """Group offences went to the police by 911 and are in the RMS only. A background offence at a station or
        on a train may also sit in the transit officers' log: referred with the file number, referred with the
        number left blank, or never referred (then it is in the transit log only)."""
        r = self.rng
        for e in self.events:
            e["in_rms"] = True
            e["tpo"] = None
            if e["group"] is not None or e["station"] is None:
                continue
            p_tpo = 0.9 if e["loc"] == "LRT TRAIN" else 0.56
            if r.random() >= p_tpo:
                continue
            u = r.random()
            kind = "REF_NUM" if u < 0.6 else ("REF_BLANK" if u < 0.76 else "NOT_REF")
            lag = int(r.integers(2, 16))
            e["tpo"] = {"kind": kind, "t_logged": e["t_event"] + dt.timedelta(minutes=lag)}
            if kind == "NOT_REF":
                e["in_rms"] = False


def make_events(trips):
    ev = Events(trips)
    ev.make_g1()
    ev.make_g2()
    ev.make_g3()
    ev.make_g4()
    ev.make_background()
    ev.make_ontrain()
    ev.assign_recording()
    return ev
