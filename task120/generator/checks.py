"""The build's assertion regime (DESIGN_NOTE.md, Assertion plan, plus the house-fix checks).
Everything here reads the files as written, except the world-level facts only the generator sees.
Assertion names carry the plan's number: m01..m33 main call, a34..a47 ask layer, p48..p52 pack,
h* house fixes."""
import itertools
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd
import pyarrow.parquet as pq
from pypdf import PdfReader

import askcheck as AC
import calib
import constructions as C
import world as Wm
from common import (PCTS, YEARS, floor_conventions, k_top, round_thousand)

ANSWER = (214_000, 318_000, 742_000)
STOP = (197_000, 293_000, 594_000)
RUNG3 = (214_000, 318_000, 657_000)
K_HH = (58_255, 29_128, 5_826)
K_FFU = (67_736, 33_868, 6_774)


def read_returns(p):
    df = pd.read_parquet(p)
    df["spouse_tin"] = df.spouse_tin.fillna(0).astype(np.int64)
    df["processed_date"] = pd.to_datetime(df.processed_date)
    return df


def floors_of(u):
    return [round_thousand(x) for x in C.nearest_rank_floors(u.agi)]


def run_all(K, W, R, S, A, app, pub, tgt, root, FILES, DISTRACTORS, skip_slow=False):
    rec = {}
    RS = {y: read_returns(tgt / FILES["returns"].format(y=y)) for y in YEARS}
    SS = {y: pd.read_parquet(tgt / FILES["sched"].format(y=y)) for y in YEARS}
    for y in YEARS:
        K(len(RS[y]) == len(R[y]) and (RS[y].federal_agi.to_numpy() == R[y].federal_agi.to_numpy()).all(), f"h.readback.{y}")
    y = 2025
    r25, s25 = RS[y], SS[y]
    U = {c: C.units(r25, s25, *c) for c in C.ALL_CONSTRUCTIONS}
    hh, ffu = U[("code1", "ffu", "attached")], U[("code1", "ffu", "separate")]
    drop = U[("code1", "ffu", "dropped")]
    # (1) counts
    K(len(r25) == 852_947, "m01.returns", len(r25))
    K((r25.residency_code == 1).sum() == 719_213, "m01.resident")
    K(((r25.residency_code == 2).sum(), (r25.residency_code == 3).sum()) == (24_281, 109_453), "m01.codes23")
    K(len(ffu) == 677_351, "m01.ffu", len(ffu))
    K(len(hh) == 582_544, "m01.households", len(hh))
    K(((r25.residency_code == 1) & (r25.filing_status == 3)).sum() == 2 * 41_862, "m01.separate_returns")
    # (2)(6)(7) floors
    fl = {c: floors_of(U[c]) for c in U}
    exact = {c: C.nearest_rank_floors(U[c].agi) for c in U}
    K(tuple(fl[("code1", "ffu", "attached")]) == ANSWER, "m02.answer", fl[("code1", "ffu", "attached")])
    K(tuple(fl[("code1", "ffu", "separate")]) == STOP, "m06.stop_rung", fl[("code1", "ffu", "separate")])
    K(tuple(fl[("code1", "ffu", "dropped")]) == RUNG3, "m07.rung3", fl[("code1", "ffu", "dropped")])
    # (3) units at or above each adopted floor equal k
    for F, k in zip(ANSWER, K_HH):
        K((hh.agi >= F).sum() == k and (hh.agi > F).sum() == k, f"m03.k_at_floor.{F}")
    for F, k in zip(STOP, K_FFU):
        K((ffu.agi >= F).sum() == k, f"m03.k_at_stop.{F}")
    # (4) rank k and k+1 inside the windows; ranks k-2..k+2 distinct
    for u, Fs in ((hh, ANSWER), (ffu, STOP), (drop, RUNG3)):
        v = np.sort(u.agi.to_numpy())[::-1]
        for F, p in zip(Fs, PCTS):
            k = k_top(len(v), p)
            K(F <= v[k - 1] < F + 250 and F - 250 <= v[k] < F, f"m04.window.{F}", (v[k - 1], v[k]))
            K(F - 250 <= v[k + 1] and v[k - 3] < F + 250 and len(set(v[k - 3:k + 2])) == 5, f"m04.neighbours.{F}", v[k - 3:k + 2])
            K(v[k - 1] % 1000 != 0, f"m04.not_round.{F}")
    # (5) quantile conventions converge, every construction
    for c, u in U.items():
        for p in PCTS:
            fc = floor_conventions(u.agi.to_numpy(), p)
            K(len({round_thousand(x) for x in fc.values()}) == 1, f"m05.conventions.{c}.{p}", fc)
            K(min(abs((x % 1000) - 500) for x in fc.values()) >= 70, f"m05.edge.{c}.{p}")
    # (8) rungs 0 and 1 realised, at least 15 per cent under the answer at every floor
    r0, r1 = fl[("all", "return", "separate")], fl[("code1", "return", "separate")]
    for i in range(3):
        K(r0[i] <= 0.85 * ANSWER[i] and r1[i] <= 0.85 * ANSWER[i], f"m08.rungs01.{i}", (r0, r1))
    # (9) floors non-decreasing rung by rung, strictly at the top floor
    ladder = [r0, r1, list(STOP), list(RUNG3), list(ANSWER)]
    for i in range(3):
        K(all(ladder[j][i] <= ladder[j + 1][i] for j in range(4)), f"m09.monotone.{i}")
    K(all(ladder[j][2] < ladder[j + 1][2] for j in range(4)), "m09.strict_top")
    # (10)(11) hit counts, read from the shipped tables
    pub_x = read_tables(tgt, FILES, app)
    for yy in (2022, 2023, 2024):
        K(pub_x[yy] == pub[yy], f"m16.tables_as_written.{yy}")
    cells = calib.all_cells(RS, SS, app)
    hits, misses = calib.hit_table(cells, pub_x)
    for c, h in hits.items():
        K(h == calib.EXPECTED_HITS[c], f"m10.hits.{c}", h)
    K(sum(len(v) for v in pub_x.values()) == 69, "m16.cell_count")
    # (11) partials' floors
    K(tuple(fl[C.PARTIAL][:2]) == STOP[:2], "m11.partial_lower_floors", fl[C.PARTIAL])
    # (12) grid: the answer is the maximum at every floor; nearest differing cell distance
    for i in range(3):
        K(all(fl[c][i] <= ANSWER[i] for c in U), f"m12.answer_max.{i}")
    near = []
    for i in range(3):
        d = sorted((100.0 * (ANSWER[i] - fl[c][i]) / ANSWER[i], c) for c in U if fl[c][i] != ANSWER[i])
        near.append(d[0])
        K(d[0][0] >= 6.0, f"m12.nearest.{i}", d[0])
    # (13) every losing cell mapped to the shipped rule it violates
    rule_check(K, misses, pub_x)
    # (14) trust group (world)
    tr = W.trust[2025]
    kid = W.kid_agi[2025]
    att = np.bincount(W.dep_owner, weights=kid, minlength=W.n).astype(np.int64)
    own = W.own[2025]
    tk = np.isin(W.dep_owner, tr) & (kid > 0)
    K(len(tr) == 1_475 and tk.sum() == 2_350, "m14.trust_size", (len(tr), int(tk.sum())))
    K(((own[tr] >= 520_000) & (own[tr] < 742_000)).all(), "m14.trust_band")
    K(((own[tr] + att[tr]) >= 742_000).sum() == 976, "m14.crossers")
    K(((own[tr] + att[tr]) < 990_001).all() and (kid[tk] < 100_000).all() and (kid[tk] >= 30_000).all(), "m14.caps")
    # (15) dependents' share of resident AGI; rung 3's total misses
    res = r25[r25.residency_code == 1]
    deps = res.filer_tin.isin(s25.dependent_tin)
    share = res.federal_agi[deps].sum() / res.federal_agi.sum()
    K(0.0200 <= share <= 0.0210, "m15.dep_share", share)
    rec["dep_share"] = round(100 * share, 3)
    for yy in (2022, 2023, 2024):
        dc = cells[("code1", "ffu", "dropped")][yy][("total_agi_k", "all")]
        d = 100.0 * (dc - pub_x[yy][("total_agi_k", "all")]) / pub_x[yy][("total_agi_k", "all")]
        K(-2.2 <= d <= -1.9, f"m15.rung3_totals.{yy}", d)
    # (17)(18) the stop rung's misses, and its ties to the dollar
    ms = misses[("code1", "ffu", "separate")]
    K(len(ms) == 11, "m17.eleven")
    for yy, key, got, want in ms:
        K(got < want and abs(got - want) / want < 0.05, f"m17.one_sided.{yy}.{key}", (got, want))
    K({(m[0], m[1][0]) for m in ms if m[1][0] != "county_units_500k"} == {(yy, t) for yy in (2022, 2023, 2024) for t in ("units", "agi_k")}, "m17.which")
    for yy in (2022, 2023, 2024):
        a_h = C.units(RS[yy], SS[yy], "code1", "ffu", "attached").agi.to_numpy()
        a_f = C.units(RS[yy], SS[yy], "code1", "ffu", "separate").agi.to_numpy()
        for (lo, hi), lab in zip(C.CLASSES, C.CLASS_LABELS):
            if lo == 500_000:
                continue
            mh = (a_h >= lo) & ((a_h < hi) if hi else True)
            mf = (a_f >= lo) & ((a_f < hi) if hi else True)
            K(mh.sum() == mf.sum() and a_h[mh].sum() == a_f[mf].sum(), f"m18.dollar_tie.{yy}.{lo}")
    units500 = {yy: pub_x[yy][("units", C.CLASS_LABELS[3])] - cells[("code1", "ffu", "separate")][yy][("units", C.CLASS_LABELS[3])] for yy in (2022, 2023, 2024)}
    K(units500 == {2022: 23, 2023: 10, 2024: 30}, "m17.unit_shortfalls", units500)
    agimiss = {yy: round(100.0 * (pub_x[yy][("agi_k", C.CLASS_LABELS[3])] - cells[("code1", "ffu", "separate")][yy][("agi_k", C.CLASS_LABELS[3])]) / pub_x[yy][("agi_k", C.CLASS_LABELS[3])], 2) for yy in (2022, 2023, 2024)}
    for yy, tgt_ in ((2022, 3.4), (2023, 3.1), (2024, 3.6)):
        K(abs(agimiss[yy] - tgt_) <= 0.25, f"m17.agi_miss.{yy}", agimiss[yy])
    rec["stop_rung_misses"] = {"units_500k_1m": units500, "agi_500k_1m_pct": agimiss,
                               "county": {m[1][1]: m[3] - m[2] for m in ms if m[1][0] == "county_units_500k"}}
    # (19) no attached income at $1M or more; no household crosses $1M on it
    for yy in YEARS:
        at = np.bincount(W.dep_owner, weights=W.kid_agi[yy], minlength=W.n).astype(np.int64)
        o = W.own[yy]
        K(((at > 0) & (o + at >= 990_001)).sum() == 0 and ((at > 0) & (o >= 1_000_000)).sum() == 0, f"m19.no_attached_at_1m.{yy}")
    # (20) twin pair
    twin_check(K, RS, SS, app, pub_x, rec)
    app2, top13 = calib.appendix_codes(RS[2024])
    K(app2 == list(app) and Wm.KESSLER in app and Wm.ABINGTON in app, "m20.appendix_is_twelve_largest", (app2, top13))
    # (21) resemblance and the smallest stop-rung miss
    def shares(cc):
        u_ = np.array([cc[("units", l)] for l in C.CLASS_LABELS], float)
        return u_ / u_.sum()
    f25 = C.published_cells(ffu, 2025, app)
    dist = {yy: float(np.abs(shares(f25) - shares(pub_x[yy])).sum()) for yy in (2022, 2023, 2024)}
    K(min(dist, key=dist.get) == 2023 and sorted(dist.values())[1] >= 1.5 * dist[2023], "m21.nearest_2023", dist)
    K(min(units500, key=units500.get) == 2023, "m21.smallest_miss_2023")
    # (22) table structure: nothing below $100,000, no total-units cell
    K(all(k[0] in ("units", "agi_k", "total_agi_k", "county_units_500k") for yy in pub_x for k in pub_x[yy]), "m22.structure")
    K(all(("units", "all") not in pub_x[yy] for yy in pub_x), "m22.no_total_units")
    # (23)-(25) structural facts
    for yy in YEARS:
        r, s = RS[yy], SS[yy]
        g = r.groupby("federal_primary_tin").residency_code.nunique()
        K((g == 1).all(), f"m23.no_mixed_units.{yy}")
        d = r[r.filer_tin.isin(s.dependent_tin)]
        cl = s.set_index("dependent_tin").claimant_return_id.loc[d.filer_tin]
        cres = r.set_index("return_id").residency_code.loc[cl.to_numpy()].to_numpy()
        K((d.residency_code.to_numpy() == cres).all() and (cres[cres == 1].size == len(d)), f"m23.dependents_code1.{yy}")
        K(s.dependent_tin.is_unique and r.filer_tin.is_unique and r.return_id.is_unique, f"m24.unique.{yy}")
        rel = s.set_index("dependent_tin").relationship_code.loc[d.filer_tin]
        K(rel.isin(["01", "02", "03"]).all(), f"m25.children.{yy}")
        K((d.filing_status == 1).all() and (~d.return_id.isin(s.claimant_return_id)).all(), f"m25.no_chains.{yy}")
        K((d.filer_tin == d.federal_primary_tin).all() and not d.filer_tin.isin(r.spouse_tin).any(), f"m25.not_spouses.{yy}")
    # (26) filter order
    allh = C.units(r25, s25, "all", "ffu", "attached")
    prim = r25[r25.filer_tin == r25.federal_primary_tin].set_index("filer_tin").residency_code
    allh_res = allh[prim.loc[allh.key].to_numpy() == 1]
    K(len(allh_res) == 582_544 and floors_of(allh_res) == list(ANSWER), "m26.filter_order")
    # (27) six row orders
    if not skip_slow:
        for i in range(6):
            rp = r25.sample(frac=1.0, random_state=1000 + i).reset_index(drop=True)
            sp = s25.sample(frac=1.0, random_state=2000 + i).reset_index(drop=True)
            u1 = C.units(rp, sp, "code1", "ffu", "attached")
            u2 = C.units(rp, sp, "code1", "ffu", "separate")
            K(len(u1) == 582_544 and floors_of(u1) == list(ANSWER) and floors_of(u2) == list(STOP), f"m27.row_order.{i}")
    # (28) zero and negative AGI units in the base
    K((hh.agi <= 0).sum() > 1000, "m28.nonpositive_present")
    for yy in (2022, 2023, 2024):
        u = C.units(RS[yy], SS[yy], "code1", "ffu", "attached")
        tot_pos = C.half_up_thousands(int(u.agi[u.agi > 0].sum()))
        K(tot_pos != pub_x[yy][("total_agi_k", "all")], f"m28.drop_negative_misses.{yy}")
    # (29) clean-data test: a claimant field on every dependent's return
    rr = r25[r25.residency_code == 1].copy()
    cl = s25.set_index("dependent_tin").claimant_return_id
    isd = rr.filer_tin.isin(s25.dependent_tin)
    rr["claimant"] = np.where(isd, cl.reindex(rr.filer_tin).to_numpy(), -1)
    fp = rr.set_index("return_id").federal_primary_tin
    key = np.where(rr.claimant > 0, fp.reindex(rr.claimant).to_numpy(), rr.federal_primary_tin)
    rep = pd.Series(rr.federal_agi.to_numpy()).groupby(key).sum()
    naive = floors_of(U[("all", "return", "separate")])
    K([round_thousand(x) for x in C.nearest_rank_floors(rep)] == list(ANSWER), "m29.repaired_answer")
    K(naive == r0 and naive != list(ANSWER), "m29.naive_unchanged")
    # (30) lens swap: different populations
    K((r25.residency_code == 1).sum() != len(hh) and len(hh) == 582_544, "m30.lens_swap")
    rec.update({"floors": {C.NAMES.get(c, str(c)): fl[c] for c in U}, "exact_floors": {str(c): exact[c] for c in U},
                "hits": {str(c): h for c, h in hits.items()}, "nearest_cells": [(round(d[0], 2), str(d[1])) for d in near]})
    # (31)-(33) and the rest of the pack
    texts = pack_texts(tgt, FILES)
    floor_grep(K, texts, fl)
    single_statement(K, texts, FILES)
    tells(K, pub_x)
    # ---------------- ask layer
    import askchecks
    rec.update(askchecks.run(K, W, RS, SS, A, tgt, FILES, texts))
    # ---------------- pack gates
    rec.update(pack_gates(K, tgt, FILES, DISTRACTORS, RS, texts, W))
    return rec


