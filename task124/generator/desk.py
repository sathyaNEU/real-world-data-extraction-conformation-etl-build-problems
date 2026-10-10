"""The trading desk's records behind the two price asks: broker quotes (two brokers in the desk's quote file, the third
on its own sheet), the desk's quote decisions, the counterparty master, the book-to-load-zone map, the trade blotter,
the confirmation matching log, the portfolio crosswalk, the 2027 trading calendar and the position report."""
from __future__ import annotations

from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

from common import BOOKS, HEDGES, all_hours_7x16, nerc_holidays, onpeak_hours

ZONES = ["LZ_HOUSTON", "LZ_NORTH", "LZ_SOUTH", "LZ_WEST"]
MONTHS = [6, 7, 8, 9]
MAP_2026 = {"Coast": "LZ_HOUSTON", "East": "LZ_NORTH", "Far West": "LZ_WEST", "North": "LZ_WEST",
            "North Central": "LZ_NORTH", "South Central": "LZ_SOUTH", "Southern": "LZ_SOUTH", "West": "LZ_WEST"}
MAP_2027 = dict(MAP_2026, East="LZ_HOUSTON")
BROKERS = {"GEB": ("Gulfline Energy Brokers", "5x16"), "TBC": ("Trinity Basin Capital Markets", "7x16"),
           "PPB": ("Pecos Power Brokerage", "5x16")}
PECOS_ZONE = {"LZ_HOUSTON": "Houston LZ", "LZ_NORTH": "North LZ", "LZ_SOUTH": "South LZ", "LZ_WEST": "West LZ"}

# counterparty master: code, legal name, approved from, approved to (None = open)
CPTY = [
    ("C0112", "Redgate Power Marketing LLC", date(2016, 3, 1), None),
    ("C0147", "Coldwater Bend Energy LP", date(2017, 9, 15), None),
    ("C0188", "Mesquite Flats Trading LLC", date(2019, 1, 7), date(2027, 3, 31)),
    ("C0203", "Kestrel Point Energy Trading Inc", date(2020, 5, 11), None),
    ("C0231", "Hollis Creek Energy Trading Inc", date(2018, 5, 1), date(2025, 10, 31)),
    ("C0231", "Saltgrass Energy LP", date(2026, 6, 15), None),
    ("C0256", "Blue Mesa Power & Gas LLC", date(2021, 2, 1), None),
    ("C0262", "Ironwood Commodities LP", date(2022, 7, 18), date(2024, 12, 31)),
    ("C0274", "Harbor Light Energy Supply LLC", date(2023, 4, 3), None),
    ("C0291", "Prairie Hen Energy LLC", date(2025, 8, 4), None),
    ("C0305", "Northbank Commodity Partners LP", date(2019, 3, 18), date(2023, 6, 30)),
    ("C0318", "Granite Shoals Power Trading LLC", date(2026, 9, 21), None),
]
VALID = ["C0112", "C0147", "C0203", "C0256", "C0274"]

# 5x16 premium per MWh the market sits near, by zone and month (USD)
BASE = {"LZ_HOUSTON": [6.85, 15.40, 23.10, 9.25], "LZ_NORTH": [6.40, 14.20, 21.70, 8.60],
        "LZ_SOUTH": [7.10, 15.90, 24.30, 9.80], "LZ_WEST": [8.30, 17.60, 26.90, 11.40]}

