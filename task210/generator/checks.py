"""task210's generator assertions, run on the shipped seed after build.py has cut target/.

    python3 task210/generator/checks.py          # exit 1 on the first failed assertion

What it asserts: the golden computed from target/ matches the clean truth's slate; every rival reader of the main call
(the five screens, the careful and constructing readers, reader (d) and the literal executions) files a wrong slate;
every semantic fork (SF1 to SF22) prints the same call or is ruled out by a quoted sentence; the separation; removing
each competing cause leaves the slate; the slate holds across the published range of the glare multiplier and the
base rate; the asks' figures equal the flag truth, sit mid-bin and are missed by the cracker; the separation line; the
input gates; Gate G; the metadata scrub.
"""
import json
import os
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import world as W  # noqa: E402
import simulate as S  # noqa: E402
import records as RC  # noqa: E402
import model as M  # noqa: E402
import golden as GD  # noqa: E402
import pack  # noqa: E402

OK = []


def check(name, cond, detail=""):
    print("%s  %s %s" % ("PASS" if cond else "FAIL", name, detail), flush=True)
    if not cond:
        sys.exit(1)
    OK.append(name)


def key(s):
    return {("%s %s" % c) if isinstance(c, tuple) else c for c in s}


def main():
    T = S.simulate(seed=W.SEED)
    P = T["passes"]
    Rr = RC.records(T, W.SEED)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    gold = set(fig["slate"])

    # ---------------- the golden and the truth
    truth = key(M.slate(M.truth_rates(T)))
    clean, Gc = M.golden(P)
    check("golden from target/ equals the truth slate", gold == truth, sorted(gold))
    check("golden on the clean truth equals the truth slate", key(M.slate(clean)) == truth)
    check("separation: the fourth slot clears the fifth by 10 per cent or more", fig["separation_pct"] >= 10.0,
          "%.1f per cent (%s at %.2f against %.2f)" % (fig["separation_pct"], fig["fifth_cell"], fig["fourth_rate"], fig["fifth_rate"]))

    # ---------------- the five screens and the readers (the main call's rivals), on the clean truth
    for name, fn in {**M.READERS, **M.LITERAL}.items():
        sh = len(key(M.slate(fn(P))) & gold)
        check("reader %s files a wrong slate" % name, sh < 4, "shares %d of 4" % sh)

    # ---------------- the semantic fork table: every reading of a term or convention prints the same call
    variants = [
        ("SF7 entry", dict(at="entry")), ("SF8 nearest", dict(sky="nearest")), ("SF8 next hour", dict(sky="next")),
        ("SF9 by time", dict(assign="time")), ("SF10 sunset", dict(dark_at=-0.833)), ("SF10 minus 3", dict(dark_at=-3.0)),
        ("SF10 civil", dict(dark_at=-6.0)), ("SF11 cone 15", dict(cone=15.0)), ("SF11 cone 20", dict(cone=20.0)),
        ("SF11 cone 30", dict(cone=30.0)), ("SF11 cone 35", dict(cone=35.0)), ("SF12 box 15", dict(efull=15.0, ezero=15.0)),
        ("SF12 box 20", dict(efull=20.0, ezero=20.0)), ("SF12 8 to 20", dict(efull=8.0, ezero=20.0)),
        ("SF12 15 to 30", dict(efull=15.0, ezero=30.0)), ("SF13 linear", dict(shape="lin", cone=30.0)),
        ("SF13 box", dict(shape="box", cone=20.0)), ("SF14 no controls", dict(controls=())), ("SF14 no hour", dict(hourfe=False)),
    ]
    A, sec, lat, lon = GD.passes()
    X = GD.pick_passes(sec, GD.pick(), lat, lon)
    ps = GD.normals_sunshine()
    for sf, kw in variants:
        r, G, _ = GD.main_call(**kw)
        check("%s prints the same call" % sf, key(GD.slate(r)) == gold)
    coef, G = GD.fit(A)
    base = GD.project(coef, G, X, ps)
    expo = pd.Series(GD.glare(X["elev"].values, X["az"].values, X["bearing"].values) * 0.68).groupby(
        [X["sd"].values, X["peak"].values]).mean()
    check("stated facts alone (SRM-07 3.8's low sun on the pick at the normals) file a wrong slate",
          len(key(GD.slate(expo)) & gold) < 4, "shares %d of 4" % len(key(GD.slate(expo)) & gold))
    mm = P[P["peak"] != "OFF"].groupby(["sd", "peak", "month"])["n_fb"].agg(["sum", "size"]).reset_index()
    rs = mm[mm["month"] == 9].set_index(["sd", "peak"])
    ro = mm[mm["month"] == 10].set_index(["sd", "peak"])
    step = ro["sum"] / ro["size"] * 1000 + (ro["sum"] / ro["size"] - rs["sum"] / rs["size"]) * 3500
    check("reader f (September to October trend carried to January) files a wrong slate", len(key(M.slate(step)) & gold) < 4)
    # SF1: a pass counted per car (two-car trains twice) rather than per train
    share2 = 2.0 / 9.0     # two of the nine Juniper blocks run two cars through both peaks
    r1 = base.copy()
    for k in r1.index:
        if k[0].startswith("J"):
            r1[k] = r1[k] / (1 + share2)
    check("SF1 a pass per car instead of per train prints the same call", key(GD.slate(r1)) == gold)
    # SF2: emergency applications counted as firm brakes too
    E = pd.read_csv(GD.path("edr"))
    Eb = E[E["event_code"].isin(["FB", "EB"])].copy()
    Eb["t"] = GD.to_local(Eb["event_time_utc"])
    Eb["car"] = Eb["car"].astype("int64")
    A2 = A.copy()
    A2["n_fb"] = GD._attach(A2, Eb, sec, "position")
    c2, G2 = GD.fit(A2)
    check("SF2 firm brakes plus emergency applications prints the same call", key(GD.slate(GD.project(c2, G2, X, ps))) == gold)
    # SF3: peak membership by the pass's midpoint or exit instead of its entry
    for col in ("mid", "exit"):
        Xm = X.copy()
        t = Xm["enter"] + (Xm["exit"] - Xm["enter"]) / 2 if col == "mid" else Xm["exit"]
        m = t.dt.hour * 60 + t.dt.minute
        Xm["peak"] = np.where((m >= 390) & (m < 540), "AM", np.where((m >= 960) & (m < 1110), "PM", "OFF"))
        rr = GD.project(coef, G, Xm[Xm["peak"] != "OFF"].reset_index(drop=True), ps)
        check("SF3 peak by the pass's %s prints the same call" % col, key(GD.slate(rr)) == gold)
    # SF4: the weather basis: the normals' 68 per cent, a sunless pick, or every hour sunny
    for v in (0.5, 0.9, 1.0):
        rr = GD.project(coef, G, X, {m: v for m in range(1, 13)})
        check("SF4 sunshine share %.2f prints the same call" % v, key(GD.slate(rr)) == gold)
    # SF5: per pass rather than per 1,000 passes (a scale)
    check("SF5 the rate's scale prints the same call", key(GD.slate(base / 1000)) == gold)
    # SF6: the two holidays kept as weekdays
    pk = GD.pick()
    pk2 = dict(pk, holidays=[])
    X6 = GD.pick_passes(sec, pk2, lat, lon)
    check("SF6 the holidays read as weekdays prints the same call", key(GD.slate(GD.project(coef, G, X6, ps))) == gold)
    # SF15: firm brakes on passes the AVL log lost, assigned by position and counted against the logged passes
    unmatched = int((E["event_code"] == "FB").sum()) - int(A["n_fb"].sum())
    wk = A["service_date"].between("2026-06-08", "2026-06-14")
    c15, G15 = GD.fit(A[~wk].reset_index(drop=True))
    check("SF15 the detector outage week dropped from every section prints the same call (%d FB records on unlogged passes)"
          % unmatched, key(GD.slate(GD.project(c15, G15, X, ps))) == gold)
    # SF16 to SF18 are ruled out by sentences (checked as text below); the CSV grain is the section-direction peak
    csv = pd.read_csv(os.path.join(TASK, "golden", "slot_plan_jan_feb_2027.csv"))
    check("SF17 the slot plan's grain is the section-direction peak (SRM-07 3.6)", len(csv) == 52 and
          (csv["restricted_speed_slot"] == "yes").sum() == W.CAP)
    srm = GD.pdfplumber.open(GD.path("srm")).pages[0].extract_text()
    for sf, phrase in (("SF16", "Mountain local time"), ("SF17", "One section, in one direction of travel, in one weekday peak"),
                       ("SF18", "at the pick's scheduled times on the pick's weekdays")):
        check("%s SRM-07 carries the closing sentence" % sf, phrase.replace(" ", "") in srm.replace("\n", "").replace(" ", ""), phrase)

    # ---------------- competing causes removed and the calibration range, on the same realization (clean truth)
    rng = np.random.default_rng(210)
    street = (P["track"] == "street").values

    def thinned(keep):
        Q = P.copy()
        Q["n_fb"] = rng.binomial(P["n_fb"].values, np.clip(keep, 0, 1))
        return Q

    def topped(extra):
        Q = P.copy()
        Q["n_fb"] = P["n_fb"].values + rng.poisson(np.clip(extra, 0, None))
        return Q

    gl = P["glare"].values * P["sun"].values
    causes = {"new operators": 1 / (1 + W.NEW_OP * P["newop"].values),
              "school mornings": 1 / (1 + np.where(street, W.SCHOOL, 0.0) * P["school_am"].values),
              "darkness": 1 / (1 + np.where(street, W.DARK["street"], W.DARK["reserved"]) * P["dark"].values)}
    for name, keep in causes.items():
        check("removing %s leaves the slate" % name, key(M.slate(M.golden(thinned(keep))[0])) == gold)
    for g in (1.2, 3.5):
        ratio = (1 + g * gl) / (1 + W.G_TRUE * gl)
        Q = thinned(ratio) if g < W.G_TRUE else topped(P["p_fb"].values * (ratio - 1))
        check("full-alignment multiplier %.1f keeps the slate" % (1 + g), key(M.slate(M.golden(Q)[0])) == gold)
    for b in (12.0, 30.0):
        Q = thinned(np.full(len(P), b / 20.0)) if b < 20 else topped(P["p_fb"].values * (b / 20.0 - 1))
        check("base rate %.0f per 1,000 keeps the slate" % b, key(M.slate(M.golden(Q)[0])) == gold)

    # ---------------- the asks
    a_truth = {("Juniper" if l == "J" else "Foundry") + " %02d" % m: int(v) for (l, m), v in Rr["eb_truth"].items()}
    check("ask A golden equals the flag truth", fig["ask_a"] == a_truth)
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    check("SF19 the asking sentence files the Mountain-time month (the UTC month moves %d figures)"
          % sum(GD.ask_a(month="utc")[k] != v for k, v in fig["ask_a"].items()), "Mountain" in prompt)
    for cls, name in (("26-2", "May"), ("26-3", "August")):
        n, h, r = Rr["os_truth"][cls]
        b = fig["ask_b"][name]
        check("ask B %s equals the flag truth" % name, (b["overspeeds"], b["hours_exact"]) == (n, h))
        for v, bin_ in ((b["hours_exact"], 0.1), (b["rate_exact"], 0.1)):
            f = (v / bin_) % 1.0
            check("ask B %s figure %.4f sits mid-bin" % (name, v), abs(f - 0.5) >= 0.07,
                  "%.0f per cent of the bin from the rounding edge" % (100 * abs(f - 0.5)))
    check("SF20 ask B by calendar day equals the service-day figures", GD.ask_b(date="calendar") == fig["ask_b"])
    t = GD.to_local(E["event_time_utc"])
    edge = (((t - t.dt.normalize()).dt.total_seconds() < 15) & (t.dt.day == 1)) | \
           (((t.dt.normalize() + pd.Timedelta(days=1) - t).dt.total_seconds() < 15) & ((t + pd.Timedelta(days=1)).dt.day == 1))
    check("SF21 no EB or OS record within 15 s of a month boundary", int((edge & E["event_code"].isin(["EB", "OS"])).sum()) == 0)
    check("SF22 the asking sentence counts the 30 days from each operator's first day in revenue service",
          "30 days from" in prompt)
    import ceiling
    cm = ceiling.main(TARGET)
    check("pair ceiling at or under 60", cm["pair"] <= 60.0, "%.1f" % cm["pair"])
    print("REPORT pair with both on the call %.1f" % cm["both_on"])
    check("full includer keeps at most two fifths", cm["full"] <= 40.0, "%.1f per cent" % cm["full"])
    check("the cracker misses ask A and ask B", cm["leak"] <= 20.0, "%.1f per cent kept" % cm["leak"])

    # ---------------- the separation line, counted on the shipped rows
    Y = pd.read_csv(GD.path("yard"))
    Y["sday"] = pd.to_datetime(Y["sheet_date"], format="%m/%d/%Y")
    trail = {(d, int(c.split("+")[1])) for d, c in zip(Y["sday"], Y["pullout_cars"].astype(str)) if "+" in c}
    fb = E[E["event_code"] == "FB"].copy()
    fb["sday"] = (GD.to_local(fb["event_time_utc"]) - pd.Timedelta(hours=3)).dt.normalize()
    on_trail = sum((d, int(c)) in trail for d, c in zip(fb["sday"], fb["car"]))
    check("no firm brake on a trailing car's recorder", on_trail == 0)
    rel = pd.read_csv(os.path.join(TARGET, pack.FILES["releases"]))
    rel["released"] = pd.to_datetime(rel["released"])
    fbt = GD.to_local(fb["event_time_utc"])
    x = pd.DataFrame({"car": fb["car"].values, "t": fbt.values}).merge(rel[["car", "released"]], on="car")
    check("no firm brake inside a depot running test", int(((x["t"] >= x["released"]) & (x["t"] <= x["released"] + pd.Timedelta(minutes=60))).sum()) == 0)

    # ---------------- input gates, Gate G and the metadata scrub
    files = sorted(os.listdir(TARGET))
    exts = {os.path.splitext(f)[1] for f in files}
    check("ten or more input files", len(files) >= 10, str(len(files)))
    check("three or more formats", len(exts) >= 3, str(sorted(exts)))
    import pyarrow.parquet as pq
    check("a file of 25,000 or more rows", pq.ParquetFile(os.path.join(TARGET, pack.FILES["avl"])).metadata.num_rows >= 25000)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("two or more distractors named in metadata.json", len(meta["distractors"]) >= 2 and
          all(d in files for d in meta["distractors"]))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, pack.FILES["dash"]))
    cells = " ".join(str(c.value) for ws in wb for row in ws.iter_rows() for c in row if c.value is not None)
    check("Gate G: the dashboard names no section and ranks nothing", not any(s[0] in cells.split() for s in W.SECTIONS))
    check("H1: workbook properties carry no author", not wb.properties.creator and not wb.properties.lastModifiedBy)
    for f in files:
        if f.endswith(".pdf"):
            m = GD.pdfplumber.open(os.path.join(TARGET, f)).metadata
            check("H1: %s carries no producer or creator" % f, not m.get("Producer") and not m.get("Creator"))
    check("H1: the parquet carries no pandas schema", b"pandas" not in (pq.read_schema(os.path.join(TARGET, pack.FILES["avl"])).metadata or {}))
    z = zipfile.ZipFile(os.path.join(TASK, "target.zip"))
    check("target.zip holds exactly target/", sorted(n.split("/", 1)[1] for n in z.namelist()) == files)
    print("ALL %d CHECKS PASS" % len(OK))


if __name__ == "__main__":
    main()
