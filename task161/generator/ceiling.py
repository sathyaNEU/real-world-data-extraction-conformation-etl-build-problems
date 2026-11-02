"""task161 ask layer against the careful solver's routes, on the cut pack.

    python3 task161/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The port ask gives
twenty figures (for each month of January to October 2026 the TEU of the import containers whose freight reached us
from the two ports, each in the month it arrived, and that TEU as a share of the two ports' loaded import TEU) and the
chart five criteria (one page, the ten months in order, a per-cent axis, the bars at the shares, each bar labelled with
its month's TEU). Every route below is a complete pipeline over the cut pack's receipts export, Avila's delivery
record and the two ports' releases, read here with csv and openpyxl (no generator module touches the ask), scored
figure by figure against figures.json; a TEU figure is kept when it is exact, a share when it matches to three
decimals.

The cracker is the careful solver: it lands the call (calc.golden on read.book, the bundle-only reader), reads every
field by its plain meaning (received_at_utc as UTC, the ISO 6346 size-type codes by length, the prompt's 45-foot
container at 2.25, Avila's record as the containers each of its trailers carried, the two releases' loaded import
columns), runs the hygiene battery (exact duplicate rows; the clock found from the hour profile and converted to
Pacific; repeated container numbers paired into one arrival where the receipts fall within days, a gap that the
profile below shows is bimodal; 53-foot trailers anti-joined to Avila's record, the unmatched ones domestic transfers
with no port container; Avila's record checked for a container listed twice) and dates each container in the month it
arrived, as the prompt files. The mirror is the best response off the call (the default path, the book's excess faded
at the earlier rushes' half-life, no block) on its natural read without the battery: each ocean-box receipt row a
container, Avila's containers by the trailer's receipt, the month from the stamp's own date. The full includer handles
every device and must give back figures.json exactly or the script exits 1 (the route code's control). The stops are
the sheet's other wrong paths, each scored as a route.

The pair is the sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over the 25 ask
criteria (twenty figures and the chart's five), a response off the call keeping r = 5 of the 38. Pair ceiling is the
worst of the measured pair and the mirror on the cracker's ask path. The script modifies nothing and never runs inside
the build."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import warnings
import zipfile
from zoneinfo import ZoneInfo

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

TASK = os.path.dirname(HERE)
PACIFIC = ZoneInfo("America/Los_Angeles")
RECEIPTS = "wms_inbound_receipts_20220912_20261206.csv"
AVILA = "avila_deliveries_2024-03_2026-12.xlsx"
POLA = "pola_container_stats_2026.csv"
POLB = "polb_teu_stats_2026.csv"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October"]
KEYS = [(2026, m) for m in range(1, 11)]
TEU_BY_LENGTH = {"2": 1.0, "4": 2.0, "L": 2.25}       # ISO 6346 size code's first character: 20, 40 and 45 ft
REC, INS, ASK, OFF = 38.0, 7.0, 55.0, 5.0
N_FIG, N_CHART = 20, 5
N_ASK = N_FIG + N_CHART


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling161-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)), md5)


# ----------------------------------------------------------------------------------- reading the pack

def utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def load(folder):
    import openpyxl
    rows = []
    with open(os.path.join(folder, RECEIPTS), newline="") as fh:
        raw = list(csv.reader(fh))
    head = raw[0]
    for r in raw[1:]:
        d = dict(zip(head, r))
        ts = utc(d["received_at_utc"])
        rows.append({"row": tuple(r), "ts": ts, "pac": ts.astimezone(PACIFIC).date(), "utc_date": ts.date(),
                     "eq": d["equipment_id"], "type": d["equipment_type"], "pallets": int(d["pallets"]),
                     "client": d["client_id"]})
    ws = openpyxl.load_workbook(os.path.join(folder, AVILA), read_only=True, data_only=True)["Deliveries"]
    it = ws.iter_rows(min_row=4, values_only=True)
    ah = list(next(it))
    av = []
    for r in it:
        d = dict(zip(ah, r))
        if d.get("Trailer") is None:
            continue
        dd = d["Delivery Date"]
        av.append({"trailer": d["Trailer"], "container": d["Container"], "iso": d["ISO Type"],
                   "delivered": dd.date() if hasattr(dd, "date") else dd, "port": d["Port"]})
    la, lb = {}, {}
    with open(os.path.join(folder, POLA), newline="") as fh:
        for r in csv.DictReader(fh):
            p = r["Month"].split()
            if len(p) == 2 and p[0] in MONTHS and p[1] == "2026":
                la[(2026, MONTHS.index(p[0]) + 1)] = int(r["Loaded Imports"])
    ab = [m[:3].upper() for m in MONTHS]
    with open(os.path.join(folder, POLB), newline="") as fh:
        for r in csv.DictReader(fh):
            if r["Year"] == "2026" and r["Month"] in ab:
                lb[(2026, ab.index(r["Month"]) + 1)] = int(r["Inbound Loaded"])
    return rows, av, la, lb


def teu_of(code, teu45=2.25):
    """TEU by the container's length, from the ISO 6346 size code (the prompt files a 45-foot container at 2.25)."""
    t = TEU_BY_LENGTH.get(code[:1])
    if t is None:
        return None
    return teu45 if code[:1] == "L" else t


