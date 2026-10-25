"""The pack's data files, each written as the system that issues it writes its records."""
import csv
import datetime as dt

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

import ash as A
import reagent as RG
import world as W

PERMIT = {}            # boiler id -> permit number
for i, b in enumerate(W.BOILERS):
    PERMIT["%s-%d" % (b["site"], b["unit"])] = "NPA/CB/%04d" % (311 + 37 * i)
UNIT_NAME = {"S01": ("Boiler 1", "Boiler 2"), "S09": ("No. 1 boiler", "No. 2 boiler")}
SUP_CUST = {}          # (supplier, site) -> customer code


def unit_label(bid):
    site, u = bid.split("-")
    if site in UNIT_NAME:
        return UNIT_NAME[site][int(u) - 1]
    return "Main boiler"


def _csv(path, header, rows, crlf=True):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


def iso(d):
    return W.day(d).isoformat()


def dmy(d):
    x = W.day(d)
    return "%02d/%02d/%04d" % (x.day, x.month, x.year)


def _sheet(ws, header, rows, widths, fmts=None):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    for r in rows:
        ws.append(r)
    for i, wd in enumerate(widths):
        ws.column_dimensions[chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)].width = wd
    if fmts:
        for col, f in fmts.items():
            for cell in ws[col][1:]:
                cell.number_format = f
    ws.freeze_panes = "A2"


def customer_codes(w):
    rng = np.random.default_rng(W.SEED + 81)
    pref = {"Ormthwaite Colliery": "OT-", "Brisgarth Main Colliery": "BG", "Ostmouth Coal Imports": "OCI/",
            "Zellfold Fuels": "ZF"}
    for sup in W.SUPPLIERS:
        used = set()
        for site in sorted(w.sites):
            while True:
                n = int(rng.integers(1000, 9999))
                if n not in used:
                    used.add(n)
                    break
            SUP_CUST[(sup, site)] = "%s%d" % (pref[sup], n)


POINT = {"Ormthwaite Colliery": lambda f: f,
         "Brisgarth Main Colliery": lambda f: f.upper() + " - YARD",
         "Ostmouth Coal Imports": lambda f: f.split()[0] + " sidings",
         "Zellfold Fuels": lambda f: " ".join(f.split()[:2]) + " (coal)"}
FLEET = {"Ormthwaite Colliery": "OC", "Brisgarth Main Colliery": "BMH", "Zellfold Fuels": "ZF"}
LABS = {"Ormthwaite Colliery": "Ormthwaite Colliery laboratory", "Brisgarth Main Colliery": "Tavscar Fuel Analysts",
        "Ostmouth Coal Imports": "Ostmouth dockside laboratory", "Zellfold Fuels": "Tavscar Fuel Analysts"}


