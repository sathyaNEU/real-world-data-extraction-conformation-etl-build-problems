"""task131 generator: tuned parameters. The effect profiles are per assigned household (the trial's
intention-to-treat scale) at full heat; the forecast curve is the 2027-28 50% POE design day in MW by half-hour."""

RESP_SHARE = 0.60

EVENTS = {
    "A": {"return": 21, "withdrawn": 1, "lifesupport": 1, "leave_early": 1, "leave": 5, "return_leave": 1,
          "move_keep": 2, "move_home": 0, "return_move": 1},
    "B": {"return": 27, "withdrawn": 1, "lifesupport": 1, "leave_early": 1, "leave": 6, "return_leave": 2,
          "move_keep": 3, "move_home": 0, "return_move": 2},
    "C": {"return": 17, "withdrawn": 1, "lifesupport": 2, "leave_early": 1, "leave": 4, "return_leave": 1,
          "move_keep": 2, "move_home": 0, "return_move": 1},
    "CTRL": {"leave": 6, "leave_early": 1, "move_home": 3},
}
# fourth-decimal adjustments to the gazetted off-peak prices (c/kWh) so each design's mean bill difference sits
# inside its cent
OFFPEAK_NUDGE = {"A": -0.0002, "B": -0.0044, "C": 0.0080}
N_PV_INSTALL = 26
# share of each design's households likely to stay on it, as the March 2026 survey would find with every household answering
SURVEY_STAY = {"A": 0.567, "B": 0.444, "C": 0.604}
N_FAULT = 4
# year-to-year change in a household's summer evening use (kW, sd), which loosens the matched blocks
PRIOR_SD = 0.04
# household day-to-day variation (log-normal sd): whole-day level, base load and air-conditioning by half-hour
NOISE = {"day": 0.04, "base": 0.10, "ac": 0.05}
# the part of that variation every household shares on the day (weather beyond the temperature, the evening's television)
COMMON = {"day": 0.03, "base": 0.08, "ac": 0.08}

# response profiles at full heat, kW per household before the opt-out and attrition dilution
EFF = {
    "cA": 0.475, "cB": 0.5697, "cC": 0.386, "cS": 0.126, "pre": 0.125,
    "sA": 0.6458, "sB": 0.7185, "sC1": 0.1164, "sC2": 0.520, "tm": 0.032, "ex": 3.0,
}

# 2027-28 50% POE design day, MW by half-hour starting 00:00
CURVE = [
    131.8, 127.6, 124.0, 121.1, 118.8, 117.0, 115.7, 114.9, 114.6, 114.8, 115.6, 117.3,
    120.2, 124.6, 129.0, 132.4, 135.3, 138.2, 141.4, 144.9, 148.6, 152.2, 155.9, 159.8,
    163.9, 168.3, 173.0, 177.9, 182.8, 187.6, 192.4, 195.4, 199.3, 203.5, 207.7, 211.6,
    214.6, 213.8, 212.0, 209.5, 204.0, 200.9, 193.1, 185.0, 177.3, 169.6, 161.8, 154.0,
]
CURVE10 = None   # the 10% POE day is the 50% day scaled by the forecast's ratio (docs.py)
