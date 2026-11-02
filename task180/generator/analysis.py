"""The golden computation, from the shipped files only.

Main call. Each gas bar tank system's daily book (gauge close, bill-of-lading receipts on the drop's business
day, point-of-sale volume) gives its quarter shortfall. The meters' over-delivery in a quarter is the drift
rate times the quarter's exposure, the sum over days and hoses of each hose's litres sold times the litres it
had passed since its last calibration or replacement (work orders, through the register and the controller's
configuration). The drift rate is fitted across every tank system's earlier quarters (2024 Q1 to 2026 Q3,
each from its first recorded calibration on), quarter shortfall on exposure. October to December's expected
over-delivery comes out of each system's shortfall; the rest, per elapsed hour, is product lost to the ground.

Ask. Each cardlock drop's received litres are the gauge's increase over its delivery report plus the litres
the fleet drew from that tank inside the report's window (the host's UTC clock against the monitoring
service's CST); the drop the gauge never reported is rebuilt from the hourly readings either side of the
gap and the litres drawn between them; months by the drop, not the bill.
"""
import csv
import datetime as dt
import json
import os
import re
import zipfile
from collections import defaultdict

import numpy as np
import openpyxl

TD = dt.timedelta
GRADE_PROD = {"REG 87": "R", "PREM 91": "P", "DSL": "D"}
ATG_PROD = {"UNLEADED": "R", "PREMIUM": "P", "DIESEL": "D"}
BOL_PROD = {"Regular Unleaded": "R", "Premium Unleaded": "P", "ULS Diesel": "D"}
THRESHOLD = 0.75
Q4 = (dt.date(2026, 10, 1), dt.date(2026, 12, 31))


