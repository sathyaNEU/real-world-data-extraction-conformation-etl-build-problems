"""task162 records: what Lynmere's systems export, built from the truth in world.py.

The telemetry is Lynmere's hourly-mean archive for the zone's loggers (GMT, the loggers' own clock): inlet loggers
carry flow and pressure, zone loggers the average zone pressure. Two logger makes are in service: the Halcyon HL-4
reports pressure in metres head, the Vexmet DP2 in bar. Loggers are swapped when they fail; the register dates each
serial's service. Batteries die and leave gaps; the archive's re-sends repeat whole blocks of rows."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import world as W

BAR = 10.197      # metres head per bar

F_INLET = "northern_zone_inlet_loggers_2025_26.csv"
F_ZONE = "northern_zone_pressure_loggers_2025_26.csv"
F_LOGGERS = "logger_register.csv"
F_DISTRICTS = "district_register.csv"
F_CODES = "district_code_history.csv"
F_PROPS = "property_extract_2026-11-02.csv"
F_BILLS = "billing_extract_north_2025_26.csv"
F_OUTLET = "thornholme_outlet_daily_2025_26.csv"
F_EXPORT = "dma_leakage_assessment_phase3_2025_26.xlsx"
F_CONTACTS = "customer_contacts_northern_2025_26.csv"
F_MILL = "brackenby_mill_amr_hourly_2025_26.csv"

INLET_COLS = ["logger_serial", "reading_time_gmt", "flow_l_s", "pressure"]
ZONE_COLS = ["logger_serial", "reading_time_gmt", "pressure"]
LOGGER_COLS = ["logger_serial", "district_code", "point", "make", "pressure_unit", "installed", "removed"]
DISTRICT_COLS = ["district_code", "district_name", "mains_km", "boundary_valves", "inlets", "azp_point"]
CODE_COLS = ["old_code", "current_code", "effective", "reason"]
PROP_COLS = ["property_ref", "uprn", "district_code", "property_class", "supply_point_ref", "charging_basis",
             "connected", "disconnected"]
BILL_COLS = ["supply_point_ref", "bill_from", "bill_to", "volume_m3", "basis", "read_type"]
OUTLET_COLS = ["date", "outlet_volume_ml", "meter_serial"]
CONTACT_COLS = ["contact_ref", "received", "district_code", "category", "outcome"]
MILL_COLS = ["reading_time_gmt", "flow_l_s"]

MAKES = {"HL4": ("Halcyon HL-4", "m"), "DP2": ("Vexmet DP2", "bar")}


def stamp(t):
    return t.strftime("%Y-%m-%d %H:%M")


# ------------------------------------------------------------------------------------------------- the logger fleet
def fleet(T):
    """Every logger serial with its district, point, make and service dates. Swaps: NZ20's inlet logger (Phase 3) on
    14 April 2025 and NZ03's zone logger on 9 December 2025 (to the bar make). The bar make also runs at NZ02's and
    NZ08's inlets and at NZ06's and NZ11's average zone points; every Phase 3 logger reads metres head."""
    r = K.rng("fleet")
    out = []
    used = set()

    def serial(make):
        while True:
            s = "%s-%s" % (make, "".join(str(x) for x in r.integers(0, 10, 6)))
            if s not in used:
                used.add(s)
                return s

    bar_inlet = {"NZ02", "NZ08"}
    bar_zone = {"NZ06", "NZ11"}
    for p in T["P"]:
        c = p["code"]
        mk = "DP2" if c in bar_inlet else "HL4"
        inst = dt.date(2019, 1, 1) + dt.timedelta(int(r.integers(0, 1800)))
        if c == "NZ20":
            s1, s2 = serial("HL4"), serial("HL4")
            out.append(dict(serial=s1, code=c, point="inlet", make="HL4", installed=inst, removed=dt.date(2025, 4, 14),
                            swap_at=dt.datetime(2025, 4, 14, 10)))
            out.append(dict(serial=s2, code=c, point="inlet", make="HL4", installed=dt.date(2025, 4, 14), removed=None,
                            swap_from=dt.datetime(2025, 4, 14, 12)))
        else:
            out.append(dict(serial=serial(mk), code=c, point="inlet", make=mk, installed=inst, removed=None))
        if c == "NZ04":
            out.append(dict(serial=serial("HL4"), code="NZ04A", point="inlet", make="HL4",
                            installed=dt.date(2018, 6, 14), removed=None))
        mz = "DP2" if c in bar_zone else "HL4"
        instz = dt.date(2019, 1, 1) + dt.timedelta(int(r.integers(0, 1800)))
        if c == "NZ03":
            s1, s2 = serial("HL4"), serial("DP2")
            out.append(dict(serial=s1, code=c, point="AZP", make="HL4", installed=instz, removed=dt.date(2025, 12, 9),
                            swap_at=dt.datetime(2025, 12, 9, 9)))
            out.append(dict(serial=s2, code=c, point="AZP", make="DP2", installed=dt.date(2025, 12, 9), removed=None,
                            swap_from=dt.datetime(2025, 12, 9, 11)))
        else:
            out.append(dict(serial=serial(mz), code=c, point="AZP", make=mz, installed=instz, removed=None))
    return out


