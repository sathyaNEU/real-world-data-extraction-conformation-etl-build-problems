"""task482's generator assertions, run on the records build.py writes (the same arrays the shipped files carry).

    python3 task482/generator/checks.py

Placement (F rows): every member of the golden family files the golden's set of districts owed, each district at least
MARGIN points of share from its benchmark under the whole family. The ladder (L rows): every wrong route files a
different set. The analyst test (T rows) on the clean truth. Layer 1 (R2 rows): each mess item mishandled the natural
way leaves the call where the golden puts it or on a wrong set, never moves the golden. The semantic forks (SF rows) and
the asks' devices (AD rows), with the separation line (X rows)."""
import collections
import json
import os
import sys

import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import world as W      # noqa: E402
import records as R    # noqa: E402
import irt             # noqa: E402
import pd as PD        # noqa: E402
import billing as BL   # noqa: E402
import golden as G     # noqa: E402

MARGIN = 4.0
OK = []


def check(tag, cond, detail=""):
    print("%-6s %s %s" % (tag, "ok  " if cond else "FAIL", detail))
    OK.append(bool(cond))


def sub(v, mask):
    return {k: (val[mask] if isinstance(val, np.ndarray) and len(val) == len(mask) else val) for k, val in v.items()}


def owed_set(share):
    return frozenset(dd["partner_id"] for dd in W.DISTRICTS if share[dd["j"]] < dd["benchmark"])


