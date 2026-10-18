"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


WORD = {4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    q = f["qualifying"]
    rv = f["rivals"]
    c = f["counted"]
    nd = f["never_recorded"]
    names = {r["lid"]: r["name"] for r in f["fields"]}
    lines = [
        "## Tags",
        "",
        "**Domain:** Physical & Environmental Sciences (emissions inventory: airport lead inventory built from an ADS-B "
        "receiver network's operations, the FAA aircraft register, tower and commissioned counts and the state's based "
        "aircraft list, the operations the network cannot see estimated from the airplanes that never broadcast).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**%s of the 24 fields without a tower qualify for the 2027 round: %s.**" % (
            f["count_word"], _join(["%s (%s)" % (r["name"], r["lid"]) for r in q])),
        "Their 2026 lead from piston-engine aircraft runs from %d to %d kg against the round's %s kg; the highest field "
        "below the line, %s, has %d kg. Not the %s fields one capture rate gives (the counted fields' %s per cent "
        "applied to every field's recorded operations, which adds %s and drops %s), because the operations the "
        "network misses belong to the airplanes that never broadcast, few at the flight-school fields and many at "
        "the vintage ones; not the %s fields a capture rate split by flight training gives (%s per cent and %s per "
        "cent, which adds %s)." % (
            min(r["lead_kg"] for r in q), max(r["lead_kg"] for r in q), f["threshold_kg"], f["first_below"]["name"],
            f["first_below"]["lead_kg"], WORD[len(rv["capture_set"])], rv["capture_pct"], _join(rv["capture_in"]),
            _join(rv["capture_out"]), WORD[rv["training_set_count"]], rv["school_pct"], rv["other_pct"],
            _join(rv["training_in"])),
        "",
        "## 2. Critical Components",
        "",
        "1. Operations the network did not record at the ten counted fields: **%s**, against **%s** based piston "
        "airplanes there that the network never recorded in 2026: **%s** operations a never-recorded airplane." % (
            c["unrecorded"], c["never_recorded"], c["per_airplane"]),
        "2. Based piston airplanes the network never recorded in 2026 at the 20 fields without a count: %s." % _join(
            ["%s **%s**" % (lid, n) for lid, n in nd.items()]),
        "3. Lead of the qualifying fields, 2026: %s." % _join(["%s **%d kg**" % (r["lid"], r["lead_kg"]) for r in q]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Read %s with times from UTC to Pacific time, kept 2026, and gave each event its aircraft through icao24 "
        "and MASTER.txt or, for a registration cancelled during 2026, DEREG.txt by its issue and cancel dates; "
        "priced each piston-engine operation by ACFTREF.txt's engines and Table 1 of %s, a touch-and-go two "
        "operations." % (W.FILES["events"], W.FILES["method"]),
        "2. At the six towers, took %s's civil operations less the civil events the network recorded in the tower "
        "hours of %s (method 4.2); at the four count fields, the studies' piston-engine operations less those "
        "recorded (method 4.3)." % (W.FILES["atct"], W.FILES["directory"]),
        "3. Matched %s's N-numbers, written four ways, to the register and found the based piston airplanes whose "
        "addresses the network never recorded in 2026." % W.FILES["based"],
        "4. Divided the counted fields' unrecorded operations by their never-recorded airplanes: %s operations an "
        "airplane." % c["per_airplane"],
        "5. At each field without a count, priced %s operations for each never-recorded airplane at %s g (method 3.2 "
        "and 4.4) and added the recorded lead." % (c["per_airplane"], f["unrecorded_g"]),
        "6. Compared each field's 2026 lead with the %s kg of the round's guidelines (section 2.2): %s qualify." % (
            f["threshold_kg"], f["count_word"].lower()),
        "7. Built the towered fields' piston operations and lead the same way, each operation assigned to the "
        "aircraft that held its address that day.",
        "8. Recommended the %s fields for the 2027 round." % f["count_word"].lower(),
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["csv"],
        "",
        "1. Lead from piston-engine aircraft, 2026, each field without a tower:",
    ]
    for r in f["fields"]:
        lines.append("   - %s (%s): %d kg" % (r["name"], r["lid"], r["lead_kg"]))
    lines += [
        "",
        "### %s" % W.GOLDEN["memo"],
        "",
        "1. Qualifying fields, 2026 lead:",
    ]
    for r in q:
        lines.append("   - %s (%s): %d kg" % (r["name"], r["lid"], r["lead_kg"]))
    lines += [
        "2. Bar chart of the 24 fields' 2026 lead against the round's %s kg threshold, the qualifying fields "
        "highlighted." % f["threshold_kg"],
        "3. Towered fields, 2026 piston-engine operations and lead:",
    ]
    for r in f["towers"]:
        lines.append("   - %s (%s): %s operations, %d kg" % (r["name"], r["lid"], r["ops"], r["lead_kg"]))
    lines.append("")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
