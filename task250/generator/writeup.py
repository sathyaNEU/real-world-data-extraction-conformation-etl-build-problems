"""figures.json and submission.md, both written from the figures computed on the shipped pack (golden.py for the graded
figures, rungs.py for the routes the recommendation names)."""
import collections
import json

import golden as GD
import rungs as R


def extras(target, F):
    d = GD.load(target, F)
    M, arr, sh, gold = R.main_rungs(d)
    mixed = R.mixed_days(arr, sh)
    a = arr.copy()
    a["day"] = a["scanned_at"].str[:10]
    on_mixed = a[[(dep, x) in mixed for dep, x in zip(a["depot_code"], a["day"])]]
    un = collections.Counter(gold[t] for t in on_mixed["tracking_no"] if t not in sh)
    ldz_sorted = sum(1 for t in on_mixed["tracking_no"] if gold[t] == "HLDZ")
    pick = lambda k, h: round(M[k][h]["rate"], 2)
    return {
        "unloadings": len(set(GD.unloadings(arr)["unloading"])),
        "mixed_mornings": len(mixed),
        "overflow_parcels": ldz_sorted,
        "overflow_missed_strykow": un["HLDZ"],
        "overflow_missed_pruszkow": un["HWAW"],
        "plan": {"HLDZ": pick("R0 plan", "HLDZ"), "HWAW": pick("R0 plan", "HWAW")},
        "shares": {"HLDZ": pick("R1 shares by depot-morning", "HLDZ"), "HWAW": pick("R1 shares by depot-morning", "HWAW")},
        "left_out": {"HWAW": pick("R2 mixed mornings left out", "HWAW"), "HLDZ": pick("R2 mixed mornings left out", "HLDZ")},
        "excess": {"HLDZ": pick("R3 excess over the base rate", "HLDZ"), "HWAW": pick("R3 excess over the base rate", "HWAW")},
    }


def _hub(fig, code):
    return [x for x in fig["hubs"] if x["hub_code"] == code][0]


def _n(v):
    return "{:,}".format(v)


