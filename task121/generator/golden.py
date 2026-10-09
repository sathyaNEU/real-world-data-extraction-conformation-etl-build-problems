"""Q4 sprint call for the checkout conversion review (INC-0914).

python3 golden.py [target_dir] [out_dir]

Reads the review-folder extracts in target_dir and writes q4_sprint_call.html and
checkout_fall_workings.xlsx to out_dir. Prints the figures the call rests on.
"""
import html
import json
import math
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "target"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE.parent / "golden"
SCRUB = HERE.parents[1] / ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py"
PREPARED = datetime(2026, 9, 30, 17, 40)   # the page and workings were finished for the Friday review

# Monday-to-Sunday weeks, Lisbon time (field reference). August is the before-the-fall window the
# shortlist's sizing line names; W1 is the dashboard's first down week.
WEEK_START = {"B0": "2026-07-27", "B1": "2026-08-03", "B2": "2026-08-10", "B3": "2026-08-17",
              "B4": "2026-08-24", "W1": "2026-08-31", "W2": "2026-09-07", "W3": "2026-09-14",
              "W4": "2026-09-21"}
BEFORE = ["B1", "B2", "B3", "B4"]
REVIEW = ["W1", "W2", "W3", "W4"]
CHART_WEEKS = BEFORE + REVIEW
CALL_WEEK = "W4"
CHALLENGE = {"C", "D"}            # provider's report: D is a decoupled (app) challenge
FINANCE_NET_FROM = pd.Timestamp("2026-08-10")
VAT = 1.23
CHALLENGED_ISSUERS = {"Bankora", "Finvo"}

# The five shortlisted fixes and the customers each is for, in the shortlist's own words.
FIXES = [
    ("F1", "Inline postcode lookup", "Duarte Cunha", "addr",
     "Accounts whose saved address the new check rejects"),
    ("F2", "Club landing page", "Lia Neto", "newfan",
     "Fans new to the store landing from the club app"),
    ("F3", "Card SDK upgrade", "Cristiano Soares", "card",
     "Saved-card payments Bankora and Finvo began challenging"),
    ("F4", "One-time-code sign-in", "Jaime Jesus", "acct",
     "Account holders arriving from the club app without signing in"),
    ("F5", "Split dispatch", "Raquel Pires", "mixed",
     "Baskets mixing pre-order and in-stock lines"),
]
FIX_NAME = {f: n for f, n, _, _, _ in FIXES}
POP = {f: p for f, _, _, p, _ in FIXES}


def lc(name):
    """A fix name inside a sentence: lower case, acronyms kept."""
    return " ".join(w if w.isupper() and len(w) > 1 else w.lower() for w in name.split())
CAUSE = {f: c for f, _, _, _, c in FIXES}


def one(prefix, ext):
    hits = sorted(p for p in TARGET.iterdir() if p.name.startswith(prefix) and p.name.endswith(ext))
    assert len(hits) == 1, (prefix, hits)
    return hits[0]


def week_of(ts):
    edges = pd.to_datetime(list(WEEK_START.values())).values
    names = np.array(list(WEEK_START))
    return names[np.searchsorted(edges, ts.values, side="right") - 1]


def load_sessions():
    s = pd.read_parquet(one("basket_sessions", ".parquet"))
    n_raw = len(s)
    bots = set(pd.read_csv(one("edge_bot_verdicts", ".csv")).session_id)
    s = s[~s.session_id.isin(bots)].copy()          # edge-flagged sessions are out of every figure
    s["ts"] = pd.to_datetime(s.started_at)
    s["wk"] = week_of(s.ts)
    s["ordered"] = s.order_id.notna()
    return s, n_raw


def attach_club_accounts(s):
    """Club Shop-tab links carry the members'-price token (mpt). Token -> member number comes from the
    club's billing reports (August and September); member number -> account from the loyalty profiles and
    from last season's members' code (SOCIO + seven-digit member number) redeemed on an account."""
    tokens = pd.concat([pd.read_csv(one("cdm_token_billing_2026-08", ".csv")),
                        pd.read_csv(one("cdm_token_billing_2026-09", ".csv"))])
    assert tokens.token.is_unique
    prof = pd.read_csv(one("loyalty_profiles", ".csv"), dtype={"club_member_no": "Int64"})
    prof = prof.dropna(subset=["club_member_no"])
    assert prof.club_member_no.is_unique
    member_of = dict(zip(tokens.token, tokens.member_no))
    account_of = dict(zip(prof.club_member_no.astype(int), prof.account_id))
    promo = pd.read_csv(one("promo_redemptions", ".csv"), dtype={"account_id": str})
    promo = promo.dropna(subset=["account_id"])
    socio = promo[promo.promo_code.str.fullmatch(r"SOCIO\d{7}")]
    on_profile = dict(account_of)
    for code, a in zip(socio.promo_code, socio.account_id):
        m = int(code[5:])
        assert account_of.get(m, a) == a
        account_of[m] = a
    s["club"] = s.landing_url.str.contains("mpt=", regex=False)
    tok = s.landing_url.str.extract(r"[?&]mpt=([^&]+)")[0]
    assert tok[s.club].notna().all()
    mem = tok.map(member_of)
    s["club_account"] = [account_of.get(int(m)) if pd.notna(m) else None for m in mem]
    s["acct"] = s.club & s.club_account.notna()
    s["acct_profile_only"] = s.club & pd.Series([pd.notna(m) and int(m) in on_profile for m in mem], index=s.index)
    s["newfan"] = s.club & s.club_account.isna()
    return s


