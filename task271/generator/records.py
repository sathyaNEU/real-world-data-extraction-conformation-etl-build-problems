"""The exports as the systems that hold them write them: the mutual's policy administration and claim systems,
the county assessor's roll and appeals, the State Tax Equalization Board's ratios as the county reprints them, and
the water authority's GIS layers and flow-test log. The mess is the systems' own (a claim code set replaced on
1 January 2024, reopened claims under suffixed numbers, voided checks, a hydrant renumbering in April 2024, base-year
assessed values); nothing is placed to be caught."""
import csv
import datetime as dt
import json
import math

import numpy as np

import common as K

RENUMBER = dt.date(2024, 4, 1)          # the authority's hydrant renumbering
OLD_CODES = {"PLUMB": "WTR-P", "APPL": "WTR-A", "FREEZE": "WTR-F", "BACKUP": "WTR-O", "SEEPAGE": "WTR-O",
             "THEFT": "THF", "LIAB": "LIA", "OTHER": "OTH", "FIRE": "FIR", "WIND": "WND", "HAIL": "HAL"}
NEW_CODES = {"PLUMB": ("3110", "3130"), "APPL": ("3120",), "FREEZE": ("3210",), "BACKUP": ("3310",),
             "SEEPAGE": ("3320",), "THEFT": ("6100",), "LIAB": ("7100",), "OTHER": ("8100",), "FIRE": ("5110", "5120"),
             "WIND": ("4110",), "HAIL": ("4210",)}
CODE_TABLE = [
    ("LEGACY", "WTR-P", "Water discharge from plumbing or heating system", "3110; 3130"),
    ("LEGACY", "WTR-A", "Water discharge from household appliance", "3120"),
    ("LEGACY", "WTR-F", "Freezing of plumbing, heating or appliance", "3210"),
    ("LEGACY", "WTR-O", "Water, other (backup, seepage, surface)", "3310; 3320; 3410"),
    ("LEGACY", "FIR", "Fire, smoke and lightning", "5110; 5120"),
    ("LEGACY", "WND", "Windstorm", "4110"),
    ("LEGACY", "HAL", "Hail", "4210"),
    ("LEGACY", "THF", "Theft and vandalism", "6100"),
    ("LEGACY", "LIA", "Liability", "7100"),
    ("LEGACY", "OTH", "All other", "8100"),
    ("2024", "3110", "Sudden discharge, plumbing system", ""),
    ("2024", "3120", "Sudden discharge, household appliance", ""),
    ("2024", "3130", "Sudden discharge, heating or air-conditioning system", ""),
    ("2024", "3210", "Freezing", ""),
    ("2024", "3310", "Backup of sewer or drain (endorsement)", ""),
    ("2024", "3320", "Seepage or leakage over time", ""),
    ("2024", "3410", "Surface or ground water", ""),
    ("2024", "4110", "Windstorm", ""),
    ("2024", "4210", "Hail", ""),
    ("2024", "5110", "Fire and smoke", ""),
    ("2024", "5120", "Lightning", ""),
    ("2024", "6100", "Theft and vandalism", ""),
    ("2024", "7100", "Liability", ""),
    ("2024", "8100", "All other", ""),
]
CAT_CODES = {dt.date(2023, 6, 27): "PCS 23-41", dt.date(2024, 5, 9): "PCS 24-17", dt.date(2025, 7, 30): "PCS 25-38"}
WALL = {"FRAME": "F", "BRICK VENEER": "MV", "MASONRY": "M", "STONE": "M"}
FOUND = {"BSMT FULL": "B", "BSMT PART": "B", "SLAB": "S", "CRAWL": "C", "PIERS": "C"}


def iso(d):
    return d.isoformat() if d else ""


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


