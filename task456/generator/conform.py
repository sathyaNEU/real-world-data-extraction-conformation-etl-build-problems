"""Read the bundle and conform the three feeds to hospital-days, the way the golden does it: the latest census
submission for each hospital and date (patients at or above staffed beds at 07:00), the adult ICU line's board
status replayed to the hospital's own days (Closed at any time), and a call on an adult ICU request declined for
no staffed bed (CAP; NB or NS before 1 December) on the hospital's own day. Also the three asks."""
import csv
import datetime as dt
import json
import os
from zoneinfo import ZoneInfo

UTC = dt.timezone.utc
CT = ZoneInfo("America/Chicago")
ICU_LABELS = {"Adult ICU", "ICU", "MICU/SICU", "Critical Care Unit", "Adult Critical Care", "Intensive Care"}
ED_LABELS = {"Emergency Department", "ED", "Emergency Dept"}
NO_BED = {"CAP", "NB", "NS"}


def _read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


class Pack:
    def __init__(self, folder, files):
        self.f = lambda k: os.path.join(folder, files[k])
        self.xw = _read(self.f("crosswalk"))
        self.reg = {r["county"]: r["region_code"] for r in _read(self.f("regions"))}
        self.hosp = {r["licence_no"]: r for r in self.xw}
        self.tz = {k: ZoneInfo(v["time_zone"]) for k, v in self.hosp.items()}
        self.region = {k: self.reg[v["county"]] for k, v in self.hosp.items()}
        self.by_new = {r["board_code"]: r["licence_no"] for r in self.xw}
        self.by_old = {r["board_code_previous"]: r["licence_no"] for r in self.xw}
        self.by_center = {r["center_code"]: r["licence_no"] for r in self.xw}
        self.by_name = {r["facility_name"]: r["licence_no"] for r in self.xw}
        self.alias = {r["typed_name"]: r for r in _read(self.f("aliases"))}
        self._events = None
        self._calls = None

    # -------------------------------------------------------------------------------------------- survey
    def census(self, latest=True, held=False):
        """{(licence, date): (staffed, patients)} from the latest submission of each hospital and date (the first,
        with latest=False; held=True counts the patients held in the emergency department as well, a mishandling)"""
        best = {}
        better = (lambda t, b: t > b) if latest else (lambda t, b: t < b)
        for r in _read(self.f("survey_new")):
            k = (r["licence_no"], dt.date.fromisoformat(r["report_date"]))
            t = dt.datetime.fromisoformat(r["submitted_at"])
            if k not in best or better(t, best[k][0]):
                best[k] = (t, int(r["staffed_adult_icu_beds"]), int(r["adult_icu_patients"]) +
                           (int(r["adult_icu_held_in_ed"]) if held else 0))
        for r in _read(self.f("survey_old")):
            k = (r["FacLicense"], dt.datetime.strptime(r["RptDate"], "%m/%d/%Y").date())
            t = dt.datetime.strptime(r["SubmitTime"], "%m/%d/%Y %H:%M").replace(tzinfo=self.tz[r["FacLicense"]])
            if k not in best or better(t, best[k][0]):
                best[k] = (t, int(r["AdultICU_Staffed"]), int(r["AdultICU_Census"]))
        return {k: (v[1], v[2]) for k, v in best.items()}

    # --------------------------------------------------------------------------------------------- board
    def events(self):
        """every board event with its hospital and unit: an event logged before the board's migration (the instant
        its system migration events re-log every unit under the crosswalk's board code) carries the facility's
        earlier code"""
        if self._events is None:
            raw = []
            with open(self.f("board"), encoding="utf-8") as fh:
                for line in fh:
                    e = json.loads(line)
                    t = dt.datetime.strptime(e["logged_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
                    raw.append((t, e))
            mig = {t for t, e in raw if e["set_by"] == "system migration"}
            assert len(mig) == 1
            self.migration = mig.pop()
            out = []
            for t, e in raw:
                lic = (self.by_old if t < self.migration else self.by_new).get(e["facility_code"])
                out.append((t, lic, e["unit"], e["status"], e["reason"]))
            out.sort(key=lambda x: x[0])
            self._events = out
        return self._events

    def intervals(self, labels, keep):
        """for each hospital, the UTC intervals during which a line with one of the labels held a status keep()
        accepts: {licence: [(start, end)]}"""
        lines = {}
        for t, lic, unit, status, reason in self.events():
            if unit in labels and lic is not None:
                lines.setdefault((lic, unit), []).append((t, status, reason))
        end = dt.datetime(2026, 1, 20, 12, 0, tzinfo=UTC)
        out = {}
        for (lic, unit), ev in lines.items():
            for i, (t, status, reason) in enumerate(ev):
                t1 = ev[i + 1][0] if i + 1 < len(ev) else end
                if keep(status, reason) and t1 > t:
                    out.setdefault(lic, []).append((t, t1))
        return out

    def board_closed_days(self, labels=ICU_LABELS):
        """{(licence, local date)}: the adult ICU line Closed at some time of the hospital's own day"""
        out = set()
        for lic, ivs in self.intervals(labels, lambda s, r: s == "Closed").items():
            for a, b in ivs:
                d = a.astimezone(self.tz[lic]).date()
                last = (b - dt.timedelta(microseconds=1)).astimezone(self.tz[lic]).date()
                while d <= last:
                    out.add((lic, d))
                    d += dt.timedelta(days=1)
        return out

    def board_logged_days(self, labels=ICU_LABELS):
        """{(licence, local date)}: a Closed status logged on the hospital's own day (a status carried in from the day
        before and not logged again that day does not count)"""
        out = set()
        for t, lic, unit, status, reason in self.events():
            if unit in labels and lic is not None and status == "Closed":
                out.add((lic, t.astimezone(self.tz[lic]).date()))
        return out

    def hours(self, labels, keep, start, end):
        """hours each hospital's lines spent in a status keep() accepts between the start of the hospital's local
        day `start` and the end of its local day `end`"""
        out = {}
        for lic, ivs in self.intervals(labels, keep).items():
            lo = dt.datetime.combine(start, dt.time(0, 0), tzinfo=self.tz[lic])
            hi = dt.datetime.combine(end + dt.timedelta(days=1), dt.time(0, 0), tzinfo=self.tz[lic])
            s = 0.0
            for a, b in ivs:
                a2, b2 = max(a, lo), min(b, hi)
                if b2 > a2:
                    s += (b2 - a2).total_seconds() / 3600
            out[lic] = s
        return out

    # ------------------------------------------------------------------------------------- transfer center
    def calls(self):
        """every call of both systems: dict(system, request, legacy, opened (aware), sender typed, patient, level,
        seq, called licence, called (aware), outcome, code)"""
        if self._calls is None:
            from openpyxl import load_workbook
            out = []
            wb = load_workbook(self.f("tc_old"), read_only=True)
            for ws in wb.worksheets:
                for row in ws.iter_rows(min_row=2, values_only=True):
                    if row[0] is None:
                        continue
                    lvl = {"Adult ICU": "ADULT_ICU", "Step-down/PCU": "STEP_DOWN", "Pediatric ICU": "PEDS_ICU"}[row[4]]
                    out.append(dict(system="old", request=str(row[0]), legacy="", opened=row[1].replace(tzinfo=CT),
                                    sender=row[2], patient=row[3], level=lvl, seq=int(row[5]),
                                    called=self.by_name.get(row[6] or ""), at=row[7].replace(tzinfo=CT),
                                    outcome={"Accepted": "ACCEPTED", "Declined": "DECLINED", "Cancelled": "CANCELLED",
                                             "No placement": "UNPLACED"}[row[8]], code=row[9] or ""))
            for r in _read(self.f("tc_new")):
                f = lambda s: dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
                out.append(dict(system="new", request=r["request_id"], legacy=r["legacy_case"], opened=f(r["opened_utc"]),
                                sender=r["sending_facility_text"], patient=r["patient_ref"], level=r["care_level"],
                                seq=int(r["seq"]), called=self.by_center.get(r["called_facility_id"]),
                                at=f(r["called_utc"]), outcome=r["outcome"], code=r["decline_code"]))
            self._calls = out
        return self._calls

    def declined_days(self, codes=NO_BED, levels=("ADULT_ICU",)):
        """{(licence, local date)}: a call on an adult ICU request declined for no staffed bed that day (codes=None:
        any decline)"""
        out = set()
        for c in self.calls():
            if (c["level"] in levels and c["outcome"] == "DECLINED" and (codes is None or c["code"] in codes)
                    and c["called"]):
                out.add((c["called"], c["at"].astimezone(self.tz[c["called"]]).date()))
        return out

    def hospital_days(self, start, end, latest=True, margin=0, labels=ICU_LABELS, codes=NO_BED,
                      levels=("ADULT_ICU",), logged=False, held=False):
        """one row per compact hospital and local day: (region, licence, name, date, census flag or None, board
        flag, transfer flag); the options are the mishandlings the checks run"""
        cen = self.census(latest, held)
        closed = self.board_logged_days(labels) if logged else self.board_closed_days(labels)
        dec = self.declined_days(codes, levels)
        rows = []
        for lic in sorted(self.hosp, key=lambda k: (self.region[k], self.hosp[k]["facility_name"])):
            d = start
            while d <= end:
                c = cen.get((lic, d))
                a = None if c is None else int(c[1] >= c[0] - margin)
                rows.append((self.region[lic], lic, self.hosp[lic]["facility_name"], d, a, int((lic, d) in closed),
                             int((lic, d) in dec)))
                d += dt.timedelta(days=1)
        return rows

    def clock(self, zone):
        """read every hospital's days on one clock (a mishandling): 'UTC', 'Central', or None for its own"""
        self._tz_own = getattr(self, "_tz_own", None) or dict(self.tz)
        if zone is None:
            self.tz = dict(self._tz_own)
        else:
            z = UTC if zone == "UTC" else CT
            self.tz = {k: z for k in self._tz_own}

    # ------------------------------------------------------------------------------------------------ asks
    def sender(self, typed):
        a = self.alias[typed]
        return a["facility_id"], (self.reg[a["county"]] if a["state"] == "TN" else None), ZoneInfo(a["time_zone"])

    def placements(self, start, end, carried_once=True, drop_cancelled=True, level="ADULT_ICU", zone=None,
                   on="opened"):
        """adult ICU placements of requests opened on the sending facility's own day in [start, end]: one per case
        (a case the new system took in at the cut-over carries the old request number as its legacy case); zone and
        on are the mishandlings the checks run (another clock; the acceptance's date)"""
        cases = {}
        for c in self.calls():
            key = c["legacy"] if (carried_once and c["legacy"]) else (c["system"] + ":" + c["request"])
            if c["system"] == "old":
                key = c["request"] if carried_once else "old:" + c["request"]
            cases.setdefault(key, []).append(c)
        out = []
        for key, cs in cases.items():
            cs.sort(key=lambda c: (c["at"], c["seq"]))
            if level and cs[0]["level"] != level:
                continue
            fid, reg, tz = self.sender(cs[0]["sender"])
            if zone is not None:
                tz = UTC if zone == "UTC" else CT
            acc = None
            for c in cs:
                if c["outcome"] == "ACCEPTED":
                    acc = c
                elif c["outcome"] == "CANCELLED" and drop_cancelled:
                    acc = None
            if acc is None:
                continue
            d = (cs[0]["opened"] if on == "opened" else acc["at"]).astimezone(tz).date()
            if not (start <= d <= end):
                continue
            out.append(dict(case=key, sender=fid, sender_region=reg, to=acc["called"], to_region=self.region[acc["called"]],
                            patient=cs[0]["patient"], opened=d))
        return out
