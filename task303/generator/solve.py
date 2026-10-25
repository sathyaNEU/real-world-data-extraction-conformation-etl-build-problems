"""Everything owed, computed from the shipped pack alone: the conversion's figure for each candidate (the golden, the
default every-breaker-ticket path and the family of shared-minute constructions), the storm record (ask A) and the
taps' record (ask B), each with the paths a response that misses its device takes.

    Pack(target_dir) reads the eleven files; nothing here imports the generator's world or records."""
import csv
import datetime as dt
import os
from collections import Counter, defaultdict
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

ET = ZoneInfo("America/New_York")
UTC = dt.timezone.utc
FILES = {"legacy": "oms_interruptions_2019_2022.csv", "current": "oms_interruptions_2023_2025.csv",
         "crews": "storm_crew_status_2023_2025.csv", "meds": "major_event_days_2019_2025.csv",
         "inventory": "feeder_inventory_2026.xlsx", "plan": "storm_hardening_plan_2027.docx"}
CAND = ["F-112", "F-114", "F-205", "F-208", "F-301", "F-303"]
LEG_CAUSE = {"TREE": "Vegetation", "WIND": "Wind", "ANML": "Wildlife", "LTNG": "Lightning",
             "EQUP": "Equipment failure", "VEH": "Vehicle / public", "UNK": "Unknown"}
LEG_DEV = {"CB": "Feeder breaker", "RCL": "Line recloser", "FUS": "Fuse", "TX": "Transformer"}
SUB_CODE = {"PLC": "Pell Creek", "SRH": "Sorrel Hill", "BYM": "Byers Mill", "HLF": "Hollow Fork",
            "KTR": "Kettle Run", "WLC": "Willow Crossing"}
ADDRESSED = ("Vegetation", "Wind", "Wildlife")
BACKBONE = ("Feeder breaker", "Line recloser")
PREVENTED, YEARS_N, INCENTIVE = 0.9, 7, 2.10


def _rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


EST = dt.timezone(dt.timedelta(hours=-5))
DEVICE_STATUS = ("En route", "On site", "Restored", "Released")


def local(day, clock):
    """an aware Eastern time for a date and a legacy clock time (HH:MM)"""
    return dt.datetime.combine(day, dt.datetime.strptime(clock, "%H:%M").time()).replace(tzinfo=ET)


def legacy_start(day, clock, minutes, handheld, mode="golden"):
    """when a legacy ticket began: OUT_DT is the day it began, except on a trouble crew's handheld ticket, which is
    dated the day the crew closed it, so the interruption began on the day that, with its duration, ends on OUT_DT"""
    if mode == "naive" or minutes is None or not (handheld or mode == "all"):
        return local(day, clock)
    for k in range(0, 5):
        st = local(day - dt.timedelta(days=k), clock)
        if (st.astimezone(UTC) + dt.timedelta(minutes=minutes)).astimezone(ET).date() == day:
            return st
    raise ValueError((day, clock, minutes))


def legacy_minutes(raw, mode="golden"):
    """DUR_MIN as each reading takes it: the control room's whole minutes; the handheld's hours.minutes"""
    if "." not in raw:
        return int(raw)
    h, m = raw.split(".")
    if mode == "golden":
        return int(h) * 60 + int(m)
    if mode == "hours":
        return float(raw) * 60.0
    if mode == "minutes":
        return float(raw)
    if mode == "drop":
        return None
    raise ValueError(mode)


