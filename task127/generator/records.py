"""The pack's data files, written from the world as each system records it."""
from __future__ import annotations

import csv
import datetime as dt
import math

import numpy as np

import common as K
import world as W


def _local(day: float) -> dt.datetime:
    return K.at(day)


def _us(day: float) -> str:
    d = _local(day)
    return "%02d/%02d/%04d" % (d.month, d.day, d.year)


def _iso_date(day: float) -> str:
    return _local(day).strftime("%Y-%m-%d")


def _writer(path, header):
    fh = open(path, "w", newline="", encoding="utf-8")
    w = csv.writer(fh, lineterminator="\r\n")
    w.writerow(header)
    return fh, w


# ------------------------------------------------------------------ the legacy system

LEGACY_DISP = {"SETTLED": "ST", "WITHDRAWN": "WD", "DENIED": "DN", "NO_INJURY": "NI", "DUPLICATE": "XD"}


def legacy_rows(feats):
    """One archive row per legacy feature: closed in the legacy era with its last closing reason, or CV when it was
    still open at the conversion weekend."""
    rows = []
    for f in feats:
        if f.system != "legacy":
            continue
        claim, feat = f.legacy_key.rsplit("-", 1)
        if f.converted:
            cls, disp = K.day(K.CUTOVER), "CV"
        else:
            last = [c for c in f.closings if c[0] < W.CUT][-1]
            cls, disp = last[0], LEGACY_DISP[last[1]]
        rows.append((claim, feat, f.state, "BI", _us(f.acc), _us(f.rep), _us(cls), disp, f.reopen_ct_legacy, f.created))
    rows.sort(key=lambda r: (r[9], r[0], r[1]))
    return rows


def write_legacy_claims(path, feats):
    fh, w = _writer(path, ["CLM_NO", "FEAT_NO", "ST", "COV", "LOSS_DT", "RPT_DT", "CLS_DT", "DISP", "REOPEN_CT"])
    n = 0
    for r in legacy_rows(feats):
        w.writerow(r[:9])
        n += 1
    fh.close()
    return n


def legacy_payments(feats):
    """Every payment and void the legacy system booked before the platform went live, by transaction date."""
    rows = []
    chk = [400118]
    wire = [20311]
    for f in feats:
        if f.legacy_key is None:
            continue
        for k, p in enumerate(f.pays):
            if p[0] >= W.LIVE:
                continue
            on = f.paid_on[0] if (f.paid_on is not None and k == f.paid_on[1]) else f
            claim, feat = on.legacy_key.rsplit("-", 1)
            payee = {"CLAIMANT": "CLMT", "ATTORNEY": "ATTY", "LIENHOLDER": "LIEN"}[p[3]]
            rows.append([p[0], claim, feat, _us(f.acc), p[2], payee, p[1], p[4]])
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = []
    for t, claim, feat, loss, method, payee, amt, void in rows:
        if method == "CHECK":
            chk[0] += 1
            ref = "%07d" % chk[0]
        else:
            wire[0] += 1
            ref = "W%06d" % wire[0]
        out.append((t, claim, feat, loss, _us(t), "PAY", ref, "CHK" if method == "CHECK" else "WIR", payee,
                    "%.2f" % amt))
        if void is not None and void < W.LIVE:
            out.append((void, claim, feat, loss, _us(void), "VOID", ref, "CHK", payee, "%.2f" % -amt))
    out.sort(key=lambda r: (r[0], r[6], r[5]))
    return out


def write_legacy_payments(path, feats):
    fh, w = _writer(path, ["CLM_NO", "FEAT_NO", "LOSS_DT", "TRANS_DT", "TRANS_CD", "CHECK_NO", "PAY_METHOD",
                           "PAYEE_TYPE", "AMOUNT"])
    rows = legacy_payments(feats)
    for r in rows:
        w.writerow(r[1:])
    fh.close()
    return len(rows)


# ------------------------------------------------------------------ the claims platform

