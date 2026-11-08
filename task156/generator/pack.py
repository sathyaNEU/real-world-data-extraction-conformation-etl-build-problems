"""The pack under target/, written from the clean truth with the organisation's own mess: the back office's status
export across its June 2025 migration (UTC, re-sent notifications, the heartbeat lag), the register with both IDs,
the two contractors' work orders in Irish time, the visit schedule in two layouts, the supply interruption log, the
2026 session export, the concession's Schedules 4 and 6, the renewal programme, the tariff and the survey."""
import csv
import datetime as dt
import io
import os

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table

import estim as ES
import officepdf
import postprocess as PP
import world as W

ORG = "Ardvane Charge DAC"
NMCP = "North Midlands Charging Partnership"
F_STATUS = "connector_status_history_2023-2026.csv"
F_SESS = "charging_sessions_2026.csv"
F_DSO = "supply_interruptions_2023-2026.csv"
F_REG = "charge_point_register.xlsx"
F_WO = "work_orders_2023-2026.xlsx"
F_PPM = "planned_maintenance_schedule.xlsx"
F_SURVEY = "customer_survey_2026.xlsx"
F_SCHED = "concession_agreement_schedules_4_and_6.pdf"
F_PROG = "asset_renewal_programme_2027.pdf"
F_TARIFF = "tariff_schedule_2026.pdf"
FILES = [F_STATUS, F_SESS, F_DSO, F_REG, F_WO, F_PPM, F_SURVEY, F_SCHED, F_PROG, F_TARIFF]
DISTRACTORS = [F_SURVEY, F_TARIFF]
EXPORT = dt.datetime(2026, 11, 2, 7, 40, tzinfo=dt.timezone.utc)

ERRORS = [("GroundFailure", "KX-3107", "Insulation fault on CCS cable %d, cable assembly replaced, insulation test passed."),
          ("HighTemperature", "KX-2210", "Repeated over-temperature trips, cooling fan replaced and filters cleaned."),
          ("PowerSwitchFailure", "KX-4102", "DC contactor K%d failed, contactor replaced, unit tested OK."),
          ("InternalError", "KX-1504", "Power module %d fault, module replaced, unit tested."),
          ("OverCurrentFailure", "KX-4415", "Output fuse F%d open, fuse replaced and output checked."),
          ("EVCommunicationError", "KX-5023", "Handshake failures on connector %d, CCS cable replaced, test charge OK.")]
HANG_TEXT = ["Charger unresponsive, display frozen, not communicating. Power cycled at unit isolator, rebooted and back online. No fault found.",
             "Unit offline, screen frozen on welcome page. Reset at local isolator, back in service. NFF.",
             "Customer reported charger not responding. Controller hung. Isolated and re-energised, rebooted OK, test charge OK.",
             "No comms to back office, controller not responding. Power cycled, unit online. Nothing found on inspection.",
             "Screen frozen and no response to remote reset. Unit isolated and restarted on site, online. NFF.",
             "Unit showing offline. On arrival display frozen. Power cycled, unit back online and charging."]
SERVICE_TEXT = ["RC50 monthly cabinet service: DC module air filters cleaned, contactors inspected, returned to service.",
                "RC50 monthly service. Filters cleaned, terminations checked, unit returned to service.",
                "Monthly RC50 cabinet check: filters, fans and contactors inspected. OK.",
                "RC50 monthly cabinet service completed, filters replaced (blocked), unit OK."]
REPAIR_TEXT = ["RC50 power module PM%d failed, module replaced, unit tested.", "RC50 AC input contactor replaced, tested OK.",
               "RC50 DC output relay fault, relay replaced, unit tested.", "RC50 power module PM%d tripping, module reseated and fan replaced."]
OTHER_TEXT = ["RC50 CHAdeMO cable damaged, cable replaced.", "RC50 card reader not reading, reader replaced.",
              "RC50 screen cracked, display replaced.", "RC50 CCS holster broken, holster replaced.",
              "RC50 emergency stop latched, reset after inspection, no damage found.", "RC50 RFID reader intermittent, reader replaced.",
              "RC50 CHAdeMO connector latch broken, connector replaced."]
VISIT_TEXT = ["Planned maintenance visit: electrical test and inspection of supply pillar and all charge points, filters cleaned, connectors inspected.",
              "Planned visit. Periodic inspection and test of pillar and chargers, cables and connectors checked, filters cleaned.",
              "Site planned maintenance: RCD and insulation tests, cabinet filters, cable inspection. All units returned to service."]


