"""task210's generator assertions, run on the shipped seed after build.py has cut target/.

    python3 task210/generator/checks.py          # exit 1 on the first failed assertion

What it asserts: the golden computed from target/ matches the clean truth's slate; every rival reader of the main call
(the first look, the careful and constructing readers, reader (d), reader (f) and the literal execution of SRM-07, which
files no definition of low sun) files a wrong slate sharing at most two slots with the golden; no shipped document names
the sun as a hazard; every semantic fork (SF1 to SF26) prints the same call or is ruled out by a quoted sentence; the
C3 corridor (the slate under every cone from 15 to 35 degrees, every elevation profile and every shape of the glare
term, with the fourth slot's separation from the fifth under each); the separation; removing each competing cause
leaves the slate; the slate holds across the published range of the glare multiplier and the base rate; the asks'
figures equal the flag truth, every reading their filed words admit counts one set and the ceiling holds on the cut
pack (asks()); the separation line; the input gates; Gate G; the
metadata scrub; the realism sweep on target/ (realism 1 to 8: ids, timestamps, counts, orderings, constant columns,
document stamps, readers and margins, no describing file); the client's three rules (R1 to R3c); and submission.md's
SOLUTION_STEPS executed as written, each step's stated figure asserted.
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
FLOOR = 10.0     # per cent: the fourth slot's separation from the fifth in every corridor cell
SUPPORT = 10.0   # twice the log-likelihood from the best-fitting glare form: the forms the record supports


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

    # ---------------- the external solar anchor: solar.py (which builds the pack and the golden) against NOAA's solar
    # calculator equations (solar_ref.py, a separate implementation the generator never imports), within TOL_DEG
    import datetime as _dt
    import solar_ref as SR
    from solar import sun_position as _sp

    def _gen(t):
        e_, a_ = _sp(np.array([np.datetime64(t.strftime("%Y-%m-%dT%H:%M:%S"))], dtype="datetime64[s]"), W.LAT0, W.LON0)
        return float(e_[0]), float(a_[0])

    def _dang(a_, b_):
        return abs(((a_ - b_ + 180.0) % 360.0) - 180.0)

    worst = 0.0
    for day in (_dt.date(2026, 6, 21), _dt.date(2026, 12, 21), _dt.date(2027, 1, 15)):
        for t_ in SR.rise_set(day, W.LAT0, W.LON0):
            e0, a0 = SR.sun(t_, W.LAT0, W.LON0)
            e1, a1 = _gen(t_)
            worst = max(worst, _dang(a0, a1), abs(e0 - e1))
    rs = SR.rise_set(_dt.date(2026, 6, 21), W.LAT0, W.LON0)
    check("solar anchor: the 21 June sunset lies north-west (azimuth 295 to 305 by the reference, %.1f by solar.py)"
          % _gen(rs[1])[1], 295 <= SR.sun(rs[1], W.LAT0, W.LON0)[1] <= 305 and 295 <= _gen(rs[1])[1] <= 305)
    check("solar anchor: sunrise and sunset azimuth and elevation on 21 June, 21 December and 15 January agree with NOAA's "
          "solar calculator within %.1f degrees" % SR.TOL_DEG, worst <= SR.TOL_DEG, "largest difference %.2f" % worst)
    worst = 0.0
    for hh, mm in ((14, 30), (15, 30), (23, 0), (23, 45)):          # 07:30, 08:30, 16:00 and 16:45 MST on 15 January 2027
        t_ = _dt.datetime(2027, 1, 15, hh, mm)
        e0, a0 = SR.sun(t_, W.LAT0, W.LON0)
        e1, a1 = _gen(t_)
        for brg in (125.0, 231.0):                                  # J4 outbound, F5 outbound (the survey's bearings)
            worst = max(worst, abs(_dang(a0, brg) - _dang(a1, brg)))
        worst = max(worst, _dang(a0, a1), abs(e0 - e1))
    check("solar anchor: the January peak hours' sun (07:30, 08:30, 16:00, 16:45 MST) and its offset from the J4 and F5 "
          "outbound bearings agree with NOAA's solar calculator within %.1f degrees" % SR.TOL_DEG, worst <= SR.TOL_DEG,
          "largest difference %.2f" % worst)

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
        check("reader %s files a wrong slate, sharing at most two slots" % name, sh <= 2, "shares %d of 4" % sh)

    # ---------------- the semantic fork table: every reading of a term or convention prints the same call
    A, sec, lat, lon = GD.passes()
    X = GD.pick_passes(sec, GD.pick(), lat, lon)
    ps = GD.normals_sunshine()
    for sf, kw in (("SF7 entry", dict(at="entry")), ("SF8 nearest", dict(sky="nearest")), ("SF8 next hour", dict(sky="next")),
                   ("SF9 by time", dict(assign="time"))):
        r, G, _ = GD.main_call(**kw)
        check("%s prints the same call" % sf, key(GD.slate(r)) == gold)

    def call(**kw):
        fk = {k: v for k, v in kw.items() if k in ("cone", "efull", "ezero", "shape", "dark_at", "controls", "hourfe")}
        pk = {k: v for k, v in kw.items() if k in ("cone", "efull", "ezero", "shape", "dark_at")}
        c_, g_ = GD.fit(A, **fk)
        return GD.project(c_, g_, X, ps, **pk).sort_values(ascending=False)

    for sf, kw in (("SF10 sunset", dict(dark_at=-0.833)), ("SF10 minus 3", dict(dark_at=-3.0)), ("SF10 civil", dict(dark_at=-6.0)),
                   ("SF14 no controls", dict(controls=())), ("SF14 no hour", dict(hourfe=False))):
        check("%s prints the same call" % sf, key(GD.slate(call(**kw))) == gold)
    # SF11 to SF13, the corridor. No shipped sentence defines low sun, so the glare term's cone, elevation profile and
    # shape are the analyst's, and the record decides them: every form the record supports (twice the log-likelihood
    # within SUPPORT of the best-fitting form) prints the golden slate, and every form that prints another slate is
    # refuted by the record (at least SUPPORT worse). The grid: cones 15 to 35, five elevation profiles, three shapes.
    import statsmodels.api as sm
    from scipy.optimize import minimize_scalar

    def fit_ll(cone, ef, ez, shape):
        d_ = pd.DataFrame({"sd": A["sd"].values, "hour": A["hour"].values, "wkend": A["wkend"].values,
                           "dark": (A["elev"].values < 0).astype(float), "y": A["n_fb"].values})
        d_["gs"] = GD.glare(A["elev"].values, A["az"].values, A["bearing"].values, cone, ef, ez, shape) * A["sun"].values
        c_ = d_.groupby(["sd", "hour", "wkend", "dark"], as_index=False).agg(y=("y", "sum"), n=("y", "size"), s=("gs", "sum"))
        Xd = pd.concat([pd.get_dummies(c_["sd"], prefix="sd").astype(float),
                        pd.get_dummies(c_["hour"].astype(str), prefix="h", drop_first=True).astype(float),
                        c_[["wkend", "dark"]]], axis=1)
        nll = lambda g: -sm.GLM(c_["y"].values, Xd.values, family=sm.families.Poisson(),
                                offset=np.log(c_["n"].values + g * c_["s"].values)).fit().llf
        r_ = minimize_scalar(nll, bounds=(0.0, 10.0), method="bounded", options={"xatol": 0.002})
        m_ = sm.GLM(c_["y"].values, Xd.values, family=sm.families.Poisson(),
                    offset=np.log(c_["n"].values + r_.x * c_["s"].values)).fit()
        return dict(zip(Xd.columns, m_.params)), r_.x, -r_.fun

    cells = []
    for shape in ("cos2", "lin", "box"):
        for cone in (15.0, 20.0, 25.0, 30.0, 35.0):
            for ef, ez in ((12.0, 25.0), (15.0, 15.0), (20.0, 20.0), (8.0, 20.0), (15.0, 30.0)):
                c_, g_, ll = fit_ll(cone, ef, ez, shape)
                r = GD.project(c_, g_, X, ps, cone=cone, efull=ef, ezero=ez, shape=shape).sort_values(ascending=False)
                cells.append(dict(shape=shape, cone=cone, ef=ef, ez=ez, ll=ll, same=key(set(r.index[:4])) == gold,
                                  sep=100 * (r.iloc[3] / r.iloc[4] - 1)))
    best = max(c["ll"] for c in cells)
    for c in cells:
        c["d2"] = 2 * (best - c["ll"])
    sup = [c for c in cells if c["d2"] <= SUPPORT]
    off = [c for c in cells if not c["same"]]
    adm = [c for c in cells if not (c["shape"] == "box" and c["cone"] >= 25)]
    check("SF11 SF12 SF13 corridor: the golden slate under every tapering form at cones 15 to 35 and every elevation "
          "profile, and every flat form to 20 degrees (%d cells)" % len(adm), all(c["same"] for c in adm),
          "off the slate: %s" % [(c["shape"], c["cone"], c["ef"], c["ez"]) for c in adm if not c["same"]])
    lo = min(adm, key=lambda c: c["sep"])
    check("corridor separation: the fourth slot clears the fifth by %.1f per cent or more in every corridor cell" % FLOOR,
          lo["sep"] >= FLOOR, "tightest %.1f per cent (%s, cone %.0f, full below %.0f, none from %.0f)" % (
              lo["sep"], lo["shape"], lo["cone"], lo["ef"], lo["ez"]))
    check("SF11 SF12 SF13 every form the record supports prints the golden slate (%d of %d within %.0f of the best fit)"
          % (len(sup), len(cells), SUPPORT), all(c["same"] for c in sup))
    check("SF11 SF12 SF13 every form that prints another slate is refuted by the record (%d cells, all flat from 25 "
          "degrees, each worse than %.0f)" % (len(off), SUPPORT),
          all(c["d2"] > SUPPORT and c["shape"] == "box" and c["cone"] >= 25 for c in off),
          "nearest %.1f" % min(c["d2"] for c in off) if off else "none")
    offd = np.abs(((A["az"] - A["bearing"] + 180.0) % 360.0) - 180.0)
    lowm = (A["elev"] > 0) & (A["elev"] < 20) & (A["sun"] == 1)
    refr = A[~lowm & (A["elev"] > 0)].groupby("sd")["n_fb"].mean()
    expv = A["sd"].map(refr)

    def excess(a, b):
        m = lowm & (offd >= a) & (offd < b)
        return A.loc[m, "n_fb"].sum() / expv[m].sum() - 1

    e_axis, e_wide = excess(0, 10), excess(20, 35)
    check("SF13 the record's excess is gone by 20 degrees off the line of travel (a flat response from 25 degrees out "
          "is refuted): the excess at 20 to 35 degrees is under a fifth of the excess at 0 to 10",
          e_wide < 0.2 * e_axis, "excess %.2f on the axis, %.2f at 20 to 35 degrees" % (e_axis, e_wide))
    coef, G = GD.fit(A)
    base = GD.project(coef, G, X, ps)
    # the literal execution of SRM-07 (no definition of low sun filed), from target/: each section-direction peak's
    # record rate since 1 April (4.2), and that rate at the normals' sunshine for the pick's weeks (4.1)
    m_ = A["enter"].dt.hour * 60 + A["enter"].dt.minute
    A["peak"] = np.where((m_ >= 390) & (m_ < 540), "AM", np.where((m_ >= 960) & (m_ < 1110), "PM", "OFF"))
    Wk = A[(A["wkend"] == 0) & (A["peak"] != "OFF")]
    lx1 = Wk.groupby(["sd", "peak"])["n_fb"].mean() * 1000
    t_ = Wk.groupby(["sd", "peak", "sun"])["n_fb"].mean().unstack("sun")
    lx2 = (t_.get(1.0, 0) * 0.68 + t_.get(0.0, 0) * 0.32) * 1000
    for name, r in (("LX1 the record's rate", lx1), ("LX2 the rate at the normals' sunshine", lx2)):
        sh = len(key(GD.slate(r)) & gold)
        check("literal execution of SRM-07 from target/, %s, files a wrong slate sharing at most two slots" % name, sh <= 2,
              "shares %d of 4" % sh)
    # no shipped document names the sun as a hazard (the normals define possible sunshine, a climate statistic)
    import re as _re
    texts = {"prompt.txt": open(os.path.join(TASK, "prompt.txt")).read()}
    for f in sorted(os.listdir(TARGET)):
        if f.endswith(".pdf"):
            texts[f] = "\n".join(pg.extract_text() or "" for pg in GD.pdfplumber.open(os.path.join(TARGET, f)).pages)
    hits = {f: _re.findall(r"glare|low sun|low-sun|dazzl|azimuth|solar|sun angle|sun position|sun's position|sunlight|"
                           r"in the sun|the sun ahead|blind", t, _re.I) for f, t in texts.items()}
    hits = {f: h for f, h in hits.items() if h}
    check("no shipped document or the prompt names low sun, glare or the sun's position", not hits, str(hits))
    check("SRM-07 names the sun nowhere", "sun" not in texts["SRM-07_seasonal_restricted_speed_orders.pdf"].lower())
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
    srm0 = GD.pdfplumber.open(GD.path("srm")).pages[0].extract_text().replace("\n", " ")
    check("SF1 a pass counted per car instead of per train shares %d of 4 with the golden; SRM-07 3.3 rules it out"
          % len(key(GD.slate(r1)) & gold), "whether the train runs as one car or two" in srm0)
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
    asks(fig, Rr, E)

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
    realism_sweep(files)
    realism_blocks(P, Rr)
    three_rules(T, Rr, P, gold, A, sec, lat, lon, X, ps, coef, G)
    literal_steps(gold)
    print("ALL %d CHECKS PASS" % len(OK))


def realism_blocks(P, Rr):
    """realism 9: every block works its day the way a streetcar block does, on the clean truth and in target/ as shipped.
    Out and back from its pull-out, with a layover at each terminal; pull-outs and pull-ins at the outer end (Union Yard,
    the Foundry depot at Foundry Loop); a bad-ordered car pulls in at Foundry Loop and the spare takes the block's next
    inbound trip; operators relieve each other at the outer end between trips; J01 and J02 couple and uncouple in Union
    Yard; as many blocks as each day type's timetable needs."""
    # the clean truth: the schedule's own blocks
    tr = P.drop_duplicates("trip")[["date", "daytype", "line", "dir", "dep_min", "block", "run", "cars"]]
    tr = tr.sort_values(["date", "block", "dep_min"]).reset_index(drop=True)
    g = tr.groupby(["date", "block"])
    check("realism 9: on the schedule every block runs out and back (no block-day repeats a direction)",
          int((g["dir"].shift() == tr["dir"]).sum()) == 0)
    rr = S.section_runs(S.geometry())
    R = {(ln, d): sum(x for _, x in rr[(ln, d)]) / 60.0 for ln in ("J", "F") for d in ("O", "I")}
    nxt = g["dep_min"].shift(-1)
    lay = (nxt - tr["dep_min"] - [R[(ln, d)] for ln, d in zip(tr["line"], tr["dir"])]).dropna()
    check("realism 9: scheduled layovers at the terminals run 9.9 to 27.6 minutes (Foundry 9.9 at each end, Juniper 12.6 or "
          "more at Mesa Park and 20.1 or more at Union Yard)", 9.8 <= lay.min() and lay.max() <= 27.7,
          "%.1f to %.1f" % (lay.min(), lay.max()))
    nb = tr.groupby(["daytype", "date"])["block"].nunique().groupby(level=0).agg(["min", "max"])
    check("realism 9: blocks per day follow the timetable (17 on weekdays, 13 on Saturdays, 9 on Sundays and holidays)",
          nb.loc["weekday"].tolist() == [17, 17] and nb.loc["saturday"].tolist() == [13, 13] and nb.loc["sunday"].tolist() == [9, 9],
          str(nb.to_dict()))
    runs = g["run"].nunique()
    last_e = tr[tr["run"].str.endswith("E")].groupby(["date", "block"])["dir"].last()
    first_l = tr[tr["run"].str.endswith("L")].groupby(["date", "block"])["dir"].first()
    check("realism 9: every block-day has an early and a late run, the early run ending on an outbound trip into the outer "
          "end and the late run starting on the inbound trip out of it (the relief at Union Yard or Foundry Loop)",
          (runs == 2).all() and (last_e == "O").all() and (first_l == "I").all())
    two = tr[tr["cars"] == 2]
    ok2 = True
    for (d, b), x in two.groupby(["date", "block"]):
        for a, z in W.TWO_CAR["J"]:
            w = x[(x["dep_min"] >= a) & (x["dep_min"] < z)]
            ok2 &= len(w) > 0 and w["dir"].iloc[0] == "I" and w["dir"].iloc[-1] == "O"
    wk = tr[(tr["line"] == "J") & (tr["daytype"] == "weekday") & tr["block"].isin(W.TWO_CAR_BLOCKS)]
    inwin = np.zeros(len(wk), dtype=bool)
    for a, z in W.TWO_CAR["J"]:
        inwin |= ((wk["dep_min"] >= a) & (wk["dep_min"] < z)).values
    check("realism 9: J01 and J02 run coupled on exactly their weekday trips leaving 06:30 to 09:29 and 15:30 to 18:44, each "
          "window opening inbound out of Union Yard and closing outbound into it (the trailing car couples in the yard)",
          ok2 and bool(((wk["cars"] == 2).values == inwin).all()) and set(two["block"]) == set(W.TWO_CAR_BLOCKS))
    # target/ as shipped
    av = pd.read_parquet(os.path.join(TARGET, pack.FILES["avl"]))
    av["block"] = av["block"].astype(str)
    av["direction"] = av["direction"].astype(str)
    t2 = av.groupby(["service_date", "trip_id"], as_index=False).agg(block=("block", "first"), dirn=("direction", "first"),
                                                                      veh=("vehicle", "first"), nveh=("vehicle", "nunique"),
                                                                      t0=("enter_local", "min"), t1=("exit_local", "max"))
    t2 = t2.sort_values(["service_date", "block", "t0"]).reset_index(drop=True)
    g2 = t2.groupby(["service_date", "block"])
    gap = (t2["t0"] - g2["t1"].shift()).dt.total_seconds() / 60
    rep = g2["dirn"].shift() == t2["dirn"]
    check("realism 9: in the AVL log no block-day repeats a direction except across an onboard unit's drop-out (a gap of "
          "more than a round trip: %d repeats)" % int(rep.sum()), bool((gap[rep] > 45).all()), "shortest %.0f min" % gap[rep].min())
    turn = gap[~rep & gap.notna()]
    check("realism 9: every turn at a terminal in the AVL log leaves the car two minutes or more", turn.min() >= 2.0 - 1 / 60,
          "shortest %.2f min" % turn.min())
    Y = pd.read_csv(os.path.join(TARGET, pack.FILES["yard"]))
    Y["service_date"] = pd.to_datetime(Y["sheet_date"], format="%m/%d/%Y").dt.date
    Y["lead"] = Y["pullout_cars"].astype(str).str.split("+").str[0].astype(int)
    f1 = g2.first().reset_index()[["service_date", "block", "veh"]]
    f1["service_date"] = pd.to_datetime(f1["service_date"]).dt.date
    mj = f1.merge(Y[["service_date", "block", "lead"]], on=["service_date", "block"], how="outer", indicator=True)
    check("realism 9: the yard sheet lists exactly the blocks the AVL log shows each day, each block's first trip on its "
          "pull-out car", bool((mj["_merge"] == "both").all()) and bool((mj["veh"] == mj["lead"]).all()), "%d block-days" % len(mj))
    wkd = GD.weekday_service()
    plus = Y[Y["pullout_cars"].astype(str).str.contains(r"\+")]
    check("realism 9: trailing cars are on the yard sheet only on weekday-timetable days, for J01 and J02",
          all(pd.Timestamp(d) in wkd for d in plus["service_date"]) and set(plus["block"]) == set(W.TWO_CAR_BLOCKS))
    ch = t2[(g2["veh"].shift().notna()) & (t2["veh"] != g2["veh"].shift())]
    prevdir = g2["dirn"].shift()[ch.index]
    check("realism 9: a car changes on a block only at Foundry Loop, between an outbound trip and the next inbound one, "
          "never inside a trip (%d changes)" % len(ch), (ch["dirn"] == "IB").all() and (prevdir == "OB").all()
          and ch["block"].str.startswith("F").all() and int((t2["nveh"] > 1).sum()) == 0)
    rel = pd.read_csv(os.path.join(TARGET, pack.FILES["releases"]))
    rel["released"] = pd.to_datetime(rel["released"])
    lastp = av.groupby([pd.to_datetime(av["service_date"]), av["vehicle"].astype(int)])["exit_local"].max()
    after = [r.released > lastp.get((r.released.normalize(), int(r.car)), pd.Timestamp("2000-01-01")) for r in rel.itertuples()]
    check("realism 9: each released car was released after its last pass that day (it had pulled in)", all(after), "%d releases" % len(rel))
    # reliefs: no trip's recorder events carry two operators
    E = pd.read_csv(os.path.join(TARGET, pack.FILES["edr"]), dtype={"operator_badge": str})
    cards = pd.read_csv(os.path.join(TARGET, pack.FILES["cards"]), dtype={"badge": str}).drop_duplicates("badge")
    E = E.merge(cards[["badge", "operator_no"]], left_on="operator_badge", right_on="badge", how="left")
    E["t"] = GD.to_local(E["event_time_utc"]).astype("datetime64[ns]")
    E["car"] = E["car"].astype("int64")
    pp = av[["vehicle", "trip_id", "service_date", "enter_local", "exit_local"]].copy()
    pp["vehicle"] = pp["vehicle"].astype("int64")
    pp["enter_local"] = pp["enter_local"].astype("datetime64[ns]")
    pp["exit_local"] = pp["exit_local"].astype("datetime64[ns]")
    x = pd.merge_asof(E.sort_values("t"), pp.sort_values("enter_local"), left_on="t", right_on="enter_local", left_by="car",
                      right_by="vehicle", direction="backward")
    x = x[(x["t"] <= x["exit_local"] + pd.Timedelta(seconds=20)).fillna(False)]
    two_ops = x.groupby(["service_date", "trip_id"])["operator_no"].nunique()
    check("realism 9: no trip's recorder events carry two operators (reliefs fall between trips; %d trips with two or more "
          "events)" % int((x.groupby(["service_date", "trip_id"]).size() > 1).sum()), int((two_ops > 1).sum()) == 0)


