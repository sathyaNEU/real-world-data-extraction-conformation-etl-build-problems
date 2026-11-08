"""task482 architecture 17: the main call's computations on the truth. The Trust's 2026 bank runs (preliminary and
final), the golden recalibration of the Term 3 items on the responses of candidates whose school had finished the
unit before they sat, the drafts' composition, and every rival route the screens and checks run."""
import datetime as dt

import numpy as np

import params as P
import rasch as RA


def matrices(w, keep="last"):
    """Persons-by-items scores and counts from the response rows. keep: 'last' (the later answer of a re-answered
    item, the platform's final response), 'first', or 'both' (every row counted)."""
    idx = {p["entry"]: r for r, p in enumerate(w["online"])}
    I = len(w["pool"]["items"])
    R = np.zeros((len(idx), I))
    M = np.zeros((len(idx), I))
    seen = {}
    for sid, entry, i, v in w["rows"]:
        r = idx[entry]
        if keep == "both":
            R[r, i] += v
            M[r, i] += 1
        elif keep == "first":
            if (r, i) not in seen:
                seen[(r, i)] = 1
                R[r, i], M[r, i] = v, 1
        else:
            R[r, i], M[r, i] = v, 1
    return R, M


def bank_run(w, R=None, M=None, upto=None):
    """The Trust's calibration: every 2026 response, the anchor block held at its banked values."""
    pl = w["pool"]
    if R is None:
        R, M = w["R"], w["M"]
    if upto is not None:
        keep = np.array([p["day"] <= upto for p in w["online"]])
        R, M = R[keep], M[keep]
    fixed = {i: float(pl["b"][i]) for i in pl["anchors"]}
    th, b = RA.calibrate(R, M, fixed)
    return np.round(b, 3), th


def thetas_t12(w, b, R=None, M=None, wle=False):
    pl = w["pool"]
    if R is None:
        R, M = w["R"], w["M"]
    t12 = pl["t12"]
    return RA.fit_theta(R[:, t12], M[:, t12], b[t12], wle=wle)


def recal_t3(w, b, mask, R=None, M=None, th=None, wle=False):
    """Term 3 items re-estimated on the responses `mask` keeps, abilities fixed on the Term 1 and 2 items."""
    pl = w["pool"]
    if R is None:
        R, M = w["R"], w["M"]
    if th is None:
        th = thetas_t12(w, b, R, M, wle=wle)
    t3 = pl["t3"]
    out = b.copy()
    MM = M[:, t3] * mask[:, t3]
    bt = RA.fit_b(R[:, t3] * (MM > 0), MM, th, b0=b[t3])
    bt = np.where(np.isnan(bt), b[t3], bt)
    out[t3] = bt
    return out


def taught_mask(w, lag_days=0, use_utc=False, calendar=None):
    """Per response: the candidate sat after their own school's last day of the item's unit (`lag_days` calendar
    days after it). calendar: None (each school's own sequence and term), 'national' (each school's week number
    read against the national term start), or 'outline' (the course outline's model weeks for every school)."""
    pl, sch = w["pool"], w["schools"]
    items = pl["items"]
    N, I = w["M"].shape
    T = np.ones((N, I), bool)
    units = np.array([it["unit"] for it in items])
    t3 = np.array(pl["t3"])
    for r, p in enumerate(w["online"]):
        s = sch[p["school"]]
        day = p["day"]
        if use_utc:
            h, m = p["period"]
            day = (dt.datetime.combine(day, dt.time(h, m), P.NZST).astimezone(dt.timezone.utc)).date()
        for i in t3:
            u = units[i]
            if calendar == "outline":
                end = dt.date(2026, 8, 21) if u == "U5" else dt.date(2026, 9, 25)
            elif calendar == "national":
                if u != s["first"]:
                    end = dt.date(2026, 9, 25)
                else:
                    end = dt.date(2026, 7, 20) + dt.timedelta(days=7 * (s["week_end1"] - 1) + 4)
            else:
                end = s["end1"] if u == s["first"] else s["term_end"]
            T[r, i] = day > end + dt.timedelta(days=lag_days)
    return T


def golden_b(w, b_bank, **kw):
    T = taught_mask(w)
    return recal_t3(w, b_bank, T.astype(float), **kw), T


def marks(b, drafts, theta=P.THETA_ACHIEVED):
    return {d: RA.expected_mark(b[ix], theta) for d, ix in drafts.items()}


def pick(mk, target=P.TARGET):
    return min(mk, key=lambda d: (abs(mk[d] - target), d))


# ---------------------------------------------------------------- the drafts
def compose(pl):
    """Each draft's 50 items: its Term 3 items (DRAFT_T3), Term 1 and 2 items inside the strand ranges, then
    Term 1 and 2 swaps until its expected Achieved mark on the items' taught difficulties (the truth) sits on
    DRAFT_GOLD. The drafts are fixed with the pool, so the screens redraw everything else around them."""
    b_gold = pl["b"]
    g = np.random.default_rng(P.POOL_SEED + 7)
    items = pl["items"]
    by_unit = {u: [i for i, it in enumerate(items) if it["unit"] == u] for u, _, _, _ in P.UNITS}
    t12_counts = {"A": {"U1": 12, "U2": 13, "U3": 10, "U4": 9}, "B": {"U1": 12, "U2": 12, "U3": 8, "U4": 7},
                  "C": {"U1": 12, "U2": 12, "U3": 5, "U4": 4}}
    drafts = {}
    for d in ("A", "B", "C"):
        u5, u6 = P.DRAFT_T3[d]
        sel = list(g.choice(by_unit["U5"], u5, replace=False)) + list(g.choice(by_unit["U6"], u6, replace=False))
        t12 = []
        for u, k in t12_counts[d].items():
            t12 += list(g.choice(by_unit[u], k, replace=False))
        target = P.DRAFT_GOLD[d]
        for _ in range(4000):
            cur = RA.expected_mark(b_gold[sel + t12], P.THETA_ACHIEVED)
            if abs(cur - target) < 0.02:
                break
            j = int(g.integers(len(t12)))
            u = items[t12[j]]["unit"]
            cands = [i for i in by_unit[u] if i not in t12]
            c = cands[int(g.integers(len(cands)))]
            new = RA.expected_mark(b_gold[sel + t12[:j] + [c] + t12[j + 1:]], P.THETA_ACHIEVED)
            if abs(new - target) < abs(cur - target):
                t12[j] = c
        drafts[d] = sorted(int(i) for i in sel + t12)
    return drafts


