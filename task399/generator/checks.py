"""task399 generator checks: the input gates, the realism sweep, the three rules on the clean truth, the ladder,
every semantic fork row, the ask cells and their bins. Run from build.py after the pack is cut; exit 1 on any
failure. Every SF id in the design note's fork table is asserted here as its own token."""
import collections
import csv
import datetime as dt
import json
import math
import os
import re
import shutil
import tempfile
import zipfile

import golden as G
import world as W

PEAK_H = (7, 8, 16, 17, 18)


class Checks:
    def __init__(self):
        self.rows = []

    def ok(self, name, cond, detail=""):
        self.rows.append((name, bool(cond), detail))
        return cond

    def report(self):
        bad = [r for r in self.rows if not r[1]]
        for name, cond, detail in self.rows:
            print("%-4s %-58s %s" % ("PASS" if cond else "FAIL", name, detail))
        print("%d checks, %d failed" % (len(self.rows), len(bad)))
        return not bad


def window(i):
    return W.WINDOW_START <= W.utc_to_local(i["utc"]).date() <= W.WINDOW_END


def tin(i):
    return (W.utc_to_local(i["utc"]) - i["shift_start"]).total_seconds() / 3600.0


def doc_text(path):
    """The text a reader of the document sees: every paragraph and table cell of a DOCX, every page of a PDF."""
    if path.endswith(".docx"):
        import docx
        d = docx.Document(path)
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                parts += [c.text for c in row.cells]
        for s in d.sections:
            parts += [p.text for p in s.header.paragraphs] + [p.text for p in s.footer.paragraphs]
        return "\n".join(parts)
    import pdfplumber
    with pdfplumber.open(path) as pdf:
        return "\n".join((pg.extract_text() or "") for pg in pdf.pages)


def edge_min(v, u=0.1):
    return (u / 2 - abs(v - round(v / u) * u)) * 60


