"""task231 architecture 2: the generator's assertions, on the built pack and the world it was cut from.

    python3 task231/generator/checks.py

Labels: R1 to R3 the client's three rules on the clean truth; G the golden against the truth and its family;
L the ladder; SF the semantic fork table's rows; A and B the asks and their devices; I the input gates and the
realism sweep."""
import csv
import datetime as dt
import glob
import json
import os
import re
import sys
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import params as P  # noqa: E402
import world as WD  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
RES = []


def check(label, ok, detail=""):
    RES.append((label, bool(ok), detail))
    print("%-6s %-4s %s" % (label, "ok" if ok else "FAIL", detail))


def sites_of(reg, idx):
    return sorted(reg["sites"][k]["site"] for k in idx)


W = WD.build()
S = A.solve(TARGET)
S["target"] = TARGET
M, reg = S["M"], S["reg"]
codes = [s["site"] for s in reg["sites"]]
tag = {P.SITE[t]: t for t in P.TAGS}
wi = [P.TAGS.index(tag[c]) for c in codes]          # analysis order -> world order
NS, NH = len(codes), P.NH
gold = set(M["retune"])
GOLD_TAGS = {"K1", "K2", "K3", "K4", "M1", "M2", "M3", "P3"}

# ---------------- G: the golden against the world's truth ----------------
truth_fr = (W["spatial"] & W["right"]).sum(1)[wi]
check("G1", (M["fr"] == truth_fr).all(), "golden false-rejection hours equal the truth at every station")
check("G2", (M["withheld"] == W["spatial"].sum(1)[wi]).all(), "the QC log's spatial rows are the test's hours")
check("G3", {tag[c] for c in sites_of(reg, gold)} == GOLD_TAGS, "re-tune set %s" % sites_of(reg, gold))
acc = np.abs(W["read"] - W["T"]) <= P.SENSOR_ACCURACY_C + 1e-9
check("G4", (acc == W["right"]).all(), "right means within 0.3 C of the station's air, every reading")
for tau in (1.5, 2.5, 3.0, 3.5, 4.0, 4.5):
    rr, _ = A.judge(M["val"], M["wh"], reg, M["G"], tau=tau)
    check("G5", ((M["wh"] & rr).sum(1) == M["fr"]).all(), "tolerance %.1f C gives the same hours" % tau)
var = {}
for nm, kw in (("corr 0.7", {"cth": 0.7}), ("corr 0.9", {"cth": 0.9}), ("15 km", {"dk": 15.0}),
               ("120 m", {"dz": 120.0}), ("sig -0.3", {"sig": -0.3}), ("sig -1.0", {"sig": -1.0})):
    G2, _, _ = A.sharing(M["val"], M["wh"], M["anyflag"], reg, M["night"], res=M["res"], **kw)
    rr, _ = A.judge(M["val"], M["wh"], reg, G2)
    var[nm] = (M["wh"] & rr).sum(1)
    mv = {codes[k]: int(var[nm][k] - M["fr"][k]) for k in range(NS) if var[nm][k] != M["fr"][k]}
    check("G6", set(A.retune(var[nm] / NH * 100)) == gold, "grouping %s: same set%s" % (
        nm, ", hours move at %s" % mv if mv else ", same hours"))
for nm, kw in (("radius 40 km", {"rad": 40.0}), ("radius 60 km", {"rad": 60.0}), ("any pool mate", {"floor_rule": "any"})):
    rr, _ = A.judge(M["val"], M["wh"], reg, M["G"], **kw)
    var[nm] = (M["wh"] & rr).sum(1)
    check("G7", (var[nm] == M["fr"]).all(), "%s gives the same hours" % nm)
rr, _ = A.judge(M["val"], M["wh"], reg, M["G"], lapse=M["slope"])
fl = (M["wh"] & rr).sum(1)
moved = {codes[k]: int(fl[k] - M["fr"][k]) for k in range(NS) if fl[k] != M["fr"][k]}
check("G7", set(A.retune(fl / NH * 100)) == gold, "each hour's fitted lapse in place of 6.5 C per km: same set, "
      "hours move at %s" % moved)
slope_c = -M["slope"] * 1000
check("G7", np.nanpercentile(slope_c, 1) < 0, "the hourly fitted lapse turns negative (%.1f C per km at the 1st "
      "percentile) on the hours the pools bend the line" % np.nanpercentile(slope_c, 1))
