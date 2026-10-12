"""task501 independent verifier: recomputes the facility amount, the fees and the 2026 distributions received from target/
alone, with the standard library and openpyxl only (no pandas, nothing imported from solve.py), and compares them with
generator/figures.json. Exit 1 on any difference."""
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import date, timedelta

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
PLAN = date(2026, 12, 31)


def d_(s):
    y, m, d = s[:10].split("-")
    return date(int(y), int(m), int(d))


def month(d):
    return d.year * 12 + d.month - 1


def main():
    fails = []
    fig = json.load(open(os.path.join(HERE, "figures.json")))

    # reference rates, per one unit
    ref = defaultdict(dict)
    with open(os.path.join(T, "fx_referenzkurse_tagesende.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            ref[r["currency"]][d_(r["rate_date"])] = float(r["rate_chf"]) / float(r["unit"])

    def rate(day, ccy):
        ccy = ccy.strip().upper()
        if ccy == "CHF":
            return 1.0
        while day not in ref[ccy]:
            day -= timedelta(days=1)
        return ref[ccy][day]

    # the register
    wb = openpyxl.load_workbook(os.path.join(T, "fondsregister_2026-12-31.xlsx"), read_only=True)
    ws = wb["Fonds"]
    rows = list(ws.iter_rows(values_only=True))
    h = {k: i for i, k in enumerate(rows[0])}
    reg = {}
    for r in rows[1:]:
        if r[0] is None:
            continue
        ipd = r[h["investment_period_end"]]
        ipd = ipd.date() if hasattr(ipd, "date") else ipd
        fcd = r[h["first_close"]]
        fcd = fcd.date() if hasattr(fcd, "date") else fcd
        reg[r[h["fund_id"]]] = dict(ccy=r[h["currency"]], C=float(r[h["commitment"]]), ip=ipd, s=r[h["strategy"]], code=r[h["fund_code"]], fc=fcd)

    # the ledger
    calls = defaultdict(lambda: defaultdict(float))          # fund -> month -> CHF at the plan-date rate
    calls_fcy_to_ip = defaultdict(float)                      # fund -> calls with a value date on or before the period end
    notice_cash = defaultdict(float)                          # distribution notice -> cash amount (fund currency)
    notice_fund = {}
    with open(os.path.join(T, "kapitalabrufe_ausschuettungen_2015-2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["status"] != "ISSUED":
                continue
            fid = r["fund_id"]
            amt = float(r["amount"])
            vd = d_(r["value_date"])
            if r["notice_type"] == "CAPITAL_CALL":
                calls[fid][month(vd)] += amt * rate(PLAN, reg[fid]["ccy"])
                if vd <= reg[fid]["ip"]:
                    calls_fcy_to_ip[fid] += amt
            elif r["line_type"] != "IN_KIND":
                notice_cash[r["notice_id"]] += amt
                notice_fund[r["notice_id"]] = fid

    P = month(PLAN)
    window = range(P + 1, P + 13)
    funds = {}
    for fid, f in reg.items():
        ms = calls.get(fid, {})
        funds[fid] = dict(f, C_chf=f["C"] * rate(PLAN, f["ccy"]), calls=ms, first=min(ms) if ms else None, ipm=month(f["ip"]), fcm=month(f["fc"]))

    # the closed funds' drawn share at the end of their investment periods
    closed = [calls_fcy_to_ip[fid] / f["C"] for fid, f in funds.items() if f["ip"] <= PLAN]
    tau = sum(closed) / len(closed)

    # pooled call rates on unfunded commitment by band of age (12 months from the first call unless a corridor case says otherwise)
    def expected_calls(tau_, band=12, anchor="first"):
        num, den = defaultdict(float), defaultdict(float)
        for f in funds.values():
            if f["first"] is None:
                continue
            a0 = f["first"] if anchor == "first" else f["fcm"]
            drawn = 0.0
            for m in range(f["first"], P + 1):
                unf = f["C_chf"] - drawn
                c = f["calls"].get(m, 0.0)
                if unf > 1.0:
                    b = (m - a0) // band
                    num[b] += c
                    den[b] += unf
                drawn += c
        band_rate = {b: num[b] / den[b] for b in num}

        def r_for(b):
            if b in band_rate:
                return band_rate[b]
            lower = [k for k in band_rate if k <= b]
            return band_rate[max(lower)] if lower else band_rate[min(band_rate)]

        def run_off(f, months, unf):
            out = 0.0
            a0 = f["first"] if anchor == "first" else f["fcm"]
            for m in months:
                c = min(unf, r_for((m - a0) // band) * unf)
                unf -= c
                out += c
            return out

        total = 0.0
        for f in funds.values():
            if f["first"] is None:
                continue
            drawn = sum(v for m, v in f["calls"].items() if m <= P)
            unf = f["C_chf"] - drawn
            if window[0] <= f["ipm"] <= window[-1]:
                need = max(0.0, tau_ * f["C_chf"] - drawn)
                total += need + run_off(f, [m for m in window if m > f["ipm"]], max(0.0, unf - need))
            else:
                total += run_off(f, window, unf)
        return total

    expected = expected_calls(tau)
    req = 1.1 * expected - 150e6
    amount = next(a for a in range(50, 401, 25) if a * 1e6 >= req)
    fees = round(amount * 1e6 * (0.0030 + 0.0015))
    fees_down = round((amount - 25) * 1e6 * (0.0030 + 0.0015))

    def check(name, mine, theirs):
        if mine != theirs:
            fails.append(f"{name}: verify {mine} against figures.json {theirs}")

    check("facility amount", amount, fig["call_amount_chf_m"])
    check("expected calls", round(expected / 1e6, 1), fig["expected_calls_chf_m"])
    check("requirement", round(req / 1e6, 1), fig["requirement_chf_m"])
    check("fees at the amount", fees, fig["fees_at_amount_chf"])
    check("fees at the next amount down", fees_down, fig["fees_at_next_down_chf"])
    check("closed funds' mean drawn share", round(100 * tau, 1), fig["closed_share_mean_pct"])
    # the corridor (C3): the lowest and highest drawn share of a closed fund, 6- and 24-month bands, age from the first close
    lo_e, hi_e = (amount - 25 + 150) / 1.1 * 1e6, (amount + 150) / 1.1 * 1e6
    corridor = {"lowest drawn share": expected_calls(min(closed)), "highest drawn share": expected_calls(max(closed)),
                "6-month bands": expected_calls(tau, band=6), "24-month bands": expected_calls(tau, band=24),
                "age from the first close": expected_calls(tau, anchor="close")}
    for name, e in corridor.items():
        if not (e >= 1.02 * lo_e and e <= 0.98 * hi_e):
            fails.append(f"corridor {name}: expected calls {e / 1e6:.1f} not 2 per cent inside {lo_e / 1e6:.1f} to {hi_e / 1e6:.1f}")

    # the ask: each 2026 credit of a distribution on the programme account, at the notice's cash amount and the reference
    # rate of the credit's value date
    grid = defaultdict(float)
    with open(os.path.join(T, "programmkonto_lindenhof_2025-2026.csv"), encoding="utf-8") as fh:
        for r in csv.DictReader(fh, delimiter=";"):
            if r["Buchungstext"] != "Gutschrift Ausschuettung":
                continue
            vd = d_(r["Valuta"])
            if vd.year != 2026:
                continue
            keys = [k for k in (r["Transaktionsreferenz"], r["Referenz"].split(" ")[0]) if k in notice_cash]
            if not keys:
                fails.append(f"credit {r['Transaktionsreferenz']} has no notice")
                continue
            fid = notice_fund[keys[0]]
            chf = notice_cash[keys[0]] * rate(vd, reg[fid]["ccy"])
            q = (vd.month - 1) // 3 + 1
            grid[(reg[fid]["s"], q)] += chf
    for s in ("BO", "GR", "PC", "IN"):
        for q in (1, 2, 3, 4):
            check(f"{s} Q{q}", round(grid[(s, q)] / 1000), fig["distributions_2026_chf_k"][f"{s}_Q{q}"])
        check(f"{s} year", round(sum(grid[(s, q)] for q in (1, 2, 3, 4)) / 1000), fig["distributions_2026_chf_k"][f"{s}_year"])
    for q in (1, 2, 3, 4):
        check(f"total Q{q}", round(sum(grid[(s, q)] for s in ("BO", "GR", "PC", "IN")) / 1000), fig["distributions_2026_chf_k"][f"total_Q{q}"])
    names = {"BO": "Buyout", "GR": "Growth", "PC": "Private credit", "IN": "Infrastructure"}
    top = max(("BO", "GR", "PC", "IN"), key=lambda s: sum(grid[(s, q)] for q in (1, 2, 3, 4)))
    check("top strategy", names[top], fig["top_strategy"])

    for f_ in fails:
        print("VERIFY FAIL:", f_)
    print(f"verify: facility CHF {amount} million (expected calls {expected / 1e6:.1f}, requirement {req / 1e6:.1f}), fees {fees:,} and "
          f"{fees_down:,}; distributions {sum(grid.values()) / 1000:,.0f} thousand, top {names[top]}; {len(fails)} differences")
    return len(fails)


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
