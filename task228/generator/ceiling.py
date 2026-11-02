"""task228 ask layer against the careful solver's routes, on the cut pack.

    python3 task228/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The script reads the
pack only (the verifier's bundle readers and pyarrow), modifies nothing and never runs inside the build. Every route is
a complete pipeline over the pack, scored figure by figure against figures.json; a count is kept only when it is exact.

The asks (prompt.txt after the call): A, for each check in the hold standard, the experiments with a confirmed data
incident it would have held (5 counts, the call's own construction); D, for each day from 6 to 19 August, how many of
the iOS and of the Android installs that sent events from SDK 9.4.1 from 3 to 6 August were still on it at the day's
end, Copenhagen time, going by the last batch each had sent (28 counts), from the collector's client summary.

The cracker is the careful solver. It lands the call (each session share tested with its variance over installs),
runs the hygiene battery on the client summary (exact and near-duplicate rows, one row a client ID and SDK version,
orphan keys, the sequence numbers checked against each client ID's own run, both clocks, the window's edges) and
reads every field by its plain meaning: a client ID is the collector's key for an install, the population is the
client IDs with a 9.4.1 batch from 3 to 6 August, and an install is still on 9.4.1 until a 9.4.2 batch arrives under
its client ID. The mirror is the best response off the call: it stops at the default path (the session-level
two-proportion z, late sessions at 0.22) and takes the ask on the same natural read. The full includer joins each
client ID first seen on 9.4.2 to the older client ID whose last sequence number it continues by one, through the
verifier's own code, and has to give back figures.json exactly (the route code's control): if it does not, the script
exits 1. The stops are the other wrong paths, each scored as a route.

The pair is the ask sheet's formula: 38 for the recommendation and the critical components, 7 for instruction
following, 55 for the asks spread evenly over the ask figures; a response off the call keeps r = 5 of the 38."""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from math import floor, sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estim as E    # noqa: E402  (the client summary's readers and the readings, pack only)
import verify as V   # noqa: E402  (the bundle-only readers, the per-arm accumulator and the independent join)

TASK = os.path.dirname(HERE)
Z, STD_N, ALLOW = V.Z, V.STD_N, 0.02
REC, INS, ASK, OFF = 38.0, 7.0, 55.0, 5.0
CHECKS = ["gap", "dup", "late", "epu", "share"]
TYPES = V.TYPES


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling228-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)), md5)


# ------------------------------------------------------------------ the pack, read as the verifier reads it
def load(folder):
    import pyarrow.parquet as pq
    from openpyxl import load_workbook
    from pypdf import PdfReader
    reg = V.read_registry(folder)["experiments"]
    arms = {}
    for r in V.q1_rows(folder):
        a = arms.setdefault((r["exp_id"], "control" if r["variant"] == "A" else "treatment"), V.Arm())
        a.add(int(r["n_sessions"]), int(r["sessions_seq_gap"]), int(r["sessions_dup_ids"]), int(r["sessions_late"]),
              int(r["events"]))
    for q in ("install_summary_2026q2.parquet", "install_summary_2026q3.parquet"):
        t = pq.read_table(os.path.join(folder, q)).to_pydict()
        for k, arm, s, g, d, l, ev in zip(t["experiment_key"], t["arm"], t["sessions"], t["gap_sessions"],
                                          t["duplicate_sessions"], t["late_sessions"], t["events_received"]):
            arms.setdefault((k, arm), V.Arm()).add(s, g, d, l, ev)
    ws = load_workbook(os.path.join(folder, "data_incident_register_2026.xlsx"), read_only=True)["Register"]
    rows = list(ws.iter_rows(values_only=True))
    register = [dict(zip(rows[0], r)) for r in rows[1:]]
    with open(os.path.join(folder, "weekly_review_log_2026.csv"), newline="", encoding="utf-8") as f:
        review = list(csv.DictReader(f))
    text = lambda f: " ".join(" ".join((p.extract_text() or "").split()) for p in PdfReader(os.path.join(folder, f)).pages)
    return dict(reg=reg, arms=arms, register=register, review=review,
                recon=text("reconciliation_summary_2026.pdf"), dh3=text("dh3_data_health_hold_standard.pdf"))


def labels(L):
    by_title = {V.norm(e["title"]): e["key"] for e in L["reg"]}
    return {by_title[V.norm(r["experiment"])] for r in L["register"] if r["scope"] == "experiment" and r["status"] == "confirmed"}


# ------------------------------------------------------------------ the call, on either route
def z_of(c, t, m, how):
    if how == "delta":
        def ratio(a):
            n = a.n
            mx, my = a.x[m] / n, a.y / n
            vx = (a.xx[m] - n * mx * mx) / (n - 1)
            vy = (a.yy - n * my * my) / (n - 1)
            cxy = (a.xy[m] - n * mx * my) / (n - 1)
            r = mx / my
            return r, (vx - 2 * r * cxy + r * r * vy) / (my * my * n)
        rc, vc = ratio(c)
        rt, vt = ratio(t)
        return (rt - rc) / sqrt(vc + vt)
    pc, pt = c.x[m] / c.y, t.x[m] / t.y
    pp = (c.x[m] + t.x[m]) / (c.y + t.y)
    return (pt - pc) / sqrt(pp * (1 - pp) * (1 / c.y + 1 / t.y))


