"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(fig_path, out):
    f = json.load(open(fig_path))
    pl = f["call"]["planned"]
    dp = f["default_path"]["planned"]
    ids = sorted(f["ask"])
    added = [u for u in pl if u not in dp]
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Place %s on a timeliness improvement plan.**" % _and(pl))
    w("Their median working days from a complete application to registration, for the applications received from 1 "
      "July to 30 September 2026, exceed 20; no other office's do. Part of each office's quarter is still open on 9 "
      "October, and the open applications are the slow ones, so each is kept at risk until its age (a product-limit "
      "median). On the registered applications alone only %s are over; %s hold their backlog among the open "
      "applications." % (_and(dp), _and(added)))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Offices placed on a plan: %s" % ", ".join("**%s**" % u for u in pl))
    w("2. Offices not placed: %s" % ", ".join(u for u in ids if u not in pl))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Stacked the legacy log (DD/MM/YYYY, two-letter office codes) and the case system's log, and kept the "
      "applications received 1 July to 30 September 2026.")
    w("2. Counted working days from the clock start (the complete day, not counted) to registration, excluding "
      "weekends and the holiday calendar.")
    w("3. Added the open caseload snapshot's third-quarter applications, each at its working days from clock start to "
      "9 October, as still running.")
    w("4. For each office took the product-limit (Kaplan-Meier) survival estimate over registered and open "
      "applications and its median, the first duration at which the estimate falls to one half.")
    w("5. Placed the offices whose median exceeds 20: %s." % ", ".join(pl))
    w("6. Ask: each payment dated by its settlement batch's terminal day (the payment file carries the settlement day, "
      "the next working day), payments taken 1 July to 30 September counted and summed by office.")
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### cro_timeliness_plans_q3_2026.xlsx")
    w("")
    w("1. Offices placed on a plan: %s." % ", ".join(pl))
    w("2. Chart of each office's median working days against the 20-day line, the planned offices marked.")
    w("3. Card payments made in the third quarter, number and amount (whole euros):")
    for u in ids:
        w("   - %s: %s, EUR %s" % (u, "{:,}".format(f["ask"][u]["payments"]), "{:,}".format(f["ask"][u]["amount"])))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
