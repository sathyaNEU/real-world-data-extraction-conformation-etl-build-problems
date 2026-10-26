"""submission.md from generator/figures.json: the five blocks, every figure emitted from the generator's own
numbers."""
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402


def f1(x):
    return "%.1f" % x


def mname(k):
    y, m = k.split("-")
    return dt.date(int(y), int(m), 1).strftime("%B %Y")


def text(fig):
    r, cp, s = fig["rates"], fig["components"], fig["steps"]
    A, B, C = (fig["asks"]["A"]["p90_processing_s"], fig["asks"]["B"]["median_first_compression_s"],
               fig["asks"]["C"]["answered_within_15s_pct"])
    out = ["## Tags", "",
           "**Domain:** Human Factors & Ergonomics (workload, fatigue and shift analysis).",
           "**Analytical objective:** Root-Cause Analysis.", "",
           "## 1. Final Recommendation", "",
           "**The rise in under-triaged medical calls came from quick returns, shifts begun less than eleven hours "
           "after the call-taker's previous shift ended, which the rotation worked from 2 March 2026 brought in.**",
           "From March 2026, %s per cent of the critical or emergent calls taken on those shifts were sent cold, "
           "against %s per cent on rested shifts, which ran at %s per cent before March. Not protocol release 13.3, "
           "which the rested shifts ran on too while they held. Not the academy graduates, since the veterans' calls "
           "rose from %s to %s per cent. Not the call mix, since the March to August rate at the earlier mix is %s "
           "per cent." % (f1(cp["from_march_on_quick_return_shifts"]), f1(cp["from_march_on_rested_shifts"]),
                          f1(cp["rested_shifts_before"]), f1(s["veterans"][0]), f1(s["veterans"][1]),
                          f1(s["standardised_from_march"])), "",
           "## 2. Critical Components", "",
           "1. The under-triage rate was **%s%%** from September 2025 to February 2026 and **%s%%** from March to "
           "August 2026." % (f1(r["before"]), f1(r["from_march"])),
           "2. Shifts begun less than eleven hours after the call-taker's previous shift ended were **%s%%** of the "
           "shifts worked from September 2025 to February 2026 and **%s%%** of those worked from March to August "
           "2026." % (f1(cp["quick_return_share_before"]), f1(cp["quick_return_share_from_march"])),
           "3. From March the under-triage rate was **%s%%** on those shifts and **%s%%** on rested shifts." %
           (f1(cp["from_march_on_quick_return_shifts"]), f1(cp["from_march_on_rested_shifts"])),
           "4. On rested shifts the rate was **%s%%** before March." % f1(cp["rested_shifts_before"]), "",
           "## 3. Step-by-Step Solution", "",
           "1. Matched each call in cad_medical_calls_2025_2026.csv to its records in "
           "epcr_patient_records_2025_2026.csv by incident number (the tablets drop the dash), each call at its most "
           "acute patient (QA program 2.2): the under-triage rate was %s per cent before March and %s from March." %
           (f1(r["before"]), f1(r["from_march"])),
           "2. Placed each call on the shift worked in roster_shifts_worked_2025_2026.csv whose start and end hold its "
           "answer time, the CAD login joined to the employee number through call_takers.csv, and took each shift's "
           "rest from the end of the call-taker's previous shift worked (the extract starts on 18 August 2025): shifts "
           "begun under eleven hours after it were %s per cent of those from September 2025 to February 2026 and %s "
           "of those from March to August 2026." % (f1(cp["quick_return_share_before"]),
                                                    f1(cp["quick_return_share_from_march"])),
           "3. Set the other changes against the rested shifts and the calls: on rested shifts, which ran on release "
           "13.3 from 3 March, the rate was %s per cent before March and %s from March; the veterans' calls rose from "
           "%s to %s per cent, and at the earlier protocol mix the March to August rate is %s." %
           (f1(cp["rested_shifts_before"]), f1(cp["from_march_on_rested_shifts"]), f1(s["veterans"][0]),
            f1(s["veterans"][1]), f1(s["standardised_from_march"])),
           "4. Ask A: took each medical call in cad_medical_calls_2025_2026.csv once (a split CAD incident repeats its "
           "call's che_call_id, answer second and call-taker), its processing time from the answer to the earliest "
           "assignment in cad_unit_history_2025_2026.csv among its incidents (unit_assigned holds the ambulance now on "
           "the incident), and each month's 90th percentile at rank 0.9 times the calls, rounded up (QA program 3).",
           "5. Ask B: took each arrest's primary review in tcpr_arrest_reviews_2025_2026.csv where compressions were "
           "coached, reading reviewer QA7's times as minutes and seconds keyed without the colon (QA7's calibrated "
           "calls agree with the other reviewer only when so read), the first compression at "
           "recording_started plus those seconds, less the CAD's call_answered, and each month's median (QA program 5).",
           "6. Ask C: took the calls in che_call_detail_2025_2026.csv on the 911 trunk groups of centre_reference.xlsx "
           "(TG01, TG02, TG03 and TG05, not the 10-digit lines on TG07), leaving out the record of a call passed from "
           "one position to another (it arrives the second an earlier record on the same trunk group from the same "
           "number was released), answered and not abandoned, and each month's share answered 15 seconds or less "
           "after arriving, by the month answered in local time (QA program 4).",
           "7. Named the cause: from March the calls on quick-return shifts were sent cold at %s per cent against %s "
           "on rested shifts, so the rise came from the quick returns." %
           (f1(cp["from_march_on_quick_return_shifts"]), f1(cp["from_march_on_rested_shifts"])), "",
           "## 4. Deliverable Answers", "", "### %s" % K.GOLDEN, "",
           "1. Cause: quick returns, shifts begun less than eleven hours after the call-taker's previous shift ended "
           "(the rotation worked from 2 March 2026), not protocol release 13.3.",
           "2. Under-triage rate: September 2025 to February 2026 %s%%; March to August 2026 %s%%." %
           (f1(r["before"]), f1(r["from_march"])),
           "3. 90th percentile call processing time, medical calls, seconds:"]
    for k in sorted(A):
        out.append("   - %s: %d" % (mname(k), A[k]))
    out.append("4. Median time to first compression, cardiac arrest calls, seconds:")
    for k in sorted(B):
        out.append("   - %s: %d" % (mname(k), B[k]))
    out.append("5. 911 calls answered within 15 seconds, per cent:")
    for k in sorted(C):
        out.append("   - %s: %s" % (mname(k), f1(C[k])))
    out += ["", "### %s" % K.CHART, "",
            "1. Line chart of each month's under-triage rate, September 2025 to August 2026, the rate stepping up "
            "from March 2026.", ""]
    return "\n".join(out)


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    with open(os.path.join(task, "submission.md"), "w", encoding="utf-8") as f:
        f.write(text(fig))
    print("submission.md written")
