"""Cuts the register's files from the world: the current system's extract of 30 September 2026, the legacy register's
archive, the crosswalk the move issued, the code lists, the Unit's published 2023-24 table and the two context files."""
import csv
import datetime as dt
import json

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import world as W

D = dt.date
ISO = "%Y-%m-%d"
DMY = "%d/%m/%Y"
PUB25 = D(2025, 9, 30)        # the extract the Unit's 2023-24 final table was compiled from


def numbers(w):
    """legacy numbers in order of first legacy registration, current numbers at the move in legacy order and then in
    order of first registration in the current system"""
    r = np.random.default_rng(W.SEED + 1)
    first = {}
    for s in sorted(w.stays, key=lambda s: (s.registered, s.pid)):
        first.setdefault(s.pid, s.registered)
    issues = sorted([(d, p, 0) for p, d in first.items() if d < W.MOVE] +
                    [(s.dup_registered, s.pid, 1) for s in w.stays if s.dup_registered])
    leg, dup, n = {}, {}, 104217
    for _, p, second in issues:
        (dup if second else leg)[p] = "PR%06d" % n
        n += 1 + (int(r.integers(1, 4)) if r.random() < .06 else 0)
    cur, n = {}, 2000001
    for num, p, second in sorted([(leg[p], p, 0) for p in leg] + [(dup[p], p, 1) for p in dup]):
        if second:
            w.dup_reg[p] = "ES%07d" % n       # the move issued a number for every legacy number it held
        else:
            cur[p] = "ES%07d" % n
        n += 1
    w.dup_no = dup
    n += 137
    for _, p in sorted((d, p) for p, d in first.items() if d >= W.MOVE):
        cur[p] = "ES%07d" % n
        n += 1 + (1 if r.random() < .03 else 0)
    w.legacy_no, w.reg_no = leg, cur
    return leg, cur


def known_leave(s, asof=W.EXTRACT, cut=W.CUT):
    """the register's own knowledge: a departure on or before the cut whose notice had come in by the extract"""
    return s.leave if (s.leave <= cut and s.notice <= asof) else None


def birth_year(w, s):
    p = w.people[s.pid]
    first = w.by_person[s.pid][0].arrive
    return int(first.year - p["age"] - (first.timetuple().tm_yday / 366.0) + .5)


def parish_now(s, registered):
    if registered >= W.MERGE and s.parish in ("HAL", "IVA"):
        return "HLI"
    return s.parish


def current_rows(w):
    rows = []
    tr = [(w.legacy_no[s.pid], s, 0) for s in w.stays if s.transferred()]
    tr += [(w.dup_no[s.pid], s, 1) for s in w.stays if s.transferred() and s.dup_registered]
    tr.sort(key=lambda x: (x[0], x[1].arrive))
    new = sorted((s for s in w.stays if W.MOVE <= s.registered <= W.EXTRACT), key=lambda s: (s.registered, w.reg_no[s.pid]))
    ref = 100001
    for legacy, s, twin in tr + [(None, s, 0) for s in new]:
        p = w.people[s.pid]
        kl = known_leave(s)
        t = s.transferred()
        reg = W.MOVE if t else s.registered
        if twin:
            # the person's second legacy record, carried as a stay of its own and closed by the same leaving notice
            code, start, parish, num = s.code, s.dup_registered, s.dup_parish, w.dup_reg[s.pid]
        else:
            code = s.move_code if t else (s.code if s.registered < W.CODES26 else s.sector)
            start, parish, num = (s.registered if t else s.arrive), (s.parish if t else parish_now(s, s.registered)), \
                w.reg_no[s.pid]
        rows.append(dict(reg_no=num, stay_ref="ST%08d" % ref, record_origin="TRANSFER" if t else "ARRIVAL",
                         arrival_date=start.strftime(ISO), registered_on=reg.strftime(ISO),
                         activity_code=code, parish_code=parish,
                         sex=p["sex"], birth_year=birth_year(w, s), nationality=p["nat"],
                         leaving_date=kl.strftime(ISO) if kl else "",
                         notice_received=s.notice.strftime(ISO) if kl else ""))
        s_ref = rows[-1]["stay_ref"]
        w.stay_ref[id(s)] = s_ref
        ref += 1 + (1 if (ref * 7919) % 97 == 0 else 0)
    return rows


