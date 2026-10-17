"""The independent verifier: reads only the shipped bundle (python3 verify.py <target>), recomputes the call, every
rung and every graded ask figure on its own code path (the csv module and openpyxl, no generator state, no pandas),
finds the asks' devices from the data rather than from what the generator knows, and compares everything with
generator/figures.json. Exit 0 when every figure agrees."""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import Counter, defaultdict
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
LONDON = ZoneInfo("Europe/London")
FAIL = []


def same(label, a, b, tol=0):
    if isinstance(a, dict):
        for k in a:
            same("%s / %s" % (label, k), a[k], b[k], tol)
        return
    if abs(a - b) > tol:
        FAIL.append("%s: verifier %s, figures.json %s" % (label, a, b))


def rows_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def rows_xlsx(path, sheet):
    ws = load_workbook(path, read_only=True, data_only=True)[sheet]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it if any(v is not None for v in r)]


def half_up(x):
    return int((x * 2 + 1) // 2)


def main(target):
    P = lambda name: os.path.join(target, name)
    files = os.listdir(target)
    find = lambda pat: [f for f in files if re.search(pat, f)][0]
    F = json.load(open(os.path.join(HERE, "figures.json")))

    # ---------------------------------------------------------------------------- the levy papers: councils, total
    gaz = rows_csv(P(find(r"gazetteer")))
    council = {}
    for g in gaz:
        council[g["area_code"]] = g["council"]
    req = F["call"]["requirement"]

    # ---------------------------------------------------------------------------- the survey
    wt = {r["case_id"]: float(r["weight"]) for r in rows_csv(P(find(r"weights")))}
    recs = []
    for r in rows_xlsx(P(find(r"wave1\.xlsx")), "Interviews"):
        wave, serial = r["Interview No"].split("-")[1:]
        recs.append((r["Home area"], int(r["Visits to Authority parks, last 12 months (incl. today)"]),
                     wt["%s-%s" % (wave, serial)]))
    for r in rows_csv(P(find(r"wave2\.csv"))):
        _, wave, serial = r["case_ref"].split("/")
        recs.append((r["home_area_code"], int(r["q9_visits_12m"]), wt["%s-%s" % (wave, serial)]))
    assert len(recs) == len(wt), "interviews and weights differ"
    members = sorted(council)
    est = {k: defaultdict(float) for k in ("golden", "raw", "visits", "unweighted", "wf")}
    for code, f, w in recs:
        if code not in council:
            continue
        est["golden"][code] += w / f
        est["raw"][code] += 1
        est["visits"][code] += w
        est["unweighted"][code] += 1 / f
        est["wf"][code] += w * f
    est["mean"] = {c: est["visits"][c] ** 2 / est["wf"][c] for c in members}
    valley = [c for c in members if council[c] in ("Keldmere District Council", "Ravenwick Borough Council",
                                                   "Snelgarth District Council")]
    tot = sum(est["golden"].values())
    levy = {council[c]: half_up(req * est["golden"][c] / tot) for c in members}
    same("levy", levy, F["call"]["levy"])
    same("levy total", sum(levy.values()), req)
    same("residents", {council[c]: int(round(est["golden"][c], -2)) for c in members}, F["call"]["residents"])
    for k in ("raw", "visits", "mean", "unweighted", "golden"):
        s = 100 * sum(est[k][c] for c in valley) / sum(est[k][c] for c in members)
        same("rung %s valley share" % k, round(s, 1), F["rungs"][k], 1e-9)

    # ---------------------------------------------------------------------------- Ask A
    park_name = {"GF": "Gorthfield Country Park", "DW": "Daskbeck Water Park", "LM": "Lockshaw Moor",
                 "TH": "Thruscote Hall"}
    tariffs = rows_xlsx(P(find(r"tariffs")), "Tariffs 2025-26")
    charges = defaultdict(set)
    for t in tariffs:
        charges[t["Car park code"][:2]].add(round(float(t["Charge (GBP)"]), 2))
    assets = rows_csv(P(find(r"asset_register")))
    reg_site = {a["asset_id"]: a["site_code"] for a in assets}
    seen, takings = set(), defaultdict(float)
    day_amounts = defaultdict(set)
    tickets = []
    for r in rows_csv(P(find(r"pay_machine"))):
        key = (r["machine_id"], r["ticket_no"])
        if key in seen:
            continue
        seen.add(key)
        when = dt.datetime.strptime(r["paid_at_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
        day = when.astimezone(LONDON).date()
        amt = round(float(r["amount_gbp"]), 2)
        tickets.append((r["machine_id"], day, amt))
        day_amounts[(r["machine_id"], day)].add(amt)
    stood = {}
    for mid in {t[0] for t in tickets}:
        own = reg_site[mid][:2]
        odd = sorted(d for (m, d), a in day_amounts.items() if m == mid and not a <= charges[own])
        if odd:
            cands = set(charges)
            for d in odd:
                cands &= {p for p in charges if day_amounts[(mid, d)] <= charges[p]}
            assert len(cands) == 1, (mid, cands)
            stood[mid] = (odd[-1], cands.pop())
    for mid, day, amt in tickets:
        park = reg_site[mid][:2]
        if mid in stood and day <= stood[mid][0]:
            park = stood[mid][1]
        takings[park] += amt
    app = defaultdict(float)
    for r in rows_xlsx(P(find(r"parking_app")), "Statement lines"):
        app[r["Location code"][4:6]] += float(r["Parking income (GBP)"])
    for p, nm in park_name.items():
        m, a = takings[p] / 1.2, app[p]
        same("Ask A %s total" % nm, half_up(m + a), F["ask_a"][nm]["total"])
        same("Ask A %s machines" % nm, half_up(m), F["ask_a"][nm]["machines"])
        same("Ask A %s app" % nm, half_up(a), F["ask_a"][nm]["app"])

    # ---------------------------------------------------------------------------- Ask B
    inv = rows_csv(P(find(r"levy_invoices")))
    owner = {i["invoice_no"]: i["customer"] for i in inv}
    due = defaultdict(float)
    for i in inv:
        due[i["customer"]] += float(i["amount_gbp"])
    advice = defaultdict(list)
    for r in rows_csv(P(find(r"remittance"))):
        advice[r["advice_ref"]].append(r)
    by_inv_date = {}
    for ref, lines in advice.items():
        for ln in lines:
            by_inv_date[(ln["invoice_no"], ln["payment_date"])] = lines
    paid = defaultdict(float)
    for r in rows_csv(P(find(r"bank_receipts"))):
        m = re.search(r"INV2\d-\d{4}", r["Reference"])
        if not m or m.group(0) not in owner:
            continue
        vd = dt.datetime.strptime(r["Value date"], "%d/%m/%Y").date()
        if vd > dt.date(2026, 3, 31):
            continue
        amt = float(r["Amount"])
        lines = by_inv_date.get((m.group(0), vd.isoformat()))
        if lines and len(lines) > 1 and abs(sum(float(x["amount_gbp"]) for x in lines) - amt) < .005:
            for x in lines:
                paid[owner[x["invoice_no"]]] += float(x["amount_gbp"])
        else:
            paid[owner[m.group(0)]] += amt
    for c in due:
        same("Ask B %s paid" % c, half_up(paid[c]), F["ask_b"][c]["paid"])
        same("Ask B %s owed" % c, half_up(due[c] - paid[c]), F["ask_b"][c]["owed"])

    # ---------------------------------------------------------------------------- Ask C, devices found in the data
    counts = defaultdict(dict)
    for r in rows_csv(P(find(r"counts_hourly"))):
        counts[r["counter_id"]][dt.datetime.strptime(r["hour_start_utc"], "%Y-%m-%d %H:%M")] = int(r["vehicles"])
    # paying vehicles per car park and local day from the machines (placed where each machine stood) and the app's
    # monthly sessions spread nowhere: the machines alone give the daily shape each counter should follow
    paying = defaultdict(Counter)
    for mid, day, amt in tickets:
        cp = reg_site[mid]
        if mid in stood and day <= stood[mid][0]:
            cp = [a["site_code"] for a in assets if a["asset_id"] != mid and a["site_code"][:2] == stood[mid][1]][0]
        paying[cp][day] += 1

    def daily(cid):
        out = Counter()
        for h, n in counts[cid].items():
            out[h.replace(tzinfo=dt.timezone.utc).astimezone(LONDON).date()] += n
        return out

    def corr(a, b, days):
        xs = [a[d] for d in days]
        ys = [b[d] for d in days]
        mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        sxx = sum((x - mx) ** 2 for x in xs) ** .5
        syy = sum((y - my) ** 2 for y in ys) ** .5
        return sxy / (sxx * syy)

    # the register's install and removal dates split the year into periods; in each, a counter is placed at the car
    # park whose daily machine payments its daily counts follow (a counter moved and re-registered changes car park)
    cuts = sorted({dt.date.fromisoformat(a[k]) for a in assets if a["asset_type"] == "Vehicle counter"
                   for k in ("installed", "removed") if a[k] and a[k] >= "2025-04-01"})
    edges = [dt.date(2025, 4, 1)] + cuts + [dt.date(2026, 4, 1)]
    cps = sorted(paying)
    site_day = {}
    for cid in counts:
        dl = daily(cid)
        for lo, hi in zip(edges, edges[1:]):
            md = [d for d in sorted(dl) if lo <= d < hi and dl[d] > 0]
            if len(md) < 10:
                for d in md:
                    site_day[(cid, d)] = reg_site[cid]
                continue
            best = max(cps, key=lambda cp: corr(dl, paying[cp], md))
            for d in md:
                site_day[(cid, d)] = best
    # a counter whose counts per paying vehicle run far above those of the counter it replaced at the same car park
    # counts every pass, in and out
    ratio = {}
    for cid in counts:
        dl = daily(cid)
        ds = [d for d in dl if (cid, d) in site_day]
        ratio[cid] = (sum(dl[d] for d in ds) / sum(paying[site_day[(cid, d)]][d] for d in ds),
                      Counter(site_day[(cid, d)] for d in ds).most_common(1)[0][0])
    halve = set()
    for cid, (r, cp) in ratio.items():
        others = [r2 for c2, (r2, cp2) in ratio.items() if c2 != cid and cp2 == cp]
        if others and r > 1.6 * min(others):
            halve.add(cid)
    # two counters giving the same count at the same car park in the same hour read one entrance twice
    vehicles = Counter()
    taken = {}
    for cid in sorted(counts):
        for h, n in sorted(counts[cid].items()):
            d = h.replace(tzinfo=dt.timezone.utc).astimezone(LONDON).date()
            cp = site_day.get((cid, d), reg_site[cid])
            if n > 0 and taken.get((cp, h)) == n:
                continue
            if n > 0:
                taken[(cp, h)] = n
            vehicles[cp[:2]] += n / 2 if cid in halve else n
    for p, nm in park_name.items():
        same("Ask C %s" % nm, vehicles[p], F["ask_c"][nm])
    moved = sorted({(cid, site_day[(cid, d)]) for (cid, d) in site_day if site_day[(cid, d)] != reg_site[cid]})
    if FAIL:
        print("verify: %d mismatches" % len(FAIL))
        for x in FAIL:
            print("  " + x)
        sys.exit(1)
    print("verify: call, rungs and every ask figure agree with figures.json (counters halved %s, counters placed "
          "off their register site %s, machines moved %s)" % (sorted(halve), moved,
                                                               {m: (str(v[0]), v[1]) for m, v in stood.items()}))


if __name__ == "__main__":
    main(sys.argv[1])
