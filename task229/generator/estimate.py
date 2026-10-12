"""Every rung, grid cell and rung-3 estimator of task229, read only from the shipped files.

The golden estimator: each in-scope face's chance of a correct record at 06:00 on 7 December is
(1 - p_class) ** days, where days is the number of trading days since the face's last count of any kind
(a count on the night of 6 December leaves none) and p_class is the per-day chance of a record going wrong,
fitted by maximum likelihood on the routine (CYC) counts that have an earlier count of any kind on the same
face in the export, each such count's exposure being the trading days since that earlier count. A centre's
share is the mean over its in-scope faces.
"""
import datetime as dt
import os

import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

import world as W
import simulate as S

STAND = pd.Timestamp("2026-12-07")
EXC = {"SHP", "NEG", "EMP", "OVR"}


def load(target):
    loc = pd.read_csv(os.path.join(target, S.FILES["locations"]), dtype=str, keep_default_na=False)
    cnt = pd.read_csv(os.path.join(target, S.FILES["counts"]), dtype=str, keep_default_na=False)
    return loc, cnt


def in_scope(loc, when="2026-12-07"):
    m = ((loc.location_type == "PICK") & (loc.client == "THN") & (loc.line_no != "") & (loc.status == "ACTIVE")
         & (loc.eff_from <= when) & ((loc.eff_to == "") | (loc.eff_to >= when)))
    f = loc[m].copy()
    f["pick_velocity"] = f.pick_velocity.astype(float)
    return f


def trading_day(utc_text):
    t = pd.to_datetime(utc_text, utc=True).dt.tz_convert("Europe/London").dt.tz_localize(None)
    return ((t - pd.Timedelta(hours=6)).dt.normalize() - pd.Timestamp(W.START)).dt.days


def prepared(target, include_out_of_scope=False, utc_days=False):
    loc, cnt = load(target)
    faces = in_scope(loc)
    if include_out_of_scope:
        allf = loc[(loc.location_type == "PICK") & (loc.client == "THN") & (loc.line_no != "")]
        allf = allf.sort_values("eff_from").drop_duplicates(["site", "location"], keep="first").copy()
        allf["pick_velocity"] = pd.to_numeric(allf.pick_velocity, errors="coerce")
        faces = allf
    c = cnt.merge(faces[["site", "location", "slot_class", "pick_velocity"]], on=["site", "location"], how="inner")
    if utc_days:
        c["day"] = (pd.to_datetime(c.counted_utc, utc=True).dt.tz_localize(None).dt.normalize()
                    - pd.Timestamp(W.START)).dt.days - 1
    else:
        c["day"] = trading_day(c.counted_utc)
    c["hit"] = c.result == "MATCH"
    c["routine"] = c.reason_code == "CYC"
    c = c.sort_values(["site", "location", "counted_utc"]).reset_index(drop=True)
    same = (c.site == c.site.shift()) & (c.location == c.location.shift())
    c["age"] = np.where(same, c.day - c.day.shift(), np.nan)
    return faces, c


def fit_geom(expo, hit):
    expo = np.asarray(expo, float); hit = np.asarray(hit, bool)

    def nll(lp):
        p = np.exp(lp)
        pr = np.clip((1 - p) ** expo, 1e-12, 1 - 1e-12)
        return -(np.log(pr[hit]).sum() + np.log(1 - pr[~hit]).sum())
    return float(np.exp(minimize_scalar(nll, bounds=(-16, -1), method="bounded", options={"xatol": 1e-10}).x))


def last_day(faces, c, routine_only=False):
    src = c[c.routine] if routine_only else c
    ld = src.groupby(["site", "location"]).day.max().rename("last_day").reset_index()
    f = faces.merge(ld, on=["site", "location"], how="left")
    f["age_f"] = (W.F - 1) - f.last_day
    return f