def attach_cohorts(s):
    """Cohort at the session: the latest assignment at or before it, every logged move included."""
    fl = json.load(open(one("checkout_flags_export", ".json"), encoding="utf-8"))
    current = {a["account_id"]: a["cohort"] for a in fl["assignments"]}
    enabled = {r["cohort"]: pd.Timestamp(r["enabled_at"][:19]) for r in fl["rollout"]}
    moved = {}
    for m in fl["assignment_moves"]:
        moved.setdefault(m["account_id"], []).append((pd.Timestamp(m["moved_at"][:19]), m["from_cohort"], m["to_cohort"]))
    coh = []
    for a, t, si in zip(s.account_id, s.ts, s.signed_in):
        if not si:
            coh.append(0)                     # the flag applies to signed-in sessions only
            continue
        if a not in moved:
            coh.append(current[a])
            continue
        hist = sorted(moved[a])
        c = hist[0][1]                        # before its first move the account sat where that move took it from
        for when, _, to in hist:
            if when <= t:
                c = to
        coh.append(c)
    s["cohort"] = coh
    s["flag_live"] = [c > 0 and t >= enabled[c] for c, t in zip(s.cohort, s.ts)]
    return s, enabled


def attach_saved_address(s):
    """Default saved address at the session. changed_at is UTC; sessions are Lisbon (UTC+1 all window)."""
    ab = pd.read_csv(one("address_book_history", ".csv"), dtype={"postcode": str})
    ab = ab[ab.is_default].copy()
    ab["local"] = (pd.to_datetime(ab.changed_at) + pd.Timedelta(hours=1)).astype("datetime64[ns]")
    ab = ab.sort_values("local")
    si = s.loc[s.signed_in, ["session_id", "account_id", "ts"]].copy()
    si["ts"] = si.ts.astype("datetime64[ns]")
    j = pd.merge_asof(si.sort_values("ts"), ab[["account_id", "local", "postcode"]],
                      left_on="ts", right_on="local", by="account_id")
    pc = s.session_id.map(dict(zip(j.session_id, j.postcode))).fillna("")
    # the check rejects a saved postcode held as the four-digit area code only (CP4)
    s["addr"] = s.signed_in & s.flag_live & pc.str.fullmatch(r"\d{4}")
    return s


def attach_default_card(s):
    """Default saved card at the session: the snapshot is at extract, so roll back set_default events."""
    cards = pd.read_csv(one("saved_cards_", ".csv"))
    ev = pd.read_csv(one("saved_card_events", ".csv"))
    issuer = dict(zip(cards.card_id, cards.issuer))
    default_now = dict(zip(cards.account_id[cards.is_default], cards.card_id[cards.is_default]))
    sd = ev[ev.event == "set_default"]
    assert sd.account_id.is_unique
    switch = {a: (pd.Timestamp(t), prev) for a, t, prev in zip(sd.account_id, sd["at"], sd.previous_default_card_id)}
    out = []
    for a, t, si in zip(s.account_id, s.ts, s.signed_in):
        if not si:
            out.append(False)
            continue
        cid = switch[a][1] if a in switch and t < switch[a][0] else default_now[a]
        out.append(issuer[cid] in CHALLENGED_ISSUERS)
    s["card"] = out
    return s


def attach_mixed(s):
    """Pre-order or in-stock status of each SKU as it stood at the session."""
    cat = pd.read_csv(one("catalogue_status_history", ".csv"))
    cat["from"] = pd.to_datetime(cat.valid_from)
    hist = {k: g.sort_values("from")[["from", "status"]].values.tolist() for k, g in cat.groupby("sku")}

    def status(sku, t):
        st = None
        for f, x in hist[sku]:
            if f <= t:
                st = x
        return st
    s["mixed"] = [{status(k, t) for k in b.split(";")} >= {"pre_order", "in_stock"}
                  for b, t in zip(s.basket_skus, s.ts)]
    return s


def baselines(s):
    """Each cause's customers against what those same customers converted at in the four weeks before
    the fall (shortlist sizing line). Account-held causes: the accounts seen in the cause during the review
    weeks, read over their signed-in August sessions. New fans have no August of their own: the web
    new-visitor rate, the convention both partner close-outs book new visitors at. Mixed baskets: August
    mixed baskets."""
    before = s[s.wk.isin(BEFORE)]
    signed = before[before.signed_in]
    base = {}
    for f in ("F1", "F3", "F4"):
        col = "club_account" if f == "F4" else "account_id"
        who = set(s.loc[s.wk.isin(REVIEW) & s[POP[f]], col].dropna())
        rows = signed[signed.account_id.isin(who)]
        base[f] = {"accounts": len(who), "sessions": len(rows), "orders": int(rows.ordered.sum()), "orders_ids": rows.order_id}
    nv = before[~before.signed_in & ~before.club & before.new_visitor]
    base["F2"] = {"accounts": None, "sessions": len(nv), "orders": int(nv.ordered.sum()), "orders_ids": nv.order_id}
    mx = before[before.mixed]
    base["F5"] = {"accounts": None, "sessions": len(mx), "orders": int(mx.ordered.sum()), "orders_ids": mx.order_id}
    for f in base:
        base[f]["rate"] = base[f]["orders"] / base[f]["sessions"]
    store = before.ordered.mean()
    return base, store


def weekly_losses(s, base):
    lost, cells = {}, {}
    for f, *_ in FIXES:
        g = s[s[POP[f]]].groupby("wk").ordered.agg(["size", "sum"])
        lost[f], cells[f] = {}, {}
        for w in CHART_WEEKS:
            n, o = (int(g.loc[w, "size"]), int(g.loc[w, "sum"])) if w in g.index else (0, 0)
            lost[f][w] = n * base[f]["rate"] - o
            cells[f][w] = (n, o)
    return lost, cells


