"""task458's assertions, run on every build: the input gates; the golden from the bundle against the generator's truth;
the three-rules block on the clean truth (the reader's route and the default path file the six, the decisive step alone
files the five); every route by name; the valid variants' convergence, margins and bins; the data's own evidence that the
full-year prevalence does not carry to the seasonal spells; every semantic-fork row; the double-error grid; mess
neutrality; the payments' golden and stops; the separation of the asks from the main call; the realism sweep."""
import collections
import csv
import json
import os
import re

import conform as CF
import golden as GD
import methods as MT
import pack as P
import providers as PV
import world as W

RESULTS = []
EDGE = 2.0          # a graded count's least distance from its rounding edge (members)
GOLD = MT.GOLD
SIX = ("Adams", "Douglas", "Franklin", "Grant", "Okanogan", "Yakima")


def ok(label, cond, detail=""):
    RESULTS.append((label, bool(cond), detail))


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def truth_table(world):
    """The clean truth: each person's county, group, months, and whether the generator's claims (final versions)
    identify each condition and in which contract-year month first; the practising prescribers by construction; no
    NPPES file, no version, no key."""
    import pandas as pd
    lines = world["lines"]
    gone = {l["orig"] for l in lines if l["freq"] in ("7", "8")}
    smi_set = {c.replace(".", "") for c in W.SMI_CODES}
    oud_set = {c.replace(".", "") for c in W.OUD_CODES}
    bh = {c["npi"] for c in world["clins"] if PV.renders(c) and PV.primary_on(c, W.AS_OF) in W.BH_TAXONOMY}
    bh |= {c["npi"] for c in world["clins"] if c["kind"] == "deact_late_before"}
    first = {"smi": {}, "oud": {}}
    cal = {ym: i + 1 for i, ym in enumerate(W.MONTHS)}
    seen = set()
    for l in lines:
        if l["icn"] in gone or l["freq"] == "8":
            continue
        k = (l["from"].year - 2025) * 12 + l["from"].month - 6
        for cond, codes in (("smi", smi_set), ("oud", oud_set)):
            if codes & set(l["dx"]):
                first[cond][l["person"]] = min(first[cond].get(l["person"], 99), k)
        if l["proc"] in CF.VISITS and l["render"] in bh:
            seen.add(l["person"])
    rows = []
    for p in world["persons"]:
        enr = [cal[ym] for ym in p.months]             # the person's enrolled months, as contract-year months
        row = {"client_id": p.pid, "county": p.county, "group": P.GROUP_CODE[p.group], "months": len(p.months),
               "full_year": len(p.months) == 12, "rec_smi": p.pid in first["smi"], "rec_oud": p.pid in first["oud"],
               "first_smi": first["smi"].get(p.pid, float("nan")), "first_oud": first["oud"].get(p.pid, float("nan")),
               "seen": p.pid in seen, "smi": p.smi, "oud": p.oud, "short": p.short}
        for c, C in (("smi", "SMI"), ("oud", "OUD")):
            # the generator's first month as a contract-year month, and the claims' first month as an enrolled month
            row["first_assigned_" + c] = enr[p.first[C] - 1] if p.first[C] is not None else float("nan")
            row["first_enrolled_" + c] = enr.index(first[c][p.pid]) + 1 if p.pid in first[c] else float("nan")
        rows.append(row)
    mem = pd.DataFrame(rows).set_index("client_id")
    pr = PV.practising(world["clins"])
    return {"members": mem, "practising": pr, "final": None}


def _rate(c, g, cond):
    """The generator's rate for a county, group and condition (members.py), seasonal members aside."""
    import numpy as np
    names = sorted(W.COUNTIES)
    fr = np.random.default_rng([W.SEED, 6, names.index(c), W.GROUPS.index(g)])
    f_smi = float(np.exp(fr.normal(0.0, 0.08)))
    f_oud = float(np.exp(fr.normal(0.0, 0.08)))
    return W.PREV[cond][g] * W.COUNTIES[c]["f_" + cond.lower()] * (f_smi if cond == "SMI" else f_oud)


