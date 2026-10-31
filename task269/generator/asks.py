"""The asks from the shipped pack. Ask A: each ward's 2025-26 hospital-onset bloodstream infections and their rate per
10,000 occupied bed days, under the hospital's surveillance protocol. Ask B: the litres of alcohol-based hand rub put
out on each ward in 2025-26 and per 1,000 occupied bed days, as the hand hygiene program measures it. Each with its
stops: the routes a careful analyst takes that file other figures."""
import datetime as dt

import numpy as np
import pandas as pd

import common as K
import pack as P

COMMENSAL_WORDS = ("Staphylococcus epidermidis", "Staphylococcus hominis", "Micrococcus", "Corynebacterium",
                   "Cutibacterium", "Bacillus", "viridans")
LITRES = {"114502": 0.5, "114519": 2.4, "114533": 1.0}


def r1(x):
    return K.r1(float(x))


def bed_days(d, m):
    c = d["census"].copy()
    c["ward"] = c["ward"].map(m["ward"])
    c["census_date"] = pd.to_datetime(c["census_date"]).dt.date
    c = c[(c["census_date"] >= K.YEAR_START) & (c["census_date"] <= K.YEAR_END)]
    return c.groupby("ward")["occupied_beds"].sum().to_dict()


# ------------------------------------------------------------------------------------------------ Ask A
def _isolates(d, m, link_retired=True):
    iso = d["isolates"].copy()
    iso["t"] = pd.to_datetime(iso["collected"], format="%d/%m/%Y %H:%M")
    iso["loc"] = iso["location"].map(m["lab"])
    adm = d["admissions"].copy()
    adm["a"] = pd.to_datetime(adm["admitted"], format="%d/%m/%Y %H:%M")
    adm["s"] = pd.to_datetime(adm["separated"], format="%d/%m/%Y %H:%M")
    by_mrn = {}
    for _, r in adm.iterrows():
        by_mrn.setdefault(r["mrn"], []).append(r)
    by_dob = {}
    for _, r in adm.iterrows():
        by_dob.setdefault((r["date_of_birth"], r["sex"]), []).append(r)
    link = []
    for _, r in iso.iterrows():
        hit = [a for a in by_mrn.get(r["mrn"], []) if a["a"] <= r["t"] <= a["s"]]
        if not hit and link_retired and r["mrn"] not in by_mrn:
            hit = [a for a in by_dob.get((r["date_of_birth"], r["sex"]), []) if a["a"] <= r["t"] <= a["s"]]
        link.append(hit[0]["admission_no"] if len(hit) == 1 else None)
    iso["admission_no"] = link
    return iso, adm


def _ward_at(d, m, adm):
    """each admission's wards over time: the admitting ward, then each transfer's ward from its time"""
    tr = d["transfers"].copy()
    tr["t"] = pd.to_datetime(tr["transferred"], format="%d/%m/%Y %H:%M")
    tr = tr.sort_values(["admission_no", "t"])
    path = {r["admission_no"]: [(r["a"], m["ward"].get(r["admitting_ward"], r["admitting_ward"]))]
            for _, r in adm.iterrows()}
    for _, r in tr.iterrows():
        path[r["admission_no"]].append((r["t"], m["ward"].get(r["to_ward"], r["to_ward"])))

    def at(a_no, t):
        w = None
        for ts, ward in path[a_no]:
            if ts <= t:
                w = ward
        return w
    return at


def stay_start(adm, gap_minutes=0):
    """when each admission's stay in the hospital began: an admission that opened within gap_minutes after the same
    patient's previous admission closed continues that stay (a change of care type closes one admission and opens the
    next at the same minute); None takes every admission as its own stay"""
    start = {}
    for _, g in adm.sort_values(["mrn", "a"]).groupby("mrn", sort=False):
        cur, prev_s = None, None
        for _, r in g.iterrows():
            if gap_minutes is None or prev_s is None or not (
                    0 <= (r["a"] - prev_s).total_seconds() <= gap_minutes * 60):
                cur = r["a"]
            start[r["admission_no"]] = cur
            prev_s = r["s"]
    return start


