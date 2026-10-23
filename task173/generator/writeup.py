"""task173 submission.md, drafted from figures.json only."""
from __future__ import annotations

import json
import os

import common as C
import calc


def f(x):
    if isinstance(x, float) and not x.is_integer():
        return "{:,.1f}".format(x) if abs(x) >= 100 else ("%.2f" % x if abs(x) < 10 else "%.1f" % x)
    return "{:,}".format(int(x))


def write(root, figs):
    F = figs
    figs = dict(F)
    figs["constants.window_days"] = 120
    figs["constants.round_unit"] = 250
    figs["constants.per"] = 100
    figs["constants.base_round"] = 10
    figs["constants.item_service"] = 101
    figs["constants.item_main"] = 201
    figs["constants.item_rest_first"] = 301
    figs["constants.item_rest_last"] = 305
    with open(os.path.join(root, "generator", "figures.json"), "w") as fh:
        json.dump({k: v for k, v in figs.items() if not k.startswith("_")}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    cen = [c.title() for c in C.CENTERS]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Energy Systems & Utilities (asset condition and maintenance).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Enter %s water service leak repairs as the Item 101 estimated quantity for 2027.** The AMI contract "
             "exchanges %s meters between February and July 2027, and every %d exchanges add about %s service leak "
             "repairs in the weeks after the new meters are set, on top of about %s repairs the services need "
             "without the visits. Not the record's %s repairs a year, which carry only the few exchanges the Meter "
             "Shop made each year." % (f(F["call.service_leak_repairs_2027"]), f(F["component.ami_exchanges_2027"]),
                                       100, "%.1f" % F["component.added_per_100_exchanges"],
                                       f(F["component.base_2027"]), f(F["step.record_repairs_per_year"])))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. 2027 service leak repairs without exchange visits: **%s** (nearest 100)." % f(F["component.base_2027"]))
    L.append("2. Added service leak repairs per %d meter exchanges: **%.1f**." % (100, F["component.added_per_100_exchanges"]))
    L.append("3. AMI meter exchanges scheduled for 2027: **%s**." % f(F["component.ami_exchanges_2027"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Counted one repair per leak, the CLOSED REP orders of WORK_TYPE SERVICE LEAK in %s and the CLOSED SVC "
             "LEAK orders in %s (MIGRATED orders are counted in EAM): %s a year from October 2024 to September 2026."
             % (C.F_EAM, C.F_LEGACY, f(F["step.record_repairs_per_year"])))
    L.append("2. Tied each repair to its GIS service (EAM ASSET_ID, legacy ADDRESS) and each meter exchange in %s (a "
             "REMOVE and the next SET at the premise) to the premise's service in %s, by SERVICE_ID or address."
             % (C.F_METER, C.F_PREM))
    L.append("3. Counted repairs on a service in the %d days after its new meter was set, for the %s exchanges whose "
             "window closes by 30 September 2026, less the service base rate outside those windows: %s added repairs "
             "per %d exchanges." % (120, f(F["step.history_exchanges"]),
                                    "%.2f" % F["component.added_per_100_exchanges_unrounded"], 100))
    L.append("4. Took the record's own exchange-visit repairs out of the record rate (%s exchanges a year in the window): "
             "%s repairs in 2027 without exchange visits." % (f(F["step.record_exchanges_per_year"]),
                                                              f(F["component.base_2027_unrounded"])))
    L.append("5. Applied the added rate to the %s METER EXCHANGE rows of %s, with the record's delay from exchange to "
             "repair, and added the two: %s repairs, %s at the nearest %d."
             % (f(F["component.ami_exchanges_2027"]), C.F_AMI, f(F["step.forecast_2027_unrounded"]),
                f(F["call.service_leak_repairs_2027"]), 250))
    L.append("6. Item 201: one break per main ASSET_ID and REPORTED time across its REP and REPC orders in %s, counted "
             "at its latest COMPLETED date and by the main's SVC_CENTER in %s: %s breaks in fiscal 2026."
             % (C.F_EAM, C.F_GIS_MAIN, f(F["ask_breaks.total"])))
    L.append("7. Items 301 to 305: for each estimate in %s the revision whose AMOUNT total equals the GROSS_AMOUNT "
             "paid in %s, QTY summed by surface type and quarter of WORK_COMPLETED." % (C.F_PAYEST, C.F_AP))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % C.DELIV_XLSX)
    L.append("")
    L.append("1. 2027 water service leak repairs: %s (nearest %d)." % (f(F["call.service_leak_repairs_2027"]), 250))
    L.append("2. Fiscal 2026 main break repairs by service centre and month:")
    for c in C.CENTERS:
        v = ["%s %d" % (calc.MON[m], F["ask_breaks.%s.%s" % (c.lower(), calc.MON[m].lower())]) for m in calc.FY_MONTHS]
        L.append("   - %s: %s" % (c.title(), ", ".join(v)))
    L.append("3. Fiscal 2026 restoration by surface type and quarter (Q1 October to December, Q2 January to March, Q3 "
             "April to June, Q4 July to September), square yards to the nearest %d:" % 10)
    for g in calc.GROUP_ORDER:
        k = g.lower().replace(" ", "_")
        v = [F["ask_restoration.%s.q%d" % (k, q)] for q in (1, 2, 3, 4)]
        L.append("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % ((g,) + tuple(f(x) for x in v)))
    L.append("")
    L.append("### %s" % C.DELIV_PNG)
    L.append("")
    L.append("1. Monthly service leak repairs January 2021 to September 2026 as a line, and the 2027 forecast by month "
             "as stacked bars, without exchange visits and added by the AMI exchanges.")
    L.append("")
    with open(os.path.join(root, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
