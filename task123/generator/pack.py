"""The pack's data files: the three utilities' extracts as each system writes them, Pine Harbor's MDMS daily reads,
the service-point file, the indicator records and the two related files the solution does not read.

Every writer sorts its rows on a stated key and formats every value itself, so two builds are byte-identical.
"""
import csv
import io
import json
from collections import defaultdict
from datetime import date, datetime, time, timedelta

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import events as EV
import world as W

D = W.D
TD = timedelta

FILES = dict(
    kvg_bills="KVG_RES_BILLING_EXTRACT_20260415.csv",
    kvg_gs="KVG_GS_BILLING_EXTRACT_20260415.csv",
    kvg_orders="KVG_SERVICE_ORDERS_20251201_20260203.csv",
    northline="Northline_KVG_collections_jobs_Jan2026.xlsx",
    kvg_wcp="KVG_WCP_ENROLLMENTS_20260415.csv",
    nng_reads="NNG_R1_READS_BIMONTHLY_20260415.txt",
    nng_activity="NNG_FIELD_ACTIVITY_DEC25_FEB26.csv",
    nng_crew="NNG_CREW_COMPLETIONS_DEC25_FEB26.csv",
    nng_accounts="NNG_ACCOUNT_PREMISE_HISTORY_20260415.csv",
    nng_flags="NNG_HHAP_PREMISES_20260131.csv",
    nng_sched="NNG_READ_SCHEDULE_2026-27.csv",
    phe_bills="PHE_RESIDENTIAL_BILLS_202510_202604.csv",
    phe_mdms="PHE_MDMS_DAILY_RES_20251006_20260414.parquet",
    phe_meters="PHE_METER_ACCOUNT_HISTORY_20260415.csv",
    phe_wo="PHE_WORK_ORDERS_DEC25_FEB26.json",
    phe_events="PHE_HES_METER_EVENTS_DEC25_FEB26.csv",
    phe_plans="PHE_PAYMENT_ARRANGEMENTS_20260415.csv",
    service_points="service_points_northern_region_2026-04-15.csv",
)
DISTRACTORS = ("kvg_gs", "nng_sched")

NEIGHBOURS = {"Ashwell": ["Brennock", "Farrish"], "Brennock": ["Ashwell", "Carrow", "Dellmoor"],
              "Carrow": ["Brennock", "Glenhollow"], "Dellmoor": ["Brennock", "Evanshade", "Tillery"],
              "Evanshade": ["Dellmoor", "Keswin"], "Farrish": ["Ashwell", "Glenhollow"],
              "Glenhollow": ["Farrish", "Halvern", "Carrow"], "Halvern": ["Glenhollow", "Keswin", "Lorrance"],
              "Keswin": ["Halvern", "Evanshade", "Merrion"], "Lorrance": ["Halvern", "Merrion", "Tillery"],
              "Merrion": ["Lorrance", "Keswin"], "Tillery": ["Lorrance", "Dellmoor"]}


def town_zip():
    out, k = {}, 0
    for c in W.COUNTY_ORDER:
        for t in W.TOWNS[c]:
            out[t] = "49%03d" % (612 + 7 * k + (k * k) % 5)
            k += 1
    return out


ZIP = town_zip()
TOWN_COUNTY = {t: W.DISPLAY[c] for c in W.COUNTY_ORDER for t in W.TOWNS[c]}


def us(d):
    return d.strftime("%m/%d/%Y")


def dt_us(s_):
    return datetime.strptime(s_, "%m/%d/%Y")


def iso(d):
    return d.isoformat()


def ymd(d):
    return d.strftime("%Y%m%d")


def _csv(rows, header, lineterminator="\r\n"):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator=lineterminator)
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def write_text(path, text, encoding="utf-8"):
    with open(path, "w", encoding=encoding, newline="") as fh:
        fh.write(text)


PULL = W.BILL_PULL


