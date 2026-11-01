"""Writes the pack under target/ from the clean truth, in the region's own export conventions (Layer 1)."""
import datetime as dt
import os
import random

import asks_world as AW
import io_util as IO
import params as P

FILES = {
    "dispensings": "statin_dispensings_202407_202612.csv",
    "products": "statin_products.csv",
    "ddd": "atc_ddd_2026.xlsx",
    "practices": "practice_register_2026.xlsx",
    "pharmacies": "pharmacies.csv",
    "programme": "statin_followup_programme_2027.pdf",
    "agreement": "pharmacy_pilot_agreement_2026.pdf",
    "conversations": "pilot_conversations_2026.xlsx",
    "statements": "pilot_statements_2026.pdf",
    "published": "regional_statin_use_ddd_2025.xlsx",
    "survey": "patient_survey_general_practice_2026.xlsx",
    "benchmark": "national_persistence_report_2025.pdf",
}
DISTRACTORS = ["published", "survey", "benchmark"]
STAMP = dt.datetime(2027, 2, 12, 8, 40)


def fmt_date(d):
    """The extract stitches the register's old system (to 31 December 2024, day-month-year) to the new (ISO)."""
    return d.strftime("%d-%m-%Y") if d.year < 2025 else d.isoformat()


def write_dispensings(W, A, path):
    rows = [[r["id"], r["sex"], r["born"].isoformat(), fmt_date(r["date"]), r["product"], r["packs"], r["prescriber"],
             r["pharmacy"]] for r in A.rows]
    return IO.write_csv(path, ["pseudonym", "sex", "birth_date", "dispensing_date", "product_number", "packs",
                               "prescriber_id", "pharmacy_id"], rows)


def write_products(W, path):
    rows = [[p.number, p.name, p.atc, "%d mg" % p.strength, p.pack] for p in sorted(W.products, key=lambda p: p.number)]
    return IO.write_csv(path, ["product_number", "product_name", "atc_code", "strength", "pack_size_tablets"], rows)


def write_ddd(path):
    rows = [["C10AA01", "simvastatin", 30, "mg", "O"], ["C10AA02", "lovastatin", 45, "mg", "O"],
            ["C10AA03", "pravastatin", 30, "mg", "O"], ["C10AA04", "fluvastatin", 60, "mg", "O"],
            ["C10AA05", "atorvastatin", 20, "mg", "O"], ["C10AA07", "rosuvastatin", 10, "mg", "O"],
            ["C10AA08", "pitavastatin", 2, "mg", "O"]]
    IO.write_xlsx(path, [("DDD", ["atc_code", "substance", "ddd", "unit", "route"], rows,
                          ["ATC/DDD index, lipid modifying agents (C10AA), as applied by the region from 1 January 2026"])],
                  ("Medicines unit", "Laust Jessen", "2026-01-08T09:12:00Z", "2026-01-08T09:20:00Z",
                   "ATC DDD 2026", "Region Lindholt"))
    return len(rows)


def write_practices(path, rng):
    rows = []
    for code, name, town, *rest in P.PRACTICES:
        base = rng.randint(2400, 8800)
        sizes = [int(base * (1 + rng.uniform(-0.02, 0.025))) for _ in range(4)]
        rows.append([code, name, town] + sizes)
    IO.write_xlsx(path, [("Practices", ["provider_number", "practice_name", "town", "listed_2026_q1", "listed_2026_q2",
                                        "listed_2026_q3", "listed_2026_q4"], rows, None)],
                  ("Practice planning", "Practice planning", "2026-12-14T10:02:00Z", "2027-01-06T08:47:00Z",
                   "Practice register 2026", "Region Lindholt"))
    return len(rows)


def write_pharmacies(path):
    return IO.write_csv(path, ["pharmacy_id", "pharmacy_name", "town"], [list(x) for x in AW.PHARMACIES])


