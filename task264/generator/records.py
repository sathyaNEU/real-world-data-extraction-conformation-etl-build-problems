"""The feeds and registers as the firm's systems hold them: the movement table and the store sales table as loaded
(every load kept, the delivery log saying which stands), the panel store register, the item master, the partner
register's chain and code lists, the feed delivery log, the retail calendar and the two files the team keeps beside
them that the index does not use."""
from __future__ import annotations

import csv
import datetime as dt

import numpy as np

import common as K
import world as W

FMT_DATE = "%Y-%m-%d"


def wk(t):
    return K.WEEKS[t]


# ---------------------------------------------------------------------------------------------- loads
def plan_loads(T):
    """Every load the firm received for retail year 2026: movement and store sales, one a chain a week, plus the
    July chain's onboarding store sales, a chain's resubmitted movement block and a chain's store sales resend.
    Returns a list of dicts in order of receipt, with load ids issued in that order."""
    loads = []
    r = K.rng("loads")
    for t in range(K.W):
        for c in K.CHAIN_CODES:
            ch = K.CH[c]
            if t < ch["start"]:
                continue
            end = wk(t) + dt.timedelta(days=1 if c == K.SUNDAY_CHAIN else 0)
            for feed in ("movement", "store sales"):
                lag_days = 2 + (1 if c == K.SUNDAY_CHAIN else 0) + int(r.integers(0, 2))
                when = dt.datetime.combine(end + dt.timedelta(days=lag_days), dt.time(0, 0)) + dt.timedelta(
                    minutes=int(r.integers(-600, 360)))
                weeks = (t, t)
                if feed == "store sales" and c == "S5" and t == ch["start"]:
                    weeks = (K.BACKFILL_FROM, t)
                status = "accepted"
                note = ""
                if feed == "movement" and c == K.RESUB_CHAIN and t in K.RESUB_WEEKS:
                    status = "superseded"
                if feed == "store sales" and c == "S5" and t == ch["start"]:
                    note = "first delivery under the data agreement"
                loads.append(dict(chain=c, feed=feed, weeks=weeks, received=when, status=status, note=note))
    # the resubmitted movement block: one store's rows were missing from the original weekly loads
    a, b = K.RESUB_WEEKS[0], K.RESUB_WEEKS[-1]
    loads.append(dict(chain=K.RESUB_CHAIN, feed="movement", weeks=(a, b), status="accepted",
                      received=dt.datetime.combine(wk(b) + dt.timedelta(days=18), dt.time(4, 41)),
                      note="resubmission of the weeks ending %s to %s; replaces the four weekly loads" % (
                          wk(a).strftime("%-d %B"), wk(b).strftime("%-d %B %Y"))))
    # the store sales resend the firm's validation turned back
    a, b = K.RESEND_WEEKS[0], K.RESEND_WEEKS[-1]
    loads.append(dict(chain=K.RESEND_CHAIN, feed="store sales", weeks=(a, b), status="rejected",
                      received=dt.datetime.combine(wk(b) + dt.timedelta(days=11), dt.time(22, 17)),
                      note="resend of the weeks ending %s to %s failed validation (store totals out of range "
                           "against the movement feed); original loads stand" % (
                               wk(a).strftime("%-d %B"), wk(b).strftime("%-d %B %Y"))))
    loads.sort(key=lambda x: (x["received"], x["chain"], x["feed"]))
    n = 2408113
    for x in loads:
        n += int(r.integers(1, 4))
        x["load_id"] = str(n)
    return loads


# ---------------------------------------------------------------------------------------------- the movement table
def promo_codes(T):
    """The till's code on each movement row: the chain's catalogue special code, its markdown code, or a price check
    override (the upgrade chain, from its till upgrade); blank for a sale at the shelf price."""
    out = []
    for x in T["sold"]:
        c = x["chain"]
        ch = K.CH[c]
        code = np.full(x["units"].shape, "", dtype=object)
        if ch["md_code"]:
            code[x["mdflag"]] = ch["md_code"]
        if c == K.UPGRADE_CHAIN:
            code[x["check"]] = "PC"
            pre = np.zeros(x["units"].shape, bool)
            pre[:, :K.UPGRADE_T] = True
            code[x["promo"] & pre] = "PC"
            code[x["promo"] & ~pre] = "TPR"
        else:
            code[x["promo"]] = ch["promo_code"]
        out.append(code)
    return out


