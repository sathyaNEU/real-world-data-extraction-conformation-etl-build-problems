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


# platform changes outside the review's five: name, owner, scope as the register states it
MINOR = [
    ("Editorial tools: byline cards", "Simone Thorsen", "CMS, all titles"),
    ("Search: synonym list", "Finn Thygesen", "Search pages, all titles"),
    ("Paywall copy update", "Ove Schmidt", "Paywall prompts, all titles"),
    ("Comments moderation queue", "Simone Thorsen", "CMS, all titles"),
    ("Video player patch", "Finn Thygesen", "Video player, all templates"),
    ("Newsletter sign-up form", "Gunhild Lund", "Sign-up forms, all titles"),
    ("Sitemap generation fix", "Mette Johansen", "Servers, all titles"),
    ("Accessibility fixes (forms)", "Finn Thygesen", "Forms, all templates"),
    ("Weather widget data source", "Simone Thorsen", "Front page widget, all titles"),
    ("TV guide listings feed", "Simone Thorsen", "TV guide pages, all titles"),
    ("Obituaries upload form", "Simone Thorsen", "CMS, all titles"),
    ("Front page curation tool", "Simone Thorsen", "CMS, all titles"),
    ("Image credit field", "Caroline Mortensen", "CMS, all titles"),
    ("Election results module", "Finn Thygesen", "Results pages, all titles"),
    ("Podcast player embed", "Finn Thygesen", "Article template, all titles"),
    ("Crossword archive pages", "Gunnar Paulsen", "Spil pages, all titles"),
    ("Event calendar feed", "Simone Thorsen", "Calendar pages, all titles"),
    ("Sports results feed", "Simone Thorsen", "Sport template, all titles"),
    ("Live blog editor: pinned posts", "Simone Thorsen", "CMS, all titles"),
    ("Push opt-in prompt", "Gunhild Lund", "App webview, all titles"),
]
ROUTINE = ["Dependency updates", "Minor CMS fixes", "Copy and translation fixes", "Logging changes",
           "Feature flag cleanup", "Admin UI fixes"]
# change numbers run with the date a change was raised; the review's five keep theirs
CHG_ANCHORS = [(date(2026, 1, 20), 2490), (date(2026, 3, 3), 2529), (date(2026, 4, 7), 2547),
               (date(2026, 5, 5), 2583), (date(2026, 6, 24), 2611), (date(2026, 9, 1), 2650)]
MINOR_CHG = {}


def _minor_plan(rng, n):
    """Which generic releases carry which minor change (first release, then follow-up fixes), the
    tracking plan's versions and the routine dependency updates."""
    items = [[] for _ in range(n)]
    order = rng.permutation(len(MINOR))
    starts = np.linspace(0, max(1, n - 4), len(MINOR))
    for k, s0 in zip(order, starts):
        s = int(min(n - 1, max(0, round(s0 + rng.integers(-1, 2)))))
        reps = int(rng.integers(1, 4))
        pos = [s]
        for _ in range(reps - 1):
            pos.append(min(n - 1, pos[-1] + int(rng.integers(1, 5))))
        for j, p_ in enumerate(sorted(set(pos))):
            items[p_].append((int(k), j > 0))
    ver = 13
    for p_ in range(int(rng.integers(2, 6)), n, 9):
        items[p_].append(("track", ver))
        ver += 1
    last = None
    for i in range(n):
        if not items[i] or rng.random() < 0.25:
            pick = [r for r in range(len(ROUTINE)) if r != last]
            last = int(rng.choice(pick))
            items[i].append(("routine", last))
    return items


def _minor_ids(first_day):
    import bisect
    taken = {int(v[0][4:]) for v in P.CHG.values()}
    out = {}
    xs = [a.toordinal() for a, _ in CHG_ANCHORS]
    for k in sorted(first_day, key=lambda k: (first_day[k], k)):
        d = first_day[k].toordinal()
        j = min(max(bisect.bisect_right(xs, d), 1), len(xs) - 1)
        (a0, n0), (a1, n1) = CHG_ANCHORS[j - 1], CHG_ANCHORS[j]
        num = int(round(n0 + (n1 - n0) * (d - a0.toordinal()) / (a1.toordinal() - a0.toordinal())))
        while num in taken:
            num += 1
        taken.add(num)
        out[k] = "CHG-%d" % num
    return out


