"""task490 golden: every graded figure computed forward from the shipped files under target/, and the three
golden deliverables written from them."""
import csv
import json
import os
from datetime import date, datetime, timedelta

import world as W
import records as R
import docs as D

GROUP_MIN = 3.0          # same-direction records this close at one lock are one chamber cycle
DUP_SEC = 60             # the same plate read twice this close is one boat


def utc_to_local(u):
    return W.to_local(u)


def parse_detected(s):
    if s.endswith("Z"):
        return utc_to_local(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")), "v2"
    return datetime.strptime(s, "%d/%m/%Y %H:%M:%S"), "v1"


def load_sites(target):
    doc = json.load(open(os.path.join(target, R.F_SITES)))
    return {s["site_code"]: s["asset"] for s in doc["sites"]}


def load_moves(target):
    site_asset = load_sites(target)
    ev = {a: [] for a in W.LOCK}
    with open(os.path.join(target, R.F_MOVES), newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t, ver = parse_detected(row["detected_at"])
            d = "up" if row["direction"] in ("UP", "A>B") else "down"
            cls = "boat" if row["class"] in ("BOAT", "VESSEL") else "unpowered"
            ev[site_asset[row["site_code"]]].append(dict(t=t, dir=d, cls=cls, idx=row["index_read"],
                                                         no=int(row["record_no"])))
    for a in ev:
        ev[a].sort(key=lambda e: (e["t"], e["no"]))
    return ev


def load_keepers(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, R.F_KEEP), read_only=True)
    out = []
    for ws in wb.worksheets:
        hdr = None
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Day":
                hdr = row
                continue
            if hdr is None or not row or not row[0]:
                continue
            t = datetime.strptime(row[0] + " " + row[1], "%d/%m/%y %H:%M")
            out.append(dict(t=t, asset="TC/L08" if row[2] == "Top" else "TC/L09", boat=row[3], idx=row[4] or "",
                            dir="up" if row[5] == "U" else "down"))
    return out


def clean_moves(ev):
    """drop unpowered craft and repeat reads of one plate; returns kept events and the counts left out."""
    kept, dups, unp = {}, {}, {}
    for a, es in ev.items():
        out, last = [], {}
        nd = nu = 0
        for e in es:
            if e["cls"] != "boat":
                nu += 1
                continue
            k = (e["idx"], e["dir"])
            if e["idx"] and k in last and (e["t"] - last[k]).total_seconds() <= DUP_SEC:
                nd += 1
                continue
            last[k] = e["t"]
            out.append(e)
        kept[a], dups[a], unp[a] = out, nd, nu
    return kept, dups, unp


def camera_gap(es, lo=date(2026, 8, 1), hi=date(2026, 8, 31)):
    best = None
    for x, y in zip(es, es[1:]):
        if lo <= x["t"].date() <= hi:
            g = (y["t"] - x["t"]).total_seconds()
            if best is None or g > best[0]:
                best = (g, x["t"], y["t"])
    return best[1], best[2]


def stitch_keepers(kept, keepers):
    """keepers' entries at Tilsey Top Lock that the camera did not record (its outage), linked by plate,
    direction and time."""
    es = kept["TC/L08"]
    g0, g1 = camera_gap(es)
    window = [e for e in es if g0 - timedelta(hours=2) <= e["t"] <= g1 + timedelta(hours=2)]
    used = set()
    add = []
    for k in keepers:
        if k["asset"] != "TC/L08" or not (g0 - timedelta(hours=1) <= k["t"] <= g1 + timedelta(hours=1)):
            continue
        match = None
        for i, e in enumerate(window):
            if i in used or e["dir"] != k["dir"] or not k["idx"] or e["idx"] != k["idx"]:
                continue
            if abs((e["t"] - k["t"]).total_seconds()) <= 25 * 60:
                match = i
                break
        if match is None:
            if g0 - timedelta(minutes=30) <= k["t"] <= g1:
                add.append(dict(t=k["t"], dir=k["dir"], cls="boat", idx=k["idx"], no=-1, keeper=True))
        else:
            used.add(match)
    merged = dict(kept)
    merged["TC/L08"] = sorted(es + add, key=lambda e: (e["t"], e["no"]))
    return merged, len(add), (g0, g1)


def cycles_of(es, gap_min=GROUP_MIN):
    cyc = []
    for e in es:
        if cyc and cyc[-1]["dir"] == e["dir"] and (e["t"] - cyc[-1]["last"]).total_seconds() <= gap_min * 60:
            cyc[-1]["boats"] += 1
            cyc[-1]["last"] = e["t"]
        else:
            cyc.append(dict(dir=e["dir"], t=e["t"], last=e["t"], boats=1))
    return cyc


def reopenings():
    """the notices' 'left empty' reopenings inside the season (local time)."""
    return {"HN/L32": [datetime(2026, 5, 29, 17, 0)]}


def replay(cyc, asset):
    st = "L"
    fills = []
    resets = list(reopenings().get(asset, []))
    prev = None
    for c in cyc:
        for r_ in resets:
            if prev is not None and prev < r_ <= c["t"]:
                st = "L"
        f = c["dir"] == "up" or st == "L"
        fills.append(f)
        st = "H" if c["dir"] == "up" else "L"
        prev = c["t"]
    return fills


def lockage(target):
    ev = load_moves(target)
    kept, dups, unp = clean_moves(ev)
    keepers = load_keepers(target)
    merged, n_keep, gap = stitch_keepers(kept, keepers)
    per = {}
    daily = []
    for a in W.LOCK:
        es = merged[a]
        cyc = cycles_of(es)
        fl = replay(cyc, a)
        vol = W.LOCK[a]["lockful"]
        up = sum(1 for e in es if e["dir"] == "up")
        down = len(es) - up
        nf = sum(fl)
        per[a] = dict(up=up, down=down, cycles=len(cyc), fills=nf, ml=round(nf * vol / 1000.0, 1),
                      m3=nf * vol, dups=dups[a], unpowered=unp[a])
        by_day = {}
        for c, f in zip(cyc, fl):
            dd = c["t"].date()
            x = by_day.setdefault(dd, [0, 0, 0])
            if f:
                x[2] += 1
        for e in es:
            x = by_day.setdefault(e["t"].date(), [0, 0, 0])
            x[0 if e["dir"] == "up" else 1] += 1
        for dd in W.DAYS:
            u, dn, f = by_day.get(dd, [0, 0, 0])
            daily.append([dd.isoformat(), W.LOCK[a]["summit"], a, W.LOCK[a]["name"], u, dn, f,
                          "%.1f" % (f * vol)])
    summit = {s: round(sum(per[a]["m3"] for a in W.SUMMIT_LOCKS[s]) / 1000.0, 1) for s in W.SUMMITS}
    return per, summit, daily, n_keep, gap, merged


# ---------------------------------------------------------------------------------------------- reservoirs
SEASON_A = datetime(2026, 4, 1, 0, 0)
SEASON_B = datetime(2026, 11, 1, 0, 0)


def load_returns(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, R.F_RET), read_only=True)
    out = {}
    for ws in wb.worksheets:
        name, lines, hdr = None, [], False
        for row in ws.iter_rows(values_only=True):
            if row and row[0] == "Site":
                name = row[1]
            elif row and row[0] == "Date":
                hdr = True
            elif hdr and row and row[0]:
                lines.append(dict(d=datetime.strptime(row[0], "%d/%m/%Y").date(), rate=float(row[3] or 0),
                                  rel=float(row[4] or 0), rem=row[5] or ""))
        out[name] = lines
    return out


