"""The hospitals' financial-assistance operations around the counsellors' decisions: the log rows each hub's system
writes (first decisions, reconsiderations once missing documents arrive, pends, withdrawals, the nightly presumptive
screening), the patient accounts an application covers, and the write-offs and reversals the billing systems post.

A household that applies again for the same bill after a denial or a partial discount opens no new case: its new
application is decided under a new number, and the billing system posts the new write-off under the number the case
was opened with. A write-off line is posted for every account an approval covers, each carrying the approval's whole
write-off; a reversal is posted on one account at that account's own write-off when Medicaid later paid it."""
import datetime as dt

import numpy as np

import common as K
import world as W

N_ACC = ([1, 2, 3, 4], [0.62, 0.25, 0.09, 0.04])
RECON_P = 0.55            # a documents denial reconsidered once the documents arrive
LEDGER_SALT = 0           # the ledger's own stream (posting lags and reversals)
PEND_P = 0.04


def bday_add(d, n):
    while n:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in K.HOLIDAYS_ALL:
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
        return ("P%d%07d" if presumptive else "A%d%07d") % (d.year % 100, ids.nxt(("pa", code, presumptive, d.year),
                                                                                 1000000 + 37000 * int(code[1:])))
    if hub == "willamette":
        return "%08d" % ids.nxt(("wa", code, presumptive), (91000000 if presumptive else 25000000) + 41000 * int(code[1:]))
    return ("PE-%d-%06d" if presumptive else "FA-%d-%06d") % (d.year, ids.nxt(("ca", code, presumptive, d.year),
                                                                             100000 + 23000 * int(code[1:])))


def guarantor_id(ids, hub):
    return {"puget": ids.rand("G%08d", 10 ** 7, 10 ** 8 - 1), "willamette": ids.rand("%07d", 10 ** 6, 10 ** 7 - 1),
            "columbia": ids.rand("GU-%07d", 10 ** 6, 10 ** 7 - 1)}[hub]


def counsellor_ids(ids, code, C):
    hub = K.HUB[code]
    out = []
    for _ in range(C):
        if hub == "puget":
            a = ids.rand("PS%04d", 1000, 9999)
        elif hub == "willamette":
            a = ids.rand("wfa%04d", 100, 2999)
        else:
            a = ids.rand("CB-%05d", 10000, 89999)
        b = ids.rand("PS%04d", 1000, 9999) if code == K.MIGRATED else None
        out.append((a, b))
    return out


def clock(day, r):
    """A local wall-clock time on a working day, 08:00 to 16:45 with a 45-minute lunch from noon."""
    secs = int(r.integers(60, 480 * 60 - 60))
    base = dt.datetime.combine(day, dt.time(8, 0))
    return base + dt.timedelta(seconds=secs + (45 * 60 if secs >= 4 * 3600 else 0))


def accounts_for(r, ids, code, guarantor, received, n):
    accs = []
    for _ in range(n):
        hub = K.HUB[code]
        num = ids.rand({"puget": "HB%09d", "willamette": "8%09d", "columbia": "AC-%08d"}[hub], 10 ** 7, 10 ** 8 - 1)
        charges = float(np.round(np.exp(r.normal(7.75, 1.05)), 2)) + 85.0
        paid = float(np.round(charges * r.uniform(0.40, 0.85), 2)) if r.random() < 0.55 else 0.0
        bal = round(max(charges - paid, 25.0 + float(r.uniform(0, 40))), 2)
        accs.append(dict(account=num, code=code, guarantor=guarantor,
                         service=received - dt.timedelta(days=int(r.integers(35, 120))),
                         charges=round(bal + paid, 2), balance=bal, open=bal))
    return accs


def user_on(cid, c, code, d):
    return cid[c][0] if (code != K.MIGRATED or d < K.MIGRATION) else cid[c][1]


