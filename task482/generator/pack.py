"""Writes task482's evidence pack from world.py and asks.py: the store list, the chain's storage standard, the
monitoring roster, the three logger makes' exports, the Tellvane readings and the pilot's plan, Meridale's invoices and
credit memos, the item master, the administrations, the write-off log, the transfers, the two year-end physical
inventories, Brannon's service history and agreement, and the two distractors (the documents are docs.py's)."""
import csv
import datetime as dt
import os

import numpy as np

import asks as A
import docs as D
import world as W

FILES = {
    "stores": "penwick_store_list_2027-01.xlsx",
    "standard": "vaccine_storage_handling_standard_po-114_rev6.pdf",
    "roster": "refrigerator_monitoring_roster_2026.xlsx",
    "frostline": "frostline_temperature_logs_2026.csv",
    "kelvra": "kelvra_logger_export_2026.csv",
    "brumal": "brumal_downloads_2026.txt",
    "tellvane": "tellvane_sensor_readings_2026.csv",
    "pilot": "tellvane_pilot_plan_2026.pdf",
    "invoices": "meridale_vaccine_invoices_2026.csv",
    "items": "vaccine_item_master_2026.xlsx",
    "admin": "pharmacy_vaccine_administrations_2026.csv",
    "writeoffs": "vaccine_writeoff_log_2026.csv",
    "credits": "meridale_credit_memos_2026.csv",
    "transfers": "vaccine_store_transfers_2026.csv",
    "inventory": "vaccine_physical_inventory_ye2025_ye2026.xlsx",
    "brannon": "brannon_service_history_2026-01_2027-01.xlsx",
    "agreement": "brannon_service_agreement_2025.pdf",
    "quotes": "pharmaceutical_refrigerator_quotes_2027.pdf",
    "weather": "regional_weather_daily_2026.csv",
}
Y0, Y1 = W.WARM, W.WARM + 525600
STREETS = ["Main Street", "Oak Avenue", "Market Street", "Mill Road", "Church Street", "Prairie Avenue", "Elm Street",
           "Station Road", "Commerce Drive", "Lincoln Way", "Maple Street", "Ridge Road", "Union Street", "High Street",
           "Cedar Lane"]


def write_csv(path, head, rows, pre=()):
    with open(path, "w", newline="", encoding="utf-8") as f:
        for line in pre:
            f.write(line + "\n")
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        n = 0
        for r in rows:
            w.writerow(r)
            n += 1
    return n


def logger_serials(no):
    """the store's data logger serials in order of service"""
    mk = W.make_of(no)

    def one(k):
        h = (no * 2654435761 + k * 40503 + 977) % 2 ** 32
        if mk == "F":
            return "FL2-%06X" % (h & 0xFFFFFF)
        if mk == "K":
            return "K10%07d" % (h % 10 ** 7)
        return "BR2-%06d" % (h % 10 ** 6)
    return [one(0), one(1)] if no in W.REPLACED else [one(0)]


def sensor_id(no):
    return "TV4-%06X" % ((no * 7393 + 811) * 2246822519 % 2 ** 24)


def replaced_at(no):
    d, hh, mm, g = W.REPLACED[no]
    a = W.at(d, hh, mm)
    return a, a + g


def records(e):
    """(physical minute, probe reading in C, serial) for the local year"""
    no = e["store"]["no"]
    t, x = e["rec_t"], e["rec_x"]
    k = (t >= Y0) & (t < Y1)
    t, x = t[k], x[k]
    ser = logger_serials(no)
    if no in W.REPLACED:
        a, b = replaced_at(no)
        s = np.where(t < a, ser[0], ser[1])
    else:
        s = np.full(len(t), ser[0])
    return t, x, s


def iso_local(m):
    loc, off = W.local_of(m)
    return loc.strftime("%Y-%m-%dT%H:%M:%S") + ("-05:00" if off == -5 else "-06:00")


def location(no):
    s = W.BY_NO[no]
    return "Penwick %d %s vaccine fridge" % (no, s["town"])


def former_name(no):
    if no // 100 == 2:
        return "Vollmer Drug #%d" % A.LEGACY_NO[no]
    if no // 100 == 3:
        return "Lindqvist Apothecary #%d" % A.LEGACY_NO[no]
    return None


