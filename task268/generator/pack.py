"""Write the evidence pack from the world: the claims extract, the representatives table, the region drawing, the
pricing mart's exposure workbook, policy admin's in-force file and change log, the aggregator report and the documents."""
import csv
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook

import common as K
import docs as DC
import world as W

NB = {"PH": "Policyholder", "TPD": "Third party", "INS": "Third-party insurer", "SOL": "Representative",
      "CMC": "Representative"}
TOD = {"PH": (7.5, 21.5), "TPD": (8.0, 20.0), "INS": (9.0, 17.0), "SOL": (9.0, 17.5), "CMC": (8.5, 18.0)}


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(header)
        wr.writerows(rows)
    return len(rows)


def _ds(d):
    return "" if d is None else d.isoformat()


class Pack:
    def __init__(self, world):
        self.w = world
        self.r = np.random.default_rng(world.ss.spawn(1)[0])
        self._claim_rows()

    # ------------------------------------------------------------------ claims
    def _claim_rows(self):
        w, r = self.w, self.r
        acc_attr = {}
        recs = []
        for c in w.all_claims:
            key = c["accident"]
            if key not in acc_attr:
                prod = c["product"]
                reg = c["region"]
                if c["head"] == "OD":
                    cov = "COMP"
                elif c["head"] in ("THEFT", "FIRE"):
                    cov = "COMP" if r.random() < 0.86 else "TPFT"
                elif c["head"] == "GLASS":
                    cov = "COMP" if r.random() < 0.95 else "TPFT"
                else:
                    cov = W.COVERS[int(r.choice(3, p=W.COVER_MIX[reg]))]
                pol = ("PC" if prod == "PC" else "CV") + "%07d" % int(r.integers(1000000, 9999999))
                acc_attr[key] = (pol, W.VRM(r), W.DIST_PICK(r, reg), cov)
            pol, vrm, dist, cov = acc_attr[key]
            lo, hi = TOD[c["route"]]
            hh = float(r.uniform(lo, hi))
            local = dt.datetime.combine(c["notified"], dt.time(int(hh), int((hh % 1) * 60), int(r.integers(60))))
            c["_attr"] = (pol, vrm, dist, cov)
            c["_local"] = local
            if c["notified"] <= K.EXTRACT:
                recs.append(c)
        by_idx = {c["idx"]: c for c in w.all_claims}
        for t in w.twins:
            ph = by_idx[t["twin_of"]]
            t["_attr"] = ph["_attr"]
            lo = dt.datetime.combine(t["acc"], dt.time(7, 0))
            tl = ph["_local"] - dt.timedelta(hours=t["twin_hours"])
            t["_local"] = tl if tl > lo else lo + (ph["_local"] - lo) / 2
            t["notified"] = t["_local"].date()
            t["closed_on"] = ph["notified"] + dt.timedelta(days=1)
            recs.append(t)
        recs.sort(key=lambda c: (c["_local"], c["accident"][4], c.get("claimant") or 0, "twin_of" in c))
        seq_l, seq_m, seq_n = 418200, 1004113, 2000517
        for c in recs:
            if c["notified"] < K.MIGRATION:
                seq_l += int(r.integers(1, 4))
                seq_m += int(r.integers(1, 3))
                c["_legacy"] = "CL/%06d" % seq_l
                c["_ref"] = "MC%08d" % seq_m
            else:
                seq_n += int(r.integers(1, 3))
                c["_legacy"] = ""
                c["_ref"] = "MC%08d" % (seq_n + 10000000)
        self.claims = recs

    def claim_rows(self):
        rows = []
        for c in self.claims:
            pol, vrm, dist, cov = c["_attr"]
            if c["notified"] < K.MIGRATION:
                note = c["notified"].isoformat()
            else:
                note = K.to_utc(c["_local"]).strftime("%Y-%m-%dT%H:%M:%SZ")
            rows.append([c["_ref"], c["_legacy"], pol, vrm, c["product"], cov, dist, c["acc"].isoformat(), note,
                         c["head"], "" if c.get("claimant") is None else c["claimant"], NB[c["route"]],
                         c["rep"] or "", c["status"], _ds(c["closed_on"]), "%.2f" % c["paid"], "%.2f" % c["outstanding"]])
        return rows

    # ------------------------------------------------------------------ lookups
    def rep_rows(self):
        return [[rp["ref"], rp["name"], rp["type"], rp["regulator"], rp["number"], rp["town"]]
                for rp in sorted(self.w.reps, key=lambda x: x["ref"])]

    @staticmethod
    def district_rows():
        out = []
        for code, name, ds in K.REGIONS:
            for d in sorted(ds.split(), key=lambda x: (x.rstrip("0123456789"), int(x[len(x.rstrip("0123456789")):]))):
                out.append([d, code, name])
        return out

    # ------------------------------------------------------------------ exposure workbook
    def write_exposure(self, path):
        wb = Workbook()
        wb.remove(wb.active)
        rows = self.w.exposure
        for y in range(2019, 2026):
            ws = wb.create_sheet(str(y))
            if y <= 2022:
                ws.append(["period", "region_code", "product_code", "cover_code", "earned_vehicle_days"])
                for (yy, m, reg, prod, cov, v) in rows:
                    if yy == y:
                        ws.append([yy * 100 + m, K.OLD_CODE[reg], "P" if prod == "PC" else "C",
                                   {"COMP": 1, "TPFT": 2, "TPO": 3}[cov], int(round(v * 365.25))])
                widths = (9, 12, 13, 11, 20)
            else:
                ws.append(["month", "sales_region", "product", "cover", "earned_car_years"])
                for (yy, m, reg, prod, cov, v) in rows:
                    if yy == y:
                        ws.append(["%d-%02d" % (yy, m), reg, prod, cov, v])
                        ws.cell(ws.max_row, 5).number_format = "0.00"
                widths = (9, 13, 9, 8, 17)
            for i, wd in enumerate(widths):
                ws.column_dimensions["ABCDE"[i]].width = wd
            ws.freeze_panes = "A2"
        wb.save(path)

    # ------------------------------------------------------------------ policies
    def inforce_rows(self):
        rows = []
        for v in self.w.vehicles:
            te = dt.date(v["te"].year, v["te"].month, v["te"].day) - dt.timedelta(days=1)
            rows.append([v["policy"], v["ts"].isoformat(), te.isoformat(), v["product"], v["cover"], v["dist"], v["vrm"],
                         v["on"].isoformat(), _ds(v["off"]), _ds(v["canc"]), v["channel"], "%.2f" % v["prem"]])
        rows.sort(key=lambda x: (x[0], x[7], x[6]))
        return rows

    def change_rows(self):
        r = np.random.default_rng(self.w.ss.spawn(1)[0])
        ch = sorted(self.w.changes, key=lambda c: (c["proc"], c["policy"], c["eff"], c["type"]))
        rows, seq = [], 5502917
        for c in ch:
            seq += int(r.integers(1, 6))
            rows.append(["MTA%08d" % seq, c["policy"], c["type"], c["eff"].isoformat(), c["proc"].isoformat(),
                         c.get("district", ""), c.get("cover", ""), c.get("old_vrm", "") or "", c.get("new_vrm", "") or "",
                         c.get("detail", "")])
        return rows

    # ------------------------------------------------------------------ the aggregator report (distractor)
    def write_aggregator(self, path):
        r = np.random.default_rng(self.w.ss.spawn(1)[0])
        wb = Workbook()
        ws = wb.active
        ws.title = "Quotes and sales"
        ws.append(["month", "sales_region", "quotes_returned", "click_throughs", "sales", "average_quoted_premium_gbp"])
        for y, m in [(2025, m) for m in range(10, 13)] + [(2026, m) for m in range(1, 10)]:
            for reg in K.REG:
                q = int(W.CY2025[reg] * float(r.uniform(1.9, 2.6)))
                ct = int(q * float(r.uniform(0.061, 0.083)))
                s = int(ct * float(r.uniform(0.21, 0.29)))
                ws.append(["%d-%02d" % (y, m), reg, q, ct, s, round(float(r.normal(612, 40)) * (1.18 if reg == "Mersey" else 1.0), 2)])
                ws.cell(ws.max_row, 6).number_format = "#,##0.00"
        for i, wd in enumerate((9, 13, 16, 15, 8, 27)):
            ws.column_dimensions["ABCDEF"[i]].width = wd
        ws.freeze_panes = "A2"
        wb.save(path)


