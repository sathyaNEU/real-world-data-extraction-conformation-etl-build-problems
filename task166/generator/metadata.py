"""Write task166/metadata.json from the built pack: the distractors, the input gates and every shipped file's source, date
and licence. Every file is constructed; none is labelled as a real organisation's release."""
import json
import os

import records as R

SOURCES = {
    R.F_LEDGER: "Marrowgate Books sales ledger, invoice lines and credit lines from 1 November 2021 to 30 October 2026 (SQLite extract)",
    R.F_TITLES: "Marrowgate Books title master at 30 October 2026, published and forthcoming editions",
    R.F_ACCOUNTS: "Marrowgate Books trade account master at 30 October 2026, with the account numbers used before the 2023 system change",
    R.F_RA: "Tallowmere Book Distribution, returns authorisations issued for Marrowgate accounts from 1 November 2024",
    R.F_RECEIPTS: "Tallowmere Book Distribution, returns received for Marrowgate from 1 November 2024, one row per delivery line",
    R.F_REINSPECT: "Tallowmere Book Distribution, re-inspection of hurt returns, a sheet a month from November 2025",
    R.F_PANEL: "Weekly UK consumer sales panel, Marrowgate ISBNs, weeks ending 2 November 2024 to 31 October 2026",
    R.F_PRINT: "Marrowgate Books production, print orders placed from 1 November 2024",
    R.F_STOCK: "Tallowmere Book Distribution, Marrowgate stock on hand at close of business 30 October 2026",
    R.F_TERMS: "Marrowgate Books terms of trade for bookselling customers, effective 1 March 2024",
    R.F_POLICY: "Marrowgate Books accounting policies (extract), draft for the FY2026 audit, September 2026",
}
DATES = {R.F_TERMS: "2024-03-01", R.F_POLICY: "2026-09-15"}
DISTRACTORS = [R.F_PRINT, R.F_STOCK]
TITLE = ("How much a London trade publisher should hold as its returns allowance at its 31 October 2026 year end against "
         "sale-or-return trade sales invoiced to that date")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
        wb.close()
        return n
    if path.endswith(".sqlite"):
        import sqlite3
        con = sqlite3.connect(path)
        n = sum(con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0] for t in ("invoice_lines", "credit_lines"))
        con.close()
        return n
    return None


def write(task_dir, n=None):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": DATES.get(f, "2026-10-30"),
                    "license": "CC0 public domain dedication (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task166",
        "title": TITLE,
        "domain": "Actuarial Science & Insurance",
        "client_domain": "Actuarial Science & Insurance",
        "house_domain": "accounting-audit-forensic",
        "subdomain": "reserving-development-triangles (the year-end returns allowance on sale-or-return book sales)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "the year-end returns allowance and its hardback part in pounds, the copies received back by channel "
                        "and quarter of the financial year, and the share of those copies written off by channel and by format",
        "as_of": "2026-10-31",
        "deliverables": ["returns_allowance_FY2026.xlsx", "returns_allowance_note.pdf"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task166/generator/build.py (seeded, deterministic) around a "
                               "fictional London trade publisher and its distributor, in the layouts of a sales ledger "
                               "extract, a title master, an account master, a distributor's returns exports, a consumer "
                               "sales panel extract and PDF documents; the companies, people, titles and ISBNs are "
                               "constructed, and no real organisation's records or person is depicted.",
                     "date": "2026-10-30", "license": "CC0 public domain dedication (original work)"}],
        "created": "2026-11-01",
        "generator": "task166/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
