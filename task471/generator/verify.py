"""The independent verifier: reads only the shipped pack (target/), the golden files and submission.md, and by its own
code rebuilds each cell's dual-system estimate from the census workbook and the survey's two person files, the
population on census day from the births, deaths and long-term movements by year of birth, the men's correction, the
regions' adults less their electors, the 200 organisers by largest remainders, and the two counts from the roll's
transaction log; then compares them with the golden CSV and submission.md. It imports nothing from the generator.

    python3 task471/generator/verify.py
"""
import csv
import datetime as dt
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

import docx
import openpyxl

TOTAL, FLOOR = 200, 2
GROUPS = [(0, 14), (15, 17), (18, 24), (25, 34), (35, 49), (50, 64), (65, 200)]
YOUNG = [(18, 24), (25, 34), (35, 49)]
BEFORE_CENSUS = 62.0 / 365.0          # 1 January to 3 March of a year of birth
COUNTRY = ZoneInfo("Pacific/Auckland")
FIRST, LAST = dt.date(2025, 3, 5), dt.date(2026, 6, 30)


def find(target, pattern):
    hits = [f for f in os.listdir(target) if re.search(pattern, f)]
    assert len(hits) == 1, (pattern, hits)
    return os.path.join(target, hits[0])


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def group(age):
    return next(g for g in GROUPS if g[0] <= age <= g[1])


def dse_cells(target):
    """(region, sex, group) -> dual-system estimate"""
    wb = openpyxl.load_workbook(find(target, r"^census_2025_usual_residents_by_region\.xlsx$"), read_only=True)
    count = {}
    for ws in wb.worksheets:
        if not re.match(r"^\d\d ", ws.title):
            continue
        reg = ws.title[:2]
        for r in ws.iter_rows(values_only=True):
            if r[0] is None or not (isinstance(r[0], int) or r[0] == "100 and over"):
                continue
            age = 100 if r[0] == "100 and over" else r[0]
            for sex, cnt, imp in (("M", r[1], r[2]), ("F", r[3], r[4])):
                k = (reg, sex, group(age))
                c = count.setdefault(k, [0, 0])
                c[0] += cnt
                c[1] += imp
    e, p = {}, {}
    for r in rows(find(target, r"^pes_2025_census_records\.csv$")):
        k = (r["REGION"], r["SEX"], group(int(r["AGE"])))
        v = e.setdefault(k, [0, 0])
        v[0] += 1
        v[1] += r["STATUS"] == "C"
    for r in rows(find(target, r"^pes_2025_people\.csv$")):
        k = (r["REGION"], r["SEX"], group(int(r["AGE"])))
        v = p.setdefault(k, [0, 0])
        v[0] += 1
        v[1] += r["MATCH"] == "M"
    return {k: (cnt - imp) * e[k][1] / e[k][0] * p[k][0] / p[k][1] for k, (cnt, imp) in count.items()}, count


