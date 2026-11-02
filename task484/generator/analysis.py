"""Every rung, the golden and the asks, computed from target/ alone."""
import csv
import datetime as dt
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import est           # noqa: E402

DAYS = est.DAYS
DIDX = {d: i for i, d in enumerate(DAYS)}
ABBR = {"ave": "avenue", "rd": "road", "st": "street", "la": "lane", "wy": "way", "hl": "hill"}
BANK_HOLIDAYS = {dt.date(2025, 1, 1), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5),
                 dt.date(2025, 5, 26), dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26)}


def norm(road):
    w = re.sub(r"[^a-z ]", " ", str(road).lower()).split()
    if w and w[-1] in ABBR:
        w[-1] = ABBR[w[-1]]
    return " ".join(w)


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def xlsx_rows(path, sheet):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet]
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    wb.close()
    return rows


def load(tgt):
    P = {}
    # count points and manual counts
    reg = xlsx_rows(os.path.join(tgt, "count_points_2025.xlsx"), "Count points")
    hdr = reg[0]
    P["points"] = {r[0]: dict(zip(hdr, r)) for r in reg[1:] if r[0] is not None}
    mc = read_csv(os.path.join(tgt, "manual_counts_2025.csv"))
    h = mc[0]
    counts = {}
    for r in mc[1:]:
        d = dict(zip(h, r))
        cp = int(d["count_point_id"])
        day = dt.date.fromisoformat(d["count_date"])
        c = counts.setdefault(cp, {"date": day, "c12": 0, "hgv": 0, "rows": 0})
        assert c["date"] == day
        c["c12"] += int(d["all_motor_vehicles"])
        c["hgv"] += int(d["all_hgvs"])
        c["rows"] += 1
    P["counts"] = counts
    # permanent counters
    sites = read_csv(os.path.join(tgt, "atc_sites_2025.csv"))
    sh = sites[0]
    P["sites"] = {r[0]: dict(zip(sh, r)) for r in sites[1:]}
    atc = read_csv(os.path.join(tgt, "atc_daily_2025.csv"))
    ah = atc[0]
    A = {}
    for r in atc[1:]:
        d = dict(zip(ah, r))
        s = A.setdefault(d["site_id"], {"q24": np.full(365, np.nan), "q12": np.full(365, np.nan),
                                        "cls": np.full((365, 8), np.nan)})
        i = DIDX[dt.date.fromisoformat(d["date"])]
        s["q24"][i] = float(d["mv_0000_2400"])
        s["q12"][i] = float(d["mv_0700_1900"])
        s["cls"][i] = [float(d["class_%d" % k]) for k in range(1, 9)]
    P["atc"] = A
    # UTC register and detector daily summaries (two half-year parts, the header repeated between them)
    jun = xlsx_rows(os.path.join(tgt, "utc_asset_register_2025.xlsx"), "Junctions")
    jh = jun[0]
    P["junctions"] = {r[0]: dict(zip(jh, r)) for r in jun[1:] if r[0]}
    det = xlsx_rows(os.path.join(tgt, "utc_asset_register_2025.xlsx"), "Detectors")
    dh = det[0]
    P["detectors"] = {r[0]: dict(zip(dh, r)) for r in det[1:] if r[0]}
    dd = read_csv(os.path.join(tgt, "utc_detector_daily_2025.csv"))
    D = {}
    for r in dd[1:]:
        if r[0] == "detector":
            continue
        did = r[0]
        x = D.setdefault(did, {"d24": np.full(365, np.nan), "d12": np.full(365, np.nan), "av": np.zeros(365)})
        day = dt.datetime.strptime(r[1], "%d/%m/%Y").date()
        i = DIDX[day]
        x["av"][i] = float(r[4])
        if r[2] != "":
            x["d12"][i] = float(r[2])
            x["d24"][i] = float(r[3])
    P["utc"] = D
    return P


def link_section(P, cp):
    """The section's own approach detectors: the junction named by the section's road and one of its end
    roads, and on it the arm whose approach is the section's road."""
    p = P["points"][cp]
    road = norm(p["road_name"])
    ends = {norm(p["start_junction_road_name"]), norm(p["end_junction_road_name"])}
    hits = []
    for ref, j in P["junctions"].items():
        roads = {norm(x) for x in str(j["junction"]).split("/")}
        if road in roads and roads & ends:
            hits.append(ref)
    if not hits:
        return None, []
    assert len(hits) == 1, (cp, hits)
    ref = hits[0]
    dets = sorted(d for d, x in P["detectors"].items() if x["junction_ref"] == ref and norm(x["approach"]) == road)
    return ref, dets


