"""task170 pack writer: every data file under target/ from the world, as each system exports it."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C
import xlsx_writer as XW

LINK_NAME = {"MAIN": "Main", "SPARE": "Spare", "INSTR": "Instructor", "MGR": "Manager", "RESTR": "Restricted duties"}
GRADE = {"MAIN": "Driver", "SPARE": "Driver", "INSTR": "Driver Instructor", "MGR": "Driver Manager",
         "RESTR": "Driver"}


class Pack:
    def __init__(self, w):
        self.w = w

    # ------------------------------------------------------------------ the on-board recorders' Start of Mission log
    def write_som(self, path):
        rows = []
        for i, (t, pid, staff, unit, cab, typ) in enumerate(self.w.starts):
            rows.append(("SM%09d" % (i + 104000000), t.strftime("%Y-%m-%dT%H:%M:%SZ"), unit, cab, staff, typ))
        return C.write_csv(path, ["som_ref", "obr_utc", "unit", "cab", "driver_id", "som_type"], rows, crlf=False)

    # ------------------------------------------------------------------ the safety desk's register
    def register_rows(self):
        w = self.w
        g = C.stream("register")
        cutoff = dt.datetime.combine(C.RECORD_END, dt.time(23, 59, 59))
        # the extract holds the reports logged to the record's end; a later report of an October event is not in it
        reps = [dict(r) for r in w.tde_reports + w.event_reports if r["when"] <= cutoff]
        reps.sort(key=lambda r: (r["when"], r["cat"], r["unit"], r["who"]))
        seq = {}
        for r in reps:
            y = r["when"].year % 100
            seq[y] = seq.get(y, 0) + 1
            r["no"] = "SD%02d-%05d" % (y, seq[y])
        first = {}
        for r in reps:
            key = r["event"]
            if r["who"] == "OBR download" or key[1] == -1:
                continue
            if r.get("primary") and key not in first:
                first[key] = r["no"]
        out = []
        for r in reps:
            linked = ""
            if r["who"] != "OBR download" and r["event"][1] != -1 and not r.get("primary"):
                linked = first.get(r["event"], "")
            age = (dt.datetime.combine(C.RECORD_END, dt.time(23, 59)) - r["when"]).days
            status = "Withdrawn" if r.get("withdrawn") else ("Open" if age < 18 and g.random() < 0.7 else "Closed")
            out.append((r["no"], r["when"].replace(second=0, microsecond=0), r["who"], r["cat"], r["depot"], r["staff"],
                        r["unit"], r["ref"], linked, status, r["what"]))
        return out

    def write_register(self, path):
        head = ["Report No", "Received", "Reporter", "Category", "Depot", "Staff No", "Unit", "SoM Ref", "Linked To",
                "Status", "Sub-category"]
        rows = self.register_rows()
        XW.STAMPS[C.F_REG] = ("Gillian Armstrong", "2026-11-04T08:42:00Z")
        return XW.write_table(path, "Register", head, rows, widths=[12, 16, 16, 9, 7, 9, 9, 13, 12, 10, 52],
                              date_fmt="dd/mm/yyyy hh:mm")

    # ------------------------------------------------------------------ Resourcing
    def write_roster(self, path):
        w = self.w
        rows = []
        for p in w.people:
            if p.end != C.RECORD_END:
                continue
            rows.append((w.number_on(p, C.ROSTER_DATE), w.depot_on(p, C.ROSTER_DATE), GRADE[p.link], LINK_NAME[p.link],
                         "Part-time" if p.contract == "PT" else "Full-time", p.dob, p.qualified))
        rows.sort(key=lambda r: (r[1], r[0]))
        XW.STAMPS[C.F_ROSTER] = ("Resourcing", "2026-11-02T07:15:00Z")
        return XW.write_table(path, "Roster 31 Oct 2026",
                              ["Staff No", "Depot", "Grade", "Link", "Contract", "Date of Birth", "Qualified"], rows,
                              widths=[10, 7, 18, 18, 11, 13, 12])

    def write_crosswalk(self, path):
        rows = []
        for p in self.w.people:
            for (when, num), (_, prev) in zip(p.numbers[1:], p.numbers[:-1]):
                dest = [d for wd, d in p.depots if wd == when][0]
                rows.append((prev, num, when.isoformat(), "Transfer to " + C.DEPOT[dest][1]))
        rows.sort(key=lambda r: (r[2], r[0]))
        return C.write_csv(path, ["old_staff_no", "new_staff_no", "effective", "reason"], rows)

    def write_duties(self, path):
        rows = [(d.isoformat(), staff, dep, duty, ca, status, issue) for d, staff, dep, duty, ca, status, issue in self.w.duties]
        return C.write_csv(path, ["duty_date", "staff_no", "depot", "duty_no", "cab_activations", "status", "issue"], rows)

    # ------------------------------------------------------------------ Class 461 fleet and the fitment programme
    def write_allocation(self, path):
        rows = sorted(((u["now"], u["depot"], "2026-12-13") for u in self.w.units461), key=lambda r: (r[1], r[0]))
        return C.write_csv(path, ["unit", "depot", "allocated_from"], rows)

    def works_rows(self):
        g = C.stream("works")
        rows = []
        for v in sorted(self.w.veh461.values(), key=lambda v: (v["unit"], v["end"])):
            acc = v["accepted"]
            done = acc <= C.RECORD_END
            win = acc - dt.timedelta(days=int(g.integers(38, 62)))
            wout = acc - dt.timedelta(days=int(g.integers(9, 21)))
            dyn = acc - dt.timedelta(days=int(g.integers(3, 8)))
            if done:
                rows.append((v["vehicle"], v["unit"], v["end"], win, wout, dyn, acc, None, "Accepted"))
            elif win <= C.RECORD_END:
                rows.append((v["vehicle"], v["unit"], v["end"], win, None, None, None, acc, "In works"))
            else:
                rows.append((v["vehicle"], v["unit"], v["end"], None, None, None, None, acc, "Planned"))
        return rows

    def write_works(self, path):
        head = ["Vehicle", "Unit", "End", "Works In", "Works Out", "Dynamic Test", "Accepted", "Planned Acceptance",
                "Status"]
        XW.STAMPS[C.F_WORKS] = ("Fitment Programme Office", "2026-11-03T16:20:00Z")
        return XW.write_table(path, "Class 461 vehicles", head, self.works_rows(),
                              widths=[9, 9, 5, 11, 11, 12, 11, 18, 10])

    def write_formations(self, path):
        cls = lambda u: "461/" + u[3]
        rows = sorted((u, a, b, cls(u)) for u, (a, b) in self.w.form461.items())
        return C.write_csv(path, ["unit", "vehicle_a_end", "vehicle_b_end", "class"], rows)

    def write_renumbering(self, path):
        rows = sorted(((o, n, d.isoformat(), why) for o, n, d, why in self.w.renum461), key=lambda r: (r[2], r[0]))
        return C.write_csv(path, ["old_unit", "new_unit", "effective", "reason"], rows)

    # ------------------------------------------------------------------ distractors
    def write_punctuality(self, path):
        g = C.stream("punctuality")
        rows = []
        for code, name, ph, golive in C.DEPOTS:
            lvl = g.uniform(88.5, 93.5)
            y, m = 2024, 1
            while (y, m) <= (2026, 10):
                v = lvl + g.normal(0, 1.1) - (1.6 if m in (11, 12, 1) else 0.0)
                planned = int(g.integers(2200, 4800) if ph < 4 else g.integers(600, 1300))
                rows.append((code, name, "%04d-%02d" % (y, m), planned, round(min(99.4, v), 1)))
                y, m = (y + (m == 12), m % 12 + 1)
        XW.STAMPS[C.F_PUNC] = ("Performance and Planning", "2026-11-05T10:02:00Z")
        return XW.write_table(path, "PPM by depot", ["Depot", "Depot Name", "Month", "Trains Planned", "PPM %"], rows,
                              widths=[7, 18, 9, 14, 8])

    def write_weather(self, path):
        g = C.stream("weather")
        rows = []
        day = dt.date(2024, 1, 1)
        while day <= C.RECORD_END:
            doy = day.timetuple().tm_yday
            for code, name, ph, golive in C.DEPOTS:
                base = 9.5 - (2.5 if ph == 4 else 0.0) + 6.5 * np.sin(2 * np.pi * (doy - 110) / 365.25)
                tmax = base + 4 + g.normal(0, 2.4)
                tmin = base - 4 + g.normal(0, 2.2)
                rain = max(0.0, g.gamma(0.7, 4.0) - 1.2)
                rows.append((day.isoformat(), code, round(tmax, 1), round(tmin, 1), round(rain, 1),
                             "Y" if tmin < 0 else "N"))
            day += dt.timedelta(days=1)
        return C.write_csv(path, ["date", "depot", "max_temp_c", "min_temp_c", "rain_mm", "frost"], rows)
