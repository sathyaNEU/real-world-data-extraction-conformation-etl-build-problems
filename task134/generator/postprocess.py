"""Reproducible containers: the PDF's date and document id, and the deck's properties and zip stamps."""
import datetime as dt
import io
import re
import zipfile

import officex as OX
import world as W


def normalize_pdf(path, local_when, doc_id=b"6D1F4C0A92B83E57A1C4D90E3B7F2A61"):
    """stamp the PDF with a UK wall-clock time and its offset from UTC, as the writer records local time
    (D:20260402150500+01'00'). The information dictionary is the last object before the cross-reference table, so
    only startxref moves with the stamp's length; every object offset is checked afterwards."""
    off = int(local_when.replace(tzinfo=W.LON).utcoffset().total_seconds() // 60)
    stamp = ("D:%s%s%02d'%02d'" % (local_when.strftime("%Y%m%d%H%M%S"), "+" if off >= 0 else "-", abs(off) // 60,
                                     abs(off) % 60)).encode()
    b = open(path, "rb").read()
    b = re.sub(rb"D:\d{14}(?:Z'?|[+-]\d\d'\d\d'?)", lambda m: stamp, b)
    b = re.sub(rb"(/ID\s*\[\s*)<[0-9A-Fa-f]{32}>(\s*)<[0-9A-Fa-f]{32}>",
               lambda m: m.group(1) + b"<" + doc_id + b">" + m.group(2) + b"<" + doc_id + b">", b)
    b = re.sub(rb"/DocChecksum /[0-9A-F]{32}", b"/DocChecksum /" + doc_id[::-1], b)
    x = b.rfind(b"\nxref\n") + 1
    b = re.sub(rb"startxref\s+\d+", b"startxref\n%d" % x, b)
    m = re.search(rb"xref\n0 (\d+)\n", b[x:])
    entries = b[x + m.end():].split(b"\n")[:int(m.group(1))]
    for k, e in enumerate(entries):
        if e.endswith(b"n "):
            o = int(e[:10])
            assert b[o:o + 20].startswith(b"%d 0 obj" % k), "object %d is not at its recorded offset" % k
    open(path, "wb").write(b)


def deck_properties(app, items):
    """the deck's extended properties as PowerPoint keeps them: slide, paragraph and word counts from the slides
    themselves, the widescreen format, and the theme and slide titles"""
    slides = sorted((n for n, _ in items if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                    key=lambda n: int(re.search(r"(\d+)", n.split("/")[-1]).group(1)))
    data = dict(items)
    paras, words, titles = 0, 0, []
    for n in slides:
        x = data[n].decode("utf-8")
        ps = [re.sub(r"<[^>]+>", "", p) for p in re.findall(r"<a:p>.*?</a:p>", x, re.S)]
        ps = [p for p in ps if p.strip()]
        paras += len(ps)
        words += sum(len(p.split()) for p in ps)
        titles.append(ps[0] if ps else "PowerPoint Presentation")
    esc = lambda v: v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    app = re.sub(r"<Words>\d+</Words>", "<Words>%d</Words>" % words, app)
    app = re.sub(r"<Paragraphs>\d+</Paragraphs>", "<Paragraphs>%d</Paragraphs>" % paras, app)
    app = re.sub(r"<Slides>\d+</Slides>", "<Slides>%d</Slides>" % len(slides), app)
    app = re.sub(r"<PresentationFormat>[^<]*</PresentationFormat>", "<PresentationFormat>Widescreen</PresentationFormat>", app)
    app = re.sub(r"<TotalTime>\d+</TotalTime>", "<TotalTime>94</TotalTime>", app)
    app = re.sub(r"<HeadingPairs>.*</HeadingPairs>",
                 '<HeadingPairs><vt:vector size="4" baseType="variant"><vt:variant><vt:lpstr>Theme</vt:lpstr></vt:variant>'
                 '<vt:variant><vt:i4>1</vt:i4></vt:variant><vt:variant><vt:lpstr>Slide Titles</vt:lpstr></vt:variant>'
                 '<vt:variant><vt:i4>%d</vt:i4></vt:variant></vt:vector></HeadingPairs>' % len(slides), app, flags=re.S)
    app = re.sub(r"<TitlesOfParts>.*</TitlesOfParts>",
                 '<TitlesOfParts><vt:vector size="%d" baseType="lpstr"><vt:lpstr>Office Theme</vt:lpstr>%s</vt:vector>'
                 '</TitlesOfParts>' % (len(slides) + 1, "".join("<vt:lpstr>%s</vt:lpstr>" % esc(t) for t in titles)),
                 app, flags=re.S)
    return app


def deterministic_embeddings(path, created):
    """an embedded workbook (a chart's data sheet) keeps the deck's own date instead of the moment it was written"""
    stamp = W.utc_stamp(created)
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for name, data in items:
        if name.startswith("ppt/embeddings/") and name.endswith(".xlsx"):
            with zipfile.ZipFile(io.BytesIO(data)) as e:
                inner = [(i.filename, e.read(i.filename)) for i in e.infolist()]
            fixed = []
            for n, d in inner:
                if n == "docProps/core.xml":
                    d = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:)", rb"\g<1>" + stamp.encode() + rb"\g<2>", d)
                fixed.append((n, d))
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as e:
                for n, d in fixed:
                    zi = zipfile.ZipInfo(n, date_time=OX.OFFICE_TIME)
                    zi.compress_type = zipfile.ZIP_DEFLATED
                    zi.create_system = 0
                    e.writestr(zi, d)
                    zi.external_attr = 0
            data = buf.getvalue()
        out.append((name, data))
    OX.write_zip(path, out)


def office_container(path, creator, modified_by, created, modified, application, revision=None):
    """document properties as the application keeps them, entries stamped 1980-01-01"""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for name, data in items:
        if name == "docProps/core.xml":
            t = data.decode("utf-8")
            title = re.search(r"<dc:title>([^<]*)</dc:title>", t)
            data = OX.core_xml(creator, modified_by, created, modified, title=title.group(1) if title else "",
                               revision=revision).encode("utf-8")
        elif name == "docProps/app.xml":
            t = data.decode("utf-8")
            if "<Slides>" in t:
                t = deck_properties(t, items)
            t = re.sub(r"<Application>[^<]*</Application>", "<Application>%s</Application>" % application, t)
            t = re.sub(r"<AppVersion>[^<]*</AppVersion>", "<AppVersion>16.0000</AppVersion>", t)
            t = re.sub(r"<Company>[^<]*</Company>|<Company/>", "<Company>Strathallan Council</Company>", t)
            data = t.encode("utf-8")
        out.append((name, data))
    OX.write_zip(path, out)
