"""Build the pack, compute every owed figure from it, write figures.json, the goldens, submission.md and
metadata.json, run the checks and the independent verifier, rebuild into a scratch folder and require
byte-identical output, then cut target.zip.

    python3 task249/generator/make.py            (full: two builds, the zip)
    python3 task249/generator/make.py --once     (one build, no zip)
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import checks as CK
import golden as GD
import params as P
import solve as S
import verify as V
import writeup as WU

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
ZIP_STAMP = (2028, 1, 17, 9, 30, 0)


def components(C):
    """the critical components' figures: a recognised item's time against the candidate's pace, the share running
    out of time on the speeded forms"""
    D, T = C["D"], C["T"]
    Pn, Mu = S.norms(T)
    num = den = 0.0
    for t in T:
        if t["w"] < 4 or not t["prev"]:
            continue
        same, sib, rev = S.exposure(T, t, D)
        expo = same | sib
        mj = np.array([Mu.get((t["w"], it), np.nan) for it in t["items"]])
        rc = t["reach"]
        tu = rc & ~expo & ~np.isnan(mj)
        lr = np.log(t["secs"][tu]) - mj[tu]
        e = rc & expo & ~np.isnan(mj)
        if not e.any():
            continue
        num += float(t["secs"][e].sum())
        den += float((np.exp(mj[e] + lr.mean()) * np.exp(lr.var() / 2)).sum())
    ft = [t for t in T if t["form"] in ("CC27-B", "CC27-D", "CC27-I") and not t["prev"]]
    share = np.mean([not t["reach"][-1] for t in ft])
    return dict(recognised_time_pct=int(5 * round(20 * num / den)), speeded_share_pct=int(10 * round(10 * share)))


LICENSED = ["golden", "golden_add", "golden_median", "golden_hit", "golden_median_hit"]


def family(C):
    """every licensed estimate's per-form gain and its two parts (a logit or additive baseline, the mean or median
    time, a submitted sitting's reach kept or rerun), the bounds the write-up states, and a recognised item's time
    against the candidate's own pace on the same item and on an item-model sibling"""
    D, T = C["D"], C["T"]
    Pn, Mu = S.norms(T)
    res = {v: {f: [] for f in S.F27} for v in LICENSED}
    lt = {"same": [], "sib": []}
    for t in T:
        if t["w"] < 4 or not t["prev"] or t["form"] not in S.F27:
            continue
        same, sib, rev = S.exposure(T, t, D)
        for v in LICENSED:
            res[v][t["form"]].append(S.sitting_gain(t, same, sib, Pn, Mu, v))
        mj = np.array([Mu.get((t["w"], it), np.nan) for it in t["items"]])
        rc = t["reach"] & ~np.isnan(mj)
        u = rc & ~same & ~sib
        if u.sum() < 20:
            continue
        lr = np.log(t["secs"]) - mj
        pace = float(np.nanmean(lr[u]))
        lt["same"].extend(lr[rc & same] - pace)
        lt["sib"].extend(lr[rc & sib & ~same] - pace)
    m = {v: {f: np.array(res[v][f]).mean(0) for f in S.F27} for v in LICENSED}
    flagged = C["flagged"]
    others = [f for f in S.F27 if f not in flagged]
    lo = min(m[v][f].sum() for v in LICENSED for f in flagged)
    hi = max(m[v][f].sum() for v in LICENSED for f in others)
    bd = [m[v][f][0] for v in LICENSED for f in ("CC27-B", "CC27-D")]
    reach_bd = min(m[v][f][1] for v in LICENSED for f in ("CC27-B", "CC27-D"))
    reach_i = [m[v]["CC27-I"][1] for v in LICENSED]
    direct_acgh = min(m[v][f][0] for v in LICENSED for f in ("CC27-A", "CC27-C", "CC27-G", "CC27-H"))
    return {"lo_flagged": float(np.floor(lo * 10) / 10), "hi_other": float(np.ceil(hi * 10) / 10),
            "direct_bd": round(float(np.mean(bd)), 1), "direct_acgh_min": float(np.floor(direct_acgh * 10) / 10),
            "reach_bd_min": float(np.floor(reach_bd * 10) / 10), "reach_i": round(float(np.mean(reach_i)), 1),
            "time_same": round(float(np.exp(np.mean(lt["same"]))), 1), "time_sib": round(float(np.exp(np.mean(lt["sib"]))), 1),
            "spread": {f: [round(float(min(m[v][f].sum() for v in LICENSED)), 2), round(float(max(m[v][f].sum() for v in LICENSED)), 2)]
                       for f in S.F27}}


