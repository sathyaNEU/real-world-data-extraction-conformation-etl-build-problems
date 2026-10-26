"""The pack's system exports for task121: the call-taker list, the roster's worked shifts, the CAD's medical calls and
unit history, the crews' patient care records, the phone system's call detail, the cardiac arrest reviews and the two
distractors. Each file in its own system's layout: the CAD and the roster in local time, the phone system in UTC."""
import csv
import datetime as dt

import numpy as np

import common as K
import world as W

SHIFT_NAME = {"D": "Day", "E": "Evening", "N": "Night"}
ACUITY = {1: "1 - Critical", 2: "2 - Emergent", 3: "3 - Urgent", 4: "4 - Non-urgent"}


def mdy(d):
    return d.strftime("%m/%d/%Y")


def mdyt(t, seconds=True):
    return t.strftime("%m/%d/%Y %H:%M:%S" if seconds else "%m/%d/%Y %H:%M")


def iso_z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def minsec(s):
    """a time of s seconds keyed as minutes and seconds without the colon: 125 seconds is 2:05, stored as 205"""
    return s if s < 60 else (s // 60) * 100 + s % 60


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(head)
        w.writerows(rows)


class Records:
    def __init__(self, world, seed=K.SEED):
        self.w = world
        self.seed = seed
        self.emp_of = {s["login"]: s["emp"] for s in world.staff}

    def taker_rows(self):
        head = ["employee_no", "cad_login", "emd_certified", "academy_class", "status", "status_date"]
        rows = []
        for s in sorted(self.w.staff, key=lambda s: s["emp"]):
            status, sd = ("Retired", mdy(s["leave"])) if s["leave"] else ("Active", "")
            if s["emp"] == self.w.staff[37]["emp"]:
                sd = mdy(s["start"])
                status = "Active (lateral)"
            rows.append([s["emp"], s["login"], mdy(s["certified"]), s["cls"], status, sd])
        return head, rows

    def roster_rows(self):
        head = ["employee_no", "shift_date", "shift", "start", "end", "worked_as"]
        rows = []
        for r in sorted(self.w.shifts, key=lambda r: (r["date"], r["start"], self.emp_of[r["login"]])):
            rows.append([self.emp_of[r["login"]], mdy(r["date"]), SHIFT_NAME[r["type"]], mdyt(r["start"], False),
                         mdyt(r["end"], False), r["kind"].title()])
        return head, rows

    def call_rows(self):
        head = ["incident_no", "call_answered", "call_taker", "protocol", "chief_complaint", "determinant",
                "response", "protocol_version", "unit", "unit_assigned", "che_call_id"]
        rows = []
        for c in self.w.calls:
            p = K.PROTOCOL[c["protocol"]]
            for inc, units in [(c["incident"], c["units"])] + ([(c["split"]["incident"], c["split"]["units"])]
                                                             if c["split"] else []):
                last = units[-1]
                rows.append([inc, mdyt(W.to_local(c["utc"])), c["login"], c["protocol"], p[1],
                             "%s-%s-%d" % (c["protocol"], c["level"], c["suffix"]),
                             "HOT" if c["level"] in K.LEVELS_HOT else "COLD", c["version"], last["unit"],
                             mdyt(W.to_local(last["assigned"])), c["che"]])
        rows.sort(key=lambda r: r[0])
        return head, rows

    def epcr_rows(self):
        """one record a patient; the incident number as the crews' tablets key it, digits only. A second patient
        taken by the split's ambulance is on the split incident's record"""
        rng = np.random.default_rng([121, self.seed, 20])
        head = ["pcr_number", "incident_number", "unit", "patient", "crew_acuity", "disposition", "pcr_completed"]
        out = []
        for c in self.w.calls:
            if not c["contact"]:
                continue
            unit = c["units"][-1]
            arr = unit["at_scene"]
            pats = [c["acuity"]]
            if c["second_patient"]:
                pats.append(3 if rng.random() < 0.5 else 4)
            for k, a in enumerate(pats, start=1):
                if a in (1, 2):
                    disp = "Dead at scene" if c["protocol"] == "09" and rng.random() < 0.55 else "Transported"
                else:
                    disp = str(rng.choice(["Transported", "Treated and released", "Refused care"], p=[0.62, 0.18, 0.2]))
                mins = dt.timedelta(minutes=int(rng.integers(35, 600)))
                inc, un, at, kk = c["incident"], unit["unit"], arr, k
                if k == 2 and c["split"]:
                    sp = c["split"]["units"][0]
                    inc, un, at, kk = c["split"]["incident"], sp["unit"], sp["at_scene"], 1
                done = W.to_local(at) + mins
                out.append((done, [None, inc.replace("-", ""), un, kk, ACUITY[a], disp, mdyt(done, False)]))
        rs = np.random.default_rng([121, self.seed, 22])
        for s in self.w.splits:
            if s["acuity"] is None:
                continue
            sp = s["units"][0]
            disp = str(rs.choice(["Transported", "Treated and released", "Refused care"], p=[0.7, 0.15, 0.15]))
            done = W.to_local(sp["at_scene"]) + dt.timedelta(minutes=int(rs.integers(35, 600)))
            out.append((done, [None, s["incident"].replace("-", ""), sp["unit"], 1, ACUITY[s["acuity"]], disp,
                               mdyt(done, False)]))
        out.sort(key=lambda x: (x[0], x[1][1], x[1][3]))
        rows = []
        n = 6120400
        for _, r in out:
            n += int(rng.integers(1, 4))
            r[0] = "E%08d" % n
            rows.append(r)
        return head, rows

    def unit_rows(self):
        head = ["incident_no", "unit", "assigned", "enroute", "at_scene", "cleared", "outcome"]
        rows = []
        incs = [(c["incident"], c["units"]) for c in self.w.calls] + [(s["incident"], s["units"]) for s in self.w.splits]
        for inc, units in sorted(incs, key=lambda x: x[0]):
            for u in units:
                f = lambda k: mdyt(W.to_local(u[k])) if u.get(k) else ""
                rows.append([inc, u["unit"], f("assigned"), f("enroute"), f("at_scene"), f("cleared"), u["outcome"]])
        return head, rows

    def che_rows(self):
        head = ["call_id", "trunk_group", "class_of_service", "ani", "arrived_utc", "answered_utc", "released_utc",
                "position", "abandoned"]
        rows = []
        for r in self.w.che:
            rows.append([r["call_id"], r["trunk"], r["cos"], r["ani"], iso_z(r["arrived"]),
                         iso_z(r["answered"]) if r["answered"] else "", iso_z(r["released"]),
                         "" if r["abandoned"] else r["position"], "Y" if r["abandoned"] else "N"])
        return head, rows

    def tcpr_rows(self):
        """the review form takes each time as minutes and seconds; the log stores seconds, reading a time keyed
        without its colon as seconds as it stands. One reviewer keys every time that way"""
        head = ["review_id", "incident_no", "review_type", "reviewer", "reviewed_on", "recording_started",
                "arrest_recognised_s", "first_compression_s", "no_tcpr_reason"]
        rows = []
        for r in self.w.tcpr:
            rec, fc = r["recognised"], r["first"]
            if r["reviewer"] == K.MINSEC_REVIEWER:
                rec = minsec(rec)
                fc = None if fc is None else minsec(fc)
            rows.append([r["review_id"], r["incident"], r["kind"], r["reviewer"], mdy(r["reviewed"]),
                         mdyt(W.to_local(r["start"])), rec, "" if fc is None else fc, r["reason"] or ""])
        return head, rows

    def case_rows(self):
        head = ["case_id", "incident_no", "call_taker", "reviewed_on", "case_entry_pct", "chief_complaint_pct",
                "key_questions_pct", "final_coding_pct", "overall_pct"]
        rows = []
        for c in self.w.cases:
            parts = c["parts"]
            rows.append([c["case_id"], c["incident"], c["login"], mdy(c["reviewed"])] + parts +
                        [K.r0(sum(parts) / 4.0)])
        return head, rows

    def unit_hour_rows(self):
        head = ["service_date", "unit", "staffed_hours"]
        return head, [[mdy(d), u, "%.1f" % h] for d, u, h in self.w.unit_hours]