def cens(d):
    """A date after the 15 April pull is not yet in the source system: blank."""
    return d if d is not None and d <= PULL else None


def bill_date(end, pid):
    r = W.rng("billdate", pid, end.isoformat())
    return EV.next_bday(end, int(r.integers(1, 4)))


# ------------------------------------------------------------------ Kestrel Valley
def kvg_bills(bills, path):
    rows = []
    kv = [b for b in bills if b.util == "KVG"]
    first = {}
    for bl in kv:
        key = (bl.pid, bl.account, bl.end)
        first.setdefault(key, (bill_date(bl.end, bl.pid), _cycle_of(bl), P_(bl.pid)))
    bno = {}
    for ym in sorted({(k[2].year, k[2].month) for k in first}):
        keys = sorted((k for k in first if (k[2].year, k[2].month) == ym), key=lambda k: first[k])
        nums = _renumber(keys, 1000 * (ym[0] % 100) + ym[1], 0.93)
        for k in keys:
            bno[k] = "%02d%02d%06d" % (ym[0] % 100, ym[1], nums[k] % 1000000)
    for bl in kv:
        key = (bl.pid, bl.account, bl.end)
        bdt = bill_date(bl.end, bl.pid)
        if bl.txn == "CNCL":
            bdt = EV.next_bday(bdt, 6)
        elif bl.txn == "RBIL":
            bdt = EV.next_bday(bdt, 6)
        rows.append((bdt, bno[key], bl.txn, A_(bl.account), P_(bl.pid), "RS-1", "%02d" % _cycle_of(bl),
                     us(bl.start + TD(1)), us(bl.end), (bl.end - bl.start).days, bl.read_type, bl.therms))
    rows.sort(key=lambda r: (r[0], r[1], {"BILL": 0, "CNCL": 1, "RBIL": 2}[r[2]]))
    out = [(r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], us(r[0])) for r in rows]
    write_text(path, _csv(out, ["BILL_NO", "TXN_TYPE", "ACCOUNT_NO", "PREMISE_NO", "RATE_CODE", "CYCLE", "SVC_FROM",
                                "SVC_TO", "DAYS", "READ_TYPE", "THERMS", "BILL_DT"]))
    return len(out)


_CYCLE = {}
_PREM, _ACCT, _METER = {}, {}, {}


def _kvg_check(body):
    return body + str(sum(int(c) * (i % 3 + 1) for i, c in enumerate(body)) % 10)


def register_ids(prem):
    """External identifiers as the utilities' systems issue them: premises numbered in the order they were set up,
    accounts in the order they were opened, meters in the order they were installed, each sequence with the gaps
    that retired and skipped numbers leave."""
    _PREM.clear()
    _ACCT.clear()
    _METER.clear()
    groups = defaultdict(list)
    for p in prem:
        groups[(p.util, p.county)].append(p)
    for (util, county) in sorted(groups, key=lambda k: (k[0], W.COUNTY_ORDER.index(k[1]))):
        ps = sorted(groups[(util, county)], key=lambda q: q.pk)
        ci = W.COUNTY_ORDER.index(county) + 1
        r = W.rng("ids", util, county)
        cur = int(r.integers(120, 1400))
        fmt = {"KVG": "KV%02d%05d", "NNG": "P%02d%05d", "PHE": "PH-%02d%05d"}[util]
        for p in ps:
            cur += int(r.geometric(0.36))
            _PREM[p.pid] = fmt % (ci, cur)
        regular = sorted(((s_, p.pk, j, a) for p in ps for j, (a, s_, e) in enumerate(p.accounts)
                          if not a.startswith("88")), key=lambda x: (x[0], x[1], x[2]))
        if util == "KVG":
            n = int(r.integers(1200000, 2400000))
            for s_, pk, j, a in regular:
                n += int(r.geometric(0.27))
                _ACCT[a] = _kvg_check("%02d%07d" % (ci, n))
        elif util == "NNG":
            n = int(r.integers(1000, 9000))
            for s_, pk, j, a in regular:
                n += int(r.geometric(0.33))
                _ACCT[a] = "4%02d%05d" % (ci, n)
        else:
            n = int(r.integers(20000, 90000))
            for s_, pk, j, a in regular:
                n += int(r.geometric(0.27))
                _ACCT[a] = "70%02d%06d" % (ci, n)
            ami = sorted(((s_, p.pk, j, a) for p in ps for j, (a, s_, e) in enumerate(p.accounts)
                          if a.startswith("88")), key=lambda x: (x[0], x[1], x[2]))
            n = int(r.integers(1000, 5000))
            for s_, pk, j, a in ami:
                n += int(r.geometric(0.7))
                _ACCT[a] = "88%02d%06d" % (ci, n)
            n = int(r.integers(100000, 400000))
            for p in ps:
                n += int(r.geometric(0.4))
                _METER[p.meter_old] = "D%02d%06d" % (ci, n)
    r = W.rng("ids", "ami-meters")
    n = int(r.integers(1400000, 1900000))
    for p in sorted((q for q in prem if q.ami), key=lambda q: (q.install, W.COUNTY_ORDER.index(q.county), q.pk)):
        n += int(r.geometric(0.8))
        _METER[p.meter_new] = "AV%07d" % n
    assert len(set(_PREM.values())) == len(_PREM) and len(set(_ACCT.values())) == len(_ACCT)
    assert len(set(_METER.values())) == len(_METER)


