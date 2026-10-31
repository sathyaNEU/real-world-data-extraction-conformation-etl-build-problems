"""figures.json: every number the write-up states, as the write-up states it."""
import golden as GD

THRESHOLD = 540


def fmt(x):
    return "{:,}".format(int(x))


def figures(F, n_checks):
    G = F["G"]
    S = GD.summary(F)
    r = G["rates"]
    pct = lambda v: "%.1f" % (100 * v)
    return {
        "call": "Add the third return-inspection officer for 2027: the routine inspections in the 2027 schedule are "
                "forecast to produce about %s unsatisfactory inspections, above the plan's 540." % fmt(S["total_r"]),
        "forecast_total": fmt(S["total_r"]),
        "forecast_unrounded": "%.1f" % S["total"],
        "threshold": fmt(THRESHOLD),
        "scheduled_routine_inspections": fmt(S["n"]),
        "first_visits_2027": fmt(S["first"]),
        "second_visits_2027": fmt(S["second"]),
        "later_visits_2027": fmt(S["later"]),
        "rate_first_visit": {str(k): pct(r[(k, 0)]) for k in (1, 2, 3)},
        "rate_second_visit": {str(k): pct(r[(k, 1)]) for k in (1, 2, 3)},
        "rate_later_visit": {str(k): pct(r[(k, 2)]) for k in (1, 2, 3)},
        "rung_category": "%.0f" % F["routes"]["category"],
        "rung_own_history": "%.0f" % F["routes"]["own"],
        "rung_inspector": "%.0f" % F["routes"]["inspector"],
        "ask_a_median_working_days": {str(d): "%.1f" % F["A"][d] for d in sorted(F["A"])},
        "ask_b_median_hours": {str(d): "%.1f" % F["B"][d] for d in sorted(F["B"])},
        "ask_c_fees_usd": {str(d): fmt(F["C"].get(d, 0)) for d in sorted(F["A"])},
        "fee_rates_usd": ["152", "168"],
        "daysheet_match_days": "20",
        "checks": n_checks,
    }
