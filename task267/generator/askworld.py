"""The records behind the two asks, on their own random streams: the analysers that ran the season's HbA1c tests
(their asset tags, the units behind them, every run the units logged) and the laboratory's billing of the OGTTs."""
import datetime as dt

import numpy as np

import common as K

# error codes of the GQ-200 (the maker's quick reference): raised at the cartridge check (the cartridge is not
# accepted and may be inserted again) or during the measurement (the sample is in the cartridge; it is discarded)
ERRORS = [
    ("E-02", "Cartridge not recognised", "check"), ("E-04", "Cartridge past its expiry date", "check"),
    ("E-06", "Cartridge temperature outside 15 to 30 C", "check"), ("E-09", "Lid open at start", "check"),
    ("E-11", "Sample volume too low", "measure"), ("E-13", "Optical reference out of range", "measure"),
    ("E-15", "Haemoglobin outside 7 to 22 g/dL", "measure"), ("E-17", "Reaction timed out", "measure"),
]
ERR_W = [0.22, 0.10, 0.12, 0.08, 0.24, 0.10, 0.06, 0.08]
SPENT = {c for c, _, w in ERRORS if w == "measure"}

UNITS = {"A%02d" % i: "GQ2-%05d" % s for i, s in zip(range(1, 13), (41107, 41123, 41168, 41205, 41239, 41260, 41288,
                                                                   41317, 41342, 41376, 41391, 41414))}
REPLACE = {"A05": (dt.date(2026, 6, 18), "GQ2-47720"), "A11": (dt.date(2026, 9, 3), "GQ2-48815")}
LOANER = "GQ2-39046"
LOANS = [("A04", dt.date(2026, 5, 4), dt.date(2026, 5, 22)), ("A09", dt.date(2026, 8, 10), dt.date(2026, 8, 28))]
FIRST_IN = dt.date(2025, 11, 3)
REPEAT_AT = 6.5
EXPORT_AS_OF = dt.date(2027, 1, 6)

# Biomedical Engineering's downloads of the units' memories into its run database: before a unit ships to the maker,
# when a loan ends, and for every unit in service at mid-season and after the season. The docking software wrote
# local time until its upgrade on 3 August 2026 and the unit's own UTC clock after it; the database skips a row whose
# serial and run time it already holds. A unit keeps its last 2,600 runs; the maker's service clears the memory.
MEMORY = 2600
UPGRADE = dt.date(2026, 8, 3)
CLEARED = {"GQ2-41205": dt.date(2026, 5, 12), "GQ2-41342": dt.date(2026, 8, 18)}
DOWNLOADS = [(dt.date(2026, 5, 3), "GQ2-41205"), (dt.date(2026, 5, 22), LOANER), (dt.date(2026, 6, 17), "GQ2-41239"),
             (dt.date(2026, 7, 7), None), (dt.date(2026, 8, 9), "GQ2-41342"), (dt.date(2026, 8, 28), LOANER),
             (dt.date(2026, 9, 2), "GQ2-41391"), (dt.date(2026, 12, 4), None)]


def assignments():
    """The asset register's rows: which unit stood behind which asset tag, from when to when."""
    rows = []
    for tag in K.ASSETS:
        own = UNITS[tag]
        spans = [(own, FIRST_IN, None)]
        if tag in REPLACE:
            d, new = REPLACE[tag]
            spans = [(own, FIRST_IN, d - dt.timedelta(days=1)), (new, d, None)]
        for t, a, b in LOANS:
            if t == tag:
                out = []
                for s, f, to in spans:
                    if (to is None or to >= a) and f <= b:
                        out.append((s, f, a - dt.timedelta(days=1)))
                        out.append((LOANER, a, b))
                        out.append((s, b + dt.timedelta(days=1), to))
                    else:
                        out.append((s, f, to))
                spans = out
        for s, f, to in spans:
            rows.append(dict(tag=tag, serial=s, frm=f, to=to))
    return rows


