"""Write task177/metadata.json from the built pack: what every file is and where it comes from, what is constructed,
the distractors, the input gates."""
from __future__ import annotations

import csv
import json
import os

from openpyxl import load_workbook

import common as C

ORIGIN = "Constructed for this task (seeded, deterministic): "
SOURCES = {
    C.F_ASSIGN: ("Daily Lantern Media (fictional) campaign tool, the 31 January 2026 at-risk list and each "
                 "subscription's arm in the retention test", "2026-01-31"),
    C.F_PROFILE: ("Daily Lantern Media CRM, snapshot of the subscriptions on the 31 January 2026 list", "2026-01-31"),
    C.F_LIST: ("Daily Lantern Media campaign tool, the at-risk list cut on 25 January 2027 for the 26 January send",
               "2027-01-25"),
    C.F_LBS: ("Daily Lantern Media legacy billing system, invoice line export for the subscriptions on either list and "
              "their add-ons", "2027-01-25"),
    C.F_SPINV: ("Daily Lantern Media subscriptions platform, invoice and credit note export pulled for this year's list "
                "(one row per document, its lines as JSON)", "2027-01-25"),
    C.F_XWALK: ("Daily Lantern Media Billing Operations, legacy reference to platform id crosswalk issued with the "
                "billing move note", "2027-01-25"),
    C.F_EVENTS: ("Daily Lantern Media subscription events for last January's list, from both billing systems",
                 "2027-01-25"),
    C.F_OFFERS: ("Daily Lantern Media offers engine, acceptances of the January 2026 retention offer", "2027-01-25"),
    C.F_EMAIL: ("Daily Lantern Media email platform, event log of the January 2026 offer email", "2027-01-25"),
    C.F_NOTE: ("Daily Lantern Media Billing Operations, note on monthly digital billing on the subscriptions platform, "
               "version 1.3", "2026-10-15"),
    C.F_PLAN: ("Daily Lantern Media Subscriber Retention, January 2027 retention offer plan", "2027-01-18"),
    C.F_DICT: ("Daily Lantern Media Audience Data, field descriptions for the pull", "2027-01-25"),
    C.F_SURVEY: ("Daily Lantern Media reader survey, fourth-quarter 2026 export", "2027-01-25"),
    C.F_VALID: ("Daily Lantern Media Audience Data Science, retention model 3.2 validation summary", "2026-12-09"),
}
TITLE = ("The share of a national news publisher's 26 January 2027 at-risk list of monthly digital subscribers still "
         "subscribed on 31 March 2027 because they are sent a half-price retention offer, forecast from last "
         "January's randomised test")


def _rows(path):
    ext = path.rsplit(".", 1)[-1]
    if ext == "csv":
        with open(path, encoding="utf-8", newline="") as fh:
            return sum(1 for _ in csv.reader(fh)) - 1
    if ext == "xlsx":
        wb = load_workbook(path, read_only=True)
        return sum(max(0, ws.max_row - 1) for ws in wb.worksheets)
    return None


def write(task_dir):
    target = os.path.join(task_dir, "target")
    files = []
    big, big_rows = None, 0
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        rows = _rows(p)
        if rows and rows > big_rows:
            big, big_rows = f, rows
        src, date = SOURCES[f]
        files.append(dict(path=f, format=f.rsplit(".", 1)[-1], bytes=os.path.getsize(p), rows=rows,
                          source=ORIGIN + src, date=date, license="CC0-1.0 (original work, constructed for this task)"))
    distractors = [
        dict(file=C.F_SURVEY, wrong_basis=False,
             why_relevant="readers' satisfaction and their own stated chance of cancelling in the next three months, "
                          "which looks like a way to size who on the list would go without the offer",
             why_unused="a voluntary sample of both lists' members with stated intentions, no arm and no billing; no "
                        "figure reads it",
             ruled_out_by="its own coverage (a voluntary sample) and the randomised test, which measures what the offer "
                          "keeps directly"),
        dict(file=C.F_VALID, wrong_basis=False,
             why_relevant="the retention model's calibration by risk band, which looks like the chance each list "
                          "member cancels without the offer",
             why_unused="it describes the chance of cancelling within 30 days, not what the offer changes; the test's "
                        "arms give that directly; no figure reads it",
             ruled_out_by="the test's holdout arm (the outcome without the offer, measured)"),
    ]
    meta = dict(
        task="task177", title=TITLE,
        domain="Product Analytics", client_domain="product-analytics",
        subdomain="churn propensity and uplift modelling (the effect of a retention offer on a monthly subscription, "
                  "carried from a randomised test whose deliveries fell at every point of the billing cycle to a list "
                  "whose bills all fall six days after the send)",
        objective="Forecasting & Predictive Modeling",
        prompt_shape="one forecast share to the nearest 5 per cent; last January's offer discounts on February and "
                     "March 2026 bills and its takers on each plan; this year's list billed for its plans after "
                     "credits in each month from October 2026 to January 2027 on each plan",
        as_of="2027-01-25",
        deliverables=["retention_offer_forecast_2027.xlsx", "january_offer_note.docx"],
        distractor_files=[d["file"] for d in distractors],
        distractors=distractors,
        stated_inputs=["48,000", "26 January 2027", "31 March 2027", "half price on the next two monthly bills",
                       "31 January 2026"],
        field_terms=[],
        input_gates=dict(files=len(files), formats=sorted(set(x["format"] for x in files)), largest_file=big,
                         largest_file_rows=big_rows),
        sources=[dict(files="all files under target/",
                      origin="constructed for this task by task177/generator/build.py (seeded, deterministic) around a "
                             "fictional national news publisher in the United Kingdom (Daily Lantern Media, publisher "
                             "of The Daily Lantern), its legacy billing system and its subscriptions platform. "
                             "Subscribers are identified by number only. No real organisation's records or person is "
                             "depicted.",
                      date="2027-01-25", license="CC0-1.0 (original work)")],
        created="2026-10-21", generator="task177/generator/build.py", files=files)
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
        fh.write("\n")
    return meta
