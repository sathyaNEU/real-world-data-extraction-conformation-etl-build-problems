"""Build task306 from its seed: the pack (target/), every owed figure computed from the pack alone, the goldens
(golden/), figures.json, submission.md and metadata.json; then the checks, a second build into a scratch folder that
has to match byte for byte, target.zip and the independent verifier on the zip.

    python3 task306/generator/build.py            (full)
    python3 task306/generator/build.py --once     (one build, no rebuild, no zip)
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A
import docs as D
import pack as P
import postprocess
import season as S
import world as W

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = (2026, 11, 2, 9, 30, 0)       # the morning the Board folder was put together


def build_target(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    P.write_ylt(F["ylt"], W.ylt())
    rec, _ = W.record()
    named = P.record_rows(sorted(rec))
    P.write_hindcast(F["hindcast"], named)
    P.write_experience(F["experience"], named)
    claims, adj = S.season2026()
    P.write_claims(F["claims"], claims)
    P.write_adjusters(F["adjusters"], adj)
    home, farms, locations, coins = S.exposure()
    P.write_home(F["home"], home)
    P.write_farm(F["farm"], farms, locations)
    P.write_coins(F["coins"], coins)
    P.write_flood(F["flood"])
    P.write_panel(F["panel"])
    D.capital_policy(F["capital"])
    postprocess.scrub(F["capital"], W.ORG, "2026-06-17")
    D.broker_quote(F["quote"])
    postprocess.scrub(F["quote"], W.BROKER, "2026-10-14")
    D.expiring_wording(F["wording"])
    postprocess.scrub(F["wording"], W.BROKER, "2025-12-09")
    D.request_eml(F["request"])


def figures(target):
    """every owed figure, from the pack alone"""
    g = A.programme(target, "golden")
    rec = A.record(target)
    rf = A.record_follows(rec)
    pooled = A.loads(target, "pooled")[1]
    a = A.ask_a(target)
    b = A.ask_b(target)
    return {
        "gross": g["gross"], "net_base": g["net_base"], "net_both": g["net_both"],
        "release_sec": g["release_sec"], "margin_sec": g["margin_sec"], "value": g["value"],
        "rec_sec": g["rec_sec"], "rp_sec": g["rp_sec"], "release_base": g["release_base"],
        "load_lone": g["loads"][0], "load_follow": g["loads"][1], "pooled": pooled,
        "record": rec, "record_follow": [bool(x) for x in rf],
        "occ2026": a["occurrences"], "recovery2026": a["recovery"], "reinstatement2026": a["reinstatement"],
        "farm_si": b,
    }


def stamp(folder):
    t = dt.datetime(*STAMP, tzinfo=dt.timezone.utc).timestamp()
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (t, t))


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def fresh(folder):
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
    os.makedirs(folder, exist_ok=True)


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    return zp


def main(second=True, checks=True):
    import golden as GD
    import writeup as WU
    fresh(TARGET)
    build_target(TARGET)
    stamp(TARGET)
    G = figures(TARGET)
    fresh(GOLDEN)
    GD.write(GOLDEN, G)
    stamp(GOLDEN)
    WU.write(TASK, G)
    if checks:
        import checks as C
        assert not C.main(TARGET), "checks failed"
    if second:
        tmp = tempfile.mkdtemp()
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        build_target(t2)
        stamp(t2)
        os.makedirs(g2, exist_ok=True)
        GD.write(g2, figures(t2))
        stamp(g2)
        d1, d2 = digest(TARGET), digest(t2)
        assert d1 == d2, [f for f in d1 if d1[f] != d2.get(f)]
        e1, e2 = digest(GOLDEN), digest(g2)
        assert e1 == e2, [f for f in e1 if e1[f] != e2.get(f)]
        shutil.rmtree(tmp)
        zp = cut_zip()
        print("byte-identical rebuild; target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
        import verify as V
        assert not V.main(zp), "verify failed"
    return G


if __name__ == "__main__":
    if "--target-only" in sys.argv:
        fresh(TARGET)
        build_target(TARGET)
        stamp(TARGET)
    else:
        main(second="--once" not in sys.argv, checks="--nochecks" not in sys.argv)