def battery(rows, av):
    """The hygiene battery a careful analyst runs on the receipts before counting: (check, detail) lines."""
    out = []
    n = len(rows)
    out.append(("exact duplicate rows", "%d of %d" % (n - len({r["row"] for r in rows}), n)))
    hours = {}
    for r in rows:
        hours[r["ts"].hour] = hours.get(r["ts"].hour, 0) + 1
    span = sorted(h for h, c in hours.items() if c > 0)
    out.append(("hour profile of received_at_utc", "receipts at %s UTC, i.e. 06:00 to 22:00 Pacific: the stamps are UTC "
                "and converted" % ", ".join("%02d" % h for h in span)))
    boxes = [r for r in rows if teu_of(r["type"]) is not None]
    last, gaps = {}, []
    for r in sorted(boxes, key=lambda x: x["ts"]):
        if r["eq"] in last:
            gaps.append((r["pac"] - last[r["eq"]]).days)
        last[r["eq"]] = r["pac"]
    near = sum(1 for g in gaps if g <= 3)
    mid = sum(1 for g in gaps if 3 < g < 60)
    far = sum(1 for g in gaps if g >= 60)
    out.append(("repeated container numbers", "%d repeats: %d within 3 days (one box devanned over two shifts), %d at 4 "
                "to 59 days, %d at 60 days or more (the box back with new freight, shortest %s days)" %
                (len(gaps), near, mid, far, min([g for g in gaps if g >= 60] or [0]))))
    av_tl = {a["trailer"] for a in av}
    tl = [r for r in rows if r["type"] == "53DV"]
    matched = sum(1 for r in tl if r["eq"] in av_tl)
    prefixes = sorted({r["eq"][:4] for r in tl if r["eq"] not in av_tl})
    out.append(("53-foot trailers anti-joined to Avila's record", "%d of %d matched; the %d unmatched carry the "
                "prefixes %s (accounts' own DCs, no port container)" % (matched, len(tl), len(tl) - matched, prefixes)))
    cn = [a["container"] for a in av]
    out.append(("Avila's record: a container listed twice", "%d" % (len(cn) - len(set(cn)))))
    tday = {r["eq"]: r["pac"] for r in tl}
    out.append(("Avila's delivery date against the trailer's Pacific receipt date", "%d of %d agree" % (
        sum(1 for a in av if tday.get(a["trailer"]) == a["delivered"]), len(av))))
    out.append(("Avila's ports", ", ".join(sorted({a["port"] for a in av}))))
    return out


# ----------------------------------------------------------------------------------- the routes