def asks(fig, Rr, E):
    """Ask A (the streetcar's emergency brake applications in service by Mountain-time month, SRM-07 6.2) and ask B
    (each line's operator cards for brakes, doors and the rest, each on the day it was written if the weekday timetable
    ran, April to October as a whole): the goldens equal the flag truth; every reading the filed words admit counts one
    set; the readings the words rule out are each another figure; the ceiling on the cut pack."""
    import re
    import ceiling
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    srm = re.sub(r"\s+", " ", " ".join((pg.extract_text() or "") for pg in GD.pdfplumber.open(GD.path("srm")).pages))
    # ask A: the golden and the truth
    a_truth = {"%02d" % m: int(v) for m, v in Rr["eb_truth"].items()}
    check("ask A golden equals the flag truth (each application made on a pass, the trailing car's copies, the depot "
          "release tests and the yards' brake checks apart)", fig["ask_a"] == a_truth, str(fig["ask_a"]))
    check("ask A: SRM-07 6.2 files in service from the pull-out onto a block until the pull-in, the depot loop's running "
          "brake test after a release excepted and a two-car train's application one; the prompt asks for applications "
          "in service by Mountain-time month",
          all(x in srm for x in ("in service on a block from the time it pulls out onto the block until it pulls in",
                                 "a running brake test on the depot loop after a release is not one",
                                 "a two-car train's application, which both cars' recorders record (3.4), is one application"))
          and "emergency brake applications in service in each Mountain-time month" in prompt)
    # each record's application: a trailing car's copy belongs to its lead's record
    eb0 = Rr["edr"][Rr["edr"]["code"] == "EB"]
    lead = eb0[~eb0["copy"]].set_index(["date", "block", "t_local"])["event_id"]
    app = dict(zip(eb0["event_id"], eb0["event_id"]))
    for r in eb0[eb0["copy"]].itertuples():
        app[r.event_id] = lead[(r.date, r.block, r.t_local)]
    truth = set(eb0.loc[~eb0["copy"] & ~eb0["test"] & ~eb0["check"], "event_id"])
    # the trip reading on the clean truth: each such record lies on one of its block's trips (a realised pass of its car,
    # the passes the AVL log lost included)
    P = Rr["passes"].sort_values("entry_local")
    PP = P[["lead_car", "entry_local", "exit_local"]].astype({"lead_car": "int64"})

    def on_pass(recs, passes):
        x_ = pd.merge_asof(recs.sort_values("t_local")[["event_id", "car", "t_local"]].astype({"car": "int64"}), passes,
                           left_on="t_local", right_on="entry_local", left_by="car", right_by="lead_car", direction="backward")
        return set(x_.loc[(x_["t_local"] <= x_["exit_local"]).fillna(False), "event_id"])

    rec = eb0[eb0["event_id"].isin(truth)]
    on_trip = on_pass(rec, PP)
    check("SF23 ask A trip reading: every application lies on one of its block's trips (a pass of its car, logged or lost)",
          on_trip == truth, "%d of %d" % (len(on_trip), len(truth)))
    check("ask A: no depot release test and no brake check lies on a trip",
          not on_pass(eb0[eb0["test"] | eb0["check"]], PP))
    # the literal reading of SRM-07 6.2 on the clean truth: each car from its own pull-out onto a block to its own pull-in
    C = Rr["consist"]
    SW = Rr["swaps"]
    bad_in, spare_out = {}, {}
    for s_ in SW.itertuples():
        d = pd.Timestamp(s_.date)
        on = (P["date"] == d) & (P["block"] == s_.block)
        bad_in[(d, int(s_.bad_car))] = P.loc[on & (P["lead_car"] == s_.bad_car), "exit_local"].max() + pd.Timedelta(minutes=10)
        spare_out[(d, int(s_.spare), s_.block)] = P.loc[on & (P["lead_car"] == s_.spare), "entry_local"].min() - pd.Timedelta(minutes=5)
    spans = []
    for r in C.itertuples():
        d = pd.Timestamp(r.date)
        spans.append((d, int(r.lead_car), r.pull_out, bad_in.get((d, int(r.lead_car)), r.pull_in)))
        if not pd.isna(r.trail_car):
            spans.append((d, int(r.trail_car), r.pull_out, r.pull_in))
    pin = {(pd.Timestamp(r.date), r.block): r.pull_in for r in C.itertuples()}
    for (d, c, blk), t0 in spare_out.items():
        spans.append((d, c, t0, pin[(d, blk)]))
    sp = pd.DataFrame(spans, columns=["date", "car", "t0", "t1"])
    y = eb0[~eb0["test"]].merge(sp, on=["date", "car"])
    lit = {app[i] for i in y.loc[(y["t_local"] >= y["t0"]) & (y["t_local"] <= y["t1"]), "event_id"]}
    check("SF23 ask A literal reading of SRM-07 6.2 on the clean truth (each car from its own pull-out onto a block to its own "
          "pull-in, the release tests out, a two-car train's records one) counts the same applications", lit == truth,
          "%d against %d" % (len(lit), len(truth)))
    # the block-assignment reading from target/: the golden's in-service map (the yard sheets' cars from the block's
    # out time to the AVL's change-off, the car that took the block over from then to the in time)
    gold_a = {app[i] for i in GD.ask_a(as_set=True)}
    check("SF23 ask A block-assignment reading from target/ (the golden's in-service map) counts the same applications",
          gold_a == truth, "%d against %d" % (len(gold_a), len(truth)))
    for w_ in (60, 120, 360):
        check("SF24 ask A: a two-car train's records paired within %d s count the same applications" % w_,
              {app[i] for i in GD.ask_a(as_set=True, window_s=w_)} == truth)
    check("SF24 ask A: the yard sheet's second car's records dropped instead of paired count the same applications",
          {app[i] for i in GD.ask_a(as_set=True, dedupe="drop")} == truth)
    check("SF24 ask A: with or without the release log, the in-service map counts the same applications (each test follows "
          "its car's pull-in)", {app[i] for i in GD.ask_a(as_set=True, tests=None)} == truth)
    # the AVL-passes-only reading differs only by the applications on passes the AVL log lost, which 6.2 includes
    avl_only = {app[i] for i in GD.ask_a(as_set=True, revenue="avl", dedupe="none")}
    logged = on_pass(rec, Rr["avl"][["lead_car", "entry_local", "exit_local"]].astype({"lead_car": "int64"}).sort_values("entry_local"))
    check("SF23 ask A: the AVL-passes-only reading differs only by the %d applications on passes the AVL log lost, which "
          "SRM-07 6.2 includes" % len(truth - logged), avl_only == logged and logged <= truth)
    # the readings the words rule out, each another figure
    for sf_, kw, label, why in (("SF19", dict(month="utc"), "the UTC month", "the asking sentence's Mountain-time month"),
                                ("SF23", dict(revenue="avl", dedupe="none"), "the AVL passes alone", "SRM-07 6.2's pull-out to pull-in"),
                                ("SF23", dict(revenue="yard"), "the yard sheets' pull-out cars alone",
                                 "SRM-07 6.2: the car that took a block over is in service on it")):
        alt = GD.ask_a(**kw)
        mv = sum(alt[k_] != v_ for k_, v_ in fig["ask_a"].items())
        check("%s ask A: %s moves %d of 7 (ruled out by %s)" % (sf_, label, mv, why), mv >= 1, str(alt))
    t = GD.to_local(E["event_time_utc"])
    edge = (((t - t.dt.normalize()).dt.total_seconds() < 15) & (t.dt.day == 1)) | \
           (((t.dt.normalize() + pd.Timedelta(days=1) - t).dt.total_seconds() < 15) & ((t + pd.Timedelta(days=1)).dt.day == 1))
    check("SF21 no EB or OS record within 15 s of a month boundary", int((edge & E["event_code"].isin(["EB", "OS"])).sum()) == 0)
    # the yard sheets' times: each block's out time precedes its first logged pass, its in time follows its last
    Y = GD.yard_sheets()
    av = pd.read_parquet(GD.path("avl"), columns=["service_date", "block", "enter_local", "exit_local"])
    av["day"] = pd.to_datetime(av["service_date"])
    av["block"] = av["block"].astype(str)
    bd = av.groupby(["day", "block"]).agg(f=("enter_local", "min"), l=("exit_local", "max")).reset_index()
    yb = Y.merge(bd, on=["day", "block"])
    check("ask A: every yard sheet line's out time precedes its block's first logged pass and its in time follows its last",
          bool((yb["out"] <= yb["f"]).all() and (yb["pin"] >= yb["l"]).all()), "%d lines" % len(yb))
    ck = eb0[eb0["check"]]
    rb = GD.ran_blocks()
    ranb = set(zip(rb["sday"], rb["car"].astype(int)))
    check("ask A: every brake check is on a car that ran no block that day, at walking pace (%d checks)" % len(ck),
          len(ck) > 100 and not any((pd.Timestamp(d), int(c)) in ranb for d, c in zip(ck["date"], ck["car"]))
          and bool((ck["speed_mph"] < 8).all()))

    # ask B: the golden and the truth
    check("ask B golden equals the flag truth", fig["ask_b"] == Rr["defect_truth"], str(fig["ask_b"]))
    flat = [fig["ask_b"][ln][g] for ln in ("Juniper", "Foundry") for g in ("Brakes", "Doors", "All other")]
    check("ask B figures are whole cards", all(isinstance(v, int) for v in flat), str(flat))
    check("SF20 SF22 SF25 ask B: the asking sentence files the day written, the weekday timetable and the months as a whole",
          all(x in prompt for x in ("each counted on the day it was written", "only if the weekday timetable ran that day",
                                    "over those months as a whole")))
    mm = pd.read_csv(GD.path("mms"), dtype={"block": str})
    check("ask B: the MMS export names its entry and no writing day (entered_at, entered_date the date of entered_at on "
          "every row)", list(mm.columns) == ["wo_no", "entered_at", "entered_date", "source", "car", "block", "defect_group", "defect"]
          and bool((pd.to_datetime(mm["entered_at"]).dt.strftime("%Y-%m-%d") == mm["entered_date"]).all()))
    K, day = GD.card_days()
    kt = Rr["cards_truth"].assign(t=lambda d_: d_["created"].dt.strftime("%Y-%m-%d %H:%M"))
    kt = kt.sort_values(["t", "car", "defect"], kind="mergesort").reset_index(drop=True)
    Ks = K.assign(t=K["entered_at"], d=day.values).sort_values(["t", "car", "defect"], kind="mergesort").reset_index(drop=True)
    check("SF20 ask B: each card dated by its car and block against the cars that ran each block falls on the day it was written",
          len(Ks) == len(kt) and bool((Ks["d"].values == kt["sday"].values).all()), "%d cards" % len(kt))
    # C1 on the dating, under the cars that ran each block (the yard sheets and the AVL's takeover cars): exactly one day
    # in the week before entry, never the entry day, so the narrow and broad readings of the day are one set
    mj = K.reset_index().merge(rb, on=["car", "block"])
    w7 = mj[(mj["sday"] < mj["kd"]) & (mj["sday"] >= mj["kd"] - pd.Timedelta(days=7))].groupby("index").size()
    on_entry = mj[mj["sday"] == mj["kd"]]
    check("SF20 ask B C1: every operator card's car ran its block on exactly one day in the week before entry and not on the "
          "entry day", len(w7) == len(K) and bool((w7 == 1).all()) and len(on_entry) == 0, "%d cards" % len(K))
    for kw in (dict(days=14), dict(days=30), dict(include_entry=True), dict(days=30, include_entry=True)):
        check("SF20 ask B: the day read as %s gives the same figures" % kw, GD.ask_b(**kw) == fig["ask_b"])
    for route, label in (("entered", "the MMS entered date"), ("previous", "the day before entry"),
                         ("car", "the car's last day out on any block")):
        alt = GD.ask_b(dating=route)
        mv = sum(alt[ln][g] != fig["ask_b"][ln][g] for ln in alt for g in alt[ln])
        check("SF20 ask B: dating each card by %s is another figure (moves %d of 6)" % (label, mv), mv >= 4)
    for route, label in (("yard", "the yard sheets alone (the car that took a block over unnamed)"),
                         ("avl", "the AVL log alone (a two-car train's trailing car unlogged)")):
        alt = GD.ask_b(dating=route)
        mv = sum(alt[ln][g] != fig["ask_b"][ln][g] for ln in alt for g in alt[ln])
        check("ask B: dating by %s moves %d of 6" % (label, mv), mv >= 3)
    # weekday service: the run sheets' schedule and the AVL log's start before 07:00 agree
    sw_ = GD.schedule_weekdays()
    check("ask B: the run sheets' Weekday schedule days are the AVL log's weekday-timetable days, the three holidays on "
          "the Sunday schedule", sw_ == GD.weekday_service() and not any(pd.Timestamp(h) in sw_ for h in W.OBS_HOLIDAYS))
    alt = GD.ask_b(weekday="calendar")
    mv = sum(alt[ln][g] != fig["ask_b"][ln][g] for ln in alt for g in alt[ln])
    check("SF22 calendar weekdays (the holidays kept) move %d of 6, ruled out by the asking sentence's weekday timetable"
          % mv, mv >= 1)
    K2, d2 = GD.card_days()
    wk2 = GD.schedule_weekdays()
    per_month = d2[d2.map(lambda d_: d_ in wk2)].dt.month.nunique()
    check("SF25 ask B per month instead of the months as a whole is another figure set (%d months, ruled out by the "
          "asking sentence's as a whole)" % per_month, per_month == 7)
    check("SF26 ask B: a card's line by its car is its line by its block on every card",
          bool(((K["car"] < 120) == K["block"].str.startswith("J")).all()))
    check("ask B: no two operator cards share car, writing day and defect",
          not Rr["cards_truth"].duplicated(["car", "sday", "defect"]).any())
    check("separation line: the MMS export carries no section, position or time of day of a card's service",
          not set(mm.columns) & {"section_id", "lat", "lon", "direction", "trip_id"} and "Operator card" in set(mm["source"]))

    # the ceiling, on the cut pack
    cm = ceiling.main(TARGET)
    check("pair ceiling at or under 60 (one response on the call, one off)", cm["pair"] <= 60.0, "%.1f" % cm["pair"])
    check("two crackers both on the call at or under 60", cm["both_on"] <= 60.0, "%.1f" % cm["both_on"])
    check("full includer keeps at most two fifths of the ask figures", cm["full"] <= 40.0, "%.1f per cent" % cm["full"])
    check("cracker keeps at most two fifths of the ask figures", cm["leak"] <= 40.0, "%.1f per cent" % cm["leak"])
    for k_, v_ in cm["keep_a"].items():
        if "cracker" in k_:
            check("%s keeps at most one of ask A's 7" % k_.split(" (")[0], v_ <= 1, "%d" % v_)
            check("%s keeps none of ask B's 6" % k_.split(" (")[0], cm["keep_b"][k_] == 0, "%d" % cm["keep_b"][k_])
    check("mirror leakage under one half", cm["mirror"] < 50.0, "%.1f per cent" % cm["mirror"])
    check("the blind route (every record but the named exceptions) keeps none of ask A",
          cm["keep_a"][[k_ for k_ in cm["keep_a"] if k_.startswith("blind")][0]] == 0)
    check("every ask figure is a whole number", all(isinstance(v, int) for v in cm["gold"]))


