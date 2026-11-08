"""task197 independent verifier: reads only target/ and figures.json, on its own code path, and recomputes every
graded figure. Exit 1 on any mismatch."""
import os, sys, csv, json, datetime as dt
from collections import defaultdict
import numpy as np
import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), "target")
F = json.load(open(os.path.join(HERE, "figures.json")))
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


# ---------------------------------------------------------------- the register
wb = openpyxl.load_workbook(os.path.join(TGT, "register/watched_products_register.xlsx"), read_only=True)
wp = list(wb["Watched products"].iter_rows(values_only=True))
upc_code, names = {}, {}
for r in wp[1:]:
    upc_code[r[7]] = r[0]
    names[r[0]] = r[1]
pc = list(wb["Packaging changes"].iter_rows(values_only=True))
first_sale = {}
for r in pc[1:]:
    v = r[4]
    first_sale[r[0]] = v.date() if isinstance(v, dt.datetime) else v
ok("register read: eight packaging changes and twelve watched products", len(first_sale) == 8 and len(names) == 12)

# ---------------------------------------------------------------- the procedure, read back
def text(p):
    return " ".join(" ".join((pg.extract_text() or "") for pg in PdfReader(os.path.join(TGT, p)).pages).split())
proc = text("packaging_review/crp_referral_procedure_issue4.pdf")
ok("procedure positive control: the effect clause is read", "divided by the number the product's packs would have produced" in proc)
ok("procedure: the threshold the call uses is 1.20", "at least 1.20" in proc)
ok("procedure: the window begins the month after the first retail sale", "begin on the first day of the month after it" in proc)

# ---------------------------------------------------------------- monthly accidental under-six counts
counts = defaultdict(lambda: defaultdict(int))
rows = 0
with open(os.path.join(TGT, "network/case_export_watched_products.csv"), newline="", encoding="utf-8") as fh:
    rd = csv.reader(fh)
    head = next(rd)
    ix = {h: i for i, h in enumerate(head)}
    for r in rd:
        rows += 1
        if r[ix["reason"]] == "Unintentional - general" and r[ix["product_code"]] and int(r[ix["patient_age_years"]]) < 6:
            y, m = int(r[ix["call_received_local"]][0:4]), int(r[ix["call_received_local"]][5:7])
            counts[r[ix["product_code"]]][(y, m)] += 1
ok("spine: 25,000 rows or more", rows >= 25000, str(rows))

