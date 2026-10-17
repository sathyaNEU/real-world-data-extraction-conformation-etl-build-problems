"""task193: the register extracts, the lookup tables and the operating files."""
import collections
import csv
from decimal import Decimal
import json
import os

import numpy as np

import world as W


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(head)
        wr.writerows(rows)
    return len(rows)


# ---------------------------------------------------------------- dispensing lines
# A pharmacy's authorisation can pass from one chain to another. The chain that owns it on the day
# of a dispensing is the chain that transmits that line, and the pharmacy register holds the chain
# that owns it at the extract date. Most of the transfers in the register are years old.
def pharmacy_moves(pharm_of):
    """pharmacy id -> (previous chain, new chain, the day the transfer took effect)."""
    rng = np.random.default_rng(W.SEED + 83)
    moves = {}
    # the four transactions inside the extract period: each chain sells a cluster of its pharmacies
    # to another, late in the window, so the lines dispensed before the transfer belong to the
    # chain that then owned them
    cycle = [(0, 2, 1047, 6), (2, 0, 1021, 8), (1, 3, 1063, 8), (3, 1, 1035, 10)]
    for a, b, day, k in cycle:
        pool = [p for p in pharm_of[a] if p not in moves]
        take = rng.choice(len(pool), size=min(k, len(pool)), replace=False)
        for j in take:
            moves[pool[int(j)]] = (a, b, day)
    # and the benign twins: transfers settled long before the extract opens
    for _ in range(11):
        a = int(rng.integers(0, len(W.CHAINS)))
        b = (a + 1 + int(rng.integers(0, len(W.CHAINS) - 1))) % len(W.CHAINS)
        pool = [p for p in pharm_of[a] if p not in moves]
        if not pool:
            continue
        moves[pool[int(rng.integers(0, len(pool)))]] = (
            a, b, -int(rng.integers(120, 1600)))
    return moves


def owner_at(moves, ph, day, fallback):
    mv = moves.get(ph)
    if mv is None:
        return fallback
    prev, new, d0 = mv
    return new if day >= d0 else prev


# the mean days a chain takes to transmit a line, by quarter of the window. The chains overlap and
# their order changes between quarters, as their own transfer schedules and backlogs do.
SUB_LAG = [[1.4, 1.9, 2.6, 2.2],
           [3.3, 2.8, 3.9, 4.5],
           [4.6, 5.4, 6.3, 5.7],
           [6.1, 7.2, 6.6, 8.0]]
# days a chain's own transfer schedule adds on top, by quarter. They overlap the chains and change
# their order between quarters, so no chain is simply faster than another all year.
SUB_EXTRA = [[2, 3, 1, 3],
             [0, 1, 0, 1],
             [0, -1, -1, 0],
             [1, 0, 1, 0]]
# how a pharmacy week falls: busiest on a Monday and a Friday, short hours on a Saturday, and
# only the duty pharmacies open on a Sunday
WEEK_SHAPE = [0.1845, 0.1705, 0.1655, 0.1680, 0.1965, 0.1065, 0.0085]


def transmit_day(d, lag, ci, q, rng):
    """The day a chain's batch reaches the register. A chain transmits on working days, so a lag
    that lands on a weekend carries to the Monday, and about one line in fifty is held back by a
    failed transfer or a re-key and arrives weeks late."""
    lag = max(0, lag + SUB_EXTRA[ci][q])
    if rng.random() < 0.019 and d < W.NDAY - 46:
        lag += 11 + int(rng.poisson(16))
    t = d + lag
    if W.day(t).weekday() >= 5:
        if W.day(t).weekday() == 5 and rng.random() < 0.14:
            pass                       # a Saturday transfer, which the smaller chains still run
        else:
            # a batch held over the weekend is swept before it or worked through after it
            back = 1 if W.day(t).weekday() == 5 else 2
            fwd = 2 if W.day(t).weekday() == 5 else 1
            u = rng.random()
            t = t - back if u < 0.38 else (t + fwd if u < 0.75 else t + fwd + 1)
    return min(max(t, d), W.PULL_DAY)


def open_day(d, rng):
    """A dispensing is taken on one of the days its own week is open."""
    monday = d - W.day(d).weekday()
    out = monday + int(rng.choice(7, p=WEEK_SHAPE))
    return int(min(max(out, 0), W.NDAY - 1))