def platform_events(f):
    """The platform's event history for a feature, up to the extract's run: (day, event, disposition). A converted
    feature's history starts at its conversion; a legacy feature re-entered after it reopened starts with that
    reopening; a platform feature starts at its creation."""
    if f.system == "platform":
        ev, hist = [(f.created, "CREATED", "")], f.closings
    elif f.converted:
        ev, hist = [(f.entered, "CONVERTED", "")], [c for c in f.closings if c[0] >= W.CUT]
    elif f.recreated:
        ev, hist = [(f.entered, "REOPENED", "")], [c for c in f.closings if c[0] > f.entered]
    else:
        return []
    for close, disp, reopen in hist:
        ev.append((close, "CLOSED", disp))
        if reopen is not None:
            ev.append((reopen, "REOPENED", ""))
    return [e for e in ev if e[0] <= W.RUN]


def platform_rows(feats):
    rows = []
    for f in feats:
        if f.platform_id is None or f.entered > W.RUN:
            continue
        ev = platform_events(f)
        closes = [e for e in ev if e[1] == "CLOSED"]
        reopens = [e for e in ev if e[1] == "REOPENED"]
        last = ev[-1]
        status = "CLOSED" if last[1] == "CLOSED" else ("REOPENED" if reopens else "OPEN")
        rows.append(dict(
            feature_id=f.platform_id, claim_number=f.claim_no, legacy_ref=f.legacy_key or "",
            coverage="BI", state=f.state, accident_date=_iso_date(f.acc), reported_date=_iso_date(f.rep),
            created_at=K.utc_text(f.entered), status=status,
            closed_at=K.utc_text(closes[-1][0]) if closes else "",
            reopened_at=K.utc_text(reopens[-1][0]) if reopens else "",
            disposition=closes[-1][2] if closes else "", _t=f.entered, _ev=ev, _f=f))
    rows.sort(key=lambda r: (r["_t"], r["feature_id"]))
    return rows


FEATURE_COLS = ["feature_id", "claim_number", "legacy_ref", "coverage", "state", "accident_date", "reported_date",
                "created_at", "status", "closed_at", "reopened_at", "disposition"]


def write_platform_features(path, rows):
    fh, w = _writer(path, FEATURE_COLS)
    for r in rows:
        w.writerow([r[c] for c in FEATURE_COLS])
    fh.close()
    return len(rows)


def write_platform_events(path, rows):
    out = []
    for r in rows:
        for t, e, disp in r["_ev"]:
            out.append((t, r["feature_id"], e, disp))
    out.sort(key=lambda x: (x[0], x[1]))
    seq = 5120000
    fh, w = _writer(path, ["event_id", "feature_id", "event", "event_at", "disposition"])
    for t, fid, e, disp in out:
        seq += 1
        w.writerow(["E%08d" % seq, fid, e, K.utc_text(t), disp])
    fh.close()
    return len(out)


def platform_payments(feats):
    """Payments the platform issued from going live to the extract's run, with voids and reissues."""
    rows = []
    for f in feats:
        if f.platform_id is None:
            continue
        idx = {}
        for k, p in enumerate(f.pays):
            if p[0] < W.LIVE or p[0] > W.RUN:
                continue
            idx[k] = len(rows)
            on = f.paid_on[0] if (f.paid_on is not None and k == f.paid_on[1]) else f
            rows.append(dict(_t=p[0], _k=k, _f=f, feature_id=on.platform_id, claim_number=f.claim_no,
                             issued=p[0], method=p[2], payee=p[3], cents=int(round(p[1] * 100)),
                             void=p[4] if (p[4] is not None and p[4] <= W.RUN) else None, reissue_of=p[5]))
    rows.sort(key=lambda r: (r["_t"], r["feature_id"], r["_k"]))
    seq = 88200000
    ids = {}
    for r in rows:
        seq += 1 + (r["cents"] % 3)
        r["payment_id"] = "P%09d" % seq
        ids[(id(r["_f"]), r["_k"])] = r["payment_id"]
    for r in rows:
        r["reissue_ref"] = ids.get((id(r["_f"]), r["reissue_of"]), "") if r["reissue_of"] is not None else ""
    return rows


