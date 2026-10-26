"""The pack's data files for task270, each in its own system's layout: the experimentation platform's scorecard export
and experiment registry, the warehouse's 2025 global holdout table, the growth analytics team's 2025 sign-up cohort
table, the 2027 first-quarter onboarding calendar, the forecasting tool's 2027 new-user forecast, and two files the
growth team keeps beside them (store ratings and acquisition spend)."""
import csv
import datetime as dt
import hashlib

import numpy as np

import common as K

ARM_STYLES = [("control", "treatment", "treatment_2"), ("control", "variant_a", "variant_b"), ("A", "B", "C"),
              ("baseline", "variant", "variant_2"), ("ctrl", "test", "test_2"), ("Control", "Variant 1", "Variant 2")]

TITLES = {
    "signup_flow": ["Sign up with Apple first on iOS", "Size and fit step before the first feed", "Shorter sign-up form",
                    "Phone check moved after first browse", "Brand picker at sign-up", "Welcome voucher screen",
                    "Email magic link instead of password", "Style quiz, three questions", "Skip button on interests",
                    "Postcode asked at sign-up", "Seller or buyer question first", "Google sign-in above email",
                    "Progress bar on sign-up", "Interests prefilled from referral", "Avatar step removed",
                    "Terms on one screen", "Kids' sizes in the size step", "Sign-up after first item view"],
    "first_feed": ["Feed sorted by nearby sellers", "Bundle discount banner in first feed", "Buyer protection badge",
                   "Trending brands carousel", "Price-drop card for saved items", "Items in your size first",
                   "Hide sold items in feed", "Larger photos in first feed", "Free shipping filter on",
                   "Recently listed near you", "Follow three sellers prompt", "Vintage tab in first session",
                   "Feed from the style quiz", "Swipe to save", "First-feed category chips", "Seller ratings on cards",
                   "Make an offer button on cards", "Sustainability label on cards"],
    "notifications": ["Saved-search alert on day 2", "Price drop push for favourites", "Weekly digest push",
                      "Seller reply push", "Back in your size push", "Abandoned offer reminder",
                      "Push permission after first save", "Quiet hours by default", "New items from followed sellers",
                      "Day 7 come-back push", "Bundle reminder push", "Push permission primer screen",
                      "Price drop push batching", "Wishlist sale alert", "First message nudge"],
}


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(head)
        w.writerows(rows)


def iso(d):
    return d.isoformat()


def f6(x):
    s = "%.6f" % x
    return "0.000000" if s == "-0.000000" else s


def user_id(seed, d, i):
    h = hashlib.sha1(("%d|%s|%d" % (seed, d.isoformat(), i)).encode()).hexdigest()
    n = int(h[:14], 16)
    a = "0123456789abcdefghijklmnopqrstuvwxyz"
    s = ""
    for _ in range(9):
        n, k = divmod(n, 36)
        s += a[k]
    return "u" + s