def iso_z(t):
    return W.utc(t).strftime("%Y-%m-%dT%H:%M:%SZ")


def loc(t, fmt="%d/%m/%Y %H:%M"):
    return W.local(t).strftime(fmt)


def write_csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    w.writerows(rows)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


# ------------------------------------------------------------------------------------------- the status export
def status_rows(H):
    rng = np.random.default_rng([W.SEED, 501])
    out = []
    umap = {u["uid"]: u for u in H["units"]}
    for uid in sorted(H["runs"]):
        u = umap[uid]
        run = H["runs"][uid]
        rows = ES.rows_from_intervals(run["iv"], run["start"])
        faults = [x for x in run["iv"] if x[2] == "Faulted"]
        mig_done = False
        for t, st in rows:
            if t >= W.MIGRATION and not mig_done:
                mig_done = True
                cur = [s for tt, s in rows if tt < W.MIGRATION]
                out.append((W.MIGRATION + int(rng.integers(120, 2400)), u["new_id"], cur[-1] if cur else "Available", "NoError", "",
                            "StatusNotification"))
            cp = u["old_id"] if t < W.MIGRATION else u["new_id"]
            err, vend = "NoError", ""
            if st == "Faulted":
                if u["model"] == "HX150":
                    e = ERRORS[int(rng.integers(0, len(ERRORS)))]
                    err, vend = e[0], e[1]
                else:
                    err, vend = ["InternalError", "PowerSwitchFailure", "ReaderFailure", "OtherError"][int(rng.integers(0, 4))], \
                        "T50-%02X" % int(rng.integers(16, 250))
            src = "ConnectionMonitor" if st == "Offline" else "StatusNotification"
            out.append((t, cp, st, err, vend, src))
            if src == "StatusNotification" and rng.random() < 0.025:
                out.append((t + int(rng.integers(1, 41)), cp, st, err, vend, src))
        del faults
        if not mig_done and run["start"] < W.MIGRATION:
            out.append((W.MIGRATION + int(rng.integers(120, 2400)), u["new_id"], "Available", "NoError", "", "StatusNotification"))
    out.sort(key=lambda r: (r[0], r[1]))
    return out


def write_status(H, target):
    rows = status_rows(H)
    write_csv(os.path.join(target, F_STATUS),
              ["timestamp_utc", "charge_point_id", "connector_id", "status", "error_code", "vendor_error_code", "source"],
              [(iso_z(t), cp, 0, st, err, vend, src) for t, cp, st, err, vend, src in rows])
    return len(rows)


# ------------------------------------------------------------------------------------------ the session export
def session_records(H, charges):
    """Every record the back office holds for the 2026 charges, with its session number, and a September page
    the export sent twice."""
    rng = np.random.default_rng([W.SEED, 601])
    umap = {u["uid"]: u for u in H["units"]}
    recs = []
    for c in charges:
        for r in c["recs"]:
            recs.append((r["start"], c["uid"], c["connector"], r["stop"], r["m0"], r["m1"], r["token"]))
    recs.sort(key=lambda x: (x[0], x[1], x[2]))
    sid = 48211000 + int(rng.integers(100, 900))
    out = []
    for start, uid, con, stop, m0, m1, tok in recs:
        sid += int(rng.integers(1, 7))
        out.append([sid, umap[uid]["new_id"], con, iso_z(start), iso_z(stop), m0, m1, "%.3f" % ((m1 - m0) / 1000.0), tok])
    page_a = W.ts(dt.datetime(2026, 9, 14, 6, 0, tzinfo=dt.timezone.utc))
    page_b = W.ts(dt.datetime(2026, 9, 15, 18, 0, tzinfo=dt.timezone.utc))
    hubs = sorted(set(u["hub"] for u in H["units"]))
    resent_hubs = set(hubs[int(i)] for i in rng.choice(len(hubs), 11, replace=False))
    resent = [list(r) for r in out if page_a <= W.ts(dt.datetime.strptime(r[3], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)) < page_b
              and [u for u in H["units"] if u["new_id"] == r[1]][0]["hub"] in resent_hubs]
    out = out + resent
    out.sort(key=lambda r: (r[3], r[0]))
    return out, len(resent), sorted(resent_hubs)


