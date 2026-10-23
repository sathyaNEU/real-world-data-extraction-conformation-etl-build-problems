"""Reads task478's pack the way an analyst would, from the files alone, and computes the golden and every rung: each
facility's 2026 NOx from its Rule 4306 units, the gas Tamsett Valley Gas delivered to it, and its emergency engines'
NOx. golden.py, checks.py, ceiling.py and writeup.py all go through this module; verify.py does not."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

NG_HHV = 1037.0
FD = {"natural gas": 8710.0, "landfill gas": 9570.0, "digester gas": 9570.0}
TIER_NOX = {"Tier 1": 6.9, "Tier 2": 4.8, "Tier 3": 3.0, "Tier 4 Final": 0.30}
ENGINE_LF = 0.74
G_LB = 453.6
YEAR = 2026
D0, D1 = dt.date(2026, 1, 1), dt.date(2027, 1, 1)
NAMES = {"plan": "tbapcd_lowry_creek_cerp_2027.pdf", "guidance": "tbapcd_emission_inventory_guidance_2026.pdf",
         "cems": "tbapcd_cems_hourly_2026.csv", "tests_old": "tbapcd_source_tests_2018_2021.csv",
         "tests_new": "tbapcd_source_tests_2022_2026.xlsx", "statements": "tbapcd_emission_statements_2017_2026.csv",
         "permits": "tbapcd_permit_devices.csv", "events": "tbapcd_compliance_events_2017_2026.csv",
         "billing": "tvg_commercial_billing_extract_2027-02.csv", "engine_logs": "tbapcd_rule4702_engine_logs_2026.xlsx",
         "inspections": "tbapcd_engine_inspections_2025_2027.csv"}
# the plan's facility table (appendix A): name, facility number, address
FACILITIES = [("Wexley Point Energy Center", "0418", "2200 Wexley Point Road"), ("Ashgrove Refining", "0102", "1 Refinery Avenue"),
              ("Valmora Glass Works", "0577", "880 Furnace Street"), ("Sedge Hollow Landfill Gas", "1240", "15500 Sedge Hollow Road"),
              ("Haskett Ridge Compressor Station", "0912", "4917 Haskett Ridge Road"),
              ("St. Aldric Medical Center", "0761", "1300 Aldric Boulevard"), ("Lindqvist Paperboard", "0233", "60 Mill Race Lane"),
              ("Tamsett State University", "0350", "500 University Drive"), ("Briar Flats Water Reclamation", "1102", "7700 Briar Flats Road"),
              ("Merriwell Foods", "0645", "210 Cannery Row"), ("Harrow Peaking Station", "1318", "3150 Harrow Lane"),
              ("Orchard Basin Almond Growers", "0880", "4410 Orchard Way"), ("Penrose Tire Retreading", "1027", "4486 Orchard Way"),
              ("Quarry Lane Data Center", "1455", "9 Quarry Lane")]
FAC_OF_NO = {no: name for name, no, _ in FACILITIES}
FAC_OF_NO["0705"] = "Haskett Ridge Compressor Station"       # its number before the 2023 change of owner
ORDER = [n for n, _, _ in FACILITIES]


def files(folder):
    return {k: os.path.join(folder, v) for k, v in NAMES.items()}


# ------------------------------------------------------------------------------------------------ the call's inputs
def read_permits(folder):
    df = pd.read_csv(files(folder)["permits"], dtype=str)
    df["facility"] = df["FAC_NO"].map(FAC_OF_NO)
    return df


def cems_2026(folder):
    """lb of NOx each monitored device reported for 2026, through the permit list's monitoring plan ids."""
    pm = read_permits(folder)
    key = {(r.FAC_NO, r.CEMS_UNIT_ID): r.DEVICE_NO for r in pm.itertuples() if isinstance(r.CEMS_UNIT_ID, str)}
    df = pd.read_csv(files(folder)["cems"], dtype={"facility_id": str, "unit_id": str})
    df["device"] = [key[(f, u)] for f, u in zip(df["facility_id"], df["unit_id"])]
    return df.groupby("device")["nox_mass_lb"].sum().to_dict()


