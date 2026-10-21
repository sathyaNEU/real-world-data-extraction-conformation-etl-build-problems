"""task177 independent verifier: recomputes the call and every graded figure from the shipped bundle alone (target/,
the goldens, submission.md, prompt.txt), with its own code and its own reading of each file, and compares them with
generator/figures.json. It imports nothing from the generator.

    python3 task177/generator/verify.py <target>"""
from __future__ import annotations

import calendar
import datetime as dt
import json
import math
import os
import re
import sys
import zipfile

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
OUT = []
PLANS = ("Digital", "Digital Plus", "Family")
MONTHS = {1: "January", 2: "February", 3: "March", 10: "October", 11: "November", 12: "December"}


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond)))
    print("%-4s %-66s %s" % ("PASS" if cond else "FAIL", label, detail), flush=True)


def nearest(v, unit):
    return int(unit * math.floor(v / unit + 0.5))


def edge(v, unit):
    return unit / 2 - abs(v - round(v / unit) * unit)


def last_sunday(y, m):
    d = dt.date(y, m, calendar.monthrange(y, m)[1])
    return d - dt.timedelta((d.weekday() + 1) % 7)


def uk(t):
    """a UTC time as UK wall time: BST from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last Sunday of
    October"""
    a = dt.datetime.combine(last_sunday(t.year, 3), dt.time(1))
    b = dt.datetime.combine(last_sunday(t.year, 10), dt.time(1))
    return t + dt.timedelta(hours=1) if a <= t < b else t


