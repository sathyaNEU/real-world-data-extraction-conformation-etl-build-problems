"""The world: the board's practices and pharmacies, its patients on a statin, and every statin item dispensed to
them from 1 October 2025 (the dispensing extract keeps 1 December 2025 onwards) to 31 December 2026.

Self-managing patients collect a 28- or 56-day supply when theirs runs low; how late they come back follows how much
of each supply they take, scattered by several days either way. A pharmacy-filled compliance aid is dispensed on the
pharmacy's own cycle (weekly 7-day items, or a 28-day item every 28 days) from the patient's set day, whatever the
patient takes, moved to the next day the pharmacy opens when the set day is a bank holiday; a care home's residents are
dispensed on the home's 28-day cycle."""
from __future__ import annotations

import datetime as dt

from common import (BANK_HOLIDAYS, BORN_BY, DISP_START, NETWORKS, NETWORK_MOVE, QUARVIS_CODE_RATE, REKEY,
                    YEAR_END, YEAR_START, rng, token)

PRACTICE_WORDS = ["Medical Centre", "Surgery", "Health Centre", "Medical Practice", "Family Practice",
                  "Group Practice"]
EXTRA_PLACES = ["Ellinwold", "Eskgarth", "Feldmere", "Iverswick", "Morvhope", "Sorrwick", "Stavholt", "Pennstead",
                "Yeldfield", "Wembdale", "Raskhope", "Tullmere", "Vellmarsh", "Gravholt", "Lathstow", "Corbrennan",
                "Kirtwick", "Nevcote", "Pellhope", "Tarvshaw", "Briskwold", "Marlhope", "Ivershope", "Lorrdale",
                "Morvstead", "Sorrfield", "Belvfield", "Drummhope", "Ellincote", "Feldcombe", "Ganthope", "Orrinwick"]

# product description, ingredient, strength mg, prevalence weight
PRODUCTS = [
    ("Atorvastatin 10mg tablets", "atorvastatin", 10, 8), ("Atorvastatin 20mg tablets", "atorvastatin", 20, 30),
    ("Atorvastatin 40mg tablets", "atorvastatin", 40, 15), ("Atorvastatin 80mg tablets", "atorvastatin", 80, 5),
    ("Simvastatin 20mg tablets", "simvastatin", 20, 8), ("Simvastatin 40mg tablets", "simvastatin", 40, 14),
    ("Rosuvastatin 5mg tablets", "rosuvastatin", 5, 4), ("Rosuvastatin 10mg tablets", "rosuvastatin", 10, 6),
    ("Rosuvastatin 20mg tablets", "rosuvastatin", 20, 3), ("Pravastatin sodium 20mg tablets", "pravastatin", 20, 2),
    ("Pravastatin sodium 40mg tablets", "pravastatin", 40, 4), ("Fluvastatin 80mg modified-release tablets",
                                                                   "fluvastatin", 80, 1),
]
BRAND = {"Atorvastatin 10mg tablets": "Lipitor 10mg tablets (Viatris UK Healthcare Ltd)",
         "Atorvastatin 20mg tablets": "Lipitor 20mg tablets (Viatris UK Healthcare Ltd)",
         "Atorvastatin 40mg tablets": "Lipitor 40mg tablets (Viatris UK Healthcare Ltd)",
         "Rosuvastatin 10mg tablets": "Crestor 10mg tablets (AstraZeneca UK Ltd)",
         "Rosuvastatin 20mg tablets": "Crestor 20mg tablets (AstraZeneca UK Ltd)"}
HALF = {"Atorvastatin 20mg tablets": "Atorvastatin 10mg tablets", "Atorvastatin 40mg tablets":
        "Atorvastatin 20mg tablets", "Atorvastatin 80mg tablets": "Atorvastatin 40mg tablets",
        "Simvastatin 40mg tablets": "Simvastatin 20mg tablets", "Rosuvastatin 20mg tablets":
        "Rosuvastatin 10mg tablets", "Rosuvastatin 10mg tablets": "Rosuvastatin 5mg tablets",
        "Pravastatin sodium 40mg tablets": "Pravastatin sodium 20mg tablets"}
ONE_A_DAY = ["ONE TABLET AT NIGHT", "ONE TO BE TAKEN EACH DAY", "TAKE ONE TABLET DAILY", "1 OD", "ONE AT NIGHT",
             "TAKE ONE ONCE A DAY", "ONE TABLET ONCE DAILY AT NIGHT", "1 TABLET AT NIGHT", "TAKE ONE AT NIGHT"]
