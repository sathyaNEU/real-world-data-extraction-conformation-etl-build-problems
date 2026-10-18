"""Build task190: cut the pack under target/, the goldens under golden/, and figures.json."""
import collections
import csv
import datetime as dt
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import docs                                       # noqa: E402
import golden as G                                # noqa: E402
import metadata                                   # noqa: E402
import pack                                       # noqa: E402
import postprocess as PP                          # noqa: E402
import sim                                        # noqa: E402
import world as W                                 # noqa: E402

TARGET = os.path.join(TASK, "target")
GOLD = os.path.join(TASK, "golden")
F = {
    "h1": "waste_movement_legs_2026_h1.csv",
    "h2": "waste_movement_legs_2026_h2.csv",
    "y25": "waste_movement_legs_2025.csv",
    "md": "bws_2026_microdata.csv",
    "log": "bws_2026_response_log.csv",
    "cw": "enterprise_permit_crosswalk.csv",
    "codes": "waste_code_crosswalk.csv",
    "fac": "facility_register.csv",
    "ops": "treatment_operation_codes.xlsx",
    "design": "bws_2026_design_and_weighting.pdf",
    "release": "waste_statistics_2025_release.pdf",
    "plan": "national_waste_management_plan_targets.pdf",
    "cap": "collection_capacity_note_2027.pdf",
    "mret": "municipal_waste_returns_2026.csv",
    "mrec": "municipal_facility_receipts_2026.csv",
    "veh": "carrier_permit_vehicle_log_2026.csv",
    "haz": "hazardous_export_notifications_2026.csv",
}
P = {k: os.path.join(TARGET, v) for k, v in F.items()}


def cell(v, what=""):
    """A tonnage total the design fixed, as the register itself adds it up. The weighbridge offsets
    on each class of each stream sum to the residue world.CLASS_RESID hands in rather than to zero,
    so a stream and stage total lands inside the tonne the deliverables print and on neither of its
    edges, and is never a whole number; this is where that is checked rather than assumed."""
    n = int(round(v))
    assert abs(v - n) < 0.45, (what, "outside the printed tonne", v)
    assert abs(v - n) > 1e-9, (what, "a whole tonne, so the register was solved backwards", v)
    return n


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        next(rd)
        return [r for r in rd]


# ------------------------------------------------------------------ the filed construction
def chains(paths):
    ch = collections.defaultdict(list)
    for p in paths:
        for r in rows(p):
            ch[r[0]].append(r)
    for c in ch:
        ch[c].sort(key=lambda r: int(r[1]))
    return ch


def terminal_op(ch, c, kind_of, child_of):
    conf = [x for x in ch[c] if x[2] == "TREATMENT_CONFIRMED"]
    op = conf[0][9] if conf else ""
    if kind_of.get(op) == "interim":
        k = child_of.get(c)
        if k:
            cc = [x for x in ch[k] if x[2] == "TREATMENT_CONFIRMED"]
            op = cc[0][9] if cc else ""
        else:
            op = ""
    return op


def recovered_by_stream(ch, kind_of, code2stream, facility_permits, year, drop_renotified=False):
    child_of = {}
    for c, rs in ch.items():
        par = rs[0][10]
        if par:
            child_of.setdefault(par, c)
    producer_origin = {c for c, rs in ch.items()
                       if [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0][4] not in facility_permits}
    out = collections.Counter()
    for c in producer_origin:
        d = [x for x in ch[c] if x[2] == "PRODUCER_DESPATCH"][0]
        if not d[3].startswith(str(year)):
            continue
        if drop_renotified and d[10] and d[10] in producer_origin:
            continue
        if kind_of.get(terminal_op(ch, c, kind_of, child_of)) == "recovery":
            out[code2stream[d[7]]] += float(d[8])
    return out


def recovered_at_cut(ch, kind_of, code2stream, facility_permits, year, cut):
    """The register's recovered tonnage for a reference year as it stood at an earlier extract: the
    same chain construction, over the consignments whose terminal confirmation had arrived by the
    cut. What a release compiled at that extract could have published, and the only basis on which
    the column it did publish makes sense."""
    child_of = {}
    for c, rs in ch.items():
        if rs[0][10]:
            child_of.setdefault(rs[0][10], c)
    po = {c for c, rs in ch.items()
          if [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0][4] not in facility_permits}
    out = collections.Counter()
    for c in po:
        d = [x for x in ch[c] if x[2] == "PRODUCER_DESPATCH"][0]
        if not d[3].startswith(str(year)) or (d[10] and d[10] in po):
            continue
        conf = [x for x in ch[c] if x[2] == "TREATMENT_CONFIRMED"]
        if not conf:
            continue
        op, cd = conf[0][9], conf[0][3]
        if kind_of.get(op) == "interim":
            k = child_of.get(c)
            cc = [x for x in ch[k] if x[2] == "TREATMENT_CONFIRMED"] if k else []
            if not cc:
                continue
            op, cd = cc[0][9], cc[0][3]
        if kind_of.get(op) == "recovery" and cd <= cut:
            out[code2stream[d[7]]] += float(d[8])
    return out


