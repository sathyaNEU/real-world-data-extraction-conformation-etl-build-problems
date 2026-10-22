"""Writes task478's evidence pack from world.py: the two WIM exports, the station list, the scale houses' tickets, the
citation log, the toll entries, the plaza list and the two distractors (the documents are docs.py's)."""
import csv
import datetime as dt
import os

import numpy as np

import world as W

FILES = {
    "program": "ctpa_freight_compliance_program_2027.pdf",
    "dictionary": "ctpa_data_exports_dictionary.pdf",
    "schedule": "ctpa_toll_schedule_2025.pdf",
    "piezo": "ctpa_wim_piezo_2026.txt",
    "bending": "ctpa_wim_bendingplate_2026.csv",
    "stations": "ctpa_wim_stations.csv",
    "tickets": "ctpa_scale_house_tickets_2026.xlsx",
    "citations": "ctpa_citations_2026.csv",
    "entries": "ctpa_toll_entries_5axle_2026.csv",
    "plazas": "ctpa_toll_plazas.csv",
    "pavement": "ctpa_pavement_condition_2026.xlsx",
    "bridges": "ctpa_bridge_postings_2026.csv",
}
# station ids as each vendor numbers them; the station list ties them to mileposts
STATION_ID = {"01": "511", "02": "514", "03": "CT03", "04": "522", "05": "CT05", "06": "527", "07": "CT07",
              "08": "533", "09": "538", "10": "CT10", "11": "544", "12": "CT12"}
STATION_MP = {"01": 9.4, "02": 33.0, "03": 57.6, "04": 75.2, "05": 101.3, "06": 119.8, "07": 146.1, "08": 166.5,
              "09": 191.0, "10": 220.4, "11": 243.7, "12": 270.9}
RESITED = ("02", 29.7, dt.date(2025, 8, 18))       # Brannock's station moved from milepost 29.7 in August 2025
RELANED = ("06", dt.date(2026, 4, 14))             # Foxbriar's controller replaced; its lanes renumbered 1 to 4
KG = 0.45359237


def _rng():
    return np.random.default_rng(W.SEED + 7)


def _times(rng, n):
    """Seconds after local standard midnight, trucks spread over the day with a morning and afternoon peak."""
    hours = rng.choice(24, size=n, p=_HOURS)
    return np.sort(hours * 3600 + rng.integers(0, 3600, n))


_H = np.array([2, 2, 2, 3, 5, 8, 10, 11, 11, 10, 10, 10, 10, 10, 10, 10, 9, 8, 6, 5, 4, 3, 3, 2], float)
_HOURS = _H / _H.sum()


def _others(rng, cls, n):
    """Axle weights (lb) and spacings (ft) for the other truck classes, plausible and never class 9."""
    if cls == 5:
        ax = np.stack([rng.normal(6500, 900, n), rng.normal(9000, 2500, n)], 1)
        sp = np.stack([rng.normal(16, 2, n)], 1)
    elif cls == 6:
        ax = np.stack([rng.normal(11000, 1200, n), rng.normal(13000, 3500, n), rng.normal(13000, 3500, n)], 1)
        sp = np.stack([rng.normal(18, 2, n), np.full(n, 4.3)], 1)
    elif cls == 7:
        ax = np.stack([rng.normal(12000, 1200, n)] + [rng.normal(12500, 3500, n) for _ in range(3)], 1)
        sp = np.stack([rng.normal(17, 2, n), np.full(n, 4.3), np.full(n, 4.3)], 1)
    elif cls == 8:
        ax = np.stack([rng.normal(10000, 900, n), rng.normal(15000, 4000, n), rng.normal(13000, 4000, n),
                       rng.normal(13000, 4000, n)], 1)
        sp = np.stack([rng.normal(16, 2, n), rng.normal(30, 4, n), np.full(n, 4.1)], 1)
    elif cls == 10:
        ax = np.stack([rng.normal(11500, 900, n)] + [rng.normal(14500, 3500, n) for _ in range(5)], 1)
        sp = np.stack([rng.normal(17, 2, n), np.full(n, 4.3), rng.normal(32, 4, n), np.full(n, 4.1), np.full(n, 4.1)], 1)
    elif cls == 11:
        ax = np.stack([rng.normal(10500, 900, n)] + [rng.normal(12500, 3000, n) for _ in range(4)], 1)
        sp = np.stack([rng.normal(12, 1.5, n), rng.normal(22, 2, n), rng.normal(9, 1, n), rng.normal(22, 2, n)], 1)
    elif cls == 12:
        ax = np.stack([rng.normal(11000, 900, n)] + [rng.normal(12500, 3000, n) for _ in range(5)], 1)
        sp = np.stack([rng.normal(15, 2, n), np.full(n, 4.3), rng.normal(22, 2, n), rng.normal(9, 1, n),
                       rng.normal(22, 2, n)], 1)
    else:
        ax = np.stack([rng.normal(11500, 900, n)] + [rng.normal(13500, 3000, n) for _ in range(6)], 1)
        sp = np.stack([rng.normal(15, 2, n), np.full(n, 4.3), rng.normal(22, 2, n), np.full(n, 4.1),
                       rng.normal(10, 1, n), rng.normal(22, 2, n)], 1)
    return np.clip(ax, 2500, None), np.clip(sp, 3.5, None)


