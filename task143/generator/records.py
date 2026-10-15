"""The exports: each system writes its own layout. The reliability lab's two cycler fleets (fleet A's software writes
semicolon-separated files with decimal commas and Bielefeld wall time, numbering a test's first cycle 0; fleet B's
writes ISO stamps in UTC and numbers from 1, its weekly pulls overlapping by a day), the lab's register of release-test
cells, the life-test export, Zelvora's cell data package for ZC2638, the battery plant's genealogy and pack register,
the shipments, the service case system, the DACH depot's SAP service orders, the returns depot's log, the carrier's
statement, the partners' monthly invoices, the treasury's rates and the service cost sheet."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import common as K
import field as FD

# ---------------------------------------------------------------------------------------------------- serial forms
def cyc_id_a(serial):
    """Fleet A's cell id: the lot's four digits, a dot, the sequence."""
    lot, seq = serial.split("-")
    return "%s.%s" % (lot[2:], seq)


def cyc_id_b(serial):
    return serial.replace("-", "")


def scan_form(serial):
    """The pack line's scanner reads the cell's code without the hyphen."""
    return serial.replace("-", "")


def de_num(x, dp):
    s = ("%." + str(dp) + "f") % x
    return s.replace(".", ",")


# ---------------------------------------------------------------------------------------------------- the release tests
CYC_A_COLS = ["Zelle", "Kanal", "Test", "Zyklus", "Ladekapazitaet_mAh", "Entladekapazitaet_mAh", "DCIR_mOhm",
              "Tmax_C", "Zyklusende"]
CYC_B_COLS = ["cell_id", "channel", "test_id", "cycle", "charge_mAh", "discharge_mAh", "dcir_10s_mohm", "t_max_c",
              "cycle_end_utc"]


def cycle_rows(W):
    """Both fleets' rows, each test's cycles on the channel it ran on; a test continued on another channel is a new
    test there, numbered from that fleet's first cycle."""
    a_rows, b_rows = [], []
    r = K.rng("cycle-export")
    tid = {"A": 210000, "B": 7700000}
    for serial in sorted(W.tests, key=lambda s: (K.LOTS.index(W.tests[s].lot), s)):
        T = W.tests[serial]
        for (i0, i1, fleet, ch) in T.segments:
            tid[fleet] += int(r.integers(1, 4))
            for i in range(i0, i1):
                n = i - i0 + (0 if fleet == "A" else 1)
                end_utc = T.ends_utc[i]
                if fleet == "A":
                    loc = K.utc_to_local(end_utc)
                    a_rows.append([cyc_id_a(serial), ch, "T%d" % tid["A"], n, de_num(T.qc[i], 1), de_num(T.q[i], 1),
                                   de_num(T.res[i], 2), de_num(T.tmax[i], 1), loc.strftime("%d.%m.%Y %H:%M:%S")])
                else:
                    b_rows.append([cyc_id_b(serial), ch, "%d" % tid["B"], n, "%.1f" % T.qc[i], "%.1f" % T.q[i],
                                   "%.3f" % T.res[i], "%.1f" % T.tmax[i], end_utc.strftime("%Y-%m-%dT%H:%M:%SZ")])
    # fleet B's export is the concatenation of weekly pulls, each pull covering eight days: the overlapping day's
    # cycles arrive twice
    out_b = []
    for row in b_rows:
        out_b.append(row)
        end = dt.datetime.strptime(row[8], "%Y-%m-%dT%H:%M:%SZ")
        if end.weekday() == 0 and end.hour < 6:
            out_b.append(list(row))
    return a_rows, out_b


REG_COLS = ["lot", "lot_released", "tray", "cell_serial", "fleet", "channel", "test_start_local", "note"]


def register_rows(W):
    rows = []
    for c in sorted(W.qcells, key=lambda c: (K.LOTS.index(c.lot), c.tray_no, c.pos)):
        T = W.tests[c.serial]
        for k, (i0, i1, fleet, ch) in enumerate(T.segments):
            if k == 0:
                start = T.start_local
                note = ""
            else:
                start = K.utc_to_local(T.ends_utc[i0 - 1]) + dt.timedelta(hours=1.5)
                start = start.replace(second=0, microsecond=0)
                note = "continued after channel fault on %s at cycle %d" % (T.segments[0][3], i0)
            rows.append([c.lot, K.lot_release(c.lot).isoformat() if c.lot != K.NEW_LOT else "",
                         c.tray, c.serial, fleet, ch, start.strftime("%Y-%m-%d %H:%M"), note])
    return rows


