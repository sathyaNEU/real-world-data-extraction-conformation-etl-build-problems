"""The reference points as the interpreters recorded them: the main campaign (the laboratory's collection tool,
every point), the quality-control campaign (the ministry's form, one point in five), the adjudication of their
disagreements, and each point's class on the final change map. Each point's true 2024-2025 class drives what the
interpreters saw; the quality-control interpreters never disagree with the main campaign on a field that decides
a point's 2024-2025 class."""
import datetime as dt

import numpy as np

import landscape as L
import world as W

ES_LC = {1: "bosque denso", 2: "bosque abierto", 3: "arbustal", 4: "plantación forestal", 5: "cultivo", 6: "pasto",
         7: "urbano o suelo desnudo", 8: "agua o humedal"}
ES_CANOPY = {"A": "<10%", "B": "10-30%", "C": "30-60%", "D": ">60%"}
ES_CONF = {"H": "alta", "M": "media", "L": "baja"}
ES_CHANGE = {"none": "ninguno", "loss": "pérdida", "gain": "ganancia"}
FINAL_CODE = {"FD": "DEF", "FF": "BOS", "FN": "NOB"}

# each district's block of the national grid (metres): x0, y0, width, height
def district_boxes():
    boxes, x, y = {}, 420_000, 180_000
    for i, (code, _, area, *_rest) in enumerate(W.DISTRICTS):
        side = (area * 10_000) ** 0.5
        col, row = i % 4, i // 4
        boxes[code] = (x + col * 125_000, y + row * 125_000, min(side, 118_000), min(side, 118_000))
    return boxes


def _workday(d):
    """the laboratory and the ministry interpret on working days: a draw on a Saturday is Friday's, on a Sunday
    Monday's"""
    return d - dt.timedelta(days=1) if d.weekday() == 5 else (d + dt.timedelta(days=1) if d.weekday() == 6 else d)


OPERATORS = ["OP01", "OP02", "OP02", "OP03", "OP04", "OP04", "OP05", "OP06", "OP07"]   # two interpreters on half time


def _date(rng, start, end):
    a, b = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    return a + dt.timedelta(days=int(rng.integers(0, (b - a).days + 1)))


def points():
    """every reference point with its stratum, district, true class, final map class and what the main campaign
    recorded"""
    C = L.cells()
    raw = L.draw_sample(W.SAMPLE_SEED, C)
    rng = np.random.default_rng(W.SEED + 5)
    spread = np.random.default_rng(W.SEED + 6)      # the interpreters' canopy calls around each cover class
    boxes = district_boxes()
    out = []
    for i, (s, d, t, f) in enumerate(raw, 1):
        x0, y0, w, h = boxes[d]
        p = dict(plot_id="LFM26-%05d" % i, stratum=s, district=d, true=t, final=f,
                 x=int(x0 + rng.random() * w), y=int(y0 + rng.random() * h),
                 operator=OPERATORS[int(rng.integers(0, 9))],
                 interpreted=_workday(_date(rng, "2026-02-03", "2026-03-27")))
        u = rng.random()
        if t == "D":
            p["lc24"] = 1 if u < 0.6 else 2
            p["cc24"] = "D" if p["lc24"] == 1 else "C"
            v = rng.random()
            p["lc25"] = 6 if v < 0.55 else (5 if v < 0.83 else (7 if v < 0.95 else 8))
            p["cc25"] = "A" if rng.random() < 0.8 else "B"
            p["change"] = "loss"
            p["loss_year"] = 2024 if rng.random() < 0.52 else 2025
            p["loss_month"] = 1 + int(rng.integers(0, 12))
            p["kind"] = "deforestation"
        elif t == "F":
            p["lc24"] = 1 if u < 0.68 else 2
            p["cc24"] = "D" if p["lc24"] == 1 else "C"
            p["lc25"], p["cc25"] = p["lc24"], p["cc24"]
            p["change"], p["loss_year"], p["loss_month"], p["kind"] = "none", None, None, "stable forest"
        else:
            p["change"], p["loss_year"], p["loss_month"] = "none", None, None
            if u < 0.56:
                c = 6 if rng.random() < 0.6 else 5
                p.update(lc24=c, cc24="A", lc25=c, cc25="A", kind="farmland")
            elif u < 0.68:
                p.update(lc24=3, cc24="B", lc25=3, cc25="B", kind="woodland")
            elif u < 0.75:
                cc = "D" if rng.random() < 0.5 else "C"
                p.update(lc24=4, cc24=cc, lc25=4, cc25=cc, kind="plantation")
            elif u < 0.88:
                c = 7 if rng.random() < 0.5 else 8
                p.update(lc24=c, cc24="A", lc25=c, cc25="A", kind="other")
            elif u < 0.95:
                p.update(lc24=6, cc24="A", lc25=6, cc25="A", kind="cleared before 2024",
                         cleared=2021 + int(rng.integers(0, 3)))
            else:
                p.update(lc24=6, cc24="A", lc25=3, cc25="B", change="gain", kind="regrowth")
        _canopy_calls(p, spread)
        p["plantation"] = "Y" if p["lc24"] == 4 else "N"
        p["img24"] = _date(rng, "2023-12-04", "2024-03-15")
        p["img25"] = _date(rng, "2025-10-20", "2026-01-24")
        p["confidence"] = "H" if rng.random() < 0.7 else ("M" if rng.random() < 0.83 else "L")
        p["ref"] = reference_class(p["lc24"], p["cc24"], p["lc25"], p["cc25"], p["loss_year"])
        assert p["ref"] == t, (p, t)
        out.append(p)
    return out


