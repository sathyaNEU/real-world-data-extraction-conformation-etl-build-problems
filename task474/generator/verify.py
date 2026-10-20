"""The independent verifier: reads only target/ and golden/, recomputes the call and both asks, and checks the golden
workbook and memo carry them."""
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
    g = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(target, "scr_upgrade_program")).pages))
    ok("pdf read back: rules 2.2, 2.3, 3.1, 3.2", "the NOx the unit emitted while operating" in g and "0.170 lb per MWh"
       in g and "gas day the hour falls in" in g and "IEEE Std 762" in g)
    rec = B.record(target)
    call = M.designated(rec, "golden")
    ok("the call: %s" % ", ".join(call), call == ["AF-1", "AF-2", "CB-1", "CB-2", "DF-1", "DF-3", "SR-1"])
    a, b = B.ask_a(target), B.ask_b(target)
    ws = load_workbook(B.find(golden, "cc_unit_nox_inventory"), read_only=True).active
    rows = {r[0]: r for i, r in enumerate(ws.iter_rows(values_only=True)) if i >= 3 and r and r[0] in rec}
    for u in sorted(rec):
        w = rows[u]
        c = 100 * int(a[u] / 100.0 + .5)
        ok("%s: %s, $%d, EFOR %.1f" % (u, w[2], c, b[u]),
           (w[2] == "Yes") == (u in call) and w[3] == c and abs(w[4] - round(b[u], 1)) < 1e-9)
    m = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(golden, "scr_upgrade_designations")).pages))
    ok("the memo designates the seven", "AF-1, AF-2, CB-1, CB-2, DF-1, DF-3 and SR-1" in m)
    print("verify: %d failures" % len(fails))
    return not fails


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
