"""task241 owed figures (figures.json) and the submission, both emitted from the analysis, never typed."""
import json
import os

import numpy as np
import pandas as pd

import estim as E
import params as P

WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
         11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen", 15: "Fifteen", 16: "Sixteen", 17: "Seventeen",
         18: "Eighteen"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]
BAND = 0.003                     # implementations of the position-mapped reference agree on every offset to within this


def fmt(n):
    return "{:,}".format(int(n))


def r3(x):
    v = round(x, 3)
    return 0.0 if v == 0 else v


def s3(x):
    v = r3(x)
    return "0.000" if v == 0 else "%+.3f" % v


def answers(X, F):
    D = X["D"]
    reg = set(D["reg"]["wmo"])
    pr = D["prof"]
    asc = pr[(pr["direction"] == "A") & pr["wmo"].isin(reg)]
    p2, lv = E.float_layer(D)
    off = X["off"]
    adj = X["adjusted"]
    routes = X["routes"]
    clean = [w for w in off if w not in adj]
    ac = D["ac"].copy()
    ac["when"] = pd.to_datetime(ac["time_utc"])
    ic = D["ic"].copy()
    ic["when"] = pd.to_datetime(ic["date"]) + pd.to_timedelta((ic["time"] * 3600).round(), unit="s")
    matched = 0
    for _, row in ic.iterrows():
        m = ((ac["when"] - row["when"]).abs() <= pd.Timedelta(minutes=15)) & \
            ((ac["latitude"] - row["lat"]).abs() <= 0.02) & ((ac["longitude"] - row["lon"]).abs() <= 0.02)
        matched += int(m.any())
    A = dict(
        files=F, off=off, off3={w: r3(v) for w, v in off.items()}, adjusted=adj, used=X["used"], model=X["model"],
        fresh=[w for w in adj if off[w] < 0], salty=[w for w in adj if off[w] > 0],
        min_adj=r3(min(abs(off[w]) for w in adj)), max_clean=r3(max(abs(off[w]) for w in clean)),
        max_clean_wmo=max(clean, key=lambda w: abs(off[w])),
        casts=X["casts"], casts_arch=X["casts_arch"], casts_other=X["casts_other"], timely=X["timely"],
        surfaced=X["surfaced"],
        profiles=int(asc[["wmo", "cycle"]].drop_duplicates().shape[0]), twice=int(asc.duplicated(["wmo", "cycle"]).sum()),
        partner=sorted(set(pr["wmo"]) - reg), descending=sorted(pr[pr["direction"] == "D"]["wmo"].unique()),
        layer_values=int(len(lv)), arch_casts=int(len(D["ac"])), ipts=int((D["ac"]["temp_scale"] == "IPTS-68").sum()),
        rhd=int(len(D["ic"])), matched=matched,
        rung={r: dict(n=len(E.adjusted(routes[r])), extra=sorted(set(E.adjusted(routes[r])) - set(adj)),
                      missed=sorted(set(adj) - set(E.adjusted(routes[r])))) for r in routes if r != "golden"},
    )
    pv = {n: E.adjusted(E.p_route(D, **kw)) for n, kw in E.P_VARIANTS.items()}
    A["p_variants"] = {n: dict(n=len(a), extra=len(set(a) - set(adj)), missed=sorted(set(adj) - set(a)))
                       for n, a in pv.items()}
    A["p_range"] = (min(v["n"] for v in A["p_variants"].values()), max(v["n"] for v in A["p_variants"].values()))
    A["p_extra_min"] = min(v["extra"] for v in A["p_variants"].values())
    tv = {n: E.adjusted(E.theta_pooled(D, **kw)) for n, kw in E.THETA_POOLED_VARIANTS.items()}
    tv["casts_on_levels"] = E.adjusted(E.theta_local(D, k=100000))
    A["t_variants"] = {n: dict(n=len(a), extra=len(set(a) - set(adj)), missed=sorted(set(adj) - set(a)))
                       for n, a in tv.items()}
    A["t_range"] = (min(v["n"] for v in A["t_variants"].values()), max(v["n"] for v in A["t_variants"].values()))
    A["t_extra_min"] = min(v["extra"] for v in A["t_variants"].values())
    rr = E.reference(D)
    A["theta_span"] = (float(rr["theta"].min()), float(rr["theta"].max()), float(lv["theta"].min()),
                       float(lv["theta"].max()))
    A["on_total"] = sum(A["timely"].values())
    A["surf_total"] = sum(A["surfaced"].values())
    return A


