"""The pack's data: the receiver network's export, the FAA register extract (MASTER, DEREG, ACFTREF, ENGINE), the six
towers' daily counts, the four count studies' records, the state's based aircraft validation and airport directory,
the airports' 5010 records and the district's lead monitoring samples. Rows only; docs.py writes the documents and
workbooks."""
import csv
import datetime as dt

import numpy as np

import activity as A
import catalog as CT
import fleet as FL
import world as W

EXPORT_FROM = dt.datetime(2025, 12, 30, 0, 0)          # local, Pacific time
EXPORT_TO = dt.datetime(2027, 1, 3, 0, 0)
EVENT_WORD = {"departure": "takeoff", "arrival": "landing", "touch_and_go": "touch_and_go"}
RUNWAYS = {"HWK": ("13", "31"), "CRV": ("16", "34"), "OSY": ("09", "27"), "VNL": ("15", "33"), "KTY": ("02", "20"),
           "DMR": ("12", "30"), "F37": ("07", "25"), "L08": ("17", "35"), "G42": ("14", "32"), "D19": ("01", "19"),
           "T61": ("10", "28"), "P05": ("13", "31"), "S27": ("06", "24"), "U44": ("16", "34"), "O16": ("04", "22"),
           "W33": ("11", "29"), "Y02": ("18", "36"), "A71": ("15", "33"), "N26": ("08", "26"), "T13": ("12", "30"),
           "K58": ("03", "21"), "Z14": ("09", "27"), "H52": ("17", "35"), "M09": ("05", "23"), "C66": ("14", "32"),
           "B48": ("02", "20"), "D73": ("16", "34"), "R31": ("07", "25"), "W85": ("13", "31"), "L29": ("10", "28")}


def everything():
    x = A.world()
    if "rows" not in x:
        x["rows"] = derive(x)
    return x


def hex_at(a, d):
    if "n_before" in a and d < a["changed_on"]:
        return a["hex_before"]
    return a["hex"]


def n_at(a, d):
    if "n_before" in a and d < a["changed_on"]:
        return a["n_before"]
    return a["n"]


def derive(x):
    """Per-operation records with everything the writers need, in local time order."""
    ac = x["aircraft"]
    ops = sorted(x["ops"], key=lambda o: (o[2], o[1], o[0]))
    rng = np.random.default_rng(4741)
    blank_id = {a["id"] for a in ac if rng.random() < 0.05}
    rows = []
    for aid, lid, t, kind, itin in ops:
        a = ac[aid]
        rows.append(dict(a=a, lid=lid, t=t, kind=kind, itin=itin or a["role"] == "survey",
                         blank=aid in blank_id and not a.get("mover")))
    return rows


# ---------------------------------------------------------------------------------------------- network export
EVENT_COLS = ["event_id", "site", "event_time_utc", "event", "icao24", "flight_id", "emitter_cat", "runway"]


