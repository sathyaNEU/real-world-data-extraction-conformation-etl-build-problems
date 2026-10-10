"""Deterministic file writers. Every container is normalised after writing: in-fiction author and
dates, no writer signature, fixed zip entry times, so two builds are byte-identical."""
import csv
import datetime as dt
import importlib.util
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SCRUB = os.path.join(REPO, ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py")
FIXED_ZIP_TIME = (2026, 10, 1, 9, 0, 0)


def load_scrub():
    spec = importlib.util.spec_from_file_location("scrub_producer_metadata", SCRUB)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_csv(path, header, rows, delimiter=","):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=delimiter, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def write_text(path, text, crlf=False):
    data = text.replace("\r\n", "\n")
    if crlf:
        data = data.replace("\n", "\r\n")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(data)


def normalize_ooxml(path, author, created, modified=None, app="Microsoft Excel", company=None):
    modified = modified or created
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}
    ciso = created.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    miso = modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    a = author.encode()
    if "docProps/core.xml" in data:
        b = data["docProps/core.xml"]
        b = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + a + rb"\g<2>", b)
        b = re.sub(rb"<dc:creator/>", b"<dc:creator>" + a + b"</dc:creator>", b)
        b = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)", rb"\g<1>" + a + rb"\g<2>", b)
        b = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + ciso + rb"\g<2>", b)
        b = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + miso + rb"\g<2>", b)
        b = re.sub(rb"<dc:description[^>]*>[^<]*</dc:description>", b"", b)
        b = re.sub(rb"<dc:description/>", b"", b)
        b = re.sub(rb"<cp:keywords[^>]*>[^<]*</cp:keywords>", b"", b)
        data["docProps/core.xml"] = b
    if "docProps/app.xml" in data:
        b = data["docProps/app.xml"]
        b = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app.encode() + b"</Application>", b)
        b = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", b)
        if company:
            b = re.sub(rb"<Company>[^<]*</Company>", b"<Company>" + company.encode() + b"</Company>", b)
        data["docProps/app.xml"] = b
    drop = {n for n in data if n.startswith("docProps/thumbnail")}
    if drop and "_rels/.rels" in data:
        data["_rels/.rels"] = re.sub(rb"<Relationship [^>]*thumbnail[^>]*/>", b"", data["_rels/.rels"])
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for i in infos:
            if i.filename in drop:
                continue
            zi = zipfile.ZipInfo(i.filename, date_time=FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zi.create_system = 0
            zo.writestr(zi, data[i.filename])
    os.replace(tmp, path)


def scrub_pdf(path, producer, stamp, floor="2024-01-01", ceiling="2026-10-10"):
    load_scrub().scrub_pdf(path, producer, stamp, floor, ceiling)


def set_mtime(path, when):
    t = when.timestamp()
    os.utime(path, (t, t))


def file_text(path):
    """Plain text of any shipped file, for the sweeps."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".csv", ".txt", ".eml", ".md"):
        return open(path, encoding="utf-8").read()
    if ext in (".xlsx", ".docx"):
        out = []
        with zipfile.ZipFile(path) as z:
            for n in z.namelist():
                if n.endswith(".xml"):
                    out.append(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf-8", "ignore")))
        return "\n".join(out)
    if ext == ".pdf":
        from pypdf import PdfReader
        return "\n".join(p.extract_text() for p in PdfReader(path).pages)
    return ""
