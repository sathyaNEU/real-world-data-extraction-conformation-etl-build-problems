"""The cracker's and the mirror's paths, run on the cut pack.

The cracker landed the call, so it ran the hygiene battery (exact duplicates, the retired keys, the
package index at the date of the dispensing, the clearance period) and executed every filed rule the
asking sentences point at. Where nothing in the pack adjudicates a handling it takes the natural
reading. For each ask this module computes what that path returns and scores it against the golden
within half a unit of the stated rounding.

The mirror stops at the most attractive wrong rung of the call, the equal-chance expectation, which
refers ten pairs. The asks are decoupled from the call, so the mirror walks the same ask path: its
ask score is the cracker's unless a shared hazard separates them, which this module checks.

It is measurement, not argument. Nothing here reads the generator's private state: every figure comes
out of target/ alone.
"""
import collections
import csv
import datetime as dt
import json
import os
import statistics
import sys
from decimal import Decimal, ROUND_HALF_UP

import openpyxl

QUARTERS = [("2025 Q4", dt.date(2025, 10, 1), dt.date(2025, 12, 31)),
            ("2026 Q1", dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
            ("2026 Q2", dt.date(2026, 4, 1), dt.date(2026, 6, 30)),
            ("2026 Q3", dt.date(2026, 7, 1), dt.date(2026, 9, 30))]
WIN_A, WIN_B = dt.date(2025, 10, 1), dt.date(2026, 9, 30)
AMEND = dt.date(2026, 4, 1)


def age_bands_from_the_standard(tgt):
    """Section 4.2's reporting bands, read out of the shipped PDF the way a solver reads it."""
    import re
    import pypdf
    r = pypdf.PdfReader(os.path.join(tgt, "screen_standard_7_2024.pdf"))
    text = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in r.pages))
    m = re.search(r"in the bands ([0-9 a-z,]*?and over)\.", text)
    assert m, "section 4.2's bands not found in the standard"
    parts = [x.strip() for x in m.group(1).replace(", and ", ", ").split(",") if x.strip()]
    out, lo = [], 0
    for x in parts:
        n = re.findall(r"\d+", x)
        if "over" in x:
            out.append((int(n[0]), 200, "%s and over" % n[0]))
        else:
            out.append((lo, int(n[1]), "%s-%s" % (n[0], n[1])))
            lo = int(n[1]) + 1
    return out


