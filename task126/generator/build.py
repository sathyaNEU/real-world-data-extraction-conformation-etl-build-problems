"""task126 pack generator: python3 build.py <out_dir> [--record <json>]

Writes <out_dir>/target/ (the evidence bundle) and <out_dir>/metadata.json, then runs every assertion in
checks.py against the in-memory world and the written files. Deterministic: two runs are byte-identical."""
import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import analysis as AN   # noqa: E402
import checks           # noqa: E402
import docs             # noqa: E402
import params as P      # noqa: E402
import tables as TB     # noqa: E402
import workbooks as WB  # noqa: E402
import world            # noqa: E402
import writers as WR    # noqa: E402

T0 = dt.datetime
WHEN = {
    "examination_dockets_FY2016_FY2026.parquet": T0(2026, 10, 2, 9, 12),
    "office_actions_FY2016_FY2026.parquet": T0(2026, 10, 2, 9, 31),
    "docket_links.csv": T0(2026, 10, 2, 9, 14),
    "docket_transfers.csv": T0(2026, 10, 2, 9, 15),
    "examiner_production_ledger_FY2016_FY2026.parquet": T0(2026, 10, 2, 9, 47),
    "art_unit_groups.csv": T0(2026, 10, 2, 9, 16),
    "examiner_roster_2026-09-30.csv": T0(2026, 9, 30, 17, 36),
    "docketing_codebook.md": T0(2026, 10, 2, 9, 58),
    "extract_notes.md": T0(2026, 10, 15, 11, 20),
    "saravel_ipo_acknowledgements_FY2019-FY2022.xlsx": T0(2026, 10, 14, 15, 3),
    "annual_report_2025_tables_P1_P2.xlsx": T0(2025, 12, 18, 12, 40),
    "report_table_notes.docx": T0(2024, 10, 11, 14, 22),
    "performance_reporting_charter.pdf": T0(2024, 9, 9, 16, 5),
    "examiner_production_standard_2019.pdf": T0(2018, 9, 14, 10, 30),
    "international_pendency_comparison_2025.xlsx": T0(2025, 11, 20, 10, 2),
    "headline_section_thread.eml": T0(2026, 10, 13, 16, 42),
}
DISTRACTORS = ["examiner_roster_2026-09-30.csv", "international_pendency_comparison_2025.xlsx"]
DELIVERABLES = ["fy2022_pendency_headline.docx", "fy2022_time_to_decision.svg"]


def build_world():
    W = world.World().build()
    A = AN.Arrays(W)
    T = TB.Tables(W)
    return W, A, T


def p1_published(A):
    rows = AN.p1_table(A)
    for fy, r in rows.items():
        r["reported"] = r["closed_share"] >= 0.98 and r["med25"] is not None
        r["published"] = AN.r1(r["med25"]) if r["reported"] else None
    return rows


def p2_counts(T, drows):
    out = {(g, fy): 0 for g in P.GROUPS for fy in range(2021, 2026)}
    for r in drows:
        fy = P.fy_of(dt.date.fromisoformat(r["docketed_on"]).toordinal())
        if 2021 <= fy <= 2025:
            out[(r["tg"], fy)] += 1
    return out


