"""Generator checks for task255, run on the installed target/ and on the clean truth the generator holds.

    python3 task255/generator/checks.py [target_dir]

Blocks: input gates; R1 to R3c (the three rules, executed); the semantic fork table (one assertion or more per SF
row); the ladder; bin clearance of every graded figure; the asks (golden equals truth, the cracker's stops miss);
the separation line; the realism sweep. Exit 1 on any failure."""
import collections
import datetime as dt
import heapq
import json
import math
import os
import re
import shutil
import statistics
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as AN  # noqa: E402
import asks_world as AW  # noqa: E402
import io_util as IO  # noqa: E402
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %s  %s" % ("PASS" if ok else "FAIL", label, detail))


def edge(v, unit):
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def r(v):
    return int(math.floor(v + 0.5))


def main(target):
    t0 = dt.datetime.now()
    w = W.build(P.SEED)
    A = w.asks
    golden_codes = ["OVP", "OST", "ZDT"]
    G = AN.main_call(target)
    gfig = {k: r(v) for k, v in G.reach.items()}

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    check("G1 ten or more files", len(files) >= 10, "%d files" % len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    check("G2 three or more formats", len(exts) >= 3, ", ".join(sorted(exts)))
    nj = sum(1 for _ in open(os.path.join(target, PK.FILES["journeys"]))) - 1
    check("G3 a file of 25,000 rows or more", nj >= 25000, "%s: %d rows" % (PK.FILES["journeys"], nj))
    meta = json.load(open(os.path.join(TASK, "metadata.json"))) if os.path.exists(os.path.join(TASK, "metadata.json")) else {}
    dis = meta.get("distractor_files", [PK.FILES[k] for k in PK.DISTRACTORS])
    check("G4 two or more distractors, none named as such", len(dis) >= 2 and all(d in files for d in dis)
          and not any("distract" in f.lower() for f in files), ", ".join(dis))
    bad_names = [f for f in files if re.search(r"readme|dictionar|notes|manifest|codebook|schema|field", f, re.I)]
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            import openpyxl
            sheets += [(f, s) for s in openpyxl.load_workbook(os.path.join(target, f), read_only=True).sheetnames]
    bad_sheets = [s for s in sheets if re.search(r"readme|dictionar|notes|manifest|toelichting|uitleg|legend", s[1], re.I)]
    check("G5 no file or sheet that describes the data", not bad_names and not bad_sheets, "%d sheets read" % len(sheets))
    used = set(AN.FILES.values())
    check("G6 the analysis reads no distractor", not (used & set(dis)), "analysis reads %d files" % len(used))
    tmp = tempfile.mkdtemp()
    for f in files:
        if f not in dis:
            shutil.copy(os.path.join(target, f), os.path.join(tmp, f))
    M2 = AN.main_call(tmp)
    same = (M2.tier == G.tier and {k: r(v) for k, v in M2.reach.items()} == gfig and AN.make_good(tmp) == AN.make_good(target)
            and AN.screens_on_sale(tmp) == AN.screens_on_sale(target) and AN.net_revenue(tmp) == AN.net_revenue(target))
    check("G7 every distractor deleted: the call and every ask unchanged", same)
    shutil.rmtree(tmp)

    # ------------------------------------------------------------------ R1: the field's raw material ships
    head = open(os.path.join(target, PK.FILES["journeys"])).readline().strip().split(",")
    check("R1 the journeys ship at journey grain with both gates and both times",
          {"card_id", "travel_date", "check_in_time", "check_in_gate", "check_out_time", "check_out_gate"} <= set(head),
          ",".join(head))
    deciding = re.compile(r"reach|pass|route|interwork|through|change|overstap|transfer|via", re.I)
    cols = list(head)
    for f in files:
        if f.endswith(".csv"):
            cols += open(os.path.join(target, f), encoding="utf-8").readline().strip().replace(";", ",").split(",")
        elif f.endswith(".xlsx"):
            import openpyxl
            for sh in openpyxl.load_workbook(os.path.join(target, f), read_only=True).sheetnames:
                cols += [str(c) for c in IO.read_xlsx(os.path.join(target, f), sh)[0] if c is not None]
    hits = sorted({c for c in cols if deciding.search(c) and c not in ("passage_code", "passage_name")})
    check("R1 no shipped column holds a route, a change or a pass count", not hits, ", ".join(hits) or "none")
    check("R1 the golden reads each journey's duration at Centraal", G.classified["read: change"] > 500
          and G.classified["read: no change"] > 5000, dict(G.classified))

    # ------------------------------------------------------------------ R2: each Layer 1 item real and neutral
    S = AN.main_call(target, halls="station")
    check("R2 gates re-coded at four stations and names in two spellings: halls by stop give the same call and figures",
          S.tier == G.tier and {k: r(v) for k, v in S.reach.items()} == gfig)
    js = AN.load_journeys(target)
    names = collections.defaultdict(set)
    for row in IO.read_csv(os.path.join(target, PK.FILES["journeys"]))[1]:
        names[row[4]].add(row[5])
    check("R2 the re-export is real: four stops carry two spellings, gate codes in two formats",
          sum(1 for v in names.values() if len(v) == 2) == 4 and any("." in j["dev_in"] for j in js)
          and any(j["dev_in"].startswith("PZ-") for j in js))
    St = AN.main_call(target, staff=True)
    check("R2 staff and service cards kept by mistake: the call unchanged (the figures move one point, rate card 3.3)",
          St.tier == G.tier)
    Op = AN.main_call(target, open_journeys="drop")
    check("R2 journeys without a check-out dropped: the call and every figure unchanged",
          Op.tier == G.tier and {k: r(v) for k, v in Op.reach.items()} == gfig,
          "%d journeys without a check-out in the window" % sum(1 for j in G.window_journeys if not j["t_out"]))
    span = [j for j in js if j["date"] in (dt.date(2026, 10, 24), dt.date(2026, 10, 25)) and
            (90 <= AN.tmin(j["t_in"]) < 240 or (j["t_out"] and 90 <= AN.tmin(j["t_out"]) < 240))]
    Ck = AN.main_call(target, clock_shift=True)
    check("R2 local clock across 25 October: no journey in the night of the change, an hour's misreading moves nothing",
          not span and Ck.tier == G.tier and {k: r(v) for k, v in Ck.reach.items()} == gfig)
    reads = []
    orig = (IO.read_csv, IO.read_xlsx, IO.pdf_text)

    def spy(fn):
        def inner(path, *a, **k):
            reads.append(os.path.basename(path))
            return fn(path, *a, **k)
        return inner
    AN.IO.read_csv, AN.IO.read_xlsx, AN.IO.pdf_text = spy(orig[0]), spy(orig[1]), spy(orig[2])
    AN._CACHE.clear()
    AN.main_call(target)
    main_reads = set(reads)
    reads.clear()
    AN.make_good(target)
    AN.screens_on_sale(target)
    AN.net_revenue(target)
    ask_reads = set(reads)
    AN.IO.read_csv, AN.IO.read_xlsx, AN.IO.pdf_text = orig
    want_main = {PK.FILES[k] for k in ("journeys", "network", "products", "rate_card")}
    check("R2 the register's log, the player health in UTC and the two billing systems sit outside the main call",
          main_reads == want_main, ", ".join(sorted(main_reads)))
    check("SEP the asks never read the journeys, the network or the products", not (ask_reads & {PK.FILES[k] for k in
          ("journeys", "network", "products")}), ", ".join(sorted(ask_reads)))

    # ------------------------------------------------------------------ R3: the analyst test, the decisive step, no plant
    truth_lm = W.reach(w, "linemap")
    truth_g = W.reach(w, "truth")
    truth_0 = W.reach(w, "none")
    lm_set = sorted(c for c in truth_lm if truth_lm[c] >= 40)
    check("R3a the default path (every change where the line map puts it) on the clean truth files the wrong tier",
          lm_set == sorted(["CEN", "BNS", "OVP", "OST", "ZDT"]), ", ".join(lm_set))
    g_set = sorted(c for c in truth_g if truth_g[c] >= 40)
    check("R3b the default path with only the Centraal change read from durations files the golden",
          g_set == sorted(golden_codes) and sorted(G.tier) == g_set, ", ".join(g_set))
    z_set = sorted(c for c in truth_0 if truth_0[c] >= 40)
    check("R3b the rung below (the gates only) and its one correction (the line map's passages) stay wrong",
          z_set != g_set and lm_set != g_set, "gates only: %s" % (", ".join(z_set) or "none"))
    check("R3b the golden reproduces the clean truth's reach for every package to the rider",
          all(abs(G.reach[k] - truth_g[k]) < 1e-9 for k in truth_g))
    seqs = collections.defaultdict(list)
    for j in js:
        seqs[j["card"]].append((j["date"], j["t_in"], j["o"], j["d"]))
    sig = collections.Counter(tuple(v) for v in seqs.values() if len(v) > 4)
    check("R3c no copied block: no two cards share a journey history", max(sig.values()) == 1)
    day_counts = collections.Counter(j["date"] for j in js)
    check("R3c no repeated day: daily journey counts all differ within each weekday",
          all(len({day_counts[d] for d in day_counts if d.weekday() == wd}) == len([d for d in day_counts if d.weekday() == wd])
              for wd in range(7)))
    check("R3c no memo, draft, briefing or stakeholder figure ships", not any(re.search(r"memo|draft|brief|concept", f, re.I)
                                                                           for f in files))

    # ------------------------------------------------------------------ the semantic fork table
    B = AN.main_call(target, weeks_rule="blocks")
    check("SF1 a regular rider's weeks as calendar weeks or seven-day blocks: same riders, same call",
          B.regular == G.regular and B.tier == G.tier, "%d riders" % len(G.regular))
    Dc = AN.main_call(target, dating="checkout")
    check("SF2 a journey dated by check-out instead of check-in: same call and figures",
          Dc.tier == G.tier and {k: r(v) for k, v in Dc.reach.items()} == gfig)
    prod = IO.read_csv(os.path.join(target, PK.FILES["products"]))[1]
    check("SF3 staff and service cards are marked as such in the product list (rate card 3.3 leaves them out)",
          {p[0] for p in prod if p[2] != "reiziger"} == {"PER", "SRV"})
    check("SF4 a journey without a check-out kept at its check-in hall or dropped: same call and figures",
          Op.tier == G.tier and {k: r(v) for k, v in Op.reach.items()} == gfig)
    Jc = AN.main_call(target, count="journey")
    check("SF5 passes counted per journey instead of per place move figures (rate card 3.4 counts each place), not the call",
          Jc.tier == G.tier, "moves %s" % ", ".join(k for k in gfig if r(Jc.reach[k]) != gfig[k]))
    check("SF6 halls through the gate list or by stop: same call and figures",
          S.tier == G.tier and {k: r(v) for k, v in S.reach.items()} == gfig)
    net = G.net
    differ = 0
    for o in net["stops"]:
        for d in net["stops"]:
            if o != d and [x[:2] for x in AN.route(net, o, d)] != [x[:2] for x in fastest(net, o, d)]:
                differ += 1
    check("SF7 the route between two gates by fewest changes or by fastest time: the same route for every pair",
          differ == 0, "%d of %d pairs differ" % (differ, len(net["stops"]) * (len(net["stops"]) - 1)))
    flagged, through_share, n_off = duration_only_flips(target, G)
    check("SF8 off the peak a duration-only reading calls changes on straight-through trips in hours whose other trips "
          "came through Centraal faster than any change, so a timetable cannot back it; the line map holds there",
          flagged > 0.05 and through_share > 0.4,
          "%d trips at six minutes or more, %.0f per cent called changes, every such hour %.0f per cent or more through"
          % (n_off, 100 * flagged, 100 * through_share))
    fam = family(target)
    check("SF9 the minute a rider reaches Centraal estimated three minutes either side, or the service pattern read for "
          "every journey: same call and the same figure in every package",
          all(t == G.tier and f == gfig for t, f in fam.values()), ", ".join(sorted(fam)))
    check("SF10 the tier line on the unrounded or the whole-per-cent reach: same call (every package 4 points or more "
          "from the line)", min(abs(v - 40.0) for v in G.reach.values()) >= 4.0,
          "nearest %.2f points" % min(abs(v - 40.0) for v in G.reach.values()))
    check("SF11 the times after the clock change read an hour off: same call and figures",
          Ck.tier == G.tier and {k: r(v) for k, v in Ck.reach.items()} == gfig)
    check("SF12 every reach sits 0.15 of a point or more inside its whole-per-cent bin (rounding half up or half even)",
          min(edge(v, 1.0) for v in G.reach.values()) >= 0.15,
          ", ".join("%s %.2f" % (k, v) for k, v in G.reach.items()))

    # ------------------------------------------------------------------ the ladder
    R0, R1 = AN.main_call(target, "none"), AN.main_call(target, "linemap")
    RA, RS = AN.main_call(target, "allday"), AN.main_call(target, "stationpass")
    check("L1 rung 0 (the gates only) files Zuidtak alone", R0.tier == ["ZDT"], ", ".join(R0.tier))
    check("L2 rung 1 (the line map's changes) files Centraal, Binnenstad, Overstappunten, Oosttak and Zuidtak",
          sorted(R1.tier) == sorted(["CEN", "BNS", "OVP", "OST", "ZDT"]) and sorted(RS.tier) == sorted(R1.tier))
    check("L3 the golden files Overstappunten, Oosttak and Zuidtak", sorted(G.tier) == sorted(golden_codes))
    check("L4 the line map overstates Centraal and Binnenstad by 20 points or more",
          R1.reach["CEN"] - G.reach["CEN"] >= 20 and R1.reach["BNS"] - G.reach["BNS"] >= 20,
          "Centraal %.1f against %.1f" % (R1.reach["CEN"], G.reach["CEN"]))
    shoulder = shoulder_hours(target, G)
    check("L5 the peak pattern for every weekday hour is refuted in the three-minute shoulder hours (north-east riders "
          "change there, north-south riders do not), and it moves three figures",
          shoulder[0] > 0.9 and shoulder[1] < 0.05 and any(r(RA.reach[k]) != gfig[k] for k in ("CEN", "BNS", "OVP")),
          "north-east changes %.0f per cent, north-south %.0f per cent" % (100 * shoulder[0], 100 * shoulder[1]))

    # ------------------------------------------------------------------ ask A: make-good per autumn booking
    mg = AN.make_good(target)
    truth_mg = {b["ref"]: AW.make_good(A, b) for b in A.bookings}
    check("A1 the make-good golden equals the clean truth for every booking",
          all(mg[k]["make_good"] == truth_mg[k][1] for k in mg))
    fr = {k: v["dark"] - 0.005 * v["booked"] for k, v in mg.items()}
    check("A2 every make-good sits 0.2 of an hour or more inside its whole hour",
          all(0.2 <= x - math.floor(x) <= 0.8 for x in fr.values()),
          ", ".join("%.2f" % (x - math.floor(x)) for x in fr.values()))
    reg_mg = AN.make_good(target, mapping="register")
    check("A3 the cracker's stop (re-cabling on the register's dates) misses every booking",
          all(reg_mg[k]["make_good"] != mg[k]["make_good"] for k in mg))
    utc = AN.make_good(target, clock="utc")
    check("SF13 the player log read in local time instead of UTC moves the figures (the header says UTC, terms 6.1 local)",
          sum(utc[k]["make_good"] != mg[k]["make_good"] for k in mg) >= 8)
    noup = AN.make_good(target, takedowns=False)
    check("SF14 the take-down at its player's last report or at the day's opening: the same hours; ignoring it moves "
          "Noordtak's booking only", [k for k in mg if noup[k]["make_good"] != mg[k]["make_good"]] == ["SB-26-0415"]
          and takedown_open_same(target, mg))
    check("SF15 part of an hour counts as an hour (terms 6.3): rounded up, never to nearest",
          all(v["make_good"] == math.ceil(round(v["dark"] - 0.005 * v["booked"], 6)) for v in mg.values()))
    bk = AN.load_bookings(target)
    hours_ok = all(abs(b["booked"] - len(b["tags"]) * sum((AN.opening(b["start"] + dt.timedelta(days=i))[1] -
                   AN.opening(b["start"] + dt.timedelta(days=i))[0]).total_seconds() / 3600.0
                   for i in range((b["end"] - b["start"]).days + 1))) < 0.01 for b in bk)
    check("SF16 the booked screen-hours in the bookings equal the opening hours times the booked screens", hours_ok)
    check("SF22 the receiving player's display report dates each re-cabling inside the register's window",
          recab_consistent(target), "%d re-cablings" % len(A.failures))

    # ------------------------------------------------------------------ ask B: screens on sale on 1 January 2027
    sc = AN.screens_on_sale(target)
    AW.register_rows(A)
    check("B1 the screens golden equals the clean truth", sc == A.screens_2027, json.dumps(sc))
    lt = AN.screens_on_sale(target, "latest_no_pos")
    check("B2 the cracker's stop (each tag's latest row) misses every package", all(lt[k] != sc[k] for k in sc))
    st = AN.screens_on_sale(target, "status")
    check("B3 the status column read as of today misses eight packages or more", sum(st[k] != sc[k] for k in sc) >= 8)
    scr, cab = AN.load_register(target)
    check("SF17 no register row hangs or comes down on 1 January 2027 itself",
          not any(str(s["hung"])[:10] == "2027-01-01" or str(s["taken_down"] or "")[:10] == "2027-01-01" for s in scr))
    check("SF18 a screen held outside the packages carries no package and counts in none",
          any(s["package"] == "-" for s in scr) and "-" not in sc)

    # ------------------------------------------------------------------ ask C: net revenue per package
    rev = AN.net_revenue(target)
    trev = AW.net_revenue(A)
    check("C1 the net revenue golden equals the clean truth to the cent", all(abs(rev[k] - trev[k]) < 0.01 for k in rev))
    check("C2 every net revenue sits 2.5 euros or more inside its 10-euro bin", min(edge(v, 10) for v in rev.values()) >= 2.5,
          ", ".join("%s %.2f" % (k, edge(v, 10)) for k, v in rev.items()))
    stm = AN.net_revenue(target, commission="statements")
    miss = [k for k in rev if r(stm[k] / 10.0) != r(rev[k] / 10.0)]
    check("C3 the cracker's stop (each statement's amount shared over its bookings) misses every agency package",
          sorted(miss) == sorted(["CEN", "OVP", "OST", "WST", "ZDT", "RNG", "EIN"]), ", ".join(miss))
    gross = AN.net_revenue(target, vat="gross")
    check("SF19 legacy invoices read with their VAT (the header says incl. btw; terms 8.3 exclude it) miss every package",
          all(r(gross[k] / 10.0) != r(rev[k] / 10.0) for k in rev))
    std = AN.net_revenue(target, commission="standard")
    check("SF20 the rate card's standard 15 per cent instead of each agency's contract rate misses every agency package",
          all(r(std[k] / 10.0) != r(rev[k] / 10.0) for k in rev if k not in ("BNS", "NRD")))
    check("SF21 the VAT split rounded to the cent or carried unrounded: the same 10-euro figures", vat_split_same(target, rev))
    rates = recovered_rates(target)
    check("C4 each statement's amount over the value it was struck on is the agency's contract rate",
          all(abs(rates[a] - AW.AGENCY_RATE[a]) < 1e-4 for a in rates), json.dumps({a: round(v, 5) for a, v in rates.items()}))

    # ------------------------------------------------------------------ realism sweep
    durs = collections.defaultdict(list)
    for j in G.window_journeys:
        if j["t_out"]:
            t1, t2 = AN.tmin(j["t_in"]), AN.tmin(j["t_out"])
            durs[(j["o"], j["d"])].append(t2 - t1 if t2 >= t1 else t2 + 1440 - t1)
    sds = [statistics.pstdev(v) for v in durs.values() if len(v) >= 30]
    check("RS1 journey durations vary on every busy pair (no fixed run)", min(sds) > 0.8, "min sd %.2f min" % min(sds))
    early = [j for j in js if AN.tmin(j["t_in"]) < {5: 390, 6: 420}.get(j["date"].weekday(), 345)
             and AN.tmin(j["t_in"]) > 60]
    check("RS2 no check-in before the metro opens", not early, "%d" % len(early))
    thru = sum(1 for j in G.window_journeys if j["t_out"] and AN.crosses(net, j["o"], j["d"]))
    check("RS3 the journeys through Centraal are a minority of the extract", thru < 0.5 * len(G.window_journeys),
          "%d of %d" % (thru, len(G.window_journeys)))
    check("RS4 screen counts differ across packages and make-good figures all differ",
          len(set(sc.values())) >= 6 and len({v["make_good"] for v in mg.values()}) == len(mg))
    docs = IO.read_xlsx(os.path.join(target, PK.FILES["billing"]), "Documents")[1]
    desc = [d[8] for d in docs if d[2] == "credit note"]
    check("RS5 no credit-note reason repeats beyond the summer corrections", len(set(desc)) >= len(desc) - 1)
    people = set(json.load(open(os.path.join(TASK, "..", ".claude", "skills", "fingerprint", "cards", "task255.json")))
                 ["world"]["people"])
    authors = set()
    for f in files:
        if f.endswith(".xlsx"):
            import zipfile
            core = zipfile.ZipFile(os.path.join(target, f)).read("docProps/core.xml").decode()
            authors |= set(re.findall(r"<(?:dc:creator|cp:lastModifiedBy)>([^<]+)<", core))
        elif f.endswith(".pdf"):
            authors |= {m.decode("latin-1") for m in re.findall(rb"/Author \(([^)]*)\)", open(os.path.join(target, f), "rb").read())}
    persons = {a for a in authors if re.fullmatch(r"[A-Z][a-z]+ [A-Z][a-z]+", a) and not re.search(
        r"Media|Benchmark|Onderzoeksbureau|Spoorbeeld|RVB|Datawarehouse|Finance|Crediteuren|Informatie", a)}
    check("RS6 every person who authored a shipped file is a persona from the card", persons <= people and persons,
          ", ".join(sorted(persons)))
    tool = [f for f in files if re.search(rb"ReportLab|reportlab|openpyxl|matplotlib|python", open(os.path.join(target, f), "rb").read())]
    check("RS7 no toolchain signature in any shipped file", not tool, ", ".join(tool))
    stamp = dt.datetime(2026, 11, 13, 8, 20).timestamp()
    check("RS8 every file carries the pull's timestamp", all(abs(os.path.getmtime(os.path.join(target, f)) - stamp) < 1
                                                            for f in files))
    last_j = max(j["date"] for j in js)
    cms = AN.load_cms(target, "utc")
    last_c = max(t for v in cms.values() for t, _, _ in v)
    last_b = max(str(d[1])[:10] for d in docs)
    check("RS9 nothing after each export's own end (journeys 4 November, player log 4 November, billing 12 November)",
          last_j <= dt.date(2026, 11, 4) and last_c < dt.datetime(2026, 11, 5) and last_b <= "2026-11-12")
    reg_times = {a for t, p, a, b in cab} | {b for t, p, a, b in cab if b}
    cms_times = {t for v in AN.load_cms(target).values() for t, _, _ in v}
    check("RS10 the register and the player log never share a time stamp for a re-cabling (two observers)",
          not ({f["logged_at"] for f in A.failures} & cms_times) and not ({f["recable_at"] for f in A.failures} & reg_times))
    gates_per_hall = collections.Counter(net["gates"].values())
    check("RS11 gate counts differ across halls", len(set(gates_per_hall.values())) >= 4)

    fails = [x for x in RESULTS if not x[1]]
    print("\n%d checks, %d failed (%.0fs)" % (len(RESULTS), len(fails), (dt.datetime.now() - t0).total_seconds()))
    return not fails


# ---------------------------------------------------------------------- helpers
def fastest(net, o, d):
    heap = [(0.0, o, ln, ((ln, o),)) for ln in net["lines_of"][o]]
    heapq.heapify(heap)
    seen, best = {}, None
    while heap:
        t, c, ln, path = heapq.heappop(heap)
        if (c, ln) in seen and seen[(c, ln)] <= t:
            continue
        seen[(c, ln)] = t
        if c == d:
            best = path
            break
        s = net["seq"][ln]
        i = net["pos"][ln][c]
        for j in (i - 1, i + 1):
            if 0 <= j < len(s):
                heapq.heappush(heap, (t + net["run"][(ln, c, s[j])], s[j], ln, path))
        for ln2 in net["lines_of"][c]:
            if ln2 != ln:
                heapq.heappush(heap, (t + net["inter"][c]["walk"], c, ln2, path + ((ln2, c),)))
    legs = []
    for k, (ln, a) in enumerate(best):
        b = best[k + 1][1] if k + 1 < len(best) else d
        if a != b:
            legs.append((ln, a, b))
    return legs


def single_through(net, j):
    legs = AN.route(net, j["o"], j["d"])
    mv = AN.movements(legs)
    if len(mv) != 1 or mv[0][0] != "MM" or not AN.crosses(net, mv[0][1], mv[0][2]):
        return None
    return mv[0]


def excess(net, j, mv):
    kind, u, v = mv
    lu, lv = AN.LINE[net["branch"][u]], AN.LINE[net["branch"][v]]
    hin, hout = net["gates"][j["dev_in"]], net["gates"][j["dev_out"]]
    t1, t2 = AN.tmin(j["t_in"]), AN.tmin(j["t_out"])
    dur = t2 - t1 if t2 >= t1 else t2 + 1440 - t1
    base = net["halls"][hin]["walk"][lu] + AN.ride(net, lu, u, "CEN") + AN.ride(net, lv, "CEN", v) + \
        net["halls"][hout]["walk"][lv]
    return dur - base


def duration_only_flips(target, G, thr=6.5):
    """Off-peak single trips the line map runs straight through Centraal (north-south, west-east) in the hours trains
    run every six minutes or less often: the share a duration-only reading at the passage walk calls a change, and, in
    every hour band where it calls any, the share of the same band's trips that came out of Centraal faster than a
    change can take (under 6.2 minutes over the run), so that the band's trains ran through."""
    net = G.net
    bands = collections.defaultdict(list)
    for j in G.window_journeys:
        if not j["t_out"]:
            continue
        mv = single_through(net, j)
        if mv is None or {net["branch"][mv[1]], net["branch"][mv[2]]} not in ({"N", "S"}, {"W", "E"}):
            continue
        t1 = AN.tmin(j["t_in"])
        if AN.headway_at(net, j["date"], t1) < 6.0:
            continue
        bands[(min(j["date"].weekday(), 5) if j["date"].weekday() < 6 else 6, int(t1 // 60))].append(excess(net, j, mv))
    allx = [x for v in bands.values() for x in v]
    flagged = sum(1 for x in allx if x > thr) / max(1, len(allx))
    mixed = [sum(1 for x in v if x < 6.2) / len(v) for v in bands.values() if any(x > thr for x in v) and len(v) >= 5]
    return flagged, (min(mixed) if mixed else 0.0), len(allx)


def shoulder_hours(target, G):
    """In the three-minute bands outside the peak service windows (06:30 to 07:00, 09:30 to 10:00, 15:30 to 16:00 and
    18:30 to 19:00 on weekdays), the share of north-east and of north-south single trips whose duration shows a change."""
    net = G.net
    ne, ns = [], []
    for j in G.window_journeys:
        if not j["t_out"] or j["date"].weekday() >= 5:
            continue
        t1 = AN.tmin(j["t_in"])
        if not (390 <= t1 < 405 or 572 <= t1 < 590 or 930 <= t1 < 945 or 1112 <= t1 < 1130):
            continue
        mv = single_through(net, j)
        if mv is None:
            continue
        pair = {net["branch"][mv[1]], net["branch"][mv[2]]}
        x = excess(net, j, mv)
        if pair == {"N", "E"}:
            ne.append(x > 5.4)
        elif pair == {"N", "S"}:
            ns.append(x > 5.4)
    return sum(ne) / max(1, len(ne)), sum(ns) / max(1, len(ns))


def family(target):
    out = {}
    orig = AN.read_change
    for name, shift, mode in (("estimated minute -3", -3.0, None), ("estimated minute +3", 3.0, None),
                              ("pattern for every journey", 0.0, "pattern")):
        def rc(net, j, hin, hout, mv, i, linemap, tally, _s=shift, _m=mode):
            kind, u, v = mv[i]
            bu, bv = net["branch"][u], net["branch"][v]
            if _m != "pattern":
                if len(mv) == 1:
                    x = excess(net, j, mv[0]) if j["t_out"] else 0
                    if x < 4.6:
                        return False
                    if x > 5.4 and AN.headway_at(net, j["date"], AN.tmin(j["t_in"])) <= 3.0:
                        return True
            est = AN.tmin(j["t_in"]) + net["halls"][hin]["walk"][AN.first_line(mv, net, u)] + 1.5 + _s
            for k in range(i):
                kk, a, b = mv[k]
                est += AN.ride(net, "M3" if kk == "M3" else AN.LINE.get(net["branch"][a], "M1"), a, b) + 3.0
                est += net["inter"][b]["walk"] if b in net["inter"] else 0.0
            est += AN.ride(net, AN.LINE[bu], u, "CEN")
            pk = j["date"].weekday() < 5 and any(a <= est % 1440 < b for a, b in AN.PEAK_WINDOWS)
            return (AN.SERVICE[bu] != AN.SERVICE[bv]) if pk else linemap
        AN.read_change = rc
        M = AN.main_call(target)
        out[name] = (M.tier, {k: r(v) for k, v in M.reach.items()})
    AN.read_change = orig
    return out


def takedown_open_same(target, mg):
    """The take-down dated at the opening of its day instead of its player's last report: the same make-good."""
    orig = AN.load_cms

    def no_zero(t, clock="local"):
        ev = orig(t, clock)
        return {p: [e for e in v if not (e[1] == "DISPLAYS" and e[2] == 0)] for p, v in ev.items()}
    AN.load_cms = no_zero
    alt = AN.make_good(target)
    AN.load_cms = orig
    return all(alt[k]["make_good"] == mg[k]["make_good"] for k in mg)


def recab_consistent(target):
    scr, cab = AN.load_register(target)
    times = AN.recabling_times(target, cab)
    return bool(times) and all(v is not None and v < k[2] for k, v in times.items())


def vat_split_same(target, rev):
    alt = AN.net_revenue(target, vat="split_exact")
    return all(r(alt[k] / 10.0) == r(rev[k] / 10.0) and abs(alt[k] - rev[k]) < 1.0 for k in rev)


def recovered_rates(target):
    h, rows = IO.read_csv(os.path.join(target, PK.FILES["legacy"]), delimiter=";")
    inv = {no: {"ref": ref, "net": round(AN.nl_num(g) / 1.21, 2)} for no, date, ref, debtor, g in rows}
    h, rows = IO.read_xlsx(os.path.join(target, PK.FILES["billing"]), "Documents")
    docs = [dict(zip(h, x)) for x in rows if x[0]]
    for d in docs:
        if d["document_type"] == "invoice":
            inv[d["document_no"]] = {"ref": d["booking_ref"], "net": float(d["net_eur"])}
    out = {}
    for s in AN.load_statements(target):
        base = sum(v["net"] for v in inv.values() if v["ref"] in s["refs"])
        for d in docs:
            if d["document_type"] == "credit note" and inv.get(d["reference"], {}).get("ref") in s["refs"] and \
                    dt.date.fromisoformat(str(d["document_date"])[:10]) <= s["date"]:
                base += float(d["net_eur"])
        out[s["agency"]] = s["amount"] / base
    return out


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    sys.exit(0 if main(tgt) else 1)