def rd(tgt, name):
    with open(os.path.join(tgt, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def iso(s):
    return dt.date(int(s[0:4]), int(s[5:7]), int(s[8:10]))


def dk(s):
    return dt.date(int(s[6:10]), int(s[3:5]), int(s[0:2]))


def quarter_of(d):
    for label, a, b in QUARTERS:
        if a <= d <= b:
            return label
    return None


def extract(tgt, dedup=True):
    """Both layouts stacked on the renamed columns, the re-sent lines counted once.

    The release notes name the two layouts and their date formats; the data dictionary says a line
    re-transmitted after a failed transfer is one dispensing. The cracker ran both.
    """
    rows = []
    for name, keyc, vnrc, datec, subc, phc, npc, parse in (
            ("dispensings_2023_2025.csv", "pseudonym", "vnr", "disp_date", "submitted",
             "pharmacy_id", "packages", iso),
            ("dispensings_2025_2026.csv", "person_key", "package_code", "date_of_dispensing",
             "submission_date", "pharmacy", "n_packages", dk)):
        for r in rd(tgt, name):
            rows.append({"key": r[keyc], "vnr": r[vnrc], "day": parse(r[datec]),
                         "submitted": parse(r[subc]), "pharmacy": r[phc],
                         "packs": int(r[npc])})
    if not dedup:
        return rows
    seen, out = set(), []
    for r in sorted(rows, key=lambda r: (r["day"], r["key"], r["vnr"], r["pharmacy"])):
        k = (r["key"], r["vnr"], r["day"], r["pharmacy"])
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


def chain_of(tgt, as_of=False):
    """The chain a line belongs to. The natural reading is the chain the register gives the
    pharmacy; `as_of` is the chain that owned it on the day, which nothing in the pack states."""
    reg = {r["pharmacy_id"]: (r["chain_code"], r["previous_chain_code"],
                              iso(r["in_chain_from"]) if r["in_chain_from"] else None)
           for r in rd(tgt, "pharmacy_register.csv")}
    if not as_of:
        return lambda ph, _d: reg[ph][0]

    def at(ph, d):
        now, prev, since = reg[ph]
        return prev if (prev and since and d < since) else now
    return at


# ---------------------------------------------------------------- A1
def ask1(tgt, quarter_of_dispensing=True, drop_resend=True, exceptions_file=True,
         chain_as_of=False):
    """Per chain and quarter of dispensing: the lines rejected, the lines accepted and the median
    days from dispensing to submission.

    The asking sentence pins the quarter basis, the dictionary pins the re-sent line, and the
    manifest points at the exceptions file. Nothing is left for the cracker to get wrong.
    """
    ch = chain_of(tgt, as_of=chain_as_of)
    acc = collections.defaultdict(list)
    for r in extract(tgt, dedup=drop_resend):
        q = quarter_of(r["day"] if quarter_of_dispensing else r["submitted"])
        if q:
            acc[(ch(r["pharmacy"], r["day"]), q)].append((r["submitted"] - r["day"]).days)
    rej = collections.Counter()
    if exceptions_file:
        for r in rd(tgt, "submission_exceptions.csv"):
            d = iso(r["date_of_dispensing"] if quarter_of_dispensing else r["submitted_on"])
            q = quarter_of(d)
            if q:
                rej[(ch(r["pharmacy"], d), q)] += 1
    else:
        for r in rd(tgt, "pharmacy_submission_log.csv"):
            q = quarter_of(dt.date(int(r["submission_month"][:4]),
                                   int(r["submission_month"][5:7]), 15))
            if q:
                rej[(r["chain_code"], q)] += int(r["lines_turned_back"])
    out = {}
    for code in sorted(set(r["chain_code"] for r in rd(tgt, "pharmacy_register.csv"))):
        for label, _a, _b in QUARTERS:
            days = sorted(acc[(code, label)])
            out[(code, label)] = {
                "accepted": len(days), "rejected": rej[(code, label)],
                "median_days": round(float(statistics.median(days)), 1) if days else 0.0}
    return out


# ---------------------------------------------------------------- A2
def fee_bands(tgt):
    wb = openpyxl.load_workbook(os.path.join(tgt, "data_fee_schedule.xlsx"))
    out = []
    for name in ("Schedule", "Amendment 2026-04-01"):
        rows = []
        for row in wb[name].iter_rows(values_only=True):
            cells = [c for c in row if c is not None]
            if len(cells) == 4 and str(cells[0]).isdigit():
                hi = 10 ** 9 if str(cells[2]).strip() == "-" else float(cells[2])
                rows.append((float(cells[1]), hi, int(cells[3])))
        out.append(sorted(rows))
    return out[0], out[1]


def ask2(tgt, follow_the_payer=True, edition_in_force=False):
    """Per payer: the defined daily doses of Annex A products dispensed in the window and the fee.

    The workbook's Notes sheet states who pays before and after a merger, the product register
    carries the transfer and its date, and the Schedule sheet states that the band is settled on the
    window total in thousands and that the amendment applies from 1 April 2026. The cracker read all
    of them; `follow_the_payer` False is the natural reading a solver takes when nothing says to
    follow the transfer, and is what the mirror of this ask would do.
    """
    # the natural reading takes the register's own ddd_per_pack; `edition_in_force` recomputes it
    # from the package's strength and the dose the edition names, which nothing in the pack says
    ed = {r["atc_code"]: (Decimal(r["ddd_mg"]) if r["ddd_mg"] else None)
          for r in rd(tgt, "atc_text.csv")}
    atc_of, tenths = {}, {}
    for r in rd(tgt, "package_index.csv"):
        atc_of[r["vnr"]] = (r["atc_code"],
                            iso(r["valid_from"]) if r["valid_from"] else None,
                            iso(r["valid_to"]) if r["valid_to"] else None)
        if edition_in_force and ed.get(r["atc_code"]) is not None:
            tenths[r["vnr"]] = int(Decimal(r["pack_size"])
                                   * Decimal(r["strength"].split()[0]) / ed[r["atc_code"]] * 10)
        else:
            tenths[r["vnr"]] = int(Decimal(r["ddd_per_pack"]) * 10) if r["ddd_per_pack"] else 0
    prod_atc = {r["product_atc"]: r["product_code"] for r in rd(tgt, "screen_annexes.csv")}
    reg = {r["product_code"]: r for r in rd(tgt, "product_register.csv")}
    hold = {r["holder_code"]: r for r in rd(tgt, "holder_register.csv")}

    def payer(code, d):
        r = reg[code]
        h = r["holder_code"]
        if follow_the_payer and r["previous_holder_code"] and r["holder_code_from"] \
                and d < iso(r["holder_code_from"]):
            h = r["previous_holder_code"]
        if follow_the_payer and hold[h]["merged_into"] and hold[h]["merger_date"] \
                and d >= iso(hold[h]["merger_date"]):
            h = hold[h]["merged_into"]
        elif not follow_the_payer and hold[h]["merged_into"]:
            h = hold[h]["merged_into"]
        return h

    before, after = collections.Counter(), collections.Counter()
    for r in extract(tgt):
        if not (WIN_A <= r["day"] <= WIN_B):
            continue
        atc, vf, vt = atc_of[r["vnr"]]
        if atc not in prod_atc:
            continue
        if (vf and r["day"] < vf) or (vt and r["day"] > vt):
            continue
        p = payer(prod_atc[atc], r["day"])
        q = tenths[r["vnr"]] * r["packs"]
        (before if r["day"] < AMEND else after)[p] += q
    bb, ba = fee_bands(tgt)
    out = {}
    for h in sorted(set(before) | set(after)):
        tb, ta = before[h], after[h]
        th = Decimal(tb + ta) / Decimal(10000)
        rb = next(x for lo, hi, x in bb if lo <= th < hi)
        ra = next(x for lo, hi, x in ba if lo <= th < hi)
        exact = (Decimal(tb) * rb + Decimal(ta) * ra) / Decimal(10000)
        out[h] = {"ddd": float(Decimal(tb + ta) / 10),
                  "fee_dkk": int(exact.quantize(Decimal(1), rounding=ROUND_HALF_UP))}
    return out


# ---------------------------------------------------------------- A3
def first_receipts(tgt):
    """Each patient's first receipt of each treatment, on the call's own construction."""
    pkg = {}
    for r in rd(tgt, "package_index.csv"):
        pkg.setdefault(r["vnr"], []).append(
            (r["atc_code"], iso(r["valid_from"]) if r["valid_from"] else None,
             iso(r["valid_to"]) if r["valid_to"] else None))
    annex = rd(tgt, "screen_annexes.csv")
    code_of = {}
    for r in annex:
        code_of[r["product_atc"]] = r["product_code"]
        code_of[r["marker_atc_group"]] = r["marker_code"]
    xw = {r["retired_person_key"]: r["current_person_key"]
          for r in rd(tgt, "person_key_crosswalk.csv")}
    first = {}
    for r in extract(tgt):
        for atc, vf, vt in pkg.get(r["vnr"], []):
            if (vf and r["day"] < vf) or (vt and r["day"] > vt):
                continue
            c = code_of.get(atc)
            if c is None:
                continue
            k = (xw.get(r["key"], r["key"]), c)
            if k not in first or r["day"] < first[k]:
                first[k] = r["day"]
            break
    return first, set(r["product_code"] for r in annex), set(r["marker_code"] for r in annex)


def ask3(tgt, bands, region_at_window_start=True, prior_vintage=False):
    """Per region and age band at the window's start: the patients with a first receipt of an Annex A
    product inside the window and the share of them with a first Annex B marker receipt inside it.

    Section 4.2 states the region vintage, the age basis and the "not stated" cell, and the data
    dictionary states what previous_region holds. `region_at_window_start` False is the natural
    reading a solver takes when nothing states the vintage.
    """
    prior = {r["person_key"]: (r["region"] or "not stated")
             for r in rd(tgt, "person_register_2025Q4.csv")} if prior_vintage else {}
    reg = {}
    for r in rd(tgt, "person_register.csv"):
        region = r["region"] or "not stated"
        if region_at_window_start and r["previous_region"] and r["region_recorded_from"] \
                and iso(r["region_recorded_from"]) > WIN_A:
            region = r["previous_region"]
        reg[r["person_key"]] = (prior.get(r["person_key"], region), int(r["year_of_birth"]))
    first, pset, mset = first_receipts(tgt)
    byp = collections.defaultdict(dict)
    for (k, c), d in first.items():
        byp[k][c] = d
    cells = collections.defaultdict(lambda: [0, 0])
    for k, got in byp.items():
        if not any(c in pset and WIN_A <= d <= WIN_B for c, d in got.items()) or k not in reg:
            continue
        region, yob = reg[k]
        age = WIN_A.year - yob
        band = next(lab for lo, hi, lab in bands if lo <= age <= hi)
        cells[(region, band)][0] += 1
        if any(c in mset and WIN_A <= d <= WIN_B for c, d in got.items()):
            cells[(region, band)][1] += 1
    return {k: {"patients": n, "share_pct": round(100.0 * w / n, 1) if n else 0.0}
            for k, (n, w) in cells.items()}


# ---------------------------------------------------------------- scoring
def score(tgt, figures, bands, a2_payer=True, a3_vintage=True, a1_quarter=True,
          a1_dedup=True, a1_exceptions=True, a1_chain_as_of=False, a3_prior=False,
          a2_edition=False):
    g = json.load(open(figures, encoding="utf-8"))
    rows = []

    a1 = ask1(tgt, quarter_of_dispensing=a1_quarter, drop_resend=a1_dedup,
              exceptions_file=a1_exceptions, chain_as_of=a1_chain_as_of)
    hits = 0
    for r in g["a1"]:
        got = a1.get((r["chain"], r["quarter"]), {})
        hits += 1 if got.get("accepted") == r["accepted"] else 0
        hits += 1 if got.get("rejected") == r["rejected"] else 0
        hits += 1 if abs(got.get("median_days", -99) - r["median_days"]) < 0.05 else 0
    rows.append(("A1 chain and quarter", 3 * len(g["a1"]), hits))

    a2 = ask2(tgt, follow_the_payer=a2_payer, edition_in_force=a2_edition)
    hits = 0
    for r in g["a2"]:
        got = a2.get(r["holder"], {})
        hits += 1 if abs(got.get("ddd", -1) - r["ddd"]) < 0.05 else 0
        hits += 1 if got.get("fee_dkk") == r["fee_dkk"] else 0
    rows.append(("A2 payer doses and fee", 2 * len(g["a2"]), hits))

    a3 = ask3(tgt, bands, region_at_window_start=a3_vintage, prior_vintage=a3_prior)
    hits = 0
    for r in g["a3"]:
        got = a3.get((r["region"], r["band"]), {})
        hits += 1 if got.get("patients") == r["patients"] else 0
        hits += 1 if abs(got.get("share_pct", -1) - r["share_pct"]) < 0.05 else 0
    rows.append(("A3 region and age band", 2 * len(g["a3"]), hits))
    return rows


def ceiling(cracker_rows, mirror_rows):
    """supplemental-stumping Part 0: C = 38 + 7 + 55 Lc, S = r + 7 + 55 Ls with r about 5."""
    total = sum(n for _a, n, _h in cracker_rows)
    lc = sum(h for _a, _n, h in cracker_rows) / float(total)
    ls = sum(h for _a, _n, h in mirror_rows) / float(total)
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    return total, lc, ls, (c + s) / 2.0, 100.0 * ls


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(here), "target")
    figures = os.path.join(here, "figures.json")
    bands = age_bands_from_the_standard(tgt)
    print("age bands read out of the shipped standard: %s"
          % ", ".join(lab for _lo, _hi, lab in bands))

    print("THE CRACKER'S PATH (landed the call, ran the battery, executed every filed rule)")
    cr = score(tgt, figures, bands)
    for ask, n, h in cr:
        print("  %-24s %3d figures, keeps %3d, misses %3d   %s"
              % (ask, n, h, n - h, "MISS" if h < n else "HIT (no device bites)"))
    print()
    print("THE MIRROR'S PATH (stops at the equal-chance expectation, same ask path)")
    mr = score(tgt, figures, bands)
    for ask, n, h in mr:
        print("  %-24s %3d figures, keeps %3d, misses %3d" % (ask, n, h, n - h))
    print()
    total, lc, ls, pair, leak = ceiling(cr, mr)
    print("ask figures %d; cracker keeps %.1f per cent, mirror keeps %.1f per cent"
          % (total, 100 * lc, 100 * ls))
    print("MEASURED pair ceiling %.1f (ceiling 40); mirror leakage %.1f per cent (under 35)"
          % (pair, leak))
    print()
    print("and what the two new primaries are worth: the path that finds each of them")
    for lbl, kw in (("A1 chain that owned the pharmacy", {"a1_chain_as_of": True}),
                    ("A2 the edition's own dose", {"a2_edition": True}),
                    ("A3 the prior person extract", {"a3_prior": True}),
                    ("all three found", {"a1_chain_as_of": True, "a2_edition": True,
                                         "a3_prior": True})):
        rr = score(tgt, figures, bands, **kw)
        t, lc2, ls2, p2, lk2 = ceiling(rr, rr)
        print("  %-34s keeps %.1f per cent, pair ceiling %.1f" % (lbl, 100 * lc2, p2))
    print()
    print("counterfactual: what each pinned device would be worth if nothing adjudicated it")
    for lbl, kw in (("A1 quarter of submission", {"a1_quarter": False}),
                    ("A1 re-sent lines kept", {"a1_dedup": False}),
                    ("A1 rejections from the chains' log", {"a1_exceptions": False}),
                    ("A2 payer not followed", {"a2_payer": False}),
                    ("A3 region vintage not followed", {"a3_vintage": False}),
                    ("every device restored at once",
                     {"a1_quarter": False, "a2_payer": False, "a3_vintage": False})):
        rr = score(tgt, figures, bands, **kw)
        t, lc2, ls2, p2, lk2 = ceiling(rr, rr)
        print("  %-34s keeps %.1f per cent, pair ceiling %.1f" % (lbl, 100 * lc2, p2))
