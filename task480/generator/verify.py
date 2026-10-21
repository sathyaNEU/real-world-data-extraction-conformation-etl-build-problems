"""An independent verifier: it reads only the shipped bundle (target/, golden/, submission.md) and recomputes the call
and every graded figure with its own code (pandas, pdftotext for the annual report's station list), then compares
with the golden workbook and the write-up."""
import datetime as dt
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

KM = 0.621371192
TON = 907184.74


def load(t):
    reg = pd.read_csv(os.path.join(t, "vehicle_registrations_2026-07-01.csv"), dtype=str)
    tst = pd.read_csv(os.path.join(t, "eip_inspections_2024_2025.csv"), dtype=str)
    cty = pd.read_csv(os.path.join(t, "county_codes.csv"), dtype=str)
    body = pd.read_csv(os.path.join(t, "registration_body_codes.csv"), dtype=str)
    rates = pd.read_excel(os.path.join(t, "nox_running_rates_cy2027.xlsx"), sheet_name="Table 2")
    return reg, tst, cty, body, rates


def completed(tst):
    """Completed initial tests, re-sent rows dropped, earliest first."""
    t = tst.drop_duplicates()
    t = t[(t["test_type"] == "INITIAL") & t["result"].isin(["PASS", "FAIL"])].copy()
    t["when"] = pd.to_datetime(t["test_start"])
    return t.sort_values(["when", "test_id"], kind="mergesort")


def first_test(reg, t, vins, plates, mys):
    """Each vehicle's first completed initial test: by VIN, else by plate and model year among the tests whose VIN
    is on no registration record."""
    by_vin = t.drop_duplicates("vin").set_index("vin")
    known = set(reg["vin"])
    orph = t[~t["vin"].isin(known)].copy()
    orph["my"] = orph["model_year"].astype(int)
    by_pm = orph.drop_duplicates(["plate", "my"]).set_index(["plate", "my"])
    rows = []
    for v, p, m in zip(vins, plates, mys):
        if v in by_vin.index:
            rows.append(by_vin.loc[v])
        elif (p, m) in by_pm.index:
            rows.append(by_pm.loc[(p, m)])
        else:
            rows.append(None)
    return rows


def nox(t):
    reg, tst, cty, body, rates = load(t)
    names = dict(zip(cty["county_no"], cty["county"]))
    el = reg[(reg["record_status"] == "ACTIVE") & reg["county_no"].isin(names)].copy()
    el["my"] = el["model_year"].astype(int)
    el = el[el["my"].between(2005, 2014) & el["fuel_code"].isin(["G", "F"]) & el["gvwr_class"].isin(["1", "2a"])].copy()
    el["county"] = el["county_no"].map(names)
    cls = dict(zip(body["body_code"], body["program_class"]))
    rt = rates.set_index("model_year")
    el["rate"] = [rt.at[m, "passenger_car_g_per_mi" if cls[b] == "PC" else "light_truck_g_per_mi"]
                  for m, b in zip(el["my"], el["body_code"])]
    t_ = completed(tst)
    t_["odo"] = pd.to_numeric(t_["odometer"])
    t_ = t_[t_["odo"].notna() & ~t_["odo"].isin([0, 999999])].copy()
    t_["miles"] = np.where(t_["odometer_unit"] == "KM", t_["odo"] * KM, t_["odo"])
    t_["age"] = (t_["when"] - pd.to_datetime(t_["model_year"] + "-01-01")).dt.days / 365.25
    p = np.polyfit(t_["age"].to_numpy(), t_["miles"].to_numpy(), 2)
    M = lambda a: np.polyval(p, a)
    rows = first_test(reg, t_, el["vin"], el["plate"], el["my"])
    lev = np.array([r["miles"] if r is not None else np.nan for r in rows], float)
    age = np.array([r["age"] if r is not None else np.nan for r in rows], float)
    a0, a1 = 2027 - el["my"].to_numpy(), 2028 - el["my"].to_numpy()
    el["m27"] = lev / M(age) * (M(a1) - M(a0))
    el["m27"] = el["m27"].fillna(el.groupby(["county", "my"])["m27"].transform("mean"))
    tons = (el["m27"] * el["rate"]).groupby(el["county"]).sum() / TON
    return tons, el.groupby("county").size(), pd.Series(~np.isnan(lev), index=el.index).groupby(el["county"]).sum()


def pilot(t):
    reg, tst, cty, body, rates = load(t)
    names = dict(zip(cty["county_no"], cty["county"]))
    v = pd.read_excel(os.path.join(t, "vrp_pilot_vouchers_2025.xlsx"), dtype=str)
    inv = pd.read_csv(os.path.join(t, "vrp_pilot_dismantler_invoices_2025.csv"), dtype=str).drop_duplicates()
    active = set(reg.loc[reg["record_status"] == "ACTIVE", "vin"])
    v = v[~v["vin"].isin(active)].copy()
    per_line = inv[inv["dismantler_licence"] != "D-2864"]
    charge = per_line.groupby("tow_zone")["amount"].agg(lambda s: float(s.astype(float).mode().iloc[0]))
    zone = inv.drop_duplicates("voucher_no").set_index("voucher_no")["tow_zone"]
    v["charge"] = v["voucher_no"].map(zone).map(charge)
    v["county"] = v["applicant_county_no"].map(names)
    return v.groupby("county").size(), v.groupby("county")["charge"].sum()


