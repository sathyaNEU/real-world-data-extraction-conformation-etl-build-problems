"""The ask sheet as code on the cut pack: every ask route a competent response builds, scored cell by cell against the
golden (a hit is the golden figure at the stated rounding), then the cracker (the careful route: the hygiene battery,
the scope of our titles, every filed rule) and the mirror (the most attractive wrong route) priced on the ask weight.

    python3 task166/generator/ceiling.py [target]"""
from __future__ import annotations

import hashlib
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C    # noqa: E402

ASK_W = 57.0        # the asks' share of the rubric, per cent
CALL_W = 38.0       # recommendation and critical components
IF_W = 5.0          # instruction-following


def rachan(P):
    return dict(zip(P.ra.ra_number, P.ra.channel))


def recv_counts(P, rec):
    f = rec[rec.date.map(C.in_fy2026)].copy()
    f["channel"] = f.ra_ref.map(rachan(P))
    g = f.groupby(["channel", f.date.map(C.fy_quarter)]).qty_received.sum()
    return {(c, q): int(g.get((c, q), 0)) for c in C.CHANNELS for q in (1, 2, 3, 4)}


def routes_received(P):
    raw = P.rec.copy()
    ours = set(P.titles.isbn)
    dedup = raw.drop_duplicates()
    dd_ours = dedup[dedup.isbn.isin(ours)]
    out = {}
    out["A0 every row"] = recv_counts(P, raw)
    out["A1 exact duplicates out"] = recv_counts(P, dedup)
    out["A2 duplicates out, our titles"] = recv_counts(P, dd_ours)
    out["A3 + repeated RA line and quantity out"] = recv_counts(P, dd_ours.drop_duplicates(["ra_ref", "isbn", "qty_received"]))
    out["A3g + repeated RA line, quantity and grades out"] = recv_counts(P, dd_ours.drop_duplicates(
        ["ra_ref", "isbn", "qty_received", "grade_saleable", "grade_hurt", "grade_unsaleable"]))
    units = dd_ours.sort_values(["date", "delivery_ref"])
    sig = units.groupby("delivery_ref", sort=False).apply(lambda g: tuple(sorted(zip(g.ra_ref, g.isbn, g.qty_received,
                                                                                    g.grade_saleable, g.grade_hurt, g.grade_unsaleable))))
    first = ~sig.duplicated()
    out["A3u + repeated delivery (every line, grades) out"] = recv_counts(P, units[units.delivery_ref.isin(set(sig[first].index))])
    auth = P.ra.groupby(["ra_number", "isbn"]).qty_authorised.sum()
    capped = dd_ours.sort_values(["date", "delivery_ref"]).copy()
    capped["cum"] = capped.groupby(["ra_ref", "isbn"]).qty_received.cumsum()
    a = np.array([auth.get((r, i), 10 ** 9) for r, i in zip(capped.ra_ref, capped.isbn)])
    capped["qty_received"] = np.clip(np.minimum(capped.qty_received, a - (capped.cum - capped.qty_received)), 0, None)
    out["A4 + capped at the authorised copies"] = recv_counts(P, capped)
    rec, _ = C.receipts_clean(P)
    out["golden"] = recv_counts(P, rec)
    cr = P.cr[(P.cr.reason_code == "RET") & P.cr.date.map(C.in_fy2026)]
    g = cr.groupby(["channel", cr.date.map(C.fy_quarter)]).qty.sum()
    out["A5 ledger credits for returns"] = {(c, q): int(g.get((c, q), 0)) for c in C.CHANNELS for q in (1, 2, 3, 4)}
    return out


def scrapped_shares(P, rec, ri_mode="golden", alloc="hurts", pulped=True):
    f = rec[rec.date.map(C.in_fy2026)].copy()
    f["channel"] = f.ra_ref.map(rachan(P))
    f["fmt"] = f.isbn.map(P.fmt)
    ri = P.ri[P.ri.date <= C.YE].sort_values(["tote", "date"])
    if ri_mode == "golden":
        fin = C.reinspection_final(P, rec).set_index("tote").pulped
    elif ri_mode == "sum":
        fin = ri.groupby("tote").pulped.sum()
    else:
        fin = ri.groupby("tote").pulped.last()
    hurts = f[f.hurts_tote != ""].groupby("hurts_tote").grade_hurt.sum()
    allh = rec[rec.hurts_tote != ""].groupby("hurts_tote").grade_hurt.sum()
    pul = np.zeros(len(f))
    if pulped:
        for i, (t, h) in enumerate(zip(f.hurts_tote, f.grade_hurt)):
            if t and t in fin.index:
                if alloc == "hurts":
                    pul[i] = fin[t] * h / allh[t] if allh.get(t, 0) else 0.0
                elif alloc == "fanout":
                    pul[i] = fin[t] if h else 0.0
                elif alloc == "fy_hurts":
                    pul[i] = fin[t] * h / hurts[t] if hurts.get(t, 0) else 0.0
    f["w"] = f.grade_unsaleable + pul
    ch = f.groupby("channel").agg(w=("w", "sum"), q=("qty_received", "sum"))
    fm = f.dropna(subset=["fmt"]).groupby("fmt").agg(w=("w", "sum"), q=("qty_received", "sum"))
    out = {("ch", c): round(100 * ch.loc[c, "w"] / ch.loc[c, "q"], 1) for c in C.CHANNELS if c in ch.index}
    out.update({("fm", x): round(100 * fm.loc[x, "w"] / fm.loc[x, "q"], 1) for x in C.FORMATS if x in fm.index})
    return out