def _canopy_calls(p, rng):
    """interpreters call the canopy class on its own, so it scatters around the cover class: dense forest now and
    then at 30 to 60 per cent, open forest now and then over 60, pasture and cropland with scattered trees, wetland
    with shrubs; never across the 30 per cent line that the forest definition draws for any point"""
    v = rng.random()
    if p["lc24"] == 1:
        p["cc24"] = "D" if v < 0.91 else "C"
    elif p["lc24"] == 2:
        p["cc24"] = "C" if v < 0.88 else "D"
    elif p["lc24"] in (5, 6):
        p["cc24"] = "A" if v < 0.86 else "B"
    elif p["lc24"] == 3:
        p["cc24"] = "B" if v < 0.9 else "A"
    elif p["lc24"] == 8:
        p["cc24"] = "A" if v < 0.8 else "B"
    w = rng.random()
    if p["kind"] in ("stable forest", "farmland", "woodland", "plantation", "other", "cleared before 2024"):
        p["cc25"] = p["cc24"] if w < 0.96 or p["lc25"] in (1, 2, 4) else ("B" if p["cc24"] == "A" else "A")
        if p["lc25"] == 3 and p["cc25"] not in ("A", "B"):
            p["cc25"] = "B"


def reference_class(lc24, cc24, lc25, cc25, loss_year):
    """the 2024-2025 class under the national forest definition (canopy cover of 30 per cent or more, plantations
    excluded) and the reporting period"""
    forest24 = lc24 in W.FOREST_CODES and cc24 in ("C", "D")
    forest25 = lc25 in W.FOREST_CODES and cc25 in ("C", "D")
    if not forest24:
        return "N"
    if forest25:
        return "F"
    return "D" if loss_year in (2024, 2025) else "N"


def qc_campaign(pts):
    """the ministry's quality-control re-interpretation of one point in five, and the adjudication of every field the
    two campaigns recorded differently"""
    rng = np.random.default_rng(W.SEED + 9)
    chosen = sorted(rng.choice(len(pts), size=int(W.QC_SHARE * len(pts)), replace=False))
    qc, adj = [], []
    for k in chosen:
        p = pts[k]
        q = dict(plot_id=p["plot_id"], stratum=p["stratum"], operator="QC%02d" % (1 + int(rng.integers(0, 3))),
                 interpreted=_workday(_date(rng, "2026-03-09", "2026-04-10")), lc24=p["lc24"], cc24=p["cc24"], lc25=p["lc25"],
                 cc25=p["cc25"], change=p["change"], loss_year=p["loss_year"], loss_month=p["loss_month"],
                 confidence=p["confidence"])
        u = rng.random()
        diffs = []
        if p["ref"] in ("D", "F") and u < 0.05:                     # dense against open forest at the start
            q["lc24"] = 2 if p["lc24"] == 1 else 1
            q["cc24"] = "C" if q["lc24"] == 2 else "D"
            diffs += [("lc24", p["lc24"], q["lc24"])] + ([("cc24", p["cc24"], q["cc24"])] if q["cc24"] != p["cc24"]
                                                          else [])
            if p["ref"] == "F":
                q["lc25"], q["cc25"] = q["lc24"], q["cc24"]
                diffs += [("lc25", p["lc25"], q["lc25"])] + ([("cc25", p["cc25"], q["cc25"])]
                                                              if q["cc25"] != p["cc25"] else [])
        elif p["ref"] == "D" and u < 0.30:                          # the month (and now and then the year) of loss
            m = p["loss_month"] + int(rng.choice([-2, -1, 1, 2]))
            yr = p["loss_year"]
            if m < 1 and yr == 2025:
                m, yr = m + 12, 2024
            elif m > 12 and yr == 2024:
                m, yr = m - 12, 2025
            m = min(max(m, 1), 12)
            if (yr, m) != (p["loss_year"], p["loss_month"]):
                q["loss_year"], q["loss_month"] = yr, m
                diffs += [("loss_month", p["loss_month"], m)] + ([("loss_year", p["loss_year"], yr)]
                                                                  if yr != p["loss_year"] else [])
        elif u < 0.11:                                              # confidence
            q["confidence"] = "M" if p["confidence"] == "H" else "H"
            diffs += [("confidence", p["confidence"], q["confidence"])]
        qc.append(q)
        keep_main = rng.random() < 0.6                              # the coordinator settles each point as a whole
        for field, a, b in diffs:
            adj.append(dict(plot_id=p["plot_id"], field=field, main=a, qc=b, adjudicated=a if keep_main else b,
                            by="RSA", on=_date(rng, "2026-04-13", "2026-04-17")))
        assert reference_class(q["lc24"], q["cc24"], q["lc25"], q["cc25"], q["loss_year"]) == p["ref"]
    return qc, adj
