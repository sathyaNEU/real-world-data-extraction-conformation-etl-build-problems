"""The independent verifier: reads every shipped file back on its own code path (csv module, zipfile XML for the
workbooks and the Word files, ASCII85 and Flate for the PDFs; no pandas, no openpyxl, nothing from analysis.py)
and recomputes the call and every ask figure, then checks figures.json and the golden deliverables against them.

    python3 task160/generator/verify.py [target_dir golden_dir figures.json]"""
import base64
import csv
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile
from collections import defaultdict
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ET, UTC = ZoneInfo("America/New_York"), ZoneInfo("UTC")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        head = next(r)
        return [dict(zip(head, x)) for x in r]


def xlsx_sheets(path):
    """Every sheet as a list of rows of strings, read from the package XML."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        x = z.read("xl/sharedStrings.xml").decode("utf-8")
        for si in re.findall(r"<si>(.*?)</si>", x, re.S):
            shared.append("".join(re.findall(r"<t[^>]*>(.*?)</t>", si, re.S)))
    wbx = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    rmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    rmap.update({a: b for b, a in re.findall(r'Target="([^"]+)"[^>]*Id="(rId\d+)"', rels)})
    out = {}
    for name, rid in re.findall(r'<sheet[^>]*name="([^"]+)"[^>]*r:id="(rId\d+)"', wbx):
        target = rmap[rid].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        x = z.read(target).decode("utf-8")
        table = []
        for rx in re.findall(r"<row[^>]*>(.*?)</row>", x, re.S):
            cells = {}
            for ref, attrs, body in re.findall(r'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(.*?)</c>)', rx, re.S):
                v = re.search(r"<v>(.*?)</v>", body or "")
                t = re.search(r't="(\w+)"', attrs)
                if t and t.group(1) == "s" and v:
                    val = shared[int(v.group(1))]
                elif t and t.group(1) == "inlineStr":
                    val = "".join(re.findall(r"<t[^>]*>(.*?)</t>", body or "", re.S))
                else:
                    val = v.group(1) if v else ""
                cells[ref] = val
            if cells:
                n = max(col_index(k) for k in cells)
                table.append([cells.get(col_name(i), "") for i in range(n + 1)])
            else:
                table.append([])
        out[name.replace("&amp;", "&")] = table
    return out


def col_index(c):
    n = 0
    for ch in c:
        n = n * 26 + ord(ch) - 64
    return n - 1


def col_name(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def docx_text(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    return " ".join(re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>", x)).replace("&amp;", "&")


def pdf_text(path):
    import zlib
    data = open(path, "rb").read()
    out = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        raw = m.group(1).strip()
        try:
            if raw.endswith(b"~>"):
                raw = base64.a85decode(raw[:-2].replace(b"\n", b"").replace(b"\r", b""))
            raw = zlib.decompress(raw)
        except Exception:
            continue
        for s in re.findall(rb"\((.*?)(?<!\\)\)\s*Tj", raw, re.S):
            out.append(s.replace(rb"\(", b"(").replace(rb"\)", b")").decode("latin-1"))
    return " ".join(out)


def et_of_utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC).astimezone(ET).replace(tzinfo=None)


def nearest100(x):
    return int(math.floor(x / 100.0 + 0.5)) * 100


def recompute(target):
    f = {n: os.path.join(target, n) for n in os.listdir(target)}
    find = lambda pre: [v for k, v in f.items() if os.path.basename(k).startswith(pre)][0]
    reg = xlsx_sheets(find("QRMC_MedAlert_Rule_Register"))
    old2code = {r[2]: r[0] for r in reg["Units"][1:] if len(r) >= 3 and r[0]}
    units = [r[0] for r in reg["Units"][1:] if r and r[0]]
    pilot = []
    for r in reg["Rules"][1:]:
        if len(r) > 5 and r[0] == "MSP26_DUP_OPIOID_PRN" and r[4] == "Live":
            pilot = [u.strip() for u in r[5].split(",")]
    going = [u for u in units if u not in pilot]
    seen, hist = set(), []
    for r in rows(find("QRMC_MedAlertHistory")):
        key = tuple(r.values())
        if key in seen:
            continue
        seen.add(key)
        r["dept"] = old2code.get(r["department"], r["department"])
        r["ts"] = dt.datetime.strptime(r["alert_dttm"], "%Y-%m-%d %H:%M:%S")
        hist.append(r)
    dup = [r for r in hist if r["dept"] in pilot and r["alert_rule_id"] == "MSP26_DUP_OPIOID_PRN"]
    qt = [r for r in hist if r["dept"] in pilot and r["alert_rule_id"] == "MSP26_QT_COMBO"]
    c = sum(r["user_action"] == "Order removed" for r in dup) / len(dup)
    p = sum(r["user_action"] == "Overridden" for r in qt) / len(qt)
    b0, b1 = dt.datetime(2026, 7, 6), dt.datetime(2026, 10, 26)
    bg = rows(find("QRMC_MSP26_BackgroundLog"))
    for r in bg:
        r["ts"] = et_of_utc(r["eval_utc"])
    removed = {r["order_id"] for r in hist if r["user_action"] == "Order removed"}
    dup_o = {r["order_id"] for r in bg if r["rule_id"] == "MSP26_DUP_OPIOID_PRN" and r["ts"] < b1}
    qt_o = {r["order_id"] for r in bg if r["rule_id"] == "MSP26_QT_COMBO" and r["ts"] < b1}
    n_qt = sum(1 for r in bg if r["rule_id"] == "MSP26_QT_COMBO" and b0 <= r["ts"] < b1
               and r["order_id"] not in removed)
    pre = 0.0
    for r in hist:
        if (r["dept"] in going and b0 <= r["ts"] < b1 and r["user_action"] == "Overridden"
                and r["alert_rule_id"] in ("DDI_SEVERE", "DRUG_ALLERGY", "MAX_DOSE")):
            d = (r["order_id"] in dup_o) + (r["interacting_order_id"] in dup_o)
            q = r["order_id"] in qt_o
            pre += 1.0 - (1.0 - c) ** d * (p if q else 1.0)
    adm_b = sum(int(r["admissions"]) for r in rows(find("QRMC_UnitCensus_Daily"))
                if r["department"] in going and "2026-07-06" <= r["census_date"] <= "2026-10-25")
    plan = xlsx_sheets(find("QRMC_FY2027_Inpatient_Volume_Plan"))["Weekly plan"]
    base = dt.date(1899, 12, 30)
    plan_adm = 0
    for r in plan[1:]:
        if len(r) < 3 or not r[0]:
            continue
        wk = base + dt.timedelta(days=int(float(r[0])))
        if dt.date(2027, 1, 4) <= wk < dt.date(2027, 4, 5) and r[1] in going:
            plan_adm += int(float(r[2]))
    scale = plan_adm / adm_b
    call = {"qt_add": p * n_qt * scale, "pre": pre * scale}
    call["net"] = call["qt_add"] - call["pre"]
    # asks
    dept_of = {int(r["alert_id"]): r["dept"] for r in hist}
    per_msg = defaultdict(int)
    for r in hist:
        if r["severity"] == "High" and r["user_action"] == "Overridden":
            per_msg[(r["order_id"], r["alert_dttm"])] += 1
    msg_of = {int(r["alert_id"]): (r["order_id"], r["alert_dttm"]) for r in hist}
    hours = defaultdict(float)
    signed = defaultdict(int)
    q0, q1 = dt.datetime(2026, 7, 1), dt.datetime(2026, 10, 1)
    for r in rows(find("CRV_QueueExport_QRMC")):
        closed, claimed = et_of_utc(r["closed_utc"]), et_of_utc(r["claimed_utc"])
        if not (q0 <= closed < q1):
            continue
        aid = int(r["alert_ref"])
        hours[dept_of[aid]] += (closed - claimed).total_seconds() / 3600.0
        if r["close_status"] == "Signed off":
            h = closed.hour
            sh = "day" if 7 <= h < 15 else ("evening" if 15 <= h < 23 else "night")
            signed[(closed.strftime("%Y-%m"), sh)] += per_msg[msg_of[aid]]
    figs = {"call_net_change": nearest100(call["net"]), "qt_reviews_added": nearest100(call["qt_add"]),
            "current_reviews_removed": nearest100(call["pre"])}
    for u in going:
        figs["desk_hours_%s" % u] = int(math.floor(hours[u] + 0.5))
    for (m, s), v in signed.items():
        figs["signed_off_%s_%s" % (m, s)] = v
    return figs, call, hours


def main(argv):
    target = argv[1] if len(argv) > 1 else os.path.join(TASK, "target")
    golden = argv[2] if len(argv) > 2 else os.path.join(TASK, "golden")
    fj = argv[3] if len(argv) > 3 else os.path.join(HERE, "figures.json")
    bad = []
    figs, call, hours = recompute(target)
    want = json.load(open(fj))["figures"]
    for k, v in want.items():
        if figs.get(k) != v:
            bad.append("figure %s: verifier %s, figures.json %s" % (k, figs.get(k), v))
    for k in figs:
        if k not in want:
            bad.append("figure %s computed by the verifier but absent from figures.json" % k)
    # every shipped file reads back
    names = sorted(os.listdir(target))
    for n in names:
        p = os.path.join(target, n)
        if n.endswith(".csv"):
            assert len(rows(p)) > 0, n
        elif n.endswith(".xlsx"):
            assert xlsx_sheets(p), n
        elif n.endswith(".docx"):
            assert docx_text(p), n
        elif n.endswith(".pdf"):
            t = pdf_text(p)
            if not t:
                bad.append("PDF %s reads back empty" % n)
    sched = pdf_text([os.path.join(target, n) for n in names if n.startswith("Corvane_QRMC_Service_Schedule")][0])
    for phrase in ("4.3 Content changes", "One overridden alert is one review.", "from claiming it to signing it off"):
        if phrase not in sched:
            bad.append("schedule PDF does not read back the phrase %r" % phrase)
    # golden deliverables carry the same figures
    gb = xlsx_sheets(os.path.join(golden, "msp26_review_forecast_q1_2027.xlsx"))
    fc = gb["Forecast"]
    net_row = [r for r in fc if r and r[0] == "Net change in override reviews"][0]
    if int(float(net_row[2])) != figs["call_net_change"]:
        bad.append("workbook net change %s against %s" % (net_row[2], figs["call_net_change"]))
    hrs = {r[0]: int(float(r[2])) for r in gb["Desk hours Q3 2026"][1:] if len(r) > 2 and r[0]}
    for u, v in hrs.items():
        if v != figs["desk_hours_%s" % u]:
            bad.append("workbook desk hours %s %s against %s" % (u, v, figs["desk_hours_%s" % u]))
    so = gb["Signed off by shift"]
    mon = {"July 2026": "2026-07", "August 2026": "2026-08", "September 2026": "2026-09"}
    for r in so[1:]:
        if r and r[0] in mon:
            for s, v in zip(("day", "evening", "night"), r[1:4]):
                if int(float(v)) != figs["signed_off_%s_%s" % (mon[r[0]], s)]:
                    bad.append("workbook signed off %s %s" % (r[0], s))
    memo = docx_text(os.path.join(golden, "msp26_go_live_review_memo.docx"))
    if "about %d more override reviews" % figs["call_net_change"] not in memo:
        bad.append("memo does not carry the net change")
    for k, v in (("qt", figs["qt_reviews_added"]), ("pre", figs["current_reviews_removed"])):
        if str(v) not in memo:
            bad.append("memo does not carry %s %s" % (k, v))
    print("verify: call net %.1f (QT %.1f, removed %.1f), %d figures recomputed on the independent path"
          % (call["net"], call["qt_add"], call["pre"], len(figs)))
    if bad:
        for b in bad:
            print("  FAIL", b)
        return 1
    print("verify: PASS, every figure and every deliverable agrees")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