def dispensings(first):
    """Every dispensing line in the clean truth, plus the patient attributes behind them."""
    rng = np.random.default_rng(W.SEED + 11)
    sub_rng = np.random.default_rng(W.SEED + 29)      # the chains' transmission, its own stream
    n = W.N_PAT
    chain_of = rng.choice(len(W.CHAINS), size=n, p=[0.37, 0.28, 0.21, 0.14])
    region_of = W.regions(n)
    outside = rng.random(n) < 0.023                     # registered outside Denmark at window start
    birth, _band = W.age_bands(n)
    sex = np.where(rng.random(n) < 0.508, "K", "M")
    pharm_of = {}
    for ci, (code, name) in enumerate(W.CHAINS):
        pharm_of[ci] = ["%s-%03d" % (code, 101 + j) for j in range(14 + 4 * ci)]
    moves = pharmacy_moves(pharm_of)
    lines = []
    lid = 0
    for code in W.PCODES + W.MCODES:
        t0 = first[code]
        who = np.nonzero(t0 >= 0)[0]
        reps = rng.poisson(0.72, size=len(who))
        for k, pid in enumerate(who):
            start = int(t0[pid])
            days = [start]
            d = start
            for _ in range(int(reps[k])):
                d = d + int(rng.integers(26, 124))
                if d > W.NDAY - 1:
                    break
                days.append(d)
            days = [open_day(int(x), rng) for x in days]
            mf, mt = W.MARKETED.get(code, (None, None))
            if mf is not None or mt is not None:
                days = [x for x in days
                        if (mf is None or x >= mf) and (mt is None or x <= mt)]
            pk = W.PACKAGES[code]
            pres = "L%05d" % (10000 + int(rng.integers(0, 7400)))
            for j, d in enumerate(days):
                valid = [p for p in pk
                         if (p[3] is None or d >= p[3]) and (p[4] is None or d <= p[4])]
                vnr = valid[int(rng.integers(0, len(valid)))][0]
                ci = int(chain_of[pid])
                ph = pharm_of[ci][int(rng.integers(0, len(pharm_of[ci])))]
                npk = int(rng.choice([1, 2, 3], p=[0.615, 0.265, 0.120]))
                q = 0 if d < 823 else (1 if d < 913 else (2 if d < 1004 else 3))
                mu = SUB_LAG[ci][q]
                lag = int(rng.poisson(mu))
                owner = owner_at(moves, ph, d, ci)
                lid += 1
                lines.append({"line": lid, "pid": int(pid), "code": code, "vnr": vnr, "day": d,
                              "pharmacy": ph, "chain": owner, "packs": npk,
                              "submitted": transmit_day(d, lag, owner, q, sub_rng),
                              "prescriber": pres,
                              "is_first": j == 0})
    # patients already on a medicine when the extract opens: their earliest line in the extract is
    # in its first weeks, so the register's volume is in steady state from the first month and none
    # of them can be a pair's patient (every first receipt falls in the clearance period).
    prev_rng = np.random.default_rng(W.SEED + 53)
    base = max(r["line"] for r in lines) + 1
    for code in W.PCODES + W.MCODES:
        mf0, mt0 = W.MARKETED.get(code, (None, None))
        if mf0 is not None and mf0 > 0:
            continue                      # not on the market when the extract opens
        pi = dict([(x[0], x[4]) for x in W.PRODUCTS] + [(m[0], m[4]) for m in W.MARKERS])[code]
        n_prev = int(round(0.235 * pi * n))
        who = prev_rng.choice(n, size=n_prev, replace=False)
        pk = W.PACKAGES[code]
        for pid in who:
            d = int(prev_rng.integers(-250, 0))
            reps = 1 + int(prev_rng.poisson(0.72))
            pres = "L%05d" % (10000 + int(prev_rng.integers(0, 7400)))
            for _ in range(reps):
                d += int(prev_rng.integers(26, 124))
                if d < 0 or d >= W.NDAY:
                    continue
                valid = [q for q in pk
                         if (q[3] is None or d >= q[3]) and (q[4] is None or d <= q[4])]
                if not valid:
                    break
                vnr = valid[int(prev_rng.integers(0, len(valid)))][0]
                ci = int(chain_of[pid])
                ph = pharm_of[ci][int(prev_rng.integers(0, len(pharm_of[ci])))]
                q2 = 0 if d < 823 else (1 if d < 913 else (2 if d < 1004 else 3))
                mu = SUB_LAG[ci][q2]
                dd = open_day(d, prev_rng)
                if (mt0 is not None and dd > mt0) or (mf0 is not None and dd < mf0):
                    continue
                owner = owner_at(moves, ph, dd, ci)
                base += 1
                lines.append({"line": base, "pid": int(pid), "code": code, "vnr": vnr, "day": dd,
                              "pharmacy": ph, "chain": owner, "packs": int(prev_rng.choice(
                                  [1, 2, 3], p=[0.615, 0.265, 0.120])),
                              "submitted": transmit_day(dd, int(prev_rng.poisson(mu)),
                                                        owner, q2, sub_rng), "prescriber": pres,
                              "is_first": False, "prevalent": True})
    for r in lines:
        r.setdefault("prevalent", False)
    lines.sort(key=lambda r: (r["day"], r["line"]))
    people = {"chain": chain_of, "region": region_of, "outside": outside, "birth": birth, "sex": sex}
    return lines, people


def apply_mess(lines, people):
    """The register's own mess: replaced pseudonyms, one re-sent batch, rejected lines."""
    rng = np.random.default_rng(W.MESS_SEED)
    n = W.N_PAT
    # (1) pseudonyms replaced after a civil-registration correction
    switched = np.sort(rng.choice(n, size=420, replace=False))
    switch_day = {int(p): int(d) for p, d in zip(switched, rng.integers(420, 1011, size=420))}
    pool = rng.choice(np.arange(3100000, 3100000 + 14 * n), size=n, replace=False)
    keys = {pid: "PK%07d" % int(pool[pid]) for pid in range(n)}
    pool2 = rng.choice(np.arange(8400000, 8400000 + 37 * max(len(switch_day), 1)),
                       size=len(switch_day), replace=False)
    new_keys = {pid: "PK%07d" % int(v) for pid, v in zip(sorted(switch_day), pool2)}
    for r in lines:
        pid = r["pid"]
        if pid in switch_day and r["day"] >= switch_day[pid]:
            r["key"] = new_keys[pid]
        else:
            r["key"] = keys[pid]
    # (2) the rejected lines: repeat dispensings the register turned back at validation,
    #     so no patient's first receipt of anything is touched
    # a line the register turns back must never be a patient's earliest observed receipt of a
    # treatment, or the ask layer's device would move the screen's own first receipts. The
    # generator's is_first flag is not enough on its own, because a prevalent user's earliest line
    # in the extract carries no flag, so the earliest line per patient and medicine is taken here.
    earliest = {}
    for i, r in enumerate(lines):
        k = (r["pid"], r["code"])
        if k not in earliest or (r["day"], r["line"]) < (lines[earliest[k]]["day"],
                                                         lines[earliest[k]]["line"]):
            earliest[k] = i
    protected = set(earliest.values())
    repeats = [i for i, r in enumerate(lines) if not r["is_first"] and i not in protected]
    # each chain validates to its own standard and each quarter has its own run of trouble; one
    # chain's spring release left a month of price records missing
    chain_rate = [0.021, 0.034, 0.047, 0.029]
    quarter_lift = {0: 1.00, 1: 1.18, 2: 0.86, 3: 0.93}
    pr = np.empty(len(repeats))
    for j, i in enumerate(repeats):
        r = lines[i]
        q = 0 if r["day"] < 823 else (1 if r["day"] < 913 else (2 if r["day"] < 1004 else 3))
        rate = chain_rate[r["chain"]] * quarter_lift[q]
        if r["chain"] == 2 and 913 <= r["day"] <= 943:
            rate *= 2.4
        pr[j] = rate
    rej_idx = set(int(i) for i, u, rate in zip(repeats, rng.random(len(repeats)), pr) if u < rate)
    # a handful of patients whose single dispensing was turned back: the register holds the
    # civil-registration record it was asked for and no dispensing for them in either extract.
    # Their one line falls in the clearance period, so no first receipt inside the screen window
    # moves and the screen cannot see them (checks.py asserts both).
    by_pid = collections.defaultdict(list)
    for i, r in enumerate(lines):
        by_pid[r["pid"]].append(i)
    wholly_clear = sorted(p for p, ix in by_pid.items()
                          if all(lines[i]["day"] <= W.CLEAR_B for i in ix))
    if wholly_clear:
        take = rng.choice(len(wholly_clear), size=min(34, len(wholly_clear)), replace=False)
        for j in take:
            rej_idx |= set(by_pid[wholly_clear[int(j)]])
    rejected, kept = [], []
    reasons = ["prescriber identifier not in the authorisation register",
               "package code not valid on the date of dispensing",
               "reimbursement code missing",
               "pharmacy identifier closed before the date of dispensing",
               "reimbursed price missing for the package on that date"]
    # the reason a line was turned back has to agree with what the registers hold: a line is
    # refused for a closed pharmacy only after that pharmacy's closing date, and for an invalid
    # package code only where the code has a validity period that the date of dispensing is
    # outside of
    closed = closed_pharmacies(set((r["chain"], r["pharmacy"]) for r in lines))
    dated = set(v for v, c, k, vf, vt in
                (p for lst in W.PACKAGES.values() for p in lst) if vf is not None or vt is not None)
    for i, r in enumerate(lines):
        if i in rej_idx:
            can = [0, 1, 2, 3, 4]
            if not (r["pharmacy"] in closed and r["day"] > closed[r["pharmacy"]]):
                can.remove(3)
            if r["vnr"] not in dated:
                can.remove(1)
            w = np.array([[0.407, 0.231, 0.168, 0.117, 0.077][j] for j in can], dtype=float)
            if r["chain"] == 2 and 913 <= r["day"] <= 943 and rng.random() < 0.74:
                r["reason"] = reasons[4]          # the month the chain's price records were missing
            else:
                r["reason"] = reasons[int(rng.choice(can, p=w / w.sum()))]
            rejected.append(r)
        else:
            kept.append(r)
    # (3) a chain's transfers re-sent under fresh line identifiers after a failed transmission.
    #     The large one is the October 2025 batch the register asked for again; a second, much
    #     smaller one follows in the spring, so the pattern is not a single unique burst.
    resent = [r for r in kept if r["chain"] == 0 and 731 <= r["day"] <= 764
              and rng.random() < 0.91]
    resent += [r for r in kept if r["chain"] == 3 and 952 <= r["day"] <= 958
               and rng.random() < 0.63]
    base = max(r["line"] for r in lines) + 1000
    extra = []
    for j, r in enumerate(resent):
        d = dict(r)
        d["line"] = base + j
        d["resend"] = True
        extra.append(d)
    for r in kept:
        r.setdefault("resend", False)
    kept = sorted(kept + extra, key=lambda r: (r["day"], r["line"]))
    return kept, rejected, switch_day, keys, new_keys


