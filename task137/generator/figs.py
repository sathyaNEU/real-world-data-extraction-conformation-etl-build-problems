"""Every owed figure, computed from the shipped files, as the write-up states it."""
import solve as S

QN = {"Q1": "Q1 (April to June)", "Q2": "Q2 (July to September)", "Q3": "Q3 (October to December)",
      "Q4": "Q4 (January to March)"}


def compute(target):
    D, ci, ev, g = S.solve(target)
    fam = S.family(D, ci, g["L"])
    lad = S.ladder(D, target, ci)
    hosp, code_spec = S.ask_hosp(ci, target)
    days = S.clinic_days_list(target)
    sick = S.ask_sick(target, days)
    wk = S.weekly(D, g["b"], g["col"])
    arr25 = g["seen_gp"] + g["away_gp"]
    # the intermediates as a band: the window the fit picks and the window next to it in fit
    aic = g["aic"]
    L2 = sorted(aic, key=aic.get)[1]
    bases = (g["base"], S.deterred(D, "s%d" % L2)[0])
    F = {
        "plan_visits_2027_28": g["plan_r"],
        "plan_unrounded": round(g["plan"]),
        "base_2025_26": round(g["base"]),
        "kept_in_house_2025_26": round(g["kept"]),
        "window_weeks": g["L"],
        "window_runner_up_weeks": L2,
        "base_2025_26_runner_up": round(bases[1]),
        "aic_gap_five_weeks_or_fewer": int(min(aic[l] - aic[g["L"]] for l in aic if l <= 5)),
        "base_2025_26_low": int(round(min(bases), -2)),
        "base_2025_26_high": int(round(max(bases), -2)),
        "kept_in_house_low": int(round(min(bases) - arr25, -2)),
        "kept_in_house_high": int(round(max(bases) - arr25, -2)),
        "plan_unrounded_low": int(round(min(bases) * S.G2, -2)),
        "plan_unrounded_high": int(round(max(bases) * S.G2, -2)),
        "coef_about": round(g["b"], 2),
        "gp_seen_2025_26": g["seen_gp"],
        "gp_turned_away_2025_26": g["away_gp"],
        "gp_arrivals_2025_26": arr25,
        "run_out_days_2025_26": g["ro_days"],
        "clinic_days_2025_26": g["days"],
        "coef_window_share": round(g["b"], 3),
        "coef_se": round(g["se"], 3),
        "growth_pct": 3.5,
        "growth_years": 2,
        "hours_per_day": 7.5,
        "rounding_unit": 2500,
        "default_path_plan": S.rnd(arr25 * S.G2),
        "default_path_unrounded": round(arr25 * S.G2),
        "seen_only_plan": S.rnd(g["seen_gp"] * S.G2),
        "seen_only_unrounded": round(g["seen_gp"] * S.G2),
        "hospital_visits_2025_26": hosp,
        "sickness_by_quarter": {q: {"days_lost": int(round(v["hours"] / 7.5)), "rate_pct": round(v["rate"], 1)}
                                for q, v in sick.items()},
        "weekly_weeks": int(len(wk)),
    }
    X = {"D": D, "ci": ci, "g": g, "fam": fam, "lad": lad, "hosp": hosp, "code_spec": code_spec, "sick": sick, "wk": wk}
    return F, X
