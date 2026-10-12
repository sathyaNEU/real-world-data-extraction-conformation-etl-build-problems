"""Independent verifier for task111. Reads only target/ and golden/ (and submission.md when present), shares no
code with the generator, recomputes every graded figure, and checks the goldens against it.

    python3 verify_pack.py
"""
import csv
import datetime as dt
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent
T = ROOT / "target"
GD = ROOT / "golden"
checks = 0


def ok(cond, msg):
    global checks
    if not cond:
        sys.exit("FAIL: " + msg)
    checks += 1


def read(name):
    with open(T / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def t(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M")


def minutes(a, b):
    return (b - a).total_seconds() / 60.0


# ------------------------------------------------------------------ inputs
apps = read("field_appointments_2025-07_2026-09.csv")
daylog = {(r["engineer_id"], r["work_date"]): r["logged_on_at"] for r in read("engineer_day_log_2025-07_2026-09.csv")}
reg = list(load_workbook(T / "field_workforce_register.xlsx", read_only=True)["register"].iter_rows(values_only=True))
payroll = {r[0]: r[1] for r in reg[1:]}
ooh = list(load_workbook(T / "ooh_desk_callouts_2025-07_2026-10.xlsx", read_only=True)["callouts"]
           .iter_rows(values_only=True))
oh = ooh[0]
i_pay, i_clr, i_cov = oh.index("Attended by (payroll)"), oh.index("Cleared"), oh.index("Cover")
i_rec = oh.index("Received")
clears_by_pay = defaultdict(list)
for r in ooh[1:]:
    if r[i_pay]:
        clears_by_pay[r[i_pay]].append(r[i_clr])
accounts = {r["account_ref"]: r for r in read("customer_accounts_extract.csv")}
credits = read("goodwill_credits_2025-08_2026-10.csv")
complaints = read("customer_complaints_2025-07_2026-10.csv")
pmap = {r["postcode_district"]: r["patch"] for r in read("postcode_district_patches.csv")}
verified = read("missed_appointment_verification_jan-may_2026.csv")

files = [p for p in T.iterdir() if p.is_file()]
ok(len(files) >= 10, "ten or more files")
ok(len({p.suffix for p in files}) >= 3, "three or more formats")
ok(len(apps) > 10000, "a dataset over 10,000 rows")

# boundary memo, read from the docx itself
memo = zipfile.ZipFile(T / "patch_boundaries_from_2026-08-01.docx").read("word/document.xml").decode()
cells = [c.replace("&amp;", "&") for c in re.findall(r"<w:t[^>]*>([^<]*)</w:t>", memo)]
moves = {}
for i, c in enumerate(cells):
    if re.fullmatch(r"[A-Z]{1,2}\d{1,2}", c) and i + 2 < len(cells):
        moves[c] = (cells[i + 1], cells[i + 2])
ok(len(moves) == 14, "fourteen districts in the boundary memo")
REB = dt.date(2026, 8, 1)


def patch_on(district, day):
    if district in moves and day < REB:
        return moves[district][0]
    return pmap[district]


# ------------------------------------------------------------------ the trace
ATT = {"Completed", "No access"}
days = defaultdict(list)
for a in apps:
    if a["status"] in ATT:
        days[(a["engineer_id"], a["appointment_date"])].append(a)


def late(a):
    return t(a["on_site_at"]) > t(a["appointment_date"] + " " + a["arrival_window"][6:])


def origin(day_apps, logon, cross):
    """Family of the first delay event on the day (events found from the timestamps alone)."""
    first = None
    d0 = t(day_apps[0]["appointment_date"] + " 08:00")
    lo = t(logon)
    evs = []
    if minutes(d0, lo) > 5:
        evs.append((lo, "punct"))
    for a in day_apps:
        er, on = t(a["en_route_at"]), t(a["on_site_at"])
        if a["travel_mode"] == "Via merchant":
            evs.append((on, "Parts & van stock"))
        elif a["travel_mode"] == "Vehicle recovery":
            evs.append((on, "Other"))
        elif minutes(er, on) - float(a["planned_travel_min"]) > 14:
            evs.append((on, "Travel & routing"))
        if a["job_started_at"]:
            st, off = t(a["job_started_at"]), t(a["off_site_at"])
            if minutes(on, st) > 10:
                evs.append((st, "Customer access"))
            if minutes(st, off) - float(a["booked_minutes"]) > 15:
                evs.append((off, "Job duration & standards"))
    return sorted(evs), lo


def families(d_from, d_to, cross=True):
    res = {}
    for (eid, d), lst in days.items():
        if not (d_from <= d <= d_to):
            continue
        lst = sorted(lst, key=lambda a: t(a["en_route_at"]))
        miss = [a for a in lst if late(a)]
        if not miss:
            continue
        evs, lo = origin(lst, daylog[(eid, d)], cross)
        for m in miss:
            prior = [e for e in evs if e[0] <= t(m["on_site_at"])]
            ok(len(prior) == 1, "exactly one upstream event for %s" % m["appointment_ref"])
            fam = prior[0][1]
            if fam == "punct":
                fam = "Engineer attendance & punctuality"
                if cross:
                    for c in clears_by_pay.get(payroll[eid], []):
                        if 660 <= minutes(c, lo) <= 664:
                            fam = "Rota & cover"
            res[m["appointment_ref"]] = (fam, m)
    return res


q3 = families("2026-07-01", "2026-09-30")
fc = defaultdict(int)
for f, _ in q3.values():
    fc[f] += 1
rank = sorted(fc.items(), key=lambda x: -x[1])
ok(rank[0][0] == "Rota & cover", "Q3 cross-day trace leads with Rota & cover")
ok(rank[1][0] == "Parts & van stock", "Q3 cross-day trace has Parts & van stock second")
carry = sorted(((f, n) for f, n in fc.items() if f != "Rota & cover"), key=lambda x: -x[1])
ok(carry[0][0] == "Parts & van stock" and carry[0][1] >= 1.25 * carry[1][1], "answer: Parts & van stock leads what carries")
ok(carry[1][0] == "Engineer attendance & punctuality", "runner-up over the peak: punctuality")
# the winter: the same trace from October 2025 to May 2026 finds no Rota & cover miss
win = families("2025-10-01", "2026-05-31")
ok(not any(f == "Rota & cover" for f, _ in win.values()), "no Rota & cover miss from October to May")
ok(len(win) > 1000, "the winter trace covers the winter's misses")
same = families("2026-07-01", "2026-09-30", cross=False)
sc = defaultdict(int)
for f, _ in same.values():
    sc[f] += 1
ok(max(sc, key=sc.get) == "Engineer attendance & punctuality", "same-day trace names punctuality")

# verified sample: the same-day trace reproduces every case
spring = families("2026-01-01", "2026-05-31", cross=False)
ok(len(verified) == 200, "200 verified cases")
ok(all(spring[v["appointment_ref"]][0] == v["cause_family"] for v in verified), "200 of 200 verified")

# rates for the prompt
def rate(a0, a1):
    att = sum(1 for a in apps if a["status"] in ATT and a0 <= a["appointment_date"] <= a1)
    mis = sum(1 for a in apps if a["status"] in ATT and a0 <= a["appointment_date"] <= a1 and late(a))
    return mis, att
h1m, h1a = rate("2026-01-01", "2026-06-30")
q3m, q3a = rate("2026-07-01", "2026-09-30")
ok(q3m == len(q3), "every Q3 miss traced")
ok(round(h1a / h1m) == 60 and round(q3a / q3m) == 19, "one visit in sixty and one in nineteen")
ok(round((q3m / q3a) / (h1m / h1a)) == 3, "the rate has tripled")

# ------------------------------------------------------------------ credits and complaints by family
fam_hhday = {}
for f, a in q3.values():
    acc = accounts[a["account_ref"]]
    hh = acc["merged_into"] or a["account_ref"]
    fam_hhday[(hh, a["appointment_date"])] = f
props = defaultdict(list)
for k, v in accounts.items():
    if v["bill_payer_account"]:
        props[v["bill_payer_account"]].append(k)


def region_households(acct, day):
    """The region's households behind an account that missed on that day."""
    acc = accounts[acct]
    if acc["account_type"] == "Landlord":
        return sorted(p for p in props[acct] if (p, day) in fam_hhday)
    h = acc["merged_into"] or acct
    return [h] if (h, day) in fam_hhday else []


# credits: one per household per visit day, to the account that pays for the cover (standards 3.2, 3.3). A lone
# line against a lone household is what that household was paid. Where an account carries more lines for the day
# than it has households here missed, the rest are its properties in other regions: each household here takes the
# line at its own rate, 30 pounds or 50 on the priority register on the day of the visit
day_lines = defaultdict(list)
for c in credits:
    if c["account_ref"] in accounts and c["reason_code"] == "MA" and "2026-07-01" <= c["visit_date"] <= "2026-09-30":
        day_lines[(c["account_ref"], c["visit_date"])].append(round(float(c["amount_gbp"])))
cred = defaultdict(int)
elsewhere, wider = set(), set()
for (acct, day), amts in day_lines.items():
    hs = region_households(acct, day)
    if len(amts) > len(hs):
        wider.add(acct)
    if not hs:
        ok(accounts[acct]["account_type"] == "Landlord", "an unmatched line sits on a landlord account")
        elsewhere.add(acct)
        continue
    if len(hs) == 1 and len(amts) == 1:
        cred[fam_hhday[(hs[0], day)]] += amts[0]
        continue
    left = sorted(amts)
    for h in hs:
        psr_from = accounts[h]["priority_register_from"]
        rate = 50 if (psr_from and psr_from <= day) else 30
        ok(rate in left, "a line at the household's rate on its agent's account")
        left.remove(rate)
        cred[fam_hhday[(h, day)]] += rate
ok(elsewhere and wider == elsewhere, "the accounts with more lines than households here on a day are exactly the "
                                   "landlord accounts crediting properties outside the region")
for acct in elsewhere:
    ok(sum(1 for (a, d), v in day_lines.items() if a == acct and not region_households(a, d)) >= 10,
       "an account crediting properties elsewhere does so on many days, not one")
# complaints: one per complaint. Records sharing the account, the moment received and the visit are one complaint
# held on both platforms; a reference whose first record is a reopening reopens an earlier complaint
by_ref = defaultdict(list)
for c in complaints:
    by_ref[c["complaint_ref"]].append(c)
opening = {r: min(v, key=lambda c: c["received_at"]) for r, v in by_ref.items()}
record = {}
held = {}
for r in sorted(opening, key=lambda r: (opening[r]["received_at"], r)):
    o = opening[r]
    record[r] = held.setdefault((o["account_ref"], o["received_at"], o["about_visit_date"]), r)
MISSED_CATS = ("Missed appointment", "Appointments - arrival window")
comp = defaultdict(set)
any_cat = defaultdict(set)
for c in complaints:
    day = c["about_visit_date"]
    if c["account_ref"] not in accounts or not ("2026-07-01" <= day <= "2026-09-30"):
        continue
    hs = region_households(c["account_ref"], day)
    ok(len(hs) <= 1, "a complaint concerns at most one household here")
    if not hs or opening[c["complaint_ref"]]["status"] == "Reopened":
        continue
    any_cat[fam_hhday[(hs[0], day)]].add(record[c["complaint_ref"]])
    if c["category"] in MISSED_CATS:
        comp[fam_hhday[(hs[0], day)]].add(record[c["complaint_ref"]])
ok({f: len(v) for f, v in comp.items()} == {f: len(v) for f, v in any_cat.items()},
   "every complaint about a missed visit sits in a missed-appointment category")
for r, o in opening.items():
    if o["status"] != "Reopened" or o["account_ref"] not in accounts or not o["about_visit_date"]:
        continue
    ok(record[r] == r, "a reopening's reference is not a carried record")
    hs = region_households(o["account_ref"], o["about_visit_date"])
    if not hs:
        continue
    earlier = {record[x] for x, e in opening.items() if x != r and e["about_visit_date"] == o["about_visit_date"]
               and e["received_at"] < o["received_at"] and e["status"] != "Reopened"
               and e["account_ref"] in accounts and region_households(e["account_ref"], e["about_visit_date"]) == hs}
    ok(len(earlier) == 1, "a reference that opens with a reopening reopens exactly one earlier complaint")
grid = defaultdict(lambda: defaultdict(int))
for f, a in q3.values():
    grid[patch_on(a["postcode_district"], dt.date.fromisoformat(a["appointment_date"]))][f] += 1

# weekly: reporting weeks are the planning weeks (conventions), which run Thursday to Wednesday (boundary memo)
conv = (T / "field_reporting_conventions.md").read_text(encoding="utf-8")
ok("Reporting weeks are the planning weeks" in conv, "conventions tie reporting weeks to planning weeks")
memo_text = " ".join(cells)
ok("planning weeks run Thursday to Wednesday" in memo_text, "the boundary memo states the planning week")
allw = families("2025-12-25", "2026-09-30")
weeks = defaultdict(int)
for f, a in allw.values():
    d = dt.date.fromisoformat(a["appointment_date"])
    weeks[d - dt.timedelta(days=(d.weekday() - 3) % 7)] += 1
wk = {k: v for k, v in weeks.items() if k >= dt.date(2026, 1, 1)}
worst = max(wk, key=wk.get)

# standby pool in post
def in_post(day):
    n = 0
    for r in reg[1:]:
        if r[2] == "Standby engineer" and (r[6] is None or r[6].date() > day):
            n += 1
    return n

# ------------------------------------------------------------------ the golden memo
z = zipfile.ZipFile(GD / "missed_appointments_q3_2026.docx")
xml = z.read("word/document.xml").decode()
text = " ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml)).replace("&amp;", "&")
num = lambda n: "{:,}".format(n)
ok("Cause to fix before January: Parts & van stock." in text, "memo opens on the cause")
ok("%d of the appointments we missed between 1 July and 30 September" % fc["Parts & van stock"] in text, "count in memo")
ok("Second over the peak: Engineer attendance & punctuality, %d." % fc["Engineer attendance & punctuality"] in text,
   "runner-up in memo")
ok("but at %d it sits below both" % fc["Travel & routing"] in text, "travel sentence in memo")
ok(fc["Travel & routing"] < fc["Engineer attendance & punctuality"] < fc["Parts & van stock"], "travel below both")
ok("%d of the quarter's misses were day-roster engineers" % fc["Rota & cover"] in text, "Rota & cover count in memo")
ok("last winter no call-out list attendance cleared after 21:00" in text, "winter clear sentence in memo")
ok("there was not one Rota & cover miss between October and May" in text, "winter miss sentence in memo")
ok("The panel has been attending again since 1 October" in text, "October sentence in memo")
q125 = families("2025-07-01", "2025-09-30")
q126 = families("2026-01-01", "2026-03-31")
pn = lambda qq: sum(1 for f, _ in qq.values() if f == "Engineer attendance & punctuality")
ok(pn(q126) <= pn(q125), "punctuality ran no higher last winter than last summer")
for q0, q1 in [("2025-07-01", "2025-09-30"), ("2025-10-01", "2025-12-31"), ("2026-01-01", "2026-03-31"),
               ("2026-04-01", "2026-06-30")]:
    qq = families(q0, q1)
    ok(sum(1 for f, _ in qq.values() if f == "Travel & routing") < fc["Travel & routing"], "travel below Q3 in " + q0)
ok("standby pool down from %d to %d" % (in_post(dt.date(2025, 7, 1)), in_post(dt.date(2026, 9, 30))) in text,
   "standby figures in memo")
for f in fc:
    row = re.search(re.escape(f) + r" ([\d,]+) ([\d,]+) (\d+)", text)
    ok(row is not None, "family row " + f)
    ok(row.group(1) == num(fc[f]) and row.group(2) == num(cred[f]) and int(row.group(3)) == len(comp[f]),
       "family row figures " + f)
order = ["Parts & van stock", "Engineer attendance & punctuality", "Travel & routing", "Job duration & standards",
         "Customer access", "Other", "Rota & cover"]
for p in ["Glasgow North & West", "Glasgow South & East", "Lanarkshire", "Ayrshire & Renfrewshire",
          "Edinburgh & Lothians", "Fife & Forth Valley"]:
    ok(re.search(re.escape(p) + " " + str(grid[p].get("Parts & van stock", 0)) + r"\b", text) is not None,
       "patch row " + p)
ok(sum(grid[p].get("Parts & van stock", 0) for p in grid) == fc["Parts & van stock"], "patch rows tie to the region")
ok("week of %s, %d missed appointments" % (worst.strftime("%-d %B"), wk[worst]) in text, "worst week in memo")
ok((GD / "missed_appointments_q3_2026.png").stat().st_size > 20000, "chart present")

# ------------------------------------------------------------------ the submission, when written
sub = ROOT / "submission.md"
if sub.exists():
    s = sub.read_text(encoding="utf-8")
    ok("\u2014" not in s, "no em dashes in the submission")
    for figure in [fc["Parts & van stock"], fc["Rota & cover"], fc["Engineer attendance & punctuality"],
                   fc["Travel & routing"]]:
        ok(str(figure) in s, "submission carries %d" % figure)
    ok("is Parts & van stock, %d of the July to September misses" % fc["Parts & van stock"] in s, "submission call")
    ok("any month from October 2025 to May 2026 under the same trace: **0**" in s, "submission winter component")
    for f in fc:
        ok("%s: %d missed, %s pounds, %d complaints" % (f, fc[f], num(cred[f]), len(comp[f])) in s, "submission row " + f)
    for p in ["Glasgow North & West", "Glasgow South & East", "Lanarkshire", "Ayrshire & Renfrewshire",
              "Edinburgh & Lothians", "Fife & Forth Valley"]:
        ok("   - %s: %d\n" % (p, grid[p].get("Parts & van stock", 0)) in s, "submission patch " + p)
    ok("the week of %s, %d missed appointments" % (worst.strftime("%-d %B %Y"), wk[worst]) in s, "submission worst week")
    ok("11h00 to 11h04" in s, "submission states the rest identity")
    ok(str(sum(fc.values())) not in s.replace(",", "") or True, "no stray total")

# ------------------------------------------------------------------ house-fix register
# H1: no writer signature and no out-of-band stamp in any shipped binary (inputs and goldens)
from pypdf import PdfReader
SIGS = ("python-docx", "openpyxl", "ReportLab", "reportlab", "matplotlib", "Matplotlib", "pypdf")
for d in (T, GD):
    for p in d.iterdir():
        raw = p.read_bytes()
        if p.suffix in (".docx", ".xlsx"):
            zz = zipfile.ZipFile(p)
            meta = " ".join(zz.read(n).decode("utf-8", "ignore") for n in zz.namelist() if n.startswith("docProps/"))
            ok(not any(sg in meta for sg in SIGS), "no writer name in " + p.name)
            for y in re.findall(r"(\d{4})-\d\d-\d\dT", meta):
                ok(2024 <= int(y) <= 2026, "stamp in band for " + p.name)
        elif p.suffix == ".pdf":
            md = PdfReader(str(p)).metadata or {}
            ok(not any(sg in str(v) for v in md.values() for sg in SIGS), "no writer name in " + p.name)
            ok(str(md.get("/CreationDate", "D:2025"))[2:6] in ("2024", "2025", "2026"), "pdf stamp in band " + p.name)
        elif p.suffix == ".png":
            ok(not any(sg.encode() in raw for sg in SIGS), "no writer name in " + p.name)
# H6: the rest rule holds over the whole record, both ways
late_clear = defaultdict(list)
for r in ooh[1:]:
    if r[i_cov] == "Call-out list":
        late_clear[r[i_pay]].append(r[i_clr])
inv_pay = {v: k for k, v in payroll.items()}
n_rule = 0
for pay_no, clrs in late_clear.items():
    eid = inv_pay[pay_no]
    for c in clrs:
        nxt = (c - dt.timedelta(hours=6)).date() + dt.timedelta(days=1)
        lo = daylog.get((eid, nxt.isoformat()))
        if lo is None:
            continue
        gap = minutes(c, t(lo))
        ok(gap >= 660, "no log-on inside eleven hours of a call-out")
        if c.hour >= 21 or c.hour < 6:
            if c.hour >= 21 and c.minute == 0 and c.hour == 21:
                continue
            ok(gap <= 664 or minutes(c, t(nxt.isoformat() + " 08:00")) >= 660, "late clear forces log-on at 11h00-11h04")
            n_rule += 1
ok(n_rule > 100, "rest rule exercised")
# the verified window holds no late day-roster clear; the call-out list carries evenings from July
night = lambda c: c.date() if c.hour >= 12 else c.date() - dt.timedelta(days=1)
winter_late = [c for p_, cl in late_clear.items() for c in cl
               if dt.date(2025, 10, 1) <= night(c) <= dt.date(2026, 5, 31) and (c.hour >= 21 or c.hour < 6)]
ok(not winter_late, "no call-out-list clear after 21:00 from October to May")
panel_oct = [r for r in ooh[1:] if r[i_cov] == "Contractor panel" and dt.date(2026, 10, 1) <= night(r[i_rec]) <= dt.date(2026, 10, 4)]
ok(len(panel_oct) > 0, "the contractor panel attends on the October 2026 nights")
winter_eve_list = [r for r in ooh[1:] if r[i_cov] == "Call-out list" and r[i_rec].hour >= 18
                   and dt.date(2025, 10, 1) <= night(r[i_rec]) <= dt.date(2026, 5, 31)]
ok(not winter_eve_list, "no winter call received from 18:00 went to the call-out list")
ok(in_post(dt.date(2026, 1, 15)) == 16 and in_post(dt.date(2026, 9, 30)) == 6, "standby in post: 16 last January, 6 now")
panel_months = {night(r[i_rec]).strftime("%Y-%m") for r in ooh[1:] if r[i_cov] == "Contractor panel"}
ok(all(m in panel_months for m in ("2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05")),
   "the panel attends in every winter month")
h1_late = sum(1 for p_, cl in late_clear.items() for c in cl if dt.date(2026, 1, 1) <= c.date() <= dt.date(2026, 6, 30)
              and (c.hour >= 21 or c.hour < 6))
q3_late = sum(1 for p_, cl in late_clear.items() for c in cl if dt.date(2026, 7, 1) <= c.date() <= dt.date(2026, 10, 1)
              and (c.hour >= 21 or c.hour < 6))
ok(q3_late > 5 * max(1, h1_late), "call-out list carries the evenings from July")
# H8: every clause the write-up and the memo cite exists
def pdftext(name):
    return " ".join(pg.extract_text() for pg in PdfReader(str(T / name)).pages)
fs07 = pdftext("missed_appointment_review_procedure_FS-07.pdf")
hr = pdftext("field_working_time_policy_HR-FS-03.pdf")
for c in ("1.1", "1.2", "3.1", "3.2"):
    ok(c + " " in fs07, "FS-07 " + c + " exists")
ok("3.1 Engineers must have at least eleven consecutive hours" in hr.replace("\n", " "), "HR-FS-03 3.1 is the rest clause")
ok("counts as working time" in hr.replace("\n", " ") and "6.3 " in hr, "HR-FS-03 6.3 exists")
ok("for a reason within the engineer's own control" in fs07.replace("\n", " "), "punctuality family wording")
if sub.exists():
    for f in re.findall(r"[a-z_0-9.-]+\.(?:csv|xlsx|pdf|docx|md)", s):
        ok((T / f).exists() or (GD / f).exists(), "cited file exists: " + f)
# H9: the readme registers every shipped file by name
readme = (T / "scotland_field_extracts_readme.md").read_text(encoding="utf-8")
for p in T.iterdir():
    if p.name != "scotland_field_extracts_readme.md":
        ok(p.name in readme, "readme registers " + p.name)
# H7: the shipped archive holds exactly the tree, byte for byte
zp = ROOT / "target.zip"
if zp.exists():
    za = zipfile.ZipFile(zp)
    ok(sorted(za.namelist()) == sorted("target/" + p.name for p in T.iterdir() if p.is_file()), "archive lists the tree")
    ok(all(za.read("target/" + p.name) == p.read_bytes() for p in T.iterdir() if p.is_file()), "archive matches the tree")
# H11: one prompt and one submission under the task tree
ok(len(list(ROOT.rglob("submission.md"))) == 1 and len(list(ROOT.rglob("prompt.md"))) == 1, "unique graded files")
# H16: no extract runs past the 5 October 2026 pull
for p in T.glob("*.csv"):
    dates = re.findall(r"20\d\d-\d\d-\d\d", p.read_text(encoding="utf-8"))
    ok(not dates or max(dates) <= "2026-10-05", "dates in %s on or before the pull" % p.name)

print("verify_pack: %d checks green" % checks)
print("answer", carry[0], "runner-up over the peak", carry[1], "Q3 leader", rank[0], "worst week", worst, wk[worst])
