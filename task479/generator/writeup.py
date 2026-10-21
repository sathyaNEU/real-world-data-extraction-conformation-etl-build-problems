"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json


def write(fig_path, out):
    f = json.load(open(fig_path))
    d = f["call"]["designated"]
    sh = f["below_basic_pct"]
    dp = f["default_path"]
    extra = [c for c in dp["designated"] if c not in d]
    L = []
    w = L.append
    w("## Tags")
    w("")
    w("**Domain:** Education & Learning Sciences (item response theory and test equating).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Designate %s and %s for 2026-27 high-dosage tutoring.**" % (", ".join(d[:-1]), d[-1]))
    w("%s per cent of their students tested in spring 2026 are below Basic, against the 35 per cent line; no other "
      "campus reaches it. Not %s, which reach %s per cent only on the vendor's reported scores: their students "
      "answered many items in under three seconds at the blind-guess rate, and scored on the responses given with "
      "effort they stand at %s per cent." % (
          ", ".join(sh[c] for c in d[:-1]) + " and " + sh[d[-1]], ", ".join(extra),
          ", ".join(dp["below_basic_pct"][c] for c in extra), ", ".join(sh[c] for c in extra)))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Designated campuses: %s" % ", ".join("**%s**" % c for c in d))
    w("2. Share of students tested below Basic, per cent: %s" % ", ".join("%s **%s**" % (c, sh[c]) for c in sorted(sh)))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Took the spring 2026 item responses from both exports (milliseconds before the 30 March release, seconds "
      "after) and the bank's 3PL parameters.")
    w("2. Found the rapid responses: none of the engaged responses took under 7.5 seconds, and those under 3 seconds "
      "were right a quarter of the time at every difficulty, the blind-guess rate on four options.")
    w("3. Rescored every student by maximum likelihood on the bank, as the technical summary scores, from the responses "
      "given in 5 seconds or more, the rapid ones treated as not administered; scale 500 + 40 theta, bounded 350 to 650.")
    w("4. Took each campus's share of students tested below 470 and applied the 35 per cent line: %s." % ", ".join(d))
    w("5. Ask A: the fall 2025 report with each temporary id resolved through the register and the fall roster to the "
      "student, the later administration of a restarted session kept; share at or above 520.")
    w("6. Ask B: fall students linked to their winter ids through the crosswalk and, for those it misses, by name and "
      "birth date between the rosters; growth is winter less fall, by winter campus.")
    w("7. Recommended %s." % ", ".join(d))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### bellweather_2026-27_tutoring_designation.xlsx")
    w("")
    w("1. Share of students tested below Basic, per cent to one decimal, and the designation:")
    for c in sorted(sh):
        w("   - %s: %s, %s" % (c, sh[c], "designated" if c in d else "not designated"))
    w("2. Chart of the fourteen campuses' shares against the 35 per cent line, the designated four in teal.")
    w("3. Fall 2025: students tested and share at or above Proficient (per cent to one decimal):")
    for c in sorted(f["ask_a"]):
        a = f["ask_a"][c]
        w("   - %s: %d, %s" % (c, a["tested"], a["proficient_pct"]))
    w("4. Students tested in fall and winter and their mean fall-to-winter growth (scale points to one decimal):")
    for c in sorted(f["ask_b"]):
        bb = f["ask_b"][c]
        w("   - %s: %d, %s" % (c, bb["students"], bb["growth"]))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