def hobsi(target, attribute="collection", link_retired=True, episodes=True, commensal_rule=True, onset_rule=True,
          map_s1a=True, stay_gap=0, episode_by="patient"):
    d = P.load(target)
    m = P.maps(d)
    if not map_s1a:
        m = dict(m)
        m["ward"] = {k: k for k in m["ward"]}
        m["lab"] = {k: (v if v != K.MOVED[0] else None) for k, v in m["lab"].items()}
        m["lab"]["AVH-6A"] = "6A"
    iso, adm = _isolates(d, m, link_retired)
    at = _ward_at(d, m, adm)
    adm_t = stay_start(adm, stay_gap)
    iso = iso[iso["admission_no"].notna()].copy()
    iso["commensal"] = iso["organism"].map(lambda o: any(w in o for w in COMMENSAL_WORDS))
    # an episode is the patient's: the cultures of one patient (the linked admission's record number) and organism,
    # across admissions; "admission" and "stay" group them within one admission or one stay instead
    adm_mrn = adm.set_index("admission_no")["mrn"].to_dict()
    iso["who"] = iso["admission_no"].map(adm_mrn) if episode_by == "patient" else (
        iso["admission_no"] if episode_by == "admission" else iso["admission_no"].map(lambda a: "%s|%s" % (adm_mrn[a], adm_t[a])))
    events = []
    for (who, org), g in iso.sort_values("t").groupby(["who", "organism"], sort=True):
        times = list(g["t"])
        locs = list(g["loc"])
        a_nos = list(g["admission_no"])
        if g["commensal"].iloc[0] and commensal_rule:
            # a commensal counts from two sets within 48 hours: the episode starts at the first set of such a pair
            starts = []
            for i in range(len(times) - 1):
                if (times[i + 1] - times[i]).total_seconds() <= 48 * 3600:
                    starts.append(i)
            idx = starts[:1]
        else:
            idx = list(range(len(times)))
        first = None
        for i in idx:
            if episodes and first is not None and (times[i] - times[first]).total_seconds() < 14 * 86400:
                continue
            first = i
            a_no = a_nos[i]
            if onset_rule and (times[i] - adm_t[a_no]).total_seconds() <= 48 * 3600:
                continue
            w = at(a_no, times[i]) if attribute == "collection" else locs[i]
            events.append((a_no, org, times[i], w))
    n = {c: 0 for c in K.WARD}
    for a_no, org, t, w in events:
        if w in n and K.YEAR_START <= t.date() <= K.YEAR_END:
            n[w] += 1
    bd = bed_days(d, m)
    rate = {c: (r1(n[c] / bd[c] * 10000.0) if bd.get(c) else None) for c in K.WARD}
    return dict(n=n, rate=rate, bed_days=bd, events=events)


# ------------------------------------------------------------------------------------------------ Ask B
def resent_records(rounds, window=20):
    """records a handheld sent a second time: the same dispenser at the same minute of the day as a record of that
    dispenser on an earlier day within the twenty days before, synchronised after the day's own records (window None:
    any earlier day of the year, which also takes genuine refills weeks apart that fell on the same minute)"""
    r = rounds.copy()
    r["t"] = pd.to_datetime(r["fitted"], format="%d/%m/%Y %H:%M")
    r["day"] = r["t"].dt.date
    r["hm"] = r["t"].dt.strftime("%H:%M")
    r["rid"] = r["record_id"].astype(int)
    seen = {}
    copies = set()
    for _, x in r.sort_values(["t", "rid"]).iterrows():
        key = (x["dispenser_id"], x["hm"])
        prev = seen.get(key)
        if prev is not None and 0 < (x["day"] - prev).days and (window is None or (x["day"] - prev).days <= window):
            copies.add(x["record_id"])
            continue
        seen[key] = x["day"]
    return copies


def hand_rub(target, drop_copies=True, one_a_day=False, carton_as_bottle=False, returns=True, map_s1a=True,
             copy_window=20):
    d = P.load(target)
    m = P.maps(d)
    wards = m["ward"] if map_s1a else {k: k for k in m["ward"]}
    iss = d["issues"].copy()
    iss["quantity"] = iss["quantity"].astype(int)
    iss = iss[iss["cost_centre"].isin(m["cc"].keys()) & iss["item_code"].isin(["114502", "114519"])]
    if not returns:
        iss = iss[iss["transaction"] == "ISSUE"]
    lit = {"114502": 0.5, "114519": 0.1 if carton_as_bottle else 2.4}
    iss["litres"] = iss["item_code"].map(lit) * iss["quantity"]
    bottles = iss.groupby(iss["cost_centre"].map(m["cc"]))["litres"].sum().to_dict()
    rd = d["rounds"].copy()
    rd["t"] = pd.to_datetime(rd["fitted"], format="%d/%m/%Y %H:%M")
    rd = rd[(rd["t"].dt.date >= K.YEAR_START) & (rd["t"].dt.date <= K.YEAR_END)]
    if drop_copies:
        rd = rd[~rd["record_id"].isin(resent_records(d["rounds"], copy_window))]
    disp = d["dispensers"].set_index("dispenser_id")["ward_or_area"].to_dict()
    kind = d["dispensers"].set_index("dispenser_id")["type"].to_dict()
    rd = rd[rd["dispenser_id"].map(kind) == "Hand rub"]
    rd["unit"] = rd["dispenser_id"].map(disp).map(lambda u: wards.get(u, u))
    if one_a_day:
        rd = rd.assign(day=rd["t"].dt.date).drop_duplicates(["dispenser_id", "day"])
    wall = rd.groupby("unit").size().to_dict()
    bd = bed_days(d, m if map_s1a else dict(m, ward={k: k for k in m["ward"]}))
    out_l, out_r = {}, {}
    for c in K.WARD:
        litres = float(bottles.get(c, 0.0)) + float(wall.get(c, 0))
        out_l[c] = r1(litres)
        out_r[c] = r1(litres / bd[c] * 1000.0) if bd.get(c) else None
    return dict(litres=out_l, rate=out_r, bottles=bottles, wall=wall, bed_days=bd)