def write_sessions(H, charges, target):
    rows, nres, rh = session_records(H, charges)
    write_csv(os.path.join(target, F_SESS), ["session_id", "charge_point_id", "connector_id", "start_time_utc", "stop_time_utc",
                                             "meter_start_wh", "meter_stop_wh", "energy_kwh", "id_tag"], rows)
    return len(rows), nres, rh


# -------------------------------------------------------------------------------------------- the supply log
CAUSES = ["Fault on MV overhead line", "LV underground cable fault", "Storm damage to overhead network", "Transformer fault",
          "Third party damage", "Fault, cause not found", "Protection operation, network restored"]


def write_dso(H, target, mprn):
    rng = np.random.default_rng([W.SEED, 701])
    rows = []
    ref = 18000 + int(rng.integers(0, 900))
    for h in H["hubs"]:
        for e in H["plans"][h["code"]]:
            if e["kind"] != "dso":
                continue
            s = e["s"] + int(rng.integers(-150, 151))
            t = e["e"] + int(rng.integers(-150, 151))
            rows.append((s, t, h["code"], e["planned"]))
    rows.sort()
    out = []
    for s, t, code, planned in rows:
        ref += int(rng.integers(3, 60))
        y = W.local(s).year % 100
        cause = "Planned works (notified)" if planned else CAUSES[int(rng.integers(0, len(CAUSES)))]
        out.append(["INC-%02d-%06d" % (y, ref), code, mprn[code], loc(s, "%Y-%m-%d %H:%M"), loc(t, "%Y-%m-%d %H:%M"),
                    "Y" if planned else "N", cause])
    write_csv(os.path.join(target, F_DSO), ["dso_reference", "hub_code", "mprn", "interruption_start_irish_time",
                                            "supply_restored_irish_time", "planned", "cause"], out)
    return len(out)


# ------------------------------------------------------------------------------------------------- workbooks
HEAD_FONT = Font(name="Calibri", bold=True, size=11)
HEAD_FILL = PatternFill("solid", fgColor="DDEBF7")


def sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = HEAD_FONT
        c.fill = HEAD_FILL
        c.alignment = Alignment(vertical="center")
    for r in rows:
        ws.append(r)
    for i, w in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    ws.freeze_panes = "A2"


def save_book(wb, path, creator, last_by, created, modified):
    wb.save(path)
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=creator)


def write_register(H, target):
    """The asset register as the network assets team keeps it: the hubs first, then every charge point."""
    rng = np.random.default_rng([W.SEED, 801])
    wb = openpyxl.Workbook()
    ws2 = wb.active
    ws2.title = "Hubs"
    mprn = {}
    rows = []
    for h in sorted(H["hubs"], key=lambda h: h["code"]):
        mprn[h["code"]] = "10%09d" % int(rng.integers(100000000, 999999999))
        rc = [u for u in H["units"] if u["hub"] == h["code"] and u["model"] == "RC50"][0]
        cap = int(rng.choice([200, 250, 315, 400, 500, 630, 800])) if h["kind"] != "M" else int(rng.choice([630, 800, 1000]))
        rows.append([h["code"], h["name"], h["county"], h["site"], mprn[h["code"]], cap, dt.date.fromisoformat(rc["commissioned"])])
    sheet(ws2, ["Hub code", "Hub", "County", "Site type", "MPRN", "Import capacity (kVA)", "Opened"], rows,
          [10, 28, 11, 24, 13, 20, 12])
    for r in ws2.iter_rows(min_row=2, min_col=7, max_col=7):
        for c in r:
            c.number_format = "dd/mm/yyyy"
    ws = wb.create_sheet("Charge points")
    rows = []
    for h in H["hubs"]:
        for u in sorted([u for u in H["units"] if u["hub"] == h["code"]], key=lambda u: u["bay"]):
            d = dt.date.fromisoformat(u["commissioned"])
            rows.append([u["serial"], u["new_id"], u["old_id"], h["code"], u["bay"], u["make"], u["model"], u["kw"], u["connectors"],
                         d, "In service"])
    sheet(ws, ["Asset serial", "Charge point ID", "Previous ID (to 09/06/2025)", "Hub code", "Bay", "Make", "Model",
               "Rated output (kW)", "Connectors", "Commissioned", "Status"], rows, [18, 16, 24, 10, 6, 10, 9, 16, 11, 13, 11])
    for r in ws.iter_rows(min_row=2, min_col=10, max_col=10):
        for c in r:
            c.number_format = "dd/mm/yyyy"
    save_book(wb, os.path.join(target, F_REG), ORG, "Network Assets", "2019-03-12T09:14:31Z", "2026-11-02T08:03:12Z")
    return mprn