def read_tests(folder, conv="lbhr"):
    """Every source test in lb/MMBtu: the new database's own column; the older one from lb/hr over the test's heat
    input ('lbhr') or from ppm through the fuel's F-factor ('ppm')."""
    f = files(folder)
    pm = read_permits(folder).set_index("DEVICE_NO")
    old = pd.read_csv(f["tests_old"], dtype=str)
    rows = []
    for r in old.itertuples():
        dev = "D-" + r.DEVICE_NO
        if conv == "lbhr":
            hi = float(r.FUEL_FLOW_SCFH) * float(r.FUEL_HHV) / 1e6
            lb = float(r.NOX_LB_HR) / hi
        else:
            o2 = float(r.O2_REF)
            lb = float(r.NOX_PPMVD) * 1.194e-7 * FD[pm.loc[dev, "FUEL"]] * 20.9 / (20.9 - o2)
        rows.append((dev, dt.datetime.strptime(r.TEST_DATE, "%m/%d/%Y").date(), lb))
    new = pd.read_excel(f["tests_new"], sheet_name="Results")
    for r in new.itertuples(index=False):
        rows.append((r[2], pd.Timestamp(r[3]).date(), float(r[7])))
    return pd.DataFrame(rows, columns=["device", "date", "lb_mmbtu"])


def read_statements(folder):
    """Heat input (MMBtu) and hours per device per month."""
    df = pd.read_csv(files(folder)["statements"], dtype=str)
    q = df["QUANTITY"].astype(float)
    hi = np.where(df["UNIT"] == "THERMS", q / 10.0, np.where(df["UNIT"] == "MMBTU", q, np.nan))
    mmscf = (df["UNIT"] == "MMSCF").to_numpy()
    hhv = pd.to_numeric(df["HHV_BTU_SCF"], errors="coerce").fillna(NG_HHV).to_numpy()
    hi = np.where(mmscf, q * hhv, hi)
    return pd.DataFrame({"device": df["DEVICE_NO"], "year": df["STMT_YEAR"].astype(int),
                         "month": df["MONTH"].astype(int), "mmbtu": hi, "hours": df["HOURS"].astype(float)})


def read_events(folder):
    df = pd.read_csv(files(folder)["events"], dtype=str).fillna("")
    df["date"] = [dt.datetime.strptime(x, "%m/%d/%Y").date() if "/" in x else dt.date.fromisoformat(x)
                  for x in df["EVENT_DATE"]]
    return df


def catalysts(folder):
    """Each device's catalyst dates: the SCR's installation and every replacement."""
    ev = read_events(folder)
    sel = ev[ev["EVENT_TYPE"].isin(["SCR INSTALLED", "CATALYST"])]
    out = {}
    for r in sel.itertuples():
        out.setdefault(r.DEVICE_NO, []).append(r.date)
    return {k: sorted(v) for k, v in out.items()}


def _spread(st, dev, col):
    """A monthly statement quantity spread evenly over the month's days."""
    s = st[st["device"] == dev]
    out = {}
    for r in s.itertuples():
        first = dt.date(r.year, r.month, 1)
        n = (dt.date(r.year + (r.month == 12), r.month % 12 + 1, 1) - first).days
        v = getattr(r, col) / n
        for i in range(n):
            out[first + dt.timedelta(days=i)] = v
    return out


def cat_hours(days, cats):
    """Operating hours on the catalyst in service at the start of each day."""
    out, h, k = {}, 0.0, 0
    for d in sorted(days):
        while k < len(cats) and d >= cats[k]:
            h, k = 0.0, k + 1
        out[d] = h
        h += days[d]
    return out