def release_log(rng, dep, path):
    rows = []
    special = ("E", "B", "D", "RUM", "PUZ")
    generic = [i for i, r in enumerate(dep.itertuples()) if r.tag not in special and not r.tag.startswith("COH:")]
    plan = _minor_plan(rng, len(generic))
    first = {}
    for g, its in zip(generic, plan):
        for k, _ in its:
            if isinstance(k, int) and k not in first:
                first[k] = pd.Timestamp(dep.local.iloc[g]).date()
    MINOR_CHG.clear()
    MINOR_CHG.update(_minor_ids(first))
    slot = dict(zip(generic, plan))
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
            parts = []
            for k, x in slot[i]:
                if k == "track":
                    parts.append(f"Tracking plan v{x}")
                elif k == "routine":
                    parts.append(ROUTINE[x])
                else:
                    name = MINOR[k][0]
                    parts.append(f"{name}{': fixes' if x else ''} ({MINOR_CHG[k]})")
            note = "; ".join(parts)
        # the release managers' rota: alternate ISO weeks
        mgr = "Mette Johansen" if loc.isocalendar()[1] % 2 == 0 else "Simone Thorsen"
        rows.append({"release_id": f"RT-26-{i + 1:03d}",
                     "deployed_at": loc.isoformat(timespec="seconds"),
                     "platform_bundle": "platform." + "".join(rng.choice(list("0123456789abcdef"), 10)),
                     "puzzles_bundle": "spil." + "".join(rng.choice(list("0123456789abcdef"), 10)),
                     "approved_by": mgr, "notes": note})
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
        ("B", "Templates with a hero image (%s)" % ", ".join(t for t in P.COHORTS + P.LEGACY if t in P.HERO),
         P.DATED["B"].isoformat(), ", ".join(rid(P.CHG["B"][0]))),
        ("D", "All templates, all titles", P.DATED["D"].isoformat(), ", ".join(rid(P.CHG["D"][0]))),
        ("A", "Ad-supported layout: spil pages, then the Bølge template groups wave by wave",
         P.PUZZLE_AD_SWITCH.isoformat(), ", ".join(rid(P.CHG["A"][0]))),
        ("C", "Bølge template groups: ad-free layout on all six at once, ad-supported layout wave "
              "by wave (see the rollout log)",
         P.COHORT_SWITCH["sektion"].isoformat(), ", ".join(rid(P.CHG["C"][0]))),
    ]
    out = [(P.CHG[k][0], P.CHG[k][1], owners[k], scope, live, rels) for k, scope, live, rels in rows]
    for k, cid in MINOR_CHG.items():
        hit = rel[rel.notes.str.contains(cid, regex=False)]
        live = pd.Timestamp(hit.deployed_at.iloc[0]).date().isoformat()
        out.append((cid, MINOR[k][0], MINOR[k][1], MINOR[k][2], live, ", ".join(hit.release_id)))
    out.sort(key=lambda r: r[0])
    for i, vals in enumerate(out):
        for j, val in enumerate(vals):
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
Q3 = (7, 8)


def closeout_table(v):
    v = v[v.month.isin(Q3)]
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
    ws.write(1, 0, "v1.2, refreshed 5 September 2026 (owner Gunhild Lund). For the quarterly service review.")
    ws.write(2, 0, "Mobile page views and the share of scored views over the service line, July and "
                   "August, by current masthead. Describes delivery against the line; it does not "
                   "attribute the share to any release.")
    hdr = ["Month", "Title", "Mobile page views", "Scored views", "Over-line views",
           "Share over line (%)"]
    for j, h in enumerate(hdr):
        ws.write(3, j, h, b)
    r = 4
    for m in Q3:
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
    for i, m in enumerate(Q3):
        x = t[t.month == m]
        ws2.write(3 + i, 0, f"2026-{m:02d}")
        ws2.write_number(3 + i, 1, int(x.views.sum()), n0)
        ws2.write_number(3 + i, 2, int(x.scored.sum()), n0)
        ws2.write_number(3 + i, 3, int(x.over.sum()), n0)
        ws2.write_number(3 + i, 4, round(100 * x.over.sum() / x.scored.sum(), 2), pct)
    ws2.set_column(0, 4, 17)
    wb.close()
    normalise_zip(path, datetime(2026, 9, 4, 11, 5))


def cdn_file(df, path):
    csv(df, path)
