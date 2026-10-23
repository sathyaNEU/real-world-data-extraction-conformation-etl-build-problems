"""Reads task478's pack the way an analyst would, from the files alone, and computes the golden and every rung: each
facility's 2026 NOx from its Rule 4306 units, the gas Tamsett Valley Gas delivered to it, and its emergency engines'
NOx. golden.py, checks.py, ceiling.py and writeup.py all go through this module; verify.py does not."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

FD_NG = 8710.0
HREF = 1.035                     # the heat content a burner's level is quoted at (any reference cancels)
TIER_NOX = {"Tier 1": 6.9, "Tier 2": 4.8, "Tier 3": 3.0, "Tier 4 Final": 0.30}
ENGINE_LF = 0.74
G_LB = 453.6
YEAR = 2026
D0, D1 = dt.date(2026, 1, 1), dt.date(2027, 1, 1)
CONVERSION = dt.date(2026, 7, 1)  # the first read the utility's new billing system billed (block 3 names it)
NAMES = {"plan": "tbapcd_lowry_creek_cerp_2027.pdf", "guidance": "tbapcd_emission_inventory_guidance_2026.pdf",
         "cems": "tbapcd_cems_hourly_2026.csv", "tests_old": "tbapcd_source_tests_2018_2021.csv",
         "tests_new": "tbapcd_source_tests_2022_2026.xlsx", "statements": "tbapcd_emission_statements_2018_2026.csv",
         "heat": "tvg_monthly_heat_content_2018_2027.csv", "permits": "tbapcd_permit_devices.csv",
         "events": "tbapcd_compliance_events_2018_2026.csv", "billing": "tvg_commercial_billing_extract_2027-02.csv",
         "engine_logs": "tbapcd_rule4702_engine_logs_2026.xlsx", "inspections": "tbapcd_engine_inspections_2025_2027.csv"}
# the plan's facility table (appendix A): name, facility number, address, gas BTU area
FACILITIES = [("Wexley Point Energy Center", "0418", "2200 Wexley Point Road", "Eastside"),
              ("Ashgrove Refining", "0102", "1 Refinery Avenue", "Eastside"),
              ("Valmora Renewable Fuels", "0577", "880 Distillery Road", "Eastside"),
              ("Sedge Hollow Creamery", "1240", "15500 Sedge Hollow Road", "Westside"),
              ("Haskett Ridge Poultry", "0912", "4917 Haskett Ridge Road", "Eastside"),
              ("St. Aldric Medical Center", "0761", "1300 Aldric Boulevard", "Eastside"),
              ("Lindqvist Paperboard", "0233", "60 Mill Race Lane", "Westside"),
              ("Tamsett State University", "0350", "500 University Drive", "Westside"),
              ("Briar Flats Water Reclamation", "1102", "7700 Briar Flats Road", "Eastside"),
              ("Merriwell Foods", "0645", "210 Cannery Row", "Westside"),
              ("Harrow Linen Services", "1318", "3150 Harrow Lane", "Eastside"),
              ("Orchard Basin Almond Growers", "0880", "4410 Orchard Way", "Westside"),
              ("Penrose Tire Retreading", "1027", "4486 Orchard Way", "Westside"),
              ("Quarry Lane Correctional Facility", "1455", "9 Quarry Lane", "Westside")]
FAC_OF_NO = {no: name for name, no, _, _ in FACILITIES}
FAC_OF_NO["0705"] = "Haskett Ridge Poultry"       # its number before the 2023 change of owner
AREA_OF = {name: area.upper() for name, _, _, area in FACILITIES}
ORDER = [n for n, _, _, _ in FACILITIES]


def files(folder):
    return {k: os.path.join(folder, v) for k, v in NAMES.items()}


def method19(ppm, o2=3.0):
    return ppm * 1.194e-7 * FD_NG * 20.9 / (20.9 - o2)


# ------------------------------------------------------------------------------------------------ the call's inputs
def read_permits(folder):
    df = pd.read_csv(files(folder)["permits"], dtype=str)
    df["facility"] = df["FAC_NO"].map(FAC_OF_NO)
    return df


def read_heat(folder):
    """{(area, year, month): therms a CCF} from the utility's table."""
    df = pd.read_csv(files(folder)["heat"], dtype=str)
    return {(r.BTU_AREA, int(r.MONTH[:4]), int(r.MONTH[5:])): float(r.BTU_FACTOR) for r in df.itertuples()}