# ---------------------------------------------------------------- the two extracts
EXTRACT_SCOPE = ("Extract LSR-2026-0441 for the October 2026 prescription-sequence screen. It covers "
                 "the screen window of 1 October 2025 to 30 September 2026 and the clearance period "
                 "of 1 October 2023 to 30 September 2025, for patients aged 18 and over on "
                 "1 October 2025, and holds every dispensing of a product in Annex A of Standard "
                 "7-2024 or of a package in one of its Annex B groups.")

OLD_HEAD = ["line_id", "pseudonym", "vnr", "disp_date", "pharmacy_id", "packages",
            "prescriber_id", "submitted"]
NEW_HEAD = ["record_id", "person_key", "package_code", "date_of_dispensing", "pharmacy",
            "n_packages", "prescriber", "submission_date"]


def write_extracts(tgt, kept):
    old, new = [], []
    for r in kept:
        if r["day"] <= W.CLEAR_B:
            old.append(["DL%08d" % r["line"], r["key"], r["vnr"], W.iso(r["day"]), r["pharmacy"],
                        r["packs"], r["prescriber"], W.iso(r["submitted"])])
        else:
            new.append(["%08d" % r["line"], r["key"], r["vnr"], W.dk(r["day"]), r["pharmacy"],
                        r["packs"], r["prescriber"], W.dk(r["submitted"])])
    a = write_csv(os.path.join(tgt, "dispensings_2023_2025.csv"), OLD_HEAD, old)
    b = write_csv(os.path.join(tgt, "dispensings_2025_2026.csv"), NEW_HEAD, new)
    return a, b


# the strengths each preparation is marketed in, in the order MARKER_NAMES lists the generics
STRENGTH_MG = {
    "P01": [25, 50, 100], "P02": [60, 90, 120], "P03": [5, 10, 20],
    "P04": [150, 300, 150], "P05": [25, 50, 75], "P06": [250, 500, 750],
    "P07": [1, 2, 4], "P08": [10, 15, 20], "P09": [50, 100, 200],
    "M1": [4, 8, 10, 10], "M2": [20, 40, 20, 40], "M3": [100, 300, 80, 120],
    "M4": [20, 40, 1, 2], "M5": [50, 100, 10, 20], "M6": [3.75, 7.5, 5, 10],
    "M7": [0.1, 0.05, 0.1, 0.064], "M8": [5, 10, 25, 100],
}
MARKER_NAMES = {
    "M1": ["Ondansetron", "Ondansetron", "Metoclopramid", "Metoclopramid"],
    "M2": ["Pantoprazol", "Pantoprazol", "Esomeprazol", "Esomeprazol"],
    "M3": ["Allopurinol", "Allopurinol", "Febuxostat", "Febuxostat"],
    "M4": ["Furosemid", "Furosemid", "Bumetanid", "Bumetanid"],
    "M5": ["Sertralin", "Sertralin", "Citalopram", "Citalopram"],
    "M6": ["Zopiclon", "Zopiclon", "Zolpidem", "Zolpidem"],
    "M7": ["Betamethason", "Betamethason", "Mometason", "Mometason"],
    "M8": ["Olanzapin", "Olanzapin", "Quetiapin", "Quetiapin"],
}
STRENGTH = {"P01": ["25 mg", "50 mg", "100 mg"], "P02": ["60 mg", "90 mg", "120 mg"],
            "P03": ["5 mg", "10 mg", "20 mg"], "P04": ["150 mg/ml", "300 mg/ml", "150 mg/ml"],
            "P05": ["25 mg", "50 mg", "75 mg"], "P06": ["250 mg", "500 mg", "750 mg"],
            "P07": ["1 mg", "2 mg", "4 mg"], "P08": ["10 mg", "15 mg", "20 mg"],
            "P09": ["100 mcg", "200 mcg", "400 mcg"]}
MARK_STRENGTH = {"M1": ["4 mg", "8 mg", "10 mg", "80 mg"], "M2": ["20 mg", "40 mg", "15 mg", "30 mg"],
                 "M3": ["100 mg", "300 mg", "80 mg", "120 mg"], "M4": ["20 mg", "40 mg", "1 mg", "2 mg"],
                 "M5": ["50 mg", "100 mg", "10 mg", "20 mg"], "M6": ["3.75 mg", "7.5 mg", "5 mg", "10 mg"],
                 "M7": ["0.1 %", "0.05 %", "0.1 %", "0.064 %"], "M8": ["5 mg", "10 mg", "25 mg", "50 mg"]}


def _plain(d):
    """A decimal as the package index prints it: no exponent and no trailing zero."""
    t = format(d, "f")
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t or "0"


