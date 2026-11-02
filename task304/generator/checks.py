"""task304 architecture 5: the generator's assertions, run on the clean truth (world.py) and the cut pack (target/).
Every label starting R1, R2 or R3 is the three-rules block; SF labels are the semantic fork table's rows."""
import datetime as dt
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)

import analysis as AN  # noqa: E402
import params as P  # noqa: E402
from io_util import pdf_text, read_csv, read_xlsx  # noqa: E402
from nbfit import nb2  # noqa: E402
from world import World  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def r1(x):
    return float("%.1f" % (x + 1e-9))


def edge(x):
    """Distance from x to the nearest rounding edge of one decimal place."""
    return abs((x * 10) % 1 - 0.5) / 10


def top(d):
    s = sorted(d.items(), key=lambda kv: -kv[1])
    return s[0][0], s[0][1] / s[1][1]


def separate_fits(pk):
    """Variant: layouts fitted apart (crossroads alone; T and staggered together), each with its own slopes."""
    out = {}
    for group in (("X",), ("T", "ST")):
        rows = []
        for n in pk.reference():
            v = pk.nodes[n]
            if v["layout"] not in group:
                continue
            for y in AN.WINDOW:
                rows.append(dict(node=n, layout=v["layout"], maj=v["maj"][y], mnr=v["mnr"][y], year=y,
                                 n=pk.counts[(n, y)]))
        cols = [np.ones(len(rows))]
        if len(group) > 1:
            cols.append(np.array([r["layout"] == "ST" for r in rows], dtype=float))
        cols += [np.log([r["maj"] for r in rows]), np.log([r["mnr"] for r in rows])]
        cols += [np.array([r["year"] == y for r in rows], dtype=float) for y in AN.WINDOW[1:]]
        X = np.column_stack(cols)
        b, a, _ = nb2(X, np.array([r["n"] for r in rows], dtype=float))
        for node in pk.listed:
            v = pk.nodes[node]
            if v["layout"] not in group:
                continue

            def mu(year, level):
                c = [1.0] + ([1.0 if v["layout"] == "ST" else 0.0] if len(group) > 1 else [])
                c += [np.log(v["maj"][year]), np.log(v["mnr"][year])] + [1.0 if level == y else 0.0 for y in AN.WINDOW[1:]]
                return float(np.exp(np.array(c) @ b))
            mus = [mu(y, y) for y in AN.WINDOW]
            mu26 = np.mean([mu(AN.PRESENT, y) for y in AN.WINDOW])
            obs = sum(pk.counts[(node, y)] for y in AN.WINDOW)
            w = 1 / (1 + a * sum(mus))
            eb = (w * sum(mus) + (1 - w) * obs) / sum(mus) * mu26
            out[v["name"]] = eb * (1 - pk.cmf[v["layout"]])
    return out


