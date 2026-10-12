"""The two asks from the shipped files, with the cracker's stops: second-pass hours (A) and the third-quarter residual
as each client's own audit counted it (C); the slide charts A."""
import datetime as dt
import json
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

import analysis as AN
import world as W

SID2 = AN.SID2
Q3A, Q3B = W.Q3
BASKET_STREAM = {v: W.SID[k] for k, v in W.SP_BASKET.items()}


# ----------------------------------------------------------------------------------------------- A, second-pass hours
def _sessions(target):
    return pd.read_csv(os.path.join(target, "second_pass_sessions_2026_09.csv"), dtype={"document_id": str})


def _families(target):
    sr = pd.read_csv(os.path.join(target, "stream_register.csv")).drop_duplicates("stream_code")
    return dict(zip(sr.stream_code, sr.form_family))


def doc_streams(target):
    """each document's stream from the first-pass log"""
    sp = pd.read_parquet(os.path.join(target, "first_pass_verifications_2026q3.parquet"), columns=["document_id", "stream_code"])
    sp = sp.drop_duplicates("document_id")
    return dict(zip(sp.document_id, sp.stream_code))


def family_rates(target, attribution="document", rework="all", L=None, ds=None):
    """minutes per document by form family: the seconds logged on a family's documents over the number of them.
    attribution: 'document' (the document's own stream) or 'basket' (the basket the session opened on);
    rework: 'all' (every line's seconds over distinct documents), 'dedupe' (first line per document only),
    'lines' (every line counted as a document)"""
    L = _sessions(target) if L is None else L.copy()
    fam = _families(target)
    if attribution == "document":
        ds = doc_streams(target) if ds is None else ds
        L["stream"] = L.document_id.map(ds)
    else:
        L["stream"] = L.basket.map(BASKET_STREAM)
    if L.stream.isna().any():
        raise AssertionError("session line without a stream")
    L["fam"] = L.stream.map(fam)
    if rework == "all":
        secs = L.groupby("fam").handling_sec.sum()
        n = L.drop_duplicates(["document_id", "fam"]).groupby("fam").size()
    elif rework == "dedupe":
        g = L.drop_duplicates("document_id", keep="first")
        secs = g.groupby("fam").handling_sec.sum()
        n = g.groupby("fam").size()
    elif rework == "lines":
        secs = L.groupby("fam").handling_sec.sum()
        n = L.groupby("fam").size()
    else:
        raise ValueError(rework)
    return (secs / 60.0 / n).to_dict()


def nov_docs(sc, one_version=False):
    pl = sc.plan.copy()
    if one_version:
        first = pl.sort_values("day").groupby("code").kfpd.first()
        pl["kfpd"] = pl.code.map(first)
        pl["docs"] = pl.kf / pl.kfpd
    return pl


def hours(target, sc, attribution="document", rework="all", one_version=False, unrounded=False, rates=None):
    rate = family_rates(target, attribution, rework) if rates is None else rates
    pl = nov_docs(sc, one_version)
    out = {}
    for c in W.ORDER:
        h = pl[pl.code == c].docs.sum() * rate[W.STREAMS[c]["family"]] / 60
        out[c] = h if unrounded else int(round(h))
    return out


def chart_order(H):
    return sorted(W.ORDER, key=lambda c: (-H[c], W.ORDER.index(c)))


# ----------------------------------------------------------------------------------------------- C, client audits
CAPTURE = {"KBA": {"D01", "D02", "D04"}, "NDS": {"KE", "KT"}, "BMC": {"DE-1", "DE-2"}, "HPB": {"E10", "E11"},
           "WBH": {"CAPT", "KEY"}, "CIP": {"C1"}, "WPC": {"DATA", "TRANS"}, "TCM": {"01", "02"}}


def _i(x, d=0):
    if x is None or x == "" or (isinstance(x, float) and np.isnan(x)):
        return d
    return int(x)


