"""Independent verifier for task138. Reads only the shipped bundle (target/ and golden/), shares no code with the
generator (no calc.py, no numpy), and recomputes the order, its schedule, the replay that sets it, the default path,
and both asks; the golden workbook is used only as the expectations.

    python3 task138/generator/verify.py [target] [golden]"""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import sys

import openpyxl

LATS = ["L%d" % k for k in range(1, 10)]


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def raw_rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.reader(fh))


def sheet(path, name):
    return [list(r) for r in openpyxl.load_workbook(path, data_only=True)[name].iter_rows(values_only=True)]


def after_header(table, first):
    k = next(i for i, r in enumerate(table) if r and r[0] == first)
    return table[k], [r for r in table[k + 1:] if r and r[0] is not None]


def days(a, b):
    d = a
    while d <= b:
        yield d
        d += dt.timedelta(days=1)


def half_up(x, step):
    return int(math.floor(x / step + 0.5)) * step


def find(target, prefix, ext):
    return next(os.path.join(target, f) for f in sorted(os.listdir(target)) if f.startswith(prefix) and f.endswith(ext))


class Pack:
    def __init__(self, target):
        self.t = target
        tables = find(target, "KBID_WOP_tables", ".xlsx")
        _, t1 = after_header(sheet(tables, "T1 Crop coefficients"), "Code")
        self.kc = {r[0]: [float(x) for x in r[2:14]] for r in t1}
        _, t2 = after_header(sheet(tables, "T2 Crops"), "Code")
        self.root = {r[0]: float(r[2]) for r in t2}
        self.mad = {r[0]: float(r[3]) for r in t2}
        _, t3 = after_header(sheet(tables, "T3 Soil units"), "Map unit")
        self.soil = {str(r[0]): (float(r[2]), None if str(r[3]).lower() == "none" else float(r[3])) for r in t3}
        _, t4 = after_header(sheet(tables, "T4 Application efficiency"), "Irrigation method")
        self.ea = {r[0]: float(r[1]) for r in t4}
        _, t5 = after_header(sheet(tables, "T5 Loss allowances"), "Conveyance")
        self.allow = {}
        for r in t5:
            if r[0].startswith("Lateral"):
                self.allow["L" + r[0].split()[1]] = float(r[1]) / 100.0
            else:
                self.main = float(r[1]) / 100.0
        # weather, spliced as WOP 6.1 says
        s39 = {}
        rr = raw_rows(find(target, "station39", ".csv"))
        h = rr[0]
        for r in rr[1:]:
            m, d, y = map(int, r[h.index("Date")].split("/"))
            s39[dt.date(y, m, d)] = (float(r[h.index("ETo (mm)")]) / 25.4, float(r[h.index("Precip (mm)")]) / 25.4)
        yard = {}
        for r in rows(find(target, "kbid_station_daily", ".csv")):
            if r["ETo_in"] and r["Rain_in"]:
                yard[dt.date.fromisoformat(r["Date"])] = (float(r["ETo_in"]), float(r["Rain_in"]))
        self.wx = {}
        for d in days(min(s39), dt.date(2027, 1, 31)):
            self.wx[d] = yard[d] if d >= dt.date(2014, 5, 1) and d in yard else s39[d]
        # the 2027 fields: latest accepted request, the register's lateral and soil unit
        req = find(target, "kbid_water_requests", ".xlsx")
        head, body = after_header(sheet(req, "Requests"), "Request no.")
        reg = {r["field_id"]: r for r in rows(find(target, "kbid_field_register", ".csv"))}
        self.fields = []
        for r in body:
            q = dict(zip(head, r))
            if q["Status"] != "Accepted":
                continue
            g = reg[q["Field"]]
            self.fields.append(dict(id=q["Field"], crop=q["Crop code"], method=q["Irrigation method"],
                                    acres=float(q["Acres"]), lat="L" + g["lateral"].split()[-1], soil=g["soil_unit"]))
        for f in self.fields:
            awc, lim = self.soil[f["soil"]]
            depth = self.root[f["crop"]] if lim is None else min(self.root[f["crop"]], lim)
            f["taw"] = awc * depth
            f["raw"] = self.mad[f["crop"]] * f["taw"]
        # each field's last delivered set in 2026
        self.last = {}
        for r in rows(find(target, "kbid_irrigation_orders", ".csv")):
            if r["season"] == "2026" and r["status"] == "Delivered":
                d = dt.date.fromisoformat(r["set_end"][:10])
                if r["field_id"] not in self.last or d > self.last[r["field_id"]]:
                    self.last[r["field_id"]] = d

    def depletion_31jan(self, f):
        D = 0.0
        for d in days(self.last[f["id"]] + dt.timedelta(days=1), dt.date(2027, 1, 31)):
            e, rain = self.wx[d]
            D = min(f["taw"], max(0.0, D + self.kc[f["crop"]][d.month - 1] * e - rain))
        return D

    def replay(self, year, start):
        """Headgate requirement by month (February to October) for the 2027 fields under year's weather."""
        farm = {(l, m): 0.0 for l in LATS for m in range(2, 11)}
        for f in self.fields:
            D = start[f["id"]]
            kc = self.kc[f["crop"]]
            for d in days(dt.date(year, 2, 1), dt.date(year, 10, 31)):
                e, rain = self.wx[d]
                D = min(f["taw"], max(0.0, D + kc[d.month - 1] * e - rain))
                if D >= f["raw"]:
                    farm[(f["lat"], d.month)] += D / self.ea[f["method"]] * f["acres"] / 12.0
                    D = 0.0
        month = {}
        for m in range(2, 11):
            month[m] = sum(farm[(l, m)] / (1 - self.allow[l]) for l in LATS) / (1 - self.main)
        return month

    def closest_approach(self, start):
        """The smallest distance, over every day of every replay, between a field's depletion and its allowable
        depletion (the irrigation test of WOP 3.4 is never decided by a hair)."""
        gap = float("inf")
        for f in self.fields:
            kc, taw, raw = self.kc[f["crop"]], f["taw"], f["raw"]
            for year in range(1997, 2027):
                D = start[f["id"]]
                for d in days(dt.date(year, 2, 1), dt.date(year, 10, 31)):
                    e, rain = self.wx[d]
                    D = min(taw, max(0.0, D + kc[d.month - 1] * e - rain))
                    gap = min(gap, abs(D - raw))
                    if D >= raw:
                        D = 0.0
        return gap

    def order(self, start):
        reqs, months = {}, {}
        for y in range(1997, 2027):
            mo = self.replay(y, start)
            months[y] = mo
            reqs[y] = sum(mo.values())
        ranked = sorted(reqs.items(), key=lambda kv: kv[1])
        y24, v24 = ranked[23]
        order = int(math.ceil(v24 / 100.0 - 1e-12) * 100)
        tot = {m: sum(months[y][m] for y in reqs) for m in range(2, 11)}
        grand = sum(tot.values())
        sched = [half_up(order * tot[m] / grand, 10) for m in range(2, 10)]
        sched.append(order - sum(sched))
        return dict(order=order, year=y24, req=v24, schedule=sched, ranked=ranked)


