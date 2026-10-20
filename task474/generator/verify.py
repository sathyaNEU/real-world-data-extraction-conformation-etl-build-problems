"""The independent verifier: reads only target/ and golden/, recomputes the call and the terminal figures, and checks
the golden workbook and memo carry them."""
import os
import re
import sys

from openpyxl import load_workbook
from pypdf import PdfReader

import bundle as B
import methods as M

HERE = os.path.dirname(os.path.abspath(__file__))


def main(target, golden):
    fails = []

    def ok(label, cond):
        print("%s  verify: %s" % ("ok  " if cond else "FAIL", label))
        if not cond:
            fails.append(label)
    g = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(target, "air_corridor")).pages))
    ok("pdf read back: rules 2.2, 2.3, 3.1", "times the class's NOx emission rate in the 2026 emission rate table" in g
       and "5.00 tonnes or more" in g and "from passing its in-gate to passing its out-gate" in g)
    rate = B.nox(target)
    call = M.designated(rate)
    ok("the call: %s" % ", ".join(call), call == ["L01", "L03", "L05", "L14"])
    wb = load_workbook(B.find(golden, "air_corridor_links"), read_only=True)
    rows = {r[0]: r for r in wb["Links"].iter_rows(values_only=True) if r and str(r[0]).startswith("L")}
    for k in sorted(rate):
        ok("%s: %.2f t per mile, %s" % (k, rate[k], rows[k][2]), (rows[k][2] == "Yes") == (k in call))
    ga = B.gate_asks(target)
    got = [r for r in wb["Terminal gates"].iter_rows(min_row=4, values_only=True) if r and r[1] and "20" in str(r[1])]
    ok("terminal rows: 12", len(got) == 12)
    vals = sorted((r[2], r[3]) for r in got)
    want = sorted((ga[k][0], round(ga[k][1], 1)) for k in ga)
    ok("terminal figures match the recomputation", vals == want)
    m = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(golden, "air_corridor_designations")).pages))
    ok("the memo designates the four", "L01, L03, L05 and L14" in m)
    print("verify: %d failures" % len(fails))
    return not fails


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