def wim_rows(e):
    """Per-vehicle records of every station, truth read through the station: class 9 from world.py, the other classes
    drawn here. Times in local standard time all year (the controllers keep no daylight time)."""
    rng = _rng()
    out = {}
    for r in e["wim"]:
        code = r["code"]
        rows = []
        n9 = len(r["gross"])
        # class 9 spacings: steer to drive, drive tandem, drive to trailer, trailer tandem (spread on flatbeds)
        sp9 = np.stack([rng.normal(17.5, 1.6, n9), rng.normal(4.3, 0.1, n9), rng.normal(33.5, 3.2, n9),
                        np.where(r["trailer"] == 1, rng.normal(9.5, 0.6, n9), rng.normal(4.2, 0.15, n9))], 1)
        per_day = {}
        for k, di in enumerate(r["dayidx"]):
            per_day.setdefault(int(di), []).append(("9", k))
        for cls, m in r["others"]:
            n = int(m.sum())
            if n == 0:
                continue
            ax, sp = _others(rng, cls, n)
            read = ax * r["bias"] * rng.normal(1, W.AXLE_SD[r["tech"]], ax.shape)
            idx = np.repeat(np.arange(len(m)), m)
            for k in range(n):
                per_day.setdefault(int(idx[k]), []).append((cls, read[k], sp[k]))
        for di in sorted(per_day):
            day = r["days"][di]
            items = per_day[di]
            secs = _times(rng, len(items))
            order = rng.permutation(len(items))
            for t, j in zip(secs, order):
                it = items[j]
                direction = "E" if rng.random() < 0.5 else "W"
                lane = 1 if rng.random() < 0.83 else 2
                if code == RELANED[0] and day >= RELANED[1] and direction == "W":
                    lane += 2           # the replacement controller numbers the four lanes across the road
                speed = float(np.clip(rng.normal(61, 5), 30, 79))
                flag = 0
                if rng.random() < 0.012:
                    flag = 1
                    speed = float(rng.choice([rng.uniform(4, 14), rng.uniform(81, 92)]))
                if it[0] == "9":
                    k = it[1]
                    ax = r["read"][k]
                    sp = sp9[k]
                    cls = 9
                else:
                    cls, ax, sp = it
                rows.append((day, int(t), direction, lane, speed, cls, ax, sp, flag))
        out[code] = rows
    return out