def write_work_orders(H, target):
    rng = np.random.default_rng([W.SEED, 901])
    umap = {u["uid"]: u for u in H["units"]}
    hub = {h["code"]: h for h in H["hubs"]}
    jobs = []
    for h in H["hubs"]:
        rc = [u for u in H["units"] if u["hub"] == h["code"] and u["model"] == "RC50"][0]
        for e in H["plans"][h["code"]]:
            if e["kind"] == "visit":
                jobs.append(dict(hub=h["code"], serial="", logged=e["arrive"] - int(rng.integers(3, 11)) * DAY_S,
                                 arrive=e["arrive"], done=e["e"] + int(rng.integers(20, 61)) * 60, kind="visit",
                                 text=VISIT_TEXT[int(rng.integers(0, len(VISIT_TEXT)))], fault=""))
            elif e["kind"] == "service":
                jobs.append(dict(hub=h["code"], serial=rc["serial"], logged=e["arrive"] - int(rng.integers(2, 9)) * DAY_S,
                                 arrive=e["arrive"], done=e["e"] + int(rng.integers(5, 16)) * 60, kind="rc_service",
                                 text=SERVICE_TEXT[int(rng.integers(0, len(SERVICE_TEXT)))], fault=""))
            elif e["kind"] in ("repair", "other"):
                txt = (REPAIR_TEXT if e["kind"] == "repair" else OTHER_TEXT)
                t = txt[int(rng.integers(0, len(txt)))]
                if "%d" in t:
                    t = t % int(rng.integers(1, 5))
                jobs.append(dict(hub=h["code"], serial=rc["serial"], logged=e["fault"] + int(rng.integers(8, 41)) * 60,
                                 arrive=e["arrive"], done=e["e"] + int(rng.integers(3, 12)) * 60, kind="rc_" + e["kind"],
                                 text=t, fault="RC50 fault alarm"))
    for uid, run in sorted(H["runs"].items()):
        u = umap[uid]
        if u["model"] != "HX150":
            continue
        for t, restart, by, arrive in run["hangs"]:
            j = dict(hub=u["hub"], serial=u["serial"], logged=t + 600 + int(rng.integers(8, 41)) * 60, kind="hang", fault="Charger offline")
            if by == "technician":
                j.update(arrive=arrive, done=restart + int(rng.integers(2, 9)) * 60, text=HANG_TEXT[int(rng.integers(0, len(HANG_TEXT)))])
            else:
                j.update(arrive=None, done=restart + int(rng.integers(10, 90)) * 60, text="Unit back online before attendance. No visit required.")
            jobs.append(j)
        for t, arrive, done in run["faults"]:
            e = ERRORS[int(rng.integers(0, len(ERRORS)))]
            txt = e[2] % int(rng.integers(1, 3)) if "%d" in e[2] else e[2]
            jobs.append(dict(hub=u["hub"], serial=u["serial"], logged=t + int(rng.integers(8, 41)) * 60, arrive=arrive,
                             done=done + int(rng.integers(3, 12)) * 60, kind="fault", text=txt, fault="Charger faulted"))
    jobs.sort(key=lambda j: (j["logged"], j["hub"], j["serial"]))
    A, B = [], []
    na, nb = {}, 104000 + int(rng.integers(100, 800))
    codesA = {"visit": "PM2", "rc_service": "PM1", "rc_repair": "R1", "rc_other": "R1", "hang": "R2", "fault": "R1"}
    codesB = {"visit": ("Planned", "PM-SITE"), "rc_service": ("Planned", "PM-RC50"), "rc_repair": ("Corrective", "CM-RC50"),
              "rc_other": ("Corrective", "CM-RC50"), "hang": ("Corrective", "CM-NR"), "fault": ("Corrective", "CM-HW")}
    for j in jobs:
        eng = rng.integers(1, 10)
        site = hub[j["hub"]]["name"]
        if j["logged"] < W.CONTRACT_B:
            y = W.local(j["logged"]).year % 100
            na[y] = na.get(y, 0) + int(rng.integers(1, 4))
            A.append(["LES-%02d-%04d" % (y, na[y]), loc(j["logged"], "%d/%m/%Y"), loc(j["logged"], "%H:%M"), site, j["serial"],
                      codesA[j["kind"]], j["fault"], j["text"], loc(j["arrive"]) if j["arrive"] else "",
                      loc(j["done"]), "LE%02d" % eng])
        else:
            nb += int(rng.integers(1, 6))
            cat, code = codesB[j["kind"]]
            outcome = "Closed, no visit" if (j["kind"] == "hang" and not j["arrive"]) else "Completed"
            B.append(["WO-%06d" % nb, loc(j["logged"]), j["serial"], j["hub"], cat, code, j["text"],
                      loc(j["arrive"]) if j["arrive"] else "", loc(j["done"]), "CT%02d" % (eng + 10), outcome])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Lissane to Mar 2024"
    sheet(ws, ["Job ref", "Date logged", "Time logged", "Site", "Charger serial", "Job type", "Reported", "Work done", "Arrived",
               "Completed", "Engineer"], A, [13, 12, 11, 27, 17, 9, 17, 70, 17, 17, 9])
    ws2 = wb.create_sheet("Corran from Apr 2024")
    sheet(ws2, ["Work order", "Logged", "Asset", "Site code", "Category", "Code", "Description", "Attended", "Closed",
                "Technician", "Outcome"], B, [11, 17, 17, 10, 11, 9, 70, 17, 17, 11, 16])
    save_book(wb, os.path.join(target, F_WO), ORG, "Maintenance Coordinator", "2023-01-09T10:02:44Z", "2026-11-02T08:11:37Z")
    return len(A), len(B)


