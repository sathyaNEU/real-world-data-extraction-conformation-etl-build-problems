"""Replace the simple formulas a sheet is built with by their values, as a saved workbook carries them."""
import re

from openpyxl.utils import column_index_from_string, get_column_letter


def _val(ws, ref):
    m = re.fullmatch(r"([A-Z]+)(\d+)", ref)
    v = ws.cell(row=int(m.group(2)), column=column_index_from_string(m.group(1))).value
    if isinstance(v, str) and v.startswith("="):
        v = _eval(ws, v)
    return v or 0


def _eval(ws, f):
    m = re.fullmatch(r"=SUM\(([A-Z]+)(\d+):([A-Z]+)(\d+)\)", f)
    if m:
        c1, r1, c2, r2 = column_index_from_string(m.group(1)), int(m.group(2)), column_index_from_string(m.group(3)), int(m.group(4))
        return sum(_val(ws, "%s%d" % (get_column_letter(c), r)) for c in range(c1, c2 + 1) for r in range(r1, r2 + 1))
    m = re.fullmatch(r"=([A-Z]+\d+)([-*])([A-Z]+\d+)", f)
    if m:
        a, b = _val(ws, m.group(1)), _val(ws, m.group(3))
        return round(a - b, 2) if m.group(2) == "-" else round(a * b, 2)
    raise ValueError(f)


def freeze(wb):
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    c.value = _eval(ws, c.value)