def write_pack(out):
    tgt = Path(out) / "target"
    if tgt.exists():
        shutil.rmtree(tgt)
    tgt.mkdir(parents=True)
    W, A, T = build_world()
    ctx = dict(W=W, A=A, T=T, tgt=tgt)
    rows = {}
    drows = T.dockets()
    rows["examination_dockets_FY2016_FY2026.parquet"] = WR.write_parquet(
        tgt / "examination_dockets_FY2016_FY2026.parquet",
        ["docket_no", "docketed_on", "art_unit", "tg", "examiner_id", "closed_on", "end_code"],
        ["str", "date", "str", "str", "str", "date", "str"], drows)
    T.actions()
    arows = T.action_rows()
    rows["office_actions_FY2016_FY2026.parquet"] = WR.write_parquet(
        tgt / "office_actions_FY2016_FY2026.parquet", ["action_id", "docket_no", "action_code", "served_on"],
        ["str", "str", "str", "date"], arows)
    lrows = T.ledger_rows()
    rows["examiner_production_ledger_FY2016_FY2026.parquet"] = WR.write_parquet(
        tgt / "examiner_production_ledger_FY2016_FY2026.parquet",
        ["credit_id", "pay_period", "examiner_id", "action_id", "credit_class", "counts"],
        ["str", "str", "str", "str", "str", "float"], lrows)
    links = T.links()
    rows["docket_links.csv"] = WR.write_csv(tgt / "docket_links.csv", links,
                                            ["parent_docket", "child_docket", "link_type", "linked_on"])
    xf = T.transfers()
    rows["docket_transfers.csv"] = WR.write_csv(tgt / "docket_transfers.csv", xf,
                                                ["docket_no", "transferred_on", "from_au", "to_au"])
    au = T.art_unit_rows()
    rows["art_unit_groups.csv"] = WR.write_csv(tgt / "art_unit_groups.csv", au,
                                               ["art_unit", "tg", "tg_name", "valid_from", "valid_to"])
    ro = T.roster_rows()
    rows["examiner_roster_2026-09-30.csv"] = WR.write_csv(
        tgt / "examiner_roster_2026-09-30.csv", ro,
        ["examiner_id", "grade", "home_art_unit", "tg", "fte", "on_roster_since"])
    C = AN.corpus(A)
    quarters = AN.corpus_quarters(A, C, C["e3"])
    rows["saravel_ipo_acknowledgements_FY2019-FY2022.xlsx"] = WB.saravel(
        tgt / "saravel_ipo_acknowledgements_FY2019-FY2022.xlsx", A, T, C, quarters,
        WHEN["saravel_ipo_acknowledgements_FY2019-FY2022.xlsx"])
    p1 = p1_published(A)
    p2 = p2_counts(T, drows)
    WB.annual_tables(tgt / "annual_report_2025_tables_P1_P2.xlsx", p1, p2,
                     WHEN["annual_report_2025_tables_P1_P2.xlsx"])
    WB.international(tgt / "international_pendency_comparison_2025.xlsx",
                     WHEN["international_pendency_comparison_2025.xlsx"])
    for key, d, author in (("performance_reporting_charter.pdf", docs.CHARTER, "Performance Statistics Unit"),
                           ("examiner_production_standard_2019.pdf", docs.STANDARD,
                            "Examination Practice Directorate")):
        WR.write_pdf(tgt / key, d["title"], d["sub"], d["by"], d["blocks"], author, WHEN[key], author)
    WR.write_docx(tgt / "report_table_notes.docx", docs.TABLE_NOTES["title"], docs.TABLE_NOTES["blocks"],
                  "Performance Statistics Unit", WHEN["report_table_notes.docx"], "Performance Statistics Unit")
    WR.write_text(tgt / "docketing_codebook.md", docs.CODEBOOK)
    WR.write_text(tgt / "headline_section_thread.eml", docs.THREAD)
    WR.write_text(tgt / "extract_notes.md", docs.extract_notes(rows))
    for name, when in WHEN.items():
        WR.set_mtime(tgt / name, when)
    ctx.update(rows=rows, drows=drows, arows=arows, lrows=lrows, links=links, xf=xf, au=au, ro=ro, C=C,
               quarters=quarters, p1=p1, p2=p2)
    return ctx


def metadata(out, ctx):
    tgt = ctx["tgt"]
    files = []
    for name in sorted(WHEN):
        p = tgt / name
        files.append({"path": name, "format": p.suffix.lstrip("."), "bytes": p.stat().st_size,
                      "rows": ctx["rows"].get(name),
                      "source": "Constructed for this task: fictional Morvane Patent Office and Saravel "
                                "Intellectual Property Office; synthetic records, no third-party data",
                      "date": WHEN[name].date().isoformat(), "license": "CC BY 4.0 (original synthetic work)"})
    big = max((f for f in files if f["rows"]), key=lambda f: f["rows"])
    meta = {
        "task": "task126", "domain": "Policy & Education", "subdomain": "public-administration",
        "objective": "Descriptive & Distribution Analysis", "as_of": P.AS_OF.isoformat(),
        "deliverables": DELIVERABLES, "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({f["format"] for f in files}),
                        "largest_file_rows": big["rows"], "largest_file": big["path"]},
        "files": files,
    }
    with open(Path(out) / "metadata.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(meta, indent=1, ensure_ascii=False) + "\n")
    return meta


def main():
    out = sys.argv[1]
    rec_path = sys.argv[sys.argv.index("--record") + 1] if "--record" in sys.argv else None
    ctx = write_pack(out)
    meta = metadata(out, ctx)
    ctx["meta"] = meta
    ctx["out"] = Path(out)
    record, failed = checks.run(ctx)
    if rec_path:
        with open(rec_path, "w") as fh:
            json.dump(record, fh, indent=1, default=str)
    n = len(record["assertions"])
    print("assertions: %d, failed: %d" % (n, len(failed)))
    for f in failed:
        print("FAILED", f)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
