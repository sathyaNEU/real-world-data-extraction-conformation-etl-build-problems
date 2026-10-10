"""task129 generator: the filed documents, the social layer, the distractors and the manifest."""
import os
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

import params as P
from golden import F


def _pdf(path, title, author, blocks):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=9.5,
                          leading=13)
    h = ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=11,
                       spaceBefore=8, spaceAfter=3)
    t = ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=14,
                       alignment=0, spaceAfter=4)
    small = ParagraphStyle("s", parent=body, fontSize=8, textColor=colors.HexColor("#555555"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm,
                            topMargin=20 * mm, bottomMargin=18 * mm, title=title, author=author,
                            invariant=1)
    flow = []
    for kind, val in blocks:
        if kind == "title":
            flow.append(Paragraph(val, t))
        elif kind == "h":
            flow.append(Paragraph(val, h))
        elif kind == "p":
            flow.append(Paragraph(val, body))
        elif kind == "small":
            flow.append(Paragraph(val, small))
        elif kind == "sp":
            flow.append(Spacer(1, val))
        elif kind == "table":
            tb = Table(val, hAlign="LEFT")
            tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
                                    ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                                    ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            flow.append(tb)
    doc.build(flow)


def service_level(path):
    _pdf(path, "Page delivery service level v3", "Elin Lauritsen", [
        ("title", "Page delivery service level, version 3"),
        ("small", "Sønderå Medier, Digital operations. In force from 1 January 2026. Owner: Elin "
                  "Lauritsen, head of digital operations. Agreed at the quarterly service review of "
                  "9 December 2025."),
        ("h", "1. Scope"),
        ("p", "This service level covers delivery of pages to readers of Sønderå Tidende, Lindå Avis "
              "and Kærby Dagblad on mobile phones. A mobile view is a page view on a device whose "
              "model the device registry lists with form factor phone. Tablets and desktop "
              "browsers are reported separately and are not part of this service level."),
        ("h", "2. The line"),
        ("p", "A page view misses the line when its largest contentful paint exceeds 4.0 seconds. A "
              "view with no paint timing (a page restored from the back-forward cache) is not "
              "scored. The service level is the share of scored mobile views that miss the line, "
              "reported monthly by title in the digital operations close-out."),
        ("h", "3. Reading a change"),
        ("p", "The effect of a change on the share is read on the 28 days either side of the "
              "release that switched it on."),
        ("h", "4. Valuing a fix"),
        ("p", "A fix is valued on the mobile views it brings back under the line at the latest full "
              "month's traffic. The operations squad works on one fix a quarter; the quarterly "
              "service review allocates it."),
        ("h", "5. Who reviews what"),
        ("p", "The quarterly service review is chaired by the head of digital operations, with the "
              "three editors-in-chief, ad sales and the group digital director. The ad-revenue "
              "committee reviews performance work on page weight from the monthly synthetic crawl; "
              "Gunnar Paulsen, head of ad operations, works from that basis and will present it at "
              "the review."),
        ("h", "6. Data"),
        ("p", "Field data is the RUM beacon export described in the field guide. The synthetic crawl "
              "is a lab measurement of the anonymous page on an emulated phone; its run "
              "configuration is filed with the crawl log."),
        ("sp", 10),
        ("small", "Internal. Not for distribution outside Sønderå Medier. Next revision due December "
                  "2026."),
    ])


def paywall(path):
    _pdf(path, "Subscriber terms, digital layout", "Sønderå Medier Abonnement", [
        ("title", "Subscriber terms: digital layout and access (extract)"),
        ("small", "Sønderå Medier A/S, Abonnementsservice. Version 2026-01, applies to Digital, "
                  "Digital+ and Weekend + digital."),
        ("h", "4. Layout"),
        ("p", "4.1 Digital access covers every article, front page, gallery, live blog and puzzle on "
              "the title or titles the product includes."),
        ("p", "4.2 Signed-in subscribers are served the ad-free layout on every template."),
        ("p", "4.3 Readers who are not signed in to an active subscription, including readers with a "
              "free account, are served the ad-supported layout. Article access for them is metered "
              "at five articles a month."),
        ("h", "5. Term and cancellation"),
        ("p", "5.1 A subscription runs from its start date until it is cancelled. Cancellation takes "
              "effect at the end of the paid period, which the subscription register records as the "
              "end date."),
        ("p", "5.2 Prices are set out in the price list in force; changes are announced 30 days ahead."),
        ("h", "6. Devices"),
        ("p", "6.1 A subscription may be used on up to five devices at a time, in the apps or in the "
              "browser."),
        ("sp", 8),
        ("small", "Sønderå Medier A/S, CVR on request. Kundeservice hverdage 7-17."),
    ])


def vendor_appendix(path):
    rows = [["Field", "Meaning"],
            ["log_date", "UTC calendar day of the requests"],
            ["pop", "Edge location (IATA code of the city)"],
            ["vendor", "primary, or fallback (the secondary vendor engaged from 9 June to 21 July)"],
            ["device_class", "Vendor's classification of the client from its user agent"],
            ["ua_family", "Client browser or agent family"],
            ["edge_hits", "Requests answered from the edge cache"],
            ["origin_fills", "Requests that missed the edge and were answered from origin. A request\n"
                             "is counted in edge_hits or in origin_fills, never in both."],
            ["bytes_served", "Bytes delivered to clients for both kinds of request. The fallback\n"
                             "vendor reports this field in kilobytes (1,000 bytes), as its contract sets."]]
    _pdf(path, "Image CDN: delivery log appendix", "Digital operations", [
        ("title", "Image delivery: daily log, appendix C"),
        ("small", "Sønderå Medier, Digital operations. Covers the image hosts img. and pix. "
                  "sonderaa-medier.dk. One row per day, edge location, vendor, device class and agent "
                  "family."),
        ("sp", 6),
        ("table", rows),
        ("sp", 8),
        ("p", "From 9 June to 21 July the primary vendor's Copenhagen capacity was reduced and part of "
              "the traffic was routed to the fallback vendor. Both vendors' rows are in the log for "
              "those days."),
        ("sp", 6),
        ("small", "Internal. Vendor contract references on file with digital operations."),
    ])


GUIDE = """# RUM beacon export: field guide

Digital operations, maintained by Gunhild Lund. Applies to `rum_mobile_views_2026.parquet` and the
registers and logs filed beside it. Last edited 4 September 2026.

## The beacon export

One row per beacon the collector received. A page view sends one beacon; `pv_id` is the page-view
key. The export holds mobile web and app-webview page views on the three titles' sites from
1 February to 31 August 2026 (Copenhagen dates). Reporting months are Copenhagen calendar months.

Sampling is by device key: when a device is sampled, every page view it makes is in the export.
`sample_weight` is the number of page views the row stands for; sum it to count views.

| Field | Meaning |
|---|---|
| beacon_id | Collector receipt number, increasing in order of receipt |
| pv_id | Page-view key |
| ts_utc | Navigation start of the page view, UTC |
| device_key | Hashed device identifier, stable for the life of the device |
| account_key | Account the device is signed in to; empty when not signed in |
| title | Masthead the page was published under at the time of the view (ST Sønderå Tidende, LA Lindå Avis, KD Kærby Dagblad) |
| template | Page template |
| url_path | Path of the page on the title's site; local-edition pages sit under /lokal/<edition>/ |
| device_model | Model string as the client reports it; resolve it against the device registry |
| os, browser | Client operating system and browser (app webviews report the app) |
| effective_connection_type | Network Information API value at navigation start |
| navigation_type | navigate, reload or back_forward |
| referrer_class | internal, search, social, direct, newsletter, push, app or other |
| ttfb_ms | Time to first byte, milliseconds |
| lcp_ms | Largest contentful paint, milliseconds; empty when the browser reported no paint |
| cls | Cumulative layout shift |
| sample_weight | Page views the row stands for |

Collector v2 came with the platform release of 3 June 2026 (see the release train log); sampling
rates are set per collector and are carried row by row in `sample_weight`.

## Registers and logs

- `device_registry_2026-09.csv`: one row per device model. `form_factor` is phone or tablet;
  `perf_band` (low, mid, high) is the model's band on the group's CPU benchmark and is the phone
  class used in performance reporting.
- `subscription_register_extract_2026-09-05.csv`: one row per subscription. A subscription is
  active from `start_date` to `end_date` inclusive; an empty `end_date` means it is running.
- `edition_register.csv`: masthead of each local edition, effective-dated; an empty `valid_to`
  is the current row.
- `release_train_log_2026.csv`: one row per platform deploy. `deployed_at` is local time with its
  offset. `platform_bundle` and `puzzles_bundle` are the content hashes of the JavaScript bundles
  the deploy shipped.
- `boelge_rollout_log.csv`: one row per Bølge wave, with the release that switched it on.
- `synthetic_crawl_requests_2026.csv`: one row per request the crawler made. `run_id` is one
  page load; `masthead` is the title whose list carries the URL.
- `web_asset_register.csv`: a request belongs to the change the register names for its host and
  longest matching path prefix; a request matching no row is platform baseline.
- `image_cdn_delivery_2026.csv`: fields in the vendor appendix (appendix C).

Throughout these extracts a kilobyte (kB) is 1,000 bytes.
"""


def field_guide(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(GUIDE)


THREAD = """From: Elin Lauritsen <elin.lauritsen@sonderaa-medier.dk>
To: digital-ops-review@sonderaa-medier.dk
Date: Wed, 2 Sep 2026 08:14:52 +0200
Subject: Q4 squad: prep for the service review on the 17th

Hi all,

The share over the line has gone up on all three titles since spring and the review on the 17th
gives the squad its Q4. One fix, so we need to pick the right one. August extract lands on Friday.
I'll make the call; tell me now if there is something I should look at.

Elin

----
From: Ove Schmidt <ove.schmidt@sonderaa-medier.dk>
Date: Wed, 2 Sep 2026 08:40:17 +0200

It's the consent banner. The numbers turned the week it went in and nothing else that size
shipped then. I'd like the squad on it.

----
From: Caroline Mortensen <caroline.mortensen@sonderaa-medier.dk>
Date: Wed, 2 Sep 2026 09:05:03 +0200

The crawl gets heavier every month and most of it is pictures. The renditions from the new image
pipeline are big. I'd rather the squad looked there than at anything the desks touch.

----
From: Finn Thygesen <finn.thygesen@sonderaa-medier.dk>
Date: Wed, 2 Sep 2026 09:31:44 +0200

For the record, Bølge has been on subscriber pages since each wave went out and those pages hardly
moved. Whatever this is, I don't think it's the front end.

----
From: Gunnar Paulsen <gunnar.paulsen@sonderaa-medier.dk>
Date: Wed, 2 Sep 2026 10:12:09 +0200

The ad-revenue committee looks at performance work on page weight from the crawl, as it always
has. That's what I'll bring to the review.

----
From: Gunhild Lund <gunhild.lund@sonderaa-medier.dk>
Date: Wed, 2 Sep 2026 10:30:55 +0200

Export for February to August goes out on the 5th with the registers. Same format as the July cut.
Field guide is updated.

----
From: Elin Lauritsen <elin.lauritsen@sonderaa-medier.dk>
Date: Wed, 2 Sep 2026 11:02:31 +0200

Thanks. Noted, all of it.

--
Sønderå Medier, Digital operations. Internal: do not forward.
"""


def thread(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(THREAD)


# ------------------------------------------------------------------ distractors
def desktop_summary(rng, path):
    rows = []
    vol = {"ST": 9.8e6, "LA": 7.4e6, "KD": 5.6e6}
    for m in range(2, 9):
        for t in P.TITLES:
            v = int(round(vol[t] * P.SEASON[m] * rng.uniform(0.97, 1.03) / 300)) * 300
            sh = 6.1 + (0.4 if m >= 3 else 0) + (0.5 if m >= 4 else 0) + (0.6 if m >= 5 else 0) \
                + rng.uniform(-0.25, 0.25) + {"ST": 0.4, "LA": 0.0, "KD": -0.3}[t]
            rows.append((f"2026-{m:02d}", P.TITLE_NAME[t], v, round(sh, 2),
                         int(round(rng.uniform(1480, 1720)))))
    pd.DataFrame(rows, columns=["month", "title", "desktop_page_views", "share_over_line_pct",
                                "p75_lcp_ms"]).to_csv(path, index=False, lineterminator="\n")


def amp_report(rng, path):
    rows = []
    vol = {"ST": 2.1e6, "LA": 1.6e6, "KD": 1.2e6}
    for m in range(2, 9):
        fade = 1 - 0.035 * (m - 2)
        for t in P.TITLES:
            v = int(round(vol[t] * fade * rng.uniform(0.96, 1.04)))
            rows.append((f"2026-{m:02d}", P.TITLE_NAME[t], v, int(round(v * rng.uniform(2.1, 2.4))),
                         "amp-ad (AMP runtime, no Prebid wrapper)",
                         round(rng.uniform(4.8, 6.4), 2), int(round(rng.uniform(1650, 1980)))))
    pd.DataFrame(rows, columns=["month", "title", "amp_landing_views", "amp_ad_requests",
                                "ad_integration", "share_over_line_pct", "p75_lcp_ms"]).to_csv(
        path, index=False, lineterminator="\n")


def newsletter_sends(rng, path):
    rows = []
    d = date(2026, 2, 1)
    lists = {"ST": ["Morgen", "Sport", "Aften"], "LA": ["Morgen", "Lokalt"], "KD": ["Morgen", "Lokalt"]}
    subs = {"ST": 41800, "LA": 30200, "KD": 22600}
    while d <= date(2026, 8, 31):
        for t in P.TITLES:
            for nl in lists[t]:
                if nl == "Sport" and d.weekday() not in (0, 3):
                    continue
                n = int(subs[t] * {"Morgen": 1.0, "Sport": 0.42, "Aften": 0.55, "Lokalt": 0.61}[nl]
                        * rng.uniform(0.985, 1.01))
                hour = {"Morgen": "06:00", "Sport": "07:30", "Aften": "18:30", "Lokalt": "06:30"}[nl]
                op = rng.uniform(0.38, 0.47)
                rows.append((d.isoformat(), hour, P.TITLE_NAME[t], nl, n, int(n * op),
                             int(n * op * rng.uniform(0.18, 0.26))))
        d += timedelta(days=1)
    pd.DataFrame(rows, columns=["send_date", "send_time_local", "title", "newsletter", "recipients",
                                "unique_opens", "unique_clicks"]).to_csv(path, index=False,
                                                                         lineterminator="\n")


# ------------------------------------------------------------------ provenance
MANIFEST = [
    ("spine", "RUM beacon export, mobile web and app webviews, three titles", "2026-02-01 to 2026-08-31", "Gunhild Lund", "Export from the RUM collector (v1 forwarder to 7 May, v2 from 8 May), pulled 2026-09-05"),
    ("release", "Release train log", "2026-01-05 to 2026-08-31", "Mette Johansen", "Export from the release tool"),
    ("rollout", "Bølge rollout log", "Waves 1 to 6", "Finn Thygesen", "Maintained by the front-end platform team"),
    ("changes", "Platform change register, 2026 extract", "Changes live since February", "Mette Johansen", "Extract of the change register"),
    ("registry", "Device registry", "Models seen on group sites, benchmark bands", "Simone Thorsen", "Registry snapshot, September 2026"),
    ("subs", "Subscription register extract", "Accounts signed in on sampled devices", "Gunhild Lund", "Extract from the subscription system, 2026-09-05"),
    ("editions", "Edition register", "Local editions and their mastheads", "Caroline Mortensen", "Editorial register"),
    ("sla", "Page delivery service level, version 3", "In force from 2026-01-01", "Elin Lauritsen", "Filed document"),
    ("paywall", "Subscriber terms, layout and access (extract)", "Version 2026-01", "Abonnementsservice", "Filed document"),
    ("closeout", "Q3 service close-out, mobile page delivery", "2026-02 to 2026-08", "Gunhild Lund", "Computed from the RUM export, v1.2"),
    ("crawl", "Synthetic crawl request log", "Monthly crawls, February to August", "Simone Thorsen", "Export from the synthetic monitoring tool"),
    ("crawlcfg", "Synthetic crawl run configuration", "Lists v1 and v2", "Simone Thorsen", "Tool configuration"),
    ("assets", "Web asset register", "Hosts and path prefixes in use", "Finn Thygesen", "Maintained by the front-end platform team"),
    ("roster", "Operations squad: closed fixes", "Fixes closed 2023 to January 2026", "Simone Thorsen", "Squad register"),
    ("cdn", "Image CDN daily delivery log", "2026-02-01 to 2026-08-31, both vendors", "Gunhild Lund", "Merged vendor exports"),
    ("cdnapp", "Image CDN delivery log, appendix C", "Field definitions", "Digital operations", "Filed document"),
    ("guide", "RUM export field guide", "Beacon export, registers and logs", "Gunhild Lund", "Filed document"),
    ("thread", "Service review prep thread", "2 September 2026", "digital-ops-review list", "Mail export"),
    ("desktop", "Desktop field summary", "2026-02 to 2026-08", "Gunhild Lund", "Computed from the desktop RUM export"),
    ("amp", "AMP landing-view report", "2026-02 to 2026-08", "Gunhild Lund", "Export from the AMP analytics report"),
    ("news", "Newsletter send log", "2026-02-01 to 2026-08-31", "Caroline Mortensen", "Export from the newsletter platform"),
]


def manifest(path, names):
    rows = [(F[k], what, cov, owner, how) for k, what, cov, owner, how in MANIFEST]
    df = pd.DataFrame(rows, columns=["file", "what_it_is", "covers", "owner", "how_produced"])
    assert sorted(df.file) == sorted(n for n in names if n != F["manifest"]), "manifest set"
    df.to_csv(path, index=False, lineterminator="\n")