def steps_text():
    import re
    sub = open(os.path.join(TASK, "submission.md")).read()
    blk = sub.split("## 3. Step-by-Step Solution")[1].split("## 4.")[0]
    steps = {int(m.group(1)): m.group(2).strip() for m in re.finditer(r"^(\d+)\. (.+)$", blk, re.M)}
    return steps, blk, sub.split("## 4. Deliverable Answers")[1]


def literal_steps(gold):
    """SOLUTION_STEPS executed as written on the shipped files: each step's own words read at face value (its parameters
    parsed from its text) and the figure it states asserted. The asks run through ceiling.py's own routes."""
    import re
    import ceiling
    steps, blk, b4 = steps_text()
    lines = [x for x in blk.strip().splitlines() if x.strip()]
    check("literal: at most eight steps, one line each", 1 <= len(steps) <= 8 and len(lines) == len(steps), "%d steps" % len(steps))
    n_ = lambda s: int(s.replace(",", ""))
    # step 1: UTC to Mountain time, each FB record on its car's pass whose section lies nearest the recorded position
    m = re.search(r"(\d+) per cent of the ([\d,]+) FB records fall on a logged pass", steps[1])
    E = pd.read_csv(GD.path("edr"))
    nfb = int((E["event_code"] == "FB").sum())
    A, sec, lat, lon = GD.passes(assign="position", at="mid", sky="hour")
    check("literal step 1: the FB records and the share on a logged pass it states", bool(m) and n_(m.group(2)) == nfb and
          int(m.group(1)) == int(round(100 * A["n_fb"].sum() / nfb)), "%d of %d" % (A["n_fb"].sum(), nfb))
    # step 2: the bearings it states, from the survey's coordinates
    m = re.search(r"J4 and J5 outbound head (\d+) and (\d+) degrees, F5 and F6 outbound (\d+) and (\d+)", steps[2])
    b = sec.set_index("section")["bearing_out"]
    got = [int(round(b[s])) for s in ("J4", "J5", "F5", "F6")]
    check("literal step 2: the bearings it states", bool(m) and got == [int(x) for x in m.groups()], str(got))
    check("literal step 2: the bearings sit clear of their rounding edges", all(abs(b[s] - round(b[s])) < 0.4 for s in ("J4", "J5", "F5", "F6")))
    # step 3: the stated glare form, fitted on every logged pass
    m = re.search(r"25 degrees off gives none and h one with the sun under (\d+) degrees up, falling to none at (\d+): G is (\d+\.\d+)", steps[3])
    coef, G = GD.fit(A, cone=25.0, efull=float(m.group(1)), ezero=float(m.group(2)), shape="cos2")
    check("literal step 3: G as it states", round(G, 1) == float(m.group(3)) and abs(G - round(G, 1)) < 0.04, "%.3f" % G)
    # step 4: the pick's passes on its weekdays, at the normals' January and February sunshine, the four highest
    pk = GD.pick()
    days = [d for d in pd.date_range(pk["start"], pk["end"]) if d.weekday() < 5 and d not in pk["holidays"]]
    ps = GD.normals_sunshine()
    m = re.search(r"on its (\d+) weekdays.*?at the (\d+) per cent possible sunshine.*?the four highest are (.+)\.$", steps[4])
    r = GD.project(coef, G, GD.pick_passes(sec, pk, lat, lon), ps)
    stated = set(m.group(3).replace(" and ", ", ").split(", "))
    check("literal step 4: the weekdays, the sunshine and the four slots it states", len(days) == int(m.group(1)) and
          ps[1] == ps[2] == int(m.group(2)) / 100 and key(GD.slate(r)) == stated == gold, str(sorted(stated)))
    # step 5: ask A as written, against block 4
    m = re.search(r"before (\d\d):00 counts to the day before.*?in the hour after each release.*?within (\d+) minutes and "
                  r"(\d+) metres", steps[5])
    a_lit = ceiling.ask_a(TARGET, "operating", tests="release", copies="pair", window=int(m.group(2)) * 60, metres=int(m.group(3)))
    sec3 = b4.split("### Emergency brake applications")[1].split("###")[0]
    a_b4 = [int(x) for x in re.findall(r"\b(?:April|May|June|July|August|September|October) (\d{1,3})(?!\d)", sec3)]
    check("literal step 5: ask A as written gives block 4's seven figures", int(m.group(1)) == 3 and a_lit == a_b4 and
          "out time" in steps[5] and "in time" in steps[5], str(a_lit))
    # step 6: ask B as written, against block 4
    b_lit = ceiling.ask_b(TARGET, "operating")
    sec4 = b4.split("### Defect cards")[1]
    b_b4 = [int(x) for ln in ("Juniper", "Foundry") for x in
            re.search(r"%s Line: brakes (\d+), doors (\d+), all other defects (\d+)" % ln, sec4).groups()]
    check("literal step 6: ask B as written gives block 4's six figures", "Weekday schedule" in steps[6] and
          "taking the block over" in steps[6] and b_lit == b_b4, str(b_lit))
    # step 7 and block 4's slot plan lines: the golden CSV as stated
    csv = pd.read_csv(os.path.join(TASK, "golden", "slot_plan_jan_feb_2027.csv"))
    yes = {"%s-%s %s" % (s, d[0].upper(), p) for s, d, p, v in
           zip(csv["section_id"], csv["direction"], csv["peak"], csv["restricted_speed_slot"]) if v == "yes"}
    check("literal step 7: the slot plan marks the four slots among its 52 rows", len(csv) == n_(re.search(r"among its (\d+) rows",
          steps[7]).group(1)) and yes == gold)
    marks = re.findall(r"- ([JF]\d) (outbound|inbound), .*?: AM (yes|no), PM (yes|no)", b4)
    want = {(s, d): (csv[(csv.section_id == s) & (csv.direction == d) & (csv.peak == "AM")].restricted_speed_slot.iloc[0],
                     csv[(csv.section_id == s) & (csv.direction == d) & (csv.peak == "PM")].restricted_speed_slot.iloc[0])
            for s, d in zip(csv["section_id"], csv["direction"])}
    check("literal block 4: every slot plan line states the CSV's marks", len(marks) == 26 and
          all(want[(s, d)] == (am, pm) for s, d, am, pm in marks))
    png = open(os.path.join(TASK, "golden", "braking_shift.png"), "rb").read()
    check("H1: the chart carries no writer's name", b"atplotlib" not in png and b"Software" not in png)


