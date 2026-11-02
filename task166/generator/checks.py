"""checks.py: the build's assertions, on the cut pack (target/), the goldens and the clean world the pack was cut from.
Labels: R1 to R3 the client's three rules executed on the clean truth; SF the semantic fork table's rows; F the family
convergence; L the ladder; A and C the asks; S the separation line; X realism; G the input gates and goldens.
Exit 1 on any failure."""
from __future__ import annotations

import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import ceiling as CE        # noqa: E402
import common as K          # noqa: E402
import records as RC        # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
FAILS = []


def check(label, cond, detail=""):
    print("%s %s%s" % ("PASS" if cond else "FAIL", label, ("  " + detail) if detail else ""))
    if not cond:
        FAILS.append(label)


def b250(x):
    return int(250000 * np.floor(x / 250000 + 0.5))


# ----------------------------------------------------------------------------------------------------------------
# The clean world: every allowance route run on the generator's own records, before any file is written


def world_frames(W):
    acc = {a.aid: a for a in W.accounts}
    eds = W.eds
    inv = pd.DataFrame(W.invoices, columns=["inv", "wk", "wd", "aid", "eid", "qty", "price"])
    inv["day"] = 7 * inv.wk + inv.wd
    inv["fmt"] = inv.eid.map(lambda e: eds[e].fmt)
    inv["ch"] = inv.aid.map(lambda a: acc[a].channel)
    inv["terms"] = inv.aid.map(lambda a: acc[a].terms)
    months = {}
    for i, e in enumerate(eds):
        if e.fmt == "Hardback" and e.succ_pub is not None:
            months[i] = (e.succ_pub - e.pub).days / 30.44
    inv["quick"] = inv.eid.map(lambda e: months.get(e, 99.0) <= 8.0)
    cr = pd.DataFrame(W.credits, columns=["cr", "day", "aid", "eid", "qty", "inv", "price", "ra", "reason"])
    return inv, cr


