"""task173 independent verifier: reads only the shipped bundle (target/) and generator/figures.json, recomputes the
booking and every ask figure with its own code (pandas, its own parsing of the standard, the calendar and the
invoices), and checks each against figures.json.

    python3 task173/generator/verify.py <target>"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def check(label, ok, detail=""):
    OUT.append(bool(ok))
    print("%s %-70s %s" % ("PASS" if ok else "FAIL", label[:70], detail))


def edt(s):
    """UTC stamps to Eastern clock time for the season's dates (EST before 8 March 2026, EDT after)."""
    t = pd.to_datetime(s, format="%Y-%m-%dT%H:%M:%SZ")
    dst0 = pd.Timestamp("2026-03-08 07:00:00")
    return t - pd.to_timedelta(np.where(t >= dst0, 4, 5), unit="h")


def pdf_text(path):
    import logging
    logging.getLogger("pypdf").setLevel(logging.ERROR)
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def half_up(x, nd=0):
    return math.floor(x * 10 ** nd + 0.5) / 10 ** nd


def main(t):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    # ------------------------------------------------------------------------------------- the standard's numbers
    import docx
    std = "\n".join(p.text for p in docx.Document(os.path.join(t, "expert_capacity_planning_standard.docx")).paragraphs)
    H = float(re.search(r"= ([\d.]+) handle hours across the fortnight", std).group(1))
    HB = float(re.search(r"Each agent hour billed by the outsourcer gives ([\d.]+) handle hours", std).group(1))
    block = int(re.search(r"whole blocks of ([\d,]+) agent hours", std).group(1).replace(",", ""))
    m = re.search(r"For the 2027 season it runs from \w+ (\d+) (\w+) (\d{4}) to \w+ (\d+) (\w+) (\d{4})", std)
    f0 = dt.datetime.strptime("%s %s %s" % m.group(1, 2, 3), "%d %B %Y").date()
    f1 = dt.datetime.strptime("%s %s %s" % m.group(4, 5, 6), "%d %B %Y").date()
    check("the standard: %.3f handle hours an expert, %.2f a billed hour, blocks of %d" % (H, HB, block), H > 60)

    # ------------------------------------------------------------------------------------- the 2026 CRM
    crm = pd.read_csv(os.path.join(t, "crm_expert_interactions_2026.csv"))
    en = crm[crm["Queue"] == "Live Experts EN"].copy()
    en["start"] = edt(en["Started (UTC)"])
    en["date"] = en["start"].dt.normalize()
    en["hmin"] = (en["Talk Seconds"] + en["After-Contact Work Seconds"]) / 60.0
    ros = pd.read_excel(os.path.join(t, "seasonal_expert_roster_2027.xlsx"), sheet_name="Seasonal experts")
    first = dict(zip(ros["Employee No"], ros["First Season"]))
    golive = dict(zip(ros["Employee No"], pd.to_datetime(ros["2026 Go-Live"])))
    en["grp"] = np.where(en["Handled By"].str.startswith("HCS-"), "V",
                         np.where(en["Handled By"].map(first) == 2026, "N", "R"))
    en["gl"] = en["Handled By"].map(golive)
    en["wk"] = (en["date"] - en["gl"]).dt.days / 7.0
    en = en.sort_values(["Case Number", "start", "Interaction ID"])
    en["followed"] = (en["Case Number"].shift(-1) == en["Case Number"]).astype(float)
    en["opening"] = en["Interaction Type"] == "New case"
    fo = en[en["opening"]]
    pR = fo.loc[fo["grp"] == "R", "followed"].mean()
    pO = fo.loc[fo["grp"] == "V", "followed"].mean()
    q = en.loc[~en["opening"], "followed"].mean()
    aR = en.loc[en["grp"] == "R", "hmin"].mean()
    aO = en.loc[en["grp"] == "V", "hmin"].mean()

    def expo(x, a, b, c):
        return a + b * np.exp(-x / c)

    def fit(sub, col, p0):
        b = np.floor(sub["wk"]).astype(int)
        g = sub.groupby(b)[col].agg(["mean", "size"])
        c, _ = curve_fit(expo, g.index.values + 0.5, g["mean"].values, p0=p0, sigma=1 / np.sqrt(g["size"].values),
                         maxfev=40000)
        return c
    cp = fit(fo[fo["grp"] == "N"], "followed", (0.14, 0.3, 5.0))
    ca = fit(en[en["grp"] == "N"], "hmin", (31.0, 14.0, 5.0))
    check("2026 rates: returning %.4f, Hillsborough %.4f, a follow-up's own %.4f" % (pR, pO, q),
          abs(100 * pR - fig["follow_returning_pct"]) < 0.05 and abs(100 * pO - fig["follow_vendor_pct"]) < 0.05
          and abs(100 * q - fig["follow_q_pct"]) < 0.05)

    # ------------------------------------------------------------------------------------- the 2027 bench and demand
    n_ret = int(((ros["Queue"] == "EN") & (ros["2027 Recall"] == "Confirmed")).sum())
    cal = pdf_text(os.path.join(t, "training_calendar_2027.pdf"))
    classes = [(dt.datetime.strptime(g, "%d %B %Y").date(), int(n)) for g, n in
               re.findall(r"27-\d\s+Room \w\s+\d{1,2} \w+ 2027\s+(\d{1,2} \w+ 2027)\s+(\d+)", cal)]
    plan = pd.read_excel(os.path.join(t, "demand_plan_2027.xlsx"), sheet_name="Daily forecast")
    plan["Date"] = pd.to_datetime(plan["Date"]).dt.date
    F = int(plan.loc[(plan["Date"] >= f0) & (plan["Date"] <= f1), "New expert cases"].sum())
    check("bench %d returning, %d classes of %s; %d new cases" % (n_ret, len(classes), {n for _, n in classes}, F),
          n_ret == fig["returning_2027"] and F == fig["new_cases_2027"] and len(classes) == 4)
    days = [f0 + dt.timedelta(k) for k in range(14)]
    Kc = n_ret * H * 60 / aR
    Kp = Kc * pR
    for d in days:
        for g, n in classes:
            x = (d - g).days / 7.0
            k = n * (H / 14) * 60 / expo(x, *ca)
            Kc += k
            Kp += k * expo(x, *cp)
    kO = HB * 60 / aO
    lo, hi = 0.0, 1e5
    for _ in range(200):
        mid = (lo + hi) / 2
        Ct = Kc + mid * kO
        if Ct - F * (1 + (Kp + mid * kO * pO) / Ct / (1 - q)) < 0:
            lo = mid
        else:
            hi = mid
    booking = int(math.ceil(lo / block - 1e-12) * block)
    check("THE CALL: %d agent hours (%.1f needed)" % (booking, lo), booking == fig["booking_blocks"]
          and abs(lo - fig["billed_hours_needed"]) < 1.0)
    Ct = Kc + lo * kO
    check("forecast contacts %.0f" % Ct, abs(Ct - fig["forecast_contacts"]) < 1.0)

    # ------------------------------------------------------------------------------------- Ask A
    st = pd.read_csv(os.path.join(t, "acd_agent_state_detail_hcs_2026.csv"))
    users = pd.read_csv(os.path.join(t, "acd_users_2026-10-29.csv"))
    ob = pd.read_excel(os.path.join(t, "hcs_agent_onboarding_2026.xlsx"), sheet_name="Agents")
    email_agent = dict(zip(ob["Email"].str.lower(), ob["HCS Agent ID"]))
    agent_of = dict(zip(ob["ACD Login"], ob["HCS Agent ID"]))
    for lg, em, role in zip(users["Login"], users["Email"].fillna("").str.lower(), users["Role"]):
        if role == "Agent" and em in email_agent:
            agent_of.setdefault(lg, email_agent[em])
    bill = st[st["State"].isin(["Available", "On Contact", "After-Contact Work"])].copy()
    bill["agent"] = bill["Agent Login"].map(agent_of)
    bill = bill.dropna(subset=["agent"])
    bill["a"] = edt(bill["Start (UTC)"])
    bill["b"] = edt(bill["End (UTC)"])
    daily = {}
    weekly = {}
    for ag, g in bill.sort_values("a").groupby("agent"):
        cur_a = cur_b = None
        spans = []
        for a, b in zip(g["a"], g["b"]):
            if cur_b is None or a > cur_b:
                if cur_b is not None:
                    spans.append((cur_a, cur_b))
                cur_a, cur_b = a, b
            elif b > cur_b:
                cur_b = b
        spans.append((cur_a, cur_b))
        for a, b in spans:
            while a < b:
                nxt = a.normalize() + pd.Timedelta(days=1)
                c = min(b, nxt)
                h = (c - a).total_seconds() / 3600
                d = a.date()
                daily[d] = daily.get(d, 0.0) + h
                wk = d - dt.timedelta(d.weekday())
                weekly[(ag, wk)] = weekly.get((ag, wk), 0.0) + h
                a = c
    for k, v in fig["ask_a_daily"].items():
        d = dt.date.fromisoformat(k)
        check("Ask A %s billable hours %.1f" % (k, half_up(daily[d], 1)), half_up(daily[d], 1) == v, "figures %.1f" % v)
    inv = pdf_text(os.path.join(t, "hcs_invoices_2026_deadline_period.pdf"))
    blocks = re.split(r"(?=INVOICE HCS-)", inv)[1:]
    parsed = []
    for b in blocks:
        no = re.match(r"INVOICE (HCS-\d\d-\d{4})", b).group(1)
        wk = dt.datetime.strptime(re.search(r"Service week\s+(\d{1,2} \w+ \d{4})", b).group(1), "%d %B %Y").date()
        rep = re.search(r"replaces invoice (HCS-\d\d-\d{4})", b)
        lines = [(a, float(h)) for a, h in re.findall(r"(HCS-\d{4})\s+([\d.]+)\s+38\.50", b)]
        parsed.append((no, wk, rep.group(1) if rep else None, lines))
    gone = {r for _, _, r, _ in parsed if r}
    for k, v in fig["ask_a_unsupported"].items():
        wk = dt.date.fromisoformat(k)
        cur = [p for p in parsed if p[1] == wk and p[0] not in gone]
        assert len(cur) == 1
        u = sum(max(0.0, h - weekly.get((ag, wk), 0.0)) for ag, h in cur[0][3])
        check("Ask A week of %s unsupported %.1f (%s)" % (k, half_up(u, 1), cur[0][0]), half_up(u, 1) == v, "figures %.1f" % v)

    # ------------------------------------------------------------------------------------- Ask B
    ac = pd.read_csv(os.path.join(t, "acd_contact_detail_en_2026_deadline.csv"), dtype={"Session ID": str})
    ac["q"] = pd.to_datetime(ac["Queued (UTC)"], format="%Y-%m-%dT%H:%M:%SZ")
    started = dict(zip(crm["Interaction ID"], pd.to_datetime(crm["Started (UTC)"], format="%Y-%m-%dT%H:%M:%SZ")))
    first_q = ac.groupby("Session ID")["q"].min()
    conv = ac.dropna(subset=["CRM Interaction"]).groupby("Session ID")["CRM Interaction"].first()
    w = pd.DataFrame({"joined": first_q.loc[conv.index], "start": conv.map(started)})
    w["wait"] = (w["start"] - w["joined"]).dt.total_seconds()
    w["date"] = (w["joined"] - pd.Timedelta(hours=4)).dt.date
    for k, v in fig["ask_b_daily_wait"].items():
        d = dt.date.fromisoformat(k)
        mval = w.loc[w["date"] == d, "wait"].mean()
        check("Ask B %s average wait %d s" % (k, int(half_up(mval))), int(half_up(mval)) == v, "%.3f" % mval)
    for k, v in fig["ask_b_share"].items():
        wk = dt.date.fromisoformat(k)
        sel = w[(w["date"] >= wk) & (w["date"] <= wk + dt.timedelta(6))]
        s = 100.0 * (sel["wait"] <= 180).mean()
        check("Ask B week of %s within three minutes %.1f" % (k, half_up(s, 1)), half_up(s, 1) == v, "%.3f" % s)
    # ------------------------------------------------------------------------------------- the text formats
    import email
    from email import policy
    msg = email.message_from_bytes(open(os.path.join(t, "re_2027_deadline_booking.eml"), "rb").read(),
                                   policy=policy.default)
    body = msg.get_body(preferencelist=("plain",)).get_content()
    check("the thread decodes and carries the recall's close", "150 of last season's English" in body
          and len(body) > 300, "%d characters" % len(body))
    notes = open(os.path.join(t, "crm_export_notes.txt"), encoding="utf-8").read()
    check("the CRM notes define the start of an interaction", "when the conversation began" in notes)
    guide = pdf_text(os.path.join(t, "acd_report_field_guide.pdf"))
    check("the field guide defines the accept time", "When the agent accepted the offer." in guide and
          "The customer's session on the expert queue." in guide)
    sch = pdf_text(os.path.join(t, "hcs_msa_schedule_b_2026.pdf"))
    check("Schedule B defines billable time and the agent-by-agent credit",
          "in the Available, On Contact or" in sch and "HCS credits the difference" in sch)
    check("the standard defines the wait and the service level", "to the start of their conversation with an" in std
          and "three minutes or less" in std)
    man = pd.read_csv(os.path.join(t, "data_pull_manifest_2026-10-30.csv"))
    check("the manifest lists every other shipped file", set(man["File"]) == set(os.listdir(t)) -
          {"data_pull_manifest_2026-10-30.csv"}, "%d files" % len(man))
    print("%d checks, %d FAIL" % (len(OUT), OUT.count(False)))
    return 0 if all(OUT) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
