"""Write target/ from the world: the exports each system would produce, with their own conventions."""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import params as P
from io_util import repack_xlsx, write_csv, write_pdf
from world import ITEM, World, index_day, stream, window
import docs

CLASS = {"0111": ("01.1.1", "Bread and cereals"), "0112": ("01.1.2", "Meat"), "0113": ("01.1.3", "Fish and seafood"),
         "0114": ("01.1.4", "Milk, cheese and eggs"), "0116": ("01.1.6", "Fruit"), "0117": ("01.1.7", "Vegetables"),
         "0119": ("01.1.9", "Food products n.e.c."), "0121": ("01.2.1", "Non-alcoholic beverages"),
         "0312": ("03.1.2", "Garments"), "0321": ("03.2.1", "Shoes and other footwear"),
         "0561": ("05.6.1", "Non-durable household goods"), "1213": ("12.1.3", "Personal care products")}

VARIETY = {
    "FV": ["loose, class 1", "loose, premium grade", "loose, value grade", "pre-packed, class 1"],
    "MF": ["fresh, store packed", "fresh, butcher counter", "free range, packed", "value pack"],
    "BC": ["Sunfield", "Ridgeway", "Harvest Gold", "store brand"],
    "DE": ["Meadowvale", "Coastline Dairy", "Ridgeway", "store brand"],
    "OF": ["Northbay", "Sunfield", "Golden Crest", "store brand"],
    "HS": ["Brightway", "Clearwell", "HomeCare", "store brand"],
    "PC": ["Puravia", "Clearwell", "Medica", "store brand"],
    "CF": ["plain cotton, regular fit", "blended, slim fit", "denim, straight leg", "synthetic, regular"],
}

OFFICERS = ["SR", "KD", "AM", "PT", "RB", "NH"]
ANALYSTS = ["GL", "MS", "HT"]


def ymstr(y, m):
    return "%04d-%02d" % (y, m)


def month_name(y, m):
    return dt.date(y, m, 1).strftime("%B %Y")


def xlsx_save(wb, path, creator, created, modified, title, company):
    wb.properties.creator = creator
    wb.save(path)
    repack_xlsx(path, creator, created, modified, title, company)


