"""Writers for the data files of the pack: the portal export, the grants register, the register
match, Ledgerwood's six packs, the payment run and the two neighbouring files."""
import csv
import datetime as dt
import io

import numpy as np
import openpyxl
from openpyxl.styles import Font, Alignment

from common import (MARCH_CENSUSES, POTS, qend, fyq, fy_q4, pct1, SEED)
from lines import (OLD_CODES, NEW_CODES, OLD_SHORT, NEW_SHORT, is_new_form)
from roster import Q
from world import rng_for

SPINE = "portal_return_lines_2018q3_2026q2.csv"
GRANTS = "grants_register_20261007.xlsx"
REGISTER = "charities_register_returns_extract_20261007.csv"
PAYRUN = "trust_payment_run_2018-07_to_2026-09.csv"
SURVEY = "canterbury_community_income_survey_2025.xlsx"
RATINGS = "grantee_capacity_ratings_2026.csv"


def pack_name(y):
    return f"SGF_screen_run_{y}-03.xlsx"


def write_csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def ts(d):
    return "" if d is None else d.strftime("%Y-%m-%d %H:%M")


def form_code(q, short):
    if is_new_form(q):
        return "QFR-24S" if short else "QFR-24"
    return "QFR-16S" if short else "QFR-16"


def line_order(q, short):
    if is_new_form(q):
        return NEW_SHORT if short else NEW_CODES
    return OLD_SHORT if short else OLD_CODES


def portal_rows(W):
    """Every row of the portal export, in file order, with design tags kept beside (never written)."""
    by = W["by"]
    keys = sorted({(v.ref, v.q) for v in W["versions"]}, key=lambda k: (k[1], k[0]))
    r = np.random.default_rng([SEED, 31])
    rid, nxt = {}, 1_104_212
    for k in keys:
        nxt += int(r.integers(1, 6))
        rid[k] = f"QR{nxt}"
    out = []
    vs = sorted(W["versions"], key=lambda v: (rid[(v.ref, v.q)], v.no))
    for v in vs:
        o = by[v.org]
        fye = qend(fy_q4(v.q, o.bal))
        for code in line_order(v.q, o.short_form):
            ytd, py = v.lines[code]
            for col, amt in (("YTD", ytd), ("PY", py)):
                out.append({"return_id": rid[(v.ref, v.q)], "grant_ref": v.ref,
                            "period_end": qend(v.q).isoformat(), "year_end": fye.isoformat(),
                            "form": form_code(v.q, o.short_form), "version_no": v.no,
                            "version_status": v.status, "submitted_at": ts(v.submitted),
                            "accepted_at": ts(v.accepted), "line_code": code, "column": col,
                            "amount": int(amt),
                            # tags for the generator's own checks
                            "is_pg": v.ref == o.pg_ref, "short": o.short_form, "status": v.status,
                            "org": v.org, "q": v.q})
    return out


SPINE_COLS = ["return_id", "grant_ref", "period_end", "year_end", "form", "version_no",
              "version_status", "submitted_at", "accepted_at", "line_code", "column", "amount"]


def write_spine(path, rows):
    write_csv(path, SPINE_COLS, ([r[c] for c in SPINE_COLS] for r in rows))
    return len(rows)


# ----------------------------------------------------------------------------- grants register

BAL_LABEL = {3: "31 March", 6: "30 June", 12: "31 December"}


def nz_date(d):
    return d


