"""Independent verifier: reads every shipped file back on its own code path (pandas for CSV, the workbook XML read
straight from the zip, its own ASCII85 and Flate decoder for the PDFs, json for the configuration) and recomputes
the call and every graded figure without importing analysis.py, world.py or params.py.

    python3 task281/generator/verify.py           # exit 1 on any mismatch with figures.json
"""
import base64
import datetime as dt
import json
import os
import re
import sys
import zipfile
import zlib
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
LA = ZoneInfo("America/Los_Angeles")
FAIL = []


def say(ok, what, detail=""):
    print("%-4s %s %s" % ("OK" if ok else "FAIL", what, detail))
    if not ok:
        FAIL.append(what)


def half_up(x, nd=0):
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(1).scaleb(-nd)
    v = Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)
    return float(v) if nd else int(v)


# ------------------------------------------------------------------------------------------------ readers
def pdf_strings(path):
    raw = open(path, "rb").read()
    words = []
    pos = 0
    while True:
        i = raw.find(b"stream", pos)
        if i < 0:
            break
        j = raw.find(b"endstream", i)
        head = raw[max(0, i - 120):i]
        body = raw[i + 6:j].strip(b"\r\n")
        pos = j + 9
        if b"ASCII85Decode" in head:
            if body.endswith(b"~>"):
                body = body[:-2]
            body = base64.a85decode(body)
        if b"FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                continue
        words += [m.decode("latin-1") for m in re.findall(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj", body)]
    return " ".join(w.replace("\\(", "(").replace("\\)", ")") for w in words)


def xlsx_sheets(path):
    """{sheet name: list of rows (lists of cell values)} read from the workbook's XML."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for s in wb.find("m:sheets", NS):
        rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        xml = ET.fromstring(z.read("xl/" + target[rid].lstrip("/").replace("xl/", "")))
        rows = []
        for row in xml.iter("{%s}row" % NS["m"]):
            vals = {}
            for c in row.findall("m:c", NS):
                ref = re.match(r"([A-Z]+)", c.get("r")).group(1)
                col = 0
                for ch in ref:
                    col = col * 26 + ord(ch) - 64
                v = c.find("m:v", NS)
                t = c.get("t")
                if t == "s":
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                elif v is None:
                    val = None
                else:
                    val = float(v.text)
                vals[col] = val
            rows.append([vals.get(k) for k in range(1, max(vals) + 1)] if vals else [])
        out[s.get("name")] = rows
    return out


def serial_date(x):
    return (dt.datetime(1899, 12, 30) + dt.timedelta(days=float(x))).date()


# ------------------------------------------------------------------------------------------------ main
def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    f = {n: os.path.join(T, n) for n in os.listdir(T)}
    res = pd.read_csv([p for n, p in f.items() if n.startswith("retina_ai_results")][0], dtype=str)
    val = pd.read_csv([p for n, p in f.items() if n.startswith("local_validation_study")][0], dtype=str)
    orders = pd.read_csv([p for n, p in f.items() if n.startswith("ehr_retinal")][0], dtype=str)
    reg = pd.read_csv([p for n, p in f.items() if n.startswith("diabetes_registry")][0], dtype=str).fillna("")
    him = pd.read_csv([p for n, p in f.items() if n.startswith("him_outside")][0], dtype=str)
    log = pd.read_csv([p for n, p in f.items() if n.startswith("pellam_overread")][0], dtype=str)
    tick = pd.read_csv([p for n, p in f.items() if n.startswith("biomed_service")][0], dtype=str).fillna("")
    dirx = pd.read_csv(f["clinic_directory.csv"], dtype=str)
    cfg = json.load(open([p for n, p in f.items() if n.endswith(".json")][0]))
    say(len(cfg["sites"]) == len(dirx), "site configuration lists every directory site", str(len(cfg["sites"])))
    for n in f:
        if n.endswith(".xlsx"):
            sh = xlsx_sheets(f[n])
            say(all(len(r) > 1 for r in sh.values()), "workbook reads back: %s" % n, ", ".join(sh))
    std = pdf_strings([p for n, p in f.items() if n.startswith("clinical_ai_governance")][0])
    proto = pdf_strings([p for n, p in f.items() if n.startswith("validation_study_protocol")][0])
    ops_txt = pdf_strings([p for n, p in f.items() if n.startswith("retinacheck_operating")][0])
    agr = pdf_strings([p for n, p in f.items() if n.startswith("pellam_reading")][0])
    for name, txt in (("standard", std), ("protocol", proto), ("guide", ops_txt), ("agreement", agr)):
        say(len(txt) > 400, "pdf text decodes: %s" % name, "%d characters" % len(txt))
    ops = sorted(((m.group(1), int(m.group(2))) for m in re.finditer(r"(\w+) (\d\d) or above", ops_txt)),
                 key=lambda o: -o[1])
    floor = int(re.search(r"at least (\d+) per cent", std).group(1)) / 100
    cap = int(re.search(r"up to ([\d,]+) referrals", agr).group(1).replace(",", ""))
    sites = dict(re.findall(r"Site ([ABC]) (Wendmere Primary Care|Quarry Hill|Yarrowby Medical)", proto))

    # cameras: placements per location from the location history, models from the asset sheet
    book = xlsx_sheets([p for n, p in f.items() if n.startswith("biomed_asset_register")][0])
    model = {}
    for r in book["Assets"][1:]:
        if r and str(r[2]).startswith("Retinal camera"):
            model[str(r[1]).replace("HO-", "")] = r[4]
    spans = {}
    openings = {}
    for r in sorted(book["Location History"][1:], key=lambda r: (r[2], str(r[1]))):
        s = str(r[1]).replace("HO-", "")
        if s not in model:
            continue
        d = serial_date(r[2])
        if (r[3], s) in openings:
            spans.setdefault(r[3], []).append((openings.pop((r[3], s)), d, s))
        openings[(r[4], s)] = d
    for (loc, s), d in openings.items():
        spans.setdefault(loc, []).append((d, dt.date(2100, 1, 1), s))

    def cam(loc, day):
        hit = [s for a, b, s in spans[loc] if a <= day < b]
        assert len(hit) == 1, (loc, day, hit)
        return model[hit[0]]

    loc_of_portal = dict(zip(dirx["portal_site"], dirx["biomed_location"]))
    name_of_portal = dict(zip(dirx["portal_site"], dirx["portal_site"]))
    code = dict(zip(dirx["portal_site"], dirx["clinic_code"]))
    pretty = {"OF": "Orrin Falls", "TB": "Thistlebrook", "WM": "Wendmere", "PB": "Pellsbury", "QH": "Quarry Hill",
              "RW": "Rookwood", "SC": "Sallow Creek", "VD": "Veldane", "BF": "Brackenfield", "YB": "Yarrowby",
              "KN": "Kestle Road", "HM": "Hollinmoor"}

    # validation sensitivity by camera model
    lv = {"moderate NPDR", "severe NPDR", "PDR"}
    val["ref"] = val["final_level"].isin(lv) | (val["final_dme"] == "Y")
    val["day"] = pd.to_datetime(val["capture_date"], format="%m/%d/%Y").dt.date
    val["cam"] = [cam(loc_of_portal[sites[s]], d) for s, d in zip(val["site"], val["day"])]
    val["score"] = pd.to_numeric(val["dr_score"])
    sens = {}
    for m in ("NR-40", "NR-70"):
        rr = val[(val["cam"] == m) & val["ref"]]
        sens[m] = {nm: float(((rr["ai_result"] == "Ungradable") | (rr["score"] >= c)).mean()) for nm, c in ops}
        say(all(half_up(100 * sens[m][nm], 1) == fig["validation_by_model_pct"][m][nm] for nm, _ in ops),
            "validation sensitivity by model %s" % m, str({k: round(100 * v, 2) for k, v in sens[m].items()}))

    # the year's screenings on their cameras, each clinic's point, the referrals
    res["t"] = pd.to_datetime(res["Captured (UTC)"], utc=True).dt.tz_convert(LA)
    res["day"] = res["t"].dt.date
    res["cam"] = [cam(loc_of_portal[s], d) for s, d in zip(res["Site"], res["day"])]
    res["score"] = pd.to_numeric(res["DR Score"])
    picks, per = {}, {}
    for site, g in res.groupby("Site"):
        sh40 = float((g["cam"] == "NR-40").mean())
        cells = {nm: sh40 * sens["NR-40"][nm] + (1 - sh40) * sens["NR-70"][nm] for nm, _ in ops}
        pk = next((nm for nm, _ in ops if cells[nm] >= floor), None)
        cut = dict(ops)[pk]
        k = pretty[code[site]]
        picks[k] = pk
        per[k] = int(((g["Result"] == "Ungradable") | (g["score"] >= cut)).sum())
        say(half_up(100 * sh40) == fig["nr40_share_pct"][k], "NR-40 share %s" % k, "%.2f" % (100 * sh40))
    say(picks == fig["points"], "2027 point at every clinic", str(picks))
    say(per == fig["referrals_by_clinic"], "referrals by clinic", str(per))
    say(sum(per.values()) == fig["referrals_total"] and sum(per.values()) <= cap, "network referrals within capacity",
        "%d of %d" % (sum(per.values()), cap))

    # reading center reads of the AI's referrals
    kind = dict(zip(orders["ORDER_ID"], orders["PROC_CODE"]))
    dept = dict(zip(orders["ORDER_ID"], orders["DEPARTMENT"]))
    ehr_code = dict(zip(dirx["ehr_department"], dirx["clinic_code"]))
    log["n"] = log["Case No"].astype(int)
    ai = log[log["Referral Order"].map(kind) == "REF7734"].sort_values("n")
    read, conf, days = {}, {}, {}
    qname = lambda d: ("Oct-Dec 2025" if d < dt.date(2026, 1, 1) else "Jan-Mar 2026" if d < dt.date(2026, 4, 1)
                       else "Apr-Jun 2026" if d < dt.date(2026, 7, 1) else "Jul-Sep 2026")
    for oid, g in ai.groupby("Referral Order"):
        k = pretty[ehr_code[dept[oid]]]
        closing = g[g["Final Grade"].isin(["Referable", "Not referable"])]
        read[k] = read.get(k, 0) + 1
        conf[k] = conf.get(k, 0) + int(len(closing) > 0 and closing.iloc[-1]["Final Grade"] == "Referable")
        if len(closing):
            d0 = dt.datetime.strptime(g.iloc[0]["Image Date"], "%m/%d/%Y").date()
            d1 = pd.Timestamp(closing.iloc[-1]["Graded (UTC)"]).tz_convert(LA).date()
            days.setdefault(qname(d0), []).append((d1 - d0).days)
    say(read == fig["reads_by_clinic"], "AI referrals read by clinic", "")
    say({k: half_up(100 * conf[k] / read[k]) for k in read} == fig["confirmed_pct_by_clinic"],
        "share confirmed referable by clinic", "")
    say({q: half_up(sum(v) / len(v), 1) for q, v in days.items()} == fig["days_by_quarter"], "days by quarter",
        str({q: round(sum(v) / len(v), 3) for q, v in days.items()}))

    # camera faults
    cams = tick[tick["Equipment Class"].str.startswith("Retinal camera")]
    loc_code = dict(zip(dirx["biomed_location"], dirx["clinic_code"]))
    cap_days = {}
    for s, d in zip(res["Site"], res["day"]):
        cap_days.setdefault(code[s], set()).add(d)
    moves_in = {}
    for r in book["Location History"][1:]:
        if str(r[1]).replace("HO-", "") in model:
            moves_in.setdefault(r[4], []).append(serial_date(r[2]))
    dt_out = {}
    for _, t in cams.iterrows():
        opened = dt.datetime.strptime(t["Opened"], "%m/%d/%Y").date()
        if not (dt.date(2025, 10, 1) <= opened <= dt.date(2026, 9, 30)):
            continue
        c = loc_code[t["Location"]]
        back = min(d for d in moves_in[t["Location"]] if d > opened)
        n_days = sum(1 for i in range(1, (back - opened).days) if (opened + dt.timedelta(days=i)).weekday() < 5
                     and (opened + dt.timedelta(days=i)) not in cap_days[c])
        dt_out["%s, fault reported %s" % (pretty[c], opened.isoformat())] = n_days
    say(dt_out == fig["downtime"], "camera faults: clinic days with no screening", str(dt_out))

    print("verify: %s (%d mismatches)" % ("PASS" if not FAIL else "FAIL", len(FAIL)))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