def write_piezo(path, rows):
    """Fixed-width per-vehicle records: station, direction, lane, date, time (hundredths), speed (tenths of mph),
    class, axles, gross and axle weights (tens of pounds), axle spacings (tenths of feet), validity flag."""
    with open(path, "w", encoding="ascii", newline="\n") as fh:
        for code in sorted(rows):
            if W.SECTIONS[W.CODES.index(code)][4] != "piezo":
                continue
            sid = STATION_ID[code]
            for day, t, direction, lane, speed, cls, ax, sp, flag in rows[code]:
                hh, mm, ss = t // 3600, (t % 3600) // 60, t % 60
                cs = (t * 37) % 100
                w = np.rint(np.asarray(ax) / 10).astype(int)
                g = int(w.sum())
                axw = "".join("%04d" % x for x in w) + "    " * (9 - len(w))
                spc = "".join("%03d" % int(round(x * 10)) for x in sp) + "   " * (8 - len(sp))
                fh.write("%-4s%s%d%s%02d%02d%02d%02d%04d%02d%02d%05d%s%s%d\n" % (
                    sid, direction, lane, day.strftime("%Y%m%d"), hh, mm, ss, cs, int(round(speed * 10)), cls,
                    len(w), g, axw, spc, flag))


def write_bending(path, rows):
    cols = ["site", "dir", "lane", "local_time", "speed_kph", "fhwa_class", "axles", "gvw_kg"] + \
           ["ax%d_kg" % i for i in range(1, 10)] + ["sp%d_m" % i for i in range(1, 9)] + ["status"]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for code in sorted(rows):
            if W.SECTIONS[W.CODES.index(code)][4] != "bending":
                continue
            sid = STATION_ID[code]
            for day, t, direction, lane, speed, cls, ax, sp, flag in rows[code]:
                stamp = dt.datetime.combine(day, dt.time()) + dt.timedelta(seconds=int(t))
                kg = [int(round(x * KG)) for x in ax]
                row = [sid, "EB" if direction == "E" else "WB", lane, stamp.strftime("%Y-%m-%d %H:%M:%S"),
                       "%.1f" % (speed * 1.609344), cls, len(kg), sum(kg)] + kg + [""] * (9 - len(kg)) + \
                      ["%.2f" % (x * 0.3048) for x in sp] + [""] * (8 - len(sp)) + ["REJ" if flag else "OK"]
                w.writerow(row)


def write_stations(path):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["station_id", "milepost", "technology", "lanes", "in_service", "previous_milepost",
                    "moved"])
        for code in W.CODES:
            tech = W.SECTIONS[W.CODES.index(code)][4]
            prev, moved = ("", "")
            if code == RESITED[0]:
                prev, moved = "%.1f" % RESITED[1], RESITED[2].isoformat()
            w.writerow([STATION_ID[code], "%.1f" % STATION_MP[code],
                        "quartz piezoelectric" if tech == "piezo" else "bending plate", 4,
                        "2019-06-01" if tech == "piezo" else "2014-09-15", prev, moved])


def entry_host(p):
    """Which host recorded a plaza's entries: the switch time, or "old" or "new" for a plaza only ever on one."""
    if p[6] is not None and p[6] < dt.date(2026, 7, 1):
        return "old"
    if p[5] is not None and p[5] >= dt.date(2026, 7, 1):
        return "new"
    return W.switch_time(p[0])


def entry_rows(e):
    """The toll back office's five-axle entries as exported from the new host: the old host's entries up to each
    plaza's move (numeric ids; the old host's receipt stamp, local time to the minute), the new host's own entries
    from the move (its ids; UTC to the second) and its backfill of each plaza's last days before the move, read from
    the lanes' logs (its ids; local time to the second). Rows: id, plaza, stamp text, tag, true local time, host."""
    rng = np.random.default_rng(W.SEED + 11)
    out = []
    for d, i, tag, s_ in sorted(e["entries"], key=lambda r: (r[0], r[3], r[1], r[2])):
        p = W.PLAZAS[i]
        local = dt.datetime.combine(d, dt.time()) + dt.timedelta(seconds=s_)
        utc = local + dt.timedelta(hours=W.eastern_offset(d))
        host = entry_host(p)
        if host == "old" or (host != "new" and local < host):
            got = local + dt.timedelta(seconds=float(rng.uniform(0, W.RECEIPT_MIN * 60)))
            out.append(["OLD", p[0], got.strftime("%Y-%m-%d %H:%M"), tag, local, "old"])
            if host != "old" and local >= host - dt.timedelta(days=W.BACKFILL_DAYS):
                out.append(["NEW", p[0], local.strftime("%Y-%m-%d %H:%M:%S"), tag, local, "backfill"])
        else:
            out.append(["NEW", p[0], utc.strftime("%Y-%m-%d %H:%M:%S"), tag, local, "live"])
    # the old host numbered entries as it received them; the new host's ids follow the lanes' own sequence
    old_id, new_id = 40250000, 0
    for r in sorted((r for r in out if r[0] == "OLD"), key=lambda r: (r[2], r[1], r[3])):
        old_id += int(rng.integers(1, 4))
        r[0] = "%d" % old_id
    for r in sorted((r for r in out if r[0] == "NEW"), key=lambda r: (r[4], r[1], r[3])):
        new_id += 1
        r[0] = "T26%08d" % new_id
    out.sort(key=lambda r: (r[2], r[1], r[0]))
    return [tuple(r) for r in out]


