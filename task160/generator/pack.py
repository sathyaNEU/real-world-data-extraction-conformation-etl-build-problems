"""Writes the bundle under target/ from the world: Quillfield's extracts as its EHR and finance teams export them,
Corvane's queue export and location map, and the governing documents (docs.py)."""
import datetime as dt
import os
from zoneinfo import ZoneInfo

import numpy as np

import docs
import io_util as IO
import params as P
import world as W

ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
UPGRADE = dt.datetime(2025, 11, 9, 0, 0)
CHUNK_DAYS = [dt.date(2025, 3, 31), dt.date(2025, 6, 30), dt.date(2025, 9, 30), dt.date(2025, 12, 31),
              dt.date(2026, 3, 31), dt.date(2026, 6, 30), dt.date(2026, 9, 30)]

FILES = {
    "history": "QRMC_MedAlertHistory_20250101-20261025.csv",
    "background": "QRMC_MSP26_BackgroundLog_20260706-20261025.csv",
    "census": "QRMC_UnitCensus_Daily_20250101-20261025.csv",
    "plan": "QRMC_FY2027_Inpatient_Volume_Plan.xlsx",
    "register": "QRMC_MedAlert_Rule_Register_20261026.xlsx",
    "release": "MSP26_Content_Release_Notes_v2026.2.pdf",
    "schedule": "Corvane_QRMC_Service_Schedule_B_rev3.pdf",
    "cr": "QRMC_CR-2291_MSP26_HospitalWide_GoLive.docx",
    "queue": "CRV_QueueExport_QRMC_20260630-20261001.csv",
    "pocmap": "CRV_PointOfCare_Map_QRMC.csv",
    "pump": "QRMC_PumpGuardrail_Events_2026Q3.csv",
    "interventions": "QRMC_RPh_Interventions_2026Q3.xlsx",
}
DISTRACTORS = ("pump", "interventions")
UNIT_NAME = {u[0]: u[1] for u in P.UNITS}
RULE_ORDER = {"DDI_SEVERE": 0, "DRUG_ALLERGY": 1, "MAX_DOSE": 2, "DDI_MODERATE": 3, "MSP26_DUP_OPIOID_PRN": 4,
              "MSP26_QT_COMBO": 5}
REASONS = ["Benefit outweighs risk", "Patient has tolerated combination", "Will monitor patient", "Dose appropriate",
           "Comfort care", "Prescriber aware, see note", "Other (see comment)"]
USER_TYPES = ["Physician", "Resident", "Nurse Practitioner", "Physician Assistant"]


def local_str(t):
    """Wall-clock Eastern time as the EHR prints it; a time inside the spring-forward gap reads an hour on."""
    d = W.tstamp(t)
    aware = d.replace(tzinfo=ET)
    if aware.astimezone(UTC).astimezone(ET).replace(tzinfo=None) != d:
        d = d + dt.timedelta(hours=1)
    return d.strftime("%Y-%m-%d %H:%M:%S")


def to_utc(d):
    return d.replace(tzinfo=ET).astimezone(UTC).replace(tzinfo=None)


def old_dept(code):
    return "QRMC " + UNIT_NAME[code].upper()


def relabel(w):
    """Order, alert, background-event and encounter ids as Quillfield's systems issue them, in time order."""
    rng = np.random.default_rng(P.SEED + 1)
    L0 = W.tnum(P.LOG_START)
    L1 = W.tnum(P.LOG_END + dt.timedelta(days=1))
    orders = []
    for e in w["encs"]:
        for o in e.orders:
            orders.append((o[3], o[0]))
    orders.sort()
    oid = {}
    cur = 48210000
    for _t, k in orders:
        cur += int(rng.integers(3, 61))
        oid[k] = cur
    encs = sorted(w["encs"], key=lambda e: (e.adm, e.key))
    csn = {}
    cur = 1104882000
    for e in encs:
        cur += int(rng.integers(1, 10))
        csn[e.key] = cur
    alerts = []
    for e in w["encs"]:
        for r in w["rows"][e.key]:
            if L0 <= r[3] < L1:
                alerts.append((r[3], oid[r[0]], RULE_ORDER[r[1]], oid.get(r[2], 0), e.key, r))
    alerts.sort(key=lambda a: a[:4])
    aid = []
    cur = 912400000
    for a in alerts:
        cur += int(rng.integers(1, 5))
        aid.append(cur)
    bgs = []
    for e in w["encs"]:
        for b in w["bg"][e.key]:
            if b[3] < L1:
                bgs.append((b[3], oid[b[0]], RULE_ORDER[b[1]], oid.get(b[2], 0), e.key, b))
    bgs.sort(key=lambda a: a[:4])
    bid = []
    cur = 7700000
    for _ in bgs:
        cur += int(rng.integers(1, 4))
        bid.append(cur)
    enc_by = {e.key: e for e in w["encs"]}
    drug_of = {}
    for e in w["encs"]:
        for o in e.orders:
            drug_of[o[0]] = o[2]
    return {"oid": oid, "csn": csn, "alerts": alerts, "aid": aid, "bgs": bgs, "bid": bid, "enc_by": enc_by,
            "drug_of": drug_of}


