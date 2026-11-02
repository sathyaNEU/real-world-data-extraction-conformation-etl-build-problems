"""task464 architecture 12: the independent verifier. Reads only target/ and golden/, never the generator's state
or answers.py, and recomputes every graded figure on its own (pandas) code path; then reads back every format the
pack ships with a positive control on the same extractor.

    python3 generator/verify.py      # exit 1 on any failure
"""
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
TGT = os.path.join(BASE, "target")
GOLD = os.path.join(BASE, "golden")
SENDS = pd.to_datetime(["2026-04-14", "2026-05-12", "2026-06-09", "2026-07-07", "2026-08-04", "2026-09-01"])
RS = ["RS-2604", "RS-2605", "RS-2606", "RS-2607", "RS-2608", "RS-2609"]
FAILS = []


def check(name, ok, detail=""):
    print("%s  %-58s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8")
    x = re.sub(r"</w:p>", "\n", x)
    return re.sub(r"<[^>]+>", "", x)


def pdf_text(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() or "" for p in PdfReader(path).pages)


def warehouse():
    w = pd.read_csv(os.path.join(TGT, "sponsored_clicks_by_mailbox_daily.csv"))
    n0 = len(w)
    w = w.drop_duplicates()
    w["channel"] = w["channel"].where(~w["channel"].str.startswith("app"), "app")
    w["click_date"] = pd.to_datetime(w["click_date"])
    clicks = w.groupby(["click_date", "mailbox_group", "audience"], as_index=False)["sponsored_clicks"].sum()
    js = w.groupby(["click_date", "mailbox_group", "audience"], as_index=False)["jobseekers"].first()
    t = clicks.merge(js, on=["click_date", "mailbox_group", "audience"])
    return t, n0 - len(w)


