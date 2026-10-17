"""task239 world: Lowfirth Parcels' teams before and after the 1 September 2027 reorganisation, its staff, who
returned the 2027 Staff Voice survey and by which channel, and every answer as the member gave it (the generator's
clean truth: team climate and workload, each member's own disposition)."""
import datetime as dt

import numpy as np

import params as P

ALPHA = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

AM_SPEC = ["Sortation", "Inbound", "Outbound", "Loading", "Unloading", "Despatch", "Returns", "Hazardous Goods",
           "Bulky Items", "Small Parcels", "Trunk Marshalling", "Yard", "Quality", "Exceptions", "Customs"]
ST_SPEC = ["Linehaul", "Trunking", "Shunting", "Fleet Maintenance", "Tyre Bay", "Vehicle Inspection", "Fuel Bay",
           "Workshop", "Trailer Repair", "Night Trunking", "Recovery"]
WC_UNITS = ["Customer Contact", "Claims", "Complaints", "Business Accounts", "Live Chat", "Escalations",
            "Collections Booking", "Returns Desk"]
MH_UNITS = ["Conveyor Maintenance", "Electrical Engineering", "Building Maintenance", "Scanner Support", "Automation",
            "Health and Safety", "Facilities", "Engineering Stores"]
CP_UNITS = ["Delivery Drivers", "Collection Drivers", "Depot Sortation", "Depot Loading", "Route Planning",
            "Parcel Exceptions", "Van Fleet", "Click and Collect", "Driver Trainers", "Depot Supervisors"]
CS_UNITS = ["Finance", "Payroll", "IT Service Desk", "Procurement", "Human Resources", "Legal", "Data and Analytics",
            "Pricing", "Sales Support", "Marketing", "Facilities Management", "Insurance", "Training",
            "Internal Audit"]
AREAS = ["North", "South", "East", "West", "Central", "Harbour", "Coastal", "Riverside", "Valley", "Hill"]
QUEUES = ["Inbound", "Outbound", "Priority", "Key Account", "Residential", "Retail", "Online", "Weekend", "Overnight",
          "Specialist"]
FUNCTIONS = ["Operations", "Commercial", "Projects", "Group", "Regional", "Business Partnering", "Shared Services",
             "Reporting", "Policy", "Change"]


class World:
    pass


def _names(rng, div, n):
    out, seen, k = [], set(), 0
    while len(out) < n:
        k += 1
        if div == "AM":
            s = AM_SPEC[rng.integers(len(AM_SPEC))]
            name = ["%s Team %d" % (s, rng.integers(1, 60)), "%s Planning %d" % (s, rng.integers(1, 4)),
                    "%s Supervisors %d" % (s, rng.integers(1, 4))][rng.choice(3, p=[0.6, 0.2, 0.2])]
        elif div == "ST":
            s = ST_SPEC[rng.integers(len(ST_SPEC))]
            name = ["%s Crew %d" % (s, rng.integers(1, 60)), "%s Desk %d" % (s, rng.integers(1, 6)),
                    "%s Admin %d" % (s, rng.integers(1, 4))][rng.choice(3, p=[0.5, 0.3, 0.2])]
        else:
            units = {"WC": WC_UNITS, "MH": MH_UNITS, "CP": CP_UNITS, "CS": CS_UNITS}[div]
            u = units[rng.integers(len(units))]
            # depot and engineering teams by area, contact-centre teams by queue, corporate teams by function
            a = {"WC": QUEUES, "CS": FUNCTIONS}.get(div, AREAS)[rng.integers(len(AREAS))]
            k2 = rng.integers(1, 9)
            name = "%s %s %d" % (a, u, k2) if div == "WC" else "%s %s %d" % (u, a, k2)
        if name not in seen:
            seen.add(name)
            out.append(name)
        assert k < 100000
    return out


def _renumbered(name, other):
    """a July name for a September team: the same team under another number (the number a name drawn for the
    division carries), as the reorganisation renumbered teams"""
    return name.rsplit(" ", 1)[0] + " " + other.rsplit(" ", 1)[1]


