"""The task121 world, simulated forward from the mechanism.

Accounts, basket sessions, the club's tokens, loyalty profiles, address book, stored cards, flag
cohorts, payment authentication attempts, orders and their finance rows. Every table is a record; no
graded figure is authored here. Outcomes in the baseline weeks and in the static review cells are
allocated with a running carry so each population's rate is exact; the address-check pool is
simulated session by session because its exposure drains as accounts re-save."""
import datetime as dt
import hashlib

import numpy as np
import pandas as pd

import params as P

HOUR_W = np.array([0.25, 0.15, 0.08, 0.05, 0.05, 0.08, 0.2, 0.45, 0.7, 0.9, 1.0, 1.05, 1.15, 1.1, 1.0,
                   0.95, 0.95, 1.0, 1.1, 1.25, 1.4, 1.45, 1.1, 0.6])
DAY_W = np.array([1.0, 0.97, 0.98, 1.0, 1.08, 1.12, 1.05])


def hx(s, n=12):
    return hashlib.sha1(s.encode()).hexdigest()[:n]


def week_of(t):
    for i in range(len(P.WEEK_STARTS) - 1, -1, -1):
        if t >= P.WEEK_STARTS[i]:
            return P.WEEK_NAMES[i]
    raise ValueError(t)


class Carry:
    """Running allocator: k = round(cumulative expected) - cumulative assigned, per family."""

    def __init__(self):
        self.exp, self.got = {}, {}

    def k(self, fam, n, rate):
        self.exp[fam] = self.exp.get(fam, 0.0) + n * rate
        k = int(np.floor(self.exp[fam] + 0.5)) - self.got.get(fam, 0)
        k = max(0, min(n, k))
        self.got[fam] = self.got.get(fam, 0) + k
        return k

    def kx(self, fam, expected, cap):
        self.exp[fam] = self.exp.get(fam, 0.0) + expected
        k = int(np.floor(self.exp[fam] + 0.5)) - self.got.get(fam, 0)
        k = max(0, min(cap, k))
        self.got[fam] = self.got.get(fam, 0) + k
        return k


def sample_times(rng, n, week, start_floor=None):
    """n session start times inside a week, Lisbon local, none within two minutes of a week edge."""
    ws = np.datetime64(P.WEEK_STARTS[P.WEEK_NAMES.index(week)], "s")
    pd_ = DAY_W / DAY_W.sum()
    ph = HOUR_W / HOUR_W.sum()
    lo = 120
    if start_floor is not None:
        lo = max(lo, int((np.datetime64(start_floor, "s") - ws) / np.timedelta64(1, "s")))
    got = np.empty(0, dtype=np.int64)
    while len(got) < n:
        m = (n - len(got)) * 2 + 10
        sec = (rng.choice(7, size=m, p=pd_) * 86400 + rng.choice(24, size=m, p=ph) * 3600
               + rng.integers(0, 3600, size=m))
        sec = sec[(sec >= lo) & (sec <= 7 * 86400 - 120)]
        got = np.concatenate([got, sec])
    got = np.sort(got[:n])
    return [dt.datetime(*P.WEEK_STARTS[P.WEEK_NAMES.index(week)].timetuple()[:6]) + dt.timedelta(seconds=int(x))
            for x in got]


# --------------------------------------------------------------------------- accounts

def make_accounts(rng):
    rows = []
    ids = set()

    def new_id():
        while True:
            v = f"C{int(rng.integers(1_100_000, 4_899_999)):07d}"
            if v not in ids:
                ids.add(v)
                return v

    spec = [("MEMBER", 2150, 0.744, 1.6), ("CP4", 2860, 1.40, 0.55), ("XY", 1850, 0.97, 1.0),
            ("OTHER", 9400, 0.915, 1.0)]
    cp4_cohort_w = np.array([1.15, 0.92, 1.10, 0.82, 1.02, 1.78, 0.95, 0.60, 1.08, 0.9, 1.0, 0.86])
    cp4_cohort_w = cp4_cohort_w / cp4_cohort_w.sum()
    for klass, n, mean, shape in spec:
        lam = rng.gamma(shape, mean / shape, size=n)
        for i in range(n):
            if klass == "CP4":
                coh = int(rng.choice(12, p=cp4_cohort_w)) + 1
            else:
                coh = int(rng.integers(1, 13))
            created = dt.datetime(2016, 3, 1) + dt.timedelta(days=int(rng.integers(0, 3700)))
            rows.append(dict(account_id=new_id(), klass=klass, lam=float(lam[i]), cohort0=coh,
                             created=created))
    acc = pd.DataFrame(rows).sort_values("account_id").reset_index(drop=True)
    # card issuer of the default saved card
    iss = []
    for k in acc.klass:
        if k == "XY":
            iss.append(P.ISSUER_X if rng.random() < 0.52 else P.ISSUER_Y)
        else:
            iss.append(P.OTHER_ISSUERS[int(rng.integers(0, len(P.OTHER_ISSUERS)))])
    acc["issuer0"] = iss
    # flag rebalance on 14 September: about 3 per cent move to a neighbouring cohort
    c1 = []
    for c in acc.cohort0:
        if rng.random() < 0.031:
            step_ = 1 if rng.random() < 0.5 else -1
            pos = (c - 1) % 4
            if pos == 0:
                step_ = 1
            elif pos == 3:
                step_ = -1
            c1.append(int(c + step_))
        else:
            c1.append(int(c))
    acc["cohort1"] = c1
    # club membership numbers: every member account, plus members who never use the Shop tab
    mno = {}
    used = set()

    def new_mno():
        while True:
            v = int(rng.integers(100_000, 389_999))
            if v not in used:
                used.add(v)
                return v
    for a, k in zip(acc.account_id, acc.klass):
        if k == "MEMBER":
            mno[a] = new_mno()
    others = acc.index[acc.klass == "OTHER"].to_numpy()
    for i in rng.choice(others, size=610, replace=False):
        mno[acc.account_id[i]] = new_mno()
    acc["member_no"] = [mno.get(a) for a in acc.account_id]
    return acc, used


# --------------------------------------------------------------------------- session skeleton

SRC_SI = (["direct", "organic_search", "email", "paid_search", "social", "affiliate", "referral"],
          [0.34, 0.22, 0.16, 0.12, 0.08, 0.04, 0.04])
SRC_NV = (["organic_search", "paid_search", "social", "affiliate", "referral", "direct"],
          [0.30, 0.28, 0.22, 0.08, 0.07, 0.05])
SRC_RG = (["direct", "organic_search", "paid_search", "social", "email", "affiliate", "referral"],
          [0.30, 0.25, 0.20, 0.12, 0.05, 0.04, 0.04])
DEV_WEB = (["mobile", "desktop", "tablet"], [0.58, 0.36, 0.06])


def _pick(rng, opts, n):
    return list(rng.choice(opts[0], size=n, p=opts[1]))


