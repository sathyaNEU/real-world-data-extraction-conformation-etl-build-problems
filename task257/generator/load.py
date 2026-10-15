"""Read the pack as a solver would: every table from target/, nothing from the generator's state."""
from __future__ import annotations

import datetime as dt
import json
import os

import pandas as pd

import common as K


def read(target):
    p = lambda n: os.path.join(target, n)
    resp = pd.read_csv(p(K.RESPONSES), comment="#", dtype={"token": str, "item": str})
    subs = pd.read_csv(p(K.SUBMISSIONS), dtype={"token": str})
    dist = pd.read_csv(p(K.INVITATIONS), dtype={"token": str, "employee_id": str})
    kiosk = pd.DataFrame([json.loads(line) for line in open(p(K.KIOSK), encoding="utf-8")])
    paper = pd.read_excel(p(K.PAPER), header=4)
    hris = pd.read_csv(p(K.HRIS), dtype={"employee_id": str}, keep_default_na=False)
    sites = pd.read_csv(p(K.SITES), keep_default_na=False)
    items = pd.read_excel(p(K.CODEBOOK), sheet_name="Items")
    return dict(resp=resp, subs=subs, dist=dist, kiosk=kiosk, paper=paper, hris=hris, sites=sites, items=items)


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


def opening_site(hris, day=K.OPEN_DAY):
    """employee_id -> the site they were assigned to on a day (terminations end an assignment)."""
    d = day.isoformat()
    h = hris[hris["action"] != "termination"]
    term = hris[hris["action"] == "termination"].set_index("employee_id")["effective_from"].to_dict()
    ok = (h["effective_from"] <= d) & ((h["effective_to"] == "") | (h["effective_to"] >= d))
    out = {}
    for e, s in zip(h.loc[ok, "employee_id"], h.loc[ok, "site_no"]):
        if e in term and term[e] <= d:
            continue
        out[e] = int(s)
    return out


def close_utc(tz):
    off = K.TZ_OFFSET[tz]
    return (dt.datetime(2026, 9, 27, 23, 59, 59) - dt.timedelta(hours=off)).strftime("%Y-%m-%dT%H:%M:%SZ")
