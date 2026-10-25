"""The county's records, written from the world as each office keeps them: the new appraisal system's 2026 roll, the
retired system's 2025 roll as an Excel export, the neighbourhood crosswalk, the Assessor's parcel change log, the
Recorder's 2025 deeds, the building department's permits, the Board of Review's hearings, the price index, and two
files the study does not use (the homestead credits and the levy sheet)."""
import csv
import datetime as dt

import numpy as np

import common as K

CLASS_2025 = {"R1": "Residential single family", "R2": "Residential condominium", "R0": "Residential vacant land"}


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(head)
        w.writerows(rows)


def dashed(b, p, n):
    return "%03d-%02d-%03d" % (b, p, n)


def undashed(b, p, n, suffix=0):
    return "%03d%02d%03d%d" % (b, p, n, suffix)


def money(v):
    return int(round(v))


class Records:
    def __init__(self, w):
        self.w = w
        self.r = np.random.default_rng(K.SEED_REC + 11)
        s = w.sf
        self.N = len(s["av25"])
        self.combined_second = {b for a, b in w.combine_pairs}
        self.combined_first = {a: b for a, b in w.combine_pairs}
        self.split = set(w.split_parents)
        big = len(K.CONDO_PROJECTS) - 1
        self.big = big
        for u in w.condo_units:
            b, p = w.condo_book[u["pj"]], w.condo_page[u["pj"]]
            u["id25"] = dashed(b, p, u["old"])
            u["id26"] = undashed(b, p, u["new"])
            name, nb, n, street = K.CONDO_PROJECTS[u["pj"]]
            label = ("%s-%d%02d" % (u["tower"], u["floor"], u["pos"] + 1)) if u["tower"] else \
                ("%d%02d" % (u["floor"], u["pos"] + 1))
            u["situs"] = "%d %s Unit %s" % (100 + 20 * u["pj"] + (3 if u["tower"] == "B" else 1), street, label)
        self.condo_year = {pj: int(1979 + (pj * 37) % 44) for pj in range(len(K.CONDO_PROJECTS))}
        self.condo_year[big] = 2016

    # ---- the 2026 roll (new system) ----------------------------------------------------------------------------
    def roll26_rows(self):
        w, s = self.w, self.w.sf
        rows = []
        for i in range(self.N):
            if i in self.split or i in self.combined_second:
                continue
            b, p, n = w.sf_id[i]
            nb = int(s["nbi"][i])
            total = int(s["av26"][i])
            sqft = int(w.sf_sqft[i])
            if i in self.combined_first:
                j = self.combined_first[i]
                total = int(s["av26"][i] + s["av26"][j])
                sqft = int(w.sf_sqft[i])
            land = int(round(total * w.sf_land_share[i], -2))
            rows.append([undashed(b, p, n), "R1", K.NBHD[nb][0], w.sf_street[i], int(w.sf_year[i]), sqft,
                         land, total - land, total])
        for i in w.split_parents:
            b, p, n = w.sf_id[i]
            nb = int(s["nbi"][i])
            total = int(s["av26"][i])
            share = w.split_share[i]
            house = int(round(total * share, -2))
            lot = total - house
            land_h = int(round(house * w.sf_land_share[i] * 0.8, -2))
            rows.append([undashed(b, p, n, 1), "R1", K.NBHD[nb][0], w.sf_street[i], int(w.sf_year[i]),
                         int(w.sf_sqft[i]), land_h, house - land_h, house])
            num, street = w.sf_street[i].split(" ", 1)
            rows.append([undashed(b, p, n, 2), "R0", K.NBHD[nb][0], "%d %s" % (int(num) + 2, street), "", "",
                         lot, 0, lot])
        for u in w.condo_units:
            if u.get("merged_into") is not None:
                continue
            total = int(u["av26"])
            land = int(round(total * 0.11, -2))
            area = int(round(u["area"] + (u["partner_area"] if "partner_area" in u else 0)))
            rows.append([u["id26"], "R2", K.NBHD[K.CONDO_PROJECTS[u["pj"]][1]][0], u["situs"],
                         self.condo_year[u["pj"]], area, land, total - land, total])
        rows.sort(key=lambda x: x[0])
        head = ["parcel_id", "class_code", "nbhd_code", "situs_address", "year_built", "living_area_sf",
                "land_value", "improvement_value", "total_assessed_value"]
        return head, rows

    # ---- the 2025 roll (retired system, Excel export) ------------------------------------------------------------
    def roll25_rows(self):
        w, s = self.w, self.w.sf
        rows = []
        for i in range(self.N):
            b, p, n = w.sf_id[i]
            nb = int(s["nbi"][i])
            total = int(s["av25"][i])
            land = int(round(total * w.sf_land_share[i], -2))
            rows.append([dashed(b, p, n), CLASS_2025["R1"], K.NBHD[nb][1], w.sf_street[i], int(w.sf_year[i]),
                         int(w.sf_sqft[i]), land, total - land, total])
        for u in w.condo_units:
            total = int(u["av25"])
            land = int(round(total * 0.11, -2))
            rows.append([u["id25"], CLASS_2025["R2"], K.NBHD[K.CONDO_PROJECTS[u["pj"]][1]][1], u["situs"],
                         self.condo_year[u["pj"]], int(round(u["area"])), land, total - land, total])
        rows.sort(key=lambda x: x[0])
        head = ["Parcel No.", "Class", "Neighborhood", "Situs Address", "Yr Built", "Sq Ft", "Land", "Improvements",
                "Total Assessed"]
        return head, rows

    def crosswalk_rows(self):
        rows = []
        for k, (code, name) in enumerate(K.NBHD):
            a = K.AREAS[k // 5]
            rows.append([code, name, a[0], a[1]])
        rows.sort(key=lambda x: x[0])
        return ["nbhd_code", "nbhd_name", "market_area", "market_area_name"], rows

    # ---- the Assessor's parcel change log --------------------------------------------------------------------------
    def change_rows(self):
        w, r = self.w, self.r
        rows = []
        for i in w.split_parents:
            b, p, n = w.sf_id[i]
            d = dt.date(2025, 2, 3) + dt.timedelta(days=int(r.integers(0, 300)))
            ref = "PLAT-25-%03d" % int(r.integers(10, 400))
            for suf in (1, 2):
                rows.append([d.isoformat(), "SPLIT", dashed(b, p, n), undashed(b, p, n, suf), ref])
        for a, bb in w.combine_pairs:
            ba, pa, na = w.sf_id[a]
            bb_, pb, nb_ = w.sf_id[bb]
            d = dt.date(2025, 2, 10) + dt.timedelta(days=int(r.integers(0, 290)))
            ref = "COMB-25-%03d" % int(r.integers(10, 400))
            rows.append([d.isoformat(), "COMBINE", dashed(ba, pa, na), undashed(ba, pa, na), ref])
            rows.append([d.isoformat(), "COMBINE", dashed(bb_, pb, nb_), undashed(ba, pa, na), ref])
        decl = "DECL-25-0117"
        for u in w.condo_units:
            if u["pj"] != self.big:
                continue
            if u.get("merged_into") is not None:
                rows.append([K.REDECLARED.isoformat(), "COMBINE", u["id25"], u["merged_into"]["id26"], decl])
            elif any(a is u for a, b in w.wex_combos):
                rows.append([K.REDECLARED.isoformat(), "COMBINE", u["id25"], u["id26"], decl])
            else:
                rows.append([K.REDECLARED.isoformat(), "RENUMBER", u["id25"], u["id26"], decl])
        rows.sort(key=lambda x: (x[0], x[2], x[3]))
        return ["effective_date", "change_type", "old_parcel_no", "new_parcel_id", "reference_doc"], rows

    # ---- the Recorder's 2025 deeds ---------------------------------------------------------------------------------
    def deed_rows(self):
        w, s, r = self.w, self.w.sf, self.r
        out = []
        for i in np.where(s["s25"])[0]:
            b, p, n = w.sf_id[i]
            u = r.random()
            dtype = "Warranty Deed" if u < 0.88 else ("Special Warranty Deed" if u < 0.97 else "Trustee's Deed")
            out.append(dict(rec=w.sf_recorded[i], deed=w.sf_deed[i], parcel=dashed(b, p, n), dtype=dtype,
                            cons=money(s["price"][i]), code="Q"))
        for t in w.sf_transfers:
            rec = t["deed"] + dt.timedelta(days=int(r.integers(1, 12)))
            if rec.year > 2025:
                rec = dt.date(2025, 12, 31)
            for i in t["i"]:
                b, p, n = w.sf_id[i]
                out.append(dict(rec=rec, deed=t["deed"], parcel=dashed(b, p, n), dtype=t["dtype"], cons=t["cons"],
                                code=t["code"], group=id(t)))
        for sale in w.condo_sales:
            u = sale["u"]
            if u["pj"] == self.big and sale["deed"] >= K.REDECLARED:
                b, p = w.condo_book[u["pj"]], w.condo_page[u["pj"]]
                parcel = dashed(b, p, u["new"])
            else:
                parcel = u["id25"]
            out.append(dict(rec=sale["recorded"], deed=sale["deed"], parcel=parcel, dtype="Warranty Deed",
                            cons=money(sale["price"]), code="Q"))
        # corrective deeds re-recorded to fix a legal description or a name, coded U6
        base = [x for x in out if x["code"] in ("Q", "U1", "U3")]
        for j in r.choice(len(base), 41, replace=False):
            x = base[int(j)]
            rec = x["rec"] + dt.timedelta(days=int(r.integers(9, 60)))
            if rec.year > 2025:
                continue
            out.append(dict(rec=rec, deed=rec - dt.timedelta(days=int(r.integers(0, 5))), parcel=x["parcel"],
                            dtype="Corrective " + x["dtype"], cons=x["cons"], code="U6"))
        out.sort(key=lambda x: (x["rec"], x["parcel"]))
        rows, inst, last_group = [], 431, {}
        for x in out:
            g = x.get("group")
            if g is not None and g in last_group:
                no = last_group[g]
            else:
                inst += int(1 + (r.random() < 0.6) + (r.random() < 0.3))
                no = "2025R%06d" % inst
                if g is not None:
                    last_group[g] = no
            rows.append([no, x["rec"].isoformat(), x["deed"].isoformat(), x["parcel"], x["dtype"], x["cons"],
                         x["code"]])
        head = ["instrument_no", "recorded_date", "deed_date", "parcel_no", "deed_type", "consideration",
                "validation_code"]
        return head, rows

    def index_rows(self):
        rows = [["%d-%02d" % ym, "%.1f" % v] for ym, v in self.w.index.items()]
        return ["period", "index_jan2025_100"], rows

    def permit_rows(self):
        w = self.w
        rows = []
        no = 25001
        allp = [(p["issued"], 0, p) for p in w.permits] + [(p["issued"], 1, p) for p in w.condo_permits]
        allp.sort(key=lambda t: (t[0], t[1]))
        for _, kind, pmt in allp:
            if kind == 0:
                b, p, n = w.sf_id[pmt["i"]]
                work = pmt["work"]
            else:
                u = pmt["u"]
                b, p, n = w.condo_book[u["pj"]], w.condo_page[u["pj"]], pmt["number"]
                work = "%s, Unit %s" % (pmt["work"], pmt["label"])
            no += int(1 + (self.r.random() < 0.7) * self.r.integers(1, 9))
            rows.append(["BP%d" % no, dashed(b, p, n), pmt["issued"].isoformat(),
                         pmt["finaled"].isoformat() if pmt["finaled"] else "", pmt["status"], work,
                         pmt["valuation"]])
        return ["permit_no", "parcel_no", "issued_date", "final_inspection_date", "status", "work_description",
                "declared_valuation"], rows

    def bor_rows(self):
        w = self.w
        rows = []
        for x in w.hearings:
            if x["cls"] == "R1":
                b, p, n = w.sf_id[x["i"]]
                parcel, cls = dashed(b, p, n), "SFR"
            else:
                parcel, cls = x["cu"]["id25"], "CONDO"
            rows.append([x["case"], parcel, cls, x["heard"].isoformat() if x["heard"] else "", x["decision"],
                         x["before"], x["after"] if x["after"] is not None else ""])
        return ["case_no", "parcel_no", "property_class", "hearing_date", "decision", "value_before",
                "value_after"], rows

    # ---- not used by the study ----------------------------------------------------------------------------------------
    def homestead_rows(self):
        head, roll = self.roll26_rows()
        r = np.random.default_rng(K.SEED_REC + 23)
        rows = []
        for x in roll:
            if x[1] == "R0":
                continue
            u = r.random()
            if u < 0.69:
                code, amt = "HS1", 25000
                if r.random() < 0.21:
                    code, amt = "HS65", 40000
                if r.random() < 0.03:
                    code, amt = "HSDV", int(min(x[8], 75000))
                rows.append([x[0], code, amt, "2026"])
        return ["parcel_id", "credit_code", "credit_amount", "tax_year"], rows
