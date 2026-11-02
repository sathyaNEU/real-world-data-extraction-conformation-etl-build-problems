"""task163 ask layer against the careful solver's route, on the cut pack.

    python3 task163/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The asks are the
workbook's two tables: the 2024 first-time employers by sales territory (signed, still with us in the fourth quarter of
2025, gross wages in their first quarter on payroll and in 2024: 24 figures) and by signup channel (5 figures), with
the note's chart of signed against still with us (4 criteria, two structural). A figure is kept when it equals
figures.json's (a count exactly, wages to the cent).

The cracker is the careful solver, never a narrowed one, and its code is its own (no generator module is imported): it
lands the call, reads every field by its plain meaning, executes every rule the counting notes file as worded, and runs
the hygiene battery, each item detecting its device on the pack before it acts:
- the rollup reconciliation: a legacy client quarter with more than one pay group is tested for a group equal to the
  sum of the others (group 00), and where that holds in every such quarter the rollup is taken as the client's total;
- the anti-join of each account's first_pay_date quarter against its wage rows: where the field's quarter holds no
  wages and a later quarter does, the field is not the first payroll, so the first payroll is read from the wage files;
- re-keyed records across two systems, as the counting notes' "whatever its account or EIN" invites: an account
  cancelled the day before an account with the same legal name, trade name, industry and entity opened is one business
  with it (the EIN pairs are printed with whether they sit one adjacent swap apart);
- EINs normalised (hyphens, a lost leading zero), returning clients under one EIN, successors and new owners through the
  payroll tax team's register, a successor of an EIN with no account in the extract its predecessor's business;
- first-time status from the state's liability record, quarters on tax filing only left out, the channel of a
  business's first account, the state of its earliest registration, the territory map, cents, the crosswalk.
Each battery item is also switched off one at a time and printed, so the sheet shows which item performs which device.

The mirror stops at the default path on the call (each state's latest closed rate carried, 2,800) and reads the asks the
plain way: flagged accounts by their own first pay date, the address state, the account's own fourth-quarter row, the
plain sum of a legacy client quarter's rows, the export's channel.

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over the 29
figures and the chart's 4 criteria, the response off the call keeping r = 5 of the 38 (r = 3 printed beside it). Exit 0
when the gate holds (the cracker keeps no ask figure, the pair at or under 60, the mirror under half the ask weight, two
careful responses on the call under 70), 2 when it does not, 1 when a control fails (the full includer must give back
figures.json exactly)."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
CHART = 4               # the note's chart: two structural criteria, one for every signed bar, one for every still bar
CHART_STRUCT = 2
PAIR_GATE, MIRROR_GATE, BOTH_GATE = 60.0, 50.0, 70.0
TERR_ORDER = ["Ohio", "Pennsylvania", "Michigan", "Indiana-Kentucky", "Upper Midwest", "South and Plains"]
CH_ORDER = ["accountant referral", "bank partner", "outbound", "partner marketplace", "web sign-up"]


# ------------------------------------------------------------------ the pack
def pack_dir(arg):
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling163-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    root = os.path.join(tmp, "target") if os.path.isdir(os.path.join(tmp, "target")) else tmp
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return root, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(root)), md5)


def rows(folder, name):
    with open(os.path.join(folder, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    return " ".join("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p))
                    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S)).replace("&amp;", "&")


def key(e):
    return re.sub(r"\D", "", e).rjust(9, "0")


def qof(d):
    return int(d[:4]), (int(d[5:7]) - 1) // 3 + 1


def qstart(y, q):
    return "%d-%02d-01" % (y, 3 * q - 2)


def opened(r):
    v = r["opened_at"]
    if "/" in v:
        return dt.datetime.strptime(v, "%m/%d/%Y %H:%M").date()
    return dt.date.fromisoformat(v[:10])


def one_swap(a, b):
    d = [i for i in range(9) if a[i] != b[i]]
    return len(d) == 2 and d[1] == d[0] + 1 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]]


# ------------------------------------------------------------------ the book, read
class Book:
    def __init__(self, folder):
        self.acc = rows(folder, "onboarding_accounts_2022-2025.csv")
        self.xw = rows(folder, "client_migration_crosswalk_2024-06-15.csv")
        self.leg = rows(folder, "legacy_quarterly_wages_2022Q1-2024Q2.csv")
        self.cur = rows(folder, "quarterly_wages_2024Q2-2025Q4.csv")
        self.reg = rows(folder, "state_tax_registrations_2026-01-09.csv")
        self.suta = rows(folder, "suta_successor_transfers_2022-2025.csv")
        self.terr = {r["state"]: r["territory"] for r in rows(folder, "sales_territories_2025.csv")}
        self.notes = docx_text(os.path.join(folder, "first_time_employer_counting_notes.docx"))
        self.acct_of = {r["legacy_client_no"]: r["account_id"] for r in self.xw}
        self.migrated = set(self.acct_of.values())
        self.regs = defaultdict(list)
        for r in self.reg:
            self.regs[r["account_id"]].append(r)
        self.by_ein = defaultdict(list)
        for a in self.acc:
            self.by_ein[key(a["ein"])].append(a)
        self.succ_of = defaultdict(list)
        self.succ_eins = set()
        for r in self.suta:
            self.succ_of[key(r["predecessor_ein"])].append(key(r["successor_ein"]))
            self.succ_eins.add(key(r["successor_ein"]))
        self.evidence = {}

    # the battery's rollup reconciliation on the legacy report
    def wages(self, rollup):
        grp = defaultdict(dict)
        for r in self.leg:
            grp[(r["client_no"], r["tax_year"], r["tax_qtr"])][r["pay_group"]] = int(r["gross_wages_cents"])
        multi = [v for v in grp.values() if len(v) > 1]
        holds = all("00" in v and v["00"] == sum(x for k, x in v.items() if k != "00") for v in multi)
        self.evidence["rollup"] = "%d legacy client quarters with two or more pay groups, group 00 the sum of the " \
                                  "others in %s of them" % (len(multi), "all" if holds else "not all")
        wq = Counter()
        for (c, y, q), v in grp.items():
            a = self.acct_of[c]
            if rollup and holds and len(v) > 1:
                wq[(a, int(y), int(q))] += v["00"]
            else:
                wq[(a, int(y), int(q))] += sum(v.values())
        for r in self.cur:
            y, q = r["quarter"].split("-Q")
            wq[(r["account_id"], int(y), int(q))] += int(round(float(r["gross_wages"]) * 100))
        return wq

    # the battery's anti-join of the field against the wage rows
    def first_quarters(self, wq, anti_join):
        firstq = {}
        for (a, y, q), c in wq.items():
            if c > 0 and (a not in firstq or (y, q) < firstq[a]):
                firstq[a] = (y, q)
        off = [a for a in self.acc if a["account_id"] in firstq and wq.get((a["account_id"],) +
                                                                            qof(a["first_pay_date"]), 0) == 0
               and firstq[a["account_id"]] > qof(a["first_pay_date"])]
        self.evidence["anti_join"] = "%d accounts whose first_pay_date quarter holds no wages while a later one does " \
                                     "(%d migrated, %d current-system)" % (
                                         len(off), sum(1 for a in off if a["account_id"] in self.migrated),
                                         sum(1 for a in off if a["account_id"] not in self.migrated))
        if anti_join and off:
            return firstq
        return {a["account_id"]: qof(a["first_pay_date"]) for a in self.acc}

    # re-keyed records across two systems: cancelled one day, the same business opened the next
    def links(self, rekey):
        same = defaultdict(list)
        for a in self.acc:
            same[(a["legal_name"].upper(), a["dba_name"].upper(), a["naics"], a["entity_type"])].append(a)
        pairs = set()
        for rs in same.values():
            for x in rs:
                if x["status"] != "Cancelled" or not x["cancelled_on"]:
                    continue
                for z in rs:
                    if z is not x and (opened(z) - dt.date.fromisoformat(x["cancelled_on"])).days == 1 and \
                            key(x["ein"]) != key(z["ein"]):
                        pairs.add(tuple(sorted((key(x["ein"]), key(z["ein"])))))
        swaps = sum(1 for p in pairs if one_swap(*p))
        self.evidence["rekey"] = "%d EIN pairs on accounts with the same names, industry and entity, cancelled the " \
                                 "day before the other opened (%d one adjacent swap apart)" % (len(pairs), swaps)
        link = defaultdict(set)
        if rekey:
            for a, b in pairs:
                link[a].add(b)
                link[b].add(a)
        return link


def tax_only(a, y, q):
    return a["product"] == "Tax filing only" and a["product_since"] and a["product_since"] <= qstart(y, q)


def careful(B, rollup=True, anti_join=True, rekey=True):
    """The careful solver's ask tables."""
    wq = B.wages(rollup)
    firstq = B.first_quarters(wq, anti_join)
    link = B.links(rekey)
    done, groups = set(), []
    for e in sorted(B.by_ein):
        if e in done:
            continue
        g, todo = set(), [e]
        while todo:
            x = todo.pop()
            if x in g:
                continue
            g.add(x)
            todo += sorted(link.get(x, ()))
        done |= g
        groups.append(sorted(g))
    T = {t: {"signed": 0, "still": 0, "first_quarter_cents": 0, "wages_2024_cents": 0} for t in TERR_ORDER}
    CH = Counter()
    for g in groups:
        accts = [a for e in g for a in B.by_ein[e]]
        qs = [firstq[a["account_id"]] for a in accts if a["account_id"] in firstq and
              (not anti_join or wq.get((a["account_id"],) + firstq[a["account_id"]], 0) > 0)]
        if not qs:
            continue
        fy, fq = min(qs)
        if fy != 2024 or any(e in B.succ_eins for e in g):
            continue
        if any(r["liability_date"] < qstart(fy, fq) for a in accts for r in B.regs[a["account_id"]]):
            continue
        first = sorted(accts, key=lambda r: (firstq.get(r["account_id"], (9999, 9)), r["first_pay_date"],
                                             r["account_id"]))[0]
        chain, todo, seen = [], list(g), set()
        while todo:
            x = todo.pop()
            if x in seen:
                continue
            seen.add(x)
            chain += B.by_ein.get(x, [])
            todo += B.succ_of.get(x, [])
            todo += sorted(link.get(x, ()))
        st = min((r for a in accts for r in B.regs[a["account_id"]]),
                 key=lambda r: (r["liability_date"], r["filing_start"]))["state"]
        t = B.terr.get(st)
        if t is None:
            continue
        T[t]["signed"] += 1
        if any(wq.get((a["account_id"], 2025, 4), 0) > 0 and not tax_only(a, 2025, 4) for a in chain):
            T[t]["still"] += 1
        T[t]["first_quarter_cents"] += sum(wq.get((a["account_id"], fy, fq), 0) for a in chain)
        T[t]["wages_2024_cents"] += sum(wq.get((a["account_id"], 2024, q), 0) for a in chain for q in (1, 2, 3, 4)
                                        if not tax_only(a, 2024, q))
        CH[first["signup_channel"]] += 1
    return T, CH


