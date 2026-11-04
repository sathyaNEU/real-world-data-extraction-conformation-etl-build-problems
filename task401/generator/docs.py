"""The governing and context documents (DOCX through python-docx, PDF through reportlab, XLSX through openpyxl),
scrubbed of toolchain marks the way the house helpers do it."""
import io, os, re, zipfile
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import docx
from docx.shared import Pt

FONT_DIR = '/usr/share/fonts/truetype/crosextra'
pdfmetrics.registerFont(TTFont('Carlito', os.path.join(FONT_DIR, 'Carlito-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Carlito-Bold', os.path.join(FONT_DIR, 'Carlito-Bold.ttf')))
WORD = 'Microsoft\xae Word for Microsoft 365'
ORG = 'Strathcorrie Council'
ST = dict(
    title=ParagraphStyle('t', fontName='Carlito-Bold', fontSize=14, leading=18, spaceAfter=4),
    sub=ParagraphStyle('s', fontName='Carlito', fontSize=9.5, leading=12, textColor=colors.HexColor('#444444'), spaceAfter=10),
    h=ParagraphStyle('h', fontName='Carlito-Bold', fontSize=11, leading=14, spaceBefore=8, spaceAfter=3),
    p=ParagraphStyle('p', fontName='Carlito', fontSize=10.5, leading=14, spaceAfter=5))
APP_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/'
           'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
           '<Template>Normal.dotm</Template><TotalTime>%d</TotalTime><Pages>%d</Pages><Words>%d</Words><Characters>%d</Characters>'
           '<Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity><Lines>%d</Lines><Paragraphs>%d</Paragraphs>'
           '<ScaleCrop>false</ScaleCrop><Company>%s</Company><LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>%d</CharactersWithSpaces>'
           '<SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>')