def write_platform_payments(path, rows):
    fh, w = _writer(path, ["payment_id", "feature_id", "claim_number", "issued_at", "method", "payee_type",
                           "amount_cents", "status", "voided_at", "reissue_of"])
    for r in rows:
        w.writerow([r["payment_id"], r["feature_id"], r["claim_number"], K.utc_text(r["issued"]), r["method"],
                    r["payee"], r["cents"], "VOIDED" if r["void"] is not None else "ISSUED",
                    K.utc_text(r["void"]) if r["void"] is not None else "", r["reissue_ref"]])
    fh.close()
    return len(rows)


# ------------------------------------------------------------------ the ledger

PD_WIRE = 96250.00                       # a vehicle-damage wire Treasury booked to 5311 in its December 2025 journal
FEED_OUTAGE = dt.date(2026, 5, 19)       # that night's feed failed; the next night posted both days
REPLAY_OF = dt.date(2026, 8, 13)         # the batch for this day was sent again the night after its own


def _ldate(day: float) -> dt.date:
    return K.at(day).date()


def value_date(day: float) -> dt.date:
    """A wire's bank value date: the day it is released, or the next business day when it is released after the
    bank's 15:00 cutoff."""
    t = K.at(day)
    d = t.date()
    if t.hour >= 15:
        d = W.next_business(d + dt.timedelta(days=1))
    return d


def ledger(pay_rows):
    """Account 5311 (losses paid, auto bodily injury) for 2026: the nightly claims feed, Treasury's monthly wire
    journals and two manual journals."""
    checks, wires = {}, {}
    for r in pay_rows:
        st = r["_f"].state
        if r["method"] == "CHECK":
            d = _ldate(r["issued"])
            checks[(d, st)] = checks.get((d, st), 0) + r["cents"]
            if r["void"] is not None:
                v = _ldate(r["void"])
                checks[(v, st)] = checks.get((v, st), 0) - r["cents"]
        else:
            v = value_date(r["issued"])
            m = (v.year, v.month)
            wires[(m, st)] = wires.get((m, st), 0) + r["cents"]
    lines = []
    batch = [31750]
    d = dt.date(2025, 12, 31)
    while d <= dt.date(2026, 12, 30):
        run = d + dt.timedelta(days=1)
        covered = [d]
        if d == FEED_OUTAGE:
            d += dt.timedelta(days=1)
            continue
        if d == FEED_OUTAGE + dt.timedelta(days=1):
            covered = [FEED_OUTAGE, d]
        for day in covered:
            batch[0] += 1
            ref = "CFB%07d" % batch[0]
            for st in K.STATES:
                amt = checks.get((day, st), 0)
                if amt:
                    lines.append(dict(posting_date=run, source="CLAIMS FEED", batch_ref=ref, state=st,
                                      description="Claims platform payments feed", cents=amt, _cover=day, _kind="feed"))
            if day == REPLAY_OF:
                pass
        if run == REPLAY_OF + dt.timedelta(days=2):
            batch[0] += 1
            ref = "CFB%07d" % batch[0]
            for st in K.STATES:
                amt = checks.get((REPLAY_OF, st), 0)
                if amt:
                    lines.append(dict(posting_date=run, source="CLAIMS FEED", batch_ref=ref, state=st,
                                      description="Claims platform payments feed", cents=amt, _cover=REPLAY_OF,
                                      _kind="replay"))
        d += dt.timedelta(days=1)
    for (y, m) in [(2025, 12)] + [(2026, k) for k in range(1, 12)]:
        ny, nm = (y + 1, 1) if m == 12 else (y, m + 1)
        post = W.nth_business_day(ny, nm, 3)
        for st in K.STATES:
            amt = wires.get(((y, m), st), 0)
            extra = int(round(PD_WIRE * 100)) if ((y, m) == (2025, 12) and st == "NE") else 0
            if amt or extra:
                lines.append(dict(posting_date=post, source="TREASURY", batch_ref="TRW%02d%02d" % (y % 100, m),
                                  state=st, description="Claims wire settlements", cents=amt + extra,
                                  _cover=(y, m), _kind="wire", _pd=extra))
    # two feed lines the ledger rejected for a missing state segment, reposted by Finance the next day
    for run, st, ref in ((dt.date(2026, 4, 1), "NE", "JE-2026-0381"), (dt.date(2026, 10, 1), "SD", "JE-2026-1019")):
        hit = [l for l in lines if l["posting_date"] == run and l["state"] == st and l["_kind"] == "feed"]
        for l in hit:
            lines.remove(l)
            lines.append(dict(posting_date=run + dt.timedelta(days=1), source="MANUAL", batch_ref=ref, state=st,
                              description="Repost claims feed line rejected %s (state segment missing)" %
                                          run.strftime("%d %b").lstrip("0"),
                              cents=l["cents"], _cover=l["_cover"], _kind="repost"))
    lines.append(dict(posting_date=dt.date(2026, 4, 16), source="MANUAL", batch_ref="JE-2026-0417", state="NE",
                      description="Reclass to 5312: wire settlement booked to 5311 in error",
                      cents=-int(round(PD_WIRE * 100)), _kind="reclass"))
    replay = [l for l in lines if l["_kind"] == "replay"]
    for l in replay:
        lines.append(dict(posting_date=dt.date(2026, 10, 6), source="MANUAL", batch_ref="JE-2026-1032",
                          state=l["state"], description="Reverse claims feed posting, ticket FIN-2291",
                          cents=-l["cents"], _kind="reversal"))
    lines.sort(key=lambda l: (l["posting_date"], {"CLAIMS FEED": 0, "TREASURY": 1, "MANUAL": 2}[l["source"]],
                              l["batch_ref"], K.STATES.index(l["state"])))
    return lines