def write_package_index(tgt):
    rows = []
    for code in W.PCODES + W.MCODES:
        sizes = W.PACK_SIZES[code]
        ddd_mg = W.DDD_MG[code]
        for i, (vnr, c, kind, vf, vt) in enumerate(W.PACKAGES[code]):
            if kind == "product":
                name, atc = W.PNAME[code], W.PATC[code]
            else:
                name, atc = MARKER_NAMES[code][i % 4], W.MATC[code]
            mg = STRENGTH_MG[code][i % len(STRENGTH_MG[code])]
            size = sizes[i % len(sizes)]
            unit = "%g mg" % mg if atc != "D07AC" else "%g %%" % mg
            if ddd_mg is None:
                ddd = ""
            else:
                exact = (Decimal(str(size)) * Decimal(str(mg)) / Decimal(str(ddd_mg)))
                if kind == "product":
                    # a screened product's package is a whole number of tenths of a daily dose
                    assert (exact * 10) % 1 == 0, (code, mg, size, exact)
                    ddd = _plain(exact.quantize(Decimal("0.1")))
                else:
                    ddd = _plain(exact.quantize(Decimal("0.01")))
            rows.append([vnr, atc, name, unit, size, ddd,
                         W.iso(vf) if vf is not None else "", W.iso(vt) if vt is not None else ""])
    rows.sort(key=lambda r: r[0])
    return write_csv(os.path.join(tgt, "package_index.csv"),
                     ["vnr", "atc_code", "preparation", "strength", "pack_size", "ddd_per_pack",
                      "valid_from", "valid_to"], rows)


def write_product_register(tgt):
    rows = []
    for code, brand, atc, prof, pi, mf, mt, holder in W.PRODUCTS:
        succ = W.TRANSFERS.get(code)
        cur = succ[0] if succ else holder
        prev = holder if succ else ""
        since = W.iso(succ[1]) if succ else ""
        note = ("authorisation transferred from %s to %s with effect from %s"
                % (holder, succ[0], W.iso(succ[1]))) if succ else ""
        rows.append([code, brand, atc, cur, prev, since,
                     W.iso(mf) if mf is not None else "2019-04-15",
                     W.iso(mt) if mt is not None else "", note])
    return write_csv(os.path.join(tgt, "product_register.csv"),
                     ["product_code", "brand_name", "atc_code", "holder_code",
                      "previous_holder_code", "holder_code_from", "first_marketed",
                      "authorisation_valid_to", "note"], rows)


def write_atc_text(tgt):
    text = {"A10BX09": "Other blood glucose lowering drugs", "M01AH07": "Coxibs",
            "C10AX18": "Other lipid modifying agents", "L04AC22": "Interleukin inhibitors",
            "N02AX09": "Other opioids", "J01DH08": "Carbapenems", "G03AA18": "Progestogens and estrogens",
            "B01AF05": "Direct factor Xa inhibitors", "R03DX13": "Other systemic drugs for obstructive airway diseases",
            "A04AD": "Other antiemetics", "A02BC": "Proton pump inhibitors",
            "M04AA": "Preparations inhibiting uric acid production", "C03CA": "Sulfonamides, plain",
            "N06AB": "Selective serotonin reuptake inhibitors", "N05CF": "Benzodiazepine related drugs",
            "D07AC": "Corticosteroids, potent (group III)", "N05AH": "Diazepines, oxazepines and thiazepines"}
    ddd = {}
    for code in W.PCODES:
        ddd[W.PATC[code]] = W.DDD_MG_2026[code]
    for code in W.MCODES:
        ddd[W.MATC[code]] = W.DDD_MG_2026[code]
    rows = sorted([k, v, "ATC 2026 edition",
                   "" if ddd.get(k) is None else _plain(Decimal(str(ddd[k])))]
                  for k, v in text.items())
    return write_csv(os.path.join(tgt, "atc_text.csv"),
                     ["atc_code", "atc_text", "edition", "ddd_mg"], rows)


def write_crosswalk(tgt, switch_day, keys, new_keys):
    reasons = ["civil registration number corrected", "duplicate registration resolved",
               "pseudonymisation key regenerated after a data correction"]
    rows = []
    for i, pid in enumerate(sorted(switch_day)):
        rows.append([keys[pid], new_keys[pid], W.iso(switch_day[pid]), reasons[i % 3]])
    rows.sort(key=lambda r: r[2])
    return write_csv(os.path.join(tgt, "person_key_crosswalk.csv"),
                     ["retired_person_key", "current_person_key", "replaced_on", "reason"], rows)


def write_person_register(tgt, people, keys, new_keys, switch_day, kept, rejected=()):
    """One row per current person key the register holds a civil-registration record for among
    the patients in this extract. A patient whose only lines were turned back at validation has a
    record here and no dispensing in either extract."""
    rng = np.random.default_rng(W.SEED + 29)
    seen = set(r["pid"] for r in kept) | set(r["pid"] for r in rejected)
    rows = []
    moved = set(rng.choice(sorted(seen), size=int(0.021 * len(seen)), replace=False).tolist())
    # Municipalities also correct a registration without the register recording when: the current
    # extract holds the corrected region and nothing beside it, and the extract delivered with the
    # October 2025 run holds what was recorded then.
    rest = sorted(set(seen) - moved)
    silent = set(rng.choice(rest, size=int(0.082 * len(rest)), replace=False).tolist())
    died = set(rng.choice(sorted(seen), size=int(0.016 * len(seen)), replace=False).tolist())
    gone = set(rng.choice(sorted(seen), size=int(0.007 * len(seen)), replace=False).tolist())
    last = {}
    for r in kept:
        last[r["pid"]] = max(last.get(r["pid"], -1), r["day"])
    at_window_start = {}
    for pid in sorted(seen):
        key = new_keys.get(pid, keys[pid])
        reg = "" if people["outside"][pid] else W.REGIONS[int(people["region"][pid])]
        prev, since = "", ""
        was = reg
        if pid in moved and reg:
            prev = W.REGIONS[(int(people["region"][pid]) + 2) % len(W.REGIONS)]
            # a move is recorded whenever it happened, which for most of them is years back
            since = W.iso(int(rng.integers(140, W.WIN_B - 20)))
            if W.day(140) < W.day(W.WIN_A) and since > W.iso(W.WIN_A):
                was = prev
        elif pid in silent:
            # a registration corrected without a recorded date, which for some of them is a
            # registration abroad resolved to a Danish region and for a few the other way about
            if not reg:
                was = W.REGIONS[(int(people["region"][pid]) + 1) % len(W.REGIONS)]
            elif pid % 17 == 0:
                was = "not stated"
            else:
                was = W.REGIONS[(int(people["region"][pid]) + 3) % len(W.REGIONS)]
        at_window_start[key] = was
        dd = de = ""
        lp = last.get(pid, -1)
        if pid in died and -1 < lp < W.NDAY - 40:
            dd = W.iso(min(W.NDAY - 1, lp + int(rng.integers(5, 60))))
        elif pid in gone and -1 < lp < W.NDAY - 40:
            de = W.iso(min(W.NDAY - 1, lp + int(rng.integers(5, 90))))
        rows.append([key, int(people["birth"][pid]), people["sex"][pid], reg, prev, since, dd, de])
    prior = [[r[0], r[1], r[2], at_window_start[r[0]]] for r in rows]
    write_csv(os.path.join(tgt, "person_register_2025Q4.csv"),
              ["person_key", "year_of_birth", "sex", "region"], prior)
    return write_csv(os.path.join(tgt, "person_register.csv"),
                     ["person_key", "year_of_birth", "sex", "region", "previous_region",
                      "region_recorded_from", "date_of_death", "date_of_emigration"], rows)


