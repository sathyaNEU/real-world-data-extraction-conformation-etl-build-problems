"""Limits: each stream's contract limit is set from its closed-quarter measured residual (the pilot's for
Hollings & Pryce) at the ratio the ladder needs, to one decimal of an error per 1,000 key fields."""
import world as W

Q3_RATIO = {"N1": 1.14, "N2": 1.12, "N3": 1.13, "N4": 1.65, "N5": 1.13, "D1": 0.50, "D2": 0.82, "D3": 0.84,
            "D4": 0.84, "D5": 0.82, "D6": 0.89}
# Hollings & Pryce's schedule, the newest contract, states its limit to two decimals
DECIMALS = {"D6": 2}


def limits(q3m):
    return {c: round(q3m[c] / Q3_RATIO[c], DECIMALS.get(c, 1)) for c in W.ORDER}