def rd(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def _nth_sunday(y, m, n):
    d = dt.date(y, m, 1)
    while d.weekday() != 6:
        d += TD(days=1)
    return d + TD(days=7 * (n - 1))


def to_cst(s):
    """'YYYY-MM-DD HH:MM ZZZ' with ZZZ CST or CDT -> naive CST datetime."""
    ts, z = s.rsplit(" ", 1)
    t = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M")
    return t - TD(hours=1) if z == "CDT" else t


def quarter_of(d):
    return (d.year, (d.month - 1) // 3 + 1)


def quarter_days(q):
    y, n = q
    a = dt.date(y, 3 * (n - 1) + 1, 1)
    b = dt.date(y + (n == 4), (3 * n) % 12 + 1, 1)
    return a, b - TD(days=1)


class Pack:
    def __init__(self, root):
        self.root = root
        self.p = lambda n: os.path.join(root, n)

    # ------------------------------------------------------------- gas bars
    def load_gasbars(self):
        reg = openpyxl.load_workbook(self.p("tpc_site_tank_register.xlsx"), data_only=True)
        tanks = {}
        for r in list(reg["Tanks"].iter_rows(values_only=True))[1:]:
            if str(r[0]).startswith("GB"):
                tanks[(r[0], r[3])] = dict(product={"Regular": "R", "Premium": "P", "Diesel": "D"}[r[4]], cap=r[5],
                                           prov=r[2])
        self.prov = {k[0]: v["prov"] for k, v in tanks.items()}
        self.tank_of = {(k[0], v["product"]): k[1] for k, v in tanks.items()}
        disp_no = {}                      # serial -> (site, dispenser number)
        for r in list(reg["Dispensers"].iter_rows(values_only=True))[1:]:
            disp_no[r[2]] = (r[0], r[1])
        cfg = json.load(open(self.p("forecourt_controller_config_2027-01-05.json")))
        self.fp_disp = {}
        for s in cfg["sites"]:
            for fp in s["fuelling_points"]:
                site, dno = disp_no[fp["dispenser_serial"]]
                assert site == s["site"]
                self.fp_disp[(s["site"], fp["fp"])] = dno
        # point of sale: the latest export of each hose-day
        latest = {}
        for r in rd(self.p("pos_fuel_sales_by_hose_2024_2026.csv")):
            k = (r["site"], r["business_date"], int(r["fp"]), r["grade"])
            if k not in latest or r["exported_at"] > latest[k][0]:
                latest[k] = (r["exported_at"], float(r["volume_l"]))
        days = sorted({k[1] for k in latest})
        self.days = [dt.date.fromisoformat(d) for d in days]
        self.didx = {d: i for i, d in enumerate(self.days)}
        nd = len(self.days)
        hoses = defaultdict(dict)
        for (site, d, fp, g), (_, v) in latest.items():
            key = (site, GRADE_PROD[g])
            if fp not in hoses[key]:
                hoses[key][fp] = np.zeros(nd)
            hoses[key][fp][self.didx[dt.date.fromisoformat(d)]] = v
        self.hoses = hoses
        # gauge closes: reading at 05:00 local on date d closes business day d-1
        self.atg = defaultdict(dict)
        for r in rd(self.p("atg_shift_close_inventory_2024_2026.csv")):
            d = dt.date.fromisoformat(r["read_at"][:10])
            self.atg[(r["site"], ATG_PROD[r["product"]])][d] = float(r["net_volume_l"])
        # receipts on the drop's business day (05:00 to 05:00 on the site's clock)
        self.recv = defaultdict(lambda: np.zeros(nd))
        for r in rd(self.p("bills_of_lading_2024_2026.csv")):
            site = r["consignee"].split()[0]
            if not site.startswith("GB") or not r["delivered_at"]:
                continue
            ts, z = r["delivered_at"].rsplit(" ", 1)
            t = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M")
            bday = (t - TD(hours=5)).date()
            if bday in self.didx:
                self.recv[(site, BOL_PROD[r["product"]])][self.didx[bday]] += float(r["net_l_15c"])
        # resets: calibrations by dispenser, dispenser replacements, meter replacements
        wb = openpyxl.load_workbook(self.p("service_work_orders_2024_2026.xlsx"), data_only=True)
        self.resets = defaultdict(list)            # (site, fp, prod) -> [date]
        self.calib_rows = []
        for r in list(wb["Work orders"].iter_rows(values_only=True))[1:]:
            wo, d, site, con, tech, cat, txt, eq, hrs = r
            site = site.split()[0]
            d = d.date() if isinstance(d, dt.datetime) else d
            fps_site = sorted({fp for (s, fp) in self.fp_disp if s == site})
            if cat == "Meter calibration":
                all_site = sorted({self.fp_disp[(site, fp)] for fp in fps_site})
                if re.search(r"all meters|all disps", txt):
                    disps = all_site
                elif re.search(r"D(\d+)-D(\d+)", txt):
                    m = re.search(r"D(\d+)-D(\d+)", txt)
                    disps = list(range(int(m.group(1)), int(m.group(2)) + 1))
                elif re.search(r"dispensers ([\d, ]+) \(", txt):
                    disps = [int(x) for x in re.search(r"dispensers ([\d, ]+) \(", txt).group(1).split(",")]
                else:
                    disps = [int(re.search(r"- D(\d+),", txt).group(1))]
                self.calib_rows.append((site, d, disps))
                for fp in fps_site:
                    if self.fp_disp[(site, fp)] in disps:
                        for prod in "RPD":
                            self.resets[(site, fp, prod)].append(d)
            elif cat == "Dispenser replacement":
                disp = int(re.search(r"dispenser (\d+)", txt).group(1))
                for fp in fps_site:
                    if self.fp_disp[(site, fp)] == disp:
                        for prod in "RPD":
                            self.resets[(site, fp, prod)].append(d)
            elif cat == "Meter replacement":
                m = re.search(r"FP ?(\d+) (REG 87|PREM 91|DSL)", txt)
                self.resets[(site, int(m.group(1)), GRADE_PROD[m.group(2)])].append(d)
        return self

    def book(self, key):
        site, prod = key
        nd = len(self.days)
        sales = sum(self.hoses[key].values())
        close = np.full(nd + 1, np.nan)
        for d, v in self.atg[key].items():
            i = (d - self.days[0]).days
            if 0 <= i <= nd:
                close[i] = v
        return sales, self.recv[key], close

    def exposure(self, key):
        """per day: sum over hoses of litres sold times litres since the hose's last reset, at the day's start;
        nan where any hose has no recorded reset yet"""
        site, prod = key
        nd = len(self.days)
        Z = np.zeros(nd)
        known = np.ones(nd, bool)
        for fp, v in self.hoses[key].items():
            rs = sorted(self.resets[(site, fp, prod)])
            L = np.full(nd, np.nan)
            cur = np.nan
            ri = 0
            for i, d in enumerate(self.days):
                while ri < len(rs) and rs[ri] <= d:
                    cur = 0.0
                    ri += 1
                L[i] = cur
                if not np.isnan(cur):
                    cur += v[i]
            known &= ~np.isnan(L)
            Z += np.where(np.isnan(L), 0.0, v * L)
        return Z / 2e9, known

    def hours(self, site, q):
        a, b = quarter_days(q)
        h = ((b - a).days + 1) * 24
        if self.prov[site] == "MB":
            if q[1] == 4:
                h += 1           # clocks back on the first Sunday of November
            elif q[1] == 1:
                h -= 1           # forward on the second Sunday of March
        return h

    def tank_quarters(self):
        out = []
        self.sys = {}
        for key in sorted(self.hoses):
            site, prod = key
            sales, recv, close = self.book(key)
            Z, known = self.exposure(key)
            qs = sorted({quarter_of(d) for d in self.days})
            for q in qs:
                a, b = quarter_days(q)
                i0, i1 = self.didx[a], self.didx[b] + 1
                if np.isnan(close[i0]) or np.isnan(close[i1]):
                    continue
                short = close[i0] + recv[i0:i1].sum() - sales[i0:i1].sum() - close[i1]
                ok = bool(known[i0:i1].all())
                out.append(dict(key=key, q=q, short=short, X=Z[i0:i1].sum() if ok else np.nan, S=sales[i0:i1].sum(),
                                hrs=self.hours(site, q), i0=i0, i1=i1))
        self.tq = out
        return out

    def fit_rate(self, rows=None, upto=(2026, 3), first=(2024, 1)):
        rows = rows if rows is not None else [r for r in self.tq if first <= r["q"] <= upto and not np.isnan(r["X"])]
        x = np.array([r["X"] for r in rows])
        y = np.array([r["short"] for r in rows])
        return float(x @ y / (x @ x)), len(rows)

    def main_call(self):
        self.tank_quarters()
        k, n = self.fit_rate()
        res = {}
        for r in self.tq:
            if r["q"] == (2026, 4):
                exp_over = k * r["X"]
                res[r["key"]] = dict(short=r["short"], total_lph=r["short"] / r["hrs"], meters_lph=exp_over / r["hrs"],
                                     loss_lph=(r["short"] - exp_over) / r["hrs"], hrs=r["hrs"], X=r["X"], S=r["S"])
        self.k = k
        self.k_n = n
        self.q4 = res
        self.designated = sorted(kk for kk, v in res.items() if v["loss_lph"] > THRESHOLD)
        return res

    # ------------------------------------------------------------- cardlocks
    def load_cardlocks(self):
        self.cl_bol = [r for r in rd(self.p("bills_of_lading_2024_2026.csv")) if r["consignee"].startswith("CL-")]
        self.cl_rep = rd(self.p("cardlock_gauge_delivery_reports_q4_2026.csv"))
        self.cl_hr = rd(self.p("cardlock_gauge_hourly_inventory_q4_2026.csv"))
        self.cl_tx = rd(self.p("cardlock_transactions_q4_2026.csv"))
        reg = openpyxl.load_workbook(self.p("tpc_site_tank_register.xlsx"), data_only=True)
        self.cl_prov = {}
        for r in list(reg["Tanks"].iter_rows(values_only=True))[1:]:
            if str(r[0]).startswith("CL"):
                self.cl_prov[r[0]] = r[2]
        return self

    def tx_series(self):
        tx = defaultdict(list)
        for r in self.cl_tx:
            prod = "D" if r["product"] == "DIESEL" else "R"
            s = dt.datetime.strptime(r["started_utc"], "%Y-%m-%dT%H:%M:%SZ") - TD(hours=6)
            e = dt.datetime.strptime(r["ended_utc"], "%Y-%m-%dT%H:%M:%SZ") - TD(hours=6)
            tx[(r["site"], prod)].append((s, e, float(r["litres"])))
        return tx

    def drawn(self, tx, key, a, b):
        """litres drawn from the tank by fills that ran inside [a, b] (CST)"""
        return sum(l for (s, e, l) in tx[key] if s >= a and e <= b)

    def cardlock_drops(self):
        tx = self.tx_series()
        hr = defaultdict(dict)
        for r in self.cl_hr:
            prod = "D" if r["product"] == "DIESEL" else "R"
            hr[(r["site"], prod)][dt.datetime.strptime(r["read_cst"], "%Y-%m-%d %H:%M")] = float(r["net_volume_l"])
        self.hr = hr
        bols = []
        for r in self.cl_bol:
            site = r["consignee"].split()[0]
            prod = "D" if r["product"] == "ULS Diesel" else "R"
            bols.append(dict(bol=r["bol_no"], site=site, prod=prod, carrier=r["carrier"], loaded=to_cst(r["loaded_at"]),
                             loaded_day=r["loaded_at"][:10], net=float(r["net_l_15c"])))
        # one row per delivery: the monthly pulls repeat what the console still held
        seen = {}
        for r in self.cl_rep:
            k = (r["site"], r["tank"], int(r["delivery_no"]))
            if k not in seen:
                prod = "D" if r["product"] == "DIESEL" else "R"
                seen[k] = dict(site=r["site"], prod=prod, start=dt.datetime.strptime(r["start_cst"], "%Y-%m-%d %H:%M"),
                               end=dt.datetime.strptime(r["end_cst"], "%Y-%m-%d %H:%M"), inc=float(r["increase_net_l"]))
        reps = sorted(seen.values(), key=lambda x: x["start"])
        q0 = dt.datetime(2026, 10, 1)
        q1 = dt.datetime(2027, 1, 1)
        used = set()
        drops = []
        for rp in reps:
            if not (q0 - TD(days=1) <= rp["start"] < q1 + TD(days=1)):
                continue
            cands = [b for b in bols if b["site"] == rp["site"] and b["prod"] == rp["prod"] and b["loaded"] < rp["start"]
                     and rp["start"] - b["loaded"] < TD(hours=12) and b["bol"] not in used]
            if not cands:
                assert not (q0 <= rp["start"] < q1), rp          # every quarter report has its bill
                continue
            b = max(cands, key=lambda x: x["loaded"])
            used.add(b["bol"])
            dr = self.drawn(tx, (rp["site"], rp["prod"]), rp["start"], rp["end"])
            drops.append(dict(b, when=rp["start"], received=rp["inc"] + dr, drawn=dr, how="report",
                              window=(rp["start"], rp["end"])))
        # bills with no report: the hourly record shows whether and when the product came in
        self.unreported = []
        for b in sorted(bols, key=lambda x: x["loaded"]):
            if b["bol"] in used or not (q0 - TD(hours=12) <= b["loaded"] < q1):
                continue
            key = (b["site"], b["prod"])
            series = hr[key]
            times = sorted(t for t in series if b["loaded"] - TD(hours=1) <= t <= b["loaded"] + TD(hours=16))
            rise = []
            for t0, t1 in zip(times, times[1:]):
                inflow = series[t1] - series[t0] + self.drawn(tx, key, t0, t1)
                if inflow > 500:
                    rise.append((t0, t1))
            if not rise:
                self.unreported.append(dict(b, status="no drop in the quarter's record"))
                continue
            a, z = rise[0][0], rise[0][1]
            for t0, t1 in rise[1:]:
                if t0 == z:
                    z = t1
            dr = self.drawn(tx, key, a, z)
            got = series[z] - series[a] + dr
            used.add(b["bol"])
            assert (a + TD(minutes=1)).month == (z - TD(minutes=1)).month, (b, a, z)      # inside one month
            drops.append(dict(b, when=a + (z - a) / 2, received=got, drawn=dr, how="hourly", window=(a, z)))
            self.unreported.append(dict(b, status="rebuilt from hourly", bracket=(a, z), received=got))
        for d in drops:
            d["short"] = d["net"] - d["received"]
            d["month"] = d["when"].month
        self.all_drops = list(drops)          # every drop the record measures, either side of the quarter's edges
        drops = [d for d in drops if q0 <= d["when"] < q1]
        self.drops = drops
        by_carrier = defaultdict(float)
        by_site = defaultdict(float)
        for d in drops:
            by_carrier[(d["carrier"], d["month"])] += d["short"]
            by_site[(d["site"], d["month"])] += d["short"]
        self.by_carrier = dict(by_carrier)
        self.by_site = dict(by_site)
        return drops


def r10(x):
    return int(np.floor(x / 10.0 + 0.5)) * 10


def run(root):
    pk = Pack(root).load_gasbars()
    pk.main_call()
    pk.load_cardlocks()
    pk.cardlock_drops()
    return pk


def figures(pk):
    names = {"R": "regular", "P": "premium", "D": "diesel"}
    out = dict(designated=["%s %s" % (k[0], names[k[1]]) for k in pk.designated],
               drift_rate_ml_per_20l_per_100k=round(pk.k, 3), drift_fit_tank_quarters=pk.k_n,
               loss_lph={"%s %s" % (k[0], names[k[1]]): round(v["loss_lph"], 1) for k, v in sorted(pk.q4.items())},
               loss_lph_exact={"%s %s" % (k[0], names[k[1]]): round(v["loss_lph"], 4) for k, v in sorted(pk.q4.items())},
               cardlock_short_by_carrier={"%s|%d" % k: r10(v) for k, v in sorted(pk.by_carrier.items())},
               cardlock_short_by_site={"%s|%d" % k: r10(v) for k, v in sorted(pk.by_site.items())},
               cardlock_short_exact_carrier={"%s|%d" % k: round(v, 2) for k, v in sorted(pk.by_carrier.items())},
               cardlock_short_exact_site={"%s|%d" % k: round(v, 2) for k, v in sorted(pk.by_site.items())},
               threshold_lph=THRESHOLD,
               total_lph={"%s %s" % (k[0], names[k[1]]): round(v["total_lph"], 1) for k, v in sorted(pk.q4.items())},
               meters_lph={"%s %s" % (k[0], names[k[1]]): round(v["meters_lph"], 1) for k, v in sorted(pk.q4.items())},
               quarter_hours=sorted({int(v["hrs"]) for v in pk.q4.values()}),
               drift_rate_one_decimal=round(pk.k, 1),
               drift_rate_units=dict(ml_per_draft_of_litres=20, per_litres_passed=100000),
               cardlock_rebuilt_drops=sum(1 for d in pk.drops if d["how"] == "hourly"),
               cardlock_drops=len(pk.drops))
    return out


if __name__ == "__main__":
    import sys
    pk = run(sys.argv[1])
    for k, v in sorted(pk.q4.items(), key=lambda kv: -kv[1]["loss_lph"])[:8]:
        print(k, "total %.3f meters %.3f loss %.3f" % (v["total_lph"], v["meters_lph"], v["loss_lph"]))
    print("k", pk.k, "n", pk.k_n, "designated", pk.designated)
    print("drops", len(pk.drops), "unreported", [(u["bol"], u["site"], u["status"]) for u in pk.unreported])
    for k, v in sorted(pk.by_carrier.items()):
        print(k, round(v, 1))
    for k, v in sorted(pk.by_site.items()):
        print(k, round(v, 1))
