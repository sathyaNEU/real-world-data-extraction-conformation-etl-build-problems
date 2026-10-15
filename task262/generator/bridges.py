"""The foundation's 2019 to 2023 Bridges program, as its two case-management systems and its ledger hold it: young
people enrolled at a regional office on an intake Monday, some moving office (a transfer, the receiving record naming
the record it continues), the April 2021 move from CaseTrack to Northstar (CaseTrack switched off with each case open that day
still showing active, and the case carried into Northstar at the same office with its intake date and a new
reference, the dates of birth CaseTrack had taken month first put right), and the program's ledger by cost centre, with the
December mentor fees some offices accrued at year end reversed in one line at the central cost centre each January,
central costs, and the 2024 close-out."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

OFFICES = [("TVL", "Torvale Metro", "Torvale"), ("HAL", "Halverston", "Halverston"), ("KES", "Kestry North", "Port Kestry"),
           ("SEL", "Selvane Valley", "Selvane Falls"), ("DAN", "Danholt Lakes", "Danholt"),
           ("CAS", "Caskell Coast", "Caskell Harbour"), ("OST", "Ostler Plains", "Ostlerton"),
           ("WEN", "Wendmoor", "Wendmoor")]
OFFICE_REGION = {o: r for o, r, _ in OFFICES}
YOUNG = {"TVL": 318, "HAL": 151, "KES": 117, "SEL": 163, "DAN": 193, "CAS": 128, "OST": 171, "WEN": 112}


def _date(r, a, b):
    return a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))


def people():
    """The young people as they were: first office, intake, date of birth, any later moves, and the outcome."""
    r = K.rng("bridges-people")
    out = []
    pid = 0
    for off, _, _ in OFFICES:
        for _ in range(YOUNG[off]):
            intake = K.BRIDGES_START + dt.timedelta(weeks=int(r.integers(0, 234)))
            age = r.uniform(15.0, 19.5)
            dob = intake - dt.timedelta(days=int(age * 365.25))
            # moves between offices (a family relocation) during the plan
            moves = []
            if r.random() < 0.06:
                to = OFFICES[int(r.integers(0, len(OFFICES)))][0]
                if to != off:
                    moves.append((to, intake + dt.timedelta(days=int(r.integers(30, 250)))))
            plan_end = intake + dt.timedelta(days=365)
            u = r.random()
            if plan_end > K.BRIDGES_END:
                outcome, end = ("Active", None) if u < 0.80 else ("Withdrawn", _date(r, intake + dt.timedelta(days=20),
                                                                                    K.BRIDGES_END))
            elif u < 0.63:
                outcome, end = "Completed", plan_end + dt.timedelta(days=int(r.integers(-10, 25)))
            else:
                outcome, end = "Withdrawn", intake + dt.timedelta(days=int(r.integers(20, 330)))
            if moves and end is not None and moves[0][1] >= end:
                moves = []
            out.append(dict(pid=pid, office=off, intake=intake, dob=dob, moves=moves, outcome=outcome, end=end,
                            swapped=False))
            pid += 1
    return out


REFERRALS = ("School", "School", "School", "Youth worker", "Youth worker", "Self", "Family", "Community agency")


def records(P):
    """The export as the two systems hold it: one row per enrolment record."""
    r = K.rng("bridges-records")
    rows = []
    seq_old = {y: 0 for y in range(2019, 2022)}
    seq_new = [0]

    def old_ref(d):
        seq_old[d.year] += 1
        return "BR-%02d-%04d" % (d.year % 100, seq_old[d.year])

    def new_ref():
        seq_new[0] += 1
        return "P%06d" % (104200 + seq_new[0] * 3 + int(r.integers(0, 3)))

    for p in sorted(P, key=lambda p: (p["intake"], p["pid"])):
        p["referral"] = REFERRALS[int(r.integers(0, len(REFERRALS)))]
        segs = []           # (office, start, end or None, closing status)
        cur_off, cur_start = p["office"], p["intake"]
        for to, when in p["moves"]:
            segs.append((cur_off, cur_start, when, "Transferred out"))
            cur_off, cur_start = to, when + dt.timedelta(days=int(r.integers(0, 15)))
        segs.append((cur_off, cur_start, p["end"], p["outcome"]))
        prev = None
        # CaseTrack took dates of birth as typed; some offices typed the month first, which Northstar put right
        ct_dob = p["dob"]
        if p["dob"].day <= 12 and p["dob"].day != p["dob"].month and r.random() < 0.55:
            ct_dob = dt.date(p["dob"].year, p["dob"].day, p["dob"].month)
        for off, start, end, status in segs:
            # the April 2021 system move: CaseTrack was switched off with a record open on the migration day still
            # active, and the case was carried into Northstar at the same office, with its intake date and a new reference
            if start < K.MIGRATION and (end is None or end > K.MIGRATION):
                ref = old_ref(start)
                if ct_dob != p["dob"]:
                    p["swapped"] = True
                p["migrated"] = True
                rows.append(dict(ref=ref, system="CaseTrack", office=off, intake=start, dob=ct_dob, status="Active",
                                 exit=None, transfer_from=prev or "", referral=p["referral"], pid=p["pid"]))
                nref = new_ref()
                rows.append(dict(ref=nref, system="Northstar", office=off, intake=start, dob=p["dob"], status=status,
                                 exit=end, transfer_from="", referral=p["referral"], pid=p["pid"]))
                prev = nref
            else:
                sysname = "CaseTrack" if start < K.MIGRATION else "Northstar"
                ref = old_ref(start) if sysname == "CaseTrack" else new_ref()
                rows.append(dict(ref=ref, system=sysname, office=off, intake=start,
                                 dob=ct_dob if sysname == "CaseTrack" else p["dob"], status=status, exit=end,
                                 transfer_from=prev or "", referral=p["referral"], pid=p["pid"]))
                prev = ref
    return rows


# ---------------------------------------------------------------------------------------------- the ledger
ACCOUNTS = ("Staff", "Mentor fees", "Bursaries", "Venues", "Transport", "Systems", "Professional services")


ACCRUAL_DRAW = 23
LEDGER_DRAW = 20


def accruing():
    """Which offices accrued their December mentor fees at year end (an office whose mentors' December invoices had
    not arrived when the year closed), by year."""
    r = K.rng("bridges-accruals", ACCRUAL_DRAW)
    out = {}
    for off, _, _ in OFFICES:
        years = [y for y in (2019, 2020, 2021, 2022) if r.random() < 0.5]
        out[off] = years or [int(r.choice([2019, 2020, 2021, 2022]))]
    return out


def ledger(P):
    r = K.rng("bridges-ledger", LEDGER_DRAW) if LEDGER_DRAW else K.rng("bridges-ledger")
    acc_years = accruing()
    lines = []
    jn = [0]

    def j():
        jn[0] += 1
        return "JE%06d" % (31800 + jn[0] * 7)

    active = {}
    for p in P:
        last = 60 if p["end"] is None else (p["end"].year - 2019) * 12 + p["end"].month
        for m in range((p["intake"].year - 2019) * 12 + p["intake"].month, min(last, 60) + 1):
            active.setdefault((p["office"], m), 0)
            active[(p["office"], m)] += 1
    for off, region, _ in OFFICES:
        base = (3000 + 18.0 * YOUNG[off]) * K.rng("office-size", K.CODES[K.NAMES.index(region)]).uniform(0.92, 1.08)
        for m in range(1, 61):
            y, mo = 2019 + (m - 1) // 12, (m - 1) % 12 + 1
            d = dt.date(y, mo, 1)
            n = active.get((off, m), 0)
            lines.append((d + dt.timedelta(days=27), off, "Staff", round(base * r.uniform(0.97, 1.03), 2), j(),
                          "Program staff %s %d" % (d.strftime("%b"), y)))
            if n:
                fee = round(120.0 * n * r.uniform(0.85, 1.15), 2)
                if mo == 12 and y in acc_years[off]:
                    lines.append((dt.date(y, 12, 31), off, "Mentor fees", fee, j(), "Year-end accrual, mentor fees"))
                    lines.append((dt.date(y + 1, 1, int(r.integers(9, 24))), off, "Mentor fees",
                                  round(fee * r.uniform(0.95, 1.05), 2), j(), "Mentor fees, December invoices"))
                else:
                    lines.append((d + dt.timedelta(days=int(r.integers(4, 20))), off, "Mentor fees", fee, j(),
                                  "Mentor fees"))
                lines.append((d + dt.timedelta(days=int(r.integers(10, 26))), off, "Bursaries",
                              round(85.0 * n * r.uniform(0.8, 1.2), 2), j(), "Bursary payments"))
            if r.random() < 0.45:
                lines.append((d + dt.timedelta(days=int(r.integers(1, 27))), off, "Venues",
                              round(r.uniform(220, 1400), 2), j(), "Room hire"))
            if r.random() < 0.6:
                lines.append((d + dt.timedelta(days=int(r.integers(1, 27))), off, "Transport",
                              round(r.uniform(90, 900), 2), j(), "Travel and bus passes"))
    # central cost centre
    for m in range(1, 61):
        y, mo = 2019 + (m - 1) // 12, (m - 1) % 12 + 1
        d = dt.date(y, mo, 1)
        lines.append((d + dt.timedelta(days=27), "CEN", "Staff", round(9850 * r.uniform(0.98, 1.02), 2), j(),
                      "Program manager and coordinator"))
        if mo in (3, 6, 9, 12):
            lines.append((d + dt.timedelta(days=15), "CEN", "Systems", round(r.uniform(1800, 4200), 2), j(),
                          "Case management licence and training"))
    for y in (2019, 2020, 2021, 2022):
        tot = sum(l[3] for l in lines if l[5] == "Year-end accrual, mentor fees" and l[0].year == y)
        lines.append((dt.date(y + 1, 1, 2), "CEN", "Mentor fees", -round(tot, 2), j(), "Reversal of %d year-end accruals" % y))
    lines.append((dt.date(2021, 5, 14), "CEN", "Systems", 18400.00, j(), "Northstar implementation"))
    # close-out, January to March 2024
    for off, _, _ in OFFICES:
        n = sum(1 for p in P if p["office"] == off and p["outcome"] == "Active")
        if n:
            lines.append((dt.date(2024, 2, int(r.integers(5, 26))), off, "Bursaries", round(150.0 * n * r.uniform(0.8, 1.2), 2), j(),
                          "Final bursaries, close-out"))
    lines.append((dt.date(2024, 3, 15), "CEN", "Professional services", 26500.00, j(), "Program evaluation, final report"))
    # journals are numbered as they are posted
    lines.sort(key=lambda l: (l[0], l[1] == "CEN", l[1], l[2], l[5]))
    rj = K.rng("journal-numbers")
    out, no = [], 31806
    for d, cc, acct, amt, _, desc in lines:
        no += 1 + (int(rj.integers(1, 4)) if rj.random() < 0.12 else 0)
        out.append((d, cc, acct, amt, "JE%06d" % no, desc))
    return out


# ---------------------------------------------------------------------------------------------- the golden asks
def truth_starts(P):
    return {o: sum(1 for p in P if p["office"] == o) for o, _, _ in OFFICES}


def truth_spending(lines, P):
    """Each region's spending: its office's lines with the year-end accruals taken back (the central reversals
    undo them), and the central lines other than the reversals shared by the young people each office started."""
    st = truth_starts(P)
    tot = sum(st.values())
    off = {o: 0.0 for o, _, _ in OFFICES}
    central = 0.0
    for d, cc, acct, amt, jn, desc in lines:
        if cc == "CEN":
            if not desc.startswith("Reversal of"):
                central += amt
        elif desc != "Year-end accrual, mentor fees":
            off[cc] += amt
    return {OFFICE_REGION[o]: off[o] + central * st[o] / tot for o in off}
