"""submission.md and metadata.json, drafted from figures.json; nothing typed."""
from __future__ import annotations

import json
import os

import figures as FG
import pack as PK
import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def n(x):
    return f"{int(x):,}"


def day(s):
    import datetime as _dt
    d = _dt.date.fromisoformat(str(s))
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def submission(F):
    L = []
    L += ["## Tags", "",
          "**Domain:** Banking, Credit & Financial Risk (credit scoring and PD modeling).",
          "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## 1. Final Recommendation", "",
          "**About %s of the pool's %s loans will be 90 or more days past due on 30 June 2027.** Each loan is read off "
          "its group: the history's six-month rate for loans whose group was paying for none, one, two or three or more "
          "members at its last meeting, applied to the pool's loans in those states, gives %.1f. Not the %s that "
          "reading each member's own payment gives, which treats every carried member as carried and every payer as "
          "safe. Not the %s that flags a group for carrying anyone, which prices a group paying for two at one meeting "
          "like a group paying for one." % (n(F["call"]), n(F["pool_loans"]), F["call_unrounded"],
                                              n(F["rival_own_posting_printed"]), n(F["rival_group_any_printed"])), ""]
    L += ["## 2. Critical Components", "",
          "1. The pool's loans by how many members their group paid for at its last meeting on or before 31 December 2026: "
          "**%s** none, **%s** one, **%s** two, **%s** three or more." % (n(F["state_loans_0"]), n(F["state_loans_1"]),
                                                                         n(F["state_loans_2"]), n(F["state_loans_3"])),
          "2. Groups paying for two or more members at that meeting: **%s**, holding **%s** of the pool's loans."
          % (n(F["state_groups_2plus"]), n(F["state_loans_2plus"])), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Joined collectpro_collections_FY2023-24.csv and collectpro_collections_FY2024-25.csv to "
          "kshetra_collections_2025-04_to_2026-12.parquet through kshetra_migration_map_20250401.csv, reading SELF and "
          "OWN as paid by the member, GS and GRP_SUPP as paid by another member of her group and NIL and NOT_PAID as "
          "unpaid (operating policy section 4): one ledger of %s instalment rows." % n(F["ledger_rows"]),
          "2. Took each loan's days past due from the due date of its oldest unpaid instalment (operating policy "
          "section 6).",
          "3. At each month end from %s to %s, took the loans current then and disbursed at least 91 days earlier, "
          "counted the instalments other members paid in the loan's group at its last meeting on or before the month "
          "end, and read the share of loans 90 or more days past due 181 days later: %.2f, %.2f, %.2f and %.2f per cent "
          "for none, one, two and three or more." % (day(F["hist_first_asof"]), day(F["hist_last_asof"]), F["state_rate_pct_0"],
                                                     F["state_rate_pct_1"], F["state_rate_pct_2"], F["state_rate_pct_3"]),
          "4. Counted the pool tape's %s loans by the same count at their group's last meeting on or before 31 December "
          "2026: %s, %s, %s and %s." % (n(F["pool_loans"]), n(F["state_loans_0"]), n(F["state_loans_1"]),
                                        n(F["state_loans_2"]), n(F["state_loans_3"])),
          "5. Multiplied each count by its rate and added: %.1f loans, %s to the nearest 100." % (F["call_unrounded"],
                                                                                            n(F["call"])),
          "6. For the guardrails, kept active JLG and MFI-IND accounts in cic_portfolio_review_PVM_20261231.csv, counted "
          "Salandi's MFI0447 and SFB0029 and Gandhamardan's BNK0102 and BNK0115 as one institution each through the "
          "successor_code and parent_code of cic_member_directory_202612.csv (CPN-MF-07 section 3), and counted a loan once where SFB0014 reports the "
          "same opening date and sanctioned amount under two account numbers, taking the report later than %s: %s "
          "borrowers in breach, INR %.1f lakh of pool principal." % (day(F["ask_stale_report_date"]),
                                                                    n(F["ask_breach_total"]), F["ask_lakh_total"]),
          "7. Recommendation: about %s loans 90 or more days past due on 30 June 2027." % n(F["call"]), ""]
    L += ["## 4. Deliverable Answers", "", "### pool_90dpd_forecast.xlsx", "",
          "1. Forecast: %s loans 90 or more days past due on 30 June 2027." % n(F["call"]),
          "2. Borrowers in breach of the microfinance guardrails on the bureau at the cut-off, and the pool principal "
          "outstanding on their loans (INR lakh), by branch:"]
    for b in FG.BRANCH_ORDER:
        L.append("   - %s %s: %s borrowers, INR %.1f lakh" % (b, FG.BRANCH_NAME[b], n(F["ask_breach_%s" % b]),
                                                           F["ask_lakh_%s" % b]))
    L += ["", "### pool_purchase_note.docx", "",
          "1. The forecast: about %s of the pool's %s loans 90 or more days past due on 30 June 2027." % (
              n(F["call"]), n(F["pool_loans"])),
          "2. One chart: horizontal bars of the expected loans 90 or more days past due by how many members the group "
          "paid for at its last meeting on or before the cut-off, each state labelled with its pool loan count.", ""]
    return "\n".join(L)


