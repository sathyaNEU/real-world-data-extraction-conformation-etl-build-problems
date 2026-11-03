"""The independent verifier: reads only the bundle, on its own code path (zoneinfo for the clock, pypdf for the PDFs, a
fresh replay), and recomputes every graded figure, then checks figures.json and submission.md against it."""
import bisect
import csv
import datetime as dt
import json
import os
import re
import zipfile
from zoneinfo import ZoneInfo

from openpyxl import load_workbook
from pypdf import PdfReader

LON, UTC = ZoneInfo("Europe/London"), ZoneInfo("UTC")


def text_pdf(p):
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in PdfReader(p).pages))


def text_docx(p):
    with zipfile.ZipFile(p) as z:
        x = z.read("word/document.xml").decode("utf-8")
    return re.findall(r"<w:tc>.*?</w:tc>", x, flags=re.S), re.sub(r"<[^>]+>", " ", x)


def days_of(target):
    wb = load_workbook(os.path.join(target, "schools/term_dates_2025_26.xlsx"), read_only=True)
    bh = {r[0].date() for r in wb["Bank holidays"].iter_rows(min_row=2, values_only=True) if r and r[0]}
    out = {}
    for county in ("Northshire", "Southshire", "Eastshire", "Westshire"):
        s = set()
        for r in wb[county].iter_rows(values_only=True):
            if r and len(r) >= 5 and isinstance(r[1], dt.datetime):
                a, hs, he, b = (x.date() for x in r[1:5])
                for i in range((b - a).days + 1):
                    d = a + dt.timedelta(days=i)
                    if d.weekday() < 5 and not hs <= d <= he and d not in bh:
                        s.add(d)
        out[county] = s
    return out


