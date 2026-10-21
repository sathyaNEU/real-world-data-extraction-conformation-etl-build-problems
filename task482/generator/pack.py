"""The pack's data files, written from the truth in world.py: the registration logs of the legacy and the current case
system, the open caseload snapshot, the public holiday calendar, the card payments and their settlement batches, the
staffing return and the customer survey."""
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "log_old": "cro_registrations_legacy_system_2026-07.csv",
    "log_new": "cro_registrations_case_system_2026-08_to_2026-10.csv",
    "open": "cro_open_caseload_snapshot_2026-10-09.csv",
    "holidays": "cro_public_holidays_2026.csv",
    "pays": "cro_card_payments_settled_2026-07_to_2026-10.csv",
    "batches": "cro_card_settlement_batches_2026q3.csv",
    "paper": "cro_board_paper_timeliness_q3_2026.pdf",
    "staff": "cro_office_staffing_2026-09.xlsx",
    "survey": "cro_customer_survey_2026h1.csv",
    "dictionary": "cro_data_dictionary.csv",
    "manifest": "cro_extract_manifest_2026-10-09.csv",
}
COMPANY = "Companies Registration Office of Ardmuir"
OLD_COLS = ["AppRef", "Office", "Received", "QueryRaised", "Complete", "Registered", "CompanyType"]
NEW_COLS = ["application_id", "office_code", "received_on", "clock_start", "registered_on", "company_type",
            "service"]
OPEN_COLS = ["office_code", "received_on", "clock_start", "open_applications"]
HOL_COLS = ["date", "holiday"]
PAY_COLS = ["payment_ref", "office_code", "batch_id", "settled_on", "amount_eur"]
BATCH_COLS = ["batch_id", "office_code", "terminal_date", "settled_on", "payments", "amount_eur"]
SURVEY_COLS = ["office_code", "responses", "satisfied_pct", "would_use_online_pct"]
TYPES = ["private company limited by shares", "designated activity company", "company limited by guarantee",
         "public limited company", "unlimited company"]
HOLNAMES = {dt.date(2026, 5, 4): "May bank holiday", dt.date(2026, 6, 1): "June bank holiday",
            dt.date(2026, 8, 3): "August bank holiday", dt.date(2026, 10, 26): "October bank holiday",
            dt.date(2026, 12, 25): "Christmas Day", dt.date(2026, 12, 28): "St Stephen's Day (observed)"}


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def ids(x):
    rng = np.random.default_rng(W.SEED + 1)
    allapps = x["apps"] + x["extra"]
    for i, j in enumerate(rng.permutation(len(allapps))):
        a = allapps[j]
        a["ref"] = ("L%06d" % (420117 + 3 * i)) if a["registered"] < dt.date(2026, 8, 1) else ("CR-%07d" % (8810233 + 7 * i))
        a["type"] = TYPES[int(rng.choice(5, p=[0.82, 0.08, 0.06, 0.02, 0.02]))]
        a["service"] = "two-day" if rng.random() < 0.12 else "standard"


def log_rows(x, which):
    """The registrations made by the extract: those made in July in the legacy system, which the offices used until
    31 July, and every later one in the case system, July's receipts still in hand migrated to it with new ids."""
    rows = []
    for a in sorted(x["apps"] + x["extra"], key=lambda a: a["ref"]):
        if a["registered"] > W.EXTRACT:
            continue
        if which == "old" and a["registered"] < dt.date(2026, 8, 1):
            rows.append((a["ref"], a["office"].replace("CRO-", ""), a["received"].strftime("%d/%m/%Y"),
                         "Y" if a["query"] else "N", a["complete"].strftime("%d/%m/%Y"),
                         a["registered"].strftime("%d/%m/%Y"), a["type"]))
        if which == "new" and a["registered"] >= dt.date(2026, 8, 1):
            rows.append((a["ref"], a["office"], a["received"].isoformat(), a["complete"].isoformat(),
                         a["registered"].isoformat(), a["type"], a["service"]))
    return rows


def open_rows(x):
    cnt = {}
    for a in x["apps"]:
        if a["registered"] > W.EXTRACT:
            k = (a["office"], a["received"], a["complete"])
            cnt[k] = cnt.get(k, 0) + 1
    return [(o, r.isoformat(), c.isoformat(), n) for (o, r, c), n in sorted(cnt.items())]


def holiday_rows():
    return [(d.isoformat(), HOLNAMES[d]) for d in sorted(W.HOLIDAYS)]


def next_working(d):
    while True:
        d += dt.timedelta(days=1)
        if d.weekday() < 5 and d not in W.HOLIDAYS:
            return d


def pay_rows(x):
    """Card payments as the acquirer settles them: one batch per office and terminal day, settled the next working
    day; the payment file carries the settlement date and the batch, the batch file the terminal day."""
    rng = np.random.default_rng(W.SEED + 2)
    rows, batches = [], {}
    order = rng.permutation(len(x["pays"]))
    for i, j in enumerate(order):
        p = x["pays"][j]
        bid = "B%s%s" % (p["office"][-2:], p["day"].strftime("%y%m%d"))
        st = next_working(p["day"])
        b = batches.setdefault(bid, [p["office"], p["day"], st, 0, 0])
        b[3] += 1
        b[4] += p["amount"]
        rows.append(("P%08d" % (31400017 + 13 * i), p["office"], bid, st.isoformat(), "%.2f" % p["amount"]))
    rows = [r for r in rows if dt.date(2026, 7, 1) <= dt.date.fromisoformat(r[3]) <= dt.date(2026, 10, 9)]
    rows.sort(key=lambda r: (r[3], r[1], r[0]))
    x["batches"] = batches
    return rows


def batch_rows(x):
    out = []
    for bid, (o, d, st, n, amt) in sorted(x["batches"].items()):
        if dt.date(2026, 7, 1) <= st <= dt.date(2026, 10, 9):
            out.append((bid, o, d.isoformat(), st.isoformat(), n, "%.2f" % amt))
    return out


def survey_rows():
    rng = np.random.default_rng(W.SEED + 3)
    return [(c, int(rng.integers(80, 400)), "%.1f" % float(rng.uniform(71, 90)), "%.1f" % float(rng.uniform(55, 80)))
            for c in W.IDS]
