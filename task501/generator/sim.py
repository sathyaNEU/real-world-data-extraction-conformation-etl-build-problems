"""task501 simulation: every fund's calls, investments, exits, distributions and valuations, month by month.

The world runs from 2015 to the end of 2027; only what the systems held on 31 December 2026 is written to the pack
(pack.py). The 2027 calls are kept as the world's own outcome for the design note and are never shipped.
"""
import math
from dataclasses import dataclass, field
from datetime import date, timedelta

import numpy as np

import world as W

COMPANY_PRE = ["Nor", "Vel", "Kar", "Bel", "Tam", "Ost", "Lir", "Fen", "Mar", "Sol", "Hal", "Dor", "Rav", "Tor",
               "Quin", "Ald", "Bran", "Cor", "Dun", "Eber", "Gal", "Hel", "Ira", "Jor", "Kel", "Lun", "Mol", "Nev",
               "Orl", "Pal", "Ren", "Sab", "Tal", "Ulm", "Var", "Wen", "Yor", "Zel", "Ant", "Bor", "Cas", "Dal",
               "Ems", "Fal", "Gor", "Hav", "Isk", "Jas", "Kor", "Lom", "Mer", "Nol", "Oss", "Pir", "Rud", "Sev"]
COMPANY_SUF = ["tek", "mat", "vion", "dyne", "core", "line", "works", "sys", "med", "logis", "pharma", "grid",
               "net", "fab", "form", "wave", "steel", "pack", "data", "care", "build", "fleet", "hydro", "optic",
               "chem", "soft", "port", "rail", "power", "foods", "labs", "metrics"]
LEGAL = {"DE": "GmbH", "FR": "SAS", "NL": "B.V.", "GB": "Ltd", "US": "Inc.", "CH": "AG", "IT": "S.p.A.", "ES": "S.L.",
         "SE": "AB", "DK": "A/S", "AT": "GmbH", "BE": "NV", "IE": "Ltd", "FI": "Oy", "NO": "AS", "PL": "Sp. z o.o."}
COUNTRIES = list(LEGAL)
# NACE Rev. 2 sections as the managers report them
SECTORS = ["C Manufacturing", "J Information and communication", "M Professional, scientific and technical activities",
           "Q Human health and social work", "G Wholesale and retail trade", "H Transportation and storage",
           "D Electricity, gas, steam and air conditioning supply", "N Administrative and support service activities",
           "F Construction", "K Financial and insurance activities", "E Water supply, sewerage, waste management",
           "I Accommodation and food service activities"]
INFRA_SECTORS = ["D Electricity, gas, steam and air conditioning supply", "H Transportation and storage",
                 "E Water supply, sewerage, waste management", "J Information and communication"]
INSTR = {"BO": "Equity", "GR": "Preferred equity", "PC": "Senior secured loan", "IN": "Equity"}
LEI_PREFIX = {"DE": "5299", "GB": "2138", "FR": "9695", "US": "5493", "CH": "5067", "SE": "5493", "NO": "5967",
              "DK": "5299", "IE": "6354"}


def lei_for(rng, country):
    body = LEI_PREFIX.get(country, "5493") + "00" + "".join(rng.choice(list("ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"), 12))
    s = "".join(str(int(c, 36)) for c in body) + "00"
    return body + f"{98 - int(s) % 97:02d}"


@dataclass
class Investment:
    ref: str
    company: str
    country: str
    sector: str
    instrument: str
    initial_date: date
    cost: float = 0.0
    tranches: list = field(default_factory=list)
    hold_days: int = 0
    exit_date: date = None
    multiple: float = 1.0
    status: str = "HELD"
    realised_cost: float = 0.0
    realised_gain: float = 0.0
    exit_kind: str = ""