def read_cems(folder):
    pm = read_permits(folder)
    key = {(r.FAC_NO, r.CEMS_UNIT_ID): r.DEVICE_NO for r in pm.itertuples() if isinstance(r.CEMS_UNIT_ID, str)}
    df = pd.read_csv(files(folder)["cems"], dtype={"facility_id": str, "unit_id": str, "nox_rate_modc": str})
    df["device"] = [key[(f, u)] for f, u in zip(df["facility_id"], df["unit_id"])]
    df["month"] = [int(x[5:7]) for x in df["op_date"]]
    return df


def cems_2026(folder, df=None):
    """lb of NOx each monitored device reported for 2026, substitute hours as reported."""
    df = read_cems(folder) if df is None else df
    return df.groupby("device")["nox_mass_lb"].sum().to_dict()


def read_tests(folder, conv="ppm"):
    """Every source test in lb/MMBtu: the new database's own column; the older one from ppm through Method 19 ('ppm')
    or from lb/hr over the device's rating times the test's load ('lbhr')."""
    f = files(folder)
    pm = read_permits(folder).set_index("DEVICE_NO")
    old = pd.read_csv(f["tests_old"], dtype=str)
    rows = []
    for r in old.itertuples():
        dev = "D-" + r.DEVICE_NO
        if conv == "ppm":
            lb = method19(float(r.NOX_PPMVD), float(r.O2_REF))
        else:
            lb = float(r.NOX_LB_HR) / (float(pm.loc[dev, "RATING"]) * float(r.LOAD_PCT) / 100.0)
        rows.append((dev, dt.datetime.strptime(r.TEST_DATE, "%m/%d/%Y").date(), lb))
    new = pd.read_excel(f["tests_new"], sheet_name="Results")
    for r in new.itertuples(index=False):
        rows.append((r[2], pd.Timestamp(r[3]).date(), float(r[7])))
    return pd.DataFrame(rows, columns=["device", "date", "lb_mmbtu"]).sort_values(["device", "date"])


def read_statements(folder, heat=None, mmscf_hhv=None):
    """Heat input (MMBtu) and hours per device per month; MMSCF at the facility's BTU area's heat content that month
    (guidance section 4), or at a fixed Btu/scf if mmscf_hhv is given."""
    heat = heat or read_heat(folder)
    df = pd.read_csv(files(folder)["statements"], dtype=str)
    out = []
    for r in df.itertuples():
        q = float(r.QUANTITY)
        y, m = int(r.STMT_YEAR), int(r.MONTH)
        if r.UNIT == "THERMS":
            hi = q / 10.0
        elif r.UNIT == "MMBTU":
            hi = q
        else:
            area = AREA_OF[FAC_OF_NO[r.FAC_NO]]
            hi = q * (mmscf_hhv if mmscf_hhv else heat[(area, y, m)] * 1000.0)
        out.append((r.DEVICE_NO, y, m, hi, float(r.HOURS)))
    return pd.DataFrame(out, columns=["device", "year", "month", "mmbtu", "hours"])


def read_events(folder):
    df = pd.read_csv(files(folder)["events"], dtype=str).fillna("")
    df["date"] = [dt.datetime.strptime(x, "%m/%d/%Y").date() if "/" in x else dt.date.fromisoformat(x)
                  for x in df["EVENT_DATE"]]
    return df


