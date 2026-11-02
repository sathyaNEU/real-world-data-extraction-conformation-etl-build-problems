"""The ask sheet's cracker and mirror, run on the cut pack.  Shares no code with the generator: it reads target.zip
(or a target folder) with the standard library only and scores against generator/figures.json at the prompt's
rounding (dwellings exact, the winter inflow to 0.1 million m3, the winter load to the nearest 100 kg, concentrations
to 0.1 ug/l).

The cracker lands the call (programme C, every figure on the main side) and runs the hygiene battery on each ask
(supplemental-stumping 1.1c): the station's provisional hours taken only where no validated hour exists, its UK clock
moved to UTC with the repeated October hour kept, each hour's flow paired with the bottle that took that hour's
sub-sample (the storm bottles for the hours a day bottle skipped); one address counted once however many visits it
had, the fix cut at 30 September 2026 on the export's date; the north basin taken under the site code the recovery
plan files (NB) and its 0 to 5 m results.  It executes every filed statement it meets.  Nothing in the battery
compares the station's flow with the regulator's two gauges above the confluence, counts the flats behind a block's
address, reads the date inside a visit reference, or reads the laboratory's site codes against the depths each
carries.

The mirror stops at the most attractive wrong rung on the call (rung 1, the season's load budget, Brathwick) and
takes the same ask paths: no ask consumes anything the call's construction produces.

Weights 38 / 7 / 55; the ask weight spread over the nine ask figures; the mirror's main block 13 of 38 (it computes
the Hollinsby and Mill Beck figures right and files Brathwick).  Stress rows (not the gate) beside them.

    python3 task202/generator/ceiling.py [target_dir]
"""
import csv
import datetime as dt
import hashlib
import io
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CUT = dt.date(2026, 9, 30)


def half(x, nd=0):
    q = 10 ** nd
    return int(x * q + 0.5) / q


class Pack:
    def __init__(self, where):
        self.zip = None
        if where.endswith(".zip"):
            self.zip = zipfile.ZipFile(where)
            self.digest = hashlib.md5(open(where, "rb").read()).hexdigest()[:8]
        else:
            self.dir = where
            self.digest = "folder"

    def rows(self, fn):
        if self.zip:
            data = self.zip.read(fn).decode("utf-8")
        else:
            data = open(os.path.join(self.dir, fn), encoding="utf-8").read()
        return list(csv.DictReader(io.StringIO(data)))