@dataclass
class Fund:
    idx: int
    fund_id: str
    code: str
    mcode: str
    number: str
    name: str
    manager: str
    strategy: str
    ccy: str
    domicile: str
    paying_agent: str
    vintage: int
    commitment: float
    first_close: date
    final_close: date
    ip_end: date
    term_end: date
    lei: str
    pace: float
    iota: float
    fee_ip: float
    fee_post: float
    first_call_idx: int = None
    inv: float = 0.0
    called: float = 0.0
    calls_by_month: dict = field(default_factory=dict)      # month index -> total called (the world's record)
    investments: list = field(default_factory=list)
    notices: list = field(default_factory=list)
    nav_q: dict = field(default_factory=dict)
    n_inv: int = 0
    n_cn: int = 0
    n_dn: int = 0


def build_funds():
    rng = np.random.RandomState(W.SEED * 7)
    funds = []
    for i, (mc, num, (vy, vm), cm, pace) in enumerate(W.FUNDS):
        mname, code, strat, ccy, dom, agent, _ = W.MANAGERS[W.MGR[mc]]
        fc = date(vy, vm, int(rng.randint(4, 27)))
        fee_ip = W.FEE_IP[strat] + float(rng.choice([-0.001, 0.0, 0.0, 0.001]))
        f = Fund(idx=i, fund_id=f"PKW-F-{101 + i:03d}", code=f"{code}-{num}", mcode=code, number=num, name=f"{mname} {num}",
                 manager=mname, strategy=strat, ccy=ccy, domicile=dom, paying_agent=agent, vintage=vy,
                 commitment=cm * 1_000_000.0, first_close=fc, final_close=W.add_months(fc, int(rng.randint(6, 15))),
                 ip_end=W.add_months(fc, W.IP_MONTHS[strat]), term_end=W.add_months(fc, W.TERM_MONTHS[strat]),
                 lei=lei_for(rng, dom), pace=pace * float(rng.uniform(0.93, 1.07)),
                 iota=W.TAU_TARGET - fee_ip * W.IP_MONTHS[strat] / 12.0 - 0.002 + float(rng.normal(0, W.IOTA_SD)),
                 fee_ip=fee_ip, fee_post=W.FEE_POST[strat])
        funds.append(f)
    return funds


# ---------------------------------------------------------------- reference rates
def build_fx():
    """Custodian 16:00 reference rates on business days, 2 January 2015 to 31 December 2026 (CHF per USD and EUR)."""
    rng = np.random.RandomState(W.SEED * 11)
    anchors_usd = [(date(2015, 1, 1), 0.995), (date(2016, 6, 30), 0.975), (date(2018, 6, 30), 0.990), (date(2020, 3, 31), 0.965),
                   (date(2021, 6, 30), 0.915), (date(2022, 10, 31), 0.995), (date(2023, 12, 31), 0.845), (date(2024, 6, 30), 0.895),
                   (date(2025, 6, 30), 0.810), (date(2026, 6, 30), 0.790), (date(2026, 12, 31), 0.785)]
    anchors_eur = [(date(2015, 1, 1), 1.200), (date(2015, 2, 15), 1.065), (date(2017, 12, 31), 1.165), (date(2019, 12, 31), 1.090),
                   (date(2021, 6, 30), 1.095), (date(2022, 9, 30), 0.960), (date(2023, 12, 31), 0.935), (date(2024, 6, 30), 0.965),
                   (date(2025, 6, 30), 0.935), (date(2026, 6, 30), 0.928), (date(2026, 12, 31), 0.931)]

    def target(anchors, d):
        for (d0, v0), (d1, v1) in zip(anchors, anchors[1:]):
            if d0 <= d <= d1:
                t = (d - d0).days / max((d1 - d0).days, 1)
                return v0 + (v1 - v0) * t
        return anchors[-1][1]

    rows = []
    u, e = 0.995, 1.200
    d = date(2015, 1, 2)
    while d <= W.PLAN_DATE:
        if d.weekday() < 5 and (d.month, d.day) not in ((1, 1), (12, 25), (12, 26), (1, 2), (8, 1)):
            u += 0.12 * (target(anchors_usd, d) - u) + rng.normal(0, 0.0034)
            e += 0.12 * (target(anchors_eur, d) - e) + rng.normal(0, 0.0024)
            rows.append((d, round(u, 4), round(e, 4)))
        d += timedelta(days=1)
    return rows


