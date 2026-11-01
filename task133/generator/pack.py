"""Writes the data files of target/ (task133 architecture 4) from the world."""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

import params as P
from io_util import write_csv, save_xlsx

WB = "weighbridge_tickets_port_kowhai_FY2026.csv"
SC = "log_scaling_port_kowhai_FY2026.csv"
FLEET = "fleet_register_2026-06-30.xlsx"
PLAN = "harvest_plan_FY2028.xlsx"
INV = "cartage_invoices_FY2026.csv"
DOCK = "mill_dockets_FY2026.csv"
MWB = "mill_weighbridge_logs_FY2026.csv"
PRICES = "export_log_prices_FY2026.csv"
VESSELS = "port_kowhai_vessel_calls_FY2026.csv"
CLOSURES = "forest_road_closures_FY2026.csv"


def write_weighbridge(W, out):
    rng = np.random.default_rng(P.SEED + 11)
    tno = 2071340
    rows = []
    for r in W.loads:
        tno += int(rng.integers(1, 7))
        r["ticket"] = str(tno)
        rows.append([r["ticket"], r["wb_time"].strftime("%d/%m/%Y %H:%M"), r["rego"], "MATIRI", r["forest"], r["grade"],
                     f"{r['net']:.2f}"])
    write_csv(os.path.join(out, WB), ["ticket_no", "weighed_at", "vehicle_rego", "supplier", "forest_code", "product_code",
                                      "net_tonnes"], rows)


def write_scaling(W, out):
    rng = np.random.default_rng(P.SEED + 12)
    sref = 58840
    rows = []
    for r in sorted(W.loads, key=lambda x: x["scale_time"]):
        sref += int(rng.integers(1, 4))
        rows.append([f"SC{sref}", r["scale_time"].strftime("%Y-%m-%d %H:%M:%S"), r["rego"], r["grade"], r["pieces"],
                     f"{r['jas']:.3f}", str(rng.choice(["JH", "MT", "RP", "SW"]))])
    write_csv(os.path.join(out, SC), ["scale_ref", "scaled_at", "truck_rego", "grade", "pieces", "jas_m3", "scaler"], rows)


def write_fleet(W, out):
    wb = Workbook()
    ws = wb.active
    ws.title = "Fleet"
    ws.append(["Matiri Forest Products Limited - contracted log cartage fleet as at 30 June 2026"])
    ws.append([])
    hdr = ["Unit", "Carrier", "Registration", "Previous registration", "Trailer registration", "Configuration", "Year",
           "Tare (t)", "50MAX permit", "Full bunks 3.9 m logs (JAS m3)", "Full bunks 5.9 m logs (JAS m3)",
           "Full bunks 12.1 m logs (JAS m3)"]
    ws.append(hdr)
    for c in ws[3]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True)
    for u in W.units:
        ws.append([u["unit"], P.CARRIERS[u["carrier"]], u["rego"], u["prev"] or None, u["trailer"], u["config"], u["year"],
                   u["tare"], "Y" if u["eligible"] else "N", u["cap"][3.9], u["cap"][5.9], u["cap"][12.1]])
    for col, w in zip("ABCDEFGHIJKL", (9, 28, 13, 13, 13, 24, 6, 9, 8, 13, 13, 13)):
        ws.column_dimensions[col].width = w
    save_xlsx(wb, os.path.join(out, FLEET), "Cartage fleet register", "Stacey MacKay", "2026-07-03T21:15:00Z")


def write_plan(W, out):
    wb = Workbook()
    ws = wb.active
    ws.title = "Export"
    ws.append(["Harvest plan FY2028 (1 July 2027 to 30 June 2028) - export logs, tonnes"])
    ws.append(["Approved by the Board 18 September 2026"])
    ws.append([])
    ws.append(["Forest"] + [P.GRADES[g]["name"] for g in P.GRADE_ORDER] + ["Total"])
    for c in ws[4]:
        c.font = Font(bold=True)
    for fc, f in P.FORESTS.items():
        vals = [W.plan[(fc, g)] for g in P.GRADE_ORDER]
        ws.append([f["name"]] + vals + [sum(vals)])
    ws2 = wb.create_sheet("Domestic")
    ws2.append(["Harvest plan FY2028 - domestic sawlogs and pulp, tonnes"])
    ws2.append([])
    ws2.append(["Mill"] + ["Tonnes"])
    for mc, name in P.MILLS.items():
        ws2.append([name, {"MSM": 54000, "AHT": 40000, "HBL": 22000}[mc]])
    ws.column_dimensions["A"].width = 26
    save_xlsx(wb, os.path.join(out, PLAN), "Harvest plan FY2028", "Nicole Clifford", "2026-09-19T02:05:00Z")


