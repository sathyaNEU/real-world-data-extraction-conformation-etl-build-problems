"""task127 generator: deterministic writers for the data files.

CSV: fixed column order, "\n" line endings. XLSX: xlsxwriter with a fixed creation date; the container is
normalised afterwards (fixed entry times and order) and its core properties scrubbed.
"""
import io
import json
import zipfile
from datetime import date, datetime

import pandas as pd
import xlsxwriter

import params as P


def write_csv(df, path):
    df.to_csv(path, index=False, lineterminator="\n")


def write_json(obj, path):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


def workbook(path, author, created):
    wb = xlsxwriter.Workbook(str(path), {"default_date_format": "yyyy-mm-dd", "strings_to_numbers": False})
    wb.set_properties({"author": author, "created": created, "company": P.FUND})
    return wb


def sheet_table(wb, name, df, top=None, widths=None, date_cols=(), num_fmt=None):
    """Write a frame as a plain table; `top` is a list of lines above the header (header row = len(top))."""
    ws = wb.add_worksheet(name)
    bold = wb.add_format({"bold": True})
    hdr = wb.add_format({"bold": True, "bottom": 1})
    dfmt = wb.add_format({"num_format": "yyyy-mm-dd"})
    nfmt = wb.add_format({"num_format": num_fmt or "#,##0"})
    r0 = 0
    for i, line in enumerate(top or []):
        ws.write(i, 0, line, bold if i == 0 else None)
        r0 = i + 1
    for j, col in enumerate(df.columns):
        ws.write(r0, j, col, hdr)
    for i, row in enumerate(df.itertuples(index=False), start=r0 + 1):
        for j, v in enumerate(row):
            col = df.columns[j]
            if v is None or (isinstance(v, float) and pd.isna(v)):
                continue
            if col in date_cols and isinstance(v, date):
                ws.write_datetime(i, j, datetime(v.year, v.month, v.day), dfmt)
            elif isinstance(v, (int,)) and not isinstance(v, bool):
                ws.write_number(i, j, v, nfmt)
            elif isinstance(v, float):
                ws.write_number(i, j, v)
            else:
                ws.write_string(i, j, str(v))
    for j, w in enumerate(widths or [14] * len(df.columns)):
        ws.set_column(j, j, w)
    ws.freeze_panes(r0 + 1, 0)
    return ws


def normalise_zip(path, when=(2026, 12, 10, 16, 0, 0)):
    """Rewrite an OOXML container with fixed entry timestamps, contents and order unchanged."""
    with zipfile.ZipFile(path) as z:
        data = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for name, blob in data:
            zi = zipfile.ZipInfo(name, date_time=when)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            out.writestr(zi, blob)
    with open(path, "wb") as f:
        f.write(buf.getvalue())
