"""Cut target/ from the clean truth: each file as the system that keeps it would export it."""
import csv
import datetime as dt
import io
import math
import os

import numpy as np

import postprocess as PP
import world as W

STAMP = dt.datetime(2026, 11, 9, 16, 42)      # the folder as the trust's programme manager assembled it


def _csv(path, header, rows, crlf=True):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def uk_clock(utc):
    """The UK wall-clock reading for a UTC hour (the station logger keeps clock time)."""
    off = 1 if _bst(utc) else 0
    return utc + dt.timedelta(hours=off)


def _bst(utc):
    y = utc.year

    def last_sunday(m):
        d = dt.date(y, m, 31)
        while d.weekday() != 6:
            d -= dt.timedelta(1)
        return d
    return dt.datetime.combine(last_sunday(3), dt.time(1)) <= utc < dt.datetime.combine(last_sunday(10), dt.time(1))


def fmt_t(t):
    return t.strftime("%d/%m/%Y %H:%M")


# --------------------------------------------------------------------------------------------- buoy
def buoy(out, lk, sd):
    r = W.rng(20)
    gaps = {dt.date(2024, 11, 19), dt.date(2024, 11, 20), dt.date(2025, 3, 11), dt.date(2025, 3, 12),
            dt.date(2025, 3, 13), dt.date(2026, 2, 4)}
    rows = []
    for i, d in enumerate(W.DAYS):
        if d in gaps:
            continue
        for j, z in enumerate(W.DEPTHS):
            rows.append([d.isoformat(), ("%.1f" % z) if z < 1 else "%d" % z, "%.2f" % lk["prof"][i, j]])
    _csv(os.path.join(out, "fellside_buoy_thermistor_daily.csv"), ["Date (UTC)", "Depth (m)", "Water temperature (degC)"], rows, crlf=False)
    rows = []
    for i, d in enumerate(W.DAYS):
        if d in gaps:
            continue
        for j, z in enumerate(W.SONDE_DEPTHS):
            chl = ("%.2f" % sd["chl"][i]) if z == 1.0 else ""
            rows.append([d.isoformat(), "%d" % z, "%.1f" % sd["cond"][i, j], "%.2f" % sd["do"][i, j], chl])
    _csv(os.path.join(out, "fellside_buoy_sondes_daily.csv"), ["Date (UTC)", "Depth (m)", "Specific conductance (uS/cm)", "Dissolved oxygen (mg/l)", "Chlorophyll (RFU)"],
         rows, crlf=False)
    return gaps


# --------------------------------------------------------------------------------------------- Lenning Foot
def station_flow(rv):
    """The station's flow column: the Lenning Bridge telemetry feed until the station's own gauge at the inlet
    took over on 1 June 2024."""
    q = rv["q"].copy()
    for h, t in enumerate(rv["hours"]):
        if t.date() < W.GAUGE_SWITCH:
            q[h] = rv["q_bridge"][h]
    return q


def station(out, rv):
    r = W.rng(21)
    q = station_flow(rv)
    val_end = dt.datetime(2026, 4, 1)
    prov_start = dt.datetime(2026, 1, 1)
    vrows, prows = [], []
    for h, t in enumerate(rv["hours"]):
        local = uk_clock(t)
        row = ["%.2f" % rv["temp"][h], "%.1f" % rv["cond"][h], "%.1f" % rv["turb"][h], "%.3f" % q[h]]
        if local < val_end:
            vrows.append([fmt_t(local)] + row)
        if local >= prov_start:
            p = list(row)
            if local < val_end and r.random() < 0.06:          # provisional values the validation later revised
                p[2] = "%.1f" % (rv["turb"][h] * (1 + r.normal(0, 0.08)))
                p[3] = "%.3f" % (q[h] * (1 + r.normal(0, 0.012)))
            prows.append([fmt_t(local)] + p)
    hdr = ["Timestamp (UK)", "Water temp (C)", "Conductivity (mS/m)", "Turbidity (NTU)", "Flow (m3/s)"]
    _csv(os.path.join(out, "lenning_foot_hourly_validated.csv"), hdr, vrows)
    _csv(os.path.join(out, "lenning_foot_hourly_provisional.csv"), hdr, prows)


