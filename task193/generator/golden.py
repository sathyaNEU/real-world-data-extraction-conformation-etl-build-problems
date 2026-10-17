"""task193: the screen, run from the shipped bundle alone.

load() conforms the two extracts; screen() runs the referral test under a named expectation route.
rung0() runs it the way a solver gets it with neither repair applied.
"""
import bisect
import collections
import csv
import datetime as dt
import os

D0 = dt.date(2023, 10, 1)
WIN_A, WIN_B = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
CLEAR_A, CLEAR_B = dt.date(2023, 10, 1), dt.date(2025, 9, 30)
MULTIPLE = 1.25
MIN_PATIENTS = 25


def rd(tgt, name):
    with open(os.path.join(tgt, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def iso(s):
    return dt.date(int(s[0:4]), int(s[5:7]), int(s[8:10]))


def dk(s):
    return dt.date(int(s[6:10]), int(s[3:5]), int(s[0:2]))


def load(tgt, fold_keys=True, packages="at_date", drop_resend=True):
    """One conformed dispensing table: person key, treatment code, date."""
    pkg = {}
    for r in rd(tgt, "package_index.csv"):
        pkg.setdefault(r["vnr"], []).append(
            (r["atc_code"], iso(r["valid_from"]) if r["valid_from"] else None,
             iso(r["valid_to"]) if r["valid_to"] else None))
    annex = rd(tgt, "screen_annexes.csv")
    prod_by_atc, mark_by_atc = {}, {}
    pairs = []
    for r in annex:
        prod_by_atc[r["product_atc"]] = r["product_code"]
        mark_by_atc[r["marker_atc_group"]] = r["marker_code"]
        pairs.append((r["product_code"], r["marker_code"]))
    xw = {}
    if fold_keys:
        for r in rd(tgt, "person_key_crosswalk.csv"):
            xw[r["retired_person_key"]] = r["current_person_key"]

    def treat(vnr, d):
        cands = pkg.get(vnr)
        if not cands:
            return None
        for atc, vf, vt in cands:
            if packages == "at_date" and ((vf and d < vf) or (vt and d > vt)):
                continue
            if packages == "current_only" and vt is not None:
                continue      # the naive join keeps only the package rows still open
            if packages == "ignore_validity":
                pass          # the index joined without its date condition
            if atc in prod_by_atc:
                return prod_by_atc[atc]
            if atc in mark_by_atc:
                return mark_by_atc[atc]
            return None
        return None

    rows = []
    for name, keyc, vnrc, datec, parse in (
            ("dispensings_2023_2025.csv", "pseudonym", "vnr", "disp_date", iso),
            ("dispensings_2025_2026.csv", "person_key", "package_code", "date_of_dispensing", dk)):
        for r in rd(tgt, name):
            d = parse(r[datec])
            code = treat(r[vnrc], d)
            if code is None:
                continue
            key = r[keyc]
            if fold_keys:
                key = xw.get(key, key)
            rows.append((key, code, d, r[vnrc], r["pharmacy_id"] if "pharmacy_id" in r else r["pharmacy"]))
    if drop_resend:
        rows = sorted(set(rows))
    return rows, pairs


def first_receipts(rows):
    first = {}
    for key, code, d, vnr, ph in rows:
        k = (key, code)
        if k not in first or d < first[k]:
            first[k] = d
    return first


def pair_counts(first, pairs, edge=0):
    """Per pair: the patients, their product and marker first-receipt dates, and the after-count."""
    by_person = collections.defaultdict(dict)
    for (key, code), d in first.items():
        by_person[key][code] = d
    out = []
    for pc, mc in pairs:
        t, s = [], []
        for key, got in by_person.items():
            tp, tm = got.get(pc), got.get(mc)
            if tp is None or tm is None:
                continue
            if not (WIN_A <= tp <= WIN_B and WIN_A <= tm <= WIN_B):
                continue
            if tp == tm:
                continue
            if edge and not (WIN_A + dt.timedelta(days=edge) <= tp
                             <= WIN_B - dt.timedelta(days=edge)):
                continue
            t.append(tp)
            s.append(tm)
        after = sum(1 for i in range(len(t)) if s[i] > t[i])
        out.append({"product": pc, "marker": mc, "key": pc + "/" + mc, "n": len(t),
                    "after": after, "before": len(t) - after, "t": t, "s": s})
    return sorted(out, key=lambda r: r["key"])


def _window_days(first, code):
    return sorted((d - WIN_A).days for (k, c), d in first.items()
                  if c == code and WIN_A <= d <= WIN_B)


def expected(r, route, first=None):
    """The number of the pair's patients expected to have the marker after the product, if
    receiving the product had no bearing on when the marker treatment is first received."""
    n = r["n"]
    if n == 0:
        return 0.0
    if route == "half":
        return 0.5 * n
    t = sorted((d - WIN_A).days for d in r["t"])
    if route == "perm":
        s = sorted((d - WIN_A).days for d in r["s"])
        tot = 0
        for x in t:
            tot += len(s) - bisect.bisect_right(s, x)
        return float(tot) / n
    if route == "incidence":
        tt = _window_days(first, r["product"])
        ss = _window_days(first, r["marker"])
        tot = 0
        for x in tt:
            tot += len(ss) - bisect.bisect_right(ss, x)
        return n * float(tot) / (len(tt) * len(ss))
    if route == "pairprod":
        ss = _window_days(first, r["marker"])
        tot = 0
        for x in t:
            tot += len(ss) - bisect.bisect_right(ss, x)
        return n * float(tot) / (len(t) * len(ss))
    if route == "even":
        span = (WIN_B - WIN_A).days + 1
        return n * sum((span - 1 - x) / float(span) for x in t) / len(t)
    raise ValueError(route)


def open_pairs(tgt):
    out = set()
    for r in rd(tgt, "signal_tracker_export.csv"):
        if r["status"].startswith("under assessment"):
            out.add((r["product_code"], r["marker_code"]))
    return out


def screen(tgt, rows_pairs, route, first=None, multiple=MULTIPLE, minimum=MIN_PATIENTS, edge=0):
    rows, pairs = rows_pairs
    if first is None:
        first = first_receipts(rows)
    counts = pair_counts(first, pairs, edge=edge)
    opened = open_pairs(tgt)
    out = []
    for r in counts:
        if r["n"] < minimum:
            r["candidate"] = False
            continue
        r["candidate"] = True
        e = expected(r, route, first)
        r["expected"] = e
        r["ratio"] = r["after"] / e if e > 0 else 0.0
        r["blocked"] = (r["product"], r["marker"]) in opened
        r["referred"] = r["ratio"] >= multiple and not r["blocked"]
        if r["referred"]:
            out.append(r["key"])
    return sorted(out), counts


def rung0(tgt):
    """The run a solver gets with the keys unfolded, the package validity ignored and the
    re-sent batch left in."""
    rp = load(tgt, fold_keys=False, packages="current_only", drop_resend=False)
    return screen(tgt, rp, "half")