TWO_A_DAY = ["TWO TABLETS AT NIGHT", "TAKE TWO DAILY", "2 AT NIGHT", "TWO TO BE TAKEN AT NIGHT"]


def working_day(d):
    """A pack due on a bank holiday or a Sunday is dispensed the next day the pharmacy opens."""
    while d.weekday() == 6 or d in BANK_HOLIDAYS:
        d += dt.timedelta(days=1)
    return d


def anchor_day(r, step):
    """The patient's set day: never a Sunday, the day the pharmacy prepares that patient's packs."""
    while True:
        d = DISP_START + dt.timedelta(days=int(r.integers(0, step)))
        if d.weekday() != 6:
            return d


def practices():
    """Each network's practices: code, name, system, network on 31 December 2026 and before 1 April 2026."""
    out, used, k = [], set(), 0
    r = rng("practices")
    letters = "ABCDEFGHJKLMNPRTUVWY"
    for code, name, sysx, n, *_rest in NETWORKS:
        npr = _rest[-1]
        places = [name] + list(r.choice(EXTRA_PLACES, size=npr - 1, replace=False))
        for i in range(npr):
            while True:
                pc = "%s%05d" % (letters[int(r.integers(0, len(letters)))], int(r.integers(81000, 87999)))
                if pc not in used:
                    used.add(pc)
                    break
            word = PRACTICE_WORDS[(k + i) % len(PRACTICE_WORDS)]
            pname = ("The %s %s" % (places[i], word)) if word == "Surgery" else "%s %s" % (places[i], word)
            out.append(dict(code=pc, name=pname, system=sysx, network=code, network_before=code,
                            weight=float(r.uniform(0.6, 1.4)), place=places[i]))
        k += npr
    # a place that names practices in two networks gets another practice word the second time, so every name is one
    # practice's (the same place's practices are told apart by their word, as real ones are)
    seen = set()
    for p in out:
        j = 0
        while p["name"] in seen:
            word = PRACTICE_WORDS[j % len(PRACTICE_WORDS)]
            p["name"] = ("The %s %s" % (p["place"], word)) if word == "Surgery" else "%s %s" % (p["place"], word)
            j += 1
        seen.add(p["name"])
    # two practices moved network on 1 April 2026: one Synaris practice from Briskdale to Grevmoor and one
    # Quarvis practice from Lathcombe to Feldcote; their year-end network is the new one
    for frm, to in (("BRK", "GRV"), ("LTH", "FEL")):
        p = [x for x in out if x["network"] == frm][-1]
        p["network"] = to
    return out


def pharmacies(pracs):
    """Community pharmacies: one cluster per network, plus one distance-selling pharmacy serving every network."""
    out, used = [], set()
    r = rng("pharmacies")
    owners = ["Pellhope Pharmacy Group", "Ravensholt Chemists Ltd", "Drevanholm Healthcare Ltd", None, None, None]
    for code, name, sysx, n, *_ in NETWORKS:
        k = max(4, int(round(n / 330)))
        for i in range(k):
            while True:
                ods = "F%s%03d" % ("ABCDEFGHJKLMNPQRSTVWXY"[int(r.integers(0, 22))], int(r.integers(100, 999)))
                if ods not in used:
                    used.add(ods)
                    break
            owner = owners[int(r.integers(0, len(owners)))]
            pname = ("%s Pharmacy" % name) if i == 0 else "%s Pharmacy" % EXTRA_PLACES[int(r.integers(0, len(EXTRA_PLACES)))]
            out.append(dict(ods=ods, name=pname, network=code, owner=owner, kind="community",
                            weight=float(r.uniform(0.5, 1.5))))
    _pharmacy_names(out)
    out.append(dict(ods="FDS801", name="Vellmarsh Direct Pharmacy", network=None, owner="Vellmarsh Direct Ltd",
                    kind="distance-selling", weight=1.0))
    return out


BRANDS = {"Pellhope Pharmacy Group": "Pellhope Pharmacy", "Ravensholt Chemists Ltd": "Ravensholt Chemists",
          "Drevanholm Healthcare Ltd": "Drevanholm Pharmacy"}
STYLES = ("%s Pharmacy", "%s Pharmacy", "%s Chemist", "%s Health Centre Pharmacy", "%s Late Night Pharmacy")