def sampler_file(out, rv, sm):
    r = W.rng(22)
    hours = rv["hours"]
    rows = []
    allb = [b for b in sm["day"]] + [b for b in sm["storm"]]
    allb.sort(key=lambda b: (b["h0"], 0 if b["kind"] == "DAY" else 1))
    lab = 26104118
    for k, b in enumerate(allb):
        first = uk_clock(hours[b["h0"]])
        last = uk_clock(hours[b["h1"] - 1])
        lab += int(r.integers(1, 4))
        bottle = ("D%s" % first.strftime("%y%m%d")) if b["kind"] == "DAY" else ("S%s-%02d" % (first.strftime("%y%m%d%H"), k % 97))
        tp = b["tp"]
        srp = b["srp"]
        rows.append(["LF%d" % lab, bottle, b["kind"], fmt_t(first), fmt_t(last), len(b["sub"]),
                     "%d" % round(tp), "%d" % round(min(srp, tp))])
    _csv(os.path.join(out, "lenning_foot_sampler_results.csv"),
         ["Lab ref", "Bottle", "Programme", "First sub-sample (UK)", "Last sub-sample (UK)", "Sub-samples",
          "TP (ug/l)", "SRP (ug/l)"], rows)


def regulator(out, rv):
    """The regulator's hourly mean flows at its two gauges above the confluence, to the end of September 2026."""
    r = W.rng(23)
    rows = []
    end = dt.datetime(2026, 10, 1)
    for name, ref, series in (("LENNING BRIDGE", "76012", rv["q_bridge"]), ("BRANKELL BECK AT HOWE", "76019", rv["q_brankell"])):
        for h, t in enumerate(rv["hours"]):
            if t >= end:
                break
            qual = "G" if r.random() > 0.004 else "E"
            rows.append([name, ref, t.strftime("%Y-%m-%dT%H:%M:%SZ"), "%.3f" % series[h], qual])
    _csv(os.path.join(out, "regulator_gauged_flows_hourly.csv"),
         ["station_name", "station_ref", "datetime", "mean_flow_m3s", "quality"], rows, crlf=False)


# --------------------------------------------------------------------------------------------- works returns
def months_of(y0):
    """Reporting year April y0 to March y0+1 (the first held year starts in October 2023)."""
    out = []
    m, y = 4, y0
    for _ in range(12):
        out.append((y, m))
        m += 1
        if m == 13:
            m, y = 1, y + 1
    return out


def works_monthly(wk):
    r = W.rng(24)
    rec = {}
    for name in ("Brathwick", "Hollinsby"):
        for i, d in enumerate(W.DAYS):
            key = (name, d.year, d.month)
            rec.setdefault(key, []).append(i)
    rows = {}
    for (name, y, m), idx in sorted(rec.items()):
        if (y, m) > (2026, 9) or (y, m) < (2023, 10):
            continue
        f = wk[name]["flow"][idx]
        vol = float(f.sum())
        nsamp = int(r.integers(9, 13)) if name == "Hollinsby" else int(r.integers(4, 7))
        pick = sorted(r.choice(len(idx), size=min(nsamp, len(idx)), replace=False))
        tp = float(np.mean([wk[name]["tp"][idx[k]] for k in pick]))
        tp = round(tp, 2)
        load = round(vol * tp / 1000.0, 1)
        temp = round(float(wk[name]["temp"][idx].mean()), 1)
        rows[(name, y, m)] = dict(vol=int(round(vol)), n=len(pick), tp=tp, load=load, temp=temp)
    return rows


def returns_xlsx(out, monthly):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    wb.remove(wb.active)
    permits = {"Brathwick": "EPR/NB3127KM", "Hollinsby": "EPR/NB3096LP"}
    for y0 in (2023, 2024, 2025, 2026):
        ws = wb.create_sheet("%d-%02d" % (y0, (y0 + 1) % 100))
        new = y0 >= 2025
        ws.append(["Fellmoor Water - wastewater treatment works monthly returns, reporting year %d/%02d" % (y0, (y0 + 1) % 100)])
        ws.append([])
        if not new:
            hdr = ["Site", "Permit ref", "Month", "Final effluent volume (m3)", "TP samples (no.)", "TP mean (mg/l)",
                   "TP load (kg)", "Final effluent temperature (deg C)"]
        else:
            hdr = ["Period", "Works", "Permit", "FE temp mean (C)", "FE volume m3", "TP mean mg/l", "TP samples",
                   "TP load kg"]
        ws.append(hdr)
        for c in ws[3]:
            c.font = Font(bold=True)
        for name in ("Brathwick", "Hollinsby"):
            for (y, m) in months_of(y0):
                k = (name, y, m)
                if k not in monthly:
                    continue
                v = monthly[k]
                if not new:
                    ws.append(["%s WwTW" % name, permits[name], dt.date(y, m, 1).strftime("%b-%y"), v["vol"], v["n"],
                               v["tp"], v["load"], v["temp"]])
                else:
                    ws.append(["%d-%02d" % (y, m), name.upper(), permits[name], v["temp"], v["vol"], v["tp"], v["n"],
                               v["load"]])
        ws.column_dimensions["A"].width = 18
    p = os.path.join(out, "fellmoor_wwtw_monthly_returns.xlsx")
    wb.save(p)
    PP.normalize_ooxml(p, "Oliver Thomas", "Oliver Thomas", "2026-10-30T09:12:00Z", "2026-11-04T14:05:00Z",
                       excel=True, company="Fellmoor Water")