class Inputs:
    """The call's inputs, read once."""

    def __init__(self, folder, conv="ppm", mmscf_hhv=None):
        self.folder = folder
        self.permits = read_permits(folder)
        rule = self.permits[self.permits["RULE"] == "4306"]
        self.devices = list(rule["DEVICE_NO"])
        self.facility = dict(zip(rule["DEVICE_NO"], rule["facility"]))
        self.area = {d: AREA_OF[f] for d, f in self.facility.items()}
        self.monitored = [d for d, m in zip(rule["DEVICE_NO"], rule["MONITORING"]) if m == "CEMS"]
        self.open = [d for d in self.devices if d not in self.monitored]
        self.control = dict(zip(rule["DEVICE_NO"], rule["NOX_CONTROL"]))
        self.limit = {r.DEVICE_NO: method19(float(r.NOX_LIMIT_PPMVD), float(r.REF_O2_PCT)) for r in rule.itertuples()}
        self.heatc = read_heat(folder)
        self.cems_df = read_cems(folder)
        self.cems = cems_2026(folder, self.cems_df)
        self.tests = read_tests(folder, conv)
        self.st = read_statements(folder, self.heatc, mmscf_hhv)
        s26 = self.st[self.st["year"] == YEAR]
        self.hi_month = {d: {int(m): v for m, v in zip(g["month"], g["mmbtu"])} for d, g in s26.groupby("device")}

    def hv(self, dev, d):
        return self.heatc[(self.area[dev], d.year, d.month)]

    def pb1_months(self):
        """The monitored low-NOx burner's measured hours by month: (month, mean rate) for the paperboard power boiler
        (the one monitored unit whose NOx control is a burner)."""
        burners = [d for d in self.monitored if "burner" in self.control[d]]
        dev = burners[0]
        g = self.cems_df[(self.cems_df["device"] == dev) & (self.cems_df["nox_rate_modc"] == "01")]
        return dev, {int(m): float(v) for m, v in g.groupby("month")["nox_rate_lb_mmbtu"].mean().items()}

    def k_pb1(self, hourly=True):
        """The rise of the monitored burner's log NOx rate with its area's heat content (per unit of heat content over
        HREF), from its measured hours or from its monthly means."""
        burners = [d for d in self.monitored if "burner" in self.control[d]]
        dev = burners[0]
        g = self.cems_df[(self.cems_df["device"] == dev) & (self.cems_df["nox_rate_modc"] == "01")]
        x = np.array([self.heatc[(self.area[dev], YEAR, int(m))] / HREF - 1 for m in g["month"]])
        y = np.log(g["nox_rate_lb_mmbtu"].to_numpy())
        if not hourly:
            mm = g.groupby("month")["nox_rate_lb_mmbtu"].mean()
            x = np.array([self.heatc[(self.area[dev], YEAR, int(m))] / HREF - 1 for m in mm.index])
            y = np.log(mm.to_numpy())
        return float(np.polyfit(x, y, 1)[0])

    def k_tests(self, area="WESTSIDE"):
        """The same rise from the burners' own tests: each unit's level, one common slope, Westside units (where the
        heat content moves) or every burner."""
        xs, ys = [], []
        for d, g in self.tests.groupby("device"):
            if "burner" not in self.control.get(d, "") or (area and self.area[d] != area):
                continue
            h = np.array([self.hv(d, t) / HREF - 1 for t in g["date"]])
            l = np.log(g["lb_mmbtu"].to_numpy())
            xs += list(h - h.mean())
            ys += list(l - l.mean())
        xs, ys = np.array(xs), np.array(ys)
        return float(np.dot(xs, ys) / np.dot(xs, xs))


