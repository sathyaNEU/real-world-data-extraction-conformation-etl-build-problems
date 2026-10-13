"""Build the pack, run the checks, write the goldens, the owed figures and metadata.json, run the independent verifier,
rebuild into a scratch folder and require byte-identical output, then cut target.zip.

    python3 task232/generator/make.py            (full: two builds, the zip)
    python3 task232/generator/make.py --once     (one build, no zip)
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
import params as P
import verify as V
import world as W

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMP = (2026, 11, 13, 6, 0, 0)
NAME_TO_FEED = {W.FEED[f]["name"]: f for f in P.FEEDS}


def answers(target):
    main, invs, names = V.main_call(target)
    g = main["window"]
    a = V.asks(target)
    rate = g["rate"]
    closed = {}
    recorded = {}
    for inv in invs:
        if inv["closed"]:
            closed[inv["cond"]] = closed.get(inv["cond"], 0) + 1
            recorded[inv["cond"]] = recorded.get(inv["cond"], 0) + len(inv["cases"])
    A = dict(
        feeds={NAME_TO_FEED[n]: g["feeds"][n] for n in names},
        rate=rate, num=g["num"], den=g["den"], closed=closed, recorded=recorded,
        reports={NAME_TO_FEED[n]: a["reports"][n] for n in names},
        cases={NAME_TO_FEED[n]: a["cases"].get(n, 0) for n in names},
        rungs={r: dict(rate=main[r]["rate"], num=main[r]["num"],
                       settings={NAME_TO_FEED[n]: main[r]["feeds"][n]["setting"] for n in names},
                       at={NAME_TO_FEED[n]: main[r]["feeds"][n]["at"] for n in names},
                       next={NAME_TO_FEED[n]: main[r]["feeds"][n]["next"] for n in names})
               for r in ("all", "lower", "upper", "before", "window")},
    )
    return A, main, invs, a


COND_ORDER = G.COND_ORDER
SHORT = {"Shigellosis": "shigellosis", "Shiga toxin-producing E. coli infection": "STEC infection",
         "Cryptosporidiosis": "cryptosporidiosis"}


def figures(A):
    """the figures the write-up owes, as it states them"""
    f2 = lambda x: "%.2f" % x
    fig = {
        "settings": {W.FEED[f]["name"]: str(A["feeds"][f]["setting"]) for f in P.FEEDS},
        "at": {W.FEED[f]["name"]: f2(A["feeds"][f]["at"]) for f in P.FEEDS},
        "next": {W.FEED[f]["name"]: (f2(A["feeds"][f]["next"]) if A["feeds"][f]["next"] is not None else "")
                 for f in P.FEEDS},
        "rate": {SHORT[c]: f2(1000 * A["rate"][c]) for c in COND_ORDER},
        "secondary_cases": {SHORT[c]: str(A["num"][c]) for c in COND_ORDER},
        "secondary_total": str(sum(A["num"].values())),
        "recorded_total": str(sum(A["recorded"].values())),
        "child_hours": {SHORT[c]: "{:,.2f}".format(A["den"][c]) for c in COND_ORDER},
        "closed_total": str(sum(A["closed"].values())),
        "basis_total": str(sum(A["feeds"][f]["n"] for f in P.FEEDS)),
        "basis": {W.FEED[f]["name"]: str(A["feeds"][f]["n"]) for f in P.FEEDS},
        "default_rate": {SHORT[c]: f2(1000 * A["rungs"]["all"]["rate"][c]) for c in COND_ORDER},
        "default_settings": {W.FEED[f]["name"]: str(A["rungs"]["all"]["settings"][f]) for f in P.FEEDS},
        "lower_settings": {W.FEED[f]["name"]: str(A["rungs"]["lower"]["settings"][f]) for f in P.FEEDS},
        "reports": {W.FEED[f]["name"]: "{:,}".format(A["reports"][f][0]) for f in P.FEEDS},
        "late": {W.FEED[f]["name"]: str(A["reports"][f][1]) for f in P.FEEDS},
        "cases": {W.FEED[f]["name"]: str(A["cases"][f]) for f in P.FEEDS},
        "tolerance": "1.00", "allowed": ["1", "2", "4", "6", "8", "12", "24"],
        "basis_period": "1 October 2023 to 30 September 2026", "year": "1 October 2025 to 30 September 2026",
        "calling_hours": ["07:00", "21:00"], "per": "1,000", "hours_24": "24",
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
                      "source": "Constructed (seeded generator): " + dict(B.DICT_FILES).get(f, "data dictionary"),
                      "date": "2026-11-13", "license": "CC0-1.0 (original work)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task232",
        "title": "At what lateness each laboratory feed's SLA alert should page the on-call officer",
        "domain": "Epidemiology & Public Health",
        "subdomain": "disease surveillance and outbreak anomaly detection (attribution of a childcare room's cases to "
                     "the index case by incubation window)",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "other: a dial per laboratory feed (six feeds, seven allowed settings) with the expected secondary "
                        "cases at the setting and the next longer one, each condition's transmission, and two asks per "
                        "feed on the platform's message log and case extract",
        "as_of": "2026-11-16",
        "deliverables": [G.CSV, G.WORKBOOK],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "field_terms": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated by task232/generator/make.py (seeded, deterministic) around a fictional local "
                               "health district's public health unit (Coast and Ranges) and its laboratories; no real "
                               "person, laboratory, centre or case is depicted.",
                     "date": "2026-11-13", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-13",
        "generator": "task232/generator/make.py",
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
    world, plat, counts = B.build(TARGET)
    stamp(TARGET)
    A, mainres, invs, asks = answers(TARGET)
    G.write(A, GOLDEN)
    stamp(GOLDEN)
    fig = figures(A)
    metadata(TARGET)
    out = C.run(TARGET, GOLDEN, world, plat, A, mainres, asks)
    print("checks: %d passed" % len(out))
    V.main(TARGET)
    if second:
        tmp = tempfile.mkdtemp(dir=os.environ.get("TMPBUILD"))
        t2, g2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
        B.build(t2)
        stamp(t2)
        G.write(answers(t2)[0], g2)
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
