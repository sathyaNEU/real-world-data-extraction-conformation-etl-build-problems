"""Every figure the write-up states, so figures_check.py can hold it to the data."""
import json

import mus
import world as W


def write(g, path):
    month, nabs, absnames, ntwice, twicenames = g["a3"]
    out = {
        "constants": {
            "tolerable_misstatement": W.TOLERABLE,
            "confidence_pct": W.CONFIDENCE,
            "capital_budget_base": W.CAPITAL_BUDGET,
            "stated_to_the_nearest": W.GRAIN,
            "selection_interval_recovered": W.INTERVAL,
            "reliability_factor_nil_overstatements": mus.RF[0],
            "plan_clause_conclusion": 4.3,
            "plan_clause_materiality": 4.2,
            "manual_clause_estimand": 9.1,
            "manual_clause_terms": 9.3,
            "plan_clause_revenue_population": 4.4,
            "manual_clause_reliability_factors": 9.5,
            "manual_clause_records": 9.2,
            "lattice_search_half_width_eur": 40,
        },
        "call": {
            "misstatement_indicated": g["total"],
            "largest_programme": W.PROG_NAME[g["largest"]],
            "largest_programme_misstatement": g["per"][g["largest"]],
            "referred_for_extended_testing": g["referred"],
        },
        "critical_components": {
            "programme_misstatement": {W.PROG_NAME[c]: g["per"][c] for c in W.PROG_CODES},
            "programme_payments_recorded": {W.PROG_NAME[c]: round(g["recorded"][c], 2)
                                            for c in W.PROG_CODES},
            "programme_certain_share_pct": {W.PROG_NAME[c]: g["certain_share"][c]
                                            for c in W.PROG_CODES},
            "authority_certain_share_pct": round(
                100.0 * sum(g["recorded"][c] * g["certain_share"][c] / 100.0
                            for c in W.PROG_CODES) / g["recorded_total"], 1),
            "payments_recorded_total": round(g["recorded_total"], 2),
            "payment_lines": len(g["lines"]),
            "tested_lines": g["tested_lines"],
            "tested_value": round(g["tested_value"], 2),
            "certainty_lines": g["cert_lines"],
            "certainty_value": round(g["cert_value"], 2),
        },
        "steps": {
            "misstatement_found_in_tested_lines": round(g["found"], 2),
            "errors_scaled_on_recorded_value": round(g["ratio"], 2),
            "stratum_ratio": round(g["stratum"], 2),
            "projection_unrounded": round(g["total_raw"], 2),
            "basic_precision": round(g["bp"], 2),
            "incremental_allowance": round(g["ia"], 2),
            "upper_misstatement_limit": round(g["uml"], 2),
            "projection_plus_basic_precision": round(g["crude"], 2),
            "taintings_in_the_sample": g["n_taint"],
            "selections": g["nsel"],
            "prior_year_projection": round(g["prior_total_raw"], 2),
            "sum_of_stated_programme_figures": sum(g["per"].values()),
        },
        "deliverables": {
            "projected_misstatement_2026.csv": {
                "misstatement_indicated_total": g["total"],
                "largest_programme": W.PROG_NAME[g["largest"]],
                "rows": {W.PROG_NAME[c]: [g["per"][c], g["certain_share"][c]]
                         for c in W.PROG_CODES},
            },
            "misstatement_by_population_2026.png": {
                "bars": {W.PROG_NAME[c]: g["per"][c] for c in W.PROG_CODES},
                "marked": W.PROG_NAME[g["largest"]],
            },
        },
        "asks": {
            "runs_by_quarter": {q: list(v) for q, v in g["a1"].items()},
            "risk_moves_by_category": {b: list(v) for b, v in g["a2"].items()},
            "schedule_rows": len(g["paper"]),
            "schedule_rows_resolving_to_the_capital_ledger": len(g["tested"]),
            "capital_ledger_lines_the_paper_covers": sum(g["a3"][0].values()),
            "schedule_lines_by_month": month,
            "schedule_lines_absent_from_the_ledger": nabs,
            "ledger_lines_on_the_schedule_twice": ntwice,
            "ledger_lines_on_the_schedule_twice_names": twicenames,
        },
    }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return out
