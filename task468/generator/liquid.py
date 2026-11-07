"""task468 architecture 6: the treatment plant's tankered liquid waste receival (ask A's world and files).

Licensed transporters deliver grease trap waste, septage, portable toilet waste and landfill leachate to the receival
station at the Glenbrae treatment plant. The station logs every discharge into its pit under a docket; the
transporter's state waste tracking manifest names the waste and the receival docket. When the pit's high-level alarm
stops a discharge, the driver finishes the load in a second pass a few minutes later under a second docket, and the
manifest carries only the first."""
import datetime as dt

import numpy as np

import wio

SEED = 46871
TYPES = [("GT", "Grease trap waste", 6.0, 12.5, 9.0), ("SE", "Septage", 4.0, 9.0, 4.0),
         ("PL", "Portable toilet waste", 1.8, 4.6, 2.5), ("LL", "Landfill leachate", 14.0, 24.0, 1.6)]
TRANSPORTERS = [("BWS", "Brennan Waste Services", ["GT", "SE"]), ("CLT", "Coastline Liquid Transport", ["GT", "PL"]),
                ("DDV", "Darling Downs Vacuum", ["SE", "GT"]), ("KPS", "Kookaburra Pump Services", ["PL", "SE"]),
                ("MRL", "Murray Road Liquid Haulage", ["LL"]), ("TWT", "Trident Waste Tankers", ["GT", "SE", "PL"])]
LOG = "glw_liquid_waste_receival_2026.csv"
MANIFESTS = "qld_waste_tracking_manifests_glw_2026.xlsx"


def world(seed=SEED):
    rng = np.random.RandomState(seed)
    rego = {}
    for t, _, _ in TRANSPORTERS:
        rego[t] = ["%03d%s%s" % (rng.randint(100, 999), t[0], "".join(rng.choice(list("ABCDEFGHJKLMNPRSTUVWXYZ"), 2)))
                   for _ in range(3 + (t in ("BWS", "TWT")))]
    loads = []
    d = dt.date(2025, 12, 31)
    docket = 88412
    manifest = 4410731
    while d <= dt.date(2027, 1, 1):
        wd = d.weekday()
        for code, desc, lo, hi, rate in TYPES:
            n = rng.poisson(rate * (1.0 if wd < 5 else (0.35 if wd == 5 else 0.1)))
            for _ in range(n):
                tr = [t for t in TRANSPORTERS if code in t[2]]
                t = tr[rng.randint(len(tr))][0]
                when = dt.datetime.combine(d, dt.time(int(rng.randint(6, 17)), int(rng.randint(0, 60))))
                vol = float(rng.uniform(lo, hi))
                loads.append({"code": code, "trans": t, "rego": rego[t][rng.randint(len(rego[t]))], "when": when,
                              "vol": vol, "split": rng.rand() < (0.11 if code in ("GT", "LL") else 0.07),
                              "rejected": rng.rand() < 0.012,
                              "collected": d - dt.timedelta(days=int(rng.rand() < 0.3))})
        d += dt.timedelta(days=1)
    loads.sort(key=lambda x: (x["when"], x["trans"], x["code"]))
    # a truck delivers at most once in three hours: each load takes a truck of its transporter that is free
    free = {}
    for x in loads:
        fleet = rego[x["trans"]]
        pick = None
        for r in fleet:
            if free.get(r, dt.datetime.min) <= x["when"]:
                pick = r
                break
        if pick is None:
            pick = "%03d%s%s" % (rng.randint(100, 999), x["trans"][0],
                                 "".join(rng.choice(list("ABCDEFGHJKLMNPRSTUVWXYZ"), 2)))
            fleet.append(pick)
        x["rego"] = pick
        free[pick] = x["when"] + dt.timedelta(hours=3)
    # each type and quarter's received volume sits clear of a half kilolitre: one plain load carries the remainder
    for code, *_ in TYPES:
        for q in range(4):
            cell = [x for x in loads if x["code"] == code and x["when"].year == 2026 and
                    (x["when"].month - 1) // 3 == q and not x["rejected"]]
            frac = sum(round(x["vol"], 2) for x in cell) % 1
            plain = [x for x in cell if not x["split"]]
            plain[len(plain) // 2]["vol"] += (1.0 - frac) if frac >= 0.5 else -frac
    rows = []
    for ld in loads:
        manifest += int(rng.randint(1, 40))
        ld["manifest"] = "QW%d" % manifest
        docket += int(rng.randint(1, 3))
        ld["docket"] = "RD%06d" % docket
        if ld["rejected"]:
            rows.append((ld["when"], ld["docket"], ld["rego"], ld["trans"], 0.0, "Rejected - pH"))
            continue
        if ld["split"]:
            first = round(ld["vol"] * float(rng.uniform(0.45, 0.8)), 2)
            second = round(ld["vol"] - first, 2)
            rows.append((ld["when"], ld["docket"], ld["rego"], ld["trans"], first, "Accepted"))
            docket += 1
            ld["docket2"] = "RD%06d" % docket
            rows.append((ld["when"] + dt.timedelta(minutes=int(rng.randint(9, 41))), ld["docket2"], ld["rego"],
                         ld["trans"], second, "Accepted"))
        else:
            rows.append((ld["when"], ld["docket"], ld["rego"], ld["trans"], round(ld["vol"], 2), "Accepted"))
        ld["declared"] = round(ld["vol"] * float(np.exp(rng.normal(0, 0.035))), 1)
    return {"loads": loads, "log": sorted(rows, key=lambda r: (r[0], r[1]))}


def truth(L):
    """Received volume by waste type and quarter of the receival date in 2026 (local), accepted loads only."""
    out = {code: [0.0] * 4 for code, *_ in TYPES}
    for when, dk, rego, tr, vol, status in L["log"]:
        if status != "Accepted" or when.year != 2026:
            continue
        ld = [x for x in L["loads"] if x["docket"] == dk or x.get("docket2") == dk][0]
        out[ld["code"]][(when.month - 1) // 3] += vol
    return out


def write(L, log_path, man_path):
    wio.csv_file(log_path, ["docket", "received", "truck_rego", "transporter", "volume_kl", "status"],
                 [[dk, w.strftime("%d/%m/%Y %H:%M"), rg, tr, "%.2f" % v, st] for w, dk, rg, tr, v, st in L["log"]])
    rows = [["Manifest", "Transporter", "Waste code", "Waste description", "Collected", "Delivered",
             "Declared volume (kL)", "Receival docket"]]
    names = {t: n for t, n, _ in TRANSPORTERS}
    desc = {c: dsc for c, dsc, *_ in TYPES}
    for ld in L["loads"]:
        if ld["rejected"]:
            continue
        rows.append([ld["manifest"], names[ld["trans"]], ld["code"], desc[ld["code"]], ld["collected"].isoformat(),
                     ld["when"].date().isoformat(), ld["declared"], ld["docket"]])
    wio.xlsx(man_path, [("Manifests", rows, [1], {})], "Waste Tracking Export", dt.datetime(2027, 1, 7, 2, 10),
             dt.datetime(2027, 1, 7, 2, 10), widths=[12, 28, 10, 22, 12, 12, 14, 14],
             company="Department of Environment")