# --------------------------------------------------------------------------------------------- outfall
def outfall_xlsx(out, of):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    r = W.rng(25)
    wb = Workbook()
    ws = wb.active
    ws.title = "Daily"
    ws.append(["Mill Beck outfall (Hollinsby) - logger daily totals"])
    ws.append(["Date", "Volume (m3)", "Mean water temp (C)"])
    for c in ws[2]:
        c.font = Font(bold=True)
    end = dt.date(2026, 9, 30)
    for i, d in enumerate(W.DAYS):
        if d > end:
            break
        ws.append([d, round(float(of["vol"][i]), 1), round(float(of["temp"][i]), 1)])
    for row in ws.iter_rows(min_row=3, max_col=1):
        for c in row:
            c.number_format = "dd/mm/yyyy"
    ws2 = wb.create_sheet("Monthly loads")
    ws2.append(["Month", "Volume (m3)", "TP flow-weighted (mg/l)", "TP load (kg)", "Event composites", "Dry-weather samples"])
    for c in ws2[1]:
        c.font = Font(bold=True)
    bym = {}
    for i, d in enumerate(W.DAYS):
        if d > end:
            break
        bym.setdefault((d.year, d.month), []).append(i)
    monthly = {}
    for (y, m), idx in sorted(bym.items()):
        if (y, m) < (2023, 10):
            continue
        vol = float(of["vol"][idx].sum())
        load = float(of["load"][idx].sum())
        monthly[(y, m)] = round(load, 1)
        ws2.append([dt.date(y, m, 1).strftime("%b %Y"), int(round(vol)), round(load * 1000 / vol, 3), round(load, 1),
                    int(of["wet"][idx].sum()), 2 if r.random() < 0.7 else 1])
    p = os.path.join(out, "mill_beck_outfall_monitoring.xlsx")
    wb.save(p)
    PP.normalize_ooxml(p, "Debra Rose", "Debra Rose", "2025-01-06T10:20:00Z", "2026-10-21T11:47:00Z",
                       excel=True, company="Selwith Water Trust")
    return monthly


# --------------------------------------------------------------------------------------------- Connect Right
CLASS = {"House": None, "Block": "PP", "Flat": "RD06"}


def survey_files(out, sv):
    r = W.rng(26)
    rows = []
    for p in sv["props"]:
        if p["kind"] == "House":
            cls = ["RD02", "RD03", "RD04"][int(r.integers(0, 3))]
        else:
            cls = CLASS[p["kind"]]
        rows.append([p["uprn"], p["parent"], p["addr"].upper(), cls, "HOLLINSBY", p["run"]])
    rows.sort(key=lambda x: x[0])
    _csv(os.path.join(out, "hollinsby_address_register_extract.csv"),
         ["UPRN", "PARENT_UPRN", "ADDRESS", "CLASS", "TOWN", "SW_DRAIN_RUN"], rows)
    byu = {p["uprn"]: p for p in sv["props"]}
    rows = []
    initials = ["CN", "VD", "CN", "ZS", "VD", "MW"]
    n = 4100
    for v in sv["visits"]:
        n += int(r.integers(1, 3))
        ref = "CR-%s-%04d" % (v["day"].strftime("%y%m%d"), n % 10000)
        addr = byu[v["uprn"]]["addr"]
        if r.random() < 0.3:
            addr = addr.replace(" Road", " Rd").replace(" Lane", " Ln")
        rows.append([ref, v["uprn"], addr, v["sync"].strftime("%d/%m/%Y"), v["outcome"], v["appliance"],
                     initials[int(r.integers(0, len(initials)))]])
    _csv(os.path.join(out, "connect_right_visits_export.csv"),
         ["Visit ref", "UPRN", "Address as recorded", "Uploaded", "Outcome", "Appliance", "Surveyor"], rows)