LIFE_COLS = ["lot", "cell_serial", "status", "cycles", "reason"]


def life_rows(W):
    rows = []
    for c in sorted(W.qcells, key=lambda c: (K.LOTS.index(c.lot), c.serial)):
        if c.lot not in K.TRAIN_LOTS:
            continue
        L = W.life[c.serial]
        rows.append([c.lot, c.serial, L.status, L.cycles, L.reason])
    return rows


# ---------------------------------------------------------------------------------------------------- the lot under release
CELL_COLS = ["cell_sn", "lot", "formation_tray", "tray_pos", "formation_end", "formation_cap_mah", "ocv_v",
             "acir_mohm", "k_value_mv_d"]


def cell_package_rows(W):
    rows = []
    N = W.new
    tmap = {t.no: t for t in N.trays}
    for tno in sorted(N.tray_cells):
        t = tmap[tno]
        for j, s in enumerate(N.tray_cells[tno]):
            c = N.cells[s]
            rows.append([c.serial, K.NEW_LOT, t.key, j + 1, (t.formed + dt.timedelta(hours=26)).strftime("%Y-%m-%d %H:%M"),
                         "%.1f" % c.cap, "%.4f" % c.ocv, "%.2f" % c.acir, "%.3f" % c.kval])
    return rows


GEN_COLS = ["pack_sn", "built", "line", "position", "cell_scan"]


def genealogy_rows(W):
    rows = []
    pk = [p for p in W.field_packs if p.lot == K.NEW_LOT]
    assert len(pk) == len(W.new.packs)
    for p, cells in zip(pk, W.new.packs):
        for pos, s in enumerate(cells):
            rows.append([p.serial, p.built.strftime("%Y-%m-%d %H:%M"), p.line, pos + 1, scan_form(W.new.cells[s].serial)])
    return rows


def model_j_rows(W):
    rows = []
    r = K.rng("model-j-serials")
    d0 = dt.datetime(2026, 9, 29, 6, 5)
    for i, cells in enumerate(W.new.j_packs):
        t = d0 + dt.timedelta(minutes=int(i * 9.7 + r.integers(0, 5)))
        while t.weekday() >= 5:
            t += dt.timedelta(days=1)
        ps = "JP%s%04d" % (t.strftime("%y%m%d"), i + 1)
        for pos, s in enumerate(cells):
            rows.append([ps, t.strftime("%Y-%m-%d %H:%M"), "J", pos + 1, scan_form(W.new.cells[s].serial)])
    return rows


# ---------------------------------------------------------------------------------------------------- the field
CASE_COLS = ["case_no", "opened_utc", "closed_utc", "region", "partner", "country", "system_sn", "model", "fault_code",
             "action", "warranty", "cycle_count", "fcc_pct", "labour_min", "battery_sn", "legacy_ref"]


def _stamp(t):
    return t.strftime("%Y-%m-%d %H:%M") if t is not None else ""


def case_rows(W):
    rows = []
    for ev in sorted(W.cases, key=lambda e: e.case):
        nb = ev.nb
        replaced = ev.code != "NFF"
        closed = ev.case_closed if (ev.case_closed is not None and ev.case_closed <= FD.END) else None
        if ev.migrated:
            opened = ev.opened.replace(hour=0, minute=0)
            closed = closed.replace(hour=0, minute=0) if closed is not None else None
            cyc = ""
            fcc = ""
        else:
            opened = ev.opened
            cyc = ev.cycles
            fcc = "%.1f" % ev.fcc
        rows.append([ev.case, _stamp(opened), _stamp(closed), ev.region, FD.PARTNER_CODE[FD.PARTNER[ev.region]],
                     nb.country, nb.serial,
                     nb.model, ev.code, "REPLACED" if (replaced and ev.closed is not None) else
                     ("NO_ACTION" if ev.code == "NFF" else ""),
                     ev.warranty, cyc, fcc, ev.labour_min if ev.closed is not None else "",
                     ev.fitted or "", ev.sap or ""])
    return rows


SAP_COLS = ["Auftrag", "Auftragsart", "Erstellt am", "Techn. Abschluss", "Equipment", "Material", "Schadenscode",
            "Zykluszähler", "Ausbau-SN", "Einbau-SN", "Arbeit Ist (Min)", "Bemerkung"]