def population(target):
    """(sex, age) -> people on census day: each year of birth's births less its deaths and departures plus its arrivals,
    aged at census day (62 of 365 born before 4 March); the 2025 period's births aged 0"""
    def period(s):
        return "Q" if s.startswith("2025-01-01/") else int(s)
    coh, q_births = {}, {}
    for r in rows(find(target, r"^live_births_by_sex_\d+_\d+\.csv$")):
        if period(r["PERIOD"]) == "Q":
            q_births[r["SEX"]] = int(r["LIVE_BIRTHS"])
        else:
            coh[(r["SEX"], int(r["PERIOD"]))] = coh.get((r["SEX"], int(r["PERIOD"])), 0) + int(r["LIVE_BIRTHS"])
    wb = openpyxl.load_workbook(find(target, r"^deaths_by_year_of_birth_\d+_\d+\.xlsx$"), read_only=True)
    for sex, title in (("M", "Males"), ("F", "Females")):
        head = None
        for r in wb[title].iter_rows(values_only=True):
            if head is None:
                if r[0] == "Year of death":
                    head = r
                continue
            if not isinstance(r[0], int):
                continue
            for c, v in zip(head[1:], r[1:]):
                if v:
                    coh[(sex, int(c))] = coh.get((sex, int(c)), 0) - v
    for r in rows(find(target, r"^deaths_by_year_of_birth_\d+_\d+\.csv$")):
        k = (r["SEX"], int(r["YEAR_OF_BIRTH"]))
        coh[k] = coh.get(k, 0) - int(r["DEATHS"])
    for r in rows(find(target, r"^long_term_movements_by_year_of_birth_\d+_\d+\.csv$")):
        k = (r["SEX"], int(r["YEAR_OF_BIRTH"]))
        coh[k] = coh.get(k, 0) + int(r["ARRIVALS"]) - int(r["DEPARTURES"])
    pop = {}
    for (sex, c), n in coh.items():
        for share, age in ((1 - BEFORE_CENSUS, 2024 - c), (BEFORE_CENSUS, 2025 - c)):
            if age >= 0:
                pop[(sex, min(age, 100))] = pop.get((sex, min(age, 100)), 0) + n * share
    for sex, n in q_births.items():
        pop[(sex, 0)] = pop.get((sex, 0), 0) + n
    return pop


def shares(gap):
    fixed = {}
    while True:
        free = [c for c in gap if c not in fixed]
        left = TOTAL - sum(fixed.values())
        g = sum(gap[c] for c in free)
        quota = {c: gap[c] * left / g for c in free}
        low = [c for c in free if quota[c] < FLOOR]
        if not low:
            break
        fixed.update({c: FLOOR for c in low})
    out = dict(fixed)
    out.update({c: int(quota[c]) for c in free})
    for c in sorted(free, key=lambda c: (int(quota[c]) - quota[c], c))[:left - sum(int(quota[c]) for c in free)]:
        out[c] += 1
    return out


def country_date(row):
    """a stamp with its UTC mark (Z) in the country's time; an unmarked stamp is the country's time as written"""
    t = dt.datetime.strptime(row["PROCESSED"].replace("T", " ").rstrip("Z"), "%Y-%m-%d %H:%M:%S")
    if row["PROCESSED"].endswith("Z"):
        t = t.replace(tzinfo=dt.timezone.utc).astimezone(COUNTRY)
    return t.date(), t.replace(tzinfo=None)


def asks(target, region_now, region_then):
    """the old platform's (R25-) electorate numbers are those of the 2023 general election's roll; a person is an elector
    number and a record a record reference; a person was on the roll at the close of census day if a removal in the
    window took off a record nothing in the window had put on the roll; each person not on it whom an accepted enrolment
    or reinstatement put on the roll in the window counts once, at the address of the first; a removal was reversed by a
    later accepted reinstatement of its record or a later accepted enrolment naming it, anywhere in the extract"""
    log = rows(find(target, r"^roll_transactions_\d+_\d+\.csv$"))
    region = lambda r: (region_then if r["TXN_ID"].startswith("R25-") else region_now)[r["ELECTORATE"]]
    timed = sorted((country_date(r)[1], i, r) for i, r in enumerate(log))
    window = [(t, r) for t, i, r in timed if FIRST <= t.date() <= LAST and r["STATUS"] == "A"]
    put_on, before, first = set(), set(), {}
    for t, r in window:
        if r["TXN_TYPE"] == "DEL" and r["RECORD_REF"] not in put_on:
            before.add(r["ELECTOR_NO"])
        if r["TXN_TYPE"] in ("NEW", "REI"):
            put_on.add(r["RECORD_REF"])
            first.setdefault(r["ELECTOR_NO"], r)
    new = {}
    for who, r in first.items():
        if who not in before and r["ADDRESS_TYPE"] == "R":
            new[region(r)] = new.get(region(r), 0) + 1
    later = {}
    for t, i, r in timed:
        if r["STATUS"] != "A":
            continue
        if r["TXN_TYPE"] == "REI":
            later.setdefault(("record", r["RECORD_REF"]), []).append(t)
        if r["TXN_TYPE"] in ("REI", "NEW") and r["CORRECTS_TXN"]:
            later.setdefault(("named", r["CORRECTS_TXN"]), []).append(t)
    died = {}
    for t, r in window:
        codes = ("01",) if r["TXN_ID"].startswith("R25-") else ("11", "12")
        if r["TXN_TYPE"] != "DEL" or r["REASON"] not in codes:
            continue
        if any(u > t for u in later.get(("record", r["RECORD_REF"]), []) + later.get(("named", r["TXN_ID"]), [])):
            continue
        died[region(r)] = died.get(region(r), 0) + 1
    return new, died


