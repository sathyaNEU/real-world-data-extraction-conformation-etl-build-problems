"""The operators' quarterly returns: per boiler, coal burned (the boiler's weigh feeders, each with its own small
calibration error), firing hours, steam, light fuel oil for start-ups, and at each quarter's start and end the site's
coal stock (a stockpile survey, to the nearest 10 tonnes) and the scrubber's limestone stock (the silo's level
gauge)."""
import numpy as np

import world as W

QDAYS = [(0, 89), (90, 180), (181, 272), (273, 364)]


def build(w):
    rets = []
    survey = {}
    for b in w.B:
        rng = W.stream(51, *W.key(b))
        yard = w.yard[b["site"]]
        silo = b["silo"]
        feeder = float(np.clip(rng.normal(0, 0.0025), -0.005, 0.005))
        for q, (a, z) in enumerate(QDAYS, start=1):
            coal = float(np.round(b["coal_day"][a:z + 1].sum() * (1 + feeder), 0))
            fire = b["load"][a:z + 1] > 0
            hrs = float(np.round(fire.sum() * 24 - rng.uniform(0, 30), 0))
            steam = float(np.round(coal * float(np.mean(b["gcv_day"][a:z + 1])) * 0.84 / 2.71, -1))
            c_open = yard["opening"] if q == 1 else yard["stock_q"][QDAYS[q - 2][1]]
            c_close = yard["stock_q"][z]
            for key_, v in (((b["site"], q - 1), c_open), ((b["site"], q), c_close)):
                survey.setdefault(key_, float(np.round(v * (1 + rng.normal(0, 0.012)), -1)))
            c_open, c_close = survey[(b["site"], q - 1)], survey[(b["site"], q)]
            l_open = silo["opening"] if q == 1 else silo["stock_q"][QDAYS[q - 2][1]]
            l_close = silo["stock_q"][z]
            l_open = l_open * (1 + rng.normal(0, 0.02)) if q == 1 else prev_close
            l_close = l_close * (1 + rng.normal(0, 0.02))
            prev_close = l_close
            rets.append(dict(boiler=b["id"], site=b["site"], unit=b["unit"], quarter=q, coal_burned=coal, hours=hrs,
                             steam=steam, oil=float(np.round(rng.uniform(4, 22) * len(b["stops"]) / 2, 1)),
                             coal_open=c_open, coal_close=c_close,
                             ls_open=float(np.round(l_open, 0)), ls_close=float(np.round(l_close, 0))))
    w.returns = rets
    return rets


def permits(w):
    out = []
    for b in w.B:
        out.append(dict(boiler=b["id"], site=b["site"], unit=b["unit"], type=b["type"], mwth=b["mwth"],
                        ash_ret=b["ash_ret"], design=b["design"], ratio=b["ratio"]))
    w.permits = out
    return out
