"""Writers for the workbooks, notes, logs and the relay event extract, plus the container scrub."""
import csv
import datetime as dt
import os
import re
import shutil
import zipfile

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import world as W

HEAD_FILL = PatternFill("solid", fgColor="DCE3EA")
BOLD = Font(bold=True)


def rng(k):
    return np.random.default_rng(W.SEED * 104729 + k)


def _sheet(ws, title_lines, header, rows, widths, date_cols=(), int_cols=(), freeze=True):
    r = 1
    for i, line in enumerate(title_lines):
        c = ws.cell(row=r, column=1, value=line)
        if i == 0:
            c.font = Font(bold=True, size=12)
        r += 1
    if title_lines:
        r += 1
    for j, h in enumerate(header, 1):
        c = ws.cell(row=r, column=j, value=h)
        c.font = BOLD
        c.fill = HEAD_FILL
        c.alignment = Alignment(vertical="center", wrap_text=True)
    hr = r
    for row in rows:
        r += 1
        for j, v in enumerate(row, 1):
            c = ws.cell(row=r, column=j, value=v)
            if j in date_cols and isinstance(v, (dt.date, dt.datetime)):
                c.number_format = "dd/mm/yyyy"
            elif j in int_cols and isinstance(v, (int, float)):
                c.number_format = "#,##0"
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    if freeze:
        ws.freeze_panes = ws.cell(row=hr + 1, column=1)
    return hr


# ---------------------------------------------------------------------------------------------
def register_last_service(tid):
    svcs = W.OLTC_SERVICES.get(tid, [])
    done = [d for d, _ in svcs]
    if not done:
        return W.REGISTER_PRE_LOG_SERVICE[tid]
    frozen = [d for d in done if d < W.REGISTER_FROZEN_FROM]
    if frozen:
        return max(frozen)
    return W.REGISTER_PRE_LOG_SERVICE.get(tid, dt.date(2018, 5, 1))


SERIAL_PREFIX = {"BR": "BE", "TW": "TW", "MP": "MP", "HC": "HC"}


def write_register(path):
    r = rng(1)
    wb = Workbook()
    ws = wb.active
    ws.title = "Transformers"
    header = ["asset_id", "substation_code", "substation", "position", "manufacturer", "serial_no",
              "year_manufactured", "rewound", "rating_mva", "voltage_kv", "vector_group", "cooling",
              "oil_volume_l", "oil_preservation", "oltc_manufacturer", "oltc_model", "oltc_type",
              "oltc_installed", "oltc_last_service", "status"]
    rows = []
    for u in W.UNITS:
        code, pos = u["id"].split("-")
        maker, ttype = W.OLTC[u["oltc"]]
        serial = f"{SERIAL_PREFIX[u['maker']]}{u['year'] % 100:02d}-{int(r.integers(1100, 9800))}"
        oil = int(round((7400 if u["rating"][1] <= 10 else 12800) * r.uniform(0.92, 1.08), -1))
        if u["rating"][1] <= 7.5:
            oil = int(round(5600 * r.uniform(0.92, 1.08), -1))
        rows.append([u["id"], code, W.SUB_NAME[code], pos, W.TX_MAKERS[u["maker"]], serial, u["year"],
                     u["rewind"], f"{u['rating'][0]:g}/{u['rating'][1]:g}", "33/11", "Dyn11",
                     "ONAN/ONAF", oil,
                     "Conservator, silica gel breather" if u["pres"] == "FB" else "Conservator, air cell",
                     maker, u["oltc"], ttype, u["oltc_year"], register_last_service(u["id"]), "In service"])
    _sheet(ws, [], header, rows, [10, 9, 13, 8, 18, 12, 10, 9, 10, 9, 8, 11, 11, 30, 14, 10, 15, 11, 14, 11],
           date_cols=(19,), int_cols=(13,))
    ws2 = wb.create_sheet("Substations")
    rows2 = []
    gxp = {"LST": "Hornby GXP 33 kV ring", "LIN": "Islington GXP", "RLS": "Islington GXP"}
    for k, (code, name) in enumerate(W.SUBSTATIONS):
        t1, t2 = W.UNIT[f"{code}-T1"], W.UNIT[f"{code}-T2"]
        firm = min(t1["rating"][1], t2["rating"][1])
        rows2.append([code, name, 2, firm, "Yes", min(t1["year"], t2["year"]) if code != "BNM" else 2011])
    _sheet(ws2, [], ["code", "zone_substation", "transformers", "firm_capacity_mva",
                     "mobile_substation_connection", "commissioned"], rows2, [8, 16, 12, 16, 26, 13])
    ws3 = wb.create_sheet("Notes")
    notes = ["Asset management system extract, zone substation power transformers, run 16/10/2026.",
             "One row per transformer in service. rating_mva is ONAN/ONAF.",
             "oltc_type is the tap changer's switching technology as recorded at installation.",
             "oltc_last_service is the date of the tap changer's last service held against the asset."]
    for i, n in enumerate(notes, 1):
        ws3.cell(row=i, column=1, value=n)
    ws3.column_dimensions["A"].width = 100
    wb.save(path)