def rate_segments(lines):
    """the valve's rate through time, rebuilt from each 09:00 rate and the timed remarks."""
    import re
    segs = []
    cur = None
    prev_rate = 0.0
    for ln in lines:
        a = datetime(ln["d"].year, ln["d"].month, ln["d"].day, 9) - timedelta(days=1)
        events = []
        for part in [p.strip() for p in ln["rem"].split(";") if p.strip()]:
            m = re.match(r"(\d\d):(\d\d) valve (opened to [\d.]+ turns \(([\d.]+) Ml/d\)|shut)", part)
            hh, mm = int(m.group(1)), int(m.group(2))
            t = datetime(ln["d"].year, ln["d"].month, ln["d"].day, hh, mm)
            if (hh, mm) > (9, 0):
                t -= timedelta(days=1)
            events.append((t, float(m.group(4)) if m.group(4) else 0.0))
        events.sort()
        t0 = a
        rate = prev_rate
        for t, r in events:
            segs.append((t0, t, rate))
            t0, rate = t, r
        segs.append((t0, a + timedelta(days=1), rate))
        assert abs(rate - ln["rate"]) < 1e-9, (ln["d"], rate, ln["rate"])
        prev_rate = ln["rate"]
    return segs


def seg_volume(segs, a, b):
    v = 0.0
    for s, e, r in segs:
        lo, hi = max(s, a), min(e, b)
        if hi > lo:
            v += r * (hi - lo).total_seconds() / 86400.0
    return v


