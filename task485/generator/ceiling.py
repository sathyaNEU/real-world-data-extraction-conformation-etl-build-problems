"""The ask layer's pair ceiling on the cut pack (supplemental-stumping Part 0 and 1.1). The cracker lands the call,
runs the hygiene battery (exact duplicates, unmatched herds, units, scope by material and service, the window) and
sums every contractor job as exported; the mirror stops off the call and reads the contractors the same way. The ask
reads no row the call reads, so the two share their ask reading by construction (checks.py, separation); each
half-handled stop is scored beside them.

    python3 task485/generator/ceiling.py
"""
import json
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
GAL = 0.00454609
LO, HI = pd.Timestamp("2026-01-13"), pd.Timestamp("2026-04-30")


def load():
    hr = pd.read_excel(os.path.join(T, "nbr_herd_register_2026-11.xlsx"), sheet_name="Herds", dtype=str)
    hr = hr[hr["Valid to"].isna()]
    region = dict(zip(hr["Herd No"], hr["Region"]))
    av = pd.read_csv(os.path.join(T, "vale_agri_jobs_2026.csv"), dtype=str)
    av["date"] = pd.to_datetime(av["Date"], format="%d/%m/%Y")
    nm = pd.read_excel(os.path.join(T, "basin_agri_job_sheets_2026.xlsx"), sheet_name="Job sheets 2026",
                       dtype={"Herd No": str})
    nm["date"] = pd.to_datetime(nm["Date"])
    kb = pd.read_excel(os.path.join(T, "countrywide_invoice_lines_2026.xlsx"), sheet_name="Invoice lines",
                       dtype={"Reference": str, "Herd No": str})
    kb["date"] = pd.to_datetime(kb["Invoice date"])
    kb["herd"] = kb["Herd No"].str.replace(" ", "", regex=False)
    return region, av, nm, kb


def route(L, dedup="ref", keep="sheet", nominal=False, hazards=False, near=False, raw_herds=False):
    region, av, nm, kb = L
    a = av if hazards else av[av["Material"] == "CATTLE SLURRY"]
    n = nm if hazards else nm[nm["Product"] == "Cattle slurry"]
    k = kb[kb["Service"].str.startswith(("SS-", "PS-", "DS-") if hazards else "SS-")]
    if not hazards:
        a, n, k = a[a["date"].between(LO, HI)], n[n["date"].between(LO, HI)], k[k["date"].between(LO, HI)]
    refs = set(av["Job No"]) | set(nm["Job No"])
    passed = set(k["Reference"]) & refs
    if dedup == "ref":
        if keep == "sheet":
            k = k[~k["Reference"].isin(refs)]
        else:
            a, n = a[~a["Job No"].isin(passed)], n[~n["Job No"].isin(passed)]
    if near:
        days = set(zip(a["Herd No"], a["date"])) | set(zip(n["Herd No"], n["date"]))
        k = k[[(h, d) not in days for h, d in zip(k["herd"], k["date"])]]
    hk = k["Herd No"] if raw_herds else k["herd"]
    rows = [pd.DataFrame(dict(region=a["Herd No"].map(region),
                              m3=a["Loads"].astype(int) * (2000 if nominal else a["Capacity (gal)"].astype(int)) * GAL,
                              less=a["Spreader"].isin(["TRAILING SHOE", "DRIBBLE BAR"]))),
            pd.DataFrame(dict(region=n["Herd No"].map(region), m3=n["Metered m3"].astype(float), less=True)),
            pd.DataFrame(dict(region=hk.map(region), m3=k["Qty"].astype(float) * 1000 * GAL,
                              less=k["Service"].isin(["SS-TS", "SS-TH", "SS-UMB", "SS-INJ", "DS-TS"])))]
    x = pd.concat(rows).dropna(subset=["region"])
    x["lm3"] = x["m3"] * x["less"]
    g = x.groupby("region")[["m3", "lm3"]].sum()
    return {r: ("{:,.0f}".format(round(g.loc[r, "m3"], -2)), "%.1f" % (100 * g.loc[r, "lm3"] / g.loc[r, "m3"]))
            for r in g.index}


def keeps(gold, other):
    return sum((other.get(r, ("", ""))[0] == gold[r]["m3"]) + (other.get(r, ("", ""))[1] == gold[r]["less_pct"])
               for r in gold)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    gold = f["ask_a"]
    L = load()
    g = route(L)
    assert all(g[r] == (gold[r]["m3"], gold[r]["less_pct"]) for r in gold), "the golden handling does not reproduce"
    stops = {
        "every job as exported (the cracker)": route(L, dedup=None),
        "Countrywide's lines kept, the job sheets they bill dropped": route(L, keep="invoice"),
        "a Countrywide line beside a same-day job on the herd dropped": route(L, dedup=None, near=True),
        "the reference read, Vale Agri's loads at 2,000 gallons": route(L, nominal=True),
        "the reference read, pig slurry, digestate and May kept": route(L, hazards=True),
        "the reference read, Countrywide's spaced herd numbers left unmatched": route(L, raw_herds=True),
    }
    n = 2 * len(gold)
    print("ask A, each region's cattle slurry spread by contractors and its low-emission share: %d figures" % n)
    for k, v in stops.items():
        print("  %-70s keeps %2d" % (k, keeps(gold, v)))
    crack = mirror = keeps(gold, stops["every job as exported (the cracker)"])
    lc, lm = crack / n, mirror / n
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * lm
    print("cracker keeps %d of %d ask figures (%.1f per cent), scores %.1f with the call" % (crack, n, 100 * lc, c))
    print("mirror keeps %d of %d (%.1f per cent), scores %.1f off it" % (mirror, n, 100 * lm, s))
    best = max(keeps(gold, v) for v in stops.values())
    print("the best half-handled response keeps %d of %d (%.1f per cent)" % (best, n, 100 * best / n))
    print("Pair ceiling: %.1f" % ((c + s) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * lm))
    return dict(crack=crack, mirror=mirror, n=n, pair=(c + s) / 2, partial=best)


if __name__ == "__main__":
    main()
