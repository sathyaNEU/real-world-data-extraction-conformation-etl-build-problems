"""task464 architecture 12: scrub the toolchain out of the containers and fix every embedded timestamp.

reportlab stamps its name into each PDF's Producer and openpyxl its own into the workbook properties; both are writer
signatures (leak.py sweep 10, reduce-house-fixes H1). The PDF fix is an equal-length, case-preserving replacement, so
every cross-reference offset stays valid. Each file gets the date its author would have saved it, which also makes two
rebuilds byte identical.
"""
import hashlib
import os
import re
import shutil
import zipfile

NEUTRAL_PDF = "docmaster"          # same length as "reportlab"
SAVED = {
    "restart_pilot_brief_2026.pdf": "20260316112000",
    "crm_send_calendar_2026.xlsx": "2026-11-12T15:05:00Z",
    "sponsored_revenue_by_sector_2026.xlsx": "2026-11-06T09:40:00Z",
    "jobseeker_email_plan_2027.docx": "2026-11-16T16:48:00Z",
    "restart_series_2027.xlsx": "2026-11-24T17:10:00Z",
    "restart_series_2027.docx": "2026-11-24T17:35:00Z",
}
AUTHOR = {"crm_send_calendar_2026.xlsx": b"Glenn Taylor",
          "sponsored_revenue_by_sector_2026.xlsx": b"Finance, Quaywork Ltd",
          "jobseeker_email_plan_2027.docx": b"Marian Smith",
          "restart_series_2027.xlsx": b"Glenn Taylor",
          "restart_series_2027.docx": b"Glenn Taylor"}


PRODUCER = b"Microsoft Word"


def scrub_pdf(path):
    b = open(path, "rb").read()
    name = os.path.basename(path)
    stamp = SAVED[name].encode()

    # the Producer literal takes the fiction's word processor; the surplus becomes whitespace after the literal
    def prod(m):
        old = m.group(0)
        new = b"/Producer (" + PRODUCER + b")"
        assert len(new) <= len(old)
        return new + b" " * (len(old) - len(new))
    nb = re.sub(rb"/Producer \((?:\\.|[^\\)])*\)", prod, b)
    # the writer's comment lines keep their % marker; their text becomes spaces
    nb = re.sub(rb"(?m)^%([^\r\n]*[Rr][Ee][Pp][Oo][Rr][Tt][Ll][Aa][Bb][^\r\n]*)$",
                lambda m: b"%" + b" " * len(m.group(1)), nb)

    def rep(m):
        s = m.group(0).decode("latin-1")
        return "".join(n.upper() if ch.isupper() else n for ch, n in zip(s, NEUTRAL_PDF)).encode("latin-1")
    nb = re.sub(rb"[Rr][Ee][Pp][Oo][Rr][Tt][Ll][Aa][Bb]", rep, nb)
    assert b"docmaster" not in nb.lower()
    nb = re.sub(rb"D:\d{14}", b"D:" + stamp, nb)
    did = hashlib.md5(("qw:" + name).encode()).hexdigest().encode()
    nb = re.sub(rb"/ID\s*\[\s*<([0-9a-fA-F]{32})>\s*<([0-9a-fA-F]{32})>\s*\]",
                lambda m: b"/ID [<" + did + b"> <" + did + b">]", nb)
    assert len(nb) == len(b), (len(nb), len(b))
    if nb != b:
        open(path, "wb").write(nb)
    return True


def scrub_xlsx(path):
    name = os.path.basename(path)
    stamp = SAVED[name].encode()
    y, mo, d = (int(x) for x in stamp[:10].decode().split("-"))
    hh, mm = int(stamp[11:13]), int(stamp[14:16])
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    who = AUTHOR.get(name, b"Quaywork Ltd")
    for n in list(data):
        if n.startswith("docProps/") or n.endswith(".xml") or n.endswith(".rels"):
            t = data[n]
            nt = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", t)
            nt = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", nt)
            nt = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + who + rb"\g<2>", nt)
            if b"<dc:creator" in nt and b"lastModifiedBy" not in nt:
                nt = nt.replace(b"</cp:coreProperties>", b"<cp:lastModifiedBy>" + who + b"</cp:lastModifiedBy></cp:coreProperties>")
            nt = re.sub(rb"[Oo]pen[Pp]yxl", b"Microsoft Excel", nt)
            nt = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + stamp + rb"\g<2>", nt)
            nt = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", nt)
            data[n] = nt
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=(y, mo, d, hh, mm, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[n])
    shutil.move(tmp, path)
    return True


def scrub_docx(path):
    name = os.path.basename(path)
    stamp = SAVED[name].encode()
    y, mo, d = (int(x) for x in stamp[:10].decode().split("-"))
    hh, mm = int(stamp[11:13]), int(stamp[14:16])
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        data = {n: z.read(n) for n in names}
    who = AUTHOR.get(name, b"Quaywork Ltd")
    for n in list(data):
        if n.startswith("docProps/"):
            t = data[n]
            t = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Office Word</Application>", t)
            t = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0000</AppVersion>", t)
            t = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + who + rb"\g<2>", t)
            t = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)", rb"\g<1>" + who + rb"\g<2>", t)
            t = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", t)
            t = re.sub(rb"<dc:description>[^<]*</dc:description>", b"<dc:description/>", t)
            t = re.sub(rb"python-docx", b"", t)
            if n == "docProps/app.xml" and "word/document.xml" in data:
                body = re.sub(rb"<[^>]+>", b" ", data["word/document.xml"]).decode("utf-8", "ignore")
                words = len(body.split())
                chars = len("".join(body.split()))
                t = re.sub(rb"<Words>\d+</Words>", b"<Words>%d</Words>" % words, t)
                t = re.sub(rb"<Characters>\d+</Characters>", b"<Characters>%d</Characters>" % chars, t)
                t = re.sub(rb"<TotalTime>\d+</TotalTime>", b"<TotalTime>%d</TotalTime>" % (40 + words % 50), t)
            data[n] = t
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=(y, mo, d, hh, mm, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data[n])
    shutil.move(tmp, path)
    return True


def run(folder):
    out = []
    for n in sorted(os.listdir(folder)):
        p = os.path.join(folder, n)
        if n.endswith(".pdf"):
            out.append((n, scrub_pdf(p)))
        elif n.endswith(".xlsx"):
            out.append((n, scrub_xlsx(p)))
        elif n.endswith(".docx"):
            out.append((n, scrub_docx(p)))
    return out
