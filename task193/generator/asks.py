"""task193: the ask layer's own files, and the ask goldens computed from them."""
import collections
import csv
import os
import statistics
from decimal import Decimal, ROUND_HALF_UP

import numpy as np

import world as W
from pack import write_csv

QUARTERS = [("2025 Q4", 731, 822), ("2026 Q1", 823, 912), ("2026 Q2", 913, 1003),
            ("2026 Q3", 1004, 1095)]
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def month_key(d):
    dd = W.day(d)
    return "%04d-%02d" % (dd.year, dd.month)


def quarter_of(d):
    for label, a, b in QUARTERS:
        if a <= d <= b:
            return label
    return None


# ---------------------------------------------------------------- A1 files
def write_exceptions(tgt, rejected):
    rows = []
    # the register numbers an exception when it writes it, so the references run in the order the
    # lines were submitted, not the order they were dispensed in
    for i, r in enumerate(sorted(rejected, key=lambda r: (r["submitted"], r["line"]))):
        rows.append(["EX-2026-%05d" % (1041 + i), r["key"], r["vnr"], W.iso(r["day"]),
                     r["pharmacy"], W.iso(r["submitted"]), r["reason"]])
    rows.sort(key=lambda x: (x[3], x[0]))
    return write_csv(os.path.join(tgt, "submission_exceptions.csv"),
                     ["exception_ref", "person_key", "vnr", "date_of_dispensing", "pharmacy",
                      "submitted_on", "rejection_reason"], rows)


def write_submission_log(tgt, kept, rejected):
    """The chains' own monthly totals, counted by month of submission, not of dispensing.

    It is the chains' count and not the register's, so it does not reconcile to the extract line
    for line: it counts the lines a chain withdrew before the register wrote them, and a batch
    transmitted after a month's cut-off is counted by the chain in the month it sent it and by
    the register in the next one.
    """
    rng = np.random.default_rng(W.SEED + 71)
    acc = collections.Counter()
    rej = collections.Counter()
    for r in kept:
        acc[(r["chain"], month_key(r["submitted"]))] += 1
    for r in rejected:
        rej[(r["chain"], month_key(r["submitted"]))] += 1
    rows = []
    for ci, (code, name) in enumerate(W.CHAINS):
        months = sorted(set(m for (c, m) in acc) | set(m for (c, m) in rej))
        months = sorted(set(m for (c, m) in list(acc) + list(rej) if c == ci))
        for m in months:
            a, t = acc[(ci, m)], rej[(ci, m)]
            cancelled = int(rng.poisson(0.0021 * max(a, 1) + 0.6))
            cutoff = int(rng.integers(-3, 4))      # lines the two sides place in adjacent months
            rows.append([code, m, a + t + cancelled + cutoff, a, t, cancelled])
    return write_csv(os.path.join(tgt, "pharmacy_submission_log.csv"),
                     ["chain_code", "submission_month", "lines_submitted", "lines_accepted",
                      "lines_turned_back", "lines_withdrawn_by_chain"], rows)


def distinct(kept):
    """One row per dispensing: a line re-sent after a transmission failure counts once."""
    seen, out = set(), []
    for r in sorted(kept, key=lambda r: (r["day"], r["line"])):
        k = (r["key"], r["vnr"], r["day"], r["pharmacy"])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def a1_golden(kept, rejected):
    """Per chain and quarter of dispensing: accepted lines, rejected lines, median days to submission."""
    kept = distinct(kept)
    out = []
    for ci, (code, name) in enumerate(W.CHAINS):
        for label, a, b in QUARTERS:
            acc = [r for r in kept if r["chain"] == ci and a <= r["day"] <= b]
            rej = [r for r in rejected if r["chain"] == ci and a <= r["day"] <= b]
            days = sorted(r["submitted"] - r["day"] for r in acc)
            med = statistics.median(days) if days else 0.0
            out.append({"chain": code, "quarter": label, "accepted": len(acc),
                        "rejected": len(rej), "median_days": round(float(med), 1)})
    return out


# ---------------------------------------------------------------- A2
def holder_at(code, d):
    """The marketing authorisation holder of the product on that date, as the register gives it."""
    succ = W.TRANSFERS.get(code)
    if succ and d >= succ[1]:
        return succ[0]
    return W.HOLDER_OF[code]


def fee_payer(holder_code, d):
    """The company that pays: the surviving company from the merger date, the merged one before it."""
    for code, name, cvr, merged in W.HOLDERS:
        if code == holder_code and merged and d >= W.MERGER_DAY:
            return merged
    return holder_code