def coal_csv(path, w):
    """the four suppliers' statements to the Directorate, collated: one row per truck or wagon, with the certificate
    of the lot it was dispatched in (a day's dispatch to a customer, or a train) and the laboratory's analysis as
    received; Ostmouth writes dates day first, the others ISO; a certificate corrected after a check sample carries
    its revision letter and the corrected analysis (the sulphur is unchanged on every re-issue)"""
    rng = np.random.default_rng(W.SEED + 82)
    fleets = {s: ["%s %03d" % (pre, n) for n in rng.choice(np.arange(11, 400), int(rng.integers(45, 90)), replace=False)]
              for s, pre in FLEET.items()}
    wagons = ["%d" % n for n in rng.choice(np.arange(30001, 32999), 260, replace=False)]
    by_lot = {}
    for x in w.lots:
        by_lot.setdefault(x["lot"], []).append(x)
    order = sorted(by_lot, key=lambda k: (by_lot[k][0]["supplier"], by_lot[k][0]["dispatched"], by_lot[k][0]["site"]))
    cert = {s: int(rng.integers(20000, 60000)) for s in W.SUPPLIERS}
    dn = {s: int(rng.integers(100000, 400000)) for s in W.SUPPLIERS}
    rows = []
    w.coal_certs = {}
    for k in order:
        xs = by_lot[k]
        x0 = xs[0]
        sup = x0["supplier"]
        cert[sup] += int(rng.integers(1, 4))
        c = "%s-%d" % (W.SUP_CODE[sup], cert[sup])
        fmt = dmy if sup == "Ostmouth Coal Imports" else iso
        issued = x0["dispatched"] + int(rng.integers(1, 3))
        ash, carbon, gcv = x0["ash"], x0["c"], x0["gcv"]
        rev = ""
        if x0["reissued"]:
            rev = "A"
            issued += int(rng.integers(9, 40))
            ash = float(np.round(ash + rng.choice([-1, 1]) * rng.uniform(0.4, 1.4), 1))
            carbon = float(np.round(carbon + rng.choice([-1, 1]) * rng.uniform(0.4, 1.6), 1))
            gcv = float(np.round(gcv + rng.choice([-1, 1]) * rng.uniform(0.1, 0.5), 2))
        w.coal_certs[k] = dict(cert=c, rev=rev)
        consign = "OCI/CN/%05d" % (dn[sup] % 100000) if x0["rail"] else None
        for x in xs:
            dn[sup] += 1
            if x["rail"]:
                note, veh = consign, "Wagon " + str(rng.choice(wagons))
            else:
                note, veh = "%d" % dn[sup], str(rng.choice(fleets[sup]))
            rows.append([sup, c, rev, fmt(issued), SUP_CUST[(sup, x["site"])], POINT[sup](w.sites[x["site"]]["firm"]),
                         note, fmt(x["dispatched"]), fmt(x["received"]), "Rail" if x["rail"] else "Road", veh,
                         "%.2f" % x["t"], "%.1f" % x["tm"], "%.1f" % ash, "%.2f" % x["s"], "%.1f" % carbon,
                         "%.2f" % gcv, LABS[sup]])
    header = ["Supplier", "Certificate No", "Rev", "Issued", "Customer Code", "Delivery Point", "Delivery Note",
              "Dispatched", "Received", "Transport", "Vehicle / Wagon", "Net Tonnes", "Total Moisture % (ar)",
              "Ash % (ar)", "Total Sulphur % (ar)", "Carbon % (ar)", "Gross CV MJ/kg (ar)", "Laboratory"]
    return _csv(path, header, rows)


def supplier_customers_csv(path, w):
    rows = []
    for (sup, site), code in sorted(SUP_CUST.items()):
        if not any(x["site"] == site and x["supplier"] == sup for x in w.lots):
            continue
        rows.append([sup, code, w.sites[site]["firm"], site_permits(site)])
    return _csv(path, ["Supplier", "Customer Code", "Customer", "Permit Numbers"], rows)


def site_permits(site):
    return "; ".join(PERMIT[b] for b in sorted(PERMIT) if b.startswith(site + "-"))


def returns_xlsx(path, w):
    """the operators' quarterly returns: quarters 1 and 2 in the 2019 template, 3 and 4 in the 2026 template"""
    wb = Workbook()
    wb.remove(wb.active)
    by = {}
    for r in w.returns:
        by.setdefault(r["quarter"], []).append(r)
    for q in (1, 2, 3, 4):
        ws = wb.create_sheet("Q%d 2026" % q)
        rows = []
        for r in sorted(by[q], key=lambda x: PERMIT[x["boiler"]]):
            site = r["site"]
            first = r["unit"] == 1
            coal_open = r["coal_open"] if first else None
            coal_close = r["coal_close"] if first else None
            if q <= 2:
                rows.append([PERMIT[r["boiler"]], w.sites[site]["firm"], unit_label(r["boiler"]), r["coal_burned"],
                             r["hours"], r["steam"], r["oil"], coal_open, coal_close, r["ls_open"], r["ls_close"]])
            else:
                rows.append([PERMIT[r["boiler"]], unit_label(r["boiler"]), w.sites[site]["firm"], r["hours"],
                             r["coal_burned"], r["oil"], r["steam"], coal_open, coal_close, r["ls_open"], r["ls_close"]])
        if q <= 2:
            header = ["Permit No", "Operator", "Boiler", "Coal burned (t)", "Firing hours", "Steam raised (t)",
                      "Gas oil for start-up (t)", "Coal stock at start of quarter (t)",
                      "Coal stock at end of quarter (t)", "Reagent held at start of quarter (t)",
                      "Reagent held at end of quarter (t)"]
        else:
            header = ["Permit reference", "Unit", "Operator", "Operating hours", "Fuel fired: coal (tonnes)",
                      "Fuel fired: gas oil (tonnes)", "Steam (tonnes)", "Coal yard, opening (tonnes)",
                      "Coal yard, closing (tonnes)", "Limestone in silo, opening (tonnes)",
                      "Limestone in silo, closing (tonnes)"]
        _sheet(ws, header, rows, [14, 30, 13, 13, 11, 12, 12, 14, 14, 14, 14])
    ws = wb.create_sheet("Notes")
    for line in ["Quarterly returns under permit condition 7 (fuel, steam and reagent), Northern Priority Area, 2026.",
                 "Quarters 1 and 2 were filed on the 2019 return template, quarters 3 and 4 on the 2026 template.",
                 "Where two boilers share a site, the coal yard is reported once, on the first boiler's row.",
                 "Stocks are as measured or estimated by the operator at the end of the quarter's last day.",
                 "Compiled by the Air Quality Directorate from the returns as filed by 31 January 2027."]:
        ws.append([line])
    ws.column_dimensions["A"].width = 110
    wb.save(path)
    return sum(len(v) for v in by.values())


