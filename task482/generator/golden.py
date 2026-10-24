"""The golden: the cap schedule under the policy, every ladder rung and every standing-family member, all computed from
the pack's tables (the benefit periods extract, the two EMR exports, the crosswalk, the code map), never from the world.

    project(tb, ret, A, post, open_) -> {ccn: (count, rows)}
"""
import datetime as dt

import numpy as np

import world as W

FY0, FY1, CLOSE = W.FY[0], W.FY[1], W.CLOSE
GRID = 6000


def day(d):
    return (d - W.DAY0).days


def norm_dx(code):
    code = code.strip().upper()
    return code if "." in code or len(code) <= 3 else code[:3] + "." + code[3:]


class Book:
    """Stays per beneficiary from the extract, each beneficiary's diagnosis group and the provider numbers' experience."""

    def __init__(self, tb, wendleglen):
        self.wendleglen = set(wendleglen)
        cw = {r["hicn"]: r["mbi"] for r in tb["crosswalk"]}
        grp = {r["code"]: r["group"] for r in tb["dx"]}
        self.group = {}
        latest = {}
        for r in tb["emr"]:
            if r["payer"] != "Medicare" or not r["medicare_id"]:
                continue
            m = cw.get(r["medicare_id"], r["medicare_id"])
            if m not in latest or r["admit_date"] >= latest[m]:
                latest[m] = r["admit_date"]
                self.group[m] = grp[norm_dx(r["primary_dx"])]
        for r in tb["legacy"]:
            m = cw.get(r["medicare_no"], r["medicare_no"])
            if m not in latest or r["admit"] > latest[m]:
                latest[m] = r["admit"]
                self.group[m] = grp[norm_dx(r["dx"])]
        by = {}
        for r in tb["extract"]:
            by.setdefault(r["mbi"], {}).setdefault(r["elect"], []).append(r)
        self.stays = {}
        self.dod = {}
        for m, el in by.items():
            lst = []
            for e, rows in sorted(el.items()):
                rows.sort(key=lambda r: r["start"])
                n = sum(r["days"] for r in rows)
                s = day(e)
                dod = rows[0]["dod"]
                open_ = rows[-1]["end"] is None
                end = s + n
                death = (not open_) and dod is not None and day(dod) == end - 1
                lst.append(dict(start=s, days=n, end=end, open=open_, death=death, first=rows[0]["ccn"],
                                last=rows[-1]["ccn"], segs=[(r["ccn"], day(r["start"]), r["days"]) for r in rows]))
            self.stays[m] = lst
            self.dod[m] = day(rows[0]["dod"]) if rows[0]["dod"] is not None else None
        self._experience()

    # -- the provider numbers' experience, by provider number and diagnosis group
    def _experience(self):
        self.stay_rows = {}      # (ccn, g) -> list of (length, kind)  kind: death | live | cen
        self.live_rows = {}      # (ccn, g) -> list of (time, kind, follow-up, next stay index)  kind: ret | death | cen
        self.live_in = {}        # same, a return counted only at the organisation's provider numbers
        self.ret_stays = {}      # (ccn, g) -> list of (length, observed, return day)
        self.ret_in = {}
        self.later = {}          # (ccn, g) -> list of (total later days to the close, return day)
        self.closed_2026 = {}    # (ccn, g) -> lengths of the provider number's stays ending in 2026 (census average)
        y0, y1 = day(dt.date(2026, 1, 1)), CLOSE
        for m, lst in self.stays.items():
            g = self.group.get(m)
            if g is None:
                continue
            dod = self.dod[m]
            for k, st in enumerate(lst):
                if st["start"] >= CLOSE:
                    continue
                if st["first"] in self.wendleglen and st["start"] >= 0:
                    kind = "cen" if st["open"] else ("death" if st["death"] else "live")
                    self.stay_rows.setdefault((st["first"], g), []).append((st["days"], kind))
                if st["last"] in self.wendleglen and not st["open"] and y0 <= st["end"] - 1 < y1:
                    here = 0
                    for ccn, s0, n in reversed(st["segs"]):
                        if ccn != st["last"]:
                            break
                        here += n
                    self.closed_2026.setdefault((st["last"], g), []).append(here)
                if st["open"] or st["death"] or st["last"] not in self.wendleglen or st["end"] < 0 or st["end"] > CLOSE:
                    continue
                key = (st["last"], g)
                nxt = lst[k + 1] if k + 1 < len(lst) and lst[k + 1]["start"] < CLOSE else None
                fu = CLOSE - st["end"]
                if nxt is not None:
                    row = (nxt["start"] - st["end"], "ret")
                    self.ret_stays.setdefault(key, []).append((nxt["days"], not nxt["open"], nxt["start"]))
                    later = sum(x["days"] for x in lst[k + 1:] if x["start"] < CLOSE)
                    self.later.setdefault(key, []).append((later, nxt["start"]))
                elif dod is not None and dod <= CLOSE:
                    row = (dod - st["end"], "death")
                else:
                    row = (CLOSE - st["end"], "cen")
                self.live_rows.setdefault(key, []).append((row[0], row[1], fu))
                nin = next((x for x in lst[k + 1:] if x["start"] < CLOSE and x["first"] in self.wendleglen), None)
                if nin is not None and nxt is nin:
                    rin = (nin["start"] - st["end"], "ret")
                    self.ret_in.setdefault(key, []).append((nin["days"], not nin["open"], nin["start"]))
                elif dod is not None and dod <= CLOSE:
                    rin = (dod - st["end"], "death")
                else:
                    rin = (CLOSE - st["end"], "cen")
                self.live_in.setdefault(key, []).append((rin[0], rin[1], fu))


