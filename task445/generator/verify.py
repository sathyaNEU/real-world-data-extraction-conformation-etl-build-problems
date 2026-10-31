"""An independent recomputation from target/ with its own readers (pandas for the register, the workbook's XML
for the north log, plain json for the south export, the PDF's text for Table 1): the summer counts, the qualifying
places, both asks. make.py compares it with the golden."""
import datetime as dt
import json
import os
import re
import sys
import zipfile
from collections import defaultdict

import pandas as pd
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as PK  # noqa: E402
import world as W  # noqa: E402

EPOCH = dt.date(1899, 12, 30)


def any_date(s):
    s = str(s)
    return dt.datetime.strptime(s, "%d/%m/%Y").date() if "/" in s else dt.date.fromisoformat(s)


def north_rows(path):
    """read the sheet straight from its XML: shared strings and Excel serial dates"""
    with zipfile.ZipFile(path) as z:
        sst = re.findall(r"<si>(?:<t[^>]*>)?(.*?)(?:</t>)?</si>", z.read("xl/sharedStrings.xml").decode("utf-8"))
        sst = [re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&apos;", "'").replace("&quot;", '"')
               .replace("&lt;", "<").replace("&gt;", ">") for s in sst]
        xml = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
    out = []
    for row in re.findall(r"<row [^>]*>(.*?)</row>", xml, re.S):
        cells = {}
        for ref, attrs, val in re.findall(r'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(?:<v>([^<]*)</v>)?</c>)', row):
            if val == "":
                continue
            cells[ref] = sst[int(val)] if 't="s"' in attrs else val
        out.append(cells)
    hdr = out[0]
    cols = {v: k for k, v in hdr.items()}
    rows = []
    for c in out[1:]:
        g = lambda name: c.get(cols[name])  # noqa: E731
        ser = lambda v: EPOCH + dt.timedelta(days=int(float(v)))  # noqa: E731
        sur, fn = g("Deceased").split(", ", 1)
        rows.append(dict(sur=sur.lower(), fn=fn.lower(), dob=ser(g("Date of birth")), dod=ser(g("Date of death")),
                         pc=g("Usual postcode"), done=ser(g("Scrutiny completed")), cref=g("Coroner ref") or ""))
    return rows


def south_rows(path):
    doc = json.load(open(path, encoding="utf-8"))
    rows = []
    for c in doc["cases"]:
        t = dt.datetime.strptime(c["scrutiny"]["completed_at"], "%Y-%m-%dT%H:%M:%SZ")
        # British Summer Time: last Sunday of March to last Sunday of October
        y = t.year
        start = max(dt.date(y, 3, d) for d in range(25, 32) if dt.date(y, 3, d).weekday() == 6)
        end = max(dt.date(y, 10, d) for d in range(25, 32) if dt.date(y, 10, d).weekday() == 6)
        local = t + dt.timedelta(hours=1) if start <= t.date() < end else t
        rows.append(dict(sur=c["deceased"]["family_name"].lower(), fn=c["deceased"]["given_names"].lower(),
                         dob=dt.date.fromisoformat(c["deceased"]["date_of_birth"]),
                         dod=dt.date.fromisoformat(c["death"]["date"]), pc=c["death"]["usual_postcode"],
                         done=local.date(), cref=(c["coroner"] or {}).get("reference") or ""))
    return rows


