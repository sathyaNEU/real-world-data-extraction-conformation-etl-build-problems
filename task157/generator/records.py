"""task157 (architecture 2) shipped records: the fifteen recorders' consolidated returns, the correction
notices, the two voter file snapshots, the office's sheet index and receipt log, the firms' own delivery
manifests, the March list-maintenance run, and the two files the solution never reads.

Every file carries the conventions the system that writes it carries: the recorders' returns keep each
county's own date format and Navajo County's own 2019 disposition codes, the snapshots carry UTC status
stamps against local signing dates, the firms count the sheets they handed over rather than the sheets the
office receipted, and sheet numbers are each firm's own so a sheet is identified by its circulator's
registration number and its number together."""
from __future__ import annotations

import datetime as dt
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402
import world as WD      # noqa: E402

F_RETURNS = "county_verification_returns_2028.csv"
F_CORR = "county_return_corrections_2028.csv"
F_SNAP_EARLY = "avid_snapshot_extract_20271220.csv"
F_SNAP_LATE = "avid_snapshot_extract_20280710.csv"
F_SHEETS = "petition_sheet_index_2028.csv"
F_RECEIPT = "petition_receipt_log_2028.csv"
F_MANIFEST = "circulator_sheet_submissions_2028.csv"
F_MAINT = "list_maintenance_run_20280314.csv"
F_CIRC = "circulator_registration_extract_i18-2028.csv"
F_CLOSEOUT = "measure_i2024-04_full_count_closeout.xlsx"
F_OTHER = "measure_i2028-04_receipt_log.csv"            # distractor
F_REGSTATS = "voter_registration_by_county_20280701.csv"  # distractor

RETURNS_COLS = ["county_code", "return_id", "return_received_utc", "circulator_reg_no", "sheet_no",
                "line_no", "signature_date", "voter_reg_id", "disposition_code", "determined_by",
                "determination_date"]
CORR_COLS = ["correction_id", "county_code", "circulator_reg_no", "sheet_no", "line_no",
             "prior_disposition_code", "corrected_disposition_code", "corrected_on", "query_code"]
SNAP_COLS = ["snapshot_date", "voter_reg_id", "county_code", "registration_status", "registration_date",
             "status_changed_utc", "cancellation_date", "cancellation_reason", "precinct_code"]
SHEET_COLS = ["sheet_serial", "bundle_id", "receipt_date", "circulator_reg_no", "sheet_no",
              "signature_lines", "county_circulated"]
RECEIPT_COLS = ["bundle_id", "received_date", "received_utc", "sheets_presented", "sheets_accepted",
                "sheets_rejected", "signature_lines_accepted", "rejection_code", "receipted_by"]
CIRC_COLS = ["circulator_reg_no", "circulator_type", "registering_firm", "firm_registration_no",
             "county_of_residence", "registered_on", "withdrawn_on", "registration_status"]
MANIFEST_COLS = ["manifest_no", "firm_name", "firm_registration_no", "delivered_date", "sheets_submitted",
                 "signatures_claimed", "office_bundle_ref"]
MAINT_COLS = ["run_id", "run_date", "voter_reg_id", "county_code", "action_code", "reason_code",
              "notice_mailed", "posted_utc"]
OTHER_COLS = ["bundle_id", "received_date", "firm_code", "sheets_presented", "sheets_accepted",
              "signature_lines_accepted", "receipted_by"]
REGSTATS_COLS = ["report_date", "county_code", "county_name", "party_code", "active_registrations",
                 "inactive_registrations"]

CANCEL_REASON = {0: "", 1: "LM-NOTICE", 2: "MOVED-OUT", 3: "DECEASED", 4: "VOTER-REQUEST"}
QUERY_CODES = ["ADDR-REREAD", "SIG-REREAD", "CODE-ENTRY", "DOB-REREAD"]
WITHDRAWN_REASON = "DUP-FILING"


