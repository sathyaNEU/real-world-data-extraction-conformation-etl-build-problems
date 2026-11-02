"""Builds task454: the world, the pack under target/, the goldens, figures.json and target.zip."""
import os, sys, json, shutil, zipfile, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from world import *
import sim, pack, calc, golden, metadata

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
G = os.path.join(TASK, "golden")
SCRATCH = os.environ.get("T454_SCRATCH", "/tmp/claude-0/-home-user-real-world-data-extraction-conformation-etl-build-problems/aa89d852-d261-54bf-a8a2-dbdcaa1de391/scratchpad/t454_build")


def world():
    rng = np.random.default_rng(SEED)
    sa2s = sim.geography(rng)
    cards, n, weight, popc = sim.sample(rng, sa2s)
    sim.routine_rows(rng, cards)
    sim.trips(rng, cards, weight, sim.region_erp(sa2s))
    sim.addresses(np.random.default_rng(SEED + 13), cards, sa2s)
    sim.publish_erp(np.random.default_rng(SEED + 29), sa2s)
    rpop = sim.region_erp(sa2s)
    rng2 = np.random.default_rng(SEED + 7)
    agreements, claims, payments, receipts, vendor_ref = sim.program(rng2)
    return dict(rng=rng, sa2s=sa2s, rpop=rpop, cards=cards, n=n, weight=weight, popc=popc, agreements=agreements,
                claims=claims, payments=payments, receipts=receipts, vendor_ref=vendor_ref)


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    W = world()
    for d in (T, G):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    rng = np.random.default_rng(SEED + 11)
    nrows = pack.write_sample(T, W["cards"], W["weight"], rng, W["sa2s"])
    pack.write_erp(T, W["sa2s"])
    pack.write_totals(T, W["cards"], W["weight"], rng)
    pack.guidelines(T, W["sa2s"])
    pack.program_files(T, W["agreements"], W["claims"], W["payments"], W["receipts"], rng)
    pack.closure(T)
    # the golden's quantities (weights as shipped, rounded to four decimals)
    w4 = {h: round(v, 4) for h, v in W["weight"].items()}
    gold = calc.golden(W["cards"], w4, W["rpop"])
    A, B, total, grant = calc.asks(W["agreements"], W["claims"], W["payments"], W["receipts"])
    golden.write_csv(G, gold, W["rpop"])
    golden.paper(G, gold, W["rpop"], A, B, total, grant, SCRATCH)
    figs = figures(gold, W["rpop"], A, B, total, grant, nrows)
    # the separation the classification rests on, measured on the sample
    pairs = [(len(c.months_in(r)), c.days_in(r)) for c in W["cards"] for r in {rr for (rr, m) in c.rows}]
    rout = [(k, d) for k, d in pairs if calc.routine_pair(k, d)]
    trip = [(k, d) for k, d in pairs if not calc.routine_pair(k, d)]
    figs.update({"trip_max_months": max(k for k, d in trip), "trip_max_days": max(d for k, d in trip),
                 "routine_min_months": min(k for k, d in rout), "routine_min_days": min(d for k, d in rout),
                 "sample_cards": len(W["cards"]), "appropriation": ROUND_BUDGET})
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    metadata.write(TASK, T)
    z = os.path.join(TASK, "target.zip")
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for fn in sorted(os.listdir(T)):
            zi = zipfile.ZipInfo(fn, date_time=(2027, 2, 5, 9, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, open(os.path.join(T, fn), "rb").read())
    print("built", nrows, "sample rows;", hashlib.md5(open(z, "rb").read()).hexdigest())
    return W, gold


def figures(gold, rpop, A, B, total, grant, nrows):
    f = {"call": [NAME[r] for r in gold["set"]], "call_codes": gold["set"],
         "first_below": NAME[gold["sixth"]], "fifth": NAME[gold["fifth"]],
         "gap_per_resident": int(round(gold["per_resident"][gold["fifth"]])) - int(round(gold["per_resident"][gold["sixth"]])),
         "margin": round(gold["margin"], 4), "sample_rows": nrows, "round_total": int(round(total)), "grant_each": int(round(grant))}
    for r in ELIGIBLE:
        q = gold["q"][r]
        f["q_%s" % r] = [golden.r1000(x) for x in q]
        f["total_%s" % r] = golden.r1000(sum(q))
        f["per_resident_%s" % r] = int(round(gold["per_resident"][r]))
        f["erp_%s" % r] = round(rpop[r], 2)
        f["remaining_%s" % r] = int(round(A[r]))
        f["unspent_%s" % r] = int(round(B[r]))
    f["remaining_all"] = sum(int(round(A[r])) for r in ELIGIBLE)
    f["unspent_all"] = sum(int(round(B[r])) for r in ELIGIBLE)
    f["round_total"] = ROUND_BUDGET + f["unspent_all"] - f["remaining_all"]
    return f


if __name__ == "__main__":
    main()
