"""task501 ask layer against the careful solver's routes, on the cut pack, read against the prompt as filed.

    python3 task501/generator/ceiling.py [target] [--prompt PATH]

Every route a careful reader takes on the three asks, figure by figure, against figures.json, read from the shipped
files only (bundle.ask_frames). Ask 1 (each option's people the register holds in the region at 30 June 2027): LH27
was reissued on 1 July 2024, so a code recorded before then is Monaghan West (D7, the circular finds it), and children
the school immunisation team did not find at school entry hold a second registration it opened, unmerged, the two
joined only by the GP card line loaded to both (Dn: a GP return line is one dose to one child). Ask 2 (no valid dose,
exactly one): GP return lines the query log shows replaced or withdrawn stay loaded, and merged registrations leave
their events on the retired number, some in a chain of two, counted per child for Ask 1's people. Ask 3 (confirmed and
imported cases): the 2019 outbreak's back-entries carry the migrated record's legacy number only in their comments,
and six illnesses were notified by both a GP and a hospital as two unlinked records.

Both responses read the prompt literally (the task's prompt.txt, or --prompt): what it files they apply, the people
counted by the region their address is in where it says the register holds them at an address in the region, and the
doses counted by the date given where it dates them; every device it leaves unfiled they take as the cracker sheet
does. The cracker lands the call, runs the hygiene battery, executes every filed rule and cracks the most obvious
device of each ask: the circular with LH27 placed by its recorded date, every registration a person (Ask 1), merges
followed and replaced and withdrawn lines removed on its own Ask 1 population, the doses counted to 30 June by the
date given (Ask 2), and the back-entries joined through their comments or a person-level key, whichever keeps more
(Ask 3). The mirror is the best response off
the call (no catch-up, every diary), scored on readings of its own and at its strongest: on each ask the best handling
that applies what is filed and cracks at most one device left unfiled beyond the cracker sheet's (Ask 2 on that
response's own Ask 1 population, over every merge, query and, where the prompt leaves it open, dose-date handling;
Ask 3 on any route but the cracker's), chosen against the answers, the worst honest number. The full includer handles
every device and must reproduce figures.json exactly; the lines after the pair price one more device cracked. Pair
on the generated rubric's weights by the sheet's formula: 38 recommendation and components, 7 instruction following,
55 asks over 25 figures; a wrong call keeps r = 5 (the deck's chart and slide structure); each response keeps 8 per
cent of the ask weight as method credit on the ask paths beside the figures it lands."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A        # noqa: E402
import bundle as B      # noqa: E402
import world as W       # noqa: E402

KEYS = ("A", "B", "C", "D", "E")
METHOD_CREDIT = 0.08    # the ask sheet's method credit on the ask paths, as a share of the ask weight
R_OFF = 5               # what a wrong call keeps of the recommendation block (chart and slide structure)

# What the prompt files, read literally: the population by the address's region, and the doses by their date
FILED = {
    "population": re.compile(r"\bat an address in the region\b|\baddress in the (?:region|State)\b|"
                             r"\bliving in the State\b"),
    "window": re.compile(r"\bhave had no valid MMR dose (?:by that date|by 30 June 2027|on or before 30 June 2027)\b|"
                         r"\bdoses? dated on or before 30 June 2027\b"),
    "unit": re.compile(r"\bhow many people born in its years had a confirmed measles case\b"),
}

ASK1_ROUTES = {   # (area code reading, which registrations are one person, registrations no practice lists)
    "the current code list, every registration a person (the natural path)": ("current", "none", "keep"),
    "the circular read, LH27 by its recorded date, every registration a person": ("lh27", "none", "keep"),
    "the current code list, registrations holding one GP line joined": ("current", "golden", "keep"),
    "every LH27 read as Monaghan West, every registration a person": ("old", "none", "keep"),
    "every LH27 read as Monaghan West, registrations holding one GP line joined": ("old", "golden", "keep"),
    "every active registration": ("all", "none", "keep"),
    "the circular read, a person key on date of birth, sex and area code": ("lh27", "dob_sex_area", "keep"),
    "the circular read, a person key on date of birth, sex and postcode": ("lh27", "dob_sex_postcode", "keep"),
    "the circular read, records joined by any shared source reference": ("lh27", "any_ref", "keep"),
    "the circular read, registrations no practice lists left out": ("lh27", "none", "drop"),
    "full includer: the circular read, registrations holding one GP line joined": ("lh27", "golden", "keep"),
}
# which of Ask 1's two devices each route handles right (D7 the reissued code, Dn the second registrations); "old"
# reads every LH27 as Monaghan West, no crack of D7; a person key or any shared reference over-joins, no crack of Dn
ASK1_HANDLES = {("current", "none"): set(), ("lh27", "none"): {"D7"}, ("current", "golden"): {"Dn"},
                ("old", "none"): set(), ("old", "golden"): {"Dn"}, ("all", "none"): set(),
                ("lh27", "dob_sex_area"): {"D7"}, ("lh27", "dob_sex_postcode"): {"D7"}, ("lh27", "any_ref"): {"D7"},
                ("lh27", "golden"): {"D7", "Dn"}}
ASK2_STOPS = {
    "merges followed, replaced and withdrawn lines out, every registration a person (the cracker)": dict(link="none"),
    "merges followed, replaced and withdrawn lines out, the current code list's people": dict(pop="current"),
    "the natural path: every loaded event, no merges, every registration a person, the current code list":
        dict(pop="current", ev_how="all", merge_how="none", link="none"),
    "every loaded event, no merges, on Ask 1's people": dict(ev_how="all", merge_how="none"),
    "merges followed, queries ignored": dict(ev_how="all"),
    "replaced and withdrawn lines out, no merges": dict(merge_how="none"),
    "every queried line dropped": dict(ev_how="drop_queried"),
    "one merge followed, not the chain": dict(merge_how="one_hop"),
    "full includer: merges to the surviving record, replaced and withdrawn lines out, Ask 1's people": dict(),
}
ASK3_ROUTES = {
    "every confirmed row counted": "none",
    "back-entries joined through their comments (the cracker's first path)": "legacy",
    "date of birth, sex and onset (the cracker's second path)": "key",
    "one per date of birth and sex": "dob_sex",
    "date of birth and sex, onsets within 14 days": "window14",
    "reference-laboratory positives only": "lab",
    "full includer: comments and a person key together": "golden",
}
WINDOWS = ("date given to 30 June", "every row in the extract", "loaded by 30 June")


def figure_keys(figs):
    out = {}
    for k in KEYS:
        out["ask1 residents %s" % k] = int(figs["ask1_register_residents"][k].replace(",", ""))
        out["ask2 none %s" % k] = int(figs["ask2_no_valid_dose"][k].replace(",", ""))
        out["ask2 one %s" % k] = int(figs["ask2_one_valid_dose"][k].replace(",", ""))
        out["ask3 confirmed %s" % k] = int(figs["ask3_confirmed_cases"][k].replace(",", ""))
        out["ask3 imported %s" % k] = int(figs["ask3_imported"][k].replace(",", ""))
    return out


def keyed1(res):
    return {"ask1 residents %s" % k: res[k] for k in KEYS}


def keyed2(res):
    r = {}
    for k in KEYS:
        r["ask2 none %s" % k] = res[k]["none"]
        r["ask2 one %s" % k] = res[k]["one"]
    return r


def keyed3(res):
    r = {}
    for k in KEYS:
        r["ask3 confirmed %s" % k] = res[k]["confirmed"]
        r["ask3 imported %s" % k] = res[k]["imported"]
    return r


def ask2(f, window="date given to 30 June", **kw):
    """Ask 2 under a dose-date handling: the date given to 30 June (the golden's), every row the extract holds, or
    the rows loaded by 30 June."""
    ev = f["events"]
    if window == "loaded by 30 June":
        ev = ev[ev["loaded_on"] <= W.AS_AT.isoformat()]
    if window == "every row in the extract":
        keep, A.AS_AT = A.AS_AT, pd.Timestamp("2099-12-31")
        try:
            return keyed2(A.ask2(f, events=ev, **kw))
        finally:
            A.AS_AT = keep
    return keyed2(A.ask2(f, events=ev, **kw))


def digest(target):
    zp = os.path.join(os.path.dirname(target.rstrip("/")), "target.zip")
    h = hashlib.sha256()
    for fn in sorted(os.listdir(target)):
        h.update(fn.encode())
        h.update(open(os.path.join(target, fn), "rb").read())
    z = hashlib.md5(open(zp, "rb").read()).hexdigest() if os.path.exists(zp) else "no target.zip"
    return h.hexdigest()[:16], z


def main(target, prompt_path):
    figs = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    truth = figure_keys(figs)
    prompt = open(prompt_path, encoding="utf-8").read()
    pop_filed = bool(FILED["population"].search(prompt))
    win_filed = bool(FILED["window"].search(prompt))
    unit_filed = bool(FILED["unit"].search(prompt))
    f = B.ask_frames(target)
    d_pack, d_zip = digest(target)
    print("pack %s (target/ sha256 %s, target.zip md5 %s)" % (target, d_pack, d_zip))
    print("prompt %s (%d characters): population by address %s; doses dated %s; ask 3 counted in people %s" % (
        prompt_path, len(prompt), "FILED" if pop_filed else "not filed", "FILED" if win_filed else "not filed",
        "FILED" if unit_filed else "not filed"))
    n1, n2, n3 = 5, 10, 10
    total = n1 + n2 + n3
    print("ask 1: %d figures, ask 2: %d, ask 3: %d; the deck's chart and call slide are scored with the "
          "recommendation (outside)" % (n1, n2, n3))
    hits1, hits3 = {}, {}
    for nm, (how, link, unl) in ASK1_ROUTES.items():
        out = keyed1(A.ask1(f, how=how, link=link, unlisted=unl))
        hits1[(how, link, unl)] = sum(out[k] == truth[k] for k in out)
        print("  1  %-98s %2d of %d" % (nm, hits1[(how, link, unl)], n1))
    for nm, kw in ASK2_STOPS.items():
        out = ask2(f, **kw)
        print("  2  %-98s %2d of %d" % (nm, sum(out[k] == truth[k] for k in out), n2))
    for w in WINDOWS[1:]:
        out = ask2(f, window=w)
        print("  2  %-98s %2d of %d" % ("every device handled, doses counted by " + w, sum(out[k] == truth[k]
                                                                                          for k in out), n2))
    outs3 = {}
    for nm, how in ASK3_ROUTES.items():
        out = keyed3(A.ask3(f["cases"], how, f["lab"]))
        outs3[nm] = out
        hits3[nm] = sum(out[k] == truth[k] for k in out)
        print("  3  %-98s %2d of %d" % (nm, hits3[nm], n3))

    # the full includer is the control: every device handled reproduces figures.json exactly
    full1 = keyed1(A.ask1(f))
    full2 = ask2(f)
    full3 = outs3["full includer: comments and a person key together"]
    full = dict(full1, **full2, **full3)
    exact = all(full[k] == truth[k] for k in truth)
    print("full includer (every device handled): %d of %d ask figures, %s" % (
        sum(full[k] == truth[k] for k in truth), total, "reproduces figures.json exactly" if exact else
        "DOES NOT REPRODUCE"))
    if not exact:
        return 1

    # the cracker: what the prompt files, plus the cracker sheet's device on each ask
    c1 = ("golden" if pop_filed else "lh27", "none", "keep")
    c2 = ask2(f, pop=c1[0], link=c1[1], unlisted=c1[2])
    # Ask 3: the cracker sheet's one device, the back-entries joined through their comments or a person-level key; where
    # the prompt counts people, the person key is the filed WHAT and the cracker's one device is the comments
    if unit_filed:
        c3 = "full includer: comments and a person key together"
    else:
        c3 = max(("back-entries joined through their comments (the cracker's first path)",
                  "date of birth, sex and onset (the cracker's second path)"), key=lambda r: hits3[r])
    kc1, kc2, kc3 = hits1[c1], sum(c2[k] == truth[k] for k in c2), hits3[c3]
    kc = kc1 + kc2 + kc3

    # the mirror: what the prompt files, then at most one of each ask's devices (Ask 1: D7 and Dn), Ask 2 on that
    # response's own Ask 1 population over every merge, query and, where the prompt leaves it open, dose-date handling
    allowed1 = [r for r in hits1 if len(ASK1_HANDLES[r[:2]]) <= 1]
    windows = (WINDOWS[0],) if win_filed else WINDOWS
    grid = {}
    for r in allowed1:
        for merge_how in ("none", "one_hop", "chain"):
            for ev_how in ("all", "golden", "drop_queried"):
                for w in windows:
                    out = ask2(f, window=w, pop=r[0], link=r[1], unlisted=r[2], ev_how=ev_how, merge_how=merge_how)
                    grid[(r, merge_how, ev_how, w)] = sum(out[k] == truth[k] for k in out)
    best1 = max(allowed1, key=lambda r: hits1[r] + max(v for k, v in grid.items() if k[0] == r))
    best2 = max((k for k in grid if k[0] == best1), key=lambda k: grid[k])
    if unit_filed:
        # the filed person key plus at most one device more: the comments, which make the ask whole
        m3 = max((r for r in ASK3_ROUTES if ASK3_ROUTES[r] in ("key", "dob_sex", "window14", "lab", "golden")),
                 key=lambda r: hits3[r])
    else:
        m3 = max((r for r in ASK3_ROUTES if not r.startswith("full includer") and r != c3), key=lambda r: hits3[r])
        assert m3 != c3, "the two rows are scored from different readings"
    km = hits1[best1] + grid[best2] + hits3[m3]
    print("ask 2 on each of the mirror's ask 1 populations (%d populations x 3 merge x 3 query x %d dose-date "
          "handlings): at most %d of %d" % (len(allowed1), len(windows), max(grid.values()), n2))

    def score(on_call, kept):
        L = kept / float(total) + METHOD_CREDIT
        return (38 + 7 + 55 * L) if on_call else (R_OFF + 7 + 55 * L)
    C, S = score(True, kc), score(False, km)
    print("cracker (on the call; ask 1 %s, ask 2 on that population with merges, replaced and withdrawn lines handled, "
          "the doses to 30 June by the date given, ask 3 %s): ask 1 %d, ask 2 %d, ask 3 %d, %d of %d ask figures, %.1f"
          % ("/".join(c1), c3, kc1, kc2, kc3, kc, total, C))
    print("mirror (off the call, no catch-up on every diary; ask 1 %s | ask 2 on that population, merges %s, queries %s, "
          "doses %s | %s): %d of %d ask figures, %.1f" % ("/".join(best1), best2[1], best2[2], best2[3], m3, km, total,
                                                          S))
    print("Cracker keeps: %d of %d ask figures" % (kc, total))
    print("Mirror leakage: %.1f per cent of ask weight (%d of %d figures, plus %.0f per cent method credit)" % (
        100.0 * km / total + 100 * METHOD_CREDIT, km, total, 100 * METHOD_CREDIT))
    print("Pair ceiling: %.1f" % ((C + S) / 2))
    Cm = score(True, km)
    print("both top responses on the call (the cracker and the mirror's ask routes): %.1f and %.1f, pair %.1f" % (
        C, Cm, (C + Cm) / 2))
    # one more device cracked: Ask 2 is counted on Ask 1's people, so a cracker that also joins the registrations one
    # GP line holds runs its Ask 2 route on the full includer's population
    f2 = sum(full2[k] == truth[k] for k in full2)
    for nm, k in (("also joined the registrations one GP line holds (ask 1 whole, ask 2 on its people)",
                   n1 + f2 + kc3),
                  ("joined both the comments and a person key (ask 3 whole)", kc1 + kc2 + n3),
                  ("cracked every device", total)):
        print("  if the cracker %s: %d of %d, %.1f, pair with the mirror %.1f" % (nm, k, total, score(True, k),
                                                                               (score(True, k) + S) / 2))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", default=os.path.join(os.path.dirname(HERE), "target"))
    ap.add_argument("--prompt", default=os.path.join(os.path.dirname(HERE), "prompt.txt"))
    a = ap.parse_args()
    sys.exit(main(a.target, a.prompt))
