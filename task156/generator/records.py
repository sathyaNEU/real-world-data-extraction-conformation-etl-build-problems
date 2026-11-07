"""task156: the pack's tabular files, written from the population (population.py) and the ask records (askdata.py)."""
import csv
import datetime as dt
import io

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import population as PO
import world as W

F_REG = "membership_register_extract_2026-11-02.csv"
F_INV = "online_vote_invitations_2022-2025.csv"
F_VOTES = "online_votes_2022-2025.csv"
F_SITES = "worksites_2026-11.csv"
F_DELEG = "delegate_register_2018-2028.xlsx"
F_ROUND = "bargaining_round_2027.xlsx"
F_REMIT = "payroll_remittance_advices_2025-26.csv"
F_DIARY = "organiser_diary_export_2025-26.csv"
F_SIGNIN = "regional_forum_signin_2025-26.csv"
F_WORKFORCE = "council_workforce_returns_2026.csv"
F_SURVEY = "member_survey_2024_results.xlsx"

LEGACY = {}   # council code -> employer label used before the July 2024 register migration
for code, name in W.NAME.items():
    base = name.replace(" Council", "")
    if base.endswith(" City"):
        LEGACY[code] = "City of " + base[:-5]
    elif base.endswith(" Rural City"):
        LEGACY[code] = "Rural City of " + base[:-11]
    else:
        LEGACY[code] = "Shire of " + base[:-6]
MIGRATION = dt.date(2024, 7, 1)


def write_csv(path, cols, rows, crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n" if crlf else "\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
        n += 1
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())
    return n


def d(x):
    return "" if x is None else x.isoformat()


def site_old(P):
    return {s["code"]: s["old"] for s in P.sites}


def register_rows():
    P = PO.build()
    old = site_old(P)
    rows = []
    for m in sorted(P.members, key=lambda m: m["no"]):
        legacy = m["cease"] is not None and m["cease"] < MIGRATION
        rows.append([m["no"], LEGACY[m["council"]] if legacy else W.NAME[m["council"]],
                     old[m["site"]] if legacy else m["site"], m["dob"].isoformat(), m["gender"], m["join"].isoformat(),
                     d(m["cease"]), m["emp"], "Band %d" % m["band"], m["pay"].title() if m["pay"] != "payroll"
                     else "Payroll deduction"])
    return rows


REG_COLS = ["member_no", "employer", "worksite", "date_of_birth", "gender", "joined", "ceased", "employment",
            "classification", "dues_method"]


def utc(local, off):
    return (local - dt.timedelta(hours=off)).strftime("%Y-%m-%dT%H:%M:%SZ")


def invitation_rows():
    P = PO.build()
    rows = []
    for r in P.inv:
        rows.append([r["vote"], "INV%07d" % (r["seq"] + 3000000), r["member"], r["channel"].replace("sms", "SMS"),
                     utc(r["sent_local"], r["off"]), "" if r["cast_local"] is None else utc(r["cast_local"], r["off"])])
    return rows


INV_COLS = ["vote_id", "invitation_id", "member_no", "channel", "sent_utc", "voted_utc"]


def vote_rows():
    return [[v[0], v[1], v[2].strftime("%Y-%m-%d %H:%M"), v[3].strftime("%Y-%m-%d %H:%M"), "Australia/Melbourne",
             "All financial members with an email address or mobile number on file"] for v in W.VOTES]


VOTE_COLS = ["vote_id", "title", "opens_local", "closes_local", "time_zone", "eligible"]


def site_rows():
    P = PO.build()
    return [[s["code"], s["old"], W.NAME[s["council"]], s["name"]] for s in P.sites]


SITE_COLS = ["worksite_code", "code_before_2024_07", "council", "worksite"]