def unit_on(rows, tag, d):
    for r in rows:
        if r["tag"] == tag and r["frm"] <= d and (r["to"] is None or d <= r["to"]):
            return r["serial"]
    raise KeyError((tag, d))


def schedule(T):
    """Asset tags at each event: one analyser to every 70 adults, at most three, a tag at one event a day."""
    rng = T["R"]["analysers"]
    by_date = {}
    for e in T["E"]:
        by_date.setdefault(e["date"], []).append(e)
    use = {}
    for d in sorted(by_date):
        free = list(K.ASSETS)
        rng.shuffle(free)
        for e in by_date[d]:
            k = 1 if e["n"] <= 70 else (2 if e["n"] <= 160 else 3)
            use[e["eid"]] = sorted(free[:k])
            free = free[k:]
    return use


def runs(T, use, rows):
    """Every run the units logged: two controls per analyser at the start of each event day, one patient run per
    encounter, an error and its repeat where the run failed, and the pre-season training day."""
    rng = T["R"]["analysers"]
    enc_by_ev = {}
    for x in T["enc"]:
        enc_by_ev.setdefault(x["event"]["eid"], []).append(x)
    out = []

    def err():
        return ERRORS[int(rng.choice(len(ERRORS), p=ERR_W))][0]

    def session(serial, t0, samples, lot):
        t = t0
        for lvl in ("CONTROL L1", "CONTROL L2"):
            while True:
                t += dt.timedelta(seconds=int(rng.integers(300, 420)))
                if rng.random() < 0.012:
                    out.append(dict(serial=serial, time=t, type=lvl, sample="QC-%s" % lvl[-2:], result="",
                                    error=err(), lot=lot))
                    continue
                out.append(dict(serial=serial, time=t, type=lvl, sample="QC-%s" % lvl[-2:],
                                result="%.1f" % (5.4 if lvl.endswith("1") else 9.6 + rng.choice([-.1, 0, 0, .1])),
                                error="", lot=lot))
                break
        for sid, when, val in samples:
            t = max(t + dt.timedelta(seconds=int(rng.integers(30, 120))), when)
            vals = [val]
            if val >= REPEAT_AT:     # a result in the diabetes range is repeated on a fresh cartridge before it is given
                vals.append(round(val + float(rng.choice([-0.1, 0.0, 0.0, 0.1])), 1))
            for k, v in enumerate(vals):
                if k:
                    t += dt.timedelta(seconds=int(rng.integers(240, 400)))
                while rng.random() < 0.034:
                    out.append(dict(serial=serial, time=t, type="PATIENT", sample=sid, result="", error=err(), lot=lot))
                    t += dt.timedelta(seconds=int(rng.integers(200, 420)))
                out.append(dict(serial=serial, time=t, type="PATIENT", sample=sid, result="%.1f" % v, error="",
                                lot=lot))

    lots = ["GQ%d%03d" % (2026, k) for k in range(101, 140)]
    for e in T["E"]:
        tags = use[e["eid"]]
        xs = sorted(enc_by_ev.get(e["eid"], []), key=lambda x: x["time"])
        lot = lots[min(len(lots) - 1, (e["date"] - K.SEASON_START).days // 7)]
        for j, tag in enumerate(tags):
            mine = [(x["enc"], x["time"] + dt.timedelta(seconds=int(rng.integers(60, 240))), x["a1c"])
                    for k, x in enumerate(xs) if k % len(tags) == j]
            t0 = dt.datetime.combine(e["date"], dt.time(e["start_h"])) - dt.timedelta(minutes=35)
            session(unit_on(rows, tag, e["date"]), t0, mine, lot)
    # the training day before the season: four analysers, staff samples
    for j, tag in enumerate(["A01", "A02", "A03", "A06"]):
        t0 = dt.datetime.combine(K.TRAINING_DAY, dt.time(9, 30))
        staff = [("E26-%06d" % (990001 + j * 10 + k), t0 + dt.timedelta(minutes=40 + 9 * k),
                  round(float(rng.normal(5.4, 0.3)), 1)) for k in range(int(rng.integers(6, 10)))]
        session(unit_on(rows, tag, K.TRAINING_DAY), t0, staff, "GQ2025187")
    out.sort(key=lambda r: (r["time"], r["serial"]))
    return out


def utc_offset(t):
    """Hours between local (Eastern) time and UTC on the 2026 calendar."""
    return 4 if dt.datetime(2026, 3, 8, 2) <= t < dt.datetime(2026, 11, 1, 2) else 5


def downloads(runlog, rows):
    """The run database as Biomedical Engineering exported it: every download loaded in turn, each run stamped in the
    docking software's time, a row skipped when its serial and run time are already held. Returns the exported rows
    and, for the record, how many runs were loaded twice."""
    mem = {}
    for r in runlog:
        mem.setdefault(r["serial"], []).append(r)
    held, out, copies = set(), [], {}
    for d, serial in DOWNLOADS:
        if serial is None:
            units = sorted({a["serial"] for a in rows if a["frm"] <= d and (a["to"] is None or d <= a["to"])})
        else:
            units = [serial]
        end = dt.datetime.combine(d, dt.time(23, 0))
        for u in units:
            start = dt.datetime.combine(CLEARED[u], dt.time(12)) if u in CLEARED and CLEARED[u] < d else None
            runs = [r for r in mem.get(u, []) if r["time"] < end and (start is None or r["time"] >= start)]
            for r in runs[-MEMORY:]:
                t = r["time"] if d < UPGRADE else r["time"] + dt.timedelta(hours=utc_offset(r["time"]))
                if (u, t) in held:
                    continue
                held.add((u, t))
                copies.setdefault(id(r), []).append(t)
                out.append(dict(r, stamp=t))
    for r in runlog:
        assert id(r) in copies, ("a run no download reached", r["serial"], r["time"])
    twice = sum(len(v) > 1 for v in copies.values())
    out.sort(key=lambda r: (r["stamp"], r["serial"]))
    return out, twice


def cartridges(runlog, rows, window=True):
    """The golden of Ask A: cartridges each asset tag used in the season (every run but one stopped at the
    cartridge check), each run on the tag whose unit it was that day."""
    out = {t: 0 for t in K.ASSETS}
    for r in runlog:
        d = r["time"].date()
        if window and not (K.SEASON_START <= d <= K.SEASON_END):
            continue
        if r["error"] and r["error"] not in SPENT:
            continue
        tag = [a["tag"] for a in rows if a["serial"] == r["serial"] and a["frm"] <= d and (a["to"] is None or d <= a["to"])]
        assert len(tag) == 1, (r["serial"], d)
        out[tag[0]] += 1
    return out


# ---------------------------------------------------------------------------------------------- billing
def billing(T):
    """The laboratory's invoice lines: each OGTT on the invoice after the month it was done (a share a month late),
    the health system's clinic tests billed to the program's account among them, a share of lines resubmitted
    under a new line on a later invoice (most credited a month or two after), and tests credited in full when the
    specimen was lost or rejected after billing."""
    rng = T["R"]["billing"]
    tests = []
    for t in T["tests"]:
        tests.append(dict(acc=t["acc"], date=t["date"], prog=True))
    # clinic OGTTs billed to the program's account
    days = [d for d in sorted({t["date"] for t in T["tests"]}) if d <= dt.date(2026, 12, 31)]
    n_clinic = int(round(0.017 * len(tests)))
    used = {t["acc"] for t in tests}
    for k in range(n_clinic):
        d = days[int(rng.integers(0, len(days)))]
        while True:
            acc = "TL%08d" % (40213500 + int(rng.integers(0, 3 * len(tests) + 300)))
            if acc not in used:
                used.add(acc)
                break
        tests.append(dict(acc=acc, date=d, prog=False))
    tests.sort(key=lambda t: (t["date"], t["acc"]))

    def invoice_of(d, late=0):
        y, m = d.year, d.month + 1 + late
        while m > 12:
            y, m = y + 1, m - 12
        return dt.date(y, m, 6)
    def memo_date(d, k):
        """Credit memos go out with the statement on the 6th or mid-cycle on the 20th."""
        return dt.date(d.year, d.month, 20) if k == 0 else invoice_of(d, 0)
    lines = []
    for t in tests:
        late = 1 if rng.random() < 0.045 else 0
        inv = invoice_of(t["date"], late)
        t["inv"] = inv
        bill = dict(inv=inv, acc=t["acc"], service=t["date"], amount=K.OGTT_PRICE, kind="bill")
        lines.append(bill)
        u = rng.random()
        if u < 0.024:      # resubmitted under a new line, on the same invoice or the next
            inv2 = inv if rng.random() < .4 else invoice_of(inv, 0)
            dup = dict(inv=inv2, acc=t["acc"], service=t["date"], amount=K.OGTT_PRICE, kind="dup")
            lines.append(dup)
            if rng.random() < 0.72:
                lines.append(dict(inv=memo_date(inv2, int(rng.integers(0, 2))), acc=t["acc"], service=t["date"],
                                  amount=-K.OGTT_PRICE, kind="credit_dup", ref=dup))
        elif u < 0.0295:   # specimen lost or rejected after billing: credited in full
            lines.append(dict(inv=memo_date(inv, int(rng.integers(0, 2))), acc=t["acc"], service=t["date"],
                              amount=-K.OGTT_PRICE, kind="credit_full", ref=bill))
    lines = [l for l in lines if l["inv"] <= EXPORT_AS_OF]
    # the charges, numbered on each month's invoice
    charges = [l for l in lines if l["amount"] > 0]
    by_inv = {}
    for l in charges:
        by_inv.setdefault(l["inv"], []).append(l)
    out = []
    for inv in sorted(by_inv):
        ls = sorted(by_inv[inv], key=lambda l: (l["service"], l["acc"]))
        for k, l in enumerate(ls):
            l.update(number="TL-%d%02d-CSP" % (inv.year, inv.month), date=inv, doc="Invoice", line=k + 1)
            out.append(l)
    # the credits, issued as credit memos of one to four lines, one reason to a memo
    credits = [l for l in lines if l["amount"] < 0]
    for l in credits:
        l["applies"] = l["ref"]
        assert "number" in l["ref"], "a credit on a line the export does not hold"
    seq = 4180
    for d in sorted({l["inv"] for l in credits}):
        for kind in ("credit_dup", "credit_full"):
            ls = sorted([l for l in credits if l["inv"] == d and l["kind"] == kind],
                        key=lambda l: (l["service"], l["acc"]))
            order = rng.permutation(len(ls))
            ls = [ls[int(k)] for k in order]
            while ls:
                n = min(len(ls), 1 + int(rng.choice(4, p=[.35, .30, .20, .15])))
                seq += int(rng.integers(3, 41))
                memo, ls = ls[:n], ls[n:]
                memo.sort(key=lambda l: l["applies"]["line"] + 100000 * (l["applies"]["inv"].month + 12 *
                                                                            l["applies"]["inv"].year))
                for k, l in enumerate(memo):
                    l.update(number="CM-%02d-%05d" % (d.year % 100, seq), date=d, doc="Credit memo", line=k + 1)
                    out.append(l)
    out.sort(key=lambda l: (l["date"], l["doc"] != "Invoice", l["number"], l["line"]))
    return out, tests


def billed_months(lines, program_accs):
    """The golden of Ask B, in cents: for each month of the season by the month each test was done, what the
    laboratory billed net of its credits (each credit reversing the one line it applies to), and the part for the
    program's own tests of screened adults."""
    out = {m: [0, 0] for m in K.MONTHS}
    price = int(round(K.OGTT_PRICE * 100))
    for l in lines:
        d = l["service"]
        if d.year != 2026 or d.month not in out:
            continue
        v = price if l["doc"] == "Invoice" else -price
        out[d.month][0] += v
        if l["acc"] in program_accs:
            out[d.month][1] += v
    return out
