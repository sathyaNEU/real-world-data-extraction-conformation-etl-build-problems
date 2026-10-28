"""submission.md and metadata.json, drafted from figures.json; nothing typed."""
from __future__ import annotations

import json
import os

import pack as PK
import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def n(x):
    return f"{int(x):,}"


def by_grade(F, key):
    return ", ".join("grade %d %s" % (g, n(F["%s_%d" % (key, g)])) for g in P.GRADES)


def submission(F):
    L = ["## Tags", "",
         "**Domain:** Education & Learning Sciences (item response theory and test equating).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).", ""]
    L += ["## 1. Final Recommendation", "",
          "**Commission %s new items below the Approaching cut: %s.** Each workshop item's difficulty is estimated "
          "from the 2025-26 responses together with the students' abilities, with the launch items held at their 2021 "
          "values. Not the %s that a Rasch fit of each workshop item gives with every student's ability fixed at the "
          "event's reported scale score, because those scores were computed from the writing panel's ratings and "
          "return them. Not the %s the panel's ratings give, "
          "which put multi-step word problems that the students' answers place above the cut below it."
          % (n(F["call"]), ", ".join("%d for grade %d" % (F["commission_%d" % g], g) for g in P.GRADES),
             n(F["riv_reported_call"]), n(F["riv_panel_call"])), ""]
    L += ["## 2. Critical Components", "",
          "1. Items below the Approaching cut in each grade's pool once the workshop items are calibrated: %s."
          % by_grade(F, "low"),
          "2. Workshop items below the cut: %s." % by_grade(F, "wk_low"), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Took each grade's operational items from tessaline_item_bank_export_20270331.csv, the complete and "
          "incomplete events of tessaline_sessions_2025-26.csv and their scored responses in "
          "tessaline_item_responses_2025-26.parquet, dropping the unscored re-delivery rows (Corvane specification "
          "section 3): %s responses." % n(F["responses_total"]),
          "2. Held each launch item at its 2021 value, theta = (QSS - 500) / 40 (scale note section 1), and estimated "
          "the %s workshop items' difficulties by marginal maximum likelihood, the students of each window a normal "
          "population with its own mean and spread." % n(F["wk_items_total"]),
          "3. Re-estimated the launch items the same way as a check: the launch items below 452 come back within %.1f "
          "points of their values in every grade, while read against the reported scale scores they come back %.1f to "
          "%.1f points too easy." % (F["anchor_golden_max_abs"], F["anchor_reported_min_abs"], F["anchor_reported_max_abs"]),
          "4. Counted each pool's items with difficulty below the grade's Approaching cut (scale note section 3): %s."
          % by_grade(F, "low"),
          "5. Took the shortfall against Corvane's floor of %d (specification section 5): %s, %s in all."
          % (P.FLOOR, by_grade(F, "commission"), n(F["call"])),
          "6. Built the import from the bank export's operational rows and qrac_item_authoring_catalog_20270315.xlsx "
          "(specification sections 1, 2 and 4): each authored item once, under the key of its latest version, so the "
          "%d revisions Tessaline re-keyed, operational in the export under both keys, are loaded under the new key "
          "only; each item's catalog record read version by version, version 1 the full record and each later version "
          "changing only the fields its changed_fields lists, so a 2026 framework code set in the 2024 review and an "
          "enemy group set on version 1 still stand on a 2025 version that leaves them blank, and a group the 2024 "
          "review cleared (%d items) is gone; the reporting domain from the item's 2026 framework code, otherwise its "
          "2010 standard through qrac_framework_crosswalk_2010_to_2026.csv with the crosswalk's skill-tag condition; "
          "an enemy set from each group's imported items in one grade, two or more to a set."
          % (F["rekeyed_items"], F["groups_cleared"]),
          "7. Recommendation: commission %s new items below the Approaching cut, %s." % (n(F["call"]), by_grade(F, "commission")),
          ""]
    L += ["## 4. Deliverable Answers", "", "### bank_import_2027-28.csv", "",
          "1. One row per operational item under its current key, %s rows: item_key, grade, difficulty to one "
          "decimal, reporting_domain, enemy_set, interaction_type." % n(F["import_rows"]), "",
          "### pool_summary_2027-28.xlsx", "",
          "1. New items to commission by grade:"]
    for g in P.GRADES:
        L.append("   - Grade %d: %d" % (g, F["commission_%d" % g]))
    L.append("2. Imported items by grade and 2026 framework domain:")
    for g in P.GRADES:
        codes = [c for c, _ in PK.FRAMEWORK[PK.band(g)]]
        L.append("   - Grade %d: %s" % (g, ", ".join("%s %d" % (c, F["dom_%d_%s" % (g, c)]) for c in codes)))
    L.append("3. Enemy sets and the items they hold, by grade:")
    for g in P.GRADES:
        L.append("   - Grade %d: %d sets, %d items" % (g, F["enemy_sets_%d" % g], F["enemy_items_%d" % g]))
    L += ["", "### low_band_commission_memo.docx", "",
          "1. The commission: %s new items below the Approaching cut, %s." % (n(F["call"]), by_grade(F, "commission")),
          "2. One chart: bars of each grade's items below the Approaching cut against the floor line at %d, each bar "
          "labelled with its count and the items to commission." % P.FLOOR, ""]
    return "\n".join(L)