# per cell: winning broker, winner flags, decoys priced under the winner
PLAN = {
    ("LZ_HOUSTON", 6): ("PPB", set(), {"declined", "tbcmis"}),
    ("LZ_HOUSTON", 7): ("PPB", set(), {"lapsed", "tbcmis"}),
    ("LZ_HOUSTON", 8): ("PPB", {"reissued"}, {"declined"}),
    ("LZ_HOUSTON", 9): ("GEB", {"rev2"}, {"lapsed", "tbcmis"}),
    ("LZ_NORTH", 6): ("TBC", {"reissued"}, {"declined"}),
    ("LZ_NORTH", 7): ("PPB", set(), {"declined", "tbcmis"}),
    ("LZ_NORTH", 8): ("PPB", set(), {"lapsed"}),
    ("LZ_NORTH", 9): ("PPB", set(), {"declined", "tbcmis"}),
    ("LZ_SOUTH", 6): ("PPB", set(), {"lapsed", "tbcmis"}),
    ("LZ_SOUTH", 7): ("GEB", {"reissued"}, {"declined", "tbcmis"}),
    ("LZ_SOUTH", 8): ("PPB", set(), {"declined"}),
    ("LZ_SOUTH", 9): ("TBC", {"rev2"}, {"lapsed"}),
    ("LZ_WEST", 6): ("GEB", {"rev2"}, {"declined", "tbcmis"}),
    ("LZ_WEST", 7): ("PPB", set(), {"declined"}),
    ("LZ_WEST", 8): ("TBC", set(), {"lapsed"}),
    ("LZ_WEST", 9): ("PPB", set(), {"lapsed", "tbcmis"}),
}


def hours(shape, m, holidays=True):
    return onpeak_hours(2027, m, holidays) if shape == "5x16" else all_hours_7x16(2027, m)


def _clear_price(value, shape, m):
    """The quoted price nearest the planned value whose dollar conversions under every hour count a reader might use
    sit at least six cents from a half-dollar edge."""
    hs = {hours(shape, m), hours("5x16", m, False), hours("5x16", m)}
    base = round(value / hours(shape, m), 2)
    for k in range(60):
        for p in (round(base + 0.01 * k, 2), round(base - 0.01 * k, 2)):
            if all(abs(((p * h) % 1.0) - 0.5) >= 0.06 for h in hs):
                return p
    raise AssertionError("no clear price")


def build_quotes(rng):
    """Quotes as sent. Each row: id, revision, broker, cpty (code; Pecos rows carry the seller's name), zone, month,
    price per MWh, sent time, decision. Values are planned in USD per MW-month and converted to each broker's price."""
    rows = []
    qn = [41_207]

    def qid():
        qn[0] += int(rng.integers(1, 6))
        return qn[0]
    pref = [0]

    def pref_id():
        pref[0] += 1
        return f"PPB-27-{318 + 3 * pref[0] + int(rng.integers(0, 3)):04d}"

    def sent(day_lo=1, day_hi=9):
        d = date(2027, 4, int(rng.integers(day_lo, day_hi + 1)))
        while d.weekday() >= 5:
            d -= timedelta(days=1)
        return datetime(2027, 4, d.day, int(rng.integers(7, 16)), int(rng.integers(0, 60)), int(rng.integers(0, 60)))

    def add(broker, value, zone, m, cpty, decision, rev=1, revs_before=None, when=None):
        shape = BROKERS[broker][1]
        price = _clear_price(value, shape, m)
        ident = pref_id() if broker == "PPB" else qid()
        t = when or (sent(3, 9) if revs_before else sent())
        if revs_before:
            for k, pv in enumerate(revs_before, start=1):
                p0 = _clear_price(pv, shape, m)
                rows.append(dict(qid=ident, rev=k, broker=broker, cpty=cpty, zone=zone, month=m, price=p0,
                                 sent=t - timedelta(hours=26 * (len(revs_before) - k + 1)), decision="SUPERSEDED"))
            rev = len(revs_before) + 1
        rows.append(dict(qid=ident, rev=rev, broker=broker, cpty=cpty, zone=zone, month=m, price=price, sent=t,
                         decision=decision))

    for (z, m), (win, flags, decoys) in PLAN.items():
        h5 = hours("5x16", m)
        v = BASE[z][m - 6] * h5 * float(rng.uniform(0.97, 1.03))
        v = np.floor(v) + float(rng.choice([0.18, 0.27, 0.36, 0.64, 0.73, 0.82]))
        cp = "C0231" if "reissued" in flags else str(rng.choice(VALID))
        prior = [v * float(rng.uniform(1.035, 1.06))] if "rev2" in flags else None
        add(win, v, z, m, cp, "ACCEPTED", revs_before=prior)
        # the field: every broker quotes the cell above the winner, at least 2 per cent above
        for b in ("GEB", "TBC", "PPB"):
            if b == win:
                k = 1
            else:
                k = 1 + int(rng.integers(0, 2))
            for _ in range(k):
                add(b, v * float(rng.uniform(1.025, 1.11)), z, m, str(rng.choice(VALID)), "ACCEPTED")
        if "declined" in decoys:
            add(str(rng.choice(["GEB", "PPB"])), v * float(rng.uniform(0.94, 0.975)), z, m, str(rng.choice(VALID)),
                "DECLINED")
        if "lapsed" in decoys:
            add(str(rng.choice(["GEB", "PPB"])), v * float(rng.uniform(0.935, 0.97)), z, m, "C0188", "ACCEPTED")
        if "tbcmis" in decoys:
            # a 7x16 quote above the winner that reads under it when taken at 5x16 hours
            add("TBC", v * float(rng.uniform(1.12, 1.24)), z, m, str(rng.choice(VALID)), "ACCEPTED")
    q = pd.DataFrame(rows)
    # identifiers run in the order the quotes first arrived, as the quote line and Pecos number them
    first = q.groupby("qid")["sent"].min().sort_values(kind="mergesort")
    gb = [k for k in first.index if not str(k).startswith("PPB")]
    pp = [k for k in first.index if str(k).startswith("PPB")]
    ren = {k: 41_208 + 3 * i + int(rng.integers(0, 3)) for i, k in enumerate(gb)}
    ren.update({k: f"PPB-27-{318 + 3 * i + int(rng.integers(0, 3)):04d}" for i, k in enumerate(pp)})
    q["qid"] = q["qid"].map(ren)
    names = {c: n for c, n, f, t in CPTY if t is None or t >= date(2027, 1, 1)}
    names["C0231"] = "Saltgrass Energy LP"
    q["seller"] = q["cpty"].map(names)
    return q


