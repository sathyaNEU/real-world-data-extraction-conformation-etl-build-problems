"""The independent verifier. It reads target/, figures.json and the golden deliverables and nothing the generator
holds: its own parse of the registers, its own SQL over the telemetry, the platform's local time converted through
the Europe/London zone rules rather than the golden's clock-change constants, a different coincidence measure for
the retired serials (discharge starts within fifteen minutes of an overflow alarm, counted), and its own 12/24 count
written from the procedure's words."""
import csv
import datetime as dt
import json
import os
import re
import sqlite3
import zipfile
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook

LONDON = ZoneInfo("Europe/London")
UTC = dt.timezone.utc
N = [0]


def check(label, cond, detail=""):
    if not cond:
        raise AssertionError("verify %s FAILED %s" % (label, detail))
    N[0] += 1


def utc_epoch(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC).timestamp()


def local_epoch(s):
    return dt.datetime.strptime(s, "%d/%m/%Y %H:%M:%S").replace(tzinfo=LONDON).timestamp()


def stations(tgt):
    wb = load_workbook(os.path.join(tgt, "registers/marsh_wolds_wastewater_assets.xlsx"), read_only=True, data_only=True)
    rows = list(wb["Pumping stations"].iter_rows(values_only=True))
    hdr = rows[0]
    out = {}
    for r in rows[1:]:
        d = dict(zip(hdr, r))
        nums = [float(x) for x in re.findall(r"\d+\.\d+|\d+", d["Wet well internal (m)"])]
        area = np.pi * nums[0] ** 2 / 4 if d["Wet well shape"] == "Circular" else nums[0] * nums[1]
        out[d["Station code"]] = dict(rtu=int(str(d["Telemetry RTU"]).split()[-1]), edm=d["EDM monitor"],
                                      installed=d["EDM installed"], area=area,
                                      band=float(d["Duty pump start (mAOD)"]) - float(d["Duty pump stop (mAOD)"]))
    return out


def delivered(tgt, sts):
    con = sqlite3.connect(os.path.join(tgt, "telemetry/marsh_wolds_sps_telemetry_2026.sqlite"))
    df = pd.read_sql_query("SELECT DISTINCT rtu, pump, state, event_utc FROM pump_event", con)
    con.close()
    df["t"] = df["event_utc"].map(utc_epoch)
    df = df.sort_values(["rtu", "t", "state"]).reset_index(drop=True)
    out = {}
    for code, s in sts.items():
        e = df[df.rtu == s["rtu"]]
        t, p, run = e["t"].to_numpy(), e["pump"].to_numpy(), (e["state"] == "RUN").to_numpy()
        vol = s["area"] * s["band"] * 1000.0
        rates = []
        for k in range(1, len(t) - 1):
            if run[k] and not run[k - 1] and not run[k + 1] and p[k] == p[k + 1]:
                off, on = t[k] - t[k - 1], t[k + 1] - t[k]
                if 0 < off <= 21600 and 0 < on <= 21600:
                    rates.append(vol / on + vol / off)
        out[code] = float(np.median(rates))
    return out


def count_1224(iv):
    """WW-ENV-PR-014 section 3, read word for word: counting begins at the start of the first discharge; any
    discharge in the first 12 hours is one spill; each following 24-hour block containing discharge is one more;
    a full 24-hour block with no discharge ends the count and the next discharge begins a new one."""
    u = merge(iv)
    n, i = 0, 0
    while i < len(u):
        end = u[i][0] + 43200.0
        n += 1
        reach = u[i][1]
        while i < len(u) and u[i][0] < end:
            reach = max(reach, u[i][1])
            i += 1
        while reach > end or (i < len(u) and u[i][0] < end + 86400.0):
            n += 1
            end += 86400.0
            while i < len(u) and u[i][0] < end:
                reach = max(reach, u[i][1])
                i += 1
    return n


