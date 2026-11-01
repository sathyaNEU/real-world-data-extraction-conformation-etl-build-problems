"""Every figure the goldens, the write-up, the checks and the ceiling script use, computed from target/ alone."""
import os
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

import analysis as A
import params as P

SEG_NAMES = [s for s, _ in P.SEGMENTS]
BAND_LABEL = ["Grades 1 to 3", "Grade 4", "Grade 5", "Grade 6", "Grades 7 to 9"]
HALVES = ("H1", "H2")


def rhu(x, places=0):
    """Round half up (the convention every deliverable states)."""
    q = Decimal(1).scaleb(-places)
    return float(Decimal(repr(x)).quantize(q, rounding=ROUND_HALF_UP))


def half_million(x):
    """NZD to NZD million at the nearest 0.5 million."""
    return float(Decimal(repr(x / 1e6 * 2)).quantize(Decimal(1), rounding=ROUND_HALF_UP)) / 2


def ask_a_detail(tdir, **kw):
    """Written off, recovered and net by segment and half (NZD), on the golden's handling unless overridden."""
    import datetime as dt
    reg = A.read_csv(os.path.join(tdir, "nzbn_extract_canterbury_otago_southland_2026-10-12.csv"))
    net = A.ask_a(tdir, reg=reg, **kw)
    by_nzbn = {r["nzbn"]: r for r in reg}
    cm = {r["customer_no"]: r for r in A.read_csv(os.path.join(tdir, "customer_master_extract_2026-10-09.csv"))}
    wo = defaultdict(float)
    for r in A.read_csv(os.path.join(tdir, "write_offs_2023-10_to_2026-09.csv")):
        if r["portfolio"] != "Business":
            continue
        h = A.half(A._d(r["posting_date"]))
        if h:
            seg = P.SEG_OF[by_nzbn[cm[r["customer_no"]]["nzbn"]]["bic_code"][0]]
            wo[(seg, h)] += float(r["amount_nzd"])
    rec = {k: wo[k] - net[k] for k in net}
    return dict(written_off=dict(wo), recovered=rec, net=net)


def ask_b_raw(tdir, **kw):
    out = A.ask_b(tdir, **kw)
    return {b: (n, k) for b, (n, k, _) in out.items()}


def compute(tdir):
    pk, res = A.ladder(tdir)
    tot, seg, per = res["golden"]
    mx = pk.mixes()
    rows = []
    sales_total = other_div = hh = 0.0
    ead_seg = defaultdict(float)
    n_seg = defaultdict(int)
    pd12_w = pds_w = ead_tot = 0.0
    for c in sorted(pk.cust.values(), key=lambda c: (SEG_NAMES.index(P.SEG_OF[c["div"]]), c["cust"])):
        if c["grade"] == "D":
            continue
        s = P.SEG_OF[c["div"]]
        ch, m, loss = per[c["cust"]]
        mix = mx[c["cust"]]
        sales = sum(mix.values())
        own_hh = sum(v for (k, d), v in mix.items() if k == "HH")
        own_b2b = sum(v for (k, d), v in mix.items() if k == "B2B" and d == c["div"])
        oth = sales - own_hh - own_b2b
        sales_total += sales
        other_div += oth
        hh += own_hh
        e = sum(pk.ead(f) for f in c["facs"])
        g = int(c["grade"])
        pd12 = P.GRADE_PD[g] / 100.0
        pds = min(1.0, pd12 * m)
        ead_seg[s] += e
        n_seg[s] += 1
        pd12_w += pd12 * e
        pds_w += pds * e
        ead_tot += e
        rows.append(dict(cust=c["cust"], name=c["name"], nzbn=c["nzbn"], div=c["div"], seg=s, grade=g,
                         pd12=pd12, sales=sales, other_share=(oth / sales if sales else 0.0),
                         hh_share=(own_hh / sales if sales else 0.0), own_change=P.SCENARIO_CHANGE[c["div"]],
                         change=ch, mult=m, pds=pds, ead=e, loss=loss))
    n_default = sum(1 for c in pk.cust.values() if c["grade"] == "D")
    a = ask_a_detail(tdir)
    b = ask_b_raw(tdir)
    F = dict(
        total=tot, total_half_m=half_million(tot),
        seg={s: seg[s] for s in SEG_NAMES}, seg_m1={s: rhu(seg[s] / 1e6, 1) for s in SEG_NAMES},
        r0_total=res["R0_own_division"][0], r0_half_m=half_million(res["R0_own_division"][0]),
        r0_seg_m1={s: rhu(res["R0_own_division"][1][s] / 1e6, 1) for s in SEG_NAMES},
        n_perf=len(rows), n_default=n_default, ead_total=ead_tot, ead_m1=rhu(ead_tot / 1e6, 1),
        ead_seg=dict(ead_seg), n_seg=dict(n_seg),
        sales_total=sales_total, other_share_pct=rhu(100 * other_div / sales_total, 0),
        hh_share_pct=rhu(100 * hh / sales_total, 0),
        pd12_wavg_pct=rhu(100 * pd12_w / ead_tot, 2), pds_wavg_pct=rhu(100 * pds_w / ead_tot, 1),
        ask_a=a, ask_a_k={k: rhu(v / 1e3, 0) for k, v in a["net"].items()},
        ask_b=b, ask_b_share={k: rhu(100.0 * d / n, 1) for k, (n, d) in b.items()},
        rows=rows, ladder={k: v[0] for k, v in res.items()},
        ladder_seg={k: v[1] for k, v in res.items()},
    )
    return F
