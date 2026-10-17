"""task193: the independent verifier. Reads only target/ and generator/figures.json, on its own
code path, and recomputes the screen, every rung and every ask figure.
"""
import bisect
import collections
import csv
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN
import datetime as dt
import json
import os
import statistics

WIN_A, WIN_B = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
CLEAR_B = dt.date(2025, 9, 30)
MULTIPLE = 1.25
MINIMUM = 25
MERGER = dt.date(2026, 4, 1)
AMEND = dt.date(2026, 4, 1)
TRANSFER = dt.date(2026, 2, 27)
QUARTERS = [("2025 Q4", dt.date(2025, 10, 1), dt.date(2025, 12, 31)),
            ("2026 Q1", dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
            ("2026 Q2", dt.date(2026, 4, 1), dt.date(2026, 6, 30)),
            ("2026 Q3", dt.date(2026, 7, 1), dt.date(2026, 9, 30))]
BANDS = [(0, 34, "18-34"), (35, 44, "35-44"), (45, 64, "45-64"), (65, 200, "65 and over")]
N = 0


def tab(tgt, name):
    with open(os.path.join(tgt, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def d_iso(s):
    return dt.date(int(s[0:4]), int(s[5:7]), int(s[8:10]))


def d_dk(s):
    return dt.date(int(s[6:10]), int(s[3:5]), int(s[0:2]))


def chain_at(tgt):
    """pharmacy -> a function of the day giving the chain that owned it then."""
    reg = {}
    for r in tab(tgt, "pharmacy_register.csv"):
        reg[r["pharmacy_id"]] = (r["chain_code"], r["previous_chain_code"],
                                 d_iso(r["in_chain_from"]) if r["in_chain_from"] else None)

    def at(ph, day):
        now, prev, since = reg[ph]
        return prev if (prev and since and day < since) else now
    return at


def _fee_bands(tgt):
    """The statutory rates as the shipped workbook states them: the Schedule sheet for doses
    dispensed before the amendment, the Amendment sheet for doses dispensed on or after it."""
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(tgt, "data_fee_schedule.xlsx"))
    out = []
    for name in ("Schedule", "Amendment 2026-04-01"):
        ws = wb[name]
        rows = []
        for row in ws.iter_rows(values_only=True):
            cells = [c for c in row if c is not None]
            if len(cells) == 4 and str(cells[0]).isdigit():
                lo = float(cells[1])
                hi = 10 ** 9 if str(cells[2]).strip() == "-" else float(cells[2])
                rows.append((lo, hi, int(cells[3])))
        assert rows, name
        out.append(sorted(rows))
    return out[0], out[1]


def run(tgt, figures_path):
    global N
    N = 0
    fail = []

    def ck(label, cond, detail=""):
        global N
        N += 1
        if not cond:
            fail.append("%s %s" % (label, detail))

    fg = json.load(open(figures_path))

    pkg = {}
    ddd = {}
    for r in tab(tgt, "package_index.csv"):
        pkg[r["vnr"]] = (r["atc_code"],
                         d_iso(r["valid_from"]) if r["valid_from"] else None,
                         d_iso(r["valid_to"]) if r["valid_to"] else None)
        ddd[r["vnr"]] = int(Decimal(r["ddd_per_pack"]) * 10) if r["ddd_per_pack"] else 0
    annex = tab(tgt, "screen_annexes.csv")
    prod = {r["product_atc"]: r["product_code"] for r in annex}
    mark = {r["marker_atc_group"]: r["marker_code"] for r in annex}
    pairs = sorted(set((r["product_code"], r["marker_code"]) for r in annex))
    xw = {r["retired_person_key"]: r["current_person_key"]
          for r in tab(tgt, "person_key_crosswalk.csv")}
    chain_of = {r["pharmacy_id"]: r["chain_code"] for r in tab(tgt, "pharmacy_register.csv")}
    preg = {r["product_code"]: r for r in tab(tgt, "product_register.csv")}
    holder_of = {k: r["holder_code"] for k, r in preg.items()}
    prev_of = {k: (r["previous_holder_code"],
                   d_iso(r["holder_code_from"]) if r["holder_code_from"] else None)
               for k, r in preg.items()}
    merged = {r["holder_code"]: r["merged_into"] for r in tab(tgt, "holder_register.csv")
              if r["merged_into"]}

    seen = set()
    lines = []
    for name, kc, vc, dc, sc, phc, pc_, parse in (
            ("dispensings_2023_2025.csv", "pseudonym", "vnr", "disp_date", "submitted",
             "pharmacy_id", "packages", d_iso),
            ("dispensings_2025_2026.csv", "person_key", "package_code", "date_of_dispensing",
             "submission_date", "pharmacy", "n_packages", d_dk)):
        for r in tab(tgt, name):
            d = parse(r[dc])
            vnr = r[vc]
            atc, vf, vt = pkg[vnr]
            if (vf and d < vf) or (vt and d > vt):
                continue
            code = prod.get(atc) or mark.get(atc)
            key = xw.get(r[kc], r[kc])
            lines.append({"key": key, "code": code, "day": d, "vnr": vnr,
                          "sub": parse(r[sc]), "ph": r[phc], "packs": int(r[pc_]),
                          "atc": atc})
            if code is not None:
                seen.add((key, code, d, vnr, r[phc]))
    # a line re-sent after a transmission failure is one dispensing (register_release_notes.json)
    dedup, seen_line = [], set()
    for r in lines:
        k = (r["key"], r["vnr"], r["day"], r["ph"])
        if k in seen_line:
            continue
        seen_line.add(k)
        dedup.append(r)
    lines = dedup

    first = {}
    for k, code, d, vnr, ph in seen:
        if code is None:
            continue
        kk = (k, code)
        if kk not in first or d < first[kk]:
            first[kk] = d

    byp = collections.defaultdict(dict)
    for (k, code), d in first.items():
        byp[k][code] = d

    def window_days(code):
        return sorted((d - WIN_A).days for (k, c), d in first.items()
                      if c == code and WIN_A <= d <= WIN_B)

    results = {}
    for pcode, mcode in pairs:
        t, s = [], []
        for k, got in byp.items():
            tp, tm = got.get(pcode), got.get(mcode)
            if tp is None or tm is None:
                continue
            if not (WIN_A <= tp <= WIN_B and WIN_A <= tm <= WIN_B) or tp == tm:
                continue
            t.append((tp - WIN_A).days)
            s.append((tm - WIN_A).days)
        after = sum(1 for i in range(len(t)) if s[i] > t[i])
        results[(pcode, mcode)] = (len(t), after, sorted(t), sorted(s))

    def expected(pcode, mcode, route):
        n, after, t, s = results[(pcode, mcode)]
        if n == 0:
            return 0.0
        if route == "half":
            return 0.5 * n
        if route == "perm":
            return sum(len(s) - bisect.bisect_right(s, x) for x in t) / float(n)
        if route == "incidence":
            tt, ss = window_days(pcode), window_days(mcode)
            return n * sum(len(ss) - bisect.bisect_right(ss, x) for x in tt) / float(len(tt) * len(ss))
        if route == "pairprod":
            ss = window_days(mcode)
            return n * sum(len(ss) - bisect.bisect_right(ss, x) for x in t) / float(len(t) * len(ss))
        if route == "even":
            span = (WIN_B - WIN_A).days + 1
            return n * sum((span - 1 - x) / float(span) for x in t) / float(len(t))
        raise ValueError(route)

    open_pairs = set((r["product_code"], r["marker_code"]) for r in tab(tgt, "signal_tracker_export.csv")
                     if r["status"].startswith("under assessment"))

    def referred(route):
        out = []
        for p in pairs:
            n, after, t, s = results[p]
            if n < MINIMUM:
                continue
            e = expected(p[0], p[1], route)
            if e > 0 and after / e >= MULTIPLE and p not in open_pairs:
                out.append("%s/%s" % p)
        return sorted(out)

    ans = referred("perm")
    ck("v.referred_count", len(ans) == fg["referred_count"],
       "%d against %d" % (len(ans), fg["referred_count"]))
    ck("v.crude_count", len(referred("half")) == fg["crude_count"])
    for route in ("incidence", "pairprod", "even"):
        ck("v.route_" + route, referred(route) == ans, route)
    cands = [p for p in pairs if results[p][0] >= MINIMUM]
    ck("v.candidate_count", len(cands) == fg["candidate_count"])
    ck("v.screened_count", len(pairs) == fg["screened_count"])
    ck("v.patients", len(set(k for k, c in first)) == fg["patients_in_extract"],
       "%d" % len(set(k for k, c in first)))

    want = {}
    for r in fg["screen_rows"]:
        want[(r["product"], r["marker"])] = r
    for p in pairs:
        n, after, t, s = results[p]
        r = want[p]
        ck("v.row_n_%s" % str(p), r["patients"] == n, "%d against %d" % (n, r["patients"]))
        ck("v.row_after_%s" % str(p), r["after"] == after)
        ck("v.row_before_%s" % str(p), r["before"] == n - after)
        if n >= MINIMUM:
            e = expected(p[0], p[1], "perm")
            ck("v.row_exp_%s" % str(p), abs(round(e, 1) - r["expected"]) < 0.051,
               "%.3f against %s" % (e, r["expected"]))
            ck("v.row_mult_%s" % str(p), abs(round(after / e, 2) - r["multiple"]) < 0.011)
            ck("v.row_ref_%s" % str(p),
               (r["referred"] == "yes") == ("%s/%s" % p in ans))
        else:
            ck("v.row_below_%s" % str(p), r["referred"] == "below minimum")

    # ---- A1
    rej = tab(tgt, "submission_exceptions.csv")
    owner = chain_at(tgt)          # the chain that owned the pharmacy on the day of the dispensing
    a1 = {}
    for label, a, b in QUARTERS:
        for ch in sorted(set(chain_of.values())):
            acc = [r for r in lines if owner(r["ph"], r["day"]) == ch and a <= r["day"] <= b]
            rr = [r for r in rej
                  if owner(r["pharmacy"], d_iso(r["date_of_dispensing"])) == ch
                  and a <= d_iso(r["date_of_dispensing"]) <= b]
            days = sorted((r["sub"] - r["day"]).days for r in acc)
            a1[(ch, label)] = (len(acc), len(rr),
                               round(float(statistics.median(days)), 1) if days else 0.0)
    for r in fg["a1"]:
        got = a1[(r["chain"], r["quarter"])]
        ck("v.a1_acc_%s_%s" % (r["chain"], r["quarter"]), got[0] == r["accepted"],
           "%d against %d" % (got[0], r["accepted"]))
        ck("v.a1_rej_%s_%s" % (r["chain"], r["quarter"]), got[1] == r["rejected"],
           "%d against %d" % (got[1], r["rejected"]))
        ck("v.a1_med_%s_%s" % (r["chain"], r["quarter"]), abs(got[2] - r["median_days"]) < 0.051,
           "%.1f against %.1f" % (got[2], r["median_days"]))

    # ---- A2
    # the statutory rates, read from the shipped workbook rather than carried in this file
    BANDS_BEFORE, BANDS_AFTER = _fee_bands(tgt)
    tot = collections.Counter()
    before = collections.Counter()
    after_d = collections.Counter()
    for r in lines:
        code = prod.get(r["atc"])
        if code is None:
            continue
        prev, since = prev_of[code]
        h = holder_of[code] if (since is None or r["day"] >= since) else prev
        if h in merged and r["day"] >= MERGER:
            h = merged[h]
        if not (WIN_A <= r["day"] <= WIN_B):
            continue
        q = ddd[r["vnr"]] * r["packs"]
        tot[h] += q
        if r["day"] < AMEND:
            before[h] += q
        else:
            after_d[h] += q
    ck("v.a2_payers", len(fg["a2"]) == len([h for h in tot if tot[h] > 0]),
       "%d against %d" % (len(fg["a2"]), len([h for h in tot if tot[h] > 0])))
    for r in fg["a2"]:
        h = r["holder"]
        th = Decimal(tot[h]) / Decimal(10000)
        rb = next(x for lo, hi, x in BANDS_BEFORE if lo <= th < hi)
        ra = next(x for lo, hi, x in BANDS_AFTER if lo <= th < hi)
        exact = (Decimal(before[h]) * rb + Decimal(after_d[h]) * ra) / Decimal(10000)
        fee = exact.quantize(Decimal(1), rounding=ROUND_HALF_UP)
        ck("v.a2_ddd_" + h, Decimal(tot[h]) / 10 == Decimal(str(r["ddd"])),
           "%s against %s" % (Decimal(tot[h]) / 10, r["ddd"]))
        ck("v.a2_fee_" + h, int(fee) == r["fee_dkk"], "%d against %d" % (fee, r["fee_dkk"]))
        # the figure is not near a rounding boundary: half-up and half-even agree
        other = exact.quantize(Decimal(1), rounding=ROUND_HALF_EVEN)
        ck("v.a2_fee_mid_bin_" + h, int(other) == r["fee_dkk"] and r["fee_distance"] >= 0.02,
           "distance %.4f" % r["fee_distance"])
        ck("v.a2_ddd_exact_" + h, Decimal(tot[h]) % 1 == 0,
           "tenths are whole: %s" % tot[h])

    # ---- A3. The region recorded at the start of the screen window is what the person extract
    # delivered with the October 2025 run holds; the current extract's own history columns explain
    # some of the differences between the two and not all of them.
    prior = {r["person_key"]: (r["region"] or "not stated")
             for r in tab(tgt, "person_register_2025Q4.csv")}
    reg = {}
    for r in tab(tgt, "person_register.csv"):
        region = r["region"] or "not stated"
        if r["previous_region"] and r["region_recorded_from"] and d_iso(r["region_recorded_from"]) > WIN_A:
            region = r["previous_region"]
        reg[r["person_key"]] = (prior.get(r["person_key"], region), int(r["year_of_birth"]))
    pset = set(prod.values())
    mset = set(mark.values())
    cells = collections.defaultdict(lambda: [0, 0])
    for k, got in byp.items():
        if not any(c in pset and WIN_A <= d <= WIN_B for c, d in got.items()):
            continue
        if k not in reg:
            continue
        region, yob = reg[k]
        age = WIN_A.year - yob
        band = next(lab for lo, hi, lab in BANDS if lo <= age <= hi)
        cells[(region, band)][0] += 1
        if any(c in mset and WIN_A <= d <= WIN_B for c, d in got.items()):
            cells[(region, band)][1] += 1
    for r in fg["a3"]:
        n, k = cells[(r["region"], r["band"])]
        ck("v.a3_n_%s_%s" % (r["region"], r["band"]), n == r["patients"],
           "%d against %d" % (n, r["patients"]))
        share = round(100.0 * k / n, 1) if n else 0.0
        ck("v.a3_share_%s_%s" % (r["region"], r["band"]), abs(share - r["share_pct"]) < 0.051,
           "%.1f against %.1f" % (share, r["share_pct"]))

    if fail:
        raise AssertionError("verifier failed (%d of %d):\n  %s" % (len(fail), N, "\n  ".join(fail)))
    return N


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    print(run(os.path.join(os.path.dirname(here), "target"), os.path.join(here, "figures.json")))