def tickets_csv(path, w):
    rng = np.random.default_rng(W.SEED + 83)
    acct = {}
    for b in w.B:
        q = RG.SITE_QUARRY[b["site"]]
        acct.setdefault((q, b["site"]), ("BSQ-%d" % int(rng.integers(2000, 2999))) if q == "Bromscar Quarry"
                        else A.MOORSIDE_NAMES[b["site"]].upper())
    w.ls_accounts = acct
    stamped = []
    for x in w.tickets:
        tare = float(np.round(rng.uniform(13.8, 15.2), 2))
        stamped.append((x, tare, int(rng.integers(6 * 60, 17 * 60))))
    stamped.sort(key=lambda v: (v[0]["quarry"], v[0]["day"], v[2]))
    rows = []
    tno = {"Bromscar Quarry": 160000, "Molhope Lime and Stone": 7300}
    for x, tare, minute in stamped:
        q = x["quarry"]
        tno[q] += 1
        rows.append([q, ("BS%d" % tno[q]) if q.startswith("Bromscar") else ("MH/%05d" % tno[q]), iso(x["day"]),
                     "%02d:%02d" % divmod(minute, 60), acct[(q, x["site"])], _point(x["boiler"]),
                     "%.2f" % (x["t"] + tare), "%.2f" % tare, "%.2f" % x["t"], "Limestone 0-2 mm (FGD grade)"])
    header = ["Quarry", "Ticket", "Date", "Time", "Account", "Delivery Point", "Gross t", "Tare t", "Net t",
              "Product"]
    return _csv(path, header, rows)


def _point(bid):
    site, u = bid.split("-")
    if site in UNIT_NAME:
        return "Absorber %s silo" % u
    return "Scrubber silo"


def certificates_xlsx(path, w):
    wb = Workbook()
    wb.remove(wb.active)
    rng = np.random.default_rng(W.SEED + 84)
    for q, short in (("Bromscar Quarry", "Bromscar weekly"), ("Molhope Lime and Stone", "Molhope weekly")):
        ws = wb.create_sheet(short)
        rows = []
        for wk in range(1, 54):
            mon = dt.date.fromisocalendar(2026, wk, 1)
            caco3 = float(w.purity[q][wk])
            rows.append([wk, mon.isoformat(), caco3, float(np.round(max(0.6, 98.6 - caco3 - rng.uniform(0.3, 1.6)), 1)),
                         float(np.round(rng.uniform(1.5, 4.0), 1)), float(np.round(rng.uniform(88, 96), 0))])
        _sheet(ws, ["ISO week", "Week commencing", "CaCO3 %", "Acid insoluble residue %", "Moisture %",
                    "Passing 63 micron %"], rows, [9, 15, 10, 13, 11, 12], fmts={"C": "0.0", "D": "0.0", "E": "0.0"})
    ws = wb.create_sheet("Delivery points")
    rows = []
    for (q, site), a in sorted(w.ls_accounts.items()):
        for b in sorted(PERMIT):
            if b.startswith(site + "-"):
                rows.append([q, a, w.sites[site]["firm"], _point(b), PERMIT[b]])
    _sheet(ws, ["Quarry", "Account", "Site", "Delivery Point", "Permit No"], rows, [26, 34, 34, 18, 14])
    ws = wb.create_sheet("Notes")
    for line in ["Each quarry certifies its FGD-grade limestone weekly: one composite sample drawn at the loading shovel",
                 "over the ISO week (Monday to Sunday), analysed by the quarry's accredited laboratory, and the result",
                 "applies to every delivery made in that week. Week 53 of 2026 runs from 28 December 2026.",
                 "Composition is stated on the limestone as delivered, its moisture included; the moisture is stated",
                 "for handling.",
                 "Delivery points are mapped to permit numbers by the Air Quality Directorate from the quarries'",
                 "customer lists and the permit files."]:
        ws.append([line])
    ws.column_dimensions["A"].width = 110
    wb.save(path)
    return len(rows)