def write_grants_register(path, W):
    by = W["by"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Grants"
    hdr = ["grant_ref", "programme", "charity_no", "organisation", "sector", "district",
           "balance_date", "start_date", "end_date", "annual_amount", "status"]
    ws.append(hdr)
    rows = []
    for o in W["orgs"]:
        terms = W["terms"][o.key]
        cur = [t for t in terms if t[0] <= dt.date(2026, 10, 7)][-1]
        status = "Ended" if o.role == "exit" else "Active"
        rows.append([o.og_ref, "Operating grant", o.cc, o.name, o.sector, o.district,
                     BAL_LABEL[o.bal], o.og_start, o.og_end, cur[2], status])
        if o.dual:
            pt = [t for t in W["pg_level"][o.key] if t[0] <= dt.date(2026, 10, 7)][-1]
            rows.append([o.pg_ref, "Project grant", o.cc, o.name, o.sector, o.district,
                         BAL_LABEL[o.bal], o.pg_start, o.pg_end, pt[2], "Active"])
    rows.sort(key=lambda r: r[0])
    for r in rows:
        ws.append(r)
    for row in ws.iter_rows(min_row=2, min_col=8, max_col=9):
        for cell in row:
            cell.number_format = "yyyy-mm-dd"
    for row in ws.iter_rows(min_row=2, min_col=10, max_col=10):
        for cell in row:
            cell.number_format = "#,##0"
    widths = [18, 16, 11, 44, 24, 16, 13, 12, 12, 14, 8]
    for i, wdt in enumerate(widths):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wdt
    ws.freeze_panes = "A2"
    # variations: every renewal at a new annual amount
    wv = wb.create_sheet("Variations")
    wv.append(["grant_ref", "effective_date", "variation", "annual_amount_before",
               "annual_amount_after", "approved_by"])
    vrows = []
    for o in W["orgs"]:
        terms = W["terms"][o.key]
        for a, b in zip(terms, terms[1:]):
            if b[0] > dt.date(2026, 10, 7):
                continue
            vrows.append([o.og_ref, b[0], "Renewal", a[2], b[2], "Grants committee"])
        if o.dual:
            pt = W["pg_level"][o.key]
            for a, b in zip(pt, pt[1:]):
                if b[0] > dt.date(2026, 10, 7):
                    continue
                vrows.append([o.pg_ref, b[0], "Renewal", a[2], b[2], "Grants committee"])
    vrows.sort(key=lambda r: (r[1], r[0]))
    for r in vrows:
        wv.append(r)
    for row in wv.iter_rows(min_row=2, min_col=2, max_col=2):
        for cell in row:
            cell.number_format = "yyyy-mm-dd"
    for col, wdt in zip("ABCDEF", [18, 14, 12, 20, 20, 18]):
        wv.column_dimensions[col].width = wdt
    # Steady Ground offers
    wo = wb.create_sheet("Steady Ground offers")
    wo.append(["offer_ref", "round", "charity_no", "organisation", "offer_amount",
               "first_instalment_for", "instalments"])
    orows = []
    for (ry, key), ref in sorted(W["sgf_refs"].items()):
        o = by[key]
        orows.append([ref, f"March {ry}", o.cc, o.name, W["offers_by_round"][ry][key],
                      f"{ry}-06", 12])
    orows.sort(key=lambda r: r[0])
    for r in orows:
        wo.append(r)
    for col, wdt in zip("ABCDEFG", [14, 12, 11, 44, 13, 20, 11]):
        wo.column_dimensions[col].width = wdt
    wb.save(path)
    return len(rows)


# ----------------------------------------------------------------------------- register match

REG_COLS = ["match_id", "charity_no", "registered_name", "year_end", "date_received",
            "return_tier", "total_gross_income", "govt_grants_contracts", "donations_bequests",
            "trading_sales", "grants_other", "investment_income", "other_income"]


def register_name(o, r):
    n = o.name
    if n.endswith(" Society") and r.random() < 0.6:
        return n + " Incorporated"
    if n.endswith(" Trust") and r.random() < 0.25:
        return n + " Board"
    if r.random() < 0.08:
        return n.upper()
    return n


def write_register(path, W):
    by = W["by"]
    rows = []
    for (key, q4), ar in sorted(W["annual"].items(), key=lambda kv: (by[kv[0][0]].cc, kv[0][1])):
        if ar.received is None or ar.received > dt.date(2026, 10, 7):
            continue
        o = by[key]
        r = rng_for("reg", key, q4)
        cc = o.cc
        roll = r.random()
        if roll < 0.04:
            cc = cc.lower()
        elif roll < 0.07:
            cc = " " + cc
        elif roll < 0.09:
            cc = cc + " "
        tier = "Tier 3" if ar.total < 5_000_000 else "Tier 2"
        if ar.total < 140_000:
            tier = "Tier 4"
        L = ar.lines
        rows.append([None, cc, register_name(o, r), qend(q4).isoformat(), ar.received.isoformat(),
                     tier, ar.total, L["gov"], L["donations"], L["trading"], L["grants_other"],
                     L["investment"], L["other"]])
    rows.sort(key=lambda x: (x[4], x[1].strip().upper()))
    mid = 88_100
    rr = np.random.default_rng([SEED, 33])
    for x in rows:
        mid += int(rr.integers(1, 9))
        x[0] = f"CRM-{mid}"
    write_csv(path, REG_COLS, rows)
    return len(rows)


# ----------------------------------------------------------------------------- Ledgerwood packs

def write_pack(path, W, c):
    s = W["corpus"][c]
    by = W["by"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Screen"
    ws.append([f"Steady Ground Fund screen, census {c.day} March {c.year}"])
    ws.append([f"Prepared for the Ashworth Pascoe Trust by Ledgerwood Analytics"])
    ws.append([])
    hdr = ["Charity no.", "Organisation", "Twelve-month income", "Twelve months before",
           "Fall ($)", "Fall (%)", "Offer ($)"]
    ws.append(hdr)
    for cell in ws[4]:
        cell.font = Font(bold=True)
    ws["A1"].font = Font(bold=True, size=12)
    for r in s["rows"]:
        o = by[r["org"]]
        ws.append([o.cc, o.name, r["cur"], r["prior"], r["fall"], pct1(r["pct"]),
                   r["offer"] if r["offer"] else None])
    for row in ws.iter_rows(min_row=5, min_col=3, max_col=5):
        for cell in row:
            cell.number_format = "#,##0;-#,##0"
    for row in ws.iter_rows(min_row=5, min_col=6, max_col=6):
        for cell in row:
            cell.number_format = "0.0"
    for row in ws.iter_rows(min_row=5, min_col=7, max_col=7):
        for cell in row:
            cell.number_format = "#,##0"
    for col, wdt in zip("ABCDEFG", [12, 44, 19, 20, 12, 9, 11]):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A5"
    wr = wb.create_sheet("Round")
    total = sum(r["offer"] for r in s["rows"])
    issued = {2021: dt.date(2021, 4, 16), 2022: dt.date(2022, 4, 14), 2023: dt.date(2023, 4, 18),
              2024: dt.date(2024, 4, 16), 2025: dt.date(2025, 4, 15), 2026: dt.date(2026, 4, 14)}[c.year]
    for k, v in [("Census date", c), ("Pot ($)", POTS[c.year]),
                 ("Rate (cents per dollar of fall)", s["rate"] / 100.0),
                 ("Organisations scored", len(s["rows"])), ("Offers made", s["n_offers"]),
                 ("Total offered ($)", total), ("Retained in the Fund ($)", POTS[c.year] - total),
                 ("Issued", issued)]:
        wr.append([k, v])
    wr["B1"].number_format = "d mmmm yyyy"
    wr["B8"].number_format = "d mmmm yyyy"
    wr["B3"].number_format = "0.00"
    for cell in ("B2", "B6", "B7"):
        wr[cell].number_format = "#,##0"
    wr.column_dimensions["A"].width = 32
    wr.column_dimensions["B"].width = 16
    wb.save(path)
    return len(s["rows"])


# ----------------------------------------------------------------------------- payment run

PAY_COLS = ["payment_id", "batch", "value_date", "charity_no", "payee", "grant_ref", "programme",
            "instalment_for", "amount", "payment_status", "reissue_of"]
PROG = {"OG": "Operating grant", "PG": "Project grant", "SGF": "Steady Ground Fund"}


def write_payrun(path, W):
    by = W["by"]
    rows = []
    for p in W["payments"]:
        if not (dt.date(2018, 7, 1) <= p["value"] <= dt.date(2026, 9, 30)):
            continue
        o = by[p["org"]]
        y, m = p["inst_for"]
        batch = f"B{p['value'].strftime('%y%m%d')}"
        rows.append([p["id"], batch, p["value"].isoformat(), o.cc, o.name, p["ref"], PROG[p["prog"]],
                     f"{y}-{m:02d}", p["amount"], p["status"], p.get("reissue_of", "")])
    write_csv(path, PAY_COLS, rows)
    return len(rows)


# ----------------------------------------------------------------------------- neighbouring files

def write_survey(path):
    """A regional survey of community-sector income by sector (published by a funders' group)."""
    r = np.random.default_rng([SEED, 41])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "By sector"
    ws.append(["Canterbury community sector income survey 2025"])
    ws.append(["Canterbury Funders' Data Group. Survey of organisations' financial years ending in 2025, "
               "compared with the year before. Fieldwork February to April 2026."])
    ws.append([])
    ws.append(["Sector", "Responses", "Median income change (%)", "Share with income down 10% or more (%)",
               "Share holding a government contract (%)", "Median months of reserves"])
    sectors = ["Social services", "Health and disability", "Education and learning", "Arts and culture",
               "Environment", "Community development", "Recreation and sport"]
    for s in sectors:
        n = int(r.integers(31, 119))
        ws.append([s, n, round(float(r.normal(-1.2, 2.6)), 1), round(float(r.uniform(9, 31)), 1),
                   round(float(r.uniform(18, 71)), 1), round(float(r.uniform(2.1, 7.9)), 1)])
    ws.append(["All sectors", 512, -1.4, 19.7, 44.3, 4.2])
    ws.column_dimensions["A"].width = 26
    for col in "BCDEF":
        ws.column_dimensions[col].width = 20
    ws["A1"].font = Font(bold=True, size=12)
    for cell in ws[4]:
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True)
    wd = ws.parent.create_sheet("By district")
    wd.append(["District", "Responses", "Median income change (%)", "Share with income down 10% or more (%)"])
    for d in ["Christchurch", "Waimakariri", "Selwyn", "Ashburton", "Timaru", "Hurunui",
              "Banks Peninsula", "Kaikoura"]:
        wd.append([d, int(r.integers(9, 220)), round(float(r.normal(-1.0, 2.2)), 1),
                   round(float(r.uniform(8, 29)), 1)])
    wd.column_dimensions["A"].width = 18
    for col in "BCD":
        wd.column_dimensions[col].width = 22
    wn = ws.parent.create_sheet("Notes")
    for line in ["Responses are self-reported and unaudited.",
                 "Income is total income for the organisation's own financial year.",
                 "Government contracts include central and local government.",
                 "Survey weights were not applied; medians are of responding organisations."]:
        wn.append([line])
    wn.column_dimensions["A"].width = 90
    wb.save(path)


def write_ratings(path, W):
    r = np.random.default_rng([SEED, 42])
    rows = []
    reviewers = ["RA", "TH", "LB", "TH", "RA"]
    for o in sorted(W["orgs"], key=lambda o: o.cc):
        if o.role == "exit":
            continue
        rd = dt.date(2025, 9, 1) + dt.timedelta(days=int(r.integers(0, 300)))
        rows.append([o.cc, o.name, rd.isoformat(), "ABBBCCD"[int(r.integers(0, 7))],
                     "ABBBCCD"[int(r.integers(0, 7))], int(r.integers(1, 6)),
                     reviewers[int(r.integers(0, 5))],
                     (rd + dt.timedelta(days=730)).strftime("%Y-%m")])
    write_csv(path, ["charity_no", "organisation", "review_date", "governance_rating",
                     "financial_management_rating", "community_reach_score", "reviewer",
                     "next_review"], rows)
    return len(rows)
