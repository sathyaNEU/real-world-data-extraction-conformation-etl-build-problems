"""Write task156/metadata.json from the built pack: the distractors, the portal's keys, the input gates and every
shipped file's source, date and licence."""
import json
import os

import docs as DOC
import records as R

SOURCES = {
    R.F_INBOX: "Millrind review platform, daily review inbox export by site, entry day and item type (pulled 8 "
               "October 2026)",
    R.F_INBOX_PRE: "Millrind review platform, daily review inbox export for September 2026 as first pulled on 2 "
                   "October 2026",
    R.F_OLD: "Millrind community operations, the old review system's monthly queue workbook, 2021 to 2023",
    R.F_ROSTER: "Millrind review platform, reviewer roster (access spells by reviewer and site)",
    R.F_FLAGSUM: "Millrind moderator tool, daily flag summary by site",
    R.F_POSTS: "Millrind posts warehouse, questions by site and month",
    R.F_PLAN: "Millrind Planning & Analytics, 2027 question plan by site and month",
    R.F_REGISTER: "Millrind site register",
    R.F_FLAGS1: "Millrind moderator tool, flag export (flags raised 1 July to 15 August 2026)",
    R.F_FLAGS2: "Millrind moderator tool, flag export (flags raised 15 August to 30 September 2026)",
    R.F_REVIEWS: "Millrind moderation quality programme, decision-review log for flag decisions",
    R.F_WFM: "Millrind WFM system, shift line export, January to September 2026",
    R.F_ASSIGN: "Millrind HR, assignment history for the paid moderation team",
    R.F_MOVES: "Millrind moderators' log of questions moved between sites, 2021 to 2023",
    R.F_PAGEVIEWS: "Millrind web analytics, page views and unique visitors by site and month",
    DOC.F_CHARTER: "Millrind Moderation Council charter, as amended 12 March 2025",
    DOC.F_STANDARDS: "Millrind Moderation Council, handle-time standards for 2027 (17 June 2026)",
    DOC.F_ENVELOPE: "Millrind Finance, 2027 envelope letter for paid moderation (30 September 2026)",
    DOC.F_FLAGSTD: "Millrind moderation operations, flag service standard (revised 4 February 2026)",
    DOC.F_SURVEY: "Millrind community research, 2026 member survey on AI assistants (2 June 2026)",
    DOC.F_OPS: "Millrind moderation operations notes (6 October 2026)",
    DOC.F_WAREHOUSE: "Millrind data platform team, posts warehouse notes",
    DOC.F_DICT: "Millrind review platform and moderator tool, export field notes",
    DOC.F_FILELIST: "Millrind moderation operations, list of the files pulled for the 2027 pool request (9 October "
                    "2026)",
}
DISTRACTORS = [R.F_PAGEVIEWS, DOC.F_SURVEY]
TITLE = ("How many paid moderator FTE a developer question-and-answer network's council requests for 2027 across its "
         "nine topic sites, when community review items reach the paid team only after volunteer reviewers have left "
         "them for 72 hours")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
    return None


def write(task_dir, n=None):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": "2026-10-09",
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task156",
        "title": TITLE,
        "domain": "Product Analytics",
        "client_domain": "Product Analytics",
        "house_domain": "product-analytics",
        "subdomain": "retention-cohort-lifetime-value-modeling (trust and safety at a developer Q&A network: each "
                     "site's volunteer reviewer pool carried forward on its own monthly lapse rate, and the reviews a "
                     "retained reviewer delivers when the inbox outruns the pool, set against the 2027 inbox the "
                     "question plan implies)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "a committed FTE request with each of nine sites' whole-FTE need and the distance from finance's "
                        "envelope, a stacked monthly chart of paid review hours by site from January 2024 to December "
                        "2027 with the envelope drawn across, and three tables (each site's share of flags first acted "
                        "on within 24 hours in July, August and September 2026; each site's paid moderators' hours "
                        "worked in the first three quarters of 2026; each site's January to September 2026 questions "
                        "as a percentage of 2022's)",
        "as_of": "2026-10-09",
        "deliverables": ["moderation_pool_2027.xlsx", "council_pool_request_2027.pptx"],
        "distractor_files": DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task156/generator/build.py (seeded, deterministic) around "
                               "a fictional Toronto-run developer question-and-answer network of nine topic sites, in "
                               "the layouts of a review platform's daily inbox export and reviewer roster, an older "
                               "review system's monthly queue workbook, a moderator tool's flag exports, a posts "
                               "warehouse, a planning team's question plan, a WFM system's shift lines and an HR "
                               "assignment history; no real organisation's records or person is depicted.",
                     "date": "2026-10-09", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-17",
        "generator": "task156/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
