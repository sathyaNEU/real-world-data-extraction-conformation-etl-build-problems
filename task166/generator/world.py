"""The world behind the pack, before any record is written: Plinthwise's customer companies, the people on their
workspaces, the job moves that end a person's seat at one customer, and the new customers those people found.

A share of new paying customers each month is founded by a project manager, superintendent or project engineer who
left a paying customer for a contractor not yet on the software, carrying the tool with them; the lag from leaving to
the new company's first paid invoice runs four to twenty months. Between April and September 2026 the Southwest's
large general contractors released most of the project staff of a finished programme of large builds, and the region's
other customers trimmed theirs: those people found new customers through 2027.

simulate() returns the accounts, users, founder events, the monthly arrays and the truths the checks need: the expected
2027 new paying customers by region under FP&A's planning basis (organic intensity at the plan's spend, founders from
the departures already made and from users leaving at each region's 2025 monthly pace from October 2026)."""
from __future__ import annotations

import math

import numpy as np

import common as K

SEASON = np.array([0.82, 0.88, 1.05, 1.12, 1.10, 1.06, 1.02, 1.00, 1.04, 1.05, 0.95, 0.91])
SEED_ROLES = ("PM", "SUPER", "PE")
OTHER_ROLES = ("OWNER", "OFFICE", "FIELD")
PRM = dict(
    base=[8.6, 9.0, 11.5, 8.0, 6.6, 7.9],             # organic new paying customers a month in January 2019, before season
    growth=[0.075, 0.08, 0.075, 0.06, 0.05, 0.065],    # organic growth a year
    acc0=[55, 60, 70, 60, 48, 55],                     # paying customers in January 2015
    churn=0.013, churn_mid=0.55, churn_big=0.28,       # monthly cancellation of an account of four users or fewer,
    gc_churn=0.15,                                     # and the share of that rate for 5 to 10 users, more, and large GCs
    hazard=0.0145,                                     # monthly job-move hazard of project staff
    other_hazard=0.010,
    p_seed=0.073,                                      # chance a leaver founds a new paying customer
    p_join=0.22,                                       # chance a leaver joins an existing customer
    lag_k=4.0, lag_theta=1.5, lag_offset=5,            # months from leaving to the new customer's first paid invoice
    same_region=0.88,
    spend_elast=0.25,
    gc_n=[16, 6, 9, 6, 5, 6],                          # large general contractors among the 2015 to 2019 customers
    gc_users=(170, 330),
    wave_from=87, wave_to=92,                          # April to September 2026
    wave_gc=14, wave_gc_mult=12.0, wave_gc_replace=0.10,
    wave_rest_mult=2.5, wave_rest_replace=0.45,
    plan_lift=[1.14, 1.12, 1.15, 1.11, 1.10, 1.12],
)


def lag_pmf(P, n=40):
    """pmf over lags of 1..n months (index 0 is one month): the offset with nothing, then a gamma."""
    from scipy.stats import gamma
    edges = np.arange(n + 1) - P["lag_offset"]
    c = gamma.cdf(np.maximum(edges, 0), P["lag_k"], scale=P["lag_theta"])
    p = np.diff(c)
    return p / p.sum()


class Pool:
    """A set with O(1) add, remove and uniform sampling."""

    def __init__(self):
        self.items, self.pos = [], {}

    def add(self, x):
        if x not in self.pos:
            self.pos[x] = len(self.items)
            self.items.append(x)

    def remove(self, x):
        i = self.pos.pop(x, None)
        if i is None:
            return
        last = self.items.pop()
        if i < len(self.items):
            self.items[i] = last
            self.pos[last] = i

    def __len__(self):
        return len(self.items)

    def sample(self, r, k):
        idx = r.choice(len(self.items), size=k, replace=False)
        return [self.items[i] for i in idx]


