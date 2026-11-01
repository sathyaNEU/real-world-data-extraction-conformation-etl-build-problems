"""The generator's assertions on the installed pack: the three rules (R1 to R3c), every semantic fork (SF ids of the
design note), mess neutrality for each Layer 1 item, the input gates, the realism sweep, every graded figure's
distance to its bin edge, the truth replays and the ask layer's ceiling.

    python3 task160/generator/checks.py"""
import datetime as dt
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import ceiling as CE  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import verify as V  # noqa: E402
import world as W  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def bin_edge(v):
    """Distance from v to the nearer edge of its nearest-100 bin."""
    return 50.0 - abs(v - A.r100(v))


def doc_texts():
    t = {}
    for fn in os.listdir(TARGET):
        p = os.path.join(TARGET, fn)
        if fn.endswith(".pdf"):
            t[fn] = V.pdf_text(p)
        elif fn.endswith(".docx"):
            t[fn] = V.docx_text(p)
        elif fn.endswith(".xlsx") and "Register" in fn:
            t[fn] = " ".join(" ".join(r) for rows in V.xlsx_sheets(p).values() for r in rows)
    return t


def main():
    Pk = A.Pack(TARGET)
    g = Pk.golden()
    rungs = Pk.rungs()
    var = Pk.variants()
    figs = A.figures(Pk)
    fj = json.load(open(os.path.join(HERE, "figures.json")))["figures"]
    texts = doc_texts()
    alltext = " ".join(texts.values())

    # ---------------- the call and its components
    check("call: golden net change rounds to %d" % figs["call_net_change"], figs["call_net_change"] == 300,
          "%.1f" % g["net"])
    check("call: QT reviews added round to 500", figs["qt_reviews_added"] == 500, "%.1f" % g["qt_add"])
    check("call: current reviews lost round to 200", figs["current_reviews_removed"] == 200, "%.1f" % g["pre"])
    check("bin edge: net change at least 25 from its edge", bin_edge(g["net"]) >= 25, "%.1f" % bin_edge(g["net"]))
    check("bin edge: QT added at least 25 from its edge", bin_edge(g["qt_add"]) >= 25, "%.1f" % bin_edge(g["qt_add"]))
    check("bin edge: reviews lost at least 25 from its edge", bin_edge(g["pre"]) >= 25, "%.1f" % bin_edge(g["pre"]))
    check("figures.json carries the generator's figures", fj == figs)

    # ---------------- the three rules
    check("R1 analyst test: the silent-mode route files 500, two bins off", A.r100(rungs["R0_silent_mode"]) == 500,
          "%.1f" % rungs["R0_silent_mode"])
    w = W.build_world()
    B0, B1 = W.tnum(P.BG_START), W.tnum(P.LOG_END + dt.timedelta(days=1))
    clean_qt = sum(1 for e in w["encs"] if e.unit in P.LIVE_UNITS for b in w["bg"][e.key]
                   if b[1] == "MSP26_QT_COMBO" and B0 <= b[3] < B1)
    clean_default = clean_qt * (1 - P.P_REMOVE["MSP26_QT_COMBO"]) * g["scale"]
    check("R1 on the clean truth: the silent-mode route at the world's own override share files 500",
          A.r100(clean_default) == 500, "%.1f" % clean_default)
    banned = ["no longer", "pre-empt", "preempt", "suppress", "never fire", "will not fire", "fewer", "cascade",
              "downstream", "takes away", "knock-on"]
    hits = [b for b in banned if b in alltext.lower()]
    check("R2 no decoy: no filed document names a downstream effect of the package's alerts", not hits, str(hits))
    nums = re.findall(r"\b(\d{3})\s+(?:more\s+)?reviews\b", alltext)
    check("R2 no decoy: no filed document carries a review forecast", not nums, str(nums))
    check("R3a not semantics: conformed pack (crosswalk, boundary days, UTC, severity) still files 500 by default",
          A.r100(Pk.call(c=0.0)["net"]) == 500, "%.1f" % Pk.call(c=0.0)["net"])
    sched = [t for k, t in texts.items() if k.startswith("Corvane_QRMC_Service_Schedule")][0]
    c43 = sched[sched.index("4.3 Content changes"):sched.index("5. Service level")]
    check("R3b not rule application: the content-change clause files the WHAT and names no removal, order or link",
          "prescribers answering its alerts" in c43 and not re.search(r"remov|interact|order|active", c43.lower().replace("change order", "")))
    enum = sorted(A.r100(v) for v in rungs.values())
    check("R3c enumerated family spans at least four bins", len(set(enum)) >= 4, str(enum))
    std = [v["net"] for v in var.values()]
    check("R3c standing family inside one bin", all(A.r100(x) == 300 for x in std),
          "%.1f to %.1f" % (min(std), max(std)))
    check("R3c standing family spread under 60 reviews", max(std) - min(std) < 60, "%.1f" % (max(std) - min(std)))
    check("ladder: own-order-only rung lands off the golden", A.r100(rungs["R1_own_order_only"]) != 300,
          "%.1f" % rungs["R1_own_order_only"])
    check("ladder: every duplicate removed lands off the golden", A.r100(rungs["R3_every_duplicate_removed"]) != 300,
          "%.1f" % rungs["R3_every_duplicate_removed"])
    check("ladder: whole-encounter removal lands off the golden", A.r100(rungs["R4_whole_encounter"]) != 300,
          "%.1f" % rungs["R4_whole_encounter"])
    check("ladder: counting duplicate-opioid acknowledgements as reviews lands off the golden",
          A.r100(rungs["R0b_duplicate_alerts_as_reviews"]) != 300, "%.1f" % rungs["R0b_duplicate_alerts_as_reviews"])
    check("Gate F: exactly one rung reaches the golden's bin",
          sum(A.r100(v) == 300 for v in rungs.values()) == 1)

    # ---------------- semantic forks
    check("SF1 one overridden alert is one review (Schedule B 2.1), and no QT order carries two QT alerts",
          "One overridden alert is one review." in sched
          and Pk.bg[Pk.bg["rule_id"] == A.QT].groupby("order_id").size().max() == 1)
    wk = Pk.plan[(Pk.plan["week"] >= A.FC0) & (Pk.plan["week"] < A.FC0 + dt.timedelta(weeks=13))]
    check("SF2 the 13 weeks from 4 January 2027 are 13 plan weeks ending with the week of 29 March",
          sorted(wk["week"].unique())[-1] == dt.datetime(2027, 3, 29) and wk["week"].nunique() == 13)
    pil = Pk.hist[Pk.hist["dept"].isin(Pk.pilot)]
    check("SF3 the pilot units already run the package live over the whole record (no change at go-live)",
          (pil["alert_rule_id"] == A.DUP).any() and pil["t"].min() < dt.datetime(2025, 1, 2)
          and not Pk.bg["department"].isin(Pk.pilot).any())
    nonp = Pk.hist[Pk.hist["dept"].isin(Pk.going_live)]
    check("SF4 without the go-live the package stays out of sight: no MSP26 alert in the going-live units' history",
          not nonp["alert_rule_id"].str.startswith("MSP26").any())
    rates = [v for k, v in var.items() if k.startswith("rates")]
    check("SF5 every pilot-rate window and grouping gives the same call", all(A.r100(v["net"]) == 300 for v in rates),
          ", ".join("%.0f" % v["net"] for v in rates))
    pj = [var["projection admissions"], var["projection patient_days"], var["projection by unit"]]
    check("SF6 admissions, patient days or unit-by-unit on the volume plan give the same call",
          all(A.r100(v["net"]) == 300 for v in pj) and "inpatient volume plan" in sched)
    check("SF6 the plan-free weekly scaling (ruled out by Schedule B 4.1) also lands in the bin",
          A.r100(var["projection weeks"]["net"]) == 300, "%.1f" % var["projection weeks"]["net"])
    bp = [var["base 13 weeks to 25 Oct"], var["base from 13 Jul"], var["base Jul to Sep"]]
    check("SF7 every base period gives the same call", all(A.r100(v["net"]) == 300 for v in bp),
          ", ".join("%.0f" % v["net"] for v in bp))
    check("SF8 product or additive combination of removal chances gives the same call",
          A.r100(var["additive removal"]["net"]) == 300)
    check("SF9 QT background rows on orders removed by another alert, dropped or kept, give the same call",
          A.r100(var["QT rows on removed orders kept"]["net"]) == 300)
    check("SF10 the repeated boundary days, dropped or kept, give the same call",
          A.r100(var["boundary duplicates kept"]["net"]) == 300 and Pk.raw_rows > len(Pk.hist))
    only_new = Pk.hist[Pk.hist["department"].isin(Pk.units)]
    keep = Pk.hist
    Pk.hist = only_new
    v11 = Pk.call()
    Pk.hist = keep
    check("SF11 dropping the rows under pre-upgrade department names gives the same call",
          A.r100(v11["net"]) == 300, "%.1f" % v11["net"])
    keepbg = Pk.bg
    Pk.bg = keepbg.assign(t=A.pd.to_datetime(keepbg["eval_utc"].str.replace("Z", "").str.replace("T", " ")))
    v12 = Pk.call()
    Pk.bg = keepbg
    check("SF12 reading the background log's UTC stamps as local time gives the same call",
          A.r100(v12["net"]) == 300, "%.1f" % v12["net"])
    fw = W.forecast_world()
    t0, t1 = W.tnum(P.FC_START), W.tnum(P.FC_END + dt.timedelta(days=1))
    truth, _off, _on = W.truth_net(fw, t0, t1, list(range(1, 13)))
    check("SF13 the replayed truth of the forecast weeks sits within 60 of the golden",
          abs(truth - g["net"]) <= 60, "truth %.1f golden %.1f" % (truth, g["net"]))
    eb = [e for e in w["encs"] if e.unit in P.LIVE_UNITS and e.dis >= B0 and e.adm < B1]
    new_rev = 0
    salts = list(range(1, 9))
    for e in eb:
        r0, _ = W.run(e, lambda t: "off", 0)
        k0 = {(x[0], x[1], x[2]) for x in r0 if x[1] in P.REVIEW_RULES and x[4] == "Overridden" and B0 <= x[3] < B1}
        for s_ in salts:
            r1, _ = W.run(e, lambda t: "live", s_)
            k1 = {(x[0], x[1], x[2]) for x in r1 if x[1] in P.EXISTING_HIGH and x[4] == "Overridden"
                  and B0 <= x[3] < B1}
            new_rev += len(k1 - k0)
    second = new_rev / len(salts) * g["scale"]
    check("SF13 the second-order term (orders a pre-empted alert would have removed survive) is under 30 and "
          "leaves the call in its bin", second < 30 and A.r100(g["net"] + second) == 300,
          "%.1f projected" % second)
    check("SF14 nearest 100 is stated; truncation would file 200", A.r100(g["net"]) == 300 and int(g["net"]) // 100 *
          100 == 200)

    # ---------------- Layer 1 mess neutrality
    check("L1 the pre-upgrade department names map through the register's Units sheet",
          set(Pk.hist_all["department"]) - set(Pk.units) <= set(Pk.old2code))
    check("L1 quarterly boundary days repeated in the history (seven pulls)", Pk.raw_rows - len(Pk.hist) > 100,
          "%d repeated rows" % (Pk.raw_rows - len(Pk.hist)))
    check("L1 the background log is in UTC and the history in local time",
          Pk.bg["eval_utc"].str.endswith("Z").all() and not Pk.hist["alert_dttm"].str.contains("Z").any())
    check("L1 spring-forward hour absent from the local history",
          not Pk.hist["alert_dttm"].str.startswith("2026-03-08 02:").any())

    # ---------------- the asks
    a, b = Pk.ask_a(), Pk.ask_b()
    check("ask A: every ward figure at least 0.15 h from its rounding edge",
          all(abs((v % 1) - 0.5) >= 0.15 for v in a.values()), str({k: round(v, 2) for k, v in a.items()}))
    amap = Pk.ask_a(ward="map")
    moved = [u for u in Pk.going_live if int(a[u] + 0.5) != int(amap[u] + 0.5)]
    pairs = {x for _w, p1, p2 in P.DECANT for x in (p1, p2)}
    check("ask A device: Corvane's location map misattributes every decant ward and no other", set(moved) == pairs,
          str(moved))
    qq = Pk.queue
    straddle = sum(int(((qq["claimed_et"] < e) & (qq["closed_et"] >= e)).sum())
                   for e in (A.pd.Timestamp("2026-07-01"), A.pd.Timestamp("2026-10-01")))
    check("ask A: no desk session straddles 1 July or 1 October Eastern, so splitting a session at the quarter's "
          "edge files the same hours", straddle == 0, str(straddle))
    ah = Pk.ask_a(time="handle_all")
    check("ask A hazard: summed handle minutes miss every ward",
          all(int(a[u] + 0.5) != int(ah[u] + 0.5) for u in Pk.going_live))
    bt = Pk.ask_b(count="tasks")
    check("ask B device: counting tasks misses every month-shift cell", all(b[k] != bt[k] for k in b))
    bu = Pk.ask_b(clock="utc")
    check("ask B hazard: shifts read in UTC miss every cell", all(b[k] != bu.get(k) for k in b))
    # truth of the asks from the world
    R = PK.relabel(w)
    unit_of_alert = {aid: R["enc_by"][ek].unit for (t, o, ro, pid, ek, r), aid in zip(R["alerts"], R["aid"])}
    q = Pk.q3_sessions()
    tru = {}
    for ref, c0, c1 in zip(q["alert_ref"], q["claimed_et"], q["closed_et"]):
        u = unit_of_alert[int(ref)]
        tru[u] = tru.get(u, 0.0) + (c1 - c0).total_seconds() / 3600.0
    check("ask A golden equals the world's desk time by ward", all(abs(tru.get(u, 0) - a[u]) < 1e-6
                                                                   for u in Pk.going_live))
    msg_n = {}
    for (t, o, ro, pid, ek, r), aid in zip(R["alerts"], R["aid"]):
        if r[1] in P.REVIEW_RULES and r[4] == "Overridden":
            msg_n[(o, t)] = msg_n.get((o, t), 0) + 1
    first = {}
    for (t, o, ro, pid, ek, r), aid in zip(R["alerts"], R["aid"]):
        if r[1] in P.REVIEW_RULES and r[4] == "Overridden" and (o, t) not in first:
            first[(o, t)] = aid
    n_of = {aid: msg_n[k] for k, aid in first.items()}
    qs = q[q["close_status"] == "Signed off"]
    tb = {}
    for ref, c1 in zip(qs["alert_ref"], qs["closed_et"]):
        k = (c1.strftime("%Y-%m"), A.shift_of(c1))
        tb[k] = tb.get(k, 0) + n_of[int(ref)]
    check("ask B golden equals the world's overridden alerts on signed-off tasks, by month and shift",
          all(tb.get(k) == v for k, v in b.items()))
    msgs = Pk.bundle_size()
    check("ask B device mass: at least 6 per cent of tasks carry two or more alerts",
          sum(1 for v in msgs.values() if v > 1) / len(msgs) >= 0.06,
          "%.3f" % (sum(1 for v in msgs.values() if v > 1) / len(msgs)))
    pair, leak, crack, n = CE.main(TARGET)
    check("ceiling: pair at or under 60", pair <= 60, "%.1f" % pair)
    check("ceiling: mirror leakage under 50 per cent", leak < 50, "%.1f" % leak)
    check("separation: no ask device row in the call's population (decant only in the queue's point of care)",
          not Pk.hist["department"].str.contains(r"\^").any() and "poc_location" not in Pk.hist.columns)

    # ---------------- house fixes: the record obeys the stated mechanism, every PDF reads back with every reader
    h = Pk.hist
    removed_orders = set(h.loc[h["user_action"] == "Order removed", "order_id"])
    refs = int(h["interacting_order_id"].isin(removed_orders).sum())
    check("H6 the record obeys the golden's rule: no alert in the history names a removed order as the order it fired "
          "against", len(removed_orders) > 1000 and refs == 0,
          "%d removed orders, %d alerts naming one" % (len(removed_orders), refs))
    import pypdf
    from pdfminer.high_level import extract_text
    phrases = {"Corvane_QRMC_Service_Schedule_B_rev3.pdf": ["One overridden alert is one review", "4.3 Content changes",
                                                           "prescribers answering its alerts"],
               PK.FILES["release"]: ["evaluate like every rule in the engine", "Background mode"]}
    ok_all = True
    for fn, want in phrases.items():
        p = os.path.join(TARGET, fn)
        t1 = " ".join(pg.extract_text() for pg in pypdf.PdfReader(p, strict=True).pages)
        t2 = extract_text(p)
        t3 = V.pdf_text(p)
        for w_ in want:
            for t in (t1, t2, t3):
                if w_ not in " ".join(t.split()):
                    ok_all = False
    check("H25 every governing PDF reads back its WHAT sentences under pypdf (strict), pdfminer and the verifier",
          ok_all)

    # ---------------- input gates and realism
    files = os.listdir(TARGET)
    exts = {os.path.splitext(f)[1] for f in files}
    check("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    check("input gate: 3 or more formats", len(exts) >= 3, str(sorted(exts)))
    check("input gate: a file of 25,000 rows or more", len(Pk.hist_all) >= 25000, str(len(Pk.hist_all)))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("input gate: two or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2)
    check("input gate: every file carries source, date and license",
          all(set(v) >= {"source", "date", "license"} for v in meta["files"].values()))
    check("realism: no file name carries an author's word",
          not [f for f in files if re.search(r"test|trap|decoy|golden|answer|synthetic|stump", f, re.I)])
    data_text = ""
    for f in files:
        if f.endswith(".csv"):
            data_text += open(os.path.join(TARGET, f), encoding="utf-8").read(200000)
    check("realism: no shipped data file says synthetic", "synthetic" not in (data_text + alltext).lower())
    card = json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task160.json")))
    people = set(card["world"]["people"])
    named = set(re.findall(r"(Chris Hernandez|Shawn Whitaker|Andrew Harvey|[A-Z][a-z]+ [A-Z][a-z]+(?=, (?:Director|"
                           r"Chief|Pharmacy Informatics Manager)))", alltext))
    check("realism: every person named in the documents is on the card", named <= people, str(named))
    dates = re.findall(r"20\d\d-\d\d-\d\d", data_text)
    late = [d for d in dates if d > "2026-10-28"]
    check("realism: no event in the extracts after the as-of date", not late, str(late[:3]))
    z = zipfile.ZipFile(os.path.join(TARGET, PK.FILES["cr"]))
    core = z.read("docProps/core.xml").decode()
    check("realism: Word and Excel properties carry the organisations' own authors",
          "Shawn Whitaker" in core and "python" not in core.lower())

    bad = [r for r in RESULTS if not r[1]]
    for name, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name, ("  [" + detail + "]") if detail else ""))
    print("checks: %d of %d pass" % (len(RESULTS) - len(bad), len(RESULTS)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
