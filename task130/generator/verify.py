"""Independent recomputation of task130's graded figures from target/ and golden/ alone.

Shares no code with the generator: it parses the CSVs with the csv module, sums in Decimal, and applies its own
reading of the readme and Schedule C (replacements drop the claims they name, voids and reversals net by sign,
denied lines carry nothing, a member month is a month whose first day the member is covered, a claim belongs to the
month of its first date of service or fill date, and a PBM row belongs to the member who held its employee number and
person code on the fill date). It then checks the golden workbook, the memo and, when present, submission.md block 4
against what it computed.

    python3 verify.py [TASK_DIR]
"""
import csv
import datetime as dt
import os
import re
import sys
from collections import defaultdict
from decimal import Decimal

from openpyxl import load_workbook

TASK = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TGT = os.path.join(TASK, "target")
GLD = os.path.join(TASK, "golden")


def iso(s):
    return dt.date(int(s[0:4]), int(s[5:7]), int(s[8:10]))


def ymd(s):
    return dt.date(int(s[0:4]), int(s[4:6]), int(s[6:8]))


def first_days(a, b):
    y, m = a.year, a.month
    while True:
        d = dt.date(y, m, 1)
        if d > b:
            return
        if d >= a:
            yield d
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def rows(name):
    with open(os.path.join(TGT, name), newline="") as f:
        return list(csv.DictReader(f))


cover = defaultdict(list)
code_spans = defaultdict(list)
for r in rows("eligibility_spans_2027-02.csv"):
    start = iso(r["span_start"])
    end = iso(r["span_end"]) if r["span_end"] else dt.date(9999, 12, 31)
    cover[r["member_id"]].append((start, end))
    code_spans[(int(r["employee_number"]), r["person_code"])].append((start, end, r["member_id"]))


def member_on(cardholder, code, day):
    """the member who carried this employee number and person code on the day of the fill"""
    hit = {m for s, e, m in code_spans[(cardholder, code)] if s <= day <= e}
    assert len(hit) == 1, ("PBM row links to one member", cardholder, code, day, hit)
    return hit.pop()


def member_months(member, a, b):
    return sum(1 for d in first_days(a, b) if any(s <= d <= e for s, e in cover[member]))


med_lines = rows("medical_claim_lines_2025-01_2027-02.csv")
replaced = {r["original_claim_number"] for r in med_lines if r["claim_frequency_code"] == "7"}
med = defaultdict(Decimal)
for r in med_lines:
    if r["claim_number"] in replaced or not r["allowed_amount"]:
        continue
    med[(r["member_id"], iso(r["first_date_of_service"]))] += Decimal(r["allowed_amount"])
rx = defaultdict(Decimal)
for r in rows("pharmacy_claims_2025-01_2027-02.csv"):
    d = ymd(r["DATE_OF_SERVICE"])
    m = member_on(int(r["CARDHOLDER_ID"]), r["PERSON_CD"], d)
    rx[(m, d)] += Decimal(r["GROSS_AMT_DUE"])
by_member_med, by_member_rx = defaultdict(list), defaultdict(list)
for (m, d), v in med.items():
    by_member_med[m].append((d, v))
for (m, d), v in rx.items():
    by_member_rx[m].append((d, v))

prior = {}
for r in rows("tpa_conversion_crosswalk_2025-01-01.csv"):
    prior["%s-%s" % (r["prior_subscriber_number"], r["prior_member_suffix"])] = r["member_id"]


def vendor_list(name, key):
    """members by risk tier, identified by the column named `key`"""
    ws = load_workbook(os.path.join(TGT, name), read_only=True, data_only=True)["Members"]
    out = defaultdict(list)
    head = None
    for row in ws.iter_rows(values_only=True):
        if head is None:
            head = list(row)
            continue
        if row[0] is not None:
            out[int(row[head.index("Risk tier")])].append(str(row[head.index(key)]))
    return out


bid = vendor_list("northcourt_rfp_2025-07_stratification_2024_claims.xlsx", "Bramwell member no.")
fin = vendor_list("northcourt_stratification_2026_claims_final.xlsx", "Member ID")
bid = {t: [prior[x] for x in xs] for t, xs in bid.items()}
draft = vendor_list("northcourt_stratification_2026_claims_draft.xlsx", "Member ID")
# every member on each list is enrolled on the date its cover gives (an open span covers 1 March 2027)
for name, lst, day in (("RFP 2025-07 list", bid, dt.date(2025, 1, 1)), ("draft list", draft, dt.date(2027, 1, 1)),
                       ("final list", fin, dt.date(2027, 3, 1))):
    for xs in lst.values():
        for m in xs:
            assert any(s <= day <= e for s, e in cover[m]), ("member not enrolled on the list's date", name, m, day)


