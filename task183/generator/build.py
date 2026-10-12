"""Build task183: the evidence pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task183/generator/build.py              everything
    python3 task183/generator/build.py --out DIR    the pack only, into DIR"""
import argparse
import datetime as dt
import hashlib
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cable as C          # noqa: E402
import docs as D           # noqa: E402
import grid as G           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "wo": R.WO, "register": R.REGISTER, "codes": R.CODES, "oms": R.OMS, "steps": R.STEPS, "conn": R.CONN,
    "devices": R.DEVICES, "cis": R.CIS, "med": R.MED, "standard": D.STANDARD, "report": D.REPORT, "notes": D.NOTES,
    "vaults": R.VAULTS, "loading": R.LOADING,
}
DISTRACTORS = ("vaults", "loading")
HISTORY_FROM = dt.date(2015, 10, 1)       # outage history kept for the published major event day thresholds
# outages the district's year needed: a transformer bank outage at each substation in the asked year, and the
# evening of 30 September 2026
FORCED = [
    (dt.date(2025, 11, 18), "bank", "MLN", 9.6), (dt.date(2026, 2, 26), "bank", "HRD", 14.2),
    (dt.date(2026, 5, 6), "bank", "QHL", 11.4), (dt.date(2026, 8, 19), "bank", "SPK", 16.8),
    (dt.date(2026, 9, 30), "fuse", "ML07", 21.3), (dt.date(2026, 9, 30), "fuse", "SP05", 22.6),
    (dt.date(2026, 9, 30), "branch", "HR14", 20.9),
    # the Mill Lane lateral's own fuse, before and after the June 2026 transfer
    (dt.date(2025, 12, 3), "lateral", "ML03", 15.7), (dt.date(2026, 3, 2), "lateral", "ML03", 8.4),
    (dt.date(2026, 7, 9), "lateral", "ML07", 17.2), (dt.date(2026, 9, 2), "lateral", "ML07", 13.9),
    # a Quarry Hill 22 lateral that kept blowing its fuse, and a Sutter Park 9 branch lockout
    (dt.date(2025, 12, 9), "pocket", "QH22", 6.8), (dt.date(2026, 4, 22), "pocket", "QH22", 19.1),
    (dt.date(2026, 8, 27), "pocket", "QH22", 14.6), (dt.date(2026, 2, 11), "branch", "SP09", 7.9),
    (dt.date(2025, 10, 23), "pocket", "HR12", 16.4), (dt.date(2026, 1, 14), "pocket", "HR12", 11.2),
    (dt.date(2026, 6, 24), "pocket", "HR12", 18.5), (dt.date(2025, 11, 3), "pocket", "SP09", 13.3),
    (dt.date(2026, 3, 30), "pocket", "SP09", 16.7), (dt.date(2026, 6, 2), "pocket", "SP09", 9.1),
    # ordinary lateral fuse operations of the year
    (dt.date(2025, 11, 14), "fuse", "ML03", 15.55), (dt.date(2025, 11, 6), "fuse", "QH22", 9.6),
    (dt.date(2025, 10, 25), "fuse", "SP05", 15.55), (dt.date(2025, 10, 27), "fuse", "HR12", 16.2),
    (dt.date(2025, 10, 20), "fuse", "SP09", 15.55),
]


def simulate():
    secs, _ = C.build()
    others = C.other_events(secs)
    wo = R.work_orders(secs, others)
    topo = G.topology()
    ev = [(dt.date.fromisoformat(r["fault_date"]), r["feeder_id"], r["cause_code"]) for r in wo
          if r["cause_code"] in ("INS", "SPL", "TRM", "TPD") and dt.date.fromisoformat(r["fault_date"]) >= HISTORY_FROM]
    outs = G.outages(topo, ev, d0=HISTORY_FROM, forced=FORCED)
    snap = R.Snap(topo.devices, topo.meter_rows)
    oms, steps = R.oms_tables(snap, outs, ship_from=W.OMS_START)
    med = published_meds(snap, outs, topo)
    return dict(secs=secs, others=others, wo=wo, topo=topo, outs=outs, snap=snap, oms=oms, steps=steps, med=med)


