"""task285 generator checks: the three rules on the clean truth, the rungs, the fork table, mess neutrality,
the ask devices, the input gates and the realism sweep. Run after build.py. Exit 1 on any failure."""
import csv
import json
import os
import re
import sys
import zipfile
from collections import Counter

import world as W
import asks as A
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
RESULTS = []


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


FIG = json.load(open(os.path.join(HERE, "figures.json")))
GOLD = W.golden_set()
ENV = W.envelope_set()
ENV0 = W.envelope_set(limit=0.0)
WH = W.worst_hour()
WHS = W.set_at_hour(WH)
NAMES = [p[1] for p in W.PARISHES]
REG = A.build_register()
SV = A.build_survey(REG)

# ------------------------------------------------------------------------------- R: the three rules, executed
ok("R1 the field's raw material ships: hourly storage-area stages, surveyed carriageway levels and the network",
   all(os.path.exists(os.path.join(T, f)) for f in ("storage_area_stages_QRN25_D100CC.csv", "highways_levels_survey_2019.csv",
                                                    "highways_network_2025.geojson", "storage_areas_QRN25.geojson")))
heads = []
for f in os.listdir(T):
    if f.endswith(".csv"):
        heads += next(csv.reader(open(os.path.join(T, f), encoding="utf-8")))
ok("R1 no shipped column holds the deciding quantity (cut off, closure hours, isolation)",
   not any(re.search(r"cut.?off|isolat|closed_hours|passab|depth", h, re.I) for h in heads), heads)
ok("R3a the analyst test: the envelope route on the clean truth files the wrong parishes", ENV != GOLD, ENV)
ok("R3a the envelope route files exactly the nine parishes the stump sentence names",
   ENV == ["Hollinside", "Ravelsby Bridge", "Lunnerby", "Yarrowcote", "Hepplewick", "Burnishaw", "Wrennick", "Cottergill",
           "Highfold"], ENV)
ok("R3b the decisive step alone (the network read at every hour) files the golden", GOLD == FIG["call"]["parishes"])
ok("R3b rung 0 to rung 1 (the 0.25 m standard) alone leaves the call wrong", ENV0 != GOLD and ENV != GOLD)
ok("R3b the single worst hour alone leaves the call wrong", WHS != GOLD, (WH, WHS))
every_single_hour = {tuple(W.set_at_hour(h)) for h in W.HOURS}
ok("R3b no single hour of the event shows the golden set", tuple(GOLD) not in every_single_hour)
peaks = sorted({W.SA[s][1] for s in W.SA})
ok("R3b snapshots at every storage area's own peak hour, read separately, never show the golden set",
   all(W.set_at_hour(p) != GOLD for p in peaks))
union_peaks = sorted(set().union(*[set(W.set_at_hour(p)) for p in peaks]), key=NAMES.index)
ok("cheap routes: the union of the storage-area peak-hour snapshots is the golden family (the timing insight)",
   union_peaks == GOLD, union_peaks)
docs = V.pdf_text("flood_ready_fund_guidance_2027.pdf") + V.pdf_text("quarnell_flood_model_report_2025.pdf")
sent = [x for x in re.split(r"(?<=[.])\s", docs.replace("\n", " ")) if "cut off" in x]
ok("R3c no plant: no shipped sentence names a parish as cut off, and no memo, draft or ranking ships",
   not any(n in x for x in sent for n in NAMES), sent)

# ------------------------------------------------------------------------------- rungs, separation, robustness
ok("rung sets are pairwise different", len({tuple(ENV0), tuple(ENV), tuple(WHS), tuple(GOLD)}) == 4)
ok("the golden is a strict subset of the envelope", set(GOLD) < set(ENV))
ok("the envelope adds Yarrowcote, Hepplewick and Highfold", sorted(set(ENV) - set(GOLD)) == sorted(["Hepplewick", "Yarrowcote", "Highfold"]))
hrs = W.cut_off_hours()
ok("early group cut off only before hour 25", all(max(hrs[n]) <= 24 for n in ("Hollinside", "Ravelsby Bridge", "Lunnerby")))
ok("late group cut off only after hour 38", all(min(hrs[n]) >= 39 for n in ("Burnishaw", "Wrennick", "Cottergill")))
ok("SF1 every golden parish is cut off for at least 8 consecutive hours, so no minimum duration up to 8 hours moves the call",
   all(len(hrs[n]) >= 8 and max(hrs[n]) - min(hrs[n]) + 1 == len(hrs[n]) for n in GOLD),
   {n: len(hrs[n]) for n in GOLD})