def read_tables(tgt, FILES, app):
    out = {}
    for yy in (2022, 2023, 2024):
        wb = openpyxl.load_workbook(tgt / FILES["tables"].format(y=yy), data_only=True)
        ws = wb["Table 1"]
        cells = {}
        for row in ws.iter_rows(min_row=1, values_only=True):
            lab = row[0]
            if lab in C.CLASS_LABELS:
                cells[("units", lab)] = int(row[1])
                cells[("agi_k", lab)] = int(row[2])
            elif isinstance(lab, str) and lab.startswith("All full-year resident household units"):
                cells[("total_agi_k", "all")] = int(row[2])
        if yy == 2024:
            wa = wb["Appendix A"]
            for row in wa.iter_rows(min_row=5, values_only=True):
                if row[1] and str(row[1]).isdigit():
                    cells[("county_units_500k", str(row[1]))] = int(row[2])
        out[yy] = cells
    return out


def rule_check(K, misses, pub):
    """Each losing construction's misses fall where the rule it breaks predicts."""
    tot = {(yy, ("total_agi_k", "all")) for yy in (2022, 2023, 2024)}
    cls = {(yy, (m, lab)) for yy in (2022, 2023, 2024) for m in ("units", "agi_k") for lab in C.CLASS_LABELS}
    for c, ms in misses.items():
        got = {(m[0], m[1]) for m in ms}
        if c[0] == "all":                       # residency: totals carry part-year and nonresident AGI
            K(tot <= got, f"m13.residency.{c}")
        if c[1] == "return":                    # spouses split: every class cell moves
            K(cls <= got, f"m13.spouses.{c}")
        if c[2] in ("dropped",) or c == C.PARTIAL:   # complete partition broken: totals move
            K(tot <= got, f"m13.partition.{c}")
        if c == ("code1", "ffu", "separate"):    # dependents unattached: the $500K to $1M class and counties
            K(not (tot & got) and all(k[1][0] == "county_units_500k" or k[1][1] == C.CLASS_LABELS[3] for k in got), f"m13.attach.{c}")