def stage_chain(ch, kind_of, code2stream, facility_permits, year, arisings):
    child_of = {}
    for c, rs in ch.items():
        par = rs[0][10]
        if par:
            child_of.setdefault(par, c)
    producer_origin = {c for c, rs in ch.items()
                       if [x for x in rs if x[2] == "PRODUCER_DESPATCH"][0][4] not in facility_permits}
    desp, conf, rec = collections.Counter(), collections.Counter(), collections.Counter()
    for c in producer_origin:
        d = [x for x in ch[c] if x[2] == "PRODUCER_DESPATCH"][0]
        if not d[3].startswith(str(year)):
            continue
        s = code2stream[d[7]]
        t = float(d[8])
        desp[s] += t
        op = terminal_op(ch, c, kind_of, child_of)
        if kind_of.get(op) in ("recovery", "disposal"):
            conf[s] += t
            if kind_of[op] == "recovery":
                rec[s] += t
    return {k: {"arisings": arisings[k], "despatched": cell(desp[k], "despatched " + k),
                "confirmed": cell(conf[k], "confirmed " + k),
                "recovered": cell(rec[k], "recovered " + k)} for k, *_ in W.STREAMS}


def ask_a1(log_rows, region_of):
    """Field days once per field visit; a visit covers several enterprises in one region."""
    days = collections.Counter()
    seen = set()
    ret = collections.Counter()
    for r in log_rows:
        reg = region_of[r[1]]
        fd = float(r[7])
        if r[8] == "h":
            fd = fd / float(W.FIELD_DAY_HOURS)
        if r[5]:
            if r[5] in seen:
                continue
            seen.add(r[5])
        days[reg] += fd
        if r[9] == "usable return":
            ret[reg] += 1
    # the usable-return count is a per-case outcome and carries no visit grain, so it is counted
    # once per collection case: the log holds a re-sent operations batch of exact duplicate rows,
    # and a case that returned is one usable return however many times its row was loaded
    ret = collections.Counter()
    cases = set()
    for r in log_rows:
        if r[9] == "usable return" and r[0] not in cases:
            cases.add(r[0])
            ret[region_of[r[1]]] += 1
    return {reg: {"days": days[reg], "returns": ret[reg], "per_day": ret[reg] / days[reg]}
            for reg in W.REGIONS}


def ask_a3(mret, mrec, authorities):
    col = collections.Counter()
    for r in mret:
        if r[0] in authorities:
            continue
        v = float(r[3])
        col[r[1]] += v / 10.0 if r[4] == "100kg" else v
    rcv = collections.Counter()
    for r in mrec:
        rcv[r[3]] += float(r[4])
    out = {}
    for reg in W.REGIONS:
        gap = col[reg] - rcv[reg]
        out[reg] = {"collections": col[reg], "receipts": rcv[reg], "gap": gap,
                    "share": 100.0 * gap / col[reg]}
    return out


