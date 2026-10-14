"""Write the society's and Harbourline's records into the pack (target/): lists, release log, dial log, close-outs,
contact points, the do-not-call register, account events and transfers, the holdings view, the legacy certificate
register and the migration batches. Each file in the idiom of the system that exports it."""
from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo

import numpy as np

import sim as S
import world as W

NZ = ZoneInfo("Pacific/Auckland")
UTC = dt.timezone.utc
TYPE_WORD = {"M": "MOBILE", "H": "HOME", "W": "WORK"}
CONTACT_WORD = {"M": "Mobile", "H": "Home", "W": "Work"}
FREQ_B = {"At maturity": "MAT", "Quarterly": "QTR", "Annually": "ANN", "Monthly": "MTH"}
BRANCH_NAME = {"0410": "Tauranga", "0412": "Mount Maunganui", "0415": "Papamoa", "0418": "Te Puke",
               "0421": "Katikati", "0430": "Whakatane", "0435": "Rotorua", "0440": "Hamilton"}


def dmy(d):
    return d.strftime("%d/%m/%Y")


def comma_money(x):
    return "{:,.2f}".format(x)


# ---------------------------------------------------------------------------------------------------------------
LISTS_2025_COLS = ["Campaign", "Account No", "Customer No", "Product", "Term (mths)", "Rate %", "Principal", "Opened",
                   "Maturity", "Interest", "Branch"]
LISTS_2026_COLS = ["campaign", "account", "customer_no", "product_code", "term_months", "int_rate", "principal",
                   "start_date", "maturity_date", "interest_freq", "branch_code"]


def lists_2025_rows(Wd):
    for q in W.PAST:
        if not q.startswith("2025"):
            continue
        for s in Wd.campaigns[q]["listed"]:
            yield ["TDR %s-Q%s" % (q[:4], q[-1]), s["acct_dashed"], s["holder"], "Term Deposit", s["term"] * 12,
                   "%.2f" % s["rate"], comma_money(s["principal"]), dmy(s["opened"]), dmy(s["maturity"]),
                   s["interest"], BRANCH_NAME[s["branch"]]]


def _row_b(campaign, s):
    return [campaign, s["acct"], s["holder"], "TD", s["term"] * 12, "%.4f" % (s["rate"] / 100.0),
            "%.2f" % s["principal"], s["opened"].isoformat(), s["maturity"].isoformat(), FREQ_B[s["interest"]],
            s["branch"]]


def lists_2026_rows(Wd):
    for q in W.PAST:
        if not q.startswith("2026"):
            continue
        for s in Wd.campaigns[q]["listed"]:
            yield _row_b("TDR-%s" % q, s)


def list_fwd_rows(Wd):
    for d in Wd.campaigns[W.FWD]["listed"]:
        s = dict(acct=d["acct"], holder=d["holder"], term=d["term"], rate=d["rate"], principal=d["principal"],
                 opened=d["opened"], maturity=d["maturity"], interest=d["interest"],
                 branch=Wd.customers[d["holder"]]["branch"])
        yield _row_b("TDR-%s" % W.FWD, s)


# ---------------------------------------------------------------------------------------------------------------
RELEASE_COLS = ["campaign", "account", "maturity_date", "release_date", "status", "reason"] + \
    [x for k in range(1, 5) for x in ("callable_%d" % k, "type_%d" % k)]


def release_rows(Wd):
    for q in W.PAST:
        for rel in Wd.campaigns[q]["released"]:
            d = Wd.deposits.get(rel["acct"])
            mat = rel["release"] + dt.timedelta(days=21)
            nums = []
            if rel["status"] == "RELEASED":
                for slot, ph in rel["numbers"]:
                    nums += [ph["e164"], TYPE_WORD[ph["kind"]]]
            nums += [""] * (8 - len(nums))
            yield ["TDR-%s" % q, rel["acct"], mat.isoformat(), rel["release"].isoformat(), rel["status"],
                   rel["reason"]] + nums


DIAL_COLS = ["case_ref", "kbs_ref", "dial_no", "dialled_utc", "number", "slot", "outcome", "talk_sec", "agent"]
CLOSE_COLS = ["case_ref", "kbs_ref", "released", "closed", "close_reason", "dials", "last_outcome"]


def vendor_ref(acct):
    return "%s-%s-%s" % (acct[:6], acct[6:13], acct[13:])