def _codes(rng, prefix, n, taken):
    pool = [c for c in ("%s-%03d" % (P.PREFIX[prefix], i) for i in range(101, 990)) if c not in taken]
    pick = rng.choice(len(pool), n, replace=False)
    out = [pool[i] for i in sorted(pick)]
    taken.update(out)
    return out


def _inv_codes(rng, n):
    seen, out = set(), []
    while len(out) < n:
        c = "".join(ALPHA[i] for i in rng.integers(0, len(ALPHA), 8))
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def make(seed=P.SEED):
    rng = np.random.default_rng(seed)
    W = World()
    divs = [d[0] for d in P.DIVISIONS]
    share = np.array([d[2] for d in P.DIVISIONS])
    T = P.N_TEAMS
    n_new = int(round(T * P.REORG_SHARE["new"]))
    n_ren = int(round(T * P.REORG_SHARE["renamed"]))
    n_mer = int(round(T * P.REORG_SHARE["merged"]))
    n_spl = int(round(T * P.REORG_SHARE["split"]))          # July teams split in two
    kinds = (["new"] * n_new + ["reissued"] * P.REISSUED + ["renamed"] * n_ren + ["merged"] * n_mer
             + ["split"] * (2 * n_spl))
    kinds += ["unchanged"] * (T - len(kinds))
    kinds = np.array(kinds, dtype=object)
    # divisions: split successors share their July team's division; the reissued teams take the division of the
    # split team whose code they reuse
    div = rng.choice(divs, T, p=share / share.sum()).astype(object)
    spl_idx = np.flatnonzero(kinds == "split")
    for a in range(0, len(spl_idx), 2):
        div[spl_idx[a + 1]] = div[spl_idx[a]]
    reis_idx = np.flatnonzero(kinds == "reissued")
    reis_div = ["AM", "CP", "MH", "AM", "CP"][:P.REISSUED]
    for i, d in zip(reis_idx, reis_div):
        div[i] = d
    # the three split teams whose codes are reissued sit in those divisions
    for k, d in enumerate(reis_div):
        div[spl_idx[2 * k]] = d
        div[spl_idx[2 * k + 1]] = d
    W.T = T
    W.kind = kinds
    W.div = div
    # September names and codes
    taken = set()
    W.name = np.empty(T, dtype=object)
    W.code = np.empty(T, dtype=object)
    for d in divs:
        idx = np.flatnonzero(div == d)
        for i, nm in zip(idx, _names(rng, d, len(idx))):
            W.name[i] = nm
    # codes: unchanged, new, renamed, merged and split teams draw fresh September codes; reissued teams take a
    # July code of a split team (set below)
    for d in divs:
        idx = np.flatnonzero((div == d) & (kinds != "reissued"))
        for i, c in zip(idx, _codes(rng, d, len(idx), taken)):
            W.code[i] = c
    # July structure
    jul = []                                            # (code, name, div, successors, change)
    W.jul_of = [[] for _ in range(T)]                     # July codes each September team's members came from
    for i in np.flatnonzero(kinds == "unchanged"):
        jul.append((W.code[i], W.name[i], div[i], [i], "unchanged"))
        W.jul_of[i] = [W.code[i]]
    for i in np.flatnonzero(kinds == "renamed"):
        old = _codes(rng, div[i], 1, taken)[0]
        if rng.random() < 0.5:                          # renumbered in the new structure
            n_now = int(W.name[i].rsplit(" ", 1)[1])
            oldname = _renumbered(W.name[i], "x %d" % (n_now + 1 if n_now < 9 else n_now - 1))
        else:
            oldname = _renumbered(W.name[i], _names(rng, div[i], 1)[0])
        jul.append((old, oldname, div[i], [i], "renamed"))
        W.jul_of[i] = [old]
    for i in np.flatnonzero(kinds == "merged"):
        olds = _codes(rng, div[i], 2, taken)
        nms = [_renumbered(W.name[i], x) for x in _names(rng, div[i], 2)]
        if nms[1] == nms[0]:
            nms[1] = _renumbered(nms[0], "x %d" % (int(nms[0].rsplit(" ", 1)[1]) + 1))
        for o, nm in zip(olds, nms):
            jul.append((o, nm, div[i], [i], "merged"))
        W.jul_of[i] = olds
    split_jul = []
    for a in range(0, len(spl_idx), 2):
        i1, i2 = spl_idx[a], spl_idx[a + 1]
        old = _codes(rng, div[i1], 1, taken)[0]
        nm = W.name[i1].rsplit(" ", 1)[0] if W.name[i1][-1].isdigit() else W.name[i1]
        if W.name[i2][-1].isdigit():                    # both halves keep the split team's function
            k2, names_now = int(W.name[i2].rsplit(" ", 1)[1]), set(W.name)
            while "%s %d" % (nm, k2) in names_now:
                k2 += 1
            W.name[i2] = "%s %d" % (nm, k2)
        jul.append((old, nm, div[i1], [i1, i2], "split"))
        W.jul_of[i1] = [old]
        W.jul_of[i2] = [old]
        split_jul.append(old)
    # the reissued codes: the first three split teams' July codes go to three new September teams
    W.reissued = []
    for k, i in enumerate(reis_idx):
        W.code[i] = split_jul[k]
        W.reissued.append((split_jul[k], i))
    W.name_reissued = {}
    for (c, i), nm in zip(W.reissued, ["Peak Sortation Team", "Same Day Couriers",
                                       "Robotics Support Team", "Cross-Dock Team", "Rural Delivery Team"]):
        W.name[i] = nm
    W.split_reissued = np.array(sorted(int(i) for a in range(0, 2 * P.REISSUED, 2)
                                       for i in (spl_idx[a], spl_idx[a + 1])))
    # new teams' members came from other July teams of their division
    unchanged_by_div = {d: [j for j in jul if j[2] == d and j[4] == "unchanged"] for d in divs}
    for i in np.flatnonzero((kinds == "new") | (kinds == "reissued")):
        pool = unchanged_by_div[div[i]]
        W.jul_of[i] = [pool[rng.integers(len(pool))][0]]
    W.jul = jul
    assert len(set(W.code)) == T
    # divisions on the census date and later: teams that moved on 1 September kept their codes; depot conveyor
    # maintenance teams moved on 1 November
    W.prev_div = np.full(T, "", dtype=object)
    W.div_since = np.full(T, "", dtype=object)
    cs_un = np.flatnonzero((div == "CS") & (kinds == "unchanged"))
    sept_movers = rng.choice(cs_un, 14, replace=False)
    for i in sept_movers:
        W.prev_div[i] = "CS"
        W.div[i] = "CP"
        W.div_since[i] = P.REORG.isoformat()
        W.name[i] = "Depot Administration %s %d" % (AREAS[rng.integers(len(AREAS))], rng.integers(1, 9))
    mh_cmht = [i for i in np.flatnonzero((div == "MH") & (kinds == "unchanged"))
               if W.name[i].startswith("Conveyor Maintenance ")]
    nov = list(rng.choice(mh_cmht, min(22, len(mh_cmht)), replace=False))
    W.census_div = W.div.copy()
    for i in nov:
        W.prev_div[i] = "MH"
        W.div[i] = "CP"
        W.div_since[i] = P.DIVISION_MOVE.isoformat()
    W.nov_movers = np.array(sorted(nov))
    W.sept_movers = np.array(sorted(sept_movers))
    # names must stay unique after the renames above
    seen = {}
    for i in range(T):
        while W.name[i] in seen:                      # a clash takes the next free number
            head, tail = W.name[i].rsplit(" ", 1)
            W.name[i] = "%s %d" % (head, int(tail) + 1) if tail.isdigit() else W.name[i] + " (2)"
        seen[W.name[i]] = i
    # sites
    W.site = np.empty(T, dtype=object)
    for i in range(T):
        d = W.census_div[i]
        opts = [(s[0], s[3][d]) for s in P.SITES if d in s[3]]
        w = np.array([o[1] for o in opts])
        W.site[i] = opts[rng.choice(len(opts), p=w / w.sum())][0]
    for i in W.split_reissued:
        if W.site[i] not in P.TABLETS:
            W.site[i] = {"AM": "CHB", "CP": "NDP", "MH": "ENC"}[W.census_div[i]]
    # sizes
    size = np.clip(np.round(rng.lognormal(np.log(14.5) - 0.18, 0.6, T)), 3, 60).astype(int)
    size[kinds == "split"] = np.clip(np.round(size[kinds == "split"] * 0.7), 4, 40)
    size[kinds == "new"] = np.clip(np.round(size[kinds == "new"] * 0.6), 4, 20)
    for c, i in W.reissued:
        size[i] = 10 + rng.integers(0, 5)
    for i in W.split_reissued:
        size[i] = 20 + rng.integers(0, 8)
    W.size = size
    # team climate and workload
    W.C = rng.standard_normal(T)
    W.L = P.RHO_CL * W.C + np.sqrt(1 - P.RHO_CL ** 2) * rng.standard_normal(T)
    W.C[W.size < 9] += 0.3                              # small teams rate their climate better
    W.C[np.isin(W.site, P.SYNC_SITES)] += 0.3
    W.resB = rng.standard_normal((T, len(P.ITEMS)))
    W.paper_all = (rng.random(T) < P.PAPER_ALL_TEAMS) & np.isin(kinds, ["unchanged", "renamed", "merged", "split"])
    W.prop = np.clip(rng.beta(6, 6, T) * 2 * P.RESPONSE_MEAN, 0.06, 0.95)
    _members(W, rng)
    _returns(W, rng)
    return W