class FX:
    def __init__(self, rows):
        self.t = {d: (u, e) for d, u, e in rows}
        self.days = sorted(self.t)

    def rate(self, d, ccy):
        if ccy == "CHF":
            return 1.0
        while d not in self.t:
            d -= timedelta(days=1)
        u, e = self.t[d]
        return u if ccy == "USD" else e


# ---------------------------------------------------------------- the simulation
def _new_investment(f, rng, value_date, part, names, in_ip):
    s = f.strategy
    f.n_inv += 1
    while True:
        ctry = COUNTRIES[int(rng.randint(len(COUNTRIES)))] if rng.rand() < 0.7 else f.domicile
        nm = COMPANY_PRE[int(rng.randint(len(COMPANY_PRE)))] + COMPANY_SUF[int(rng.randint(len(COMPANY_SUF)))]
        nm = nm[0].upper() + nm[1:] + " " + LEGAL[ctry]
        if nm not in names:
            names.add(nm)
            break
    sector = INFRA_SECTORS[int(rng.randint(len(INFRA_SECTORS)))] if s == "IN" else SECTORS[int(rng.randint(len(SECTORS)))]
    iv = Investment(ref=f"{f.code}-{f.n_inv:02d}", company=nm, country=ctry, sector=sector, instrument=INSTR[s],
                    initial_date=value_date, cost=part, tranches=[(value_date, part)])
    mean, sd, lo, hi = W.HOLD[s]
    months = float(np.clip(rng.normal(mean, sd), lo, hi))
    hold = int(months * 30.44 + rng.randint(0, 28))
    ex = value_date + timedelta(days=hold)
    if ex.month == 12 and ex.day >= 12:
        ex += timedelta(days=30)
    iv.hold_days = (ex - value_date).days
    iv.exit_date = ex
    mmean, msd = W.MULT[s]
    if rng.rand() < W.LOSS_SHARE[s]:
        iv.multiple = float(rng.uniform(0.3, 0.93)) if s != "PC" else float(rng.uniform(0.6, 0.95))
    else:
        iv.multiple = float(max(1.0, rng.normal(mmean, msd))) if s != "PC" else float(rng.uniform(1.0, 1.06))
    f.investments.append(iv)
    return iv


def _call_dates(rng, y, m, f, months_left):
    nd = W.bday(date(y, m, int(rng.randint(2, 21))))
    vd = W.add_bdays(nd, int(rng.randint(8, 11)))
    if m == 12 and vd.year != y:
        vd = W.bday_back(date(y, 12, 22))
        nd = min(nd, W.bday_back(vd - timedelta(days=12)))
    if months_left == 0 or nd <= f.ip_end < vd:  # the period's last call is due by its end; nothing straddles it
        vd = W.bday_back(f.ip_end)
        nd = W.bday_back(vd - timedelta(days=13))
    if months_left < 0 and nd <= f.ip_end:      # a call after the period is noticed after it
        nd = W.add_bdays(f.ip_end, 1)
        vd = W.add_bdays(nd, 9)
    return nd, vd