# ----------------------------------------------------------------------------------------------------- temperatures
def write_frostline(path, E):
    n = 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("Serial,Location,Timestamp,Temperature (C)\n")
        for s in W.STORES:
            if s["make"] != "F":
                continue
            t, x, ser = records(E[s["no"]])
            loc = location(s["no"])
            out = ["%s,%s,%s,%.1f\n" % (ser[i], loc, iso_local(t[i]), x[i]) for i in range(len(t))]
            f.write("".join(out))
            n += len(out)
    return n


def write_kelvra(path, E):
    n = 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("Kelvra LogView 4 export\nExported 2027-01-07 16:42 by pharmacy.ops\nAll times UTC\n")
        f.write("Logger ID,Date,Time,Temperature (F)\n")
        for s in W.STORES:
            if s["make"] != "K":
                continue
            t, x, ser = records(E[s["no"]])
            utc = [W.utc_of(m) for m in t]
            month = np.array([u.year * 12 + u.month for u in utc])
            idx = np.arange(len(t))
            for mo in sorted(set(month.tolist())):
                blk = idx[month == mo].tolist()
                if s["no"] == 204 and mo == 2026 * 12 + 9:
                    blk = [i for i in idx[month == mo - 1].tolist() if utc[i].date() == dt.date(2026, 8, 31)] + blk
                out = ["%s,%s,%s,%.1f\n" % (ser[i], utc[i].strftime("%m/%d/%Y"), utc[i].strftime("%H:%M:%S"),
                                            x[i] * 9 / 5 + 32) for i in blk]
                f.write("".join(out))
                n += len(out)
    return n


