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
    rm = pd.read_csv(os.path.join(pack, "rm_booking_build_s25.csv"), usecols=["flight_no", "dep_date", "sold_out_utc"],
                     dtype={"sold_out_utc": str})
    ref = pd.read_csv(os.path.join(pack, "booking_engine_refusals_s25.csv"), dtype={"session_ref": str})
    ref = ref[((ref["orig"] == "LIN") & ref["dest"].isin(NINE)) | ((ref["dest"] == "LIN") & ref["orig"].isin(NINE))]
    j = ref.merge(rm, on=["flight_no", "dep_date"], how="left", validate="many_to_one")
    assert j["sold_out_utc"].notna().sum() + j["sold_out_utc"].isna().sum() == len(ref)
    j["after"] = j["sold_out_utc"].notna() & (pd.to_datetime(j["logged_utc"], utc=True) >=
                                              pd.to_datetime(j["sold_out_utc"], utc=True))
    return j


def counts(df):
    return {"%s-%s" % k: int(v) for k, v in df.groupby(["orig", "dest"])["pax"].sum().items()}


def paths(j):
    out = {}
    # the cracker: the full-flight condition executed, repeated keys collapsed (battery: key uniqueness)
    out["cracker"] = counts(j[j["after"]].drop_duplicates(["session_ref", "flight_no", "dep_date"]))
    # the cracker who also drops exact duplicates only (no key collapse): every record of a full flight
    out["cracker_exact_dups_only"] = counts(j[j["after"]].drop_duplicates(
        [c for c in j.columns if c not in ("event_id",)]))
    # the mirror: every refusal record is a turned-away request
    out["mirror_every_record"] = counts(j)
    out["mirror_sold_out_departures"] = counts(j[j["sold_out_utc"].notna()].drop_duplicates(
        ["session_ref", "flight_no", "dep_date"]))
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
        print("%-28s %2d of %d figures hit, %.1f per cent of ask weight" % (name, h, len(gold), 100 * share))
    lc = rows["cracker"][1]
    ls = max(rows["mirror_every_record"][1], rows["mirror_sold_out_departures"][1])
    C = 38 + 7 + 55 * lc
    S = 5 + 7 + 55 * ls
    print("cracker on the call %.1f, mirror off the call %.1f: pair ceiling %.1f" % (C, S, (C + S) / 2))
    print("both on the call with the cracker's asks: %.1f" % (38 + 7 + 55 * lc))
    print("mirror leakage %.1f per cent of ask weight" % (100 * ls))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