def write_ledger(path, lines):
    fh, w = _writer(path, ["journal_id", "line", "posting_date", "period", "account", "source", "batch_ref", "state",
                           "description", "amount"])
    jn = 0
    last = None
    ln = 0
    for l in lines:
        key = (l["posting_date"], l["batch_ref"])
        if key != last:
            jn += 1
            ln = 0
            last = key
        ln += 1
        w.writerow(["J26%06d" % (40000 + jn * 7), ln, l["posting_date"].isoformat(),
                    l["posting_date"].strftime("%Y-%m"), "5311", l["source"], l["batch_ref"], l["state"],
                    l["description"], "%.2f" % (l["cents"] / 100.0)])
    fh.close()
    return len(lines)


# ------------------------------------------------------------------ distractors

def write_exposure(path, seed=K.SEED):
    rng = np.random.default_rng(seed + 7)
    fh, w = _writer(path, ["quarter", "state", "earned_car_years"])
    n = 0
    for i in range(K.N_AQ):
        tot = 150000.0 * K.GROWTH ** (i / 4.0) * (1.0 + 0.004 * rng.normal())
        for st, sh in zip(K.STATES, K.STATE_SHARE):
            w.writerow([K.aq_label(i).replace(" ", ""), st, "%.1f" % (tot * sh * (1.0 + 0.01 * rng.normal()))])
            n += 1
    fh.close()
    return n


def write_pd(path, seed=K.SEED):
    """Motor property damage paid by accident quarter and development quarter, a reserving extract of another line."""
    rng = np.random.default_rng(seed + 11)
    pattern = [0.62, 0.90, 0.965, 0.985, 0.993, 0.997, 0.999, 1.0]
    fh, w = _writer(path, ["accident_quarter", "development_quarter", "cumulative_paid_usd"])
    n = 0
    for i in range(K.N_AQ):
        ult = 21.5e6 * K.GROWTH ** (i / 4.0) * 1.04 ** (i / 4.0) * (1.0 + 0.03 * rng.normal())
        for j in range(K.N_AQ - i):
            share = pattern[min(j, len(pattern) - 1)] * (1.0 + (0.01 * rng.normal() if j < 3 else 0.0))
            w.writerow([K.aq_label(i).replace(" ", ""), j + 1, "%.2f" % (ult * min(share, 1.0))])
            n += 1
    fh.close()
    return n