DAY_S = W.DAY


def write_ppm(H, target):
    rng = np.random.default_rng([W.SEED, 951])
    wb = openpyxl.Workbook()
    first = True
    for y in (2023, 2024, 2025):
        ws = wb.active if first else wb.create_sheet(str(y))
        if first:
            ws.title = str(y)
            first = False
        rows = []
        for h in sorted(H["hubs"], key=lambda h: h["code"]):
            ds = [e["date"] for e in H["plans"][h["code"]] if e["kind"] == "visit" and e["date"].year == y]
            cells = [d for d in ds] + [None] * (6 - len(ds))
            rows.append([h["code"], h["name"]] + cells + ["08:30-14:30", "Yes"])
        sheet(ws, ["Hub code", "Hub", "Visit 1", "Visit 2", "Visit 3", "Visit 4", "Visit 5", "Visit 6", "Window", "Notified"],
              rows, [10, 28, 11, 11, 11, 11, 11, 11, 12, 9])
        for r in ws.iter_rows(min_row=2, min_col=3, max_col=8):
            for c in r:
                c.number_format = "dd/mm/yyyy"
    for label, year in (("2026", 2026), ("2027 plan", 2027)):
        ws = wb.create_sheet(label)
        rows = []
        for h in sorted(H["hubs"], key=lambda h: h["code"]):
            if year == 2026:
                ev = [e for e in H["plans"][h["code"]] if e["kind"] == "visit" and e["date"].year == 2026]
                for e in ev:
                    status = "Completed" if e["ws"] < W.HIST_END else "Planned"
                    rows.append([h["code"], h["name"], e["date"], "08:30", "14:30", e["notified"], status])
            else:
                for d in W.plan_2027(h):
                    rows.append([h["code"], h["name"], d, "08:30", "14:30", None, "Planned"])
        rows.sort(key=lambda r: (r[2], r[0]))
        sheet(ws, ["Hub code", "Hub", "Visit date", "Window from", "Window to", "Notified to partnership", "Status"], rows,
              [10, 28, 12, 12, 11, 22, 11])
        for r in ws.iter_rows(min_row=2, min_col=3, max_col=3):
            for c in r:
                c.number_format = "dd/mm/yyyy"
        for r in ws.iter_rows(min_row=2, min_col=6, max_col=6):
            for c in r:
                c.number_format = "dd/mm/yyyy"
    save_book(wb, os.path.join(target, F_PPM), "Corran EV Services", ORG, "2022-11-21T14:26:03Z", "2026-10-29T16:48:20Z")


