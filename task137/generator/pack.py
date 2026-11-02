"""Cut every data file of the pack from the seeded world (the two PDFs are docs.py's). Each file is written the way its
producing system exports it: the telematics platform in UTC under two export templates, the insurer's listing in UK
clock time under its report header, the bodyshop's job list, the accounts-payable ledger, the recovery account's bank
export, the fleet register, the 2027 route schedule and its calendar, the stores' delivery windows and the gov.uk
bank-holiday feed."""
import datetime as dt
import json
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import astro as A
import common as CM
import costs as CO
import params as P
import world as WO

FILES = {
    "tele_a": "gridtrak_day_summary_2023-10_2025-03.csv",
    "tele_b": "gridtrak_day_summary_2025-03_2026-09.csv",
    "listing": "ravensby_fleet_claims_listing_2026-10-31.xlsx",
    "register": "fleet_register_2026-10.xlsx",
    "schedule": "route_schedule_2027.xlsx",
    "stores": "store_delivery_windows_2027.xlsx",
    "handbook": "driver_handbook_2026.pdf",
    "terms": "claims_fund_terms_2027.pdf",
    "jobs": "brantwick_jobs_2023-10_2026-10.csv",
    "ap": "ap_ledger_brantwick_2023-10_2026-10.csv",
    "bank": "claims_recovery_account_2024-10_2026-10.csv",
    "bh": "bank-holidays-england-and-wales.json",
}
DISTRACTORS = ["stores", "bh"]
TELE_A_END = dt.date(2025, 3, 29)      # the old export template's last pull
TELE_B_START = dt.date(2025, 3, 24)    # the new template's first export starts with that reporting week
GROUP_OLD = {"CRA": "CRAMLINGTON", "GAT": "TEAM VALLEY", "CAR": "CARLISLE", "DAR": "DARLINGTON"}
GROUP_NEW = {"CRA": "Cramlington", "GAT": "Team Valley", "CAR": "Carlisle", "DAR": "Darlington"}
DEPOT_NAME = {"CRA": "Cramlington", "GAT": "Gateshead (Team Valley)", "CAR": "Carlisle (Kingmoor)",
              "DAR": "Darlington (Faverdale)"}
BANK_NAME = {
    "Aldwyn General Insurance Ltd": "ALDWYN GENERAL INS", "Bellmont Motor Underwriting Ltd": "BELLMONT MOTOR UW",
    "Coquet Mutual Insurance": "COQUET MUTUAL INS", "Delamere Insurance plc": "DELAMERE INS PLC",
    "Elsdon Direct Ltd": "ELSDON DIRECT LTD", "Fenwick & Hart Insurance": "FENWICK AND HART",
    "Greyfriars Assurance Ltd": "GREYFRIARS ASSUR", "Halsall Motor Ltd": "HALSALL MOTOR LTD",
    "Ingleby Insurance Company": "INGLEBY INS CO", "Kirkhaugh Insurance plc": "KIRKHAUGH INS PLC",
    "Lowther General Ltd": "LOWTHER GENERAL", "Morrell Motor Insurance": "MORRELL MOTOR INS",
    "Northallerton Mutual": "NORTHALLERTON MUT", "Ottery Underwriting Ltd": "OTTERY UW LTD"}
SALVAGE = "BRACKENHOLME SALV"
CAUSES = [("Hit third party in rear", 0.15), ("Third party hit insured in rear", 0.11), ("Collision at junction", 0.13),
          ("Reversing", 0.17), ("Hit parked vehicle", 0.10), ("Hit fixed object", 0.12), ("Changing lanes", 0.07),
          ("Narrow road / passing", 0.09), ("Hit by third party (other)", 0.04), ("Animal", 0.02)]
MAKES = ["DAF LF 180 FA 7.5t", "Iveco Eurocargo 75E16", "MAN TGL 7.150 4x2 BL"]
CAR_MAKES = ["Skoda Octavia Estate 2.0 TDI", "Ford Focus 1.0 EcoBoost", "Kia Niro 1.6 GDi HEV", "Vauxhall Astra 1.2"]
HDR_FILL = PatternFill("solid", fgColor="D9E1F2")


def reg_nospace(r):
    return r.replace(" ", "")


