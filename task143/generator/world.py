"""The truth behind the pack, before any export is written: the qualification cells of every lot (their formation
trays, their first-100-cycle features, their cycle lives on QP-3), the lot under release cell by cell (formation trays,
incoming inspection, the release test, the packs the line built), and the field that the service records come from.

The generative model of a qualification cell's life on QP-3:
    ln N80 = B0 + B1 (ln dQ - ln 60) + B2 (dR - 1.2) + t[tray] + c[cell]
dQ is the discharge capacity lost from the 10th to the 100th cycle (mAh) and dR the rise in 10-second DC resistance over
the same cycles (milliohm), both as the cycler measures them; t is the formation tray's effect, which the first 100
cycles do not show (the tray's shared formation run and electrolyte fill set when the capacity knee arrives), and c the
cell's own. The tray and cell effects are drawn as stratified normal samples (every lot's trays spread over the whole
distribution, the pooled sample matching the normal in its tails), so that the earlier lots' whole trays measure the
two components without a lucky or unlucky lot."""
from __future__ import annotations

import datetime as dt
import math
from types import SimpleNamespace

import numpy as np
from scipy import stats

import common as K

# ---------------------------------------------------------------------------------------------------- the truth
B0 = 6.88
B1 = -0.45
B2 = -0.060
LNQ_REF = math.log(60.0)
DR_REF = 1.2
SD_TRAY = 0.160          # the tray's share of the life the first 100 cycles do not show
SD_CELL = 0.085          # the cell's own
LOT_LNQ_SD = 0.14        # lot-to-lot spread of the early fade
TRAY_LNQ_SD = 0.020      # a tray's own early fade (the first 100 cycles see almost none of the tray effect)
CELL_LNQ_SD = 0.170
DR_MEAN, DR_SD = 1.20, 0.45
NEW_LOT_SHIFT = 0.215    # ZC2638's early fade sits above every finished lot's but two


def strat_normal(r, n, perm=True):
    """n stratified standard-normal draws: one from each of n equal-probability strata, in random order."""
    u = (np.arange(n) + r.uniform(0.0, 1.0, n)) / n
    z = stats.norm.ppf(u)
    if perm:
        r.shuffle(z)
    return z


def tray_effects(n_lots, trays, lot_lnq):
    """Every finished lot's tray effects: a stratified sample of the pooled distribution (so its tails are the
    normal's), dealt to the lots at random, so each lot's twenty trays are a random draw from it. Of 400 random deals
    the one is kept whose lot means are least correlated with the lots' early fade and spread most like a random
    draw's, so no lot's trays happen to lean with its fade."""
    r = K.rng("tray-effects")
    z = strat_normal(r, n_lots * trays, perm=False)
    target = 1.0 / math.sqrt(trays)
    best, best_score = None, None
    x = np.array(lot_lnq) - np.mean(lot_lnq)
    for _ in range(400):
        p = r.permutation(z)
        m = p.reshape(n_lots, trays).mean(axis=1)
        corr = abs(np.corrcoef(m, x)[0, 1])
        spread = abs(m.std(ddof=1) - target) / target
        score = corr + spread
        if best_score is None or score < best_score:
            best, best_score = p, score
    return [best[l * trays:(l + 1) * trays] * SD_TRAY for l in range(n_lots)]


def lot_levels():
    """Each lot's mean early fade (log scale) and mean resistance rise; the lot under release sits high on fade."""
    r = K.rng("lot-levels")
    lv = {}
    z = strat_normal(r, len(K.LOTS) - 1)
    for i, lot in enumerate(K.LOTS[:-1]):
        lv[lot] = (LOT_LNQ_SD * z[i], r.normal(0.0, 0.08))
    lv[K.NEW_LOT] = (NEW_LOT_SHIFT, 0.03)
    return lv


def true_lnlife(lnq, dr, t, c):
    return B0 + B1 * (lnq - LNQ_REF) + B2 * (dr - DR_REF) + t + c


# ---------------------------------------------------------------------------------------------------- serials
def cell_serial(lot, seq):
    return "%s-%07d" % (lot, seq)


def tray_key(lot, n):
    """Zelvora's formation tray key as its cell data package writes it: T plus five digits before lot ZC2532, the lot
    and the tray number after."""
    if K.LOTS.index(lot) < K.LOTS.index(K.TRAY_KEY_CHANGE):
        return "T%05d" % n
    return "FT%s-%05d" % (lot[2:], n)


