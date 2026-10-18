"""Shipped records from the clean truth: the paediatric register in its two systems, the supply-side extracts, and
the call's documents' tables. Every Layer 1 item is applied here and named where it is applied:

  R-L1  the register's migration: legacy rows (ART numbers, day/month/year dates, free-text regimen lines, 0.5 kg on
        paper-captured sites) to 30 June 2024; EPR rows (national patient identifier, ISO dates, regimen codes) from
        1 June 2024; June 2024 in both.
  R-L2  a new ART number at each transfer between facilities in the legacy system, linked by the crosswalk.
  R-L3  medicines collected by a caregiver: a visit with no weighing.
  R-L4  EPR encounters re-sent by a clinic tablet after a failed sync: a second row under a new encounter id.
  R-L5  outcomes entered weeks after the outcome date; the extract holds those entered by the pull.
  R-L6  dates of birth estimated (1 July of the year) for part of the late-diagnosed cohort.
  S-L1  CMS's customer master keeps the delivery region each account was opened with.
  S-L2  a delivery is posted when picked and signed for days later.
  S-L3  the Northern depot's restocking from the Main warehouse in the same delivery export.
  S-L4  logistics reports returned by the district reviewer and resubmitted; every submission in the export.
  S-L5  the reporting region stamped from the requisition group at submission.
  S-L6  registry codes reissued from closed sites to new ones."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as C
import world as WD
import world_log as WL
import views as VW

D = dt.date
DAYS = dt.timedelta


def _luhn(s):
    tot = 0
    for k, ch in enumerate(reversed(s)):
        d = int(ch)
        if k % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        tot += d
    return str((10 - tot % 10) % 10)


def ids(W, rng):
    N = W["N"]
    base = rng.choice(np.arange(310_000_000, 899_999_999, 7), N, replace=False)
    W["upid"] = [str(int(b)) + _luhn(str(int(b))) for b in base]


def dob_recorded(W, rng):
    """R-L6: a fifth of the late-diagnosed cohort has its date of birth recorded as 1 July of the year."""
    out = []
    est = []
    for i in range(W["N"]):
        d = VW.dob_of(W, i)
        e = bool(W["kind"][i] == 1 and rng.random() < 0.2)
        out.append(D(d.year, 7, 1) if e else d)
        est.append(e)
    W["dob_rec"] = out
    W["dob_est"] = est


def register(W, rng):
    """The register's rows. Returns legacy visits, EPR visits, the patient master, the crosswalk, and the clean view
    (one row per real visit, keyed by the child) that the call's computation reads once the mess is undone."""
    F = W["F"]
    V = W["V"]
    N = W["N"]
    VW.outcome_dates(W)
    ids(W, rng)
    dob_recorded(W, rng)
    mfl = [f["mfl"] for f in F]
    paper = [f["paper"] for f in F]
    # legacy ART numbers: one per child per facility (R-L2)
    serial = {}
    artno = {}
    reg_text = {r[0]: r[4] for r in C.REGIMENS}
    t_lo, t_hi = C.month_of(C.SHIP_FROM), C.M_COUNT
    order = np.lexsort((V["t"], V["i"]))
    leg, epr, clean = [], [], []
    enc = 41_300_000
    recno = 2_100_000
    for k in order:
        t = int(V["t"][k])
        if t < t_lo or t > t_hi:
            continue
        i = int(V["i"][k])
        d = WD.visit_date(W, i, t)
        if d > C.COUNT:
            continue
        fac = int(V["fac"][k])
        w = V["w"][k]
        reg = V["reg"][k]
        cad = int(V["cad"][k])
        nxt = VW.add_months(d, cad)
        clean.append((i, d, w, reg, cad, nxt, mfl[fac]))
        if d <= C.LEGACY_END:
            key = (i, fac)
            if key not in artno:
                serial[fac] = serial.get(fac, 0) + int(rng.integers(1, 4))
                artno[key] = "%s-%05d" % (mfl[fac], 300 + serial[fac])
            recno += int(rng.integers(1, 3))
            leg.append(dict(record_no="LR%07d" % recno, art_no=artno[key], facility_code=mfl[fac],
                            visit_date=d.strftime("%d/%m/%Y"),
                            weight_kg="" if w != w else ("%.1f" % w),
                            regimen=reg_text[reg], months_dispensed=cad, next_visit=nxt.strftime("%d/%m/%Y"),
                            visit_type="P" if w != w else "C"))
        if d >= C.EPR_LIVE:
            enc += int(rng.integers(1, 6))
            hh = int(rng.integers(7, 16))
            sync = dt.datetime(d.year, d.month, d.day, hh, int(rng.integers(0, 60)), int(rng.integers(0, 60)))
            sync += dt.timedelta(minutes=int(rng.integers(5, 300)))
            row = dict(encounter_id="E%08d" % enc, upid=W["upid"][i], facility_code=mfl[fac], visit_date=d.isoformat(),
                       encounter_type="Medication collection" if w != w else "Clinical visit",
                       weight_kg="" if w != w else ("%.1f" % w), regimen_code=reg, months_dispensed=cad,
                       next_appointment=nxt.isoformat(), synced_at=sync.strftime("%Y-%m-%dT%H:%M:%SZ"))
            epr.append(row)
            if rng.random() < 0.012:                      # R-L4
                enc += int(rng.integers(1, 6))
                r2 = dict(row)
                r2["encounter_id"] = "E%08d" % enc
                s2 = sync + dt.timedelta(hours=int(rng.integers(20, 160)), minutes=int(rng.integers(0, 60)))
                r2["synced_at"] = s2.strftime("%Y-%m-%dT%H:%M:%SZ")
                epr.append(r2)
    # patient master (as the EPR holds it at the pull): every child with a visit in the extract
    seen = sorted(set(r[0] for r in clean))
    pts = []
    for i in seen:
        od, po = W["odate"][i], W["oposted"][i]
        known = od is not None and po <= C.PULL and od <= C.COUNT
        y, m = C.ym(int(W["enrol"][i]))
        st = D(y, m, int(1 + (i * 104729) % 28))
        last_fac = int(W["fac1"][i]) if (W["tr_month"][i] >= 0 and W["tr_month"][i] <= C.M_COUNT) else int(W["fac0"][i])
        xt = {"LTFU": "Lost to follow-up", "TO": "Transferred out", "DIED": "Died", "ADULT": "Transferred to adult care"}
        pts.append(dict(upid=W["upid"][i], sex="F" if W["sex"][i] == 0 else "M",
                        date_of_birth=W["dob_rec"][i].isoformat(), dob_estimated="Y" if W["dob_est"][i] else "N",
                        art_start_date=st.isoformat(), current_facility=mfl[last_fac],
                        outcome=xt[W["xtype"][i]] if known else "",
                        outcome_date=od.isoformat() if known else "",
                        outcome_entered=po.isoformat() if known else ""))
    cw = [dict(art_no=v, upid=W["upid"][i], facility_code=mfl[f]) for (i, f), v in sorted(artno.items(), key=lambda x: x[1])]
    return leg, epr, pts, cw, clean


