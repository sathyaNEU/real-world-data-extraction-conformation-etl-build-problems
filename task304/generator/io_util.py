"""task304: readers shared by the analysis (the verifier keeps its own): CSV, XLSX and the PDF text of a reportlab file
(ASCII85 then Flate streams decoded), plus the PDF scrub the document writer applies."""
import base64
import csv
import re
import zlib


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def read_xlsx(path, sheet, header_row=1):
    from openpyxl import load_workbook
    ws = load_workbook(path, read_only=True, data_only=True)[sheet]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    head = [str(c) if c is not None else "" for c in rows[header_row - 1]]
    body = [r for r in rows[header_row:] if any(c is not None for c in r)]
    return head, body


def scrub_pdf(path, created="D:20261116090000+10'00'", modified=None):
    """Blank the writer's comment line and set the document's own creation and modification stamps, each
    substituted at equal length so the cross-reference offsets stay valid."""
    data = open(path, "rb").read()
    data = re.sub(rb"(%[\x80-\xff]*)([^\n]*ReportLab[^\n]*)\n",
                  lambda m: m.group(1) + b" " * len(m.group(2)) + b"\n", data)
    for key, stamp in ((rb"/CreationDate", created), (rb"/ModDate", modified or created)):
        def sub(m, key=key, stamp=stamp):
            width = len(m.group(0)) - len(key) - 3
            assert len(stamp) == width, (stamp, width)
            return m.group(0)[:len(key) + 2] + stamp.encode() + b")"
        data = re.sub(key + rb" \(D:[^)]*\)", sub, data)
    open(path, "wb").write(data)


def _unescape(s):
    s = re.sub(rb"\\([0-7]{1,3})", lambda m: bytes([int(m.group(1), 8) & 0xFF]), s)
    s = s.replace(rb"\(", b"(").replace(rb"\)", b")").replace(rb"\n", b"\n").replace(rb"\r", b"\r")
    s = s.replace(rb"\t", b"\t").replace(b"\\\\", b"\\")
    return s.decode("latin-1")


def pdf_text(path):
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        txt = raw
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[2:-2] if raw.startswith(b"<~") else raw[:-2])
            txt = zlib.decompress(raw)
        except Exception:
            pass
        for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", txt, re.S):
            out.append(_unescape(s))
    return " ".join(out)
