"""The records behind task268's asks, on their own random streams so the main call's world never moves with them:
the deployment tool's production log (releases and rollbacks), the cloud provider's billing lines, invoices and
resource inventory (each service's cost by half), and the incident tool's export beside the public status page's
history (each service's customer-facing incident minutes by half). The truth of each ask is kept beside its records."""
import datetime as dt

import numpy as np

import common as K

Y0 = dt.datetime(2026, 1, 1)
Y1 = dt.datetime(2027, 1, 1)
H1_END = dt.datetime(2026, 7, 1)          # halves are read in Lisbon time; 1 July 00:00 Lisbon is 30 June 23:00 UTC


def lisbon_offset(t_utc):
    """Lisbon's offset from UTC at a UTC instant: +1 from 01:00 UTC on the last Sunday of March to 01:00 UTC on the
    last Sunday of October."""
    def last_sunday(m):
        d = dt.datetime(2026, m, 31 if m in (3, 10) else 30)
        while d.weekday() != 6:
            d -= dt.timedelta(days=1)
        return d.replace(hour=1)
    return 1 if last_sunday(3) <= t_utc < last_sunday(10) else 0


def to_lisbon(t_utc):
    return t_utc + dt.timedelta(hours=lisbon_offset(t_utc))


def half_of(t_lisbon):
    return 1 if t_lisbon < H1_END else 2


# ------------------------------------------------------------------ deployments
PIPELINE_SA = "system:serviceaccount:delivery:pipeline-deployer"
MIGRATION_SA = "system:serviceaccount:platform:cluster-migration"
CUTOVER = dt.datetime(2026, 4, 14, 5, 30)        # production moved to the prd-lis-2 cluster
ON_CALL = ["ipereira", "fvalente", "mdomingues", "ateixeira", "rcosta", "lsantos", "jmatos"]


def _sha(r):
    return "".join("%02x" % b for b in r.integers(0, 256, 20, dtype=np.uint8))