# --------------------------------------------------------------------------------------------- laboratory
def lab_file(out, labrows):
    r = W.rng(27)
    rows = []
    n = 25301877
    for x in labrows:
        d = x["day"]
        if x["site"] == "north":
            code = "NB" if d < dt.date(2025, 4, 1) else "SWL01"
        else:
            code = "NB"
        n += int(r.integers(1, 5))
        rows.append(["FLL%d" % n, code, d.strftime("%d-%b-%Y"), x["depth"], "Total phosphorus", "%.1f" % x["tp"], "ug/l", ""])
        if x["chl"] is not None:
            v = x["chl"]
            q = "<" if v < 1.0 else ""
            rows.append(["FLL%d" % n, code, d.strftime("%d-%b-%Y"), x["depth"], "Chlorophyll a", "%.1f" % max(v, 1.0),
                         "ug/l", q])
    _csv(os.path.join(out, "fellside_lake_lab_results.csv"),
         ["lab_ref", "site", "sampled", "depth_m", "determinand", "result", "unit", "qualifier"], rows)


# --------------------------------------------------------------------------------------------- distractors
def bathing_file(out, bt):
    rows = [["HOLLINSBY BEACH", b["day"].strftime("%d/%m/%Y"), b["ec"], b["ie"]] for b in bt]
    _csv(os.path.join(out, "hollinsby_beach_bathing_results.csv"),
         ["Bathing water", "Sample date", "E. coli (cfu/100ml)", "Intestinal enterococci (cfu/100ml)"], rows)


def farmyard_xlsx(out, fy):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Holdings"
    ws.append(["Holding", "CPH", "Sub-catchment", "Cattle", "Sheep", "Yard area (m2)", "Yard roofed (%)",
               "Slurry storage (months)"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for f in fy:
        ws.append([f["holding"], f["cph"], f["sub"], f["cattle"], f["sheep"], f["yard_m2"], f["roofed_pct"],
                   f["slurry_months"]])
    p = os.path.join(out, "lenning_farm_yard_survey_2025.xlsx")
    wb.save(p)
    PP.normalize_ooxml(p, "Debra Rose", "Debra Rose", "2025-08-14T08:55:00Z", "2025-09-02T16:10:00Z",
                       excel=True, company="Selwith Water Trust")


# --------------------------------------------------------------------------------------------- appraisals
APPRAISALS = [
    ("A", "Lenning farm infrastructure programme", "Phosphorus lost from farms in the Lenning catchment",
     "Selwith Water Trust with the farm advisory service", 1248000, "May 2027", 30,
     "Yard roofing, clean and dirty water separation and slurry store covers on 14 holdings"),
    ("B", "Brathwick WwTW chemical phosphorus removal", "Brathwick works final effluent",
     "Fellmoor Water (trust contribution)", 1176000, "April 2027", 82,
     "Ferric dosing and a new 1.0 mg/l permit"),
    ("C", "Hollinsby WwTW tertiary filtration", "Hollinsby works final effluent",
     "Fellmoor Water (trust contribution)", 1337000, "May 2027", 71,
     "Tertiary sand filter, design effluent 0.25 mg/l"),
    ("D", "Mill Beck outfall treatment wetland", "Mill Beck surface-water outfall",
     "Selwith Water Trust with the district council", 612000, "May 2027", 50,
     "Constructed wetland between the outfall and the shore"),
]


def appraisal_xlsx(out):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Shortlist"
    ws.append(["Programme", "Title", "Source it acts on", "Lead", "Capital cost (GBP)", "Operating by",
               "Credited phosphorus reduction (% of source)", "Scope"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for a in APPRAISALS:
        ws.append(list(a))
    ws.column_dimensions["B"].width = 40
    ws.column_dimensions["C"].width = 44
    p = os.path.join(out, "programme_appraisals_2027.xlsx")
    wb.save(p)
    PP.normalize_ooxml(p, "Debra Rose", "Debra Rose", "2026-09-22T13:30:00Z", "2026-10-28T09:41:00Z",
                       excel=True, company="Selwith Water Trust")


# --------------------------------------------------------------------------------------------- documents
def _pdf(path, title, author, blocks, created, modified):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    from reportlab.lib import colors
    st = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=8)
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=4)
    sm = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject="", creator="")
    flow = []
    for kind, val in blocks:
        if kind == "h1":
            flow.append(Paragraph(val, h1))
        elif kind == "h2":
            flow.append(Paragraph(val, h2))
        elif kind == "p":
            flow.append(Paragraph(val, st))
        elif kind == "small":
            flow.append(Paragraph(val, sm))
        elif kind == "sp":
            flow.append(Spacer(1, val))
        elif kind == "table":
            t = Table(val, hAlign="LEFT")
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.6), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.6),
                                   ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            flow.append(t)
    def _meta(c, d):
        c.setProducer("Microsoft\xae Word for Microsoft 365")
        c.setCreator("Microsoft\xae Word for Microsoft 365")
    doc.build(flow, onFirstPage=_meta, onLaterPages=_meta)
    PP.normalize_pdf(path, created, modified)