def hand_soap(target, drop_copies=True, cartridge=0.8, map_s1a=True, sum_quantity=False, copy_window=20):
    """the litres of liquid hand soap put out on each ward: the store's soap pump bottles to the ward's cost centre
    less returns, and the contractor's cartridges on the ward's soap dispensers, one a record (a terminal clean's job
    carries its cartridges on each of its records), the re-sent records left out"""
    d = P.load(target)
    m = P.maps(d)
    wards = m["ward"] if map_s1a else {k: k for k in m["ward"]}
    iss = d["issues"].copy()
    iss["quantity"] = iss["quantity"].astype(int)
    iss = iss[iss["cost_centre"].isin(m["cc"].keys()) & (iss["item_code"] == "114541")]
    bottles = (iss.groupby(iss["cost_centre"].map(m["cc"]))["quantity"].sum() * 0.5).to_dict()
    rd = d["rounds"].copy()
    rd["t"] = pd.to_datetime(rd["fitted"], format="%d/%m/%Y %H:%M")
    rd = rd[(rd["t"].dt.date >= K.YEAR_START) & (rd["t"].dt.date <= K.YEAR_END)]
    if drop_copies:
        rd = rd[~rd["record_id"].isin(resent_records(d["rounds"], copy_window))]
    disp = d["dispensers"].set_index("dispenser_id")["ward_or_area"].to_dict()
    kind = d["dispensers"].set_index("dispenser_id")["type"].to_dict()
    rd = rd[rd["dispenser_id"].map(kind) == "Hand soap"]
    rd["unit"] = rd["dispenser_id"].map(disp).map(lambda u: wards.get(u, u))
    if sum_quantity:
        wall = rd.groupby("unit")["quantity"].apply(lambda q: q.astype(int).sum()).to_dict()
    else:
        wall = rd.groupby("unit").size().to_dict()
    bd = bed_days(d, m if map_s1a else dict(m, ward={k: k for k in m["ward"]}))
    out_l, out_r = {}, {}
    for c in K.WARD:
        litres = float(bottles.get(c, 0.0)) + cartridge * float(wall.get(c, 0))
        out_l[c] = r1(litres)
        out_r[c] = r1(litres / bd[c] * 1000.0) if bd.get(c) else None
    return dict(litres=out_l, rate=out_r, bottles=bottles, wall=wall, bed_days=bd)


def golden(target):
    a = hobsi(target)
    b = hand_rub(target)
    c = hand_soap(target)
    return dict(A=a, B=b, C=c)


def stops(target):
    """each ask's ladder: the routes that file other figures"""
    return dict(
        A_request_location=hobsi(target, attribute="request"),
        A_retired_numbers_dropped=hobsi(target, link_retired=False),
        A_every_culture=hobsi(target, episodes=False),
        A_commensal_single=hobsi(target, commensal_rule=False),
        A_s1a_unmapped=hobsi(target, map_s1a=False),
        A_episodes_within_each_admission=hobsi(target, episode_by="admission"),
        A_episodes_within_each_stay=hobsi(target, episode_by="stay"),
        A_each_admission_its_own_stay=hobsi(target, stay_gap=None),
        A_admissions_a_day_apart_joined=hobsi(target, stay_gap=24 * 60),
        B_copies_kept=hand_rub(target, drop_copies=False),
        B_same_minute_all_year=hand_rub(target, copy_window=None),
        B_one_refill_a_day=hand_rub(target, drop_copies=False, one_a_day=True),
        B_carton_as_bottle=hand_rub(target, carton_as_bottle=True),
        B_returns_left_out=hand_rub(target, returns=False),
        B_s1a_unmapped=hand_rub(target, map_s1a=False),
        C_copies_kept=hand_soap(target, drop_copies=False),
        C_same_minute_all_year=hand_soap(target, copy_window=None),
        C_job_quantity_summed=hand_soap(target, sum_quantity=True),
        C_copies_kept_and_quantity_summed=hand_soap(target, drop_copies=False, sum_quantity=True),
        C_cartridge_as_a_litre=hand_soap(target, cartridge=1.0),
        C_s1a_unmapped=hand_soap(target, map_s1a=False),
    )