def submission(fig, ex):
    H = {x["hub_code"]: x for x in fig["hubs"]}
    fired = ", ".join(fig["fired"][:-1]) + " and " + fig["fired"][-1]
    under = sorted((x for x in fig["hubs"] if not x["fires"]), key=lambda x: -x["rate"])[0]
    lines = []
    w = lines.append
    w("# task250 submission")
    w("")
    w("## Tags")
    w("")
    w("**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: a parcel carrier's "
      "sort-scan completeness, where the hub an unscanned parcel passed through is itself missing and is recovered from "
      "the unloading it arrived in at its delivery depot).")
    w("**Analytical objective:** Data Quality Monitoring & Alerting (whether the TDS-4 scan alert fires at any of Kurier "
      "Warta's sort hubs for October 2026, and at which).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Fire the October 2026 scan alerts at %s, and at no other hub.**" % fired)
    w("")
    w("Sosnowiec missed %.2f per cent of its sort scans, Strykow %.2f and Pruszkow %.2f, against the 1.00 per cent "
      "tolerance; the nearest hub under it is %s at %.2f. On %d mornings the Warsaw depots unloaded a second trailer "
      "from Strykow, which had sorted %s parcels of Pruszkow's flow by hand; %d of their sort scans are missing, against "
      "%d missing from Pruszkow's own trailers on those mornings, so a parcel without a sort scan is charged to the hub "
      "whose trailer it came off, read from its unloading. Not the sort plan's hub, which charges Strykow's misses to "
      "Pruszkow (Pruszkow %.2f, Strykow %.2f) and leaves Strykow under the line. Not each depot morning's split of its "
      "sorted parcels, which assumes the two hubs missed alike (Strykow %.2f). Not the mornings with two hubs left out "
      "(Pruszkow %.2f, Strykow %.2f), nor the excess over Pruszkow's rate on its other mornings charged to Strykow "
      "(Strykow %.2f, Pruszkow %.2f): Pruszkow's own sorter missed more on the same heavy nights, so both clear "
      "Pruszkow." % (H["HKTW"]["rate"], H["HLDZ"]["rate"], H["HWAW"]["rate"], under["hub_name"], under["rate"],
                     ex["mixed_mornings"], _n(ex["overflow_parcels"]), ex["overflow_missed_strykow"],
                     ex["overflow_missed_pruszkow"], ex["plan"]["HWAW"], ex["plan"]["HLDZ"], ex["shares"]["HLDZ"],
                     ex["left_out"]["HWAW"], ex["left_out"]["HLDZ"], ex["excess"]["HLDZ"], ex["excess"]["HWAW"]))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Missed-scan rate by hub: " + "; ".join("%s **%.2f** per cent" % (x["hub_name"], x["rate"]) for x in fig["hubs"]))
    w("2. Parcels handled and missed sort scans at the three hubs that fire: " + "; ".join(
        "%s **%s** and **%s**" % (H[h]["hub_name"], _n(H[h]["parcels"]), _n(H[h]["missed"])) for h in ("HKTW", "HLDZ", "HWAW")))
    w("3. The mornings with two trailers: **%d** depot mornings at Warszawa-Okecie and Warszawa-Targowek; **%s** "
      "parcels off Strykow's trailers, **%d** of them without a sort scan" % (ex["mixed_mornings"],
                                                                          _n(ex["overflow_parcels"]),
                                                                          ex["overflow_missed_strykow"]))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Took October's parcels from depot_scan_events_2026-10.csv, one per tracking number unloaded on the mornings of "
      "1 to 31 October (TDS-4 s.2.1; the rows re-sent on 21 October are the same rows again): %s parcels." % _n(fig["n_parcels"]))
    w("2. Took each parcel's hub from hub_sort_events_2026-10.parquet where it has a sort event (one hub per parcel; a "
      "second read on the sorter loop is the same sort); a parcel with none is a missed sort scan (s.2.2).")
    w("3. Split each depot door's arrival scans into unloadings wherever the door stood idle for more than ten minutes "
      "(any pause from one to 29 minutes gives the same %d unloadings), and found every unloading's sorted parcels "
      "carrying one hub." % ex["unloadings"])
    w("4. Charged each parcel without a sort scan to its unloading's hub, then counted each hub's parcels, missed sort "
      "scans and rate, and fired the alert above 1.00 per cent (s.2.3).")
    w("5. Courier events sent twice (TDS-4 s.3): a later-received record of the same parcel, event, courier and handheld "
      "carrying the first record's time cut to the minute, as local time from a TC52 and as UTC from a TC51 (two hours "
      "behind local until 25 October, one after); a second loop or the afternoon wave is a new scan; counted under the "
      "depot the event names.")
    w("6. Pre-advised parcels never picked up (TDS-4 s.4): each consignment's latest version with an October collection "
      "date, D-KRK1 read as D-KRK3 from 12 October, its pieces as parcels; a parcel the platform holds a pickup, sort, "
      "arrival or delivery record for was collected (trailer collections carry no pickup scan) and a failed pickup is "
      "not a collection; a piece label is the consignment number plus a three-digit piece number, and a marketplace "
      "order is matched on its first 20 characters, the orders sharing them counted against their pickups.")
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### %s" % GD.XLSX)
    w("")
    w("1. Each hub's parcels handled, missed sort scans, missed-scan rate and alert:")
    for x in fig["hubs"]:
        w("   - %s (%s): %s parcels, %s missed, %.2f per cent, %s" % (x["hub_name"], x["hub_code"], _n(x["parcels"]),
                                                                       _n(x["missed"]), x["rate"],
                                                                       "fires" if x["fires"] else "does not fire"))
    w("2. Each depot's courier events sent twice and pre-advised parcels never picked up:")
    for x in fig["depots"]:
        w("   - %s %s: %s sent twice, %s never picked up" % (x["depot_code"], x["depot_name"], _n(x["sent_twice"]),
                                                           _n(x["never_picked"])))
    w("")
    w("### %s" % GD.PPTX)
    w("")
    w("3. One slide: a horizontal bar chart of each hub's missed-scan rate against the 1.00 per cent tolerance line, "
      "the bars of %s marked as firing and the other three under the line, beside the six hubs' parcels, missed sort "
      "scans, rates and alerts." % fired)
    w("")
    return "\n".join(lines)


def write_figures(path, fig, ex):
    out = {"call": sorted(fig["fired"]), "tolerance": fig["tolerance"], "parcels": fig["n_parcels"],
           "hubs": [{k: x[k] for k in ("hub_code", "hub_name", "parcels", "missed", "rate", "fires")} for x in fig["hubs"]],
           "depots": fig["depots"], "routes": ex}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