def cpty_valid_on(code, when: date):
    return any(c == code and f <= when and (t is None or when <= t) for c, n, f, t in CPTY)


def premium_answer(q, zone_map=MAP_2027, holidays=True, drop_revised_reissued=False, decisions=True,
                   approval=True, pecos=True, notional=True, latest_rev_only=False):
    """USD per MW-month by book and month under a set of handling choices (the answer with every default True)."""
    d = q.copy()
    if not pecos:
        d = d[d["broker"] != "PPB"]
    if latest_rev_only:
        d = d.sort_values("rev").groupby("qid").tail(1)
    if decisions:
        d = d[d["decision"] == "ACCEPTED"]
    if approval:
        d = d[[cpty_valid_on(c, s.date()) for c, s in zip(d["cpty"], d["sent"])]]
    if drop_revised_reissued:
        revised = set(q.loc[q["rev"] > 1, "qid"])
        d = d[~d["qid"].isin(revised) & (d["cpty"] != "C0231")]
    shape = d["broker"].map(lambda b: BROKERS[b][1] if notional else "5x16")
    d = d.assign(usd=[p * hours(s, m, holidays) for p, s, m in zip(d["price"], shape, d["month"])])
    best = d.groupby(["zone", "month"])["usd"].min()
    return {(b, m): float(best[(zone_map[b], m)]) for b in BOOKS for m in MONTHS}


# ------------------------------------------------------------------------------ hedges
PORTFOLIOS = {"Coast": ["HOU-CI", "HOU-LCI"], "East": ["ETX-CI"], "Far West": ["FWT-CI"], "North": ["NTX-CI"],
              "North Central": ["DFW-CI", "DFW-LCI"], "South Central": ["CTX-CI", "CTX-LCI"], "Southern": ["STX-CI"],
              "West": ["WTX-CI"]}