def clean_view(W, clean):
    """The view the call's computation reads: one row per real visit, keyed by the child, the register's recorded
    date of birth and outcomes as entered by the pull."""
    rows = [(i, d, w, reg, cad, nxt) for (i, d, w, reg, cad, nxt, f) in clean]
    visits = pd.DataFrame(rows, columns=["uid", "date", "weight", "regimen", "months", "next_appt"])
    kids = []
    for i in sorted(set(visits.uid)):
        od, po = W["odate"][i], W["oposted"][i]
        known = od is not None and po <= C.PULL and od <= C.COUNT
        y, m = C.ym(int(W["enrol"][i]))
        kids.append(dict(uid=i, dob=W["dob_rec"][i], sex="F" if W["sex"][i] == 0 else "M",
                         art_start=D(y, m, int(1 + (i * 104729) % 28)),
                         outcome=W["xtype"][i] if known else None, outcome_date=od if known else None))
    return pd.DataFrame(kids), visits


# ------------------------------------------------------------------------------------------------ supply side
def supply(W, rng):
    """Registry, accounts, deliveries, PODs and logistics reports, July 2025 to August 2026."""
    F = W["F"]
    child_fac = set(int(x) for x in W["fac0"]) | set(int(x) for x in W["fac1"][W["tr_month"] >= 0])
    recs, old, new = WL.registry(F, rng, child_fac)
    adults = WL.adults_by_site(recs, rng)
    # the register's children under 15 on TLD at each site at each month end (from the clean truth)
    kids_tld = {}
    V = W["V"]
    for (y, m) in WL.LOG_MONTHS:
        t = C.mi(y, m)
        tld = (W["switch"] <= t) & ~W["second"] & (W["exitm"] > t) & ((t - W["bm"]) / 12 < 15)
        idx = np.where(tld)[0]
        fac = np.where((W["tr_month"][idx] >= 0) & (W["tr_month"][idx] <= t), W["fac1"][idx], W["fac0"][idx])
        for f in fac:
            kids_tld[(int(f), y, m)] = kids_tld.get((int(f), y, m), 0) + 1
    pats = WL.monthly_patients(recs, adults, kids_tld, rng)
    disp, close, opening, recv, dels, don = WL.flows(recs, pats, rng)
    proj = WL.projection(recs, adults, rng)
    batches, ship = WL.cms_stock(rng)
    return dict(recs=recs, old=old, new=new, adults=adults, pats=pats, disp=disp, close=close, opening=opening,
                recv=recv, dels=dels, don=don, proj=proj, batches=batches, ship=ship)


