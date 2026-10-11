"""Assertions on the shipped pack: input gates, the answer, the ladder, bin margins, rounding edges."""
import datetime as dt
import json
import os
import re
import statistics
import sys
import zipfile

import docx
import openpyxl
import pandas as pd
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E
import world as W

TASK = os.path.dirname(HERE)
T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
n_ok = 0
LOTS = 13
# every graded figure as submission.md blocks 1 and 4 state it, and the unrounded values behind them: the realism
# repairs after reader round 6 move none of them
FROZEN = dict(
    lots=13, modules=325, cost=638625, avail=15, serviceable=12, at_repair=3, quarantine=7,
    lam=298.60587831924823, lam_1=298.6, cover_1=99.1, cover12_1=83.6,
    by_year={2026: 11.585843978150951, 2027: 45.064933292639836, 2028: 44.67490922568835, 2029: 42.88135692728273,
             2030: 40.63767488485243, 2031: 36.082141907792796, 2032: 30.028448006972155, 2033: 23.875543185056756,
             2034: 15.96398905933716, 2035: 7.81103785145221},
    by_year_1={2026: 11.6, 2027: 45.1, 2028: 44.7, 2029: 42.9, 2030: 40.6, 2031: 36.1, 2032: 30.0, 2033: 23.9, 2034: 16.0,
               2035: 7.8},
    by_region={"Central": 54.70509663935361, "North": 117.47403097737761, "South": 126.42675070251525},
    by_region_1={"North": 117.5, "Central": 54.7, "South": 126.4},
    in_service={2027: 1163, 2028: 1094, 2029: 973, 2030: 884, 2031: 783, 2032: 695, 2033: 564, 2034: 373, 2035: 201},
    settings_1={8: 0.0, 9: 0.0, 10: 2.6, 11: 32.2, 12: 83.6, 13: 99.1, 14: 100.0, 15: 100.0, 16: 100.0, 17: 100.0, 18: 100.0,
             19: 100.0, 20: 100.0, 21: 100.0, 22: 100.0},
    n_fail=210, counts=[15, 49, 68, 66, 12])


FAILS = [] if os.environ.get("CHECKS_ALL") else None


def ok(cond, msg):
    global n_ok
    if not cond:
        if FAILS is None:
            raise AssertionError(msg)
        FAILS.append(msg)
        return
    n_ok += 1


def edge(v):
    return abs((v * 10) % 1 - 0.5)


