"""Independent verifier: recomputes the call, the 2027 grid and the three annex measures from target/ alone, with its
own parsing and arithmetic (no generator module), and compares them with what the goldens state."""
import csv
import datetime as dt
import math
import os
import re
import sys
import zipfile
from zoneinfo import ZoneInfo

BERLIN = ZoneInfo("Europe/Berlin")
UTC = dt.timezone.utc
AMBER = 120
NAMES = {"MOS": "Moorstetten", "PFB": "Pfeilbrunn", "LZR": "Lanzenried", "WDR": "Wendelsried", "OTM": "Ottenmoos"}


def ts(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def local(t):
    x = dt.datetime.fromtimestamp(t, UTC).astimezone(BERLIN)
    return x.year, (x.month - 1) // 3 + 1, x.hour + x.minute / 60 + x.second / 3600, x.month


def seg_dist(lat, lon, a, b):
    lat0 = (a[0] + b[0]) / 2
    kx, ky = 111.320 * math.cos(math.radians(lat0)), 110.574
    px, py = (lon - a[1]) * kx, (lat - a[0]) * ky
    vx, vy = (b[1] - a[1]) * kx, (b[0] - a[0]) * ky
    t = max(0.0, min(1.0, (px * vx + py * vy) / (vx * vx + vy * vy)))
    return math.hypot(px - t * vx, py - t * vy)


def holes(target):
    out = {}
    with open(os.path.join(target, "well_register.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["function"] == "injection":
                out.setdefault(r["plant"], []).append(((float(r["oh_top_lat"]), float(r["oh_top_lon"])),
                                                       (float(r["oh_bottom_lat"]), float(r["oh_bottom_lon"]))))
    return out


def plant_of(lat, lon, hm):
    for p, segs in hm.items():
        if min(seg_dist(lat, lon, a, b) for a, b in segs) <= 5.0:
            return p
    return None


def call(target):
    hm = holes(target)
    xml = open(os.path.join(target, "station_inventory_2026-10-12.xml"), encoding="utf-8").read()
    switch = ts(re.search(r'<Station code="LZR5" startDate="([^"]+)"', xml).group(1))
    sl = dt.datetime.fromtimestamp(switch, UTC).astimezone(BERLIN)
    lzr_first = dt.datetime(sl.year + (sl.month == 12), sl.month % 12 + 1, 1, tzinfo=BERLIN).timestamp()
    n = {p: 0 for p in NAMES}
    nq = {p: 0 for p in NAMES}
    with open(os.path.join(target, "seismic_catalogue_reviewed_2023-01_2026-09.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["event_type"] != "earthquake" or float(r["ml"]) < 1.0:
                continue
            p = plant_of(float(r["latitude"]), float(r["longitude"]), hm)
            t = ts(r["origin_time_utc"])
            if p is None or (p == "LZR" and t < lzr_first):
                continue
            n[p] += 1
            h = local(t)[2]
            nq[p] += h >= 23.5 or h < 5.0
    months = reported_months(target)
    sw = dt.datetime.fromtimestamp(switch, UTC).astimezone(BERLIN)
    first = (sw.year + (sw.month == 12), sw.month % 12 + 1)
    vol, vrec = {}, {p: 0.0 for p in NAMES}
    for (p, y, m), v in months.items():
        if (y, m) > (2026, 9):
            continue
        vol[(p, y, (m - 1) // 3 + 1)] = vol.get((p, y, (m - 1) // 3 + 1), 0.0) + v
        if p != "LZR" or (y, m) >= first:
            vrec[p] += v
    fc = {}
    for p in NAMES:
        rate = (nq[p] * 24 / 5.5 if p == "PFB" else n[p]) / vrec[p]
        for q in (1, 2, 3, 4):
            fc[(p, q)] = rate * vol[(p, 2026, q) if q < 4 else (p, 2025, 4)]
    return fc


def reported_months(target):
    """(plant, year, month) -> reported injected volume; the 2026 sheet files each report a month late, and December
    2025 appears on both the 2025 and the 2026 sheet."""
    import openpyxl
    op = {"Geowärme Moorstetten GmbH": "MOS", "Stadtwerke Pfeilbrunn": "PFB", "Erdwärme Lanzenried GmbH & Co. KG": "LZR",
          "Wendelsrieder Wärme eG": "WDR", "Ottenmoos Thermal GmbH": "OTM"}
    wb = openpyxl.load_workbook(os.path.join(target, "injection_reports_2023-2026.xlsx"), data_only=True)
    rows = {}
    for ws in wb.worksheets:
        for r in ws.iter_rows(min_row=2, values_only=True):
            if not r[0] or r[3] != "injection":
                continue
            y, m = int(r[0][:4]), int(r[0][5:7])
            if ws.title == "2026":
                y, m = (y - 1, 12) if m == 1 else (y, m - 1)
            rows[(r[2], y, m)] = (op[r[1]], r[4])
    out = {}
    for (_, y, m), (p, vv) in rows.items():
        out[(p, y, m)] = out.get((p, y, m), 0) + vv
    return out


def memo_table(golden):
    with zipfile.ZipFile(os.path.join(golden, "amber_outlook_2027.docx")) as z:
        x = z.read("word/document.xml").decode("utf-8")
    tables = re.findall(r"<w:tbl>.*?</w:tbl>", x, re.S)
    rows = re.findall(r"<w:tr[ >].*?</w:tr>", tables[1], re.S)
    out = {}
    for r in rows[1:]:
        cells = ["".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", c)) for c in re.findall(r"<w:tc>.*?</w:tc>", r, re.S)]
        code = {v: k for k, v in NAMES.items()}[cells[0]]
        for q in (1, 2, 3, 4):
            out[(code, q)] = int(cells[q])
    return out, x


def annex(golden):
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(golden, "tls_annex_2026.xlsx"), data_only=True)["Annex 2026"]
    out = {}
    code = {v: k for k, v in NAMES.items()}
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0]:
            out[(code[r[0]], int(r[1][1]))] = (r[2], r[3], r[4])
    return out


def volumes(target):
    import openpyxl
    op = {"Geowärme Moorstetten GmbH": "MOS", "Stadtwerke Pfeilbrunn": "PFB", "Erdwärme Lanzenried GmbH & Co. KG": "LZR",
          "Wendelsrieder Wärme eG": "WDR", "Ottenmoos Thermal GmbH": "OTM"}
    ws = openpyxl.load_workbook(os.path.join(target, "injection_reports_2023-2026.xlsx"), data_only=True)["2026"]
    out = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[3] != "injection":
            continue
        y, m = int(r[0][:4]), int(r[0][5:7]) - 1                  # filed under the month after the month it reports
        if m == 0:
            y, m = y - 1, 12
        if y == 2026:
            k = (op[r[1]], (m - 1) // 3 + 1)
            out[k] = out.get(k, 0) + r[4]
    return {k: int(math.floor(v / 100 + 0.5)) * 100 for k, v in out.items()}


def automatic(target):
    hm = holes(target)
    rows = []
    with open(os.path.join(target, "origins_2023-01_2026-09.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["author"] == "scautoloc@lgrt1":
                rows.append((ts(r["origin_time_utc"]), ts(r["creation_time_utc"]), float(r["latitude"]),
                             float(r["longitude"]), float(r["ml"])))
    rows.sort()
    events, last = [], []
    for o in rows:
        hit = None
        for i in range(len(last) - 1, max(-1, len(last) - 6), -1):
            t0, la, lo = last[i]
            if o[0] - t0 <= 3.0 and math.hypot((o[3] - lo) * 74.6, (o[2] - la) * 110.6) <= 8.0:
                hit = i
                break
        if hit is None:
            events.append([o])
            last.append((o[0], o[2], o[3]))
        else:
            events[hit].append(o)
            last[hit] = (o[0], o[2], o[3])
    out = {}
    for e in events:
        f = max(e, key=lambda o: o[1])
        if f[4] < 1.0:
            continue
        p = plant_of(f[2], f[3], hm)
        y, q, _, _ = local(f[0])
        if p and y == 2026:
            out[(p, q)] = out.get((p, q), 0) + 1
    return out


def hours(target):
    import json
    reg = json.load(open(os.path.join(target, "plant_register.json"), encoding="utf-8"))
    xml = open(os.path.join(target, "station_inventory_2026-10-12.xml"), encoding="utf-8").read()
    ep = {}
    for sta, body in re.findall(r'<Station code="(\w+)".*?>(.*?)</Station>', xml, re.S):
        for a, b in re.findall(r'<Channel code="HHZ" locationCode="\d\d" startDate="([^"]+)"(?: endDate="([^"]+)")?>', body):
            ep.setdefault(sta, []).append((ts(a), ts(b) if b else None))
    gaps = {}
    with open(os.path.join(target, "availability_gaps_2026-01_2026-09.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["cha"] == "HHZ":
                gaps.setdefault(r["sta"], []).append((ts(r["gap_start"]), ts(r["gap_end"])))
    out = {}
    for p in reg["plants"]:
        for q in (1, 2, 3):
            a = dt.datetime(2026, 3 * q - 2, 1, tzinfo=BERLIN).timestamp()
            b = dt.datetime(2026, 3 * q + 1, 1, tzinfo=BERLIN).timestamp()
            pts = {a, b}
            for sta in p["monitoring_network"]:
                for s, e in ep[sta]:
                    pts.update(x for x in (s, e) if x and a < x < b)
                pts.update(x for g in gaps.get(sta, []) for x in g if a < x < b)
            pts = sorted(pts)
            under = 0.0
            for x0, x1 in zip(pts, pts[1:]):
                mid = (x0 + x1) / 2
                up = sum(1 for sta in p["monitoring_network"]
                         if any(s <= mid < (e or 9e12) for s, e in ep[sta])
                         and not any(g0 <= mid < g1 for g0, g1 in gaps.get(sta, [])))
                if up < 4:
                    under += x1 - x0
            out[(p["plant"], q)] = math.floor(under / 3600 * 10 + 0.5) / 10
    return out


def main(target, golden):
    fc = call(target)
    over = sorted(k for k, v in fc.items() if v > AMBER)
    assert over == [("PFB", 1), ("PFB", 4)], over
    tab, xml = memo_table(golden)
    for k, v in fc.items():
        assert tab[k] == int(math.floor(v + 0.5)), (k, v, tab[k])
    assert "Pfeilbrunn will run over amber in the first and fourth quarters of 2027" in xml
    ann = annex(golden)
    vol, aut, hrs = volumes(target), automatic(target), hours(target)
    for p in NAMES:
        for q in (1, 2, 3):
            got = ann[(p, q)]
            assert got[0] == vol[(p, q)], ("volume", p, q, got[0], vol[(p, q)])
            assert got[1] == aut.get((p, q), 0), ("automatic", p, q, got[1], aut.get((p, q)))
            assert abs(got[2] - hrs[(p, q)]) < 1e-9, ("hours", p, q, got[2], hrs[(p, q)])
    print("verify: OK (call %s; 20 forecast cells and 45 annex figures recomputed independently)" %
          ", ".join("%s Q%d" % k for k in over))


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(task, "target"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(task, "golden"))
