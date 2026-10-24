"""submission.md, every figure read from generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import records as R   # noqa: E402
import world as W     # noqa: E402
import goldwb as GW   # noqa: E402


def usd(v):
    return "USD {:,.0f}".format(v)


def n(v):
    return "{:,}".format(v)


def write(fig_path, out_path):
    f = json.load(open(fig_path))
    order = list(W.CODES)
    name = {c: "%s (%s)" % (R.PROGRAM[c], R.CCN[c]) for c in order}
    st = f["fal_states"]
    o = ["## Tags\n",
         "**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics (a hospice "
         "organisation's EMR admissions, its acquired hospice's census register, claim lines and remittances and the "
         "Medicare hospice benefit periods extract conformed into the FY2026 aggregate cap schedule its December 2026 "
         "accrual reads).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).\n",
         "## 1. Final Recommendation\n",
         "**Accrue USD %.1f million for FY2026 Medicare hospice cap repayments, all of it at Fallowmere Hospice (provider "
         "number %s); the other seven provider numbers are under their caps.**" % (f["call"]["total_musd"],
                                                                        f["provider_numbers"]["FAL"]),
         "Fallowmere's FY2026 payments before sequestration of %s run above its aggregate cap once each beneficiary it "
         "discharged alive carries the hospice days still expected after the close. Not nothing, which taking every "
         "beneficiary discharged alive as finished gives: %s of Fallowmere's elections end in a live discharge, and the "
         "extract's later benefit periods show many of those beneficiaries electing hospice again, most at hospices "
         "outside the organisation.\n" % (usd(f["payments_usd"]["FAL"]), GW.in_words(f["history"]["alive_share"]["FAL"])),
         "## 2. Critical Components\n",
         "1. Fallowmere's FY2026 payments before sequestration are **%s**." % usd(f["payments_usd"]["FAL"]),
         "2. Fallowmere has **%s** FY2026 beneficiaries: at 31 December 2026 **%s** on service, **%s** discharged alive "
         "and not back, **%s** died." % (n(f["fal_n"]), n(st["open"]), n(st["out"]), n(st["dead"])),
         "3. Fallowmere's FY2026 repayment is **USD %.1f million**; every other provider number's is nil.\n" % f["repayment_musd"]["FAL"],
         "## 3. Step-by-Step Solution\n",
         "1. Read medicare_hospice_benefit_periods_20270105.txt (%s benefit periods, the periods sharing an election date "
         "one stay), with wendleglen_emr_admissions.csv and fallowmere_census_register_20250228.xlsx matched to MBIs "
         "through hicn_mbi_crosswalk.csv and each beneficiary's group taken from diagnosis_groups.csv: %s FY2026 "
         "beneficiaries across the eight provider numbers." % (n(f["rows"]["extract"]), n(f["cohort_n"])),
         "2. Took each beneficiary's FY2026 days at each provider number, days to 31 December 2026 in every hospice and "
         "year, and state at the close (at Fallowmere %s on service, %s discharged alive and not back, %s died)."
         % (n(st["open"]), n(st["out"]), n(st["dead"])),
         "3. Read the days expected after the close from the experience since 1 October 2016 of the provider number that "
         "cared for the beneficiary last, in the beneficiary's group (wendleglen_cap_liability_policy.docx section 2.4): "
         "for a stay still open, the further days of that provider number's stays that had run as long (Kaplan-Meier), "
         "plus the chance such a stay ends alive times the chance of a later election times the days a later election "
         "brings.",
         "4. For a beneficiary discharged alive and alive at the close, the chance of a later election at any hospice "
         "among the provider number's live discharges still alive and not back after as many days out (Aalen-Johansen on "
         "the extract's later elections and dates of death), times the days a later election brings (the Kaplan-Meier "
         "mean of those elections); a beneficiary who died has none.",
         "5. Counted each beneficiary at each provider number as its FY2026 days over the days to the close plus the "
         "expected days (section 2.3) and multiplied each provider number's count by USD 35,361.44 (section 2.1).",
         "6. Summed each provider number's FY2026 payments from remittance_register_fy2026.csv (CLP rows with reversals, "
         "adj_carc_253 added back, PLB interest left out) and took 98 per cent of any excess over the cap (section 3.2): "
         "only Fallowmere's payments exceed its cap.",
         "7. For the inpatient cap, took the version of each FY2026 claim in wendleglen_claim_lines_fy2026.csv that "
         "remittance_register_fy2026.csv shows paid and not reversed (a returned replacement was never paid, so the claim "
         "it would have replaced stands), repriced it from its dated level-of-care lines with fy2026_hospice_payment_rates.pdf, "
         "the routine care count from the extract and the wage index in provider_numbers.json, and where the payment falls "
         "short, counted its last general inpatient and respite days paid at the routine rate (the one count that closes "
         "the gap to the cent) out of the 0656 and 0655 units, over each provider number's FY2026 days of care in the "
         "extract.",
         "8. The accrual is as in the Final Recommendation.\n",
         "## 4. Deliverable Answers\n",
         "### fy2026_hospice_cap_accrual.xlsx\n",
         "1. FY2026 aggregate cap repayments to accrue, USD millions to one decimal:"]
    for c in order:
        o.append("   - %s: %.1f" % (name[c], f["repayment_musd"][c]))
    o.append("   - Total: %.1f" % f["call"]["total_musd"])
    o.append("2. FY2026 inpatient cap, general inpatient days and inpatient respite days Medicare paid for (whole days) and "
             "the inpatient share of days of care (per cent to one decimal):")
    for c in order:
        a = f["ask_a"][c]
        o.append("   - %s: general inpatient %s, respite %s, share %.1f" % (name[c], n(a["gip_days"]), n(a["respite_days"]),
                                                                          a["share_pct"]))
    o.append("3. The cap schedule: one row per FY2026 beneficiary per provider number (%s rows) with the FY2026 days there, "
             "the hospice days to the close, the days expected after it and the share counted." % n(f["schedule_rows"]))
    open(out_path, "w").write("\n".join(o) + "\n")


if __name__ == "__main__":
    write(os.path.join(HERE, "figures.json"), os.path.join(os.path.dirname(HERE), "submission.md"))