def deployments(seed=K.SEED + 101):
    """Each service's 2026 changes to production in two systems. The delivery pipeline's log holds its staging and
    production attempts by version and commit; the production cluster's rollout history holds every change to the
    service's deployment, whoever made it, each image tagged by its commit's short hash. On-call engineers undo
    releases and apply hotfix images by hand, and restart deployments; those changes reach the rollout history only.
    A release is a version reaching production for the first time; a rollback replaces production's running version
    with a version first released before it. Neither system flags either."""
    r = np.random.default_rng(seed)
    rows, hist, truth = [], [], {}
    used_ids = set()
    pace = {"journey-search": 46, "fares": 38, "places": 30, "seat-map": 34, "booking": 26, "payments": 18,
            "tickets": 22, "accounts": 28, "partner-gateway": 40, "notifications": 24}
    roll_p = {"journey-search": 0.08, "fares": 0.04, "places": 0.10, "seat-map": 0.12, "booking": 0.06,
              "payments": 0.10, "tickets": 0.03, "accounts": 0.05, "partner-gateway": 0.14, "notifications": 0.02}
    did = 0
    for svc in K.SVC:
        name = K.TRACE_NAME[svc]
        n_rel = pace[svc]
        major, minor, patch = int(r.integers(2, 6)), int(r.integers(0, 30)), 0
        days = np.sort(r.choice(np.arange(3, 356), n_rel, replace=False))
        after = [j for j in range(1, n_rel - 1) if Y0 + dt.timedelta(days=int(days[j])) > CUTOVER + dt.timedelta(days=1)]
        cand = after
        undo_i = {int(x) for x in r.choice(cand, int(r.integers(1, 4)), replace=False)}
        hot_i = {int(x) for x in r.choice([c for c in cand if c not in undo_i], int(r.integers(1, 3)), replace=False)}
        version_of = {}
        first = {}
        state = {"rev": int(r.integers(40, 400)), "running": None, "rel": 0, "roll": 0}

        def change(t, sha, by):
            state["rev"] += 1
            hist.append({"deployment": name, "revision": state["rev"], "image": "registry.rotalinha.pt/platform/%s:%s"
                         % (name, sha[:7]), "changed_at": t, "changed_by": by})
            run = state["running"]
            if sha not in first:
                first[sha] = t
                if t >= Y0:
                    state["rel"] += 1
            elif run is not None and sha != run and first[sha] < first[run]:
                state["roll"] += 1
            state["running"] = sha

        def emit(v, env, start, outcome):
            nonlocal did
            did += 1
            dur = int(r.integers(240, 1500))
            while True:
                dep_id = "dep-%06d" % int(r.integers(100000, 999999))
                if dep_id not in used_ids:
                    used_ids.add(dep_id)
                    break
            rows.append({"deployment_id": dep_id, "service": name, "environment": env,
                         "version": v, "commit": [c for c, vv in version_of.items() if vv == v][0],
                         "started_at": start, "finished_at": start + dt.timedelta(seconds=dur), "outcome": outcome,
                         "triggered_by": r.choice(["pipeline", "pipeline", "pipeline", "manual"])})
            return start + dt.timedelta(seconds=dur)

        # the image running when the year opened, from a 2025 release
        sha0 = _sha(r)
        version_of[sha0] = "%d.%d.%d" % (major, minor, patch)
        t0 = Y0 - dt.timedelta(days=int(r.integers(3, 25)), hours=int(r.integers(8, 18)))
        first[sha0] = t0
        state["rev"] += 1
        hist.append({"deployment": name, "revision": state["rev"], "image": "registry.rotalinha.pt/platform/%s:%s"
                     % (name, sha0[:7]), "changed_at": t0, "changed_by": PIPELINE_SA})
        state["running"] = sha0
        prev_end = Y0
        for i, d in enumerate(days):
            if r.random() < 0.25:
                minor += 1
                patch = 0
            else:
                patch += 1
            ver = "%d.%d.%d" % (major, minor, patch)
            sha = _sha(r)
            version_of[sha] = ver
            t = Y0 + dt.timedelta(days=int(d), hours=int(r.integers(8, 18)), minutes=int(r.integers(0, 60)))
            t = max(t, prev_end + dt.timedelta(minutes=30))
            t_next = (Y0 + dt.timedelta(days=int(days[i + 1]), hours=7)) if i + 1 < n_rel else Y1 - dt.timedelta(days=1)
            before = state["running"]
            # staging first, then production; one in seven production attempts fails and is retried
            emit(ver, "staging", t - dt.timedelta(hours=int(r.integers(2, 30))), "succeeded")
            tt = t
            if r.random() < 1 / 7:
                tt = emit(ver, "production", tt, "failed") + dt.timedelta(minutes=int(r.integers(10, 90)))
            start = tt
            tt = emit(ver, "production", tt, "succeeded")
            change(start + dt.timedelta(seconds=int(r.integers(8, 40))), sha, PIPELINE_SA)
            cur = [tt]
            limit = t_next - dt.timedelta(hours=2)

            def later(lo, hi):
                """A follow-up change after the last one, lo to hi hours on, or None when the next release is too
                close."""
                t_ = cur[0] + dt.timedelta(hours=float(r.uniform(lo, hi)))
                if t_ >= limit:
                    return None
                cur[0] = t_
                return t_
            if i in undo_i:
                # on call undoes the release by hand: the deployment goes back to its previous revision's image
                tu = later(0.3, 6)
                if tu is not None:
                    prev_img = hist[-2]["image"].rsplit(":", 1)[1]
                    back = [k for k in first if k[:7] == prev_img][0]
                    change(tu, back, str(r.choice(ON_CALL)))
                    if r.random() < 0.5:
                        # the fixed config goes out with the same version through the pipeline: neither
                        tr = later(6, 30)
                        if tr is not None:
                            cur[0] = emit(ver, "production", tr, "succeeded")
                            change(tr + dt.timedelta(seconds=int(r.integers(8, 40))), sha, PIPELINE_SA)
            elif r.random() < roll_p[svc] and i > 0 and before in version_of:
                # a rollback through the pipeline to the version before
                tb = later(1, 20)
                if tb is not None:
                    cur[0] = emit(version_of[before], "production", tb, "succeeded")
                    change(tb + dt.timedelta(seconds=int(r.integers(8, 40))), before, PIPELINE_SA)
                    if r.random() < 0.35:
                        tr = later(22, 50)
                        if tr is not None:
                            cur[0] = emit(ver, "production", tr, "succeeded")
                            change(tr + dt.timedelta(seconds=int(r.integers(8, 40))), sha, PIPELINE_SA)
            if i in hot_i:
                # a hotfix image built from a branch and applied by hand: a version no pipeline record carries
                th = later(2, 40)
                if th is not None:
                    change(th, _sha(r), str(r.choice(ON_CALL)))
            if r.random() < 0.12 and cur[0] > CUTOVER:
                # a restart re-applies the running image: neither
                tr = later(3, 60)
                if tr is not None:
                    change(tr, state["running"], str(r.choice(ON_CALL)))
            if r.random() < 0.10 and state["running"] in version_of:
                # a config refresh through the pipeline, same version: neither
                tc = later(4, 80)
                if tc is not None:
                    cur[0] = emit(version_of[state["running"]], "production", tc, "succeeded")
                    change(tc + dt.timedelta(seconds=int(r.integers(8, 40))), state["running"], PIPELINE_SA)
            tt = cur[0]
            prev_end = max(tt, prev_end)
        truth[svc] = {"releases": state["rel"], "rollbacks": state["roll"]}
    # the old cluster's history went with it: the export is prd-lis-2's, whose revisions start at the cutover with the
    # image each service was running
    out = []
    for name in sorted({h["deployment"] for h in hist}):
        hs = sorted([h for h in hist if h["deployment"] == name], key=lambda h: (h["changed_at"], h["revision"]))
        pre = [h for h in hs if h["changed_at"] < CUTOVER]
        post = [h for h in hs if h["changed_at"] >= CUTOVER]
        out.append({"deployment": name, "revision": 1, "image": pre[-1]["image"],
                    "changed_at": CUTOVER + dt.timedelta(minutes=int(r.integers(2, 50)), seconds=int(r.integers(0, 60))),
                    "changed_by": MIGRATION_SA})
        for j, h in enumerate(post):
            out.append({**h, "revision": j + 2})
    out.sort(key=lambda x: (x["changed_at"], x["deployment"], x["revision"]))
    rows.sort(key=lambda x: (x["started_at"], x["deployment_id"]))
    return rows, out, truth


