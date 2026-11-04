"""Build task399: the world, the pack under target/, the goldens from the pack, figures.json, metadata.json and
target.zip. Usage: python3 build.py [--pack-only]"""
import json
import os
import shutil
import sys
import time
import zipfile

import docs
import ops as O
import pack as PK
import staffing as S
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = time.mktime((2026, 10, 9, 8, 52, 0, 0, 0, -1))
ZIP_TIME = (2026, 10, 9, 8, 52, 0)


def world():
    net = W.build_network()
    net["rmap"] = {rt["route_id"]: rt for rt in net["routes"]}
    staff = W.build_signallers()
    ros = S.build(staff)
    res = O.simulate(net, staff, ros)
    inc = res["incidents"]
    O.delays(inc, O.Trains(W.rng(30)))
    O.number_incidents(inc)
    moves = O.reviews(inc)
    O.investigate(inc)
    lab = PK.exit_line(net)
    O.register_fields(inc, net, lambda r, i: PK.narrative(r, i, net, lab, i["minutes"]))
    idx = S.on_duty_index(ros["spans"])
    periods, drops = O.ars(idx)
    fails = O.failovers()
    return dict(net=net, staff=staff, ros=ros, res=res, inc=inc, moves=moves, periods=periods, drops=drops,
                fails=fails)


def cut(target, S_):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    info = {}
    info["log_rows"] = PK.write_log(target, S_["res"]["events"], S_["fails"])
    PK.write_registers(target, S_["inc"], S_["net"])
    info["delay_rows"], info["review_rows"] = PK.write_delay(target, S_["inc"], S_["moves"])
    info["layout_objects"] = PK.write_layout(target, S_["net"])
    PK.write_rosters(target, S_["ros"], S_["staff"])
    info["changes_rows"] = PK.write_changes(target, S_["ros"])
    PK.write_competence(target, S_["staff"], S_["ros"])
    info["ars_rows"] = PK.write_ars(target, S_["periods"], S_["drops"], S_["fails"])
    info["adhesion_rows"] = PK.write_adhesion(target)
    docs.build(target, {k: PK.path(target, k) for k in ("tor", "catalogue", "workload")})
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
    S_ = world()
    info = cut(TARGET, S_)
    print("pack cut in %.0fs:" % (time.time() - t0), json.dumps(info))
    if "--pack-only" in sys.argv:
        return S_
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
    import checks
    if not checks.run(S_, TARGET, res).report():
        sys.exit("generator checks failed")
    n = archive(TARGET, os.path.join(TASK, "target.zip"))
    import writeup
    writeup.main()
    import verify
    if not verify.main(TARGET):
        sys.exit("independent verifier failed")
    print("built in %.0fs: call %s (%d minutes), zip members %d" % (time.time() - t0, F["call"], F["call_minutes"], n))
    return S_


if __name__ == "__main__":
    main()
