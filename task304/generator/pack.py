"""task304 architecture 4: write the evidence pack (target/) from the clean truth, in the formats the organisation's
systems export. Layer 1 mess is what those systems do to records; nothing is placed to be caught."""
import csv
import datetime as dt
import io
import json
import os
import zoneinfo
from collections import defaultdict

import numpy as np
import openpyxl
from openpyxl.styles import Font

import params as P
import docs
from asks_world import Audiometry, Vending
from world import World

FIXED = dt.datetime(2026, 11, 16, 9, 0, 0)
SITE_WCS = {"LAR": "BRL-BNE1", "ECR": "BRL-SYD2", "TRU": "BRL-MEL1", "WFD": "BRL-ADL1", "KEW": "BRL-PER1", "BFD": "BRL-NTL1"}
SITE_HR = {"LAR": "Larapinta", "ECR": "Eastern Creek", "TRU": "Truganina", "WFD": "Wingfield", "KEW": "Kewdale", "BFD": "Beresfield"}
SITE_VEND = {"LAR": "Brolga Larapinta DC", "ECR": "Brolga Eastern Creek DC", "TRU": "Brolga Truganina", "WFD": "Brolga Wingfield",
             "KEW": "Brolga Kewdale DC", "BFD": "Brolga Beresfield"}
SITE_AUDIO = {"LAR": "BNE - Larapinta", "ECR": "SYD - Eastern Creek", "TRU": "MEL - Truganina", "WFD": "ADL - Wingfield",
              "KEW": "PER - Kewdale", "BFD": "NTL - Beresfield"}


def station_code(code, k):
    v = {h["code"]: h["vendor"] for h in P.HUBS}[code]
    if v == "V1":
        return "IND-%02d" % k
    if v == "V2":
        return "S1-I%02d" % k
    return "INDUCT %d" % k


def utc(code, local):
    tz = zoneinfo.ZoneInfo({h["code"]: h["tz"] for h in P.HUBS}[code])
    return local.replace(tzinfo=tz).astimezone(dt.timezone.utc)


def isoz(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if path.endswith("_export_20261116.csv") else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def scrub_xlsx(wb, creator):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = FIXED
    wb.properties.modified = FIXED
    wb.properties.title = None


CORE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        '<dc:creator>{c}</dc:creator><cp:lastModifiedBy>{c}</cp:lastModifiedBy>'
        '<dcterms:created xsi:type="dcterms:W3CDTF">{cr}</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">{d}</dcterms:modified></cp:coreProperties>')
APP = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
       '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
       'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
       '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
       '<Company>{c}</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
       '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
EXPORT_STAMP = {"Site Security": "2026-11-13T06:41:00Z", "Workforce Planning": "2026-11-10T23:05:00Z",
                "Engineering": "2026-06-30T02:12:00Z", "SafeStock": "2026-09-30T07:30:00Z",
                "ClearTone Occupational Audiology": "2026-11-06T04:18:00Z"}
CREATED_STAMP = {"Engineering": "2024-03-11T22:47:00Z"}     # a register kept and re-saved, not a one-off export


