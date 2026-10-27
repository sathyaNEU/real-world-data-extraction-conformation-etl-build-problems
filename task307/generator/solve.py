"""Golden and ladder: each candidate's 2028 benefit under user equilibrium, and the cheaper routes a solver takes."""
import numpy as np
import params as P
import world, net

CONN_MIN = 60 * 0.2 / 30          # one connector traversal, minutes


def aggregate(od):
    zm = world.zones()
    agg = {}
    for (o, d), q in od.items():
        k = (world.ATTACH[zm[int(o)]], world.ATTACH[zm[int(d)]])
        agg[k] = agg.get(k, 0) + q
    return agg


def project_caps(links, cap, proj):
    c = cap.copy()
    for j, l in enumerate(links):
        if proj["change"] == "lanes" and l["name"] == proj["street"] and (proj.get("segment") is None or l["bottleneck"]):
            c[j] = proj["new_lanes"] * net.LANE_CAP[l["ftype"]]
        if proj["change"] == "lane_capacity" and l["name"] in proj["streets"]:
            c[j] = l["lanes"] * proj["new_lane_cap"]
    return c


def vht(v, t, trips):
    return (v @ t) / 60.0 + trips * 2 * CONN_MIN / 60.0


def equilibrium(links, od, cap, t0, al, be):
    v, t, gap, it = net.ue_paths(links, aggregate(od), cap, t0, al, be)
    assert gap < 1e-9, gap
    return v, t


def run(tabs=None):
    links = world.network()
    cap, t0, al, be = net.link_arrays(links)
    tabs = tabs or world.trip_tables()
    nb = {}
    for per, od in tabs.items():
        v, t = equilibrium(links, od, cap, t0, al, be)
        nb[per] = dict(v=v, t=t, vht=vht(v, t, sum(od.values())))
    res = {}
    for pr in P.PROJECTS:
        c2 = project_caps(links, cap, pr)
        r = {}
        for per, od in tabs.items():
            trips = sum(od.values())
            v, t = equilibrium(links, od, c2, t0, al, be)
            b = nb[per]
            fixed = vht(b["v"], t0 * (1 + al * (b["v"] / c2) ** be), trips)
            r[per] = dict(saved=b["vht"] - vht(v, t, trips), saved_fixed=b["vht"] - fixed, v=v, t=t)
        r["annual"] = (r["AM"]["saved"] + r["PM"]["saved"]) * P.ANNUAL_FACTOR
        r["annual_fixed"] = (r["AM"]["saved_fixed"] + r["PM"]["saved_fixed"]) * P.ANNUAL_FACTOR
        r["per_m"] = r["annual"] / pr["cost_m"]
        res[pr["code"]] = r
    return dict(links=links, nobuild=nb, proj=res, cap=cap, t0=t0, al=al, be=be, tabs=tabs)


if __name__ == "__main__":
    o = run()
    for per in ("AM", "PM"):
        print(per, "no-build VHT %.3f" % o["nobuild"][per]["vht"])
    for c, r in o["proj"].items():
        print(c, "annual %.0f  fixed %.0f  per_m %.0f  AM %.2f PM %.2f" % (r["annual"], r["annual_fixed"], r["per_m"], r["AM"]["saved"], r["PM"]["saved"]))
