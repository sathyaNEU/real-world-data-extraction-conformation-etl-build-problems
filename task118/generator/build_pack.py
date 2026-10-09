"""Build the task118 evidence pack: python3 build_pack.py [--out DIR]

Writes DIR/target/ and DIR/metadata.json (DIR defaults to the task folder), then runs every assertion in
checks.py against the files as written. Exit status 0 only when every assertion holds.
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import xlsxwriter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import params as P          # noqa: E402
import world                # noqa: E402
import asks                 # noqa: E402
import docs                 # noqa: E402
import spine as SP          # noqa: E402
import archive as AR        # noqa: E402

TASK = HERE.parent
REPO = TASK.parent
SCRUB = REPO / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"

F = dict(
    spine="pageviews_by_source_age_2025-10_2026-09.parquet",
    archive="headline_tests_archive_2019-2026.csv",
    staff="newsroom_staff_list_2026-10-12.xlsx",
    plan="audience_plan_2027.xlsx",
    changelog="headline_squad_change_log.xlsx",
    fieldref="audience_warehouse_field_reference.md",
    charter="headline_squad_2027_placement_brief.pdf",
    desks="desk_register.csv",
    dashboard="experimentation_dashboard_export_2026-10-01.csv",
    cms="cms_revisions_web_desks_2025-10_2026-09.csv",
    cmsnotes="cms_revisions_export_fields.txt",
    policy="editorial_standards_s7_corrections.pdf",
    panel="panel_monthly_audience_2025-10_2026-09.csv",
    panelwb="panel_reference_workbook.xlsx",
    bulletin="standards_bulletin_2026-04.docx",
    thread="squad_placement_thread.eml",
    agreement="newsfold_syndication_agreement.pdf",
    newsletter="newsletter_performance_2026-07_2026-09.csv",
    exportlog="audience_data_export_log.csv",
)
# The dashboard export is the licensed wrong basis's instrument (rung 0): declared as a wrong-basis distractor.
DISTRACTORS = ["agreement", "newsletter", "dashboard"]
EXPORT_STAMP = dt.datetime(2026, 10, 16, 9, 0)      # AEST: the folder as handed over; no file is later than this
# AEST wall clock at which each file was last written: its mtime, a workbook's last save, a document's own date.
# The six extract runs are the export log's; every other file keeps the date its own owner gave it. The change
# log's save is computed from its rows (changelog_saved).
STAMP = dict(
    dashboard=dt.datetime(2026, 10, 1, 9, 14), newsletter=dt.datetime(2026, 10, 2, 10, 38),
    fieldref=dt.datetime(2026, 10, 2, 16, 52), plan=dt.datetime(2026, 10, 9, 14, 5),
    staff=dt.datetime(2026, 10, 12, 8, 46), charter=dt.datetime(2026, 10, 12, 16, 20, 41),
    panel=dt.datetime(2026, 10, 15, 16, 18), panelwb=dt.datetime(2026, 10, 15, 16, 40),
    spine=dt.datetime(2026, 10, 16, 6, 31), archive=dt.datetime(2026, 10, 16, 6, 44),
    desks=dt.datetime(2026, 10, 16, 6, 46), cms=dt.datetime(2026, 10, 16, 7, 19),
    cmsnotes=dt.datetime(2026, 10, 16, 7, 52), exportlog=dt.datetime(2026, 10, 16, 7, 56),
    thread=dt.datetime(2026, 10, 16, 8, 41), policy=dt.datetime(2025, 1, 28, 11, 0, 37),
    bulletin=dt.datetime(2026, 4, 8, 11, 30), agreement=dt.datetime(2025, 6, 24, 15, 0, 12),
)
# Audience data's export log: the extract runs behind the files it produced (run id, source, run by, requested by,
# coverage). Workbooks and documents from other owners are not extract runs and carry their own provenance.
EXTRACT_RUNS = [
    ("newsletter", "EXT-26-1187", "Email platform", "Natalie Benjamin", "Kayla Torres",
     "Weeks starting 29 Jun to 21 Sep 2026"),
    ("panel", "EXT-26-1239", "Audience warehouse", "Kayla Torres", "Kayla Torres",
     "Periods Oct 2025 to Sep 2026, every release"),
    ("spine", "EXT-26-1244", "Audience warehouse", "Natalie Benjamin", "Corey Cox",
     "Pageviews 1 Oct 2025 to 30 Sep 2026 (AEST), all desks"),
    ("archive", "EXT-26-1245", "Audience warehouse", "Natalie Benjamin", "Corey Cox",
     "App engine from 2019; web CMS engine from 1 Oct 2025; concluded to 30 Sep 2026"),
    ("desks", "EXT-26-1246", "Audience warehouse", "Natalie Benjamin", "Corey Cox", "Current desks"),
    ("cms", "EXT-26-1248", "Web CMS (national and Brisbane instances)", "Natalie Benjamin", "Standards",
     "Documents first live 1 Oct 2025 to 30 Sep 2026, and never-live documents first saved then"),
]
# Each input workbook's Excel properties: (creator, last saved by, first created, AEST); the last save is STAMP's.
WORKBOOK_PROPS = dict(
    staff=("People and Culture", "People and Culture", dt.datetime(2026, 10, 12, 8, 30)),
    plan=("Kayla Torres", "Kayla Torres", dt.datetime(2026, 9, 18, 11, 20)),
    changelog=("Nina Franklin", "Nina Franklin", None),     # created the working day after embedding 1's sign-off
    panelwb=("Kayla Torres", "Kayla Torres", dt.datetime(2025, 11, 11, 10, 5)),
)
AUDIT_FLOOR = "2019-01-01"      # the squad's first year: the change log was started when embedding 1 closed


def utc(t):
    return (t - P.AEST).strftime("%Y-%m-%dT%H:%M:%SZ")


def epoch(t):
    return (t - P.AEST - dt.datetime(1970, 1, 1)).total_seconds()


def workbook_props(path, creator, last_by, created, modified):
    """Excel's own record in docProps/core.xml: who made the workbook, who saved it last, and when (UTC). Every
    other entry is carried over byte for byte, at the 1980-01-01 entry time Excel writes."""
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}
    core = data["docProps/core.xml"].decode("utf-8")
    core = re.sub(r"<dc:creator>[^<]*</dc:creator>", "<dc:creator>%s</dc:creator>" % creator, core)
    core = re.sub(r"<cp:lastModifiedBy>[^<]*</cp:lastModifiedBy>",
                  "<cp:lastModifiedBy>%s</cp:lastModifiedBy>" % last_by, core)
    core = re.sub(r"(<dcterms:created[^>]*>)[^<]*", lambda m: m.group(1) + utc(created), core)
    core = re.sub(r"(<dcterms:modified[^>]*>)[^<]*", lambda m: m.group(1) + utc(modified), core)
    data["docProps/core.xml"] = core.encode("utf-8")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = i.external_attr
            zi.create_system = i.create_system
            zout.writestr(zi, data[i.filename])
    Path(path).write_bytes(buf.getvalue())
    with zipfile.ZipFile(path) as z:
        for i in infos:
            if i.filename != "docProps/core.xml":
                assert z.getinfo(i.filename).CRC == i.CRC, i.filename


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def xlsx_book(path, title, when):
    wb = xlsxwriter.Workbook(str(path), {"strings_to_numbers": False})
    wb.set_properties({"title": title, "author": "Bightline News", "company": "Bightline News",
                       "created": when})
    return wb


# ---------------------------------------------------------------------------------- data files

def write_spine(W, path):
    ids, desks, dates, srcs, ages, pvs = [], [], [], [], [], []
    for d in P.DESK:
        A = W.art[d]
        for pv, aid, pub in ((A.pv, A.ids, A.pub), (A.old_pv, A.old_ids, A.old_pub)):
            if pv.size == 0:
                continue
            i, s, g = np.nonzero(pv)
            ids.append(aid[i])
            desks.append(np.full(len(i), d, dtype=object))
            day = np.array([(SP.T0 + dt.timedelta(minutes=int(m))).date() for m in pub])
            dates.append(day[i])
            srcs.append(s)
            ages.append(g)
            pvs.append(pv[i, s, g])
    ids = np.concatenate(ids)
    desks = np.concatenate(desks)
    dates = np.concatenate(dates)
    srcs = np.concatenate(srcs)
    ages = np.concatenate(ages)
    pvs = np.concatenate(pvs)
    order = np.lexsort((ages, srcs, ids))
    epoch = dt.date(1970, 1, 1)
    table = pa.table({
        "article_id": pa.array(ids[order], pa.int64()),
        "desk_code": pa.array(desks[order].tolist(), pa.string()),
        "published_date": pa.array(np.array([(x - epoch).days for x in dates[order]], np.int32), pa.date32()),
        "source_code": pa.array(np.array(P.SOURCES, dtype=object)[srcs[order]].tolist(), pa.string()),
        "age_band": pa.array(np.array(P.AGE_BANDS, dtype=object)[ages[order]].tolist(), pa.string()),
        "pageviews": pa.array(pvs[order], pa.int64()),
    }).replace_schema_metadata(None)
    pq.write_table(table, str(path), compression="snappy", use_dictionary=True, row_group_size=500_000,
                   write_statistics=True)
    return len(ids)


def write_archive(W, path):
    rows = []
    for t in W.tests:
        st = t["start"].strftime("%Y-%m-%dT%H:%M:00Z")
        en = t["end"].strftime("%Y-%m-%dT%H:%M:00Z")
        for k in range(len(t["ns"])):
            var = "control" if k == 0 else "BCDE"[k - 1]
            rows.append((t["test_id"], t["engine"], t["desk"], t["article_id"], t["owner"], st, en,
                         "%s-%s" % (t["test_id"], "A" if k == 0 else "BCDE"[k - 1]), var, int(t["ns"][k]),
                         int(t["cs"][k]), "Y" if t["ship"] == k else "N"))
    write_csv(path, ["test_id", "engine", "desk_code", "article_id", "owner_staff_id", "started_at", "concluded_at",
                     "package_id", "variant", "impressions", "clicks", "shipped"], rows)
    return len(rows)


def write_staff(W, path):
    wb = xlsx_book(path, "Newsroom staff list", dt.datetime(2026, 10, 12, 8, 30))
    ws = wb.add_worksheet("Staff")
    hd = wb.add_format({"bold": True, "bottom": 1})
    df = wb.add_format({"num_format": "yyyy-mm-dd"})
    cols = ["staff_id", "full_name", "team_code", "team", "role", "base", "start_date", "end_date"]
    for j, c in enumerate(cols):
        ws.write(0, j, c, hd)
    for i, r in enumerate(W.staff, start=1):
        for j, c in enumerate(cols[:6]):
            ws.write_string(i, j, r[c])
        ws.write_datetime(i, 6, dt.datetime.combine(r["start_date"], dt.time()), df)
        if r["end_date"] is not None:
            ws.write_datetime(i, 7, dt.datetime.combine(r["end_date"], dt.time()), df)
    ws.set_column(0, 0, 10)
    ws.set_column(1, 1, 22)
    ws.set_column(2, 2, 10)
    ws.set_column(3, 4, 24)
    ws.set_column(5, 7, 12)
    ws.freeze_panes(1, 0)
    ws2 = wb.add_worksheet("About")
    lines = ["Newsroom staff list, extracted from the HR system on 12 October 2026 for the audience team.",
             "Covers the newsroom teams: desks, the headline squad, audience, audience data, experimentation, "
             "standards and editorial leadership.",
             "Includes staff who have left since 1 January 2019; end_date is blank for current staff.",
             "team_code for desk staff is the desk code in the desk register."]
    for i, l in enumerate(lines):
        ws2.write_string(i, 0, l)
    ws2.set_column(0, 0, 110)
    wb.close()
    return len(W.staff)


def write_plan(W, path):
    wb = xlsx_book(path, "Audience plan 2027", dt.datetime(2026, 10, 9, 14, 5))
    ws = wb.add_worksheet("Plan 2027")
    hd = wb.add_format({"bold": True, "bottom": 1, "text_wrap": True})
    nf = wb.add_format({"num_format": "#,##0"})
    bold_nf = wb.add_format({"num_format": "#,##0", "bold": True, "top": 1})
    bold = wb.add_format({"bold": True, "top": 1})
    cols = ["desk_code", "desk", "edition", "clicks_oct25_sep26", "plan_2027_clicks"]
    for j, c in enumerate(cols):
        ws.write(0, j, c, hd)
    i = 1
    tot = 0
    for d in [x[0] for x in P.DESKS]:
        v = int(W.total[d])
        ws.write_string(i, 0, d)
        ws.write_string(i, 1, P.DESK[d][1])
        ws.write_string(i, 2, P.DESK[d][3])
        ws.write_number(i, 3, v, nf)
        ws.write_number(i, 4, v, nf)
        tot += v
        i += 1
    ws.write_string(i, 0, "Total", bold)
    ws.write_string(i, 1, "", bold)
    ws.write_string(i, 2, "", bold)
    ws.write_number(i, 3, tot, bold_nf)
    ws.write_number(i, 4, tot, bold_nf)
    ws.set_column(0, 0, 10)
    ws.set_column(1, 1, 20)
    ws.set_column(2, 2, 10)
    ws.set_column(3, 4, 18)
    ws.freeze_panes(1, 0)
    ws2 = wb.add_worksheet("Notes")
    lines = ["Audience plan 2027, version P2, 9 October 2026. Owner: Kayla Torres, Head of audience.",
             "Clicks are article pageviews from the audience warehouse, counted at the owning desk.",
             "2027 clicks are held at the twelve months to September 2026 for every desk, with no change assumed in "
             "where clicks come from.",
             "New initiatives for 2027, including the headline squad's embedding, are planned on top of these figures.",
             "Version P1 (18 September) used the twelve months to August and is superseded."]
    for i, l in enumerate(lines):
        ws2.write_string(i, 0, l)
    ws2.set_column(0, 0, 110)
    wb.close()


def changelog_saved(rows):
    """Experimentation saves the log on the working day after the latest embedding is signed off."""
    d = max(r["closed"] for r in rows) + dt.timedelta(days=1)
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return dt.datetime.combine(d, dt.time(10, 15))


def write_changelog(W, path, rows):
    wb = xlsx_book(path, "Headline squad change log", changelog_saved(rows))
    ws = wb.add_worksheet("Embeddings")
    hd = wb.add_format({"bold": True, "bottom": 1})
    df = wb.add_format({"num_format": "yyyy-mm-dd"})
    nf = wb.add_format({"num_format": "#,##0"})
    f1 = wb.add_format({"num_format": "0.0"})
    cols = ["embedding", "desk", "desk_code", "distribution", "started", "ended", "tests_run",
            "avg_winning_lift_pct", "planned_clicks_m", "realised_incremental_clicks", "closed_on"]
    for j, c in enumerate(cols):
        ws.write(0, j, c, hd)
    for i, r in enumerate(rows, start=1):
        ws.write_number(i, 0, r["no"])
        ws.write_string(i, 1, P.DESK[r["desk"]][1])
        ws.write_string(i, 2, r["desk"])
        ws.write_string(i, 3, "app only")
        ws.write_datetime(i, 4, dt.datetime.combine(r["started"], dt.time()), df)
        ws.write_datetime(i, 5, dt.datetime.combine(r["ended"], dt.time()), df)
        ws.write_number(i, 6, r["tests"])
        ws.write_number(i, 7, r["lift_pct"], f1)
        ws.write_number(i, 8, r["planned_m"], f1)
        ws.write_number(i, 9, r["realised"], nf)
        ws.write_datetime(i, 10, dt.datetime.combine(r["closed"], dt.time()), df)
    ws.set_column(0, 0, 10)
    ws.set_column(1, 3, 12)
    ws.set_column(4, 5, 11)
    ws.set_column(6, 9, 14)
    ws.set_column(10, 10, 11)
    ws.freeze_panes(1, 0)
    ws2 = wb.add_worksheet("Notes")
    lines = ["Kept by Experimentation (Nina Franklin). One row per closed embedding of the headline squad.",
             "realised_incremental_clicks: incremental article clicks at the embedded desk over the embedding year, "
             "measured against matched app desks (difference in differences), signed off on closed_on.",
             "planned_clicks_m: the desk's planned article clicks for the embedding year, in millions, from that "
             "year's audience plan.",
             "avg_winning_lift_pct and tests_run: the embedding's concluded tests in the headline test archive.",
             "The 2026 embedding with Puzzles closes in December 2026 and is added once its year is measured."]
    for i, l in enumerate(lines):
        ws2.write_string(i, 0, l)
    ws2.set_column(0, 0, 110)
    wb.close()


def write_desks(path):
    rows = [(d[0], d[1], d[2], d[3], d[4]) for d in P.DESKS]
    write_csv(path, ["desk_code", "desk_name", "vertical", "edition", "distribution"], rows)


def write_dashboard(path, dash):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["Headline testing: concluded tests by vertical"])
        w.writerow(["Window", "2025-10-01 to 2026-09-30 (trailing 12 months, AEST)"])
        w.writerow(["Refreshed", "2026-10-01 06:00 AEST"])
        w.writerow(["Owner", "Experimentation"])
        w.writerow(["Filters", "Test status is Concluded; concluded date in window"])
        w.writerow([])
        w.writerow(["vertical", "tests_concluded", "tests_with_variant_shipped", "avg_winning_lift_pct"])
        for v, n, s, lift in dash:
            w.writerow([v, n, s, "%.2f" % lift])


def write_cms(W, path):
    rows = asks.cms_rows(W.cms_docs)
    write_csv(path, ["doc_id", "desk_code", "doc_type", "parent_doc", "revision", "saved_at", "status", "publish_at",
                     "headline_sha1", "correction_note", "restored_from_doc", "migrated_from"], rows)
    return len(rows)


def write_panel(W, path):
    write_csv(path, ["release", "period", "site_code", "section_code", "unique_audience", "visits"], W.panel_rows)
    return len(W.panel_rows)


def write_panelwb(W, path):
    wb = xlsx_book(path, "Panel reference workbook", dt.datetime(2026, 10, 15, 16, 40))
    hd = wb.add_format({"bold": True, "bottom": 1})
    df = wb.add_format({"num_format": "yyyy-mm-dd"})
    ws = wb.add_worksheet("Sections (current)")
    for j, c in enumerate(["site_code", "site", "section_code", "section_name", "bightline_desk"]):
        ws.write(0, j, c, hd)
    for i, (site, code, name, desk) in enumerate(asks.SECTION_NEW, start=1):
        ws.write_string(i, 0, site)
        ws.write_string(i, 1, asks.SITES[site])
        ws.write_number(i, 2, code)
        ws.write_string(i, 3, name)
        ws.write_string(i, 4, desk)
    ws.set_column(0, 4, 18)
    ws = wb.add_worksheet("Section history")
    for j, c in enumerate(["site_code", "section_code", "section_name", "valid_from", "valid_to", "bightline_desk"]):
        ws.write(0, j, c, hd)
    i = 1
    for site, code, name, desk in asks.SECTION_OLD:
        ws.write_string(i, 0, site)
        ws.write_number(i, 1, code)
        ws.write_string(i, 2, name)
        ws.write_datetime(i, 3, dt.datetime(2024, 7, 1), df)
        ws.write_datetime(i, 4, dt.datetime(2026, 2, 28), df)
        ws.write_string(i, 5, desk)
        i += 1
    for site, code, name, desk in asks.SECTION_NEW:
        ws.write_string(i, 0, site)
        ws.write_number(i, 1, code)
        ws.write_string(i, 2, name)
        ws.write_datetime(i, 3, dt.datetime(2026, 3, 1), df)
        ws.write_string(i, 5, desk)
        i += 1
    ws.set_column(0, 5, 15)
    ws = wb.add_worksheet("Release log")
    for j, c in enumerate(["release", "published_on", "periods", "note"]):
        ws.write(0, j, c, hd)
    i = 1
    for rel in sorted(W.panel_rel_pub, key=lambda r: (W.panel_rel_pub[r], r)):
        pers = sorted(W.panel_rel_per[rel])
        note = ""
        if rel == "R26-04":
            note = "First release on the 2026 content taxonomy."
        if rel == asks.HISTORY_RELEASE:
            note = ("History release: November 2025 to February 2026 rerun on the 2026 content taxonomy. These "
                    "figures replace the earlier releases for those months.")
        if rel == "R26-07B":
            note = ("Restated April, May and June 2026 after a processing fault undercounted mobile audiences for "
                    "those months. These figures replace those published in R26-05, R26-06 and R26-07.")
        ws.write_string(i, 0, rel)
        ws.write_datetime(i, 1, dt.datetime.combine(W.panel_rel_pub[rel], dt.time()), df)
        ws.write_string(i, 2, ", ".join(pers))
        ws.write_string(i, 3, note)
        i += 1
    ws.set_column(0, 1, 12)
    ws.set_column(2, 2, 26)
    ws.set_column(3, 3, 100)
    ws = wb.add_worksheet("Definitions")
    defs = [("release", "Panel release the row was loaded from."),
            ("period", "Calendar month measured."),
            ("site_code", "BLN is bightline.com.au (national edition); BLB is the Brisbane edition site."),
            ("section_code", "Panel section code."),
            ("unique_audience", "Estimated number of different people aged 14 and over who visited the section at "
                                "least once in the month, on any device."),
            ("visits", "Estimated visits to the section in the month.")]
    for j, c in enumerate(["field", "definition"]):
        ws.write(0, j, c, hd)
    for i, (k, v) in enumerate(defs, start=1):
        ws.write_string(i, 0, k)
        ws.write_string(i, 1, v)
    ws.set_column(0, 0, 16)
    ws.set_column(1, 1, 100)
    wb.close()


def write_newsletter(W, path):
    rng = AR.rng_for(800)
    lists = [("Morning Briefing", 7, 412_000, 0.35, 0.22), ("Politics Weekly", 1, 96_500, 0.38, 0.18),
             ("Market Close", 5, 128_300, 0.40, 0.15), ("Sport Daily", 7, 151_800, 0.33, 0.12),
             ("Brisbane Today", 7, 87_400, 0.36, 0.20), ("Weekend Culture", 1, 64_900, 0.42, 0.25)]
    rows = []
    for w in range(13):
        wk = dt.date(2026, 6, 29) + dt.timedelta(days=7 * w)
        for name, sends, size, open_rate, cto in lists:
            listsize = int(size * (1 + 0.002 * w + rng.normal(0, 0.003)))
            delivered = int(listsize * sends * rng.uniform(0.982, 0.991))
            opens = int(delivered * open_rate * rng.uniform(0.93, 1.07))
            proxy = int(opens * rng.uniform(0.42, 0.55))
            clicks = int(opens * cto * rng.uniform(0.9, 1.1))
            unsub = int(delivered * rng.uniform(0.0004, 0.0011))
            rows.append((wk.isoformat(), name, sends, listsize, delivered, opens, proxy, clicks, unsub))
    write_csv(path, ["week_starting", "newsletter", "sends", "list_size", "delivered", "opens", "opens_privacy_proxy",
                     "clicks", "unsubscribes"], rows)


def write_exportlog(path, counts):
    rows = []
    for key, run, source, by, asked, coverage in EXTRACT_RUNS:
        n = {"newsletter": 78, "desks": len(P.DESKS)}.get(key, counts.get(key))
        rows.append((run, STAMP[key].strftime("%Y-%m-%d %H:%M"), F[key], source, by, asked, coverage, n))
    write_csv(path, ["run_id", "run_at_aest", "file", "source_system", "run_by", "requested_by", "coverage", "rows"],
              rows)


# ---------------------------------------------------------------------------------- derived numbers for the files

def dashboard_rows(W):
    lo = dt.datetime(2025, 10, 1) - P.AEST
    hi = dt.datetime(2026, 10, 1) - P.AEST
    out = []
    for v in ["Politics", "Business", "Sport", "Local", "Culture", "Puzzles & Games", "Food & Wellbeing"]:
        ts = [t for t in W.tests if P.DESK[t["desk"]][2] == v and lo <= t["end"] < hi]
        if not ts:
            continue
        lift = 100 * AR.desk_lift(ts, shrink=False)
        out.append((v, len(ts), sum(1 for t in ts if t["ship"] > 0), round(lift, 2)))
    return out


def changelog_rows(W):
    eps = AR.rng_for(777).uniform(-P.REALISED_NOISE, P.REALISED_NOISE, size=len(P.EMBEDDINGS))
    rows = []
    for k, e in enumerate(P.EMBEDDINGS):
        ts = W.emb_tests[e["no"]]
        s = AR.desk_lift(ts, W.prior)
        raw = AR.desk_lift(ts, shrink=False)
        y = e["year"]
        start = dt.date(y, 1, 4)
        while start.weekday() != 0:
            start += dt.timedelta(days=1)
        end = dt.date(y, 12, 18)
        while end.weekday() != 4:
            end -= dt.timedelta(days=1)
        closed = dt.date(y + 1, 2, 2) + dt.timedelta(days=int(AR.rng_for(778, y).integers(0, 14)))
        rows.append(dict(no=e["no"], desk=e["desk"], started=start, ended=end, tests=len(ts),
                         lift_pct=round(100 * raw, 1), planned_m=e["planned_m"],
                         realised=int(round(s * e["planned_m"] * 1e6 * (1 + eps[k]))), closed=closed,
                         eps=float(eps[k])))
    return rows


def bulletin_counts(W):
    """March 2026 (AEST) headline and text corrections across the web desks, by the standards rule."""
    lo = dt.datetime(2026, 3, 1) - P.AEST
    hi = dt.datetime(2026, 4, 1) - P.AEST
    arts = asks.read_corrections(asks.cms_rows(W.cms_docs))
    h = sum(lo <= t < hi for a in arts.values() for t in a["heads"])
    b = sum(lo <= t < hi for a in arts.values() for t in a["texts"])
    return h, b


# ---------------------------------------------------------------------------------- normalisation

def normalise(target, stamps):
    # producer metadata: every writer is given its in-fiction application at write time, so the audit has nothing
    # to repair; it runs as a check, and a flagged file stops the build rather than being patched here
    r = subprocess.run([sys.executable, str(SCRUB), str(target), "--floor", AUDIT_FLOOR, "--ceiling",
                        P.AS_OF.isoformat()], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("producer audit flags files:\n" + r.stdout + r.stderr)
    # each file carries the time it was written: an extract its run, a workbook its last save, a document its date
    for key, name in F.items():
        ts = epoch(stamps[key])
        os.utime(Path(target) / name, (ts, ts))
    return r.stdout.strip()


# ---------------------------------------------------------------------------------- main

def build(out):
    out = Path(out)
    target = out / "target"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    W = world.build()
    asks.build_cms(W)
    asks.build_panel(W)
    counts = {}
    counts["spine"] = write_spine(W, target / F["spine"])
    counts["archive"] = write_archive(W, target / F["archive"])
    counts["staff"] = write_staff(W, target / F["staff"])
    write_plan(W, target / F["plan"])
    W.changelog = changelog_rows(W)
    write_changelog(W, target / F["changelog"], W.changelog)
    W.stamp = dict(STAMP, changelog=changelog_saved(W.changelog))
    first = min(W.changelog, key=lambda r: r["no"])["closed"] + dt.timedelta(days=1)
    while first.weekday() >= 5:
        first += dt.timedelta(days=1)
    W.wb_created = {k: (v[2] if v[2] else dt.datetime.combine(first, dt.time(9, 40))) for k, v in WORKBOOK_PROPS.items()}
    (target / F["fieldref"]).write_text(docs.field_reference_md(), encoding="utf-8")
    docs.write_pdf(target / F["charter"], "Headline squad: 2027 placement brief", docs.charter_blocks(),
                   "Bightline News | Internal. Not for circulation outside the newsroom.", STAMP["charter"],
                   author="Corey Cox", app="word2010")
    write_desks(target / F["desks"])
    W.dashboard = dashboard_rows(W)
    write_dashboard(target / F["dashboard"], W.dashboard)
    counts["cms"] = write_cms(W, target / F["cms"])
    (target / F["cmsnotes"]).write_text(docs.cms_fields_txt(), encoding="utf-8")
    docs.write_pdf(target / F["policy"], "Editorial standards: corrections", docs.policy_blocks(),
                   "Bightline News editorial standards | Section 7", STAMP["policy"],
                   author="Bightline News Standards", app="word2010")
    counts["panel"] = write_panel(W, target / F["panel"])
    write_panelwb(W, target / F["panelwb"])
    for key, (creator, last_by, _) in WORKBOOK_PROPS.items():
        workbook_props(target / F[key], creator, last_by, W.wb_created[key], W.stamp[key])
    W.bulletin = bulletin_counts(W)
    docs.write_docx(target / F["bulletin"], docs.bulletin_paras(*W.bulletin), STAMP["bulletin"] - dt.timedelta(hours=2),
                    author="Standards desk", title="Standards bulletin, April 2026")
    (target / F["thread"]).write_text(docs.thread_eml(), encoding="utf-8")
    docs.write_pdf(target / F["agreement"], "Content syndication agreement", docs.agreement_blocks(),
                   "Bightline News Pty Ltd and Newsfold Pty Ltd | Commercial in confidence",
                   STAMP["agreement"], author="Bightline News Commercial", app="pdfmaker")
    write_newsletter(W, target / F["newsletter"])
    write_exportlog(target / F["exportlog"], counts)
    W.scrub_audit = normalise(target, W.stamp)
    write_metadata(out, target, counts, W.stamp)
    return W, target


def write_metadata(out, target, counts, stamps):
    fmt = {}
    files = []
    for key, name in F.items():
        p = target / name
        ext = p.suffix.lstrip(".")
        fmt[ext] = fmt.get(ext, 0) + 1
        files.append({"path": name, "format": ext, "bytes": p.stat().st_size,
                      "rows": counts.get(key, None),
                      "source": "Constructed for this task: fictional publisher Bightline News; no third-party data",
                      "date": stamps[key].date().isoformat(), "license": "CC0-1.0 (original work)"})
    meta = {
        "task": "task118",
        "domain": "Marketing & Consumer Research",
        "subdomain": "media-audience-measurement",
        "objective": "Opportunity Sizing & Decision Support",
        "as_of": P.AS_OF.isoformat(),
        "deliverables": ["squad_placement_2027.docx", "squad_placement_2027.xlsx"],
        "distractor_files": [F[k] for k in DISTRACTORS],
        "input_gates": {"files": len(F), "formats": sorted(fmt), "largest_file_rows": max(v for v in counts.values()),
                        "largest_file": F["spine"]},
        "files": files,
    }
    (Path(out) / "metadata.json").write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(TASK))
    ap.add_argument("--no-checks", action="store_true")
    a = ap.parse_args()
    W, target = build(a.out)
    if a.no_checks:
        print("built", target)
        return 0
    import checks
    return checks.run(W, target, Path(a.out))


if __name__ == "__main__":
    sys.exit(main())