def group(P, setting=None):
    out = []
    for sid, s in sorted(P["sites"].items()):
        if setting is None or s["setting"] == setting:
            out.append((P["atc"][sid]["q24"], P["atc"][sid]["q12"]))
    return out


def own_arrays(P, dets):
    d24 = np.nansum([P["utc"][d]["d24"] for d in dets], axis=0)
    d12 = np.nansum([P["utc"][d]["d12"] for d in dets], axis=0)
    av = np.min([P["utc"][d]["av"] for d in dets], axis=0)
    d24 = np.where(av > 0, d24, np.nan)
    d12 = np.where(av > 0, d12, np.nan)
    return d24, d12, av


def sections(P):
    """Per counted section: count, link, every rung's AADF."""
    out = []
    for cp, c in sorted(P["counts"].items()):
        p = P["points"][cp]
        di = DIDX[c["date"]]
        c12 = c["c12"]
        grp = group(P, p["setting"])
        r = {"cp": cp, "road": p["road_name"], "from": p["start_junction_road_name"], "to": p["end_junction_road_name"],
             "length": float(p["link_length_km"]), "date": c["date"], "c12": c12, "setting": p["setting"]}
        r["tmg"] = {k: (f(c12, di, grp) if "same-day" in k else f(c12, di, grp, BANK_HOLIDAYS)) for k, f in est.TMG.items()}
        r["tmg"]["T5 same-day, every counter pooled"] = est.tmg_sameday_ratio_of_sums(c12, di, group(P))
        ref, dets = link_section(P, cp)
        r["junction"], r["dets"] = ref, dets
        r["own"] = {}
        if dets:
            d24, d12, av = own_arrays(P, dets)
            for k, f in est.OWN.items():
                r["own"][k] = f(c12, di, d24, d12, av) if "month" not in k else f(c12, di, d24, d12, av, BANK_HOLIDAYS)
            if len(dets) == 2:
                for dd in dets:
                    x = P["utc"][dd]
                    r["own"]["G1 lane %s alone" % P["detectors"][dd]["lane"]] = est.own_exact_day(c12, di, x["d24"], x["d12"], x["av"])
            # rungs that read the detectors wrongly
            r["raw_detector"] = float(np.nanmean(d24[av >= 100]))
            r["own_group_2412"] = est.own_group_2412(c12, di, d24, d12, av, grp)
        r["gold_aadf"] = r["own"]["G1 counted day, full days"] if dets else r["tmg"]["T1 same-day, ratio of sums"]
        r["default_aadf"] = r["tmg"]["T1 same-day, ratio of sums"]
        out.append(r)
    return out


def nearest_junction_rung(P, secs):
    """Rung: the junction nearest the count point by coordinates, its whole detected flow as the section's record."""
    out = {}
    jl = {ref: (float(j["latitude"]), float(j["longitude"])) for ref, j in P["junctions"].items()}
    for r in secs:
        p = P["points"][r["cp"]]
        lat, lon = C.bng_to_wgs84(float(p["easting"]), float(p["northing"]))
        best = min(jl, key=lambda k: (jl[k][0] - lat) ** 2 + ((jl[k][1] - lon) * math.cos(math.radians(lat))) ** 2)
        dets = [d for d, x in P["detectors"].items() if x["junction_ref"] == best and d in P["utc"]]
        d24, d12, av = own_arrays(P, dets)
        ok = av >= 100
        di = DIDX[r["date"]]
        if np.isnan(d12[di]):
            out[r["cp"]] = r["default_aadf"]
            continue
        out[r["cp"]] = r["c12"] * float(np.nanmean(d24[ok])) / float(d12[di])
    return out


def pooled_utc_rung(P, secs):
    """Rung: one factor pooled over every detector in the system, as if the detectors were another counter group."""
    out = {}
    for r in secs:
        di = DIDX[r["date"]]
        num = den = 0.0
        for d, x in P["utc"].items():
            if x["av"][di] >= 100 and not np.isnan(x["d12"][di]):
                num += float(np.nanmean(x["d24"][x["av"] >= 100]))
                den += float(x["d12"][di])
        out[r["cp"]] = r["c12"] * num / den
    return out


def annual(aadf):
    return est.bin01(aadf)