def dial_rows(Wd):
    r = W.rng("agents")
    agents = ["HLA%03d" % k for k in sorted(int(x) for x in r.choice(np.arange(11, 260), 74, replace=False))]
    for q in W.PAST:
        for ref, acct, dials in Wd.campaigns[q]["dials"]:
            for x in dials:
                t = x["local"].replace(tzinfo=NZ).astimezone(UTC)
                yield [ref, vendor_ref(acct), x["seq"], t.strftime("%Y-%m-%dT%H:%M:%SZ"), x["e164"].lstrip("+"),
                       x["slot"], x["code"], x["talk"], agents[int(r.integers(0, len(agents)))]]


def closeout_rows(Wd):
    for q in W.PAST:
        dl = {ref: dials for ref, _, dials in Wd.campaigns[q]["dials"]}
        for co in Wd.campaigns[q]["closeouts"]:
            dials = dl[co["case_ref"]]
            last = dials[-1]["code"] if dials and co["reason"] != "WITHDRAWN" else ""
            if co["reason"] == "WITHDRAWN" and dials:
                last = ""
            yield [co["case_ref"], vendor_ref(co["acct"]), co["release"].isoformat(), co["closed_on"].isoformat(),
                   co["reason"], len(dials), last]


# ---------------------------------------------------------------------------------------------------------------
CONTACT_COLS = ["customer_no", "priority", "contact_type", "number", "recorded"]


def contact_rows(Wd):
    seen = set()
    for d in sorted(Wd.campaigns[W.FWD]["listed"], key=lambda d: d["holder"]):
        c = Wd.customers[d["holder"]]
        if c["cust"] in seen:
            continue
        seen.add(c["cust"])
        for k, ph in enumerate(c["phones"]):
            yield [c["cust"], k + 1, CONTACT_WORD[ph["kind"]], ph["display"], ph["added"].isoformat()]


DNC_COLS = ["number", "recorded", "withdrawn", "source"]


def dnc_rows(Wd):
    for e in Wd.register:
        yield [e["e164"], e["added"].isoformat(), e["removed"].isoformat() if e["removed"] else "", e["source"]]


# ---------------------------------------------------------------------------------------------------------------
EVENT_COLS = ["account", "customer_no", "event_date", "event_type", "amount", "term_months", "rate", "maturity_date"]
TRANSFER_COLS = ["value_date", "from_account", "to_account", "amount", "narrative"]


def event_rows(Wd):
    order = {"OPEN": 0, "MATURE": 1, "REINVEST": 3, "PAYOUT": 4, "BREAK": 5, "CLOSE": 6}
    rows = [e for e in Wd.events if W.EVENTS_FROM <= e[1] <= W.EVENTS_TO]
    rows.sort(key=lambda e: (e[1], e[0], order[e[2]]))
    for a, d, t, amt, term, rate, mat in rows:
        rr = "%.4f" % (float(rate) / 100.0) if rate != "" else ""
        yield [a, Wd.deposits[a]["holder"], d.isoformat(), t, "%.2f" % amt, term, rr, mat]


def transfer_rows(Wd):
    """The payments system's view: a deposit's maturity proceeds leave through the society's maturity settlement
    account, the matured deposit named in the narrative in the payments system's reference format."""
    rows = []
    for d, a, b, amt, nar in Wd.transfers:
        if not (W.EVENTS_FROM <= d <= W.EVENTS_TO):
            continue
        if nar == "MATURITY PROCEEDS":
            rows.append((d, W.SETTLEMENT, b, amt, "TD MATURITY %s" % Wd.deposits[a]["acct_dashed"]))
        else:
            rows.append((d, a, b, amt, nar))
    rows.sort(key=lambda t: (t[0], t[1], t[2], t[3]))
    for d, a, b, amt, nar in rows:
        yield [d.isoformat(), a, b, "%.2f" % amt, nar]


# ---------------------------------------------------------------------------------------------------------------
HOLD_COLS = ["customer_no", "account", "product", "principal", "int_rate", "term_months", "start_date",
             "maturity_date"]
KIP_COLS = ["cert_no", "member_no", "principal", "rate", "issue_date", "maturity_date", "term_months", "status"]
BATCH_COLS = ["batch", "batch_date", "cert_no", "new_account", "status"]


def holdings_rows(H):
    for row in H["rows"]:
        yield row


def kip_rows(H):
    for row in H["kip"]:
        yield row


def batch_rows(H):
    for row in H["batches"]:
        yield row
