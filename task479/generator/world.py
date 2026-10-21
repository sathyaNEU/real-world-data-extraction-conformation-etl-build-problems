"""The world of task479 (architecture 4): Bellweather Academies, a charter network of fourteen middle-school campuses,
whose spring 2026 math benchmark is delivered and scored by Quantilis Assessment on a three-parameter logistic item
bank. In a few campuses' sessions some students answered many items in a second or two, at the blind-guess rate:
those responses carry nothing about what the student knows, and the vendor's maximum likelihood scores read them as
wrong answers.

    x = build()    the truth: campuses, students, abilities, spring responses and times, fall and winter scores"""
import datetime as dt

import numpy as np

SEED = 4794
D = 1.7
LOT, HOT = 350, 650
BASIC, PROFICIENT = 470, 520
LINE = 0.35
N_ITEMS = 40


def ss(theta):
    return np.clip(np.round(500 + 40 * np.asarray(theta)), LOT, HOT)


TH_LO, TH_HI = (LOT - 500) / 40, (HOT - 500) / 40

# campus id, name, students per grade, mean ability, share of students rapid-guessing in its disengaged sessions,
# which grades sat a disengaged session, its place ("both" over the line either way, "vendor" over on the vendor's
# scores only, "neither")
CAMPUSES = [
    ("C01", "Bellweather Eastgate", 150, -0.56, 0.00, (), "both"),
    ("C02", "Bellweather Riverside", 175, 0.36, 0.00, (), "neither"),
    ("C03", "Bellweather Highpoint", 140, 0.05, 0.62, (7, 8), "vendor"),
    ("C04", "Bellweather Carver Park", 190, -0.60, 0.55, (7, 8), "both"),
    ("C05", "Bellweather Northfield", 120, 0.42, 0.55, (6,), "neither"),
    ("C06", "Bellweather Lakemont", 165, 0.12, 0.58, (6, 7), "vendor"),
    ("C07", "Bellweather Ashby", 130, -0.56, 0.00, (), "both"),
    ("C08", "Bellweather Southridge", 200, 0.30, 0.00, (), "neither"),
    ("C09", "Bellweather Delmar", 145, -0.02, 0.66, (7, 8), "vendor"),
    ("C10", "Bellweather Westbrook", 110, 0.25, 0.00, (), "neither"),
    ("C11", "Bellweather Granger", 160, -0.05, 0.52, (6, 8), "vendor"),
    ("C12", "Bellweather Oak Hollow", 135, 0.48, 0.40, (7,), "neither"),
    ("C13", "Bellweather Fairview", 180, -0.60, 0.00, (), "both"),
    ("C14", "Bellweather Mercer", 125, 0.20, 0.45, (8,), "neither"),
]
NAMES = [c[0] for c in CAMPUSES]
GRADE_SHIFT = {"C04": {6: 0.55, 7: -0.28, 8: -0.28}}     # Carver Park's grade 6 strong, its grades 7 and 8 weak
GRADES = (6, 7, 8)


def bank(rng):
    items = []
    for g in GRADES:
        for k in range(N_ITEMS):
            items.append({"id": "Q%d-%03d" % (g, 101 + 7 * k + g), "grade": g, "pos": k + 1,
                          "a": round(float(rng.uniform(0.75, 1.85)), 3), "b": round(float(rng.normal(0.0, 0.95)), 3),
                          "c": round(float(rng.uniform(0.15, 0.24)), 3)})
    return items


def p3(theta, a, b, c):
    return c + (1 - c) / (1 + np.exp(-D * a * (np.asarray(theta)[..., None] - b)))


def mle(resp, mask, a, b, c, iters=60):
    """Maximum likelihood ability for each row of resp (0/1) over the items where mask is True, bounded to the
    reporting scale's range; a row with every answered item right or wrong goes to the bound."""
    n = resp.shape[0]
    th = np.zeros(n)
    for _ in range(iters):
        p = p3(th, a, b, c)
        q = 1 - p
        w = (p - c) / (p * (1 - c))
        g = (D * a * w * (resp - p) * mask).sum(1)
        info = ((D * a) ** 2 * ((p - c) / (1 - c)) ** 2 * q / p * mask).sum(1)
        step = g / np.maximum(info, 1e-9)
        th = np.clip(th + np.clip(step, -1.0, 1.0), TH_LO, TH_HI)
    return th


def build():
    rng = np.random.default_rng(SEED)
    items = bank(rng)
    students = []
    sid = 0
    for cid, cname, n, mu, share, dgrades, place in CAMPUSES:
        for g in GRADES:
            for i in range(int(round(n * float(rng.uniform(0.9, 1.1))))):
                sid += 1
                theta = float(rng.normal(mu + 0.04 * (g - 7) + GRADE_SHIFT.get(cid, {}).get(g, 0.0), 0.95))
                students.append({"k": sid, "campus": cid, "grade": g, "theta": theta,
                                 "dis": g in dgrades and rng.random() < share * (1.35 if theta < mu else 0.65)})
    # spring responses: engaged answers from the model, rapid guesses at chance with times of a second or two
    for g in GRADES:
        its = [it for it in items if it["grade"] == g]
        a = np.array([it["a"] for it in its])
        b = np.array([it["b"] for it in its])
        c = np.array([it["c"] for it in its])
        st = [s for s in students if s["grade"] == g]
        th = np.array([s["theta"] for s in st])
        pr = p3(th, a, b, c)
        u = rng.random(pr.shape)
        resp = (u < pr).astype(int)
        rt = np.exp(rng.normal(np.log(38) + 0.25 * (b - b.mean()), 0.45, pr.shape))
        rt = np.maximum(rt, 7.5 + rng.random(pr.shape) * 2)
        rapid = np.zeros(pr.shape, dtype=bool)
        for i, s in enumerate(st):
            if s["dis"]:
                start = int(rng.integers(6, 22))
                rapid[i, start:] = rng.random(N_ITEMS - start) < 0.82
            elif rng.random() < 0.01:
                rapid[i, int(rng.integers(30, 38)):] = True
        guess = (rng.random(pr.shape) < 0.25).astype(int)
        resp = np.where(rapid, guess, resp)
        rt = np.where(rapid, 0.6 + rng.random(pr.shape) * 2.2, rt)
        for i, s in enumerate(st):
            s["resp"], s["rt"], s["rapid"] = resp[i], np.round(rt[i], 1), rapid[i]
        vend = mle(resp, np.ones_like(resp, dtype=bool), a, b, c)
        gold = mle(resp, ~rapid, a, b, c)
        for i, s in enumerate(st):
            s["ss_vendor"] = int(ss(vend[i]))
            s["ss_gold"] = int(ss(gold[i]))
            s["ss_true"] = int(ss(s["theta"]))
    # fall and winter scores (the asks): the true ability a little lower earlier in the year, scored with noise
    for s in students:
        s["fall"] = int(ss(s["theta"] - 0.32 + rng.normal(0, 0.28)))
        s["winter"] = int(ss(s["theta"] - 0.15 + rng.normal(0, 0.28)))
    return {"items": items, "students": students}


def shares(x, key):
    out = {}
    for cid in NAMES:
        st = [s for s in x["students"] if s["campus"] == cid]
        out[cid] = sum(s[key] < BASIC for s in st) / len(st)
    return out
