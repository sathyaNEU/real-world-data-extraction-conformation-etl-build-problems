"""The 2026 season's claims under the expiring programme with the loss adjusters' instructions, and the books at the
extract date: home policy records, farm policies with their holdings, and the coinsurance register."""
import datetime as dt
import math

import numpy as np

import world as W

# the 2026 storms: (name, peak in UTC, the local days its damage was done on, the mutual's incurred on first claims)
STORMS_2026 = [
    ("Ffion", dt.datetime(2026, 1, 11, 3, 15), [dt.date(2026, 1, 11)], 6_420_000.0),
    ("Gethin", dt.datetime(2026, 1, 12, 19, 40), [dt.date(2026, 1, 12), dt.date(2026, 1, 13)], 8_870_000.0),
    ("Hollis", dt.datetime(2026, 2, 8, 14, 25), [dt.date(2026, 2, 8), dt.date(2026, 2, 9)], 19_760_000.0),
    ("Juno", dt.datetime(2026, 2, 15, 22, 5), [dt.date(2026, 2, 15), dt.date(2026, 2, 16)], 4_230_000.0),
    ("Aelwen", dt.datetime(2026, 10, 24, 2, 50), [dt.date(2026, 10, 24), dt.date(2026, 10, 25)], 740_000.0),
]
# a roof still sheeted or a gable still propped when the next storm came: the claim is reopened for the further
# damage, and the adjuster is instructed again for it
REDAMAGE = {"Ffion": ("Hollis", 0.030), "Gethin": ("Hollis", 0.034), "Hollis": ("Juno", 0.062)}
EXTRACT_DATE = dt.date(2026, 10, 31)
WEB_SHARE = 0.27      # storm claims notified through the web form, which records the day it is sent as the loss date
ADJUSTER_FLOOR = 8000.0   # ordinary claims above this go to the loss adjusters too