def P_(pid):
    return _PREM[pid]


def A_(acct):
    return _ACCT[acct] if acct else ""


def M_(meter):
    return _METER[meter]


def _renumber(keys, start, p):
    """New running numbers for records in their issue order: start plus steps of one with occasional gaps."""
    r = W.rng("renumber", start)
    out, n = {}, start
    for k in keys:
        n += int(r.geometric(p))
        out[k] = n
    return out


def _cycle_of(bl):
    return _CYCLE.get(bl.pid, 0)


def register_cycles(prem):
    for p in prem:
        if p.util in ("KVG", "PHE"):
            _CYCLE[p.pid] = p.cycle


def kvg_gs(path):
    """Kestrel Valley's general-service bills for the same cycles: shops, schools and master-metered apartment
    buildings. Simulated on the region's own winter."""
    r = W.rng("gs")
    ri = W.rng("gs-ids")
    nxt_p, nxt_a = {}, {}
    rows = []
    hd = W.HDD
    for k in range(940):
        county = W.COUNTY_ORDER[int(r.integers(0, 5))] if k < 900 else "Tillery"
        ci = W.COUNTY_ORDER.index(county) + 1
        nxt_p[ci] = nxt_p.get(ci, int(ri.integers(20, 400))) + int(ri.geometric(0.3))
        nxt_a[ci] = nxt_a.get(ci, int(ri.integers(8100000, 8300000))) + int(ri.geometric(0.3))
        pid = "KV%02d9%04d" % (ci, nxt_p[ci])
        cls = "GS-2" if r.random() < 0.28 else "GS-1"
        size = float(r.lognormal(1.9 if cls == "GS-2" else 1.1, 0.6))
        base = 0.8 * float(r.lognormal(0, 0.3))
        cyc = int(np.clip(round(r.normal(11, 5)), 1, 21))
        acct = _kvg_check("%02d%07d" % (ci, nxt_a[ci]))
        u = size * (base + 0.135 * hd) * (1 + r.normal(0, 0.05, W.NDAY))
        for d, h in W.DST_HOURS.items():
            u[W.IDX[d]] *= h / 24.0
        cum = np.cumsum(np.maximum(u, 0))
        reads = [W.cycle_day(y, m, cyc, 21) for y, m in W.MONTHS]
        reads = [d for d in reads if W.SIM_START <= d <= W.SIM_END]
        for a, b in zip(reads[:-1], reads[1:]):
            if b < D(2025, 10, 1) or b >= W.BILL_PULL:
                continue
            th = int(round(cum[W.IDX[b]] - cum[W.IDX[a]]))
            rows.append((bill_date(b, pid), pid, acct, cls, cyc, a, b, th))
    rows.sort(key=lambda x: (x[0], x[1]))
    out = []
    for ym in sorted({(x[6].year, x[6].month) for x in rows}):
        sub = [x for x in rows if (x[6].year, x[6].month) == ym]
        nums = _renumber(range(len(sub)), 900000 + 100 * ym[1], 0.9)
        for i, (bdt, pid, acct, cls, cyc, a, b, th) in enumerate(sub):
            bno = "%02d%02d%06d" % (b.year % 100, b.month, nums[i] % 1000000)
            out.append((bno, "BILL", acct, pid, cls, "%02d" % cyc, us(a + TD(1)), us(b), (b - a).days, "A", th,
                        us(bdt)))
    out.sort(key=lambda x: (dt_us(x[11]), x[0]))
    write_text(path, _csv(out, ["BILL_NO", "TXN_TYPE", "ACCOUNT_NO", "PREMISE_NO", "RATE_CODE", "CYCLE", "SVC_FROM",
                                "SVC_TO", "DAYS", "READ_TYPE", "THERMS", "BILL_DT"]))
    return len(out), [x[1] for x in rows]