def order_values(base):
    """Net order value per order over August: latest export of each order, one row per order (rows are
    shipments), VAT taken out of rows exported before the 10 August finance release."""
    fin = pd.read_csv(one("finance_order_export", ".csv"))
    fin["exported"] = pd.to_datetime(fin.exported_at)
    fin = fin[fin.exported == fin.groupby("order_id").exported.transform("max")].drop_duplicates("order_id")
    net = np.where(fin.exported < FINANCE_NET_FROM, fin.order_total_eur / VAT, fin.order_total_eur)
    value = dict(zip(fin.order_id, net))
    out = {}
    for f in base:
        ids = base[f]["orders_ids"].dropna()
        v = ids.map(value)
        assert v.notna().all(), f
        out[f] = float(v.mean())
    return out


def challenge_shares(s):
    """Share of the call week's card payment attempts that met a 3-D Secure challenge. One attempt per
    attempt_ref (the 3DS server re-sends some challenges under the same ref); C and D both challenges."""
    log = pd.read_csv(one("tagus_3ds_log", ".csv")).drop_duplicates("attempt_ref")
    out = {}
    for f, *_ in FIXES:
        ids = set(s.session_id[(s.wk == CALL_WEEK) & s[POP[f]]])
        a = log[log.session_id.isin(ids)]
        out[f] = (len(a), int(a.three_ds_status.isin(CHALLENGE).sum()))
    return out, log


def cohort_tables(s, enabled):
    rev = s[s.wk.isin(REVIEW) & s.signed_in]
    assert (rev.cohort > 0).all()
    tot = rev.groupby("cohort").ordered.agg(["size", "sum"])
    wk = rev.groupby(["cohort", "wk"]).ordered.agg(["size", "sum"])
    return tot, wk


def r100(x):
    return int(math.floor(x / 100 + 0.5) * 100)


def whole(x):
    return int(math.floor(x + 0.5))


def analyse():
    s, n_raw = load_sessions()
    s = attach_club_accounts(s)
    s, enabled = attach_cohorts(s)
    s = attach_saved_address(s)
    s = attach_default_card(s)
    s = attach_mixed(s)
    base, store = baselines(s)
    lost, cells = weekly_losses(s, base)
    value = order_values(base)
    ch, log = challenge_shares(s)
    coh_tot, coh_wk = cohort_tables(s, enabled)
    w4 = {f: lost[f][CALL_WEEK] for f in lost}
    rank = sorted(w4, key=lambda f: -w4[f])
    call, runner = rank[0], rank[1]
    r = {
        "s": s, "n_raw": n_raw, "base": base, "store": store, "lost": lost, "cells": cells,
        "value": value, "ch": ch, "log": log, "enabled": enabled, "coh_tot": coh_tot, "coh_wk": coh_wk,
        "call": call, "runner": runner, "w4": w4,
        "L1": {f: sum(lost[f][w] for w in REVIEW) for f in lost},
        "L2": {f: lost[f]["W1"] for f in lost},
        "L3": {f: w4[f] * value[f] for f in lost},
        "L4": {f: 100.0 * ch[f][1] / ch[f][0] for f in lost},
    }
    r["gap"] = w4[call] - w4[runner]
    # control totals a reader will check
    assert whole(r["gap"]) == whole(w4[call]) - whole(w4[runner])
    for f in lost:
        assert whole(r["L1"][f]) == sum(whole(lost[f][w]) for w in REVIEW), f
    club_w4 = s[(s.wk == CALL_WEEK) & s.club]
    assert club_w4.acct.sum() + club_w4.newfan.sum() == len(club_w4)
    assert w4[call] >= 1.2 * w4[runner]
    return r


