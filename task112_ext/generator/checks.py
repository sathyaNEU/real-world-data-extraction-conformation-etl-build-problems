"""Assertions on the cut pack, read back from the shipped files: the input gates, the keys between files, the
contact policy obeyed send by send, the shopping and redemption files tying, Meta's reach arithmetic, and the
realism sweep. No stump and no device: every check is a coherence check."""
import csv
import datetime as dt
import json
import os
import re
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

import params as P
import records as RC

STO = ZoneInfo("Europe/Stockholm")
N = [0]


def ok(cond, label):
    assert cond, label
    N[0] += 1


def _utc(s):
    return pd.to_datetime(s, utc=True)


def secs(s):
    """epoch seconds whatever resolution pandas chose"""
    return ((s - pd.Timestamp("1970-01-01", tz="UTC")) // pd.Timedelta(seconds=1)).astype(np.int64)


def _loc(s):
    return pd.to_datetime(s).dt.tz_localize(STO, ambiguous="raise", nonexistent="raise").dt.tz_convert("UTC")


def run(target):
    N[0] = 0
    F = RC.FILES
    p = lambda k: os.path.join(target, F[k])
    files = sorted(os.listdir(target))

    # ---------------------------------------------------------------- input gates
    ok(len(files) >= 10 and set(files) == set(F.values()), "G1 the pack holds exactly its 20 files")
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "G2 three or more formats")
    mem = pd.read_csv(p("members"), dtype=str, keep_default_na=False)
    sends = pq.read_table(p("sends")).to_pandas()
    ok(max(len(mem), len(sends)) >= 25000, "G3 a file of 25,000 rows or more")
    for f in files:
        if f.endswith((".csv", ".md", ".jsonl")):
            t = open(os.path.join(target, f), encoding="utf-8").read()
            ok("\u2014" not in t and "\u2013" not in t, "G4 no em or en dash in %s" % f)

    # ---------------------------------------------------------------- keys
    ok(mem.member_id.is_unique and mem.card_number.is_unique, "K1 member and card ids unique")
    ok(all(re.fullmatch(r"BP\d{8}", x) for x in mem.member_id), "K2 member id format")
    ids = set(mem.member_id)
    stores = pd.read_csv(p("stores"), dtype=str)
    codes = set(stores.store_code)
    ok(set(mem.home_store) <= codes, "K3 home stores are stores")
    pcs = pd.read_csv(p("postcodes"), dtype=str)
    ok(set(mem.postcode_area) <= set(pcs.postcode_area) and set(stores.postcode_area) <= set(pcs.postcode_area),
       "K4 postcode areas known")
    hh = mem.groupby("household_id").agg(n=("member_id", "size"), pc=("postcode_area", "nunique"),
                                         mu=("municipality", "nunique"))
    ok((hh.pc == 1).all() and (hh.mu == 1).all(), "K5 a household has one address")
    snap = pd.read_csv(p("snapshot"), dtype=str)
    con = pd.read_csv(p("consent"), dtype=str)
    ok(set(snap.member_id) <= ids and set(con.member_id) <= ids, "K6 consent members are members")
    ok(con.event_id.astype(int).is_monotonic_increasing, "K7 consent log in order")
    mailings = pd.read_csv(p("mailings"), dtype={"sends": int}, keep_default_na=False)
    ok(sends.send_id.is_unique and set(sends.member_id) <= ids, "K8 sends unique and known")
    ok((sends.groupby("mailing_id").size().reindex(mailings.mailing_id).values == mailings.sends.values).all(),
       "K9 mailing counts tie to the sends")
    events = pq.read_table(p("events")).to_pandas()
    m = events.merge(sends[["send_id", "mailing_id", "member_id", "sent_at", "status"]], on="send_id",
                     suffixes=("", "_s"), how="left")
    ok(m.mailing_id_s.notna().all() and (m.mailing_id == m.mailing_id_s).all() and (m.member_id == m.member_id_s).all(),
       "K10 every event belongs to its send")
    ok((m.event_at > m.sent_at).all() and (m.status == "delivered").all(), "K11 events follow delivered sends")
    ok(events.event_id.is_unique, "K12 event ids unique")
    sms = pd.read_csv(p("sms"), dtype=str, keep_default_na=False)
    ok(set(sms.customer_ref) <= ids and sms.message_id.is_unique, "K13 SMS keys")
    push = pd.DataFrame([json.loads(x) for x in open(p("push"), encoding="utf-8")])
    ok(set(push.member_id) <= ids, "K14 push members known")
    mail = pd.read_csv(p("mail"), dtype=str, keep_default_na=False)
    ok(set(mail.addressee_member_id) <= ids, "K15 mail addressees known")
    ok(not mail.duplicated(["drop_code", "household_id"]).any(), "K16 one piece per household and drop")
    hmap = dict(zip(mem.member_id, mem.household_id))
    ok((mail.addressee_member_id.map(hmap) == mail.household_id).all(), "K17 the addressee lives in the household")
    spend = pq.read_table(p("spend")).to_pandas()
    red = pd.read_csv(p("redemptions"), sep=";", dtype=str, decimal=",")
    ok(set(spend.member_id) <= ids and set(spend.store_code) <= codes, "K18 spend keys")
    ok(set(red.member_id) <= ids and set(red.store_code) <= codes and red.receipt_id.is_unique, "K19 redemption keys")
    cal = pd.read_excel(p("calendar"), sheet_name=None)
    offers = cal["Erbjudanden"]
    ok(set(red.offer_code) <= set(offers["Offer code"]), "K20 redeemed offers are in the calendar")
    drops = set(cal["Utskick"]["Drop"])
    ok(set(mailings.mailing_id) <= drops and set(sms.campaign_ref) <= drops and set(push.notification_id) <= drops
       and set(mail.drop_code) <= drops, "K21 every drop is in the calendar")

    # ---------------------------------------------------------------- consent at the moment of sending
    snapd = {c: dict(zip(snap.member_id, snap[c] == "Y")) for c in ("email", "sms", "push", "post")}
    con["t"] = secs(_utc(con.event_time_utc))
    con = con.sort_values(["t", "event_id"], kind="mergesort")

    def replay(ch, q_member, q_t):
        """the state per the snapshot and the log, at each query"""
        e = con[con.channel == ch]
        st = dict(snapd[ch])
        et, em, ea = e.t.values, e.member_id.values, (e.action == "granted").values
        order = np.argsort(q_t, kind="mergesort")
        out = np.zeros(len(q_t), bool)
        j = 0
        for k in order:
            while j < len(et) and et[j] <= q_t[k]:
                st[em[j]] = ea[j]
                j += 1
            out[k] = st.get(q_member[k], False)
        return out

    s_t = secs(sends.sent_at).values
    ok(replay("email", sends.member_id.values, s_t).all(), "C1 every email went to a member with email consent")
    sms_t = secs(_loc(sms.submitted)).values
    ok(replay("sms", sms.customer_ref.values, sms_t).all(), "C2 every SMS went to a member with SMS consent")
    push_t = secs(_utc(push.sent_at)).values
    ok(replay("push", push.member_id.values, push_t).all(), "C3 every push went to a member with push consent")
    sel = {d: dt.datetime(s.year, s.month, s.day, 6, tzinfo=STO).timestamp() for d, c_, po, s, a, k in P.MAIL}
    ok(replay("post", mail.addressee_member_id.values, mail.drop_code.map(sel).values.astype(np.int64)).all(),
       "C4 every mail piece went to a main card holder with post consent on the selection date")
    # withdrawals from the email platform and the gateway reach the log within 15 minutes
    un = events[events.event_type.isin(["unsubscribe", "spam_complaint"])]
    y27 = int(dt.datetime(2027, 1, 1, tzinfo=dt.timezone.utc).timestamp())
    cw = con[(con.channel == "email") & con.source.isin(["esp_unsubscribe", "esp_complaint"]) & (con.t >= y27)]
    j = un.merge(cw, on="member_id")
    ea = secs(j.event_at)
    j = j[(j.t >= ea) & (j.t <= ea + 900)]
    ok(j.member_id.nunique() == un.member_id.nunique() == len(cw), "C5 email withdrawals logged within 15 minutes")
    stop = sms[sms.reply_text == "STOPP"]
    sw = con[(con.channel == "sms") & (con.source == "sms_stop") & (con.t >= y27)]
    ok(len(stop) == len(sw) and set(stop.customer_ref) == set(sw.member_id), "C6 STOPP replies logged")
    # no message after an unsubscribe or a hard bounce
    last_bad = pd.concat([un[["member_id", "event_at"]],
                          sends[sends.status == "hard_bounce"][["member_id", "sent_at"]].rename(
                              columns={"sent_at": "event_at"})]).groupby("member_id").event_at.min()
    after = sends[sends.member_id.isin(last_bad.index)]
    after = after[after.sent_at > after.member_id.map(last_bad)]
    regr = set(cw.member_id) & set(con[(con.channel == "email") & (con.action == "granted")].member_id)
    ok(after.member_id.isin(regr).all(), "C7 no email after an unsubscribe or hard bounce unless consent was given again")

    # ---------------------------------------------------------------- frequency and hours
    mk = sends.merge(mailings[["mailing_id", "type"]], on="mailing_id")
    mk = mk[mk.type != "automation"]
    lt = mk.sent_at.dt.tz_convert(STO)
    wk = lt.dt.isocalendar()
    ok(mk.groupby([mk.member_id, wk.year, wk.week]).size().max() <= 2, "F1 two marketing emails a week at most")
    sl = pd.to_datetime(sms.submitted)
    ok(sms.groupby([sms.customer_ref, sl.dt.month]).size().max() <= 2, "F2 two SMS a month at most")
    ok(sl.dt.hour.between(9, 18).all() and (sl.dt.weekday < 6).all(), "F3 SMS inside the sending hours")
    pl = _utc(push.sent_at).dt.tz_convert(STO)
    pw = pl.dt.isocalendar()
    ok(push.groupby([push.member_id, pw.year, pw.week]).size().max() <= 3, "F4 three pushes a week at most")
    ok(pl.dt.hour.between(8, 20).all(), "F5 push inside the sending hours")

    # ---------------------------------------------------------------- shopping, offers and tiers
    red["paid"] = red.receipt_total_sek.str.replace(",", ".").astype(float)
    red["disc"] = red.discount_sek.str.replace(",", ".").astype(float)
    red["month"] = red.redeemed_at.str[:7]
    g = red.groupby(["member_id", "store_code", "month"]).agg(n=("receipt_id", "size"), d=("disc", "sum"),
                                                              paid=("paid", "sum")).reset_index()
    s2 = spend.merge(g, on=["member_id", "store_code", "month"], how="left").fillna({"n": 0, "d": 0.0, "paid": 0.0})
    ok((s2.offers_redeemed == s2.n).all() and np.allclose(s2.offer_discount_sek, s2.d, atol=0.006),
       "S1 the warehouse's offer columns tie to the POS redemptions")
    ok(len(g.merge(spend, on=["member_id", "store_code", "month"])) == len(g), "S2 every redemption month is in spend")
    ok((s2.visits >= s2.offers_redeemed).all() and (s2.spend_sek >= s2.paid - 0.006).all() and (s2.visits > 0).all(),
       "S3 visits and amounts cover the redemption receipts")
    tot = spend.groupby("member_id").spend_sek.sum()
    t28 = np.where(tot >= P.GULD, "Guld", np.where(tot >= P.SILVER, "Silver", "Bas"))
    rule = pd.Series(t28, index=tot.index)
    opn = mem[mem.account_status == "open"].set_index("member_id")
    exp = rule.reindex(opn.index).fillna("Bas")
    ok((opn.tier_2028 == exp).all(), "S4 tier_2028 follows the rule on 2027 purchases")
    ok((mem[mem.account_status == "closed"].tier_2028 == "").all(), "S5 closed accounts carry no 2028 tier")
    jd = dict(zip(mem.member_id, mem.joined_date))
    cd = dict(zip(mem.member_id, mem.closed_date))
    sm = spend.member_id.map(jd).str[:7] <= spend.month
    ok(sm.all(), "S6 no purchases before joining")
    cl = spend.member_id.map(cd)
    ok(((cl == "") | (spend.month <= cl.str[:7])).all(), "S7 no purchases after closing")
    ofr = offers.set_index("Offer code")
    vf = pd.to_datetime(red.offer_code.map(ofr["Valid from"]))
    vt = pd.to_datetime(red.offer_code.map(ofr["Valid to"]))
    rd = pd.to_datetime(red.redeemed_at.str[:10])
    wel = red.offer_code == "BV27-02-O1"
    ok(((rd >= vf) & (rd <= vt))[~wel].all(), "S8 redemptions inside the offer's validity")
    wj = pd.to_datetime(red[wel].member_id.map(jd))
    ok(((rd[wel] >= wj) & (rd[wel] <= wj + pd.Timedelta(days=29))).all(), "S9 welcome offers inside 30 days of joining")
    g27 = set(mem[mem.tier_2027 == "Guld"].member_id)
    ok(set(red[red.offer_code == "BV27-12-O1"].member_id) <= g27, "S10 Guldveckan offers redeemed by Guld members")
    sp = spend.pivot_table(index="member_id", columns="month", values="visits", aggfunc="sum", fill_value=0)
    had = sp[[c for c in sp.columns if c <= "2027-05"]].sum(axis=1) > 0
    none = sp[[c for c in sp.columns if "2027-06" <= c <= "2027-08"]].sum(axis=1) == 0
    lapsed = set(sp.index[had & none])
    ok(set(red[red.offer_code == "BV27-10-O1"].member_id) <= lapsed, "S11 win-back offers redeemed by lapsed members")
    ok(set(sends[sends.mailing_id == "BV27-10-E1"].member_id) <= lapsed and
       set(sms[sms.campaign_ref == "BV27-10-S1"].customer_ref) <= lapsed, "S12 the win-back audience is the lapsed set")
    gm = mail[mail.drop_code == "BV27-13-D1"]
    hsp = spend[spend.month <= "2027-10"].assign(h=lambda x: x.member_id.map(hmap)).groupby("h").spend_sek.sum()
    ok((gm.household_id.map(hsp) >= 6000).all(), "S13 Julbrevet went to households over 6,000 SEK")

    # ---------------------------------------------------------------- Meta
    md = pd.read_csv(p("meta_daily"))
    ml = pd.read_csv(p("meta_life"))
    gd = md.groupby(["Campaign name", "Ad set name"]).agg(r=("Reach", "sum"), rmax=("Reach", "max"),
                                                          i=("Impressions", "sum"), s=("Amount spent (SEK)", "sum"),
                                                          c=("Link clicks", "sum"))
    jl = ml.set_index(["Campaign name", "Ad set name"]).join(gd)
    ok((jl.Reach <= jl.r).all() and (jl.Reach >= jl.rmax).all(), "M1 lifetime reach between the daily max and sum")
    ok((jl.Impressions == jl.i).all() and np.allclose(jl["Amount spent (SEK)"], jl.s, atol=0.02) and
       (jl["Link clicks"] == jl.c).all(), "M2 lifetime totals tie to the days")
    ok((md.Reach <= md.Impressions).all(), "M3 reach within impressions")

    # ---------------------------------------------------------------- realism sweep
    ns = sends[sends.mailing_id.str.startswith("BV27-01")].groupby("mailing_id").size()
    ok(ns.nunique() >= 0.9 * len(ns) and (ns.diff().iloc[1:] != 0).all(),
       "R1 newsletter issue sizes drift (no run of equal issues)")
    vm = spend.groupby("month").visits.sum()
    ok(vm.nunique() == 12 and (vm % 100 == 0).sum() <= 1 and (vm % 1000 != 0).all(),
       "R2 monthly visits differ and are not rounded (one total ending in 00 is chance)")
    ok(md["Amount spent (SEK)"].nunique() > 0.95 * len(md), "R3 daily spend is not a constant stream")
    ok(red.offer_code.value_counts().nunique() > 0.8 * red.offer_code.nunique(), "R4 redemption counts differ by offer")
    for k in ("members", "sms", "mail"):
        ok(not pd.read_csv(p(k), dtype=str).duplicated().any(), "R5 no repeated rows in %s" % F[k])
    pc = pd.read_csv(p("postcodes"))
    ok((pc.population % 100 != 0).sum() >= len(pc) - 2, "R6 postcode populations are not rounded")
    return N[0]
