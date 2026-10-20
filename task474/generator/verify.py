"""The independent verifier: reads only target/ and golden/, recomputes the call and the pharmacy summary, and checks
the golden workbook and memo carry them."""
import os
import re
import sys

from openpyxl import load_workbook
from pypdf import PdfReader

import bundle as B

HERE = os.path.dirname(os.path.abspath(__file__))


def main(target, golden):
    fails = []

    def ok(label, cond):
        print("%s  verify: %s" % ("ok  " if cond else "FAIL", label))
        if not cond:
            fails.append(label)
    g = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(target, "cost_performance")).pages))
    ok("pdf read back: rules 2.2, 2.3, 3.1", "covered by the plan in the same six months" in g and "$412.00 or more" in g
       and "as the pharmacy claims stand on 31 October 2026" in g)
    rate = B.pmpm(target)
    call = sorted(k for k, v in rate.items() if v >= 412.0)
    ok("the call: %s" % ", ".join(call), call == ["PG04", "PG07", "PG08", "PG10"])
    wb = load_workbook(B.find(golden, "provider_group_pmpm"), read_only=True)
    rows = {r[0]: r for r in wb["Groups"].iter_rows(values_only=True) if r and str(r[0]).startswith("PG")}
    for k in sorted(rate):
        ok("%s: %.2f, %s" % (k, rate[k], rows[k][2]), (rows[k][2] == "Yes") == (k in call))
    ph = B.pharmacy(target)
    prow = {r[0]: r for r in wb["Pharmacy"].iter_rows(values_only=True) if r and r[0] in ph}
    for c in sorted(ph):
        ok("%s: $%d, %d fills" % (c, int(ph[c][0] + .5), ph[c][1]),
           prow[c][1] == int(ph[c][0] + .5) and prow[c][2] == ph[c][1])
    m = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(golden, "provider_group_designations")).pages))
    ok("the memo designates the four", "PG04, PG07, PG08 and PG10" in m)
    print("verify: %d failures" % len(fails))
    return not fails


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