# ---------------------------------------------------------------- workbook
def write_workbook(r, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    HEAD = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    HFILL = PatternFill("solid", fgColor="1F3A5F")
    BODY = Font(name="Calibri", size=10)
    BOLD = Font(name="Calibri", size=10, bold=True)
    TITLE = Font(name="Calibri", size=12, bold=True)
    NOTE = Font(name="Calibri", size=9, italic=True, color="555555")
    TOP = Border(top=Side(style="thin", color="1F3A5F"))
    COUNT, PCT2, PCT1, EUR, EUR0 = "#,##0", '0.00"%"', '0.0"%"', '"€"#,##0.00', '"€"#,##0;-"€"#,##0'

    wb = Workbook()

    def sheet(title, heading, sub, header, widths, first=False):
        ws = wb.active if first else wb.create_sheet()
        ws.title = title
        ws["A1"], ws["A2"] = heading, sub
        ws["A1"].font, ws["A2"].font = TITLE, NOTE
        for j, (h, w) in enumerate(zip(header, widths), 1):
            c = ws.cell(row=4, column=j, value=h)
            c.font, c.fill = HEAD, HFILL
            c.alignment = Alignment(horizontal="left" if j == 1 else "right", vertical="center", wrap_text=True)
            ws.column_dimensions[get_column_letter(j)].width = w
        ws.row_dimensions[4].height = 30
        ws.freeze_panes = "B5"
        ws.print_title_rows = "4:4"
        ws.page_setup.orientation = "landscape"
        ws.page_setup.fitToWidth = 1
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        return ws

    def put(ws, row, values, fmts, font=BODY, border=None):
        for j, (v, f) in enumerate(zip(values, fmts), 1):
            c = ws.cell(row=row, column=j, value=v)
            c.font = font
            if f:
                c.number_format = f
            c.alignment = Alignment(horizontal="left" if isinstance(v, str) else "right")
            if border:
                c.border = border

    # 1. the cohort view Duarte's squad asked for
    ws = sheet("Address check cohorts",
               "Address check (checkout.address.full_postcode): flag cohorts, 31 Aug to 27 Sep 2026",
               "Signed-in basket sessions by the cohort the account was in at the session (the 14 and 16 Sep "
               "assignment moves applied as of the session); edge-flagged sessions excluded. Conversion = orders / basket sessions.",
               ["Cohort", "Flag live from", "Basket sessions", "Orders", "Conversion"],
               [10, 18, 16, 10, 13], first=True)
    row = 5
    for k, x in r["coh_tot"].iterrows():
        put(ws, row, [int(k), r["enabled"][int(k)].to_pydatetime(), int(x["size"]), int(x["sum"]),
                      round(100 * x["sum"] / x["size"], 2)],
            [None, "ddd d mmm hh:mm", COUNT, COUNT, PCT2])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="left")
        row += 1
    n, o = int(r["coh_tot"]["size"].sum()), int(r["coh_tot"]["sum"].sum())
    put(ws, row, ["All cohorts", None, n, o, round(100 * o / n, 2)], [None, None, COUNT, COUNT, PCT2], BOLD, TOP)
    ws.cell(row=row + 2, column=1, value="Cohort sessions include the days before a cohort went live. Club-app "
            "sessions are signed out, so the flag does not apply to them and they are not in any cohort.").font = NOTE

    # 2. the same by week, for testing cells
    ws = sheet("Cohorts by week", "Address check cohorts by week", "Same population as 'Address check cohorts'. "
               "Week = Monday to Sunday, Lisbon time.",
               ["Cohort", "Week starting", "Basket sessions", "Orders", "Conversion"], [10, 14, 16, 10, 13])
    row = 5
    for (k, w), x in r["coh_wk"].iterrows():
        put(ws, row, [int(k), pd.Timestamp(WEEK_START[w]).to_pydatetime(), int(x["size"]), int(x["sum"]),
                      round(100 * x["sum"] / x["size"], 2)], [None, "d mmm yyyy", COUNT, COUNT, PCT2])
        ws.cell(row=row, column=1).alignment = Alignment(horizontal="left")
        row += 1
    ws.auto_filter.ref = f"A4:E{row - 1}"

    # 3. lost orders by cause and week (the chart's data)
    hdr = ["Fix", "Customers it is for"] + [pd.Timestamp(WEEK_START[w]).strftime("%-d %b") for w in CHART_WEEKS] \
        + ["31 Aug to 27 Sep"]
    ws = sheet("Lost orders by week", "Orders lost each week, by cause",
               "Each cause's customers against their own conversion over 3 to 30 August (orders lost = basket "
               "sessions x August conversion - orders). Negative = orders gained. Columns are week-starting dates.",
               hdr, [24, 46] + [8] * 8 + [16])
    ws.freeze_panes = "C5"
    row = 5
    for f, name, _, _, cause in FIXES:
        vals = [whole(r["lost"][f][w]) for w in CHART_WEEKS]
        put(ws, row, [name, cause] + vals + [whole(r["L1"][f])], [None, None] + [COUNT] * 9,
            BOLD if f == r["call"] else BODY)
        row += 1
    ws.cell(row=row + 1, column=1, value="August cells are the baseline weeks themselves, so they sit at or near "
            "zero. Club-app causes start on 31 Aug, the day the Shop tab went live.").font = NOTE

    # 4. the call week, sized the way the shortlist says
    ws = sheet("Call week sizing", "Week of 21 to 27 September: lost orders and sales by cause",
               "Sizing line from the Q4 sprint shortlist: latest complete week, each cause's customers against "
               "the same customers' conversion over the four weeks before the fall, a lost order valued at their "
               "August average net order value.",
               ["Fix", "Aug basket sessions", "Aug orders", "Aug conversion", "Basket sessions 21-27 Sep",
                "Orders 21-27 Sep", "Expected orders", "Orders lost", "Avg net order value, Aug",
                "Sales lost (nearest €100)"], [24, 13, 10, 12, 14, 12, 12, 11, 15, 15])
    row = 5
    for f, name, *_ in FIXES:
        b = r["base"][f]
        n, o = r["cells"][f][CALL_WEEK]
        put(ws, row, [name, b["sessions"], b["orders"], round(100 * b["rate"], 2), n, o,
                      whole(n * b["rate"]), whole(r["w4"][f]), round(r["value"][f], 2), r100(r["L3"][f])],
            [None, COUNT, COUNT, PCT2, COUNT, COUNT, COUNT, COUNT, EUR, EUR0], BOLD if f == r["call"] else BODY)
        row += 1
    ws.cell(row=row + 1, column=1, value="Card SDK, postcode lookup and sign-in rows use the accounts seen in the "
            "cause between 31 Aug and 27 Sep, read over their signed-in August sessions; club-app accounts are "
            "matched through the club token report to the member number, then to the account holding it on the "
            "loyalty profile or in last season's SOCIO code redemptions.").font = NOTE
    ws.cell(row=row + 2, column=1, value="Club landing page uses the August web new-visitor conversion, as both "
            "partner close-outs book new visitors. Split dispatch uses August mixed baskets.").font = NOTE

    # 5. 3-D Secure challenges in the call week
    ws = sheet("Challenges 21-27 Sep", "Card payment attempts that met a 3-D Secure challenge, 21 to 27 September",
               "Tagus 3DS log, one attempt per attempt_ref (re-sent challenge messages share the ref). "
               "Challenged = status C or D (D is a decoupled challenge approved in the issuer's banking app, per the Tagus report).",
               ["Fix", "Card payment attempts", "Challenged", "Share challenged"], [24, 16, 12, 14])
    row = 5
    for f, name, *_ in FIXES:
        a, c = r["ch"][f]
        put(ws, row, [name, a, c, round(r["L4"][f], 1)], [None, COUNT, COUNT, PCT1])
        row += 1

    # 6. notes
    ws = wb.create_sheet("Notes")
    lines = [
        ("Checkout conversion review INC-0914: workings behind q4_sprint_call.html", TITLE),
        ("Prepared for the review on Friday 2 October 2026. Extracts as cut on 28 to 29 September 2026.", BODY),
        ("", BODY),
        ("Sources", BOLD),
        ("basket_sessions export (3 Aug to 27 Sep); edge_bot_verdicts; cdm_token_billing 2026-08 and 2026-09; "
         "loyalty_profiles; promo_redemptions (2025/26); checkout_flags_export; address_book_history; saved_cards and saved_card_events; "
         "catalogue_status_history; finance_order_export; tagus_3ds_log.", BODY),
        ("", BODY),
        ("Conventions", BOLD),
        ("Conversion is orders over basket sessions. Edge-flagged sessions are out of sessions and orders.", BODY),
        ("Weeks run Monday to Sunday, Lisbon time. Address book times are UTC and are moved to Lisbon (UTC+1) "
         "before they are compared with sessions.", BODY),
        ("Flag cohort, default saved card and pre-order status are each taken as they stood at the session.", BODY),
        ("Order values: latest export of each order, one value per order (rows are shipments), net of VAT "
         "(rows exported before 10 Aug divided by 1.23).", BODY),
        ("Counts are whole numbers, lost orders included; sales lost to the nearest €100; the challenge share "
         "to one decimal and conversion to two, both as percentages.", BODY),
        ("Causes overlap (a mixed basket on a Bankora account counts in both), so the rows do not add to the "
         "store's fall.", BODY),
    ]
    for i, (t, ft) in enumerate(lines, 1):
        c = ws.cell(row=i, column=1, value=t)
        c.font = ft
        c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 120
    wb.properties.creator = "Ventania Merch product analytics"
    wb.properties.title = "Checkout fall workings"
    wb.properties.created = wb.properties.modified = PREPARED
    wb.save(path)


