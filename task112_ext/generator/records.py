"""The pack's data files, cut from the world as each source system exports them."""
import csv
import datetime as dt
import json
import os

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import params as P
import world as W

FILES = {
    "members": "crm_members_extract_2028-01-08.csv",
    "snapshot": "consent_snapshot_2026-01-01.csv",
    "consent": "consent_events_2026-2027.csv",
    "calendar": "campaign_calendar_2027.xlsx",
    "mailings": "esp_mailings_2027.csv",
    "sends": "esp_sends_2027.parquet",
    "events": "esp_events_2027.parquet",
    "sms": "sms_gateway_log_2027.csv",
    "push": "app_push_log_2027.jsonl",
    "mail": "direct_mail_drops_2027.csv",
    "meta_daily": "meta_ads_daily_2027.csv",
    "meta_life": "meta_ads_lifetime_2027.csv",
    "spend": "member_store_month_2027.parquet",
    "redemptions": "pos_offer_redemptions_2027.csv",
    "stores": "stores.csv",
    "postcodes": "postcode_areas.csv",
    "policy": "contact_policy_v2.pdf",
    "mediaplan": "media_plan_2027.pdf",
    "dictionary": "DATA_DICTIONARY.md",
    "manifest": "export_manifest.csv",
}


def _iso_utc(t):
    return dt.datetime.fromtimestamp(int(t), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _local(t, fmt="%Y-%m-%d %H:%M:%S"):
    return dt.datetime.fromtimestamp(int(t), W.STO).strftime(fmt)


def _iso_off(t):
    return dt.datetime.fromtimestamp(int(t), W.STO).isoformat()


def _csv(path, header, rows, sep=",", quote=csv.QUOTE_MINIMAL):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh, delimiter=sep, quoting=quote, lineterminator="\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(["" if x is None else x for x in r])
    return len(rows)


def _yn(b):
    return "Y" if b else "N"


def _parquet(path, cols):
    """the warehouse's export settings: zstd pages, dictionaries for text, delta encoding for ids, counts and times"""
    t = pa.table(cols)
    t = t.replace_schema_metadata(None)
    text = [f.name for f in t.schema if pa.types.is_string(f.type)]
    delta = {f.name: "DELTA_BINARY_PACKED" for f in t.schema
             if pa.types.is_integer(f.type) or pa.types.is_timestamp(f.type)}
    pq.write_table(t, path, compression="zstd", use_dictionary=text, column_encoding=delta, write_statistics=True,
                   row_group_size=250000)
    return t.num_rows


# ------------------------------------------------------------------ CRM and consent
def members(w, path):
    y27 = w.paid.sum(axis=0)
    open_end = ~(w.closed & (w.close_day <= np.datetime64("2027-12-31")))
    t28 = np.where(y27 >= P.GULD, "Guld", np.where(y27 >= P.SILVER, "Silver", "Bas"))
    rows = []
    for i in np.argsort(w.mid):
        rows.append((w.mid[i], w.card[i], w.hid[w.hh[i]], str(w.join[i]), w.signup[i], w.home[i], w.pc[i], w.muni[i],
                     int(w.birth[i]), _yn(w.has_email[i]), _yn(w.has_mobile[i]),
                     str(w.app_since[i]) if w.app[i] else "", w.tier27[i], t28[i] if open_end[i] else "",
                     "open" if open_end[i] else "closed", "" if open_end[i] else str(w.close_day[i])))
    return _csv(path, ["member_id", "card_number", "household_id", "joined_date", "signup_channel", "home_store",
                       "postcode_area", "municipality", "birth_year", "email_on_file", "mobile_on_file",
                       "app_registered_date", "tier_2027", "tier_2028", "account_status", "closed_date"], rows)


def snapshot(w, path):
    rows = []
    for i in np.argsort(w.mid):
        if w.join_ts[i] < w.live:
            rows.append((w.mid[i], _yn(w.init["email"][i]), _yn(w.init["sms"][i]), _yn(w.init["push"][i]),
                         _yn(w.init["post"][i])))
    return _csv(path, ["member_id", "email", "sms", "push", "post"], rows)


def consent(w, path):
    ev = []
    for c in W.CH:
        for ts, i, g, src in w.cons[c].log:
            ev.append((ts, w.mid[i], W.CH.index(c), c, "granted" if g else "withdrawn", src))
    ev.sort(key=lambda z: (z[0], z[1], z[2]))
    rows = [(k + 1, m, c, a, _iso_utc(ts), src) for k, (ts, m, _, c, a, src) in enumerate(ev)]
    return _csv(path, ["event_id", "member_id", "channel", "action", "event_time_utc", "source"], rows)


# ------------------------------------------------------------------ email
def mailings(w, path):
    rows = []
    for m in w.mailings:
        rows.append((m["mailing_id"], m["campaign_code"], m["type"], m["subject"], _iso_utc(m["scheduled"]), m["sends"]))
    for s, (wid, off, subj) in enumerate(P.WELCOME):
        rows.append((wid, "BV27-02", "automation", subj, "", w.welcome_sent[s]))
    rows.sort(key=lambda z: z[0])
    return _csv(path, ["mailing_id", "campaign_code", "type", "subject", "scheduled_utc", "sends"], rows)


def sends(w, path):
    ids = np.concatenate([s[0] for s in w.sends])
    mail = np.concatenate([s[1] for s in w.sends]).astype(str)
    who = np.concatenate([s[2] for s in w.sends])
    t = np.concatenate([s[3] for s in w.sends])
    st = np.concatenate([s[4] for s in w.sends]).astype(str)
    o = np.lexsort((ids, t))
    return _parquet(path, {"send_id": pa.array(ids[o], pa.int64()), "mailing_id": pa.array(mail[o]),
                           "member_id": pa.array(w.mid[who[o]]),
                           "sent_at": pa.array(t[o], pa.timestamp("s", tz="UTC")), "status": pa.array(st[o])})


def events(w, path):
    sid = np.concatenate([e[0] for e in w.events])
    mail = np.concatenate([e[1] for e in w.events]).astype(str)
    who = np.concatenate([e[2] for e in w.events])
    t = np.concatenate([e[3] for e in w.events])
    typ = np.concatenate([e[4] for e in w.events]).astype(str)
    cl = np.concatenate([e[5] for e in w.events])
    lk = np.concatenate([e[6] for e in w.events])
    rank = np.array([{"open": 0, "click": 1, "unsubscribe": 2, "spam_complaint": 3}[x] for x in typ])
    o = np.lexsort((rank, sid, t))
    return _parquet(path, {"event_id": pa.array(np.arange(1, len(o) + 1) + 7340000, pa.int64()),
                           "send_id": pa.array(sid[o], pa.int64()), "mailing_id": pa.array(mail[o]),
                           "member_id": pa.array(w.mid[who[o]]), "event_type": pa.array(typ[o]),
                           "event_at": pa.array(t[o], pa.timestamp("s", tz="UTC")),
                           "client": pa.array(list(cl[o]), pa.string()), "link": pa.array(list(lk[o]), pa.string())})


# ------------------------------------------------------------------ SMS, push, mail
def sms(w, path):
    rows = []
    for sid, who, sub, st, done, seg, price, stop, rt in w.sms:
        for j in range(len(who)):
            i = who[j]
            rows.append((int(sub[j]), W.hexid("sms", sid, w.mid[i], n=18).lower(), "Brannvik", sid, w.mid[i],
                         w.operator[i], _local(sub[j]), st[j], _local(done[j]), seg, "%.2f" % price[j],
                         "STOPP" if stop[j] else "", _local(rt[j]) if stop[j] else ""))
    rows.sort(key=lambda z: (z[0], z[1]))
    return _csv(path, ["message_id", "sender", "campaign_ref", "customer_ref", "operator", "submitted", "status",
                       "status_time", "segments", "price_sek", "reply_text", "reply_time"], [r[1:] for r in rows])


def push(w, path):
    out = []
    for pid, camp, title, who, sent, st, reason, op, opt in w.push:
        for j in range(len(who)):
            i = who[j]
            x = {"notification_id": pid, "member_id": w.mid[i], "platform": "ios" if w.ios[i] else "android",
                 "sent_at": _iso_off(sent[j]), "status": st[j]}
            if reason[j]:
                x["failure_reason"] = reason[j]
            if op[j]:
                x["opened_at"] = _iso_off(opt[j])
            out.append((int(sent[j]), pid, w.mid[i], json.dumps(x, ensure_ascii=False, separators=(",", ":"))))
    out.sort(key=lambda z: (z[0], z[1], z[2]))
    with open(path, "w", encoding="utf-8", newline="") as fh:
        for x in out:
            fh.write(x[3] + "\n")
    return len(out)


def mail(w, path):
    rows = []
    for did, camp, prim, ver, posted, ret, retd in w.mail:
        for j in range(len(prim)):
            i = prim[j]
            rows.append((did, w.hid[w.hh[i]], w.mid[i], w.pc[i], ver[j], str(posted),
                         str(posted + dt.timedelta(days=int(retd[j]))) if ret[j] else ""))
    rows.sort(key=lambda z: (z[0], z[3], z[1]))
    return _csv(path, ["drop_code", "household_id", "addressee_member_id", "postcode_area", "version", "posted_date",
                       "returned_date"], rows)


# ------------------------------------------------------------------ Meta
def meta_daily(w, path):
    rows = []
    for d, cname, aset, reach, imp, spent, clk in w.meta_daily:
        rows.append((str(d), str(d), cname, aset, reach, imp, "%.6f" % (imp / reach), "%.2f" % spent, clk,
                     "%.2f" % (spent / imp * 1000)))
    return _csv(path, ["Reporting starts", "Reporting ends", "Campaign name", "Ad set name", "Reach", "Impressions",
                       "Frequency", "Amount spent (SEK)", "Link clicks", "CPM (cost per 1,000 impressions) (SEK)"],
                rows, quote=csv.QUOTE_ALL)


def meta_life(w, path):
    rows = []
    for a, b, cname, aset, reach, imp, spent, clk in w.meta_life:
        rows.append((str(a), str(b), cname, aset, reach, imp, "%.6f" % (imp / reach), "%.2f" % spent, clk,
                     "%.2f" % (spent / imp * 1000)))
    return _csv(path, ["Reporting starts", "Reporting ends", "Campaign name", "Ad set name", "Reach", "Impressions",
                       "Frequency", "Amount spent (SEK)", "Link clicks", "CPM (cost per 1,000 impressions) (SEK)"],
                rows, quote=csv.QUOTE_ALL)


# ------------------------------------------------------------------ shopping and redemptions
def spend(w, path):
    rows = sorted(w.spend_rows, key=lambda z: (z[1], w.mid[z[0]], z[2]))
    return _parquet(path, {
        "member_id": pa.array([w.mid[z[0]] for z in rows]),
        "month": pa.array(["2027-%02d" % z[1] for z in rows]),
        "store_code": pa.array([z[2] for z in rows]),
        "visits": pa.array([z[3] for z in rows], pa.int32()),
        "spend_sek": pa.array([z[4] for z in rows], pa.float64()),
        "offer_discount_sek": pa.array([z[5] for z in rows], pa.float64()),
        "offers_redeemed": pa.array([z[6] for z in rows], pa.int32())})


def _sv(x):
    return ("%.2f" % x).replace(".", ",")


def redemptions(w, path):
    rows = sorted(w.redemptions, key=lambda z: (z[0], z[3], w.mid[z[1]], z[2]))
    seq = {}
    out = []
    base = {s["store_code"]: 20000 + int(W.hexid("rcpt", s["store_code"], n=4), 16) % 30000 for s in w.stores}
    for ts, i, code, store, paid, disc in rows:
        seq[store] = seq.get(store, 0) + 1 + int(W.hexid(ts, i, n=2), 16) % 9
        out.append(("%s-%06d" % (store, base[store] + seq[store] * 7), w.mid[i], code, store,
                    _local(ts, "%Y-%m-%d %H:%M"), _sv(paid), _sv(disc)))
    return _csv(path, ["receipt_id", "member_id", "offer_code", "store_code", "redeemed_at", "receipt_total_sek",
                       "discount_sek"], out, sep=";")


# ------------------------------------------------------------------ lookups
def stores(w, path):
    rows = [(s["store_code"], s["store_name"], s["municipality"], s["county"], s["postcode_area"], s["format"],
             s["sales_area_sqm"], s["opened_year"]) for s in w.stores]
    return _csv(path, ["store_code", "store_name", "municipality", "county", "postcode_area", "format",
                       "sales_area_sqm", "opened_year"], rows)


def postcodes(w, path):
    r = np.random.default_rng(P.SEED + 70)
    rows = []
    for m, (cl, county, pcs, pop, code) in P.MUNIS.items():
        pop = pop + int(r.integers(-49, 50))
        sh = r.dirichlet(np.full(len(pcs), 6.0)) if len(pcs) > 1 else np.array([1.0])
        pp = np.round(sh * pop).astype(int)
        pp[-1] = pop - pp[:-1].sum()
        for pc, x in zip(pcs, pp):
            rows.append((pc, m, code, county, int(x), int(round(x / r.uniform(1.98, 2.22)))))
    rows.sort(key=lambda z: z[0])
    return _csv(path, ["postcode_area", "municipality", "municipality_code", "county", "population",
                       "households"], rows)


def write_all(w, target):
    p = lambda k: os.path.join(target, FILES[k])
    n = {}
    for k, f in [("members", members), ("snapshot", snapshot), ("consent", consent), ("mailings", mailings),
                 ("sends", sends), ("events", events), ("sms", sms), ("push", push), ("mail", mail),
                 ("meta_daily", meta_daily), ("meta_life", meta_life), ("spend", spend),
                 ("redemptions", redemptions), ("stores", stores), ("postcodes", postcodes)]:
        n[k] = f(w, p(k))
    return n