def asks(target):
    meters = {}
    ms = find(target, "kbid_meter_shop_log", ".xlsx")
    head, body = after_header(sheet(ms, "Meters in service"), "Meter")
    for r in body:
        meters[r[0]] = (r[3] == "acre-feet", float(str(r[4]).replace(",", "")))
    head, body = after_header(sheet(ms, "2026 changes"), "Date")
    change = {}
    for r in body:
        change[(r[3], r[5])] = (float(r[4]), float(r[6]))
    reg = {}
    for r in rows(find(target, "kbid_field_register", ".csv")):
        t = r["turnout_id"]
        reg["%d-%d" % (int(t[1:3]), int(t[3:6]))] = "L" + r["lateral"].split()[-1]
    book = {}
    for r in rows(find(target, "kbid_meter_book", ".csv")):
        m, d, y = map(int, r["read_date"].split("/"))
        hh, mm = map(int, r["read_time"].split(":"))
        book.setdefault(r["turnout"], []).append((dt.datetime(y, m, d, hh, mm), r["meter"], float(r["reading"])))
    deliv = {l: 0.0 for l in LATS}
    for tid, rd in book.items():
        rd.sort()
        built = "L%d" % int(tid.split("-")[0])
        for (t0, s0, v0), (t1, s1, v1) in zip(rd, rd[1:]):
            if s0 == s1:
                af, cap = meters[s0]
                vol = (v1 - v0) % cap
                vol = vol if af else vol / 435.6
            else:
                rem, ins = change[(s0, s1)]
                af0, cap0 = meters[s0]
                af1, cap1 = meters[s1]
                a = (rem - v0) % cap0
                b = (v1 - ins) % cap1
                vol = (a if af0 else a / 435.6) + (b if af1 else b / 435.6)
            lat = reg[tid]
            if built != lat and t1.date() <= dt.date(2026, 6, 15):
                lat = built
            deliv[lat] += vol
    inflow = {l: 0.0 for l in LATS}
    for r in rows(find(target, "kbid_lateral_headings", ".csv")):
        inflow["L" + r["lateral"].split()[-1]] += float(r["volume_af"])
    share = {l: 100 * (inflow[l] - deliv[l]) / inflow[l] for l in LATS}
    st = find(target, "kbid_canal_structures", ".xlsx")
    head, body = after_header(sheet(st, "Tail weirs"), "Lateral")
    weir = {"L" + r[0].split()[-1]: (float(r[2]), float(r[3]), float(r[4])) for r in body}
    sheets = {}
    for r in rows(find(target, "kbid_tail_weir_sheets", ".csv")):
        m, d, y = map(int, r["sheet_date"].split("/"))
        sheets.setdefault("L" + r["lateral"].split()[-1], {})[dt.date(y, m, d)] = (float(r["gauge_ft"]), r["remarks"])
    spill = {}
    for l in LATS:
        L, crest, c = weir[l]
        boards, cur, tot = 0, None, 0.0
        for d in days(dt.date(2026, 2, 1), dt.date(2026, 10, 31)):
            if d in sheets[l]:
                g, rem = sheets[l][d]
                rem = rem.lower().strip()
                if rem[:5].count(":") == 1 and rem[:2].isdigit():
                    rem = rem[5:].strip()
                if rem == "pulled boards":
                    boards = 0
                elif rem.startswith("pulled") and rem.endswith("board"):
                    boards -= 1
                elif "2-inch board" in rem:
                    boards += 1
                cur = (g, boards)
            g, b = cur
            h = g - crest - b * (2.0 / 12.0)
            if h > 0:
                tot += c * L * h ** 1.5 * 86400.0 / 43560.0
        spill[l] = tot
    return deliv, share, spill


