"""task212 writers: byte-stable parquet, scrubbed workbooks and PDFs, and the registers and plans each producing team
keeps (accounts, hubs, the peak plan, the flat-rate terms, the sorter maker's visit log)."""
import calendar
import io
import os
import re
import zipfile
import datetime as dt
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
import world

ORG = "Brujula Paqueteria SL"
HUB_ROWS = [
    # hub key, sorter number, audit app name, town, province, sorter, commissioned, heavy-goods chute,
    # customer-service area, CMMS site, tracking location
    ("ZAZ", 50, "Zaragoza Plaza", "Zaragoza", "Zaragoza", "tilt-tray, 2 induction lines", 2011, "N", "ZARAGOZA",
     "ZGZ Plaza", "PLAT-50"),
    ("VLC", 46, "Ribarroja", "Ribarroja del Turia", "Valencia", "tilt-tray, 3 induction lines", 2013, "N", "VALENCIA",
     "VLC Ribarroja", "PLAT-46"),
    ("SVQ", 41, "Dos Hermanas", "Dos Hermanas", "Sevilla", "tilt-tray, 2 induction lines", 2012, "N", "SEVILLA",
     "SVQ Dos Hermanas", "PLAT-41"),
    ("MAD", 28, "San Fernando", "San Fernando de Henares", "Madrid", "cross-belt, 6 induction lines", 2021, "Y",
     "MADRID", "MAD San Fernando", "PLAT-28"),
    ("BCN", 8, "El Prat", "El Prat de Llobregat", "Barcelona", "cross-belt, 5 induction lines", 2020, "Y", "BARCELONA",
     "BCN El Prat", "PLAT-08"),
    ("BIO", 48, "Basauri", "Basauri", "Bizkaia", "cross-belt, 3 induction lines", 2022, "N", "BILBAO", "BIO Basauri",
     "PLAT-48"),
]
# parcels sorted a week, the quarter's mean, and the peak build-up by ISO week (the operations planners' plan)
WEEKLY_Q3 = {"ZAZ": 118400, "VLC": 124300, "SVQ": 108700, "MAD": 305600, "BCN": 267900, "BIO": 96200}
PEAK_UPLIFT = {40: 1.02, 41: 1.04, 42: 1.05, 43: 1.07, 44: 1.10, 45: 1.16, 46: 1.24, 47: 1.31, 48: 1.74, 49: 1.66,
               50: 1.55, 51: 1.44, 52: 0.93}


# ------------------------------------------------------------------------------------------------- writers

def write_parquet(df, path, writer=b"parquet-mr version 1.12.3 (build f8dced182c4c1fbdec6ccb3185537b5a01e6ed6b)"):
    """Parquet with no pandas schema metadata and the export tool's own writer string in the footer."""
    tbl = pa.Table.from_pandas(df, preserve_index=False).replace_schema_metadata(None)
    pq.write_table(tbl, path, compression="snappy", version="2.6", use_dictionary=True)
    b = open(path, "rb").read()
    flen = int.from_bytes(b[-8:-4], "little")
    foot = b[-8 - flen:-8]
    i = foot.find(b"parquet-cpp-arrow version")
    assert i > 0
    foot2 = foot[:i - 1] + bytes([len(writer)]) + writer + foot[i + foot[i - 1]:]
    open(path, "wb").write(b[:-8 - flen] + foot2 + len(foot2).to_bytes(4, "little") + b"PAR1")


