"""The hospitals' financial-assistance operations around the counsellors' decisions: the log rows each hub's system
writes (determinations, pends, withdrawals, the nightly presumptive screening), the applications and the patient
accounts they cover, and the write-offs and reversals the billing systems post.

Counsellor determinations come from world.py's decision chains unchanged, in their order; a pend or a withdrawal sits
between two determinations and is not one. The presumptive screening runs at about two in the morning on weekdays
and approves accounts under the hub's system user; on nine nights a year at each hub the job was restarted after a
failure and posted part of that night's approvals again under fresh application numbers (the accounts were already
written off, so the second write-off is zero). A write-off line is posted for every account an approval covers, each
carrying the approval's whole write-off; a reversal is posted on one account at that account's own amount."""
import datetime as dt

import numpy as np

import common as K
import world as W

TIER_P = ([100, 75, 50, 25], [0.55, 0.15, 0.15, 0.15])
N_ACC = ([1, 2, 3, 4], [0.62, 0.25, 0.09, 0.04])
REASON_P = (K.DENIAL_REASONS, [0.33, 0.52, 0.10, 0.05])
RERUN_NIGHTS = 9


def bday_add(d, n):
    while n:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in K.HOLIDAYS:
            n -= 1
    return d


def hub_on(code, d):
    if code == K.MIGRATED:
        return "columbia" if d < K.MIGRATION else "puget"
    return K.HUB[code]


class Ids:
    """Every identifier in its hub's or hospital's own format, issued in order and never reused."""

    def __init__(self, r):
        self.r = r
        self.n = {}
        self.used = set()

    def nxt(self, key, start):
        self.n[key] = self.n.get(key, start) + int(self.r.integers(1, 4))
        return self.n[key]

    def rand(self, fmt, lo, hi):
        while True:
            v = fmt % int(self.r.integers(lo, hi))
            if v not in self.used:
                self.used.add(v)
                return v


def app_id(ids, code, hub, presumptive, d):
    if hub == "puget":
        return ("P%d%07d" if presumptive else "A%d%07d") % (d.year % 100, ids.nxt(("pa", code, presumptive), 1000000 + 37000 * int(code[1:])))
    if hub == "willamette":
        return "%08d" % ids.nxt(("wa", code, presumptive), (91000000 if presumptive else 25000000) + 41000 * int(code[1:]))
    return ("PE-%d-%06d" if presumptive else "FA-%d-%06d") % (d.year, ids.nxt(("ca", code, presumptive), 100000 + 23000 * int(code[1:])))


def counsellor_ids(r, ids, code, C):
    hub = K.HUB[code]
    out = []
    for c in range(C):
        if hub == "puget":
            a = ids.rand("PS%04d", 1000, 9999)
        elif hub == "willamette":
            a = ids.rand("wfa%04d", 100, 2999)
        else:
            a = ids.rand("CB-%05d", 10000, 89999)
        b = ids.rand("PS%04d", 1000, 9999) if code == K.MIGRATED else None
        out.append((a, b))
    return out


def clock(day, secs):
    """Seconds of working time after 08:00 to a local wall-clock datetime, with a 45-minute lunch from noon."""
    base = dt.datetime.combine(day, dt.time(8, 0))
    return base + dt.timedelta(seconds=int(secs) + (45 * 60 if secs >= 4 * 3600 else 0))


def accounts_for(r, ids, code, guarantor, first_seen, n):
    accs = []
    for _ in range(n):
        hub = K.HUB[code]
        num = ids.rand({"puget": "HB%09d", "willamette": "8%09d", "columbia": "AC-%08d"}[hub], 10 ** 7, 10 ** 8 - 1)
        charges = float(np.round(np.exp(r.normal(7.75, 1.05)), 2)) + 85.0
        paid = float(np.round(charges * r.uniform(0.40, 0.85), 2)) if r.random() < 0.55 else 0.0
        bal = round(max(charges - paid, 25.0 + float(r.uniform(0, 40))), 2)
        accs.append(dict(account=num, code=code, guarantor=guarantor,
                         service=first_seen - dt.timedelta(days=int(r.integers(15, 200))),
                         charges=round(bal + paid, 2), balance=bal))
    return accs