PHARMACY_NAMES = [
    ("Koebenhavn", ["Svanen", "Loeveapoteket", "Kronprinsessegade", "Oesterbro", "Noerrebro",
                    "Vesterbro Torv", "Amagerbro", "Valby Tingsted", "Frederiksberg Alle"]),
    ("Aarhus", ["Stjerne", "Banegaardspladsen", "Trojborg", "Viby Torv", "Risskov", "Hasle Torv"]),
    ("Odense", ["Vestergade", "Rosengaard", "Tarup", "Hunderup", "Dalum"]),
    ("Aalborg", ["Budolfi", "Noerresundby", "Hasseris", "Vejgaard"]),
    ("Esbjerg", ["Torvet", "Kvaglund", "Sedden"]),
    ("Randers", ["Houmeden", "Dronningborg"]),
    ("Kolding", ["Slotssoen", "Vonsild"]),
    ("Horsens", ["Soendergade", "Torsted"]),
    ("Vejle", ["Mariegade", "Soendermarken"]),
    ("Roskilde", ["Dom", "Trekroner"]),
    ("Herning", ["Vest", "Gullestrup"]),
    ("Silkeborg", ["Torvet", "Alderslyst"]),
    ("Naestved", ["Axeltorv", "Grimstrup"]),
    ("Viborg", ["Hjultorvet", "Soendersoe"]),
    ("Koege", ["Torvebyen"]),
    ("Holstebro", ["Noerreport"]),
    ("Slagelse", ["Nytorv"]),
    ("Hilleroed", ["Slotsarkaderne"]),
    ("Soenderborg", ["Perlegade"]),
    ("Svendborg", ["Moellergade"]),
    ("Hjoerring", ["Metropol"]),
    ("Frederikshavn", ["Danmarksgade"]),
    ("Haderslev", ["Gravene"]),
    ("Skive", ["Posthuset"]),
    ("Ringsted", ["Naestvedvej"]),
    ("Helsingoer", ["Stengade"]),
    ("Holbaek", ["Ahlgade"]),
    ("Fredericia", ["Gothersgade"]),
    ("Hoersholm", ["Midtpunkt"]),
    ("Lyngby", ["Storcenter"]),
    ("Glostrup", ["Hovedvejen"]),
    ("Ballerup", ["Centrum"]),
    ("Hvidovre", ["Risbjerggaard"]),
    ("Gentofte", ["Ordrup"]),
    ("Birkeroed", ["Hovedgaden"]),
    ("Taastrup", ["City2"]),
    ("Albertslund", ["Bytorvet"]),
    ("Roedovre", ["Roedovrevej"]),
    ("Greve", ["Waves"]),
    ("Solroed", ["Strandvejen"]),
    ("Farum", ["Bytorv"]),
    ("Frederikssund", ["Sillebroen"]),
    ("Kalundborg", ["Kordilgade"]),
    ("Nykoebing Falster", ["Jernbanegade"]),
    ("Nakskov", ["Axeltorv"]),
    ("Vordingborg", ["Algade"]),
    ("Faaborg", ["Graabroedretorv"]),
    ("Nyborg", ["Kongegade"]),
    ("Middelfart", ["Algade"]),
    ("Assens", ["Oestergade"]),
    ("Varde", ["Torvegade"]),
    ("Ribe", ["Seminarievej"]),
    ("Toender", ["Storegade"]),
    ("Aabenraa", ["Soendergade"]),
    ("Vejen", ["Soendergade"]),
    ("Grindsted", ["Borgergade"]),
    ("Billund", ["Hovedgaden"]),
    ("Ikast", ["Raadhusstraede"]),
    ("Struer", ["Oestergade"]),
    ("Lemvig", ["Vestergade"]),
    ("Thisted", ["Storegade"]),
    ("Nykoebing Mors", ["Algade"]),
    ("Hobro", ["Adelgade"]),
    ("Hadsund", ["Storegade"]),
    ("Aars", ["Himmerlandsgade"]),
    ("Broenderslev", ["Bredgade"]),
    ("Saeby", ["Algade"]),
    ("Skagen", ["Sankt Laurentii Vej"]),
    ("Grenaa", ["Storegade"]),
    ("Ebeltoft", ["Adelgade"]),
    ("Odder", ["Rosensgade"]),
    ("Skanderborg", ["Adelgade"]),
    ("Hedensted", ["Bytorvet"]),
    ("Brande", ["Torvegade"]),
    ("Bjerringbro", ["Storegade"]),
    ("Hammel", ["Vestergade"]),
    ("Ringkoebing", ["Algade"]),
    ("Skjern", ["Bredgade"]),
    ("Aalestrup", ["Jernbanegade"]),
    ("Stege", ["Storegade"]),
    ("Roenne", ["Store Torvegade"]),
    ("Maribo", ["Vestergade"]),
    ("Rudkoebing", ["Oerstedsgade"]),
    ("Fredensborg", ["Jernbanegade"]),
    ("Frederiksvaerk", ["Noerregade"]),
    ("Hundested", ["Noerregade"]),
    ("Stenloese", ["Egedal Centret"]),
    ("Smoerum", ["Flodvej"]),
    ("Dragoer", ["Kongevejen"]),
    ("Taarnby", ["Amager Landevej"]),
]


def closed_pharmacies(seen):
    """The pharmacies that closed inside the extract period, and the day each closed."""
    rng = np.random.default_rng(W.SEED + 61)
    ids = sorted(set(ph for _ci, ph in seen))
    pick = rng.choice(len(ids), size=6, replace=False)
    return {ids[int(i)]: int(d) for i, d in zip(pick, rng.integers(300, W.NDAY - 60, size=6))}