def spend_and_intensity(P):
    """Marketing spend ($K a month by region, February 2019 to January 2028, the plan from October 2026) and the
    organic intensity of new paying customers."""
    r_ = K.rng(1)
    R = 6
    base, growth = np.array(P["base"]), np.array(P["growth"])
    ts = np.arange(K.T0, 109)
    spend = np.full((R, len(ts)), np.nan)
    s0 = base * 6.0
    for i, t in enumerate(ts):
        if t < 1:
            continue
        for r in range(R):
            trend = s0[r] * 1.06 ** (t / 12) * SEASON[t % 12]
            if t <= K.T_OBS:
                spend[r, i] = round(trend * math.exp(r_.normal(0, 0.16)), 1)
            else:
                spend[r, i] = round(trend * P["plan_lift"][r], 0)
    obs = (ts >= 1) & (ts <= K.T_OBS)
    sbar = np.nanmean(spend[:, obs], axis=1)
    lam = np.zeros((R, len(ts)))
    for i, t in enumerate(ts):
        for r in range(R):
            f = (spend[r, i] / sbar[r]) ** P["spend_elast"] if t >= 1 else 1.0
            lam[r, i] = base[r] * math.exp(growth[r] * t / 12) * SEASON[t % 12] * f
    return ts, spend, lam


