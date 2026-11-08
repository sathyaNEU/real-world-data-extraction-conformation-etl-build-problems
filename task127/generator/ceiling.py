"""task127: the ask layer's cracker and mirror sheets measured on the cut pack (supplemental-stumping 1.1, Part 0).

The cracker landed the call, ran the hygiene battery and executed every filed rule (the index's latest published
value per quarter, title references normalised, the validation report's default definition: first trigger, in default
until the cure). The mirror stopped at the default path's own-ECL call and at each ask's lazy stop. The after-notice
rows model a response that finds one device and handles it fully. Every route reads target/ only."""
import hashlib
import json
import math
import os
import re
import subprocess
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD  # noqa: E402

T = os.path.join(os.path.dirname(HERE), "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))


def r_half(x, u):
    return int(math.floor(x / u + 0.5)) * u


def digest():
    h = hashlib.md5()
    for f in sorted(os.listdir(T)):
        h.update(f.encode())
        h.update(open(os.path.join(T, f), "rb").read())
    return h.hexdigest()


wl = subprocess.run(["pdftotext", "-layout", os.path.join(T, "watch_list_2027-01.pdf"), "-"],
                    capture_output=True, text=True).stdout
LINES = {}
for ln in wl.splitlines():
    m = re.match(r"\s*(C\d{6})\s", ln)
    amts = re.findall(r"\d{1,3}(?:,\d{3})+", ln)
    if m and len(amts) >= 2:
        LINES[m.group(1)] = float(amts[-1].replace(",", ""))
wb = openpyxl.load_workbook(os.path.join(T, "customer_master_2026-12.xlsx"), read_only=True)
NAME = {r[0]: r[1].replace(" Limited", "") for r in list(wb["Customers"].iter_rows(values_only=True))[1:]}
P = GD.Pack(T, LINES)

gold_A = FIG["security"]
gold_B = FIG["commitment"]
gold_C = {k.split(" ")[0]: v for k, v in FIG["sector_share"].items()}


def score_money(route, gold):
    return {NAME[c]: (r_half(v, 1000), r_half(v, 1000) == gold[NAME[c]]) for c, v in route.items()}


def score_share(route):
    return {s: (round(v[0], 1), round(v[0], 1) == gold_C[s]) for s, v in route.items()}


ROUTES = {
    "cracker": {
        "A": score_money(P.security(use_made=False, drop_discharged=False), gold_A),
        "B": score_money(P.commitment(former=False, drop_released=False), gold_B),
        "C": score_share(P.sector_table(use_register=True, use_cures=True, keys="noloan")),
    },
    "mirror": {
        "A": score_money(P.security(use_made=False, drop_discharged=False), gold_A),
        "B": score_money(P.commitment(former=False, drop_released=False), gold_B),
        "C": score_share(P.sector_table(use_register=False, use_cures=False, keys="noloan")),
    },
    "after notice A1 (made dates found, discharges not)": {
        "A": score_money(P.security(use_made=True, drop_discharged=False), gold_A)},
    "after notice A2 (discharges found, register dates kept)": {
        "A": score_money(P.security(use_made=False, drop_discharged=True), gold_A)},
    "after notice B1 (former names linked, releases not)": {
        "B": score_money(P.commitment(former=True, drop_released=False), gold_B)},
    "after notice B2 (releases found, exact names only)": {
        "B": score_money(P.commitment(former=False, drop_released=True), gold_B)},
    "after notice C (loan accounts resolved through the ledger)": {
        "C": score_share(P.sector_table(use_register=True, use_cures=True, keys="all"))},
    "C, UTP rows only (every account-keyed row dropped)": {
        "C": score_share(P.sector_table(use_register=True, use_cures=True, keys="utp"))},
}
N_ASK = len(gold_A) + len(gold_B) + len(gold_C)
empty = [a for a, g in (("A", gold_A), ("B", gold_B), ("C", gold_C)) if not g]
unscored = [n for n, asks in ROUTES.items() for a, rows in asks.items() if not rows]
if empty or unscored or len(LINES) != 8:
    print("ceiling: REFUSED, nothing to measure: golden asks with no figures %s; routes that scored no row %s; watch-list "
          "lines read %d" % (empty, unscored, len(LINES)))
    sys.exit(2)

print("pack md5 %s  (%d files)" % (digest(), len(os.listdir(T))))
print("ask figures graded: A %d, B %d, C %d = %d" % (len(gold_A), len(gold_B), len(gold_C), N_ASK))
kept = {}
for name, asks in ROUTES.items():
    k = 0
    parts = []
    for a, rows in asks.items():
        hit = sum(1 for _, h in rows.values() if h)
        k += hit
        parts.append("%s %d of %d" % (a, hit, len(rows)))
    kept[name] = k
    print("%-62s %s" % (name, ", ".join(parts)))
    if name in ("cracker", "mirror"):
        for a, rows in asks.items():
            print("    %s: %s" % (a, "; ".join("%s %s%s" % (key, v, "" if h else " (miss)") for key, (v, h) in rows.items())))

own = P.best_set({c: P.own(c) for c in LINES})[0]
mirror_on_call = sorted(own) == sorted(FIG["call_ids"])
Lc = kept["cracker"] / N_ASK
Ls = kept["mirror"] / N_ASK
C = 38 + 7 + 55 * Lc
S = (38 if mirror_on_call else 5) + 7 + 55 * Ls
print("mirror's call (own ECL only): %s, %s the golden" % (" and ".join(sorted(NAME[c] for c in own)),
                                                         "equals" if mirror_on_call else "misses"))
print("Cracker keeps %d of %d ask figures (%.1f per cent): %.1f" % (kept["cracker"], N_ASK, 100 * Lc, C))
print("Mirror keeps %d of %d ask figures (%.1f per cent): %.1f" % (kept["mirror"], N_ASK, 100 * Ls, S))
print("Mirror leakage: %.1f per cent of ask weight" % (100 * Ls))
print("Pair ceiling: %.1f" % ((C + S) / 2))
worst = max(v for k, v in kept.items() if k.startswith("after notice"))
print("Largest single after-notice keep: %d of %d (%.1f per cent of ask weight)" % (worst, N_ASK, 100 * worst / N_ASK))
bad = []
if kept["cracker"]:
    bad.append("cracker keeps an ask figure")
if any(all(h for _, h in rows.values()) for rows in ROUTES["mirror"].values()):
    bad.append("mirror keeps an ask whole")
if Ls >= 0.4:
    bad.append("mirror leakage at or over two fifths")
if (C + S) / 2 >= 60:
    bad.append("pair ceiling at or over 60")
print("ceiling: %s" % ("PASS" if not bad else "FAIL " + "; ".join(bad)))
sys.exit(1 if bad else 0)
