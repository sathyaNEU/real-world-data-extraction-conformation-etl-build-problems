"""task468 architecture 6: Glenbrae Water's trade waste world and its pack.

The truth: each customer's effluent carries organic carbon and chloride; the dichromate COD the agreements limit reads
both (COD = A0 + B_TOC x TOC + C_CL x chloride, with a few per cent of method noise), while TOC reads the carbon only.
From 2 February 2026 the laboratory reports TOC in place of COD. Three brine customers carry chloride: Coolabah Olives
steadily, Mt Edwin Cheese until its brine recovery started in May 2026, Tallowood Tannery at a low level until a new
salted-hide supplier from mid-March 2026."""
import datetime as dt
import json
import os
from email.message import EmailMessage
from email.utils import format_datetime

import numpy as np

import wio

SEED = 46806
TZ = dt.timedelta(hours=10)          # Australia/Brisbane, no daylight saving
SWITCH = dt.date(2026, 2, 2)         # samples collected on or after this local date are tested for TOC
PAR0, PAR1 = dt.date(2025, 10, 6), dt.date(2025, 12, 19)
A0, B_TOC, C_CL, NOISE = 14.0, 2.78, 0.232, 0.032
UTILITY = "Glenbrae Water"
SS_RL = 5.0

# key, name, industry, old site code, new point, toc mean, toc cv, kL a day, ss mean, chloride regime, target ratio, unit
CUSTOMERS = [
    ("COOL", "Coolabah Olives Pty Ltd", "olive and pickle packing", "TW-031", "DP0317", 905, 0.22, 138, 380,
     [(None, 11600)], 1.12, "t"),
    ("TALL", "Tallowood Tannery Pty Ltd", "hide tannery", "TW-012", "DP0128", 1480, 0.20, 176, 1150,
     [(None, 3150), (dt.date(2026, 3, 16), 10400)], 1.10, "t"),
    ("MTED", "Mt Edwin Cheese Company", "cheese and whey", "TW-027", "DP0274", 1210, 0.21, 205, 520,
     [(None, 9150), (dt.date(2026, 5, 11), 2350)], 0.88, "t"),
    ("GMEA", "Glenbrae Meats Pty Ltd", "beef and lamb abattoir", "TW-004", "DP0041", 1320, 0.19, 410, 1450,
     [(None, 420)], 1.16, "t"),
    ("RIVP", "Riverbend Poultry", "poultry processing", "TW-019", "DP0195", 980, 0.20, 360, 820,
     [(None, 360)], 1.09, "t"),
    ("SUND", "Sunvale Dairy Ingredients", "milk powder and butter", "TW-022", "DP0226", 690, 0.23, 520, 260,
     [(None, 300)], 0.93, "t"),
    ("HART", "Hartley Street Brewing Co", "brewery", "TW-036", "DP0362", 1650, 0.25, 96, 610,
     [(None, 190)], 0.71, "kg"),
    ("BELL", "Bellbird Beverages", "soft drink bottling", "TW-008", "DP0083", 740, 0.24, 240, 120,
     [(None, 160)], 0.58, "t"),
    ("KING", "Kingfisher Linen Services", "commercial laundry", "TW-015", "DP0159", 210, 0.18, 330, 140,
     [(None, 410)], 0.66, "kg"),
    ("GOLD", "Golden Crumb Bakeries", "bakery", "TW-024", "DP0242", 520, 0.26, 85, 310,
     [(None, 230)], 0.49, "kg"),
    ("PADD", "Paddock Fresh Vegetables", "vegetable washing and cutting", "TW-010", "DP0106", 380, 0.24, 290, 640,
     [(None, 210)], 0.77, "t"),
    ("WATT", "Wattle Pet Foods", "pet food manufacture", "TW-029", "DP0295", 1120, 0.21, 150, 900,
     [(None, 470)], 0.82, "t"),
]
KEYS = [c[0] for c in CUSTOMERS]
C = {c[0]: dict(zip(["key", "name", "industry", "old", "point", "toc", "cv", "kl", "ss", "cl", "target", "unit"], c))
     for c in CUSTOMERS}
# meter exchanges: customer, local date and hour the old meter came off, hours the logger was off, new meter's opening read
SWAPS = [("GMEA", dt.datetime(2026, 4, 22, 9), 5, 3.2), ("SUND", dt.datetime(2026, 8, 12, 13), 4, 0.0),
         ("PADD", dt.datetime(2026, 11, 3, 8), 6, 1.7)]