def km(lengths, observed):
    T = np.clip(np.asarray(lengths, int), 0, GRID)
    obs = np.asarray(observed, bool)
    ev = np.bincount(T[obs], minlength=GRID + 1)
    ce = np.bincount(T[~obs], minlength=GRID + 1)
    at = len(T) - np.concatenate([[0], np.cumsum(ev + ce)[:-1]])
    return np.cumprod(1 - np.where(at > 0, ev / np.maximum(at, 1), 0.0))     # S[t] = P(T > t)


def mrl_fn(S):
    tail = np.concatenate([np.cumsum(S[::-1])[::-1], [0.0]])
    def f(e):
        e = int(min(max(e, 0), len(S) - 1))
        Se = S[e - 1] if e > 0 else 1.0
        return float(tail[e] / Se) if Se > 0 else 0.0
    return f


def aj(rows, what="ret"):
    """Aalen-Johansen: rows (time, kind) with kind `what`, a competing kind, or cen. Returns (p(s), F_inf):
    p(s) the chance of `what` after s given neither event by s."""
    T = np.array([min(max(int(r[0]), 0), GRID) for r in rows])
    K = np.array([r[1] for r in rows])
    hit = np.bincount(T[K == what], minlength=GRID + 1)
    oth = np.bincount(T[(K != what) & (K != "cen")], minlength=GRID + 1)
    cen = np.bincount(T[K == "cen"], minlength=GRID + 1)
    at = len(T) - np.concatenate([[0], np.cumsum(hit + oth + cen)[:-1]])
    S = np.ones(GRID + 1)
    F = np.zeros(GRID + 1)
    s, fr = 1.0, 0.0
    for t in range(GRID + 1):
        if at[t] > 0:
            fr += s * hit[t] / at[t]
            s *= 1 - (hit[t] + oth[t]) / at[t]
        S[t], F[t] = s, fr
    Finf = F[-1]
    def p(x):
        x = int(min(max(x, 0), GRID))
        return float((Finf - F[x]) / S[x]) if S[x] > 1e-12 else 0.0
    return p, float(Finf)


def empirical(rows, min_fu=1461):
    arr = [(t, k) for t, k, fu in rows if fu >= min_fu]
    def p(s):
        den = sum(1 for t, k in arr if t > s)
        num = sum(1 for t, k in arr if t > s and k == "ret")
        return num / den if den else 0.0
    return p


class Estimates:
    def __init__(self, book):
        self.b = book
        self.cache = {}

    def get(self, name, key):
        ck = (name, key)
        if ck in self.cache:
            return self.cache[ck]
        b = self.b
        if name == "mrl":
            rows = b.stay_rows.get(key, [])
            v = mrl_fn(km([r[0] for r in rows], [r[1] != "cen" for r in rows]))
        elif name == "mrl_ret":
            rows = b.ret_stays.get(key, [])
            v = mrl_fn(km([r[0] for r in rows], [r[1] for r in rows]))
        elif name == "plive":
            rows = b.stay_rows.get(key, [])
            closed = [r for r in rows if r[1] != "cen"]
            share = sum(1 for r in closed if r[1] == "live") / len(closed) if closed else 0.0
            v = lambda e, share=share: share
        elif name == "plive_e":
            rows = b.stay_rows.get(key, [])
            v = aj([(r[0], "ret" if r[1] == "live" else r[1]) for r in rows])[0]
        elif name == "aj":
            v = aj([(t, k) for t, k, fu in b.live_rows.get(key, [])])
        elif name == "aj_in":
            v = aj([(t, k) for t, k, fu in b.live_in.get(key, [])])
        elif name == "emp":
            v = empirical(b.live_rows.get(key, []))
        elif name == "A_km":
            rows = b.ret_stays.get(key, [])
            v = float(km([r[0] for r in rows], [r[1] for r in rows]).sum()) if rows else 0.0
        elif name == "A_in":
            rows = b.ret_in.get(key, [])
            v = float(km([r[0] for r in rows], [r[1] for r in rows]).sum()) if rows else 0.0
        elif name in ("A_after5", "A_after3"):
            yrs = 1826 if name == "A_after5" else 1096
            rows = [x for x, s in b.later.get(key, []) if s < CLOSE - yrs]
            v = float(np.mean(rows)) if rows else 0.0
        elif name == "alos":
            rows = b.closed_2026.get(key, [])
            v = float(np.mean(rows)) if rows else 0.0
        else:
            raise KeyError(name)
        self.cache[ck] = v
        return v


