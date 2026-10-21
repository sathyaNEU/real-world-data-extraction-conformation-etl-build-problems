"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(fig_path, out):
    f = json.load(open(fig_path))
    ch = f["call"]["chosen"]
    dp = f["default_path"]["chosen"]
    ids = sorted(f["ask_a"])
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Send %s to the 2027 re-validation.**" % _and(ch))
    w("Their registers' share of records in error exceeds 4 per cent; no other region's does. The summer audit drew "
      "the records the May risk screen had referred far more often than the rest, and referred records are in error "
      "far more often, so each audited record is carried to its stratum's records on the 30 April register. Read as "
      "the audited share, %d regions would go (%s), at audited error shares the registers themselves do not have." % (
          len(dp), _and(dp)))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Regions going to re-validation: %s" % ", ".join("**%s**" % u for u in ch))
    w("2. Regions not going: %s" % ", ".join(u for u in ids if u not in ch))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Took the 30 April 2026 register: records created before 1 May in Ardmuir local time (the extract's times "
      "are UTC, an hour behind in summer), active and since dissolved.")
    w("2. Marked each record referred or not from the May risk screen's referral list.")
    w("3. Joined the audit outcomes by record, old region codes through the crosswalk; FAIL and codes 1 to 4 are "
      "errors.")
    w("4. In each region and stratum (referred, not referred) took the audited error rate and carried it to the "
      "stratum's records on the 30 April register; summed and divided by the region's records.")
    w("5. Chose the regions over 4 per cent: %s." % ", ".join(ch))
    w("6. Ask A: registrations created from 1 July to 30 September 2026 in Ardmuir local time.")
    w("7. Ask B: companies whose last notice in the quarter is struck off and dissolved (a later restoration takes a "
      "company back onto the register).")
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### sar_register_revalidation_2027_regions.xlsx")
    w("")
    w("1. Regions going to re-validation: %s." % ", ".join(ch))
    w("2. Chart of each region's register error rate against the 4 per cent line, the chosen regions marked.")
    w("3. New registrations in the third quarter of 2026:")
    for u in ids:
        w("   - %s: %s" % (u, "{:,}".format(f["ask_a"][u])))
    w("4. Companies struck off and dissolved in the quarter and still dissolved at its end:")
    for u in ids:
        w("   - %s: %s" % (u, "{:,}".format(f["ask_b"][u])))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