def twin_check(K, RS, SS, app, pub, rec):
    yy = 2024
    r, s = RS[yy], SS[yy]
    f = C.units(r, s, "code1", "ffu", "separate")
    h = C.units(r, s, "code1", "ffu", "attached")
    kf = ((f.agi >= 500_000) & (f.county == Wm.KESSLER)).sum()
    af = ((f.agi >= 500_000) & (f.county == Wm.ABINGTON)).sum()
    kh = ((h.agi >= 500_000) & (h.county == Wm.KESSLER)).sum()
    ah = ((h.agi >= 500_000) & (h.county == Wm.ABINGTON)).sum()
    K(kf == af == 287, "m20.twin_ffu", (kf, af))
    K(pub[yy][("county_units_500k", Wm.KESSLER)] == 301 and pub[yy][("county_units_500k", Wm.ABINGTON)] == 287, "m20.twin_published")
    K((kh, ah) == (301, 287), "m20.twin_households")
    res = r[r.residency_code == 1]
    K(((res.federal_agi >= 500_000) & (res.county_code == Wm.KESSLER)).sum() == ((res.federal_agi >= 500_000) & (res.county_code == Wm.ABINGTON)).sum(), "m20.twin_returns_500k")
    dep = res[res.filer_tin.isin(s.dependent_tin)]
    cl = s.set_index("dependent_tin").claimant_return_id.loc[dep.filer_tin]
    ccty = res.set_index("return_id").county_code.loc[cl.to_numpy()].to_numpy()
    nk, na = (ccty == Wm.KESSLER).sum(), (ccty == Wm.ABINGTON).sum()
    K(abs(nk - na) <= 0.02 * max(nk, na), "m20.twin_dependents", (nk, na))
    # any allocation that treats the two counties alike reproduces at most one of them
    K(301 - kf != 287 - af, "m20.symmetric_fails")
    rec["twin"] = {"ffu_500k": [int(kf), int(af)], "published": [301, 287], "dependents_returns": [int(nk), int(na)]}