def first_reg(reg, rng):
    """A plausible first-registration date from the registration's age identifier."""
    age = int(reg[2:4])
    if age < 50:
        a = dt.date(2000 + age, 3, 1)
        b = dt.date(2000 + age, 8, 31)
    else:
        a = dt.date(2000 + age - 50, 9, 1)
        b = dt.date(2000 + age - 49, 2, 28)
    return a + dt.timedelta(days=int(rng.integers(0, (b - a).days + 1)))


def car_reg(rng, used):
    letters = "ABCDEFGHJKLMNOPRSTUVWXYZ"
    while True:
        r = "%s%s%s %s" % (rng.choice(list("NSLY")), rng.choice(list(letters)), rng.choice(["20", "70", "21", "71", "22",
                                                                                              "72", "23", "73", "24"]),
                           "".join(rng.choice(list(letters), 3)))
        if r not in used:
            used.add(r)
            return r


def notify_lag(rng):
    u, acc = rng.random(), 0.0
    for lag, p in P.NOTIFY_LAG:
        acc += p
        if u <= acc:
            return lag
    return P.NOTIFY_LAG[-1][0]


def listing_rows(W, rng):
    """The truck collisions, a second notification of some of them, notifications later withdrawn, and the company
    cars' claims, numbered in notification order."""
    regs = {v["reg"]: v for v in W["vehicles"]}
    by_reg_days = {}
    for r in W["runs"]:
        by_reg_days.setdefault(r["reg"], []).append(r)
    rows = []
    for c in W["claims"]:
        c["notified"] = c["date"] + dt.timedelta(days=notify_lag(rng))
        m = int(round(c["time_h"] * 12)) * 5
        c["time_txt"] = "%02d:%02d" % (m // 60 % 24, m % 60)
        c["cause"] = CAUSES[int(rng.choice(len(CAUSES), p=[p for _, p in CAUSES]))][0]
        if c["notified"] <= P.LISTING_AS_AT:
            rows.append({"kind": "truck", "c": c, "notified": c["notified"]})
            if rng.random() < P.P_DUP_NOTIFY:
                rows.append({"kind": "dup", "c": c, "notified": min(c["notified"] + dt.timedelta(days=int(rng.integers(1, 6))),
                                                                     P.LISTING_AS_AT)})
    # notifications withdrawn: a driver's report of an incident that turned out to be none
    nw = int(round(P.P_WITHDRAWN * len(W["claims"])))
    for _ in range(nw):
        run = W["runs"][int(rng.integers(0, len(W["runs"])))]
        a, b = run["journeys"][0][0], run["journeys"][0][1]
        h = float(rng.uniform(a, b))
        m = int(round(h * 12)) * 5
        d = run["date"]
        rows.append({"kind": "withdrawn", "date": d, "time_txt": "%02d:%02d" % (m // 60, m % 60), "reg": run["reg"],
                     "notified": d + dt.timedelta(days=notify_lag(rng)),
                     "cause": CAUSES[int(rng.choice(len(CAUSES), p=[p for _, p in CAUSES]))][0]})
    # company cars: a separate class on the same policy
    used = set(regs)
    cars = [{"reg": car_reg(rng, used), "make": CAR_MAKES[int(rng.integers(0, len(CAR_MAKES)))],
             "use": "Pool" if rng.random() < 0.3 else "Assigned"} for _ in range(P.CARS)]
    W["cars"] = cars
    span = (P.LISTING_AS_AT - P.REC_START).days
    ncar = int(rng.poisson(P.CAR_CLAIMS_PER_YEAR * span / 365.25))
    for _ in range(ncar):
        d = P.REC_START + dt.timedelta(days=int(rng.integers(0, span)))
        h = float(rng.uniform(7.0, 19.5))
        m = int(round(h * 12)) * 5
        lia = rng.choice(["ours", "theirs", "shared", "no_tp"], p=[0.5, 0.3, 0.1, 0.1])
        rows.append({"kind": "car", "date": d, "time_txt": "%02d:%02d" % (m // 60, m % 60),
                     "reg": cars[int(rng.integers(0, len(cars)))]["reg"], "notified": d + dt.timedelta(days=notify_lag(rng)),
                     "lia": str(lia), "cause": CAUSES[int(rng.choice(len(CAUSES), p=[p for _, p in CAUSES]))][0],
                     "tp": P.TP_INSURERS[int(rng.integers(0, len(P.TP_INSURERS)))] if lia != "no_tp" else ""})
    rows = [r for r in rows if r["notified"] <= P.LISTING_AS_AT]
    def inc(r):
        return r["c"]["date"] if "c" in r else r["date"]
    rows.sort(key=lambda r: (r["notified"], inc(r), 0 if r["kind"] == "truck" else 1, r["c"]["reg"] if "c" in r else r["reg"]))
    no = 104000 + int(rng.integers(0, 3000))
    for r in rows:
        no += int(rng.integers(1, 40))
        r["no"] = "RVM%06d" % no
        if r["kind"] == "truck":
            r["c"]["claim_no"] = r["no"]
    for r in rows:
        if r["kind"] == "dup":
            r["dup_of"] = r["c"]["claim_no"]
            r["c"]["dup_no"] = r["no"]
    return rows


FAULT = {"ours": "Fault", "theirs": "Non-fault", "shared": "Split", "no_tp": "No third party"}


def write_listing(path, rows, rng):
    wb = Workbook()
    ws = wb.active
    ws.title = "Claims"
    ws["A1"] = P.INSURER
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Motor fleet claims listing: %s, policy MF22190046" % P.COMPANY
    ws["A3"] = "Incidents from 01/10/2023. As at 31/10/2026. Amounts in GBP."
    head = ["Claim no.", "Notified", "Incident date", "Incident time (UK)", "Registration", "Vehicle", "Cause", "Fault",
            "Own damage", "TP damage", "TP injury", "Third-party insurer", "Status", "TP paid", "TP reserve"]
    ws.append([])
    ws.append(head)
    for c in ws[5]:
        c.font = Font(bold=True)
        c.fill = HDR_FILL
    for r in rows:
        if r["kind"] in ("truck", "dup"):
            c = r["c"]
            if r["kind"] == "truck":
                paid = res = 0.0
                if c["liability"] in ("ours", "shared") and (c["tppd"] or c["tpi"]):
                    tot = (float(np.exp(np.log(1800) + 0.7 * rng.normal())) if c["tppd"] else 0.0) + \
                          (float(np.exp(np.log(6500) + 0.8 * rng.normal())) if c["tpi"] else 0.0)
                    if c["liability"] == "shared":
                        tot *= (1 - c["share"])
                    settled = (P.LISTING_AS_AT - c["notified"]).days > 75 and rng.random() < 0.85
                    paid, res = (round(tot, 2), 0.0) if settled else (round(tot * float(rng.uniform(0, 0.4)), 2),
                                                                     round(tot * float(rng.uniform(0.5, 1.0)), 2))
                status = "Settled" if ((P.LISTING_AS_AT - c["notified"]).days > 90 and rng.random() < 0.8) else "Open"
                ws.append([r["no"], r["notified"], c["date"], c["time_txt"], c["reg"], "HGV 7.5t", c["cause"],
                           FAULT[c["liability"]], "Y" if c["od"] else "N", "Y" if c["tppd"] else "N",
                           "Y" if c["tpi"] else "N", c["tp_insurer"] or "", status, paid, res])
            else:
                ws.append([r["no"], r["notified"], c["date"], c["time_txt"], c["reg"], "HGV 7.5t", c["cause"],
                           "Not assessed", "", "", "", "", "Closed - duplicate of %s" % r["dup_of"], 0.0, 0.0])
        elif r["kind"] == "withdrawn":
            ws.append([r["no"], r["notified"], r["date"], r["time_txt"], r["reg"], "HGV 7.5t", r["cause"], "Not assessed",
                       "", "", "", "", "Withdrawn", 0.0, 0.0])
        else:
            ws.append([r["no"], r["notified"], r["date"], r["time_txt"], r["reg"], "Car", r["cause"], FAULT[r["lia"]],
                       "Y", "Y" if r["lia"] != "no_tp" else "N", "N", r["tp"],
                       "Settled" if (P.LISTING_AS_AT - r["notified"]).days > 90 else "Open", 0.0, 0.0])
    for row in ws.iter_rows(min_row=6):
        row[1].number_format = row[2].number_format = "dd/mm/yyyy"
        row[13].number_format = row[14].number_format = "#,##0.00"
    for col, w in zip("ABCDEFGHIJKLMNO", [12, 11, 12, 10, 11, 9, 28, 13, 6, 6, 6, 30, 28, 11, 11]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A6"
    CM.save_xlsx(wb, path, dt.datetime(2026, 11, 2, 7, 15), "Ravensby Claims MI", company=P.INSURER)


def write_telematics(target, W, rng):
    regs = {v["reg"]: v for v in W["vehicles"]}
    a_rows, b_rows = [], []
    for r in sorted(W["runs"], key=lambda r: (r["date"], regs[r["reg"]]["fleet_no"])):
        d = r["date"]
        if d > P.REC_END:
            continue
        v = regs[r["reg"]]
        a, b, km, _ = r["journeys"][0]
        off = A.bst_offset(d)
        on_m = int(round((a - off) * 60))
        off_m = int(round((b - off) * 60))
        idle = int(rng.integers(8, 41))
        drive = r["drive_min"]
        if d <= TELE_A_END:
            a_rows.append([reg_nospace(v["reg"]), v["fleet_no"], GROUP_OLD[v["depot"]], CM.ddmmyyyy(d),
                           "%02d:%02d" % (on_m // 60, on_m % 60), "%02d:%02d" % (off_m // 60, off_m % 60),
                           "%.1f" % (km / 1.609344), r["nj"], "%d:%02d" % (drive // 60, drive % 60),
                           "%d:%02d" % (idle // 60, idle % 60)])
        if d >= TELE_B_START:
            on = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=on_m)
            of = dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=off_m)
            b_rows.append([v["reg"], v["fleet_no"], GROUP_NEW[v["depot"]], d.isoformat(), on.strftime("%Y-%m-%dT%H:%M:00Z"),
                           of.strftime("%Y-%m-%dT%H:%M:00Z"), "%.1f" % km, r["nj"], drive, idle])
    CM.write_csv(os.path.join(target, FILES["tele_a"]),
                 ["Vehicle", "Fleet No.", "Group", "Date", "First Ignition On (UTC)", "Last Ignition Off (UTC)",
                  "Distance (mi)", "Journeys", "Driving Time", "Idle Time"], a_rows)
    CM.write_csv(os.path.join(target, FILES["tele_b"]),
                 ["registration", "fleet_number", "group", "day_utc", "ignition_on_utc", "ignition_off_utc", "distance_km",
                  "journeys", "driving_minutes", "idle_minutes"], b_rows)
    return len(a_rows), len(b_rows)


def write_register(path, W, rng):
    wb = Workbook()
    ws = wb.active
    ws.title = "Trucks"
    ws.append(["Fleet no.", "Registration", "Depot", "Use", "Make and model", "First registered", "In fleet", "Off fleet",
               "Reason", "Forward sensors"])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HDR_FILL
    rows = []
    for v in W["vehicles"]:
        fr = first_reg(v["reg"], rng)
        inf = max(fr, v["from"])
        rows.append([v["fleet_no"], v["reg"], DEPOT_NAME[v["depot"]], "Spare" if v["spare"] else "Route",
                     MAKES[int(rng.integers(0, len(MAKES)))], fr, inf, v["to"], "Total loss" if v["to"] else None,
                     v["adas"]])
    rows.sort(key=lambda x: (x[0].rstrip("R"), x[0]))
    for x in rows:
        ws.append(x)
    for row in ws.iter_rows(min_row=2):
        for k in (5, 6, 7):
            row[k].number_format = "dd/mm/yyyy"
    for col, w in zip("ABCDEFGHIJ", [9, 11, 22, 7, 22, 12, 11, 11, 10, 17]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    wc = wb.create_sheet("Company cars")
    wc.append(["Registration", "Make and model", "Base", "Use"])
    for c in wc[1]:
        c.font = Font(bold=True)
        c.fill = HDR_FILL
    for c in sorted(W["cars"], key=lambda c: c["reg"]):
        wc.append([c["reg"], c["make"], "Head office, Washington", c["use"]])
    for col, w in zip("ABCD", [11, 28, 24, 9]):
        wc.column_dimensions[col].width = w
    CM.save_xlsx(wb, path, dt.datetime(2026, 10, 30, 11, 2), P.PEOPLE["workshop"])


def bank_holidays():
    ev = [("2023-01-02", "New Year’s Day", "Substitute day"), ("2023-04-07", "Good Friday", ""),
          ("2023-04-10", "Easter Monday", ""), ("2023-05-01", "Early May bank holiday", ""),
          ("2023-05-08", "Bank holiday for the coronation of King Charles III", ""),
          ("2023-05-29", "Spring bank holiday", ""), ("2023-08-28", "Summer bank holiday", ""),
          ("2023-12-25", "Christmas Day", ""), ("2023-12-26", "Boxing Day", ""),
          ("2024-01-01", "New Year’s Day", ""), ("2024-03-29", "Good Friday", ""), ("2024-04-01", "Easter Monday", ""),
          ("2024-05-06", "Early May bank holiday", ""), ("2024-05-27", "Spring bank holiday", ""),
          ("2024-08-26", "Summer bank holiday", ""), ("2024-12-25", "Christmas Day", ""), ("2024-12-26", "Boxing Day", ""),
          ("2025-01-01", "New Year’s Day", ""), ("2025-04-18", "Good Friday", ""), ("2025-04-21", "Easter Monday", ""),
          ("2025-05-05", "Early May bank holiday", ""), ("2025-05-26", "Spring bank holiday", ""),
          ("2025-08-25", "Summer bank holiday", ""), ("2025-12-25", "Christmas Day", ""), ("2025-12-26", "Boxing Day", ""),
          ("2026-01-01", "New Year’s Day", ""), ("2026-04-03", "Good Friday", ""), ("2026-04-06", "Easter Monday", ""),
          ("2026-05-04", "Early May bank holiday", ""), ("2026-05-25", "Spring bank holiday", ""),
          ("2026-08-31", "Summer bank holiday", ""), ("2026-12-25", "Christmas Day", ""),
          ("2026-12-28", "Boxing Day", "Substitute day"), ("2027-01-01", "New Year’s Day", ""),
          ("2027-03-26", "Good Friday", ""), ("2027-03-29", "Easter Monday", ""),
          ("2027-05-03", "Early May bank holiday", ""), ("2027-05-31", "Spring bank holiday", ""),
          ("2027-08-30", "Summer bank holiday", ""), ("2027-12-27", "Christmas Day", "Substitute day"),
          ("2027-12-28", "Boxing Day", "Substitute day")]
    return [{"title": t, "date": d, "notes": n, "bunting": True} for d, t, n in ev]


def write_bh(path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"england-and-wales": {"division": "england-and-wales", "events": bank_holidays()}}, fh,
                  ensure_ascii=False, separators=(",", ":"))


def write_schedule(path, W):
    wb = Workbook()
    ws = wb.active
    ws.title = "Routes"
    ws.append(["Route", "Depot", "Stores", "Departs now (Sep to Apr)", "Departs now (May to Aug)",
               "Departs from 2 Jan 2027", "Planned day (h:mm)", "Planned km"])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HDR_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in sorted(W["routes"], key=lambda r: r["route"]):
        dur_m = int(round(r["dur"] * 60 / 5)) * 5
        ws.append([r["route"], r["depot"], r["stores"], CM.hhmm(r["std"]), CM.hhmm(r["summer"]), CM.hhmm(r["plan"]),
                   "%d:%02d" % (dur_m // 60, dur_m % 60), int(r["km"])])
    for col, w in zip("ABCDEFGH", [9, 7, 7, 12, 12, 12, 10, 9]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    wc = wb.create_sheet("Calendar 2027")
    wc.append(["Date", "Day", "Week", "Deliveries", "Bank holiday"])
    for c in wc[1]:
        c.font = Font(bold=True)
        c.fill = HDR_FILL
    bh = {e["date"]: e["title"] for e in bank_holidays()}
    runs = set(WO.plan_2027())
    d = dt.date(P.FUND_YEAR, 1, 1)
    while d.year == P.FUND_YEAR:
        wc.append([d, d.strftime("%A"), d.isocalendar()[1], "Yes" if d in runs else "No", bh.get(d.isoformat(), "")])
        wc.cell(row=wc.max_row, column=1).number_format = "dd/mm/yyyy"
        d += dt.timedelta(days=1)
    for col, w in zip("ABCDE", [11, 10, 6, 10, 26]):
        wc.column_dimensions[col].width = w
    wc.freeze_panes = "A2"
    CM.save_xlsx(wb, path, dt.datetime(2026, 10, 19, 14, 48), P.PEOPLE["transport_director"])


TOWNS = {"CRA": [("Blyth", "NE24"), ("Ashington", "NE63"), ("Morpeth", "NE61"), ("Bedlington", "NE22"),
                 ("Whitley Bay", "NE26"), ("North Shields", "NE29"), ("Wallsend", "NE28"), ("Alnwick", "NE66"),
                 ("Amble", "NE65"), ("Cramlington", "NE23"), ("Gosforth", "NE3"), ("Seaton Delaval", "NE25")],
         "GAT": [("Gateshead", "NE8"), ("Jarrow", "NE32"), ("South Shields", "NE33"), ("Washington", "NE37"),
                 ("Sunderland", "SR4"), ("Houghton-le-Spring", "DH4"), ("Chester-le-Street", "DH3"),
                 ("Durham", "DH1"), ("Consett", "DH8"), ("Hexham", "NE46"), ("Prudhoe", "NE42"), ("Blaydon", "NE21")],
         "CAR": [("Carlisle", "CA2"), ("Penrith", "CA11"), ("Workington", "CA14"), ("Whitehaven", "CA28"),
                 ("Maryport", "CA15"), ("Cockermouth", "CA13"), ("Keswick", "CA12"), ("Wigton", "CA7"),
                 ("Brampton", "CA8"), ("Kendal", "LA9"), ("Appleby", "CA16"), ("Annan", "DG12")],
         "DAR": [("Darlington", "DL1"), ("Bishop Auckland", "DL14"), ("Newton Aycliffe", "DL5"), ("Stockton", "TS18"),
                 ("Middlesbrough", "TS1"), ("Hartlepool", "TS24"), ("Redcar", "TS10"), ("Northallerton", "DL6"),
                 ("Richmond", "DL10"), ("Spennymoor", "DL16"), ("Barnard Castle", "DL12"), ("Thirsk", "YO7")]}


def write_stores(path, W, rng):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stores"
    ws.append(["Store no.", "Fascia", "Town", "Postcode district", "Route", "Depot", "Delivery window from 2 Jan 2027",
               "Opens"])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HDR_FILL
    no = 3100
    rows = []
    for r in sorted(W["routes"], key=lambda r: r["route"]):
        t0 = r["plan"] + 0.5
        for k in range(r["stores"]):
            no += int(rng.integers(1, 6))
            town, pc = TOWNS[r["depot"]][int(rng.integers(0, 12))]
            arr = t0 + k * (r["dur"] - 1.0) / max(r["stores"], 1)
            lo = int(arr * 4) / 4
            opens = 6.0 if rng.random() < 0.55 else 7.0
            rows.append(["NL%04d" % no, P.FASCIA, town, pc, r["route"], r["depot"],
                         "%s to %s" % (CM.hhmm(lo), CM.hhmm(lo + 1.5)), CM.hhmm(opens)])
    for x in rows:
        ws.append(x)
    for col, w in zip("ABCDEFGH", [9, 15, 18, 9, 9, 7, 16, 7]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    CM.save_xlsx(wb, path, dt.datetime(2026, 9, 24, 10, 31), "Store Operations")


def write_jobs(path, W, rng):
    C = W["claims"]
    rows = []
    for j in sorted(W["jobs"], key=lambda j: j["job"]):
        c = C[j["claim"]]
        ref = c.get("claim_no", "")
        if c.get("dup_no") and rng.random() < 0.3:
            ref = c["dup_no"]          # the engineer's instruction quoted the second notification's number
        if not ref:
            continue                   # not yet on the insurer's listing
        rows.append([j["job"], ref, reg_nospace(j["reg"]) if rng.random() < 0.18 else j["reg"], j["site"],
                     "Total loss" if j["kind"] == "total loss" else "Accident repair", CM.ddmmyyyy(j["in"]),
                     CM.ddmmyyyy(j["out"])])
    CM.write_csv(path, ["Job No", "Claim Ref", "Registration", "Site", "Job Type", "Date In", "Date Completed"], rows)
    return rows


COST_CENTRE = {"Washington": "4410-NE", "Carlisle": "4410-CA", "Stockton": "4410-TS"}


def write_ap(path, W):
    C = W["claims"]
    jobs = {j["job"]: j for j in W["jobs"]}
    rows = []
    for x in sorted(W["invoices"], key=lambda x: x["ap_doc"]):
        if not C[x["claim"]].get("claim_no"):
            continue
        net = x["net"]
        vat = float(np.round(net * P.VAT + 1e-9, 2))
        rows.append([x["ap_doc"], CM.ddmmyyyy(x["posted"]), "BRA014", P.BODYSHOP, x["job"], CM.ddmmyyyy(x["inv_date"]),
                     x["desc"], "%.2f" % net, "%.2f" % vat, "%.2f" % (net + vat), COST_CENTRE[jobs[x["job"]]["site"]],
                     x["posted"].strftime("%Y-%m")])
    CM.write_csv(path, ["Doc No", "Posting Date", "Supplier", "Supplier Name", "Supplier Ref", "Invoice Date",
                        "Description", "Net", "VAT", "Gross", "Cost Centre", "Period"], rows)
    return rows


def write_bank(path, W, rng):
    C = W["claims"]
    ev = []
    for r in W["receipts"]:
        c = C[r["claim"]]
        ref = r["payer_ref"] + ((" " + c["claim_no"]) if (r["quotes_ours"] and c.get("claim_no")) else "")
        r["narrative"] = "%-18s %s" % (BANK_NAME[r["payer"]], ref)
        ev.append((r["date"], 0, "BAC", r["narrative"], r["amount"], None))
    sv = 10200 + int(rng.integers(0, 400))
    for c in C:
        if c["od"] and c["write_off"]:
            d = c["date"] + dt.timedelta(days=int(rng.integers(28, 70)))
            if P.RECEIPTS_FROM <= d <= P.LISTING_AS_AT:
                sv += int(rng.integers(3, 30))
                ev.append((d, 0, "BAC", "%-18s SV%d" % (SALVAGE, sv), float(np.round(rng.uniform(2800, 8900), 2)), None))
    # month-end sweep to the main account
    d = P.RECEIPTS_FROM
    while d <= P.LISTING_AS_AT:
        nxt = (d.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        last = nxt - dt.timedelta(days=1)
        while last.weekday() > 4:
            last -= dt.timedelta(days=1)
        if last <= P.LISTING_AS_AT:
            ev.append((last, 1, "TFR", "TFR TO 40-11-62 31827744", None, "sweep"))
        d = nxt
    ev.sort(key=lambda e: (e[0], e[1], e[3]))
    bal = 5000.00
    rows = []
    for d, _, typ, desc, pin, flag in ev:
        if flag == "sweep":
            out = round(bal - 5000.00, 2)
            if out <= 0:
                continue
            bal = 5000.00
            rows.append([CM.ddmmyyyy(d), typ, desc, "", "%.2f" % out, "%.2f" % bal])
        else:
            bal = round(bal + pin, 2)
            rows.append([CM.ddmmyyyy(d), typ, desc, "%.2f" % pin, "", "%.2f" % bal])
    CM.write_csv(path, ["Date", "Type", "Description", "Paid in", "Paid out", "Balance"], rows)
    return rows


def build(target, seed=P.SEED, W=None):
    """Simulate (unless a world is passed), cost, and write every data file; returns the world."""
    if W is None:
        W = WO.simulate(seed)
    CO.build(W, seed)
    rng = np.random.default_rng([seed, 7])
    for r in W["routes"]:
        r["stores"] = int(rng.integers(4, 8))
    rows = listing_rows(W, rng)
    W["listing"] = rows
    write_listing(os.path.join(target, FILES["listing"]), rows, rng)
    W["n_tele"] = write_telematics(target, W, rng)
    write_register(os.path.join(target, FILES["register"]), W, rng)
    write_schedule(os.path.join(target, FILES["schedule"]), W)
    write_stores(os.path.join(target, FILES["stores"]), W, rng)
    W["job_rows"] = write_jobs(os.path.join(target, FILES["jobs"]), W, rng)
    W["ap_rows"] = write_ap(os.path.join(target, FILES["ap"]), W)
    W["bank_rows"] = write_bank(os.path.join(target, FILES["bank"]), W, rng)
    write_bh(os.path.join(target, FILES["bh"]))
    import docs as DC
    DC.handbook(os.path.join(target, FILES["handbook"]))
    DC.terms(os.path.join(target, FILES["terms"]))
    return W