def write_pharmacy_register(tgt, kept):
    # the old named pharmacies carry their own name; the rest are named for their street or quarter
    NAMED = ("Svanen", "Stjerne", "Budolfi", "Dom", "Loeveapoteket", "Metropol", "Posthuset")
    flat = [(m, "%s Apotek" % n if n in NAMED else "%s %s Apotek" % (m, n))
            for m, names in PHARMACY_NAMES for n in names]
    assert len(set(x[1] for x in flat)) == len(flat), "two pharmacies would carry the same name"
    pharm_of = {}
    for ci, (code, _name) in enumerate(W.CHAINS):
        pharm_of[ci] = ["%s-%03d" % (code, 101 + j) for j in range(14 + 4 * ci)]
    moves = pharmacy_moves(pharm_of)
    home = {ph: ci for ci, lst in pharm_of.items() for ph in lst}
    seen = sorted(set(r["pharmacy"] for r in kept), key=lambda p: (home[p], p))
    closed = closed_pharmacies(set((home[p], p) for p in seen))
    rows, used = [], 0
    for ph in seen:
        muni, name = flat[used % len(flat)]
        used += 1
        now = owner_at(moves, ph, W.PULL_DAY, home[ph])
        prev, since = "", ""
        if ph in moves:
            prev = W.CHAINS[moves[ph][0]][0]
            since = W.iso(moves[ph][2])
        rows.append([ph, name, W.CHAINS[now][0], W.CHAINS[now][1], muni,
                     prev, since, W.iso(closed[ph]) if ph in closed else ""])
    return write_csv(os.path.join(tgt, "pharmacy_register.csv"),
                     ["pharmacy_id", "pharmacy_name", "chain_code", "chain_name", "municipality",
                      "previous_chain_code", "in_chain_from", "closed_on"], rows)


def write_holder_register(tgt):
    rows = []
    for code, name, cvr, merged in W.HOLDERS:
        rows.append([code, name, cvr, merged or "", W.iso(W.MERGER_DAY) if merged else "",
                     "fee payer from the merger date is the surviving company" if merged else ""])
    return write_csv(os.path.join(tgt, "holder_register.csv"),
                     ["holder_code", "holder_name", "cvr", "merged_into", "merger_date", "note"], rows)


# the signal desk's open and closed signals, each on a pair that fails the referral test on every
# route (checks.py asserts it): (product, marker) -> (opened, closed or 0, status)
TRACKER = {
    ("P01", "M2"): (520, 645, "closed, no further action"),
    ("P02", "M5"): (455, 700, "closed, product information updated"),
    ("P04", "M7"): (905, 0, "under assessment"),
    ("P05", "M2"): (505, 661, "closed, no further action"),
    ("P08", "M5"): (548, 712, "closed, referred to the committee"),
    ("P03", "M1"): (1004, 0, "under assessment"),
    ("P09", "M8"): (480, 622, "closed, no further action"),
}
TRACKED_PAIRS = list(TRACKER)


def write_tracker(tgt, first):
    """The signal desk's own tracker export: pairs opened before the window, with status.

    Chosen so that no pair it names passes the referral test on any route (checks.py asserts it).
    """
    rows = []
    for (pc, mc), (opened, closed, status) in TRACKER.items():
        mf = W.MARKETED[pc][0]
        assert mf is None or opened >= mf, (pc, opened, mf)
        rows.append(["SM-%s-%s" % (pc, mc), pc, W.PNAME[pc], mc, W.MNAME[mc],
                     W.iso(opened), W.iso(closed) if closed else "", status])
    return write_csv(os.path.join(tgt, "signal_tracker_export.csv"),
                     ["tracker_ref", "product_code", "brand_name", "marker_code", "marker_treatment",
                      "opened_on", "closed_on", "status"], rows)


QUARTER_SPAN = [("2025 Q4", 731, 822), ("2026 Q1", 823, 912),
                ("2026 Q2", 913, 1003), ("2026 Q3", 1004, 1095)]


# Adverse reactions reported per dispensing of a product, and the share of those judged serious.
# Reporting follows how visible the reaction is to the patient and the prescriber, which is a
# property of the reaction rather than of the screen: the four products the sequence screen
# separates (P03 and P04 entering the market, P05 and P08 leaving it) sit inside the range the
# other five span on every reading of this file, so no ranking of it recovers the screen's answer.
# checks.py asserts that, and the file carries no marker dimension at all.
REPORT_RATE = {"P01": 0.01297, "P02": 0.00884, "P03": 0.00980, "P04": 0.00820,
               "P05": 0.00740, "P06": 0.02000, "P07": 0.00620, "P08": 0.00880,
               "P09": 0.01090}
SERIOUS_SHARE = {"P01": 0.38, "P02": 0.21, "P03": 0.27, "P04": 0.31, "P05": 0.24,
                 "P06": 0.35, "P07": 0.19, "P08": 0.29, "P09": 0.33}
# the four products the screen's two methods disagree about
SCREEN_DECISIVE = ("P03", "P04", "P05", "P08")


def write_distractors(tgt, kept=None):
    rng = np.random.default_rng(W.SEED + 41)
    vol = collections.Counter()
    for r in (kept or []):
        code, kind = W.PKG_OF[r["vnr"]][0], W.PKG_OF[r["vnr"]][1]
        if kind != "product":
            continue
        for label, a, b in QUARTER_SPAN:
            if a <= r["day"] <= b:
                vol[(code, label)] += 1
    rows = []
    for code in W.PCODES:
        mf = W.MARKETED[code][0]
        for label, a, b in QUARTER_SPAN:
            if mf is not None and mf > b:
                continue                      # not yet on the market in that quarter
            n = vol.get((code, label), 0)
            rate = REPORT_RATE[code] * float(rng.normal(1.0, 0.13))
            base = max(0, int(round(n * max(rate, 0.0))) + int(rng.integers(-1, 2)))
            ser = int(round(base * SERIOUS_SHARE[code] * float(rng.normal(1.0, 0.18))))
            ser = min(max(ser, 0), base)
            rows.append([code, W.PNAME[code], label, base, ser,
                         min(ser, int(round(base * 0.21 * float(rng.normal(1.0, 0.4)))))])
    n1 = write_csv(os.path.join(tgt, "spontaneous_reports_summary.csv"),
                   ["product_code", "brand_name", "quarter", "reports_received",
                    "reports_serious", "reports_from_patients"], rows)
    # the screening desk's own titles, composed the way papers are titled rather than from one
    # template: a design, a question and a setting, drawn independently
    DESIGN = ["A register-based cohort study of", "A nested case-control study of",
              "A self-controlled case series of", "A cross-sectional survey of",
              "A systematic review of", "A drug-utilisation study of",
              "An interrupted time-series analysis of", "A case series of",
              "A record-linkage study of", "A prospective cohort study of"]
    TOPIC = ["initiation of %s", "persistence on %s", "discontinuation of %s",
             "co-medication with %s", "dose reduction of %s", "switching away from %s",
             "adherence to %s", "off-label use of %s", "hospital admission after %s",
             "laboratory monitoring during %s treatment", "reported reactions to %s",
             "prescribing of %s to older patients", "%s in renal impairment",
             "%s and the risk of fracture", "%s after a safety communication",
             "the first two years of %s on the market"]
    SETTING = ["in Danish primary care", "in the Nordic countries", "in nursing homes",
               "in hospital outpatient clinics", "among women of childbearing age",
               "in patients over 75", "across five regions", "in a national register",
               "before and after the reimbursement change", "in general practice", "",
               "in a prescription register", "among new users", "in routine care"]
    # the desk notes the signal a screened-in paper was read against, where it has one open
    tracked = {W.PNAME[pc]: "SM-%s-%s" % (pc, mc) for pc, mc in TRACKED_PAIRS}
    subjects = [W.PNAME[c] for c in W.PCODES] + sorted(
        set(n for code in W.MCODES for n in MARKER_NAMES[code]))
    rows, day = [], 1001
    for i in range(96):
        name = subjects[int(rng.integers(0, len(subjects)))]
        day += int(rng.choice([0, 1, 2, 3, 4, 7], p=[0.21, 0.26, 0.19, 0.13, 0.11, 0.10]))
        day = min(day, W.PULL_DAY - 3)
        decision = "screened in" if rng.random() < 0.22 else "not relevant"
        rows.append(["LS-2026-%03d" % (i + 1), W.iso(day),
                     (" ".join([DESIGN[int(rng.integers(0, len(DESIGN)))],
                                TOPIC[int(rng.integers(0, len(TOPIC)))] % name,
                                SETTING[int(rng.integers(0, len(SETTING)))]]).strip()
                      .replace("  ", " ")), name,
                     str(rng.choice(["Embase", "Medline", "Scopus", "Web of Science"],
                                    p=[0.41, 0.33, 0.17, 0.09])),
                     decision,
                     tracked.get(name, "") if decision == "screened in" else ""])
    n2 = write_csv(os.path.join(tgt, "literature_screening_log.csv"),
                   ["screening_ref", "screened_on", "title", "medicine", "source", "decision",
                    "read_against"], rows)
    return n1, n2