def pack_texts(tgt, FILES):
    out = {}
    for p in sorted(tgt.iterdir()):
        if p.suffix in (".txt", ".csv"):
            out[p.name] = p.read_text(encoding="utf-8", errors="ignore")
        elif p.suffix == ".pdf":
            out[p.name] = "\n".join(pg.extract_text() or "" for pg in PdfReader(str(p)).pages)
        elif p.suffix == ".xlsx":
            wb = openpyxl.load_workbook(p, data_only=True)
            lines = []
            for ws in wb.worksheets:
                for row in ws.iter_rows(values_only=True):
                    lines.append("\t".join("" if v is None else str(v) for v in row))
            out[p.name] = "\n".join(lines)
    return out


def floor_grep(K, texts, fl):
    figs = set()
    for v in fl.values():
        figs.update(v)
    for name, t in texts.items():
        if name.endswith(".csv") and name not in ("intake_log.csv",):
            continue          # record files: amounts are data, not stated floors
        for F in figs:
            for form in (f"{F:,}", f"${F // 1000}K", f"${F // 1000},000", f"{F // 1000}k"):
                K(form not in t, f"m31.no_floor.{name}.{F}.{form}")


P1 = "Tiers are drawn on full-year resident household units at the 10, 5 and 1 per cent marks of household AGI"
P2 = "A tier schedule is adopted only on a construction that reproduces every published cell"
P3 = "Tier 1 runs from the 1 per cent floor up"