def season2026(seed=W.SEED + 26):
    """claim lines of 2026 (dicts) and the loss adjusters' instruction rows"""
    rng = np.random.default_rng(seed)
    nrng = np.random.default_rng(seed + 1000)      # the claims system's numbering, with the gaps of voided and other-line numbers
    claims, adj = [], []
    seq = [0]
    by_name = {s[0]: s for s in STORMS_2026}

    def claim_no(day):
        seq[0] += int(nrng.integers(1, 4))
        return "HC%s%05d" % (day.strftime("%y%m"), seq[0])

    def instruct(c, damage, notified):
        adj.append({"claim": c, "damage": damage, "instructed": notified + dt.timedelta(days=int(rng.integers(0, 3)))})

    for name, peak, damage_days, target in STORMS_2026:
        n = int(target / 5200.0)
        sizes = np.exp(rng.normal(math.log(2600.0), 1.05, n))
        sizes = sizes * (target / sizes.sum())
        settle_p = 0.30 if name == "Aelwen" else 0.80
        for k in range(n):
            local_day = damage_days[int(rng.integers(0, len(damage_days)))]
            line = "Farm" if rng.random() < 0.18 else "Home"
            u = rng.random()
            channel = "Web" if u < WEB_SHARE else ("Broker" if u < WEB_SHARE + 0.12 else "Phone")
            lag = int(rng.integers(2, 10)) if channel == "Web" else int(rng.integers(0, 3))
            notified = local_day + dt.timedelta(days=lag)
            recorded = notified if channel == "Web" else local_day
            amount = round(float(sizes[k]), 2)
            settled = rng.random() < settle_p
            paid = amount if settled else round(amount * float(rng.uniform(0.2, 0.7)), 2)
            out = 0.0 if settled else round(amount - paid, 2)
            county = W.COUNTIES[int(rng.choice(4, p=[0.31, 0.37, 0.20, 0.12]))]
            c = {"claim": claim_no(local_day), "line": line, "peril": "Storm", "loss_date": recorded,
                 "notified": notified, "channel": channel, "county": county, "paid": paid, "outstanding": out,
                 "status": "Closed" if settled else "Open", "storm": name, "damage_date": local_day}
            if notified > EXTRACT_DATE:
                continue
            claims.append(c)
            instruct(c["claim"], local_day, notified)
            u2 = rng.random()
            nxt = REDAMAGE.get(name)
            later = by_name[nxt[0]] if nxt else None
            day2 = later[2][int(rng.integers(0, len(later[2])))] if nxt else None
            if nxt and u2 < nxt[1] and notified + dt.timedelta(days=2) < day2:
                # a claim already open, its adjuster instructed and the roof sheeted, when the next storm came: the
                # further damage is booked as a supplementary line on the reopened claim, which keeps the claim's loss
                # date, and the adjuster's second instruction carries the day the further damage was done
                note2 = day2 + dt.timedelta(days=int(rng.integers(1, 6)))
                extra = round(amount * float(rng.uniform(0.35, 0.95)), 2)
                done = rng.random() < 0.85
                p2 = extra if done else round(extra * 0.5, 2)
                claims.append(dict(c, claim=c["claim"] + "/R1", paid=p2, outstanding=round(extra - p2, 2),
                                   status="Closed" if done else "Open", notified=note2, storm=later[0],
                                   damage_date=day2))
                instruct(c["claim"], day2, note2)
            elif settled and u2 > 0.94:
                # a supplementary payment on the same damage (a second contractor's invoice, a ceiling found later):
                # the claim reopened on a new line, with no new instruction
                note2 = c["notified"] + dt.timedelta(days=int(rng.integers(30, 120)))
                if note2 <= EXTRACT_DATE:
                    extra = round(amount * float(rng.uniform(0.15, 0.6)), 2)
                    claims.append(dict(c, claim=c["claim"] + "/R1", paid=extra, outstanding=0.0, status="Closed",
                                       notified=note2))
    perils = [("Escape of water", 0.36), ("Accidental damage", 0.26), ("Theft", 0.12), ("Fire", 0.05),
              ("Storm", 0.21)]
    storm_days = [d for _, _, days, _ in STORMS_2026 for d in days]
    for k in range(9800):
        day = dt.date(2026, 1, 1) + dt.timedelta(days=int(rng.integers(0, 303)))
        peril = perils[int(rng.choice(len(perils), p=[p for _, p in perils]))][0]
        # the year's ordinary wind claims (a fence, a slipped ridge tile) fall away from the named storms' weeks
        if peril == "Storm" and any(abs((day - sd).days) <= 12 for sd in storm_days):
            peril = "Accidental damage"
        channel = "Web" if rng.random() < 0.3 else "Phone"
        notified = day + dt.timedelta(days=int(rng.integers(0, 6)))
        amount = round(float(math.exp(rng.normal(math.log(1400.0), 1.1))), 2)
        if peril == "Fire":
            amount = round(amount * 4.0, 2)
        settled = rng.random() < 0.85
        paid = amount if settled else round(amount * 0.4, 2)
        if notified > EXTRACT_DATE:
            continue
        c = {"claim": claim_no(day), "line": "Farm" if rng.random() < 0.15 else "Home", "peril": peril,
             "loss_date": notified if channel == "Web" else day, "notified": notified, "channel": channel,
             "county": W.COUNTIES[int(rng.integers(0, 4))], "paid": paid,
             "outstanding": 0.0 if settled else round(amount - paid, 2),
             "status": "Closed" if settled else "Open", "storm": None, "damage_date": day}
        claims.append(c)
        if amount >= ADJUSTER_FLOOR:
            instruct(c["claim"], day, notified)
    claims.sort(key=lambda c: (c["notified"], c["claim"]))
    adj.sort(key=lambda a: (a["instructed"], a["claim"], a["damage"]))
    job = [40117]
    for i, a in enumerate(adj):
        job[0] += int(nrng.integers(1, 13))      # the adjusters number every insurer's instructions in one series
        a["job"] = "PLA-26-%05d" % job[0]
    return claims, adj


# ---------------------------------------------------------------------------------------------------------- books
RENUMBER_P = 0.07          # holdings the Rural Payments Agency gave a new CPH in 2026 (a merger, a split, a let)
COINS_LAPSED = 0.06        # coinsured farm policies in the register that did not renew in 2026


def _cph(rng, county):
    return "%02d/%03d/%04d" % (10 + W.COUNTIES.index(county) * 7 + int(rng.integers(0, 6)),
                               int(rng.integers(1, 999)), int(rng.integers(1, 9999)))


