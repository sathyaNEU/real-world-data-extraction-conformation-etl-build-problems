"""Households, landlords, merges, priority register; appointment rows, credits and complaints."""
import datetime as dt
from collections import Counter, defaultdict

import numpy as np

from sample import FAMILY
from world import BANK_HOLIDAYS, END, EXTRACT, MERGE_DAY, START, patch_of

D = dt.date


def nth_working_day(year, month, n):
    d = D(year, month, 1)
    k = 0
    while True:
        if d.weekday() < 5 and d not in BANK_HOLIDAYS:
            k += 1
            if k == n:
                return d
        d += dt.timedelta(days=1)


def run_date_for(visit):
    y, m = (visit.year + 1, 1) if visit.month == 12 else (visit.year, visit.month + 1)
    return nth_working_day(y, m, 2)


def build_accounts(W, seed=111):
    rng = np.random.default_rng([seed, 3])
    used = set()

    def new_ref():
        while True:
            r = "HC%07d" % int(rng.integers(1200000, 9899999))
            if r not in used:
                used.add(r)
                return r

    W.households = {}
    W.by_district = defaultdict(list)
    for dist in W.districts:
        n = int(1900 * W.dweight[dist] / 1.0 * 0.55)
        for _ in range(n):
            ref = new_ref()
            h = {"ref": ref, "district": dist, "opened": D(int(rng.integers(2009, 2025)), int(rng.integers(1, 13)),
                                                          int(rng.integers(1, 28))),
                 "plan": ["Boiler & heating", "Boiler, heating & plumbing", "Plumbing & drains"][
                     int(rng.choice(3, p=[0.46, 0.44, 0.10]))],
                 "landlord": None, "psr_from": None, "cancelled": None, "dup": None}
            if rng.random() < 0.12:
                h["psr_from"] = D(int(rng.integers(2016, 2026)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
                if h["psr_from"] > D(2026, 9, 1):
                    h["psr_from"] = D(2026, 5, 11)
            W.households[ref] = h
            W.by_district[dist].append(ref)
    # landlords: each holds 3 to 14 properties in nearby districts
    W.landlords = {}
    allrefs = list(W.households)
    rng.shuffle(allrefs)
    pool = allrefs[: int(0.15 * len(allrefs))]
    i = 0
    while i < len(pool):
        k = int(rng.integers(3, 15))
        lref = new_ref()
        props = pool[i:i + k]
        W.landlords[lref] = {"ref": lref, "props": props,
                             "district": W.households[props[0]]["district"],
                             "opened": D(int(rng.integers(2010, 2024)), int(rng.integers(1, 13)), 1)}
        for p in props:
            W.households[p]["landlord"] = lref
        i += k
    # duplicate accounts merged on MERGE_DAY
    for ref in allrefs[int(0.15 * len(allrefs)): int(0.15 * len(allrefs)) + int(0.035 * len(allrefs))]:
        dref = new_ref()
        W.households[ref]["dup"] = dref
    # cancellations
    for ref in allrefs[-int(0.06 * len(allrefs)):]:
        W.households[ref]["cancelled"] = START + dt.timedelta(days=int(rng.integers(20, (END - START).days + 5)))
    W.dup_of = {h["dup"]: h["ref"] for h in W.households.values() if h["dup"]}
    return W


def assign_households(W, seed=111):
    """Give every routed job a household; a few consecutive jobs are a second visit at the same address."""
    rng = np.random.default_rng([seed, 4])
    W.appointments = []
    seq = int(rng.integers(30000000, 31000000))
    for r in W.day_records:
        d = r["date"]
        prev = None
        for k, (j, a) in enumerate(zip(r["jobs"], r["acts"])):
            if prev is not None and rng.random() < 0.08 and prev["district"] == j["district"]:
                h = prev["hh"]
            else:
                cand = W.by_district[j["district"]]
                for _ in range(20):
                    h = cand[int(rng.integers(len(cand)))]
                    c = W.households[h]["cancelled"]
                    if c is None or c > d:
                        break
            hh = W.households[h]
            acct = hh["ref"]
            if hh["dup"] and d < MERGE_DAY and rng.random() < 0.5:
                acct = hh["dup"]
            lead = int(rng.integers(1, 6)) if j["job_type"] != "Annual service" else int(rng.integers(7, 43))
            booked_on = d - dt.timedelta(days=lead)
            seq += int(rng.integers(1, 9))
            rec = {"appointment_ref": "J%08d" % seq, "booked_on": booked_on, "account_ref": acct, "hh": h,
                   "district": j["district"], "stored_patch": patch_of(j["district"], booked_on),
                   "engineer_id": r["engineer_id"], "date": d, "window": j["window"], "job_type": j["job_type"],
                   "booked": j["booked"], "ptravel": j["ptravel"], "arr_plan": j["arr_plan"],
                   "status": "No access" if j.get("no_access") else "Completed", "en_route": a["en_route"],
                   "arr": a["arr"], "start": a["start"], "dep": a["dep"], "travel_type": a["travel_type"],
                   "missed": k in r["missed"], "day": r, "k": k}
            W.appointments.append(rec)
            prev = {"hh": h, "district": j["district"]}
    # no landlord with two different properties missed on one date (keeps credit lines one-to-one)
    seen = {}
    for a in W.appointments:
        if not a["missed"]:
            continue
        lref = W.households[a["hh"]]["landlord"]
        if not lref:
            continue
        key = (lref, a["date"])
        if key in seen and seen[key] != a["hh"]:
            # re-home this visit to a household with no landlord in the same district
            cand = [x for x in W.by_district[a["district"]] if not W.households[x]["landlord"]
                    and not W.households[x]["dup"] and (W.households[x]["cancelled"] is None or
                                                         W.households[x]["cancelled"] > a["date"])]
            h = cand[int(rng.integers(len(cand)))]
            a["hh"] = h
            a["account_ref"] = h
        else:
            seen[key] = a["hh"]
    # customer-side cancellations and rebooks: rows that never reached a route
    extra = []
    for a in W.appointments:
        if rng.random() < 0.046:
            seq += int(rng.integers(1, 9))
            st = "Cancelled by customer" if rng.random() < 0.66 else "Rebooked by customer"
            extra.append({"appointment_ref": "J%08d" % seq, "booked_on": a["booked_on"],
                          "account_ref": a["account_ref"], "hh": a["hh"], "district": a["district"],
                          "stored_patch": a["stored_patch"], "engineer_id": a["engineer_id"], "date": a["date"],
                          "window": a["window"], "job_type": a["job_type"], "booked": a["booked"],
                          "ptravel": None, "arr_plan": None, "status": st, "en_route": None, "arr": None,
                          "start": None, "dep": None, "travel_type": "", "missed": False, "day": None, "k": None})
    W.appointments += extra
    return W




# ------------------------------------------------------------------------------------------------ the ask-path layer
Q3_FROM, Q3_TO = D(2026, 7, 1), D(2026, 9, 30)
PLATFORM_MOVE = D(2026, 9, 1)       # complaints move to the new platform; its category list applies from here
NEW_CATEGORY = {"Missed appointment": "Appointments - arrival window", "Repair not fixed": "Repairs - not fixed",
                "Engineer conduct": "Engineers - conduct", "Billing": "Billing - charges",
                "Cover terms": "Cover - terms and renewals"}
MISSED_LABELS = ("Missed appointment", NEW_CATEGORY["Missed appointment"])
# letting agents holding cover for a whole UK portfolio on one landlord account: (office district, districts
# their Scottish properties sit in, Scottish properties, attendances a working day in the other regions)
PORTFOLIOS = [
    ("G12", ["G11", "G12", "G13", "G14", "G20", "G21", "G22", "G31", "G32", "G33", "G40", "G41", "G42", "G43",
             "G44", "G51", "G52"], 2600, 1.5),
    ("EH3", ["EH3", "EH4", "EH5", "EH6", "EH7", "EH8", "EH9", "EH10", "EH11", "EH12", "EH13", "EH14", "EH15",
             "EH16", "EH17"], 2000, 1.2),
    ("G41", ["G11", "G12", "G20", "G31", "G41", "G51", "EH3", "EH6", "EH7", "EH11", "PA1", "PA2", "ML1", "ML3",
             "KY1", "KY2"], 1600, 2.4),
]


def label_on(cat, when):
    """The category as the complaints platform in use on that day records it."""
    return NEW_CATEGORY[cat] if when.date() >= PLATFORM_MOVE else cat


def missed_hh_days(W):
    """Missed household-days (household, visit date) -> the missed appointments that day."""
    out = defaultdict(list)
    for a in W.appointments:
        if a["missed"]:
            out[(a["hh"], a["date"])].append(a)
    return out


def family_of_hh_day(W):
    return {k: FAMILY[v[0]["day"]["event"][0]] for k, v in missed_hh_days(W).items()}


def _stable_psr(h):
    return h["psr_from"] is None or h["psr_from"] <= D(2025, 6, 30)


def portfolio_landlords(W, seed=111):
    """Three letting agents hold the cover for whole portfolios on one landlord account each. Their Scottish
    properties are let households in the extract; the rest of each portfolio sits in the other regions, and the
    company-wide ledger carries those properties' credits on the same account."""
    rng = np.random.default_rng([seed, 10])
    used = set(W.households) | set(W.landlords) | set(W.dup_of)

    def new_ref():
        while True:
            r = "HC%07d" % int(rng.integers(1200000, 9899999))
            if r not in used:
                used.add(r)
                return r

    def eligible(h):
        x = W.households[h]
        return x["landlord"] is None and x["dup"] is None and x["cancelled"] is None and _stable_psr(x)

    W.portfolio = {}
    taken = set()
    for office, dists, n, rate in PORTFOLIOS:
        pool = sorted(h for dd in dists for h in W.by_district[dd] if eligible(h) and h not in taken)
        pick = sorted(int(i) for i in rng.choice(len(pool), n, replace=False))
        props = [pool[i] for i in pick]
        taken.update(props)
        lref = new_ref()
        W.portfolio[lref] = {"ref": lref, "props": props, "district": office, "rate": rate,
                             "opened": D(int(rng.integers(2014, 2020)), int(rng.integers(1, 13)), 1)}
    order = list(W.portfolio)
    fam = family_of_hh_day(W)
    q3 = sorted(k for k in fam if Q3_FROM <= k[1] <= Q3_TO)
    owner = {h: l for l in order for h in W.portfolio[l]["props"]}
    # every cause family carries let days on these accounts, and at least two days on which one agent had two
    # Scottish properties missed, the family's household the later of the two on the account
    for f in sorted(set(fam.values())):
        mine = [k for k in q3 if fam[k] == f]
        held = [k for k in mine if k[0] in owner]
        free = [k for k in mine if k[0] not in owner and eligible(k[0])]
        while len(held) < 4 and free:
            k = free.pop(int(rng.integers(len(free))))
            l = order[int(rng.integers(len(order)))]
            W.portfolio[l]["props"].append(k[0])
            owner[k[0]] = l
            held.append(k)
        multi = 0
        for k in held:
            l = owner[k[0]]
            if any(o[1] == k[1] and o[0] != k[0] and owner.get(o[0]) == l and o[0] < k[0] for o in q3):
                multi += 1
        tries = [k for k in held]
        rng.shuffle(tries)
        for k in tries:
            if multi >= 2:
                break
            l = owner[k[0]]
            mates = [o for o in q3 if o[1] == k[1] and o[0] < k[0] and o[0] not in owner and eligible(o[0])]
            if not mates:
                continue
            o = mates[int(rng.integers(len(mates)))]
            W.portfolio[l]["props"].append(o[0])
            owner[o[0]] = l
            multi += 1
    # and a let household on the priority register, whose credit is the 50-pound line among the agent's lines
    for f in sorted(set(fam.values())):
        mine = [k for k in q3 if fam[k] == f]
        if any(k[0] in owner and W.households[k[0]]["psr_from"] for k in mine):
            continue
        pool = [k for k in mine if k[0] not in owner and W.households[k[0]]["landlord"] is None
                and W.households[k[0]]["dup"] is None and W.households[k[0]]["cancelled"] is None
                and W.households[k[0]]["psr_from"] is not None and W.households[k[0]]["psr_from"] <= D(2025, 6, 30)]
        if pool:
            k = pool[int(rng.integers(len(pool)))]
            l = order[int(rng.integers(len(order)))]
            W.portfolio[l]["props"].append(k[0])
            owner[k[0]] = l
    for l, p in W.portfolio.items():
        for h in p["props"]:
            W.households[h]["landlord"] = l
        W.landlords[l] = {"ref": l, "props": p["props"], "district": p["district"], "opened": p["opened"],
                          "portfolio": True}
    W.portfolio_props = set(owner)
    return W


def priority_joiners(W, seed=111):
    """Households an engineer put on the priority services register in the days after a missed visit, before the
    goodwill run for it."""
    rng = np.random.default_rng([seed, 11])
    fam = family_of_hh_day(W)
    hd = missed_hh_days(W)
    q3 = sorted(k for k in fam if Q3_FROM <= k[1] <= Q3_TO)
    per = Counter(fam[k] for k in q3)
    W.joiners = set()
    for f in sorted(per):
        cand = [k for k in q3 if fam[k] == f and k[0] not in W.portfolio_props
                and W.households[k[0]]["psr_from"] is None and W.households[k[0]]["dup"] is None
                and W.households[k[0]]["cancelled"] is None and k[0] not in W.joiners
                and all(a["status"] == "Completed" for a in hd[k])]
        n = max(1, int(round(0.04 * per[f])))
        for i in sorted(int(x) for x in rng.choice(len(cand), min(n, len(cand)), replace=False)):
            h, d = cand[i]
            run = run_date_for(d)
            W.households[h]["psr_from"] = d + dt.timedelta(days=int(rng.integers(1, min(14, (run - d).days) + 1)))
            W.joiners.add(h)
    return W


def _received(rng, d, lo=1, hi=10):
    return dt.datetime(d.year, d.month, d.day, 9, 0) + dt.timedelta(days=int(rng.integers(lo, hi)),
                                                                    minutes=int(rng.integers(0, 540)))


def _closed(rng, recv):
    return recv + dt.timedelta(days=2 + int(rng.gamma(2.0, 9.5)), hours=int(rng.integers(0, 9)))


class Cases:
    """Complaint cases and their entries. A case is one complaint; each contact on it is an entry. A complaint
    closed on the old platform and reopened after the move is opened on the new platform as a new case."""

    def __init__(self, survivor=None):
        self.entries = []
        self.n = 0
        self.survivor = survivor or {}

    def new(self):
        self.n += 1
        return self.n

    def log(self, rng, acct, recv, channel, cat, about, hh, close=None, reopen=None, scot=True, reopen_acct=None):
        case = self.new()
        if close is None:
            close = _closed(rng, recv)
        st = "Closed" if close.date() <= EXTRACT else "Open"
        carried = recv.date() < PLATFORM_MOVE <= close.date()
        entry = {"case": case, "account_ref": acct, "received": recv, "channel": channel,
                 "category": label_on(cat, recv), "about_visit_date": about, "status": "Open" if carried else st,
                 "hh": hh, "scot": scot}
        self.entries.append(entry)
        cur = case
        if carried:
            # open at the move: the new platform took the record across under its own reference, and the old
            # platform's copy stays as it stood on the day
            cur = self.new()
            self.entries.append(dict(entry, case=cur, status=st))
        if reopen is not None and st == "Closed" and close < reopen and reopen.date() <= EXTRACT:
            rcase = cur
            if close.date() < PLATFORM_MOVE <= reopen.date():
                rcase = self.new()
            acct = reopen_acct or acct
            if acct in self.survivor and reopen.date() >= MERGE_DAY:
                acct = self.survivor[acct]
            self.entries.append({"case": rcase, "account_ref": acct, "received": reopen, "channel": "Phone",
                                 "category": label_on(cat, reopen), "about_visit_date": about, "status": "Reopened",
                                 "hh": hh, "scot": scot})
        return case


CHANNELS = (["Phone", "Email", "Web form"], [0.6, 0.25, 0.15])


def credits_and_complaints(W, seed=111):
    rng = np.random.default_rng([seed, 5])
    W.credits = []
    hh_days = missed_hh_days(W)
    protected = W.portfolio_props | W.joiners
    # some households cancel their cover within a few weeks of a missed visit
    last_visit = {}
    for a in W.appointments:
        if a["date"] > last_visit.get(a["hh"], D(2000, 1, 1)):
            last_visit[a["hh"]] = a["date"]
    for (h, d) in sorted(hh_days, key=lambda x: (x[1], x[0])):
        hh = W.households[h]
        u, gap = rng.random(), int(rng.integers(3, 26))
        if h in protected:
            continue
        if hh["cancelled"] is None and last_visit[h] == d and u < 0.09:
            c = d + dt.timedelta(days=gap)
            if c <= EXTRACT:
                hh["cancelled"] = c
    # goodwill: one credit per household per visit day to the account that pays for the cover; the run reads
    # the priority register as it stands on the run date
    for (h, d), apps in sorted(hh_days.items(), key=lambda x: (x[0][1], x[0][0])):
        hh = W.households[h]
        run = run_date_for(d)
        if run > EXTRACT:
            continue
        if hh["cancelled"] and hh["cancelled"] <= run:
            continue
        acct = apps[0]["account_ref"]
        if hh["dup"] and run >= MERGE_DAY:
            acct = hh["ref"]
        psr = hh["psr_from"] is not None and hh["psr_from"] <= run
        W.credits.append({"account_ref": hh["landlord"] or acct, "visit_date": d, "run_date": run, "reason": "MA",
                          "amount": 50 if psr else 30, "hh": h})
    comp = [a for a in W.appointments if a["status"] == "Completed" and not a["missed"]]
    for _ in range(int(0.22 * len(W.credits))):
        a = comp[int(rng.integers(len(comp)))]
        run = run_date_for(a["date"])
        if run > EXTRACT:
            continue
        hh = W.households[a["hh"]]
        W.credits.append({"account_ref": hh["landlord"] or a["account_ref"], "visit_date": a["date"],
                          "run_date": run, "reason": ["RV", "CG"][int(rng.integers(2))],
                          "amount": [20, 25, 40][int(rng.integers(3))], "hh": a["hh"]})
    W.cases = Cases(dict(W.dup_of))
    _scottish_complaints(W, seed, hh_days, comp)
    _settle_complaints(W, seed, hh_days)
    _other_regions(W, seed)
    _number(W, seed)
    _settle_credits(W, seed)
    return W


def _logger(W, rng, hh, apps, recv, who):
    if who == "landlord":
        return hh["landlord"]
    acct = apps[0]["account_ref"] if apps else hh["ref"]
    if hh["dup"] and recv.date() >= MERGE_DAY:
        acct = hh["ref"]
    return acct


def _scottish_complaints(W, seed, hh_days, comp):
    rng = np.random.default_rng([seed, 13])
    C = W.cases
    lands = {l for l in W.landlords if not W.landlords[l].get("portfolio")}
    complained = set()
    for (h, d), apps in sorted(hh_days.items(), key=lambda x: (x[0][1], x[0][0])):
        hh = W.households[h]
        psr = hh["psr_from"] is not None and hh["psr_from"] <= d
        if rng.random() >= (0.26 if psr else 0.17):
            continue
        recv = _received(rng, d)
        who = "landlord" if (hh["landlord"] in lands and rng.random() < 0.55) else "household"
        ch = CHANNELS[0][int(rng.choice(3, p=CHANNELS[1]))]
        close = _closed(rng, recv)
        reopen = close + dt.timedelta(days=int(rng.integers(2, 26)), hours=int(rng.integers(0, 8))) \
            if rng.random() < 0.06 else None
        if recv.date() > EXTRACT:
            continue
        C.log(rng, _logger(W, rng, hh, apps, recv, who), recv, ch, "Missed appointment", d, h, close, reopen)
        complained.add((h, d))
    _forced(W, seed, hh_days, complained)
    # complaints about visits we kept: the customer's view of late is not always the window's
    land_days = {(W.households[h]["landlord"], d) for (h, d) in hh_days if W.households[h]["landlord"]}
    missed = set(hh_days)
    kept = [a for a in comp if (a["hh"], a["date"]) not in missed]
    n_scot = len({e["case"] for e in C.entries})
    for _ in range(int(0.11 * n_scot)):
        a = kept[int(rng.integers(len(kept)))]
        hh = W.households[a["hh"]]
        recv = _received(rng, a["date"], 1, 8)
        if recv.date() > EXTRACT:
            continue
        acct = _logger(W, rng, hh, [a], recv, "household")
        if hh["landlord"] in lands and (hh["landlord"], a["date"]) not in land_days and rng.random() < 0.4:
            acct = hh["landlord"]
        C.log(rng, acct, recv, CHANNELS[0][int(rng.choice(3, p=CHANNELS[1]))], "Missed appointment", a["date"],
              a["hh"])
    # texture: complaints for other reasons, never on a day the household was missed
    for _ in range(int(1.1 * n_scot)):
        a = kept[int(rng.integers(len(kept)))]
        recv = _received(rng, a["date"], 1, 12)
        if recv.date() > EXTRACT:
            continue
        cat = ["Repair not fixed", "Engineer conduct", "Billing", "Cover terms"][int(rng.choice(4, p=[0.45, 0.15,
                                                                                                       0.25, 0.15]))]
        hh = W.households[a["hh"]]
        reopen = None
        close = _closed(rng, recv)
        if rng.random() < 0.05:
            reopen = close + dt.timedelta(days=int(rng.integers(2, 26)))
        C.log(rng, _logger(W, rng, hh, [a], recv, "household"), recv,
              ["Phone", "Email", "Web form"][int(rng.integers(3))], cat,
              a["date"] if cat in ("Repair not fixed", "Engineer conduct") else None, a["hh"], close, reopen)


def _forced(W, seed, hh_days, complained):
    """Every cause family carries each kind of complaint record the log holds: a let household where tenant and
    landlord both complained, a landlord's complaint, a complaint closed before the platform move and reopened
    after it, a complaint about a late-September visit received in October, and a reopened complaint."""
    rng = np.random.default_rng([seed, 14])
    C = W.cases
    fam = family_of_hh_day(W)
    lands = {l for l in W.landlords if not W.landlords[l].get("portfolio")}
    q3 = sorted(k for k in fam if Q3_FROM <= k[1] <= Q3_TO and k not in complained)
    W.forced = defaultdict(list)

    def take(pool):
        if not pool:
            return None
        k = pool[int(rng.integers(len(pool)))]
        q3.remove(k)
        return k

    for f in sorted(set(fam[k] for k in q3)):
        let = lambda: [k for k in q3 if fam[k] == f and W.households[k[0]]["landlord"] in lands]
        k = take([k for k in let() if k[1] <= D(2026, 8, 10)])
        if k:
            _kind(W, rng, hh_days, k, "moved_landlord")
            W.forced[f].append(("moved_landlord", k))
        k = take(let())
        if k:
            _kind(W, rng, hh_days, k, "pair")
            W.forced[f].append(("pair", k))
        for kind, pool in (("moved", [k for k in q3 if fam[k] == f and k[1] <= D(2026, 8, 10)]),
                           ("carried", [k for k in q3 if fam[k] == f and D(2026, 7, 20) <= k[1] <= D(2026, 8, 21)]),
                           ("october", [k for k in q3 if fam[k] == f and k[1] >= D(2026, 9, 22)])):
            k = take(pool)
            if k:
                _kind(W, rng, hh_days, k, kind)
                W.forced[f].append((kind, k))
    return W


def _kind(W, rng, hh_days, k, kind):
    """Write one complaint record of a given kind about the missed household-day k."""
    C = W.cases
    h, d = k
    hh, apps = W.households[h], hh_days[k]
    tenant = lambda r: _logger(W, rng, hh, apps, r, "household")
    move = dt.datetime(2026, 9, 1, 9, 0)
    if kind == "pair":                                   # the tenant and the landlord both complained
        r1 = _received(rng, d, 1, 5)
        C.log(rng, tenant(r1), r1, "Phone", "Missed appointment", d, h)
        r2 = _received(rng, d, 2, 9)
        C.log(rng, hh["landlord"], r2, "Email", "Missed appointment", d, h)
    elif kind == "landlord":                             # the landlord complained
        r = _received(rng, d, 1, 8)
        C.log(rng, hh["landlord"], r, ["Phone", "Email"][int(rng.integers(2))], "Missed appointment", d, h)
    elif kind in ("moved", "moved_landlord"):            # closed before the move, reopened after it
        r = _received(rng, d, 1, 4)
        close = max(min(r + dt.timedelta(days=int(rng.integers(4, 14))), dt.datetime(2026, 8, 28, 16, 0)),
                    r + dt.timedelta(days=2))
        reopen = move + dt.timedelta(days=int(rng.integers(0, 22)), minutes=int(rng.integers(0, 480)))
        C.log(rng, tenant(r), r, ["Phone", "Email"][int(rng.integers(2))], "Missed appointment", d, h, close, reopen,
              reopen_acct=hh["landlord"] if kind == "moved_landlord" else None)
    elif kind == "carried":                              # still open on the day of the move
        r = _received(rng, d, 1, 9)
        close = move + dt.timedelta(days=int(rng.integers(1, 40)), hours=int(rng.integers(0, 8)))
        C.log(rng, tenant(r), r, ["Phone", "Email", "Web form"][int(rng.integers(3))], "Missed appointment", d, h,
              close)
    elif kind == "october":                              # received in October, still open at the pull
        r = dt.datetime(2026, 10, 1, 9, 0) + dt.timedelta(days=int(rng.integers(0, 5)),
                                                          minutes=int(rng.integers(0, 480)))
        C.log(rng, tenant(r), r, ["Phone", "Web form"][int(rng.integers(2))], "Missed appointment", d, h,
              r + dt.timedelta(days=int(rng.integers(8, 30))))
    else:
        raise ValueError(kind)


def _other_regions(W, seed):
    """The ledger and the complaints log are company-wide: the other regions' lines ride alongside, and the
    letting agents' properties in the other regions are credited to the same landlord accounts."""
    orng = np.random.default_rng([seed, 9])
    taken = set(W.households) | set(W.landlords) | set(W.dup_of)

    def other_ref():
        while True:
            r = "HC%07d" % int(orng.integers(1200000, 9899999))
            if r not in taken:
                taken.add(r)
                return r
    oaccts = [other_ref() for _ in range(60000)]
    runs = sorted({c["run_date"] for c in W.credits})
    scot = defaultdict(int)
    for c in W.credits:
        scot[c["run_date"]] += 1
    for run in runs:
        n = int(scot[run] * orng.uniform(4.2, 5.4))
        y, m = (run.year - 1, 12) if run.month == 1 else (run.year, run.month - 1)
        last = (D(run.year, run.month, 1) - dt.timedelta(days=1)).day
        for _ in range(n):
            vd = D(y, m, int(orng.integers(1, last + 1)))
            while vd.weekday() >= 5:
                vd = D(y, m, int(orng.integers(1, last + 1)))
            reason = "MA" if orng.random() < 0.82 else ["RV", "CG"][int(orng.integers(2))]
            amt = (50 if orng.random() < 0.13 else 30) if reason == "MA" else [20, 25, 40][int(orng.integers(3))]
            W.credits.append({"account_ref": oaccts[int(orng.integers(len(oaccts)))], "visit_date": vd,
                              "run_date": run, "reason": reason, "amount": amt, "hh": None})
    # the letting agents' attendances elsewhere in the UK
    prng = np.random.default_rng([seed, 12])
    d = START
    while d <= END:
        if d.weekday() < 5:
            run = run_date_for(d)
            if run <= EXTRACT:
                season = 1.25 if d.month in (11, 12, 1, 2) else 1.0
                for l, p in W.portfolio.items():
                    for _ in range(int(prng.poisson(p["rate"] * season))):
                        W.credits.append({"account_ref": l, "visit_date": d, "run_date": run, "reason": "MA",
                                          "amount": 50 if prng.random() < 0.13 else 30, "hh": None})
                    if prng.random() < 0.06:
                        W.credits.append({"account_ref": l, "visit_date": d, "run_date": run,
                                          "reason": ["RV", "CG"][int(prng.integers(2))],
                                          "amount": [20, 25, 40][int(prng.integers(3))], "hh": None})
        d += dt.timedelta(days=1)
    C = W.cases
    nq = int(len({e["case"] for e in C.entries}) * 5.1)
    for _ in range(nq):
        recv = dt.datetime(2025, 7, 2, 9, 0) + dt.timedelta(days=int(orng.integers(0, (EXTRACT - D(2025, 7, 2)).days)),
                                                           minutes=int(orng.integers(0, 600)))
        cat = ["Missed appointment", "Repair not fixed", "Engineer conduct", "Billing", "Cover terms"][
            int(orng.choice(5, p=[0.3, 0.3, 0.1, 0.18, 0.12]))]
        about = None
        if cat in ("Missed appointment", "Repair not fixed", "Engineer conduct"):
            about = (recv - dt.timedelta(days=int(orng.integers(1, 10)))).date()
            while about.weekday() >= 5:
                about -= dt.timedelta(days=1)
        close = _closed(orng, recv)
        reopen = close + dt.timedelta(days=int(orng.integers(2, 26))) if orng.random() < 0.05 else None
        C.log(orng, oaccts[int(orng.integers(len(oaccts)))], recv, ["Phone", "Email", "Web form"][int(orng.integers(3))],
              cat, about, None, close, reopen, scot=False)


def _number(W, seed):
    """Reference numbers: credits numbered as each run posts, complaints in the order they were opened."""
    rng = np.random.default_rng([seed, 15])
    out = []
    ref = int(rng.integers(5104000, 5110000))
    for run in sorted({c["run_date"] for c in W.credits}):
        batch = [c for c in W.credits if c["run_date"] == run]
        batch.sort(key=lambda c: (c["account_ref"], c["visit_date"], c["reason"], c["amount"]))
        for i in rng.permutation(len(batch)):
            ref += int(rng.integers(1, 4))
            c = batch[int(i)]
            c["credit_ref"] = "GC%07d" % ref
            out.append(c)
        ref += int(rng.integers(40, 400))
    W.credits = sorted(out, key=lambda c: (c["run_date"], c["credit_ref"]))
    first = {}
    for e in W.cases.entries:
        if e["case"] not in first or e["received"] < first[e["case"]]:
            first[e["case"]] = e["received"]
    num, q = {}, int(rng.integers(61000, 62000))
    for case in sorted(first, key=lambda c: (first[c], c)):
        q += int(rng.integers(1, 4))
        num[case] = "CMP-%06d" % q
    W.complaints = []
    for e in W.cases.entries:
        e["complaint_ref"] = num[e["case"]]
        W.complaints.append(e)
    W.complaints.sort(key=lambda c: (c["received"], c["complaint_ref"]))
    return W


# ------------------------------------------------------------------------------------------------ ask-path audit
class _View:
    """The ask paths as a solver meets them, computed from the simulation's own records."""

    def __init__(self, W):
        self.W = W
        self.fam = {k: f for k, f in family_of_hh_day(W).items() if Q3_FROM <= k[1] <= Q3_TO}
        self.booked = defaultdict(set)
        for a in W.appointments:
            if a["missed"] and Q3_FROM <= a["date"] <= Q3_TO:
                self.booked[(a["account_ref"], a["date"])].add((a["hh"], a["date"]))
        self.hh_of = {h: h for h in W.households}
        self.hh_of.update(W.dup_of)
        self.props = defaultdict(list)
        for h, x in W.households.items():
            if x["landlord"]:
                self.props[x["landlord"]].append(h)

    def psr(self, h, day):
        p = self.W.households[h]["psr_from"]
        return p is not None and p <= day

    def hits(self, acct, day):
        if acct in self.W.landlords:
            return sorted(p for p in self.props[acct] if (p, day) in self.fam)
        if acct in self.hh_of and (self.hh_of[acct], day) in self.fam:
            return [self.hh_of[acct]]
        return []

    def credits(self):
        grp = defaultdict(list)
        for c in self.W.credits:
            if c["reason"] == "MA" and Q3_FROM <= c["visit_date"] <= Q3_TO:
                grp[(c["account_ref"], c["visit_date"])].append(c)
        P = {k: Counter() for k in ("golden", "all_lines", "single_hit", "first_hit", "one_per_acct_day",
                                    "first_line", "direct", "policy")}
        for (acct, day), ls in grp.items():
            hits = self.hits(acct, day)
            if not hits:
                continue
            amts = [c["amount"] for c in ls]
            if len(ls) == len(hits) == 1:
                P["golden"][self.fam[(hits[0], day)]] += amts[0]
            else:
                pool = list(amts)
                for h in hits:
                    r = 50 if self.psr(h, day) else 30
                    pool.remove(r)
                    P["golden"][self.fam[(h, day)]] += r
            for a in amts:
                for h in hits:
                    P["all_lines"][self.fam[(h, day)]] += a
                P["first_hit"][self.fam[(hits[0], day)]] += a
                if len(hits) == 1:
                    P["single_hit"][self.fam[(hits[0], day)]] += a
            lsr = sorted(ls, key=lambda c: c.get("credit_ref", ""))
            P["one_per_acct_day"][self.fam[(hits[0], day)]] += lsr[0]["amount"]
            for i, h in enumerate(hits):
                if i < len(lsr):
                    P["first_line"][self.fam[(h, day)]] += lsr[i]["amount"]
            for k in self.booked.get((acct, day), []):
                P["direct"][self.fam[k]] += sum(amts)
                break
        for (h, day), f in self.fam.items():
            run = run_date_for(day)
            c = self.W.households[h]["cancelled"]
            if c and c <= run:
                continue
            P["policy"][f] += 50 if self.psr(h, day) else 30
        return P

    def complaints(self):
        E = self.W.cases.entries
        first = {}
        for e in E:
            if e["case"] not in first or e["received"] < first[e["case"]]["received"]:
                first[e["case"]] = e
        canon, seen = {}, {}
        for c, e in sorted(first.items(), key=lambda x: (x[1]["received"], x[0])):
            canon[c] = seen.setdefault((e["account_ref"], e["received"], e["about_visit_date"]), c)
        ents = [e for e in E if e["scot"] and e["about_visit_date"] is not None
                and Q3_FROM <= e["about_visit_date"] <= Q3_TO]
        res, direct = [], []
        for e in ents:
            day = e["about_visit_date"]
            if e["account_ref"] in self.W.landlords:
                h = [p for p in self.props[e["account_ref"]] if (p, day) in self.fam]
                assert len(h) <= 1
                if h:
                    res.append(((h[0], day), e))
            elif e["account_ref"] in self.hh_of and (self.hh_of[e["account_ref"]], day) in self.fam:
                res.append(((self.hh_of[e["account_ref"]], day), e))
            for k in self.booked.get((e["account_ref"], day), []):
                direct.append((k, e))
                break
        lab = lambda e: e["category"] in MISSED_LABELS
        moved = lambda e: first[e["case"]]["status"] == "Reopened"
        units = {"rows": None, "refs": lambda e: e["case"], "canon": lambda e: canon[e["case"]],
                 "acctvisit": lambda e: (e["account_ref"], e["about_visit_date"]), "hhday": lambda e: 0}

        def count(rows, keep, unit, drop_moved):
            out, seen_ = Counter(), defaultdict(set)
            for k, e in rows:
                if not keep(e) or (drop_moved and moved(e)):
                    continue
                if unit == "rows":
                    out[self.fam[k]] += 1
                else:
                    seen_[k].add(units[unit](e))
            for k, v in seen_.items():
                out[self.fam[k]] += len(v)
            return out
        closed = {e["case"] for e in E if e["status"] == "Closed"}
        return {"golden": count(res, lab, "canon", True),
                "rows_direct": count(direct, lab, "rows", False), "refs_direct": count(direct, lab, "refs", False),
                "rows_resolved": count(res, lab, "rows", False), "refs_resolved": count(res, lab, "refs", False),
                "drop_reopened": count(res, lambda e: lab(e) and e["status"] != "Reopened", "refs", False),
                "dedup_copies": count(res, lab, "canon", False),
                "dedup_acct_visit": count(res, lab, "acctvisit", False),
                "closed_only": count(res, lambda e: lab(e) and e["case"] in closed, "canon", True),
                "label_only": count(res, lambda e: e["category"] == "Missed appointment", "canon", True),
                "received_q3": count(res, lambda e: lab(e) and first[e["case"]]["received"].date() <= Q3_TO,
                                     "canon", True),
                "dedup_hhday": count(res, lab, "hhday", True)}


def ask_margins(P):
    """Per path and family: how far the wrong path's figure sits from the golden."""
    g = P["golden"]
    return {p: {f: c.get(f, 0) - g.get(f, 0) for f in g} for p, c in P.items() if p != "golden"}


CREDIT_FLOOR = 0.02      # every resolving path misses every family's credits by at least two per cent
COMPLAINT_FLOOR = {"refs_resolved": 0.025}


def _settle_complaints(W, seed, hh_days):
    """Top up the complaint records any cause family lacks until every path a solver could take misses every
    family's figure."""
    rng = np.random.default_rng([seed, 16])
    fix = {"rows_direct": "landlord", "refs_direct": "landlord", "rows_resolved": "moved",
           "refs_resolved": "moved", "drop_reopened": "carried", "dedup_copies": "moved",
           "dedup_acct_visit": "moved_landlord", "closed_only": "october", "label_only": "october",
           "received_q3": "october", "dedup_hhday": "pair"}
    for _ in range(12):
        P = _View(W).complaints()
        g = P["golden"]
        todo = []
        for p, kind in fix.items():
            for f in sorted(g):
                need = max(1, int(np.ceil(COMPLAINT_FLOOR.get(p, 0) * g[f])))
                if abs(P[p].get(f, 0) - g[f]) < need:
                    todo.append((f, kind))
        if not todo:
            return W
        for f, kind in sorted(set(todo)):
            _one_more(W, rng, hh_days, f, kind)
    raise RuntimeError("complaint paths would not separate")


def _one_more(W, rng, hh_days, f, kind):
    V = _View(W)
    lands = {l for l in W.landlords if not W.landlords[l].get("portfolio")}
    busy = {(e["hh"], e["about_visit_date"]) for e in W.cases.entries if e["scot"]}
    pool = [k for k in sorted(V.fam) if V.fam[k] == f and k not in busy]
    if kind in ("landlord", "pair", "moved_landlord"):
        pool = [k for k in pool if W.households[k[0]]["landlord"] in lands]
    if kind in ("moved", "moved_landlord"):
        pool = [k for k in pool if k[1] <= D(2026, 8, 10)]
    elif kind == "carried":
        pool = [k for k in pool if D(2026, 7, 20) <= k[1] <= D(2026, 8, 21)]
    elif kind == "october":
        pool = [k for k in pool if k[1] >= D(2026, 9, 22)]
    if not pool:
        raise RuntimeError("no household-day left in %s for %s" % (f, kind))
    k = pool[int(rng.integers(len(pool)))]
    _kind(W, rng, hh_days, k, kind)
    W.forced[f].append((kind, k))


def _settle_credits(W, seed):
    """Add the letting agents' other-region attendances on days their Scottish properties were missed until the
    paths that take every line on a matched day miss every family's credits by the floor."""
    rng = np.random.default_rng([seed, 17])
    for _ in range(40):
        P = _View(W).credits()
        g = P["golden"]
        short = [f for f in sorted(g) for p in ("single_hit", "first_hit", "all_lines")
                 if abs(P[p].get(f, 0) - g[f]) < CREDIT_FLOOR * g[f]]
        flat = [f for f in sorted(g) for p in ("one_per_acct_day", "direct", "policy") if P[p].get(f, 0) == g[f]]
        if flat:
            raise RuntimeError("credit path lands on the golden for %s" % flat)
        odd = [f for f in sorted(g) if abs(P["first_line"].get(f, 0) - g[f]) < 20]
        if not short and not odd:
            return W
        V = _View(W)
        for f in sorted(set(short)):
            days_ = sorted({(W.households[h]["landlord"], d) for (h, d), ff in V.fam.items() if ff == f
                            and h in W.portfolio_props and len(V.hits(W.households[h]["landlord"], d)) == 1})
            l, d = days_[int(rng.integers(len(days_)))]
            W.credits.append({"account_ref": l, "visit_date": d, "run_date": run_date_for(d), "reason": "MA",
                              "amount": 50 if rng.random() < 0.13 else 30, "hh": None})
        for f in odd:
            days_ = sorted((h, d) for (h, d), ff in V.fam.items() if ff == f and h in W.portfolio_props
                           and len(V.hits(W.households[h]["landlord"], d)) == 1)
            reg = [k for k in days_ if V.psr(*k)]
            h, d = (reg or days_)[int(rng.integers(len(reg or days_)))]
            W.credits.append({"account_ref": W.households[h]["landlord"], "visit_date": d,
                              "run_date": run_date_for(d), "reason": "MA",
                              "amount": 30 if V.psr(h, d) else 50, "hh": None})
        _number(W, seed)
    raise RuntimeError("credit paths would not separate")