def main():
    files = sorted(os.listdir(T))
    ok(len(files) >= 10, "10 or more input files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "3 or more formats")
    wo = pd.read_csv(os.path.join(T, E.F["wo"]), dtype=str)
    ok(len(wo) >= 25000, "work-order spine has 25,000 or more rows (%d)" % len(wo))
    ok(wo["reported_date"].min() >= "2021-01-01", "no work order before the EAM go-live")
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok(len(meta["distractors"]) >= 2 and all(d in files for d in meta["distractors"]), "two or more distractors on disk")
    for f in files:
        ok(not any(w in f.lower() for w in ("answer", "golden", "trap", "clean", "_v2", "test_")), "file name %s carries no author noun" % f)

    s = E.solve(T)
    ok(s["lots"] == LOTS, "answer is %d lots (%d)" % (LOTS, s["lots"]))
    ok(s["cover"] >= W.COVER > s["settings"][s["lots"] - 1]["cover"], "the answer clears 95 per cent and one lot fewer does not")
    ok(min(W.SETTINGS) <= s["lots"] - 3 and max(W.SETTINGS) >= s["lots"] + 5, "the asked settings run well either side of the answer")
    lo, hi = s["lam"], s["lam"]
    while E.lots_needed(lo, s["avail"]) == s["lots"]:
        lo -= 0.05
    while E.lots_needed(hi, s["avail"]) == s["lots"]:
        hi += 0.05
    ok((s["lam"] - lo) / s["lam"] >= 0.03 and (hi - s["lam"]) / s["lam"] >= 0.03,
       "expected failures sit at least 3 per cent inside the answer's lot bin (%.1f < %.1f < %.1f)" % (lo, s["lam"], hi))
    vals = [s["lam"]] + list(s["by_year"].values()) + list(s["by_region"].values()) + [
        100 * v["cover"] for v in s["settings"].values() if 0.05 < 100 * v["cover"] < 99.95]
    for v in vals:
        ok(edge(v) >= 0.05, "figure %.4f at least 0.05 of a tenth clear of its rounding edge" % v)
    ok(abs(sum(s["by_year"].values()) - s["lam"]) < 1e-6, "years add to the total")
    ok(abs(sum(s["by_region"].values()) - s["lam"]) < 1e-6, "regions add to the total")
    ok(list(s["in_service"].values()) == sorted(s["in_service"].values(), reverse=True), "supported relays fall year on year")

    r, avail = E.rungs(T)
    ans = r["ANSWER"][0]
    for k, (v, l) in r.items():
        if k == "ANSWER":
            continue
        ok(l != s["lots"], "rung %s lands on %d lots, not the answer" % (k, l))
    ok(r["window_no_renewal"][1] >= s["lots"] + 4, "keeping today's module in every month is at least four lots high")
    ok(r["window_no_renewal"][0] >= 1.25 * ans, "and at least 25 per cent high")
    ok(r["install_renewal"][0] <= 0.88 * ans, "exposure from fitting rather than the go-live is at least 12 per cent low")
    ok(r["relay_age_window_no_renewal"][0] <= 0.88 * ans, "relay age in place of module age is at least 12 per cent low")
    ok(r["trailing_rate"][0] <= 0.80 * ans, "the trailing twelve-month rate is at least 20 per cent low")
    # staged schemes and the superseded plan show in the supported-relay column
    reg0, wo0, hist0, subs0, stock0, plan0 = E.load(T)
    fl0 = E.fleet(reg0)
    in25 = E.in_service_jan1(fl0, plan0["2025 plan (superseded)"])
    ok(sum(in25[y] != s["in_service"][y] for y in in25) >= 6, "the 2025 plan misstates the supported relays in most years")
    p26 = plan0["Approved 2026"]
    first = {sub: min((w or E.month_add(W.PROGRAMME_END, 1)) for _, w in rows) for sub, rows in p26.items()}
    live = fl0[fl0["status"] == "IN SERVICE"]
    by_station = {y: int(sum(1 for sub in live["sub_code"] if sub in first and first[sub] > dt.date(y, 1, 1))) for y in range(2027, 2036)}
    ok(sum(by_station[y] != s["in_service"][y] for y in by_station) >= 5, "reading a staged scheme by station misstates the supported relays")
    # every module counted in the rates is in the history the procedure names, and the failures tie to it
    f = E.failures(wo0, fl0, hist0)
    ok(len(f) == s["n_fail"] and f["fitted"].notna().all(), "every failure ties to the module it removed")
    ok((hist0["removal_reason"] == "FAILED").sum() >= len(f), "the history records a removal for every failure")
    realism(reg0, wo0, hist0, subs0, plan0, f)
    repair3(reg0, wo0, hist0, subs0, plan0, f, s)
    no_move(s)
    cleanup(reg0, wo0, hist0, subs0, plan0, f, s)
    if FAILS:
        print("CHECKS FAIL", len(FAILS))
        for m in FAILS:
            print("  FAIL", m)
        sys.exit(1)
    print("CHECKS PASS", n_ok)



def _text(path):
    """the words a reader sees in a shipped file"""
    if path.endswith(".docx"):
        d = docx.Document(path)
        out = [p.text for p in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                out += [c.text for c in row.cells]
        for sec in d.sections:
            out += [p.text for p in sec.footer.paragraphs]
        return "\n".join(out)
    if path.endswith(".pdf"):
        return "\n".join(pg.extract_text() for pg in PdfReader(path).pages)
    if path.endswith(".xlsx"):
        wb = openpyxl.load_workbook(path, data_only=True)
        return "\n".join(" ".join(str(v) for v in row if v is not None) for ws in wb for row in ws.iter_rows(values_only=True)) + \
            "\n" + " ".join(wb.sheetnames)
    return open(path, encoding="utf-8").read()


def realism(reg, wo, hist, subs, plan, f):
    """the operating texture the pack has to carry, each piece asserted so a later retune cannot strip it out"""
    d = lambda x: dt.date.fromisoformat(x) if x else None
    wo_by = wo.set_index("wo_number")
    # failure path: some spares fitted on a follow-up work order raised the same or the next working day, numbered
    # after the failure, carrying no failed component, and fitted no later than the first day of the next month
    eam = hist[hist["record_source"] == "EAM"]
    sep = 0
    for a, fit, fwo in zip(eam["asset_id"], eam["fitted"], eam["fitting_wo"]):
        prev = hist[(hist["asset_id"] == a) & hist["removed"].map(lambda x: x is not None) & (hist["removal_reason"] == "FAILED")]
        prev = prev[prev["removed"] <= fit].sort_values("removed").iloc[-1]
        nxt = E.month_add(dt.date(prev["removed"].year, prev["removed"].month, 1), 1)
        ok(prev["removed"] <= fit <= nxt, "replacement on %s fitted between the removal and the next first of the month" % a)
        if fwo != prev["removal_wo"]:
            sep += 1
            w = wo_by.loc[fwo]
            ok(fwo > prev["removal_wo"] and w["work_type"] == "CM" and w["failed_component"] == "" and
               (d(w["reported_date"]) - prev["removed"]).days <= 4, "follow-up fitting %s raised after its failure, no component" % fwo)
    ok(sep >= 15, "%d spares fitted on a separate follow-up work order" % sep)
    ok(len(f) == (hist["removal_reason"] == "FAILED").sum(), "every 5.1 failure is one FAILED removal")
    # RMA register: from the 2015 service bulletin, boxes of two, references blank or mistyped, skewed receipt lags,
    # a module removed before go-live received in January 2021
    wb = openpyxl.load_workbook(os.path.join(T, "veldtek_rma_log_vpr340_psu.xlsx"))
    rows = list(wb.active.iter_rows(min_row=2, values_only=True))
    rec = [r[5].date() for r in rows]
    ok(min(rec) < dt.date(2015, 12, 31) and sum(x < E.month_add(dt.date(2021, 1, 1), 0) for x in rec) >= 50,
       "the RMA register runs from 2015 (%d receipts before go-live)" % sum(x < dt.date(2021, 1, 1) for x in rec))
    ok(sum("SB-15-02" in str(r[6]) for r in rows) >= 30, "the service-bulletin returns are in the register")
    created = re.search(r"<dcterms:created[^>]*>(\d{4}-\d{2}-\d{2})", zipfile.ZipFile(
        os.path.join(T, "veldtek_rma_log_vpr340_psu.xlsx")).read("docProps/core.xml").decode()).group(1)
    ok(created < min(rec).isoformat(), "the register workbook was created before its first receipt")
    log = wo[(wo["work_type"] == "LOG") & (wo["failed_component"] == "PSU")]
    refs = [str(r[4]) for r in rows if r[4]]
    pairs = sum(1 for w in set(log["wo_number"]) if refs.count(w) == 2)
    ok(pairs >= 5, "%d logistics work orders ship two modules in one box" % pairs)
    blank = sum(1 for r in rows if not r[4] and r[5].year >= 2021)
    odd = sum(1 for r in rows if r[4] and r[5].year >= 2021 and str(r[4]) not in set(log["wo_number"]))
    ok(blank >= 3 and odd >= 3, "references blank (%d) or not a logistics work order (%d) after go-live" % (blank, odd))
    serials = set(hist["serial_no"])
    first_fit = {}
    for sn_, fit_ in zip(hist["serial_no"], hist["fitted"]):
        first_fit[sn_] = min(fit_, first_fit.get(sn_, fit_))
    held = [r for r in rows if r[5].year == 2021 and r[5].month == 1 and r[4] and not str(r[4]).startswith(("WO", "SB"))
            and str(r[4]).isdigit()]
    ok(all(r[2] not in serials or first_fit[r[2]] > r[5].date() for r in held),
       "%d legacy returns held over the cutover, none from a relay in service at go-live" % len(held))
    removed = {}
    for s_, rm, why in zip(hist["serial_no"], hist["removed"], hist["removal_reason"]):
        if why == "FAILED":
            removed.setdefault(s_, []).append(rm)
    lag = []
    for r in rows:
        prior = [x for x in removed.get(r[2], []) if x <= r[5].date()]
        if prior:
            lag.append((r[5].date() - max(prior)).days)
    ok(statistics.median(lag) <= 25 and max(lag) >= 90 and statistics.mean(lag) > statistics.median(lag),
       "removal-to-receipt days skewed (median %s, mean %.0f, max %s)" % (statistics.median(lag), statistics.mean(lag), max(lag)))
    turn = [(r[7] - r[5]).days for r in rows if r[7] is not None]
    ok(min(turn) <= 15 and max(turn) >= 80, "repair turnaround from %d to %d days" % (min(turn), max(turn)))
    # master data: year-only legacy dates as 1 July, units held in stores before installation, the feeder identity
    ok(sum(str(x).endswith("-07-01") for x in reg["install_date"]) >= 30, "legacy install dates held as 1 July")
    ok(sum(1 for x, s_ in zip(hist["fitted_date"], hist["record_source"]) if s_ == "GO-LIVE LOAD" and x.endswith("-07-01")) >= 5,
       "legacy fitted dates held as 1 July")
    pat = {"VPR-340": r"V340-(\d\d)-", "VPR-220": r"V220-(\d\d)-", "NX-9": r"N9-(\d\d)-", "NX-5": r"N5-(\d\d)-",
           "AT-7": r"AW7(\d\d)", "KDR-30": r"K30(\d\d)", "RT-400": r"AW4(\d\d)", "RT-600": r"AW6(\d\d)"}
    gap = []
    for mdl, sn, inst in zip(reg["model"], reg["serial_no"], reg["install_date"]):
        yy = int(re.match(pat[mdl], sn).group(1))
        gap.append(int(str(inst)[:4]) - (1900 + yy if yy > 50 else 2000 + yy))
    ok(min(gap) >= 0 and max(gap) <= 3 and sum(g >= 2 for g in gap) >= 20,
       "serial year 0 to 3 years before installation (%d at 2 or 3)" % sum(g >= 2 for g in gap))
    trips = pd.read_csv(os.path.join(T, "feeder_relay_operations_2025.csv"))
    ok((trips["trip_operations"] == trips["protection_trips"] + trips["supervisory_trips"]).all()
       and (trips["protection_trips"] == trips["reclose_attempts"] + trips["lockouts"]).all()
       and (trips["successful_recloses"] <= trips["reclose_attempts"]).all()
       and (trips[trips["reclosing"] == "OFF"]["reclose_attempts"] == 0).all(), "the operations export closes on every feeder")
    ok((trips["supervisory_trips"] > 0).sum() >= 30, "%d feeders with supervisory trips" % (trips["supervisory_trips"] > 0).sum())
    # program: spare bays and VPR-220 feeders inside scheme bay lists, a 2025 plan that differs, every live VPR-340 bay
    # in exactly one approved row
    p26, p25 = plan["Approved 2026"], plan["2025 plan (superseded)"]
    live = reg[reg["status"] == "IN SERVICE"]
    occupied = set(zip(reg["sub_code"], reg["bay"]))
    spare = mixed = 0
    for sub, rws in p26.items():
        listed = {b for rngs, _ in rws for lo, hi in rngs for b in range(lo, hi + 1)}
        spare += sum((sub, "F%02d" % b) not in occupied for b in listed)
        models = set(live[(live["sub_code"] == sub) & live["bay"].isin({"F%02d" % b for b in listed})]["model"])
        mixed += {"VPR-340", "VPR-220"} <= models
    ok(spare >= 3 and mixed >= 3, "approved schemes take in %d spare bays and %d stations mixing VPR-220 and VPR-340" % (spare, mixed))
    v340 = live[live["model"] == "VPR-340"]
    for sub, bay in zip(v340["sub_code"], v340["bay"]):
        n = sum(any(lo <= int(bay[1:]) <= hi for lo, hi in rngs) for rngs, _ in p26.get(sub, []))
        ok(n == 1, "VPR-340 %s %s sits in one approved row" % (sub, bay))
    ok(len(set(p26) ^ set(p25)) >= 10, "the 2025 plan lists a different station set")
    wbp = openpyxl.load_workbook(os.path.join(T, E.F["prog"]))
    sc26 = {r[2]: r[6] for r in wbp["Approved 2026"].iter_rows(min_row=4, values_only=True) if r[2] and r[1] is None}
    sc25 = {r[2]: r[6] for r in wbp["2025 plan (superseded)"].iter_rows(min_row=4, values_only=True) if r[2]}
    both = set(sc26) & set(sc25)
    ok(0.2 <= sum(sc26[k] != sc25[k] for k in both) / len(both) <= 0.8, "scope text differs between versions in places")
    notes = " ".join(str(r[0]) for r in wbp["Notes"].iter_rows(values_only=True))
    ok("Each stage replaces the bays it lists" in notes and "booked from the 1st of its commissioning month" in notes
       and "out of service from that day" in notes, "the program notes pin staging and the outage day")
    ok("first day of the commissioning month" not in notes and "keep their existing protection" not in notes
       and "including spare bays" not in notes, "the notes read as program management notes")
    # maintenance distractor derived from the PM work orders, with formulas
    import distract as Q
    wo_d = wo.copy()
    wo_d["reported_date"] = wo_d["reported_date"].map(d)
    wo_d["completed_date"] = wo_d["completed_date"].map(d)
    cnt = Q.compliance_counts(reg, subs, wo_d)
    wc = openpyxl.load_workbook(os.path.join(T, "pc_relay_maintenance_compliance_2025.xlsx"))
    ws = wc.active
    body = [r for r in ws.iter_rows(min_row=4, values_only=True) if r[0] and r[0] != "All models"]
    ok(len(body) == len(cnt), "one compliance row per model and region tested in 2025")
    exp = {k: list(v) for k, v in cnt.items()}
    adj = Q.adjustments(exp)
    for r in body:
        ok(exp[(r[0], r[1])] == list(r[2:6]) and bool(r[7]) == ((r[0], r[1]) in adj),
           "compliance %s %s recomputes from the PM work orders, with any correction noted" % (r[0], r[1]))
    ok(len(adj) == 2 and all(exp[k] != list(cnt[k]) for k in adj), "two corrections made by hand, each noted against its row")
    ok(all(str(c.value).startswith("=") for c in ws["G"][3:]), "on-time per cent is a formula")
    pm = wo[(wo["work_type"] == "PM") & (wo["status"] != "CANC") & wo["description"].str.contains("relay test|RELAY MAINT", case=False)]
    kind = dict(zip(subs["sub_code"], subs["station_type"]))
    dev = []
    for (a, sub), g in pm.groupby(["asset_id", "sub_code"]):
        ds = sorted(d(x) for x in g["reported_date"])
        dev += [(y - x).days - (730 if kind[sub] == "TS" else 1095) for x, y in zip(ds, ds[1:])]
    ok(statistics.pstdev(dev) > 15 and sum(x > 60 for x in dev) >= 20,
       "relay test intervals slip past the nominal interval (sd %.0f days, %d over 60)" % (statistics.pstdev(dev), sum(x > 60 for x in dev)))
    # crew text and the extract's make-up
    fdesc = wo[wo["wo_number"].isin(set(hist["removal_wo"][hist["removal_reason"] == "FAILED"]))]["description"]
    ok(fdesc.nunique() >= 0.95 * len(fdesc), "failure write-ups are the crews' own (%d distinct of %d)" % (fdesc.nunique(), len(fdesc)))
    ok(wo["description"].nunique() >= 5000, "%d distinct descriptions" % wo["description"].nunique())
    ok(not wo["description"].str.contains(r"\bu/s\b|healthy", case=False).any(), "no UK crew terms")
    back = {}
    for r in rows:
        if r[7] is not None:
            back.setdefault(r[2], []).append(r[7].date())
    rep = 0
    for s_, fit, fw in zip(hist["serial_no"], hist["fitted"], hist["fitting_wo"]):
        if fw and any(x < fit for x in back.get(s_, [])):
            rep += 1
            t = wo_by.loc[fw, "description"].lower()
            ok(not re.search(r"\bnew (module|psu|unit|power supply|p/s)", t), "repaired %s not written up as new" % s_)
    ok(rep >= 10, "%d repaired modules fitted again" % rep)
    ok(len(wo) >= 25000 and (wo["work_type"] == "INSP").mean() <= 0.25 and (wo["asset_id"] == "").mean() <= 0.2,
       "extract over 25,000 rows, inspections %.0f%%, blank asset %.0f%%" % (100 * (wo["work_type"] == "INSP").mean(),
                                                                            100 * (wo["asset_id"] == "").mean()))
    other = set(wo["asset_id"]) - set(reg["asset_id"]) - {""}
    ok(len(other) >= 1000 and not other & set(reg["asset_id"]), "%d station DC, breaker and VT assets carry their own numbers" % len(other))
    # documents: Canadian spelling, the letter date, repair terms, the procedure's filing rule and definitions
    for fn in sorted(os.listdir(T)):
        txt = _text(os.path.join(T, fn))
        ok(not re.search(r"programme|organis|reorganis|minimis|prioritis|analys(e|ing)\b", txt, re.I), "Canadian spelling in %s" % fn)
    eol = _text(os.path.join(T, "veldtek_vpr340_eol_notice.pdf"))
    ok("August 20, 2026" in eol and "electrolytic capacitors and any failed input fuse" in " ".join(eol.split())
       and not re.search(r"\bfans?\b", eol, re.I), "the notice's date and a relay PSU's repair terms")
    ok(not any(re.search(r"\bfans?\b", str(r[8]), re.I) for r in rows), "no fan in a PSU repair note")
    proc = _text(os.path.join(T, "AM-PC-014_obsolete_spares_final_buy.docx"))
    ok("by year" not in proc and "Monthly failure rate" in proc and "Module age" in proc, "8.3 files, section 3 defines")
    ok(not re.search(r"ageing|aging|renewed|starts again|replacement module", proc, re.I), "no sentence on ageing or renewal")
    dic = _text(os.path.join(T, "eam_extract_dictionary.txt"))
    for col in ["item_code", "item_no", "item_description", "location", "bin", "stock_state", "uom", "quantity", "unit_cost_cad",
                "1 July", "KALLISON", "removed_to", "disposal_ref", "CR-2024-031"]:
        ok(col in dic, "dictionary documents %s" % col)
    ok("\nGeneral\n" not in dic.replace("\r", ""), "the dictionary carries the reporting service's notes, not a caveat list")
    # containers: each workbook saved by its own Excel, Word's ids irregular, the PDF stamped to the second
    geo = set()
    for fn in ("protection_renewal_program_2026.xlsx", "veldtek_rma_log_vpr340_psu.xlsx", "pc_relay_maintenance_compliance_2025.xlsx"):
        x = zipfile.ZipFile(os.path.join(T, fn)).read("xl/workbook.xml").decode()
        geo.add((re.search(r'rupBuild="(\d+)"', x).group(1), re.search(r"<workbookView [^>]*", x).group(0)[:80]))
    ok(len(geo) == 3, "three workbooks, three Excel builds and windows")
    x = zipfile.ZipFile(os.path.join(T, "AM-PC-014_obsolete_spares_final_buy.docx")).read("word/document.xml").decode()
    tids = re.findall(r'w14:textId="([0-9A-F]{8})"', x)
    ok("77777777" not in tids and len(set(tids)) == len(tids), "text ids are Word's own")
    runs = [len(list(g)) for _, g in __import__("itertools").groupby(re.findall(r'<w:p [^>]*w:rsidR="([0-9A-F]+)"', x))]
    ok(len(set(runs)) >= 5, "revision sessions run in blocks of %d different lengths" % len(set(runs)))
    info = PdfReader(os.path.join(T, "veldtek_vpr340_eol_notice.pdf"), strict=True).metadata
    ok(not info["/CreationDate"][14:16] == "00", "PDF creation stamped to the second")
    raw = open(os.path.join(T, "veldtek_vpr340_eol_notice.pdf"), "rb").read()
    ok(info["/Producer"].startswith("LibreOffice") and info["/Creator"] == "Writer" and b"Microsoft" not in raw
       and b"/DocChecksum" in raw, "the notice is LibreOffice Writer's own export")


def repair3(reg, wo, hist, subs, plan, f, s):
    """the third repair's texture, and the claims that it moves no graded figure"""
    import shutil
    import tempfile
    d = lambda x: dt.date.fromisoformat(x) if x else None
    # P1, P2: one period for failures and exposure; the last month of the program period counted
    proc = " ".join(_text(os.path.join(T, "AM-PC-014_obsolete_spares_final_buy.docx")).split())
    ok("Failures and module-years are both counted over the period the work-order history covers" in proc,
       "5.3 counts failures and module-years over one period")
    ok("counted for every month up to and including the last month of the period" in proc and "December 2035" not in proc,
       "4.2 counts the last month of the program period")
    ok("IA-25-09" in proc and "First issue" in proc and proc.count("Prepared") == 1 and "Revision history" in proc,
       "AM-PC-014 carries its revision history and approval")
    # R1: young modules fail, at a rate an electronic power supply shows, and repaired modules fail early now and then
    ok(s["counts"][0] >= 8 and 0.003 <= s["rates"][0] <= 0.010,
       "0-9 band: %d failures, %.4f per module-year" % (s["counts"][0], s["rates"][0]))
    ok(int((f["age"] < 6).sum()) >= 3, "%d failures of modules under six years old" % int((f["age"] < 6).sum()))
    rows = list(openpyxl.load_workbook(os.path.join(T, "veldtek_rma_log_vpr340_psu.xlsx")).active.iter_rows(min_row=2, values_only=True))
    back = {}
    for r in rows:
        if r[7] is not None:
            back.setdefault(r[2], []).append(r[7].date())
    early = [(sn, fit, rem) for sn, fit, rem, why in zip(hist["serial_no"], hist["fitted"], hist["removed"], hist["removal_reason"])
             if why == "FAILED" and any(b < fit for b in back.get(sn, [])) and (rem - fit).days < 250]
    warranty = [r for r in rows if r[8] and str(r[8]).startswith("Warranty")]
    ok(len(early) >= 2 and len(warranty) >= 1
       and all(any(q[2] == w[2] and q[7] is not None and q[7] < w[5] for q in rows) for w in warranty),
       "%d repaired modules failed within eight months of refit, %d back at Veldtek under warranty" % (len(early), len(warranty)))
    # repaired modules back from Veldtek and not fitted since are on the shelf, inside the serviceable count
    stock0 = pd.read_csv(os.path.join(T, E.F["stock"]), dtype={"item_no": str})
    last_fit = {}
    for sn_, fit_ in zip(hist["serial_no"], hist["fitted"]):
        last_fit[sn_] = max(fit_, last_fit.get(sn_, fit_))
    shelf = sum(1 for r in rows if r[7] is not None and r[7].date() >= W.MIGRATION
                and r[2] not in [q[2] for q in rows if q[5] > r[5]] and last_fit.get(r[2], dt.date(1900, 1, 1)) < r[7].date())
    ok(shelf <= s["serviceable"], "%d repaired modules on the shelf at the count, within the %d serviceable" % (shelf, s["serviceable"]))
    # R2: modules left in relays retired by a rebuild went for scrap with them, under the e-waste manifest in the LOG
    # work order for that rebuild; none comes back, and the stock is untouched
    scrap = hist[hist["removal_reason"] == "ASSET RETIRED"]
    ok(len(scrap) >= 20 and (scrap["removed_to"] == "SCRAP").all() and (scrap["disposal_ref"] != "").all(),
       "%d modules scrapped with their retired relays, each with a manifest" % len(scrap))
    a2s = dict(zip(reg["asset_id"], reg["sub_code"]))
    for man, g in scrap.groupby("disposal_ref"):
        lw = wo[(wo["work_type"] == "LOG") & wo["description"].str.contains(man, regex=False)]
        n = re.search(r"(\d+) VPR-340", lw["description"].iloc[0], re.I) if len(lw) == 1 else None
        ok(len(lw) == 1 and lw["sub_code"].iloc[0] == a2s[g["asset_id"].iloc[0]] and n is not None and int(n.group(1)) == len(g),
           "manifest %s: one LOG work order at the station listing its %d relays" % (man, len(g)))
        later = hist[hist["serial_no"].isin(set(g["serial_no"])) & (hist["fitted"] > g["removed"].max())]
        ok(len(later) == 0 and not any(r[2] in set(g["serial_no"]) and r[5].date() > g["removed"].min() for r in rows),
           "no module scrapped under %s is seen again" % man)
    fail = hist[hist["removal_reason"] == "FAILED"]
    cur = dict(zip(subs["sub_code"], subs["region"]))
    leg = dict(zip(subs["sub_code"], subs["legacy_region"]))
    store = {"North": "NORTH DEPOT", "Central": "CENTRAL STORES", "South": "SOUTH DEPOT"}
    lstore = {"Lakeshore": "NORTH DEPOT", "Ridge": "CENTRAL STORES", "Valley": "CENTRAL STORES", "Harbour": "SOUTH DEPOT"}
    ok(all(to == (store[cur[a2s[a]]] if rm >= W.REORG else lstore[leg[a2s[a]]]) + " RETURNS"
           for a, rm, to in zip(fail["asset_id"], fail["removed"], fail["removed_to"])),
       "failed modules go back to the store serving the station's region of the day")
    # R6: the residue an EAM carries, none of it on a graded path
    after = wo[[d(x) >= W.REORG for x in wo["reported_date"]]]
    old = after[after["region"].isin(["Lakeshore", "Ridge", "Valley", "Harbour"])]
    ok(len(old) >= 20 and all((wt == "PM" and d(x) < W.PM_MASTER_UPDATE) or (wt != "PM" and (d(x) - W.REORG).days < 21)
                              for wt, x in zip(old["work_type"], old["reported_date"])),
       "%d work orders raised on the old region and crew codes after the change" % len(old))
    rd = list(wo["reported_date"])
    back_steps = sum(1 for a, b in zip(rd, rd[1:]) if b < a)
    ok(list(wo["wo_number"]) == sorted(wo["wo_number"]) and back_steps >= 50,
       "%d work orders entered after later-dated ones" % back_steps)
    new = reg[[d(x) >= W.MIGRATION for x in reg["install_date"]]].sort_values("asset_id")
    inv = sum(1 for a, b in zip(new["install_date"], list(new["install_date"])[1:]) if b < a)
    ok(inv >= 10, "%d post-go-live asset numbers out of install-date order" % inv)
    bay_of = dict(zip(reg["asset_id"], reg["bay"]))
    styled = wrong = 0
    for a, t, wt in zip(wo["asset_id"], wo["description"], wo["work_type"]):
        if wt not in ("CM", "EM") or a not in bay_of or not bay_of[a].startswith("F"):
            continue
        for m in re.finditer(r"\b(?:F-?|FDR ?|feeder )(\d+)\b", t, re.I):
            styled += not re.fullmatch(r"F\d\d", m.group(0))
            wrong += int(m.group(1)) != int(bay_of[a][1:])
    ok(styled >= 50 and 1 <= wrong <= 20, "crew bay references: %d written their own way, %d on the wrong bay" % (styled, wrong))
    # R7: late-2026 commissionings on the approved sheet, 2026 entries on the 2025 plan
    wbp = openpyxl.load_workbook(os.path.join(T, E.F["prog"]))
    c26 = [r[7] for r in wbp["Approved 2026"].iter_rows(min_row=4, values_only=True) if isinstance(r[7], dt.datetime)]
    c25 = [r[7] for r in wbp["2025 plan (superseded)"].iter_rows(min_row=4, values_only=True) if isinstance(r[7], dt.datetime)]
    ok(1 <= sum(x.year == 2026 for x in c26) <= 8 and min(c26) >= dt.datetime(2026, 10, 1),
       "%d approved schemes commission in late 2026" % sum(x.year == 2026 for x in c26))
    ok(sum(x.year == 2026 for x in c25) >= 2, "%d 2026 entries on the 2025 plan" % sum(x.year == 2026 for x in c25))
    # R13: the bulletin's returns are its date codes
    sb = [r for r in rows if "SB-15-02" in str(r[6])]
    ok(len(sb) >= 20 and all(88 <= int(r[2][5:7]) <= 97 for r in sb), "%d SB-15-02 returns, all date codes 97 or earlier" % len(sb))
    # R14: Ontario names, distribution stations at a distribution station's size
    live = reg[(reg["status"] == "IN SERVICE") & reg["bay"].str.startswith("F")]
    kind = dict(zip(subs["sub_code"], subs["station_type"]))
    nfeed = live.groupby("sub_code").size()
    ok(max(n for sc, n in nfeed.items() if kind[sc] == "DS") <= W.DS_FEEDERS_MAX, "distribution stations carry 12 feeders at most")
    ok(not any(re.search(r"bury|worth|^(Stag|Owl|Otter|Wolf|Fox|Deer|Elk|Crow|Raven|Wren|Heron|Swan|Lark|Fish)", n)
               for n in subs["sub_name"]), "no English-village or animal station names")
    # R9, R10: exports as the systems write them
    for fn in sorted(os.listdir(T)):
        if fn.endswith((".csv", ".txt")):
            raw = open(os.path.join(T, fn), "rb").read()
            ok(raw.count(b"\r\n") == raw.count(b"\n") > 0, "%s has Windows line endings" % fn)
    ok(wo["labour_hours"].str.fullmatch(r"\d+\.\d\d").all(), "labour hours to two decimals")
    stock = pd.read_csv(os.path.join(T, E.F["stock"]), dtype=str)
    ok(stock["unit_cost_cad"].str.fullmatch(r"\d+\.\d\d").all(), "unit costs to the cent")
    z = zipfile.ZipFile(os.path.join(T, "pc_relay_maintenance_compliance_2025.xlsx"))
    sheet = z.read("xl/worksheets/sheet1.xml").decode()
    chain = re.findall(r'<c r="([A-Z]+\d+)"', z.read("xl/calcChain.xml").decode())
    ok(chain == re.findall(r'<c r="([A-Z]+\d+)"[^>]*><f>', sheet), "the calculation chain lists every formula cell")
    import postprocess as P
    vals = re.findall(r"<v>(-?[\d.]+(?:E[-+]\d+)?)</v>", sheet)
    ok(vals and all(v == P._num(v) for v in vals) and any(len(v) >= 18 for v in vals), "cached values as Excel writes doubles")
    zd = zipfile.ZipFile(os.path.join(T, "AM-PC-014_obsolete_spares_final_buy.docx"))
    x = zd.read("word/document.xml").decode()
    rs_set = re.findall(r'<w:rsid w:val="([0-9A-F]+)"', zd.read("word/settings.xml").decode())
    rs_body = set(re.findall(r'w:rsidR="([0-9A-F]+)"', x))
    ok(len(rs_set) >= 15 and len(rs_body) >= 10, "%d editing sessions, %d on body paragraphs" % (len(rs_set), len(rs_body)))
    app = zd.read("docProps/app.xml").decode()
    words = int(re.search(r"<Words>(\d+)</Words>", app).group(1))
    split = len(" ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", x)).split())
    ok(words != split and abs(words - split) < 0.1 * split, "word count %d measured on the document (split %d)" % (words, split))
    # crew text: people's own habits
    fdesc = wo[wo["wo_number"].isin(set(hist["removal_wo"][hist["removal_reason"] == "FAILED"]))]["description"]
    bare = [re.sub(r"PS02-\d\d-\d+|WO\d+", "", t) for t in fdesc]
    low = sum(t == t.lower() for t in bare) / len(bare)
    caps = sum(t == t.upper() for t in bare) / len(bare)
    ok(0.08 <= low <= 0.35 and 0.08 <= caps <= 0.35, "failure write-ups %.0f%% lower case, %.0f%% capitals" % (100 * low, 100 * caps))
    clause = {}
    for t in fdesc:
        for p in re.split(r"\. |, | - |; | / ", t):
            p = re.sub(r"F-?\d+|FDR ?\d+|feeder \d+|PS02-\d\d-\d+", "#", p.strip().strip(".").lower())
            clause[p] = clause.get(p, 0) + 1
    top = max(clause.values())
    common = sum(1 for v in clause.values() if v >= 11)
    ok(top <= 0.13 * len(fdesc) and common <= 15,
       "no clause in more than 13 per cent of failure write-ups (most %d of %d), %d clauses recur 11 times or more"
       % (top, len(fdesc), common))
    # the claims that none of this moves a graded figure: the answer from a work-order extract re-sorted by date, with
    # every region and crew code set to the station's current one, is the same answer
    tmp = tempfile.mkdtemp()
    try:
        for fn in os.listdir(T):
            shutil.copy(os.path.join(T, fn), tmp)
        w2 = pd.read_csv(os.path.join(T, E.F["wo"]), dtype=str, keep_default_na=False)
        w2["region"] = [cur.get(sc, rg) for sc, rg in zip(w2["sub_code"], w2["region"])]
        w2["crew"] = ""
        w2.sort_values(["reported_date", "wo_number"]).to_csv(os.path.join(tmp, E.F["wo"]), index=False)
        s2 = E.solve(tmp)
        ok(all(abs(s2[k] - s[k]) < 1e-9 for k in ("lam", "avail", "lots")) and s2["by_region"] == s["by_region"]
           and s2["by_year"] == s["by_year"] and s2["in_service"] == s["in_service"],
           "graded figures unchanged by work-order order, region and crew codes")
    finally:
        shutil.rmtree(tmp)
    ok(s["by_region"].keys() == set(subs["region"]), "regions are the current regions of substations.csv")