def call(secs, key):
    over = sorted(r["road"] for r in secs if annual(key(r)) > 3.0)
    return over


# ----------------------------------------------------------------- ask A: counters' heavy goods vehicles per day
def switch_date(P):
    """The day the counters' channel 5 stops carrying two-axle rigid goods vehicles and starts carrying buses:
    on weekdays channel 5 runs at about twice channel 8 under the legacy classes and below it under the native
    ones; the first weekday from which every later weekday reads native, pooled over the counters."""
    r = []
    for sid in sorted(P["atc"]):
        a = P["atc"][sid]
        r.append(a["cls"][:, 4] / a["cls"][:, 7])
    r = np.nanmedian(np.array(r), axis=0)
    wk = [i for i, d in enumerate(DAYS) if d.weekday() < 5]
    native = {i: r[i] < 1.0 for i in wk}
    for k, i in enumerate(wk):
        if all(native[j] for j in wk[k:]) and not native[wk[k - 1]]:
            return DAYS[i]
    raise RuntimeError("no switch found")


def hgv_per_day(P, how, sw=None):
    out = {}
    for sid in sorted(P["atc"]):
        a = P["atc"][sid]
        ard = a["cls"][:, 4] + a["cls"][:, 5] + a["cls"][:, 6]
        tx = a["cls"][:, 5] + a["cls"][:, 6] + a["cls"][:, 7]
        if how == "switch":
            cut = DIDX[sw]
            v = np.concatenate([ard[:cut], tx[cut:]])
        elif how == "install":
            cut = DIDX[dt.date.fromisoformat(P["sites"][sid]["installed"])]
            v = np.concatenate([ard[:cut], tx[cut:]])
        elif how == "current":
            v = tx
        elif how == "legacy":
            v = ard
        out[sid] = float(np.nanmean(v))
    return out


# ----------------------------------------------------------------- ask B: approaches at the two renewed junctions
ASK_B = ("Western Avenue / Fenwick Road", "Ring Road / Tanyard Lane")


def junction_ref(P, name):
    want = {norm(x) for x in name.split("/")}
    for ref, j in P["junctions"].items():
        if {norm(x) for x in str(j["junction"]).split("/")} == want:
            return ref
    raise KeyError(name)


def renewal_day(P, ref):
    """The first day after the junction went dark: from the detector days themselves."""
    dets = [d for d, x in P["detectors"].items() if x["junction_ref"] == ref]
    av = np.min([P["utc"][d]["av"] for d in dets], axis=0)
    dark = np.where(av == 0)[0]
    return DAYS[int(dark[1])], [DAYS[int(i)] for i in dark]


def remap(P, ref, sw):
    """Which current channel each channel was before the renewal. The register gives the current channels'
    approaches; before the renewal the same numbers carried other lanes. Lanes of one approach carry one stream, so
    their day-to-day departures from their own weekday rhythm move together: the pre-renewal channels are grouped
    into approaches of the register's sizes by that co-movement, and each group is matched to the current approach
    with the closest level, weekend shares and 07:00-19:00 share across the dark days. Within a two-lane approach
    the lanes are matched by level."""
    import itertools
    dets = sorted(d for d, x in P["detectors"].items() if x["junction_ref"] == ref)
    i = DIDX[sw]
    pre = [k for k in range(i - 63, i - 1) if all(P["utc"][d]["av"][k] > 0 for d in dets)]
    post = [k for k in range(i + 2, i + 65) if all(P["utc"][d]["av"][k] > 0 for d in dets)]

    def resid(d, idx):
        v = np.log(P["utc"][d]["d24"][idx])
        wk = np.array([DAYS[k].weekday() for k in idx])
        out = v.copy()
        for w in range(7):
            out[wk == w] -= v[wk == w].mean()
        return out

    def sig(v24, v12, idx):
        wk = np.array([DAYS[k].weekday() for k in idx])
        lvl = np.mean(v24[wk < 5])
        return np.array([math.log(lvl), np.mean(v24[wk == 5]) / lvl, np.mean(v24[wk == 6]) / lvl,
                         np.sum(v12[wk < 5]) / np.sum(v24[wk < 5])])

    arms = {}
    for d in dets:
        x = P["detectors"][d]
        arms.setdefault((norm(x["approach"]), x["heading"]), []).append(d)
    sizes = sorted(len(v) for v in arms.values())
    R = {d: resid(d, pre) for d in dets}
    corr = {(a, b): float(np.corrcoef(R[a], R[b])[0, 1]) for a in dets for b in dets if a < b}
    best = None
    for perm in itertools.permutations(dets):
        groups, k = [], 0
        for n in sorted(len(v) for v in arms.values()):
            groups.append(tuple(sorted(perm[k:k + n])))
            k += n
        key = tuple(sorted(groups))
        score = sum(corr[(g[0], g[1])] for g in groups if len(g) == 2)
        if best is None or score > best[0]:
            best = (score, key)
    pre_groups = list(best[1])
    S_pre = {g: sig(sum(P["utc"][d]["d24"][pre] for d in g), sum(P["utc"][d]["d12"][pre] for d in g), pre) for g in pre_groups}
    S_post = {a: sig(sum(P["utc"][d]["d24"][post] for d in ds), sum(P["utc"][d]["d12"][post] for d in ds), post) for a, ds in arms.items()}
    wts = np.array([1.0, 4.0, 4.0, 8.0])
    bestm = None
    for perm in itertools.permutations(list(arms)):
        if any(len(g) != len(arms[a]) for g, a in zip(pre_groups, perm)):
            continue
        cost = sum(float(np.sum(((S_pre[g] - S_post[a]) * wts) ** 2)) for g, a in zip(pre_groups, perm))
        if bestm is None or cost < bestm[0]:
            bestm = (cost, perm)
    mp = {}
    for g, a in zip(pre_groups, bestm[1]):
        cur = sorted(arms[a], key=lambda d: -np.mean(P["utc"][d]["d24"][post]))
        old = sorted(g, key=lambda d: -np.mean(P["utc"][d]["d24"][pre]))
        for o, c in zip(old, cur):
            mp[o] = c
    return mp            # pre-renewal id -> the current id carrying the same lane