def _pharmacy_names(out):
    """A chain's branch carries the chain's brand and its place; an independent its place in a style of its own. The
    names come from their own stream, so no other draw moves, and no two pharmacies share one."""
    seen = set()
    for p in out:
        place = p["name"][:-len(" Pharmacy")]
        r = rng("pharmacy name", p["ods"])
        style = int(r.integers(0, len(STYLES)))
        cands = (["%s %s" % (BRANDS[p["owner"]], place)] if p["owner"] else []) + \
            [STYLES[(style + j) % len(STYLES)] % place for j in range(len(STYLES))]
        p["name"] = next(c for c in cands if c not in seen)
        seen.add(p["name"])


def _sm_items(r, start, supply, tpd, adh):
    """Self-managing collections from the first one in the extract window to the year end."""
    out = []
    t = start
    while t <= YEAR_END:
        out.append(t)
        sd = 5.5 if supply == 28 else 8.0
        gap = max(10, int(round(supply / adh + r.normal(0.0, sd))))
        t = t + dt.timedelta(days=gap)
    return out


def _aid_items(r, weekly, anchor, until=YEAR_END, frm=DISP_START, pause=None):
    step = 7 if weekly else 28
    out = []
    t = anchor
    while t < frm:
        t += dt.timedelta(days=step)
    while t <= until:
        d = working_day(t)
        if not (pause and pause[0] <= d < pause[1]):
            out.append(d)
        t += dt.timedelta(days=step)
    return out