def main():
    PD.crm_names()
    P = R.build()
    c = P["c"]
    v = R.tested_view(c)
    V = R.contractor(v)
    D = c["D"]
    B = np.array([dd["benchmark"] for dd in W.DISTRICTS])
    el = v["eligible"]
    ve = sub(v, el)
    m = np.ones(len(ve["g"]), bool)
    gold, wg, _ = G.golden_shares(v)
    gset = owed_set(gold)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    check("G0", sorted(gset) == figs["call"]["owed"], "golden owed set matches figures.json (%d districts)" % len(gset))

    # ---- the golden family (F rows) ----
    fam = {}
    fam["F1 district and grade only"] = irt.share_post(ve["dist"], ve["g"], irt.lr_em(ve["L"], irt.X_of(ve, "dist_grade", m))[0], D)
    fam["F2 district-specific spread"] = irt.share_post(ve["dist"], ve["g"], irt.lr_em(ve["L"], irt.X_of(ve, "gold", m), groups=ve["dist"])[0], D)
    fam["F3 district by grade cells"] = irt.share_post(ve["dist"], ve["g"], irt.lr_em(ve["L"], irt.X_of(ve, "dist_x_grade", m))[0], D)
    for s in (7, 11, 13):
        fam["F4 five plausible values from the golden model, seed %d" % s] = irt.share_pv_scale(
            ve["dist"], ve["g"], irt.to_scale(irt.draw_pv(wg, s)), D)
    allm = np.ones(len(v["g"]), bool)
    wa = irt.lr_em(v["L"], irt.X_of(v, "gold", allm))[0]
    fam["F5 golden model fitted on every assessed student"] = irt.share_post(ve["dist"], ve["g"], wa[el], D)
    Xg = irt.X_of(ve, "gold", m)
    _, gg, s2g = irt.lr_em(ve["L"], Xg)
    p = norm.sf((W.CUT_THETA[ve["g"]] - Xg @ gg) / np.sqrt(s2g))
    fam["F6 the golden model's implied share"] = 100 * np.bincount(ve["dist"], p, minlength=D) / np.bincount(ve["dist"], minlength=D)
    sb, sg = np.zeros(D), np.zeros(D)
    for j in range(D):
        mj = ve["dist"] == j
        cj = sub(ve, mj)
        g3 = irt.onehot(cj["g"], 3)
        X1 = np.column_stack([g3, irt.onehot(cj["band"], 5, drop_first=True),
                              np.column_stack([cj["ed"], cj["el"], cj["iep"]]).astype(float)])
        keep = X1.std(0) > 0
        keep[:3] = True
        z = np.zeros(mj.sum(), int)
        sb[j] = irt.share_post(z, cj["g"], irt.lr_em(cj["L"], X1[:, keep])[0], 1)[0]
        sg[j] = irt.share_post(z, cj["g"], irt.lr_em(cj["L"], g3)[0], 1)[0]
    fam["F7 each district fitted alone, with background"] = sb
    fam["F8 each district fitted alone, grade only"] = sg
    fam["F9 district effects, no grade term"] = irt.share_post(ve["dist"], ve["g"], irt.lr_em(ve["L"], irt.X_of(ve, "dist_only", m))[0], D)
    allf = np.array(list(fam.values()) + [gold])
    lo, hi = allf.min(0), allf.max(0)
    owed = gold < B
    marg = np.where(owed, B - hi, lo - B)
    for k, val in fam.items():
        check("F", owed_set(val) == gset, "%s: max |dev| %.2f, same set" % (k, np.abs(val - gold).max()))
    check("F0", marg.min() >= MARGIN, "every district at least %.1f points from its benchmark across the family (min %.2f at %s)"
          % (MARGIN, marg.min(), W.DISTRICTS[int(marg.argmin())]["partner_id"]))

    # ---- the ladder (L rows): each wrong route files its own wrong set ----
    pvs = V["pv"]
    L = {}
    L["L1 contractor plausible values by district (default)"] = irt.share_pv_scale(ve["dist"], ve["g"], pvs[:, el], D)
    L["L1a the same over every assessed student"] = irt.share_pv_scale(v["dist"], v["g"], pvs, D)
    L["L1b contractor posterior probability"] = irt.share_post(ve["dist"], ve["g"], V["w"][el], D)
    L["L1c each student's mean plausible value counted"] = 100 * np.bincount(
        ve["dist"], (pvs[:, el].mean(0) >= np.array(W.CUT_SCALE)[ve["g"]] - 1e-9).astype(float), minlength=D) / \
        np.bincount(ve["dist"], minlength=D)
    L["L2 contractor-model EAP counted"] = irt.share_point(ve["dist"], ve["g"], (V["w"] @ W.Q)[el], D)
    wu = irt.lr_em(v["L"], irt.X_of(v, "uncond", allm))[0]
    L["L3 unconditional EAP counted"] = irt.share_point(ve["dist"], ve["g"], (wu @ W.Q)[el], D)
    L["L4 maximum likelihood estimate counted"] = irt.share_point(ve["dist"], ve["g"], W.Q[np.argmax(ve["ll"], 1)], D)
    L["L0 number correct through the test characteristic curve"] = irt.share_point(
        ve["dist"], ve["g"], irt.tcc_theta(ve["y"], ve["mods"], ve["admin"]), D)
    L["L5 golden-model EAP counted"] = irt.share_point(ve["dist"], ve["g"], wg @ W.Q, D)
    sets = {}
    for k, val in L.items():
        s = owed_set(val)
        sets[k] = s
        flips = sorted(s ^ gset)
        check("L", s != gset and len(s) != len(gset) or (s != gset and k.startswith("L1b")),
              "%s: %d owed, %d flips from the golden (%s)" % (k, len(s), len(flips), ", ".join(flips)))
    d1 = L["L1 contractor plausible values by district (default)"]
    cross = np.where(owed, d1 - B, B - d1)
    fl = [i for i in range(D) if (d1[i] < B[i]) != owed[i]]
    check("L1x", len(fl) >= 6 and min(cross[i] for i in fl) >= 3.0,
          "the default route flips %d districts, each by at least 3 points (min %.1f)" % (len(fl), min(cross[i] for i in fl)))
    check("L1y", not any(abs(d1[i] - B[i]) < 1.0 for i in range(D)), "no district within a point of its benchmark on the default route")
    robust = {}
    for k, val in L.items():
        cr = [(val[i] - B[i]) if owed[i] else (B[i] - val[i]) for i in range(D) if (val[i] < B[i]) != owed[i]]
        robust[k] = max(cr) if cr else 0.0
    check("L9", all(x >= 1.5 for x in robust.values()),
          "every wrong route crosses at least one benchmark by 1.5 points or more (smallest largest crossing %.1f)"
          % min(robust.values()))
    # ---- the analyst test on the clean truth (T rows) ----
    truth = np.zeros(D)
    for dd in W.DISTRICTS:
        s = W.students(dd["pool"])
        msk = s["eligible"] & s["tested"]
        truth[dd["j"]] = 100 * np.mean(s["theta"][msk] >= W.CUT_THETA[s["g"][msk]])
    check("T1", owed_set(truth) == gset, "the world's true shares file the golden's set (max |golden - truth| %.2f)"
          % np.abs(gold - truth).max())
    check("T2", sets["L1 contractor plausible values by district (default)"] != owed_set(truth),
          "the default route files a wrong set against the world's truth")
    dist_eff = np.array([W.POOL["delta"][dd["pool"]] for dd in W.DISTRICTS])
    check("T3", np.corrcoef(gold - d1, dist_eff)[0, 1] > 0.8,
          "the default route's error tracks the district effect (r = %.2f)" % np.corrcoef(gold - d1, dist_eff)[0, 1])

    # the physics the note states: the reliability of two modules, the district effects, how much of a district's
    # departure from its background prediction the default route keeps
    wv = V["w"]
    mv = wv @ W.Q
    post_var = (wv * (W.Q[None, :] - mv[:, None]) ** 2).sum(1)
    rel = 1 - post_var.mean() / (post_var.mean() + mv.var())
    Xv = irt.X_of(v, "vendor", allm)
    pp = norm.sf((W.CUT_THETA[ve["g"]] - (Xv @ V["gamma"])[el]) / np.sqrt(V["s2"]))
    bgp = 100 * np.bincount(ve["dist"], pp, minlength=D) / np.bincount(ve["dist"], minlength=D)
    slope = np.polyfit(gold - bgp, d1 - bgp, 1)[0]
    rr = np.corrcoef(gold - bgp, d1 - bgp)[0, 1]
    check("T4", 0.6 < rel < 0.75 and 0.35 < slope < 0.6,
          "reliability %.2f; district effects sd %.2f (%.2f to %.2f); the default route keeps %.2f of a district's departure "
          "from its background prediction (r = %.2f); the contractor's residual sd %.2f"
          % (rel, dist_eff.std(), dist_eff.min(), dist_eff.max(), slope, rr, np.sqrt(V["s2"])))

    # ---- Layer 1 mishandled (R2 rows): the golden method on the mishandled population ----
    def golden_on(vv):
        mm = np.ones(len(vv["g"]), bool)
        w_ = irt.lr_em(vv["L"], irt.X_of(vv, "gold", mm))[0]
        return irt.share_post(vv["dist"], vv["g"], w_, D)
    s_all = golden_on(v)
    check("R2a", owed_set(s_all) == gset, "eligibility ignored (every assessed student): same call (max dev %.2f)" % np.abs(s_all - gold).max())
    v_nr = dict(v)
    adm = np.ones_like(v["admin"])
    ll = irt.loglik(v["y"] * v["admin"], v["mods"], adm)        # not-reached items scored incorrect
    v_nr["ll"], v_nr["L"] = ll, irt.norm_lik(ll)
    s_nr = golden_on(sub(v_nr, el))
    check("R2b", owed_set(s_nr) == gset, "items not reached scored incorrect: same call (max dev %.2f)" % np.abs(s_nr - gold).max())
    vb = dict(ve)
    rb = np.random.default_rng(5)
    band = ve["band"].copy()
    co = np.isin(ve["dist"], [dd["j"] for dd in W.DISTRICTS if dd["state"] in ("CO", "OH")])
    band[co & (band == 0) & (rb.random(len(band)) < 0.5)] = 1          # a five-level state's two lowest levels split
    vb["band"] = band
    s_b = golden_on(vb)
    check("R2c", owed_set(s_b) == gset, "Colorado and Ohio levels mapped one band apart: same call (max dev %.2f)" % np.abs(s_b - gold).max())
    vc = dict(ve)
    vc["band"] = np.full(len(ve["band"]), 4)
    vc["ed"] = np.zeros(len(ve["ed"]), np.int8); vc["el"] = vc["ed"]; vc["iep"] = vc["ed"]
    s_c = golden_on(vc)
    check("R2d", owed_set(s_c) == gset, "roster fields not joined (no background): same call (max dev %.2f)" % np.abs(s_c - gold).max())
    # abandoned sessions' answers added to the submitted session's
    ab = collections.defaultdict(list)
    sess_of = {x["session_id"]: x for x in P["sessions"]}
    for sid_, q, it, st, sc in P["responses"]:
        if sess_of[sid_]["status"] == "Abandoned" and sc is not None:
            ab[sess_of[sid_]["test_taker_id"]].append((it, sc))
    item_ix = {val: key for key, val in P["item_id"].items()}
    ll2 = ve["ll"].copy()
    tt_ix = {t: i for i, t in enumerate(ve["tt"])}
    n_add = 0
    for t, lst in ab.items():
        i = tt_ix.get(t)
        if i is None:
            continue
        for it, sc in lst:
            mm_, kk = item_ix[it]
            pq = 1 / (1 + np.exp(-W.A[mm_, kk] * (W.Q - W.B[mm_, kk])))
            ll2[i] += sc * np.log(pq) + (1 - sc) * np.log(1 - pq)
            n_add += 1
    vd = dict(ve)
    vd["ll"], vd["L"] = ll2, irt.norm_lik(ll2)
    s_d = golden_on(vd)
    check("R2e", owed_set(s_d) == gset, "abandoned sessions' %d answers scored with the submitted session: same call (max dev %.2f)"
          % (n_add, np.abs(s_d - gold).max()))
    # the default route under each of the same mishandlings stays wrong
    check("R2f", sets["L1a the same over every assessed student"] != gset, "the default route over every assessed student: still wrong")

    # ---- semantic forks (SF rows) ----
    s_sf1 = gold * np.bincount(ve["dist"], minlength=D) / np.bincount(c["dist"][c["eligible"]], minlength=D)
    check("SF1", owed_set(s_sf1) == gset,
          "SF1 the share over every eligible student, untested ones counted not proficient: same call (max dev %.2f; MSA 9.2 "
          "closes it)" % np.abs(s_sf1 - gold).max())
    sess_status = collections.Counter(x["status"] for x in P["sessions"])
    tested_tt = set(x["test_taker_id"] for x in P["sessions"] if x["status"] == "Submitted")
    check("SF2", len(tested_tt) == len(v["g"]) and sess_status["Submitted"] == len(v["g"]),
          "SF2 one submitted session per assessed student; %d abandoned sessions never scored" % sess_status["Abandoned"])
    one_cut = irt.share_post(ve["dist"], np.zeros(len(ve["g"]), int), wg, D)
    check("SF3", owed_set(one_cut) != gset, "SF3 a single cut at 500 for every grade files another set (closed by MSA 9.2)")
    check("SF4", len(owed_set(gold)) == len(gset), "SF4 at or above against above: a posterior has no mass on a cut (grid cells end on each cut)")
    check("SF5", all(abs(x) < 1e-12 for x in (W.Q[1:] - W.Q[:-1] - 0.05)) and set(W.CUT_THETA) <= set(np.round(W.Q - 0.025, 4)),
          "SF5 the grid's cells end on every cut; scale 500 + 50 theta with D = 1 (technical report)")
    check("SF6", owed_set(s_nr) == gset, "SF6 not reached left out (technical report); scored incorrect, same call (R2b)")
    om = sum(1 for x in P["responses"] if x[3] == "Omitted")
    check("SF7", om > 0 and all(x[4] == 0 for x in P["responses"] if x[3] == "Omitted"), "SF7 %d omitted items scored incorrect" % om)
    elig_by = collections.defaultdict(list)
    for x in P["elig"]:
        elig_by[x["student_id"]].append(x)
    yes = [x for x in P["elig"] if x["eligible"] == "Y"]
    check("SF8", len(set(x["student_id"] for x in yes)) == len(yes) and all(x["rostered_2026_05_01"] == "Y" for x in yes),
          "SF8 one eligible record per student, on the 1 May roster; %d students carry two records" %
          sum(1 for k, x in elig_by.items() if len(x) > 1))
    xw = collections.Counter(x["test_taker_id"] for x in P["xwalk"])
    check("SF9", sum(1 for t, n in xw.items() if n > 1) > 0, "SF9 %d test takers linked to two student IDs (re-rostered), one person each"
          % sum(1 for t, n in xw.items() if n > 1))
    check("SF10", owed_set(fam["F5 golden model fitted on every assessed student"]) == gset, "SF10 fitted on every assessed student: same call (F5)")
    check("SF11", owed_set(fam["F1 district and grade only"]) == gset, "SF11 covariates left out: same call (F1)")
    check("SF12", owed_set(fam["F2 district-specific spread"]) == gset, "SF12 district-specific spread: same call (F2)")
    check("SF13", all(owed_set(val) == gset for k, val in fam.items() if k.startswith("F4")), "SF13 plausible values from the golden model: same call (F4)")
    figs_d = figs["districts"]
    check("SF14", all(abs(figs_d[dd["partner_id"]]["og"] - (round(dd["fee"] * dd["credit_pct"] / 100, 2) if dd["partner_id"] in gset else 0)) < 1e-9
                      for dd in W.DISTRICTS), "SF14 the credit is the Credit Percentage of the 2025-26 Subscription Fee before any credit")
    check("SF15", min(np.abs(gold - B)) > 1.0, "SF15 below the benchmark, strictly: no district within a point of it (min %.2f)" % min(np.abs(gold - B)))

    # ---- the asks (AD rows) and the separation line (X rows) ----
    rows, truth_min = PD.build()
    gold_h = {k: PD.half_hours(m_ / 60.0) for k, m_ in truth_min.items()}
    H = {dd["partner_id"]: dd["pd_hours"] for dd in W.DISTRICTS}
    dec, cat, dedup = collections.Counter(), collections.Counter(), collections.Counter()
    seen = set()
    for x in rows:
        dd = next(d for d in W.DISTRICTS if d["partner_id"] == x["partner_id"])
        if PD.counts(x, dd):
            dec[x["partner_id"]] += float(x["hours"])                    # the hours field read as decimal hours
            cat[x["partner_id"]] += PD.OFFER[x["offering_code"]][4]      # every session at its catalog length
            if x["session_id"] not in seen:                             # one row per session id
                dedup[x["partner_id"]] += x["minutes"] / 60.0
        seen.add(x["session_id"])
    def missed(h):
        return [k for k in gold_h if PD.half_hours(h[k]) != gold_h[k]]
    check("AD1", len(missed(dec)) >= 48, "the hours field read as decimal hours misses %d of 58 districts' hours" % len(missed(dec)))
    check("AD1b", len(missed(cat)) >= 44, "every session at its catalog length misses %d of 58" % len(missed(cat)))
    check("AD1c", len(set(missed(dec)) & set(missed(cat))) >= 40, "both readings miss %d of 58" % len(set(missed(dec)) & set(missed(cat))))
    short_t = [k for k in gold_h if gold_h[k] < H[k]]
    def credits_right(h):
        return [k for k in short_t if max(0.0, H[k] - PD.half_hours(h[k])) == H[k] - gold_h[k]]
    check("AD2", len(credits_right(dec)) <= 3 and len(credits_right(cat)) <= 4,
          "of %d shortfall credits the decimal reading gets %d right and the catalog lengths %d"
          % (len(short_t), len(credits_right(dec)), len(credits_right(cat))))
    check("AD3", len(missed(dedup)) >= 8, "session ids de-duplicated (joint sessions dropped) misses %d districts" % len(missed(dedup)))
    mins = [int(x["hours"].split(".")[1]) for x in rows]
    check("AD6", max(mins) < 60 and sum(1 for m_ in mins if m_) >= 120,
          "%d session rows carry minutes after the point, none past 59; whole-hour sessions read alike either way"
          % sum(1 for m_ in mins if m_))
    inv = BL.build()
    def naive_inv(dd):
        cc = [x for x in inv if x["customer_account"] == dd["account"] and x["status"] == "Open"]
        return min(cc, key=lambda x: (x["due_date"], x["invoice_number"])) if cc else None
    credited = [dd for dd in W.DISTRICTS if figs_d[dd["partner_id"]]["og"] + figs_d[dd["partner_id"]]["pl"] > 0]
    diff = [dd["partner_id"] for dd in credited if naive_inv(dd) is not BL.target_invoice(dd, inv)]
    check("AD4", len(diff) >= 5, "the earliest open invoice on the account, any description, misplaces %d of %d credited districts"
          % (len(diff), len(credited)))
    check("AD5", all((BL.target_invoice(dd, inv) is None) or BL.target_invoice(dd, inv)["balance"] >=
                     figs_d[dd["partner_id"]]["og"] + figs_d[dd["partner_id"]]["pl"] for dd in credited),
          "every applied credit fits its invoice's balance")
    # ---- the asks' forks (SF16 to SF20) ----
    rec = collections.Counter()
    for x in rows:
        dd = next(d for d in W.DISTRICTS if d["partner_id"] == x["partner_id"])
        if x["status"] == "Delivered" and x["delivery"] not in PD.LIVE and dd["term_start"] <= x["session_date"] <= dd["term_end"]:
            rec[x["partner_id"]] += float(x["hours"])
    check("SF16", sum(1 for k in rec if rec[k] > 0) >= 10 and all(abs(figs_d[k]["pd_delivered"] - gold_h[k]) < 1e-9 for k in gold_h),
          "SF16 recorded and on-demand hours in %d districts' terms, none counted (MSA 8.1)" % sum(1 for k in rec if rec[k] > 0))
    by_sess = collections.defaultdict(set)
    for x in rows:
        if x["status"] == "Delivered":
            by_sess[x["session_id"]].add(x["partner_id"])
    joint = [k for k, val in by_sess.items() if len(val) > 1 and not k.startswith("PLS-SSI")]
    check("SF17", len(joint) >= 10, "SF17 %d joint sessions, each counted in full for every district attending (MSA 8.2)" % len(joint))
    check("SF18", all(m_ % 30 != 15 for m_ in truth_min.values()) and all(PD.OFFER[c][4] == int(PD.OFFER[c][4]) for c in PD.OFFER),
          "SF18 every offering scheduled in whole hours; no district's minutes on a quarter hour, so the half hour has no tie")
    cents = [dd["fee"] * dd["credit_pct"] for dd in W.DISTRICTS]
    check("SF14b", all(abs(c_ - round(c_)) < 1e-9 for c_ in cents), "SF14 every outcomes credit a whole number of cents")
    va = [dd for dd in W.DISTRICTS if "va_account" in dd]
    check("SF19", len(va) == 6 and all(BL.target_invoice(dd, inv) is None or BL.target_invoice(dd, inv)["customer_account"] == dd["account"]
                                       for dd in W.DISTRICTS),
          "SF19 every credit applied on the order form's bill-to account; %d districts also bill a virtual academy" % len(va))
    check("SF20", all(m_["credit_date"] == "2026-11-30" for m_ in figs["memos"]), "SF20 every memo dated 2026-11-30 (the prompt)")
    check("X1", all(x["partner_id"] in figs_d for x in rows) and len(set(x["partner_id"] for x in rows)) == 58,
          "the professional learning rows are sessions, never students: the call reads none of them")
    check("X2", set(figs["call"]["owed"]) == gset, "the call is computed from shares and benchmarks only")
    print("\n%d of %d checks passed" % (sum(OK), len(OK)))
    return 0 if all(OK) else 1


if __name__ == "__main__":
    raise SystemExit(main())