def build(hs, seed=W.SEED):
    """Every extract row, application, account, ledger line and crosswalk entry, from the decided world."""
    r = np.random.default_rng([seed, 99])
    ids = Ids(r)
    rows, apps, accounts = [], {}, {}
    cw_couns, cw_guar = [], []
    for h in hs:
        code = h["code"]
        rh = np.random.default_rng([seed, int(code[1:]), 7])
        n25 = sum(1 for a in h["apps"] if a.get("decided") and a["decided"].year == 2025)
        C = int(np.clip(round(n25 / 1300.0), 2, 9))
        cid = counsellor_ids(ids, code, C)
        h["counsellor_ids"] = cid
        if code == K.MIGRATED:
            for a_, b_ in cid:
                cw_couns.append(dict(code=code, old=a_, new=b_, effective=K.MIGRATION))
        guar = {}                      # household -> (id in its first hub, id after the migration)
        case_app = {}                  # case -> the application number the case was opened under
        case_accts = {}                # case -> its accounts
        for a in sorted(h["apps"], key=lambda x: (x["received"], x["hh"])):
            hub0 = hub_on(code, a["received"])
            if a["hh"] not in guar:
                g0 = guarantor_id(ids, K.HUB[code])
                g1 = guarantor_id(ids, "puget") if code == K.MIGRATED else None
                guar[a["hh"]] = (g0, g1)
                if g1:
                    cw_guar.append(dict(code=code, old=g0, new=g1, effective=K.MIGRATION))
            if a["status"] == "after":
                continue
            decided = a.get("decided")
            when_day = decided or W.working(a["received"] + dt.timedelta(days=int(rh.integers(5, 31))))
            if when_day.year > 2025:
                continue
            hub = hub_on(code, when_day)
            g = guar[a["hh"]][0] if (code != K.MIGRATED or when_day < K.MIGRATION) else guar[a["hh"]][1]
            num = app_id(ids, code, hub0, False, a["received"])
            if a["case"] not in case_accts:
                case_accts[a["case"]] = accounts_for(rh, ids, code, g, a["received"],
                                                     int(rh.choice(N_ACC[0], p=N_ACC[1])))
                case_app[a["case"]] = num
                for x in case_accts[a["case"]]:
                    accounts[x["account"]] = x
            accs = case_accts[a["case"]]
            c = int(rh.integers(C))
            base = dict(code=code, app=num, guarantor=g, size=a["size"], kind=a["kind"], received=a["received"],
                        inc3=a["inc3"])
            if decided is None:
                rows.append(dict(base, hub=hub, when=clock(when_day, rh), user=user_on(cid, c, code, when_day),
                                 type="INITIAL", outcome="withdraw", tier=None, reason=None))
                continue
            if rh.random() < PEND_P:
                pd_ = W.working(decided - dt.timedelta(days=int(rh.integers(4, 26))))
                if pd_ > a["received"] and pd_ < decided:
                    rows.append(dict(base, hub=hub_on(code, pd_), when=clock(pd_, rh), user=user_on(cid, c, code, pd_),
                                     guarantor=guar[a["hh"]][0] if (code != K.MIGRATED or pd_ < K.MIGRATION)
                                     else guar[a["hh"]][1], type="INITIAL", outcome="pend", tier=None, reason=None))
            user = user_on(cid, c, code, decided)
            rows.append(dict(base, hub=hub, when=clock(decided, rh), user=user, type="INITIAL", outcome=a["outcome"],
                             tier=a["tier"] if a["outcome"] == "approve" else None, reason=a["reason"]))
            apps[num] = dict(code=code, guarantor=g, hh=a["hh"], case=a["case"], case_app=case_app[a["case"]],
                             accounts=[x["account"] for x in accs], source="counsellor", outcome=a["outcome"],
                             tier=a["tier"], decided=decided, type="INITIAL", reason=a["reason"])
            # a documents denial reconsidered once the documents arrive
            if a["reason"] == "INCOMPLETE" and rh.random() < RECON_P:
                rd = W.working(decided + dt.timedelta(days=int(rh.integers(7, 61))))
                if rd.year <= 2025:
                    c2 = int(rh.integers(C))
                    if rh.random() < 0.10:
                        out, tier, reason = "deny", None, "INCOMPLETE"
                    elif a["tier_policy"] > 0:
                        out, tier, reason = "approve", a["tier_policy"], None
                    else:
                        out, tier, reason = "deny", None, "OVER_INCOME"
                    g2 = guar[a["hh"]][0] if (code != K.MIGRATED or rd < K.MIGRATION) else guar[a["hh"]][1]
                    rows.append(dict(base, hub=hub_on(code, rd), when=clock(rd, rh), user=user_on(cid, c2, code, rd),
                                     guarantor=g2, type="RECON", outcome=out, tier=tier, reason=reason))
                    if out == "approve":
                        apps[num].update(outcome="approve", tier=tier, decided=rd, type="RECON", reason=None)
    _presumptive(r, ids, hs, rows, apps, accounts)
    ledger = _ledger(np.random.default_rng([seed, 99, LEDGER_SALT]), apps, accounts)
    return dict(rows=rows, apps=apps, accounts=accounts, ledger=ledger, crosswalk=cw_couns, guarantor_crosswalk=cw_guar)


