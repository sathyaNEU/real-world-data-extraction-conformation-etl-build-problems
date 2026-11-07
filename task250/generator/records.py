"""task250 architecture 4: the institute's operational records, derived from the clean truth.

Cases with their mailings and final dispositions, the returns in each mode (households that returned twice
included), the household grid, access codes, web sessions, refusals, partial returns, the letters the postal
service sent back and the helpdesk's contacts. Everything here is true; pack.py writes it the way each system
exports it."""
import datetime as dt
import numpy as np

import params as P
import world as Wm

PAGES = 32          # web questionnaire pages: 1 welcome, 2 the selection question, 3 the grid, 4-12 core, 13-31 topic, 32 submit
CORE_END = 12


def luhn_digit(s):
    tot = 0
    for i, ch in enumerate(reversed(s)):
        d = int(ch)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        tot += d
    return str((10 - tot % 10) % 10)


ALPHA = "ACDEFGHJKLMNPQRTUVWXY3479"


def code8(rng):
    return "".join(ALPHA[int(i)] for i in rng.integers(len(ALPHA), size=8))


def build(W):
    R = {}
    rs = Wm.stream("records")
    rs_web = Wm.stream("web")
    rs_post = Wm.stream("post")
    rs_help = Wm.stream("helpdesk")
    n = len(W["addr_survey"])
    occ_index = {int(a): j for j, a in enumerate(W["occ"])}
    stn = W["status_names"]
    # ------------------------------------------------------------ identifiers
    used = set()
    case_id = []
    for a in range(n):
        si = int(W["addr_survey"][a])
        while True:
            body = "%d%06d" % (si + 1, int(rs.integers(0, 1000000)))
            if body not in used:
                used.add(body)
                break
        case_id.append(body + luhn_digit(body))
    R["case_id"] = case_id
    addr_used = set()
    address_id = []
    for a in range(n):
        mun = W["addr_mun"][a]
        while True:
            seq = int(rs.integers(0, 1000000))
            body = "%s%06d" % (mun, seq)
            if body not in addr_used:
                addr_used.add(body)
                break
        address_id.append(body + "%02d" % (int(body) % 97))
    R["address_id"] = address_id
    # ------------------------------------------------------------ per case outcome
    kind = ["none"] * n          # complete_web, complete_paper, partial, refusal_contact, refusal_blank, none
    kept_mode = [None] * n
    kept_day = [None] * n
    second = [None] * n          # (mode, day, respondent index)
    web_engaged = [None] * n     # for sessions: list of (code_index, start_day, last_page, submitted)
    for a in range(n):
        j = occ_index.get(a)
        if j is None:
            continue
        if W["resp"][j]:
            kept_mode[a] = int(W["mode"][j])
            kept_day[a] = int(W["day"][j])
            kind[a] = "complete_web" if kept_mode[a] == 0 else "complete_paper"
            if rs.random() < 0.013:
                k = len(W["hh_members"][j])
                other_mode = 1 - kept_mode[a]
                d2 = kept_day[a] + int(rs.integers(2, 24))
                if other_mode == 1:
                    d2 = max(d2, 25)
                r2 = int(W["respondent"][j])
                if k > 1 and rs.random() < 0.45:
                    r2 = int((r2 + 1 + rs.integers(0, k - 1)) % k)
                second[a] = (other_mode, min(d2, 58), r2)
        else:
            u = rs.random()
            if u < 0.046:
                kind[a] = "breakoff"
            elif u < 0.046 + 0.021:
                kind[a] = "refusal_contact"
            elif u < 0.046 + 0.021 + 0.006:
                kind[a] = "refusal_blank"
    R["kind"], R["kept_mode"], R["kept_day"], R["second"] = kind, kept_mode, kept_day, second
    # ------------------------------------------------------------ access codes
    codes = []                    # (case index, code, issued date, reason)
    case_codes = [[] for _ in range(n)]
    seen = set()
    for a in range(n):
        letter = W["addr_letter"][a]
        while True:
            c = code8(rs)
            if c not in seen:
                seen.add(c)
                break
        case_codes[a].append(len(codes))
        codes.append((a, c, letter - dt.timedelta(days=int(rs.integers(9, 15))), "initial"))
    R["codes"], R["case_codes"] = codes, case_codes
    # ------------------------------------------------------------ web sessions
    sessions = []                 # (code index, start datetime UTC, end datetime UTC, last page answered, submitted)
    replacement_cases = []

    def local_dt(letter, day, rng):
        hour = int(rng.choice([8, 9, 10, 12, 13, 14, 18, 19, 20, 21, 22, 23],
                              p=[0.04, 0.05, 0.06, 0.07, 0.08, 0.06, 0.10, 0.14, 0.15, 0.13, 0.08, 0.04]))
        t = dt.datetime.combine(letter + dt.timedelta(days=day), dt.time(hour, int(rng.integers(0, 60)),
                                                                          int(rng.integers(0, 60))))
        return t

    def to_utc(t):
        # Portugal mainland: WET in winter, WEST (UTC+1) from 29 March to 25 October 2026
        if dt.datetime(2026, 3, 29, 1) <= t < dt.datetime(2026, 10, 25, 2):
            return t - dt.timedelta(hours=1)
        return t

    for a in range(n):
        letter = W["addr_letter"][a]
        k = kind[a]
        web_complete = (k == "complete_web") or (second[a] is not None and second[a][0] == 0)
        started_web_then_paper = (k == "complete_paper" and rs_web.random() < 0.085)
        if not (web_complete or k == "breakoff" or started_web_then_paper):
            continue
        cidx = case_codes[a][0]
        # a household that lost its letter asks the helpdesk for a new code
        if rs_web.random() < 0.019:
            while True:
                c = code8(rs_web)
                if c not in seen:
                    seen.add(c)
                    break
            iss = letter + dt.timedelta(days=int(rs_web.integers(3, 16)))
            case_codes[a].append(len(codes))
            codes.append((a, c, iss, "replacement"))
            replacement_cases.append(a)
        code_list = case_codes[a]
        if web_complete:
            day = kept_day[a] if k == "complete_web" else second[a][1]
            n_sess = 1 + (rs_web.random() < 0.15) + (rs_web.random() < 0.03)
            first_day = max(1, day - int(rs_web.integers(0, 9)) if n_sess > 1 else day)
            days = sorted(set([first_day] + [int(rs_web.integers(first_day, day + 1)) for _ in range(n_sess - 2)]
                              + [day]))
            for i, dd in enumerate(days):
                last = i == len(days) - 1
                ci = code_list[-1] if (last and len(code_list) > 1) else code_list[0]
                st = local_dt(letter, dd, rs_web)
                if last:
                    dur = int(np.clip(rs_web.gamma(4.0, 6.0), 9, 95))
                    page = PAGES
                else:
                    dur = int(np.clip(rs_web.gamma(2.0, 4.0), 2, 40))
                    page = int(rs_web.integers(2, PAGES - 1))
                sessions.append((ci, to_utc(st), to_utc(st + dt.timedelta(minutes=dur)), page, last))
        else:
            day = int(rs_web.integers(1, 40))
            n_sess = 1 + (rs_web.random() < 0.22)
            for i in range(n_sess):
                ci = code_list[-1] if (i == n_sess - 1 and len(code_list) > 1) else code_list[0]
                st = local_dt(letter, min(day + 3 * i, 48), rs_web)
                if k == "breakoff":
                    page = int(rs_web.choice([2, 3, 4, 6, 9, 11, 13, 15, 18, 22, 26],
                                             p=[0.09, 0.13, 0.12, 0.10, 0.09, 0.08, 0.10, 0.08, 0.08, 0.07, 0.06]))
                else:
                    page = int(rs_web.integers(2, 20))
                dur = int(np.clip(rs_web.gamma(2.0, 4.0), 2, 40))
                sessions.append((ci, to_utc(st), to_utc(st + dt.timedelta(minutes=dur)), page, False))
        # a log-in that never answered the first question
        if rs_web.random() < 0.06:
            st = local_dt(letter, int(rs_web.integers(1, 10)), rs_web)
            sessions.append((code_list[0], to_utc(st), to_utc(st + dt.timedelta(minutes=1)), 0, False))
    # households that logged in and left at the welcome page
    for a in range(n):
        if kind[a] == "none" and W["addr_status"][a] == stn.index("occupied") and rs_web.random() < 0.018:
            letter = W["addr_letter"][a]
            st = local_dt(letter, int(rs_web.integers(1, 30)), rs_web)
            sessions.append((case_codes[a][0], to_utc(st), to_utc(st + dt.timedelta(minutes=1)),
                             int(rs_web.choice([0, 1], p=[0.7, 0.3])), False))
    # the IT team's launch checks: test codes outside the case register
    test_codes = []
    for si, s in enumerate(P.SURVEYS):
        letter = s[3]
        for i in range(int(rs_web.integers(18, 34))):
            c = code8(rs_web)
            test_codes.append((si, c))
            st = dt.datetime.combine(letter - dt.timedelta(days=int(rs_web.integers(1, 6))),
                                     dt.time(int(rs_web.integers(9, 18)), int(rs_web.integers(0, 60))))
            page = int(rs_web.choice([2, 5, 12, PAGES]))
            sessions.append((("TEST", si, c), to_utc(st), to_utc(st + dt.timedelta(minutes=int(rs_web.integers(2, 30)))),
                             page, page == PAGES))
    R["sessions"], R["test_codes"], R["replacement_cases"] = sessions, test_codes, replacement_cases
    R["web_complete_case"] = [(kind[a] == "complete_web") or (second[a] is not None and second[a][0] == 0)
                              for a in range(n)]
    # partial returns: a breakoff past the core module's last page (the web system's status at close)
    max_page = {}
    for ci, st, en, page, sub in sessions:
        if isinstance(ci, tuple):
            continue
        a = codes[ci][0]
        max_page[a] = max(max_page.get(a, 0), page)
    R["max_page"] = max_page
    for a in range(n):
        if kind[a] == "breakoff" and max_page.get(a, 0) >= CORE_END:
            kind[a] = "partial"
    # ------------------------------------------------------------ mailings and postal returns
    mailings = []
    returns_post = []             # (case index, mailing number, received date, reason code)
    st_names = stn
    p_ret = {"nonexistent": 0.86, "vacant": 0.41, "nonresidential": 0.12, "communal": 0.07, "occupied": 0.008}
    reasons = {"nonexistent": (["02", "01"], [0.71, 0.29]), "vacant": (["03", "04", "06"], [0.46, 0.29, 0.25]),
               "nonresidential": (["03", "08"], [0.8, 0.2]), "communal": (["03", "05"], [0.6, 0.4]),
               "occupied": (["04", "06", "05", "07"], [0.4, 0.35, 0.15, 0.10])}
    for a in range(n):
        letter = W["addr_letter"][a]
        answered_day = kept_day[a] if kept_day[a] is not None else None
        sent = [1]
        if kind[a] in ("refusal_contact",):
            pass
        if answered_day is None or answered_day > P.REMINDER_DAYS:
            sent.append(2)
        if (answered_day is None or answered_day > P.PAPER_MAILING_DAYS) and kind[a] != "refusal_contact":
            sent.append(3)
        mailings.append(sent)
        status = st_names[W["addr_status"][a]]
        pr = p_ret[status]
        for mnum in sent:
            if rs_post.random() < pr:
                off = {1: 0, 2: P.REMINDER_DAYS, 3: P.PAPER_MAILING_DAYS}[mnum]
                got = letter + dt.timedelta(days=off + int(rs_post.integers(5, 27)))
                codes_, pp = reasons[status]
                reason = str(rs_post.choice(codes_, p=pp))
                returns_post.append((a, mnum, got, reason))
    R["mailings"], R["returns_post"] = mailings, returns_post
    # ------------------------------------------------------------ helpdesk contacts
    contacts = []
    for a in replacement_cases:
        contacts.append((a, codes[case_codes[a][-1]][2] - dt.timedelta(days=int(rs_help.integers(0, 2))),
                         "codigo_acesso"))
    for a in range(n):
        letter = W["addr_letter"][a]
        if kind[a] == "refusal_contact":
            contacts.append((a, letter + dt.timedelta(days=int(rs_help.integers(1, 30))), "recusa"))
        u = rs_help.random()
        if u < 0.0026:
            contacts.append((a, letter + dt.timedelta(days=int(rs_help.integers(1, 35))), "quem_responde"))
        elif u < 0.0026 + 0.0042:
            contacts.append((a, letter + dt.timedelta(days=int(rs_help.integers(1, 35))), "pedido_papel"))
        elif u < 0.0026 + 0.0042 + 0.0035:
            contacts.append((a, letter + dt.timedelta(days=int(rs_help.integers(1, 35))), "problema_tecnico"))
        elif u < 0.0026 + 0.0042 + 0.0035 + 0.0021:
            contacts.append((a, letter + dt.timedelta(days=int(rs_help.integers(1, 40))), "outro"))
    R["contacts"] = contacts
    return R
