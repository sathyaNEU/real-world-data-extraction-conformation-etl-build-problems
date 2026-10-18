"""Settles the reply draw so that every graded figure sits inside its hundred under every reading of the golden's
method that a careful reader could take (each lot's own handout days, the lots post-stratified to their own entries),
at least 10 trips or passengers from either edge, and so that the coded party lands outside the golden's hundred.

Each step returns one card that could have come back (its car left by the last box collection) or holds back one that
did; nothing else in the population, the handout or the register moves. The steps are chosen greedily and
deterministically from the sim's own draw.
"""
from collections import defaultdict

import numpy as np

import world as W

VARIANTS = ("golden", "per_lot", "post", "post_lot")
EDGE_G = 15.0      # the golden's own distance to its bin edge
EDGE_V = 10.0      # every variant's distance to the edge
EDGE_C = 10.0      # the coded party's distance outside the golden's bin


class Frame:
    """Every card that could have come back, as arrays, with the weights each reading gives it."""

    def __init__(self, x, seed):
        import sim
        cards = x["cards"] + x["held"]
        self.cards = cards
        self.resp = np.array([True] * len(x["cards"]) + [False] * len(x["held"]))
        waves = [w for w, _, _ in W.WAVES]
        self.wave = np.array([waves.index(c["wave"]) for c in cards])
        self.lot = np.array([W.LOTS.index(c["lot"]) for c in cards])
        self.L = np.array([c["nights"] for c in cards])
        groups = list(W.MARKETS)
        self.grp = np.array([groups.index(c["group"]) if c["group"] in W.MARKETS else -1 for c in cards])
        self.cand = [groups.index(m) for m in W.CANDIDATES]
        self.party = np.array([c["party"] for c in cards], dtype=float)
        self.keyed = np.array([c["party_keyed"] for c in cards], dtype=float)
        sa = self.grp >= 0
        # the Layer 1 items on the cards, mishandled: a ZIP keyed with its plus-four or a space matched as written
        # (the card is lost to the service area), and the ZIP on two counties' lists joined row for row (counted twice)
        self.zip_lost = sa & np.array([c["zip_keyed"] != c["zip"] for c in cards])
        self.fanout = sa & np.array([c["zip"] == "47058" for c in cards])
        self.serial = np.array([c["serial"] for c in cards])
        E = defaultdict(int)
        EL = defaultdict(int)
        for d, l, n in x["entries"]:
            q = (d.month - 1) // 3 + 1
            E[q] += n
            EL[(q, l)] += n
        self.E = np.array([E[q] for _, q, _ in W.WAVES], dtype=float)
        self.EL = np.array([[EL[(q, l)] for l in W.LOTS] for _, q, _ in W.WAVES], dtype=float)
        self.Wpool, self.Wlot, self.Wdays = weights(x["handout"])
        self.w = {
            "golden": self.Wpool[self.wave, self.L],
            "per_lot": self.Wlot[self.wave, self.lot, self.L],
            "post": self.Wpool[self.wave, self.L],
            "post_lot": self.Wlot[self.wave, self.lot, self.L],
            "days": self.Wdays[self.wave, self.L],
            "raw": np.ones(len(cards)),
        }

    def figures(self, how, unit=None, resp=None, num=None, dup=None):
        """num: a multiplier on each card's place in its market's count only; dup: extra copies of cards (both)."""
        r = self.resp if resp is None else resp
        w = self.w[how]
        if dup is not None:
            w = w * (1.0 + dup)
        post = how.startswith("post")
        cell = self.wave * 3 + self.lot if post else self.wave
        ncell = 12 if post else 4
        S = np.bincount(cell[r], weights=w[r], minlength=ncell)
        base = self.EL.reshape(-1) if post else self.E
        contrib = base[cell] * w / np.where(S[cell] > 0, S[cell], 1.0)
        if unit is not None:
            contrib = contrib * unit
        if num is not None:
            contrib = contrib * num
        m = r & (self.grp >= 0)
        out = np.bincount(self.grp[m], weights=contrib[m], minlength=len(W.MARKETS))
        return out


