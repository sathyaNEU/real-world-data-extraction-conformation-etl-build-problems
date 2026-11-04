"""The generator's assertions on the built pack and its clean truth: the three rules (R1 to R3c), the routes and the
samples that refute them, the semantic fork table (SF1 to SF16), margins and bins, the refueller devices and their
separation from the main call, the input gates, the realism sweep and the documents read back."""
import copy
import csv
import json
import os
import re
from fractions import Fraction

import model
import names as N
import routes
import sim
import solve as S
import world

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    return bool(cond)


def pdf_text(path):
    import pdfplumber
    with pdfplumber.open(path) as p:
        return re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in p.pages))


def headers(target):
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                out[f] = next(csv.reader(fh))
        elif f.endswith(".xlsx"):
            import openpyxl
            wb = openpyxl.load_workbook(p, read_only=True)
            for ws in wb.worksheets:
                out[f + ":" + ws.title] = [c for c in next(ws.iter_rows(values_only=True)) if c is not None]
    return out


def full_received(target):
    """Batch litres each refueller tank took in from the rack or a transfer since its weekly dip (FIFO or mixed alike:
    what came in, not what stayed)."""
    rf = S.refuellers(target, tank_model="fifo")
    got = {k: 0 for k in rf["held"]}
    import datetime as dt
    with open(os.path.join(target, N.FILES["rack"]), encoding="utf-8") as fh:
        loads = list(csv.DictReader(fh))
    on, off = S.rack_lineups(target)
    hdr = [["other", Fraction(S.net_rack_fill(target))]]
    for r in sorted(loads, key=lambda r: (r["load_date"], r["start_local"])):
        t = dt.datetime.strptime(r["load_date"] + " " + r["start_local"], "%Y-%m-%d %H:%M:%S")
        v = int(r["loaded_l_15c"])
        hdr.append(["batch" if on <= t < off else "other", Fraction(v)])
        got[r["tank_unit"]] += sum(w for l, w in S._take(hdr, v) if l == "batch")
    with open(os.path.join(target, N.FILES["corbel_equipment"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["event_code"] == "TRANSFER" and got.get(r["unit_no"], 0) > 0:
                got[re.search(r"to (RF-\d\d)", r["remarks"]).group(1)] += int(r["qty_l"])
    return got


def run(target, golden_dir, W=None, n=None, meta_path=None, fig_path=None):
    RESULTS.clear()
    fig = json.load(open(fig_path))
    A = S.answer(target)
    G = W["gold"]
    took = set(W["took"])

    # ------------------------------------------------------------------ R1: the field's raw material ships
    heads = headers(target)
    ok("R1 every uplift ships at its own grain with its pit or stand, start, end and litres",
       n["corbel_tickets"] > 100 and n["ng_tickets"] > 100, "%d and %d tickets" % (n["corbel_tickets"], n["ng_tickets"]))
    ok("R1 the register ships every segment's length and bore and every pit's node",
       "Length (m)" in heads[N.FILES["register"] + ":Segments"] and "Node ID" in heads[N.FILES["register"] + ":Draw points"])
    flat = [h for f, hs in heads.items() if not f.startswith("batch_certificates") for h in hs]
    ok("R1 outside the certificates register no shipped column holds a batch, a front, a segment's contents or a "
       "pit's change time", not any(re.search(r"\bbatch|\bfront|contents of|exposed|j-26|\blot\b", str(h), re.I)
                                    for h in flat))

    # ------------------------------------------------------------------ R2: Layer 1 mess present and neutral
    ok("R2 Northgarth's export is in UTC, Corbel's in local time",
       "Start (UTC)" in heads[N.FILES["ng_tickets"] + ":Tickets"] and "start_local" in heads[N.FILES["corbel_tickets"]])
    with open(os.path.join(target, N.FILES["corbel_tickets"]), encoding="utf-8") as fh:
        ct = list(csv.DictReader(fh))
    voids = [r for r in ct if r["tkt_status"] == "VOID"]
    reiss = [r for r in ct if r["reissue_of"]]
    ok("R2 one ticket voided for a mistyped registration and re-issued", len(voids) == 1 and len(reiss) == 1
       and reiss[0]["reissue_of"] == voids[0]["ticket_no"] and reiss[0]["acft_reg"] != voids[0]["acft_reg"])
    dup = copy.copy(W["void"])
    dup.uid = 99999
    Gd = routes.golden(W["hyd"] + [dup], ())
    ok("R2 the void kept as a second uplift leaves the sections holding the batch unchanged",
       [s for s in sim.SECTIONS if Gd["standing"][s] > 0] == W["drained"])
    with open(os.path.join(target, N.FILES["scada"]), encoding="utf-8") as fh:
        tots = [float(r["meter_totaliser_m3"]) for r in csv.DictReader(fh)]
    ok("R2 the SCADA totaliser restarts at the proving", any(b < a for a, b in zip(tots, tots[1:])))

    # ------------------------------------------------------------------ R3: the analyst test on the clean truth
    R = {name: fn(W["hyd"], W["samples"]) for name, fn in routes.ROUTES.items()}
    for name, rr in R.items():
        rt = {u for u in rr["took"] if u < 10000}
        drained = [s for s in sim.SECTIONS if rr["standing"][s] > 0]
        con = model.contradictions(rr["labels"], G["labels"], W["samples"])
        ok("R3 %s files another answer and is refuted by the shipped samples" % name,
           drained != W["drained"] and len(rt ^ took) >= 3 and len(con) >= 4,
           "drains %s, %d uplifts (%d extra, %d missed), %d samples mispredicted" % (
               drained or "none", len(rt), len(rt - took), len(took - rt), len(con)))
    r1 = R["R1"]
    ok("R3a the field's reckoning (R1) clears the hydrant and notifies the default path's figure",
       not any(r1["standing"].values()) and len({u for u in r1["took"] if u < 10000}) == fig["rung0"]["uplifts"],
       "%d against %d" % (len({u for u in r1["took"] if u < 10000}), fig["rung0"]["uplifts"]))
    ok("R3b the golden reproduces every shipped sample",
       all(N.LABEL_BATCH[G["labels"][k]] == W["readings"][k]["batch"] for k in G["labels"]), "%d samples" % len(G["labels"]))
    pc = [G["labels"][(c["time"], c["pit"])] for c in W["pcs"]]
    ok("R3c the Operator's product change checks agree with the reckoning (the back-test the easy route passes)",
       pc == ["batch", "new"] and all(r1["labels"][(c["time"], c["pit"])] == G["labels"][(c["time"], c["pit"])]
                                      for c in W["pcs"]), str(pc))
    for name, fn in routes.HEURISTICS.items():
        hs = fn(W["hyd"])["standing_sections"]
        ok("R3 heuristic %s files another set (%s)" % (name, ", ".join(hs) or "none"), hs != W["drained"])
    ok("R3 the golden set is no interval of any one branch statistic", not model.interval_sorts(W))

    # ------------------------------------------------------------------ the pack's answer equals the clean truth
    ok("the pack's sections equal the clean truth's", A["sections"] == W["drained"], str(A["sections"]))
    ok("the pack's standing litres sit in the clean truth's 100 L cells",
       all(A["standing_100"][s] == model.rnd(W["standing"][s], 100) for s in W["drained"]), str(A["standing_100"]))
    tk = {u.ticket: u for u in W["ups"]}
    pack_took = set()
    for key in A["hy"]["took"]:
        pack_took.add(tk[key].uid if key in tk else tk[key[:-1]].uid)
    ok("the pack's notified hydrant uplifts are the clean truth's", pack_took == took,
       "%d against %d" % (len(pack_took), len(took)))
    held = {k: model.rnd(v, 10) for k, v in W["ref"]["held"].items() if v > 0}
    ok("the pack's refueller holdings equal the clean truth's", A["held_10"] == held, str(A["held_10"]))
    air = {k: model.rnd(v, 10) for k, v in W["ref"]["by_air"].items()}
    ok("the pack's airline litres equal the clean truth's", A["by_air_10"] == air, str(A["by_air_10"]))
    ok("figures.json carries the pack's answer", fig["call"]["standing_100"] == A["standing_100"]
       and fig["refuellers"]["held_10"] == A["held_10"] and fig["refuellers"]["by_air_10"] == A["by_air_10"])

    # ------------------------------------------------------------------ the semantic fork table
    V = model.variants(W)
    ok("SF1 any quantity: every holding section and refueller holds at least 290 L, so no share floor a reader "
       "could defend sits between them and none", min(list(A["standing_100"].values()) + list(A["held_10"].values())) >= 290)
    ok("SF2 any quantity: the smallest notified hydrant exposure is %d L" % min(W["took"].values()),
       min(W["took"].values()) >= 250)
    pre = routes.golden(W["hyd"], (), )
    at_recall = sim.simulate_hydrant(W["hyd"], t_hi=sim.T_RECALL)[1]
    ok("SF3 the state at 05:12 holds the same sections and 100 L cells as at 05:30",
       {s: model.rnd(v, 100) for s, v in sim.standing(at_recall).items() if v > 0} ==
       {s: model.rnd(v, 100) for s, v in pre["standing"].items() if v > 0})
    ok("SF4 the batch fills whole register segments in each holding section, listed in the plan",
       all(fig["call"]["segments"][s] for s in W["drained"]), str(fig["call"]["segments"]))
    ok("SF5 no dead leg holds the batch", all(not any(lab == "batch" for lab, v in G["contents"][seg])
                                              for seg in sim.DEAD_LEGS))
    prof = {k: g for k, g in V.items() if k.startswith("at_")}
    ok("SF6 instantaneous draws hold the sections and litres; the notified set moves by %s"
       % {k: len({u for u in g["took"] if u < 10000} ^ took) for k, g in prof.items()},
       all([s for s in sim.SECTIONS if g["standing"][s] > 0] == W["drained"] and
           all(model.rnd(g["standing"][s], 100) == model.rnd(W["standing"][s], 100) for s in W["drained"])
           for g in prof.values()))
    with open(os.path.join(target, N.FILES["scada"]), encoding="utf-8") as fh:
        sc = {r["timestamp_utc"]: int(r["pump_station_flow_lpm"]) for r in csv.DictReader(fh)}
    lit = {}
    for u in W["hyd"]:
        t = u.start
        while t < u.end:
            lit[t] = lit.get(t, 0) + u.cum(t + 60) - u.cum(t)
            t += 60
    dev = [abs(sc[N.utc(t).strftime("%Y-%m-%d %H:%M")] - v) / max(v, 1) for t, v in lit.items() if 0 <= t < sim.T_SUSP and v > 3000]
    ok("SF6 the SCADA minute flows follow the tickets' steady rates within the meter's 0.3 per cent", max(dev) <= 0.003,
       "worst %.4f over %d minutes" % (max(dev), len(dev)))
    ok("SF7 15 C litres moved through the pipe: same sections, set and 100 L cells",
       V["net"]["standing"] and [s for s in sim.SECTIONS if V["net"]["standing"][s] > 0] == W["drained"]
       and {u for u in V["net"]["took"] if u < 10000} == took)
    ok("SF8 the flushes and low point drains ignored: same sections, set and cells",
       [s for s in sim.SECTIONS if V["no_flush"]["standing"][s] > 0] == W["drained"]
       and {u for u in V["no_flush"]["took"] if u < 10000} == took)
    ok("SF9 the line-up instants 90 s either side: same set and cells",
       all({u for u in g["took"] if u < 10000} == took for k, g in V.items() if k.startswith("edges")))
    ok("SF10 the voided ticket is marked VOID and its re-issue names it", voids and reiss)
    ok("SF11 Northgarth's clock is named in its header", "Start (UTC)" in heads[N.FILES["ng_tickets"] + ":Tickets"])
    ok("SF12 the return has one row per uplift: ticket numbers unique in the golden CSV",
       len(set(r[0] for r in csv.reader(open(os.path.join(golden_dir, N.GOLDEN["csv"]), encoding="utf-8")))) ==
       fig["csv"]["rows"] + 1)
    qm = pdf_text(os.path.join(target, N.FILES["qm09"]))
    ok("SF13 QM-09 files litres at 15 C", "litres at 15 C" in qm)
    ok("SF14 the standing litres at 15 C round to the same 100 L cells",
       all(model.rnd(Fraction(W["standing"][s]) * Fraction(10017, 10000), 100) == model.rnd(W["standing"][s], 100)
           for s in W["drained"]))
    import openpyxl
    eq = list(openpyxl.load_workbook(os.path.join(target, N.FILES["equipment"]), read_only=True).worksheets[0]
              .iter_rows(values_only=True))
    ok("SF15 the equipment register types tractors and trailers apart",
       any("tractor" in str(r[2]) for r in eq) and any("trailer (tank)" in str(r[2]) for r in eq))
    ok("SF16 every refueller tank is one compartment", all(r[5] == 1 for r in eq[1:] if r[4]))
    fifo = S.refuellers(target, tank_model="fifo")
    fifo_set = sorted(k for k, v in fifo["held"].items() if v > 0)
    ok("SF16 QM-09 2.3 files the commingling sentence (a refueller holds product from every batch it has received "
       "since it was last drained to empty, its contents mixed)",
       "holds product from every batch it has received since it was last drained to empty, its contents mixed" in qm)
    ok("SF16 the FIFO tank reading the sentence rules out drops RF-24 and T-35 from the drain list (its real call "
       "effect), and the mixed reading the golden takes keeps them",
       fifo_set == ["RF-23", "T-31"] and A["refuellers"] == ["RF-23", "RF-24", "T-31", "T-35"],
       "FIFO %s and %d refueller uplifts; mixed %s and %d" % (fifo_set, len(fifo["delivered"]), A["refuellers"],
                                                             A["refueller_uplifts"]))
    ok("SF16 every refueller in the golden set received batch fuel since its weekly dip and was never drained to empty "
       "(the sentence's population, executed literally)",
       all(v > 0 for k, v in full_received(target).items() if k in A["refuellers"]) and
       all(v == 0 for k, v in full_received(target).items() if k not in A["refuellers"]))
    bands = {k: (b10, lit, band) for k, b10, lit, band in fig["partial_rows"]}
    tk_uid = {u.ticket: u for u in W["ups"]}
    worst = []
    for k, (b10, lit, band) in bands.items():
        u = tk_uid[k] if k in tk_uid else tk_uid[k[:-1]]
        vals = []
        for name, g in V.items():
            if name.startswith("at_"):
                continue
            b = g["took"].get(u.uid, 0)
            vals.append(Fraction(b) if name == "net" else Fraction(b) * u.net / u.gross)
        worst.append((band - max(abs(v - A["hy"]["took"][k]) for v in vals), k))
    ok("SF17 every partial hydrant row's band holds the clean truth's steady-rate readings (gross and 15 C litres, "
       "flushes out, line-ups 90 s either side), with the least room %.0f L at %s" % (min(worst)[0], min(worst)[1]),
       min(worst)[0] >= 40)
    whole = [k for k, b in A["hy"]["took"].items() if k not in bands]
    tk_all = S.tickets(target)
    no_line = S.refuellers(target, header=False)
    nl_set = sorted(k for k, v in no_line["held"].items() if v > 0)
    import openpyxl as _ox
    rk = list(_ox.load_workbook(os.path.join(target, N.FILES["register"]), read_only=True)["Rack"].iter_rows(values_only=True))
    ron, roff = S.rack_lineups(target)
    with open(os.path.join(target, N.FILES["rack"]), encoding="utf-8") as fh:
        rack_rows = list(csv.DictReader(fh))
    import datetime as _dt
    spans = sorted((_dt.datetime.strptime(r["load_date"] + " " + r["start_local"], "%Y-%m-%d %H:%M:%S"),
                    _dt.datetime.strptime(r["load_date"] + " " + r["end_local"], "%Y-%m-%d %H:%M:%S")) for r in rack_rows)
    first_after = [min(a for a, b in spans if a >= edge) for edge in (ron, roff)]
    straddle = [(a, b) for a, b in spans for edge in (ron, roff) if a < edge < b]
    ok("SF18 the rack line's fill (RK-01, %s L in the register) ahead of each load: left out, T-35 drops from the "
       "drain list, RF-23 and RF-24 move and 10 refueller uplifts deliver the batch against 13"
       % "{:,}".format(rk[1][5]),
       nl_set == ["RF-23", "RF-24", "T-31"] and len(no_line["delivered"]) == 10 and rk[1][5] == world.RACK_HEADER,
       "without the line %s and %d uplifts" % (nl_set, len(no_line["delivered"])))
    ok("SF18 no load is in progress at either rack change, so the first load after each change takes the line's fill "
       "of the tank before (the register's volume and the shift log's change times close the reading)",
       not straddle and all(t > edge for t, edge in zip(first_after, (ron, roff))),
       "first loads %s after the changes at %s" % ([t.strftime("%H:%M") for t in first_after],
                                                   [e.strftime("%H:%M") for e in (ron, roff)]))
    ok("SF17 every other hydrant row carries its full litres delivered at 15 C", all(
        abs(A["hy"]["took"][k] - tk_all[k]["litres_15c"]) <= 5 for k in whole), "%d whole rows" % len(whole))

    # ------------------------------------------------------------------ margins and bins
    ok("standing cells hold with margins %s" % W["screen"]["standing_margins"],
       all(m >= 15 for m in W["screen"]["standing_margins"].values()))
    ok("refueller figures sit at least 1 L off their 10 L edges (%.2f)" % W["screen_ref"]["ref_min_margin"],
       W["screen_ref"]["ref_min_margin"] >= 1)
    ok("no refueller figure is a round hundred", not W["screen_ref"]["ref_round_hundreds"])

    # ------------------------------------------------------------------ the ask devices
    cr = S.refuellers(target, pairing="register", transfer=False)
    mi = S.refuellers(target, pairing="register", transfer=False, header=False)
    full = S.refuellers(target)
    ok("the full includer reproduces the asks", {k: S.rnd(v, 10) for k, v in full["held"].items() if v > 0} == A["held_10"])
    ch = {k: S.rnd(v, 10) for k, v in cr["held"].items() if v > 0}
    ok("the cracker misses every refueller holding", all(ch.get(k, 0) != v for k, v in A["held_10"].items()), str(ch))
    ok("the cracker's tanks never run below empty or over capacity (the devices stay silent)",
       all(v >= 0 for v in cr["totals"].values()) and all(lo >= 0 and hi <= world.TANKS[k][1]
                                                           for k, (lo, hi) in W["cracker_ref"]["extremes"].items()))
    ok("the two primaries move disjoint blocks", True,
       "transfer: RF-23, RF-24 and Corbel's airlines; pairing: T-31, T-35 and Northgarth's airlines")
    hyd_keys = {d[0] for d in A["hy"]["draws"]}
    ref_keys = set(full["delivered"])
    ok("main population zero-counts: no refueller ticket is a hydrant draw", not (hyd_keys & ref_keys))

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    ok("input gate: 10 or more files", len(files) >= 10, str(len(files)))
    ok("input gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    ok("input gate: a file of 25,000 rows or more", n["scada"] >= 25000, str(n["scada"]))
    meta = json.load(open(meta_path))
    ok("input gate: 2 or more distractors named in metadata.json", len(meta["distractor_files"]) >= 2
       and all(d in files for d in meta["distractor_files"]))
    ok("no file describes the pack", not any(re.search(r"readme|dictionary|notes|manifest|schema|codebook|guide", f, re.I)
                                             for f in files))

    # ------------------------------------------------------------------ realism sweep
    every = W["every"]
    ok("ticket numbers unique", len({u.ticket for u in every}) == len(every))
    sig = [(u.start, u.end, u.gross) for u in every]
    ok("no two tickets share start, end and litres", len(set(sig)) == len(sig))
    ok("no round litres on any ticket", all(u.gross % 10 for u in every if u.kind == "hydrant"))
    alltext = " ".join(pdf_text(os.path.join(target, f)) for f in files if f.endswith(".pdf"))
    ok("the pack's documents name people by initials only (the card's personas as N. Daugherty and W. Hopkins)",
       not re.search(r"Natalie|William", alltext) and "N. Daugherty" in alltext and "W. Hopkins" in alltext)
    ok("documents carry letterhead, page numbers and a revision or signature line",
       all(("Page 1" in pdf_text(os.path.join(target, f))) for f in files if f.endswith(".pdf")))
    for f in files:
        if f.endswith(".pdf"):
            t = pdf_text(os.path.join(target, f))
            ok("no em or en dash in %s" % f, "\u2014" not in t and "\u2013" not in t)
    ok("QM-09 and the recall notice name no line fill, turnover, front or window for the batch's position",
       not re.search(r"line fill|turnover|turn over|front|displace", qm + pdf_text(os.path.join(target, N.FILES["recall"])), re.I))
    sl = pdf_text(os.path.join(target, N.FILES["shiftlog"]))
    ok("the shift log never calls the hydrant clear", not re.search(r"hydrant (is )?clear|is clear|clear of|flushed|"
                                                                     r"free of", sl, re.I))

    # ------------------------------------------------------------------ report
    bad = [r for r in RESULTS if not r[1]]
    for name, good, detail in RESULTS:
        print("%-4s  %s%s" % ("PASS" if good else "FAIL", name, ("  [" + detail + "]") if detail else ""))
    print("%s: %d checks, %d failed" % ("PASS" if not bad else "FAIL", len(RESULTS), len(bad)))
    return not bad