def world_allowance(inv, cr, T, step, lag=425):
    start = (K.EXTRACT_FROM - K.DAY0).days
    sor = inv[inv.terms == "SOR"].copy()
    sor["seg"] = sor.fmt + "|" + sor.ch + np.where(step & sor.quick & (sor.fmt == "Hardback"), "|q", "")
    mat = sor[(sor.day >= start) & (sor.day <= T - lag)]
    c = cr[(cr.reason == "RET") & (cr.day <= T)].merge(mat[["inv", "day", "seg"]].rename(columns={"day": "iday"}), on="inv")
    c["age"] = np.clip((c.day - c.iday) // 7, 0, 70)
    tot = mat.groupby("seg").qty.sum()
    curves = {k: np.cumsum(np.bincount(g.age.values, weights=g.qty.values, minlength=71)) / tot[k] for k, g in c.groupby("seg")}
    op = sor[(sor.day <= T) & (sor.day > T - 365)].copy()
    op["a"] = np.clip((T - op.day) // 7, 0, 70)
    out = 0.0
    for k, g in op.groupby("seg"):
        cv = curves.get(k)
        if cv is not None:
            out += float((g.qty.values * (cv[70] - cv[g.a.values]) * g.price.values).sum())
    return out


def world_truth(inv, cr, T):
    f = cr[(cr.reason == "RET") & (cr.day > T)].merge(inv[["inv", "day"]].rename(columns={"day": "iday"}), on="inv")
    f = f[f.iday <= T]
    return float((f.qty * f.price).sum())


# ----------------------------------------------------------------------------------------------------------------
# Variants of the pack route the fork table and the family name


def dev_variant(P, T, seg, unit_days=7, max_units=70, price="line", open_days=365, firm=False, keep_dit=False, lag=425):
    inv = P.inv if firm else P.inv[P.inv.terms == "SOR"]
    inv = inv.copy()
    inv["seg"] = seg(inv)
    inv["price"] = inv.net_value / inv.qty
    if price == "average":
        avg = inv.groupby("seg").apply(lambda g: g.net_value.sum() / g.qty.sum())
        inv["price"] = inv.seg.map(avg)
    cr = P.cr[(P.cr.day <= T) & ((P.cr.reason_code == "RET") | keep_dit)]
    lo = (C.EXTRACT_FROM - dt.date(2020, 11, 2)).days
    mat = inv[(inv.day >= lo) & (inv.day <= T - lag)]
    c = cr.merge(mat[["invoice_no", "day", "seg"]].rename(columns={"day": "iday"}), left_on="against_invoice", right_on="invoice_no")
    c["age"] = np.clip(((c.day - c.iday) / unit_days).astype(int), 0, max_units)
    tot = mat.groupby("seg").qty.sum()
    curves = {k: np.cumsum(np.bincount(g.age.values, weights=g.qty.values, minlength=max_units + 1)) / tot[k] for k, g in c.groupby("seg")}
    op = inv[(inv.day <= T) & (inv.day > T - open_days)].copy()
    op["a"] = np.clip(((T - op.day) / unit_days).astype(int), 0, max_units)
    out = 0.0
    hb = 0.0
    for k, g in op.groupby("seg"):
        cv = curves.get(k)
        if cv is None:
            continue
        v = float((g.qty.values * (cv[max_units] - cv[g.a.values]) * g.price.values).sum())
        out += v
        if k.startswith("Hardback"):
            hb += v
    return out, hb


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    G, GH = fig["allowance_gbp"]["value"], fig["allowance_hardback_gbp"]["value"]
    P = C.Pack(TARGET)
    T = C.dnum(C.YE)
    W = WD.simulate()
    inv_w, cr_w = world_frames(W)
    gold, gparts = C.golden_allowance(P)
    dflt, dparts = C.default_allowance(P)
    trail, _ = C.trailing_rate_allowance(P)

    # ---------------------------------------------------------------- the three rules on the clean truth
    late = P.cr[(P.cr.reason_code == "RET") & (P.cr.date >= dt.date(2023, 2, 1))]
    check("R1 the triangle's raw material ships: invoice lines and the credits that quote them (from February 2023)",
          len(P.inv) > 100000 and late.against_invoice.isin(P.inv.invoice_no).mean() > 0.995,
          "%d invoice lines, %.2f%% of later returns credits quote a shipped invoice" % (
              len(P.inv), 100 * late.against_invoice.isin(P.inv.invoice_no).mean()))
    fc = P.titles[P.titles.pub > C.YE]
    check("R1 the title master carries the forthcoming paperbacks under their own ISBNs",
          (fc.fmt == "Paperback").sum() >= 20 and set(fc.status) <= {"Forthcoming"}, "%d forthcoming paperbacks" % (fc.fmt == "Paperback").sum())
    cols = {c.lower() for c in P.titles.columns}
    check("R1 the deciding property has no column (no edition, successor or paperback field on the title master)",
          not any(w in c for c in cols for w in ("paperback", "successor", "edition", "related", "parent", "work_id")), str(sorted(cols)))
    ct = world_truth(inv_w, cr_w, T)
    cd = world_allowance(inv_w, cr_w, T, step=False)
    cg = world_allowance(inv_w, cr_w, T, step=True)
    check("R2 clean-data test: on the clean records the development without the step still files the wrong bin",
          b250(cd) != b250(cg) and b250(cd) < G, "clean default %.0f (%d), clean step %.0f (%d)" % (cd, b250(cd), cg, b250(cg)))
    check("R2 the step on the clean records lands the golden bin, and so does the realised credit",
          b250(cg) == G and b250(ct) == G, "clean step %.0f, realised %.0f, golden %d" % (cg, ct, G))
    check("R3a executing every filed rule (terms and policy) on the default path files the wrong allowance",
          b250(dflt) != G, "default %.0f -> %d" % (dflt, b250(dflt)))
    fam = C.family(P)
    ns, st = fam[fam.route == "no step"], fam[fam.route == "step"]
    check("R3b the enumerated family without the step: every member below the golden bin",
          (ns.value.map(b250) < G).all(), "%.0f to %.0f over %d members" % (ns.value.min(), ns.value.max(), len(ns)))
    check("R3b the standing family (the step taken): every member in the golden bin",
          (st.value.map(b250) == G).all(), "%.0f to %.0f over %d members" % (st.value.min(), st.value.max(), len(st)))
    cheap = {"trailing twelve months": trail, "development by format and channel": dflt,
             "development by format": C.development(P, T, C.seg_fmt)[0],
             "development by month of invoice age": dev_variant(P, T, C.seg_fmt_channel, unit_days=30.44, max_units=16)[0]}
    land = [k for k, v in cheap.items() if b250(v) == G]
    check("R3c cheap routes on the pack landing the call: none", not land,
          "; ".join("%s %.0f" % (k, v) for k, v in cheap.items()))

    # ---------------------------------------------------------------- the ladder and the back-test
    check("L0 rung 0, the trailing rate, files the wrong bin", b250(trail) != G, "%.0f" % trail)
    check("L1 rung 1, the field's development by format, channel and weeks since invoice, files the wrong bin",
          b250(dflt) != G, "%.0f" % dflt)
    check("L2 the golden is the development with the hardbacks split by their own paperback's date", b250(gold) == G, "%.0f" % gold)
    check("L2 separation: golden over default 1.25 or more", gold / dflt >= 1.25, "%.3f" % (gold / dflt))
    bt = C.backtest(P)
    check("L back-test: the default validates within 5 per cent at the 2024 and 2025 year ends",
          all(abs(e / a - 1) <= 0.05 for e, a in bt.values()), "; ".join("%d %+.1f%%" % (y, 100 * (e / a - 1)) for y, (e, a) in bt.items()))
    check("L the golden sits in its bin with room on both sides", gold - (G - 125000) >= 40000 and (G + 125000) - gold >= 40000,
          "%.0f in [%d, %d)" % (gold, G - 125000, G + 125000))
    check("L the hardback part's family all in its bin", (st.hb.map(b250) == GH).all() and b250(gparts["Hardback"]) == GH,
          "%.0f to %.0f, golden %.0f, bin %d" % (st.hb.min(), st.hb.max(), gparts["Hardback"], GH))
    check("L the hardback part without the step falls outside its bin", (ns.hb.map(b250) != GH).all(), "%.0f to %.0f" % (ns.hb.min(), ns.hb.max()))

    # ---------------------------------------------------------------- the semantic fork table
    dit, _ = C.development(P, T, C.make_quick_seg(P), keep_dit=True)[:2]
    check("SF1 transit claims kept in the development: ruled out by the accounting policy; same bin either way",
          b250(dit) == G, "%.0f" % dit)
    firm = dev_variant(P, T, C.make_quick_seg(P), firm=True)
    check("SF2 firm-sale accounts kept in: ruled out by the terms (section 4); same bin either way", b250(firm[0]) == G, "%.0f" % firm[0])
    o490 = dev_variant(P, T, C.make_quick_seg(P), open_days=490)
    check("SF3 invoices up to 16 months old at the year end kept open: same bin", b250(o490[0]) == G, "%.0f" % o490[0])
    avgp = dev_variant(P, T, C.make_quick_seg(P), price="average")
    check("SF4 credit at the segment's average net price instead of each line's own: same bin", b250(avgp[0]) == G, "%.0f" % avgp[0])
    mo = dev_variant(P, T, C.make_quick_seg(P), unit_days=30.44, max_units=16)
    check("SF5 development by months since invoice instead of weeks: same bin", b250(mo[0]) == G and b250(mo[1]) == GH,
          "%.0f, hardbacks %.0f" % mo)
    thr = {t: C.development(P, T, C.make_quick_seg(P, t))[0] for t in (6.0, 7.0, 9.0, 10.0, 11.0)}
    check("SF6 the paperback-date threshold anywhere from 6 to 11 months: the same figure (no paperback falls between)",
          max(thr.values()) - min(thr.values()) < 1.0, ", ".join("%g: %.0f" % kv for kv in thr.items()))
    L = C.link_editions(P.titles)
    gaps = L.months.values
    check("SF6 no hardback's own paperback falls between 5.4 and 11.3 months", not ((gaps > 5.4) & (gaps < 11.3)).any(),
          "%d links" % len(L))
    check("SF7 hardbacks: the legacy code HB and the current label both map to Hardback", set(P.titles.format.unique()) >= {"HB", "Hardback"})
    check("SF8 the allowance rounds to its bin unambiguously (40,000 or more from either edge)",
          min(gold - (G - 125000), (G + 125000) - gold) >= 40000, "%.0f -> %d" % (gold, G))
    rec, drop = C.receipts_clean(P)
    cal = rec[rec.date.map(C.in_fy2026)]
    calq = cal.groupby(["channel", cal.date.map(lambda d: (d.month - 1) // 3 + 1)]).qty_received.sum()
    gA = C.ask_received(P, rec)
    check("SF9 calendar quarters instead of the financial year's: different cells (ruled out by the year to 31 October)",
          sum(1 for k, v in gA.items() if int(calq.get(k, -1)) == v) <= 2)
    S = CE.routes_scrapped(P)
    check("SF10 written off read as graded unsaleable only: ruled out by the accounting policy (pulped hurts are written off)",
          CE.hits(S["C0 graded unsaleable only"], S["golden"])[0] == 0)
    check("SF11 copies of our titles: every kept receipt's ISBN is on the title master", rec.isbn.isin(set(P.titles.isbn)).all())
    check("SF12 a receipt's channel is its authorisation's account's: every FY2026 receipt maps", rec[rec.date.map(C.in_fy2026)].channel.notna().all())
    A = CE.routes_received(P)
    check("SF13 copies sent beyond an authorisation came in (terms: held for collection): capping them out misses cells",
          CE.hits(A["A4 + capped at the authorised copies"], A["golden"])[0] <= 12)
    check("SF14 the hardback part is the allowance on hardback invoice lines", abs(sum(gparts.values()) - gold) < 1)

    def remainder_methods(Ty):
        seg = C.make_quick_seg(P, 8.0, True)
        _, _, cv = C.development(P, Ty, seg)
        iv = P.inv[P.inv.terms == "SOR"].copy()
        iv["seg"] = seg(iv)
        o = iv[(iv.day <= Ty) & (iv.day > Ty - 365)].copy()
        o["a"] = np.clip((Ty - o.day) // 7, 0, 70)
        cum = np.array([cv[k][a] for k, a in zip(o.seg, o.a)])
        ult = np.array([cv[k][70] for k in o.seg])
        done = P.cr[(P.cr.reason_code == "RET") & (P.cr.day <= Ty)].groupby("against_invoice").net_value.sum()
        pattern = float(((ult - cum) * o.net_value.values).sum())
        elr = float((ult * o.net_value.values).sum() - o.invoice_no.map(done).fillna(0).sum())
        later = float(P.cr[(P.cr.day > Ty) & (P.cr.reason_code == "RET") & P.cr.against_invoice.isin(o.invoice_no)].net_value.sum())
        return pattern, elr, later
    bt_m = {y: remainder_methods(C.dnum(dt.date(y, 10, 31))) for y in (2024, 2025)}
    p26, e26, _ = remainder_methods(T)
    check("SF15 the credit still to come: the share still to come after each line's age back-tests within 1 per cent at both "
          "year ends, while expected ultimate less credits already given misses 31 October 2025 by more than 10 per cent",
          all(abs(p / l - 1) <= 0.01 for p, e, l in bt_m.values()) and (bt_m[2025][1] / bt_m[2025][2] - 1) > 0.10,
          "; ".join("%d pattern %+.1f%%, ultimate less credited %+.1f%%" % (y, 100 * (p / l - 1), 100 * (e / l - 1)) for y, (p, e, l) in bt_m.items())
          + "; at 2026 %.0f against %.0f" % (p26, e26))
    f26 = rec[rec.date.map(C.in_fy2026)].copy()
    fin26 = C.reinspection_final(P, rec).set_index("tote").pulped
    allh = rec[rec.hurts_tote != ""].copy()
    Hh = allh.groupby("hurts_tote").grade_hurt.sum()
    allh["fr"] = [fin26.get(t, 0) * h / Hh[t] if Hh.get(t, 0) else 0.0 for t, h in zip(allh.hurts_tote, allh.grade_hurt)]
    lr = {}
    for t, g in allh.groupby("hurts_tote"):
        base = np.floor(g.fr.values)
        rem = int(round(g.fr.sum() - base.sum()))
        base[np.argsort(-(g.fr.values - base))[:rem]] += 1
        lr.update(dict(zip(g.index, base)))
    f26["w"] = f26.grade_unsaleable + np.array([lr.get(i, 0.0) for i in f26.index])
    chw = f26.groupby("channel").agg(w=("w", "sum"), q=("qty_received", "sum"))
    fmw = f26.groupby("fmt").agg(w=("w", "sum"), q=("qty_received", "sum"))
    whole = {**{("ch", k): round(100 * chw.loc[k, "w"] / chw.loc[k, "q"], 1) for k in chw.index},
             **{("fm", k): round(100 * fmw.loc[k, "w"] / fmw.loc[k, "q"], 1) for k in fmw.index}}
    gS16 = CE.routes_scrapped(P)["golden"]
    check("SF16 a tote's pulped copies shared in whole copies (largest remainder) instead of fractions: the same shares in every cell",
          all(whole.get(k) == v for k, v in gS16.items()))

    # ---------------------------------------------------------------- the link the step reads
    t = P.titles.assign(c=P.titles.contributor.str.lower(), k=P.titles.title.str.lower())
    naive = t[t.fmt == "Hardback"].merge(t[t.fmt == "Paperback"], on=["c", "k"])
    check("F the hardback-to-paperback link needs normalising: an exact title and contributor join finds under 60 per cent",
          len(naive) < 0.6 * len(L), "%d of %d" % (len(naive), len(L)))
    true_links = {(W.eds[i].isbn, W.eds[e.successor - 1].isbn) for i, e in enumerate(W.eds) if e.fmt == "Hardback" and e.successor is not None
                  and W.eds[e.successor - 1].fmt == "Paperback"}
    got = set(zip(L.isbn_hb, L.isbn_pb))
    on_master = {(a, b) for a, b in true_links if a in set(P.titles.isbn) and b in set(P.titles.isbn)}
    check("F the normalised link finds every hardback's own paperback on the master and nothing else",
          got == on_master, "%d found, %d true" % (len(got), len(on_master)))
    q26 = L[(L.pub_hb >= dt.date(2026, 8, 1)) & (L.pub_hb <= C.YE)]
    check("F most autumn 2026 hardbacks have their paperback within 8 months", (q26.months <= 8).mean() >= 0.8,
          "%d of %d" % ((q26.months <= 8).sum(), len(q26)))
    hist = L[(L.pub_hb >= dt.date(2021, 8, 1)) & (L.pub_hb < dt.date(2025, 11, 1))]
    check("F earlier hardbacks with a paperback that close exist in the record, a minority",
          10 <= (hist.months <= 8).sum() and (hist.months <= 8).mean() <= 0.2, "%d of %d" % ((hist.months <= 8).sum(), len(hist)))

    # ---------------------------------------------------------------- shock: the step is not the pack's loudest movement
    hb = P.inv[(P.inv.fmt == "Hardback") & (P.inv.terms == "SOR")]
    pub = dict(zip(P.titles.isbn, P.titles.pub))
    hb = hb.assign(pub=hb.isbn.map(pub))
    first = hb[(hb.date - hb.pub).map(lambda x: abs(x.days) <= 10)]
    by = first.groupby(first.pub.map(lambda d: d.year if d.month >= 8 else None)).qty.sum().dropna()
    check("X shock: the autumn 2026 hardbacks' subscription copies sit inside the earlier autumns' range",
          2026 in by.index and by.loc[2026] <= by.drop(2026).max() * 1.15, by.round().to_dict().__repr__())

    # ---------------------------------------------------------------- the asks
    world_rec = None
    Sx = RC.shipped_receipts(RC.Records(W))
    tr = Sx[(~Sx.double) & (~Sx.resent) & (Sx.eid >= 0)].copy()
    tr["d"] = tr.day.map(RC.day_date)
    tr = tr[tr.d.map(C.in_fy2026)]
    tch = tr.aid.map(lambda a: next(x.channel for x in W.accounts if x.aid == a))
    tg = tr.groupby([tch, tr.d.map(C.fy_quarter)]).qty.sum()
    check("A fair: the golden copies received equal the copies that came in, every cell", all(int(tg.get(k, 0)) == v for k, v in gA.items()))
    check("A fair: the second bookings the golden drops are exactly the shipped second bookings",
          set(Sx[Sx.double].delivery_no) == set(drop), "%d" % len(drop))
    for k in ("A0 every row", "A1 exact duplicates out", "A2 duplicates out, our titles", "A3 + repeated RA line and quantity out",
              "A3g + repeated RA line, quantity and grades out", "A3u + repeated delivery (every line, grades) out",
              "A4 + capped at the authorised copies", "A5 ledger credits for returns"):
        h, n = CE.hits(A[k], A["golden"])
        check("A device: route '%s' misses half the cells or more" % k, h <= n // 2, "%d of %d" % (h, n))
    check("A no two cells equal and no total a round hundred", len(set(gA.values())) == len(gA) and sum(gA.values()) % 100 != 0)
    for k in [k for k in S if k != "golden"]:
        h, n = CE.hits(S[k], S["golden"])
        if k.startswith("C5"):
            print("INFO C hazard: route '%s' keeps %d of %d (other publishers' copies move the received ask, not these shares)" % (k, h, n))
            continue
        if k.startswith("C8"):
            check("C device: the full includer still misses a block of the shares (two or more)", n - h >= 2, "%d of %d" % (h, n))
            continue
        check("C device: route '%s' misses half the cells or more" % k, h <= n // 2, "%d of %d" % (h, n))
    fin = C.reinspection_final(P, rec)
    check("C fair: every tote's re-inspection resolves against the hurts put into it", not fin.attrs["unresolved"])
    ri_true = RC.Records(W).reinspect
    rt = ri_true[ri_true.day <= (K.LAST_DATA - K.DAY0).days].set_index("tote").qty_pulped
    check("C fair: the resolved pulped count is each tote's own, every tote", all(int(rt.get(tt, -1)) == int(p) for tt, p in zip(fin.tote, fin.pulped)))
    multi = P.ri.groupby("tote").size()
    check("C the re-inspection holds both kinds of repeated tote (sessions and recounts)", (multi > 1).sum() >= 40, "%d" % (multi > 1).sum())

    # ---------------------------------------------------------------- separation: the call reads no device row
    class NoDevices:
        pass
    Q = NoDevices()
    Q.__dict__.update({k: v for k, v in P.__dict__.items() if k not in ("rec", "ri", "ra", "panel")})
    g2 = C.golden_allowance(Q)[0]
    check("S the call reads neither distributor file, nor the panel: same allowance without them", abs(g2 - gold) < 1e-6)
    check("S zero device rows in the call's population (the ledger has no second booking, over-send or other publisher)",
          not P.inv.isbn.str.startswith("97818914").any() and not P.cr.isbn.str.startswith("97818914").any())

    # ---------------------------------------------------------------- realism and the input gates
    files = sorted(os.listdir(TARGET))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("G ten or more files", len(files) >= 10, "%d" % len(files))
    check("G three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    check("G a file of 25,000 rows or more", meta["input_gates"]["largest_file_rows"] >= 25000, str(meta["input_gates"]["largest_file_rows"]))
    check("G two or more distractors named in metadata.json and shipped", len(meta["distractor_files"]) >= 2 and
          all(f in files for f in meta["distractor_files"]))
    check("G no file describes the data (readme, dictionary, notes, manifest)",
          not any(w in f.lower() for f in files for w in ("readme", "dictionary", "notes", "manifest", "schema", "glossary")))
    from openpyxl import load_workbook
    sheets = []
    for f in files:
        if f.endswith(".xlsx"):
            wb = load_workbook(os.path.join(TARGET, f), read_only=True)
            sheets += [s.lower() for s in wb.sheetnames]
    check("G no notes, readme or dictionary sheet", not any(s in ("notes", "readme", "read me", "dictionary", "about") for s in sheets))
    tmp = tempfile.mkdtemp()
    try:
        for f in files:
            if f not in meta["distractor_files"]:
                shutil.copy(os.path.join(TARGET, f), tmp)
        import deliver
        R2 = deliver.compute(tmp)
        same = abs(R2["total"] - gold) < 1e-6 and R2["recv"] == gA
        check("G deleting the distractors moves no graded figure", same)
    finally:
        shutil.rmtree(tmp)
    last = max(P.inv.date.max(), P.cr.date.max(), P.rec.date.max(), P.ra.date.max())
    check("X no record after the pack's last working day", last <= K.LAST_DATA, str(last))
    check("X personas from guard.py names only", set(K.PEOPLE.values()) == {"Hilary Singh", "Marc Hudson", "Jade Hewitt"})
    vc = P.rec.qty_received.value_counts(normalize=True)
    check("X the receipts' quantities spread (no single size over a quarter of the rows)", vc.max() < 0.25, "%.2f" % vc.max())
    gold_files = sorted(os.listdir(os.path.join(TASK, "golden")))
    check("G goldens: the workbook and the one-page note", gold_files == ["returns_allowance_FY2026.xlsx", "returns_allowance_note.pdf"])
    from pypdf import PdfReader
    check("G the note is one page", len(PdfReader(os.path.join(TASK, "golden", "returns_allowance_note.pdf")).pages) == 1)
    print("%d failed" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