FILES = {
    "lims_old": "glw_lims_trade_waste_results_2025-01_to_2026-02.csv",
    "lims_new": "glw_labware_trade_waste_results_2026.csv",
    "telemetry": "glw_trade_waste_flow_telemetry_2026.csv",
    "register": "glw_trade_waste_agreements_register_2026.xlsx",
    "policy": "glw_trade_waste_policy_v4.pdf",
    "lab_notice": "glw_laboratory_notice_toc_2026.pdf",
    "crosswalk": "glw_sampling_point_crosswalk.csv",
    "jobs": "glw_field_service_jobs_2026.xlsx",
    "request": "cod_review_request.eml",
    "rain": "glenbrae_daily_rainfall_2026.csv",
    "returns": "glw_customer_production_returns_2026.xlsx",
    "inspections": "glw_trade_waste_inspections_2026.csv",
    "receival": "glw_liquid_waste_receival_2026.csv",
    "manifests": "qld_waste_tracking_manifests_glw_2026.xlsx",
}
DISTRACTORS = ["rain", "returns"]


def local_dates(y0, y1):
    d = dt.date(y0, 1, 1)
    while d <= dt.date(y1, 12, 31):
        yield d
        d += dt.timedelta(days=1)


def chloride_level(c, day):
    lvl = None
    for start, v in C[c]["cl"]:
        if start is None or day >= start:
            lvl = v
    return lvl


def world(seed=SEED):
    rng = np.random.RandomState(seed)
    W = {"flow": {}, "samples": [], "swaps": SWAPS}
    # daily and hourly flows (local), 2025-12-30 to 2027-01-02 so the UTC export spans both year ends
    days = [dt.date(2025, 12, 30) + dt.timedelta(days=i) for i in range(369)]
    hours_share = {}
    for k in KEYS:
        c = C[k]
        wk = np.array([1.0, 1.04, 1.02, 1.03, 1.0, 0.62, 0.38])
        season = 1 + 0.08 * np.sin(2 * np.pi * (np.arange(len(days)) - 40) / 365.0)
        noise = np.exp(rng.normal(0, 0.09, len(days)))
        daily = {d: c["kl"] * wk[d.weekday()] * season[i] * noise[i] for i, d in enumerate(days)}
        prof = np.array([0.4, 0.3, 0.3, 0.3, 0.4, 0.8, 1.3, 1.6, 1.7, 1.6, 1.5, 1.5,
                         1.4, 1.5, 1.6, 1.6, 1.5, 1.3, 1.1, 0.9, 0.7, 0.6, 0.5, 0.4])
        hours_share[k] = prof / prof.sum()
        W["flow"][k] = daily
    W["hours_share"] = hours_share
    # sampling: weekly 24-hour composites on a working day, plus the 2025 parallel run (two a week, Oct to Dec)
    sid_old, sid_new = 251004, 260006
    for k in KEYS:
        c = C[k]
        for d in local_dates(2025, 2026):
            par = PAR0 <= d <= PAR1
            weekly = d.weekday() == (KEYS.index(k) % 4) + 0 and rng.rand() < 0.93
            twice = par and d.weekday() in ((KEYS.index(k) % 4), (KEYS.index(k) % 4) + 1)
            if not (weekly or twice):
                continue
            toc = c["toc"] * np.exp(rng.normal(-0.5 * c["cv"] ** 2, c["cv"]))
            cl = chloride_level(k, d) * np.exp(rng.normal(-0.007, 0.12))
            cod = (A0 + B_TOC * toc + C_CL * cl) * np.exp(rng.normal(0, NOISE))
            ss = c["ss"] * np.exp(rng.normal(-0.08, 0.4))
            ph = round(float(np.clip(rng.normal(6.9 if k not in ("GMEA", "RIVP") else 7.4, 0.5), 4.8, 10.2)), 1)
            hh = int(rng.randint(7, 11))
            mm = int(rng.choice([0, 5, 10, 15, 20, 30, 35, 40, 45, 50]))
            new = d >= SWITCH
            if new:
                sid_new += int(rng.randint(3, 19))
                sid = "GW26-%06d" % sid_new
            else:
                sid_old += int(rng.randint(2, 15))
                sid = "%d" % sid_old
            W["samples"].append({"key": k, "day": d, "time": dt.time(hh, mm), "sid": sid, "toc": toc, "cl": cl,
                                 "cod": cod, "ss": ss, "ph": ph, "parallel": par, "new": new,
                                 "rerun": False, "dup": False})
    # quality control: duplicates (one in about twelve new samples) and re-runs (a TOC or SS result re-tested)
    for s in W["samples"]:
        if s["new"]:
            s["dup"] = rng.rand() < 0.085
            s["rerun_toc"] = rng.rand() < 0.035
            s["rerun_ss"] = rng.rand() < 0.03
            s["first_toc"] = s["toc"] * (1 + rng.choice([-1, 1]) * rng.uniform(0.18, 0.4))
            s["first_ss"] = s["ss"] * (1 + rng.choice([-1, 1]) * rng.uniform(0.25, 0.5))
            s["dup_toc"] = s["toc"] * np.exp(rng.normal(0, 0.03))
            s["dup_ss"] = s["ss"] * np.exp(rng.normal(0, 0.08))
            s["dup_cl"] = s["cl"] * np.exp(rng.normal(0, 0.02))
    # trade waste officers' inspection visits; at most of them a grab sample is taken for suspended solids and pH
    W["inspections"] = []
    for k in KEYS:
        c = C[k]
        days = sorted(set(dt.date(2026, 2, 3) + dt.timedelta(days=int(x)) for x in rng.randint(0, 330, 11)))
        for d in days:
            if d.weekday() >= 5:
                continue
            when = dt.datetime.combine(d, dt.time(int(rng.randint(10, 15)), int(rng.choice([0, 10, 20, 30, 40, 50]))))
            grab = rng.rand() < 0.8
            W["inspections"].append({"key": k, "when": when, "grab": grab})
            if grab:
                W["samples"].append({"key": k, "day": d, "time": when.time(), "sid": "", "grab": True, "new": True,
                                     "ss": c["ss"] * 1.7 * np.exp(rng.normal(0, 0.35)), "parallel": False,
                                     "ph": round(float(np.clip(rng.normal(6.6, 0.8), 4.0, 11.0)), 1),
                                     "dup": False, "rerun_toc": False, "rerun_ss": False})
    # LabWare numbers every sample it registers in one series, composites and grabs alike
    sid_new = 260006
    for s in sorted((s for s in W["samples"] if s["new"]), key=lambda s: (s["day"], s["time"], s["key"])):
        sid_new += int(rng.randint(3, 19))
        s["sid"] = "GW26-%06d" % sid_new
    return W


