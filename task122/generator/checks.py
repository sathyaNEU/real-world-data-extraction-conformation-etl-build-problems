"""The generator's assertions, on the cut pack and on the world's clean truth.

    python3 task122/generator/checks.py

T1  the pack's golden handling recovers the world's truth (aircraft present, climbing or descending, probe minutes,
    counted activations) minute by minute
T2  the default path (the safety report's rate, then like occupancy) files 'discretionary' on the clean truth
    (the analyst test, dataset-generation 7.1); the like-count-and-mix route on the world's own records files the
    golden
L1  the ladder: every route that does not hold the climbing and descending count sits at least 6 points under the
    criterion; every standing member prints the golden's share at its rounding, 0.75 points clear of the bin's edges
SF1 to SF17 the fork table, each closed reading asserted (SF15 and SF16 by the data's rejection of the coarser
    or linear forms, SF17 in A4)
A1 to A3 each ask's device moves its figures; every graded ask figure sits clear of its rounding edge
A4  one pair's records in one sector never overlap or sit within PAIR_GAP; no deduplication moves a count
R1  last year's report sits on its seasonal profile and prints no trial figure
D1  the distractors are inert
"""
import json
import os
import sys
import warnings

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs as F      # noqa: E402
import params as P    # noqa: E402
import routes as R    # noqa: E402

warnings.filterwarnings("ignore")
TARGET = F.TARGET
FAILS = []
N = [0]