def patients(pracs, pharms):
    """Every patient of the board's practices with a statin on repeat in the extract window."""
    pts = []
    by_net = {}
    for p in pracs:
        by_net.setdefault(p["network"], []).append(p)
    ph_net = {}
    for p in pharms:
        if p["kind"] == "community":
            ph_net.setdefault(p["network"], []).append(p)
    dsp = [p for p in pharms if p["kind"] == "distance-selling"][0]
    prod_names = [x[0] for x in PRODUCTS]
    prod_w = [x[3] for x in PRODUCTS]
    pid = 0
    for code, name, sysx, n, ch, aid, w7, low, _npr in NETWORKS:
        r = rng("patients", code)
        nets_pr = by_net[code]
        pw = [p["weight"] for p in nets_pr]
        pw = [x / sum(pw) for x in pw]
        phs = ph_net[code]
        phw = [p["weight"] for p in phs]
        phw = [x / sum(phw) for x in phw]
        # care homes in the network: each with its own 28-day cycle day and its supplying pharmacy
        homes = []
        for h in range(max(2, int(round(n * ch / 14)))):
            homes.append(dict(anchor=anchor_day(r, 28),
                              pharmacy=phs[int(r.integers(0, len(phs)))]["ods"]))
        bands = [("65+", n, ch, aid, low), ("60-64", int(round(n * 0.16)), ch * 0.15, aid * 0.25, low + 0.03)]
        for band, nb, chb, aidb, lowb in bands:
            n_ch, n_aid = int(round(nb * chb)), int(round(nb * aidb))
            kinds = ["ch"] * n_ch + ["aid"] * n_aid + ["sm"] * (nb - n_ch - n_aid)
            for kind in kinds:
                pid += 1
                prac = nets_pr[int(r.choice(len(nets_pr), p=pw))]
                yob = int(r.integers(1931, BORN_BY + 1)) if band == "65+" else int(r.integers(BORN_BY + 1, 1967))
                if band == "65+" and r.random() < 0.55:      # an older-leaning age mix
                    yob = int(r.integers(1931, 1956))
                sex = "F" if r.random() < (0.47 if kind == "sm" else 0.62) else "M"
                prod = prod_names[int(r.choice(len(prod_names), p=[w / sum(prod_w) for w in prod_w]))]
                tpd = 2 if (prod in HALF and r.random() < 0.07) else 1
                item_prod = HALF[prod] if tpd == 2 else prod
                if item_prod in BRAND and r.random() < 0.06:
                    item_prod = BRAND[item_prod]
                dose_text = (TWO_A_DAY[int(r.integers(0, len(TWO_A_DAY)))] if tpd == 2 else
                             ("AS DIRECTED" if r.random() < 0.03 else ONE_A_DAY[int(r.integers(0, len(ONE_A_DAY)))]))
                pt = dict(pid=pid, network=code, practice=prac["code"], system=prac["system"], band=band, yob=yob,
                          sex=sex, kind=kind, product=item_prod, tpd=tpd, dose_text=dose_text, items=[],
                          left=None, coded_aid=False, aid_code_date=None, care_home_date=None, weekly=None,
                          aid_from=None)
                # a few leave the board or die during 2026: dispensing stops and they are not in the year-end lists
                if r.random() < 0.055:
                    pt["left"] = YEAR_START + dt.timedelta(days=int(r.integers(20, 350)))
                if kind == "sm":
                    supply = 56 if r.random() < 0.18 else 28
                    adh = (float(r.uniform(0.40, 0.76)) if r.random() < lowb else float(r.uniform(0.86, 1.12)))
                    pt["adh"] = adh
                    usual = phs[int(r.choice(len(phs), p=phw))]["ods"]
                    if r.random() < 0.03:
                        usual = dsp["ods"]
                    start = DISP_START + dt.timedelta(days=int(r.integers(0, supply)))
                    if r.random() < 0.035:               # started a statin during 2026
                        start = YEAR_START + dt.timedelta(days=int(r.integers(20, 330)))
                    dates = _sm_items(r, start, supply, tpd, adh)
                    ptype = ["Repeat", "Repeat dispensing", "Acute"][int(r.choice(3, p=[0.70, 0.25, 0.05]))]
                    switch_at = YEAR_START + dt.timedelta(days=int(r.integers(60, 300))) if r.random() < 0.05 else None
                    for d in dates:
                        ods = usual if r.random() > 0.08 else phs[int(r.integers(0, len(phs)))]["ods"]
                        p_now = item_prod
                        if switch_at and d >= switch_at:
                            p_now = "Atorvastatin 20mg tablets" if "Atorvastatin" not in item_prod else \
                                "Rosuvastatin 10mg tablets"
                        pt["items"].append((d, ods, p_now, supply * tpd, ptype))
                elif kind == "aid":
                    weekly = r.random() < w7
                    pt["weekly"] = weekly
                    anchor = anchor_day(r, 7 if weekly else 28)
                    ods = phs[int(r.choice(len(phs), p=phw))]["ods"]
                    pause = None
                    if r.random() < 0.05:                # (a stay away keeps the cycle: the packs are collected)
                        r.integers(30, 300), r.integers(10, 40)
                    aid_from = DISP_START
                    if r.random() < 0.0:                 # (no patient moved onto an aid during 2026)
                        aid_from = YEAR_START + dt.timedelta(days=int(r.integers(60, 240)))
                        pt["aid_from"] = aid_from
                        adh = float(r.uniform(0.45, 1.0))
                        for d in _sm_items(r, DISP_START + dt.timedelta(days=int(r.integers(0, 28))), 28, tpd, adh):
                            if d < aid_from:
                                pt["items"].append((d, ods, item_prod, 28 * tpd, "Repeat"))
                    step = 7 if weekly else 28
                    for d in _aid_items(r, weekly, anchor, frm=aid_from, pause=pause):
                        pt["items"].append((d, ods, item_prod, step * tpd, "Repeat"))
                    if prac["system"] == "Q" and r.random() < QUARVIS_CODE_RATE:
                        pt["coded_aid"] = True
                        pt["aid_code_date"] = (aid_from if pt["aid_from"] else
                                               dt.date(int(r.integers(2018, 2026)), int(r.integers(1, 13)), 1)
                                               + dt.timedelta(days=int(r.integers(0, 27))))
                else:                                    # care home resident on the home's 28-day cycle
                    home = homes[int(r.integers(0, len(homes)))]
                    pt["care_home_date"] = dt.date(int(r.integers(2019, 2026)), int(r.integers(1, 13)), 1) + \
                        dt.timedelta(days=int(r.integers(0, 27)))
                    for d in _aid_items(r, False, home["anchor"]):
                        pt["items"].append((d, home["pharmacy"], item_prod, 28 * tpd, "Repeat"))
                if pt["left"]:
                    pt["items"] = [x for x in pt["items"] if x[0] < pt["left"]]
                pts.append(pt)
    return pts


def keys(pts):
    """The data service's pseudonyms: an old key on every item before 1 July 2026, a new key from then on and on the
    year-end lists, and the crosswalk for every patient still registered on 1 July."""
    for pt in pts:
        pt["new_key"] = "IV" + token("new", pt["pid"], n=10).upper()
        pt["old_key"] = "%012d" % (int(token("old", pt["pid"], n=12), 16) % 10 ** 12)
        pt["in_crosswalk"] = not (pt["left"] and pt["left"] < REKEY)
    return pts


def build():
    pr = practices()
    ph = pharmacies(pr)
    pts = keys(patients(pr, ph))
    return pr, ph, pts