def fund_rules(out):
    blocks = [
        ("small", "Selwith Water Trust  |  Registered charity no. 1187245  |  Issued 3 November 2026"),
        ("h1", "Selwith Recovery Fund: rules for the 2027 award"),
        ("h2", "1. The fund"),
        ("p", "1.1 The Selwith Recovery Fund holds GBP 1.38 million granted to the trust under the lakes recovery "
              "programme for one capital programme that reduces the phosphorus feeding the summer algal blooms in "
              "Selwith Water."),
        ("p", "1.2 The fund backs one programme in 2027. The trustees choose it at their meeting on 26 November 2026 "
              "from the shortlist in the programme appraisal (programme_appraisals_2027.xlsx)."),
        ("h2", "2. How the shortlisted programmes are compared"),
        ("p", "2.1 Programmes are compared on the phosphorus each keeps out of the lake's surface water between "
              "1 June and 30 September. The surface water is the water from the surface down to 5 metres, in which "
              "the summer blooms grow and from which the trust takes its bloom samples."),
        ("p", "2.2 The phosphorus a programme keeps out in a season is the reduction its appraisal credits it with, "
              "applied to the phosphorus its source added to the surface water between 1 June and 30 September of "
              "that season."),
        ("p", "2.3 Programmes are judged on the 2024, 2025 and 2026 seasons. The figure compared is the average of "
              "the three seasons, in kilograms of phosphorus."),
        ("p", "2.4 Inputs are taken as measured by the monitoring the trust and its partners hold: the Lenning Foot "
              "station and sampler, Fellmoor Water's monthly returns for the Brathwick and Hollinsby works, and the "
              "trust's Mill Beck outfall monitoring."),
        ("h2", "3. Conditions of the award"),
        ("p", "3.1 The chosen programme must be operating by 31 May 2027. The lead partner reports progress to the "
              "trustees each quarter until it is commissioned."),
        ("p", "3.2 Where a partner contributes to a programme, the award is paid against certified stages of the "
              "work and the trust's contribution is capped at the fund's balance."),
        ("p", "3.3 The trust publishes the trustees' decision, the comparison behind it and the programme's "
              "reporting on its website."),
        ("sp", 8),
        ("small", "Approved by the trustees on 29 October 2026. Contact: Debra Rose, catchment programme manager."),
    ]
    _pdf(os.path.join(out, "selwith_recovery_fund_rules_2027.pdf"), "Selwith Recovery Fund: rules for the 2027 award",
         "Selwith Water Trust", blocks, b"D:20261103101500+00'00'", b"D:20261103101500+00'00'")