def movement_rows(T, loads):
    """Rows as loaded: (load_id, store_id, item_code, week_ending, units, sales_aud, promo_code). The resubmitted
    block's original weekly loads lack one store; the resubmission carries every store."""
    items = T["items"]
    kg = np.array([it["kg"] for it in items])
    codes = promo_codes(T)
    by_chain_week = {}
    for x, code in zip(T["sold"], codes):
        i_idx, t_idx = np.nonzero(x["units"] > 0)
        for i, t in zip(i_idx, t_idx):
            by_chain_week.setdefault((x["chain"], int(t)), []).append(
                (x["code"], items[i]["code"], float(x["units"][i, t]), float(x["dollars"][i, t]), code[i, t], kg[i]))
    resub_store = sorted({x["code"] for x in T["sold"] if x["chain"] == K.RESUB_CHAIN and
                          all(x["units"][:, t].sum() > 0 for t in K.RESUB_WEEKS)})[1]
    rows = []
    resub = [x for x in loads if x["chain"] == K.RESUB_CHAIN and x["feed"] == "movement" and
             x["weeks"][0] != x["weeks"][1]][0]
    for x in loads:
        if x["feed"] != "movement":
            continue
        c = x["chain"]
        for t in range(x["weeks"][0], x["weeks"][1] + 1):
            for store, item, u, d, pc, isk in by_chain_week.get((c, t), []):
                if x["status"] == "superseded" and store == resub_store:
                    continue
                if c == K.ZERO_DROP_CHAIN:
                    item = item[1:]
                rows.append((x["load_id"], store, item, wk(t).strftime(FMT_DATE),
                             ("%.3f" % u) if isk else "%d" % int(round(u)), "%.2f" % d, pc))
    return rows, resub_store, resub["load_id"]


def write_movement(path, T, loads, per_load):
    rows, resub_store, resub_id = movement_rows(T, loads)
    for row in rows:
        per_load[row[0]] = per_load.get(row[0], 0) + 1
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["load_id", "store_id", "item_code", "week_ending", "units", "sales_aud", "promo_code"])
        w.writerows(rows)
    return len(rows), resub_store, resub_id


# ---------------------------------------------------------------------------------------------- store sales
def store_sales_rows(T, loads):
    rows = []
    tk = {x["code"]: x for x in T["takings"]}
    codes_by_chain = {}
    for x in T["codes"]:
        codes_by_chain.setdefault(x["chain"], []).append(x["code"])
    live = [x["code"] for x in T["codes"] if x["chain"] == K.RESEND_CHAIN and x["first"] <= K.RESEND_WEEKS[0] and
            x["last"] >= K.RESEND_WEEKS[-1]]
    doubled = set(sorted(live)[1:3])
    for x in loads:
        if x["feed"] != "store sales":
            continue
        c = x["chain"]
        for t in range(x["weeks"][0], x["weeks"][1] + 1):
            day = wk(t) + dt.timedelta(days=1 if c == K.SUNDAY_CHAIN else 0)
            for code in sorted(codes_by_chain[c]):
                y = tk[code]
                hit = np.nonzero(y["weeks"] == t)[0]
                if not len(hit):
                    continue
                k = int(hit[0])
                vals = y["values"][k]
                total = round(float(vals.sum()), 2)
                for j, (dcode, dname, _) in enumerate(y["depts"]):
                    v = float(vals[j])
                    if c in K.VENDOR_CHAINS:
                        v = total
                    if x["status"] == "rejected" and code in doubled:
                        v = round(2 * v, 2)
                    rows.append((x["load_id"], code, day.strftime(FMT_DATE), dcode, dname, "%.2f" % v))
    return rows, sorted(doubled)


def write_store_sales(path, T, loads, per_load):
    rows, doubled = store_sales_rows(T, loads)
    for row in rows:
        per_load[row[0]] = per_load.get(row[0], 0) + 1
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["load_id", "store_id", "week_ending", "dept_code", "dept_name", "sales_aud"])
        w.writerows(rows)
    return len(rows), doubled


# ---------------------------------------------------------------------------------------------- registers
def store_names(T):
    """The trading name the chain gives each site, kept through a re-code."""
    names = {}
    seen = {}
    for s in T["sites"]:
        ch = K.CH[s["chain"]]
        base = "%s %s%s" % (ch["banner"], W.LOCAL_NAMES[s["fmt"]], s["suburb"])
        k = seen.get(base, 0)
        seen[base] = k + 1
        names[s["site"]] = base if k == 0 else "%s %s" % (base, ["North", "Central", "Plaza"][k - 1])
    return names