# ---------------------------------------------------------------------------------------------------- qualification cells
def qualification_cells(W):
    """The release-test cells of every lot: 20 trays of six, with their features and (for the finished lots and the
    lot under release, in truth) their lives."""
    qlots = K.TRAIN_LOTS + K.OPEN_LOTS + [K.NEW_LOT]
    lv = W.lot_levels
    teff_train = tray_effects(len(K.TRAIN_LOTS), K.TEST_TRAYS, [lv[l][0] for l in K.TRAIN_LOTS])
    cells = []
    for li, lot in enumerate(qlots):
        r = K.rng("qual-cells", lot)
        mq, mr = lv[lot]
        if li < len(K.TRAIN_LOTS):
            te = teff_train[li]
        else:
            te = strat_normal(r, K.TEST_TRAYS) * SD_TRAY
        n = K.TEST_TRAYS * K.TRAY_CELLS
        zq = strat_normal(r, n)
        zc = strat_normal(r, n)
        zr = strat_normal(r, n)
        # the lot's tray numbers: the twenty trays drawn from the lot's A trays (the lot under release draws its own
        # from its tray list in the lot model below)
        if lot == K.NEW_LOT:
            tray_nos = W.new.test_trays
        else:
            tray_nos = sorted(r.choice(np.arange(1, 4300), K.TEST_TRAYS, replace=False).tolist())
        base_seq = int(r.integers(1000, 5000))
        for k in range(K.TEST_TRAYS):
            s = r.normal(0.0, TRAY_LNQ_SD)
            tno = int(tray_nos[k])
            for j in range(K.TRAY_CELLS):
                i = k * K.TRAY_CELLS + j
                lnq = LNQ_REF + mq + s + CELL_LNQ_SD * zq[i]
                dr = DR_MEAN + mr + DR_SD * zr[i]
                if lot == K.NEW_LOT:
                    seq = W.new.tray_cells[tno][j]
                else:
                    seq = base_seq + (tno - 1) * K.TRAY_CELLS + j + 1
                cells.append(SimpleNamespace(lot=lot, tray_no=tno, tray=tray_key(lot, tno), pos=j + 1,
                                             serial=cell_serial(lot, seq), lnq=lnq, dr=dr, t=float(te[k]),
                                             c=float(SD_CELL * zc[i])))
    for c in cells:
        c.lnlife = true_lnlife(c.lnq, c.dr, c.t, c.c)
        c.life = int(round(math.exp(c.lnlife)))
    return cells


# ---------------------------------------------------------------------------------------------------- the release tests
CYCLE_H = 2.70          # QP-3: 1C CC-CV charge, 10 minutes' rest, 1C discharge to 3.00 V, 10 minutes' rest
FLEET_B_FROM = "ZC2506"  # the second cycler fleet took its first lot in February 2025