def call(L, how):
    """each check's record, the pick under DH-3 s.5 and its line, for the install-level route or the session-level one"""
    inc = labels(L)
    design = {e["key"]: e["design"]["treatment"] for e in L["reg"]}
    keys = sorted(design)
    held = {m: set() for m in CHECKS}
    for k in keys:
        c, t = L["arms"][(k, "control")], L["arms"][(k, "treatment")]
        for m in ("gap", "dup", "late"):
            if z_of(c, t, m, how) > Z:
                held[m].add(k)
        ec, et = c.e / c.n, t.e / t.n
        vec = (c.ee - c.n * ec * ec) / (c.n - 1)
        vet = (t.ee - t.n * et * et) / (t.n - 1)
        if (ec - et) / sqrt(vec / c.n + vet / t.n) > Z:
            held["epu"].add(k)
        n, p = c.n + t.n, design[k]
        if (n * p - t.n) / sqrt(n * p * (1 - p)) > Z:
            held["share"].add(k)
    none = [k for k in keys if k not in inc]
    cap = floor(ALLOW * len(none) + 1e-9)
    rec = {m: (len(held[m] & inc), len(held[m] - inc)) for m in CHECKS}
    pick = sorted([m for m in CHECKS if rec[m][1] <= cap], key=lambda m: (-rec[m][0], rec[m][1]))[0]
    X = Y = XX = YY = XY = 0.0
    N = 0
    for k in none:
        for arm in ("control", "treatment"):
            a = L["arms"][(k, arm)]
            X += a.x[pick]; Y += a.y; XX += a.xx[pick]; YY += a.yy; XY += a.xy[pick]; N += a.n
    r = X / Y
    if how == "delta":
        s2 = (XX - 2 * r * XY + r * r * YY) / (N - 1) / (Y / N) ** 2
        line = 100 * Z * sqrt(2 * s2 / STD_N)
    else:
        line = 100 * Z * sqrt(2 * r * (1 - r) / (STD_N * (Y / N)))
    return dict(pick=pick, line=line, rec=rec, inc=inc)


# ------------------------------------------------------------------ the hygiene battery on the client summary
def battery(Cl):
    """(check, finding) lines: each a step the careful solver takes on the client summary before it counts anything"""
    out = []
    tup = list(map(tuple, Cl.astype(str).to_numpy()))
    out.append(("exact duplicate rows", "%d" % (len(tup) - len(set(tup)))))
    out.append(("one row a client ID and SDK version", "%s" % (Cl.groupby(["client_id", "sdk_version"]).size().max() == 1)))
    near = Cl.groupby(["platform", "first_seq", "last_seq", "events"]).size()
    out.append(("near-duplicate rows (platform, sequence range, events)", "%d" % int((near - 1).clip(lower=0).sum())))
    has942 = set(Cl.loc[Cl["sdk_version"] == "9.4.2", "client_id"])
    older = Cl[Cl["sdk_version"] != "9.4.2"]
    lo = older[older["client_id"].isin(has942)].sort_values(["client_id", "last_batch"]).groupby("client_id").last()
    nx = Cl[Cl["sdk_version"] == "9.4.2"].set_index("client_id")
    cont = (nx.loc[lo.index, "first_seq"].to_numpy() == lo["last_seq"].to_numpy() + 1)
    out.append(("each client ID's sequence runs on across its SDK versions", "%d of %d" % (cont.sum(), len(cont))))
    out.append(("sequence numbers starting at one or near it", "%d" % int((Cl["first_seq"] < 1000).sum())))
    out.append(("client IDs on 9.4.2 with no earlier row (new installs, or the orphan side of an anti-join)",
                "%d" % int((~Cl.loc[Cl["sdk_version"] == "9.4.2", "client_id"].isin(set(older["client_id"]))).sum())))
    tod = Cl["first_batch"].dt.hour
    out.append(("batch clock: UTC in the file, read in Copenhagen time as the asking sentence says; hours seen",
                "%d to %d" % (tod.min(), Cl["last_batch"].dt.hour.max())))
    pop = E.population(Cl)
    late = Cl[(Cl["sdk_version"] == "9.4.1") & ~Cl["client_id"].isin(set(pop))]
    out.append(("9.4.1 client IDs first seen after 6 August (outside the window, dropped)", "%d" % len(late)))
    return out


def golden():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    a = {m: f["record"][V.NAMES[m]]["incidents"] for m in CHECKS}
    d = {k: dict(v) for k, v in f["sdk941"].items()}
    return f, a, d


def score_a(a, ga):
    return sum(a[m] == ga[m] for m in CHECKS)