def published_meds(snap, outs, topo):
    """The published major event days for RY2021 to RY2025, each year's threshold from its own five prior years
    (the outage history before October 2020 is held by Reliability Engineering and is not in the extract)."""
    import math
    import numpy as np
    cm, biggest = {}, {}
    for o in outs:
        res = o.get("res") or R.restorations(snap, o)
        o["res"] = res
        day = o["start"].astimezone(W.LOCAL).date()
        tot = 0.0
        for _, _, t, _ in res:
            mins = (t - o["start"]).total_seconds() / 60
            if mins > 5:
                cm[day] = cm.get(day, 0.0) + mins
                tot += mins
        if tot > biggest.get(day, (0.0, ""))[0]:
            biggest[day] = (tot, o["cause"], snap.devices[o["device"]]["type"])
    served = {}

    def base(y):
        if y not in served:
            d = dt.date(y, 9, 30)
            served[y] = len({r["meter_id"] for r in topo.meter_rows if r["eff_from"] <= d and (r["eff_to"] is None or d < r["eff_to"])})
        return served[y]

    def daily(y):
        lo, hi = dt.date(y - 1, 10, 1), dt.date(y, 9, 30)
        out, d = {}, lo
        while d <= hi:
            out[d] = cm.get(d, 0.0) / base(y)
            d += dt.timedelta(days=1)
        return out
    storms = G.storm_days()
    names = {dt.date(2020, 11, 15): "Wind storm", dt.date(2021, 6, 30): "Thunderstorms",
             dt.date(2021, 9, 1): "Remnants of Hurricane Ida", dt.date(2022, 2, 4): "Ice and freezing rain",
             dt.date(2022, 7, 21): "Thunderstorms", dt.date(2023, 4, 1): "Wind storm",
             dt.date(2023, 8, 8): "Thunderstorms", dt.date(2024, 1, 10): "Wind and rain storm",
             dt.date(2024, 7, 16): "Thunderstorms", dt.date(2025, 2, 16): "Ice storm", dt.date(2025, 6, 19): "Thunderstorms"}
    rows = []
    for y in range(2021, 2026):
        prior = {}
        for p in range(y - 5, y):
            prior.update(daily(p))
        v = np.log(np.array([x for x in prior.values() if x > 0]))
        T = math.exp(v.mean() + 2.5 * v.std(ddof=1))
        for d, s in sorted(daily(y).items()):
            if s > T:
                _, cause, dtype = biggest[d]
                other = ("Substation transformer outage" if dtype == "TRANSFORMER BANK" else
                         "Feeder lockout" if dtype == "FEEDER BREAKER" else "Multiple lateral outages")
                rows.append(dict(reliability_year="RY%d" % y, med_date=d.isoformat(), tmed_saidi_min="%.2f" % T,
                                 event=names.get(d, "Storm" if d in storms else other)))
    return rows


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    p = lambda k: os.path.join(out, FILES[k])
    w = world or simulate()
    counts = {}
    counts["wo"] = R.write_wo(p("wo"), w["wo"])
    counts["register"] = R.write_register(p("register"), R.register_rows(w["secs"]))
    counts["codes"] = R.write_codes(p("codes"))
    counts["oms"] = R.write_csv(p("oms"), w["oms"], R.OMS_COLS)
    counts["steps"] = R.write_csv(p("steps"), w["steps"], R.STEP_COLS)
    counts["conn"] = R.write_connectivity(p("conn"), w["topo"])
    counts["devices"] = R.write_devices(p("devices"), w["topo"])
    counts["cis"] = R.write_cis(p("cis"), R.cis_rows(w["topo"]))
    counts["med"] = R.write_med(p("med"), w["med"])
    counts["vaults"] = R.write_vaults(p("vaults"), R.vault_rows(w["secs"]))
    counts["loading"] = R.write_loading(p("loading"))
    D.write_standard(p("standard"))
    D.write_report(p("report"), *report_tables(w))
    D.write_notes(p("notes"), counts)
    PP.normalize_ooxml(p("register"), W.PEOPLE["gis"], W.PEOPLE["gis"], "2016-05-11T13:02:44Z", "2026-10-01T06:15:09Z",
                       excel=True)
    PP.normalize_ooxml(p("loading"), W.PEOPLE["reliability"], W.PEOPLE["reliability"], "2021-02-08T15:40:21Z",
                       "2026-10-05T19:22:37Z", excel=True)
    PP.normalize_pdf(p("standard"), b"D:20231204091522-05'00'", b"D:20231211143005-05'00'")
    PP.normalize_pdf(p("report"), b"D:20260424101410-04'00'", b"D:20260429163852-04'00'")
    stamp = dt.datetime(2026, 10, 6, 15, 40, tzinfo=W.LOCAL).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    w["counts"] = counts
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in counts.items())))
    return w


