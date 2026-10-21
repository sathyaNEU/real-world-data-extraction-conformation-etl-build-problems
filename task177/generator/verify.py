"""task177 verify: an independent recomputation from the shipped bundle alone (target/, the goldens, figures.json),
on its own code path: pandas for the exports, its own likelihood, its own optimiser settings and its own simulation.

    python3 task177/generator/verify.py <target>

Exit 1 when a graded figure does not reproduce."""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
OUT = []


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond)))
    print("%-4s %-62s %s" % ("PASS" if cond else "FAIL", label, detail), flush=True)


def pdf(path):
    from pypdf import PdfReader
    return " ".join(" ".join((p.extract_text() or "") for p in PdfReader(path).pages).split())


def winnipeg_to_utc(ts):
    """Manitoba local times (naive) to UTC: CDT from the second Sunday of March 02:00 to the first Sunday of November"""
    def bounds(y):
        m = pd.Timestamp(y, 3, 1)
        s2 = m + pd.Timedelta(days=(6 - m.weekday()) % 7 + 7)
        n = pd.Timestamp(y, 11, 1)
        s1 = n + pd.Timedelta(days=(6 - n.weekday()) % 7)
        return s2 + pd.Timedelta(hours=2), s1 + pd.Timedelta(hours=2)
    out = ts.copy()
    for y in sorted(set(ts.dt.year)):
        a, b = bounds(y)
        sel = ts.dt.year == y
        summer = sel & (ts >= a) & (ts < b)
        out[sel] = ts[sel] + pd.Timedelta(hours=6)
        out[summer] = ts[summer] + pd.Timedelta(hours=5)
    return out