def write_pack(out, seed=K.SEED):
    w = W.World(seed)
    pk = Pack(w)
    p = lambda k: os.path.join(out, K.FILES[k])
    n = {}
    n["claims"] = _w(p("claims"), ["claim_ref", "legacy_claim_ref", "policy_ref", "vrm", "product", "cover",
                                   "risk_postcode_district", "accident_date", "notified_at", "head_of_claim",
                                   "claimant_no", "notified_by", "representative_ref", "status", "closed_on",
                                   "paid_to_date_gbp", "outstanding_gbp"], pk.claim_rows())
    n["reps"] = _w(p("reps"), ["representative_ref", "firm_name", "firm_type", "regulator", "regulator_number", "town"],
                   pk.rep_rows())
    n["districts"] = _w(p("districts"), ["postcode_district", "sales_region_code", "sales_region"], pk.district_rows())
    pk.write_exposure(p("exposure"))
    n["inforce"] = _w(p("inforce"), ["policy_ref", "term_start", "term_end", "product", "cover", "risk_postcode_district",
                                     "vrm", "vehicle_on_cover_from", "vehicle_off_cover_from", "cancelled_from",
                                     "sales_channel", "annual_premium_gbp"], pk.inforce_rows())
    n["changes"] = _w(p("changes"), ["change_ref", "policy_ref", "change_type", "effective_from", "processed_on",
                                     "new_postcode_district", "new_cover", "old_vrm", "new_vrm", "detail"], pk.change_rows())
    pk.write_aggregator(p("aggregator"))
    DC.write_terms(p("terms"))
    DC.write_standard(p("standard"))
    DC.write_quote(p("quote"))
    with open(p("thread"), "w", encoding="utf-8", newline="\n") as f:
        f.write(DC.thread_text())
    return w, pk, n