def figures(target, X):
    C = S.call(target)
    A, _ = S.ask_a(target, D=C["D"])
    Bk = S.ask_b(target, D=C["D"])
    n_resit = sum(C["comp"][f]["n"] for f in S.F27)
    routes = {k: S.flagged(C["routes"], k) for k in ("golden", "golden_add", "golden_median", "direct",
                                                     "direct_blanks_wrong", "same_item", "raw_within", "between")}
    fig = {
        "call": {"flagged": C["flagged"], "threshold": P.THRESH, "gain": C["gain"],
                 "direct": {f: C["comp"][f]["direct"] for f in S.F27}, "reach": {f: C["comp"][f]["reach"] for f in S.F27},
                 "resit_sittings": {f: C["comp"][f]["n"] for f in S.F27}, "n_resit": n_resit, "routes": routes},
        "components": components(C),
        "family": family(C),
        "asks": {"interrupted": A, "offline": Bk, "power_day": "19 August 2027",
                 "hall_stops": "the Chennai fire alarm of 14 May 2027 and the Hyderabad switch to the generator of 16 "
                               "November 2027"},
    }
    return fig, C


def metadata(target, fig):
    files = []
    for k in B.PACK:
        f = B.FILES[k]
        p = os.path.join(target, f)
        rows = sum(1 for _ in open(p, encoding="utf-8")) - 1 if f.endswith(".csv") else None
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "source": "Constructed (seeded generator)", "date": "2028-01-17", "license": "CC0-1.0 (original work)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    return {
        "task": "task249",
        "title": "Which of a coding certification examination's ten 2027 forms gave their resit candidates more than one "
                 "scored item per resit sitting from what an earlier sitting or results review had shown them, beside each "
                 "form's 2027 sittings a workstation or power failure interrupted and those that ran in part without the "
                 "centre's link",
        "domain": "Psychology & Behavioral Science",
        "subdomain": "psychometric-measurement-scale-validation (repeat-examinee exposure on a credentialing examination's "
                     "forms: item models, randomly drawn forms, four-hour open-book sittings, latencies and unanswered items)",
        "objective": "Data Quality Monitoring & Alerting",
        "prompt_shape": "10: a designation over ten forms against the regulations' one-item line, beside two audit figures "
                        "for the integrity report and a chart of every form's gain against the line",
        "as_of": "2028-01-17",
        "deliverables": [GD.XLSX, GD.PDF],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "context_artifacts": [B.FILES[k] for k in B.CONTEXT],
        "stated_inputs": [], "field_terms": [],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated by task249/generator/make.py (seeded, deterministic) around a fictional Indian "
                               "professional institute's coding certification examination: an item bank written from item "
                               "models, six 2026 and ten 2027 forms, trial blocks, four-hour open-book sittings with each "
                               "item's latency, resits on a form not sat before, results reviews, a test delivery provider's "
                               "exports, seat plan and event log, invigilators' reports and the item review panel's log; "
                               "the institute, provider, centres, items and every person are invented, the psychometric "
                               "methods follow published practice, and no real dataset is reproduced.",
                     "date": "2028-01-17", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-21",
        "generator": "task249/generator/make.py",
        "files": files,
    }


def digest(folder):
    out = {}
    for f in sorted(os.listdir(folder)):
        out[f] = hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest()
    return out


def run(once=False):
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    X = B.run(TARGET)
    fig, C = figures(TARGET, X)
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    GD.write(GOLDEN, fig)
    WU.write(os.path.join(TASK, "submission.md"), fig)
    json.dump(metadata(TARGET, fig), open(os.path.join(TASK, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    CK.main(TARGET, dict(W=X["W"], A=X["A"]))
    assert V.main(TARGET) == 0, "verify"
    if once:
        return
    tmp = tempfile.mkdtemp()
    try:
        B.run(os.path.join(tmp, "target"))
        a, b = digest(TARGET), digest(os.path.join(tmp, "target"))
        assert a == b, "rebuild differs: %s" % [k for k in a if a[k] != b.get(k)]
        g1 = digest(GOLDEN)
        GD.write(os.path.join(tmp, "golden"), fig)
        assert g1 == digest(os.path.join(tmp, "golden")), "golden rebuild differs"
    finally:
        shutil.rmtree(tmp)
    z = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(os.listdir(TARGET)):
            info = zipfile.ZipInfo("target/" + f, ZIP_STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, open(os.path.join(TARGET, f), "rb").read())
    print("target.zip %s" % hashlib.sha256(open(z, "rb").read()).hexdigest()[:8])


if __name__ == "__main__":
    run(once="--once" in sys.argv)
