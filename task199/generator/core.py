"""task199 clean truth: the world's parameters and every quantity measured on them.

This is the single source of truth for the design note's numbers. It carries no file writing: the
pack builder (stage 3) imports `WORLD`, `panel_truth` and `ask_truth` from here, and `ceiling.py`
imports the ask stops. Run it directly to print every measurement the design note quotes:

    python3 task199/generator/core.py

Sections, in the order the design note uses them:
  1 the world (eleven panel cities, twelve municipalities outside the panel, the outlet panel)
  2 panel truth: activity, presence, capture, citations, and the recorded counts they imply
  3 the routes a solver can take, and the ladder's four rungs
  4 the four pricing screens, the exposure-elasticity corridor and the seed sweep
  5 the ask layer's stops and forcing figures
"""
import math
import random

# ----------------------------------------------------------------- 1 the world

# Eleven panel cities. One row per city:
#   pop        2026 projected residents
#   lam0       actions actually occurring per month in the baseline
#   pres0      items the clipping service delivers per month from the city, all topics
#   p0         baseline probability that an action that happened enters the register
#   r0         citations the register holds per recorded action in the baseline
#   lam_m      multiplier on activity in the designation window
#   pres_m     multiplier on delivered items in the window (capture moves with it)
#   r_m        multiplier on citations per action in the window
PANEL = [
    #  city              pop    lam0  pres0   p0    r0   lam_m pres_m  r_m
    ("Valledupar",     512300, 58.0, 3600, 0.78, 2.90, 1.00, 1.00, 1.00),
    ("Barrancabermeja", 198400, 26.0, 2050, 0.72, 2.60, 1.00, 1.00, 1.00),
    ("Aguachica",       112700, 20.0, 1050, 0.64, 2.20, 1.03, 1.00, 1.00),
    ("Ocana",            98600, 21.0,  820, 0.60, 2.00, 0.97, 1.00, 1.00),
    ("Tibu",            149800, 26.0,  509, 0.33, 1.50, 1.98, 1.00, 1.00),   # golden
    ("Sardinata",       146200, 24.0,  497, 0.32, 1.45, 1.00, 2.65, 1.40),   # rung 1
    ("El Tarra",        178500, 27.0,  607, 0.34, 1.55, 1.00, 2.42, 1.35),
    ("Convencion",      120400, 20.0,  409, 0.33, 1.50, 1.00, 2.52, 1.37),
    ("Teorama",         162900, 30.0,  554, 0.35, 1.60, 1.05, 1.00, 0.36),   # rung 2
    ("San Calixto",     104100, 23.0,  352, 0.37, 1.70, 1.07, 1.05, 1.00),
    ("Hacari",           86900, 21.0,  291, 0.35, 1.60, 0.95, 0.97, 1.00),
]
GOLDEN = "Tibu"
# the pool the ranking is decided in: every city whose baseline capture is under a half
POOL = ["Tibu", "Sardinata", "El Tarra", "Convencion", "Teorama", "San Calixto", "Hacari"]
BASE_MONTHS = 24       # 2024-01-01 .. 2025-12-31
WIN_MONTHS = 6         # 2026-04-01 .. 2026-09-30
CAP = 0.95             # no city's capture exceeds this

# Twelve municipalities the register covers and the designation protocol does not: every ask
# device row sits here, or in a column the call never reads, or in 2023.
OUTSIDE = [
    ("Abrego", 41200), ("Rio de Oro", 15600), ("La Playa", 8700), ("Cachira", 10900),
    ("Gonzalez", 7300), ("La Esperanza", 12800), ("Bucarasica", 5100), ("El Carmen", 14600),
    ("San Martin", 19800), ("Curumani", 36400), ("Chimichagua", 32100), ("Pelaya", 18300),
]

WORLD = {"panel": PANEL, "outside": OUTSIDE, "base_months": BASE_MONTHS,
         "win_months": WIN_MONTHS, "golden": GOLDEN}


# ------------------------------------------------- 2 panel truth, no sampling noise