def utc_to_winnipeg(ts):
    loc = ts - pd.Timedelta(hours=6)
    back = winnipeg_to_utc(loc)
    summer = back != ts
    loc[summer] = ts[summer] - pd.Timedelta(hours=5)
    return loc


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    plan = pdf(os.path.join(target, "assistant_first_rollout_plan.pdf"))
    acc = pdf(os.path.join(target, "release4_acceptance_summary.pdf"))
    order = pdf(os.path.join(target, "usage_tier_order_form_2027.pdf"))
    ok("plan reads back (control: section 2.1)", "answers every call that reaches the Claimant Services queue" in plan)
    ok("acceptance summary reads back (control: the criterion)", "Acceptance criterion" in acc)
    ok("order form reads back (control: the tenant)", "prairieworks-mb (production)" in order)
    m = re.search(r"All intents ([\d,]+) ([\d,]+) ([\d.]+)%", acc)
    p_new = int(m.group(2).replace(",", "")) / int(m.group(1).replace(",", ""))
    cycle = int(re.search(r"checks in every (\d+) days", plan).group(1))
    bn = re.search(r"Business number (\d{9})", order).group(1)
    ok("filed inputs: release 4.0 resolved share, check-in cycle, business number", 0.8 < p_new < 0.9 and cycle == 14,
       "%.4f, %d days, %s" % (p_new, cycle, bn))

    # ------------------------------------------------------------------------------------------- the contacts
    legs = pd.read_csv(os.path.join(target, "contact_legs_2026.csv"), dtype=str, keep_default_na=False)
    cl = legs[legs.line_dnis == "2049450100"].copy()
    cl["leg_no"] = cl.leg_no.astype(int)
    cl = cl.sort_values(["interaction_id", "leg_no"])
    first = cl.groupby("interaction_id").first()
    first = first[first.caller_entered != ""]
    xfer = cl[(cl.leg_result.isin(["XFR", "transferred"])) & (cl.transfer_to == "ASKPW-VOICE")].interaction_id.unique()
    agents = cl[cl.leg_type.isin(["AGT", "agent"])].groupby("interaction_id").disposition.last()
    sess = pd.read_json(os.path.join(target, "assistant_sessions_2026.jsonl"), lines=True, dtype=False)
    voice = sess[sess.channel == "voice"].set_index("call_ref").end_state
    calls = pd.DataFrame({"case": first.caller_entered, "t": pd.to_datetime(first.start_utc.str[:19])})
    calls["chose"] = False
    calls["red"] = calls.index.isin(xfer)
    calls["res"] = np.where(calls.red, calls.index.map(voice).fillna("") == "resolved",
                            calls.index.map(agents).fillna("").isin(["RS", "RESOLVED"]))
    xw = pd.read_csv(os.path.join(target, "contact_details_crosswalk.csv"), dtype=str, keep_default_na=False)
    link = xw[xw.detail_type == "assistant_account"].set_index("detail_value").case_no
    chat = sess[sess.channel.isin(["app", "web"])].sort_values(["conversation_id", "started"])
    g = chat.groupby("conversation_id")
    conv = pd.DataFrame({"acct": g.account_ref.first(), "start": g.started.first(), "end": g.end_state.last()})
    conv["case"] = conv.acct.map(link)
    conv = conv[conv.case.notna()]
    conv_t = winnipeg_to_utc(pd.to_datetime(conv.start))
    chats = pd.DataFrame({"case": conv.case.values, "t": conv_t.values, "chose": True, "red": False,
                          "res": (conv.end == "resolved").values})
    reg = pd.read_csv(os.path.join(target, "claims_register_2026.csv"), dtype=str, keep_default_na=False)
    cases = set(reg.case_no)
    allc = pd.concat([calls.reset_index(drop=True), chats], ignore_index=True)
    allc = allc[allc.case.isin(cases)].sort_values(["case", "t"]).reset_index(drop=True)
    ok("contacts rebuilt", len(allc) == fig["n_contacts"], "%d" % len(allc))
    ok("overflow transfers", int(allc.red.sum()) == fig["n_redirects"], "%d" % allc.red.sum())

    # ------------------------------------------------------------------------- the likelihood, written afresh
    allc["k"] = allc.groupby("case").cumcount()
    sizes = allc.groupby("case").size().sort_values(ascending=False, kind="stable")
    order_cases = list(sizes.index)
    row_of = {c: i for i, c in enumerate(order_cases)}
    N, L = len(order_cases), int(sizes.max())
    ri = allc.case.map(row_of).values
    ki = allc.k.values
    CH = np.zeros((N, L), bool); RD = np.zeros((N, L), bool); RS = np.zeros((N, L))
    CH[ri, ki] = allc.chose.values
    RD[ri, ki] = allc.red.values
    RS[ri, ki] = allc.res.values.astype(float)
    alive = (sizes.values[None, :] > np.arange(L)[:, None]).sum(1)

    def negll(theta, rates_tied=False, want_state=False):
        af = 1 / (1 + np.exp(-theta[0]))
        ao = af if rates_tied else 1 / (1 + np.exp(-theta[1]))
        j = 1 if rates_tied else 2
        be, bi, ka = np.exp(theta[j]), theta[j + 1], theta[j + 2]
        vb = np.full(N, 0.5); vp = np.full(N, 0.5); lc = np.zeros(N)
        tot = 0.0
        for t in range(L):
            n = alive[t]
            z = be * (vb[:n] - vp[:n]) + bi + ka * lc[:n]
            c = CH[:n, t]
            tot += np.sum(np.log1p(np.exp(-np.abs(z))) + np.maximum(-z, 0) * c + np.maximum(z, 0) * (~c))
            met_asst = c | RD[:n, t]
            lr = np.where(RD[:n, t], ao, af)
            vb[:n] = np.where(met_asst, vb[:n] + lr * (RS[:n, t] - vb[:n]), vb[:n])
            vp[:n] = np.where(met_asst, vp[:n], vp[:n] + af * (RS[:n, t] - vp[:n]))
            lc[:n] = np.where(c, 1.0, -1.0)
        if want_state:
            return tot, vb, vp, lc
        return tot
    fit = minimize(negll, np.array([0.0, -2.0, 1.6, -0.3, 0.2]), method="L-BFGS-B",
                   options={"maxiter": 500, "eps": 1e-6})
    fit1 = minimize(lambda x: negll(x, True), np.array([0.0, 1.6, -0.3, 0.2]), method="L-BFGS-B",
                    options={"maxiter": 500, "eps": 1e-6})
    th = fit.x
    af, ao = 1 / (1 + np.exp(-th[0])), 1 / (1 + np.exp(-th[1]))
    ok("the transfer rate is about a fifth of the chosen rate", abs(ao / af - fig["ratio"]) < 0.03,
       "%.3f / %.3f = %.3f" % (ao, af, ao / af))
    ok("the split model beats one rate by the stated margin", abs((fit1.fun - fit.fun) - fig["ll_gain_one_rate"]) < 5,
       "%.1f" % (fit1.fun - fit.fun))

    # ------------------------------------------------------------------------------- the forward simulation
    reg["opened_d"] = pd.to_datetime(reg.opened)
    reg["closed_d"] = pd.to_datetime(reg.closed.replace("", None))
    popdate = pd.Timestamp(2027, 1, 3)
    pop = reg[(reg.opened_d <= popdate) & (reg.closed_d.isna() | (reg.closed_d >= popdate))]
    ok("the planning population", len(pop) == fig["n_pop"], "%d" % len(pop))
    af_s, af_e = pd.Timestamp(2027, 1, 4), pd.Timestamp(2027, 2, 28)
    w_s, w_e = pd.Timestamp(2027, 3, 1), pd.Timestamp(2027, 4, 25)

    def dues(o, a, b):
        k0 = int(np.ceil(max((a - o).days, 1) / cycle))
        n = 0
        while True:
            d = o + pd.Timedelta(days=cycle * k0)
            if d > b:
                return n
            n += d >= a
            k0 += 1
    s_af = np.array([dues(o, af_s, af_e) for o in pop.opened_d])
    s_w = np.array([dues(o, w_s, w_e) for o in pop.opened_d])
    phone = allc[~allc.chose & ~allc.red]
    p_ph = phone.res.mean()
    p_ov = allc.red.sum() / (~allc.chose).sum()
    # questions between check-ins: every contact not a check-in, per claim-day open in the record
    chk_calls = set(first[first.menu_path == "1>1"].index)
    n_chk = len(calls[calls.index.isin(chk_calls) & calls.case.isin(cases)])
    n_chk += int((chat.groupby("conversation_id").intent.first().reindex(conv.index) == "check_in").sum())
    rs, re_ = pd.Timestamp(2026, 1, 5), pd.Timestamp(2027, 1, 3)
    days = ((reg.closed_d.fillna(re_).clip(upper=re_) - reg.opened_d.clip(lower=rs)).dt.days + 1).clip(lower=0).sum()
    adhoc = (len(allc) - n_chk) / days

    def forward(theta, tied, reps, seed):
        tot, vb, vp, lc = negll(theta, tied, want_state=True)
        a_f = 1 / (1 + np.exp(-theta[0]))
        a_o = a_f if tied else 1 / (1 + np.exp(-theta[1]))
        j = 1 if tied else 2
        be, bi, ka = np.exp(theta[j]), theta[j + 1], theta[j + 2]
        idx = np.array([row_of.get(c, -1) for c in pop.case_no])
        have = idx >= 0
        b0 = np.where(have, vb[np.maximum(idx, 0)], 0.5)
        p0 = np.where(have, vp[np.maximum(idx, 0)], 0.5)
        l0 = np.where(have, lc[np.maximum(idx, 0)], 0.0)
        rng = np.random.default_rng(seed)
        hit = seen = 0
        for _ in range(reps):
            b, p, la = b0.copy(), p0.copy(), l0.copy()
            for phase, nd, sch in ((0, 56, s_af), (1, 56, s_w)):
                nk = sch + rng.poisson(adhoc * nd, size=len(pop))
                for t in range(int(nk.max())):
                    i = np.flatnonzero(nk > t)
                    want = rng.random(i.size) < 1 / (1 + np.exp(-(be * (b[i] - p[i]) + bi + ka * la[i])))
                    sent = (~want) & ((phase == 0) | (rng.random(i.size) < p_ov))
                    met = want | sent
                    good = np.where(met, rng.random(i.size) < p_new, rng.random(i.size) < p_ph)
                    lr = np.where(sent, a_o, a_f)
                    b[i] = np.where(met, b[i] + lr * (good - b[i]), b[i])
                    p[i] = np.where(met, p[i], p[i] + a_f * (good - p[i]))
                    la[i] = np.where(want, 1.0, -1.0)
                    if phase == 1:
                        hit += want.sum(); seen += i.size
        return hit / seen
    # the back-test the note quotes: both models fitted to the contacts before 1 November 2026
    cut_t = pd.Timestamp(2026, 11, 1, 5)          # 00:00 CDT is 05:00 UTC
    early = (allc.t.values < cut_t.to_datetime64())
    held = np.zeros((N, L), bool)
    held[ri, ki] = ~early

    def negll_masked(theta, tied, mask_fit):
        global_mask = mask_fit
        af_ = 1 / (1 + np.exp(-theta[0]))
        ao_ = af_ if tied else 1 / (1 + np.exp(-theta[1]))
        j = 1 if tied else 2
        be_, bi_, ka_ = np.exp(theta[j]), theta[j + 1], theta[j + 2]
        vb = np.full(N, 0.5); vp = np.full(N, 0.5); lc = np.zeros(N)
        tot = 0.0; pr = 0.0
        for t in range(L):
            n = alive[t]
            z = be_ * (vb[:n] - vp[:n]) + bi_ + ka_ * lc[:n]
            c = CH[:n, t]
            mk = global_mask[:n, t]
            term = np.log1p(np.exp(-np.abs(z))) + np.maximum(-z, 0) * c + np.maximum(z, 0) * (~c)
            tot += np.sum(term[mk])
            pr += np.sum((1 / (1 + np.exp(-z)))[mk])
            met = c | RD[:n, t]
            lr = np.where(RD[:n, t], ao_, af_)
            vb[:n] = np.where(met, vb[:n] + lr * (RS[:n, t] - vb[:n]), vb[:n])
            vp[:n] = np.where(met, vp[:n], vp[:n] + af_ * (RS[:n, t] - vp[:n]))
            lc[:n] = np.where(c, 1.0, -1.0)
        return tot, pr
    fit_mask = np.zeros((N, L), bool)
    fit_mask[ri, ki] = early
    fe = minimize(lambda x: negll_masked(x, False, fit_mask)[0], th, method="L-BFGS-B", options={"maxiter": 400})
    fe1 = minimize(lambda x: negll_masked(x, True, fit_mask)[0], fit1.x, method="L-BFGS-B", options={"maxiter": 400})
    h_s, p_s = negll_masked(fe.x, False, held)
    h_1, p_1 = negll_masked(fe1.x, True, held)
    n_h = held.sum()
    ok("back-test: one rate's predicted November and December share", int(np.floor(100 * p_1 / n_h + 0.5)) ==
       fig["bt_one_rate_pred"], "%.4f" % (p_1 / n_h))
    ok("back-test: the split's held-out gain", abs((h_1 - h_s) - fig["bt_ll_gain"]) < 5, "%.1f" % (h_1 - h_s))
    share = forward(th, False, 300, 991)
    ok("the forecast share reproduces at its printed nearest 5 per cent",
       int(5 * np.floor(share * 100 / 5 + 0.5)) == fig["call_share"], "%.4f against %d" % (share, fig["call_share"]))
    one = forward(fit1.x, True, 150, 992)
    ok("one learning rate reproduces its own figure", int(5 * np.floor(one * 100 / 5 + 0.5)) == fig["share_one_rate"],
       "%.4f against %d" % (one, fig["share_one_rate"]))

    # ------------------------------------------------------------------------------------------------- the asks
    sess["t0"] = pd.to_datetime(sess.started)
    # the widget's day cut: a widget session closed at 00:00:00 UTC and its account's widget session opened at that
    # second under another conversation id are one conversation
    ew = sess[sess.channel == "employer"]
    cut_end = ew[ew.ended.str.endswith("T00:00:00")][["account_ref", "ended", "conversation_id"]].rename(
        columns={"ended": "started", "conversation_id": "parent"})
    cut_start = ew[ew.started.str.endswith("T00:00:00")][["account_ref", "started", "conversation_id"]]
    pairs = cut_start.merge(cut_end, on=["account_ref", "started"])
    parent = {c: p_ for c, p_ in zip(pairs.conversation_id, pairs.parent) if c != p_}
    ok("the widget's day cut: every session closed at 00:00:00 UTC has its reopened twin", len(pairs) == len(cut_end),
       "%d pairs, %d other sessions starting on the second" % (len(pairs), len(cut_start) - len(pairs)))

    def root(c):
        while c in parent:
            c = parent[c]
        return c
    sess["conv"] = [root(c) for c in sess.conversation_id]
    firsts = sess.sort_values(["conv", "t0"]).groupby("conv").first()
    emp_mask = firsts.channel == "employer"
    t_loc = firsts.t0.copy()
    t_loc[emp_mask] = utc_to_winnipeg(firsts.t0[emp_mask])
    staff = set(sess[sess.account_type == "staff"].account_ref)
    inv = pd.read_excel(os.path.join(target, "vendor_invoices_2026.xlsx"), dtype=str)
    vendor_bn = set(inv.supplier_gst_hst.str.slice(0, 9))
    ok("the vendor's business number, from its invoices", len(vendor_bn) == 1, ", ".join(sorted(vendor_bn)))
    is_own = ((firsts.channel == "console") & ~firsts.org_ref.isin(vendor_bn)) | (emp_mask & (firsts.org_ref == bn)) | \
        (firsts.channel.isin(["app", "web"]) & firsts.account_ref.isin(staff))
    is_emp = emp_mask & (firsts.org_ref != bn)
    yr = t_loc.dt.year == 2026
    emp = [int(((t_loc.dt.month == m) & yr & is_emp).sum()) for m in range(1, 13)]
    own = [int(((t_loc.dt.month == m) & yr & is_own).sum()) for m in range(1, 13)]
    months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December")
    ok("employers' conversations by month", emp == [fig["ask_employers"][m] for m in months], "%s" % emp)
    ok("our own staff and test conversations by month", own == [fig["ask_own"][m] for m in months], "%s" % own)

    # --------------------------------------------------------------------------------------- the goldens read back
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(TASK, "golden", "assistant_share_forecast_mar_apr_2027.xlsx"), data_only=True)
    ws = wb["Forecast"]
    ok("the workbook states the forecast", ws["B4"].value == fig["call_share"], "%s" % ws["B4"].value)
    ws4 = wb["Employers and own use"]
    ok("the workbook's monthly counts", [ws4.cell(row=i, column=2).value for i in range(2, 14)] == emp and
       [ws4.cell(row=i, column=3).value for i in range(2, 14)] == own)
    from docx import Document
    note = " ".join(p.text for p in Document(os.path.join(TASK, "golden", "assistant_first_aftermath_note.docx")).paragraphs)
    ok("the note states the forecast", ("%d per cent" % fig["call_share"]) in note)
    wsm = wb["Model comparison"]
    lab = {r[0]: r[1] for r in ws.iter_rows(values_only=True) if r and r[0] is not None}
    sub = open(os.path.join(TASK, "submission.md"), encoding="utf-8").read()
    rates = ("%.2f" % af, "%.2f" % ao)
    FRACTION = {5: "a fifth"}[int(round(af / ao))]
    ok("the learning rates agree with this fit in every file", rates == ("%.2f" % fig["a_free"], "%.2f" % fig["a_forced"])
       and (lab["Learning rate, contacts the jobseeker chose"], lab["Learning rate, overflow transfers"]) ==
       (fig["a_free"], fig["a_forced"])
       and (wsm["D2"].value, wsm["E2"].value) == (fig["a_free"], fig["a_forced"])
       and "%s as far as a conversation" % fig["ratio_words"] in note and "about %s" % FRACTION in sub
       and abs(ao / af - fig["ratio"]) < 0.005, "%s and %s" % rates)
    ok("the one-rate figure agrees in every file",
       lab["One learning rate for every contact would give (nearest 5 per cent)"] == fig["share_one_rate"] and
       wsm["I3"].value == fig["share_one_rate"] and ("%d per cent" % fig["share_one_rate"]) in note and
       ("Not the %d per cent" % fig["share_one_rate"]) in sub)
    ok("the split's gain over one rate agrees in every file", wsm["C3"].value == fig["ll_gain_one_rate"] and
       ("{:,}".format(fig["ll_gain_one_rate"])) in note and ("more than {:,} log-likelihood".format(fig["ll_gain_floor"]))
       in sub and abs((fit1.fun - fit.fun) - fig["ll_gain_one_rate"]) < 0.5 and fit1.fun - fit.fun > fig["ll_gain_floor"])
    for f in ("data_dictionary.xlsx", "telephony_migration_codes.xlsx", "vendor_invoices_2026.xlsx"):
        w = load_workbook(os.path.join(target, f), read_only=True)
        n = sum(1 for s in w.worksheets for _ in s.iter_rows())
        ok("%s reads back" % f, n > 3, "%d rows" % n)
    fails = [x for x in OUT if not x[1]]
    print("%s: %d checks, %d FAIL" % ("PASS" if not fails else "FAIL", len(OUT), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")))