def report_tables(w):
    years = [2021, 2022, 2023, 2024, 2025]
    failures = {f: {y: 0 for y in years} for f in W.FEEDERS}
    for r in w["wo"]:
        y = int(r["fault_date"][:4])
        if y in years and r["cause_code"] in ("INS", "SPL", "TRM"):
            failures[r["feeder_id"]][y] += 1
    miles = {f: {y: 0.0 for y in years} for f in W.FEEDERS}
    for s in w["secs"]:
        for y in years:
            d = dt.date(y, 12, 31)
            if s.installed <= d and (s.retired is None or s.retired > d):
                ln = R.plat_length(s) if d < R.REMEASURE[s.feeder] else s.length
                miles[R.feeder_at(s, d)][y] += ln / 5280.0
    customers = {f: {y: 0 for y in years} for f in W.FEEDERS}
    for y in years:
        d = dt.date(y, 12, 31)
        seen = set()
        for r in w["topo"].meter_rows:
            if r["eff_from"] <= d and (r["eff_to"] is None or d < r["eff_to"]) and r["meter_id"] not in seen:
                seen.add(r["meter_id"])
                customers[r["feeder_id"]][y] += 1
    return failures, miles, customers


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = dt.datetime.combine(W.EXTRACT_DAY, dt.time(15, 42, 6)).timetuple()[:6]
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    DL.main(os.path.join(root, "target"), os.path.join(root, "golden"), os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import checks as CK
    import verify as V
    world = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
           meta_path=os.path.join(TASK, "metadata.json"))
    V.main(os.path.join(TASK, "target"), os.path.join(TASK, "golden"))
    tmp = tempfile.mkdtemp(dir=TASK, suffix=".tmp")
    try:
        os.makedirs(os.path.join(tmp, "generator"))
        everything(tmp, quiet=True)
        same_t = digest(os.path.join(TASK, "target")) == digest(os.path.join(tmp, "target"))
        same_g = digest(os.path.join(TASK, "golden")) == digest(os.path.join(tmp, "golden"))
        same = {}
        for f in ("metadata.json", os.path.join("generator", "figures.json")):
            same[f] = open(os.path.join(TASK, f), "rb").read() == open(os.path.join(tmp, f), "rb").read()
        if not (same_t and same_g and all(same.values())):
            raise SystemExit("second build differs: target %s, golden %s, %s" % (same_t, same_g, same))
    finally:
        shutil.rmtree(tmp)
    allh = hashlib.sha256("".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode()).hexdigest()
    print("two builds byte-identical: %d target files, %d golden files, metadata.json and figures.json (sha256 %s)" % (
        len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))), allh[:16]))
    import zipfile
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)" % (
        len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