def panel_truth():
    out = {}
    for (nm, pop, lam0, pres0, p0, r0, lm, pm, rm) in PANEL:
        p1 = min(CAP, p0 * pm)
        out[nm] = dict(
            pop=pop, lam_b=lam0, lam_w=lam0 * lm, p_b=p0, p_w=p1,
            v_b=pres0, v_w=pres0 * pm, r_b=r0, r_w=r0 * rm,
            n_b=lam0 * p0, n_w=lam0 * lm * p1,          # recorded actions per month
        )
    return out


def recorded(d, span):
    """Recorded actions over a whole span."""
    return d["n_b"] * BASE_MONTHS if span == "base" else d["n_w"] * WIN_MONTHS


def rate_per_100k(d):
    """The graded figure: recorded actions in the window per 100,000 residents."""
    return recorded(d, "win") / d["pop"] * 1e5


# ------------------------------------------------------- 3 the routes and the ladder

def routes(t, q_red=0.30, alpha=1.0):
    """Every route a solver can take. Score is the window's monthly level over the baseline's."""
    R = {}
    for nm, d in t.items():
        n_b, n_w = d["n_b"], d["n_w"]
        cit_b, cit_w = n_b * d["r_b"], n_w * d["r_w"]
        k_b, k_w = cit_b * 1.18, cit_w * 1.18            # items retained for screening
        s_b = 9.0 * (1 - (1 - 0.055 * d["r_b"]) ** max(n_b, .1))   # distinct citing outlets
        s_w = 9.0 * (1 - (1 - 0.055 * d["r_w"]) ** max(n_w, .1))
        put = lambda k, v: R.setdefault(k, {}).__setitem__(nm, v)
        # A: no conditioning at all
        put("A rows_as_exported", (n_w * 1.0) / n_b)     # replaced below by the rung-0 route
        put("A rate_per_100k", n_w / n_b)
        put("A window_level", n_w / d["pop"] * 1e5)
        put("A absolute_increase", (n_w - n_b) * WIN_MONTHS)
        # B: conditioned on a volume the actions themselves produce
        put("B per_retained_item", (n_w / k_w) / (n_b / k_b))
        put("B per_citation", (n_w / cit_w) / (n_b / cit_b))
        put("B per_citing_outlet", (n_w / s_w) / (n_b / s_b))
        # C: capture estimated from citation redundancy, with a free parameter
        put("C redundancy_capture",
            (n_w / (1 - (1 - q_red) ** d["r_w"])) / (n_b / (1 - (1 - q_red) ** d["r_b"])))
        # D: conditioned on the material the monitor received, every form
        put("D per_received_item", (n_w / d["v_w"]) / (n_b / d["v_b"]))
        put("D per_received_alpha", (n_w / d["v_w"] ** alpha) / (n_b / d["v_b"] ** alpha))
        put("D per_received_sqrt", (n_w / math.sqrt(d["v_w"])) / (n_b / math.sqrt(d["v_b"])))
        put("D presence_saturating",
            (n_w / (1 - math.exp(-d["v_w"] / 700.))) / (n_b / (1 - math.exp(-d["v_b"] / 700.))))
        put("Z truth_activity", d["lam_w"] / d["lam_b"])
    # D fitted: log n = a_city + beta log v, beta from the within-city movement, pooled
    num = den = 0.0
    for nm, d in t.items():
        dv, dn = math.log(d["v_w"] / d["v_b"]), math.log(d["n_w"] / d["n_b"])
        num += dv * dn
        den += dv * dv
    beta = num / den if den else 1.0
    for nm, d in t.items():
        R.setdefault("D fitted_beta", {})[nm] = math.exp(
            math.log(d["n_w"] / d["n_b"]) - beta * math.log(d["v_w"] / d["v_b"]))
    R["_beta"] = beta
    return R


def alpha_corridor(t, lo=0.0, hi=1.6, step=0.001):
    """Every exposure elasticity for which the golden still leads: closure move C3."""
    good = []
    a = lo
    while a <= hi + 1e-9:
        r = routes(t, alpha=a)["D per_received_alpha"]
        if max(r, key=r.get) == GOLDEN:
            good.append(round(a, 3))
        a += step
    return (min(good), max(good)) if good else (None, None)


