"""Independent verifier for task125:  python3 verify.py <task_dir>

Reads only <task_dir>/target/ (and metadata.json for the distractor list). Shares no code with the
generator: it parses the shipped bytes, rebuilds the screen from the published payments, and recomputes
every rung, rival-killer, calibration outcome and graded figure. Exit 0 only when every check holds."""
import csv
import datetime as dt
import itertools
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import openpyxl
from pypdf import PdfReader

TASK = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
T = TASK / "target"
OUT = []

# the figures the build claims (the golden values this verifier must reproduce from the bytes)
CLAIM = dict(order=6914, order_h=6900, asc=3902, hs=816, r2=7608, r3=5718, r4=6498, r5=6706, fernhollow=8102,
             gap_h=1200, A=[650, 632, 614, 596, 578, 560, 542, 524, 700, 506, 506, 506])


def check(name, cond, detail=""):
    OUT.append((name, bool(cond)))
    print("%s  %s%s" % ("PASS" if cond else "FAIL", name, ("  [%s]" % (detail,)) if detail != "" else ""))


def find(pattern):
    hits = sorted(T.glob(pattern))
    assert len(hits) == 1, (pattern, hits)
    return hits[0]


def pdf_text(p):
    return "\n".join(pg.extract_text() for pg in PdfReader(str(p)).pages)


def pence(s):
    neg = s.startswith("-")
    s = s.lstrip("-")
    a, b = s.split(".")
    v = int(a) * 100 + int(b)
    return -v if neg else v


def fy(d):
    y = d.year if d.month >= 4 else d.year - 1
    return "%d/%02d" % (y, (y + 1) % 100)


BEN = {d: math.log10(1 + 1 / d) for d in range(10, 100)}


