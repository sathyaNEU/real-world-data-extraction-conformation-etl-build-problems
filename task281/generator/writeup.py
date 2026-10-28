"""submission.md for task281, rendered from generator/figures.json so that every figure in the write-up is the one
the generator computed (build.py calls it after the goldens)."""
import json
import os

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
A_, B_ = P.DRV["A"].split()[0], P.DRV["B"].split()[0]


def c(n):
    return format(int(n), ",")


def render(fig):
    ph, fits, pl, call = fig["phases"], fig["fits"], fig["pooled"], fig["call"]
    gset = call["set"]
    names = ", ".join(gset[:-1]) + " and " + gset[-1]
    ins = [ph[p]["share5"] for p in gset]
    out = [p for p in P.PHASE_CODES if p not in gset]
    top_out = sorted(out, key=lambda p: -ph[p]["share"])[:2]
    pmin = min(ph[p]["pooled_pct"] for p in P.PHASE_CODES)
    pmax = max(ph[p]["pooled_pct"] for p in P.PHASE_CODES)
    a, b = fits[P.DRV["A"]], fits[P.DRV["B"]]
    floor = pl["expected_floor"]
    rest_max = max(ph[p]["share5"] for p in out)
    shares_in = ", ".join("%s %d" % (p, ph[p]["share5"]) for p in gset)
    shares_out = ", ".join("%s %d" % (p, ph[p]["share5"]) for p in out)
    towns = sorted(fig["towns"])
    k = fig["constants"]
    lines = []
    w = lines.append
    w("## Tags\n")
    w("**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: a censored "
      "lifetime distribution read past its follow-up).")
    w("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    w("## 1. Final Recommendation\n")
    w("**Put conversion phases %s into the 2027 group driver replacement program, %s luminaires still on their "
      "original driver.**" % (names, c(call["program_luminaires"])))
    w("Each of the five is projected at %d to %d per cent of its original-driver luminaires failing before their "
      "twelfth year against the %d per cent trigger, because only %s's drivers wear out and these phases were built "
      "mostly from %s lots. Not all ten, which one Weibull over every conversion driver files at %d to %d per cent "
      "each: it reads %s's survivors as failures still to come, expecting more than %s %s failures by the close "
      "against the %d recorded. Not %s or %s, the highest of the rest at %d and %d per cent, built mostly from %s "
      "lots.\n" % (min(ins), max(ins), k["trigger_pct"], A_, A_, round(pmin), round(pmax), B_, c(floor), B_,
                   b["failures"], top_out[0], top_out[1], ph[top_out[0]]["share5"], ph[top_out[1]]["share5"], B_))
    w("## 2. Critical Components\n")
    w("1. Driver failures on record to 31 December 2026: **%s %s** of %s drivers and **%s %d** of %s, against the "
      "**more than %s** %s failures one Weibull over every driver expects" % (
          A_, c(a["failures"]), c(a["drivers"]), B_, b["failures"], c(b["drivers"]), c(floor), B_))
    w("2. %s's original-driver lifetime: Weibull shape **%.1f**, characteristic life **%.1f years**; %s's drivers "
      "show no wear-out" % (A_, a["shape1"], a["life1"], B_))
    w("3. Projected share failing before year 12, to the nearest 5 per cent: **%s**; %s" % (shares_in, shares_out))
    w("4. Luminaires on their original driver on 1 January 2027 in the five phases: **%s**\n" % c(call["program_luminaires"]))
    w("## 3. Step-by-Step Solution\n")
    w("1. Took each luminaire's retrofit date, phase and lot from %s (both sheet layouts, every pole-tag form) and each "
      "lot's LED driver maker from %s: %s %s and %s %s drivers." % (
          P.FILES["install"], P.FILES["coc"], c(a["drivers"]), A_, c(b["drivers"]), B_))
    w("2. Dated each original driver's failure at the completion of the first driver-replacement order on its pole "
      "(DRVR in %s, SL-DRV-RPL in %s, the legacy orders open at the cutover counted once as MIGRATED) and each exit "
      "at its knockdown, warranty swap or pole removal order, per %s 2.2 to 2.4, every other luminaire suspended at "
      "its age on 31 December 2026." % (P.FILES["wo_legacy"], P.FILES["wo_new"], P.FILES["note"]))
    w("3. Fitted the two-parameter Weibull by maximum likelihood to each driver maker's drivers (the note's 3.1): %s "
      "shape %.1f and characteristic life %.1f years on %s failures; %s's %d failures show no wear-out, where one fit "
      "over both makers expects more than %s." % (A_, a["shape1"], a["life1"], c(a["failures"]), B_, b["failures"],
                                                 c(floor)))
    w("4. Averaged, over each phase's luminaires on their original driver on 1 January 2027, the probability of "
      "failure before the twelfth anniversary of installation given survival to their age that day, under their "
      "maker's fit: %s above %d per cent, every other phase at %d per cent or less." % (
          names, k["trigger_pct"], rest_max))
    w("5. Energy saved: each converted pole's sodium fixture from the installer's Removed column at %s input watts "
      "against its LED at the catalog's input watts, the LED at %d W from the completion of a glare order without a "
      "shield part where %s shows the pole at %d W, to its removal order's day, for the tariff's monthly burning hours "
      "by days in service, Corrinvale's LEDs at the dimmed level for the hours %s records." % (
          P.FILES["tariff"], k["reprogrammed_watts"], P.FILES["register"], k["reprogrammed_watts"], P.FILES["nlc"]))
    w("6. Late repairs: every outage order completed in 2026, timed from the first report of the outage in %s (portal "
      "stamps converted from UTC to the local time the orders carry, phone reports placed by pole number or register "
      "address), an underground cable order's reports taken from every pole on its riser's feed in the register, an "
      "order the crews found from its creation; counted those over %d hours (the tariff's 4.2)." % (
          P.FILES["reports"], k["repair_standard_hours"]))
    w("7. Designated the five phases above %d per cent: %s luminaires.\n" % (k["trigger_pct"],
                                                                          c(call["program_luminaires"])))
    w("## 4. Deliverable Answers\n")
    w("### %s\n" % P.GOLDEN_XLSX)
    w("1. The 2027 program: %s, %s luminaires on their original driver." % (names, c(call["program_luminaires"])))
    w("2. Projected share failing before year 12, to the nearest 5 per cent, and whether the phase goes in:")
    for p in P.PHASE_CODES:
        w("   - %s: %d per cent, %s" % (p, ph[p]["share5"], "in" if ph[p]["designated"] else "out"))
    w("3. Energy the converted poles saved in 2026 against the sodium fixtures, whole MWh:")
    for t in towns:
        w("   - %s: %s" % (t, c(fig["towns"][t]["energy"])))
    w("4. Outages repaired in 2026 that missed the 72-hour standard:")
    for t in towns:
        w("   - %s: %d" % (t, fig["towns"][t]["late"]))
    w("\n### %s\n" % P.GOLDEN_PNG)
    w("1. One bar per phase of its projected share, the %d per cent trigger drawn across, the five program phases set "
      "apart in colour, each bar labelled with its share to the nearest 5 per cent." % k["trigger_pct"])
    return "\n".join(lines) + "\n"


def write(fig, path=os.path.join(TASK, "submission.md")):
    with open(path, "w") as fh:
        fh.write(render(fig))


if __name__ == "__main__":
    write(json.load(open(os.path.join(HERE, "figures.json"))))