def metadata(F, nrows):
    files = []
    fmt = {}
    covers = {
        "pool_tape": "the loans offered in Pool PVM/2026-12 at the cut-off, one row per loan",
        "kshetra": "every instalment due at a centre meeting from April 2025 to the cut-off, as Kshetra recorded it",
        "collectpro_a": "every instalment due at a centre meeting, July 2023 to March 2024, as CollectPro exported it",
        "collectpro_b": "every instalment due at a centre meeting, April 2024 to March 2025, as CollectPro exported it",
        "migmap": "CollectPro identifiers of members, loans and groups and their Kshetra identifiers from 1 April 2025",
        "kyc": "KYC of the pool's borrowers: bureau reference, enrolment date, village, gram panchayat and block as "
               "recorded at enrolment",
        "centre_master": "the assignor's centres: codes on both platforms, branch, village, meeting day, field officer",
        "cic": "the credit bureau's portfolio review of the pool's borrowers at the cut-off, one row per account",
        "cic_directory": "the bureau's member directory for the lenders in the review",
        "policy": "the assignor's JLG operating policy, version 6.1",
        "term_sheet": "the bank's indicative term sheet for the pool",
        "guardrails": "the bank's credit policy note on microfinance guardrails",
        "field_update": "the assignor's field update to lenders after the October 2026 cyclone",
        "portfolio": "the assignor's monthly branch portfolio report, April 2024 to December 2026",
        "claims": "credit-life claims on members' deaths, 2023 to 2026",
        "postings": "field officers' postings in 2026",
    }
    for key, name in PK.FILES.items():
        ext = name.rsplit(".", 1)[1]
        fmt[ext] = 1
        files.append(dict(file=name, format=ext, rows=nrows.get(name), covers=covers[key],
                          made="constructed by task177/generator/build.py (seeded, deterministic)"))
    big = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    return {
        "task": "task177",
        "title": "How many of the microloans in a pool an Odisha NBFC-MFI offers a bank, every loan current at the "
                 "31 December 2026 cut-off ten weeks after a cyclone, will be 90 or more days past due on 30 June 2027",
        "domain": "Banking, Credit & Financial Risk",
        "client_domain": "banking-credit-financial-risk",
        "subdomain": "credit-scoring-pd-modeling (six-month default of joint-liability group microloans in a "
                     "direct-assignment pool)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "one forecast count to the nearest 100 loans; for each of the fourteen branches the pool "
                        "borrowers in breach of the bank's microfinance guardrails on the bureau and the pool principal "
                        "outstanding on their loans in INR lakh; a purchase note with one chart",
        "as_of": "2027-01-08",
        "deliverables": ["pool_90dpd_forecast.xlsx", "pool_purchase_note.docx"],
        "distractor_files": [PK.FILES["claims"], PK.FILES["postings"], PK.FILES["portfolio"]],
        "distractors": [
            {"file": PK.FILES["claims"], "wrong_basis": False,
             "why_relevant": "deaths close members' loans through the credit-life cover, which looks like it should come "
                             "off a default forecast or out of the pool",
             "why_unused": "the pool tape holds live borrowers' current loans at the cut-off; a claim settles a loan "
                           "that is no longer in the pool, and no figure reads the register",
             "ruled_out_by": "the term sheet's clause 3 (the pool is the pool tape)"},
            {"file": PK.FILES["postings"], "wrong_basis": False,
             "why_relevant": "field officer coverage and moves look like a driver of collections in the cyclone months",
             "why_unused": "no figure reads a field officer; the forecast reads each group's own meetings",
             "ruled_out_by": "the ledger, which records every instalment at the meeting it fell due"},
            {"file": PK.FILES["portfolio"], "wrong_basis": False,
             "why_relevant": "the assignor's own PAR and collection efficiency by branch and month, which look like the "
                             "pool's track record",
             "why_unused": "branch-level metrics cannot show which loans are current because co-members paid for "
                           "them; the forecast reads the ledger at the group and meeting",
             "ruled_out_by": "the operating policy's section 6 (collection efficiency counts every instalment collected "
                             "at the meeting) and the ledger's GRP_SUPP and GS rows"},
        ],
        "stated_inputs": ["31 December 2026", "30 June 2027", "90 or more days past due", "fourteen branches", "12,880",
                          "INR 2,00,000"],
        "input_gates": {"files": len(files), "formats": sorted(fmt), "largest_file": big["file"],
                        "largest_file_rows": big["rows"]},
        "sources": [{
            "files": "all files under target/",
            "origin": "constructed for this task by task177/generator/build.py (seeded, deterministic) around a "
                      "fictional NBFC-MFI (Prachi Valley Microfinance Pvt Ltd), a fictional bank (Tamralipta Bank Ltd), "
                      "fictional lenders on a fictional credit bureau's report and a fictional October 2026 cyclone, "
                      "set in real Odisha districts and blocks; villages and gram panchayats are invented names. "
                      "Members are identified by number only. No real organisation's records or person is depicted.",
            "date": "2027-01-08",
            "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-28",
        "generator": "task177/generator/build.py",
        "files": files,
    }


def write(F, nrows):
    with open(os.path.join(TASK, "submission.md"), "w") as f:
        f.write(submission(F))
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(metadata(F, nrows), f, indent=1)
        f.write("\n")
