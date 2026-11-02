"""Text out of the pack's PDFs: each content stream decoded (ASCII85 then Flate, as the writer encodes it) and the
strings of its text operators read in order. Used by the analysis and the checks; verify.py has its own reader."""
import base64
import re
import zlib


def _unescape(s):
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            nx = s[i + 1]
            if nx in "nrtbf":
                out.append({"n": "\n", "r": "\r", "t": "\t", "b": "\b", "f": "\f"}[nx])
                i += 2
                continue
            if nx in "()\\":
                out.append(nx)
                i += 2
                continue
            m = re.match(r"[0-7]{1,3}", s[i + 1:])
            if m:
                out.append(chr(int(m.group(0), 8)))
                i += 1 + len(m.group(0))
                continue
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def streams(data):
    for m in re.finditer(rb"<<((?:(?!<<|>>).)*?)>>\s*stream\r?\n(.*?)(?:\r?\n)?endstream", data, re.S):
        head, body = m.group(1), m.group(2)
        if b"/ASCII85Decode" in head:
            body = _a85(body)
        if b"/FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                continue
        yield body


def _a85(b):
    b = b.strip()
    if b.endswith(b"~>"):
        b = b[:-2]
    return base64.a85decode(b)


def lines(path):
    """The strings drawn on each page, in order, one entry per text-showing operator."""
    data = open(path, "rb").read()
    out = []
    for body in streams(data):
        txt = body.decode("latin-1")
        if "BT" not in txt:
            continue
        for m in re.finditer(r"\((.*?)(?<!\\)\)\s*Tj|\[(.*?)\]\s*TJ", txt, re.S):
            if m.group(1) is not None:
                out.append(_unescape(m.group(1)))
            else:
                parts = re.findall(r"\((.*?)(?<!\\)\)", m.group(2), re.S)
                out.append("".join(_unescape(p) for p in parts))
    return out


def text(path):
    return " ".join(lines(path))
