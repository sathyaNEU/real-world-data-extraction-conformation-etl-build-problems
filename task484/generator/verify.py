"""The independent verifier: reads only target/ and golden/, recomputes the tiers and the housing authorized, and
checks the golden workbook and memo carry them."""
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
    g = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(target, "revenue_sharing")).pages))
    ok("pdf read back: rules 2.2, 2.3, 3.1", "estimated by the housing unit method" in g and "50,000 or more" in g
       and "A building counts in the year its first permit was issued" in g)
    pop = B.population(target)
    up = B.tier(pop)
    ok("the tier: %s" % ", ".join(up), up == ["Fairhaven", "Linden"])
    wb = load_workbook(B.find(golden, "city_population_estimates"), read_only=True)
    rows = [r[0] for r in wb["Tiers"].iter_rows(min_row=4, values_only=True) if r and r[1] == "Yes"]
    ok("the workbook lists the upper tier", sorted(rows) == up)
    au = B.authorized(target)
    got = {r[0]: (r[1], r[2]) for r in wb["Housing authorized 2025"].iter_rows(min_row=4, values_only=True)
           if r and r[0] in au}
    ok("housing authorized matches the recomputation", got == au)
    m = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(golden, "revenue_sharing_tiers")).pages))
    ok("the memo names the pair", "Fairhaven and Linden" in m)
    print("verify: %d failures" % len(fails))
    return not fails


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