def qual_tests(W):
    """Each qualification cell's release test: the fleet and channel it ran on, its start, and its first 100 cycles
    as the cycler measured them (discharge and charge capacity, the 10-second DC resistance at half charge, the
    cycle's highest temperature, the cycle's end in UTC). A few tests stopped on a channel fault and continued on
    another channel after a rest, numbered there as a new test."""
    tests = {}
    by_lot = {}
    for c in W.qcells:
        by_lot.setdefault(c.lot, []).append(c)
    interrupted = {("ZC2502", 3), ("ZC2549", 1), ("ZC2610", 4), (K.NEW_LOT, 2)}
    for lot, cells in by_lot.items():
        r = K.rng("qual-tests", lot)
        start_day = K.LOT_START[lot] + dt.timedelta(days=int(r.integers(9, 12)))
        use_b = K.LOTS.index(lot) >= K.LOTS.index(FLEET_B_FROM)
        trays = sorted({c.tray_no for c in cells})
        tray_fleet = {}
        for t in trays:
            tray_fleet[t] = "B" if (use_b and r.random() < 0.5) else "A"
        chan_a = r.permutation(np.arange(1, 97))
        chan_b = r.permutation(np.arange(1, 129))
        ia = ib = 0
        load0 = dt.datetime.combine(start_day, dt.time(7, 30))
        cell_i = 0
        for t in trays:
            load = load0 + dt.timedelta(minutes=int(trays.index(t) * 9 + r.integers(0, 6)))
            for c in sorted([x for x in cells if x.tray_no == t], key=lambda x: x.pos):
                f = tray_fleet[t]
                if f == "A":
                    ch = "A-%d-%02d" % (1 + (chan_a[ia % 96] - 1) // 24, 1 + (chan_a[ia % 96] - 1) % 24)
                    ia += 1
                else:
                    ch = "B%d.%03d" % (1 + (chan_b[ib % 128] - 1) // 32, 1 + (chan_b[ib % 128] - 1) % 32)
                    ib += 1
                cell_i += 1
                tests[c.serial] = make_cycles(c, f, ch, load, r, (lot, cell_i) in interrupted)
    return tests


def make_cycles(c, fleet, channel, start_local, r, interrupt):
    n = 100
    dq = math.exp(c.lnq)
    q10 = 4880.0 + r.normal(0.0, 12.0)
    idx = np.arange(1, n + 1)
    x = np.clip((idx - 10) / 90.0, 0.0, None)
    h = np.where(idx >= 10, -x ** 0.88, 0.035 * np.sin(np.pi * (10 - idx) / 18.0))
    q = q10 + dq * h
    q += r.normal(0.0, 1.15, n)
    q[9] = q10
    q[99] = q10 - dq
    r10 = 25.2 + r.normal(0.0, 0.6)
    g = np.where(idx >= 10, x ** 1.1, 0.0) * c.dr + np.where(idx < 10, 0.28 * (10 - idx) / 9.0, 0.0)
    res = r10 + g + r.normal(0.0, 0.07, n)
    res[9] = r10
    res[99] = r10 + c.dr
    ce = 0.99965 + r.normal(0.0, 0.00006, n)
    ce[:3] = [0.9951, 0.9982, 0.9991]
    qc = q / ce
    tmax = 30.6 + r.normal(0.0, 0.35) + r.normal(0.0, 0.18, n) + 0.004 * idx
    dur = CYCLE_H + r.normal(0.0, 0.035, n)
    seg = [(0, n, fleet, channel)]
    gap_h = 0.0
    if interrupt:
        k = int(r.integers(31, 79))
        gap_h = float(r.uniform(38.0, 61.0))
        other = "A" if fleet == "B" else "B"
        ch2 = ("A-%d-%02d" % (int(r.integers(1, 5)), int(r.integers(1, 25)))) if other == "A" else               ("B%d.%03d" % (int(r.integers(1, 5)), int(r.integers(1, 33))))
        seg = [(0, k, fleet, channel), (k, n, other, ch2)]
        # the rest lets the cell recover a little capacity, gone within a few cycles
        rec = 0.0035 * q10 * np.exp(-np.arange(n - k) / 2.4)
        q[k:] += rec
        q[99] = q10 - dq   # the hundredth cycle is past the recovery
    ends = []
    t = start_local
    for i in range(n):
        if interrupt and i == seg[1][0]:
            t = t + dt.timedelta(hours=gap_h)
        t = t + dt.timedelta(hours=float(dur[i]))
        ends.append(t)
    # local wall time to UTC
    ends_utc = []
    for e in ends:
        off = K.cet_offset(e - dt.timedelta(hours=1))
        ends_utc.append(e - dt.timedelta(hours=off))
    return SimpleNamespace(serial=c.serial, lot=c.lot, segments=seg, q=q, qc=qc, res=res, tmax=tmax,
                           ends_utc=ends_utc, start_local=start_local, interrupted=interrupt)


def life_results(W):
    """The finished lots' life tests: each qualification cell's cycles to 80 per cent of rated capacity on QP-3, or the
    cycle at which a channel fault or a thermal alarm stopped the test first."""
    out = {}
    r = K.rng("life-results")
    rs = K.rng("life-stops")
    for c in W.qcells:
        if c.lot not in K.TRAIN_LOTS:
            continue
        stop = r.random() < 0.0105
        if stop:
            # a cell near the end of its life runs warm, and the chamber's alarm or a channel fault stops it first
            r.integers(180, max(c.life - 30, 200))      # the stream's draw, kept so later cells' draws stay put
            at = int(c.life * rs.uniform(0.88, 0.97))
            out[c.serial] = SimpleNamespace(status="STOPPED", cycles=at, reason="thermal alarm" if r.random() < 0.7
                                            else "channel fault", cap=None)
        else:
            out[c.serial] = SimpleNamespace(status="EOL", cycles=c.life, reason="", cap=None)
    return out


def model_j(W):
    """The lot's B trays went to Model J, the two-cell pack of the J12 convertible: two cells at a time in tray order."""
    r = K.rng("model-j")
    packs = []
    rack = []
    for t in W.new.trays:
        if t.grade != "B":
            continue
        good = [s for s in W.new.tray_cells[t.no] if not W.new.cells[s].reject]
        while len(good) >= 2:
            packs.append(good[:2])
            good = good[2:]
        rack.extend(good)
        while len(rack) >= 2:
            packs.append(rack[:2])
            rack = rack[2:]
    W.new.j_packs = packs
    return packs


# ---------------------------------------------------------------------------------------------------- the lot under release
def new_lot(W):
    """ZC2638 cell by cell: 4,320 formation trays of six, the incoming inspection's rejects, A and B trays, the twenty
    release-test trays, and the Model K packs the line built three cells at a time in tray order, the part-tray rack
    completing packs from leftover cells."""
    r = K.rng("new-lot")
    n_trays = 4320
    lot = K.NEW_LOT
    mq, mr = W.lot_levels[lot]
    trays = []
    tray_cells = {}
    seq = 3_110_000
    form0 = dt.datetime.combine(K.LOT_START[lot], dt.time(6, 0))
    for tno in range(1, n_trays + 1):
        cap_tray = r.normal(0.0, 9.0)
        cl = []
        for j in range(K.TRAY_CELLS):
            seq += 1
            cl.append(seq)
        tray_cells[tno] = cl
        trays.append(SimpleNamespace(no=tno, key=tray_key(lot, tno), cap_off=cap_tray,
                                     formed=form0 + dt.timedelta(minutes=int(tno * 2.2 + r.integers(0, 3)))))
    cells = {}
    for t in trays:
        for j, s in enumerate(tray_cells[t.no]):
            cap = 4868.0 + t.cap_off + r.normal(0.0, 11.0)
            ocv = r.normal(3.8920, 0.0016)
            acir = r.normal(24.6, 0.55)
            kval = abs(r.normal(0.034, 0.008))
            reject = bool(r.random() < 0.0105)
            if reject:   # out of the incoming limits on one measure
                which = r.integers(0, 3)
                if which == 0:
                    ocv -= r.uniform(0.012, 0.03)
                elif which == 1:
                    acir += r.uniform(3.0, 6.0)
                else:
                    kval += r.uniform(0.09, 0.2)
            cells[s] = SimpleNamespace(seq=s, serial=cell_serial(lot, s), tray_no=t.no, tray=t.key, pos=j + 1, cap=cap,
                                       ocv=ocv, acir=acir, kval=kval, reject=reject)
    for t in trays:
        good = [s for s in tray_cells[t.no] if not cells[s].reject]
        t.mean_cap = float(np.mean([cells[s].cap for s in good])) if good else 0.0
        t.grade = "A" if t.mean_cap >= 4855.0 and len(good) >= 3 else "B"
    a_trays = [t.no for t in trays if t.grade == "A"]
    test = sorted(r.choice(np.array(a_trays), K.TEST_TRAYS, replace=False).tolist())
    # packs: A trays in formation order, test trays out
    packs = []
    rack = []
    build_t = dt.datetime(2026, 9, 28, 6, 10)
    for tno in a_trays:
        if tno in test:
            continue
        good = [s for s in tray_cells[tno] if not cells[s].reject]
        while len(good) >= 3 and len(packs) < K.MODEL_K_PACKS:
            packs.append(good[:3])
            good = good[3:]
        rack.extend(good)
        while len(rack) >= 3 and len(packs) < K.MODEL_K_PACKS:
            packs.append(rack[:3])
            rack = rack[3:]
        if len(packs) >= K.MODEL_K_PACKS:
            break
    assert len(packs) == K.MODEL_K_PACKS
    W.new = SimpleNamespace(trays=trays, tray_cells=tray_cells, cells=cells, a_trays=a_trays, test_trays=test,
                            packs=packs, rack_left=rack)
    return W.new


def simulate():
    W = SimpleNamespace()
    W.lot_levels = lot_levels()
    new_lot(W)
    W.qcells = qualification_cells(W)
    W.tests = qual_tests(W)
    W.life = life_results(W)
    model_j(W)
    return W


if __name__ == "__main__":
    W = simulate()
    from collections import Counter
    comp = Counter(len({W.new.cells[s].tray_no for s in p}) for p in W.new.packs)
    print("packs", len(W.new.packs), "composition (trays per pack)", dict(comp))
    print("A trays", len(W.new.a_trays), "of", len(W.new.trays))
    print("qcells", len(W.qcells))