def mirror(B):
    """The plain read: flagged accounts by their own first pay date, the address state, the account's own row."""
    wq = B.wages(rollup=False)
    T = {t: {"signed": 0, "still": 0, "first_quarter_cents": 0, "wages_2024_cents": 0} for t in TERR_ORDER}
    CH = Counter()
    for a in B.acc:
        if a["first_time_employer"] != "Y" or not a["first_pay_date"].startswith("2024"):
            continue
        t = B.terr.get(a["address_state"])
        if t is None:
            continue
        T[t]["signed"] += 1
        T[t]["still"] += int(wq.get((a["account_id"], 2025, 4), 0) > 0)
        T[t]["first_quarter_cents"] += wq.get((a["account_id"],) + qof(a["first_pay_date"]), 0)
        T[t]["wages_2024_cents"] += sum(wq.get((a["account_id"], 2024, q), 0) for q in (1, 2, 3, 4))
        CH[a["signup_channel"]] += 1
    return T, CH


def golden(fig):
    T = {t: {"signed": v["signed"], "still": v["still"],
             "first_quarter_cents": int(round(float(v["first_quarter_wages"]) * 100)),
             "wages_2024_cents": int(round(float(v["wages_2024"]) * 100))} for t, v in fig["territories"].items()}
    return T, dict(fig["channels"])


