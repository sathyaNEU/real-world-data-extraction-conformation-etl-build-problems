"""Screen driver: every reader at one seed, or the pick tally over redraws (python3 screen.py SEED | multi N)."""
import sys
import pandas as pd
import world, records, analysis


def run(seed):
    w = world.simulate(seed)
    rec = records.cut(w, seed)
    t = analysis.base_table(rec, w["accounts"])
    r = analysis.readers(t, rec)
    tr = w["parcels"].groupby("hub").apply(lambda d: (d.p_true - d.p_noequip).sum() / len(d) * 1e4)
    r["truth_equip"] = tr
    return w, rec, t, r


if __name__ == "__main__":
    if sys.argv[1] == "multi":
        from multiprocessing import Pool
        n = int(sys.argv[2])
        def one(s):
            _, _, _, r = run(1000 + s)
            sm = analysis.summarise(r)
            return sm.set_index("reader")[["pick", "second", "lead"]]
        with Pool(4) as p:
            res = p.map(one, range(n))
        cols = res[0].index
        for c in cols:
            picks = pd.Series([x.loc[c, "pick"] for x in res]).value_counts().to_dict()
            secs = pd.Series([x.loc[c, "second"] for x in res]).value_counts().to_dict()
            leads = [x.loc[c, "lead"] for x in res]
            print("%-18s picks %s  second %s  min-lead %.2f" % (c, picks, secs, min(leads)))
    else:
        seed = int(sys.argv[1])
        w, rec, t, r = run(seed)
        pd.set_option("display.width", 250)
        print(r.round(1).T.to_string())
        print(analysis.summarise(r).to_string(index=False))
        print("fits (deviance):", analysis.fits(t))
        for kw in [dict(check_audits=True), dict(notfound_as_ok=True), dict(weight_pick="last"),
                   dict(weight_pick="mean"), dict(order="last")]:
            t2 = analysis.base_table(rec, w["accounts"], **kw)
            g = pd.DataFrame(analysis.golden_family(t2))
            s = analysis.summarise(g)
            print(kw, "golden picks", s.pick.value_counts().to_dict(), "min lead", s.lead.min(),
                  "VLC cells60", round(float(g.loc["VLC", "g_cells_T60"]), 2))