class Records:
    def __init__(self, world, seed=K.SEED):
        self.w = world
        self.seed = seed
        rng = np.random.default_rng([270, seed, 20])
        used = {layer: 0 for layer in K.LAYERS}
        self.labels, self.titles = {}, {}
        for e in world.experiments:
            st = ARM_STYLES[int(rng.integers(0, len(ARM_STYLES)))]
            self.labels[e.idx] = list(st[:e.arms])
            pool = TITLES[e.layer]
            t = pool[used[e.layer] % len(pool)]
            rnd = used[e.layer] // len(pool)
            used[e.layer] += 1
            self.titles[e.idx] = t if rnd == 0 else "%s (%s)" % (t, ["retest", "v2", "v3", "round 4"][min(rnd - 1, 3)])

    def in_export(self, e):
        return e.two_week_at <= K.PULL and e.end <= self.w.last_day

    # --------------------------------------------------------------------------------------------- scorecard export
    def scorecard_rows(self):
        head = ["experiment_id", "arm", "metric", "users", "mean", "std_dev", "computed_at"]
        rows = []
        for e in self.w.experiments:
            if not self.in_export(e):
                continue
            labels = self.labels[e.idx]
            comps = []
            if e.late:
                comps.append((e.two_week_at, True, False))
                comps.append((K.RECOMPUTED, False, False))
            else:
                comps.append((e.two_week_at, False, False))
            if e.six_month_at <= K.PULL:
                comps.append((e.six_month_at, False, True))
            for when, late, six in comps:
                for a in range(e.arms):
                    n, mean, sd = self.w.arm_stats(e, a, late=late)
                    idx = [5] if six else [0, 1, 2, 3, 4, 6, 7]
                    for j in idx:
                        key = K.METRICS[j]
                        key = K.OLD_KEY[key] if when < K.RENAME else key
                        rows.append([e.eid, labels[a], key, n, f6(mean[j]), f6(sd[j]), iso(when)])
        rows.sort(key=lambda r: (r[0], r[6], r[2], self._arm_order(r[0], r[1])))
        return head, rows

    def _arm_order(self, eid, label):
        return label

    # ---------------------------------------------------------------------------------------------------- registry
    def registry_rows(self):
        head = ["experiment_id", "title", "layer", "owning_team", "start_date", "planned_end_date", "end_date", "arms",
                "control_arm", "status", "srm_check", "decision", "shipped_on", "six_month_read_closes"]
        rows = []
        for e in self.w.experiments:
            if e.start > K.PULL:
                continue
            labels = self.labels[e.idx]
            running = e.end > self.w.last_day or e.two_week_at > K.PULL
            status = "running" if e.end > K.PULL else ("analysing" if running else e.status)
            if running:
                decision, shipped = "", ""
            elif e.decision and "shipped" in e.decision:
                arm = labels[1 + e.decision.index("shipped")]
                decision, shipped = "shipped %s" % arm, iso(e.ship) if e.ship <= K.PULL else ""
                if not shipped:
                    decision = "ship %s" % arm
            else:
                decision, shipped = "not shipped", ""
            srm = "" if running else ("fail" if e.srm else "pass")
            rows.append([e.eid, self.titles[e.idx], e.layer, e.team, iso(e.start), iso(e.planned_end),
                         "" if e.end > K.PULL else iso(e.end), ";".join(labels), labels[0], status, srm, decision,
                         shipped, iso(e.six_month_at)])
        return head, rows

    # ----------------------------------------------------------------------------------------------------- holdout
    def holdout_rows(self):
        head = ["user_id", "signed_up_on", "platform", "country"] + K.CAND + [K.RET]
        rows = []
        count = {}
        for r in self.w.holdout_rows:
            d, ios, be = r[0], r[1], r[2]
            i = count.get(d, 0)
            count[d] = i + 1
            vals = [int(round(v)) for v in r[3:9]]
            rows.append([user_id(self.seed, d, i), iso(d), "ios" if ios else "android", "BE" if be else "NL"] + vals)
        rows.sort(key=lambda x: (x[1], x[0]))
        return head, rows

    # ------------------------------------------------------------------------------------------- 2025 cohort table
    def cohort_rows(self):
        """sign-ups by day, platform and country, split by the type each account signed up as and the type it holds at
        the table's refresh (consumers who later upgraded to a business account are counted under business now); the
        consumer counts take in every new consumer, the global holdout's users included; the days of the Black Friday
        fortnight were refreshed again after the order backfill"""
        head = ["signup_date", "platform", "country", "account_type", "signup_account_type", "new_users",
                "active_days_total", "sessions_total", "first_purchases", "items_saved_total", "push_opens_total",
                "retained_m6_users", "refreshed_at"]
        rows = []
        rng = np.random.default_rng([270, self.seed, 21])
        bf = (dt.date(2025, 11, 24), dt.date(2025, 12, 14))
        for (d, ios, be), acc in sorted(self.w.cohort.items(), key=lambda x: (x[0][0], not x[0][1], x[0][2])):
            cv = self.w.converted[(d, ios, be)]
            plat, ctry = "ios" if ios else "android", "BE" if be else "NL"
            parts = [("consumer", "consumer", int(acc[0] - cv[0]), acc[2:8] - cv[1:7]),
                     ("business", "consumer", int(cv[0]), cv[1:7])]
            for now, at_signup, n, sums in parts:
                if n <= 0:
                    continue
                vals = [int(round(v)) for v in sums]
                base = [iso(d), plat, ctry, now, at_signup, n]
                if bf[0] <= d <= bf[1]:
                    early = list(vals)
                    early[2] = int(round(vals[2] * (1 - rng.uniform(0.05, 0.09))))
                    rows.append(base + early + ["2026-07-06"])
                    rows.append(base + vals + ["2026-08-03"])
                else:
                    rows.append(base + vals + ["2026-07-06"])
            b = self.w.business.get((d, ios, be))
            if b is not None and b[0] > 0:
                rows.append([iso(d), plat, ctry, "business", "business", int(b[0])] +
                            [int(round(v)) for v in b[1:7]] + ["2026-07-06"])
        return head, rows

    # ----------------------------------------------------------------------------------- 2027 calendar and forecast
    CALENDAR = [
        ("OB-27-001", "Size and fit step with photos", "signup_flow", "all", dt.date(2027, 1, 4), dt.date(2027, 1, 31), 2, "Activation"),
        ("OB-27-002", "Sign up with Apple, one tap", "signup_flow", "ios", dt.date(2027, 1, 11), dt.date(2027, 2, 7), 2, "Identity"),
        ("OB-27-003", "Interests from the first three saves", "signup_flow", "all", dt.date(2027, 2, 1), dt.date(2027, 2, 28), 3, "Activation"),
        ("OB-27-004", "First feed in your size and area", "first_feed", "all", dt.date(2027, 1, 4), dt.date(2027, 2, 7), 2, "Discovery"),
        ("OB-27-005", "Buyer protection explainer card", "first_feed", "android", dt.date(2027, 1, 18), dt.date(2027, 2, 14), 2, "Buyer Experience"),
        ("OB-27-006", "Saved-search alert after first search", "notifications", "all", dt.date(2027, 2, 15), dt.date(2027, 3, 14), 2, "Messaging"),
        ("OB-27-007", "Push permission after the first save", "notifications", "android", dt.date(2027, 3, 1), dt.date(2027, 3, 28), 2, "Lifecycle"),
    ]

    def calendar_rows(self):
        head = ["experiment_id", "title", "layer", "platforms", "start_date", "end_date", "arms", "owning_team"]
        return head, [[a, b, c, d, iso(s), iso(t), n, tm] for a, b, c, d, s, t, n, tm in self.CALENDAR]

    def forecast_weekly(self):
        """the forecasting tool's weekly new consumer users by platform, 2027, from the 2026 run rate"""
        rng = np.random.default_rng([270, self.seed, 22])
        out = {}
        monday = dt.date(2026, 12, 28)          # ISO week 2026-W53 runs to 3 January 2027
        while monday <= dt.date(2027, 12, 27):
            mid = monday + dt.timedelta(days=3)
            g = 1.0 + 0.085 * ((mid - dt.date(2024, 1, 1)).days / 365.25)
            from world import MONTH, WEEKDAY
            wk = self.w.p["BASE"] * g * MONTH[mid.month - 1] * sum(WEEKDAY)
            for plat, share in (("ios", 0.46), ("android", 0.54)):
                out[(monday, plat)] = int(round(wk * share * rng.uniform(0.985, 1.015), -1))
            monday += dt.timedelta(days=7)
        return out

    def forecast_rows(self):
        """one line a day and platform; the tool writes each ISO week's forecast on every day of that week"""
        head = ["date", "iso_week", "platform", "new_consumer_users_forecast"]
        wk = self.forecast_weekly()
        rows = []
        d = dt.date(2027, 1, 1)
        while d <= dt.date(2027, 12, 31):
            monday = d - dt.timedelta(days=d.weekday())
            y, w, _ = d.isocalendar()
            for plat in ("ios", "android"):
                rows.append([iso(d), "%d-W%02d" % (y, w), plat, wk[(monday, plat)]])
            d += dt.timedelta(days=1)
        return head, rows

    # --------------------------------------------------------------------------------------------- the distractors
    def ratings_rows(self):
        head = ["week_starting", "store", "new_ratings", "average_rating", "written_reviews"]
        rng = np.random.default_rng([270, self.seed, 23])
        rows = []
        d = dt.date(2024, 1, 1)
        lvl = {"App Store": 4.62, "Google Play": 4.41}
        while d <= dt.date(2026, 10, 12):
            for store in ("App Store", "Google Play"):
                lvl[store] = min(4.85, max(4.0, lvl[store] + rng.normal(0, 0.012)))
                n = int(rng.poisson(1650 if store == "App Store" else 2100))
                rows.append([iso(d), store, n, "%.2f" % (lvl[store] + rng.normal(0, 0.03)),
                             int(rng.binomial(n, 0.21))])
            d += dt.timedelta(days=7)
        return head, rows

    def spend_rows(self):
        rng = np.random.default_rng([270, self.seed, 24])
        chans = [("Paid social", 182000, 2.9), ("Search", 96000, 3.6), ("Creators and influencers", 74000, 4.4),
                 ("Online video", 51000, 6.1), ("Referral credits", 38000, 2.2), ("App store ads", 44000, 3.1)]
        rows = []
        for m in range(1, 10):
            for c, base, cpi in chans:
                spend = base * (1.15 if m in (1, 9) else 1.0) * rng.uniform(0.9, 1.1)
                inst = int(spend / (cpi * rng.uniform(0.92, 1.08)))
                rows.append([dt.date(2026, m, 1), c, round(spend, 2), inst])
        return rows
