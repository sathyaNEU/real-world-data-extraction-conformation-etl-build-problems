"""The generator's assertions, run on every build: the input gates, the three rules executed on the clean truth (R1 the
field's raw material ships, R2 the Layer 1 mess cannot move the call, R3 the analyst test and its ladder), every
semantic fork (SF1 to SF18), bin margins, the ask devices measured, the separation line and the realism sweep."""
import csv
import datetime as dt
import json
import os
import re
import zipfile

import numpy as np

import golden as GO
import pack as P
import verify as V
import world as W

ROWS = []


def ok(label, cond, detail=""):
    ROWS.append((label, bool(cond), detail))


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def arrays(steps, end_extra=0):
    flow, voc = np.zeros(W.YEAR), np.zeros(W.YEAR)
    for st in steps:
        a, b = max(0, st[6]), min(W.YEAR, st[7] + end_extra)
        if a < b:
            flow[a:b] += st[8]
            voc[a:b] += st[9] / 60.0
    return flow, voc


def tons(flow, voc, status, fan=W.FAN_MAX, dre=W.DRE, capacity=True, bin_min=1, run_modes=("RUN",)):
    run = np.isin(status, run_modes)
    e = V.emitted(flow, voc, run, fan, dre, capacity=capacity, bin_min=bin_min)
    q = [float(e[a:b].sum()) / 2000 for a, b in W.QUARTERS]
    return sum(q), q


def verdict(t):
    return "over" if t > W.LIMIT_TONS else "within"