class Inputs:
    """The call's inputs, read once."""

    def __init__(self, folder, conv="lbhr"):
        self.folder = folder
        self.permits = read_permits(folder)
        rule = self.permits[self.permits["RULE"] == "4306"]
        self.devices = list(rule["DEVICE_NO"])
        self.facility = dict(zip(rule["DEVICE_NO"], rule["facility"]))
        self.monitored = [d for d, m in zip(rule["DEVICE_NO"], rule["MONITORING"]) if m == "CEMS"]
        self.open = [d for d in self.devices if d not in self.monitored]
        self.kind = {}
        for r in rule.itertuples():
            desc = r.DESCRIPTION
            self.kind[r.DEVICE_NO] = ("engine" if "engine" in desc else "boiler" if "boiler" in desc else
                                      "heater" if "heater" in desc else "turbine" if "turbine" in desc else "furnace")
        self.limit = {r.DEVICE_NO: (float(r.NOX_LIMIT_PPMVD), float(r.REF_O2_PCT), FD[r.FUEL])
                      for r in rule.itertuples() if isinstance(r.NOX_LIMIT_PPMVD, str)}
        self.cems = cems_2026(folder)
        self.tests = read_tests(folder, conv)
        self.st = read_statements(folder)
        self.cats = catalysts(folder)
        self.hours = {d: _spread(self.st, d, "hours") for d in self.open}
        self.heat = {d: _spread(self.st, d, "mmbtu") for d in self.open}
        self.cat = {d: cat_hours(self.hours[d], self.cats.get(d, [])) for d in self.open}
        self.hi26 = {d: sum(v for k, v in self.heat[d].items() if k.year == YEAR) for d in self.open}

    def test_rows(self, since=None, age="hours"):
        rows = []
        for r in self.tests.itertuples():
            if r.device not in self.cat or (since and r.date < since):
                continue
            if age == "hours":
                a = self.cat[r.device][r.date]
            else:
                a = (r.date - max(c for c in self.cats[r.device] if c <= r.date)).days / 365.25
            rows.append((r.device, a, r.lb_mmbtu, r.date))
        return rows


def fit_climb(rows, groups=None):
    """log rate = each unit's level + a common climb a catalyst hour (or one per group)."""
    keys = sorted({r[0] for r in rows})
    gs = sorted({groups(d) if groups else "all" for d in keys})
    X = np.zeros((len(rows), len(keys) + len(gs)))
    y = np.zeros(len(rows))
    for i, (d, a, lb, _) in enumerate(rows):
        X[i, keys.index(d)] = 1
        X[i, len(keys) + gs.index(groups(d) if groups else "all")] = a
        y[i] = np.log(lb)
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ c
    return ({d: float(c[keys.index(d)]) for d in keys},
            {d: float(c[len(keys) + gs.index(groups(d) if groups else "all")]) for d in keys},
            float(np.sqrt(np.sum(res ** 2) / (len(rows) - X.shape[1]))))


def integrate(I, dev, rate):
    """lb of NOx in 2026: each day's heat input at the rate the day's mid-day catalyst hours give."""
    tot = 0.0
    for d, hi in I.heat[dev].items():
        if d.year == YEAR and hi > 0:
            tot += hi * rate(I.cat[dev][d] + I.hours[dev][d] / 2, d)
    return tot


def unit_lb(I, method="golden"):
    """lb of NOx each unmonitored device emitted in 2026 under a method."""
    t = I.tests.sort_values("date")
    out = {}
    if method in ("golden", "bykind", "since2022"):
        rows = I.test_rows(since=dt.date(2022, 1, 1) if method == "since2022" else None)
        lv, b, _ = fit_climb(rows, (lambda d: I.kind[d]) if method == "bykind" else None)
        for d in I.open:
            out[d] = integrate(I, d, lambda h, day, a=lv[d], bb=b[d]: np.exp(a + bb * h))
        return out
    if method == "anchor":
        lv, b, _ = fit_climb(I.test_rows())
        for d in I.open:
            last = t[t["device"] == d].iloc[-1]
            h0 = I.cat[d][last["date"]]
            out[d] = integrate(I, d, lambda h, day, r=last["lb_mmbtu"], bb=b[d], h0=h0: r * np.exp(bb * (h - h0)))
        return out
    if method == "calendar_age":
        lv, b, _ = fit_climb(I.test_rows(age="calendar"))
        for d in I.open:
            cats = I.cats[d]
            out[d] = integrate(I, d, lambda h, day, a=lv[d], bb=b[d], cats=cats:
                               np.exp(a + bb * (day - max(c for c in cats if c <= day)).days / 365.25))
        return out
    for d in I.open:
        s = t[t["device"] == d]["lb_mmbtu"].to_numpy()
        if method == "latest":
            r = s[-1]
        elif method == "mean":
            r = s.mean()
        elif method == "max":
            r = s.max()
        elif method == "median":
            r = np.median(s)
        elif method == "last2":
            r = s[-2:].mean()
        elif method == "limit":
            ppm, o2, fd = I.limit[d]
            r = ppm * 1.194e-7 * fd * 20.9 / (20.9 - o2)
        elif method == "caltrend":
            dd = t[t["device"] == d]
            x = np.array([(v - dt.date(2018, 1, 1)).days / 365.25 for v in dd["date"]])
            bb, aa = np.polyfit(x, np.log(dd["lb_mmbtu"].to_numpy()), 1)
            r = float(np.exp(aa + bb * (dt.date(2026, 7, 1) - dt.date(2018, 1, 1)).days / 365.25))
        else:
            raise ValueError(method)
        out[d] = I.hi26[d] * r
    return out