def sunday(y, m):
    d = dt.date(y, m, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(1)
    return d


def utc(local, repeat=False):
    on = dt.datetime.combine(sunday(local.year, 3), dt.time(1))
    off = dt.datetime.combine(sunday(local.year, 10), dt.time(1))
    if local.date() == sunday(local.year, 10) and local.hour == 1:
        return local - dt.timedelta(hours=0 if repeat else 1)
    return local - dt.timedelta(hours=1 if on <= local < off else 0)


def station(P):
    out = {}
    for fn in ("lenning_foot_hourly_validated.csv", "lenning_foot_hourly_provisional.csv"):
        seen = set()
        for r in P.rows(fn):
            loc = dt.datetime.strptime(r["Timestamp (UK)"], "%d/%m/%Y %H:%M")
            u = utc(loc, loc in seen)
            seen.add(loc)
            out.setdefault(u, float(r["Flow (m3/s)"]))
    return out


def hourly_tp(P):
    conc = {}
    sam = P.rows("lenning_foot_sampler_results.csv")
    for kind in ("DAY", "STORM"):
        for r in sam:
            if r["Programme"] == kind:
                t = utc(dt.datetime.strptime(r["First sub-sample (UK)"], "%d/%m/%Y %H:%M"), True)
                e = utc(dt.datetime.strptime(r["Last sub-sample (UK)"], "%d/%m/%Y %H:%M"), True)
                while t <= e:
                    conc[t] = float(r["TP (ug/l)"])
                    t += dt.timedelta(hours=1)
    return conc


def winter(P, add_brankell):
    q = station(P)
    c = hourly_tp(P)
    sk = {}
    if add_brankell:
        for r in P.rows("regulator_gauged_flows_hourly.csv"):
            if r["station_name"] == "BRANKELL BECK AT HOWE":
                sk[dt.datetime.strptime(r["datetime"], "%Y-%m-%dT%H:%M:%SZ")] = float(r["mean_flow_m3s"])
    vol = load = 0.0
    t = dt.datetime(2023, 9, 30, 23)
    while t < dt.datetime(2024, 4, 30, 23):
        f = q[t] + (sk.get(t, 0.0) if t.date() < dt.date(2024, 6, 1) else 0.0)
        vol += f * 3600
        load += f * 3600 * c[t] / 1e6
        t += dt.timedelta(hours=1)
    return {"inflow_2023_24": half(vol / 1e6, 1), "load_2023_24": int(half(load / 100)) * 100}


def dwellings(P, expand, ref_date):
    kids = {}
    if expand:
        for r in P.rows("hollinsby_address_register_extract.csv"):
            if r["PARENT_UPRN"]:
                kids.setdefault(r["PARENT_UPRN"], []).append(r["UPRN"])
    found, fixed = set(), set()
    for v in P.rows("connect_right_visits_export.csv"):
        d = dt.datetime.strptime(v["Visit ref"][3:9], "%y%m%d").date() if ref_date else \
            dt.datetime.strptime(v["Uploaded"], "%d/%m/%Y").date()
        dw = kids.get(v["UPRN"], [v["UPRN"]])
        if v["Outcome"] == "MISCONNECTED":
            found.update(dw)
        elif v["Outcome"] == "FIX CONFIRMED" and d <= CUT:
            fixed.update(dw)
    fixed &= found
    return {"dw_found": len(found), "dw_fixed": len(fixed), "dw_open": len(found - fixed)}


def north_basin(P, reissue_read):
    out = {}
    lab = P.rows("fellside_lake_lab_results.csv")
    for y in (2025, 2026):
        acc = {"Total phosphorus": [], "Chlorophyll a": []}
        for r in lab:
            d = dt.datetime.strptime(r["sampled"], "%d-%b-%Y").date()
            if reissue_read:
                keep = r["site"] == "SWL01" or (r["site"] == "NB" and d < dt.date(2025, 4, 1))
            else:
                keep = r["site"] == "NB"
            if keep and d.year == y and 6 <= d.month <= 9 and r["depth_m"] == "0-5":
                acc[r["determinand"]].append(float(r["result"]))
        out["tp_%d" % y] = half(sum(acc["Total phosphorus"]) / len(acc["Total phosphorus"]), 1)
        out["chl_%d" % y] = half(sum(acc["Chlorophyll a"]) / len(acc["Chlorophyll a"]), 1)
    return out


ASKS = [("A1 winter inflow and load", ("inflow_2023_24", "load_2023_24")),
        ("A2 north basin phosphorus and chlorophyll", ("tp_2025", "chl_2025", "tp_2026", "chl_2026")),
        ("A3 Connect Right dwellings", ("dw_found", "dw_fixed", "dw_open"))]


def score(route, gold):
    return {k: route[k] == gold[k] for k in route}


def main(argv):
    where = argv[1] if len(argv) > 1 else os.path.join(TASK, "target.zip")
    P = Pack(where)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    gold = {k: fig[k] for _, ks in ASKS for k in ks}
    crack = {}
    crack.update(winter(P, add_brankell=False))
    crack.update(north_basin(P, reissue_read=False))
    crack.update(dwellings(P, expand=False, ref_date=False))
    hits = score(crack, gold)
    n_ask = sum(len(ks) for _, ks in ASKS)
    print("pack %s" % P.digest)
    print("| Ask | Cracker figures | Golden | Verdict |")
    for name, ks in ASKS:
        kept = [k for k in ks if hits[k]]
        print("| %s | %s | %s | %s |" % (name, ", ".join("%s %s" % (k, crack[k]) for k in ks),
                                          ", ".join(str(gold[k]) for k in ks), "keeps " + ",".join(kept) if kept else "miss"))
    kept = sum(hits.values())
    cr = 38 + 7 + 55.0 * kept / n_ask
    mi = 13 + 7 + 55.0 * kept / n_ask
    print("cracker keeps %d of %d ask figures: %.1f; mirror %.1f; pair ceiling %.1f; mirror leakage %.1f per cent"
          % (kept, n_ask, cr, mi, (cr + mi) / 2, 100.0 * kept / n_ask))
    stress = [("adds the Brankell Beck (compares the station with both gauges)", winter(P, add_brankell=True)),
              ("counts the flats, dates by upload", dwellings(P, expand=True, ref_date=False)),
              ("counts the flats, dates by the visit reference", dwellings(P, expand=True, ref_date=True)),
              ("addresses only, dates by the visit reference", dwellings(P, expand=False, ref_date=True)),
              ("reads the site codes against their depths", north_basin(P, reissue_read=True))]
    full = 0
    for name, r in stress:
        s = score(r, gold)
        print("stress: %-58s keeps %d of %d (%s)" % (name, sum(s.values()), len(s), ", ".join("%s %s" % kv for kv in r.items())))
    full_inc = {}
    full_inc.update(winter(P, True))
    full_inc.update(north_basin(P, True))
    full_inc.update(dwellings(P, True, True))
    fk = sum(score(full_inc, gold).values())
    print("stress: the full includer keeps %d of %d (pair %.1f with a second full includer off the call)"
          % (fk, n_ask, (38 + 7 + 55.0 * fk / n_ask + 13 + 7 + 55.0 * fk / n_ask) / 2))
    return 0 if kept == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