def simulate(P=None):
    P = dict(PRM, **(P or {}))
    R = 6
    ts, spend, lam = spend_and_intensity(P)
    ix = {t: i for i, t in enumerate(ts)}
    pmf = lag_pmf(P)
    r_ = K.rng(2)
    accounts, users = [], []
    acct_users = {}
    seed_pool = [Pool() for _ in range(R)]
    other_pool = [Pool() for _ in range(R)]
    open_accts = [Pool() for _ in range(R)]
    persons = [0]
    seed_queue, pending_hires, pending_joins, seed_events = {}, {}, {}, []

    def new_person():
        persons[0] += 1
        return persons[0]

    def add_user(acct, role, t, pid=None):
        if pid is None:
            pid = new_person()
        u = dict(uid=len(users) + 1, pid=pid, acct=acct, role=role, created_t=t, deact_t=None, reason="")
        users.append(u)
        acct_users.setdefault(acct, []).append(u["uid"])
        reg = accounts[acct - 1]["region"]
        (seed_pool if role in SEED_ROLES else other_pool)[reg].add(u["uid"])
        return u

    def drop_user(uid, t, reason):
        u = users[uid - 1]
        u["deact_t"] = t
        u["reason"] = reason
        reg = accounts[u["acct"] - 1]["region"]
        (seed_pool if u["role"] in SEED_ROLES else other_pool)[reg].remove(uid)
        acct_users[u["acct"]].remove(uid)

    def open_account(region, t, kind, founder_pid=None, founder_role="PM", gc=False):
        a = dict(id=len(accounts) + 1, region=region, start_t=t, close_t=None, kind=kind, gc=gc, wave=False)
        accounts.append(a)
        open_accts[region].add(a["id"])
        frole = founder_role if kind == "champion" else ("OWNER" if r_.random() < 0.45 else "PM")
        f = add_user(a["id"], frole, t, founder_pid)
        a["founder_uid"] = f["uid"]
        if gc:
            n_seed = int(r_.integers(P["gc_users"][0], P["gc_users"][1] + 1))
            n_other = int(n_seed * r_.uniform(0.25, 0.4))
            spread = 8
        else:
            n_seed = max(1, int(round(r_.lognormal(math.log(4.5), 0.75))))
            n_other = max(1, int(round(r_.lognormal(math.log(2.5), 0.6))))
            spread = 3
        for _ in range(n_seed - (1 if frole in SEED_ROLES else 0)):
            add_user(a["id"], str(r_.choice(SEED_ROLES, p=[0.45, 0.35, 0.20])), t + int(r_.integers(0, spread)))
        for _ in range(n_other - (0 if frole in SEED_ROLES else 1)):
            add_user(a["id"], str(r_.choice(OTHER_ROLES, p=[0.25, 0.45, 0.30])), t + int(r_.integers(0, spread)))
        return a

    # the 2015 book and the large general contractors (opened 2015 to 2019)
    for r in range(R):
        for _ in range(int(P["acc0"][r])):
            open_account(r, K.T0 - int(r_.integers(1, 30)), "legacy")
    gc_start = {}
    for r in range(R):
        for k in range(int(P["gc_n"][r])):
            gc_start.setdefault(int(r_.integers(K.T0, 6)), []).append(r)
    haz = np.full((R, len(ts)), P["hazard"])
    for t in ts:
        i = ix[t]
        for r in gc_start.get(int(t), []):
            open_account(r, int(t), "organic", gc=True)
        if t == P["wave_from"]:
            # the Southwest's large general contractors on the finished programme of large builds
            gcs = [a for a in accounts if a["gc"] and a["region"] == K.SW and a["close_t"] is None]
            gcs.sort(key=lambda a: -len(acct_users.get(a["id"], [])))
            for a in gcs[:int(P["wave_gc"])]:
                a["wave"] = True
        # cancellations, likelier the smaller the account: every user goes with the account
        for r in range(R):
            n_close = r_.binomial(len(open_accts[r]), P["churn"])
            for aid in (open_accts[r].sample(r_, n_close) if n_close else []):
                a = accounts[aid - 1]
                nu = len(acct_users.get(aid, []))
                keep = P["gc_churn"] if a["gc"] else (1.0 if nu <= 4 else (P["churn_mid"] if nu <= 10 else P["churn_big"]))
                if a["start_t"] >= t or r_.random() > keep:
                    continue
                a["close_t"] = int(t)
                open_accts[r].remove(aid)
                for uid in list(acct_users.get(aid, [])):
                    drop_user(uid, int(t), "Account closed")
        # new paying customers this month: organic, then founded by leavers
        for r in range(R):
            for _ in range(r_.poisson(lam[r, i])):
                open_account(r, int(t), "organic")
        for (dest, pid, oacct, dep_t, role) in seed_queue.pop(int(t), []):
            a = open_account(dest, int(t), "champion", founder_pid=pid, founder_role=role)
            seed_events.append(dict(acct=a["id"], dest=dest, pid=pid, origin_acct=oacct, dep_t=dep_t, land_t=int(t)))
        for (acct, role) in pending_hires.pop(int(t), []):
            if accounts[acct - 1]["close_t"] is None:
                add_user(acct, role, int(t))
        for (pid, dest, role) in pending_joins.pop(int(t), []):
            if len(open_accts[dest]):
                add_user(open_accts[dest].sample(r_, 1)[0], role, int(t), pid)
        in_wave = P["wave_from"] <= t <= P["wave_to"]
        # job moves of project staff from customers that stay open
        for r in range(R):
            n = len(seed_pool[r])
            if not n:
                continue
            cand = []
            if in_wave and r == K.SW:
                # the wave: the programme's general contractors and the rest of the region's customers separately
                gc_u = [uid for uid in seed_pool[r].items if accounts[users[uid - 1]["acct"] - 1]["wave"]]
                rest = n - len(gc_u)
                k_gc = min(len(gc_u), r_.poisson(len(gc_u) * P["hazard"] * P["wave_gc_mult"]))
                if k_gc:
                    cand += [(uid, P["wave_gc_replace"]) for uid in r_.choice(gc_u, size=k_gc, replace=False)]
                gset = set(gc_u)
                k_rest = min(rest, r_.poisson(rest * P["hazard"] * P["wave_rest_mult"]))
                if k_rest:
                    pool = [uid for uid in seed_pool[r].items if uid not in gset]
                    cand += [(uid, P["wave_rest_replace"]) for uid in r_.choice(pool, size=k_rest, replace=False)]
            else:
                k = min(n, r_.poisson(n * P["hazard"]))
                cand = [(uid, 1.0) for uid in (seed_pool[r].sample(r_, k) if k else [])]
            for uid, p_replace in cand:
                uid = int(uid)
                u = users[uid - 1]
                if u["created_t"] >= t:
                    continue
                drop_user(uid, int(t), "Left company")
                dest = r if r_.random() < P["same_region"] else int(r_.choice([x for x in range(R) if x != r]))
                v = r_.random()
                if v < P["p_seed"]:
                    lag = 1 + int(r_.choice(len(pmf), p=pmf))
                    seed_queue.setdefault(int(t) + lag, []).append((dest, u["pid"], u["acct"], int(t), u["role"]))
                elif v < P["p_seed"] + P["p_join"]:
                    pending_joins.setdefault(int(t) + 1 + int(r_.integers(0, 4)), []).append((u["pid"], dest, u["role"]))
                if r_.random() < p_replace:
                    pending_hires.setdefault(int(t) + 1 + int(r_.integers(0, 3)), []).append((u["acct"], u["role"]))
            # the other roles turn over too (with the same wave), and found nothing
            n = len(other_pool[r])
            if not n:
                continue
            if in_wave and r == K.SW:
                gc_o = [uid for uid in other_pool[r].items if accounts[users[uid - 1]["acct"] - 1]["wave"]]
                gset = set(gc_o)
                rest_o = [uid for uid in other_pool[r].items if uid not in gset]
                ko = []
                k1 = min(len(gc_o), r_.poisson(len(gc_o) * P["other_hazard"] * P["wave_gc_mult"]))
                if k1:
                    ko += [(int(u_), P["wave_gc_replace"]) for u_ in r_.choice(gc_o, size=k1, replace=False)]
                k2 = min(len(rest_o), r_.poisson(len(rest_o) * P["other_hazard"] * P["wave_rest_mult"]))
                if k2:
                    ko += [(int(u_), P["wave_rest_replace"]) for u_ in r_.choice(rest_o, size=k2, replace=False)]
            else:
                k = min(n, r_.poisson(n * P["other_hazard"]))
                ko = [(uid, 1.0) for uid in (other_pool[r].sample(r_, k) if k else [])]
            for uid, p_replace in ko:
                u = users[uid - 1]
                if u["created_t"] >= t:
                    continue
                drop_user(uid, int(t), "Left company")
                if r_.random() < p_replace:
                    pending_hires.setdefault(int(t) + 1 + int(r_.integers(0, 3)), []).append((u["acct"], u["role"]))
    # monthly arrays over the world's months
    n_t = len(ts)
    new = np.zeros((R, n_t), int)
    seeds = np.zeros((R, n_t), int)
    dep = np.zeros((R, n_t), int)            # project staff leaving paying customers that stay open
    dep_all = np.zeros((R, n_t), int)        # every job move off an open customer, any role
    champ_ids = {e["acct"] for e in seed_events}
    for a in accounts:
        if K.T0 <= a["start_t"] <= ts[-1]:
            new[a["region"], ix[a["start_t"]]] += 1
            if a["id"] in champ_ids:
                seeds[a["region"], ix[a["start_t"]]] += 1
    for u in users:
        if u["reason"] == "Left company" and u["deact_t"] is not None and u["deact_t"] in ix:
            reg = accounts[u["acct"] - 1]["region"]
            dep_all[reg, ix[u["deact_t"]]] += 1
            if u["role"] in SEED_ROLES:
                dep[reg, ix[u["deact_t"]]] += 1
    W = dict(P=P, ts=ts, ix=ix, spend=spend, lam=lam, pmf=pmf, accounts=accounts, users=users, seed_events=seed_events,
             new=new, seeds=seeds, dep=dep, dep_all=dep_all, persons=persons[0])
    W["truth"] = truth(W)
    return W


