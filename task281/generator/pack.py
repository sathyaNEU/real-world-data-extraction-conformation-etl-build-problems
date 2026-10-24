"""Read the cut pack back: every figure the goldens carry is computed from these files, never from the world."""
from __future__ import annotations

import csv
import datetime as dt
import os

import numpy as np

import common as K

OFF_POST = ("Annual leave", "Sick leave", "Injury on duty", "Training", "Family and medical leave", "Military leave")


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        head = next(r)
        return [dict(zip(head, x)) for x in r]


class Pack:
    def __init__(self, target, dedupe=True, map_shiftlink=True):
        p = lambda k: os.path.join(target, K.FILES[k])
        self.target = target
        cat = {(r["source_system"], r["status_code"]): r["state_category"] for r in rows(p("codes"))}
        ro = rows(p("rosters"))
        if dedupe:
            # the nightly export re-ran for some days: one row a line and date, the latest export standing
            last = {}
            for r in ro:
                k = (r["shift_date"], r["line_id"])
                if k not in last or r["exported_at"] > last[k]["exported_at"]:
                    last[k] = r
            ro = list(last.values())
        for r in ro:
            c = cat.get((r["source_system"], r["status_code"]))
            if c is None and not map_shiftlink:
                c = "Unknown"
            r["cat"] = c
        self.roster = ro
        self.emp_rows = rows(p("employees"))
        self.emp_hist = {}
        for r in self.emp_rows:
            self.emp_hist.setdefault(r["employee_id"], []).append(r)
        for v in self.emp_hist.values():
            v.sort(key=lambda r: r["title_effective_from"])
        self.emp = {e: v[-1] for e, v in self.emp_hist.items()}
        self.position = rows(p("position"))
        self.classes = rows(p("classes"))
        self.payroll = rows(p("payroll"))
        self.earn = rows(p("earn"))
        self.offers = rows(p("offers"))

    # ------------------------------------------------------------------ helpers on the FY2026 record
    @staticmethod
    def day_index(d):
        return (dt.date.fromisoformat(d) - K.FY26_START).days

    def weekly(self, unit, cats):
        """hours by FY2026 fiscal week of the unit's roster rows in the given categories"""
        out = np.zeros(K.WEEKS)
        for r in self.roster:
            if r["unit_code"] != unit or r["cat"] not in cats:
                continue
            w = K.fweek(self.day_index(r["shift_date"]))
            if w:
                out[w - 1] += float(r["scheduled_hours"])
        return out

    def availability(self, select):
        """1 less the share of held scheduled hours off post, over the roster rows whose holder passes select"""
        sched = off = 0.0
        for r in self.roster:
            e = r["employee_id"]
            if not e or not select(r, self.emp.get(e)):
                continue
            h = float(r["scheduled_hours"])
            sched += h
            if r["cat"] in OFF_POST:
                off += h
        return 1.0 - off / sched

    def title_on(self, e, d):
        """the title an employee held on date d (ISO string), from HR's rows a title spell"""
        for r in self.emp_hist.get(e, []):
            if r["title_effective_from"] <= d and (not r["title_effective_to"] or d <= r["title_effective_to"]):
                return r["title_code"]
        return self.emp[e]["title_code"]

    def new_lines(self, unit):
        """the position control's lines vacant at the start of FY2028: (line, first shift on post, days off)"""
        days = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
        out = []
        for r in self.position:
            if r["unit_code"] == unit and r["status_fy2028_start"] == "Vacant":
                off = {days.index(x) for x in r["days_off"].split("/")}
                out.append((r["line_id"], dt.date.fromisoformat(r["first_shift_on_post"]), off))
        return out