SURVEY_COMMENTS = ["Quick charge, no problems.", "Had to try the second charger, first one would not start.", "Card reader slow.",
                   "Good location, toilets nearby.", "Charger was offline, used the other one.", "Price has gone up again.",
                   "App would not connect, used contactless.", "Bays blocked by petrol cars.", "Fast and easy.",
                   "Screen hard to read in sunshine.", "Waited 20 minutes for a free charger.", "Cable very heavy.",
                   "Charged fine but slower than advertised.", "Would like more chargers here.", "Lighting poor at night."]


def write_survey(H, target):
    rng = np.random.default_rng([W.SEED, 1001])
    rows = []
    rid = 3100 + int(rng.integers(0, 400))
    codes = [h["code"] for h in H["hubs"]]
    wts = np.array([h["hx_charges"] * len(h["comm"]) + h["rc_charges"] for h in H["hubs"]], float)
    wts /= wts.sum()
    t = W.ts(dt.datetime(2026, 3, 2, tzinfo=dt.timezone.utc))
    end = W.ts(dt.datetime(2026, 6, 28, tzinfo=dt.timezone.utc))
    while t < end:
        t += int(rng.exponential(DAY_S / 11.0))
        rid += int(rng.integers(1, 4))
        code = codes[int(rng.choice(len(codes), p=wts))]
        sat = int(np.clip(round(rng.normal(3.9, 0.9)), 1, 5))
        rows.append([rid, W.local(t).replace(tzinfo=None, microsecond=0), code,
                     ["Rapid (150 kW)", "Fast (50 kW)", "Not sure"][int(rng.choice(3, p=[0.66, 0.24, 0.10]))], sat,
                     "Yes" if rng.random() < 0.86 else "No", int(np.clip(round(rng.normal(7.2, 2.0)), 0, 10)),
                     SURVEY_COMMENTS[int(rng.integers(0, len(SURVEY_COMMENTS)))] if rng.random() < 0.12 else None])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Responses"
    sheet(ws, ["Response ID", "Submitted", "Hub code", "Charger used", "Overall satisfaction (1-5)", "Started first time",
               "Likely to recommend (0-10)", "Comment"], rows, [12, 18, 10, 15, 24, 18, 25, 55])
    for r in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for c in r:
            c.number_format = "dd/mm/yyyy hh:mm"
    save_book(wb, os.path.join(target, F_SURVEY), ORG, "Customer Experience", "2026-03-02T09:30:11Z", "2026-07-06T11:17:45Z")
    return len(rows)


# ------------------------------------------------------------------------------------------------- documents
SS = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13, spaceAfter=6, spaceBefore=4)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, spaceAfter=3, spaceBefore=7)
BODY = ParagraphStyle("body", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.2, spaceAfter=4, leading=12)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8, spaceAfter=2)
CELL = ParagraphStyle("cell", parent=BODY, fontSize=8, spaceAfter=0, leading=10)


def P(t, st=BODY):
    return Paragraph(t, st)


def T(rows, widths_mm):
    return Table([[P(c, CELL) if isinstance(c, str) else c for c in r] for r in rows], colWidths=[w * 72 / 25.4 for w in widths_mm])