def no_move(s):
    """the graded figures are the ones submission.md states, down to their unrounded values"""
    F = FROZEN
    ok(s["lots"] == F["lots"] and s["modules"] == F["modules"] and round(s["cost"]) == F["cost"],
       "%d lots, %d modules, CAD %d" % (s["lots"], s["modules"], s["cost"]))
    ok(s["avail"] == F["avail"] and s["serviceable"] == F["serviceable"] and s["at_repair"] == F["at_repair"]
       and s["quarantine"] == F["quarantine"], "15 modules available: 12 serviceable and 3 at repair, 7 in quarantine")
    ok(abs(s["lam"] - F["lam"]) < 1e-6 and round(s["lam"], 1) == F["lam_1"], "expected failures unmoved (%.6f)" % s["lam"])
    ok(round(100 * s["cover"], 1) == F["cover_1"] and round(100 * s["settings"][12]["cover"], 1) == F["cover12_1"],
       "cover 99.1 per cent at 13 lots and 83.6 at 12")
    ok(set(s["by_year"]) == set(F["by_year"]) and all(abs(s["by_year"][y] - v) < 1e-6 and round(s["by_year"][y], 1) == F["by_year_1"][y]
                                                      for y, v in F["by_year"].items()), "every year's expected failures unmoved")
    ok(set(s["by_region"]) == set(F["by_region"]) and all(abs(s["by_region"][g] - v) < 1e-6 and round(s["by_region"][g], 1) == F["by_region_1"][g]
                                                          for g, v in F["by_region"].items()), "every region's expected failures unmoved")
    ok(s["in_service"] == F["in_service"], "relays supported on 1 January unmoved")
    ok(all(round(100 * s["settings"][n]["cover"], 1) == v and round(s["settings"][n]["cost"]) == n * W.LOT * 1965
           for n, v in F["settings_1"].items()), "every lot setting's cover and cost unmoved")
    ok(s["n_fail"] == F["n_fail"] and [int(c) for c in s["counts"]] == F["counts"], "210 failures in the same bands")
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    toks = ["Order 13 lots (325 modules)", "CAD 638,625", "**298.6**", "**15**", "**99.1%**", "**83.6%**",
            "October to December 2026: %.1f" % F["by_year_1"][2026]]
    toks += ["%d lots: %.1f%%, CAD %s" % (n, v, "{:,}".format(n * W.LOT * 1965)) for n, v in F["settings_1"].items()]
    toks += ["%s: %.1f" % (g, v) for g, v in F["by_region_1"].items()]
    toks += ["%d: %.1f; %s relays" % (y, F["by_year_1"][y], "{:,}".format(F["in_service"][y])) for y in range(2027, 2036)]
    ok(all(t in sub for t in toks), "submission.md states every frozen figure (%d tokens)" % len(toks))