def panel_from(T):
    """Each chain's first panel week before the window (its data agreement), drawn once a chain."""
    out = {}
    for c in K.CHAIN_CODES:
        r = K.rng("agreement", c)
        if K.CH[c]["start"] > 0:
            out[c] = wk(K.CH[c]["start"])
        else:
            out[c] = K.WEEK1 - dt.timedelta(days=7 * int(r.integers(60, 420)))
    return out


def write_register(path, T):
    names = store_names(T)
    site_by = {s["site"]: s for s in T["sites"]}
    pf = panel_from(T)
    rows = []
    for x in sorted(T["codes"], key=lambda x: x["code"]):
        s = site_by[x["site"]]
        if x["first"] == 0:
            first = pf[x["chain"]]
            r = K.rng("joined", x["code"])
            first = max(first, K.WEEK1 - dt.timedelta(days=7 * int(r.integers(0, 260))))
            first = first + dt.timedelta(days=(5 - first.weekday()) % 7)
        else:
            first = wk(x["first"])
        last = "" if x["last"] == K.W - 1 else wk(x["last"]).strftime(FMT_DATE)
        rows.append((x["code"], x["chain"], x["fmt"], names[s["site"]], s["suburb"], s["state"], s["postcode"],
                     first.strftime(FMT_DATE), last))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["store_id", "chain_code", "format", "store_name", "suburb", "state", "postcode",
                    "first_week_ending", "last_week_ending"])
        w.writerows(rows)
    return len(rows)


def write_items(path, T):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["item_code", "description", "category_code", "category", "unit_of_sale"])
        for it in sorted(T["items"], key=lambda it: (K.CAT_CODE[it["cat"]], it["code"])):
            w.writerow([it["code"], it["desc"], K.CAT_CODE[it["cat"]], it["cat"], "kg" if it["kg"] else "each"])
    return len(T["items"])


def write_log(path, loads, counts):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["load_id", "chain_code", "feed", "first_week_ending", "last_week_ending", "received_utc",
                    "rows", "status", "note"])
        for x in loads:
            day = 1 if x["chain"] == K.SUNDAY_CHAIN and x["feed"] == "store sales" else 0
            w.writerow([x["load_id"], x["chain"], x["feed"],
                        (wk(x["weeks"][0]) + dt.timedelta(days=day)).strftime(FMT_DATE),
                        (wk(x["weeks"][1]) + dt.timedelta(days=day)).strftime(FMT_DATE),
                        x["received"].strftime("%Y-%m-%dT%H:%M:%SZ"), counts.get(x["load_id"], 0),
                        x["status"], x["note"]])
    return len(loads)


def write_calendar(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["retail_year", "retail_week", "week_start", "week_ending", "retail_quarter"])
        start = dt.date(2024, 12, 1)            # retail year 2025 starts Sunday 1 December 2024
        for ry in (2025, 2026, 2027):
            for k in range(52):
                a = start + dt.timedelta(days=7 * k)
                w.writerow([ry, k + 1, a.strftime(FMT_DATE), (a + dt.timedelta(days=6)).strftime(FMT_DATE), k // 13 + 1])
            start = start + dt.timedelta(days=7 * 52)
    return 156


# ---------------------------------------------------------------------------------------------- the files beside them
def write_audit(path, T):
    """Price accuracy checks the firm's field team ran in 2025: the shelf label against the till at sampled stores."""
    r = K.rng("audit")
    items = T["items"]
    stores = [x for x in T["codes"] if x["first"] == 0 and x["fmt"] != "online"]
    rows = []
    day = dt.date(2025, 2, 4)
    while day < dt.date(2025, 11, 28):
        for _ in range(int(r.integers(3, 6))):
            st = stores[int(r.integers(0, len(stores)))]
            ch = K.CH[st["chain"]]
            for _ in range(int(r.integers(8, 15))):
                it = items[int(r.integers(0, len(items)))]
                if not W.ranged_at(it, st["chain"]):
                    continue
                shelf = float(W.price_point(it["base"] * ch["lvl"] * r.uniform(0.95, 0.99), st["chain"]))
                till = shelf if r.random() > 0.035 else round(shelf + float(r.choice([0.1, 0.2, 0.5, 1.0, -0.1])), 2)
                rows.append((day.strftime(FMT_DATE), st["code"], it["code"], "%.2f" % shelf, "%.2f" % till,
                             "Y" if abs(till - shelf) < 0.005 else "N"))
        day += dt.timedelta(days=int(r.integers(2, 5)))
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(["audit_date", "store_id", "item_code", "shelf_label_aud", "till_price_aud", "label_matches_till"])
        w.writerows(rows)
    return len(rows)