def _bus_days(a, b):
    out, d = [], a
    while d <= b:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


class Shaped:
    pass


def shape(w):
    """Everything the shipped files and the deliverables are cut from, at the grain each is written at."""
    S = Shaped()
    p = w.params
    r = K.rng("shape", seed=w.seed)
    samp = w.sample
    nS = len(samp)

    # ---------------------------------------------------------------- per sampled line
    sheet = w.line_sheet[samp]
    S.sheet = sheet
    S.line_no = w.line_no[samp]
    S.circ = np.array([w.sheet_circ[i] for i in sheet], dtype=object)
    S.sheet_no = w.sheet_no[sheet]
    S.firm = w.sheet_firm[sheet]
    signer = w.line_signer[samp]
    S.signer = signer
    S.county = w.signer_county[signer]
    S.vid = w.signer_vid[signer]
    S.code = np.array([K.CODE_KEYS[c] for c in w.sample_code], dtype=object)
    S.day = w.line_day[samp]
    S.det_division = w.det_sos

    # the date the line carries. A line struck as MD either carries no date or a date outside the
    # circulation period, which is the ground the recorder struck it on.
    md = S.code == "MD"
    md_ix = np.where(md)[0]
    blank = md_ix[r.random(len(md_ix)) < 0.40]
    outside = np.array(sorted(set(md_ix.tolist()) - set(blank.tolist())), dtype=np.int64)
    sign_date = np.array([K.WINDOW_OPEN + dt.timedelta(days=int(d)) for d in S.day], dtype=object)
    off = r.integers(-74, -2, size=len(outside))
    for k, i in enumerate(outside):
        sign_date[i] = K.WINDOW_OPEN + dt.timedelta(days=int(off[k]))
    S.sign_date = sign_date
    S.date_blank = np.zeros(nS, dtype=bool)
    S.date_blank[blank] = True
    S.in_window = np.array([(not S.date_blank[i]) and K.WINDOW_OPEN <= sign_date[i] <= K.WINDOW_CLOSE
                            for i in range(nS)])

    # ---------------------------------------------------------------- the recorders' return batches
    bus = _bus_days(K.RETURNS_OPEN, K.RETURNS_CLOSE)
    S.return_id = np.empty(nS, dtype=object)
    S.return_utc = np.empty(nS, dtype=object)
    S.det_date = np.empty(nS, dtype=object)
    batches = []
    for ci, (cc, name, _) in enumerate(K.COUNTIES):
        ix = np.where(S.county == ci)[0]
        if len(ix) == 0:
            continue
        nb = 1 if len(ix) < 60 else (2 if len(ix) < 900 else 3)
        pace = r.random(len(ix))
        order = ix[np.argsort(pace, kind="stable")]
        cuts = np.array_split(order, nb)
        lo = int(2 + ci % 4)
        for b, part in enumerate(cuts):
            dayix = min(lo + b * (3 + ci % 3) + 2, len(bus) - 1)
            day = bus[dayix]
            rid = "R%s-%02d" % (cc, b + 1)
            stamp = K.utc_stamp(dt.datetime.combine(day, dt.time(13 + (ci + b) % 5, 10 + (7 * ci + 3 * b) % 48)))
            for i in part:
                S.return_id[i] = rid
                S.return_utc[i] = stamp
                back = int(1 + (i % 4))
                dd = bus[max(0, dayix - back)]
                S.det_date[i] = dd
            batches.append((cc, rid, day, len(part)))
    S.batches = batches
    # the lines the division determined itself carry the division's own determination date
    for i in np.where(S.det_division)[0]:
        S.det_date[i] = K.CORRECTIONS_CLOSE - dt.timedelta(days=1)
    S.determined_by = np.where(S.det_division, "DIVISION", "RECORDER")

    # ---------------------------------------------------------------- the correction notices
    # a query notice only ever moves a line between two single-signature grounds, and never touches a
    # cancellation ground, a counted line or a duplicate, so no reading of the notices moves the call
    movable = {"AD": "SG", "SG": "AD", "NR": "AD", "NC": "AD", "IL": "MD", "MD": "IL"}
    cand = np.array([i for i in range(nS) if S.code[i] in movable and not S.det_division[i]])
    pick = cand[r.permutation(len(cand))[:p["corrections"]]]
    pick.sort()
    S.corrected = {}
    corr = []
    cdays = _bus_days(K.RETURNS_OPEN + dt.timedelta(days=7), K.CORRECTIONS_CLOSE)
    for k, i in enumerate(pick):
        new = movable[S.code[i]]
        S.corrected[int(i)] = new
        corr.append(dict(
            correction_id="Q-%s-%04d" % (K.COUNTY_CODES[S.county[i]], 1 + k),
            county_code=K.COUNTY_CODES[S.county[i]], circulator_reg_no=S.circ[i],
            sheet_no=int(S.sheet_no[i]), line_no=int(S.line_no[i]),
            prior=S.code[i], new=new,
            corrected_on=cdays[min(len(cdays) - 1, 3 + (k * 7) % (len(cdays) - 3))],
            query_code=QUERY_CODES[(k + S.county[i]) % len(QUERY_CODES)]))
    S.corrections = corr
    S.code_current = np.array([S.corrected.get(i, S.code[i]) for i in range(nS)], dtype=object)

    # ---------------------------------------------------------------- the sheet index and the receipt log
    S.n_sheets = K.SHEETS
    rej = _rejected(w, r)
    S.rejected = rej
    return S


