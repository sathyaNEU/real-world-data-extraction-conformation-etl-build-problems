"""The pack's data files: Orrin Rx's specialty claims (January 2019 to December 2025), Tallis Pharmacy Services'
specialty claims (January to June 2026), the plan's member crosswalk, Tallis's specialty drug list and 2026 price
schedule, and Orrin Rx's 2025 rebate statement."""
import csv
import datetime as dt

import numpy as np
import pandas as pd

import sim as S
import world as W

ORRIN_COLS = ["claim_no", "line_type", "fill_date", "member_key", "ndc", "product_desc", "qty", "days_supply",
              "ingredient_cost", "dispensing_fee", "member_copay", "plan_paid", "pharmacy_npi"]
TALLIS_COLS = ["ClaimID", "Status", "DateOfService", "MemberNo", "NDC11", "Quantity", "DaysSupply", "IngredientCost",
               "DispFee", "CopayAmt", "PlanPaidAmt", "PharmacyNPI", "Channel"]
XWALK_COLS = ["plan_member_id", "orrin_member_key", "tallis_member_no"]
DRUG_COLS = ["ndc11", "product_name", "package", "class_code", "class_name", "route"]
PHARMACIES = {"Specialty": ["1912048837", "1598810243"], "Health-system": ["1356442087", "1063918274"],
              "Mail": ["1427093361"], "Retail": ["1083726641", "1366509028", "1740231185"]}


def rng(k):
    return np.random.default_rng([W.SEED, 31, k])


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def ids(x):
    """Plan member ids, Orrin member keys and Tallis member numbers for every member the files show."""
    if "ids" in x:
        return x["ids"]
    f = x["fills"]
    r = rng(1)
    seen = f[(f["date"] >= W.FIRST_MONTH) & (f["date"] <= W.LAST_DAY)]
    mem = sorted(seen["member"].unique())
    plan = {m: "MHP%08d" % v for m, v in zip(mem, r.choice(np.arange(10_000_000, 99_999_999), len(mem), replace=False))}
    orrin_m = sorted(seen[seen["date"] < W.SWITCH]["member"].unique())
    tallis_m = sorted(seen[seen["date"] >= W.SWITCH]["member"].unique())
    orrin = {m: "OX-%07d" % v for m, v in zip(orrin_m, r.choice(np.arange(1_000_000, 9_999_999), len(orrin_m),
                                                                replace=False))}
    tallis = {m: "T%09d" % v for m, v in zip(tallis_m, r.choice(np.arange(300_000_000, 399_999_999), len(tallis_m),
                                                                replace=False))}
    x["ids"] = dict(plan=plan, orrin=orrin, tallis=tallis)
    return x["ids"]


def channel(row_days, prod_cls, r):
    """Where a fill was dispensed: long supplies by mail; the maintenance classes partly at retail; every class partly
    through the health systems' own specialty pharmacies."""
    if row_days >= 84:
        return "Mail"
    u = r.random()
    if prod_cls in ("HIV", "MS", "GLP", "CGR") and u < 0.3:
        return "Retail"
    if u > 0.72:
        return "Health-system"
    return "Specialty"