SAP_CODE = {"CAP": "B10", "SWL": "B20", "CON": "B30", "BMS": "B40", "NFF": "B90"}
SAP_TYPE = {"WTY": "ZS01", "GW": "ZS02", "OOW": "ZS03"}
MATERIAL = {"K14": "4100-2214", "K15": "4100-2215"}


def sap_rows(W):
    rows = []
    notes = {"CAP": ["Akku tauschen, Kapazität zu gering", "Akku verbraucht", "Kunde: Laufzeit unter 2 h", ""],
             "SWL": ["Akku gewölbt, Gehäuse hebt sich", "Akku aufgebläht"], "CON": ["Akku wird nicht erkannt", ""],
             "BMS": ["Ladeanzeige springt", "Akku lädt nicht über 60 %"], "NFF": ["kein Fehler, Akku i.O.", ""]}
    r = K.rng("sap-notes")
    for ev in sorted(W.sap_orders, key=lambda e: e.sap):
        nb = ev.nb
        replaced = ev.code != "NFF" and ev.closed is not None
        rows.append([ev.sap, SAP_TYPE[ev.warranty], ev.opened.strftime("%d.%m.%Y"),
                     ev.closed.strftime("%d.%m.%Y") if (ev.closed is not None and ev.closed.date() < K.MIGRATION)
                     else "", nb.serial, MATERIAL[nb.model], SAP_CODE[ev.code], ev.cycles,
                     ev.removed if replaced else "", ev.fitted or "", ev.labour_min if ev.closed is not None else "",
                     notes[ev.code][int(r.integers(0, len(notes[ev.code])))]])
    return rows


# ---------------------------------------------------------------------------------------------------- workbooks
HEAD_FILL = PatternFill("solid", fgColor="D9E1F2")