def make_skeleton(rng, acc):
    """One row per basket session with its hidden class; outcomes come later."""
    rows = []
    lam = {k: acc[acc.klass == k] for k in ("MEMBER", "CP4", "XY", "OTHER")}
    for w in P.WEEK_NAMES:
        vol = P.WEEK_VOL[w]
        rev = w in P.REVIEW
        floor = P.CLUB_LAUNCH if w == "W1" else None
        for k, base in P.SI_WEEKLY.items():
            sub = lam[k]
            p = (sub.lam / sub.lam.sum()).to_numpy()
            if k == "MEMBER" and rev:
                n_app = int(round(1600 * P.MEMBER_APP_SHARE[w]))
                n_web = 1600 - n_app
            else:
                n_app, n_web = 0, int(round(base * vol))
            for seg, n in (("SI", n_web), ("CLUB4", n_app)):
                if n == 0:
                    continue
                who = rng.choice(sub.account_id.to_numpy(), size=n, p=p)
                ts = sample_times(rng, n, w, floor if seg == "CLUB4" else None)
                rng.shuffle(who)
                for a, t in zip(who, ts):
                    rows.append(dict(t=t, week=w, seg=seg, acct=a, klass=k))
        for seg, base in (("NV", P.NV_WEEKLY), ("RG", P.RG_WEEKLY)):
            n = int(round(base * vol))
            for t in sample_times(rng, n, w):
                rows.append(dict(t=t, week=w, seg=seg, acct=None, klass=seg))
        if rev:
            n2 = {"W1": 512, "W2": 781, "W3": 908, "W4": 972}[w]
            for t in sample_times(rng, n2, w, floor):
                rows.append(dict(t=t, week=w, seg="CLUB2", acct=None, klass="CLUB2"))
    sk = pd.DataFrame(rows)
    n = len(sk)
    dev = np.empty(n, dtype=object)
    src = np.empty(n, dtype=object)
    for seg in sk.seg.unique():
        m = (sk.seg == seg).to_numpy()
        c = int(m.sum())
        if seg in ("CLUB4", "CLUB2"):
            dev[m] = "mobile"
            src[m] = "club_app"
        else:
            dev[m] = _pick(rng, DEV_WEB, c)
            src[m] = _pick(rng, {"SI": SRC_SI, "NV": SRC_NV, "RG": SRC_RG}[seg], c)
    sk["device"] = dev
    sk["source"] = src
    sk["signed_in"] = sk.seg == "SI"
    sk["new_visitor"] = sk.seg.isin(["NV", "CLUB4", "CLUB2"])
    sk["bot"] = ""
    return sk


def add_bots(rng, sk, acc):
    """The launch-day scraper replaying harvested Shop-tab links, and the credential-stuffing run."""
    rows = []
    t0 = dt.datetime(2026, 8, 31, 14, 5)
    for i in range(P.BOT_SCRAPE_SESSIONS):
        t = t0 + dt.timedelta(seconds=int(i * 136 + rng.integers(0, 90)))
        rows.append(dict(t=t, week=week_of(t), seg="BOTS", acct=None, klass="BOTS", device="mobile",
                         source="club_app", signed_in=False, new_visitor=True, bot="scrape"))
    kl = dict(zip(acc.account_id, acc.klass))
    pool = acc[acc.klass != "MEMBER"].account_id.to_numpy()
    victims = sorted(rng.choice(pool, size=P.BOT_STUFF_ACCOUNTS, replace=False))
    for a in victims:
        for _ in range(1 if rng.random() < 0.89 else 2):
            t = dt.datetime(2026, 9, 16, 1, 0) + dt.timedelta(seconds=int(rng.integers(0, 2 * 86400 + 60000)))
            rows.append(dict(t=t, week=week_of(t), seg="BOTI", acct=a,
                             klass=kl[a], device=_pick(rng, DEV_WEB, 1)[0],
                             source=_pick(rng, SRC_SI, 1)[0], signed_in=True, new_visitor=False, bot="stuff"))
    sk = pd.concat([sk, pd.DataFrame(rows)], ignore_index=True)
    sk = sk.sort_values(["t", "seg"], kind="mergesort").reset_index(drop=True)
    return sk, victims


# --------------------------------------------------------------------------- outcomes

def exit_probs(name, rate_single, mixed, addr_factor=1.0):
    c1, c2, c3, c4 = P.PROFILE[name]
    c5 = rate_single / (c1 * c2 * c3 * c4)
    c3 = c3 * addr_factor
    if mixed:
        c4 = c4 * P.MIXED_FACTOR
    reach = [1.0, c1, c1 * c2, c1 * c2 * c3, c1 * c2 * c3 * c4]
    cont = [c1, c2, c3, c4, c5]
    ex = np.array([reach[i] * (1 - cont[i]) for i in range(5)])
    conv = reach[4] * c5
    return ex, conv


def single_rate(rate, mixed_share=P.MIXED_SHARE):
    return rate / (1 - (1 - P.MIXED_FACTOR) * mixed_share)


def allocate_mixed(rng, sk):
    mixed = np.zeros(len(sk), dtype=bool)
    car = Carry()
    grp = np.where((sk.seg == "SI") & (sk.klass == "MEMBER"), "M", "O")
    other_si = (P.MIXED_SHARE * 16000 - P.MIXED_SHARE_MEMBER * 1600) / 14400
    for (seg, g_, w), g in sk.assign(grp=grp).groupby(["seg", "grp", "week"], sort=True):
        idx = g.index.to_numpy()
        if seg in ("SI", "NV", "RG"):
            share = P.MIXED_SHARE if seg != "SI" else (P.MIXED_SHARE_MEMBER if g_ == "M" else other_si)
            k = car.k(("mix", seg, g_), len(idx), share)
            mixed[rng.choice(idx, size=k, replace=False)] = True
        elif seg == "BOTS":
            mixed[idx] = True
    sk["mixed"] = mixed


def xy_switches(rng, sk, acc):
    """Accounts of the two issuers that moved their default card to another bank after being challenged."""
    iss = acc.set_index("account_id").issuer0
    si = sk[(sk.seg == "SI") & (sk.klass == "XY") & sk.week.isin(P.REVIEW)]
    first = {}
    for a, t in zip(si.acct, si.t):
        if t >= P.ISSUER_STOP[iss[a]] and a not in first:
            first[a] = t
    cand = sorted(a for a, t in first.items() if t < dt.datetime(2026, 9, 17))
    pick = sorted(rng.choice(cand, size=141, replace=False))
    sw = {}
    for a in pick:
        s = first[a] + dt.timedelta(minutes=int(rng.integers(180, 72 * 60)))
        sw[a] = min(s, dt.datetime(2026, 9, 19, 21, 0) + dt.timedelta(minutes=int(rng.integers(0, 90))))
    return sw


def cohort_asof(acc_row_c0, acc_row_c1, t):
    return acc_row_c1 if t >= P.REBALANCE_AT else acc_row_c0