def write_entries(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["txn_id", "plaza", "entry_utc", "axle_class", "tag_id"])
        for tid, plaza, stamp, tag, _, _ in rows:
            w.writerow([tid, plaza, stamp, 5, tag])


def write_plazas(path):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["plaza", "plaza_name", "milepost", "in_service_from"])
        for p in W.PLAZAS:
            if p[6] is not None:
                continue
            w.writerow([p[0], p[1], "%.1f" % p[3], p[5].isoformat() if p[5] else ""])


def citation_rows(e):
    rows = []
    paper_no, e_no = 26000400, 1
    tk_no = ticket_numbers(e)
    for c in sorted(e["citations"], key=lambda c: (c["local"], c["code"])):
        stp = e["stops"][c["ticket"]]
        if c["paper"]:
            paper_no += 1
            num = "C%d" % paper_no
        else:
            num = "EC-%s-%05d" % (c["local"].strftime("%y%m"), e_no)
            e_no += 1
        logged = W.PLAZAS[e["entries"][c["logged"]][1]][0]
        rows.append((num, c["local"].strftime("%m/%d/%Y %H:%M"), c["keyed"].strftime("%m/%d/%Y %H:%M"),
                     W.SCALE_HOUSES[stp["house"]][0], tk_no[c["ticket"]], stp["tag"], c["code"], logged))
    return rows


def ticket_numbers(e):
    order = sorted(range(len(e["stops"])), key=lambda j: e["stops"][j]["local"])
    nums = {}
    cnt = {"W": 0, "E": 0}
    for j in order:
        h = e["stops"][j]["house"]
        cnt[h] += 1
        nums[j] = "%s26-%05d" % (h, cnt[h])
    return nums


def write_citations(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["citation_no", "issued", "keyed", "scale_house", "ticket_no", "tag_id", "violation",
                    "entry_plaza"])
        for r in rows:
            w.writerow(r)


BODY = {0: "Van", 1: "Flatbed", 2: "Dump", 3: "Container chassis", 4: "Tank"}


def write_tickets(path, e):
    """The scale houses' class 9 tickets, keyed at the scale: every axle and the gross as the officer typed it."""
    import openpyxl
    from openpyxl.styles import Alignment, Font
    rng = np.random.default_rng(W.SEED + 13)
    tk, st = e["tickets"], e["stops"]
    nums = ticket_numbers(e)
    cited = {}
    for c in e["citations"]:
        cited.setdefault(c["ticket"], []).append(c["code"])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tickets 2026"
    head = ["Ticket", "Scale house", "Date", "Time", "Tag", "Body", "Axle 1 (lb)", "Axle 2 (lb)", "Axle 3 (lb)",
            "Axle 4 (lb)", "Axle 5 (lb)", "Gross (lb)", "Result"]
    ws.append(head)
    for cell in ws[1]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    order = sorted(range(len(st)), key=lambda j: st[j]["local"])
    for j in order:
        s_ = st[j]
        local = s_["local"]
        ax = [int(round(x / 20.0) * 20) for x in tk["axles"][j]]
        gross = sum(ax)
        if rng.random() < 0.006:
            g = list("%d" % gross)
            k = int(rng.integers(0, len(g) - 1))
            g[k], g[k + 1] = g[k + 1], g[k]
            gross = int("".join(g))
        res = "Cited " + "/".join(cited[j]) if j in cited else "Passed"
        ws.append([nums[j], W.SCALE_HOUSES[s_["house"]][0], local.date(), local.strftime("%H:%M"), s_["tag"],
                   BODY[int(tk["trailer"][j])]] + ax + [gross, res])
    for row in ws.iter_rows(min_row=2):
        row[2].number_format = "m/d/yyyy"
        for c in row[6:12]:
            c.number_format = "#,##0"
    widths = [12, 17, 11, 7, 13, 17, 11, 11, 11, 11, 11, 11, 12]
    for i, wd in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    ws.freeze_panes = "A2"
    wb.save(path)


