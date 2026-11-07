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
        "ask_first_aid_2026_by_quarter": {dd: [str(v) for v in A[dd]["quarters"]] for dd in W.DISTRICTS},
        "ask_first_aid_2026_total": {dd: str(A[dd]["total"]) for dd in W.DISTRICTS},
        "ytd_first_aid_2026": {"quarters": [str(v) for v in y["quarters"]], "total": str(y["total"])},
        "plan_crew_hours_2027": fmt(sum(sum(v) for (dd, t), v in F["plan"].items() if t in ("OH", "UG", "SUB", "VEG"))),
        "plan_technician_hours_2027": fmt(sum(sum(v) for (dd, t), v in F["plan"].items() if t in ("MTR", "LOC"))),
        "limit_recordables_2027": fmt(W.LIMIT * S["hours"] / W.RATE_BASE),
        "count_days": [str(lo) for lo, hi, n, e, r in F["bins"]] + [str(hi - 1) for lo, hi, n, e, r in F["bins"]],
        "count_length_days": str(W.MILESTONE),
        "programme_start": "11 January 2021",
        "bins": [["%d-%d" % (lo, hi - 1), int(n), "%.2f" % r] for lo, hi, n, e, r in F["bins"]],
        "checks": n_checks,
    }