# ---------------------------------------------------------------------------------------------
def _fmt_counter(v):
    return f"{v:,}"


def log_rows(dlist, ops, cnt, R=None):
    """Closed work orders, 2019 to the extract: tap-changer services, oil processing, breathers,
    annual inspections and other plant work, written the way the crews write them."""
    r = rng(2)
    iday = {d: i for i, d in enumerate(dlist)}
    rows = []

    def counter_at(tid, d):
        j = W.IDS.index(tid)
        if d >= W.START:
            return int(cnt[iday[d], j])
        if any(dd == d and rp for dd, rp in W.OLTC_SERVICES[tid]):
            return int(r.integers(61_000, 98_000))      # the old counter's final reading
        rate = ops[:365, j].mean()
        back = int(round(rate * (W.START - d).days))
        return (int(cnt[0, j]) - back) % W.COUNTER_MODULUS

    oltc_fitters = [W.PEOPLE["fitter"], W.PEOPLE["fitter"], W.PEOPLE["fitter2"]]
    for tid, svcs in W.OLTC_SERVICES.items():
        maker, ttype = W.OLTC[W.UNIT[tid]["oltc"]]
        for k, (d, repl) in enumerate(svcs):
            c = counter_at(tid, d)
            wear = round(float(r.uniform(1.4, 3.6)), 1)
            who = oltc_fitters[int(r.integers(0, 3))]
            if ttype == "Vacuum":
                txt = (f"{maker} {W.UNIT[tid]['oltc']} vacuum tap changer inspection. Diverter insert lifted, "
                       f"interrupter wear indicators within limits, insert oil changed, drive tested through "
                       f"full range. Op counter {_fmt_counter(c)}.")
                rows.append((d, tid, "OLTC INSPECTION", txt, who, round(float(r.uniform(9, 14)) * 2) / 2))
                continue
            style = int(r.integers(0, 4))
            if repl:
                txt = [
                    f"Tap changer service. Diverter switch lifted and overhauled, arcing contacts replaced "
                    f"(worn to {wear} mm), compartment drained, flushed and refilled with new oil. Op counter "
                    f"sticking at {_fmt_counter(c)}, counter replaced, new counter reads 00000.",
                    f"OLTC full service. Diverter overhauled, new contact set fitted, diverter oil changed. "
                    f"Mechanical counter faulty (read {_fmt_counter(c)}), new counter fitted from zero.",
                    f"Diverter overhaul and oil change. Contacts {wear} mm remaining, replaced. Replaced the "
                    f"operations counter, old counter final reading {_fmt_counter(c)}, new counter 00000.",
                    f"{maker} {W.UNIT[tid]['oltc']} service: diverter out, contacts and transition resistors "
                    f"checked, oil changed. Op counter replaced with new unit at zero (old {_fmt_counter(c)}).",
                ][style]
            else:
                stated = r.random() < 0.7 or d < W.START
                cs = f" Op counter {_fmt_counter(c)}, not replaced." if stated else " Counter not replaced."
                txt = [
                    f"Tap changer service. Diverter switch lifted and overhauled, arcing contacts {wear} mm "
                    f"remaining, transition resistors in tolerance, compartment drained, cleaned and refilled "
                    f"with new oil. Drive greased and run through full range.{cs}",
                    f"OLTC full service. Diverter contacts within limits ({wear} mm), new oil in diverter "
                    f"compartment, drive mechanism serviced.{cs}",
                    f"Diverter overhaul and oil change, contact wear OK.{cs}",
                    f"{maker} {W.UNIT[tid]['oltc']} service. Diverter removed, cleaned, contacts measured "
                    f"{wear} mm, oil replaced, motor drive checked.{cs}",
                ][style]
            rows.append((d, tid, "OLTC SERVICE", txt, who, round(float(r.uniform(10, 16)) * 2) / 2))
    for tid, d, n in W.OIL_PROCESSING:
        before = [R["moisture"][i] for i in R["per"][tid] if R["samples"][i][1].date() < d] if R else []
        a = int(round(before[-1] * float(r.uniform(1.05, 1.25)))) if before else int(r.integers(14, 22))
        b = int(r.integers(3, 6))
        txt = (f"Main tank oil processed on site with the hot oil vacuum plant over {n} days, "
               f"{int(r.integers(3, 5))} passes. Water {a} mg/kg before, {b} mg/kg after. Oil degassed. "
               f"Transformer returned to service.")
        rows.append((d + dt.timedelta(n - 1), tid, "OIL PROCESSING", txt, W.PEOPLE["fitter2"], float(8 * n)))
    for tid, d in W.BREATHERS:
        txt = ["Silica gel breather replaced, gel fully saturated (green). Oil seal cup topped up.",
               "Breather replaced, old gel exhausted. New 3 kg breather fitted.",
               "Replaced silica gel breather, crystals all changed colour."][int(r.integers(0, 3))]
        rows.append((d, tid, "BREATHER", txt, W.PEOPLE["sampler"], 1.5))
    # annual inspections and other plant work
    for y in range(2019, 2027):
        for k, (code, name) in enumerate(W.SUBSTATIONS):
            d = dt.date(y, 2, 1) + dt.timedelta(int(r.integers(0, 250)))
            while d.weekday() >= 5 or d in W.HOLIDAYS:
                d += dt.timedelta(1)
            if d > W.EXTRACT_DATE - dt.timedelta(5):
                continue
            col = ["orange", "orange", "orange with some green", "mostly green"][int(r.integers(0, 4))]
            extra = ["", "", " T1 oil level gauge glass cracked, replace at next outage.",
                     " T2 fan 3 noisy bearing, raised WO.", " Kiosk door hinge repaired.",
                     " Bird nest removed from T1 radiator bank."][int(r.integers(0, 6))]
            txt = (f"Annual zone substation inspection. T1 and T2 visual, oil levels normal, breathers {col}, "
                   f"Buchholz relays checked, fans run on manual.{extra}")
            rows.append((d, f"{code} ZS", "ANNUAL INSPECTION", txt, W.PEOPLE["fitter2"], 3.0))
            if r.random() < 0.18:
                d2 = d + dt.timedelta(int(r.integers(20, 90)))
                while d2.weekday() >= 5 or d2 in W.HOLIDAYS:
                    d2 += dt.timedelta(1)
                if d2 < W.EXTRACT_DATE - dt.timedelta(5):
                    t = ["Protection secondary injection test, feeder relays and transformer IDMT.",
                         "Substation battery bank replaced (110 V, 8 years old).",
                         "11 kV switchboard maintenance, breakers racked out and timed.",
                         "Earth grid test, results within limits."][int(r.integers(0, 4))]
                    rows.append((d2, f"{code} ZS", "PLANT WORK", t, W.PEOPLE["fitter2"], 6.0))
    rows.sort(key=lambda x: (x[0], x[1]))
    out = []
    seq = 41180
    for d, asset, kind, txt, who, hrs in rows:
        seq += int(r.integers(3, 29))
        site = W.SUB_NAME[asset.split("-")[0].split(" ")[0]]
        out.append([f"WO{seq}", d, site, asset, kind, txt, who, hrs])
    return out