class Exports:
    def __init__(self, w):
        self.w = w
        self.rng = np.random.default_rng(w.seed + 271)
        self.claim_no = {}
        self.reopens = {}
        self.payments = []
        self.tpa = []           # (claim, transactions) handled by the adjusting firm

    # ---- the mutual's policy administration system
    def terms(self, path):
        rng = self.rng
        rows = []
        for t in self.w.terms:
            h = t["home"]
            reason = ""
            canc = t["cancel"]
            rein = None
            if canc is not None:
                reason = rng.choice(["SOLD", "INSURED REQUEST", "NONPAY"], p=[0.62, 0.30, 0.08])
            elif rng.random() < 0.016:
                # a cancellation for non-payment, reinstated without a lapse when the premium arrived
                span = (t["end"] - t["start"]).days
                canc = t["start"] + dt.timedelta(int(rng.integers(40, max(41, span - 30))))
                rein = canc + dt.timedelta(int(rng.integers(6, 26)))
                if rein >= t["end"]:
                    canc, rein = None, None
                else:
                    reason = "NONPAY"
            form = "HO-5" if t["coverage_a"] > 520000 and rng.random() < 0.6 else "HO-3"
            prem = round(t["coverage_a"] / 1000.0 * (2.95 if form == "HO-3" else 3.35) *
                         {500: 1.08, 1000: 1.0, 2500: 0.86}[t["deductible"]] * rng.normal(1.0, 0.03), 0)
            rows.append([t["policy_no"], t["term"], iso(t["start"]), iso(t["end"]), iso(canc), reason, iso(rein),
                         h["parcel_id"], h["town"], form, h["year_built"], WALL[h["wall"]], FOUND[h["foundation"]],
                         h["full"], h["half"], ("%.1f" % h["stories"]).replace(".0", ""), t["coverage_a"],
                         t["deductible"], "%.0f" % prem])
        rows.sort(key=lambda r: (r[0], r[1]))
        return write_csv(path, ["policy_number", "term_number", "term_effective", "term_expiration",
                                "cancellation_effective", "cancellation_reason", "reinstatement_effective", "parcel_id",
                                "municipality_code", "policy_form", "year_built", "construction", "foundation",
                                "full_baths", "half_baths", "stories", "coverage_a", "deductible", "annual_premium"], rows)

    # ---- the claim system and its payments
    def claims(self, path):
        rng = self.rng
        rows = []
        seq = {}
        for c in sorted(self.w.claims, key=lambda c: (c["reported"], c["policy_no"])):
            yr = c["reported"].year
            seq[yr] = seq.get(yr, 0) + int(rng.integers(1, 4))
            no = "C%02d-%05d" % (yr % 100, seq[yr])
            c["claim_no"] = no
            legacy = c["reported"] < K.CODE_CHANGE
            if legacy:
                code = OLD_CODES[c["kind"]]
            else:
                opts = NEW_CODES[c["kind"]]
                if c["kind"] == "PLUMB":
                    code = "3130" if rng.random() < 0.16 else "3110"
                elif c["kind"] == "FIRE":
                    code = "5120" if rng.random() < 0.12 else "5110"
                else:
                    code = opts[0]
            cat = CAT_CODES.get(c["loss"], "") if c["kind"] == "HAIL" else ""
            paid = max(0.0, c["amount"] - c["deductible"])
            denied = c["kind"] == "SEEPAGE" and rng.random() < 0.7
            if denied:
                paid = 0.0
            closes = c["reported"] + dt.timedelta(int(rng.integers(12, 160)))
            status = "CLOSED" if paid > 0 else "CLOSED WITHOUT PAYMENT"
            if closes > K.EXTRACT:
                status, closes = "OPEN", None
            c["paid"] = paid if status != "OPEN" or rng.random() < 0.5 else 0.0
            c["status"] = status
            c["tpa"] = (dt.date(2023, 3, 1) <= c["reported"] <= dt.date(2023, 8, 31) and c["kind"] != "LIAB") or \
                (c["kind"] in ("PLUMB", "APPL") and c["amount"] > 25000)
            rows.append([no, c["policy_no"], c["term"], c["parcel_id"], iso(c["loss"]), iso(c["reported"]), code, cat,
                         status, iso(closes), ""])
            self._pay(c, no, closes)
            # a closed claim reopened for a supplement: a new line under the suffixed number
            if status == "CLOSED" and not c.get("tpa") and rng.random() < 0.012:
                ro = closes + dt.timedelta(int(rng.integers(20, 200)))
                if ro < K.EXTRACT:
                    rno = no + "-R1"
                    rcode = code if ro < K.CODE_CHANGE or not legacy else NEW_CODES[c["kind"]][0]
                    rclose = ro + dt.timedelta(int(rng.integers(10, 70)))
                    rstatus = "CLOSED" if rclose <= K.EXTRACT else "OPEN"
                    rows.append([rno, c["policy_no"], c["term"], c["parcel_id"], iso(c["loss"]), iso(ro), rcode, cat,
                                 rstatus, iso(rclose) if rstatus == "CLOSED" else "", no])
                    extra = round(float(c["amount"] * rng.uniform(0.08, 0.35)), 2)
                    self._add_pay(rno, ro + dt.timedelta(int(rng.integers(5, 40))), "INDEMNITY", extra)
                    c["paid"] += extra
        rows.sort(key=lambda r: (r[5], r[0]))
        return write_csv(path, ["claim_number", "policy_number", "term_number", "parcel_id", "date_of_loss",
                                "date_reported", "cause_code", "catastrophe_code", "claim_status", "date_closed",
                                "reopened_from"], rows)

    def _add_pay(self, no, d, kind, amt, check=None):
        self.payments.append([no, d, kind, amt, check])

    def _pay(self, c, no, closes):
        rng = self.rng
        if c.get("tpa"):
            return self._tpa_pay(c, no, closes)
        if c["paid"] <= 0:
            if rng.random() < 0.6:
                self._add_pay(no, c["reported"] + dt.timedelta(int(rng.integers(3, 30))), "EXPENSE",
                              round(float(rng.uniform(120, 480)), 2))
            return
        n = int(rng.choice([1, 2, 3], p=[0.62, 0.30, 0.08]))
        last = closes or (K.EXTRACT - dt.timedelta(5))
        span = max(1, (last - c["reported"]).days)
        shares = rng.dirichlet(np.ones(n)) if n > 1 else [1.0]
        left = round(c["paid"], 2)
        for i, s in enumerate(shares):
            amt = round(c["paid"] * s, 2) if i < n - 1 else round(left, 2)
            left -= amt
            d = c["reported"] + dt.timedelta(int(span * (i + 1) / (n + 0.4)))
            self._add_pay(no, d, "INDEMNITY", amt)
            if rng.random() < 0.015:          # a check voided and reissued
                self._add_pay(no, d + dt.timedelta(int(rng.integers(5, 25))), "VOID", -amt)
                self._add_pay(no, d + dt.timedelta(int(rng.integers(26, 50))), "INDEMNITY", amt)
        if rng.random() < 0.55:
            self._add_pay(no, c["reported"] + dt.timedelta(int(rng.integers(3, 40))), "EXPENSE",
                          round(float(rng.uniform(140, 900)), 2))
        if c["kind"] in ("PLUMB", "APPL") and rng.random() < 0.06:   # subrogation against a plumber or maker
            rec = round(float(c["paid"] * rng.uniform(0.25, 0.9)), 2)
            self._add_pay(no, last + dt.timedelta(int(rng.integers(30, 260))), "RECOVERY", -rec)
            c["recovered"] = rec

    def _tpa_pay(self, c, no, closes):
        """the adjusting firm pays the claim from its own account and reports it on its monthly bordereau"""
        rng = self.rng
        tx = []
        if c["paid"] > 0:
            n = int(rng.choice([1, 2, 3], p=[0.5, 0.35, 0.15]))
            last = closes or (K.EXTRACT - dt.timedelta(5))
            span = max(1, (last - c["reported"]).days)
            shares = rng.dirichlet(np.ones(n)) if n > 1 else [1.0]
            left = round(c["paid"], 2)
            for i, sh in enumerate(shares):
                amt = round(c["paid"] * sh, 2) if i < n - 1 else round(left, 2)
                left -= amt
                tx.append((c["reported"] + dt.timedelta(int(span * (i + 1) / (n + 0.4))), "PAID", amt))
            if c["kind"] in ("PLUMB", "APPL") and rng.random() < 0.10:
                rec = round(float(c["paid"] * rng.uniform(0.25, 0.9)), 2)
                tx.append((last + dt.timedelta(int(rng.integers(30, 200))), "RECOVERED", rec))
                c["recovered"] = rec
        self.tpa.append((c, no, closes, tx))

    def bordereau(self, path):
        """the adjusting firm's monthly bordereau, one sheet a month: every claim it held that month, paid this month
        and to date (indemnity), recovered to date and the outstanding reserve"""
        import openpyxl
        from openpyxl.styles import Font
        rng = self.rng
        months = []
        m = dt.date(2023, 3, 1)
        while m <= dt.date(2026, 8, 1):
            months.append(m)
            m = dt.date(m.year + (m.month == 12), 1 if m.month == 12 else m.month + 1, 1)
        wb = openpyxl.Workbook()
        wb.remove(wb.active)
        refs = {}
        nrow = 0
        for mo in months:
            nxt = dt.date(mo.year + (mo.month == 12), 1 if mo.month == 12 else mo.month + 1, 1)
            ws = wb.create_sheet(mo.strftime("%Y-%m"))
            ws.append(["Corrigan Adjusting Services LLC: claims bordereau for Halverstead Mutual Fire Insurance "
                       "Company, %s" % mo.strftime("%B %Y")])
            ws["A1"].font = Font(bold=True)
            ws.append(["Insurer claim no.", "CAS reference", "Date of loss", "Peril", "Paid this month",
                       "Paid to date", "Recovered to date", "Outstanding reserve", "Status at month end"])
            for c, no, closes, tx in sorted(self.tpa, key=lambda t: t[1]):
                if c["reported"] >= nxt or (closes is not None and closes < mo):
                    continue
                if no not in refs:
                    refs[no] = "CAS-%d-%04d" % (c["reported"].year, 1000 + len(refs) * 3 % 9000)
                paid_m = round(sum(a for d, k, a in tx if k == "PAID" and mo <= d < nxt), 2)
                paid_td = round(sum(a for d, k, a in tx if k == "PAID" and d < nxt), 2)
                rec_td = round(sum(a for d, k, a in tx if k == "RECOVERED" and d < nxt), 2)
                closed = closes is not None and closes < nxt
                reserve = 0.0 if closed else round(max(0.0, c["paid"] - paid_td) * float(rng.uniform(0.9, 1.4)), 2)
                ws.append([no, refs[no], c["loss"], {"PLUMB": "Water - plumbing", "APPL": "Water - appliance"}.get(
                    c["kind"], c["kind"].title()), paid_m, paid_td, rec_td, reserve, "Closed" if closed else "Open"])
                nrow += 1
            for col, wdt in zip("ABCDEFGHI", (16, 15, 12, 18, 14, 13, 16, 18, 18)):
                ws.column_dimensions[col].width = wdt
            for row in ws.iter_rows(min_row=3):
                row[2].number_format = "mm/dd/yyyy"
                for cell in row[4:8]:
                    cell.number_format = "#,##0.00"
        wb.save(path)
        return nrow

    def payments_file(self, path):
        rng = self.rng
        rows = []
        chk = 504100
        for no, d, kind, amt, _ in sorted(self.payments, key=lambda p: (p[1], p[0])):
            if d > K.EXTRACT:
                continue
            chk += int(rng.integers(1, 3)) if kind in ("INDEMNITY", "EXPENSE") else 0
            rows.append([no, iso(d), kind, "%.2f" % amt, str(chk) if kind in ("INDEMNITY", "EXPENSE") else "",
                         {"INDEMNITY": "INSURED", "EXPENSE": "VENDOR", "VOID": "INSURED", "RECOVERY": "THIRD PARTY"}[kind]])
        for i, r in enumerate(rows):
            r.insert(0, "P%07d" % (3104000 + i * 3))
        return write_csv(path, ["transaction_id", "claim_number", "transaction_date", "transaction_type", "amount",
                                "check_number", "payee_type"], rows)

    def codes(self, path):
        return write_csv(path, ["code_set", "cause_code", "description", "maps_to_2024"], CODE_TABLE)

    # ---- the county assessor
    def parcels(self, path):
        rng = self.rng
        rows = []
        lu_desc = {"R-SFD": "Residential, single-family detached", "R-TWN": "Residential, townhouse",
                   "R-DUP": "Residential, two-family", "R-MH": "Residential, manufactured home",
                   "R-APT": "Residential, apartments", "C-RET": "Commercial, retail", "C-OFF": "Commercial, office",
                   "I-LGT": "Industrial, light", "V-RES": "Vacant land, residential", "F-AG": "Farm, agricultural",
                   "E-EX": "Exempt"}
        for p in self.w.parcels:
            mkt = (p["land"] + p["bldg"]) * 1.0
            assessed = mkt * K.CLR_2025 * float(rng.lognormal(0, 0.11))
            land = int(round(assessed * p["land"] / mkt / 10.0)) * 10
            imp = int(round(assessed / 10.0)) * 10 - land
            p["assessed_land"], p["assessed_imp"] = land, imp
            hs = "H" if p["homestead"] == "Y" else ""
            sale = self._sale(p)
            rows.append([p["parcel_id"], p["town"], K.TOWN_NAME[p["town"]].upper(), p["land_use"], lu_desc[p["land_use"]],
                         hs, "%.1f" % p["x"], "%.1f" % p["y"], "%.3f" % float(rng.uniform(0.12, 1.4)), land, imp,
                         land + imp, sale[0], sale[1]])
        # the roll's other parcels: commercial, industrial, vacant, farm and exempt land
        for town, _, _ in K.TOWNS:
            homes = [p for p in self.w.parcels if p["town"] == town]
            for i in range(int(len(homes) * 0.21)):
                q = homes[int(rng.integers(0, len(homes)))]
                lu = rng.choice(["C-RET", "C-OFF", "I-LGT", "V-RES", "F-AG", "E-EX"], p=[0.18, 0.1, 0.06, 0.38, 0.18, 0.1])
                x, y = q["x"] + rng.normal(0, 700), q["y"] + rng.normal(0, 700)
                pid = q["parcel_id"][:6] + "%04d" % (int(q["parcel_id"][-4:]) + 5000 + i) if False else \
                    "%s-%03d-%04d" % (q["parcel_id"][:2], 900 + (i // 9000), (i * 7 + 13) % 10000)
                land = int(rng.lognormal(math.log(14000), 0.7)) // 10 * 10
                imp = 0 if lu in ("V-RES", "F-AG") and rng.random() < 0.7 else int(rng.lognormal(math.log(60000), 0.9)) // 10 * 10
                rows.append([pid, town, K.TOWN_NAME[town].upper(), lu, lu_desc[lu], "F" if lu == "F-AG" and rng.random()
                             < 0.4 else "", "%.1f" % x, "%.1f" % y, "%.3f" % float(rng.lognormal(0.5, 1.0)), land, imp,
                             land + imp, "", ""])
        ids = [r[0] for r in rows]
        assert len(set(ids)) == len(ids), "parcel ids collide"
        rows.sort(key=lambda r: r[0])
        return write_csv(path, ["parcel_id", "municipality_code", "municipality", "land_use_code", "land_use",
                                "homestead_farmstead", "x_coord_ft", "y_coord_ft", "acres", "assessed_land",
                                "assessed_improvement", "assessed_total", "last_sale_date", "last_sale_price"], rows)

    def _sale(self, p):
        rng = self.rng
        if rng.random() < 0.55:
            return "", ""
        d = dt.date(int(rng.integers(1999, 2026)), int(rng.integers(1, 13)), int(rng.integers(1, 29)))
        price = (p["land"] + p["bldg"]) * (0.45 + 0.55 * (d.year - 1998) / 28.0) * float(rng.lognormal(0, 0.12))
        return iso(d), int(round(price / 100.0)) * 100

    def dwellings(self, path):
        rng = self.rng
        rows = []
        for p in self.w.parcels:
            rows.append([p["parcel_id"], 1, p["year_built"], p["foundation"], p["full"], p["half"],
                         ("%.1f" % p["stories"]).replace(".0", ""), p["wall"], p["area"],
                         rng.choice(["GAS", "OIL", "HEAT PUMP", "ELECTRIC"], p=[0.46, 0.22, 0.2, 0.12]),
                         rng.choice(["A", "B", "C", "D"], p=[0.08, 0.32, 0.48, 0.12])])
            if p["land_use"] == "R-SFD" and rng.random() < 0.011:
                # a second card: a detached in-law cottage or a garage apartment on the same parcel
                rows.append([p["parcel_id"], 2, int(min(2025, p["year_built"] + rng.integers(5, 60))),
                             rng.choice(["SLAB", "CRAWL"]), 1, 0, "1", "FRAME", int(rng.integers(380, 900)),
                             "ELECTRIC", "C"])
        rows.sort(key=lambda r: (r[0], r[1]))
        return write_csv(path, ["parcel_id", "card_number", "year_built", "foundation", "full_baths", "half_baths",
                                "stories", "exterior_wall", "living_area_sqft", "heating", "grade"], rows)

    def appeals(self, path):
        rng = self.rng
        rows = []
        seq = 0
        for p in self.w.parcels:
            if p["land_use"] != "R-SFD" or rng.random() > 0.022:
                continue
            seq += int(rng.integers(1, 4))
            before = p["assessed_land"] + p["assessed_imp"]
            filed = dt.date(2025, 8, 1) + dt.timedelta(int(rng.integers(0, 30)))
            hearing = dt.date(2025, 10, 1) + dt.timedelta(int(rng.integers(0, 70)))
            dec = rng.choice(["REDUCED", "SUSTAINED", "WITHDRAWN", "INCREASED"], p=[0.52, 0.30, 0.12, 0.06])
            after = before
            if dec == "REDUCED":
                after = int(round(before * rng.uniform(0.72, 0.95) / 10.0)) * 10
            elif dec == "INCREASED":
                after = int(round(before * rng.uniform(1.04, 1.18) / 10.0)) * 10
            p["appeal_after"] = after
            rows.append(["A26-%04d" % seq, p["parcel_id"], iso(filed), iso(hearing), dec, before,
                         after if dec in ("REDUCED", "INCREASED", "SUSTAINED") else "", "2026"])
        return write_csv(path, ["appeal_number", "parcel_id", "date_filed", "hearing_date", "decision",
                                "assessed_total_before", "assessed_total_after", "tax_year"], rows)

    def clr(self, path):
        rows = []
        hist = [(2016, 0.562), (2017, 0.549), (2018, 0.533), (2019, 0.518), (2020, 0.507), (2021, 0.496),
                (2022, 0.478), (2023, 0.466), (2024, 0.459), (2025, K.CLR_2025), (2026, K.CLR_2026)]
        for y, v in hist:
            rows.append([K.COUNTY.replace(" County", "").upper(), y, "%.3f" % v, "%.2f" % (1 / v),
                         "%d-07-01" % y, "%d-06-30" % (y + 1), "%d sales" % (y - 1)])
        return write_csv(path, ["county", "ratio_year", "common_level_ratio", "factor", "effective_from",
                                "effective_to", "based_on"], rows)

    # ---- the water authority's GIS layers and flow-test log
    def zones_geojson(self, path, zoner):
        feats = []
        edits = {"PZ-1": "2023-05-11", "PZ-2": "2025-11-14", "PZ-3": "2025-11-14", "PZ-4": "2021-09-02"}
        types = {"PZ-1": "GRAVITY", "PZ-2": "BOOSTED", "PZ-3": "GRAVITY", "PZ-4": "GRAVITY"}
        for z in K.ZONES:
            rings = zoner.polys[z[0]]
            if len(rings) == 1:
                geom = {"type": "Polygon", "coordinates": [[list(v) for v in rings[0]]]}
            else:
                geom = {"type": "MultiPolygon", "coordinates": [[[list(v) for v in r]] for r in rings]}
            feats.append({"type": "Feature", "properties": {"ZONE_ID": z[0], "ZONE_NAME": z[1].upper(),
                                                            "SUPPLY": z[2], "HGL_FT": z[3], "ZONE_TYPE": types[z[0]],
                                                            "LAST_EDIT": edits[z[0]]}, "geometry": geom})
        doc = {"type": "FeatureCollection", "name": "TCWA_PRESSURE_ZONES",
               "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::2272"}}, "features": feats}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, separators=(",", ":"))
        return len(feats)

    def hydrants_geojson(self, path, tests_path):
        """the register as of 30 June 2026 and the flow-test log; the April 2024 renumbering reused the old range, so
        most numbers before it belong to another hydrant after it"""
        rng = self.rng
        hs = self.w.hydrants
        n = len(hs)
        old = rng.permutation(n)
        new = rng.permutation(n)
        for i, h in enumerate(hs):
            h["old_id"] = "H-%05d" % (10001 + old[i]) if h["installed"] < RENUMBER.year else ""
            h["new_id"] = "H-%05d" % (10001 + new[i])
        feats = []
        for h in sorted(hs, key=lambda h: h["new_id"]):
            feats.append({"type": "Feature", "properties": {
                "HYDRANT_ID": h["new_id"], "FORMER_ID": h["old_id"], "STATUS": h["status"], "OWNER": h["owner"],
                "ZONE_ID": h["zone"], "MAIN_DIAM_IN": h["main"], "INSTALL_YEAR": h["installed"],
                "MUNI_CODE": h["town"]}, "geometry": {"type": "Point", "coordinates": [h["x"], h["y"]]}})
        doc = {"type": "FeatureCollection", "name": "TCWA_HYDRANTS",
               "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::2272"}}, "features": feats}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, separators=(",", ":"))
        rows = []
        tid = 61000
        for h in hs:
            for t in h["tests"]:
                tid += int(rng.integers(1, 3))
                hid = h["old_id"] if (t["date"] < RENUMBER and h["old_id"]) else h["new_id"]
                rows.append(["FT%06d" % tid, hid, iso(t["date"]), t["static"], t["resid"], t["flow"], t["crew"]])
        rows.sort(key=lambda r: (r[2], r[0]))
        write_csv(tests_path, ["test_id", "hydrant_id", "test_date", "static_psi", "residual_psi", "flow_gpm",
                               "tested_by"], rows)
        return len(feats), len(rows)