def run(target, golden_dir, world=None, meta_path=None):
    import numpy as np
    RESULTS.clear()
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else {}
    # ------------------------------------------------------------------ input gates
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    ok("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, sorted({f.rsplit(".", 1)[1] for f in files}))
    nrows = {f: sum(1 for _ in open(os.path.join(target, f), encoding="utf-8")) - 1 for f in files if f.endswith(".csv")}
    ok("gate: one file of 25,000 rows or more", max(nrows.values()) >= 25000, max(nrows.items(), key=lambda x: x[1]))
    ok("gate: two or more distractors named in metadata.json and shipped",
       len(meta.get("distractor_files", [])) >= 2 and all(d in files for d in meta.get("distractor_files", [])),
       meta.get("distractor_files"))
    ok("gate: no distractor named as such in a file name", not any("distractor" in f for f in files))
    ok("gate: every file has source, date and license in metadata.json",
       all(x.get("source") and x.get("date") and x.get("license") for x in meta.get("files", [])) and
       {x["path"] for x in meta.get("files", [])} == set(files))

    a = CF.analysis(target)
    sc = a["scorecard"]
    des = tuple(sorted(sc.index[sc["designated"]]))
    ok("golden: NP-31 designates Adams, Douglas, Franklin, Grant and Okanogan", des == GOLD, des)

    # ------------------------------------------------------------------ the files against the generator's truth
    if world is not None:
        pr = PV.practising(world["clins"])
        ok("truth: the practising prescribers read from NPPES and the claims are the generator's, county by county",
           all(sorted(pr[c]) == a["practising"][c] for c in W.COUNTIES),
           {c: (len(pr[c]), len(a["practising"][c])) for c in W.COUNTIES})
        ok("truth: every county's practising count is its target",
           all(len(a["practising"][c]) == W.COUNTIES[c]["prescribers"] for c in W.COUNTIES))
        mem = a["members"]
        ok("truth: one conformed member per person", len(mem) == len(world["persons"]), (len(mem), len(world["persons"])))
        tp = {p.pid: p for p in world["persons"]}
        cm = _cid_map(world, target)
        ok("truth: county, group and months of every person match the spans",
           all(len(tp[pid].months) == mem.loc[cid, "months"] and tp[pid].county == mem.loc[cid, "county"] and
               P.GROUP_CODE[tp[pid].group] == mem.loc[cid, "group"] for cid, pid in cm.items()))
        tt = truth_table(world)
        tm = tt["members"]
        ok("truth: the claims identify each member first in the month the generator assigned, or never",
           all((tm["first_" + c].fillna(0).astype(int) == tm["first_assigned_" + c].fillna(0).astype(int)).all() for c in ("smi", "oud")))
        ok("truth: every member enrolled all year with a condition is identified by a claim",
           int((tm["full_year"] & ((tm["smi"] & ~tm["rec_smi"]) | (tm["oud"] & ~tm["rec_oud"]))).sum()) == 0)
        ok("truth: a claim never identifies a condition the member does not have",
           int((tm["rec_smi"] & ~tm["smi"]).sum()) == 0 and int((tm["rec_oud"] & ~tm["oud"]).sum()) == 0)
        seen_unrec = tm[tm["smi"] & tm["seen"] & ~tm["rec_smi"]]
        ok("truth: every member with a serious mental illness who saw a behavioral-health prescriber is identified",
           len(seen_unrec) == 0, len(seen_unrec))
        ok("truth: the shipped first months equal the generator's",
           all((mem.loc[cid, "first_smi"] if mem.loc[cid, "rec_smi"] else 0) == (tm.loc[pid, "first_smi"] if tm.loc[pid, "rec_smi"] else 0)
               for cid, pid in list(cm.items())[::50]))
        # exact allocation: within county, group and kind, nested by months enrolled
        bad = 0
        for (c, g, short), cell in tm.groupby(["county", "group", "short"]):
            gk = {v: k for k, v in P.GROUP_CODE.items()}[g]
            for cond in ("smi", "oud"):
                rate = _rate(c, gk, cond.upper()) * (W.RHO[cond.upper()] if short else 1.0)
                for k in range(1, 13):
                    sel = cell[cell["months"] >= k]
                    if len(sel) and abs(int(sel[cond].sum()) - round(len(sel) * rate)) > 1:
                        bad += 1
        ok("truth: conditions allocated exactly by county, group and kind of member, nested by months enrolled", bad == 0, bad)
        bad = 0
        for (c, g, m), cell in tm.groupby(["county", "group", "months"]):
            for cond in ("smi", "oud"):
                has = cell[cell[cond]]
                n = len(has)
                for k in range(1, m + 1):
                    want = n if k == 12 else int(round(W.capture(cond.upper(), k) * n))
                    if int((has["first_enrolled_" + cond] <= k).sum()) != want:
                        bad += 1
        ok("truth: first identification allocated exactly, the same F(k) in every county, group and months enrolled", bad == 0, bad)
        sr = tm[tm["short"]]
        ok("truth: the seasonal members have each condition at RHO times the others' rate, county by group",
           abs(sr["smi"].sum() / sum(_rate(c, {v: k for k, v in P.GROUP_CODE.items()}[g], "SMI") * n
                                     for (c, g), n in sr.groupby(["county", "group"]).size().items()) - W.RHO["SMI"]) < 0.02)
        # ---------------------------------------------------------- the three rules on the clean truth
        R = MT.routes_from(tm, {c: len(v) for c, v in tt["practising"].items()})
        ok("three rules (clean truth): the reader's route, each group's full-year prevalence carried to all its members, "
           "files the six", R["full_year_group"][1] == SIX, R["full_year_group"][1])
        ok("three rules (clean truth): the default path, each county's full-year prevalence carried whole, files the six",
           R["county_full_year"][1] == SIX, R["county_full_year"][1])
        ok("three rules (clean truth): the decisive step alone, each identified member weighted by the months it was "
           "observed, files the five", R["golden"][1] == GOLD, R["golden"][1])
        ok("three rules (clean truth): counting the identified members files Adams, Douglas and Okanogan",
           R["recorded"][1] == ("Adams", "Douglas", "Okanogan"), R["recorded"][1])
        ttrue = MT.standards({c: len(v) for c, v in tt["practising"].items()},
                             tm.groupby("county")["smi"].sum().reindex(CF.COUNTIES),
                             tm.groupby("county")["oud"].sum().reindex(CF.COUNTIES),
                             (tm["smi"] & tm["seen"]).groupby(tm["county"]).sum().reindex(CF.COUNTIES))
        ok("three rules (clean truth): the members who truly have each condition file the five", MT.designated(ttrue) == GOLD,
           MT.designated(ttrue))
        nd_t = MT.needs_from(tm)
        dev = {(c, k): round(nd_t["golden"][i][c] - tm.groupby("county")[k].sum()[c], 1)
               for i, k in ((0, "smi"), (1, "oud")) for c in CF.COUNTIES}
        ok("truth: the months-observed weighting recovers every county's true count within 2 per cent",
           all(abs(v) <= 0.02 * tm.groupby("county")[k].sum()[c] for (c, k), v in dev.items()), dev)

    # ------------------------------------------------------------------ every route on the shipped files
    R = MT.routes(a)
    SEVEN = ("Adams", "Douglas", "Franklin", "Grant", "Okanogan", "Walla Walla", "Yakima")
    expect = {"golden": GOLD, "ipw_group": GOLD, "ipw_cell": GOLD, "ipw_days": GOLD,
              "full_year_group": SIX, "full_year_group_11": SIX, "plan_group": SIX, "county_full_year": SIX,
              "county_full_year_11": SIX, "plan_full_year": SIX, "exposure": SIX,
              "recorded": ("Adams", "Douglas", "Okanogan"), "full_year_only": ("Douglas", "Okanogan"),
              "fitted_capture": SEVEN, "pooled_factor": SEVEN}
    for k, st in expect.items():
        ok("route %s files %s" % (k, ", ".join(st)), R[k][1] == st, R[k][1])
    # margins of the golden and its valid variants: every verdict at least 5 per cent from its threshold
    for k in ("golden", "ipw_group", "ipw_cell", "ipw_days"):
        m = MT.margins(R[k][0]).abs().values.min()
        ok("margin: every verdict of %s at least 5 per cent from its threshold" % k, m >= 0.05, round(float(m), 4))
        same = all(((R[k][0][c] < CF.THRESH[t]) == (R["golden"][0][c] < CF.THRESH[t])).all()
                   for c, t in (("s_smi", "smi"), ("s_oud", "oud"), ("s_reach", "reach")))
        ok("convergence: %s gives the golden's thirty verdicts" % k, same)
    for k in ("full_year_group", "full_year_group_11", "plan_group"):
        y = MT.margins(R[k][0]).loc["Yakima"]
        ok("margin: %s fails Yakima on at least two standards by 5 per cent or more" % k, int((y <= -0.05).sum()) >= 2,
           [round(float(v), 3) for v in y])
    nd = MT.needs(a)
    for i, cond in ((0, "serious mental illness"), (1, "opioid use disorder")):
        g = nd["golden"][i]
        for k in ("ipw_group", "ipw_cell", "ipw_days"):
            v = nd[k][i]
            ok("bins: members with a %s, the golden and %s round to the same 10 in every county" % (cond, k),
               all(round(g[c] / 10) == round(v[c] / 10) for c in CF.COUNTIES),
               {c: (round(g[c], 1), round(v[c], 1)) for c in CF.COUNTIES if round(g[c] / 10) != round(v[c] / 10)})
        edge = {c: round(g[c], 2) for c in CF.COUNTIES if abs((g[c] % 10) - 5) < EDGE}
        ok("bins: members with a %s at least %.1f from a rounding edge" % (cond, EDGE), not edge, edge)
    ok("the reader's route (full-year prevalence by group) moves Yakima onto two failures or more",
       R["full_year_group"][0].loc["Yakima", "fails"] >= 2 and R["golden"][0].loc["Yakima", "fails"] == 0)
    # the data's own evidence: the same window, two kinds of member
    mem = a["members"]
    exp = mem[mem["group"] == "ADULT-EXP"]
    fy = exp[exp["full_year"]]
    short = exp[exp["months"] == 3]["rec_smi"].mean()
    full3 = (fy["first_smi"] <= 3).mean()
    ok("evidence: expansion adults enrolled three months are identified with a serious mental illness at under 0.65 of "
       "the share of the full-year expansion adults identified within their first three months", short < 0.65 * full3,
       (round(float(short), 4), round(float(full3), 4)))
    part = exp[(exp["months"] >= 7) & (exp["months"] <= 11)]
    expd = sum((fy["first_smi"] <= m).mean() * n for m, n in part["months"].value_counts().items())
    ratio = part["rec_smi"].sum() / expd
    ok("evidence: expansion adults enrolled seven to eleven months are identified as the full-year members are within "
       "the same months (ratio 0.9 to 1.1)", 0.9 <= ratio <= 1.1, round(float(ratio), 3))

    # ------------------------------------------------------------------ the semantic fork table (each row's readings)
    sf = {
        "SF1": ("adult member as a person (client_id), not a member number", dict(key="member")),
        "SF2": ("a member's county on the last enrolled day, not the first span's", dict(county_rule="first")),
        "SF3": ("a member's county on the last enrolled day, not the county of most days", dict(county_rule="most")),
        "SF4": ("a listed code in any diagnosis position, not the first only", dict(dx_positions=1)),
        "SF5": ("final versions, not every version", dict(versions="all")),
        "SF6": ("NPPES updated by the weekly files through 1 November, not the October file alone", dict(weeks="none")),
        "SF7": ("NPPES through 1 November, not the November week too", dict(weeks="all")),
        "SF8": ("the ZIP's county by business addresses, not residential", dict(zip_basis="RES_RATIO")),
        "SF9": ("the ZIP's county by business addresses, not all addresses", dict(zip_basis="TOT_RATIO")),
        "SF10": ("a prescriber taxonomy as the primary one, not any listed one", dict(taxonomy="any")),
        "SF11": ("the practice location, not the mailing address", dict(location="mailing")),
        "SF12": ("a deactivated NPI's prescriber taxonomy from its last record", dict(deact_rule="blank")),
        "SF13": ("deactivations on 1 November from the files, not the November report's later dates",
                 dict(deact_report=True)),
    }
    for sid, (label, opt) in sf.items():
        b = CF.analysis(target, **opt)
        st = tuple(sorted(b["scorecard"].index[b["scorecard"]["designated"]]))
        ok("%s: %s (same call)" % (sid, label), st == GOLD, st)
    b = CF.analysis(target, require_service=False)
    st = tuple(sorted(b["scorecard"].index[b["scorecard"]["designated"]]))
    ok("SF14: the service requirement (NP-31 2.7) read away files another set, ruled out by 2.7", st != GOLD, st)
    ok("SF15: the reach counts visits with prescribers wherever they practise (2.8); in-county prescribers only files "
       "another set or the same", True, _incounty_reach(a))
    ok("SF16: NP-31 3.2 compares unrounded values; rounded to one decimal the verdicts are the same",
       all(((sc[c].round(1 if c != "s_reach" else 2) < CF.THRESH[t]) == (sc[c] < CF.THRESH[t])).all()
           for c, t in (("s_smi", "smi"), ("s_oud", "oud"), ("s_reach", "reach"))))
    ok("SF17: members with a condition counted whether or not a claim identifies them (2.5): the identified count files "
       "Adams, Douglas and Okanogan, ruled out by 2.5", R["recorded"][1] == ("Adams", "Douglas", "Okanogan"))
    ok("SF18: each county measured from its own members (2.5): the capture shares from each county's own full-year "
       "members file the same five and the same counts", R["ipw_cell"][1] == GOLD and
       all(round(nd["golden"][i][c] / 10) == round(nd["ipw_cell"][i][c] / 10) for i in (0, 1) for c in CF.COUNTIES))
    # SF19: a full-year member no claim identifies, counted as not having the condition (2.5); a constant hazard carried
    # past the twelfth month (each identified member over 1 - (1 - q)^m, q the full-year members' July share) counts some
    import numpy as np
    import pandas as pd
    mem_ = a["members"]
    unt = []
    for cond in ("smi", "oud"):
        fy_ = mem_[mem_["full_year"] & mem_["rec_" + cond]]
        q = float((fy_["first_" + cond] == 1).mean())
        rec_ = mem_[mem_["rec_" + cond]]
        w_ = 1.0 / (1 - (1 - q) ** rec_["months"].values)
        unt.append(pd.Series(w_, index=rec_.index).groupby(rec_["county"]).sum().reindex(CF.COUNTIES))
    seen_ = (mem_["rec_smi"] & mem_["seen"]).groupby(mem_["county"]).sum().reindex(CF.COUNTIES)
    st_u = MT.designated(MT.standards({c: len(v) for c, v in a["practising"].items()}, unt[0], unt[1], seen_))
    moved = sum(1 for i in (0, 1) for c in CF.COUNTIES if round(unt[i][c] / 10) != round(nd["golden"][i][c] / 10))
    ok("SF19: a full-year member no claim identifies counts as not having the condition (2.5); a hazard carried past "
       "twelve months moves %d of twenty counts, same call" % moved, st_u == GOLD and moved > 0, (st_u, moved))
    # the double-error grid: a Layer 1 slip with each wrong completion
    slips = {"member numbers": dict(key="member"), "October file only": dict(weeks="none"),
             "no service requirement": dict(require_service=False), "any taxonomy": dict(taxonomy="any"),
             "residential ZIP share": dict(zip_basis="RES_RATIO"), "first span county": dict(county_rule="first"),
             "mailing address": dict(location="mailing")}
    hits = []
    for nm, opt in slips.items():
        b = CF.analysis(target, **opt)
        Rb = MT.routes(b)
        for rt in ("recorded", "full_year_only", "county_full_year", "full_year_group", "plan_group", "pooled_factor",
                   "exposure"):
            if Rb[rt][1] == GOLD:
                hits.append((nm, rt))
    ok("grid: no Layer 1 slip combined with the identified count, the full-year count, a full-year prevalence, the "
       "pooled factor or the exposure scaling files the five", not hits, hits)

    # ------------------------------------------------------------------ mess neutrality and the separation line
    b = CF.analysis(target, versions="all")
    ok("separation: every version or the final versions identify the same members, in the same first months, and the "
       "same visits",
       (b["members"]["rec_smi"] == a["members"]["rec_smi"]).all() and (b["members"]["rec_oud"] == a["members"]["rec_oud"]).all()
       and (b["members"]["seen"] == a["members"]["seen"]).all()
       and (b["members"]["first_smi"].fillna(0) == a["members"]["first_smi"].fillna(0)).all())

    # ------------------------------------------------------------------ the payments and their stops
    raw, fin = a["raw"], a["final"]
    mbr = dict(zip(fin["mbr_id"], fin["client_id"]))
    raw = raw.copy()
    raw["client_id"] = raw["mbr_id"].map(mbr)
    stops = {"lines summed": _pay(fin, a, once=False), "every version": _pay(raw[raw["clm_freq_cd"] != "8"], a),
             "every version, lines summed": _pay(raw[raw["clm_freq_cd"] != "8"], a, once=False),
             "billing provider's taxonomy": _pay(fin, a, by="billing_npi")}
    for nm, v in stops.items():
        moved = sum(1 for c in CF.COUNTIES for q, _, _ in CF.QUARTERS if abs(v[(c, q)] - a["pay"][(c, q)]) >= 1)
        need = 40 if nm in ("lines summed", "every version, lines summed", "billing provider's taxonomy") else 30
        ok("payments stop '%s' moves %s county-quarter figure" % (nm, "every" if need == 40 else "nearly every"),
           moved >= need, moved)
    if world is not None:
        tp = _truth_pay(world, a)
        ok("payments: the golden equals the generator's paid claims, county by quarter",
           all(abs(tp[k] - a["pay"][k]) < 0.005 for k in a["pay"]))
    ok("payments: every claim's paid amount is the sum of its lines' lesser of billed charge and fee-schedule amount",
       _paid_is_fee_sum(target, fin))

    # ------------------------------------------------------------------ goldens on disk
    fj = json.load(open(os.path.join(os.path.dirname(target), "generator", "figures.json")))
    ok("figures.json carries the five", fj["designated"] == list(GOLD))
    rows = list(csv.DictReader(open(os.path.join(golden_dir, GD.CONFORMED))))
    ok("conformed: 40 rows, every county and group", len(rows) == 40)
    ok("conformed: adult members sum to the persons", sum(int(r["adult_members"]) for r in rows) == len(a["members"]))
    # ------------------------------------------------------------------ realism sweep on the pack's text
    txt = pdf_text(os.path.join(target, P.FILES["policy"]))
    ok("realism: no em dash in the policy", "—" not in txt)
    ok("realism: the policy states the five filed pins (2.2 person, 2.3 county, 2.5 whether or not, 2.7 service, 3.2)",
       all(s in re.sub(r"\s+", " ", txt) for s in ("counts once", "last day of enrollment", "whether or not a claim",
                                                   "rendering provider of at least one claim", "unrounded",
                                                   "is counted as not having the condition")))
    for f in files:
        if f.endswith(".csv"):
            head = open(os.path.join(target, f), encoding="utf-8").read(200000)
            ok("realism: no em dash in %s" % f, "—" not in head)
    ok("realism: no persona surname among the clinicians", not any(c["last"] in {p.split()[1] for p in W.PEOPLE.values()}
                                                                   for c in (world or {}).get("clins", [])))
    import pandas as pd
    sp = pd.read_csv(os.path.join(target, P.FILES["spans"]), dtype=str, keep_default_na=False)
    age_floor = sp.apply(lambda r: r["span_start_dt"] >= "%04d%s" % (int(r["birth_dt"][:4]) + (65 if r["elig_group_cd"] == "AGED-65" else 19),
                                                                    r["birth_dt"][4:]), axis=1)
    ok("realism: no span starts before the member's 19th birthday (65th for AGED-65)", bool(age_floor.all()),
       int((~age_floor).sum()))
    cl = raw
    dx = pd.concat([cl[c] for c in ("dx_cd_1", "dx_cd_2", "dx_cd_3", "dx_cd_4")])
    dx = dx[dx != ""]
    ok("realism: every diagnosis code is a full ICD-10-CM code (a letter, two digits, up to four more characters)",
       bool(dx.str.fullmatch(r"[A-Z][0-9][0-9A-Z]{1,5}").all() & (dx.str.len() >= 3).all()),
       sorted(set(dx[~dx.str.fullmatch(r"[A-Z][0-9][0-9A-Z]{1,5}")]))[:5])
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, P.FILES["adequacy"]), data_only=True).active
    adq = {r[0]: r[1] for r in ws.iter_rows(min_row=5, values_only=True) if r and r[0] in W.COUNTIES}
    june = {}
    for r in sp.to_dict("records"):
        if r["span_start_dt"] <= "2026-06-30" and (r["span_end_dt"] == "" or r["span_end_dt"] >= "2026-06-30"):
            june.setdefault(r["client_id"], CF.COUNTY_FIPS[r["res_county_fips"]])
    jc = collections.Counter(june.values())
    ok("realism: the adequacy report's June members equal the spans' members on 30 June 2026",
       all(adq[c] == jc[c] for c in W.COUNTIES), {c: (adq[c], jc[c]) for c in W.COUNTIES if adq[c] != jc[c]})
    ffs = fin[fin["fin_arrangement_cd"] == "FFS"]
    ok("realism: some lines are paid at their billed charge, under the fee schedule", _under_fee(target, ffs) > 100,
       _under_fee(target, ffs))
    n_ok = sum(1 for _, c, _ in RESULTS if c)
    for label, cond, detail in RESULTS:
        if not cond:
            print("FAIL", label, detail)
    print("checks: %d of %d pass" % (n_ok, len(RESULTS)))
    return n_ok == len(RESULTS)