def save_xlsx(wb, path, creator):
    scrub_xlsx(wb, creator)
    wb.save(path)
    # normalise the zip so two builds are byte-identical, with the exporting system's own stamp
    import zipfile
    stamp = EXPORT_STAMP.get(creator, "2026-11-16T09:00:00Z")
    buf = io.BytesIO()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        names = [i.filename for i in zin.infolist()]
        for item in sorted(zin.infolist(), key=lambda i: i.filename):
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                data = CORE.format(c=creator, d=stamp, cr=CREATED_STAMP.get(creator, stamp)).encode()
            elif item.filename == "docProps/app.xml":
                data = APP.format(c=creator).encode()
            zi = zipfile.ZipInfo(item.filename, date_time=(2026, 11, 16, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


class Pack:
    def __init__(self, out):
        self.out = out
        os.makedirs(out, exist_ok=True)
        self.W = World()
        self.V = Vending(self.W)
        self.A = Audiometry(self.W)
        self.rng = np.random.default_rng(P.SEED + 101)
        self._ids()

    # ------------------------------------------------------------------ identifiers
    def _ids(self):
        rng = self.rng
        W = self.W
        pool = rng.choice(np.arange(100000, 999999), size=len(W.people) * 3, replace=False)
        self.payroll, self.lhno, self.badge = {}, {}, {}
        self.badges = []        # rows of the badge register
        i = 0
        for p in W.people:
            if p["kind"] == "EMP":
                self.payroll[p["pid"]] = "%06d" % pool[i]
            else:
                self.lhno[p["pid"]] = ("TW%05d" % (pool[i] % 100000)) if p.get("agency") == "Tasman Workforce" else ("M%06d" % pool[i])
            i += 1
        bpool = rng.choice(np.arange(1000000, 9999999), size=len(W.people) * 2 + 50, replace=False)
        j = 0
        self.badge_of = defaultdict(list)    # pid -> [(badge, issued, cancelled)]
        for p in W.people:
            pid = p["pid"]
            if p["kind"] == "EMP":
                b = "0%07d" % bpool[j]
                j += 1
                issued = dt.date(2019, 1, 1) + dt.timedelta(days=int(rng.integers(0, 2400)))
                self.badge_of[pid].append([b, issued, None])
            else:
                b = "TB%05d" % (bpool[j] % 100000)
                j += 1
                issued = P.LOG_START - dt.timedelta(days=int(rng.integers(3, 160)))
                self.badge_of[pid].append([b, issued, None])
        # badges reissued after loss: most before the reference weeks, a few inside them (induct-line staff)
        emps = [p for p in W.people if p["kind"] == "EMP"]
        pick = rng.choice(len(emps), size=34, replace=False)
        for n, k in enumerate(pick):
            p = emps[int(k)]
            if n < 24:
                d = P.LOG_START + dt.timedelta(days=int(rng.integers(0, 11)))
            else:
                d = P.REF_START + dt.timedelta(days=int(rng.integers(2, 20)))
            old = self.badge_of[p["pid"]][0]
            old[2] = d
            nb = "0%07d" % bpool[j]
            j += 1
            self.badge_of[p["pid"]].append([nb, d, None])
        # contractors' badges (maintenance)
        self.contractors = []
        for c in range(9):
            b = "CB%04d" % int(rng.integers(1000, 9999))
            hub = [h["code"] for h in P.HUBS][c % 6]
            self.contractors.append(dict(badge=b, hub=hub, name=W._name(), company=str(rng.choice(["Intralogix Services", "Conveyline Maintenance"]))))

    def badge_at(self, pid, when_date):
        for b, iss, can in self.badge_of[pid]:
            if iss <= when_date and (can is None or when_date < can):
                return b
        return self.badge_of[pid][-1][0]

    # ------------------------------------------------------------------ files
    def write_all(self):
        self.sessions()
        self.badge_register()
        self.hr_list()
        self.ta()
        self.timesheets()
        self.stations()
        self.distractors()
        self.vending()
        self.audiometry()
        docs.write_docs(self.out, self)
        for name in os.listdir(self.out):
            os.utime(os.path.join(self.out, name), (FIXED.timestamp(), FIXED.timestamp()))

    def sessions(self):
        rng = self.rng
        rows = []
        for s in self.W.sessions:
            code = s["hub"]
            st = s["start"]
            b = self.badge_at(s["pid"], (st - dt.timedelta(hours=5)).date())
            rows.append((utc(code, st), SITE_WCS[code], "S1", station_code(code, s["station_no"]), b,
                         utc(code, s["end"]), "AUTO_TIMEOUT" if s["end_type"] == "AUTO" else "OPERATOR"))
        # maintenance contractors' test log-ons
        for c in self.contractors:
            code = c["hub"]
            n = int(rng.integers(8, 15))
            for _ in range(n):
                d = self.W.days[int(rng.integers(0, len(self.W.days)))]
                start = dt.datetime(d.year, d.month, d.day, int(rng.integers(6, 20)), int(rng.integers(0, 60)))
                end = start + dt.timedelta(minutes=float(rng.uniform(4, 18)))
                k = int(rng.integers(1, {h["code"]: h["stations"] for h in P.HUBS}[code] + 1))
                rows.append((utc(code, start), SITE_WCS[code], "S1", station_code(code, k), c["badge"], utc(code, end), "OPERATOR"))
        rows.sort(key=lambda r: (r[0], r[1], r[3]))
        self.session_rows = rows
        write_csv(os.path.join(self.out, "wcs_operator_sessions_export_20261116.csv"),
                  ["site_code", "sorter", "station", "badge_id", "logon_utc", "logoff_utc", "logoff_reason"],
                  [(r[1], r[2], r[3], r[4], isoz(r[0]), isoz(r[5]), r[6]) for r in rows])

    def badge_register(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Badges"
        ws.append(["Badge ID", "Holder type", "Holder ref", "Holder name", "Site", "Issued", "Cancelled", "Reason"])
        for c in ws[1]:
            c.font = Font(bold=True)
        rows = []
        for p in self.W.people:
            for b, iss, can in self.badge_of[p["pid"]]:
                if p["kind"] == "EMP":
                    typ, ref = "Employee", self.payroll[p["pid"]]
                else:
                    typ, ref = "Labour hire", self.lhno[p["pid"]]
                reason = "Lost - reissued" if can else None
                rows.append([b, typ, ref, p["name"], SITE_HR[p["hub"]], iss, can, reason])
        for c in self.contractors:
            rows.append([c["badge"], "Contractor", c["company"], c["name"], SITE_HR[c["hub"]], dt.date(2026, 3, 2), None, None])
        rows.sort(key=lambda r: (r[4], r[0]))
        for r in rows:
            ws.append(r)
        for row in ws.iter_rows(min_row=2):
            for c in row[5:7]:
                if c.value:
                    c.number_format = "dd/mm/yyyy"
        ws.column_dimensions["D"].width = 24
        save_xlsx(wb, os.path.join(self.out, "badge_register_20261113.xlsx"), "Site Security")

    def hr_list(self):
        rows = []
        for p in self.W.people:
            if p["kind"] != "EMP":
                continue
            given, sur = p["name"].split(" ", 1)
            team = {"AM": "AM", "PM": "PM", "NT": "NIGHT"}[p["team"]]
            start = dt.date(2016, 1, 1) + dt.timedelta(days=int(self.rng.integers(0, 3700)))
            rows.append([self.payroll[p["pid"]], sur, given, SITE_HR[p["hub"]], p["title"], team, start.strftime("%d/%m/%Y")])
        rows.sort(key=lambda r: (r[3], r[1], r[2]))
        write_csv(os.path.join(self.out, "hr_employee_list_20261113.csv"),
                  ["payroll_no", "surname", "given_name", "site", "position_title", "roster_team", "start_date"], rows)

    def ta(self):
        rows = []
        stat = {"WORKED": "WORKED", "LEAVE": "ANNUAL LEAVE", "SICK": "PERSONAL LEAVE"}
        for s in self.W.shifts:
            p = self.W.people[s["pid"]]
            if p["kind"] != "EMP":
                continue
            rows.append([self.payroll[s["pid"]], s["date"].isoformat(), s["shift"], SITE_HR[s["hub"]], stat[s["status"]],
                         "8.00" if s["status"] != "SICK" else "7.60"])
        rows.sort(key=lambda r: (r[1], r[3], r[2], r[0]))
        write_csv(os.path.join(self.out, "ta_shift_records_20260928_20261108.csv"),
                  ["emp_no", "work_date", "shift_code", "site", "status", "paid_hours"], rows)

    def timesheets(self):
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1.title = "Tasman Workforce"
        ws1.append(["Tasman Workforce Pty Ltd - client timesheet export", None, None, None, None, None, None, None])
        ws1.append(["Client: Brolga Parcel Network", None, None, None, None, None, None, None])
        ws1.append(["Worker No", "Worker", "Site", "Date", "Shift", "Start", "Finish", "Hours"])
        for c in ws1[3]:
            c.font = Font(bold=True)
        mer = defaultdict(lambda: defaultdict(dict))
        trows = []
        for s in self.W.shifts:
            p = self.W.people[s["pid"]]
            if p["kind"] != "LH" or s["status"] != "WORKED":
                continue
            st = P.SHIFTS[s["shift"]]
            if p.get("agency") == "Tasman Workforce":
                trows.append([self.lhno[p["pid"]], p["name"], SITE_HR[p["hub"]], s["date"], s["shift"],
                              "%02d:00" % st, "%02d:00" % ((st + 8) % 24), 8])
            else:
                we = s["date"] + dt.timedelta(days=6 - s["date"].weekday())
                mer[(self.lhno[p["pid"]], p["name"], SITE_HR[p["hub"]])][we][s["date"].weekday()] = s["shift"]
        trows.sort(key=lambda r: (r[2], r[3], r[0]))
        for r in trows:
            ws1.append(r)
        for row in ws1.iter_rows(min_row=4):
            row[3].number_format = "dd/mm/yyyy"
        ws2 = wb.create_sheet("Meridian Labour Hire")
        ws2.append(["Meridian Labour Hire - weekly timesheet summary (shift worked, 8 h each)"])
        ws2.append(["Worker ID", "Name", "Site", "Week ending", "Mon", "Tue", "Wed", "Thu", "Fri", "Shifts"])
        for c in ws2[2]:
            c.font = Font(bold=True)
        mrows = []
        for (wid, name, site), weeks in mer.items():
            for we, dd in weeks.items():
                cells = [dd.get(k) for k in range(5)]
                mrows.append([wid, name, site, we] + cells + [sum(1 for x in cells if x)])
        mrows.sort(key=lambda r: (r[2], r[3], r[0]))
        for r in mrows:
            ws2.append(r)
        for row in ws2.iter_rows(min_row=3):
            row[3].number_format = "dd/mm/yyyy"
        save_xlsx(wb, os.path.join(self.out, "labour_hire_timesheets_oct_nov_2026.xlsx"), "Workforce Planning")

    def stations(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Induct stations"
        ws.append(["Site", "WCS site code", "Sorter", "Station", "Line", "Commissioned"])
        for c in ws[1]:
            c.font = Font(bold=True)
        rng = self.rng
        for h in P.HUBS:
            comm = dt.date(int(rng.integers(2014, 2022)), int(rng.integers(1, 13)), 1)
            for k in range(1, h["stations"] + 1):
                ws.append([SITE_HR[h["code"]], SITE_WCS[h["code"]], "S1", station_code(h["code"], k),
                           "Induct", comm if k <= h["stations"] - 2 else comm + dt.timedelta(days=int(rng.integers(300, 1500)))])
        for row in ws.iter_rows(min_row=2):
            row[5].number_format = "mmm yyyy"
        save_xlsx(wb, os.path.join(self.out, "induct_station_register.xlsx"), "Engineering")

    def distractors(self):
        rng = self.rng
        rows = []
        cats = ["Reversing alarms", "Truck movements at night", "Roller door noise", "PA announcements", "Idling trucks"]
        k = 5000 + int(rng.integers(0, 400))
        for h in P.HUBS:
            for _ in range(int(rng.integers(4, 15))):
                d = dt.date(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 300)))
                k += int(rng.integers(3, 60))
                rows.append(["NC-%05d" % k, d.isoformat(), SITE_HR[h["code"]], str(rng.choice(cats)),
                             str(rng.choice(["Closed - no further action", "Closed - mitigation agreed", "Open"]))])
        rows.sort(key=lambda r: r[1])
        write_csv(os.path.join(self.out, "boundary_noise_complaints_2026.csv"),
                  ["complaint_ref", "received", "site", "category", "status"], rows)
        rows = []
        heads = defaultdict(int)
        for p in self.W.people:
            heads[p["hub"]] += 1
        d = dt.date(2026, 7, 1)
        while d <= dt.date(2026, 11, 13):
            if d.weekday() < 5:
                for h in P.HUBS:
                    base = h["stations"] * 1150 * 21.5
                    v = int(base * float(rng.uniform(0.86, 1.12)))
                    rows.append([SITE_HR[h["code"]], d.isoformat(), v, int(v / 21.5 * float(rng.uniform(1.25, 1.45)))])
            d += dt.timedelta(days=1)
        write_csv(os.path.join(self.out, "sort_volumes_daily_2026.csv"), ["site", "date", "parcels_sorted", "peak_hour_rate"], rows)

    def vending(self):
        V = self.V
        recs = []
        slots = {"EP-01": ["A1", "A2", "B1"], "EM-01": ["C3"]}
        rng = np.random.default_rng(P.SEED + 131)
        for v in sorted(V.vends, key=lambda v: (v["local"], v["machine"])):
            recs.append({"machine_id": v["machine"], "vend_utc": isoz(utc(v["hub"], v["local"])),
                         "product_code": v["product"], "slot": str(rng.choice(slots[v["product"]])), "qty": 1})
        recs.sort(key=lambda r: (r["vend_utc"], r["machine_id"]))
        doc = {"export": "SafeStock Cloud - vend transactions", "account": "Brolga Parcel Network",
               "period": {"from": "2026-06-29", "to": "2026-10-02"}, "export_created_utc": "2026-10-06T03:14:09Z",
               "records": recs}
        with open(os.path.join(self.out, "ppe_vending_transactions_2026q3.json"), "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=1, sort_keys=False)
        rows = []
        for v in V.visits:
            rows.append([v["date"].strftime("%d/%m/%Y"), v["machine"], SITE_VEND[v["hub"]], v["action"], v["product"], v["qty"], v["uom"]])
        write_csv(os.path.join(self.out, "ppe_vending_service_visits_2026q3.csv"),
                  ["visit_date", "machine_id", "site", "visit_type", "product_code", "qty_loaded", "uom"], rows)
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Machines"
        ws.append(["Machine ID", "Model", "Site", "Location in site", "Installed"])
        for c in ws[1]:
            c.font = Font(bold=True)
        for m in sorted(V.machines, key=lambda m: m["machine"]):
            cur = V.current[m["machine"]]
            loc = m["location"] if cur == m["hub0"] else ("North" if m["location"] == "South" else "South")
            ws.append([m["machine"], m["model"], SITE_VEND[cur], loc + " amenities", dt.date(2023, 2, 14)])
        ws2 = wb.create_sheet("Products")
        ws2.append(["Product code", "Description", "Unit"])
        for c in ws2[1]:
            c.font = Font(bold=True)
        ws2.append(["EP-01", "Disposable foam earplugs, Class 4, pack of 5 pairs", "Pack"])
        ws2.append(["EM-01", "Earmuff, Class 5, headband", "Each"])
        save_xlsx(wb, os.path.join(self.out, "ppe_vending_asset_list_20260930.xlsx"), "SafeStock")

    def audiometry(self):
        A = self.A
        rng = np.random.default_rng(P.SEED + 151)
        client = {}
        cpool = rng.choice(np.arange(20000, 99999), size=len(A.enrolled) + 5, replace=False)
        for i, p in enumerate(A.enrolled):
            client[p["pid"]] = "CW%05d" % cpool[i]
        rows = []
        auds = ["J. Okafor", "R. Liang", "S. Patel", "M. Brennan"]
        for t in sorted(A.tests, key=lambda t: (t["date"], t["test_id"])):
            if t["date"].year < 2025 and t["type"] != "BASELINE":
                continue
            hub = A.hub_at(t["pid"], t["date"])
            rows.append([t["test_id"], client[t["pid"]], t["date"].isoformat(), t["type"], SITE_AUDIO[hub]]
                        + ["%d" % x for x in t["L"]] + ["%d" % x for x in t["R"]] + [str(rng.choice(auds))])
        write_csv(os.path.join(self.out, "audiometry_results_2025_2026.csv"),
                  ["test_id", "client_no", "test_date", "test_type", "test_site", "L_2k", "L_3k", "L_4k", "R_2k", "R_3k", "R_4k", "audiometrist"],
                  rows)
        conf, cur = A.truth()
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Clients"
        ws.append(["Client No", "Employee No", "Surname", "Given name", "Date of birth", "Reference test", "Reference date"])
        for c in ws[1]:
            c.font = Font(bold=True)
        crow = []
        for p in A.enrolled:
            given, sur = p["name"].split(" ", 1)
            dob = dt.date(int(rng.integers(1962, 2004)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            r = cur[p["pid"]]
            crow.append([client[p["pid"]], self.payroll[p["pid"]], sur, given, dob, r["test_id"], r["date"]])
        crow.sort(key=lambda r: r[0])
        for r in crow:
            ws.append(r)
        for row in ws.iter_rows(min_row=2):
            row[4].number_format = "dd/mm/yyyy"
            row[6].number_format = "dd/mm/yyyy"
        save_xlsx(wb, os.path.join(self.out, "audiometry_clients_%s.xlsx" % P.AUDIO_EXPORT.strftime("%Y%m%d")), "ClearTone Occupational Audiology")
        rows = []
        for t in sorted(A.transfers, key=lambda t: t["effective"]):
            rows.append([self.payroll[t["pid"]], SITE_HR[t["from_hub"]], SITE_HR[t["to_hub"]], t["effective"].strftime("%d/%m/%Y")])
        write_csv(os.path.join(self.out, "hr_site_transfers_2026.csv"), ["payroll_no", "from_site", "to_site", "effective_date"], rows)


def build(out):
    pk = Pack(out)
    pk.write_all()
    return pk


if __name__ == "__main__":
    import sys
    build(sys.argv[1] if len(sys.argv) > 1 else "../target")
