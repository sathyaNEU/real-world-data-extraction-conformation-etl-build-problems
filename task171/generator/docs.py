"""The documents and smaller extracts of task171's pack: rate schedules (PDF), the rates committee paper (DOCX),
the CRM request export (XLSX), the billing summary, EV charger rebates, degree days, the dictionary and the
export manifest. Fixed timestamps so two builds are byte-identical."""
from __future__ import annotations

import datetime as dt
import os
import zipfile

import numpy as np
import pandas as pd

import common as C

FIXED = dt.datetime(2026, 11, 20, 7, 42, 0)


# ---------------------------------------------------------------- rate schedules (PDF)
def sched_text():
    r1 = C.R1_HIST
    t = C.RTOU_HIST
    o = C.RON_2027
    pages = []
    pages.append(("Sablewood Electric Cooperative", [
        "Residential rate schedules R-1, R-TOU and R-ON",
        "Tariff book section 3, residential service. Revision 14, issued November 6, 2026. Approved by the Board of Directors on October 27, 2026 for service on and after January 1, 2027; earlier rates shown for reference.",
        "",
        "Schedule R-1  Residential Service",
        "Availability: single-phase service to a residence or a farm dwelling through one meter.",
        "Monthly rate (each bill):",
        "  Effective January 1, 2023: customer charge $%.2f; energy charge %.2f cents per kWh." % (r1[2023]["cc"], r1[2023]["e"] * 100),
        "  Effective January 1, 2024: customer charge $%.2f; energy charge %.2f cents per kWh." % (r1[2024]["cc"], r1[2024]["e"] * 100),
        "  Effective January 1, 2025: customer charge $%.2f; energy charge %.2f cents per kWh." % (r1[2025]["cc"], r1[2025]["e"] * 100),
        "  Effective January 1, 2027: customer charge $%.2f; energy charge %.2f cents per kWh." % (r1[2027]["cc"], r1[2027]["e"] * 100),
        "Power cost adjustment, taxes and the franchise fee are billed under Riders PCA-1 and TX-2 on every residential schedule alike and are not part of this schedule.",
        "",
        "Schedule R-TOU  Residential Time-of-Use (Evening Peak)",
        "Availability: offered from March 1, 2024 to members served under Schedule R-1. Closed to new service after December 31, 2026; members on R-TOU on that date may stay on it.",
        "On-peak hours: 4:00 p.m. to 9:00 p.m. every day, prevailing local time. All other hours are off-peak.",
        "Monthly rate (each bill):",
        "  Effective March 1, 2024: customer charge $%.2f; on-peak energy %.2f cents per kWh; off-peak energy %.2f cents per kWh." % (t[2024]["cc"], t[2024]["peak"] * 100, t[2024]["other"] * 100),
        "  Effective January 1, 2025: customer charge $%.2f; on-peak energy %.2f cents per kWh; off-peak energy %.2f cents per kWh." % (t[2025]["cc"], t[2025]["peak"] * 100, t[2025]["other"] * 100),
        "  Rates for 2027 are unchanged from 2025 for members remaining on the schedule.",
    ]))
    pages.append(("Sablewood Electric Cooperative  -  tariff book section 3, revision 14", [
        "Schedule R-ON  Residential Overnight",
        "Availability: offered from January 1, 2027 to members served under Schedule R-1.",
        "Off-peak hours: 11:00 p.m. to 6:00 a.m. every day, prevailing local time. All other hours are on-peak.",
        "Monthly rate (each bill):",
        "  Effective January 1, 2027: customer charge $%.2f; off-peak energy %.2f cents per kWh; on-peak energy %.2f cents per kWh." % (o["cc"], o["off"] * 100, o["other"] * 100),
        "",
        "General terms for the optional residential schedules",
        "1. A member requests a schedule change in writing, online or by telephone. The change takes effect at the member's next scheduled meter read after the request is processed, and the first bill on the new schedule covers the period that begins at that read.",
        "2. A member may change residential schedules once in any twelve months.",
        "3. Billing determinants for the time-of-use periods are the interval data recorded by the member's meter and summed by the meter data management system to the cooperative's load-research periods.",
        "",
        "Load-research periods (prevailing local time): 11:00 p.m. to 6:00 a.m.; 6:00 a.m. to 4:00 p.m.; 4:00 p.m. to 9:00 p.m.; 9:00 p.m. to 11:00 p.m. These are the periods of the wholesale power contract's demand and energy billing and are used by every time-of-use schedule.",
    ]))
    return pages


