"""The records cut from the truth: the plan's monthly roster, the state's capitation remittance, the paid medical
claims, and the pharmacy claims behind the asks (which the call never reads)."""
import datetime as dt

import numpy as np

import sources as S
import world as W

RATE = {"TANF-ADULT": 412.18, "TANF-CHILD": 188.42, "ABD": 1294.66, "EXPANSION": 537.90}
CLASSES = ["ACE inhibitors", "Statins", "SSRIs", "Insulins", "Metformin", "Inhaled corticosteroids", "Anticonvulsants",
           "Atypical antipsychotics", "Proton pump inhibitors", "Beta blockers", "Thyroid hormones", "Opioid analgesics"]
# each class's share of fills and its mean paid per fill ($)
MIX = {"ACE inhibitors": (.09, 9.8), "Statins": (.13, 11.6), "SSRIs": (.12, 14.2), "Insulins": (.05, 412.0),
       "Metformin": (.10, 7.4), "Inhaled corticosteroids": (.08, 188.0), "Anticonvulsants": (.08, 61.0),
       "Atypical antipsychotics": (.05, 236.0), "Proton pump inhibitors": (.09, 12.9), "Beta blockers": (.08, 8.6),
       "Thyroid hormones": (.06, 13.3), "Opioid analgesics": (.07, 21.5)}


def month_add(d, k):
    y, m = d.year + (d.month - 1 + k) // 12, (d.month - 1 + k) % 12 + 1
    return dt.date(y, m, 1)


