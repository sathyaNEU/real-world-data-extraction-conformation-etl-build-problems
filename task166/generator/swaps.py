"""The bank's interest-rate swaps at the close on 30 November 2026: the hedge programme (ALCO's book) and the
customer programme (borrower swaps and their dealer offsets). Clean truth only; records.py writes the treasury
system's register, the amortisation schedules and the clearing broker's statement from it.

Four of the programme's uncleared trades with one dealer were backloaded into clearing on Friday 18 September 2026;
the treasury system booked the cleared trades and still carries the bilateral originals as live (their closes wait on
the dealer's termination confirmations). Two genuine pairs were executed the same way on purpose: one leg with a dealer
bilaterally, one leg cleared, identical terms."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

D = dt.date
BACKLOAD = D(2026, 9, 18)

# dealers (invented names; the register carries the counterparty's short name)
DEALERS = ["Halvorsen Markets", "Pemberly Securities", "Larkmoor Capital Markets", "Corvane Bank NA",
           "Ostrander Securities"]
CCP = "CME Clearing"

# programme trades: key, direction (PAY = the bank pays fixed), notional, trade, effective, maturity, fixed rate,
# counterparty, cleared at inception, amortising, strategy, hedged item
PROGRAMME = [
    ("OV23", "PAY", 750_000_000, D(2023, 3, 14), D(2023, 3, 16), D(2028, 3, 16), 3.982, 0, False, True, "OVERLAY",
     "Residential mortgages originated 2019 to 2022"),
    ("OV24", "PAY", 312_500_000, D(2024, 6, 11), D(2024, 6, 13), D(2029, 6, 13), 4.207, 4, False, False, "OVERLAY",
     "Municipal securities, available for sale"),
    ("OV25A", "PAY", 400_000_000, D(2025, 12, 9), D(2026, 1, 6), D(2030, 1, 6), 3.465, 2, False, False, "OVERLAY",
     "Agency multifamily securities bought 2022 and 2023"),
    ("OV25B", "PAY", 400_000_000, D(2025, 12, 9), D(2026, 1, 6), D(2030, 1, 6), 3.465, 1, True, False, "OVERLAY",
     "Agency multifamily securities bought 2022 and 2023"),
    ("FH1", "PAY", 275_000_000, D(2023, 2, 8), D(2023, 2, 10), D(2028, 2, 10), 3.851, 0, False, False, "FUNDING",
     "Residential mortgages originated 2019 to 2022, second layer"),
    ("FH2", "PAY", 250_000_000, D(2023, 8, 15), D(2023, 8, 17), D(2027, 8, 17), 4.418, 3, False, False, "FUNDING",
     "Brokered certificates of deposit, rollovers"),
    ("FH3", "PAY", 187_500_000, D(2024, 4, 9), D(2024, 4, 11), D(2029, 4, 11), 4.052, 4, False, False, "FUNDING",
     "Federal Home Loan Bank advances, rollovers"),
    ("FH4", "PAY", 350_000_000, D(2026, 10, 20), D(2027, 7, 1), D(2031, 7, 1), 3.574, 1, True, False, "FUNDING",
     "Brokered certificates of deposit, forecast issuance"),
    ("RF1", "REC", 400_000_000, D(2022, 4, 12), D(2022, 4, 14), D(2027, 4, 14), 2.712, 1, False, False, "LOAN",
     "SOFR-indexed commercial loans, interest"),
    ("RF2", "REC", 325_000_000, D(2022, 9, 13), D(2022, 9, 15), D(2027, 9, 15), 3.618, 2, False, False, "LOAN",
     "SOFR-indexed commercial loans, interest"),
    ("RF3", "REC", 250_000_000, D(2023, 1, 10), D(2023, 1, 12), D(2028, 1, 12), 3.552, 0, False, False, "LOAN",
     "SOFR-indexed commercial real estate loans, interest"),
    ("RF4", "REC", 250_000_000, D(2023, 1, 10), D(2023, 1, 12), D(2028, 1, 12), 3.552, 3, True, False, "LOAN",
     "SOFR-indexed commercial real estate loans, interest"),
    ("RF5", "REC", 362_500_000, D(2023, 6, 6), D(2023, 6, 8), D(2028, 6, 8), 3.804, 4, False, False, "LOAN",
     "SOFR-indexed commercial loans, interest"),
    ("RF6", "REC", 212_500_000, D(2023, 11, 7), D(2023, 11, 9), D(2028, 11, 9), 4.149, 4, False, False, "LOAN",
     "SOFR-indexed commercial loans, interest"),
    ("RF7", "REC", 300_000_000, D(2024, 3, 5), D(2024, 3, 7), D(2029, 3, 7), 3.951, 2, True, True, "LOAN",
     "SOFR-indexed commercial loans, interest"),
    ("RF8", "REC", 200_000_000, D(2022, 3, 15), D(2022, 3, 17), D(2027, 3, 17), 2.235, 3, False, False, "LOAN",
     "SOFR-indexed commercial loans, interest"),
    ("RF9", "REC", 250_000_000, D(2022, 6, 7), D(2022, 6, 9), D(2027, 6, 9), 3.105, 0, False, False, "LOAN",
     "SOFR-indexed commercial loans, interest"),                    # terminated 2025-06-17
]
TERMINATED = {"RF9": D(2025, 6, 17)}
BACKLOADED = ("OV24", "FH3", "RF5", "RF6")   # Ostrander's four uncleared trades
FH1_REDESIGNATED = D(2026, 4, 1)             # the strategy column keeps the label set at trade entry

# OV23 amortises with the 2019-22 mortgage pool's expected run-off at inception: quarterly resets on the 16th, flat
# for the first year, then the pool's projected balance at a constant 9.6 per cent a year
OV23_STEPS = [750.0] * 4 + [round(750.0 * (1 - 0.096) ** (k / 4.0), 1) for k in range(1, 17)]


def quarter_dates(eff, mat, months=3):
    out = [eff]
    y, m = eff.year, eff.month
    while True:
        m += months
        y += (m - 1) // 12
        m = (m - 1) % 12 + 1
        d = D(y, m, min(eff.day, 28 if m == 2 else 30 if m in (4, 6, 9, 11) else 31))
        if d >= mat:
            out.append(mat)
            break
        out.append(d)
    return out


# RF7 amortises with the hedged loans' scheduled paydown: semi-annual resets on the 7th of March and September
RF7_STEPS = [300.0, 300.0] + [round(300.0 * (1 - 0.074) ** (k / 2.0), 1) for k in range(1, 9)]


def rf7_schedule():
    t = [x for x in PROGRAMME if x[0] == "RF7"][0]
    ds = quarter_dates(t[4], t[5], months=6)
    return [(ds[i], ds[i + 1], round(RF7_STEPS[i] * 1_000_000, 2)) for i in range(len(ds) - 1)]


def ov23_schedule():
    t = [x for x in PROGRAMME if x[0] == "OV23"][0]
    ds = quarter_dates(t[4], t[5])
    rows = []
    for i in range(len(ds) - 1):
        rows.append((ds[i], ds[i + 1], round(OV23_STEPS[i] * 1_000_000, 2)))
    return rows


def build():
    g = K.rng(30)
    S = {}
    # trade numbers: seven digits, issued by the treasury system in booking order
    pool = list(range(4_100_000, 9_900_000, 1))
    nums = sorted(int(x) for x in g.choice(pool, size=len(PROGRAMME) + len(BACKLOADED) + 140, replace=False))
    k = 0
    trades = []
    for t in sorted(PROGRAMME, key=lambda x: x[3]):
        key, dirn, notl, td, eff, mat, rate, cp, cleared, amort, strat, item = t
        trades.append(dict(key=key, id=nums[k], dir=dirn, notional=notl, trade=td, eff=eff, mat=mat, rate=rate,
                           cpty=CCP if cleared else DEALERS[cp], exec_dealer=DEALERS[cp], cleared=cleared, amort=amort,
                           strategy=strat, item=item, book="ALM", status="TERMINATED" if key in TERMINATED else "LIVE",
                           terminated=TERMINATED.get(key), ccp_id=None, client_ref=None,
                           cleared_on=td if cleared else None))
        k += 1
    # the backload: a cleared trade booked for each of Ostrander's three, the bilateral originals still live
    for key in BACKLOADED:
        o = [x for x in trades if x["key"] == key][0]
        c = dict(o)
        c.update(key=key + "C", id=nums[k], cpty=CCP, cleared=True, cleared_on=BACKLOAD)
        trades.append(c)
        k += 1
    # customer programme: borrower swaps (the bank receives fixed) and their dealer offsets (the bank pays fixed)
    cust = []
    for j in range(70):
        td = D(2019, 1, 1) + dt.timedelta(days=int(g.integers(0, 2860)))
        eff = td + dt.timedelta(days=2)
        yrs = int(g.choice([5, 7, 10], p=[0.45, 0.35, 0.20]))
        mat = D(eff.year + yrs, eff.month, min(eff.day, 28))
        notl = round(float(np.exp(g.normal(np.log(9.5e6), 0.75))) / 50_000) * 50_000
        rate = round(float(g.uniform(1.2, 5.6)), 3)
        dealer = int(g.integers(0, 4))
        cleared = td >= D(2023, 1, 1) and g.random() < 0.6
        for side in ("CUST", "OFFSET"):
            cust.append(dict(key="C%02d%s" % (j, side[0]), id=nums[k], dir="REC" if side == "CUST" else "PAY",
                             notional=notl, trade=td, eff=eff, mat=mat,
                             rate=round(rate + (0.0 if side == "CUST" else -0.012), 3),
                             cpty=("Borrower %06d" % int(g.integers(100000, 999999))) if side == "CUST" else
                             (CCP if cleared else DEALERS[dealer]), exec_dealer=DEALERS[dealer],
                             cleared=side == "OFFSET" and cleared, amort=False,
                             strategy="CUSTOMER" if side == "CUST" else "CUSTOMER OFFSET", item="", book="CUSTOMER",
                             status="LIVE" if mat > K.AS_OF else "MATURED", terminated=None, ccp_id=None,
                             client_ref=None,
                             cleared_on=td if (side == "OFFSET" and cleared) else None))
            k += 1
    trades += cust
    # clearing references for every cleared trade; the client reference the bank gave the broker
    for t in trades:
        if t["cleared"]:
            t["ccp_id"] = "%d%06d" % (9, int(g.integers(100000, 999999)))
            if t["key"].endswith("C") and t["key"][:-1] in BACKLOADED:
                orig = [x for x in trades if x["key"] == t["key"][:-1]][0]
                t["client_ref"] = str(orig["id"])
            else:
                t["client_ref"] = str(t["id"])
    S["trades"] = trades
    S["ov23"] = ov23_schedule()
    S["rf7"] = rf7_schedule()
    S["sched"] = {"OV23": S["ov23"], "RF7": S["rf7"], "RF7C": S["rf7"]}
    return S


def notional_on(t, d, S):
    """the notional of trade t in effect on date d (effective on or before d, maturity and any termination after d)"""
    if t["status"] != "LIVE":
        return 0.0
    if not (t["eff"] <= d < t["mat"]) or (t.get("terminated") and d >= t["terminated"]):
        return 0.0
    if t["key"] in S["sched"]:
        for a, b, n in S["sched"][t["key"]]:
            if a <= d < b:
                return float(n)
        return 0.0
    return float(t["notional"])


QUARTER_ENDS = [D(2027, 3, 31), D(2027, 6, 30), D(2027, 9, 30), D(2027, 12, 31)]


def category(t):
    """the programme's categories as the policy defines them: an overlay is a pay-fixed swap designated against a
    fixed-rate asset pool, a funding hedge a pay-fixed swap on the bank's funding, a loan hedge a receive-fixed swap."""
    if t["dir"] == "REC":
        return "loan"
    if t["key"] == "FH1":
        return "overlay"           # designated against the 2019-22 mortgages from 1 April 2026
    return "overlay" if t["strategy"] == "OVERLAY" else "funding"


def ask_a_truth(S):
    """the hedge programme's notional in effect at each 2027 quarter-end by category, the new overlay included"""
    out = {c: [] for c in ("overlay", "funding", "loan")}
    live = [t for t in S["trades"] if t["book"] == "ALM" and t["status"] == "LIVE" and t["key"] not in BACKLOADED]
    for d in QUARTER_ENDS:
        tot = {"overlay": 0.0, "funding": 0.0, "loan": 0.0}
        for t in live:
            tot[category(t)] += notional_on(t, d, S)
        tot["overlay"] += K.NOTIONAL if K.EFFECTIVE <= d < K.MATURITY else 0.0
        for c in tot:
            out[c].append(tot[c])
    return out
