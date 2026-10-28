"""An independent path to every graded figure of task281, sharing no code with analysis.py: pandas readers, a
regex-free certificate read by page and table position, the Weibull fitted on its full likelihood rather than the
profile score, energy by month arithmetic in arrays, and repairs by a sort-and-scan over each light's orders and
reports. It reads only <task>/target and compares with generator/figures.json."""
import datetime as dt
import json
import os
import subprocess
import sys
import zoneinfo

import numpy as np
import pandas as pd
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import params as P   # noqa: E402  (file names, the as-of dates and the trigger only)


def digits(s):
    s = "" if s is None or (isinstance(s, float) and np.isnan(s)) else str(s)
    d = "".join(ch if ch.isdigit() else " " for ch in s).split()
    six = [x for x in d if len(x) == 6]
    return int(six[-1]) if six else None


def install(target):
    xl = pd.read_excel(os.path.join(target, P.FILES["install"]), sheet_name=None)
    parts = []
    for name, df in xl.items():
        if "Pole Tag" in df.columns:
            df = df.rename(columns={"Date": "date", "Phase": "phase", "Municipality": "town", "Pole Tag": "pole",
                                    "Catalog No.": "catalog", "Lot #": "lot", "Removed": "removed"})
            df["date"] = pd.to_datetime(df["date"]).dt.date
        else:
            df = df.rename(columns={"install_date": "date", "pole_id": "pole", "removed_fixture": "removed"})
            df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y").dt.date
        df["pole"] = df["pole"].map(digits)
        parts.append(df[["date", "phase", "town", "pole", "catalog", "lot", "removed"]])
    out = pd.concat(parts, ignore_index=True)
    out["watts"] = out["catalog"].str.extract(r"-(\d+)W-")[0].astype(int)
    return out.set_index("pole")


def makers(target):
    txt = subprocess.run(["pdftotext", "-raw", os.path.join(target, P.FILES["coc"]), "-"], capture_output=True,
                         text=True, check=True).stdout
    out = {}
    for page in txt.split("\f"):
        lines = [x.strip() for x in page.splitlines() if x.strip()]
        lot = next((x.split("Lot ")[1].rstrip(".") for x in lines if " Lot HL" in x), None)
        if not lot:
            continue
        drv = next(x for x in lines if x.startswith("LED driver"))
        out[lot] = "Vantrel" if "Vantrel" in drv else ("Corvane" if "Corvane" in drv else None)
    return out


def orders(target):
    lg = pd.read_csv(os.path.join(target, P.FILES["wo_legacy"]), dtype=str).fillna("")
    lg = pd.DataFrame(dict(pole=lg["LOCATION"].map(digits), res=lg["RES"],
                           opened=pd.to_datetime(lg["OPENED"], format="%m/%d/%Y %H:%M"),
                           done=pd.to_datetime(lg["CLOSED"], format="%m/%d/%Y %H:%M", errors="coerce"),
                           source="", parts="", sysname="legacy"))
    code = {"DRVR": "SL-DRV-RPL", "KD": "SL-KNOCKDOWN", "LUM": "SL-LUM-RPL", "REM": "SL-POLE-REM", "GLR": "SL-GLARE"}
    lg["activity"] = lg["res"].map(lambda x: code.get(x, "LEG-" + x))
    nw = pd.read_csv(os.path.join(target, P.FILES["wo_new"]), dtype=str).fillna("")
    wall = lambda s: pd.to_datetime(s.str[:16], format="%Y-%m-%dT%H:%M", errors="coerce")
    nw = pd.DataFrame(dict(pole=nw["asset_id"].map(digits), activity=nw["activity"],
                           opened=wall(nw["created_at"]), reported=wall(nw["reported_at"]),
                           done=wall(nw["completed_at"].where(nw["status"] == "CLOSED", "")),
                           source=nw["source"], parts=nw["parts"], sysname="eam"))
    return pd.concat([lg, nw], ignore_index=True)


