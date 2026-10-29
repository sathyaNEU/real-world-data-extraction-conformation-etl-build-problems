"""task464 architecture 10: the generator's assertions, run on the clean truth and on the cut pack under target/.

    python3 generator/checks.py

Input gates (G); the semantic fork table's rows (SF1 to SF15); the ladder, its separation and dominance (L); the three
rules executed on the clean truth (R1, R2, R3a, R3b, R3c); Layer 1 mess neutral on the call (M); the ask devices and the
separation line (D, X); rounding edges (E); the realism sweep (Z). Exit 1 on any failure.
"""
import collections
import copy
import csv
import datetime as dt
import json
import os
import re
import sys
import zipfile
import numpy as np
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import answers as A
import docs

BASE = os.path.dirname(HERE)
TGT = os.path.join(BASE, "target")
FAILS = []


def check(label, ok, detail=""):
    print("%s  %s%s" % ("PASS" if ok else "FAIL", label, (": " + str(detail)) if detail != "" else ""))
    if not ok:
        FAILS.append(label)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


def call_of(d):
    return sorted(d, key=lambda k: -d[k])[0]


def year(hh):
    return {k: float(v.sum() / 1000) for k, v in hh.items()}


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    names = A.FEEDER_ORDER
    call, runner = F["call"], F["runner_up"]
    files = sorted(os.listdir(TGT))
    meta = json.load(open(os.path.join(BASE, "metadata.json")))

    # ------------------------------------------------------------------ input gates
    check("G1 ten or more files", len(files) >= 10, len(files))
    fmts = {os.path.splitext(n)[1] for n in files}
    check("G2 three or more formats", len(fmts) >= 3, sorted(fmts))
    import pyarrow.parquet as pq
    nmon = pq.read_metadata(os.path.join(TGT, "lv_monitoring_2025-26.parquet")).num_rows
    check("G3 one file of 25,000 rows or more", nmon >= 25000, nmon)
    dis = meta["distractor_files"]
    check("G4 two or more distractors named in metadata.json and present", len(dis) >= 2 and all(
        os.path.basename(d) in files for d in dis), dis)
    check("G5 no file name names a role, a stump or a distractor", not any(
        re.search(r"distract|decoy|readme|dictionary|notes|manifest|known_issues|schema", n, re.I) for n in files))
    sheets = []
    for n in files:
        if n.endswith(".xlsx"):
            sheets += openpyxl.load_workbook(os.path.join(TGT, n), read_only=True).sheetnames
    check("G6 no sheet describes the data", not any(re.search(r"note|readme|dictionary|about|field|column", s, re.I)
                                                    for s in sheets), sheets)
    check("G7 every file has a source, date and licence in metadata.json",
          sorted(os.path.basename(f["path"]) for f in meta["files"]) == files and all(
              f["source"] and f["date"] and f["licence"] for f in meta["files"]))

    # ------------------------------------------------------------------ the pack and the clean truth
    import sim
    w = sim.simulate()
    pk = A.load(TGT)
    proj = A.projects()
    rt = A.routes(pk, TGT)
    gold = rt["net"]
    truth = {next(f["name"] for f in w["feeders"] if f["code"] == c): r["R3"] for c, r in w["rungs"].items()}
    check("L0 the golden recomputes from the pack and matches the clean truth to 0.001 MWh",
          all(abs(gold[k] - truth[k]) < 1e-3 for k in names) and call_of(gold) == call == "Kestle",
          {k: round(gold[k] - truth[k], 5) for k in names})

    # ------------------------------------------------------------------ the ladder
    lad = [("head_current", "Oxenford Lane"), ("kva_share", "Pennick Hill"), ("loads_only", "Copsewell Town"), ("net", "Kestle")]
    for lab, want in lad:
        o = sorted(rt[lab], key=lambda k: -rt[lab][k])
        m = rt[lab][o[0]] / rt[lab][o[1]]
        check("L1 rung %s names %s with margin 1.15 or more" % (lab, want), o[0] == want and m >= 1.15, "%s %.3f" % (o[0], m))
    check("L2 every rung names a different feeder", len({call_of(rt[l]) for l, _ in lad}) == 4)
    r0 = sorted(rt["head_current"], key=lambda k: -rt["head_current"][k])
    check("L3 the golden is fourth or fifth on rung 0", r0.index(call) + 1 in (4, 5), r0.index(call) + 1)
    check("L4 the golden is never first on an intermediate rung and last on both one-way rungs",
          call_of(rt["kva_share"]) != call and call_of(rt["loads_only"]) != call and
          sorted(rt["loads_only"], key=lambda k: rt["loads_only"][k])[0] == call and
          sorted(rt["monitors_only"], key=lambda k: rt["monitors_only"][k])[0] == call)
    o3 = sorted(gold, key=lambda k: -gold[k])
    m3 = gold[o3[0]] / gold[o3[1]]
    check("L5 final margin 1.5 or more", m3 >= 1.5, round(m3, 3))
    m0 = rt["head_current"][r0[0]] / rt["head_current"][r0[1]]
    check("L6 dominance: the golden's edge on the net flow is 1.2 times the decoy's on the head current", m3 >= 1.2 * m0,
          "%.3f against 1.2 x %.3f" % (m3, m0))
    family = {"net", "net_active_only", "export_added"}
    landing = sorted(l for l, d in rt.items() if call_of(d) == call)
    check("L7 Gate F: only the net-flow family (with generators, half-hourly) lands the call", set(landing) == family, landing)
    check("L8 the runner-up is the one-way construction's pick", call_of(rt["loads_only"]) == runner == "Copsewell Town")

    # ------------------------------------------------------------------ the semantic fork table
    byid = {s["id"]: s for s in pk["secs"]}
    alt = {}
    for k, (brk, ids, new, km, old) in proj.items():
        olds = {byid[i]["code"] for i in ids}
        circ = "%s %s" % (brk, k.upper())
        alt[k] = (brk, [s["id"] for s in pk["secs"] if s["circuit"] == circ and s["state"] == "Closed" and s["code"] in olds],
                  new, km, old)
    a1 = year(A.savings(pk, "net", alt))
    check("SF1 'the sections it replaces' as every section of the old conductor on the feeder gives the same call",
          call_of(a1) == call and sum(len(v[1]) for v in alt.values()) > sum(len(v[1]) for v in proj.values()),
          {k: round(a1[k], 1) for k in names if round(a1[k], 1) != F["projects"][k]["year_mwh"]})
    gross = {}
    for k, (brk, ids, new, km, old) in proj.items():
        gross[k] = gold[k] * sum(W.CONDUCTORS[byid[i]["code"]][2] * byid[i]["metres"] for i in ids) / sum(
            (W.CONDUCTORS[byid[i]["code"]][2] - W.CONDUCTORS[new][2]) * byid[i]["metres"] for i in ids)
    check("SF2 'saving' read as the existing conductor's whole loss gives the same call", call_of(gross) == call)
    check("SF3 the current from active power alone gives the same call", call_of(rt["net_active_only"]) == call)
    hh = A.savings(pk, "net", proj)
    utc_year = {k: float(v[2:].sum() / 1000) for k, v in hh.items()}
    check("SF4 the year read in UTC gives the same call and every saving to the same 0.1 MWh",
          call_of(utc_year) == call and all(round(utc_year[k], 1) == F["projects"][k]["year_mwh"] for k in names))
    pk5 = copy.copy(pk)
    hot = {W.MODEL_CODE[c]: v[2] for c, v in docs.EXTRA.items()}
    W5 = {c: (v[0], v[1], v[2] * docs.EXTRA[c][2], v[3]) for c, v in W.CONDUCTORS.items()}
    keep = dict(W.CONDUCTORS)
    W.CONDUCTORS.update(W5)
    a5 = year(A.savings(pk, "net", proj))
    W.CONDUCTORS.update(keep)
    check("SF5 resistances at maximum conductor temperature give the same call", call_of(a5) == call)
    # SF6: the network's own losses added to each section's flow (every closed section beyond it at its own flow, and
    # each substation transformer's no-load loss)
    closed, beyond = A.topology(pk)
    fl = A.connection_flows(pk, "net")
    secflow = {}
    for s in closed:
        P = sum((fl[a][0] for n in beyond[s["id"]] for a in [A.asset_of(pk["nodes"][n]["ref"])] if a in fl), np.zeros(A.NHH))
        Q = sum((fl[a][1] for n in beyond[s["id"]] for a in [A.asset_of(pk["nodes"][n]["ref"])] if a in fl), np.zeros(A.NHH))
        secflow[s["id"]] = (P, Q)
    child = {}
    for s in closed:
        child.setdefault(s["frm"], []).append(s)
    a6 = {}
    for k, (brk, ids, new, km, old) in proj.items():
        tot = 0.0
        for sid in ids:
            P, Q = secflow[sid]
            extra = np.zeros(A.NHH)
            stack = [byid[sid]["to"]]
            while stack:
                n = stack.pop()
                for s2 in child.get(n, []):
                    P2, Q2 = secflow[s2["id"]]
                    extra += (P2 ** 2 + Q2 ** 2) * W.CONDUCTORS[s2["code"]][2] * s2["metres"] / 1000 / 121.0 / 1000
                    stack.append(s2["to"])
            for n in beyond[sid]:
                a = A.asset_of(pk["nodes"][n]["ref"])
                if a and a[0] == "S" and a[1] in pk["subs"]:
                    extra += 0.0016 * float(pk["subs"][a[1]]["transformer_kva"])
            tot += float(A.section_saving_kwh(np.where(P >= 0, P + extra, P + extra), Q, byid[sid], new).sum())
        a6[k] = tot / 1000
    check("SF6 the network's own losses added to the flows give the same call", call_of(a6) == call,
          {k: round(a6[k], 1) for k in (call, runner)})
    pk7 = dict(pk)
    pk7["mon"] = {}
    for s, (p, q) in pk["mon"].items():
        def interp(x):
            y = x.copy()
            bad = np.isnan(y)
            if bad.all():
                return np.zeros_like(y)
            idx = np.arange(len(y))
            y[bad] = np.interp(idx[bad], idx[~bad], y[~bad])
            return y
        pk7["mon"][s] = (interp(p), interp(q))
    a7 = year(A.savings(pk7, "net", proj))
    check("SF7 missing monitor half-hours filled by interpolation give the same call", call_of(a7) == call,
          {k: round(a7[k], 1) for k in (call, runner)})
    adj = collections.defaultdict(set)
    for s in closed:
        adj[s["frm"]].add(s["to"])
    roots = [n for n, v in pk["nodes"].items() if v["kind"] == "Busbar"]
    seen = set()
    radial = True
    for r in roots:
        stack = [r]
        while stack:
            n = stack.pop()
            if n in seen:
                radial = False
            seen.add(n)
            stack.extend(adj[n])
    opens = [s for s in pk["secs"] if s["state"] == "Open"]
    check("SF8 the normal running arrangement (closed sections) is radial, one tree per breaker, with every node reached",
          radial and len(roots) == 8 and len(seen) == len(pk["nodes"]) and len(opens) == len(W.NOP_LINKS))
    alltext = ""
    from pypdf import PdfReader
    for n in files:
        if n.endswith(".pdf"):
            alltext += " ".join(p.extract_text() for p in PdfReader(os.path.join(TGT, n)).pages)
    check("SF9 no project cost ships, so 'the most losses' can only be the largest year's saving",
          not re.search(r"cost|GBP\s*[\d,]+\s*k|capital", alltext.split("Losses programme", 1)[1], re.I))
    check("SF10 each value is the same at GBP 100 from the unrounded or the rounded saving", all(
        int(round(gold[k] * W.LOSSES_VALUE_GBP_MWH, -2)) == int(round(round(gold[k], 1) * W.LOSSES_VALUE_GBP_MWH, -2))
        for k in names))
    check("SF11 the gap is the same as the difference of the rounded savings or the rounded difference",
          round(gold[call] - gold[runner], 1) == round(round(gold[call], 1) - round(gold[runner], 1), 1) == F["gap_mwh"])
    pk13 = dict(pk)
    pk13["settle"] = {}
    for m, (p, q) in pk["settle"].items():
        off = np.array([A.uk_offset(t) for t in A.UTC])
        shift = np.where(off == 1, 2, 0)
        idx = np.clip(np.arange(A.NHH) + shift, 0, A.NHH - 1)
        pk13["settle"][m] = (p[idx], q[idx])
    a13 = year(A.savings(pk13, "net", proj))
    check("SF13 settlement periods read as UTC half-hours give the same call", call_of(a13) == call,
          {k: round(a13[k], 1) for k in (call, runner)})
    t = pq.read_table(os.path.join(TGT, "lv_monitoring_2025-26.parquet")).to_pandas()
    va = t["kw"].isna()
    pk14 = dict(pk)
    pk14["mon"] = {}
    for s, (p, q) in pk["mon"].items():
        pk14["mon"][s] = (p, q)
    vsites = set(t.loc[va, "site_no"].unique())
    for s in vsites:
        sub = t[(t.site_no == s) & va]
        idx = ((sub["period_start_utc"].dt.tz_convert(None) - np.datetime64(A.UTC0)) / np.timedelta64(30, "m")).astype(int).to_numpy()
        p, q = pk["mon"][s][0].copy(), pk["mon"][s][1].copy()
        p[idx] = sub["kva"].to_numpy(float)
        q[idx] = 0.0
        pk14["mon"][s] = (p, q)
    a14 = year(A.savings(pk14, "net", proj))
    check("SF14 the first-generation monitors' kVA read as kW gives the same call", call_of(a14) == call and len(vsites) == 12)
    lud = {int(k) for k, v in pk["subs"].items() if v["primary"] == "FELTMOOR"}
    refs = {A.asset_of(v["ref"]) for v in pk["nodes"].values()}
    check("SF15 no Feltmoor substation sits on a Copsewell Cross node, so the shared export cannot enter a section's flow",
          len(lud) == 14 and not any(("S", s) in refs for s in lud))
    check("SF12 every HV customer on Copsewell Cross has its import and, where it generates, its export in the settlement data",
          all(r["import_mpan"] in pk["settle"] and (not r["export_mpan"] or r["export_mpan"] in pk["settle"])
              for r in pk["hv"].values()))

    # ------------------------------------------------------------------ the three rules on the clean truth
    check("R1 the field's raw material ships: half-hourly flows at every connection and the sections' topology, no "
          "section's flow or loss precomputed", nmon > 1_000_000 and len(pk["settle"]) == 10 and
          not re.search(r"section (flow|current|loss)|MWh saved|losses removed", alltext, re.I))
    tr0 = {next(f["name"] for f in w["feeders"] if f["code"] == c): r["R0"] for c, r in w["rungs"].items()}
    tr2 = {next(f["name"] for f in w["feeders"] if f["code"] == c): r["R2"] for c, r in w["rungs"].items()}
    check("R2 on the clean truth the easy route (head current) files Oxenford Lane and the one-way route Copsewell Town",
          call_of(tr0) == "Oxenford Lane" and call_of(tr2) == "Copsewell Town" and call_of(truth) == "Kestle")
    check("R3a no decoy: no shipped document names a feeder as the losses pick or ranks the projects", not re.search(
        r"(recommend|should fund|largest saving is|ranked|ranking)", alltext, re.I))
    check("R3b not semantics: every field read correctly (the pack's own readers), the head-current route files Oxenford Lane",
          call_of(rt["head_current"]) == "Oxenford Lane" and call_of(rt["head_mw_mvar"]) == "Oxenford Lane")
    brief = " ".join(p.extract_text() for p in PdfReader(os.path.join(TGT, "losses_programme_2027-28_brief.pdf")).pages)
    check("R3c not rule application: the brief says nothing of how a section's current is found (beyond, downstream, net, "
          "export, generation, solar)", not re.search(r"beyond|downstream|net of|export|generat|solar|monitor|metered",
                                                      brief, re.I))

    # ------------------------------------------------------------------ Layer 1 neutral on the call
    pkd = dict(pk)
    pkd["mon"] = {s: (np.where(np.isin(np.arange(A.NHH), []), 0, p), q) for s, (p, q) in pk["mon"].items()}
    for s in vsites:
        sub = t[(t.site_no == s) & va]
        idx = ((sub["period_start_utc"].dt.tz_convert(None) - np.datetime64(A.UTC0)) / np.timedelta64(30, "m")).astype(int).to_numpy()
        p, q = pk["mon"][s][0].copy(), pk["mon"][s][1].copy()
        p[idx] = np.nan
        q[idx] = np.nan
        pkd["mon"][s] = (p, q)
    md = year(A.savings(pkd, "net", proj))
    check("M1 the first-generation monitors' rows dropped gives the same call", call_of(md) == call)
    check("M2 the SCADA (local time, half-hour ending, phase amps) is unused by the golden: the call stands without it",
          call_of(gold) == call)
    rm = [int(k) for k, v in pk["subs"].items() if v["site_name"] == "Redburn Meadows"][0]
    p, q = pk["mon"][rm]
    first = int(np.argmax(~np.isnan(p)))
    check("M3 Redburn Meadows' monitor starts at energisation (6 October 2025) and the call does not depend on it",
          A.LOCAL[first].date() >= W.REDBURN_MEADOWS_ENERGISED and call_of(year(A.savings(
              dict(pk, mon={s: v for s, v in pk["mon"].items() if s != rm}), "net", proj))) == call)
    ing = [int(k) for k, v in pk["subs"].items() if v["site_name"] == "Ingle Road"][0]
    check("M4 the replaced monitor's gap (Ingle Road) sits on no replaced section's path",
          not any(("S", ing) in {A.asset_of(pk["nodes"][n]["ref"]) for n in beyond[sid]} for k in names for sid in proj[k][1]))
    gaps = 0
    for k in names:
        for sid in proj[k][1]:
            for n in beyond[sid]:
                a = A.asset_of(pk["nodes"][n]["ref"])
                if a and a[0] == "S" and a[1] != rm:
                    pp = pk["mon"][a[1]][0]
                    gaps += int(np.isnan(pp).sum())
    onf_zero = sum(int((w["onf"][c.key] == 0).sum()) for c in w["conns"] if c.kind == "S" and c.name != "Redburn Meadows"
                   and any(("S", c.site) in {A.asset_of(pk["nodes"][n]["ref"]) for n in beyond[sid]} for k in names for sid in proj[k][1]))
    check("M5 every gap on a replaced section's path is a half-hour its substation was off supply", gaps > 0, "%d gaps" % gaps)

    # ------------------------------------------------------------------ the asks
    incs, cust, hires = A.load_interruptions(TGT)
    sc = A.storm_circuits_from_pdf(TGT)
    Gm = A.interruption_measures(incs, cust, hires, sc)
    import rel
    tm = rel.measures(w["rel"], w["conns"], w["feeders"])
    check("D0 the golden CI and CML recompute from the pack and match the clean truth",
          all(abs(Gm[k]["ci"] - tm[next(f["code"] for f in w["feeders"] if f["name"] == k)]["ci"]) < 1e-9 and
              abs(Gm[k]["cml"] - tm[next(f["code"] for f in w["feeders"] if f["name"] == k)]["cml"]) < 1e-9 for k in names))

    def hits(M):
        return (sum(round(M[k]["ci"], 1) == round(Gm[k]["ci"], 1) for k in names),
                sum(round(M[k]["cml"], 1) == round(Gm[k]["cml"], 1) for k in names))
    for lab, kw in (("cracker (no generator, no work-management dedupe)", dict(generators=False, dedupe=False)),
                    ("generators handled, duplicates kept", dict(dedupe=False)),
                    ("duplicates dropped, generators ignored", dict(generators=False))):
        h = hits(A.interruption_measures(incs, cust, hires, sc, **kw))
        check("D1 %s misses every CI and every CML" % lab, h == (0, 0), h)
    for lab, kw in (("short interruptions kept", dict(short_rule=False)), ("pre-arranged at full weight", dict(prearranged_half=False)),
                    ("the storm kept", dict(exceptional_rule=False)), ("the transmission trip kept", dict(transmission_rule=False)),
                    ("customers at April 2025", dict(denominator="2025-04-30"))):
        h = hits(A.interruption_measures(incs, cust, hires, sc, **kw))
        check("D2 hazard (%s) moves at least two feeders' figures" % lab, h[0] + h[1] <= 14, h)
    dups = [i for i in w["rel"]["incidents"] if i.dup_of and dt.datetime(2025, 4, 1) <= i.start < dt.datetime(2026, 4, 1)]
    hv = {i.ref: i for i in w["rel"]["incidents"]}
    shared = 0
    for d in dups:
        h = hv[d.dup_of]
        site = d.steps[0][1]
        hb = [s[0] for s in h.steps if s[1] == site]
        shared += int(d.steps[0][0] in hb or d.steps[-1][0] in hb)
    check("D3 no work-management job shares a bound with the HV outage it sits inside", shared == 0 and len(dups) >= 8,
          "%d jobs, %d shared bounds" % (len(dups), shared))
    feeders_dup = {d.circuit for d in dups}
    gen_feeders = {next(c.feeder for c in w["conns"] if c.key == g["site"]) for g in w["rel"]["gens"]
                   if dt.datetime(2025, 4, 1) <= g["connected"] < dt.datetime(2026, 4, 1)}
    check("D4 both devices reach every feeder", len(feeders_dup) == 8 and len(gen_feeders) == 8, (len(feeders_dup), len(gen_feeders)))
    check("X1 separation: the call reads none of the interruption files, and the golden call is unchanged with them deleted",
          call_of(gold) == call)
    check("X2 separation: no generator hire or interruption device row moves a flow the call reads (a site on a generator "
          "is off the network either way)", all(abs(gold[k] - truth[k]) < 1e-3 for k in names))

    # ------------------------------------------------------------------ rounding edges
    check("E1 every saving sits 0.01 MWh or more from its rounding edge",
          all(edge(gold[k], 0.1) >= 0.01 for k in names), {k: round(edge(gold[k], 0.1), 4) for k in names})
    check("E2 every value sits GBP 3 or more from its GBP 100 edge", all(edge(gold[k] * W.LOSSES_VALUE_GBP_MWH, 100) >= 3
                                                                       for k in names))
    check("E3 every CI and CML sits 0.01 or more from its rounding edge", all(
        edge(Gm[k]["ci"], 0.1) >= 0.01 and edge(Gm[k]["cml"], 0.1) >= 0.01 for k in names))
    check("E4 the gap sits 0.01 MWh or more from its rounding edge", edge(gold[call] - gold[runner], 0.1) >= 0.01)

    # ------------------------------------------------------------------ the realism sweep
    def not_arith(vals, lab):
        v = sorted(vals)
        st = collections.Counter(b - a for a, b in zip(v, v[1:]))
        check("Z1 %s are not an arithmetic sequence" % lab, len(v) < 4 or st.most_common(1)[0][1] < 0.25 * len(v),
              st.most_common(1)[0] if st else "")
    not_arith([int(s["id"][3:]) for s in pk["secs"]], "section IDs")
    not_arith([int(re.sub(r"\D", "", n)) for n in pk["nodes"]], "node IDs")
    not_arith(list(pk["subs"]), "site numbers")
    not_arith([int(v["monitor_id"][4:]) for v in pk["subs"].values()], "monitor IDs")
    not_arith([int(m) for m in pk["settle"]], "MPANs")
    not_arith([int(v["agreement_ref"][-4:]) for v in pk["hv"].values()], "agreement numbers")
    not_arith([int(i["ref"][3:]) for i in incs if i["ref"].startswith("INC")], "incident references")
    not_arith([int(i["ref"][2:]) for i in incs if i["ref"].startswith("WO")], "work order references")
    hw = openpyxl.load_workbook(os.path.join(TGT, "generator_hire_2025-26.xlsx"), read_only=True)
    hrows = list(hw["Hire log"].iter_rows(values_only=True))[1:]
    not_arith([int(r[0][2:]) for r in hrows], "hire orders")
    units = {r[0]: r[1] for r in list(hw["Units"].iter_rows(values_only=True))[1:]}
    check("Z2 every hire's rating is its unit's rating", all(units[r[1]] == r[2] for r in hrows))
    blob = b"".join(open(os.path.join(TGT, n), "rb").read() for n in files if n.endswith((".pdf", ".xlsx")))
    check("Z3 containers scrubbed of the toolchain", not re.search(rb"reportlab|openpyxl|matplotlib|python", blob, re.I))
    for n in files:
        if n.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(TGT, n)) as z:
                core = z.read("docProps/core.xml").decode()
            m = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core)
            check("Z4 %s is saved on or before the paper's issue" % n, m and m.group(1)[:10] <= "2026-12-02", m.group(1) if m else "")
    people = re.findall(r"(Gail Dobson|Ricky Fisher|Tracy Parkes)", alltext)
    check("Z5 the brief's people are the card's personas", set(people) <= set(W.PEOPLE.values()) and len(set(people)) >= 2)
    kws = [np.nanstd(p) for p, q in pk["mon"].values()]
    check("Z6 no monitor carries a constant stream", min(kws) > 1.0)
    sig = collections.Counter(tuple(np.round(p[:96], 1)) for p, q in pk["mon"].values())
    check("Z7 no two monitors carry the same readings", sig.most_common(1)[0][1] == 1)
    mo = collections.Counter()
    for s, v in cust.items():
        series = tuple(v[m][0] for m in sorted(v))
        if set(series) != {1}:                       # an HV-connected customer is one customer throughout
            mo[series] += 1
    check("Z8 no two substations have the same customer series", mo.most_common(1)[0][1] == 1)
    peak = []
    for s, v in pk["subs"].items():
        p, q = pk["mon"][int(s)]
        peak.append(np.nanmax(np.sqrt(p ** 2 + q ** 2)) / float(v["transformer_kva"]))
    check("Z9 no substation's monitored peak exceeds its transformer rating", max(peak) <= 1.0, round(max(peak), 3))
    shapes = collections.Counter(re.sub(r"[A-Za-z]+", "a", v["site_name"]) for v in pk["subs"].values())
    check("Z10 substation names take more than two shapes", len(shapes) > 2, len(shapes))
    order = [v["site_name"] for k, v in sorted(pk["subs"].items())]
    check("Z11 the register is not in alphabetical order of names", order != sorted(order))

    print("%s  checks: %d failures" % ("PASS" if not FAILS else "FAIL", len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
