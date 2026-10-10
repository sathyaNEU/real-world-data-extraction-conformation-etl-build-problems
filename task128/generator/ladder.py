"""The ladder. Every rung is computed forward from the records: the split of 300 tickets across the
six estates and the exploitable host exposures it takes out in November.

Rungs:
  R0  flag exploitability, no drain limit (the office scanner ranked on the office objective)
  R1  cut-day score exploitability (the close-out rule), no drain limit
  R2  cut-day score, drains bounded by the day's-peak headroom (88 payments, 48 checkout)
  R3  cut-day score, drains bounded by the window-hours headroom (96 payments, 120 checkout);
      colocated tickets credited with only the ticket package, densest packages first  [stop rung]
  R4  as R3 for the cloud estates, but each colocated drain valued at the whole host it returns:
      one ticket per colocated estate on a package every host carries, naming the most exposed
      hosts  [decisive]

The estate order is fixed: payments, checkout, search, media, tools, pipeline.
"""
from params import ESTATES, COLO, CLOUD, DENSE, TICKETS, CODE


def cloud_values(spine_rows, pool, rule):
    """{(estate, package): count} of findings exploitable under `rule` ("flag" or "score")."""
    byid = {}
    for ent in pool.values():
        for c in ent["bulk"]:
            byid[c.id] = c
        if ent["exp"]:
            byid[ent["exp"].id] = ent["exp"]
    vals = {}
    for r in spine_rows:
        c = byid[r["cve"]]
        hit = c.flag if rule == "flag" else (c.final >= 0.10)
        if hit:
            k = (r["estate"], r["package"])
            vals[k] = vals.get(k, 0) + 1
    return vals


def colo_pkg_values(hosts, rule):
    """{(estate, package): (total_exposure, per_host_rate, n_hosts)} under per-package valuation.

    Exposure of a package = its exploitable findings across hosts carrying it. rule selects which
    findings count. All colocated findings are exploitable-now by construction, so "flag" and
    "score" differ only through the scanner flag, which the provider feed does not carry; the
    colocated feed is scored on the finding being open, so both readings agree on the colocated
    estates. The per-host rate ranks packages for the drain budget.
    """
    out = {}
    for est in COLO:
        agg = {}
        for h in hosts[est]:
            seen = {}
            for pkg, cve in h.findings:
                seen[pkg] = seen.get(pkg, 0) + 1
            for pkg, cnt in seen.items():
                t, nh = agg.get(pkg, (0, 0))
                agg[pkg] = (t + cnt, nh + 1)
        for pkg, (t, nh) in agg.items():
            out[(est, pkg)] = (t, t / nh, nh)
    return out


def colo_drains_per_package(hosts, budget):
    """Spend `budget` drains per colocated estate on packages with the most exposure per drained
    host, densest first, crediting only the ticket package. Returns {estate: (tickets, exposure)}.
    """
    res = {}
    for est in COLO:
        # candidate packages ranked by exposure per host carrying them (dense roles lead)
        host_pkg = []
        agg = {}
        for h in hosts[est]:
            cnt = {}
            for pkg, cve in h.findings:
                cnt[pkg] = cnt.get(pkg, 0) + 1
            for pkg, c in cnt.items():
                agg.setdefault(pkg, []).append((h.hid, c))
        rate = {pkg: sum(c for _, c in rows) / len(rows) for pkg, rows in agg.items()}
        order = sorted(agg, key=lambda p: (-rate[p], p))
        used, exposure, tickets = 0, 0, 0
        for pkg in order:
            if used >= budget:
                break
            rows = sorted(agg[pkg], key=lambda x: (-x[1], x[0]))
            took = 0
            for hid, c in rows:
                if used >= budget:
                    break
                exposure += c
                used += 1
                took += 1
            if took:
                tickets += 1
        res[est] = (tickets, exposure)
    return res


def colo_whole_host(hosts, budget):
    """Value each drain at the whole host it returns: drain the `budget` most exposed hosts, one
    ticket per estate. Returns {estate: (1, exposure, drained_host_ids)}.
    """
    res = {}
    for est in COLO:
        ranked = sorted(hosts[est], key=lambda h: (-h.whole(), h.hid))
        drained = ranked[:budget]
        exposure = sum(h.whole() for h in drained)
        res[est] = (1, exposure, [h.hid for h in drained])
    return res


