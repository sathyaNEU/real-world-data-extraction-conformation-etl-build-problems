"""The generator's assertions on the cut pack: the input gates, the call and its family, the rungs, the three rules
(R1 the field's raw material ships, R2 every mess item neutral, R3 the analyst test on the clean truth), the semantic
forks (SF rows), the separation of the asks from the call, the ask device and its stops, the rounding edges, the
realism sweep and the containers. Every label is printed with PASS or FAIL; the run fails on any FAIL."""
import collections
import csv
import datetime as dt
import json
import os
import re
import zipfile

import analysis as AN
import asks as AS
import common as K
import side2025 as S25

ROWS = []


def row(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def edge(v, unit):
    """distance from the unrounded value to the nearest rounding edge at the printed unit"""
    return unit / 2 - abs(v - round(v / unit) * unit)


def rows_of(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def order(r3):
    return sorted(K.SCHED, key=lambda s: -r3[s])


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    golden_dir = os.path.join(task, "golden")
    W = b["world"]
    P = res["pack"]
    gold = fig["call"]["schedule"]

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    row("GATE files", len(files) >= 10, "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    row("GATE formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    big = max(b["counts"].values())
    row("GATE 25,000-row file", big >= 25000, "largest %d rows" % big)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    row("GATE distractors", len(meta["distractor_files"]) >= 2 and
        all(os.path.basename(x) in files for x in meta["distractor_files"]), ", ".join(meta["distractor_files"]))
    row("GATE provenance", set(meta["provenance"]) == set(files), "%d entries" % len(meta["provenance"]))
    row("GATE deliverables", sorted(os.listdir(golden_dir)) == sorted([K.BOOK, K.DECK]), ", ".join([K.BOOK, K.DECK]))

    # ------------------------------------------------------------------ the call
    m = res["main"]
    r3 = m["reach3"]
    row("CALL golden schedule", gold == "A" and order(r3) == ["A", "B", "C"],
        "A %.2f, B %.2f, C %.2f" % tuple(100 * r3[s] for s in K.SCHED))
    ids = W.young_ids()
    truth = {s: W.reach(W.exposures(s, "golden", ids), 3, ids) for s in K.SCHED}
    row("CALL the world's truth names it", order(truth)[0] == gold and all(abs(truth[s] - r3[s]) < 1e-9
                                                                          for s in K.SCHED),
        "A %.4f, B %.4f, C %.4f" % tuple(100 * truth[s] for s in K.SCHED))
    row("CALL golden margin over the runner-up at least 1.2x", r3["A"] / r3["B"] >= 1.2,
        "%.3f" % (r3["A"] / r3["B"]))
    spend = {s: sum(ln["price"] for ln in P.sched[s]) for s in K.SCHED}
    row("CALL every schedule within the budget and within one spot of it",
        all(K.BUDGET - 4000 < spend[s] <= K.BUDGET for s in K.SCHED), str(spend))

    # ------------------------------------------------------------------ the family: readings a careful reader may take
    fam = {}
    fam["places at 30 seconds from their start"] = AN.main_call(target, pack=AN.Pack(target, length=30))["reach3"]
    for k, v in fam.items():
        row("FAMILY %s files A" % k, order(v)[0] == gold,
            "A %.2f, B %.2f, C %.2f" % tuple(100 * v[s] for s in K.SCHED))

    # ------------------------------------------------------------------ the rungs
    rg = AN.rungs(target, P)
    for k in ("R0_ratings_grps", "breaks", "uniform", "nonpremium", "asrun"):
        o = order(rg[k])
        row("RUNG %s files B" % k, o[0] == "B" and rg[k]["B"] / rg[k]["A"] > 1.15,
            "B over A %.3f; %s" % (rg[k]["B"] / rg[k]["A"], ", ".join("%s %.2f" % (s, rg[k][s] *
                                                                                  (1 if k.startswith("R0") else 100))
                                                                     for s in K.SCHED)))
    row("RUNG default path (in-window rotation places) margin", rg["asrun"]["B"] / rg["asrun"]["A"] > 1.15,
        "%.3f" % (rg["asrun"]["B"] / rg["asrun"]["A"]))

    # ------------------------------------------------------------------ R1 the field's raw material ships
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().strip().lower()
             for f in files if f.endswith(".csv")}
    bad = [f for f, h in heads.items() if re.search(r"cobertura|reach|exposi|probab|frequen|\bgrp\b|mudad|movid|fora_da",
                                                     h)]
    row("R1 no shipped column holds a reach, an exposure or a moved booking", not bad, ", ".join(bad) or "none")
    nview = b["counts"]["viewing"]
    row("R1 the decisive step reads the person-level viewing, the as-run log and the bookings",
        nview > 25000 and len(P.booking) > 10000 and len(P.asrun) > 10000,
        "%d statements, %d as-run spots, %d bookings" % (nview, len(P.asrun), len(P.booking)))

    # ------------------------------------------------------------------ R2 every mess item neutral
    for label, kw in (("the panel's UTC read as local time across the clock change", dict(dst=False)),
                      ("Pulsar+ left apart from Pulsar", dict(rename=False)),
                      ("time-shifted viewing read as live at its viewing time", dict(playback=True)),
                      ("guest statements read in", dict(guests=True)),
                      ("a break found by its civil date", dict(civil=True))):
        v = AN.main_call(target, pack=AN.Pack(target, **kw))["reach3"]
        row("R2 %s" % label, order(v)[0] == gold, "A %.2f, B %.2f, C %.2f" % tuple(100 * v[s] for s in K.SCHED))
    promos_at_ends = sum(1 for a in P.asrun if a["kind"] == "AUTOPROMOÇÃO" and a["pos"] in (1, a["n"]))
    row("R2 self-promotions never take a break's first or last place", promos_at_ends == 0, str(promos_at_ends))

    # ------------------------------------------------------------------ R3 the analyst test on the clean truth
    easy = {s: W.reach(W.exposures(s, "asrun", ids), 3, ids) for s in K.SCHED}
    row("R3a ANALYST the easy route on the clean truth files B", order(easy)[0] == "B",
        "A %.2f, B %.2f, C %.2f" % tuple(100 * easy[s] for s in K.SCHED))
    row("R3b DECISIVE the bookings' places alone file A", order(truth)[0] == "A",
        "A %.2f, B %.2f" % (100 * truth["A"], 100 * truth["B"]))
    moved = sum(1 for k, lst in W.booked.items() if k[2] == "prime" for s in lst if s.get("moved"))
    row("R3 the moved bookings are the channels' traffic, not a plant: every one sits in an open daytime place",
        all(s["kind"] == "ROS" for k, lst in W.booked.items() for s in lst) and moved > 0, "%d moved" % moved)

    # ------------------------------------------------------------------ SF rows: the semantic forks
    sched_rows = [x for s in K.SCHED for x in P.sched[s]]
    row("SF1 every spot line lands in its own reference week",
        all(0 <= (dt.date.fromisoformat(x["ref"]) - K.REF_START).days - 7 * (x["week"] - 1) < 7 for x in sched_rows),
        "%d lines" % len(sched_rows))
    missing = [(x["ch"], x["ref"], x["prog"], x["brk"]) for x in sched_rows if x["kind"] != "ROS" and
               (x["ch"], x["ref"], x["prog"], x["brk"]) not in P.by_break]
    row("SF2 every fixed-place line finds its reference break", not missing, str(missing[:3]))
    ros_missing = [x for x in sched_rows if x["kind"] == "ROS" and not P.sold.get((x["ch"], x["ref"], x["window"]))]
    row("SF3 every rotation line finds that day's bookings", not ros_missing, "%d" % len(ros_missing))
    per_day = collections.Counter((x["ch"], x["ref"]) for x in P.sched["B"])
    row("SF4 one rotation spot per channel and night, so spots read as independent cannot share a place",
        max(per_day.values()) == 1, str(max(per_day.values())))
    overl = 0
    for c, (arr, mem) in P.view.items():
        last = {}
        for (a0, a1), mm in zip(arr.tolist(), mem):
            if mm in last and a0 < last[mm]:
                overl += 1
            last[mm] = max(last.get(mm, 0), a1)
    row("SF5 no member's live statements on one channel overlap, so summed seconds are seconds seen", overl == 0,
        str(overl))
    pb = res["prime"]
    row("SF6 the bookings say where the window's rotation aired: a third outside prime time",
        0.25 < pb["share_elsewhere"] < 0.4, "%d of %d" % (pb["elsewhere"], pb["bookings"]))

    # ------------------------------------------------------------------ separation of the asks from the call
    for k in ("portal", "portal_notes", "report2025"):
        row("SEP the call never opens %s" % K.FILES[k], K.FILES[k] not in open(AN.__file__, encoding="utf-8").read(),
            "")
    brief_txt = _pdf_text(os.path.join(target, K.FILES["brief"]))
    row("SEP the brief carries no ask organ", not re.search(r"marca[çc][õo]es|resposta|Portal do Dador", brief_txt),
        "")

    # ------------------------------------------------------------------ the ask device and its stops
    gold_r = res["asks"]["response"]
    for route in ("donor", "donor_open", "document_open"):
        rr = AS.response(target, route)
        moved_all = all(abs(a - g) > 0.05 for a, g in zip(rr["above"], gold_r["above"])) and \
            abs(rr["avg"] - gold_r["avg"]) > 0.05 and abs(rr["per_thousand"] - gold_r["per_thousand"]) > 0.005
        row("ASK R stop %s misses every figure" % route, moved_all,
            "average %.2f, above %s, response %.4f" % (rr["avg"], [round(x, 2) for x in rr["above"]],
                                                        rr["per_thousand"]))
        xb = AS.expected_bookings(rr["per_thousand"], m["reach3"], res["asks"]["universe"])
        row("ASK X stop %s misses every schedule" % route,
            all(round(xb[s] / 10) != round(res["asks"]["bookings"][s] / 10) for s in K.SCHED),
            str({s: round(xb[s], 1) for s in K.SCHED}))
    portal = rows_of(os.path.join(target, K.FILES["portal"]))
    doc_of = collections.defaultdict(set)
    for r in portal:
        doc_of[r["documento_hash"]].add(r["id_dador"])
    two = sum(1 for v in doc_of.values() if len(v) > 1)
    row("ASK R people under two donor numbers, linked by their identity document", two > 100, "%d" % two)
    multi_doc = collections.defaultdict(set)
    for r in portal:
        multi_doc[r["id_dador"]].add(r["documento_hash"])
    row("ASK R a donor number never carries two documents", max(len(v) for v in multi_doc.values()) == 1, "")
    attrs = collections.defaultdict(set)
    for r in portal:
        attrs[r["documento_hash"]].add((r["data_nascimento"], r["sexo"], r["distrito"]))
    row("ASK R a document always carries one birth date, sex and district", max(len(v) for v in attrs.values()) == 1,
        "")
    row("ASK R the response is fair: the golden handling reproduces the generator's truth",
        abs(gold_r["per_thousand"] - S25.response(S25.Bookings(K.SEED))["extra"] / AS.REPORT_REACHED3) < 1e-9,
        "%.4f" % gold_r["per_thousand"])
    xw = AS.expected_bookings(K.r(gold_r["per_thousand"], 2), {s: K.r(100 * m["reach3"][s], 1) / 100
                                                               for s in K.SCHED}, res["asks"]["universe"])
    row("ASK X the same tens from rounded inputs", all(round(xw[s] / 10) == round(res["asks"]["bookings"][s] / 10)
                                                       for s in K.SCHED), str({s: round(xw[s], 1) for s in K.SCHED}))

    # ------------------------------------------------------------------ rounding edges
    edges = []
    for s in K.SCHED:
        edges.append(("3+ %s" % s, edge(100 * m["reach3"][s], 0.1)))
        edges.append(("1+ %s" % s, edge(100 * res["asks"]["reach1"][s], 0.1)))
        edges.append(("bookings %s" % s, edge(res["asks"]["bookings"][s], 10)))
    edges.append(("lead", edge(100 * m["lead"], 0.1)))
    edges.append(("response", edge(gold_r["per_thousand"], 0.01)))
    edges.append(("share outside prime", edge(100 * pb["share_elsewhere"], 0.1)))
    worst = min(edges, key=lambda x: x[1] / (10 if x[0].startswith("bookings") else 0.01 if x[0] == "response" else
                                             0.1))
    row("ROUND every graded figure clear of its rounding edge",
        all(e > (1.0 if k.startswith("bookings") else 0.0005 if k == "response" else 0.005) for k, e in edges),
        "closest %s (%.4f)" % worst)
    row("ROUND weekly figures exact at one decimal", all(abs(x * 10 - round(x * 10)) < 1e-9 for x in
                                                         gold_r["above"] + [gold_r["avg"]]), "")

    # ------------------------------------------------------------------ realism sweep
    row("REAL the 2025 baseline is not a round number", gold_r["avg"] * 4 % 50 != 0, "%.1f" % gold_r["avg"])
    for s in K.SCHED:
        row("REAL schedule %s's cost is not round" % s, spend[s] % 1000 != 0, str(spend[s]))
    people = [K.REQUESTER, K.PLANNER, K.PANEL_CONTACT]
    row("REAL personas from guard.py names --geo PT --seed 270", set(people) <=
        {"Jaime Lima", "Dinis Vaz", "Lara Gomes", "Madalena Brito", "Bruno Morais", "Helena Gaspar", "Miguel Silva",
         "Benedita Leal", "Lia Coelho", "Miriam Pereira"}, ", ".join(people))
    text = ""
    for f in files:
        if f.endswith(".pdf"):
            text += _pdf_text(os.path.join(target, f))
        elif f.endswith((".csv", ".txt")) and os.path.getsize(os.path.join(target, f)) < 200000:
            text += open(os.path.join(target, f), encoding="utf-8").read()
    row("REAL no em dash, no LLM tell", "—" not in text and not re.search(
        r"\b(delve|leverage|robust|seamless|comprehensive)\b", text, re.I), "")
    late = [f for f in files if f.endswith(".csv") and _max_date(os.path.join(target, f)) > K.ASSEMBLED.date()]
    row("REAL no record dated after the pack's assembly", not late, ", ".join(late))
    for f in files:
        if f.endswith(".pdf"):
            raw = open(os.path.join(target, f), "rb").read()
            row("REAL %s carries no library banner" % f, b"ReportLab" not in raw and b"reportlab" not in raw, "")
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                app = z.read("docProps/app.xml")
                row("REAL %s saved by Excel" % f, b"Microsoft Excel" in app and b"openpyxl" not in z.read(
                    "docProps/core.xml"), "")

    # ------------------------------------------------------------------ figures.json carries the goldens' figures
    fj = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json")))
    row("FIG figures.json is the build's", fj == json.loads(json.dumps(fig, ensure_ascii=False)), "")

    fails = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if detail else ""))
    print("checks: %d rows, %d failed" % (len(ROWS), len(fails)))
    return 1 if fails else 0


def _pdf_text(path):
    import pypdf
    return " ".join(p.extract_text() or "" for p in pypdf.PdfReader(path).pages)


def _max_date(path):
    best = dt.date(1900, 1, 1)
    pat = re.compile(r"(20\d\d)-(\d\d)-(\d\d)")
    with open(path, encoding="utf-8") as f:
        for line in f:
            for y, mo, d in pat.findall(line):
                try:
                    v = dt.date(int(y), int(mo), int(d))
                except ValueError:
                    continue
                if v > best and v.year < 2027:
                    best = v
    return best