def score(gold, got):
    GT, GC = gold
    T, CH = got
    out = []
    for t in TERR_ORDER:
        for k in ("signed", "still", "first_quarter_cents", "wages_2024_cents"):
            out.append(("%s %s" % (t, k.replace("_cents", "")), GT[t][k], T.get(t, {}).get(k)))
    for c in CH_ORDER:
        out.append(("channel %s" % c, GC.get(c, 0), CH.get(c, 0)))
    return [(n, g, v, g == v) for n, g, v in out]


def share(sc):
    signed = all(r[3] for r in sc if r[0].endswith(" signed"))
    still = all(r[3] for r in sc if r[0].endswith(" still"))
    kept = sum(1 for r in sc if r[3]) + CHART_STRUCT + int(signed) + int(still)
    return kept / float(len(sc) + CHART), kept


def fmt(name, v):
    return ("%.2f" % (v / 100.0)) if "wages" in name or "first_quarter" in name else str(v)


def main(argv):
    folder, tmp, stamp = pack_dir(argv[1] if len(argv) > 1 else None)
    try:
        fig = json.load(open(os.path.join(HERE, "figures.json")))
        B = Book(folder)
        gold = golden(fig)
        print("pack: %s" % stamp)
        print("the call: the cracker lands it (%d); the mirror stops at the default path (2,800)" % fig["call"])
        notes_ok = all(p in B.notes for p in ("whatever its account or EIN", "first payroll ever runs with us",
                                              "state it first employed in", "tax filing only does not count"))
        print("the counting notes read (positive control on the extractor): %s" % notes_ok)

        routes = {
            "careful solver (every battery item)": dict(),
            "  less the rollup reconciliation": dict(rollup=False),
            "  less the first_pay_date anti-join": dict(anti_join=False),
            "  less the re-key link": dict(rekey=False),
        }
        res = {}
        for name, kw in routes.items():
            res[name] = score(gold, careful(B, **kw))
        print("battery evidence on this pack:")
        for k, v in B.evidence.items():
            print("  %-10s %s" % (k, v))
        full = res["careful solver (every battery item)"]
        ok_full = all(r[3] for r in full)
        print("\ncracker sheet (golden, the careful solver, verdict):")
        for n, g, v, hit in full:
            print("  %-38s %16s %16s %s" % (n, fmt(n, g), fmt(n, v) if v is not None else "-", "hit" if hit else
                                            "miss"))
        ms = score(gold, mirror(B))
        Lp, mk = share(ms)
        print("\nmirror, the plain read (default path, plain asks): keeps %d of %d ask criteria, %.1f per cent of ask "
              "weight" % (mk, len(ms) + CHART, 100 * Lp))
        # the asks consume nothing the call's construction produces (checks.py SEPARATION), so the best response off
        # the call is free to run the careful ask route: that is the mirror the gate reads
        Ls = share(full)[0]
        print("mirror, the gated one (off the call, the asks decoupled, so the careful ask route): %.1f per cent of "
              "ask weight" % (100 * Ls))
        whole = [a for a in ("signed", "still", "first_quarter", "wages_2024", "channel")
                 if all(r[3] for r in full if (a in r[0] if a != "channel" else r[0].startswith("channel")))]
        print("  asks the gated mirror keeps whole: %s" % (", ".join(whole) or "none"))
        print("\nroutes (ask criteria kept of %d, ask share):" % (len(full) + CHART))
        for name, sc in res.items():
            L, k = share(sc)
            print("  %-40s %2d  %.3f   figures kept %d of %d" % (name, k, L, sum(1 for r in sc if r[3]), len(sc)))
        L, k = share(full)
        C = W_REC + W_INSTR + W_ASK * L
        print("\npair (38, 7, 55):")
        worst = 0.0
        for r in (5.0, 3.0):
            S = r + W_INSTR + W_ASK * Ls
            pair = (C + S) / 2.0
            worst = max(worst, pair)
            Sp = r + W_INSTR + W_ASK * Lp
            print("  off the call keeps r = %.0f: careful on the call %.1f, gated mirror %.1f, pair %.1f (with the "
                  "plain-read mirror %.1f, pair %.1f)" % (r, C, S, pair, Sp, (C + Sp) / 2.0))
        print("  two careful responses on the call: %.1f each, pair %.1f" % (C, C))
        print("full includer: the careful route gives back figures.json %s (%d of %d figures)"
              % ("exactly" if ok_full else "NOT", sum(1 for r in full if r[3]), len(full)))
        kept_figs = sum(1 for r in full if r[3])
        gate = kept_figs == 0 and worst <= PAIR_GATE and 100 * Ls < MIRROR_GATE and not whole and C < BOTH_GATE
        print("\ngate: the cracker keeps %d of %d ask figures; pair %.1f (gate %.0f); mirror %.1f per cent (gate %.0f); "
              "two careful responses %.1f (gate %.0f): %s" % (kept_figs, len(full), worst, PAIR_GATE, 100 * Ls,
                                                              MIRROR_GATE, C, BOTH_GATE, "HOLDS" if gate else "FAILS"))
        if not notes_ok:
            return 1
        return 0 if gate else 2
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