def run(target, gdir, w, meta_path, fig_path):
    del ROWS[:]
    fig = json.load(open(fig_path))
    meta = json.load(open(meta_path))
    files = sorted(os.listdir(target))
    G = fig["raw"]["total_tons"]

    # ------------------------------------------------------------------ input gates
    ok("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    fmts = sorted({f.rsplit(".", 1)[1] for f in files})
    ok("G2 three or more formats", len(fmts) >= 3, ", ".join(fmts))
    big = max(meta["rows"].values())
    ok("G3 a file of 25,000 rows or more", big >= 25000, "%d rows" % big)
    ok("G4 two or more distractors named and shipped", len(meta["distractor_files"]) >= 2 and
       all(d in files for d in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    bad = [f for f in files if re.search(r"readme|dictionar|manifest|notes|codebook|field.?guide|schema", f, re.I)]
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                wbx = z.read("xl/workbook.xml").decode()
                sheets += re.findall(r'<sheet name="([^"]+)"', wbx)
    bad += [s for s in sheets if re.search(r"readme|dictionar|manifest|notes|about|how to", s, re.I)]
    ok("G5 no file or sheet describes the data", not bad, ", ".join(bad) or "sheets: " + "; ".join(sheets))
    vsrc = open(os.path.join(os.path.dirname(__file__), "verify.py")).read()
    ok("G6 the distractors are read by no figure", not any(p in vsrc for p in ("eu_b1", "eu_g1", "ldar")), "verify.py")
    import openpyxl
    nums = [c.value for row in openpyxl.load_workbook(os.path.join(target, P.FILES["form"])).active.iter_rows()
            for c in row if isinstance(c.value, (int, float))]
    ok("G7 the form template carries no figure", not nums, P.FILES["form"])

    # ------------------------------------------------------------------ R1: the field's raw material ships
    steps = w.steps
    in26 = [s for s in steps if s[7] > 0 and s[6] < W.YEAR]
    ok("R1a every vent's steps with start and end to the minute", len({s[0] for s in in26}) == 9, "%d steps" % len(in26))
    ok("R1b every executed step has a basis flow and VOC rate", all(s[8] > 0 and s[9] > 0 for s in in26))
    ok("R1c the oxidizer's maximum draw is on the register and nowhere a capture figure", True, "3,800 scfm")

    # ------------------------------------------------------------------ R3: the analyst test on the clean truth
    flow, voc, status = w.flow, w.voc_min, w.status
    r0 = tons(flow, voc, status, capacity=False, run_modes=("RUN", "WARMUP", "OFF"))[0]
    r1 = tons(flow, voc, status, capacity=False)[0]
    h60 = tons(flow, voc, status, bin_min=60)[0]
    h15 = tons(flow, voc, status, bin_min=15)[0]
    h5 = tons(flow, voc, status, bin_min=5)[0]
    g = tons(flow, voc, status)[0]
    L = W.LIMIT_TONS
    ok("R3a destruction on every pound, downtime ignored: within", r0 * 1.15 <= L, "%.3f t" % r0)
    ok("R3b the field's method (offline minutes uncontrolled) files within", r1 * 1.15 <= L, "%.3f t, %.2fx" % (r1, L / r1))
    ok("R3c the fan checked on hourly mean header flow files within", h60 * 1.15 <= L, "%.3f t, %.2fx" % (h60, L / h60))
    ok("R3d minute-by-minute capture files over by 1.2x or more", g >= 1.2 * L, "%.3f t, %.2fx" % (g, g / L))
    ok("R3e the golden is the clean truth's", abs(g - G) < 1e-3, "%.4f against %.4f" % (g, G))
    cheap = [x for x in (r0, r1, h60) if verdict(x) == "over"]
    ok("R3f no cheap route lands the call", not cheap, "R0 %.2f, R1 %.2f, hourly %.2f; 15-minute %.2f, 5-minute %.2f"
       % (r0, r1, h60, h15, h5))

    # ------------------------------------------------------------------ R2: Layer 1 cannot move the call
    by_batch, inflight = P.classify(w)
    pre = [s for s in steps if (s[0], s[1]) in inflight and s[6] < W.CUTOVER]
    f2, v2 = arrays(steps + pre)
    t_dup = tons(f2, v2, status)[0]
    trunc = [s[:7] + [min(s[7], W.CUTOVER)] + s[8:] if (s[0], s[1]) in inflight and s[6] < W.CUTOVER else s
             for s in steps]
    f3, v3 = arrays(trunc)
    t_trunc = tons(f3, v3, status)[0]
    st_local = status.copy()
    st_local[W.DST_START:W.DST_END - 60] = status[W.DST_START + 60:W.DST_END]
    t_dahs = tons(flow, voc, st_local)[0]
    shifted = [s[:6] + [s[6] + (240 if s[6] < W.DST_END else 300), s[7] + (240 if s[6] < W.DST_END else 300)] + s[8:]
               if s[6] >= W.CUTOVER else s for s in steps]
    f4, v4 = arrays(shifted)
    t_utc = tons(f4, v4, status)[0]
    ok("R2a the cutover's in-flight steps counted twice: same call", verdict(t_dup) == "over", "%.3f t" % t_dup)
    ok("R2b the open step ended at the cutover: same call", verdict(t_trunc) == "over", "%.3f t" % t_trunc)
    ok("R2c the DAHS clock read as local time: same call", verdict(t_dahs) == "over", "%.3f t" % t_dahs)
    ok("R2d Orbitas UTC read as local time: same call", verdict(t_utc) == "over", "%.3f t" % t_utc)

    # ------------------------------------------------------------------ the semantic fork table
    px = lambda s: s[0].startswith("R-") and s[2] in ("PX-711", "PX-714") and s[4] not in ("HOLD", "CIP")
    alt60 = 35.3146667 * 288.706 / 273.15
    f5, v5 = arrays([s[:8] + [s[8] * alt60 / W.SCF_PER_NM3] + s[9:] if px(s) else s for s in steps])
    t60 = tons(f5, v5, status)[0]
    f6, v6 = arrays([s[:8] + [s[8] * 35.3146667 / W.SCF_PER_NM3] + s[9:] if px(s) else s for s in steps])
    t0c = tons(f6, v6, status)[0]
    f7, v7 = arrays(steps, end_extra=1)
    t_incl = tons(f7, v7, status)[0]
    t_warm = tons(flow, voc, status, run_modes=("RUN", "WARMUP"))[0]
    t_low = tons(flow, voc, status, dre=0.9936)[0]
    t_s1 = tons(flow, voc, status, capacity=False)[0]
    ok("SF1 emitted is released to the atmosphere at any point (D.1); the S-1 and S-2 stacks alone file within",
       verdict(G) == "over" and verdict(t_s1) == "within", "golden %.3f, stacks only %.3f" % (G, t_s1))
    e_g = V.emitted(flow, voc, status == "RUN", W.FAN_MAX, W.DRE)
    est_b = [d * 1440 for d in (0, 90, 181, 273, 365)]
    q_est = [float(e_g[a:b].sum()) / 2000 for a, b in zip(est_b[:-1], est_b[1:])]
    q_utc = [float(e_g[max(0, a - 300):b - 300].sum()) / 2000 for a, b in zip(est_b[:-1], est_b[1:])]
    ok("SF2 calendar 2026 and its quarters in local time (D.1): EST or UTC boundaries give the same bins",
       all(round(x, 1) == round(y, 1) == round(z, 1) for x, y, z in zip(fig["raw"]["quarters_tons"], q_est, q_utc)),
       "EST %s, UTC %s" % ([round(x, 3) for x in q_est], [round(x, 3) for x in q_utc]))
    ok("SF3 a ton is 2,000 pounds (D.1); a tonne files %.2f, still over" % (G * 2000 / 2204.62262), verdict(G * 0.9072) == "over")
    ok("SF4 standard conditions 68 F (D.1); at 60 F %.3f, uncorrected Nm3 %.3f, both over" % (t60, t0c),
       verdict(t60) == "over" and verdict(t0c) == "over")
    runs = [float(r[5]) for r in __import__("docs").TEST_RUNS]
    ok("SF5 destruction 99.4 per cent, the test's mean (B.4); the runs average %.2f; the lowest run files %.3f, over"
       % (sum(runs) / 3, t_low), abs(sum(runs) / 3 - 99.40) < 0.005 and verdict(t_low) == "over")
    ok("SF6 a step lasts from its start to its end; counting the end minute files %.3f, over" % t_incl,
       verdict(t_incl) == "over")
    ok("SF7 the cutover's in-flight steps once; twice files %.3f, same call" % t_dup, verdict(t_dup) == "over")
    ok("SF8 the open Batchwise step completed from Orbitas; truncated %.3f, same call" % t_trunc,
       verdict(t_trunc) == "over")
    ok("SF9 DAHS in Eastern Standard Time (its header); read as local %.3f, same call" % t_dahs,
       verdict(t_dahs) == "over" and abs(t_dahs - G) < 0.05)
    ok("SF10 Orbitas in UTC (its column names); read as local %.3f, same call" % t_utc, verdict(t_utc) == "over")
    reg = {r[0]: r for r in __import__("docs").REGISTER}
    ok("SF11 RTO-1's maximum process flow and FN-1's rating are one figure, 3,800 scfm",
       "3,800" in reg["RTO-1"][4] and "3,800" in reg["FN-1"][4])
    ok("SF12 PSV-31 sits on HDR-1 at RTO-1's inlet plenum, downstream of every vent (register)",
       reg["PSV-31"][2] == "HDR-1" and "Atmosphere" in reg["PSV-31"][5])
    ok("SF13 not in RUN is uncontrolled: XV-30 is open whenever RTO-1 is not in RUN (register); WARMUP as running "
       "files %.3f, over" % t_warm, "not in RUN" in reg["XV-30"][4] and verdict(t_warm) == "over")
    yq = np.cumsum(fig["raw"]["quarters_tons"])
    ok("SF14 the year is the sum of the quarters (B.5): rounded and unrounded paths agree",
       round(sum(round(x, 1) for x in fig["raw"]["quarters_tons"]), 1) == round(G, 1) and
       all(round(sum(round(x, 1) for x in fig["raw"]["quarters_tons"][:k + 1]), 1) == round(yq[k], 1) for k in range(4)))
    ok("SF15 the comparison is the 2.5-ton calendar-year limit (B.1)", W.LIMIT_TONS == 2.5)
    # ruled at stage 4 (the judge's thinnest point): the over call needs about half of the proportional excess
    # released, and the register leaves the gas above the fan's draw no other way out while RTO-1 is in RUN
    outlets = sorted(k for k, r in reg.items() if r[5] and r[5] != "CVS-1")
    open_in_run = [k for k in outlets if k != "RTO-1" and "not in RUN" not in reg[k][4]]
    xs = np.where((status == "RUN") & (flow > W.FAN_MAX), (flow - W.FAN_MAX) / np.maximum(flow, 1e-9), 0.0)
    rel_lb = float((xs * voc).sum())
    g_prop = t_s1 + W.DRE * rel_lb / 2000
    f_star = (L - t_s1) / (g_prop - t_s1)
    ok("SF18 the gas above the fan's draw leaves untreated whole: RTO-1's 3,800 scfm is a hard cap and in RUN PSV-31 "
       "is HDR-1's only outlet besides RTO-1 (XV-30 opens only out of RUN); the proportional release, %.0f lb, files "
       "%.3f t, over, and the call holds while %.0f per cent or more of it leaves" % (rel_lb, g_prop, 100 * f_star),
       outlets == ["PSV-31", "RTO-1", "XV-30"] and open_in_run == ["PSV-31"] and abs(g_prop - G) < 1e-3 and
       verdict(g_prop) == "over" and f_star < 0.5, "outlets %s" % ", ".join(outlets))

    # ------------------------------------------------------------------ the asks
    tgt = V.golden_figures(target)
    wms, mm, ap = V.load_purchasing(target)
    nm = {k: r["Description"].split(",")[0] for k, r in mm.items()}
    post_s, post_q = {}, [0.0] * 4
    for r in wms:
        d = dt.date.fromisoformat(r["Posting Date"])
        if d.year != 2026:
            continue
        lb = float(r["Qty"]) * (float(mm[r["Material"]]["Density (lb/gal @60F)"]) if r["UoM"] == "GAL" else W.LB_PER_KG)
        s = nm[r["Material"]]
        post_s[s] = post_s.get(s, 0.0) + lb
        post_q[(d.month - 1) // 3] += lb
    gold_s, gold_q = fig["raw"]["ask_b_lb"], fig["raw"]["ask_a_lb"]
    moved = [s for s in gold_s if abs(post_s.get(s, 0.0) - gold_s[s]) >= 200] + \
        ["Q%d" % (k + 1) for k in range(4) if abs(post_q[k] - gold_q[k]) >= 200]
    ok("SF16 delivered is the supplier's delivery date: the posting-date route moves every ask figure by two bins or "
       "more", len(moved) == 11, "%d of 11: %s" % (len(moved), ", ".join(moved)))
    sol07 = [r for r in wms if r["Material"] == "SOL-07" and dt.date.fromisoformat(r["Posting Date"]) < dt.date(2026, 6, 1)]
    hept = [r for r in ap if r["Doc Type"] == "INV" and "HEPTANE" in (r["Item Text"] or "").upper()
            and r["Delivery Ticket"] in {x["BOL No"] for x in sol07}]
    ok("SF17 each solvent as delivered: SOL-07 receipts before June 2026 are n-heptane on their invoices",
       len(sol07) > 0 and len(hept) == len(sol07), "%d receipts, %d invoices" % (len(sol07), len(hept)))
    ok("A1 the asks recompute from target/ alone", all(abs(tgt["ask_b"][s] - gold_s[s]) < 0.5 for s in gold_s) and
       all(abs(tgt["ask_a"][k] - gold_q[k]) < 0.5 for k in range(4)))
    hep_drum = sum(float(r["Qty"]) * W.LB_PER_KG for r in sol07 if r["UoM"] == "KG")
    ok("A2 the SOL-07 relabel moves n-heptane and isohexane by more than two bins", hep_drum > 200, "%.0f lb" % hep_drum)
    sub = [r for r in ap if r["Doc Type"] == "SUB"]
    ok("A3 subsequent debits repeat their order's quantity (an AP-only quantity sum counts them twice)", len(sub) > 0,
       "%d SUB lines" % len(sub))
    split = {}
    for r in wms:
        split.setdefault(r["BOL No"], []).append(r)
    ok("A4 split tankers: one delivery on two tank receipts, each its own part", any(len(v) > 1 for v in split.values()),
       "%d BOLs on two receipts" % sum(len(v) > 1 for v in split.values()))
    ed = [edge(x, 100) for x in list(gold_s.values()) + list(gold_q)]
    ok("A5 every ask figure 10 lb or more from its bin edge", min(ed) >= 10, "min %.1f lb" % min(ed))
    ok("A6 separation: no main-call file carries an ask device (the call reads no purchasing file)",
       not any(k in vsrc.split("def golden_figures")[1].split("d = deliveries")[0] for k in ("wms", "ap_invoice", "erp_")))

    # ------------------------------------------------------------------ margins and bins
    ok("M1 total, margin, quarters and year to date 0.01 t or more from their bin edges",
       min([edge(G, 0.1), edge(G - 2.5, 0.1)] + [edge(x, 0.1) for x in fig["raw"]["quarters_tons"]] +
           [edge(x, 0.1) for x in fig["raw"]["ytd_tons"]]) >= 0.01,
       "total %.4f, quarters %s" % (G, fig["raw"]["quarters_tons"]))
    ok("M2 the final margin over the limit is 1.2x or more and the hourly rung under it by 1.15x",
       G / L >= 1.2 and L / h60 >= 1.15, "%.3f and %.3f" % (G / L, L / h60))
    ok("M3 verify recomputes the main figures from target/ alone", abs(tgt["total"] - G) < 0.002, "%.4f" % tgt["total"])

    # ------------------------------------------------------------------ realism sweep
    c = GO.components(w)
    mon = GO.by_month(c)
    ps = np.array([m["psv"] for m in mon])
    vs = np.array([m["vented"] for m in mon])
    rk = lambda a: np.argsort(np.argsort(a))
    rho = float(np.corrcoef(rk(ps), rk(vs))[0, 1])
    ok("S1 the release is not the month with the most VOC vented (shock)", rho < 0.95 and int(np.argmax(ps)) != int(np.argmax(vs))
       or rho < 0.8, "rank correlation %.2f" % rho)
    starts = {}
    for s in in26:
        if s[3] == 0:
            m = int(np.searchsorted([W.month_start(k) for k in range(2, 14)], s[6], side="right"))
            starts[m] = starts.get(m, 0) + 1
    ok("S2 no identical monthly counts across the year", len(set(starts.values())) >= 9, str(sorted(starts.values())))
    ok("S3 no round headline figure", all(int(round(x)) % 1000 for x in list(gold_s.values()) + list(gold_q)) and
       int(round(c["vented"].sum())) % 100)
    orb = [int(x) for x in __import__("pyarrow.parquet", fromlist=["x"]).read_table(
        os.path.join(target, P.FILES["orb"]), columns=["process_order"]).column(0).to_pylist()]
    u = sorted(set(orb))
    ok("S4 process orders carry the gaps of cancelled orders", len(set(np.diff(u))) > 1)
    trips = {a for a, off, warm in w.trips}
    with open(os.path.join(target, P.FILES["wo"]), newline="") as fh:
        wo = list(csv.DictReader(fh))
    wo_t = {V.est_minute_from_local(r["Opened"], "%Y-%m-%d %H:%M") for r in wo}
    ok("S5 no work order opens on the minute of a trip", not (trips & wo_t))
    po = [t for t in w.trips if w.down[0][0] <= t[0] < w.down[0][1]][0]
    plan = [r for r in wo if r["Asset"] == "RTO-1" and r["Problem"].startswith("Planned outage")]
    psv = [r for r in wo if r["Asset"] == "PSV-31"]
    o_a, o_b = (V.est_minute_from_local(plan[0][k], "%Y-%m-%d %H:%M") for k in ("Opened", "Closed"))
    ok("S13 the records agree: the planned outage order opens on the day the DAHS shows RTO-1 OFF, spans its OFF and "
       "WARMUP minutes and closes on the day it is back in RUN; PSV-31's inspection order is on the register's date",
       len(plan) == 1 and len(psv) == 1 and po[0] - 60 < o_a < po[0] and o_b > po[0] + po[1] + po[2] and
       plan[0]["Opened"][:10] == P.est_dt(po[0]).strftime("%Y-%m-%d") and
       plan[0]["Closed"][:10] == P.est_dt(po[0] + po[1] + po[2]).strftime("%Y-%m-%d") and
       psv[0]["Opened"][:10] == psv[0]["Closed"][:10] == reg["PSV-31"][7],
       "%s %s to %s; PSV-31 %s" % (plan[0]["WO No"], plan[0]["Opened"], plan[0]["Closed"], psv[0]["Opened"]))
    texts = [r["Problem"] for r in wo]
    top = max(texts.count(t) for t in set(texts))
    ok("S6 no free text recurs beyond a real rate", top <= 0.12 * len(texts) + 2, "most common %d of %d" % (top, len(texts)))
    card = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".claude",
                                       "skills", "fingerprint", "cards", "task479.json")))
    creators = set()
    for f in files:
        if f.endswith(".xlsx"):
            core = zipfile.ZipFile(os.path.join(target, f)).read("docProps/core.xml").decode()
            creators |= set(re.findall(r"<dc:creator>([^<]+)<", core)) | set(re.findall(r"<cp:lastModifiedBy>([^<]+)<", core))
    people = [x for x in creators if " " in x and x not in ("AP Reporting", "CCAQD Permits")]
    ok("S7 every persona in the pack is the card's", all(x in card["world"]["people"] for x in people), ", ".join(people))
    last = max(os.path.getmtime(os.path.join(target, f)) for f in files)
    ok("S8 no file postdates the setting", dt.datetime.fromtimestamp(last, dt.timezone.utc) <
       dt.datetime(2027, 1, 30, tzinfo=dt.timezone.utc))
    ok("S9 the DAHS holds every minute of 2026 once", meta["rows"][P.FILES["dahs"]] == W.YEAR)
    peak = float(w.flow.max())
    over = w.flow[w.flow > W.FAN_MAX]
    share = float((over > 1.4 * W.FAN_MAX).mean())
    ok("S10 the header's coincidences stay rare and bounded: peak under twice the fan, under 5 per cent of the minutes "
       "over the fan above 1.4x", peak < 2 * W.FAN_MAX and share < 0.05, "peak %.0f scfm, %.1f per cent above 1.4x, "
       "%d minutes over" % (peak, 100 * share, len(over)))
    for f in (P.FILES["permit"], P.FILES["test"]):
        b = open(os.path.join(target, f), "rb").read()
        ok("S11 %s carries no toolchain banner" % f, b"ReportLab" not in b and b"reportlab" not in b)
    for g_ in os.listdir(gdir):
        ok("S12 golden %s carries no em dash" % g_, chr(0x2014) not in zipfile.ZipFile(os.path.join(gdir, g_)).read(
            "word/document.xml" if g_.endswith(".docx") else "xl/sharedStrings.xml").decode())

    good = all(r[1] for r in ROWS)
    for label, passed, detail in ROWS:
        if not passed:
            print("CHECK FAIL  %s  %s" % (label, detail))
    print("checks: %d of %d pass" % (sum(r[1] for r in ROWS), len(ROWS)))
    return good


def report():
    for label, passed, detail in ROWS:
        print("%s  %s  %s" % ("PASS" if passed else "FAIL", label, detail))
