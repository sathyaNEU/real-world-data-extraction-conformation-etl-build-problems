"""The pack's data files, each as its source system exports it: the RUM warehouse's beacon extract and sampling
configuration, the squad's review extract, change log and AVIF size table, the CDN host list, the image hosts' and
the old media server's request rollups, the DAM's hero-collection export, the public CrUX rows, the analytics suite's
page views, and the extract log."""
from __future__ import annotations

import csv
import datetime as dt

import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import common as K
import world as W

INT_COLS = ("lcp_ms", "ttfb_ms", "load_delay_ms", "load_time_ms", "render_delay_ms")


def _utc(t) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def _write(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def _beacon_rows(df, cols):
    out = []
    for rec in df[[c if c != "form_factor" else "device" for c in cols]].itertuples(index=False, name=None):
        row = []
        for c, v in zip(cols, rec):
            if c == "fired_at_utc":
                row.append(_utc(v))
            elif c in INT_COLS:
                row.append("" if v is None or v is pd.NA or (isinstance(v, float) and v != v) else int(v))
            else:
                row.append(v)
        out.append(row)
    return out


BEACON_COLS = ["beacon_id", "origin", "page_path", "form_factor", "navigation_type", "fired_at_utc", "lcp_ms",
               "lcp_element", "lcp_url", "ttfb_ms", "load_delay_ms", "load_time_ms", "render_delay_ms"]


def write_beacons(path, nov):
    return _write(path, BEACON_COLS, _beacon_rows(nov, BEACON_COLS))


def write_engagement_beacons(path, eng):
    cols = ["beacon_id", "engagement", "origin", "page_path", "form_factor", "navigation_type", "fired_at_utc", "lcp_ms",
            "lcp_element", "lcp_url", "ttfb_ms", "load_delay_ms", "load_time_ms", "render_delay_ms"]
    e = eng.copy()
    e["beacon_id"] = [W._hexid("review", i) for i in range(len(e))]
    return _write(path, cols, _beacon_rows(e, cols))


# the sampling configuration's history; the rates in force from 1 June 2026 are common.SAMPLING
SAMPLING_HISTORY = [
    ("2024-02-12T00:00:00Z", {"tideline": 0.0010, "matchday": 0.0010, "hearth": 0.0010, "ledger": 0.0010,
                              "trailhead": 0.0010, "pantry": 0.0010}, "WEBPLAT-1182", "drhodes",
     "collector go-live"),
    ("2025-04-07T01:00:00Z", {"tideline": 0.0004, "matchday": 0.0007, "pantry": 0.0015, "trailhead": 0.0015},
     "WEBPLAT-1571", "drhodes", "per-origin rates"),
    ("2025-10-06T01:00:00Z", {"matchday": 0.0009, "hearth": 0.0011}, "WEBPLAT-1877", "drhodes", "quota review"),
    ("2026-06-01T00:00:00Z", {"tideline": 0.0005, "matchday": 0.0008, "hearth": 0.0010, "ledger": 0.0010,
                              "trailhead": 0.0012, "pantry": 0.0010}, "WEBPLAT-2240", "drhodes",
     "quota review"),
]
SAMPLING_CHANGES = {
    "tideline": ("WEBPLAT-2391", "drhodes", "collector capacity added"),
    "ledger": ("WEBPLAT-2418", "drhodes", "over beacon quota"),
}


def write_sampling(path):
    rows = []
    for since, rates, ref, by, note in SAMPLING_HISTORY:
        for p in K.PROPERTIES:
            if p["code"] in rates:
                rows.append([p["origin"], "%.4f" % rates[p["code"]], since, ref, by, note])
    for p in K.PROPERTIES:
        for since, rate in K.SAMPLING[p["code"]][1:]:
            ref, by, note = SAMPLING_CHANGES[p["code"]]
            rows.append([p["origin"], "%.4f" % rate, _utc(since), ref, by, note])
    # the configuration in force from 1 June 2026 is the history's last block; assert it matches the world
    june = SAMPLING_HISTORY[-1][1]
    for p in K.PROPERTIES:
        assert abs(june[p["code"]] - K.SAMPLING[p["code"]][0][1]) < 1e-12
    rows.sort(key=lambda r: (r[2], r[0]))
    return _write(path, ["origin", "sample_rate", "effective_from_utc", "change_ref", "changed_by", "note"], rows)


SMALL_SITES = [("Clutch", "clutch.brolga.au", "2019-03-11"), ("Tenancy", "tenancy.brolga.au", "2020-08-03"),
               ("Fairway", "fairway.brolga.au", "2018-05-21"), ("Undercurrent", "undercurrent.brolga.au", "2021-02-15"),
               ("Brolga Kids", "kids.brolga.au", "2019-09-30"), ("Tidewater", "tidewater.brolga.au", "2022-04-04"),
               ("Paddock", "paddock.brolga.au", "2020-11-23")]
SINCE = {"tideline": "2016-03-01", "matchday": "2017-02-13", "hearth": "2015-09-01", "ledger": "2018-08-20",
         "trailhead": "2014-11-10", "pantry": "2019-10-07"}


def write_cdn_hosts(path):
    hdr = ["host", "path_prefix", "kind", "property", "status", "since", "retired_for_new_links", "owner", "note"]
    rows = []
    for p in K.PROPERTIES:
        rows.append([p["origin"], "/", "page origin", p["name"], "live", SINCE[p["code"]], "", "web platform", ""])
        img_since = W.ALIAS_BEFORE[p["code"]].isoformat() if p["code"] in W.ALIAS_BEFORE else SINCE[p["code"]]
        rows.append([p["img"], "/", "image host", p["name"], "live", img_since, "", "web platform", ""])
        if p["alias"]:
            rows.append([p["alias"][0], "/", "legacy image alias", p["name"], "answering", SINCE[p["code"]],
                         p["alias"][1].isoformat(), "web platform",
                         "old media server; answers links to images uploaded before the image host"])
        rows.append([K.CDN_HOST, "/%s/" % p["code"], "image CDN path", p["name"], "live", "2025-06-16", "",
                     "web platform", ""])
    for name, origin, since in SMALL_SITES:
        code = origin.split(".")[0]
        rows.append([origin, "/", "page origin", name, "live", since, "", "web platform", ""])
        rows.append(["images." + origin, "/", "image host", name, "live", since, "", "web platform", ""])
        rows.append([K.CDN_HOST, "/%s/" % code, "image CDN path", name, "live", "2024-02-05", "", "web platform", ""])
    rows.append([K.AGENCY_HOSTS[0], "/", "third party", "", "live", "", "", "Pressframe Syndication",
                 "agency photos, licensed per use"])
    rows.append([K.AGENCY_HOSTS[1], "/", "third party", "", "live", "", "", "Wirelens", "agency photos"])
    rows.append([K.AD_HOSTS[0], "/", "third party", "", "live", "", "", "ad exchange", "ad creatives"])
    rows.append([K.VIDEO_HOST, "/", "third party", "", "live", "", "", "video platform", "video posters"])
    return _write(path, hdr, rows)


def write_crux(path, frame):
    rows = [list(r) for r in frame.itertuples(index=False, name=None)]
    rows = [[a, b, c, "%.4f" % d, "%.4f" % e, "%.4f" % f, g] for a, b, c, d, e, f, g in rows]
    return _write(path, list(frame.columns), rows)


def write_analytics(path, frame):
    return _write(path, list(frame.columns), [list(r) for r in frame.itertuples(index=False, name=None)])


def write_image_logs(path, frame):
    rows = [[t.strftime("%Y-%m-%d %H:00"), h, pp, s, n] for t, h, pp, s, n in frame.itertuples(index=False, name=None)]
    return _write(path, ["hour_utc", "host", "path_prefix", "status", "requests"], rows)


def write_legacy_log(path, frame):
    rows = [[t.strftime("%d/%b/%Y:%H +1100"), h, u, c, n] for t, h, u, c, n in frame.itertuples(index=False, name=None)]
    return _write(path, ["log_hour", "vhost", "uri_dir", "code", "hits"], rows)


def write_dam(path, frame):
    rows = [[a, b, c, d, e, f, g, _utc(h), i.isoformat(), j]
            for a, b, c, d, e, f, g, h, i, j in frame.itertuples(index=False, name=None)]
    return _write(path, list(frame.columns), rows)


def _sheet(ws, widths, freeze=None):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    if freeze:
        ws.freeze_panes = freeze


def write_change_log(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Engagements"
    bold = Font(bold=True)
    ws.append(["Performance squad change log, 2024 to 2026"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Every engagement the squad has shipped with the hero-image playbook. Review windows as on the "
               "Review windows sheet."])
    ws.append([])
    hdr = ["Ref", "Site", "Origin", "Pages", "Before from", "Before to", "Shipped", "After from", "After to",
           "Changes", "Notes"]
    ws.append(hdr)
    for c in ws[4]:
        c.font = bold
    pages = {"Clutch": "article template", "Tenancy": "listing and article templates",
             "Fairway": "article template", "Undercurrent": "article template", "Brolga Kids": "article template",
             "Tidewater": "article template", "Paddock": "article and gallery templates"}
    notes = {"E01": "shipped with theme release 3.8", "E02": "", "E03": "", "E04": "shipped with theme release 4.1",
             "E05": "gallery template, the second Clutch engagement", "E06": "", "E07": "",
             "E08": "listing template added after E02", "E09": "", "E10": "the second Fairway engagement",
             "E11": "the second Undercurrent engagement"}
    tickets = {"E01": "SQD-104", "E02": "SQD-131", "E03": "SQD-158", "E04": "SQD-173", "E05": "SQD-197",
               "E06": "SQD-226", "E07": "SQD-251", "E08": "SQD-279", "E09": "SQD-306", "E10": "SQD-334",
               "E11": "SQD-361"}
    for e, (_, b0, b1, ship, a0, a1) in zip(K.ENGAGEMENTS, W.engagement_windows()):
        ws.append([e[0], e[1], e[2], pages[e[1]], b0, b1, ship, a0, a1, "steps 1 to 4, %s" % tickets[e[0]],
                   notes[e[0]] or None])
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        for c in row[4:9]:
            c.number_format = "d mmm yyyy"
    _sheet(ws, [6, 13, 23, 28, 12, 12, 12, 12, 12, 20, 40], "A5")
    pb = wb.create_sheet("Playbook")
    pb.append(["Hero-image playbook (version 3, since 5 February 2024)"])
    pb["A1"].font = Font(bold=True, size=12)
    pb.append([])
    pb.append(["Step", "What the squad changes"])
    for c in pb[3]:
        c.font = bold
    steps = ["Serve the hero image from the group image CDN, img.brolgacdn.au, under the site's path",
             "Encode the hero image as AVIF at the hero slot's size (squad_avif_size_table.xlsx)",
             "Preload the hero image from the document head with fetchpriority=\"high\"",
             "Never lazy-load the hero image (no loading=\"lazy\" on it)"]
    for i, s in enumerate(steps, 1):
        pb.append([i, s])
    pb.append([])
    pb.append(["Scope", "The hero image of each page in the engaged templates."])
    pb.append(["Not in scope", "Time to first byte (origin, HTML caching), scripts, fonts, ad slots, third-party "
                               "images, the render path."])
    _sheet(pb, [12, 96])
    rw = wb.create_sheet("Review windows")
    rw.append(["How the squad reviews an engagement"])
    rw["A1"].font = Font(bold=True, size=12)
    rw.append([])
    for line in ["Before window: the 28 days to the day before the change ships.",
                 "After window: the 28 days starting 7 days after the change ships (the first week lets browser "
                 "caches and the CDN fill).",
                 "Both windows are read on the group RUM, Sydney dates, the engaged pages' loads whose LCP element "
                 "is the hero image (squad_engagement_beacons_2024-2026.csv)."]:
        rw.append([line])
        rw.cell(rw.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    _sheet(rw, [110])
    wb.save(path)
    return len(K.ENGAGEMENTS)


def write_avif_table(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "AVIF sizes"
    ws.append(["Performance squad: AVIF sizes by slot"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["libavif 1.1, quality 60, speed 6, encoded from the DAM originals at each slot's size; mean over a "
               "random sample of each property's images used in the slot. Updated 18 November 2026."])
    ws.append([])
    ws.append(["Property", "Slot", "Width (px)", "Height (px)", "Mean AVIF size (bytes)", "Images sampled"])
    for c in ws[4]:
        c.font = Font(bold=True)
    r = K.stream("avif_sample")
    n = 0
    for p in K.PROPERTIES:
        for slot in ("hero", "inline", "thumbnail"):
            w, h = K.SLOT_SIZES[p["code"]][slot]
            ws.append([p["name"], slot, w, h, K.AVIF_BYTES[p["code"]][slot], int(r.integers(380, 520))])
            n += 1
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[4].number_format = "#,##0"
    _sheet(ws, [12, 11, 11, 11, 22, 15], "A5")
    wb.save(path)
    return n


def write_extract_log(path, counts, names):
    """counts: file -> data rows."""
    E = K.EXTRACT_DATE.isoformat()
    rows = [
        [names["beacons"], "RUM warehouse", E + "T01:12:40Z", "UTC days 2026-10-31 to 2026-11-30", "UTC",
         counts[names["beacons"]], "drhodes", "every beacon received for the six www origins"],
        [names["sampling"], "RUM collector config", E + "T01:14:05Z", "full history", "UTC",
         counts[names["sampling"]], "drhodes", "effective-dated"],
        [names["eng"], "RUM warehouse (squad review extract)", E + "T01:31:22Z", "each engagement's review windows",
         "UTC", counts[names["eng"]], "tmurillo", "about 3,000 beacons sampled at random from each window"],
        [names["img"], "image host log rollup", E + "T02:02:51Z", "UTC days 2026-10-31 to 2026-11-30", "UTC",
         counts[names["img"]], "drhodes", "the group's image hosts and the image CDN, hourly; status 200 sends the "
         "image, 304 tells the browser its cached copy is current and sends none"],
        [names["legacy"], "old media server", E + "T02:05:17Z", "local days 2026-11-01 to 2026-11-30",
         "Sydney (+1100)", counts[names["legacy"]], "drhodes", "the server's own hourly rollup; codes as in the "
         "image host logs"],
        [names["dam"], "DAM", E + "T02:10:44Z", "hero collections, all assets", "UTC", counts[names["dam"]],
         "tmurillo", "one row per rendition; property is the hero collection the asset was uploaded to; "
         "last_used_on and last_used_page come from the nightly crawl of live pages, the latest on 2026-12-02"],
        [names["crux"], "Chrome UX Report (public)", E + "T02:20:09Z", "2026-11", "", counts[names["crux"]],
         "tmurillo", "origin-level, all of Chrome"],
        [names["analytics"], "analytics suite", E + "T02:24:36Z", "Sydney dates 2026-11-01 to 2026-11-30",
         "Sydney", counts[names["analytics"]], "mgood", "page views by section"],
        [names["hosts"], "CDN host list", E + "T02:26:58Z", "current", "", counts[names["hosts"]], "drhodes", ""],
    ]
    return _write(path, ["file", "source", "extracted_utc", "covers", "clock", "rows", "extracted_by", "note"], rows)