def xlsx_scrub(path, creator, stamp_iso, title="", company=ORG):
    """docProps rewritten to the issuer and the date; every other entry byte for byte, same order, one fixed date."""
    src = open(path, "rb").read()
    zin = zipfile.ZipFile(io.BytesIO(src))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename == "docProps/core.xml":
                data = (
                    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
                    'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                    '<dc:title>%s</dc:title><dc:creator>%s</dc:creator><cp:lastModifiedBy>%s</cp:lastModifiedBy>'
                    '<dcterms:created xsi:type="dcterms:W3CDTF">%s</dcterms:created>'
                    '<dcterms:modified xsi:type="dcterms:W3CDTF">%s</dcterms:modified></cp:coreProperties>'
                    % (title, creator, creator, stamp_iso, stamp_iso)).encode()
            elif info.filename == "docProps/app.xml":
                data = (
                    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" '
                    'xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
                    '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
                    '<Company>%s</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                    '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>'
                    % company).encode()
            zi = zipfile.ZipInfo(info.filename, date_time=(2026, 10, 26, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            zout.writestr(zi, data)
    open(path, "wb").write(out.getvalue())


def sheet_xlsx(path, sheets, creator, stamp_iso, title, widths=None, numfmt=None):
    """One or more plain sheets: a bold header, the rows, set column widths and number formats."""
    wb = Workbook()
    first = True
    for name, df in sheets:
        ws = wb.active if first else wb.create_sheet()
        first = False
        ws.title = name
        ws.append(list(df.columns))
        for c in ws[1]:
            c.font = Font(bold=True)
        for row in df.itertuples(index=False):
            ws.append([None if (isinstance(v, float) and np.isnan(v)) else (v.item() if hasattr(v, "item") else v)
                       for v in row])
        for j, col in enumerate(df.columns, start=1):
            w = (widths or {}).get(col, max(10, min(40, len(str(col)) + 4)))
            ws.column_dimensions[get_column_letter(j)].width = w
            fmt = (numfmt or {}).get(col)
            if fmt:
                for r in range(2, ws.max_row + 1):
                    ws.cell(row=r, column=j).number_format = fmt
        ws.freeze_panes = "A2"
    wb.save(path)
    xlsx_scrub(path, creator, stamp_iso, title)


def scrub_pdf(path):
    raw = open(path, "rb").read()
    out = re.sub(rb"(%[^\n]*?)( ?ReportLab[^\n]*)", lambda m: m.group(1) + b" " * len(m.group(2)), raw)
    assert len(out) == len(raw) and b"ReportLab" not in out
    open(path, "wb").write(out)


def stamp(y, m, d, hh=9, mm=0):
    import time
    return time.struct_time((y, m, d, hh, mm, 0, 0, 1, 0))


def pdf(path, title, author, when, story_fn, pagesize=None):
    """A PDF whose producer, author and dates are the issuer's, rebuilt byte for byte."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate

    def deco(c, d):
        c._doc.info.producer = "Microsoft Word for Microsoft 365"
        c._doc.info.creator = "Microsoft Word for Microsoft 365"
        c._doc.info.author = author
        c._doc.info.title = title
        c._doc.info.subject = ""
        c.setFont("Helvetica", 7.2)
        c.drawString(20 * mm, 11 * mm, title)
        c.drawRightString(190 * mm, 11 * mm, "%d" % c.getPageNumber())

    doc = SimpleDocTemplate(path, pagesize=pagesize or A4, invariant=1, leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm)
    old = os.environ.get("SOURCE_DATE_EPOCH")
    os.environ["SOURCE_DATE_EPOCH"] = str(calendar.timegm(when))
    try:
        doc.build(story_fn(), onFirstPage=deco, onLaterPages=deco)
        scrub_pdf(path)
    finally:
        if old is None:
            del os.environ["SOURCE_DATE_EPOCH"]
        else:
            os.environ["SOURCE_DATE_EPOCH"] = old


def styles():
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.4, leading=12.4, spaceAfter=5)
    h = ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, spaceBefore=7, spaceAfter=3)
    t = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=14, alignment=0, spaceAfter=4)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.2, textColor=colors.HexColor("#333333"))
    return body, h, t, small


# ------------------------------------------------------------------------------------------------- registers

def company_names(n, seed):
    from faker import Faker
    f = Faker("es_ES")
    f.seed_instance(seed)
    out, seen = [], set()
    while len(out) < n:
        nm = f.company()
        if nm not in seen:
            seen.add(nm)
            out.append(nm)
    return out


def accounts_register(accounts, seed):
    acc = accounts.copy().sort_values("account").reset_index(drop=True)
    names = company_names(len(acc), seed + 41)
    heavy = {v[0]: v[1] for v in world.HEAVY_ACCOUNT.values()}
    r = np.random.default_rng(seed + 42)
    acc["account_name"] = [heavy.get(a, n) for a, n in zip(acc.account, names)]
    acc["collection"] = np.where(acc.account.isin(list(heavy)), "dedicated trailer",
                                 r.choice(["depot round", "depot round", "depot round", "drop-off at depot"], len(acc)))
    since = [dt.date(2014, 1, 1) + dt.timedelta(days=int(x)) for x in r.integers(0, 4300, len(acc))]
    acc["customer_since"] = [d.isoformat() for d in since]
    acc.loc[acc.account == "C48316", "customer_since"] = "2026-01-19"   # Basauri's paper account, new this year
    return acc[["account", "account_name", "sector", "collection", "customer_since"]]


def hub_register():
    return pd.DataFrame([(h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[8], h[9], h[10]) for h in HUB_ROWS],
                        columns=["hub_no", "hub_name", "town", "province", "sorter", "sorter_commissioned",
                                 "heavy_goods_chute", "cs_area", "cmms_site", "tracking_location"])


def peak_plan(vlc_peak_mean=None):
    """Weekly parcels sorted: the quarter's actuals by week and the plan from week 40, by hub."""
    r = np.random.default_rng(212)
    strength = {"ZAZ": 1.00, "VLC": 0.71, "SVQ": 1.04, "MAD": 1.09, "BCN": 1.06, "BIO": 0.93}
    rows = []
    for h in world.HUB_KEYS:
        base = WEEKLY_Q3[h]
        for wk in range(27, 40):
            rows.append((h, wk, "sorted", int(round(base * r.normal(1, 0.035), -2))))
        for wk in range(40, 53):
            up = 1 + (PEAK_UPLIFT[wk] - 1) * strength[h] * r.normal(1, 0.04)
            rows.append((h, wk, "plan", int(round(base * up, -2))))
    p = pd.DataFrame(rows, columns=["hub", "iso_week", "basis", "parcels"])
    if vlc_peak_mean is not None:
        m = (p.hub == "VLC") & p.iso_week.between(48, 52)
        cur = p.loc[m, "parcels"].mean()
        p.loc[m, "parcels"] = (p.loc[m, "parcels"] * vlc_peak_mean / cur).round(-2).astype(int)
    return p