def pilot_mask(d):
    m = np.zeros(len(d), bool)
    for s in SENDS:
        m |= (d >= s) & (d < s + pd.Timedelta(days=28))
    return m


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    t, dup = warehouse()
    check("warehouse reload rows dropped as exact copies", dup > 0, "%d rows" % dup)
    pil = t[pilot_mask(t["click_date"].values)]
    arms = pil[pil["audience"].str.startswith("restart_pilot")]
    size = t[(t["click_date"] == SENDS[0]) & t["audience"].str.startswith("restart_pilot")].groupby("audience")["jobseekers"].sum()
    cl = arms.groupby("audience")["sponsored_clicks"].sum()
    nm, nh = size["restart_pilot_mailed"], size["restart_pilot_holdout"]
    U = (cl["restart_pilot_mailed"] / nm - cl["restart_pilot_holdout"] / nh) * nm
    check("pilot gain among the paused pool", abs(U - fig["pilot_uplift_exact"]) < 0.5, "%.1f" % U)
    act = t[t["audience"] == "alerts_on"].pivot_table(index="click_date", columns="mailbox_group",
                                                       values=["sponsored_clicks", "jobseekers"], aggfunc="sum")
    C, N = act["sponsored_clicks"], act["jobseekers"]
    R = C / N
    # groups that fall after the sends: each against its own same-weekday rate in the 14 days before each send
    share = {}
    for g in C.columns:
        loss = base = 0.0
        for s in SENDS:
            for i in range(14):
                d = s + pd.Timedelta(days=i)
                prev = [s - pd.Timedelta(days=j) for j in range(1, 15)]
                same = [x for x in prev if x.weekday() == d.weekday() and x in R.index]
                cf = R.loc[same, g].mean()
                loss += (cf - R.loc[d, g]) * N.loc[d, g]
                base += C.loc[d, g]
        share[g] = loss / base
    aff = sorted(g for g in share if share[g] > 0.01)
    ctl = sorted(g for g in share if share[g] <= 0.01)
    check("groups that fall after the sends", aff == sorted(fig["affected_groups"]), ", ".join(aff))
    ctl_rate = C[ctl].sum(axis=1) / N[ctl].sum(axis=1)
    D = 0.0
    for g in aff:
        for s in SENDS:
            ev = pd.date_range(s, periods=14)
            ref = pd.date_range(s + pd.Timedelta(days=14), periods=14)
            ratio = (C.loc[ref, g].sum() / N.loc[ref, g].sum()) / (C.loc[ref, ctl].sum().sum() / N.loc[ref, ctl].sum().sum())
            D += ((ctl_rate.loc[ev] * ratio - R.loc[ev, g]) * N.loc[ev, g]).sum()
    check("pilot loss among jobseekers with alerts on", abs(D - fig["pilot_loss_exact"]) < 0.5, "%.1f" % D)
    net = U - D
    f27 = net / 6 * 13
    check("2027 sizing", abs(f27 - fig["series_2027_clicks_exact"]) < 0.5, "%.1f" % f27)
    check("2027 at the nearest 100,000", int(100000 * round(f27 / 100000)) == fig["series_2027_clicks"],
          "%d" % int(100000 * round(f27 / 100000)))
    for k, (v, unit) in {"pilot_uplift_clicks": (U, 50000), "pilot_loss_clicks": (D, 50000),
                         "pilot_net_clicks": (net, 50000)}.items():
        check("%s at the nearest %d" % (k, unit), int(unit * round(v / unit)) == fig[k], "%d" % int(unit * round(v / unit)))
    check("call: drop", (f27 < 0) and fig["call"] == "drop")

    # asks
    rl = pd.read_csv(os.path.join(TGT, "alert_restarts_pilot_pool_2026.csv"), dtype=str)
    ev = pd.read_csv(os.path.join(TGT, "postvane_clicks_restart_series_2026.csv"), dtype=str)
    ev["t"] = pd.to_datetime(ev["clicked_at_utc"].str.slice(0, 23))
    ev = ev.sort_values(["campaign_code", "subscriber_key", "t"])
    bursts = set()
    for (camp, sub), grp in ev.groupby(["campaign_code", "subscriber_key"], sort=False):
        if len(grp) < 4:
            continue
        ts = grp["t"].values
        ln = grp["link_name"].values
        j = 0
        for i in range(len(ts)):
            while ts[i] - ts[j] > np.timedelta64(10, "s"):
                j += 1
            if len(set(ln[j:i + 1])) >= 4:
                bursts.add((camp, sub))
                break
    el = rl[(rl["route"] == "email_link") & rl["link_campaign"].isin(RS)]
    people = el[[(c, a) not in bursts for c, a in zip(el["link_campaign"], el["account_id"])]]
    a1 = [people.loc[people["link_campaign"] == c, "account_id"].nunique() for c in RS]
    check("ask A1 restarts by people", a1 == fig["restarted_by_people"], str(a1))
    ck = pd.read_csv(os.path.join(TGT, "restarted_jobseekers_sponsored_clicks.csv"), dtype=str)
    pairs = pd.concat([ck.loc[ck["account_id"].notna() & ck["app_install_id"].notna(), ["app_install_id", "account_id"]],
                       rl.loc[rl["app_install_id"].notna(), ["app_install_id", "account_id"]]]).drop_duplicates()
    nacc = pairs.groupby("app_install_id")["account_id"].nunique()
    check("no app device carries two jobseekers", int(nacc.max()) == 1, "max %d" % int(nacc.max()))
    dev = pairs.drop_duplicates("app_install_id").set_index("app_install_id")["account_id"]
    ck["who"] = ck["account_id"].fillna(ck["app_install_id"].map(dev))
    check("every logged-out app click tied to a jobseeker", ck["who"].notna().all())
    check("the pull and the restart log label their clock as UK time; Postvane's as UTC",
          "clicked_at_uk" in ck.columns and "restarted_at_uk" in rl.columns and "clicked_at_utc" in ev.columns
          and "clicked_at" not in ck.columns and "restarted_at" not in rl.columns)
    ck["t"] = pd.to_datetime(ck["clicked_at_uk"])
    ck["d"] = ck["t"].dt.normalize()

    def a2_count(inside):
        out = []
        for k, c in enumerate(RS):
            who = set(people.loc[people["link_campaign"] == c, "account_id"])
            w = ck[inside(k, ck) & ck["who"].isin(who)]
            out.append(int(w["who"].nunique()))
        return out
    a2 = a2_count(lambda k, x: (x["d"] >= SENDS[k]) & (x["d"] <= SENDS[k] + pd.Timedelta(days=27)))
    check("ask A2 clicked on the send's date or in the 27 days after it", a2 == fig["clicked_within_28_days"], str(a2))
    # positive controls on the same readers: each rival reading the prompt and the headers close moves the figure
    hrs = a2_count(lambda k, x: (x["t"] >= SENDS[k] + pd.Timedelta(hours=10)) &
                   (x["t"] < SENDS[k] + pd.Timedelta(days=28, hours=10)))
    check("control: 28 x 24 hours from the 10:00 send moves A2 (closed by the send's date and 27 days)",
          hrs != a2, str(hrs))
    rt = people.assign(rt=pd.to_datetime(people["restarted_at_uk"])).groupby(["link_campaign", "account_id"])["rt"].min()
    post = []
    for k, c in enumerate(RS):
        who = rt.loc[c]
        w = ck[(ck["d"] >= SENDS[k]) & (ck["d"] <= SENDS[k] + pd.Timedelta(days=27)) & ck["who"].isin(who.index)]
        w = w[w["t"] >= w["who"].map(who)]
        post.append(int(w["who"].nunique()))
    check("control: clicks after the restart only moves A2 (closed by 'before or after restarting')", post != a2, str(post))
    as_utc = ck["t"].dt.tz_localize("UTC").dt.tz_convert("Europe/London").dt.tz_localize(None).dt.normalize()
    utc = a2_count(lambda k, x: (as_utc >= SENDS[k]) & (as_utc <= SENDS[k] + pd.Timedelta(days=27)))
    check("control: clicked_at_uk read as UTC moves A2 (closed by the header's label)", utc != a2, str(utc))
    rs = ev[ev["link_name"] == "restart_alerts"].copy()
    rs["uk"] = rs["t"].dt.tz_localize("UTC").dt.tz_convert("Europe/London").dt.tz_localize(None).dt.floor("min")
    first = rs.groupby(["campaign_code", "subscriber_key"])["uk"].min()
    j = el.join(first, on=["link_campaign", "account_id"], how="inner")
    gap = (pd.to_datetime(j["restarted_at_uk"]) - j["uk"]).dt.total_seconds() / 60
    check("control: every email restart logs the minute of its Postvane restart click on the UK clock (60 min off as UTC)",
          len(j) > 40000 and (gap == 0).all(), "%d rows, gaps %s" % (len(j), sorted(gap.unique())[:3]))
    check("the restart email's links name no job (restart, six sector tiles, the footer)",
          not ev["link_name"].str.match(r"job_?\d").any() and ev["link_name"].nunique() == 11,
          ", ".join(sorted(ev["link_name"].unique())))

    # every format read back, positive control on the same extractor
    plan = docx_text(os.path.join(TGT, "jobseeker_email_plan_2027.docx"))
    check("plan docx: measurement line present", "judged on the sponsored clicks Quaywork takes with it" in plan)
    check("plan docx: thirteen sends and the 28-day count",
          "the 2027 series is sized at what one pilot send did on average, thirteen times" in plan and
          "those clicks are counted over the 28 days from each pilot send" in plan)
    brief = pdf_text(os.path.join(TGT, "restart_pilot_brief_2026.pdf"))
    check("pilot brief pdf: design text present", "Restart my alerts" in brief and "one digit in ten" in brief, "%d chars" % len(brief))
    from openpyxl import load_workbook
    cal = load_workbook(os.path.join(TGT, "crm_send_calendar_2026.xlsx"), read_only=True)
    codes = [r[0] for r in cal["Sends 2026"].iter_rows(min_row=2, values_only=True)]
    check("send calendar xlsx: the six restart sends", all(c in codes for c in RS), str(codes[:4]))
    rev = load_workbook(os.path.join(TGT, "sponsored_revenue_by_sector_2026.xlsx"), read_only=True)
    check("revenue xlsx readable", rev.sheetnames == ["Sponsored by sector"])
    words = re.compile(r"\b(junk|spam folder|reputation|deliverability|inbox placement|spam trap|interference|"
                       r"spillover|gateway|scanner|logged out|holdout uplift)\b", re.I)
    for name, txt in [("plan", plan), ("brief", brief)]:
        check("%s: none of the step's vocabulary" % name, not words.search(txt), (words.search(txt) or [""])[0])
    # goldens
    gx = load_workbook(os.path.join(GOLD, "restart_series_2027.xlsx"), read_only=True)
    vals = [r for r in gx["Pilot sends"].iter_rows(min_row=2, max_row=7, values_only=True)]
    check("golden workbook: restart counts", [v[4] for v in vals] == fig["restarted_by_people"] and
          [v[5] for v in vals] == fig["clicked_within_28_days"])
    sz = [r for r in gx["Sizing"].iter_rows(values_only=True)]
    flat = [x for r in sz for x in r if isinstance(x, (int, float))]
    check("golden workbook: 2027 figure at its rounding", fig["series_2027_clicks"] in flat)
    note = docx_text(os.path.join(GOLD, "restart_series_2027.docx"))
    check("golden note: recommendation and 2027 cost", "Drop the restart series" in note and "300,000" in note)
    with zipfile.ZipFile(os.path.join(GOLD, "restart_series_2027.docx")) as z:
        check("golden note: one chart", sum(1 for n in z.namelist() if n.startswith("word/media/")) == 1)
    print("verify: %d failures" % len(FAILS))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
