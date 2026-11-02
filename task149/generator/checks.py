"""The generator's assertions on the cut pack: the three-rules block (R1 to R3c), every semantic fork (SF ids), mess
neutrality per Layer 1 item, the input gates, the realism sweep and each graded figure's distance to its bin edge.

    python3 task149/generator/checks.py"""
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import ceiling as C  # noqa: E402
import io_util as IO  # noqa: E402
import params as P  # noqa: E402,F401

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))


def edge(x, step):
    """Distance from x to the nearest rounding edge at the given step."""
    q = x / step
    return abs((q - int(q)) - 0.5) * step


def same_bin(vals, step):
    return len({int(round(v / step)) for v in vals}) == 1


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    R = A.run(TARGET)
    V = R["variants"]
    D = A.load(TARGET)
    gold = R["golden"]
    tot_bin = lambda x: int(round(x / 100.0))  # noqa: E731

    # ---------------- the call and its ladder
    check("golden total recomputes to figures.json", int(round(gold / 100.0)) * 100 == F["total_boardings"],
          "%.1f" % gold)
    check("golden sits inside its bin (>= 30 from the edge at the nearest 100)", edge(gold, 100) >= 30,
          "%.1f, edge %.1f" % (gold, edge(gold, 100)))
    check("scope follows the threshold: reduced scheme", gold < R["threshold"] and F["scope"] == "reduced scheme",
          "%.1f against %d" % (gold, R["threshold"]))
    check("golden is at least 60 boardings below the threshold", R["threshold"] - gold >= 60,
          "%.1f below" % (R["threshold"] - gold))
    routes = {"census as daily journeys (default)": R["census_daily"], "line recovery factor": R["network_route"],
              "Lisnagry recovery factor": R["lisnagry_route"], "pooled panel weekday share": R["pooled_route"]}
    for name, v in routes.items():
        check("wrong route outside the golden bin: %s" % name, tot_bin(v) != tot_bin(gold) and v >= R["threshold"],
              "%.1f (bin %d, %s)" % (v, tot_bin(v) * 100, "full" if v >= R["threshold"] else "reduced"))
    cheap = [n for n, v in routes.items() if tot_bin(v) == tot_bin(gold) or v < R["threshold"]]
    check("Gate F on the clean truth: no cheap route reaches the call", not cheap, ", ".join(cheap) or "none")
    check("default path ends on about 2,400", int(round(R["census_daily"] / 100.0)) * 100 == 2400,
          "%.1f" % R["census_daily"])

    # ---------------- the three rules block
    check("R1 domain: the deciding quantity is trips per commuter per weekday, below one in every served zone",
          all(0.4 < R["freq"][z] < 0.9 for z in R["shares"] if R["shares"][z] > 0),
          ", ".join("%s %.3f" % (z, R["freq"][z]) for z in sorted(R["shares"]) if R["shares"][z] > 0))
    check("R1 domain: zones differ in their weekday share (spread of at least 0.2)",
          max(R["freq"][z] for z in R["shares"] if R["shares"][z] > 0)
          - min(R["freq"][z] for z in R["shares"] if R["shares"][z] > 0) >= 0.2, "")
    check("R2 two layers: every Layer 1 handling keeps the total in its bin",
          all(tot_bin(V[k]["total"]) == tot_bin(gold) for k in ("utcdays", "split", "with_midterm", "all_days_den")),
          ", ".join("%s %.1f" % (k, V[k]["total"]) for k in ("utcdays", "split", "with_midterm", "all_days_den")))
    prov = sum(R["census_prov"].get(z, 0) * s * R["freq"].get(z, 0) for z, s in R["shares"].items())
    check("R2 two layers: the provisional census release keeps the total in its bin", tot_bin(prov) == tot_bin(gold),
          "%.1f" % prov)
    check("R3a no decoy: no shipped text carries the golden total or the default figure",
          not any(s in IO.pdf_text(os.path.join(TARGET, f)) for f in os.listdir(TARGET) if f.endswith(".pdf")
                  for s in ("1,300", "1,312", "2,375", "2,400")), "")
    check("R3a no decoy: the refresh files the WHAT and no method sentence (no trip rate, frequency or factor)",
          not re.search(r"trip rate|per week|frequency|factor|days a week", R and IO.pdf_text(
              os.path.join(TARGET, "rathgarvan_fbc_demand_refresh_dec2027.pdf")), re.I), "")
    check("R3b not semantics: with every field read right, the census-daily route still files the full scheme",
          R["census_daily"] >= R["threshold"] and tot_bin(R["census_daily"]) != tot_bin(gold),
          "%.1f" % R["census_daily"])
    enumerated = [R["census_daily"], R["network_route"], R["lisnagry_route"], R["pooled_route"], gold]
    standing = [V[k]["total"] for k in ("long210", "long270", "long300", "majority", "minlong5", "split", "utcdays",
                                        "devmean")] + [gold]
    check("R3c not rule application: the enumerated family spreads over 900 boardings",
          max(enumerated) - min(enumerated) > 900, "%.0f to %.0f" % (min(enumerated), max(enumerated)))
    check("R3c not rule application: the standing family lands in one bin", same_bin(standing, 100),
          "%.1f to %.1f" % (min(standing), max(standing)))
    check("R3c back-test: the Lisnagry review's outturn is within 6 per cent of its census forecast",
          abs(float(re.search(r"([+-]\d+\.\d) per cent against the forecast", IO.pdf_text(
              os.path.join(TARGET, "lisnagry_opening_review_apr2020.pdf"))).group(1))) < 6.0, "")

    # ---------------- semantic forks (each SF id asserted)
    check("SF1 commute day: a workplace stay of 3.5 to 5 hours gives the same figures",
          all(same_bin([V[k]["rows"][z] for k in ("long210", "long270", "long300")] + [R["boardings"][z]], 10)
              for z in F["zone_boardings"]), "")
    check("SF2 usual workplace: modal zone, majority zone or five long stays give the same figures",
          all(same_bin([V[k]["rows"][z] for k in ("majority", "minlong5")] + [R["boardings"][z]], 10)
              for z in F["zone_boardings"]), "")
    check("SF3 a cell shared by two zones: majority zone or area-share split give the same figures",
          all(same_bin([V["split"]["rows"][z], R["boardings"][z]], 10) for z in F["zone_boardings"]), "")
    check("SF4 ratio of totals, mean of each device's share, or every device over all ordinary weekdays give the same "
          "figures", all(same_bin([V["devmean"]["rows"][z], V["all_days_den"]["rows"][z], R["boardings"][z]], 10)
                         for z in F["zone_boardings"]), "")
    spans = [len(obs) for _d, wz, _cd, obs in A.workers(D) if R["shares"].get(list(wz)[0], 0) > 0]
    check("SF4 by construction: no served-zone commuter's identifier is reissued inside the weeks (every span covers "
          "at least 50 of the ordinary weekdays)", min(spans) >= 50, "shortest span %d of %d" % (min(spans), R["ordinary_days"]))
    check("SF5 days by Irish date or by UTC date give the same figures",
          all(same_bin([V["utcdays"]["rows"][z], R["boardings"][z]], 10) for z in F["zone_boardings"]), "")
    check("SF6 ordinary weekdays: the mid-term week and the bank holiday are outside (filed), and including them "
          "keeps the total in its bin", tot_bin(V["with_midterm"]["total"]) == tot_bin(gold),
          "%.1f" % V["with_midterm"]["total"])
    check("SF7 census basis: the final release (filed); the provisional one keeps the total in its bin",
          tot_bin(prov) == tot_bin(gold), "")
    special = ("KX01", "KX02", "KX03")
    check("SF8 home workers, no fixed place and outside the county are outside the market (filed)",
          all(z not in R["shares"] for z in special) and all(z in D["census"] for z in special), "")
    check("SF9 a boarding is a journey to work begun at the station by a catchment resident (filed, one per commuting "
          "day)", "begin at Rathgarvan" in IO.pdf_text(os.path.join(TARGET, "rathgarvan_fbc_demand_refresh_dec2027.pdf"))
          or "begin at" in IO.pdf_text(os.path.join(TARGET, "rathgarvan_fbc_demand_refresh_dec2027.pdf")), "")
    check("SF10 the station share applies to each zone's journeys to work (filed in Table 2)",
          len(R["shares"]) == 11 and abs(R["shares"]["KW02"] - 0.47) < 1e-9, "")
    check("SF11 reissued device identifiers: each identifier over its own span; all 55 days as the denominator "
          "keeps the total in its bin", tot_bin(V["all_days_den"]["total"]) == tot_bin(gold),
          "%.1f" % V["all_days_den"]["total"])
    check("SF12 the census base is held at 2022 (filed); no completions or jobs growth enter",
          "held at the 2022 base" in IO.pdf_text(os.path.join(TARGET, "rathgarvan_fbc_demand_refresh_dec2027.pdf")), "")
    reg_codes = {r["station_code"] for r in D["register"]}
    asset_ids = {r["asset_id"] for r in D["assets"]}
    codes = {g for _d, g, _n in D["gates"]}
    check("SF13 ask A: a station counts with the code it replaced (UHK with KUH, CBH with CBY), from the register",
          {"UHK", "KUH", "CBH", "CBY"} <= reg_codes and R["station_ratios"]["KUH"] and R["station_ratios"]["CBY"], "")
    check("SF14 ask A: every location code in the gate file is a register station or a gate asset, and an asset belongs "
          "to the station its dated row places it at on the day", codes <= reg_codes | asset_ids, "")
    moved = [a for a in asset_ids if len({r["station_code"] for r in D["assets"] if r["asset_id"] == a}) > 1]
    check("SF14 ask A: each of the four gate assets moved between stations, so a static join misplaces one period",
          len(moved) == 4 and len(asset_ids) == 4, ", ".join(sorted(moved)))
    check("SF15 ask B: arrival in the zone is the day's first stay in a cell of the workplace zone, Irish time, ordinary "
          "weekdays, from 07:30 up to and including 09:30 (prompt's words)",
          all(int(round(100 * R["arrivals"][z])) == v for z, v in F["arrival_share"].items()), "")
    check("SF15 ask B: no stay away from home starts at 07:30 or 09:30, so an inclusive or exclusive window gives the "
          "same figures", all(abs(R["arrivals"][z] - R["arrivals_exclusive"][z]) < 1e-12 for z in F["arrival_share"]),
          "")
    check("SF17 ask A: the line is its total entries, all stations summed by day (prompt's words); the mean of the "
          "station ratios is another quantity", int(round(100 * R["station_ratios"]["LINE"])) == F["station_ratio"]["LINE"]
          and int(round(100 * R["line_mean_of_stations"])) != F["station_ratio"]["LINE"],
          "%.2f against %.2f" % (100 * R["station_ratios"]["LINE"], 100 * R["line_mean_of_stations"]))
    check("SF16 zone boardings to the nearest 10 and the total to the nearest 100 from the same exact figures",
          abs(sum(R["boardings"].values()) - gold) < 1e-6, "")

    # ---------------- bin edges for every graded figure
    for z, v in F["zone_boardings"].items():
        vals = [R["boardings"][z]] + [V[k]["rows"][z] for k in V if k != "with_midterm"]
        check("bin: zone %s boardings %d under every estimator and reading (edge >= 1.5)" % (z, v),
              same_bin(vals, 10) and min(edge(x, 10) for x in vals) >= 1.5 and int(round(R["boardings"][z] / 10)) * 10 == v,
              "%.2f to %.2f, nearest edge %.2f" % (min(vals), max(vals), min(edge(x, 10) for x in vals)))
    for z, v in F["arrival_share"].items():
        x = 100 * R["arrivals"][z]
        check("bin: arrival share %s %d%% (edge >= 0.15)" % (z, v), edge(x, 1) >= 0.15, "%.2f" % x)
    for s, v in F["station_ratio"].items():
        x = 100 * R["station_ratios"][s]
        check("bin: station %s %d%% (edge >= 0.2)" % (s, v), edge(x, 1) >= 0.2, "%.2f" % x)

    # ---------------- ask devices
    for mode in ("register", "last", "first"):
        rr = R["station_ratios_%s" % mode]
        check("ask A device: a static reading of the gate assets (%s) misses every station figure" % mode,
              all(rr[s] is None or int(round(100 * rr[s])) != F["station_ratio"][s]
                  for s in ("ARD", "LSG", "KCN", "KDK", "KUH", "CBY")),
              ", ".join("%s %s" % (s, "n/a" if rr[s] is None else int(round(100 * rr[s]))) for s in F["station_ratio"]))
    utc = R["arrivals_utc"]
    check("ask B device: UTC stamps read as Irish time move every arrival figure",
          all(int(round(100 * utc[z])) != v for z, v in F["arrival_share"].items()), "")
    lg = R["arrivals_long"]
    check("ask B device: timing the journey by the long workplace stay moves every arrival figure",
          all(int(round(100 * lg[z])) != v for z, v in F["arrival_share"].items()),
          ", ".join("%s %d" % (z, int(round(100 * lg[z]))) for z in sorted(F["arrival_share"])))
    pc, ml, crack, n, full = C.main(TARGET)
    check("ceiling: pair at or under 60 and mirror leakage under 50", pc <= 60 and ml < 50, "%.1f, %.1f" % (pc, ml))
    check("ceiling: the full includer reproduces every ask figure", full == n, "%d of %d" % (full, n))

    # ---------------- input gates
    files = sorted(os.listdir(TARGET))
    exts = {f.rsplit(".", 1)[1] for f in files}
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    check("input gate: ten or more files", len(files) >= 10, str(len(files)))
    check("input gate: three or more formats", len(exts) >= 3, ",".join(sorted(exts)))
    check("input gate: a file of 25,000 rows or more", meta["largest_file"]["rows"] >= 25000,
          str(meta["largest_file"]["rows"]))
    check("input gate: two or more distractors named in metadata.json, none in a file name as such",
          len(meta["distractor_files"]) >= 2 and not any("distract" in f for f in files), "")
    check("input gate: every file carries source, date and licence",
          all(set(v) >= {"source", "date", "license"} for v in meta["files"].values()) and set(meta["files"]) == set(files),
          "")

    # ---------------- realism sweep
    bad_words = re.compile(r"test_|trap|decoy|golden|stump|synthetic|fake|dummy", re.I)
    check("realism: no file name carries the author's words", not any(bad_words.search(f) for f in files), "")
    text = ""
    for f in files:
        p = os.path.join(TARGET, f)
        if f.endswith(".pdf"):
            text += IO.pdf_text(p)
        elif f.endswith((".docx", ".xlsx")):
            z = zipfile.ZipFile(p)
            text += " ".join(z.read(n).decode("utf-8", "ignore") for n in z.namelist() if n.endswith(".xml"))
    check("realism: no em or en dash in shipped documents", "—" not in text and "–" not in text, "")
    check("realism: no author's words in shipped documents", not re.search(r"\b(decoy|trap|stump|golden)\b", text, re.I),
          "")
    gates_last = max(d for d, _c, _n in D["gates"])
    cal_last = max(r["date"] for r in D["cal"])
    check("realism: no data dated after the as-of date", str(gates_last) <= P.AS_OF and cal_last <= P.AS_OF,
          "%s, %s" % (gates_last, cal_last))
    people = {"Colum Curtis", "Deaglan Gilmore", "Eve Dunne"}
    names = set(re.findall(r"(?:Prepared by|Author:|Contact:) ([A-Z][a-z]+ [A-Z][a-zA-Z]+)", text))
    check("realism: the only personas are the card's drawn people", names <= people, ", ".join(sorted(names)))
    labels = set()
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(TARGET, "census2022_pow_rathgarvan_catchment.xlsx"), read_only=True)
    for row in wb["Final release"].iter_rows(values_only=True):
        labels |= {str(c) for c in row if c is not None}
    reg_names = {r["station_name"] for r in D["register"]}
    import golden as GD
    check("realism: every zone label the golden prints appears in a shipped file",
          all(GD.ZONE_NAMES[z] in labels for z in F["zone_boardings"]), "")
    check("realism: every station label the golden prints appears in the register or is the line",
          all(GD.STATION_NAMES[s] in reg_names or s == "LINE" for s in F["station_ratio"]), "")
    check("realism: the golden files exist", all(os.path.exists(os.path.join(GOLDEN, f)) for f in (GD.BOOK, GD.MEMO)),
          "")

    # ---------------- the write-up states nothing the honest family splits on
    sub = open(os.path.join(TASK, "submission.md")).read() if os.path.exists(os.path.join(TASK, "submission.md")) else ""
    lo, hi = F["zone_weekday_share_range_pct"]
    check("write-up: the zones' weekday shares are stated as the span over every licensed filter (%d to %d per cent)"
          % (lo, hi), ("span %d to %d per cent" % (lo, hi)) in sub, "")
    check("write-up: no unrounded total and no one-decimal zone share in the write-up",
          "%.1f" % gold not in sub and not re.search(r"KW\d\d \d+\.\d per cent", sub), "")
    check("write-up: the total and the gap are stated at the nearest 100 only",
          "**1,300** (to the nearest 100), about 100 below" in sub and F["gap_to_threshold_rounded"] == 100, "")

    fails = [r for r in RESULTS if not r[1]]
    for name, ok, detail in RESULTS:
        print("%-4s %s%s" % ("PASS" if ok else "FAIL", name, ("  [" + detail + "]") if detail else ""))
    print("%d checks, %d failed" % (len(RESULTS), len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
