"""Write the whole pack into a target folder from the seeded world."""
import datetime as dt
import os

import numpy as np

import docs as DC
import params as P
import pdfs as PD
import records as RC
import world as WO

FILES, PACK, DISTRACTORS, CONTEXT = DC.FILES, DC.PACK, DC.DISTRACTORS, DC.CONTEXT


def build(target, seed=P.SEED):
    os.makedirs(target, exist_ok=True)
    W = WO.simulate(seed)
    V, AW, speeds = RC.build(W, seed)
    V = RC.pas_relabel(V)
    rng = np.random.default_rng([seed, 5])
    n_leg = DC.legacy(target, V, rng)
    n_ev = DC.events(target, V, rng)
    turned = DC.reception_log(target, W, V, AW, rng)
    n_ro = DC.eroster(target, W, rng)
    DC.kiosk(target, W, rng)
    DC.practices(target)
    DC.clinics(target)
    DC.bank_holidays(target)
    DC.survey(target, rng)
    DC.hub_plan(target)
    DC.dictionary(target)
    # report tables from the same records the files carry
    monthly, yearly = {}, {}
    for v in V:
        d, g = v[0], v[1]
        f = WO.fy(d)
        yr = yearly.setdefault(f, {"gp": 0, "h": 0})
        yr["h" if g == "H" else "gp"] += 1
        if f == 2025:
            r = monthly.setdefault((d.year, d.month), {"days": set(), "gp_seen": 0, "h_seen": 0, "gp_away": 0, "h_away": 0, "ro": set()})
            r["days"].add(d)
            r["h_seen" if g == "H" else "gp_seen"] += 1
    for d, g, m in AW:
        if WO.fy(d) == 2025:
            r = monthly[(d.year, d.month)]
            r["h_away" if g == "H" else "gp_away"] += 1
            r["ro"].add(d)
    rows = []
    for ym in sorted(monthly):
        r = monthly[ym]
        rows.append({"ym": ym, "days": len(r["days"]), "gp_seen": r["gp_seen"], "h_seen": r["h_seen"],
                     "gp_away": r["gp_away"], "h_away": r["h_away"], "ro": len(r["ro"])})
    PD.annual_report(os.path.join(target, FILES["report"]), rows, yearly)
    PD.icb_letter(os.path.join(target, FILES["icb"]))
    return {"W": W, "V": V, "AW": AW, "truth": WO.truth(W), "monthly": rows, "yearly": yearly,
            "rows": {"legacy": n_leg, "events": n_ev, "roster": n_ro}}