def main(target, gdir, quiet=False):
    ok = True

    def check(cond, msg):
        nonlocal ok
        if not cond:
            ok = False
            print("VERIFY FAIL:", msg)

    est, count = dse_cells(target)
    pop = population(target)
    fac = {}
    for g in YOUNG:
        m_da = sum(pop.get(("M", a), 0) for a in range(g[0], g[1] + 1))
        f_da = sum(pop.get(("F", a), 0) for a in range(g[0], g[1] + 1))
        m = sum(v for (c, s, gg), v in est.items() if s == "M" and gg == g)
        f = sum(v for (c, s, gg), v in est.items() if s == "F" and gg == g)
        fac[g] = (m_da / f_da) / (m / f)
    conc = {r["ELECTORATE"]: r for r in rows(find(target, r"^electorates_and_regions\.csv$"))}
    region_of = {k: r["REGION"] for k, r in conc.items()}
    region_then = {r["ELECTORATE"]: r["REGION"]
                   for r in rows(find(target, r"^roll_at_2023_general_election_by_electorate\.csv$"))}
    names = {r["REGION"]: r["REGION_NAME"] for r in conc.values()}
    roll = {c: 0 for c in names}
    for r in rows(find(target, r"^roll_at_close_of_census_day_2025\.csv$")):
        if r["ADDRESS_TYPE"] == "R":
            roll[region_of[r["ELECTORATE"]]] += int(r["ELECTORS"])
    adults, dse_adults, counted = {c: 0.0 for c in names}, {c: 0.0 for c in names}, {c: 0 for c in names}
    for (c, s, g), v in est.items():
        if g[0] >= 18:
            adults[c] += v * (fac[g] if s == "M" and g in fac else 1.0)
            dse_adults[c] += v
            counted[c] += count[(c, s, g)][0]
    org = shares({c: adults[c] - roll[c] for c in names})
    dse_org = shares({c: dse_adults[c] - roll[c] for c in names})
    census_org = shares({c: counted[c] - roll[c] for c in names})
    new, died = asks(target, region_of, region_then)
    # the documents the call and the asks lean on, read back
    plan = " ".join(" ".join(p.text for p in docx.Document(find(target, r"^enrolment_campaign_plan_2027\.docx$")).paragraphs).split())
    check("whether or not the census counted them" in plan and "Overseas electors are not counted in any region." in plan
          and "200 field organisers" in plan, "the plan files the population, the roll and the organisers")
    report = " ".join(subprocess.run(["pdftotext", "-raw", find(target, r"^pes_2025_methods_report\.pdf$"), "-"],
                                     capture_output=True, text=True, check=True).stdout.split())
    check("region by sex by age group" in report and "except the records the census imputed" in report,
          "the methods report files the cells and the records file's scope")
    mig = " ".join(subprocess.run(["pdftotext", "-raw", find(target, r"^roll_platform_migration_notes\.pdf$"), "-"],
                                  capture_output=True, text=True, check=True).stdout.split())
    check("01 deceased" in mig, "the migration notes file the old platform's death code")
    code_list = {(r["FIELD"], r["CODE"]): r["MEANING"] for r in rows(find(target, r"^roll_transaction_codes\.csv$"))}
    check(code_list[("REASON", "11")].startswith("Deceased") and code_list[("REASON", "12")].startswith("Deceased")
          and code_list[("TXN_TYPE", "REI")] == "Reinstatement of a removed elector"
          and "code list" in mig, "the code list files the new platform's death codes and the reinstatement")
    wb = openpyxl.load_workbook(find(target, r"^enrolment_gap_file_specification\.xlsx$"), read_only=True)
    spec = " ".join(str(v) for ws in wb.worksheets for r in ws.iter_rows(values_only=True) for v in r if v is not None)
    check("Dates and times are the country's time, which is 12 hours ahead of UTC" in spec and "each person once" in spec,
          "the specification files the window's clock, its offset from UTC and the count of people")
    # against the golden CSV
    gold = rows(os.path.join(gdir, "enrolment_gap_allocation_2027.csv"))
    check([g["REGION_CODE"] for g in gold] == sorted(names) and len(gold) == 16, "16 regions in code order")
    for g in gold:
        c = g["REGION_CODE"]
        check(g["REGION"] == names[c], "%s name" % c)
        check(int(g["ORGANISERS"]) == org[c], "%s organisers %s against %d" % (c, g["ORGANISERS"], org[c]))
        check(int(g["NEW_ELECTORS"]) == new.get(c, 0), "%s new electors %s against %d" % (c, g["NEW_ELECTORS"], new.get(c, 0)))
        check(int(g["REMOVED_DIED"]) == died.get(c, 0), "%s deaths %s against %d" % (c, g["REMOVED_DIED"], died.get(c, 0)))
    check(sum(org.values()) == TOTAL, "200 organisers")
    # against submission.md
    sub = open(os.path.join(os.path.dirname(gdir), "submission.md"), encoding="utf-8").read()
    rec = sub.split("## 1. Final Recommendation")[1].split("## 2.")[0]
    call = rec.split("**")[1]
    for c in sorted(names):
        check(re.search(r"\b%s %d\b" % (re.escape(names[c]), org[c]), call) is not None, "the call names %s %d" % (
            names[c], org[c]))
    changed = [c for c in sorted(names) if dse_org[c] != org[c]]
    rival = rec.split("Not the dual-system estimates as they stand, which give ")[1].split(";")[0]
    check(all(re.search(r"\b%s %d\b" % (re.escape(names[c]), dse_org[c]), rival) for c in changed)
          and len(re.findall(r"\d+", rival)) == len(changed), "the rival clause names the default path's %d regions" % len(
              changed))
    check("change %d regions" % sum(1 for c in names if census_org[c] != org[c]) in rec, "the census counts' rival")
    elect = sum(roll.values())
    check("**{:,}**".format(elect) in sub and "about **%.2f million**" % (sum(dse_adults.values()) / 1e6) in sub,
          "the electors and the dual-system adults")
    check("about **%.2f million**" % (sum(adults.values()) / 1e6) in sub, "the corrected adults")
    for c in sorted(names):
        line = re.search(r"^   - %s \(%s\): (\d+) organisers, ([\d,]+) added, ([\d,]+) removed because they had died$" % (
            re.escape(names[c]), c), sub, re.M)
        check(line is not None and int(line.group(1)) == org[c] and int(line.group(2).replace(",", "")) == new.get(c, 0)
              and int(line.group(3).replace(",", "")) == died.get(c, 0), "submission line for %s" % names[c])
    if not quiet:
        print("verify: %s; organisers %s; %d new electors, %d removed because they had died" % (
            "PASS" if ok else "FAIL", " ".join("%s %d" % (names[c], org[c]) for c in sorted(names)),
            sum(new.values()), sum(died.values())))
    return ok


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
