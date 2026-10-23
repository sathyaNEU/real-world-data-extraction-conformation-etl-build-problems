"""submission.md, every figure read from generator/figures.json."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def join(xs, word="and"):
    xs = [str(x) for x in xs]
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " %s " % word + xs[-1]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    st = f["stores"]
    c = f["components"]
    d = f["default"]
    nb = c["nearest_below"]
    tau = c["tau_minutes"]
    cov = [str(n) for n in f["call"]["stores"]]
    dflt = [str(n) for n in d["stores"]]
    out_ = [n for n in dflt if n not in cov]
    in_ = [n for n in cov if n not in dflt]
    order = sorted(st, key=int)
    o = []
    o.append("## Tags\n")
    o.append("**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution "
             "(thirty pharmacy stores' 2026 vaccine refrigerator temperature records, kept by three data logger makes "
             "and at ten pilot stores from mid-year by an in-carton sensor, conformed into one record of the "
             "vaccine's temperature per store).")
    o.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    o.append("## 1. Final Recommendation\n")
    o.append("**Penwick Pharmacy replaces the vaccine refrigerators of stores %s before the 2027 respiratory "
             "season.**" % join(cov))
    o.append("Their vaccine spent %s hours above 8 °C in 2026 against the 24-hour line; the nearest store below it, "
             "%d %s, spent %d, %d short. Not the loggers' own readings, which put %s over the line at %s hours and "
             "%s under it at %s: a logger's probe in its glycol bottle crosses 8 °C through every defrost swing, "
             "restock and busy hour the vaccine in its cartons rode out, and ends a propped-door delivery's "
             "excursion before the vaccine has cooled.\n"
             % (join([st[n]["hours"] for n in cov]), nb["store"], nb["town"], nb["hours"], nb["short_hours"],
                join(out_), join([d["hours"][n] for n in out_]), join(in_), join([d["hours"][n] for n in in_])))
    o.append("## 2. Critical Components\n")
    o.append("1. On the pilot stores' overlaps the in-carton sensor trails its logger's record by a first-order lag "
             "of **%.1f** minutes at the Frostline stores, **%.1f** at the Kelvra stores and **%.1f** at the "
             "Brumal stores." % (tau["Frostline"], tau["Kelvra"], tau["Brumal"]))
    k = 2
    for n in in_:
        o.append("%d. Store %s's vaccine spent **%d** hours above 8 °C, %d on its logger's readings."
                 % (k, n, st[n]["hours"], d["hours"][n]))
        k += 1
    o.append("%d. Stores %s, over the line on their loggers' readings, spent **%s** hours." % (
        k, join(out_), join([st[n]["hours"] for n in out_])))
    o.append("%d. The nearest store below the line is %d %s at **%d** hours, **%d** short.\n"
             % (k + 1, nb["store"], nb["town"], nb["hours"], nb["short_hours"]))
    o.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Put frostline_temperature_logs_2026.csv (local times with their offsets), kelvra_logger_export_2026.csv "
        "(UTC and Fahrenheit, its one day exported twice counted once), brumal_downloads_2026.txt (UTC-6 all "
        "year) and tellvane_sensor_readings_2026.csv (UTC) on one clock in degrees C, and joined every serial and "
        "sensor id to its store through refrigerator_monitoring_roster_2026.xlsx, the replaced loggers at stores 207 "
        "and 302 in sequence.",
        "Took 2026 as the stores' local (Central) year and, at the ten pilot stores, the in-carton sensor from its "
        "first reading, the logger before it (standard PO-114 section 6.4).",
        "Fitted the vaccine's response on the weeks each pilot store's logger kept recording after its sensor's first "
        "reading: a first-order lag with each record holding over its ten minutes (section 6.3), %.1f, %.1f and %.1f "
        "minutes for Frostline, Kelvra and Brumal." % (tau["Frostline"], tau["Kelvra"], tau["Brumal"]),
        "Carried every logger record through its make's lag and counted ten minutes for each record whose vaccine "
        "temperature at its time stamp is above 8.0 °C (section 7.3), with the in-carton readings above 8.0: stores "
        "%s at 24 hours or more, %d nearest below at %d." % (join(cov), nb["store"], nb["hours"]),
        "For doses unaccounted for (section 8.2), took the YE 2025 count in "
        "vaccine_physical_inventory_ye2025_ye2026.xlsx, added meridale_vaccine_invoices_2026.csv deliveries "
        "(packages times vaccine_item_master_2026.xlsx doses per package, the Lindqvist stores' accounts before April by "
        "their former names) and transfers in from vaccine_store_transfers_2026.csv, took off "
        "pharmacy_vaccine_administrations_2026.csv, vaccine_writeoff_log_2026.csv and transfers out and the YE 2026 "
        "count, each flow between the two counts' own closing times, so the stores that counted on 30 December keep "
        "the next day's flows out of the year they close or in the year they open.",
        "Read the write-off log's multi-dose vial quantities before the %s inventory update as vials of ten doses "
        "(their cost is a vial's) and left meridale_credit_memos_2026.csv out, every credited unit being an expired "
        "2025-26 dose already written off on 1 July." % f["stated"]["inventory_update"],
        "For Brannon spend (section 9.2), took each invoice in brannon_service_history_2026-01_2027-01.xlsx once for "
        "work orders whose last visit is in 2026, added %.1f per cent sales tax to invoices dated before %s (the old "
        "platform's amounts are before tax, as its maintenance-only invoices at the agreement's Schedule B prices "
        "show), and split each two-store maintenance route by Schedule B's price for each store's unit."
        % (f["stated"]["tax_pct"], f["stated"]["platform"]),
        "Listed the stores at 24 hours or more: %s." % join(cov),
    ]
    for i, s in enumerate(steps, 1):
        o.append("%d. %s" % (i, s))
    o.append("")
    o.append("## 4. Deliverable Answers\n")
    o.append("### penwick_refrigerator_replacements_2027.xlsx\n")
    o.append("1. Stores that get a new refrigerator before the 2027 respiratory season: %s." % join(cov))
    o.append("2. Each store's 2026 hours with its vaccine above 8 °C, whole hours, and whether it gets a new "
             "refrigerator:")
    for n in order:
        o.append("   - Store %s %s: %d, %s" % (n, st[n]["town"], st[n]["hours"], "yes" if st[n]["replaced"] else "no"))
    o.append("3. Nearest store below the line: %d %s, %d hours, %d short." % (nb["store"], nb["town"], nb["hours"],
                                                                            nb["short_hours"]))
    o.append("4. Each store's 2026 vaccine doses its stock records leave unaccounted for, whole doses:")
    for n in order:
        o.append("   - Store %s: %d" % (n, st[n]["doses_unaccounted"]))
    o.append("5. Each store's 2026 refrigerator service spend with Brannon, whole dollars:")
    for n in order:
        o.append("   - Store %s: %s" % (n, "{:,}".format(st[n]["service_usd"])))
    o.append("\n### penwick_vaccine_hours_2026.svg\n")
    o.append("6. Horizontal bar chart of the thirty stores' 2026 hours with the vaccine above 8 °C, highest first, each "
             "bar labelled with its whole hours, a vertical line at 24 hours, the %d stores that get a new "
             "refrigerator in blue and the rest in grey, and the nearest store below the line named in the subtitle."
             % len(cov))
    open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")


if __name__ == "__main__":
    main()