def build(hs, seed=W.SEED):
    r = np.random.default_rng([seed, 99])
    ids = Ids(r)
    rows, apps, accounts, crosswalk = [], {}, {}, []
    for h in hs:
        code = h["code"]
        rh = np.random.default_rng([seed, int(code[1:]), 7, h["attempt"]])
        cid = counsellor_ids(rh, ids, code, h["C"])
        h["counsellor_ids"] = cid
        if code == K.MIGRATED:
            for a, b in cid:
                crosswalk.append(dict(code=code, old=a, new=b, effective=K.MIGRATION))
        start = [int(rh.integers(-25, 46)) * 60 for _ in range(h["C"])]
        guar = lambda: ids.rand("G%08d", 10 ** 7, 10 ** 8 - 1)
        # every counsellor-day in date order, so a reconsideration finds the denial it reopens
        daylist = sorted(((d["date"], c, d) for c, co in enumerate(h["couns"]) for d in co["days"]),
                         key=lambda t: (t[0], t[1]))
        incomplete = []          # (date, application) denied for missing documents, not yet reopened
        pend_wanted = []
        for day, c, d in daylist:
            y, recon = d["y"], d["recon"]
            n = len(y)
            extra = int(rh.binomial(n, 0.012))           # withdrawals recorded during the day
            m = n + extra
            secs = np.sort(rh.choice(np.arange(60, 480 * 60 - 60), size=m, replace=False)) + start[c]
            pos_extra = set(rh.choice(m, size=extra, replace=False).tolist()) if extra else set()
            ti = 0
            k = 0
            user = cid[c][0] if hub_on(code, day) == K.HUB[code] or code != K.MIGRATED else cid[c][1]
            for j in range(m):
                when = clock(day, secs[j])
                hub = hub_on(code, day)
                if j in pos_extra:
                    g = guar()
                    a = app_id(ids, code, hub, False, day)
                    apps[a] = dict(code=code, guarantor=g, accounts=[], source="counsellor", outcome="withdraw")
                    rows.append(dict(code=code, hub=hub, when=when, user=user, app=a, guarantor=g, type="INITIAL",
                                     outcome="withdraw", tier=None, reason=None))
                    continue
                approve = bool(y[k])
                is_recon = bool(recon[k])
                k += 1
                if is_recon:
                    pool = [x for x in incomplete if 7 <= (day - x[0]).days <= 90]
                    if pool:
                        pick = pool[int(rh.integers(len(pool)))]
                        incomplete.remove(pick)
                        a = pick[1]
                    else:
                        g = guar()
                        a = ("FA-2024-%06d" % int(rh.integers(100000, 999999)) if K.HUB[code] == "columbia" else
                             "A24%07d" % int(rh.integers(1000000, 9999999)) if K.HUB[code] == "puget" else
                             "%08d" % int(rh.integers(24000000, 24999999)))
                        accs = accounts_for(rh, ids, code, g, day - dt.timedelta(days=int(rh.integers(40, 120))),
                                            int(rh.choice(N_ACC[0], p=N_ACC[1])))
                        apps[a] = dict(code=code, guarantor=g, accounts=[x["account"] for x in accs],
                                       source="counsellor", outcome="deny", year=2024)
                        for x in accs:
                            accounts[x["account"]] = x
                    g = apps[a]["guarantor"]
                    typ = "RECON"
                else:
                    g = guar()
                    a = app_id(ids, code, hub, False, day)
                    accs = accounts_for(rh, ids, code, g, day - dt.timedelta(days=int(rh.integers(5, 40))),
                                        int(rh.choice(N_ACC[0], p=N_ACC[1])))
                    apps[a] = dict(code=code, guarantor=g, accounts=[x["account"] for x in accs], source="counsellor")
                    for x in accs:
                        accounts[x["account"]] = x
                    typ = "INITIAL"
                    if rh.random() < 0.04:
                        pend_wanted.append((day, c, a, g))
                if approve:
                    tier = int(rh.choice(TIER_P[0], p=TIER_P[1]))
                    apps[a].update(outcome="approve", tier=tier, decided=day, by=user)
                    rows.append(dict(code=code, hub=hub, when=when, user=user, app=a, guarantor=g, type=typ,
                                     outcome="approve", tier=tier, reason=None))
                else:
                    reason = str(rh.choice(REASON_P[0], p=REASON_P[1]))
                    apps[a].update(outcome="deny", decided=day, by=user, reason=reason)
                    rows.append(dict(code=code, hub=hub, when=when, user=user, app=a, guarantor=g, type=typ,
                                     outcome="deny", tier=None, reason=reason))
                    if reason == "INCOMPLETE" and typ == "INITIAL":
                        incomplete.append((day, a))
        # pends: an earlier row on the application, on a day the same counsellor sat, between its determinations
        sat = {}
        for day, c, d in daylist:
            sat.setdefault(c, []).append(day)
        for day, c, a, g in pend_wanted:
            cands = [x for x in sat[c] if 3 <= (day - x).days <= 25]
            if not cands:
                continue
            pd_ = cands[int(rh.integers(len(cands)))]
            hub = hub_on(code, pd_)
            user = cid[c][0] if (code != K.MIGRATED or pd_ < K.MIGRATION) else cid[c][1]
            when = clock(pd_, int(rh.integers(60, 480 * 60 - 60)) + start[c])
            rows.append(dict(code=code, hub=hub, when=when, user=user, app=a, guarantor=g, type="INITIAL",
                             outcome="pend", tier=None, reason=None, pend=True))
    _presumptive(r, ids, hs, rows, apps, accounts)
    ledger = _ledger(r, apps, accounts)
    return dict(rows=rows, apps=apps, accounts=accounts, ledger=ledger, crosswalk=crosswalk)