# summer 2027 strips per book: (MW, shape, amendment plan) where plan is "", "m" (one matched price amendment),
# "u" (one matched amendment then an unmatched second), "x" (an unmatched first amendment)
STRIPS = {
    "Coast": [(100, "5x16", "m"), (75, "7x16", "u"), (50, "5x16", ""), (125, "5x16", "x"), (50, "7x16", ""), (75, "5x16", "")],
    "East": [(50, "5x16", "u"), (40, "7x16", ""), (30, "5x16", "m"), (25, "7x16", "")],
    "Far West": [(35, "5x16", "m"), (40, "7x16", "x"), (20, "5x16", "")],
    "North": [(30, "5x16", ""), (25, "7x16", "m"), (25, "5x16", "u")],
    "North Central": [(100, "5x16", "u"), (60, "7x16", "m"), (75, "5x16", ""), (80, "7x16", ""), (50, "5x16", "x")],
    "South Central": [(90, "5x16", "x"), (70, "7x16", ""), (60, "5x16", "m"), (60, "7x16", "")],
    "Southern": [(45, "5x16", ""), (40, "7x16", "u"), (35, "5x16", "m")],
    "West": [(50, "5x16", "u"), (45, "7x16", "m"), (40, "5x16", "")],
}
ZCODE = {"LZ_HOUSTON": "HZ", "LZ_NORTH": "NZ", "LZ_SOUTH": "SZ", "LZ_WEST": "WZ"}


def build_trades(rng):
    """Blotter rows (every booked amendment) and the matching log."""
    blot, match = [], []
    tid = [270_400]

    def nid():
        tid[0] += int(rng.integers(3, 40))
        return f"SCT-{tid[0]}"

    def cp():
        return str(rng.choice(VALID))

    for b in BOOKS:
        assert sum(x[0] for x in STRIPS[b]) == HEDGES[b], b
        for k, (mw, shape, plan) in enumerate(STRIPS[b]):
            pf = PORTFOLIOS[b][k % len(PORTFOLIOS[b])]
            zone = MAP_2027[b] if k % 2 == 0 else MAP_2026[b]
            base = (rng.uniform(78, 94) if shape == "5x16" else rng.uniform(59, 72))
            p0 = round(base, 2)
            td = date(2025, 5, 1) + timedelta(days=int(rng.integers(0, 500)))
            while td.weekday() >= 5:
                td += timedelta(days=1)
            t = nid()
            prod = f"ERCOT.{ZCODE[zone]}.{shape.upper()}"
            row = dict(trade_id=t, portfolio=pf, cpty=cp(), product=prod, start=date(2027, 6, 1), end=date(2027, 9, 30),
                       mw=mw, trade_date=td)
            blot.append(dict(row, amend=0, price=p0, booked=td))
            match.append((t, 0, "MATCHED", td + timedelta(days=int(rng.integers(1, 4)))))
            when = td + timedelta(days=int(rng.integers(8, 60)))
            if plan in ("m", "u"):
                p1 = round(p0 + float(rng.choice([-1, 1])) * float(rng.uniform(0.9, 2.4)), 2)
                blot.append(dict(row, amend=1, price=p1, booked=when))
                match.append((t, 1, "MATCHED", when + timedelta(days=int(rng.integers(1, 5)))))
                if plan == "u":
                    w2 = when + timedelta(days=int(rng.integers(20, 90)))
                    p2 = round(p1 + float(rng.choice([-1, 1])) * float(rng.uniform(1.6, 3.2)), 2)
                    blot.append(dict(row, amend=2, price=p2, booked=w2))
                    match.append((t, 2, "DISPUTED", w2 + timedelta(days=3)))
                    match.append((t, 2, "WITHDRAWN", w2 + timedelta(days=int(rng.integers(9, 30)))))
            if plan == "x":
                p1 = round(p0 + float(rng.choice([-1, 1])) * float(rng.uniform(1.8, 3.4)), 2)
                blot.append(dict(row, amend=1, price=p1, booked=when))
                match.append((t, 1, "DISPUTED", when + timedelta(days=2)))
                match.append((t, 1, "WITHDRAWN", when + timedelta(days=int(rng.integers(10, 40)))))
    # trades outside the summer 2027 strips: delivered summer 2026, Q4 2027 and calendar 2028
    for b in BOOKS:
        for start, end, shape in ((date(2026, 6, 1), date(2026, 9, 30), "5x16"), (date(2027, 10, 1), date(2027, 12, 31), "7x16"),
                                  (date(2028, 1, 1), date(2028, 12, 31), "5x16")):
            if rng.uniform() < 0.25 and start.year != 2026:
                continue
            t = nid()
            td = start - timedelta(days=int(rng.integers(90, 400)))
            while td.weekday() >= 5:
                td += timedelta(days=1)
            td = min(td, date(2027, 4, 7))
            mw = int(5 * rng.integers(4, 21))
            price = round(rng.uniform(52, 90), 2)
            blot.append(dict(trade_id=t, portfolio=PORTFOLIOS[b][0], cpty=cp(),
                             product=f"ERCOT.{ZCODE[(MAP_2027 if start.year >= 2027 else MAP_2026)[b]]}.{shape.upper()}", start=start, end=end, mw=mw,
                             trade_date=td, amend=0, price=price, booked=td))
            match.append((t, 0, "MATCHED", td + timedelta(days=2)))
    # a cancelled Q4 2026 strip, booked and voided the same week (no confirmation)
    t = nid()
    blot.append(dict(trade_id=t, portfolio="WTX-CI", cpty="C0256", product="ERCOT.WZ.5X16", start=date(2026, 10, 1),
                     end=date(2026, 12, 31), mw=15, trade_date=date(2026, 8, 12), amend=0, price=61.85,
                     booked=date(2026, 8, 12)))
    match.append((t, 0, "CANCELLED", date(2026, 8, 14)))
    bl = pd.DataFrame(blot)
    ml = pd.DataFrame(match, columns=["trade_id", "amend", "status", "status_date"])
    # keep every book's average a clear tenth of a cent from a half-cent edge: nudge one unamended strip by a cent
    from common import bin_distance
    pf = {p: b for b, ps in PORTFOLIOS.items() for p in ps}
    amended = set(bl.loc[bl["amend"] > 0, "trade_id"])
    for b in BOOKS:
        for _ in range(40):
            if bin_distance(hedge_price_answer(bl, ml)[b], 0.01) >= 0.0015:
                break
            cand = bl[(bl["portfolio"].map(pf) == b) & (bl["start"] == date(2027, 6, 1)) & ~bl["trade_id"].isin(amended)]
            i = cand.index[0]
            bl.at[i, "price"] = round(bl.at[i, "price"] + 0.01, 2)
        else:
            raise AssertionError(b)
    assert bl["booked"].max() <= date(2027, 4, 9) and ml["status_date"].max() <= date(2027, 4, 9), "dates after extract"
    return bl, ml