def route(rows, av, la, lb, visits="gap", gap_days=7, trailers="avila", month="pacific", teu45=2.25, date_at="first"):
    """The twenty figures a route gives: TEU per month and share per cent of the two ports' loaded imports.
    visits: 'gap' pairs receipts of one container number within gap_days into one arrival; 'rows' counts every row;
    'global' collapses every repeat of a number into its first arrival. trailers: 'avila' counts the containers in
    Avila's record at the trailer's receipt, 'none' counts no trailer, 'len' counts every 53-foot trailer at 53/20.
    month: 'pacific' or 'utc'. date_at: an arrival dated at its 'first' or 'last' receipt."""
    day = (lambda r: r["pac"]) if month == "pacific" else (lambda r: r["utc_date"])
    teu = {k: 0.0 for k in KEYS}
    boxes = sorted([r for r in rows if teu_of(r["type"]) is not None], key=lambda x: x["ts"])
    arrivals = []
    if visits == "rows":
        arrivals = [(day(r), r["type"]) for r in boxes]
    elif visits == "global":
        seen = set()
        for r in boxes:
            if r["eq"] not in seen:
                seen.add(r["eq"])
                arrivals.append((day(r), r["type"]))
    else:
        open_ = {}
        for r in boxes:
            k = r["eq"]
            if k in open_ and (day(r) - open_[k]["last"]).days <= gap_days:
                open_[k]["last"] = day(r)
                continue
            if k in open_:
                v = open_[k]
                arrivals.append((v["first"] if date_at == "first" else v["last"], v["type"]))
            open_[k] = {"first": day(r), "last": day(r), "type": r["type"]}
        for v in open_.values():
            arrivals.append(((v["first"] if date_at == "first" else v["last"]), v["type"]))
    for d, typ in arrivals:
        k = (d.year, d.month)
        if k in teu:
            teu[k] += teu_of(typ, teu45)
    src = {}
    for a in av:
        src.setdefault(a["trailer"], []).append(a["iso"])
    for r in rows:
        if r["type"] != "53DV":
            continue
        k = (day(r).year, day(r).month)
        if k not in teu:
            continue
        if trailers == "avila" and r["eq"] in src:
            teu[k] += sum(teu_of(x, teu45) for x in src[r["eq"]])
        elif trailers == "len":
            teu[k] += 53.0 / 20.0
    share = {k: 100.0 * teu[k] / (la[k] + lb[k]) for k in KEYS}
    return teu, share


def scored(fig, gold):
    teu, share = fig
    t = sum(1 for k, m in zip(KEYS, MONTHS) if int(round(teu[k] + 1e-9)) == gold["teu"]["%s 2026" % m])
    s = sum(1 for k, m in zip(KEYS, MONTHS) if "%.3f" % round(share[k] + 1e-12, 3) == gold["share"]["%s 2026" % m])
    chart = 3 + (1 if s == 10 else 0) + (1 if t == 10 else 0)     # page, months in order, axis; bars; labels
    return {"teu": t, "share": s, "chart": chart, "kept": t + s + chart}


