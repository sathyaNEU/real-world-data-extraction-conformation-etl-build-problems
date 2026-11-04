"""task210's generator assertions, run on the shipped seed after build.py has cut target/.

    python3 task210/generator/checks.py          # exit 1 on the first failed assertion

What it asserts: the golden computed from target/ matches the clean truth's slate; every rival reader of the main call
(the first look, the careful and constructing readers, reader (d), reader (f) and the literal execution of SRM-07, which
files no definition of low sun) files a wrong slate sharing at most two slots with the golden; no shipped document names
the sun as a hazard; every semantic fork (SF1 to SF22) prints the same call or is ruled out by a quoted sentence; the
C3 corridor (the slate under every cone from 15 to 35 degrees, every elevation profile and every shape of the glare
term, with the fourth slot's separation from the fifth under each); the separation; removing each competing cause
leaves the slate; the slate holds across the published range of the glare multiplier and the base rate; the asks'
figures equal the flag truth and are missed by the cracker; the separation line; the input gates; Gate G; the
metadata scrub.
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
    # SF11 to SF13, the C3 corridor: no shipped sentence defines low sun, so the glare term's cone, elevation profile and
    # shape are the analyst's; the slate is the same, with the fourth slot clear of the fifth, across all of them
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
    a_truth = {("Juniper" if l == "J" else "Foundry") + " %02d" % m: int(v) for (l, m), v in Rr["eb_truth"].items()}
    check("ask A golden equals the flag truth", fig["ask_a"] == a_truth)
    prompt = open(os.path.join(TASK, "prompt.txt")).read()
    check("SF19 the asking sentence files the Mountain-time month (the UTC month moves %d figures)"
          % sum(GD.ask_a(month="utc")[k] != v for k, v in fig["ask_a"].items()), "Mountain" in prompt)
    check("ask B golden equals the flag truth", fig["ask_b"] == Rr["defect_truth"], str(fig["ask_b"]))
    flat = [fig["ask_b"][ln][g] for ln in ("Juniper", "Foundry") for g in ("Brakes", "Doors", "All other")]
    check("ask B figures are whole cards, each 0.5 of a card from its rounding edges", all(isinstance(v, int) for v in flat),
          str(flat))
    # SF20, C1 on the dating: each operator card's car pulled out on the card's block on exactly one service day in
    # the week before the card was keyed (the yard's block sheets as shipped), so every dating window agrees
    mm = pd.read_csv(GD.path("mms"), dtype={"block": str})
    oc = mm[mm["source"] == "Operator card"].copy()
    oc["kd"] = pd.to_datetime(oc["created"]).dt.normalize()
    Yd = pd.read_csv(GD.path("yard"))
    Yd["sday"] = pd.to_datetime(Yd["sheet_date"], format="%m/%d/%Y")
    Yl = pd.DataFrame([(d, b, int(c)) for d, b, cs in zip(Yd["sday"], Yd["block"], Yd["pullout_cars"].astype(str))
                       for c in cs.split("+")], columns=["sday", "block", "car"])
    mj = oc.reset_index().merge(Yl, on=["car", "block"])
    nwin = mj[(mj["sday"] < mj["kd"]) & (mj["sday"] >= mj["kd"] - pd.Timedelta(days=7))].groupby("index").size()
    check("SF20 C1 every operator card's car ran its block on exactly one service day in the week before keying",
          len(nwin) == len(oc) and bool((nwin == 1).all()), "%d cards" % len(oc))
    for d_ in (14, 30):
        check("SF20 a %d-day dating window gives the same figures" % d_, GD.ask_b(days=d_) == fig["ask_b"])
    for route, label in (("reported", "the MMS reported date"), ("previous", "the day before keying"),
                         ("car", "the car's last day out on any block")):
        alt = GD.ask_b(dating=route)
        mv = sum(alt[ln][g] != fig["ask_b"][ln][g] for ln in alt for g in alt[ln])
        check("SF20 dating each card by %s is another figure (moves %d of 6)" % (label, mv), mv >= 5)
    # SF22: weekday service days are the days the weekday timetable ran; the three holidays ran the Sunday timetable
    alt = GD.ask_b(weekday="calendar")
    mv = sum(alt[ln][g] != fig["ask_b"][ln][g] for ln in alt for g in alt[ln])
    Av = pd.read_parquet(GD.path("avl"), columns=["service_date", "enter_local"])
    first = Av.groupby("service_date")["enter_local"].min()
    hol = [pd.Timestamp(h) for h in W.OBS_HOLIDAYS]
    check("SF22 the holidays (Mon or Fri) ran the Sunday timetable, service from 07:00 (calendar weekdays move %d of 6)" % mv,
          all(first[h.date()].hour == 7 for h in hol) and all(h.weekday() < 5 for h in hol))
    check("SF22 the asking sentence names weekday service days", "weekday service days" in prompt)
    check("separation line: the MMS export carries no section, position or time of day of a card's service",
          not set(mm.columns) & {"section_id", "lat", "lon", "direction", "trip_id"} and "Operator card" in set(mm["source"]))
    t = GD.to_local(E["event_time_utc"])
    edge = (((t - t.dt.normalize()).dt.total_seconds() < 15) & (t.dt.day == 1)) | \
           (((t.dt.normalize() + pd.Timedelta(days=1) - t).dt.total_seconds() < 15) & ((t + pd.Timedelta(days=1)).dt.day == 1))
    check("SF21 no EB or OS record within 15 s of a month boundary", int((edge & E["event_code"].isin(["EB", "OS"])).sum()) == 0)
    import ceiling
    cm = ceiling.main(TARGET)
    check("pair ceiling at or under 60", cm["pair"] <= 60.0, "%.1f" % cm["pair"])
    print("REPORT pair with both on the call %.1f" % cm["both_on"])
    check("full includer keeps at most two fifths", cm["full"] <= 40.0, "%.1f per cent" % cm["full"])
    check("the cracker misses ask A and ask B", cm["leak"] <= 20.0, "%.1f per cent kept" % cm["leak"])
    for k_, v_ in cm["keep_a"].items():
        if "cracker" in k_:
            check("%s keeps at most one of ask A's 14" % k_.split(" (")[0], v_ <= 1, "%d" % v_)
            check("%s keeps none of ask B's 6" % k_.split(" (")[0], cm["keep_b"][k_] == 0, "%d" % cm["keep_b"][k_])
    check("mirror leakage under one half", cm["leak"] < 50.0, "%.1f per cent" % cm["leak"])

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
