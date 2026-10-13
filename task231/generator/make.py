"""Build the pack, run the checks, write the goldens, the owed figures and metadata.json, run the independent verifier,
rebuild into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task231/generator/make.py            (full: two builds, the zip)
    python3 task231/generator/make.py --once     (one build, no zip)
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
import build as B
import checks as C
import golden as G
import verify as V
import world as W

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = (2026, 9, 25, 22, 0, 0)


def answers(res):
    lad = res["ladder"]
    call = V.call_from(lad)
    pk = res["pack"]
    num = den = 0
    s = res["shares"]["settled"]
    sh, dn = pk.settled_share()
    A = dict(levels=call["levels"], extension=call["extension"], email=call["email"], neither=call["neither"],
             rate={g: lad[g]["golden"] for g in lad}, R={g: lad[g]["R"] for g in lad},
             inscope_pct=round(100.0 * (1 - s), 1), settled_pct=round(100.0 * s, 1),
             settled_den=dn["all"], settled_num=int(round(sh["all"] * dn["all"])),
             invited_total=sum(lad[g]["inv"] for g in lad), R_total=sum(lad[g]["R"] for g in lad),
             known_total=sum(lad[g]["known"] for g in lad), n_total=sum(lad[g]["n"] for g in lad),
             reached=res["A"]["reached"], calls=res["A"]["calls"],
             june_returns=res["B"]["returns"], late=res["B"]["late"], late_share=res["B"]["share"],
             recruited=res["C"]["recruited"], returned=res["C"]["returned"],
             default_red=[g for g in lad if V.band(lad[g]["R1"]) == "red"],
             default_amber=[g for g in lad if V.band(lad[g]["R1"]) == "amber"],
             casro_red=[g for g in lad if V.band(lad[g]["casro"]) == "red"],
             allr_red=[g for g in lad if V.band(lad[g]["allr"]) == "red"])
    return A


def figures(A, res):
    """the figures the write-up owes, as it states them"""
    name = lambda gs: [W.NAME[g] for g in gs]
    fig = {
        "extension": name(A["extension"]), "email": name(A["email"]), "neither": name(A["neither"]),
        "levels": A["levels"],
        "level_names": {W.NAME[g]: lv for g, lv in A["levels"].items()},
        "settled_pct": "%.1f" % A["settled_pct"], "inscope_pct": "%.1f" % A["inscope_pct"],
        "settled_rounds": "23", "settled_den": "{:,}".format(A["settled_den"]), "settled_num": "{:,}".format(A["settled_num"]),
        "invited_total": "{:,}".format(A["invited_total"]), "R_total": "{:,}".format(A["R_total"]),
        "known_total": "{:,}".format(A["known_total"]), "n_total": "{:,}".format(A["n_total"]),
        "rate": {g: "%.1f" % A["rate"][g] for g in W.REGS},
        "default_red": name(A["default_red"]), "default_red_n": str(len(A["default_red"])),
        "default_amber_n": str(len(A["default_amber"])),
        "casro_red": name(A["casro_red"]), "casro_red_n": str(len(A["casro_red"])),
        "allr_red": name(A["allr_red"]), "allr_red_n": str(len(A["allr_red"])),
        "share_all": "%.1f" % (100.0 * res["shares"]["all"]), "share_recent": "%.1f" % (100.0 * res["shares"]["recent"]),
        "reached": {g: str(v) for g, v in A["reached"].items()}, "calls": {g: str(v) for g, v in A["calls"].items()},
        "reached_fmt": {g: "{:,}".format(v) for g, v in A["reached"].items()},
        "calls_fmt": {g: "{:,}".format(v) for g, v in A["calls"].items()},
        "june_returns": {g: str(v) for g, v in A["june_returns"].items()},
        "late": {g: str(v) for g, v in A["late"].items()},
        "late_share": {g: "%.1f" % v for g, v in A["late_share"].items()},
        "recruited": {g: str(v) for g, v in A["recruited"].items()},
        "returned_once": {g: str(v) for g, v in A["returned"].items()},
        "recruited_total": str(sum(A["recruited"].values())), "returned_total": str(sum(A["returned"].values())),
        "close_june": "19 June 2026", "close_sep": "25 September 2026", "frame": "1 September 2026",
        "lines": ["55", "58"],
    }
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return fig


def metadata(target):
    files = []
    for k, f in B.FILES.items():
        p = os.path.join(target, f)
        rows = None
        if f.endswith(".csv"):
            rows = sum(1 for _ in open(p, encoding="utf-8")) - 1
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "source": "Constructed: " + (B.DESCRIBE.get(k) or "export manifest"), "date": "2026-09-25",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task231",
        "title": "Which regions go into the reminder-call extension of a central bank's business survey round",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "nonresponse, calibration and measurement-error adjustment (eligibility of unresolved non-respondents)",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "10 (scorecard): twelve regions' response rates checked against the 55 and 58 per cent lines, with the "
                        "contact centre's work, the June late returns and the March refreshment",
        "as_of": "2026-09-25",
        "deliverables": [G.WORKBOOK, G.SLIDE],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task231/generator/make.py (seeded, deterministic) around a "
                               "fictional central bank's business survey (Brevland Central Bank, Business Conditions Survey); "
                               "no real person, firm, organisation or register record is depicted.",
                     "date": "2026-09-25", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-13",
        "generator": "task231/generator/make.py",
        "files": files,
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
        fh.write("\n")


def stamp(folder):
    t = dt.datetime(*STAMP, tzinfo=dt.timezone.utc).timestamp()
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (t, t))


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip():
    zp = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(TARGET)):
            zi = zipfile.ZipInfo(f, date_time=STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(TARGET, f), "rb").read())
    return zp


def main(second=True):
    pan, rec, counts = B.build(TARGET)
    stamp(TARGET)
    res = V.compute(TARGET)
    A = answers(res)
    G.write(A, GOLDEN)
    stamp(GOLDEN)
    fig = figures(A, res)
    metadata(TARGET)
    out = C.run(TARGET, GOLDEN, pan, rec, res)
    V.main(TARGET, GOLDEN, os.path.join(HERE, "figures.json"))
    print("checks: %d passed" % len(out))
    if second:
        tmp = tempfile.mkdtemp(dir=os.environ.get("TMPBUILD"))
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        B.build(t2)
        stamp(t2)
        G.write(answers(V.compute(t2)), g2)
        stamp(g2)
        d1, d2 = digest(TARGET), digest(t2)
        assert d1 == d2, [f for f in d1 if d1[f] != d2.get(f)]
        assert digest(GOLDEN) == digest(g2), "golden differs between builds"
        shutil.rmtree(tmp)
        zp = cut_zip()
        print("byte-identical; target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    return A, fig


if __name__ == "__main__":
    main(second="--once" not in sys.argv)