def _rejected(w, r):
    """The 240 sheets two firms had already filed, struck at receipt. They never received a serial, so the
    office's sheet index does not carry them and the firms' own manifests do."""
    out = []
    for firm_ix, count in ((0, 150), (2, 90)):
        ix = np.where(w.sheet_firm == firm_ix)[0]
        pick = ix[r.permutation(len(ix))[:count]]
        for j, s in enumerate(sorted(pick.tolist())):
            out.append(dict(firm=firm_ix, bundle=int(w.sheet_bundle[s]),
                            lines=int(w.sheet_lines[s]), seq=j))
    return out


# ---------------------------------------------------------------------------------- row writers
def _code_written(cc, code):
    """Navajo County's recorder files on its own 2019 code list; every other county on the current set."""
    if cc != K.OLD_CODE_COUNTY:
        return code
    for old, news in K.OLD_TO_NEW.items():
        if code in news:
            return old
    raise AssertionError(code)


def _date_written(cc, d, blank):
    if blank:
        return ""
    if cc == K.DMY_COUNTY:
        return "%02d/%02d/%d" % (d.day, d.month, d.year)
    if cc == K.OLD_CODE_COUNTY:
        return "%02d-%s-%02d" % (d.day, K.UMON3[d.month], d.year % 100)
    return K.iso(d)


def returns_rows(w, S):
    order = np.lexsort((S.line_no, S.sheet_no, np.array([str(c) for c in S.circ]),
                        np.array([K.COUNTY_CODES[c] for c in S.county])))
    for i in order:
        cc = K.COUNTY_CODES[S.county[i]]
        yield dict(county_code=cc, return_id=S.return_id[i], return_received_utc=S.return_utc[i],
                   circulator_reg_no=S.circ[i], sheet_no=int(S.sheet_no[i]), line_no=int(S.line_no[i]),
                   signature_date=_date_written(cc, S.sign_date[i], S.date_blank[i]),
                   voter_reg_id=(int(S.vid[i]) if S.vid[i] else ""),
                   disposition_code=_code_written(cc, S.code[i]),
                   determined_by=S.determined_by[i], determination_date=K.iso(S.det_date[i]))