# ------------------------------------------------------------------ cloud billing
# each service's resources: (resource kind, product, monthly EUR in January, monthly growth)
RES = {
    "journey-search": [("cluster", "Compute", 9400, 0.020), ("cache", "Database", 2100, 0.010), ("storage", "Storage", 380, 0.03)],
    "fares": [("cluster", "Compute", 5200, 0.012), ("database", "Database", 2600, 0.008)],
    "places": [("cluster", "Compute", 3900, 0.015), ("index", "Database", 3300, 0.012)],
    "seat-map": [("cluster", "Compute", 2400, 0.010), ("cache", "Database", 900, 0.005)],
    "booking": [("cluster", "Compute", 2900, 0.008), ("database", "Database", 4100, 0.010)],
    "payments": [("cluster", "Compute", 1800, 0.006), ("database", "Database", 2200, 0.004)],
    "tickets": [("cluster", "Compute", 1500, 0.006), ("storage", "Storage", 1300, 0.025)],
    "accounts": [("cluster", "Compute", 2100, 0.006), ("database", "Database", 1700, 0.006)],
    "partner-gateway": [("cluster", "Compute", 4300, 0.018), ("queue", "Messaging", 760, 0.012)],
    "notifications": [("cluster", "Compute", 1200, 0.004), ("queue", "Messaging", 640, 0.006)],
}
# resources replaced during the year: the old one ran under a team tag until the replacement took over
REPLACED = {("journey-search", "cache"): 95, ("journey-search", "cluster"): 238,
            ("fares", "database"): 66, ("fares", "cluster"): 301,
            ("places", "index"): 120, ("places", "cluster"): 214,
            ("seat-map", "cache"): 47, ("seat-map", "cluster"): 266,
            ("booking", "database"): 152, ("booking", "cluster"): 199,
            ("payments", "database"): 88, ("payments", "cluster"): 325,
            ("tickets", "cluster"): 133, ("tickets", "storage"): 210,
            ("accounts", "database"): 58, ("accounts", "cluster"): 287,
            ("partner-gateway", "queue"): 110, ("partner-gateway", "cluster"): 248,
            ("notifications", "queue"): 140, ("notifications", "cluster"): 309}
