"""task464 architecture 6: the generating process.

Per partner and intake: applications arrive, a ballot orders them, places are offered to the top of the order,
refused places are passed further down the order until the partner's waitlist effort runs out or the enrolment
census date closes the intake, learners who are offered a place enrol if they would accept it, and achievement
follows a latent readiness plus the partner's own effect on the learners who enrol.

Readiness drives BOTH acceptance and achievement. That is the selection which makes any attendance-based
comparison wrong, and it is why the ballot is the only honest contrast in the pack.
"""
import numpy as np
import world as W


def simulate(seed=None):
    seed = W.SEED if seed is None else seed
    rng = np.random.default_rng(seed)
    cells, rows = {}, []
    for p in W.PARTNERS:
        for ik in W.INTAKES:
            n = W.apps_for(p, ik["code"])
            places = W.places_for(p, ik["code"])
            readiness = rng.normal(0, 1, n)
            order = rng.permutation(n)                  # the ballot draw: random order
            rank = np.empty(n, int)
            rank[order] = np.arange(n)                  # rank 0 is first in the ballot
            # Who would take a place up if offered one. Calibrated to the partner's own take-up.
            accepts = readiness > np.quantile(readiness, 1 - p["takeup"])
            won_first = rank < places

            # The waitlist cascade. A refused place is passed to the next applicant in ballot order. The partner
            # works its list only so far: cascade is the share of refused places it refills before the census
            # date, which is set by how early it ballots and whether it keeps a standing reserve list.
            refused = int((won_first & ~accepts).sum())
            target = int(round(p["cascade"] * refused))
            boundary, refilled, r = places - 1, 0, places
            while r < n and refilled < target:
                if accepts[order[r]]:
                    refilled += 1
                boundary = r
                r += 1
            offered = rank <= boundary                  # ever offered a place, first round or down the list
            enrolled = offered & accepts

            pr = p["base"] + W.SELECTION * readiness + p["effect"] * enrolled
            achieved = rng.random(n) < np.clip(pr, 0.01, 0.99)

            cells[(p["key"], ik["code"])] = dict(
                n=n, places=places, rank=rank, order=order, offered=offered, won_first=won_first,
                enrolled=enrolled, achieved=achieved, readiness=readiness,
                boundary=int(boundary), refused=refused, refilled=refilled,
                m=int(offered.sum()), filled=int(enrolled.sum()))
            for i in range(n):
                rows.append((p["key"], ik["code"], int(rank[i]), bool(offered[i]), bool(won_first[i]),
                             bool(enrolled[i]), bool(achieved[i]), float(readiness[i])))
    return dict(seed=seed, cells=cells, rows=rows)


def _contrast(c, treat_mask, control_mask):
    y = c["achieved"]
    if treat_mask.sum() == 0 or control_mask.sum() == 0:
        return 0.0
    return float(y[treat_mask].mean() - y[control_mask].mean())


def ladder(sim):
    """Every route a competent analyst can take, per partner, pooled over the two intakes.

    golden  additional achievements per 100 PLACES FUNDED, the unit the authority commits:
            100 * sum_over_intakes(m_i * clean_contrast_i) / sum_over_intakes(places_i)
    rung3   the same clean contrast expressed per 100 LEARNERS OFFERED a place
    rung2b  the first-round ballot contrast grossed per funded place
    rung2   the first-round ballot contrast per learner offered (the textbook ITT)
    rung1   ballot winners who enrolled against ballot losers
    rung0   learners who enrolled against learners who did not
    """
    out = {}
    for p in W.PARTNERS:
        num_clean = num_first = 0.0
        m_tot = pl_tot = 0
        enr_y = enr_n = nen_y = nen_n = 0
        w1_y = w1_n = lo_y = lo_n = 0
        for ik in W.INTAKES:
            c = sim["cells"][(p["key"], ik["code"])]
            clean = _contrast(c, c["offered"], ~c["offered"])
            first = _contrast(c, c["won_first"], ~c["won_first"])
            num_clean += clean * c["m"]
            num_first += first * c["m"]
            m_tot += c["m"]
            pl_tot += c["places"]
            y = c["achieved"]
            enr_y += y[c["enrolled"]].sum(); enr_n += int(c["enrolled"].sum())
            nen_y += y[~c["enrolled"]].sum(); nen_n += int((~c["enrolled"]).sum())
            we = c["won_first"] & c["enrolled"]
            w1_y += y[we].sum(); w1_n += int(we.sum())
            lo_y += y[~c["won_first"]].sum(); lo_n += int((~c["won_first"]).sum())
        out[p["key"]] = dict(
            golden=100.0 * num_clean / pl_tot,
            rung3=100.0 * num_clean / m_tot,
            rung2b=100.0 * num_first / pl_tot,
            rung2=100.0 * num_first / m_tot,
            rung1=100.0 * (w1_y / w1_n - lo_y / lo_n),
            rung0=100.0 * (enr_y / enr_n - nen_y / nen_n),
            places=pl_tot, offers=m_tot,
            filled=sum(sim["cells"][(p["key"], i["code"])]["filled"] for i in W.INTAKES))
        out[p["key"]]["fill"] = out[p["key"]]["filled"] / pl_tot
    return out


def rank_by(lad, key):
    return sorted(lad, key=lambda k: -lad[k][key])


if __name__ == "__main__":
    s = simulate()
    lad = ladder(s)
    print("seed", s["seed"], " applications", len(s["rows"]))
    print("%-4s %7s %7s %7s %7s %7s %8s | %6s %7s %7s" % (
        "key", "rung0", "rung1", "rung2", "rung2b", "rung3", "GOLDEN", "fill", "places", "offers"))
    for p in W.PARTNERS:
        d = lad[p["key"]]
        print("%-4s %7.2f %7.2f %7.2f %7.2f %7.2f %8.2f | %6.3f %7d %7d" % (
            p["key"], d["rung0"], d["rung1"], d["rung2"], d["rung2b"], d["rung3"], d["golden"],
            d["fill"], d["places"], d["offers"]))
    print()
    for k in ("rung0", "rung1", "rung2", "rung2b", "rung3", "golden"):
        print("%-7s %s" % (k, " > ".join(rank_by(lad, k))))
    g = rank_by(lad, "golden")
    print()
    print("call %s, runner-up %s, margin %.3fx" % (g[0], g[1], lad[g[0]]["golden"] / lad[g[1]]["golden"]))
    for k in ("rung0", "rung1", "rung2", "rung2b", "rung3"):
        print("  golden's rank on %-7s %d of 6 (that route names %s)" % (
            k, rank_by(lad, k).index(g[0]) + 1, rank_by(lad, k)[0]))
