"""The general ledger: postings, the vouchers they post under, and the monitoring platform's verdicts.

A posting is one source document's entry into the ledger. The interface that carries it decides how many
postings share a voucher: the purchase ledger and the migrated delivery rounds post at the document, so a
voucher is one posting, while branch EPOS, payroll and the unmigrated rounds consolidate, so a voucher can
be thousands. The monitoring platform writes one verdict per voucher.

Per-unit exception rates are tuned here, by bisection on a fixed random stream, so that each unit's
recovered figure lands on its target, which is a bin centre. The tuning is deterministic given SEED.
"""
import datetime as dt
import zlib

import numpy as np

import world as W
from estimate import recover_unit

SEED = 184_008

# postings a period by unit kind, and the share of those postings on each stream.
# The streams whose voucher holds one posting are what identify the rate; the consolidating streams
# carry the mass the platform's verdict hides.
KIND = {
    "branch": dict(postings=(10_200, 15_400), streams={
        "EPOS": 0.655, "ROUTE_DOCKET": 0.120, "ROUTE_VAN": 0.100,
        "AP_INVOICE": 0.100, "AP_BATCH": 0.015, "PAYROLL": 0.000, "MANUAL": 0.010}),
    "contracts": dict(postings=(8_800, 11_200), streams={
        "EPOS": 0.000, "ROUTE_DOCKET": 0.300, "ROUTE_VAN": 0.120,
        "AP_INVOICE": 0.100, "AP_BATCH": 0.020, "PAYROLL": 0.440, "MANUAL": 0.020}),
    "bakery": dict(postings=(6_400, 8_600), streams={
        "EPOS": 0.280, "ROUTE_DOCKET": 0.180, "ROUTE_VAN": 0.090,
        "AP_INVOICE": 0.130, "AP_BATCH": 0.020, "PAYROLL": 0.280, "MANUAL": 0.020}),
    "services": dict(postings=(2_100, 3_300), streams={
        "EPOS": 0.000, "ROUTE_DOCKET": 0.000, "ROUTE_VAN": 0.000,
        "AP_INVOICE": 0.200, "AP_BATCH": 0.040, "PAYROLL": 0.700, "MANUAL": 0.060}),
}
# postings on one voucher, by stream. EPOS splits at the branch-to-till change.
VOUCHER = {
    "EPOS_BRANCH_DAY": (900, 3_200),
    "EPOS_TILL_DAY":   (150, 560),
    "ROUTE_DOCKET":    (1, 1),
    "ROUTE_VAN":       (24, 72),
    "AP_INVOICE":      (1, 1),
    "AP_BATCH":        (12, 130),
    "PAYROLL":         (820, 2_400),
    "MANUAL":          (1, 1),
}
STREAM_INTERFACE = {"EPOS": "EPOS", "ROUTE_DOCKET": "ROUTE", "ROUTE_VAN": "ROUTE",
                    "AP_INVOICE": "AP", "AP_BATCH": "AP", "PAYROLL": "PAYROLL", "MANUAL": "MANUAL"}

# Each unit's recovered figure, which is a bin centre on the nearest hundred. The rate is solved to hit it.
# Distinct multiples of the bin, assigned so that every unit's implied per-posting rate sits in a narrow
# band (0.9 to 1.8 per cent). The band matters: the map from the rate to the voucher-level indicator is
# concave, so a wide spread of rates across units is what drives a pooled estimate away from the per-unit
# one, and the group total is graded.
TARGET = {
    "DPG-110": 1_700, "DPG-120": 2_100, "DPG-130": 1_500, "DPG-210": 1_300,
    "DPG-220": 1_100, "DPG-310": 1_200, "DPG-320": 1_400, "DPG-410": 1_000,
    "DPG-420": 1_600, "DPG-510": 900, "DPG-610": 800, "DPG-900": 400,
}
UBIN, GBIN = 100, 1_000