# closest call for the alternating parishes: the fewest hours between one route closing and the other opening
gap = min(min(x for x in W.HOURS if W.link_impassable(l, x)) for l in W.LINKS if l[5] in ("SA-LD1", "SA-LD3", "SA-LD5", "SA-LD7") and l[6] > 0) - \
    max(max(x for x in W.HOURS if W.link_impassable(l, x)) for l in W.LINKS if l[5] in ("SA-HB1", "SA-SB1", "SA-MW1") and l[6] > 0)
ok("the becks' closures end at least six hours before the Quarnell's first closure begins", gap >= 6, gap)
for lim in (0.20, 0.30):
    ok("golden unchanged at a %.2f m standard (convergence)" % lim,
       sorted(W.cut_off_hours(limit=lim).keys(), key=NAMES.index) == GOLD)
ok("SF2 the superseded 2023 run files the same golden set", W.golden_set(2023) == GOLD)
ok("SF2 the superseded 2023 run files the same envelope", W.envelope_set(run=2023) == ENV)
# SF3: a link closes where any point exceeds the standard; its mean depth never does on these dips
st_v, polys_v, net_v, pts_v, hosp_v, annex_v = V.load()
mean_cut = set()
for h in W.HOURS:
    closed = set()
    for lid, ps in pts_v.items():
        ds = [st_v[sa][h] - lev for sa, lev in ps if sa]
        if ds and sum(ds) / len(ds) > 0.25:
            closed.add(lid)
    rr = V.reach(net_v, closed, hosp_v)
    mean_cut |= {p for p, n in annex_v.items() if n not in rr}
ok("SF3 the link-mean reading (a link closes only when its points average over 0.25 m) files another set, ruled out by 'where floodwater stands deeper than 0.25 m'",
   sorted(mean_cut) != sorted(GOLD), sorted(mean_cut))
# SF4: strict against non-strict at the hourly stages
near = [(l[0], l[1], h) for l in W.LINKS if l[5] for h in W.HOURS
        if abs(W.stage(l[5], h) - W.link_peak_level(l) - W.DEPTH_LIMIT) < 0.0005]
ok("SF4 no surveyed point stands within 0.5 mm of the 0.25 m standard at any hour", not near, near)
# SF5: public highways against classified roads only
classified = [l for l in W.LINKS if l[4] in "ABC"]
r = W.reach([l for l in classified])
ok("SF5 a classified-roads-only network strands parishes that only unclassified roads serve (ruled out by section 2)",
   any(p[2] not in r for p in W.PARISHES if p[1] not in GOLD))
# SF8: interpolation between model hours
qcut = set()
for q in range(0, 481):
    hq = q / 4.0
    rr = W.reach([l for l in W.LINKS if not (l[5] and W.stage(l[5], hq) - W.link_peak_level(l) > W.DEPTH_LIMIT)])
    qcut |= {p[1] for p in W.PARISHES if p[2] not in rr}
ok("SF8 reading the stages at 15-minute steps files the same golden set", sorted(qcut, key=NAMES.index) == GOLD, sorted(qcut))
ok("SF9 households are the council tax valuation list's dwellings, not the address register's",
   W.dwellings(GOLD) == FIG["call"]["households_total"] == 2093)
ok("SF10 Hawkesbridge West merger cannot move the call (Hawkesbridge North is never cut off)", "Hawkesbridge North" not in GOLD)
# SF11: survey points on split 2019 links assigned to either half
ok("SF11 both halves of each split 2019 link sit in one storage area and close together",
   all(W.LINKS[i][5] == W.LINKS[j][5] for i, j in [(6, 7), (15, 16)] if W.LINKS[i][5] or W.LINKS[j][5]))
