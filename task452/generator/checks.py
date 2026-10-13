"""task452's generator checks: the input gates, every route's slate and margin, the forcing evidence, the Layer 1
items neutral to the call, the three rules executed, the semantic forks' ruling sentences, the asks' bins and devices,
the separation of the asks from the call, the documents and the goldens."""
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import golden as G      # noqa: E402
import pack as P        # noqa: E402
import world as W       # noqa: E402

TASK = os.path.dirname(HERE)
COUNT, FAILS = [0], []
GOLDEN_SLATE = ["Kestle River", "Hessick River", "Varrow Brook"]
DEFAULT_SLATE = ["Varrow Brook", "Orrinwood Brook", "Ambrey River"]
GAP_MIN = 150.0          # kilograms between the third and the fourth on every golden route
EDGE_MIN = 60.0          # kilograms between any golden excess and zero

QUOTES = [
    ("SF1", "agreement", "named for the calendar year in which it ends"),
    ("SF2", "agreement", "at which the tributary's load is measured"),
    ("SF3", "agreement", "phosphorus in all forms in an unfiltered sample of stream water, expressed as P"),
    ("SF4", "agreement", "carried past a tributary's compliance station during a water year, in kilograms"),
    ("SF5", "agreement", "the Commission's samples, the storm samples the"),
    ("SF6", "agreement", "Comparisons under this agreement are made on unrounded loads"),
    ("SF7", "agreement", "exceeds its allocation by the most kilograms"),
    ("SF8", "agreement", "Where fewer than three tributaries exceed their allocations"),
    ("SF9", "program", "Both are reported with their activity type"),
    ("SF10", "program", "Result status is Accepted once a result passes review, or Rejected with the reason in the comment"),
    ("SF11", "transmittal", "The approved values above replace them"),
    ("SF12", "transmittal", "Daily values are means over local calendar days"),
    ("SF13", "program", "whose gage is 4.2 km upstream; the register gives both drainage areas"),
]
BANNED = re.compile(r"rating curve|regression|interpolat|LOADEST|smearing|retransform|flow-weighted|concentration-discharge|"
                    r"\bC-Q\b|load estimat|storm days|base flow|baseflow|representative", re.I)


def ok(cond, msg):
    COUNT[0] += 1
    if cond:
        print("ok    " + msg)
    else:
        print("FAIL  " + msg)
        FAILS.append(msg)


def text_of(path):
    if path.endswith((".csv", ".txt")):
        return open(path, encoding="utf-8", errors="replace").read()
    if path.endswith(".pdf"):
        from pypdf import PdfReader
        return "\n".join(p.extract_text() for p in PdfReader(path).pages)
    if path.endswith(".docx"):
        import docx
        return "\n".join(p.text for p in docx.Document(path).paragraphs)
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        return "\n".join(" ".join(str(v) for v in r if v is not None) for ws in wb.worksheets for r in ws.iter_rows(values_only=True))
    return ""


def gap(loads, A):
    top, ex = C.slate(loads, A)
    srt = sorted(ex, key=lambda k: -ex[k])
    return top, ex[srt[2]] - ex[srt[3]]