# ---------------------------------------------------------------- chart (inline SVG, drawn here)
SERIES = ["F4", "F3", "F1", "F2", "F5"]          # fixed slot order: the call takes slot 1
SLOT = {f: i + 1 for i, f in enumerate(SERIES)}


def week_label(w):
    return pd.Timestamp(WEEK_START[w]).strftime("%-d %b")


def chart_svg(r, title):
    W, H = 800, 380
    L, R, T, B = 52, 196, 30, 46
    pw, ph = W - L - R, H - T - B
    lo, hi = -10, 60
    xs = {w: L + pw * i / (len(CHART_WEEKS) - 1) for i, w in enumerate(CHART_WEEKS)}
    y = lambda v: T + ph * (hi - v) / (hi - lo)
    step = pw / (len(CHART_WEEKS) - 1)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="chart-title" class="chart">',
           f'<title id="chart-title">{html.escape(title)}</title>']
    cx = xs[CALL_WEEK]
    out.append(f'<rect class="band" x="{cx - step / 2:.1f}" y="{T}" width="{step / 2 + 8:.1f}" height="{ph}"/>')
    out.append(f'<text class="band-label" x="{cx - step / 2 + 6:.1f}" y="{T - 10}">Week the call rests on</text>')
    for v in range(lo, hi + 1, 10):
        cls = "zero" if v == 0 else "grid"
        out.append(f'<line class="{cls}" x1="{L}" x2="{L + pw}" y1="{y(v):.1f}" y2="{y(v):.1f}"/>')
        out.append(f'<text class="tick" x="{L - 8}" y="{y(v) + 4:.1f}" text-anchor="end">{v}</text>')
    for w in CHART_WEEKS:
        out.append(f'<text class="tick" x="{xs[w]:.1f}" y="{T + ph + 18}" text-anchor="middle">{week_label(w)}</text>')
    out.append(f'<text class="axis" x="{L + pw / 2:.1f}" y="{H - 6}" text-anchor="middle">Week starting (Monday), 2026</text>')
    out.append(f'<text class="axis" transform="translate(14,{T + ph / 2:.0f}) rotate(-90)" text-anchor="middle">'
               'Orders lost per week</text>')
    x0 = xs["W1"] - step / 2
    out.append(f'<line class="start" x1="{x0:.1f}" x2="{x0:.1f}" y1="{T}" y2="{T + ph}"/>')
    out.append(f'<text class="tick" x="{x0 - 6:.1f}" y="{T + 12}" text-anchor="end">Shop tab live, address check on</text>')
    for f in reversed(SERIES):
        pts = " ".join(f"{xs[w]:.1f},{y(r['lost'][f][w]):.1f}" for w in CHART_WEEKS)
        cls = f"s{SLOT[f]}" + (" lead" if f == r["call"] else "")
        out.append(f'<polyline class="line {cls}" points="{pts}"/>')
        for w in CHART_WEEKS:
            v = r["lost"][f][w]
            out.append(f'<circle class="dot {cls}" cx="{xs[w]:.1f}" cy="{y(v):.1f}" r="4">'
                       f'<title>{FIX_NAME[f]}, week of {week_label(w)}: {whole(v)} orders lost</title></circle>')
    f = r["call"]
    ly = y(r["lost"][f][CALL_WEEK])
    out.append(f'<text class="direct" x="{cx + 10:.1f}" y="{ly - 4:.1f}">{FIX_NAME[f]}</text>')
    out.append(f'<text class="direct sub" x="{cx + 10:.1f}" y="{ly + 12:.1f}">{whole(r["w4"][f])} orders lost, chosen fix</text>')
    g = r["runner"]
    out.append(f'<text class="direct sub" x="{cx + 10:.1f}" y="{y(r["lost"][g][CALL_WEEK]) + 4:.1f}">'
               f'{FIX_NAME[g]}: {whole(r["w4"][g])}</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------------------------------------------------------------- the review page
CSS = """
:root{color-scheme:light;--surface:#fcfcfb;--panel:#f3f2ee;--ink:#0b0b0b;--ink-2:#52514e;--ink-3:#7a7974;
--rule:#dcdad3;--grid:#e8e6e0;--band:#eef3fb;--accent:#1f3a5f;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--s5:#e87ba4}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){color-scheme:dark;--surface:#1a1a19;
--panel:#24241f;--ink:#ffffff;--ink-2:#c3c2b7;--ink-3:#97968d;--rule:#3a3a35;--grid:#2e2e2a;--band:#1f2a38;
--accent:#9fb8d8;--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181}}
:root[data-theme="dark"]{color-scheme:dark;--surface:#1a1a19;--panel:#24241f;--ink:#ffffff;--ink-2:#c3c2b7;
--ink-3:#97968d;--rule:#3a3a35;--grid:#2e2e2a;--band:#1f2a38;--accent:#9fb8d8;--s1:#3987e5;--s2:#d95926;
--s3:#199e70;--s4:#c98500;--s5:#d55181}
*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--ink);font:15px/1.55 "Segoe UI",Helvetica,Arial,sans-serif}
main{max-width:980px;margin:0 auto;padding:20px 16px 48px}
.strip{font-size:12px;color:var(--ink-2);border-bottom:2px solid var(--accent);padding-bottom:6px;
display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 16px}
h1{font-size:26px;line-height:1.25;margin:18px 0 10px}
h2{font-size:17px;margin:30px 0 8px}
p{margin:0 0 12px;max-width:72ch}
.call{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1px;background:var(--rule);
border:1px solid var(--rule);margin:16px 0 20px}
.call div{background:var(--panel);padding:10px 12px}
.call .k{font-size:12px;color:var(--ink-2)}
.call .v{font-size:20px;font-weight:600;font-variant-numeric:tabular-nums}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}
th,td{padding:7px 9px;border-bottom:1px solid var(--rule);vertical-align:top}
th{font-size:12px;color:var(--ink-2);font-weight:600;text-align:right}
th:first-child,th:nth-child(2),td:first-child,td:nth-child(2){text-align:left}
td{text-align:right}
tr.chosen td{background:var(--panel);font-weight:600}
td .who{display:block;font-size:12px;color:var(--ink-2);font-weight:400}
.src{font-size:12px;color:var(--ink-3);margin-top:6px}
ol.notes{font-size:12px;color:var(--ink-2);padding-left:18px;margin:8px 0 0}
figure{margin:12px 0 0}
figure h3{font-size:15px;margin:0 0 8px}
.legend{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:13px;color:var(--ink-2);margin-bottom:4px}
.legend span::before{content:"";display:inline-block;width:16px;height:3px;border-radius:2px;margin:0 6px 4px 0;
background:var(--c)}
svg.chart{width:100%;height:auto;display:block}
.chart .grid{stroke:var(--grid);stroke-width:1}.chart .zero{stroke:var(--ink-3);stroke-width:1}
.chart .start{stroke:var(--ink-3);stroke-width:1;stroke-dasharray:3 3}
.chart .band{fill:var(--band)}.chart .tick{fill:var(--ink-3);font-size:11px}
.chart .axis{fill:var(--ink-2);font-size:12px}.chart .band-label{fill:var(--ink-2);font-size:11px}
.chart .line{fill:none;stroke-width:2;stroke-linejoin:round}.chart .line.lead{stroke-width:3}
.chart .dot{stroke:var(--surface);stroke-width:2}
.chart .direct{fill:var(--ink);font-size:12px;font-weight:600}.chart .direct.sub{fill:var(--ink-2);font-weight:400}
.s1{stroke:var(--s1)}.dot.s1{fill:var(--s1)}.s2{stroke:var(--s2)}.dot.s2{fill:var(--s2)}
.s3{stroke:var(--s3)}.dot.s3{fill:var(--s3)}.s4{stroke:var(--s4)}.dot.s4{fill:var(--s4)}
.s5{stroke:var(--s5)}.dot.s5{fill:var(--s5)}
details{margin-top:10px;font-size:13px}summary{cursor:pointer;color:var(--ink-2)}
footer{margin-top:34px;padding-top:10px;border-top:1px solid var(--rule);font-size:12px;color:var(--ink-3)}
@media (max-width:560px){h1{font-size:22px}.call .v{font-size:18px}}
"""


def eur(x):
    v = r100(x)
    return ("-" if v < 0 else "") + f"€{abs(v):,}"


def backtest_statements(r):
    """Every rule the page and the workbook state, run back over the whole record."""
    s = r["s"]
    club = s[s.club]
    assert not club.signed_in.any() and club.account_id.isna().all() and club.new_visitor.all()
    for w in REVIEW:                                   # "most Shop-tab basket sessions belong to existing accounts"
        assert s.acct[(s.wk == w) & s.club].mean() > 0.5, w
    assert (s.mixed & s.card).any()                    # causes overlap
    ab = pd.read_csv(one("address_book_history", ".csv"), dtype={"postcode": str})
    ab = ab[ab.is_default & ~ab.postcode.str.fullmatch(r"\d{4}")].copy()
    ab["local"] = pd.to_datetime(ab.changed_at) + pd.Timedelta(hours=1)
    p1 = s[s.addr]
    first = p1.groupby("account_id").ts.min()
    resave = ab[ab.account_id.isin(first.index)]
    resave = resave[resave.local > resave.account_id.map(first)].groupby("account_id").local.min()
    assert not (p1.ts > p1.account_id.map(resave)).any()   # after a full-postcode re-save the account passes
    b = s[s.wk.isin(BEFORE)]
    half = b[b.mixed].ordered.mean() / b[~b.mixed].ordered.mean()
    assert 0.4 < half < 0.6                            # mixed baskets at about half the rest, in August too
    flags = json.loads(one("checkout_flags_export", ".json").read_text())
    moves = {m["moved_at"][:10] for m in flags["assignment_moves"]}
    assert moves == {"2026-09-14", "2026-09-16"}, moves   # "the 14 and 16 Sep assignment moves"


def write_page(r, path):
    c, g = r["call"], r["runner"]
    w4, L1, L2, L3, L4 = r["w4"], r["L1"], r["L2"], r["L3"], r["L4"]
    n4, o4 = r["cells"][c][CALL_WEEK]
    # statements the prose makes, checked against the numbers
    assert o4 / n4 < r["base"][c]["rate"] / 3
    assert w4["F1"] < L2["F1"] / 3 and w4["F2"] < 3 and w4["F5"] < 0
    backtest_statements(r)
    cw = r["s"][(r["s"].wk == CALL_WEEK) & r["s"].club]
    share_prof, share_both = 100 * cw.acct_profile_only.mean(), 100 * cw.acct.mean()
    title = (f"Q4 sprint to {lc(FIX_NAME[c])}: account holders arriving from the club app signed out cost "
             f"{whole(w4[c])} orders in the week of 21 September, {whole(r['gap'])} more than the next cause")
    e = html.escape
    rows = []
    for f, name, owner, _, cause in FIXES:
        rows.append(
            f'<tr{" class=chosen" if f == c else ""}><td>{e(name)}<span class="who">{e(owner)}</span></td>'
            f'<td>{e(cause)}</td><td>{whole(L1[f])}</td><td>{whole(L2[f])}</td><td>{eur(L3[f])}</td>'
            f'<td>{L4[f]:.1f}%</td></tr>')
    wk_rows = "".join(
        f"<tr><td>{week_label(w)}</td>" + "".join(f"<td>{whole(r['lost'][f][w])}</td>" for f in SERIES) + "</tr>"
        for w in CHART_WEEKS)
    legend = "".join(f'<span style="--c:var(--s{SLOT[f]})">{e(FIX_NAME[f])}</span>' for f in SERIES)
    page = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Q4 sprint call</title>
<style>{CSS}</style>
</head>
<body>
<main>
<div class="strip"><span>Ventania Merch · Product · INC-0914 checkout conversion review</span>
<span>For the review on Friday 2 October 2026 · Júlia Machado, head of product</span></div>

<h1>The Q4 sprint goes to {e(lc(FIX_NAME[c]))} at checkout</h1>

<p>Both checkout squads go on {e(lc(FIX_NAME[c]))} for the sprint (12 October to 6 November). The cause it
removes is customers who already hold a Ventania account arriving from the Shop tab in the Monteralto+ app without
being signed in. Checkout has none of their saved address, saved card or card-on-file exemption, so they type a
postcode the new check can reject and pay with a card that gets challenged, and many give up. In the week of 21 to
27 September they converted at under a third of what the same accounts converted at in August, and that cost
<strong>{whole(w4[c])} orders</strong>. A code by text or email at the contact step signs them in inside the app
without a password, which is the only fix on the list that reaches them.</p>

<p>The closest fix is the {e(lc(FIX_NAME[g]))}: saved-card payments that Bankora and Finvo began challenging
in September cost {whole(w4[g])} orders the same week. That loss is real and stays on the Q1 list, but it is
{whole(r['gap'])} orders a week smaller.</p>

<div class="call">
<div><div class="k">Sprint goes to</div><div class="v">{e(FIX_NAME[c])}</div></div>
<div><div class="k">Orders lost, 21 to 27 Sep</div><div class="v">{whole(w4[c])}</div></div>
<div><div class="k">Next closest</div><div class="v">{e(FIX_NAME[g])}, {whole(w4[g])}</div></div>
<div><div class="k">Gap</div><div class="v">{whole(r['gap'])} orders a week</div></div>
</div>

<h2>How the club-app sessions were matched to accounts</h2>
<p>The session export files every Shop-tab session as a new visitor with no account, which is right as far as the
store can see: nobody signed in. Each Shop-tab link carries the members'-price token (<code>mpt</code>). The
club's token reports for August and September give the member number each token was issued to. A member number
reaches an account two ways: on the loyalty profile, where some members have typed it, and in last season's
members' discount, the SOCIO code with the member number that members entered at checkout on their own account.
The profile alone places {share_prof:.0f}% of the week's Shop-tab sessions on an account; with the codes it is
{share_both:.0f}%, and those accounts converted at
{100 * r['base'][c]['rate']:.2f}% in August when they shopped signed in. The rest are genuine new fans, and they
convert like any web new visitor.</p>

<h2>Why not the other three</h2>
<p><strong>{e(FIX_NAME['F1'])}.</strong> Duarte is right that the address check hurt: it cost {whole(L2['F1'])}
orders in its first week. But once a customer re-saves their address with the full postcode the account passes
from then on, and as accounts re-saved the loss drained: by 21 to 27 September it was down to {whole(w4['F1'])}. The cohort sheet in the workings
lets the squad test this cohort by cohort.</p>
<p><strong>{e(FIX_NAME['F2'])}.</strong> Fans who are new to the store are booked against the rate web new
visitors converted at in August ({100 * r['base']['F2']['rate']:.2f}%), the way both partner close-outs book new
visitors. Booked that way they cost {whole(w4['F2'])} orders that week. Luciana's dilution reading is right for them; it is not right for account holders who came in
signed out.</p>
<p><strong>{e(FIX_NAME['F5'])}.</strong> Mixed pre-order baskets do convert at about half the rate of the rest,
but they did in August too. Against their own August they gained about one order that week.</p>

<h2>Five fixes against the evidence</h2>
<div class="scroll"><table>
<thead><tr><th>Fix</th><th>Customers it is for</th><th>Orders lost, 31 Aug to 27 Sep<sup>1</sup></th>
<th>Orders lost, week of 31 Aug</th><th>Sales lost, week of 21 Sep<sup>2</sup></th>
<th>Card attempts challenged, week of 21 Sep<sup>3</sup></th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table></div>
<ol class="notes">
<li>Each cause's customers against their own conversion over 3 to 30 August, the shortlist's sizing basis. Edge-flagged
automated sessions are excluded throughout. Causes overlap, so the rows do not add to the store's fall.</li>
<li>Lost orders valued at the same customers' average net order value in August (latest finance export, one
value per order, VAT out). Nearest €100; negative means sales gained.</li>
<li>Share of card payment attempts (one per <code>attempt_ref</code>) that met a challenge, status C or D in the
Tagus 3DS log. The sign-in row is challenged because those customers pay without their saved card's exemption.</li>
</ol>

