"""Deterministic writers and readers for every format the pack ships."""
import csv
import io
import os
import re
import zipfile
import zlib

FIXED_ZIP_TIME = (2026, 10, 31, 9, 12, 0)
MTIME = 1793440320   # 2026-10-31 09:12 UTC, after the latest record


def write_csv(path, header, rows, delimiter=",", crlf=False):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=delimiter, lineterminator="\r\n" if crlf else "\n")
    w.writerow(header)
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def read_csv(path, delimiter=","):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f, delimiter=delimiter))
    return rows[0], rows[1:]


def fix_zip(path, created=b"2026-10-31T09:00:00Z", modified=b"2026-10-31T09:12:00Z"):
    """Rewrite an OOXML zip with fixed entry times so two builds are byte-identical."""
    with zipfile.ZipFile(path) as z:
        entries = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    fixed = []
    for name, data in entries:
        if name == "docProps/core.xml":
            # the workbook library stamps the save time; the producing system's export carries its own
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + modified + rb"\g<2>", data)
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + created + rb"\g<2>", data)
        fixed.append((name, data))
    entries = fixed
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in entries:
            zi = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)
    os.replace(tmp, path)


def set_mtime(path):
    os.utime(path, (MTIME, MTIME))


def pdf_text(path):
    """Text of a reportlab PDF: inflate each content stream (ASCII85 then Flate, or Flate alone) and pull the
    strings out of the Tj and TJ operators."""
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"<<((?:(?!<<).)*?)>>\s*stream\r?\n(.*?)endstream", data, re.S):
        head, body = m.group(1), m.group(2)
        try:
            if b"ASCII85Decode" in head:
                b = body.strip()
                if b.startswith(b"<~"):
                    b = b[2:]
                if b.endswith(b"~>"):
                    b = b[:-2]
                import base64
                body = base64.a85decode(b, adobe=False)
            if b"FlateDecode" in head:
                body = zlib.decompress(body.strip() if b"ASCII85Decode" not in head else body)
        except Exception:
            continue
        for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", body, re.S):
            out.append(_pdf_unescape(s))
        for arr in re.findall(rb"\[(.*?)\]\s*TJ", body, re.S):
            out.append("".join(_pdf_unescape(x) for x in re.findall(rb"\((.*?)(?<!\\)\)", arr, re.S)))
    return "\n".join(out)


def _pdf_unescape(s):
    s = s.replace(rb"\(", b"(").replace(rb"\)", b")").replace(rb"\\", b"\\")
    s = re.sub(rb"\\(\d{3})", lambda m: bytes([int(m.group(1), 8)]), s)
    return s.decode("latin-1")


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    return re.sub(r"<[^>]+>", "", re.sub(r"</w:p>", "\n", xml))
