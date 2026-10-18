"""ceiling.py: the cracker and the mirror run as code on the cut pack, and the pair ceiling they imply.

    python3 task168/generator/ceiling.py [<unzipped pack dir> | <target.zip>]

The cracker lands the call, runs the hygiene battery (key uniqueness, exact duplicates, unmatched joins, fan-out,
count ties) and executes every condition it is pointed at: here, a request is turned away because the flight was
full when it was logged at or after the departure's sell-out time in the RM build, and a key repeated in the
refusals log (session_ref, flight, date) is one request. The mirror stops at the most attractive wrong rung of the
call and reads the log the natural way. Each figure is scored a hit when it equals the golden (whole passengers,
half a unit of the stated rounding). Weights follow supplemental-stumping Part 0: 38 for the call and its
components, 7 for instruction following, 55 for the asks; a wrong call keeps about 5.
"""
import json
import os
import sys
import tempfile
import zipfile

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
NINE = {"CTA", "PMO", "NAP", "BRI", "BDS", "SUF", "REG", "CAG", "TPS"}


def load(pack):
    rm = pd.read_csv(os.path.join(pack, "rm_booking_build_s25.csv"),
                     usecols=["flight_no", "dep_date", "orig", "dest", "sold_out_utc"], dtype={"sold_out_utc": str})
    ref = pd.read_csv(os.path.join(pack, "booking_engine_refusals_s25.csv"), dtype={"session_ref": str})
    j = ref.merge(rm, on=["flight_no", "dep_date"], how="left", suffixes=("", "_dep"), validate="many_to_one")
    j["after"] = j["sold_out_utc"].notna() & (pd.to_datetime(j["logged_utc"], utc=True) >=
                                              pd.to_datetime(j["sold_out_utc"], utc=True))
    return j


def nine(df, o, d):
    return ((df[o] == "LIN") & df[d].isin(NINE)) | ((df[d] == "LIN") & df[o].isin(NINE))


def counts(df, o="orig", d="dest"):
    return {"%s-%s" % k: int(v) for k, v in df.groupby([o, d])["pax"].sum().items()}


KEY = ["session_ref", "flight_no", "dep_date"]


def paths(j):
    out = {}
    # the cracker: the filed unit executed, the full-flight condition executed against the RM sell-out time, the
    # nine routes read off the records' own airport fields (the first filter a reader applies to a log)
    rec9 = j[nine(j, "orig", "dest")]
    out["cracker (filed unit, sell-out test, record airports)"] = counts(rec9[rec9["after"]].drop_duplicates(KEY))
    # single crack the other way: the departure's route from the RM build, every request for a sold-out departure
    dep9 = j[nine(j, "orig_dep", "dest_dep")]
    out["cracker (filed unit, departure route, departure-level filter)"] = counts(
        dep9[dep9["sold_out_utc"].notna()].drop_duplicates(KEY), "orig_dep", "dest_dep")
    # the mirror: every refusal record of the nine routes is a turned-away request
    out["mirror (every record)"] = counts(rec9)
    out["mirror (sold-out departures, once per reference)"] = counts(
        rec9[rec9["sold_out_utc"].notna()].drop_duplicates(KEY))
    return out


def main(arg):
    if arg.endswith(".zip"):
        tmp = tempfile.mkdtemp()
        with zipfile.ZipFile(arg) as z:
            z.extractall(tmp)
        pack = tmp
    else:
        pack = arg
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gold = figs["turned_away"]
    j = load(pack)
    res = paths(j)
    n = len(gold) + 2            # 18 figures and two value-bound chart criteria (bars present per direction, labels)
    rows = {}
    for name, got in res.items():
        hits = sum(1 for k, v in gold.items() if got.get(k) == v)
        chart = 2 if hits == len(gold) else 0
        rows[name] = (hits, (hits + chart) / n)
    for name, (h, share) in rows.items():
        print("%-66s %2d of %d figures hit, %.1f per cent of ask weight" % (name, h, len(gold), 100 * share))
    names = list(res)
    print("%-8s %7s %s" % ("figure", "golden", " ".join("%7s" % ("p%d" % (k + 1)) for k in range(len(names)))))
    for k in gold:
        print("%-8s %7d %s" % (k, gold[k], " ".join("%7d" % res[n].get(k, 0) for n in names)))
    print("%-8s %7d %s" % ("total", sum(gold.values()), " ".join("%7d" % sum(res[n].values()) for n in names)))
    for k, n in enumerate(names):
        print("p%d %s" % (k + 1, n))
    lc = max(rows["cracker (filed unit, sell-out test, record airports)"][1],
             rows["cracker (filed unit, departure route, departure-level filter)"][1])
    ls = max(rows["mirror (every record)"][1], rows["mirror (sold-out departures, once per reference)"][1])
    C = 38 + 7 + 55 * lc
    S = 5 + 7 + 55 * ls
    print("cracker on the call %.1f, mirror off the call %.1f: pair ceiling %.1f" % (C, S, (C + S) / 2))
    print("both on the call with the cracker's asks: %.1f" % (38 + 7 + 55 * lc))
    print("mirror leakage %.1f per cent of ask weight" % (100 * ls))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
