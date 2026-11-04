"""Build task398: the world, the pack under target/, the goldens from the pack, figures.json, metadata.json and
target.zip. Usage: python3 build.py [--pack-only]"""
import json
import os
import shutil
import sys
import time
import zipfile

import numpy as np

import docs
import pack as PK
import plant as PL
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = time.mktime((2026, 11, 2, 8, 14, 0, 0, 0, -1))
ZIP_TIME = (2026, 11, 2, 8, 14, 0)


def world():
    Wd = W.build()
    rng = np.random.default_rng(W.SEED + 20)
    res = PL.results(rng, Wd["rec"])
    mgd = PL.flows(rng, Wd["rec"])
    setpoints, events, lb_day, downtime = PL.carbon(np.random.default_rng(W.SEED + 106), res, mgd)
    alarms = PL.alarm_history(np.random.default_rng(W.SEED + 22), events, res, setpoints)
    return dict(W=Wd, res=res, mgd=mgd, setpoints=setpoints, events=events, lb_day=lb_day, downtime=downtime,
                alarms=alarms)


def cut(target, S):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    Wd = S["W"]
    info = {}
    rng = np.random.default_rng(W.SEED + 30)
    PK.storm_starts(Wd["ST"], rng)
    q15, t15, c15 = {}, {}, {}
    for n, k in enumerate(W.SUBS):
        q15[k], t15[k], c15[k] = PK.series15(Wd, k, np.random.default_rng(W.SEED + 40 + n))
    S["q15"], S["t15"], S["c15"] = q15, t15, c15
    for n, (key, k) in enumerate((("tr01", "TES"), ("fc02", "FEN"), ("oc03", "OXL"))):
        info[key] = PK.write_station(target, key, k, q15[k], t15[k], np.random.default_rng(W.SEED + 50 + 100 * n))
    for n, (key, k) in enumerate((("dc04", "DUN"), ("lb05", "LAD"))):
        info[key] = PK.write_logger(target, key, k, q15[k], t15[k], np.random.default_rng(W.SEED + 51 + 100 * n))
    visits = PK.field_visits(Wd, q15, np.random.default_rng(W.SEED + 52))
    PK.write_ratings(target, rng, visits)
    bottles = PK.sampling(Wd, c15, np.random.default_rng(W.SEED + 53))
    bottles = PK.lab_results(bottles, np.random.default_rng(W.SEED + 54))
    S["bottles"] = bottles
    PK.write_field_log(target, bottles, t15, np.random.default_rng(W.SEED + 55))
    info["isco"] = PK.write_isco(target, Wd["isco_runs"], np.random.default_rng(W.SEED + 67))
    info["shl"] = PK.write_shl(target, bottles, np.random.default_rng(W.SEED + 56))
    PK.write_city(target, bottles, np.random.default_rng(W.SEED + 57))
    info["lims_old"] = PK.write_lims_old(target, S["res"], np.random.default_rng(W.SEED + 58))
    PK.write_lims_new(target, S["res"], np.random.default_rng(W.SEED + 59))
    PK.write_ops(target, S["mgd"], Wd, np.random.default_rng(W.SEED + 60))
    info["pac_sp"] = PK.write_pac_setpoints(target, S["setpoints"], np.random.default_rng(W.SEED + 61))
    info["alarms"] = PK.write_alarms(target, S["alarms"])
    info["buoy"] = PK.write_buoy(target, np.random.default_rng(W.SEED + 62))
    PK.write_buoy_log(target)
    S["dam_elev"] = PK.write_dam(target, Wd["rec"], Wd["rain"], np.random.default_rng(W.SEED + 63))
    PK.write_acap(target)
    PK.write_rain(target, Wd["rain"])
    PK.write_survey(target, np.random.default_rng(W.SEED + 64))
    PK.write_nitrate(target, bottles, np.random.default_rng(W.SEED + 65))
    PK.write_beach(target, np.random.default_rng(W.SEED + 66))
    docs.build(target, {k: PK.path(target, k) for k in ("plan", "sop", "drawing")})
    for root, dirs, files in os.walk(target):
        for fn in files + dirs:
            os.utime(os.path.join(root, fn), (STAMP, STAMP))
    os.utime(target, (STAMP, STAMP))
    return info


def archive(target, out):
    names = []
    for root, dirs, files in os.walk(target):
        for f in files:
            p = os.path.join(root, f)
            names.append((os.path.relpath(p, target).replace(os.sep, "/"), p))
    names.sort()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, p in names:
            info = zipfile.ZipInfo(arc, date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(p, "rb") as fh:
                z.writestr(info, fh.read())
    return len(names)


def main():
    t0 = time.time()
    S = world()
    info = cut(TARGET, S)
    print("pack cut in %.0fs:" % (time.time() - t0), json.dumps(info))
    if "--pack-only" in sys.argv:
        return S
    import golden as G
    import deliver
    res = G.compute(TARGET)
    if os.path.isdir(GOLDEN):
        shutil.rmtree(GOLDEN)
    os.makedirs(GOLDEN)
    F = deliver.write(res, GOLDEN)
    for fn in os.listdir(GOLDEN):
        os.utime(os.path.join(GOLDEN, fn), (STAMP, STAMP))
    F["pack"] = info
    json.dump(F, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, default=str)
    import meta
    json.dump(meta.metadata(), open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    n = archive(TARGET, os.path.join(TASK, "target.zip"))
    import writeup
    writeup.main()
    print("built in %.0fs: call %s (%d days), zip members %d" % (time.time() - t0, F["call"], F["call_days"], n))
    return S


if __name__ == "__main__":
    main()