GAPS = {   # battery failures: (district, point) -> list of (start GMT, hours)
    ("NZ27", "AZP"): [(dt.datetime(2026, 2, 6, 14), 61)],
    ("NZ15", "inlet"): [(dt.datetime(2025, 10, 21, 2), 30)],
    ("NZ11", "inlet"): [(dt.datetime(2025, 7, 8, 9), 93)],
    ("NZ05", "AZP"): [(dt.datetime(2025, 11, 30, 20), 40)],
}
RESENDS = [("NZ22", "inlet", dt.datetime(2025, 6, 17, 0), 48), ("NZ08", "AZP", dt.datetime(2026, 1, 28, 6), 24),
           ("NZ30", "AZP", dt.datetime(2025, 9, 9, 0), 36)]


def logger_series(T):
    """Hourly readings as each logger reports them: (inlet rows, zone rows). Values carry the logger's own noise and
    resolution: flows to 0.01 l/s, metres to 0.1, bar to 0.001."""
    idx = T["idx"]
    F = fleet(T)
    inlet_rows, zone_rows = [], []
    for f in F:
        code = "NZ04" if f["code"] == "NZ04A" else f["code"]
        D = T[code]
        rr = K.rng("logger", f["serial"])
        n = len(idx)
        if f["point"] == "inlet":
            flow = D["flow_inlet_a"] if f["code"] == "NZ04A" else D["flow_inlet"]
            flow = flow * (1.0 + 0.004 * rr.standard_normal(n))
            pres = D["inlet"] + 0.05 * rr.standard_normal(n)
        else:
            flow = None
            pres = D["azp"] + 0.05 * rr.standard_normal(n)
        unit = MAKES[f["make"]][1]
        gaps = GAPS.get((code, f["point"]), [])
        rows = []
        for h, t in enumerate(idx):
            if "swap_at" in f and t >= f["swap_at"]:
                break
            if "swap_from" in f and t < f["swap_from"]:
                continue
            if any(g0 <= t < g0 + dt.timedelta(hours=gh) for g0, gh in gaps):
                continue
            pv = pres[h] / BAR if unit == "bar" else pres[h]
            pv = round(pv, 3) if unit == "bar" else round(pv, 1)
            if f["point"] == "inlet":
                rows.append([f["serial"], stamp(t), "%.2f" % max(flow[h], 0.0), ("%.3f" % pv) if unit == "bar" else ("%.1f" % pv)])
            else:
                rows.append([f["serial"], stamp(t), ("%.3f" % pv) if unit == "bar" else ("%.1f" % pv)])
        for (dc, pt, t0, hrs) in RESENDS:
            if dc == f["code"] and pt == f["point"]:
                block = [r for r in rows if t0 <= dt.datetime.strptime(r[1], "%Y-%m-%d %H:%M") < t0 + dt.timedelta(hours=hrs)]
                at = next(i for i, r in enumerate(rows) if r[1] == stamp(t0 + dt.timedelta(hours=hrs)))
                rows = rows[:at] + block + rows[at:]
        (inlet_rows if f["point"] == "inlet" else zone_rows).extend(rows)
    return F, inlet_rows, zone_rows


def logger_register_rows(F):
    out = []
    for f in F:
        out.append([f["serial"], f["code"], "inlet" if f["point"] == "inlet" else "average zone point", MAKES[f["make"]][0],
                    "metres head" if MAKES[f["make"]][1] == "m" else "bar", f["installed"].isoformat(),
                    f["removed"].isoformat() if f["removed"] else ""])
    return sorted(out, key=lambda r: (r[1], r[2], r[5]))