def _autowidth(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w


def write_sap(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Export"
    ws.append(SAP_COLS)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
    for r in rows:
        ws.append([None if v == "" else v for v in r])
    _autowidth(ws, [12, 11, 11, 15, 14, 11, 13, 12, 17, 17, 15, 38])
    ws.freeze_panes = "A2"
    wb.save(path)


RET_COLS = ["Received", "Consignment", "Sender", "Reference", "Battery SN", "Depot FCC %", "Finding", "Freight EUR"]


def write_returns(path, W):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Returns"
    ws.append(RET_COLS)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
    for row in sorted(W.returns, key=lambda x: (x.received, x.cons, x.serial)):
        ev = row.ev
        ref = ev.case if (ev.case and not ev.migrated) else (str(ev.sap) if ev.sap else ev.case)
        finding = "confirmed" if (ev.code != "CAP" or row.fcc < 80.0) else "above limit"
        ws.append([row.received, row.cons, FD.PARTNER_CODE[row.partner], ref, row.serial, row.fcc, finding,
                   row.charge if row.partner != "KVD" else None])
    for c in ws["A"][1:]:
        c.number_format = "dd.mm.yyyy"
    _autowidth(ws, [11, 12, 8, 14, 17, 11, 12, 11])
    ws.freeze_panes = "A2"
    wb.save(path)


# ---------------------------------------------------------------------------------------------------- money
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# each partner's own invoice layout: its language, its header labels, its line columns, its sheet names
INV_LAYOUT = {
    "SVT": dict(months=["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre",
                        "Novembre", "Décembre"],
                country="France", invoice="Facture n°", replaces="Annule et remplace", date="Date de facture",
                period="Période", customer="Client", currency="Devise",
                cols=["N° intervention", "Dossier", "N° de série", "Panne", "Prise en charge", "Main-d'oeuvre",
                      "Manutention", "Total HT"],
                net="Total HT", vat="TVA (autoliquidation)", total="Total TTC", datefmt="dd/mm/yyyy"),
    "HRL": dict(months=MONTHS, country="United Kingdom", invoice="Invoice", replaces="Replaces invoice",
                date="Invoice date", period="Service period", customer="Customer", currency="Currency",
                cols=["Job", "Case", "System SN", "Fault", "Basis", "Labour", "Handling", "Line total"],
                net="Net", vat="VAT (reverse charge)", total="Total", datefmt="dd/mm/yyyy"),
    "NFX": dict(months=["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober",
                        "november", "december"],
                country="Sverige", invoice="Faktura", replaces="Ersätter faktura", date="Fakturadatum",
                period="Period", customer="Kund", currency="Valuta",
                cols=["Arbetsorder", "Ärende", "Serienummer", "Fel", "Grund", "Arbete", "Hantering", "Summa"],
                net="Netto", vat="Moms (omvänd skattskyldighet)", total="Att betala", datefmt="yyyy-mm-dd"),
    "RPS": dict(months=["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre",
                        "Ottobre", "Novembre", "Dicembre"],
                country="Italia", invoice="Fattura n.", replaces="Sostituisce la fattura", date="Data fattura",
                period="Periodo", customer="Cliente", currency="Valuta",
                cols=["Ordine", "Pratica", "Matricola", "Guasto", "Copertura", "Manodopera", "Gestione", "Totale riga"],
                net="Imponibile", vat="IVA (inversione contabile)", total="Totale documento", datefmt="dd/mm/yyyy"),
}


def invoice_number(partner, y, m):
    if partner == "HRL":
        return "TM-%02d%02d" % (y % 100, m)
    if partner == "SVT":
        return "DVG-F%d" % (25110 + (y - 2025) * 12 + m)
    if partner == "NFX":
        return "LJQ-%d-%04d" % (y, 600 + (y - 2025) * 12 + m)
    return "FA/%d/%03d" % (y, m * 3 + 1)


def write_invoice_book(path, partner, W):
    """One sheet per invoice in the partner's own layout and language: the header block, a line per job carried out in
    the service period, the totals."""
    cur, lab, hand, diag = FD.FEES[partner]
    L = INV_LAYOUT[partner]
    lines = W.invoices[partner]
    by_m = {}
    for ln in lines:
        by_m.setdefault(ln.month, []).append(ln)
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    city, cc = FD.PARTNER_CITY[partner]
    for (y, m) in sorted(by_m):
        ls = sorted(by_m[(y, m)], key=lambda x: x.job)
        issue = W.invoice_issue[(partner, y, m)]
        inv_no = invoice_number(partner, y, m)
        period = "%s %d" % (L["months"][m - 1], y)
        variants = [(period, inv_no, issue, ls, None, None)]
        if partner == "HRL" and (y, m) == (2026, 3):
            # the invoice as first sent (last year's handling fee, one job billed twice) and its reissue
            dup = sorted(list(ls) + [ls[len(ls) // 2]], key=lambda x: x.job)
            variants = [(period, inv_no, issue, dup, 6.50, None),
                        (period + " R1", inv_no + "-R1", W.invoice_reissue[(partner, y, m)], ls, None, inv_no)]
        for title, number, idate, items, hand_override, replaces in variants:
            ws = wb.create_sheet(title)
            ws.append([FD.PARTNER_NAME[partner]])
            ws.append(["%s, %s" % (city, L["country"])])
            ws.append([])
            ws.append([L["invoice"], number])
            if replaces:
                ws.append([L["replaces"], replaces])
            ws.append([L["date"], idate])
            ws.cell(ws.max_row, 2).number_format = L["datefmt"]
            ws.append([L["period"], period])
            ws.append([L["customer"], "Kalvenhorst Systeme GmbH, Service Operations, Bielefeld"])
            ws.append([L["currency"], cur])
            ws.append([])
            ws.append(L["cols"])
            hr = ws.max_row
            for c in ws[hr]:
                c.font = Font(bold=True)
                c.fill = HEAD_FILL
            net = 0.0
            for ln in items:
                ev = ln.ev
                hnd = ln.handling if (hand_override is None or ln.handling == 0) else hand_override
                tot = round(ln.labour + hnd, 2)
                net += tot
                ws.append([ln.job, ev.case, ev.nb.serial, ev.code, ev.warranty, ln.labour, hnd, tot])
            ws.append([])
            ws.append([None] * 6 + [L["net"], round(net, 2)])
            ws.append([None] * 6 + [L["vat"], 0.0])
            ws.append([None] * 6 + [L["total"], round(net, 2)])
            for c, w in zip("ABCDEFGH", (16, 13, 14, 7, 15, 13, 26, 11)):
                ws.column_dimensions[c].width = w
    wb.save(path)


CARRIER_COLS = ["consignment", "pickup_date", "shipper", "shipper_city", "shipper_country", "pieces", "weight_kg",
                "charge_eur"]


def carrier_rows(W):
    rows = []
    a = dt.date(2025, 9, 1)
    b = dt.date(2026, 10, 7)
    for c in sorted(W.consignments, key=lambda c: (c.pickup, c.no)):
        if c.partner == "KVD" or not (a <= c.pickup <= b):
            continue
        city, cc = FD.PARTNER_CITY[c.partner]
        rows.append([c.no, c.pickup.isoformat(), FD.PARTNER_NAME[c.partner], city, cc, c.n, "%.1f" % c.weight,
                     "%.2f" % c.charge])
    return rows


FX_COLS = ["month_end", "currency", "units_per_eur"]


def fx_rows(W):
    rows = []
    for (y, m) in sorted(W.fx):
        me = FD.month_ends((y, m), (y, m))[0]
        for cur in ("CHF", "DKK", "GBP", "NOK", "SEK"):
            rows.append([me.isoformat(), cur, "%.4f" % W.fx[(y, m)][cur]])
    return rows


def write_cost_sheet(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Service pack"
    ws.append(["Service cost sheet FY2026 (1 October 2025 to 30 September 2026)"])
    ws.append(["Kalvenhorst Systeme GmbH, Service Operations controlling"])
    ws.append([])
    ws.append(["Part", "Description", "Valid from", "Valid to", "Standard cost EUR"])
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
    ws.append(["4100-8820", "Model K service battery pack (3S1P, 4,820 mAh)", dt.date(2025, 10, 1), dt.date(2025, 12, 31),
               52.40])
    ws.append(["4100-8820", "Model K service battery pack (3S1P, 4,820 mAh)", dt.date(2026, 1, 1), None, 49.80])
    ws.append(["4100-8830", "Model J service battery pack (2S1P, 4,820 mAh)", dt.date(2025, 10, 1), None, 37.10])
    for row in ws.iter_rows(min_row=5, max_row=7):
        for c in row[2:4]:
            c.number_format = "dd.mm.yyyy"
    for col, w in zip("ABCDE", (11, 46, 12, 12, 17)):
        ws.column_dimensions[col].width = w
    ws2 = wb.create_sheet("DACH depot")
    ws2.append(["DACH service depot, Bielefeld: internal prices to the product divisions"])
    ws2.append([])
    ws2.append(["Item", "Valid from", "Valid to", "Price EUR", "Per"])
    for c in ws2[3]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
    ws2.append(["Battery replacement, notebook (labour and test)", dt.date(2025, 10, 1), dt.date(2025, 12, 31), 31.60,
                "repair"])
    ws2.append(["Battery replacement, notebook (labour and test)", dt.date(2026, 1, 1), None, 33.10, "repair"])
    ws2.append(["No fault found, diagnosis", dt.date(2025, 10, 1), None, 19.40, "case"])
    ws2.append(["Courier collection and return of the notebook", dt.date(2025, 10, 1), None, 12.80, "case"])
    for row in ws2.iter_rows(min_row=4, max_row=7):
        for c in row[1:3]:
            c.number_format = "dd.mm.yyyy"
    for col, w in zip("ABCDE", (48, 12, 12, 11, 8)):
        ws2.column_dimensions[col].width = w
    ws3 = wb.create_sheet("Partners")
    ws3.append(["Repair partners: contract rates per repair, FY2026"])
    ws3.append([])
    ws3.append(["Partner", "Region", "Currency", "Battery replacement", "Handling", "Diagnosis (no fault found)"])
    for c in ws3[3]:
        c.font = Font(bold=True)
        c.fill = HEAD_FILL
    for p, reg in (("SVT", "FRB"), ("HRL", "UKI"), ("NFX", "NOR"), ("RPS", "SOU")):
        cur, lab, hand, diag = FD.FEES[p]
        ws3.append([FD.PARTNER_NAME[p], reg, cur, lab, hand, diag])
    for col, w in zip("ABCDEF", (26, 8, 9, 20, 10, 26)):
        ws3.column_dimensions[col].width = w
    ws4 = wb.create_sheet("Costing")
    ws4.append(["How Service Operations controlling costs a battery repair"])
    ws4.append([])
    ws4.append(["Partner repair", "The partner's invoice line (labour and handling), converted from the invoice "
                "currency at treasury's month-end rate for the invoice's service period; the return freight of the "
                "battery it removed to the Bielefeld returns depot; the service pack fitted, at the standard cost valid "
                "on the day it was fitted."])
    ws4.append(["DACH depot repair", "The depot's internal price, the courier collection and return of the notebook, "
                "and the service pack fitted, at the standard cost valid on the day it was fitted."])
    ws4.append(["Swollen batteries", "Scrapped where they are removed; they travel to no depot."])
    ws4.column_dimensions["A"].width = 20
    ws4.column_dimensions["B"].width = 120
    wb.save(path)
