"""task470 checks: the three rules executed on the clean truth (R1 to R3c), the ladder and its margins, the golden
family, the semantic fork table (SF1 to SF14), the Layer 1 items' neutrality, the separation of the ask's device from
the call, the towered fields' ask and its stops, every graded figure's distance to its bin edge, the input gates and
distractors, the realism sweeps and the deliverables' agreement with figures.json."""
import csv
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

import numpy as np

import bundle as B
import methods as M
import world as W

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))
    print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  [%s]" % detail) if (detail != "" and not ok) else ""))
    return ok


def pdf_text(path):
    out = subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True, check=True).stdout
    return re.sub(r"\s+", " ", out)


def xlsx_text(path):
    with zipfile.ZipFile(path) as z:
        return " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml"))


def edge(v, unit):
    return unit / 2.0 - abs(v - round(v / unit) * unit)


# ---------------------------------------------------------------------------------------------- the clean truth
def truth(x):
    """The world before any file is written: per field, the piston airplane operations and lead the network could
    hear, the operations of the based piston airplanes that never broadcast, and the based counts."""
    ac = x["aircraft"]
    H, h, miss, miss_open = {}, {}, {}, {}
    for aid, lid, t, kind, itin in x["ops"]:
        if t.year != 2026:
            continue
        a = ac[aid]
        if not a["piston_airplane"]:
            continue
        n = 2 if kind == "touch_and_go" else 1
        if a["broadcasts"]:
            g = W.LEAD[(a["cls"], kind)] * (2 if kind == "touch_and_go" else 1)
            H[lid] = H.get(lid, 0.0) + g
            h[lid] = h.get(lid, 0) + n
        else:
            miss[lid] = miss.get(lid, 0) + n
            if lid not in W.TOWERED or W.tower_open(lid, t):
                miss_open[lid] = miss_open.get(lid, 0) + n
    nd = {f["lid"]: sum(1 for a in ac if a["home"] == f["lid"] and a["piston_airplane"] and not a["broadcasts"])
          for f in W.F}
    return dict(H=H, h=h, miss=miss, miss_open=miss_open, nd=nd)


def truth_rungs(T):
    C = W.COUNTED
    r = sum(T["h"][l] for l in C) / sum(T["h"][l] + T["miss"].get(l, 0) for l in C)
    k = sum(T["miss"].get(l, 0) for l in C) / sum(T["nd"][l] for l in C)
    sch = [l for l in C if W.BY_LID[l]["school"]]
    oth = [l for l in C if not W.BY_LID[l]["school"]]
    rs = sum(T["h"][l] for l in sch) / sum(T["h"][l] + T["miss"].get(l, 0) for l in sch)
    ro = sum(T["h"][l] for l in oth) / sum(T["h"][l] + T["miss"].get(l, 0) for l in oth)
    U = W.LEAD_UNRECORDED
    out = {}
    for name, fn in (("easy: one capture rate", lambda l: T["h"][l] * (1 - r) / r),
                     ("capture by flight training", lambda l: T["h"][l] * (1 - (rs if W.BY_LID[l]["school"] else ro))
                      / (rs if W.BY_LID[l]["school"] else ro)),
                     ("decisive step alone: per never-heard airplane", lambda l: k * T["nd"][l]),
                     ("the year's actual lead", lambda l: T["miss"].get(l, 0))):
        lead = {}
        for l in W.UNTOWERED:
            u = T["miss"].get(l, 0) if l in W.STUDIED else fn(l)
            lead[l] = (T["H"][l] + u * U) / 1000.0
        out[name] = B.qualifying(lead)
    return out, dict(r=r, k=k)