def district_rows(T):
    r = K.rng("district_register")
    out = []
    for p in T["P"]:
        c = p["code"]
        bv = {"NZ09": "BV-0910", "NZ10": "BV-0910; BV-1011", "NZ11": "BV-1011"}.get(c, "BV-%s%02d" % (c[2:], int(r.integers(1, 40))))
        out.append([c, p["name"], "%.1f" % (p["households"] / 95.0 + r.uniform(1, 6)), bv, 2 if c == "NZ04" else 1,
                    "AZP-%s-%02d" % (c, int(r.integers(1, 30)))])
    return out


CODE_HISTORY = [
    ["NZ04A", "NZ04", "2024-03-11", "Wrenfold Lane boundary valve left open after the 2024 rezoning; the old upper "
                                    "district's inlet meter stays in service"],
    ["NZ19B", "NZ19", "2021-08-02", "Tolleby merged on the trunk main diversion"],
    ["NZ27X", "NZ27", "2022-11-21", "temporary code during the Holmwick mains renewal"],
    ["NZ31A", "NZ31", "2020-05-04", "Dimmock Edge upper and lower combined"],
]


# ------------------------------------------------------------------------------------------------- properties and bills
def properties(T):
    """Every property in the zone, existing ones and the year's new connections, with its district code as the
    property system holds it (NZ04's upper streets still under NZ04A), class, supply point and charging basis. The
    older streets nearer Thornholme have flats on shared supplies (two to six dwellings on one supply point, each on
    the assessed charge); a new build is connected under the developer's plot record and gets its address record, on
    the same supply point, when it is addressed weeks or months later (the plot record is closed then about one time
    in seven). The Western zone, on another reservoir, shares the North region's property system."""
    r = K.rng("properties")
    out = []
    k = 0

    def ref():
        return "P%07d" % (3100000 + k)

    def uprn():
        return "%012d" % (10090000000 + 7919 * k % 89000000)

    def homes(code_of, n, shared, metered_share):
        nonlocal k
        i = 0
        while i < n:
            size = min(int(r.choice((2, 2, 3, 3, 4, 5, 6))), n - i) if (shared and r.random() < 0.035) else 1
            k += 1
            sp = "SP%08d" % (40000000 + k)
            for j in range(size):
                if j:
                    k += 1
                if size > 1:
                    basis = "unmeasured"
                else:
                    basis = "metered" if r.random() < metered_share else "unmeasured"
                out.append(dict(ref=ref(), uprn=uprn(), code=code_of(i), cls="household", sp=sp, basis=basis,
                                connected="", disconnected="", flat=size > 1))
                i += 1

    for p in T["P"]:
        c = p["code"]
        D = T[c]
        upper = int(round(0.37 * p["households"])) if c == "NZ04" else 0
        first = len(out)
        homes(lambda i: "NZ04A" if i < upper else c, p["households"], p["phase"] == 4, 0.61)
        single = [x for x in out[first:] if not x["flat"] and x["basis"] == "metered"]
        for x, d in zip(r.choice(single, size=len(D["demol_days"]), replace=False), D["demol_days"]):
            x["disconnected"] = (W.START.date() + dt.timedelta(d)).isoformat()          # demolished or merged
        for d in D["infill_days"]:
            k += 1
            out.append(dict(ref=ref(), uprn=uprn(), code=c, cls="household", sp="SP%08d" % (40000000 + k),
                            basis="metered", connected=(W.START.date() + dt.timedelta(d)).isoformat(), disconnected="",
                            flat=False))
        plots = r.choice(np.arange(1, 900), size=len(D["conn_days"]), replace=False) if D["conn_days"] else []
        for d, num in zip(D["conn_days"], plots):
            k += 1
            day = W.START.date() + dt.timedelta(d)
            sp = "SP%08d" % (40000000 + k)
            addr_day = day + dt.timedelta(int(r.integers(45, 151)))
            closed = r.random() < 0.15
            out.append(dict(ref="PL-%s-%04d" % (c, num), uprn="", code=c, cls="household", sp=sp, basis="metered",
                            connected=day.isoformat(), disconnected=addr_day.isoformat() if closed else "", flat=False,
                            handover=addr_day))
            out.append(dict(ref=ref(), uprn=uprn(), code=c, cls="household", sp=sp, basis="metered",
                            connected=addr_day.isoformat(), disconnected="", flat=False))
        for i in range(p["nonhh"]):
            k += 1
            out.append(dict(ref=ref(), uprn=uprn(), code=("NZ04A" if (c == "NZ04" and i < 9) else c),
                            cls="non-household", sp="SP%08d" % (40000000 + k), basis="metered", connected="",
                            disconnected="", flat=False))
    k += 1
    out.append(dict(ref=ref(), uprn="%012d" % 10094417730, code="NZ-TM", cls="non-household", sp="SP90000001",
                    basis="metered", connected="", disconnected="", flat=False))      # the mill, on its own off-take
    for j in range(1, 9):
        c = "WZ%02d" % j
        homes(lambda i: c, int(r.integers(500, 1100)), True, 0.58)
        for i in range(int(r.integers(10, 40))):
            k += 1
            out.append(dict(ref=ref(), uprn=uprn(), code=c, cls="non-household", sp="SP%08d" % (40000000 + k),
                            basis="metered", connected="", disconnected="", flat=False))
    # the systems' own identifiers: property references, UPRNs and supply point references issued over decades, so
    # none runs in district order or at a fixed step (the working numbers above only keep the records apart)
    q = K.rng("identifiers")

    def issue(n, lo, hi, taken=()):
        got, seen = [], set(taken)
        while len(got) < n:
            v = int(q.integers(lo, hi))
            if v not in seen:
                seen.add(v)
                got.append(v)
        return got

    mill = out[[x["sp"] for x in out].index("SP90000001")]
    refs = iter(issue(sum(1 for x in out if x["ref"].startswith("P") and not x["ref"].startswith("PL-")),
                      1000000, 9999999))
    uprns = iter(issue(sum(1 for x in out if x["uprn"] and x is not mill), 10090000000, 10099999999, {10094417730}))
    sps = sorted({x["sp"] for x in out} - {"SP90000001"})
    spmap = dict(zip(sps, ("SP%08d" % v for v in issue(len(sps), 30000000, 79999999))))
    for x in out:
        if x["ref"].startswith("P") and not x["ref"].startswith("PL-"):
            x["ref"] = "P%07d" % next(refs)
        if x["uprn"] and x is not mill:
            x["uprn"] = "%012d" % next(uprns)
        if x["sp"] != "SP90000001":
            x["sp"] = spmap[x["sp"]]
    out.sort(key=lambda x: (x["code"], x["ref"]))
    return out