def main(target):
    rd = lambda f: pd.read_csv(os.path.join(target, f), dtype=str, keep_default_na=False)
    figs = json.load(open(os.path.join(HERE, "figures.json")))

    # ------------------------------------------------------------------------------------------- the call
    asg = rd("retention_campaign_2026-01_assignment.csv")
    ev = rd("subscription_events.csv")
    lbs = rd("legacy_billing_invoices.csv")
    lbs["day"] = pd.to_datetime(lbs.invoice_date, dayfirst=True, format="%d/%m/%Y")
    lbs["gbp"] = lbs.amount_pence.astype(int) / 100
    leg = ev[ev.system == "legacy"].copy()
    leg["day"] = pd.to_datetime(leg.event_date)
    end = leg[leg.event == "access_ended"].groupby("subscription_key").day.min()
    back = leg[leg.event == "restarted"].groupby("subscription_key").day.min()
    h = pd.Timestamp("2026-03-31")
    e_, b_ = asg.subscription_ref.map(end), asg.subscription_ref.map(back)
    asg["kept"] = (~(e_.notna() & (e_ < h)) | (b_.notna() & (b_ <= h))).astype(int)
    asg["offer"] = asg.arm == "offer"
    jan = lbs[(lbs.line_type == "SUB") & (lbs.day.dt.year == 2026) & (lbs.day.dt.month == 1)]
    bday = jan.groupby("subscription_ref").day.max().dt.day
    asg["bill_day"] = asg.subscription_ref.map(bday)
    ok("every test subscription has a January 2026 bill", asg.bill_day.notna().all())
    asg["lead"] = [(dt.date(2026, 2, min(int(k), 28)) - dt.date(2026, 1, 31)).days for k in asg.bill_day]

    def gap(df):
        return 100 * (df.kept[df.offer].mean() - df.kept[~df.offer].mean())

    whole, fort = gap(asg), gap(asg[asg.lead <= 14])
    later = gap(asg[asg.lead > 14])
    sp = rd("subscriptions_platform_invoices.csv")
    lst = rd("at_risk_list_2027-01-26.csv")
    ids = set(lst.subscription_id)
    rows = []
    for iid, doc, at, lj in zip(sp.invoice_id, sp.doc_type, sp.issued_at, sp.lines):
        if doc != "invoice":
            continue
        t = uk(dt.datetime.strptime(at, "%Y-%m-%dT%H:%M:%SZ"))
        for x in json.loads(lj):
            if x["subscription_id"] in ids:
                rows.append((x["subscription_id"], x["item"], x["to"], float(x["amount"]), t.year, t.month))
    ln = pd.DataFrame(rows, columns=["sub", "item", "to", "gbp", "y", "m"])
    nxt = ln.groupby("sub").to.max().map(lambda s: dt.date.fromisoformat(s) + dt.timedelta(1))
    leads = {(d - dt.date(2027, 1, 26)).days for d in nxt}
    ok("this year's list: every subscription billed to 31 January, next bill 1 February, 6 days after the send",
       len(nxt) == len(ids) == 48000 and leads == {6}, str(sorted(leads)))
    ok("call: the fortnight's arms, carried to a list billed 6 days after the send", nearest(fort, 5) == figs["call_share"]
       == 20, "%.2f" % fort)
    ok("call components: whole list, fortnight, later (nearest 5)",
       (nearest(whole, 5), nearest(fort, 5), nearest(later, 5)) == (figs["call_whole_list"], figs["call_fortnight_kept"],
                                                                   figs["call_later_kept"]),
       "%.2f %.2f %.2f" % (whole, fort, later))
    ok("call: distance to the cell's edge at least 2 points", edge(fort, 5) >= 2.0, "%.2f" % edge(fort, 5))
    ok("call counts: test list, fortnight subscriptions, this year's list",
       (len(asg), int((asg.lead <= 14).sum()), len(lst)) == (figs["call_n_ly"], figs["call_n_fort"], figs["call_n_ty"]))

    # ------------------------------------------------------------------------------------------- ask A
    off = rd("offers_engine_acceptances_2026.csv")
    prof = rd("subscriber_profile_2026-01-31.csv").set_index("subscription_ref")
    d = lbs[(lbs.line_type == "DISC") & lbs.applied_ref.isin(set(off.acceptance_ref))].copy()
    d["plan"] = d.subscription_ref.map(prof.plan)
    for m in (2, 3):
        for pl in PLANS:
            v = -d[(d.day.dt.year == 2026) & (d.day.dt.month == m) & (d.plan == pl)].gbp.sum()
            ok("ask A discount, %s 2026 bills, %s" % (MONTHS[m], pl),
               nearest(v, 100) == figs["ask_a_discount"]["%s %s" % (MONTHS[m], pl)] and edge(v, 100) >= 25,
               "%.2f, edge %.2f" % (v, edge(v, 100)))
    tk = d.drop_duplicates("subscription_ref").plan.value_counts()
    for pl in PLANS:
        ok("ask A takers, %s" % pl, int(tk.get(pl, 0)) == figs["ask_a_takers"][pl], str(int(tk.get(pl, 0))))

    # ------------------------------------------------------------------------------------------- ask B
    plan = lst.set_index("subscription_id").plan
    xw = rd("subscription_id_crosswalk.csv").set_index("legacy_subscription_ref").platform_subscription_id
    lb = lbs[(lbs.line_type == "SUB") & (lbs.day >= "2026-10-01")].copy()
    lb["sub"] = lb.subscription_ref.map(xw)
    lb = lb[lb["sub"].isin(ids)]
    cov = set(x for s in sp[sp.doc_type == "credit_note"].covers for x in s.split(";") if x)
    for (y, m) in ((2026, 10), (2026, 11), (2026, 12), (2027, 1)):
        for pl in PLANS:
            s_ = ln[(ln.y == y) & (ln.m == m) & (ln["sub"].map(plan) == pl)].gbp.sum()
            g_ = lb[(lb.day.dt.year == y) & (lb.day.dt.month == m) & (lb["sub"].map(plan) == pl)]
            v = s_ + g_.gbp.sum() - g_[g_.invoice_no.isin(cov)].gbp.sum()
            ok("ask B billed for the plan after credits, %s %d, %s" % (MONTHS[m], y, pl),
               nearest(v, 100) == figs["ask_b_billed"]["%s %d %s" % (MONTHS[m], y, pl)] and edge(v, 100) >= 25,
               "%.2f, edge %.2f" % (v, edge(v, 100)))

    # ------------------------------------------------------------------------------- the write-up and goldens
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    money = lambda v: "GBP {:,}".format(int(v))
    want = ["%d per cent" % figs["call_share"]]
    want += [money(v) for v in figs["ask_a_discount"].values()] + [money(v) for v in figs["ask_b_billed"].values()]
    want += ["{:,}".format(v) for v in figs["ask_a_takers"].values()]
    miss = [w for w in want if w not in sub]
    ok("submission.md states every graded figure as figures.json holds it", not miss, ", ".join(miss[:5]))
    blocks = [l for l in sub.splitlines() if l.startswith("## ")]
    ok("submission.md has exactly the five blocks", blocks == ["## Tags", "## 1. Final Recommendation",
                                                            "## 2. Critical Components", "## 3. Step-by-Step Solution",
                                                            "## 4. Deliverable Answers"], str(blocks))
    steps = re.findall(r"^\d+\. ", sub.split("## 3. Step-by-Step Solution")[1].split("## 4.")[0], re.M)
    ok("at most eight steps", len(steps) <= 8, str(len(steps)))
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(TASK, "golden", "retention_offer_forecast_2027.xlsx"), data_only=True)
    vals = [c.value for ws in wb.worksheets for r in ws.iter_rows() for c in r if isinstance(c.value, (int, float))]
    need = [figs["call_share"]] + list(figs["ask_a_discount"].values()) + list(figs["ask_a_takers"].values()) + \
        list(figs["ask_b_billed"].values())
    ok("the workbook carries the call and every ask figure", all(v in vals for v in need))
    with zipfile.ZipFile(os.path.join(TASK, "golden", "january_offer_note.docx")) as z:
        body = re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode("utf-8"))
    ok("the note commits the call", "%d per cent" % figs["call_share"] in body)
    prompt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    ok("the prompt's roundings govern the figures as printed",
       "nearest 5 per cent" in prompt and "nearest hundred" in prompt and "whole numbers" in prompt)
    bad = [p for p in (sub, body, prompt) if "\u2014" in p or "\u2013" in p]
    ok("no em or en dash in the write-up, the note or the prompt", not bad)

    fails = [o for o in OUT if not o[1]]
    print("%s: %d checks, %d FAIL" % ("PASS" if not fails else "FAIL", len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