rr, _ = A.judge(M["val"], M["wh"], reg, M["G"], agg="mean")
mean_fr = (M["wh"] & rr).sum(1)
check("G8", set(A.retune(mean_fr / NH * 100)) == gold, "a mean of the stations sharing the air: same set, hours "
      "move at %s" % {codes[k]: int(mean_fr[k] - M["fr"][k]) for k in range(NS) if mean_fr[k] != M["fr"][k]})
# every graded share holds at its rounding (whole per cents) under every defensible variant
whole_g = [A.whole(x) for x in M["share"]]
var["mean of the stations sharing the air"] = mean_fr
var["each hour's fitted lapse"] = fl
for tau in (1.5, 2.5, 3.0, 3.5, 4.0, 4.5):
    rr, _ = A.judge(M["val"], M["wh"], reg, M["G"], tau=tau)
    var["tolerance %.1f" % tau] = (M["wh"] & rr).sum(1)
bad_w = {nm: [codes[k] for k in range(NS) if A.whole(v[k] / NH * 100) != whole_g[k]] for nm, v in var.items()}
check("G9", not any(bad_w.values()), "whole-per-cent shares identical at every station under %d variants" % len(var))
edge = min(min(abs(M["fr"][k] - (j + 0.5) * NH / 100.0) for j in range(0, 30)) for k in gold)
check("G9", edge >= 7, "every re-tuned station's hours sit %.1f hours or more from a whole-per-cent edge" % edge)
# the tolerance corridor's floor and ceiling, from the readings themselves
floor_idx = [k for k in range(NS) if M["G"][k]]
d_ok = []
for k in floor_idx:
    ok = ~M["anyflag"][k] & ~np.isnan(M["val"][k])
    ref = np.nanmedian(M["val"][M["G"][k]][:, ok], axis=0)
    d_ok.append(np.abs(M["val"][k, ok] - ref))
d_ok = np.concatenate(d_ok)
d_ok = d_ok[~np.isnan(d_ok)]
check("G10", np.percentile(d_ok, 99) < 1.5, "stations sharing a pool agree within %.2f C on 99 per cent of the "
      "hours the QC passed" % np.percentile(d_ok, 99))
fault_dev = []
for k in range(NS):
    i = wi[k]
    hs = np.where(M["wh"][k] & ~W["right"][i])[0]
    if not len(hs):
        continue
    if M["G"][k]:
        ref = np.nanmedian(M["val"][M["G"][k]][:, hs], axis=0)
    else:
        fa = [j for j in range(NS) if not M["G"][j] and j != k and reg["D"][k, j] <= A.FA_RADIUS_KM]
        ref = np.nanmedian(M["val"][fa][:, hs] + A.LAPSE / 1000.0 * (reg["Z"][fa] - reg["Z"][k])[:, None], axis=0)
    fault_dev.append(np.abs(M["val"][k, hs] - ref))
fault_dev = np.concatenate(fault_dev)
check("G11", fault_dev.min() > 4.5, "every wrong withheld reading is %.2f C or more from its reference" %
      fault_dev.min())
sh = M["share"]
inn = [sh[k] for k in gold]
out = [sh[k] for k in range(NS) if k not in gold]
check("G12", min(inn) >= 2.5 and max(out) <= 0.6, "the line sits in a gap: lowest re-tuned %.2f, highest other %.2f"
      % (min(inn), max(out)))
check("G13", M["nopeer"].sum() == 0, "every withheld reading has a delivered reference")

# ---------------- L: the ladder ----------------
R = A.rungs(M, TARGET)
for k, v in R.items():
    s = set(A.retune(v))
    check("L1", s != gold, "%s files %s" % (k, sites_of(reg, s)))
r2 = {tag[c] for c in sites_of(reg, A.retune(R["R2 hourly lapse refit within 5 C"]))}
check("L2", r2 == {"K4", "M3", "P3"}, "the default path (hourly lapse refit) ends on %s" % sorted(r2))
r8 = {tag[c] for c in sites_of(reg, A.retune(R["R8 HRRR forecast within 5 C"]))}
check("L3", r8 == r2, "the forecast check files the same as the lapse refit")
r7 = {tag[c] for c in sites_of(reg, A.retune(R["R7 withheld with a neighbour within 30 km"]))}
check("L4", "P3" not in r7 and r7 < GOLD_TAGS, "co-withholding misses %s" % sorted(GOLD_TAGS - r7))
pre = W["preseason"]
check("L5", max(abs(b - a) for _, _, a, b in pre) <= 0.3, "every probe passed the October check within 0.3 C")
cnt = sum(1 for k, v in R.items() if set(A.retune(v)) == gold)
check("L6", cnt == 0, "cheap routes landing the call: %d" % cnt)
# R1, the analyst test on the clean truth: every field read right, the easy route still files the wrong set
check("R1", set(A.retune(R["R2 hourly lapse refit within 5 C"])) != gold and
      set(A.retune(R["R1 every withheld reading right"])) != gold,
      "the field's background-field check and the vendor's own log both miss the golden")