def allocate_outcomes(rng, sk, acc, switches):
    """Static cells by carry allocation; the address-check pool session by session."""
    A = acc.set_index("account_id")
    n = len(sk)
    step = np.array(["basket"] * n, dtype=object)
    order = np.zeros(n, dtype=bool)
    p3 = np.zeros(n, dtype=bool)
    p3aff = np.zeros(n, dtype=bool)
    fam = np.empty(n, dtype=object)
    fam_mx = np.zeros(n, dtype=bool)
    for i, (seg, w, a, k, t, mx) in enumerate(zip(sk.seg, sk.week, sk.acct, sk.klass, sk.t, sk.mixed)):
        if seg in ("BOTS", "BOTI"):
            fam[i] = None
            if seg == "BOTI" and k == "XY":
                p3[i] = (a not in switches) or t < switches[a]
            continue
        rev = w in P.REVIEW
        if seg == "SI":
            if k == "XY":
                on_xy = (a not in switches) or t < switches[a]
                p3[i] = on_xy
                if rev and on_xy and t >= P.ISSUER_STOP[A.issuer0[a]]:
                    p3aff[i] = True
                    fam[i] = ("P3", mx)
                    continue
            if k == "CP4" and rev:
                fam[i] = "DYN"
                continue
            fam[i] = (k, mx, "rev" if rev else "base")
        elif seg in ("NV", "RG"):
            fam[i] = (seg, mx)
        elif seg == "CLUB4":
            fam[i] = ("P4", False)
        elif seg == "CLUB2":
            fam[i] = ("P2", False)
    # appearance of each account in its population, known from the skeleton before any outcome
    rv = sk[sk.week.isin(P.REVIEW)]
    app = {}
    for seg, a, k, t, w in zip(rv.seg, rv.acct, rv.klass, rv.t, rv.week):
        if a is None or seg == "BOTI":
            continue
        if k == "MEMBER" and seg == "CLUB4":
            app.setdefault(a, set()).update({"win", "w4"} if w == "W4" else {"win"})
        elif k == "XY" and seg == "SI" and ((a not in switches) or t < switches[a]):
            app.setdefault(a, set()).update({"win", "w4"} if w == "W4" else {"win"})
        elif k == "CP4" and seg == "SI":
            coh = cohort_asof(A.cohort0[a], A.cohort1[a], t)
            if t >= P.COHORT_LIVE[coh]:
                app.setdefault(a, set()).add("win")
    for i, (seg, w, a, k) in enumerate(zip(sk.seg, sk.week, sk.acct, sk.klass)):
        f = fam[i]
        if isinstance(f, tuple) and len(f) == 3 and f[2] == "base":
            ap = app.get(a, set())
            fam[i] = (k, "B0") if w == "B0" else (k, "base", "win" in ap, "w4" in ap)
            fam_mx[i] = f[1]
        elif isinstance(f, tuple) and len(f) == 3 and f[2] == "rev":
            fam[i] = (k, "rev")
            fam_mx[i] = f[1]
        elif isinstance(f, tuple) and len(f) == 2:
            fam[i] = (f[0], "B0" if w == "B0" else ("base" if w in P.BASE else "rev"))
            fam_mx[i] = f[1]
    # review-week signed-in cells are allocated per flag cohort as of the session
    for i, (seg, w, a, t) in enumerate(zip(sk.seg, sk.week, sk.acct, sk.t)):
        if seg == "SI" and w in P.REVIEW and isinstance(fam[i], tuple):
            fam[i] = fam[i] + (int(cohort_asof(A.cohort0[a], A.cohort1[a], t)),)
    rates = {"P3": ("P3", P.R_P3), "P4": ("P4", P.R_P4), "P2": ("P2", P.R_P2), "NV": ("NV", P.R_NV),
             "RG": ("RG", P.R_RG)}
    car = Carry()
    sk["fam"] = fam
    keyed = sk[sk.fam.notna() & (sk.fam != "DYN")]
    groups = {}
    for i, f, w in zip(keyed.index, keyed.fam, keyed.week):
        groups.setdefault((f, bool(fam_mx[i]), w), []).append(i)
    fams = {}
    for (f, mx, w), idx in groups.items():
        fams.setdefault((f, w), {})[mx] = np.array(idx)
    for (f, w) in sorted(fams, key=lambda x: (P.WEEK_NAMES.index(x[1]), str(x[0]))):
        cells = fams[(f, w)]
        head = f[0]
        prof, r = rates.get(head, ("SI", P.R_SI))
        rs = single_rate(r) if prof in ("SI", "P3", "NV", "RG") else r
        ns = len(cells.get(False, []))
        nm = len(cells.get(True, []))
        k = car.k(f, ns + nm, r)
        km = car.kx((f, "mx"), k * (P.MIXED_FACTOR * nm) / (ns + P.MIXED_FACTOR * nm), nm)
        for mx, kk in ((False, k - km), (True, km)):
            if mx not in cells:
                continue
            idx = cells[mx]
            kk = min(kk, len(idx))
            perm = rng.permutation(idx)
            conv, rest = perm[:kk], perm[kk:]
            order[conv] = True
            step[conv] = "confirmation"
            ex, _ = exit_probs(prof, rs, mx)
            ex = ex / ex.sum()
            pos = 0
            for j, st in enumerate(P.STEPS[:5]):
                c = car.kx((f, mx, st), len(rest) * ex[j], len(rest) - pos) if j < 4 else len(rest) - pos
                step[rest[pos:pos + c]] = st
                pos += c
    sk["step"] = step
    sk["order"] = order
    sk["p3"] = p3
    sk["p3aff"] = p3aff
    return sk


def simulate_cp4(rng, sk, acc):
    """Address-check pool in the review weeks: a session is exposed when the account's saved default
    address is four-digit-postcode-only at its start and its flag cohort is live; exposure ends when
    the account re-saves the address."""
    c0 = dict(zip(acc.account_id, acc.cohort0))
    c1 = dict(zip(acc.account_id, acc.cohort1))
    rs_single = single_rate(P.R_SI)
    resave = {}
    p1 = np.zeros(len(sk), dtype=bool)
    trig = np.zeros(len(sk), dtype=bool)
    step = sk.step.to_numpy().copy()
    order = sk.order.to_numpy().copy()
    cp4_state = {a: True for a in acc.account_id[acc.klass == "CP4"]}
    lr_exp, lr_got = {}, {}
    w4_sessions = {}
    for a_, t_, w_, sg_ in zip(sk.acct, sk.t, sk.week, sk.seg):
        if w_ == "W4" and sg_ == "SI" and a_ in cp4_state:
            w4_sessions.setdefault(a_, []).append(t_)
    m = ((sk.klass == "CP4") & sk.week.isin(P.REVIEW) & sk.seg.isin(["SI", "BOTI"])).to_numpy()
    acct, tt, wk, mxd, sg = (sk.acct.to_numpy(), sk.t.to_numpy(), sk.week.to_numpy(), sk.mixed.to_numpy(),
                             sk.seg.to_numpy())
    for i in np.flatnonzero(m):
        a, t, w, mx, seg = acct[i], tt[i], wk[i], mxd[i], sg[i]
        t = pd.Timestamp(t).to_pydatetime()
        if a in resave and resave[a] <= t:
            cp4_state[a] = False
        coh = cohort_asof(c0[a], c1[a], t)
        live = t >= P.COHORT_LIVE[coh]
        if cp4_state[a] and live:
            p1[i] = True
        if seg == "BOTI":
            continue
        ex, conv = exit_probs("SI", rs_single, mx, addr_factor=(0.208 if p1[i] else 1.0))
        probs = np.append(ex, conv)
        probs = probs / probs.sum()
        key = (coh, w, bool(p1[i]), bool(mx))
        e = lr_exp.setdefault(key, np.zeros(6))
        gt = lr_got.setdefault(key, np.zeros(6))
        e += probs
        j = int(np.argmax(e - gt))
        gt[j] += 1
        s_ = P.STEPS[j]
        step[i] = s_
        order[i] = s_ == "confirmation"
        if p1[i] and a not in resave:
            reached = P.STEPS.index(s_) >= 2
            if rng.random() < (0.9 if reached else 0.82):
                trig[i] = True
                for _try in range(40):
                    if w != "W4" and rng.random() < 0.08:
                        d = dt.timedelta(minutes=int(rng.integers(12, 56)))
                    else:
                        d = dt.timedelta(minutes=int(rng.integers(130, 48 * 60)))
                    r_ = t + d
                    if not any(r_ - dt.timedelta(hours=2) <= x < r_ for x in w4_sessions.get(a, [])):
                        break
                else:
                    raise AssertionError(("no clear re-save time", a, t))
                resave[a] = r_
    sk["step"] = step
    sk["order"] = order
    sk["p1"] = p1
    sk["p1_trigger"] = trig
    return sk, resave


# --------------------------------------------------------------------------- catalogue and baskets

PREORDER = {  # sku: (pre-order from, in stock from or None)
    "MON-K3-2627": (dt.datetime(2026, 8, 31, 0, 0), dt.datetime(2026, 9, 20, 8, 0)),
    "GAM-CE-ORION": (dt.datetime(2026, 6, 18, 9, 0), None),
    "MUS-VBX-LUMEN": (dt.datetime(2026, 7, 9, 9, 0), None),
    "MON-JKT-2627": (dt.datetime(2026, 9, 15, 9, 0), None),
    "MON-K1-2627": (dt.datetime(2026, 6, 1, 9, 0), dt.datetime(2026, 7, 21, 8, 0)),
    "MON-K2-2627": (dt.datetime(2026, 6, 1, 9, 0), dt.datetime(2026, 7, 21, 8, 0)),
}