# ------------------------------------------------------------------------------------------------ the truth

def day_volume(W, k, d):
    return W["flow"][k][d]


def true_masses(W):
    out = {}
    for k in KEYS:
        vol = sum(W["flow"][k][d] for d in local_dates(2026, 2026))
        ss = [s for s in W["samples"] if s["key"] == k and s["day"].year == 2026 and not s.get("grab")]
        v = np.array([day_volume(W, k, s["day"]) for s in ss])
        cod = np.array([s["cod"] for s in ss])
        out[k] = {"vol": vol, "cod_t": vol * float((cod * v).sum() / v.sum()) / 1e6}
    return out


# ------------------------------------------------------------------------------------------------ the pack

def fmt_val(x, d=0):
    return ("%." + str(d) + "f") % x


def write_lims_old(W, path):
    rows = []
    for s in sorted(W["samples"], key=lambda s: (s["day"], s["time"], s["sid"])):
        if s["new"]:
            continue
        stamp = "%s %s" % (s["day"].strftime("%d/%m/%Y"), s["time"].strftime("%H:%M"))
        site = C[s["key"]]["old"]
        tests = [("COD", fmt_val(s["cod"]), "mg/L", ""), ("CL", fmt_val(s["cl"]), "mg/L", "")]
        if s["parallel"]:
            tests.append(("TOC", fmt_val(s["toc"]), "mg/L", ""))
        ssv = s["ss"]
        tests.append(("SS", "5" if ssv < SS_RL else fmt_val(ssv), "mg/L", "<" if ssv < SS_RL else ""))
        tests.append(("PH", "%.1f" % s["ph"], "pH units", ""))
        for t, v, u, q in tests:
            rows.append([s["sid"], site, stamp, t, v, u, q, "Authorised"])
    wio.csv_file(path, ["Sample No", "Site Code", "Sampled", "Test", "Result", "Units", "Qualifier", "Status"], rows)


AN = {"toc": "TOC (NPOC)", "cl": "Chloride", "ss": "Suspended Solids", "ph": "pH"}