def archive_rows(w):
    rows = []
    for s in sorted((s for s in w.stays if s.registered < W.MOVE), key=lambda s: (w.legacy_no[s.pid], s.arrive)):
        p = w.people[s.pid]
        t = s.transferred()
        row = dict(LEGACY_NO=w.legacy_no[s.pid], DATE_OF_ARRIVAL=s.arrive.strftime(DMY),
                   DATE_REGISTERED=s.registered.strftime(DMY), ACTIVITY=s.code, PARISH=s.parish,
                   SEX=p["sex"], YOB=birth_year(w, s), NATIONALITY=p["nat"],
                   DATE_OF_LEAVING="" if t else s.leave.strftime(DMY),
                   CLOSURE="TRANSFERRED" if t else "LEFT",
                   CLOSED_ON=(W.MOVE - dt.timedelta(days=1)).strftime(DMY) if t else s.notice.strftime(DMY))
        rows.append(row)
        if s.dup_registered:
            rows.append(dict(row, LEGACY_NO=w.dup_no[s.pid], DATE_REGISTERED=s.dup_registered.strftime(DMY),
                             PARISH=s.dup_parish))
    rows.sort(key=lambda r: (r["LEGACY_NO"], r["DATE_OF_ARRIVAL"][6:] + r["DATE_OF_ARRIVAL"][3:5] + r["DATE_OF_ARRIVAL"][:2]))
    return rows


