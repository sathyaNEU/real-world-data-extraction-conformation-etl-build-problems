"""The ask layer's ceiling, measured on the cut pack: the cracker (lands the call, runs the hygiene battery, executes
every filed sentence and reads every helper document) and each single crack, ask by ask, scored cell by cell against
the golden at the asks' own rounding (counts exact, euros and minutes to half a unit). The mirror is the best response
off the call; it takes the cracker's ask paths, so its leakage is the cracker's kept share. Prints the cracker sheet
and the pair ceiling the design note's ask sheet carries.

    python3 ceiling.py [pack_dir]
"""
import csv
import datetime as dt
import json
import os
import sys

import common as K
import analysis as AN

HERE = os.path.dirname(os.path.abspath(__file__))


def deploys_pipeline_only(t, g):
    """Section 5.1 executed on the delivery pipeline's log: production, succeeded, a release the first time a version
    goes out, a rollback a version first released before the running one."""
    d = json.load(open(os.path.join(t, K.FILES["deploys"])))["deployments"]
    out = {s: {"releases": 0, "rollbacks": 0} for s in K.SVC}
    by = {}
    for x in d:
        if x["environment"] == "production" and x["outcome"] == "succeeded":
            by.setdefault(g.by_trace[x["service"]], []).append((x["started_at"], x["version"]))
    for s, ev in by.items():
        ev.sort()
        first, running = {}, None
        for t_, v in ev:
            if v not in first:
                first[v] = t_
                out[s]["releases"] += 1
            elif running is not None and v != running and first[v] < first[running]:
                out[s]["rollbacks"] += 1
            running = v
    return out


def deploys_history_only(t, g):
    """Section 5.1 executed on the cluster's rollout history alone, its first revision read as a release."""
    hist = list(csv.DictReader(open(os.path.join(t, K.FILES["rollouts"]))))
    out = {s: {"releases": 0, "rollbacks": 0} for s in K.SVC}
    by = {}
    for h in hist:
        by.setdefault(g.by_trace[h["deployment"]], []).append((h["changed_at_utc"], h["image"].rsplit(":", 1)[1]))
    for s, ev in by.items():
        ev.sort()
        first, running = {}, None
        for t_, sha in ev:
            if sha not in first:
                first[sha] = t_
                out[s]["releases"] += 1
            elif running is not None and sha != running and first[sha] < first[running]:
                out[s]["rollbacks"] += 1
            running = sha
    return out


def costs_by_tag(t, g, team_split=False):
    """Section 5.3 executed on the billing lines: each line to the service its tag names, US dollars at its invoice's
    rate, VAT and the support plan out, credits netted, dated by usage; a line tagged only with a team goes to no
    service, or (team_split) is shared evenly among the team's services."""
    rate = {row["invoice_id"]: float(row["usd_eur_rate"]) for row in csv.DictReader(open(os.path.join(t, K.FILES["invoices"])))}
    tag_svc = {c["Cost tag (service=)"]: c["Service"] for c in g.cat}
    team_svcs = {}
    for c in g.cat:
        team_svcs.setdefault(c["Team tag (team=)"], []).append(c["Service"])
    out = {s: [0.0, 0.0] for s in K.SVC}
    for row in csv.DictReader(open(os.path.join(t, K.FILES["billing"]))):
        if row["line_type"] == "tax":
            continue
        tags = dict(p.split("=", 1) for p in row["resource_tags"].split(";") if "=" in p)
        eur = float(row["cost"]) * (rate[row["invoice_id"]] if row["currency"] == "USD" else 1.0)
        half = 0 if row["usage_date"] < "2026-07-01" else 1
        if "service" in tags:
            out[tag_svc[tags["service"]]][half] += eur
        elif team_split and tags.get("team") in team_svcs:
            for s in team_svcs[tags["team"]]:
                out[s][half] += eur / len(team_svcs[tags["team"]])
    return {s: [round(v[0], 2), round(v[1], 2)] for s, v in out.items()}