def build(rng, ms):
    cell = {}
    for x in ms:
        if W.GROUPS[x["group"]][0].startswith(("Riverside", "Prairie Gate", "Bluestem")) and rng.random() < .7:
            cell[x["mid"]] = "ABD"
        else:
            cell[x["mid"]] = str(rng.choice(["TANF-ADULT", "TANF-CHILD", "EXPANSION"], p=[.32, .4, .28]))
        if W.GROUPS[x["group"]][0].endswith("Pediatrics"):
            cell[x["mid"]] = "TANF-CHILD"
    roster, remit, claims = [], [], []
    # roster: one row per member per month on the roster
    for x in ms:
        for m in range(S.NM):
            if x["roster"][m]:
                roster.append(dict(month=W.MONTHS[m], mid=x["mid"], group=x["group"], cell=cell[x["mid"]]))
    # capitation: the month's capitation by rate cell for the members on that month's roster, paid in the month;
    # member-level lines for the months the state reinstated after a renewal lapse (paid when the reinstatement was
    # processed), for the months recouped after a member's death, and pairs moving a member between rate cells
    for m in range(S.NM):
        counts = {}
        for r in roster:
            if r["month"] == W.MONTHS[m]:
                counts[r["cell"]] = counts.get(r["cell"], 0) + 1
        pay = W.MONTHS[m] + dt.timedelta(days=int(rng.integers(8, 13)))
        for c in sorted(counts):
            remit.append(dict(pay=pay, mid="", cell=c, cov=W.MONTHS[m], n=counts[c], amt=round(counts[c] * RATE[c], 2)))
    for x in ms:
        c = cell[x["mid"]]
        if x["event"] and x["event"][0] == "lapse":
            a, b = x["event"][1], x["event"][2]
            proc = month_add(W.MONTHS[min(b, S.NM - 1)], int(rng.integers(0, 2)))
            pay = proc + dt.timedelta(days=int(rng.integers(8, 13)))
            for m in range(a, b):
                remit.append(dict(pay=pay, mid=x["mid"], cell=c, cov=W.MONTHS[m], n=1, amt=RATE[c]))
        if x["dead"] is not None:
            for m in range(x["dead"] + 1, S.NM):
                if x["roster"][m]:
                    pay = month_add(W.MONTHS[m], int(rng.integers(1, 4))) + dt.timedelta(days=int(rng.integers(8, 13)))
                    remit.append(dict(pay=pay, mid=x["mid"], cell=c, cov=W.MONTHS[m], n=-1, amt=-RATE[c]))
        if c != "TANF-CHILD" and rng.random() < .025:
            m = int(rng.integers(0, S.NM))
            if x["roster"][m] and x["cov"][m]:
                new = "ABD" if c != "ABD" else "TANF-ADULT"
                pay = month_add(W.MONTHS[m], int(rng.integers(1, 3))) + dt.timedelta(days=int(rng.integers(8, 13)))
                remit.append(dict(pay=pay, mid=x["mid"], cell=new, cov=W.MONTHS[m], n=1, amt=RATE[new]))
                remit.append(dict(pay=pay, mid=x["mid"], cell=c, cov=W.MONTHS[m], n=-1, amt=-RATE[c]))
    # paid medical claims: the month's cost split over claims, each paid some weeks after service (after the
    # reinstatement for a lapse month)
    cid = 26000000
    for x in ms:
        for m in range(S.NM):
            cost = x["cost"][m]
            if cost <= 0:
                continue
            k = max(1, min(int(rng.poisson(.25 + cost / 900)), int(cost // 25)))
            shares = rng.dirichlet(np.ones(k) * 1.4)
            for s in shares:
                cid += int(rng.integers(1, 30))
                day = int(rng.integers(0, 28))
                svc = W.MONTHS[m] + dt.timedelta(days=day)
                lag = int(rng.gamma(2.2, 9)) + 4
                if x["lapse"][m]:
                    proc = month_add(W.MONTHS[min(x["event"][2], S.NM - 1)], 1)
                    paid = max(svc + dt.timedelta(days=lag), proc + dt.timedelta(days=int(rng.integers(3, 25))))
                else:
                    paid = svc + dt.timedelta(days=lag)
                if paid > W.PAID_BY:
                    continue
                inst = rng.random() < (.22 + min(.5, cost / 4000))
                claims.append(dict(cid="C%d" % cid, mid=x["mid"], svc=svc,
                                   end=svc + dt.timedelta(days=int(rng.integers(0, 5)) if inst else 0),
                                   ctype="Institutional" if inst else "Professional", paid=paid,
                                   amt=round(float(cost * s), 2), npi=1000000000 + int(rng.integers(1, 9e8))))
    return dict(roster=roster, remit=remit, claims=claims, cell=cell)


def pharmacy(rng, ms):
    """Pharmacy claims: fills, each under its claim number, and later lines under the same number where the pharmacy
    rebilled a fill (a corrected quantity, product or fill date) or reversed it (paid now zero)."""
    rows = []
    num = 88100000
    for x in ms:
        n = int(rng.poisson(.3 * S.NM * min(3.0, .5 + x["risk"])))
        for _ in range(n):
            num += int(rng.integers(1, 12))
            cls = str(rng.choice(CLASSES, p=[MIX[c][0] for c in CLASSES]))
            fill = dt.date(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 190)))
            amt = round(float(rng.gamma(2.2, MIX[cls][1] / 2.2)), 2)
            proc = dt.datetime.combine(fill, dt.time(int(rng.integers(8, 21)), int(rng.integers(0, 60))))
            rows.append(dict(claim="RX%d" % num, mid=x["mid"], fill=fill, cls=cls, amt=amt, proc=proc,
                             qty=int(rng.choice([30, 30, 30, 60, 90]))))
            u = rng.random()
            later = proc + dt.timedelta(days=int(rng.integers(1, 20)), hours=int(rng.integers(1, 9)))
            if u < .04:
                rows.append(dict(rows[-1], amt=0.0, proc=later))
            elif u < .07:
                f2 = fill + dt.timedelta(days=int(rng.choice([-3, -2, 2, 3, 4])))
                later = max(later, dt.datetime.combine(f2, dt.time(9)) + dt.timedelta(hours=int(rng.integers(1, 30))))
                rows.append(dict(rows[-1], fill=f2, amt=round(amt * float(rng.uniform(.6, 1.2)), 2), proc=later))
            elif u < .09:
                c2 = str(rng.choice([c for c in CLASSES if c != cls]))
                rows.append(dict(rows[-1], cls=c2, amt=round(float(rng.gamma(2.2, MIX[c2][1] / 2.2)), 2), proc=later))
    return rows
