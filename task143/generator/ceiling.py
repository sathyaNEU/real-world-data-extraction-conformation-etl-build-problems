"""task143 ask layer against the careful solver's routes, on the cut pack.

    python3 task143/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The script modifies
nothing and never runs inside the build.

The asks give 20 figures: for each repair partner the capacity replacements under the warranty it carried out from
October 2025 to September 2026 and what one cost on average to the nearest euro (8), and the capacity replacements
under the warranty carried out in each of the twelve months across the service regions (12). Every route below is a
complete pipeline over the cut pack's service and costing files, scored figure by figure against figures.json: a
count is kept only when exact, an average when it rounds to the golden euro.

The cracker lands the call (the golden construction on the lab's files), runs the hygiene battery on the ask files
(exact duplicate rows in every file; the reissued invoice in place of the one it replaces; the depot's carried-over
SAP orders matched to their cases through legacy_ref; the cases anti-joined to the invoice lines and to the returns
log, the returns log to the carrier statement; a header amount on its item rows: the log's freight against the
carrier's charge and pieces; both clocks on a partner case: its closing day against its invoice's service period;
each code against its text or its own evidence), executes every filed rule as worded (the cost sheet's costing:
the invoice line at treasury's month-end rate for the invoice's service period, the return freight of the removed
battery, the service pack at the standard cost valid when it was fitted) and takes each ask on its natural read.
The mirror stops at the call's default path (independent cells, 500 packs) and takes the asks on the natural read
without the battery; it is scored again running the battery (the cracker's ask path, off the call). The full
includer handles every device and has to give back figures.json exactly or the script exits 1.

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over the
ask criteria (the 20 figures and the chart's three form criteria, which any response drawing the chart keeps), a
method credit of 8 per cent on every ask criterion not kept, a response off the call keeping 5 of the 38. Pair
ceiling is the worst of the measured pair, the pair with the mirror running the battery and every single device
the cracker could be granted."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C     # noqa: E402  (the bundle-only readers)
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
REC, INS, ASK, OFF, CREDIT = 38.0, 7.0, 55.0, 5.0, 0.08
CHART_FORM = 3            # one stacked bar a month, the regions, each bar's total: kept by any response drawing it
LABEL = {"DVG": "Dauvergne Réparation", "TMR": "Tolley Marsh Repair", "LJQ": "Ljungqvist Service",
         "FRC": "Ferrucci Assistenza"}

# a route: dating (period: the invoice's service period; closed: the case's closing day), freight (share: the
# consignment's charge over its pieces; log: the returns log's Freight EUR on the battery's row), invoices (latest:
# a reissue replaces the invoice it names; all: both versions), dach (dedupe: carried-over orders once through
# legacy_ref; both: counted in each system), cover (WTY: the warranty code; all: goodwill kept), fx (period: the
# month-end rate of the service period, the cost sheet's rule; issue: the invoice date's month), pack (dated: the
# standard cost valid in the repair month; current: the latest row)
CRACKER = dict(dating="period", freight="share", invoices="latest", dach="dedupe", cover="WTY", fx="period",
               pack="dated")
MIRROR = dict(dating="closed", freight="log", invoices="all", dach="both", cover="WTY", fx="period", pack="dated")
FULL = dict(CRACKER)
CRACKS = {}               # devices the cracker could be granted (none: every device below is a battery item)


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling143-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    inner = os.path.join(tmp, "target")
    folder = inner if os.path.isdir(inner) else tmp
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return folder, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(folder)), md5)


# ---------------------------------------------------------------------------------------------------- the battery
def battery(t):
    """The hygiene battery on the ask files: (check, finding, what the careful solver does with it)."""
    out = []
    cs = C.cases(t)
    rows = [tuple(r.values()) for r in cs]
    out.append(("exact duplicate case rows", "%d" % (len(rows) - len(set(rows))), "none to drop"))
    inv_all = C.invoice_lines(t, keep_replaced=True)
    inv = C.invoice_lines(t)
    gone = {l["invoice"] for l in inv_all} - {l["invoice"] for l in inv}
    out.append(("a reissue in place of the invoice it replaces", ", ".join(sorted(gone)) or "none",
                "the replaced invoice dropped, its duplicated job with it"))
    keyc = Counter((l["partner"], l["job"]) for l in inv)
    out.append(("one line per job on the invoices in force", "%d repeated" % sum(v > 1 for v in keyc.values()),
                "none left"))
    sap = C.sap_orders(t)
    sapno = {str(r["Auftrag"]) for r in sap}
    mig = [r for r in cs if r["legacy_ref"]]
    out.append(("the depot's carried-over SAP orders matched to their cases (legacy_ref)",
                "%d cases carry an SAP order, %d of them found in SAP" % (len(mig), sum(r["legacy_ref"] in sapno
                                                                                   for r in mig)),
                "an order completed in SAP counted once, from SAP"))
    line_of = {l["case"] for l in inv}
    rep = [r for r in cs if r["region"] != "DACH" and r["fault_code"] == "CAP" and r["warranty"] == "WTY" and
           r["action"] == "REPLACED"]
    first_inv = min(dt.date(*l["period"], 1) for l in inv)
    orph = [r for r in rep if r["case_no"] not in line_of]
    out.append(("partner replacements anti-joined to the invoice lines", "%d of %d without a line, all opened before "
                "the first invoice's period" % (len(orph), len(rep)) if all(C._d(r["opened_utc"]) < first_inv
                                                                          for r in orph) else
                "%d of %d without a line, some inside the window" % (len(orph), len(rep)),
                "each replacement priced on its line"))
    carrier, by_ref = C.freight(t)
    first_pick = min(dt.date.fromisoformat(r["pickup_date"]) for r in C._csv(os.path.join(
        t, "carrier_statement_inbound_returns_2025-09_2026-10.csv")))
    ret = C._xlsx_rows(os.path.join(t, "depot_returns_log_2024-09_2026-09.xlsx"))
    received = {str(r[1]): C._d(r[0]) for r in ret[1:]}
    oc = {v[0] for v in by_ref.values() if v[1] is not None and v[0] not in carrier}
    out.append(("returns log anti-joined to the carrier statement", "%d partner consignments not on the statement, %s"
                % (len(oc), "all received before its first pickup" if all(received[c] <= first_pick for c in oc)
                   else "some inside its span"), "none in the window"))
    nolog = [r for r in rep if r["case_no"] in line_of and r["case_no"] not in by_ref]
    out.append(("partner replacements anti-joined to the returns log", "%d billed replacements with no battery "
                                                                      "received" % len(nolog),
                "no freight for a battery that never travelled (every reading rounds alike)"))
    per = Counter(v[0] for v in by_ref.values())
    whole = sum(1 for v in by_ref.values() if v[1] is not None and v[0] in carrier and
                abs(float(v[1]) - carrier[v[0]][0]) < 0.005)
    pieces_ok = sum(1 for k, (ch, pcs) in carrier.items() if per.get(k) == pcs)
    out.append(("a header amount on its item rows: the log's freight against the carrier's charge",
                "%d of %d rows carry their whole consignment's charge; pieces equal the log's rows in %d of %d "
                "consignments" % (whole, sum(1 for v in by_ref.values() if v[1] is not None), pieces_ok, len(carrier)),
                "each battery takes its consignment's charge over its pieces"))
    cs_by = {r["case_no"]: r for r in cs}
    period = {l["case"]: l["period"] for l in inv}
    after = sum(1 for r in rep if r["case_no"] in period and r["closed_utc"] and C._d(r["closed_utc"]) >= dt.date(
        period[r["case_no"]][0] + period[r["case_no"]][1] // 12, period[r["case_no"]][1] % 12 + 1, 1))
    openr = sum(1 for r in rep if r["case_no"] in period and not r["closed_utc"])
    days = Counter((r["partner"], r["closed_utc"][:10]) for r in rep if r["closed_utc"])
    out.append(("both clocks on a partner case: closing day against its invoice's service period",
                "%d of %d close after their service period ends, %d billed but still open, %d closing days" % (
                    after, sum(1 for r in rep if r["case_no"] in period and r["closed_utc"]), openr, len(days)),
                "the closing day is the desk's approval; a job is carried out in its invoice's service period"))
    texts = {(r["Auftragsart"], r["Auftragsartentext"]) for r in sap} | {(r["Schadenscode"], r["Schadenstext"])
                                                                       for r in sap}
    out.append(("each SAP code against its own text", "%d code-text pairs, one text a code" % len(texts),
                "ZS01 the warranty repair, B10 the capacity fault"))
    fcc = [float(r["fcc_pct"]) for r in cs if r["fault_code"] == "CAP" and r["fcc_pct"]]
    out.append(("the case system's CAP against its full charge capacity", "max %.1f per cent over %d cases" % (
        max(fcc), len(fcc)), "CAP is the capacity fault"))
    bad = [r["case_no"] for r in cs if r["fault_code"] == "CAP" and r["cycle_count"] and
           (r["warranty"] == "WTY") != (int(r["cycle_count"]) <= 600)]
    out.append(("the warranty code against the gauge's cycle count", "%d disagree" % len(bad),
                "WTY is the battery warranty"))
    return out


# ---------------------------------------------------------------------------------------------------- the routes
def route(t, r, L=None):
    """The 20 figures a route gives: {partner: (count, average)} and {month: count}."""
    L = L or {}
    if "inv" not in L:
        L["inv"] = {"latest": C.invoice_lines(t), "all": C.invoice_lines(t, keep_replaced=True)}
        L["cs"] = C.cases(t)
        L["fx"] = C.fx_table(t)
        L["cost"] = C.cost_tables(t)
        L["freight"] = C.freight(t)
        L["sap"] = C.sap_orders(t)
    inv = L["inv"][r["invoices"]]
    cs = L["cs"]
    fx = L["fx"]
    pack, depot, coll = L["cost"]
    carrier, by_ref = L["freight"]
    cover = ("WTY",) if r["cover"] == "WTY" else ("WTY", "GW")
    line = defaultdict(list)
    for l in inv:
        line[l["case"]].append(l)
    n, tot = Counter(), defaultdict(float)
    months = Counter()
    for c in cs:
        if c["fault_code"] != "CAP" or c["warranty"] not in cover or c["action"] != "REPLACED":
            continue
        if c["region"] == "DACH":
            continue
        ls = line.get(c["case_no"], [])
        if r["dating"] == "period":
            if not ls:
                continue
            ym = ls[0]["period"]
        else:
            if not c["closed_utc"]:
                continue
            d = C._d(c["closed_utc"])
            ym = (d.year, d.month)
        if ym not in C.WINDOW:
            continue
        months[ym] += 1
        if not ls:
            continue
        p = c["partner"]
        cost = 0.0
        for l in ls:                       # every line billing the case (a duplicated job shows here)
            y, m = ym if r["fx"] == "period" else (l["period"][0] + l["period"][1] // 12, l["period"][1] % 12 + 1)
            rate = 1.0
            if l["currency"] != "EUR":
                while (y, m, l["currency"]) not in fx:
                    y, m = (y, m - 1) if m > 1 else (y - 1, 12)
                rate = fx[(y, m, l["currency"])]
            cost += l["amount"] / rate
        fr = 0.0
        if c["case_no"] in by_ref:
            cn, row_fr = by_ref[c["case_no"]]
            if r["freight"] == "share":
                ch, pcs = carrier[cn]
                fr = ch / pcs
            elif r["freight"] == "log":
                fr = float(row_fr or 0.0)
        pc = C.valid(pack, dt.date(ym[0], ym[1], 15)) if r["pack"] == "dated" else pack[-1][2]
        n[p] += 1
        tot[p] += cost + fr + pc
    # the depot: SAP orders by Techn. Abschluss, its cases by their closing day
    done = set()
    for o in L["sap"]:
        if o["Schadenscode"] == "B10" and o["Auftragsart"] in (("ZS01",) if r["cover"] == "WTY" else ("ZS01", "ZS02")) \
                and o["Techn. Abschluss"] and o["Einbau-SN"]:
            d = C._d(o["Techn. Abschluss"])
            if (d.year, d.month) in C.WINDOW:
                months[(d.year, d.month)] += 1
            done.add(str(o["Auftrag"]))
    for c in cs:
        if c["region"] != "DACH" or c["fault_code"] != "CAP" or c["warranty"] not in cover or \
                c["action"] != "REPLACED" or not c["closed_utc"]:
            continue
        if r["dach"] == "dedupe" and c["legacy_ref"] and c["legacy_ref"] in done:
            continue
        d = C._d(c["closed_utc"])
        if (d.year, d.month) in C.WINDOW:
            months[(d.year, d.month)] += 1
    a = {p: (n[p], tot[p] / n[p] if n[p] else 0.0) for p in C.PARTNERS}
    return a, {ym: months[ym] for ym in C.WINDOW}


def golden():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    ga = {p: (int(f["ask_a"][p]["replacements"]), int(f["ask_a"][p]["average_cost_eur"])) for p in C.PARTNERS}
    gb = {ym: int(f["ask_b"][dt.date(ym[0], ym[1], 1).strftime("%B %Y")]) for ym in C.WINDOW}
    return ga, gb


def kept(fig, gold):
    a, b = fig
    ga, gb = gold
    ka_n = sum(a[p][0] == ga[p][0] for p in C.PARTNERS)
    ka_c = sum(a[p][0] > 0 and K.round_to(a[p][1], 1) == ga[p][1] for p in C.PARTNERS)
    kb = sum(b[ym] == gb[ym] for ym in C.WINDOW)
    return {"A replacements": ka_n, "A average cost": ka_c, "B months": kb}


def pair(kc, km, n):
    pts = lambda k: ASK * (k + CREDIT * (n - k)) / n
    c, s = REC + INS + pts(kc), OFF + INS + pts(km)
    return c, s, (c + s) / 2.0


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(t, stamp):
    print("pack: " + stamp)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    gold = golden()
    n_fig = 4 + 4 + 12
    n = n_fig + CHART_FORM

    # the calls
    mc = C.main_call(t)
    call = K.round_to(mc["golden"], 50)
    r0 = mc["rungs"]["R0 default: the cell chance at the model error, three independent cells"]
    on_call = call == int(figs["call"]["reserve_packs"])
    off_call = K.round_to(r0, 50) != int(figs["call"]["reserve_packs"])
    print("cracker's call: %.1f packs, files %d (%s the golden %s)" % (mc["golden"], call,
                                                                       "lands" if on_call else "MISSES",
                                                                       figs["call"]["reserve_packs"]))
    print("mirror's call (the default path, independent cells): %.1f packs, files %d (%s)" % (
        r0, K.round_to(r0, 50), "off the call" if off_call else "ON THE CALL"))
    if not (on_call and off_call):
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1

    print("\nthe cracker's hygiene battery on the ask files:")
    for check, finding, does in battery(t):
        print("  %-78s %s; %s" % (check, finding, does))

    L = {}
    full = route(t, FULL, L)
    kf = kept(full, gold)
    if sum(kf.values()) != n_fig:
        print("CONTROL FAILED: the full includer keeps %s of %d, the route code does not reproduce figures.json" % (
            kf, n_fig))
        return 1
    crk = route(t, CRACKER, L)
    mir = route(t, MIRROR, L)
    mirb = route(t, CRACKER, L)          # the mirror running the battery: the cracker's ask path, off the call
    kc, km, kmb = kept(crk, gold), kept(mir, gold), kept(mirb, gold)

    ga, gb = gold
    for who, fig in (("cracker", crk), ("mirror", mir), ("full includer (control)", full)):
        a, b = fig
        print("\n%s (golden in brackets):" % who)
        print("  A " + "; ".join("%s %d at %.2f (%d at %d)" % (LABEL[p], a[p][0], a[p][1], ga[p][0], ga[p][1])
                                 for p in C.PARTNERS))
        print("  B " + ", ".join("%d (%d)" % (b[ym], gb[ym]) for ym in C.WINDOW))
    print("\nper ask, figures kept:")
    print("  %-22s %-9s %-9s %-26s %s" % ("", "cracker", "mirror", "mirror with the battery", "full includer"))
    for k, tot_ in (("A replacements", 4), ("A average cost", 4), ("B months", 12)):
        print("  %-22s %-9d %-9d %-26d %d of %d" % (k, kc[k], km[k], kmb[k], kf[k], tot_))
    skc, skm, skmb = sum(kc.values()), sum(km.values()), sum(kmb.values())
    print("  %-22s %-9d %-9d %-26d %d of %d" % ("all asks", skc, skm, skmb, sum(kf.values()), n_fig))

    worst = []
    c, s, p = pair(skc + CHART_FORM, skm + CHART_FORM, n)
    worst.append(p)
    print("\nthe sheet's formula (38, 7, 55 over %d ask criteria, 8 per cent method credit, r = 5): cracker %.1f, "
          "mirror %.1f, pair %.1f" % (n, c, s, p))
    pm = pair(skc + CHART_FORM, skmb + CHART_FORM, n)[2]
    worst.append(pm)
    print("  if the mirror runs the hygiene battery (the cracker's ask path, off the call): pair %.1f" % pm)
    for nm, ch in CRACKS.items():
        k = sum(kept(route(t, dict(CRACKER, **ch), L), gold).values())
        pc = pair(k + CHART_FORM, skm + CHART_FORM, n)[2]
        worst.append(pc)
        print("  if the cracker %s: %d of %d, pair %.1f" % (nm, k, n_fig, pc))
    print("  (both top responses on the call with no device found: %.1f)" % (
        (REC + INS + ASK * (n_fig + CHART_FORM) / n)))

    print("\nCracker keeps: %d of %d ask figures" % (skc, n_fig))
    print("Mirror leakage: %.1f per cent of ask weight (%.1f running the battery)" % (
        100.0 * (skm + CHART_FORM + CREDIT * (n - skm - CHART_FORM)) / n,
        100.0 * (skmb + CHART_FORM + CREDIT * (n - skmb - CHART_FORM)) / n))
    print("Pair ceiling: %.1f (the worst of the measured pair, the mirror running the battery and each single device "
          "granted)" % max(worst))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