def top(d, k=4):
    return sorted(((n, v) for n, v in d.items() if not n.startswith("_")),
                  key=lambda kv: -kv[1])[:k]


# ------------------------------------------------------------------ 4 the screens

def se_log_rise(d):
    """Standard error of the log rise, from the two Poisson counts that make it."""
    return math.sqrt(1.0 / recorded(d, "win") + 1.0 / recorded(d, "base"))


def pois(rng, lam):
    if lam <= 0:
        return 0
    if lam > 30:
        return max(0, int(round(rng.gauss(lam, math.sqrt(lam)))))
    el, k, p = math.exp(-lam), 0, 1.0
    while True:
        p *= rng.random()
        if p <= el:
            return k
        k += 1


def seed_sweep(t, seeds=60, base=7000):
    """Is the ranking a designed mechanism or a tuned seed?"""
    hit_dec = miss_raw = 0
    pos_raw, pos_dec = [], []
    for s in range(seeds):
        rng = random.Random(base + s)
        sim = {}
        for nm, d in t.items():
            nb = sum(pois(rng, d["n_b"]) for _ in range(BASE_MONTHS))
            nw = sum(pois(rng, d["n_w"]) for _ in range(WIN_MONTHS))
            vb = sum(pois(rng, d["v_b"]) for _ in range(BASE_MONTHS))
            vw = sum(pois(rng, d["v_w"]) for _ in range(WIN_MONTHS))
            sim[nm] = ((nw / WIN_MONTHS) / max(nb / BASE_MONTHS, 1e-9),
                       (nw / vw) / max(nb / vb, 1e-9))
        o_r = sorted(sim, key=lambda n: -sim[n][0])
        o_d = sorted(sim, key=lambda n: -sim[n][1])
        hit_dec += o_d[0] == GOLDEN
        miss_raw += o_r[0] != GOLDEN
        pos_raw.append(o_r.index(GOLDEN) + 1)
        pos_dec.append(o_d.index(GOLDEN) + 1)
    return dict(seeds=seeds, decisive_hits=hit_dec, default_misses=miss_raw,
                pos_raw=(min(pos_raw), max(pos_raw), sum(pos_raw) / seeds),
                pos_dec=(min(pos_dec), max(pos_dec), sum(pos_dec) / seeds))


def corr(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((x - mb) ** 2 for x in b))
    return 0.0 if sa == 0 or sb == 0 else sum((a[i] - ma) * (b[i] - mb) for i in range(n)) / (sa * sb)


# ------------------------------------------- 4b screen 6: what a subset hands over
#
# When a quantity is recoverable exactly from a subset of records, ask what else that subset hands
# over. Three subsets matter here, and the answer to the first one set the generator's step dates.
STEP = "2026-04-01"     # every presence shift and the activity rise take effect on this date


def screen6(t):
    out = {}
    # S1 a short pre-window baseline instead of the filed twenty-four months. The leak exists only
    # where presence has already moved and activity has not, so the generator steps both on the same
    # date and every pre-window and sub-window month carries the baseline's levels.
    for label, pres_moved, lam_moved in (("presence steps first, activity later", True, False),
                                         ("both step together on " + STEP, False, False),
                                         ("activity steps first, presence later", False, True)):
        short = {}
        for nm, d in t.items():
            n_pre = d["lam_b"] * (d["lam_w"] / d["lam_b"] if lam_moved else 1.0) * \
                    (d["p_w"] if pres_moved else d["p_b"])
            short[nm] = d["n_w"] / n_pre
        o = sorted(short, key=lambda n: -short[n])
        out[label] = (o[0], short[o[0]], o.index(GOLDEN) + 1)
    # S2 do the two denominators ever meet? retained items are citations plus near misses.
    out["max_retained_over_delivered"] = max(
        (n * r * 1.18) / v
        for d in t.values()
        for n, v, r in ((d["n_b"], d["v_b"], d["r_b"]), (d["n_w"], d["v_w"], d["r_w"])))
    # S3 is any panel city-month empty of delivered items, so presence reads off absence?
    out["thinnest_delivered_month"] = min(d["v_b"] for d in t.values())
    return out


