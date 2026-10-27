"""task157 (architecture 2) metadata.json: per file its source, date, licence, what it covers and how it
was made, beside the declared distractors and the portal's keys. It sits in the task folder, never under
target/, because nothing under target/ describes the pack."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402
import deliver as DL    # noqa: E402
import docs as DOC      # noqa: E402
import records as R     # noqa: E402

LIC = "Constructed for this task from Arizona's own statutory scheme; no third-party material. CC0-1.0."
OFFICE = "%s, %s" % (K.OFFICE, K.DIVISION)

FILES = [
    (R.F_RETURNS, OFFICE, "2028-08-03", "The fifteen county recorders' verification returns for the "
     "statutory sample of initiative serial I-18-2028, consolidated by the division's load, one row per "
     "sampled signature line. Each recorder's own date format and Navajo County's own 2019 disposition "
     "codes are kept as received."),
    (R.F_CORR, OFFICE, "2028-08-03", "Query notices the division raised on the returns and the recorders' "
     "re-determinations, one row per line re-determined."),
    (R.F_SNAP_EARLY, OFFICE, "2027-12-20", "Registration records for the identifiers the sample transmittal "
     "cites, taken from the archived statewide voter file snapshot of 20 December 2027, the last snapshot "
     "before circulation opened."),
    (R.F_SNAP_LATE, OFFICE, "2028-07-10", "The same registration records taken from the statewide voter "
     "file snapshot of 10 July 2028."),
    (R.F_SHEETS, OFFICE, "2028-07-07", "The office's register of the petition sheets it receipted, one row "
     "per sheet, with the receipt bundle, the circulator's registration number, the firm's own sheet "
     "number and the signature lines the sheet carries."),
    (R.F_RECEIPT, OFFICE, "2028-07-07", "The office's receipt log for the filing, one row per bundle "
     "presented, with the sheets accepted, the sheets struck at receipt and the signature lines accepted."),
    (R.F_MANIFEST, "Petition circulator firms, filed with the office", "2028-07-07", "Each circulator "
     "firm's own delivery manifest for the bundles it handed over, carrying the firm's own sheet and "
     "signature counts and the trading name it filed under."),
    (R.F_CIRC, OFFICE, "2028-07-11", "The office's extract of the paid circulators registered to gather "
     "signatures for serial I-18-2028, by registration number, with the firm that registered each and the "
     "dates each registration ran from and, where the circulator registered again under another firm, to."),
    (R.F_MAINT, OFFICE, "2028-03-14", "The register of the statewide list-maintenance run of 14 March 2028: "
     "the registrations it cancelled and the registrations it moved to inactive."),
    (R.F_CLOSEOUT, OFFICE, "2024-08-29", "The office's close-out of the full count of initiative serial "
     "I-04-2024, ordered by the Superior Court, with the examination's dates, examiners and per-county "
     "figures. The only settled measure the office holds of what examining a petition line by line takes."),
    (DOC.F_RECORD, OFFICE, "2028-07-11", "The office's filing and sample record for serial I-18-2028: the "
     "filing, the receipt, the number required, the sample drawn and the statutory determination."),
    (DOC.F_INSTRUCTION, OFFICE, "2027-11-18", "The signature verification instruction the county recorders "
     "work to, with the current disposition code set and the order the grounds are applied in."),
    (DOC.F_OLDCODES, "Navajo County Recorder", "2019-04-15", "Navajo County's own disposition code list, "
     "which that recorder has not reissued and still files on."),
    (R.F_OTHER, OFFICE, "2028-07-05", "The office's receipt log for initiative serial I-04-2028, a second "
     "measure filed in the same cycle."),
    (R.F_REGSTATS, OFFICE, "2028-07-01", "The office's published registration report of 1 July 2028, active "
     "and inactive registrations by county and party."),
]

DISTRACTORS = [R.F_OTHER, R.F_REGSTATS]


def write(task_dir, n):
    target = os.path.join(task_dir, "target")
    present = sorted(os.listdir(target))
    listed = [f for f, _, _, _ in FILES]
    assert sorted(listed) == present, (sorted(set(listed) ^ set(present)),)
    doc = {
        "task": "task157",
        "world": "The Arizona Secretary of State's elections division projects, from the statutory five per "
                 "cent random sample, how many of the 540,000 signature lines filed for initiative serial "
                 "I-18-2028 a full count would find valid, and whether the petition qualifies, goes to a "
                 "full count or fails.",
        "as_of": K.iso(K.AS_OF),
        "domain": "political-science-public-policy / election-polling-forecasting",
        "objective": "Forecasting & Predictive Modeling",
        "deliverables": [DL.G_BOOK, DL.G_CHART],
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["365,678", "404,170", "384,924", "540,000", "27,000", "38,080", "38,320",
                          "2,566,154", "365678", "404170", "384924", "540000"],
        "field_terms": ["sample", "sampled", "sampling", "signature", "signatures"],
        "official_decoy": False,
        "validated_decoy": False,
        "calibration_corpus": R.F_CLOSEOUT,
        "files": [
            {"file": f, "source": src, "date": date, "licence": LIC, "covers": covers,
             "rows": n.get(f), "made": "Written by task157/generator from the generator's clean truth; no "
                                       "third-party data."}
            for f, src, date, covers in FILES
        ],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=1)
        fh.write("\n")