def metadata(F, nrows):
    covers = {
        "bank": "every item in Tessaline's bank for the consortium at close-out, with its operational difficulty and basis",
        "events": "every 2025-26 test event, grades 3 to 8, three windows",
        "responses": "every item delivery in the 2025-26 test events",
        "stats": "Tessaline's item statistics by window, 2025-26",
        "catalog": "the consortium's authoring catalog, one row per authored version",
        "crosswalk": "the consortium's crosswalk from the 2010 standards to its 2026 framework domains",
        "panel": "the writing panels' ratings of the 2024 and 2025 workshop items",
        "roster": "the consortium's student roster for 2025-26 with Tessaline student keys",
        "scale_note": "the consortium's note on the Quarrystone scale and cut scores",
        "corvane_spec": "Corvane's item pool import specification, version 3.2",
        "payments": "stipends and mileage paid to workshop writers, 2024 and 2025",
        "incidents": "Tessaline platform incidents during 2025-26",
    }
    files, fmt = [], set()
    for k, name in PK.FILES.items():
        ext = name.rsplit(".", 1)[1]
        fmt.add(ext)
        files.append(dict(file=name, format=ext, rows=nrows.get(name), covers=covers[k],
                          made="constructed by task488/generator/build.py (seeded, deterministic)"))
    big = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    return {
        "task": "task488",
        "title": "How many new items below the Approaching cut a regional assessment consortium must commission for "
                 "each grade's adaptive pool when it moves its interim from one platform to another",
        "domain": "Education & Learning Sciences", "client_domain": "education-learning-sciences",
        "subdomain": "item-response-theory-test-equating (calibrating workshop items run on provisional ratings in an "
                     "adaptive interim onto the launch scale)",
        "objective": "Data Extraction & Conformation (ETL)",
        "prompt_shape": "a count of items to commission for each of six grades; the conformed import file; per grade "
                        "the imported items in each framework domain and the enemy sets with their items; a board "
                        "memo with one chart",
        "as_of": "2027-04-02",
        "deliverables": ["bank_import_2027-28.csv", "pool_summary_2027-28.xlsx", "low_band_commission_memo.docx"],
        "distractor_files": [PK.FILES["payments"], PK.FILES["incidents"], PK.FILES["panel"]],
        "distractors": [
            {"file": PK.FILES["payments"], "wrong_basis": False,
             "why_relevant": "what the workshop paid per accepted item looks like the cost side of the commission",
             "why_unused": "the commission is a count of items, set by the floor and the pool", "ruled_out_by":
                 "Corvane specification section 5"},
            {"file": PK.FILES["incidents"], "wrong_basis": False,
             "why_relevant": "interrupted sessions look like a reason to drop or weight responses",
             "why_unused": "an interrupted session's re-delivery row is unscored and the scored row stands",
             "ruled_out_by": "the response file's own unscored re-delivery rows"},
            {"file": PK.FILES["panel"], "wrong_basis": False,
             "why_relevant": "each workshop item's ratings by the panel that set its provisional difficulty",
             "why_unused": "the panel's mean is already the bank's operational value, and the answer estimates the "
                           "difficulty from the responses", "ruled_out_by": "the bank export's difficulty_basis column"},
        ],
        "stated_inputs": [str(P.FLOOR), "July", "2026", "2025-26"],
        "input_gates": {"files": len(files), "formats": sorted(fmt), "largest_file": big["file"],
                        "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task488/generator/build.py (seeded, deterministic) around "
                               "a fictional regional assessment consortium of eleven Wisconsin school districts "
                               "(Quarrystone Regional Assessment Consortium), a fictional delivery vendor (Tessaline "
                               "Learning Systems) and a fictional new platform (Corvane Assessment); districts and "
                               "students are invented and identified by code only.",
                     "date": "2027-04-02", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-28", "generator": "task488/generator/build.py", "files": files,
    }


def write(F, nrows):
    with open(os.path.join(TASK, "submission.md"), "w") as f:
        f.write(submission(F))
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(F, nrows), f, indent=1)
        f.write("\n")
