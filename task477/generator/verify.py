"""The independent verifier: reads only target/ and golden/, recomputes the call, every industry's growth and both
asks, and checks the golden table and memo carry them."""
import csv
import os
import re
import sys

import bundle as B
import methods as M
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))


def main(target, golden):
    fails = []

    def ok(label, cond):
        print("%s  verify: %s" % ("ok  " if cond else "FAIL", label))
        if not cond:
            fails.append(label)
    from pypdf import PdfReader
    g = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(B.find(target, "sector_partnership_fund")).pages))
    ok("pdf read back: guidelines 2.1 to 2.3 and 3.3", "1,000 or more" in g and "for the work they performed" in g
       and "four eligible industries with the highest growth" in g and "less any of those checks later voided" in g)
    rec = B.record(target)
    gr = M.route(rec, "golden")
    slate, nxt = M.slate(gr)
    ok("the call: %s, next %s" % (", ".join(slate), nxt), sorted(slate) == ["23", "51", "52", "54"] and nxt == "31-33")
    a, b = B.ask_a(target), B.ask_b(target)
    rows = list(csv.DictReader(open(B.find(golden, "sector_partnership_application"), encoding="utf-8")))
    for r in rows:
        s = r["naics_sector"]
        ok("%s: %d%%, %s, %d exiters, $%d" % (s, round(100 * gr[s]), r["on_slate"], a.get(s, 0), round(b.get(s, 0))),
           int(r["pay_per_job_growth_2021_2025_pct"]) == round(100 * gr[s]) and (r["on_slate"] == "Yes") == (s in slate)
           and int(r["exiters_employed_q2_after_exit"]) == a.get(s, 0) and
           int(r["ita_payments_2025_usd"]) == round(b.get(s, 0)))
    ok("the table has every eligible industry", sorted(r["naics_sector"] for r in rows) == M.eligible(rec))
    from docx import Document
    d = Document(B.find(golden, "sector_partnership_slate"))
    txt = " ".join(p.text for p in d.paragraphs)
    ok("the memo names the slate and the next in line",
       "Information, Finance and insurance, Professional, scientific, and technical services and Construction" in txt
       and "Manufacturing is next in line" in txt)
    ok("the memo carries the chart", len(d.inline_shapes) == 1)
    print("verify: %d failures" % len(fails))
    return not fails


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