def single_statement(K, texts, FILES):
    norm = {k: re.sub(r"\s+", " ", v) for k, v in texts.items()}
    for lab, s in (("P1", P1), ("P2", P2), ("P3", P3)):
        n = {k: v.count(s) for k, v in norm.items()}
        K(sum(n.values()) == 1 and n.get(FILES["method"], 0) == 1, f"m32.{lab}", n)
    allowed_files = {FILES["tables"].format(y=y) for y in (2022, 2023, 2024)}
    fiscal = "The Legislative Fiscal Office draws its household tiers on federal filing units"
    for k, v in norm.items():
        if k in allowed_files:
            continue
        rest = v.replace(P1 + "; every such unit counts in the base whatever its AGI", "")
        rest = rest.replace(fiscal, "").replace("Household Income Tables", "").replace("household_income_tables_ty", "")
        rest = rest.replace("head of household", "")
        K("household" not in rest.lower(), f"m32.household_word.{k}")
        K("filing unit" not in v.replace(fiscal, "").lower(), f"m32.filing_unit.{k}")


def tells(K, pub):
    for yy, cc in pub.items():
        for key, v in cc.items():
            K(v % 100 != 0, f"m33.round.{yy}.{key}")


def check_metadata(K, root, tgt, DISTRACTORS):
    m = json.loads((root / "metadata.json").read_text())
    K(len(m["distractor_files"]) >= 2 and all((tgt / f).exists() for f in m["distractor_files"]), "p48.distractors_named")
    for p in tgt.iterdir():
        K("distractor" not in p.name.lower(), f"p48.no_label_name.{p.name}")
        if p.suffix in (".txt", ".csv"):
            K("distractor" not in p.read_text(errors="ignore").lower(), f"p48.no_label_text.{p.name}")
    K(m["sources"] and all(s.get("license") and s.get("date") for s in m["sources"]), "p48.sources_recorded")