RULES = (
    # rule_id, title, live_from, withdrawn_in, share of trips
    ("CM-01", "Posting to a control account by a user outside finance",   "FY24", None,   0.17),
    ("CM-02", "Credit to a cost account with no matching debit",          "FY24", None,   0.14),
    ("CM-03", "Posting dated outside the period it was entered in",       "FY24", None,   0.13),
    ("CM-04", "Round-sum posting at or above the authorisation limit",    "FY24", None,   0.12),
    ("CM-05", "Posting entered and released by the same user",            "FY24", None,   0.11),
    ("CM-07", "Supplier bank detail changed within ten days of payment",  "FY25", None,   0.10),
    ("CM-08", "Posting to a dormant account",                             "FY25", None,   0.09),
    ("CM-09", "Weekend or holiday posting by a branch user",              "FY25", None,   0.08),
    ("CM-11", "Posting reversed and re-entered inside forty-eight hours", "FY26", None,   0.06),
    ("CM-06", "Manual journal above the delegated limit",                 "FY24", "FY25", 0.00),
    ("CM-10", "Posting to a closed cost centre",                          "FY25", "FY26", 0.00),
)
LIVE_FY26 = tuple(r[0] for r in RULES if r[3] is None)
WITHDRAWN = tuple(r[0] for r in RULES if r[3] is not None)


def _voucher_key(stream, day):
    if stream != "EPOS":
        return stream
    return "EPOS_BRANCH_DAY" if day < W.RENUMBER_DATE else "EPOS_TILL_DAY"


def _sizes(rng, stream, postings, day):
    lo, hi = VOUCHER[_voucher_key(stream, day)]
    if lo == hi == 1:
        return [1] * postings
    out = []
    left = postings
    while left > 0:
        out.append(min(int(rng.integers(lo, hi + 1)), left))
        left -= out[-1]
    return out


