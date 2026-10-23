"""task170 records: the world's spells written the way each system holds them.

HR keeps every spell since January 2019 under both employee numbers (the new HR and payroll system issued E-numbers
at the February 2026 cutover; V-numbers are the old system's). Ledstrand, the plan's administrator, keeps one row per
membership under the employer reference it was opened with. Tarnmark Mutual keeps one row per income protection
policy. Payroll exports a line per assignment per deduction code per payroll."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C
import world as W

DEPTS = {"VCS": ["Medicine", "Surgery", "Emergency", "Women and children", "Radiology", "Laboratory", "Facilities",
                 "Administration"],
         "RDH": ["Medicine", "Surgery", "Emergency", "Rehabilitation", "Facilities", "Administration"],
         "ASK": ["Medicine", "Surgery", "Psychiatry", "Facilities", "Administration"],
         "OSV": ["Medicine", "Geriatrics", "Emergency", "Facilities", "Administration"],
         "BRB": ["Medicine", "Surgery", "Facilities", "Administration"],
         "LDM": ["Rehabilitation", "Medicine", "Geriatrics", "Facilities", "Administration"]}
DEPT_CODE = {"Medicine": "110", "Surgery": "120", "Emergency": "130", "Women and children": "140", "Radiology": "150",
             "Laboratory": "160", "Psychiatry": "170", "Geriatrics": "180", "Rehabilitation": "190",
             "Facilities": "810", "Administration": "900"}
RERUN = ((2026, 4), "RDH")
END_REASONS = [("Resignation", 0.64), ("End of fixed term", 0.19), ("Retirement", 0.09), ("Dismissal", 0.02),
               ("Transfer to another employer", 0.06)]


def d_of(i):
    y, m = C.ym_of(i)
    return C.D(y, m, 1)


def start_date(i):
    y, m = C.ym_of(i)
    return C.first_working_day(y, m)


def end_date(i):
    y, m = C.ym_of(i)
    return C.month_end(y, m)


def scale_for(i):
    y, _ = C.ym_of(i)
    return C.SCALE_2025 if y <= 2025 else C.SCALE_2026


def enrich(S, seed=C.SEED + 1):
    """Departments, end reasons, new employee numbers, the stock's retirements at the October 2026 month end."""
    rng = np.random.default_rng(seed)
    last = C.mindex(C.LAST_PAYROLL)
    newno = {}
    order = sorted({s["emp"] for s in S})
    perm = rng.permutation(len(order))
    for k, e in zip(perm, order):
        newno[e] = 400000 + int(k) * 3 + int(rng.integers(0, 3))
    for s in S:
        s["vol_ipc"] = bool(s["stock"] and rng.random() < 0.34)
        s["dept"] = str(rng.choice(DEPTS[s["hosp"]]))
        s["eno"] = "E%06d" % newno[s["emp"]]
        s["vno"] = "V%06d" % s["emp"]
        r = rng.random()
        acc = 0
        s["reason"] = END_REASONS[0][0]
        for name, w in END_REASONS:
            acc += w
            if r < acc:
                s["reason"] = name
                break
    # retirements at the end of October 2026: staff in the January 2019 stock who reach pension age then
    for h in C.H_CODES:
        pool = [s for s in S if s["stock"] and s["hosp"] == h and s["end"] > last and s["save"] and s["join"] is not None
                and s["join"] < C.mindex(C.HIST_START)]
        k = int(rng.integers(3, 7))
        for s in sorted(pool, key=lambda x: x["start"])[:k]:
            s["end"] = last
            s["reason"] = "Retirement"
    return S