def fy_quarter(d):
    if dt.date(2025, 4, 1) <= d <= dt.date(2026, 3, 31):
        return {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[d.month]
    return 0


def run(target=W.TARGET):
    reg = pd.read_csv(os.path.join(target, PK.REG), dtype=str)
    reg["reg"] = reg["date_of_registration"].map(any_date)
    reg["dod"] = reg["date_of_death"].map(any_date)
    reg["dob"] = reg["date_of_birth"].map(any_date)
    first = reg[reg["version"] == "1"].drop_duplicates(["registration_district", "entry_number"])
    lk = pd.read_csv(os.path.join(target, PK.LOOKUP), dtype=str)
    place_of_pc = dict(zip(lk["postcode"], lk["place_name"]))
    place_of_code = dict(zip(lk["place_code"], lk["place_name"]))
    first = first.assign(place=first["usual_residence_code"].map(place_of_code))
    txt = " ".join(p.extract_text() for p in PdfReader(os.path.join(target, PK.TERMS)).pages)
    expected = {p: int(re.search(re.escape(p) + r"\s+E\d{8}\s+([\d,]+)", txt).group(1).replace(",", ""))
                for p in W.NAMES}
    w = first[(first["dod"] >= W.W0) & (first["dod"] <= W.W1)]
    on_reg = set(zip(w["deceased_surname"].str.lower(), w["deceased_forenames"].str.lower(), w["dob"], w["dod"]))
    counts = w.groupby("place").size().to_dict()
    north = north_rows(os.path.join(target, PK.NORTH))
    south = south_rows(os.path.join(target, PK.SOUTH))
    extra = {}
    for r in north + south:
        if W.W0 <= r["dod"] <= W.W1 and r["pc"] in place_of_pc:
            k = (r["sur"], r["fn"], r["dob"], r["dod"])
            if k not in on_reg:
                extra[k] = place_of_pc[r["pc"]]
    for k, p in extra.items():
        counts[p] = counts.get(p, 0) + 1
    ex = {p: 100.0 * (counts[p] - expected[p]) / expected[p] for p in W.NAMES}
    qual = [p for p in W.NAMES if ex[p] >= 10.0]
    # ask B: deaths, not cases: rows sharing a coroner reference or a person are one death
    ask_b = {}
    for office, rows in (("North", north), ("South", south)):
        rows = [r for r in rows if fy_quarter(r["done"])]
        label = {}
        nxt = 0
        merged = {}
        for i, r in enumerate(rows):
            ks = [("p", r["sur"], r["fn"], r["dob"], r["dod"])] + ([("c", r["cref"])] if r["cref"] else [])
            ids = {label[k] for k in ks if k in label}
            if ids:
                tgt = min(ids)
                for k2, v2 in list(label.items()):
                    if v2 in ids:
                        label[k2] = tgt
                for v2 in ids:
                    if v2 != tgt:
                        merged[v2] = tgt
            else:
                tgt = nxt
                nxt += 1
            for k in ks:
                label[k] = tgt
            r["_g"] = tgt
        def root(g):  # noqa: E306
            while g in merged:
                g = merged[g]
            return g
        first_q = {}
        for r in rows:
            g = root(r["_g"])
            first_q[g] = min(first_q.get(g, 9), fy_quarter(r["done"]))
        for q in (1, 2, 3, 4):
            ask_b[(office, q)] = sum(1 for v in first_q.values() if v == q)
    # ask C: each entry as it now stands, its fields off the last version and its date off the registration
    reg["v"] = reg["version"].astype(int)
    last = reg.sort_values(["registration_district", "entry_number", "v"]).drop_duplicates(
        ["registration_district", "entry_number"], keep="last")
    regdate = dict(zip(zip(first["registration_district"], first["entry_number"]), first["reg"]))
    last = last.assign(reg=[regdate[k] for k in zip(last["registration_district"], last["entry_number"])],
                       place=last["usual_residence_code"].map(place_of_code))
    c = last[(last["dod"] >= dt.date(2025, 1, 1)) & (last["dod"] <= dt.date(2025, 12, 31))
             & last["certification"].str.startswith("Medical certificate")]
    c = c.assign(q=c["dod"].map(lambda d: (d.month - 1) // 3 + 1),
                 fast=[(a - b).days <= 5 for a, b in zip(c["reg"], c["dod"])])
    ask_c = {(p, q): 100.0 * g["fast"].mean() for (p, q), g in c.groupby(["place", "q"])}
    return dict(counts=counts, excess=ex, qualifying=qual, ask_b=ask_b, ask_c=ask_c, expected=expected)