def nll(x, t, d):
    k, lam = np.exp(x)
    z = (t / lam) ** k
    return -(np.sum(np.log(k) - np.log(lam) + (k - 1) * np.log(t / lam), where=d) - z.sum())


def fit(t, d):
    t = np.maximum(np.asarray(t, float), 1e-9)
    d = np.asarray(d, bool)
    best = None
    for k0, l0 in ((3.0, 10.0), (1.0, 500.0), (1.5, 50.0)):
        r = minimize(nll, [np.log(k0), np.log(l0)], args=(t, d), method="Nelder-Mead",
                     options={"xatol": 1e-12, "fatol": 1e-12, "maxiter": 20000})
        if best is None or r.fun < best.fun:
            best = r
    return np.exp(best.x)


WORDS = {"twelfth": 12.0, "tenth": 10.0, "fifteenth": 15.0}


def note(target):
    """The program test as the lifecycle note files it: the trigger, the horizon and the year length."""
    txt = " ".join(subprocess.run(["pdftotext", "-raw", os.path.join(target, P.FILES["note"]), "-"],
                                  capture_output=True, text=True, check=True).stdout.split())
    assert "two-parameter Weibull distribution, fitted by maximum likelihood" in txt, "the note's 3.1 not read"
    trig = float(txt.split(" per cent of those luminaires")[0].split("more than ")[-1]) / 100.0
    horizon = WORDS[txt.split(" anniversary of the luminaire")[0].split()[-1]]
    year = float(txt.split(" days a year")[0].split()[-1])
    return trig, horizon, year


def call(target):
    trig, horizon, year = note(target)
    ins = install(target)
    mk = makers(target)
    ins["maker"] = ins["lot"].map(mk)
    wo = orders(target)
    wo = wo[wo["pole"].isin(ins.index) & wo["done"].notna()]
    wo = wo[wo["done"].dt.date <= P.RECORD_END]
    wo = wo.join(ins[["date"]], on="pole")
    wo = wo[wo["done"].dt.date > wo["date"]]
    first_drv = wo[wo["activity"] == "SL-DRV-RPL"].groupby("pole")["done"].min().dt.date
    first_exit = wo[wo["activity"].isin(["SL-KNOCKDOWN", "SL-LUM-RPL", "SL-POLE-REM"])].groupby("pole")["done"].min().dt.date
    ins["fail"] = first_drv
    ins["exit"] = first_exit
    failed = ins["fail"].notna() & (ins["exit"].isna() | (ins["fail"] <= ins["exit"]))
    stop = np.where(failed, ins["fail"], ins["exit"].where(ins["exit"].notna(), P.RECORD_END))
    stop = [min(s, P.RECORD_END) if not f else s for s, f in zip(stop, failed)]
    ins["t"] = [(s - d0).days / year for s, d0 in zip(stop, ins["date"])]
    ins["d"] = failed
    ins["alive"] = (~failed) & ins["exit"].isna()
    ins["age"] = [(P.AS_OF - d0).days / year for d0 in ins["date"]]
    fits = {m: fit(g["t"], g["d"]) for m, g in ins.groupby("maker")}

    def p(row):
        k, lam = fits[row["maker"]]
        F = lambda x: 1 - np.exp(-(x / lam) ** k)
        return (F(horizon) - F(row["age"])) / (1 - F(row["age"]))
    al = ins[ins["alive"]].copy()
    al["p"] = al.apply(p, axis=1)
    shares = al.groupby("phase")["p"].mean()
    n = al.groupby("phase").size()
    ins.attrs["trigger"] = trig
    return shares, n, fits, ins