def skeleton(fy_periods, n_periods, tag):
    """Every unit's entries for a financial year: unit, period, date, stream, postings on the voucher."""
    rng = np.random.default_rng(SEED + zlib.crc32(tag.encode()))
    rows = []
    for code, _old, _name, kind, _county in W.UNITS:
        spec = KIND[kind]
        lo, hi = spec["postings"]
        for pno, pstart, pend in fy_periods[:n_periods]:
            total = int(rng.integers(lo, hi + 1))
            days = [pstart + dt.timedelta(days=d) for d in range((pend - pstart).days + 1)]
            trading = [d for d in days if d.weekday() < 6]
            for stream, share in spec["streams"].items():
                n = int(round(total * share))
                if n <= 0:
                    continue
                if stream == "PAYROLL":                      # one run a period
                    for k in _sizes(rng, stream, n, trading[-1]):
                        rows.append((code, pno, trading[-1], stream, k))
                    continue
                per_day = max(n // len(trading), 1)
                left = n
                for d in trading:
                    if left <= 0:
                        break
                    take = min(per_day, left)
                    left -= take
                    for k in _sizes(rng, stream, take, d):
                        rows.append((code, pno, d, stream, k))
    return rows


def _stream(code):
    return np.random.default_rng(SEED + 7919 + zlib.crc32(code.encode()))


def trips(k, u, r):
    """Postings on each entry that trip the ruleset, on the fixed stream u."""
    ends = np.cumsum(k)
    return np.add.reduceat((u < r).astype(np.int64), ends - k) if len(k) else np.array([], np.int64)


def tune(rows, verbose=False):
    """Per unit, solve the per-posting rate so the recovered figure lands on TARGET."""
    out = {}
    for code, _old, _name, _kind, _county in W.UNITS:
        k = np.array([r[4] for r in rows if r[0] == code], dtype=np.int64)
        T = int(k.sum())
        u = _stream(code).random(T)
        lo, hi = 1e-4, 0.08
        for _ in range(42):
            r = (lo + hi) / 2
            f = (trips(k, u, r) > 0).astype(np.int64)
            if recover_unit(k, f) * T < TARGET[code]:
                lo = r
            else:
                hi = r
        r = (lo + hi) / 2
        out[code] = r
        if verbose:
            f = (trips(k, u, r) > 0).astype(np.int64)
            got = recover_unit(k, f) * T
            print("  %-8s postings %9s entries %8s rate %.5f recovered %8.1f target %5d off-centre %+.2f"
                  % (code, f"{T:,}", f"{len(k):,}", r, got, TARGET[code],
                     (got - TARGET[code]) / (UBIN / 2.0)))
    return out


def unit_arrays(rows, code, rate):
    """(entry sizes, trips per entry, flagged per entry, the unit's uniform stream)."""
    k = np.array([r[4] for r in rows if r[0] == code], dtype=np.int64)
    u = _stream(code).random(int(k.sum()))
    per = trips(k, u, rate)
    return k, per, (per > 0).astype(np.int64)


LINES_PER_POSTING = (2, 7)
# FY25 is not graded: it carries the comparative ledger the three asks work on.
FY25_RATE = 0.0135


def materialise():
    """Everything the pack is written from, built once and deterministically.

    Returns a dict with, per financial year, the entry table as parallel arrays, the postings that tripped
    the ruleset per entry, and the rules that fired on each flagged entry.
    """
    out = {}
    for tag, fy_periods, n_periods in (("FY26", W.FY26_PERIODS, W.GRADED_PERIODS),
                                       ("FY25", W.FY25_PERIODS, 12)):
        rows = skeleton(fy_periods, n_periods, tag)
        rates = tune(rows) if tag == "FY26" else {u[0]: FY25_RATE for u in W.UNITS}
        by_unit = {}
        for code, _o, _n, _k, _c in W.UNITS:
            k, per, f = unit_arrays(rows, code, rates[code])
            by_unit[code] = dict(k=k, trips=per, flag=f, rate=rates[code])
        out[tag] = dict(rows=rows, rates=rates, by_unit=by_unit, periods=fy_periods[:n_periods])
    return out


def entry_table(sim, tag):
    """One row per journal entry, in posting order, with the fields the extract carries."""
    rng = np.random.default_rng(SEED + 101 + zlib.crc32(tag.encode()))
    rows = sim[tag]["rows"]
    by_unit = sim[tag]["by_unit"]
    seen = {c: 0 for c in by_unit}
    users = {}
    out = []
    for code, pno, day, stream, k in rows:
        i = seen[code]
        seen[code] += 1
        d = by_unit[code]
        lpp = int(rng.integers(*LINES_PER_POSTING, endpoint=True))
        amt = round(float(k) * float(rng.uniform(18.0, 240.0)), 2)
        if code not in users:
            users[code] = ["%s%02d" % (code[-3:], j) for j in range(1, 9)]
        who = users[code][int(rng.integers(0, 8))]
        rel = who if stream == "MANUAL" and rng.random() < 0.18 else users[code][int(rng.integers(0, 8))]
        out.append(dict(unit_now=code, unit_code=W.unit_code_at(code, day), period=pno, day=day,
                        stream=stream, interface=STREAM_INTERFACE[stream], items=int(k),
                        lines=int(k) * lpp, amount=amt, entered_by=who, released_by=rel,
                        trips=int(d["trips"][i]), flag=int(d["flag"][i])))
    out.sort(key=lambda r: (r["day"], r["unit_now"], r["stream"]))
    for n, r in enumerate(out, start=1):
        r["entry_no"] = n
        r["voucher_ref"] = "%s%s-%06d" % (r["interface"][:2].upper(), tag[-2:], n)
    return out


def register_rows(table, tag):
    """One row per flagged entry, with every rule that fired on it. Unique on the entry."""
    rng = np.random.default_rng(SEED + 211 + zlib.crc32(tag.encode()))
    live = [r for r in RULES if r[3] is None] if tag == "FY26" else [r for r in RULES if r[0] != "CM-11"]
    pool = [r[0] for r in live if r[4] > 0]
    share = np.array([r[4] for r in live if r[4] > 0], dtype=float)
    share = share / share.sum()
    out = []
    for r in table:
        if not r["flag"]:
            continue
        n = max(int(r["trips"]), 1)
        fired = sorted(set(rng.choice(pool, size=n, p=share)))
        out.append(dict(entry_no=r["entry_no"], voucher_ref=r["voucher_ref"],
                        unit_code=r["unit_code"], day=r["day"], period=r["period"],
                        rules=";".join(fired), n_rules=len(fired)))
    for n, r in enumerate(out, start=1):
        r["exception_id"] = "CMX-%s-%05d" % (tag[-2:], n)
    return out
