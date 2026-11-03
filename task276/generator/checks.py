"""Assertions on every build: input gates, the three rules on the clean truth, the ladder, every SF row, bin edges,
the separation line, the back-test, realism and the documents.  run() returns the count passed; LOG holds the lines."""
import collections
import csv
import datetime as dt
import os
import re
import zipfile

import params as P
import build as B
import solve as SV
import ceiling as CE

LOG = []


def ok(label, cond, detail=""):
    LOG.append("%s %s %s" % ("PASS" if cond else "FAIL", label, detail))
    assert cond, (label, detail)


def edge(v, u):
    return u / 2.0 - abs(v - round(v / u) * u)


def rk(v):
    return int(round(v / 1000.0)) * 1000


def lead(d):
    o = sorted(d, key=lambda n: -d[n])
    return o[0], d[o[0]] / d[o[1]]


def run(target, golden, W, S, A):
    LOG.clear()
    n0 = 0
    names = S["names"]
    files = [os.path.relpath(os.path.join(r, f), target) for r, _, fs in os.walk(target) for f in fs]
    fmts = {f.rsplit(".", 1)[1] for f in files}
    rows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok("G1 input gates", len(files) >= 10 and len(fmts) >= 3 and max(rows.values()) >= 25000,
       "%d files, formats %s, largest %d rows" % (len(files), sorted(fmts), max(rows.values())))
    ok("G2 distractors shipped and never read by the solution",
       all(os.path.exists(os.path.join(target, B.FILES[k])) for k in B.DISTRACTORS)
       and not set(B.FILES[k] for k in B.DISTRACTORS) & set(SV.F.values()), str([B.FILES[k] for k in B.DISTRACTORS]))
    bad = [f for f in files if re.search(r"readme|dictionary|notes|manifest|codebook|field", f, re.I)]
    ok("G3 no file describes the data", not bad, str(bad))
    for f in files:
        if f.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                wbx = z.read("xl/workbook.xml").decode()
            ok("G3 no notes sheet in %s" % f, not re.search(r'name="[^"]*(note|readme|about)', wbx, re.I))

    # ------------------------------------------------ the three rules on the clean truth
    ok("R1 raw material ships at event and quarter-hour grain", rows[B.FILES["barrier"]] > 200000 and
       rows[B.FILES["counts"]] > 80000, str(rows))
    heads = {f: open(os.path.join(target, f), encoding="utf-8").readline().strip() for f in rows}
    ok("R1 no column holds the deciding quantity", not any(re.search(r"delay|vehicle_hours|queue", h, re.I)
                                                           for h in heads.values()), str(heads))
    V = S["variants"]
    ok("R2 sensor-bounce repeats neutral", all(abs(V["no_dedupe"][n] - S["delay"][n]) < 1e-6 for n in names))
    lf, mf = lead(V["utc_unconverted_free"])
    ok("R2 the UTC clock read as local leaves the closure model on Station Road", lf == "Station Road", "%.2f" % mf)
    ok("R2 the UTC clock read as local leaves every non-Mill crossing's delay in its thousand",
       all(rk(V["utc_unconverted_free"][n]) == rk(S["delay"][n]) for n in names if n != "Mill Lane"))
    l3, m3 = lead(S["free"])
    ok("R3a the analyst test: the closure model with every filed rule names Station Road", l3 == "Station Road" and m3 >= 1.15,
       "%.3f" % m3)
    l5, m5 = lead(S["delay"])
    ok("R3b the decisive step alone (the replay through the section's controls) names Mill Lane", l5 == "Mill Lane" and m5 >= 1.2,
       "%.3f" % m5)
    per = S["per"]
    for key, label in (("closures", "R0"), ("minutes", "R1"), ("held", "R2")):
        ld, m = lead({n: per[n][key] for n in names})
        ok("R3b lower rung %s (%s) does not name Mill Lane, margin 1.15 or more" % (label, key), ld != "Mill Lane" and m >= 1.15,
           "%s %.3f" % (ld, m))
    l4, m4 = lead(S["wb_only"])
    ok("L4 the bridge for the westbound queue only names Mill Lane", l4 == "Mill Lane" and m4 >= 1.15, "%.3f" % m4)
    ok("L0 closures per morning name Common Road", lead({n: per[n]["closures"] for n in names})[0] == "Common Road")
    ok("L1 closure minutes name Station Road", lead({n: per[n]["minutes"] for n in names})[0] == "Station Road")
    cnt_days = collections.Counter()
    for (c, k, d), (veh, hgv) in W["counts"].items():
        if B.day_type(d, P.CROSSINGS[c]["county"]) == "school":
            cnt_days[(c, k, tuple(veh))] += 1
    ok("R3c no copied count block (no site repeats a school morning's counts)", max(cnt_days.values()) == 1)
    seen = collections.Counter(tuple((x[0], x[1]) for x in W["closures"][c][d]) for c in P.ORDER for d in B.days())
    ok("R3c no copied closure day", max(seen.values()) == 1)

    # ------------------------------------------------ semantic forks
    evs = set()
    with open(os.path.join(target, B.FILES["barrier"]), newline="") as fh:
        rdr = csv.reader(fh)
        hb = next(rdr)
        for r in rdr:
            evs.add(r[3])
    ok("SF1 the log carries only LOWERED and RAISED", evs == {"LOWERED", "RAISED"}, str(evs))
    ok("SF2 the barrier clock is named UTC in its header", hb[2] == "event_time_utc", str(hb))
    sd_counts = {c: len(S["sdays"][c]) for c in names}
    ok("SF3 school days per county as filed", all(180 <= v <= 196 for v in sd_counts.values()), str(sd_counts))
    ok("SF3 the brief files the county's own term dates", "published term dates of the county the crossing lies in" in
       re.sub(r"\s+", " ", SV.shortlist(target)[1]))
    ok("SF4 SF12 the replay started at 07:00 keeps every thousand", all(rk(V["start7"][n]) == rk(S["delay"][n]) for n in names))
    ok("SF5 every crossing with no control in its section gives the closure model's figure",
       all(abs(S["delay"][n] - S["free"][n]) < 1e-6 for n in names if not S["layout"][n]["gate"]))
    ok("SF5 only Mill Lane's section holds a control", [n for n in names if S["layout"][n]["controls"]] == ["Mill Lane"])
    M = S["M"]
    ok("SF6 saturation flow 1,800 an hour per lane, Common Road two lanes", M["sat"] == 1800 and
       S["layout"]["Common Road"]["lanes"] == 2 and all(S["layout"][n]["lanes"] == 1 for n in names if n != "Common Road"))
    ok("SF7 arrivals at the start of each quarter hour keep every thousand",
       all(rk(V["start_mode"][n]) == rk(S["delay"][n]) for n in names))
    g = S["layout"]["Mill Lane"]["gate"]
    ok("SF8 storage 42 m at 5.75 m a vehicle is seven, floor and nearest agree",
       g["storage_m"] == 42 and int(42 // 5.75) == 7 == int(round(42 / 5.75)))
    ok("SF8 six or eight vehicles of storage keep Mill Lane's thousand",
       rk(V["N6"]["Mill Lane"]) == rk(V["N8"]["Mill Lane"]) == rk(S["delay"]["Mill Lane"]),
       "%.0f %.0f %.0f" % (V["N6"]["Mill Lane"], S["delay"]["Mill Lane"], V["N8"]["Mill Lane"]))
    ok("SF9 effective green filed as the displayed green", "Effective green is taken as the displayed green" in M["text"])
    ok("SF10 two or five seconds of travel between stop lines keep Mill Lane's thousand",
       rk(V["tau2"]["Mill Lane"]) == rk(V["tau5"]["Mill Lane"]) == rk(S["delay"]["Mill Lane"]))
    ok("SF11 bounce repeats dropped or kept, same figures", all(abs(V["no_dedupe"][n] - S["delay"][n]) < 1e-6 for n in names))
    ok("SF13 the brief sums each counted vehicle's extra time", "summed over the school days" in
       re.sub(r"\s+", " ", SV.shortlist(target)[1]))
    gaps = [rk(V[k]["Mill Lane"] - V[k]["Station Road"]) for k in ("start_mode", "N6", "N8", "tau2", "tau5", "start7")]
    ok("SF14 the gap from unrounded and from rounded figures, and under every variant, is the same thousand",
       rk(S["gap"]) == rk(S["delay"]["Mill Lane"]) - rk(S["delay"]["Station Road"]) and set(gaps) == {rk(S["gap"])},
       str(gaps))
    at10 = sum(1 for c in P.ORDER for d in B.school_days(P.CROSSINGS[c]["county"]) for x in W["closures"][c][d]
               if x[0] in (7 * 3600, 10 * 3600))
    ok("SF15 no school-day closure begins exactly at 07:00:00 or 10:00:00", at10 == 0, str(at10))
    held = [x for c in P.ORDER for d in B.days() for x in W["closures"][c][d] if x[2] in ("fault", "reset")]
    ok("SF16 every fault-held closure carries a reported closing fault or a signaller's reset", len(held) ==
       sum(1 for o in W["orders"] if o.get("closing")) + sum(1 for o in W["occ"] if o["kind"] == "reset"), str(len(held)))
    ok("SF17 the heavy share's population: both approaches, quarter hours 07:00 to 09:45, school days",
       all(len(S["layout"][n]["sites"]) == 2 for n in names))
    first, last = min(B.days()), max(B.days())
    ok("SF18 the log covers 1 September 2025 to 31 August 2026", first == dt.date(2025, 9, 1) and last == dt.date(2026, 8, 31))
    cnt = SV.counts(target)
    miss = sum(1 for n in names for s in S["layout"][n]["sites"] for d in S["sdays"][n]
               if len(cnt[(s["site"], d)]) != 20)
    ok("SF19 no count dropout on a school day between 06:00 and 11:00", miss == 0, str(miss))
    ok("SF20 Common Road's two lanes a direction in the links file", S["layout"]["Common Road"]["lanes"] == 2)

    # ------------------------------------------------ bins
    for n in names:
        e = edge(S["delay"][n], 1000)
        ok("B1 %s's delay clear of its thousand edge" % n, e >= 150, "%.0f (%.0f)" % (S["delay"][n], e))
        for key in ("start_mode", "N6", "N8", "tau2", "tau5", "start7"):
            ok("B1 %s's delay keeps its thousand under %s" % (n, key), rk(V[key][n]) == rk(S["delay"][n]))
    for n in names:
        ok("B3 %s's closures per morning clear of the edge" % n, edge(per[n]["closures"], 0.1) >= 0.008,
           "%.4f" % per[n]["closures"])
        ok("B4 %s's fault-held hours clear of the edge" % n, edge(S["fault"]["golden"][n], 0.1) >= 0.02,
           "%.4f" % S["fault"]["golden"][n])
        ok("B5 %s's heavy share clear of the edge" % n, edge(S["hgv"]["golden"][n], 0.1) >= 0.025,
           "%.4f" % S["hgv"]["golden"][n])

    # ------------------------------------------------ the asks, the separation line and the ceiling
    F1 = CE.F1
    moved = [n for n in names if F1(S["fault"]["careful"][n]) != F1(S["fault"]["golden"][n])]
    ok("K1 the careful fault route misses the crossings carrying a device", set(moved) == {"Station Road", "Common Road",
       "Long Drove", "Church Lane"}, str(moved))
    ok("K1 the lazy and long-closure reads miss every fault figure", all(F1(S["fault"][r][n]) != F1(S["fault"]["golden"][n])
                                                                          for r in ("lazy", "long10") for n in names))
    moved = [n for n in names if F1(S["hgv"]["lazy"][n]) != F1(S["hgv"]["golden"][n])]
    ok("K2 the heavy column read as counts misses every crossing with an older counter", set(moved) ==
       {"Common Road", "Long Drove", "Moor Road", "Church Lane"}, str(moved))
    sw = dt.date.fromisoformat(P.SWITCH_DATE)
    sites, _ = SV.netreg(target)
    flagged = sorted(s["site"] for s in sites if s["counter"] != "QT-40" and SV.share_rows(cnt, s["site"], s["installed"]))
    truth = sorted(W["site_refs"][(c, k)] for c, k in P.QT40_SWITCHED.items())
    ok("K2 the switched sites are found by their own rows", flagged == truth, "%s %s" % (flagged, truth))
    C = CE.sheet(S, target)
    ok("K3 pair ceiling at or under 60 on the cut pack", C["pair"] <= 60, "%.1f" % C["pair"])
    ok("K3 mirror leakage under 50 per cent", C["mirror_leak"] < 50, "%.1f" % C["mirror_leak"])
    ok("K3 no single finding lifts a response by over a third of the ask weight", max(C["lifts"].values()) <= 1 / 3.0 + 1e-9,
       str({k: round(v, 3) for k, v in C["lifts"].items()}))
    inmain = [x for c in P.ORDER for d in B.days() for x in W["closures"][c][d]
              if x[2] != "train" and B.day_type(d, P.CROSSINGS[c]["county"]) == "school" and x[0] < 11 * 3600 and x[1] > 6 * 3600]
    ok("Z1 no fault-held or long closure touches a school day between 06:00 and 11:00", not inmain, str(len(inmain)))
    bad = [o for o in W["orders"] if o.get("crossing") and B.in_main(o["crossing"], o["date"], o["rep"])]
    ok("Z2 no work order is reported inside the main population's window", not bad, str(len(bad)))
    bad = [o for o in W["occ"] if B.in_main(o["crossing"], o["date"], o["t"])]
    ok("Z2 no occurrence entry falls inside the main population's window", not bad, str(len(bad)))

    # ------------------------------------------------ the back-test: the survey agrees with the closure model everywhere
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, B.FILES["survey"]), read_only=True)
    sitemap = {(n, s["direction"]): s["site"] for n in names for s in S["layout"][n]["sites"]}
    diffs = collections.defaultdict(list)
    for r in wb["Queue at rise"].iter_rows(min_row=2, values_only=True):
        if not r or not r[0]:
            continue
        d = r[1].date()
        hms = lambda s: sum(int(x) * m for x, m in zip(s.split(":"), (3600, 60, 1)))
        down, up = hms(r[2]), hms(r[3])
        arr, _ = SV.arrivals(cnt[(sitemap[(r[0], r[4])], d)])
        model = sum(1 for a in arr if down <= a < up)
        diffs[r[0]].append((r[5] - model, model))
    for n in names:
        v = [x for x, _ in diffs[n]]
        size = sum(m for _, m in diffs[n]) / len(v)
        ok("T1 the survey's queues at rise agree with the counts at %s" % n, len(v) >= 20 and abs(sum(v) / len(v)) < 1.0 and
           sum(abs(x) for x in v) / len(v) < size ** 0.5 + 1.2, "n %d mean %.2f mad %.2f of %.1f" % (
               len(v), sum(v) / len(v), sum(abs(x) for x in v) / len(v), size))

    # ------------------------------------------------ realism
    with open(os.path.join(target, B.FILES["barrier"]), newline="") as fh:
        ids = [int(r[0]) for r in list(csv.reader(fh))[1:5000]]
    ok("Q1 event ids are not an arithmetic sequence", len(set(b - a for a, b in zip(ids, ids[1:]))) > 3)
    with open(os.path.join(target, B.FILES["orders"]), newline="") as fh:
        wo = [int(r[0][2:]) for r in list(csv.reader(fh))[1:]]
    ok("Q1 work order numbers are not an arithmetic sequence", len(set(b - a for a, b in zip(wo, wo[1:]))) > 3)
    refs = sorted(int(s["site"].split()[1]) for s in sites)
    ok("Q1 count site numbers are not an arithmetic sequence", len(set(b - a for a, b in zip(refs, refs[1:]))) > 3)
    tot = collections.Counter()
    for (c, k, d), (veh, _) in W["counts"].items():
        tot[(d, sum(veh))] += 1
    ok("Q2 no two sites share a day's total often", max(tot.values()) <= 3)
    texts = SV.pdf_text(os.path.join(target, B.FILES["method"])) + SV.pdf_text(os.path.join(target, B.FILES["register"]))
    ok("D1 positive control: the method reads back", "1,800 vehicles an hour" in re.sub(r"\s+", " ", texts) and
       "5.75 metres" in texts)
    ok("D1 positive control: the register reads back ten crossings", len(S["reg"]) == 10, str(len(S["reg"])))
    ok("D1 positive control: the brief's shortlist reads back", sorted(names) == sorted(P.CROSSINGS[c]["name"] for c in P.ORDER))
    for f in files:
        if f.endswith((".docx", ".xlsx")):
            with zipfile.ZipFile(os.path.join(target, f)) as z:
                app = z.read("docProps/app.xml").decode()
            ok("D3 %s saved as Office saves it" % f, ("Microsoft Excel" in app) if f.endswith(".xlsx") else
               ("Microsoft Office Word" in app))
    doc_people = set(re.findall(r"(?:Author|Lead|Manager)[:,]? ([A-Z][a-z]+ [A-Z][a-z]+)", SV.shortlist(target)[1]))
    ok("Q3 personas from the drawn list only", doc_people <= {P.LEAD, P.PM}, str(doc_people))

    # ------------------------------------------------ the goldens carry the answers
    from openpyxl import load_workbook as lw
    ws = lw(os.path.join(golden, "crossing_delay_2025_26.xlsx"), read_only=True)["Crossing delay"]
    got = {r[1]: r for r in ws.iter_rows(min_row=5, values_only=True) if r and r[1] in names}
    ok("GD1 the golden workbook carries every figure", all(got[n][4] == A["delay"][n] and "%.1f" % got[n][5] == A["closures"][n]
                                                          and "%.1f" % got[n][6] == A["fault"][n] and "%.1f" % got[n][7] ==
                                                          A["hgv"][n] for n in names))
    import docx
    dtext = "\n".join(p.text for p in docx.Document(os.path.join(golden, "crossing_choice_2027.docx")).paragraphs)
    ok("GD2 the golden paper names the call, the runner-up and the gap", "Replace Mill Lane in 2027." in dtext and
       "The runner-up is Station Road" in dtext and "{:,} vehicle-hours behind".format(A["gap"]) in dtext)
    return sum(1 for line in LOG if line.startswith("PASS"))
