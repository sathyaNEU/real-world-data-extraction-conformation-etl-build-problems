"""Generator-side common-point screens on the token-level event table, and the tuning passes that hold
the designed structure (the car-wash and PIN-pad twin, nothing else elevated) before anything is written.

golden.py recomputes every screen from the shipped files on its own code path; this module only steers
the generator.
"""
import numpy as np
import pandas as pd

import sim as S

DAY = S.DAY
CONTACT = (S.E05, S.E80, S.E90)
CARD_PRESENT = (S.E05, S.E07, S.E80, S.E90, S.E91)


def tid_ids(cat, term, day):
    """Integer id of the terminal ID live at each (terminal position, day); -1 for card-not-present."""
    out = np.full(len(term), -1, np.int64)
    has = term >= 0
    out[has] = term[has] * 10
    for t in cat.terminals:
        h = t["tid_history"]
        if len(h) < 2:
            continue
        sel = term == t["idx"]
        for k, (frm, _) in enumerate(h[1:], start=1):
            out[sel & (day >= S.day_of(frm))] = t["idx"] * 10 + k
    return out


def tid_string(cat, tid_id):
    t = cat.terminals[int(tid_id) // 10]
    return t["tid_history"][int(tid_id) % 10][1]


class Engine:
    def __init__(self, cat, ev):
        self.cat = cat
        self.refresh(ev)

    def refresh(self, ev):
        self.ev = ev
        self.tok = ev.tok.values
        self.day = (ev.t.values // DAY)
        self.tid = tid_ids(self.cat, ev.term.values, self.day)
        self.contact = np.isin(ev.entry.values, CONTACT)
        self.cp = np.isin(ev.entry.values, CARD_PRESENT)

    def screen(self, victims, L=60, base="span", modes="contact"):
        """victims: dict token -> first-use day. Returns DataFrame indexed by tid id: v, b, n_v, n_act, lift."""
        vt = np.array(sorted(victims))
        fd = np.array([victims[v] for v in vt])
        span0, span1 = fd.min() - L, fd.max() - 1
        mode = self.contact if modes == "contact" else self.cp
        isv = np.isin(self.tok, vt)
        fmap = dict(zip(vt, fd))
        sel = isv & mode & (self.tid >= 0)
        idx = np.nonzero(sel)[0]
        f_of = np.array([fmap[x] for x in self.tok[idx]])
        d = self.day[idx]
        inlb = (d >= f_of - L) & (d <= f_of - 1)
        a = pd.DataFrame({"tid": self.tid[idx[inlb]], "tok": self.tok[idx[inlb]]}).drop_duplicates()
        v = a.groupby("tid").tok.size()
        if base == "span":
            ins = (self.day >= span0) & (self.day <= span1)
        else:
            ins = np.ones(len(self.day), bool)
        nv = ~isv
        n_act = len(np.unique(self.tok[ins & nv]))
        bsel = ins & nv & mode & (self.tid >= 0)
        b = pd.DataFrame({"tid": self.tid[bsel], "tok": self.tok[bsel]}).drop_duplicates().groupby("tid").tok.size()
        out = pd.DataFrame({"v": v}).join(pd.DataFrame({"b": b}), how="left").fillna({"b": 0})
        out["share_v"] = out.v / len(vt)
        out["base"] = out.b / n_act
        out["lift"] = np.where(out.b > 0, out.share_v / out.base.replace(0, np.nan), np.inf)
        out.attrs["n_v"], out.attrs["n_act"] = len(vt), n_act
        return out.sort_values("lift", ascending=False)

    def victims_read_at(self, victims, tid, L=60, modes="contact"):
        vt = np.array(sorted(victims))
        mode = self.contact if modes == "contact" else self.cp
        sel = np.isin(self.tok, vt) & mode & (self.tid == tid)
        idx = np.nonzero(sel)[0]
        out = set()
        for i in idx:
            f = victims[self.tok[i]]
            if f - L <= self.day[i] <= f - 1:
                out.add(int(self.tok[i]))
        return out


def sequential(eng, victims, L=60, base="span", modes="contact", floor=10, stop=3.0, max_steps=6):
    """Attribute victims to the strongest terminal, screen the rest, repeat while a terminal that read at
    least `floor` of the remaining victims stands above `stop`."""
    rem = dict(victims)
    chosen = []
    for _ in range(max_steps):
        if len(rem) < floor:
            break
        sc = eng.screen(rem, L, base, modes)
        cand = sc[sc.v >= floor]
        if not len(cand) or cand.lift.iloc[0] <= stop:
            break
        top = int(cand.index[0])
        chosen.append(top)
        hit = eng.victims_read_at(rem, top, L, modes)
        rem = {k: v for k, v in rem.items() if k not in hit}
    return chosen, rem


# tuning -----------------------------------------------------------------------------------------
def _soften(eng, rng, victims_hit, tid, L, victims, ev_rows_drop, ev_rows_tap, ev_rows_move, modes="contact"):
    """Victims' contact reads at one terminal, inside their lookback: tap where the terminal and card
    allow it, another lane of the same merchant where there is one, otherwise the visit is dropped."""
    cat = eng.cat
    term = tid // 10
    t = cat.terminals[term]
    m = cat.merchants[t["merchant"]]
    ev = eng.ev
    for tok in victims_hit:
        f = victims[tok]
        mode = eng.contact if modes == "contact" else eng.cp
        sel = np.nonzero((eng.tok == tok) & (eng.tid == tid) & mode & (eng.day >= f - L) & (eng.day <= f - 1))[0]
        for i in sel:
            if modes == "contact" and eng.ev.kind.values[i] in (S.K_PUR, S.K_PUMP) and t["tap"] and \
                    eng.ev.amount.values[i] <= 100.0 and eng.nfc[ev.slot.values[i]]:
                ev_rows_tap.append(i)
            elif len(m["terminals"]) > 1:
                alt = [x for x in m["terminals"] if x != term]
                ev_rows_move.append((i, int(rng.choice(alt))))
            else:
                ev_rows_drop.append(i)


def apply_edits(eng, drop, tap, move):
    ev = eng.ev.copy()
    if tap:
        ev.loc[ev.index[tap], "entry"] = np.int8(S.E07)
    for i, nt in move:
        ev.loc[ev.index[i], "term"] = np.int32(nt)
    if drop:
        ev = ev.drop(ev.index[drop])
    ev = ev.reset_index(drop=True)
    eng.refresh(ev)


def trim(eng, rng, victims, designed, rules, rounds=14, log=None):
    """rules: list of (victim subset dict, min v, cap, L, base, modes); cap is a number or a function of the
    screen. Softens victims' reads at any non-designed terminal that breaks a rule, until none does."""
    for _ in range(rounds):
        drop, tap, move = [], [], []
        touched = 0
        for sub, vmin, cap, L, base, modes in rules:
            sc = eng.screen(sub, L, base, modes)
            c = cap(sc) if callable(cap) else cap
            bad = sc[(sc.v >= vmin) & (sc.lift > c) & ~sc.index.isin(designed)]
            for tid, r in bad.iterrows():
                target_v = int(np.floor(c * r.base * sc.attrs["n_v"]))
                k = int(r.v) - max(target_v, vmin - 1) if np.isfinite(r.lift) else int(r.v) - (vmin - 1)
                k = max(1, min(int(r.v), k))
                hit = sorted(eng.victims_read_at(sub, int(tid), L, modes))
                pick = [hit[j] for j in rng.permutation(len(hit))[:k]]
                _soften(eng, rng, pick, int(tid), L, victims, drop, tap, move, modes)
                touched += 1
                if log is not None:
                    log.append((int(tid), int(r.v), float(r.lift), k))
        if not touched:
            return True
        apply_edits(eng, sorted(set(drop)), sorted(set(tap) - set(drop)), [(i, t) for i, t in move if i not in set(drop)])
    return False


def car_wash_twin(eng, rng, victims, pump_tokens, wash_tid, sco2_tid, target_v, slot_of_tok, tok_window, L=60):
    """Exactly target_v pump victims read at the car wash in their lookback, and as many other active cards
    read there over the span as at the PIN pad."""
    cat = eng.cat
    wash_term = wash_tid // 10
    wash_merch = cat.terminals[wash_term]["merchant"]
    ev = eng.ev
    hit = eng.victims_read_at({k: victims[k] for k in pump_tokens}, wash_tid, L)
    v = len(hit)
    new_rows, drop = [], []
    if v > target_v:
        hs = sorted(hit)
        for tok in [hs[j] for j in rng.permutation(len(hs))[:v - target_v]]:
            f = victims[tok]
            drop += list(np.nonzero((eng.tok == tok) & (eng.tid == wash_tid) & (eng.day >= f - L) & (eng.day <= f - 1))[0])
    elif v < target_v:
        cand = sorted(set(pump_tokens) - hit)
        for tok in [cand[j] for j in rng.permutation(len(cand))[:target_v - v]]:
            f = victims[tok]
            lo = max(f - L, tok_window[tok][0])
            d = int(rng.integers(lo, f))
            h = 15.5 + 4.5 * rng.random()
            new_rows.append(dict(slot=slot_of_tok[tok], t=d * DAY + int(h * 3600), merch=wash_merch, term=wash_term,
                                 kind=S.K_PUR, amount=round(float(rng.choice([12.0, 14.0, 16.0, 19.0])), 2),
                                 entry=S.E05, resp=0, tag=0, tok=tok))
    _commit(eng, drop, new_rows)
    # base: as many other active cards as the PIN pad
    vic = dict(victims)
    sc = eng.screen(vic, L)
    bw, bs = int(sc.loc[wash_tid, "b"]), int(sc.loc[sco2_tid, "b"])
    fd = np.array(list(victims.values()))
    span0, span1 = fd.min() - L, fd.max() - 1
    isv = np.isin(eng.tok, np.array(sorted(victims)))
    ins = (eng.day >= span0) & (eng.day <= span1)
    new_rows, drop = [], []
    if bw > bs:
        w_idx = np.nonzero(~isv & ins & (eng.tid == wash_tid) & eng.contact)[0]
        toks = sorted(set(eng.tok[w_idx].tolist()))
        for tok in [toks[j] for j in rng.permutation(len(toks))[:bw - bs]]:
            drop += [i for i in w_idx if eng.tok[i] == tok]
    elif bw < bs:
        users = set(eng.tok[~isv & ins & (eng.tid == wash_tid)].tolist())
        # members who already stop at the plaza or live in Kemptville
        plaza_terms = set(cat.fuel["terminals"]) | set(cat.coffee["terminals"])
        near = set(eng.tok[~isv & ins & np.isin(eng.ev.term.values, sorted(plaza_terms))].tolist())
        cand = sorted(near - users)
        for tok in [cand[j] for j in rng.permutation(len(cand))[:bs - bw]]:
            lo = max(span0, tok_window[tok][0])
            hi = min(span1, tok_window[tok][1])
            if hi < lo:
                continue
            d = int(rng.integers(lo, hi + 1))
            h = 9.5 + 10.0 * rng.random()
            new_rows.append(dict(slot=slot_of_tok[tok], t=d * DAY + int(h * 3600), merch=wash_merch, term=wash_term,
                                 kind=S.K_PUR, amount=round(float(rng.choice([12.0, 14.0, 16.0, 19.0])), 2),
                                 entry=S.E05, resp=0, tag=0, tok=tok))
    _commit(eng, drop, new_rows)


def _commit(eng, drop, new_rows):
    ev = eng.ev
    if drop:
        ev = ev.drop(ev.index[sorted(set(drop))])
    if new_rows:
        add = pd.DataFrame(new_rows)
        for c in ev.columns:
            add[c] = add[c].astype(ev[c].dtype)
        ev = pd.concat([ev, add[ev.columns]], ignore_index=True)
    ev = ev.sort_values(["t", "slot"], kind="mergesort").reset_index(drop=True)
    eng.refresh(ev)
