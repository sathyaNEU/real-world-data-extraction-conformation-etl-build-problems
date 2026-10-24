"""Assembles the world into the pack: the claims' inpatient days placed so each provider number's inpatient share sits
mid-cell, each provider number's wage index solved so its cap ratio sits where the design puts it (Fallowmere's
repayment mid-cell), then the remittances. Returns everything the writers and the golden need."""
import numpy as np

import world as W
import records as R
import tables as T
import golden as Gd

FAL_TARGET = 0.285e6           # Fallowmere's golden repayment, so the standing family spans the 0.3 cell's middle
RATIO = {"BRK": 0.8873, "COR": 0.5482, "DUN": 0.7811, "LIN": 0.8962, "PEN": 0.4927, "SAL": 0.8768, "WEX": 0.8691}


def fy_days_by_ccn(people):
    out = {}
    for b in people:
        for code in W.CODES:
            d = W.fy_days(b.eps, code)
            if d:
                out[R.CCN[code]] = out.get(R.CCN[code], 0) + d
    return out


def place_shares(allc, days):
    """Move each provider number's paid general inpatient days by whole days so its inpatient share sits within 0.018
    of a printed value (the middle of its cell): a routine day on a paid original that carries no device becomes a
    general inpatient day, or the last day of a general inpatient run becomes routine, each repriced at its own tier."""
    rng = R.stream(7)
    for code in W.CODES:
        ccn = R.CCN[code]
        paid = [c for c in R.paid_versions(allc) if c["code"] == code]
        g = sum(R.paid_units(c, "G") + R.paid_units(c, "I") for c in paid)
        n = days[ccn]
        s = 100.0 * g / n
        target = round(s, 1) + float(rng.uniform(-0.018, 0.018))
        delta = int(round((target - s) * n / 100.0))
        free = [c for c in paid if c["kind"] == "original" and "returned_rep" not in c and "review" not in c
                and "replaced_by" not in c and "voided_by" not in c]
        free.sort(key=lambda c: c["key"])
        while delta != 0:
            if delta > 0:
                cands = [c for c in free if c["units"]["R"] >= 5 and c["units"]["G"] == 0 and c["units"]["I"] == 0]
                c = cands[int(rng.integers(len(cands)))]
                spots = [j for j in range(1, len(c["days"]) - 1) if c["days"][j][1] == "R"
                         and c["days"][j - 1][1] == "R" and c["days"][j + 1][1] == "R"]
                j = spots[int(rng.integers(len(spots)))]
                to, step = "G", 1
            else:
                cands = [c for c in free if c["units"]["G"] >= 2]
                c = cands[int(rng.integers(len(cands)))]
                ends = [j for j, d in enumerate(c["days"]) if d[1] == "G"
                        and (j + 1 == len(c["days"]) or c["days"][j + 1][1] != "G")]
                j = ends[int(rng.integers(len(ends)))]
                to, step = "R", -1
            d, x, hi, q = c["days"][j]
            c["days"] = c["days"][:j] + [(d, to, hi, q)] + c["days"][j + 1:]
            R.refresh(c)
            delta -= step


def solve_wage_index(allc, counts):
    """Each provider number's wage index, four decimals, so its FY2026 payments sit at its designed cap ratio, and
    Fallowmere's at its cap plus the target repayment."""
    paid = R.paid_versions(allc)
    wi = {}
    for code in W.CODES:
        fixed = sum(c["fixed"] for c in paid if c["code"] == code)
        labor = sum(c["labor"] for c in paid if c["code"] == code)
        cap = counts[R.CCN[code]] * W.CAP
        target = cap + FAL_TARGET / 0.98 if code == "FAL" else RATIO[code] * cap
        wi[code] = round((target - fixed) / labor, 4)
    return wi


def build():
    bens = W.simulate()
    people = R.build(bens)
    tb = T.build(people)
    claims = R.build_claims(people)
    allc = R.versions(claims)
    days = fy_days_by_ccn(people)
    place_shares(allc, days)
    book = Gd.Book(tb, R.CCN.values())
    est = Gd.Estimates(book)
    cohort = Gd.cohort(book)
    gold = Gd.counts(cohort, est, **Gd.RUNGS["G"])
    wi = solve_wage_index(allc, gold)
    rem = R.remittances(allc, wi)
    return dict(bens=bens, people=people, tb=tb, claims=allc, days=days, book=book, est=est, cohort=cohort,
                gold=gold, wi=wi, remit=rem)


if __name__ == "__main__":
    P = build()
    pay = {}
    for r in P["remit"]:
        if r["record"] == "CLP":
            pay[r["provider_number"]] = pay.get(r["provider_number"], 0.0) + r["paid"] + r["sequestration"]
    inv = {v: k for k, v in R.CCN.items()}
    for ccn in sorted(pay, key=lambda c: inv[c]):
        cnt = P["gold"][ccn]
        print("%s wi %.4f payments %.2f count %.3f cap %.2f ratio %.4f repay %.0f" % (
            inv[ccn], P["wi"][inv[ccn]], pay[ccn], cnt, cnt * W.CAP, pay[ccn] / (cnt * W.CAP), Gd.repayment(pay[ccn], cnt)))