def _presumptive(r, ids, hs, rows, apps, accounts):
    nights = [d for d in W.WORKDAYS]
    rerun = {hub: set(r.choice(len(nights), size=RERUN_NIGHTS, replace=False).tolist())
             for hub in ("puget", "willamette", "columbia")}
    lam = {h["code"]: float(r.uniform(0.8, 2.5)) for h in hs}
    for i, night in enumerate(nights):
        for h in hs:
            code = h["code"]
            hub = hub_on(code, night)
            n = int(r.poisson(lam[code]))
            made = []
            for _ in range(n):
                g = ids.rand("G%08d", 10 ** 7, 10 ** 8 - 1)
                fam = [g] + ([g] if r.random() < 0.10 else [])
                for gg in fam:
                    a = app_id(ids, code, hub, True, night)
                    accs = accounts_for(r, ids, code, gg, night - dt.timedelta(days=int(r.integers(3, 30))),
                                        int(r.choice([1, 2, 3], p=[0.72, 0.21, 0.07])))
                    for x in accs:
                        accounts[x["account"]] = x
                    zero = r.random() < 0.03
                    apps[a] = dict(code=code, guarantor=gg, accounts=[x["account"] for x in accs], source="presumptive",
                                   outcome="approve", tier=100, decided=night, by=K.SYSTEM_USER[hub], zero=zero)
                    when = dt.datetime.combine(night, dt.time(2, 10)) + dt.timedelta(seconds=int(r.integers(0, 1800)))
                    rows.append(dict(code=code, hub=hub, when=when, user=K.SYSTEM_USER[hub], app=a, guarantor=gg,
                                     type="PRESUMPTIVE", outcome="approve", tier=100, reason=None))
                    made.append(a)
            if i in rerun[hub] and made:
                share = r.uniform(0.4, 0.8)
                for a in made:
                    if r.random() >= share:
                        continue
                    src = apps[a]
                    b = app_id(ids, code, hub, True, night)
                    apps[b] = dict(code=code, guarantor=src["guarantor"], accounts=list(src["accounts"]),
                                   source="replay", outcome="approve", tier=100, decided=night, by=K.SYSTEM_USER[hub],
                                   replay_of=a)
                    when = dt.datetime.combine(night, dt.time(4, 5)) + dt.timedelta(seconds=int(r.integers(0, 2400)))
                    rows.append(dict(code=code, hub=hub, when=when, user=K.SYSTEM_USER[hub], app=b,
                                     guarantor=src["guarantor"], type="PRESUMPTIVE", outcome="approve", tier=100,
                                     reason=None))


def _ledger(r, apps, accounts):
    """Write-off lines (FAWO), one per account an approval covers, each at the approval's whole write-off; reversal lines
    (FAWR) on one account at that account's own write-off when Medicaid later paid the account."""
    lines = []
    for a in sorted(apps):
        x = apps[a]
        if x.get("outcome") != "approve":
            continue
        own = {acc: round(accounts[acc]["balance"] * x["tier"] / 100.0, 2) for acc in x["accounts"]}
        total = round(sum(own.values()), 2)
        if x["source"] == "replay" or x.get("zero"):
            total = 0.0
        x["writeoff"] = total
        x["own"] = own
        posted = bday_add(x["decided"], int(r.integers(1, 4)))
        for acc in x["accounts"]:
            lines.append(dict(code=x["code"], app=a, account=acc, posted=posted, kind="FAWO", amount=total))
        if total > 0 and r.random() < 0.05:
            rev = list(x["accounts"])
            r.shuffle(rev)
            for acc in rev[:int(r.integers(1, min(2, len(rev)) + 1))]:
                p2 = posted + dt.timedelta(days=int(r.integers(30, 151)))
                if p2 <= K.EXTRACT_CUT:
                    lines.append(dict(code=x["code"], app=a, account=acc, posted=p2, kind="FAWR", amount=own[acc]))
                    x.setdefault("reversed", 0.0)
                    x["reversed"] = round(x["reversed"] + own[acc], 2)
    lines.sort(key=lambda t: (t["posted"], t["code"], t["app"], t["account"], t["kind"]))
    for i, t in enumerate(lines):
        t["id"] = "FA%09d" % (300000000 + 7 * i + int(r.integers(0, 7)))
    return lines
