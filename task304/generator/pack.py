"""task304 architecture 5: write the evidence pack (target/) from the clean truth, in the formats the county's and the
police force's systems export. Layer 1 mess is what those systems do to records; nothing is placed to be caught."""
import csv
import datetime as dt
import io
import json
import os
import zipfile

import numpy as np
import openpyxl
from openpyxl.styles import Font

import docs
import params as P
from world import TRUNK, World, road_user

OLD_CASUALTY_TYPE = {"Car": "Car occupant", "Taxi or private hire car": "Car occupant", "Pedal cycle": "Pedal cyclist",
                     "Motorcycle 125cc and under": "Motorcyclist", "Motorcycle 125cc to 500cc": "Motorcyclist",
                     "Motorcycle over 500cc": "Motorcyclist", "Van or light goods": "Van occupant",
                     "Goods 7.5 tonnes and over": "Goods vehicle occupant", "Bus or coach": "Bus or coach occupant",
                     "E-scooter": "E-scooter rider", "Agricultural vehicle": "Other vehicle occupant",
                     "Other": "Other vehicle occupant"}
OLD_VEHICLE_CODE = {"Pedal cycle": 1, "Motorcycle 125cc and under": 3, "Motorcycle 125cc to 500cc": 4,
                    "Motorcycle over 500cc": 5, "Taxi or private hire car": 8, "Car": 9, "Bus or coach": 11,
                    "Agricultural vehicle": 17, "Van or light goods": 19, "Goods 7.5 tonnes and over": 21,
                    "E-scooter": 106, "Other": 90}
SEV_TEXT = {1: "Fatal", 2: "Serious", 3: "Slight"}

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
STAMPS = {"Ardleshire County Council Network Management": ("2014-09-22T08:05:00Z", "2026-10-14T13:22:00Z"),
          "Ardleshire Police Fatal Collision Investigation Unit": ("2026-02-09T10:41:00Z", "2026-11-23T15:08:00Z")}