ok("SF1 the envelope describes no moment: no hour has every envelope closure in force at once",
   all(not all(W.link_impassable(l, h) for l in W.LINKS if l[5] and l[6] > 0) for h in W.HOURS))
gtxt = V.pdf_text("flood_ready_fund_guidance_2027.pdf")
ok("SF6 the hospital's network node is filed once in the guidance and is in the network", gtxt.count(hosp_v) == 1 and any(hosp_v in ab for ab in net_v.values()))
ok("SF7 every parish's main village access node is filed once in Annex A and is a node of the 2025 network",
   sorted(annex_v) == sorted(NAMES) and all(any(n in ab for ab in net_v.values()) for n in annex_v.values())
   and all(gtxt.count(n) == 1 for n in annex_v.values()), sorted(annex_v))
ok("SF12 households are counts: no rounding path", all(isinstance(FIG["households"][n], int) for n in GOLD))
g_exact = {n: W.BASE_GRANT + (W.BUDGET - W.BASE_GRANT * len(GOLD)) * FIG["households"][n] / FIG["call"]["households_total"]
           for n in GOLD}
ok("SF13 the grants, each rounded once from its exact share as section 3 files it, add to the GBP 30,000 budget",
   sum(FIG["grant_amounts"].values()) == W.BUDGET and all(FIG["grant_amounts"][n] == int(round(g_exact[n])) for n in GOLD),
   FIG["grant_amounts"])
ok("SF13 no exact grant sits on a half pound", min(abs(v - int(v) - 0.5) for v in g_exact.values()) >= 0.05,
   {n: round(v, 2) for n, v in g_exact.items()})
ok("the default path's nine parishes move every grant", all(FIG["default_path_grants"].get(n) != FIG["grant_amounts"][n]
                                                           for n in GOLD))

# ------------------------------------------------------------------------------- the verifier on the bundle
gold_v, env_v, env0_v, wh_v, hours_v = V.main_call()
ok("verifier on the bundle: golden", gold_v == sorted(GOLD))
ok("verifier on the bundle: envelope", env_v == sorted(ENV))
ok("verifier on the bundle: worst hour", wh_v[1] == sorted(WHS))

# ------------------------------------------------------------------------------- shock: not an interval of a statistic
stats = {}
for code, name, node, dw in W.PARISHES:
    x, y = W.NODES[node]
    flooded_near = sum(1 for l in W.LINKS if l[5] and l[6] > 0 and min(W.km(l[0], node) if hasattr(W, "km") else
                       ((W.NODES[l[0]][0] - x) ** 2 + (W.NODES[l[0]][1] - y) ** 2) ** 0.5, 99) < 2.5)
    stats[name] = {"households": dw, "y": y, "x": x, "flooded_links_near": flooded_near,
                   "dwellings_reached": FIG["ask1_dwellings_reached"][name]}
for key in ("households", "y", "x", "flooded_links_near", "dwellings_reached"):
    for rev in (False, True):
        top = sorted(NAMES, key=lambda n: (stats[n][key], n), reverse=rev)[:len(GOLD)]
        ok("shock: the golden set is not the top %d by %s%s" % (len(GOLD), key, " (descending)" if rev else ""),
           sorted(top) != sorted(GOLD))

# ------------------------------------------------------------------------------- asks: devices move their figures
a1 = A.ask1_golden(REG, SV)
# device P1: the 2008 survey's datum read as Ordnance Datum
def a1_variant(datum_fix=True, flats_ground_only=True, use_survey=True):
    floor = {s["uprn"]: s["floor"] for s in SV} if use_survey else {}
    units = {s["uprn"]: set(u.strip().upper() for u in s["units"].split(",") if u.strip()) for s in SV if s["units"]}
    out = Counter()
    for r_ in REG:
        if not r_["t_dwelling"] or r_["t_sa"] is None:
            continue
        pk = W.peak_stage(r_["t_sa"])
        if r_["cls"] == "RD06":
            if flats_ground_only and r_["sao"].upper() not in units.get(r_["block"], set()):
                continue
            fl = floor.get(r_["block"], r_["ground_rec"] + (W.DATUM_SHIFT if datum_fix and r_["src"] == "SURV08" else 0) + 0.15)
        else:
            g = r_["ground_rec"] + (W.DATUM_SHIFT if datum_fix and r_["src"] == "SURV08" else 0)
            fl = floor.get(r_["uprn"], g + W.DEFAULT_THRESHOLD)
        if pk > fl:
            out[r_["parish"]] += 1
    return out


