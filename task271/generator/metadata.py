"""Write task271/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_HESS: "Hessenby Analytics, per-execution export for Fenmarsh Investment Management's central dealing desk, with "
              "the consolidated mid at the execution and 1, 5, 30, 60 and 300 seconds after (pulled 2 November 2026)",
    R.F_ASHL: "Ashlowe Securities, execution report for Fenmarsh Investment Management, 2026",
    R.F_PEMB: "Pemberwick & Co, monthly execution reports for Fenmarsh Investment Management, 2026",
    R.F_OMS: "Fenmarsh Investment Management order management system, parent orders, 2026",
    R.F_VENUES: "Fenmarsh Investment Management central dealing desk, venue register",
    R.F_MASTER: "Fenmarsh Investment Management securities reference team, UK equities master (30 October 2026)",
    R.F_CA: "Fenmarsh Investment Management securities reference team, 2026 corporate actions",
    R.F_CAL: "Fenmarsh Investment Management operations, UK trading calendar",
    R.F_ORDERS: "Fenmarsh Wealth platform, client order book export (orders placed 29 December 2025 to 30 October 2026)",
    R.F_NOTES: "Gresmere Stockbrokers, contract notes for Fenmarsh Wealth's clients, settling 2 January to 3 November "
               "2026",
    R.F_AUCT: "Wexcombe Stock Exchange, daily closing auction statistics for the desk's universe, 2026",
    DOC.F_POLICY: "Fenmarsh Investment Management, Order Execution Policy 2025.2 (15 September 2025)",
    DOC.F_PLAN: "Fenmarsh Wealth, client dealing from 4 January 2027, paper for the board (12 October 2026)",
    DOC.F_ROUTER: "Fenmarsh Investment Management central dealing desk, router configuration 2026 (5 January 2026)",
    DOC.F_REPORT: "Fenmarsh Investment Management, top five execution venues for 2025 (28 April 2026)",
}
DISTRACTORS = [R.F_AUCT, DOC.F_REPORT]
TITLE = ("Which execution venues an asset manager's wealth board keeps off its platform's venue list when the group's "
         "central dealing desk starts dealing for the platform, on each venue's adverse move in the minute after a fill")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(sum(1 for _ in ws.iter_rows(values_only=True)) - 1, 0) for ws in wb.worksheets)
    return None


def write(task_dir, n=None):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-11-04",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task271",
        "title": TITLE,
        "domain": "Quantitative Finance",
        "client_domain": "Quantitative Finance",
        "subdomain": "market-microstructure-execution-cost (an asset manager's venue list for its wealth platform's "
                     "in-house dealing orders, each venue's adverse move in the minute after a fill read from a year "
                     "of the central desk's algorithmic fills)",
        "objective": "Descriptive & Distribution Analysis",
        "prompt_shape": "a scorecard of eight venues against the policy's 1.5 basis point line with each venue's adverse "
                        "move in whole basis points and a chart, and two tables (the mean size against average daily "
                        "volume of the platform's 2026 dealt orders as 2027 market orders at each dealing point; the "
                        "value bought less the value sold through Gresmere in each month to October)",
        "as_of": "2026-11-04",
        "deliverables": ["venue_list_board_paper_2027.pdf", "venue_review_2027.xlsx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task271/generator/build.py (seeded, deterministic) around "
                               "a fictional London asset manager, its wealth platform and its two brokers, in the "
                               "layouts of a transaction cost provider's per-execution export, brokers' execution "
                               "reports, an order management system's export, a platform's client order book and a "
                               "stockbroker's contract notes; no real organisation's records or person is depicted.",
                     "date": "2026-11-04", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-27",
        "generator": "task271/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