class Pack:
    def __init__(self, target):
        self.dir = target
        F = {k: os.path.join(target, v) for k, v in FILES.items()}
        self.meds = {dt.date.fromisoformat(r["event_date"]) for r in _rows(F["meds"])}
        wb = load_workbook(F["inventory"], read_only=True)
        ws = wb["Feeders"]
        it = ws.iter_rows(values_only=True)
        head = next(it)
        self.inv = {r[0]: dict(zip(head, r)) for r in it if r and r[0]}
        self.subfeeders = defaultdict(set)
        for f, r in self.inv.items():
            self.subfeeders[r["Substation"]].add(f)
        self.legacy = _rows(F["legacy"])
        self.current = _rows(F["current"])
        self.crew = _rows(F["crews"])
        self.tickets = self._tickets()

    def _tickets(self, mode="golden", date="golden"):
        out = []
        for r in self.legacy:
            day = dt.datetime.strptime(r["OUT_DT"], "%m/%d/%Y").date()
            mins = legacy_minutes(r["DUR_MIN"], mode)
            st = legacy_start(day, r["OUT_TM"], mins, "." in r["DUR_MIN"], date)
            out.append(dict(tkt=r["TKT_NO"], sys="legacy", feeder="F-" + r["FDR"], sub=SUB_CODE[r["SUB_CD"]],
                            start=st, raw=r["DUR_MIN"], minutes=mins,
                            customers=int(r["CUST_OUT"]), cause=LEG_CAUSE[r["CAUSE_CD"]],
                            device=LEG_DEV[r["DEV_TYP"]], dev=r["DEV_ID"]))
        for r in self.current:
            s = dt.datetime.strptime(r["interruption_start_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            e = dt.datetime.strptime(r["restoration_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            out.append(dict(tkt=r["interruption_id"], sys="current", feeder=r["feeder"], sub=r["substation"],
                            start=s.astimezone(ET), end=e, raw=None, minutes=int((e - s).total_seconds() // 60),
                            customers=int(r["customers_interrupted"]), cause=r["cause_category"],
                            device=r["protective_device_type"], dev=r["protective_device"]))
        for t in out:
            t["day"] = t["start"].date()
            t["med"] = t["day"] in self.meds
            t["minute"] = t["start"].replace(second=0, microsecond=0)
        return out

    # the main call
    def shared_flags(self, tickets, tol=0, need=None):
        """a ticket opened in the same minute (within tol) as tickets on every feeder at its substation (or on at least
        `need` feeders there)"""
        starts = defaultdict(list)
        for t in tickets:
            starts[(t["sub"], t["day"])].append((t["start"], t["feeder"]))
        out = []
        for t in tickets:
            hit = {f for (s, f) in starts[(t["sub"], t["day"])]
                   if abs((s - t["start"]).total_seconds()) <= 60 * tol}
            out.append(len(hit) >= need if need else hit >= self.subfeeders[t["sub"]])
        return out

    def call(self, exclude_shared=True, tol=0, need=None, devices=BACKBONE, causes=ADDRESSED, med=True):
        rec = [t for t in self.tickets if 2019 <= t["day"].year <= 2025 and not (med and t["med"])]
        fl = self.shared_flags(rec, tol, need) if exclude_shared else [False] * len(rec)
        cmi = defaultdict(int)
        for t, sh in zip(rec, fl):
            if sh:
                continue
            if t["device"] in devices and t["cause"] in causes:
                cmi[t["feeder"]] += t["customers"] * t["minutes"]
        return {f: PREVENTED * cmi[f] / YEARS_N for f in CAND}

    def family(self):
        """the constructions that take out the tickets every feeder at a substation opened together"""
        out = {}
        for tol in (0, 1, 2, 5):
            out["same minute within %d" % tol] = self.call(True, tol)
        for tol in (0, 2):
            out["at least two feeders within %d" % tol] = self.call(True, tol, need=2)
        return out

    def shared_counts(self):
        rec = [t for t in self.tickets if not t["med"]]
        fl = self.shared_flags(rec)
        n = Counter()
        cmi = Counter()
        for t, sh in zip(rec, fl):
            if sh and t["feeder"] in CAND:
                n[t["feeder"]] += 1
                if t["device"] in BACKBONE and t["cause"] in ADDRESSED:
                    cmi[t["feeder"]] += t["customers"] * t["minutes"]
        return n, cmi

    # ask A: the storm record
    def stamp(self, r, mode="golden"):
        """a status's time: the storm desk records Assigned on its own screen and each crew's device the rest; the
        contract crews' devices keep Eastern standard time all year"""
        naive = dt.datetime.strptime(r["status_time_local"], "%Y-%m-%d %H:%M")
        device = r["status"] in DEVICE_STATUS
        if mode == "golden" and device and r["crew_type"] == "Contract line crew":
            return naive.replace(tzinfo=EST)
        if mode == "all_est" and device:
            return naive.replace(tzinfo=EST)
        if mode == "pbl_all_year" and device and r["crew_type"] == "Contract line crew":
            return naive.replace(tzinfo=ET) + dt.timedelta(hours=1)
        return naive.replace(tzinfo=ET)

    def crew_times(self, mode="golden"):
        restored, released = {}, defaultdict(list)
        for r in self.crew:
            if not r["oms_interruption_id"]:
                continue
            tm = self.stamp(r, mode)
            if r["status"] == "Restored":
                assert r["oms_interruption_id"] not in restored
                restored[r["oms_interruption_id"]] = tm
            elif r["status"] == "Released":
                released[r["oms_interruption_id"]].append(tm)
        return restored, {k: max(v) for k, v in released.items()}

    def storm(self, mode="golden"):
        """customer-minutes and customers interrupted on the accepted major event days of 2023 to 2025"""
        restored, released = self.crew_times({"crew": "eastern", "all_est": "all_est",
                                              "pbl_all_year": "pbl_all_year"}.get(mode, "golden"))
        tk = [t for t in self.tickets if t["sys"] == "current" and t["feeder"] in CAND]
        if mode == "utc_day":
            sel = [t for t in tk if t["start"].astimezone(UTC).date() in self.meds]
        else:
            sel = [t for t in tk if t["med"]]
        stamps = Counter(t["end"] for t in self.tickets if t["sys"] == "current" and t["med"])
        cmi, ci = defaultdict(int), defaultdict(int)
        for t in sel:
            end = t["end"]
            if mode in ("golden", "utc_day", "crew", "all_est", "pbl_all_year") and t["tkt"] in restored:
                end = restored[t["tkt"]]
            elif mode == "released" and t["tkt"] in released:
                end = released[t["tkt"]]
            elif mode == "repeated" and stamps[t["end"]] >= 2 and t["tkt"] in restored:
                end = restored[t["tkt"]]
            m = int((end.astimezone(UTC) - t["start"].astimezone(UTC)).total_seconds() // 60)
            cmi[t["feeder"]] += t["customers"] * m
            ci[t["feeder"]] += t["customers"]
        return {f: dict(cmi=cmi[f], ci=ci[f], per=cmi[f] / ci[f]) for f in CAND}

    # ask B: the taps' record
    def taps(self, mode="golden", date="golden"):
        tk = self._tickets(mode, date) if (mode, date) != ("golden", "golden") else self.tickets
        cmi, ci = defaultdict(float), defaultdict(int)
        for t in tk:
            if t["feeder"] not in CAND or t["device"] != "Fuse" or t["med"]:
                continue
            m = t["minutes"]
            if m is None or (mode == "minutes" and m <= 5):
                continue
            cmi[t["feeder"]] += t["customers"] * m
            ci[t["feeder"]] += t["customers"]
        return {f: dict(year=cmi[f] / YEARS_N, per=cmi[f] / ci[f]) for f in CAND}


def rnd(x, unit):
    return int(round(x / unit)) * unit if unit >= 1 else round(round(x / unit) * unit, 6)