def routes_scrapped(P):
    raw = P.rec.copy()
    ours = set(P.titles.isbn)
    dd = raw.drop_duplicates()
    dd_ours = dd[dd.isbn.isin(ours)].copy()
    rec, _ = C.receipts_clean(P)
    out = {}
    out["C0 graded unsaleable only"] = scrapped_shares(P, rec, pulped=False)
    out["C1 re-inspection rows summed"] = scrapped_shares(P, rec, "sum")
    out["C2 last re-inspection row per tote"] = scrapped_shares(P, rec, "last")
    out["C3 tote pulped on every line of the tote"] = scrapped_shares(P, rec, "golden", "fanout")
    out["C4 double bookings kept"] = scrapped_shares(P, dd_ours, "last")
    out["C5 other publishers kept"] = scrapped_shares(P, pd.concat([rec, dd[~dd.isbn.isin(ours)]]), "golden")
    out["C6 careful: duplicates and other publishers out, last row per tote"] = scrapped_shares(P, dd_ours, "last")
    out["C7 careful: duplicates and other publishers out, rows summed"] = scrapped_shares(P, dd_ours, "sum")
    units = dd_ours.sort_values(["date", "delivery_ref"])
    sig = units.groupby("delivery_ref", sort=False).apply(lambda g: tuple(sorted(zip(g.ra_ref, g.isbn, g.qty_received,
                                                                                    g.grade_saleable, g.grade_hurt, g.grade_unsaleable))))
    keep = units[units.delivery_ref.isin(set(sig[~sig.duplicated()].index))].copy()
    keep["channel"] = keep.ra_ref.map(rachan(P))
    keep["fmt"] = keep.isbn.map(P.fmt)
    out["C8 full includer: repeated deliveries dropped, totes resolved against hurts"] = scrapped_shares(P, keep, "golden")
    out["golden"] = scrapped_shares(P, rec)
    return out


def hits(route, golden):
    return sum(1 for k, v in golden.items() if route.get(k) == v), len(golden)


def main(target):
    P = C.Pack(target)
    dig = hashlib.sha256()
    for f in sorted(os.listdir(target)):
        dig.update(open(os.path.join(target, f), "rb").read())
    A = routes_received(P)
    S = routes_scrapped(P)
    gA, gS = A["golden"], S["golden"]
    nA, nS = len(gA), len(gS)
    rows = []
    for k, v in A.items():
        h, n = hits(v, gA)
        rows.append(("received", k, h, n))
    for k, v in S.items():
        h, n = hits(v, gS)
        rows.append(("written off", k, h, n))
    print("pack sha256 %s" % dig.hexdigest()[:16])
    for a, k, h, n in rows:
        print("  %-12s %-66s %2d of %2d" % (a, k, h, n))
    per_cell = ASK_W / (nA + nS)
    cracker = {"received": "A2 duplicates out, our titles", "written off": "C6 careful: duplicates and other publishers out, last row per tote"}
    mirror = {"received": "A1 exact duplicates out", "written off": "C0 graded unsaleable only"}

    def kept(sel):
        hA = hits(A[sel["received"]], gA)[0]
        hS = hits(S[sel["written off"]], gS)[0]
        return (hA + hS) * per_cell, hA, hS
    ck, ckA, ckS = kept(cracker)
    mk, mkA, mkS = kept(mirror)
    # the pair: the cracker lands the call and its critical components; the mirror misses them
    on_call = CALL_W + IF_W + ck
    off_call = 5.0 + IF_W + mk
    pair = (on_call + off_call) / 2
    print("cracker keeps %.1f of %.0f ask points (received %d of %d, written off %d of %d)" % (ck, ASK_W, ckA, nA, ckS, nS))
    print("mirror keeps %.1f of %.0f ask points (received %d of %d, written off %d of %d)" % (mk, ASK_W, mkA, nA, mkS, nS))
    print("pair: on the call %.1f, off the call %.1f, average %.1f" % (on_call, off_call, pair))
    fiA = hits(A["A3u + repeated delivery (every line, grades) out"], gA)[0]
    fS = S["C8 full includer: repeated deliveries dropped, totes resolved against hurts"]
    fiC = sum(1 for k, v in gS.items() if k[0] == "ch" and fS.get(k) == v)
    fiF = sum(1 for k, v in gS.items() if k[0] == "fm" and fS.get(k) == v)
    fk = (fiA + fiC + fiF) * per_cell
    print("full includer keeps %.1f of %.0f ask points (received %d of %d, written off by channel %d, by format %d); on the call %.1f, "
          "with the mirror off the call the pair is %.1f" % (fk, ASK_W, fiA, nA, fiC, fiF, CALL_W + IF_W + fk, (CALL_W + IF_W + fk + off_call) / 2))
    res = dict(pack=dig.hexdigest(), cracker_kept=ck, mirror_kept=mk, pair=pair,
               mirror_share=mk / ASK_W, cracker_share=ck / ASK_W,
               routes={"%s|%s" % (a, k): [h, n] for a, k, h, n in rows})
    return res


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    r = main(t)
    if len(sys.argv) > 2:
        json.dump(r, open(sys.argv[2], "w"), indent=1)