def event_rows(x):
    rng = np.random.default_rng(4743)
    out = []
    wind = {}
    for r in x["rows"]:
        a = r["a"]
        if not a["broadcasts"] or not (EXPORT_FROM <= r["t"] < EXPORT_TO):
            continue
        d = r["t"].date()
        key = (r["lid"], d, r["t"].hour // 6)
        if key not in wind:
            wind[key] = 0 if rng.random() < 0.72 else 1
        if a.get("stale_flight_id") and d >= a["changed_on"]:
            fid = a["n_before"]
        elif a.get("mover") and d >= a["fid_from"]:      # the old airplane's pilot broadcasting its new number
            fid = a["n_after"]
        elif a.get("swap_on") and a["fid_from_b"] <= d < a["swap_on"] and not r["blank"]:
            fid = a["n_new_b"]
        elif a.get("callsign") and not r["blank"]:
            fid = a["callsign"]
        else:
            fid = "" if r["blank"] else n_at(a, d)
        u = W.to_utc(r["t"]) + dt.timedelta(seconds=int(rng.integers(0, 60)))
        out.append([None, r["lid"], u, EVENT_WORD[r["kind"]], hex_at(a, d).lower(), fid, FL.emitter(a["model"]),
                    RUNWAYS[r["lid"]][wind[key]]])
    out.sort(key=lambda z: (z[2], z[1], z[4]))
    # the network database's key runs across every receiver and record type it stores (taxi tracks, overflights,
    # surface movements), so the field events take a share of its numbers
    step = np.random.default_rng(4744).geometric(0.22, len(out))
    key = 48211037
    for z, s in zip(out, step):
        key += int(s)
        z[0] = key
        z[2] = z[2].strftime("%Y-%m-%dT%H:%M:%SZ")
    return out


# ---------------------------------------------------------------------------------------------- the register
MASTER_COLS = [("N-NUMBER", 5), ("SERIAL NUMBER", 30), ("MFR MDL CODE", 7), ("ENG MFR MDL", 5), ("YEAR MFR", 4),
               ("TYPE REGISTRANT", 1), ("REGION", 1), ("LAST ACTION DATE", 8), ("CERT ISSUE DATE", 8),
               ("CERTIFICATION", 10), ("TYPE AIRCRAFT", 1), ("TYPE ENGINE", 2), ("STATUS CODE", 2),
               ("MODE S CODE", 8), ("FRACT OWNER", 1), ("AIR WORTH DATE", 8), ("EXPIRATION DATE", 8),
               ("UNIQUE ID", 8), ("KIT MFR", 30), ("KIT MODEL", 20), ("MODE S CODE HEX", 10)]
DEREG_COLS = [("N-NUMBER", 5), ("SERIAL-NUMBER", 30), ("MFR-MDL-CODE", 7), ("ENG-MFR-MDL", 5), ("YEAR-MFR", 4),
              ("CERTIFICATION", 10), ("REGION", 1), ("AIR-WORTH-DATE", 8), ("CANCEL-DATE", 8), ("MODE-S-CODE", 8),
              ("EXP-COUNTRY", 2), ("LAST-ACT-DATE", 8), ("CERT-ISSUE-DATE", 8), ("KIT MFR", 30), ("KIT MODEL", 20),
              ("MODE S CODE HEX", 10)]
ACFTREF_COLS = [("CODE", 7), ("MFR", 30), ("MODEL", 20), ("TYPE-ACFT", 1), ("TYPE-ENG", 2), ("AC-CAT", 1),
                ("BUILD-CERT-IND", 1), ("NO-ENG", 2), ("NO-SEATS", 3), ("AC-WEIGHT", 7), ("SPEED", 4)]
ENGINE_COLS = [("CODE", 5), ("MFR", 10), ("MODEL", 13), ("TYPE", 2), ("HORSEPOWER", 5), ("THRUST", 6)]


def _ymd(d):
    return d.strftime("%Y%m%d") if d else ""


def _kit(a):
    k = CT.BY_CODE[a["reg_model"]]["kit"]
    return k if k else ("", "")


def master_rows(x):
    out = []
    for r in FL.REG["master"]:
        a = r["a"]
        m = CT.BY_CODE[a["reg_model"]]
        hx = FL.icao_hex(r["n"])
        kit = _kit(a)
        exp = r["issued"].replace(year=r["issued"].year + 7) if not (r["issued"].month == 2 and r["issued"].day == 29) \
            else dt.date(r["issued"].year + 7, 3, 1)
        out.append([r["n"][1:], a["reg_serial"], m["code"], a["reg_engine"], str(a["year"]), a["kind_code"], "7",
                    _ymd(r["last"]), _ymd(r["issued"]), a["cert"], str(m["ta"]), str(m["te"]), r["status"],
                    "%08o" % int(hx, 16),
                    a["fract"], _ymd(a["air_worth"]), _ymd(exp), a["uid"], kit[0], kit[1], hx])
    out.sort(key=lambda z: z[0])
    return out


def dereg_rows(x):
    out = []
    for r in FL.REG["dereg"]:
        a = r["a"]
        m = CT.BY_CODE[a["reg_model"]]
        hx = FL.icao_hex(r["n"])
        kit = _kit(a)
        last = r["cancel"]
        out.append([r["n"][1:], a["reg_serial"], m["code"], a["reg_engine"], str(a["year"]), a["cert"], "7",
                    _ymd(a["air_worth"]), _ymd(r["cancel"]), "%08o" % int(hx, 16), r["exp"], _ymd(last),
                    _ymd(r["issued"]), kit[0], kit[1], hx])
    out.sort(key=lambda z: (z[0], z[8]))
    return out


def acftref_rows(x):
    used = {r["a"]["reg_model"] for r in FL.REG["master"]} | {r["a"]["reg_model"] for r in FL.REG["dereg"]}
    out = []
    for m in CT.CATALOG:
        if m["code"] not in used:
            continue
        out.append([m["code"], m["mfr"], m["model"], str(m["ta"]), str(m["te"]), "1", str(m["bc"]), str(m["ne"]),
                    str(m["seats"]), CT.weight_class(m["wt"]), str(m["spd"])])
    out.sort(key=lambda z: z[0])
    return out


def engine_rows(x):
    used = {r["a"]["reg_engine"] for r in FL.REG["master"]} | {r["a"]["reg_engine"] for r in FL.REG["dereg"]}
    out = [[e[0], e[1], e[2], str(e[3]), str(e[4]), str(e[5])] for e in CT.ENGINES if e[0] in used]
    out.sort(key=lambda z: z[0])
    return out


def write_padded(path, cols, rows):
    """The FAA's releasable database layout: comma-separated values, each padded to its field width, a trailing
    comma on every line, CRLF line ends."""
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(",".join(c for c, w in cols) + ",\r\n")
        for row in rows:
            fh.write(",".join(str(v).ljust(w)[:max(w, len(str(v)))] for v, (c, w) in zip(row, cols)) + ",\r\n")
    return len(rows)


# ---------------------------------------------------------------------------------------------- tower counts
ATCT_COLS = ["Date", "Facility", "Itinerant Air Carrier", "Itinerant Air Taxi", "Itinerant General Aviation",
             "Itinerant Military", "Itinerant Total", "Local Civil", "Local Military", "Local Total",
             "Total Operations"]
MILITARY = {"HWK": (40, 22), "CRV": (66, 30), "OSY": (18, 12), "VNL": (8, 0), "KTY": (12, 6), "DMR": (0, 0)}


def atct_counts(x):
    """{(lid, date): [air carrier, air taxi, GA itinerant, military itinerant, local civil, military local]} in
    tower hours."""
    cnt = {}
    for lid in W.TOWERED:
        for d in A.DAYS:
            cnt[(lid, d)] = [0, 0, 0, 0, 0, 0]
    for r in x["rows"]:
        lid, t = r["lid"], r["t"]
        if lid not in W.TOWER_HOURS or t.year != 2026 or not W.tower_open(lid, t):
            continue
        a = r["a"]
        n = 2 if r["kind"] == "touch_and_go" else 1
        c = cnt[(lid, t.date())]
        if r["itin"]:
            taxi = a["role"] == "charter" or a.get("charter")
            c[1 if taxi else 2] += n
        else:
            c[4] += n
    # military helicopters and transports working the towers' patterns and approaches (not exported by the network)
    rng = np.random.default_rng(4751)
    for lid, (itin, local) in MILITARY.items():
        for kind, total in ((3, itin), (5, local)):
            days = [d for d in A.DAYS if W.tower_open(lid, dt.datetime(d.year, d.month, d.day, 12))]
            for _ in range(total // 2):
                d = days[int(rng.integers(0, len(days)))]
                cnt[(lid, d)][kind] += 2
    return cnt


def atct_rows(x):
    cnt = atct_counts(x)
    out = []
    for d in A.DAYS:
        for lid in sorted(W.TOWERED):
            c = cnt[(lid, d)]
            it = c[0] + c[1] + c[2] + c[3]
            lo = c[4] + c[5]
            out.append([d.strftime("%m/%d/%Y"), lid, c[0], c[1], c[2], c[3], it, c[4], c[5], lo, it + lo])
    return out


# ---------------------------------------------------------------------------------------------- count studies
def study_counts(x, lid):
    """{local date: {category: operations}} for a field over 2026, every hour; a touch-and-go is two operations.
    Also the L08 split of piston airplane takeoffs, landings and touch-and-go circuits."""
    out = {}
    for r in x["rows"]:
        if r["lid"] != lid or r["t"].year != 2026:
            continue
        a = r["a"]
        cat = {"single": "piston", "multi": "piston", "turbine": "turbine", "rotor": "helicopter",
               "glider": "glider"}[a["cls"]]
        d = out.setdefault(r["t"].date(), {})
        n = 2 if r["kind"] == "touch_and_go" else 1
        d[cat] = d.get(cat, 0) + n
        if cat == "piston":
            k = {"departure": "takeoffs", "arrival": "landings", "touch_and_go": "circuits"}[r["kind"]]
            d[k] = d.get(k, 0) + 1
        if cat == "glider":
            k = {"departure": "launches", "arrival": "glider_landings"}[r["kind"]]
            d[k] = d.get(k, 0) + 1
    return out


def monthly(daily):
    out = {}
    for d, v in daily.items():
        m = out.setdefault(d.month, {})
        for k, n in v.items():
            m[k] = m.get(k, 0) + n
    return out


# ---------------------------------------------------------------------------------------------- based aircraft
def based_type(a):
    m = CT.BY_CODE[a["reg_model"]]
    if m["te"] == 5:
        return "Jet"
    if m["ta"] == 6:
        return "Helicopter"
    if m["ta"] == 1:
        return "Glider"
    return "Single Engine" if m["ta"] == 4 else "Multi Engine"


def based_list(x):
    """The aircraft based at each field and strip on 1 January 2027: everything homed there, less the airplanes
    that left in 2026 (sold abroad, or gone when their number moved)."""
    out = []
    for a in x["aircraft"]:
        if a["home"] is None or a["role"] == "filler":
            continue
        if "leaves_on" in a or "exported_on" in a:
            continue
        out.append(a)
    return out


def _nfmt(n, county, rng):
    s = n[1:]
    if county == "Corrisan":
        return n
    if county == "Halwick":
        return s
    if county == "Ostrey":
        return n.lower()
    return (" " if rng.random() < 0.3 else "") + n + (" " if rng.random() < 0.4 else "")


def based_rows(x):
    """{county: [rows]}, each row [LocID, airport name, N-number as the county wrote it, make/model, type,
    validated date]."""
    rng = np.random.default_rng(4753)
    rn = np.random.default_rng(4754)
    names = {f["lid"]: (f["name"], f["county"]) for f in W.F}
    names.update({lid: (nm, c) for lid, nm, c in W.STRIPS})
    # each airport's sponsor writes make and model its own way: as the owner gave it, some in capitals
    caps = {lid: (sum(map(ord, lid)) % 5 == 0) for lid in names}
    sheets = {c: [] for c in W.COUNTIES}
    for a in based_list(x):
        nm, county = names[a["home"]]
        cands = CT.BY_CODE[a["reg_model"]]["names"]
        mm = cands[int(rn.integers(0, len(cands)))]
        rng.random()
        if caps[a["home"]]:
            mm = mm.upper()
        val = dt.date(2026, int(rng.integers(9, 13)), int(rng.integers(1, 29)))
        if a.get("cancelled_on") and val >= a["cancelled_on"]:   # validated while the registration stood
            val = a["cancelled_on"] - dt.timedelta(days=9 + int(rn.integers(0, 40)))
        sheets[county].append([a["home"], nm, _nfmt(a["n"], county, rng), mm, based_type(a), val])
    for c in sheets:
        sheets[c].sort(key=lambda z: (z[0], z[2].strip().upper().lstrip("N")))
    return sheets


# ---------------------------------------------------------------------------------------------- 5010 records
def m5010_rows(x):
    """The airports' master records as last filed: based aircraft by type and annual operations, the managers'
    estimates for the twelve months ending on the date shown."""
    rng = np.random.default_rng(4757)
    out = []
    for f in W.F:
        lid = f["lid"]
        here = [a for a in x["aircraft"] if a["home"] == lid]
        bt = {}
        for a in here:
            k = based_type(a)
            bt[k] = bt.get(k, 0) + 1
        drift = rng.uniform(0.75, 1.3)
        sgl = int(round(bt.get("Single Engine", 0) * drift))
        mlt = int(round(bt.get("Multi Engine", 0) * rng.uniform(0.7, 1.3)))
        base = (f["B"] * rng.uniform(55, 160) + 1500) * (1.5 if f["school"] else 1.0)
        gen = int(round(base / (1000 if base > 20000 else 500))) * (1000 if base > 20000 else 500)
        loc = int(round(gen * rng.uniform(0.35, 0.6) / 100)) * 100
        year = int(rng.integers(2018, 2026))
        out.append([lid, f["name"], sgl, mlt, bt.get("Jet", 0), bt.get("Helicopter", 0), bt.get("Glider", 0),
                    int(rng.integers(0, 4)), 0, int(round(gen * 0.03 / 10)) * 10 if f["turbines"] else 0, loc,
                    gen - loc, 0 if not f["towered"] else int(rng.integers(1, 6)) * 20,
                    dt.date(year, 12, 31) if rng.random() < 0.6 else dt.date(year, 6, 30),
                    dt.date(int(rng.integers(2016, 2025)), int(rng.integers(1, 13)), 1)])
    return out


# ---------------------------------------------------------------------------------------------- lead monitoring
PBMON_COLS = ["site_id", "site_name", "sample_date", "pb_tsp_ug_m3", "mdl_ug_m3", "qualifier", "method_code"]


def pbmon_rows(x):
    rng = np.random.default_rng(4759)
    out = []
    sites = [("CV-0412", "Halwick Municipal Runway 31 End", 0.032), ("CV-0418", "Corrisan Valley Regional North", 0.021)]
    d = dt.date(2026, 1, 3)
    while d.year == 2026:
        for sid, nm, mu in sites:
            season = 0.7 + 0.6 * A.MONTH_W[d.month - 1] / A.MONTH_W.max()
            v = float(rng.lognormal(np.log(mu * season), 0.55))
            q = ""
            if rng.random() < 0.03:
                out.append([sid, nm, d.isoformat(), "", "0.004", "AN", "192"])
                continue
            if v < 0.004:
                q = "MD"
            out.append([sid, nm, d.isoformat(), "%.4f" % v, "0.004", q, "192"])
        d += dt.timedelta(days=6)
    return out


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
    return len(rows)
