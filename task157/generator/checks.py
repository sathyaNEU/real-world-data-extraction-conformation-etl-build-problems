"""task157 checks: the call and its corridor, the three rules executed on the generator's clean truth, the shipped HOW
sentences, every semantic fork row, the closure axes that can move, the ladder and its out-of-sample record, both asks
with their stops and devices, the realism sweep, the input gates and the distractors. Run by build.py after the
goldens are written; exits 1 on any failure.

    python3 task157/generator/checks.py"""
from __future__ import annotations

import copy
import csv
import datetime as dt
import json
import math
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import deliver as DL        # noqa: E402
import docs as DOC          # noqa: E402
import ops as OP            # noqa: E402
import records as R         # noqa: E402
import world as WD          # noqa: E402

TASK = os.path.dirname(HERE)
RESULTS = []
GOLD_FUND, GOLD_DRIVERS = 1650000, 4700
RUNG_FUND = {"R0": 1450000, "R0b": 1350000, "R1": 1500000, "R2a": 1450000, "R2b": 1500000, "R2c": 1450000,
             "R2d": 1550000, "R2e": 1600000}
EXPECT_A = {2025: dict(never=12950.0, net=889350.0, drivers=2541, main=900900.0, later=5950.0, recovered=4550.0),
            2026: dict(never=16100.0, net=1038450.0, drivers=2966, main=1053500.0, later=7350.0, recovered=6300.0)}
EXPECT_B = {6: (446, 313, 263), 7: (448, 322, 274), 8: (500, 350, 294), 9: (423, 311, 255), 10: (481, 338, 286)}
PEOPLE_OK = {"Gary Mathews", "Kathy Sherman", "Jesse Velasquez", "Melvin Harrell"}
MAIN_FILES = [R.F_LEGACY, R.F_ACTIVITY, R.F_CROSSWALK, R.F_ACCOUNTS, R.F_RUN26, R.F_ADJ, R.F_APPS, DOC.F_TERMS,
              DOC.F_EMAIL]
DEVICE_FILES = [R.F_EVENTS, R.F_RETURNS, R.F_ORDERS]


def ok(label, cond, detail=""):
    RESULTS.append((bool(cond), label, detail))
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))


def rows(target, f):
    return C.rd(target, f)


def pdf_text(path):
    import pypdf
    return "\n".join(pg.extract_text() for pg in pypdf.PdfReader(path).pages)


def docx_text(path):
    import docx
    return "\n".join(p.text for p in docx.Document(path).paragraphs)


def flat_text(target):
    out = {}
    for f in os.listdir(target):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = pdf_text(p)
        elif f.endswith(".docx"):
            out[f] = docx_text(p)
        elif f.endswith((".md", ".eml", ".log")):
            out[f] = open(p, encoding="utf-8").read()
    return out


def linked_copy(target, tmp, skip=(), replace=None):
    os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(target):
        if f in skip:
            continue
        if replace and f in replace:
            continue
        os.link(os.path.join(target, f), os.path.join(tmp, f))
    for f, (cols, rws) in (replace or {}).items():
        K.write_csv(os.path.join(tmp, f), cols, rws)
    return tmp


def fund_of(target, **kw):
    D = C.load(target)
    return C.fund(D, **kw)


def clean_pack(W, O, S, D):
    """The generator's clean truth in calc's shape: every account's completed trips by month from the world itself
    (one id space, no layouts, no crosswalk, no zero-trip rows), the extract's cut on 3 January 2027, and last year's
    qualifiers from the world (eligible accounts at 40 completed trips)."""
    P = C.Pack()
    P.ids = list(D.ids)
    P.idx = dict(D.idx)
    P.acc = D.acc
    P.months = D.months
    P.mi = D.mi
    k_of = {O.driver_id[k]: k for k in range(O.n_acc)}
    ml, T = OP._monthly(W.trips, 0, K.ASOF_W[2027] + 1)
    assert ml == D.months
    TT = np.zeros((len(P.ids), len(ml)), dtype=np.int32)
    for i, d in enumerate(P.ids):
        k = k_of[d]
        if k < W.n:
            TT[i] = T[k]
    P.T = TT
    P.A = TT > 0
    P.row = P.A
    P.first_m = np.where(P.A.any(1), P.A.argmax(1), 10 ** 6)
    P.apps = D.apps
    q = {}
    for y in K.GUARANTEE_YEARS:
        v = np.zeros(len(P.ids), dtype=bool)
        for i, d in enumerate(P.ids):
            k = k_of[d]
            if k < W.n and O.eligible_qual[y][k]:
                v[i] = True
        q[y] = v
    P.qual_override = q
    return P