# ---------------------------------------------------------------------------------------------- the run
def run(target, golden, x=None, meta_path=None, fig_path=None):
    del RESULTS[:]
    G = B.Pack(target)
    gi = G.inventory()
    cache = G.cache()
    gold = B.qualifying(gi["lead"])
    lead, ops = gi["lead"], gi["ops"]
    gk = {l: round(lead[l]) for l in B.FIELDS}
    go = {l: round(ops[l] / 100.0) for l in W.TOWERED}
    TH = W.THRESHOLD_KG
    F = json.load(open(fig_path)) if fig_path else None
    GOLD = ["A71", "F37", "L08", "O16", "T13", "U44", "W33"]
    R0SET = ["A71", "F37", "K58", "L08", "P05", "S27", "T13", "T61"]

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    with open(os.path.join(target, W.FILES["events"]), encoding="utf-8") as fh:
        n_events = sum(1 for _ in fh) - 1
    check("gates: %d files (10 or more), formats %s (3 or more), the export %d rows (25,000 or more)" % (
        len(files), sorted(fmts), n_events), len(files) >= 10 and len(fmts) >= 3 and n_events >= 25000)
    check("gates: the pack is exactly the files world.FILES declares", set(files) == set(W.FILES.values()),
          sorted(set(files) ^ set(W.FILES.values())))

    # ------------------------------------------------------------------ the call
    check("call: the golden qualifies %s" % " ".join(GOLD), gold == GOLD, gold)
    check("call: %d of the 24 fields without a tower" % len(gold), len(gold) == 7 and len(W.UNTOWERED) == 24)
    near = min(abs(lead[l] - TH) / TH for l in W.UNTOWERED)
    check("call: every field's lead at least 10 per cent from the %.1f kg line (closest %.1f per cent)" % (TH, 100 * near),
          near >= 0.10)

    # ------------------------------------------------------------------ R1 to R3: the three rules
    check("R1 the field's raw material ships: the network's event rows, the register's four files, the towers' daily "
          "counts, the four count studies and the based aircraft validation, and no shipped column holds a field's "
          "lead, a recorded share or an airplane's ADS-B equipage",
          n_events > 150000 and not any(re.search(r"lead_|_lead|equip|adsb_out|recorded_share|capture",
                                                  open(os.path.join(target, W.FILES[k]), encoding="utf-8")
                                                  .readline(), re.I)
                                        for k in ("events", "master", "dereg", "acftref", "engine", "atct", "pbmon")))
    if x is not None:
        T = truth(x)
        tr, tp = truth_rungs(T)
        check("R3a analyst test on the clean truth: one capture rate (%.3f) from the counted fields, every filed rule "
              "applied, qualifies %s (the default path's Ends on)" % (tp["r"], " ".join(R0SET)),
              tr["easy: one capture rate"] == R0SET, tr["easy: one capture rate"])
        check("R3b the decisive step alone on the clean truth (%.1f unrecorded operations per never-broadcasting based "
              "airplane at the counted fields) qualifies the golden seven" % tp["k"],
              tr["decisive step alone: per never-heard airplane"] == GOLD,
              tr["decisive step alone: per never-heard airplane"])
        check("R3b the lower rung's single correction (the capture rate split by flight training) stays wrong on the "
              "clean truth", tr["capture by flight training"] not in (GOLD,), tr["capture by flight training"])
        check("R3b the year's actual lead qualifies the same seven", tr["the year's actual lead"] == GOLD,
              tr["the year's actual lead"])
        check("R3 the pack's recorded lead equals the clean truth's at every field (within 1 g)",
              all(abs(gi["heard"].loc[l, "lead"] - T["H"].get(l, 0.0)) < 1.0 for l in B.FIELDS))
        check("R3 the pack's counted fields' unrecorded operations equal the never-broadcasting airplanes' operations "
              "in the hours each count covers (%d of them on the contract towers' closed days)" % (
                  sum(T["miss"].get(l, 0) - T["miss_open"].get(l, 0) for l in W.TOWERED)),
              all(gi["unrec"][l] == T["miss_open"].get(l, 0) for l in W.COUNTED),
              {l: (gi["unrec"][l], T["miss_open"].get(l, 0)) for l in W.COUNTED})
        check("R3 the never-recorded based piston airplanes are the never-broadcasting ones, field by field",
              all(gi["nd"][l] == T["nd"][l] for l in B.FIELDS), {l: (gi["nd"][l], T["nd"][l]) for l in B.FIELDS
                                                                 if gi["nd"][l] != T["nd"][l]})
    docs = {k: pdf_text(os.path.join(target, W.FILES[k])) for k in
            ("method", "grants", "network", "reg_notes", "f37", "g42")}
    for k in ("based", "directory", "l08", "d19", "m5010"):
        docs[k] = xlsx_text(os.path.join(target, W.FILES[k]))
    control = {"method": "An operation is a takeoff or a landing.", "grants": "The round funds every qualifying field.",
               "network": "An aircraft that broadcasts ADS-B Out is recorded at every field it uses.",
               "reg_notes": "N-NUMBER is written without the leading N.", "f37": "A takeoff or a landing is one",
               "g42": "a touch-and-go two", "based": "Released 5 January 2027",
               "directory": "ATCT hours are local time", "l08": "two operations", "d19": "Acoustic and video counters",
               "m5010": "airport manager's estimate"}
    check("R3c positive controls: each document's text is read through the extractor the absence checks use",
          all(control[k] in docs[k] for k in control), [k for k in control if control[k] not in docs[k]])
    banned = r"never[- ]recorded|never[- ]heard|capture|completion factor|correction factor|per based|equipage|" \
             r"equipped|per airplane|per aircraft|non-broadcast|qualif(?:y|ies) (?:Umber|Orrin|Wickrow|Thornacre)"
    hits = {k: re.findall(banned, v, re.I) for k, v in docs.items()}
    check("R3c no plant: no document names the never-recorded airplanes, a capture or correction factor, an "
          "estimator per airplane or a verdict on a field", not any(hits.values()), {k: v for k, v in hits.items() if v})
    check("R3c the network notes state the mechanism only: aircraft without ADS-B Out are not recorded",
          "An aircraft without ADS-B Out, or with it switched off, is not recorded." in docs["network"])
    check("R3c no memo, briefing, draft or stakeholder figure ships (the pack's documents are the method, the "
          "guidelines, the network's and register's notes, two count reports and five workbooks)",
          not any(re.search(r"memo|draft|briefing", f, re.I) for f in files))

    # ------------------------------------------------------------------ the ladder
    rungs, sets, par = M.rungs(G, gi)
    want = {"R0 one capture rate": R0SET, "R0b one capture rate on the lead": R0SET,
            "R1 capture by flight training": ["A71", "F37", "K58", "L08", "N26", "P05", "S27", "T13", "T61"],
            "R2 operations per based airplane": ["A71", "F37", "H52", "L08", "O16", "T13", "U44", "W33", "W85"],
            "R3 unrecorded per based airplane": ["A71", "F37", "K58", "L08", "P05", "T13", "T61", "U44"],
            "R4 never-heard airplanes fly like the heard ones": ["A71", "F37", "L08", "T13", "W33"],
            "R5 the network's record alone": ["A71", "F37", "L08", "T13"],
            "G unrecorded per never-heard airplane": GOLD}
    for k, v in want.items():
        check("ladder %s qualifies %s" % (k, " ".join(v)), sets[k] == v, sets[k])
    distinct = {frozenset(v) for k, v in want.items() if k != "R0b one capture rate on the lead"}
    check("ladder every rung names its own set (R0b is R0's variant)", len(distinct) == len(want) - 1)
    for k, v in rungs.items():
        if k.startswith("G"):
            continue
        m = min(abs(v[l] - TH) / TH for l in W.UNTOWERED)
        check("ladder %s: every field at least 3.5 per cent from the line (closest %.1f)" % (k, 100 * m), m >= 0.035)
    check("ladder the default path keeps the counted fields' capture at %.3f and the training split at %.3f and %.3f"
          % (par["r"], par["r_school"], par["r_other"]), 0.78 < par["r"] < 0.85 and par["r_school"] > par["r_other"])
    caps = {l: (gi["tower"][l]["heard_in_hours"] / gi["tower"][l]["civil"]) if l in W.TOWERED else
            gi["heard"].loc[l, "ops"] / G.study[l] for l in W.COUNTED}
    per = {l: gi["unrec"][l] / gi["nd"][l] for l in W.COUNTED}
    check("ladder the counted fields' capture spreads %.2f to %.2f while unrecorded operations per never-recorded "
          "airplane stay within %.0f to %.0f" % (min(caps.values()), max(caps.values()), min(per.values()),
                                                 max(per.values())),
          max(caps.values()) - min(caps.values()) > 0.3 and max(per.values()) / min(per.values()) < 1.15)

    # the counted fields score the completions on equal terms: each predicts a left-out counted field's unrecorded
    # operations from the other nine
    pb = {l: len(v) for l, v in gi["piston_based"].items()}
    act = G.based_activity(gi)
    hops = {l: gi["tower"][l]["heard_in_hours"] if l in W.TOWERED else gi["heard"].loc[l, "ops"] for l in W.COUNTED}
    cnt = {l: gi["tower"][l]["civil"] if l in W.TOWERED else G.study[l] for l in W.COUNTED}
    err = {m: [] for m in ("capture", "per based", "operations per based", "recorded airplanes' rate", "golden")}
    for l in W.COUNTED:
        o = [z for z in W.COUNTED if z != l]
        r_ = sum(hops[z] for z in o) / sum(cnt[z] for z in o)
        k_ = sum(gi["unrec"][z] for z in o) / sum(gi["nd"][z] for z in o)
        kb_ = sum(gi["unrec"][z] for z in o) / sum(pb[z] for z in o)
        op_ = sum(gi["heard"].loc[z, "ops"] + gi["unrec"][z] for z in o) / sum(pb[z] for z in o)
        pred = {"capture": hops[l] * (1 - r_) / r_, "per based": kb_ * pb[l],
                "operations per based": max(0.0, op_ * pb[l] - gi["heard"].loc[l, "ops"]),
                "recorded airplanes' rate": act[l] * gi["nd"][l], "golden": k_ * gi["nd"][l]}
        for m, v in pred.items():
            err[m].append(abs(v - gi["unrec"][l]) / gi["unrec"][l])
    mean = {m: 100 * sum(v) / len(v) for m, v in err.items()}
    check("ladder leave-one-out at the ten counted fields: the rate per never-recorded airplane misses by %.0f per "
          "cent on average (worst %.0f), every other completion by %.0f per cent or more" % (
              mean["golden"], 100 * max(err["golden"]), min(v for m, v in mean.items() if m != "golden")),
          mean["golden"] < 6 and max(err["golden"]) < 0.10 and
          all(v > 25 for m, v in mean.items() if m != "golden"), {m: round(v) for m, v in mean.items()})

    # ------------------------------------------------------------------ the golden family and the fork table
    fam = {}
    for m in ("mean_of_ratios", "ols_origin", "median"):
        fam[m] = G.inventory(k_method=m)
    fam["towers only"] = G.inventory(k_fields=W.TOWERED)
    fam["studies only"] = G.inventory(k_fields=W.STUDIED)
    for k, inv in fam.items():
        check("SF13 the per-airplane rate by %s (%.2f) gives the same call and every field's lead in the same whole "
              "kilogram" % (k, inv["k"]), B.qualifying(inv["lead"]) == gold and
              all(round(inv["lead"][l]) == gk[l] for l in W.UNTOWERED))
    variants = {"SF2 the year read on UTC dates": dict(year="utc"), "L1 the export's padding days kept": dict(year="all"),
                "L1 times read at UTC-8 all year": dict(dst=False),
                "SF10 tower hours without the winter hours and closed days": dict(winter=False),
                "L1 addresses today's register no longer lists dropped": dict(dereg=False),
                "SF9 the towers' military columns taken as civil": dict(civil="all"),
                "SF12 a based airplane tested by its current address only": dict(link=False)}
    vinv = {}
    for k, o in variants.items():
        P = B.Pack(target, _cache=cache, **o)
        inv = P.inventory()
        vinv[k] = inv
        check("%s: the same call and every non-towered field's lead in the same whole kilogram" % k,
              B.qualifying(inv["lead"]) == gold and all(round(inv["lead"][l]) == gk[l] for l in W.UNTOWERED),
              [l for l in W.UNTOWERED if round(inv["lead"][l]) != gk[l]])
    check("SF1 'qualifies' at 12.5 kg or more: no field within 1 kg of the line, so or more and more than agree",
          min(abs(lead[l] - TH) for l in W.UNTOWERED) > 1.0)
    check("SF14 qualification on the rounded lead (whole kilograms) gives the same call",
          sorted(l for l in W.UNTOWERED if round(lead[l]) >= TH) == gold)
    check("SF3 a touch-and-go is two operations (method 2.1) and one event in the export (network notes)",
          "A touch-and-go is two operations, a landing and a takeoff" in docs["method"] and
          "A touch-and-go is one event." in docs["network"])
    ev = G.priced()
    tg_lead = {}
    for l in W.UNTOWERED:
        e = ev[(ev["site"] == l) & (ev["event"] == "touch_and_go")]
        tg_lead[l] = e["lead_g"].sum() / 2.0 / 1000.0
    alt = {l: lead[l] - tg_lead[l] for l in W.UNTOWERED}
    check("SF3 a touch-and-go read as one operation priced once: the call %s" % (
        "unchanged" if B.qualifying(alt) == gold else "moves (ruled out by method 2.1)"),
          "A touch-and-go is two operations" in docs["method"])
    R = G.R
    airframe = B.Pack(target, _cache=cache)
    for g in airframe.R["regs"]:
        g["_p"], g["_c"] = g["piston"], g["cls"]
        g["piston"] = g["type_acft"] in ("4", "5")
        g["cls"] = ("single" if g["type_acft"] == "4" else "multi") if g["piston"] else "other"
    ainv = airframe.inventory()
    for g in airframe.R["regs"]:
        g["piston"], g["cls"] = g.pop("_p"), g.pop("_c")
    check("SF4 'piston-engine' by TYPE ENGINE 1 (method 1.2, register notes): reading every fixed-wing airplane as "
          "piston, turboprops and jets included, %s" % ("keeps the call" if B.qualifying(ainv["lead"]) == gold else
                                                        "moves the call and is ruled out by method 1.2"),
          "Aircraft with turbine engines" in docs["method"])
    check("SF5 the candidates are the 24 public-use fields without a tower (guidelines 2.1); the directory's six "
          "private strips are private use", sum(1 for l, d in G.dir.items() if d["Use"] == "Public" and d["ATCT"] == "N")
          == 24 and all(G.dir[l]["Use"] == "Private" for l, _, _ in W.STRIPS))
    check("SF6 lead in flight away from the field is outside the inventory (method 1.2)",
          "lead emitted in flight away from the field" in docs["method"])
    check("SF7 an unrecorded operation is %.3f g (method 3.2)" % W.LEAD_UNRECORDED,
          ("%.3f g" % W.LEAD_UNRECORDED) in docs["method"])
    check("SF8 the counted fields are the six towers and the four count fields (method 4.2, 4.3); towers or studies "
          "alone give the same call (SF13 rows)", "At the six fields with a control tower" in docs["method"] and
          "Fennick Airpark, Lanthorne Field, Graylow Municipal and Dunmarsh Airport" in docs["method"])
    check("SF11 the based airplanes come from the state's validation by N-number; the 5010 records give counts only "
          "and their own vintage", "Based aircraft and annual operations are as each airport reported them" in
          docs["m5010"])
    allb = [b for b in G.based]
    regn = {g["n"] for g in R["regs"]}
    check("L1 every N-number on the based aircraft validation, written four ways by county, matches the register "
          "(%d of %d)" % (sum(b["n"] in regn for b in allb), len(allb)), all(b["n"] in regn for b in allb))
    raw = {c: sum(1 for b in allb if b["county"] == c and re.fullmatch(r"N[0-9A-Z]+", str(b["raw"]))) for c in W.COUNTIES}
    check("L1 the counties write N-numbers differently (prefix, case, spaces)", raw["Corrisan"] > 0 and
          raw["Halwick"] == 0 and raw["Ostrey"] == 0, raw)

    # ------------------------------------------------------------------ separation: the ask's device and the call
    cur = G.inventory(how="current")
    check("separation: today's register in place of the register's history leaves every non-towered field's lead, "
          "the counted fields' unrecorded operations and k unchanged",
          all(abs(cur["lead"][l] - lead[l]) < 1e-9 for l in W.UNTOWERED) and cur["unrec"] == gi["unrec"] and
          abs(cur["k"] - gi["k"]) < 1e-12)
    moved = [g for g in R["regs"] if not g["current"] and g["cancel"].year == 2026 and
             any(c["current"] and c["hex"] == g["hex"] and c["serial"] != g["serial"] for c in R["regs"])]
    before = ev[ev["icao24"].isin({g["hex"] for g in moved})]
    cut = {g["hex"]: g["cancel"] for g in moved}
    before = before[[d < cut[h] for h, d in zip(before["icao24"], before["date"])]]
    check("separation: the %d addresses that passed in 2026 to another aircraft carried the piston airplanes' %d "
          "events before the change at the towered fields only" % (len(moved), len(before)),
          len(moved) == 8 and set(before["site"]) <= set(W.TOWERED) and len(before) > 1000, sorted(set(before["site"])))

    # ------------------------------------------------------------------ the ask: the towered fields
    stops = {"today's register (the cracker)": cur}
    drop = B.Pack(target, _cache=cache)
    drop.ev = drop.ev[~drop.ev["icao24"].isin({g["hex"] for g in moved})]
    stops["the passed addresses' events dropped"] = drop.inventory()
    allyear = B.Pack(target, _cache=cache)
    for g in allyear.R["regs"]:
        if g in moved:
            g["_cancel"] = g["cancel"]
            g["cancel"] = dt.date(2027, 12, 31)
    stops["the passed addresses read as the piston airplane all year"] = allyear.inventory()
    for g in allyear.R["regs"]:
        if "_cancel" in g:
            g["cancel"] = g.pop("_cancel")
    for k, inv in stops.items():
        miss = sum((round(inv["lead"][l]) != gk[l]) + (round(inv["ops"][l] / 100.0) != go[l]) for l in W.TOWERED)
        check("ask: %s misses %d of the 12 towered figures" % (k, miss), miss == 12 if "cracker" in k else miss >= 8)
    for k in ("L1 times read at UTC-8 all year", "SF10 tower hours without the winter hours and closed days",
              "SF9 the towers' military columns taken as civil"):
        inv = vinv[k]
        mv = sum((round(inv["lead"][l]) != gk[l]) + (round(inv["ops"][l] / 100.0) != go[l]) for l in W.TOWERED)
        check("ask hazard %s moves %d towered figures" % (k, mv), mv >= 1)
    deltas = {l: (lead[l] - cur["lead"][l], ops[l] - cur["ops"][l]) for l in W.TOWERED}
    check("ask: the device moves every tower by at least 1 kg and 500 operations",
          all(d[0] >= 1.0 and d[1] >= 500 for d in deltas.values()), deltas)

    # ------------------------------------------------------------------ bins
    e1 = {l: edge(lead[l], 1.0) for l in B.FIELDS}
    e2 = {l: edge(ops[l], 100.0) for l in W.TOWERED}
    worst = min(e1, key=e1.get)
    check("bins: every lead at least 0.25 kg from its whole-kilogram edge (tightest %s, %.2f)" % (worst, e1[worst]),
          min(e1.values()) >= 0.25)
    worst2 = min(e2, key=e2.get)
    check("bins: every towered field's operations at least 20 from the hundreds edge (tightest %s, %.0f)" % (
        worst2, e2[worst2]), min(e2.values()) >= 20)
    check("bins: no figure sits on a round value (no lead within 0.02 kg of a whole kilogram, no operations on a "
          "hundred)", all(abs(lead[l] - round(lead[l])) > 0.02 for l in B.FIELDS) and
          all(abs(ops[l] - round(ops[l] / 100.0) * 100) > 2 for l in W.TOWERED))

    # ------------------------------------------------------------------ distractors
    for k in W.DISTRACTORS:
        tmp = tempfile.mkdtemp()
        try:
            for f in files:
                if f != W.FILES[k]:
                    shutil.copy(os.path.join(target, f), tmp)
            inv = B.Pack(tmp).inventory()
            check("distractor %s deleted: the call and every graded figure unchanged" % W.FILES[k],
                  B.qualifying(inv["lead"]) == gold and all(round(inv["lead"][l]) == gk[l] for l in B.FIELDS)
                  and all(round(inv["ops"][l] / 100) == go[l] for l in W.TOWERED))
        finally:
            shutil.rmtree(tmp)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(target, W.FILES["m5010"]), read_only=True)
    rows = list(wb["5010 data"].iter_rows(min_row=2, values_only=True))
    base_5010 = {}
    for r in rows:
        if r[0] in W.UNTOWERED:
            tot = (r[9] or 0) + (r[10] or 0) + (r[11] or 0)
            base_5010[r[0]] = tot * W.LEAD_UNRECORDED / 1000.0
    s5010 = sorted(l for l, v in base_5010.items() if v >= TH)
    check("wrong-basis distractor: the 5010 operations priced at %.3f g qualify %s, neither the golden nor the "
          "default path's set" % (W.LEAD_UNRECORDED, " ".join(s5010)), s5010 not in (gold, R0SET), s5010)
    check("wrong-basis distractor: ruled out by its own notes (the managers' estimates for twelve months ending "
          "2018 to 2025)", "operations are the airport manager's estimate for the 12 months ending" in docs["m5010"]
          and all(r[13].year <= 2025 for r in rows))

    # ------------------------------------------------------------------ realism and consistency
    dash = []
    for f in files:
        p = os.path.join(target, f)
        txt = pdf_text(p) if f.endswith(".pdf") else (xlsx_text(p) if f.endswith(".xlsx") else
                                                       open(p, encoding="utf-8").read())
        if re.search("[–—]", txt):
            dash.append(f)
    check("realism: no en or em dash in any shipped file", not dash, dash)
    lad = max(B.ymd(g) for g in [r["LAST ACTION DATE"] for r in B.padded(os.path.join(target, W.FILES["master"]))])
    can = max(g["cancel"] for g in R["regs"] if not g["current"])
    check("realism: no register date after the 1 February 2027 download (last action %s, last cancellation %s)" % (
        lad, can), lad <= dt.date(2027, 2, 1) and can <= dt.date(2027, 2, 1))
    evx = B.events(target)
    check("realism: the export runs from 30 December 2025 to 2 January 2027 local time, before its 8 January pull",
          evx["local"].min().date() >= dt.date(2025, 12, 30) and evx["local"].max().date() <= dt.date(2027, 1, 2))
    check("realism: every event's address is in the register (MASTER or DEREG)",
          set(evx["icao24"]) <= {g["hex"] for g in R["regs"]}, len(set(evx["icao24"]) - {g["hex"] for g in R["regs"]}))
    a = B.atct(target)
    check("realism: the towers' daily rows add up (itinerant and local totals)",
          (a["Itinerant Total"] == a["Itinerant Air Carrier"] + a["Itinerant Air Taxi"] +
           a["Itinerant General Aviation"] + a["Itinerant Military"]).all() and
          (a["Total Operations"] == a["Itinerant Total"] + a["Local Total"]).all())
    series = {f: tuple(a.loc[a["Facility"] == f, "Total Operations"]) for f in W.TOWERED}
    check("realism sweep: no two towers share a daily series and no tower repeats one count day after day",
          len(set(series.values())) == len(series) and all(len(set(v)) > 30 for v in series.values()))
    check("realism sweep: no tower's annual civil total, no study's piston total and no field's recorded operations "
          "sit on a round hundred", all(int(a.loc[a["Facility"] == f, "civil"].sum()) % 100 for f in W.TOWERED) and
          all(v % 100 for v in G.study.values()) and all(int(gi["heard"].loc[l, "all_ops"]) % 100 for l in B.FIELDS))
    check("realism sweep: event ids unique and no event repeated (site, time, address)",
          evx["event_id"].is_unique and not evx.duplicated(["site", "event_time_utc", "icao24"]).any())
    mon = {}
    for l in ("F37", "G42"):
        txt = B.pdf_layout(os.path.join(target, W.FILES[l.lower()]))
        mon[l] = re.findall(r"^\s*(?:January|February|March|April|May|June|July|August|September|October|November|"
                            r"December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+([\d,]+)", txt, re.M)
    check("realism sweep: the count reports' monthly rows differ month to month (no repeated block)",
          all(len(v) == 12 and len(set(v)) == 12 for v in mon.values()), mon)
    closed = a[(a["Facility"].isin(W.CONTRACT_TOWERS)) & (a["Date"].isin(["12/25/2026", "01/01/2026"]))]
    check("realism: the contract towers' closed days carry no count", (closed["Total Operations"] == 0).all())
    if golden and F:
        with open(os.path.join(golden, W.GOLDEN["csv"]), encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        check("deliverables: the CSV carries the 24 fields' lead as figures.json does",
              [(r["loc_id"], int(r["lead_2026_kg"])) for r in rows] == [(r["lid"], r["lead_kg"]) for r in F["fields"]])
        check("deliverables: the CSV's leads are the bundle's, rounded", all(int(r["lead_2026_kg"]) == gk[r["loc_id"]]
                                                                            for r in rows))
        from docx import Document
        d = Document(os.path.join(golden, W.GOLDEN["memo"]))
        body = "\n".join(p.text for p in d.paragraphs)
        tab = [[c.text for c in r.cells] for r in d.tables[0].rows]
        check("deliverables: the memo names every qualifying field with its lead",
              all("%s (%s, %d kg)" % (r["name"], r["lid"], r["lead_kg"]) in body for r in F["qualifying"]))
        check("deliverables: the memo's towered fields table matches figures.json",
              tab[1:] == [[r["name"], r["lid"], r["ops"], str(r["lead_kg"])] for r in F["towers"]], tab)
        check("deliverables: the memo carries one chart", len(d.inline_shapes) == 1)
        check("deliverables: figures.json towers are the bundle's figures",
              all(r["lead_kg"] == gk[r["lid"]] and int(r["ops"].replace(",", "")) == go[r["lid"]] * 100
                  for r in F["towers"]))
    if meta_path:
        meta = json.load(open(meta_path))
        check("metadata: the distractors are named and exist", all(f in files for f in meta["distractor_files"]) and
              len(meta["distractor_files"]) >= 2)
    n_ok = sum(ok for _, ok, _ in RESULTS)
    print("checks: %d of %d pass" % (n_ok, len(RESULTS)))
    return n_ok == len(RESULTS)