def pmpm(members, a, b):
    s_med = sum((v for m in members for d, v in by_member_med[m] if a <= d <= b), Decimal(0))
    s_rx = sum((v for m in members for d, v in by_member_rx[m] if a <= d <= b), Decimal(0))
    mm = sum(member_months(m, a, b) for m in members)
    return s_med / mm, s_rx / mm


TM, TR = Decimal("1.065") ** 2, Decimal("1.09") ** 2
A0, A1 = dt.date(2025, 4, 1), dt.date(2026, 3, 31)
Y0, Y1 = dt.date(2026, 1, 1), dt.date(2026, 12, 31)
tiers = sorted(fin)
n = {t: len(fin[t]) for t in tiers}
assert sum(n.values()) == 140 and sum(len(v) for v in bid.values()) == 140
base, y26 = {}, {}
for t in tiers:
    am, ar = pmpm(bid[t], A0, A1)
    base[t] = (am * TM, ar * TR)
    y26[t] = pmpm(fin[t], Y0, Y1)
prog_m = sum(n[t] * base[t][0] for t in tiers) / 140
prog_r = sum(n[t] * base[t][1] for t in tiers) / 140
total = prog_m + prog_r
r0 = sum(n[t] * (y26[t][0] * Decimal(1.065 ** 1.25) + y26[t][1] * Decimal(1.09 ** 1.25)) for t in tiers) / 140


def whole(x):
    return int(x.quantize(Decimal("1"), rounding="ROUND_HALF_UP"))


print("tier  members  2026 medical  2026 pharmacy  baseline medical  baseline pharmacy")
for t in tiers:
    print("%4d  %7d  %12s  %13s  %16s  %17s" % (t, n[t], "{:,}".format(whole(y26[t][0])), "{:,}".format(whole(y26[t][1])),
                                                "{:,}".format(whole(base[t][0])), "{:,}".format(whole(base[t][1]))))
print("programme baseline: medical %s, pharmacy %s, total %s" % tuple("{:,}".format(whole(x)) for x in (prog_m, prog_r, total)))
print("members' own 2026 claims at trend (not certified): %s" % "{:,}".format(whole(r0)))

# the golden workbook
ws = load_workbook(os.path.join(GLD, "cohort_baseline_2027.xlsx"), data_only=True)["Baseline"]
got = {}
for row in ws.iter_rows(values_only=True):
    if row and isinstance(row[0], str) and re.fullmatch(r"Tier \d", row[0]):
        got[int(row[0][-1])] = tuple(row[1:6])
    if row and row[0] == "All enrolled members" and row[4] is not None:
        got["prog"] = (row[1], row[4], row[5], row[6])
for t in tiers:
    want = (n[t], whole(y26[t][0]), whole(y26[t][1]), whole(base[t][0]), whole(base[t][1]))
    assert got[t] == want, ("workbook tier", t, got[t], want)
assert got["prog"] == (140, whole(prog_m), whole(prog_r), whole(total)), ("workbook programme", got["prog"])
assert whole(prog_m) + whole(prog_r) == whole(total), "the rounded parts add to the rounded total"

# the memo opens with the total
import zipfile
xml = zipfile.ZipFile(os.path.join(GLD, "baseline_certification_memo.docx")).read("word/document.xml").decode("utf-8")
text = re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", "\n", xml))
paras = [p for p in text.split("\n") if p.strip()]
opening = next(p for p in paras if p.startswith("I recommend"))
assert "${:,}".format(whole(total)) in opening.split(":")[0], "memo opens with the total programme baseline"
assert "word/media/" in "".join(zipfile.ZipFile(os.path.join(GLD, "baseline_certification_memo.docx")).namelist()), "chart"

# submission.md block 4, when it exists
sub = os.path.join(TASK, "submission.md")
if os.path.exists(sub):
    s = open(sub).read()
    b4 = s[s.index("## 4."):]
    for t in tiers:
        line = next(l for l in b4.split("\n") if re.match(r"\s*-\s*Tier %d:" % t, l))
        for v in (n[t], whole(y26[t][0]), whole(y26[t][1]), whole(base[t][0]), whole(base[t][1])):
            tok = "{:,}".format(v)
            assert re.search(r"(?<![\d,])\$?%s(?![\d,])" % re.escape(tok), line), ("submission tier", t, tok, line)
    for v in (whole(prog_m), whole(prog_r), whole(total)):
        assert "${:,}".format(v) in b4, ("submission programme", v)
    b1 = s[s.index("## 1."):s.index("## 2.")]
    assert "${:,}".format(whole(total)) in b1, "block 1 carries the total"
    print("submission.md agrees with the recomputation")
print("verify: every graded figure recomputes from target/ and agrees with golden/")