def score_d(d, gd):
    return sum(d[k][p] == gd[k][p] for k in gd for p in ("ios", "android"))


def pair(kc, km, n):
    c = REC + INS + ASK * kc / n
    s = OFF + INS + ASK * km / n
    return c, s, (c + s) / 2.0


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    L = load(folder)
    f, ga, gd = golden()
    n = {"A": 5, "D": 2 * len(gd)}
    N = sum(n.values())
    cr = call(L, "delta")
    mi = call(L, "naive")
    on_call = V.NAMES[cr["pick"]] == f["call"] and "%.2f" % cr["line"] == f["line"]
    off_call = V.NAMES[mi["pick"]] != f["call"]
    print("cracker's call: %s at %.2f points (%s the golden)" % (V.NAMES[cr["pick"]], cr["line"], "lands" if on_call else "MISSES"))
    print("mirror's call (the default path, sessions as independent draws): %s at %.2f points (%s)" % (
        V.NAMES[mi["pick"]], mi["line"], "off the call" if off_call else "ON THE CALL"))
    if not (on_call and off_call):
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1
    Cl = E.load_clients(folder)
    print("\nthe cracker's hygiene battery on the client summary:")
    for k, v in battery(Cl):
        print("  %-96s %s" % (k, v))
    full_d = V.sdk941(folder)
    full = dict(A=score_a({m: cr["rec"][m][0] for m in CHECKS}, ga), D=score_d(full_d, gd))
    if full != n:
        print("CONTROL FAILED: the full includer keeps %s of %s; the route code does not reproduce figures.json" % (full, n))
        return 1
    natural = E.still_on(Cl, {})                       # a client ID is an install
    kc = dict(A=score_a({m: cr["rec"][m][0] for m in CHECKS}, ga), D=score_d(natural, gd))
    km = dict(A=score_a({m: mi["rec"][m][0] for m in CHECKS}, ga), D=score_d(natural, gd))
    stops = {"an install silent for a week read as gone": E.still_on(Cl, {}, silent_days=7),
             "a stopped 9.4.1 client ID joined to the next new 9.4.2 client ID (timing)": E.still_on(Cl, E.timing_links(Cl)),
             "every 9.4.1 client ID, whenever it first sent, with the sequence join": E.still_on(
                 Cl, E.links(Cl), pop=dict(zip(Cl.loc[Cl["sdk_version"] == "9.4.1", "client_id"],
                                               Cl.loc[Cl["sdk_version"] == "9.4.1", "platform"])))}
    print("\nper ask, figures kept:")
    print("  %-44s %-9s %-9s %s" % ("", "cracker", "mirror", "full includer (control)"))
    print("  %-44s %-9d %-9d %d of %d" % ("A, incidents each check would have held", kc["A"], km["A"], full["A"], n["A"]))
    print("  %-44s %-9d %-9d %d of %d" % ("D, SDK 9.4.1 installs still on it each day", kc["D"], km["D"], full["D"], n["D"]))
    tc, tm = sum(kc.values()), sum(km.values())
    print("  %-44s %-9d %-9d %d of %d" % ("all asks", tc, tm, sum(full.values()), N))
    days = sorted(gd)
    show = lambda d: "iOS %s ... %s; Android %s ... %s" % (d[days[0]]["ios"], d[days[-1]]["ios"], d[days[0]]["android"], d[days[-1]]["android"])
    print("\nD by route, 6 August ... 19 August:")
    print("  %-78s %s" % ("figures.json", show(gd)))
    print("  %-78s %s  kept %d of %d" % ("cracker and mirror: a client ID read as an install", show(natural), score_d(natural, gd), n["D"]))
    for k, v in stops.items():
        print("  %-78s %s  kept %d of %d" % ("stop: " + k, show(v), score_d(v, gd), n["D"]))
    print("  %-78s %s  kept %d of %d" % ("full includer: the sequence join (the verifier's code)", show(full_d), full["D"], n["D"]))
    c, sm, p = pair(tc, tm, N)
    print("\nthe sheet's formula (38, 7, 55 over the %d ask figures; r = 5): cracker %.1f, mirror %.1f, pair %.1f" % (N, c, sm, p))
    print("  the mirror running the battery takes the same natural read: mirror %.1f, pair %.1f" % (sm, p))
    print("  if the cracker finds the join (keeps all %d): pair %.1f; if the mirror does too: %.1f" % (
        N, pair(N, tm, N)[2], pair(N, km["A"] + n["D"], N)[2]))
    print("  two careful responses on the call: %.1f" % pair(tc, tc, N)[0])
    print("\nCracker keeps: %d of %d ask figures (A %d of 5 is the call's own construction; the device ask D: %d of %d)"
          % (tc, N, kc["A"], kc["D"], n["D"]))
    print("Mirror leakage: %.1f per cent of ask weight (the same with the battery run; no ask whole)" % (100.0 * tm / N))
    print("Pair ceiling: %.1f (the sheet's formula on the measured keeps)" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