CLAUSE_STOP = set("the a an to on at for from with and & of in up off out by then as is was be it w/ into after before till "
                  "until pending not no".split())


def cleanup(reg, wo, hist, subs, plan, f, s):
    """the cleanup after reader round 6, none of which moves a graded figure (no_move): module serials against the
    relay serials, a recorded end for every failed module, crew text without a clause library, the notice on
    Veldtek's letterhead, the program notes against the RTU-only rows, and the rebuilds' modules"""
    import sim as S
    d = lambda x: dt.date.fromisoformat(x) if x else None
    rows = list(openpyxl.load_workbook(os.path.join(T, "veldtek_rma_log_vpr340_psu.xlsx")).active.iter_rows(min_row=2, values_only=True))
    # module serials: Veldtek numbers every module it builds, the one in each relay and the spares, so its module
    # numbers run ahead of its relay numbers, ours take about the share of them we take of its relays, and they run in
    # order of manufacture under the date code
    num = lambda x: int(x.rsplit("-", 1)[1])
    code = lambda x: (1900 + int(x.split("-")[1])) if int(x.split("-")[1]) > 50 else (2000 + int(x.split("-")[1]))
    psu = sorted(set(hist["serial_no"]) | {r[2] for r in rows})
    rel = list(reg[reg["model"] == "VPR-340"]["serial_no"])
    ok(all(re.fullmatch(r"PS02-\d\d-\d{5}", x) for x in psu), "module serials keep the PS02-yy-nnnnn form")
    pspan = max(map(num, psu)) - min(map(num, psu)) + 1
    rspan = max(map(num, rel)) - min(map(num, rel)) + 1
    ok(pspan >= 1.15 * rspan and len(psu) / pspan <= 1.1 * len(rel) / rspan,
       "%d module serials over %d numbers, %d relays over %d" % (len(psu), pspan, len(rel), rspan))
    by_num = sorted(psu, key=num)
    ok(all(code(a) <= code(b) for a, b in zip(by_num, by_num[1:])), "module numbers run in date-code order")
    rfirst, pfirst = {}, {}
    for x in rel:
        rfirst[code(x)] = min(num(x), rfirst.get(code(x), num(x)))
    for x in psu:
        pfirst[code(x)] = min(num(x), pfirst.get(code(x), num(x)))
    ok(all(pfirst[y] >= rfirst[y] for y in pfirst if y in rfirst), "each year's module numbers start above its relay numbers")
    ok(all(code(x) <= fit.year for x, fit in zip(hist["serial_no"], hist["fitted"])), "no module fitted before its date code")
    # every failed module since go-live ends somewhere on record: at Veldtek under an RMA it was shipped on, or scrapped
    # by the store on bench check under an e-waste manifest, on a disposal work order at the store that names it; only a
    # module removed in the months before the count can still be on a returns shelf
    log = wo[wo["work_type"] == "LOG"]
    fits = {}
    for x, fit in zip(hist["serial_no"], hist["fitted"]):
        fits.setdefault(x, []).append(fit)
    fail = hist[hist["removal_reason"] == "FAILED"]
    n_rma = n_scrap = 0
    pending = []
    for x, rm, ref in zip(fail["serial_no"], fail["removed"], fail["disposal_ref"]):
        rma = [r for r in rows if r[2] == x and r[5].date() >= rm]
        if ref:
            dw = log[log["description"].str.contains(ref, regex=False)]
            ok(len(dw) == 1 and x in dw["description"].iloc[0] and dw["sub_code"].iloc[0] == "" and dw["asset_id"].iloc[0] == ""
               and d(dw["completed_date"].iloc[0]) >= rm and not rma and not any(y > rm for y in fits[x]),
               "%s scrapped by the store under %s and not seen again" % (x, ref))
            n_scrap += 1
        elif rma:
            ship = log[log["description"].str.contains(x, regex=False) & log["reported_date"].map(lambda y: d(y) >= rm)]
            ok(len(ship) >= 1, "%s shipped to Veldtek on a logistics work order" % x)
            n_rma += 1
        else:
            pending.append(rm)
    ok(n_scrap >= 60 and n_rma >= 80 and len(pending) <= 8 and all(y >= dt.date(2026, 5, 1) for y in pending),
       "failed modules: %d to Veldtek, %d scrapped by the stores, %d removed since May 2026 still on a returns shelf"
       % (n_rma, n_scrap, len(pending)))
    man_date = []
    for t, rep, done, sc in zip(log["description"], log["reported_date"], log["completed_date"], log["sub_code"]):
        m = re.search(r"EW(\d\d)-(\d{4})", t)
        if m and "SC-2021-118" in t:
            man_date.append((d(rep) if sc else d(done), int(m.group(1)), int(m.group(2))))
    man_date.sort()
    ok(len({(a, b) for _, a, b in man_date}) == len(man_date)
       and all(b[2] > a[2] for a, b in zip(man_date, man_date[1:]) if a[1] == b[1]),
       "%d e-waste manifests, numbered in collection order through each year" % len(man_date))
    disp = log[(log["sub_code"] == "") & log["description"].str.contains("SC-2021-118", regex=False)]
    ok(len(disp) == len(set(fail["disposal_ref"]) - {""}) and disp["asset_id"].eq("").all()
       and disp["region"].isin(["North", "Central", "South", "Lakeshore", "Ridge", "Valley", "Harbour"]).all(),
       "%d disposal work orders at the stores, one for each manifest" % len(disp))
    # the count: open RMAs are at repair, and a module Veldtek returned comes back by overnight courier and is
    # SERVICEABLE from the next working day, so the one returned on 29 September is in the count on the 30th
    stock = pd.read_csv(os.path.join(T, E.F["stock"]), dtype={"item_no": str})
    ps = stock[stock["item_code"] == "VPR340-PSU-02"]
    ok(int(ps[ps["stock_state"] == "AT REPAIR"]["quantity"].sum()) == sum(r[6] == "OPEN" for r in rows), "at repair = open RMAs")
    shelf = []
    for r in rows:
        if r[7] is None or r[7].date() < W.MIGRATION:
            continue
        back = r[7].date()
        if not any(y >= back for y in fits.get(r[2], [])) and not any(q[2] == r[2] and q[5] > r[5] for q in rows):
            shelf.append(back)
    ok(len(shelf) <= s["serviceable"] and all(S.add_bdays(b + dt.timedelta(days=1), 0) <= W.ASOF for b in shelf)
       and dt.date(2026, 9, 29) in shelf, "%d repaired module(s) back on the shelf by the count, the 29 September return among them" % len(shelf))
    dic = " ".join(_text(os.path.join(T, "eam_extract_dictionary.txt")).split())
    ok("overnight courier" in dic and "received to SERVICEABLE the day it arrives" in dic and "is not stock" in dic
       and "blank for work at a store" in dic,
       "the dictionary says how returns, failed modules and store work are booked")
    # crew text: a clause comes back on one crew's work orders, not across crews
    cw = wo[wo["work_type"].isin(["CM", "EM", "LOG"])]
    clause = {}
    for t, c in zip(cw["description"], cw["crew"]):
        for p in re.split(r"\. |, | - |; | / ", t):
            p = re.sub(r"(?:\b(?:s/n:?|sn|ser) |#)?\bps02-\d\d-\d+\b|\b(?:f-?\d+|fdr ?\d+|feeder \d+|wo\d+)\b", "#",
                       p.strip().strip(".").lower())
            if len([w for w in p.split() if w != "#" and w not in CLAUSE_STOP]) >= 4:
                clause.setdefault(p, {})
                clause[p][c] = clause[p].get(c, 0) + 1
    out = {p: sum(v.values()) - max(v.values()) for p, v in clause.items()}
    worst = max(out, key=out.get)
    ok(out[worst] <= 3, "no clause of four or more words recurs more than 3 times outside the crew that writes it most "
                        "(worst '%s', %d)" % (worst, out[worst]))
    for phrase in ("relay restarts when panel door closed", "reclosing blocked until relay back"):
        ok(sum(phrase in t.lower() for t in cw["description"]) <= 3, "'%s' is an odd entry, not a stock phrase" % phrase)
    # the notice on Veldtek's letterhead with its reference, ordering terms and a contact; lot size and price as they were
    eol = " ".join(_text(os.path.join(T, "veldtek_vpr340_eol_notice.pdf")).split())
    ok(all(x in eol for x in ("VELDTEK", "PROTECTION SYSTEMS INC.", "Mississauga", "Tel ", "Notice no. EOL-2026-07", "Ordering",
                              "purchase order", "lots of 25", "CAD 1,965.00 per module", "CAD 49,125.00 per lot", "net 30",
                              "Contact", "@veldtek.ca")) and W.LOT == 25 and W.UNIT_PRICE == 1965.0,
       "the notice carries Veldtek's letterhead, its reference, ordering terms and a contact")
    # the program: no RTU-only scheme on the approved sheet, as its notes say
    wbp = openpyxl.load_workbook(os.path.join(T, E.F["prog"]))
    rtu26 = [r for r in wbp["Approved 2026"].iter_rows(min_row=4, values_only=True) if r[2] and str(r[5]).strip() == "RTU"]
    rtu25 = [r for r in wbp["2025 plan (superseded)"].iter_rows(min_row=4, values_only=True) if r[2] and str(r[5]).strip() == "RTU"]
    notes = " ".join(str(r[0]) for r in wbp["Notes"].iter_rows(values_only=True))
    ok(not rtu26 and rtu25 and "RTU-only schemes moved to the SCADA upgrade program" in notes,
       "no RTU-only scheme on the approved sheet, as the notes say (%d on the 2025 plan)" % len(rtu25))
    # the rebuilds' modules went with their relays because the rebuilds came before the end-of-life notice
    man = set(hist[hist["removal_reason"] == "ASSET RETIRED"]["disposal_ref"])
    rb = log[log["description"].map(lambda t: any(m in t for m in man))]
    ok(len(rb) == len(man) and all(re.search(r"veldtek", t, re.I) and re.search(r"psu", t, re.I) for t in rb["description"])
       and all(d(x) < W.NOTICE_DATE for x in rb["reported_date"]),
       "each rebuild's e-waste order says why the modules went with the relays, before the end-of-life notice")


if __name__ == "__main__":
    main()