def _presumptive(r, ids, hs, rows, apps, accounts):
    """The nightly presumptive screening: approvals in full under each hub's system user, 2024 and 2025."""
    d, nights = dt.date(2024, 1, 2), []
    while d.year <= 2025:
        if d.weekday() < 5 and d not in K.HOLIDAYS_ALL:
            nights.append(d)
        d += dt.timedelta(days=1)
    lam = {h["code"]: float(r.uniform(0.8, 2.5)) for h in hs}
    for night in nights:
        for h in hs:
            code = h["code"]
            hub = hub_on(code, night)
            for _ in range(int(r.poisson(lam[code]))):
                g = guarantor_id(ids, hub)
                a = app_id(ids, code, hub, True, night)
                accs = accounts_for(r, ids, code, g, night, int(r.choice([1, 2, 3], p=[0.72, 0.21, 0.07])))
                for x in accs:
                    accounts[x["account"]] = x
                apps[a] = dict(code=code, guarantor=g, accounts=[x["account"] for x in accs], source="presumptive",
                               outcome="approve", tier=100, decided=night, case_app=a, type="PRESUMPTIVE")
                when = dt.datetime.combine(night, dt.time(2, 10)) + dt.timedelta(seconds=int(r.integers(0, 1800)))
                rows.append(dict(code=code, hub=hub, when=when, user=K.SYSTEM_USER[hub], app=a, guarantor=g,
                                 type="PRESUMPTIVE", outcome="approve", tier=100, reason=None, size=None, kind=None,
                                 received=night, inc3=None))


def _ledger(r, apps, accounts):
    """Write-off lines (FAWO), one per account an approval covers, each at the approval's whole write-off, posted under
    the number the case was opened with; reversal lines (FAWR) on one account at that account's own write-off when
    Medicaid later paid it. The file holds every line posted from 1 January 2025 to the extract's cut."""
    lines = []
    for a in sorted(apps, key=lambda k: (apps[k]["decided"], k)):
        x = apps[a]
        if x.get("outcome") != "approve":
            continue
        own = {}
        for acc in x["accounts"]:
            v = round(accounts[acc]["open"] * x["tier"] / 100.0, 2)
            own[acc] = v
            accounts[acc]["open"] = round(accounts[acc]["open"] - v, 2)
        total = round(sum(own.values()), 2)
        x["writeoff"] = total
        x["own"] = own
        posted = bday_add(x["decided"], int(r.integers(1, 4)))
        post_as = x["case_app"]
        for acc in x["accounts"]:
            if own[acc] > 0:
                lines.append(dict(code=x["code"], app=post_as, account=acc, posted=posted, kind="FAWO", amount=total))
        if total > 0 and r.random() < 0.05:
            rev = [acc for acc in x["accounts"] if own[acc] > 0]
            r.shuffle(rev)
            for acc in rev[:int(r.integers(1, min(2, len(rev)) + 1))]:
                p2 = posted + dt.timedelta(days=int(r.integers(30, 151)))
                if p2 <= K.EXTRACT_CUT:
                    lines.append(dict(code=x["code"], app=post_as, account=acc, posted=p2, kind="FAWR", amount=own[acc]))
                    x["reversed"] = round(x.get("reversed", 0.0) + own[acc], 2)
    lines = [t for t in lines if dt.date(2025, 1, 1) <= t["posted"] <= K.EXTRACT_CUT]
    lines.sort(key=lambda t: (t["posted"], t["code"], t["app"], t["account"], t["kind"]))
    for i, t in enumerate(lines):
        t["id"] = "FA%09d" % (300000000 + 7 * i + int(r.integers(0, 7)))
    return lines