def a2_golden(kept, ddd_of):
    """Per fee payer: DDD of Annex A products dispensed in the window, and the fee due.

    Every screened product's package holds a whole number of tenths of a defined daily dose, so
    the arithmetic runs in tenths as integers and the figures carry no floating-point residue.
    """
    kept = distinct(kept)
    before = collections.Counter()
    after = collections.Counter()
    for r in kept:
        if r["day"] < W.WIN_A or r["day"] > W.WIN_B:
            continue
        code, kind = W.PKG_OF[r["vnr"]][0], W.PKG_OF[r["vnr"]][1]
        if kind != "product":
            continue
        payer = fee_payer(holder_at(code, r["day"]), r["day"])
        deci = ddd_of[r["vnr"]]                    # tenths of a defined daily dose, an integer
        assert deci == int(deci), (r["vnr"], deci)
        q = int(deci) * r["packs"]
        if r["day"] < W.FEE_AMENDMENT_DAY:
            before[payer] += q
        else:
            after[payer] += q
    out = []
    for code, name, cvr, merged in W.HOLDERS:
        tb, ta = before[code], after[code]         # tenths
        total = tb + ta
        if total <= 0:
            continue
        thousands = Decimal(total) / Decimal(10000)
        rate_before = next(rt for lo, hi, rt in W.FEE_BANDS if lo <= thousands < hi)
        rate_after = next(rt for lo, hi, rt in W.FEE_BANDS_AMENDED if lo <= thousands < hi)
        exact = (Decimal(tb) * rate_before + Decimal(ta) * rate_after) / Decimal(10000)
        fee = exact.quantize(Decimal(1), rounding=ROUND_HALF_UP)
        out.append({"holder": code, "name": name,
                    "ddd": float(Decimal(total) / 10), "ddd_before": float(Decimal(tb) / 10),
                    "ddd_after": float(Decimal(ta) / 10), "rate_before": rate_before,
                    "rate_after": rate_after, "fee_dkk": int(fee),
                    "fee_exact": str(exact),
                    "fee_distance": float(abs(exact - exact.to_integral_value(
                        rounding=ROUND_HALF_UP)))})
    return out


# ---------------------------------------------------------------- A3
def a3_golden(tgt, firsts, pairs):
    """Per region and age band at the start of the screen window: patients with a first receipt of
    an Annex A product inside the window, and the share of them who also had a first receipt of an
    Annex B marker treatment inside it. Read from the shipped bundle, per standard section 4.2."""
    import csv as _csv
    import golden as G
    # the region recorded for the patient at the start of the screen window, which is what the
    # person extract delivered with the October 2025 run holds
    prior = {}
    with open(os.path.join(tgt, "person_register_2025Q4.csv"), newline="",
              encoding="utf-8") as fh:
        for r in _csv.DictReader(fh):
            prior[r["person_key"]] = r["region"] or "not stated"
    reg = {}
    with open(os.path.join(tgt, "person_register.csv"), newline="", encoding="utf-8") as fh:
        for r in _csv.DictReader(fh):
            region = r["region"] or "not stated"
            if r["previous_region"] and r["region_recorded_from"] \
                    and G.iso(r["region_recorded_from"]) > G.WIN_A:
                region = r["previous_region"]
            reg[r["person_key"]] = (prior.get(r["person_key"], region),
                                    int(r["year_of_birth"]))
    pset = set(p for p, m in pairs)
    mset = set(m for p, m in pairs)
    byp = collections.defaultdict(dict)
    for (k, code), d in firsts.items():
        byp[k][code] = d
    cells = collections.defaultdict(lambda: [0, 0])
    for k, got in byp.items():
        tp = [d for c, d in got.items() if c in pset and G.WIN_A <= d <= G.WIN_B]
        if not tp or k not in reg:
            continue
        region, yob = reg[k]
        age = G.WIN_A.year - yob
        band = next(lab for lo, hi, lab in W.AGE_BANDS if lo <= age <= hi)
        cells[(region, band)][0] += 1
        if any(c in mset and G.WIN_A <= d <= G.WIN_B for c, d in got.items()):
            cells[(region, band)][1] += 1
    out = []
    for region in W.REGIONS + ["not stated"]:
        for lo, hi, band in W.AGE_BANDS:
            n, k = cells[(region, band)]
            out.append({"region": region, "band": band, "patients": n,
                        "share_pct": round(100.0 * k / n, 1) if n else 0.0, "with_marker": k})
    return out