v_datum = a1_variant(datum_fix=False)
v_flats = a1_variant(flats_ground_only=False)
moved_d = [n for n in NAMES if v_datum.get(n, 0) != a1.get(n, 0)]
moved_f = [n for n in NAMES if v_flats.get(n, 0) != a1.get(n, 0)]
ok("ask 1 device P1 (register levels on the navigation datum read as Ordnance Datum) moves most parishes",
   len(moved_d) >= 10, moved_d)
ok("ask 1 hazard (each block's survey level applied to every flat in it) moves its parishes", len(moved_f) >= 5, moved_f)
ok("ask 1 golden reproduces through the clean variant", dict(a1_variant()) == {k: v for k, v in a1.items() if v})
shift, low, spread = V.datum_shift()
ok("ask 1 the shipped records separate the navigation-datum source: SURV08 alone sits about 0.42 m below the "
   "surveyors' ground levels at the same UPRNs, every other source within 0.08 m of them",
   low == {"SURV08"} and spread["SURV08"][0] >= 50 and abs(spread["SURV08"][1] + 0.42) <= 0.02
   and -0.50 <= spread["SURV08"][2] and spread["SURV08"][3] <= -0.34
   and all(-0.08 <= v[2] and v[3] <= 0.08 for k, v in spread.items() if k != "SURV08"), spread)
ok("ask 1 no shipped document names the source that is on the navigation datum (found only from the records)",
   not re.search(r"SURV08|2008|riverside survey", docs))
blocks_in_sa = [r_ for r_ in REG if r_["cls"] == "PP" and r_["t_sa"]]
ok("ask 1 every building of flats in the floodplain was surveyed in 2022, so its ground floor is on record",
   all(any(s["uprn"] == b["uprn"] and s["units"] for s in SV) for b in blocks_in_sa), len(blocks_in_sa))
near = []
fl_of = {s["uprn"]: s["floor"] for s in SV}
for r_ in REG:
    if r_["t_dwelling"] and r_["t_sa"]:
        f = fl_of.get(r_["block"] if r_["cls"] == "RD06" else r_["uprn"], r_["ground"] + W.DEFAULT_THRESHOLD)
        near.append(abs(W.peak_stage(r_["t_sa"]) - f))
ok("ask 1 no dwelling's threshold sits within 5 mm of its storage area's peak stage", min(near) >= 0.005, min(near))
zeros1 = sum(1 for v in FIG["ask1_dwellings_reached"].values() if v == 0)
ok("ask 1 blind response: the all-nil sheet keeps no more than a quarter of the parishes", zeros1 <= len(NAMES) / 4, zeros1)

a2 = A.ask2_golden()
edge2 = {k: 0.5 - abs(v - round(v)) for k, v in a2.items()}
ok("ask 2 every figure at least 0.2 h from its rounding edge", min(edge2.values()) >= 0.2, edge2)
import ceiling as CL
g2 = FIG["ask2_closure_hours"]
r_ref = CL.ask2(True, True, True)
r_blank = CL.ask2(False, True, False)
r_span = CL.ask2_span()
moved_ref = [k for k in g2 if r_ref.get(k) != g2[k]]
ok("ask 2 device P1 (closures keyed by the reference a row carries, the route closure under its own) moves every site",
   len(moved_ref) == len(g2), moved_ref)
ok("ask 2 the police closure handed to highways moves its site when left out",
   [k for k in g2 if r_blank.get(k) != g2[k]] == ["HW21-07-08"])
police_secs = sorted(sid for sid, road, loc, bars, pol in A.SECTIONS if pol)
r_local = CL.ask2(False, True, True, utc_convert=False)
ok("ask 2 hazard: the police clock read as BST moves every site the police closed",
   len(police_secs) >= 5 and all(r_local[s] != g2[s] for s in police_secs), (police_secs, r_local))
