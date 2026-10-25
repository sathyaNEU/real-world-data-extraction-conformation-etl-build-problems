"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def usd(x):
    return "USD {:,.2f}".format(x)


def joined(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def short(k):
    return k.split()[0]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    k_, par = f["constants"], f["parameters"]
    order, steps = k_["order"], par["steps"]
    enter, stay = f["call"]["enter"], f["call"]["stay"]
    held = dict(steps["held"])
    hp = sorted(held, key=lambda k: order.index(k))
    dflt, runout = steps["default_enter"], steps["runout_enter"]
    out = ["## Tags", "",
           "**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics (a clinically "
           "integrated network's 2027 two-sided risk elections for its thirteen primary care practices, conformed from "
           "three commercial payers' claim, coverage and attribution feeds in three layouts, the network's clinician "
           "roster and master patient index, its performance standard and the payers' E&M fee schedules).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**Enter %s in the 2027 two-sided track and keep %s one-sided.**" % (
               joined([short(k) for k in enter]), joined([short(k) for k in stay])),
           "%s come in over their thresholds once the %s members still in hospital on 31 August 2026, each already past "
           "the USD %s cap, are carried at it. Not %s alone, the interim measure as it stands: the October runs attribute "
           "only the members whose qualifying visit has been paid. Not %s as well, the interim measure carried by each "
           "practice's own 2025 run-out alone: a hospital bills a stay when it ends, so neither the completion factors "
           "nor the run-out carries a stay still running at the cut." % (
               joined([short(k) for k in hp]), WORDS[sum(held.values())], "{:,}".format(k_["cap"]),
               joined([short(k) for k in dflt]), joined([short(k) for k in runout if k not in enter])), "",
           "## 2. Critical Components", "",
           "1. Members in a hospital stay still running on 31 August 2026 and already past the USD %s cap: **%s**, %s." % (
               "{:,}".format(k_["cap"]), WORDS[sum(held.values())],
               " and ".join("%s at %s" % (WORDS[held[k]], k) for k in hp)),
           "2. 2026 thresholds, 98 per cent of the benchmark: %s." % " and ".join(
               "%s **%s**" % (short(k), usd(par["threshold"][k])) for k in hp), "",
           "## 3. Step-by-Step Solution", "",
           "1. Conformed the three payers' claims at their current version (Merrinlake's voided originals out, "
           "Kesselcrest's superseded claims (status A) out and its cents in dollars, Pemberglen's latest version), member months from "
           "the coverage files, and every run's TIN to its practice through lpn_primary_care_roster_2026-10.xlsx.",
           "2. Took each practice's 2025 network measure on the payers' final 2025 runs (standard, section 3: claims "
           "first paid by 31 March 2026, each member's year capped at USD %s) and its threshold at %d per cent of its "
           "benchmark, the measure to the cent times %s to the cent (section 3.4)." % (
               "{:,}".format(k_["cap"]), k_["threshold_share"], k_["trend"]),
           "3. Computed each practice's interim measure on the October runs (section 4.1, the factors in "
           "payer_completion_factors_2026-09.csv): taken as the 2026 figure it enters %s alone." % joined(
               [short(k) for k in dflt]),
           "4. Re-ran the standard's attribution (section 2) on the 2025 professional claims at the October run's cut, "
           "qualifying services incurred by 31 August 2025 and paid by 30 September 2025, and carried each practice's "
           "interim measure by its 2025 measure over the January to August 2025 measure of the members so attributed "
           "(no long stay was running at the 2025 cut): %s practices come in under." % WORDS[len(runout)],
           "5. Found the members in a stay still running at the cut (their attending physicians' daily inpatient visits "
           "run to the cut with no facility claim in the October feeds): at the lowest per-day amount any closed stay of "
           "a month or more of the same kind was allowed, %s had passed the USD %s cap; carried at the cap with each "
           "one's months of coverage in the year, %s come in over their thresholds." % (
               WORDS[sum(held.values())], "{:,}".format(k_["cap"]), joined([short(k) for k in hp])),
           "6. For the level 5 share, read each visit's paid level from its claim's allowed amount, every line of the claim "
           "counted, against the payer's 2026 rate for its setting in payer_em_fee_schedules_2026.xlsx: a Kesselcrest %s "
           "claim whose line with no procedure code takes it down to Kesselcrest's %s rate is level 4, and a Merrinlake "
           "E&M billed with modifier 25 beside a minor procedure by the same clinician that day is at the level whose rate "
           "is twice its allowed amount (a halved %s equals Merrinlake's %s rate), a modifier 25 visit beside a preventive "
           "visit at its own rate." % (k_["codes"][3], k_["codes"][2], k_["codes"][3], k_["codes"][1]),
           "7. Entered the %s practices under their thresholds in the two-sided track for 2027." % WORDS[len(enter)],
           "", "## 4. Deliverable Answers", "",
           "### two_sided_track_elections_2027.xlsx", "",
           "1. Elections, one row per practice:"]
    for k in order:
        out.append("   - %s: %s" % (k, "two-sided" if k in enter else "one-sided"))
    out.append("2. Share of established-patient visits January to August 2026 the payers paid at level 5, per cent:")
    for k in order:
        out.append("   - %s: %.1f" % (k, f["ask_a"][k]))
    out += ["", "### practice_cost_vs_benchmark_2026.png", "",
            "1. Horizontal bar chart of each practice's projected 2026 network measure against its threshold: the %s "
            "entering practices' bars fall below the threshold line and the %s one-sided practices' bars above it." % (
                WORDS[len(enter)], WORDS.get(len(stay), str(len(stay))))]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
