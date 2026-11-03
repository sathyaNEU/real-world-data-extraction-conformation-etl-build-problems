"""submission.md, every figure read from figures.json."""
import os

import golden as G
import pack as PK
import params as P


def n(x, places=1):
    return format(x, ",") if isinstance(x, int) else ("%.*f" % (places, x))


def write(task_dir, fig, A):
    cab = {r["id"]: r for r in A["cabs"]}
    order = sorted(A["cabs"], key=lambda r: r["fail"])
    best, second = A["best"], A["second"]
    rivals = [r for r in order if r["id"] not in (best, second)]
    wre = [r for r in rivals if r["id"] == "WRE-FD35"][0]
    rd = [r for r in rivals if r["id"] != "WRE-FD35"]
    fn = lambda k: os.path.basename(PK.FILES[k])
    L = []
    L += ["## Tags", "", "**Domain:** Human Factors & Ergonomics (anthropometric design fit).",
          "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    L += ["## 1. Final Recommendation", "",
          "**We should specify %s for the 2027 front-line ambulance order.**" % G.LABEL[best],
          "It fails %s of our rostered drivers, %s fewer than the runner-up, %s, at %s. Not %s, whose longer stated seat "
          "travel fits more drivers on paper but whose forward bulkhead stops the backrest of its tall drivers short of "
          "their posture, so it fails %s. Not the two RD43 cabs, which fail %s and %s." % (
              n(fig["call_fail"]), n(fig["gap"]), G.LABEL[second], n(fig["runner_up_fail"]), G.LABEL["WRE-FD35"],
              n(fig["fail_WRE-FD35"]), n(fig["fail_PEN-RD43"]), n(fig["fail_WRE-RD43"])), ""]
    L += ["## 2. Critical Components", "",
          "1. %s fails **%s** rostered drivers." % (G.LABEL[best], n(fig["call_fail"])),
          "2. %s fails **%s**." % (G.LABEL[second], n(fig["runner_up_fail"])),
          "3. %s fails **%s** once each driver's backrest is placed against its bulkhead, against **%s** on its stated "
          "travel and vision alone." % (G.LABEL["WRE-FD35"], n(fig["fail_WRE-FD35"]), n(fig["default_fail"])), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Took every staff number on %s (the cab fit standard's section 2), joined each to its latest measurement in "
          "%s through %s for former Vennerley numbers, the Vennerley paper forms converted from inches, stones and "
          "pounds: %s drivers." % (fn("roster"), fn("measure"), fn("crosswalk"), n(fig["drivers"])),
          "2. Placed each driver in each shortlisted cab with the hip point, torso angle and eye point equations in %s, "
          "taking H30, the H-point travel, the bulkhead trim face and the chassis sight points from the package data, "
          "%s's dimensions moved from each cab's stated SgRP to the heel point." % (fn("posture"), fn("pkg_wrenfold")),
          "3. Set the seat to that posture: the hip point inside the cab's H-point travel, and the backrest at the "
          "predicted torso angle with its top rear corner (%.2f in along and %.2f in behind the torso line, %s) not "
          "behind the bulkhead trim face line at the corner's height." % (
              fig["backrest_along_in"], fig["backrest_behind_in"], fn("seat")),
          "4. Checked the eye point against the %d degree upward and %d degree downward sight lines to the chassis points "
          "(section 4) and counted the drivers each cab fails: the figures in block 4." % (
              fig["vision_up_deg"], fig["vision_down_deg"]),
          "5. Rebuilt each 2025-26 front-line vehicle from %s, %s and %s (renumbered Vennerley vehicles from their "
          "original in-service dates), and gave each job, telematics unit and off-road spell to the vehicle holding its "
          "fleet number on its date, reused numbers resolved through the disposals." % (
              fn("register"), fn("disposals"), fn("assets")),
          "6. Counted seat and cab-structure jobs (B12, B30 and their Vennerley codes in %s) by the quarter first "
          "raised, a Vennerley job carried into %s on 1 July 2025 counted once at its Vennerley date; took miles as each "
          "unit's distance while fitted per %s; and days off the road as the calendar days in the union of each "
          "vehicle's spells: the converter and chassis figures in block 4." % (
              fn("codemap"), fn("jobs"), fn("units")),
          "7. Specified the cab the fewest drivers fail (section 7): %s." % G.LABEL[best], ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % G.XLSX, "",
          "1. Rostered drivers each shortlisted cab fails to fit, whole drivers:"]
    for r in order:
        L.append("   - %s: %s, of whom %s women" % (r["cab"], n(r["fail"]), n(r["women"])))
    L.append("2. Recommended: %s; runner-up %s, which fails %s more drivers." % (G.LABEL[best], G.LABEL[second],
                                                                              n(fig["gap"])))
    L.append("3. Seat and cab-structure defect jobs raised in 2025-26 by quarter, miles run that year to the nearest "
             "hundred and jobs per %s miles to two decimals:" % n(fig["rate_miles_unit"]))
    for r in A["converters"]:
        k = r["converter"].split()[0].lower()
        L.append(("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s; %s miles; %s jobs per " + n(fig["rate_miles_unit"]) + " miles") % (
            r["converter"], *[n(fig["jobs_%s_q%d" % (k, i)]) for i in range(1, 5)], n(fig["miles_%s" % k]),
            n(fig["jobs_rate_%s" % k], 2)))
    L.append("4. Days off the road in 2025-26 by quarter, vehicle-years in service and days off the road per "
             "vehicle-year, to one decimal:")
    for r in A["chassis"]:
        k = r["chassis"].lower()
        L.append("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s; %s vehicle-years; %s days per vehicle-year" % (
            r["chassis"], *[n(fig["vor_%s_q%d" % (k, i)]) for i in range(1, 5)], n(fig["vy_%s" % k]),
            n(fig["vor_rate_%s" % k])))
    L += ["", "### %s" % G.PDF, "",
          "5. One bar per shortlisted cab giving the drivers it fails to fit, each bar labelled with its count, the %s bar "
          "in blue and marked Recommended." % G.SHORT[best], ""]
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write("\n".join(L))