def make_catalogue(rng):
    rows = [("MON-K1-2627", "CD Monteralto home shirt 26/27", "football"),
            ("MON-K2-2627", "CD Monteralto away shirt 26/27", "football"),
            ("MON-K3-2627", "CD Monteralto third shirt 26/27", "football"),
            ("MON-GK-2627", "CD Monteralto goalkeeper shirt 26/27", "football"),
            ("MON-JKT-2627", "CD Monteralto winter jacket 26/27", "football"),
            ("MON-TRN-2627", "CD Monteralto training top 26/27", "football"),
            ("MON-SHO-2627", "CD Monteralto home shorts 26/27", "football"),
            ("MON-KID-K1", "CD Monteralto home kit, junior", "football"),
            ("GAM-CE-ORION", "Orion Drift collector's edition", "gaming"),
            ("MUS-VBX-LUMEN", "Lumen Avenue tour vinyl box", "music"),
            ("GFT-25", "Gift card 25 EUR", "gift_card"), ("GFT-50", "Gift card 50 EUR", "gift_card"),
            ("GFT-100", "Gift card 100 EUR", "gift_card")]
    words_f = ["scarf", "cap", "beanie", "mug", "flag", "keyring", "poster", "socks", "backpack", "pin set"]
    for i, w in enumerate(words_f):
        rows.append((f"MON-ACC-{i + 11:02d}", f"CD Monteralto {w}", "football"))
    bands = ["Lumen Avenue", "Os Marés", "Cinza Norte", "Paper Lanterns", "Rio Alto", "Velha Guarda"]
    for i, b in enumerate(bands):
        rows.append((f"MUS-TEE-{i + 21:02d}", f"{b} tour t-shirt", "music"))
        rows.append((f"MUS-LP-{i + 21:02d}", f"{b} vinyl LP", "music"))
    games = ["Orion Drift", "Pixel Harbour", "Iron Tide", "Neon Kart", "Ghost Relay"]
    for i, g in enumerate(games):
        rows.append((f"GAM-HOO-{i + 31:02d}", f"{g} hoodie", "gaming"))
        rows.append((f"GAM-FIG-{i + 31:02d}", f"{g} figure", "gaming"))
    for i, cl in enumerate(["Atlético Sardoal", "União de Vilarinho", "SC Pedra Branca"]):
        rows.append((f"FUT-{i + 41:02d}-H", f"{cl} home shirt 26/27", "football"))
    cat = pd.DataFrame(rows, columns=["sku", "product_name", "category"])
    hist = []
    for s in cat.sku:
        if s in PREORDER:
            a, b = PREORDER[s]
            hist.append((s, "pre_order", a))
            if b is not None:
                hist.append((s, "in_stock", b))
        else:
            hist.append((s, "in_stock", dt.datetime(2025, 7, 1) + dt.timedelta(days=int(rng.integers(0, 330)))))
    h = pd.DataFrame(hist, columns=["sku", "status", "valid_from"])
    return cat, h


def preorder_at(sku, t):
    if sku not in PREORDER:
        return False
    a, b = PREORDER[sku]
    return t >= a and (b is None or t < b)


def make_baskets(rng, sk, cat):
    instock_web = [s for s in cat.sku if s not in PREORDER or s in ("MON-K1-2627", "MON-K2-2627")]
    instock_web = [s for s in instock_web if not s.startswith("GFT")]
    club_kits = ["MON-K1-2627", "MON-K2-2627", "MON-GK-2627", "MON-TRN-2627", "MON-SHO-2627", "MON-KID-K1"]
    po_all = ["MON-K3-2627", "GAM-CE-ORION", "MUS-VBX-LUMEN", "MON-JKT-2627"]
    po_w = {"MON-K3-2627": 0.55, "GAM-CE-ORION": 0.2, "MUS-VBX-LUMEN": 0.15, "MON-JKT-2627": 0.1}
    out = []
    for seg, t, mx, bot in zip(sk.seg, sk.t, sk.mixed, sk.bot):
        if bot == "scrape":
            out.append("MON-K3-2627;MON-K1-2627")
            continue
        if bot == "stuff":
            out.append(";".join(sorted(set(rng.choice(["GFT-25", "GFT-50", "GFT-100"],
                                                        size=int(rng.integers(1, 3)))))))
            continue
        avail_po = [s for s in po_all if preorder_at(s, t)]
        if seg in ("CLUB4", "CLUB2"):
            pool = club_kits + (["MON-K3-2627"] if not preorder_at("MON-K3-2627", t) else [])
            n = 1 if rng.random() < 0.7 else 2
            out.append(";".join(sorted(set(rng.choice(pool, size=n)))))
            continue
        n_in = 1 + int(rng.random() < 0.38) + int(rng.random() < 0.12)
        items = list(rng.choice(instock_web, size=n_in))
        if rng.random() < 0.015:
            items.append(str(rng.choice(["GFT-25", "GFT-50", "GFT-100"])))
        if mx:
            w = np.array([po_w[s] for s in avail_po])
            items.append(str(rng.choice(avail_po, p=w / w.sum())))
        elif rng.random() < 0.02:
            items = [str(rng.choice(avail_po))]
        out.append(";".join(sorted(set(items))))
    sk["basket"] = out


def is_mixed_asof(basket, t, current=False):
    skus = basket.split(";")
    if current:
        po = [s for s in skus if s in PREORDER and PREORDER[s][1] is None]
    else:
        po = [s for s in skus if preorder_at(s, t)]
    return 0 < len(po) < len(skus)


# --------------------------------------------------------------------------- club side

B32 = np.array(list("ABCDEFGHJKLMNPQRSTUVWXYZ23456789"))


def token(rng):
    return "".join(rng.choice(B32, size=20))


def make_tokens(rng, sk, acc, used_mno):
    """Every Shop-tab tap the club issued a members'-price token for, with the member number."""
    mno = dict(zip(acc.account_id, acc.member_no))
    nonacct = []
    while len(nonacct) < 2700:
        v = int(rng.integers(100_000, 389_999))
        if v not in used_mno:
            used_mno.add(v)
            nonacct.append(v)
    nonacct = np.array(sorted(nonacct))
    p2w = rng.gamma(0.8, 1.0, size=len(nonacct))
    p2w = p2w / p2w.sum()
    tok = np.empty(len(sk), dtype=object)
    member = np.empty(len(sk), dtype=object)
    issued = []
    seen = set()

    def new_tok():
        while True:
            x = token(rng)
            if x not in seen:
                seen.add(x)
                return x
    for i in np.flatnonzero(sk.seg.isin(["CLUB4", "CLUB2"]).to_numpy()):
        m = mno[sk.acct[i]] if sk.seg[i] == "CLUB4" else int(rng.choice(nonacct, p=p2w))
        x = new_tok()
        tok[i], member[i] = x, m
        issued.append((x, m, sk.t[i] - dt.timedelta(seconds=int(rng.integers(2, 25)))))
    # taps that did not reach a basket
    members_app = acc[acc.klass == "MEMBER"].member_no.to_numpy()
    for w, n4, n2 in (("W1", 1050, 760), ("W2", 1620, 1150), ("W3", 1930, 1330), ("W4", 2150, 1420)):
        ts = sample_times(rng, n4 + n2, w, P.CLUB_LAUNCH if w == "W1" else None)
        who = list(rng.choice(members_app, size=n4)) + list(rng.choice(nonacct, size=n2, p=p2w))
        rng.shuffle(who)
        for m, t in zip(who, ts):
            issued.append((new_tok(), int(m), t))
    sk["token"] = tok
    sk["member_no"] = member
    # the scraper replayed links harvested on launch day
    day1 = sk[(sk.seg.isin(["CLUB4", "CLUB2"])) & (sk.t < dt.datetime(2026, 8, 31, 14, 0))]
    h4 = list(day1[day1.seg == "CLUB4"].index[:11])
    h2 = list(day1[day1.seg == "CLUB2"].index[:3])
    harvested = [sk.token[i] for i in h4 + h2]
    bots = np.flatnonzero((sk.bot == "scrape").to_numpy())
    for j, i in enumerate(bots):
        src = (h4 + h2)[j % 14] if j < 14 * 3 else (h4 + h2)[int(rng.integers(0, 14))]
        sk.at[i, "token"] = sk.token[src]
        sk.at[i, "member_no"] = sk.member_no[src]
    tk = pd.DataFrame(issued, columns=["token", "member_no", "issued_at"]).sort_values(
        ["issued_at", "token"]).reset_index(drop=True)
    return tk, harvested, nonacct