def run():
    target = os.path.join(TASK, "target")
    golden = os.path.join(TASK, "golden")
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    ptxt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    files = sorted(os.listdir(target))
    texts = flat_text(target)
    flat = "\n".join(texts.values())
    flat1 = re.sub(r"\s+", " ", flat)
    D = C.load(target)
    F = C.fund(D)
    L = C.ladder(D)
    BT = C.backtest(D)
    A = C.ask_a(D)
    B = C.ask_b(D)

    # ------------------------------------------------------------------ the call and its corridor
    ok("CALL the fund is %s and the drivers expected to qualify %s" % (K.money(F.fund), "{:,}".format(
        F.drivers_rounded)), F.fund == GOLD_FUND and F.drivers_rounded == GOLD_DRIVERS,
       "expected total %.0f, %.1f drivers" % (F.total, F.drivers))
    ok("CALL mid-bin: the expected total sits %.2f of a $50,000 bin from its edge and the drivers %.2f of a 100-driver "
       "bin (both at least 0.35)" % (K.bin_clearance(F.total, 50000), K.bin_clearance(F.drivers, 100)),
       K.bin_clearance(F.total, 50000) >= 0.35 and K.bin_clearance(F.drivers, 100) >= 0.35)
    sig = F.n_back * F.g_sigma * F.qJ
    lo, hi = F.drivers - sig, F.drivers + sig
    ok("CALL one sigma of the timing ratio (%.4f, binomial on the 2024 to 2026 returns) moves the drivers by %.0f and "
       "leaves both rounded figures unchanged" % (F.g_sigma, sig),
       all(K.round_to(v * K.AMOUNT, 50000) == GOLD_FUND and K.round_to(v, 100) == GOLD_DRIVERS for v in (lo, hi)),
       "%.1f to %.1f" % (lo, hi))
    variants = {
        "ratio 2026 alone": dict(g_years=(2026,)), "ratio 2025 and 2026": dict(g_years=(2025, 2026)),
        "mean of the yearly ratios": dict(g_mean=True), "qualification 2025 and 2026 pooled": dict(q_years=(2025, 2026)),
        "wave on December to March trips": dict(wave_kw=dict(active=(12, 1, 2, 3))),
        "wave on June to October blanks": dict(wave_kw=dict(blank=(6, 7, 8, 9, 10))),
        "wave on January to April trips": dict(wave_kw=dict(active=(1, 2, 3, 4))),
        "wave on rows, not trips": dict(wave_kw=dict(on_rows=True)),
        "December bands in twenties": dict(bands=[1, 20, 40, 60]),
        "December bands in tens": dict(bands=[1, 10, 20, 30, 40, 50, 60, 70, 80]),
        "other returners as a rate": dict(other_as_rate=True), "new drivers as last year's count": dict(new_mode="count"),
        "new drivers on every new qualifier": dict(new_mode="ratio"), "second accounts dropped": dict(drop_dups=True),
    }
    vals = {k: C.fund(D, **kw) for k, kw in variants.items()}
    bad = {k: (v.fund, v.drivers_rounded) for k, v in vals.items() if v.fund != GOLD_FUND or
           v.drivers_rounded != GOLD_DRIVERS}
    ok("CALL C1 convergence: %d defensible constructions of the golden all file $1,650,000 and 4,700 drivers" %
       len(vals), not bad, bad or "%.1f to %.1f drivers" % (min(v.drivers for v in vals.values()),
                                                          max(v.drivers for v in vals.values())))
    gy = np.array([F.g_by_year[y] for y in (2024, 2025, 2026)])
    sd = float(np.std(gy, ddof=1))
    comp_ok = all(K.round_to(F.n_back * g_ * 1.0, 100) == K.round_to(F.n_rest, 100) and
                  K.round_to(F.n_back * F.qD + F.n_back * g_ * F.qJ, 100) == K.round_to(F.back + F.rest, 100)
                  for g_ in (F.g - sd, F.g + sd))
    ok("CALL the stated components hold across the constructions and the winters' own spread of the ratio (sd %.4f): "
       "about %s back, about %.1f, about %s due, about %s of the qualifiers" % (
           sd, DL.about(F.n_back, 100), K.round_half_up(F.g, 1), DL.about(F.n_rest, 100),
           DL.about(F.back + F.rest, 100)),
       comp_ok and all(DL.about(v.n_back, 100) == DL.about(F.n_back, 100) and
                       "%.1f" % K.round_half_up(v.g, 1) == "%.1f" % K.round_half_up(F.g, 1) and
                       DL.about(v.n_rest, 100) == DL.about(F.n_rest, 100) and
                       DL.about(v.back + v.rest, 100) == DL.about(F.back + F.rest, 100) for v in vals.values()))

    # ------------------------------------------------------------------ the ladder
    D2 = C.load(target)
    hyb = C.fund(D2, back_in_bands=True)
    L["R2e"] = hyb.drivers
    rf = {k: K.round_to(L[k] * K.AMOUNT, 50000) for k in RUNG_FUND}
    ok("LADDER every rung files its own fund: %s" % ", ".join("%s %s" % (k, K.money(v)) for k, v in rf.items()),
       rf == RUNG_FUND, rf)
    gap = {k: (F.total - L[k] * K.AMOUNT) / 50000 for k in RUNG_FUND}
    ok("LADDER the golden is the extreme cell: every rung files less, the default path %.1f bins under, the nearest "
       "rival that skips the leading edge (one ratio over every driver back after a break) %.1f bins under" % (
           gap["R0"], gap["R2d"]), all(v > 0 for v in gap.values()) and gap["R0"] >= 3.0 and gap["R2d"] >= 1.5 and
       min(v for k, v in gap.items() if k != "R2e") >= 1.5, {k: round(v, 2) for k, v in gap.items()})
    ok("LADDER the half step (the rest of the wave developed, the drivers already back priced by December trips) "
       "files one bin under, %s" % K.money(rf["R2e"]), rf["R2e"] == GOLD_FUND - 50000 and gap["R2e"] > 0.5)
    bt_dev = {y: BT[y]["development"] / BT[y]["actual"] - 1 for y in (2025, 2026)}
    bt_pool = {y: BT[y]["pool"] / BT[y]["actual"] - 1 for y in (2025, 2026)}
    bt_all = {y: BT[y]["all_ratio_pred"] / BT[y]["all_ratio_actual"] - 1 for y in (2025, 2026)}
    ok("OOS the leading-edge ratio predicted each earlier January's returns within 2 per cent (%s); last year's share "
       "on the drivers still away missed by %s" % (", ".join("%+.1f%%" % (100 * v) for v in bt_dev.values()),
                                                  ", ".join("%+.1f%%" % (100 * v) for v in bt_pool.values())),
       all(abs(v) < 0.02 for v in bt_dev.values()) and all(abs(v) > 0.10 for v in bt_pool.values()))
    def lapsed(y):
        return ~C.roster(D, y) & C.anyin(D, [(y - 1, m) for m in range(1, 12)])
    l24, l25, l26 = lapsed(2024), lapsed(2025), lapsed(2026)
    p25 = l25.sum() * (l24 & D.A[:, D.mi[(2024, 1)]]).sum() / l24.sum()
    a25 = (l25 & D.A[:, D.mi[(2025, 1)]]).sum()
    p26 = l26.sum() * (l25 & D.A[:, D.mi[(2025, 1)]]).sum() / l25.sum()
    a26 = (l26 & D.A[:, D.mi[(2026, 1)]]).sum()
    ok("OOS the default's own pool (a trip from January to November, none in December) carried a year forward missed "
       "January 2025's returns by %+.0f per cent and held January 2026's within %.0f per cent: its rate moves with "
       "who sits in it" % (100 * (p25 / a25 - 1), abs(100 * (p26 / a26 - 1))),
       p25 / a25 - 1 < -0.15 and abs(p26 / a26 - 1) < 0.03)
    brk = {}
    for kk in (2, 3, 4, 6):
        brk[kk] = C.fund(D, wave_kw=dict(break_months=kk))
    ok("OOS a generic pool of drivers back after a k-month break: k = 2 and 3 file %s and %s (%d and %d drivers), k = 4 "
       "and 6 the golden; the winter pool's ratio holds 1.07 to 1.10 in every winter while the k = 2 and 3 pools' run "
       "%.2f to %.2f" % (K.money(brk[2].fund), K.money(brk[3].fund), brk[2].drivers_rounded, brk[3].drivers_rounded,
                         min(min(brk[k].g_by_year.values()) for k in (2, 3)),
                         max(max(brk[k].g_by_year.values()) for k in (2, 3))),
       brk[2].fund < GOLD_FUND and brk[3].fund < GOLD_FUND and brk[4].fund == GOLD_FUND and brk[6].fund == GOLD_FUND
       and all(1.07 <= v <= 1.10 for v in F.g_by_year.values()) and
       all(v < 1.03 for k in (2, 3) for v in brk[k].g_by_year.values()))
    mix = {}
    for kk in (2, 3):
        rows_ = []
        for y in (2024, 2025, 2026, 2027):
            S_, b_, j_ = C.wave(D, y, break_months=kk)
            Sw_, bw_, jw_ = C.wave(D, y)
            r_in = (j_ & jw_).sum() / max(1, (b_ & bw_).sum())
            r_out = (j_ & ~jw_).sum() / max(1, (b_ & ~bw_).sum())
            rows_.append((y, (b_ & bw_).sum() / b_.sum(), r_in, r_out))
        mix[kk] = rows_
    ok("OOS the break pools mix two timings: inside them last winter's drivers return about 1.1 in January for each one "
       "back by December and the rest under 0.25, and last winter's share of the pool's December returns is higher in "
       "2027 (%s) than in any earlier winter (%s), so the pooled ratio carried forward under-sizes the window" % (
           ", ".join("%.2f" % mix[k][-1][1] for k in (2, 3)),
           ", ".join("%.2f to %.2f" % (min(r[1] for r in mix[k][:3]), max(r[1] for r in mix[k][:3])) for k in (2, 3))),
       all(1.07 <= r[2] <= 1.10 and r[3] < 0.25 for k in (2, 3) for r in mix[k][:3]) and
       all(mix[k][-1][1] > max(r[1] for r in mix[k][:3]) for k in (2, 3)))
    ok("OOS the one ratio over every driver back after a break missed by %s, unstable from year to year" % (
        ", ".join("%+.1f%%" % (100 * v) for v in bt_all.values())), max(abs(v) for v in bt_all.values()) > 0.08)
    S25, b25, j25 = C.wave(D, 2025)
    S26, b26, j26 = C.wave(D, 2026)
    q25, q26 = C.qualified(D, 2025), C.qualified(D, 2026)
    r25 = C.band_rates(D, 2025, exclude_back=False)
    bnd = C.band(C.dec_trips(D, 2026))
    by_band = sum(r25[k] * (b26 & (bnd == k)).sum() for k in range(len(C.BANDS)))
    by_own = b26.sum() * (q25 & b25).sum() / b25.sum()
    act = (q26 & b26).sum()
    ok("OOS pricing last winter's drivers already back: their own share a year earlier put 2026's at %.0f against %d "
       "qualifying; December-trip bands put them at %.0f" % (by_own, act, by_band),
       abs(by_own / act - 1) < 0.03 and by_band / act - 1 < -0.10)

    # ------------------------------------------------------------------ the three rules on the clean truth
    W = WD.simulate()
    O = OP.build(W)
    S = R.shape(W, O)
    P = clean_pack(W, O, S, D)
    ok("R1 the field's raw material ships: each account's completed trips by month (the extract) and last year's "
       "payees; the golden's decisive computation reads those rows, and no shipped column marks a seasonal driver, a "
       "return, a return share or a timing ratio",
       not any(re.search(r"season|return_share|timing|wave|returner|cohort", c, re.I) for f in files if
               f.endswith(".csv") for c in open(os.path.join(target, f), encoding="utf-8").readline().split(",")))
    ok("R2 the stitched extract (old layout through the crosswalk, July 2024 in both layouts, re-registrations merged) "
       "equals the clean truth cell for cell", np.array_equal(P.T, D.T))
    FP = C.fund(P)
    ok("R2 the clean truth files the same fund and drivers as the pack (%s, %s)" % (K.money(FP.fund),
                                                                                   FP.drivers_rounded),
       FP.fund == GOLD_FUND and FP.drivers_rounded == GOLD_DRIVERS and abs(FP.drivers - F.drivers) < 1e-6)
    tmp = tempfile.mkdtemp(prefix="c157_", dir=TASK)
    try:
        leg = rows(target, R.F_LEGACY)
        t1 = linked_copy(target, os.path.join(tmp, "nojul"), replace={R.F_LEGACY: (R.LEGACY_COLS, [
            [r[c] for c in R.LEGACY_COLS] for r in leg if r["MONTH"] != "2024-07"])})
        f1 = fund_of(t1)
        ok("R2 the July 2024 overlap mishandled (the old layout's 1 to 14 July dropped) leaves the call", f1.fund ==
           GOLD_FUND and f1.drivers_rounded == GOLD_DRIVERS, "%.1f" % f1.drivers)
        xw = rows(target, R.F_CROSSWALK)
        second = {r["legacy_driver_no"] for r in xw if r["migration_note"]}
        t2 = linked_copy(target, os.path.join(tmp, "norereg"), replace={
            R.F_LEGACY: (R.LEGACY_COLS, [[r[c] for c in R.LEGACY_COLS] for r in leg if r["DRIVER_NO"] not in second]),
            R.F_CROSSWALK: (R.CROSSWALK_COLS, [[r[c] for c in R.CROSSWALK_COLS] for r in xw
                                               if not r["migration_note"]])})
        f2 = fund_of(t2)
        ok("R2 the re-registered drivers' second numbers mishandled (dropped) leaves the call", f2.fund == GOLD_FUND and
           f2.drivers_rounded == GOLD_DRIVERS, "%.1f" % f2.drivers)
        actv = rows(target, R.F_ACTIVITY)
        t3 = linked_copy(target, os.path.join(tmp, "nojan"), replace={R.F_ACTIVITY: (R.ACTIVITY_COLS, [
            [r[c] for c in R.ACTIVITY_COLS] for r in actv if r["activity_month"] != "2027-01-01"])})
        f3 = fund_of(t3)
        ok("SF6 R2 the partial January 2027 (1 to 3 January) dropped files the same fund", f3.fund == GOLD_FUND and
           f3.drivers_rounded == GOLD_DRIVERS, "%.1f" % f3.drivers)
        D4 = C.load(target)
        jan27 = D4.A[:, D4.mi[(2027, 1)]]
        S27, b27, j27 = C.wave(D4, 2027)
        moved = int((S27 & ~b27 & jan27).sum())
        D4.T[:, D4.mi[(2026, 12)]] += np.where(S27 & ~b27 & jan27, D4.T[:, D4.mi[(2027, 1)]], 0)
        D4.A = D4.T > 0
        f4 = C.fund(D4)
        ok("SF6 the %d of last winter's drivers first back on 1 to 3 January counted as already back files the same "
           "fund" % moved, f4.fund == GOLD_FUND and f4.drivers_rounded == GOLD_DRIVERS)
        f5 = vals["wave on rows, not trips"]
        ok("R2 the months a driver went online without completing a trip read as activity leave the call",
           f5.fund == GOLD_FUND and f5.drivers_rounded == GOLD_DRIVERS)
        st = {r["driver_id"]: r["account_status"] for r in rows(target, R.F_ACCOUNTS)}
        D6 = C.load(target)
        gone = np.array([st[d] in ("deactivated", "merged") for d in D6.ids])
        D6.T[gone] = 0
        D6.A = D6.T > 0
        D6.first_m = np.where(D6.A.any(1), D6.A.argmax(1), 10 ** 6)
        f6 = C.fund(D6)
        ok("R2 CLOSURE 19 account status read (deactivated and merged accounts left out) leaves the call; the golden "
           "reads no status", f6.fund == GOLD_FUND and f6.drivers_rounded == GOLD_DRIVERS, "%.1f" % f6.drivers)
        D7 = C.load(target)
        orig = C.central
        C.central = C.parse_utc
        try:
            f7 = C.fund(D7)
        finally:
            C.central = orig
        ok("R2 the onboarding app's UTC times read as Central leave the call", f7.fund == GOLD_FUND and
           f7.drivers_rounded == GOLD_DRIVERS, "%.1f" % f7.drivers)
        # the device files deleted: the call reads none of them
        t8 = linked_copy(target, os.path.join(tmp, "nodev"), skip=set(DEVICE_FILES) | {R.F_RUN25})
        D8 = C.load(t8)
        ok("DEVICE the call reads no payout event, bank return, screening order or 2025 run row: the fund computed "
           "without those files is unchanged to the driver", abs(C.fund(D8).drivers - F.drivers) < 1e-9)
        # distractors
        t9 = linked_copy(target, os.path.join(tmp, "nodistr"), skip=set(meta["distractor_files"]))
        D9 = C.load(t9)
        ok("GATE the call and both asks unchanged with the distractors deleted (%s)" % ", ".join(
            meta["distractor_files"]), C.fund(D9).total == F.total and C.ask_a(D9) == A and C.ask_b(D9) == B)
    finally:
        shutil.rmtree(tmp)

    def easy(Pk):
        """The default path: December's roster at last January's shares by December trips, the approved drivers
        without a trip at last year's share, every driver with a trip in the twelve months to November and none in
        December at last January's return-and-qualify share."""
        return C.ladder(Pk)["R0"]
    e = easy(P)
    ok("R3a the analyst test on the clean truth: every filed rule applied, the easy route files %s, not the golden" %
       K.money(K.round_to(e * K.AMOUNT, 50000)), K.round_to(e * K.AMOUNT, 50000) == RUNG_FUND["R0"])
    LP = C.ladder(P)
    ok("R3b the decisive step alone on the clean truth (the rest of last winter's wave sized from the part back by the "
       "funding date at the earlier winters' ratio, the wave at its own January shares) files the golden, %s" %
       K.money(FP.fund), FP.fund == GOLD_FUND)
    one = {k: K.round_to(LP[k] * K.AMOUNT, 50000) for k in ("R1", "R2a", "R2b", "R2c", "R2d")}
    one["R2e"] = K.round_to(C.fund(P, back_in_bands=True).total, 50000)
    ok("R3b each lower rung's single correction stays wrong on the clean truth: %s" % ", ".join(
        "%s %s" % (k, K.money(v)) for k, v in one.items()), all(v != GOLD_FUND for v in one.values()))
    truth = int(O.eligible_qual[2027].sum())
    ok("R3b the window itself (simulated past the run, never shipped): %d eligible drivers complete 40 trips, %s; the "
       "golden is %.1f per cent from it and the default path %.1f per cent" % (
           truth, K.money(truth * K.AMOUNT), 100 * (F.drivers / truth - 1), 100 * (e / truth - 1)),
       abs(F.drivers / truth - 1) < 0.02 and e / truth - 1 < -0.10 and K.round_to(truth * K.AMOUNT, 50000) == GOLD_FUND)
    # no copied block: no two accounts share a trip history of twelve or more active months
    seen, rep = set(), 0
    for i in range(D.T.shape[0]):
        if D.A[i].sum() >= 12:
            key = D.T[i].tobytes()
            rep += key in seen
            seen.add(key)
    ok("R3c no copied block: no two accounts with twelve or more active months share a trip history", rep == 0, rep)
    money_docs = set(re.findall(r"\$[0-9]+(?:,[0-9]{3})*", flat))
    ok("R3c no document states a fund, a count of drivers coming back or a qualifier forecast: the only dollar figures "
       "in the documents are the guarantee, finance's step and the referral bonus", money_docs <= {"$350", "$50,000"},
       sorted(money_docs))

    # ------------------------------------------------------------------ HOW, executed literally
    how = {
        "pays": "Larch pays $350 to every eligible driver who completes 40 trips between 00:00 on Monday 4 January 2027 "
                "and 23:59 on Sunday 31 January 2027, Central time.",
        "eligible": "The guarantee is open to every driver whose Larch account is approved by 23:59 on Sunday 3 January "
                    "2027 and is in good standing, including drivers returning to Larch after time away and approved "
                    "drivers who take their first trip during the guarantee.",
        "trip": "A completed trip is a trip the rider completed and paid for.",
        "once": "A driver who drives on more than one account is paid once, and a second payment is recovered.",
        "expected": "What I need from you is the expected total the guarantee will pay for 4 to 31 January: $350 for "
                    "every eligible driver we expect to complete 40 trips, including the drivers who aren't driving "
                    "right now, returning and new, since the terms pay them the same way.",
        "rounding": "Treasury moves money in $50,000 steps, so round it to the nearest $50,000, and send the number of "
                    "drivers you expect to qualify with it.",
        "count": "It pays $350 to every account the payments system counts at 40 completed trips at 23:59 on the Sunday "
                 "after the window; only accounts approved by the Sunday before the window take part.",
    }
    missing = [k for k, v in how.items() if v not in flat1]
    ok("HOW the shipped sentences fixing what is counted are quoted from the pack (population with returning and new "
       "drivers, outcome, window, unit, rounding, eligibility, who was paid)", not missing, missing)
    cue = re.findall(r"season|laid off|layoff|lay-off|\btrades?\b|construction|landscap|\bwave\b|return rate|"
                     r"drivers? (?:\w+ ){0,3}(?:come|coming) back|returns? (?:in|by) (?:january|december|november)|"
                     r"\btiming\b|\bratio\b|campaign recruits|winter recruits", flat, re.I)
    ok("HOW no shipped sentence names a wave, a season, layoffs, a return rate, a timing ratio or how many drivers "
       "come back", not cue, cue)
    ok("HOW executed word for word the filed sentences give the estimand only: the fund needs a forecast of who drives "
       "the window, and the easy method on the same literal estimand files %s" % K.money(RUNG_FUND["R0"]),
       not cue and RUNG_FUND["R0"] != GOLD_FUND)
    ok("HOW the prompt asks the expected need at go-live and names no method, wave or return",
       "need in its account when it goes live" in ptxt and not re.search(r"season|\bwave\b|returning|campaign|"
                                                                          r"back on|come back|\bratio\b|cohort", ptxt,
                                                                          re.I))

    # ------------------------------------------------------------------ the semantic fork table
    cover = K.round_to((F.drivers + 2 * sig) * K.AMOUNT, 50000)
    ok("SF1 a cover figure (the expected total plus two sigma) files %s; finance's email asks the expected total and "
       "says not to pad it" % K.money(cover), cover != GOLD_FUND and "Please don't pad it" in flat1 and
       how["expected"] in flat1)
    ok("SF2 SF9 each person once: second accounts dropped from last year's qualifiers files the same fund and drivers",
       vals["second accounts dropped"].fund == GOLD_FUND)
    D10 = C.load(target)
    canc = {}
    for r in rows(target, R.F_ACTIVITY):
        if int(r["trips_cancelled_by_driver"]) > 0:
            canc[(r["driver_id"], r["activity_month"][:7])] = True
    for (d, m) in canc:
        D10.A[D10.idx[d], D10.mi[(int(m[:4]), int(m[5:7]))]] = True
    f10 = C.fund(D10)
    ok("SF3 activity read as trips accepted (a driver cancellation counts as activity) files the same fund; the terms "
       "count completed trips", f10.fund == GOLD_FUND and f10.drivers_rounded == GOLD_DRIVERS and how["trip"] in flat1,
       "%.1f" % f10.drivers)
    ok("SF4 the window is the terms' four weeks on Central time; the golden reads last year's payees, never a count of "
       "window trips, so calendar January or ISO weeks file the same", how["pays"] in flat1)
    r0b = K.round_to(L["R0b"] * K.AMOUNT, 50000)
    ok("SF5 drivers not on the road included (terms and email); December's roster alone files %s" % K.money(r0b),
       how["eligible"] in flat1 and r0b < GOLD_FUND)
    late_ok = int((W.qual[2026] & ~O.eligible_qual[2026]).sum())
    ok("SF12 the drivers the guarantee can pay are accounts approved by the Sunday before the window: %d drivers who "
       "completed 40 trips in the 2026 window on accounts approved later were not paid, and the terms and the prompt "
       "('every eligible driver') rule them out" % late_ok,
       late_ok > 0 and "Accounts approved from Monday 4 January take part in the next guarantee." in flat1 and
       "every eligible driver" in ptxt and not any(O.eligible_qual[2026][k] for k in np.nonzero(
           W.qual[2026] & ~O.eligible_qual[2026])[0]))
    seg = sum(int(K.round_half_up(x)) for x in (F.nonwave, F.back, F.rest, F.other, F.new))
    ceil = 50000 * math.ceil(F.total / 50000)
    ok("SF7 the rounding path: segments rounded first (%d drivers) or a ceiling to the next step (%s) file the same "
       "fund" % (seg, K.money(ceil)), K.round_to(seg * K.AMOUNT, 50000) == GOLD_FUND and ceil == GOLD_FUND)
    D11 = C.load(target)
    D11.late = {2025: [], 2026: []}
    D11.recoveries = []
    f11 = C.fund(D11)
    ok("SF8 last year's qualifiers read as the main run alone files the same fund and drivers", f11.fund == GOLD_FUND
       and f11.drivers_rounded == GOLD_DRIVERS, "%.1f" % f11.drivers)
    fk = C.fund(D, kept=True)
    s_trips = ("Larch pays $350 to every eligible driver who completes 40 trips between 00:00 on Monday 4 January 2027 "
               "and 23:59 on Sunday 31 January 2027, Central time.")
    s_leave = "Returned payouts and recoveries come back to the account afterwards, so leave them out."
    ok("SF13 last year's qualifiers read as the drivers who kept a payment (Ask A's basis, returned-and-never-resent "
       "payees dropped) files %s and %d drivers; ruled out because a driver qualifies by completing 40 trips whatever "
       "happened to the payment (the terms) and finance leaves returns out (the email), and the payout notes count "
       "accounts at 40 completed trips" % (K.money(fk.fund), fk.drivers_rounded),
       fk.fund == GOLD_FUND - 50000 and fk.drivers_rounded == GOLD_DRIVERS - 100 and s_trips in flat1 and
       s_leave in flat1 and how["count"] in flat1, "%.1f" % fk.drivers)
    end26 = dt.datetime(2026, 1, 4, 23, 59, 59)
    appr = [a for a in D.apps if a["status"] in ("approved", "approval_lapsed") and a["decision_at_utc"] and
            C.central(a["decision_at_utc"]) <= end26 and
            (dt.date(2026, 1, 4) - C.central(a["decision_at_utc"]).date()).days <= 90]
    no_dec = [a for a in appr if not a["first_trip_at_utc"] or C.central(a["first_trip_at_utc"]) >= dt.datetime(2026, 1, 1)]
    no_jan4 = [a for a in no_dec if not a["first_trip_at_utc"] or C.central(a["first_trip_at_utc"]) > end26]
    paid_n = sum(1 for a in no_jan4 if q26[D.idx[a["driver_id"]]])
    ok("NEW the 2026 base for the approved drivers without a trip is the %d accounts approved in the 90 days to 4 January "
       "2026 with no first trip by the end of that day (%d paid); the %d with no trip through December include %d that "
       "first drove on 1 to 4 January, and both bases file the same fund and drivers" % (
           len(no_jan4), paid_n, len(no_dec), len(no_dec) - len(no_jan4)),
       len(no_jan4) == F.apn26 and paid_n == F.new26_from_pool and
       K.round_to((F.drivers - F.new + F.apn27 * paid_n / len(no_dec)) * K.AMOUNT, 50000) == GOLD_FUND and
       K.round_to(F.drivers - F.new + F.apn27 * paid_n / len(no_dec), 100) == GOLD_DRIVERS and
       "An approval lapses 90 days after it is given if the driver has not taken a trip" in flat1 and
       "first_trip_at_utc is that account's first completed trip" in flat1)
    amounts = {r["amount_usd"] for r in rows(target, R.F_RUN26)} | {r["amount_usd"] for r in rows(target, R.F_ADJ)}
    ok("SF10 every payout in both years is $350 and the terms say the guarantee has run on these terms since 2025",
       {abs(float(a)) for a in amounts} == {350.0} and "The guarantee has run on these terms each January since 2025"
       in flat1)
    ok("SF11 last winter's drivers on December to March trips, on June to October blanks or on January to April trips "
       "file the same fund", all(vals[k].fund == GOLD_FUND and vals[k].drivers_rounded == GOLD_DRIVERS for k in (
           "wave on December to March trips", "wave on June to October blanks", "wave on January to April trips")))

    # ------------------------------------------------------------------ closure axes that can move
    ok("CLOSURE 8 the winters the ratio is read from (2026 alone, 2025 and 2026, 2024 to 2026, the mean) file the same "
       "fund", all(vals[k].fund == GOLD_FUND for k in ("ratio 2026 alone", "ratio 2025 and 2026",
                                                       "mean of the yearly ratios")))
    ok("CLOSURE 6 13 the denominators and the order of segments (bands in tens or twenties, other returners as a count "
       "or a rate) file the same fund", all(vals[k].fund == GOLD_FUND for k in (
           "December bands in twenties", "December bands in tens", "other returners as a rate")))
    keys = [(r["activity_month"], r["driver_id"]) for r in actv]
    ok("CLOSURE 15 16 no duplicate driver-month in either layout; every legacy number maps to one driver_id",
       len(set(keys)) == len(keys) and len({r["legacy_driver_no"] for r in xw}) == len(xw) and
       len({(r["MONTH"], r["DRIVER_NO"]) for r in leg}) == len(leg))

    # ------------------------------------------------------------------ Ask A
    ok("ASK A the golden: %s" % "; ".join("%d never %s net %s drivers %d" % (y, K.money(A[y]["never"]),
                                                                            K.money(A[y]["net"]), A[y]["drivers"])
                                          for y in (2025, 2026)),
       all(A[y][k] == EXPECT_A[y][k] for y in (2025, 2026) for k in EXPECT_A[y]), A)
    s1 = C.ask_a(D, net_every_return=True)
    graded = [(y, k) for y in (2025, 2026) for k in ("never", "net", "drivers")]
    miss1 = [x for x in graded if s1[x[0]][x[1]] != A[x[0]][x[1]]]
    ok("ASK A S1/S2 every bank return netted (the battery's work otherwise right) misses all 6 graded figures (A1)",
       len(miss1) == 6, miss1)
    s3 = C.ask_a(D, book_by_run=True)
    ok("ASK A S3 recoveries booked by run date move both nets (HA2: a 2025 recovery in the March 2026 run)",
       s3[2025]["net"] != A[2025]["net"] and s3[2026]["net"] != A[2026]["net"])
    s5 = C.ask_a(D, later_subtracted=True)
    ok("ASK A 'net of later runs' read as later runs subtracted moves both nets ($%s, $%s); the payout notes add them: "
       "a guarantee's cost is what its runs paid, less returns never paid out again and recoveries" % (
           "{:,.0f}".format(s5[2025]["net"]), "{:,.0f}".format(s5[2026]["net"])),
       s5[2025]["net"] != A[2025]["net"] and s5[2026]["net"] != A[2026]["net"] and
       "A guarantee's cost is what its runs paid, less payouts the bank returned that were never paid out again and "
       "less what was recovered" in flat1)
    s4 = C.ask_a(D, by_account=True)
    ok("ASK A HA3 accounts counted for people: the 2026 drivers paid move (a merged second account not yet recovered)",
       s4[2026]["drivers"] != A[2026]["drivers"])
    ev = rows(target, R.F_EVENTS)
    resent = len({r["payout_id"] for r in ev if r["detail"] == "payout details updated"})
    rets = [r for r in rows(target, R.F_RETURNS) if r["company_entry_description"] == "GUARANTEE"]
    ok("ASK A A1 is real and silent: %d guarantee payouts were sent again after a return; every bank return line is a "
       "true return and every resend sits in the events log under the same payout id" % resent,
       resent >= 40 and all(r["individual_id"] in D.payout_year for r in rets) and
       not re.search(r"resen|sent again|re-?present|same payout id", flat, re.I))
    # Ask B
    ok("ASK B the golden: %s" % "; ".join("%d %d/%d/%d" % (m, B[m]["applied"], B[m]["approved"], B[m]["first_trip"])
                                          for m in range(6, 11)),
       all((B[m]["applied"], B[m]["approved"], B[m]["first_trip"]) == EXPECT_B[m] for m in range(6, 11)))
    sb3 = C.ask_b(D, approved=("approved",))
    moved = [m for m in range(6, 11) if sb3[m]["approved"] != B[m]["approved"]]
    ok("ASK B 'approved' read as the approved status alone (lapsed approvals left out) moves the approvals of %d months; "
       "the counting notes count approval on any application and the data notes define approval_lapsed as approved" %
       len(moved), len(moved) >= 3 and "approved means approved on any of their applications" in flat1 and
       "approval_lapsed (approved, the approval lapsed 90 days after it was given without a trip)" in flat1)
    sb1 = C.ask_b(D, month_from="submitted", tz="utc", persons="application")
    sb2 = C.ask_b(D, month_from="submitted")
    keysb = [(m, k) for m in range(6, 11) for k in ("applied", "approved", "first_trip")]
    m1 = [x for x in keysb if sb1[x[0]][x[1]] != B[x[0]][x[1]]]
    m2 = [x for x in keysb if sb2[x[0]][x[1]] != B[x[0]][x[1]]]
    ok("ASK B S1 application rows by their UTC submitted month miss %d of 15; S2 the battery's work (Central time, "
       "people through the vendor's candidates) on the app's submitted time misses %d of 15 (B1)" % (len(m1), len(m2)),
       len(m1) == 15 and len(m2) == 15, (m1, m2))
    od = {r["client_reference"]: C.parse_utc(r["ordered_at"]) for r in rows(target, R.F_ORDERS)}
    later = sum(1 for r in rows(target, R.F_APPS) if (C.parse_utc(r["submitted_at_utc"]) - od[r["application_id"]])
                .total_seconds() > 86400)
    ok("ASK B B1 is real and silent: %d applications show a submitted time more than a day after their screening "
       "order; every submitted time is complete and before its decision" % later,
       later > 1500 and all(not r["decision_at_utc"] or r["submitted_at_utc"] < r["decision_at_utc"]
                            for r in rows(target, R.F_APPS)) and
       not re.search(r"overwrit|latest submission|last submission", flat, re.I))
    ok("ASK the asks' rows are outside the call: the fund reads no event, return or order (see DEVICE) and no "
       "submitted time", True)

    # ------------------------------------------------------------------ the write-up and the goldens
    import subprocess
    fc = subprocess.run([sys.executable, os.path.join(TASK, "..", ".claude", "skills", "determinism-check",
                                                      "figures_check.py"), TASK, "--quiet"],
                        capture_output=True, text=True)
    ok("WRITEUP figures_check: every number in blocks 1 to 4 is in figures.json", fc.returncode == 0,
       fc.stdout.strip()[-200:])
    # SF15: the out-of-sample line has to say what its per cent is a per cent of, or it reads as the fund's own
    # precision. The portal's second determinism judge read "within 2 per cent" that way and called the headline
    # unforced on a band of about plus or minus 94 drivers. The counts it is an error of are a few hundred.
    _bt_counts = [str(int(K.round_half_up(BT[y]["development"]))) for y in (2025, 2026)] + \
                 [str(int(BT[y]["actual"])) for y in (2025, 2026)]
    ok("SF15 the out-of-sample sentence names the return counts its per cent is of (%s), so the referent is the "
       "returns and not the fund" % ", ".join(_bt_counts),
       all(c in sub for c in _bt_counts) and re.search(r"within \d+ per cent of the count", sub) is not None,
       [c for c in _bt_counts if c not in sub])
    ok("SF15 no sentence in the write-up attaches a per cent band to the fund or the driver count",
       not re.search(r"\b(?:fund|drivers)\b[^.]{0,60}within \d+ per cent", sub, re.I))
    ok("WRITEUP the call, the components and the rivals' clauses carry no rival figure",
       not re.search(r"\$1,(?:35|45|50|55|60)0,000", sub))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(golden, DL.XLSX), data_only=True)
    ok("GOLDEN the workbook names its sheets and states the fund and the drivers",
       wb.sheetnames == ["Fund", "Earlier winters", "Guarantees 2025 and 2026", "Onboarding Jun-Oct 2026", "Notes"] and
       wb["Fund"]["D5"].value == GOLD_FUND and wb["Fund"]["D6"].value == GOLD_DRIVERS)
    w4 = wb["Onboarding Jun-Oct 2026"]
    ok("GOLDEN the onboarding table carries Ask B", all(
        (w4.cell(row=5 + i, column=2).value, w4.cell(row=5 + i, column=3).value, w4.cell(row=5 + i, column=4).value)
        == EXPECT_B[m] for i, m in enumerate(range(6, 11))))
    from pptx import Presentation
    prs = Presentation(os.path.join(golden, DL.PPTX))
    st = [" ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame) for s in prs.slides]
    ok("GOLDEN the deck has two slides: the fund stated, then the two guarantees from main run to net cost",
       len(st) == 2 and "$1,650,000" in st[0] and "4,700" in st[0] and any(sh.shape_type == 13 for sh in
                                                                          prs.slides[1].shapes))

    # ------------------------------------------------------------------ realism sweep
    bad_ppl = set(re.findall(r"\b(?:Gary|Kathy|Jesse|Melvin|Mathews|Sherman|Velasquez|Harrell)\b", flat))
    named = set(re.findall(r"(Gary Mathews|Kathy Sherman|Jesse Velasquez|Melvin Harrell)", flat))
    ok("REALISM every persona is from guard.py names: %s" % ", ".join(sorted(named)), named <= PEOPLE_OK and named)
    dash = [f for f, t in texts.items() if "\u2014" in t] + (["submission.md"] if "\u2014" in sub else []) + \
        (["prompt.txt"] if "\u2014" in ptxt else [])
    ok("REALISM no em dash in any document, the prompt or the write-up", not dash, dash)
    tell = re.findall(r"construct|fictional|fictitious|synthetic|generated|this exercise|simulat", flat, re.I)
    ok("REALISM no sentence in the pack says it was built", not tell, tell)
    sig_bytes = []
    for root in (target, golden):
        for f in os.listdir(root):
            b = open(os.path.join(root, f), "rb").read()
            for w in (b"openpyxl", b"python-docx", b"python-pptx", b"ReportLab", b"reportlab", b"matplotlib",
                      b"Matplotlib"):
                if w in b:
                    sig_bytes.append((f, w.decode()))
    ok("REALISM H1 no writer's name in any shipped container or golden", not sig_bytes, sig_bytes)
    late_rows = []
    lim = dt.datetime.combine(K.AS_OF, dt.time(21, 40))
    for f, cols in ((R.F_APPS, ("submitted_at_utc", "decision_at_utc", "first_trip_at_utc")),
                    (R.F_EVENTS, ("event_at_utc",))):
        for r in rows(target, f):
            for c in cols:
                if r[c] and K.from_utc(C.parse_utc(r[c])) > lim:
                    late_rows.append((f, c, r[c]))
    for r in rows(target, R.F_ORDERS):
        for c in ("ordered_at", "completed_at"):
            if r[c] and K.from_utc(C.parse_utc(r[c])) > lim:
                late_rows.append((R.F_ORDERS, c, r[c]))
    acc_max = max(r["last_trip_on"] for r in rows(target, R.F_ACCOUNTS) if r["last_trip_on"])
    ret_max = max(r["return_date"] for r in rows(target, R.F_RETURNS))
    # SF14: the shipped rider demand plan must be able to serve the window it plans. The portal's first
    # determinism judge read it as a trip ceiling, divided the planned pool by the trips a qualifier takes
    # and derived 3,500 drivers against the golden's 4,700. The plan is a declared distractor and nothing in
    # the solution reads it, so what is asserted is that it cannot bind: the arithmetic a judge does on
    # shipped data alone has to clear the golden. Every figure here comes from the pack.
    import openpyxl as _ox
    _wb = _ox.load_workbook(os.path.join(target, R.F_DEMAND), data_only=True)
    _ws = _wb["Q1 2027 weekly"]
    _plan_window = int(sum(_ws.cell(row=5 + k, column=5).value for k in range(4)))
    _act = {}
    for _r in rows(target, R.F_ACTIVITY):
        _act.setdefault(_r["activity_month"], []).append(int(_r["trips_completed"] or 0))
    _dec = _act["2026-12-01"]
    _dec_q = [t for t in _dec if t >= 40]
    _mean_q = sum(_dec_q) / len(_dec_q)
    _cap = int(_plan_window / _mean_q)
    ok("SF14 the plan's January window carries %s completed trips, and divided by December's mean qualifier "
       "trips (%.1f) that is %s qualifiers, clear of the golden's 4,700, so no demand-constrained reading "
       "binds" % (f"{_plan_window:,}", _mean_q, f"{_cap:,}"), _cap > 4700,
       {"plan_window": _plan_window, "mean_qualifier_trips": round(_mean_q, 1), "cap": _cap})
    ok("SF14 the plan's January window is above the last actual month in the pack, December 2026's %s "
       "completed trips, so the plan is not a ceiling under recent actuals" % f"{sum(_dec):,}",
       _plan_window > sum(_dec), {"plan_window": _plan_window, "dec_2026": sum(_dec)})
    _jan3 = sum(_act["2027-01-01"])
    ok("SF14 the first three days of the window already ran %s completed trips, %.0f per cent of the plan's "
       "own daily rate, so the plan reads as a floor on the window and not a cap"
       % (f"{_jan3:,}", 100 * (_jan3 / 3) / (_plan_window / 28)), (_jan3 / 3) > 0.9 * (_plan_window / 28),
       {"jan_1_to_3": _jan3, "plan_daily": int(_plan_window / 28)})

    ok("REALISM H16 no record dated after the extract run (forward dates only in the terms, the email and the demand "
       "plan)", not late_rows and acc_max <= "2027-01-03" and ret_max <= "2026-12-31", late_rows[:3])
    log = texts[DOC.F_LOG]
    in_log = set(re.findall(r"([\w.-]+\.(?:csv|xlsx|pdf|docx|eml|md))", log))
    ok("REALISM H9 the pull log names every shipped file but itself, and the data notes name every other file",
       in_log == set(files) - {DOC.F_LOG} and all(f in texts[DOC.F_NOTES] for f in files if f != DOC.F_NOTES),
       sorted(set(files) - {DOC.F_LOG} - in_log))
    ids_ok = len({r["driver_id"] for r in rows(target, R.F_ACCOUNTS)}) == len(rows(target, R.F_ACCOUNTS)) and \
        len({r["application_id"] for r in rows(target, R.F_APPS)}) == len(rows(target, R.F_APPS)) and \
        len({r["order_id"] for r in rows(target, R.F_ORDERS)}) == len(rows(target, R.F_ORDERS)) and \
        len({r["payout_id"] for r in rows(target, R.F_RUN26)}) == len(rows(target, R.F_RUN26))
    ok("REALISM identifiers unique in every register (accounts, applications, orders, payouts)", ids_ok)
    kpi = DOC.kpi_rows(target)
    ok("REALISM the KPI report reproduces from the extract and never repeats a month's figures",
       len({(r["active"], r["new"], r["trips"]) for r in kpi}) == len(kpi) and
       "Counts are accounts." in texts[DOC.F_KPI])
    ok("REALISM no round headline: the 2026 qualifiers, the main runs and the monthly active drivers are not round",
       int(q26.sum()) % 100 and all(r["active"] % 100 for r in kpi[-6:]), int(q26.sum()))

    # ------------------------------------------------------------------ input gates
    fmts = {f.rsplit(".", 1)[1] for f in files}
    nrows = {f: len(rows(target, f)) for f in files if f.endswith(".csv")}
    ok("GATE %d files, %d formats, the largest %s at %s rows" % (len(files), len(fmts), max(nrows, key=nrows.get),
                                                                 "{:,}".format(max(nrows.values()))),
       len(files) >= 10 and len(fmts) >= 3 and max(nrows.values()) >= 25000)
    ok("GATE two or more distractors named in metadata.json, shipped, none named as one",
       len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]) and
       not any("distract" in f for f in files))
    ok("GATE metadata.json lists every shipped file with a source, date and licence",
       sorted(x["path"] for x in meta["files"]) == files and all(x["source"] and x["license"] for x in meta["files"]))


def main():
    run()
    n_fail = sum(1 for r in RESULTS if not r[0])
    print("\nchecks: %d run, %d failed" % (len(RESULTS), n_fail))
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
