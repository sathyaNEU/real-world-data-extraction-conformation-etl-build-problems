"""Tuning report: each district's 2026 methane per CI/BS mile under every route and the truth."""
import datetime as dt

import methods as M
import truth as T
import world as W


def evaluate():
    segs = T.segments()
    lk = T.leaks(segs)
    odor = [L.found for L in lk if L.how == "ODOR" and L.found.year <= W.YEAR]
    prof = M.profile(odor)
    miles = {}
    for s in segs:
        if s.material in ("CI", "BS"):
            miles[s.district] = miles.get(s.district, 0) + s.miles
    rows = []
    for L in lk:
        if L.found.year != W.YEAR:
            continue
        prev = L.seg.surveys[L.found.year - 1] if L.how == "SURVEY" else None
        if L.how == "SURVEY" and L.seg.surveys[L.found.year] != L.found.date():
            prev = L.seg.surveys[L.found.year]
        rows.append(dict(district=L.seg.district, how=L.how, found=L.found, prev=prev, grade=L.grade,
                         repaired=L.repaired, true=L.start))
    res = {}
    for route in ("record", "mid", "full", "golden"):
        m = M.methane(rows, route, prof, W.RATE, W.END)
        res[route] = {d: m.get(d, 0) / miles[d] for d in miles}
    tr = {}
    for r in rows:
        stop = min(r["repaired"], dt.datetime(2027, 1, 1))
        tr[r["district"]] = tr.get(r["district"], 0) + W.RATE[r["grade"]] * (stop - r["true"]).total_seconds() / 3.6e6
    res["truth"] = {d: tr.get(d, 0) / miles[d] for d in miles}
    return res, prof, rows


if __name__ == "__main__":
    res, prof, rows = evaluate()
    print("profile", " ".join("%.3f" % p for p in prof), "leaks 2026", len(rows))
    for d in W.DISTRICTS:
        print("%-13s m%-2d " % (d, W.DISTRICTS[d][0]) + "  ".join("%s %.3f" % (k[:4], res[k][d]) for k in res))
    for k in res:
        print(k, sorted(d for d, v in res[k].items() if v >= W.LINE))