def weights(handout):
    """Collection-window weights: the inverse of the share of the wave's handed cards (pooled over the lots, or the
    lot's own) whose handout day left room for a stay of L nights to end by the last box collection; and the same with
    every handout day counted equally."""
    waves = [w for w, _, _ in W.WAVES]
    Wpool = np.zeros((4, W.MAX_STAY + 1))
    Wlot = np.zeros((4, 3, W.MAX_STAY + 1))
    Wdays = np.zeros((4, W.MAX_STAY + 1))
    for wi, wname in enumerate(waves):
        days = sorted({r[1] for r in handout if r[0] == wname})
        h = defaultdict(int)
        hl = defaultdict(int)
        for w, d, l, a, b, n in handout:
            if w == wname:
                h[d] += n
                hl[(d, l)] += n
        for L in range(W.MAX_STAY + 1):
            ok = [d for i, d in enumerate(days) if i + 1 + L <= W.LAST_COLLECT]
            Wpool[wi, L] = sum(h[d] for d in days) / sum(h[d] for d in ok)
            Wdays[wi, L] = len(days) / len(ok)
            for li, lot in enumerate(W.LOTS):
                Wlot[wi, li, L] = sum(hl[(d, lot)] for d in days) / sum(hl[(d, lot)] for d in ok)
    return Wpool, Wlot, Wdays


LAYER1 = ("zip_as_keyed", "zip_fanout")


def state(F, resp=None):
    """Every graded figure under every reading, the trips with each Layer 1 item mishandled, the coded party's
    passengers."""
    out = {}
    for how in VARIANTS:
        out[("trips", how)] = F.figures(how, resp=resp)
        out[("pax", how)] = F.figures(how, F.party, resp=resp)
    out[("trips", "zip_as_keyed")] = F.figures("golden", resp=resp, num=1.0 - F.zip_lost)
    out[("trips", "zip_fanout")] = F.figures("golden", resp=resp, dup=F.fanout.astype(float))
    out["cracker"] = F.figures("golden", F.keyed, resp=resp)
    return out


def edge(v):
    return 50.0 - abs(v - round(v / 100.0) * 100.0)


def same_bin(a, b):
    return round(a / 100.0) == round(b / 100.0)


def windows(S, F):
    """For each figure, the interval its golden value must sit in (given each reading's present offset from it)."""
    win = {}
    for unit in ("trips", "pax"):
        g = S[(unit, "golden")]
        for k in F.cand:
            offs = [S[(unit, v)][k] - g[k] for v in VARIANTS + (LAYER1 if unit == "trips" else ())]
            b = round(g[k] / 100.0) * 100.0
            best = None
            for bb in (b, b - 100.0, b + 100.0):
                lo = bb - 50.0 + max(EDGE_G, EDGE_V - min(offs))
                hi = bb + 50.0 - max(EDGE_G, EDGE_V + max(offs))
                if unit == "pax":
                    loss = g[k] - S["cracker"][k]          # the coded party's shortfall, positive
                    hi = min(hi, bb - 50.0 + loss - EDGE_C)
                if lo <= hi:
                    d = 0.0 if lo <= g[k] <= hi else min(abs(g[k] - lo), abs(g[k] - hi))
                    if best is None or d < best[0]:
                        best = (d, lo, hi)
            win[(unit, k)] = best
    return win


def gap_ok(S, F):
    g = S[("trips", "golden")]
    order = sorted(F.cand, key=lambda k: -g[k])
    a, b = order[2], order[3]
    vals = [S[("trips", v)][a] - S[("trips", v)][b] for v in VARIANTS + LAYER1]
    return edge(vals[0]) >= EDGE_G and all(edge(v) >= EDGE_V and same_bin(v, vals[0]) for v in vals), (a, b)


def violations(S, F):
    win = windows(S, F)
    bad = []
    for (unit, k), wv in win.items():
        g = S[(unit, "golden")][k]
        if wv is None:
            bad.append((unit, k, None, None))
        elif not (wv[1] <= g <= wv[2]):
            bad.append((unit, k, wv[1], wv[2]))
    ok, pair = gap_ok(S, F)
    return bad, ok, pair, win