# R2: the main path's mess is neutral
fr_dup = M["fr"].copy()
val2, st2 = A.feed(TARGET, reg)
check("R2", st2["duplicates"] > 0 and np.array_equal(np.nan_to_num(val2, nan=-999), np.nan_to_num(M["val"], nan=-999)),
      "re-sent feed rows (%d) carry identical readings" % st2["duplicates"])
wh_any = M["anyflag"]
rr, _ = A.judge(M["val"], wh_any, reg, M["G"])
check("R2", set(A.retune((wh_any & rr).sum(1) / NH * 100)) == gold, "counting the step test's rows too: same set")
main_files = {P.FILES[k] for k in ("feed", "qc", "register", "standard")}
ask_device_files = {P.FILES[k] for k in ("messages", "modems", "outages", "pavement", "sla")}
check("R2", not (main_files & ask_device_files), "no ask device sits in a file the main call reads")
# R3: no decoy, not semantics, not rule application
hdr = open(A.fpath(TARGET, "qc"), encoding="utf-8").readline().strip().split(",")
check("R3", not any(x in hdr for x in ("right", "valid", "verdict", "false_rejection", "confirmed")),
      "the QC log carries no verdict on its rows")
txt = open(A.fpath(TARGET, "email"), encoding="utf-8").read()
check("R3", not re.search(r"\d+(\.\d+)? per cent|lapse|pool|inversion|basin", txt), "the request carries no figure "
      "or method")
spread = {k: tuple(sites_of(reg, A.retune(v))) for k, v in R.items()}
check("R3", len(set(spread.values())) >= 6, "the enumerated family files %d different sets; the standing family "
      "(G5 to G7) files one" % len(set(spread.values())))

# ---------------- SF: the semantic fork table ----------------
check("SF1", NH == 5088 and P.WIN_START_UTC == dt.datetime(2026, 10, 1, 6), "winter = 5,088 hours from 1 Oct 00:00 MDT")
cut = M["wh"].copy()
cut[:, :6] = False
check("SF1", set(A.retune((cut & M["right"]).sum(1) / NH * 100)) == gold, "the window read from UTC midnight: same set")
deliv = (~np.isnan(M["val"])).sum(1)
check("SF2", set(A.retune(M["fr"] / deliv * 100)) == gold, "share of the hours delivered instead: same set")
check("SF3", set(A.retune(M["fr"] / NH * 100 - 1e-9)) == gold and not any(abs(x - 2.0) < 0.5 for x in sh),
      "above against at-or-above 2 per cent: same set, no share within half a point of the line")
rr, _ = A.judge(M["val"], M["wh"], reg, M["G"], tau=0.3)
ok = ~M["anyflag"] & ~np.isnan(M["val"])
bad = 0
tot = 0
for k in floor_idx:
    ref = np.nanmedian(M["val"][M["G"][k]][:, ok[k]], axis=0)
    bad += int((np.abs(M["val"][k, ok[k]] - ref) > 0.3).sum())
    tot += int(ok[k].sum())
check("SF4", bad / tot > 0.3, "0.3 C against the stations sharing the air would call %.0f per cent of the readings "
      "the QC passed wrong: the accuracy is the probe's against its own air, not a tolerance between stations" % (
          100 * bad / tot))