def _members(W, rng):
    T = W.T
    team = np.repeat(np.arange(T), W.size)
    n = len(team)
    W.n = n
    W.m_team = team
    d = W.census_div[team]
    pe = np.array([P.EMAIL[x] for x in d])
    newish = np.isin(W.kind[team], ["new", "reissued"])
    pe[newish] = 1.0
    pe[np.isin(team, W.split_reissued)] = 0.5
    W.m_email = rng.random(n) < pe
    W.m_pack = (~W.m_email) | W.paper_all[team]
    W.m_inv = np.array(_inv_codes(rng, n), dtype=object)
    W.m_F = rng.standard_normal(n)
    W.m_U = rng.standard_normal((n, len(P.ITEMS)))
    W.m_group = rng.choice(len(P.STAFF_GROUPS), n, p=[0.36, 0.08, 0.12, 0.04, 0.2, 0.12, 0.06, 0.02])
    W.m_years = rng.choice(5, n, p=[0.12, 0.2, 0.22, 0.24, 0.22])
    # each member's July team code: the July team they were in
    jul = np.empty(n, dtype=object)
    for t in range(T):
        idx = np.flatnonzero(team == t)
        opts = W.jul_of[t]
        jul[idx] = [opts[k] for k in rng.integers(0, len(opts), len(idx))]
    W.m_jul = jul
    lp = np.log(W.prop[team] / (1 - W.prop[team])) + 0.25 * W.m_F
    W.m_resp = rng.random(n) < 1 / (1 + np.exp(-lp))