def corr_rows(w, S):
    for c in S.corrections:
        cc = c["county_code"]
        yield dict(correction_id=c["correction_id"], county_code=cc,
                   circulator_reg_no=c["circulator_reg_no"], sheet_no=c["sheet_no"], line_no=c["line_no"],
                   prior_disposition_code=_code_written(cc, c["prior"]),
                   corrected_disposition_code=_code_written(cc, c["new"]),
                   corrected_on=K.iso(c["corrected_on"]), query_code=c["query_code"])


def _snapshot(w, S, when, late):
    """The registration records for the identifiers the sample transmittal cites, as they stood in the
    archived statewide snapshot of that date."""
    seen = {}
    for i in range(len(S.vid)):
        v = int(S.vid[i])
        if v:
            seen.setdefault(v, int(S.signer[i]))
    day_of = lambda k: K.WINDOW_OPEN + dt.timedelta(days=int(k))
    out = []
    for v in sorted(seen):
        s = seen[v]
        cc = K.COUNTY_CODES[w.signer_county[s]]
        if w.signer_ground[s] == WD.CODE_IX["NC"]:
            cc = K.COUNTY_CODES[(w.signer_county[s] + 4) % len(K.COUNTIES)]
        cancel = int(w.signer_cancel[s])
        restore = int(w.signer_restore[s])
        reason = int(w.signer_cancel_reason[s])
        regday = int(w.signer_regday[s])
        has_cancel = cancel < 10 ** 6
        cut = (when - K.WINDOW_OPEN).days
        shown_cancel = has_cancel and cancel <= cut
        shown_restore = restore < 10 ** 6 and restore <= cut
        status = "ACTIVE"
        cdate, creason = "", ""
        if shown_cancel and not shown_restore:
            status = "CANCELLED"
            cdate = K.iso(day_of(cancel))
            creason = CANCEL_REASON[reason]
        elif shown_cancel and shown_restore:
            cdate = K.iso(day_of(cancel))
            creason = CANCEL_REASON[reason]
        last = max([regday] + ([cancel] if shown_cancel else []) + ([restore] if shown_restore else []))
        stamp = dt.datetime.combine(day_of(last), dt.time(8 + (v % 9), (v // 7) % 60))
        reg = day_of(restore) if shown_restore else day_of(regday)
        out.append(dict(snapshot_date=K.iso(when), voter_reg_id=v, county_code=cc,
                        registration_status=status, registration_date=K.iso(reg),
                        status_changed_utc=K.utc_stamp(stamp), cancellation_date=cdate,
                        cancellation_reason=creason,
                        precinct_code="%s-%03d" % (cc, 1 + int(K.token("prec", v, n=3,
                                                                       alphabet="0123456789"), 10) % 240)))
    return out


def snapshot_rows(w, S, late):
    return _snapshot(w, S, K.LATE_SNAPSHOT if late else K.EARLY_SNAPSHOT, late)


def sheet_rows(w, S):
    rej = {(d["firm"], d["seq"]) for d in S.rejected}
    for s in range(K.SHEETS):
        yield dict(sheet_serial="S%06d" % int(w.sheet_serial[s]), bundle_id="B%04d" % int(w.sheet_bundle[s]),
                   receipt_date=K.iso(K.FILED if int(w.sheet_bundle[s]) % 2 else K.RECEIPT_CLOSED),
                   circulator_reg_no=w.sheet_circ[s],
                   sheet_no=int(w.sheet_no[s]), signature_lines=int(w.sheet_lines[s]),
                   county_circulated=K.COUNTY_CODES[w.sheet_county[s]])


def receipt_rows(w, S):
    nb = w.n_bundles
    rej_by_bundle = {}
    for d in S.rejected:
        rej_by_bundle.setdefault(d["bundle"], []).append(d)
    for b in range(1, nb + 1):
        ix = np.where(w.sheet_bundle == b)[0]
        if len(ix) == 0:
            continue
        acc = len(ix)
        lines = int(w.sheet_lines[ix].sum())
        rj = rej_by_bundle.get(b, [])
        day = K.FILED if b % 2 else K.RECEIPT_CLOSED
        yield dict(bundle_id="B%04d" % b, received_date=K.iso(day),
                   received_utc=K.utc_stamp(dt.datetime.combine(day, dt.time(8 + (b % 9), (b * 17) % 60))),
                   sheets_presented=acc + len(rj), sheets_accepted=acc,
                   sheets_rejected=len(rj), signature_lines_accepted=lines,
                   rejection_code=(WITHDRAWN_REASON if rj else ""),
                   receipted_by="ELEC-%02d" % (1 + b % 6))


def manifest_rows(w, S):
    """Each firm's own delivery manifest. A firm counts what it handed over, so the 240 sheets the office
    struck at receipt are inside these counts, and the firm that changed its trading name in April filed
    under both names on one registration number."""
    rej_by_bundle = {}
    for d in S.rejected:
        rej_by_bundle.setdefault(d["bundle"], []).append(d)
    k = 0
    for b in range(1, w.n_bundles + 1):
        ix = np.where(w.sheet_bundle == b)[0]
        if len(ix) == 0:
            continue
        fi = int(w.sheet_firm[ix[0]])
        code, name, _, regno = K.FIRMS[fi]
        rj = rej_by_bundle.get(b, [])
        day = K.FILED if b % 2 else K.RECEIPT_CLOSED
        sheets = len(ix) + len(rj)
        lines = int(w.sheet_lines[ix].sum()) + sum(d["lines"] for d in rj)
        # the firm's deliveries are manifested under the name it traded as when the sheets were gathered
        med = int(np.median(w.sheet_day[ix]))
        shown = _firm_name_on(fi, K.WINDOW_OPEN + dt.timedelta(days=med))
        k += 1
        yield dict(manifest_no="M-%s-%03d" % (code, k), firm_name=shown, firm_registration_no=regno,
                   delivered_date=K.iso(day), sheets_submitted=sheets, signatures_claimed=lines,
                   office_bundle_ref="B%04d" % b)


def _firm_name_on(fi, when):
    """The name a firm traded under on a date: one of the four changed its trading name in April and kept
    its registration number."""
    code, name, _, _ = K.FIRMS[fi]
    if code == K.FIRM_RENAMED and when >= K.FIRM_RENAME_DATE:
        return K.FIRM_NEW_NAME
    return name


def circ_rows(w, S):
    """The office's extract of the paid circulators registered to gather signatures for this serial. A
    circulator who left one firm for another inside the window registered again under the firm it joined,
    so a registration number carries two rows with their own dates."""
    r = K.rng("circ_rows", seed=w.seed)
    out = []
    for cid in sorted(w.circulators):
        fi = w.circulator_firm[cid]
        cc = K.COUNTY_CODES[int(r.choice(len(K.COUNTIES),
                                         p=np.array([x for _, _, x in K.COUNTIES])
                                         / sum(x for _, _, x in K.COUNTIES)))]
        reg = K.SERIAL_ISSUED + dt.timedelta(days=int(r.integers(2, 24)))
        if cid in w.circulator_moves:
            was, now, day = w.circulator_moves[cid]
            moved = K.WINDOW_OPEN + dt.timedelta(days=day)
            out.append(dict(circulator_reg_no=cid, circulator_type="PAID",
                            registering_firm=_firm_name_on(was, reg),
                            firm_registration_no=K.FIRMS[was][3],
                            county_of_residence=cc, registered_on=K.iso(reg),
                            withdrawn_on=K.iso(moved), registration_status="WITHDRAWN"))
            out.append(dict(circulator_reg_no=cid, circulator_type="PAID",
                            registering_firm=_firm_name_on(now, moved),
                            firm_registration_no=K.FIRMS[now][3],
                            county_of_residence=cc, registered_on=K.iso(moved),
                            withdrawn_on="", registration_status="ACTIVE"))
        else:
            out.append(dict(circulator_reg_no=cid, circulator_type="PAID",
                            registering_firm=_firm_name_on(fi, reg),
                            firm_registration_no=K.FIRMS[fi][3],
                            county_of_residence=cc, registered_on=K.iso(reg), withdrawn_on="",
                            registration_status="ACTIVE"))
    out.sort(key=lambda d: (d["circulator_reg_no"], d["registered_on"]))
    return out


def maint_rows(w, S):
    """The 14 March 2028 statewide list-maintenance run, as the division's own run register wrote it."""
    r = K.rng("maint", seed=w.seed)
    rows = []
    mid = np.where(w.signer_ca_mid)[0]
    for s in mid.tolist():
        rows.append((int(w.signer_vid[s]), K.COUNTY_CODES[w.signer_county[s]], 1))
    extra = w.params["maintenance_other"]
    ids = r.integers(102_000_000, 499_000_000, size=int(extra * 1.03), dtype=np.int64)
    ids = np.unique(ids)[:extra]
    cshare = np.array([x for _, _, x in K.COUNTIES])
    cc = r.choice(len(K.COUNTIES), size=len(ids), p=cshare / cshare.sum())
    for j, v in enumerate(ids.tolist()):
        rows.append((int(v), K.COUNTY_CODES[cc[j]], 0))
    rows.sort()
    reasons = ["LM-NOTICE", "LM-NCOA", "LM-JURY", "LM-RETURNED"]
    act = r.random(len(rows))
    for j, (v, cc, ours) in enumerate(rows):
        # the run both cancels registrations and moves others to inactive; only a cancellation takes a
        # registration out, and only a cancellation before the date signed strikes a signature
        action = "CANCEL" if (ours or act[j] < 0.60) else "INACTIVATE"
        notice = K.LIST_MAINTENANCE - dt.timedelta(days=int(28 + (v % 37)))
        yield dict(run_id="LM-2028-01", run_date=K.iso(K.LIST_MAINTENANCE), voter_reg_id=v, county_code=cc,
                   action_code=action, reason_code=reasons[0] if ours else reasons[1 + j % 3],
                   notice_mailed=K.iso(notice),
                   posted_utc=K.utc_stamp(dt.datetime.combine(K.LIST_MAINTENANCE,
                                                              dt.time(18 + j % 5, (j * 11) % 60))))


def other_rows(w, S):
    """A second initiative measure filed in the same cycle: the office's receipt log for I-04-2028. The
    solution never reads it."""
    r = K.rng("other", seed=w.seed)
    n = 512
    for b in range(1, n + 1):
        firm = K.FIRMS[int(r.integers(0, len(K.FIRMS)))][0]
        acc = int(r.integers(38, 58))
        lines = int(acc * 15 - r.integers(0, 42))
        pres = acc + (1 if r.random() < 0.04 else 0)
        yield dict(bundle_id="C%04d" % b, received_date=K.iso(dt.date(2028, 7, 3) + dt.timedelta(days=b % 3)),
                   firm_code=firm, sheets_presented=pres, sheets_accepted=acc,
                   signature_lines_accepted=lines, receipted_by="ELEC-%02d" % (1 + b % 6))


def regstats_rows(w, S):
    """The office's published registration report of 1 July 2028. The solution never reads it."""
    r = K.rng("regstats", seed=w.seed)
    parties = ["REP", "DEM", "IND", "LBT", "GRN"]
    base = {"REP": 0.345, "DEM": 0.302, "IND": 0.333, "LBT": 0.013, "GRN": 0.007}
    for cc, name, share in K.COUNTIES:
        total = 4_382_000 * share * (1 + 0.04 * (r.random() - 0.5))
        for pc in parties:
            act = int(total * base[pc] * (1 + 0.09 * (r.random() - 0.5)))
            yield dict(report_date=K.iso(dt.date(2028, 7, 1)), county_code=cc, county_name=name,
                       party_code=pc, active_registrations=act,
                       inactive_registrations=int(act * (0.07 + 0.05 * r.random())))