def write_pdf(path, pages):
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import simpleSplit
    c = canvas.Canvas(path, pagesize=letter, invariant=1, pageCompression=1)
    c.setAuthor("Sablewood Electric Cooperative"); c.setTitle("Residential rate schedules"); c.setSubject("Tariff book section 3, revision 14"); c.setCreator("Tariff book"); c.setProducer("Tariff book")
    for head, lines in pages:
        y = 740
        c.setFont("Helvetica-Bold", 12); c.drawString(54, y, head); y -= 24
        for ln in lines:
            bold = ln.startswith("Schedule ") or ln.startswith("General terms") or ln.startswith("Residential rate")
            c.setFont("Helvetica-Bold" if bold else "Helvetica", 9.5)
            for part in (simpleSplit(ln, "Helvetica", 9.5, 500) or [""]):
                c.drawString(54, y, part); y -= 13
            if bold:
                y -= 2
        c.setFont("Helvetica", 8); c.drawString(54, 40, "Sablewood Electric Cooperative  |  Tariff book section 3  |  Revision 14")
        c.showPage()
    c.save()
    raw = open(path, "rb").read()
    for a in (b"ReportLab Generated PDF document http://www.reportlab.com", b"ReportLab PDF Library - www.reportlab.com", b"ReportLab"):
        while a in raw:
            rep = b"Sablewood tariff book"[:len(a)].ljust(len(a))
            raw = raw.replace(a, rep, 1)
    raw = raw.replace(b"D:20000101000000+00'00'", b"D:20261106093000-06'00'")
    open(path, "wb").write(raw)


# ---------------------------------------------------------------- the rates committee paper (DOCX)
PLAN = [
    ("h", "R-ON launch: enrolment and revenue forecast for the 2027 budget"),
    ("p", "Rates Committee, meeting of December 3, 2026. Paper RC-26-19 from Wendy Morris, Manager of Rate Products. Draft for the committee, November 13, 2026."),
    ("h2", "What the committee asked for"),
    ("p", "At its October meeting the committee asked for two figures to carry into the 2027 budget: how many R-1 services will have moved to Schedule R-ON by December 31, 2027, and the revenue those services give up. Bryan Castro in Finance will carry the revenue figure into the budget's residential revenue line."),
    ("p", "The forecast is of the R-1 services on the books at October 31, 2026 that were billed for all twelve billing months November 2025 to October 2026 (the test year), taken as they stand: no service is counted as closing or opening in 2027. A service has moved by a date when R-ON is in effect for it on that date. The revenue figure is a test-year figure: for each service expected to have moved by December 31, 2027, its bill on R-1 less its bill on R-ON, both on the 2027 schedules, priced on its own billed use in the test year, counted in full whatever month of 2027 the service moves."),
    ("h2", "How R-ON opens"),
    ("p", "R-ON opens on January 1, 2027 to members on R-1. It is marketed the way R-TOU was in 2024: the launch letter goes to every R-1 member in the first billing week of January, the bill insert runs on the next three billing cycles, and requests come in through the same online form, the member services line and the mail-in card. Changes take effect at the member's next scheduled read under the general terms of the tariff book. R-TOU closes to new service after December 31, 2026; members already on it may stay."),
    ("h2", "R-TOU tables for the same meeting"),
    ("p", "The committee also asked for two tables on R-TOU, which closes to new service as R-ON opens. The first gives, by district, the services on R-TOU at October 31, 2026 and the kWh they used from 4 p.m. to 9 p.m. in the billing months November 2025 to October 2026. The second gives, by district, the services that came off R-TOU between March 1, 2025 and October 31, 2026, split between those that went back to R-1 and those whose service ended while on R-TOU. Districts are the districts of the service locations."),
    ("h2", "Systems"),
    ("p", "Use comes from the load-research extract of the meter data management system, which carries every billing month from March 2023. Accounts and rate assignments come from the customer information system as at October 31, 2026; requests from the member services CRM. The CIS was upgraded on June 15, 2025, and the TOU enrolment module now writes the R-TOU rate rows."),
]