def figures(A):
    return {"call": {"adjusted": A["adjusted"], "adjusted_count": len(A["adjusted"]), "floats": 24, "tolerance": P.TOL,
                     "tolerance_band": [-P.TOL, P.TOL], "array": sorted(A["off3"])},
            "constants": {"ipts68_factor": 1.00024, "fit_theta_origin": 3.5, "cast_depth_dbar": 2000},
            "components": {"offsets_adjusted": {w: A["off3"][w] for w in A["adjusted"]},
                           "fresh": A["fresh"], "salty": A["salty"], "max_clean": A["max_clean"],
                           "max_clean_wmo": A["max_clean_wmo"], "min_adjusted": A["min_adj"], "band": BAND},
            "steps": {"profiles": A["profiles"], "received_twice": A["twice"], "partner": A["partner"],
                      "descending_floats": A["descending"], "layer_values": A["layer_values"],
                      "archive_casts": A["arch_casts"], "ipts68_casts": A["ipts"], "rhd_stations": A["rhd"],
                      "rhd_institute_copies": A["matched"], "layer": list(P.LAYER), "reference_layer": [1300, 2050]},
            "deliverables": {"offsets": A["off3"], "decision": {w: ("adjust" if w in A["adjusted"] else "as measured")
                                                                for w in sorted(A["off3"])},
                             "casts_2000": A["casts"], "timely": A["timely"], "timely_total": A["on_total"],
                             "surfaced_total": A["surf_total"]},
            "rungs": dict(A["rung"], p_variants=A["p_variants"], p_range=list(A["p_range"]),
                          p_extra_min=A["p_extra_min"], t_variants=A["t_variants"], t_range=list(A["t_range"]),
                          t_extra_min=A["t_extra_min"], theta_span=[round(x, 2) for x in A["theta_span"]])}


