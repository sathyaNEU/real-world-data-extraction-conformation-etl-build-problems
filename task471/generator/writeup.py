"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed."""
import json

import pack as P
import world as W

F = P.FILES


def _list(names):
    return ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]


def write(fig_path, out_path):
    fig = json.load(open(fig_path, encoding="utf-8"))
    progs = fig["programs"]
    rev = sorted((q for q in progs if q["review"]), key=lambda q: q["name"])
    words = {3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven"}
    nab, nbe = fig["nearest_above"], fig["nearest_below"]
    eq_hi = fig["equated_at_cut"]
    eq_lo = fig["equated_below_cut"]
    lines = []
    lines.append("## Tags\n")
    lines.append("**Domain:** Education & Learning Sciences (item response theory and test equating: a licensing "
                 "board conforms two scoring contractors' results, its attempt history and its programs' completer "
                 "lists onto the 2025 reporting scale, equating the 2026 form to the 2025 form through a mixed-format "
                 "anchor whose rater-scored assignment is put back on the 2025 rating standard).  ")
    lines.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    lines.append("## 1. Final Recommendation\n")
    lines.append("**%s of the sixteen programs fall below 70 per cent and go to formal review in 2027: %s. The other "
                 "%s do not.**  " % (words[len(rev)], _list(["%s (%.1f)" % (q["name"], q["rate"]) for q in rev]),
                                     {11: "eleven", 10: "ten", 12: "twelve", 9: "nine"}[16 - len(rev)]))
    lines.append("Their 2025-26 completers' first-attempt pass rates run from %.1f to %.1f per cent; the lowest rate "
                 "among the programs that stay off review is %s's %.1f. The Form 26A raw passing score is %d. Not the "
                 "eight programs the anchor gives as Arcwright's raters scored it (raw %d: Delacourt, Marisford and "
                 "Riverbend added), because WA2, the anchor's written assignment, was read in 2026 by a new scoring "
                 "team that read its validity papers, June 2025 responses, %.2f points per read below the scores the "
                 "2025 reads gave them, which makes the 2026 cohort look weaker on the anchor than it is; nor the list "
                 "the twenty shared multiple-choice "
                 "items alone give (raw %d or %d: Eastridge comes off it), because the 2026 candidates' weaker writing, "
                 "which WA2 shows even on the 2025 standard and the shared items do not, is part of the difference "
                 "the anchor has to carry.\n" % (
                     min(q["rate"] for q in rev), max(q["rate"] for q in rev), nab["name"], nab["rate"],
                     fig["raw_cut"], fig["rungs"]["as scored"], -fig["validity_bias"],
                     min(fig["rungs"]["multiple-choice anchor"]), max(fig["rungs"]["multiple-choice anchor"])))
    lines.append("## 2. Critical Components\n")
    lines.append("1. WA2 on the 2025 standard: Arcwright's raters read the %d WA2 validity papers, June 2025 responses "
                 "whose two 2025 reads agreed, %d times, **%.2f** points per read below the 2025 score, so each 2026 WA2 "
                 "score moves up by **%.2f** and each 2026 anchor score by **%.2f**." % (
                     fig["wa2_papers"], fig["wa2_validity_reads"], -fig["validity_bias"], -2 * fig["validity_bias"],
                     fig["anchor_shift"]))
    lines.append("2. The Form 26A raw passing score: **%d**. At raw %d every method's equated Form 25A score is %.2f to "
                 "%.2f, which rounds to %d (scale 240); at raw %d it is %.2f to %.2f, which rounds to %d." % (
                     fig["raw_cut"], fig["raw_cut"], min(eq_hi.values()), max(eq_hi.values()), fig["pass_raw_25a"],
                     fig["raw_cut"] - 1, min(eq_lo.values()), max(eq_lo.values()), fig["pass_raw_25a"] - 1))
    lines.append("3. The programs on review, passers over completers counted: %s; the nearest program above the line, "
                 "%s, **%d** of **%d** (**%.1f** per cent).\n" % (
                     "; ".join("%s **%d** of **%d** (**%.1f** per cent)" % (q["name"], q["passed"], q["counted"],
                                                                         q["rate"]) for q in rev),
                     nab["name"], [q for q in progs if q["name"] == nab["name"]][0]["passed"],
                     [q for q in progs if q["name"] == nab["name"]][0]["counted"], nab["rate"]))
    lines.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Matched the June 2026 registrations in %s to educator records through %s and dated each educator's first "
        "attempt from %s, voided attempts left out (Rule 8.4.3): %s first attempts on Form 25A in June 2025 and %s on "
        "Form 26A in June 2026." % (F["scores26"], F["crosswalk"], F["history"], "{:,}".format(fig["n_first_2025"]),
                                   "{:,}".format(fig["n_first_2026"])),
        "Scored each first attempt's anchor: the 20 items both forms carry (matched by item ID in %s; Form 25A's from "
        "the ITEM_SCORES positions in %s, Form 26A's from %s) plus twice its WA2 score (the two reads summed, or twice "
        "a resolution read)." % (F["maps"], F["scores25"], F["items26"]),
        "Measured Arcwright's raters against the 2025 raters on WA2: the VALIDITY reads of the WA2 papers in %s "
        "against each paper's score on file in %s (June 2025 responses, the score both 2025 reads gave), %.2f points "
        "per read below it; "
        "moved every 2026 WA2 score (two reads) up by %.2f, so the anchor's 2026 reads keep their own rater-to-rater "
        "spread and sit at the 2025 standard, as the 2025 anchor scores do." % (
            F["reads26"], F["qc26"], -fig["validity_bias"], -2 * fig["validity_bias"]),
        "Equated Form 26A to Form 25A on the two first-attempt samples through that anchor (Tucker and Levine at each "
        "synthetic-population weight, chained linear and chained equipercentile agree), rounded each equated score and converted "
        "it with %s: raw %d is the lowest Form 26A score at a scale score of 240." % (F["conv"], fig["raw_cut"]),
        "Took each program's 2025-26 completers from %s: elementary pathways only, completion dates July 1, 2025 to "
        "June 30, 2026, each educator once (Rule 8.4.2)." % F["completers"],
        "Gave each completer's first attempt at or before June 13, 2026 its result: a June 2026 first attempt passes at "
        "raw %d or more, an earlier one keeps its reported result; completers with no attempt are not counted (8.4.4); "
        "programs under 70 per cent go to review (8.4.1)." % fig["raw_cut"],
        "For the 2024-25 completers, took the elementary pathways of program year 2024-25 in %s and matched each to "
        "the history by educator ID, and where that record has no attempts, by name and birth date (a completer the "
        "program entered under a new educator record); counted first attempts at or before June 14, 2025 and their "
        "results." % F["register"],
        "Charted the sixteen 2026 rates against the 70 per cent line, the programs on review highlighted.",
    ]
    for i, s in enumerate(steps, 1):
        lines.append("%d. %s" % (i, s))
    lines.append("\n## 4. Deliverable Answers\n")
    lines.append("### eli_2027_program_review.xlsx\n")
    lines.append("1. Programs that go to formal review in 2027: **%d**: %s." % (len(rev), _list([q["name"] for q in rev])))
    lines.append("2. Form 26A raw passing score: **%d**." % fig["raw_cut"])
    lines.append("3. Each program's 2025-26 completers counted, passers on first attempt and first-attempt pass rate "
                 "(per cent, one decimal):")
    for q in progs:
        lines.append("   - %s: %d completers, %d passed, %.1f" % (q["name"], q["counted"], q["passed"], q["rate"]))
    lines.append("4. Each program's 2024-25 completers with a first attempt by June 14, 2025, and their first-attempt "
                 "pass rate (per cent, one decimal):")
    for q in progs:
        lines.append("   - %s: %d completers, %.1f" % (q["name"], q["prior_tested"], q["prior_rate"]))
    lines.append("\n### eli_2026_program_pass_rates.png\n")
    lines.append("5. Bar chart of the sixteen programs' 2026 first-attempt pass rates against the 70 per cent line, the "
                 "%s programs on review highlighted." % words[len(rev)].lower())
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