def permits_xlsx(path, w):
    rng = np.random.default_rng(W.SEED + 85)
    wb = Workbook()
    ws = wb.active
    ws.title = "Register"
    rows = []
    vend = {}
    for b in w.B:
        vend[b["id"]] = "Kellfold Process Systems" if int(b["site"][1:]) % 3 else "Lundsett Absorber Engineering"
        rows.append([PERMIT[b["id"]], w.sites[b["site"]]["firm"], unit_label(b["id"]), b["industry"].capitalize(),
                     "Pulverised coal" if b["type"] == "PF" else "Chain grate stoker", b["mwth"],
                     int(rng.integers(1988, 2012)), "Wet limestone scrubber", vend[b["id"]],
                     int(rng.integers(2019, 2024)), 100 * b["design"], 100 * b["ash_ret"], "Annual test (periodic)"])
    w.vendor = vend
    _sheet(ws, ["Permit No", "Operator", "Unit", "Sector", "Boiler type", "Rated thermal input (MWth)",
                "Boiler commissioned", "SO2 abatement", "Scrubber supplier", "Scrubber commissioned",
                "Design SO2 removal (%)", "Sulphur retained in ash (% of sulphur fired)", "SO2 monitoring"],
           rows, [13, 34, 13, 15, 18, 12, 11, 20, 28, 11, 11, 14, 20], fmts={"F": "0.0", "K": "0.0", "L": "0.0"})
    ws = wb.create_sheet("Conditions")
    for line in ["Standard conditions for permitted coal boilers, Northern Priority Area (summary).",
                 "C3  Burn only coal delivered with a supplier's analysis certificate for each lot.",
                 "C5  Operate the sulphur dioxide abatement plant whenever the boiler fires coal, so far as practicable.",
                 "C7  File a quarterly return of fuel burned, steam raised and fuel and reagent held, by the end of the "
                 "month after the quarter.",
                 "C9  Keep fuel and reagent delivery records for six years.",
                 "C11 Commission an accredited laboratory to test the scrubber's performance once a year at not less "
                 "than 60 per cent of the boiler's rating."]:
        ws.append([line])
    ws.column_dimensions["A"].width = 120
    wb.save(path)
    return len(rows)