def facility_tons(I, method="golden"):
    lb = dict(unit_lb(I, method))
    lb.update(I.cems)
    out = {n: 0.0 for n in ORDER}
    for d, v in lb.items():
        out[I.facility[d]] += v / 2000.0
    return out


def five(f):
    return sorted(sorted(f, key=lambda n: -f[n])[:5], key=ORDER.index)


def hround(x):
    return int(np.floor(x + 0.5))


# ------------------------------------------------------------------------------------------------ ask A: utility gas
def _norm(a):
    a = a.upper().replace(".", "")
    for full, short in ((" ROAD", " RD"), (" AVENUE", " AVE"), (" STREET", " ST"), (" BOULEVARD", " BLVD"),
                        (" LANE", " LN"), (" DRIVE", " DR"), (" WAY", " WY")):
        a = a.replace(full, short)
    return re.sub(r"\s+", " ", a).strip()


def read_billing(folder):
    df = pd.read_csv(files(folder)["billing"], dtype=str)
    for c in ("READ_FROM", "READ_TO"):
        df[c] = [dt.datetime.strptime(x, "%m/%d/%Y").date() for x in df[c]]
    for c in ("PRIOR_READ", "CURRENT_READ", "USAGE_CCF"):
        df[c] = df[c].astype(int)
    for c in ("PRESSURE_MULT", "BTU_FACTOR"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    addr = {_norm(a): n for n, _, a in FACILITIES}
    df["facility"] = [addr[_norm(a)] for a in df["SERVICE_ADDRESS"]]
    return df


def is_therm_line(r):
    """On a meter billed from its index (a multiplier shown): usage equal to the read difference times the multiplier
    times the BTU factor is therms, usage equal to the read difference times the multiplier is corrected CCF."""
    ccf = (r.CURRENT_READ - r.PRIOR_READ) * r.PRESSURE_MULT
    return abs(r.USAGE_CCF - ccf * r.BTU_FACTOR) < abs(r.USAGE_CCF - ccf)


def conversion(df):
    """The first read date from which the utility bills therms: read off the meters billed from their index, where
    every line from that date on is therms and every line before it CCF; the corrector meters follow the same bills."""
    idx = df[df["PRESSURE_MULT"].notna()]
    flag = [(r.READ_TO, is_therm_line(r)) for r in idx.itertuples()]
    cut = min(d for d, t in flag if t)
    assert all(t == (d >= cut) for d, t in flag)
    assert not any(cut > d > max(x for x, t in flag if not t) for d in df["READ_TO"])
    return cut


def gas_2026(folder, handling="golden"):
    """MMBtu each facility took from the utility in 2026: each bill's billed usage in therms (corrected CCF times the
    BTU factor before the utility's therm billing, the usage itself from it), spread over its read period by days.
    Rungs: 'all_ccf' (every line CCF), 'all_therms' (every line therms), 'reads' (therms from the index where a
    multiplier shows, the usage as CCF elsewhere), 'by_line' (each index-billed line by its own identity, the corrector
    meters as CCF), 'no_split' (each bill in the year of its current read)."""
    df = read_billing(folder)
    cut = conversion(df)
    out = {n: 0.0 for n in ORDER}
    for r in df.itertuples():
        idx = not np.isnan(r.PRESSURE_MULT)
        if handling in ("golden", "no_split"):
            therms = r.USAGE_CCF if r.READ_TO >= cut else r.USAGE_CCF * r.BTU_FACTOR
        elif handling == "all_ccf":
            therms = r.USAGE_CCF * r.BTU_FACTOR
        elif handling == "all_therms":
            therms = r.USAGE_CCF
        elif handling == "reads":
            therms = ((r.CURRENT_READ - r.PRIOR_READ) * r.PRESSURE_MULT if idx else r.USAGE_CCF) * r.BTU_FACTOR
        elif handling == "by_line":
            therms = r.USAGE_CCF if idx and is_therm_line(r) else r.USAGE_CCF * r.BTU_FACTOR
        else:
            raise ValueError(handling)
        if handling == "no_split":
            out[r.facility] += therms / 10.0 if r.READ_TO.year == YEAR else 0.0
            continue
        n = (r.READ_TO - r.READ_FROM).days
        k = max(0, (min(r.READ_TO, D1) - max(r.READ_FROM, D0)).days)
        out[r.facility] += therms * k / n / 10.0
    return out


# --------------------------------------------------------------------------------------- ask B: emergency engines
def read_engine_logs(folder):
    """Every log row: facility, device, date, the logged value, the sheet's column header."""
    xl = pd.ExcelFile(files(folder)["engine_logs"])
    rows = []
    for sh in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sh, header=1, dtype=object)
        for r in df.itertuples(index=False):
            rows.append((FAC_OF_NO[sh], r[1], pd.Timestamp(r[0]).date(), float(r[2]), df.columns[2]))
    return pd.DataFrame(rows, columns=["facility", "device", "date", "value", "header"])


