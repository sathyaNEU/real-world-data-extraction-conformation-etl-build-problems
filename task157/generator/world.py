"""task157 (architecture 2) clean truth.

Builds the petition as the office's own systems would have produced it: 36,000 receipted sheets of fifteen
lines, the signers behind them, the statutory five per cent random sample of the signature lines and the
disposition each sampled line was given. Nothing here is shipped; `records.py` and `docs.py` cut the pack
from it and `checks.py` executes the three rules on it.

The parameters below are the stage 3 pin (the design note's `## Bin measurements`). They are set so that,
at every one of the six sweep seeds, the projection the sample supports sits inside the statute's 95 to 105
per cent band with both clearances at or above 2.5 bins of 5,000, and so that at the world seed it prints
within 1,500 of its cell's centre. They are not tuned on anything the pack does not carry."""
from __future__ import annotations

import datetime as dt
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402

# ------------------------------------------------------------------------------------------------- parameters
PARAMS = dict(
    # signers who signed the petition more than once. The multiplicity is drawn near binary on purpose: the
    # all-doubles expansion overstates the burden by (1 - p) per registered triple signer, and a world with a
    # five per cent triple share among multi-signers carries a bias of 0.59 bins that the sample cannot
    # identify. See checks.py R-bias and the design note's `## Bin measurements`.
    doubles=34_000,
    triples=150,
    # line grounds, drawn per signature line
    rate_il=0.01150, rate_md=0.00650, rate_ws=0.00150,
    # registration grounds, drawn per signer and applied to every line the signer signed
    rate_nr=0.08600, rate_ad=0.05600, rate_sg=0.04200, rate_nc=0.01530, rate_nq=0.00400,
    rate_ca_pre=0.00740,    # cancelled before the December 2027 snapshot: both snapshots agree
    rate_ca_mid=0.01810,    # cancelled in the 14 March 2028 list-maintenance run, signed afterwards
    # the recorder flags a duplicate it meets in its own queue; the division's consolidation check of the
    # whole returned sample is the backstop and strikes the rest
    county_found=0.620,
    # registrations cancelled after the signature was given, so valid at signing and cancelled in the July
    # snapshot, and registrations cancelled and then restored before signing (status active, cancel date set)
    rate_post_cancel=0.02500, rate_reinstated=0.00210,
    # electors who registered between the December 2027 snapshot and the day they signed
    rate_new_registration=0.00180,
    # sampled lines the recorder returned without a determination (the transmitted copy was unreadable) and
    # which the division determined itself
    division_illegible=160,
    # the division's query notices: lines a recorder re-determined after the consolidation check, every one
    # of them a move between two single-signature grounds, so no reading of them moves the call
    corrections=380,
    # registrations the 14 March run cancelled that belong to nobody on this petition
    maintenance_other=17_800,
    # paid circulators who left one firm for another inside the circulation window and registered again.
    # A signature belongs to the firm that had its circulator registered on the day it was given, which is
    # not the firm whose bundle the sheet was delivered in.
    circulator_moves=22,
    # registrations cancelled after the signature was given and restored before the July snapshot, so the
    # snapshot shows an active registration carrying a cancellation date later than the signature
    rate_late_restored=0.00150,
)

CODE_IX = {c: i for i, c in enumerate(K.CODE_KEYS)}


class World:
    pass