def make_profiles(rng, acc):
    rows = []
    for a, k, m, c in zip(acc.account_id, acc.klass, acc.member_no, acc.created):
        if k == "MEMBER" or m is not None and not pd.isna(m) or rng.random() < 0.55:
            enr = max(c, dt.datetime(2019, 4, 1)) + dt.timedelta(days=int(rng.integers(0, 400)))
            enr = min(enr, dt.datetime(2026, 7, 1))
            tier = rng.choice(["bronze", "prata", "ouro"], p=[0.62, 0.28, 0.10])
            rows.append(dict(account_id=a, enrolled_on=enr.date().isoformat(), tier=str(tier),
                             points_balance=int(rng.gamma(1.2, 380)),
                             club_member_no=(int(m) if m is not None and not pd.isna(m) else None),
                             marketing_opt_in=bool(rng.random() < 0.58)))
    return pd.DataFrame(rows)


LOCALITIES = [("Lisboa", "11"), ("Lisboa", "12"), ("Lisboa", "17"), ("Porto", "40"), ("Porto", "41"),
              ("Vila Nova de Gaia", "44"), ("Braga", "47"), ("Coimbra", "30"), ("Aveiro", "38"),
              ("Leiria", "24"), ("Setúbal", "29"), ("Faro", "80"), ("Viseu", "35"), ("Évora", "70"),
              ("Guimarães", "48"), ("Matosinhos", "44"), ("Almada", "28"), ("Amadora", "27"),
              ("Funchal", "90"), ("Ponta Delgada", "95")]


def fp16(rng):
    return "".join(rng.choice(list("0123456789abcdef"), size=16))


def make_addresses(rng, acc, sk, resave):
    """Default delivery address per account and its change history. Change times are UTC."""
    rows = []
    fp_now, fp_full = {}, {}
    for a, k, c in zip(acc.account_id, acc.klass, acc.created):
        loc, pre = LOCALITIES[int(rng.integers(0, len(LOCALITIES)))]
        cp4 = f"{pre}{int(rng.integers(0, 100)):02d}"
        full = f"{cp4}-{int(rng.integers(1, 999)):03d}"
        aid = "AD" + fp16(rng)[:10]
        f_full = fp16(rng)
        fp_full[a] = (aid, full, loc, f_full)
        if k == "CP4":
            f0, pc = fp16(rng), cp4
        else:
            f0, pc = f_full, full
        fp_now[a] = f0
        rows.append(dict(account_id=a, address_id=aid, event="created", is_default=True, postcode=pc,
                         locality=loc, address_fp=f0, changed_at=c + dt.timedelta(hours=int(rng.integers(8, 20)))))
        if rng.random() < 0.22:
            l2, p2_ = LOCALITIES[int(rng.integers(0, len(LOCALITIES)))]
            rows.append(dict(account_id=a, address_id="AD" + fp16(rng)[:10], event="added", is_default=False,
                             postcode=f"{p2_}{int(rng.integers(0, 100)):02d}-{int(rng.integers(1, 999)):03d}",
                             locality=l2, address_fp=fp16(rng),
                             changed_at=min(c + dt.timedelta(days=int(rng.integers(30, 900))),
                                            dt.datetime(2026, 7, 20, 12, 0))))
    for a, r in sorted(resave.items()):
        if r >= P.END:
            continue
        aid, full, loc, f_full = fp_full[a]
        rows.append(dict(account_id=a, address_id=aid, event="updated", is_default=True, postcode=full,
                         locality=loc, address_fp=f_full, changed_at=r - dt.timedelta(hours=1)))
    # ordinary moves by other customers, kept two hours clear of their own sessions
    sess = sk[sk.acct.notna()].groupby("acct").t.apply(list).to_dict()
    oth = acc[acc.klass == "OTHER"].account_id.to_numpy()
    moved = 0
    for a in rng.choice(oth, size=900, replace=False):
        r = dt.datetime(2026, 7, 27) + dt.timedelta(seconds=int(rng.integers(0, 62 * 86400)))
        if any(abs((s - r).total_seconds()) < 3 * 3600 for s in sess.get(a, [])):
            continue
        loc, pre = LOCALITIES[int(rng.integers(0, len(LOCALITIES)))]
        aid = fp_full[a][0]
        newfp = fp16(rng)
        rows.append(dict(account_id=a, address_id=aid, event="updated", is_default=True,
                         postcode=f"{pre}{int(rng.integers(0, 100)):02d}-{int(rng.integers(1, 999)):03d}",
                         locality=loc, address_fp=newfp, changed_at=r - dt.timedelta(hours=1)))
        fp_full[a] = (aid, None, loc, newfp)
        moved += 1
        if moved >= 610:
            break
    ab = pd.DataFrame(rows).sort_values(["changed_at", "account_id"]).reset_index(drop=True)
    return ab


BINS = {}


def make_cards(rng, acc, switches):
    """Saved cards: snapshot at extract and the change history over the extract window."""
    issuers = [P.ISSUER_X, P.ISSUER_Y] + P.OTHER_ISSUERS
    for j, i in enumerate(issuers):
        BINS[i] = [f"{4 if q % 2 == 0 else 5}{int(rng.integers(10000, 99999)):05d}" for q in range(3)]
    snap, chg = [], []
    default_card = {}
    for a, iss, c in zip(acc.account_id, acc.issuer0, acc.created):
        cid = "pm_" + fp16(rng)[:14]
        added = max(c, dt.datetime(2021, 1, 1)) + dt.timedelta(days=int(rng.integers(0, 600)))
        added = min(added, dt.datetime(2026, 6, 30))
        b = BINS[iss][int(rng.integers(0, 3))]
        snap.append(dict(account_id=a, card_id=cid, card_fp=fp16(rng), brand="visa" if b[0] == "4" else "mastercard",
                         issuer=iss, bin6=b, last4=f"{int(rng.integers(0, 10000)):04d}", added_at=added,
                         is_default=True))
        default_card[a] = len(snap) - 1
        if rng.random() < 0.3:
            i2 = issuers[2 + int(rng.integers(0, len(P.OTHER_ISSUERS)))]
            b2 = BINS[i2][int(rng.integers(0, 3))]
            when = dt.datetime(2026, 7, 27) + dt.timedelta(seconds=int(rng.integers(0, 62 * 86400)))
            old = rng.random() < 0.75
            ad = added + dt.timedelta(days=30) if old else when
            snap.append(dict(account_id=a, card_id="pm_" + fp16(rng)[:14], card_fp=fp16(rng),
                             brand="visa" if b2[0] == "4" else "mastercard", issuer=i2, bin6=b2,
                             last4=f"{int(rng.integers(0, 10000)):04d}", added_at=ad, is_default=False))
            if not old:
                chg.append(dict(account_id=a, card_id=snap[-1]["card_id"], event="added", at=ad))
    for a, s in sorted(switches.items()):
        i2 = P.OTHER_ISSUERS[int(rng.integers(0, len(P.OTHER_ISSUERS)))]
        b2 = BINS[i2][int(rng.integers(0, 3))]
        snap[default_card[a]]["is_default"] = False
        snap.append(dict(account_id=a, card_id="pm_" + fp16(rng)[:14], card_fp=fp16(rng),
                         brand="visa" if b2[0] == "4" else "mastercard", issuer=i2, bin6=b2,
                         last4=f"{int(rng.integers(0, 10000)):04d}", added_at=s, is_default=True))
        chg.append(dict(account_id=a, card_id=snap[-1]["card_id"], event="added", at=s))
        chg.append(dict(account_id=a, card_id=snap[-1]["card_id"], event="set_default",
                        at=s + dt.timedelta(seconds=int(rng.integers(4, 40)))))
    cards = pd.DataFrame(snap)
    ch = pd.DataFrame(chg).sort_values(["at", "account_id"]).reset_index(drop=True)
    return cards, ch


