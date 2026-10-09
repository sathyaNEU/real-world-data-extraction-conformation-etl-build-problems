#!/usr/bin/env python3
"""Build task123 twice into scratch, assert the two outputs are byte-identical, build into the task
folder, run the independent verifier there, and assert the generator and the verifier agree on every
graded figure (A52).

    python3 ship.py --task /path/to/task123 --scratch /path/to/scratch
"""
import argparse
import filecmp
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
            out[os.path.relpath(p, root)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit(f"failed: {' '.join(cmd)}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    gen = os.path.join(HERE, "build.py")
    ver = os.path.join(HERE, "verify.py")
    builds = []
    for k in ("build_a", "build_b"):
        d = os.path.join(a.scratch, k)
        if os.path.isdir(d):
            shutil.rmtree(d)
        os.makedirs(d)
        print(run([sys.executable, gen, "--out", d, "--record", d + "_record.json"]).strip().splitlines()[0])
        builds.append(d)
    da, db = digest_tree(builds[0]), digest_tree(builds[1])
    assert da == db, "two consecutive builds differ"
    print(f"A52: two consecutive builds byte-identical ({len(da)} files)")
    # the build that ships
    print(run([sys.executable, gen, "--out", a.task, "--record", os.path.join(a.scratch, "task_record.json")]).strip())
    dt_ = digest_tree(os.path.join(a.task, "target"))
    assert dt_ == {k[len("target/"):]: v for k, v in da.items() if k.startswith("target/")}, \
        "the shipped pack differs from the scratch builds"
    print("A52: the shipped pack is byte-identical to both scratch builds")
    vjson = os.path.join(a.scratch, "task_verify.json")
    print(run([sys.executable, "-I", ver, a.task, "--json", vjson]).strip())
    g = json.load(open(os.path.join(a.scratch, "task_record.json")))
    v = json.load(open(vjson))
    assert g["rate_hc"] == round(v["golden"]["rate_cents"] * 100), "rate disagrees"
    vrows = {r["cc"]: r for r in v["golden"]["screen"]}
    assert len(vrows) == len(g["rows"]) == g["scored"]
    n = 0
    from decimal import Decimal, ROUND_HALF_UP
    for r in g["rows"]:
        x = vrows[r["cc"]]
        p1 = float(Decimal(repr(r["pct"])).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))
        same = (r["cur"], r["prior"], r["fall"], r["offer"], r["K1"], r["K2"]) == \
            (x["cur"], x["prior"], x["fall"], x["offer"], x["K1"], x["K2"])
        assert same and abs(p1 - x["pct"]) < 1e-9, (r["cc"], r, x)
        n += 7
    for y, c in g["corpus"].items():
        assert v["corpus"][y]["rate"] == c["rate_hc"] and v["corpus"][y]["rows"] == c["rows"]
        n += 2
    for k, m in g["rivals"].items():
        key = {"V1 overdue only": "V1", "V2 December balance dates": "V2", "V3 Q4 amended after census": "V3",
               "V4 current window only": "V4", "V5 unfiled left unscored": "V5",
               "T-strict census day exclusive": "T-strict", "T-extract register at 7 Oct": "T-extract",
               "fallback register Q4 else management": "fallback"}.get(k, k)
        assert v["rivals"][key]["rows"] == m["rows"], (k, m, v["rivals"][key])
        n += 1
    for k in ("R0", "R1", "R2", "R3", "R4"):
        assert v["september"]["rungs"][k] == g["rungs"][k]["rate_hc"], k
        n += 1
    cell_names = {"per return, as held, step-back": "dual twice", "per organisation, latest, step-back": "latest",
                  "per return, latest, step-back": "dual twice, latest",
                  "30-June grantees not stepped back": "30 June unstepped",
                  "only 30-June grantees stepped back": "only 30 June stepped",
                  "current window stepped back, prior not": "prior natural",
                  "register read as at the extract": "register at extract",
                  "census day exclusive": "census exclusive", "4.1 read strictly (after, not on)": "4.1 strict",
                  "4.1 against the census a year before": "4.1 a year before",
                  "R4, per return, as held": "R4 dual twice", "R4, latest versions": "R4 latest",
                  "register fallback, no step-back": "fallback", "overdue only": "overdue"}
    for gk, vk in cell_names.items():
        assert v["september"]["cells"][vk] == g["cells"][gk], (gk, v["september"]["cells"][vk], g["cells"][gk])
        n += 1
    print(f"A52: generator and verifier agree on {n} figures (every scored row, offer, K1, K2, rate, "
          f"corpus round, rival, rung and grid cell)")


if __name__ == "__main__":
    main()
