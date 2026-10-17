"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    rel = f["relationships"]
    back = [s for s in W.ORDER if rel[s]["verdict"] == "send back"]
    keep = [s for s in W.ORDER if rel[s]["verdict"] == "accept"]
    nm = lambda s: rel[s]["name"]
    join = lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]
    lines = [
        "## Tags",
        "",
        "**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution: the "
        "authority's stand log linked to three operators' flight logs and its registers into turns, each turn's need "
        "left-censored by the time its 2026 schedule gave it).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**Send back the minimum ground times filed for %s; accept the other three.**" % join(
            ["%s (%s minutes)" % (nm(s), rel[s]["filed"]) for s in back]),
        "An estimated %s per cent of those relationships' 2026 peak turns would need longer than the filed time, against "
        "the %s per cent SFG-3 allows; the shortest ground times the authority would accept from them are %s minutes, "
        "and from the three it accepts %s. Not accepting all six, which counts only the overruns the records show "
        "and divides by every turn (no relationship above %s per cent), although most 2026 turns had more time than "
        "the new filings and finished inside it; not sending all six back, which reads each turn's time on the stand "
        "as its need (at least %s per cent everywhere), although a turn ready early waited for its scheduled "
        "departure." % (join([rel[s]["share_at_filed"] for s in back]), f["standard_pct"],
                         join([rel[s]["shortest"] for s in back]),
                         join(["%s (filed %s)" % (rel[s]["shortest"], rel[s]["filed"]) for s in keep]),
                         f["rivals"]["visible_overruns_max_pct"], f["rivals"]["ground_time_min_pct"]),
        "",
        "## 2. Critical Components",
        "",
        "1. Turns at the E gates with on-block from 15 June to 15 September 2026: %s." % join(
            ["**%s** (%s)" % (rel[s]["turns_2026"], nm(s)) for s in W.ORDER]),
        "2. Estimated share of each relationship's peak turns needing longer than its filing: %s." % join(
            ["**%s per cent** (%s, filed %s)" % (rel[s]["share_at_filed"], nm(s), rel[s]["filed"]) for s in W.ORDER]),
        "3. Shortest ground time each relationship's turns allow under the standard: %s." % join(
            ["**%s minutes** (%s; %s per cent at %s, %s per cent five minutes shorter)" % (
                rel[s]["shortest"], nm(s), rel[s]["share_at_shortest"], rel[s]["shortest"],
                rel[s]["share_5_below_shortest"]) for s in W.ORDER]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Built turns from %s: registrations read without the hyphen, each on-block at an E stand paired with the "
        "same aircraft's next off-block on the same operating day, 03:00 to 02:59 (SFG-3 2.2, towed turns kept, night "
        "stops out), and kept the turns with on-block from 15 June to 15 September 2026." % W.FILES["aodb"],
        "2. Gave each turn the relationship of its departing flight: the callsign's number in the flight number blocks "
        "of %s and the aircraft type of its registration in %s." % (W.FILES["affiliates"], W.FILES["aircraft"]),
        "3. Joined each departure to its operator's log by flight number and date (%s from UTC to Kelderby time, %s with "
        "the sub-code letter dropped, %s with its delay field split) for the scheduled departure and the minutes coded "
        "aircraft not ready or held for another reason in %s." % (
            W.FILES["pellmont"], W.FILES["sable"], W.FILES["grayling"], W.FILES["delay_codes"]),
        "4. Read each turn's need under SFG-3 2.4: the time it had (scheduled departure less on-block) plus its "
        "not-ready minutes where it held its departure, and no more than the time it had where it was ready in time.",
        "5. Estimated, for each relationship, the share of turns needing longer than each ground time with the "
        "product-limit estimator for needs censored in this way; the share among turns that had less than the ground "
        "time, each of which shows whether it needed longer, gives the same decisions.",
        "6. Applied SFG-3 3.1 and 3.3 to the filings in %s: %s sent back, the shortest acceptable ground time being the "
        "first five-minute step at or under %s per cent." % (W.FILES["filings"], join([nm(s) for s in back]),
                                                              f["standard_pct"]),
        "7. Counted the turns of the week of 12 to 18 July 2027 in %s, UTC files on Kelderby time, each arrival paired "
        "with the same aircraft's next departure on the same operating day by its onward link or its next leg; each "
        "rotation a brand files again under its own numbers (the same legs, times and type as a partner's, numbers "
        "%s never carried, more rotations than %s gives the operators aircraft) counted once, under the numbers the "
        "operator flies (SFG-3 2.1)." % (W.FILES["ssim27"], W.FILES["ssim26"], W.FILES["fleet27"]),
        "8. Recommended sending back the three filings and accepting the other three.",
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["workbook"],
        "",
    ]
    for i, s in enumerate(W.ORDER):
        r = rel[s]
        lines.append("%d. %s: filed %s minutes, %s, shortest ground time accepted %s minutes." % (
            i + 1, r["name"], r["filed"], "sent back" if r["verdict"] == "send back" else "accepted", r["shortest"]))
    n = len(W.ORDER)
    lines.append("%d. Line chart on the Need curves sheet of each relationship's share of 2026 peak turns needing longer "
                 "than each ground time from 20 to 60 minutes, the 20 per cent standard dashed." % (n + 1))
    lines.append("%d. Turns the summer 2027 initial submissions schedule at Kelderby in the week of 12 to 18 July 2027, "
                 "and of them shorter than the filed ground time:" % (n + 2))
    for s in W.ORDER:
        lines.append("   - %s: %s turns, %s shorter" % (nm(s), rel[s]["week_turns"], rel[s]["week_short"]))
    lines.append("")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
