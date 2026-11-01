"""figures.json: every number the write-up states, as the write-up states it."""
import golden as GD
import world as W


def fmt(x):
    return "{:,}".format(int(round(x)))


def figures(F, n_checks):
    S = GD.summary(F)
    A = S["asks"]
    y = S["ytd"]
    return {
        "call": "No: Redbud forecasts about %d recordable injuries on Pinewater work in 2027, a rate of %.2f per "
                "200,000 hours on the 2027 work plan, above CS-4's limit of 3.0." % (S["total"], S["rate"]),
        "forecast_recordables_2027": fmt(S["total"]),
        "forecast_rate_2027": "%.2f" % S["rate"],
        "forecast_quarters": [fmt(v) for v in S["quarters"]],
        "forecast_quarter_rates": ["%.2f" % v for v in S["qrates"]],
        "plan_hours_2027": fmt(S["hours"]),
        "plan_quarter_hours": [fmt(v) for v in S["qhours"]],
        "limit": "3.0",
        "crew_rate_first_35_days": "%.2f" % S["clean"],
        "technician_rate": "%.2f" % S["tech"],
        "crew_rate_recorded": "%.2f" % S["recorded_crew"],
        "all_rate_recorded": "%.2f" % S["recorded"],
        "naive_recordables_2027": fmt(S["naive"]),
        "ask_cases_2026": {dd: str(A[dd]["cases"]) for dd in W.DISTRICTS},
        "ask_crew_rate_2026": {dd: "%.2f" % A[dd]["crew_rate"] for dd in W.DISTRICTS},
        "ask_hours_2026": {dd: fmt(A[dd]["hours"]) for dd in W.DISTRICTS},
        "ask_rate_2026": {dd: "%.2f" % A[dd]["rate"] for dd in W.DISTRICTS},
        "ask_awards_2026": {dd: str(A[dd]["milestones"]) for dd in W.DISTRICTS},
        "ask_award_usd_2026": {dd: fmt(A[dd]["usd"]) for dd in W.DISTRICTS},
        "ytd_totals_2026": {"cases": str(y["cases"]), "hours": fmt(y["hours"]),
                            "rate": "%.2f" % y["rate"], "awards": str(y["milestones"]), "usd": fmt(y["usd"])},
        "bins": [["%d-%d" % (lo, hi - 1), int(n), "%.2f" % r] for lo, hi, n, e, r in F["bins"]],
        "checks": n_checks,
    }
