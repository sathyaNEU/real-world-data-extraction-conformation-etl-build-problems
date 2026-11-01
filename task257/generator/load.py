"""Read the pack as a solver would: every table from target/, nothing from the generator's state."""
from __future__ import annotations

import datetime as dt
import json
import os
import re

import pandas as pd

import common as K


def questionnaire(path):
    """The questionnaire's rows: each question's English and French numbers, library item, type and English and
    French wording, read from the fielding copy's text (a question's English wording ends at its first full stop or
    question mark; the French follows)."""
    import pdfplumber
    lines = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            lines += page.extract_text().splitlines()
    head = re.compile(r"^(Q\d\d|ENPS)\s+(F\d\d|ENPS)\s+(KL-\d{4})\s+(Statement|Yes or no|Recomme\S*)\s*(.*)$")
    rows, cur = [], None
    for ln in lines:
        m = head.match(ln.strip())
        if m:
            cur = dict(Item=m.group(1), French=m.group(2), Library=m.group(3), Type=m.group(4), text=[m.group(5)])
            rows.append(cur)
        elif cur is not None and not ln.startswith(("Kestrava Listening", "EN no.", "Page ")):
            cur["text"].append(ln.strip())
    out = []
    for r in rows:
        words = " ".join(t for t in r["text"] if t)
        if r["Item"] == "ENPS":
            cut = words.index(")") + 1
        else:
            cut = min(i for i in (words.find(". "), words.find("? ")) if i >= 0) + 1
        out.append({"Item": r["Item"], "French code": r["French"], "Library item": r["Library"],
                    "Scale": "agree5" if r["Type"] == "Statement" else ("yesno" if r["Type"] == "Yes or no" else "nps11"),
                    "Question (English)": words[:cut].strip(), "Question (French)": words[cut:].strip()})
    return pd.DataFrame(out)


def read(target):
    p = lambda n: os.path.join(target, n)
    resp = pd.read_csv(p(K.RESPONSES), comment="#", dtype={"token": str, "item": str})
    subs = pd.read_csv(p(K.SUBMISSIONS), dtype={"token": str})
    dist = pd.read_csv(p(K.INVITATIONS), dtype={"token": str, "employee_id": str})
    kiosk = pd.DataFrame([json.loads(line) for line in open(p(K.KIOSK), encoding="utf-8")])
    paper = pd.read_excel(p(K.PAPER), header=4)
    sites = pd.read_csv(p(K.SITES), keep_default_na=False)
    items = questionnaire(p(K.QUESTIONNAIRE))
    T = dict(resp=resp, subs=subs, dist=dist, kiosk=kiosk, paper=paper, sites=sites, items=items)
    if os.path.exists(p(K.HRIS)):
        T["hris"] = pd.read_csv(p(K.HRIS), comment="#", dtype={"employee_id": str, "department_code": str},
                                keep_default_na=False)
    return T


def item_map(items):
    """Export item code (English Q or French F code) -> the item's English code; the 30 items in English order."""
    m = {}
    order = []
    for _, r in items.iterrows():
        if r["Item"] == "ENPS":
            continue
        m[r["Item"]] = r["Item"]
        m[r["French code"]] = r["Item"]
        order.append(r["Item"])
    return m, order


def in_force(hris, day):
    """The assignment rows in force on a day (terminations end an employee's assignments from their own date)."""
    d = day.isoformat()
    h = hris[hris["action"] != "termination"]
    term = hris[hris["action"] == "termination"].groupby("employee_id")["effective_from"].min().to_dict()
    ok = (h["effective_from"] <= d) & ((h["effective_to"] == "") | (h["effective_to"] >= d))
    h = h[ok]
    keep = [not (e in term and term[e] <= d) for e in h["employee_id"]]
    return h[keep]


def opening_site(hris, day=K.OPEN_DAY):
    """employee_id -> the site they were assigned to on a day."""
    h = in_force(hris, day)
    return dict(zip(h["employee_id"], h["site_no"].astype(int)))


def close_utc(tz):
    off = K.TZ_OFFSET[tz]
    return (dt.datetime(2026, 9, 27, 23, 59, 59) - dt.timedelta(hours=off)).strftime("%Y-%m-%dT%H:%M:%SZ")
