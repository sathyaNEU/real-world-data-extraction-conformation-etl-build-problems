"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
WORDS = {9: "nine", 10: "ten", 8: "eight", 11: "eleven", 3: "three", 4: "four", 12: "twelve"}


def c(n):
    return format(n, ",")


def usd(x):
    return "USD {:,.2f}".format(x)


def joined(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def short(k):
    return k.split()[0]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    P, order, s, k_ = f["practices"], f["order"], f["steps"], f["constants"]
    enter, stay = f["call"]["enter"], f["call"]["stay"]
    late = [k for k in enter if k not in s["default_enter"]]
    pooled_extra = [k for k in s["pooled_enter"] if k not in enter]
    out = ["## Tags", "",
           "**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics (a clinically "
           "integrated network's 2027 two-sided risk elections for its thirteen primary care practices, conformed from "
           "three commercial payers' claim, coverage and attribution feeds in three layouts, the network's clinician "
           "roster and master patient index, its performance standard and the payers' care coordination remittances).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**Enter %s in the 2027 two-sided track and keep %s one-sided.**" % (
               joined([short(k) for k in enter]), joined([short(k) for k in stay])),
           "On the payers' final 2026 attribution each of the %s comes in %.1f to %.1f per cent under its threshold, its "
           "October interim measure carried to the year by its own 2025 run-out at the same cut. Not %s alone, the "
           "interim measure taken as it stands: the October runs attribute only the members whose qualifying visit has "
           "happened, and the year adds the members who visit late, with a whole year of member months and a fraction of "
           "the cost. Not %s as well, one pooled network run-out of %.3f: their members come early, or cost what the "
           "practice's other members cost." % (
               WORDS[len(enter)], s["under_min"], s["under_max"], joined([short(k) for k in s["default_enter"]]),
               joined([short(k) for k in pooled_extra]), s["pooled_runout"]), "",
           "## 2. Critical Components", "",
           "1. 2025 network measure on the payers' final 2025 runs, USD per member month: %s." % "; ".join(
               "%s **%s**" % (short(k), "{:,.2f}".format(P[k]["f2025"])) for k in order),
           "2. 2026 threshold, 98 per cent of the benchmark, the 2025 measure to the cent times %s to the cent (standard, "
           "section 3.4): %s." % (
               k_["trend"], "; ".join("%s **%s**" % (short(k), "{:,.2f}".format(P[k]["threshold"])) for k in order)), "",
           "## 3. Step-by-Step Solution", "",
           "1. Conformed the three payers' claims at their current version (Merrinlake's voided originals out, "
           "Kesselcrest's adjusted lines out and its cents in dollars, Pemberglen's latest version), member months from "
           "the coverage files, and every run's TIN to its practice through lpn_primary_care_roster_2026-10.xlsx.",
           "2. Took each practice's 2025 network measure on the payers' final 2025 runs (standard, section 3: claims "
           "first paid by 31 March 2026, each member's year capped at USD %s) and its threshold at 98 per cent of its "
           "benchmark, the measure to the cent times %s to the cent (section 3.4)." % (c(k_["cap"]), k_["trend"]),
           "3. Computed each practice's interim measure on the October runs (section 4.1, the factors in "
           "payer_completion_factors_2026-09.csv): taken as the 2026 figure it enters %s alone." % joined(
               [short(k) for k in s["default_enter"]]),
           "4. Re-ran the standard's attribution (section 2) on the 2025 professional claims at the October run's cut, "
           "qualifying services incurred by 31 August 2025 and paid by 30 September 2025, and took each practice's 2025 "
           "run-out, its 2025 measure over the January to August 2025 measure of the members so attributed: %.3f to "
           "%.3f." % (s["runout_min"], s["runout_max"]),
           "5. Carried each practice's interim measure by its own run-out: %s come in under their thresholds." % (
               WORDS[len(enter)]),
           "6. For the level 5 share, read each visit's paid level from its allowed amount against the payer's 2026 rate "
           "for its setting in payer_em_fee_schedules_2026.xlsx: Kesselcrest's reviewed 99215 visits allowed at its "
           "99214 rate are level 4, and Merrinlake's modifier-25 visits with a same-day minor procedure by the same "
           "clinician, allowed at half the rate, keep their level.",
           "7. For the fees, summed the three remittance files by the month each line covers: Pemberglen's by the month "
           "in its payment reference (PMH-CCF-TIN-YYYYMM-sequence), not its posting period, and Kesselcrest's only at "
           "the standard's USD %.2f (its USD %.2f lines are its Medicare Advantage fees)." % (k_["kbp_fee"], k_["ma_fee"]),
           "8. Entered the %s practices under their thresholds in the two-sided track for 2027." % WORDS[len(enter)],
           "", "## 4. Deliverable Answers", "",
           "### two_sided_track_elections_2027.xlsx", "",
           "1. Elections, one row per practice (2026 benchmark, threshold, election):"]
    for k in order:
        x = P[k]
        out.append("   - %s: benchmark %s, threshold %s, %s" % (k, usd(x["benchmark"]), usd(x["threshold"]),
                                                               "two-sided" if x["enters"] else "one-sided"))
    out.append("2. Share of established-patient visits January to August 2026 the payers paid at level 5, per cent:")
    for k in order:
        out.append("   - %s: %.1f" % (k, f["ask_a"][k]))
    out.append("3. Care coordination fees paid under the standard, by coverage quarter, USD:")
    for k in order:
        out.append("   - %s: Q1 %s, Q2 %s, Q3 %s" % (k, usd(f["ask_b"]["%s|Q1" % k]), usd(f["ask_b"]["%s|Q2" % k]),
                                                      usd(f["ask_b"]["%s|Q3" % k])))
    out += ["", "### practice_cost_vs_benchmark_2026.png", "",
            "1. Horizontal bar chart of each practice's projected 2026 network measure as the per cent above or below "
            "its threshold, the %s entering practices shaded apart, with each practice's October interim measure "
            "marked beside its bar." % WORDS[len(enter)]]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