def energy(target, ins):
    tariff = subprocess.run(["pdftotext", "-layout", os.path.join(target, P.FILES["tariff"]), "-"],
                            capture_output=True, text=True, check=True).stdout
    watts = {}
    for line in tariff.splitlines():
        s = line.split()
        if len(s) > 4 and s[0] in ("LED", "HPS") and s[2] == "W":
            nums = [x for x in s[3:] if x.isdigit()]
            watts[(s[0], int(s[1]))] = int(nums[0])
        if s and s[0] == "Hours":
            hrs = [int(x.replace(",", "")) for x in s[1:13]]
    reg = pd.read_csv(os.path.join(target, P.FILES["register"]), dtype=str).fillna("")
    reg["pole"] = reg["pole_id"].map(digits)
    regw = dict(zip(reg["pole"], reg["lamp_watts"].astype(int)))
    wo = orders(target)
    wo = wo[wo["done"].notna() & wo["pole"].isin(ins.index)]
    nlc = pd.read_csv(os.path.join(target, P.FILES["nlc"]), dtype={"pole_id": str})
    nlc["pole"] = nlc["pole_id"].map(digits)
    nlc["m"] = nlc["month"].str[5:7].astype(int)
    nl = {(a, b): (c, e) for a, b, c, e in zip(nlc["pole"], nlc["m"], nlc["dimmed_hours"], nlc["dim_level_pct"])}
    days = pd.date_range("2026-01-01", "2026-12-31").date
    month = np.array([d.month for d in days])
    ndays = np.array([pd.Timestamp(d).days_in_month for d in days])
    perday = np.array([hrs[m - 1] for m in month]) / ndays
    out = {}
    for pole, g in wo.groupby("pole"):
        pass
    evs = {pole: g.sort_values("done") for pole, g in wo.groupby("pole")}
    for pole, r in ins.iterrows():
        hps = watts[("HPS", int(str(r["removed"]).split("W")[0].split()[-1]))]
        cur = np.full(len(days), watts[("LED", int(r["watts"]))], float)
        live = np.ones(len(days), bool)
        gone_before = False
        for _, e in (evs[pole].iterrows() if pole in evs else []):
            d = e["done"].date()
            if d <= r["date"]:
                continue
            ix = days >= d
            if e["activity"] == "SL-GLARE" and not e["parts"].startswith("HSS"):
                cur[ix] = watts[("LED", regw[pole])]
            elif e["activity"] in ("SL-KNOCKDOWN", "SL-LUM-RPL") and "HRX-" in e["parts"]:
                cur[ix] = watts[("LED", int(e["parts"].split("HRX-")[1].split("-")[1].rstrip("W")))]
            elif e["activity"] in ("SL-POLE-REM",):
                live &= ~ix
                if d < dt.date(2026, 1, 1):
                    gone_before = True
        if gone_before:
            continue
        tot = 0.0
        for m in range(1, 13):
            sel = (month == m) & live
            if not sel.any():
                continue
            tot += ((hps - cur[sel]) * perday[sel]).sum()
            if (pole, m) in nl:
                dh, lv = nl[(pole, m)]
                tot += cur[sel].mean() * (1 - lv / 100.0) * dh
        out[r["town"]] = out.get(r["town"], 0.0) + tot
    return {t: v / 1e6 for t, v in out.items()}