def rung3(faces, c):
    """The four rigorous estimators per centre (per day by class is the golden)."""
    f = last_day(faces, c)
    obs = c[c.routine & c.age.notna()]
    out = {}
    for code, g in f.groupby("site"):
        o = obs[obs.site == code]
        res = {}
        day_cls = np.zeros(len(g)); htx_cls = np.zeros(len(g)); lin = np.zeros(len(g))
        for k in "ABC":
            ok = o[o.slot_class == k]; m = (g.slot_class == k).values
            p = fit_geom(ok.age, ok.hit)
            day_cls[m] = (1 - p) ** g.age_f.values[m]
            p4 = fit_geom(ok.age * ok.pick_velocity, ok.hit)
            htx_cls[m] = (1 - p4) ** (g.age_f.values[m] * g.pick_velocity.values[m])
            mpd = (~ok.hit).sum() / ok.age.sum()
            lin[m] = 1 - mpd * g.age_f.values[m]
        p1 = fit_geom(o.age * o.pick_velocity, o.hit)
        res["per_day_by_class"] = 100 * day_cls.mean()
        res["per_handling_pooled"] = 100 * ((1 - p1) ** (g.age_f * g.pick_velocity)).mean()
        res["per_handling_by_class"] = 100 * htx_cls.mean()
        res["linear_by_class"] = 100 * lin.mean()
        out[code] = res
    return out


def count_rates(faces, c):
    """Rungs 0 to 2 and the count-based grid cells."""
    out = {}
    flagged = set(map(tuple, c[~c.routine][["site", "location"]].values))
    for code, g in c.groupby("site"):
        fz = faces[faces.site == code]
        share = fz.slot_class.value_counts(normalize=True)
        r = g[g.routine]
        res = {"rung0_all_counts": 100 * g.hit.mean(), "rung1_routine": 100 * r.hit.mean(),
               "rung2_class_weighted": 100 * sum(share[k] * r[r.slot_class == k].hit.mean() for k in "ABC")}
        for w in range(4, 27):
            rw = r[r.day >= W.F - 7 * w]
            res["rung2_last_%dw" % w] = 100 * sum(share[k] * rw[rw.slot_class == k].hit.mean() for k in "ABC")
        fl = np.array([(code, x) in flagged for x in fz.location])
        gfl = np.array([(code, x) in flagged for x in g.location])
        s = 0.0
        for k in "ABC":
            for v in (False, True):
                cell = ((fz.slot_class == k).values & (fl == v))
                rows = ((g.slot_class == k).values & (gfl == v))
                if cell.sum():
                    s += cell.sum() / len(fz) * g[rows].hit.mean()
        res["cell_weighted_flag_class"] = 100 * s
        latest = g.groupby("location").tail(1)
        res["latest_result_per_face"] = 100 * latest.hit.mean()
        out[code] = res
    return out


def partial_cells(faces, c):
    out = {}
    f = last_day(faces, c)
    fr = last_day(faces, c, routine_only=True)
    for code, g in f.groupby("site"):
        o = c[(c.site == code) & c.age.notna()]
        p6 = fit_geom(o.age * o.pick_velocity, o.hit)
        res = {"accrual_from_every_count": 100 * ((1 - p6) ** (g.age_f * g.pick_velocity)).mean()}
        r = c[(c.site == code) & c.routine].copy()
        same = r.location == r.location.shift()
        r["rage"] = np.where(same, r.day - r.day.shift(), np.nan)
        rr = r[r.rage.notna()]
        p5 = fit_geom(rr.rage * rr.pick_velocity, rr.hit)
        gr = fr[fr.site == code]
        res["resets_at_routine_only"] = 100 * ((1 - p5) ** (gr.age_f * gr.pick_velocity)).mean()
        obs = c[(c.site == code) & c.routine & c.age.notna()]
        pd_ = fit_geom(obs.age, obs.hit)
        res["per_day_pooled_classes"] = 100 * ((1 - pd_) ** g.age_f).mean()
        res["counted_taken_as_correct"] = 100 * g.last_day.notna().mean()
        out[code] = res
    return out


def everything(target, **kw):
    faces, c = prepared(target, **kw)
    names = {x["code"]: x["name"] for x in W.CENTRES}
    r3, cr, pc = rung3(faces, c), count_rates(faces, c), partial_cells(faces, c)
    out = {}
    for code in names:
        out[names[code]] = dict(r3[code], **cr[code], **pc[code], in_scope_faces=int((faces.site == code).sum()),
                                count_rows=int((c.site == code).sum()))
    return out


R3_KEYS = ["per_day_by_class", "per_handling_pooled", "per_handling_by_class", "linear_by_class"]
GOLDEN_KEY = "per_day_by_class"


def qualifying(est, key, line=W.LINE):
    return sorted(n for n in W.NAMES if est[n][key] >= line)
