"""submission.md, drafted from figures.json: the five blocks and nothing else."""
from __future__ import annotations

import datetime as dt

import deliver as DL
import records as R
import docs as D


def fmt(n):
    return "{:,}".format(int(n))


def write(path, b, res, f):
    worst = f["call_limiting"]
    L = f["call_largest_m3d"]
    lines = []
    lines.append("## Tags")
    lines.append("")
    lines.append("**Domain:** Physical & Environmental Sciences (hydrology: the drawdown a groundwater abstraction "
                 "causes at neighbouring licensed boreholes over a licence term).")
    lines.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    lines.append("")
    lines.append("## 1. Final Recommendation")
    lines.append("")
    lines.append("**Apply for %s cubic metres a day: the 1,800 a day the new line needs fails the derogation test, "
                 "and %s limits the quantity.**" % (fmt(L), worst))
    lines.append("At 1,800 a day %s's predicted drawdown on 31 March 2039 is %d m against its %.2f m available "
                 "drawdown. Not the unbounded aquifer the June 2014 test fits, which never reached the Coldharbour "
                 "Fault and lets 1,800 pass with Kilnbrook Nurseries limiting. Not an unbounded aquifer refitted or "
                 "scaled to the observation boreholes' record since 2015, which still puts the limit at Kilnbrook "
                 "Nurseries and above %s." % (worst, f["at1800_lower_m"], f["avail_lower_m"], fmt(L)))
    lines.append("")
    lines.append("## 2. Critical Components")
    lines.append("")
    lines.append("1. The June 2014 constant-rate test gives a transmissivity of **%d m2/d** and a storage coefficient "
                 "of **%.5f**." % (f["T_m2d"], f["S"]))
    lines.append("2. The Coldharbour Fault closes the aquifer east of Borehole 2, so each protected borehole's drawdown "
                 "includes that of Borehole 2's image across the fault.")
    lines.append("3. %s's predicted drawdown on 31 March 2039 at 1,800 a day is **%d m** against **%.2f m** "
                 "available." % (worst, f["at1800_lower_m"], f["avail_lower_m"]))
    lines.append("")
    lines.append("## 3. Step-by-Step Solution")
    lines.append("")
    lines.append("1. Fitted Theis to the drawdown at OB1, OB2 and OB3 in %s (OB3's kPa converted and its local clock "
                 "set to UTC, the rate the field sheet's flow checks give): transmissivity %d m2/d, storage coefficient "
                 "%.5f." % (R.F_TEST, f["T_m2d"], f["S"]))
    lines.append("2. Took the Coldharbour Fault's trace from the two grid references in %s, where it throws the "
                 "sandstone down %d m to the east against Mercia Mudstone, and placed Borehole 2's image across it." %
                 (D.F_GEOLOGY, f["fault_throw_m"]))
    lines.append("3. Set both models against %s less the Windle Cross regional movement in %s, under the returns' "
                 "abstraction: the closed aquifer fits to %.2f m rms against %.2f m for the unbounded one, and Windle "
                 "Cross shows no response." % (R.F_OBS, R.F_RMB, f["rms_closed_m"], f["rms_unbounded_m"]))
    lines.append("4. Ran the pre-application letter's derogation test with the image well: at 1,800 a day the "
                 "predicted drawdowns are %d m at Lower Hay Farm, %d m at Kilnbrook Nurseries and %d m at Hollin Bank "
                 "Golf Club, each above its available drawdown." % (f["at1800_lower_m"], f["at1800_kilnbrook_m"],
                                                                      f["at1800_hollin_m"]))
    lines.append("5. Solved each protected borehole's quantity at its available drawdown: %s limits, and the largest "
                 "daily quantity that passes is %s cubic metres." % (worst, fmt(L)))
    lines.append("6. For the returns check, set each ticket in %s on its run in %s (a time in before noon belongs to "
                 "the next calendar day, the haulier's night shift), added the bulk loads to FM-1's volume from %s by "
                 "local day, and counted the days above 1,200 m3." % (R.F_TICKETS, R.F_PUMP, R.F_TELEM))
    lines.append("7. For line 3, divided FM-L3's water by local month by the good bottles in %s times each bottle's "
                 "size, as %s sizes it, with BSG-1101 at the 750 ml its fill weights in %s show through March 2026, "
                 "not the export's 700." % (R.F_RUNS, D.F_BRIEF, R.F_QC))
    lines.append("8. Apply for %s cubic metres a day." % fmt(L))
    lines.append("")
    lines.append("## 4. Deliverable Answers")
    lines.append("")
    lines.append("### %s" % DL.G_NOTE)
    lines.append("")
    lines.append("1. Largest daily quantity that passes the derogation test: %s cubic metres a day." % fmt(L))
    lines.append("2. Protected borehole that limits it: %s." % worst)
    lines.append("3. Whether 1,800 cubic metres a day passes: no.")
    lines.append("4. Predicted drawdown on 31 March 2039 at 1,800 cubic metres a day:")
    lines.append("   - Lower Hay Farm: %d m" % f["at1800_lower_m"])
    lines.append("   - Kilnbrook Nurseries: %d m" % f["at1800_kilnbrook_m"])
    lines.append("   - Hollin Bank Golf Club: %d m" % f["at1800_hollin_m"])
    lines.append("5. Chart on page 1: %s's predicted drawdown at each 31 March from 2016 to 2039, at %s and at 1,800 "
                 "cubic metres a day, against its %.2f m available drawdown." % (worst, fmt(L), f["avail_lower_m"]))
    lines.append("6. Litres of water line 3 took per litre packed, cleans included:")
    for k in DL.MONTHS_B:
        lines.append("   - %s: %.2f" % (DL.month_label(k), f["askB_l3_%04d_%02d" % k]))
    lines.append("")
    lines.append("### %s" % DL.G_CSV)
    lines.append("")
    lines.append("1. Volume taken from Borehole 2 and days above 1,200 cubic metres, by month from April to "
                 "September 2026:")
    for k in DL.MONTHS_A:
        lab = "%04d_%02d" % k
        n = f["askA_days_%s" % lab]
        lines.append("   - %s: %s m3, %d %s" % (DL.month_label(k), fmt(f["askA_volume_%s" % lab]), n,
                                                 "day" if n == 1 else "days"))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