def recovery_plan(out):
    blocks = [
        ("small", "Selwith Water Trust with the Fellside Lake Laboratory  |  March 2025"),
        ("h1", "Selwith Water lake recovery plan 2025 to 2030"),
        ("h2", "1. The lake and its catchment"),
        ("p", "Selwith Water is 4.6 km long and covers 3.1 square kilometres, with a maximum depth of 29 m over the "
              "north basin and a mean depth of 12 m; it holds about 37 million cubic metres. Its main inflow is the "
              "River Lenning, which drains 74 square kilometres of fell and farmland at the head of the valley and "
              "enters the lake at Lenning Foot; the Brankell Beck joins the Lenning 600 m above the lake. The village of "
              "Brathwick, 5 km up the Lenning, is served by a small works discharging to the river. The town of "
              "Hollinsby stands at the south end; its works discharges through an outfall into the south basin, and "
              "its surface-water drains reach the lake at the Mill Beck outfall. The lake drains south over the outflow weir."),
        ("h2", "2. The problem"),
        ("p", "Cyanobacteria blooms have formed in the lake's surface water in every summer since 2019, with scums "
              "closing Hollinsby beach on 19 days in 2023. The laboratory's north basin results show summer surface "
              "chlorophyll a well above the level at which the lake would meet good ecological status, and the "
              "growing-season total phosphorus in the surface water has stayed above 25 micrograms per litre."),
        ("h2", "3. Targets"),
        ("table", [["Measure (north basin surface water, June to September mean)", "2023", "Target 2030"],
                   ["Total phosphorus (ug/l)", "27.1", "20"],
                   ["Chlorophyll a (ug/l)", "7.3", "5"],
                   ["Beach closure days", "19", "0"]]),
        ("sp", 6),
        ("h2", "4. Monitoring"),
        ("p", "The laboratory samples the north basin buoy site (code NB) fortnightly from April to October and "
              "monthly in winter, as a 0 to 5 m tube sample and a 20 m bottle. The buoy logs water temperature at "
              "1 m intervals and conductivity, oxygen and chlorophyll fluorescence at fixed depths. The trust and the "
              "laboratory run a monitoring station and sampler at Lenning Foot. Fellmoor Water supplies monthly "
              "returns for both works, and the trust logs the Mill Beck outfall."),
        ("h2", "5. Measures"),
        ("p", "The plan's measures are to be funded as money becomes available: a farm infrastructure programme in "
              "the Lenning catchment, phosphorus removal at Brathwick works, tertiary treatment at Hollinsby works, "
              "a wetland on the Mill Beck outfall, and a review of misconnected drains in Hollinsby under the "
              "Connect Right survey."),
    ]
    _pdf(os.path.join(out, "selwith_lake_recovery_plan_2025.pdf"), "Selwith Water lake recovery plan 2025 to 2030",
         "Selwith Water Trust", blocks, b"D:20250318094000+00'00'", b"D:20250321161200+00'00'")


def cover_note(out):
    txt = (
        "From: Oliver Thomas <oliver.thomas@fellmoorwater.co.uk>\r\n"
        "To: Debra Rose <debra.rose@selwithwatertrust.org.uk>\r\n"
        "Date: Wed, 04 Nov 2026 14:22:51 +0000\r\n"
        "Subject: Brathwick and Hollinsby returns to end of September\r\n"
        "Message-ID: <20261104142251.7731@fellmoorwater.co.uk>\r\n"
        "MIME-Version: 1.0\r\n"
        "Content-Type: text/plain; charset=utf-8\r\n"
        "\r\n"
        "Hi Debra,\r\n\r\n"
        "Attached are the monthly returns for Brathwick and Hollinsby from October 2023 to the end of\r\n"
        "September, one tab per reporting year.\r\n\r\n"
        "Happy to talk through the tertiary filter design for Hollinsby before the trustees meet, and the\r\n"
        "dosing trial we ran at Brathwick in 2022 if that helps the appraisal.\r\n\r\n"
        "Thanks,\r\n\r\n"
        "Oliver Thomas\r\nCatchment Scientist, Fellmoor Water\r\n")
    with open(os.path.join(out, "fellmoor_returns_cover_note.eml"), "w", newline="", encoding="utf-8") as f:
        f.write(txt)


def stamp_all(out):
    t = STAMP.timestamp()
    for root, _, files in os.walk(out):
        for fn in files:
            os.utime(os.path.join(root, fn), (t, t))


def cut(out, S):
    os.makedirs(out, exist_ok=True)
    buoy(out, S["lake"], S["sondes"])
    station(out, S["river"])
    sampler_file(out, S["river"], S["sampler"])
    regulator(out, S["river"])
    returns_xlsx(out, S["monthly"])
    S["outfall_monthly"] = outfall_xlsx(out, S["outfall"])
    survey_files(out, S["survey"])
    lab_file(out, S["lab"])
    bathing_file(out, S["bathing"])
    farmyard_xlsx(out, S["farmyards"])
    appraisal_xlsx(out)
    fund_rules(out)
    recovery_plan(out)
    cover_note(out)
    stamp_all(out)
