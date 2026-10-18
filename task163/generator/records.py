"""task163 records: the world and Kilbourne's book shaped into the exports the research team, sales operations and the
payroll tax team hand over.

The research team's pulls of the Census Bureau's business formation statistics for the twelve states: the October 2026
release through the API (long layout, FIPS state codes) and the April 2026 release from the download page (wide layout,
postal codes). The current account system's year-end planning extract of Friday 9 January 2026: the onboarding export
of every account opened from January 2022, the quarterly wages filed for each account from the move to the current
system, and each account's state registrations; the migration load's crosswalk from legacy client numbers; the legacy
system's quarterly wages (in cents, by pay group); the payroll tax team's successor-transfer register; sales
operations' territory map; and the Census Bureau's 2023 nonemployer statistics for the twelve states (read by neither
the plan nor the asks)."""
from __future__ import annotations

import datetime as dt
import json

import numpy as np

import common as K
import company as CO
import world as WD

F_BFS = "bfs_state_api_2026-10-14.json"
F_BFS_APR = "bfs_monthly_states_2026-04-15.csv"
F_ACCOUNTS = "onboarding_accounts_2022-2025.csv"
F_XWALK = "client_migration_crosswalk_2024-06-15.csv"
F_LEGACY = "legacy_quarterly_wages_2022Q1-2024Q2.csv"
F_WAGES = "quarterly_wages_2024Q2-2025Q4.csv"
F_REG = "state_tax_registrations_2026-01-09.csv"
F_SUTA = "suta_successor_transfers_2022-2025.csv"
F_TERR = "sales_territories_2025.csv"
F_NES = "nonemployer_statistics_2023_states.csv"

TERRITORY = {"OH": "Ohio", "PA": "Pennsylvania", "MI": "Michigan", "IN": "Indiana-Kentucky", "KY": "Indiana-Kentucky",
             "MN": "Upper Midwest", "WI": "Upper Midwest", "IA": "Upper Midwest", "TN": "South and Plains",
             "MO": "South and Plains", "VA": "South and Plains", "WV": "South and Plains"}
TERRITORIES = ["Ohio", "Pennsylvania", "Michigan", "Indiana-Kentucky", "Upper Midwest", "South and Plains"]
CHANNELS = ["accountant referral", "bank partner", "outbound", "partner marketplace", "web sign-up"]

SERIES_BA = ("BA_BA", "BA_HBA", "BA_WBA", "BA_CBA")
FREQ_LABEL = {"w": "Weekly", "b": "Biweekly", "s": "Semimonthly", "m": "Monthly"}
ENTITY_LABEL = {"LLC": "LLC", "INC": "Corporation", "SOLE": "Sole proprietor", "LP": "Partnership", "PLLC": "PLLC"}


# ------------------------------------------------------------------------------------------------- statistics
def monthly(W, usps):
    """The release's monthly series for a state, unadjusted: dict series -> array over the simulation's months."""
    return {"BA_BA": W.BA[usps], "BA_HBA": W.HBA[usps], "BA_WBA": W.WBA[usps], "BA_CBA": W.CBA[usps],
            "BF_BF4Q": W.F4[usps], "BF_BF8Q": W.F8[usps], "BF_DUR4Q": W.D4[usps], "BF_DUR8Q": W.D8[usps]}


def seasonal_factors(x, last):
    """Calendar-month factors from the ratio of a series to its centred twelve-month moving average, over the months
    the release holds (index 0 to last), averaged by calendar month and scaled to average one."""
    x = np.asarray(x[:last + 1], dtype=float)
    ratios = {m: [] for m in range(12)}
    for t in range(6, len(x) - 6):
        ma = (0.5 * x[t - 6] + x[t - 5:t + 6].sum() + 0.5 * x[t + 6]) / 12.0
        if ma > 0:
            ratios[t % 12].append(x[t] / ma)
    f = np.array([np.mean(ratios[m]) if ratios[m] else 1.0 for m in range(12)])
    return f / f.mean()


