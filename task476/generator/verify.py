"""The independent verifier: reads only target/ and golden/, recomputes the call, every graded tract figure and both
asks, and checks the golden workbook and memo carry them."""
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
    g = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(target, "nsf_2027_program")).pages))
    ok("pdf read back: guidelines 3.1 and 3.2 (the tests, the rate, the margins, the area)",
       "at least three of its listed 2020 census tracts" in g and "is more than 1.645" in g and
       "the rate for the area the 2020 tract covers" in g and "square root of the sum of their squared margins" in g)
    rows = B.tract_table(target)
    call, cnt = B.designated(rows)
    ok("the call: %s" % ", ".join(call), call == ["Dunmore Heights", "Kestrel Park"])
    wb = load_workbook(B.find(golden, "nsf_2027_tract_poverty_change"), read_only=True)
    tr = {str(r[2]): r for i, r in enumerate(wb["Tracts"].iter_rows(values_only=True)) if i and r[0]}
    for r in rows:
        w = tr[r["geoid"]]
        ok("%s %s: %.1f ± %.1f, %.1f ± %.1f, %s" % (r["nbhd"], r["geoid"][-6:], 100 * r["r18"], 100 * r["m18"],
                                                    100 * r["r23"], 100 * r["m23"], r["qual"]),
           "%.1f" % w[3] == "%.1f" % (100 * r["r18"]) and "%.1f" % w[4] == "%.1f" % (100 * r["m18"]) and
           "%.1f" % w[5] == "%.1f" % (100 * r["r23"]) and "%.1f" % w[6] == "%.1f" % (100 * r["m23"]) and
           (w[11] == "Yes") == r["qual"])
    nb = {r[0]: r for i, r in enumerate(wb["Neighborhoods"].iter_rows(values_only=True)) if i and r[0] != "Total"}
    a, b = B.ask_a(target), B.ask_b(target)
    for k in sorted(cnt):
        w = nb[k]
        ok("%s: %d qualifying, %d open properties, %d days, $%d, %d paid" % (k, cnt[k], a[k][0], round(a[k][1]),
                                                                            round(b[k][0]), b[k][1]),
           w[1] == cnt[k] and (w[2] == "Yes") == (k in call) and w[3] == a[k][0] and w[4] == round(a[k][1]) and
           w[5] == round(b[k][0]) and w[6] == b[k][1])
    m = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(golden, "nsf_2027_designation"))
                                    .pages))
    ok("the memo recommends the two", "recommends designating Dunmore Heights and Kestrel Park" in m)
    print("verify: %d failures" % len(fails))
    return not fails


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