# ------------------------------------------------------------------- 5 the asks
#
# Every ask device sits outside the call's declared population: on a municipality the
# designation protocol does not cover, in 2023, or in a column the call never reads.
# Each entry carries the stops a response can land on, the golden last, and the figure that
# makes the wrong reading wrong (the inconsistency a careful analyst can find).

ASKS = {
    "A": {
        "name": "intake reconciled to the service's invoices, 2025, by quarter and outlet type",
        "figures": 25,          # 4 quarters x 4 outlet types + 4 billed amounts + 5 reconciling groups
        "home": "audit trail: an input the call consumes, through rows the call never reads, to another system's control total",
        "population": "every delivery row for 2025, all 23 municipalities; the device rows are the Rio de Oro desk's",
        "primary": "D1 duplication under fresh item ids: the service re-sent the Rio de Oro desk's August batch after a transmission failure and the log holds both copies, while the invoice bills the batch once",
        "inconsistency": "the log's August item count for that desk exceeds the invoice line by exactly the re-sent batch, and the re-sent rows repeat the publication dates of rows already held",
        "hazards": ["H1 outlet codes gain a service prefix in 2026",
                    "H2 the invoice states amounts in thousands of pesos and items in units"],
        "stops": {
            "log as exported": 41860,
            "invoice total read as the log's": 40980,
            "re-sent batch dropped by publication date, which also drops genuine same-day items": 41402,
            "golden: re-sent batch identified by its transmission id and removed": 41508,
        },
    },
    "B": {
        "name": "what the register holds for the twelve municipalities outside the panel, 2025",
        "figures": 27,          # 12 municipalities x 2 figures + 3 totals
        "home": "component: the coverage the stakeholder wants anyway before committing a mission, on rows the designation never reads",
        "population": "the twelve municipalities outside the designation panel, 2025",
        "primary": "D7 keys: three of the twelve were re-coded when two municipalities were merged in the national code list, so their 2025 actions sit under a code the register's own city table maps to the merged entity, and a raw join on the current code drops them",
        "inconsistency": "actions whose citations point at delivered items from a municipality the raw join shows as holding none",
        "hazards": ["H2 the invoice's thousands", "H3 the 2024 export's day-first dates"],
        "stops": {
            "raw join on the current code": 1184,
            "raw join plus an unmatched-row drop": 1131,
            "merged entity credited with both municipalities' actions": 1352,
            "golden: each action credited to the municipality its own code names on its action date": 1268,
        },
    },
    "C": {
        "name": "participants estimated per action by actor sector, 2025, whole corridor",
        "figures": 20,          # 6 sectors x 3 figures + 2 totals
        "home": "component: the scale of the actions behind the register's counts, a measure every city carries that the designation does not turn on",
        "population": "every 2025 action's participants column, which the call never reads",
        "primary": "D3 units and meaning: radio-transcript coding records a range in the note field and writes its lower bound in the numeric column, and the 2024 template wrote a zero where participants were not reported while the 2026 template leaves it blank",
        "inconsistency": "sectors whose mean participants per action fall when the register's own note field reports a wider crowd, and a zero in a column the manual says is never zero",
        "hazards": ["H3 the 2024 export's day-first dates", "H4 the sector code list gained two codes in 2025"],
        "stops": {
            "numeric column as exported, zeros counted": 318.4,
            "zeros dropped, ranges still read as their lower bound": 372.1,
            "ranges read as their upper bound": 436.7,
            "golden: ranges read at their midpoint and unreported participants excluded": 401.6,
        },
    },
}


def ask_truth():
    return ASKS


# ------------------------------------------------------------------------ report