<h2>Orders lost each week since August</h2>
<figure>
<h3>{e(title)}</h3>
<div class="legend">{legend}</div>
{chart_svg(r, title)}
<details><summary>Weekly figures behind the chart</summary>
<div class="scroll"><table><thead><tr><th>Week starting</th>{''.join(f'<th>{e(FIX_NAME[f])}</th>' for f in SERIES)}</tr></thead>
<tbody>{wk_rows}</tbody></table></div></details>
</figure>
<p class="src">Source: basket session export, edge verdicts, club token reports, loyalty profiles, 2025/26 code
redemptions, flag export,
address book, saved cards, catalogue status, finance order export and Tagus 3DS log, as cut 28 to 29 September.
Workings: checkout_fall_workings.xlsx.</p>

<footer>Internal. Product team and incident review only.</footer>
</main>
</body>
</html>
"""
    path.write_text(page, encoding="utf-8")
    return title


def repack(path):
    """Same entries in the same order, each stamped with the preparation time, so a rerun is byte-identical."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            info = zipfile.ZipInfo(name, date_time=PREPARED.timetuple()[:6])
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    r = analyse()
    write_workbook(r, OUT / "checkout_fall_workings.xlsx")
    title = write_page(r, OUT / "q4_sprint_call.html")
    # the workbook library stamps its own name into docProps; replace it with the store's
    subprocess.run([sys.executable, str(SCRUB), str(OUT), "--apply", "--producer", "Ventania Merch",
                    "--stamp", PREPARED.strftime("%Y-%m-%d")], capture_output=True, text=True)
    audit = subprocess.run([sys.executable, str(SCRUB), str(OUT)], capture_output=True, text=True)
    assert "flagged" not in audit.stdout or "0 file(s) flagged" in audit.stdout, audit.stdout
    repack(OUT / "checkout_fall_workings.xlsx")
    for f in ("q4_sprint_call.html", "checkout_fall_workings.xlsx"):
        os.utime(OUT / f, (PREPARED.timestamp(), PREPARED.timestamp()))
    c, g = r["call"], r["runner"]
    print(f"Basket sessions read: {r['n_raw']:,}; after edge exclusion: {len(r['s']):,}")
    print(f"Call: {FIX_NAME[c]} ({c}); cause: {CAUSE[c]}")
    print(f"  orders lost 21-27 Sep: {whole(r['w4'][c])}  (unrounded {r['w4'][c]:.3f})")
    print(f"Runner-up: {FIX_NAME[g]} ({g}), {whole(r['w4'][g])} orders  (unrounded {r['w4'][g]:.3f})")
    print(f"Gap: {whole(r['gap'])} orders a week  (unrounded {r['gap']:.3f})")
    print(f"{'Fix':<24}{'L1 4 wks':>9}{'L2 W1':>7}{'L3 EUR':>9}{'L4 chall':>10}")
    for f, name, *_ in FIXES:
        print(f"{name:<24}{whole(r['L1'][f]):>9}{whole(r['L2'][f]):>7}{r100(r['L3'][f]):>9,}{r['L4'][f]:>9.1f}%")
    print("Cohorts (basket sessions, conversion %):",
          "; ".join(f"{int(k)}: {int(x['size']):,}, {100 * x['sum'] / x['size']:.2f}" for k, x in r["coh_tot"].iterrows()))
    print("Chart title:", title)


if __name__ == "__main__":
    main()