def write_docx(path, items):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10.5)
    for kind, text in items:
        if kind == "h":
            d.add_heading(text, level=1)
        elif kind == "h2":
            d.add_heading(text, level=2)
        else:
            d.add_paragraph(text)
    cp = d.core_properties
    cp.author = "Wendy Morris"; cp.last_modified_by = "Wendy Morris"; cp.title = "RC-26-19 R-ON launch forecast"
    cp.created = dt.datetime(2026, 11, 13, 15, 10); cp.modified = dt.datetime(2026, 11, 13, 16, 2); cp.revision = 3
    d.save(path)
    _normalise_zip(path)


def _normalise_zip(path):
    with zipfile.ZipFile(path) as z:
        items = [(i, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for i, data in sorted(items, key=lambda t: t[0].filename):
            if i.filename == "docProps/app.xml":
                import re as _re
                appname = b"Microsoft Excel" if path.endswith(".xlsx") else b"Microsoft Office Word"
                data = _re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + appname + b"</Application>", data)
                data = _re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
            data = data.replace(b"python-docx", b"").replace(b"openpyxl", b"").replace(b"Openpyxl", b"")
            if i.filename == "docProps/core.xml":
                import re as _re
                data = _re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>2026-11-20T07:42:00Z\g<2>", data)
                data = _re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>2026-11-13T15:10:00Z\g<2>", data)
            zi = zipfile.ZipInfo(i.filename, date_time=(2026, 11, 13, 16, 2, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def write_xlsx(path, sheets, author="Sablewood member services"):
    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, df in sheets:
        ws = wb.create_sheet(name)
        ws.append(list(df.columns))
        for row in df.itertuples(index=False):
            ws.append([None if (isinstance(v, float) and np.isnan(v)) else v for v in row])
    wb.properties.creator = author; wb.properties.lastModifiedBy = author
    wb.properties.created = FIXED; wb.properties.modified = FIXED
    wb.save(path)
    _normalise_zip(path)


# ---------------------------------------------------------------- CRM requests
from zoneinfo import ZoneInfo
LOCAL = ZoneInfo("America/Chicago")


def utc(local_naive):
    return local_naive.replace(tzinfo=LOCAL).astimezone(dt.timezone.utc).replace(tzinfo=None)

def crm_requests(P, rng):
    svc, rd = P["svc"], P["rdates"]
    rows = []
    case = 2_400_518
    for i in np.where(svc.tou_start.values >= 0)[0]:
        rdi = rd[int(svc.cyc.iat[i])]
        ts = int(svc.tou_start.iat[i])
        eff = rdi[ts + 1]
        lag = int(rng.integers(3, 26))
        rec = dt.datetime.combine(eff - dt.timedelta(days=lag), dt.time(int(rng.integers(7, 23)), int(rng.integers(0, 60)), int(rng.integers(0, 60))))
        ch = rng.choice(["Web form", "Member services line", "Mail-in card"], p=[0.58, 0.31, 0.11])
        case += int(rng.integers(1, 40))
        done = eff - dt.timedelta(days=int(rng.integers(1, max(2, lag))))
        named = svc.acct.iat[i]
        if i in P["ids"].second and rng.random() < {"Web form": 0.92, "Member services line": 0.35, "Mail-in card": 0.0}[ch]:
            named = svc.acct.iat[P["ids"].second[i]]      # the web form is keyed to the member's first service
        rows.append([case, utc(rec), ch, named, "Enrol R-TOU", "Completed", done.isoformat()])
        if ch == "Web form" and rng.random() < 0.035:
            rows.append([case + 1, utc(rec + dt.timedelta(seconds=int(rng.integers(4, 90)))), ch, named, "Enrol R-TOU", "Closed - duplicate", ""])
            case += 1
        te = int(svc.tou_end.iat[i])
        if te >= 0:
            off = rdi[te]
            lag = int(rng.integers(3, 20)); case += int(rng.integers(1, 40))
            rec = dt.datetime.combine(off - dt.timedelta(days=lag), dt.time(int(rng.integers(7, 22)), int(rng.integers(0, 60))))
            rows.append([case, utc(rec), rng.choice(["Web form", "Member services line"]), svc.acct.iat[i], "Return to R-1", "Completed", (off - dt.timedelta(days=1)).isoformat()])
    # requests that came to nothing
    cand = np.where((svc.tou_start.values < 0) & (svc.open_i.values < C.MIDX[(2026, 6)]))[0]
    for i in rng.choice(cand, int(len(rows) * 0.07), replace=False):
        case += int(rng.integers(1, 40))
        m = int(rng.integers(C.OFFER_A, len(C.MONTHS)))
        y, mo = C.MONTHS[m]
        rec = dt.datetime(y, mo, int(rng.integers(1, 28)), int(rng.integers(7, 23)), int(rng.integers(0, 60)))
        rows.append([case, utc(rec), rng.choice(["Web form", "Member services line", "Mail-in card"]), svc.acct.iat[i],
                     "Enrol R-TOU", rng.choice(["Cancelled by member", "Cancelled - not eligible"], p=[0.8, 0.2]), ""])
    df = pd.DataFrame(rows, columns=["case_no", "received_utc", "channel", "service_acct", "request", "status", "completed_on"])
    df = df.sort_values(["received_utc", "case_no"]).reset_index(drop=True)
    df["received_utc"] = df.received_utc.dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return df


def billing_summary(W, P):
    svc, use, on_tou = W["svc"], W["use"], W["on_tou"]
    off_of = {"Sedge Flats": "Sedge Flats", "Brisco Bend": "Brisco Bend", "Kessel Mill": "Kessel Mill", "Pike Ridge": "Pike Ridge", "Tamsey": "Tamsey"}
    rows = []
    act = W["active"]
    for m in C.TEST:
        y, mo = C.MONTHS[m]
        r1 = C.R1_HIST[y]; tp = C.RTOU_HIST[min(y, 2026)]
        k = use[:, m, :]
        tot = k.sum(1)
        rev = np.where(on_tou[:, m], tp["cc"] + k[:, 2] * tp["peak"] + (tot - k[:, 2]) * tp["other"], r1["cc"] + tot * r1["e"])
        a = act[:, m] & (tot > 0)
        office = svc.district.map(off_of).values.copy()
        if (y, mo) >= (2025, 7):
            office = np.where(office == "Pike Ridge", "Brisco Bend", office)
        df = pd.DataFrame(dict(office=office[a], bills=1, kwh=tot[a], rev=rev[a]))
        g = df.groupby("office").agg(bills=("bills", "sum"), kwh=("kwh", "sum"), rev=("rev", "sum")).reset_index()
        for r in g.itertuples():
            rows.append(["%04d-%02d" % (y, mo), r.office, "Residential", int(r.bills), int(round(r.kwh)), round(r.rev, 2)])
    df = pd.DataFrame(rows, columns=["bill_month", "billing_office", "class", "bills", "kwh_billed", "base_revenue_usd"])
    return df


def ev_rebates(W, P, rng):
    svc = W["svc"]
    rows = []
    for i in np.where((svc.ev_kwh.values > 0) & (svc.ev_i.values < len(C.MONTHS)))[0]:
        if rng.random() < 0.58:
            m = max(int(svc.ev_i.iat[i]) - int(rng.integers(0, 3)), -20)
            if m < 0:
                y, mo = 2022 + (m + 26) // 12 - 1, (m + 26) % 12 + 1
            else:
                y, mo = C.MONTHS[m]
            rows.append([P["svc"].acct.iat[i], "%04d-%02d-%02d" % (y, mo, int(rng.integers(1, 28))), rng.choice(["Level 2, 40 A", "Level 2, 48 A", "Level 2, 32 A"]),
                         rng.choice([250, 400], p=[0.6, 0.4])])
    for i in rng.choice(len(svc), 90, replace=False):
        rows.append([P["svc"].acct.iat[i], "2025-%02d-%02d" % (int(rng.integers(1, 13)), int(rng.integers(1, 28))), "Level 2, 40 A", 250])
    df = pd.DataFrame(rows, columns=["service_acct", "rebate_paid", "charger", "rebate_usd"]).sort_values("rebate_paid").reset_index(drop=True)
    return df


def degree_days(rng):
    days = pd.date_range("2023-01-01", "2026-10-31", freq="D")
    doy = days.dayofyear.values
    t = 12.5 - 13.5 * np.cos((doy - 18) / 365.25 * 2 * np.pi) + rng.normal(0, 4.0, len(days))
    tf = t * 9 / 5 + 32
    hdd = np.maximum(65 - tf, 0); cdd = np.maximum(tf - 65, 0)
    return pd.DataFrame(dict(date=days.strftime("%Y-%m-%d"), station="Kessel Mill substation", tavg=tf.round(1), hdd=hdd.round(1), cdd=cdd.round(1)))


DICT = {
    C.F_AMI: [("meter_no", "Meter serial number"), ("service_acct", "CIS service account billed for the read period"),
              ("bill_month", "Billing month: the month of the read that closes the period (read_to)"),
              ("read_from", "Opening read date (or the meter's set date)"), ("read_to", "Closing read date (or the meter's removal date)"),
              ("kwh_2300_0600", "kWh recorded 11 p.m. to 6 a.m. in the read period"), ("kwh_0600_1600", "kWh recorded 6 a.m. to 4 p.m."),
              ("kwh_1600_2100", "kWh recorded 4 p.m. to 9 p.m."), ("kwh_2100_2300", "kWh recorded 9 p.m. to 11 p.m."),
              ("read_type", "ACT read from interval data; EST estimated by the MDM")],
    C.F_SVC: [("service_acct", "CIS service account"), ("membership_no", "Cooperative membership number"), ("location_no", "Service location (map) number"),
              ("district", "District of the service location"), ("premise_type", "Dwelling type recorded at connection"), ("primary_heat", "Primary heating fuel recorded at connection"),
              ("billing_cycle", "Meter reading cycle 1 to 4"), ("service_start", "Date service began (MM/DD/YYYY)"), ("service_end", "Date of the final read (MM/DD/YYYY); blank while active"),
              ("status", "Active or Final")],
    C.F_RATE: [("service_acct", "CIS service account"), ("rate_code", "Rate schedule"), ("eff_from", "First day the schedule applies"), ("eff_to", "Last day the schedule applies; blank while open")],
    C.F_EXCH: [("location_no", "Service location"), ("removed_meter", "Meter taken out"), ("installed_meter", "Meter put in"), ("exchange_date", "Date of the exchange"), ("reason", "Work order reason")],
    C.F_CRM: [("case_no", "CRM case"), ("received_utc", "Time the request was received, UTC"), ("channel", "How the request came in"), ("service_acct", "Service account named on the request"),
              ("request", "What was asked for"), ("status", "Case outcome"), ("completed_on", "Date the CIS change was made")],
    C.F_BILL: [("bill_month", "Billing month"), ("billing_office", "District office issuing the bills"), ("class", "Rate class"), ("bills", "Bills issued"),
               ("kwh_billed", "kWh billed"), ("base_revenue_usd", "Revenue under the base schedules, before riders")],
    C.F_EV: [("service_acct", "Service account paid"), ("rebate_paid", "Date paid"), ("charger", "Charger installed"), ("rebate_usd", "Rebate paid")],
    C.F_HDD: [("date", "Day"), ("station", "Weather station"), ("tavg", "Daily average temperature, deg F"), ("hdd", "Heating degree days, base 65 F"), ("cdd", "Cooling degree days, base 65 F")],
}