moved_span = sorted(k for k in g2 if r_span.get(k) != g2[k])
ok("ask 2 'hours in all' is the union in force: first closing to last reopening moves the sites with a gap "
   "(Nettlecote, Highfold, Yarrowcote)", moved_span == ["HW21-07-05", "HW21-07-07", "HW21-07-09"], (moved_span, r_span))
ok("ask 2 blind response: no single value holds more than a quarter of the sites",
   max(Counter(g2.values()).values()) <= len(g2) / 4, Counter(g2.values()))
hw = list(csv.DictReader(open(os.path.join(T, "highways_road_closures_jul2021.csv"), encoding="utf-8")))
pol = list(csv.DictReader(open(os.path.join(T, "police_road_closures_jul2021.csv"), encoding="utf-8")))
sites = {(s[1], s[2].split(",")[-1].strip()) for s in A.SECTIONS}
ok("ask 2 the duty log's clock is in its own header (closed_bst, reopened_bst) and the police log's in its own "
   "(closed_utc, opened_utc)", "closed_bst" in hw[0] and "reopened_bst" in hw[0] and "closed_utc" in pol[0])
for r in hw:
    site = (r["road_number"], r["location"].split(",")[-1].strip())
    ok("ask 2 closure %s at %s is entered against one of the log's nine closure sites" % (r["closure_ref"], r["location"]),
       site in sites, site)
route = [r for r in hw if r["barrier_position"].startswith("route closure")]
ok("ask 2 the B5131 route closure is entered once at each closure site it covered, the three B5131 sites, and nowhere "
   "else", sorted(r["location"] for r in route) == sorted(s[2] for s in A.SECTIONS if s[0] in A.ROUTE[4])
   and len({(r["closed_bst"], r["reopened_bst"], r["closure_ref"]) for r in route}) == 1, [r["location"] for r in route])
for r in pol:
    road, place = r["location_text"].split(" ", 1)
    ok("ask 2 police incident %s is at one of the log's closure sites" % r["incident"], (road, place) in sites)
gtxt2 = V.pdf_text("flood_ready_fund_guidance_2027.pdf").replace("\n", " ")
ok("ask 2 nothing in the guidance or the model report speaks of a closure site, a route closure or a diversion",
   not re.search(r"closure site|route closure|diversion", gtxt2 + V.pdf_text("quarnell_flood_model_report_2025.pdf")))

a3 = A.ask3_golden()
r3_ref = CL.ask3(True, "reference")
r3_pay = CL.ask3(True, "payee")
r3_nocan = CL.ask3(False, "award")
ok("ask 3 device P1 (cancelled cheques in the bank's advice only) moves Lunnerby and Yarrowcote",
   sorted(k for k in a3 if r3_nocan[k] != a3[k]) == sorted(["Yarrowcote", "Lunnerby"]))
ok("ask 3 device P2 (instalments under a closed 2025 reference) moves three parishes when keyed by reference",
   sorted(k for k in a3 if r3_ref[k] != a3[k]) == sorted(["Tolmarsh", "Whinnerby", "Cottergill"]))
ok("ask 3 device P2 (instalments to another payee under the 2026 reference) moves three parishes when keyed by payee",
   sorted(k for k in a3 if r3_pay[k] != a3[k]) == sorted(["Hollinside", "Burnishaw", "Upper Quarnell"]))
from openpyxl import load_workbook
bf = load_workbook(os.path.join(T, "flood_ready_ledger_2026.xlsx"), read_only=True)["2025 awards b-f"]
bfr = {r[0]: r for r in bf.iter_rows(min_row=2, values_only=True)}
ok("ask 3 every 2025 reference an instalment carries is a 2025 award closed at a zero balance before the payment",
   all(bfr[ref][4] == 0 and "closed" in bfr[ref][5] for ref in A.MISREF.values()))
rem_ok = True
for parish, ref, amt, var, pays in A.AWARDS_2026:
    total = amt + (var[0] if var else 0)
    if parish in A.MISREF or parish in A.PAYEE:
        rem_ok &= pays[1][2] <= total - pays[0][2]