def write_lims_new(W, path):
    rows = []
    for s in sorted(W["samples"], key=lambda s: (s["day"], s["time"], s["sid"])):
        if not s["new"]:
            continue
        loc = dt.datetime.combine(s["day"], s["time"])
        utc = (loc - TZ).strftime("%Y-%m-%dT%H:%M:%SZ")
        auth = (loc + dt.timedelta(days=3, hours=4)) - TZ
        pid = C[s["key"]]["point"]

        def add(sid, an, val, unit="mg/L", flag="", when=auth):
            rows.append([sid, pid, utc, AN[an], val, unit, flag, when.strftime("%Y-%m-%dT%H:%M:%SZ")])
        if s.get("grab"):
            add(s["sid"], "ss", "5" if s["ss"] < SS_RL else fmt_val(s["ss"]), flag="<" if s["ss"] < SS_RL else "")
            add(s["sid"], "ph", "%.1f" % s["ph"], unit="pH")
            continue
        toc0 = s["first_toc"] if s["rerun_toc"] else s["toc"]
        add(s["sid"], "toc", fmt_val(toc0, 1))
        add(s["sid"], "cl", fmt_val(s["cl"]))
        ss0 = s["first_ss"] if s["rerun_ss"] else s["ss"]
        add(s["sid"], "ss", "5" if ss0 < SS_RL else fmt_val(ss0), flag="<" if ss0 < SS_RL else "")
        add(s["sid"], "ph", "%.1f" % s["ph"], unit="pH")
        if s["rerun_toc"]:
            add(s["sid"] + "-R", "toc", fmt_val(s["toc"], 1), when=auth + dt.timedelta(days=2, hours=3))
        if s["rerun_ss"]:
            add(s["sid"] + "-R", "ss", "5" if s["ss"] < SS_RL else fmt_val(s["ss"]),
                flag="<" if s["ss"] < SS_RL else "", when=auth + dt.timedelta(days=1, hours=6))
        if s["dup"]:
            add(s["sid"] + "-D", "toc", fmt_val(s["dup_toc"], 1))
            add(s["sid"] + "-D", "cl", fmt_val(s["dup_cl"]))
            add(s["sid"] + "-D", "ss", "5" if s["dup_ss"] < SS_RL else fmt_val(s["dup_ss"]),
                flag="<" if s["dup_ss"] < SS_RL else "")
    wio.csv_file(path, ["sample_id", "point_id", "collected_utc", "analyte", "value", "unit", "result_qualifier", "authorised_utc"],
                 rows)


METER0 = {k: "GW-%s-%05d" % (["ABB", "KRH", "SEN"][i % 3], 41210 + i * 377) for i, k in enumerate(KEYS)}
METER1 = {k: "GW-SEN-%05d" % (50311 + i * 211) for i, k in enumerate(KEYS)}


def telemetry(W):
    """Hourly cumulative register reads in kL by meter, UTC, from 2025-12-31T00:00Z to 2027-01-01T00:00Z."""
    out = {}
    start = dt.datetime(2025, 12, 31, 0)
    end = dt.datetime(2027, 1, 1, 0)
    for i, k in enumerate(KEYS):
        reg = 10000.0 + 9137.0 * i + 413.0 * (i % 5)
        swap = [s for s in SWAPS if s[0] == k]
        rows = []
        meter = METER0[k]
        t = start
        gap_until = None
        swap_info = None
        while t <= end:
            loc = t + TZ
            d = loc.date()
            inc = W["flow"][k][d] * W["hours_share"][k][loc.hour]
            if swap and loc == swap[0][1]:
                # the logger is unplugged at the swap hour; the new meter starts at its opening read
                swap_info = {"key": k, "old": meter, "off_local": loc, "final": round(reg, 1)}
                gap_until = loc + dt.timedelta(hours=swap[0][2])
                meter = METER1[k]
                reg = swap[0][3]
            if gap_until is not None and loc < gap_until:
                reg += inc
                t += dt.timedelta(hours=1)
                continue
            if gap_until is not None and loc >= gap_until and swap_info and "new_open" not in swap_info:
                swap_info["new_open"] = swap[0][3]
                swap_info["new"] = meter
                swap_info["on_local"] = gap_until
                W.setdefault("swap_info", []).append(swap_info)
            rows.append((t, meter, round(reg, 1)))
            reg += inc
            t += dt.timedelta(hours=1)
        out[k] = rows
    return out


def write_telemetry(W, tel, path):
    rows = []
    for k in KEYS:
        for t, meter, reg in tel[k]:
            rows.append([t.strftime("%Y-%m-%dT%H:%M:%SZ"), meter, "%.1f" % reg, "kL"])
    rows.sort(key=lambda r: (r[0], r[1]))
    wio.csv_file(path, ["reading_utc", "meter_serial", "register", "unit"], rows)