def _answer(W, rng, m, occasion):
    """one return's scored answers (1 to 5, favourable high) for the index items, before any channel coding"""
    t = W.m_team[m]
    out = np.zeros(len(P.ITEMS), dtype=int)
    for j, (code, wording, neg, (icc, bC, bL, om), icpt, nr) in enumerate(P.ITEMS):
        sB, sW = np.sqrt(icc), np.sqrt(1 - icc)
        rB = np.sqrt(max(1 - (bC ** 2 + bL ** 2 + 2 * bC * bL * P.RHO_CL), 0))
        u = W.m_U[m, j] if occasion is None else 0.85 * W.m_U[m, j] + 0.527 * occasion[j]
        y = icpt + sB * (bC * W.C[t] + bL * W.L[t] + rB * W.resB[t, j]) + sW * (om * W.m_F[m] + np.sqrt(1 - om ** 2) * u)
        out[j] = 1 + int(np.sum(y > np.array(P.THRESHOLDS)))
    return out


def _engage(W, rng, m):
    t = W.m_team[m]
    base = 0.55 * W.m_F[m] + 0.25 * W.C[t] - 0.2 * W.L[t]
    vals = []
    for k in range(len(P.ENGAGE)):
        y = base + 0.8 * rng.standard_normal() + (0.3 if k in (2, 5) else 0.0)
        if k == 3:
            y = -y
        vals.append(1 + int(np.sum(y > np.array(P.THRESHOLDS))))
    return vals