def window_weight(pmf, t):
    """The share of a month-t leaver's founding that lands in calendar 2027."""
    return float(sum(pmf[L] for L in range(len(pmf)) if 96 <= t + 1 + L <= 107))


def founder_landings_2027(dep, ix, pmf, p, same, future):
    """Expected 2027 founder-led customers by region: realised leavers to September 2026 and planned leavers after."""
    R = dep.shape[0]
    S = np.full((R, R), (1 - same) / (R - 1))
    np.fill_diagonal(S, same)
    out = np.zeros(R)
    for t in range(K.T0, 108):
        w = window_weight(pmf, t)
        if w <= 0:
            continue
        d = dep[:, ix[t]] if t <= K.T_OBS else future
        out += (d * p * w) @ S
    return out


def truth(W):
    """Expected 2027 new paying customers by region under the planning basis, in the world's own terms: organic
    intensity at the plan's spend, plus founders from leavers to September 2026 and from leavers at each region's 2025
    monthly pace from October 2026 (all job moves of project staff, as the founder yield is defined per such move)."""
    P, ix = W["P"], W["ix"]
    org = W["lam"][:, [ix[t] for t in K.Y27]].sum(1)
    fut = W["dep"][:, [ix[t] for t in range(72, 84)]].mean(1)
    ch = founder_landings_2027(W["dep"], ix, W["pmf"], P["p_seed"], P["same_region"], fut)
    return dict(org27=org, champ27=ch, total=org + ch)