# ---------------------------------------------------------------- daily purchases from four-week periods
D0 = dt.date(2008, 1, 6)
rev, pre_rel = defaultdict(lambda: defaultdict(int)), defaultdict(lambda: defaultdict(int))
for f, store in (("market/halcyon_pos_4wk_revised.csv", rev), ("market/halcyon_pos_4wk_preliminary.csv", pre_rel)):
    with open(os.path.join(TGT, f), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            store[upc_code[r["upc"]]][r["period_ending"]] += int(r["units"])
units = {c: dict(rev[c]) for c in rev}
for c in pre_rel:                      # the preliminary release counts only for periods the revision does not hold
    for e, u in pre_rel[c].items():
        units.setdefault(c, {}).setdefault(e, u)
last = max(dt.date.fromisoformat(e) for c in units for e in units[c])
N = (last - D0).days + 1
days = [D0 + dt.timedelta(i) for i in range(N)]
mkeys = np.array([d.year * 12 + d.month - 1 for d in days])


def buys_of(code):
    b = np.zeros(N)
    for e, u in units[code].items():
        z = (dt.date.fromisoformat(e) - D0).days
        b[z - 27:z + 1] += u / 28.0
    return b


def drained(b, L):
    q = np.exp(-1.0 / (L * 30.4375))
    out = np.empty_like(b)
    acc = 0.0
    for i in range(len(b)):           # its own loop, not the generator's filter
        acc = acc * q + b[i]
        out[i] = acc
    return out


def month_sum(v, ks):
    return np.array([v[mkeys == k].sum() for k in ks])


def nll(y, x):
    h = y.sum() / x.sum()
    mu = h * x
    return float(np.sum(mu - y * np.log(mu))), h


EFF = {}
for code, fs in first_sale.items():
    b = buys_of(code)
    ck = fs.year * 12 + fs.month - 1
    pre = list(range(2019 * 12, ck))
    post = list(range(ck + 1, ck + 13))
    y = np.array([counts[code].get((k // 12, k % 12 + 1), 0) for k in pre], dtype=float)
    grid = np.arange(1.0, 70.0, 0.25)
    vals = [nll(y, month_sum(drained(b, L), pre))[0] for L in grid]
    i = int(np.argmin(vals))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, len(grid) - 1)]
    for _ in range(30):                # golden-section refinement on its own bracket
        m1, m2 = lo + 0.382 * (hi - lo), lo + 0.618 * (hi - lo)
        if nll(y, month_sum(drained(b, m1), pre))[0] < nll(y, month_sum(drained(b, m2), pre))[0]:
            hi = m2
        else:
            lo = m1
    L = (lo + hi) / 2
    st = drained(b, L)
    _, h = nll(y, month_sum(st, pre))
    obs = sum(counts[code].get((k // 12, k % 12 + 1), 0) for k in post)
    EFF[code] = obs / (h * month_sum(st, post).sum())
order = sorted(EFF, key=lambda c: -EFF[c])
fig = {e["product_code"]: e for e in F["effects"]}
ok("call: the largest effect is the referred product", names[order[0]] == F["call"], names[order[0]])
ok("call: its effect prints as filed", round(EFF[order[0]] + 1e-12, 1) == F["call_effect"], "%.4f" % EFF[order[0]])
ok("runner-up: second largest effect", names[order[1]] == F["runner_up"], names[order[1]])
ok("runner-up: its effect prints as filed", round(EFF[order[1]] + 1e-12, 1) == F["runner_up_effect"])
ok("gap: as filed", round(round(EFF[order[0]] + 1e-12, 1) - round(EFF[order[1]] + 1e-12, 1), 1) == F["gap"])
for code, e in EFF.items():
    ok("effect %s prints as filed" % code, round(e + 1e-12, 1) == fig[code]["effect"], "%.4f vs %s" % (e, fig[code]["effect"]))
    ok("threshold %s as filed" % code, (e >= 1.20) == fig[code]["reaches"])
    edge = 0.05 - abs(e - round(e, 1))
    ok("effect %s sits 0.012 or more from a printed edge" % code, edge >= 0.012, "%.4f" % edge)

# ---------------------------------------------------------------- the antidote asks, grouped on this code path
bags = []
with open(os.path.join(TGT, "hospitals/antidote_preparations_2024-07_2026-10.csv"), newline="") as fh:
    for r in csv.DictReader(fh):
        bags.append((r["hospital_code"], dt.datetime.fromisoformat(r["prepared_local"]),
                     "A" if "Acetylcysteine" in r["product"] else "D", int(r["dose_mg"])))
HALF = {"2025 H1": (dt.date(2025, 1, 1), dt.date(2025, 6, 30)), "2025 H2": (dt.date(2025, 7, 1), dt.date(2025, 12, 31)),
        "2026 H1": (dt.date(2026, 1, 1), dt.date(2026, 6, 30))}
REG = {150: ((50, 0.3, 1.6), (100, 0.3, 6.0), (100, 18.5, 22.5)), 200: ((100, 3.0, 5.0), (100, 18.5, 21.5))}
nac_start = defaultdict(int)
for hosp in sorted({x[0] for x in bags}):
    a = sorted([x for x in bags if x[0] == hosp and x[2] == "A"], key=lambda x: x[1])
    taken = set()
    for i, (h, t, _, d) in enumerate(a):
        if i in taken:
            continue
        best = []
        for load, roles in REG.items():
            w = d / load
            got = []
            for mgkg, lo, hi in roles:
                for j in range(i + 1, len(a)):
                    if j in taken or j in got:
                        continue
                    dh = (a[j][1] - t).total_seconds() / 3600
                    if dh > hi:
                        break
                    if dh >= lo and abs(a[j][3] / mgkg - w) <= 0.15:
                        got.append(j)
                        break
            if len(got) > len(best):
                best = got
        taken.update(best)
        for lab, (x0, x1) in HALF.items():
            if x0 <= t.date() <= x1:
                nac_start[(h, lab)] += 1
dfo_start = defaultdict(int)
for hosp in sorted({x[0] for x in bags}):
    d = sorted([x for x in bags if x[0] == hosp and x[2] == "D"], key=lambda x: x[1])
    nightly = set()
    for i, x in enumerate(d):
        for j, z in enumerate(d):
            if i != j and x[3] == z[3] and 18 <= abs((z[1] - x[1]).total_seconds()) / 3600 <= 30:
                nightly.add(i)
    acute = [x for i, x in enumerate(d) if i not in nightly]
    last_by_dose = {}
    for x in acute:
        p = last_by_dose.get(x[3])
        if p is None or not (6.5 <= (x[1] - p).total_seconds() / 3600 <= 9.5):
            for lab, (x0, x1) in HALF.items():
                if x0 <= x[1].date() <= x1:
                    dfo_start[(hosp, lab)] += 1
        last_by_dose[x[3]] = x[1]
for a in F["antidote"]:
    k = (a["hospital"], a["half"])
    ok("acetylcysteine courses %s %s" % k, nac_start[k] == a["acetylcysteine_courses"], "%d vs %d" % (nac_start[k], a["acetylcysteine_courses"]))
    ok("deferoxamine courses %s %s" % k, dfo_start[k] == a["deferoxamine_courses"], "%d vs %d" % (dfo_start[k], a["deferoxamine_courses"]))
    ok("together %s %s" % k, nac_start[k] + dfo_start[k] == a["antidote_courses"])

bad = [x for x in OUT if not x[1]]
for label, good, detail in OUT:
    if not good:
        print("FAIL", label, detail)
print("%d checks, %d failed" % (len(OUT), len(bad)))
sys.exit(1 if bad else 0)