rr, _ = A.judge(M["val"], M["wh"], reg, M["G"], floor_rule="any")
check("SF5", ((M["wh"] & rr).sum(1) == M["fr"]).all(), "any one pool mate within the tolerance, against their median: same hours")
check("SF6", M["qc"]["step"] > 0, "the step test's rows are a different test; the standard reviews each test")
rel = set()
with open(A.fpath(TARGET, "qc"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rel.add(r["qc_release"])
check("SF7", rel == {"4.3.0", "4.3.2"}, "both releases carry the same air temperature tests (configuration 4.3)")
check("SF8", len({s["rpu"] for s in reg["sites"]}) == NS, "one RPU per site")

# ---------------- A: unavailable hours under Schedule B ----------------
Asla = S["A"]
rec_w = np.array([[x if x is not None else np.inf for x in row] for row in W["received"]], float)
late_w = rec_w - (np.arange(NH)[None, :] + 1) * 60.0
avail_w = (late_w <= P.SLA_GRACE_MIN) & ~W["outage"]
un_w = (NH - avail_w.sum(1) - W["outage"].sum(1))[wi]
check("A1", (Asla["unavailable"] == un_w).all(), "unavailable hours equal the truth at every station")
fin = late_w[np.isfinite(late_w)]
check("A2", not ((fin > 13.5) & (fin < 20.5)).any(), "no receipt between 13.5 and 20.5 minutes: the 20-minute line "
      "is clear")
placed = sorted(tag[codes[k]] for spells in Asla["placed"].values() for k, _, _ in spells)
check("A3", placed == sorted(W["spare"]), "each spell of a shop spare places at exactly one station: %s" % placed)
secs = sorted({s_["section"] for s_ in reg["sites"]})
spare_secs = sorted({reg["sites"][k]["section"] for spells in Asla["placed"].values() for k, _, _ in spells})
check("A3", spare_secs == secs, "a spare spell in every maintenance section")
check("A4", len({int(x) for x in Asla["unavailable"]}) >= 27, "unavailable hours are not one number repeated")
avail_rate = 1 - Asla["unavailable"] / (NH - Asla["excluded"])
check("A5", (avail_rate >= 0.975).sum() >= 10 and (avail_rate < 0.975).sum() >= 5, "stations either side of the "
      "97.5 per cent service level: %d at or above, %d below" % ((avail_rate >= 0.975).sum(), (avail_rate < 0.975).sum()))
import ceiling as CL  # noqa: E402
crack_un = A.by_section(reg, CL.cracker_sla(TARGET, reg, M["val"]))
gold_un = A.by_section(reg, Asla["unavailable"])
check("A6", all(crack_un[x] != gold_un[x] for x in secs), "dropping the spares' messages moves every section's "
      "unavailable station-hours: %s" % {x: gold_un[x] - crack_un[x] for x in secs})

# ---------------- B: travel-lane freezing and ice hours ----------------
B = S["B"]
frz_w = np.zeros((NS, NH), bool)
ice_w = np.zeros((NS, NH), bool)
for (t, lane, ser, model, a, b, port) in W["sensors"]:
    if lane != "travel lane":
        continue
    k = codes.index(P.SITE[t])
    i = P.TAGS.index(t)
    for h in range(a, b):
        if not W["have"][i, h]:
            continue
        sv = W["surf"][(t, lane)][h]
        f_ = (int(round(sv * 10)) / 10.0) * 9 / 5 + 32 if model == "IRS-31" else float("%.1f" % (sv * 9 / 5 + 32))
        frz_w[k, h] = f_ <= 32.0 + 1e-9
        ice_w[k, h] = W["status"][(t, lane)][h] in ("ice warning", "ice watch")
check("B1", (B["freezing"] == frz_w.sum(1)).all() and (B["ice"] == ice_w.sum(1)).all(),
      "freezing and ice hours equal the truth at every station")
check("B2", B["duplicates"] > 0, "re-sent pavement rows (%d) counted once" % B["duplicates"])
check("B3", len({int(x) for x in B["freezing"]}) >= 28 and len({int(x) for x in B["ice"]}) >= 25,
      "freezing and ice hours vary by station")
old_heads = sorted(ser for (t, lane, ser, model, a, b, port) in W["sensors"] if b < NH)
check("B4", B["unregistered"] == old_heads, "the heads that came out are the export's only unregistered serials: %s"
      % old_heads)
old_secs = sorted({reg["sites"][reg["idx"][P.SITE[t]]]["section"] for (t, lane, ser, model, a, b, port)
                   in W["sensors"] if b < NH})
check("B4", old_secs == secs, "a replaced head in every maintenance section")
cb = A.pavement(TARGET, reg, drop_unregistered=True)
for meas in ("freezing", "ice"):
    gsec, csec = A.by_section(reg, B[meas]), A.by_section(reg, cb[meas])
    check("B5", all(gsec[x] != csec[x] for x in secs), "dropping the old heads' rows moves every section's %s "
          "station-hours: %s" % (meas, {x: gsec[x] - csec[x] for x in secs}))
# the pavement export's stamps carry their zone: each is one UTC hour of the winter, one per hour
stamps = set()
with open(A.fpath(TARGET, "pavement"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        stamps.add(r["obs_time"])
st = sorted(A.utc_of_local(x) for x in stamps)
inside = all(P.WIN_START_UTC < x <= P.WIN_END_UTC for x in st)
check("B7", inside and len(set(st)) == NH, "every pavement stamp is one hour of the winter with its zone, one per hour")
amb = []
with open(A.fpath(TARGET, "outages"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        for col in ("starts", "ends"):
            d_ = dt.datetime.strptime(r[col][:16], "%Y-%m-%d %H:%M")
            if d_.date() in (dt.date(2026, 11, 1), dt.date(2027, 3, 14)) and 1 <= d_.hour <= 3:
                amb.append(r["notice_no"])
check("B7", not amb, "no planned outage starts or ends in a repeated or skipped local hour")
fwh = [h for ser, h in W["fw_change"].items()]
check("B6", all(W["utc"][h] < P.DST_ON_UTC and W["utc"][h] >= P.DST_OFF_UTC for h in fwh),
      "every firmware change falls inside standard time, so the MST export and the local applied times agree")

# ---------------- I: input gates and the realism sweep ----------------
files = sorted(os.listdir(TARGET))
check("I1", len(files) >= 10 and set(files) == set(P.FILES.values()), "%d files" % len(files))
check("I2", len({os.path.splitext(f)[1] for f in files}) >= 3, "formats %s" % sorted({os.path.splitext(f)[1]
                                                                                     for f in files}))
big = max(sum(1 for _ in open(os.path.join(TARGET, f), encoding="utf-8")) for f in files if f.endswith(".csv"))
check("I3", big >= 25000, "largest csv %d rows" % big)
meta = json.load(open(os.path.join(TASK, "metadata.json")))
check("I4", len(meta["distractors"]) >= 2 and all(d["name"] in files for d in meta["distractors"]), "distractors named")
check("I5", not any(re.search(r"readme|dictionary|manifest|notes|schema|field_guide", f, re.I) for f in files),
      "no file describes the data")
from openpyxl import load_workbook  # noqa: E402
sheets = []
for f in files:
    if f.endswith(".xlsx"):
        sheets += load_workbook(os.path.join(TARGET, f), read_only=True).sheetnames
check("I5", not any(re.search(r"readme|notes|dictionary|about|how to", s, re.I) for s in sheets), "sheets %s" % sheets)
setting = dt.datetime(2027, 5, 18, 23, 59)
with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as z:
    stamps = [dt.datetime(*zi.date_time) for zi in z.infolist()]
check("I6", max(stamps) <= setting, "zip stamps no later than the setting")
pdfs = [f for f in files if f.endswith(".pdf")]
pdf_ok = all(b"ReportLab" not in open(os.path.join(TARGET, f), "rb").read() for f in pdfs)
check("I6", pdf_ok, "no toolchain banner in the PDFs")
alltext = ""
for f in files:
    if f.endswith((".eml",)):
        alltext += open(os.path.join(TARGET, f), encoding="utf-8").read()
tells = re.findall(r"\b(leverage|robust|comprehensive|seamless|delve|ensure|furthermore)\b", alltext, re.I)
check("I7", not tells, "no LLM tells in the request")
from collections import Counter  # noqa: E402
big_w = Counter(int(x) for x in M["withheld"] if x >= 20)
fr_in = [int(M["fr"][k]) for k in gold]
check("I8", max(big_w.values()) <= 2 and len(set(fr_in)) == len(fr_in), "no withheld count shared by three stations, "
      "no two re-tuned stations with the same false-rejection hours")
dist_free = A.main_call(TARGET)
check("I9", dist_free["retune"] == M["retune"], "the call is computed without either distractor")
fig = json.load(open(os.path.join(HERE, "figures.json")))
check("I10", fig["retune_count"] == len(gold) and fig["winter_hours"] == NH, "figures.json agrees")
nfail = sum(1 for _, ok, _ in RES if not ok)
print("checks: %d, failures %d" % (len(RES), nfail))
sys.exit(1 if nfail else 0)