def write_csv(path, rows, fields, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\r\n" if crlf else "\n")
        wr.writeheader()
        for r in rows:
            wr.writerow(r)
    return len(rows)


CUR_FIELDS = ["reg_no", "stay_ref", "record_origin", "arrival_date", "registered_on", "activity_code", "parish_code",
              "sex", "birth_year", "nationality", "leaving_date", "notice_received"]
ARC_FIELDS = ["LEGACY_NO", "DATE_OF_ARRIVAL", "DATE_REGISTERED", "ACTIVITY", "PARISH", "SEX", "YOB", "NATIONALITY",
              "DATE_OF_LEAVING", "CLOSURE", "CLOSED_ON"]


def register_files(paths, w):
    w.stay_ref = {}
    w.dup_reg = {}
    numbers(w)
    n = {}
    cur = current_rows(w)
    n["extract"] = write_csv(paths["extract"], cur, CUR_FIELDS)
    n["archive"] = write_csv(paths["archive"], archive_rows(w), ARC_FIELDS, crlf=True)
    xw = [dict(legacy_no=w.legacy_no[p], reg_no=w.reg_no[p], issued_on=W.MOVE.strftime(ISO)) for p in w.legacy_no]
    xw += [dict(legacy_no=w.dup_no[p], reg_no=w.dup_reg[p], issued_on=W.MOVE.strftime(ISO)) for p in w.dup_no]
    xw.sort(key=lambda r: r["legacy_no"])
    n["crosswalk"] = write_csv(paths["crosswalk"], xw, ["legacy_no", "reg_no", "issued_on"])
    w.extract_rows = cur
    return n


def sector_json(path):
    doc = {"title": "Employment sector classification for population and migration statistics, 2026 edition",
           "publisher": "Esklett Statistics Unit", "issued": "2025-11-14", "in_use_from": "2026-01-01",
           "note": ("The 2026 sector list replaces the 2014 activity codes on registration forms from 1 January 2026. "
                    "Records registered before then keep the 2014 code they were registered under; each 2014 code "
                    "belongs to exactly one 2026 sector."),
           "sectors_2026": [dict(code=c, name=n) for c, n in W.SECTORS],
           "activity_codes_2014": [dict(code=c, title=t, sector_2026=s) for c, t, s in W.ACT14]}
    json.dump(doc, open(path, "w"), indent=2)
    return len(W.ACT14)


def parish_csv(path):
    rows = []
    for c, n in W.PARISHES:
        rows.append(dict(parish_code=c, parish=n, in_use_from="2014-01-01",
                         in_use_to="2025-03-31" if c in ("HAL", "IVA") else "",
                         now_part_of="HLI" if c in ("HAL", "IVA") else c))
    rows.append(dict(parish_code="HLI", parish="Haldervoe and Ivarsby", in_use_from="2025-04-01", in_use_to="",
                     now_part_of="HLI"))
    return write_csv(path, rows, ["parish_code", "parish", "in_use_from", "in_use_to", "now_part_of"])


def _sheet_widths(ws, widths):
    for i, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wd


def final_table(w, year0, asof):
    """each sector's arrivals in the year from 1 July year0 and those whose stay reached twelve months, as the extract
    of `asof` recorded them (the current system's records only: every such arrival registered after the move)"""
    out = {s: [0, 0] for s in W.SECT}
    a0, a1 = D(year0, 7, 1), D(year0 + 1, 6, 30)
    for r in w.extract_rows:
        a = dt.date.fromisoformat(r["arrival_date"])
        if r["record_origin"] != "ARRIVAL" or not (a0 <= a <= a1):
            continue
        if dt.date.fromisoformat(r["registered_on"]) > asof:
            continue
        sec = W.TO26.get(r["activity_code"], r["activity_code"])
        lv = r["leaving_date"]
        known = lv and dt.date.fromisoformat(r["notice_received"]) <= asof
        long_ = (not known) or dt.date.fromisoformat(lv) >= W.anniversary(a)
        out[sec][0] += 1
        out[sec][1] += long_
    return out


def published_2023_24(path, w):
    t = final_table(w, 2023, PUB25)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Table 1"
    ws["A1"] = "Table 1. Long-term immigration by employment sector, year to 30 June 2024 (final)"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Esklett Statistics Unit. Population and Migration Statistics, published 16 October 2025."
    hdr = ["Sector code", "Employment sector", "Arrivals registered", "Long-term immigration",
           "Stays under twelve months", "Long-term share (%)"]
    ws.append([])
    ws.append(hdr)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    tot = [0, 0]
    for code, name in W.SECTORS:
        a, l = t[code]
        tot[0] += a
        tot[1] += l
        ws.append([code, name, a, l, a - l, round(100.0 * l / a, 1)])
    ws.append([None, "All sectors", tot[0], tot[1], tot[0] - tot[1], round(100.0 * tot[1] / tot[0], 1)])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[5].number_format = "0.0"
        for c in row[2:5]:
            c.number_format = "#,##0"
    ws.append([])
    notes = ["Source: Population Register, current system, extract of 30 September 2025.",
             "Long-term immigration: arrivals in the year whose stay on the island lasted twelve months or more.",
             "Sector: the activity declared at the arrival registration (2014 activity codes, shown on the 2026 sector list).",
             "Arrivals registered for work only; the year runs from 1 July 2023 to 30 June 2024 by arrival date."]
    for nline in notes:
        ws.append([nline])
    _sheet_widths(ws, [12, 38, 14, 14, 14, 12])
    ws.freeze_panes = "A5"
    wb.save(path)
    return t


def passengers(path):
    r = np.random.default_rng(W.SEED + 7)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Monthly"
    ws.append(["Month", "Port", "Passengers arriving", "Passengers departing"])
    for c in ws[1]:
        c.font = Font(bold=True)
    season = [.62, .66, .78, .92, 1.05, 1.18, 1.42, 1.48, 1.12, .9, .72, .8]
    m, n = D(2024, 1, 1), 0
    while m <= D(2026, 8, 1):
        for port, base in (("Esklett Airport", 27400), ("Port Esklett Ferry Terminal", 21900)):
            k = season[m.month - 1] * base * (1 + .021 * (m.year - 2024))
            if m.month == 6:
                k *= 1.17 if port.startswith("Port") else 1.08          # the midsummer festival fortnight
            if port.startswith("Port") and (m.year, m.month) == (2025, 2):
                k *= .58                                                 # the ferry's refit, a relief vessel
            if (m.year, m.month) in ((2024, 12), (2025, 1), (2026, 3)):
                k *= .9 + .04 * r.random()                               # sailings and flights lost to gales
            arr = int(k * r.normal(1, .03))
            dep = int(k * r.normal(1, .03) * (1.06 if m.month in (7, 8) and port.startswith("Port") else .99))
            ws.append([m.strftime("%b %Y"), port, arr, dep])
            n += 1
        m = D(m.year + (m.month == 12), m.month % 12 + 1, 1)
    for row in ws.iter_rows(min_row=2):
        for c in row[2:]:
            c.number_format = "#,##0"
    ws2 = wb.create_sheet("Notes")
    for line in ["Passenger movements through Esklett Airport and Port Esklett Ferry Terminal, all travellers.",
                 "Source: Esklett Ports Authority, operators' monthly returns. Crew and transit passengers excluded.",
                 "Published 9 September 2026."]:
        ws2.append([line])
    _sheet_widths(ws, [12, 30, 20, 20])
    _sheet_widths(ws2, [100])
    ws.freeze_panes = "A2"
    wb.save(path)
    return n


def census_2021(path):
    r = np.random.default_rng(W.SEED + 11)
    groups = ["Esklett", "United Kingdom", "Ireland", "Other Europe", "Rest of the world"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "CT03"
    ws["A1"] = "Census 2021, table CT03: usual residents by parish and country of birth"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Census day 21 March 2021. Esklett Statistics Unit."
    ws.append([])
    ws.append(["Parish code", "Parish"] + groups + ["All usual residents"])
    for c in ws[4]:
        c.font = Font(bold=True)
    tot = np.zeros(6, int)
    for (c, nm), wt in zip(W.PARISHES, W.PARISH_W):
        pop = int(84050 * wt * r.normal(1, .04))
        shares = np.array([.47, .29, .045, .085, .11]) * r.normal(1, .06, 5)
        shares = shares / shares.sum()
        v = [int(pop * x) for x in shares]
        ws.append([c, nm] + v + [sum(v)])
        tot += np.array(v + [sum(v)])
    ws.append([None, "Esklett"] + [int(x) for x in tot])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    for row in ws.iter_rows(min_row=5):
        for c in row[2:]:
            c.number_format = "#,##0"
    _sheet_widths(ws, [12, 16, 11, 15, 11, 13, 17, 19])
    wb.save(path)
    return len(W.PARISHES)