def summer_hours(shape, holidays=True):
    return sum(hours(shape, m, holidays) for m in MONTHS)


def hedge_price_answer(bl, ml, version="matched", weight="mwh", holidays=True):
    """Average fixed price per book on its summer 2027 strips, USD/MWh."""
    s = bl[(bl["start"] == date(2027, 6, 1)) & (bl["end"] == date(2027, 9, 30))].copy()
    if version == "latest":
        s = s.sort_values("amend").groupby("trade_id").tail(1)
    elif version == "original":
        s = s[s["amend"] == 0]
    else:
        last = ml.sort_values(["status_date"]).groupby(["trade_id", "amend"]).tail(1)
        ok = set(map(tuple, last.loc[last["status"] == "MATCHED", ["trade_id", "amend"]].to_numpy()))
        s = s[[(t, a) in ok for t, a in zip(s["trade_id"], s["amend"])]]
        s = s.sort_values("amend").groupby("trade_id").tail(1)
    pf = {p: b for b, ps in PORTFOLIOS.items() for p in ps}
    s["book"] = s["portfolio"].map(pf)
    s["shape"] = s["product"].str.split(".").str[2].str.lower()
    if weight == "mw":
        s["w"] = s["mw"].astype(float)
    else:
        s["w"] = s["mw"] * s["shape"].map(lambda x: summer_hours(x, holidays))
    g = s.groupby("book")
    return {b: float((g.get_group(b)["price"] * g.get_group(b)["w"]).sum() / g.get_group(b)["w"].sum()) for b in BOOKS}