def write_programme(path):
    blocks = [
        ("t", "Statin follow-up programme 2027"),
        ("s", "Region Lindholt, medicines unit. Programme description adopted by the practice planning committee on "
              "26 January 2027."),
        ("h", "1. Purpose"),
        ("p", "From 2027 the region funds a pharmacist-led follow-up of patients who start a statin, offered through the "
              "general practices where patients most often stop their treatment within the first year."),
        ("h", "2. Which practices join"),
        ("p", "2.1 A general practice joins the programme in 2027 when fewer than 60 per cent of its new statin users of "
              "the second half of 2025 were persistent for twelve months."),
        ("h", "3. Definitions"),
        ("p", "3.1 A new statin user is a patient whose first statin dispensing (ATC C10AA) between 1 July and 31 "
              "December 2025 followed no statin dispensing in the 365 days before it. The patient belongs to the "
              "practice that issued the prescription for that first dispensing; a patient whose first dispensing was "
              "prescribed at a hospital belongs to no practice."),
        ("p", "3.2 A new statin user was persistent for twelve months when, in the 365 days from the first dispensing, "
              "the patient was never more than 30 days in a row without tablets. The tablets of a dispensing last as "
              "long as it takes the patient to use them at the daily dose they take; tablets left from an earlier "
              "dispensing are used before those of a later one."),
        ("p", "3.3 A practice's continuing statin users in 2026 are the persons who had a statin dispensed in each "
              "quarter of 2026, each person counted once, at the practice that prescribed their last dispensing of "
              "2026."),
        ("h", "4. Follow-up"),
        ("p", "The pharmacies that took part in the 2026 pilot offer the conversations. The medicines unit reviews the "
              "selection after the 2026 cohort has completed its first year."),
    ]
    IO.write_pdf(path, "Statin follow-up programme 2027", "Medicines unit", "Region Lindholt", blocks,
                 "Region Lindholt, medicines unit, statin follow-up programme 2027", "D:20270126143000+01'00'",
                 "D:20270126143000+01'00'")


def write_agreement(path):
    blocks = [
        ("t", "Pharmacy pilot 2026: statin follow-up conversations"),
        ("s", "Agreement between Region Lindholt and the participating pharmacies, signed 15 December 2025."),
        ("h", "1. The conversation"),
        ("p", "A follow-up conversation is a meeting of at least fifteen minutes between a pharmacist and a patient who "
              "started a statin, held at the pharmacy and entered in the pilot's conversation log."),
        ("h", "2. Payment"),
        ("p", "2.1 The region pays each pharmacy its agreed rate for every follow-up conversation held in 2026. A "
              "conversation that is cancelled is not paid."),
        ("p", "2.2 Each quarter the region draws up a statement for each pharmacy on the quarter's last day, covering "
              "the conversations held in the quarter and not cancelled by then. The rate agreed with each pharmacy is "
              "set out in its own annex."),
    ]
    IO.write_pdf(path, "Pharmacy pilot agreement 2026", "Medicines unit", "Region Lindholt", blocks,
                 "Region Lindholt, pharmacy pilot 2026", "D:20251215101500+01'00'", "D:20251215101500+01'00'")


def write_conversations(A, path):
    rows = [[c["no"], c["pharmacy"], c["date"].isoformat(), c["status"],
             c["cancelled"].isoformat() if c["cancelled"] else ""] for c in A.conversations]
    IO.write_xlsx(path, [("Conversations", ["conversation_no", "pharmacy_id", "conversation_date", "status",
                                            "cancelled_date"], rows, None)],
                  ("Britta Winther", "Britta Winther", "2026-01-05T08:00:00Z", "2027-02-10T15:21:00Z",
                   "Pilot conversation log 2026", "Region Lindholt"))
    return len(rows)


def nl_money(x):
    s = "%.2f" % x
    whole, frac = s.split(".")
    parts = []
    while len(whole) > 3:
        parts.insert(0, whole[-3:])
        whole = whole[:-3]
    parts.insert(0, whole)
    return ".".join(parts) + "," + frac