def ceiling_deltas(path, P, a1, a2, a3, region_of, kind_of, code2stream, facility_permits, ch25):
    """Per ask figure, whether each response's own reading lands within half the stated rounding unit
    of the golden. The cracker resolves every documented handling and everything the battery finds
    (the unit columns, the dated code revision, the re-sent batch, the permit supersessions), which
    since the collection documentation states the visit grain includes ask A1's grain; the mirror
    takes each ask's lazy stop and resolves the code revision only."""
    log = rows(P["log"])
    out = {"cracker": {}, "mirror": {}}

    def mark(resp, name, got, want, unit):
        out[resp][name] = 0.0 if abs(got - want) < unit / 2.0 else 1.0

    for resolve_units in (True, False):
        resp = "cracker" if resolve_units else "mirror"
        days, ret = collections.Counter(), collections.Counter()
        seen_case = set()
        seen_visit = set()
        for r in log:
            reg = region_of[r[1]]
            fd = float(r[7])
            if r[8] == "h" and resolve_units:
                fd = fd / float(W.FIELD_DAY_HOURS)
            if resolve_units and r[5]:             # the grain the design document now states
                if r[5] in seen_visit:
                    continue
                seen_visit.add(r[5])
            days[reg] += fd
            if r[9] == "usable return":
                # the cracker runs the battery, so it counts a case once; the mirror counts rows
                if resolve_units and r[0] in seen_case:
                    continue
                seen_case.add(r[0])
                ret[reg] += 1
        for reg in W.REGIONS:
            mark(resp, "field days consumed %s" % reg, days[reg], a1[reg]["days"], 0.01)
            mark(resp, "usable returns per field day %s" % reg,
                 ret[reg] / days[reg], a1[reg]["per_day"], 0.01)
        lazy25 = recovered_by_stream(ch25, kind_of, code2stream, facility_permits, 2025)
        for k, *_ in W.STREAMS:
            mark(resp, "2025 confirmed recovery tonnage %s" % k, lazy25[k], a2[k], 1.0)
        col, rcv = collections.Counter(), collections.Counter()
        for r in rows(P["mret"]):                      # the authority returns left in
            v = float(r[3])
            if r[4] == "100kg" and resolve_units:
                v = v / 10.0
            col[r[1]] += v
        for r in rows(P["mrec"]):
            rcv[r[3]] += float(r[4])
        for reg in W.REGIONS:
            gap = col[reg] - rcv[reg]
            mark(resp, "municipal gap %s" % reg, gap, a3[reg]["gap"], 1.0)
            mark(resp, "gap as a share of collections %s" % reg,
                 100.0 * gap / col[reg], a3[reg]["share"], 0.1)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)