def kvg_orders(ind, path):
    rows = [o for o in ind["kvg_orders"] if D(2025, 12, 1) <= o["done"].date() <= W.KVG_ORDERS_PULL]
    rows.sort(key=lambda o: (o["created"], o["order"]))
    nums = _renumber([o["order"] for o in rows], 26103870, 0.8)
    out = []
    for o in rows:
        status_dt = o["done"]
        out.append((nums[o["order"]], A_(o["account"]), P_(o["premise"]), o["otype"], o["reason"], o["status"],
                    o["created"].strftime("%m/%d/%Y %H:%M"), o["done"].strftime("%m/%d/%Y %H:%M"),
                    status_dt.strftime("%m/%d/%Y"), o["crew"]))
    write_text(path, _csv(out, ["ORDER_NO", "ACCOUNT_NO", "PREMISE_NO", "ORDER_TYPE", "REASON_CD", "STATUS",
                                "CREATED_TS", "COMPLETED_TS", "STATUS_DT", "CREW_ID"]))
    return len(out)


def northline_xlsx(ind, path):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Jobs"
    ws["A1"] = "NORTHLINE UTILITY SERVICES"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Job report: Kestrel Valley Gas collections work order batch KV-COLL-0105"
    ws["A3"] = "Completed jobs 01/05/2026 to 01/16/2026. Prepared 02/09/2026 for invoice NUS-26-0114."
    hdr = ["Job #", "Date", "Acct #", "Service Address", "City", "Job Type", "Tech", "Time On Site"]
    for j, h in enumerate(hdr):
        c = ws.cell(row=5, column=j + 1, value=h)
        c.font = Font(bold=True)
    rows = sorted(ind["northline"], key=lambda x: (x["date"], x["done"], x["job"]))
    nums = _renumber([x["job"] for x in rows], 3012, 0.75)
    for i, x in enumerate(rows):
        vals = ["NL-2601-%04d" % nums[x["job"]], datetime.combine(x["date"], time(0, 0)), int(A_(x["account"])),
                x["address"].upper(),
                x["town"].upper(), "DISCONNECT - NONPAY", x["tech"], x["done"].strftime("%H:%M")]
        for j, v in enumerate(vals):
            c = ws.cell(row=6 + i, column=j + 1, value=v)
            if j == 1:
                c.number_format = "mm/dd/yyyy"
            if j == 2:
                c.number_format = "0"
                c.alignment = Alignment(horizontal="left")
    n = len(rows)
    ws.cell(row=7 + n, column=1, value="Total jobs: %d" % n).font = Font(bold=True)
    for col, wdt in zip("ABCDEFGH", (14, 11, 13, 26, 16, 20, 8, 12)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A6"
    wb.save(path)
    return n


def kvg_wcp(ind, path):
    rows = sorted(ind["kvg_lipp"], key=lambda x: (x["applied"], x["enr"]))
    nums = _renumber([x["enr"] for x in rows], 104300, 0.6)
    out = [("WCP-%06d" % nums[x["enr"]], A_(x["account"]), "WCP", W.DISPLAY[x["county"]].upper(), us(x["applied"]), us(x["approved"]),
            us(x["effective"]), us(x["end"]) if x["end"] and x["end"] <= W.BILL_PULL else "", x["end_reason"])
           for x in rows]
    write_text(path, _csv(out, ["ENROLLMENT_ID", "ACCOUNT_NO", "PROGRAM", "SERVICE_COUNTY", "APPLICATION_DT",
                                "APPROVED_DT", "EFFECTIVE_DT", "END_DT", "END_REASON"]))
    return len(out)


# ------------------------------------------------------------------ Northbank
NNG_LAYOUT = [  # (field, start column, length, picture, description)
    ("REC-TYPE", 1, 1, "X", "H header, D detail, T trailer"),
    ("PREMISE-ID", 2, 8, "X(8)", "premise number"),
    ("ACCOUNT-NO", 10, 8, "9(8)", "account billed for the read"),
    ("RATE-CD", 18, 2, "X(2)", "rate schedule"),
    ("ROUTE", 20, 2, "9(2)", "meter-reading route"),
    ("READ-GRP", 22, 1, "X", "A or B: the route's reading months"),
    ("PREV-READ-DT", 23, 8, "9(8)", "date of the prior read, CCYYMMDD"),
    ("CURR-READ-DT", 31, 8, "9(8)", "date of this read, CCYYMMDD"),
    ("PREV-RDG", 39, 5, "9(5)", "register at the prior read"),
    ("CURR-RDG", 44, 5, "9(5)", "register at this read"),
    ("DIALS", 49, 1, "9", "register digits (4 or 5); the register rolls over to zero"),
    ("CCF", 50, 6, "9(6)", "hundred cubic feet registered between the reads"),
    ("HV-FACTOR", 56, 5, "9V9999", "therms per CCF for the month of the read"),
    ("THERMS", 61, 7, "9(7)", "therms billed"),
    ("READ-CD", 68, 1, "X", "A actual, F final read at a move-out"),
    ("BILL-DT", 69, 8, "9(8)", "bill date, CCYYMMDD"),
]
NNG_WIDTH = 76


def nng_reads(bills, prem, path):
    pmap = {p.pid: p for p in prem}
    rows = []
    for bl in bills:
        if bl.util != "NNG":
            continue
        p = pmap[bl.pid]
        dials = 4 if W.seed("dials", p.pid) % 100 < 22 else 5
        mod = 10 ** dials
        final = any(e == bl.end and a == bl.account for a, s, e in p.accounts)
        hv = W.HV_NNG_MONTH[(bl.end.year, bl.end.month)]
        rows.append((ymd(bill_date(bl.end, bl.pid)), p.route, p.group, P_(bl.pid), A_(bl.account), bl.start, bl.end,
                     bl.reg0 % mod, bl.reg1 % mod, dials, bl.ccf, hv, bl.therms, "F" if final else "A"))
    rows.sort(key=lambda r: (r[0], r[1], r[3], r[6]))
    lines = ["H%-8s%-50s%s" % ("NNGCIS", "R1 BIMONTHLY READS AND BILLED USAGE", "20260415")]
    tot_ccf = tot_th = 0
    for bdt, route, grp, pid, acct, a, b, r0, r1, dials, ccf, hv, th, rc in rows:
        ln = "D%-8s%08d%-2s%02d%s%s%s%05d%05d%d%06d%05d%07d%s%s" % (
            pid, int(acct), "R1", route, grp, ymd(a), ymd(b), r0, r1, dials, ccf, int(round(hv * 10000)), th, rc, bdt)
        assert len(ln) == NNG_WIDTH, (len(ln), ln)
        lines.append(ln)
        tot_ccf += ccf
        tot_th += th
    lines.append("T%09d%012d%012d" % (len(rows), tot_ccf, tot_th))
    lines = [ln.ljust(NNG_WIDTH) for ln in lines]
    write_text(path, "\r\n".join(lines) + "\r\n", encoding="ascii")
    return len(rows)


def nng_activity(ind, path):
    rows = [a for a in ind["nng_activity"] if D(2025, 12, 1) <= a["sched"] <= D(2026, 2, 28)]
    rows.sort(key=lambda a: (a["sched"], a["route"], a["act"]))
    nums = _renumber([a["act"] for a in rows], 5108140, 0.85)
    out = [(nums[a["act"]], P_(a["premise"]), a["code"], iso(a["sched"]), "%02d" % a["route"], a["crew"], a["result"])
           for a in rows]
    write_text(path, _csv(out, ["ACTIVITY_ID", "PREMISE_ID", "ACT_CD", "ACT_DATE", "ROUTE", "CREW", "RESULT_CD"]))
    return len(out), nums


def nng_crew(ind, acts, path):
    rows = [c for c in ind["nng_crew"] if c["act"] in acts]
    rows.sort(key=lambda c: (c["done"], acts[c["act"]]))
    out = [(acts[c["act"]], c["done"].strftime("%Y-%m-%d %H:%M"), c["crew"], c["note"]) for c in rows]
    write_text(path, _csv(out, ["ACTIVITY_ID", "COMPLETED_AT", "CREW", "REMARKS"]))
    return len(out)


def nng_accounts(ind, path):
    rows = sorted((x for x in ind["nng_accounts"] if x["start"] <= PULL),
                  key=lambda x: (x["premise"], x["start"], x["account"]))
    out = [(A_(x["account"]), P_(x["premise"]), "RES", iso(x["start"]), iso(cens(x["end"])) if cens(x["end"]) else "")
           for x in rows]
    out.sort(key=lambda x: (x[1], x[3], x[0]))
    write_text(path, _csv(out, ["ACCOUNT_NO", "PREMISE_ID", "CUST_CLASS", "START_DT", "END_DT"]))
    return len(out)


def nng_flags(ind, path):
    out = sorted((P_(x["premise"]), A_(x["account"]), "HHAP", iso(x["since"]), "A") for x in ind["nng_roster"])
    write_text(path, _csv(out, ["PREMISE_ID", "ACCOUNT_NO", "PROGRAM_CD", "PROGRAM_START_DT", "PROGRAM_STATUS"]))
    return len(out)


EV_REFRESH = D(2025, 12, 1)


def nng_sched(path):
    out = []
    months = [(2026, m) for m in range(9, 13)] + [(2027, m) for m in range(1, 9)]
    for route in range(1, 21):
        for k, (y, m) in enumerate(months):
            grp = "A" if m % 2 == 1 else "B"
            bd = []
            d = D(y, m, 1)
            while d.month == m:
                if d.weekday() < 5:
                    bd.append(d)
                d += TD(1)
            j = int(round((route - 1) * (len(bd) - 1) / 19))
            out.append(("%02d" % route, grp, "%04d-%02d" % (y, m), iso(bd[j]), "NB-MR%02d" % (1 + (route - 1) // 3)))
    out.sort(key=lambda r: (r[2], r[0]))
    write_text(path, _csv(out, ["ROUTE", "READ_GRP", "READ_MONTH", "SCHED_READ_DT", "READER"]))
    return len(out)


# ------------------------------------------------------------------ Pine Harbor
def phe_bills(bills, path):
    rows = []
    for bl in bills:
        if bl.util != "PHE":
            continue
        basis = bl.basis
        rt = "AMI" if basis == "CALENDAR" else {"A": "ACT", "E": "EST"}[bl.read_type]
        rows.append((A_(bl.account), P_(bl.pid), "RES", basis, "" if basis == "CALENDAR" else "%02d" % _cycle_of(bl),
                     bl.start + TD(1), bl.end, bl.therms, rt, bill_date(bl.end, bl.pid)))
    rows.sort(key=lambda r: (r[9], r[0], r[6]))
    out = [(r[0], r[1], r[2], r[3], r[4], iso(r[5]), iso(r[6]), r[7], r[8], iso(r[9])) for r in rows]
    write_text(path, _csv(out, ["ACCOUNT", "PREMISE", "RATE", "BILL_BASIS", "CYCLE", "SERVICE_START", "SERVICE_END",
                                "THERMS", "READ_TYPE", "BILL_DATE"]))
    return len(out)


def phe_mdms(prem, mdms, path):
    pmap = {p.pid: p for p in prem}
    meters, days, vals, vee = [], [], [], []
    epoch = date(1970, 1, 1)
    last = W.IDX[W.BILL_PULL - TD(1)]
    for pid in sorted(mdms, key=lambda x: M_(pmap[x].meter_new)):
        d0, ccf, q = mdms[pid]
        m = M_(pmap[pid].meter_new)
        for k in range(len(ccf)):
            i = d0 + k
            if i > last or not np.isfinite(ccf[k]):
                continue
            meters.append(m)
            days.append((W.DAYS[i] - epoch).days)
            vals.append(float(ccf[k]))
            vee.append(q[k])
    table = pa.table({
        "meter_id": pa.array(meters, pa.string()),
        "read_date": pa.array(np.array(days, np.int32), pa.date32()),
        "usage_ccf": pa.array(np.array(vals, np.float64), pa.float64()),
        "vee_status": pa.array(vee, pa.string()),
        "uom": pa.array(["CCF"] * len(meters), pa.string()),
    }).replace_schema_metadata(None)
    pq.write_table(table, path, compression="snappy", use_dictionary=True, row_group_size=250_000,
                   write_statistics=True)
    return len(meters)


def phe_meters(prem, path):
    out = []
    for p in prem:
        if p.util != "PHE":
            continue
        for a, s, e in p.accounts:
            if s > PULL:
                continue
            if p.ami and s > p.install:
                out.append((M_(p.meter_new), "AMI-V", P_(p.pid), A_(a), s, cens(e)))
            else:
                out.append((M_(p.meter_old), "DIAL", P_(p.pid), A_(a), s, cens(e)))
    out.sort(key=lambda r: (r[2], r[4], r[0]))
    rows = [(m, t, pid, a, iso(s), iso(e) if e else "") for m, t, pid, a, s, e in out]
    write_text(path, _csv(rows, ["METER_NO", "METER_TYPE", "PREMISE_ID", "ACCOUNT_NO", "LINKED_FROM", "LINKED_TO"]))
    return len(rows)


def phe_wo(ind, path):
    rows = [w for w in ind["phe_wo"] if D(2025, 12, 1) <= w["sched"] <= D(2026, 2, 28)]
    rows.sort(key=lambda w: (w["sched"], w["wo"]))
    nums = _renumber([w["wo"] for w in rows], 641220, 0.5)
    recs = []
    for w in rows:
        recs.append({"woNumber": "WO-%06d" % nums[w["wo"]], "accountNumber": A_(w["account"]),
                     "premiseId": P_(w["premise"]),
                     "woType": w["wtype"], "status": w["status"], "scheduledDate": iso(w["sched"]),
                     "completedAt": w["done"].strftime("%Y-%m-%dT%H:%M:00-05:00"), "crew": w["crew"]})
    doc = {"exportName": "WORK_ORDERS_RES", "system": "PHE FieldPoint", "exportedAt": "2026-04-15T07:12:44-04:00",
           "criteria": {"scheduledFrom": "2025-12-01", "scheduledTo": "2026-02-28", "customerClass": "RES"},
           "count": len(recs), "workOrders": recs}
    write_text(path, json.dumps(doc, indent=1, ensure_ascii=True) + "\n")
    return len(recs)


def phe_events(ind, path):
    lo = datetime(2025, 12, 1, 5, 0)
    hi = datetime(2026, 3, 1, 5, 0)
    rows = [e for e in ind["phe_events"] if lo <= e["utc"] < hi]
    rows.sort(key=lambda e: (e["utc"], M_(e["meter"]), e["code"]))
    out = [(M_(e["meter"]), e["utc"].strftime("%Y-%m-%dT%H:%M:%SZ"), e["code"], e["source"], e["ref"], e["reason"])
           for e in rows]
    write_text(path, _csv(out, ["METER_ID", "EVENT_TS_UTC", "EVENT_CODE", "SOURCE", "REQUEST_REF", "REASON_CD"]))
    return len(out)


def phe_plans(ind, path):
    rows = sorted((x for x in ind["phe_plans"] if x["created"] <= PULL), key=lambda x: (x["created"], x["plan"]))
    nums = _renumber([x["plan"] for x in rows], 2006180, 0.7)
    out = [("PP%07d" % nums[x["plan"]], A_(x["account"]), {"LIPP": "IBPP"}.get(x["ptype"], x["ptype"]), iso(x["start"]),
            iso(cens(x["end"])) if cens(x["end"]) else "", "ENDED" if cens(x["end"]) else "ACTIVE", iso(x["created"]))
           for x in rows]
    write_text(path, _csv(out, ["PLAN_ID", "ACCOUNT_NO", "PLAN_TYPE", "START_DATE", "END_DATE", "STATUS",
                                "CREATED_DATE"]))
    return len(out)


# ------------------------------------------------------------------ the region's service points
def service_points(prem, gs_pids, path):
    r = W.rng("sp")
    out = []
    for p in prem:
        town = p.town
        if r.random() < 0.03:
            # a premise near the county line takes its mail through the neighbouring county's post office
            nb = NEIGHBOURS[p.county][int(r.integers(0, len(NEIGHBOURS[p.county])))]
            town = W.TOWNS[nb][0]
        out.append(({"KVG": "KESTREL VALLEY", "NNG": "NORTHBANK", "PHE": "PINE HARBOR"}[p.util], P_(p.pid),
                    p.street.upper(), town.upper(), ZIP[town], W.DISPLAY[p.county].upper(), "SFR" if r.random() < 0.93 else
                    ("MH" if r.random() < 0.7 else "2-4")))
    for k, pid in enumerate(sorted(set(gs_pids))):
        c = W.COUNTY_ORDER[int(pid[2:4]) - 1]
        town = W.TOWNS[c][int(W.seed("gs-town", pid) % len(W.TOWNS[c]))]
        st = ["MAIN", "STATE", "COMMERCE", "INDUSTRIAL", "MARKET", "DEPOT", "HARBOR", "MILL", "LAKE", "CENTER"]
        sf = ["ST", "AVE", "DR", "PKWY", "RD"]
        out.append(("KESTREL VALLEY", pid, "%d %s %s" % (100 + W.seed("gs-st", pid) % 9000, st[W.seed("gs-sn", pid) % 10],
                                                         sf[W.seed("gs-sf", pid) % 5]), town.upper(),
                    ZIP[town], W.DISPLAY[c].upper(), "COM" if W.seed("gs-t", pid) % 10 < 7 else "MFR"))
    out.sort(key=lambda x: (x[0], x[1]))
    write_text(path, _csv(out, ["UTILITY", "PREMISE_ID", "SERVICE_ADDRESS", "CITY", "ZIP", "COUNTY", "PREMISE_TYPE"]))
    return len(out)