def run(target, golden, world=None, meta_path=None):
    names = sorted(os.listdir(target))
    texts = {n: text_of(os.path.join(target, n)) for n in names}
    meta = json.load(open(meta_path or os.path.join(TASK, "metadata.json")))
    X = G.compute(target)
    L, A, R = X["L"], X["A"], X["R"]
    # ------------------------------------------------------------------ input gates
    ok(len(names) >= 10, "ten or more files (%d)" % len(names))
    ok(len({n.rsplit(".", 1)[1] for n in names}) >= 3, "three or more formats")
    ok(len(L["uv"]) >= 25000, "the spine has 25,000 rows or more (%d)" % len(L["uv"]))
    tu = pd.to_datetime(L["uv"]["datetime_utc"])
    steps = tu.groupby(L["uv"]["gage_id"]).apply(lambda s: set((s.sort_values().diff().dropna() / pd.Timedelta(minutes=1)).astype(int)))
    ok(all(x == {15} for x in steps) and not tu.groupby(L["uv"]["gage_id"]).apply(lambda s: s.duplicated().any()).any(),
       "every gage's 15-minute record runs in UTC without a gap or a repeat, the clock changes included")
    ok(len(meta["distractor_files"]) >= 2 and all(d in names for d in meta["distractor_files"]), "two or more distractors named in metadata.json")
    ok(not any("distractor" in n.lower() for n in names), "no file name says distractor")
    ok(sorted(names) == sorted(P.FILES.values()), "the pack is exactly the files the generator names")

    # ------------------------------------------------------------------ the call and every route
    for nm in C.ROUTES:
        top, g = gap(R[nm], A)
        if nm in C.GOLDEN:
            ok(sorted(top) == sorted(GOLDEN_SLATE), "%s funds %s" % (nm, ", ".join(top)))
            ok(g >= GAP_MIN, "%s: the third stands %.0f kg above the fourth" % (nm, g))
        elif nm == C.DEFAULT:
            ok(sorted(top) == sorted(DEFAULT_SLATE), "%s funds %s" % (nm, ", ".join(top)))
            ok(g >= GAP_MIN, "%s: the third stands %.0f kg above the fourth" % (nm, g))
        else:
            ok(sorted(top) != sorted(GOLDEN_SLATE), "%s funds %s, not the golden three" % (nm, ", ".join(top)))
    ok(len(set(A.values())) == len(A), "no two allocations equal")
    for nm in C.GOLDEN:
        e = {k: R[nm][k] - A[k] for k in A}
        k0 = min(e, key=lambda k: abs(e[k]))
        ok(abs(e[k0]) >= EDGE_MIN, "%s: no excess within %.0f kg of zero (nearest %s, %.1f)" % (nm, EDGE_MIN, k0, e[k0]))
        ok(sum(v > 0 for v in e.values()) >= 3, "SF8 %s: %d tributaries exceed, so three are funded" % (nm, sum(v > 0 for v in e.values())))
    ok(sorted(C.slate({k: round(v, -1) for k, v in R[C.GOLD].items()}, A)[0]) == sorted(GOLDEN_SLATE),
       "SF6 loads rounded to 10 kg before the comparison: same call")
    share = {k: (R[C.GOLD][k] - A[k]) / A[k] for k in A}
    ok(sorted(sorted(share, key=lambda k: -share[k])[:3]) == sorted(GOLDEN_SLATE), "SF7 the largest share above allocation: same call")

    # ------------------------------------------------------------------ the forcing evidence
    samples, q = C.tp_samples(L), C.daily_q(L)
    for n in W.NAME.values():
        b = X["info"][n]["beta"][1]
        ok(b >= 0.25, "%s: concentration rises with discharge (log slope %.2f)" % (n, b))
    share_load, share_samp = [], []
    for n in W.NAME.values():
        qd = np.array([q[n][d] for d in C.WY26])
        q90 = np.quantile(qd, 0.9)
        A_ = X["info"][n]["beta"]
        s26 = [d for d, c in samples[n] if W.WY26_START <= d <= W.WY_END]
        share_samp.append(np.mean([q[n][d] > q90 for d in s26]))
    ok(max(share_samp) <= 0.25, "no station has more than a quarter of its water year 2026 samples on its top tenth of flows (%.2f)" % max(share_samp))
    F_ = G.figures(X)
    for n in ("Kestle River", "Hessick River"):
        ok(F_["top_tenth_load_pct"][n] >= 55 and F_["top_tenth_samples_pct"][n] <= 5,
           "%s: its top tenth of days carry %d%% of the load and %d%% of the samples" % (n, F_["top_tenth_load_pct"][n], F_["top_tenth_samples_pct"][n]))

    # ------------------------------------------------------------------ R2: the Layer 1 items neutral to the call
    def call_with(samples_=None, q_=None):
        s_, qq = samples_ or samples, q_ or q
        loads = {n: C.rating(s_[n], qq[n], C.WY26)[0] for n in s_}
        return sorted(C.slate(loads, A)[0])
    ok(call_with(samples_=C.tp_samples(L, accepted_only=False, routine_only=False)) == sorted(GOLDEN_SLATE),
       "R2 quality-control replicates, blanks and rejected results kept: same call")
    ok(call_with(q_=C.daily_q(L, local=False)) == sorted(GOLDEN_SLATE), "R2 daily means on UTC days: same call")
    reg = C.register(L)
    commission = dict(L, wq=L["wq"][L["wq"]["MonitoringLocationIdentifier"].isin({r["st"] for r in reg.values()})])
    Rc, _ = C.route_loads(commission, q=q)
    for nm in C.GOLDEN:
        ok(sorted(C.slate(Rc[nm], A)[0]) == sorted(GOLDEN_SLATE), "SF5 %s on the Commission's samples alone: same call" % nm)
    ok(call_with(q_=C.daily_q(L, ratio=False)) == sorted(GOLDEN_SLATE), "R2 Dunmarsh Brook without the drainage-area ratio: same call")
    prov = pd.read_csv(os.path.join(target, P.FILES["prov"]), comment="#", dtype={"gage_id": str, "qualifiers": str})
    t = pd.to_datetime(L["uv"]["datetime_utc"])
    uvp = pd.concat([L["uv"][~(t >= "2026-07-01 04:00")], prov])
    ok(call_with(q_=C.daily_q(L, uv=uvp)) == sorted(GOLDEN_SLATE), "R2 the provisional July to September discharge: same call")

    # ------------------------------------------------------------------ R3: the three rules executed
    ok(sorted(X["slates"][C.DEFAULT]) != sorted(GOLDEN_SLATE),
       "R3a the default path (every filed rule applied, samples interpolated across the year) funds %s" % ", ".join(X["slates"][C.DEFAULT]))
    ok(sorted(X["slates"][C.GOLD]) == sorted(GOLDEN_SLATE), "R3b the same path with only the day's concentration taken from the rating curve funds the golden three")

    # ------------------------------------------------------------------ semantic forks
    for sf, doc, qt in QUOTES:
        tx = re.sub(r"\s+", " ", texts[P.FILES[doc]].replace("\n", " "))
        ok(re.sub(r"\s+", " ", qt) in tx, "%s ruling sentence present in %s" % (sf, P.FILES[doc]))

    # ------------------------------------------------------------------ the asks
    ww, cov = X["ww"], X["cover"]
    crackers = {
        "Ask A, the receiving-water name join": (C.ask_wastewater(L, "name"), ww),
        "Ask A, each report times the days in its end month": (C.ask_wastewater(L, days="month"), ww),
        "Ask B, each line's contracted acres shared by the overlay": (C.ask_cover(L, "split_contract"), cov),
        "Ask B, each line's contracted acres under its watershed": (C.ask_cover(L, "label_latest"), cov),
        "Ask B, each field's own acres under its line's watershed": (C.ask_cover(L, "label_field"), cov),
    }
    for n in W.NAME.values():
        fr = ww[n] / 10 - np.floor(ww[n] / 10)
        ok(abs(fr - 0.5) * 10 >= 2.0, "Ask A %s %.1f kg at least 2 kg from a rounding edge" % (n, ww[n]))
        fr = cov[n] / 10 - np.floor(cov[n] / 10)
        ok(abs(fr - 0.5) * 10 >= 2.0, "Ask B %s %.1f acres at least 2 acres from a rounding edge" % (n, cov[n]))
    for label, (got, gold) in crackers.items():
        hits = [n for n in W.NAME.values() if G.k10(got[n]) == G.k10(gold[n])]
        gaps = [abs(got[n] - gold[n]) for n in W.NAME.values()]
        ok(not hits, "%s misses all ten rows (off by %.0f to %.0f; hits %s)" % (label, min(gaps), max(gaps), hits))
    # the reports cover whole months or whole calendar quarters, the smaller dischargers quarterly
    dm = L["dmr"]
    st_, en_ = pd.to_datetime(dm["MONITORING_PERIOD_START_DATE"]), pd.to_datetime(dm["MONITORING_PERIOD_END_DATE"])
    months = (en_.dt.year - st_.dt.year) * 12 + en_.dt.month - st_.dt.month + 1
    q = dm["PERMIT_ID"].isin(W.QUARTERLY)
    ok((st_.dt.day == 1).all() and ((en_ + pd.Timedelta(days=1)).dt.day == 1).all(), "every report runs from a month's first day to a month's last")
    ok(months[q].eq(3).all() and months[~q].eq(1).all() and st_[q].dt.month.isin([1, 4, 7, 10]).all(),
       "the %d quarterly dischargers report calendar quarters, the rest months" % len(W.QUARTERLY))
    per = dm.drop_duplicates(["PERMIT_ID", "MONITORING_PERIOD_START_DATE", "MONITORING_PERIOD_END_DATE"])
    tiles = per.groupby("PERMIT_ID").apply(lambda g: sorted(m for a, b in zip(pd.to_datetime(g["MONITORING_PERIOD_START_DATE"]),
                                                                              pd.to_datetime(g["MONITORING_PERIOD_END_DATE"]))
                                                            for m in pd.period_range(a, b, freq="M").astype(str)))
    wy = [str(p_) for p_ in pd.period_range("2025-10", "2026-09", freq="M")]
    ok(all(t == wy for t in tiles), "each facility's reports cover every month of the water year exactly once")
    ups = {}
    walk = C.stream_to_tributary(L)
    for pid, fname, rw, rkm, mgd, tp, mode, resub, reloc in W.FACILITIES:
        trib, join = walk(rw)
        if (rkm if join is None else join) > C.register(L)[trib]["rkm"] and pid in W.QUARTERLY:
            ups.setdefault(trib, []).append(pid)
    ok(sorted(ups) == sorted(W.NAME.values()), "every tributary has a quarterly discharger upstream of its station")
    # every contract's acres are its enrolled fields' acres in the overlay, on every amendment
    con, fl = L["contracts"], L["fields"]
    fa = dict(zip(fl["field_id"], fl["field_acres"].astype(float)))
    sums = con.assign(fa=con["field_id"].map(fa)).groupby(["contract_id", "amendment_no"]).agg(ca=("contracted_acres", "first"), fs=("fa", "sum"))
    ok((sums["ca"].astype(float) - sums["fs"]).abs().max() < 0.05 and con.groupby(["contract_id", "amendment_no"])["contracted_acres"].nunique().eq(1).all(),
       "each contract's acres, repeated on its field lines, equal its fields' acres (%d contract versions)" % len(sums))
    multi = con.groupby(["contract_id", "amendment_no"])["field_id"].count().gt(1).sum()
    ok(multi >= 20, "%d contract versions enrol more than one field" % multi)
    shares = fl.assign(s=fl["share_of_field"].astype(float)).groupby("field_id")["s"].sum()
    ok((shares - 1).abs().max() < 1e-9, "every field's shares sum to one")

    # ------------------------------------------------------------------ separation: the asks' files never reach the call
    L2 = dict(L, dmr=None, contracts=None, fields=None, facilities=None, streams=None)
    R2, _ = C.route_loads(L2)
    ok(sorted(C.slate(R2[C.GOLD], A)[0]) == sorted(GOLDEN_SLATE),
       "separation: the call recomputes with the reports, contracts, field mapping, streams and outfalls withheld")

    # ------------------------------------------------------------------ documents
    for n in names:
        if n.endswith(".csv"):
            continue
        hit = BANNED.findall(texts[n])
        ok(not hit, "%s names no estimator or sampling bias (%s)" % (n, hit[:3]))
    for p_ in W.PEOPLE.values():
        ok(any(p_[0] in texts[n] for n in names), "persona %s appears in the pack" % p_[0])
    gd = sorted(os.listdir(golden))
    ok(gd == sorted([G.DOCX, G.CSV]), "the goldens are the two files the prompt names (%s)" % gd)
    print("checks: %d assertions, %d failed" % (COUNT[0], len(FAILS)))
    return not FAILS


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    sys.exit(0 if run(tgt, os.path.join(TASK, "golden")) else 1)