def hr_rows(S):
    """One row per spell in post at any time from 1 January 2019; open spells have no end date."""
    last = C.mindex(C.LAST_PAYROLL)
    rows = []
    for s in sorted(S, key=lambda x: (x["start"], x["emp"], x["spell"])):
        hosp = s["hosp"]
        if hosp == "LDM" and s["end"] < C.mindex((2024, 7)):
            hosp = "LRC"
        ended = s["end"] <= last
        rows.append([s["eno"], s["vno"], s["spell"], hosp, s["dept"], s["grade"], s["fte"], start_date(s["start"]),
                     end_date(s["end"]) if ended else "", s["reason"] if ended else ""])
    return rows


def register_rows(S, rng):
    """Ledstrand's member register at the October 2026 payroll: one row per membership. The snapshot is taken before
    the October month-end leavers file, so members whose employment ended on 31 October 2026 still read Active."""
    last = C.mindex(C.LAST_PAYROLL)
    member_no = {}
    rows = []
    mem = [s for s in S if s["join"] is not None and s["join"] <= last]
    seen = {}
    for s in sorted(mem, key=lambda x: (x["join"], x["emp"])):
        if s["emp"] not in member_no:
            member_no[s["emp"]] = "K%07d" % (1200000 + len(member_no) * 7 + int(rng.integers(0, 7)))
        seen[s["emp"]] = seen.get(s["emp"], 0) + 1
        seq = seen[s["emp"]]
        ref = s["vno"] if s["join"] < C.mindex(C.MIGRATION) else s["eno"]
        hosp = s["hosp"]
        if hosp == "LDM" and s["join"] < C.mindex((2024, 7)):
            hosp = "LRC"
        y, m = C.ym_of(s["join"])
        jd = C.pay_day(y, m)
        cur = s["rate"]
        # a few members change their rate at an April pay award
        n_apr = max(0, (min(s["end"], last) - s["join"]) // 12)
        for _ in range(n_apr):
            if rng.random() < 0.05:
                cur = int(rng.choice(W.RATES, p=W.RATE_W))
        s["cur_rate"] = cur
        if s["end"] < last:
            status, sd = "Deferred", end_date(s["end"])
        else:
            status, sd = "Active", ""
        rows.append([member_no[s["emp"]], seq, ref, hosp, jd, s["rate"], cur, status, sd])
    return rows


def ipc_rows(S, rng):
    """Tarnmark Mutual's bordereau: every hire since January 2019 was enrolled in the cover at hire; a member may
    cancel at any time, and a cancellation received by the 10th stops that month's premium. Policies opened before
    the insurer's July 2022 system change carry their old number beside the new one."""
    last = C.mindex(C.LAST_PAYROLL)
    rows = []
    seq = [0]
    for s in sorted([s for s in S if not s["stock"] or s["vol_ipc"]], key=lambda x: (x["start"], x["emp"], x["spell"])):
        seq[0] += 1
        sy, sm = C.ym_of(s["start"])
        newp = "NM-%08d" % (31000000 + seq[0] * 3 + int(rng.integers(0, 3)))
        oldp = ("IP%02d-%06d" % (sy % 100, seq[0])) if s["start"] < C.mindex((2022, 7)) else ""
        hosp = s["hosp"]
        if hosp == "LDM" and s["start"] < C.mindex((2024, 7)):
            hosp = "LRC"
        ref = s["vno"] if s["start"] < C.mindex(C.MIGRATION) else s["eno"]
        cs = start_date(s["start"])
        basis = "Auto"
        if s["stock"]:
            basis, ref, cs = "Voluntary", s["vno"], C.D(2019, 1, 1) if s["start"] < C.mindex(C.HIST_START) else cs
        recv, cend, reason = "", "", ""
        if s["cancel"] is not None and s["cancel"] <= last:
            c = s["cancel"]
            cy, cm = C.ym_of(c)
            if c == s["start"]:
                lo, hi = cs, C.D(cy, cm, C.CUTOFF_DAY)
            else:
                py, pm = C.ym_of(c - 1)
                lo, hi = C.D(py, pm, C.CUTOFF_DAY + 1), C.D(cy, cm, C.CUTOFF_DAY)
            span = (hi - lo).days
            recv = lo + dt.timedelta(days=int(rng.integers(0, span + 1)))
            cend = cs if c == s["start"] else end_date(c - 1)
            reason = "Cancelled by member"
        elif s["end"] <= last:
            cend, reason = end_date(s["end"]), "Employment ended"
        if s["stock"]:
            oldp = "IP%02d-%06d" % (18, seq[0])
            if s["end"] <= last:
                cend, reason = end_date(s["end"]), "Employment ended"
        rows.append([newp, oldp, ref, hosp, basis, cs, recv, cend, reason])
    return rows


def deduction_rows(S, rng):
    """Payroll deduction lines, November 2025 to October 2026: PEN (the employee's contribution), ERM (the
    employer's match) and IPC (the cover's premium), one line per assignment. Payroll computes the match on the
    person's pensionable pay across assignments and writes it on each assignment's line."""
    first, last = C.mindex(C.DEDUCT_START), C.mindex(C.LAST_PAYROLL)
    rows = []
    for i in range(first, last + 1):
        y, m = C.ym_of(i)
        pdte = C.pay_day(y, m)
        scale = scale_for(i)
        new_sys = i >= C.mindex(C.MIGRATION)
        for s in S:
            if not (s["start"] <= i <= s["end"]):
                continue
            ref = s["eno"] if new_sys else s["vno"]
            a1 = round(scale[s["grade"]] * s["fte"], 2)
            a2 = round(scale[s["grade"]] * s["second_fte"], 2) if s["second_fte"] else 0.0
            posts = [(1, a1, DEPT_CODE[s["dept"]])] + ([(2, a2, "950")] if a2 else [])
            cc = s["hosp"]
            contributing = s["join"] is not None and s["join"] <= i
            rate = s.get("cur_rate", s["rate"]) if contributing else 0
            covered = (not s["stock"]) and not (s["cancel"] is not None and s["cancel"] <= i)
            if s["stock"]:
                covered = s.get("vol_ipc", False)
            erm = round(C.match_pct(rate) / 100 * (a1 + a2), 2) if contributing else 0.0
            lines = []
            for a, basic, dc in posts:
                if contributing:
                    lines.append([a, cc + "-" + dc, "PEN", basic, rate, round(rate / 100 * basic, 2)])
                    lines.append([a, cc + "-" + dc, "ERM", basic, "", erm])
                if covered and a == 1:
                    lines.append([a, cc + "-" + dc, "IPC", basic, "", round(C.IPC_PREMIUM * basic, 2)])
            if (y, m) == RERUN[0] and s["hosp"] == RERUN[1]:
                # Rendholm's April 2026 payroll ran on the 2025 scale, was reversed and run again on the 2026 scale
                old = C.SCALE_2025
                b1 = round(old[s["grade"]] * s["fte"], 2)
                b2 = round(old[s["grade"]] * s["second_fte"], 2) if s["second_fte"] else 0.0
                e_old = round(C.match_pct(rate) / 100 * (b1 + b2), 2) if contributing else 0.0
                wrong = []
                for ln in lines:
                    b = b1 if ln[0] == 1 else b2
                    amt = {"PEN": round(rate / 100 * b, 2), "ERM": e_old, "IPC": round(C.IPC_PREMIUM * b, 2)}[ln[2]]
                    wrong.append([ln[0], ln[1], ln[2], b, ln[4], amt])
                for ln in wrong:
                    rows.append([y * 100 + m, pdte, "MAIN", ref] + ln)
                for ln in wrong:
                    rows.append([y * 100 + m, C.D(2026, 4, 28), "REVERSAL", ref] + ln[:3] + [-ln[3], ln[4], -ln[5]])
                for ln in lines:
                    rows.append([y * 100 + m, C.D(2026, 4, 29), "RERUN", ref] + ln)
            else:
                for ln in lines:
                    rows.append([y * 100 + m, pdte, "MAIN", ref] + ln)
    return rows
