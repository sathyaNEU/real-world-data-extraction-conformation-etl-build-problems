"""The true monthly records and the true mercury released, derived from the simulated works.

The ledger tonnages, the laboratory composites and the dust dispatches are the works' own records of what
happened; the world takes the laboratory's composites as the materials' true content, so the year's true release
to air from each kiln is what entered in raw materials and fuels less what left in clinker and in the filter dust
shipped off site, plus the change in what the meal silo and the dust silo held (asserted negligible).
"""
import datetime as dt

import numpy as np

import world as W


def month_index(world):
    """Local month of each minute (1..12)."""
    return world["mon"]


def build_truth():
    w = W.simulate()
    lab = W.lab_values(w)
    mon = month_index(w)
    out = {"world": w, "lab": lab, "kiln": {}}
    for k, d in w["kilns"].items():
        mix = W.mix_by_month(k, 1 if k == "K1" else 2)
        rows = {}
        for m in W.MONTHS:
            sel = mon == m
            meal = float(d["meal"][sel].sum())
            clk = float(d["clk"][sel].sum())
            coal = float(d["coal"][sel].sum())
            srf = float(d["srf"][sel].sum())
            mats = {}
            for mat, share in mix[m].items():
                q = m if mat not in W.QUARTERLY else (1 + 3 * ((m - 1) // 3))
                moist = lab[(mat, q)]["moist"]
                dry = meal * share
                mats[mat] = dict(dry=dry, wet=dry / (1 - moist / 100.0), q=q)
            fuels = {}
            for f, ar in (("coal", coal), ("srf", srf)):
                if ar > 0:
                    fuels[f] = dict(ar=ar)
            rows[m] = dict(meal=meal, clk=clk, mats=mats, fuels=fuels, bled=float(d["bleed"][sel].sum()),
                           feed_h=float(d["kiln_on"][sel].sum()) / 60.0)
        out["kiln"][k] = dict(rows=rows, mix=mix)
    _dust(out)
    _release(out)
    return out


def _dust(out):
    """K1's filter dust: bled to silo S7 while the kiln is on feed, shipped in bulk tankers on weekdays."""
    w = out["world"]
    d = w["kilns"]["K1"]
    r = np.random.default_rng(W.SEED * 7 + 3)
    bleed = d["bleed"]
    # cumulative bleed by local day
    days = (np.arange(W.NMIN) + w["off"]) // 1440
    day_bleed = np.bincount(days, weights=bleed, minlength=367)[:365]
    s7 = 182.0
    s7_start = s7
    tickets = []
    for day in range(365):
        date = dt.date(2026, 1, 1) + dt.timedelta(days=day)
        s7 += day_bleed[day]
        if date.weekday() < 5:
            # ship while the silo holds more than 260 t, 26 to 30 t a load, at most five loads a day
            loads = 0
            target = 182.0 if date.month == 12 and date.day >= 21 else 260.0
            while s7 > target + 15 and loads < 5:
                net = float(np.clip(r.normal(28.4, 0.9), 26.0, 30.2))
                net = min(net, s7 - 10)
                hh = 7 + loads * 2 + int(r.integers(0, 2))
                mm = int(r.integers(0, 60))
                tickets.append(dict(date=date, hh=hh, mm=mm, net=round(net, 2)))
                s7 -= net
                loads += 1
    out["dust"] = dict(tickets=tickets, s7_start=s7_start, s7_end=s7)


def _release(out):
    lab = out["lab"]
    for k, kd in out["kiln"].items():
        tot_in = tot_clk = tot_dust = 0.0
        monthly = {}
        for m, row in kd["rows"].items():
            hg_in = 0.0
            for mat, v in row["mats"].items():
                hg_in += v["dry"] * lab[(mat, v["q"])]["hg"] / 1000.0      # t x mg/kg = g; /1000 = kg
            for f, v in row["fuels"].items():
                hg_in += v["ar"] * lab[(f, m)]["hg"] / 1000.0          # fuel mercury is reported as received
            hg_clk = row["clk"] * lab[("clinker_" + k, m)]["hg"] / 1000.0
            hg_dust = 0.0
            if k == "K1":
                hg_dust = row["bled"] * lab[("dust_K1", m)]["hg"] / 1000.0
            monthly[m] = dict(hg_in=hg_in, hg_clk=hg_clk, hg_dust=hg_dust)
            tot_in += hg_in
            tot_clk += hg_clk
            tot_dust += hg_dust
        # silo terms: the meal silo's change times the meal's own mercury, the dust silo's change times the dust's
        w = out["world"]["kilns"][k]
        meal_hg = sum(sum(v["dry"] * lab[(mat, v["q"])]["hg"] for mat, v in row["mats"].items())
                      for row in kd["rows"].values()) / sum(row["meal"] for row in kd["rows"].values())
        silo_term = (W.KILNS[k]["silo0"] - float(w["silo"][-1])) * meal_hg / 1000.0
        dust_term = 0.0
        release = tot_in - tot_clk - tot_dust + silo_term
        kd["hg"] = dict(inputs=tot_in, clinker=tot_clk, dust=tot_dust, silo_term=silo_term, dust_term=dust_term,
                        release=release, monthly=monthly)
        # per-minute release: compound rate r_c, direct rate ratio_d x r_c, both scaled by feed
        shape = w["rel_shape"]
        r_c = release * 1000.0 / (shape.sum() / 60.0)        # g per hour at nominal feed in compound operation
        kd["r_c"] = r_c
        kd["rel_g_per_min"] = shape * r_c / 60.0