def accounts(S, rng):
    """S-L1: one CMS customer account per site, numbered in the order accounts were opened, carrying the delivery
    region and route set when it was opened; the reissued codes' new sites get new accounts."""
    recs = S["recs"]
    acc = {}
    rows = []
    n = 400_117
    order = sorted(recs, key=lambda r: (r["opened"], r["rid"]))
    routes = {}
    for r in order:
        n += int(rng.integers(3, 40))
        lag = int(rng.integers(5, 60))
        # accounts carried over at the warehouse system's go-live in March 2009; a site opened since then has its
        # account set up a few weeks before its opening stock is sent
        created = (D(2009, 3, 1) + DAYS(days=lag) if r["opened"] < D(2009, 3, 1)
                   else max(D(2009, 3, 2), r["opened"] - DAYS(days=14 + lag // 2)))
        reg = WL.region_at(r, created)
        rc = "%s-%02d" % (r["district"], 1 + (r["rid"] % 3))
        short = {"District hospital": "DH", "Mission hospital": "MH", "Health centre": "HC", "Clinic": "CLN",
                 "Private clinic": "PVT"}[r["type"]]
        acc[r["rid"]] = str(n)
        rows.append(dict(account=str(n), account_name="%s %s" % (short, r["mfl"]), mfl_code=r["mfl"],
                         delivery_region=reg, route=rc, opened_on=created.isoformat(),
                         status="Closed" if r["closed"] is not None else "Active",
                         closed_on=(r["closed"] + DAYS(days=int(rng.integers(3, 20)))).isoformat() if r["closed"] else ""))
    rows.append(dict(account="900120", account_name="CMS NORTHERN DEPOT", mfl_code="", delivery_region="Northern",
                     route="DEPOT", opened_on="2019-05-06", status="Active", closed_on=""))
    S["acc"] = acc
    return sorted(rows, key=lambda x: x["account"])


def deliveries(S, rng):
    """Delivery lines (S-L2, S-L3) and PODs. The Main warehouse (plant M01) serves every route but the Northern and
    Eastern, which the Northern depot (N01) serves from stock the Main warehouse transfers to it."""
    recs = {r["rid"]: r for r in S["recs"]}
    acc = S["acc"]
    lines, pods = [], []
    dn = 80_412_000
    dep_need = {}
    for d in sorted(S["dels"], key=lambda x: (x["posted"], x["rid"])):
        r = recs[d["rid"]]
        plant = "N01" if r["region"] in ("Northern", "Eastern") or r["region_old"] in ("Northern",) else "M01"
        dn += int(rng.integers(1, 9))
        q = d["qty"]
        if q < 600 or rng.random() < 0.7:
            parts = [q]
        else:
            # a delivery picked from two batches: the second batch's share in whole cartons of 12, the rest from the
            # first (the second draw is kept so the stream of later draws stands as it was)
            share, _ = int(rng.integers(30, 70)), int(rng.integers(30, 70))
            x = (q * share // 100) // 12 * 12
            parts = [q - x, x] if 0 < x < q else [q]
        for it, pq in enumerate(parts):
            lines.append(dict(delivery_no=str(dn), item=10 * (it + 1), plant=plant, delivery_type="LF",
                              posting_date=d["posted"].isoformat(), customer=acc[d["rid"]],
                              material="ARV0412", batch="TL%02d%04d" % (25 + (it % 2), int(rng.integers(1000, 9999))),
                              qty=int(pq)))
        sb = d["reason"] if d.get("refused") else ["Pharmacist", "Pharmacy assistant", "Nurse in charge",
                                                    "Facility manager"][int(rng.integers(0, 4))]
        pods.append(dict(delivery_no=str(dn), customer=acc[d["rid"]], signed_on=d["signed"].isoformat(), signed_by=sb,
                         vehicle="GVC %03d %s" % (int(rng.integers(100, 999)), ["CMS", "CMS", "NTH"][int(rng.integers(0, 3))])))
        if d.get("refused"):
            dn2 = dn + 500_000
            lines.append(dict(delivery_no=str(dn2), item=10, plant=plant, delivery_type="LR",
                              posting_date=d["returned"].isoformat(), customer=acc[d["rid"]], material="ARV0412",
                              batch=lines[-1]["batch"], qty=int(q)))
        if plant == "N01":
            key = (d["posted"].year, d["posted"].month)
            dep_need[key] = dep_need.get(key, 0) + q
    # S-L3: the depot's restocking, two transfers a month sized on the month's depot deliveries
    for (y, m), q in sorted(dep_need.items()):
        for half in (0, 1):
            dn += int(rng.integers(1, 9))
            pd_ = D(y, m, 4 + 14 * half + int(rng.integers(0, 5)))
            qq = int(q * (0.5 + float(rng.normal(0, 0.04)))) // 96 * 96
            lines.append(dict(delivery_no=str(dn), item=10, plant="M01", delivery_type="NL",
                              posting_date=pd_.isoformat(), customer="900120", material="ARV0412",
                              batch="TL25%04d" % int(rng.integers(1000, 9999)), qty=qq))
            pods.append(dict(delivery_no=str(dn), customer="900120", signed_on=(pd_ + DAYS(days=int(rng.integers(1, 3)))).isoformat(),
                             signed_by="Depot storekeeper", vehicle="GVC %03d CMS" % int(rng.integers(100, 999))))
    return lines, pods


OTHER_PRODUCTS = [
    ("ARV0388", "ABC/3TC 600/300 mg tablets, 30", 0.050),
    ("ARV0391", "ABC/3TC 120/60 mg dispersible tablets, 60", 0.030),
    ("ARV0407", "DTG 10 mg dispersible tablets, 90", 0.028),
    ("ARV0365", "LPV/r 100/25 mg tablets, 60", 0.009),
]
TLD_CODE = "ARV0412"
TLD_DESC = "TDF/3TC/DTG 300/300/50 mg tablets, 30"
TLD_DON_CODE = "ARV0412D"
TLD_DON_DESC = "TDF/3TC/DTG 300/300/50 mg tablets, 30 (partner donation)"


def lmis(S, rng):
    """Monthly logistics reports, July 2025 to August 2026: one requisition per site and month, a line per product.
    Submitted in the first fortnight of the next month (paper-captured sites later), reviewed days after; four per
    cent returned by the district reviewer and resubmitted (S-L4); the region stamped from the site's requisition
    group on the submission date (S-L5)."""
    recs = S["recs"]
    rows = []
    rep = 7_700_000
    for r in recs:
        for (y, m) in WL.LOG_MONTHS:
            key = (r["rid"], y, m)
            if S["pats"][r["rid"]][WL.LOG_MONTHS.index((y, m))] <= 0 and S["opening"].get(key, 0) <= 0:
                continue
            ny, nm_ = y + (m == 12), m % 12 + 1
            sub = D(ny, nm_, int(rng.integers(1, 13)) + (int(rng.integers(3, 9)) if r["paper"] else 0))
            if sub > C.PULL:
                continue
            tld = dict(opening=S["opening"][key], received=S["recv"][key], dispensed=S["disp"][key])
            loss = max(0, tld["opening"] + tld["received"] - tld["dispensed"] - S["close"][key])
            tld["losses"] = -loss
            tld["closing"] = S["close"][key]
            so = 0 if tld["closing"] > 0.3 * max(1, tld["dispensed"]) else int(rng.integers(0, 6))
            lines = [(TLD_CODE, TLD_DESC, tld, so)]
            for code, desc, share in OTHER_PRODUCTS:
                base = S["pats"][r["rid"]][WL.LOG_MONTHS.index((y, m))] * share * float(rng.lognormal(0, 0.25))
                dsp = int(round(base))
                op = int(round(base * float(rng.uniform(1.5, 3.5))))
                rc = int(round(base * float(rng.uniform(0.0, 2.2))) // 6 * 6)
                ls = -int(rng.integers(0, 3)) if rng.random() < 0.1 else 0
                dsp = min(dsp, op + rc)
                ls = max(ls, -(op + rc - dsp))
                cl = op + rc - dsp + ls
                lines.append((code, desc, dict(opening=op, received=rc, dispensed=dsp, losses=ls, closing=cl), 0))
            dn_ = S["don"].get(key)
            if dn_ is not None:
                lines.insert(1, (TLD_DON_CODE, TLD_DON_DESC, dict(opening=dn_["opening"], received=dn_["received"],
                                                                  dispensed=dn_["dispensed"], losses=0,
                                                                  closing=dn_["closing"]), 0))
            returned = rng.random() < 0.04
            subs = []
            if returned:
                rv = sub + DAYS(days=int(rng.integers(1, 5)))
                subs.append(("Returned", sub, rv, True))
                sub2 = rv + DAYS(days=int(rng.integers(1, 6)))
                subs.append(("Approved", sub2, sub2 + DAYS(days=int(rng.integers(1, 5))), False))
            else:
                subs.append(("Approved", sub, sub + DAYS(days=int(rng.integers(1, 7))), False))
            for status, s_at, r_at, wrong in subs:
                if s_at > C.PULL:
                    continue
                rep += int(rng.integers(1, 7))
                st = status if r_at <= C.PULL else "Submitted"
                region = WL.region_at(r, s_at)
                ts = dt.datetime(s_at.year, s_at.month, s_at.day, int(rng.integers(7, 18)), int(rng.integers(0, 60)))
                for code, desc, q, so_ in lines:
                    qq = dict(q)
                    if wrong and code == TLD_CODE:
                        f = float(rng.choice([0.1, 10.0, 1.0]))
                        if f == 1.0:
                            qq["dispensed"] = q["dispensed"] + int(rng.integers(20, 200))
                        else:
                            qq["dispensed"] = int(round(q["dispensed"] * f))
                        qq["losses"] = qq["closing"] - (qq["opening"] + qq["received"] - qq["dispensed"])
                    rows.append(dict(report_id="RQ%07d" % rep, facility_code=r["mfl"], period="%04d-%02d" % (y, m),
                                     product_code=code, product=desc, opening_balance=qq["opening"],
                                     received=qq["received"], dispensed=qq["dispensed"],
                                     losses_adjustments=qq["losses"], closing_balance=qq["closing"],
                                     stockout_days=so_, region=region,
                                     submitted_at=ts.strftime("%Y-%m-%dT%H:%M"), status=st,
                                     reviewed_on=r_at.isoformat() if r_at <= C.PULL else ""))
    return rows