def annual_list(t):
    """The 2024 annual report's station list: number, name, county, status, off the PDF's text layer."""
    txt = subprocess.run(["pdftotext", "-layout", os.path.join(t, "eip_annual_report_2024.pdf"), "-"],
                         capture_output=True, text=True).stdout
    out = []
    for line in txt.splitlines():
        m = re.match(r"^\s*(\d{4})\s{2,}(.+?)\s{2,}(.+?)\s{2,}([A-Z][a-z]+)\s{2,}(closed .+|licensed)\s*$", line)
        if m:
            out.append(dict(no=m.group(1), name=m.group(2).strip(), county=m.group(4), status=m.group(5).strip()))
    return pd.DataFrame(out)


def stations(t):
    reg, tst, cty, body, rates = load(t)
    names = dict(zip(cty["county_no"], cty["county"]))
    sr = pd.read_excel(os.path.join(t, "eip_station_register_2026-06-30.xlsx"), dtype=str)
    cur = sr.set_index("station_no")
    old = annual_list(t)
    tests = completed(tst)
    prior, cut = {}, {}
    for no, g in old.groupby("no"):
        g = g[g["county"] != cur.at[no, "county"]] if no in cur.index else g
        if len(g):
            # a number the 2024 report places in another county than the register: the earlier station held it
            # until the longest pause in the number's tests, the register's station after it
            prior[no] = g["county"].iloc[0]
            days = tests.loc[tests["station_no"] == no, "when"].dt.normalize().drop_duplicates().sort_values()
            gaps = days.diff()
            cut[no] = days.iloc[int(np.argmax(gaps.fillna(pd.Timedelta(0)).to_numpy()))].date()
    act = reg[reg["record_status"] == "ACTIVE"].copy()
    act["my"] = act["model_year"].astype(int)
    act["county"] = act["county_no"].map(names)
    rows = first_test(reg, completed(tst), act["vin"], act["plate"], act["my"])
    where = []
    for r in rows:
        if r is None:
            where.append(None)
            continue
        no, d = r["station_no"], r["when"].date()
        if no in prior and d < cut[no]:
            where.append(prior[no])
        else:
            where.append(cur.at[no, "county"] if no in cur.index else prior.get(no))
    act["st"] = where
    return (act["st"] == act["county"]).groupby(act["county"]).sum()


def main(target, gdir):
    ok = True
    tons, n, read = nox(target)
    q = sorted(c for c in tons.index if tons[c] >= 10.0)
    wb = os.path.join(gdir, "retirement_program_county_nox_2027.xlsx")
    g = pd.read_excel(wb, sheet_name="Intake counties", dtype={"County no.": str})
    g = g[g["County no."].notna() & (g["County no."] != "")].set_index("County")
    gq = sorted(g.index[g["Intake events"] == "Yes"])
    print("verify: %d counties at 10 tons or more %s (golden %s)" % (len(q), q, gq))
    ok &= q == gq
    for c in tons.index:
        same = int(tons[c] + 0.5) == int(g.at[c, "2027 NOx (short tons)"]) and int(n[c]) == int(g.at[c, "Eligible vehicles"]) \
            and int(read[c]) == int(g.at[c, "With a usable reading"])
        if not same:
            print("verify: MISMATCH %s %.3f tons, %d eligible, %d read" % (c, tons[c], n[c], read[c]))
        ok &= same
    pn, pc = pilot(target)
    p = pd.read_excel(wb, sheet_name="Pilot 2025").dropna(subset=["County no."]).set_index("County")
    for c in pn.index:
        same = int(pn[c]) == int(p.at[c, "Vehicles retired"]) and int(round(pc[c])) == int(p.at[c, "Dismantler charges paid ($)"])
        print("verify: pilot %s %d retired, $%s %s" % (c, pn[c], "{:,.0f}".format(pc[c]), "ok" if same else "MISMATCH"))
        ok &= same
    st = stations(target)
    s = pd.read_excel(wb, sheet_name="Station inspections").set_index("County")
    bad = [c for c in st.index if int(st[c]) != int(s.at[c, "Initial inspections at a station in the county"])]
    print("verify: station counts %s" % ("agree in all twelve counties" if not bad else "MISMATCH %s" % bad))
    ok &= not bad
    sub = open(os.path.join(os.path.dirname(gdir), "submission.md"), encoding="utf-8").read()
    for c in tons.index:
        ok &= ("- %s: %d; " % (c, int(tons[c] + 0.5))) in sub and ("- %s: %s" % (c, "{:,}".format(int(st[c])))) in sub
    for c in pn.index:
        ok &= ("- %s: %d vehicles; $%s" % (c, pn[c], "{:,.0f}".format(pc[c]))) in sub
    print("verify: %s" % ("PASS" if ok else "FAIL"))
    return bool(ok)


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