ok("ask 3 every re-keyed or re-addressed instalment fits inside its 2026 award's remaining balance", rem_ok)
ok("ask 3 the payment posted after 31 October moves Wrennick when counted",
   a3["Wrennick"] == 460 and any(p[0] > "2026-10-31" for p in dict((x[0], x[4]) for x in A.AWARDS_2026)["Wrennick"]))
ok("ask 3 blind response: no parish's unpaid figure is nil", all(v != 0 for v in a3.values()), a3)
rule = ("The Fund pays an award to the parish council or, at the parish council's written request, to its clerk or to "
        "a village body it names.")
ok("ask 3 the guidance files the Fund's general payment rule once", " ".join(gtxt2.split()).count(rule) == 1)
ok("ask 3 the golden is the rule's literal reading: every instalment to another payee goes to a clerk or a village body "
   "and carries its parish's 2026 award reference, and the golden counts it as paid",
   all(("Clerk to" in p or "Village" in p) for p in A.PAYEE.values())
   and all(a3[k] != r3_pay[k] for k in A.PAYEE) and all(a3[k] == r3_ref[k] for k in A.PAYEE))
ok("ask 3 no ledger row carries a remark on who asked for a payment (the ledger has no remark column)",
   [c.value for c in next(load_workbook(os.path.join(T, "flood_ready_ledger_2026.xlsx"), read_only=True)["Transactions"].iter_rows(max_row=1))]
   == ["Posted", "Type", "Reference", "Payee", "Method", "Cheque no", "Amount GBP"])

# ------------------------------------------------------------------------------- separation line
main_files = {"storage_area_stages_QRN25_D100CC.csv", "highways_levels_survey_2019.csv", "highways_network_2025.geojson",
              "storage_areas_QRN25.geojson", "link_reference_crosswalk_2019_2025.csv",
              "council_tax_dwellings_by_parish_oct2026.csv", "flood_ready_fund_guidance_2027.pdf"}
ask_files = {"address_register_extract_oct2026.csv", "pfr_property_survey_2022.xlsx", "highways_road_closures_jul2021.csv",
             "police_road_closures_jul2021.csv", "flood_ready_ledger_2026.xlsx", "bank_cancelled_cheques_2026.csv"}
ok("separation: no ask device file is a main-call file", not (main_files & ask_files))

