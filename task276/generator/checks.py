"""Generator assertions: input gates, the ladder, the three rules on the clean truth, every semantic fork, the asks'
devices, bins, separation, distractors, realism. Each check logs one line; any failure raises."""
import csv
import datetime as dt
import io
import math
import os
import re
import shutil
import tempfile
import zipfile

import pandas as pd

import golden as G
import pack as PK
import params as P
import solve as SV
import world as Wd

LOG = []
N = [0]


def ok(cond, label, detail=""):
    if not cond:
        raise AssertionError("%s: %s" % (label, detail))
    N[0] += 1
    LOG.append("%-34s %s" % (label, detail)[:220])


def walk(folder):
    out = []
    for root, _, files in os.walk(folder):
        for f in files:
            out.append(os.path.relpath(os.path.join(root, f), folder))
    return sorted(out)


def text_of(path):
    """every shipped format through one extractor (the verifier has its own)"""
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)
    if path.endswith(".docx"):
        z = zipfile.ZipFile(path)
        return re.sub(r"<[^>]+>", " ", z.read("word/document.xml").decode("utf-8"))
    if path.endswith(".xlsx"):
        z = zipfile.ZipFile(path)
        parts = [z.read(n).decode("utf-8") for n in z.namelist() if n.startswith("xl/") and n.endswith(".xml")]
        return re.sub(r"<[^>]+>", " ", " ".join(parts))
    return open(path, encoding="utf-8-sig").read()


def edge(v, u):
    c = round(v / u) * u
    return u / 2 - abs(v - c)


