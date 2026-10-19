"""The clean truth of the decision: the eight eligible hospitals' pancreatic resections in 2023 to 2025, each
patient's condition before surgery, the earlier operation on the pancreas or bile ducts that sends a patient on to a
referral centre, harmless earlier procedures on the same organs, complications after the operation and the deaths
within 90 days. Each hospital-year draws from its own stream, so the details written later never move it.

The conditions that differ between patients but not between hospitals (heart failure, kidney disease and the rest,
the conditions that carry no added risk, an earlier gallbladder removal, a stent before a Whipple) are drawn at the
same rate in every hospital-year, so a risk model's choice among them moves no hospital's ratio. What does differ
between hospitals is the operation mix and the earlier operations referral brings."""
import numpy as np
import pandas as pd

H = ["A", "B", "C", "D", "E", "F", "G", "H"]
VOL = dict(A=150, B=125, C=95, D=78, E=66, F=60, G=54, H=48)          # operations a year, 2023 to 2025
REDO = dict(A=.18, B=.15, C=.05, D=.04, E=.04, F=.03, G=.03, H=.03)
TOTAL = dict(A=.14, B=.13, C=.07, D=.06, E=.06, F=.05, G=.05, H=.05)
CHOLE = .03            # an earlier gallbladder removal, every hospital alike, no added risk
STENT = .30            # endoscopic stenting of the bile duct before a Whipple, every hospital alike, no added risk
B0 = -3.45
BETA = dict(age=.40, male=.15, chf=.65, ckd=.45, copd=.35, liver=.70, wtloss=.45, dm=.10, af=.30, total=.50,
            whip=.30, mal=.25, urg=.85, redo=1.20)
PREV = dict(chf=.06, ckd=.09, copd=.10, liver=.04, dm=.30, af=.07)
BACKGROUND = ["htn", "lipid", "gerd", "obese", "smoke", "osa", "thyroid", "depress"]
BG_RATE = .16
EFF = dict(A=-.45, B=.00, C=-.35, D=.12, E=-.25, F=.20, G=.05, H=.30)     # each hospital's own care
COMP = dict(A=-.35, B=-.10, C=.00, D=.10, E=.05, F=.25, G=.65, H=.45)     # complications it lets happen
SEED = 4172


def _exact(r, n, p, among=None):
    """round(p * m) of the m eligible patients, chosen at random."""
    idx = np.arange(n) if among is None else np.flatnonzero(among)
    k = int(round(p * len(idx)))
    out = np.zeros(n, bool)
    if k:
        out[r.choice(idx, size=k, replace=False)] = True
    return out


def core(seed=SEED, eff=None, comp=None):
    eff, comp = eff or EFF, comp or COMP
    rows = []
    for hi, h in enumerate(H):
        for yr in (2023, 2024, 2025):
            r = np.random.default_rng([seed, hi, yr])
            n = int(r.poisson(VOL[h]))
            age = np.clip(r.normal(67, 9.5, n), 25, 92)
            male = r.random(n) < .52
            mal = r.random(n) < .72
            tot = r.random(n) < TOTAL[h]
            whip = (~tot) & (r.random(n) < .66)
            redo = r.random(n) < REDO[h]
            tot = tot | (redo & (r.random(n) < .25))
            whip = whip & ~tot
            urg = r.random(n) < .07
            com = {k: _exact(r, n, p) for k, p in PREV.items()}
            wtloss = _exact(r, n, .20, mal) | _exact(r, n, .06, ~mal)
            chole = _exact(r, n, CHOLE)
            stent = _exact(r, n, STENT, whip)
            x = (BETA["age"] * (age - 67) / 10 + BETA["male"] * male + sum(BETA[k] * com[k] for k in PREV)
                 + BETA["wtloss"] * wtloss + BETA["total"] * tot + BETA["whip"] * whip + BETA["mal"] * mal
                 + BETA["urg"] * urg + BETA["redo"] * redo)
            p = 1 / (1 + np.exp(-(B0 + x + eff[h])))
            dead = r.random(n) < p
            pc = 1 / (1 + np.exp(-(-1.35 + .6 * x + comp[h])))
            cmp_ = np.where(dead, r.random(n) < .85, r.random(n) < pc)
            bg = {k: _exact(r, n, BG_RATE) for k in BACKGROUND}
            rows.append(pd.DataFrame(dict(h=h, year=yr, k=np.arange(n), age=age, male=male, mal=mal, tot=tot,
                                          whip=whip, urg=urg, redo=redo, wtloss=wtloss, chole=chole, stent=stent,
                                          comp=cmp_, dead=dead, p=p, **com, **bg)))
    return pd.concat(rows, ignore_index=True)