def property_rows(props):
    return [[x["ref"], x["uprn"], x["code"], x["cls"], x["sp"], x["basis"], x["connected"], x["disconnected"]] for x in props]


ASSESSED_BANDS = (62, 89, 118, 146)            # Lynmere's assessed household volumes, m3 a year, by property band
FLAT_BAND = 71                                 # the assessed volume for a flat
BILLED_TO = dt.date(2026, 10, 30)              # the last read the extract of 2 November 2026 can carry


def bills(T, props):
    """Bills for the year and its edges: metered households read half-yearly on their own read cycle, unmeasured
    households billed on an assessed volume a year (April to March), non-households monthly, the mill monthly from its
    AMR. Volumes are the consumption the bill covers as the customer's meter registers it (metered), the assessed
    volume (unmeasured), or the mill's AMR."""
    r = K.rng("bills")
    out = []
    pc = {p["code"]: p for p in T["P"]}
    pc["NZ04A"] = pc["NZ04"]
    for j in range(1, 9):
        pc["WZ%02d" % j] = dict(percap=310.0 + 6 * j, nhh_night=7.0)
    y0, y1 = dt.date(2024, 10, 1), dt.date(2026, 9, 30)
    cum = np.cumsum((0.18, 0.32 - W.BAND_SHIFT, 0.32 + W.BAND_SHIFT, 0.18))
    for x in props:
        if x["sp"] == "SP90000001":
            continue
        p = pc[x["code"]]
        if x["cls"] == "household":
            daily = p["percap"] * (0.75 + 0.5 * r.random()) / 1000.0 * W.METER_REG     # m3 a day as registered
            if x["basis"] == "unmeasured":
                if x["flat"] or r.random() < 0.10:
                    band = FLAT_BAND
                else:
                    band = ASSESSED_BANDS[int(np.searchsorted(cum, r.random()))]
                out.append([x["sp"], "2025-04-01", "2026-03-31", "%d" % band, "assessed", ""])
                continue
            if "handover" in x:                         # the developer's plot account, closed at the handover read
                a = dt.date.fromisoformat(x["connected"])
                out.append([x["sp"], a.isoformat(), (x["handover"] - dt.timedelta(1)).isoformat(),
                            "%.0f" % (daily * (x["handover"] - a).days * (0.9 + 0.2 * r.random())), "metered", "actual"])
                continue
            start = dt.date.fromisoformat(x["connected"]) if x["connected"] else y0 + dt.timedelta(int(r.integers(0, 182)))
            stop = dt.date.fromisoformat(x["disconnected"]) if x["disconnected"] else None   # the final read
            prev = start
            nxt = prev + dt.timedelta(int(r.integers(170, 196)))
            while prev < (stop or y1):
                end = nxt if stop is None or nxt < stop else stop
                vol = daily * (end - prev).days * (0.9 + 0.2 * r.random())
                est = r.random() < 0.08 and end != stop
                if end <= BILLED_TO:                    # a read after the extract was taken is not billed yet
                    out.append([x["sp"], prev.isoformat(), (end - dt.timedelta(1)).isoformat(), "%.0f" % vol,
                                "metered", "estimated" if est else "actual"])
                if end == stop:
                    break
                prev = nxt
                nxt = prev + dt.timedelta(int(r.integers(170, 196)))
        else:
            daily = (p["nhh_night"] * 24 / 1000.0 + 0.010 * 3600 * 12 * 5 / 7 / 1000.0) * (0.6 + 0.8 * r.random()) \
                * W.METER_REG
            m = dt.date(2025, 4, 1)
            while m <= dt.date(2026, 3, 1):
                nm = dt.date(m.year + (m.month // 12), m.month % 12 + 1, 1)
                out.append([x["sp"], m.isoformat(), (nm - dt.timedelta(1)).isoformat(),
                            "%.0f" % (daily * (nm - m).days * (0.9 + 0.2 * r.random())), "metered", "actual"])
                m = nm
    # the mill from its AMR
    mill = T["mill_lps"]
    for mi, m in enumerate(K.MONTHS):
        nm = K.MONTHS[mi + 1] if mi < 11 else K.YEAR_END
        sel = np.array([m <= t < nm for t in T["idx"]])
        vol = float(mill[sel].sum() * 3.6)
        out.append(["SP90000001", m.date().isoformat(), (nm.date() - dt.timedelta(1)).isoformat(), "%.0f" % vol,
                    "metered", "actual"])
    return out


def outlet_daily(T, bill_rows):
    """The Thornholme outlet meter's daily volumes in Ml (local days), as recorded: 1.4 per cent low until its
    recalibration on 12 November 2025. True input = every district's inflow plus the mill plus the trunk main's own
    losses (about 0.31 Ml/d)."""
    total = T["mill_lps"].copy()
    for p in T["P"]:
        D = T[p["code"]]
        total = total + D["flow"]
    days = {}
    for h, t in enumerate(T["idx"]):
        d = K.local(t).date()
        days[d] = days.get(d, 0.0) + total[h] * 3.6 / 1000.0
    out = []
    r = K.rng("outlet")
    for d in sorted(days):
        if not (dt.date(2025, 4, 1) <= d <= dt.date(2026, 3, 31)):
            continue
        true = days[d] + W.TRUNK_LOSS
        rec = true * (1.0 + K.CERT_ERROR) if d < K.CERT_DATE else true
        rec *= (1.0 + 0.002 * r.standard_normal())
        out.append([d.isoformat(), "%.3f" % rec, "TH-OUT-0417"])
    return out


def mill_rows(T):
    r = K.rng("mill_amr")
    return [[stamp(t), "%.1f" % (T["mill_lps"][h] * (1.0 + 0.01 * r.standard_normal()))] for h, t in enumerate(T["idx"])]


def contact_rows(T):
    r = K.rng("contacts")
    cats = ["low pressure", "no water", "discoloured water", "leak in the street", "billing query", "noisy pipes"]
    out = []
    k = 0
    for p in T["P"]:
        n = int(r.poisson(6 + p["households"] / 220))
        for _ in range(n):
            k += 1
            d = W.START + dt.timedelta(hours=int(r.integers(0, W.HOURS)))
            cat = cats[int(r.choice(len(cats), p=[0.18, 0.08, 0.14, 0.32, 0.18, 0.10]))]
            out.append(["CC-%06d" % (520000 + k), stamp(d), p["code"], cat,
                        ["advice given", "job raised", "no fault found", "referred"][int(r.integers(0, 4))]])
    return sorted(out, key=lambda x: x[1])