def main(target, golden):
    P = Pack(target)
    starts = {f["id"]: P.depletion_31jan(f) for f in P.fields}
    gold = P.order(starts)
    full = P.order({f["id"]: 0.0 for f in P.fields})
    deliv, share, spill = asks(target)
    # expectations from the golden workbook
    book = os.path.join(golden, "kbid_order_2027.xlsx")
    o = sheet(book, "Order 2027")
    lab = {r[0]: r[1] for r in o if r and r[0]}
    assert lab["2027 order (acre-feet)"] == gold["order"], (lab["2027 order (acre-feet)"], gold["order"])
    assert lab["Weather year whose replay sets the order"] == gold["year"]
    assert lab["Headgate requirement in that replay (acre-feet)"] == half_up(gold["req"], 10)
    months = [lab[m] for m in ("February", "March", "April", "May", "June", "July", "August", "September", "October")]
    assert months == gold["schedule"], (months, gold["schedule"])
    lt = sheet(book, "Laterals 2026")
    head, body = after_header(lt, "Lateral")
    for r in body:
        l = "L" + r[0].split()[-1]
        assert r[2] == half_up(deliv[l], 10), (l, r[2], deliv[l])
        assert abs(r[3] - half_up(share[l], 0.1)) < 1e-9, (l, r[3], share[l])
        assert r[4] == half_up(spill[l], 10), (l, r[4], spill[l])
    assert full["order"] != gold["order"] and full["year"] != gold["year"]
    gap = P.closest_approach(starts)
    assert gap > 1e-7, gap
    print("verify.py: order %s AF set by %d (%s AF), schedule %s; default path (full on 1 February) %s AF set by %d; "
          "closest approach to an allowable depletion %.1e in; Ask A and Ask B recomputed on 9 laterals each; all match the "
          "golden" % (
              "{:,}".format(gold["order"]), gold["year"], "{:,}".format(half_up(gold["req"], 10)), gold["schedule"],
              "{:,}".format(full["order"]), full["year"], gap))
    return gold, full


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "golden")
    main(t, g)