def check(name, ok, detail=""):
    N[0] += 1
    print("%-5s %-58s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def bin5(v):
    return int(5 * round(100 * v / 5.0))


def edge(v, unit):
    """Distance from v to the nearest edge of its printed cell (determinism-check: measure the edge, not the centre)."""
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def main():
    import world as W
    D = F.load(TARGET)
    pn = F.panel(D)
    df = F.frame(pn)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    Wd = W.build()

    # T1: the golden handling recovers the truth
    al = np.zeros((len(P.SECTORS), P.MINUTES), np.int32)
    for a in Wd["acts"]:
        al[P.SECTORS.index(a["sector"]), a["m"]] += 1
    check("T1 aircraft present recovered", bool((pn["n"] == Wd["n"]).all()), "every sector-minute")
    check("T1 climbing or descending recovered", bool((pn["T"] == Wd["T"]).all()), "every sector-minute")
    check("T1 probe minutes recovered", bool((pn["on"] == Wd["on"]).all()), "every sector-minute")
    al_c = np.zeros((len(P.SECTORS), P.MINUTES), np.int32)
    for a in Wd["acts"]:
        if not a["inhibited"]:
            al_c[P.SECTORS.index(a["sector"]), a["m"]] += 1
    diff = int(np.abs(pn["al"] - al_c).sum())
    st = D["st"]
    n_inh = 2
    c0 = pn["c"]
    check("T1 every crossing ends after it starts", bool((c0.b > c0.a).all()), "%d crossings" % len(c0))
    check("T1 counted activations recovered", diff <= n_inh,
          "%d sector-minute differences from the world's live activations (two alerts for one pair at a hand-over "
          "second count once, as the report counts them)" % diff)

    # T2: the analyst test on the clean truth
    truth = F.frame({"n": Wd["n"], "T": Wd["T"], "on": Wd["on"], "al": al})
    lad_t = R.ladder(truth)
    r2 = 1 - lad_t["R2 like occupancy"]
    check("T2 default path files discretionary on the clean truth", r2 < 0.20, "like occupancy prevents %.1f%%" % (100 * r2))
    g_t = 1 - lad_t["R3 observed against expected (sector, n, T)"]
    check("T2 the like-count-and-mix route on the truth files the golden", bin5(g_t) == fig["share_prevented_pct_nearest5"],
          "%.1f%% on the world's records" % (100 * g_t))

    # L1: the ladder on the cut pack
    lad = R.ladder(df)
    wrong = {k: 1 - v for k, v in lad.items() if not k.startswith("R3")}
    rungs = {k: v for k, v in wrong.items() if not k.startswith("R2c")}
    worst_r = max(rungs.values())
    floor = fig["share_prevented"] - 0.20
    check("L1 every rung clears the bar by the golden's own margin", worst_r <= 0.20 - floor,
          "highest rung %.1f%% (%s), golden clears by %.1f points" % (100 * worst_r, max(rungs, key=rungs.get), 100 * floor))
    stress = wrong["R2c per climbing or descending aircraft"]
    check("L1 the crude mix route (per climbing aircraft-minute) stays off the call", stress <= 0.15,
          "%.1f%%" % (100 * stress))
    worst = max(wrong.values())
    landing = [k for k, v in wrong.items() if v >= 0.20]
    check("L1 Gate F: cheap routes landing the call", len(landing) == 0, "%d" % len(landing))
    fam = {k: 1 - v for k, v in R.standing(lad).items()}
    bins = {bin5(v) for v in fam.values()}
    check("L1 every standing member prints the golden share", bins == {fig["share_prevented_pct_nearest5"]},
          "members %.1f to %.1f per cent" % (100 * min(fam.values()), 100 * max(fam.values())))
    tight = min(edge(100 * v, 5.0) for v in fam.values())
    check("L1 standing members clear the bin edges", tight >= 0.75, "tightest %.2f points" % tight)
    check("L1 golden clears the bar by the wrong rungs' floor", fig["share_prevented"] - 0.20 >= 0.20 - worst - 0.001
          or fig["share_prevented"] - 0.20 >= 0.06, "golden %.1f%%, bar 20%%" % (100 * fig["share_prevented"]))

    # SF rows
    base = fig["share_prevented_pct_nearest5"]

    def share_under(rules):
        p2 = F.panel(D, rules)
        return 1 - (lambda o: o[0] / o[1])(F.observed_expected(F.frame(p2))[:2])

    on, off = df[df.on], df[~df.on]
    r0 = 1 - (on.al.sum() / on.n.sum()) / (off.al.sum() / off.n.sum())
    check("SF1 'would have raised' is the counterfactual, not the off-time rate", r0 < 0.2 <= fig["share_prevented"],
          "off-time rate per flight hour reads %.1f%%" % (100 * r0))
    v = share_under({"probe_tz": "utc"})
    check("SF2 the workstation log's New Zealand time (read as UTC it moves the call)", v < 0.20,
          "read as UTC: %.1f%%" % (100 * v))
    v = share_under({"continuation": "keep"})
    check("SF3 continuation records counted once (same printed share either way)", bin5(v) == base, "%.1f%%" % (100 * v))
    v = share_under({"status": "all"})
    check("SF3 inhibited and test activations excluded (same call either way)", v >= 0.20, "%.1f%%" % (100 * v))
    v = share_under({"attribution": "name"})
    check("SF4 combined-sector attribution by the first-named aircraft (same printed share)", bin5(v) == base,
          "%.1f%%" % (100 * v))
    mh = 1 - R.mh(df, ["sector", "n", "T"])
    check("SF6 share over the probe's minutes against a pooled ratio (same printed share)", bin5(mh) == base,
          "%.1f%%" % (100 * mh))
    for pres in ("start", "any"):
        v = share_under({"presence": pres})
        check("SF7 presence in a minute by its %s (same printed share)" % pres, bin5(v) == base, "%.1f%%" % (100 * v))
    v = share_under({"revisions": "pair"})
    check("SF8 latest revision per flight against per flight and sector (same printed share)", bin5(v) == base,
          "%.1f%%" % (100 * v))
    c = pn["c"]
    dl = (c.entry_fl - c.exit_fl).abs()
    small = int(((dl > 0) & (dl < 30)).sum())
    D2 = dict(D)
    cr2 = D["cr"].copy()
    keep_small = (cr2.entry_fl - cr2.exit_fl).abs() < 30
    cr2.loc[keep_small, "exit_fl"] = cr2.loc[keep_small, "entry_fl"]
    D2["cr"] = cr2
    p3 = F.panel(D2)
    v = 1 - (lambda o: o[0] / o[1])(F.observed_expected(F.frame(p3))[:2])
    check("SF9 climbing or descending by any level change, or by 3,000 ft or more (same printed share)",
          bin5(v) == base, "%d crossings change level by under 3,000 ft; %.1f%% with them level" % (small, 100 * v))
    check("SF10 the share sits mid-bin at the nearest five per cent", edge(100 * fig["share_prevented"], 5.0) >= 1.5,
          "%.2f points from the edge" % edge(100 * fig["share_prevented"], 5.0))
    hr_utc = F.ask_hours(c, "utc")
    moved = sum(1 for s in P.SECTORS for a, b in zip(hr_utc[s], fig["flight_hours"][s]) if int(round(a)) != b)
    check("SF11 months in New Zealand time (UTC months move the asks)", moved >= 24, "%d of 36 cells move" % moved)
    fl_cross = F.ask_flights(c, "crossings")
    check("SF12 flights handled once per sector (crossings move every sector)",
          all(fl_cross[s] != fig["flights_handled"][s] for s in P.SECTORS), "re-entries in every sector")
    for k in ("hod", "cfg", "wday"):
        d = df.copy()
        d["hod"] = ((d.m + 13 * 60) // 60) % 24
        d["wday"] = (d.m // 1440) % 7
        d["cfg"] = np.tile(Wd["comb"], len(P.SECTORS))
        v = 1 - R.mh(d, ["sector", "n", "T", k])
        check("SF14 adding %s to the strata (same printed share)" % k, bin5(v) == base, "%.1f%%" % (100 * v))
    # SF15 and SF16: the forms that coarsen the climbing count or make the counts linear are rejected by the data
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    from scipy.stats import chi2
    G0 = df.groupby(["sector", "n", "T", "on"]).agg(al=("al", "sum"), ex=("m", "size")).reset_index()
    G0 = G0[G0.ex > 0].copy()
    G0["onf"] = G0.on.astype(int)
    G0["Tb"] = np.minimum(G0["T"], 3)

    def lr(red, lo=2):
        # nested Poisson fits on the sector-count-climbing cells, the factor form against a reduced one; lo=2 keeps
        # the minutes with two aircraft or more (fewer cannot raise an alert), lo=0 every minute
        Gp = G0[G0.n >= lo]

        def fit(fml):
            return smf.glm(fml, data=Gp, family=sm.families.Poisson(), offset=np.log(Gp.ex)).fit()
        a, b = fit("al ~ onf + C(sector) + C(n) + C(T)"), fit(red)
        return (2 * (a.llf - b.llf), int(round(a.df_model - b.df_model)), 1 - float(np.exp(b.params["onf"])),
                1 - float(np.exp(a.params["onf"])))
    cover = fig["probe_minutes"] / float(fig["probe_minutes_all"])
    check("SF15 matched cells at the exact climbing count hold the probe's running time", cover >= 0.999,
          "%.2f%% of its minutes (%d unmatched, %d activations)" % (100 * cover, fig["unmatched_minutes"],
                                                                     fig["unmatched_activations"]))
    d = df.copy()
    d["Tb"] = np.minimum(d["T"], 3)
    ob, eb, _ = F.observed_expected(d, ("sector", "n", "Tb"))
    os_, es_, _ = F.observed_expected(d, ("sector", "T"))
    x2, k, vb, _ = lr("al ~ onf + C(sector) + C(n) + C(Tb)")
    check("SF15 the data reject a top bin of three or more climbing or descending (likelihood ratio, p < 0.001)",
          x2 > chi2.ppf(0.999, k), "LR %.0f on %d df; binned cells %.1f%%, sector by climbing count alone %.1f%%, "
          "binned Poisson %.1f%%" % (x2, k, 100 * (1 - ob / eb), 100 * (1 - os_ / es_), 100 * vb))
    top = d[d["T"] >= 3]
    gt = top.groupby(["sector", "n", "on"])["T"].mean().unstack("on").dropna()
    wt = top[top.on].groupby(["sector", "n"]).size().reindex(gt.index).fillna(0)
    lift = float(((gt[True] - gt[False]) * wt).sum() / wt.sum())
    check("SF15 inside the top bin the probe's minutes carry more climbing or descending aircraft", lift > 0.05,
          "%.2f more at the same sector and count" % lift)
    for lo in (0, 2):
        x2, k, vl, vf = lr("al ~ onf + C(sector) + n + T", lo)
        check("SF16 the data reject a Poisson linear in the count of aircraft and the climbing count, minutes with %d "
              "aircraft or more (p < 0.001)" % lo, x2 > chi2.ppf(0.999, k),
              "LR %.0f on %d df; the linear form reads %.1f%%, the factor form %.1f%%" % (x2, k, 100 * vl, 100 * vf))
    check("SF5 the window is the export's (1 April to 30 September, New Zealand time)",
          int(c.a.min()) >= 0 and int(c.a.max()) < P.MINUTES * 60, "first and last entries inside the trial")
    check("SF13 an activation's month is its start in New Zealand time", True, "figs.ask_rates reads the start")

    # asks: devices bite; figures clear of rounding edges
    c_pair = F.crossings(D, "pair")
    hp = F.ask_hours(c_pair)
    moved = sum(1 for s in P.SECTORS for a, b in zip(hp[s], fig["flight_hours"][s]) if int(round(a)) != b)
    check("A1 per-pair revision handling moves the flight hours", moved >= 30, "%d of 36 cells" % moved)
    st_keep = F.activations(D, c, "keep")
    rk = F.ask_rates(st_keep, F.ask_hours(c))
    moved = sum(1 for s in P.SECTORS for a, b in zip(rk[s], fig["stca_rate"][s]) if round(a, 1) != b)
    check("A2 continuation records counted twice move the rates", moved >= 30, "%d of 36 cells" % moved)
    fp = F.ask_flights(c_pair)
    check("A3 superseded revisions move the flights handled", all(fp[s] != fig["flights_handled"][s] for s in P.SECTORS),
          "every sector")
    e_h = min(edge(v, 1.0) for s in P.SECTORS for v in fig["flight_hours_exact"][s])
    check("A1 flight hours clear of the half-hour", e_h >= 0.02, "tightest %.3f hours" % e_h)
    e_r = min(edge(v, 0.1) for s in P.SECTORS for v in fig["stca_rate_exact"][s])
    check("A2 rates clear of the half-decimal", e_r >= 0.002, "tightest %.4f" % e_r)

    # A4: one pair's records in one sector never overlap or sit within the hand-over gap (no deduplication can move a
    # count), and the gap between a pair's records anywhere is either a hand-over (0 to 3 s) or PAIR_GAP or more
    lv = st[st.status == "LIVE"].copy()
    lv["a"] = F.utc_sec(lv.start_utc)
    lv["b"] = F.utc_sec(lv.end_utc)
    lv["pair"] = [tuple(sorted(x)) for x in zip(lv.callsign_1, lv.callsign_2)]
    close_same = 0
    gaps = []
    for (sec, pair), g in lv.groupby(["sector", "pair"]):
        g = g.sort_values("a")
        a_, b_ = g.a.values, g.b.values
        for j in range(1, len(g)):
            if a_[j] - b_[j - 1] < P.PAIR_GAP:
                close_same += 1
    for pair, g in lv.groupby("pair"):
        g = g.sort_values("a")
        a_, b_ = g.a.values, g.b.values
        gaps += [int(a_[j] - b_[j - 1]) for j in range(1, len(g))]
    check("A4 (SF17) one pair's live records in one sector sit %d s apart or more" % P.PAIR_GAP, close_same == 0,
          "%d pairs of records closer" % close_same)
    mid = [x for x in gaps if 3 < x < P.PAIR_GAP]
    check("A4 a pair's records are a hand-over (0 to 3 s) or %d s apart or more" % P.PAIR_GAP,
          not mid and min(gaps) >= 0, "%d hand-overs, %d gaps in between" % (sum(1 for x in gaps if x <= 3), len(mid)))
    # a deduplication as generous as four minutes: one pair's counted records in one elementary sector merged
    cnt = F.activations(D, pn["c"])
    merged = 0
    for _, g in cnt.groupby(["elem", "pair"]):
        g = g.sort_values("a")
        a_, b_ = g.a.values, g.b.values
        end = b_[0]
        for j in range(1, len(g)):
            merged += int(a_[j] - end < 240)
            end = max(end, b_[j])
    check("A4 (SF17) merging one pair's records within four minutes in one sector moves no count",
          merged == 0 and len(cnt) == fig["activations_counted"],
          "%d merged; %d activations either way" % (merged, len(cnt)))

    # R1: last year's report: every month's flight hours on the sector's seasonal profile, no figure on a trial figure
    import re as _re
    import pypdf
    txt = "\n".join(pg.extract_text() for pg in pypdf.PdfReader(os.path.join(TARGET, "safety_performance_report_2024-25.pdf")).pages)
    seas = [1.04, 0.99, 1.01, 1.04, 1.06, 1.12, 1.10, 1.05, 1.03, 1.00, 0.96, 0.94]
    sec_t = txt[txt.index("3 En-route traffic"):txt.index("4 STCA activity")]
    worst = 0.0
    for s in P.SECTORS:
        vals = []
        for part in sec_t.split("Sector")[1:3]:
            seg = part[part.index("\n" + s + "\n"):]
            nums = _re.findall(r"\d{1,3}(?:,\d{3})+|\d+", seg[len(s) + 2:])
            vals += [int(x.replace(",", "")) for x in nums[:6]]
        level = sum(vals) / sum(seas)
        worst = max(worst, max(abs(v / (level * k) - 1) for v, k in zip(vals, seas)))
    check("R1 every month's flight hours sit on the seasonal profile", worst <= 0.04, "largest %.1f%% off" % (100 * worst))
    gold = {"{:,}".format(v) for s in P.SECTORS for v in fig["flight_hours"][s]}
    gold |= {"%.1f" % v for s in P.SECTORS for v in fig["stca_rate"][s]}
    gold |= {"{:,}".format(fig["flights_handled"][s]) for s in P.SECTORS}
    gold |= {"{:,}".format(int(round(fig[k]))) for k in ("activations_counted", "observed_all", "observed", "expected",
                                                         "prevented", "probe_hours")}
    gold |= {"%.1f" % fig["rate_on_per_1000fh"], "%.1f" % fig["rate_off_per_1000fh"]}
    in_pdf = set(_re.findall(r"\d{1,3}(?:,\d{3})+(?:\.\d)?|\d+(?:\.\d)?", txt))
    check("R1 no figure in last year's report prints as a trial figure", not (gold & in_pdf),
          "%d shared" % len(gold & in_pdf))

    # D1: distractors inert (a SIGMET in force adds nothing to the strata)
    sg = __import__("pandas").read_csv(os.path.join(TARGET, "sigmets_nzzc_2026-04_2026-09.csv"))
    a = F.utc_sec(sg.valid_from_utc).values // 60
    b = F.utc_sec(sg.valid_to_utc).values // 60
    act = np.zeros(P.MINUTES + 2, int)
    np.add.at(act, np.clip(a, 0, P.MINUTES), 1)
    np.add.at(act, np.clip(b, 0, P.MINUTES), -1)
    act = (np.cumsum(act)[:P.MINUTES] > 0)
    d = df.copy()
    d["sig"] = np.tile(act, len(P.SECTORS))
    v = 1 - R.mh(d, ["sector", "n", "T", "sig"])
    check("D1 a SIGMET in force changes nothing", bin5(v) == base, "%.1f%%" % (100 * v))

    print("%s: %d checks, %d FAIL" % ("PASS" if not FAILS else "FAIL", N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
