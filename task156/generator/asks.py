"""task156: the asks recomputed from the shipped pack, with the handlings the ceiling sheet prices.

Ask A, dues each council's payroll deducted for the branch for pay periods ending 1 July 2025 to 30 June 2026 (whole
dollars). Golden: one copy of each advice; the shared bureau's payments split by its statements; each run placed by its
pay period, an advice dated on a Thursday (the regional payroll platform's pay day, four days after the Sunday period
end) moved back to its period end.

Ask B, organiser hours at each council in 2025-26 (whole hours). Golden: travel and administration out; one row per
organiser, invitation and day, the last updated (the calendar keeps a superseded booking's row when it is
rescheduled); a regional forum's hours shared across councils by the delegates who signed in from each."""
import csv
import datetime as dt
import os
import re
import subprocess

FY0, FY1 = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
F_REMIT = "payroll_remittance_advices_2025-26.csv"
F_BUREAU = "western_shires_payroll_statements_2025-26.pdf"
F_DIARY = "organiser_diary_export_2025-26.csv"
F_SIGNIN = "regional_forum_signin_2025-26.csv"
F_REG = "membership_register_extract_2026-11-02.csv"
F_SITES = "worksites_2026-11.csv"
BUREAU = "Western Shires Payroll Services"
F_ROUND = "bargaining_round_2027.xlsx"


def councils(target):
    """The councils in the 2027 round (the tracker's '2027 round' sheet)."""
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, F_ROUND), read_only=True)["2027 round"]
    return sorted(r[0] for i, r in enumerate(ws.iter_rows(values_only=True)) if i > 0 and r[0])


def bureau_split(target):
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(target, F_BUREAU), "-"], capture_output=True,
                         text=True, check=True).stdout
    out = []
    for m in re.finditer(r"(\d{2})/(\d{2})/(\d{4})\s+(.+?Council)\s+(\d+)\s+([\d,]+\.\d{2})", txt):
        out.append((dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))), m.group(4).strip(),
                    float(m.group(6).replace(",", ""))))
    return out


def ask_a(target, dedup=True, split=True, payday=True):
    rows = list(csv.DictReader(open(os.path.join(target, F_REMIT), encoding="utf-8")))
    if dedup:
        seen, keep = set(), []
        for r in rows:
            if r["advice_no"] in seen:
                continue
            seen.add(r["advice_no"])
            keep.append(r)
        rows = keep
    tot = {c: 0.0 for c in councils(target)}
    for r in rows:
        d = dt.date.fromisoformat(r["period_end"])
        if r["employer"] == BUREAU:
            continue
        if payday and d.weekday() == 3:
            d = d - dt.timedelta(days=4)
        if FY0 <= d <= FY1 and r["employer"] in tot:
            tot[r["employer"]] += float(r["amount"])
    if split:
        for d, c, amt in bureau_split(target):
            if FY0 <= d <= FY1 and c in tot:
                tot[c] += amt
    return {c: round(v, 2) for c, v in tot.items()}


def _hours(r):
    a = dt.datetime.strptime(r["starts"], "%H:%M")
    b = dt.datetime.strptime(r["ends"], "%H:%M")
    return (b - a).total_seconds() / 3600.0


def ask_b(target, key=("invitation_uid", "organiser", "date"), forums="signin"):
    """key: the identity one diary event has (None keeps every row)."""
    rows = [r for r in csv.DictReader(open(os.path.join(target, F_DIARY), encoding="utf-8"))
            if r["activity"] not in ("Travel", "Administration")
            and FY0 <= dt.date.fromisoformat(r["date"]) <= FY1]
    if key:
        best = {}
        for r in rows:
            k = tuple(r[x] for x in key)
            if k not in best or r["last_updated_utc"] > best[k]["last_updated_utc"]:
                best[k] = r
        rows = list(best.values())
    tot = {c: 0.0 for c in councils(target)}
    forum_h = {}
    for r in rows:
        if r["activity"] == "Regional delegates forum":
            forum_h[r["date"]] = forum_h.get(r["date"], 0.0) + _hours(r)
        elif r["council"] in tot:
            tot[r["council"]] += _hours(r)
    if forums == "signin":
        mem = {}
        for r in csv.DictReader(open(os.path.join(target, F_REG), encoding="utf-8")):
            mem[r["member_no"]] = r
        sites = {}
        for r in csv.DictReader(open(os.path.join(target, F_SITES), encoding="utf-8")):
            sites[r["worksite_code"]] = r["council"]
            sites[r["code_before_2024_07"]] = r["council"]
        by = {}
        for r in csv.DictReader(open(os.path.join(target, F_SIGNIN), encoding="utf-8")):
            c = sites[mem[r["member_no"]]["worksite"]]
            by.setdefault(r["forum_date"], {}).setdefault(c, 0)
            by[r["forum_date"]][c] += 1
        for d, h in forum_h.items():
            n = sum(by[d].values())
            for c, k in by[d].items():
                if c in tot:
                    tot[c] += h * k / n
    return {c: round(v, 4) for c, v in tot.items()}


def rnd(x):
    return int(x + 0.5)