def claims(x):
    """Both PBMs' claim lines, with each fill's channel, reversals and rebills, as two lists of rows."""
    if "claims" in x:
        return x["claims"]
    f = x["fills"]
    f = f[(f["date"] >= W.FIRST_MONTH) & (f["date"] <= W.LAST_DAY)].sort_values(["date", "member"], kind="stable")
    idm = ids(x)
    r = rng(2)
    prod = S.PROD
    orrin, tallis, chans = [], [], []
    n_o, n_t = 4_100_000, 0
    for row in f.itertuples(index=False):
        p = prod.loc[row.prod]
        ch = channel(row.days, row.cls, r)
        chans.append(ch)
        npi = PHARMACIES[ch][int(r.integers(0, len(PHARMACIES[ch])))]
        copay = 0.0 if row.cls in ("HIV",) else float(min(150.0, round(0.1 * row.paid26, 2)))
        if row.date < W.SWITCH:
            fac = W.ORRIN_PRICE_FACTOR[row.date.year]
            ing = round(row.units * p["price"] * fac, 2)
            fee = 1.50
            paid = round(ing + fee - copay, 2)
            ndc10 = "%s-%s-%s" % (row.ndc11[:5], row.ndc11[6:9], row.ndc11[9:])
            n_o += int(r.integers(3, 40))
            line = [str(n_o), "PAID", row.date.isoformat(), idm["orrin"][row.member], ndc10, p["product"],
                    "%g" % row.units, str(row.days), "%.2f" % ing, "%.2f" % fee, "%.2f" % copay, "%.2f" % paid, npi]
            orrin.append(line)
            if r.random() < 0.025:      # reversed, and usually rebilled
                rev = list(line)
                rev[1] = "REVERSAL"
                for k in (6, 8, 9, 10, 11):
                    rev[k] = "-" + rev[k] if not rev[k].startswith("-") and float(rev[k]) != 0 else rev[k]
                orrin.append(rev)
                n_o += int(r.integers(3, 40))
                rebill = list(line)
                rebill[0] = str(n_o)
                orrin.append(rebill)
        else:
            ing = round(row.units * p["price"], 2)
            fee = W.DISPENSING_FEE
            paid = round(ing + fee - copay, 2)
            n_t += 1
            cid = "TPS26%07d" % (n_t * 7 + int(r.integers(0, 7)))
            line = [cid, "P", row.date.strftime("%m/%d/%Y"), idm["tallis"][row.member], row.ndc11, "%g" % row.units,
                    str(row.days), "%.2f" % ing, "%.2f" % fee, "%.2f" % copay, "%.2f" % paid, npi, ch]
            tallis.append(line)
            if r.random() < 0.03:
                rev = list(line)
                rev[1] = "R"
                tallis.append(rev)
                n_t += 1
                re_ = list(line)
                re_[0] = "TPS26%07d" % (n_t * 7 + int(r.integers(0, 7)))
                tallis.append(re_)
    x["claims"] = (orrin, tallis)
    x["channels"] = chans
    return x["claims"]


def crosswalk_rows(x):
    idm = ids(x)
    rows = []
    for m, pid in idm["plan"].items():
        rows.append([pid, idm["orrin"].get(m, ""), idm["tallis"].get(m, "")])
    rows.sort()
    return rows


def drug_rows():
    rows = []
    for p in S.PROD.itertuples(index=False):
        for pk in [p.pack] + ([p.pack_long] if isinstance(p.pack_long, str) else []):
            rows.append([p.labeler + p.code + pk, p.product, pk, p.cls, W.CLASSES[p.cls]["name"],
                         "Subcutaneous" if ("pen" in p.product or "syringe" in p.product) else "Oral"])
    return sorted(rows)


def price_rows():
    rows = []
    for p in S.PROD.itertuples(index=False):
        for pk in [p.pack] + ([p.pack_long] if isinstance(p.pack_long, str) else []):
            rows.append((p.labeler + p.code + pk, p.product, round(p.price, 2), W.DISPENSING_FEE))
    return sorted(rows)


def rebate_rows(x):
    """Orrin's 2025 rebate statement: one line for each product, channel and utilization quarter, carrying that line's
    units and the product's rebate for the quarter (all channels); with the prior year's last quarter invoiced in 2025."""
    f = x["fills"]
    claims(x)
    f = f[(f["date"] >= W.FIRST_MONTH) & (f["date"] <= W.LAST_DAY)].sort_values(["date", "member"], kind="stable").copy()
    f["channel"] = x["channels"]
    f = f[(f["date"] >= dt.date(2024, 10, 1)) & (f["date"] < W.SWITCH)]
    f["q"] = ["%dQ%d" % (d.year, (d.month - 1) // 3 + 1) for d in f["date"]]
    rows = []
    prod = S.PROD
    for (pi, q), g in f.groupby(["prod", "q"]):
        p = prod.loc[pi]
        amount = round(g["units"].sum() * p["rebate"] * (W.REBATE_2024 if q.startswith("2024") else 1.0), 2)
        inv = {"2024Q4": "2025Q1", "2025Q1": "2025Q2", "2025Q2": "2025Q3", "2025Q3": "2025Q4", "2025Q4": "2026Q1"}[q]
        for ch, gc in g.groupby("channel"):
            rows.append([inv, q, p["product"], p["cls"], ch, float(gc["units"].sum()), amount])
    rows.sort(key=lambda r: (r[0], r[2], r[4]))
    return rows


def truth_rebates(x):
    rows = rebate_rows(x)
    seen, out = set(), {c: 0.0 for c in W.CANDIDATES}
    for inv, q, prod, cls, ch, units, amount in rows:
        if q.startswith("2025") and (prod, q) not in seen:
            seen.add((prod, q))
            out[cls] += amount
    return out