def ash_files(paths, w):
    E = w.ash_exports
    rng = np.random.default_rng(W.SEED + 86)
    # Whinmoss's invoice lines
    wb = Workbook()
    ws = wb.active
    ws.title = "Invoice lines"
    rows = []
    inv = 61000
    rate = {"Bottom ash": 31.40, "Fly ash (conditioned)": 33.10, "Fly ash (dry)": 21.75,
            "General waste": 24.60, "Skip hire": 196.00, "Scrap metal": 38.00}
    by_month = {}
    for r in E["moorside"]:
        by_month.setdefault((r["site"], W.day(r["day"]).month if r["day"] <= 364 else 13), []).append(r)
    acct = {s: "WMH%04d" % (100 + 7 * i) for i, s in enumerate(sorted(w.sites))}
    for key in sorted(by_month, key=lambda k: (k[1], k[0])):
        inv += 1
        for n, r in enumerate(sorted(by_month[key], key=lambda x: (x["day"], x["ref"])), start=1):
            svc = r["service"]
            rt = next(v for k, v in rate.items() if svc.startswith(k))
            rows.append(["INV-%d" % inv, iso(r["day"]), acct[r["site"]], A.MOORSIDE_NAMES[r["site"]], n, svc,
                         r["qty"], r["unit"], rt, float(np.round(r["qty"] * rt, 2)), r["ref"]])
    _sheet(ws, ["Invoice No", "Line date", "Account", "Customer", "Line", "Service", "Quantity", "Unit", "Rate",
                "Net", "Reference"], rows, [12, 11, 10, 34, 5, 46, 9, 5, 7, 10, 13],
           fmts={"G": "0.00", "I": "0.00", "J": "#,##0.00"})
    wb.save(paths["moorside"])
    # Carnhope's job sheet
    trows = []
    for r in E["tolland"]:
        tare = int(rng.integers(11800, 14600))
        trows.append([r["job"], iso(r["day"]), w.sites[r["site"]]["firm"], r["material"], r["dest"],
                      r["net_kg"] + tare, tare, r["net_kg"]])
    _csv(paths["tolland"], ["Job No", "Date", "Site", "Material", "Destination", "Gross kg", "Tare kg", "Net kg"],
         trows)
    # Pellrigg's dockets
    wb = Workbook()
    ws = wb.active
    ws.title = "Dockets"
    grows = []
    for r in E["greave"]:
        grows.append([r["job"], iso(r["day"]), w.sites[r["site"]]["firm"].upper(), r["material"], r["dest"],
                      r["net_t"]])
    _sheet(ws, ["Docket", "Date", "Customer", "Material", "Taken to", "Net t"], grows, [13, 11, 40, 22, 26, 8],
           fmts={"F": "0.00"})
    wb.save(paths["greave"])
    # the Directorate's cross-reference of the contractors' customer names
    xrows = []
    for s in sorted(w.sites):
        xrows.append(["Whinmoss Waste Haulage", A.MOORSIDE_NAMES[s], s and site_permits(s)])
        xrows.append([A.LOCAL[s], w.sites[s]["firm"] if A.LOCAL[s] == "Carnhope Skips" else w.sites[s]["firm"].upper(),
                      site_permits(s)])
    _csv(paths["xref"], ["Contractor", "Customer as recorded", "Permit Numbers"], xrows)
    return len(rows), len(trows), len(grows)


def ambient_csv(path):
    rng = np.random.default_rng(W.SEED + 87)
    st = ["Quarholt Road", "Eskfold Lock", "Nethstead Park", "Velthwaite Hill", "Umbgarth Centre", "Ulvdale Green",
          "Pridwold School", "Wendscar Bridge"]
    rows = []
    for s in st:
        base = rng.uniform(4.0, 11.0)
        for m in range(1, 13):
            v = base * (1 + 0.35 * np.cos(2 * np.pi * (m - 1) / 12)) * rng.lognormal(0, 0.12)
            rows.append([s, "2026-%02d" % m, "%.1f" % v, "%.0f" % rng.uniform(86, 100)])
    return _csv(path, ["Station", "Month", "SO2 monthly mean (ug/m3)", "Data capture (%)"], rows)


def national_coal_json(path):
    """the statistics office's provisional 2025 coal consumption by sector, as its open data portal serves it"""
    import json
    rows = [("Electricity generation", 4812), ("Iron and steel", 1106), ("Cement and lime", 644),
            ("Paper, printing and publishing", 297), ("Food, drink and tobacco", 238), ("Chemicals", 205),
            ("Textiles and leather", 94), ("Other industry", 167), ("Public administration and health", 71),
            ("Domestic", 412), ("Commercial and other", 58)]
    doc = {"dataset": "ENR-COAL-02", "title": "Coal consumption by sector, 2025 (provisional)",
           "unit": "thousand tonnes", "source": "National Statistics Office, energy balance",
           "released": "2026-06-25", "status": "provisional",
           "data": [{"sector": s, "year": 2025, "value": v} for s, v in rows]}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    return len(rows)