def aware(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def write_schedules(target):
    story = [P("CONCESSION AGREEMENT FOR PUBLIC RAPID CHARGING (NORTH MIDLANDS)", H1),
             P("Between the North Midlands Charging Partnership and Ardvane Charge DAC. Consolidated text of Schedules 4 and 6 "
               "incorporating Variation No. 2 (March 2024).", BODY),
             T([["Document", "Version", "Date", "Supersedes"], ["NMCP/CA/2021/03, Schedules 4 and 6", "3 (consolidated)", "14/03/2024",
                                                               "Version 2 of 02/09/2022"]], [70, 30, 25, 45]),
             P("Schedule 4: Availability", H2),
             P("4.1 This Schedule applies to every high-power charge point, being a charge point rated at 150 kW or more, in service "
               "at a Hub at any time in a Contract Year, including any charge point brought into service during that Contract Year.", BODY),
             P("4.2 A Contract Year runs from 00:00 on 1 January to 24:00 on 31 December, Irish time.", BODY),
             P("4.3 The Availability of a high-power charge point for a Contract Year is A = (T - E - D) / (T - E), where T is the minutes "
               "of the Contract Year in which the charge point is in service, E is the minutes of Excluded Events, and D is the minutes "
               "outside Excluded Events in which the Operator's back office records the charge point as Faulted, Unavailable or Offline. "
               "Excluded Events are (a) planned maintenance within a window notified to the Partnership at least seven days in advance, "
               "and (b) interruptions of the supply to the Hub as recorded by the distribution system operator. Each Excluded Event "
               "includes the 30 minutes following the end of the notified window or the restoration of supply.", BODY),
             P("4.4 The Availability Standard is 99 per cent for each high-power charge point in each Contract Year.", BODY),
             P("4.5 The Operator reports each high-power charge point's Availability monthly from the back office records, and the "
               "Partnership may audit those records at any time on five working days' notice.", BODY),
             P("4.6 Availability Plan. By 30 November in each year the Operator shall submit an Availability Plan for the following "
               "Contract Year. The Plan shall list each Hub at which the Operator forecasts that any high-power charge point will fall "
               "below the Availability Standard in that Contract Year, the forecast being made on the asset base set by the Partnership's "
               "approved renewal programme for that year, and shall set out the actions the Operator proposes at each listed Hub. The "
               "Plan is reviewed at the Partnership's annual concession review in December.", BODY),
             P("4.7 A Hub listed in an accepted Plan is managed under the remedial actions agreed for it. For any other Hub, a "
               "high-power charge point whose Availability falls below the Availability Standard attracts the service credits in "
               "Table 4.1.", BODY),
             T([["Availability in the Contract Year", "Service credit (per charge point)"],
                ["98.5 per cent to below 99 per cent", "EUR 1,500"], ["98 per cent to below 98.5 per cent", "EUR 4,000"],
                ["Below 98 per cent", "EUR 9,000 and a remedial plan within 30 days"]], [80, 80]),
             P("Table 4.1 Service credits", SMALL),
             P("4.8 Nothing in this Schedule relieves the Operator of its obligations under Schedule 3 (Maintenance).", BODY),
             P("Schedule 6: Reporting", H2),
             P("6.1 With each Availability Plan the Operator returns, for each Hub, the charges begun at its high-power charge points "
               "in the reporting period and the energy those charges delivered, in the return format the Partnership issues.", BODY),
             P("6.2 A charge is a vehicle's connection to a connector of a charge point during which energy was delivered, from "
               "connection to disconnection. A charge is counted once, in the month in which it began, Irish time.", BODY),
             P("6.3 The energy of a charge is the energy the charge point's meter registered for it. Energy is reported in MWh.", BODY),
             P("6.4 For the Availability Plan submitted in 2026 the reporting period is 1 January to 31 October 2026.", BODY),
             P("6.5 The Operator retains the back office records underlying each return for six years.", BODY),
             Spacer(1, 8),
             P("Signed for the Partnership: concession manager. Signed for the Operator: managing director. Consolidated text "
               "issued by the Partnership's concession office, 14 March 2024.", SMALL)]
    officepdf.build(os.path.join(target, F_SCHED), story, "Concession Agreement: Schedules 4 and 6", NMCP,
                    "Availability and reporting schedules, consolidated text", "North Midlands Charging Partnership, concession office",
                    aware("2024-03-14T10:12:07Z"), aware("2024-03-14T10:26:51Z"), producer="LibreOffice 7.6")


def write_programme(H, target):
    hubs = {h["code"]: h for h in H["hubs"]}
    rows = [["Hub code", "Hub", "RC50 serial", "Works date", "New Korrant HX150"]]
    for code in sorted(W.WORKS, key=lambda c: (W.WORKS[c], c)):
        rc = [u for u in H["units"] if u["hub"] == code and u["model"] == "RC50"][0]
        d = dt.date.fromisoformat(W.WORKS[code])
        rows.append([code, hubs[code]["name"], rc["serial"], d.strftime("%d/%m/%Y"),
                     "Yes, commissioned on the works date" if hubs[code]["kind"] in W.NEW_UNIT_KINDS else "No"])
    story = [P("NORTH MIDLANDS CHARGING PARTNERSHIP", H1),
             P("Asset Renewal Programme 2027", H2),
             P("Approved by the Partnership Board on 21 October 2026. Issued to Ardvane Charge DAC under the Concession Agreement.", BODY),
             P("1. Purpose", H2),
             P("Tavrin has given notice that it will withdraw parts and software support for the RC50 50 kW charger from 31 December "
               "2026. Eighteen of the network's thirty RC50 units are retained for 2027 under a parts agreement the Operator holds for "
               "used power modules; the remaining twelve are removed under this programme, and at ten of those Hubs a Korrant HX150 is "
               "installed in the RC50's bay. The programme sets the network's asset base for the 2027 Contract Year.", BODY),
             P("2. Schedule of works", H2),
             T(rows, [18, 44, 30, 22, 50]),
             P("3. Works", H2),
             P("At each Hub the contractor isolates the supply on the works date, disconnects and removes the RC50 and, where shown, "
               "installs and commissions the new HX150 the same day. Works start at 09:30 and the Hub is expected back in service by "
               "15:00. The works dates are notified under Schedule 4 as planned maintenance.", BODY),
             P("4. Retained RC50 units", H2),
             P("The retained RC50 units continue under the Operator's maintenance arrangements for 2027. The Partnership will review "
               "them in the second quarter of 2027 for the 2028 programme.", BODY),
             P("5. Risks", H2),
             T([["Risk", "Owner", "Mitigation"],
                ["HX150 delivery slips past a works date", "Operator", "Korrant has confirmed the ten units ex stock; a slipped unit is installed on the next free date"],
                ["Supply works needed at a Hub", "Partnership", "Import capacity checked for every Hub; no upgrade required"],
                ["Customer disruption on works days", "Operator", "Works dates published in the app seven days ahead"]], [55, 25, 90]),
             P("6. Funding and contacts", H2),
             P("The works are funded under the Partnership's capital allocation for 2026. Queries to the concession office.", BODY),
             P("Document control", H2),
             T([["Version", "Date", "Status", "By"], ["0.3", "07/10/2026", "Draft for the Board", "Concession office"],
                ["1.0", "21/10/2026", "Approved", "Partnership Board"], ["1.1", "22/10/2026", "Issued to the Operator", "Concession office"]],
               [20, 28, 60, 50])]
    officepdf.build(os.path.join(target, F_PROG), story, "Asset Renewal Programme 2027", NMCP, "RC50 removal and HX150 installation",
                    "North Midlands Charging Partnership, Asset Renewal Programme 2027", aware("2026-10-21T15:40:22Z"),
                    aware("2026-10-22T08:05:49Z"), producer="LibreOffice 24.8")


def write_tariff(target):
    story = [P("ARDVANE RAPID: CHARGING TARIFF", H1),
             P("Public rapid charging on the North Midlands network. Effective from 1 March 2026. Prices include VAT.", BODY),
             T([["How you pay", "Price", "Notes"],
                ["Ardvane Rapid app or RFID card", "EUR 0.55 per kWh", "Billed monthly to your account"],
                ["Contactless bank card at the charger", "EUR 0.59 per kWh", "A pre-authorisation of EUR 40.00 is placed on your card and released when the charge is settled"],
                ["Other providers' apps and cards", "Set by your provider", "Roaming partners listed in the app"],
                ["Overstay at motorway hubs", "EUR 0.20 per minute", "From 15 minutes after the end of a charge"]], [50, 35, 85]),
             P("Charges are calculated on the energy registered by the charge point's meter. No connection fee applies.", BODY),
             P("Prices are reviewed each March. Ardvane Charge DAC, customer services.", SMALL)]
    officepdf.build(os.path.join(target, F_TARIFF), story, "Ardvane Rapid charging tariff", ORG, "Public charging prices from 1 March 2026",
                    "Ardvane Charge DAC, tariff from 1 March 2026", aware("2026-02-11T12:03:40Z"), aware("2026-02-11T12:09:02Z"),
                    producer="LibreOffice 7.6")


def build_pack(H, charges, target):
    os.makedirs(target, exist_ok=True)
    info = {}
    info["status_rows"] = write_status(H, target)
    info["session_rows"], info["resent"], info["resent_hubs"] = write_sessions(H, charges, target)
    mprn = write_register(H, target)
    info["dso_rows"] = write_dso(H, target, mprn)
    info["wo_a"], info["wo_b"] = write_work_orders(H, target)
    write_ppm(H, target)
    info["survey_rows"] = write_survey(H, target)
    write_schedules(target)
    write_programme(H, target)
    write_tariff(target)
    stamp = EXPORT.timestamp()
    for f in FILES:
        os.utime(os.path.join(target, f), (stamp, stamp))
    return info