def quick_resets(target):
    """Routes cancelled within twenty seconds of being set and reset from the same entrance within ten:
    (entrance, {cancelled exit, reset exit}) -> count, from the shipped control system log."""
    rows = []
    with open(os.path.join(target, "control_system/roc_signaller_actions_20251001_20260930.csv"), newline="",
              encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append((G.parse_utc(r["event_utc"]), r["server"], r["wkstn"], r["user"], r["action"],
                         r["entrance"], r["exit"]))
    by_user = collections.defaultdict(list)
    seen = set()
    for t, srv, ws, u, a, e, x in rows:
        k = (u, a, e, x, t.replace(microsecond=0))
        if k in seen:
            continue
        seen.add(k)
        by_user[u].append((t, a, e, x))
    out = collections.Counter()
    for u, lst in by_user.items():
        lst.sort()
        for k in range(len(lst) - 2):
            t1, a1, e1, x1 = lst[k]
            if a1 != "ST":
                continue
            t2, a2, e2, x2 = lst[k + 1]
            t3, a3, e3, x3 = lst[k + 2]
            if (a2 == "CN" and e2 == e1 and x2 == x1 and (t2 - t1).total_seconds() <= 20 and a3 == "RQ" and e3 == e1
                    and x3 != x1 and (t3 - t2).total_seconds() <= 10):
                out[(e1, frozenset((x1, x3)))] += 1
    return out, len(rows)


def run(S_, target, res):
    C = Checks()
    net, staff, inc = S_["net"], S_["staff"], S_["inc"]
    byp = {p["staff_no"]: p for p in staff}
    M = res["main"]
    L = M["layout"]
    win = [i for i in inc if window(i)]
    fin = lambda xs: sum(i["final_minutes"] for i in xs)

    # ------------------------------------------------------------------ input gates
    files = []
    for root, _, fs in os.walk(target):
        for f in fs:
            files.append(os.path.relpath(os.path.join(root, f), target))
    fmts = {os.path.splitext(f)[1] for f in files}
    C.ok("gate: ten or more files", len(files) >= 10, "%d files" % len(files))
    C.ok("gate: three or more formats", len(fmts) >= 3, ", ".join(sorted(fmts)))
    with open(os.path.join(target, "control_system/roc_signaller_actions_20251001_20260930.csv"), encoding="utf-8") as fh:
        n_log = sum(1 for _ in fh) - 1
    C.ok("gate: a file of 25,000 rows or more", n_log >= 25000, "control system log %d rows" % n_log)
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json"))) if os.path.exists(
        os.path.join(os.path.dirname(target), "metadata.json")) else {}
    dis = meta.get("distractor_files", [])
    C.ok("gate: two or more distractors named in metadata.json, each shipped", len(dis) >= 2 and all(
        os.path.exists(os.path.join(target, d)) for d in dis), ", ".join(dis))
    bad_names = [f for f in files if re.search(r"readme|dictionary|field.?notes|manifest|notes|schema|glossary", f, re.I)]
    C.ok("gate: no file describes the data (by name)", not bad_names, ", ".join(bad_names))
    stump_words = [f for f in files if re.search(r"slip|spacing|gap|close|distance|neighbour|design.?induced", f, re.I)]
    C.ok("gate: no file name broadcasts the step", not stump_words, ", ".join(stump_words))
    hdrs = []
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                hdrs += fh.readline().strip().split(",")
    sus = [h for h in hdrs if re.search(r"gap|spacing|distance|slip|close|px", h, re.I)]
    C.ok("R1: no shipped column holds the deciding quantity", not sus, ", ".join(sus) or "csv headers clean")

    # ------------------------------------------------------------------ realism sweep
    sn = sorted(int(p["staff_no"]) for p in staff)
    d = {b - a for a, b in zip(sn, sn[1:])}
    C.ok("realism: staff numbers not an arithmetic sequence", len(d) > 5, "%d distinct steps" % len(d))
    tr = sorted(i["trust"] for i in inc)
    d = {b - a for a, b in zip(tr, tr[1:])}
    C.ok("realism: TRUST numbers rise with uneven gaps", len(d) > 20, "%d distinct steps" % len(d))
    refs = sorted(int(i["ref"][-4:]) for i in inc if i["ref"].startswith("FROC/26"))
    C.ok("realism: register numbers carry gaps", any(b - a > 1 for a, b in zip(refs, refs[1:])))
    desks = [W.DESK[w] for w in W.WS_IDS]
    C.ok("realism: workstation numbers do not follow the alphabet", desks != sorted(desks), " ".join(desks))
    per_ws = collections.Counter(i["ws"] for i in win)
    C.ok("realism: incident counts differ by workstation", len(set(per_ws.values())) == len(per_ws), str(dict(per_ws)))
    C.ok("realism: the call's minutes are not a round figure", M["b_minutes"] % 50 != 0, str(M["b_minutes"]))
    cn_all = sum(1 for e in S_["res"]["events"] if e[3] == "CN")
    resets, _ = quick_resets(target)
    C.ok("realism: quick resets are a minority of the log's cancellations", sum(resets.values()) < 0.25 * cn_all,
         "%d quick resets of %d cancellations" % (sum(resets.values()), cn_all))
    fnd = collections.Counter(i["finding"] for i in win if i["type"] == "RS1")
    C.ok("realism: investigators' findings on wrong routes vary", len(fnd) >= 4, str(dict(fnd)))
    import openpyxl
    crow = list(openpyxl.load_workbook(os.path.join(target, "staffing/signaller_competence_register.xlsx"),
                                       read_only=True)["Competence"].iter_rows(values_only=True))
    comp_from = {}
    for row in crow[1:]:
        for j, ws in enumerate(W.WS_IDS):
            v = row[4 + j]
            if v is not None:
                comp_from[(str(row[0]), ws)] = v.date() if isinstance(v, dt.datetime) else v
    early = [(s, ws, s0) for s, ws, s0, s1, how in S_["ros"]["spans"] if (s, ws) not in comp_from or
             s0.date() < comp_from[(s, ws)]]
    late = [k for k, v in comp_from.items() if v > dt.date(2026, 8, 28)]
    C.ok("realism: nobody works a workstation before the competence date the register gives it, and no date is "
         "later than the register", not early and not late, "%d early, %d late" % (len(early), len(late)))
    people = ["Helen Douglas", "Alan Pope", "Zoe Hayward", "Joanna Bryan", "Julian Thomson", "Jake Bray"]
    drawn = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "names_drawn.txt")).read()
    C.ok("realism: every persona drawn with guard.py names", all(p in drawn for p in people))

    # ------------------------------------------------------------------ the decisive geometry
    gaps = M["rs1_gaps"]
    close = [g for g in gaps if g <= 12]
    far = [g for g in gaps if g > 12]
    C.ok("geometry: every wrong route's exits are drawn under 12 px or over 36 px apart",
         max(close) <= W.CLOSE_MAX and min(far) >= W.FAR_MIN, "%.1f against %.1f px" % (max(close), min(far)))
    seps = [rt["sep"] for rt in net["routes"] if rt["multi"] and rt.get("sep") is not None]
    C.ok("geometry: no exit pair anywhere is drawn between 12 and 36 px", all(s <= 12 or s >= 36 for s in seps))
    slips_truth = {i["ref"] for i in win if i["mech"] == "slip"}
    slips_pack = {i["ref"] for i in M["incidents"] if i["slip"]}
    C.ok("SF6: the slips read from the drawn positions are exactly the slips", slips_truth == slips_pack,
         "%d slips" % len(slips_pack))
    for thr in (14, 20, 30, 40, 50):
        s = {i["ref"] for i in M["incidents"] if i["exit_gap_px"] is not None and i["exit_gap_px"] <= thr
             and i["code"] == "RS1"}
        C.ok("SF6: the slip set is the same at a %d px reading" % thr, s == slips_pack)
    prone = set(resets)
    by_reset = {i["ref"] for i in M["incidents"] if i["code"] == "RS1" and i["route_set"] and i["route_required"]
                and (L["routes"][i["route_required"]][0], frozenset((L["routes"][i["route_set"]][1],
                                                                     L["routes"][i["route_required"]][1]))) in prone}
    C.ok("SF6: the slips read from the log's quick resets are the same set", by_reset == slips_pack,
         "%d pairs carry quick resets" % len(prone))
    close_pairs = {(rt["entrance"], frozenset((rt["exit"], net["rmap"][rt["neighbour"]]["exit"])))
                   for rt in net["routes"] if rt["close"]}
    ar_close = [i for i in M["incidents"] if i["code"] == "AR1" and i["route_set"] and i["route_required"] and
                (L["routes"][i["route_set"]][0], frozenset((L["routes"][i["route_set"]][1],
                                                            L["routes"][i["route_required"]][1]))) in close_pairs]
    C.ok("SF6: no ARS wrong route falls on a drawn-close pair, so the geometry reads the same with ARS included",
         not ar_close, "%d" % len(ar_close))
    qc, qb = M["quick_cancels"], M["quick_cancels_beside"]
    C.ok("step 4: of the routes cancelled within twenty seconds of being set, all but three were followed from the "
         "same entrance by the exit drawn beside", qc - qb == 3 and qb >= 300, "%d of %d" % (qb, qc))
    C.ok("evidence: quick resets fall only on the drawn-close pairs", prone <= close_pairs,
         "%d of %d reset pairs" % (len(prone & close_pairs), len(prone)))

    # ------------------------------------------------------------------ programme figures on the clean truth
    B = fin([i for i in win if i["mech"] in ("slip", "display")])
    A_ub = fin([i for i in win if i["fy"] and i["mech"] in ("mistake", "workload", "fatigue", "regulation",
                                                            "communication")])
    C_ub = fin([i for i in win if i["mech"] not in ("slip", "display", "ars") and tin(i) >= 8])
    D_ = fin([i for i in win if i["mech"] == "ars"])
    E_ub = fin([i for i in win if i["mech"] == "workload" and i["ws"] == "W03"])
    A_loose = fin([i for i in win if i["fy"]])
    C_loose = fin([i for i in win if tin(i) >= 8])
    E_loose = fin([i for i in win if i["ws"] == "W03"])
    rival = max(A_ub, C_ub, D_, E_ub)
    C.ok("golden: the pack's figure is the clean truth's", B == M["b_minutes"], "%d" % B)
    C.ok("SF7: the display renewal beats every rival's widest honest reach by 1.5x", B >= 1.5 * rival,
         "B %d, A %d, C %d, D %d, E %d, margin %.2f" % (B, A_ub, C_ub, D_, E_ub, B / rival))
    C.ok("SF7: and beats every rival credited with every incident it touches", B > max(A_loose, C_loose, E_loose),
         "A %d, C %d, E %d" % (A_loose, C_loose, E_loose))

    # ------------------------------------------------------------------ the three rules on the clean truth
    prog = M["by_prog_findings"]
    r0 = max(prog, key=prog.get)
    C.ok("R3a: the default path (findings booked to the catalogue) files A", r0 == "A", str(prog))
    rank_b = sorted(prog, key=lambda k: -prog[k]).index("B") + 1
    C.ok("ladder: the golden sits fourth or fifth on the default path", rank_b >= 4, "rank %d" % rank_b)
    dist = M["findings"].get("distraction", 0)
    alts = []
    for to in (None, "A", "E", "C"):
        alt = dict(prog)
        if to:
            alt[to] = alt.get(to, 0) + dist
        alts.append(max(alt, key=alt.get))
    C.ok("ladder: however the distraction findings are booked, the default path files A or E, never B",
         alts[0] == "A" and set(alts) <= {"A", "E"}, "distraction %d minutes, calls %s" % (dist, alts))
    reb = dict(prog)
    moved = M["slip_minutes"]
    reb["B"] = reb.get("B", 0) + moved
    # the slips were booked across competence, distraction and workload findings
    slip_by_f = collections.Counter()
    for i in M["incidents"]:
        if i["slip"]:
            slip_by_f[i["finding"]] += i["minutes"]
    for f, v in slip_by_f.items():
        if f in G.PROGRAMME_OF_FINDING:
            reb[G.PROGRAMME_OF_FINDING[f]] -= v
    C.ok("R3b: the default path with only the slips re-attributed files B", max(reb, key=reb.get) == "B", str(reb))
    # rung 1: error probability per manual request by the performance shaping factors on record
    req = collections.Counter()
    for e in S_["res"]["events"]:
        if e[3] != "RQ":
            continue
        lc = W.utc_to_local(e[0])
        if not (W.WINDOW_START <= lc.date() <= W.WINDOW_END):
            continue
        req[("fy", W.first_two_years(byp[e[2]], lc.date()))] += 1
        req[("pk", lc.hour in PEAK_H)] += 1
    wr = [i for i in win if i["type"] == "RS1"]
    rfy = sum(1 for i in wr if i["fy"]) / req[("fy", True)]
    rex = sum(1 for i in wr if not i["fy"]) / req[("fy", False)]
    rpk = sum(1 for i in wr if W.utc_to_local(i["utc"]).hour in PEAK_H) / req[("pk", True)]
    rop = sum(1 for i in wr if W.utc_to_local(i["utc"]).hour not in PEAK_H) / req[("pk", False)]
    C.ok("ladder: wrong routes per request run higher for first-two-years signallers", rfy >= 1.25 * rex,
         "%.2f against %.2f per 10,000" % (1e4 * rfy, 1e4 * rex))
    C.ok("ladder: wrong routes per request run higher in the peaks", rpk >= 1.25 * rop,
         "%.2f against %.2f per 10,000" % (1e4 * rpk, 1e4 * rop))
    # inside the drawn-close routes the slip rate does not follow experience or the hour
    import staffing as ST
    idx = ST.on_duty_index(S_["ros"]["spans"])
    creq = collections.Counter()
    for e in S_["res"]["events"]:
        if e[3] != "RQ" or not net["rmap"][e[6]]["close"]:
            continue
        lc = W.utc_to_local(e[0])
        if not (W.WINDOW_START <= lc.date() <= W.WINDOW_END):
            continue
        sn, s0, how = ST.who_at(idx, e[1], e[0])
        creq[("fy", W.first_two_years(byp[e[2]], lc.date()))] += 1
        creq[("pk", lc.hour in PEAK_H)] += 1
        creq[("late", s0 is not None and (lc - s0).total_seconds() >= 8 * 3600)] += 1
    sl = [i for i in win if i["mech"] == "slip"]

    def slip_ratio(key, pred):
        a = sum(1 for i in sl if pred(i)) / creq[(key, True)]
        b = sum(1 for i in sl if not pred(i)) / creq[(key, False)]
        return a / b
    for key, pred, what in (("fy", lambda i: i["fy"], "for both experience bands"),
                            ("pk", lambda i: W.utc_to_local(i["utc"]).hour in PEAK_H, "in the peaks and out of them"),
                            ("late", lambda i: tin(i) >= 8, "after eight hours on shift and before")):
        v = slip_ratio(key, pred)
        C.ok("evidence: at the drawn-close routes slips per request run alike %s" % what, 0.75 <= v <= 1.33,
             "ratio %.2f" % v)
    C.ok("realism: the display renewal's minutes differ by workstation", len(set(M["b_by_ws"].values())) == 6,
         str(M["b_by_ws"]))
    cat = doc_text(os.path.join(target, "governance/improvement_catalogue_2027.docx"))
    tor = doc_text(os.path.join(target, "governance/2027_improvement_plan_terms_of_reference.pdf"))
    wla = doc_text(os.path.join(target, "reference/fenmoor_roc_workload_assessment_2025.pdf"))
    C.ok("control: the catalogue, the terms of reference and the workload report are read",
         "Workstation display renewal" in cat and "would not have happened had that programme been in place" in tor
         and "Hatherby" in wla and min(len(cat), len(tor), len(wla)) > 1500, "%d, %d, %d chars" % (
             len(cat), len(tor), len(wla)))
    from pypdf import PdfReader
    same = []
    for rel in ("governance/2027_improvement_plan_terms_of_reference.pdf",
                "reference/fenmoor_roc_workload_assessment_2025.pdf"):
        pth = os.path.join(target, rel)
        t1 = "".join(pg.extract_text() or "" for pg in PdfReader(pth, strict=True).pages)
        t2 = "".join(pg.extract_text() or "" for pg in PdfReader(pth).pages)
        same.append(t1 == t2 and len(t1) > 1000)
    C.ok("realism: every shipped PDF reads the same strict and lenient (and through pdfplumber above)", all(same))
    rank_words = r"\b(benefit|priorit|rank|recommend|expected reduction|would remove|would prevent|minutes saved)"
    C.ok("R3c: no plant: no document ranks or prices the programmes on minutes",
         not re.search(rank_words, cat, re.I) and not re.search(rank_words, tor, re.I))
    C.ok("R3c: the workload report names no programme and no minutes figure",
         not re.search(r"display renewal|seventh workstation|eight-hour|delay minutes", wla, re.I))
    C.ok("leak: no document names the drawn spacing of the exits", not any(re.search(
        r"pixel|spacing|too close|adjacent exit|squeez|crowd|slip", t, re.I) for t in (cat, tor, wla)))
    C.ok("R3c: the investigators' findings were set from what an investigator sees, never the mechanism",
         len({i["finding"] for i in wr if i["mech"] == "slip"}) >= 3)

    # ------------------------------------------------------------------ semantic forks on the main call
    tot_p = sum(i["delay_records"][0][2] for i in win if i["mech"] in ("slip", "display"))
    C.ok("SF1: primary-only minutes would print another figure, the ToR files both", tot_p != B, "%d" % tot_p)
    all_moves = sum((-m["minutes"] if m["out"] else m["minutes"]) for m in S_["moves"]
                    if m["inc"]["mech"] in ("slip", "display") and window(m["inc"]))
    agreed = sum((-m["minutes"] if m["out"] else m["minutes"]) for m in S_["moves"]
                 if m["inc"]["mech"] in ("slip", "display") and window(m["inc"]) and m["status"] == "Agreed")
    C.ok("SF2: agreed moves applied (ToR 2.4); every move applied, or none, leaves the call",
         min(B - agreed, B - agreed + all_moves) >= 1.4 * rival, "agreed %+d, all %+d" % (agreed, all_moves))
    edge = [i for i in inc if W.near_window_edge(i["utc"], hours=2.0)]
    C.ok("SF3: no incident within two hours of the window's ends (UK time against UTC converge)", not edge,
         "%d" % len(edge))
    C.ok("SF4: both financial-year registers carry the window", {i["ref"][:7] for i in M["incidents"]} >=
         {"FROC/25", "FROC/26"})
    C.ok("SF5: the investigations' findings never name the display for a wrong route", not any(
        i["finding"] == "equipment" for i in wr))
    C.ok("SF19: the catalogue files that B removes the VDS-3 equipment from every workstation",
         "The VDS-3 equipment removed from every workstation." in cat)
    C.ok("SF19: the figure moves without the display faults (so the scope sentence closes it)",
         M["slip_minutes"] != M["b_minutes"] and M["n_eq"] == 10, "%d against %d" % (M["slip_minutes"],
                                                                                     M["b_minutes"]))
    C.ok("SF19: the display faults counted for B or left out, the call stands",
         M["slip_minutes"] >= 1.5 * rival and M["eq_minutes"] > 0, "%d without the faults against %d" % (
             M["slip_minutes"], rival))
    C.ok("SF8: by-workstation minutes add to the figure", sum(M["b_by_ws"].values()) == M["b_minutes"])
    srt = sorted(M["b_by_ws"].values(), reverse=True)
    C.ok("SF9: the starting workstation leads the next by 1.2x", srt[0] >= 1.2 * srt[1], "%d against %d" % tuple(srt[:2]))
    styles = collections.Counter()
    for f in ("incidents/operating_incident_register_2025-26.xlsx",):
        import openpyxl
        rows = list(openpyxl.load_workbook(os.path.join(target, f), read_only=True).active.iter_rows(values_only=True))
        h = {k: i for i, k in enumerate(rows[0])}
        for r in rows[1:]:
            for col in ("Route set", "Route required"):
                v = r[h[col]]
                if v:
                    styles["to" if " to " in v else ("dash" if "-" in v else "id")] += 1
    rs1_parsed = [i for i in M["incidents"] if i["code"] == "RS1"]
    C.ok("SF10: every wrong route's text, in any of the register's three forms, maps to one layout route",
         all(i["route_set"] and i["route_required"] for i in rs1_parsed) and len(styles) == 3, str(dict(styles)))
    C.ok("SF11: every registered window incident carries operating-centre delay", all(
        i["trust"] is not None for i in M["incidents"]))
    C.ok("SF12: no window incident ends at nil minutes", all(i["minutes"] > 0 for i in M["incidents"]))
    init = sum(i["initial"] for i in win if i["mech"] in ("slip", "display"))
    C.ok("SF13: the register's initial delays would print another figure (ToR 2.4 files the attribution)",
         init != B, "%d" % init)
    # R2: each Layer 1 item's natural mishandling leaves the call and the components
    alt_ws = collections.Counter()
    for i in M["incidents"]:
        if i["slip"] or i["code"] == "EQ1":
            alt_ws[i["ws"]] += i["minutes"]
    C.ok("R2: desk names against numbers leave the split by workstation", dict(alt_ws) == {
        k: v for k, v in M["b_by_ws"].items() if v})
    C.ok("R2: the call holds on the registers' initial delays", init > 1.5 * sum(
        i["initial"] for i in win if i["fy"] and i["mech"] in ("mistake", "workload", "fatigue", "regulation",
                                                               "communication")))
    C.ok("R2: the call holds on primary minutes only", tot_p > sum(
        i["delay_records"][0][2] for i in win if i["mech"] not in ("slip", "display", "ars") and tin(i) >= 8))

    # ------------------------------------------------------------------ asks
    H, A = res["hours"], res["ars"]
    lo, hi = dt.datetime(2025, 10, 1), dt.datetime(2026, 10, 1)
    th = collections.defaultdict(float)
    for s, ws, s0, s1, how in S_["ros"]["spans"]:
        a, b = max(s0, lo), min(s1, hi)
        if b <= a:
            continue
        band = "first two years" if W.first_two_years(byp[s], a.date()) else "other"
        th[(ws, band)] += (W.local_to_utc(b) - W.local_to_utc(a)).total_seconds() / 3600.0
    C.ok("ask 1: every hours cell recomputes from the pack to the truth", max(abs(th[k] - H[k]) for k in H) < 1e-9)
    C.ok("ask 1: every hours cell sits at least 0.02 h from its rounding edge",
         min(edge_min(v) for v in H.values()) >= 1.2, "%.2f min" % min(edge_min(v) for v in H.values()))
    C.ok("ask 1: every hours cell sits at least a minute from its rounding edge",
         min(edge_min(v) for v in H.values()) >= 1.0, "%.2f min" % min(edge_min(v) for v in H.values()))
    ta = collections.defaultdict(float)
    for p in S_["periods"]:
        for name, q0, q1 in G.QUARTERS:
            x = max(p["off"], W.local_to_utc(dt.datetime.combine(q0, dt.time(0))))
            y = min(p["on"], W.local_to_utc(dt.datetime.combine(q1, dt.time(0))))
            if y > x:
                ta[(p["ws"], name)] += (y - x).total_seconds() / 3600.0
    C.ok("ask 2: every ARS cell recomputes from the pack to the truth", max(abs(ta[k] - A[k]) for k in A) < 1e-9)
    C.ok("realism: no two ask cells print the same figure", len({round(v, 1) for v in A.values()}) == len(A) and
         len({round(v, 1) for v in H.values()}) == len(H))
    C.ok("ask 2: every ARS cell sits at least 0.02 h from its rounding edge",
         min(edge_min(v) for v in A.values()) >= 1.2, "%.2f min" % min(edge_min(v) for v in A.values()))
    _, ivals = G.ars_hours(target, L)
    sa_cell = collections.defaultdict(float)
    for sa, lst in ivals.items():
        for a_, b_ in lst:
            for name, q0, q1 in G.QUARTERS:
                x = max(a_, W.local_to_utc(dt.datetime.combine(q0, dt.time(0))))
                y = min(b_, W.local_to_utc(dt.datetime.combine(q1, dt.time(0))))
                if y > x:
                    sa_cell[(sa, name)] += (y - x).total_seconds() / 3600.0
    C.ok("SF21: a per-sub-area table would meet no cell within 0.02 h of a rounding line",
         min(edge_min(v) for v in sa_cell.values()) >= 1.2 and len(sa_cell) >= 55,
         "%d cells, nearest %.2f min" % (len(sa_cell), min(edge_min(v) for v in sa_cell.values())))
    no_fail, _ = G.ars_hours(target, L, keep=lambda row: row["reason"] != "FAIL")
    moved = sum(1 for k in A if abs(no_fail[k] - A[k]) >= 0.05)
    C.ok("SF20: the FAIL rows read OFF, and leaving them out would move the cells", moved >= 6,
         "%d of %d cells move" % (moved, len(A)))
    C.ok("ask 2: every ARS cell sits at least a minute from its rounding edge",
         min(edge_min(v) for v in A.values()) >= 1.0, "%.2f min" % min(edge_min(v) for v in A.values()))
    nights = []
    for s, ws, s0, s1, how in S_["ros"]["spans"]:
        if s0 in (dt.datetime(2025, 9, 30, 19), dt.datetime(2026, 9, 30, 19)):
            nights.append(W.first_two_years(byp[s], s0.date()))
    C.ok("SF14: both boundary nights were worked outside the first two years (by time or by start converge)",
         not any(nights) and len(nights) == 12)
    cross = 0
    for s, ws, s0, s1, how in S_["ros"]["spans"]:
        q = byp[s]["qualified"]
        for dday in (q, G.anniversary(q)):
            m = dt.datetime.combine(dday, dt.time(0))
            if s0 < m < s1:
                cross += 1
    C.ok("SF15: no worked span crosses a qualification or second anniversary", cross == 0)
    dst = [(ws, s0) for s, ws, s0, s1, how in S_["ros"]["spans"] if s0.date() in (dt.date(2025, 10, 25), dt.date(2026, 3, 28))
           and s0.hour == 19]
    C.ok("SF16: the clock-change nights are worked and last 13 and 11 hours", len(dst) == 12)
    quiet = [(x, y) for x, y in __import__("ops").quiet_windows()]
    near = [p for p in S_["periods"] if any(not (p["on"] <= x or p["off"] >= y) for x, y in quiet)]
    C.ok("SF17: no ARS interval within two hours of a quarter boundary (UK and UTC quarters converge)", not near)
    C.ok("SF18: workstation-wide ARS drops are logged once for the workstation", len(S_["drops"]) >= 12,
         "%d drops" % len(S_["drops"]))
    # ask devices, measured on the cut pack
    import staffing as ST2
    idx2 = ST2.on_duty_index(S_["ros"]["spans"])
    unrec = [c for c in S_["ros"]["changes"] if c.get("unrecorded")]
    C.ok("ask 1 device: every workstation has a day's change missing from the changes list that moves its bands",
         {c["ws"] for c in unrec} == set(W.WS_IDS) and all(
             W.first_two_years(byp[c["rostered"]], c["day"]) != W.first_two_years(byp[c["worked"]], c["day"])
             for c in unrec), "%d changes" % len(unrec))
    acts_by = collections.defaultdict(list)
    for e in S_["res"]["events"]:
        acts_by[e[2]].append(e[0])
    ok_ev = True
    for c in unrec:
        a, b = W.local_to_utc(c["start"]), W.local_to_utc(c["end"])
        ros_acts = sum(1 for t in acts_by[c["rostered"]] if a <= t < b)
        wk_acts = sum(1 for t in acts_by[c["worked"]] if a <= t < b)
        ok_ev = ok_ev and ros_acts == 0 and wk_acts >= 20
    C.ok("ask 1 device: the control system shows only the signaller who worked each of those shifts", ok_ev)
    import bisect
    lag = collections.Counter()
    with open(os.path.join(target, "control_system/ars_status_log_20251001_20260930.csv"), newline="",
              encoding="utf-8") as fh:
        ars_rows = list(csv.DictReader(fh))
    code = lambda c: L["old"].get(c, c)
    a_t = collections.defaultdict(list)
    for r in ars_rows:
        if r["server"] == "ROC-A":
            a_t[(code(r["subarea"]), r["state"])].append(G.parse_utc(r["logged_utc"]))
    for v in a_t.values():
        v.sort()
    n_copies = 0
    for r in ars_rows:
        if r["server"] == "ROC-B" and not r["user"]:
            n_copies += 1
            t = G.parse_utc(r["logged_utc"])
            lst = a_t[(code(r["subarea"]), r["state"])]
            for hh in (1, 2):
                u = t - dt.timedelta(hours=hh)
                k = bisect.bisect_right(lst, u) - 1
                if k >= 0 and 0 < (u - lst[k]).total_seconds() < 1.0:
                    lag[hh] += 1
    edge_copies = sum(1 for r in ars_rows if r["server"] == "ROC-B" and not r["user"] and (
        G.parse_utc(r["logged_utc"]) < dt.datetime(2025, 10, 1, 2) or G.parse_utc(r["logged_utc"]) >
        dt.datetime(2026, 9, 30, 22)))
    C.ok("ask 2 device: server B's copies sit one hour (winter) or two (summer) behind A's",
         lag[1] > 1000 and lag[2] > 1000 and lag[1] + lag[2] + edge_copies >= n_copies,
         "%d and %d of %d copies, %d at the export's edges" % (lag[1], lag[2], n_copies, edge_copies))
    b_only = [r for r in ars_rows if r["server"] == "ROC-B" and r["user"]]
    C.ok("ask 2 device: B alone logged events on A's maintenance nights", len(b_only) >= 12, "%d rows" % len(b_only))
    import ceiling
    cm = ceiling.main(target)
    C.ok("asks: the cracker keeps no ask figure", cm["cracker"] == 0.0, "%.1f per cent" % (100 * cm["cracker"]))
    C.ok("asks: the mirror keeps under two fifths of the ask figures", cm["mirror"] < 0.4,
         "%.1f per cent" % (100 * cm["mirror"]))
    C.ok("asks: the pair sits under 60, and under 60 with both on the call", cm["pair"] <= 60 and cm["both_on_call"]
         <= 60, "%.1f and %.1f" % (cm["pair"], cm["both_on_call"]))

    # separation: no ask device row in the main call's population, and the main call reads no ask file
    C.ok("separation: the call is unchanged with the ask files deleted", call_without(target, [
        "staffing", "control_system/ars_status_log_20251001_20260930.csv"]) == M["b_minutes"])
    for dname in dis:
        C.ok("distractor %s: deleting it moves nothing" % os.path.basename(dname),
             call_without(target, [dname]) == M["b_minutes"])
    return C


def call_without(target, rels):
    tmp = tempfile.mkdtemp(prefix="t399chk_")
    try:
        dst = os.path.join(tmp, "target")
        shutil.copytree(target, dst)
        for rel in rels:
            p = os.path.join(dst, rel)
            if os.path.isdir(p):
                shutil.rmtree(p)
            elif os.path.exists(p):
                os.remove(p)
        return G.main_call(dst)["b_minutes"]
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    import sys
    import build as B
    S_ = B.world()
    B.cut(B.TARGET, S_)
    res = G.compute(B.TARGET)
    ok = run(S_, B.TARGET, res).report()
    sys.exit(0 if ok else 1)
