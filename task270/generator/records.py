"""The pack's data files for task270, each in its own system's layout: Hallowmere's F-gas register (packs, and
integral cabinets and cold rooms) and store list, Kelbray's job sheet export (day-first dates, store numbers without
the chain's leading zeros, trade names on some sheets) and cylinder log, Tarnley's daily receiver levels under its own
pack tags and the tag list, and the stores' electricity readings."""
import csv
import datetime as dt

import numpy as np
import pandas as pd

import common as K
import world as W

ENGINEERS = ["A. Kenyon", "M. Dobson", "S. Pratt", "L. Haworth", "K. Nolan", "R. Bisset", "J. Firth", "D. Carr",
             "T. Ostle", "P. Varey"]
TEAM = {"YOR": [0, 1, 6], "LAN": [2, 3, 7], "NE": [4, 5, 8], "CUM": [9, 6]}


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        w.writerows(rows)


def dmy(d):
    return d.strftime("%d/%m/%Y")


def gas_label(gas, rng):
    return K.TRADE[gas] if gas in K.TRADE and rng.random() < 0.18 else gas


class Records:
    def __init__(self, w, seed=K.SEED):
        self.w, self.seed = w, seed
        self.st, self.pk = w["stores"], w["packs"]
        self.store_name = {s.store: "Hallowmere %s" % s.town for s in self.st.itertuples(index=False)}
        self.counts = {}

    # ---- the stores and the register ----
    def stores(self, path):
        rows = []
        for s in self.st.itertuples(index=False):
            closed = W.CLOSED.get(s.town)
            rows.append(["%03d" % s.store, self.store_name[s.store], K.REGION_NAME[s.region], s.opened,
                         dmy(closed) if closed else "", s.sqm])
        write_csv(path, ["store_no", "store_name", "region", "opened", "closed", "sales_area_sqm"], rows)
        self.counts["stores"] = len(rows)

    def register_rows(self):
        rng = np.random.default_rng([self.seed, 41])
        packs = []
        for p, r in self.pk.iterrows():
            gas = r.gas
            if p in self.w["retro"] and not self.w["retro"][p][2]:
                gas = self.w["retro"][p][1]
            since = dt.date(int(r.installed), int(rng.integers(2, 12)), int(rng.integers(1, 28)))
            dec = self.w["dec"].get(p)
            packs.append([r.code, "%03d" % r.store, self.store_name[r.store], gas, r.charge, dmy(since),
                          dmy(dec[0]) if dec else "", "Tarnley"])
        for c in self.w["co2"]:
            code = "%03d/%s" % (c["store"], c["kind"])
            packs.append([code + "C", "%03d" % c["store"], self.store_name[c["store"]], "R744", c["charge"],
                          dmy(c["since"]), "", "Tarnley"])
        packs.sort(key=lambda x: (x[0]))
        eq = [[e.asset, "%03d" % e.store, e.type, e.gas, e.charge, e.installed]
              for e in self.w["eq"].itertuples(index=False)]
        return packs, eq

    # ---- Kelbray's job sheets and cylinder log ----
    def jobs(self, path, cyl_path):
        rng = np.random.default_rng([self.seed, 43])
        rows, cyl = [], []
        jb = self.w["jobs"].sort_values(["date", "hour", "job"])
        cyl_no = {g: 0 for g in K.GWP}
        stock = {}

        def cylinder(g, kg, day, job, region, out=True):
            key = (region, g)
            c = stock.get(key)
            if c is None or c[1] < kg + 0.5:
                cyl_no[g] += 1
                serial = "KR-%s-%04d" % (g.replace("R", ""), 300 + 37 * cyl_no[g] % 9000 + cyl_no[g])
                c = [serial, round(float(rng.choice([10.0, 11.3, 12.0, 45.0 if kg > 9 else 12.0])) + 0.0, 1)]
                c[1] = max(c[1], round(kg + 2.0, 1))
                stock[key] = c
            before = round(c[1] + float(rng.uniform(7.8, 8.6)), 1)          # gross, cylinder tare included
            c[1] = round(c[1] - kg, 1)
            if day.year == K.YEAR:
                cyl.append([c[0], g, job, dmy(day), before, round(before - kg, 1)])

        for j in jb.itertuples(index=False):
            if j.type == "RETROFIT":           # retrofits were done by the gas supplier's own team, not Kelbray
                continue
            r = self.pk.loc[j.pack]
            day = j.date
            eng = ENGINEERS[TEAM[r.region][int(rng.integers(0, len(TEAM[r.region])))]]
            g = j.gas
            arr = "" if j.arr is None or (isinstance(j.arr, float) and np.isnan(j.arr)) else "%.1f" % j.arr
            dep = "" if j.dep is None or (isinstance(j.dep, float) and np.isnan(j.dep)) else "%.1f" % j.dep
            rows.append([j.job, dmy(day), int(r.store), r.kind, j.type, gas_label(g, rng), "%.1f" % j.charged,
                         "%.1f" % j.recovered if j.recovered else "0.0", arr, dep, j.leak, eng])
            if j.charged > 0:
                cylinder(g, j.charged, day, j.job, r.region)
        for c in self.w["co2"]:
            code = "%sC" % c["kind"]
            rows.append([90000 + c["store"], dmy(c["since"]), c["store"], code, "COMMISSIONING", "R744",
                         "%.1f" % c["charge"], "0.0", "", "%.1f" % c["full"], "N", "Kelbray projects"])
        # cabinets and cold rooms: one sheet line per asset; some handhelds stamp the visit's total on every line
        jn = 70500
        for v in self.w["visits"]:
            reg = v["region"]
            eng = ENGINEERS[TEAM[reg][int(rng.integers(0, len(TEAM[reg])))]]
            tot = round(sum(v["kg"]), 1)
            jn += int(rng.integers(1, 5))
            for a, kg in zip(v["assets"], v["kg"]):
                shown = tot if v["stamp_total"] else kg
                rows.append([jn, dmy(v["date"]), v["store"], a, "REPAIR", gas_label(v["gas"], rng), "%.1f" % shown,
                             "0.0", "", "", "Y", eng])
            cylinder(v["gas"], tot, v["date"], jn, reg)
        rows.sort(key=lambda x: (dt.datetime.strptime(x[1], "%d/%m/%Y"), x[0]))
        write_csv(path, ["job_no", "job_date", "store", "asset", "job_type", "refrigerant", "charged_kg",
                         "recovered_kg", "receiver_arrival_pct", "receiver_departure_pct", "leak_found", "engineer"],
                  rows)
        cyl.sort(key=lambda x: (dt.datetime.strptime(x[3], "%d/%m/%Y"), x[2], x[0]))
        write_csv(cyl_path, ["cylinder", "refrigerant", "job_no", "job_date", "gross_before_kg", "gross_after_kg"],
                  cyl)
        self.counts["jobs"], self.counts["cylinders"] = len(rows), len(cyl)

    # ---- Tarnley's receiver levels and tags ----
    def levels(self, path, tag_path):
        rng = np.random.default_rng([self.seed, 47])
        L = self.w["levels"]
        rows, tags = [], []
        days = W.DAYS
        guard = {pd.Timestamp(2025, 12, 30), pd.Timestamp(2025, 12, 31), pd.Timestamp(2026, 1, 1),
                 pd.Timestamp(2026, 1, 2), pd.Timestamp(2026, 12, 30), pd.Timestamp(2026, 12, 31)}
        for p, r in self.pk.iterrows():
            tag = "HFS-%03d-%s" % (r.store, r.kind)
            tags.append([tag, r.code, self.store_name[r.store]])
            out = set()
            for _ in range(int(rng.integers(0, 4))):          # communications outages, a day to a few days
                s = int(rng.integers(0, len(days) - 6))
                out.update(range(s, s + int(rng.integers(1, 5))))
            for t, day in enumerate(days):
                v = L[p, t]
                if np.isnan(v):
                    continue
                if t in out and day not in guard:
                    continue
                n = 24 if rng.random() > 0.01 or day in guard else int(rng.integers(9, 23))
                status = "OK"
                lv = "%.1f" % v
                if day not in guard and rng.random() < 0.002:
                    status, lv = "SENSOR FAULT", ""
                rows.append([day.strftime("%Y-%m-%d"), tag, lv, n, status])
        for c in self.w["co2"]:
            tag = "HFS-%03d-%sC" % (c["store"], c["kind"])
            tags.append([tag, "%03d/%sC" % (c["store"], c["kind"]), self.store_name[c["store"]]])
            for day in days:
                if day.date() < c["since"]:
                    continue
                rows.append([day.strftime("%Y-%m-%d"), tag, "%.1f" % (c["full"] + rng.normal(0, 0.6)), 24, "OK"])
        rows.sort(key=lambda x: (x[0], x[1]))
        write_csv(path, ["date", "bureau_tag", "receiver_level_pct", "readings", "status"], rows)
        tags.sort()
        write_csv(tag_path, ["bureau_tag", "pack_code", "site"], tags)
        self.counts["levels"], self.counts["tags"] = len(rows), len(tags)

    # ---- electricity (a distractor) ----
    def power(self, path):
        rng = np.random.default_rng([self.seed, 53])
        rows = []
        for s in self.st.itertuples(index=False):
            base = s.sqm * rng.uniform(26, 34)
            for y in (2024, 2025, 2026):
                for m in range(1, 13):
                    if s.town in W.CLOSED and dt.date(y, m, 1) > W.CLOSED[s.town]:
                        continue
                    season = 1 + 0.12 * np.cos(2 * np.pi * (m - 7) / 12)
                    rows.append(["%03d" % s.store, "%d-%02d" % (y, m), int(base * season * rng.uniform(0.95, 1.05))])
        write_csv(path, ["store_no", "month", "kwh"], rows)
        self.counts["power"] = len(rows)