def write_statements(A, path):
    blocks = [("t", "Pharmacy pilot 2026: quarterly statements"),
              ("s", "Region Lindholt, finance. Statements as sent to the pharmacies.")]
    names = {c: n for c, n, t in AW.PHARMACIES}
    for qi in range(1, 5):
        rows = [["Pharmacy", "Statement date", "Amount (DKK)"]]
        for s in A.statements:
            if s["quarter"] == qi:
                rows.append(["%s (%s)" % (names[s["pharmacy"]], s["pharmacy"]), s["date"].strftime("%d.%m.%Y"),
                             nl_money(s["amount"])])
        blocks += [("h", "Quarter %d, 2026" % qi), ("table", rows)]
    IO.write_pdf(path, "Pilot statements 2026", "Ester Poulsen", "Region Lindholt", blocks,
                 "Region Lindholt, finance, pharmacy pilot statements 2026", "D:20270105091000+01'00'",
                 "D:20270105091000+01'00'", colw={3: [240, 110, 120]})


def write_distractors(W, target, rng):
    rows = []
    for code, name, town, *rest in P.PRACTICES:
        for q in range(1, 5):
            rows.append([town, "2025-Q%d" % q, round(rng.uniform(78, 132), 1)])
    rows = sorted({(a, b): c for a, b, c in rows}.items())
    IO.write_xlsx(os.path.join(target, FILES["published"]),
                  [("Statin use", ["town", "quarter", "ddd_per_1000_inhabitants_per_day"],
                    [[a, b, c] for (a, b), c in rows],
                    ["Statin use by town, 2025, as published on the region's website on 14 March 2026"])],
                  ("Medicines unit", "Medicines unit", "2026-03-14T09:00:00Z", "2026-03-14T09:00:00Z",
                   "Statin use 2025", "Region Lindholt"))
    srows = [[code, name, rng.randint(80, 260), round(rng.uniform(3.6, 4.7), 2), round(rng.uniform(55, 92), 1)]
             for code, name, town, *rest in P.PRACTICES]
    IO.write_xlsx(os.path.join(target, FILES["survey"]),
                  [("Survey 2026", ["provider_number", "practice_name", "respondents", "mean_score_1_to_5",
                                    "pct_would_recommend"], srows,
                    ["Patient survey of general practice, autumn 2026, fieldwork September to October 2026"])],
                  ("Survey team", "Survey team", "2026-11-20T12:00:00Z", "2026-11-20T12:00:00Z",
                   "Patient survey 2026", "Region Lindholt"))
    blocks = [("t", "Persistence with statins in Denmark, 2025"),
              ("s", "National report on medicine use, published October 2025."),
              ("p", "Among patients who started a statin in 2023, 64 per cent were still collecting their tablets twelve "
                    "months later. Persistence was higher among patients over 65 and among those who started after a "
                    "cardiovascular event."),
              ("table", [["Substance", "New users 2023", "Persistent at 12 months (%)"],
                         ["atorvastatin", "41,280", "65"], ["rosuvastatin", "12,940", "63"],
                         ["simvastatin", "9,870", "61"], ["pravastatin", "1,120", "58"]]),
              ("p", "Persistence in this report is measured by collection of a new pack within 180 days of the "
                    "previous one.")]
    IO.write_pdf(os.path.join(target, FILES["benchmark"]), "Persistence with statins 2025", "Medicine statistics",
                 "Medicine statistics", blocks, "National report on medicine use 2025", "D:20251020100000+02'00'",
                 "D:20251020100000+02'00'", colw={3: [160, 140, 170]})


def build_all(W, A, target):
    os.makedirs(target, exist_ok=True)
    rng = random.Random(P.SEED * 10 + 5)
    n = {}
    n["dispensings"] = write_dispensings(W, A, os.path.join(target, FILES["dispensings"]))
    n["products"] = write_products(W, os.path.join(target, FILES["products"]))
    n["ddd"] = write_ddd(os.path.join(target, FILES["ddd"]))
    n["practices"] = write_practices(os.path.join(target, FILES["practices"]), rng)
    n["pharmacies"] = write_pharmacies(os.path.join(target, FILES["pharmacies"]))
    write_programme(os.path.join(target, FILES["programme"]))
    write_agreement(os.path.join(target, FILES["agreement"]))
    n["conversations"] = write_conversations(A, os.path.join(target, FILES["conversations"]))
    write_statements(A, os.path.join(target, FILES["statements"]))
    write_distractors(W, target, rng)
    stamp = STAMP.timestamp()
    for fn in os.listdir(target):
        os.utime(os.path.join(target, fn), (stamp, stamp))
    return n