def submission(A):
    F = A["files"]
    adj = A["adjusted"]
    fr, sa = A["fresh"], A["salty"]
    L = []
    L.append("# task241 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: delayed-mode "
             "calibration of profiling-float salinity against ship CTD reference data).")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting (which floats of an observing array have "
             "their year's salinity record adjusted in the delayed-mode release, with the reference coverage and the "
             "real-time delivery record the release report carries).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Adjust the 2027 salinity of %s of the 24 floats in the delayed-mode release: %s, which read fresh "
             "(offsets %s), and %s, which read salty (%s). The other %d floats' 2027 salinity goes out as measured.**\n"
             % (WORDS[len(adj)].lower(), ", ".join(fr[:-1]) + " and " + fr[-1],
                ", ".join(s3(A["off"][w]) for w in fr), " and ".join(sa), ", ".join(s3(A["off"][w]) for w in sa),
                24 - len(adj)))
    g, p, pl, s = A["rung"]["theta_global"], A["rung"]["p_global"], A["rung"]["p_local"], A["rung"]["self"]
    L.append("Each adjusted float reads %.3f or more from the water it sampled, and the largest offset among the other "
             "floats is %.3f, against the tolerance of %.3f. Below the Mediterranean water the deep layer's temperature identifies the "
             "water, but in 2027 the layer sat deeper than in the reference years and heaved with eddies, and on a "
             "given potential-temperature level the water freshens westward across the basin. So each float's "
             "salinity is compared with the reference water of the same potential temperature at the profile's own "
             "position. Differencing at fixed pressure, against the reference casts' mean or the nearest casts, "
             "adjusts %d to %d floats depending on the levels and casts used, at least %s of them floats whose sensors "
             "read true, because water at a fixed pressure in 2027 was not the water the casts sampled there. "
             "Comparing on potential-temperature levels against the "
             "basin's pooled reference adjusts %d to %d, at least %s of them clean floats on the basin's eastern and "
             "western sides. Measuring "
             "each float against its own first profiles finds only the %s floats that drifted during the year and "
             "misses %s, whose sensors were off from deployment.\n"
             % (A["min_adj"], A["max_clean"], P.TOL, A["p_range"][0], A["p_range"][1], WORDS[A["p_extra_min"]].lower(),
                A["t_range"][0], A["t_range"][1], WORDS[A["t_extra_min"]].lower(), WORDS[s["n"]].lower(),
                " and ".join(s["missed"])))
    L.append("## 2. Critical Components\n")
    L.append("1. The %s floats reading fresh: %s." % (WORDS[len(fr)].lower(), "; ".join(
        "%s **%s**" % (w, s3(A["off"][w])) for w in fr)))
    L.append("2. The %s floats reading salty: %s." % (WORDS[len(sa)].lower(), "; ".join(
        "%s **%s**" % (w, s3(A["off"][w])) for w in sa)))
    L.append("3. The largest offset among the other %d floats is **%s** (%s)." %
             (24 - len(adj), s3(A["off"][A["max_clean_wmo"]]), A["max_clean_wmo"]))
    L.append("")
    L.append("Offsets are in practical salinity and are accepted within %.3f of these values: any mapping of the "
             "reference water to the profile's position on potential-temperature levels (nearest casts, casts within "
             "a few degrees, a fit in position) reproduces each offset to within %.3f, the third decimal moving with "
             "the mapping, and every such mapping adjusts the same %s floats.\n" % (BAND, BAND, WORDS[len(adj)].lower()))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took the array's 24 floats from %s and their 2027 ascending profiles from %s: %s profiles, %d of them "
             "received twice (file_version 1 broke off part way; file_version 2 carries every level, and is the one "
             "used). The partner float %s, decoded beside the array, and the descending profiles of floats %s are "
             "left out (%s)."
             % (F["register"], F["profiles"], fmt(A["profiles"]), A["twice"], ", ".join(A["partner"]),
                ", ".join(A["descending"]), F["thread"]))
    L.append("2. Joined the levels in %s and kept the good values, flag 1 or 2 in pressure, temperature and "
             "salinity, between 1,400 and 1,900 dbar: %s values in %s profiles."
             % (F["levels"], fmt(A["layer_values"]), fmt(A["profiles"])))
    L.append("3. Built the reference water from both sources named in %s: the institute's archive (%s and %s, %d "
             "casts; the %d casts of the 2015 and 2016 cruises in IPTS-68, divided by 1.00024 for ITS-90) and the RHD "
             "extract (%s and %s, %d stations; depths taken to pressure by Saunders 1981)."
             % (F["refnote"], F["arch_casts"], F["arch_levels"], A["arch_casts"], A["ipts"], F["intl_casts"],
                F["intl_levels"], A["rhd"]))
    L.append("4. Computed potential temperature referred to the surface (EOS-80) for every float level and every "
             "reference level.")
    L.append("5. Fitted the reference salinity between 1,300 and 2,050 dbar on potential temperature theta and "
             "position: S = a + b theta + c theta^2 + (theta - 3.5)(d longitude + e latitude), least squares. The "
             "reference levels' potential temperatures (%.2f to %.2f) span every float level's used (%.2f to %.2f), so "
             "the fit is read only inside its own range." % A["theta_span"])
    L.append("6. For each profile, the mean over its good layer values of the float's salinity less the fitted "
             "reference salinity at the value's potential temperature and the profile's position; for each float, "
             "the mean over its 2027 ascending profiles (%s)." % F["thread"])
    L.append("7. Applied the tolerance in %s, an offset more than %.3f in magnitude: %s floats are adjusted."
             % (F["thread"], P.TOL, WORDS[len(adj)].lower()))
    L.append("8. Reference casts reaching 2,000 dbar: an archive cast counts when its max_pres is 2,000 or more; an "
             "RHD station when its deepest depth, taken to pressure, is 2,000 dbar or more. %d RHD stations are the "
             "institute's own casts under RHD ids (time within 15 minutes and position within 0.02 degree of an "
             "archive cast) and count once; casts the archive holds twice at one station a few hours apart are two "
             "casts. Counted by the year of the cast." % A["matched"])
    L.append("9. Delivery record: each of the array's ascending profiles, by the month the float surfaced, the end "
             "of the ascent (ascent_end in %s; the model K floats' juld is the start of the ascent, about six hours "
             "earlier). Its time of arrival is the receipt of the file carrying every level in %s, the server's "
             "Lisbon time taken to UTC. Counted when that is within 24 hours of surfacing: %d of %s profiles in "
             "2027." % (F["technical"], F["deliveries"], A["on_total"], fmt(A["surf_total"])))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### ioa_dmqc_salinity_2027.xlsx\n")
    L.append("1. Each float's 2027 offset (practical salinity, three decimals; accepted within %.3f, the third "
             "decimal moving with the mapping of the reference to the profile's position) and decision:" % BAND)
    for w in sorted(A["off3"]):
        L.append("   - %s: %s, %s" % (w, s3(A["off"][w]), "adjust" if w in adj else "release as measured"))
    L.append("2. Reference casts reaching 2,000 dbar, by year: %s." % "; ".join(
        "%d %d" % (y, A["casts"][y]) for y in sorted(A["casts"])))
    L.append("3. The array's ascending profiles that reached the data centre in full within 24 hours of the float "
             "surfacing, by the month the float surfaced: %s." % "; ".join(
                 "%s %d" % (MONTHS[m - 1], A["timely"][m]) for m in range(1, 13)))
    L.append("")
    L.append("### ioa_dmqc_offsets_2027.png\n")
    L.append("4. One bar per float with its 2027 offset, the tolerance band from %.3f to +%.3f shaded, and the %s "
             "adjusted floats (%s) marked." % (-P.TOL, P.TOL, WORDS[len(adj)].lower(), ", ".join(adj)))
    return "\n".join(L) + "\n"


def write(task, here, A):
    fig = figures(A)
    with open(os.path.join(here, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=2, sort_keys=True, default=str)
        fh.write("\n")
    with open(os.path.join(task, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