def make_flags(acc):
    sched = [{"cohort": c, "enabled_at": P.COHORT_LIVE[c].strftime("%Y-%m-%dT%H:%M:%S+01:00")}
             for c in range(1, 13)]
    current = [{"account_id": a, "cohort": int(c1)} for a, c1 in zip(acc.account_id, acc.cohort1)]
    log = [{"account_id": a, "from_cohort": int(c0), "to_cohort": int(c1),
            "moved_at": P.REBALANCE_AT.strftime("%Y-%m-%dT%H:%M:%S+01:00")}
           for a, c0, c1 in zip(acc.account_id, acc.cohort0, acc.cohort1) if c0 != c1]
    return {"flag_key": "checkout.address.full_postcode", "scope": "signed_in_sessions",
            "notes": "A session's cohort is the latest assignment at or before the session. The flag applies to "
                     "signed-in sessions.",
            "rollout": sched, "assignments": current, "assignment_moves": log}


# --------------------------------------------------------------------------- orders, payments, ids

AOV_BASE = {"MEMBER": 71.0, "CP4": 57.5, "XY": 64.0, "OTHER": 61.0, "NV": 48.5, "RG": 54.0, "P4APP": 63.0,
            "P2APP": 52.0}


def aov_key(seg, klass, mixed):
    if seg == "CLUB4":
        return "P4APP"
    if seg == "CLUB2":
        return "P2APP"
    if seg == "NV":
        return "NV"
    if klass in ("MEMBER", "CP4", "XY"):
        return klass
    return "MIXED" if mixed else None


def make_orders(rng, sk):
    """Net order totals before tuning scales, and the refund corrections of the 17 August re-export."""
    conv = np.flatnonzero(sk.order.to_numpy())
    ids = 2_604_117 + np.arange(len(conv)) * 3 + rng.integers(0, 3, size=len(conv))
    oid = np.empty(len(sk), dtype=object)
    oid[conv] = [f"VM{x}" for x in ids]
    sk["order_id"] = oid
    base = np.zeros(len(sk))
    for i in conv:
        k = "P4APP" if sk.seg[i] == "CLUB4" else "P2APP" if sk.seg[i] == "CLUB2" else (
            sk.klass[i] if sk.seg[i] == "SI" else sk.seg[i])
        v = AOV_BASE[k] * float(np.exp(rng.normal(-0.08, 0.4)))
        if sk.mixed[i]:
            v += 38.0 * float(np.exp(rng.normal(-0.05, 0.3)))
        base[i] = round(max(v, 9.9), 2)
    sk["amount_base"] = base
    cand = [i for i in conv if sk.t[i] < dt.datetime(2026, 8, 16)]
    corr = sorted(rng.choice(cand, size=412, replace=False))
    refund = {int(i): float(rng.uniform(0.12, 0.45)) for i in corr}
    return refund


OUTCOME_OK = {"cof": (["I", "Y", "CH"], [0.60, 0.30, 0.10]), "typed": (["Y", "CH"], [0.36, 0.64]),
              "p3": (["Y", "CH"], [0.08, 0.92])}
OUTCOME_FAIL = {"cof": (["Y", "CH", "N", "U"], [0.35, 0.45, 0.12, 0.08]),
                "typed": (["Y", "CH", "N", "U"], [0.20, 0.62, 0.12, 0.06]),
                "p3": (["CH", "N", "U"], [0.92, 0.05, 0.03])}


def make_attempts(rng, sk, cards, member_card_fp, p2_card_fp):
    """Card payment attempts (3-D Secure authentication) for every review-week session that reached
    payment. One attempt is one attempt_ref; re-sent messages are added at assembly."""
    cd = cards[cards.is_default | cards.account_id.duplicated(keep=False)]
    issuer_of = dict(zip(cards.card_fp, cards.issuer))
    bin_of = dict(zip(cards.card_fp, cards.bin6))
    rows = []
    allis = [P.ISSUER_X, P.ISSUER_Y] + P.OTHER_ISSUERS
    m = (sk.week.isin(P.REVIEW) & sk.step.isin(["payment", "confirmation"]) & (sk.bot == "")).to_numpy()
    for i in np.flatnonzero(m):
        seg = sk.seg[i]
        if seg == "SI":
            fp = sk.card_fp[i]
            ctx = "p3" if sk.p3aff[i] else "cof"
        elif seg == "CLUB4":
            fp, ctx = member_card_fp[sk.acct[i]], "typed"
        elif seg == "CLUB2":
            fp, ctx = p2_card_fp[sk.member_no[i]], "typed"
        else:
            fp, ctx = fp16(rng), "typed"
        if fp not in issuer_of:
            iss = allis[int(rng.choice(len(allis), p=[0.06, 0.06] + [0.88 / len(P.OTHER_ISSUERS)] * len(P.OTHER_ISSUERS)))]
            issuer_of[fp] = iss
            bin_of[fp] = BINS[iss][int(rng.integers(0, 3))]
        iss = issuer_of[fp]
        ok = bool(sk.order[i])
        n_fail = (1 if rng.random() < 0.07 else 0) if ok else (2 if rng.random() < 0.18 else 1)
        seq = []
        for _ in range(n_fail):
            o = rng.choice(OUTCOME_FAIL[ctx][0], p=OUTCOME_FAIL[ctx][1])
            seq.append((str(o), "N"))
        if ok:
            seq.append((str(rng.choice(OUTCOME_OK[ctx][0], p=OUTCOME_OK[ctx][1])), "Y"))
        off = int(rng.integers(240, 900))
        for j, (o, au) in enumerate(seq):
            if o == "CH":
                o = "D" if iss == P.ISSUER_X else "C"
            rows.append(dict(sidx=int(i), attempt_ref="PA" + fp16(rng)[:12], seq=j, outcome=o, authorised=au,
                             card_fp=fp, bin6=bin_of[fp], issuer=iss,
                             sent_at=sk.t[i] + dt.timedelta(seconds=off + j * int(rng.integers(50, 160))),
                             amount_eur=round(float(sk.amount_base[i]) * (1 + P.VAT) if ok else
                                              float(60 * np.exp(rng.normal(0, 0.4))), 2)))
    return pd.DataFrame(rows)


def make_ids(rng, sk):
    seen = set()
    out = []
    for _ in range(len(sk)):
        while True:
            x = fp16(rng)[:12]
            if x not in seen:
                seen.add(x)
                out.append(x)
                break
    sk["session_id"] = out


CAMPAIGNS = ["regresso_aulas", "nova_epoca", "vinil_setembro", "gaming_semana"]
AFFS = ["descontos_pt", "ofertasja", "cupao"]