def unit_lb(I, method="golden", k=None):
    """lb of NOx each unmonitored device emitted in 2026 under a method. golden: each burner's tests carried from
    their months' heat content to each 2026 month's by the monitored burner's rise (a level per unit from all its
    tests); an SCR unit's tests held."""
    out = {}
    if method in ("golden", "latest_hv", "golden_ktests", "latest_hv_ktests", "golden_monthly", "golden_allburners"):
        if k is None:
            k = (I.k_tests() if "ktests" in method else I.k_tests(area=None) if method == "golden_allburners"
                 else I.k_pb1(hourly=method != "golden_monthly"))
    if method in ("pb1_all", "pb1_area"):
        _, pbm = I.pb1_months()
    for d in I.open:
        g = I.tests[I.tests["device"] == d]
        s = g["lb_mmbtu"].to_numpy()
        dates = list(g["date"])
        burner = "burner" in I.control[d]
        months = I.hi_month[d]
        if method in ("golden", "latest_hv", "golden_ktests", "latest_hv_ktests", "golden_monthly",
                      "golden_allburners") and burner:
            adj = [v / np.exp(k * (I.hv(d, t) / HREF - 1)) for v, t in zip(s, dates)]
            lvl = adj[-1] if method.startswith("latest") else float(np.exp(np.mean(np.log(adj))))
            out[d] = sum(mm * lvl * np.exp(k * (I.heatc[(I.area[d], YEAR, m)] / HREF - 1)) for m, mm in months.items())
            continue
        if method in ("pb1_all", "pb1_area") and burner and (method == "pb1_all" or I.area[d] == "WESTSIDE"):
            r0, t0 = s[-1], dates[-1]
            out[d] = sum(mm * r0 * pbm[m] / pbm[t0.month] for m, mm in months.items())
            continue
        if method in ("latest", "golden", "latest_hv", "golden_ktests", "latest_hv_ktests", "golden_monthly",
                      "golden_allburners", "pb1_all", "pb1_area"):
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
            r = I.limit[d]
        elif method == "limit_stale":
            r = I.limit[d] if dates[-1].year < YEAR else s[-1]
        elif method == "caltrend":
            x = np.array([(v - dt.date(2018, 1, 1)).days / 365.25 for v in dates])
            bb, aa = np.polyfit(x, np.log(s), 1)
            r = float(np.exp(aa + bb * (dt.date(2026, 7, 1) - dt.date(2018, 1, 1)).days / 365.25))
        else:
            raise ValueError(method)
        out[d] = sum(months.values()) * r
    return out


def facility_tons(I, method="golden", k=None):
    lb = dict(unit_lb(I, method, k))
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
    df["USAGE_THERMS"] = df["USAGE_THERMS"].astype(int)
    df["BTU_FACTOR"] = df["BTU_FACTOR"].astype(float)
    addr = {_norm(a): n for n, _, a, _ in FACILITIES}
    df["facility"] = [addr[_norm(a)] for a in df["SERVICE_ADDRESS"]]
    return df


def combined_accounts(df):
    """Accounts whose meters carry the same usage on every bill: the account's combined usage repeated on each line."""
    out = set()
    for acct, g in df.groupby("ACCOUNT_NO"):
        if g["METER_NO"].nunique() < 2:
            continue
        if all(gg["USAGE_THERMS"].nunique() == 1 for _, gg in g.groupby("READ_TO")):
            out.add(acct)
    return out