def coldmere(target):
    harn = tils = total = 0.0
    with open(os.path.join(target, R.F_COLD), newline="") as f:
        for row in csv.DictReader(f):
            t = datetime.strptime(row["period_end_utc"], "%Y-%m-%dT%H:%M:%SZ")
            if not (datetime(2026, 3, 31, 23, 0) < t <= datetime(2026, 11, 1, 0, 0)):
                continue
            h = float(row["head_mm_mean"]) / 1000.0
            b = W.COLDMERE_OLD_B if t <= W.COLDMERE_PLATE_UTC else W.COLDMERE_NEW_B
            q = W.weir_q(b, h)
            qh, qt = fox_split(q)
            total += q * 900
            harn += qh * 900
            tils += qt * 900
    return total / 1000.0, harn / 1000.0, tils / 1000.0


def fox_split(q):
    if q <= 0:
        return 0.0, 0.0
    lo, hi = 0.0, 2.0
    for _ in range(80):
        H = (lo + hi) / 2
        tot = W.weir_q(W.FOX_HARNOCK_B, H) + W.weir_q(W.FOX_TILSEY_B, H - W.FOX_TILSEY_CREST)
        if tot < q:
            lo = H
        else:
            hi = H
    H = (lo + hi) / 2
    qh = W.weir_q(W.FOX_HARNOCK_B, H)
    qt = W.weir_q(W.FOX_TILSEY_B, H - W.FOX_TILSEY_CREST)
    k = q / (qh + qt)
    return qh * k, qt * k


def reservoirs(target):
    ret = load_returns(target)
    rel = {}
    for name in ("Upper Kelsby Reservoir", "Tilsey Reservoir", "Lower Kelsby Reservoir"):
        rel[name] = seg_volume(rate_segments(ret[name]), SEASON_A, SEASON_B)
    c_tot, c_h, c_t = coldmere(target)
    rel["Coldmere Reservoir"] = c_tot
    recv = {"Kelsby": rel["Lower Kelsby Reservoir"], "Harnock": c_h, "Tilsey": rel["Tilsey Reservoir"] + c_t}
    return rel, recv, (c_h, c_t)


