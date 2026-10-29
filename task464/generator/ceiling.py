"""task464 architecture 10: the cracker and mirror sheets, measured on the cut pack under target/.

    python3 generator/ceiling.py        # prints the sheets and writes generator/ceiling.json

The cracker lands the call (each replaced section's current as the net of every connection beyond it) and, on the asks,
runs the hygiene battery and executes every rule the reporting definitions file: short interruptions out, pre-arranged
interruptions at half weight, the transmission trip and the accepted storm out, customers at 31 March 2026. It does not
treat a mobile generator as restoring or keeping supply (no filed sentence points at the hire log), and it keeps the
work-management LV jobs, whose references, times and causes are their own. The mirror stops at the default path on the
call (the feeder-head current) and handles the asks as the cracker does. A figure is kept when it rounds to the golden.
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import answers as A

BASE = os.path.dirname(HERE)
TGT = os.path.join(BASE, "target")


def digest():
    h = hashlib.md5()
    for n in sorted(os.listdir(TGT)):
        h.update(n.encode())
        h.update(open(os.path.join(TGT, n), "rb").read())
    return h.hexdigest()


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    pk = A.load(TGT)
    rt = A.routes(pk, TGT)
    incs, cust, hires = A.load_interruptions(TGT)
    sc = A.storm_circuits_from_pdf(TGT)
    crack = A.interruption_measures(incs, cust, hires, sc, generators=False, dedupe=False)
    names = A.FEEDER_ORDER
    gold_mwh = {k: F["projects"][k]["year_mwh"] for k in names}
    gold_gbp = {k: F["projects"][k]["value_gbp"] for k in names}

    def kept_mwh(route):
        return sum(round(rt[route][k], 1) == gold_mwh[k] for k in names)

    def kept_gbp(route):
        return sum(int(round(rt[route][k] * A.W.LOSSES_VALUE_GBP_MWH, -2)) == gold_gbp[k] for k in names)
    ci = sum(round(crack[k]["ci"], 1) == F["iis"][k]["ci"] for k in names)
    cml = sum(round(crack[k]["cml"], 1) == F["iis"][k]["cml"] for k in names)
    # ask criteria, one point each: eight savings, eight values, eight CI, eight CML, the chart's four named parts
    # (a bar per project, each labelled with its MWh, the pick highlighted, the pick being the golden's)
    n_ask = 8 + 8 + 8 + 8 + 4
    crk = dict(mwh=kept_mwh("net"), gbp=kept_gbp("net"), ci=ci, cml=cml, chart=4)
    mir = dict(mwh=kept_mwh("head_current"), gbp=kept_gbp("head_current"), ci=ci, cml=cml, chart=2)
    Lc = sum(crk.values()) / n_ask
    Ls = sum(mir.values()) / n_ask
    C = 38 + 7 + 55 * Lc
    S = 5 + 7 + 55 * Ls
    out = dict(pack_md5=digest(), cracker=crk, mirror=mir, ask_criteria=n_ask, Lc=round(Lc, 3), Ls=round(Ls, 3),
               cracker_score=round(C, 1), mirror_score=round(S, 1), pair_ceiling=round((C + S) / 2, 1),
               mirror_leakage_pct=round(100 * Ls, 1),
               device_asks=dict(ci=dict(cracker=ci, of=8), cml=dict(cracker=cml, of=8)),
               cracker_iis={k: [round(crack[k]["ci"], 1), round(crack[k]["cml"], 1)] for k in names})
    json.dump(out, open(os.path.join(HERE, "ceiling.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items() if k != "cracker_iis"}, indent=1, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