def published(W, vintage):
    """{(state, series, sa, month index): value} for one release. The April release's last three months of
    applications are its preliminary counts (the October release has the late-processed filings in them)."""
    if vintage == "2026-10":
        apps_last, bf4_last, bf8_last = K.midx(K.APPS_LAST), K.midx(K.BF4_LAST), K.midx(K.BF8_LAST)
    else:
        apps_last, bf4_last, bf8_last = K.midx(K.APPS_LAST_EARLY), K.midx(K.BF4_LAST_EARLY), K.midx(K.BF8_LAST_EARLY)
    out = {}
    for s in WD.STATES:
        ser = monthly(W, s.usps)
        rv = K.rng("preliminary", s.usps)
        cuts = {"BF_BF4Q": bf4_last, "BF_BF8Q": bf8_last, "BF_DUR4Q": bf4_last, "BF_DUR8Q": bf8_last}
        for name, x in ser.items():
            last = cuts.get(name, apps_last)
            vals = np.array(x[:last + 1], dtype=float)
            if vintage == "2026-04" and name in SERIES_BA:
                for t in range(last - 2, last + 1):
                    vals[t] = np.floor(vals[t] * (1 - 0.0045 * (t - last + 3) * rv.random()))
            for t in range(last + 1):
                out[(s.usps, name, "no", t)] = float(vals[t])
            if name in ("BF_DUR4Q", "BF_DUR8Q"):
                continue
            f = seasonal_factors(vals, last)
            for t in range(last + 1):
                out[(s.usps, name, "yes", t)] = float(np.floor(vals[t] / f[t % 12] + 0.5))
    return out


def _cell(name, v):
    return ("%.2f" % v) if name in ("BF_DUR4Q", "BF_DUR8Q") else "%d" % int(round(v))


def bfs_json(W):
    """The API response as the research team saved it: a JSON array of string arrays, header first."""
    P = published(W, "2026-10")
    head = ["cell_value", "data_type_code", "time_slot_id", "error_data", "category_code", "seasonally_adj", "time",
            "state"]
    rows = []
    order = {n: i for i, n in enumerate(("BA_BA", "BA_CBA", "BA_HBA", "BA_WBA", "BF_BF4Q", "BF_BF8Q", "BF_DUR4Q",
                                         "BF_DUR8Q"))}
    for (usps, name, sa, t), v in P.items():
        y, m = K.mfrom(t)
        rows.append([_cell(name, v), name, "0", "no", "TOTAL", sa, "%d-%02d" % (y, m), WD.BY[usps].fips])
    rows.sort(key=lambda r: (r[6], r[7], order[r[1]], r[5]))
    lines = [json.dumps(head, separators=(",", ":"))] + [json.dumps(r, separators=(",", ":")) for r in rows]
    return "[" + ",\n".join(lines) + "]\n", len(rows)


def bfs_april_rows(W):
    P = published(W, "2026-04")
    rows = []
    for sa in ("A", "U"):
        for name in ("BA_BA", "BA_CBA", "BA_HBA", "BA_WBA", "BF_BF4Q", "BF_BF8Q", "BF_DUR4Q", "BF_DUR8Q"):
            if sa == "A" and name in ("BF_DUR4Q", "BF_DUR8Q"):
                continue
            for s in sorted(WD.STATES, key=lambda x: x.usps):
                for y in range(2022, 2027):
                    vals = []
                    for m in range(1, 13):
                        v = P.get((s.usps, name, "yes" if sa == "A" else "no", K.midx(y, m)))
                        vals.append("" if v is None else _cell(name, v))
                    if any(vals):
                        rows.append([sa, "TOTAL", name, s.usps, y] + vals)
    return rows


BFS_APR_COLS = ["sa", "naics_sector", "series", "geo", "year", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                "sep", "oct", "nov", "dec"]


