"""Build task451: the pack into <task>/target (data first, then Schedule B with each partner's 2026 target placed from
the completed cost the data give), the goldens into <task>/golden, metadata.json and generator/figures.json; then the
checks and the independent verifier, a second full build into a scratch folder inside the task compared byte for byte,
and target.zip cut from the final build.

    python3 task451/generator/build.py              everything
    python3 task451/generator/build.py --out DIR    the pack only, into DIR
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import calc as C            # noqa: E402
import docs as DC           # noqa: E402
import pack as P            # noqa: E402
import postprocess as PP    # noqa: E402
import sim as S             # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
EASTERN = dt.timezone(dt.timedelta(hours=-5))
STAMP = dt.datetime(2027, 2, 3, 14, 18, tzinfo=EASTERN)       # the folder as the Fund Office shared it


GOLD_ROUTES = ("G1 received, all development", "G2 received, latest 12 months", "G3 paid, after the go-live month",
               "G4 received, by claim type", "G5 paid (latest versions), after the go-live month")


def place_targets(target):
    """each partner's Target PMPM from the shipped data: x = golden (G1) TCOC PMPM over 1.02 times the target, fixed
    for the owe and clear roles, and for the banded roles the geometric middle of the band its role names, measured
    on every route's TCOC PMPM for that partner"""
    X = C.compute(target)
    P_ = X["pmpm"]
    g = P_["G1 received, all development"]
    b = {nm: {c: v[c] / g[c] for c in W.CODES} for nm, v in P_.items()}
    x = {}
    for c in W.CODES:
        role = W.ROLE[c]
        gold_hi = max(b[r][c] for r in GOLD_ROUTES)
        gold_lo = min(b[r][c] for r in GOLD_ROUTES)
        if role in ("owe", "clear"):
            x[c] = W.PLACE[c]
        elif role == "owe_r1":       # every golden route flags (x > 1 / gold_lo), paid-as-extracted does not
            lo, hi = 1 / gold_lo, 1 / b["R1 paid as extracted"][c]
            x[c] = (lo * hi) ** 0.5
        elif role == "band_l4":      # no golden route flags (x < 1 / gold_hi), the four-month paid ladder does
            lo, hi = 1 / b["paid, latest 4 months"][c], 1 / gold_hi
            x[c] = (lo * hi) ** 0.5
        elif role == "band_r0":      # the twelve-month and all-history paid ladders flag, the six-month does not
            lo = 1 / min(b["R0 paid, all development"][c], b["paid, latest 12 months"][c])
            hi = 1 / b["paid, latest 6 months"][c]
            x[c] = (lo * hi) ** 0.5
    out = {}
    for c in W.CODES:
        t = round(g[c] / ((1 + W.CORRIDOR) * x[c]), 2)
        step = 0
        while abs(t - round(t)) < 0.05 or t in out.values():      # no target on a whole dollar, none repeated
            step += 1
            t = round(g[c] / ((1 + W.CORRIDOR) * x[c] * (1 + 0.0004 * step)), 2)
        out[c] = t
    return out, X


def build(out, quiet=False, world=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = world or S.simulate()
    f = lambda k: os.path.join(out, P.FILES[k])
    n = {}
    n["claims"] = P.write_claims(w, f("claims"))
    n["elig"] = P.write_elig(w, f("elig"))
    n["roster"] = P.write_roster(w, f("roster"))
    n["rx"] = P.write_rx(w, f("rx"))
    n["clinicians"] = P.write_clinicians(w, f("clinicians"))
    n["quality"] = P.write_quality(w, f("quality"))
    import polish as PO
    Cw = w["C"]
    info = dict(movers=[m["npi"] for m in Cw["moves"]], pcp=Cw["pcp"],
                outside_example=(Cw["outside"][0], Cw["outside_bill"][Cw["outside"][0]]))
    w["polish"] = dict(leakage=PO.leakage(out, Cw["group"], info), rx=PO.rx(out))
    targets, X = place_targets(out)
    DC.write_schedule_b(f("agreement"), targets, w["C"]["group"])
    DC.write_tallis_notice(f("notice"))
    DC.write_code_values(f("codes"))
    DC.write_stop_loss(f("stoploss"))
    adm, ctl = W.PEOPLE["administrator"][0], W.PEOPLE["controller"][0]
    PP.normalize_ooxml(f("clinicians"), adm, adm, "2024-06-11T13:02:00Z", "2027-01-04T15:27:44Z", excel=True, company=W.FUND)
    PP.normalize_ooxml(f("quality"), ctl, adm, "2026-12-08T16:40:00Z", "2027-01-22T19:05:31Z", excel=True, company=W.FUND)
    PP.normalize_pdf(f("agreement"), b"D:20251118153012-05'00'", b"D:20251119094405-05'00'")
    PP.normalize_pdf(f("notice"), b"D:20260915101500-05'00'", b"D:20260915101500-05'00'")
    PP.normalize_pdf(f("stoploss"), b"D:20251222111806-05'00'", b"D:20251222112251-05'00'")
    stamp = STAMP.timestamp()
    for name in os.listdir(out):
        os.utime(os.path.join(out, name), (stamp, stamp))
    w["counts"] = n
    w["targets"] = targets
    if not quiet:
        print("built %s: %d files; %s" % (out, len(os.listdir(out)), ", ".join("%s %d" % kv for kv in n.items())))
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 2, 3, 14, 18, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for name in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(name, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, name), "rb").read())
    return zp


def everything(root, quiet=False, world=None):
    import golden as G
    import metadata as MD
    world = build(os.path.join(root, "target"), quiet=quiet, world=world)
    if os.path.exists(os.path.join(root, "golden")):
        shutil.rmtree(os.path.join(root, "golden"))
    world["golden"] = G.main(os.path.join(root, "target"), os.path.join(root, "golden"),
                             os.path.join(root, "generator", "figures.json"))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    return world


def main():
    import checks as CK
    import verify as V
    world = everything(TASK)
    ok = CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), world=world,
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
                          "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode() +
                          open(os.path.join(TASK, "metadata.json"), "rb").read() +
                          open(os.path.join(HERE, "figures.json"), "rb").read()).hexdigest()
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
    if not ok:
        raise SystemExit("checks failed")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    else:
        main()