def gas_2026(folder, handling="golden"):
    """MMBtu each facility took from the utility in 2026: each billing period's therms (a line read before the
    conversion holds corrected CCF, so times its BTU factor; from the conversion therms), a combined account's usage
    once per period, spread over the read period by days. Rungs: 'as_labelled' (every line therms, every line
    summed), 'all_ccf' (every line times its BTU factor), 'no_dedupe' (the conversion handled, every line summed),
    'as_labelled_dedupe' (the label read as is, the combined usage once), 'no_split' (the golden, each bill in the year
    of its current read)."""
    df = read_billing(folder)
    comb = combined_accounts(df) if handling in ("golden", "as_labelled_dedupe", "all_ccf", "no_split") else set()
    seen = set()
    out = {n: 0.0 for n in ORDER}
    for r in df.itertuples():
        if r.ACCOUNT_NO in comb:
            key = (r.ACCOUNT_NO, r.READ_TO)
            if key in seen:
                continue
            seen.add(key)
        if handling in ("golden", "no_dedupe", "no_split"):
            therms = r.USAGE_THERMS if r.READ_TO >= CONVERSION else r.USAGE_THERMS * r.BTU_FACTOR
        elif handling == "all_ccf":
            therms = r.USAGE_THERMS * r.BTU_FACTOR
        elif handling in ("as_labelled", "as_labelled_dedupe"):
            therms = r.USAGE_THERMS
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
    """Every log row: facility, device, date, the logged value, purpose."""
    xl = pd.ExcelFile(files(folder)["engine_logs"])
    rows = []
    for sh in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sh, header=1, dtype=object)
        for r in df.itertuples(index=False):
            rows.append((FAC_OF_NO[sh], r[1], pd.Timestamp(r[0]).date(), float(r[2]), r[3]))
    return pd.DataFrame(rows, columns=["facility", "device", "date", "value", "purpose"])


def _as_hmm(v):
    whole = int(np.floor(v + 1e-9))
    return whole + round((v - whole) * 100) / 60.0


def elog_dates(folder):
    """The date from which each facility's log holds hours and minutes: from it every value's fraction is a count of
    minutes (never .60 or more) and the weekly readiness runs, about half an hour, read 0.24 to 0.36 where before they
    read 0.40 to 0.60. The hour meters agree with that reading (checks.py B1)."""
    logs = read_engine_logs(folder)
    out = {}
    for fac, g in logs.groupby("facility"):
        g = g.sort_values("date")
        ready = g[g["purpose"].str.startswith("Testing")]
        for d in sorted(set(g["date"])):
            after, before = g[g["date"] >= d], ready[ready["date"] < d]
            ra = ready[ready["date"] >= d]
            frac_ok = all(round((v - np.floor(v + 1e-9)) * 100) <= 59 for v in after["value"])
            if frac_ok and len(ra) >= 4 and ra["value"].max() < 0.40 and len(before) and before["value"].min() >= 0.40:
                out[fac] = d
                break
    return out


def outages(folder):
    """Each facility's 2026 outages from the event log: date -> hours its emergency engines carried it."""
    ev = read_events(folder)
    out = {}
    for r in ev[ev["EVENT_TYPE"] == "OUTAGE"].itertuples():
        m = re.search(r"for ([\d.]+) hours", r.DESCRIPTION)
        out.setdefault(FAC_OF_NO[r.FAC_NO], {})[r.date] = float(m.group(1))
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
    golden: each facility's log read as hours and minutes from its e-logbook date, an emergency line that carries
    more than the outage the event log records read as the outage's hours, and a replaced engine's runs before its
    replacement at the engine then in place. Rungs: 'naive' (every value as decimal hours, every line as logged, the
    engines now permitted), 'no_elog', 'no_bank', 'current' (each device alone undone)."""
    logs = read_engine_logs(folder)
    pm = read_permits(folder).set_index("DEVICE_NO")
    el = elog_dates(folder) if handling in ("golden", "no_bank", "current") else {}
    outs = outages(folder) if handling in ("golden", "no_elog", "current") else {}
    rep = replacements(folder) if handling in ("golden", "no_elog", "no_bank") else {}
    out = {n: 0.0 for n in ORDER}
    for r in logs.itertuples():
        h = _as_hmm(r.value) if (r.facility in el and r.date >= el[r.facility]) else r.value
        if r.purpose.startswith("Emergency") and r.facility in outs and r.date in outs[r.facility]:
            h = min(h, outs[r.facility][r.date])
        bhp, tier = float(pm.loc[r.device, "RATING"]), pm.loc[r.device, "ENGINE_TIER"]
        if r.device in rep and r.date < rep[r.device][0]:
            bhp, tier = rep[r.device][1], rep[r.device][2]
        out[r.facility] += h * bhp * ENGINE_LF * TIER_NOX[tier] / G_LB
    return out
