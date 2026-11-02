"""Document writers: PDFs through reportlab (invariant), workbooks through openpyxl and Word files through python-docx,
each re-zipped with fixed timestamps so two builds are byte-identical."""
import io, os, re, zipfile, datetime as dt
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

RL_COMMENTS = (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)")

XLSX_APP = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/'
            'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/'
            'docPropsVTypes"><Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false'
            '</ScaleCrop><HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr>'
            '</vt:variant><vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector></HeadingPairs><TitlesOfParts><vt:vector '
            'size="%d" baseType="lpstr">%s</vt:vector></TitlesOfParts><Company>%s</Company><LinksUpToDate>false'
            '</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300'
            '</AppVersion></Properties>')
DOCX_APP = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/'
            'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/'
            'docPropsVTypes"><Template>Normal.dotm</Template><TotalTime>%d</TotalTime><Application>Microsoft Office Word'
            '</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop><Company>%s</Company><LinksUpToDate>false'
            '</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000'
            '</AppVersion></Properties>')

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=12.6, spaceAfter=5)
SMALL = ParagraphStyle("small", fontName="Helvetica", fontSize=8, leading=10)
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=3)
META = ParagraphStyle("meta", fontName="Helvetica", fontSize=8.5, leading=11, textColor=colors.HexColor("#444444"))


def pdf(path, title, author, story_fn, footer, when):
    """A PDF dated by its issuer (when, UTC), its writer's comment lines replaced at equal length."""
    def deco(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(18 * mm, 10 * mm, footer)
        c.drawRightString(192 * mm, 10 * mm, "Page %d" % d.page)
        c.restoreState()
    os.environ["SOURCE_DATE_EPOCH"] = str(int(when.replace(tzinfo=dt.timezone.utc).timestamp()))
    try:
        doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                                bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                                subject="", keywords="")
        doc.build(story_fn(), onFirstPage=deco, onLaterPages=deco)
    finally:
        del os.environ["SOURCE_DATE_EPOCH"]
    b = open(path, "rb").read()
    n = len(b)
    for old in RL_COMMENTS:
        assert b.count(old) == 1, (path, old)
        b = b.replace(old, author.encode().ljust(len(old)))
    assert len(b) == n
    open(path, "wb").write(b)


def table(rows, widths, header=True, align_right=()):
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.2), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
          ("TOPPADDING", (0, 0), (-1, -1), 2.2)]
    if header:
        st.append(("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.2))
    for c in align_right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def rezip(path, created, modified=None, app=None, drop=()):
    """Rewrite an OOXML zip with its own dates (member times and core properties), a stable member order, the
    producing application's properties and none of the writing library's leftovers."""
    modified = modified or created
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist() if i.filename not in drop]
    iso = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    out = []
    for name, data in items:
        if name == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + iso(created) + rb"\g<2>", data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + iso(modified) + rb"\g<2>", data)
        elif name == "docProps/app.xml" and app is not None:
            data = app.encode()
        elif name == "_rels/.rels":
            for d in drop:
                data = re.sub(rb'<Relationship [^>]*Target="' + re.escape(d.encode()) + rb'"/>', b"", data)
        out.append((name, data))
    order = sorted(out, key=lambda x: (x[0] != "[Content_Types].xml", x[0]))
    stamp = (modified.year, modified.month, modified.day, modified.hour, modified.minute, modified.second)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in order:
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    open(path, "wb").write(buf.getvalue())


def xlsx_app(sheets, company):
    return XLSX_APP % (len(sheets), len(sheets), "".join("<vt:lpstr>%s</vt:lpstr>" % s for s in sheets), company)


def docx_app(company, minutes):
    return DOCX_APP % (minutes, company)


def save_xlsx(wb, path, creator, created, modified, company):
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.save(path)
    rezip(path, created, modified, app=xlsx_app(wb.sheetnames, company))


def fix_docx_props(d, author, title):
    cp = d.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.revision = 3
    cp.comments = ""
    cp.keywords = ""
    cp.subject = ""
    cp.category = ""