def write_log(path, dlist, ops, cnt, R=None):
    wb = Workbook()
    ws = wb.active
    ws.title = "Closed work orders"
    rows = log_rows(dlist, ops, cnt, R)
    _sheet(ws, [], ["wo_number", "completed", "site", "asset", "work_type", "description", "completed_by",
                    "hours"], rows, [10, 11, 13, 10, 18, 110, 15, 7], date_cols=(2,))
    for row in ws.iter_rows(min_row=2, min_col=6, max_col=6):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    return len(rows)


# ---------------------------------------------------------------------------------------------
def write_bookings(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Bookings 2027-28"
    D = dt.date
    rows = [
        ["MSU2-2701", "Rangitata Lines", "Geraldine zone substation", D(2027, 4, 5), D(2027, 4, 9),
         "33 kV CB replacement", "Confirmed"],
        ["MSU2-2702", "Ellesmere Lines", "To be advised", D(2027, 4, 12), D(2027, 5, 21),
         "Zone transformer internal inspection (window 1 of 3)", "Held"],
        ["MSU2-2703", "Ashley Valley Networks", "Rangiora North zone substation", D(2027, 6, 7), D(2027, 7, 16),
         "Transformer replacement", "Confirmed"],
        ["MSU2-2704", "Rangitata Lines", "Pleasant Point zone substation", D(2027, 7, 26), D(2027, 8, 13),
         "Protection upgrade", "Provisional"],
        ["MSU2-2705", "Ellesmere Lines", "To be advised", D(2027, 8, 23), D(2027, 10, 1),
         "Zone transformer internal inspection (window 2 of 3)", "Held"],
        ["MSU2-2706", "Ashley Valley Networks", "Oxford zone substation", D(2027, 10, 18), D(2027, 11, 26),
         "33 kV bus rebuild", "Confirmed"],
        ["MSU2-2707", "Pool", "Christchurch depot", D(2027, 12, 6), D(2028, 1, 21),
         "MSU-2 annual maintenance and summer standby", "Confirmed"],
        ["MSU2-2708", "Ellesmere Lines", "To be advised", D(2028, 1, 31), D(2028, 3, 10),
         "Zone transformer internal inspection (window 3 of 3)", "Held"],
        ["MSU2-2709", "Rangitata Lines", "Temuka zone substation", D(2028, 3, 20), D(2028, 3, 31),
         "Switchroom earthing works", "Provisional"],
    ]
    for row in rows:
        row.insert(5, (row[4] - row[3]).days + 1)
    hr = _sheet(ws, ["Canterbury mobile substation pool: MSU-2 bookings, 1 April 2027 to 31 March 2028",
                     "Capacity as booked at 9 October 2026. Held windows are the network's; the site is advised "
                     "by 1 December 2026. Travel and set-up (three days each way) fall inside each window."],
                ["booking", "network", "site", "from", "to", "days", "purpose", "status"], rows,
                [11, 22, 31, 11, 11, 6, 52, 11], date_cols=(4, 5))
    ws2 = wb.create_sheet("MSU-2")
    spec = [("Unit", "MSU-2 mobile substation (two trailers: transformer, 11 kV switchroom)"),
            ("Rating", "33/11 kV, 10/15 MVA ONAN/ONAF, on-load tap changer, Dyn11"),
            ("Connection", "Plug-in 33 kV and 11 kV connection points at every pool member zone substation"),
            ("Owner", "Canterbury mobile substation pool (Ellesmere Lines, Rangitata Lines, Ashley Valley Networks)"),
            ("Bookings", "Aroha O'Brien, Ellesmere Lines maintenance planning, for the pool")]
    for i, (k, v) in enumerate(spec, 1):
        ws2.cell(row=i, column=1, value=k).font = BOLD
        ws2.cell(row=i, column=2, value=v)
    ws2.column_dimensions["A"].width = 14
    ws2.column_dimensions["B"].width = 95
    wb.save(path)


# ---------------------------------------------------------------------------------------------
def write_notes(path, F):
    txt = f"""# Oil results and plant extracts: field notes

Barry Forbes, zone substation engineering. Pulled on 16 October 2026 for the 2027/28 inspection
slate. These notes say what each field is; the rules we work to are in ES-DGA-02.

## {F['main']}

Main-tank oil results from Waihora Laboratories, one row per issue of a laboratory report.

- `sample_id`: the laboratory's number for the syringe.
- `transformer_id`: our asset number, substation code and position.
- `sampled`: date and time the sample was drawn, New Zealand time, as written on the label.
- `date`: date the laboratory analysed the sample.
- `report_no`, `issue`: the laboratory report and its issue number. A corrected report keeps the sample
  ID and report number and carries the next issue number.
- `H2`, `CH4`, `C2H6`, `C2H4`, `C2H2`, `CO`, `CO2`, `O2`, `N2`: dissolved gases, ppm (uL/L). A result
  below the laboratory's limit of detection is written as `<` followed by the limit.
- `moisture_ppm`: water content, mg/kg, coulometric titration to IEC 60814.
- `oil_temp_c`: the top-oil temperature written on the label by the technician; blank where none was
  written.
- `sample_point`: the valve the sample was drawn from.

## {F['counters']}

- `date`, `transformer_id`
- `tap_ops_counter`: the tap changer's operations counter as read by SCADA at 00:00 on `date`. The
  counter has five digits.

## {F['topoil']}

Historian export, one row per transformer per hour.

- `timestamp`: start of the hour.
- `top_oil_c`: mean top-oil temperature over the hour, degrees C.
- `load_mva`: mean load over the hour, MVA. A transformer out of service reads zero.

## {F['register']}

Asset management system extract, one row per transformer in service, and the substations.

## {F['log']}

Closed work orders on zone substation plant since January 2019, as the crews entered them.

## {F['bookings']}

The pool's MSU-2 booking sheet for April 2027 to March 2028.

## {F['relay']}

Operations recorded by the feeder and incomer protection relays, from the relay event download.

## {F['thermal']}

The March 2026 infrared survey of the 11 kV switchboards.
"""
    with open(path, "w", newline="\n") as fh:
        fh.write(txt)


def write_extract_log(path, F, counts):
    lines = [
        "ELLESMERE LINES   asset data extract   job AM-EXT-0412",
        "run 16/10/2026 06:40   operator asimpson   host amrpt02",
        "",
        "source                      object                                   file                                          rows",
        f"LIMS Waihora Laboratories   results, main tank, from 01/01/2021      {F['main']:<45} {counts['main']}",
        f"SCADA historian             ZS_TX*.TAPCOUNT daily at 00:00           {F['counters']:<45} {counts['counters']}",
        f"SCADA historian             ZS_TX*.TOPOIL, ZS_TX*.MVA hourly mean    {F['topoil']:<45} {counts['topoil']}",
        f"AMS                         assets: zone transformers, substations   {F['register']:<45} {counts['register']}",
        f"AMS                         work orders closed, ZS plant, from 2019  {F['log']:<45} {counts['log']}",
        f"Relay event download        feeder and incomer relays 2025-26        {F['relay']:<45} {counts['relay']}",
        "",
        f"documents copied: {F['standard']}, {F['bookings']}, {F['thermal']}, {F['notes']}",
        "historian tags: hourly means and 00:00 counter values to the run date",
        "job completed 06:52, 0 warnings",
    ]
    with open(path, "w", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------------------------
def write_relay_events(path):
    """Feeder and incomer relay operations, 2025 and 2026 (to the extract)."""
    r = rng(5)
    causes = ["Tree contact", "Bird", "Possum", "Vehicle vs pole", "Lightning", "Wind, clashing conductors",
              "Unknown, patrolled nothing found", "Irrigator contact", "Equipment failure, insulator"]
    rows = []
    d = dt.datetime(2025, 1, 1)
    end = dt.datetime(2026, 10, 15, 23, 59)
    while True:
        d = d + dt.timedelta(hours=float(r.exponential(23.0)))
        if d > end:
            break
        code, name = W.SUBSTATIONS[int(r.integers(0, len(W.SUBSTATIONS)))]
        fdr = f"{code} F{int(r.integers(1, 7))}"
        el = ["51 OC", "51N EF", "50 HS OC", "51N EF", "SEF"][int(r.integers(0, 5))]
        cur = int(r.integers(180, 2400)) if el != "SEF" else int(r.integers(4, 30))
        ph = ["A-B", "B-C", "A-N", "B-N", "C-N", "A-B-C"][int(r.integers(0, 6))]
        cause = causes[int(r.integers(0, len(causes)))]
        t = d.replace(microsecond=0)
        rows.append([t.strftime("%d/%m/%Y %H:%M:%S"), name, fdr, "Feeder relay", el, "Trip", cur, ph, cause])
        if r.random() < 0.7:
            t2 = t + dt.timedelta(seconds=int(r.integers(5, 30)))
            ok = r.random() < 0.8
            rows.append([t2.strftime("%d/%m/%Y %H:%M:%S"), name, fdr, "Feeder relay", "79 AR",
                         "Reclose" if ok else "Lockout", "", "", cause])
        if cur > 1800 and r.random() < 0.5:
            rows.append([(t + dt.timedelta(milliseconds=0)).strftime("%d/%m/%Y %H:%M:%S"), name,
                         f"{code} T{int(r.integers(1, 3))} incomer", "Incomer relay", "51 OC", "Pickup", cur,
                         ph, cause])
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["event_time", "substation", "bay", "relay", "element", "event", "fault_current_a",
                     "phases", "cause"])
        wr.writerows(rows)
    return len(rows)


def thermal_findings():
    """Eleven findings from the March 2026 survey: hottest spot to the whole degree, rise to a tenth."""
    r = rng(6)
    comps = ["CB 2 cable box, red phase lug", "Busbar chamber, joint B2/B3", "Incomer CB, rear spout, blue phase",
             "Feeder CB 4 cable termination", "VT fuse carrier, yellow phase", "33 kV incoming bushing clamp",
             "Bus section CB, front spout", "Feeder CB 1 cable lug, white phase"]
    out = []
    picks = sorted(r.choice(len(W.SUBSTATIONS), size=11, replace=False))
    rises = [4.3, 6.2, 7.6, 9.1, 12.9, 15.4, 23.8, 5.3, 9.7, 10.4, 29.2]
    for n, k in enumerate(picks, 1):
        code, name = W.SUBSTATIONS[int(k)]
        comp = comps[int(r.integers(0, len(comps)))]
        rise = rises[n - 1]
        mx = int(round(18 + rise + float(r.uniform(0, 6))))
        load = int(r.integers(60, 340))
        pri = 4 if rise < 10 else (3 if rise < 20 else 2)
        out.append([f"F{n:02d}", name, "11 kV switchroom" if "33 kV" not in comp else "33 kV yard", comp,
                    str(mx), f"{rise:.1f}", str(load), str(pri)])
    return out


# ---------------------------------------------------------------------------------------------
STAMP_ISO = "2026-10-16T06:40:00Z"


def rewrite_ooxml(path, creator, stamp_iso=STAMP_ISO, zip_time=(2026, 10, 16, 6, 40, 0)):
    """Pin the container: entry times, created/modified and the author, so two builds give the same
    bytes."""
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                s = data.decode("utf8")
                s = re.sub(r"<dc:creator>.*?</dc:creator>", f"<dc:creator>{creator}</dc:creator>", s)
                s = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>",
                           f"<cp:lastModifiedBy>{creator}</cp:lastModifiedBy>", s)
                s = re.sub(r"(<dcterms:created[^>]*>).*?(</dcterms:created>)", rf"\g<1>{stamp_iso}\g<2>", s)
                s = re.sub(r"(<dcterms:modified[^>]*>).*?(</dcterms:modified>)", rf"\g<1>{stamp_iso}\g<2>", s)
                data = s.encode("utf8")
            if item.filename == "docProps/app.xml":
                s = data.decode("utf8")
                app = "Microsoft Excel" if path.endswith(".xlsx") else "Microsoft Office Word"
                s = re.sub(r"<Application>.*?</Application>", f"<Application>{app}</Application>", s)
                s = re.sub(r"<AppVersion>.*?</AppVersion>", "<AppVersion>16.0300</AppVersion>", s)
                data = s.encode("utf8")
            zi = zipfile.ZipInfo(item.filename, date_time=zip_time)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zout.writestr(zi, data)
    shutil.move(tmp, path)
