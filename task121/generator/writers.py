"""File writers with deterministic bytes and the container clean-up every binary goes through:
in-fiction authors and dates, no writer signature, fixed zip entry times."""
import datetime as dt
import io
import os
import re
import zipfile

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

ORG = "Ventania Merch"
ZIP_TIME = (2026, 9, 28, 9, 0, 0)


def write_csv(df, path):
    # the warehouse writes booleans in lower case
    df = df.copy()
    for c in df.columns:
        if df[c].dtype == bool:
            df[c] = df[c].map({True: "true", False: "false"})
    df.to_csv(path, index=False, lineterminator="\n")


def write_parquet(df, path):
    tbl = pa.Table.from_pandas(df, preserve_index=False).replace_schema_metadata(None)
    buf = io.BytesIO()
    pq.write_table(tbl, buf, compression="zstd", compression_level=9, use_dictionary=True,
                   write_statistics=True, row_group_size=60000, store_schema=False)
    b = buf.getvalue()
    m = re.search(rb"parquet-cpp-arrow version [0-9.]+", b)
    if m:
        old = m.group(0)
        new = b"Ventania datalake export v2.14.0"
        assert len(new) == len(old), (old, new)
        b = b.replace(old, new)
    open(path, "wb").write(b)


def normalize_ooxml(path, author, created, modified=None, app="Microsoft Excel"):
    modified = modified or created
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}
    ciso = created.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    miso = modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    a = author.encode("utf-8")
    if "docProps/core.xml" in data:
        b = data["docProps/core.xml"]
        b = re.sub(rb"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", rb"\g<1>" + a + rb"\g<2>", b)
        b = re.sub(rb"(<cp:lastModifiedBy[^>]*>)[^<]*(</cp:lastModifiedBy>)", rb"\g<1>" + a + rb"\g<2>", b)
        b = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + ciso + rb"\g<2>", b)
        b = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + miso + rb"\g<2>", b)
        b = re.sub(rb"<dc:description[^>]*>[^<]*</dc:description>", b"", b)
        b = re.sub(rb"<dc:description[^>]*/>", b"", b)
        data["docProps/core.xml"] = b
    if "docProps/app.xml" in data:
        b = data["docProps/app.xml"]
        b = re.sub(rb"<Application>[^<]*</Application>", b"<Application>" + app.encode() + b"</Application>", b)
        b = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", b)
        data["docProps/app.xml"] = b
    drop = {n for n in data if n.startswith("docProps/thumbnail")}
    if drop and "_rels/.rels" in data:
        data["_rels/.rels"] = re.sub(rb"<Relationship [^>]*thumbnail[^>]*/>", b"", data["_rels/.rels"])
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zo:
        for i in infos:
            if i.filename in drop:
                continue
            zi = zipfile.ZipInfo(i.filename, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zi.create_system = 0
            zo.writestr(zi, data[i.filename])
    os.replace(tmp, path)


def normalize_pdf(path, when, producer=ORG):
    """reportlab's invariant mode fixes dates at 2000-01-01 and the document ID; move the dates to
    the document's own date and replace the producer, keeping every byte offset."""
    b = open(path, "rb").read()
    n0 = len(b)
    stamp = when.strftime("D:%Y%m%d%H%M%S").encode()
    b = re.sub(rb"D:20000101000000", stamp, b)
    for key in (rb"/Producer", rb"/Creator"):
        m = re.search(key + rb" \(((?:\\.|[^\\)])*)\)", b)   # values may hold escaped parentheses
        if m:
            old = m.group(1)
            new = producer.encode()
            assert len(new) <= len(old), (old, new)
            k = m.start(1)
            b = b[:k] + new + b")" + b" " * (len(old) - len(new)) + b[m.end(1) + 1:]
    for tok in (rb"ReportLab Generated PDF document", rb"ReportLab", rb"reportlab"):
        for mm_ in list(re.finditer(rb"%[^\n]*" + tok + rb"[^\n]*", b)):
            line = mm_.group(0)
            b = b.replace(line, b"%" + b" " * (len(line) - 1))
        b = re.sub(tok, lambda x: b"x" * len(x.group(0)), b)
    assert len(b) == n0, "PDF length moved"
    open(path, "wb").write(b)


def set_mtime(root, when):
    ts = when.timestamp()
    for d, _, fs in os.walk(root):
        for f in fs:
            os.utime(os.path.join(d, f), (ts, ts))
