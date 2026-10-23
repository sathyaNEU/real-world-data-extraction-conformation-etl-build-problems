"""Writes task482's evidence pack from world.py and asks.py: the plants' press logs, the oxidizer historians, the
safety data sheet master, the Department's plant register, the stores issues, the hauler's manifests, the parts washer
tickets, the solvent vendors' payment lines, the two suppliers' 2026 invoices and Haldane's catalog, the stock counts,
and the two distractors (the documents are docs.py's)."""
import csv
import datetime as dt
import os

import world as W
import asks as A

FILES = {
    "rule": "deq_rule_18-4_draft_2027-02-19.pdf",
    "letter": "deq_information_request_2027-01-12.pdf",
    "register": "deq_printing_plants_register_2027-02.xlsx",
    "press": "press_material_use_2026.csv",
    "sds": "safety_data_sheet_master_2027-01.xlsx",
    "hist": "oxidizer_historian_hourly_2026.csv",
    "tests": "oxidizer_performance_tests_2017_2026.pdf",
    "issues": "stores_cleaning_issues_2026.csv",
    "manifests": "cantrell_bend_manifests_2026.csv",
    "profiles": "cantrell_bend_waste_profiles_2026.pdf",
    "tickets": "wexcombe_service_tickets_2026.csv",
    "payments": "solvent_vendor_payments_2026.csv",
    "corvane": "corvane_invoice_export_2026.csv",
    "haldane": "haldane_statement_2026.xlsx",
    "catalog": "haldane_catalog_2026-04.csv",
    "counts": "stock_counts_2026.csv",
    "presses": "deq_press_register_2026.csv",
    "ozone": "kestle_valley_ozone_design_values_2024_2026.csv",
}