def write_manifest(tgt, counts):
    rows = [["(extract scope)", "", EXTRACT_SCOPE, W.iso(W.PULL_DAY)]]
    notes = {
        "dispensings_2023_2025.csv": "dispensings to 30 September 2025, register layout R-2023.2",
        "dispensings_2025_2026.csv": "dispensings from 1 October 2025, register layout R-2025.1",
        "submission_exceptions.csv": "validation outcomes for the lines the register turned back",
        "pharmacy_submission_log.csv": "the chains' own monthly totals, counted by month of submission",
        "package_index.csv": "package codes with the dates each was valid for dispensing",
        "person_register.csv": "one row per current person key, as the civil registration system recorded it at the pull",
        "register_variable_documentation.csv": "the register's documentation of the variables in this extract",
    }
    for name in sorted(counts):
        rows.append([name, counts[name], notes.get(name, ""), W.iso(W.PULL_DAY)])
    return write_csv(os.path.join(tgt, "extract_manifest.csv"),
                     ["file_name", "rows", "note", "pulled_on"], rows)


def write_release_notes(tgt):
    obj = {
        "register": "Laegemiddelstatistikregisteret",
        "release": "R-2025.1",
        "released_on": W.iso(731),
        "supersedes": "R-2023.2",
        "summary": ("The October 2025 release renames five variables and writes dates as "
                    "DD-MM-YYYY. Extracts covering periods on both sides of the release are "
                    "delivered as one file per layout."),
        "renamed_variables": [
            {"was": "pseudonym", "is": "person_key"},
            {"was": "vnr", "is": "package_code"},
            {"was": "disp_date", "is": "date_of_dispensing"},
            {"was": "packages", "is": "n_packages"},
            {"was": "submitted", "is": "submission_date"}],
        "layouts": [
            {"layout": "R-2023.2", "file": "dispensings_2023_2025.csv",
             "date_format": "YYYY-MM-DD", "columns": OLD_HEAD,
             "covers": "dispensings up to 30 September 2025"},
            {"layout": "R-2025.1", "file": "dispensings_2025_2026.csv",
             "date_format": "DD-MM-YYYY", "columns": NEW_HEAD,
             "covers": "dispensings from 1 October 2025"}],
        "variable_documentation": "register_variable_documentation.csv",
    }
    path = os.path.join(tgt, "register_release_notes.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    return 1


def write_annexes(tgt):
    """The run's own parameter file: the pairs Annexes A and B put on the screen."""
    rows = []
    for pc in W.PCODES:
        for mc in W.ANNEX[pc]:
            rows.append([pc, W.PNAME[pc], W.PATC[pc], mc, W.MNAME[mc], W.MATC[mc],
                         "Standard 7-2024 Annex A and Annex B"])
    return write_csv(os.path.join(tgt, "screen_annexes.csv"),
                     ["product_code", "brand_name", "product_atc", "marker_code",
                      "marker_treatment", "marker_atc_group", "source"], rows)


VARIABLE_DOC = [
    ("dispensings_2025_2026.csv", "record_id",
     "Identifies the transmission in which the register received the line. A dispensing "
     "re-transmitted after a failed transfer is given a new record identifier on each "
     "transmission; the register holds one dispensing behind them and counts it once, in its "
     "lines and in its doses."),
    ("dispensings_2025_2026.csv", "person_key",
     "The pseudonym the register holds for the patient. Where a pseudonym has been replaced, lines "
     "dispensed before the replacement carry the retired pseudonym and "
     "person_key_crosswalk.csv gives the pair; the register holds one patient behind them."),
    ("dispensings_2025_2026.csv", "package_code",
     "The Nordic article number of the package handed out. A package code identifies one package "
     "of one product only between the dates package_index.csv gives for it, and the register "
     "reads the product from the code at the date of the dispensing."),
    ("dispensings_2025_2026.csv", "date_of_dispensing",
     "The date the pharmacy handed the package to the patient. The register places a dispensing "
     "in the day, month, quarter and year of this date."),
    ("dispensings_2025_2026.csv", "submission_date",
     "The date the pharmacy chain transmitted the line to the register. It is on or after the "
     "date of dispensing and may fall in a later month or quarter."),
    ("dispensings_2025_2026.csv", "n_packages",
     "Packages handed out on the line. Defined daily doses are this times the package's "
     "ddd_per_pack in package_index.csv, where the anatomical therapeutic chemical index assigns "
     "the package a defined daily dose."),
    ("dispensings_2025_2026.csv", "pharmacy",
     "The dispensing pharmacy. pharmacy_register.csv gives its chain."),
    ("dispensings_2025_2026.csv", "prescriber",
     "The prescriber's authorisation number as the prescription carried it."),
    ("dispensings_2023_2025.csv", "pseudonym, vnr, disp_date, packages, submitted",
     "The names release R-2023.2 gave person_key, package_code, date_of_dispensing, n_packages "
     "and submission_date. The variables are the same and carry the same meaning; only the names "
     "and the date format changed at release R-2025.1."),
    ("dispensings_2023_2025.csv", "line_id",
     "The line's identifier in release R-2023.2. It is unique in this file and is not comparable "
     "with the record identifiers release R-2025.1 writes."),
    ("dispensings_2023_2025.csv", "pharmacy_id, prescriber_id",
     "The dispensing pharmacy and the prescriber's authorisation number, under the names release "
     "R-2023.2 gave them."),
    ("package_index.csv", "vnr",
     "The Nordic article number. One number is given to one package of one product at a time and "
     "may be reissued to another package after it has been withdrawn."),
    ("package_index.csv", "atc_code",
     "The anatomical therapeutic chemical code of the package's substance, to the level the index "
     "codes it. atc_text.csv gives the code's text."),
    ("package_index.csv", "preparation, strength, pack_size",
     "The preparation's name, the strength of one unit and the number of units in the package, as "
     "the package register holds them."),
    ("package_index.csv", "valid_from, valid_to",
     "The period in which the package code was valid for dispensing. A code withdrawn on a "
     "transfer of marketing authorisation keeps its rows, so that lines dispensed before the "
     "transfer still resolve."),
    ("package_index.csv", "ddd_per_pack",
     "Defined daily doses in the package: pack size times strength divided by the defined daily "
     "dose the anatomical therapeutic chemical index assigns the substance. Blank where the index "
     "assigns none, as for topical preparations."),
    ("person_register.csv", "region",
     "The region recorded for the patient at the extract date. Where region_recorded_from falls "
     "inside the extract period, previous_region is the region recorded before that date."),
    ("person_register.csv", "year_of_birth",
     "Year of birth as the civil registration system holds it."),
    ("person_register.csv", "person_key",
     "The pseudonym the register holds for the patient at the extract date. A patient whose "
     "pseudonym was replaced appears here under the current one only, and "
     "person_key_crosswalk.csv gives the retired one."),
    ("person_register.csv", "sex",
     "Sex as the civil registration system holds it: K for a woman, M for a man."),
    ("person_register.csv", "region_recorded_from",
     "The date the current region was recorded. Blank where the region has not changed inside the "
     "extract period."),
    ("person_register.csv", "date_of_death, date_of_emigration",
     "The date the civil registration system records the patient as having died or as having left "
     "the country. Blank for a patient it records as neither."),
    ("submission_exceptions.csv", "person_key, vnr, date_of_dispensing, pharmacy, submitted_on",
     "The line as the pharmacy transmitted it. The values are the pharmacy's, not the register's, "
     "because the line was never written to a dispensing extract."),
    ("submission_exceptions.csv", "rejection_reason",
     "The validation rule the line failed. One rule is recorded for a line even where it fails "
     "more than one."),
    ("submission_exceptions.csv", "submitted_on",
     "The date the chain transmitted the line. A line turned back may be transmitted again, and "
     "the later transmission is a row of its own in the dispensing extract, not here."),
    ("pharmacy_submission_log.csv", "lines_submitted, lines_accepted, lines_turned_back, "
                                    "lines_withdrawn_by_chain",
     "The chains' own monthly counts, by the month the chain transmitted the lines. They are the "
     "chains' figures and not the register's, so they do not reconcile to the extract line for "
     "line: a chain counts lines it withdrew before the register wrote them, and a batch sent "
     "after a month's cut-off is counted by the chain in the month it sent it."),
    ("pharmacy_register.csv", "pharmacy_id, pharmacy_name, chain_code, chain_name",
     "The dispensing pharmacy, the name it trades under and the chain that owns it. A pharmacy "
     "keeps its identifier if it changes chain."),
    ("pharmacy_register.csv", "municipality",
     "The municipality the pharmacy is sited in, as the authorisation register holds it."),
    ("pharmacy_register.csv", "closed_on",
     "The date the pharmacy's authorisation to dispense ended. Blank for a pharmacy still open "
     "at the extract date. The register holds a closed pharmacy so that its earlier lines "
     "resolve."),
    ("product_register.csv", "product_code, brand_name, atc_code",
     "The product as the authorisation register holds it. The product code is the division's "
     "own and is the code Annex A of Standard 7-2024 uses."),
    ("product_register.csv", "holder_code, previous_holder_code, holder_code_from",
     "The marketing authorisation holder at the extract date, the holder before the latest "
     "transfer, and the date that transfer took effect. Both are blank where the authorisation "
     "has never been transferred."),
    ("product_register.csv", "first_marketed, authorisation_valid_to",
     "The first day the product could be dispensed in Denmark and, where the authorisation has "
     "lapsed, the last. Blank where the authorisation is still in force."),
    ("holder_register.csv", "holder_code, holder_name, cvr",
     "The marketing authorisation holder and its central business register number."),
    ("holder_register.csv", "merged_into, merger_date",
     "Where a holder has merged into another company, the company that survives the merger and "
     "the date it took effect. Both are blank for a holder that has not merged."),
    ("screen_annexes.csv", "product_code, marker_code",
     "One row per pair of a product in Annex A of Standard 7-2024 and a marker treatment group "
     "in its Annex B, as the standard lists them for this run."),
    ("signal_tracker_export.csv", "tracker_ref, opened_on, closed_on, status",
     "The division's signal management tracker as it stood at the extract date: the reference "
     "it gave the signal, the day it was opened, the day it was closed where it has been, and "
     "the status it then carried."),
    ("person_key_crosswalk.csv", "retired_person_key, current_person_key, replaced_on, reason",
     "A pseudonym the register has replaced, the pseudonym that replaced it, the day of the "
     "replacement and the civil-registration event behind it."),
    ("atc_text.csv", "atc_code, atc_text, edition",
     "The text the anatomical therapeutic chemical index gives a code, and the edition of the "
     "index the text is taken from."),
    ("(codelist)", "sex",
     "K a woman, M a man, as the civil registration system codes it."),
    ("(codelist)", "region",
     "Hovedstaden, Midtjylland, Nordjylland, Sjaelland, Syddanmark. A patient the civil "
     "registration system records outside Denmark carries no region."),
    ("(codelist)", "rejection_reason",
     "prescriber identifier not in the authorisation register; package code not valid on the "
     "date of dispensing; reimbursement code missing; pharmacy identifier closed before the "
     "date of dispensing; reimbursed price missing for the package on that date."),
    ("(codelist)", "status",
     "under assessment; closed, no further action; closed, product information updated; "
     "closed, referred to the committee."),
    ("(codelist)", "reason",
     "The events that replace a pseudonym: civil registration number corrected; duplicate "
     "registration resolved; pseudonymisation key regenerated after a data correction."),
    ("submission_exceptions.csv", "exception_ref",
     "One row for every line the register turned back at validation. A line turned back is not "
     "written to the dispensing extracts and has to be re-submitted to be held."),
]


def write_variable_documentation(tgt):
    rows = [[f, c, t] for f, c, t in VARIABLE_DOC]
    return write_csv(os.path.join(tgt, "register_variable_documentation.csv"),
                     ["file_name", "variable", "documentation"], rows)