def exposure(seed=W.SEED + 27):
    """home policy records in the extract, farm policies with their holdings, the coinsurance register"""
    rng = np.random.default_rng(seed)
    nrng = np.random.default_rng(seed + 1000)      # the policy systems' numbering, gaps where numbers were voided
    hid = [int(x) for x in 2100000 + np.cumsum(nrng.integers(1, 4, 43000))]
    lid = [int(x) for x in 2590000 + np.cumsum(nrng.integers(1, 5, 1600))]
    fid = [int(x) for x in 410000 + np.cumsum(nrng.integers(1, 6, 5200))]
    rnum = [3100000]
    home = []
    asof = EXTRACT_DATE
    for k in range(43000):
        county = W.COUNTIES[int(rng.choice(4, p=[0.30, 0.38, 0.20, 0.12]))]
        bld = round(float(math.exp(rng.normal(math.log(285000), 0.38))), -3)
        cts = round(float(math.exp(rng.normal(math.log(42000), 0.45))), -2)
        start = asof - dt.timedelta(days=int(rng.integers(0, 365)))
        pol = "HH%07d" % hid[k]
        home.append({"policy": pol, "status": "Live", "start": start, "end": start + dt.timedelta(days=364),
                     "county": county, "buildings": bld, "contents": cts})
        renew = start + dt.timedelta(days=365)
        if renew <= asof + dt.timedelta(days=21) and rng.random() < 0.86:
            # invited and accepted three weeks ahead: the renewal term under a new number
            rnum[0] += int(nrng.integers(1, 5))
            home.append({"policy": "HH%07d" % rnum[0], "status": "Live", "start": renew,
                         "end": renew + dt.timedelta(days=364), "county": county,
                         "buildings": round(bld * 1.04, -3), "contents": round(cts * 1.03, -2)})
    for k in range(1600):
        county = W.COUNTIES[int(rng.integers(0, 4))]
        end = asof - dt.timedelta(days=int(rng.integers(1, 300)))
        home.append({"policy": "HH%07d" % lid[k], "status": "Lapsed", "start": end - dt.timedelta(days=364),
                     "end": end, "county": county,
                     "buildings": round(float(math.exp(rng.normal(math.log(270000), 0.4))), -3),
                     "contents": round(float(math.exp(rng.normal(math.log(40000), 0.45))), -2)})
    farms, locations, coins = [], [], []
    for k in range(5200):
        corr = W.COUNTIES[int(rng.choice(4, p=[0.33, 0.40, 0.19, 0.08]))]
        nloc = int(rng.choice([1, 2, 3, 4], p=[0.58, 0.25, 0.11, 0.06]))
        pol = "FM%06d" % fid[k]
        locs = []
        for j in range(nloc):
            county = corr if (j == 0 or rng.random() < 0.62) else W.COUNTIES[int(rng.integers(0, 4))]
            b = round(float(math.exp(rng.normal(math.log(430.0), 0.7))), 0)    # thousands of pounds
            ct = round(float(math.exp(rng.normal(math.log(190.0), 0.8))), 0)
            cph = _cph(rng, county)
            prev = ""
            if rng.random() < RENUMBER_P:
                prev, cph = cph, _cph(rng, county)
            locs.append({"policy": pol, "location": j + 1, "cph": cph, "prev": prev, "county": county,
                         "b_k": b, "c_k": ct})
        locations.extend(locs)
        total = sum(l["b_k"] + l["c_k"] for l in locs)
        farms.append({"policy": pol, "cph": locs[0]["cph"], "county": corr, "si_k": total})
        if total >= 1500 and rng.random() < 0.55:
            share = float(rng.choice([0.40, 0.50, 0.60, 0.75]))
            # the register keeps the main holding's CPH as it stood when the arrangement was last renewed; a holding
            # renumbered since then is still under its old number
            arranged = dt.date(2025, 11, 1) + dt.timedelta(days=int(rng.integers(0, 365)))
            key = locs[0]["cph"]
            if locs[0]["prev"] and rng.random() < 0.72:
                key = locs[0]["prev"]
            coins.append({"lead": ["Tamarisk Insurance", "Caradon Agricultural", "Exmoor Farmers' Union Mutual"][int(rng.integers(0, 3))],
                          "lead_ref": "LD-%06d" % int(rng.integers(100000, 999999)), "cph": key.replace("/", ""),
                          "share": share, "policy": pol, "arranged": arranged})
    # arrangements on farm policies that did not renew this year stay in the register until it is tidied at renewal
    n_lapsed = int(round(len(coins) * COINS_LAPSED))
    for k in range(n_lapsed):
        county = W.COUNTIES[int(rng.choice(4, p=[0.33, 0.40, 0.19, 0.08]))]
        coins.append({"lead": ["Tamarisk Insurance", "Caradon Agricultural", "Exmoor Farmers' Union Mutual"][int(rng.integers(0, 3))],
                      "lead_ref": "LD-%06d" % int(rng.integers(100000, 999999)),
                      "cph": _cph(rng, county).replace("/", ""), "share": float(rng.choice([0.40, 0.50, 0.60, 0.75])),
                      "policy": None, "arranged": dt.date(2025, 11, 1) + dt.timedelta(days=int(rng.integers(0, 200)))})
    coins.sort(key=lambda c: (c["arranged"], c["lead_ref"]))
    return home, farms, locations, coins
