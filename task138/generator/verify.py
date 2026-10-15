"""Independent verifier for task138. Reads only the shipped bundle (target/ and golden/), shares no code with the
generator (no calc.py, no numpy), and recomputes the efficiency the soil moisture stations' 2026 readings show for each
irrigation method (its own fit: a grid, then a parabola through the best three points), the order and the replay that
sets it, the default path (the 2026 record run at the Table 4 efficiency) and the four lateral asks; the golden workbook
is used only as the expectations.

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
        # each field's 2026 orders: the delivered sets' water by day (the ordered flow for the hours it ran that day)
        # and the last delivered set's day
        self.last = {}
        self.water = {}
        for r in rows(find(target, "kbid_irrigation_orders", ".csv")):
            if r["season"] != "2026" or r["status"] != "Delivered":
                continue
            a = dt.datetime.strptime(r["set_start"], "%Y-%m-%d %H:%M")
            b = dt.datetime.strptime(r["set_end"], "%Y-%m-%d %H:%M")
            q = float(r["ordered_cfs"])
            t = a
            while t < b:
                nxt = min(b, dt.datetime(t.year, t.month, t.day) + dt.timedelta(days=1))
                key = (r["field_id"], t.date())
                self.water[key] = self.water.get(key, 0.0) + q * (nxt - t).total_seconds() / 43560.0
                t = nxt
            if r["field_id"] not in self.last or b.date() > self.last[r["field_id"]]:
                self.last[r["field_id"]] = b.date()
        # the soil moisture network: each station's field through its parcel number, its full point, and each reading
        # by the local day it ends (a reading at local midnight ends the day before; the platform stamps UTC)
        from zoneinfo import ZoneInfo
        net = find(target, "kbid_soil_moisture_network", ".xlsx")
        head, body = after_header(sheet(net, "Sites"), "Station")
        col = {h: k for k, h in enumerate(head)}
        by_apn = {r["apn"].replace("-", ""): r["field_id"] for r in rows(find(target, "kbid_field_register", ".csv"))}
        byid = {f["id"]: f for f in self.fields}
        self.stations = {}
        for r in body:
            self.stations[r[col["Station"]]] = dict(field=byid[by_apn[str(r[col["APN"]])]], method=r[col["Irrigation"]],
                                                     full=float(r[col["Full point (in)"]]), reads={})
        tz = ZoneInfo("America/Los_Angeles")
        for r in sheet(net, "Daily")[1:]:
            if not r or r[0] is None:
                continue
            t = dt.datetime.strptime(r[1], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc).astimezone(tz)
            self.stations[r[0]]["reads"][t.date() - dt.timedelta(days=1)] = float(r[2])

    def run_2026(self, f, ea):
        """The 2026 season from field capacity at the end of 27 January 2026 (the winter's rains had every root zone
        full, see winter_full) to the end of 31 January 2027, each day's delivered water at the share ea reaching the
        root zone: {day: depletion at its end}."""
        D, out = 0.0, {}
        for d in days(dt.date(2026, 1, 28), dt.date(2027, 1, 31)):
            e, rain = self.wx[d]
            w = self.water.get((f["id"], d), 0.0) * 12.0 / f["acres"] * ea
            D = min(f["taw"], max(0.0, D + self.kc[f["crop"]][d.month - 1] * e - rain - w))
            out[d] = D
        return out

    def depletion_31jan(self, f, ea=None):
        return self.run_2026(f, self.ea[f["method"]] if ea is None else ea)[dt.date(2027, 1, 31)]

    def fit(self, st):
        """The share of the record's water that brings the station's field's run onto its readings (least squares):
        every ten-thousandth from 0.60 to 1.00 (the misfit's floor can be flat and bumpy on a small root zone), then
        grids ten times finer around the best point until the step is under a ten-millionth."""
        def misfit(ea):
            run = self.run_2026(st["field"], ea)
            return sum((st["full"] - v - run[d]) ** 2 for d, v in st["reads"].items() if d in run)
        lo, step, n = 0.60, 0.0001, 4001
        while True:
            grid = [lo + step * k for k in range(n)]
            vals = [misfit(x) for x in grid]
            k = min(range(len(grid)), key=lambda j: vals[j])
            if step < 1e-7:
                return grid[k]
            lo, step, n = grid[k] - step, step / 10.0, 21

    def station_efficiency(self):
        per = {s: self.fit(st) for s, st in self.stations.items() if st["method"] != "Border"}
        by = {}
        for m in ("Drip", "Micro-sprinkler", "Sprinkler"):
            v = [per[s] for s, st in self.stations.items() if st["method"] == m]
            by[m] = sum(v) / len(v)
        return per, by

    def winter_full(self, f):
        """The field's root zone at the end of 27 January 2026 from 1 November 2025, starting empty (at its total
        available water) and full: both zero if the winter's rains filled it."""
        out = []
        for D in (f["taw"], 0.0):
            for d in days(dt.date(2025, 11, 1), dt.date(2026, 1, 27)):
                e, rain = self.wx[d]
                D = min(f["taw"], max(0.0, D + self.kc[f["crop"]][d.month - 1] * e - rain))
            out.append(D)
        return max(out)

    def depletion_from_last_set(self, f):
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
        reqs = {}
        for y in range(1997, 2027):
            reqs[y] = sum(self.replay(y, start).values())
        ranked = sorted(reqs.items(), key=lambda kv: kv[1])
        y24, v24 = ranked[23]
        order = int(math.ceil(v24 / 1000.0 - 1e-12) * 1000)
        return dict(order=order, year=y24, req=v24, ranked=ranked, reqs=reqs)


