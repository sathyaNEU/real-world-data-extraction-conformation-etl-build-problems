"""The ask layer measured on the cut pack: each path a response could take through the validated database, the figures
it keeps against the golden, the cracker (on the call: the hygiene battery, the codes read as the dictionary gives
them, section 5's 45 minutes taken from the codes) and the mirror (off the call, the same care), and the pair ceiling.
    python3 pair.py [target]      (--paths prints every path's figures)"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import solve as S
import writeup as WU

TASK = os.path.dirname(HERE)
STATIONS = WU.STATIONS

# each path: its arguments and the silent devices it has found (t: the titration hours coded valid, m: the spare's
# hours under MAG, l: the 0 degrees C loggers)
PATHS = {
    "golden": ({}, "tml"),
    "the database as delivered, V and R, each row once": (dict(gpt=False, spare=False, logger=None), ""),
    "the same, V only": (dict(gpt=False, spare=False, logger=None, r_valid=False), ""),
    "the same, the re-sent days kept": (dict(gpt=False, spare=False, logger=None, dedupe=False), ""),
    "titration hours found": (dict(spare=False, logger=None), "t"),
    "titration hours found on the sheets' clock as solar": (dict(spare=False, logger=None, cest=False), "t"),
    "MAG found": (dict(gpt=False, logger=None), "m"),
    "loggers found": (dict(gpt=False, spare=False), "l"),
    "titration hours and MAG found": (dict(logger=None), "tm"),
    "titration hours and loggers found": (dict(spare=False), "tl"),
    "MAG and loggers found": (dict(gpt=False), "ml"),
}


def main(target):
    D = S.load(target, B.FILES)
    import pandas as pd
    D["db_raw"] = pd.read_csv(os.path.join(target, B.FILES["database"]), sep=";", decimal=",",
                              dtype={"stazione": str, "codice": str})
    D["db_raw"]["t"] = pd.to_datetime(D["db_raw"]["data_ora_solare"], format="%d/%m/%Y %H:%M")
    res = {k: S.asks(D, **v[0]) for k, v in PATHS.items()}
    g = res["golden"]
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    assert all(g[s]["valid"] == fig["asks"]["valid_hours_2027"][s]
               and round(g[s]["mean"], 1) == fig["asks"]["mean_2027_ugm3"][s]
               and int(round(g[s]["p19"])) == fig["asks"]["p19_2027_ugm3"][s] for s in STATIONS), \
        "pair.py's golden path is the golden"
    n = 3 * len(STATIONS)
    sc = {}
    for k, p in res.items():
        a = sum(int(p[s]["valid"] == g[s]["valid"]) for s in STATIONS)
        m = sum(int(round(p[s]["mean"], 1) == round(g[s]["mean"], 1)) for s in STATIONS)
        c = sum(int(round(p[s]["p19"]) == round(g[s]["p19"])) for s in STATIONS)
        sc[k] = a + m + c
        print("  %-58s valid %2d/16  mean %2d/16  19th %2d/16   %2d/%d" % (k, a, m, c, a + m + c, n))
        if "--paths" in sys.argv:
            print("      ", [p[s]["valid"] for s in STATIONS], [round(p[s]["mean"], 1) for s in STATIONS],
                  [round(p[s]["p19"]) for s in STATIONS])
    natural = [k for k in res if PATHS[k][1] == ""]
    one = [k for k in res if len(PATHS[k][1]) == 1]
    two = [k for k in res if len(PATHS[k][1]) == 2]
    kc = max(sc[k] for k in natural)
    ks = kc
    lc, ls = kc / n, ks / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    print("cracker (the codes as the dictionary gives them, the hygiene battery, section 5's 45 minutes from the codes) "
          "keeps %d of %d; the mirror the same" % (kc, n))
    print("pair ceiling %.1f ((%.1f + %.1f) / 2); mirror leakage %.0f per cent of ask weight" % ((c + s) / 2, c, s,
                                                                                                100 * ls))
    k1, k2 = max(sc[k] for k in one), max(sc[k] for k in two)
    print("a reader who finds one silent device keeps at most %d of %d (%.1f with the call); two, %d (%.1f with the "
          "call)" % (k1, n, 38 + 7 + 55 * k1 / n, k2, 38 + 7 + 55 * k2 / n))
    return sc


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else os.path.join(TASK, "target"))