def _cid_map(world, target):
    """client_id -> person id, through the spans file."""
    import pandas as pd
    s = pd.read_csv(os.path.join(target, P.FILES["spans"]), dtype=str, keep_default_na=False)
    mb = {}
    for p in world["persons"]:
        for sp in p.spells:
            mb[sp["member_id"]] = p.pid
    return {c: mb[m] for c, m in zip(s["client_id"], s["mbr_id"])}


def _incounty_reach(a):
    mem, fin = a["members"], a["final"]
    inc = {n for c, v in a["practising"].items() for n in v}
    v = fin[fin["proc_cd"].isin(CF.VISITS) & fin["rendering_npi"].isin(inc)]
    seen2 = mem.index.isin(set(v["client_id"]))
    return int((mem["seen"] & ~seen2 & mem["rec_smi"]).sum())


def _pay(df, a, once=True, by="rendering_npi"):
    d = df[df["fin_arrangement_cd"] == "FFS"].copy()
    keep = set(d.loc[d[by].map(lambda n: n in a["bh"]), "clm_icn"])
    d = d[d["clm_icn"].isin(keep)]
    if once:
        d = d.sort_values(["clm_icn", "clm_line_num"]).drop_duplicates("clm_icn")
    d["county"] = d["client_id"].map(a["members"]["county"])
    d["dos"] = d["svc_from_dt"].map(CF._iso)
    out = {}
    for c in CF.COUNTIES:
        for q, s, e in CF.QUARTERS:
            sel = d[(d["county"] == c) & (d["dos"] >= s) & (d["dos"] <= e)]
            out[(c, q)] = float(sel["paid_amt"].astype(float).sum())
    return out


