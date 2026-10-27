"""Every figure the goldens and the write-up state, computed from the pack alone, written to figures.json."""
import datetime as dt
import json

import params as P
import solve as S


def compute(target):
    pk = S.Pack(target)
    c = pk.call()
    g, r0 = c["golden"], c["resident"]
    guests = pk.guests()
    parks = sorted(pk.parks, key=lambda p: -p["n"])
    pl = parks[0]
    s3 = g[c["site"]]
    names = {r["site"]: "%s, %s" % (r["town"], r["address"]) for r in pk.sites}
    area = {r["site"]: float(r["proposed_floor_area_m2"]) for r in pk.sites}
    A, B, C = S.ask_a(target), S.ask_b(target), S.ask_c(target)
    tenth = lambda v: round(v / 1e5) / 10.0
    own = [k for k, x in enumerate(pk.stores) if x["own"]]
    park_share = {}
    for p in pk.parks:
        sh = pk.shares(p["xy"], pk.stores)
        park_share[p["pc"]] = sum(sh[k] for k in own)
    side = {"107": "RADDLEFORD WATER HOLIDAY PARK", "105": "WITHYBECK LAKES CARAVAN PARK", "104": "SALLOWMERE MILL CARAVAN PARK"}
    named = {r[9]: (pk.smv[r[6]][0], r[14]) for r in pk.voa if r[6] in pk.smv and pk.smv[r[6]][1] == "pitches"}
    v_direct = sum(guests[k] for k in side) / sum(named[v][0] for v in side.values())
    ad = pk.appraise(v_direct)
    d_site = max(ad, key=lambda k: ad[k]["add"])
    fig_extra = dict(
        park_shares_pct={v.title(): int(round(100 * park_share[named[v][1]])) for v in side.values()},
        v_direct=int(round(v_direct / 10.0) * 10), direct_site=d_site, direct_add=tenth(ad[d_site]["add"]),
        direct_s3=tenth(ad[c["site"]]["add"]),
    )
    fig = dict(
        site=c["site"], site_name=names[c["site"]], add=tenth(c["add"]), add_exact=round(c["add"]),
        V=int(round(c["V"] / 10.0) * 10), V_exact=round(c["V"], 1),
        wrentoft_lakes_pitches=int(pl["n"]),
        s3_sales=tenth(s3["new"]), s3_took=round(s3["took"] / 1e3), s3_cost=round(s3["cost"]),
        s3_resident=tenth(r0[c["site"]]["add"]), resident_site=c["resident_site"],
        s3_resident_rank=["first", "second", "third", "fourth", "fifth", "sixth"][
            sorted(r0, key=lambda k: -r0[k]["add"]).index(c["site"])],
        resident_site_name=names[c["resident_site"]], resident_add=tenth(r0[c["resident_site"]]["add"]),
        runner_up="S1", runner_up_add=tenth(g["S1"]["add"]),
        sites={k: dict(name=names[k], add=tenth(v["add"]), add_exact=round(v["add"]), sales=tenth(v["new"]),
                       sales_exact=round(v["new"]), took=round(v["took"]), cost=round(v["cost"]),
                       resident_add=tenth(r0[k]["add"]), resident_add_exact=round(r0[k]["add"]),
                       area=int(area[k])) for k, v in g.items()},
        guests_by_store={k: round(v) for k, v in sorted(guests.items())},
        parks=[dict(desc=p["desc"], pitches=int(p["n"]), postcode=p["pc"]) for p in parks],
        n_stores_share=len(pk.stores),
        ask_a={k: int(round(v)) for k, v in sorted(A.items())}, ask_a_exact={k: round(v, 2) for k, v in sorted(A.items())},
        ask_b={k: int(round(v)) for k, v in sorted(B.items())}, ask_b_exact={k: round(v, 2) for k, v in sorted(B.items())},
        ask_c={k: int(v) for k, v in sorted(C.items())},
        weeks=25, radius_m=int(P.BUS_RADIUS), margin_pct=int(P.MARGIN * 100), instore_pct=int(P.INSTORE * 100),
        beta=P.BETA, roadf=P.ROADF, min_area=P.MIN_AREA, weeks_year=52, turn_base_min=4, turn_min_per_case=0.02,
        n_park_sites=len(parks), area_code=P.AREA, deterrence_exponent=-P.BETA, bus_day=P.BUS_DAY.day,
        bus_weekday=P.BUS_DAY.strftime("%A"), bus_eve=(P.BUS_DAY - dt.timedelta(days=1)).day,
        store_numbers=sorted(int(k) for k in A),
    )
    fig.update(fig_extra)
    return fig


def write(fig, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    import sys
    f = compute(sys.argv[1])
    print(json.dumps({k: f[k] for k in ("site", "add", "V", "s3_sales", "s3_resident", "resident_site", "resident_add", "runner_up_add")}))
    print(f["sites"])