# ---------------------------------------------------------------- the rival routes
def rivals(w, b_bank, drafts, R=None, M=None):
    """Expected Achieved marks under every route the screens name. Returns {route: {draft: mark}}."""
    pl = w["pool"]
    out = {}
    if R is None:
        R, M = w["R"], w["M"]
    th = thetas_t12(w, b_bank, R, M)
    T = taught_mask(w)
    out["golden"] = marks(recal_t3(w, b_bank, T.astype(float), R, M, th), drafts)
    out["bank"] = marks(b_bank, drafts)
    for lag in (2, 4):
        out["lag%d" % lag] = marks(recal_t3(w, b_bank, taught_mask(w, lag_days=lag).astype(float), R, M, th), drafts)
    out["utc_day"] = marks(recal_t3(w, b_bank, taught_mask(w, use_utc=True).astype(float), R, M, th), drafts)
    out["wle"] = marks(recal_t3(w, b_bank, T.astype(float), R, M, wle=True), drafts)
    # joint recalibration: untaught Term 3 responses dropped, the anchor block held, everything else re-estimated
    MJ = M * np.where(T, 1.0, 0.0)
    fixed = {i: float(pl["b"][i]) for i in pl["anchors"]}
    _, bj = RA.calibrate(R * (MJ > 0), MJ, fixed)
    out["joint"] = marks(bj, drafts)
    # a single taught shift shared by every Term 3 item
    out["one_shift"] = marks(one_shift(w, b_bank, T, R, M, th), drafts)
    # readers who do not reach the per-response state
    nat = taught_mask(w, calendar="national")
    out["national_weeks"] = marks(recal_t3(w, b_bank, nat.astype(float), R, M, th), drafts)
    outl = taught_mask(w, calendar="outline")
    out["outline_weeks"] = marks(recal_t3(w, b_bank, outl.astype(float), R, M, th) if outl[:, pl["t3"]].any()
                                 else b_bank, drafts)
    wk5 = np.ones_like(T)
    days = np.array([p["day"] for p in w["online"]])
    for i in pl["t3"]:
        u = pl["items"][i]["unit"]
        wk5[:, i] = days >= dt.date(2026, 8, 17) if u == "U5" else False
    out["outline_last_week"] = marks(recal_t3(w, b_bank, wk5.astype(float), R, M, th) if wk5[:, pl["t3"]].any()
                                     else b_bank, drafts)
    late = np.zeros_like(T)
    late[days >= P.WINDOW[-3], :] = True
    out["last_days"] = marks(recal_t3(w, b_bank, late.astype(float), R, M, th), drafts)
    whole = np.zeros_like(T)
    sch = w["schools"]
    for r, p in enumerate(w["online"]):
        s = sch[p["school"]]
        for i in pl["t3"]:
            whole[r, i] = pl["items"][i]["unit"] == s["first"] and s["end1"] < s["days"][0]
    out["whole_school"] = marks(recal_t3(w, b_bank, whole.astype(float), R, M, th) if whole[:, pl["t3"]].sum() > 50
                                else b_bank, drafts)
    out["trend"] = marks(trend(w, b_bank, R, M, th), drafts)
    return out


def one_shift(w, b_bank, T, R, M, th, it=12):
    pl = w["pool"]
    t3 = pl["t3"]
    Rt, Mt, Tt = R[:, t3], M[:, t3], T[:, t3].astype(float)
    b = b_bank[t3].copy()
    gam = 0.0
    for _ in range(it):
        off = gam * Tt
        for _ in range(6):
            p = RA.sig(th[:, None] - b[None, :] + off)
            b = b + (p * Mt - Rt).sum(0) / np.maximum((p * (1 - p) * Mt).sum(0), 1e-9)
        for _ in range(6):
            p = RA.sig(th[:, None] - b[None, :] + gam * Tt)
            gr = ((Rt - p * Mt) * Tt).sum()
            hs = (p * (1 - p) * Mt * Tt).sum()
            gam += gr / max(hs, 1e-9)
    out = b_bank.copy()
    out[t3] = b - gam
    return out


def trend(w, b_bank, R, M, th):
    """Each Term 3 item's residual against the bank, regressed on the sitting day and carried to the window's
    last day."""
    pl = w["pool"]
    days = np.array([(p["day"] - P.WINDOW[0]).days for p in w["online"]], float)
    out = b_bank.copy()
    last = (P.WINDOW[-1] - P.WINDOW[0]).days
    for i in pl["t3"]:
        m = M[:, i] > 0
        p = RA.sig(th[m] - b_bank[i])
        res = R[m, i] - p
        slope = np.polyfit(days[m], res, 1)[0]
        info = (p * (1 - p)).mean()
        out[i] = b_bank[i] - slope * (last - days[m].mean()) / max(info, 1e-6)
    return out
