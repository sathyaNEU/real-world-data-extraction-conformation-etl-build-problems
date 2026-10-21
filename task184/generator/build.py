"""Build task184: the pack into <task>/target, the goldens into <task>/golden, metadata.json and
generator/figures.json, then the checks and the independent verifier, then a second full build into a scratch
folder inside the task (removed after) compared byte for byte, then target.zip cut from the final build.

    python3 task184/generator/build.py              everything
    python3 task184/generator/build.py --out DIR    the pack only, into DIR
    python3 task184/generator/build.py --no-checks  the pack, goldens and figures only"""
import argparse
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as AN     # noqa: E402
import asks as AK         # noqa: E402
import docs as D          # noqa: E402
import offences as O      # noqa: E402
import pack as P          # noqa: E402
import places as PL       # noqa: E402
import postprocess as PP  # noqa: E402
import records as R       # noqa: E402
import sensors as S       # noqa: E402
import world as W         # noqa: E402

TASK = os.path.dirname(HERE)
FILES = {
    "rms": R.RMS, "legacy": R.LEGACY, "notes": D.NOTES, "dictionary": D.DICTIONARY, "rules": D.RULES,
    "contract": D.CONTRACT, "schedule": D.SCHEDULE, "register": PL.REGISTER, "gazetteer": PL.GAZETTEER,
    "beats": PL.BEATS, "premises": PL.PREMISES, "counts": S.COUNTS, "availability": S.AVAIL,
    "sensors": S.SENSREG, "trading": S.TRADING, "plan": P.PLAN,
}
DISTRACTORS = ("plan", "premises")
BST = dt.timezone(dt.timedelta(hours=1))


def world():
    rows = R.decorate(O.simulate())
    fringe = R.fringe()
    R.unique_keys(rows, fringe)
    counts = S.counts()
    contracted = O.contracted(rows)
    lad = AN.ladder(contracted)
    return {"rows": rows, "fringe": fringe, "counts": counts, "contracted": contracted, "ladder": lad,
            "ask1": AK.offences_by_class(rows), "ask2": AK.location_shares(rows), "ask3": AK.footfall(counts)}


def build(out, quiet=False, w=None):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    w = w or world()
    P.build(out, w["rows"], w["fringe"], w["counts"])
    PP.normalize_ooxml(os.path.join(out, P.PLAN), W.PEOPLE["inspector"][0], W.PEOPLE["inspector"][0],
                       "2026-10-06T10:04:00Z", "2026-10-09T14:22:00Z", title="Harbourgate patrol plan 2026",
                       excel=True)
    PP.normalize_pdf(os.path.join(out, D.RULES), b"D:20270104093512+00'00'", b"D:20270104093512+00'00'")
    PP.normalize_pdf(os.path.join(out, D.CONTRACT), b"D:20261204161140+00'00'", b"D:20261204161140+00'00'")
    stamp = dt.datetime(2027, 1, 22, 9, 15, tzinfo=BST).timestamp()
    for f in os.listdir(out):
        os.utime(os.path.join(out, f), (stamp, stamp))
    if not quiet:
        print("built %s: %d files" % (out, len(os.listdir(out))))
    return w


def figures(w):
    """Every figure the write-up and the goldens state."""
    lad, g = w["ladder"], w["ladder"]["golden"]
    weights, slate = g["weights"], g["slate"]
    order = sorted(weights.items(), key=lambda kv: -kv[1])
    runner = order[W.CAP]
    fifty = lambda x: int(round(x / 50.0) * 50)
    name = lambda s: "%s %02d:00-%02d:00" % (W.DAYS[s[0]], s[1], (s[1] + W.SLOT_H) % 24)
    fig = {
        "call": {
            "slate": [name(s) for s in slate],
            "slot_offences": {name(s): fifty(weights[s]) for s in slate},
            "covered_total": fifty(g["files"]),
            "covered_total_exact": round(g["files"], 2),
            "runner_up": name(runner[0]),
            "runner_up_offences": fifty(runner[1]),
            "weakest_of_the_eight": fifty(weights[slate[-1]]),
            "gap_to_the_runner_up": fifty(weights[slate[-1]]) - fifty(runner[1]),
        },
        "week": {name(s): fifty(weights[s]) for s in W.SLOTS},
        "default_path": {
            "slate": [name(s) for s in lad["rung3_flat_aoristic"]["slate"]],
            "files": fifty(lad["rung3_flat_aoristic"]["files"]),
            "meets": fifty(lad["rung3_flat_aoristic"]["meets"]),
            "share_of_golden": round(lad["rung3_flat_aoristic"]["meets"] / g["files"], 3),
        },
        "rungs": {k: {"slate": [name(s) for s in v["slate"]], "files": fifty(v["files"]), "meets": fifty(v["meets"]),
                      "share_of_golden": round(v["meets"] / g["files"], 3)}
                  for k, v in lad.items() if k != "golden"},
        "asks": {
            "offences_by_class": {"%s %d" % (c, 2025 + si): int(round(w["ask1"][(c, si)], -1))
                                  for c in W.CLASSES for si in range(len(W.SEASONS))},
            "location_shares_per_cent": {"%s %d" % (loc, 2025 + si): round(w["ask2"][(loc, si)], 1)
                                         for loc in W.LOCATIONS for si in range(len(W.SEASONS))},
            "footfall_per_trading_hour": {"%s %d" % (sid, 2025 + si): int(round(w["ask3"][(sid, si)], -1))
                                          for sid in sorted(W.SENSORS) for si in range(len(W.SEASONS))},
        },
        "context": {
            "slots_in_the_week": len(W.SLOTS),
            "contracted_offences_both_seasons": len(w["contracted"]),
            "contracted_offences_a_season": int(round(len(w["contracted"]) / len(W.SEASONS))),
            "share_of_windows_over_four_hours_per_cent": round(100.0 * sum(
                1 for r in w["contracted"] if (r["to"] - r["from"]).total_seconds() > 4 * 3600) /
                len(w["contracted"]), 1),
            "share_carrying_a_window_per_cent": round(100.0 * sum(
                1 for r in w["contracted"] if r["to"] > r["from"]) / len(w["contracted"]), 1),
            "share_of_windows_crossing_a_slot_per_cent": round(100.0 * sum(
                1 for r in w["contracted"]
                if O.slot_of(r["from"]) != O.slot_of(r["to"] - dt.timedelta(seconds=1))) /
                len(w["contracted"]), 1),
            "share_of_windows_over_four_hours": round(
                sum(1 for r in w["contracted"] if (r["to"] - r["from"]).total_seconds() > 4 * 3600) /
                len(w["contracted"]), 3),
            "share_of_windows_crossing_a_slot": round(
                sum(1 for r in w["contracted"]
                    if O.slot_of(r["from"]) != O.slot_of(r["to"] - dt.timedelta(seconds=1))) /
                len(w["contracted"]), 3),
            "rms_rows": len(R.rms_rows(w["rows"], w["fringe"])) - 1,
            "legacy_rows": len(R.legacy_rows(w["rows"], w["fringe"])) - 1,
            "footfall_rows": len(w["counts"]),
        },
    }
    return fig