def write_csv(path, head, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(head)
        n = 0
        for r in rows:
            w.writerow(r)
            n += 1
    return n


def _q(x):
    return ("%.1f" % x) if isinstance(x, float) else str(x)


# ---------------------------------------------------------------------------------------------------------------------
PRESS_COLS = ["facility_no", "plant_name", "press_id", "record_basis", "log_date", "shift", "job_no", "start_local",
              "end_local", "material_code", "quantity", "uom"]


def press_rows(e):
    rows = []
    for p in W.PLANTS:
        for r in e["plants"][p["code"]]["rows"]:
            rows.append((r["fac"], r["plant"], r["press"], r["basis"], r["date"].isoformat(), r["shift"], r["job"],
                         r["start"].strftime("%Y-%m-%d %H:%M"), r["end"].strftime("%Y-%m-%d %H:%M"), r["material"],
                         ("%d" % r["qty"]) if r["uom"] == "LB" else ("%.1f" % r["qty"]), r["uom"]))
    rows.sort(key=lambda x: (x[4], x[0], x[2], x[7], x[9]))
    return rows


HIST_COLS = ["unit_tag", "hour_beginning_utc", "mode", "chamber_degf", "exhaust_flow_scfm", "fan_speed_pct"]


def hist_rows(e):
    rows = []
    for p in W.PLANTS:
        if not p["ox"]:
            continue
        for tag, t, mode, temp, flow, sp in e["plants"][p["code"]]["hist"]:
            rows.append((tag, t.strftime("%Y-%m-%dT%H:%MZ"), mode, temp, flow, ("%.1f" % sp) if sp != "" else ""))
    rows.sort(key=lambda x: (x[1], x[0]))
    return rows


ISSUE_COLS = ["facility_no", "issue_no", "issue_date", "material_code", "quantity", "uom", "issued_to"]


def issue_rows(e):
    return [(x["fac"], x["no"], x["date"].isoformat(), x["material"], x["qty"], x["uom"], x["to"])
            for x in e["ask_a"]["issues"]]


MANIFEST_COLS = ["manifest_tracking_no", "ship_date", "generator_facility_no", "waste_profile", "containers",
                 "container_type", "net_weight", "weight_unit"]


def manifest_rows(e):
    return [(x["no"], x["date"].strftime("%m/%d/%Y"), x["fac"], x["profile"], x["containers"], x["ctype"], x["net"],
             x["unit"]) for x in e["ask_a"]["manifests"]]


TICKET_COLS = ["ticket_no", "service_date", "facility_no", "washer_id", "solvent_product", "fresh_added_gal",
               "spent_removed_gal"]


def ticket_rows(e):
    return [(x["ticket"], x["date"].isoformat(), x["fac"], x["washer"], x["product"], "%.1f" % x["added"],
             "%.1f" % x["removed"]) for x in e["ask_a"]["tickets"]]


PAYMENT_COLS = ["line", "facility_no", "vendor", "invoice_no", "invoice_date", "amount_usd", "gl_account",
                "description"]


def payment_rows(e):
    return [(x["line"], x["fac"], x["vendor"], x["inv"], x["date"].isoformat(), "%.2f" % x["amount"], x["gl"],
             x["desc"]) for x in e["ask_a"]["payments"]]


CORVANE_COLS = ["DOC_TYPE", "DOC_NO", "INVOICE_DATE", "SHIP_DATE", "ACCOUNT", "SHIP_TO", "ITEM", "DESCRIPTION", "QTY",
                "UOM", "UNIT_PRICE", "EXT_AMOUNT"]


def corvane_rows(e):
    out = []
    for x in e["ask_b"]["inv_a"]:
        out.append((x["doc"], x["no"], x["inv_date"].strftime("%Y%m%d"), x["ship"].strftime("%Y%m%d"), x["acct"],
                    x["name"], x["item"], x["desc"].upper(), x["qty"], x["uom"], "%.2f" % x["price"],
                    "%.2f" % (x["qty"] * x["price"])))
    return out


CATALOG_COLS = ["item_no", "product_code", "description", "category", "sold_by", "pack_size", "replaces_item",
                "effective_from"]


def catalog_rows():
    cat = {"COATING": "Coatings", "ADHESIVE": "Adhesives", "PRESS WASH": "Press washes", "CLEANING": "Cleaning"}
    out = []
    for item, code, pack, sold, rep in A.CATALOG:
        out.append((item, code, "%s, %s" % (W.PRODUCTS[code][0], ("%d gal" % pack) if sold == "GAL" else
                                            ("%d lb drum" % pack)), cat[W.PRODUCTS[code][2]], sold, pack, rep,
                    "2026-04-01"))
    return out


COUNT_COLS = ["facility_no", "count_date", "material_code", "quantity", "uom"]


def count_rows(e):
    rows = [(x["fac"], x["date"].isoformat(), x["material"], x["qty"], x["uom"]) for x in e["ask_b"]["counts"]
            if x["qty"] > 0 or x["date"].month == 1]
    rows.sort(key=lambda x: (x[0], x[1], x[2]))
    return rows


PRESSES_COLS = ["facility_no", "press_id", "press_type", "manufacturer", "web_width_in", "max_speed_fpm",
                "year_installed", "exhaust_to"]
PRESS_KIND = {"F": ("Central impression flexographic", ("Vellmar", "Kessner", "Arbo-Lindt")),
              "G": ("Rotogravure", ("Kessner", "Ordway")), "L": ("Laminator", ("Ordway", "Halberg")),
              "C": ("Coater", ("Halberg",))}


def presses_rows():
    out = []
    for p in W.PLANTS:
        r = W.rng_for("pressreg", p["code"])
        for i, pid in enumerate(p["presses"]):
            kind, makes = PRESS_KIND[pid[0]]
            if p["code"] in ("BRI", "PEL") or (p["code"] == "IVE"):
                kind = "Narrow-web flexographic" if pid[0] in "LF" else kind
            yr = int(r.integers(2003, 2023))
            if p["code"] in ("ASH", "ELS", "GAR", "MER", "NOR") and i >= 2:
                yr = {"ASH": 2019, "ELS": 2018, "GAR": 2019, "MER": 2019, "NOR": 2018}[p["code"]] + (i - 2)
            elif p["code"] in ("ASH", "ELS", "GAR", "MER", "NOR"):
                yr = min(yr, 2016)
            out.append((p["fac"], pid, kind, makes[int(r.integers(0, len(makes)))],
                        int(r.choice([10, 13, 17, 42, 52, 60])) if pid[0] in "LF" and p["code"] in ("BRI", "PEL", "IVE")
                        else int(r.choice([42, 52, 60, 65])), int(r.choice([800, 1000, 1200, 1500, 1800])), yr,
                        p["ox"]["tag"] if p["ox"] else "Building exhaust"))
    return out


OZONE_COLS = ["site_id", "site_name", "year", "fourth_high_8hr_ppb", "design_value_ppb", "complete"]


def ozone_rows():
    sites = [("57-031-0012", "Kestle Valley North"), ("57-031-0020", "Ashcombe Fire Station"),
             ("57-031-0034", "Merrion Water Plant"), ("57-031-0041", "Ravensbrook School"),
             ("57-089-0007", "Upper Kestle")]
    out = []
    r = W.rng_for("ozone")
    for sid, name in sites:
        base = float(r.uniform(68, 76))
        vals = []
        for y in (2024, 2025, 2026):
            v = int(round(base + r.normal(0, 2.5)))
            vals.append(v)
            dv = int(sum(vals[-3:]) / 3) if len(vals) == 3 else ""
            out.append((sid, name, y, v, dv, "Y"))
    return out


# ---------------------------------------------------------------------------------------------------------------------
def write_sds(path):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Products"
    head = ["Product code", "Product name", "Supplier", "Product type", "Density (lb/gal)", "VOC basis", "VOC",
            "Water (vol %)", "Exempt compounds (vol %)", "Exempt compounds", "SDS revision", "Revision date"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    sup = {"A": W.SUPPLIERS["A"], "B": W.SUPPLIERS["B"], "KL": W.WASHERS["KL"], "SS": W.WASHERS["SS"]}
    rev_date = {code: d for code, rv, d, _, _ in W.REVISIONS if W.CURRENT_REV.get(code) == rv}
    basis = {"WT": "% by weight", "LWE": "lb/gal less water and exempt"}
    for code in sorted(W.PRODUCTS):
        name, s, kind, den, b, val, wv, ev, exn, sold = W.PRODUCTS[code]
        ws.append([code, name, sup[s], kind.title(), den, basis[b], val, wv if b == "LWE" else None,
                   ev if ev else None, exn or None, W.CURRENT_REV.get(code, 1),
                   rev_date.get(code, dt.date(2021, 3, 1) if s == "A" else dt.date(2022, 7, 1))])
    for row in ws.iter_rows(min_row=2):
        row[4].number_format = "0.00"
        row[6].number_format = "0.00"
        row[11].number_format = "yyyy-mm-dd"
    for i, wd in enumerate([13, 38, 30, 12, 10, 26, 8, 9, 11, 12, 9, 12]):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.freeze_panes = "B2"
    rl = wb.create_sheet("Revision log")
    rl.append(["Product code", "Revision", "Effective from", "Change"])
    for c in rl[1]:
        c.font = Font(bold=True)
    for code, rv, d, what, _ in sorted(W.REVISIONS, key=lambda x: (x[2], x[0])):
        rl.append([code, rv, d, what])
    for row in rl.iter_rows(min_row=2):
        row[2].number_format = "yyyy-mm-dd"
    for col, wd in zip("ABCD", (13, 9, 13, 96)):
        rl.column_dimensions[col].width = wd
    nt = wb.create_sheet("Notes")
    for line in (["Safety data sheet master, all plants' returns, as compiled 26 January 2027."],
                 ["VOC is as each sheet states it: per cent by weight of the product, or pounds per gallon of the "
                  "product less water and exempt compounds."]):
        nt.append(line)
    nt.column_dimensions["A"].width = 110
    wb.save(path)
    return len(W.PRODUCTS)


def write_register(path, e):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Plants"
    ws.append(["Facility no.", "Plant", "Town", "Operation", "Presses", "Oxidizer", "Parts washers",
               "Carbon content of VOC (lb C per lb VOC)", "Former name"])
    for p in W.PLANTS:
        ws.append([p["fac"], p["name"], p["town"], p["what"], len(p["presses"]), "Yes" if p["ox"] else "No",
                   A.CLEAN[p["code"]][3], p["ox"]["cf"] if p["ox"] else None,
                   ("%s (facility %s) until 30 April 2026" % (p["old_name"], p["old_fac"])) if p.get("old_name")
                   else None])
    ox = wb.create_sheet("Oxidizers")
    ox.append(["Facility no.", "Plant", "Historian tag", "Manufacturer", "Type", "Installed",
               "Combustion chamber set point (F)", "Residence time (s)", "Fan drive", "Rated airflow (scfm)",
               "Minimum fan speed (%)", "Historian logs", "Permit no.", "Destruction condition"])
    for p in W.PLANTS:
        o = p["ox"]
        if not o:
            continue
        drive = "Fixed speed" if o["fan"] == "FIXED" else ("Variable speed (from %d)" % o["vfd_from"] if
                                                           o.get("vfd_from") else "Variable speed")
        tag = o["tag"] if not o.get("old_tag") else "%s (%s until 15 June 2026)" % (o["tag"], o["old_tag"])
        ox.append([p["fac"], p["name"], tag, W.VENDORS[o["vendor"]], "Regenerative thermal oxidizer, three chambers",
                   o["installed"], 1550, 1.0, drive, int(round(o["Q"], -1)),
                   int(o["qmin"] * 100) if o["fan"] == "VFD" else None,
                   "Exhaust flow (scfm)" if o["logs"] == "FLOW" else "Fan speed (% of rated)",
                   "AQ-%s-%d" % (p["fac"], 2000 + o["installed"] % 100 * 3 % 97),
                   "Not less than 95 per cent destruction of the VOC delivered to the oxidizer, shown by a performance "
                   "test at maximum production within 180 days of start-up and every five years after"])
    cp = wb.create_sheet("Capture")
    cp.append(["Facility no.", "Plant", "Capture determination", "Date", "Capture efficiency (%)", "Notes"])
    for p in W.PLANTS:
        o = p["ox"]
        if not o:
            continue
        r = W.rng_for("capture", p["code"])
        d = dt.date(int(r.integers(2019, 2025)), int(r.integers(1, 12)), int(r.integers(1, 28)))
        if o["cap"] == "PTE":
            cp.append([p["fac"], p["name"], "Permanent total enclosure verified (EPA Method 204)", d, 100.0,
                       "Natural draft openings within Method 204 criteria; inward face velocity above 200 fpm"])
        else:
            cp.append([p["fac"], p["name"], "Capture efficiency test, temporary total enclosure (EPA Methods 204 "
                       "and 204B to 204F)", d, round(o["CE"] * 100, 1), "Three runs at maximum production"])
    for sh, widths in ((ws, (10, 30, 12, 52, 8, 9, 8, 14, 44)), (ox, (10, 30, 26, 22, 34, 9, 12, 9, 22, 11, 10, 20, 14,
                                                                     60)), (cp, (10, 30, 56, 11, 12, 60))):
        for c in sh[1]:
            c.font = Font(bold=True)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for i, wd in enumerate(widths):
            sh.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
        sh.freeze_panes = "C2"
    for row in cp.iter_rows(min_row=2):
        row[3].number_format = "yyyy-mm-dd"
        row[4].number_format = "0.0"
    for row in ws.iter_rows(min_row=2):
        row[7].number_format = "0.000"
    wb.save(path)
    return len(W.PLANTS)


def write_haldane(path, e):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Statement detail"
    ws.append(["Haldane Coatings & Adhesives: customer statement detail, Kestle Valley accounts, documents dated "
               "1 January 2026 to 31 January 2027"])
    ws["A1"].font = Font(bold=True)
    ws.append(["Doc type", "Doc no.", "Doc date", "Ship date", "Account", "Ship to", "Item", "Description", "Qty",
               "Unit price", "Amount"])
    for c in ws[2]:
        c.font = Font(bold=True)
    n = 0
    for x in e["ask_b"]["stmt_b"]:
        ws.append([x["doc"], x["no"], x["date"], x["ship"], x["acct"], x["name"], x["item"], x["desc"], x["qty"],
                   x["price"], round(x["qty"] * x["price"], 2)])
        n += 1
    for row in ws.iter_rows(min_row=3):
        row[2].number_format = "mm/dd/yyyy"
        row[3].number_format = "mm/dd/yyyy"
        row[9].number_format = "#,##0.00"
        row[10].number_format = "#,##0.00"
    for col, wd in zip("ABCDEFGHIJK", (8, 12, 11, 11, 9, 30, 7, 26, 8, 10, 12)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A3"
    wb.save(path)
    return n


# ---------------------------------------------------------------------------------------------------------------------
def build_pack(out, e):
    import docs as DC
    f = lambda k: os.path.join(out, FILES[k])
    n = {}
    n["press"] = write_csv(f("press"), PRESS_COLS, press_rows(e))
    n["hist"] = write_csv(f("hist"), HIST_COLS, hist_rows(e))
    n["issues"] = write_csv(f("issues"), ISSUE_COLS, issue_rows(e))
    n["manifests"] = write_csv(f("manifests"), MANIFEST_COLS, manifest_rows(e), crlf=True)
    n["tickets"] = write_csv(f("tickets"), TICKET_COLS, ticket_rows(e))
    n["payments"] = write_csv(f("payments"), PAYMENT_COLS, payment_rows(e))
    n["corvane"] = write_csv(f("corvane"), CORVANE_COLS, corvane_rows(e), crlf=True)
    n["catalog"] = write_csv(f("catalog"), CATALOG_COLS, catalog_rows())
    n["counts"] = write_csv(f("counts"), COUNT_COLS, count_rows(e))
    n["presses"] = write_csv(f("presses"), PRESSES_COLS, presses_rows())
    n["ozone"] = write_csv(f("ozone"), OZONE_COLS, ozone_rows())
    n["sds"] = write_sds(f("sds"))
    n["register"] = write_register(f("register"), e)
    n["haldane"] = write_haldane(f("haldane"), e)
    n["tests"] = DC.write_tests(f("tests"), e)
    n["profiles"] = DC.write_profiles(f("profiles"), e)
    DC.write_rule(f("rule"))
    DC.write_letter(f("letter"))
    return n