def main():
    W = World()
    pk = AN.Pack(TARGET)
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    figs = pk.junction_figures()
    names = {n: figs[n]["name"] for n in figs}
    lad = pk.ladder(figs)
    gold = {r["name"]: r["benefit"] for r in figs.values()}
    best = F["call"]

    # ------------------------------------------------------------------ R1: the field's raw material ships
    head, body = read_csv(os.path.join(TARGET, "collision_records_2016_2025.csv"))
    ix = {h: i for i, h in enumerate(head)}
    check("R1.1 the validated record ships every injury collision at collision level with its junction node link "
          "(25,000 rows or more)", len(body) >= 25000 and sum(1 for r in body if r[ix["junction_node"]]) > 4000, str(len(body)))
    check("R1.2 the inventory ships every give-way or stop-controlled T, staggered and crossroads junction with its "
          "major and minor traffic by year", len(pk.reference()) >= 1400 and pk.years == list(range(2016, 2027)),
          str(len(pk.reference())))
    shipped_txt = " ".join(open(os.path.join(TARGET, f), encoding="utf-8", errors="ignore").read()[:5000].lower()
                           for f in os.listdir(TARGET) if f.endswith((".csv", ".json")))
    check("R1.3 no shipped column holds an expected, predicted or performance-function figure",
          not re.search(r"expected|predicted|spf|empirical|bayes|benefit", shipped_txt))
    scr = pdf_text(os.path.join(TARGET, "network_screening_2026.pdf"))
    check("R1.4 the screening note lists the junctions and their roads without any count",
          len(pk.listed) == 6 and not re.search(r"\b1[2-9] (injury )?collisions\b|\b2[0-9] collisions\b", scr))

    # ------------------------------------------------------------------ R2: Layer 1 mess, each neutral to the call
    pre19 = [r for r in body if r[ix["junction_node"]] and int(r[ix["collision_date"]][-4:]) < 2019]
    check("R2.1 every pre-2019 record's former node number maps to one current node, and the window uses current numbers",
          all(r[ix["junction_node"]] in pk.former for r in pre19)
          and not any(r[ix["junction_node"]].startswith("N") for r in body if int(r[ix["collision_date"]][-4:]) >= 2019))
    refs = [r[ix["accident_ref"]] for r in body]
    check("R2.2 the record's references change format in 2020 and stay unique; node counts do not depend on them",
          len(set(refs)) == len(refs) and any(x.startswith("AR/") for x in refs) and any("/47/" in x for x in refs))
    check("R2.3 every date parses as dd/mm/yyyy and every day-of-week code matches its date",
          all(((AN.d_dmy(r[ix["collision_date"]]).isoweekday() % 7) + 1) == int(r[ix["day_of_week"]]) for r in body[:4000]))
    hc, bc = read_xlsx(os.path.join(TARGET, "junction_inventory_2026.xlsx"), "Codes")
    codes = {(r[0], r[1]) for r in bc}
    check("R2.4 the inventory's codes sheet maps every layout and control code the junctions carry",
          all(("layout", v["layout"]) in codes and ("control", v["control"]) in codes for v in pk.nodes.values()))
    minor = [r for r in body if r[ix["junction_detail"]] != "0" and not r[ix["junction_node"]]]
    check("R2.5 collisions at junctions off the inventory (junction detail set, no node) exist and add nothing to any "
          "listed junction's count", len(minor) > 1000 and all(pk.counts[(n, y)] == W_count(W, n, y) for n in pk.listed for y in AN.WINDOW))
    check("R2.6 the main call reads no 2026 row: the validated record ends at 2025 and the provisional files are separate",
          max(AN.d_dmy(r[ix["collision_date"]]) for r in body) <= dt.date(2025, 12, 31))
    m_all = all_types_variant(pk)
    check("R2.7 roundabout, mini-roundabout and signal junctions in the inventory stay out of the reference group; "
          "fitting them in with their own layout terms keeps the call", top(m_all)[0] == best, str({k: round(v, 3) for k, v in m_all.items()}))

    # ------------------------------------------------------------------ R3: the analyst test, executed
    truth = {}
    for j in W.candidates():
        mu26 = W.mu(j, 2026) / P.YEAR_FACTOR[2026]
        truth[j["name"]] = mu26 * j["theta"] * (1 - P.CMF[j["layout"]])
    obs_t = {j["name"]: sum(j["n"][y] for y in P.WINDOW) / 5 * (1 - P.CMF[j["layout"]]) for j in W.candidates()}
    check("R3a the cluster-site route (each junction's 2021 to 2025 count as its expected count) files Saxby Cross on the "
          "cut pack and on the clean truth", lad["observed"][0] == "Saxby Cross" and top(obs_t)[0] == "Saxby Cross" and lad["observed"][1] >= 1.15,
          "%s %.2f" % (lad["observed"][0], lad["observed"][1]))
    check("R3a' carrying each count to 2026 traffic keeps the cluster-site route on Saxby Cross",
          lad["traffic_observed"][0] == "Saxby Cross" and lad["traffic_observed"][1] >= 1.15, "%.2f" % lad["traffic_observed"][1])
    check("R3a'' collisions per million entering vehicles also file Saxby Cross", lad["rate"][0] == "Saxby Cross")
    check("R3b the traffic model alone (each junction's predicted count, its own record ignored) files Tollgate Crossroads",
          lad["model_only"][0] == "Tollgate Crossroads" and lad["model_only"][1] >= 1.15, "%.2f" % lad["model_only"][1])
    check("R3c the golden (each junction's own record weighed against the model by empirical Bayes) files Mill Lane "
          "Crossroads by 1.2 or more", lad["golden"][0] == best == "Mill Lane Crossroads" and lad["golden"][1] >= 1.2,
          "%.3f" % lad["golden"][1])
    check("R3c' on the clean truth (each junction's true long-run rate at 2026 traffic) the largest benefit is at Mill Lane "
          "Crossroads, the junction the golden names", top(truth)[0] == best, str({k: round(v, 3) for k, v in truth.items()}))
    pos0 = [r["name"] for r in lad["observed"][2]].index(best) + 1
    pos1 = [r["name"] for r in lad["model_only"][2]].index(best) + 1
    check("R3c'' the golden junction is not first on any easy route (second on the cluster-site route, %d on the model "
          "alone)" % pos1, pos0 >= 2 and pos1 >= 2, "%d %d" % (pos0, pos1))

    # the standing family: every licensed estimate of the expected collisions
    fam = {}
    for lab, kw, lev in (("base", {}, "mean"), ("no year terms", dict(yeardum=False), "mean"), ("2025 level", {}, "last"),
                         ("moment overdispersion", dict(kmode="moments"), "mean"), ("staggered pooled with T", dict(stx=False), "mean")):
        f = pk.junction_figures(pk.spf(**kw), level=lev)
        fam[lab] = {r["name"]: r["benefit"] for r in f.values()}
    fam["layouts fitted apart"] = separate_fits(pk)
    same_call = all(top(v)[0] == best and top(v)[1] >= 1.18 for v in fam.values())
    check("R3d every licensed estimator of the filed quantity (the record weighed against a performance function with a "
          "layout term, across specifications) files Mill Lane Crossroads (margin 1.18 or more)", same_call,
          str({k: "%s %.2f" % top(v) for k, v in fam.items()}))
    bins_ok = all(len({r1(v[n]) for v in fam.values()}) == 1 for n in gold)
    check("R3e every member of the standing family prints every listed junction's benefit at the same one-decimal value",
          bins_ok, str({n: sorted({round(v[n], 3) for v in fam.values()}) for n in gold}))
    # every licensed fit of the expected collisions (analysis.Pack.FAMILY), each listed junction's benefit asserted at
    # its one-decimal value with its distance to the rounding edge
    famx = pk.family()
    edges = {lab: min(edge(d[n]["benefit"]) for n in d) for lab, d in famx.items()}
    held = all(r1(d[n]["benefit"]) == r1(gold[n]) for d in famx.values() for n in gold)
    check("R3h each of the %d licensed fits (junction-year or five-year totals, year terms or none, layouts pooled or "
          "apart, overdispersion by likelihood or moments, a stop-control term, 2026 or window traffic) prints every listed "
          "junction's benefit at the golden's one-decimal value, 0.010 or more from the rounding edge" % len(famx),
          held and min(edges.values()) >= 0.010,
          "; ".join("%s: min edge %.3f" % (lab, e) for lab, e in edges.items()))
    for n in sorted(gold):
        v = [d[n]["benefit"] for d in famx.values()]
        check("R3h' %s: %.1f under every fit (%.3f to %.3f, nearest edge %.3f)" % (n, r1(gold[n]), min(v), max(v),
              min(edge(x) for x in v)), all(r1(x) == r1(gold[n]) for x in v) and min(edge(x) for x in v) >= 0.010)
    m_tot = pk.spf(form="total")
    m_base = pk.spf()
    tot = {r["name"]: r["benefit"] for r in pk.junction_figures(m_tot).values()}
    check("R3f total entering traffic in place of major and minor fits the record worse (log-likelihood lower by more "
          "than 10) and keeps the call", m_base["ll"] - m_tot["ll"] > 10 and top(tot)[0] == best,
          "%.1f %.1f" % (m_base["ll"], m_tot["ll"]))
    m_long = pk.spf(years=list(range(2016, 2026)))
    long_ = {r["name"]: r["benefit"] for r in pk.junction_figures(m_long).values()}
    check("R3g a model fitted on 2016 to 2025 (against clause 3.3's window) keeps the call", top(long_)[0] == best)

    # ------------------------------------------------------------------ semantic fork table
    check("SF1 the listed junctions: the screening note's list equals the screening rule run on the record (12 or more "
          "in 2021 to 2025)", sorted(pk.listed) == pk.screened_by_rule())
    ksi = ksi_variant(pk)
    check("SF2 injury collisions are every severity (clause 3.2); killed or seriously injured alone would move the "
          "figures", ksi != gold)
    check("SF3 the record is the validated 2021 to 2025 window (clause 3.3); the longer record keeps the call (R3g)",
          top(long_)[0] == best)
    check("SF4 as it stands: the listed junctions are give-way or stop-controlled in the inventory today",
          all(pk.nodes[n]["control"] in ("GW", "STOP") for n in pk.listed))
    f25 = traffic_year_variant(pk, 2025)
    check("SF5 at its 2026 traffic: carrying to 2025 traffic instead keeps the call (the figures are the fund's 2026)",
          top(f25)[0] == best)
    check("SF6 the year level carried to 2026 (window average, 2025, or no year terms) prints the same figures (R3e)", bins_ok)
    near = distance_variant(pk, W)
    check("SF7 a junction's collisions are those the county's system links to its node; counting every collision within "
          "20 metres gives the same counts", near)
    check("SF8 the factor follows the inventory layout: crossroads 0.52, T and staggered 0.70 (Table 2)",
          all(figs[n]["cmf"] == {"X": 0.52, "T": 0.70, "ST": 0.70}[pk.nodes[n]["layout"]] for n in pk.listed))
    rp = all(r1(r1(figs[n]["expected"]) * (1 - figs[n]["cmf"])) == r1(figs[n]["benefit"]) for n in pk.listed)
    check("SF9 the benefit rounds the same whether taken from the rounded or the unrounded expected count", rp)
    check("SF10 the benefit is expected annual collisions times one less the factor (clause 3.2), not the factor itself",
          all(abs(figs[n]["benefit"] - figs[n]["expected"] * (1 - figs[n]["cmf"])) < 1e-12 for n in pk.listed))
    check("SF11 the reference group is the inventory's give-way and stop-controlled T, staggered and crossroads junctions; "
          "adding the other layouts with their own terms keeps the call (R2.7)", top(m_all)[0] == best)
    a_recv = pk_ask_received(pk)
    check("SF12 a collision's quarter is that of its date, not of its receipt; receipt dates would move the figures",
          a_recv != pk.ask_a())
    check("SF13 severity follows A1's 30-day definition: without the unit's notifications fatal and serious move",
          pk.ask_a(deaths="none") != pk.ask_a())
    check("SF14 roads the county is highway authority for: the register's sections by their grid references; the whole of a "
          "road with a trunk section left out would move the figures", pk.ask_a(trunk="road") != pk.ask_a())
    reg = pk.road_register()
    u = [x for x in reg if x["road"] == "U"]
    check("SF17 unclassified roads: the register's own entry gives them to the county; leaving them out moves every cell",
          len(u) == 1 and u[0]["auth"] == "Ardleshire County Council"
          and all(v != pk.ask_a()[k] for k, v in pk.ask_a(trunk="classified").items()))
    a46 = sorted((x for x in reg if x["road"] == "A4600"), key=lambda x: x["e0"])
    placed = [c for c in pk.provisional(trunk="none") if c["road"] in ("A4600", "A6510")]
    check("SF18 the A4600 handover is pinned at one grid easting on the register rows (the Brindham East node's) and every "
          "A4600 and A6510 collision falls in exactly one section",
          len(a46) == 2 and a46[0]["e1"] == a46[1]["e0"] == W.trunk_boundary
          and all(len(pk.sections_hit(c["road"], c["e"], reg)) == 1 for c in placed), str(len(placed)))
    gtxt = " ".join(pdf_text(os.path.join(TARGET, "junction_safety_fund_guidance_2027.pdf")).split())
    check("L1 clause 3.3 files the quantity: the long-run yearly average the junction would have as it stands, its recorded "
          "count part of the evidence and not the average, and names no model, comparison group or weighting",
          "long-run yearly average that junction would have as it stands" in gtxt
          and "are part of the evidence on that average and are not the average itself" in gtxt
          and not re.search(r"model|performance function|empirical|bayes|weight|comparable|similar junctions|shrink", gtxt, re.I))
    check("L2 the literal reader with the own-count input (the record, scaled to 2026 traffic or not) executes the quantity "
          "clause 3.3 excludes and files Saxby Cross; the model alone leaves out the record 3.3 makes evidence and files "
          "Tollgate Crossroads; only the record weighed against the model files Mill Lane Crossroads",
          lad["observed"][0] == lad["traffic_observed"][0] == "Saxby Cross" and lad["model_only"][0] == "Tollgate Crossroads"
          and lad["golden"][0] == best)
    check("SF15 road user groups as A2 defines them (motorcycles of any size, taxis and private hire cars with cars)",
          set(k[1] for k in pk.ask_b()) == set(AN.GROUPS))
    check("SF16 A2 counts the casualties of the A1 collisions (same scope, same quarters)",
          sum(F["ask_b"]["Q%d" % q][g] for q in (1, 2, 3) for g in AN.GROUPS) <= sum(len(c["cas"]) for c in pk.provisional()))

    # ------------------------------------------------------------------ asks: truth, devices and fairness
    ta, tb = W.prov_truth()
    ga, gb = pk.ask_a(), pk.ask_b()
    check("A0 ask A from the cut pack equals the clean truth in all nine cells", all(ga[k] == ta.get(k, 0) for k in ga))
    check("A0' ask B from the cut pack equals the clean truth in all twelve cells", all(gb[k] == tb.get(k, 0) for k in gb))
    resent = [c for c in W.prov if c.get("resent")]
    recs = pk.provisional()
    check("A1 the migration's re-sends are found one for one by date, road, time and place (no false pair)",
          len(resent) == sum(1 for c in json.load(open(os.path.join(TARGET, "police_export_2026_jun_sep.json")))["collisions"]
                             if c["occurred"][:10] < "2026-06-01"))
    cells_twin = {((c["date"].month - 1) // 3 + 1, min(k["sev"] for k in c["casualties"])) for c in resent}
    check("A2 every first- and second-quarter cell of ask A holds at least one re-sent collision",
          all((q, s) in cells_twin for q in (1, 2) for s in (1, 2, 3)))
    a46 = {((c["date"].month - 1) // 3 + 1, min(k["sev"] for k in c["casualties"])) for c in W.prov
           if c["road"] == "A4600" and not c["trunk"]}
    check("A3 every third-quarter cell of ask A holds a collision on the detrunked section of the A4600",
          all((3, s) in a46 for s in (1, 2, 3)))
    check("A4 every notification of a death within 30 days matches one collision", pk.notif_matched >= 9)
    check("A5 a response that de-duplicates on the reference (each re-send kept twice) misses every first- and "
          "second-quarter cell of ask A", all(pk.ask_a(dedupe="ref")[k] != ga[k] for k in ga if k[0] in (1, 2)))
    check("A6 the main call's files carry no ask device: the validated record and inventory hold no 2026 collision, no "
          "re-send and no fatality notification", True)

    # ------------------------------------------------------------------ input gates and realism
    files = sorted(os.listdir(TARGET))
    exts = {f.rsplit(".", 1)[1] for f in files}
    meta = json.load(open(os.path.join(TASK, "metadata.json"), encoding="utf-8")) if os.path.exists(os.path.join(TASK, "metadata.json")) else {}
    check("G1 10 or more files in 3 or more formats", len(files) >= 10 and len(exts) >= 3, "%d %s" % (len(files), sorted(exts)))
    check("G2 two or more distractors named in metadata.json, neither read by the solution",
          len(meta.get("distractor_files", [])) >= 2)
    check("G3 no file describes the data (no readme, dictionary, notes, manifest or schema)",
          not any(re.search(r"readme|dictionary|notes|manifest|schema|codebook", f) for f in files))
    yr = Counter(AN.d_dmy(r[ix["collision_date"]]).year for r in body)
    check("G4 no two years of the record carry the same number of collisions", len(set(yr.values())) == len(yr))
    nodes_sorted = sorted(int(n[1:]) for n in pk.nodes)
    steps = {b - a for a, b in zip(nodes_sorted, nodes_sorted[1:])}
    check("G5 node numbers and references do not advance in a fixed step", len(steps) > 3)
    docs_txt = pdf_text(os.path.join(TARGET, "junction_safety_fund_guidance_2027.pdf")) + scr
    check("G6 the personas in the documents are the card's (Cheryl Gregory, Alison Hartley)",
          "Cheryl Gregory" in docs_txt and "Alison Hartley" in docs_txt)
    stamps = []
    for f in files:
        if f.endswith(".pdf"):
            raw = open(os.path.join(TARGET, f), "rb").read()
            stamps.append(re.search(rb"/CreationDate \(D:(\d{14})", raw).group(1))
    check("G7 each PDF carries its own creation stamp", len(set(stamps)) == len(stamps))
    late = []
    for f in files:
        if f.endswith((".csv", ".json")):
            for m in re.finditer(r"(20\d\d)-(\d\d)-(\d\d)", open(os.path.join(TARGET, f), encoding="utf-8").read()):
                if m.group(0) > "2026-12-04":
                    late.append(m.group(0))
    check("G8 no date in the pack falls after the fiction's as-of date (4 December 2026)", not late, str(late[:3]))
    check("G9 the record's give-way junction collisions run level across 2022 to 2025 (year-on-year within 2 per cent)",
          max(sum(pk.counts[(n, y)] for n in pk.reference()) for y in range(2022, 2026)) /
          min(sum(pk.counts[(n, y)] for n in pk.reference()) for y in range(2022, 2026)) < 1.02)

    # ------------------------------------------------------------------ bin distance
    worst = min(edge(gold[n]) for n in gold)
    check("B1 every graded benefit sits at least 0.008 from its one-decimal rounding edge", worst >= 0.008,
          str({n: round(gold[n], 3) for n in gold}))
    check("B2 the call's expected annual collisions sit at least 0.01 from their rounding edge (%.3f)" % figs[[n for n in figs if names[n] == best][0]]["expected"],
          edge(figs[[n for n in figs if names[n] == best][0]]["expected"]) >= 0.01)
    check("B3 figures.json carries the benefit, call and annex figures the write-up states",
          F["call"] == best and F["benefit"] == {n: r1(v) for n, v in gold.items()} and F["ask_a"]["Q1"]["Fatal"] == ga[(1, 1)])

    fails = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [" + detail + "]") if (detail and not ok) else ""))
    print("%d checks, %d FAIL" % (len(RESULTS), len(fails)))
    sys.exit(1 if fails else 0)


def W_count(W, node, year):
    for j in W.junctions:
        if j["node"] == node:
            return j["n"][year]
    return None


def all_types_variant(pk):
    keep = pk.reference
    pk.reference = lambda: [n for n, v in pk.nodes.items() if v["layout"] in ("T", "ST", "X", "MR", "RB", "SIG")]
    old_design = pk.design

    def design(rows, form="majmin", stx=True, yeardum=True, years=AN.WINDOW):
        X = old_design(rows, form, stx, yeardum, years)
        extra = [np.array([r["layout"] == L for r in rows], dtype=float) for L in ("MR", "RB", "SIG")]
        return np.column_stack([X] + extra)
    pk.design = design
    try:
        f = pk.junction_figures(pk.spf())
    finally:
        pk.reference = keep
        pk.design = old_design
    return {r["name"]: r["benefit"] for r in f.values()}


def ksi_variant(pk):
    head, body = read_csv(os.path.join(TARGET, "collision_records_2016_2025.csv"))
    ix = {h: i for i, h in enumerate(head)}
    keep = dict(pk.counts)
    pk.counts = defaultdict(int)
    for r in body:
        node = r[ix["junction_node"]].strip()
        if node and r[ix["severity"]] in ("1", "2"):
            pk.counts[(pk.former.get(node, node), AN.d_dmy(r[ix["collision_date"]]).year)] += 1
    try:
        f = pk.junction_figures(pk.spf())
    finally:
        pk.counts = defaultdict(int, keep)
    return {r["name"]: r1(r["benefit"]) for r in f.values()}


def traffic_year_variant(pk, year):
    keep = AN.PRESENT
    AN.PRESENT = year
    try:
        f = pk.junction_figures(pk.spf())
    finally:
        AN.PRESENT = keep
    return {r["name"]: r["benefit"] for r in f.values()}


def distance_variant(pk, W):
    head, body = read_csv(os.path.join(TARGET, "collision_records_2016_2025.csv"))
    ix = {h: i for i, h in enumerate(head)}
    hi, bi = read_xlsx(os.path.join(TARGET, "junction_inventory_2026.xlsx"), "Junctions")
    jx = {h: i for i, h in enumerate(hi)}
    pos = {r[jx["node"]]: (int(r[jx["easting"]]), int(r[jx["northing"]])) for r in bi}
    ok = True
    for node in pk.listed:
        e0, n0 = pos[node]
        c = 0
        for r in body:
            y = int(r[ix["collision_date"]][-4:])
            if y in AN.WINDOW and abs(int(r[ix["easting"]]) - e0) <= 20 and abs(int(r[ix["northing"]]) - n0) <= 20:
                if np.hypot(int(r[ix["easting"]]) - e0, int(r[ix["northing"]]) - n0) <= 20:
                    c += 1
        ok &= c == sum(pk.counts[(node, y)] for y in AN.WINDOW)
    return ok


def pk_ask_received(pk):
    """Ask A by the quarter each record was received (the old system's receipt date), the wrong clock."""
    head, body = read_csv(os.path.join(TARGET, "police_collisions_2026_jan_may.csv"))
    ix = {h: i for i, h in enumerate(head)}
    recv = {r[ix["accident_ref"]]: AN.d_dmy(r[ix["date_received"]]) for r in body}
    recs = pk.provisional()
    a = {(q, s): 0 for q in (1, 2, 3) for s in (1, 2, 3)}
    for c in recs:
        d = recv.get(c["ref"], c["date"])
        q = (d.month - 1) // 3 + 1
        if q <= 3:
            a[(q, c["sev"])] += 1
    return a


if __name__ == "__main__":
    main()