def everything(root, quiet=False):
    import deliver as DL
    import metadata as MD
    w = build(os.path.join(root, "target"), quiet=quiet)
    gold = os.path.join(root, "golden")
    if os.path.exists(gold):
        shutil.rmtree(gold)
    os.makedirs(gold)
    fig = figures(w)
    with open(os.path.join(root, "generator", "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    tmp = tempfile.mkdtemp()
    try:
        DL.paper(os.path.join(gold, DL.PAPER), fig, w["ladder"], tmp)
    finally:
        shutil.rmtree(tmp)
    DL.workbook(os.path.join(gold, DL.BOOK), w["ladder"], w["ask1"], w["ask2"], w["ask3"])
    an = W.PEOPLE["analyst"][0]
    PP.normalize_pdf(os.path.join(gold, DL.PAPER), b"D:20270129094122+00'00'", b"D:20270129101705+00'00'")
    PP.normalize_ooxml(os.path.join(gold, DL.BOOK), an, an, "2027-01-28T16:12:00Z", "2027-01-29T09:41:00Z",
                       title="Harbourgate patrol slot weights", excel=True)
    stamp = dt.datetime(2027, 1, 29, 10, 20, tzinfo=BST).timestamp()
    for f in os.listdir(gold):
        os.utime(os.path.join(gold, f), (stamp, stamp))
    MD.write(os.path.join(root, "target"), os.path.join(root, "metadata.json"))
    w["fig"] = fig
    return w


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
            for f in sorted(os.listdir(folder))}


def cut_zip(root):
    import zipfile
    folder = os.path.join(root, "target")
    stamp = (2027, 1, 22, 9, 15, 0)
    zp = os.path.join(root, "target.zip")
    with zipfile.ZipFile(zp, "w") as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zp


def main():
    import checks as CK
    import verify as V
    w = everything(TASK)
    CK.run(os.path.join(TASK, "target"), os.path.join(TASK, "golden"), w, os.path.join(TASK, "metadata.json"))
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
    allh = hashlib.sha256(
        "".join(v for _, v in sorted(digest(os.path.join(TASK, "target")).items())).encode() +
        "".join(v for _, v in sorted(digest(os.path.join(TASK, "golden")).items())).encode()).hexdigest()
    print("two builds byte-identical: %d target files, %d golden files, metadata.json and figures.json (sha256 %s)"
          % (len(os.listdir(os.path.join(TASK, "target"))), len(os.listdir(os.path.join(TASK, "golden"))),
             allh[:16]))
    import zipfile
    zp = cut_zip(TASK)
    with zipfile.ZipFile(zp) as z:
        inside = {i.filename: hashlib.sha256(z.read(i.filename)).hexdigest() for i in z.infolist()}
    if inside != digest(os.path.join(TASK, "target")):
        raise SystemExit("target.zip differs from target/")
    print("target.zip cut from this build: %d files, each identical to target/ (sha256 %s)"
          % (len(inside), hashlib.sha256(open(zp, "rb").read()).hexdigest()[:16]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="build the pack only, into this folder")
    ap.add_argument("--no-checks", action="store_true", help="build the pack, goldens and figures only")
    a = ap.parse_args()
    if a.out:
        build(a.out)
    elif a.no_checks:
        everything(TASK)
    else:
        main()
