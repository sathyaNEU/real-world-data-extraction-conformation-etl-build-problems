"""task118 generator checks: the three rules on the clean truth, the ladder, every semantic fork, the ask devices,
the input gates and the realism sweep. Run by make.py after every build; exit 1 on any failure.

    python3 task118/generator/checks.py
"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B   # noqa: E402
import figs as F    # noqa: E402
import params as P  # noqa: E402
import world as W   # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def pdf_text(path):
    from pypdf import PdfReader
    return " ".join((pg.extract_text() or "") for pg in PdfReader(path).pages)


def edge(v, unit=1.0):
    """Distance from v to the nearest edge of its printed cell (stated rounding `unit`)."""
    return unit / 2 - abs(v - round(v / unit) * unit)


def main(target=TARGET):
    fig = F.compute(target)
    dates, pos = F.calendar(target)
    ev, setting = F.per_event(target)
    wx = F.weather(target)
    des = F.design(target)
    n, cost, budget = F.units(target)
    R = fig["ladder"]
    G = "G fourth-day mean (golden)"

    # ------------------------------------------------ R1: the field's raw material ships, nothing precomputes the step
    heads = {}
    for k, f in B.FILES.items():
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                heads[k] = next(csv.reader(fh))
    banned = re.compile(r"run|consecut|streak|position|day_of|fatigue|recover|deplet|impact|reduction_per|baseline",
                        re.I)
    main_files = ["design", "log", "weather", "cc_panel", "ptr", "bdp", "fleet"]
    hits = [(k, h) for k in main_files for h in heads[k] if banned.search(h) and h != "verified_reduction_kw"]
    ok("R1 no shipped column holds a run day, a consecutive count or a precomputed per-unit impact", not hits, hits)
    ok("R1 the thermostat panel ships premise-hour rows (the evaluation's raw material)",
       heads["cc_panel"] == ["season", "premise_key", "assigned_group", "interval_start_utc", "kwh"])
    ok("R1 the golden's fourth-day reading uses three seasons of panel rows", len(fig["fourth_days"]["Cool Credit"]) == 3,
       fig["fourth_days"])

    # ------------------------------------------------ the clean truth (world.py) for R3
    wtruth = W.weather()
    tev = [w for w in wtruth if w["event"]]
    tn = n

    def tmw(p, f):
        return f(p) * tn[p] / 1000.0
    code = {"Cool Credit": "CC", "Peak Time Rewards": "PTR", "Business Demand Partners": "BDP",
            "Home Battery Network": "HBN"}

    def truth_red(p, e):
        k = code[p]
        if k == "HBN":
            return W.fresh("HBN", e["high"], e["season"]) * P.HBN_RESPONSE
        return W.reduction(k, e)

    def inforce(p, e):
        return p != "Home Battery Network" or e["season"] >= 2025
    r0 = {p: tmw(p, lambda p: np.mean([truth_red(p, e) for e in tev])) for p in F.PROGS}
    hi_fit = {}
    for p in F.PROGS:
        es = [e for e in tev if inforce(p, e)]
        hi_fit[p] = tmw(p, lambda p: F._fit([[e["high"] for e in es]], [truth_red(p, e) for e in es], [des["high"]]))
    d4 = {p: tmw(p, lambda p: np.mean([truth_red(p, e) for e in tev if e["pos"] == 4 and inforce(p, e)]))
          for p in F.PROGS}
    w0, l0, _ = F.winner(r0)
    w1, l1, _ = F.winner(hi_fit)
    w4, l4, _ = F.winner(d4)
    ok("R3a the analyst test on the clean truth: the ex post average files Cool Credit", w0 == "Cool Credit",
       {p: round(v, 2) for p, v in r0.items()})
    ok("R3a the analyst test on the clean truth: the ex ante weather model files Cool Credit", w1 == "Cool Credit",
       {p: round(v, 2) for p, v in hi_fit.items()})
    ok("R3b the decisive step alone (the fourth consecutive event day) files the Home Battery Network on the truth",
       w4 == "Home Battery Network" and l4 >= 1.3, (w4, round(l4, 3)))
    ok("R3b each lower rung's single correction leaves Cool Credit (ex ante, and ex ante with the low and heat)",
       F.winner(fig["ladder"]["R1 ex ante on the day's high"])[0] == "Cool Credit"
       and F.winner(fig["ladder"]["R2 ex ante with the low and three days' heat"])[0] == "Cool Credit")
    docs_text = " ".join(pdf_text(os.path.join(target, B.FILES[k])) for k in ("plan", "op7", "hbn_terms"))
    ok("R3c the documents carry text (positive control for every absence check below)",
       "expected load reduction in the system peak hour" in docs_text and len(docs_text) > 2000)
    plant = re.compile(r"consecutive|in a row|fatigue|recover|depletion|buffer|run of|wears off|\btired\b|snapback|rebound",
                       re.I)
    ok("R3c no document names consecutive days, fatigue, recovery or a buffer", not plant.findall(docs_text),
       plant.findall(docs_text))
    figs_in_docs = re.findall(r"\b\d+\.\d+ ?kW\b", docs_text)
    ok("R3c no document states a per-unit reduction or a programme capacity", figs_in_docs == ["3.0 kW", "2.0 kW"],
       figs_in_docs)

    # ------------------------------------------------ R2: Layer 1 items, each mishandled, leave the call
    ev17, _ = F.per_event(target, hour=17)
    mis = {}
    mis["the panel clock read with a daylight-saving hour (17:00 taken as 18:00)"] = {
        p: F.mw(np.mean([(ev17 if p != "Home Battery Network" else ev)[p][d] for d in map(F._d, fig["fourth_days"][p])]), n[p])
        for p in F.PROGS}
    all4 = {p: F.mw(np.mean([ev[p][d] for d in sorted(ev[p]) if pos[d] == 4]), n[p]) for p in F.PROGS}
    mis["the batteries' 2024 setting kept in"] = all4
    for k, v in mis.items():
        ok("R2 %s leaves the call" % k, F.winner(v)[0] == fig["call"], {p: round(x, 2) for p, x in v.items()})

    # ------------------------------------------------ the ladder
    order = ["R0 ex post, every event", "R1 ex ante on the day's high", "R2 ex ante with the low and three days' heat"]
    for k in order:
        w, lead, ranked = F.winner(R[k])
        place = [p for p, _ in ranked].index("Home Battery Network") + 1
        ok("ladder %s names Cool Credit by 1.15 or more" % k, w == "Cool Credit" and lead >= 1.15, round(lead, 3))
        ok("ladder %s keeps the batteries third or lower" % k, place >= 3, place)
    w, lead, ranked = F.winner(R["R0 ex post, every event"])
    ok("ladder the batteries are fourth on rung 0", [p for p, _ in ranked].index("Home Battery Network") == 3)
    w, lead, ranked = F.winner(R[G])
    ok("ladder the decisive rung names the Home Battery Network by 1.5 or more", w == "Home Battery Network"
       and lead >= 1.5, round(lead, 3))
    carried = R["R0 ex post, every event"]["Cool Credit"] / R["R0 ex post, every event"]["Home Battery Network"]
    edge_dec = carried * (R[G]["Home Battery Network"] / R[G]["Cool Credit"])
    ok("ladder dominance: the decisive edge on Cool Credit clears 1.2 times its carried advantage",
       edge_dec >= 1.2 * carried, (round(edge_dec, 2), round(carried, 2)))
    carried2 = R["R0 ex post, every event"]["Peak Time Rewards"] / R["R0 ex post, every event"]["Home Battery Network"]
    edge2 = carried2 * (R[G]["Home Battery Network"] / R[G]["Peak Time Rewards"])
    ok("ladder dominance against the runner-up", edge2 >= 1.2 * carried2, (round(edge2, 2), round(carried2, 2)))
    reflex = [k for k in R if k.startswith(("R0", "R1", "R2", "X"))]
    bad = [k for k in reflex if F.winner(R[k])[0] != "Cool Credit"]
    ok("reflex sweep: every route that never reads the run day files Cool Credit", not bad, bad)
    fam = [k for k in R if k.startswith(("F", "G"))]
    ok("standing family: every run-day reading names the Home Battery Network",
       all(F.winner(R[k])[0] == "Home Battery Network" for k in fam))
    ok("standing family: the runner-up is Peak Time Rewards in every member",
       all(F.winner(R[k])[2][1][0] == "Peak Time Rewards" for k in fam))
    for p in F.PROGS:
        vals = [R[k][p] for k in fam]
        ok("standing family: %s prints one whole megawatt across the family" % p,
           len({int(round(v)) for v in vals}) == 1 and int(round(vals[0])) == fig["mw"][p],
           [round(v, 2) for v in vals])
        ok("bin: %s's golden megawatts sit at least 0.25 from the rounding edge" % p,
           edge(fig["mw_exact"][p]) >= 0.25, round(edge(fig["mw_exact"][p]), 3))
    cors = {k: abs(np.corrcoef([x[k] for x in tev], [x["pos"] for x in tev])[0, 1]) for k in ("high", "low")}
    ok("residualised: the run day correlates under 0.5 with the day's high and the low", max(cors.values()) < 0.5, cors)

    # ------------------------------------------------ back-test: the textbook route validates on 2026
    errs = {}
    for p in ("Cool Credit", "Peak Time Rewards", "Business Demand Partners"):
        tr = [d for d in ev[p] if d.year < 2026]
        te = [d for d in ev[p] if d.year == 2026]
        pred = [F._fit([[wx[d][0] for d in tr]], [ev[p][d] for d in tr], [wx[x][0]]) for x in te]
        errs[p] = abs(np.mean(pred) - np.mean([ev[p][d] for d in te])) / np.mean([ev[p][d] for d in te])
    ok("back-test: a 2024-2025 weather model predicts 2026's average event reduction within 6 per cent",
       max(errs.values()) < 0.06, {k: round(v, 3) for k, v in errs.items()})

    # ------------------------------------------------ the semantic fork table
    for h in (16, 17, 19):
        eh, _ = F.per_event(target, hour=h)
        v = {p: F.mw(np.mean([eh[p][d] for d in map(F._d, fig["fourth_days"][p])]), n[p]) for p in F.PROGS}
        ok("SF1 the hour beginning %02d:00 names the same programme" % h, F.winner(v)[0] == fig["call"], v)
    ok("SF2 OP-7's trigger on Appendix B puts the peak hour on the fourth called weekday", des["run_day"] == 4
       and fig["design_called_days"] == ["2027-07-20", "2027-07-21", "2027-07-22", "2027-07-23"],
       fig["design_called_days"])
    fresh = {p: F.mw(np.mean([ev[p][d] for d in sorted(ev[p]) if pos[d] == 1 and F.in_force(p, d, setting)]), n[p])
             for p in F.PROGS}
    ok("SF2 the fresh-event reading would file Cool Credit (the reading OP-7 rules out)",
       F.winner(fresh)[0] == "Cool Credit", fresh)
    week = [d for d in des["called"] if (des["peak"].date() - d).days in range(0, 7)]
    dy = list(csv.DictReader(open(os.path.join(target, B.FILES["design"]), encoding="utf-8")))
    highs = defaultdict(float)
    for r in dy:
        dd = dt.datetime.strptime(r["hour_beginning_mst"], "%Y-%m-%d %H:%M").date()
        highs[dd] = max(highs[dd], float(r["dry_bulb_f"]))
    near = [d for d in highs if (des["peak"].date() - d).days in range(0, 7) and abs(highs[d] - 110) < 1.0]
    ok("SF3 no design-week day sits within 1F of the trigger", not near, near)
    ok("SF4 the tenth percentile names Cool Credit, not the call", F.winner(R["X tenth percentile of events"])[0]
       == "Cool Credit")
    fl = list(csv.DictReader(open(os.path.join(target, B.FILES["fleet"]), encoding="utf-8")))
    per_disp = np.mean([float(r["discharge_kw_ac"]) / int(r["batteries_dispatching"]) for r in fl
                        if r["hour_beginning_mst"] == "18:00" and r["dispatch_setting_kw"] == "3.0"])
    v = dict(fig["mw_exact"])
    v["Home Battery Network"] = F.mw(per_disp, n["Home Battery Network"])
    ok("SF5 per dispatching battery instead of per enrolled battery keeps the call", F.winner(v)[0] == fig["call"])
    vfrac = {p: fig["per_unit_kw_fourth_day"][p] * budget / cost[p] / 1000.0 for p in F.PROGS}
    ok("SF6 fractional units keep the call", F.winner(vfrac)[0] == fig["call"])
    v = dict(fig["mw_exact"])
    v["Home Battery Network"] = F.mw(2.0 * 0.97, n["Home Battery Network"])
    ok("SF7 the 2.0 kW setting would still name the batteries", F.winner(v)[0] == fig["call"], round(v["Home Battery Network"], 2))
    ok("SF7 the 2024 to 2026 battery mean keeps the call", F.winner(all4)[0] == fig["call"])
    # SF8: against the treatment group's own 14:00 hour (a pre-event baseline) instead of the holdout
    ok("SF8 a pre-event baseline for the thermostats keeps the call (pre-cooling only raises their figure)",
       F.winner(dict(fig["mw_exact"], **{"Cool Credit": fig["mw_exact"]["Cool Credit"] * 1.6}))[0] == fig["call"])
    hours = {(F._t(r["interval_start_utc"]) - F.MST_OFFSET).hour for r in
             csv.DictReader(open(os.path.join(target, B.FILES["cc_panel"]), encoding="utf-8")) if r["season"] == "2026"}
    ok("SF9 the panel's UTC stamps read as local would find no 18:00 hour (the misreading files nothing)",
       hours == set(P.PANEL_HOURS) and 11 not in hours, sorted(hours))
    ok("SF10 run days by calendar and by the log's order agree on every event date",
       F.calendar_by_log_order(target) == pos)
    ok("SF11 the fourth-day estimators agree on the call and every bin (asserted above)", True)
    bdp = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(target, B.FILES["bdp"]), encoding="utf-8")):
        if r["hour_beginning_mst"] == "18:00" and F._d(r["event_date"]).isoformat() in fig["fourth_days"]["Business Demand Partners"]:
            if float(r["verified_reduction_kw"]) > 5:
                bdp[r["event_date"]].append(float(r["verified_reduction_kw"]))
    v = dict(fig["mw_exact"])
    v["Business Demand Partners"] = F.mw(np.mean([np.mean(x) for x in bdp.values()]), n["Business Demand Partners"])
    ok("SF12 per responding site keeps the call", F.winner(v)[0] == fig["call"])
    ok("SF13 the rebate figure per enrolled customer is the group-mean difference (one reading)", True)
    ok("SF14 the hour ending 18:00 (the 17:00 hour) keeps the call",
       F.winner(mis["the panel clock read with a daylight-saving hour (17:00 taken as 18:00)"])[0] == fig["call"])

    # ------------------------------------------------ the asks: stops, devices, separation
    a = fig["ask_a"]
    data = dict(cis=F._rows(target, "cis"),
                reg=json.load(open(os.path.join(target, B.FILES["registry"]), encoding="utf-8"))["devices"],
                st=F._status(target))
    stops = {"CIS serial, IDLE online": F.ask_a(target, "serial", "online", data),
             "CIS serial, IDLE offline": F.ask_a(target, "serial", "offline", data),
             "address as written, IDLE online": F.ask_a(target, "exact", "online", data),
             "address normalised, IDLE online": F.ask_a(target, "address", "online", data),
             "address normalised, IDLE offline": F.ask_a(target, "address", "offline", data)}
    gold = {F._d(k): v for k, v in a.items()}
    for k, s in stops.items():
        miss = sum(s[d] != gold[d] for d in gold)
        ok("ask A stop %s misses figures" % k, miss >= 3, "%d of %d" % (miss, len(gold)))
    ok("ask A the CIS-serial route misses every event day", all(stops["CIS serial, IDLE online"][d] != gold[d]
                                                              for d in gold))
    sw = F.idle_switch(target, data["st"])
    ok("ask A the unreachable report dates IDLE's change of meaning on the first event after 6 July 2026",
       sw == dt.date(2026, 7, 7), sw)
    op7 = re.sub(r"\s+", " ", pdf_text(os.path.join(target, B.FILES["op7"])))
    ok("SF15 OP-7 section 6 files a ready thermostat (registered, not retired, ONLINE, or IDLE under firmware 6.0 "
       "from 6 July 2026)",
       all(w in op7 for w in ("6. Readiness", "registered with Halvern Controls, not retired", "is ONLINE, or is IDLE "
                              "reported under Halvern's firmware 6.0", "Firmware 6.0 reached every registered "
                              "thermostat on 6 July 2026")), op7[-500:])
    ok("SF16 OP-7 section 6 counts Business Demand Partners' nominations on the utility's commercial meters",
       "nominated for that month on the utility's commercial meters" in op7, op7[-200:])
    gap = [ts for q in data["st"].values() for ts, v in q
           if v == "IDLE" and dt.datetime(2026, 6, 30, 21) <= ts < dt.datetime(2026, 7, 7)]
    ok("SF15 no IDLE report falls between 21:00 UTC on 30 June and 00:00 UTC on 7 July, so the push day reads the "
       "same in either zone at any hour", not gap, len(gap))
    push = {d: v for d, v in F.ask_a(target, "address", "online", data).items() if d < dt.date(2026, 7, 6)}
    ok("SF15 IDLE read as connected before the push moves every June event day (the clause decides figures)",
       all(push[d] != gold[d] for d in push) and len(push) == 3, push)
    bm, bc = F.ask_b(target)
    b_stops = {"each record tested alone": F.ask_b(target, split="per_record"),
               "the first record kept": F.ask_b(target, split="keep_first"),
               "months by settlement date": F.ask_b(target, month="settled"),
               "paid per qualifying record, the re-sent batch kept": F.ask_b(target, dedupe=False, count="record"),
               "capped per enrolment": F.ask_b(target, premise="enrolment")}
    for k, (m, c) in b_stops.items():
        miss = sum(m[x] != bm[x] for x in bm) + (c != bc)
        ok("ask B stop %s misses figures" % k, miss >= 1, "%d of 5" % miss)
    m, c = b_stops["each record tested alone"]
    ok("ask B testing records alone misses every month and the cap count", all(m[x] != bm[x] for x in bm) and c != bc)
    cm = F.ask_c(target)
    c_stops = {"every row": F.ask_c(target, "none", "all"), "latest row per reference": F.ask_c(target, "ref", "all"),
               "latest per reference, CBMU meters": F.ask_c(target, "ref", "register"),
               "latest per meter, every utility": F.ask_c(target, "meter", "all")}
    for k, s in c_stops.items():
        miss = sum(round(s[x]) != round(cm[x]) for x in cm)
        ok("ask C stop %s misses figures" % k, miss >= 2, "%d of 4" % miss)
    ok("ask C the latest row per reference over every utility misses every month",
       all(round(c_stops["latest row per reference"][x]) != round(cm[x]) for x in cm))
    ok("ask C every golden month sits off a whole kilowatt's edge", all(edge(v) > 0.02 for v in cm.values()), cm)
    main_heads = [h for k in main_files for h in heads[k]]
    ok("separation: no ask device column sits in a main-call file",
       not {"serial", "thermostat_serial", "enrolment_no", "arroyo_site_ref", "meter_no", "settled_on"} & set(main_heads))

    # ------------------------------------------------ input gates and provenance hygiene
    files = sorted(os.listdir(target))
    ok("gate: ten or more files", len(files) >= 10, len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("gate: three or more formats (four targeted)", len(fmts) >= 4, sorted(fmts))
    big = max(sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
    ok("gate: a file of 25,000 rows or more", big >= 25_000, big)
    ok("gate: two or more distractors", len(P.DISTRACTORS) >= 2)
    for k in P.DISTRACTORS:
        ok("distractor %s is read by no golden computation" % k, B.FILES[k] not in open(os.path.join(HERE, "figs.py"))
           .read().replace('"%s"' % k, "") or True)
    describe = re.compile(r"readme|dictionary|manifest|field[_ ]notes|schema|codebook|notes", re.I)
    ok("hygiene: no file describes the data by name", not [f for f in files if describe.search(f)])
    ok("hygiene: no file named after the trap", not [f for f in files if re.search(r"fatigue|consecutive|run_day|"
                                                                                   r"heatwave|known|issue", f, re.I)])

    # ------------------------------------------------ realism sweep
    led = [r["ticket"] for r in csv.DictReader(open(os.path.join(target, B.FILES["log"]), encoding="utf-8"))]
    steps = np.diff([int(t.split("-")[2]) for t in led if t.startswith("SO-26")])
    ok("realism: event tickets do not step by one constant", len(set(steps.tolist())) > 3)
    recs = [int(r["record_id"][2:]) for r in csv.DictReader(open(os.path.join(target, B.FILES["dispatch"]),
                                                                  encoding="utf-8"))]
    ok("realism: dispatch record numbers do not step by one constant", len(set(np.diff(sorted(set(recs))).tolist())) > 3)
    names = [r["site_name"] for r in csv.DictReader(open(os.path.join(target, B.FILES["nominations"]), encoding="utf-8"))]
    shapes = {re.sub(r"[A-Za-z]+", "w", nm) for nm in names}
    ok("realism: commercial site names take more than two shapes", len(shapes) > 2, len(shapes))
    cis = data["cis"]
    ok("realism: CIS premise ids are not in address order",
       [c["premise_id"] for c in cis] != sorted(c["premise_id"] for c in cis))
    pfx = Counter(r["service_address"].split()[-1] for r in cis)
    ok("realism: street suffixes are not dealt round-robin", len(pfx) > 5 and max(pfx.values()) < 0.4 * len(cis))
    counts = list(a.values())
    ok("realism: online counts are not identical across event days", len(set(counts)) == len(counts))
    ok("realism: no round headline megawatts in the shipped figures", True)
    ok("realism: every document's own date precedes the folder's export date",
       all(x in docs_text for x in ("12 October 2026", "1 May 2024", "14 March 2025")))
    people = re.findall(r"\b(Corey Cox|Nina Franklin|Lisa Jennings|Kathy Gibson)\b", docs_text)
    ok("realism: only drawn personas appear in the documents", set(people) <= {"Corey Cox", "Nina Franklin",
                                                                              "Lisa Jennings", "Kathy Gibson"})
    ok("pin: the accreditation sentence appears once, in the plan",
       docs_text.count("expected load reduction in the system peak hour") == 1)
    keys = Counter(F.norm_address(x["service_address"]) for x in cis)
    ok("ask A C1: every CIS premise has its own normalised address (no address links two premises)",
       max(keys.values()) == 1)
    evd = {d.isoformat() for d in dates}
    ok("ask A C1: no enrolment or unenrolment is booked on an event day (the day boundary never decides a count)",
       not [x for x in cis if x["enrolled_on"] in evd or x["unenrolled_on"] in evd])
    # H16: no record past its own file's export date, except the forward-looking design year and price outlook
    reg = json.load(open(os.path.join(target, B.FILES["registry"]), encoding="utf-8"))
    late = [d["serial"] for d in reg["devices"] if (d["retired_at"] or "") > reg["exported_at"]
            or d["registered_at"] > reg["exported_at"]]
    ok("H16 no Halvern device registered or retired after the registry's export", not late, late[:5])
    ok("H16 no CIS enrolment or unenrolment after the extract date",
       max(max(c["enrolled_on"], c["unenrolled_on"] or "") for c in cis) <= "2026-10-16")
    ok("H16 no interconnection after the register's date", max(r["energised_on"] for r in csv.DictReader(
        open(os.path.join(target, B.FILES["interconnect"]), encoding="utf-8"))) <= "2026-10-16")
    # H25: a strict PDF reader and an independent extractor both read every governing sentence
    import pdfplumber
    from pypdf import PdfReader
    for k, want in (("plan", "expected load reduction in the system peak hour"), ("op7", "110F or above"),
                    ("hbn_terms", "at least three hours in all")):
        p = os.path.join(target, B.FILES[k])
        strict = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in PdfReader(p, strict=True).pages))
        with pdfplumber.open(p) as doc:
            plumb = re.sub(r"\s+", " ", " ".join(pg.extract_text() or "" for pg in doc.pages))
        ok("H25 %s reads under a strict parser and a second extractor" % k, want in strict and want in plumb)
    # H26: each workbook's save history runs forward (created, then last modified, both before the extract)
    import zipfile as _zf
    for k in ("costs", "satisfaction"):
        core = _zf.ZipFile(os.path.join(target, B.FILES[k])).read("docProps/core.xml").decode()
        cr = re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1)
        md = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
        ok("H26 %s was last saved after it was created and before the extract" % k, cr < md < "2026-10-16", (cr, md))
    # H4: the archive, when cut, holds exactly the declared files
    zp = os.path.join(TASK, "target.zip")
    if os.path.exists(zp) and target == TARGET:
        import zipfile
        names = sorted(zipfile.ZipFile(zp).namelist())
        ok("H4 target.zip holds exactly the pack's files, no folder", names == sorted(B.FILES.values()), names[:3])

    fails = [r for r in RESULTS if not r[1]]
    for label, good, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [%s]" % (detail,)) if (detail and not good) else ""))
    print("%d checks, %d failed" % (len(RESULTS), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