def simulate():
    funds = build_funds()
    fx_rows = build_fx()
    names = set()
    last_idx = W.month_index(*W.FORWARD_END)
    for f in funds:
        rng = np.random.RandomState(W.SEED * 1000 + f.idx)
        s = f.strategy
        C = f.commitment
        fc_idx = W.month_index(f.first_close.year, f.first_close.month)
        f.first_call_idx = fc_idx + int(rng.randint(1, 3))
        ip_idx = W.month_index(f.ip_end.year, f.ip_end.month)
        term_idx = W.month_index(f.term_end.year, f.term_end.month)
        pending = []
        for i in range(f.first_call_idx, last_idx + 1):
            y, mo = W.ym(i)
            months_left = ip_idx - i
            in_ip = months_left >= 0
            # ---------------- capital called for investments
            amt = 0.0
            if in_ip:
                rem = max(0.0, f.iota * C - f.inv)
                age = i - f.first_call_idx
                ramp = min(1.0, 0.35 + 0.65 * age / 12.0)          # a new fund takes about a year to reach its pace
                exp = W.H[s] * f.pace * W.market(y, mo) * rem * ramp
                if months_left < W.DRAWDOWN_MONTHS:
                    exp = max(exp, rem / (months_left + 1))
                    amt = rem if months_left == 0 else exp * float(rng.uniform(0.85, 1.15))
                elif i == f.first_call_idx:
                    amt = C * float(rng.uniform(0.035, 0.065))      # the first call: the first deal and the opening fees
                else:
                    amt = (exp / 0.45) * float(np.exp(rng.normal(0, 0.35))) if rng.rand() < 0.45 else 0.0
                amt = min(amt, rem)
            elif i <= term_idx:
                age_post = i - ip_idx
                exp = 0.022 * max(0.0, C - f.called) * math.exp(-age_post / 36.0)
                amt = (exp / 0.3) * float(np.exp(rng.normal(0, 0.4))) if rng.rand() < 0.3 else 0.0
            amt = math.floor(min(amt, max(0.0, 0.985 * C - f.called)) / 1000.0) * 1000.0
            if amt < 0.002 * C and not (in_ip and months_left == 0):
                amt = 0.0 if amt < 0.0008 * C else amt
            # ---------------- fees and expenses
            fee = 0.0
            exps = 0.0
            if mo in (1, 4, 7, 10) and in_ip:
                # the management fee is called on commitment during the investment period; afterwards the managers
                # deduct it from proceeds, so it is never called again
                fee = round(f.fee_ip * C / 4.0, 2)
                if rng.rand() < 0.35:
                    exps = round(C * float(rng.uniform(0.0002, 0.0007)), 2)
            room = max(0.0, C - f.called)
            amt = min(amt, math.floor(room / 1000.0) * 1000.0)
            fee = min(fee, round(math.floor((room - amt) * 100) / 100.0, 2))
            exps = min(exps, round(math.floor((room - amt - fee) * 100) / 100.0, 2))
            lines = []
            if amt > 0 or fee > 0 or exps > 0:
                nd, vd = _call_dates(rng, y, mo, f, months_left)
                if amt > 0:
                    n_parts = 1 if amt < 0.02 * C else int(rng.choice([1, 2, 2, 3]))
                    parts = rng.dirichlet(np.ones(n_parts) * 3) * amt if n_parts > 1 else np.array([amt])
                    parts = [math.floor(p / 1000.0) * 1000.0 for p in parts]
                    parts[-1] += amt - sum(parts)
                    for part in parts:
                        if part <= 0:
                            continue
                        held = [iv for iv in f.investments if iv.status == "HELD" and iv.exit_date > vd + timedelta(days=60)]
                        follow = held and (not in_ip or rng.rand() < 0.28)
                        if follow:
                            iv = held[int(rng.randint(len(held)))]
                            iv.cost += part
                            iv.tranches.append((vd, part))
                            lines.append(("INVESTMENT", iv.ref, f"Follow-on investment in {iv.company}", part))
                        else:
                            iv = _new_investment(f, rng, vd, part, names, in_ip)
                            pending.append(iv)
                            lines.append(("INVESTMENT", iv.ref, f"Investment in {iv.company}", part))
                    f.inv += amt
                if fee > 0:
                    lines.append(("MANAGEMENT_FEE", "", f"Management fee Q{(mo - 1) // 3 + 1} {y}", fee))
                if exps > 0:
                    lines.append(("PARTNERSHIP_EXPENSES", "", "Partnership expenses", exps))
                total = sum(l[3] for l in lines)
                f.called += total
                f.calls_by_month[i] = f.calls_by_month.get(i, 0.0) + total
                f.n_cn += 1
                f.notices.append(dict(notice_id=f"{f.code}-CN-{f.n_cn:03d}", type="CAPITAL_CALL", notice_date=nd,
                                      value_date=vd, arrival=vd, lines=lines, status="ISSUED", remarks="", source="clerk"))
            # ---------------- exits this month
            dlines = []
            exits = [iv for iv in pending if iv.exit_date.year == y and iv.exit_date.month == mo]
            for iv in exits:
                pending.remove(iv)
                iv.status = "REALISED"
                proceeds = iv.cost * iv.multiple
                roc = round(min(iv.cost, proceeds), 2)
                gain = round(max(0.0, proceeds - iv.cost), 2)
                iv.realised_cost, iv.realised_gain = roc, gain
                dlines.append(("RETURN_OF_CAPITAL", iv.ref, f"Realisation of {iv.company}: return of capital", roc))
                if gain > 0:
                    dlines.append(("REALISED_GAIN", iv.ref, f"Realisation of {iv.company}: realised gain", gain))
            if mo in (3, 6, 9, 12) and W.INCOME_Q[s] > 0:
                for iv in f.investments:
                    if iv.status == "HELD" and iv.initial_date <= date(y, mo, 1):
                        inc = round(iv.cost * W.INCOME_Q[s] * float(rng.uniform(0.85, 1.15)), 2)
                        if inc > 0:
                            dlines.append(("INCOME", iv.ref, f"Income distribution Q{(mo - 1) // 3 + 1} {y}: {iv.company}", inc))
            elif W.INCOME_Q[s] == 0 and rng.rand() < 0.03:
                held = [iv for iv in f.investments if iv.status == "HELD"]
                if held:
                    iv = held[int(rng.randint(len(held)))]
                    inc = round(iv.cost * float(rng.uniform(0.04, 0.12)), 2)
                    dlines.append(("INCOME", iv.ref, f"Dividend recapitalisation: {iv.company}", inc))
            if dlines:
                if exits:
                    nd = W.bday(exits[0].exit_date + timedelta(days=int(rng.randint(3, 10))))
                elif W.INCOME_Q[s] > 0 and mo in (3, 6, 9, 12):
                    nd = W.bday_back(date(y, mo, int(rng.randint(16, 23))))
                else:
                    nd = W.bday(date(y, mo, int(rng.randint(3, 22))))
                if W.INCOME_Q[s] > 0 and mo in (3, 6, 9, 12) and not exits:
                    vd = W.bday_back(W.month_end(i) - timedelta(days=int(rng.choice([0, 0, 0, 1, 2]))))
                else:
                    vd = W.add_bdays(nd, int(rng.randint(5, 9)))
                f.n_dn += 1
                f.notices.append(dict(notice_id=f"{f.code}-DN-{f.n_dn:03d}", type="DISTRIBUTION", notice_date=nd,
                                      value_date=vd, arrival=vd, lines=dlines, status="ISSUED", remarks="", source="clerk"))
            # ---------------- quarterly valuation
            if mo in (3, 6, 9, 12):
                qe = W.month_end(i)
                nav = 0.0
                for iv in f.investments:
                    if iv.status == "HELD" and iv.initial_date <= qe:
                        prog = min(1.0, (qe - iv.initial_date).days / max(iv.hold_days, 1))
                        nav += iv.cost * (1.0 + (iv.multiple - 1.0) * prog ** 1.3)
                f.nav_q[(y, (mo - 1) // 3 + 1)] = round(nav, 2)
        assert f.called <= f.commitment + 0.01, f.code
    return funds, fx_rows


def world_calls_2027(funds, fx):
    """The world's own 2027 calls by value date at the plan-date rate (the record, never shipped)."""
    tot = 0.0
    for f in funds:
        r = fx.rate(W.PLAN_DATE, f.ccy)
        for n in f.notices:
            if n["type"] == "CAPITAL_CALL" and n["status"] == "ISSUED" and n["value_date"].year == 2027:
                tot += sum(l[3] for l in n["lines"]) * r
    return tot