def incidents_final_list(t, g):
    """Section 5.2 executed with each incident's services taken from the export's column, every service named from the
    declaration; posts matched by component and time, the page's Lisbon clock converted, the end at operational, a
    service's minutes counted once."""
    import asks as A
    st = json.load(open(os.path.join(t, K.FILES["status"])))

    def utc(local):
        tt = dt.datetime.strptime(local, "%Y-%m-%d %H:%M")
        for off in (1, 0):
            u = tt - dt.timedelta(hours=off)
            if A.lisbon_offset(u) == off:
                return u
        return tt
    posts = [{"components": set(p["components"]), "created": utc(p["created_at"])} for p in st["incidents"]]
    ops = {}
    for c in st["component_status_changes"]:
        if c["status"] == "operational":
            ops.setdefault(c["component"], []).append(utc(c["at"]))
    for v in ops.values():
        v.sort()
    comp = {c["Service"]: c["Status page component"] for c in g.cat}
    iv = {s: [] for s in K.SVC}
    for row in csv.DictReader(open(os.path.join(t, K.FILES["incidents"]))):
        decl = dt.datetime.strptime(row["declared_at_utc"], "%Y-%m-%d %H:%M:%S")
        names = [g.by_trace[x] for x in row["services"].split(";")]
        match = [p for p in posts if p["components"] & {comp[x] for x in names}
                 and dt.timedelta(0) <= p["created"] - decl.replace(second=0) <= dt.timedelta(minutes=15)]
        if not match:
            continue
        p = match[0]
        end = max(min(x for x in ops[c] if x > p["created"]) for c in p["components"])
        for s in names:
            iv[s].append((decl, end))
    h1_end = dt.datetime(2026, 6, 30, 23, 0)
    res = {}
    for s, lst in iv.items():
        merged = []
        for a, b in sorted(lst):
            if merged and a <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        m = [0.0, 0.0]
        for a, b in merged:
            for i, (lo, hi) in enumerate(((dt.datetime(2026, 1, 1), h1_end), (h1_end, dt.datetime(2027, 1, 1)))):
                lo_, hi_ = max(a, lo), min(b, hi)
                if hi_ > lo_:
                    m[i] += (hi_ - lo_).total_seconds() / 60
        res[s] = m
    return res


def kept_deploys(got, gold):
    return sum((got[s]["releases"] == gold[s]["releases"]) + (got[s]["rollbacks"] == gold[s]["rollbacks"])
               for s in K.SVC)


def kept_pairs(got, gold):
    return sum(sum(round(a) == round(b) for a, b in zip(got[s], gold[s])) for s in K.SVC)


def measure(t):
    g = AN.Golden(t)
    gd, gc, gi = g.deploys(), g.costs(), g.incidents()
    rows = []
    a_c = kept_deploys(deploys_pipeline_only(t, g), gd)
    b_c = kept_pairs(costs_by_tag(t, g), gc)
    c_c = kept_pairs(incidents_final_list(t, g), gi)
    rows.append(("Ask A, cracker: section 5.1 on the delivery pipeline's log", "A", a_c))
    rows.append(("Ask B, cracker: section 5.3 by tag, team-tagged lines to no service", "B", b_c))
    rows.append(("Ask B, cracker variant: team-tagged lines shared evenly in the team", "B",
                 kept_pairs(costs_by_tag(t, g, team_split=True), gc)))
    rows.append(("Ask C, cracker: section 5.2 with the export's services named from the declaration", "C", c_c))
    rows.append(("Ask A, one crack: the rollout history alone, its cutover revision a release", "A",
                 kept_deploys(deploys_history_only(t, g), gd)))
    total = a_c + b_c + c_c
    L = total / 60.0
    on, off = 45 + 55 * L, 12 + 55 * L
    return rows, L, on, off


def main(argv):
    t = argv[1] if len(argv) > 1 else os.path.join(HERE, "..", "target")
    rows, L, on, off = measure(t)
    print("| Path (cracker = lands the call, runs the battery, executes filed documents) | Kept of 20 | Verdict |")
    print("|---|---|---|")
    for label, ask, k in rows:
        print("| %s | %d of 20 | %s |" % (label, k, "miss" if k < 20 else "keeps"))
    print()
    print("Mirror leakage: %.1f per cent of ask weight (the mirror takes the cracker's ask paths off the call)." % (100 * L))
    print("Pair ceiling: %.1f (cracker on the call %.1f, mirror off it %.1f)." % ((on + off) / 2, on, off))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
