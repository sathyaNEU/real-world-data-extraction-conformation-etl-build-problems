"""task110 build: world -> assertions -> target/ -> golden deliverables -> verifier -> zips.

    python3 generator/build.py

Any failed assertion stops the build before anything is packaged."""
import hashlib
import json
import os
import random
import subprocess
import sys
import tempfile
import time
import zipfile
from decimal import Decimal as D

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import assertions as A  # noqa: E402
import docs  # noqa: E402
import gl as GLM  # noqa: E402
import golden  # noqa: E402
import ledger as L  # noqa: E402
import pack  # noqa: E402
import seal  # noqa: E402
import solution as S  # noqa: E402
import world as W  # noqa: E402
from params import PACK_DATE  # noqa: E402

TARGET = os.path.join(TASK, "target")
OUT = os.path.join(TASK, "deliverables")

FILES = {
    "register": "YCB_asset_register_2026-10-02.xlsx",
    "gl": "YCB_GL_detail_2025-07_to_2026-09.csv",
    "tb": "YCB_trial_balance_30-09-2026.xlsx",
    "fy25": "YCB_FY2025_financial_statements_extract.pdf",
    "approvals": "YCB_capital_approvals_2018-2026.csv",
    "scans": "verification_scans_YCB_2026.csv",
    "sheet": "RAY_count_sheet_07-10-2026.pdf",
    "brm": "BRM_load_2026-07-01.csv",
    "mapping": "group_asset_class_mapping.xlsx",
    "spec": "fa_load_specification.xlsx",
    "standard": "fa_migration_standard.pdf",
    "procedure": "asset_verification_procedure.pdf",
    "thread": "RE_Yacaaba_cutover.eml",
    "notes": "YCB_extract_notes.md",
    "sources": "sources_and_licences.txt",
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


TUNE_FILE = os.path.join(HERE, "tuning.json")


def tuning_assets(w):
    """Minor assets still depreciating in 2027: one furniture item per site, one computer item per site,
    and one each in the other classes, so every graded figure has a lever of a few cents."""
    eng = L.Engine(w.ledger_assets())
    picks = []
    for cat in ("Furniture & fittings", "Computer equipment"):
        for s in ("CHA", "MAI", "CES", "RAY"):
            c = [a for a in w.ledger_assets() if a["category"] == cat and a["site"] == s and a["kind"] == "main"
                 and not a["disposed"] and eng.h2(a) > 0 and a is not w.joinery]
            c.sort(key=lambda a: int(a["id"]))
            if c:
                picks.append(c[-1]["id"])
    # nil-book-value assets that load at each site (the base world's own load), so every site's nil cost has a lever
    w2 = W.World()
    e2 = L.Engine(w2.ledger_assets())
    w2.approvals = W.build_approvals(w2)
    W.build_verification(w2, e2)
    base = S.solve(w2)
    for s in ("CHA", "MAI", "CES", "RAY"):
        c = [r["a"] for r in base["rows"] if r["site"] == s and r["nbv"] == 0 and r["a"]["kind"] == "main"]
        c.sort(key=lambda a: (a["category"] not in ("Furniture & fittings", "Computer equipment"), int(a["id"])))
        picks += [a["id"] for a in c[:2]]
    for cat in ("Ultrasound", "Motor vehicles", "Leasehold improvements", "Medical imaging equipment"):
        c = [a for a in w.ledger_assets() if a["category"] == cat and a["kind"] == "main" and not a["disposed"]
             and eng.h2(a) > 0 and a["cost"] < 200000]
        c.sort(key=lambda a: int(a["id"]))
        if c:
            picks.append(c[-1]["id"])
    return picks


def find_tweak():
    """Deterministic search for cents adjustments that put every graded figure clear of the half-dollar."""
    if os.path.exists(TUNE_FILE):
        return json.load(open(TUNE_FILE))
    base = W.World()
    picks = tuning_assets(base)
    be = L.Engine(base.ledger_assets())
    base_nil = {a["id"]: be.nbv(a, L.DEC26) == 0 for a in base.ledger_assets()}
    rng = random.Random(4110)
    for attempt in range(3000):
        tweak = {} if attempt == 0 else {no: rng.randint(-60, 60) if base_nil.get(no) else rng.randint(-24000, 24000) for no in picks}
        w = W.World(tweak)
        eng = L.Engine(w.ledger_assets())
        w.approvals = W.build_approvals(w)
        W.build_verification(w, eng)
        t = S.solve(w)
        figs = [t["h2"]] + [t["sites"][s][k] for s in t["sites"] for k in ("nbv_sep", "q4", "nbv_load", "h2", "nil_cost")] + list(t["classes"].values())
        foot = all(sum(S.rnd(t["sites"][s][k]) for s in t["sites"]) == S.rnd(sum((t["sites"][s][k] for s in t["sites"]), D(0)))
                   for k in ("nbv_sep", "q4", "nbv_load", "h2", "nil_cost"))
        foot = foot and sum(S.rnd(v) for v in t["classes"].values()) == S.rnd(t["load_nbv"])
        if foot and all(abs(((D(v) - D(int(D(v)))) % 1) - D("0.5")) >= D("0.03") and S.rnd(v) % 1000 != 0 for v in figs):
            json.dump(tweak, open(TUNE_FILE, "w"), indent=1, sort_keys=True)
            return tweak
    raise SystemExit("no tweak found")


def make_world():
    w = W.World(find_tweak())
    eng = L.Engine(w.ledger_assets())
    w.approvals = W.build_approvals(w)
    W.build_verification(w, eng)
    g = GLM.GL(w, eng, random.Random(9110))
    lines = g.build()
    return w, eng, lines


def write_target(w, eng, lines):
    os.makedirs(TARGET, exist_ok=True)
    for f in os.listdir(TARGET):
        os.remove(os.path.join(TARGET, f))
    p = lambda k: os.path.join(TARGET, FILES[k])  # noqa: E731
    pack.write_register(p("register"), w)
    pack.write_gl(p("gl"), lines)
    prelim = GLM.trial_balance(lines)
    final = GLM.trial_balance(lines, GLM.reclass_entries(w, eng))
    pack.write_tb(p("tb"), prelim, final)
    docs.fy2025_extract(p("fy25"), w, eng)
    pack.write_approvals(p("approvals"), w.approvals)
    pack.write_scans(p("scans"), w)
    docs.count_sheet(p("sheet"), w)
    brm = pack.write_bremer_load(p("brm"), random.Random(2110))
    pack.write_mapping(p("mapping"))
    pack.write_load_spec(p("spec"))
    docs.migration_standard(p("standard"))
    docs.verification_procedure(p("procedure"))
    docs.thread(p("thread"))
    counts = dict(reg=len(w.assets), gl=len(lines), appr=len(w.approvals), scan=len(w.verification["scans"]), brm=len(brm))
    docs.extract_notes(p("notes"), counts["gl"], counts["reg"], counts["appr"], counts["scan"], counts["brm"])
    docs.sources(p("sources"), counts)
    seal.seal_target(TARGET, FILES)
    return counts, prelim, final


def zip_files(paths, zpath):
    if os.path.exists(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(paths):
            zi = zipfile.ZipInfo(os.path.basename(f), date_time=time.localtime(os.path.getmtime(f))[:6])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(f, "rb") as fh:
                z.writestr(zi, fh.read())


def main():
    t0 = time.time()
    w, eng, lines = make_world()
    truth, lure, endh, ten, less1, cells = A.ladder(w)
    A.construction_layer(truth, lure)
    A.host_text(w)
    scan_tbl = A.scan_devices(w, truth)
    dev = A.devices(w, truth)
    figs = A.bins(truth)
    A.footing(truth)
    counts, prelim, final = write_target(w, eng, lines)
    A.check("gate: GL detail has more than 10,000 lines", counts["gl"] > 10000, counts["gl"])
    A.check("gate: 10 or more files", len(os.listdir(TARGET)) >= 10, len(os.listdir(TARGET)))
    exts = {os.path.splitext(f)[1] for f in os.listdir(TARGET)}
    A.check("gate: 3 or more formats", len(exts) >= 3, sorted(exts))
    with tempfile.TemporaryDirectory() as td:
        golden.build(truth, OUT, td)
    seal.seal_deliverables(OUT)
    import writeup
    writeup.render(os.path.join(TASK, "submission.md"), truth)
    gf = {
        "h2": S.rnd(truth["h2"]), "h2_cents": str(truth["h2"]),
        "sites": {s: {k: (S.rnd(v) if not isinstance(v, int) else v) for k, v in truth["sites"][s].items()} for s in truth["sites"]},
        "classes": {k: S.rnd(v) for k, v in truth["classes"].items()},
        "load_rows": truth["load_rows"], "load_nbv": S.rnd(truth["load_nbv"]), "load_cost": S.rnd(truth["load_cost"]),
        "q4": S.rnd(truth["q4"]), "written_off": len(truth["written_off"]),
        "cells": {k: str(v) for k, v in cells.items()},
        "lure_sites": {s: {k: (S.rnd(v) if not isinstance(v, int) else v) for k, v in lure["sites"][s].items()} for s in lure["sites"]},
        "lure_classes": {k: S.rnd(v) for k, v in lure["classes"].items()},
        "devices": {k: {kk: str(vv) for kk, vv in v.items()} for k, v in dev.items()},
        "scan_devices": {k: {kk: str(vv) for kk, vv in v.items()} for k, v in scan_tbl.items()},
    }
    with open(os.path.join(HERE, "golden_figures.json"), "w") as fh:
        json.dump(gf, fh, indent=1, sort_keys=True)
    # the independent verifier reads only the shipped files
    r = subprocess.run([sys.executable, os.path.join(HERE, "verify_pack.py")], capture_output=True, text=True)
    print(r.stdout[-3000:])
    A.check("verifier: passes on the shipped bundle", r.returncode == 0, r.stderr[-2000:])
    zip_files([os.path.join(TARGET, f) for f in os.listdir(TARGET)], os.path.join(TASK, "target.zip"))
    zip_files([os.path.join(OUT, f) for f in os.listdir(OUT)], os.path.join(TASK, "deliverables.zip"))
    with open(os.path.join(HERE, "build_report.txt"), "w") as fh:
        for name, ok, detail in A.RESULTS:
            fh.write("%s  %s\n" % ("PASS" if ok else "FAIL", name))
        fh.write("\n%d assertions\n" % len(A.RESULTS))
        for f in sorted(os.listdir(TARGET)):
            fh.write("%s  %s\n" % (sha(os.path.join(TARGET, f))[:16], f))
        for f in sorted(os.listdir(OUT)):
            fh.write("%s  %s\n" % (sha(os.path.join(OUT, f))[:16], f))
    print("build ok: %d assertions, H2 %s, %.1fs" % (len(A.RESULTS), truth["h2"], time.time() - t0))


if __name__ == "__main__":
    main()