def closures_of(target):
    rows = {}
    with open(os.path.join(target, "rail/barrier_events_2025_26.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            t = dt.datetime.fromisoformat(r["event_time_utc"].replace("Z", "+00:00")).astimezone(LON)
            rows.setdefault(r["lx_ref"], []).append((t, r["event_type"]))
    out = {}
    for code, ev in rows.items():
        ev.sort()
        state, down, by = "up", None, {}
        for t, e in ev:
            if e == "LOWERED" and state == "up":
                state, down = "down", t
            elif e == "RAISED" and state == "down":
                state = "up"
                mid = down.replace(hour=0, minute=0, second=0, microsecond=0)
                by.setdefault(down.date(), []).append(((down - mid).total_seconds(), (t - mid).total_seconds()))
        out[code] = by
    return out


def replay(arr, cl, h, gate=None):
    """gate: (kind, N, off, cyc, g0, g1, hb) with kind 'down' (barrier then stop line) or 'up' (stop line then barrier)"""
    starts = [c[0] for c in cl]

    def bar(t):
        i = bisect.bisect_right(starts, t) - 1
        return cl[i][1] if i >= 0 and cl[i][0] <= t < cl[i][1] else t

    def grn(s, off, cyc, g0, g1):
        ph = (s - off) % cyc
        return s if g0 <= ph < g1 else s + (g0 - ph) % cyc
    if gate is None:
        out, last = [], -1e18
        for a in arr:
            t = bar(max(a, last + h))
            out.append(t)
            last = t
        return out
    kind, N, off, cyc, g0, g1, hb = gate
    first, second, l1, l2 = [], [], -1e18, -1e18
    for i, a in enumerate(arr):
        if kind == "down":
            t = max(a, l1 + h)
            while True:
                t1 = bar(max(t, second[i - N] if i >= N else t))
                if t1 == t:
                    break
                t = t1
            first.append(t)
            l1 = t
            s = grn(max(t, l2 + hb), off, cyc, g0, g1)
            second.append(s)
            l2 = s
        else:
            s = max(a, l1 + hb)
            while True:
                s1 = grn(max(s, second[i - N] if i >= N else s), off, cyc, g0, g1)
                if s1 == s:
                    break
                s = s1
            first.append(s)
            l1 = s
            t = bar(max(s, l2 + h))
            second.append(t)
            l2 = t
    return second


def main(target, golden, figures_path, submission_path):
    F = json.load(open(figures_path))
    sub = open(submission_path).read()
    method = text_pdf(os.path.join(target, "programme/road_delay_appraisal_conventions.pdf"))
    sat = int(re.search(r"at ([\d,]+) vehicles an hour", method).group(1).replace(",", ""))
    vlen = float(re.search(r"occupies ([\d.]+) metres", method).group(1))
    reg_text = text_pdf(os.path.join(target, "rail/crossing_register_2025.pdf"))
    cells, brief = text_docx(os.path.join(target, "programme/crossing_programme_2027.docx"))
    short = [re.sub(r"<[^>]+>", "", c).strip() for c in cells][3::3]
    reg = {}
    for m in re.finditer(r"([A-Z]{3}) (\d+)m (\d\d)ch ([A-Z][a-z]+(?: [A-Z][a-z]+)*) \S+ (\w+shire) (\d{6}) (\d{6}) (LXB/\d+)",
                         reg_text):
        reg[m.group(4)] = dict(code="%s %03d.%s" % (m.group(1), int(m.group(2)), m.group(3)), county=m.group(5),
                               grid=(int(m.group(6)), int(m.group(7))), asset=m.group(8))
    assert sorted(short) == sorted(n for n in short if n in reg) and len(short) == 6, short
    sdays = days_of(target)
    cl = closures_of(target)
    counts = {}
    with open(os.path.join(target, "highways/approach_counts_2025_26.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            counts.setdefault((r["site_ref"], r["count_date"]), {})[r["interval_start"]] = (int(r["veh_total"]), int(r["veh_hgv"]))
    nodes = {}
    with open(os.path.join(target, "highways/network_nodes.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            nodes[int(r["node_ref"])] = (int(r["easting"]), int(r["northing"]))
    links = []
    with open(os.path.join(target, "highways/network_links.csv"), newline="") as fh:
        links = list(csv.DictReader(fh))
    wb = load_workbook(os.path.join(target, "highways/network_register_2026.xlsx"), read_only=True)
    sites = [r for r in wb["Count sites"].iter_rows(min_row=2, values_only=True) if r and r[0]]
    sig = {int(r[1]): r for r in wb["Signal sites"].iter_rows(min_row=2, values_only=True) if r and r[0]}
    got = {}
    for n in short:
        x, y = reg[n]["grid"]
        node = min(nodes, key=lambda k: abs(nodes[k][0] - x) + abs(nodes[k][1] - y))
        mine = [r for r in sites if r[3].startswith(n + ",")]
        touching = [L for L in links if int(L["from_node"]) == node or int(L["to_node"]) == node]
        lanes = max(int(L["lanes_each_direction"]) for L in touching)
        h = 3600.0 / (sat * lanes)
        nb = [int(L["to_node"]) if int(L["from_node"]) == node else int(L["from_node"]) for L in touching]
        gate_node = [k for k in nb if k in sig]
        gate = None
        if gate_node:
            s = sig[gate_node[0]]
            storage = float([L for L in touching if gate_node[0] in (int(L["from_node"]), int(L["to_node"]))][0]["length_m"])
            N = int(storage // vlen)
            off = sum(int(v) * m for v, m in zip(re.search(r"cycle zero (\S+)\)", s[4]).group(1).split(":"), (3600, 60, 1)))
            cyc = float(s[5])
            stages = {s[6]: (0.0, float(s[7])), s[9]: (float(s[7]) + float(s[8]), float(s[7]) + float(s[8]) + float(s[10]))}
            hb = 3600.0 / int(str(s[12]).split("/")[0])
            gate = (N, off, cyc, stages, hb, gate_node[0])
        days = sorted(sdays[reg[n]["county"]])
        total = k = 0.0
        hv = tv = 0.0
        for d in days:
            day = sorted(cl[reg[n]["code"]].get(d, []))
            k += sum(1 for c in day if 25200 <= c[0] < 36000)
            for r in mine:
                rows = counts[(r[0], d.isoformat())]
                arr, keep = [], []
                for q in range(16):
                    key = "%02d:%02d" % (6 + q // 4, 15 * (q % 4))
                    v = rows[key][0]
                    arr += [6 * 3600 + 900 * q + (j + 0.5) * 900.0 / v for j in range(v)]
                    keep += [q >= 4] * v
                if gate:
                    N, off, cyc, stages, hb, gn = gate
                    g0, g1 = stages[r[4]]
                    # the stop line is downstream when the count site is on the crossing's side away from it
                    sx, sy = nodes[int(r[1])]
                    gx, gy = nodes[gn]
                    down = (sx - x) * (gx - x) + (sy - y) * (gy - y) < 0
                    G = ("down" if down else "up", N, off, cyc, g0, g1, hb)
                    w, w0 = replay(arr, day, h, G), replay(arr, [], h, G)
                else:
                    w, w0 = replay(arr, day, h), replay(arr, [], h)
                total += sum(a - b for a, b, kk in zip(w, w0, keep) if kk)
                older = r[5] == "QT-40"
                inst = r[6].date() if hasattr(r[6], "date") else r[6]
                for q in range(4, 16):
                    v, hg = rows["%02d:%02d" % (6 + q // 4, 15 * (q % 4))]
                    share = older or (d < inst and inst > dt.date(2025, 9, 1) and switched(counts, r[0], inst))
                    hv += hg * v / 100.0 if share else hg
                    tv += v
        got[n] = dict(delay=int(round(total / 3600.0 / 1000)) * 1000, closures="%.1f" % (k / len(days)),
                      hgv="%.1f" % (100 * hv / tv))
    # fault-held hours on the verifier's own reading of the two fault records
    by_asset = {reg[n]["asset"]: n for n in reg}
    held = {n: set() for n in short}
    with open(os.path.join(target, "rail/lx_work_orders_2025_26.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            if r["fault_code"] not in ("BFR", "ODF", "PWR"):
                continue
            t = dt.datetime.strptime(r["reported_at"], "%d/%m/%Y %H:%M")
            sec = t.hour * 3600 + t.minute * 60 + 30
            cand = [by_asset[r["asset_no"]]] if r["asset_no"] in by_asset else list(short)
            hits = [(n, c) for n in cand if n in held for c in cl[reg[n]["code"]].get(t.date(), []) if c[0] <= sec <= c[1]
                    and (r["asset_no"] in by_asset or c[1] - c[0] > 600)]
            if len(hits) == 1:
                held[hits[0][0]].add((t.date(), hits[0][1]))
    occ = load_workbook(os.path.join(target, "rail/signaller_occurrences_2025_26.xlsx"), read_only=True)["Occurrences"]
    for r in occ.iter_rows(min_row=2, values_only=True):
        m = r and r[3] and re.match(r"(.+) LC: barriers failed to rise .* reset from panel (\d\d):(\d\d)", r[3])
        if m and m.group(1) in held:
            reset = int(m.group(2)) * 3600 + int(m.group(3)) * 60
            for c in cl[reg[m.group(1)]["code"]].get(r[0].date(), []):
                if reset <= c[1] < reset + 60:
                    held[m.group(1)].add((r[0].date(), c))
    for n in short:
        got[n]["fault"] = "%.1f" % (sum(c[1] - c[0] for _, c in held[n]) / 3600.0)
    order = sorted(short, key=lambda n: -got[n]["delay"])
    key = lambda n: n.lower().replace(" ", "_")
    for n in short:
        assert F["delay_" + key(n)] == got[n]["delay"], (n, F["delay_" + key(n)], got[n])
        assert F["closures_" + key(n)] == got[n]["closures"], (n, got[n])
        assert F["fault_hours_" + key(n)] == got[n]["fault"], (n, got[n])
        assert F["hgv_share_" + key(n)] == got[n]["hgv"], (n, got[n])
        line = "   - %s: %s vehicle-hours, %s closures per school morning, %s fault-held hours, %s%% heavy goods vehicles" % (
            n, "{:,}".format(got[n]["delay"]), got[n]["closures"], got[n]["fault"], got[n]["hgv"])
        assert line in sub, line
    assert F["call"] == order[0] and F["runner_up"] == order[1], order
    assert F["gap"] == got[order[0]]["delay"] - got[order[1]]["delay"], (F["gap"], order)
    for fname in ("crossing_delay_2025_26.xlsx", "crossing_choice_2027.docx"):
        assert os.path.exists(os.path.join(golden, fname)), fname
    print("verify: %d crossings recomputed from the bundle alone; call %s, runner-up %s" % (len(short), order[0], order[1]))
    return got


def switched(counts, site, inst):
    lo, hi = [], []
    for (s, d), rows in counts.items():
        if s != site or dt.date.fromisoformat(d) >= inst:
            continue
        for v, h in rows.values():
            if v < 45:
                lo.append(h / max(v, 1))
            elif v > 95:
                hi.append(h / v)
    return bool(lo and hi) and sum(lo) / len(lo) > 2 * sum(hi) / len(hi)
