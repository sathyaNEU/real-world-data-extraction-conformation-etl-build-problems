"""Read the cut pack the way an analyst would, and run every route the design names on it. Nothing here reads
world.py's truth; golden.py, checks.py, verify.py and ceiling.py all go through it.

    load(target)            the spring responses in one layout, the score reports, the bank, the rosters
    spring(b, route)        each student's spring scale score under a route
    shares(b, scores)       each campus's share of tested students below Basic
    ask_a(b, link)          fall students tested and the share at or above Proficient, by campus
    ask_b(b, link)          students tested fall and winter and their mean growth, by winter campus"""
import csv
import os

import numpy as np

FILES = {
    "resp1": "quantilis_spring2026_item_responses_through_2026-03-27.csv",
    "resp2": "quantilis_spring2026_item_responses_from_2026-03-30.csv",
    "spring": "quantilis_spring2026_score_report.csv",
    "bank": "quantilis_item_bank_2025-26.csv",
    "fall": "quantilis_fall2025_score_report.csv",
    "temp": "quantilis_temporary_id_register_fall2025.csv",
    "winter": "quantilis_winter2026_score_report.csv",
    "roster_f": "bellweather_sis_roster_2025-10-01.csv",
    "roster_s": "bellweather_sis_roster_2026-03-01.csv",
    "xwalk": "bellweather_sis_id_crosswalk_2026-01-05.csv",
}
D = 1.7
LOT, HOT = 350, 650
BASIC, PROFICIENT = 470, 520
LINE = 0.35
RAPID = 5.0          # seconds: no engaged response is faster than 7.5, no rapid one slower than 2.8
ROUTES = ("golden", "vendor", "rescore_all", "drop_rapid_students", "golden_3s", "golden_6s", "drop_rapid_sessions")


