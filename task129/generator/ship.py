"""task129 generator: deterministic writers for the data files under target/."""
import io
import json
import os
import zipfile
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import xlsxwriter

import params as P
import world as Wd
import lab
from golden import F

XLSX_WHEN = datetime(2026, 9, 4, 16, 20, 0)


def csv(df, path):
    df.to_csv(path, index=False, lineterminator="\n")


def normalise_zip(path, when):
    with zipfile.ZipFile(path) as z:
        data = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as out:
        for name, blob in data:
            zi = zipfile.ZipInfo(name, date_time=when.timetuple()[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            out.writestr(zi, blob)
    open(path, "wb").write(buf.getvalue())


def workbook(path, author, when):
    wb = xlsxwriter.Workbook(path, {"strings_to_numbers": False})
    wb.set_properties({"author": author, "company": P.ORG, "created": when})
    wb.set_calc_mode("auto")
    return wb


# ------------------------------------------------------------------ the spine
def spine(S, path):
    ts = pd.DatetimeIndex(S.ts.values).tz_localize("UTC")
    acc = S.account_key.values
    lcp = S.lcp_ms.values
    cols = {
        "beacon_id": pa.array(S.beacon_id.values, pa.int64()),
        "pv_id": pa.array(S.pv_id.values, pa.string()),
        "ts_utc": pa.array(ts.as_unit("ms"), pa.timestamp("ms", tz="UTC")),
        "device_key": pa.array(S.device_key.values, pa.string()),
        "account_key": pa.array([a if a else None for a in acc], pa.string()),
        "title": pa.array(S.title.values, pa.string()),
        "template": pa.array(S.template.values, pa.string()),
        "url_path": pa.array(S.url_path.values, pa.string()),
        "device_model": pa.array(S.model.values, pa.string()),
        "os": pa.array(S.os.values, pa.string()),
        "browser": pa.array(S.browser.values, pa.string()),
        "effective_connection_type": pa.array(S.effective_connection_type.values, pa.string()),
        "navigation_type": pa.array(S.navigation_type.values, pa.string()),
        "referrer_class": pa.array(S.referrer_class.values, pa.string()),
        "ttfb_ms": pa.array(S.ttfb_ms.values.astype(np.int32), pa.int32()),
        "lcp_ms": pa.array([None if np.isnan(x) else int(x) for x in lcp], pa.int32()),
        "cls": pa.array(S.cls.values.astype(float), pa.float64()),
        "sample_weight": pa.array(S.weight.values.astype(np.int16), pa.int16()),
    }
    tbl = pa.table(cols)
    pq.write_table(tbl, path, compression="zstd", compression_level=9, row_group_size=250_000,
                   use_dictionary=True, data_page_version="1.0", write_statistics=True)
    return len(S)


# ------------------------------------------------------------------ registers and logs
def registry(path):
    csv(Wd.registry(), path)


def editions(path):
    csv(Wd.edition_register(), path)


GENERIC_NOTES = [
    "Editorial tools: byline cards", "Search: synonym list", "Paywall copy update",
    "Dependency updates", "Comments moderation queue", "Video player patch",
    "Newsletter sign-up form", "Sitemap generation fix", "Accessibility fixes (forms)",
    "Weather widget data source", "TV guide listings feed", "Obituaries upload form",
    "Front page curation tool", "Tracking plan v14", "Image credit field", "Election results module",
]


def release_log(rng, dep, path):
    rows = []
    for i, r in enumerate(dep.itertuples()):
        loc = pd.Timestamp(r.local).tz_localize(P.TZ)
        tag = r.tag
        if tag in ("E", "B", "D"):
            note = {"E": f"Brand web fonts live on all templates ({P.CHG['E'][0]})",
                    "B": f"Image pipeline: responsive renditions on hero templates ({P.CHG['B'][0]})",
                    "D": f"Consent banner: new CMP on all templates ({P.CHG['D'][0]})"}[tag]
        elif tag == "RUM":
            note = "RUM beacon v2 (collector v2): sampling rate set per property and sign-in"
        elif tag == "PUZ":
            note = f"Spil: header bidding on ad-supported puzzle pages ({P.CHG['A'][0]})"
        elif tag.startswith("COH:"):
            c = tag[4:]
            wave = P.COHORTS.index(c) + 1
            note = f"Bølge wave {wave}: {c} templates ({P.CHG['C'][0]}, {P.CHG['A'][0]})"
            if wave == 1:
                note += "; ad-free layout on all six template groups"
        else:
            k = int(rng.integers(1, 3))
            note = "; ".join(rng.choice(GENERIC_NOTES, k, replace=False))
        rows.append({"release_id": f"RT-26-{i + 1:03d}",
                     "deployed_at": loc.isoformat(timespec="seconds"),
                     "platform_bundle": "platform." + "".join(rng.choice(list("0123456789abcdef"), 10)),
                     "puzzles_bundle": "spil." + "".join(rng.choice(list("0123456789abcdef"), 10)),
                     "approved_by": "Mette Johansen", "notes": note})
    df = pd.DataFrame(rows)
    csv(df, path)
    return df


def rollout_log(rel, path):
    rows = []
    for i, c in enumerate(P.COHORTS):
        m = rel.notes.str.startswith(f"Bølge wave {i + 1}:")
        r = rel[m].iloc[0]
        if i == 0:
            rows.append({"wave": 1, "layout": "ad-free (signed-in subscribers)",
                         "template_groups": "; ".join(P.COHORTS), "release_id": r.release_id,
                         "switched_on": r.deployed_at, "front_end": "Bølge", "ad_stack": "none",
                         "signed_off_by": "Finn Thygesen"})
        rows.append({"wave": i + 1, "layout": "ad-supported", "template_groups": c,
                     "release_id": r.release_id, "switched_on": r.deployed_at,
                     "front_end": "Bølge", "ad_stack": "Prebid header-bidding wrapper",
                     "signed_off_by": "Finn Thygesen"})
    csv(pd.DataFrame(rows), path)


def subscriptions(rng, dev, path):
    rows = []
    sub = dev[dev.gtype == "sub"]
    products = ["Digital", "Digital", "Digital+ (alle titler)", "Weekend + digital"]
    for r in sub.itertuples():
        if pd.isna(r.sub_start_in_window):
            st = date(2019, 1, 1) + timedelta(days=int(rng.integers(0, 2400)))
            st = min(st, date(2026, 1, 20))
        else:
            st = pd.Timestamp(r.sub_start_in_window).date()
        end = "2026-10-31" if rng.random() < 0.02 else ""
        rows.append((r.account_key, st.isoformat(), end, r.home,
                     products[int(rng.integers(0, len(products)))]))
    free = dev[dev.gtype == "free"]
    for r in free.itertuples():
        if rng.random() < 0.28:
            st = date(2020, 1, 1) + timedelta(days=int(rng.integers(0, 1500)))
            en = st + timedelta(days=int(rng.integers(60, 700)))
            en = min(en, date(2025, 12, 31))
            rows.append((r.account_key, st.isoformat(), en.isoformat(), r.home, "Digital"))
    df = pd.DataFrame(rows, columns=["account_key", "start_date", "end_date", "title", "product"])
    df = df.sort_values(["account_key", "start_date"]).reset_index(drop=True)
    df.insert(0, "subscription_id", [f"S-{int(x):07d}" for x in
                                     rng.choice(np.arange(1_200_000, 2_900_000), len(df), replace=False)])
    df["title"] = df.title.map(P.TITLE_NAME)
    csv(df[["subscription_id", "account_key", "title", "product", "start_date", "end_date"]], path)
    return df


def change_register(rel, path):
    wb = workbook(path, "Mette Johansen", XLSX_WHEN)
    ws = wb.add_worksheet("Register")
    b = wb.add_format({"bold": True})
    ws.write(0, 0, "Digital platform change register, 2026 (extract)", b)
    ws.write(1, 0, "Changes shipped since February that touch every title. Maintained by the release manager.")
    hdr = ["Change", "Name", "Owner", "Scope", "Live from", "Release(s)"]
    for j, h in enumerate(hdr):
        ws.write(3, j, h, b)

    def rid(pat):
        return rel[rel.notes.str.contains(pat, regex=False)].release_id.tolist()
    owners = {"A": "Gunnar Paulsen", "B": "Caroline Mortensen", "C": "Finn Thygesen",
              "D": "Ove Schmidt", "E": "Caroline Mortensen"}
    rows = [
        ("E", "All templates, all titles", P.DATED["E"].isoformat(), ", ".join(rid(P.CHG["E"][0]))),
        ("B", "Templates with a hero image", P.DATED["B"].isoformat(), ", ".join(rid(P.CHG["B"][0]))),
        ("D", "All templates, all titles", P.DATED["D"].isoformat(), ", ".join(rid(P.CHG["D"][0]))),
        ("A", "Ad-supported layout: spil pages, then the Bølge template groups wave by wave",
         P.PUZZLE_AD_SWITCH.isoformat(), ", ".join(rid(P.CHG["A"][0]))),
        ("C", "Bølge template groups: ad-free layout on all six at once, ad-supported layout wave "
              "by wave (see the rollout log)",
         P.COHORT_SWITCH["sektion"].isoformat(), ", ".join(rid(P.CHG["C"][0]))),
    ]
    for i, (k, scope, live, rels) in enumerate(rows):
        for j, val in enumerate([P.CHG[k][0], P.CHG[k][1], owners[k], scope, live, rels]):
            ws.write(4 + i, j, val)
    ws.set_column(0, 0, 11)
    ws.set_column(1, 1, 44)
    ws.set_column(2, 2, 20)
    ws.set_column(3, 3, 62)
    ws.set_column(4, 4, 11)
    ws.set_column(5, 5, 70)
    wb.close()
    normalise_zip(path, XLSX_WHEN)


# ------------------------------------------------------------------ the close-out (context artifact)
def closeout_table(v):
    v = v[(v.month >= 2) & (v.month <= 8)]
    g = v.assign(sw=v.w * v.scored, ow=v.w * (v.scored & v.over)).groupby(["month", "title_cur"])
    t = pd.DataFrame({"views": g.w.sum(), "scored": g.sw.sum(), "over": g.ow.sum()}).reset_index()
    return t


def closeout(t, path):
    wb = workbook(path, "Gunhild Lund", datetime(2026, 9, 4, 11, 5))
    b = wb.add_format({"bold": True})
    pct = wb.add_format({"num_format": "0.00"})
    n0 = wb.add_format({"num_format": "#,##0"})
    ws = wb.add_worksheet("By title")
    ws.write(0, 0, "Digital operations: Q3 service close-out, mobile page delivery", b)
    ws.write(1, 0, "v1.2, refreshed 4 September 2026 (owner Gunhild Lund). For the quarterly service review.")
    ws.write(2, 0, "Monthly mobile page views and the share of scored views over the service line, by "
                   "current masthead. Describes delivery against the line; it does not attribute the "
                   "share to any release.")
    hdr = ["Month", "Title", "Mobile page views", "Scored views", "Over-line views",
           "Share over line (%)"]
    for j, h in enumerate(hdr):
        ws.write(3, j, h, b)
    r = 4
    for m in range(2, 9):
        for ti in P.TITLES:
            x = t[(t.month == m) & (t.title_cur == ti)].iloc[0]
            ws.write(r, 0, f"2026-{m:02d}")
            ws.write(r, 1, P.TITLE_NAME[ti])
            ws.write_number(r, 2, int(x.views), n0)
            ws.write_number(r, 3, int(x.scored), n0)
            ws.write_number(r, 4, int(x.over), n0)
            ws.write_number(r, 5, round(100 * x.over / x.scored, 2), pct)
            r += 1
    ws.set_column(0, 0, 9)
    ws.set_column(1, 1, 18)
    ws.set_column(2, 5, 17)
    ws2 = wb.add_worksheet("Group")
    ws2.write(0, 0, "All three titles", b)
    for j, h in enumerate(["Month", "Mobile page views", "Scored views", "Over-line views",
                           "Share over line (%)"]):
        ws2.write(2, j, h, b)
    for i, m in enumerate(range(2, 9)):
        x = t[t.month == m]
        ws2.write(3 + i, 0, f"2026-{m:02d}")
        ws2.write_number(3 + i, 1, int(x.views.sum()), n0)
        ws2.write_number(3 + i, 2, int(x.scored.sum()), n0)
        ws2.write_number(3 + i, 3, int(x.over.sum()), n0)
        ws2.write_number(3 + i, 4, round(100 * x.over.sum() / x.scored.sum(), 2), pct)
    ws2.set_column(0, 4, 17)
    wb.close()
    normalise_zip(path, datetime(2026, 9, 4, 11, 5))


# ------------------------------------------------------------------ crawl, config, assets
def crawl_files(rng, tgt):
    df, v1, v2 = lab.crawl(rng)
    csv(df, os.path.join(tgt, F["crawl"]))
    csv(lab.asset_register(), os.path.join(tgt, F["assets"]))
    cfg = {
        "crawler": "SMDQ synthetic monitoring, monthly mobile crawl",
        "owner": "Simone Thorsen",
        "user_agent": lab.AGENT,
        "profile": {"device": "Moto G Power (emulated)", "network": "4G throttled 9 Mbps / 170 ms",
                    "consent": "no stored choice", "login": "anonymous (ad-supported layout)",
                    "cache": "cold: one run per URL, browser cache and service worker cleared"},
        "url_lists": {"v1": {"in_use_from": "2026-01-01", "urls": int(len(v1))},
                      "v2": {"in_use_from": lab.LIST_V2_FROM.isoformat(), "urls": int(len(v2)),
                             "note": "refreshed list: stale article URLs replaced"}},
        "comparison_rule": "Comparisons across crawls use the URLs present in both crawls' lists.",
        "retries": "A run that times out is retried once later the same night; the completed run "
                   "is the run of record. Both runs are filed.",
        "crawls": [{"crawl_date": d.isoformat(), "url_list": "v2" if d >= lab.LIST_V2_FROM else "v1"}
                   for d in lab.CRAWL_DATES],
    }
    with open(os.path.join(tgt, F["crawlcfg"]), "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return df, v1, v2


def cdn_file(df, path):
    csv(df, path)


# ------------------------------------------------------------------ the closed-fix roster
FIXES = [
    ("OPS-FX-231", "2023-03-14", "Lazy-load images below the fold", "artikel", 0.58, 118.0, 31.0),
    ("OPS-FX-237", "2023-06-06", "Subset legacy web fonts", "all", 0.21, 64.0, 66.0),
    ("OPS-FX-244", "2023-09-19", "Edge cache for front-page HTML", "forside", 1.42, 0.0, 6.4),
    ("OPS-FX-251", "2023-11-28", "Stop video player autoload", "artikel, liveblog", 0.47, 212.0, 23.0),
    ("OPS-FX-262", "2024-02-20", "Lazy-load ad slots on puzzle pages", "spil", 2.20, 46.0, 4.6),
    ("OPS-FX-268", "2024-05-07", "Recompress hero images (quality 72)", "hero templates", 0.92, 180.0, 56.0),
    ("OPS-FX-275", "2024-08-27", "Inline critical CSS", "all", 0.33, 8.0, 64.0),
    ("OPS-FX-283", "2024-11-12", "Defer analytics tags", "all", 0.29, 22.0, 65.0),
    ("OPS-FX-290", "2025-03-04", "Edge caching of article HTML", "artikel", 0.74, 0.0, 30.5),
    ("OPS-FX-297", "2025-08-19", "Liveblog polling every 30 s instead of 10 s", "liveblog", 1.36, 14.0, 3.1),
    ("OPS-FX-304", "2026-01-13", "Preconnect to the image host", "hero templates", 0.37, 0.0, 57.5),
]


def roster(rng, path):
    rows = []
    for fid, gl, name, scope, drop, kb, mviews in FIXES:
        pre_v = int(round(mviews * 1e6 * 28 / 30.4 / 300)) * 300
        post_v = int(round(pre_v * rng.uniform(0.97, 1.03) / 300)) * 300
        s_pre = rng.uniform(0.17, 0.27)
        s_post = s_pre - drop / 100
        pre_o = int(round(pre_v * s_pre / 300)) * 300
        post_o = int(round(post_v * s_post / 300)) * 300
        golive = date.fromisoformat(gl)
        fm = date(golive.year + (golive.month == 12), golive.month % 12 + 1, 1)
        month_v = int(round(mviews * 1e6 * rng.uniform(0.98, 1.03) / 300)) * 300
        saving = round((pre_o / pre_v - post_o / post_v) * month_v)
        closed = golive + timedelta(days=int(rng.integers(30, 45)))
        rows.append([fid, name, scope, gl, pre_v, pre_o, post_v, post_o, fm.strftime("%Y-%m"),
                     month_v, saving, kb, closed.isoformat()])
    cols = ["Fix", "What was changed", "Templates", "Go-live", "Views, 4 wk before",
            "Over-line views, 4 wk before", "Views, 4 wk after", "Over-line views, 4 wk after",
            "First full month", "Mobile views in that month", "Realised saving (views a month)",
            "Crawl kB removed per page", "Closed"]
    wb = workbook(path, "Simone Thorsen", datetime(2026, 2, 3, 9, 40))
    b = wb.add_format({"bold": True})
    n0 = wb.add_format({"num_format": "#,##0"})
    ws = wb.add_worksheet("Closed fixes")
    ws.write(0, 0, "Operations squad: fixes closed, with what each brought back", b)
    ws.write(1, 0, "Saving = (over-line share before - share after) x mobile views of the fix's "
                   "templates in the first full month after go-live. Counts are mobile field views.")
    for j, h in enumerate(cols):
        ws.write(2, j, h, b)
    for i, r in enumerate(rows):
        for j, val in enumerate(r):
            if isinstance(val, (int, np.integer)):
                ws.write_number(3 + i, j, int(val), n0)
            elif isinstance(val, float):
                ws.write_number(3 + i, j, val)
            else:
                ws.write(3 + i, j, val)
    ws.set_column(0, 0, 11)
    ws.set_column(1, 1, 42)
    ws.set_column(2, 2, 18)
    ws.set_column(3, 12, 14)
    wb.close()
    normalise_zip(path, datetime(2026, 2, 3, 9, 40))
    return pd.DataFrame(rows, columns=cols)