def main():
    t = panel_truth()
    R = routes(t)
    beta = R.pop("_beta")
    easy, dec = R["A rate_per_100k"], R["D per_received_item"]
    o_raw = sorted(easy, key=lambda n: -easy[n])
    o_dec = sorted(dec, key=lambda n: -dec[n])

    print("=" * 98)
    print("1  PANEL TRUTH")
    print("=" * 98)
    print("  %-17s %8s %8s %8s %8s %8s %8s %8s" %
          ("city", "base n", "win n", "rate/100k", "pres b", "pres w", "cap b", "cap w"))
    for nm, _, _, _, _, _, _, _, _ in PANEL:
        d = t[nm]
        print("  %-17s %8.0f %8.0f %9.1f %8.0f %8.0f %8.2f %8.2f"
              % (nm, recorded(d, "base"), recorded(d, "win"), rate_per_100k(d),
                 d["v_b"] * BASE_MONTHS, d["v_w"] * WIN_MONTHS, d["p_b"], d["p_w"]))

    print("\n" + "=" * 98)
    print("2  ROUTES: top four each")
    print("=" * 98)
    for k in sorted(R):
        print("  %-24s %s" % (k, "  ".join("%-16s %.3f" % (n, v) for n, v in top(R[k]))))
    print("  fitted exposure elasticity beta = %.3f" % beta)
    print("  golden position: default path %d of 11, decisive route %d"
          % (o_raw.index(GOLDEN) + 1, o_dec.index(GOLDEN) + 1))

    print("\n" + "=" * 98)
    print("3  THE FOUR SCREENS")
    print("=" * 98)
    needed = easy[o_raw[0]] - easy[GOLDEN]
    lead = t[o_raw[0]]
    avail = easy[o_raw[0]] - lead["lam_w"] / lead["lam_b"]
    print("  screen 1 residue: a method (which measured volume stands in the denominator), not a knob")
    print("  screen 2 move needed %.3f, available %.3f, ratio %.2fx" % (needed, avail, avail / needed))
    print("  screen 3 decisive margin %.3f = %.1f SE of the golden's own rise; margin ratio %.2fx; "
          "default-path margin %.2fx"
          % (dec[GOLDEN] - dec[o_dec[1]],
             (dec[GOLDEN] - dec[o_dec[1]]) / (math.exp(se_log_rise(t[GOLDEN])) - 1),
             dec[GOLDEN] / dec[o_dec[1]], easy[o_raw[0]] / easy[GOLDEN]))
    worst = max(PANEL, key=lambda m: se_log_rise(t[m[0]]))
    print("           thinnest city %s at SE %.3f; golden SE %.3f"
          % (worst[0], se_log_rise(t[worst[0]]), se_log_rise(t[GOLDEN])))
    d = t[o_raw[0]]
    lever_noise = math.sqrt(1 / (d["v_w"] * WIN_MONTHS) + 1 / (d["v_b"] * BASE_MONTHS))
    print("  screen 4 lever %.3fx in the denominator (a level); its own noise %.4f against the ranked "
          "quantity's %.4f, a ratio of %.0f to 1: two variances"
          % (d["v_w"] / d["v_b"], lever_noise, se_log_rise(d),
             abs(d["v_w"] / d["v_b"] - 1) / lever_noise))
    # the refinement's own number: the distance to the decision boundary, in units of the lever's
    # own noise, rather than a preference for a decision shape
    g = t[GOLDEN]
    margin = dec[GOLDEN] - dec[o_dec[1]]
    lever_noise_units = dec[GOLDEN] * math.sqrt(
        1 / (g["v_w"] * WIN_MONTHS) + 1 / (g["v_b"] * BASE_MONTHS))
    print("           distance to the nearest decision boundary: %.3f ranking units = %.1f units of the"
          " lever's own noise (%.4f), and %.1f standard errors of the ranked quantity (%.4f)"
          % (margin, margin / lever_noise_units, lever_noise_units,
             margin / (dec[GOLDEN] * se_log_rise(g)), dec[GOLDEN] * se_log_rise(g)))
    lo, hi = alpha_corridor(t)
    print("  C3 corridor: the golden leads for every exposure elasticity in [%.3f, %.3f]; "
          "the fitted value is %.3f" % (lo, hi, beta))
    print("  knob sweep, redundancy family: " + ", ".join(
        "q=%.2f %s" % (q, max(routes(t, q_red=q)["C redundancy_capture"].items(),
                              key=lambda kv: kv[1])[0]) for q in (0.10, 0.25, 0.40, 0.55)))

    sw = seed_sweep(t)
    print("\n  seed sweep over %d seeds: decisive route names the golden %d, default path misses it %d"
          % (sw["seeds"], sw["decisive_hits"], sw["default_misses"]))
    print("  golden's default-path position min %d max %d mean %.1f; decisive min %d max %d mean %.2f"
          % (sw["pos_raw"] + sw["pos_dec"]))

    print("\n  orthogonality inside the %d-city pool:" % len(POOL))
    idx = {m[0]: m for m in PANEL}
    pres_m = [idx[n][7] for n in POOL]
    lam_m = [idx[n][6] for n in POOL]
    cols = {"pop": [idx[n][1] for n in POOL], "baseline actions": [idx[n][2] for n in POOL],
            "baseline presence": [idx[n][3] for n in POOL],
            "presence per 100k": [idx[n][3] / idx[n][1] * 1e5 for n in POOL],
            "baseline capture": [idx[n][4] for n in POOL],
            "baseline citations": [idx[n][5] for n in POOL],
            "recorded baseline": [t[n]["n_b"] for n in POOL],
            "window rate": [rate_per_100k(t[n]) for n in POOL]}
    mx = 0.0
    for lab, col in cols.items():
        a, b = corr(pres_m, col), corr(lam_m, col)
        mx = max(mx, abs(a), abs(b))
        print("    %-20s corr(presence mult)=%+.3f corr(activity mult)=%+.3f" % (lab, a, b))
    print("    max |corr| %.3f" % mx)
    print("  the golden against the three presence risers, on every static attribute:")
    for lab in ("baseline capture", "presence per 100k", "baseline citations", "window rate"):
        g = cols[lab][POOL.index(GOLDEN)]
        rng = [cols[lab][POOL.index(n)] for n in ("Sardinata", "El Tarra", "Convencion")]
        inside = min(rng) <= g <= max(rng)
        print("    %-20s golden %8.1f against risers %s -> %s"
              % (lab, g, " ".join("%.1f" % x for x in sorted(rng)),
                 "inside their range" if inside else "OUTSIDE their range"))

    print("\n" + "=" * 98)
    print("4  GRADED FIGURE: bin position")
    print("=" * 98)
    for nm in o_raw[:5]:
        v = rate_per_100k(t[nm])
        edge = 0.05 - abs(v - round(v, 1))
        print("  %-17s %8.3f  prints %5.1f  edge distance %.4f = %.2f of the unit"
              % (nm, v, round(v, 1), edge, edge / 0.1))

    print("\n" + "=" * 98)
    print("4b SCREEN 6: what a subset of the records hands over")
    print("=" * 98)
    s6 = screen6(t)
    for label in ("presence steps first, activity later", "both step together on " + STEP,
                  "activity steps first, presence later"):
        w, v, pos = s6[label]
        print("  short pre-window baseline, %-38s winner %-12s %.3f, golden at %d"
              % (label, w, v, pos))
    print("  -> only the first placement hands the golden to a raw comparison with no denominator, so")
    print("     every presence shift and the activity rise step together on %s and every pre-window" % STEP)
    print("     and sub-window month carries the baseline's own levels (asserted in checks.py).")
    print("  highest retained/delivered ratio over every city and span: %.3f, so the wrong denominator"
          % s6["max_retained_over_delivered"])
    print("     never meets the right one on any subset")
    print("  thinnest panel city-month: %.0f delivered items, so no panel city-month is empty and"
          % s6["thinnest_delivered_month"])
    print("     presence is readable only inside the decisive family")

    print("\n" + "=" * 98)
    print("5  ASK STOPS (clean truth; re-measured on the cut pack at stage 3)")
    print("=" * 98)
    for k, a in ASKS.items():
        print("  ask %s  %s" % (k, a["name"]))
        vals = list(a["stops"].values())
        gold = vals[-1]
        for label, v in a["stops"].items():
            print("      %-72s %10.1f %s" % (label, v, "<- golden" if v == gold else
                                             "delta %+.1f" % (v - gold)))
        print("      figures %d; primary %s" % (a["figures"], a["primary"][:60] + "..."))


if __name__ == "__main__":
    main()