def write_csv(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def save_xlsx(wb, path, creator):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.title = None
    wb.save(path)
    created, modified = STAMPS[creator]
    buf = io.BytesIO()
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in sorted(zin.infolist(), key=lambda i: i.filename):
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                data = CORE.format(c=creator, d=modified, cr=created).encode()
            elif item.filename == "docProps/app.xml":
                data = APP.format(c=creator).encode()
            zi = zipfile.ZipInfo(item.filename, date_time=(2026, 11, 27, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zout.writestr(zi, data)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def dmy(d):
    return d.strftime("%d/%m/%Y")


def bst(d):
    """UK summer time: last Sunday of March to last Sunday of October."""
    def last_sunday(y, m):
        x = dt.date(y, m, 31)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    return last_sunday(d.year, 3) <= d < last_sunday(d.year, 10)


class Pack:
    def __init__(self, out):
        self.out = out
        os.makedirs(out, exist_ok=True)
        self.W = World()
        self.rng = np.random.default_rng(P.SEED + 77)

    def p(self, name):
        return os.path.join(self.out, name)

    # ------------------------------------------------------------------ the validated record and the inventory
    def collision_record(self):
        rows = []
        for c in self.W.collisions:
            node = c["node"]
            if node and c["date"].year < 2019:
                node = c["former"]
            dow = (c["date"].isoweekday() % 7) + 1          # 1 Sunday to 7 Saturday
            rows.append([c["ref"], dmy(c["date"]), "%02d:%02d" % (c["hour"], c["minute"]), dow, c["district"],
                         c["easting"], c["northing"], c["road1"], c["road2"], c["jd"], c["jc"], node, c["severity"],
                         c["vehicles"], c["casualties"], c["speed"], c["light"], c["weather"], c["surface"]])
        write_csv(self.p("collision_records_2016_2025.csv"),
                  ["accident_ref", "collision_date", "collision_time", "day_of_week", "district", "easting", "northing",
                   "first_road", "second_road", "junction_detail", "junction_control", "junction_node", "severity",
                   "number_of_vehicles", "number_of_casualties", "speed_limit", "light_conditions",
                   "weather_conditions", "road_surface"], rows, crlf=True)

    def inventory(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Junctions"
        head = ["node", "former_node", "junction_name", "district", "layout", "control", "major_road", "minor_road",
                "easting", "northing"]
        head += ["aadt_major_%d" % y for y in P.YEARS] + ["aadt_minor_%d" % y for y in P.YEARS]
        ws.append(head)
        for c in ws[1]:
            c.font = Font(bold=True)
        js = sorted(self.W.junctions, key=lambda j: j["node"])
        for j in js:
            major = "%s %s" % (j["road"], j["road_name"]) if not j["road"].startswith("C") else j["road_name"]
            row = [j["node"], j["former"], j["name"], j["district"], j["layout"], j["control"], major, j["minor"],
                   j["easting"], j["northing"]]
            row += [int(round(v / 10.0) * 10) for v in j["maj"]] + [int(round(v / 10.0) * 10) for v in j["mnr"]]
            ws.append(row)
        ws.freeze_panes = "D2"
        ws2 = wb.create_sheet("Codes")
        ws2.append(["field", "code", "meaning"])
        for c in ws2[1]:
            c.font = Font(bold=True)
        for code, meaning in (("T", "T junction"), ("ST", "Staggered junction"), ("X", "Crossroads"),
                              ("MR", "Mini-roundabout"), ("RB", "Roundabout"), ("SIG", "Signal-controlled junction")):
            ws2.append(["layout", code, meaning])
        for code, meaning in (("GW", "Give way"), ("STOP", "Stop line"), ("SIG", "Traffic signals"), ("RBT", "Roundabout")):
            ws2.append(["control", code, meaning])
        save_xlsx(wb, self.p("junction_inventory_2026.xlsx"), "Ardleshire County Council Network Management")

    def road_register(self):
        rows = [["A4600", "Ardle Bypass", 452000, 470000, "A", "Strategic road network", "01/04/2009"],
                ["A4600", "Kestermoor Road East", 470000, 486000, "A", "Ardleshire County Council", "01/04/2019"],
                ["A6510", "Wold Road", 441000, 470000, "A", "Strategic road network", "01/04/2009"]]
        seen = set()
        for road, name in sorted(set((j["road"], j["road_name"]) for j in self.W.junctions)):
            if road in TRUNK or road in seen or road.startswith("C"):
                continue
            seen.add(road)
            rows.append([road, name, 441000, 486000, road[0], "Ardleshire County Council", "01/04/1996"])
        rows.sort(key=lambda r: (r[0], r[2]))
        write_csv(self.p("road_network_register_2026.csv"),
                  ["road_number", "section_name", "easting_from", "easting_to", "road_class", "highway_authority",
                   "authority_from"], rows)

    # ------------------------------------------------------------------ the 2026 provisional police data
    def provisional(self):
        rng = self.rng
        old_c, old_k, old_v, new = [], [], [], []
        seq_old, seq_new = 4100, 10200
        for c in self.W.prov:
            t = dt.datetime(c["date"].year, c["date"].month, c["date"].day, c["hour"], c["minute"])
            if c["date"] < P.MIGRATION:
                seq_old += int(rng.integers(1, 4))
                ref = "2026/47/%07d" % seq_old
                c["old_ref"] = ref
                rec_sev = min(k["recorded"] for k in c["casualties"])
                received = c["date"] + dt.timedelta(days=int(rng.choice([1, 2, 3, 5, 8, 13, 21])))
                old_c.append([ref, dmy(c["date"]), "%02d:%02d" % (c["hour"], c["minute"]),
                              int(round(c["easting"] / 10.0) * 10), int(round(c["northing"] / 10.0) * 10),
                              c["road"], rec_sev, len(c["vehicles"]), len(c["casualties"]), dmy(received)])
                for v in c["vehicles"]:
                    old_v.append([ref, v["ref"], OLD_VEHICLE_CODE[v["type"]]])
                vt = {v["ref"]: v["type"] for v in c["vehicles"]}
                for i, k in enumerate(c["casualties"], start=1):
                    cls = {"Driver or rider": 1, "Passenger": 2, "Pedestrian": 3}[k["cls"]]
                    ctype = "Pedestrian" if k["cls"] == "Pedestrian" else OLD_CASUALTY_TYPE[vt[k["vehicle"]]]
                    old_k.append([ref, i, k["vehicle"], cls, k["recorded"], 1 if k["sex"] == "Male" else 2, k["age"], ctype])
            if c["date"] >= P.MIGRATION or c.get("resent"):
                rs = c.get("resent")
                tt = t + dt.timedelta(minutes=(rs["dmin"] if rs else 0))
                off = "+01:00" if bst(tt.date()) else "+00:00"
                e = c["easting"] + (rs["de"] if rs else 0)
                n_ = c["northing"] + (rs["dn"] if rs else 0)
                if rs:
                    upd = P.MIGRATION + dt.timedelta(days=int(rng.integers(3, 120)))
                    status = "Amended"
                else:
                    amended = rng.random() < 0.09
                    upd = c["date"] + dt.timedelta(days=int(rng.integers(1, 30 if not amended else 60)))
                    status = "Amended" if amended else "Submitted"
                upd = min(upd, dt.date(2026, 11, 19))
                cas = []
                for i, k in enumerate(c["casualties"], start=1):
                    ksev = k["recorded"]
                    if rs and rs["sev_change"] and k["recorded"] == 3 and k["sev"] == 2:
                        ksev = 2
                    cas.append({"casualty": i, "vehicle": k["vehicle"], "class": k["cls"], "severity": SEV_TEXT[ksev],
                                "sex": "M" if k["sex"] == "Male" else "F", "age": k["age"]})
                created = (upd if rs else c["date"] + dt.timedelta(days=int(rng.integers(0, 4))))
                new.append({"_created": (created, tt), "collision_id": None, "occurred": tt.strftime("%Y-%m-%dT%H:%M:00") + off,
                            "easting": int(e), "northing": int(n_), "road": c["road"],
                            "severity": SEV_TEXT[min(SEV_TEXT_INV[x["severity"]] for x in cas)],
                            "record_status": status, "last_updated": upd.isoformat(),
                            "vehicles": [{"vehicle": v["ref"], "type": v["type"]} for v in c["vehicles"]],
                            "casualties": cas})
        write_csv(self.p("police_collisions_2026_jan_may.csv"),
                  ["accident_ref", "collision_date", "collision_time", "easting", "northing", "first_road", "severity",
                   "number_of_vehicles", "number_of_casualties", "date_received"], old_c)
        write_csv(self.p("police_casualties_2026_jan_may.csv"),
                  ["accident_ref", "casualty_ref", "vehicle_ref", "casualty_class", "casualty_severity", "sex", "age",
                   "casualty_type"], old_k)
        write_csv(self.p("police_vehicles_2026_jan_may.csv"), ["accident_ref", "vehicle_ref", "vehicle_type"], old_v)
        # the new system numbers records as they are created in it: a migrated collision when it was amended
        new.sort(key=lambda r: r["_created"])
        for r in new:
            seq_new += int(rng.integers(1, 4))
            r["collision_id"] = "47-2026-%06d" % seq_new
            del r["_created"]
        new = [dict([("collision_id", r["collision_id"])] + [(k, v) for k, v in r.items() if k != "collision_id"]) for r in new]
        doc = {"source": "Ardleshire Police collision recording system", "extract": "Injury road traffic collisions, Ardleshire policing area",
               "pulled": "2026-11-20T08:14:00Z", "collisions": new}
        with open(self.p("police_export_2026_jun_sep.json"), "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")

    def fatal_notifications(self):
        rng = np.random.default_rng(P.SEED + 91)
        rows = []
        for c in self.W.prov:
            for k in c["casualties"]:
                if "died_day" not in k:
                    continue
                death = c["date"] + dt.timedelta(days=k["died_day"])
                if death > dt.date(2026, 11, 15):
                    continue
                tm = (c["hour"] * 60 + c["minute"] + int(rng.integers(-6, 7))) % 1440
                near = "near %s" % ("the junction with a minor road" if rng.random() < 0.4 else "%d m from the %s" % (
                    int(rng.integers(2, 30)) * 50, "village" if rng.random() < 0.5 else "previous junction"))
                rows.append([dmy(c["date"]), "%02d:%02d" % (tm // 60, (tm % 60) // 5 * 5), c["road"],
                             "%s, %s" % (c["road"], near), c["district"], k["sex"], k["age"], dmy(death),
                             dmy(death + dt.timedelta(days=int(rng.integers(1, 6))))])
        rows.sort(key=lambda r: dt.datetime.strptime(r[0], "%d/%m/%Y"))
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Notifications 2026"
        ws.append(["notification", "collision_date", "approx_time", "road", "location", "district", "casualty_sex",
                   "casualty_age", "date_of_death", "notified"])
        for c in ws[1]:
            c.font = Font(bold=True)
        for i, r in enumerate(rows, start=1):
            ws.append(["FCIU-26-%03d" % (i * 3 + 4)] + r)
        save_xlsx(wb, self.p("fatal_casualty_notifications_2026.xlsx"), "Ardleshire Police Fatal Collision Investigation Unit")

    # ------------------------------------------------------------------ distractors
    def distractors(self):
        rng = np.random.default_rng(P.SEED + 133)
        rows = []
        roads = sorted(set(j["road"] for j in self.W.junctions if not j["road"].startswith("C")))
        for road in roads:
            ch = 0
            for _ in range(int(rng.integers(30, 70))):
                ln = int(rng.integers(5, 21)) * 10
                sc = float(np.clip(rng.normal(0.47, 0.07), 0.25, 0.70))
                il = float(rng.choice([0.35, 0.40, 0.45, 0.50, 0.55], p=[0.15, 0.30, 0.30, 0.15, 0.10]))
                d = dt.date(2025, 5, 12) + dt.timedelta(days=int(rng.integers(0, 120)))
                rows.append([road, ch, ch + ln, rng.choice(["L1", "R1"]), dmy(d), "%.2f" % sc, "%.2f" % il])
                ch += ln
        write_csv(self.p("skid_resistance_survey_2025.csv"),
                  ["road", "chainage_from_m", "chainage_to_m", "lane", "survey_date", "sc_value", "investigatory_level"], rows)
        places = ["Saxby", "Holt", "Brindham", "Kestermoor", "Thorpe", "Carlby", "Stow", "Hollin", "Mill End", "Ings"]
        rows = []
        for _ in range(240):
            d = dt.date(2026, 1, 5) + dt.timedelta(days=int(rng.integers(0, 300)))
            place = places[int(rng.integers(0, len(places)))]
            lim = int(rng.choice([20, 30, 30, 40]))
            checked = int(rng.integers(60, 420))
            over = int(checked * float(np.clip(rng.normal(0.14, 0.07), 0.01, 0.45)))
            start = int(rng.choice([7, 8, 15, 16, 17]))
            rows.append([dmy(d), place, lim, "%02d:00" % start, "%02d:00" % (start + 1), checked, over])
        rows.sort(key=lambda r: (dt.datetime.strptime(r[0], "%d/%m/%Y"), r[1]))
        write_csv(self.p("community_speedwatch_2026.csv"),
                  ["session_date", "location", "speed_limit_mph", "start", "end", "vehicles_checked", "over_limit"], rows)

    def build(self):
        self.collision_record()
        self.inventory()
        self.road_register()
        self.provisional()
        self.fatal_notifications()
        self.distractors()
        docs.write_docs(self.out, self)
        return self


SEV_TEXT_INV = {"Fatal": 1, "Serious": 2, "Slight": 3}


def build(out):
    return Pack(out).build()