def run(T, Gd, W, S, A, fig, info):
    files = walk(T)
    # ------------------------------------------------------------------ input gates and pack hygiene
    ok(len(files) >= 10, "gate.files", "%d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "gate.formats", ",".join(sorted(fmts)))
    big = max(sum(1 for _ in open(os.path.join(T, f), encoding="utf-8-sig")) - 1 for f in files if f.endswith(".csv"))
    ok(big >= 25000, "gate.big_file", "%d rows in the largest csv" % big)
    ok(len(PK.DISTRACTORS) >= 2 and all(os.path.exists(os.path.join(T, PK.FILES[k])) for k in PK.DISTRACTORS),
       "gate.distractors", ", ".join(PK.FILES[k] for k in PK.DISTRACTORS))
    bad = [f for f in files if re.search(r"(?i)readme|dictionar|manifest|notes|codebook|field_guide|distractor|bulkhead|"
                                         r"clearance|backrest|trap|decoy", f)]
    ok(not bad, "gate.no_describing_or_signalling_names", ",".join(bad) or "none")
    texts = {f: text_of(os.path.join(T, f)) for f in files}
    ok(all(len(t) > 200 for t in texts.values()), "gate.every_file_read", "shortest %d chars" % min(len(t) for t in texts.values()))
    ok("seated in the driving posture" in texts[PK.FILES["standard"]], "control.standard_text_read", "positive control found")
    ok("torso line" in texts[PK.FILES["seat"]], "control.seat_text_read", "positive control found")
    dashes = [f for f, t in texts.items() if "\u2014" in t or "\u2013" in t]
    ok(not dashes, "realism.no_em_or_en_dash", ",".join(dashes) or "none")
    narr = [f for f, t in texts.items() if re.search(r"(?i)\bbulkhead\b.{0,80}\b(backrest|recline|seat travel|torso)|"
                                                     r"\b(backrest|recline)\b.{0,80}\bbulkhead\b|clearance", t)]
    ok(not narr, "leak.no_sentence_relating_backrest_and_bulkhead", ",".join(narr) or "none")
    # ------------------------------------------------------------------ the ladder
    fit, rg = S["fit"], S["rungs"]
    best, second, gap = S["call"]
    ok(best == "PEN-FD35" and second == "OST-FD35", "ladder.golden", "%s %d, runner-up %s %d" % (
        best, fit[best]["fail"], second, fit[second]["fail"]))
    ok(fit[second]["fail"] / fit[best]["fail"] >= 1.5, "ladder.golden_margin", "%.2fx" % (fit[second]["fail"] / fit[best]["fail"]))
    d0, d1, _ = S["default_call"]
    ok(d0 == "WRE-FD35", "ladder.default_path_R2", "%s %d" % (d0, rg["R2"][d0]["fail"]))
    order2 = sorted(rg["R2"], key=lambda k: rg["R2"][k]["fail"])
    m1 = rg["R2"][order2[1]]["fail"] / rg["R2"][order2[0]]["fail"]
    m2 = rg["R2"][order2[2]]["fail"] / rg["R2"][order2[1]]["fail"]
    ok(order2[:3] == ["WRE-FD35", "WRE-RD43", "PEN-FD35"] and m1 >= 1.15 and m2 >= 1.15, "ladder.R2_positions",
       "%s, margins %.2f and %.2f, golden third" % (order2[:3], m1, m2))
    order1 = sorted(rg["R1"], key=lambda k: rg["R1"][k]["fail"])
    ok(order1[0] == "WRE-FD35" and order1.index("PEN-FD35") == 2, "ladder.R1_travel_only", "%s, golden third" % order1[:3])
    ok(rg["R2r"] == rg["R2"], "ladder.R2r_recline_never_binds", "the recline range check moves nothing")
    r0 = S["r0"]
    z = [k for k, v in r0.items() if v == 0.0]
    ok("PEN-FD35" not in z and "WRE-FD35" in z, "ladder.R0_percentile", "zero shortfall: %s" % z)
    order_g = sorted(fit, key=lambda k: fit[k]["fail"])
    ok(order_g[-1] == "WRE-FD35" or fit["WRE-FD35"]["fail"] > fit["OST-FD35"]["fail"], "ladder.decisive_moves_wrenfold",
       "Wrenfold FD35 %d to %d" % (rg["R2"]["WRE-FD35"]["fail"], fit["WRE-FD35"]["fail"]))
    edge_win = fit["WRE-FD35"]["fail"] - rg["R2"]["WRE-FD35"]["fail"]
    adv = rg["R2"]["PEN-FD35"]["fail"] - rg["R2"]["WRE-FD35"]["fail"]
    ok(edge_win >= 1.2 * adv, "ladder.dominance", "decisive step adds %d against a carried advantage of %d" % (edge_win, adv))
    ok(rg["R1c"]["PEN-FD35"]["fail"] < min(v["fail"] for k, v in rg["R1c"].items() if k != "PEN-FD35"),
       "ladder.decisive_alone_on_R1", "travel plus the backrest names Pennick FD35")
    ok(len({v["fail"] for v in fit.values()}) == 5, "SF13.no_ties", "five distinct counts")
    # ------------------------------------------------------------------ the three rules on the clean truth
    truth = Wd.truth_fit(W)
    ok(truth == fit, "R1.raw_material_and_golden_from_clean_truth", "per-driver measurements and package geometry")
    cols = " ".join(texts[PK.FILES["measure"]].split()[:60]) + texts[PK.FILES["roster"]][:400]
    ok(not re.search(r"(?i)\bfit|fail|accommodat|h-point|hip point", cols), "R1.no_column_holds_the_deciding_quantity",
       "no fit, fail or hip point column in the roster or the measurements")
    roster = [s for s in W["staff"] if s["on_roster"]]

    def default_on_truth(which="latest"):
        t = {}
        for cab in P.CABS:
            t[cab["id"]] = sum(1 for s in roster
                               if not SV.rung(cab, Wd.assess(cab, *Wd._rec_values(s, which)), "R2"))
        return min(t, key=t.get)
    ok(default_on_truth() == "WRE-FD35", "R3a.analyst_test", "the stated-range method on the clean truth files Wrenfold FD35")
    ok(min(rg["R1c"], key=lambda k: rg["R1c"][k]["fail"]) == "PEN-FD35" and
       min(fit, key=lambda k: fit[k]["fail"]) == "PEN-FD35", "R3b.decisive_step_alone",
       "adding only the backrest placement names the golden")
    for name, var in S["variants"].items():
        ok(SV.call(var)[0] == "PEN-FD35", "R2.mess_neutral.%s" % name, "call holds, %s fails %d" % (
            SV.call(var)[0], var["PEN-FD35"]["fail"]))
    ok(S["variants"]["lb_rounded"] == fit, "SF4.imperial_factors", "rounded conversion factors move no count")
    ok(SV.call(S["variants"]["first"])[0] == best and SV.call(S["variants"]["mean"])[0] == best, "SF2.latest_measurement",
       "first and mean measurements name the same cab")
    ok(SV.call(S["variants"]["measured"])[0] == best, "SF1.population", "every measured member of staff names the same cab")
    ok(SV.call(S["variants"]["no_crosswalk"])[0] == best, "SF3.crosswalk", "dropping unmapped Vennerley numbers names the same cab")
    plants = [f for f in files if re.search(r"(?i)memo|draft|briefing|recommend", f)]
    ok(not plants, "R3c.no_plant_files", "no memo, draft or briefing ships")
    # ------------------------------------------------------------------ dead zone and the forks it closes
    dr = SV.drivers(T)
    worst = [99.0, 99.0, 99.0]
    corner_binds = True
    for d in dr:
        for cab in P.CABS:
            a = Wd.assess(cab, d["stature"], d["weight"], d["seh"])
            m = a["margins"]
            worst[0] = min(worst[0], m[0], m[1])
            worst[1] = min(worst[1], m[2], m[3])
            worst[2] = min(worst[2], m[4])
            if a["clear"]:
                # every point of the rear face below the corner is clear when the corner is
                for f in (0.25, 0.5, 0.75):
                    th = math.radians(a["th"])
                    L = Wd.inches(P.SEAT_IN["backrest_along"]) * f
                    Dd = Wd.inches(P.SEAT_IN["backrest_behind"])
                    x = a["xh"] + L * math.sin(th) + Dd * math.cos(th)
                    zz = cab["h30"] + L * math.cos(th) - Dd * math.sin(th)
                    if x > Wd.bulkhead_x(cab, zz):
                        corner_binds = False
    ok(worst[0] >= P.DEAD_ZONE_MM, "SF5.travel_limits_inclusive_or_not", "nearest hip point %.2f mm from a limit" % worst[0])
    ok(worst[1] >= P.DEAD_ZONE_DEG, "SF6.vision_at_least", "nearest sight line %.3f deg from 11 or 5" % worst[1])
    ok(worst[2] >= P.DEAD_ZONE_MM, "SF8a.corner_clear_of_the_line", "nearest corner %.2f mm from the trim face" % worst[2])
    ok(corner_binds, "SF8.corner_is_the_contact_point", "no rear-face point binds before the top rear corner")
    ok(all(P.SEAT_IN["recline_min"] <= Wd.assess(c, d["stature"], d["weight"], d["seh"])["th"] <= P.SEAT_IN["recline_max"]
           for d in dr for c in P.CABS), "SF9.recline_range_covers_every_torso_angle", "8 to 34 degrees")
    alt = {}
    for cab in P.CABS:
        n = 0
        for d in dr:
            xh, th, xe, ze, bmi = Wd.posture(d["stature"], d["weight"], d["seh"], cab["h30"])
            a = Wd.assess(cab, d["stature"], d["weight"], d["seh"])
            up, dn = Wd.sight(cab, xh + 18.0, ze)
            n += not (a["in_travel"] and a["clear"] and up >= P.VISION["up_deg"] and dn >= P.VISION["down_deg"])
        alt[cab["id"]] = n
    ok(min(alt, key=alt.get) == best, "SF7.eye_point_side", "an eye point 18 mm aft still names %s" % best)
    ok(len(dr) == len([s for s in W["staff"] if s["on_roster"]]), "SF1b.every_roster_driver_measured", "%d drivers" % len(dr))
    sexes = {r["Sex"] for r in csv.DictReader(io.StringIO(texts[PK.FILES["roster"]]))}
    ok(sexes == {"F", "M"}, "SF11.women_from_the_roster", "one sex field, two values")
    ok(texts[PK.FILES["standard"]].count("Tender HAS-F-2026-04") == 5, "SF12.shortlist_in_the_standard", "five shortlisted cabs")
    ok(all("%d mm aft of and %d mm above" % P.WRENFOLD_SGRP[ch] in texts[PK.FILES["pkg_wrenfold"]] for ch in ("FD35", "RD43"))
       and all(c["h30"] == P.WRENFOLD_SGRP[c["chassis"]][1] for c in P.CABS if c["converter"] == "Wrenfold Bodies"),
       "SF10.wrenfold_datum", "each cab's SgRP stated, its height equal to the cab's H30")
    ok("BMI" not in texts[PK.FILES["measure"]], "SF15.bmi_from_stature_and_weight", "no recorded BMI to choose between")
    pts = {}
    for key in ("pkg_pennick", "pkg_wrenfold", "pkg_ostrel"):
        txt = texts[PK.FILES[key]]
        for sec in re.split(r"\n(?=\w+ conversion on the )", txt)[1:]:
            ch = re.match(r"\w+ conversion on the (\w+)", sec).group(1)
            sg = re.search(r"SgRP located (\d+) mm aft of and (\d+) mm above", sec)
            ox, oz = (int(sg.group(1)), int(sg.group(2))) if sg else (0, 0)
            v = re.search(r"Windscreen header, lower edge of clear area \(x, z\)\s*\n([+\-\d]+), ([+\-\d]+)", sec)
            pts.setdefault(ch, set()).add((int(v.group(1)) + ox, int(v.group(2)) + oz))
    ok(all(len(v) == 1 for v in pts.values()) and len(pts) == 2, "SF14.one_set_of_chassis_points",
       "every converter's data gives the same header point per chassis: %s" % {k: sorted(v) for k, v in pts.items()})
    # ------------------------------------------------------------------ asks: truth, devices, bins
    jobs = list(csv.DictReader(open(os.path.join(T, PK.FILES["jobs"]), encoding="utf-8")))
    conv_t, chas_t = Wd.truth_fleet(W)
    F = S["fleet"]
    for c in G.CONVERTERS:
        ok(F["converters"][c]["jobs"] == conv_t[c]["jobs"], "ask.jobs_truth.%s" % c.split()[0], "%s" % F["converters"][c]["jobs"])
        ok(abs(F["converters"][c]["miles"] - conv_t[c]["miles"]) < 5, "ask.miles_truth.%s" % c.split()[0],
           "%.1f against %.1f" % (F["converters"][c]["miles"], conv_t[c]["miles"]))
    for c in G.CHASSIS:
        ok(F["chassis"][c]["days"] == chas_t[c]["vor"], "ask.vor_truth.%s" % c, "%s" % F["chassis"][c]["days"])
        ok(abs(F["chassis"][c]["vehicle_years"] * 365 - chas_t[c]["days"]) < 1e-6, "ask.vy_truth.%s" % c,
           "%.3f" % F["chassis"][c]["vehicle_years"])
    naive = SV.fleet_figures(T, join="register")
    moved = all(naive["converters"][c]["jobs"][q] != F["converters"][c]["jobs"][q] for c in G.CONVERTERS for q in range(4))
    ok(moved, "device.D7_reused_numbers_move_every_job_cell", "%s" % [naive["converters"][c]["jobs"] for c in G.CONVERTERS])
    movedv = all(naive["chassis"][c]["days"][q] != F["chassis"][c]["days"][q] for c in G.CHASSIS for q in range(4))
    ok(movedv, "device.D7_reused_numbers_move_every_day_cell", "%s" % [naive["chassis"][c]["days"] for c in G.CHASSIS])
    ok(all(abs(naive["converters"][c]["miles"] - F["converters"][c]["miles"]) >= 100 for c in G.CONVERTERS),
       "device.D7_miles", "%s" % [round(naive["converters"][c]["miles"] - F["converters"][c]["miles"]) for c in G.CONVERTERS])
    held = SV.fleet_figures(T, in_service="held")
    ok(all(round(held["chassis"][c]["vehicle_years"], 1) != round(F["chassis"][c]["vehicle_years"], 1) for c in G.CHASSIS),
       "device.D2_renumbering_date_moves_vehicle_years", "%s" % [round(held["chassis"][c]["vehicle_years"], 1) for c in G.CHASSIS])
    vs = SV.fleet_figures(T, vor="sum")
    ok(all(vs["chassis"][c]["days"][q] > F["chassis"][c]["days"][q] for c in G.CHASSIS for q in range(4)),
       "SF19.days_counted_once", "summing spells over-counts every quarter")
    both = SV.fleet_figures(T, transferred="both")
    ok(any(both["converters"][c]["jobs"] != F["converters"][c]["jobs"] for c in G.CONVERTERS), "SF17.first_raised",
       "a carried job counted twice moves a quarter")
    span = SV.fleet_figures(T, miles_how="unit_span")
    ok(any(round(span["converters"][c]["miles"], -2) != round(F["converters"][c]["miles"], -2) for c in G.CONVERTERS),
       "SF18.unit_window", "unit spans ignoring the fitted window move the miles")
    for r in A["converters"]:
        e1 = edge(r["miles_exact"], 100)
        e2 = edge(r["rate_exact"], 0.01)
        e3 = edge(sum(r["jobs"]) / r["miles"] * 1e5, 0.01)
        ok(e1 >= 10 and e2 >= 0.0015 and e3 >= 0.0015, "bin.%s" % r["converter"].split()[0],
           "miles %.1f from an edge, rate %.4f and %.4f" % (e1, e2, e3))
        ok(round(sum(r["jobs"]) / r["miles"] * 1e5, 2) == r["rate"], "SF23.rate_path.%s" % r["converter"].split()[0],
           "exact and rounded miles print one rate")
    for r in A["chassis"]:
        e1 = edge(r["vy_exact"], 0.1)
        e2 = edge(r["rate_exact"], 0.1)
        e3 = edge(sum(r["days"]) / r["vehicle_years"], 0.1)
        ok(e1 >= 0.015 and e2 >= 0.015 and e3 >= 0.015, "bin.%s" % r["chassis"],
           "vehicle-years %.4f, rate %.4f and %.4f from an edge" % (e1, e2, e3))
        ok(round(sum(r["days"]) / r["vehicle_years"], 1) == r["rate"], "SF23.rate_path.%s" % r["chassis"],
           "exact and rounded vehicle-years print one rate")
    ok(not any(v["converter"] == "Wrenfold Bodies" for v in F["_vehicles"]), "SF22.converters_with_vehicles",
       "Wrenfold has no vehicles in the 2025-26 fleet")
    kpi = texts[PK.FILES["kpi"]]
    ok("financial quarter" in kpi and "1 April to 31 March" in kpi, "SF16.financial_quarters", "the definitions file the year")
    ok("365 days in the front-line fleet" in kpi, "SF20.vehicle_year", "a vehicle-year is 365 days")
    kflat = " ".join(kpi.split())
    ok("measured from the odometer reading entered when the unit was fitted" in kflat and
       "from the date it was fitted up to the date it was removed" in kflat, "SF18.miles_from_the_entered_odometer",
       "the definitions fix a unit's miles from the odometer entered at fitting, the fitting date counted")
    first = SV.fleet_figures(T, miles_how="window_first")
    ok(all(round(first["converters"][c]["miles"], -2) != round(F["converters"][c]["miles"], -2) for c in G.CONVERTERS),
       "SF18.first_reading_baseline_moves_the_miles", "%s" % [round(first["converters"][c]["miles"] - F["converters"][c]["miles"])
                                                             for c in G.CONVERTERS])
    reg_x = pd.read_excel(os.path.join(T, PK.FILES["register"]), dtype={"Former fleet number": str})
    renum = reg_x[reg_x["Former fleet number"].notna()]
    legacy_rows = list(csv.DictReader(open(os.path.join(T, PK.FILES["legacy_jobs"]), encoding="utf-8")))
    seen_before = {r["Vehicle"] for r in legacy_rows}
    ok(set(renum["In service"].dt.date) == {P.WORKSHOP_CUTOVER} and
       len(seen_before & set(renum["Former fleet number"])) >= 0.8 * len(renum), "SF21.original_in_service_dates",
       "every renumbered vehicle shows 1 July 2025 in the register and most carry Vennerley jobs before it")
    vs_all = F["_vehicles"]
    early = 0
    for r in jobs:
        v = SV._owner(vs_all, r["fleet_no"], SV._d(r["raised"]))
        if v is not None and v["start"] is not None and SV._d(r["raised"]) < v["start"]:
            early += 1
    naive_early = 0
    for r in jobs:
        v = SV._owner(vs_all, r["fleet_no"], SV._d(r["raised"]), "register")
        if v is not None and v["start"] is not None and SV._d(r["raised"]) < v["start"]:
            naive_early += 1
    ok(early == 0 and naive_early > 0, "SF24.record_belongs_to_the_number_holder_on_its_date",
       "no job before its vehicle entered service under the dated holder; %d under the current holder" % naive_early)
    # ------------------------------------------------------------------ separation and distractors
    tmp = tempfile.mkdtemp()
    try:
        main_only = os.path.join(tmp, "main")
        shutil.copytree(T, main_only)
        for k in ("register", "disposals", "assets", "units", "odometer", "jobs", "legacy_jobs", "codemap", "kpi"):
            os.remove(os.path.join(main_only, PK.FILES[k]))
        ok(SV.fit_table(SV.drivers(main_only)) == fit, "separation.main_call_reads_no_fleet_file", "fleet files deleted")
        asks_only = os.path.join(tmp, "asks")
        shutil.copytree(T, asks_only)
        for k in ("roster", "crosswalk", "measure", "standard", "posture", "seat", "pkg_pennick", "pkg_wrenfold", "pkg_ostrel"):
            os.remove(os.path.join(asks_only, PK.FILES[k]))
        f2 = SV.fleet_figures(asks_only)
        ok(all(f2["converters"][c]["jobs"] == F["converters"][c]["jobs"] for c in G.CONVERTERS),
           "separation.asks_read_no_main_file", "driver files deleted")
        nod = os.path.join(tmp, "nod")
        shutil.copytree(T, nod)
        for k in PK.DISTRACTORS:
            os.remove(os.path.join(nod, PK.FILES[k]))
        S2 = SV.solve(nod)
        ok(S2["fit"] == fit and S2["fleet"]["chassis"]["FD35"]["days"] == F["chassis"]["FD35"]["days"],
           "distractors.deletion", "golden and asks unchanged without %s" % ", ".join(PK.DISTRACTORS))
    finally:
        shutil.rmtree(tmp)
    prices = pd.read_excel(os.path.join(T, PK.FILES["prices"]))
    cheapest = prices.loc[prices["Total per vehicle (GBP)"].idxmin()]
    ok("%s %s" % (cheapest["Converter"].split()[0], cheapest["Chassis-cab"]) != "Pennick FD35", "gateG.prices_do_not_name_the_golden",
       "cheapest is %s %s" % (cheapest["Converter"], cheapest["Chassis-cab"]))
    # ------------------------------------------------------------------ realism sweep
    def no_step(vals, label):
        nums = sorted({int(re.sub(r"\D", "", str(v)) or 0) for v in vals if re.sub(r"\D", "", str(v))})
        steps = {b - a for a, b in zip(nums, nums[1:])}
        ok(len(steps) > 3, "realism.no_arithmetic_ids.%s" % label, "%d ids, %d distinct steps" % (len(nums), len(steps)))
    roster_rows = list(csv.DictReader(io.StringIO(texts[PK.FILES["roster"]])))
    no_step([r["Staff number"] for r in roster_rows], "staff")
    meas = pd.read_excel(os.path.join(T, PK.FILES["measure"]))
    no_step(meas["Ref"], "measurement_refs")
    jobs = list(csv.DictReader(open(os.path.join(T, PK.FILES["jobs"]), encoding="utf-8")))
    no_step([r["job_no"] for r in jobs], "job_numbers")
    reg = pd.read_excel(os.path.join(T, PK.FILES["register"]))
    no_step(reg["Fleet number"], "fleet_numbers")
    hubs = [h[1] for h in P.HUBS]
    ok(hubs != sorted(hubs) and [h[0] for h in P.HUBS] != sorted(h[0] for h in P.HUBS), "realism.hub_order",
       "codes and names in the area order the service uses, not the alphabet")
    shapes = {len(h.split()) for h in hubs}
    ok(len(shapes) >= 3 and len({h[1].split()[-1] for h in P.HUBS}) >= 6, "realism.name_shapes", "%d hub name shapes" % len(shapes))
    per_hub = pd.Series([r["Hub code"] for r in roster_rows]).value_counts()
    ok(per_hub.nunique() == len(per_hub), "realism.no_identical_counts", "drivers per hub all differ")
    ok(not re.search(r"(?i)john doe|acme|company a\b|lorem", " ".join(texts.values())), "realism.no_placeholders", "none")
    people = set(re.findall("|".join(sorted(PK.PERSONAS)), " ".join(texts.values())))
    ok(people <= PK.PERSONAS, "realism.personas", ", ".join(sorted(people)) or "none named in text")

    def core(key):
        x = zipfile.ZipFile(os.path.join(T, PK.FILES[key])).read("docProps/core.xml").decode("utf-8")
        g = lambda tag: (re.search(r"<%s[^>]*>([^<]*)</%s>" % (tag, tag), x) or [None, None])[1]
        return g("dc:creator"), g("cp:lastModifiedBy"), g("dcterms:created"), g("dcterms:modified")
    eds = {k: core(k)[1] for k in ("register", "codemap", "disposals", "crosswalk", "measure")}
    ok(eds["crosswalk"] == PK.HR_EDITOR and eds["measure"] == PK.OH_EDITOR and
       eds["register"] in (PK.FLEET_EDITOR, PK.DISPOSALS_EDITOR) and eds["codemap"] in (PK.FLEET_EDITOR, PK.DISPOSALS_EDITOR) and
       len({eds["crosswalk"], eds["measure"], eds["register"]}) == 3, "realism.department_editors",
       ", ".join("%s %s" % kv for kv in sorted(eds.items())))
    dcr, dlast, dc0, dc1 = core("disposals")
    dlast_row = pd.read_excel(os.path.join(T, PK.FILES["disposals"]))["Disposed"].max().date().isoformat()
    ok(dc0[:10] > dlast_row and dc1 >= dc0 and dc1[:10] <= P.PACK_DATE.isoformat() and dcr and dlast and
       "Fleet Services" != dcr and dcr in PK.PERSONAS, "realism.disposals_dated_after_its_rows",
       "last disposal %s, created %s, modified %s, by %s / %s" % (dlast_row, dc0, dc1, dcr, dlast))
    from pypdf import PdfReader as _R
    tool = {}
    for key in ("pkg_pennick", "pkg_wrenfold", "pkg_ostrel"):
        rd = _R(os.path.join(T, PK.FILES[key]))
        fonts = {str(f.get_object()["/BaseFont"]).split("+")[-1] for pg in rd.pages
                 for f in pg["/Resources"]["/Font"].values()} - {"Helvetica"}
        tool[key] = (rd.metadata.get("/Creator"), rd.metadata.get("/Producer"), frozenset(fonts), rd.pdf_header)
        made = rd.metadata.get("/CreationDate")[2:10]
        ok("20260401" <= made <= "20260602", "realism.package_dated_before_evaluation.%s" % key, made)
    ok(len({t[0] for t in tool.values()}) == 3 and len({t[1] for t in tool.values()}) == 3 and
       len({t[2] for t in tool.values()}) == 3, "realism.package_toolchains_differ",
       "; ".join("%s: %s / %s / %s" % (k, t[0], t[1], ",".join(sorted(t[2]))) for k, t in sorted(tool.items())))
    for key in ("pkg_pennick", "pkg_wrenfold", "pkg_ostrel"):
        pages = [pg.extract_text() or "" for pg in _R(os.path.join(T, PK.FILES[key])).pages]
        note_page = [i for i, t in enumerate(pages) if "stretcher-side wall" in t]
        last_table = [i for i, t in enumerate(pages) if "Bulkhead walk-through door width" in t]
        ok(note_page and note_page[0] == last_table[-1] and all(len(t.split()) > 40 for t in pages),
           "realism.no_orphaned_note.%s" % key, "%d pages, note on page %d" % (len(pages), note_page[0] + 1 if note_page else 0))
    # document dates against their content
    jl = list(csv.DictReader(open(os.path.join(T, PK.FILES["legacy_jobs"]), encoding="utf-8")))
    last_legacy = max(dt.datetime.strptime(r["Date in"], "%d/%m/%y").date() for r in jl)
    ok(last_legacy < P.WORKSHOP_CUTOVER, "realism.legacy_extract_window", "last Vennerley job raised %s" % last_legacy)
    al = pd.read_excel(os.path.join(T, PK.FILES["assets"]))
    ok(al["In service"].max().date() <= dt.date(2025, 6, 27), "realism.asset_list_before_its_export", "%s" % al["In service"].max().date())
    ok(meas["Date measured"].max().date() <= P.PROGRAMME[1], "realism.measurements_inside_programme",
       "%s" % meas["Date measured"].max().date())
    odo_last = max(r.split(",")[1] for r in open(os.path.join(T, PK.FILES["odometer"]), encoding="utf-8").read().split("\n")[1:] if r)
    ok(odo_last <= "2026-03-31", "realism.odometer_window", odo_last)
    # containers
    for f in files:
        p = os.path.join(T, f)
        if f.endswith(".docx") or f.endswith(".xlsx"):
            z = zipfile.ZipFile(p)
            names = z.namelist()
            app = z.read("docProps/app.xml").decode("utf-8")
            ok("python-docx" not in " ".join(z.read(n).decode("utf-8", "ignore") for n in names if n.endswith(".xml"))
               and "openpyxl" not in app, "container.%s" % os.path.basename(f), "%d parts, %s" % (
                   len(names), re.search(r"<Application>([^<]+)", app).group(1)))
            if f.endswith(".docx"):
                ok("latentStyles" not in z.read("word/styles.xml").decode("utf-8"), "container.docx_lean_styles", "no latentStyles")
        if f.endswith(".pdf"):
            raw = open(p, "rb").read()
            ok(not re.search(rb"(?i)reportlab|pypdf", raw) and b"/Producer" in raw, "container.%s" % os.path.basename(f),
               "%d bytes" % len(raw))
    # H25: every shipped PDF reads the same through a lenient reader, a strict one and an independent extractor
    import logging
    import subprocess
    from pypdf import PdfReader
    warned = []

    class _Catch(logging.Handler):
        def emit(self, rec):
            warned.append(rec.getMessage())

    catch = _Catch()
    logging.getLogger("pypdf").addHandler(catch)
    flat = lambda s: re.sub(r"\s+", "", s)
    pdfs = [os.path.join(T, f) for f in files if f.endswith(".pdf")] + [os.path.join(Gd, G.PDF)]
    for p in pdfs:
        del warned[:]
        lenient = "\n".join(pg.extract_text() or "" for pg in PdfReader(p).pages)
        strict = "\n".join(pg.extract_text() or "" for pg in PdfReader(p, strict=True).pages)
        pop = subprocess.run(["pdftotext", "-q", p, "-"], capture_output=True, text=True)
        lines = [flat(x) for x in lenient.splitlines() if len(x.strip()) >= 25]
        lost = [x for x in lines if x not in flat(pop.stdout)]
        ok(not warned and flat(lenient) == flat(strict) and pop.returncode == 0 and lines and not lost,
           "container.readers.%s" % os.path.basename(p),
           "pypdf strict = lenient, poppler holds %d of %d lines, %d warnings" % (len(lines) - len(lost), len(lines),
                                                                                  len(warned)))
    logging.getLogger("pypdf").removeHandler(catch)
    return N[0]
