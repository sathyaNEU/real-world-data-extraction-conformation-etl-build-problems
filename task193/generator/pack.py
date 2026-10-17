"""task193: the register extracts, the lookup tables and the operating files."""
import collections
import csv
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
def dispensings(first):
    """Every dispensing line in the clean truth, plus the patient attributes behind them."""
    rng = np.random.default_rng(W.SEED + 11)
    n = W.N_PAT
    chain_of = rng.choice(len(W.CHAINS), size=n, p=[0.37, 0.28, 0.21, 0.14])
    region_of = rng.choice(len(W.REGIONS), size=n, p=W.REGION_W)
    outside = rng.random(n) < 0.023                     # registered outside Denmark at window start
    birth = rng.integers(1934, 2008, size=n)
    sex = np.where(rng.random(n) < 0.508, "K", "M")
    pharm_of = {}
    for ci, (code, name) in enumerate(W.CHAINS):
        pharm_of[ci] = ["%s-%03d" % (code, 101 + j) for j in range(14 + 4 * ci)]
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
                mu = [[1.4, 1.9, 2.6, 2.2], [3.3, 2.8, 3.9, 4.5],
                      [4.6, 5.4, 6.3, 5.7], [6.1, 7.2, 6.6, 8.0]][ci][q]
                lag = 1 + int(rng.poisson(mu))
                lid += 1
                lines.append({"line": lid, "pid": int(pid), "code": code, "vnr": vnr, "day": d,
                              "pharmacy": ph, "chain": ci, "packs": npk,
                              "submitted": min(d + lag, W.NDAY + 20), "prescriber": pres,
                              "is_first": j == 0})
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
    keys = {}
    for pid in range(n):
        keys[pid] = "PK%07d" % (3100000 + 83 * pid)
    new_keys = {}
    for pid in switch_day:
        new_keys[pid] = "PK%07d" % (8400000 + 211 * pid)
    for r in lines:
        pid = r["pid"]
        if pid in switch_day and r["day"] >= switch_day[pid]:
            r["key"] = new_keys[pid]
        else:
            r["key"] = keys[pid]
    # (2) the rejected lines: repeat dispensings the register turned back at validation,
    #     so no patient's first receipt of anything is touched
    repeats = [i for i, r in enumerate(lines) if not r["is_first"]]
    rej_idx = set(rng.choice(repeats, size=int(0.031 * len(lines)), replace=False).tolist())
    rejected, kept = [], []
    reasons = ["prescriber identifier not in the authorisation register",
               "package code not valid on the date of dispensing",
               "reimbursement code missing",
               "pharmacy identifier closed before the date of dispensing",
               "duplicate of a line already accepted in this batch"]
    for i, r in enumerate(lines):
        if i in rej_idx:
            r["reason"] = str(rng.choice(reasons, p=[0.407, 0.231, 0.168, 0.117, 0.077]))
            rejected.append(r)
        else:
            kept.append(r)
    # (3) one chain's first batch of the window re-sent under fresh line identifiers
    resent = [r for r in kept if r["chain"] == 0 and 731 <= r["day"] <= 761]
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