def _csv(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load(target):
    bank = {r["item_id"]: (float(r["a"]), float(r["b"]), float(r["c"])) for r in _csv(os.path.join(target, FILES["bank"]))}
    resp = {}
    for r in _csv(os.path.join(target, FILES["resp1"])):
        resp.setdefault(r["StudentID"], []).append((int(r["ItemSeq"]), r["ItemID"], int(r["Scored"]),
                                                    int(r["ResponseTimeMs"]) / 1000.0))
    for r in _csv(os.path.join(target, FILES["resp2"])):
        resp.setdefault(r["student_id"], []).append((int(r["item_seq"]), r["item_id"], int(r["score"]),
                                                     float(r["response_time_s"])))
    spring = {r["student_id"]: r for r in _csv(os.path.join(target, FILES["spring"]))}
    return {"bank": bank, "resp": resp, "spring": spring, "target": target,
            "campuses": sorted({r["campus_id"] for r in spring.values()})}


def _mle(u, a, b, c, m, iters=60):
    th = np.zeros(u.shape[0])
    lo, hi = (LOT - 500) / 40, (HOT - 500) / 40
    for _ in range(iters):
        p = c + (1 - c) / (1 + np.exp(-D * a * (th[:, None] - b)))
        w = (p - c) / (p * (1 - c))
        g = (D * a * w * (u - p) * m).sum(1)
        info = ((D * a) ** 2 * ((p - c) / (1 - c)) ** 2 * (1 - p) / p * m).sum(1)
        th = np.clip(th + np.clip(g / np.maximum(info, 1e-9), -1.0, 1.0), lo, hi)
    return np.clip(np.round(500 + 40 * th), LOT, HOT).astype(int)


def spring(b, route="golden"):
    if route == "vendor":
        return {s: int(r["scale_score"]) for s, r in b["spring"].items()}
    thr = {"golden_3s": 3.0, "golden_6s": 6.0}.get(route, RAPID)
    ids = sorted(b["resp"])
    rows = [sorted(b["resp"][s]) for s in ids]
    u = np.array([[x[2] for x in r] for r in rows])
    t = np.array([[x[3] for x in r] for r in rows])
    a = np.array([[b["bank"][x[1]][0] for x in r] for r in rows])
    bb = np.array([[b["bank"][x[1]][1] for x in r] for r in rows])
    c = np.array([[b["bank"][x[1]][2] for x in r] for r in rows])
    if route in ("golden", "golden_3s", "golden_6s"):
        m = t >= thr
    else:
        m = np.ones_like(u, dtype=bool)
    sc = _mle(u, a, bb, c, m)
    out = dict(zip(ids, sc.tolist()))
    if route == "drop_rapid_students":
        out = {s: v for s, v in zip(ids, sc.tolist()) if (t[ids.index(s)] >= RAPID).all()}
    if route == "drop_rapid_sessions":
        cnt, bad_n = {}, {}
        for s, tt in zip(ids, t):
            r = b["spring"][s]
            k = (r["campus_id"], r["grade"])
            cnt[k] = cnt.get(k, 0) + 1
            bad_n[k] = bad_n.get(k, 0) + ((tt < RAPID).mean() > 0.25)
        bad = {k for k in cnt if bad_n[k] / cnt[k] > 0.10}
        out = {s: v for s, v in out.items() if (b["spring"][s]["campus_id"], b["spring"][s]["grade"]) not in bad}
    return out


def shares(b, scores):
    n, below = {}, {}
    for s, v in scores.items():
        cid = b["spring"][s]["campus_id"]
        n[cid] = n.get(cid, 0) + 1
        below[cid] = below.get(cid, 0) + (v < BASIC)
    return {c: below[c] / n[c] for c in n}


def designate(b, scores):
    sh = shares(b, scores)
    return sorted(c for c in sh if sh[c] >= LINE)


# ------------------------------------------------------------------------------------------------ the asks
def _people(b):
    t = b["target"]
    rf = {r["student_id"]: (r["last_name"], r["first_name"], r["birth_date"]) for r in _csv(os.path.join(t, FILES["roster_f"]))}
    rs = {(r["last_name"], r["first_name"], r["birth_date"]): r["student_id"]
          for r in _csv(os.path.join(t, FILES["roster_s"]))}
    tmp = {r["temporary_student_id"]: (r["last_name"], r["first_name"], r["birth_date"]) for r in _csv(os.path.join(t, FILES["temp"]))}
    who_old = {v: k for k, v in rf.items()}
    return rf, rs, tmp, who_old


def fall_scores(b, link=True):
    """Each fall student's score: with link, temporary ids resolved to the student and the later administration kept;
    without, every row a student."""
    rf, rs, tmp, who_old = _people(b)
    rows = _csv(os.path.join(b["target"], FILES["fall"]))
    out = {}
    for r in sorted(rows, key=lambda r: (r["test_date"], r["student_id"])):
        sid = r["student_id"]
        if link and sid in tmp:
            sid = who_old[tmp[sid]]
        out[sid] = (r["campus_id"], int(r["scale_score"]))
    return out


def ask_a(b, link=True):
    fs = fall_scores(b, link)
    n, prof = {}, {}
    for sid, (cid, v) in fs.items():
        n[cid] = n.get(cid, 0) + 1
        prof[cid] = prof.get(cid, 0) + (v >= PROFICIENT)
    return {c: (n[c], 100.0 * prof[c] / n[c]) for c in n}


def ask_b(b, link=True):
    """Students with a fall and a winter score, by the campus of the winter administration, and their mean growth.
    link: temporary ids resolved and the crosswalk's gaps joined by name and birth date; else the crosswalk alone."""
    rf, rs, tmp, who_old = _people(b)
    xw = {r["legacy_student_id"]: r["student_id"] for r in _csv(os.path.join(b["target"], FILES["xwalk"]))}
    fs = fall_scores(b, link)
    win = {r["student_id"]: (r["campus_id"], int(r["scale_score"])) for r in _csv(os.path.join(b["target"], FILES["winter"]))}
    n, gsum = {}, {}
    for sid, (fc, fv) in fs.items():
        new = xw.get(sid)
        if new is None and link and sid in rf:
            new = rs.get(rf[sid])
        if new is None or new not in win:
            continue
        wc, wv = win[new]
        n[wc] = n.get(wc, 0) + 1
        gsum[wc] = gsum.get(wc, 0) + (wv - fv)
    return {c: (n[c], gsum[c] / n[c]) for c in n}