def write_brumal(path, E):
    n = 0
    r = np.random.default_rng(W.SEED * 1000 + 1301)
    with open(path, "w", encoding="utf-8", newline="") as f:
        for s in W.STORES:
            if s["make"] != "P":
                continue
            t, x, ser = records(E[s["no"]])
            std = [W.utc_of(m) - dt.timedelta(hours=6) for m in t]
            month = np.array([u.month for u in std])
            idx = np.arange(len(t))
            for mo in range(1, 13):
                blk = idx[month == mo].tolist()
                if not blk:
                    continue
                for sr in sorted(set(ser[i] for i in blk), key=lambda z: logger_serials(s["no"]).index(z)):
                    b2 = [i for i in blk if ser[i] == sr]
                    nxt = dt.date(2026 + mo // 12, mo % 12 + 1, 1)
                    got = dt.datetime(nxt.year, nxt.month, int(r.integers(2, 5)), 9, int(r.integers(0, 59)))
                    if mo == 3 and s["no"] == 302 and sr == logger_serials(302)[0]:
                        got = W.local_of(replaced_at(302)[0])[0] + dt.timedelta(minutes=12)
                    f.write("=" * 64 + "\n")
                    f.write("Brumal BR-20  Data Download Report\n")
                    f.write("Serial number:      %s\n" % sr)
                    f.write("Description:        Lindqvist #%d %s vaccine fridge\n" % (A.LEGACY_NO[s["no"]], s["town"]))
                    f.write("Download time:      %s\n" % got.strftime("%m/%d/%Y %H:%M"))
                    f.write("Logging interval:   10 min\n")
                    f.write("Clock:              UTC-06:00, daylight saving time not applied\n")
                    f.write("First record:       %s\n" % std[b2[0]].strftime("%m/%d/%Y %H:%M"))
                    f.write("Last record:        %s\n" % std[b2[-1]].strftime("%m/%d/%Y %H:%M"))
                    f.write("Records:            %d\n" % len(b2))
                    f.write("-" * 64 + "\n")
                    f.write("Date\tTime\tTemperature (C)\n")
                    f.write("".join("%s\t%s\t%.1f\n" % (std[i].strftime("%m/%d/%Y"), std[i].strftime("%H:%M"), x[i])
                                    for i in b2))
                    n += len(b2)
    return n


def write_tellvane(path, E):
    n = 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("sensor_id,reading_time_utc,temperature_c\n")
        for no in sorted(W.PILOT):
            e = E[no]
            ct, cx = e["cl_t"], e["cl_x"]
            k = ct < Y1
            sid = sensor_id(no)
            out = ["%s,%s,%.1f\n" % (sid, W.utc_of(m).strftime("%Y-%m-%dT%H:%M:%SZ"), v) for m, v in zip(ct[k], cx[k])]
            f.write("".join(out))
            n += len(out)
    return n


# ----------------------------------------------------------------------------------------------------------- office
def _book():
    import openpyxl
    return openpyxl.Workbook()


def _style(ws, widths, fmt=None, header=1):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    for c in ws[header]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, wd in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.freeze_panes = ws.cell(row=header + 1, column=1).coordinate
    for col, f in (fmt or {}).items():
        for row in ws.iter_rows(min_row=header + 1):
            if len(row) > col:
                row[col].number_format = f


def write_stores(path):
    wb = _book()
    ws = wb.active
    ws.title = "Stores"
    ws.append(["Store", "Store name", "Town", "Address", "Former name", "Joined Penwick", "Time zone",
               "Pharmacy hours", "Vaccine refrigerator", "Unit type", "Meridale ship-to", "Brannon site"])
    for s in W.STORES:
        no = s["no"]
        mk, md, _ = A.model_of(no)
        joined = {1: None, 2: dt.date(2024, 7, 1), 3: dt.date(2025, 3, 1)}[no // 100]
        ws.append([no, "Penwick Pharmacy %s" % s["town"], s["town"],
                   "%d %s" % (100 + (no * 37) % 1900, STREETS[(no * 7 + no // 100) % len(STREETS)]),
                   former_name(no), joined, "Central", "Mon-Fri 8:00-21:00, Sat 9:00-18:00, Sun 10:00-18:00",
                   "%s %s" % (mk, md), "Pharmaceutical-grade" if s["unit"] == "pharma" else "Household-style",
                   str(A.SHIP_TO[no]), A.BRANNON_SITE[no]])
    _style(ws, (7, 28, 13, 22, 22, 13, 9, 44, 18, 20, 13, 11), {5: "yyyy-mm-dd"})
    wb.save(path)
    return len(W.STORES)


def roster_rows(E):
    r = np.random.default_rng(W.SEED * 1000 + 1401)
    rows = []
    for s in W.STORES:
        no = s["no"]
        mk, md = W.MAKES[s["make"]]
        first = {"F": dt.date(2024, 2, 5), "K": dt.date(2023, 5, 8), "P": dt.date(2024, 9, 9)}[s["make"]]
        inst = first + dt.timedelta(days=int(r.integers(0, 40)))
        ser = logger_serials(no)
        e = E[no]
        if no in W.REPLACED:
            day = W.local_of(replaced_at(no)[0])[0].date()
            rows.append([no, "Data logger", mk, md, ser[0], inst, day, inst, day,
                         "Replaced: would not download" if no == 302 else "Replaced: probe lead damaged"])
            rows.append([no, "Data logger", mk, md, ser[1], day, None, day, None, None])
        elif no in W.PILOT:
            ins = W.local_of(e["inst"])[0].date()
            col = W.local_of(e["coll"])[0].date()
            rows.append([no, "Data logger", mk, md, ser[0], inst, col, inst, ins, "Collected at pilot check-in visit"])
            rows.append([no, "In-carton sensor", "Tellvane (Tamberlane Sensing)", "TV-4", sensor_id(no), ins, None, ins,
                         None, "Pilot store"])
        else:
            rows.append([no, "Data logger", mk, md, ser[0], inst, None, inst, None, None])
    return rows


def write_roster(path, E):
    wb = _book()
    ws = wb.active
    ws.title = "Devices"
    ws.append(["Store", "Device type", "Make", "Model", "Serial or sensor id", "Installed", "Removed",
               "Device of record from", "Device of record to", "Notes"])
    rows = roster_rows(E)
    for row in rows:
        ws.append(row)
    _style(ws, (7, 16, 28, 12, 18, 12, 12, 12, 12, 34), {5: "yyyy-mm-dd", 6: "yyyy-mm-dd", 7: "yyyy-mm-dd",
                                                         8: "yyyy-mm-dd"})
    wb.save(path)
    return len(rows)


def write_items(path):
    wb = _book()
    ws = wb.active
    ws.title = "Vaccine items"
    ws.append(["NDC", "Description", "Manufacturer", "Package", "Doses per package", "Season", "Package cost (USD)"])
    for k, it in A.ITEM.items():
        ws.append([it["ndc"], it["desc"], A.LABELERS[it["ndc"].split("-")[0]], it["package"], it["dpp"],
                   it["season"] or None, it["cost"]])
    _style(ws, (14, 64, 22, 24, 9, 10, 11), {6: "#,##0.00"})
    wb.save(path)
    return len(A.ITEM)


MERIDALE_DESC = {"F25S": "FLU VAC TRIV 25-26 PFS 0.5ML 10X", "F25V": "FLU VAC TRIV 25-26 MDV 5ML",
                 "F25H": "FLU VAC HD 25-26 PFS 0.5ML 10X", "F26S": "FLU VAC TRIV 26-27 PFS 0.5ML 10X",
                 "F26V": "FLU VAC TRIV 26-27 MDV 5ML", "F26H": "FLU VAC HD 26-27 PFS 0.5ML 10X",
                 "C25": "COVID-19 VAC 25-26 PFS 0.5ML 10X", "C26": "COVID-19 VAC 26-27 PFS 0.5ML 10X",
                 "RSV": "RSV VAC ADJ SDV KIT 1X", "PCV": "PNEUMO CONJ VAC 21V PFS 0.5ML 10X",
                 "RZV": "ZOSTER VAC RECOMB ADJ KIT 10X", "TDP": "TDAP VAC PFS 0.5ML 10X",
                 "HPB": "HEP B VAC ADULT PFS 1ML 10X"}


def ship_to(no, d):
    if no in A.OLD_SHIP_TO and d < A.ACCOUNTS_MOVED:
        return str(A.OLD_SHIP_TO[no]), "LINDQVIST APOTHECARY #%02d" % A.LEGACY_NO[no]
    return str(A.SHIP_TO[no]), "PENWICK PHARMACY #%d" % no


def invoice_rows(F):
    lst = []
    for no in sorted(F):
        for (t, inv, lines) in F[no]["receipts"]:
            lst.append((inv, no, t, lines))
    lst.sort(key=lambda x: (x[0], x[1], x[2]))
    r = np.random.default_rng(W.SEED * 1000 + 1501)
    rows = []
    num = 4417300
    for inv, no, t, lines in lst:
        num += int(r.integers(4, 90))
        acct, name = ship_to(no, inv)
        for (key, pk, k) in lines:
            it = A.ITEM[key]
            lot = A.lots_name(key, k)
            rows.append(["MPD%07d" % num, inv.strftime("%m/%d/%Y"), acct, name, A.ndc11(it["ndc"]), MERIDALE_DESC[key],
                         lot, A.LOT_EXP[lot].strftime("%m/%d/%Y"), pk, it["uom"], "%.2f" % it["cost"],
                         "%.2f" % (pk * it["cost"]), t.strftime("%m/%d/%Y %H:%M")])
    return rows


def admin_rows(F):
    lst = []
    for no in sorted(F):
        for (t, key, lot) in F[no]["admin"]:
            lst.append((t, no, key, lot))
    lst.sort(key=lambda x: (x[0], x[1]))
    seq = {no: 0 for no in F}
    rows = []
    for t, no, key, lot in lst:
        seq[no] += 1
        rows.append([no, t.strftime("%Y-%m-%d %H:%M"), "V%d%06d" % (no, seq[no]), A.ITEM[key]["ndc"], A.SHORT[key],
                     lot, 1])
    return rows


def writeoff_rows(F):
    lst = []
    for no in sorted(F):
        for (t, key, lot, doses, logged, reason) in F[no]["writeoffs"]:
            lst.append((t, no, key, lot, logged, reason))
    lst.sort(key=lambda x: (x[0], x[1]))
    rows = []
    for t, no, key, lot, logged, reason in lst:
        it = A.ITEM[key]
        unit = it["cost"] if (it["mdv"] and t.date() < A.UPDATE) else it["cost"] / it["dpp"]
        rows.append([no, t.strftime("%Y-%m-%d %H:%M"), it["ndc"], A.SHORT[key], lot,
                     A.LOT_EXP[lot].strftime("%Y-%m-%d"), logged, reason, "%.2f" % (logged * unit)])
    return rows


def credit_rows(F):
    r = np.random.default_rng(W.SEED * 1000 + 1601)
    rows = []
    memo = 208114
    order = sorted(F, key=lambda no: (int((no * 13) % 31), no))
    for i, no in enumerate(order):
        d = dt.date(2026, 7, 14) + dt.timedelta(days=int(i * 1.2) + int(r.integers(0, 3)))
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        memo += int(r.integers(3, 30))
        acct, name = ship_to(no, d)
        for (key, lot, units, doses) in F[no]["credits"]:
            if units <= 0:
                continue
            it = A.ITEM[key]
            rows.append(["CM%06d" % memo, d.strftime("%m/%d/%Y"), acct, name, A.ndc11(it["ndc"]), MERIDALE_DESC[key],
                         lot, units, "VL" if it["mdv"] else "EA", "%.2f" % (units * it["cost"] / it["upp"]),
                         "SEASONAL RETURN - EXPIRED"])
    rows.sort(key=lambda x: (x[0], x[4]))
    return rows


def transfer_rows(F):
    rows = []
    for no in sorted(F):
        for (t, key, lot, q, nb, tno, tr) in F[no]["t_out"]:
            rows.append([tno, t.strftime("%Y-%m-%d %H:%M"), no, nb, A.ITEM[key]["ndc"], A.SHORT[key], lot, q,
                         tr.strftime("%Y-%m-%d %H:%M")])
    rows.sort(key=lambda x: (x[1], x[0]))
    return rows


def write_inventory(path, F):
    wb = _book()
    r = np.random.default_rng(W.SEED * 1000 + 1701)
    n = 0
    for j, yr in enumerate((2025, 2026)):
        ws = wb.active if j == 0 else wb.create_sheet()
        ws.title = "YE %d" % yr
        ws.append(["Store", "NDC", "Description", "Doses on hand", "Count closed", "Counted by"])
        for no in sorted(F):
            t, have = F[no]["counts"][yr]
            who = "E%05d" % (10000 + (no * 41 + yr * 7 + int(r.integers(0, 3))) % 89999)
            for key in A.ITEM:
                if have[key] > 0:
                    ws.append([no, A.ITEM[key]["ndc"], A.ITEM[key]["desc"], have[key], t, who])
                    n += 1
        _style(ws, (7, 14, 64, 10, 17, 10), {4: "yyyy-mm-dd hh:mm"})
    wb.save(path)
    return n


def brannon_site_name(no):
    s = W.BY_NO[no]
    if no // 100 == 1:
        return "PENWICK PHARMACY #%d %s" % (no, s["town"].upper())
    return "%s %s" % (former_name(no).upper(), s["town"].upper())


def brannon_rows(wos):
    rows = []
    for w in wos:
        if not (dt.date(2026, 1, 1) <= w["invoice_date"] <= dt.date(2027, 1, 22)):
            continue
        for i, (vd, tt, h) in enumerate(w["visits"]):
            arr = dt.datetime(vd.year, vd.month, vd.day, int(tt[:2]), int(tt[3:]))
            dep = arr + dt.timedelta(minutes=int(round(h * 60)))
            no = w["stores"][i]
            rows.append([A.BRANNON_SITE[no], brannon_site_name(no), w["wo"], i + 1, vd,
                         arr.strftime("%H:%M"), dep.strftime("%H:%M"), w["tech"],
                         "Preventive maintenance" if w["pm"] else "Service call", w["work"][i], w["invoice"],
                         w["invoice_date"], w["amount"]])
    rows.sort(key=lambda x: (x[0], x[4], x[2], x[3]))
    return rows


def write_brannon(path, wos):
    from openpyxl.styles import Font
    wb = _book()
    ws = wb.active
    ws.title = "Service history"
    ws.append(["Brannon Refrigeration Service, customer portal"])
    ws.append(["Service history for Penwick Pharmacy, Inc., invoices dated 01/01/2026 to 01/22/2027"])
    ws.append([])
    ws.append(["Site", "Site name", "Work order", "Visit", "Visit date", "Arrive", "Depart", "Technician", "Call type",
               "Work performed", "Invoice", "Invoice date", "Invoice amount"])
    rows = brannon_rows(wos)
    for row in rows:
        ws.append(row)
    _style(ws, (10, 34, 11, 6, 11, 7, 7, 10, 20, 70, 9, 11, 12), {4: "mm/dd/yyyy", 11: "mm/dd/yyyy", 12: "#,##0.00"},
           header=4)
    ws["A1"].font = Font(bold=True, size=12)
    wb.save(path)
    return len(rows)


def weather_rows():
    r = np.random.default_rng(W.SEED * 1000 + 1801)
    rows = []
    storms = {W.STORMS["S1"][0]: "Freezing rain and ice; scattered power outages",
              W.STORMS["S2"][0]: "Severe thunderstorms, damaging winds; power outages",
              W.STORMS["S3"][0] - 1: "Line of severe storms after midnight; widespread power outages"}
    for d in range(365):
        day = dt.date(2026, 1, 1) + dt.timedelta(days=d)
        mean = 50 - 28 * np.cos(2 * np.pi * (d + 1 - 20) / 365.0)
        hi = mean + 10 + r.normal(0, 6)
        lo = mean - 10 + r.normal(0, 5)
        rain = max(0.0, r.gamma(0.5, 0.25) - 0.05) if r.random() < 0.32 else 0.0
        snow = round(rain * 10 * r.uniform(0.6, 1.2), 1) if (hi < 34 and rain > 0) else 0.0
        gust = int(round(max(8, r.normal(24, 7))))
        note = storms.get(d, "")
        if note:
            gust = int(r.integers(52, 71))
            rain = max(rain, round(r.uniform(0.6, 1.6), 2))
        rows.append([day.isoformat(), "CORRIDEN REGIONAL AIRPORT", int(round(hi)), int(round(lo)), "%.2f" % rain,
                     "%.1f" % snow, gust, note.upper()])
    return rows


def build_pack(out, E, F, wos):
    f = lambda k: os.path.join(out, FILES[k])
    n = {}
    n["frostline"] = write_frostline(f("frostline"), E)
    n["kelvra"] = write_kelvra(f("kelvra"), E)
    n["brumal"] = write_brumal(f("brumal"), E)
    n["tellvane"] = write_tellvane(f("tellvane"), E)
    n["stores"] = write_stores(f("stores"))
    n["roster"] = write_roster(f("roster"), E)
    n["items"] = write_items(f("items"))
    n["invoices"] = write_csv(f("invoices"), ["INVOICE_NO", "INVOICE_DATE", "SHIP_TO", "SHIP_TO_NAME", "NDC",
                                              "ITEM_DESCRIPTION", "LOT", "EXP_DATE", "QTY_SHIPPED", "UOM",
                                              "UNIT_PRICE", "EXT_PRICE", "DELIVERED"], invoice_rows(F))
    n["admin"] = write_csv(f("admin"), ["store", "administered_at", "transaction_id", "ndc", "product", "lot",
                                        "doses"], admin_rows(F))
    n["writeoffs"] = write_csv(f("writeoffs"), ["store", "written_off_at", "ndc", "product", "lot", "expiration",
                                                "quantity", "reason", "cost"], writeoff_rows(F))
    n["credits"] = write_csv(f("credits"), ["CREDIT_MEMO", "MEMO_DATE", "SHIP_TO", "SHIP_TO_NAME", "NDC",
                                            "ITEM_DESCRIPTION", "LOT", "QTY", "UOM", "CREDIT_AMT", "REASON"],
                             credit_rows(F))
    n["transfers"] = write_csv(f("transfers"), ["transfer_no", "shipped_at", "from_store", "to_store", "ndc",
                                                "product", "lot", "doses", "received_at"], transfer_rows(F))
    n["inventory"] = write_inventory(f("inventory"), F)
    n["brannon"] = write_brannon(f("brannon"), wos)
    n["weather"] = write_csv(f("weather"), ["DATE", "STATION", "TMAX", "TMIN", "PRCP", "SNOW", "WSFG", "REMARKS"],
                             weather_rows())
    D.write_standard(f("standard"))
    D.write_pilot(f("pilot"), [(no, W.local_of(E[no]["inst"])[0].date()) for no in W.PILOT])
    D.write_agreement(f("agreement"))
    D.write_quotes(f("quotes"))
    n["standard"] = n["pilot"] = n["agreement"] = n["quotes"] = 1
    return n