# marketplace software billed in US dollars: (service, product name, monthly USD)
MARKET = [("journey-search", "Typesense Cloud (Marketplace)", 1650), ("places", "Geocoding API (Marketplace)", 2280),
          ("notifications", "SMS gateway (Marketplace)", 1340), ("partner-gateway", "API monitoring (Marketplace)", 410)]


def billing(seed=K.SEED + 202):
    r = np.random.default_rng(seed)
    resources, lines = [], []
    invoices = []
    rate = {}
    for m in range(1, 13):
        rate[m] = round(float(1.0 / r.uniform(1.035, 1.145)), 4)        # EUR per USD on the invoice
        inv = "INV-PT-2026%02d-%04d" % (m, int(r.integers(1000, 9999)))
        invoices.append({"invoice_id": inv, "billing_period": "2026-%02d" % m, "currency": "EUR",
                         "usd_eur_rate": rate[m],
                         "issued_on": (dt.date(2026, m, 1) + dt.timedelta(days=34)).replace(day=3)})
    inv_of = {int(i["billing_period"][-2:]): i["invoice_id"] for i in invoices}
    rid = 7100
    truth = {s: [0.0, 0.0] for s in K.SVC}

    def new_id():
        nonlocal rid
        rid += int(r.integers(3, 40))
        return "rsc-%06x" % (rid * 2654435761 % 0xFFFFFF)
    compute_ids = {svc: [] for svc in K.SVC}
    for svc in K.SVC:
        for kind, product, eur, g in RES[svc]:
            day_cut = REPLACED.get((svc, kind))
            ids = [new_id()]
            if day_cut:
                ids.append(new_id())
                resources.append({"resource_id": ids[0], "kind": kind, "created": dt.date(2024, 9, 2) + dt.timedelta(days=int(r.integers(0, 300))),
                                  "deleted": dt.date(2026, 1, 1) + dt.timedelta(days=day_cut), "replaces": "",
                                  "tags": "team=%s;env=prd" % K.OLD_TAG[svc]})
                resources.append({"resource_id": ids[1], "kind": kind, "created": dt.date(2026, 1, 1) + dt.timedelta(days=day_cut - 2),
                                  "deleted": "", "replaces": ids[0], "tags": "service=%s;team=%s;env=prd" % (K.COST_TAG[svc], K.OLD_TAG[svc])})
            else:
                resources.append({"resource_id": ids[0], "kind": kind, "created": dt.date(2024, 3, 1) + dt.timedelta(days=int(r.integers(0, 500))),
                                  "deleted": "", "replaces": "", "tags": "service=%s;team=%s;env=prd" % (K.COST_TAG[svc], K.OLD_TAG[svc])})
            if product == "Compute":
                compute_ids[svc].extend(ids)
            for d in range(365):
                day = dt.date(2026, 1, 1) + dt.timedelta(days=d)
                which = 0 if (day_cut and d < day_cut) else (1 if day_cut else 0)
                res_id = ids[which]
                daily = eur * (1 + g) ** (d / 30.4) / 30.4 * r.uniform(0.9, 1.1)
                if svc in ("journey-search", "places", "partner-gateway") and day.month == 12:
                    daily *= 1.25
                cost = round(daily, 2)
                tag = ("team=%s;env=prd" % K.OLD_TAG[svc]) if (day_cut and d < day_cut) else \
                    ("service=%s;team=%s;env=prd" % (K.COST_TAG[svc], K.OLD_TAG[svc]))
                lines.append({"usage_date": day, "invoice_id": inv_of[day.month], "resource_id": res_id,
                              "resource_tags": tag, "product": product, "line_type": "usage", "currency": "EUR",
                              "cost": cost, "description": "%s %s usage" % (product, kind)})
                truth[svc][0 if day < dt.date(2026, 7, 1) else 1] += cost
    # sustained-use credits on compute, one line a month per cluster, dated the last day of the month and booked to the
    # cluster running that day
    for svc in K.SVC:
        ids = set(compute_ids[svc])
        for m in range(1, 13):
            last = (dt.date(2026, m + 1, 1) if m < 12 else dt.date(2027, 1, 1)) - dt.timedelta(days=1)
            usage = sum(x["cost"] for x in lines if x["resource_id"] in ids and x["usage_date"].month == m)
            cr = -round(0.06 * usage * r.uniform(0.9, 1.1), 2)
            on = [x for x in lines if x["resource_id"] in ids and x["usage_date"] == last][0]
            lines.append({"usage_date": last, "invoice_id": inv_of[m], "resource_id": on["resource_id"],
                          "resource_tags": on["resource_tags"], "product": "Compute", "line_type": "credit",
                          "currency": "EUR", "cost": cr, "description": "Sustained use discount"})
            truth[svc][0 if last < dt.date(2026, 7, 1) else 1] += cr
    # marketplace software in US dollars, one line a month, no resource of its own
    for svc, name, usd in MARKET:
        for m in range(1, 13):
            amt = round(usd * r.uniform(0.95, 1.08), 2)
            day = dt.date(2026, m, 1)
            lines.append({"usage_date": day, "invoice_id": inv_of[m], "resource_id": "",
                          "resource_tags": "service=%s;env=prd" % K.COST_TAG[svc], "product": name,
                          "line_type": "usage", "currency": "USD", "cost": amt, "description": "Monthly subscription"})
            truth[svc][0 if m <= 6 else 1] += amt * rate[m]
    # VAT on every invoice, and shared platform costs tagged to no service
    for m in range(1, 13):
        lines.append({"usage_date": dt.date(2026, m, 1), "invoice_id": inv_of[m], "resource_id": "",
                      "resource_tags": "team=platform;env=shared", "product": "Support plan", "line_type": "usage",
                      "currency": "EUR", "cost": round(4200 * r.uniform(0.98, 1.02), 2), "description": "Business support"})
    totals = {}
    month_of = {v: k for k, v in inv_of.items()}
    for x in lines:
        eur = x["cost"] * (rate[month_of[x["invoice_id"]]] if x["currency"] == "USD" else 1.0)
        totals[x["invoice_id"]] = totals.get(x["invoice_id"], 0.0) + eur
    for m in range(1, 13):
        inv = inv_of[m]
        vat = round(0.23 * totals[inv], 2)
        lines.append({"usage_date": dt.date(2026, m, 1), "invoice_id": inv, "resource_id": "", "resource_tags": "",
                      "product": "VAT", "line_type": "tax", "currency": "EUR", "cost": vat, "description": "IVA 23%"})
    lines.sort(key=lambda x: (x["usage_date"], x["invoice_id"], x["resource_id"], x["product"], x["line_type"]))
    resources.sort(key=lambda x: x["resource_id"])
    truth = {s: [round(v[0], 2), round(v[1], 2)] for s, v in truth.items()}
    return lines, invoices, resources, truth, rate