def main():
    os.makedirs(TARGET, exist_ok=True)
    os.makedirs(GOLD, exist_ok=True)
    for d in (TARGET, GOLD):
        for f in os.listdir(d):
            os.remove(os.path.join(d, f))

    pop, samp, idx = sim.build_sample()
    att = sim.attainment(samp)
    rng = np.random.default_rng(W.SEED + 7)

    ents, per = pack.build_entities(rng)
    n_md = pack.build_microdata(samp, idx, ents, per, P["md"])
    permit_of, sup_pairs, n_cw = pack.build_crosswalk(ents, rng, P["cw"])
    fac = pack.build_facilities(rng, P["fac"])
    n_h1, n_h2, n_25, att2, renot = pack.build_register(
        samp, ents, permit_of, fac, rng, {"h1": P["h1"], "h2": P["h2"], "y25": P["y25"]}, pop=pop)
    n_log, visits, n_dup = pack.build_response_log(ents, per, permit_of, rng, P["log"])
    n_mret, n_mrec, muni_base = pack.build_municipal(rng, fac, P["mret"], P["mrec"])
    n_codes = pack.build_code_crosswalk(P["codes"])
    n_veh, n_haz = pack.build_distractors(rng, fac, P["veh"], P["haz"])

    # read back from the shipped files and recompute everything the goldens state
    kind_of = {c: k for c, k, _d in pack.OPS}
    code2stream = {r[0]: r[1] for r in rows(P["codes"])}
    facility_permits = {r[0] for r in rows(P["fac"])}
    region_of = {r[0]: r[2] for r in rows(P["cw"])}
    ch26 = chains([P["h1"], P["h2"]])
    rec26 = recovered_by_stream(ch26, kind_of, code2stream, facility_permits, 2026)
    for k, *_ in W.STREAMS:
        assert cell(rec26[k], "recovered " + k) == att[k]["recovered_t"], \
            (k, rec26[k], att[k]["recovered_t"])
    arisings = {k: att[k]["arisings"] for k, *_ in W.STREAMS}
    chain = stage_chain(ch26, kind_of, code2stream, facility_permits, 2026, arisings)
    ch25 = chains([P["y25"]])
    a2raw = recovered_by_stream(ch25, kind_of, code2stream, facility_permits, 2025, drop_renotified=True)
    a2 = {k: cell(a2raw[k], "2025 recovery " + k) for k, *_ in W.STREAMS}
    a2_lazy = recovered_by_stream(ch25, kind_of, code2stream, facility_permits, 2025)
    a1 = ask_a1(rows(P["log"]), region_of)
    authorities = set(pack.AUTHORITY.values())
    a3 = ask_a3(rows(P["mret"]), rows(P["mrec"]), authorities)

    targets = {k: att[k]["target"] for k, *_ in W.STREAMS}
    nat_cv, nat_tot = sim.national_cv(samp)          # the 2026 round's own precision, published nowhere
    cv25, tot25, est25 = sim.round_2025(pop, idx)    # the 2025 round, which the release reports
    # The 2025 release's Table 1. Arisings are the 2025 round's own estimate. Recovered tonnage is
    # the register as it stood at the 30 June 2026 extract the release was compiled from: the
    # consignments whose treatment confirmation had arrived by then. It therefore sits below a
    # recompute on the shipped 2027-01-31 extract by exactly the confirmations the register took in
    # between, which is what the release says explains it, and the register has been amended in the
    # ordinary way since that cut (world.PRIOR_DRIFT), so no recompute reproduces the column.
    cut25 = recovered_at_cut(ch25, kind_of, code2stream, facility_permits, 2025, W.PRIOR_EXTRACT)
    prior = {}
    for k, *_ in W.STREAMS:
        prior[k] = (int(round(est25[k])),
                    int(round(cut25[k] * (1.0 + W.PRIOR_DRIFT[k]))))
    docs.plan_targets(P["plan"], targets)
    docs.sample_design(P["design"], W.ISSUED, {c: r for c, _l, _N, r in W.STRATA})
    docs.release_2025(P["release"], cv25, tot25, prior)
    docs.capacity_note(P["cap"], targets)
    docs.operation_codes(P["ops"])

    gx = os.path.join(GOLD, "recovery_attainment_2026.xlsx")
    gp = os.path.join(GOLD, "attainment_against_target_2026.png")
    G.workbook(gx, att, chain, a1, a2, a3, prior)
    G.chart(gp, att)

    extra = {
        "published_national_cv_pct_2025": round(cv25 * 100, 1),
        "national_arisings_cv_pct_2026": round(nat_cv * 100, 1),
        "survey_usable_returns": n_md,
        "register_legs_2026": n_h1 + n_h2,
        "a2_lazy_total_t": int(sum(a2_lazy.values())),
        "a2_total_t": int(sum(a2.values())),
        "renotified_pairs": len(renot),
        "visits_2026": len(visits),
        "golden_take_all_share_pct": round(100.0 * samp[W.GOLDEN_STREAM][0].sum()
                                           / att[W.GOLDEN_STREAM]["arisings"], 1),
        "streams_examined": len(W.STREAMS),
    }
    figs = G.figures(os.path.join(HERE, "figures.json"), att, chain, a1, a2, a3, extra)
    ceiling_deltas(os.path.join(HERE, "ceiling_deltas.json"), P, a1, a2, a3, region_of,
                   kind_of, code2stream, facility_permits, ch25)
    stated = []
    for k, *_ in W.STREAMS:
        t26 = targets[k] * 100.0
        stated += ["%.1f" % t26, "%.1f" % (t26 + 3.5), "%.1f" % (t26 + 7.0)]
        pa, pr = prior[k]
        stated += ["%d" % pa, "%d" % pr, "%.1f" % (100.0 * pr / pa)]
    pub_tot = sum(a for a, _r in prior.values())      # the total the release prints, its own column's sum
    stated += ["%.1f" % (cv25 * 100), "%d" % pub_tot, "{:,}".format(pub_tot),
               "%d" % W.MODULE_DAYS, "36,735", "36735"]
    for v in (3.0, 2.0, 2.5, 1.0, 1.0):
        stated.append("%.1f" % v)
    stated += ["214", "143", "178", "71", "69"]
    for code, _l, N, r in W.STRATA:
        stated += ["%d" % N, "%d" % W.ISSUED[code], "%d" % W.OUT_OF_SCOPE[code], "%d" % r,
                   "%.6f" % (N / float(r))]
    metadata.write(os.path.join(TASK, "metadata.json"), F, {
        "microdata_rows": n_md, "crosswalk_rows": n_cw, "legs_h1": n_h1, "legs_h2": n_h2,
        "legs_2025": n_25, "log_rows": n_log, "muni_returns": n_mret, "muni_receipts": n_mrec,
        "code_rows": n_codes, "vehicle_rows": n_veh, "hazardous_rows": n_haz,
        "facilities": len(fac)}, stated_figures=sorted(set(stated)))

    PP.normalize_all(TARGET, GOLD)

    print("target/: %d files" % len(os.listdir(TARGET)))
    print("  legs h1 %d, h2 %d, 2025 %d; microdata %d; log %d; crosswalk %d"
          % (n_h1, n_h2, n_25, n_md, n_log, n_cw))
    print("  call: %s, rate %.1f%%, target %.1f%%, shortfall %.1f pp, z %.2f"
          % (figs["call"], figs["call_rate_pct"], figs["call_target_pct"],
             figs["call_shortfall_pp"], figs["call_z"]))
    print("  established: %s" % ", ".join(figs["established_streams"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