# --------------------------------------------------------------------------------------------- abstraction
def abstraction(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, R.F_LIC), read_only=True)
    lic = []
    for row in wb.worksheets[0].iter_rows(values_only=True):
        if row and isinstance(row[0], str) and "/" in row[0] and row[0][:2] in ("KA", "HA", "TA"):
            lic.append(dict(ref=row[0], summit=row[2].replace(" summit", ""), point=row[3], digits=int(row[7]),
                            serial=row[6]))
    reads = {}
    with open(os.path.join(target, R.F_READ), newline="") as f:
        for row in csv.DictReader(f):
            t = datetime.strptime(row["read_date"] + " " + row["read_time"], "%d/%m/%Y %H:%M")
            reads.setdefault(row["point_ref"], []).append((t, row["meter_serial"], int(row["reading_m3"])))
    notes = []
    with open(os.path.join(target, R.F_WO), newline="") as f:
        for row in csv.DictReader(f):
            if row["completion_note"].startswith("Meter SN"):
                notes.append(row)
    import re
    out = {}
    for L in lic:
        rs = sorted(reads[L["point"]])
        mod = 10 ** L["digits"]
        serials = []
        for t, s, v in rs:
            if s not in serials:
                serials.append(s)
        take = 0
        if len(serials) == 1:
            for (t0, s0, v0), (t1, s1, v1) in zip(rs, rs[1:]):
                take += (v1 - v0) % mod
        else:
            note = [n for n in notes if n["asset"] == L["point"]][0]["completion_note"]
            m = re.match(r"Meter SN (\S+) removed, final reading (\d+)\. New meter SN (\S+) fitted and sealed, "
                         r"reading (\d+)", note)
            old_s, removed, new_s, installed = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
            old = [x for x in rs if x[1] == old_s]
            new = [x for x in rs if x[1] == new_s]
            seq_old = [v for _, _, v in old] + [removed]
            seq_new = [installed] + [v for _, _, v in new]
            for a_, b_ in zip(seq_old, seq_old[1:]):
                take += (b_ - a_) % mod
            for a_, b_ in zip(seq_new, seq_new[1:]):
                take += (b_ - a_) % mod
        out[L["ref"]] = dict(summit=L["summit"], take=take)
    tot = {s: sum(v["take"] for v in out.values() if v["summit"] == s) for s in W.SUMMITS}
    return out, tot


# ------------------------------------------------------------------------------------------------ figures
def figures(target):
    per, summit, daily, n_keep, gap, merged = lockage(target)
    rank = sorted(W.SUMMITS, key=lambda s: -summit[s])
    rel, recv, split = reservoirs(target)
    absn, abst = abstraction(target)
    figs = {
        "call": rank[0], "runner_up": rank[1], "third": rank[2],
        "gap_ml": round(summit[rank[0]] - summit[rank[1]], 1),
        "lockage_ml": {s: summit[s] for s in W.SUMMITS},
        "locks": {a: dict({k: per[a][k] for k in ("up", "down", "cycles", "fills", "ml", "dups", "unpowered")},
                      boats=per[a]["up"] + per[a]["down"])
                  for a in W.LOCK},
        "records_left_out": {"duplicate_reads": sum(per[a]["dups"] for a in W.LOCK),
                             "unpowered_craft": sum(per[a]["unpowered"] for a in W.LOCK)},
        "keepers_entries_taken": n_keep,
        "camera_gap": [gap[0].isoformat(sep=" "), gap[1].isoformat(sep=" ")],
        "reservoir_release_ml": {k: round(v, 1) for k, v in rel.items()},
        "summit_received_ml": {k: round(v, 1) for k, v in recv.items()},
        "fox_bridge_ml": {"Harnock arm": round(split[0], 1), "Tilsey arm": round(split[1], 1)},
        "abstraction_m3": {k: v["take"] for k, v in absn.items()},
        "abstraction_summit_m3": abst,
        "lockfuls_m3": {a: W.LOCK[a]["lockful"] for a in W.LOCK},
    }
    return figs, daily


# ------------------------------------------------------------------------------------------ deliverables
def write_return(folder, daily):
    with open(os.path.join(folder, "summit_lockage_return_2026.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["date", "summit", "lock_asset", "lock_name", "boats_up", "boats_down", "chamber_fillings",
                    "water_drawn_m3"])
        for r in sorted(daily, key=lambda x: (x[0], x[2])):
            w.writerow(r)