def asks(target):
    import re
    import docx
    meters = {}
    ms = find(target, "kbid_meter_shop_log", ".xlsx")
    head, body = after_header(sheet(ms, "Meter inventory"), "Meter")
    for r in body:
        meters[r[0]] = (r[3] == "acre-feet", float(str(r[4]).replace(",", "")))
    head, body = after_header(sheet(ms, "Work orders 2026"), "WO no.")
    col = {h: k for k, h in enumerate(head)}
    change = {}
    for r in body:
        if r[col["Meter out"]]:
            change[(r[col["Meter out"]], r[col["Meter in"]])] = (float(r[col["Reg. out"]]), float(r[col["Reg. in"]]))
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
                isaf, cap = meters[s0]
                vol = (v1 - v0) % cap
                vol = vol if isaf else vol / 435.6
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
    log = docx.Document(find(target, "kbid_canal_operations_log", ".docx")).tables[0]
    month_names = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
    for row in log.rows[1:]:
        text = row.cells[2].text
        if "estimat" not in text.lower():
            continue
        lat = re.search(r"\b(?:Lateral|Lat|L) ?([1-9])\b", text)
        words = re.findall(r"[A-Za-z]+|\d+/\d+|\d+\.\d+|\d+", text)
        seen = set()
        for k in range(len(words) - 2):
            a, b, c = words[k], words[k + 1], words[k + 2]
            if not re.fullmatch(r"\d+\.\d", c):
                continue
            key = None
            if a.isdigit() and b[:3].lower() in month_names:
                key = (b[:3].lower(), int(a))
            elif a[:3].lower() in month_names and b.isdigit():
                key = (a[:3].lower(), int(b))
            elif re.fullmatch(r"\d+/\d+", b):
                key = ("slash", b)
            if key is not None and key not in seen:
                seen.add(key)
                inflow["L" + lat.group(1)] += float(c)
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
                words = rem.lower().split()
                if words[:1] in (["set"], ["added"]) and "brd" in words:
                    boards += 1
                elif words[:2] == ["pulled", "1"]:
                    boards -= 1
                elif words[:2] == ["brds", "out"]:
                    boards = 0
                cur = (g, boards)
            g, b = cur
            h = g - crest - b * (2.0 / 12.0)
            if h > 0:
                tot += c * L * h ** 1.5 * 86400.0 / 43560.0
        spill[l] = tot
    return deliv, inflow, share, spill


