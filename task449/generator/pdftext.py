"""Text of a reportlab PDF: every content stream ASCII85- then Flate-decoded, the strings drawn with Tj and TJ."""
import base64
import re
import zlib


def _streams(raw):
    pos = 0
    while True:
        i = raw.find(b"stream", pos)
        if i < 0:
            return
        if raw[i - 3:i] == b"end":
            pos = i + 6
            continue
        j = raw.find(b"endstream", i)
        head = raw[raw.rfind(b"<<", 0, i):i]
        body = raw[i + 6:j].strip(b"\r\n")
        if b"ASCII85Decode" in head:
            b = re.sub(rb"\s", b"", body)
            if b.endswith(b"~>"):
                b = b[:-2]
            body = base64.a85decode(b)
        if b"FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                pos = j + 9
                continue
        yield body
        pos = j + 9


def pdf_text(path):
    raw = open(path, "rb").read()
    parts = []
    for body in _streams(raw):
        for m in re.finditer(rb"\(((?:\\.|[^\\)])*)\)\s*Tj", body):
            s = m.group(1).decode("latin-1")
            s = re.sub(r"\\([()\\])", r"\1", s)
            parts.append(s)
    return " ".join(parts)
