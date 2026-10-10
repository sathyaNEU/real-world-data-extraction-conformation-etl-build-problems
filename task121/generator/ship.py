#!/usr/bin/env python3
"""Build task121 twice into scratch, assert the two outputs are byte-identical, build into the task
folder, assert it matches the scratch builds, run the independent verifier on the shipped bytes and
assert the generator and the verifier agree on every graded figure.

    python3 ship.py --task <task121 dir> --scratch <scratch dir>
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
FIX = {"P1": "F1", "P2": "F2", "P3": "F3", "P4": "F4", "P5": "F5"}


def digest(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stdout[-3000:] + r.stderr[-3000:])
        raise SystemExit("failed: " + " ".join(cmd))
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    gen = os.path.join(HERE, "build.py")
    dg = []
    for k in ("build_a", "build_b"):
        d = os.path.join(a.scratch, k)
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
        print(k, run([sys.executable, gen, "--out", d, "--record", d + "_record.json"]))
        dg.append(digest(d))
    assert dg[0] == dg[1], [k for k in dg[0] if dg[0].get(k) != dg[1].get(k)]
    print(f"two consecutive builds byte-identical ({len(dg[0])} files including metadata.json)")
    rec = os.path.join(a.scratch, "task_record.json")
    print("task", run([sys.executable, gen, "--out", a.task, "--record", rec]))
    shipped = digest(os.path.join(a.task, "target"))
    assert shipped == {k[len("target/"):]: v for k, v in dg[0].items() if k.startswith("target/")}, \
        "the shipped pack differs from the scratch builds"
    m0 = hashlib.sha256(open(os.path.join(a.task, "metadata.json"), "rb").read()).hexdigest()
    assert m0 == dg[0]["metadata.json"], "metadata.json differs from the scratch builds"
    print("the task folder's target/ and metadata.json are byte-identical to both scratch builds")
    vj = os.path.join(a.scratch, "task_verify.json")
    print(run([sys.executable, "-I", os.path.join(HERE, "verify_pack.py"), a.task, "--json", vj]))
    g = json.load(open(rec))
    v = json.load(open(vj))
    n = 0
    assert g["call"] == v["call"] and g["runner_up"] == v["runner_up"]
    for k in ("call_w4", "runner_up_w4", "gap"):
        assert abs(g[k] - v[k]) < 1e-6, k
        n += 1
    for blk in ("L1", "L2", "L3", "L4"):
        for p, f in FIX.items():
            assert abs(g[blk][p] - v[blk][f]) < 1e-6, (blk, p, g[blk][p], v[blk][f])
            n += 1
    for c, (cn, cv) in g["cohorts"].items():
        vn, vv = v["cohorts"][c]
        assert cn == vn and abs(cv - vv) < 1e-9, c
        n += 2
    for p, f in FIX.items():
        for w, x in g["chart"][f].items():
            assert abs(x - v["weekly"][f][w]) < 1e-3, (f, w)
            n += 1
    for r, d in g["ladder"].items():
        if isinstance(d, dict) and "figures" in d:
            for f, x in d["figures"].items():
                assert abs(x - v["rungs"][r]["figures"][f]) < 0.01, (r, f, x, v["rungs"][r]["figures"][f])
                n += 1
            assert d["leader"] == v["rungs"][r]["leader"]
    assert abs(g["calibration"]["twin"]["loss"][0] - v["twins"]["6"]) < 0.01
    assert abs(g["calibration"]["twin"]["loss"][1] - v["twins"]["8"]) < 0.01
    n += 2
    for k, gk in (("closeout_festival", "margens"), ("closeout_kaiju", "kaiju")):
        for q in ("visitor_type", "store_rate", "all_new"):
            assert abs(g["calibration"][gk][q] - v["killers"]["R1_closeouts"][k][q]) < 0.01, (k, q)
            n += 1
    for k, e in v["releases"].items():
        assert abs(g["calibration"][k]["cohort"] - e["cohort"]) < 1e-3 and abs(g["calibration"][k]["calendar"] - e["calendar"]) < 1e-3
        n += 2
    print(f"generator and verifier agree on {n} figures; generator assertions: {g['assertions']}")


if __name__ == "__main__":
    main()
