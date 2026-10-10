#!/usr/bin/env python3
"""Build task130 twice into scratch, assert the two outputs are byte-identical, build into the task
folder, run the independent verifier there, and assert the generator and the verifier agree on every
graded figure.

    python3 ship.py --task /path/to/task130 --scratch /path/to/scratch
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


def digest_tree(root):
    out = {}
    for d, _, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = (hashlib.sha256(open(p, "rb").read()).hexdigest(), int(os.path.getmtime(p)))
    return out


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit(f"failed: {' '.join(cmd)}")
    return r.stdout.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    gen, ver = os.path.join(HERE, "build.py"), os.path.join(HERE, "verify.py")
    outs = []
    for k in ("build_a", "build_b"):
        d = os.path.join(a.scratch, k)
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
        print(k, run([sys.executable, gen, "--out", d, "--record", d + "_record.json"]))
        outs.append(d)
    da, db = digest_tree(outs[0]), digest_tree(outs[1])
    assert da == db, sorted(k for k in da if da.get(k) != db.get(k))
    print(f"two consecutive builds byte-identical, mtimes included ({len(da)} files)")
    print("task", run([sys.executable, gen, "--out", a.task, "--record", os.path.join(a.scratch, "task_record.json")]))
    dt_ = digest_tree(os.path.join(a.task, "target"))
    assert dt_ == {k[len("target/"):]: v for k, v in da.items() if k.startswith("target/")}, "task build differs"
    assert open(os.path.join(a.task, "metadata.json"), "rb").read() == open(os.path.join(outs[0], "metadata.json"), "rb").read()
    print("the task folder's pack and metadata.json are byte-identical to both scratch builds")
    vj = os.path.join(a.scratch, "task_verify.json")
    print(run([sys.executable, "-I", ver, a.task, "--json", vj]))
    g = json.load(open(os.path.join(a.scratch, "task_record.json")))
    v = json.load(open(vj))
    n = 0
    assert sorted(g["answer"]) == sorted(v["answer"]), "answer"
    n += 1
    for s, x in g["golden"].items():
        y = v["golden"][s]
        assert (x["lh"], x["share"], x["group"], x["group_n"], x["empty"]) == \
            (y["lh"], y["share"], y["group"], y["group_n"], y["empty"]), (s, x, y)
        n += 5
    for m, counts in g["rungs"].items():
        assert counts == v["counts"][m], m
        n += 14
    gn, vn = g["nearest"], v["nearest"]
    role = {s: x["role"] for s, x in g["golden"].items()}
    for k in ("designated", "undesignated"):
        assert gn[k][0] == role[vn[k][0]] and gn[k][1:] == vn[k][1:], (k, gn[k], vn[k])
        n += 3
    for s, (start, steps) in v["bridge"].items():
        assert g["bridge"][role[s]] == [start, steps], (s, g["bridge"], v["bridge"])
        n += 7
    assert g["calibration"]["settled"] == v["settled"] and g["calibration"]["backtest"] == v["backtest"]
    n += 2
    for s, c in v["annex2026"].items():
        assert int(g["annex26"][s][1]) == c, s
        n += 1
    print(f"generator and verifier agree on {n} figures (answer, 14 annex rows x 5 columns, 7 rungs x 14 sections, "
          f"both nearest sections, both bridges, the corpus counts and the 2026 close-out)")


if __name__ == "__main__":
    main()