class Pack:
    def __init__(self, world, out):
        self.w = world
        self.out = out
        os.makedirs(out, exist_ok=True)
        self.rng = stream(20)
        self._staff()

    def path(self, name):
        return os.path.join(self.out, name)

    # people and kit --------------------------------------------------------------------------
    def _staff(self):
        rng = stream(21)
        ids = rng.choice(np.arange(100, 999), size=80, replace=False)
        devs = rng.choice(np.arange(1000, 9999), size=80, replace=False)
        self.collectors = {}
        k = 0
        for r in self.w.regions:
            n = 3 if r["ring"] == 0 else 2 + int(rng.random() < 0.4)
            self.collectors[r["code"]] = [("TC%03d" % ids[k + j], "HH-%04d" % devs[k + j]) for j in range(n)]
            k += n
        self.collector_of = {}
        for o in self.w.base_outlets:
            lst = self.collectors[o["region"]]
            self.collector_of[o["oid"]] = lst[int(rng.integers(0, len(lst)))]
        for o in self.w.outlets:
            if o["predecessor"] is not None:
                self.collector_of[o["oid"]] = self.collector_of[o["predecessor"]]
        vrng = stream(22)
        self.variety = {}
        for q in self.w.quotes:
            self.variety[q["qid"]] = int(vrng.integers(0, 4))
        self.region = {r["code"]: r for r in self.w.regions}

    def variety_text(self, q, k):
        opts = VARIETY[q["group"]]
        it = ITEM[q["item"]]
        return "%s, %s" % (opts[k % len(opts)], it["unit"])

    # the price database extract ----------------------------------------------------------------
    def quotes_csv(self):
        w = self.w
        rng = stream(23)
        rows = []
        vk = dict(self.variety)
        batch_seq = {}
        resent = set()
        visited = sorted({(r["qid"], r["y"], r["m"]) for r in w.records})
        om = sorted({(w.quotes[q]["oid"], y, m) for q, y, m in visited})
        for key in om:
            if rng.random() < P.RESENT_BATCH:
                resent.add(key)
        self.resent = resent
        self.batches = {}
        for (oid, y, m) in om:
            v = w.vis_index[(oid, y, m)]
            d0 = v["days"][0]
            s = batch_seq.get(d0, 100 + int(rng.integers(0, 40)))
            batch_seq[d0] = s + 1 + int(rng.integers(0, 3))
            self.batches[(oid, y, m)] = "LB%s%03d" % (d0.strftime("%y%m%d"), s)
        for r in sorted(w.records, key=lambda x: (x["y"], x["m"], w.quotes[x["qid"]]["quote_id"])):
            q = w.quotes[r["qid"]]
            o = w.outlet_for(q["oid"], r["y"], r["m"])
            if r["status"] == "R":
                vk[r["qid"]] = vk[r["qid"]] + 1 + int(r["variety_no"] % 3)
            new_codes = (r["y"], r["m"]) >= (2026, 8)
            status = {"P": "10", "U": "20", "R": "30"}[r["status"]] if new_codes else r["status"]
            price = "" if r["price"] is None else "%.2f" % r["price"]
            row = [ymstr(r["y"], r["m"]), q["quote_id"], o["nso_code"], q["item"], self.variety_text(q, vk[r["qid"]]),
                   price, status, self.batches[(q["oid"], r["y"], r["m"])]]
            rows.append(row)
            if (q["oid"], r["y"], r["m"]) in resent:
                dup = list(row)
                d = dt.datetime.strptime(row[7][2:8], "%y%m%d").date() + dt.timedelta(days=1 + int(rng.integers(0, 2)))
                dup[7] = "LB%s%03d" % (d.strftime("%y%m%d"), 600 + int(rng.integers(0, 300)))
                rows.append(dup)
        self.n_quote_rows = write_csv(self.path("cpi_field_quotes_2025-10_2026-09.csv"),
                                      ["ref_month", "quote_id", "outlet_code", "item_code", "variety", "price",
                                       "status", "load_batch"], rows)
        return self.n_quote_rows

    def status_codes_csv(self):
        rows = [["P", "Priced", "2019-04-01", "2026-08-02"], ["U", "Not available at visit", "2019-04-01", "2026-08-02"],
                ["R", "Priced, replacement variety", "2019-04-01", "2026-08-02"],
                ["10", "Priced", "2026-08-03", ""], ["20", "Not available at visit", "2026-08-03", ""],
                ["30", "Priced, replacement variety", "2026-08-03", ""]]
        write_csv(self.path("handheld_status_codes.csv"), ["status", "meaning", "used_from", "used_to"], rows)

    def item_list_csv(self):
        rows = []
        for c, it in sorted(ITEM.items()):
            cl = CLASS[c[:4]]
            rows.append([c, it["desc"], cl[0], cl[1], it["unit"]])
        write_csv(self.path("cpi_item_list_2026.csv"), ["item_code", "item_description", "coicop_class", "class_name",
                                                         "unit_of_measure"], rows)

    # the outlet register -----------------------------------------------------------------------
    def outlet_register(self):
        w = self.w
        wb = Workbook()
        ws = wb.active
        ws.title = "Outlets"
        hdr = ["Outlet code", "Contractor outlet no.", "Outlet name", "Address", "Region", "Outlet type", "Kind",
               "Chain", "In sample from", "In sample to"]
        ws.append(hdr)
        for c in ws[1]:
            c.font = Font(bold=True)
        kinds = {"supermarket": "Supermarket", "pharmacy_chain": "Pharmacy", "clothing_chain": "Clothing store",
                 "greengrocer": "Greengrocer", "butcher": "Butcher", "bakery": "Bakery", "convenience": "Convenience store",
                 "pharmacy": "Pharmacy", "boutique": "Clothing store", "hardware": "Hardware store"}
        for o in sorted(w.outlets, key=lambda x: (x["region"], x["nso_code"])):
            ws.append([o["nso_code"], o["tnum"], o["name"], o["address"], o["region"],
                       "Multiple" if o["stratum"] == "M" else "Independent", kinds[o["kind"]], o["chain"] or None,
                       o["added"], o["removed"]])
        for row in ws.iter_rows(min_row=2):
            for c in (row[8], row[9]):
                if c.value is not None:
                    c.number_format = "dd/mm/yyyy"
        ws2 = wb.create_sheet("Regions")
        ws2.append(["Region", "Region name", "Contractor area"])
        for c in ws2[1]:
            c.font = Font(bold=True)
        for r in w.regions:
            ws2.append([r["code"], r["name"], r["cname"]])
        xlsx_save(wb, self.path("cpi_outlet_register_2026-10.xlsx"), "Prices Division",
                  "2024-02-12T09:10:00Z", "2026-10-01T03:22:00Z", "CPI outlet register", "National Statistics Office")

    # the Field Quality Team's register ---------------------------------------------------------
    def backcheck_register(self):
        w = self.w
        rng = stream(24)
        wb = Workbook()
        wb.remove(wb.active)
        by_month = {}
        for b in w.backchecks:
            by_month.setdefault((b["y"], b["m"]), []).append(b)
        officer_of = {r["code"]: OFFICERS[i % len(OFFICERS)] for i, r in enumerate(w.regions)}
        for (y, m) in P.QUARTER:
            ws = wb.create_sheet(dt.date(y, m, 1).strftime("%b %Y"))
            ws.append(["Field Quality Team back-check register"])
            ws.append(["Reference month: %s" % month_name(y, m)])
            ws.append([])
            sep = (y, m) == (2026, 9)
            hdr = (["Region", "Outlet", "Quote", "Item", "Re-collected on", "Officer", "Collector price", "FQT price", "Found"]
                   if sep else
                   ["Region", "Outlet", "Quote", "Item", "Collector price", "Re-collected on", "FQT price", "Found", "Officer"])
            ws.append(hdr)
            for c in ws[4]:
                c.font = Font(bold=True)
            rows = sorted(by_month[(y, m)], key=lambda b: (b["region"], w.outlets[b["oid"]]["nso_code"], w.quotes[b["qid"]]["quote_id"]))
            final = []
            for b in rows:
                q = w.quotes[b["qid"]]
                o = w.outlets[b["oid"]]
                officer = officer_of[b["region"]] if rng.random() > 0.15 else OFFICERS[int(rng.integers(0, len(OFFICERS)))]
                when = b["fqt"].strftime("%d/%m/%Y") if (y, m) == (2026, 7) else b["fqt"]
                fqt = b["fqt_price"] if b["fqt_price"] is not None else None
                found = "Y" if b["fqt_price"] is not None else "N"
                if sep:
                    rec = [b["region"], o["nso_code"], q["quote_id"], q["item"], when, officer, b["rec_price"], fqt, found]
                else:
                    rec = [b["region"], o["nso_code"], q["quote_id"], q["item"], b["rec_price"], when, fqt, found, officer]
                final.append(rec)
            for rec in final:
                ws.append(rec)
            for row in ws.iter_rows(min_row=5):
                for c in row:
                    if isinstance(c.value, dt.date):
                        c.number_format = "dd/mm/yyyy"
        xlsx_save(wb, self.path("fqt_backcheck_register_2026q3.xlsx"), "Field Quality Team",
                  "2026-07-15T21:40:00Z", "2026-10-02T04:05:00Z", "Back-check register Q3 2026", "National Statistics Office")

    # the contractor's visit log -----------------------------------------------------------------
    def visit_log(self):
        w = self.w
        rng = stream(25)
        refs = rng.choice(np.arange(1000000, 9999999), size=5000, replace=False)
        rows = []
        k = 0
        recs = {}
        for r in w.records:
            if (r["y"], r["m"]) in P.QUARTER:
                recs.setdefault((w.quotes[r["qid"]]["oid"], r["y"], r["m"]), []).append(r)
        for (y, m) in P.QUARTER:
            for o in w.base_outlets:
                v = w.vis_index[(o["oid"], y, m)]
                if not v["days"]:
                    continue
                cur = w.outlet_for(o["oid"], y, m)
                col, dev = self.collector_of[o["oid"]]
                rr = recs.get((o["oid"], y, m), [])
                for d in v["days"]:
                    n = sum(1 for x in rr if x["vday"] == d)
                    if n == 0:
                        continue
                    start = dt.datetime.combine(d, dt.time(8, 30)) + dt.timedelta(minutes=int(rng.integers(0, 470)))
                    fin = start + dt.timedelta(minutes=int(8 + n * 1.3 + rng.integers(0, 14)))
                    rows.append(["V%07d" % refs[k], col, cur["tnum"], self.region[o["region"]]["cname"],
                                 start.strftime("%Y-%m-%dT%H:%M+12:00"), fin.strftime("%Y-%m-%dT%H:%M+12:00"), n, dev])
                    k += 1
        rows.sort(key=lambda x: (x[4], x[0]))
        self.visit_rows = rows
        write_csv(self.path("tallis_visit_log_2026-07_2026-09.csv"),
                  ["visit_ref", "collector", "outlet_no", "area", "started", "finished", "prices_entered", "device"], rows)

    def schedule(self):
        w = self.w
        rows = []
        for (y, m) in P.QUARTER:
            win = window(y, m)
            for o in w.base_outlets:
                v = w.vis_index[(o["oid"], y, m)]
                plan = v["days"][0] if v["days"] and v["days"][0] in win else win[(int(o["tnum"][1:]) + m) % len(win)]
                col, _ = self.collector_of[o["oid"]]
                rows.append([ymstr(y, m), o["tnum"], o["name"], self.region[o["region"]]["cname"], col,
                             plan.strftime("%d/%m/%Y")])
        rows.sort(key=lambda x: (x[0], x[3], x[1]))
        write_csv(self.path("tallis_collection_schedule_2026q3.csv"),
                  ["month", "outlet_no", "outlet_name", "area", "collector", "planned_visit"], rows)

    def calendar(self):
        rows = []
        for (y, m) in [(2025, 11), (2025, 12)] + [(2026, k) for k in range(1, 13)]:
            rows.append([index_day(y, m).isoformat(), "Index day"])
        for h in P.HOLIDAYS:
            if h >= dt.date(2025, 11, 1):
                rows.append([h.isoformat(), "Public holiday"])
        rows.sort()
        write_csv(self.path("nso_collection_calendar_2026.csv"), ["date", "event"], rows)

    # the commodity team's decisions -------------------------------------------------------------
    def reviews(self):
        w = self.w
        rng = stream(26)
        refs = rng.choice(np.arange(10000, 99999), size=600, replace=False)
        wb = Workbook()
        ws = wb.active
        ws.title = "Decisions"
        ws.append(["Review no.", "Quote", "Outlet", "Item", "Decision", "Decided on", "Analyst"])
        for c in ws[1]:
            c.font = Font(bold=True)
        rows = sorted(w.reviews, key=lambda x: (x["date"], w.quotes[x["qid"]]["quote_id"], x["final"]))
        for i, rv in enumerate(rows):
            q = w.quotes[rv["qid"]]
            o = w.outlet_for(q["oid"], rv["y"], rv["m"])
            analyst = "HT" if (not rv["final"] and rv["decision"] != "Query to contractor") else ANALYSTS[int(rng.integers(0, 2))]
            if rv["final"] and i > 0 and rows[i - 1]["qid"] == rv["qid"] and rows[i - 1]["decision"] != "Query to contractor":
                analyst = "HT"
            ws.append(["RV-%05d" % refs[i], q["quote_id"], o["nso_code"], q["item"], rv["decision"], rv["date"], analyst])
        for row in ws.iter_rows(min_row=2):
            row[5].number_format = "dd/mm/yyyy"
        xlsx_save(wb, self.path("commodity_replacement_decisions_2026.xlsx"), "Prices Division",
                  "2026-06-10T22:15:00Z", "2026-10-14T02:50:00Z", "Replacement decisions 2026", "National Statistics Office")

    # the contractor's quarterly return (context artifact) --------------------------------------
    def quarterly_return(self):
        w = self.w
        wb = Workbook()
        ws = wb.active
        ws.title = "Q3 2026 return"
        ws.append(["Tallis Field Research Ltd, quarterly activity return to the National Statistics Office"])
        ws.append(["Collection activity by area, July to September 2026, as uploaded from the handhelds before NSO validation"])
        ws.append(["Return version 1.0, submitted 9 October 2026 by L. Morrison, Contract Manager"])
        ws.append([])
        ws.append(["Area", "Month", "Outlets scheduled", "Outlet visits", "Prices entered", "Not available", "Replacements"])
        for c in ws[5]:
            c.font = Font(bold=True)
        visits = {}
        for row in self.visit_rows:
            key = (row[3], row[4][:7])
            visits[key] = visits.get(key, 0) + 1
        ent, una, rep = {}, {}, {}
        for r in w.records:
            if (r["y"], r["m"]) not in P.QUARTER:
                continue
            q = w.quotes[r["qid"]]
            key = (self.region[q["region"]]["cname"], ymstr(r["y"], r["m"]))
            mult = 2 if (q["oid"], r["y"], r["m"]) in self.resent else 1
            if r["status"] == "U":
                una[key] = una.get(key, 0) + mult
            else:
                ent[key] = ent.get(key, 0) + mult
                if r["status"] == "R":
                    rep[key] = rep.get(key, 0) + mult
        sched = {}
        for o in w.base_outlets:
            for (y, m) in P.QUARTER:
                key = (self.region[o["region"]]["cname"], ymstr(y, m))
                sched[key] = sched.get(key, 0) + 1
        for r in w.regions:
            for (y, m) in P.QUARTER:
                key = (r["cname"], ymstr(y, m))
                ws.append([r["cname"], dt.date(y, m, 1).strftime("%b %Y"), sched.get(key, 0), visits.get(key, 0),
                           ent.get(key, 0), una.get(key, 0), rep.get(key, 0)])
        xlsx_save(wb, self.path("tallis_quarterly_return_2026q3.xlsx"), "Tallis Field Research Ltd",
                  "2026-10-06T23:05:00Z", "2026-10-08T21:12:00Z", "Quarterly activity return Q3 2026",
                  "Tallis Field Research Ltd")

    # distractors ------------------------------------------------------------------------------
    def roster(self):
        rng = stream(27)
        wb = Workbook()
        ws = wb.active
        ws.title = "Collectors"
        ws.append(["Staff no.", "Area", "Role", "Started", "Last collection test", "Test result"])
        for c in ws[1]:
            c.font = Font(bold=True)
        rows = []
        for r in self.w.regions:
            for j, (cid, dev) in enumerate(self.collectors[r["code"]]):
                started = dt.date(2014 + int(rng.integers(0, 12)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                test = dt.date(2025, int(rng.integers(9, 13)), int(rng.integers(1, 28))) if rng.random() < 0.5 else \
                    dt.date(2026, int(rng.integers(1, 9)), int(rng.integers(1, 28)))
                rows.append([cid, r["cname"], "Team leader" if j == 0 and r["ring"] == 0 else "Price collector",
                             started, max(test, started), "Pass" if rng.random() < 0.93 else "Pass on resit"])
        for row in sorted(rows, key=lambda x: (x[1], x[0])):
            ws.append(row)
        for row in ws.iter_rows(min_row=2):
            row[3].number_format = "dd/mm/yyyy"
            row[4].number_format = "dd/mm/yyyy"
        xlsx_save(wb, self.path("tallis_collector_roster_2026-09.xlsx"), "Tallis Field Research Ltd",
                  "2025-01-20T01:00:00Z", "2026-09-30T05:40:00Z", "Collector roster", "Tallis Field Research Ltd")

    def regional_indices(self):
        rng = stream(28)
        rows = []
        for r in self.w.regions:
            lvl = {g: 1000 * float(np.exp(rng.normal(0.045, 0.012))) for g in ("All groups", "Food", "Housing and household", "Clothing and footwear", "Personal care")}
            for (y, m) in [(2026, 6), (2026, 7), (2026, 8), (2026, 9)]:
                for g in lvl:
                    lvl[g] *= float(np.exp(rng.normal(0.0028, 0.0035)))
                    rows.append([r["code"], r["name"], ymstr(y, m), g, "%.1f" % lvl[g]])
        write_csv(self.path("cpi_regional_indices_2026-06_2026-09.csv"),
                  ["region", "region_name", "month", "index_group", "index_dec2024_1000"], rows)

    # documents --------------------------------------------------------------------------------
    def documents(self):
        docs.pcqs(self.path("pcqs_price_collection_quality_standard_v3.pdf"))
        docs.fees(self.path("pcsa_schedule4_collection_fees.pdf"), self.w.regions)

    def write_all(self):
        self.quotes_csv()
        self.status_codes_csv()
        self.item_list_csv()
        self.outlet_register()
        self.backcheck_register()
        self.visit_log()
        self.schedule()
        self.calendar()
        self.reviews()
        self.quarterly_return()
        self.roster()
        self.regional_indices()
        self.documents()
        stamp = dt.datetime(2026, 10, 15, 8, 30).timestamp()
        for f in os.listdir(self.out):
            os.utime(self.path(f), (stamp, stamp))


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "target"
    Pack(World(), out).write_all()
    print("written", sorted(os.listdir(out)))