def merge(iv):
    out = []
    for a, b in sorted(iv):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def run(tgt, figures_path):
    N[0] = 0
    task = os.path.dirname(tgt)
    figs = json.load(open(figures_path))
    sts = stations(tgt)
    cons = {}
    for r in csv.DictReader(open(os.path.join(tgt, "registers/wastewater_discharge_consents_2026.csv"), encoding="utf-8")):
        cons["SPS" + r["site_id"][-4:]] = dict(permit=r["permit_ref"], pff=float(r["pass_forward_ls"]), name=r["discharge_name"])
    dl = delivered(tgt, sts)
    breach = [c for c in sts if dl[c] < cons[c]["pff"]]
    check("one breach", len(breach) == 1, breach)
    k = breach[0]
    check("call", cons[k]["name"] == figs["call"] and cons[k]["permit"] == figs["call_permit"], (k, figs["call"]))
    check("call delivered", round(dl[k]) == figs["call_delivered_ls"], (dl[k], figs["call_delivered_ls"]))
    check("call pff", round(cons[k]["pff"]) == figs["call_pff_ls"])
    check("call share", round(100 * dl[k] / cons[k]["pff"]) == figs["call_share_of_pff_pct"])
    rest = {c: dl[c] / cons[c]["pff"] for c in sts if c != k}
    tight = min(rest, key=rest.get)
    check("tightest", round(dl[tight]) == figs["tightest_delivered_ls"] and round(cons[tight]["pff"]) == figs["tightest_pff_ls"])

    # event duration monitoring, by the zone rules
    log = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(tgt, "edm/edm_discharge_log_2026.csv"), encoding="utf-8")):
        log[r["monitor_serial"]].append((local_epoch(r["discharge_start"]), local_epoch(r["discharge_end"])))
    status = defaultdict(dict)
    for r in csv.DictReader(open(os.path.join(tgt, "edm/edm_monitor_daily_status_2026.csv"), encoding="utf-8")):
        status[r["monitor_serial"]][r["date"]] = float(r["hours_reporting"])
    devices = list(csv.DictReader(open(os.path.join(tgt, "edm/edm_monitor_list_2027-01-15.csv"), encoding="utf-8")))
    con = sqlite3.connect(os.path.join(tgt, "telemetry/marsh_wolds_sps_telemetry_2026.sqlite"))
    al = defaultdict(list)
    for rtu, a in con.execute("SELECT rtu, raised_utc FROM alarm WHERE alarm = 'OVERFLOW OPERATING'"):
        al[rtu].append(utc_epoch(a))
    con.close()
    site = {s["edm"]: c for c, s in sts.items()}
    for d in devices:
        if d["status"] != "RETIRED":
            continue
        ret = dt.datetime.strptime(d["retired"], "%d/%m/%Y").date()
        cands = [c for c, s in sts.items() if 0 <= (ret - (s["installed"].date() if hasattr(s["installed"], "date")
                                                             else s["installed"])).days <= 10]
        score = {c: sum(1 for a, b in log[d["serial"]] if any(abs(a - x) <= 900 for x in al[sts[c]["rtu"]])) for c in cands}
        best = sorted(score.items(), key=lambda x: -x[1])
        check("retired serial %s mapped" % d["serial"], best[0][1] > 0 and (len(best) == 1 or best[1][1] < 0.6 * best[0][1]), best)
        site[d["serial"]] = best[0][0]
    check("every serial placed", len(site) == len(devices))
    lo = dt.datetime(2026, 1, 1, tzinfo=LONDON).timestamp()
    hi = dt.datetime(2027, 1, 1, tzinfo=LONDON).timestamp()
    lines = {}
    months = {}
    for c in sts:
        iv = [x for s, cc in site.items() if cc == c for x in log.get(s, []) if lo <= x[0] < hi]
        u = merge(iv)
        h = sum(b - a for a, b in u) / 3600.0
        mon = [0.0] * 12
        for a, b in u:
            t = a
            while t < b:
                ld = dt.datetime.fromtimestamp(t, LONDON)
                nxt = dt.datetime(ld.year + (ld.month == 12), ld.month % 12 + 1, 1, tzinfo=LONDON).timestamp()
                e = min(b, nxt)
                mon[ld.month - 1] += (e - t) / 3600.0
                t = e
        days = defaultdict(float)
        for s, cc in site.items():
            if cc == c:
                for d, hrs in status.get(s, {}).items():
                    days[d] = max(days[d], hrs)
        op = 100.0 * sum(days.values()) / ((hi - lo) / 3600.0)
        lines[cons[c]["permit"]] = dict(spills=count_1224(iv), hours="%.1f" % h, operational="%.1f" % op,
                                        delivered=round(dl[c]), pff=round(cons[c]["pff"]), met="No" if c == k else "Yes",
                                        overflow=cons[c]["name"])
        months[c] = mon
    check("year has 8760 hours", round((hi - lo) / 3600.0) == 8760)
    for permit, v in lines.items():
        f = figs["lines"][permit]
        for key in ("spills", "hours", "operational", "delivered", "pff", "met", "overflow"):
            check("line %s %s" % (permit, key), v[key] == f[key], (v[key], f[key]))
    top = max(sts, key=lambda c: sum(months[c]))
    check("chart top", cons[top]["name"] == figs["chart_top_overflow"] and "%.1f" % sum(months[top]) == figs["chart_top_hours"])
    check("call spills and hours", lines[cons[k]["permit"]]["spills"] == figs["call_spills_12_24"]
          and lines[cons[k]["permit"]]["hours"] == figs["call_hours"])

    # the golden deliverables carry the same figures
    gold = os.path.join(task, "golden")
    rows = list(csv.DictReader(open(os.path.join(gold, "overflow_return_lines_2026.csv"), encoding="utf-8")))
    check("csv one line per overflow", len(rows) == len(sts))
    for r in rows:
        v = lines[r["permit_ref"]]
        check("csv %s" % r["permit_ref"], int(r["spills_12_24"]) == v["spills"] and r["discharge_hours"] == v["hours"]
              and r["monitoring_operational_pct"] == v["operational"] and int(r["pass_forward_delivered_ls"]) == v["delivered"]
              and int(r["pass_forward_permitted_ls"]) == v["pff"] and r["met_permit"] == v["met"], (r, v))
    from docx import Document
    doc = Document(os.path.join(gold, "overflow_self_report_2026.docx"))
    text = "\n".join(p.text for p in doc.paragraphs) + "\n".join(c.text for t in doc.tables for row in t.rows for c in row.cells)
    for needle in (figs["call"], figs["call_permit"], "%d litres per second" % figs["call_pff_ls"],
                   "%d litres per second" % figs["call_delivered_ls"]):
        check("docx states %s" % needle, needle in text, needle)
    svg = open(os.path.join(gold, "spill_hours_by_month_2026.svg"), encoding="utf-8").read()
    for c in sts:
        check("svg row %s" % c, cons[c]["permit"] in svg)
    labels = re.findall(r"<!-- (\d+\.\d) -->", svg)
    want = sorted("%.1f" % x for c in sts for x in months[c] if x > 0)
    check("svg cell labels", sorted(labels) == want, (len(labels), len(want)))
    check("svg no writer stamp", "matplotlib" not in svg.lower() and "<metadata>" not in svg)
    with zipfile.ZipFile(os.path.join(gold, "overflow_self_report_2026.docx")) as z:
        core = z.read("docProps/core.xml").decode()
        check("docx author is the company", "python-docx" not in core and "2013-12-23" not in core)
    return N[0]


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    print(run(os.path.join(os.path.dirname(here), "target"), os.path.join(here, "figures.json")))
