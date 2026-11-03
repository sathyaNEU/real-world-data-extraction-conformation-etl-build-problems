"""Office and PDF writers that save like the tools a utility's staff use (fixed dates, no library fingerprints)."""
import io
import re
import zipfile

APP_DOCX = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/'
            'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Template>Normal.dotm</Template><TotalTime>{tt}</TotalTime><Pages>{pages}</Pages><Words>{words}</Words>'
            '<Characters>{chars}</Characters><Application>Microsoft Office Word</Application><DocSecurity>0</DocSecurity>'
            '<Lines>{lines}</Lines><Paragraphs>{paras}</Paragraphs><ScaleCrop>false</ScaleCrop><Company>Sørdal Kraft AS</Company>'
            '<LinksUpToDate>false</LinksUpToDate><CharactersWithSpaces>{cws}</CharactersWithSpaces><SharedDoc>false</SharedDoc>'
            '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion></Properties>')
APP_XLSX = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Properties xmlns="http://schemas.openxmlformats.org/'
            'officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">'
            '<Application>Microsoft Excel</Application><DocSecurity>0</DocSecurity><ScaleCrop>false</ScaleCrop>'
            '<Company>Sørdal Kraft AS</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
            '<HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0300</AppVersion></Properties>')
CORE = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/'
        'package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
        'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">{title}'
        '<dc:creator>{author}</dc:creator><cp:lastModifiedBy>{author}</cp:lastModifiedBy>{rev}'
        '<dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">{modified}</dcterms:modified></cp:coreProperties>')


def resave(raw, kind, author, created, modified, title='', words=0, rev=None):
    """Rewrite an Office package: Office 16 app.xml, plain core.xml, no thumbnail, member dates at `modified`."""
    zin = zipfile.ZipFile(io.BytesIO(raw))
    y, mo, d = int(modified[0:4]), int(modified[5:7]), int(modified[8:10])
    hh, mm, ss = int(modified[11:13]), int(modified[14:16]), int(modified[17:19])
    out = io.BytesIO()
    zout = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
    order = ['[Content_Types].xml', '_rels/.rels'] + [n for n in zin.namelist() if n not in ('[Content_Types].xml', '_rels/.rels')]
    for name in order:
        if name == 'docProps/thumbnail.jpeg' or name.startswith('customXml/'):
            continue
        data = zin.read(name)
        if name == '_rels/.rels':
            data = re.sub(rb'<Relationship [^>]*thumbnail\.jpeg"/>', b'', data)
        if name == '[Content_Types].xml':
            data = re.sub(rb'<Override PartName="/customXml/[^>]*/>', b'', data)
        if name == 'word/_rels/document.xml.rels':
            data = re.sub(rb'<Relationship [^>]*customXml[^>]*/>', b'', data)
        if name == 'docProps/app.xml':
            if kind == 'docx':
                data = APP_DOCX.format(tt=12 + words // 40, pages=max(1, words // 420 + 1), words=words, chars=words * 6,
                                       lines=max(1, words // 11), paras=max(1, words // 45), cws=words * 7).encode('utf-8')
            else:
                data = APP_XLSX.encode('utf-8')
        if name == 'docProps/core.xml':
            t = '<dc:title>%s</dc:title>' % title if title else ''
            r = '<cp:revision>%d</cp:revision>' % rev if rev else ''
            data = CORE.format(title=t, author=author, rev=r, created=created, modified=modified).encode('utf-8')
        zi = zipfile.ZipInfo(name, date_time=(y, mo, d, hh, mm, ss))
        zi.compress_type = zipfile.ZIP_DEFLATED
        zout.writestr(zi, data)
    zout.close()
    return out.getvalue()


def pdf(path, title, author, date_pdf, story_fn, producer='Microsoft\u00ae Word for Microsoft 365'):
    """Write a PDF with reportlab in invariant mode, then stamp the document's own dates (same-length edits only, so
    every cross-reference offset stays valid) and blank the library's comment lines."""
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, title=title, author=author, creator=producer, producer=producer,
                            leftMargin=56, rightMargin=56, topMargin=60, bottomMargin=60)
    doc.build(story_fn())
    raw = buf.getvalue()

    def same(m, new):
        return new.ljust(len(m.group(0)))[:len(m.group(0))]
    raw = re.sub(rb"D:\d{14}[+-]\d\d'\d\d'", lambda m: ("D:%s+01'00'" % date_pdf).encode(), raw)
    raw = re.sub(rb"(?i)reportlab generated pdf document[^\r\n]*", lambda m: b' ' * len(m.group(0)), raw)
    assert not re.search(rb"(?i)reportlab|anonymous", raw), 'library string left in ' + path
    with open(path, 'wb') as f:
        f.write(raw)


KEEP_STYLES = ('Normal', 'DefaultParagraphFont', 'TableNormal', 'NoList', 'Heading1', 'Heading2', 'Heading1Char',
               'Heading2Char')


def lean_docx(raw):
    """Cut a python-docx package down to what a short Word note carries: a styles part with the document defaults and
    only the styles in use (and their linked character styles), no stylesWithEffects part. Theme, settings, fonts and
    numbering stay."""
    zin = zipfile.ZipFile(io.BytesIO(raw))
    styles = zin.read('word/styles.xml').decode('utf-8')
    head = styles[:styles.index('<w:docDefaults>')]
    dd = styles[styles.index('<w:docDefaults>'):styles.index('</w:docDefaults>') + len('</w:docDefaults>')]
    dd = dd.replace('w:val="en-US" w:eastAsia="en-US"', 'w:val="nb-NO" w:eastAsia="en-US"')
    body = []
    for sid in KEEP_STYLES:
        m = re.search(r'<w:style [^>]*w:styleId="%s".*?</w:style>' % sid, styles, re.S)
        body.append(m.group(0))
    lean = head + dd + ''.join(body) + '</w:styles>'
    out = io.BytesIO()
    zout = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
    for zi in zin.infolist():
        n = zi.filename
        if n == 'word/stylesWithEffects.xml':
            continue
        data = zin.read(n)
        if n == 'word/styles.xml':
            data = lean.encode('utf-8')
        elif n == 'word/_rels/document.xml.rels':
            data = re.sub(rb'<Relationship [^>]*stylesWithEffects[^>]*/>', b'', data)
        elif n == '[Content_Types].xml':
            data = re.sub(rb'<Override PartName="/word/stylesWithEffects.xml"[^>]*/>', b'', data)
        zout.writestr(zi, data)
    zout.close()
    return out.getvalue()