def share_base(W):
    """Each state's formations within four quarters from the applications of the share tab's base window, October
    release, unadjusted."""
    a, b = K.midx(K.SHARE_BASE[0]), K.midx(K.SHARE_BASE[1])
    return {s.usps: int(W.F4[s.usps][a:b + 1].sum()) for s in WD.STATES}


def counts_2025(C):
    """Sales operations' 2025 first-time employers by state (the January extract, counted by the counting notes)."""
    out = {s.usps: 0 for s in WD.STATES}
    for b in CO.first_time(C):
        if b.first_pay.year == 2025:
            out[b.state0] += 1
    return out


# ------------------------------------------------------------------------------------------------- the book
def _ein_shown(sp):
    if sp.legacy:
        return sp.ein.lstrip("0")
    return "%s-%s" % (sp.ein[:2], sp.ein[2:])


def ein_dash(e):
    return "%s-%s" % (e[:2], e[2:])


def _years(b, d):
    return max(0.0, (d - b.first_pay).days / 365.25)


def _legacy_text(t_utc):
    local = t_utc - dt.timedelta(hours=CO._et_offset(t_utc - dt.timedelta(hours=5)))
    return local.strftime("%m/%d/%Y %H:%M")


ACCOUNT_COLS = ["account_id", "ein", "legal_name", "dba_name", "entity_type", "naics", "address_state", "opened_at",
                "first_pay_date", "first_time_employer", "previous_provider", "signup_channel", "pay_frequency",
                "employees_at_signup", "product", "product_since", "status", "cancelled_on"]


def account_rows(C):
    out = []
    extract = CO.EXTRACT_PULLED.date()
    for b in C.business.values():
        for sp in b.spells:
            stop = sp.stop
            emp = max(1, int(round(b.employees0 * (1 + b.growth) ** _years(b, sp.start))))
            name = b.name.upper() if sp.legacy else b.name
            dba = b.dba.upper() if (sp.legacy and b.dba) else b.dba
            out.append({
                "account_id": sp.acct, "ein": _ein_shown(sp), "legal_name": name, "dba_name": dba,
                "entity_type": ENTITY_LABEL[b.entity], "naics": b.naics,
                "address_state": b.state_on(stop if stop else extract),
                "opened_at": _legacy_text(sp.opened) if sp.legacy else sp.opened.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "first_pay_date": sp.start.isoformat(), "first_time_employer": "Y" if sp.flag_first else "N",
                "previous_provider": sp.prev_provider, "signup_channel": sp.channel_shown,
                "pay_frequency": FREQ_LABEL[CO.NM.frequency(b)], "employees_at_signup": emp,
                "product": sp.product, "product_since": sp.product_since.isoformat() if sp.product_since else "",
                "status": "Active" if stop is None else "Cancelled", "cancelled_on": stop.isoformat() if stop else "",
            })
    out.sort(key=lambda r: r["account_id"])
    return out


XWALK_COLS = ["legacy_client_no", "account_id", "legacy_source_code", "status_at_migration", "migrated_at"]


def crosswalk_rows(C):
    legacy = sorted(((sp.legacy, sp, b) for b in C.business.values() for sp in b.spells if sp.legacy),
                    key=lambda x: int(x[0]))
    t0 = dt.datetime(2024, 6, 15, 11, 40, 2)
    out = []
    for i, (no, sp, b) in enumerate(legacy):
        status = "Cancelled" if (sp.stop is not None and sp.stop <= CO.LEGACY_LAST_PAY) else "Active"
        out.append({"legacy_client_no": no, "account_id": sp.acct, "legacy_source_code": sp.legacy_code,
                    "status_at_migration": status,
                    "migrated_at": (t0 + dt.timedelta(seconds=int(i * 0.29))).strftime("%Y-%m-%dT%H:%M:%SZ")})
    return out


LEGACY_COLS = ["client_no", "tax_year", "tax_qtr", "pay_group", "check_dates", "employees_paid", "gross_wages"]
WAGES_COLS = ["account_id", "quarter", "pay_dates", "employees_paid", "gross_wages"]