def _nonresponse(rng, j, paper, f=0.0):
    dk, skip = P.ITEMS[j][5]
    lift = float(np.exp(-0.9 * f))                     # members who think less of their team leave more items
    dk, skip = dk * lift, skip * lift
    u = rng.random()
    if u < dk:
        return "dk"
    if u < dk + skip:
        return "skip"
    if paper and u < dk + skip + 0.004:
        return "multi"
    return None


def _returns(W, rng):
    """every return as made: channel, the time it reached the company, the team code on it and its answers"""
    n = W.n
    team = W.m_team
    tablets = np.isin(W.site[team], list(P.TABLETS))
    resp = np.flatnonzero(W.m_resp)
    chan = np.empty(n, dtype=object)
    for m in resp:
        key = "email_pack" if (W.m_email[m] and W.m_pack[m]) else ("email" if W.m_email[m] else "pack")
        p = np.array(P.CHANNEL[key], dtype=float)
        if W.site[team[m]] in P.SYNC_SITES or team[m] in W.split_reissued:
            p[1] *= 1.8
        if not tablets[m]:
            p[1] = 0.0
        chan[m] = ["personal", "site", "paper"][rng.choice(3, p=p / p.sum())]
    W.m_chan = chan
    newish = np.isin(W.kind[team], ["new", "reissued"])
    # members who return twice: the first return, then a second at least two days later by another channel
    weights = np.exp(0.6 * W.m_F + 0.9 * W.C[team])
    cand = {"A": [m for m in resp if chan[m] == "paper" and W.m_email[m]],
            "E": [m for m in resp if chan[m] == "personal" and W.m_pack[m]],
            "B": [m for m in resp if chan[m] == "personal" and tablets[m]],
            "C": [m for m in resp if chan[m] == "site" and W.m_email[m] and not newish[m]],
            "D": [m for m in resp if chan[m] == "paper" and tablets[m]]}
    share = {"A": 0.33, "E": 0.12, "B": 0.22, "C": 0.15, "D": 0.18}
    dual = {}
    used = set()
    for k in "AEBCD":
        pool = np.array([m for m in cand[k] if m not in used])
        want = int(round(P.N_DUAL * share[k]))
        w = weights[pool] / weights[pool].sum()
        pick = rng.choice(pool, min(want, len(pool)), replace=False, p=w)
        for m in pick:
            dual[int(m)] = k
            used.add(int(m))
    W.dual = dual
    # personal resubmissions (two submitted sessions on one link)
    pers = [m for m in resp if chan[m] == "personal" and m not in used]
    W.resubmit = set(int(x) for x in rng.choice(pers, P.N_RESUBMIT, replace=False))
    rets = []
    days = (P.CLOSE.date() - P.OPEN.date()).days + 1

    wday = np.array([3.0 if k < 3 else 1.0 for k in range(days)])
    for r in P.REMINDERS:
        wday[(r - P.OPEN.date()).days] += 2.2
        wday[(r - P.OPEN.date()).days + 1] += 1.0

    def online_time(after=None, site=False):
        lo = 0 if after is None else (after.date() - P.OPEN.date()).days + 2
        ok = [k for k in range(lo, days) if not (site and (P.OPEN.date() + dt.timedelta(days=k)).weekday() >= 5)]
        if not ok:
            return None
        if after is not None:
            w = np.ones(len(ok))
        elif site:
            w = np.array([2.2 if k < 7 else 1.0 for k in ok])
        else:
            w = wday[ok]
        for _ in range(200):
            dd = P.OPEN.date() + dt.timedelta(days=int(ok[rng.choice(len(ok), p=w / w.sum())]))
            hh = rng.uniform(7.5, 19.0) if site else [rng.uniform(7, 9), rng.uniform(12, 14),
                                                       rng.uniform(19, 22.5)][rng.integers(3)]
            t = dt.datetime.combine(dd, dt.time(0)) + dt.timedelta(hours=float(hh))
            if t < P.OPEN or t > P.CLOSE - dt.timedelta(hours=2):
                continue
            if site and P.REFRESH_OFF <= t < P.REFRESH_ON + dt.timedelta(minutes=20):
                continue
            return t.replace(microsecond=0)
        return None

    def paper_time(after=None):
        lo = dt.date(2027, 9, 7)
        if after is not None:
            lo = max(lo, after.date() + dt.timedelta(days=2))
        span = [lo + dt.timedelta(days=k) for k in range((P.PAPER_DEADLINE - lo).days + 1)]
        span = [x for x in span if x.weekday() < 5]
        if not span:
            return None
        dd = span[rng.integers(len(span))]
        return (dt.datetime.combine(dd, dt.time(0)) + dt.timedelta(hours=float(rng.uniform(9, 16)))).replace(microsecond=0)

    def make_ret(m, ch, t, occasion=None, entered=False):
        r = dict(member=m, chan=ch, time=t, scored=_answer(W, rng, m, occasion), engage=_engage(W, rng, m),
                 nr=[_nonresponse(rng, j, ch == "paper", W.m_F[m] + 0.6 * W.C[team[m]]) for j in range(len(P.ITEMS))],
                 entered=entered)
        if ch == "personal":
            r["team_code"] = W.code[team[m]]
        elif ch == "site":
            r["team_code"] = W.m_jul[m] if t < P.REFRESH_ON else W.code[team[m]]
        else:
            r["team_code"] = W.m_jul[m]
        return r

    for m in resp:
        ch = chan[m]
        if ch == "site" and newish[m]:
            pre = True
            while pre:
                t = online_time(site=True)
                pre = t < P.REFRESH_ON
        elif ch == "paper":
            t = paper_time()
        else:
            t = online_time(site=(ch == "site"))
        k = dual.get(int(m))
        entered = ch == "site" and (k == "C" or rng.random() < P.SITE_CODE_ENTERED)
        first = make_ret(m, ch, t, entered=entered)
        first["dual"] = k
        rets.append(first)
        if k is not None:
            ch2 = {"A": "personal", "E": "paper", "B": "site", "C": "personal", "D": "site"}[k]
            t2 = None
            for _ in range(50):
                t2 = paper_time(after=t) if ch2 == "paper" else online_time(after=t, site=(ch2 == "site"))
                if t2 is not None and (ch2 != "site" or t2 >= P.REFRESH_ON or not newish[m]):
                    break
            if t2 is None:
                del W.dual[int(m)]
                first["dual"] = None
                continue
            second = make_ret(m, ch2, t2, occasion=rng.standard_normal(len(P.ITEMS)), entered=(ch2 == "site"))
            second["dual"] = k
            rets.append(second)
        if int(m) in W.resubmit:
            t2 = t + dt.timedelta(hours=float(rng.uniform(1, 72)))
            if t2 < P.CLOSE - dt.timedelta(hours=2):
                again = make_ret(m, "personal", t2.replace(microsecond=0), occasion=rng.standard_normal(len(P.ITEMS)))
                again["resubmit"] = True
                rets.append(again)
    # paper forms scanned after the deadline, and forms that came back with nothing marked
    lone_paper = [r for r in rets if r["chan"] == "paper" and r.get("dual") is None]
    late = rng.choice(len(lone_paper), P.N_LATE, replace=False)
    span = [P.LATE_SCANS[0] + dt.timedelta(days=k) for k in range((P.LATE_SCANS[1] - P.LATE_SCANS[0]).days + 1)]
    span = [x for x in span if x.weekday() < 5]
    for k in late:
        dd = span[rng.integers(len(span))]
        lone_paper[k]["time"] = (dt.datetime.combine(dd, dt.time(0))
                                 + dt.timedelta(hours=float(rng.uniform(9, 16)))).replace(microsecond=0)
        lone_paper[k]["late"] = True
    packs_idle = np.flatnonzero(W.m_pack & ~W.m_resp)
    for m in rng.choice(packs_idle, P.N_BLANK, replace=False):
        r = make_ret(int(m), "paper", paper_time())
        r["blank"] = True
        rets.append(r)
    W.rets = rets