def write_pavement(path):
    """Distractor: the 2026 pavement condition survey by section and direction."""
    import openpyxl
    from openpyxl.styles import Font
    rng = np.random.default_rng(W.SEED + 17)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Condition 2026"
    ws.append(["Section", "Section name", "Direction", "Lane-miles", "IRI (in/mi)", "Rut depth (in)",
               "Cracking (% of area)", "Survey date"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for s in W.SECTIONS:
        for d in ("EB", "WB"):
            lm = round((s[3] - s[2]) * 2, 1)
            ws.append([s[0], s[1], d, lm, int(rng.normal(88, 18)), round(float(rng.uniform(0.12, 0.38)), 2),
                       round(float(rng.uniform(0.5, 9.0)), 1),
                       dt.date(2026, 5, 4) + dt.timedelta(days=int(rng.integers(0, 40)))])
    for row in ws.iter_rows(min_row=2):
        row[7].number_format = "m/d/yyyy"
    ws.freeze_panes = "A2"
    for i, wd in enumerate([9, 16, 10, 11, 11, 13, 19, 12]):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wd
    wb.save(path)


def write_bridges(path):
    """Distractor: bridges on the roads crossing the turnpike near its interchanges with posted weight limits."""
    rng = np.random.default_rng(W.SEED + 19)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["structure_no", "carries", "near_plaza", "milepost", "posted_limit_tons", "posted_since"])
        k = 0
        for p in W.PLAZAS:
            if p[6] is not None or p[0] in ("P01", "P32"):
                continue
            for _ in range(int(rng.integers(0, 3))):
                k += 1
                w.writerow(["%07d" % (4180000 + 37 * k), "County Road %d" % int(rng.integers(100, 990)), p[0],
                            "%.1f" % (p[3] + rng.uniform(-1.5, 1.5)), int(rng.choice([15, 20, 24, 30, 36])),
                            (dt.date(2012, 1, 1) + dt.timedelta(days=int(rng.integers(0, 4800)))).isoformat()])


def build_pack(target, e=None):
    """Write every file but the PDFs; returns the world and the row counts."""
    e = e or W.everything()
    os.makedirs(target, exist_ok=True)
    rows = wim_rows(e)
    write_piezo(os.path.join(target, FILES["piezo"]), rows)
    write_bending(os.path.join(target, FILES["bending"]), rows)
    write_stations(os.path.join(target, FILES["stations"]))
    write_tickets(os.path.join(target, FILES["tickets"]), e)
    cr = citation_rows(e)
    write_citations(os.path.join(target, FILES["citations"]), cr)
    er = entry_rows(e)
    write_entries(os.path.join(target, FILES["entries"]), er)
    write_plazas(os.path.join(target, FILES["plazas"]))
    write_pavement(os.path.join(target, FILES["pavement"]))
    write_bridges(os.path.join(target, FILES["bridges"]))
    n = {"piezo": sum(len(v) for k, v in rows.items() if W.SECTIONS[W.CODES.index(k)][4] == "piezo"),
         "bending": sum(len(v) for k, v in rows.items() if W.SECTIONS[W.CODES.index(k)][4] == "bending"),
         "entries": len(er), "citations": len(cr), "tickets": len(e["stops"])}
    return e, n