# ------------------------------------------------------------------------------- input gates and hygiene
files = sorted(os.listdir(T))
ok("input gate: 10 or more files", len(files) >= 10, len(files))
ok("input gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
big = max(sum(1 for _ in open(os.path.join(T, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv"))
ok("input gate: a file of 25,000 rows or more", big >= 25000, big)
meta = json.load(open(os.path.join(TASK, "metadata.json")))
ok("input gate: two or more distractors declared", len(meta["distractor_files"]) >= 2)
ok("distractors are never read by the verifier",
   not any(d.split("/")[-1] in open(os.path.join(HERE, "verify.py")).read() for d in meta["distractor_files"]))
ok("no readme, dictionary, notes or manifest file", not any(re.search(r"readme|dictionar|notes|manifest|schema", f, re.I) for f in files))
ok("no file name broadcasts the stump", not any(re.search(r"isolat|cut.?off|envelope|hour", f, re.I) for f in files))
for f in files:
    if f.endswith(".xlsx"):
        z = zipfile.ZipFile(os.path.join(T, f))
        core = z.read("docProps/core.xml").decode()
        ok("xlsx %s modified date is the export date" % f, "2026-11-02T09:12:00Z" in core)
# realism: id columns not arithmetic sequences
ids = [int(r["UPRN"]) for r in csv.DictReader(open(os.path.join(T, "address_register_extract_oct2026.csv"), encoding="utf-8"))]
ids.sort()
steps = Counter(b - a for a, b in zip(ids, ids[1:]))
ok("realism: UPRNs do not step by one constant", len(steps) > 5, steps.most_common(3))
ok("realism: council tax totals are not round", sum(1 for p in W.PARISHES if p[3] % 10 == 0) <= 2)
ok("realism: the PDFs open and carry their filed sentences (positive control)",
   "cut off when it has no road route to the hospital" in V.pdf_text("flood_ready_fund_guidance_2027.pdf").replace("\n", " ")
   and "0.42 m below Ordnance Datum Newlyn" in V.pdf_text("quarnell_flood_model_report_2025.pdf").replace("\n", " "))
ok("figures.json carries the call", FIG["call"]["count"] == 6)

# ------------------------------------------------------------------------------- house fixes
def _ed(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


ref_places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt"), encoding="utf-8")
              if x.strip() and not x.startswith("#")]
invented = sorted({w for n in NAMES for w in n.split() if w not in ("Bridge", "Moor", "Upper", "North", "South")}
                  | {"Quarnell", "Hawkesbridge"})
near = [(n, p) for n in invented for p in ref_places if p not in ("bridge", "ridge")
        and (_ed(n.lower(), p) <= 2 or (len(p) >= 5 and (p in n.lower() or n.lower() in p)))]
ok("H21 every invented place word is three or more edits from every reference place", not near, near[:6])
late = []
for f in files:
    if f.endswith((".csv", ".geojson")):
        for m in re.finditer(r"(20\d\d)-(\d\d)-(\d\d)", open(os.path.join(T, f), encoding="utf-8").read()):
            if m.group(0) > "2026-11-02":
                late.append((f, m.group(0)))
ok("H16 no date in the data files after the 2 November 2026 export", not late, late[:3])
led = open(os.path.join(T, "flood_ready_ledger_2026.xlsx"), "rb").read()
sigs = [f for f in files if f.endswith((".pdf", ".xlsx")) and re.search(rb"reportlab|openpyxl",
        open(os.path.join(T, f), "rb").read() if f.endswith(".pdf") else
        b"".join(zipfile.ZipFile(os.path.join(T, f)).read(n) for n in zipfile.ZipFile(os.path.join(T, f)).namelist()
                 if n.startswith("docProps/")), re.I)]
ok("H1 no writer signature in any shipped PDF or workbook", not sigs, sigs)
from pypdf import PdfReader
for f, who in (("flood_ready_fund_guidance_2027.pdf", "Gareth Johnston"), ("quarnell_flood_model_report_2025.pdf", "Eleanor Rose")):
    md = PdfReader(os.path.join(T, f)).metadata
    ok("realism: %s names its author (%s), no creator or producer, and a creation time with real seconds" % (f, who),
       md.get("/Author") == who and not md.get("/Creator") and not md.get("/Producer")
       and md.get("/CreationDate", "")[14:16] not in ("", "00"), dict(md))
mtxt = " ".join(V.pdf_text("quarnell_flood_model_report_2025.pdf").split())
gtxt3 = " ".join(V.pdf_text("flood_ready_fund_guidance_2027.pdf").split())
ok("leak: the model report says nothing of one storage area peaking or draining against another, of routes or of "
   "isolation", not re.search(r"\broutes?\b|isolat|cut off|\bdrain|\blags?\b|earlier than|later than|"
                              r"peaks? (?:before|after)|time to peak|\baccess", mtxt, re.I), mtxt[:200])
ok("leak: the guidance names no hour, time step or moment of the flood", not re.search(r"\bhour|\bmoment|time step|at any time",
                                                                                     gtxt3, re.I))
ok("realism: the guidance carries the trustees' approval block with names from the card",
   all(n in gtxt3 for n in ("Kirsty Grant", "Mitchell Metcalfe", "Approved for the trustees")))
zpath = os.path.join(TASK, "target.zip")
zfresh = os.path.exists(zpath) and sorted(zipfile.ZipFile(zpath).namelist()) == sorted("target/" + f for f in files) and all(
    zipfile.ZipFile(zpath).read("target/" + f) == open(os.path.join(T, f), "rb").read() for f in files)
ok("H7 target.zip holds exactly target/, byte for byte", zfresh)


def main():
    bad = [r for r in RESULTS if not r[1]]
    for label, good, detail in RESULTS:
        if not good:
            print("FAIL", label, str(detail)[:300])
    print("checks: %d assertions, %d failed" % (len(RESULTS), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
