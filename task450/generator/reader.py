"""Read task450's shipped files back into the arrays calc.py works on, the way a solver would: score each year's
answers with the bank's keys (the notice's correction applied), place each 2026 test with its student and campus,
and keep the 2025 tests' campus fields as the old platform recorded them."""
import csv
import datetime as dt
import os
import re

import numpy as np
import openpyxl

import docs as DC
import pack as P
import world as W


def _date(s):
    return dt.date.fromisoformat(s)


def notice(target):
    from pypdf import PdfReader
    txt = " ".join(" ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, DC.NOTICE)).pages).split())
    m = re.search(r"Item (M5\d{5}), position (\d+) .*? with key ([A-D])\. .*?Score the item with key ([A-D])", txt)
    return dict(item=m.group(1), pos=int(m.group(2)), wrong=m.group(3), right=m.group(4))


def bank(target):
    ws = openpyxl.load_workbook(os.path.join(target, P.FILES["bank"]), read_only=True)["Items"]
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    return [dict(item=r[0], key=r[4], pos25=r[6], pos26=r[7]) for r in rows]


def directory(target):
    ws = openpyxl.load_workbook(os.path.join(target, P.FILES["directory"]), read_only=True)["Campuses"]
    out = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        out[str(r[0])] = dict(name=r[1], community=r[2], status=r[5])
    names = {v["name"]: k for k, v in out.items()}
    into = {}
    for k, v in out.items():
        m = re.search(r"attendance zone to (.+)$", v["status"] or "")
        if m:
            into[k] = names[m.group(1).strip()]
    return out, into


def expand(abbrev):
    n = " " + abbrev + " "
    for a, b in ((" EL ", " ELEMENTARY "), (" AVE ", " AVENUE "), (" ST ", " STREET "), (" RD ", " ROAD "),
                 (" TER ", " TERRACE "), (" XING ", " CROSSING "), (" PR ", " PRAIRIE "), (" HOLW ", " HOLLOW "),
                 (" MDW ", " MEADOW "), (" JUNP ", " JUNIPER ")):
        n = n.replace(a, b)
    return n.strip()


def load(target, corrected=True):
    B = bank(target)
    N = notice(target)
    key25 = [None] * W.N_ITEMS
    key26 = [None] * W.N_ITEMS
    id26 = {}
    for r in B:
        if r["pos25"]:
            key25[int(r["pos25"]) - 1] = r["key"]
        if r["pos26"]:
            k = r["key"]
            if corrected and r["item"] == N["item"]:
                k = N["right"]
            key26[int(r["pos26"]) - 1] = k
            id26[r["item"]] = int(r["pos26"])
    anchor = sorted(int(r["pos25"]) - 1 for r in B if r["pos25"] and r["pos26"])
    # 2025: wide by position
    with open(os.path.join(target, P.FILES["resp25"]), newline="") as fh:
        rd = csv.reader(fh)
        hdr = next(rd)
        rows25 = list(rd)
    ic = hdr.index("I01")
    R25 = np.array([r[ic:ic + W.N_ITEMS] for r in rows25], dtype=object)
    S25 = (R25 == np.array(key25, dtype=object)[None, :]).astype(int)
    code25 = [r[hdr.index("SCHOOL_CODE")] for r in rows25]
    name25 = [r[hdr.index("SCHOOL_NAME")] for r in rows25]
    # 2026: long by item id
    resp = {}
    with open(os.path.join(target, P.FILES["resp26"]), newline="") as fh:
        rd = csv.DictReader(fh)
        for r in rd:
            a = resp.setdefault(r["test_taker_id"], [""] * W.N_ITEMS)
            a[id26[r["item_id"]] - 1] = r["response"]
    takers = sorted(resp)
    R26 = np.array([resp[t] for t in takers], dtype=object)
    S26 = (R26 == np.array(key26, dtype=object)[None, :]).astype(int)
    xw = {}
    reg_campus = {}
    with open(os.path.join(target, P.FILES["xwalk"]), newline="") as fh:
        for r in csv.DictReader(fh):
            xw[r["test_taker_id"]] = r["student_id"]
            reg_campus[r["test_taker_id"]] = r["campus_number"]
    spells = {}
    with open(os.path.join(target, P.FILES["enroll"]), newline="") as fh:
        for r in csv.DictReader(fh):
            spells.setdefault(r["student_id"], []).append((r["campus_number"], _date(r["entry_date"]),
                                                           _date(r["exit_date"]), r["exit_code"]))
    merges = {}
    with open(os.path.join(target, P.FILES["merges"]), newline="") as fh:
        for r in csv.DictReader(fh):
            merges[r["merged_id"]] = r["surviving_id"]
    D, into = directory(target)
    return dict(S25=S25, R25=R25, S26=S26, R26=R26, takers=takers, anchor=anchor, key25=key25, key26=key26,
                code25=code25, name25=name25, xw=xw, reg_campus=reg_campus, spells=spells, merges=merges,
                directory=D, into=into, notice=N)


def fay_campus(spells, snapshot=W.SNAPSHOT, first=W.WINDOW[0]):
    """The campus a student is full academic year at (the policy's section 3), or None. An exit dated the last day of
    school with code EY is an enrollment open at year end."""
    cover = [c for c, a, b, code in spells if a <= snapshot and b >= first]
    if len(cover) != 1:
        return None
    c = cover[0]
    for c2, a, b, code in spells:
        if c2 != c and a <= first and b >= snapshot:
            return None
    return c


def campus_table(L, r, corrected_raw=None, use_fay=True, merge_closed=True, n_min=W.N_MIN):
    """Per rated campus number: (tested full-academic-year students, those at or above r)."""
    raw = (corrected_raw if corrected_raw is not None else L["S26"]).sum(1)
    agg = {}
    for i, t in enumerate(L["takers"]):
        sid = L["xw"][t]
        sp = L["spells"].get(sid, [])
        c = fay_campus(sp) if use_fay else (sp[-1][0] if sp else None)
        if c is None:
            continue
        if merge_closed:
            c = L["into"].get(c, c)
        n, k = agg.get(c, (0, 0))
        agg[c] = (n + 1, k + int(raw[i] >= r))
    return {c: (n, k) for c, (n, k) in agg.items() if n >= n_min}


def designated(table, line=W.LINE):
    return sorted(c for c, (n, k) in table.items() if k < line * n)