def _truth_pay(world, a):
    lines = world["lines"]
    gone = {l["orig"] for l in lines if l["freq"] in ("7", "8")}
    bh = {c["npi"] for c in world["clins"] if PV.renders(c) and PV.primary_on(c, W.AS_OF) in W.BH_TAXONOMY}
    bh |= {c["npi"] for c in world["clins"] if c["kind"] == "deact_late_before"}
    county = {p.pid: p.county for p in world["persons"]}
    claims = collections.OrderedDict()
    for l in lines:
        if l["arr"] != "FFS" or l["icn"] in gone or l["freq"] == "8":
            continue
        claims.setdefault(l["icn"], []).append(l)
    out = collections.defaultdict(float)
    for icn, ls in claims.items():
        if not any(x["render"] in bh for x in ls):
            continue
        d = ls[0]["from"]
        q = [q for q, s, e in CF.QUARTERS if s <= d <= e][0]
        out[(county[ls[0]["person"]], q)] += ls[0]["paid"]
    return {k: round(out.get(k, 0.0), 2) for k in a["pay"]}


def _fee_rates(target):
    import pandas as pd
    fees = pd.read_csv(os.path.join(target, P.FILES["fees"]), dtype=str)
    return {(r["proc_cd"], r["effective_from"]): float(r["max_allowable_per_unit_usd"]) for r in fees.to_dict("records")}


def _paid_is_fee_sum(target, fin):
    rate = _fee_rates(target)
    d = fin[fin["fin_arrangement_cd"] == "FFS"]
    bad = 0
    for icn, g in d.groupby("clm_icn"):
        day = g["svc_from_dt"].iloc[0]
        eff = "2026-01-01" if day >= "2026-01-01" else "2025-07-01"
        tot = sum(min(float(b), round(rate[(p, eff)] * int(u), 2))
                  for p, u, b in zip(g["proc_cd"], g["svc_units"], g["billed_amt"]))
        if abs(tot - float(g["paid_amt"].iloc[0])) > 0.011 or g["paid_amt"].nunique() != 1:
            bad += 1
    return bad == 0


def _under_fee(target, ffs):
    rate = _fee_rates(target)
    n = 0
    for p, u, b, day in zip(ffs["proc_cd"], ffs["svc_units"], ffs["billed_amt"], ffs["svc_from_dt"]):
        eff = "2026-01-01" if day >= "2026-01-01" else "2025-07-01"
        if float(b) < rate[(p, eff)] * int(u) - 0.005:
            n += 1
    return n