def pair(kc, km):
    c = REC + INS + ASK * kc / N_ASK
    s = OFF + INS + ASK * km / N_ASK
    return c, s, (c + s) / 2.0


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    gold = {"teu": F["a2_teu"], "share": F["a2_share"]}

    # the calls, on the bundle-only reader
    import calc
    import read
    B = read.book(folder)
    g = calc.golden(B)
    fade = calc.rival_decay(B)
    on_call = g["blocks"] == F["call"]["blocks"]
    off_call = fade["blocks"] != F["call"]["blocks"]
    print("cracker's call: %d blocks, block uses %s (%s)" % (g["blocks"], [round(u, 3) for u in g["use"][:4]],
                                                              "lands the golden" if on_call else "MISSES"))
    print("mirror's call (the default path, a fade at a %.2f-month half-life): %d blocks (%s)" % (
        fade["half_life_months"], fade["blocks"], "off the call" if off_call else "ON THE CALL"))
    if not (on_call and off_call):
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1

    rows, av, la, lb = load(folder)
    print("\nthe cracker's hygiene battery on the receipts export and Avila's record:")
    for check, detail in battery(rows, av):
        print("  %-62s %s" % (check, detail))

    full = scored(route(rows, av, la, lb, visits="gap", gap_days=3), gold)
    if full["teu"] != 10 or full["share"] != 10:
        print("CONTROL FAILED: the full includer gives %d TEU and %d shares of 10, the route code does not reproduce "
              "figures.json" % (full["teu"], full["share"]))
        return 1
    crk_fig = route(rows, av, la, lb, visits="gap", gap_days=7)
    crk = scored(crk_fig, gold)
    grid = {gd: scored(route(rows, av, la, lb, visits="gap", gap_days=gd), gold)["kept"] for gd in (4, 7, 14, 30, 59)}
    mir = scored(route(rows, av, la, lb, visits="rows", month="utc"), gold)
    stops = {
        "every receipt row a container, Pacific months": dict(visits="rows"),
        "every repeat of a number collapsed into its first arrival": dict(visits="global"),
        "no 53-foot trailer counted": dict(trailers="none"),
        "every 53-foot trailer at 53/20 TEU": dict(trailers="len"),
        "months from the UTC stamp's date": dict(month="utc"),
        "a 45-foot container at 2 TEU": dict(teu45=2.0),
        "an arrival dated at its last receipt": dict(date_at="last"),
    }
    print("\nper route, ask criteria kept of %d (TEU of 10, shares of 10, chart of 5):" % N_ASK)
    print("  %-64s %2d  (TEU %d, shares %d, chart %d)" % ("cracker (careful solver, arrivals paired within 7 days)",
                                                          crk["kept"], crk["teu"], crk["share"], crk["chart"]))
    print("  %-64s %s" % ("  the same with the pairing window at 4, 7, 14, 30 or 59 days", grid))
    print("  %-64s %2d  (TEU %d, shares %d, chart %d)" % ("mirror (off the call, natural read, no battery)",
                                                          mir["kept"], mir["teu"], mir["share"], mir["chart"]))
    for nm, kw in stops.items():
        s = scored(route(rows, av, la, lb, **kw), gold)
        print("  %-64s %2d  (TEU %d, shares %d)" % ("stop: " + nm, s["kept"], s["teu"], s["share"]))
    print("  %-64s %2d  (control, figures.json reproduced)" % ("full includer (arrivals paired within 3 days)",
                                                              full["kept"]))
    print("\nthe cracker's figures (figures.json in brackets):")
    for k, m in zip(KEYS, MONTHS):
        lab = "%s 2026" % m
        print("  %-9s %5d TEU (%5d)  %.3f%% (%s%%)" % (m, int(round(crk_fig[0][k])), gold["teu"][lab],
                                                     round(crk_fig[1][k], 3), gold["share"][lab]))

    c, s, p = pair(crk["kept"], mir["kept"])
    _, s2, p2 = pair(crk["kept"], crk["kept"])
    both = pair(crk["kept"], crk["kept"])[0]
    print("\nthe sheet's formula (38, 7, 55 over the %d ask criteria; r = 5): cracker %.1f, mirror %.1f, pair %.1f"
          % (N_ASK, c, s, p))
    print("  the mirror on the cracker's ask path (the battery run, off the call): mirror %.1f, pair %.1f" % (s2, p2))
    print("  two careful responses on the call: %.1f each, pair %.1f" % (both, both))
    print("\nCracker keeps: %d of %d ask figures (%d of %d ask criteria)" % (crk["teu"] + crk["share"], N_FIG,
                                                                            crk["kept"], N_ASK))
    print("Mirror leakage: %.1f per cent of ask weight (%.1f on the cracker's ask path)" % (
        100.0 * mir["kept"] / N_ASK, 100.0 * crk["kept"] / N_ASK))
    print("Pair ceiling: %.1f (the worst of the measured pair %.1f and the mirror on the cracker's ask path)" % (
        max(p, p2), p))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
