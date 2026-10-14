"""The independent verifier: reads only the shipped bundle (target/) and the goldens, on its own code path (its own
parsing of the PDFs' figures, its own likelihood in the log of sigma, a quasi-Newton optimiser), and recomputes the
call, every attachment's expected count, the curve, the premiums and the rated exposure by class."""
import csv
import datetime as dt
import math
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np
import openpyxl
from scipy import optimize, special


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(path).pages))


def find(folder, prefix):
    hits = [f for f in os.listdir(folder) if f.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return os.path.join(folder, hits[0])


def norm_sf_log(z):
    return np.log(0.5 * special.erfc(z / math.sqrt(2.0)))


def main(target, golden):
    memo = pdf_text(find(target, "liability_coverage_memorandum"))
    study = pdf_text(find(target, "actuarial_study"))
    quotes = pdf_text(find(target, "excess_liability_indications"))
    policy = pdf_text(find(target, "risk_financing_policy"))
    m = re.search(r"\$([\d,]+) for occurrences in (\d{4}) to (\d{4}) and \$([\d,]+) for occurrences from 1 January (\d{4})", memo)
    r_old, y0, y1, r_new, y2 = int(m.group(1).replace(",", "")), int(m.group(2)), int(m.group(3)), int(m.group(4).replace(",", "")), int(m.group(5))
    retention = lambda ay: r_old if ay <= y1 else r_new
    index = {int(a): float(b) for a, b in re.findall(r"\b(20\d\d)(?: \(projected\))? (\d{2,3}\.\d)\b", study)}
    lam = float(re.search(r"Expected 2027 liability occurrences costing more than \$25,000 ([\d.]+)", study).group(1))
    win = re.search(r"accident years (\d{4}) to (\d{4})\)", policy)
    years = range(int(win.group(1)), int(win.group(2)) + 1)
    opts = [(int(a.replace(",", "")), float(gl), float(al)) for a, gl, al in
            re.findall(r"\$([\d,]{9,}) \$10,000,000 \$(0\.\d{4}) \$([\d.]+)", quotes)]
    assert len(opts) == 7 and len(index) >= 14, (len(opts), len(index))
    line = 1.0 if "is one or fewer" in policy else None

    # the pool's record of every occurrence of the policy's years, both administrators, an open file at what the pool
    # has paid and still reserves
    occ = []
    wb = openpyxl.load_workbook(find(target, "liability_closed_claims"), read_only=True)
    for name in wb.sheetnames:
        if not name.startswith("AY"):
            continue
        for row in wb[name].iter_rows(min_row=6, values_only=True):
            if not row or not row[0]:
                continue
            ay = dt.datetime.strptime(row[3], "%m/%d/%Y").year
            occ.append((ay, float(row[7]), float(row[7]) + float(row[10]), row[6] == "CL"))
    for r in csv.DictReader(open(find(target, "liability_loss_run"))):
        ay = int(r["loss_date"][:4])
        occ.append((ay, float(r["deductible"]), float(r["deductible"]) + float(r["paid_indemnity"]) +
                    float(r["paid_defense"]) + float(r["reserve_indemnity"]) + float(r["reserve_defense"]),
                    r["status"] == "Closed"))
    fit = [o for o in occ if o[0] in years]
    assert sum(1 for o in fit if not o[3]) == 20, "the policy's years hold twenty open files"
    f = np.array([index[2027] / index[o[0]] for o in fit])
    x = np.log(np.array([o[2] for o in fit]) * f)
    d = np.log(np.array([o[1] for o in fit]) * f)
    cens = np.array([o[2] >= retention(o[0]) - 0.005 for o in fit])

    def nll(p):
        mu, ls = p
        s = math.exp(ls)
        z = (x - mu) / s
        dens = -0.5 * z * z - 0.5 * math.log(2 * math.pi) - ls - x
        return -(np.where(cens, norm_sf_log(z), dens) - norm_sf_log((d - mu) / s)).sum()

    start = [float(x.mean()), math.log(float(x.std()))]
    res = optimize.minimize(nll, start, method="BFGS", options=dict(gtol=1e-9))
    res = optimize.minimize(nll, res.x, method="Nelder-Mead", options=dict(xatol=1e-12, fatol=1e-12, maxiter=20000))
    mu, sigma = float(res.x[0]), math.exp(float(res.x[1]))

    def count(a):
        return lam * math.exp(norm_sf_log((math.log(a) - mu) / sigma) - norm_sf_log((math.log(25_000) - mu) / sigma))

    counts = {a: count(a) for a, _, _ in opts}
    call = next(a for a, _, _ in opts if counts[a] <= line)

    # the rated exposure: each member's declared total once; one vehicle per latest unit number added for it
    toe = {}
    wb = openpyxl.load_workbook(find(target, "exposure_declarations"), read_only=True)
    cls = {}
    for row in wb["Declarations"].iter_rows(min_row=2, values_only=True):
        if row[6] is not None:
            toe[row[0]] = max(toe.get(row[0], 0), int(row[6]))
        cls[row[0]] = row[1]
    rating = dt.date(2026, 9, 30)
    adds, gone, key = {}, set(), {}

    def ident(v, s):
        v = re.sub(r"[\s-]", "", v).upper()
        return v if len(v) == 17 else "S:" + re.sub(r"[\s-]", "", s).upper()

    for r in csv.DictReader(open(find(target, "vehicle_schedule_log"))):
        k = (int(r["member_no"]), r["unit_no"])
        eff = dt.date.fromisoformat(r["effective_date"])
        if eff > rating:
            continue
        if r["txn_type"] == "ADD":
            adds[k] = (eff, r["entered_date"])
            key[k] = ident(r["vin"], r["serial_no"])
        elif r["txn_type"] == "DELETE":
            gone.add(k)
    latest = {}
    for k, stamp in adds.items():
        kk = (k[0], key[k])
        if kk not in latest or stamp > latest[kk][0]:
            latest[kk] = (stamp, k)
    units = Counter(kk[0] for kk, (_, k) in latest.items() if k not in gone)
    T, U = sum(toe.values()), sum(units.values())
    prem = {a: round(gl * T / 1000 + al * U) for a, gl, al in opts}
    by = defaultdict(lambda: [0, 0, 0])
    for mno, v in toe.items():
        by[cls[mno]][0] += 1
        by[cls[mno]][1] += v
        by[cls[mno]][2] += units.get(mno, 0)

    # the goldens
    gw = openpyxl.load_workbook(os.path.join(golden, "retention_2027.xlsx"))
    ws = gw["Retention 2027"]
    rows = [r for r in ws.iter_rows(min_row=6, max_row=12, values_only=True)]
    for r in rows:
        assert abs(r[1] - round(counts[r[0]], 2)) < 1e-9, ("count", r[0], r[1], counts[r[0]])
        assert r[5] == prem[r[0]], ("premium", r[0], r[5], prem[r[0]])
        assert (r[2] == "Yes") == (counts[r[0]] <= line)
    rec_txt = ws["A2"].value
    assert "${:,.0f}".format(call) in rec_txt, rec_txt
    curve = [c for c in ws.iter_rows(min_row=13, values_only=True) if c[0] and str(c[0]).startswith("Severity curve")][0][1]
    assert "log mean %.2f" % mu in curve and "log standard deviation %.2f" % sigma in curve, curve
    ex = gw["Rated exposure"]
    for r in ex.iter_rows(min_row=5, max_row=11, values_only=True):
        b = by[r[0].lower()]
        assert (r[1], r[2], r[3]) == (b[0], round(b[1] / 1000), b[2]), (r, b)
    print("verify: from target/ alone, %d occurrences (%d censored), log mean %.4f, log sd %.4f, call $%s (%.2f; runner-up "
          "%.2f); premiums %s; operating expenditures $%s, %d vehicles; goldens agree" % (
              len(fit), int(cens.sum()), mu, sigma, "{:,}".format(call), counts[call],
              counts[[a for a, _, _ in opts][[a for a, _, _ in opts].index(call) - 1]],
              ", ".join("{:,}".format(prem[a]) for a, _, _ in opts), "{:,}".format(T), U))


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "target"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "golden"))