def _s(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    return str(x)


def _d(x):
    return pd.Timestamp(x).date()


def normalized_client_audits(target):
    """one row per finding round (or one row for a clean claim): client, claim reference, file, the client's received
    date, finding sequence, reason, review round"""
    f = lambda n: os.path.join(target, n)
    rows = []
    k = pd.read_csv(f("kessington_audit_findings_q3.csv"), dtype=str, keep_default_na=False)
    for r in k.itertuples(index=False):
        rows.append(dict(client="KBA", claim=r[0], file=r[1], received=_d(r[2]), seq=_i(r[4], 0), reason=r[5], rnd=_i(r[6], 1)))
    for sheet, c in (("Northgate", "NDS"), ("Brightmoor", "BMC"), ("Harbison", "HPB")):
        d = AN._xl(f("client_audits_us_q3.xlsx"), sheet)
        for r in d.itertuples(index=False):
            if c == "NDS":
                rows.append(dict(client=c, claim=r[0], file=r[1], received=_d(r[2]), seq=_i(r[3], 0), reason=_s(r[4]),
                                 rnd=2 if r[5] == "RE-REVIEWED" else 1, status=r[5]))
            elif c == "BMC":
                rows.append(dict(client=c, claim=r[0], file=r[1], received=_d(r[2]), seq=_i(r[3], 0),
                                 reason="" if r[4] == "CLEAN" else r[4], rnd=_i(r[5], 1)))
            else:
                rows.append(dict(client=c, claim=r[0], file=r[1], received=_d(r[2]), seq=_i(r[3], 0), reason=_s(r[4]),
                                 rnd=_i(r[5], 1)))
    for sheet, c in (("Wattlebird QA", "WBH"), ("Coolabah QA", "CIP")):
        d = AN._xl(f("client_audits_au_q3.xlsx"), sheet)
        for r in d.itertuples(index=False):
            rows.append(dict(client=c, claim=r[0], file=r[2], received=_d(r[3]), seq=_i(r[4], 0),
                             reason="" if r[5] == "NIL" else r[5], rnd=2 if r[6] == "Second review" else 1))
    js = json.load(open(f("client_portal_audits_uk_q3.json")))
    for rec in js["records"]:
        c = "WPC" if rec["insurer"].startswith("Whinfell") else "TCM"
        if not rec["findings"]:
            rows.append(dict(client=c, claim=rec["claim_ref"], file=rec["batch"], received=_d(rec["received_on"]), seq=0,
                             reason="", rnd=1))
        for fnd in rec["findings"]:
            rows.append(dict(client=c, claim=rec["claim_ref"], file=rec["batch"], received=_d(rec["received_on"]),
                             seq=fnd["n"], reason=fnd["code"], rnd=fnd["review"]))
    df = pd.DataFrame(rows)
    df["code"] = df.file.str.split("_").str[1].map(SID2)
    df["shift_day"] = pd.to_datetime(df.file.str.split("_").str[2], format="%Y%m%d").dt.date
    return df


def claim_documents(target):
    ix = pd.read_parquet(os.path.join(target, "delivery_index_2026q3.parquet"), columns=["file_name", "claim_ref", "document_id"])
    return ix.groupby(["file_name", "claim_ref"]).size()


def delivery_dates(target):
    """each file's delivery date in each client's zone, from the gateway's transmission time"""
    m = pd.read_csv(os.path.join(target, "delivery_manifests_2026q3.csv"))
    t = pd.to_datetime(m.transmitted_at, utc=True)
    out = {}
    for f, s, ts in zip(m.file_name, m.stream_code, t):
        c = W.STREAMS[SID2[s]]["client"]
        out[f] = ts.tz_convert(ZoneInfo(W.CLIENTS[c]["tz"])).date()
    return out


def _final(df):
    """a re-reviewed finding is replaced by its re-review"""
    f = df[df.seq > 0]
    last = f.groupby(["claim", "seq"]).rnd.transform("max")
    return f[f.rnd == last]


def client_audit_rates(target, df=None, docs=None, dd=None, clock="delivered", per_claim="index", rereview=True,
                       capture_only=True, unrounded=True):
    """per stream: capture findings per 1,000 key fields on sampled claims delivered in Q3 (client's zone).
    clock: 'delivered' (the gateway's transmission time in the client's zone), 'received' (the client's received
    business date), 'shift_day' (the file's shift date); per_claim: 'index' (key fields on every document of the
    claim, from the delivery index) or 'one' (one document per claim)"""
    df = normalized_client_audits(target) if df is None else df.copy()
    if clock == "delivered":
        dd = delivery_dates(target) if dd is None else dd
        df["ldate"] = df.file.map(dd)
    elif clock == "received":
        df["ldate"] = df.received
    elif clock == "shift_day":
        df["ldate"] = df.shift_day
    else:
        raise ValueError(clock)
    df = df[(df.ldate >= Q3A) & (df.ldate <= Q3B)]
    claims = df.drop_duplicates(["client", "claim"]).copy()
    kfpd = np.array([W.kfpd(c, d) for c, d in zip(claims.code, claims.shift_day)])
    if per_claim == "index":
        docs = claim_documents(target) if docs is None else docs
        nd = np.array([docs[(f, cl)] for f, cl in zip(claims.file, claims.claim)])
    else:
        nd = np.ones(len(claims), dtype=int)
    claims["kf"] = kfpd * nd
    den = claims.groupby("code").kf.sum()
    fin = _final(df) if rereview else df[df.seq > 0]
    if capture_only:
        fin = fin[[r in CAPTURE[c] for r, c in zip(fin.reason, fin.client)]]
    else:
        fin = fin[fin.reason != "WD"]
    num = fin.groupby("code").size().reindex(den.index, fill_value=0)
    out = (num / den * 1000).to_dict()
    return out if unrounded else {k: round(v, 2) for k, v in out.items()}


def ten_streams():
    return [c for c in W.ORDER if c != "D6"]


# ----------------------------------------------------------------------------------------------- both asks, stops, pair
def run(target, pk, sc):
    out = {}
    L = _sessions(target)
    ds = doc_streams(target)
    rates = {(a, r): family_rates(target, a, r, L=L, ds=ds) for a in ("document", "basket") for r in ("all", "dedupe", "lines")}
    out["rates"] = rates
    H = lambda a, r, **kw: hours(target, sc, rates=rates[(a, r)], **kw)
    out["A"] = {"golden": H("document", "all"), "basket": H("basket", "all"), "basket_dedupe": H("basket", "dedupe"),
                "basket_lines": H("basket", "lines"), "dedupe": H("document", "dedupe"), "lines": H("document", "lines"),
                "one_version": H("document", "all", one_version=True)}
    out["A_unrounded"] = H("document", "all", unrounded=True)
    df = normalized_client_audits(target)
    docs = claim_documents(target)
    dd = delivery_dates(target)
    C = lambda **kw: client_audit_rates(target, df=df, docs=docs, dd=dd, unrounded=False, **kw)
    out["C_unrounded"] = client_audit_rates(target, df=df, docs=docs, dd=dd)
    out["C"] = {"golden": C(), "one_doc": C(per_claim="one"), "received": C(clock="received"),
                "cracker_received": C(per_claim="one", clock="received"), "shift_day": C(clock="shift_day"),
                "no_rereview": C(rereview=False), "all_codes": C(capture_only=False)}
    out["order"] = chart_order(out["A"]["golden"])
    out["cracker_order"] = chart_order(out["A"]["basket"])
    # the pair simulation: the cracker landed the call, ran the battery and executed every filed rule (each
    # document counted once, the quarter by delivery date in the client's zone, capture codes, re-reviews)
    rows = []
    for c in W.ORDER:
        rows.append(("A", c, out["A"]["basket"][c] != out["A"]["golden"][c]))
    for c in ten_streams():
        rows.append(("C", c, out["C"]["one_doc"][c] != out["C"]["golden"][c]))
    rows.append(("chart", "series", all(out["A"]["basket"][c] != out["A"]["golden"][c] for c in W.ORDER)))
    rows.append(("chart", "order", out["cracker_order"] != out["order"]))
    rows.append(("chart", "title", out["cracker_order"][0] != out["order"][0]))
    out["cracker_rows"] = rows
    n = len(rows)
    hits = sum(1 for r in rows if not r[2])
    Lk = hits / n
    r = 6.0
    out["pair_ceiling_measured"] = ((38 + 7 + 55 * Lk) + (r + 7 + 55 * Lk)) / 2
    out["pair_ceiling_allowance"] = ((38 + 7 + 55 * max(Lk, 0.10)) + (r + 7 + 55 * max(Lk, 0.10))) / 2
    return out