def history_rows(w, R):
    rng = np.random.default_rng(P.SEED + 2)
    rows = []
    for (t, o, _ro, pid, ek, r), a in zip(R["alerts"], R["aid"]):
        e = R["enc_by"][ek]
        stamp = local_str(t)
        dept = e.unit if W.tstamp(t) >= UPGRADE else old_dept(e.unit)
        rule = r[1]
        name, sev = P.RULES[rule]
        action = r[4]
        reason = REASONS[int(rng.integers(len(REASONS)))] if action == "Overridden" else ""
        utype = USER_TYPES[int(rng.integers(len(USER_TYPES)))]
        rows.append([a, stamp, R["csn"][ek], dept, o, r[6], rule, name, sev, pid if pid else "",
                     R["drug_of"][r[2]] if r[2] else "", action, reason, utype])
    out = []
    for i, row in enumerate(rows):
        out.append(row)
        day = dt.date.fromisoformat(row[1][:10])
        nxt = rows[i + 1][1][:10] if i + 1 < len(rows) else None
        if day in CHUNK_DAYS and nxt != row[1][:10]:
            # the next quarter's chunk was pulled from the boundary day again
            j = i
            while j >= 0 and rows[j][1][:10] == row[1][:10]:
                j -= 1
            out.extend(rows[j + 1:i + 1])
    return out


def background_rows(w, R):
    rows = []
    for (t, o, _ro, pid, ek, b), bid in zip(R["bgs"], R["bid"]):
        e = R["enc_by"][ek]
        utc = to_utc(dt.datetime.strptime(local_str(t), "%Y-%m-%d %H:%M:%S"))
        rule = b[1]
        name, sev = P.RULES[rule]
        rows.append(["BG%08d" % bid, utc.strftime("%Y-%m-%dT%H:%M:%SZ"), R["csn"][ek], e.unit, o, b[5], rule, name,
                     sev, pid if pid else "", R["drug_of"][b[2]] if b[2] else "", "Background - not displayed"])
    return rows


def census_rows(w):
    adm, dis = {}, {}
    days = [P.LOG_START + dt.timedelta(days=i) for i in range((P.LOG_END - P.LOG_START).days + 1)]
    mid = {(d, u[0]): 0 for d in days for u in P.UNITS}
    for e in w["encs"]:
        a, b = W.tday(e.adm), W.tday(e.dis)
        adm[(a, e.unit)] = adm.get((a, e.unit), 0) + 1
        dis[(b, e.unit)] = dis.get((b, e.unit), 0) + 1
        d = a
        while d < b:
            if (d, e.unit) in mid:
                mid[(d, e.unit)] += 1
            d += dt.timedelta(days=1)
    rows = []
    for d in days:
        for u in P.UNITS:
            rows.append([d.isoformat(), u[0], adm.get((d, u[0]), 0), dis.get((d, u[0]), 0), mid[(d, u[0])]])
    return rows


def plan_rows():
    rows = []
    start = dt.date(2026, 6, 29)
    for k in range(52):
        wk = start + dt.timedelta(days=7 * k)
        for (code, _n, _t, rate, los, _p) in P.UNITS:
            f = sum(P.SEASON[(wk + dt.timedelta(days=i)).month] for i in range(7))
            pa = int(round(rate * f))
            rows.append([wk, code, pa, int(round(pa * los))])
    return rows


def shift_of(d):
    h = d.hour
    if 7 <= h < 15:
        return "Day"
    if 15 <= h < 23:
        return "Evening"
    return "Night"


