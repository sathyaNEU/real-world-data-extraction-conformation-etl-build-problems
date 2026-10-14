"""Build the pack, compute every owed figure, write the goldens, figures.json and metadata.json, run the checks and the
independent verifier, rebuild into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task230/generator/make.py            (full: two builds, the zip)
    python3 task230/generator/make.py --once     (one build, no zip)
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
import estim as E
import golden as GD
import params as P
import world as W

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = (2026, 11, 13, 18, 0, 0)
ROUTE_NAME = {"O": "online self-response", "P": "paper self-response", "FS": "follow-up, household member",
              "FP": "follow-up, proxy"}


def answers(target):
    D = E.load(target)
    out, R = E.rungs(D)
    gold = out["golden"]
    A = dict(warned=E.flags(gold), bias={g: float(v) for g, v in zip(W.GROUPS, gold)},
             bias_r={g: float(f"{v:.1f}") + 0.0 for g, v in zip(W.GROUPS, gold)},
             coded={r: int(R[r]["nc"]) for r in P.ROUTES}, still={r: int(R[r]["m"]) for r in P.ROUTES},
             rung_flags={k: E.flags(v) for k, v in out.items()}, rung_values={k: [float(x) for x in v] for k, v in out.items()},
             teams=E.ask_teams(D), regions=E.ask_regions(D))
    return A, D, out, R


def _list(gs):
    return ", ".join(gs[:-1]) + " and " + gs[-1] if len(gs) > 1 else gs[0]


def figures(A):
    f1 = lambda x: f"{x:.1f}".replace("-0.0", "0.0")
    fig = {
        "warned": _list(A["warned"]),
        "warned_bias": {g: f1(A["bias"][g]) for g in A["warned"]},
        "bias": {g: f1(A["bias"][g]) for g in W.GROUPS},
        "coded": {ROUTE_NAME[r]: "{:,}".format(A["coded"][r]) for r in P.ROUTES},
        "still": {ROUTE_NAME[r]: "{:,}".format(A["still"][r]) for r in P.ROUTES},
        "coded_total": "{:,}".format(sum(A["coded"].values())),
        "still_total": "{:,}".format(sum(A["still"].values())),
        "release_total": "{:,}".format(sum(A["coded"].values()) + sum(A["still"].values())),
        "default_flags": _list(A["rung_flags"]["default"]),
        "rule_flags": _list(A["rung_flags"]["rule"]),
        "bt_new_flags": _list(A["rung_flags"]["bt_new"]),
        "route_old_flags": _list(A["rung_flags"]["route_old"]),
        "teams": {t: {"writeins": "{:,}".format(A["teams"][t][0]), "hours": "{:,.2f}".format(A["teams"][t][1])}
                  for t in W.TEAMS},
        "regions": {n: {"calls": "{:,}".format(A["regions"][n][0]), "nocontact": "{:,}".format(A["regions"][n][1])}
                    for _, n, _ in W.REGIONS},
        "warning_line": "2.0", "warning_lines": ["-2.0", "+2.0"], "group_codes": list(W.GROUPS),
        "clauses_cited": ["2.1", "3.1", "3.3", "4.1", "5.3", "5.5"],
        "new_accept": "0.80", "old_accept": "0.90", "intervals": ["10", "4", "2"],
        "dates": ["13 November", "16 November", "31 October", "30 March 2027"], "groups": "40",
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
        elif f.endswith(".parquet"):
            import pyarrow.parquet as pq
            rows = pq.ParquetFile(p).metadata.num_rows
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "source": "Constructed (seeded generator)", "date": "2026-11-13",
                      "license": "CC0-1.0 (original work)" if k != "aoc" else
                      "ISCO-08 structure and titles: International Labour Office, International Standard Classification "
                      "of Occupations 2008 (reproduced for statistical use); national extension CC0-1.0"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task230",
        "title": "Which occupation groups carry the coding quality warning in the census's first occupation release",
        "domain": "Survey Research & Official Statistics",
        "subdomain": "census, register and administrative data quality (occupation coding bias in a census release)",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "10: scorecard, each of the 40 ISCO-08 sub-major groups' coding bias against the plus or minus 2.0 "
                        "per cent warning line, with two asks (five coding teams, eight regions)",
        "as_of": "2026-11-13",
        "deliverables": [GD.XLSX, GD.PNG],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "field_terms": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated by task230/generator/make.py (seeded, deterministic) around a fictional "
                               "island state's census office (the Office of the Registrar General of Aldmere); no real "
                               "person, address or return is depicted. ISCO-08 titles as published by the ILO.",
                     "date": "2026-11-13", "license": "CC0-1.0 (original work); ISCO-08 titles ILO"}],
        "created": "2026-10-14",
        "generator": "task230/generator/make.py",
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


def fresh(folder):
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))
    os.makedirs(folder, exist_ok=True)


def main(second=True, checks=True):
    fresh(TARGET)
    S, U, Cd, T, counts, facts = B.run(TARGET)
    stamp(TARGET)
    A, D, out, R = answers(TARGET)
    fresh(GOLDEN)
    GD.write(GOLDEN, A)
    stamp(GOLDEN)
    fig = figures(A)
    metadata(TARGET)
    if checks:
        import checks as C
        n = C.run(TARGET, GOLDEN, S, U, Cd, T, A, D, out, R, facts)
        print("checks: %d passed" % n)
        import verify as V
        V.main(TARGET, os.path.join(HERE, "figures.json"))
    if second:
        tmp = tempfile.mkdtemp(dir=os.environ.get("TMPBUILD"))
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        B.run(t2)
        stamp(t2)
        GD.write(g2, answers(t2)[0])
        stamp(g2)
        d1, d2 = digest(TARGET), digest(t2)
        assert d1 == d2, [f for f in d1 if d1[f] != d2.get(f)]
        assert digest(GOLDEN) == digest(g2), "golden differs between builds"
        shutil.rmtree(tmp)
        zp = cut_zip()
        print("byte-identical; target.zip sha256", hashlib.sha256(open(zp, "rb").read()).hexdigest())
    return A, fig


if __name__ == "__main__":
    main(second="--once" not in sys.argv, checks="--nochecks" not in sys.argv)