def _as_hmm(v):
    whole = int(np.floor(v + 1e-9))
    return whole + round((v - whole) * 100) / 60.0


def hmm_facilities(folder):
    """Facilities whose logs hold hours and minutes: read that way, each engine's log sums to its hour meter between two
    inspections, while read as decimal hours it falls short."""
    logs = read_engine_logs(folder)
    insp = pd.read_csv(files(folder)["inspections"], dtype=str)
    insp["date"] = [dt.date.fromisoformat(x) for x in insp["INSPECTION_DATE"]]
    insp["read"] = insp["HOUR_METER"].astype(float)
    replaced = set(replacements(folder))
    out = set()
    for fac, g in logs.groupby("facility"):
        score = {"dec": 0.0, "hmm": 0.0}
        for dev, gd in g.groupby("device"):
            if dev in replaced:
                continue
            ins = insp[insp["DEVICE_NO"] == dev].sort_values("date")
            a, b = ins.iloc[0], ins.iloc[1]
            sel = gd[(gd["date"] >= a["date"]) & (gd["date"] < b["date"])]
            meter = b["read"] - a["read"]
            score["dec"] += abs(sel["value"].sum() - meter)
            score["hmm"] += abs(sum(_as_hmm(v) for v in sel["value"]) - meter)
        if score["hmm"] < score["dec"]:
            out.add(fac)
    return out


def replacements(folder):
    """Engines replaced in 2026: device -> (date, old bhp, old tier), from the event log."""
    ev = read_events(folder)
    out = {}
    for r in ev[ev["EVENT_TYPE"] == "EQUIPMENT"].itertuples():
        m = re.search(r"removed .*?\(([\d,]+) bhp, (Tier [^)]+)\)", r.DESCRIPTION)
        out[r.DEVICE_NO] = (r.date, int(m.group(1).replace(",", "")), m.group(2))
    return out


def engine_lb(folder, handling="golden"):
    """lb of NOx each facility's emergency engines emitted in 2026: hours x bhp x 0.74 x the tier's g/bhp-hr.
    golden: hours-and-minutes logs read as such, and a replaced engine's runs before its replacement at the engine then
    in place. Rungs: 'decimal' (every log as decimal hours), 'current' (every run at the engine installed now),
    'naive' (both)."""
    logs = read_engine_logs(folder)
    pm = read_permits(folder).set_index("DEVICE_NO")
    hmm = hmm_facilities(folder) if handling in ("golden", "current") else set()
    rep = replacements(folder) if handling in ("golden", "decimal") else {}
    out = {n: 0.0 for n in ORDER}
    for r in logs.itertuples():
        h = _as_hmm(r.value) if r.facility in hmm else r.value
        bhp, tier = float(pm.loc[r.device, "RATING"]), pm.loc[r.device, "ENGINE_TIER"]
        if r.device in rep and r.date < rep[r.device][0]:
            bhp, tier = rep[r.device][1], rep[r.device][2]
        out[r.facility] += h * bhp * ENGINE_LF * TIER_NOX[tier] / G_LB
    return out
