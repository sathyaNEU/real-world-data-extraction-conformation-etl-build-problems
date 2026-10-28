"""Independent verifier: reads only target.zip (csv, openpyxl and pypdf; none of solve.py, world.py or params.py),
recomputes every graded figure on its own code path and compares with figures.json."""
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import zipfile
import zoneinfo

import numpy as np
import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
UK = zoneinfo.ZoneInfo("Europe/London")
DUTY = {"Beer": "BEER", "Cider": "CIDR", "Wine": "WINE", "Spirits": "SPIR", "Road fuel": "FUEL"}
QUARTERS = ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]


def main(zpath):
    z = zipfile.ZipFile(zpath)
    names = z.namelist()
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    n = [0]

    def check(label, cond, detail=""):
        n[0] += 1
        if not cond:
            raise AssertionError("VERIFY FAIL %s %s" % (label, detail))

    pick = lambda pre: [x for x in names if x.startswith(pre)][0]

    def csv_rows(name):
        with z.open(name) as f:
            return list(csv.DictReader(io.TextIOWrapper(f, encoding="utf-8")))

    def book(name):
        return openpyxl.load_workbook(io.BytesIO(z.read(name)), read_only=True, data_only=True)

    def pdf_text(name):
        return re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(io.BytesIO(z.read(name))).pages))

    # the documents: every filed sentence the call or the asks lean on, read back from the shipped file
    manual = pdf_text(pick("treasury_budget_appraisal_manual"))
    for s in ("every tax on the good counts towards it: the duty and the GST charged on the duty-inclusive price",
              "passes in full to the shelf price, with GST charged on top",
              "the calendar year in which it takes effect", "on what consumers will buy in that year",
              "the latest four quarters of duty-paid clearances", "each quarter standing for the same quarter of the "
              "Budget year", "with the duty rates already set for the Budget year", "after consumers respond",
              "the prices they pay", "removes the most excess burden in the Budget year for that sum"):
        check("pdf manual: %s" % s[:40], s in manual)
    ce14 = pdf_text(pick("customs_excise_accounting_note_ce14"))
    for s in ("by the date in Eskerholm, which keeps United Kingdom time", "records acceptance times in UTC",
              "in the period in which the release was first accepted", "A cancelled declaration accounts for nothing",
              "credited in the period the repayment is accepted", "at the rate in force that day",
              "up to the day before its end date"):
        check("pdf CE14: %s" % s[:40], s in ce14)
    eml = z.read(pick("budget_2027_duty_envelope")).decode("utf-8")
    check("eml: the envelope", "GBP 1.5 million envelope" in eml and "It goes to" in eml)
    envelope = 1.5e6

    # the series: the back-series workbook (one sheet per duty) and the long release, stacked
    series = {c: {} for c in DUTY.values()}
    wb = book(pick("excise_clearances_prices_quarterly_2008"))
    for name, code in DUTY.items():
        for row in list(wb[name].iter_rows(values_only=True))[1:]:
            if row and row[0]:
                y, q = row[0].split(" Q")
                series[code][(int(y), int(q))] = (float(row[1]), float(row[2]))
    check("xlsx back series: 16 quarters per duty", all(len(v) == 16 for v in series.values()))
    for row in csv_rows(pick("excise_clearances_prices_quarterly_2012")):
        y, q = row["quarter"].split("Q")
        series[DUTY[row["duty"]]][(int(y), int(q))] = (float(row["duty_paid_clearances_thousand_litres"]),
                                                       float(row["average_shelf_price_gbp_per_litre_2026_prices"]))
    check("csv release: 75 quarters per duty once stacked", all(len(v) == 75 for v in series.values()))
    rates = {c: [] for c in DUTY.values()}
    wr = book(pick("excise_duty_rates"))
    for row in list(wr["Duty rates"].iter_rows(values_only=True))[1:]:
        d = row[1].date() if isinstance(row[1], dt.datetime) else row[1]
        rates[DUTY[row[0]]].append((d, float(row[2])))
    gst = [r for r in list(wr["GST"].iter_rows(values_only=True))[1:]]
    check("xlsx GST: 5 per cent from April 2011", float(gst[-1][1]) == 0.05)
    g = 0.05

    def rate(code, day):
        return [v for d, v in sorted(rates[code]) if d <= day][-1]

    # each duty: OLS by the normal equations, the 2027 path, the cut by bisection, the welfare integral by quadrature
    out = {}
    for code, d in series.items():
        ks = sorted(d)
        lq = np.log([d[k][0] for k in ks])
        lp = np.log([d[k][1] for k in ks])
        X = np.array([[1.0 * (ks[t][1] == j) for j in (1, 2, 3, 4)] + [lp[t], lq[t - 1]] for t in range(1, len(ks))])
        b = np.linalg.solve(X.T @ X, X.T @ lq[1:])
        beta, lam = b[4], b[5]
        eps = [beta * (1 - lam ** k) / (1 - lam) for k in (1, 2, 3, 4)]
        last4 = {k[1]: d[k][0] * 1000.0 for k in ks[-4:]}
        q0 = np.array([last4[1], last4[2], last4[3], last4[4]])
        p_last = d[ks[-1]][1]
        c = p_last / (1 + g) - rate(code, dt.date(2026, 9, 1))
        d27 = rate(code, dt.date(2027, 1, 1))
        p0 = (c + d27) * (1 + g)

        def revenue(cut):
            p1 = (c + d27 - cut) * (1 + g)
            q1 = q0 * (p1 / p0) ** np.array(eps)
            return float(np.sum((p0 - c) * q0 - (p1 - c) * q1)), q1, p1
        lo, hi = 0.0, d27 * 0.999
        for _ in range(200):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if revenue(mid)[0] < envelope else (lo, mid)
        cut = (lo + hi) / 2
        _, q1, p1 = revenue(cut)
        gain = 0.0
        for a, bq, e in zip(q0, q1, eps):
            grid = np.linspace(a, bq, 4001)
            price = p0 * (grid / a) ** (1.0 / e)
            gain += float(np.sum((price[1:] + price[:-1]) / 2 - c) * (grid[1] - grid[0]))
        out[code] = dict(gain=gain, cut=cut, d27=d27)
    order = sorted(out, key=lambda k: -out[k]["gain"])
    tenth = lambda x: float(np.floor(x * 10 + 0.5) / 10)
    check("call: the duty", order[0] == fig["winner"], order)
    check("call: the figure", tenth(out[order[0]]["gain"] / 1e6) == fig["winner_m"], out[order[0]]["gain"])
    check("call: the next best", order[1] == fig["runner"])
    check("call: its figure", tenth(out[order[1]]["gain"] / 1e6) == fig["runner_m"], out[order[1]]["gain"])
    for code in out:
        check("cut %s" % code, abs(out[code]["cut"] - fig["duties"][code]["cut"]) < 2e-4)
        check("excess burden %s" % code, abs(out[code]["gain"] / 1000 - fig["duties"][code]["eb_k"]) <= 0.6)

    # the asks: Customs' declarations under CE14, with the register
    reg = book(pick("bonded_warehouse_register"))
    prem = {}
    for row in list(reg["Approved warehouses"].iter_rows(values_only=True))[1:]:
        start = row[4].date() if isinstance(row[4], dt.datetime) else row[4]
        end = row[5].date() if isinstance(row[5], dt.datetime) else (row[5] or None)
        prem[row[0]] = (row[2], start, end)

    def approved(wid, day):
        p = prem[wid][0]
        return any(v[0] == p and v[1] <= day and (v[2] is None or day < v[2]) for v in prem.values())
    decl_rows = csv_rows(pick("customs_excise_declarations"))
    check("csv declarations: 25,000 rows or more", len(decl_rows) >= 25000)
    uniq = list({tuple(r.items()): r for r in decl_rows}.values())

    def local(r):
        return dt.datetime.fromisoformat(r["accepted_at_utc"].replace("Z", "+00:00")).astimezone(UK).date()

    def qtr(d):
        return "%dQ%d" % (d.year, (d.month + 2) // 3)
    tot = {c: {q: 0.0 for q in QUARTERS} for c in DUTY.values()}
    groups = {}
    for r in uniq:
        if r["cpc"] == "4071" and r["status"] != "CANCELLED":
            groups.setdefault(r["declaration_no"], []).append(r)
    parent = {no: rs[0]["related_declaration"] for no, rs in groups.items() if rs[0]["related_declaration"]}
    corrected = set(parent.values())
    for no, rs in groups.items():
        if no in corrected:
            continue
        root = no
        while root in parent:
            root = parent[root]
        first = local(groups[root][0])
        q = qtr(first)
        for r in rs:
            if r["duty_code"] in tot and q in tot[r["duty_code"]]:
                tot[r["duty_code"]][q] += round(int(r["quantity_litres"]) * rate(r["duty_code"], first), 2)
    for r in uniq:
        if r["cpc"] == "6171" and r["status"] != "CANCELLED" and r["duty_code"] in tot:
            q = qtr(local(r))
            if q in tot[r["duty_code"]]:
                tot[r["duty_code"]][q] -= float(r["duty_gbp"])
        if r["cpc"] == "7171" and r["status"] != "CANCELLED" and r["duty_code"] in tot:
            day = local(r)
            if not approved(r["warehouse_to"], day) and qtr(day) in tot[r["duty_code"]]:
                tot[r["duty_code"]][qtr(day)] += round(int(r["quantity_litres"]) * rate(r["duty_code"], day), 2)
    for c in tot:
        for q in QUARTERS:
            k = float(np.floor(tot[c][q] / 100 + 0.5) / 10)
            check("ask %s %s" % (c, q), k == fig["asks_k"][c][q], (k, fig["asks_k"][c][q]))
    cpc = csv_rows(pick("customs_procedure_codes"))
    check("csv procedure codes: 4071 is a release for home use", any(r["cpc"] == "4071" and "home use" in r["description"]
                                                                    for r in cpc))
    print("verify: %d assertions passed on %s" % (n[0], os.path.basename(zpath)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target.zip")))