def write_invoices(W, out):
    rng = np.random.default_rng(P.SEED + 13)
    by_month = {}
    for ln in W.invoice_lines:
        d = ln["load"]["date"]
        by_month.setdefault((d.year, d.month, ln["billed"]), []).append(ln)
    rows = []
    inv_no = 40118
    dupe_ids = {id(x) for x in W.dupes}
    for (y, m, car) in sorted(by_month):
        inv_no += int(rng.integers(1, 5))
        nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
        idate = nxt + dt.timedelta(days=int(rng.integers(2, 8)))
        for j, ln in enumerate(by_month[(y, m, car)], start=1):
            r = ln["load"]
            rows.append([f"INV{inv_no}", idate.strftime("%d/%m/%Y"), car, j, r["ticket"], r["rego"], r["forest"],
                         f"{r['net']:.2f}", f"{ln['rate']:.2f}", f"{ln['amount']:.2f}"])
            if id(ln) in dupe_ids:
                # billed again on the next month's invoice, then credited
                rows.append([f"INV{inv_no + 1}", (idate + dt.timedelta(days=31)).strftime("%d/%m/%Y"), car, 900 + j,
                             r["ticket"], r["rego"], r["forest"], f"{r['net']:.2f}", f"{ln['rate']:.2f}", f"{ln['amount']:.2f}"])
                rows.append([f"CRN{inv_no + 7000}", (idate + dt.timedelta(days=45)).strftime("%d/%m/%Y"), car, 1,
                             r["ticket"], r["rego"], r["forest"], f"{-r['net']:.2f}", f"{ln['rate']:.2f}", f"{-ln['amount']:.2f}"])
    write_csv(os.path.join(out, INV), ["document_no", "document_date", "carrier_code", "line_no", "ticket_ref", "vehicle_rego",
                                       "forest_code", "tonnes", "rate_nzd_per_t", "amount_nzd"], rows)


def write_mills(W, out):
    rng = np.random.default_rng(P.SEED + 14)
    dno = 7700410
    drows, wrows = [], []
    for r in W.mill_loads:
        dno += int(rng.integers(1, 4))
        r["docket"] = f"MFP{dno}"
        if P.FY26[0] <= r["posted"] <= P.FY26[1]:
            drows.append([r["docket"], r["mill"], r["posted"].strftime("%d/%m/%Y"), r["rego"], r["forest"], r["grade"],
                          f"{r['net']:.2f}"])
        if P.FY26[0] <= r["date"] <= P.FY26[1]:
            u_tare = round(float(rng.uniform(16.6, 19.4)), 2)
            wrows.append([r["mill"], r["time"].strftime("%Y-%m-%d %H:%M"), r["rego"], r["docket"],
                          f"{r['net'] + u_tare:.2f}", f"{u_tare:.2f}"])
    # the mills' weighbridges also log every other supplier's trucks
    for k in range(int(len(wrows) * 1.6)):
        mc = str(rng.choice(list(P.MILLS)))
        d = P.FY26[0] + dt.timedelta(days=int(rng.integers(0, 365)))
        t = dt.datetime.combine(d, dt.time(6, 30)) + dt.timedelta(minutes=int(rng.integers(0, 660)))
        tare = round(float(rng.uniform(15.5, 19.5)), 2)
        net = round(float(rng.uniform(18, 27)), 2)
        wrows.append([mc, t.strftime("%Y-%m-%d %H:%M"), "".join(rng.choice(list("ABCDEFGHJKLMNPRSTUVWXYZ"), 3)) +
                      str(int(rng.integers(100, 999))), str(rng.choice(["HFL", "PANP", "TWN", "OTH"])) + str(int(rng.integers(100000, 999999))),
                      f"{net + tare:.2f}", f"{tare:.2f}"])
    drows.sort(key=lambda x: (dt.datetime.strptime(x[2], "%d/%m/%Y"), x[0]))
    # two dockets re-sent in the July batch
    for i in (5, 9):
        drows.append(list(drows[i]))
    drows.sort(key=lambda x: (dt.datetime.strptime(x[2], "%d/%m/%Y"), x[0]))
    wrows.sort(key=lambda x: (x[0], x[1]))
    write_csv(os.path.join(out, DOCK), ["docket_no", "mill_code", "docket_date", "vehicle_rego", "forest_code", "product",
                                        "tonnes"], drows)
    write_csv(os.path.join(out, MWB), ["mill_code", "weigh_in", "vehicle_rego", "supplier_docket", "gross_t", "tare_t"], wrows)


def write_distractors(W, out):
    rng = np.random.default_rng(P.SEED + 15)
    rows = []
    d = dt.date(2025, 7, 1)
    base = {"A": 142, "P": 205, "K": 128, "KI": 112, "KIS": 98}
    while d <= P.FY26[1]:
        for g in P.GRADE_ORDER:
            rows.append([d.strftime("%Y-%m"), g, round(base[g] * float(np.exp(rng.normal(0, 0.05))), 0)])
        d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    write_csv(os.path.join(out, PRICES), ["month", "grade", "awg_nzd_per_jas_m3"], rows)
    vrows = []
    d = dt.date(2025, 7, 4)
    k = 0
    while d <= P.FY26[1]:
        k += 1
        vrows.append([f"V{25000 + k * 7 + int(rng.integers(0, 6))}", str(rng.choice(["Ocean Kaori", "Star Haruna", "Tasman Pioneer", "Golden Kiwi", "Pacific Totara"])),
                      d.strftime("%d/%m/%Y"), (d + dt.timedelta(days=int(rng.integers(2, 5)))).strftime("%d/%m/%Y"),
                      int(rng.integers(26000, 39000)), str(rng.choice(["China", "India", "Korea"]))])
        d += dt.timedelta(days=int(rng.integers(8, 14)))
    write_csv(os.path.join(out, VESSELS), ["call_ref", "vessel", "berthed", "sailed", "jas_m3_loaded", "destination"], vrows)
    crows = []
    for fc in P.FORESTS:
        for k in range(int(rng.integers(8, 16))):
            d = P.FY26[0] + dt.timedelta(days=int(rng.integers(0, 365)))
            crows.append([fc, d.strftime("%d/%m/%Y"), str(rng.choice(["Rain - roading", "Rain - skid site", "Fire risk", "Slip on access road"]))])
    crows.sort(key=lambda x: (dt.datetime.strptime(x[1], "%d/%m/%Y"), x[0]))
    write_csv(os.path.join(out, CLOSURES), ["forest_code", "date", "reason"], crows)