def scrub_docx(path, author, stamp, created):
    src = zipfile.ZipFile(path)
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    body = [d for n, d in items if n == 'word/document.xml'][0]
    words = len(re.sub(rb'<[^>]+>', b' ', body).split())
    out = []
    for name, data in items:
        if name in ('word/stylesWithEffects.xml', 'docProps/thumbnail.jpeg'):
            continue
        if name == 'docProps/app.xml':
            data = (APP_XML % (37, max(1, words // 420), words, words * 6, words // 11, 19, ORG, words * 7)).encode()
        if name == 'docProps/core.xml':
            data = re.sub(rb'(<dc:creator[^>]*>)[^<]*', rb'\g<1>' + author.encode(), data)
            data = re.sub(rb'(<cp:lastModifiedBy[^>]*>)[^<]*', rb'\g<1>' + author.encode(), data)
            data = re.sub(rb'(<dcterms:created[^>]*>)[^<]*', rb'\g<1>' + created.encode(), data)
            data = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*', rb'\g<1>' + created.encode(), data)
            data = re.sub(rb'<cp:revision>[^<]*</cp:revision>', b'<cp:revision>3</cp:revision>', data)
            for tag in (rb'dc:description', rb'cp:keywords', rb'dc:subject', rb'cp:category', rb'dc:title'):
                data = re.sub(rb'<' + tag + rb'>[^<]*</' + tag + rb'>|<' + tag + rb'/>', b'', data)
        if name in ('[Content_Types].xml', 'word/_rels/document.xml.rels', '_rels/.rels'):
            data = re.sub(rb'<(Override|Relationship)[^>]*(stylesWithEffects|thumbnail)[^>]*/>', b'', data)
            data = re.sub(rb'<Default Extension="jpeg"[^>]*/>', b'', data)
        out.append((name, data))
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=stamp); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


def shared_strings(items):
    """Excel stores cell text in a shared string table; move openpyxl's inline strings there."""
    table, index = [], {}
    pat = re.compile(rb'<c ([^>]*?)t="inlineStr"([^>]*)><is><t(?: [^>]*)?>(.*?)</t></is></c>|<c ([^>]*?)t="inlineStr"([^>]*)><is><t(?: [^>]*)?/></is></c>', re.S)
    def sub(m):
        if m.group(3) is not None:
            a, b, text = m.group(1), m.group(2), m.group(3)
        else:
            a, b, text = m.group(4), m.group(5), b''
        if text not in index:
            index[text] = len(table); table.append(text)
        return b'<c ' + a + b't="s"' + b + b'><v>' + str(index[text]).encode() + b'</v></c>'
    out, total = [], 0
    for name, data in items:
        if name.startswith('xl/worksheets/sheet') and b'inlineStr' in data:
            total += len(pat.findall(data))
            data = pat.sub(sub, data)
        out.append((name, data))
    if not table:
        return out
    sst = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<sst xmlns="http://schemas.openxmlformats.org/'
           b'spreadsheetml/2006/main" count="%d" uniqueCount="%d">' % (total, len(table)) +
           b''.join(b'<si><t xml:space="preserve">' + t + b'</t></si>' if t[:1] == b' ' or t[-1:] == b' ' else b'<si><t>' + t + b'</t></si>' for t in table) + b'</sst>')
    res = []
    for name, data in out:
        if name == '[Content_Types].xml' and b'sharedStrings' not in data:
            data = data.replace(b'</Types>', b'<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-'
                                              b'officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
        if name == 'xl/_rels/workbook.xml.rels' and b'sharedStrings' not in data:
            data = data.replace(b'</Relationships>', b'<Relationship Id="rId99" Type="http://schemas.openxmlformats.org/officeDocument/'
                                                      b'2006/relationships/sharedStrings" Target="sharedStrings.xml"/></Relationships>')
        res.append((name, data))
        if name == 'xl/styles.xml':
            res.append(('xl/sharedStrings.xml', sst))
    if not any(n == 'xl/sharedStrings.xml' for n, _ in res):
        res.append(('xl/sharedStrings.xml', sst))
    return res


def scrub_xlsx(path, author, created, modified, stamp):
    src = zipfile.ZipFile(path)
    items = [(i.filename, src.read(i.filename)) for i in src.infolist()]
    src.close()
    items = shared_strings(items)
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if name == 'docProps/core.xml':
                data = re.sub(rb'(<dc:creator[^>]*>)[^<]*', rb'\g<1>' + author.encode(), data)
                data = re.sub(rb'(<cp:lastModifiedBy[^>]*>)[^<]*', rb'\g<1>' + author.encode(), data)
                data = re.sub(rb'(<dcterms:created[^>]*>)[^<]*', rb'\g<1>' + created.encode(), data)
                data = re.sub(rb'(<dcterms:modified[^>]*>)[^<]*', rb'\g<1>' + modified.encode(), data)
            if name == 'docProps/app.xml':
                data = re.sub(rb'<Application>[^<]*</Application>', b'<Application>Microsoft Excel</Application>', data)
                data = re.sub(rb'<AppVersion>[^<]*</AppVersion>', b'<AppVersion>16.0300</AppVersion>', data)
                if b'<Company>' in data:
                    data = re.sub(rb'<Company>[^<]*</Company>', b'<Company>' + ORG.encode() + b'</Company>', data)
            zi = zipfile.ZipInfo(name, date_time=stamp); zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


def write_docx(path, blocks, author, stamp, created):
    d = docx.Document()
    st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
    for kind, val in blocks:
        if kind == 'title':
            p = d.add_paragraph(); r = p.add_run(val); r.bold = True; r.font.size = Pt(15)
        elif kind == 'sub':
            p = d.add_paragraph(); r = p.add_run(val); r.font.size = Pt(9.5)
        elif kind == 'h':
            p = d.add_paragraph(); r = p.add_run(val); r.bold = True; r.font.size = Pt(12)
        elif kind == 'p':
            d.add_paragraph(val)
        elif kind == 'table':
            t = d.add_table(rows=len(val), cols=len(val[0])); t.style = 'Table Grid'
            for i, row in enumerate(val):
                for j, c in enumerate(row):
                    cell = t.cell(i, j); cell.text = str(c)
                    if i == 0:
                        for r in cell.paragraphs[0].runs:
                            r.bold = True
    d.core_properties.author = author
    d.save(path)
    scrub_docx(path, author, stamp, created)


def write_pdf(path, title, author, blocks, issued):
    flow = []
    for kind, val in blocks:
        if kind == 'table':
            t = Table(val[0], colWidths=val[1])
            t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'Carlito'), ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Carlito-Bold'), ('LINEBELOW', (0, 0), (-1, 0), 0.6, colors.black),
                                   ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
            flow.append(t); flow.append(Spacer(1, 6))
        else:
            flow.append(Paragraph(val, ST[kind]))
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=WORD, producer=WORD)
    doc.build(flow)
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject, DictionaryObject
    r = PdfReader(io.BytesIO(buf.getvalue())); w = PdfWriter()
    for pg in r.pages:
        w.add_page(pg)
    info = DictionaryObject({NameObject('/Title'): TextStringObject(title), NameObject('/Author'): TextStringObject(author),
                             NameObject('/Creator'): TextStringObject(WORD), NameObject('/Producer'): TextStringObject(WORD),
                             NameObject('/CreationDate'): TextStringObject('D:' + issued), NameObject('/ModDate'): TextStringObject('D:' + issued)})
    w._info = w._add_object(info)
    b2 = io.BytesIO(); w.write(b2)
    open(path, 'wb').write(b2.getvalue())


