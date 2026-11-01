"""Independent verifier for task259: reads every shipped format back with the standard library only (csv, zipfile and
XML for xlsx and docx, ASCII85 and Flate for the PDFs) and recomputes every graded figure on its own code path, then
compares with generator/figures.json and the golden workbook.

    python3 task259/generator/verify.py
"""
import base64
import collections
import csv
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REF = ["2025Q4", "2026Q1", "2026Q2", "2026Q3"]
QI = {q: i for i, q in enumerate(["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"])}
FAILS = []


def ok(label, cond, detail=""):
    print("%s  %-60s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAILS.append(label)


def rows(name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def xlsx_sheets(path):
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    rmap = {r.get("Id"): r.get("Target") for r in rels}
    out = {}
    for s in wb.find("m:sheets", NS):
        rid = s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        target = rmap[rid].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        sh = ET.fromstring(z.read(target))
        data = []
        for r in sh.iter("{%s}row" % NS["m"]):
            vals = []
            for c in r.findall("m:c", NS):
                v = c.find("m:v", NS)
                t = c.get("t")
                if t == "s":
                    vals.append(shared[int(v.text)])
                elif t == "inlineStr":
                    vals.append("".join(x.text or "" for x in c.iter("{%s}t" % NS["m"])))
                else:
                    vals.append(v.text if v is not None else None)
            data.append(vals)
        out[s.get("name")] = data
    return out


def docx_text(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))


def pdf_text(path):
    raw = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", raw, re.S):
        data = m.group(1).strip()
        try:
            if data.endswith(b"~>"):
                data = base64.a85decode(data, adobe=True)
            out.append(zlib.decompress(data).decode("latin-1"))
        except Exception:
            continue
    return " ".join(re.findall(r"\((.*?)\)\s*Tj", " ".join(out)))


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    # ---------------------------------------------------------------- read every format back
    P = rows("HES_PERSON_2025Q1_2026Q3.csv")
    X = rows("HES_CASEID_CROSSWALK_CAPI2026.csv")
    D = rows("HES_HOUSEHOLD_DISPOSITIONS_2025Q1_2026Q3.csv")
    Fr = rows("HES_FRAME_MAINTENANCE_2024-07_2026-09.csv")
    codes = rows("HES_DISPOSITION_CODES.csv")
    Wb = xlsx_sheets(os.path.join(T, "HES_FINAL_WEIGHTS_2025Q4_2026Q3.xlsx"))
    Ab = xlsx_sheets(os.path.join(T, "TDLI_WORKFORCE_AREAS_2026.xlsx"))
    rule = docx_text(os.path.join(T, "TAR_24-30-104_PORTABLE_BENEFITS_PILOT_AREAS.docx"))
    note = pdf_text(os.path.join(T, "HES_TECHNICAL_NOTE_2026-09.pdf"))
    rel = pdf_text(os.path.join(T, "HES_RELEASE_2026Q3_PRELIMINARY.pdf"))
    ok("V1 every format reads back (csv, xlsx, docx, pdf)", P and X and D and Fr and codes and Wb and Ab and rule and
       note and rel, "%d person rows, %d weight sheets" % (len(P), len(Wb)))
    ok("V2 the rule files the 7.0 percent line, the four quarters and the self-report basis",
       "7.0 percent" in rule and "30 September 2026" in rule and "would report it themselves" in rule)
    ok("V3 the technical note files the response-rate definitions and the 2026Q3 reissue",
       "occupied at the time of the interviewer" in note and "reissued" in note)

    # ---------------------------------------------------------------- weights and employed records
    wt = {}
    for q in REF:
        sheet = "2026Q3 rev" if q == "2026Q3" else q
        for r in Wb[sheet][1:]:
            wt[(q, r[0], int(r[1]))] = float(r[2])
    first_q3 = {(r[0], int(r[1])): float(r[2]) for r in Wb["2026Q3"][1:]}
    areas = sorted({p["HES_AREA"] for p in P})
    emp = [p for p in P if p["SURVEY_QTR"] in REF and p["LFSTAT"] in ("1", "2")]
    for p in emp:
        p["w"] = wt[(p["SURVEY_QTR"], p["CASEID"], int(p["LINENO"]))]
        p["self"] = p["RESPLINE"] == p["LINENO"]
        p["m"] = 1.0 if p["MJH"] == "1" else 0.0

    # ---------------------------------------------------------------- the panel, linked person by person
    n2o = {r["NEW_CASEID"]: r["OLD_CASEID"] for r in X}
    by = collections.defaultdict(list)
    for p in P:
        by[(n2o.get(p["CASEID"], p["CASEID"]), p["LINENO"])].append(p)
    pairs = []
    for key, recs in by.items():
        recs.sort(key=lambda r: QI[r["SURVEY_QTR"]])
        for a, b in zip(recs, recs[1:]):
            if a["SEX"] != b["SEX"] or int(b["AGE"]) - int(a["AGE"]) not in (0, 1):
                continue
            if QI[b["SURVEY_QTR"]] - QI[a["SURVEY_QTR"]] != 1:
                continue
            if a["LFSTAT"] in ("1", "2") and b["LFSTAT"] in ("1", "2"):
                pairs.append((a["RESPLINE"] == a["LINENO"], b["RESPLINE"] == b["LINENO"], a["MJH"] == "1",
                              b["MJH"] == "1"))
    # chains break at an identity change: a pair across a break is dropped above; a chain resumes after it
    sp = [p for p in pairs if p[0] and not p[1] and p[2]]
    ps = [p for p in pairs if not p[0] and p[1] and p[3]]
    ss = [p for p in pairs if p[0] and p[1]]
    keep_f = sum(p[3] for p in ss if p[2]) / sum(1 for p in ss if p[2])
    keep_b = sum(p[2] for p in ss if p[3]) / sum(1 for p in ss if p[3])
    raw = (sum(p[3] for p in sp) + sum(p[2] for p in ps)) / (len(sp) + len(ps))
    n0, n1 = sum(1 for p in ss if p[2]), sum(1 for p in ss if p[3])
    s = raw / ((n0 * keep_f + n1 * keep_b) / (n0 + n1))
    fsp = [p for p in pairs if p[0] and not p[1] and not p[2]]
    fps = [p for p in pairs if not p[0] and p[1] and not p[3]]
    gain = (sum(p[3] for p in ss if not p[2]) + sum(p[2] for p in ss if not p[3])) / \
        (sum(1 for p in ss if not p[2]) + sum(1 for p in ss if not p[3]))
    fp = max(0.0, (sum(p[3] for p in fsp) + sum(p[2] for p in fps)) / (len(fsp) + len(fps)) - gain)
    ok("V4 the within-person sensitivity reproduces (56 percent)", round(100 * s) == figs["sensitivity_pct"],
       "%.4f" % s)
    ok("V5 the raw share and the false-report rate reproduce", round(100 * raw, 1) == figs["sensitivity_raw_pct"] and
       round(100 * fp, 1) == figs["false_report_pct"], "%.4f %.4f" % (raw, fp))

    # ---------------------------------------------------------------- shares, certification, statewide
    names = {r[0]: r[1] for r in Ab["Areas"][1:]}
    share, tot_num, tot_den, face_num = {}, 0.0, 0.0, 0.0
    for a in areas:
        g = [p for p in emp if p["HES_AREA"] == a]
        sw = sum(p["w"] for p in g if p["self"])
        sm = sum(p["w"] * p["m"] for p in g if p["self"])
        pw = sum(p["w"] for p in g if not p["self"])
        pm = sum(p["w"] * p["m"] for p in g if not p["self"])
        t = (pm / pw - fp) / (s - fp)
        share[a] = 100 * (sm + t * pw) / (sw + pw)
        tot_num += sm + t * pw
        tot_den += sw + pw
        face_num += sm + pm
    cert = [names[a] for a in areas if share[a] >= 7.0]
    ok("V6 the certified areas reproduce", cert == figs["certified"], ", ".join(cert))
    ok("V7 each area's share reproduces to one decimal",
       all(round(share[a], 1) == figs["shares_pct"][names[a]] for a in areas))
    ok("V8 the statewide share reproduces (whole percent) and the as-collected figure",
       round(100 * tot_num / tot_den) == figs["statewide_pct"] and
       round(100 * face_num / tot_den, 1) == figs["statewide_as_collected_pct"],
       "%.3f %.3f" % (100 * tot_num / tot_den, 100 * face_num / tot_den))

    # ---------------------------------------------------------------- the release, the context artifact
    rel_ok = True
    for q in REF:
        g = [p for p in P if p["SURVEY_QTR"] == q and p["LFSTAT"] in ("1", "2")]
        ww = [(first_q3[(p["CASEID"], int(p["LINENO"]))] if q == "2026Q3" else wt[(q, p["CASEID"], int(p["LINENO"]))])
              for p in g]
        pct = 100 * sum(w for w, p in zip(ww, g) if p["MJH"] == "1") / sum(ww)
        rel_ok &= ("%.1f" % pct) in rel
    ok("V9 the release's multiple-jobholding percentages reproduce on the first-issue weights", rel_ok)

    # ---------------------------------------------------------------- the asks
    cty_area = {}
    for wda, nm, counties, board in Ab["Areas"][1:]:
        for c in counties.split(","):
            cty_area.setdefault(c.strip(), wda)
    zip_area = {r[0]: r[1] for r in Ab["County 59041"][1:]}
    interview = {c["CODE"] for c in codes if c["AAPOR_GROUP"] == "I"}
    ne = {c["CODE"] for c in codes if c["AAPOR_GROUP"] == "NE"}
    nch = {c["CODE"] for c in codes if c["AAPOR_GROUP"] == "NC"}
    units = {}
    for r in D:
        if r["SURVEY_QTR"] not in REF:
            continue
        k = (r["FRAMEID"], r["SURVEY_QTR"])
        u = units.setdefault(k, {"area": zip_area[r["ZIP"]] if r["CTY"] == "59041" else cty_area[r["CTY"]],
                                 "int": False, "codes": []})
        if r["DISPO"] in interview:
            u["int"] = True
        else:
            u["codes"].append((r["DISPO_DATE"], r["DISPO"]))
    log = collections.defaultdict(list)
    for r in Fr:
        log[r["FRAMEID"]].append(r)
    rr, nc = {}, {}
    tally = {a: [0, 0, 0] for a in areas}
    for (fid, q), u in units.items():
        if u["int"]:
            tally[u["area"]][0] += 1
            tally[u["area"]][1] += 1
            continue
        date, code = sorted(u["codes"])[-1]
        if code in ne:
            continue
        gone = False
        for e in log.get(fid, []):
            if e["ACTION"] == "DELETE" and e["REASON"] in ("VACANT", "DEMOLISHED") and e["EFFECTIVE"] <= date:
                undone = any(x["ACTION"] == "RESTORE" and x["REASON"] == "DELETED IN ERROR" and
                             x["EFFECTIVE"] >= e["EFFECTIVE"] for x in log[fid])
                gone |= not undone
        if gone:
            continue
        tally[u["area"]][1] += 1
        tally[u["area"]][2] += code in nch
    for a in areas:
        rr[a] = 100 * tally[a][0] / tally[a][1]
        nc[a] = 100 * tally[a][2] / tally[a][1]
    ok("V10 every household response rate reproduces to one decimal",
       all(round(rr[a], 1) == figs["response_rate_pct"][names[a]] for a in areas))
    ok("V11 every noncontact rate reproduces to one decimal",
       all(round(nc[a], 1) == figs["noncontact_rate_pct"][names[a]] for a in areas))

    # ---------------------------------------------------------------- the goldens agree with the figures
    G = xlsx_sheets(os.path.join(TASK, "golden", "pba_pilot_areas_2027.xlsx"))
    pa = {r[1]: r for r in G["Pilot areas"][1:9]}
    sq = {r[1]: r for r in G["Survey quality"][1:9]}
    ok("V12 the golden workbook's certification and rates match the figures",
       all((pa[n][3] == "Yes") == (n in figs["certified"]) for n in pa) and
       all(abs(float(sq[n][2]) - figs["response_rate_pct"][n]) < 1e-9 and
           abs(float(sq[n][3]) - figs["noncontact_rate_pct"][n]) < 1e-9 for n in sq))
    memo = docx_text(os.path.join(TASK, "golden", "pba_pilot_certification_2027.docx"))
    ok("V13 the memo names every certified area and the statewide share",
       all(n in memo for n in figs["certified"]) and ("%d percent" % figs["statewide_pct"]) in memo)
    print("%s: %d failed" % ("PASS" if not FAILS else "FAIL", len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
