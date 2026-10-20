"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W

WORD = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 9: "nine"}
CLS = {"ssn": "Social Security number on file", "simple": "no number, single surname",
       "compound": "no number, two-part surname"}


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def money(v):
    return "${:,}".format(v)


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    hs = {r["short"]: r for r in f["hospitals"]}
    lose = [hs[s] for s in f["lose"]]
    keep = [r for r in f["hospitals"] if r["verdict"] == "keeps"]
    top_keep = max(keep, key=lambda r: r["ratio"])
    rt = f["rates"]
    reflex_extra = [s for s in f["reflex"]["lose"] if s not in f["lose"]]
    reflex_miss = [s for s in f["lose"] if s not in f["reflex"]["lose"]]
    lines = [
        "## Tags",
        "",
        "**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics: a Medicaid "
        "plan's hospital pay-for-performance measure conformed from its claims, a delegated group's encounters and the "
        "state's death record linkage, the linked deaths corrected for the linkage's own errors).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**%s of Halbrook's 14 network hospitals lose the 2027 Hospital Quality Bonus: %s. The other %s keep it.**" % (
            WORD[f["count_lose"]].capitalize(), _join([r["name"] for r in lose]), WORD[14 - f["count_lose"]]),
        "Their fiscal 2026 mortality ratios run from %.2f to %.2f against the 1.15 line; the highest ratio among the "
        "hospitals that keep it is %s's %.2f. Not the %s hospitals that the deaths on the bills and the Office of Vital "
        "Records' links give, even with every link a later claim contradicts dropped and every death a later bill "
        "records added (%s), because for members enrolled without a Social Security number the linkage links living "
        "members with common names to other people's deaths and misses the deaths of members with two-part surnames, "
        "and those repairs reach only the members whose later claims happen to show it: corrected at the error rates "
        "the record's recorded deaths and living members measure, %s keeps the bonus and %s lose it." % (
            min(r["ratio"] for r in lose), max(r["ratio"] for r in lose), top_keep["name"], top_keep["ratio"],
            WORD[f["reflex"]["count"]], _join(f["reflex"]["lose"]), _join(reflex_extra), _join(reflex_miss)),
        "",
        "## 2. Critical Components",
        "",
        "1. The linkage's error rates by identifier class, measured on the index admissions whose deaths the bills "
        "record and on the members seen alive after day 30: %s." % "; ".join(
            "%s, **%d of %d** recorded deaths linked and **%d of %s** living members linked" % (
                CLS[k], rt[k]["pos_linked"], rt[k]["pos"], rt[k]["neg_linked"], "{:,}".format(rt[k]["neg"]))
            for k in ("ssn", "simple", "compound")),
        "2. The hospitals that lose the bonus, deaths over expected deaths: %s." % "; ".join(
            "%s **%.1f** over **%.1f**, ratio **%.2f**" % (r["name"], r["deaths"], r["expected"], r["ratio"])
            for r in lose),
        "3. %s, which the uncorrected links put over the line: **%.1f** deaths over **%.1f** expected, ratio "
        "**%.2f**." % (_join([hs[s]["name"] for s in reflex_extra]), hs[reflex_extra[0]]["deaths"],
                       hs[reflex_extra[0]]["expected"], hs[reflex_extra[0]]["ratio"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Conformed %s and %s into stays, each as last corrected with voided and deleted bills dropped, Carrisford "
        "member numbers mapped through %s and both of Mercy Valley's NPIs through %s." % (
            W.FILES["claims"], W.FILES["encounters"], W.FILES["enrollment"], W.FILES["roster"]),
        "2. Kept the index admissions of specification 2.1 to 2.4 (%s in all): adults, no delivery DRGs, no patient "
        "status 07, each member's first, a transfer joined to the first hospital's stay." % "{:,}".format(
            f["index_total"]),
        "3. Summed each hospital's HIMM 3.2 scores from %s, keyed by member, admission date and NPI." % W.FILES["scores"],
        "4. Counted the deaths the bills record (patient status 20 on the stay, its transfer stay or a later stay ending "
        "within the 30 days) and joined %s on member and admission date." % W.FILES["linkage"],
        "5. Classed each member by %s (Social Security number on file; otherwise single or two-part surname) and "
        "measured each class's share of recorded deaths linked and share of members with a service line in %s, an "
        "admission or a live discharge after day 30 linked." % (W.FILES["enrollment"], W.FILES["activity"]),
        "6. For each hospital and class, estimated the deaths among the admissions neither recorded dead nor seen alive "
        "after day 30 as (links less the false-link share times the admissions) over (the share linked less the "
        "false-link share), and added the recorded deaths.",
        "7. Divided each hospital's deaths by its expected deaths and marked the hospitals over 1.15 (specification "
        "5.2).",
        "8. Took 2 per cent of each hospital's Halbrook payments for stays discharged in fiscal 2026 (Carrisford's out): "
        "each stay its original plus a CPS replacement's change or a platform replacement's full amount, a voided bill "
        "nothing, plus each additional payment in %s made by September 30 on those stays, except one the disputed "
        "claim's replacement bill paid that day already carries: the replacement's change to the stay's payment (a CPS "
        "replacement's amount, or a platform replacement's amount less the original's) equals the additional payment."
        % W.FILES["disputes"],
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["workbook"],
        "",
        "1. Hospitals that lose the 2027 bonus: **%d**: %s." % (f["count_lose"], _join([r["name"] for r in lose])),
        "2. Each hospital, 2027 bonus and bonus at stake (2 per cent of fiscal 2026 inpatient payments, nearest $100):",
    ]
    for r in f["hospitals"]:
        lines.append("   - %s: %s, %s" % (r["name"], r["verdict"], money(r["bonus"])))
    lines += [
        "3. Total bonus at stake across the network: %s." % money(f["total_bonus"]),
        "4. Bar chart of the 14 hospitals' fiscal 2026 mortality ratios against the 1.15 line, the five that lose the "
        "bonus highlighted.",
        "",
    ]
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