def _sheet(ws, cols, rows, widths=None):
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="D9E1F2")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, wd in enumerate(widths or [], start=1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A2"


def write_delegates(path):
    P = PO.build()
    old = site_old(P)
    sitename = {s["code"]: s["name"] for s in P.sites}
    wb = Workbook()
    first = True
    for term in reversed(W.TERMS):
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = "%d-%02d" % (term, (term + 2) % 100)
        rows = []
        for r in sorted([x for x in P.deleg if x["term"] == term], key=lambda x: (W.NAME[x["council"]], x["site"],
                                                                                   x["role"] != "Senior delegate")):
            sc = r["site"] if term >= 2024 else old[r["site"]]
            rows.append([W.NAME[r["council"]] if term >= 2024 else LEGACY[r["council"]], sc, sitename[r["site"]],
                         r["member"], r["role"], r["status"], r["elected"], r["start"], r["end"]])
        _sheet(ws, ["Council", "Worksite code", "Worksite", "Member no", "Role", "Election", "Declared", "Term starts",
                    "Term ends"], rows, [30, 13, 34, 11, 15, 11, 12, 12, 12])
        for row in ws.iter_rows(min_row=2, min_col=7, max_col=9):
            for c in row:
                c.number_format = "dd/mm/yyyy"
    wb.save(path)
    return sum(1 for _ in P.deleg)


def write_survey(path):
    """The branch's 2024 member survey, results by council (unused by the solution)."""
    rng = np.random.default_rng(W.SEED + 9)
    P = PO.build()
    wb = Workbook()
    ws = wb.active
    ws.title = "Results by council"
    rows = []
    for code in W.CODES:
        n = sum(1 for m in P.members if m["council"] == code and PO.active(m, dt.date(2024, 9, 1)))
        resp = int(n * float(rng.uniform(0.12, 0.24)))
        rows.append([W.NAME[code], resp, round(float(rng.uniform(58, 81)), 1), round(float(rng.uniform(44, 72)), 1),
                     round(float(rng.uniform(51, 77)), 1), round(float(rng.uniform(30, 55)), 1)])
    _sheet(ws, ["Council", "Responses", "Satisfied with the union's service (%)",
                "Rate workload as a top bargaining issue (%)", "Rate pay as the top bargaining issue (%)",
                "Read the branch newsletter monthly (%)"], rows, [32, 11, 18, 18, 18, 18])
    ws2 = wb.create_sheet("Notes")
    ws2.append(["Online survey of members, 2 to 27 September 2024. Results are unweighted shares of the members "
                "who responded at each council."])
    wb.save(path)
    return len(rows)


def write_round(path):
    """The 2027 bargaining round: each council's agreement, its nominal expiry and where bargaining stands."""
    rng = np.random.default_rng(W.SEED + 7)
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 round"
    rows = []
    for code in W.CANDIDATES:
        y = 2026 if rng.uniform() < 0.35 else 2027
        exp = dt.date(y, int(rng.choice([6, 9, 12])) if y == 2026 else int(rng.choice([3, 6])), 30) \
            if True else None
        if exp.month in (9,):
            exp = dt.date(exp.year, 9, 30)
        notice = exp - dt.timedelta(days=int(rng.integers(90, 160)))
        if notice > dt.date(2026, 10, 30):
            notice = dt.date(2026, 10, int(rng.integers(1, 29)))
        meetings = int(rng.integers(2, 9))
        rows.append([W.NAME[code], "%s Enterprise Agreement %d" % (W.NAME[code].replace(" Council", ""), exp.year - 3),
                     exp, notice, meetings, "Bargaining" if meetings > 2 else "Claims served"])
    _sheet(ws, ["Council", "Agreement", "Nominal expiry", "Notice of representational rights", "Meetings held to 31 Oct 2026",
                "Status"], rows, [32, 44, 14, 16, 14, 14])
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=4):
        for c in row:
            c.number_format = "dd/mm/yyyy"
    ws2 = wb.create_sheet("Outside the round")
    rows2 = [[W.NAME[c], "Agreement runs to 2028 or later"] for c in W.CODES if c not in W.CANDIDATES]
    _sheet(ws2, ["Council", "Note"], rows2, [32, 40])
    wb.save(path)
    return len(rows)