ERANK = {e: i for i, e in enumerate(ESTATES)}


def _cloud_sorted(cloud_vals):
    return sorted(((v, ERANK[e], e, p) for (e, p), v in cloud_vals.items() if v > 0),
                  key=lambda x: (-x[0], x[1], x[3]))


def assemble_unbounded(colo_pkg, cloud_vals):
    """R0/R1: no drain limit. Rank every package ticket across all six estates by exposure, take
    the top 300. Returns (split dict, total exposure, boundary info)."""
    cands = [(t, ERANK[e], e, p) for (e, p), (t, rate, nh) in colo_pkg.items()]
    cands += [(v, ERANK[e], e, p) for (v, _, e, p) in _cloud_sorted(cloud_vals)]
    cands.sort(key=lambda x: (-x[0], x[1], x[3]))
    chosen = cands[:TICKETS]
    split = {e: 0 for e in ESTATES}
    total = 0
    for v, _, e, p in chosen:
        split[e] += 1
        total += v
    last_in = chosen[-1]
    first_out = cands[TICKETS] if len(cands) > TICKETS else None
    return split, total, (last_in, first_out)


def assemble_bounded(colo_res, cloud_vals, colo_exposure_key=1):
    """R2/R3/R4: colocated tickets fixed by the colocated computation, cloud fills the rest.

    colo_res: {estate: (tickets, exposure, ...)}. Returns (split, total, boundary)."""
    colo_tickets = sum(colo_res[e][0] for e in COLO)
    colo_exp = sum(colo_res[e][1] for e in COLO)
    n_cloud = TICKETS - colo_tickets
    cs = _cloud_sorted(cloud_vals)
    chosen = cs[:n_cloud]
    split = {e: 0 for e in ESTATES}
    for e in COLO:
        split[e] = colo_res[e][0]
    total = colo_exp
    for v, _, e, p in chosen:
        split[e] += 1
        total += v
    last_in = chosen[-1] if chosen else None
    first_out = cs[n_cloud] if len(cs) > n_cloud else None
    return split, total, (last_in, first_out)


def colo_ticket_package(hosts, drained_ids, est, reg):
    """The package the standard's ticketing rule selects for the colocated estate under the
    whole-host reading: of the packages with an open finding on every drained host, the one whose
    highest-scoring open finding on those hosts scores highest. Returns (package, coverage)."""
    idset = set(drained_ids)
    cover, top = {}, {}
    for h in hosts[est]:
        if h.hid in idset:
            for pkg, cve in h.findings:
                top[pkg] = max(top.get(pkg, 0.0), reg.by_id[cve].final)
            for pkg in {p for (p, c) in h.findings}:
                cover[pkg] = cover.get(pkg, 0) + 1
    full = [p for p, n in cover.items() if n == len(idset)]
    best = sorted(full, key=lambda p: (-top[p], p))
    return (best[0], cover[best[0]]) if best else (None, 0)


def answer_tickets(W):
    """The 300-ticket cut list in rank order (estate, package, hosts_reached, exposures)."""
    from params import COLO
    import windows as WIN
    wh, _ = WIN.nov_drains()
    r4raw = W["rungs"]["r4raw"]
    rows = []
    for e in COLO:
        drained = golden_drained(W, e, wh[e])
        pkg, cov = colo_ticket_package(W["hosts"], drained, e, W["reg"])
        rows.append({"estate": e, "package": pkg, "hosts": len(drained),
                     "exposures": W["rungs"]["r4c"][e][1], "colocated": True})
    # cloud chosen tickets
    for v, _, e, p in W["chosen_cloud"]:
        rows.append({"estate": e, "package": p, "hosts": v, "exposures": v, "colocated": False})
    rows.sort(key=lambda r: (-r["exposures"], ERANK[r["estate"]], r["package"]))
    return rows


def golden_drained(W, est, budget):
    ranked = sorted(W["hosts"][est], key=lambda h: (-h.whole(), h.hid))
    return [h.hid for h in ranked[:budget]]
