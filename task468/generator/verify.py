"""An independent verifier for task468: reads only the shipped bundle (target/) and the golden workbook, with its own
readers and arithmetic (no generator module), and recomputes the caseloads, each class's projected managed spend, the
staffing and the rebates.

    python3 task468/generator/verify.py
"""
import csv
import datetime as dt
import math
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
N = {"orrin": "orrin_rx_specialty_claims_2019_2025.csv", "tallis": "tallis_specialty_claims_2026h1.csv",
     "xw": "member_id_crosswalk_2026.csv", "drugs": "tallis_specialty_drug_list_2026.csv",
     "prices": "tallis_specialty_price_schedule_2026.xlsx", "rebates": "orrin_rx_rebate_statement_2025.xlsx"}
GOLD = "merrow_specialty_pharmacist_staffing_2026_27.xlsx"
CLASSES = ["IMM", "MS", "ONC", "HCV", "GLP", "HIV", "AST", "CF", "CGR"]


def rows(p):
    with open(p, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def mi(d):
    return (d.year - 2019) * 12 + d.month - 1


def month_end(i):
    y, m = divmod(i + 1, 12)
    return dt.date(2019 + y, m + 1, 1) - dt.timedelta(days=1)


def main(target, golden):
    from openpyxl import load_workbook
    p = lambda k: os.path.join(target, N[k])
    xo, xt = {}, {}
    for r in rows(p("xw")):
        if r["orrin_member_key"]:
            xo[r["orrin_member_key"]] = r["plan_member_id"]
        if r["tallis_member_no"]:
            xt[r["tallis_member_no"]] = r["plan_member_id"]
    cls = {r["ndc11"]: r["class_code"] for r in rows(p("drugs"))}
    price = {}
    for r in load_workbook(p("prices"), data_only=True).active.iter_rows(min_row=4, values_only=True):
        if r and r[0]:
            price[str(r[0])] = (float(r[2]), float(r[3]))
    fills = []    # (member, class, date, days, spend)
    o = rows(p("orrin"))
    rev = {r["claim_no"] for r in o if r["line_type"] == "REVERSAL"}
    for r in o:
        if r["claim_no"] in rev:
            continue
        a, b, c = r["ndc"].split("-")
        n = a.zfill(5) + b.zfill(4) + c.zfill(2)
        fills.append((xo[r["member_key"]], cls[n], dt.date.fromisoformat(r["fill_date"]), int(r["days_supply"]),
                      round(float(r["qty"]) * price[n][0], 2) + price[n][1]))
    t = rows(p("tallis"))
    rev = {r["ClaimID"] for r in t if r["Status"] == "R"}
    for r in t:
        if r["ClaimID"] in rev:
            continue
        d = dt.datetime.strptime(r["DateOfService"], "%m/%d/%Y").date()
        fills.append((xt[r["MemberNo"]], cls[r["NDC11"]], d, int(r["DaysSupply"]),
                      round(float(r["Quantity"]) * price[r["NDC11"]][0], 2) + price[r["NDC11"]][1]))
    first = {}
    spend = defaultdict(float)
    cover = defaultdict(list)
    for m, c, d, ds, s in fills:
        k = (m, c)
        first[k] = min(first.get(k, d), d)
        spend[(m, c, mi(d))] += s
        cover[k].append((d, d + dt.timedelta(days=ds - 1)))

    def on(day):
        return {k for k, iv in cover.items() if any(a <= day <= b for a, b in iv)}

    last = mi(dt.date(2026, 6, 30))
    cap = 36
    early = dt.date(2019, 3, 31)

    def dur(k, i):
        return cap if first[k] <= early else min(i - mi(first[k]), cap)

    cell = defaultdict(lambda: [0.0, 0])
    for i in range(0, last - 12 + 1):
        for k in on(month_end(i)):
            nxt = sum(spend.get((k[0], k[1], j), 0.0) for j in range(i + 1, i + 13))
            s = cell[(k[1], dur(k, i))]
            s[0] += nxt
            s[1] += 1
    case = on(dt.date(2026, 6, 30))
    proj = defaultdict(float)
    n_case = defaultdict(int)
    for k in case:
        t_ = dur(k, last)
        while (k[1], t_) not in cell and t_ > 0:
            t_ -= 1
        s = cell[(k[1], t_)]
        proj[k[1]] += s[0] / s[1]
        n_case[k[1]] += 1
    pharm = {c: int(math.ceil(proj[c] / 1_500_000)) for c in CLASSES}
    seen, reb = set(), defaultdict(float)
    for r in load_workbook(p("rebates"), data_only=True).active.iter_rows(min_row=5, values_only=True):
        if r and r[0] and str(r[1]).startswith("2025") and (r[2], r[1]) not in seen:
            seen.add((r[2], r[1]))
            reb[r[3]] += float(r[6])
    ws = load_workbook(os.path.join(golden, GOLD), data_only=True)["Staffing"]
    gw = {r[0]: r for r in ws.iter_rows(min_row=5, values_only=True) if r and r[0] in CLASSES}
    checks = {
        "caseloads": all(gw[c][2] == n_case[c] for c in CLASSES),
        "pharmacists": all(gw[c][4] == pharm[c] for c in CLASSES),
        "managed spend": all(gw[c][3] == int(proj[c] / 1e6 + 0.5) for c in CLASSES),
        "rebates": all(gw[c][5] == int(reb[c] / 1000 + 0.5) for c in CLASSES),
    }
    for k, v in checks.items():
        print("%s  verify: %s" % ("PASS" if v else "FAIL", k))
    print("verify: %d fills, caseload %d, pharmacists %s (total %d)" % (len(fills), len(case), pharm,
                                                                      sum(pharm.values())))
    if not all(checks.values()):
        raise SystemExit("verify failed")


if __name__ == "__main__":
    main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
