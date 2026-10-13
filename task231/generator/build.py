"""Write the pack under target/: the simulated panel through the records layer, then the documents and the manifest."""
import csv
import json
import os
import shutil

import docs
import params as P
import records
import sim
import world as W

FILES = {
    "standard": "BCS_fieldwork_quality_standard_v3.pdf",
    "calendar": "BCS_round_calendar.xlsx",
    "panel": "bcs_panel_register.csv",
    "outcomes": "bcs_round_outcomes_2017_2026.csv",
    "invitations": "bcs_invitations_2026_09.csv",
    "returns": "bcs_returns_2026_09.csv",
    "closures": "brevland_business_register_closures.csv",
    "register_notes": "business_register_extract_notes.pdf",
    "calls": "contact_centre_calls_2022_2026.csv",
    "codes": "contact_centre_outcome_codes.xlsx",
    "review": "bcs_region_review_2023.csv",
    "dictionary": "BCS_data_dictionary.xlsx",
    "balances": "BCS_regional_balances_2026_06.xlsx",
    "questionnaire": "BCS_questionnaire_2026.pdf",
    "manifest": "export_manifest.json",
}
DISTRACTORS = ["balances", "questionnaire"]
EXTRACTED = {
    "panel": ("Panel register (survey management system)", "2026-09-25T15:20:41Z", W.PEOPLE["analyst"]),
    "outcomes": ("Survey database, round outcomes table", "2026-09-25T15:24:09Z", W.PEOPLE["analyst"]),
    "invitations": ("Fieldwork system, invitation run of 1 September 2026", "2026-09-25T15:21:37Z", W.PEOPLE["analyst"]),
    "returns": ("Fieldwork system, receipts log", "2026-09-25T15:00:02Z", W.PEOPLE["analyst"]),
    "closures": ("Brevland Business Register, closure extract for the bank", "2026-09-25T21:47:00Z", "Brevland Business Register"),
    "calls": ("Contact centre system, call records", "2026-09-25T15:02:18Z", W.PEOPLE["cc"]),
    "review": ("Regional review 2023, code table", "2023-04-03T08:10:00Z", W.PEOPLE["analyst"]),
}
DOCUMENTS = {
    "standard": ("2026-07-06", W.PEOPLE["head"]),
    "calendar": ("2026-09-14", W.PEOPLE["analyst"]),
    "register_notes": ("2026-09-25", "Brevland Business Register"),
    "codes": ("2022-03-02", W.PEOPLE["cc"]),
    "dictionary": ("2026-09-25", W.PEOPLE["analyst"]),
    "balances": ("2026-07-30", W.PEOPLE["analyst"]),
    "questionnaire": ("2026-02-10", W.PEOPLE["head"]),
}
DESCRIBE = {
    "standard": "BCS fieldwork quality standard, version 3.0",
    "calendar": "BCS round calendar, March 2017 to December 2026",
    "panel": "Every firm recruited to the BCS panel since 2014",
    "outcomes": "Outcome of every invited firm, rounds March 2017 to June 2026",
    "invitations": "Firms invited to the September 2026 round",
    "returns": "Returns logged for the September 2026 round up to the main close",
    "closures": "Business register closure records for the panel's company numbers, as at 25 September 2026",
    "register_notes": "The register's notes on its closure extract",
    "calls": "Contact centre call records, March 2022 to the September 2026 main close",
    "codes": "Contact centre outcome codes, both schemes",
    "review": "Region codes before and after the 2023 regional review",
    "dictionary": "Data dictionary for these files",
    "balances": "Published net balances, June 2026 round",
    "questionnaire": "BCS questionnaire 2026",
}


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def review_rows():
    rows = []
    for code in sorted(W.REGS, key=lambda c: W.OLD_CODE[c]):
        rows.append([W.OLD_CODE[code], W.OLD_NAME[code], code, W.NAME[code], W.REVIEW_EFFECTIVE.isoformat()])
    return ["old_code", "old_name", "new_code", "new_name", "effective_from"], rows


def build(target, pan=None, rec=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    pan = pan or sim.Panel().run()
    rec = rec or records.Records(pan)
    p = lambda k: os.path.join(target, FILES[k])
    counts = {}
    counts["panel"] = write_csv(p("panel"), *rec.panel_register())
    counts["outcomes"] = write_csv(p("outcomes"), *rec.outcomes())
    counts["invitations"] = write_csv(p("invitations"), *rec.invitations())
    counts["returns"] = write_csv(p("returns"), *rec.returns_sep())
    counts["closures"] = write_csv(p("closures"), *rec.closures())
    counts["calls"] = write_csv(p("calls"), *rec.calls_table())
    counts["review"] = write_csv(p("review"), *review_rows())
    docs.standard(p("standard"))
    docs.register_notes(p("register_notes"))
    docs.questionnaire(p("questionnaire"))
    docs.calendar(p("calendar"))
    docs.codebook(p("codes"))
    docs.dictionary(p("dictionary"))
    docs.balances(p("balances"))
    man = []
    for k, f in FILES.items():
        if k == "manifest":
            continue
        if k in EXTRACTED:
            sysname, when, owner = EXTRACTED[k]
            man.append({"file": f, "description": DESCRIBE[k], "source": sysname, "extracted_at": when,
                        "rows": counts.get(k), "owner": owner})
        else:
            issued, owner = DOCUMENTS[k]
            man.append({"file": f, "description": DESCRIBE[k], "issued": issued, "owner": owner})
    with open(p("manifest"), "w", encoding="utf-8") as fh:
        json.dump({"package": "BCS September 2026 round: fieldwork files at the main close",
                   "prepared_by": W.UNIT, "prepared_at": "2026-09-25T21:58:00Z", "files": man}, fh, indent=2,
                  ensure_ascii=False)
        fh.write("\n")
    return pan, rec, counts