def check_containers(K, tgt, SCRUB):
    r = subprocess.run([sys.executable, str(SCRUB), str(tgt), "--floor", "2023-01-01", "--ceiling", "2026-11-06"],
                       capture_output=True, text=True)
    K(r.returncode == 0 and "clean" in r.stdout, "h1.scrub_clean", r.stdout + r.stderr)
    for p in tgt.iterdir():
        b = p.read_bytes()[:4096] if p.suffix == ".parquet" else b""
        if p.suffix in (".xlsx",):
            z = zipfile.ZipFile(p)
            blob = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/"))
            K(b"xlsxwriter" not in blob.lower() and b"openpyxl" not in blob.lower(), f"h1.xlsx_props.{p.name}")
        if p.suffix == ".pdf":
            raw = p.read_bytes()
            K(b"ReportLab" not in raw and b"reportlab" not in raw, f"h1.pdf_signature.{p.name}")
        if p.suffix == ".parquet":
            md = pq.read_schema(p).metadata or {}
            K(b"pandas" not in md, f"h1.parquet_no_pandas_meta.{p.name}")
            import duckdb
            n_dd = duckdb.connect().execute(f"select count(*) from read_parquet('{p}')").fetchone()[0]
            K(n_dd == pq.ParquetFile(p).metadata.num_rows, f"h.parquet_readers.{p.name}")