def repairs(target, ins):
    ny = zoneinfo.ZoneInfo("America/New_York")
    reg = pd.read_csv(os.path.join(target, P.FILES["register"]), dtype=str).fillna("")
    reg["pole"] = reg["pole_id"].map(digits)
    town = dict(zip(reg["pole"], reg["town"]))
    for pl, r in ins.iterrows():
        town.setdefault(pl, r["town"])
    feed = dict(zip(reg["pole"], reg["feed"]))
    members = reg[reg["feed"] != "OH"].groupby("feed")["pole"].apply(list).to_dict()
    byaddr = reg.groupby(["town", "nearest_address"])["pole"].apply(list).to_dict()
    rp = pd.read_csv(os.path.join(target, P.FILES["reports"]), dtype=str).fillna("")

    def when(row):
        if row["channel"] == "PORTAL":
            return pd.Timestamp(row["received"]).tz_convert(ny).tz_localize(None)
        return pd.to_datetime(row["received"][:19], format="%m/%d/%Y %I:%M %p")
    rp["t"] = rp.apply(when, axis=1)
    rp["pl"] = [digits(p) if digits(p) else (byaddr.get((tw, a), [None])[0] if len(byaddr.get((tw, a), [])) == 1
                                             else None) for p, tw, a in zip(rp["pole"], rp["town"], rp["address"])]
    rep = rp.dropna(subset=["pl"]).groupby("pl")["t"].apply(lambda s: sorted(s)).to_dict()
    wo = orders(target)
    wo = wo[(wo["sysname"] == "eam") & wo["done"].notna()].copy()
    out_codes = {"SL-DRV-RPL", "SL-PC-RPL", "SL-WIRING", "SL-FUSE-RPL", "SL-LAMP-RPL", "SL-BALLAST-RPL",
                 "SL-KNOCKDOWN", "SL-LUM-RPL", "SL-UG-CABLE"}
    wo["lights"] = [members.get(feed.get(p), [p]) if a == "SL-UG-CABLE" else [p]
                    for p, a in zip(wo["pole"], wo["activity"])]
    cov = {}
    for ls, d in zip(wo["lights"], wo["done"]):
        for p in ls:
            cov.setdefault(p, []).append(d)
    late, tot = {}, {}
    for _, w in wo[wo["activity"].isin(out_codes) & (wo["done"].dt.year == 2026)].iterrows():
        prev = max([d for p in w["lights"] for d in cov.get(p, []) if d < w["done"]], default=None)
        ts = [t for p in w["lights"] for t in rep.get(p, []) if (prev is None or t > prev) and t <= w["done"]]
        base = w["reported"] if w["source"].startswith("CR-") else w["opened"]
        first = min(ts + ([w["reported"]] if w["source"].startswith("CR-") else [])) if ts else base
        tw = town[w["pole"]]
        tot[tw] = tot.get(tw, 0) + 1
        late[tw] = late.get(tw, 0) + int((w["done"] - first).total_seconds() > 72 * 3600)
    return late, tot


def run(target, golden):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    shares, n, fits, ins = call(target)
    ok = True
    print("PASS  verify: the note read through its own extractor (trigger %.2f)" % ins.attrs["trigger"])
    sset = [pc for pc in P.PHASE_CODES if shares[pc] > ins.attrs["trigger"]]
    good = sset == fig["call"]["set"] and int(sum(n[pc] for pc in sset)) == fig["call"]["program_luminaires"]
    print("%s  verify: the set %s and %d luminaires" % ("PASS" if good else "FAIL", sset, sum(n[pc] for pc in sset)))
    ok &= good
    d = max(abs(shares[pc] - fig["phases"][pc]["share"]) for pc in P.PHASE_CODES)
    s5 = all(int(round(shares[pc] * 20) * 5) == fig["phases"][pc]["share5"] for pc in P.PHASE_CODES)
    print("%s  verify: every phase's share (largest gap %.2e) and its nearest 5 per cent" % (
        "PASS" if (d < 1e-4 and s5) else "FAIL", d))
    ok &= d < 1e-4 and s5
    E = energy(target, ins)
    gE = all(int(round(E[t])) == fig["towns"][t]["energy"] for t in fig["towns"])
    print("%s  verify: every town's MWh %s" % ("PASS" if gE else "FAIL", {t: round(v, 2) for t, v in sorted(E.items())}))
    ok &= gE
    late, tot = repairs(target, ins)
    gR = all(late[t] == fig["towns"][t]["late"] and tot[t] == fig["towns"][t]["repaired"] for t in fig["towns"])
    print("%s  verify: every town's late repairs %s" % ("PASS" if gR else "FAIL", dict(sorted(late.items()))))
    ok &= gR
    return ok


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    sys.exit(0 if run(t, None) else 1)