def landing(rng, seg, src, basket, tok):
    first = basket.split(";")[0]
    cat = {"MON": "futebol/cd-monteralto", "FUT": "futebol/clubes", "MUS": "musica", "GAM": "gaming",
           "GFT": "cartoes-oferta"}[first.split("-")[0]]
    path = f"/{cat}/{first.lower()}"
    if src == "club_app":
        return (f"https://{P.STORE_DOMAIN}/socios{path}?mpt={tok}"
                f"&utm_source=cdmonteralto&utm_medium=app&utm_campaign=separador_loja")
    if src == "paid_search":
        return f"https://{P.STORE_DOMAIN}{path}?gclid={fp16(rng)}{fp16(rng)[:6]}"
    if src == "email":
        return (f"https://{P.STORE_DOMAIN}{path}?utm_source=newsletter&utm_medium=email"
                f"&utm_campaign={CAMPAIGNS[int(rng.integers(0, 4))]}")
    if src == "social":
        return f"https://{P.STORE_DOMAIN}{path}?utm_source={rng.choice(['instagram', 'tiktok', 'facebook'])}&utm_medium=social"
    if src == "affiliate":
        return f"https://{P.STORE_DOMAIN}{path}?utm_source={AFFS[int(rng.integers(0, 3))]}&utm_medium=affiliate"
    return f"https://{P.STORE_DOMAIN}{path}"


def make_edge(rng, sk):
    rows = []
    for sid, t, b in zip(sk.session_id, sk.t, sk.bot):
        if b == "scrape":
            rows.append((sid, t + dt.timedelta(seconds=int(rng.integers(3, 40))), "R-1043", "automated"))
        elif b == "stuff":
            rows.append((sid, t + dt.timedelta(seconds=int(rng.integers(3, 40))), "R-2210", "automated"))
    seen = set(sk.session_id)
    for w in P.WEEK_NAMES:
        for t in sample_times(rng, int(rng.integers(330, 420)), w):
            while True:
                x = fp16(rng)[:12]
                if x not in seen:
                    seen.add(x)
                    break
            rows.append((x, t, str(rng.choice(["R-0310", "R-0412", "R-0517"], p=[0.5, 0.35, 0.15])), "automated"))
    e = pd.DataFrame(rows, columns=["session_id", "first_seen", "rule_id", "verdict"])
    return e.sort_values(["first_seen", "session_id"]).reset_index(drop=True)


# --------------------------------------------------------------------------- member links

PROMO_CODES = [  # code, first day, last day, redemptions, guest share, discount (low, high)
    ("BEMVINDO10", dt.datetime(2025, 7, 1), dt.datetime(2026, 6, 30), 2460, 0.62, (3.9, 12.5)),
    ("KAIJU15", dt.datetime(2025, 11, 3), dt.datetime(2025, 11, 30), 690, 0.81, (5.2, 17.9)),
    ("BLACKFRIDAY25", dt.datetime(2025, 11, 27), dt.datetime(2025, 12, 1), 1385, 0.31, (6.0, 31.0)),
    ("NATAL25", dt.datetime(2025, 12, 1), dt.datetime(2025, 12, 24), 905, 0.27, (4.0, 14.0)),
    ("SALDOS26", dt.datetime(2026, 1, 7), dt.datetime(2026, 2, 28), 1110, 0.35, (5.0, 22.0)),
]


def _season_t(rng, lo, hi):
    span = (hi - lo).total_seconds()
    t = lo + dt.timedelta(seconds=float(rng.uniform(0, span)))
    return t.replace(microsecond=0)


def make_member_links(T):
    """Where each member's link to a store account is stored, on a random stream of its own: the
    loyalty profile's member number for some members, last season's members' code (SOCIO plus the
    seven-digit member number) redeemed on the account for the rest, and both for many. The promotions
    extract also carries every other code of the 2025/26 season, guests included."""
    rng = np.random.default_rng(P.LINK_SEED)
    acc = T["acc"]
    mem = acc[acc.member_no.notna()]
    keep, socio = {}, []
    for a, k, m in zip(mem.account_id, mem.klass, mem.member_no):
        kp = bool(rng.random() < P.PROFILE_KEEP.get(k, 0.45))
        keep[a] = kp
        n = int(rng.poisson(0.6)) if kp else 1 + int(rng.poisson(0.8))
        for _ in range(n):
            u = rng.random()
            if u < 0.45:
                t = _season_t(rng, P.SEASON_START, dt.datetime(2025, 9, 30, 23, 0))
            elif u < 0.70:
                t = _season_t(rng, dt.datetime(2025, 11, 15), dt.datetime(2025, 12, 24, 22, 0))
            else:
                t = _season_t(rng, P.SEASON_START, P.SEASON_END)
            kits = 1 if rng.random() < 0.83 else 2
            price = float(rng.choice([64.99, 69.99, 74.99, 79.99, 89.99]))
            socio.append((t, a, f"SOCIO{int(m):07d}", round(0.10 * price * kits, 2)))
    prof = T["profiles"].copy()
    prof["club_member_no"] = [m if (pd.notna(m) and keep.get(a, False)) else None
                              for a, m in zip(prof.account_id, prof.club_member_no)]
    T["profiles"] = prof
    rows = list(socio)
    allacc = acc.account_id.to_numpy()
    for code, lo, hi, n, guest, (dlo, dhi) in PROMO_CODES:
        for _ in range(n):
            a = None if rng.random() < guest else str(rng.choice(allacc))
            rows.append((_season_t(rng, lo, hi), a, code, round(float(rng.uniform(dlo, dhi)), 2)))
    for mth in range(12):
        y, mo = (2025, 7 + mth) if mth < 6 else (2026, mth - 5)
        lo = dt.datetime(y, mo, 1)
        hi = (dt.datetime(y + (mo == 12), mo % 12 + 1, 1) - dt.timedelta(minutes=1))
        for _ in range(int(rng.integers(205, 290))):
            a = None if rng.random() < 0.09 else str(rng.choice(allacc))
            rows.append((_season_t(rng, lo, hi), a, f"NL{y % 100:02d}{mo:02d}", 5.0))
    rows.sort(key=lambda r: (r[0], r[2], r[1] or ""))
    span = (P.SEASON_END - P.SEASON_START).total_seconds()
    used, out = set(), []
    for j, (t, a, code, disc) in enumerate(rows):
        oid = 2_180_000 + int((t - P.SEASON_START).total_seconds() / span * 423_000)
        while oid in used:
            oid += 1
        used.add(oid)
        out.append(dict(redemption_id=f"PR{3_310_000 + j * 3 + int(rng.integers(0, 3)):07d}",
                        redeemed_at=t, order_id=f"VM{oid}", account_id=a, promo_code=code,
                        discount_eur=disc))
    T["promo"] = pd.DataFrame(out)
    T["profile_keep"] = keep
    return T


def revert_moves(T):
    """On 16 September the checkout squad put part of the 14 September rebalance back: those accounts
    carry a second move, back to the cohort they came from, and that cohort is their assignment at
    extract. Every move stays inside its rollout wave, so no session's exposure changes."""
    rng = np.random.default_rng(P.REVERT_SEED)
    fl = T["flags"]
    back = []
    for m in fl["assignment_moves"]:
        if rng.random() < P.REVERT_SHARE:
            back.append({"account_id": m["account_id"], "from_cohort": m["to_cohort"], "to_cohort": m["from_cohort"],
                         "moved_at": P.REVERT_AT.strftime("%Y-%m-%dT%H:%M:%S+01:00")})
    home = {m["account_id"]: m["to_cohort"] for m in back}
    fl["assignments"] = [{"account_id": a["account_id"], "cohort": home.get(a["account_id"], a["cohort"])}
                         for a in fl["assignments"]]
    fl["assignment_moves"] = sorted(fl["assignment_moves"] + back, key=lambda m: (m["moved_at"], m["account_id"]))
    T["reverted"] = sorted(home)
    return T


# --------------------------------------------------------------------------- orchestration