def approach_flows(P, how):
    out = {}
    for name in ASK_B:
        ref = junction_ref(P, name)
        sw, dark = renewal_day(P, ref)
        mp = remap(P, ref, sw) if how == "remap" else None
        dets = sorted(d for d, x in P["detectors"].items() if x["junction_ref"] == ref)
        arms = {}
        for d in dets:
            x = P["detectors"][d]
            arms.setdefault((norm(x["approach"]).title(), x["heading"]), []).append(d)
        for (road, head), ds in sorted(arms.items()):
            series = np.zeros(365)
            for d in ds:
                if how == "remap":
                    inv = {v: k for k, v in mp.items()}
                    pre_id = inv[d]
                    v = np.concatenate([P["utc"][pre_id]["d24"][:DIDX[sw]], P["utc"][d]["d24"][DIDX[sw]:]])
                else:
                    v = P["utc"][d]["d24"].copy()
                series = series + v
            if how == "post":
                series[:DIDX[sw]] = np.nan
            out[(name, "%s %s" % (road, head))] = float(np.nansum(series))
    return out


def compute(tgt):
    P = load(tgt)
    secs = sections(P)
    R = {"P": P, "secs": secs}
    R["near"] = nearest_junction_rung(P, secs)
    R["pooled"] = pooled_utc_rung(P, secs)
    R["sw"] = switch_date(P)
    R["askA"] = {k: hgv_per_day(P, k, R["sw"]) for k in ("switch", "install", "current", "legacy")}
    R["askB"] = {k: approach_flows(P, k) for k in ("remap", "register", "post")}
    return R


if __name__ == "__main__":
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(C.TASK, "target")
    R = compute(tgt)
    for r in R["secs"]:
        print("%-17s %s c12 %5d gold %6.0f %.2fM default %.2fM near %.2fM pooled %.2fM raw %s g2412 %s %s" % (
            r["road"], r["date"], r["c12"], r["gold_aadf"], annual(r["gold_aadf"]), annual(r["default_aadf"]),
            annual(R["near"][r["cp"]]), annual(R["pooled"][r["cp"]]),
            "%.2fM" % annual(r["raw_detector"]) if r["dets"] else "-", "%.2fM" % annual(r["own_group_2412"]) if r["dets"] else "-",
            r["junction"] or ""))
    print("golden", call(R["secs"], lambda r: r["gold_aadf"]))
    print("default", call(R["secs"], lambda r: r["default_aadf"]))
    print("switch", R["sw"])
    for k, v in R["askA"].items():
        print("A", k, {s: round(x) for s, x in v.items()})
    for k, v in R["askB"].items():
        print("B", k, {s[1]: round(x) for s, x in v.items()})