def cell(v):
    return int(str(v // 100)[:2])


# ---------------------------------------------------------------------------------------- read the bytes
spine_p = find("*spend_over_500*.csv")
pays = []
with open(spine_p, encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        d = dt.datetime.strptime(r["payment_date"], "%d/%m/%Y").date()
        pays.append((r["department"], d, pence(r["net_amount"]), pence(r["vat_amount"]), r["expense_type"],
                     r["vendor_no"]))
DEPTS = []
for p in pays:
    if p[0] not in DEPTS:
        DEPTS.append(p[0])

st_text = pdf_text(find("digit_conformity_statements*.pdf"))
statements = {}
for block in re.split(r"Digit-conformity statement ", st_text)[1:]:
    year = block[:7]
    for d in DEPTS:
        m = re.search(re.escape(d) + r"\s*\n\s*([\d,]+)\s*\n\s*(0\.\d{5})", block)
        statements[(year, d, "tested")] = int(m.group(1).replace(",", ""))
        statements[(year, d, "mad")] = m.group(2)
    m = re.search(r"Council \(all departments\)\s*\n\s*(0\.\d{5})", block)
    statements[(year, "ALL", "mad")] = m.group(1)
YEARS = ["2023/24", "2024/25", "2025/26"]
check("statements parsed: 63 published figures", len(statements) == 63, len(statements))


def screen(amt, rng, cr):
    out = defaultdict(Counter)
    for dept, d, net, vat, _, _ in pays:
        y = fy(d)
        if y not in YEARS:
            continue
        v = net if amt == "net" else net + vat
        if v < 0:
            if cr == "excl":
                continue
            v = -v
        if rng == "pub" and v <= 0:
            continue
        if rng == "dec" and not 100000 <= v <= 99999999:
            continue
        if rng == "unc" and v < 100000:
            continue
        out[(y, dept)][cell(v)] += 1
    return out


def mad(c):
    n = sum(c.values())
    return sum(abs(c.get(k, 0) / n - BEN[k]) for k in range(10, 100)) / 90


def reproduce(cnt):
    hit = 0
    for y in YEARS:
        pooled = Counter()
        for d in DEPTS:
            c = cnt[(y, d)]
            pooled.update(c)
            hit += sum(c.values()) == statements[(y, d, "tested")]
            hit += ("%.5f" % mad(c)) == statements[(y, d, "mad")]
        hit += ("%.5f" % mad(pooled)) == statements[(y, "ALL", "mad")]
    return hit


def flagged(cnt, y):
    out = set()
    for d in DEPTS:
        c = cnt[(y, d)]
        n = sum(c.values())
        for k in range(10, 100):
            e = BEN[k] * n
            if c.get(k, 0) > 1.5 * e and c.get(k, 0) - e >= 30:
                out.add((d, k))
    return out


def routed(cells, amt, year="2025/26"):
    by = Counter()
    for dept, d, net, vat, _, _ in pays:
        if fy(d) != year:
            continue
        v = net if amt == "net" else net + vat
        if v >= 100000 and (dept, cell(v)) in cells:
            by[(dept, cell(v))] += 1
    return by


cnts = {(a, r, c): screen(a, r, c) for a in ("net", "gross") for r in ("pub", "dec", "unc") for c in ("excl", "abs")}
rep = {k: reproduce(v) for k, v in cnts.items()}
check("corpus: gross payments over complete decades, credit notes excluded, reproduce 63 of 63",
      rep[("gross", "dec", "excl")] == 63)
check("corpus: every other construction of the twelve reproduces 57 or fewer",
      all(v <= 57 for k, v in rep.items() if k != ("gross", "dec", "excl")), {"/".join(k): v for k, v in rep.items()})
G = cnts[("gross", "dec", "excl")]
c2526, c2324 = flagged(G, "2025/26"), flagged(G, "2023/24")
check("2025/26 screen flags five department-cells", len(c2526) == 5, sorted(c2526))
r2by = routed(c2526, "gross")
r2 = sum(r2by.values())
check("rung 2: 2025/26 flagged-cell payments = 7,608", r2 == CLAIM["r2"], r2)
r1 = sum(routed(flagged(cnts[("net", "dec", "excl")], "2025/26"), "net").values())
r0 = sum(routed(flagged(cnts[("net", "pub", "excl")], "2025/26"), "net").values())
check("rungs 0 and 1 (net bases) land in hundreds of their own", len({round(x, -2) for x in (r0, r1, r2)}) == 3,
      (r0, r1))

# ---------------------------------------------------------------------------------------- Housing Support
tsp = defaultdict(list)
rounds = {}
with open(find("tenancy_sustainment_payments*.csv"), encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        tsp[r["case_ref"]].append(dt.date.fromisoformat(r["payment_date"]))
        rounds[r["case_ref"]] = r["scheme_round"]
done21 = [len(v) for k, v in tsp.items() if rounds[k] == "2021"]
check("term pin: all 288 households of the completed 2021 round received exactly 30 payments",
      len(done21) == 288 and set(done21) == {30})
PLAN0, PLAN1 = dt.date(2027, 4, 1), dt.date(2028, 3, 31)


def ym_add(y, m, k):
    t = y * 12 + (m - 1) + k
    return t // 12, t % 12 + 1


hs_plan_by = Counter()
for k, v in tsp.items():
    first = min(v)
    for i in range(30):
        y, m = ym_add(first.year, first.month, i)
        if (PLAN0.year, PLAN0.month) <= (y, m) <= (PLAN1.year, PLAN1.month):
            hs_plan_by["%d-%02d" % (y, m)] += 1
hs_other = sum(1 for p in pays if p[0] == "Housing Support" and fy(p[1]) == "2025/26" and p[2] + p[3] >= 100000
               and cell(p[2] + p[3]) == 14 and p[4] != "Tenancy sustainment payments")
hs_plan = hs_other + sum(hs_plan_by.values())
check("Housing Support cell 14 in 2027/28 = 816 (168 other payments, 648 instalments)", hs_plan == CLAIM["hs"],
      (hs_other, sum(hs_plan_by.values())))

# ---------------------------------------------------------------------------------------- Shared Lives
rt = pdf_text(find("shared_lives_carer_rates*.pdf"))
rates = {}
for m in re.finditer(r"(Long-term, band \d|Home First step-down, \w+)\s*\n?\s*(\d{3})\.00", rt):
    rates[m.group(1)] = int(m.group(2))
check("rate schedule parsed: six weekly placement rates", len(rates) == 6, rates)
hist = defaultdict(dict)
for dept, d, net, vat, exp, ven in pays:
    if exp == "Shared Lives carer payments":
        hist[ven][d] = net + vat
run_dates = sorted({d for h in hist.values() for d in h})
last = run_dates[-1]
check("every Shared Lives carer vendor is paid at most once a run", sum(len(h) for h in hist.values()) ==
      sum(1 for p in pays if p[4] == "Shared Lives carer payments"))
decomp = defaultdict(list)
for k in (1, 2, 3):
    for ms in itertools.combinations_with_replacement(sorted(rates), k):
        decomp[400 * sum(rates[g] for g in ms)].append(ms)
cur = {v: h[last] for v, h in hist.items() if last in h}            # paid on the latest run
gone = {v: h for v, h in hist.items() if last not in h}             # stopped inside the extract
amts = Counter(cur.values())
single = {a for a in amts if len(decomp[a]) == 1}
rest = {a for a in amts if a not in single}
check("every current carer amount that is not four weeks of a set of placement rates is half of one, uniquely",
      all(not decomp[a] and len(decomp[2 * a]) == 1 for a in rest), sorted(a // 100 for a in rest))
hv = sorted(v for v, a in cur.items() if a in rest)
paired = len(hv) % 2 == 0 and all(hist[hv[i]] == hist[hv[i + 1]] and int(hv[i + 1]) == int(hv[i]) + 1
                                  for i in range(0, len(hv), 2))
check("the current halves are paid to consecutive vendor numbers in pairs, identical on every run", paired,
      len(hv) // 2)
# the record of how a joint household is paid when it loses a guest: every pair whose amounts changed in the extract
events = []
for v in sorted(hist):
    w = "%06d" % (int(v) + 1)
    if w not in hist:
        continue
    first = sorted(set(hist[v]) & set(hist[w]))
    if not first or hist[v][first[0]] != hist[w][first[0]] or hist[v][first[0]] in single:
        continue
    half0 = hist[v][first[0]]
    if decomp[half0] or len(decomp[2 * half0]) != 1:
        continue
    change = [d for d in run_dates if d in hist[v] and hist[v][d] != half0]
    if not change:
        continue
    d0 = change[0]
    after_v, after_w = hist[v][d0], hist[w].get(d0)
    if after_w is None:              # the second vendor is no longer paid: the first is paid a whole fee
        ms = decomp[after_v]
        events.append(("whole", len(ms[0]) if len(ms) == 1 else None,
                       all(d not in hist[w] for d in run_dates if d >= d0)))
    else:
        ms = decomp[2 * after_v]
        events.append(("halves", len(ms[0]) if len(ms) == 1 and after_v == after_w else None, True))
check("the extract's changed joint households: every one left with one guest is paid whole to the first vendor "
      "(the second never paid again); every one left with two or more is still paid in halves",
      events and all((k == "whole" and n == 1 and stop) or (k == "halves" and n is not None and n >= 2)
                     for k, n, stop in events) and {k for k, n, stop in events} == {"whole", "halves"},
      Counter((k, n) for k, n, stop in events))
check("every vendor no longer paid stopped on the run its partner's amount changed",
      all("%06d" % (int(v) - 1) in hist and min(d for d in run_dates if d > max(h)) in hist["%06d" % (int(v) - 1)]
          for v, h in gone.items()), len(gone))


def keep(ms):
    return [g for g in ms if not g.startswith("Home First")]


def fee(ms):
    return 400 * sum(rates[g] for g in ms)


def plan_pays(rule):
    """Carer payments on one 2027/28 run. rule: 'answer' (halves while two or more guests remain, whole to one
    vendor while one remains), 'halves' (every household halved again), 'held' (the halves at today's amounts)."""
    out = []
    for v, a in cur.items():
        if a in single:
            out.append(fee(keep(decomp[a][0])))
    for i in range(0, len(hv), 2):
        a = cur[hv[i]]
        left = keep(decomp[2 * a][0])
        if rule == "held":
            out += [a, a]
        elif rule == "halves" or len(left) >= 2:
            out += [fee(left) // 2] * 2
        elif len(left) == 1:
            out.append(fee(left))
    return [x for x in out if x]


def in14(lst):
    return sum(1 for x in lst if x >= 100000 and cell(x) == 14)


in14_now = sum(n for a, n in amts.items() if cell(a) == 14)
in14_after, in14_halves, in14_held = in14(plan_pays("answer")), in14(plan_pays("halves")), in14(plan_pays("held"))
check("after the closure 194 carer payments a run sit in cell 14 (102 now; 178 if every joint household were "
      "halved again; 162 with the halves held)", (in14_now, in14_after, in14_halves, in14_held) == (102, 194, 178, 162),
      (in14_now, in14_after, in14_halves, in14_held))
cal = openpyxl.load_workbook(find("bacs_payment_calendar*.xlsx"), read_only=True)
ws = cal["2027-28"]
plan_rows = [r for r in ws.iter_rows(min_row=4, values_only=True) if r[0]]
sl_plan = [(dt.datetime.strptime(r[1], "%d/%m/%Y").date(), dt.datetime.strptime(r[2], "%d/%m/%Y").date())
           for r in plan_rows if r[0] == "Shared Lives carers"]
check("2027/28 carries 13 Shared Lives runs", len(sl_plan) == 13)
asc_other = sum(1 for p in pays if p[0] == "Adult Social Care" and fy(p[1]) == "2025/26" and p[2] + p[3] >= 100000
                and cell(p[2] + p[3]) == 14 and p[4] != "Shared Lives carer payments")
asc_plan = asc_other + len(sl_plan) * in14_after
check("Adult Social Care cell 14 in 2027/28 = 3,902", asc_plan == CLAIM["asc"], (asc_other, in14_after))
flat = {k: v for k, v in r2by.items() if k[0] not in ("Adult Social Care", "Housing Support")}
order = asc_plan + hs_plan + sum(flat.values())
check("the order: 6,914 routed payments, filed 6,900", order == CLAIM["order"] and round(order, -2) == 6900,
      order)
r3 = order - len(sl_plan) * (in14_after - in14_now)
check("rung 3 (Shared Lives carried at current amounts) = 5,718", r3 == CLAIM["r3"], r3)
r5 = order - len(sl_plan) * (in14_after - in14_halves)
check("rung 5 (every joint household re-summed and halved again) = 6,706, filed 6,700",
      r5 == CLAIM["r5"] and round(r5, -2) == 6700, r5)
r4 = order - len(sl_plan) * (in14_after - in14_held)
check("rung 4 (every carer row decomposed on its own, the halves held) = 6,498, filed 6,500",
      r4 == CLAIM["r4"] and round(r4, -2) == 6500, r4)
check("Adult Social Care carries the largest share", asc_plan == max(asc_plan, hs_plan, *flat.values()))

# ---------------------------------------------------------------------------------------- plan-year months
months = ["2027-%02d" % m for m in range(4, 13)] + ["2028-%02d" % m for m in range(1, 4)]
flat_month = Counter()
for dept, d, net, vat, exp, ven in pays:
    if fy(d) == "2025/26" and net + vat >= 100000 and (dept, cell(net + vat)) in flat:
        flat_month[d.month] += 1
check("the flat streams carry the same count in every 2025/26 month", len(set(flat_month.values())) == 1,
      set(flat_month.values()))
per_month_flat = next(iter(set(flat_month.values())))
dp_month = asc_other // 12
A = []
for m in months:
    sl = sum(1 for pd_, sub in sl_plan if sub.strftime("%Y-%m") == m) * in14_after
    A.append(per_month_flat + hs_other // 12 + dp_month + hs_plan_by[m] + sl)
check("ask A: plan-year routed payments by run month", A == CLAIM["A"], A)

# ---------------------------------------------------------------------------------------- run log and Fernhollow
def dept_of(code):
    inits = {d: "".join(w[0] for w in re.findall(r"[A-Za-z']+", d) if w[0].isupper()) for d in DEPTS}
    c = [d for d in DEPTS if inits[d] == code] or [d for d in DEPTS if d.upper().startswith(code[:2])]
    assert len(c) == 1, code
    return c[0]


rl = openpyxl.load_workbook(find("digit_filter_run_log*.xlsx"), read_only=True).worksheets[0]
hdr, rows = None, []
for r in rl.iter_rows(values_only=True):
    if r and r[0] == "run_ref":
        hdr = list(r)
        continue
    if hdr and r and r[0]:
        rows.append(dict(zip(hdr, r)))
applied = {(dept_of(r["department"]), int(r["flagged_cell"])) for r in rows if r["flagged_cell"] not in (None, "")}
check("the run log applied exactly the 2023/24 screen's cells", applied == c2324, sorted(applied))
check("2023/24 cells are the 2025/26 cells plus one", c2526 < c2324 and len(c2324 - c2526) == 1,
      sorted(c2324 - c2526))
reran = {r["run_month"] for r in rows if r["run_type"] == "Re-run"}
B1 = Counter()
for r in rows:
    if r["run_type"] == "Scheduled" and r["run_month"] in reran:
        continue
    B1[r["run_month"]] += int(r["payments_routed"])
fern = sum(B1.values())
check("Fernhollow's figure: the run log's 2025/26 routed total = 8,102", fern == CLAIM["fernhollow"], fern)
gap_u, gap_h = round(fern - order, -2), round(fern, -2) - round(order, -2)
check("gap to Fernhollow's figure: 1,200 on unrounded and on rounded figures", gap_u == gap_h == CLAIM["gap_h"],
      (gap_u, gap_h))
# screened counts tie to the spending file by BACS file month (the calendar's submission dates)
sub_of = {}
for sh in cal.worksheets:
    for r in sh.iter_rows(min_row=4, values_only=True):
        if r[0]:
            sub_of[dt.datetime.strptime(r[1], "%d/%m/%Y").date()] = dt.datetime.strptime(r[2], "%d/%m/%Y").date()
by_file = Counter()
for dept, d, net, vat, exp, ven in pays:
    g = net + vat
    if 100000 <= g <= 99999999 and d in sub_of:
        f = sub_of[d]
        if dt.date(2025, 4, 1) <= f <= dt.date(2026, 3, 31) and (dept, cell(g)) in c2324:
            by_file[f.strftime("%Y-%m")] += 1
check("ask B1 reproduces from the spending file by BACS submission month", by_file == B1,
      [B1[m] for m in sorted(B1)])
acks = json.loads(find("fernhollow_batch_acknowledgements*.json").read_text())["batches"]
bmonth = {r["batch_ref"]: r["run_month"] for r in rows if r["batch_ref"]}
B2 = Counter()
for a in acks:
    B2[bmonth[a["batch_ref"]]] += a["payments_examined"]
check("ask B2: examined by routing month, every batch mapped to a run", len(bmonth) >= len(acks) and
      sum(B2.values()) == sum(a["payments_examined"] for a in acks), [B2[m] for m in sorted(B1)])
q2 = pdf_text(find("fernhollow_service_report_q2*.pdf"))
q2_ex = int(re.search(r"Payments examined\s*\n?\s*([\d,]+)", q2).group(1).replace(",", ""))
check("referee: the Q2 service report's examined total matches July to September",
      q2_ex == B2["2025-07"] + B2["2025-08"] + B2["2025-09"], q2_ex)
terms = pdf_text(find("pasf_lot2_calloff_terms*.pdf"))
minimum = int(re.search(r"minimum charge of (\d+) examinations", terms).group(1))
share = int(re.search(r"at (\d+) per cent of the base rate", terms).group(1)) / 100
od = pdf_text(find("calloff_*order_and_variation*.pdf"))
alloc0 = int(re.search(r"Quarterly allocation\s*\n?\s*([\d,]+)", od).group(1).replace(",", ""))
alloc1 = int(re.search(r"increased to\s*\n?\s*([\d,]+)", od).group(1).replace(",", ""))
rc = openpyxl.load_workbook(find("fernhollow_rate_cards*.xlsx"), read_only=True)["2025-26"]
base = [r[1] for r in rc.iter_rows(values_only=True) if r[0] and str(r[0]).startswith("Base rate")][0]
charged = Counter()
for a in acks:
    q = {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[int(bmonth[a["batch_ref"]][5:])]
    charged[q] += max(a["payments_examined"], minimum) if a["payments_examined"] else 0
alloc = {1: alloc0, 2: alloc0, 3: alloc1, 4: alloc1}
prem = [max(0, charged[q] - alloc[q]) for q in (1, 2, 3, 4)]
unused = [round(max(0, alloc[q] - charged[q]) * share * base) for q in (1, 2, 3, 4)]
check("ask C: quarterly premium examinations and unused-volume charges recompute", prem[0] > 0 and prem[1] > 0
      and unused[2] > 0 and unused[3] > 0, prem + unused)
inv = list(csv.DictReader(open(find("fernhollow_invoice_lines*.csv"), encoding="utf-8")))
inv_q = Counter()
for r in inv:
    inv_q[r["batch_ref"]] += int(r["quantity"])
check("invoice quantities net of the credit note equal the charged examinations batch by batch",
      all(inv_q[a["batch_ref"]] == (max(a["payments_examined"], minimum) if a["payments_examined"] else 0)
          for a in acks))

# ---------------------------------------------------------------------------------------- input gates
meta = json.loads((TASK / "metadata.json").read_text())
files = sorted(p for p in T.iterdir() if p.is_file())
check("input gates: 10 or more files and 3 or more formats",
      len(files) >= 10 and len({p.suffix for p in files}) >= 3, (len(files), sorted({p.suffix for p in files})))
check("input gate: a file of 25,000 or more rows", len(pays) >= 25000, len(pays))
check("input gate: two or more distractors, present and named nowhere in target/",
      len(meta["distractor_files"]) >= 2 and all((T / f).exists() for f in meta["distractor_files"])
      and not any("distractor" in p.name.lower() for p in files))
n_ok = sum(1 for _, c in OUT if c)
print("\nverifier: %d of %d checks pass" % (n_ok, len(OUT)))
print("FIGURES " + json.dumps(dict(order=order, asc=asc_plan, hs=hs_plan, r0=r0, r1=r1, r2=r2, r3=r3,
                                   fernhollow=fern, A=A, B1=[B1[m] for m in sorted(B1)],
                                   B2=[B2[m] for m in sorted(B1)], C=prem + unused)))
sys.exit(0 if n_ok == len(OUT) else 1)