def main(target, golden):
    P = Pack(target)
    assert all(P.winter_full(f) == 0.0 for f in P.fields), "a root zone short of field capacity on 27 January 2026"
    per, by = P.station_efficiency()
    assert all(v > P.ea[P.stations[s]["method"]] + 0.02 for s, v in per.items()), ("a station at Table 4", per)
    # every station's 31 January reading is the same under Table 4 and under its own efficiency
    for s, st in P.stations.items():
        a = P.depletion_31jan(st["field"])
        b = P.depletion_31jan(st["field"], per.get(s, P.ea[st["method"]]))
        assert abs(a - b) < 1e-9 and abs(st["full"] - st["reads"][dt.date(2027, 1, 31)] - a) < 0.15, s
    starts = {f["id"]: P.depletion_31jan(f, by.get(f["method"], P.ea[f["method"]])) for f in P.fields}
    gold = P.order(starts)
    default = P.order({f["id"]: P.depletion_31jan(f) for f in P.fields})
    deliv, inflow, share, spill = asks(target)
    # expectations from the golden workbook
    book = os.path.join(golden, "kbid_order_2027.xlsx")
    o = sheet(book, "Order 2027")
    lab = {r[0]: r[1] for r in o if r and r[0]}
    assert lab["2027 order (acre-feet)"] == gold["order"], (lab["2027 order (acre-feet)"], gold["order"])
    assert lab["Replay that sets the order"] == gold["year"]
    head, body = after_header(sheet(book, "Replays"), "Weather year")
    for r in body:
        v = gold["reqs"][r[0]]
        # equal at the workbook's rounding, unless the recomputed value sits within half an acre-foot of a rounding line
        assert r[1] == half_up(v, 10) or abs((v % 10) - 5) < 0.5, (r[0], r[1], v)
    lt = sheet(book, "Laterals 2026")
    head, body = after_header(lt, "Lateral")
    for r in body:
        if r[0] == "Nine laterals":
            tin, tdl = sum(inflow.values()), sum(deliv.values())
            assert r[1] == half_up(tdl, 10) and r[2] == half_up(tin, 10), ("total row", r[1], r[2])
            assert abs(r[3] - half_up(1000.0 * (tin - tdl) / tin, 1) / 10.0) < 1e-9, ("total share", r[3])
            assert r[4] == half_up(sum(spill.values()), 10), ("total spill", r[4])
            continue
        l = "L" + r[0].split()[-1]
        assert r[1] == half_up(deliv[l], 10), (l, r[1], deliv[l])
        assert r[2] == half_up(inflow[l], 10), (l, r[2], inflow[l])
        assert abs(r[3] - half_up(share[l] * 10, 1) / 10.0) < 1e-9, (l, r[3], share[l])
        assert r[4] == half_up(spill[l], 10), (l, r[4], spill[l])
    assert default["order"] != gold["order"], "the default path files the golden"
    assert default["order"] - gold["order"] >= 3000, (gold["order"], default["order"])
    assert 400 <= gold["req"] - (gold["order"] - 1000) <= 600, gold["req"]
    gap = P.closest_approach(starts)
    assert gap > 1e-7, gap
    print("verify.py: the stations' efficiency %s; order %s AF set by %d (24th %.1f AF); default path (the 2026 record "
          "at Table 4) %s AF set by %d; closest approach to an allowable depletion %.1e in; the four lateral asks "
          "recomputed on 9 laterals each; all match the golden" % (
              {k: round(v, 4) for k, v in by.items()}, "{:,}".format(gold["order"]), gold["year"], gold["req"],
              "{:,}".format(default["order"]), default["year"], gap))
    return gold, default


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "target")
    g = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "golden")
    main(t, g)