def _steps(v):
    d = np.diff(np.sort(np.asarray(v, dtype=float)))
    return set(np.round(d[d > 0], 6))


def realism_sweep(files):
    """The realism sweep on target/ (dataset-generation sections 7, 9 and 11; house fixes H1 and H13). Constant columns
    the producing systems really write are accepted and named: the airport file's station id (one station's
    download), the roster's status (a roster of active operators) and the depot release log's check (the release
    form's printed check)."""
    import datetime as dtm
    import re
    import pypdf
    import pyarrow.parquet as pq
    from pandas.api.types import is_numeric_dtype
    rd = lambda k, **kw: pd.read_csv(os.path.join(TARGET, pack.FILES[k]), **kw)
    edr, mms, rel = rd("edr"), rd("mms", dtype={"block": str}), rd("releases")
    ros, bdg, runs, awos = rd("roster"), rd("cards"), rd("runs"), rd("metar")
    av = pd.read_parquet(os.path.join(TARGET, pack.FILES["avl"]))
    # 1 no id column steps by one constant
    seq = edr["event_id"].str.split("-").str[1].astype(int)
    ids = {"EDR event numbers, fewest step sizes in any car": min(len(_steps(seq[edr["car"] == c])) for c in edr["car"].unique()),
           "MMS work orders": len(_steps(mms["wo_no"].str[3:].astype(int))),
           "depot release work orders": len(_steps(rel["work_order"].str[3:].astype(int))),
           "roster operator numbers": len(_steps(ros["operator_no"])), "badge numbers": len(_steps(bdg["badge"])),
           "track survey lengths": len(_steps([f["properties"]["length_ft"] for f in json.load(open(os.path.join(
               TARGET, pack.FILES["survey"])))["features"] if "length_ft" in f["properties"]]))}
    check("realism 1: no id or number column steps by one constant (H13)", all(v > 1 for v in ids.values()), str(ids))
    wr = rel.sort_values("released")["work_order"].str[3:].astype(int)
    check("realism 1: the depot's repair work orders run in time order inside the agency's series, apart from every MMS row",
          wr.is_monotonic_increasing and not set(wr) & set(mms["wo_no"].str[3:].astype(int)))
    # 2 no timestamp rises by a fixed increment: the AVL log carries the actual running, not the timetable
    rt = (av["exit_local"] - av["enter_local"]).dt.total_seconds()
    nrt = rt.groupby([av["section_id"].astype(str), av["direction"].astype(str)]).nunique()
    check("realism 2: AVL running times vary within every section direction (fewest distinct values 30 or more)",
          nrt.min() >= 30, "fewest %d" % nrt.min())
    first = av[av["section_id"].astype(str).isin(["J1", "F1"]) & (av["direction"].astype(str) == "OB")]
    check("realism 2: AVL entry stamps use every second of the minute, and outer-stop departures leave late by varying amounts",
          av["enter_local"].dt.second.nunique() == 60 and first["enter_local"].dt.second.nunique() == 60)
    rh = runs[runs["duty"] == "operator"].groupby("run")["revenue_hours"].nunique()
    check("realism 2: each run's revenue hours vary day to day", rh.min() > 10, "fewest distinct %d" % rh.min())
    gaps = pd.to_datetime(mms["entered_at"]).sort_values().diff().dt.total_seconds().dropna()
    check("realism 2: the MMS keying times do not step by a constant", gaps.nunique() > 50)
    # 3 no identical counts across periods, sites or entities
    pc = av.groupby([av["line"].astype(str), pd.to_datetime(av["service_date"]).dt.month]).size()
    check("realism 3: AVL passes per line and month all differ", pc.nunique() == len(pc), str(pc.to_dict()))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(TARGET, pack.FILES["dash"]))
    rows = [r for r in wb.active.iter_rows(min_row=4, values_only=True) if r[0]]
    check("realism 3: the dashboard's trips and passes differ across every line and month, April to October only",
          len({r[2] for r in rows}) == len(rows) and len({r[3] for r in rows}) == len(rows)
          and [r[0] for r in rows][::2] == ["2026-%02d" % m for m in range(4, 11)])
    dash_pass = {(r[0], r[1]): r[3] for r in rows}
    av_pass = {("2026-%02d" % m, {"JUN": "Juniper", "FDY": "Foundry"}[ln]): int(v) for (ln, m), v in pc.items()}
    check("realism 3: the dashboard's section passes tie to the AVL log as shipped", dash_pass == av_pass)
    pk = GD.pick()
    check("realism 3: the January pick's running times differ by direction on most sections",
          sum(o != i for o, i in pk["run"].values()) >= 10, str(pk["run"]))
    # 4 no round headline totals
    sizes = {f: (pq.ParquetFile(os.path.join(TARGET, f)).metadata.num_rows if f.endswith(".parquet") else
                 sum(1 for _ in open(os.path.join(TARGET, f))) - 1) for f in files if f.endswith((".csv", ".parquet"))}
    tot = list(sizes.values()) + [v for r in rows for v in r[2:5] + r[6:8]]
    check("realism 4: no file's row count and no dashboard count is a multiple of 100", not any(v % 100 == 0 for v in tot),
          str(sizes))
    # 5 no ordering follows the alphabet; names take more than two shapes; nothing dealt round-robin
    stops = [f["properties"]["stop_name"] for f in json.load(open(os.path.join(TARGET, pack.FILES["survey"])))["features"]
             if "stop_name" in f["properties"]]
    ctr = list(dict.fromkeys(rd("peds")["counter"]))
    by_code = [c.split(" ", 1)[1] for c in sorted(ctr, key=lambda c: int(c.split()[0][3:]))]
    check("realism 5: stops in line order and the pedestrian counters in code order are not alphabetical",
          stops != sorted(stops) and by_code != sorted(by_code))
    shapes = {s.split()[-1] if len(s.split()) > 1 else "one word" for s in stops}
    check("realism 5: stop names take more than two shapes", len(shapes) > 2, str(sorted(shapes)))
    op = runs[runs["duty"] == "operator"].sort_values(["service_date", "run"])
    mono = op.groupby("service_date")["operator_no"].apply(lambda s: s.is_monotonic_increasing or s.is_monotonic_decreasing)
    check("realism 5: no day's runs take operators in number order (no round-robin over the roster)", mono.mean() < 0.05,
          "%.3f of days" % mono.mean())
    const = {f"{k}.{c}" for k, d in (("metar", awos), ("roster", ros), ("releases", rel), ("mms", mms), ("edr", edr),
                                     ("runs", runs)) for c in d.columns if d[c].nunique() == 1}
    check("realism 5: the only constant columns are the accepted ones",
          const == {"metar.station", "roster.status", "releases.release_check"}, str(sorted(const)))
    big = awos["tmpf"].diff().abs()
    check("realism 5: the airport temperature moves in spells, not hour by hour", big.quantile(0.95) <= 6, "95th %.0f" % big.quantile(0.95))
    # 6 timestamps coherent: every record precedes the bundle's export, documents' own stamps in order and in the fiction
    zt = pd.Timestamp(dtm.datetime(*pack.FIXED_ZIP_TIME))
    last = max(pd.to_datetime(mms["entered_at"]).max(), GD.to_local(edr["event_time_utc"]).max(), av["exit_local"].max(),
               pd.to_datetime(rel["released"]).max(), GD.to_local(awos["valid_utc"] + "Z").max())
    check("realism 6: every record precedes the bundle's export stamp", last < zt, "%s before %s" % (last, zt))
    zi = zipfile.ZipFile(os.path.join(TASK, "target.zip")).infolist()
    check("realism 6: every bundle entry carries the export stamp", {i.date_time for i in zi} == {pack.FIXED_ZIP_TIME})
    stamps = {}
    for f in files:
        if f.endswith(".pdf"):
            raw = open(os.path.join(TARGET, f), "rb").read()
            md = pypdf.PdfReader(os.path.join(TARGET, f)).metadata
            c_, m_ = (pd.Timestamp(dtm.datetime.strptime(md[k][2:16], "%Y%m%d%H%M%S")) for k in ("/CreationDate", "/ModDate"))
            stamps[f] = (c_, m_)
            check("realism 6 H1: %s carries no writer name and its own stamps, created before modified, before the export" % f,
                  b"ReportLab" not in raw and b"reportlab" not in raw and c_ < m_ < zt and c_.year >= 2021)
    check("realism 6 H13: no two documents share a creation stamp", len({c for c, _ in stamps.values()}) == len(stamps))
    srm_c = stamps[pack.FILES["srm"]][0]
    srm_t = " ".join((pg.extract_text() or "") for pg in GD.pdfplumber.open(GD.path("srm")).pages)
    check("realism 6: SRM-07's revision is dated after the recorder commissioning it cites and before its effective date",
          "Revision 4. Effective 1 October 2026" in srm_t and pd.Timestamp("2026-04-01") < srm_c < pd.Timestamp("2026-10-01"))
    pick_m = stamps[pack.FILES["pick"]][1]
    check("realism 6: the pick timetable was last saved on its issue date", pick_m.date() == dtm.date(2026, 11, 2))
    zx = zipfile.ZipFile(os.path.join(TARGET, pack.FILES["dash"]))
    app, core = zx.read("docProps/app.xml"), zx.read("docProps/core.xml").decode()
    cr = re.search(r"<dcterms:created[^>]*>([^<]+)<", core).group(1)
    mo = re.search(r"<dcterms:modified[^>]*>([^<]+)<", core).group(1)
    check("realism 6 H1 H13: the workbook names Excel with Excel's version, created at the first download, modified at the last",
          b"<Application>Microsoft Excel</Application><AppVersion>16." in app and b"penpyxl" not in app and
          cr < mo and cr.startswith("2026-05-01") and mo.startswith("2026-11-01"), "%s %s" % (cr, mo))
    # 7 every PDF reads the same in a strict reader, a lenient one and pdftotext, and no text runs past the margin
    import subprocess
    sq = lambda s: re.sub(r"\s+", "", s)
    for f, ctl in ((pack.FILES["srm"], "One section, in one direction of travel, in one weekday peak"),
                   (pack.FILES["pick"], "Holidays in this pick (Sunday timetable)"), (pack.FILES["normals"], "Possible sunshine, %")):
        p_ = os.path.join(TARGET, f)
        strict = " ".join(pg.extract_text() or "" for pg in pypdf.PdfReader(p_, strict=True).pages)
        plumb = " ".join(pg.extract_text() or "" for pg in GD.pdfplumber.open(p_).pages)
        ptt = subprocess.run(["pdftotext", "-layout", p_, "-"], capture_output=True, text=True, check=True).stdout
        check("realism 7 H25: %s reads the same in a strict reader, a lenient one and pdftotext" % f,
              all(sq(ctl) in sq(t) for t in (strict, plumb, ptt)) and len(sq(strict)) > 200)
        over = max(max((c["x1"] for c in pg.chars), default=0) - (pg.width - 36) for pg in GD.pdfplumber.open(p_).pages)
        check("realism 7 H13: no text in %s runs past the right margin" % f, over <= 0, "%.1f pt inside the half-inch" % -over)
    # 8 nothing under target/ describes the data; one write-up and one prompt in the task tree
    check("realism 8 H9: no file or sheet under target/ describes the data",
          not any(re.search(r"readme|dictionar|manifest|notes|schema|field.?guide|codebook", f, re.I) for f in files)
          and not any(re.search(r"readme|notes|dictionar|about|how to", s, re.I) for s in wb.sheetnames), str(wb.sheetnames))
    tree = sorted(f for _, _, fs in os.walk(TASK) for f in fs if f in ("submission.md", "prompt.txt", "prompt.md"))
    check("realism 8 H11: one submission.md and one prompt.txt in the task tree", tree == ["prompt.txt", "submission.md"], str(tree))