def build_truth(seed=P.SEED):
    rng = np.random.default_rng(seed)
    acc, used = make_accounts(rng)
    sk = make_skeleton(rng, acc)
    sk, victims = add_bots(rng, sk, acc)
    allocate_mixed(rng, sk)
    switches = xy_switches(rng, sk, acc)
    sk = allocate_outcomes(rng, sk, acc, switches)
    sk, resave = simulate_cp4(rng, sk, acc)
    bal, bal_it = balance_baseline(rng, sk, switches)
    cat, cat_hist = make_catalogue(rng)
    make_baskets(rng, sk, cat)
    tk, harvested, nonacct = make_tokens(rng, sk, acc, used)
    prof = make_profiles(rng, acc)
    ab = make_addresses(rng, acc, sk, resave)
    cards, cch = make_cards(rng, acc, switches)
    # the card and the address each session carried
    dflt = cards[cards.is_default]
    orig = {}
    for a, fp, iss, added in zip(cards.account_id, cards.card_fp, cards.issuer, cards.added_at):
        if a in switches and added == switches[a]:
            continue
        if a not in orig or (a in switches and iss in (P.ISSUER_X, P.ISSUER_Y)):
            orig.setdefault(a, fp)
    first_default = {}
    for a, fp, isd, iss in zip(cards.account_id, cards.card_fp, cards.is_default, cards.issuer):
        if isd and a not in switches:
            first_default[a] = fp
    for a in switches:
        x = cards[(cards.account_id == a) & cards.issuer.isin([P.ISSUER_X, P.ISSUER_Y])]
        first_default[a] = x.card_fp.iloc[0]
    new_default = dict(zip(dflt.account_id, dflt.card_fp))
    card_fp = np.empty(len(sk), dtype=object)
    for i, (a, t, seg) in enumerate(zip(sk.acct, sk.t, sk.seg)):
        if seg in ("SI", "BOTI"):
            card_fp[i] = new_default[a] if (a in switches and t >= switches[a]) else first_default[a]
    sk["card_fp"] = card_fp
    member_card_fp = {a: first_default[a] for a in acc.account_id[acc.klass == "MEMBER"]}
    p2_card_fp = {int(m): fp16(rng) for m in nonacct}
    ab_l = ab.assign(local=ab.changed_at + dt.timedelta(hours=1)).sort_values("local")
    hist = {}
    for a, aid, isd, f, loc in zip(ab_l.account_id, ab_l.address_id, ab_l.is_default, ab_l.address_fp, ab_l.local):
        if isd:
            hist.setdefault(a, []).append((loc, f))
    full_fp = {}
    for a, ev, f in zip(ab.account_id, ab.event, ab.address_fp):
        if ev == "updated":
            full_fp.setdefault(a, f)

    def fp_asof(a, t):
        cur = None
        for loc, f in hist[a]:
            if loc <= t:
                cur = f
        return cur
    afp = np.empty(len(sk), dtype=object)
    for i, (a, t, seg, st, p1) in enumerate(zip(sk.acct, sk.t, sk.seg, sk.step, sk.p1)):
        if P.STEPS.index(st) < 3:
            continue
        if seg == "SI":
            afp[i] = full_fp.get(a, fp16(rng)) if p1 else fp_asof(a, t)
        elif seg == "CLUB4":
            afp[i] = fp_asof(a, t)
        else:
            afp[i] = fp16(rng)
    sk["address_fp"] = afp
    refund = make_orders(rng, sk)
    att = make_attempts(rng, sk, cards, member_card_fp, p2_card_fp)
    make_ids(rng, sk)
    sk["landing_url"] = [landing(rng, seg, src, b, tok) for seg, src, b, tok in
                         zip(sk.seg, sk.source, sk.basket, sk.token)]
    edge = make_edge(rng, sk)
    flags = make_flags(acc)
    T = dict(acc=acc, sk=sk, victims=victims, switches=switches, resave=resave, cat=cat, cat_hist=cat_hist,
             tokens=tk, harvested=harvested, nonacct=nonacct, profiles=prof, address=ab, cards=cards,
             card_changes=cch, refund=refund, attempts=att, edge=edge, flags=flags, balance=bal, balance_it=bal_it)
    T = make_member_links(T)
    return revert_moves(T)


# --------------------------------------------------------------------------- baseline balance

def balance_baseline(rng, sk, switches, tol=0.3):
    """Swap baseline-week conversions between sessions of the same account class, week and basket
    type until every account set a population can be read through converts at the signed-in rate.
    Totals per class, week and basket type are unchanged by construction."""
    nb = (sk.bot == "")
    si = sk[(sk.seg == "SI") & nb]
    base = sk[(sk.seg == "SI") & sk.week.isin(P.BASE)]
    r_si = base.order.mean()
    sets = {}
    for w in P.REVIEW:
        sets[("P1", w)] = set(si.acct[si.p1 & (si.week == w)])
        sets[("P3", w)] = set(si.acct[si.p3 & (si.week == w)])
        sets[("P3cur", w)] = sets[("P3", w)] - set(switches)
        c4 = sk[(sk.seg == "CLUB4") & (sk.week == w)]
        sets[("P4", w)] = set(c4.acct)
    rv = P.REVIEW
    sets[("P1", "win")] = set().union(*[sets[("P1", w)] for w in rv])
    sets[("P3", "win")] = set().union(*[sets[("P3", w)] for w in rv])
    sets[("P3cur", "win")] = sets[("P3", "win")] - set(switches)
    sets[("P4", "win")] = set().union(*[sets[("P4", w)] for w in rv])
    c4 = sk[sk.seg == "CLUB4"]
    late = set(c4.acct[c4.t >= dt.datetime(2026, 9, 1)])
    sets[("P4sep", "win")] = sets[("P4", "win")] & late
    sets[("P4sep", "W1")] = sets[("P4", "W1")] & set(c4.acct[(c4.week == "W1") & (c4.t >= dt.datetime(2026, 9, 1))])
    keys = sorted(sets, key=str)
    idx = base.index.to_numpy()
    acct = base.acct.to_numpy()
    member = np.array([[a in sets[k] for k in keys] for a in acct], dtype=np.int8)
    order = sk.order.to_numpy().copy()
    step = sk.step.to_numpy().copy()
    o = order[idx].astype(float)
    target = member.T.astype(float) @ np.full(len(idx), r_si)
    dev = member.T.astype(float) @ o - target
    grp = (base.klass + "|" + base.week + "|" + base.mixed.astype(str)).to_numpy()
    groups = {}
    for j, gname in enumerate(grp):
        groups.setdefault(gname, []).append(j)
    gnames = sorted(groups)
    M = member.astype(float)
    nrm = (M ** 2).sum(axis=1)
    it, stall = 0, 0
    best_obj = (dev ** 2).sum()
    while it < 8000 and stall < 400:
        it += 1
        gname = gnames[int(rng.integers(0, len(gnames)))]
        js = np.array(groups[gname])
        conv = js[o[js] == 1]
        non = js[o[js] == 0]
        if len(conv) == 0 or len(non) == 0:
            stall += 1
            continue
        xs = rng.choice(conv, size=min(150, len(conv)), replace=False)
        ys = rng.choice(non, size=min(300, len(non)), replace=False)
        Mx, My = M[xs], M[ys]
        gain = (-(nrm[xs][:, None] + nrm[ys][None, :] - 2 * Mx @ My.T)
                - 2 * (My @ dev)[None, :] + 2 * (Mx @ dev)[:, None])
        i, j = np.unravel_index(int(np.argmax(gain)), gain.shape)
        if gain[i, j] <= 1e-9:
            stall += 1
            continue
        bx, by = xs[i], ys[j]
        dev = dev - M[bx] + M[by]
        o[bx], o[by] = 0.0, 1.0
        ix, iy = idx[bx], idx[by]
        order[ix], order[iy] = False, True
        step[ix], step[iy] = step[iy], step[ix]
        obj = (dev ** 2).sum()
        stall = 0 if obj < best_obj - 1e-9 else stall + 1
        best_obj = min(best_obj, obj)
    sk["order"] = order
    sk["step"] = step
    return {str(k): round(float(v), 3) for k, v in zip(keys, dev)}, it