def _svc_of_tag(tags):
    for part in tags.split(";"):
        if part.startswith("service="):
            v = part.split("=", 1)[1]
            for s in K.SVC:
                if K.COST_TAG[s] == v:
                    return s
    for part in tags.split(";"):
        if part.startswith("team="):
            return part.split("=", 1)[1]
    return None


# ------------------------------------------------------------------ incidents and the status page
def incidents(seed=K.SEED + 305):
    """The incident tool holds every incident with its declaration, the services it named by the time it was closed
    and the administrative close after the review; its timeline holds each event, the moment each service was named
    among them; the status page holds the public posts and each component's status changes in Lisbon local time. A
    customer-facing incident's minutes run from its declaration until the status page shows every component it
    affected operational again, and a service's minutes are those in which such an incident named it, counted once.
    The tool and the page share no key."""
    r = np.random.default_rng(seed)
    inc, posts, changes, timeline = [], [], [], []
    iv = {s: [] for s in K.SVC}
    need = {(h, s) for h in (1, 2) for s in K.SVC}
    fold = dt.datetime(2026, 10, 25, 0, 0)
    n = 0
    t = Y0 + dt.timedelta(days=3)
    while True:
        t += dt.timedelta(hours=float(r.uniform(55, 150)))
        if t >= Y1 - dt.timedelta(days=3):
            if not need:
                break
            t = Y0 + dt.timedelta(days=3, hours=float(r.uniform(0, 40)))     # a second pass for any cell still empty
            continue
        if any(abs((t - x["declared_at"]).total_seconds()) < 30 * 3600 for x in inc):
            continue
        half = 1 if t < H1_END - dt.timedelta(hours=1) else 2
        open_cells = sorted(s_ for (h, s_) in need if h == half)
        near_fold = fold - dt.timedelta(hours=8) <= t <= fold + dt.timedelta(hours=3)
        if open_cells and not near_fold and r.random() < 0.75:
            lead = open_cells[int(r.integers(0, len(open_cells)))]
            posted = True
        else:
            lead = K.SVC[int(r.integers(0, len(K.SVC)))]
            posted = (not near_fold) and r.random() < 0.3
        k = 1 if r.random() < 0.45 else (2 if r.random() < 0.7 else 3)
        others = [x for x in K.SVC if x != lead]
        svcs = [lead] + [str(x) for x in r.choice(others, k - 1, replace=False)]
        n += 1
        iid = "INC-%04d" % (1000 + n * 7 + int(r.integers(0, 7)))
        sev = "SEV%d" % (1 if r.random() < 0.15 else (2 if r.random() < 0.55 else 3))
        declared = t.replace(second=int(r.integers(0, 60)), microsecond=0)
        mins = int(r.integers(18, 190))
        end_first = (declared + dt.timedelta(minutes=mins)).replace(second=0)
        # the responders name the services one by one: the first with the declaration or within minutes, the rest as
        # the call finds them, now and then one only in the review after the incident has ended
        named = {}
        named[lead] = declared + (dt.timedelta(0) if r.random() < 0.5 else dt.timedelta(seconds=int(r.integers(30, 200))))
        for x in svcs[1:]:
            if r.random() < 0.12:
                named[x] = end_first + dt.timedelta(hours=float(r.uniform(2, 40)))
            else:
                named[x] = declared + dt.timedelta(seconds=int(r.integers(240, min(45 * 60, mins * 60 - 120))))
        order = sorted(svcs, key=lambda x: named[x])
        closed = end_first + dt.timedelta(hours=float(r.uniform(4, 70)))
        commander = str(r.choice(["ipereira", "fvalente", "mdomingues", "ateixeira", "tnogueira"]))
        inc.append({"incident_id": iid, "declared_at": declared, "resolved_at": closed.replace(microsecond=0),
                    "severity": sev, "services": ";".join(K.TRACE_NAME[x] for x in order),
                    "title": _title(svcs, r), "commander": commander})
        timeline.append((iid, declared, "declared", _title(svcs, r)))
        timeline.append((iid, declared + dt.timedelta(seconds=int(r.integers(5, 50))), "severity set", sev))
        timeline.append((iid, declared + dt.timedelta(seconds=int(r.integers(20, 120))), "commander assigned", commander))
        for x in order:
            timeline.append((iid, named[x], "service added", K.TRACE_NAME[x]))
        if not posted:
            timeline.append((iid, end_first + dt.timedelta(minutes=int(r.integers(-10, 5))), "mitigated", ""))
            timeline.append((iid, closed.replace(microsecond=0), "resolved", ""))
            continue
        # the status page: a post a few minutes after the declaration on the components of the services named by
        # then; a component joins the post when a service on it is named while the incident is still open
        post_at = (declared + dt.timedelta(minutes=int(r.integers(2, 9)))).replace(second=0)
        comp_from = {}
        for x in order:
            if named[x] < end_first:
                c = K.COMPONENT[x]
                at = max(post_at, (named[x] + dt.timedelta(minutes=1)).replace(second=0))
                if c not in comp_from or at < comp_from[c]:
                    comp_from[c] = at
        comps = sorted(comp_from, key=K.COMPONENTS.index)
        ends = {}
        for j, c in enumerate(sorted(comps, key=lambda c: comp_from[c])):
            ce = end_first if j == 0 else end_first + dt.timedelta(minutes=int(r.integers(5, 45)))
            ends[c] = ce
            changes.append({"component": c, "status": "degraded_performance" if sev != "SEV1" else "partial_outage",
                            "at_local": to_lisbon(comp_from[c])})
            changes.append({"component": c, "status": "operational", "at_local": to_lisbon(ce)})
        fin = max(ends.values())
        posts.append({"post_id": "sp-%s" % format(int(r.integers(10 ** 9, 10 ** 10)), "x"),
                      "name": _public(comps, r), "components": comps, "created_local": to_lisbon(post_at),
                      "resolved_local": to_lisbon(fin)})
        timeline.append((iid, fin + dt.timedelta(minutes=int(r.integers(-6, 4))), "mitigated", ""))
        timeline.append((iid, closed.replace(microsecond=0), "resolved", ""))
        for x in svcs:
            if named[x] < fin:
                iv[x].append((max(declared, named[x]), fin))
            need.discard((half, x))
    truth = {}
    for x in K.SVC:
        merged = []
        for a_, b_ in sorted(iv[x]):
            if merged and a_ <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], b_)
            else:
                merged.append([a_, b_])
        m = [0.0, 0.0]
        for a_, b_ in merged:
            for hi_, (lo, hi) in enumerate(((Y0, H1_END - dt.timedelta(hours=1)), (H1_END - dt.timedelta(hours=1), Y1))):
                lo_, up = max(a_, lo), min(b_, hi)
                if up > lo_:
                    m[hi_] += (up - lo_).total_seconds() / 60
        truth[x] = m
    changes.sort(key=lambda x: (x["at_local"], x["component"], x["status"]))
    inc.sort(key=lambda x: x["declared_at"])
    timeline.sort(key=lambda x: (x[1], x[0]))
    return inc, posts, changes, timeline, truth


def _title(svcs, r):
    s = svcs[0]
    words = {"journey-search": "Search results slow", "fares": "Fare quotes timing out", "places": "Stop autocomplete errors",
             "seat-map": "Seat maps not loading", "booking": "Booking confirmations failing", "payments": "Card payments declined",
             "tickets": "E-tickets delayed", "accounts": "Sign-in failures", "partner-gateway": "Operator availability calls failing",
             "notifications": "Booking emails delayed"}
    return words[s] + (" (%d services)" % len(svcs) if len(svcs) > 1 else "")


def _public(comps, r):
    return {"Search": "Slow or failing journey searches", "Booking and payments": "Problems completing bookings",
            "Tickets and boarding passes": "Delays sending tickets", "Sign-in and accounts": "Trouble signing in"}[comps[0]]