def cohort(book):
    """Each beneficiary with FY2026 days at the organisation's provider numbers: FY2026 days by provider number, days
    to the close in every hospice, state at the close, the last provider number that cared for them, the group."""
    out = []
    for m, lst in book.stays.items():
        fy = {}
        kn = 0
        last_eg = None
        for st in lst:
            if st["start"] >= CLOSE:
                continue
            kn += min(st["days"], CLOSE - st["start"])
            for ccn, s, n in st["segs"]:
                a, z = max(s, FY0), min(s + n, FY1)
                if ccn in book.wendleglen and z > a:
                    fy[ccn] = fy.get(ccn, 0) + (z - a)
                if ccn in book.wendleglen and s < CLOSE:
                    last_eg = ccn
        if not fy:
            continue
        seen = [st for st in lst if st["start"] < CLOSE]
        last = seen[-1]
        dod = book.dod[m]
        if last["open"]:
            ret_stay = last["first"] not in book.wendleglen
            state = ("open", CLOSE - last["start"], ret_stay)
        elif last["death"] or (dod is not None and dod <= CLOSE - 1):
            state = ("dead",)
        else:
            state = ("out", CLOSE - last["end"])
        out.append(dict(mbi=m, fy=fy, known=kn, state=state, home=last_eg, g=book.group[m]))
    return out


def future(row, est, ret="aj", A="km", post="cond", open_="km"):
    st = row["state"]
    key = (row["home"], row["g"])
    a = est.get({"km": "A_km", "after5": "A_after5", "after3": "A_after3", "alos": "alos", "in": "A_in"}[A], key)
    if st[0] == "dead":
        return 0.0
    if st[0] == "open":
        e, ret_stay = st[1], st[2]
        if open_ == "none":
            return 0.0
        if open_ == "alos":
            return max(0.0, est.get("alos", key) - e)
        if ret_stay:
            return est.get("mrl_ret", key)(e)
        f = est.get("mrl", key)(e)
        if post != "none":
            pl = est.get("plive_e", key)(e) if post in ("cond", "in") else est.get("plive", key)(e)
            finf = est.get("aj_in" if post == "in" else "aj", key)[1]
            f += pl * finf * a
        return f
    s = st[1]
    if ret == "none":
        return 0.0
    if ret == "uncond":
        return est.get("aj", key)[1] * a
    if ret == "aj":
        return est.get("aj", key)[0](s) * a
    if ret == "emp":
        return est.get("emp", key)(s) * a
    if ret == "in":
        return est.get("aj_in", key)[0](s) * a
    raise KeyError(ret)


RUNGS = {
    "R0": dict(ret="none", post="none", open_="none"),
    "R1": dict(ret="none", post="none", open_="alos"),
    "R2": dict(ret="none", post="none", open_="km"),
    "R3": dict(ret="uncond", post="all", open_="km"),
    "R3n": dict(ret="uncond", post="none", open_="km"),
    "R3c": dict(ret="uncond", A="alos", post="none", open_="km"),
    "R4": dict(ret="in", A="in", post="in", open_="km"),
    "R5": dict(ret="aj", A="alos", post="cond", open_="km"),
    "R6": dict(ret="aj", A="km", post="none", open_="km"),
    "G": dict(ret="aj", A="km", post="cond", open_="km"),
}
FAMILY = [dict(ret=r, A=a, post=p, open_="km") for r in ("aj", "emp") for a in ("km", "after5", "after3") for p in ("cond", "all")]


def counts(rows, est, **opts):
    out = {}
    for r in rows:
        D = r["known"] + future(r, est, **opts)
        for ccn, d in r["fy"].items():
            out[ccn] = out.get(ccn, 0.0) + d / D
    return out


def schedule(rows, est, **opts):
    out = []
    for r in rows:
        f = future(r, est, **opts)
        D = r["known"] + f
        for ccn, d in sorted(r["fy"].items()):
            out.append(dict(mbi=r["mbi"], ccn=ccn, fy_days=d, known=r["known"], expected_after=f, share=d / D))
    return out


def repayment(payments, count):
    """Policy section 3: 98 per cent of the payments before sequestration above the cap, nil when under it."""
    return max(0.0, 0.98 * (payments - count * W.CAP))