def wage_rows(C):
    """(legacy rows, current rows). Legacy: cents, one row per pay group, and for a client with two groups the
    company-level group 00 holding the client's totals. Current: dollars, one row per account and quarter."""
    leg, cur = [], []
    for b in C.business.values():
        for sp in b.spells:
            for system, y, q, pays, emp, wages in CO.segments(b, sp):
                if system == "legacy":
                    cents = int(round(wages * 100))
                    if b.groups == 2:
                        r = K.rng("groups", b.key, sp.k, y, q)
                        e1 = max(1, int(round(emp * b.split)))
                        e1 = min(e1, emp - 1) if emp >= 2 else e1
                        e2 = max(1, emp - e1)
                        c1 = int(round(cents * min(0.95, max(0.05, b.split + 0.04 * (r.random() - 0.5)))))
                        leg.append([sp.legacy, y, q, "01", pays, e1, c1])
                        leg.append([sp.legacy, y, q, "02", pays, e2, cents - c1])
                        leg.append([sp.legacy, y, q, "00", pays, e1 + e2, cents])
                    else:
                        leg.append([sp.legacy, y, q, "00", pays, emp, cents])
                else:
                    cur.append([sp.acct, "%d-Q%d" % (y, q), pays, emp, "%.2f" % wages])
    leg.sort(key=lambda r: (int(r[0]), r[1], r[2], 1 if r[3] == "00" else 0, r[3]))
    cur.sort(key=lambda r: (r[1], r[0]))
    return leg, cur


REG_COLS = ["account_id", "state", "withholding_account", "ui_account", "liability_date", "kilbourne_from",
            "kilbourne_to"]


def _regnos(b, state):
    r = K.rng("regno", b.key, state)
    wh = "%08d" % int(r.integers(10 ** 7, 10 ** 8))
    ui = "%07d" % int(r.integers(10 ** 6, 10 ** 7))
    if state == "PA":
        ui = "%s-%s" % (ui[:2], ui[2:])
    elif state == "MI":
        ui = "%s %s" % (ui[:4], ui[4:])
    elif state == "OH":
        wh = "51-%s" % wh[2:]
    return wh, ui


def residence(b):
    """[(state, entered, left)] over the business's life with Kilbourne (left None: still there)."""
    out, cur, since = [], b.state0, b.first_pay
    for when, st in b.moves:
        out.append((cur, since, when - dt.timedelta(days=1)))
        cur, since = st, when
    out.append((cur, since, None))
    return out


def registration_rows(C):
    out = []
    for b in C.business.values():
        res = residence(b)
        liable = {}
        for st, entered, _ in res:
            liable.setdefault(st, b.liable0 if st == b.state0 else entered)
        for sp in b.spells:
            stop = sp.stop
            for st, entered, left in res:
                a = max(entered, sp.start)
                z = min(x for x in (left, stop) if x is not None) if (left or stop) else None
                if z is not None and z < a:
                    continue
                wh, ui = _regnos(b, st)
                out.append({"account_id": sp.acct, "state": st, "withholding_account": wh, "ui_account": ui,
                            "liability_date": liable[st].isoformat(), "kilbourne_from": a.isoformat(),
                            "kilbourne_to": z.isoformat() if z else ""})
    out.sort(key=lambda r: (r["account_id"], r["kilbourne_from"], r["state"]))
    return out


SUTA_COLS = ["transfer_no", "state", "effective_date", "predecessor_ein", "predecessor_name", "successor_ein",
             "successor_name", "transfer", "filed_on"]