MARKER_NAMES = {
    "M1": ["Ondasetron", "Metoclopramid", "Domperidon", "Aprepitant"],
    "M2": ["Pantoprazol", "Esomeprazol", "Lansoprazol", "Omeprazol"],
    "M3": ["Allopurinol", "Febuxostat", "Allopurinol Orion", "Febuxostat Teva"],
    "M4": ["Furosemid", "Bumetanid", "Furix", "Burinex"],
    "M5": ["Sertralin", "Citalopram", "Escitalopram", "Fluoxetin"],
    "M6": ["Zopiclon", "Zolpidem", "Imozop", "Stilnoct"],
    "M7": ["Betamethason", "Mometason", "Elocon", "Diprosalic"],
    "M8": ["Olanzapin", "Quetiapin", "Zyprexa", "Seroquel"],
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


def write_package_index(tgt):
    rows = []
    for code in W.PCODES + W.MCODES:
        sizes = W.PACK_SIZES[code]
        unit = W.DDD_PER_UNIT[code]
        for i, (vnr, c, kind, vf, vt) in enumerate(W.PACKAGES[code]):
            if kind == "product":
                name, atc = W.PNAME[code], W.PATC[code]
                st = STRENGTH[code][i % len(STRENGTH[code])]
            else:
                name, atc = MARKER_NAMES[code][i % 4], W.MATC[code]
                st = MARK_STRENGTH[code][i % 4]
            size = sizes[i % len(sizes)]
            rows.append([vnr, atc, name, st, size, round(size * unit, 2),
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
    rows = sorted([k, v, "ATC 2026 edition"] for k, v in text.items())
    return write_csv(os.path.join(tgt, "atc_text.csv"), ["atc_code", "atc_text", "edition"], rows)


def write_crosswalk(tgt, switch_day, keys, new_keys):
    reasons = ["civil registration number corrected", "duplicate registration resolved",
               "pseudonymisation key regenerated after a data correction"]
    rows = []
    for i, pid in enumerate(sorted(switch_day)):
        rows.append([keys[pid], new_keys[pid], W.iso(switch_day[pid]), reasons[i % 3]])
    rows.sort(key=lambda r: r[2])
    return write_csv(os.path.join(tgt, "person_key_crosswalk.csv"),
                     ["retired_person_key", "current_person_key", "replaced_on", "reason"], rows)


def write_person_register(tgt, people, keys, new_keys, switch_day, kept):
    rng = np.random.default_rng(W.SEED + 29)
    seen = set(r["pid"] for r in kept)
    rows = []
    moved = set(rng.choice(sorted(seen), size=int(0.021 * len(seen)), replace=False).tolist())
    died = set(rng.choice(sorted(seen), size=int(0.016 * len(seen)), replace=False).tolist())
    gone = set(rng.choice(sorted(seen), size=int(0.007 * len(seen)), replace=False).tolist())
    last = {}
    for r in kept:
        last[r["pid"]] = max(last.get(r["pid"], -1), r["day"])
    for pid in sorted(seen):
        key = new_keys.get(pid, keys[pid])
        reg = "" if people["outside"][pid] else W.REGIONS[int(people["region"][pid])]
        prev, since = "", ""
        if pid in moved and reg:
            prev = W.REGIONS[(int(people["region"][pid]) + 2) % len(W.REGIONS)]
            since = W.iso(int(rng.integers(W.WIN_A + 20, W.WIN_B - 20)))
        dd = de = ""
        if pid in died and last[pid] < W.NDAY - 40:
            dd = W.iso(min(W.NDAY - 1, last[pid] + int(rng.integers(5, 60))))
        elif pid in gone and last[pid] < W.NDAY - 40:
            de = W.iso(min(W.NDAY - 1, last[pid] + int(rng.integers(5, 90))))
        rows.append([key, int(people["birth"][pid]), people["sex"][pid], reg, prev, since, dd, de])
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
]


def write_pharmacy_register(tgt, kept):
    flat = [(m, "%s %s Apotek" % (m, n) if n not in ("Svanen", "Stjerne", "Budolfi", "Dom")
             else "%s Apotek" % n) for m, names in PHARMACY_NAMES for n in names]
    seen = sorted(set((r["chain"], r["pharmacy"]) for r in kept))
    rows = []
    per = collections.defaultdict(int)
    for ci, ph in seen:
        j = (per[ci] * 4 + ci * 7) % len(flat)
        per[ci] += 1
        muni, name = flat[j]
        rows.append([ph, name, W.CHAINS[ci][0], W.CHAINS[ci][1], muni])
    return write_csv(os.path.join(tgt, "pharmacy_register.csv"),
                     ["pharmacy_id", "pharmacy_name", "chain_code", "chain_name", "municipality"], rows)


def write_holder_register(tgt):
    rows = []
    for code, name, cvr, merged in W.HOLDERS:
        rows.append([code, name, cvr, merged or "", W.iso(W.MERGER_DAY) if merged else "",
                     "fee payer from the merger date is the surviving company" if merged else ""])
    return write_csv(os.path.join(tgt, "holder_register.csv"),
                     ["holder_code", "holder_name", "cvr", "merged_into", "merger_date", "note"], rows)


def write_tracker(tgt, first):
    """The signal desk's own tracker export: pairs opened before the window, with status.

    Chosen so that no pair it names passes the referral test on any route (checks.py asserts it).
    """
    rows = []
    picks = [("P01", "M2", 520, 645, "closed, no further action"),
             ("P02", "M5", 455, 700, "closed, product information updated"),
             ("P04", "M7", 612, 0, "under assessment"),
             ("P05", "M2", 398, 589, "closed, no further action"),
             ("P08", "M5", 505, 668, "closed, referred to the committee"),
             ("P03", "M1", 701, 0, "under assessment"),
             ("P09", "M8", 480, 622, "closed, no further action")]
    for pc, mc, opened, closed, status in picks:
        rows.append(["SM-%s-%s" % (pc, mc), pc, W.PNAME[pc], mc, W.MNAME[mc],
                     W.iso(opened), W.iso(closed) if closed else "", status])
    return write_csv(os.path.join(tgt, "signal_tracker_export.csv"),
                     ["tracker_ref", "product_code", "brand_name", "marker_code", "marker_treatment",
                      "opened_on", "closed_on", "status"], rows)


def write_distractors(tgt):
    rng = np.random.default_rng(W.SEED + 41)
    rows = []
    for code in W.PCODES:
        for q, label in enumerate(["2025 Q4", "2026 Q1", "2026 Q2", "2026 Q3"]):
            base = 4 + int(rng.integers(0, 29))
            ser = int(round(base * float(rng.uniform(0.17, 0.62))))
            rows.append([code, W.PNAME[code], label, base, ser,
                         int(round(ser * float(rng.uniform(0.1, 0.8))))])
    n1 = write_csv(os.path.join(tgt, "spontaneous_reports_summary.csv"),
                   ["product_code", "brand_name", "quarter", "reports_received",
                    "reports_serious", "reports_from_patients"], rows)
    titles = ["Hepatic safety of %s in routine care", "A case series of %s exposure in pregnancy",
              "Prescribing trends for %s in primary care", "Adherence to %s over twelve months",
              "Renal outcomes among new users of %s", "Switching patterns away from %s"]
    rows = []
    for i in range(96):
        code = W.PCODES[i % len(W.PCODES)]
        rows.append(["LS-2026-%03d" % (i + 1), W.iso(1000 + (i * 3) % 95),
                     titles[i % len(titles)] % W.PNAME[code], W.PNAME[code],
                     ["Embase", "Medline", "Scopus"][i % 3],
                     ["not relevant", "not relevant", "screened in", "not relevant"][i % 4]])
    n2 = write_csv(os.path.join(tgt, "literature_screening_log.csv"),
                   ["screening_ref", "screened_on", "title", "medicine", "source", "decision"], rows)
    return n1, n2


def write_manifest(tgt, counts):
    rows = []
    notes = {
        "dispensings_2023_2025.csv": "clearance-period extract, register layout R-2023.2, ISO dates",
        "dispensings_2025_2026.csv": "screen-window extract, register layout R-2025.1, day-month-year dates",
        "submission_exceptions.csv": "every line the register turned back at validation over the screen window and the clearance period; rejected lines are not in either extract",
        "pharmacy_submission_log.csv": "the chains' own monthly submission totals, by month of submission",
        "package_index.csv": "package codes with the dates each was valid for dispensing",
        "person_register.csv": "one row per person key appearing in either extract, attributes as recorded at the pull",
    }
    for name in sorted(counts):
        rows.append([name, counts[name], notes.get(name, ""), W.iso(W.PULL_DAY)])
    return write_csv(os.path.join(tgt, "extract_manifest.csv"),
                     ["file_name", "rows", "note", "pulled_on"], rows)


def write_release_notes(tgt):
    obj = {
        "register": "Laegemiddelstatistikregisteret",
        "extract_request": "LSR-2026-0441",
        "pulled_on": W.iso(W.PULL_DAY),
        "layouts": [
            {"layout": "R-2023.2", "file": "dispensings_2023_2025.csv",
             "date_format": "YYYY-MM-DD",
             "columns": OLD_HEAD,
             "note": "in use for extracts covering dispensings up to 30 September 2025"},
            {"layout": "R-2025.1", "file": "dispensings_2025_2026.csv",
             "date_format": "DD-MM-YYYY",
             "columns": NEW_HEAD,
             "note": "in use from the October 2025 release; pseudonym, vnr, disp_date, packages and submitted were renamed person_key, package_code, date_of_dispensing, n_packages and submission_date"}],
        "known_handling": [
            "A line turned back at validation is not written to the extract. The validation outcome for every line is in submission_exceptions.csv.",
            "One chain re-sent its batch for October 2025 after a transmission failure. The resent lines carry fresh record identifiers and repeat the original line's person key, package code, date of dispensing, pharmacy and submission stamp. A line re-sent after a transmission failure is one dispensing: it counts once in any count of lines and once in any count of doses.",
            "The register reports a dispensing line in the quarter of its date of dispensing, whatever quarter it was submitted in. The chains' own submission log in pharmacy_submission_log.csv counts by month of submission instead, which is why its totals do not line up with the extract quarter by quarter.",
            "The extract covers patients aged 18 and over at the start of the screen window; the register's paediatric population is extracted separately and is not in this request.",
            "Person keys replaced after a civil-registration correction are listed in person_key_crosswalk.csv with the date of replacement. Lines dispensed before that date carry the retired key.",
            "Package codes are valid for dispensing only between the dates package_index.csv gives for them."]
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