def pack_gates(K, tgt, FILES, DISTRACTORS, RS, texts, W):
    rec = {}
    files = sorted(p.name for p in tgt.iterdir() if p.is_file())
    fmts = sorted({Path(f).suffix for f in files})
    K(len(files) >= 10, "p48.files", len(files))
    K(len(fmts) >= 3, "p48.formats", fmts)
    rows = {}
    for f in files:
        p = tgt / f
        if p.suffix == ".parquet":
            rows[f] = pq.ParquetFile(p).metadata.num_rows
        elif p.suffix in (".csv",):
            rows[f] = sum(1 for _ in open(p)) - 1
        elif p.suffix == ".txt":
            rows[f] = sum(1 for _ in open(p))
    K(max(rows.values()) >= 25_000, "p48.volume")
    K(len(DISTRACTORS) >= 2 and all(d in files for d in DISTRACTORS), "p48.distractors_exist")
    # (51) the Department's table ties to the TY2025 file, all filers, to the row and the dollar
    import docs
    wb = openpyxl.load_workbook(tgt / FILES["dept"], data_only=True)
    ws = wb.active
    got = [(r[0], int(r[1]), int(r[2])) for r in ws.iter_rows(min_row=6, values_only=True) if r[0] and isinstance(r[1], (int, float))]
    K(got == docs.dept_table_rows(RS[2025]), "p51.dept_ties")
    # the intake log lists every shipped file but itself, by name
    il = pd.read_csv(tgt / FILES["intake"])
    K(set(il.file) == set(files) - {FILES["intake"]}, "h9.intake_complete")
    # H16: dates in the extracts sit on or before the extract dates
    lim = {FILES["ledger"]: "2026-01-31", FILES["returned"]: "2026-02-28", FILES["register"]: "2026-10-22",
           FILES["schd"]: "2026-10-22", FILES["amended"]: "2026-10-22", FILES["deposits"]: "2025-12-31"}
    for f, d in lim.items():
        t = texts.get(f)
        if t is None:
            df = pd.read_parquet(tgt / f)
            t = df.to_csv(index=False)
        dates = re.findall(r"\b(20\d\d-\d\d-\d\d)", t)
        K(max(dates) <= d, f"h16.dates.{f}", max(dates))
    for y in YEARS:
        K(RS[y].processed_date.max() <= pd.Timestamp("2026-10-22"), f"h16.processed.{y}")
    for f, t in texts.items():
        dates = re.findall(r"\b(20\d\d-\d\d-\d\d)", t)
        if dates:
            K(max(dates) <= "2026-11-06", f"h16.asof.{f}", max(dates))
        K("\u2014" not in t, f"h.no_em_dash.{f}")
    # (52) the distractors: no solution path reads them, and each sits in the decision's world
    import askcheck, constructions
    import inspect
    solution_src = inspect.getsource(askcheck) + inspect.getsource(constructions)
    for d in DISTRACTORS:
        K(d not in solution_src and Path(d).stem not in solution_src, f"p52.unused.{d}")
    dep = pd.read_csv(tgt / FILES["deposits"])
    ef = pd.read_parquet(tgt / FILES["efile"])
    K(dep.employer_ein.isin(ef.employer_ein).mean() > 0.8, "p52.deposits_same_employers")
    statewide = int(ef.state_tax_withheld.sum())
    K(0.85 < dep.amount.sum() / statewide < 1.15, "p52.deposits_adjacent_measure", dep.amount.sum() / statewide)
    rec["files"] = {f: rows.get(f, "") for f in files}
    rec["formats"] = fmts
    return rec