def _pred_name(r, b):
    """The predecessor's legal name as the state's transfer filing gives it: the business's core name under the
    entity it was before (never the successor's own name)."""
    core = (b.dba or b.name).split(",")[0]
    for suf in (" LLC", " L.L.C.", " Llc", " Inc.", " Inc", " Corporation", " Corp.", " PLLC", " P.L.L.C.", " LP",
                " Ltd."):
        if core.endswith(suf):
            core = core[: -len(suf)]
    u, v = r.random(), r.random()
    name = "%s %s" % (core, "LLC" if u < 0.5 else ("Partnership" if v < 0.5 else "Co."))
    if name.upper().replace(".", "").replace(",", "") == b.name.upper().replace(".", "").replace(",", ""):
        name = "%s %s" % (core, "Partnership" if v < 0.5 else "Co.")
    return name


def suta_rows(C):
    rows = []
    for pred, succ, when, state in C.successors:
        if when > CO.END:
            continue
        s = C.business[succ]
        r = K.rng("suta", s.key)
        if pred is None:
            p_ein, p_name = s.pred_ein, _pred_name(r, s)
        else:
            p = C.business[pred]
            p_ein, p_name = p.ein, p.name
        filed = when + dt.timedelta(days=int(r.integers(9, 44)))
        rows.append([state, when, ein_dash(p_ein), p_name, ein_dash(s.ein), s.name, "Total", filed])
    rows.sort(key=lambda x: (x[7], x[1], x[4]))
    out, seq = [], {}
    for state, when, pe, pn, se, sn, tr, filed in rows:
        seq[filed.year] = seq.get(filed.year, 0) + 1
        out.append({"transfer_no": "ST%d-%04d" % (filed.year, seq[filed.year]), "state": state,
                    "effective_date": when.isoformat(), "predecessor_ein": pe, "predecessor_name": pn,
                    "successor_ein": se, "successor_name": sn, "transfer": tr, "filed_on": filed.isoformat()})
    return out


TERR_COLS = ["state", "state_name", "territory"]


def territory_rows():
    return [{"state": s.usps, "state_name": s.name, "territory": TERRITORY[s.usps]} for s in WD.STATES]


NES_COLS = ["NAME", "state", "NAICS2017", "NAICS2017_LABEL", "NESTAB", "NRCPTOT", "YEAR"]
NES_SECTORS = [("11", "Agriculture, forestry, fishing and hunting", 0.021, 61), ("23", "Construction", 0.113, 92),
               ("31-33", "Manufacturing", 0.013, 88), ("42", "Wholesale trade", 0.011, 141),
               ("44-45", "Retail trade", 0.071, 47), ("48-49", "Transportation and warehousing", 0.098, 58),
               ("51", "Information", 0.014, 54), ("52", "Finance and insurance", 0.031, 73),
               ("53", "Real estate and rental and leasing", 0.106, 96), ("54", "Professional, scientific, and technical services", 0.142, 63),
               ("56", "Administrative and support and waste management and remediation services", 0.067, 39),
               ("61", "Educational services", 0.031, 17), ("62", "Health care and social assistance", 0.088, 36),
               ("71", "Arts, entertainment, and recreation", 0.052, 22), ("72", "Accommodation and food services", 0.022, 64),
               ("81", "Other services (except public administration)", 0.121, 31)]


def nes_rows(W):
    out = []
    for s in sorted(WD.STATES, key=lambda x: x.fips):
        r = K.rng("nes", s.usps)
        total = s.base * 12 * 6.4 * (0.94 + 0.12 * r.random())
        rows = [(code, label, total * w * (0.9 + 0.2 * r.random()), rec) for code, label, w, rec in NES_SECTORS]
        tot_estab = int(round(sum(x[2] for x in rows)))
        tot_rcpt = int(round(sum(x[2] * x[3] * (0.85 + 0.3 * r.random()) for x in rows)))
        out.append([s.name, s.fips, "00", "Total for all sectors", tot_estab, tot_rcpt, 2023])
        for code, label, est, rec in rows:
            out.append([s.name, s.fips, code, label, int(round(est)), int(round(est * rec * (0.9 + 0.2 * r.random()))),
                        2023])
    return out