def queue_rows(hist):
    """Corvane's desk: one task per message (an order's overridden high-severity alerts at one signing), sessions
    from claim to sign-off or return, stamped in UTC by the queue platform."""
    rng = np.random.default_rng(P.SEED + P.QUEUE_SALT)
    t0 = dt.datetime(2026, 6, 30, 12, 0)
    t1 = dt.datetime(2026, 10, 1, 0, 0)
    seen = set()
    msgs = {}
    for r in hist:
        key = tuple(r)
        if key in seen:
            continue
        seen.add(key)
        if r[8] != "High" or r[11] != "Overridden":
            continue
        d = dt.datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S")
        if not (t0 <= d < t1):
            continue
        msgs.setdefault((r[4], r[1]), []).append(r)
    order = sorted(msgs.items(), key=lambda kv: (kv[0][1], min(x[0] for x in kv[1])))
    pools = {"Day": ["RPH%04d" % n for n in (412, 418, 431, 447, 455, 460, 473, 488, 491, 502)],
             "Evening": ["RPH%04d" % n for n in (415, 426, 439, 444, 468, 479, 497, 506)],
             "Night": ["RPH%04d" % n for n in (421, 433, 452, 484, 499, 511)]}
    wait_mean = {"Day": 9.0, "Evening": 12.0, "Night": 16.0}
    rows = []
    tid = 3318000
    for (_o, stamp), alerts in order:
        tid += int(rng.integers(1, 7))
        first = min(alerts, key=lambda x: x[0])
        unit = first[3]
        fired = dt.datetime.strptime(stamp, "%Y-%m-%d %H:%M:%S")
        recv = fired + dt.timedelta(seconds=int(rng.integers(5, 46)))
        sh = shift_of(recv)
        claim = recv + dt.timedelta(minutes=0.5 + rng.exponential(wait_mean[sh]))
        wing = unit
        for when, a, b in P.DECANT:
            if fired >= when:
                if unit == a:
                    wing = b
                elif unit == b:
                    wing = a
        floor = "".join(ch for ch in unit if ch.isdigit())
        poc = "QRMC^%s^%s%02d^%s" % (wing, floor, int(rng.integers(1, 33)), "AB"[int(rng.integers(2))])
        n = len(alerts)
        rx = rng.random()
        if rx < P.P_RETURN:
            m1 = float(np.clip(rng.lognormal(np.log(4.5), 0.5), 1.0, 30.0))
            close1 = claim + dt.timedelta(minutes=m1)
            reclaim = close1 + dt.timedelta(minutes=1.0 + rng.exponential(15.0))
            m2 = float(np.clip(rng.lognormal(np.log(6.0) + 0.2 * (n - 1), 0.5), 1.5, 45.0))
            close2 = reclaim + dt.timedelta(minutes=m2)
            ph1 = pools[shift_of(claim)][int(rng.integers(len(pools[shift_of(claim)])))]
            cand = [p for p in pools[shift_of(reclaim)] if p != ph1]
            ph2 = cand[int(rng.integers(len(cand)))]
            sess = [(claim, close1, "Returned to queue", m1, ph1),
                    (reclaim, close2, "Signed off", (close2 - claim).total_seconds() / 60.0, ph2)]
        else:
            m = float(np.clip(rng.lognormal(np.log(7.0) + 0.25 * (n - 1), 0.5), 1.5, 60.0))
            close = claim + dt.timedelta(minutes=m)
            ph = pools[shift_of(claim)][int(rng.integers(len(pools[shift_of(claim)])))]
            sess = [(claim, close, "Signed off", m, ph)]
        for i, (c0, c1, status, hm, ph) in enumerate(sess):
            c0s = c0.replace(microsecond=0)
            c1s = c1.replace(microsecond=0)
            rows.append(["T%07d" % tid, i + 1, "%010d" % first[0], poc,
                         to_utc(recv).strftime("%Y-%m-%dT%H:%M:%SZ"), to_utc(c0s).strftime("%Y-%m-%dT%H:%M:%SZ"),
                         to_utc(c1s).strftime("%Y-%m-%dT%H:%M:%SZ"), status,
                         "%.1f" % hm, ph, "QRMC"])
    lo, hi = "2026-06-30T00:00:00Z", "2026-10-02T00:00:00Z"
    return [r for r in rows if lo <= r[6] < hi]


def pocmap_rows():
    rows = [[u[0], u[1], "QRMC", "Adult inpatient", "2024-09-01"] for u in P.UNITS]
    rows += [["ED", "Emergency Department", "QRMC", "Not reviewed by desk", "2024-09-01"],
             ["PACU", "Post-Anesthesia Care Unit", "QRMC", "Not reviewed by desk", "2024-09-01"],
             ["L&D", "Labor and Delivery", "QRMC", "Not reviewed by desk", "2024-09-01"],
             ["OBS", "Observation Unit", "QRMC", "Not reviewed by desk", "2025-02-17"]]
    return sorted(rows, key=lambda r: r[0])