def three_rules(T, Rr, P, gold, A, sec, lat, lon, X, ps, coef, G):
    """The client's three rules on the clean truth and on target/ (dataset-generation section 7.1)."""
    import pyarrow.parquet as pq
    # R1: the field's raw material ships, and no shipped column holds the deciding quantity
    heads = []
    for f in sorted(os.listdir(TARGET)):
        p_ = os.path.join(TARGET, f)
        if f.endswith(".csv"):
            heads += list(pd.read_csv(p_, nrows=1).columns)
        elif f.endswith(".parquet"):
            heads += pq.read_schema(p_).names
        elif f.endswith(".geojson"):
            heads += [k for ft in json.load(open(p_))["features"] for k in ft["properties"]]
    bad = [h for h in heads if any(w in h.lower() for w in ("sun", "elev", "azim", "glare", "bearing", "heading", "rate", "risk"))]
    check("R1 no shipped column holds the sun's position, a heading, a glare term or a cell's rate (%d headers read)" % len(heads),
          len(heads) > 30 and not bad, str(bad))
    nfb = int((pd.read_csv(GD.path("edr"))["event_code"] == "FB").sum())
    check("R1 the field's raw material ships: every logged pass and every firm brake, the survey's coordinates and the "
          "airport's hourly sky (the golden reads them all)", len(A) > 600000 and int(A["n_fb"].sum()) > 0.9 * nfb,
          "%d passes, %d of %d FB attached" % (len(A), int(A["n_fb"].sum()), nfb))
    # R2: every Layer 1 item is real and neutral: mishandled, it leaves the call or announces itself
    E = pd.read_csv(GD.path("edr"))
    E = E[E["event_code"] == "FB"].copy()
    E["car"] = E["car"].astype("int64")
    for label, shift in (("the recorder's UTC stamps read as Mountain time", 0), ("a fixed UTC-7 offset all season", -7)):
        E["t"] = (pd.to_datetime(E["event_time_utc"].str[:19]) + pd.Timedelta(hours=shift)).astype("datetime64[ns]")
        att = int(GD._attach(A, E, sec, "position").sum())
        check("R2 clock: %s is loud (%d of %d firm brakes find a pass of their car)" % (label, att, len(E)), att < 0.4 * len(E))
    Xb = X.copy()
    mid = Xb["enter"] + (Xb["exit"] - Xb["enter"]) / 2
    from solar import sun_position as _sp
    el_, az_ = _sp(np.asarray((mid + pd.Timedelta(hours=6)).dt.round("s").values, dtype="datetime64[s]"), lat, lon)
    Xb["elev"], Xb["az"] = el_, az_
    sh = len(key(GD.slate(GD.project(coef, G, Xb, ps))) & gold)
    check("R2 clock: the pick's January times converted at the summer offset (UTC-6) %s" %
          ("keeps the call" if sh == 4 else "moves the call (%d of 4): SRM-07 3.5 files Mountain local time" % sh),
          sh == 4 or "Mountain local time" in GD.pdfplumber.open(GD.path("srm")).pages[0].extract_text())
    # (GPS scatter, the drop-outs and outage week, and the :53 sky reports are R2 items asserted above as SF9, SF15, SF8)
    swk = set(zip(pd.to_datetime(Rr["swaps"]["date"]), Rr["swaps"]["block"]))
    on_sw = np.array([(d, b) in swk for d, b in zip(A["service_date"], A["block"].astype(str))])
    c_s, g_s = GD.fit(A[~on_sw].reset_index(drop=True))
    check("R2 cars swapped in service: the swapped Foundry block-days dropped from the fit (%d passes) print the same call"
          % int(on_sw.sum()), key(GD.slate(GD.project(c_s, g_s, X, ps))) == gold)
    sched = GD.pick()
    check("R2 the pick as a PDF table: its weekday spans, holidays and 26 running times read back",
          len(sched["spans"]) == 3 and len(sched["holidays"]) == 2 and len(sched["run"]) == 13)
    # R3a: the analyst test, the default path on the clean truth files the named wrong slate
    rung1 = key(M.slate(M.reader_a(P)))
    check("R3a the default path (rates netted for operators, darkness, sky and school, October carried) files "
          "F3-I AM, F4-O PM, J2-O AM and J3-O AM on the clean truth", rung1 == {"F3-I AM", "F4-O PM", "J2-O AM", "J3-O AM"},
          str(sorted(rung1)))
    # R3b: the decisive step alone moves the default path's model onto the golden; each lower rung's correction does not
    g_only, _ = M.golden(P)
    check("R3b the default path's model with only the sun-against-direction term added and carried to the pick's passes "
          "files the golden", key(M.slate(g_only)) == gold)
    for name in ("b_lowsun", "b_suntime", "c_sepoct", "d3_held_sepoct"):
        check("R3b the lower rung %s alone stays off the golden" % name, key(M.slate(M.READERS[name](P))) != gold)
    # R3c: no plant: no copied or backfilled block, no memo, draft or stakeholder figure, nothing ranks the cells
    daily = P[P["peak"] != "OFF"].groupby(["date", "sd"])["n_fb"].sum().unstack(fill_value=0)
    dup = daily.duplicated().sum()
    check("R3c no day's firm-brake counts across the section directions repeat another day's", dup == 0, "%d repeats" % dup)
    kinds = {os.path.splitext(f)[1] for f in os.listdir(TARGET)}
    check("R3c no memo, email, draft or briefing ships (no docx, eml, txt, md or pptx)",
          not kinds & {".docx", ".eml", ".txt", ".md", ".pptx", ".msg"}, str(sorted(kinds)))


if __name__ == "__main__":
    main()
