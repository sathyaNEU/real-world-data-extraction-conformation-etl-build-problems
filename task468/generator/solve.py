"""task468 architecture 6: every owed figure computed from target/ alone, with the routes the checks price."""
import csv
import datetime as dt
import os

import numpy as np
import openpyxl

F = {"lims_old": "glw_lims_trade_waste_results_2025-01_to_2026-02.csv",
     "lims_new": "glw_labware_trade_waste_results_2026.csv",
     "telemetry": "glw_trade_waste_flow_telemetry_2026.csv",
     "register": "glw_trade_waste_agreements_register_2026.xlsx",
     "crosswalk": "glw_sampling_point_crosswalk.csv",
     "jobs": "glw_field_service_jobs_2026.xlsx"}
TZ = dt.timedelta(hours=10)
Y0, Y1 = dt.datetime(2026, 1, 1), dt.datetime(2027, 1, 1)
QB = [dt.datetime(2026, m, 1) for m in (1, 4, 7, 10)] + [Y1]
RL_SS = 5.0


def rows(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sheet(path, name):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[name]
    vals = list(ws.iter_rows(values_only=True))
    hdr = list(vals[0])
    return [dict(zip(hdr, r)) for r in vals[1:] if any(v is not None for v in r)]


def load(target):
    p = lambda k: os.path.join(target, F[k])
    reg = sheet(p("register"), "Agreements")
    cross = rows(p("crosswalk"))
    point_cust = {r["Sampling point"]: r["Customer"] for r in reg}
    legacy = {r["legacy_site_code"]: point_cust[r["point_id"]] for r in cross}
    lim = {}
    for r in reg:
        v = float(r["COD limit"])
        lim[r["Customer"]] = v / 1000.0 if str(r["COD limit unit"]).startswith("kg") else v
    return {"target": target, "reg": reg, "point_cust": point_cust, "legacy": legacy, "limit": lim,
            "custs": [r["Customer"] for r in reg]}


# ------------------------------------------------------------------------------------------------ laboratory

def lab(D, dup="drop", rerun="replace", below="half", year_clock="local"):
    """Each compliance sample: customer, local date, analytes. Old LIMS (local times) and LabWare (UTC)."""
    samples = {}
    for r in rows(os.path.join(D["target"], F["lims_old"])):
        when = dt.datetime.strptime(r["Sampled"], "%d/%m/%Y %H:%M")
        key = ("old", r["Sample No"])
        s = samples.setdefault(key, {"cust": D["legacy"][r["Site Code"]], "when": when, "an": {}})
        v = float(r["Result"])
        if r["Test"] == "SS" and r["Qualifier"] == "<":
            v = {"half": RL_SS / 2, "rl": RL_SS, "zero": 0.0}[below]
        s["an"][{"COD": "cod", "TOC": "toc", "CL": "cl", "SS": "ss", "PH": "ph"}[r["Test"]]] = v
    reruns = []
    for r in rows(os.path.join(D["target"], F["lims_new"])):
        utc = dt.datetime.strptime(r["collected_utc"], "%Y-%m-%dT%H:%M:%SZ")
        when = utc + TZ if year_clock == "local" else utc
        sid = r["sample_id"]
        an = {"TOC (NPOC)": "toc", "Chloride": "cl", "Suspended Solids": "ss", "pH": "ph"}[r["analyte"]]
        v = float(r["value"])
        if an == "ss" and r["result_qualifier"] == "<":
            v = {"half": RL_SS / 2, "rl": RL_SS, "zero": 0.0}[below]
        if sid.endswith("-D"):
            if dup == "drop":
                continue
            if dup == "own":
                key = ("new", sid)
            else:
                continue
        elif sid.endswith("-R"):
            reruns.append((sid[:-2], an, v, when))
            continue
        else:
            key = ("new", sid)
        s = samples.setdefault(key, {"cust": D["point_cust"][r["point_id"]], "when": when, "an": {}})
        s["an"][an] = v
    for base, an, v, when in reruns:
        key = ("new", base)
        if rerun == "replace":
            samples[key]["an"][an] = v
        elif rerun == "own":
            samples[("new", base + "-R")] = {"cust": samples[key]["cust"], "when": when, "an": {an: v}}
    return samples


def parallel(samples):
    return [s for s in samples.values() if "toc" in s["an"] and "cod" in s["an"]]


def fit(par, form="chloride", intercept=True, weights=None):
    toc = np.array([s["an"]["toc"] for s in par])
    cod = np.array([s["an"]["cod"] for s in par])
    cl = np.array([s["an"]["cl"] for s in par])
    cols = [toc] + ([cl] if form == "chloride" else [])
    if intercept:
        cols = [np.ones_like(toc)] + cols
    X = np.c_[tuple(cols)]
    w = np.ones_like(cod) if weights is None else weights(cod)
    b = np.linalg.lstsq(X * np.sqrt(w)[:, None], cod * np.sqrt(w), rcond=None)[0]
    if not intercept:
        b = np.r_[0.0, b]
    if form != "chloride":
        b = np.r_[b, 0.0]
    return b   # intercept, per mg/L TOC, per mg/L chloride


def converter(samples, route="golden"):
    par = parallel(samples)
    if route == "golden":
        b = fit(par)
        return lambda c, an: b[0] + b[1] * an["toc"] + b[2] * an["cl"]
    if route == "chloride_origin":
        b = fit(par, intercept=False)
        return lambda c, an: b[1] * an["toc"] + b[2] * an["cl"]
    if route == "chloride_wls":
        b = fit(par, weights=lambda y: 1.0 / y ** 2)
        return lambda c, an: b[0] + b[1] * an["toc"] + b[2] * an["cl"]
    if route == "pooled_ratio":
        r = sum(s["an"]["cod"] for s in par) / sum(s["an"]["toc"] for s in par)
        return lambda c, an: r * an["toc"]
    if route == "pooled_ols":
        b = fit(par, form="toc")
        return lambda c, an: b[0] + b[1] * an["toc"]
    if route == "own_ratio":
        own = {}
        for c in set(s["cust"] for s in par):
            ps = [s for s in par if s["cust"] == c]
            own[c] = sum(s["an"]["cod"] for s in ps) / sum(s["an"]["toc"] for s in ps)
        return lambda c, an: own[c] * an["toc"]
    if route == "own_median_ratio":
        own = {}
        for c in set(s["cust"] for s in par):
            own[c] = float(np.median([s["an"]["cod"] / s["an"]["toc"] for s in par if s["cust"] == c]))
        return lambda c, an: own[c] * an["toc"]
    if route == "own_ols":
        own = {}
        for c in set(s["cust"] for s in par):
            own[c] = fit([s for s in par if s["cust"] == c], form="toc")
        return lambda c, an: own[c][0] + own[c][1] * an["toc"]
    raise ValueError(route)


# ------------------------------------------------------------------------------------------------ volumes

def meters(D):
    """Each customer's meter segments: (serial, opening read or None, final read or None, on, off) in local time."""
    jobs = sheet(os.path.join(D["target"], F["jobs"]), "Jobs")
    seg = {}
    reg_meter = {r["Customer"]: r["Flow meter"] for r in D["reg"]}
    for c in D["custs"]:
        ex = [j for j in jobs if j["Customer"] == c and j["Job type"] == "Meter exchange"]
        if not ex:
            seg[c] = [(reg_meter[c], None, None, None, None)]
            continue
        j = ex[0]
        off = dt.datetime.strptime(j["Started (local)"], "%d/%m/%Y %H:%M")
        on = dt.datetime.strptime(j["Completed (local)"], "%d/%m/%Y %H:%M")
        seg[c] = [(j["Asset removed"], None, float(j["Removed final read (kL)"]), None, off),
                  (j["Asset installed"], float(j["Installed opening read (kL)"]), None, on, None)]
    return seg


def telemetry(D, clock="local"):
    tel = {}
    for r in rows(os.path.join(D["target"], F["telemetry"])):
        t = dt.datetime.strptime(r["reading_utc"], "%Y-%m-%dT%H:%M:%SZ")
        tel.setdefault(r["meter_serial"], {})[t + TZ if clock == "local" else t] = float(r["register"])
    return tel


def cumulative(D, tel, seg, c):
    """Volume a customer discharged from local 2026-01-01 00:00 to time t (local), across a meter exchange."""
    s = seg[c]
    first = s[0][0]
    base = tel[first][Y0]

    def cum(t):
        if len(s) == 1 or t <= s[0][4]:
            return tel[first][t] - base
        old_vol = s[0][2] - base
        return old_vol + tel[s[1][0]][t] - s[1][1]
    return cum


def volumes(D, tel=None, seg=None):
    tel = tel or telemetry(D)
    seg = seg or meters(D)
    out = {}
    for c in D["custs"]:
        cum = cumulative(D, tel, seg, c)
        out[c] = {"year": cum(Y1), "q": [cum(QB[i + 1]) - cum(QB[i]) for i in range(4)], "cum": cum}
    return out


def day_volume(vol, c, d):
    t0 = dt.datetime.combine(d, dt.time(0))
    return vol[c]["cum"](t0 + dt.timedelta(days=1)) - vol[c]["cum"](t0)


# ------------------------------------------------------------------------------------------------ masses

def masses(D, samples, vol, conv, analyte="cod", composites_only=True):
    out = {}
    for c in D["custs"]:
        num = den = 0.0
        for s in samples.values():
            if s["cust"] != c or s["when"].year != 2026:
                continue
            an = s["an"]
            if composites_only and not ("toc" in an or "cod" in an):
                continue      # an inspection grab: suspended solids and pH only, not a compliance composite
            if analyte == "cod":
                if "cod" in an:
                    x = an["cod"]
                elif "toc" in an:
                    x = conv(c, an)
                else:
                    continue
            else:
                if analyte not in an:
                    continue
                x = an[analyte]
            v = day_volume(vol, c, s["when"].date())
            num += x * v
            den += v
        out[c] = vol[c]["year"] * num / den / 1e6
    return out


TYPES = ["GT", "SE", "PL", "LL"]


def liquid(target, join="identity"):
    """Tankered waste received in 2026 by waste code and quarter of the receival date (local, accepted rows)."""
    log = rows(os.path.join(target, "glw_liquid_waste_receival_2026.csv"))
    man = sheet(os.path.join(target, "qld_waste_tracking_manifests_glw_2026.xlsx"), "Manifests")
    code = {m["Receival docket"]: m["Waste code"] for m in man}
    out = {t: [0.0] * 4 for t in TYPES}
    last = {}
    for r in sorted(log, key=lambda r: (dt.datetime.strptime(r["received"], "%d/%m/%Y %H:%M"), r["docket"])):
        when = dt.datetime.strptime(r["received"], "%d/%m/%Y %H:%M")
        if r["status"] != "Accepted":
            continue
        c = code.get(r["docket"])
        if c is not None:
            last[r["truck_rego"]] = (when, c)
        elif join == "identity":
            prev = last.get(r["truck_rego"])
            if prev and when - prev[0] <= dt.timedelta(hours=2):
                c = prev[1]
        if c is None or when.year != 2026:
            continue
        out[c][(when.month - 1) // 3] += float(r["volume_kl"])
    return out


def solve(target, route="golden"):
    D = load(target)
    S = lab(D)
    vol = volumes(D)
    conv = converter(S, route)
    cod = masses(D, S, vol, conv)
    ss = masses(D, S, vol, conv, analyte="ss")
    over = sorted(c for c in D["custs"] if cod[c] > D["limit"][c])
    return {"D": D, "samples": S, "vol": vol, "cod": cod, "ss": ss, "over": over, "liquid": liquid(target),
            "fit": fit(parallel(S)), "n_parallel": len(parallel(S))}


if __name__ == "__main__":
    import sys
    R = solve(sys.argv[1])
    print("fit", np.round(R["fit"], 4), "parallel samples", R["n_parallel"])
    for c in R["D"]["custs"]:
        print("%-30s vol %9.0f  COD %7.1f t  limit %7.1f  %s  SS %6.1f t  q %s" % (
            c, R["vol"][c]["year"], R["cod"][c], R["D"]["limit"][c], "OVER" if c in R["over"] else "    ",
            R["ss"][c], [round(x) for x in R["vol"][c]["q"]]))
