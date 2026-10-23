"""The records each organisation keeps, written from the clean truth in world.py, with the mess its own systems
produce (the 2020 CIS conversion, meter exchanges, estimated reads and their true-ups, cancelled and re-issued bills,
two GSA report layouts, a feeder moved between substations, the delivery-point meters' own clock).

Every frame here is what the pack writer serialises; nothing in this module computes an answer."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np
import pandas as pd

import common as C
import world as Wd

ROADS = ["Road 14", "Road 16", "Road 19", "Road 22", "Road 23", "Road 27", "Road 31", "Road 34", "Avenue 9",
         "Avenue 12", "Avenue 15", "Avenue 18", "Avenue 21", "Levee Road", "Gaither Lane", "Ostrom Road",
         "Bottoms Road", "Lone Bench Road", "Corwin Road", "Mill Slough Road", "Kessler Road", "Pruett Lane",
         "Dunsmore Road", "Hatch Road"]


CLEAN = False      # checks.py sets this to cut the clean-truth pack: no Layer 1 mess on the call's records


def rng(tag):
    return Wd.rng("rec:" + tag)


# ---------------------------------------------------------------- identities
def holder_names(n, tag):
    from faker import Faker
    r = rng("names" + tag)
    pools = []
    for loc, w in (("en_US", 0.55), ("es_MX", 0.22), ("pt_PT", 0.13), ("it_IT", 0.10)):
        f = Faker(loc)
        f.seed_instance(int(r.integers(1, 10 ** 9)))
        pools.append((f, w))
    out, seen = [], set()
    forms = ["{L} Ranch", "{L} Farms", "{L} Family Trust", "{F}. & {G}. {L}", "{L} Bros.", "{L} Farms LLC",
             "{L} Orchards", "{L} Land Co.", "{F}. {L}", "{L} Family Partnership", "{L} & Sons",
             "{L} Ranch LP", "{F}. {L} Trust"]
    while len(out) < n:
        f = pools[int(r.choice(len(pools), p=[w for _, w in pools]))][0]
        last = f.last_name().split()[0].replace(",", "")
        first = f.first_name()[0]
        second = f.first_name()[0]
        form = forms[int(r.integers(0, len(forms)))]
        nm = form.format(L=last, F=first, G=second)
        if nm in seen:
            continue
        seen.add(nm)
        out.append(nm)
    return out


def make_ids(W):
    r = rng("ids")
    nJ, nS = W.nJ, W.nS
    n = nJ + nS + 7                       # seven services closed before 2019 ride along in the history
    svc = r.choice(np.arange(100100, 189900), n, replace=False)
    ids = {}
    ids["svcJ"] = [str(x) for x in svc[:nJ]]
    ids["svcS"] = [str(x) for x in svc[nJ:nJ + nS]]
    ids["svcX"] = [str(x) for x in svc[nJ + nS:]]
    legacy = r.choice(np.arange(10000, 99999), n, replace=False)
    ids["legacy"] = {s: "%02d-%05d-%d" % (int(r.integers(1, 9)), int(l), int(r.integers(0, 9)))
                     for s, l in zip(ids["svcJ"] + ids["svcS"] + ids["svcX"], legacy)}
    newacct = r.choice(np.arange(4100000000, 4100999999), n, replace=False)
    ids["acct"] = {s: str(a) for s, a in zip(ids["svcJ"] + ids["svcS"] + ids["svcX"], newacct)}
    ids["holdJ"] = holder_names(nJ, "J")
    ids["holdS"] = holder_names(nS + 3, "S")
    # assessor parcels: Lone Bench lands in books 045 to 049, bottomlands in books 031 to 034
    def apns(k, books):
        out = []
        used = set()
        for i in range(k):
            m = int(r.choice([1, 1, 1, 2, 2, 3, 4]))
            cur = []
            while len(cur) < m:
                a = "%03d-%03d-%03d" % (int(r.choice(books)), int(r.integers(10, 400)), int(r.integers(1, 60)))
                if a not in used:
                    used.add(a)
                    cur.append(a)
            out.append(cur)
        return out
    ids["apnJ"] = apns(nJ, [45, 46, 47, 48, 49])
    ids["apnS"] = apns(nS, [31, 32, 33, 34])
    wells = set()
    def wellno(twn, rngw):
        while True:
            w = "%02dN%02dW%02d%s%03dM" % (twn, rngw, int(r.integers(1, 37)), "ABCDEFGHJKLMNPQR"[int(r.integers(0, 16))],
                                         int(r.integers(1, 6)))
            if w not in wells:
                wells.add(w)
                return w
    ids["wellJ"] = [wellno(int(r.choice([14, 15])), int(r.choice([2, 3, 4]))) for _ in range(nJ)]
    ids["wellS"] = [wellno(int(r.choice([12, 13])), int(r.choice([3, 4, 5]))) if W.S["well"][i] else ""
                    for i in range(nS)]
    ids["rightS"] = ["D-%04d" % x for x in r.choice(np.arange(40, 2400), nS, replace=False)]
    ids["podS"] = ["VR-%03d" % x for x in r.choice(np.arange(100, 999), nS, replace=False)]
    ids["roadJ"] = [ROADS[int(r.integers(0, len(ROADS)))] for _ in range(nJ)]
    ids["roadS"] = [ROADS[int(r.integers(0, len(ROADS)))] for _ in range(nS)]
    ids["noJ"] = [int(r.integers(1000, 9999)) for _ in range(nJ)]
    ids["noS"] = [int(r.integers(1000, 9999)) for _ in range(nS)]
    # feeders
    fdr = {"RIVERSIDE": ["1201", "1202", "1203", "1204"], "MILL SLOUGH": ["2201", "2202", "2203"],
           "BENCH": ["3201", "3202", "3203", "3204", "3205"], "CORWIN ROAD": ["4201", "4202", "4203", "4204"]}
    ids["fdr_of_dp"] = fdr
    fJ = [str(r.choice(fdr[dp], p=[0.23, 0.21, 0.22, 0.13, 0.21])) if dp == "BENCH" else fdr[dp][int(r.integers(0, len(fdr[dp])))]
          for dp in W.J["dp"]]
    fS = []
    for dp in W.S["dp"]:
        if dp == "RIVERSIDE":
            fS.append(r.choice(fdr[dp], p=[0.30, 0.27, 0.27, 0.16]))
        else:
            fS.append(fdr[dp][int(r.integers(0, len(fdr[dp])))])
    ids["fdrJ"] = fJ
    ids["fdrS"] = [str(x) for x in fS]
    return ids


TRANSFER_FEEDER = "1204"
TRANSFER_DATE = dt.date(2026, 3, 16)
TRANSFER2_FEEDER = "3204"
TRANSFER2_DATE = dt.date(2025, 11, 3)


def feeder_dp(feeder, day):
    """Where a feeder was supplied from on a day (the OMS record)."""
    base = {"12": "RIVERSIDE", "22": "MILL SLOUGH", "32": "BENCH", "42": "CORWIN ROAD"}[feeder[:2]]
    if feeder == TRANSFER_FEEDER and day >= TRANSFER_DATE:
        return "MILL SLOUGH"
    if feeder == TRANSFER2_FEEDER and day >= TRANSFER2_DATE:
        return "CORWIN ROAD"
    return base


# ---------------------------------------------------------------- billing
def month_end(y, m):
    return dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)


def billing(W, ids):
    r = rng("billing")
    rows = []
    services = [(s, "J", i) for i, s in enumerate(ids["svcJ"])] + [(s, "S", i) for i, s in enumerate(ids["svcS"])]
    # closed services: four bench wells and three bottomland plants that left the rate before 2019
    closed = {}
    for k, s in enumerate(ids["svcX"]):
        typ = "J" if k < 4 else "S"
        close = dt.date(int(r.choice([2016, 2017, 2018])), int(r.integers(1, 13)), 1)
        closed[s] = (typ, close, int(r.integers(0, W.nJ if typ == "J" else W.nS)), float(r.uniform(0.4, 1.2)))
    ids["closed"] = closed
    mult = {}
    for s, typ, i in services:
        hp_big = (typ == "J" and W.J["acres"][i] > 220)
        mult[s] = int(r.choice([40, 80])) if hp_big else 1
    for s, (typ, close, i, f) in closed.items():
        mult[s] = 1
    meter = {}
    reg = {}
    def new_meter(s):
        m = "S%07d" % int(r.integers(1000000, 9999999))
        meter[s] = m
        reg[m] = int(r.integers(1000, 90000))
        return m
    for s in list(mult):
        new_meter(s)
    exch = set(r.choice([s for s, _, _ in services], 26, replace=False))
    exch_month = {s: (int(r.choice([2017, 2018, 2019])), int(r.integers(1, 13))) for s in exch}
    cancel = set()
    est = {}
    def line(s, y, m, kwh, rtype, status, mtr, start=None, end=None):
        mm = mult[s]
        adv = int(round(kwh / mm))
        prev = reg[mtr]
        reg[mtr] = prev + adv
        legacy = y < 2020 and not CLEAN
        rows.append({
            "acct_no": ids["legacy"][s] if legacy else ids["acct"][s],
            "svc_no": "" if legacy else s,
            "rate": "IP",
            "bill_month": "%04d-%02d" % (y, m),
            "read_start": (start or dt.date(y, m, 1)).isoformat(),
            "read_end": (end or month_end(y, m)).isoformat(),
            "meter_no": mtr,
            "prev_read": prev,
            "curr_read": prev + adv,
            "mult": mm,
            "kwh": adv * mm,
            "read_type": rtype,
            "bill_status": status,
        })
        return adv * mm
    for (y, m) in W.months:
        for s, typ, i in services:
            kwh = float((W.J_kwh if typ == "J" else W.S_kwh)[(y, m)][i])
            mtr = meter[s]
            if s in exch and exch_month[s] == (y, m) and not CLEAN:
                cut = int(r.integers(5, 25))
                a = kwh * cut / month_end(y, m).day
                line(s, y, m, a, "A", "BILLED", mtr, end=dt.date(y, m, cut))
                mtr = new_meter(s)
                line(s, y, m, kwh - a, "A", "BILLED", mtr, start=dt.date(y, m, cut))
                continue
            carry = est.pop(s, None)
            if carry is not None:
                kwh = kwh + carry
            if m in (5, 6, 7) and carry is None and r.random() < 0.012 and not CLEAN and y not in (2022, 2026):
                e = kwh * float(r.uniform(0.8, 1.2))
                line(s, y, m, e, "E", "BILLED", mtr)
                est[s] = kwh - e
                continue
            if 2016 <= y <= 2019 and r.random() < 0.0009 and not CLEAN:
                wrong = kwh * float(r.uniform(1.3, 1.9))
                billed = line(s, y, m, wrong, "A", "CANCELLED", mtr)
                rows.append(dict(rows[-1], kwh=-billed, prev_read=rows[-1]["curr_read"], curr_read=rows[-1]["prev_read"],
                                 bill_status="CANCEL"))
                reg[mtr] = rows[-1]["curr_read"]
                line(s, y, m, kwh, "A", "REBILL", mtr)
                cancel.add(s)
                continue
            line(s, y, m, kwh, "A", "BILLED", mtr)
        for s, (typ, close, i, f) in closed.items():
            if dt.date(y, m, 1) >= close:
                continue
            kwh = float((W.J_kwh if typ == "J" else W.S_kwh)[(y, m)][i]) * f
            line(s, y, m, kwh, "A", "BILLED", meter[s])
    df = pd.DataFrame(rows)
    ids["meter_exchanges"] = sorted(exch)
    return df


# ---------------------------------------------------------------- register, crosswalk, GIS, OMS
def register(W, ids):
    r = rng("register")
    rows = []
    for i, s in enumerate(ids["svcJ"]):
        hp = int(5 * round(W.J["need_n"][i] * W.J["k"][i] / 2400 / 5 + 0.5)) + 5
        hp = max(hp, 30)
        rows.append({"svc_no": s, "acct_no": ids["acct"][s], "rate": "IP", "status": "ACTIVE",
                     "premise": "%d %s" % (ids["noJ"][i], ids["roadJ"][i]), "apn": "; ".join(ids["apnJ"][i]),
                     "customer": ids["holdJ"][i], "plant": "WELL %d HP" % hp, "connected_hp": hp,
                     "connect_date": dt.date(int(r.integers(1979, 2015)), int(r.integers(1, 13)), 1).isoformat(),
                     "close_date": ""})
    for i, s in enumerate(ids["svcS"]):
        hr = int(5 * max(2, round(W.S["need_n"][i] * W.S["kr"][i] / 1300 / 5)))
        if W.S["well"][i]:
            hw = int(5 * max(3, round(W.S["need_n"][i] * W.S["kw"][i] / 1500 / 5)))
            plant, chp = "RIVER LIFT %d HP + WELL %d HP" % (hr, hw), hr + hw
        else:
            plant, chp = "RIVER LIFT %d HP" % hr, hr
        rows.append({"svc_no": s, "acct_no": ids["acct"][s], "rate": "IP", "status": "ACTIVE",
                     "premise": "%d %s" % (ids["noS"][i], ids["roadS"][i]), "apn": "; ".join(ids["apnS"][i]),
                     "customer": ids["holdS"][i], "plant": plant, "connected_hp": chp,
                     "connect_date": dt.date(int(r.integers(1962, 2012)), int(r.integers(1, 13)), 1).isoformat(),
                     "close_date": ""})
    for s, (typ, close, i, f) in ids["closed"].items():
        rows.append({"svc_no": s, "acct_no": ids["acct"][s], "rate": "IP", "status": "CLOSED",
                     "premise": "%d %s" % (int(r.integers(1000, 9999)), ROADS[int(r.integers(0, len(ROADS)))]),
                     "apn": "%03d-%03d-%03d" % (int(r.choice([31, 46])), int(r.integers(10, 400)), int(r.integers(1, 60))),
                     "customer": ids["holdS"][-1 - (len(rows) % 3)] if typ == "S" else holder_names(1, s)[0],
                     "plant": "WELL 60 HP" if typ == "J" else "RIVER LIFT 15 HP",
                     "connected_hp": 60 if typ == "J" else 15,
                     "connect_date": "1988-05-01", "close_date": close.isoformat()})
    df = pd.DataFrame(rows).sort_values("svc_no").reset_index(drop=True)
    return df


def crosswalk(ids):
    rows = [{"legacy_acct_no": ids["legacy"][s], "acct_no": ids["acct"][s], "svc_no": s, "converted": "2020-01-06"}
            for s in ids["svcJ"] + ids["svcS"]]
    for s, (typ, close, i, f) in ids["closed"].items():
        rows.append({"legacy_acct_no": ids["legacy"][s], "acct_no": "", "svc_no": s, "converted": ""})
    return pd.DataFrame(rows).sort_values("legacy_acct_no").reset_index(drop=True)


def service_points(W, ids):
    """GIS service points as of 30 September 2026; the substation column was set when each point was mapped."""
    r = rng("gis")
    rows = []
    for i, s in enumerate(ids["svcJ"]):
        f = ids["fdrJ"][i]
        rows.append({"svc_no": s, "xfmr_id": "T%s-%03d" % (f, int(r.integers(1, 400))), "feeder": f,
                     "substation": feeder_dp(f, dt.date(2015, 1, 1))})
    for i, s in enumerate(ids["svcS"]):
        f = ids["fdrS"][i]
        rows.append({"svc_no": s, "xfmr_id": "T%s-%03d" % (f, int(r.integers(1, 400))), "feeder": f,
                     "substation": feeder_dp(f, dt.date(2015, 1, 1))})
    return pd.DataFrame(rows).sort_values(["feeder", "svc_no"]).reset_index(drop=True)


def feeder_sources(ids):
    rows = []
    for dp, fs in ids["fdr_of_dp"].items():
        for f in fs:
            if f == TRANSFER_FEEDER:
                rows.append({"feeder": f, "source_dp": C.DP_CODES["RIVERSIDE"], "source_bus": "RIVERSIDE 12.47 KV BUS 2",
                             "effective_from": "2009-06-02", "effective_to": "2026-03-15", "order_no": "SO-09-118"})
                rows.append({"feeder": f, "source_dp": C.DP_CODES["MILL SLOUGH"], "source_bus": "MILL SLOUGH 12.47 KV BUS 1",
                             "effective_from": "2026-03-16", "effective_to": "", "order_no": "SO-26-031"})
            elif f == TRANSFER2_FEEDER:
                rows.append({"feeder": f, "source_dp": C.DP_CODES["BENCH"], "source_bus": "BENCH 12.47 KV BUS 1",
                             "effective_from": "2009-06-02", "effective_to": "2025-11-02", "order_no": "SO-09-118"})
                rows.append({"feeder": f, "source_dp": C.DP_CODES["CORWIN ROAD"], "source_bus": "CORWIN ROAD 12.47 KV BUS 2",
                             "effective_from": "2025-11-03", "effective_to": "", "order_no": "SO-25-207"})
            else:
                rows.append({"feeder": f, "source_dp": C.DP_CODES[dp], "source_bus": "%s 12.47 KV BUS %d" % (dp, 1 + int(f[-1]) % 2),
                             "effective_from": "2009-06-02", "effective_to": "", "order_no": "SO-09-118"})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- water records
def wy_of(y, m):
    return y + 1 if m >= 10 else y


def gsa_reports(W, ids):
    """Annual metered extraction by well and water year (October to September)."""
    r = rng("gsa")
    out = {}
    for wy in C.WY_GSA:
        rows = []
        months = [(wy - 1, m) for m in (10, 11, 12)] + [(wy, m) for m in range(1, 10)]
        for i, s in enumerate(ids["svcJ"]):
            af = sum(float(W.J_af[k][i]) for k in months if k in W.J_af)
            rows.append({"well": ids["wellJ"][i], "apn": ids["apnJ"][i][0], "owner": ids["holdJ"][i],
                         "power": "VVPUD %s" % s, "af": af * float(r.normal(1, 0.015)), "method": "FLOWMETER"})
        for i, s in enumerate(ids["svcS"]):
            if not W.S["well"][i]:
                continue
            af = sum(float(W.S_wa[k][i]) for k in months if k in W.S_wa)
            rows.append({"well": ids["wellS"][i], "apn": ids["apnS"][i][0], "owner": ids["holdS"][i],
                         "power": "VVPUD %s" % s, "af": af * float(r.normal(1, 0.015)), "method": "FLOWMETER"})
        df = pd.DataFrame(rows)
        if wy == 2026:
            # the water year's reports are due 31 October; about a fifth had not come in by the pull
            keep = r.random(len(df)) > 0.06
            if not CLEAN:
                df = df[keep].reset_index(drop=True)
        out[wy] = df
    return out


def diversions(W, ids):
    """Monthly diversion statements: each senior right's river pump, and the district's canal at its dam."""
    r = rng("div")
    rows = []
    for y in C.YEARS:
        for m in C.SEASON:
            for i in range(W.nS):
                af = float(W.S_div[(y, m)][i]) * float(r.normal(1, 0.012))
                rows.append({"right_no": ids["rightS"][i], "pod": ids["podS"][i], "year": y, "month": m,
                             "af_diverted": round(af, 1), "measure": "VVPUD %s" % ids["svcS"][i]})
            lbid = C.LBID_ALLOC[y] * float(W.J["contract"].sum()) * Wd.DELIV_SHARE[m] / 0.86
            rows.append({"right_no": "D-0007", "pod": "LBD-1", "year": y, "month": m,
                         "af_diverted": round(lbid * float(r.normal(1, 0.01)), 1), "measure": "CANAL GAUGE LB-1"})
    return pd.DataFrame(rows)


def allotments(W, ids):
    r = rng("allot")
    rows = [{"right_no": "D-0007", "class": "POST-1914 APPROPRIATIVE", "priority": "1921-04-11",
             "holder": "Lone Bench Irrigation District", "pod": "LBD-1", "place_of_use": "LBID service area",
             "season_allotment_af": int(round(W.J["contract"].sum() / 0.86, -2))}]
    for i in range(W.nS):
        cls = "RIPARIAN" if r.random() < 0.62 else "PRE-1914 APPROPRIATIVE"
        pri = "" if cls == "RIPARIAN" else dt.date(int(r.integers(1856, 1913)), int(r.integers(1, 13)), int(r.integers(1, 28))).isoformat()
        rows.append({"right_no": ids["rightS"][i], "class": cls, "priority": pri, "holder": ids["holdS"][i],
                     "pod": ids["podS"][i], "place_of_use": "; ".join(ids["apnS"][i]),
                     "season_allotment_af": int(W.S["allot"][i])})
    return pd.DataFrame(rows).sort_values("right_no").reset_index(drop=True)


def lbid(W, ids):
    con = pd.DataFrame({"landowner": ids["holdJ"], "apn": ["; ".join(a) for a in ids["apnJ"]],
                        "contract_af": W.J["contract"]})
    al = pd.DataFrame([{"season": y, "allocation_pct": int(round(100 * C.LBID_ALLOC[y])),
                        "announced": dt.date(y, 3 if C.LBID_ALLOC[y] < 1 else 2, 12 + (y % 9)).isoformat()} for y in C.YEARS])
    return con, al


def eto(W):
    r = rng("eto-qc")
    rows = []
    for d, v in W.eto_daily:
        q = "" if (r.random() > 0.004 or CLEAN) else "M"
        rows.append({"date": d.isoformat(), "eto_in": round(v, 3), "qc": q})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- the PUD's pump test programme (bench wells)
def pump_tests(W, ids):
    """Plants of 75 hp and more on Schedule IP are offered a free test every three years; bench wells only, since
    no bottomland plant reaches the size. Two contractors, two report layouts (the change came with the 2022 bid)."""
    r = rng("ptest")
    old, new = [], []
    for i, s in enumerate(ids["svcJ"]):
        hp_est = W.J["need_n"][i] * W.J["k"][i] / 2400
        if hp_est < 75 or r.random() < 0.18:
            continue
        y0 = int(r.choice([2019, 2020, 2021]))
        for y in range(y0, 2027, 3):
            mo = int(r.choice([1, 2, 3, 11, 12]))
            day = dt.date(y, mo if not (y == 2026 and mo > 9) else mo - 9, int(r.integers(2, 27)))
            swl = W.J["swl"][i] * float(r.normal(1, 0.02)) - (4 if day.month in (1, 2, 3) else 0)
            pwl = swl + W.J["dd"][i] * float(r.normal(1, 0.06))
            dis_psi = W.J["dis"][i] / 2.31 * float(r.normal(1, 0.05))
            tdh = pwl + dis_psi * 2.31
            ope = W.J["ope"][i] * float(r.normal(1, 0.03))
            gpm = float(r.uniform(900, 2400))
            kw = gpm * tdh / 3960 * 0.746 / ope
            kwh_af = 1.0241 * tdh / ope
            rec = {"svc_no": s, "well": ids["wellJ"][i], "test_date": day.isoformat(), "swl_ft": round(swl, 1),
                   "pwl_ft": round(pwl, 1), "dis_psi": round(dis_psi, 1), "tdh_ft": round(tdh, 1), "gpm": int(round(gpm)),
                   "kw_input": round(kw, 1), "ope": ope, "kwh_af": round(kwh_af)}
            if y <= 2021:
                old.append({"Service": "IP-" + s, "Well No": rec["well"], "Date": day.strftime("%m/%d/%Y"),
                            "Standing Level (ft)": rec["swl_ft"], "Pumping Level (ft)": rec["pwl_ft"],
                            "Discharge (psi)": rec["dis_psi"], "TDH (ft)": rec["tdh_ft"], "Flow (gpm)": rec["gpm"],
                            "Input kW": rec["kw_input"], "OPE %": round(100 * ope, 1)})
            else:
                new.append({"svc_no": s, "state_well_no": rec["well"], "test_date": rec["test_date"],
                            "swl_ft": rec["swl_ft"], "pwl_ft": rec["pwl_ft"], "discharge_psi": rec["dis_psi"],
                            "tdh_ft": rec["tdh_ft"], "flow_gpm": rec["gpm"], "input_kw": rec["kw_input"],
                            "ope": round(ope, 3), "kwh_per_af": rec["kwh_af"]})
    return pd.DataFrame(old), pd.DataFrame(new)