def write_workbook(folder, figs):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    wb = Workbook()
    wb.properties.creator = W.PEOPLE["planner"]
    wb.properties.lastModifiedBy = W.PEOPLE["planner"]
    wb.properties.title = "Summit water 2026"
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DCE8E2")
    ml, cnt = "#,##0.0", "#,##0"

    def header(ws, row):
        for c in ws[row]:
            if c.value is not None:
                c.font = bold
                c.fill = head
                c.alignment = Alignment(wrap_text=True, vertical="top")

    ws = wb.active
    ws.title = "Lockage"
    ws.append(["Kelsby summit drew the most water in 2026: lockage by summit lock, 1 April to 31 October"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Water drawn from the summit pound by filling the chamber; lockful from the 2025 chamber survey"])
    ws.append([])
    ws.append(["Summit", "Lock", "Asset", "Boats up", "Boats down", "Chamber cycles", "Chamber fillings",
               "Lockful (m3)", "Water drawn (Ml)"])
    header(ws, 4)
    for s in W.SUMMITS:
        for a in W.SUMMIT_LOCKS[s]:
            L = figs["locks"][a]
            ws.append([s, W.LOCK[a]["name"], a, L["up"], L["down"], L["cycles"], L["fills"], W.LOCK[a]["lockful"],
                       L["ml"]])
        ws.append([s + " summit", "", "", "", "", "", "", "", figs["lockage_ml"][s]])
        ws.cell(row=ws.max_row, column=1).font = bold
        ws.cell(row=ws.max_row, column=9).font = bold
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        for c in row[3:7]:
            c.number_format = cnt
        row[7].number_format = "#,##0.0"
        row[8].number_format = ml
    ws.append([])
    ws.append(["Recommended site", figs["call"] + " summit", "", "", "", "", "", "Lead over " + figs["runner_up"],
               figs["gap_ml"]])
    ws.cell(row=ws.max_row, column=9).number_format = ml
    ws.append(["Source: LockCount export of 3 November 2026; Tilsey keepers' log for Tilsey Top Lock, 3 to 23 August."])
    ws.freeze_panes = "A5"
    for col, wd in zip("ABCDEFGHI", (17, 19, 9, 10, 11, 14, 15, 12, 16)):
        ws.column_dimensions[col].width = wd
    ws2 = wb.create_sheet("Counter records")
    ws2.append(["Counter records left out of the return, by summit lock"])
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.append([])
    ws2.append(["Lock", "Asset", "Repeat reads of one plate", "Unpowered craft"])
    header(ws2, 3)
    for a in W.LOCK:
        ws2.append([W.LOCK[a]["name"], a, figs["locks"][a]["dups"], figs["locks"][a]["unpowered"]])
    ws2.append(["All summit locks", "", figs["records_left_out"]["duplicate_reads"],
                figs["records_left_out"]["unpowered_craft"]])
    ws2.cell(row=ws2.max_row, column=1).font = bold
    for row in ws2.iter_rows(min_row=4, max_row=ws2.max_row):
        for c in row[2:4]:
            c.number_format = cnt
    ws2.append([])
    ws2.append(["Tilsey Top Lock camera out of service", "from the last record at %s to the first at %s" % (
        figs["camera_gap"][0][:16], figs["camera_gap"][1][:16])])
    ws2.append(["Keepers' log entries taken in for the outage", figs["keepers_entries_taken"]])
    ws2.freeze_panes = "A4"
    for col, wd in zip("ABCD", (40, 34, 24, 16)):
        ws2.column_dimensions[col].width = wd
    ws3 = wb.create_sheet("Reservoirs")
    ws3.append(["Reservoir water, 1 April to 31 October 2026, reckoned at the outlets"])
    ws3["A1"].font = Font(bold=True, size=12)
    ws3.append([])
    ws3.append(["Reservoir", "Released (Ml)", "Goes to"])
    header(ws3, 3)
    goes = {"Upper Kelsby Reservoir": "Lower Kelsby Reservoir", "Lower Kelsby Reservoir": "Kelsby summit",
            "Coldmere Reservoir": "Fox Bridge division weir", "Tilsey Reservoir": "Tilsey summit"}
    for k in W.RESERVOIRS:
        ws3.append([k, figs["reservoir_release_ml"][k], goes[k]])
        ws3.cell(row=ws3.max_row, column=2).number_format = ml
    ws3.append([])
    ws3.append(["Summit", "Received (Ml)", "From"])
    header(ws3, ws3.max_row)
    frm = {"Kelsby": "Lower Kelsby Reservoir", "Harnock": "Coldmere, Harnock arm at Fox Bridge (%.1f)" %
           figs["fox_bridge_ml"]["Harnock arm"],
           "Tilsey": "Tilsey Reservoir and Coldmere, Tilsey arm at Fox Bridge (%.1f)" % figs["fox_bridge_ml"]["Tilsey arm"]}
    for s in W.SUMMITS:
        ws3.append([s + " summit", figs["summit_received_ml"][s], frm[s]])
        ws3.cell(row=ws3.max_row, column=2).number_format = ml
    ws3.append([])
    ws3.append(["Coldmere re-rated on crest plate C2 from 10:30 UTC on 16 June (reservoir register extract)."])
    for col, wd in zip("ABC", (30, 16, 56)):
        ws3.column_dimensions[col].width = wd
    ws4 = wb.create_sheet("Abstraction")
    ws4.append(["Metered take between the March and October month-end readings"])
    ws4["A1"].font = Font(bold=True, size=12)
    ws4.append([])
    ws4.append(["Licence", "Holder", "Summit", "Take (m3)", "Licensed (m3 a year)"])
    header(ws4, 3)
    for L in W.LICENCES:
        ws4.append([L["ref"], L["holder"], L["summit"], figs["abstraction_m3"][L["ref"]], L["annual"]])
    for s in W.SUMMITS:
        ws4.append([s + " summit", "", "", figs["abstraction_summit_m3"][s], ""])
        ws4.cell(row=ws4.max_row, column=1).font = bold
    for row in ws4.iter_rows(min_row=4, max_row=ws4.max_row):
        row[3].number_format = cnt
        row[4].number_format = cnt
    ws4.append([])
    ws4.append(["KA/022, HA/019, HA/026 and TA/011 changed meters in the season; removal and installation "
                "readings from the works orders."])
    ws4.freeze_panes = "A4"
    for col, wd in zip("ABCDE", (14, 34, 10, 12, 20)):
        ws4.column_dimensions[col].width = wd
    ws5 = wb.create_sheet("Notes")
    for line in ["Summit locks: the two locks that rise to each summit pound (programme paper 3.2).",
                 "Season: 1 April to 31 October 2026, clock time at the lock (programme paper 3.1).",
                 "Lockful: the chamber volume in the 2025 chamber survey, in cubic metres (programme paper 3.3).",
                 "Left out of the return: unpowered craft (they portage round the lock) and repeat reads of one plate "
                 "within a minute.",
                 "Reservoir water reckoned at the outlets over the season's clock hours; the keepers' water day ends "
                 "at 09:00 (programme paper 4.2).",
                 "Prepared by Katy Wilkinson, Water Resources Planner, 6 November 2026."]:
        ws5.append([line])
    ws5.column_dimensions["A"].width = 110
    path = os.path.join(folder, "summit_water_2026.xlsx")
    wb.save(path)
    R.normalise_zip(path, "2026-11-06T16:42:00Z")


def write_chart(path, figs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    order = sorted(W.SUMMITS, key=lambda s: -figs["lockage_ml"][s])
    vals = [figs["lockage_ml"][s] for s in order]
    fig, ax = plt.subplots(figsize=(6.2, 2.9), dpi=160)
    cols = ["#1f6f5c" if s == figs["call"] else "#b9c2c8" for s in order]
    bars = ax.barh(order[::-1], vals[::-1], color=cols[::-1], height=0.52)
    for b, v in zip(bars, vals[::-1]):
        ax.text(v + 18, b.get_y() + b.get_height() / 2, "{:,.1f} Ml".format(v), va="center", fontsize=8.5,
                color="#1d2327")
    ax.set_xlim(0, max(vals) * 1.22)
    ax.set_xlabel("Water drawn from the summit pound, megalitres", fontsize=8, color="#3c434a")
    ax.set_title("Kelsby's summit locks drew the most water in the 2026 season", fontsize=9.5, loc="left",
                 color="#1d2327")
    ax.tick_params(labelsize=8.5, colors="#3c434a")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: "{:,.0f}".format(x)))
    ax.grid(axis="x", color="#e3e6e8", linewidth=0.6)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    fig.text(0.01, 0.01, "1 April to 31 October 2026. Source: LockCount export, Tilsey keepers' log, 2025 chamber survey.",
             fontsize=6.5, color="#646970")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def _page_field(par):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    par._p.append(fld)


def write_paper(folder, figs, chart):
    from docx import Document
    from docx.shared import Pt, Mm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Mm(22)
        sec.top_margin = sec.bottom_margin = Mm(18)
        f = sec.footer.paragraphs[0]
        f.text = "Coldmere Canals Trust | Water Management | WM/BP/26-07 | page "
        f.runs[0].font.size = Pt(8)
        _page_field(f)
    cp = doc.core_properties
    cp.author = W.PEOPLE["planner"]
    cp.last_modified_by = W.PEOPLE["planner"]
    cp.title = "Back-pumping scheme 2027/28: siting"
    cp.created = datetime(2026, 11, 5, 9, 12)
    cp.modified = datetime(2026, 11, 6, 16, 40)
    cp.revision = 4
    cp.comments = ""
    cp.keywords = ""
    cp.category = ""
    cp.subject = "Back-pumping scheme siting"
    lk, c, r2, r3 = figs["lockage_ml"], figs["call"], figs["runner_up"], figs["third"]
    p = doc.add_paragraph()
    p.add_run("COLDMERE CANALS TRUST  ").bold = True
    p.add_run("Water Management")
    blk = doc.add_table(rows=5, cols=2)
    for i, (k, v) in enumerate([("To", "Water Management Group, for the trustees' capital meeting of 10 December 2026"),
                                ("From", "Katy Wilkinson, Water Resources Planner"),
                                ("Date", "6 November 2026"),
                                ("Subject", "Back-pumping scheme 2027/28: siting"),
                                ("Reference", "WM/BP/26-07")]):
        blk.rows[i].cells[0].text = k
        blk.rows[i].cells[1].text = v
        blk.rows[i].cells[0].paragraphs[0].runs[0].bold = True
    doc.add_heading("Kelsby summit should take the 2027/28 back-pumping scheme", level=1)
    doc.add_paragraph(
        "Kelsby's two summit locks drew %.1f Ml from the summit pound by filling their chambers between 1 April "
        "and 31 October 2026, %.1f Ml more than %s (%.1f Ml) and well clear of %s (%.1f Ml). On the siting basis "
        "the Water Management Group agreed in September (programme paper 3.1 to 3.4), the scheme goes to Kelsby." % (
            lk[c], figs["gap_ml"], r2, lk[r2], r3, lk[r3]))
    doc.add_heading("What each summit drew", level=2)
    doc.add_paragraph(
        "A summit pound gives up a lockful each time one of its summit locks is filled: for every boat or pair of "
        "boats going up, and for boats going down whenever the boats before them left the chamber empty. I "
        "followed each summit lock's chamber through the season from the counter network's export, with the Tilsey "
        "keepers' log for the three weeks Tilsey Top Lock's camera was out of service.")
    doc.add_paragraph(
        "Harnock carries the biggest lockfuls on the network, but its broad chambers take two boats side by side and "
        "most of its crews share: Harnock Top Lock's %s boat movements made %s chamber cycles and Steward's Lock's %s "
        "made %s. Kelsby's narrow chambers take one boat at a time, short cruisers apart, and the Kelsby Ring and the hire base at the wharf send most "
        "crews up Kelsby Top Lock and down Wharf Lock, so each chamber is usually set against the next boat. Tilsey "
        "carries the most boats, but its flight is worked in turn, with boats going down taking the chamber the last "
        "boat up left full." % ("{:,}".format(figs["locks"]["HN/L31"]["boats"]), "{:,}".format(figs["locks"]["HN/L31"]["cycles"]),
                               "{:,}".format(figs["locks"]["HN/L32"]["boats"]), "{:,}".format(figs["locks"]["HN/L32"]["cycles"])))
    t = doc.add_table(rows=1, cols=5)
    t.style = "Light List Accent 1"
    for i, h in enumerate(["Summit lock", "Boats up", "Boats down", "Fillings", "Water drawn (Ml)"]):
        t.rows[0].cells[i].text = h
    for s in W.SUMMITS:
        for a in W.SUMMIT_LOCKS[s]:
            L = figs["locks"][a]
            row = t.add_row().cells
            for i, v in enumerate([W.LOCK[a]["name"], "{:,}".format(L["up"]), "{:,}".format(L["down"]),
                                   "{:,}".format(L["fills"]), "%.1f" % L["ml"]]):
                row[i].text = v
                if i:
                    row[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    src = doc.add_paragraph("Source: LockCount export of 3 November 2026 with %s repeat reads and %s unpowered craft "
                            "left out; lockfuls from the 2025 chamber survey.*" % (
                                "{:,}".format(figs["records_left_out"]["duplicate_reads"]),
                                "{:,}".format(figs["records_left_out"]["unpowered_craft"])))
    src.runs[0].font.size = Pt(8.5)
    doc.add_picture(chart, width=Mm(150))
    doc.add_heading("The summit water budget", level=2)
    rv, rc = figs["reservoir_release_ml"], figs["summit_received_ml"]
    doc.add_paragraph(
        "Over the same season the reservoirs released %.1f Ml from Lower Kelsby (topped up with %.1f Ml from Upper "
        "Kelsby), %.1f Ml from Coldmere and %.1f Ml from Tilsey. Divided at Fox Bridge, that gave Kelsby summit "
        "%.1f Ml, Harnock summit %.1f Ml and Tilsey summit %.1f Ml. Abstraction agreements took %s m3 from Kelsby, "
        "%s m3 from Harnock (most of it the trout farm's through-flow) and %s m3 from Tilsey." % (
            rv["Lower Kelsby Reservoir"], rv["Upper Kelsby Reservoir"], rv["Coldmere Reservoir"], rv["Tilsey Reservoir"],
            rc["Kelsby"], rc["Harnock"], rc["Tilsey"],
            "{:,}".format(figs["abstraction_summit_m3"]["Kelsby"]),
            "{:,}".format(figs["abstraction_summit_m3"]["Harnock"]),
            "{:,}".format(figs["abstraction_summit_m3"]["Tilsey"])))
    doc.add_heading("For approval", level=2)
    doc.add_paragraph("That the trustees approve Kelsby summit as the site of the 2027/28 back-pumping scheme, with "
                      "detailed design from January 2027. The figures by lock, reservoir and agreement are in "
                      "summit_water_2026.xlsx and the day-by-day return in summit_lockage_return_2026.csv.")
    fn = doc.add_paragraph("* A lockful is the chamber volume in the 2025 chamber survey (programme paper 3.3); the 1951 "
                           "schedule's dimensions in feet and inches are not used.")
    fn.runs[0].font.size = Pt(8)
    path = os.path.join(folder, "backpumping_site_2027.docx")
    doc.save(path)
    R.normalise_zip(path, "2026-11-06T16:40:00Z", app="Microsoft Office Word", ver="16.0000")


def write_golden(folder, target):
    figs, daily = figures(target)
    write_return(folder, daily)
    write_workbook(folder, figs)
    chart = os.path.join(folder, "_chart.png")
    write_chart(chart, figs)
    write_paper(folder, figs, chart)
    os.remove(chart)
    return figs