def settle(x, seed, max_steps=400, quiet=True):
    """Return or hold back single cards until every figure sits in its window; moves cards between x['cards'] and
    x['held']."""
    F = Frame(x, seed)
    resp = F.resp.copy()
    order = np.lexsort((F.serial, F.wave))            # deterministic tie-break
    rank = np.empty(len(order), dtype=int)
    rank[order] = np.arange(len(order))
    used = np.zeros(len(resp), dtype=bool)
    steps = []
    for step in range(max_steps):
        S = state(F, resp)
        bad, gap_good, pair, win = violations(S, F)
        if not bad and gap_good:
            break
        if bad:
            unit, k, lo, hi = bad[0]
            if lo is None:
                raise SystemExit("calibrate: no window for %s %s" % (unit, W.CANDIDATES[F.cand.index(k)]))
            g_t = S[("trips", "golden")][k]
            g_p = S[("pax", "golden")][k]
            wt, wp = win[("trips", k)], win[("pax", k)]
            tgt_t = (wt[1] + wt[2]) / 2.0
            tgt_p = (wp[1] + wp[2]) / 2.0
            need_t, need_p = tgt_t - g_t, tgt_p - g_p
            market = k
        else:
            # the gap: move the third market's trips within its own window towards its middle
            a, b = pair
            wt = win[("trips", a)]
            market = a
            g_t = S[("trips", "golden")][a]
            need_t = ((wt[1] + wt[2]) / 2.0 - g_t) or 20.0
            need_p = 0.0
            wp = win[("pax", a)]
        # each card's effect on its market's trips and passengers if returned (or held back)
        S_w = np.bincount(F.wave[resp], weights=F.w["golden"][resp], minlength=4)
        dt_ = F.E[F.wave] * F.w["golden"] / S_w[F.wave]
        sign = np.where(resp, -1.0, 1.0)
        cand = (F.grp == market) & ~used
        d_t = sign * dt_
        d_p = sign * dt_ * F.party
        ht = max((wt[2] - wt[1]) / 2.0, 5.0)
        hp = max((wp[2] - wp[1]) / 2.0, 5.0)
        cost = ((need_t - d_t) / ht) ** 2 + ((need_p - d_p) / hp) ** 2
        cost = np.where(cand, cost, np.inf)
        j = int(np.lexsort((rank, cost))[0])
        resp[j] = ~resp[j]
        used[j] = True
        steps.append(j)
        if not quiet:
            print(step, W.CANDIDATES[F.cand.index(market)] if market in F.cand else market, "%+.0f %+.0f" % (
                need_t, need_p), "flip", F.cards[j]["wave"], F.cards[j]["serial"], "now", bool(resp[j]))
    else:
        raise SystemExit("calibrate: not settled in %d steps" % max_steps)
    S = state(F, resp)
    for v in VARIANTS:
        g = S[("trips", v)]
        order = sorted(F.cand, key=lambda k: -g[k])
        if g[order[3]] / g[order[4]] < 1.05:
            raise SystemExit("calibrate: the fourth and fifth markets within 5 per cent under %s" % v)
    keep = [F.cards[i] for i in range(len(resp)) if resp[i]]
    held = [F.cards[i] for i in range(len(resp)) if not resp[i]]
    x["cards"], x["held"] = keep, held
    x["settled"] = len(steps)
    return len(steps)


def dup_batch(x, keyed):
    """The keying batch the contractor's export carried twice: of the third wave's batches of 40 to 150 cards, the one
    whose second copy leaves every candidate's trips in its hundred by the widest margin (the export error is real;
    which night's batch it hit is the world's draw)."""
    F = Frame(x, W.SEED)
    g = F.figures("golden")
    index = {(c["wave"], c["serial"]): i for i, c in enumerate(F.cards)}
    batches = {}
    for c, b, z in keyed:
        if c["wave"] == "W3":
            batches.setdefault(b, []).append(index[(c["wave"], c["serial"])])
    best = None
    for b in sorted(batches):
        idx = batches[b]
        if not 40 <= len(idx) <= 150:
            continue
        dup = np.zeros(len(F.cards))
        dup[idx] = 1.0
        v = F.figures("golden", dup=dup)
        margin = min(50.0 - abs(v[k] - round(g[k] / 100.0) * 100.0) for k in F.cand)
        if best is None or margin > best[0]:
            best = (margin, b)
    if best is None or best[0] < 5.0:
        raise SystemExit("calibrate: no neutral batch to repeat")
    return best[1]
