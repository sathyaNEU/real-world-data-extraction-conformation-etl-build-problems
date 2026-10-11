"""Reproducible containers: the PDF's date and document id, and the deck's properties and zip stamps."""
import datetime as dt
import re
import zipfile

import officex as OX
import world as W


def normalize_pdf(path, local_when, doc_id=b"6D1F4C0A92B83E57A1C4D90E3B7F2A61"):
    """stamp the PDF with the UTC instant of a Sydney wall-clock time (the writer records UTC as D:...Z')"""
    utc = local_when.replace(tzinfo=W.SYD).astimezone(dt.timezone.utc).strftime("%Y%m%d%H%M%S")
    b = open(path, "rb").read()
    b = re.sub(rb"D:\d{14}Z'", ("D:%sZ'" % utc).encode(), b)
    b = re.sub(rb"(/ID\s*\[\s*)<[0-9A-Fa-f]{32}>(\s*)<[0-9A-Fa-f]{32}>",
               lambda m: m.group(1) + b"<" + doc_id + b">" + m.group(2) + b"<" + doc_id + b">", b)
    b = re.sub(rb"/DocChecksum /[0-9A-F]{32}", b"/DocChecksum /" + doc_id[::-1], b)
    open(path, "wb").write(b)


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
            t = re.sub(r"<Application>[^<]*</Application>", "<Application>%s</Application>" % application, t)
            t = re.sub(r"<AppVersion>[^<]*</AppVersion>", "<AppVersion>16.0000</AppVersion>", t)
            t = re.sub(r"<Company>[^<]*</Company>|<Company/>", "<Company>Bellbird Personal Finance Ltd</Company>", t)
            data = t.encode("utf-8")
        out.append((name, data))
    OX.write_zip(path, out)