def pump_rows():
    rng = np.random.default_rng(P.SEED + 4)
    libs = ["Heparin 25,000 units/250 mL", "Insulin regular 100 units/100 mL", "Norepinephrine 4 mg/250 mL",
            "Vancomycin 1.25 g/250 mL", "Potassium chloride 20 mEq/100 mL", "Morphine PCA 1 mg/mL",
            "Hydromorphone PCA 0.2 mg/mL", "Magnesium sulfate 2 g/50 mL", "Propofol 10 mg/mL"]
    rows = []
    d = dt.datetime(2026, 7, 1)
    while d < dt.datetime(2026, 10, 1):
        d += dt.timedelta(minutes=float(rng.exponential(46.0)))
        if d >= dt.datetime(2026, 10, 1):
            break
        u = P.UNITS[int(rng.integers(len(P.UNITS)))][0]
        lib = libs[int(rng.integers(len(libs)))]
        lt = ["Soft max", "Soft max", "Soft min", "Hard max"][int(rng.integers(4))]
        resp = ("Reprogrammed" if lt == "Hard max" else
                ["Overrode soft limit", "Reprogrammed", "Cancelled infusion"][int(rng.integers(3))])
        rows.append([d.strftime("%m/%d/%Y %H:%M"), u, "PCU-%05d" % int(rng.integers(10000, 99999)),
                     "ABCD"[int(rng.integers(4))], lib, lt, resp])
    return rows


def intervention_rows():
    rng = np.random.default_rng(P.SEED + 5)
    kinds = ["Renal dose adjustment", "IV to PO conversion", "Therapeutic substitution", "Allergy clarification",
             "Drug interaction management", "Duplicate order clarification", "Pharmacokinetic dosing",
             "Medication reconciliation discrepancy"]
    meds = sum((P.DRUGS[k] for k in ("OTH", "ACG", "QTP", "SED", "OPI")), [])
    rows = []
    d = dt.date(2026, 7, 1)
    while d <= dt.date(2026, 9, 30):
        for _ in range(int(rng.poisson(11))):
            u = P.UNITS[int(rng.integers(len(P.UNITS)))][0]
            rows.append([d, u, kinds[int(rng.integers(len(kinds)))], meds[int(rng.integers(len(meds)))],
                         "Accepted" if rng.random() < 0.86 else "Not accepted", int(rng.integers(5, 41)),
                         ["JKM", "RTP", "ALS", "DWH", "CEB", "MNV"][int(rng.integers(6))]])
        d += dt.timedelta(days=1)
    return rows


HEAD = {
    "history": ["alert_id", "alert_dttm", "pat_enc_csn_id", "department", "order_id", "medication", "alert_rule_id",
                "alert_rule_name", "severity", "interacting_order_id", "interacting_medication", "user_action",
                "override_reason", "user_type"],
    "background": ["bg_event_id", "eval_utc", "pat_enc_csn_id", "department", "order_id", "medication", "rule_id",
                   "rule_name", "severity", "interacting_order_id", "interacting_medication", "display_mode"],
    "census": ["census_date", "department", "admissions", "discharges", "midnight_census"],
    "queue": ["task_id", "session_no", "alert_ref", "poc_location", "msg_received_utc", "claimed_utc", "closed_utc",
              "close_status", "handle_min", "pharmacist_id", "client_code"],
    "pocmap": ["point_of_care", "location_name", "client_code", "review_scope", "effective_from"],
    "pump": ["Event Time", "Care Area", "Pump Serial", "Channel", "Drug Library Entry", "Limit Type",
             "Clinician Response"],
}


def build(target):
    os.makedirs(target, exist_ok=True)
    for fn in os.listdir(target):
        os.remove(os.path.join(target, fn))
    w = W.build_world()
    R = relabel(w)
    hist = history_rows(w, R)
    n = {}
    n["history"] = IO.write_csv(os.path.join(target, FILES["history"]), HEAD["history"], hist)
    n["background"] = IO.write_csv(os.path.join(target, FILES["background"]), HEAD["background"],
                                   background_rows(w, R))
    n["census"] = IO.write_csv(os.path.join(target, FILES["census"]), HEAD["census"], census_rows(w))
    q = queue_rows(hist)
    n["queue"] = IO.write_csv(os.path.join(target, FILES["queue"]), HEAD["queue"], q)
    n["pocmap"] = IO.write_csv(os.path.join(target, FILES["pocmap"]), HEAD["pocmap"], pocmap_rows())
    n["pump"] = IO.write_csv(os.path.join(target, FILES["pump"]), HEAD["pump"], pump_rows())
    plan = plan_rows()
    n["plan"] = docs.write_plan(os.path.join(target, FILES["plan"]), plan)
    n["interventions"] = docs.write_interventions(os.path.join(target, FILES["interventions"]),
                                                  intervention_rows())
    n["register"] = docs.write_register(os.path.join(target, FILES["register"]))
    docs.write_release(os.path.join(target, FILES["release"]))
    docs.write_schedule(os.path.join(target, FILES["schedule"]))
    docs.write_cr(os.path.join(target, FILES["cr"]))
    n["release"] = n["schedule"] = n["cr"] = 0
    return w, R, n