def _sheet_layer(w, p, seed):
    """36,000 receipted sheets: firm, circulator, the firm's own sheet number, the office's receipt bundle
    and serial, and the days the sheet was circulated over."""
    r = K.rng("sheets", seed=seed)
    n = K.SHEETS
    shares = np.array([s for _, _, s, _ in K.FIRMS])
    counts = np.floor(shares * n).astype(np.int64)
    counts[0] += n - counts.sum()
    firm = np.repeat(np.arange(len(K.FIRMS)), counts)

    # each firm has its own circulators and numbers its own sheets as it prints them
    # paid circulators register with the office; the registration number carries no firm marking, so a
    # sampled line's firm is only reachable through the office's sheet index
    want = [int(28 + 62 * shares[fi] / shares.max() * 1.4) for fi in range(len(K.FIRMS))]
    pool = sorted({K.token("circ", j, n=5, alphabet="0123456789", seed=seed) for j in range(sum(want) * 4)})
    pool = ["PC-%s" % t for t in pool if t[0] != "0"][:sum(want)]
    assert len(pool) == sum(want)
    circ_of_firm, circ_id, circ_firm = [], [], []
    at = 0
    for fi, (code, _, _, _) in enumerate(K.FIRMS):
        m = want[fi]
        ids = pool[at:at + m]
        at += m
        circ_of_firm.append(ids)
        for cid in ids:
            circ_id.append(cid)
            circ_firm.append(fi)
    w.circulators = circ_id
    w.circulator_firm = {c: f for c, f in zip(circ_id, circ_firm)}

    sheet_circ = np.empty(n, dtype=object)
    sheet_no = np.zeros(n, dtype=np.int64)
    # a circulator works a stretch of the window; sheets are numbered by the firm in print order
    start = 0
    for fi in range(len(K.FIRMS)):
        ix = np.where(firm == fi)[0]
        ids = circ_of_firm[fi]
        wt = r.gamma(2.6, 1.0, size=len(ids))
        wt = wt / wt.sum()
        pick = r.choice(len(ids), size=len(ix), p=wt)
        sheet_circ[ix] = np.array(ids, dtype=object)[pick]
        start += len(ix)

    # when each sheet was circulated: the campaign accelerates towards the filing deadline
    day = np.clip(r.beta(2.15, 1.55, size=n) * K.WINDOW_DAYS, 0, K.WINDOW_DAYS - 1).astype(np.int64)
    # firms join the drive at different points
    offs = np.array([0, 9, 24, 46])
    day = np.clip(day + offs[firm] - 12, 0, K.WINDOW_DAYS - 1)

    # the office's receipt bundles: the committee delivered in boxes, numbered on receipt
    order = np.lexsort((sheet_no, firm, day))
    bundle = np.zeros(n, dtype=np.int64)
    serial = np.zeros(n, dtype=np.int64)
    sizes = r.integers(42, 56, size=n // 40 + 8)
    ends = np.cumsum(sizes)
    rank = np.arange(n)
    bundle[order] = np.searchsorted(ends, rank, side="right") + 1
    serial[order] = rank + 1

    # Sheets are issued to a circulator in a numbered pad, so the number printed on a sheet is that
    # circulator's own series and a sheet is identified by the registration number with that number.
    seq = {}
    for j in np.lexsort((np.arange(n), day)).tolist():
        c = sheet_circ[j]
        seq[c] = seq.get(c, 0) + 1
        sheet_no[j] = seq[c]

    # the signature lines each sheet carries. A sheet has fifteen lines; the firms filed the sheets they had,
    # so most are full and a tail are not, and the office's count of the lines filed is the statutory total.
    shape = np.array([15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4])
    wts = np.array([0.280, 0.170, 0.130, 0.100, 0.080, 0.060, 0.050, 0.040, 0.030, 0.025, 0.020, 0.015])
    wts = wts / wts.sum()
    used = r.choice(shape, size=n, p=wts)
    short = K.LINES_FILED - int(used.sum())
    step = 1 if short > 0 else -1
    while short != 0:
        cand = np.where(used < 15)[0] if step > 0 else np.where(used > 4)[0]
        take = r.choice(cand, size=min(abs(short), len(cand)), replace=False)
        used[take] += step
        short = K.LINES_FILED - int(used.sum())
    w.sheet_lines = used.astype(np.int64)

    # the county a sheet was circulated in, which is the county most of its signers claim
    cshare = np.array([s for _, _, s in K.COUNTIES])
    cshare = cshare / cshare.sum()
    sheet_county = r.choice(len(K.COUNTIES), size=n, p=cshare)

    w.sheet_firm = firm
    w.sheet_circ = sheet_circ
    w.sheet_no = sheet_no
    w.sheet_day = day
    w.sheet_bundle = bundle
    w.sheet_serial = serial
    w.sheet_county = sheet_county
    w.n_bundles = int(bundle.max())

    # the circulators who moved firm inside the window: each keeps one registration number and registers
    # again under the firm it joined
    rm = K.rng("moves", seed=seed)
    # the circulators who move are the busiest, which is what the trade looks like: a firm poaches the
    # gatherers who bring in the sheets, so the move touches every firm and every month of the drive
    load = {}
    for j in range(n):
        load[sheet_circ[j]] = load.get(sheet_circ[j], 0) + 1
    cand = sorted(circ_id, key=lambda c: (-load.get(c, 0), c))[:int(p["circulator_moves"] * 2.6)]
    pick = rm.permutation(len(cand))[:p["circulator_moves"]]
    moves = {}
    for j in pick.tolist():
        cid = cand[j]
        was = w.circulator_firm[cid]
        now = int(rm.choice([f for f in range(len(K.FIRMS)) if f != was]))
        day = int(rm.integers(38, K.WINDOW_DAYS - 24))
        moves[cid] = (was, now, day)
    w.circulator_moves = moves


def _line_layer(w, p, seed):
    """540,000 signature lines: the sheet and line they sit on, the day they were signed, the line defect the
    recorder would find, and the signer behind them."""
    r = K.rng("lines", seed=seed)
    n = K.LINES_FILED
    lu = w.sheet_lines
    w.line_sheet = np.repeat(np.arange(K.SHEETS), lu)
    starts = np.concatenate([[0], np.cumsum(lu)[:-1]])
    w.line_no = (np.arange(n) - np.repeat(starts, lu) + 1).astype(np.int64)
    spread = r.integers(0, 5, size=n)
    w.line_day = np.clip(w.sheet_day[w.line_sheet] + spread, 0, K.WINDOW_DAYS - 1)

    u = r.random(n)
    g = np.zeros(n, dtype=np.int8)
    a, b, c = p["rate_il"], p["rate_md"], p["rate_ws"]
    g[u < a] = CODE_IX["IL"]
    g[(u >= a) & (u < a + b)] = CODE_IX["MD"]
    g[(u >= a + b) & (u < a + b + c)] = CODE_IX["WS"]
    w.line_ground = g

    # signers. A signer who signed twice or three times did so on different sheets, at different events.
    rs = K.rng("signers", seed=seed)
    d, t = p["doubles"], p["triples"]
    need = 2 * d + 3 * t
    pool = rs.permutation(n)[:need + 4000]
    # pairs first, then triples, then the spare tail that replaces a member sharing a sheet with its own group
    pairs = pool[:2 * d].reshape(d, 2)
    trips = pool[2 * d:2 * d + 3 * t].reshape(t, 3)
    spare = list(pool[2 * d + 3 * t:][::-1])
    sh = w.line_sheet

    def fix(block):
        for row in range(block.shape[0]):
            seen = set()
            for col in range(block.shape[1]):
                while int(sh[block[row, col]]) in seen:
                    block[row, col] = spare.pop()
                seen.add(int(sh[block[row, col]]))
        return block

    bad_p = np.where(sh[pairs[:, 0]] == sh[pairs[:, 1]])[0]
    if len(bad_p):
        pairs[bad_p] = fix(pairs[bad_p])
    bad_t = np.where((sh[trips[:, 0]] == sh[trips[:, 1]]) | (sh[trips[:, 0]] == sh[trips[:, 2]])
                     | (sh[trips[:, 1]] == sh[trips[:, 2]]))[0]
    if len(bad_t):
        trips[bad_t] = fix(trips[bad_t])

    signer = np.full(n, -1, dtype=np.int64)
    signer[pairs.ravel()] = np.repeat(np.arange(d), 2)
    signer[trips.ravel()] = np.repeat(np.arange(d, d + t), 3)
    rest = np.where(signer < 0)[0]
    signer[rest] = np.arange(d + t, d + t + len(rest))
    w.line_signer = signer
    w.n_signers = int(signer.max()) + 1
    w.multi_pairs = pairs
    w.multi_trips = trips
    w.multi_k = np.concatenate([np.full(d, 2, dtype=np.int8), np.full(t, 3, dtype=np.int8)])


def _signer_layer(w, p, seed):
    """Every signer's registration as the county recorder would find it: the ground that strikes the signer's
    lines if any, the county the registration sits in, the registration identifier, and the cancellation and
    restoration dates the two snapshots carry."""
    r = K.rng("signers_attr", seed=seed)
    ns = w.n_signers

    # the county each signer claims: the county their first sheet was circulated in, with a real spill
    order = np.lexsort((w.line_no, w.line_sheet, w.line_day))
    srt = w.line_signer[order]
    _, idx = np.unique(srt, return_index=True)
    first = order[idx]
    county = w.sheet_county[w.line_sheet[first]].astype(np.int64)
    spill = r.random(ns) < 0.07
    cshare = np.array([s for _, _, s in K.COUNTIES])
    cshare = cshare / cshare.sum()
    county[spill] = r.choice(len(K.COUNTIES), size=int(spill.sum()), p=cshare)
    w.signer_county = county
    w.signer_first_day = w.line_day[first]

    # the registration ground, drawn per signer
    u = r.random(ns)
    ground = np.zeros(ns, dtype=np.int8)
    edges, keys = [], []
    acc = 0.0
    for key, rate in (("NR", p["rate_nr"]), ("CA_PRE", p["rate_ca_pre"]), ("CA_MID", p["rate_ca_mid"]),
                      ("AD", p["rate_ad"]), ("SG", p["rate_sg"]), ("NC", p["rate_nc"]), ("NQ", p["rate_nq"])):
        acc += rate
        edges.append(acc)
        keys.append(key)
    w.single_signer_rate = acc
    lo = 0.0
    ca_mid = np.zeros(ns, dtype=bool)
    for key, hi in zip(keys, edges):
        sel = (u >= lo) & (u < hi)
        if key == "CA_PRE":
            ground[sel] = CODE_IX["CA"]
        elif key == "CA_MID":
            ground[sel] = CODE_IX["CA"]
            ca_mid |= sel
        else:
            ground[sel] = CODE_IX[key]
        lo = hi
    # a signer cancelled in the 14 March run can only be struck on that ground if every line they signed
    # came after the run; the rest were registered when they signed and the recorder counted them
    md = (K.LIST_MAINTENANCE - K.WINDOW_OPEN).days
    late_enough = w.signer_first_day > md
    moved = ca_mid & ~late_enough
    ground[moved] = 0
    ca_mid &= late_enough
    w.signer_ground = ground
    w.signer_ca_mid = ca_mid

    # registration identifiers. Arizona's statewide identifier is a nine digit number; the office's extract
    # carries it as written. NR and NQ signers have no record in the voter file at all.
    has_rec = ~np.isin(ground, [CODE_IX["NR"], CODE_IX["NQ"]])
    vid = np.zeros(ns, dtype=np.int64)
    m = int(has_rec.sum())
    draw = r.integers(102_000_000, 499_000_000, size=int(m * 1.02), dtype=np.int64)
    draw = np.unique(draw)
    r.shuffle(draw)
    assert len(draw) >= m
    vid[has_rec] = draw[:m]
    w.signer_vid = vid
    w.signer_has_record = has_rec

    # registration dates, cancellations and restorations
    regday = -(r.integers(40, 8600, size=ns).astype(np.int64))
    cancel = np.full(ns, 10 ** 6, dtype=np.int64)        # day offset from the window open, 10**6 is none
    cancel_reason = np.zeros(ns, dtype=np.int8)          # 1 list maintenance, 2 moved out, 3 deceased, 4 request
    cancel[w.signer_ca_mid] = md
    cancel_reason[w.signer_ca_mid] = 1
    pre = (ground == CODE_IX["CA"]) & ~w.signer_ca_mid
    cancel[pre] = -(r.integers(30, 900, size=int(pre.sum())).astype(np.int64))
    cancel_reason[pre] = r.choice([2, 3, 4], size=int(pre.sum()), p=[0.56, 0.27, 0.17])
    # a registration the snapshot still shows cancelled was registered before the cancellation, never
    # after it: a record carrying a later registration date against a standing cancellation is a
    # contradiction, and it is what a strict date test and the status column would disagree about
    late_reg = pre & (regday >= cancel)
    regday[late_reg] = cancel[late_reg] - r.integers(60, 5200, size=int(late_reg.sum())).astype(np.int64)

    # cancelled after the signature was given: valid at signing, cancelled in the July snapshot
    clean = (ground == 0) & has_rec
    pc = clean & (r.random(ns) < p["rate_post_cancel"])
    span = (K.LATE_SNAPSHOT - K.WINDOW_OPEN).days
    ix = np.where(pc)[0]
    lo = w.signer_first_day[ix] + 1
    drop = lo >= span
    pc[ix[drop]] = False
    ix, lo = ix[~drop], lo[~drop]
    cancel[ix] = lo + (r.random(len(ix)) * (span - lo)).astype(np.int64)
    cancel_reason[ix] = r.choice([2, 3, 4], size=len(ix), p=[0.52, 0.31, 0.17])
    w.signer_post_cancel = pc

    # cancelled and restored before signing: the July snapshot shows an active registration with a
    # cancellation date on it, which is what a count of non-empty cancellation dates gets wrong
    restore = np.full(ns, 10 ** 6, dtype=np.int64)
    ri = clean & ~pc & (r.random(ns) < p["rate_reinstated"])
    ix = np.where(ri)[0]
    fd = w.signer_first_day[ix]
    drop = fd < 18
    ri[ix[drop]] = False
    ix, fd = ix[~drop], fd[~drop]
    # cancelled and restored inside the circulation window, so the December 2027 snapshot shows neither
    cancel[ix] = 1 + (r.random(len(ix)) * (fd - 9)).astype(np.int64)
    cancel_reason[ix] = 1
    rlo = cancel[ix] + 4
    restore[ix] = rlo + (r.random(len(ix)) * ((fd - 2) - rlo)).astype(np.int64)
    w.signer_restored = ri

    # cancelled after the signature was given and restored before the July snapshot: the snapshot shows an
    # active registration whose cancellation date is later than the signature's own date
    lr = clean & ~pc & ~ri & (r.random(ns) < p["rate_late_restored"])
    ix = np.where(lr)[0]
    fd = w.signer_first_day[ix]
    room = span - 14 - fd
    drop = room < 6
    lr[ix[drop]] = False
    ix, fd, room = ix[~drop], fd[~drop], room[~drop]
    cancel[ix] = fd + 1 + (r.random(len(ix)) * (room - 4)).astype(np.int64)
    cancel_reason[ix] = 1
    rlo = cancel[ix] + 3
    restore[ix] = rlo + (r.random(len(ix)) * (span - 2 - rlo)).astype(np.int64)
    w.signer_late_restored = lr
    # electors who registered after the December 2027 snapshot and signed afterwards: the archived
    # snapshot carries no record for them at all, which is what a seven month old extract looks like
    nr_pool = (ground == 0) & has_rec & (w.signer_first_day > 20)
    newreg = nr_pool & (r.random(ns) < p["rate_new_registration"])
    ix = np.where(newreg)[0]
    fd = w.signer_first_day[ix]
    cut = (K.EARLY_SNAPSHOT - K.WINDOW_OPEN).days
    regday[ix] = (cut + 1) + (r.random(len(ix)) * (fd - cut - 2)).astype(np.int64)
    w.signer_new_registration = newreg

    # the day each registration was last touched, which is what a status log stamps: a registration that
    # has moved address or been re-verified carries a later stamp than the day it was created
    touched = regday.copy()
    moved = r.random(ns) < 0.78
    span2 = (K.LATE_SNAPSHOT - K.WINDOW_OPEN).days
    jx = np.where(moved)[0]
    lo2 = regday[jx] + 30
    room2 = span2 - lo2
    keep2 = room2 > 10
    jx, lo2, room2 = jx[keep2], lo2[keep2], room2[keep2]
    touched[jx] = lo2 + (r.random(len(jx)) * room2).astype(np.int64)
    w.signer_touched = touched

    w.signer_cancel = cancel
    w.signer_cancel_reason = cancel_reason
    w.signer_restore = restore
    w.signer_regday = regday


def _sample_layer(w, p, seed):
    """The statutory five per cent random sample of the signature lines, and the disposition the recorders
    and the division gave each sampled line."""
    r = K.rng("sample", seed=seed)
    draw = r.choice(K.LINES_FILED, size=K.SAMPLE_LINES, replace=False)
    draw.sort()
    w.sample = draw
    w.sample_seq = np.argsort(np.argsort(r.permutation(K.SAMPLE_LINES)))   # the office's draw order

    ground = w.signer_ground[w.line_signer[draw]]
    lg = w.line_ground[draw]
    code = np.where(lg > 0, lg, ground).astype(np.int8)

    # the duplicate class. A sampled line is struck as a duplicate only where the same signer's earlier
    # signature was drawn into the sample as well and is itself countable: the sample is the only part of
    # the petition anybody keyed.
    clean = (lg == 0) & (ground == 0)
    pos = {int(j): i for i, j in enumerate(draw)}
    by_signer = {}
    for i in np.where(clean)[0]:
        s = int(w.line_signer[draw[i]])
        by_signer.setdefault(s, []).append(i)
    dup_ix = []
    for s, ixs in by_signer.items():
        if len(ixs) < 2:
            continue
        ixs.sort(key=lambda i: (int(w.line_day[draw[i]]), int(w.sheet_serial[w.line_sheet[draw[i]]]),
                                int(w.line_no[draw[i]])))
        dup_ix.extend(ixs[1:])
    dup_ix = np.array(sorted(dup_ix), dtype=np.int64)
    code[dup_ix] = CODE_IX["DU"]
    w.sample_code = code
    w.dup_ix = dup_ix

    # who determined each sampled line: its recorder, except the duplicates the recorder did not meet in its
    # own queue and the lines whose transmitted copy was unreadable, which the division determined
    rd = K.rng("determined", seed=seed)
    det_sos = np.zeros(K.SAMPLE_LINES, dtype=bool)
    det_sos[dup_ix] = rd.random(len(dup_ix)) >= p["county_found"]
    il = np.where((code == CODE_IX["IL"]) & ~det_sos)[0]
    pick = rd.choice(il, size=min(p["division_illegible"], len(il)), replace=False)
    det_sos[pick] = True
    w.det_sos = det_sos

    # the full count's own duplicate burden, which nothing in the pack carries
    full = 0
    for block, k in ((w.multi_pairs, 2), (w.multi_trips, 3)):
        if block.shape[0] == 0:
            continue
        sgn = w.line_signer[block[:, 0]]
        okreg = w.signer_ground[sgn] == 0
        m = (w.line_ground[block] == 0).sum(axis=1)
        full += int(np.maximum(0, m - 1)[okreg].sum())
    w.dup_full = full


def _clear_move_days(w):
    """A circulator moves firm on a day it gathered nothing, so no signature sits on the boundary and the
    firm a signature belongs to is never a convention."""
    days = {}
    for j in range(len(w.line_signer)):
        c = w.sheet_circ[w.line_sheet[j]]
        days.setdefault(c, set()).add(int(w.line_day[j]))
    fixed = {}
    for cid, (was, now, day) in w.circulator_moves.items():
        busy = days.get(cid, set())
        d = day
        for step in range(0, 40):
            for cand in (day + step, day - step):
                if cand not in busy and 30 <= cand <= K.WINDOW_DAYS - 10:
                    d = cand
                    break
            else:
                continue
            break
        fixed[cid] = (was, now, d)
    w.circulator_moves = fixed


def simulate(seed=K.SEED, params=None):
    p = dict(PARAMS)
    if params:
        p.update(params)
    w = World()
    w.seed = seed
    w.params = p
    _sheet_layer(w, p, seed)
    _line_layer(w, p, seed)
    _clear_move_days(w)
    _signer_layer(w, p, seed)
    _sample_layer(w, p, seed)
    return w


# ------------------------------------------------------------------------------------------------- the figures
def counts(w):
    """The sampled counts every route starts from."""
    code = w.sample_code
    out = {k: int((code == CODE_IX[k]).sum()) for k in K.CODE_KEYS}
    out["single"] = sum(out[k] for k in K.SINGLE_CODES)
    out["dup"] = out["DU"]
    out["valid_sampled"] = out["V"]
    # the sampled lines a solver re-deriving registration from the December 2027 snapshot would not strike:
    # cancelled in the March run, signed afterwards, so active in that snapshot
    sl = w.signer_ca_mid[w.line_signer[w.sample]] & (code == CODE_IX["CA"])
    out["vintage_slip"] = int(sl.sum())
    out["dup_county"] = int((~w.det_sos[w.dup_ix]).sum())
    out["dup_division"] = int((w.det_sos[w.dup_ix]).sum())
    out["division_determined"] = int(w.det_sos.sum())
    # sampled lines whose signer the July 2028 snapshot shows cancelled, and the subset of those the
    # recorders counted because the cancellation came after the signature
    sg = w.line_signer[w.sample]
    canc = (w.signer_cancel[sg] < 10 ** 6) & (w.signer_restore[sg] == 10 ** 6)
    out["snapshot_cancelled"] = int(canc.sum())
    out["post_cancel_sampled"] = int((w.signer_post_cancel[sg]).sum())
    out["restored_sampled"] = int((w.signer_restored[sg]).sum())
    return out


def project(single, dup_estimate):
    return K.LINES_FILED - single * K.SAMPLE_DIVISOR - dup_estimate


def routes(w):
    """Every route a competent analyst takes on the deciding quantity, computed on the clean truth. The
    reflex row is enumerated from election administration's and sampling's own vocabulary for a sample
    projection rather than from the rungs beneath it."""
    c = counts(w)
    s, d = c["single"], c["dup"]
    F, n = float(K.LINES_FILED), float(K.SAMPLE_LINES)
    f = F / n                      # the sample's own factor, 20
    pp = K.P_LINE * K.P_LINE
    out = []
    out.append(("R0", "every class at the sample's factor, registration re-derived off the December 2027 "
                "snapshot", project(s - c["vintage_slip"], d * f), "rung 0"))
    out.append(("R1", "every class at the sample's factor, the recorders' determinations as filed",
                project(s, d * f), "rung 1"))
    out.append(("R2", "every class at the sample's factor, both lines of a duplicate pair struck",
                project(s, 2 * d * f), "reflex"))
    out.append(("R3", "expanded county by county at each county's own factor and summed",
                project(s, d * f), "reflex"))
    signers = F - w.params["doubles"] - 2 * w.params["triples"]
    out.append(("R4", "duplicates expanded on the signer base rather than the signature base",
                project(s, d * (signers / (n * (signers / F)))), "reflex"))
    out.append(("R5", "duplicates at twice the sampling fraction, either line of the pair drawn",
                project(s, d / (2 * K.P_LINE)), "reflex"))
    f1, f2 = n - 2 * d, d
    chao = (f1 * f1) / (2 * f2) if f2 else float("inf")
    out.append(("R6", "Chao1 unseen pairs off the sample's singletons and doubletons", project(s, chao),
                "rival family"))
    cs = c["dup_county"]
    out.append(("R7", "the pair's inclusion probability on the division's own strikes only, the recorders' "
                "strikes at the sample's factor", project(s, cs * f + (d - cs) / pp), "rung 2"))
    out.append(("R8", "the pair's inclusion probability, registration re-derived off the July 2028 snapshot "
                "so cancellations after the signature strike it", project(s + c["post_cancel_sampled"],
                                                                         d / pp), "reflex"))
    out.append(("R9", "the pair's inclusion probability, the square of the sampling fraction",
                project(s, d / pp), "GOLDEN"))
    return out


def golden(w):
    c = counts(w)
    return project(c["single"], c["dup"] / (K.P_LINE * K.P_LINE))


def default_path(w):
    c = counts(w)
    return project(c["single"] - c["vintage_slip"], c["dup"] * (float(K.LINES_FILED) / K.SAMPLE_LINES))


def families(w):
    """Convergence. The golden's own family first, then the families a competent solver builds instead."""
    c = counts(w)
    s, d = c["single"], c["dup"]
    F, n = float(K.LINES_FILED), float(K.SAMPLE_LINES)
    pp = K.P_LINE * K.P_LINE
    own = [("the square of the sampling fraction", project(s, d / pp))]
    hyper = K.P_LINE * ((n - 1) / (F - 1))
    own.append(("the hypergeometric pair inclusion, p times (n-1)/(N-1)", project(s, d / hyper)))
    for name, groups in (("the same estimator per county and summed", len(K.COUNTIES)),
                         ("the same estimator per circulator firm and summed", len(K.FIRMS))):
        parts, rem = [], d
        for i in range(groups):
            take = rem // (groups - i)
            parts.append(take)
            rem -= take
        own.append((name, project(s, sum(x / pp for x in parts))))
    own.append(("two steps: the partner seen at the fraction, then expanded at the sample's factor",
                project(s, (d / K.P_LINE) * (F / n))))
    rival = [("Chao1 unseen pairs off the sample's singletons and doubletons",
              project(s, ((n - 2 * d) ** 2) / (2 * d)))]
    r = K.rng("bootstrap", seed=w.seed)
    draws = r.binomial(int(n), d / n, size=200) / pp
    rival.append(("a bootstrap over the sampled lines, 200 draws, mean",
                  project(s, float(draws.mean()))))
    rival.append(("the linear expansion of every disposition class", project(s, d * (F / n))))
    return own, rival


def bin_metrics(w):
    """(a) the decisive step's worth, (b) the defensible family spread, (c) the golden estimator's own 95 per
    cent sampling interval, each in signatures and in units of the graded figure's bin."""
    c = counts(w)
    s, d = c["single"], c["dup"]
    F, n = float(K.LINES_FILED), float(K.SAMPLE_LINES)
    pp = K.P_LINE * K.P_LINE
    gold = project(s, d / pp)
    r0 = default_path(w)
    r1 = project(s, d * (F / n))
    cs = c["dup_county"]
    r2 = project(s, cs * (F / n) + (d - cs) / pp)
    own, _ = families(w)
    spread = max(v for _, v in own) - min(v for _, v in own)
    sd_dup = math.sqrt(d) / pp
    sd_single = math.sqrt(w.single_rate_line * (1 - w.single_rate_line) / n) * F
    cc = 1.96 * math.sqrt(sd_dup ** 2 + sd_single ** 2)
    # the bias the all-doubles expansion carries because a registered triple signer's pair is seen with
    # probability 3p^2 - p^3 rather than p^2
    regt = int((w.signer_ground[w.line_signer[w.multi_trips[:, 0]]] == 0).sum()) if w.multi_trips.shape[0] else 0
    bias = regt * (1 - K.P_LINE)
    return {
        "seed": w.seed, "golden": gold, "rung0": r0, "rung1": r1, "rung2": r2,
        "a_full": r1 - gold, "a_last": r2 - gold, "b": spread, "c": cc,
        "gap01": r0 - r1, "gap12": r1 - r2, "gap23": r2 - gold,
        "clear_hi": K.BAND_HI - gold, "clear_lo": gold - K.BAND_LO,
        "centre": K.cell_centre_distance(gold), "edge": K.bin_edge(gold),
        "edge_r0": K.bin_edge(r0), "edge_r1": K.bin_edge(r1), "edge_r2": K.bin_edge(r2),
        "triple_bias": bias, "dup": d, "single": s, "dup_full": w.dup_full,
        "band_golden": K.band(gold), "band_default": K.band(r0), "band_rung1": K.band(r1),
    }


def attach_rates(w):
    """The realised single-ground rate per sampled line, which (c) is read off."""
    c = counts(w)
    w.single_rate_line = c["single"] / float(K.SAMPLE_LINES)
    return w


def build(seed=K.SEED, params=None):
    return attach_rates(simulate(seed, params))
